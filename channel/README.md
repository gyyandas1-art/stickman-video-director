# Stickman Comedy Meme Shorts

This channel is now configured for **English-language stickman comedy meme Shorts**. The uploaded 14.17-second bodybuilding meme is the visual reference for the production direction.

## Channel defaults

- Format: YouTube Shorts, vertical 9:16
- Initial duration target: 15–30 seconds (the reference is approximately 14 seconds)
- Language: English
- Genre: visual stickman comedy, absurd humour, relatable situations and punchline-driven memes
- Visual direction: hand-drawn 2D cartoon linework; expressive, exaggerated characters; muted olive-grey backgrounds; restrained blue-grey props; slightly imperfect ink outlines; simple but readable environments
- Motion: pose-to-pose character animation, anticipation, squash/stretch, prop interaction, reaction shots, quick cuts and camera reframing
- Audio: original voiceover only when it improves the joke; sound effects and music must be licensed, original, or otherwise cleared
- Publishing: manual upload by the channel owner; no YouTube OAuth or automatic publishing
- Operating target: under 10 minutes/day after the pipeline is proven
- Cost target: ₹0/month where free tiers allow; free-tier availability and quotas are not guaranteed

## Reference analysis

The supplied reference file is a 720×1280, 24 fps, approximately 14.17-second Short. Its visible language is not a minimal line-only stick figure on a blank canvas. It combines a comic muscular character, expressive hand-drawn contours, a muted olive-grey setting, blue-grey gym equipment, exaggerated physical poses and abrupt visual beats. The new pipeline must aim at this language rather than the previous psychology renderer.

The reference is for style analysis only. Do not reuse its footage, character design, exact sequence, audio, script, or distinctive assets. Build original characters and jokes.

## Production requirements

Read [meme-format-spec.md](./meme-format-spec.md) before creating an episode.

A pipeline is not considered complete merely because a script, still images, or an MP4 file exists. A publish candidate must pass:
1. Originality and joke-clarity review.
2. Character consistency across all shots.
3. Visible purposeful motion in every story beat.
4. Strong opening visual and a readable punchline.
5. Audio mix and timing review.
6. 9:16 phone-size inspection.
7. Human approval before upload.

## Current implementation status

The first renderer is intentionally a limited engineering prototype: it draws each frame procedurally and encodes a real MP4. It does not yet match the uploaded reference's painted character finish or acting quality. Its synthesized SFX are placeholders for timing, not a finished soundtrack. Never label its output publish-ready without visual/audio review.

- [x] Channel direction changed from psychology to stickman comedy memes on a dedicated branch.
- [x] Reference video inspected for duration, frame size, frame rate and visual design.
- [x] Editorial and visual production specification added.
- [ ] Topic/script generator adapted to comedy formats.
- [ ] Reusable original character model and expression/pose library.
- [x] First deterministic pose-animated 2D prototype renderer added (`render_comedy_prototype.py`); this is a procedural prototype, not the final character rig.
- [x] Prototype MP4 workflow added with encode checks for 720×1280, 24 fps and H.264 output.
- [x] Original synthesized impact SFX and timed captions included in the prototype (no voiceover or music yet).
- [ ] Reusable original character model sheets, facial-expression library and reusable pose/limb rig.
- [ ] Upgrade animation to stronger articulated acting, prop contact, camera cuts and more convincing physical comedy.
- [ ] Voiceover, sound design and final audio mix.
- [ ] Inspect decoded MP4 visually and acoustically; human phone-size review remains mandatory.

The previous psychology implementation is not treated as the production pipeline for this channel. Its open pull request remains separate and is not merged into this branch.

## Credentials and safety

Never commit API keys. Store provider credentials only in GitHub Actions repository secrets. Do not paste secrets into chat or logs. Do not add YouTube OAuth; final uploads remain manual.
