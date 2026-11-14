# Psychology Stickman Shorts — channel setup

This directory stores channel configuration and production guidance. It never stores API credentials.

## Locked channel defaults

- Language: English
- Niche: psychology and human behaviour
- Format: 9:16 portrait Shorts
- Visual direction: minimal hand-drawn stick figures on warm, faint-grid paper
- Target length: 45–60 seconds
- Initial cadence: 3 videos per week
- Target ongoing effort: no more than 10 minutes/day
- Target service budget: ₹0/month, subject to free-tier quotas and availability
- Publishing: manual upload by the channel owner; no YouTube OAuth or automatic publishing

## Gemini credential

Store `GEMINI_API_KEY` only in GitHub Actions repository secrets:

https://github.com/gyyandas1-art/stickman-video-director/settings/secrets/actions

Never put the key in this directory, a commit, workflow log, artifact, or chat. A configured secret is not proof that a Gemini API call has succeeded.

## Sample build workflow

The repository now includes:
- `channel/gemini-adapter.mjs`: Gemini structured script generation and Gemini TTS narration.
- `channel/render_spotlight_short.py`: speech alignment with faster-whisper, a procedural portrait stick-figure render, captions, thumbnail, source notes and upload description.
- `.github/workflows/psychology-short-sample.yml`: builds a Spotlight Effect sample and uploads a 14-day artifact.
- `skills/directing-stickman-videos/tests/gemini-adapter.test.mjs`: script validation tests.

The sample uses a curated academic source list: Gilovich, Medvec & Savitsky (2000) and Gilovich & Savitsky (1999). The workflow verifies that the cited source URLs respond before packaging the video. Source verification does not by itself verify every generated sentence; review the narration and sources.

### Run from an Android phone

1. Open the repository's **Actions** tab.
2. Select **Build psychology Short sample**.
3. If the run has not already started from the latest push, tap **Run workflow**.
4. Open the latest completed run.
5. Download the `psychology-spotlight-effect-sample` artifact.

The first Spotlight Effect package was successfully generated in [GitHub Actions run #43565938945](https://github.com/gyyandas1-art/stickman-video-director/actions/runs/43565938945). Its artifact is named `psychology-spotlight-effect-sample` and expires after 14 days. The package contains an MP4, thumbnail, SRT captions, source notes, YouTube description and a technical report.

## Important production boundary

The sample renderer is a procedural hand-drawn stick-figure implementation; it is **not yet an accepted B1 reference-equivalent film** and is not a substitute for the installed B1 renderer's full visual acceptance process. The first artifact's technical render completed successfully, but the package deliberately records `REVIEW_REQUIRED`; the actual MP4 has not been independently inspected at phone size in this workflow. The generated package is marked `REVIEW_REQUIRED` until the actual video, narration, captions, phone-size readability and factual claims have been inspected. Do not publish it merely because GitHub Actions succeeded.

The broader B1 workflow also requires story-specific drawing, purposeful local animation, native portrait composition and comparison with the approved reference effects. A successful encode, unit test or automated quality report cannot create independent visual acceptance or your approval.

## Editorial safeguards

- No invented studies, statistics, quotations, diagnoses or unsupported neuroscience claims.
- Use original everyday examples and a distinct scene plan for every episode.
- Distinguish established research from interpretation.
- Avoid repetitive, mass-produced scripts and identical scene templates.

## Runtime check

From `skills/directing-stickman-videos`:

```bash
npm ci
node scripts/autopilot.mjs doctor
node scripts/autopilot.mjs workflow --style B1 --ratio 9:16
npm test
```

YouTube OAuth and automatic publishing are intentionally out of scope; you will upload reviewed MP4s manually.
