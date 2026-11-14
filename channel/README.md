# Psychology Stickman Shorts — channel setup

This directory stores the channel's editorial and production configuration. It does not contain API credentials.

## Locked channel defaults

- Language: English
- Niche: psychology and human behaviour
- Format: native 9:16 YouTube Shorts
- Renderer style: B1 Minimal Hand-Drawn
- Target length: 45–60 seconds
- Initial cadence: 3 videos per week
- Budget: ₹0/month
- Human approval: mandatory before scheduling or publishing

## Important production boundary

The upstream Stickman Video Director repository provides a renderer and detailed creative/acceptance contracts. It does **not** automatically turn a topic into a researched script, generated voice, original scene artwork, aligned captions, a completed B1 manifest, and an approved MP4. Those stages require project-local adapters and actual media generation. Do not mark an episode rendered or approved merely because a workflow or unit test passed.

## Required credentials (add only through GitHub Actions repository secrets)

- `GEMINI_API_KEY`: optional provider credential for a configured Gemini adapter. The current repository does not bundle a Gemini TTS/script adapter for this channel.
- YouTube OAuth client/refresh-token material: required only if a YouTube Data API uploader is implemented. Never store OAuth JSON or tokens in this directory, commits, Actions artifacts, or logs.

A secret name in documentation is not evidence that a secret has been configured or that a provider call works.

## Next implementation gates

1. Implement and test the selected text-generation and TTS adapters.
2. Implement original story-specific B1 portrait scene authoring; do not reuse the sample's poses/scenes as a template.
3. Align captions to the actual generated voice track.
4. Build and validate a complete B1 project manifest and render an MP4.
5. Independently inspect actual encoded picture and sound against the B1 portrait and shared acceptance contracts.
6. Add a persistent idempotent episode queue and only then schedule unattended production.
7. Add YouTube OAuth upload/scheduling only after manual approval has been demonstrated.

## Local/cloud runtime check

From `skills/directing-stickman-videos`:

```bash
npm ci
node scripts/autopilot.mjs doctor
node scripts/autopilot.mjs workflow --style B1 --ratio 9:16
npm test
```

The GitHub Actions workflow currently validates the runtime only. It intentionally does not claim to generate or publish videos until the missing production adapters and approval gates exist.
