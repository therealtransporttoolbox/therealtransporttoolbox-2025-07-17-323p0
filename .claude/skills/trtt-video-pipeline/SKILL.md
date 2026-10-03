---
name: trtt-video-pipeline
description: Produce TRTT AI presenter and character videos (Presenter A, Presenter B, Big Red, Bigfoot Barry) for Australian transport law content. Use whenever the user wants a new episode, script-to-video clip, character clip, truck or cab b-roll, voice or lip-sync work, or a social short built from a case. Uses the approved assets, voices and settings in production/characters.json and the steps in production/RUNBOOK.md.
---

# TRTT video pipeline

Follow `production/RUNBOOK.md` exactly and take every ID, voice and setting from `production/characters.json`. Do not invent IDs or swap voices.

## Start of every episode

1. Read `production/RUNBOOK.md` and `production/characters.json`.
2. Take the story from a primary source (NHVR court outcomes, notices, ATSB). Record the URL and the date checked. Every figure on screen must come from it.
3. Run `python3 tools/new_episode.py <slug> --title "..." --source "<url>" --characters <keys>` to scaffold `drafts/<slug>/`.
4. Write the script and captions, run `python3 tools/voice_lint.py` on both, and fix every ERROR.
5. Produce voice, then lip-sync, then b-roll, using the approved tools per character (see the runbook).
6. Write the edit list in `drafts/<slug>/shotlist.md`.
7. Commit and push to the feature branch. Never publish. Save to RobinReach only as a draft, and only after the owner has approved.

## Hard rules

- Owner is the quality gate: you cannot view Higgsfield or Hedra media from here, so never claim a clip looks right. Ask the owner to judge faces, voices, mouths and truck orientation.
- Every road or cab prompt carries the Australian orientation language and negatives. Generate a still first and get it checked before animating.
- Never prompt trailer couplings or air lines. Keep other vehicles out of cab shots. No legible text or logos in prompts.
- Characters stay photorealistic and friendly. No fire, emergency vehicles or frightening scenes.
- Label every AI video and use the platform AI labels.
- Hedra needs its own upload URLs; copy them exactly or use library asset IDs. Never fabricate a URL.
- Update `production/characters.json` when the owner approves something new, and record known failures in the runbook.
