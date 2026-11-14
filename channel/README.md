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

The intended API workflow is:
- Gemini text model for an evidence-aware script and scene plan.
- Gemini TTS for English narration.
- Actual-audio word alignment for captions.
- Original story-specific artwork and native portrait composition.
- B1 rendering, technical checks, and human review.
- Download the finished MP4 from a GitHub Actions artifact and upload it manually in YouTube Studio.

Gemini free-tier quotas can change. Free-tier data may be used to improve Google's products; review the current Gemini API terms before sending any private or sensitive information. Do not send personal stories or identifiable third-party details to the model.

## Production and approval boundary

The upstream renderer is a production tool, not a topic-to-video service. The channel pipeline must explicitly create and validate every stage. It must not label an episode rendered or approved because an API call, workflow, or unit test succeeded.

B1 portrait has a native-composition and visual-acceptance contract. The workflow must not bypass it or fabricate an independent review. The first usable episode should be delivered as a review preview; full production should follow only after the actual preview is reviewed and approved.

## Editorial safeguards

- Cite factual claims in the episode's source notes.
- Prefer established psychological concepts and distinguish evidence from interpretation.
- No invented studies, statistics, quotations, diagnoses, or unsupported neuroscience claims.
- Use original examples and a distinct scene plan for every episode.
- Avoid repetitive, mass-produced scripts and identical scene templates.

## Current runtime check

From `skills/directing-stickman-videos`:

```bash
npm ci
node scripts/autopilot.mjs doctor
node scripts/autopilot.mjs workflow --style B1 --ratio 9:16
npm test
```

The existing runtime-check workflow validates dependencies and tests only. It does not yet generate a complete episode or upload/publish a video.
