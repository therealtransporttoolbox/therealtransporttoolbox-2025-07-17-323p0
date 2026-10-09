# Cowork handover: TRTT video pipeline on the owner's machine

Paste the block below as the first message of a Cowork session on the computer that has Premiere Pro, After Effects and AEJuice. It gives the local session everything it needs; the rest lives in the repo.

---

You are continuing the TRTT AI video pipeline that was built in a cloud Claude Code session. This machine has Premiere Pro, After Effects and AEJuice installed, which the cloud session could not reach. Work in the repo `therealtransporttoolbox/therealtransporttoolbox-2025-07-17-323p0`, branch `claude/trtt-socials-branding-review-hifdmb`. Clone or pull it first.

Read these before doing anything else, in this order:
1. `production/RUNBOOK.md` (the 12-step flow, labels decision, orientation rules, failures table)
2. `production/characters.json` (approved characters, Element IDs, stills, voices, lip-sync models; never substitute)
3. `.claude/skills/trtt-video-pipeline/SKILL.md`
4. `drafts/albury-work-diary/edit.json`, `shotlist.md` and `captions.txt`

Standing decisions from the owner (do not revisit):
- No on-screen "Dramatisation / AI presenter" banner, no end card, no spoken "General information, not legal advice" line. The platform AI-content toggle is switched on at upload instead, and the source line goes in the caption.
- Two lanes: trust lane (Presenter A Marty, Presenter B Esa, real cases) and reach lane (Big Red, Bigfoot Barry, fiction that teaches one sourced legal point).
- Presenter B voice is Esa. It exists in Hedra (ElevenLabs v3 clone) and in Higgsfield as voice Element `52b27fcf-0e0e-4405-b1f5-bba90dd739f0` (Eleven v4). Both approved 3 October 2026.
- Big Red voice is Benji (Higgsfield preset), Barry is Charlie (Hedra). Lip-sync models per character are in `characters.json`.
- Every truck or cab prompt carries the Australian left-hand traffic wording from the runbook. Trucks are framed from behind or rear three-quarter. Never prompt couplings or air lines.
- Nothing publishes. RobinReach posts are saved as drafts only; scheduling is the owner's Sunday review.
- Scripts: Year 7 reading level, no em-dashes, no exclamation marks, no lists of exactly three, no formula openers. Run `python3 tools/voice_lint.py <script> --platform <platform>` before voicing.

What the cloud session could not do, and this session should (Premiere first):
1. **Albury short, RobinReach draft.** Do this after the Premiere export is approved, using that export as the media. The approved v2 cut is a 45 s 1080x1920 file. The ffmpeg version of the same cut can be rebuilt with `FFMPEG=<path> python3 tools/stitch_short.py drafts/albury-work-diary/edit.json` if Premiere is unavailable. Create one RobinReach draft for TikTok (profile 16266), Instagram Reels (13241) and YouTube Shorts (16267) via the RobinReach connector: `media_direct_upload_create`, PUT the file, `media_direct_upload_finalize`, `posts_validate`, `posts_create` with `post_status: "draft"`. Caption uses `captions.txt` wording plus the source line "Source: NHVR court outcomes, 7 September 2026." Note in the draft that the AI-content toggle must be on at publish.
2. **Premiere assembly of the same cut (the main job).** Build the Albury short in Premiere Pro from `drafts/albury-work-diary/edit.json`. Spec:
   - Sequence: 1080x1920, 25 fps, 48 kHz stereo, name `albury-work-diary-v2`.
   - Media: import the presenter clip and the four cutaways (`station.mp4`, `cab.mp4`, `camera.mp4`, `highway.mp4`) from the owner's download folder. If they are missing, download them from the Hedra library using the asset IDs in the `_sources` block of `edit.json`.
   - V1: presenter clip from 0 s for the full 45.16 s, scaled to fill the 9:16 frame, audio kept.
   - V2: each cutaway placed at its listed start and trimmed to its listed end (station 1.5 to 5.0 s, cab 6.5 to 9.5 s, camera 9.8 to 12.8 s, highway 33.0 to 36.5 s). Cutaway audio muted. Presenter audio runs underneath throughout.
   - V3: one Essential Graphics text layer per caption at the listed in and out times, wording exactly as in `edit.json`, line breaks as written. Style: bold sans (Inter or Arial Bold), 50 px equivalent, white text on a TRTT navy (#002E47) box at 60 percent opacity, centred, bottom third, clear of the TikTok and Reels UI (keep the box above the bottom 300 px).
   - Final caption "Source: NHVR court outcomes, 7 September 2026." from 45.3 s is now off the end of the presenter clip, so place it over the last 3 s of the presenter instead (42.2 to 45.1 s), or extend the sequence with a 3 s hold on the final presenter frame.
   - AEJuice: use one lower-third preset for the first caption and simple dip-to-colour or whip transitions on the cutaway joins only if they look quiet. No banner, no end card, no logo stings.
   - Drive Premiere by script (ExtendScript through the Premiere scripting API, or UXP) rather than by clicking, so the build is repeatable from `edit.json`. Save the script as `tools/premiere_build.jsx` (or `.js`) and commit it. Keep `.prproj` files out of git.
   - Export: H.264, 1080x1920, 25 fps, VBR 2-pass 10 Mbps target, AAC 192 kbps, to the owner's chosen folder. Record the export path and date in `shotlist.md`.
   - Owner reviews the export before anything goes to RobinReach.

3. **After Effects bridge.** Run the Higgsfield MCP command `/use-after-effects` and follow its installation and verification references. This installs a local Node MCP server that drives After Effects. Only report it connected after a live call succeeds. Do not edit any existing After Effects project without being asked.
4. **Next renders, on the owner's say-so only.** Gosford long-form (script and shot list in `drafts/gosford-steer-axle-longform/`, about 2,500 Hedra credits, Marty V3 voice, Hedra Avatar) or a Big Red or Barry short on the Albury case. Ask which before spending credits.

Things that did not carry over from the cloud session: scratch clips (re-download from Hedra by asset ID), the GitHub pull request subscription (PR 2 on this repo is the site redirect; leave it for the owner to merge), and the cloud network allow-list (irrelevant here).

Commit work to the same branch with clear messages. Do not create a pull request unless asked.

---
