#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import {validateEpisode, synthesizeNarration} from './gemini-adapter.mjs';

const narration = `Imagine walking into class with a stain on your shirt. You feel as if every person has noticed it. But how many actually have? Psychologists call this the spotlight effect: we tend to overestimate how much other people notice our appearance and actions. In one experiment, students wore an embarrassing T-shirt and guessed how many classmates would remember it. They overestimated the number. The researchers found a similar pattern when people judged how noticeable their comments were in a group discussion. Why does this happen? Your own experience is vivid, so your mind uses it as the starting point. It takes effort to adjust for what everyone else is focused on. This doesn't mean nobody notices you. It means their attention is usually divided. Next time you feel watched, ask: what else might everyone be thinking about?`;

const raw = {
  title: "The Spotlight Effect: Why You Feel Everyone Is Watching",
  hook: "Why does one small mistake feel like the whole room noticed?",
  narration,
  scenes: [
    {visual_metaphor:"A bright spotlight isolates one small stain on a shirt while the rest of the room remains calm",character_action:"A stick figure notices a stain and freezes in embarrassment",on_screen_text:"FEELING EXPOSED"},
    {visual_metaphor:"A magnifying glass enlarges the character's own shirt while the background fades",character_action:"The character leans toward the magnified shirt",on_screen_text:"YOUR MIND ZOOMS IN"},
    {visual_metaphor:"Several classmates look at their own notebooks and phones rather than the shirt",character_action:"Other figures remain occupied with their own tasks",on_screen_text:"OTHERS HAVE THEIR OWN FOCUS"},
    {visual_metaphor:"A simple research card shows one participant and several observers",character_action:"The participant estimates attention while observers recall less",on_screen_text:"THE T-SHIRT EXPERIMENT"},
    {visual_metaphor:"The spotlight widens to reveal multiple people absorbed in their own thoughts",character_action:"The main character looks around as the room comes into view",on_screen_text:"ATTENTION IS DIVIDED"},
    {visual_metaphor:"The character relaxes as the spotlight fades and the room returns to normal",character_action:"The character stands upright and asks a reflective question",on_screen_text:"ZOOM OUT"}
  ],
  sources: [
    {title:"Gilovich, Medvec & Savitsky (2000), The Spotlight Effect in Social Judgment",url:"https://pubmed.ncbi.nlm.nih.gov/10707330/",claim_supported:"Original experiments on T-shirt recall and perceived prominence of comments in group discussion."},
    {title:"Gilovich & Savitsky (1999), The Spotlight Effect and the Illusion of Transparency",url:"https://www.psychologicalscience.org/journals/current-directions/1467-8721.00039/",claim_supported:"Review of egocentric bias in estimates of how much other people notice behaviour and appearance."}
  ]
};
const episode = validateEpisode(raw);
const date = new Date().toISOString().slice(0,10);
const dir = path.resolve('episodes', `${date}-spotlight-effect`);
await fs.mkdir(path.dirname(dir), {recursive:true});
await fs.mkdir(dir, {recursive:false});
await fs.writeFile(path.join(dir,'episode-draft.json'),JSON.stringify(episode,null,2)+'\n',{flag:'wx'});
const audio = await synthesizeNarration(narration);
await fs.writeFile(path.join(dir,'narration.wav'),audio,{flag:'wx'});
console.log(JSON.stringify({directory:dir,title:episode.title,word_count:episode.word_count,narration_bytes:audio.length,status:episode.editorial_status},null,2));
