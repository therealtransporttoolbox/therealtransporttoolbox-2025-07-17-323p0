# TRTT AI video runbook

The repeatable flow for scripted video with AI presenters and characters. Approved assets, IDs and voices live in `production/characters.json`. Nothing goes live without the owner's sign-off, and every AI video is labelled.

## Roles

- **Trust lane:** real Herby, real documents, real case reviews. Presenter A and Presenter B may front explainers. From 3 October 2026 the owner's default presenter for new episodes is Presenter B (Esa). Never used for testimonials or scenes presented as real.
- **Reach lane:** Big Red and Bigfoot Barry. Fiction, friendly, harmless. Each clip teaches one correct legal point tied to a real, sourced case and links to the trust lane.

## The flow (one episode)

1. **Pick the story.** Start from a primary source: the NHVR court outcomes page, an NHVR notice, an ATSB report. Record the URL and the date checked. Facts on screen come only from the source.
2. **Scaffold.** `python3 tools/new_episode.py <slug> --title "..." --source "<url>" --characters presenter_a,big_red`. This creates `drafts/<slug>/` with script, shot list, captions and checklist files.
3. **Write the script.** Year 7 reading level. No em-dashes, no exclamation marks in scripts, no lists of exactly three, no formula openers. Do not put "General information, not legal advice" in the narration (owner decision); it belongs in the caption or description if used at all.
4. **Lint.** `python3 tools/voice_lint.py drafts/<slug>/script.txt --platform tiktok` (or the target platform). Fix every ERROR. Decide each WARN.
5. **Fact check.** Tick each figure and section number against the source. Note the source line and the "last verified" date.
6. **Voice audio.** Hedra `generate_speech`, model `elevenlabs-v3`, with the character's approved voice. Big Red is the exception: Higgsfield `text2speech_v2` (variant `elevenlabs`) with the Benji preset. Esa and Marty-V3 also exist as Higgsfield voice Elements (IDs in `characters.json`) for the Higgsfield-only path below.
7. **Start frame.** Use an approved still from `characters.json`. For a new scene, generate it with the character's Element and check it (below) before animating.
8. **Lip-sync.**
   - Presenter A and Barry: Hedra Avatar (`hedra-avatar`, settings in `characters.json`).
   - Presenter B: VEED Fabric 1.0 (`veed-fabric-10`), which held sync on a 49 second take where Hedra Avatar drifted. Owner decision 3 October 2026: VEED stays the Esa render model until the Hedra credit pack runs down.
   - Big Red: Higgsfield `seedance_2_5` `omni_reference` with the still as `start_image` and the imported audio as `audio_references`.
9. **B-roll.** Generate a still first, check orientation, then animate. See the orientation rules below.
10. **Edit list.** Timeline with cutaways every 4 to 6 seconds, on-screen text added in the editor (never by the models), captions, labels, end card. For a vertical short, write it as `drafts/<slug>/edit.json` and run `python3 tools/stitch_short.py drafts/<slug>/edit.json`; for a 16:9 long-form with several presenter takes, image graphics and lower thirds, use `python3 tools/stitch_video.py drafts/<slug>/edit.json` (format in the file header) (needs ffmpeg and Pillow; clips downloaded from the Hedra library first). The Albury short was built this way.
11. **Owner review.** The owner watches and listens. The owner is the quality gate for faces, voices, mouths and orientation.
12. **Draft, not publish.** Save to RobinReach as a draft. Scheduling follows the Sunday review.

## Higgsfield-only path (script, voice, avatar, b-roll in one tool)

The owner cloned Esa into Higgsfield on 3 October 2026 so a whole episode can run there. What changes and what does not:

- Voice: `elevenlabs_v4` with `dialogue: [{text, voice_type: "element", voice_id}]`, or `text2speech_v2` variant `elevenlabs`. Both cost about 0.3 credits for a ten second line.
- Audio handoff: the voice job ID can be passed straight into a video job as `audio_references` (no Hedra upload, no signed URLs).
- Lip-sync: `seedance_2_5` `omni_reference` (up to 30 s) or `wan2_7` (up to 15 s, built for synced speech). Neither renders a 45 s take in one job, so split the script into 10 to 15 s takes and plan a cutaway at every join. Hedra VEED remains the only approved full-take option for Presenter B.
- Everything else (orientation rules, still first, owner review, drafts only) is unchanged.
- Use the Higgsfield path when the clip is short or heavy on b-roll. Use Hedra when a long continuous presenter take matters. Decide per episode in the shot list.

## Editors (Premiere Pro, After Effects, AEJuice)

Premiere Pro, After Effects and the AEJuice plug-ins run on the owner's computer and have no cloud connector. From this cloud session the only editing is `tools/stitch_short.py` (ffmpeg) and the Adobe for creativity connector's `video_render` timeline tool. Higgsfield ships a `/use-after-effects` bridge (local Node MCP server driving After Effects by ExtendScript) that installs only from a local Claude Code session on the same machine as After Effects; Cowork and cloud sessions are not supported for it. The split that works:

- Cloud session: script, lint, voice, avatar, b-roll, `edit.json`, a stitched review cut, RobinReach draft.
- Owner's machine: open the same clips in Premiere, add AEJuice lower thirds, captions and transitions from `drafts/<slug>/edit.json`, export the master. The edit list is the handover document.

## Moving clips between tools (the owner's preferred flow)

