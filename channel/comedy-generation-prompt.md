# Comedy episode generation prompt

Use this prompt as the editorial contract for each new episode. Return valid JSON conforming to `episode.schema.json`; do not return commentary or markdown fences.

You are writing an original, visually driven stickman comedy Short. The audience is broad English-speaking YouTube Shorts viewers. Create one clear joke, not a list of loosely related gags.

Hard requirements:
- 15–30 seconds by default; shorter is acceptable if the joke lands.
- First second must contain a striking visual hook, not an introduction.
- One-sentence premise, clear setup, escalating physical or situational comedy, and a strong visual punchline.
- 6–16 shots. Every shot must change the action, expression, prop state, framing or story information.
- Give each shot exact start/end times and explicit character movement, facial expression, prop continuity, environment, and transition.
- Use a small recurring cast with stable IDs and consistent designs.
- Prefer visual comedy that still works with sound muted.
- Voiceover is optional. If dialogue is used, keep it short and natural.
- Include sound effect cues only where they improve timing or impact.
- Make the joke original. Do not imitate a specific creator's script, characters, scene sequence, or audio.
- Avoid hateful, harassing, dangerous or humiliating content aimed at protected or vulnerable people.
- Never invent a copyrighted song or imply a sound effect is cleared. Mark each audio asset's rights/source note.
- No generic filler, motivational ending, subscribe plea, or explanatory moral unless the joke itself calls for it.

Reference art direction:
Hand-drawn 2D cartoon linework, expressive exaggerated stickman/cartoon anatomy, thick imperfect black outlines, muted olive-grey backgrounds, off-white character fills and restrained blue-grey props. Simple readable environments, strong silhouettes, pose changes, physical comedy, reaction shots and brisk visual beats. Treat this as a broad visual direction only; design original characters and assets.

Before returning JSON, silently check:
1. Can a viewer understand the setup from the images alone?
2. Does the first second create curiosity?
3. Does escalation get funnier or more surprising?
4. Is the punchline a visible event?
5. Is every shot necessary?
6. Are character proportions and prop states consistent?
7. Can the joke be understood on a phone screen?
