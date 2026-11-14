#!/usr/bin/env python3
"""Validate an authored stickman-comedy episode package using only Python stdlib."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

REQUIRED = {"title", "premise", "hook", "setup", "escalation", "punchline", "characters", "shots", "audio", "review_status"}
SHOT_REQUIRED = {"start", "end", "framing", "action", "expression", "prop_state", "background", "transition"}

def fail(message: str) -> None:
    raise ValueError(message)

def validate(data: dict) -> dict:
    if not isinstance(data, dict): fail("Episode root must be an object")
    missing = REQUIRED - data.keys()
    if missing: fail("Missing episode fields: " + ", ".join(sorted(missing)))
    for key in ("title", "premise", "hook", "setup", "punchline"):
        if not isinstance(data[key], str) or not data[key].strip(): fail(f"{key} must be non-empty text")
    if not isinstance(data["escalation"], list) or not data["escalation"] or not all(isinstance(x, str) and x.strip() for x in data["escalation"]):
        fail("escalation must be a non-empty list of non-empty strings")
    chars = data["characters"]
    if not isinstance(chars, list) or not chars: fail("At least one character is required")
    ids = []
    for c in chars:
        if not isinstance(c, dict) or not all(k in c for k in ("id", "description", "palette")): fail("Each character needs id, description and palette")
        if not isinstance(c["id"], str) or not c["id"].strip(): fail("Character id must be non-empty")
        if not isinstance(c["description"], str) or len(c["description"].strip()) < 20: fail(f"{c['id']}: character description is too short")
        if not isinstance(c["palette"], list) or not c["palette"]: fail(f"{c['id']}: palette is required")
        ids.append(c["id"])
    if len(ids) != len(set(ids)): fail("Character IDs must be unique")
    shots = data["shots"]
    if not isinstance(shots, list) or not 6 <= len(shots) <= 20: fail("Use 6–20 purposeful shots")
    previous_end = 0.0
    used_characters = set()
    actions = set()
    for i, shot in enumerate(shots, 1):
        if not isinstance(shot, dict): fail(f"Shot {i} must be an object")
        missing_shot = SHOT_REQUIRED - shot.keys()
        if missing_shot: fail(f"Shot {i} missing: " + ", ".join(sorted(missing_shot)))
        start, end = shot["start"], shot["end"]
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or start < 0 or end <= start:
            fail(f"Shot {i} has invalid timing")
        if i == 1 and start != 0: fail("First shot must start at 0 seconds")
        if start < previous_end - 0.001: fail(f"Shot {i} overlaps the previous shot")
        if start > previous_end + 0.05: fail(f"Gap before shot {i}; explicitly author intentional black/silence if desired")
        previous_end = end
        for key in SHOT_REQUIRED - {"start", "end"}:
            if not isinstance(shot[key], str) or not shot[key].strip(): fail(f"Shot {i}: {key} must be non-empty text")
        if len(shot.get("on_screen_text", "")) > 48: fail(f"Shot {i}: on-screen text exceeds 48 characters")
        if len(shot["action"].strip()) < 15: fail(f"Shot {i}: action description lacks production detail")
        action = shot["action"].strip().lower()
        if action in actions: fail(f"Shot {i}: repeated action; each beat must advance the joke")
        actions.add(action)
        for cid in shot.get("character_ids", []):
            if cid not in ids: fail(f"Shot {i}: unknown character id {cid}")
            used_characters.add(cid)
    if used_characters != set(ids): fail("Every declared character must appear in at least one shot")
    duration = previous_end
    if duration < 8 or duration > 35: fail(f"Episode duration {duration:.2f}s outside prototype target (8–35s)")
    if shots[0]["end"] > 2.0: fail("Hook must land within the first 2 seconds")
    if not isinstance(data["audio"], dict): fail("audio must be an object")
    for key in ("voiceover", "music", "effects"):
        if key not in data["audio"]: fail(f"audio.{key} is required")
    for i, effect in enumerate(data["audio"]["effects"], 1):
        if not all(k in effect for k in ("time", "cue", "rights_note")): fail(f"Audio effect {i} needs time, cue and rights_note")
        if not 0 <= effect["time"] <= duration: fail(f"Audio effect {i} is outside episode duration")
        if not effect["rights_note"].strip(): fail(f"Audio effect {i} has no rights/source note")
    if data["review_status"] not in ("DRAFT", "REVIEW_REQUIRED", "APPROVED", "REJECTED"): fail("Invalid review_status")
    if data["review_status"] == "APPROVED": fail("Automation cannot approve a video; approval must be a human action")
    return {"valid": True, "title": data["title"], "duration_seconds": duration, "shot_count": len(shots), "character_ids": ids, "status": data["review_status"], "publish_ready": False}

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("episode", type=Path)
    args = ap.parse_args()
    try:
        data = json.loads(args.episode.read_text(encoding="utf-8"))
        report = validate(data)
        print(json.dumps(report, indent=2))
        return 0
    except Exception as exc:
        print(f"EPISODE VALIDATION FAILED: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
