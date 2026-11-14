#!/usr/bin/env node
/**
 * Gemini adapter for the Psychology Stickman Shorts project.
 * Generates a structured draft and a WAV narration. This is deliberately
 * separate from the B1 renderer: it does not claim to create or approve a film.
 */
import fs from 'node:fs/promises';
import path from 'node:path';

const TEXT_MODEL = process.env.GEMINI_TEXT_MODEL || 'gemini-3.8-flash';
const TTS_MODEL = process.env.GEMINI_TTS_MODEL || 'gemini-3.8-flash-lite-tts';
const API_ROOT = 'https://generativelanguage.googleapis.com/v1beta';
const key = () => {
  const value = process.env.GEMINI_API_KEY;
  if (!value) throw new Error('GEMINI_API_KEY is missing. Add it as a GitHub Actions repository secret.');
  return value;
};

async function post(url, body) {
  const response = await fetch(url, {
    method: 'POST',
    headers: {'content-type': 'application/json', 'x-goog-api-key': key()},
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(120000)
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    const message = payload?.error?.message || `Gemini request failed with HTTP ${response.status}`;
    throw new Error(message.slice(0, 1200));
  }
  return payload;
}

function extractText(payload) {
  const parts = payload?.candidates?.[0]?.content?.parts || [];
  const text = parts.filter(p => typeof p.text === 'string').map(p => p.text).join('\n').trim();
  if (!text) throw new Error('Gemini returned no text content.');
  return text;
}

function parseJson(text) {
  const cleaned = text.replace(/^\uFEFF/, '').trim()
    .replace(/^\x60{3}(?:json)?\s*/i, '').replace(/\s*\x60{3}$/i, '');
  try { return JSON.parse(cleaned); }
  catch { throw new Error('Gemini response was not valid JSON; no episode files were written.'); }
}

export function validateEpisode(data) {
  if (!data || typeof data !== 'object' || Array.isArray(data)) throw new Error('Episode must be a JSON object.');
  if (typeof data.title !== 'string' || data.title.trim().length < 4 || data.title.length > 90) throw new Error('Episode title must be 4–90 characters.');
  if (typeof data.hook !== 'string' || data.hook.trim().length < 8) throw new Error('Episode hook is missing.');
  if (typeof data.narration !== 'string' || data.narration.trim().length < 450) throw new Error('Narration is too short for the 45–60 second target.');
  const words = data.narration.trim().split(/\s+/).length;
  if (words < 100 || words > 150) throw new Error(`Narration must be 100–150 words; received ${words}.`);
  if (!Array.isArray(data.scenes) || data.scenes.length !== 6) throw new Error('Exactly six scene beats are required.');
  for (const [i, scene] of data.scenes.entries()) {
    if (!scene || typeof scene !== 'object' ||
        typeof scene.visual_metaphor !== 'string' || scene.visual_metaphor.length < 12 ||
        typeof scene.character_action !== 'string' || scene.character_action.length < 8 ||
        typeof scene.on_screen_text !== 'string' || scene.on_screen_text.length > 42) {
      throw new Error(`Scene ${i + 1} is missing a usable visual metaphor, action, or short on-screen phrase.`);
    }
  }
  if (!Array.isArray(data.sources) || data.sources.length < 2 ||
      data.sources.some(s => typeof s.title !== 'string' || typeof s.url !== 'string' || !/^https:\/\//.test(s.url))) {
    throw new Error('At least two source references with HTTPS URLs are required; verify them before publication.');
  }
  return {...data, word_count: words, editorial_status: 'DRAFT_REQUIRES_SOURCE_AND_HUMAN_REVIEW'};
}

export async function generateEpisode(topic) {
  const prompt = `Create an original English-language psychology YouTube Short about: ${topic}

Return ONLY a JSON object with this exact structure:
{
 "title": "short title",
 "hook": "one-sentence opening hook",
 "narration": "complete spoken narration, 100 to 150 words, approximately 45–60 seconds at natural pace",
 "scenes": [
   {"visual_metaphor":"specific drawable visual idea","character_action":"specific visible stick-figure action","on_screen_text":"2–6 word phrase"}
 ],
 "sources": [{"title":"real source title","url":"https://...","claim_supported":"specific claim"}]
}

Requirements:
- Six scenes, in the same order as the narration; no generic filler.
- Explain the psychological concept accurately in plain English.
- Distinguish established findings from plausible interpretation.
- Do not invent studies, statistics, quotes, author names, journal titles, or URLs.
- Use well-known academic, university, government, or established reference sources; if uncertain, say so in the claim_supported field rather than fabricating.
- Do not diagnose viewers or make medical/neurological claims.
- The opening must create curiosity without misleading the viewer.
- Use a fresh everyday example, not a recycled viral script.
- End with a thoughtful, non-bait question.
- The on_screen_text must be concise and readable on a phone.
- Avoid claims that a single trick will reliably change someone's behaviour.`;

  const payload = await post(`${API_ROOT}/models/${TEXT_MODEL}:generateContent`, {
    contents: [{role: 'user', parts: [{text: prompt}]}],
    generationConfig: {responseMimeType: 'application/json', temperature: 0.65}
  });
  return validateEpisode(parseJson(extractText(payload)));
}

function findAudioData(value) {
  if (!value || typeof value !== 'object') return null;
  if (typeof value.data === 'string' && (value.mimeType?.startsWith('audio/') || value.mime_type?.startsWith('audio/') || value.type === 'audio')) {
    return {data: value.data, mimeType: value.mimeType || value.mime_type || 'audio/wav'};
  }
  if (Array.isArray(value)) {
    for (const item of value) { const found = findAudioData(item); if (found) return found; }
  } else {
    for (const [k, v] of Object.entries(value)) {
      if (k === 'data' && typeof v === 'string' && value.type === 'audio') return {data: v, mimeType: value.mimeType || 'audio/wav'};
      const found = findAudioData(v); if (found) return found;
    }
  }
  return null;
}

export async function synthesizeNarration(text) {
  const payload = await post(`${API_ROOT}/interactions`, {
    model: TTS_MODEL,
    input: text,
    response_format: {type: 'audio'},
    generation_config: {speech_config: [{voice: 'Kore', language: 'en-US'}]}
  });
  const audio = findAudioData(payload.steps || payload);
  if (!audio) throw new Error('Gemini TTS returned no audio data in the interaction steps.');
  const bytes = Buffer.from(audio.data, 'base64');
  if (bytes.length < 1000) throw new Error('Gemini TTS audio payload is unexpectedly small.');
  if (audio.mimeType !== 'audio/wav' && audio.mimeType !== 'audio/x-wav') {
    throw new Error(`Unexpected Gemini TTS audio format: ${audio.mimeType}; expected WAV.`);
  }
  return bytes;
}

async function main() {
  const topic = process.argv.slice(2).join(' ').trim();
  if (!topic) throw new Error('Usage: node channel/gemini-adapter.mjs "psychology topic"');
  const slug = topic.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 48) || 'episode';
  const dir = path.resolve('episodes', `${new Date().toISOString().slice(0, 10)}-${slug}`);
  await fs.mkdir(path.dirname(dir), {recursive: true});
  await fs.mkdir(dir, {recursive: false});
  const episode = await generateEpisode(topic);
  const narration = await synthesizeNarration(episode.narration);
  await fs.writeFile(path.join(dir, 'episode-draft.json'), JSON.stringify(episode, null, 2) + '\n', {flag: 'wx'});
  await fs.writeFile(path.join(dir, 'narration.wav'), narration, {flag: 'wx'});
  console.log(JSON.stringify({directory: dir, title: episode.title, word_count: episode.word_count, narration_bytes: narration.length, status: episode.editorial_status}, null, 2));
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(error => { console.error(error.message); process.exitCode = 1; });
}