Clips generated in Higgsfield are downloaded by the owner and uploaded into the Hedra library in the browser. The session then reads them from the library by asset ID (`query_assets`), assembles the cut, and sends the owner a 1080p web master. The owner uploads that master into the RobinReach library (Library, Uploads), and the session builds the draft post from there. Two hand uploads per episode, no other setup.

## Labels

Owner decision, 3 October 2026: no on-screen "AI presenter" banner, no end card, and no spoken "General information, not legal advice" line in narration. None is a legal requirement.

What still applies:
- Switch on each platform's AI-generated or altered content toggle at upload (TikTok, YouTube, Instagram, Facebook). That is the platform's own disclosure mechanism and it protects reach.
- Put the source line (NHVR court outcomes, date) in the post caption or description. A short on-screen source caption at the end of the clip is fine.
- The disclaimer can go in the caption or description if wanted; it stays out of the narration.
- Characters (Big Red, Barry) remain plainly fictional in how they are written; a "Fiction" caption is optional.

## Australian orientation (trucks and cabs)

Higgsfield models default to US traffic. Every road or cab prompt must include:

- Positive: "Australian left-hand traffic, right-hand drive vehicle, driving in the left lane". For cabs: "steering wheel on the right side of the cabin, camera positioned from the left (passenger) seat".
- Negatives: "NOT right-hand traffic, NOT left-hand drive, NOT American road markings, NOT US highway signage".
- Generate a still first, check it, then animate. Orientation is fixed at the source image, not in the video prompt.
- For a truck on a road, frame it from directly behind or rear three-quarter. The lane is then unambiguous, and the orientation words alone were not enough for a side view (one in four failed even with the full language).
- Keep other vehicles out of cab shots. They often appear on the wrong side.
- Never prompt trailer couplings or air lines: the model draws chains between trucks or puts air lines under the trailer. Air lines connect at the back of the prime mover.
- No legible text or logos in prompts. Add text in the editor.

## Character rules

- Photorealistic, never cartoon: put "NOT cartoon, NOT mascot costume, NOT 3D render" in prompts. The humour comes from the situation.
- Friendly and harmless. No fire, emergency vehicles or frightening scenes.
- Reference each character by its Element (`<<<element_id>>>` in Higgsfield prompts) so the look holds.

## Known failures and fixes

| Symptom | Cause | Fix |
|---|---|---|
| Voice does not match the original | Higgsfield `elevenlabs_v4` returned 422 with a preset voice on 1 October; `text2speech_v2` ignores stability settings | Use Hedra `elevenlabs-v3` with the cloned voice, or the Higgsfield voice Element with `elevenlabs_v4` (worked 3 October with Esa) |
| Hedra rejects an audio or image link | External URLs must come from Hedra `upload_file`; links are one-hour signed URLs and easy to mistype | Upload, then use the exact URL immediately, or use a library asset ID. Uploaded files become library assets once used |
| Mouth movement shows AI tells | Video model lip-sync is weak | Use Hedra Avatar, cut away often, keep clips short |
| Lip-sync drifts in parts of a long take (seen on Presenter B, 49 s, Hedra Avatar) | Single long take | Compare VEED Fabric 1.0 and Kling AI Avatar v2 (pro) on the same still and audio; split the audio into 10 to 15 second takes; cover drifting sections with b-roll in the edit |
| Truck on the wrong side of the road | Model default | Orientation rules above, still first |
| Cartoonish character | Prompt too playful | Documentary phone-photo wording and the NOT list |
| Higgsfield 429 | Too many jobs at once | Wait for running jobs, resubmit the rest |
| Higgsfield "IN THE DARK" preset recommendation | Preset suggestion | Resubmit with `declined_preset_id` from `characters.json` |
| Hedra `generate_video` rejects a pasted signed URL or fails on a start frame | Long signed URLs are easy to corrupt when copied by hand; upload links expire after an hour | Pass Hedra library asset IDs (`asset_...`) where possible. If a start frame is missing from the library, ask the owner to drop the still into the Hedra library in the browser, then look it up with `query_assets` and use its short ID |
| Cloud session cannot upload to RobinReach or fetch Higgsfield audio | Environment network policy denies robinreach.com and the Higgsfield cloudfront download host | Add those hosts under Allowed domains in the cloud environment settings, or upload the sent master by hand |
| Hedra Avatar output is 3:4 although 16:9 was requested | Hedra Avatar follows the start frame's shape | For 16:9 masters, fit the 3:4 presenter over a blurred fill (`tools/stitch_video.py` does this) or make a 16:9 start frame first |
| B-roll is the wrong shape for the master | Clips were generated 9:16 for shorts | Generate b-roll at the master's aspect ratio; otherwise the stitch tool fits it over a blurred fill, or use Higgsfield `reframe` |
| Higgsfield tool rejects job lists | Schema expects `[{index, job_id}]` | Use that shape |

## Consistency checks before owner review

- [ ] Facts match the source; source line and date recorded.
- [ ] `voice_lint` passes.
- [ ] Voice is the approved one for each character.
- [ ] Trucks left of road, driver on the right, no coupling detail, no stray vehicles.
- [ ] Characters look like their approved stills; nothing frightening.
- [ ] Platform AI toggle noted for upload; source line in the caption.
- [ ] Nothing published; draft only.

## Cost habits

Use the cheaper preview first: stills before video, short clips before long, one voice test before the full line. Hedra Avatar at 720p is about 5 US cents a second.
