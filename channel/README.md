# Psychology Stickman Shorts — channel setup

This directory stores channel configuration and production guidance. It never stores API credentials.

## Locked channel defaults

- Language: English
- Niche: psychology and human behaviour
- Format: native 9:16 YouTube Shorts
- Renderer style: B1 Minimal Hand-Drawn
- Target length: 45–60 seconds
- Initial cadence: 3 videos per week
- Target ongoing effort: no more than 10 minutes/day
- Target service budget: ₹0/month (subject to free-tier quotas and availability)
- Publishing: manual upload by the channel owner; no YouTube OAuth or automatic publishing

## Gemini credential

Store `GEMINI_API_KEY` only in GitHub Actions repository secrets:

https://github.com/gyyandas1-art/stickman-video-director/settings/secrets/actions

Never put the key in this directory, a commit, workflow log, artifact, or chat. A configured secret is not proof that a Gemini API call has succeeded.

## Implemented stage 1: draft and narration

The repository now includes:
- `channel/gemini-adapter.mjs`: calls Gemini for a structured English psychology script and uses Gemini TTS to create a WAV narration.
- `.github/workflows/psychology-episode-draft.yml`: manually triggered workflow; accepts a topic and uploads the script plus WAV as a 7-day artifact.
- Unit tests for episode-draft validation.

To run it from an Android phone:
1. Open the repository's **Actions** tab.
2. Select **Psychology episode draft and narration**.
3. Tap **Run workflow**, enter a topic, and run it.
4. Open the completed run and download the `psychology-episode-draft` artifact.
5. Review the script and source URLs; do not assume the model's references are genuine without checking them.

Gemini free-tier quotas can change. Free-tier data may be used to improve Google's products; review the current Gemini API terms before sending any private or sensitive information. Do not send personal stories or identifiable third-party details to the model.

## Not yet implemented

The adapter is only stage 1. It does **not** create a finished video. Remaining work:
1. Verify source URLs and factual claims against primary references.
2. Align captions to the actual generated narration.
3. Create original story-specific B1 portrait artwork and native scene composition.
4. Build and validate the complete B1 project manifest.
5. Render the MP4 and run technical checks.
6. Inspect the actual encoded video and audio; preserve the B1 visual-acceptance gate.
7. Deliver a review preview and require your approval before a full production run.

The workflow must not label an episode rendered or approved because an API call, workflow, or unit test succeeded. It must not fabricate an independent review.

## Editorial safeguards

- Cite factual claims in the episode's source notes.
- Prefer established psychological concepts and distinguish evidence from interpretation.
- No invented studies, statistics, quotations, diagnoses, or unsupported neuroscience claims.
- Use original examples and a distinct scene plan for every episode.
- Avoid repetitive, mass-produced scripts and identical scene templates.

## Renderer runtime check

From `skills/directing-stickman-videos`:

```bash
npm ci
node scripts/autopilot.mjs doctor
node scripts/autopilot.mjs workflow --style B1 --ratio 9:16
npm test
```

The runtime-check workflow validates dependencies and tests only. YouTube OAuth and automatic publishing are intentionally out of scope; you will upload approved MP4s manually.
