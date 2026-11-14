# Stickman Comedy Meme — Production Specification

## 1. Creative promise

Every Short must deliver one instantly understandable visual joke. The viewer should understand the setup without reading a paragraph or hearing a long explanation. The punchline must be a visual event, not merely a final caption.

Preferred comedy engines:
- Escalation: a small action causes increasingly ridiculous consequences.
- Contrast: confident expectation versus humiliating reality.
- Misinterpretation: a character misunderstands a simple situation.
- Overconfidence: a character's plan collapses in a visual way.
- Physical comedy: timing, impact, recoil, transformation and reaction.
- Relatable absurdity: gym, school, work, friendship, relationships, gaming and daily life.

Avoid generic "random funny" scenes. Each episode needs a clear setup, escalation and payoff.

## 2. Reference-derived art direction

The supplied reference is a 720×1280, 24 fps, 14.17-second vertical animation. Use these observable traits as a guide:
- 2D hand-drawn cartoon appearance, not clean corporate vector art.
- Thick, slightly irregular black outlines.
- Expressive, simplified faces and exaggerated anatomy/poses.
- Muted olive-grey background with restrained blue-grey objects.
- Off-white character/body fills and dark charcoal gym props.
- Simple environments with enough perspective to ground props.
- Clear silhouettes and large readable actions.
- Short visual beats and abrupt changes in pose or composition.

Do not copy the reference's actual character, drawings, scene order, timing, footage or audio. Develop a distinct recurring cast and original props.

## 3. Character bible

Create a reusable original cast before batch production. Each character needs:
- Stable head/body proportions and outline thickness.
- Front, side and three-quarter views.
- Neutral, happy, smug, confused, shocked, angry, embarrassed and exhausted expressions.
- Idle, walk, run, lift/push, fall, recoil, point and celebrate poses.
- A limited, repeatable palette.
- A model sheet that can be used as a reference for every generated shot.

Do not redesign a character between scenes. If image generation is used, each scene prompt must include the character identity and model-sheet reference.

## 4. Short structure and timing

Default target: 15–30 seconds. Use 10–16 purposeful visual beats; a shorter joke may use fewer. Do not pad to hit a duration.

Suggested timing:
- 0.0–1.0 s: visual hook; start with action or an unusual image.
- 1.0–5.0 s: establish the situation and character goal.
- 5.0–12.0 s: escalate through new actions or consequences.
- 12.0–20.0 s: strongest reversal or punchline.
- Final 0.5–1.5 s: reaction, button or seamless loop when it improves the joke.

Every beat must change something: pose, expression, prop state, camera framing, location, or story information. Avoid static image slideshows with only captions moving.

## 5. Animation language

Prioritize:
- Anticipation before a lift, jump, impact or reveal.
- Follow-through and recoil after movement.
- Squash/stretch for comedic impacts, used consistently.
- Facial expression changes that sell the joke.
- Prop interaction with visible contact and believable continuity.
- Reaction shots and deliberate pauses before punchlines.
- Camera push-ins, pans or reframing only when they clarify or amplify the joke.

Motion must be visible at normal phone playback size. Avoid relying on tiny movements that disappear on a 6–7 inch display.

## 6. Editing and sound

- Vertical 9:16 composition; keep faces and key props inside mobile-safe areas.
- Prefer fast cuts driven by action; use holds only for anticipation or punchline timing.
- Captions are optional, concise and timed to speech. They must not cover faces or the action.
- Sound effects should reinforce physical events and reactions, not clutter every frame.
- Voiceover is optional. Do not add narration when the visual joke works better silently.
- Use only original, licensed, public-domain or otherwise cleared music and sound effects.
- Mix dialogue clearly above music; prevent clipping and abrupt audio cutoffs.

## 7. Script and storyboard contract

Every episode package must contain:
- Working title and one-sentence joke premise.
- Hook visual in the first second.
- Setup, escalation and punchline stated explicitly.
- Shot list with start/end time, framing, character action, expression, prop state, background and transition.
- Character IDs used in each shot.
- Sound/music cues with rights/source notes.
- Thumbnail frame and title/description suggestions.
- A final review checklist.

Reject a script if the joke cannot be explained in one sentence, the punchline is weak, or shots repeat the same visual information.

## 8. Technical delivery

- MP4, H.264 video, AAC audio.
- 1080×1920 preferred; 720×1280 acceptable for prototypes only.
- 24 or 30 fps, consistent throughout each episode.
- Portrait 9:16; no letterboxing.
- Captions/metadata as separate files when present.
- Verify duration, dimensions, frame rate, audio stream and decode integrity with ffprobe/FFmpeg.

## 9. Quality gates

A successful workflow run is not proof of a good video. Each episode must be reviewed for:
- Hook clarity in the first second.
- Joke comprehension without explanation.
- Punchline strength and timing.
- Character consistency.
- Purposeful animation rather than static slides.
- Scene continuity and prop interaction.
- Readable framing on a phone.
- Clean audio and properly timed effects.
- Originality and asset rights.

Status values:
- DRAFT: script or storyboard only.
- RENDERED: MP4 generated and technically checked.
- REVIEW_REQUIRED: awaiting human visual/audio review.
- APPROVED: owner has reviewed and approved.
- REJECTED: fails one or more creative/technical gates.

Never automatically label a video APPROVED or upload it.
