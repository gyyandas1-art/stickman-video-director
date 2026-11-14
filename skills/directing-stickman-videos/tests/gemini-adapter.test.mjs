import test from 'node:test';
import assert from 'node:assert/strict';
import {validateEpisode} from '../../../channel/gemini-adapter.mjs';

const narration = Array.from({length: 112}, (_, i) => ['People','often','assume','their','choices','are','fully','deliberate','but','context','can','quietly','shape','what','they','notice'][i % 16]).join(' ');

test('accepts a complete evidence-aware short draft', () => {
  const episode = validateEpisode({
    title: 'A Psychology Concept',
    hook: 'What if the room changes your choice?',
    narration,
    scenes: Array.from({length: 6}, (_, i) => ({
      visual_metaphor: `A distinct visual metaphor for beat number ${i + 1}`,
      character_action: `The character performs action ${i + 1} with a clear prop`,
      on_screen_text: `Beat ${i + 1}`
    })),
    sources: [
      {title: 'University reference A', url: 'https://example.edu/a', claim_supported: 'A supported claim'},
      {title: 'Journal reference B', url: 'https://example.org/b', claim_supported: 'Another supported claim'}
    ]
  });
  assert.equal(episode.word_count, 112);
  assert.equal(episode.editorial_status, 'DRAFT_REQUIRES_SOURCE_AND_HUMAN_REVIEW');
});

test('rejects a script outside the short duration target', () => {
  assert.throws(() => validateEpisode({
    title: 'Too short', hook: 'A hook that is long enough',
    narration: 'Only a few words.',
    scenes: [], sources: []
  }), /too short|100–150 words/i);
});

test('rejects fabricated or missing source URLs', () => {
  assert.throws(() => validateEpisode({
    title: 'A Psychology Concept', hook: 'What if the room changes your choice?',
    narration, scenes: Array.from({length: 6}, (_, i) => ({
      visual_metaphor: `A distinct visual metaphor for beat number ${i + 1}`,
      character_action: `The character performs action ${i + 1} with a clear prop`,
      on_screen_text: `Beat ${i + 1}`
    })),
    sources: [{title: 'Unverified', url: 'not-a-url', claim_supported: 'Unknown'}]
  }), /source references/i);
});
