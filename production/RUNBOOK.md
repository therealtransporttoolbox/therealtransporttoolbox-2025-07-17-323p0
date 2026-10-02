# TRTT AI video runbook

The repeatable flow for scripted video with AI presenters and characters. Approved assets, IDs and voices live in `production/characters.json`. Nothing goes live without the owner's sign-off, and every AI video is labelled.

## Roles

- **Trust lane:** real Herby, real documents, real case reviews. Presenter A and Presenter B may front explainers. Never used for testimonials or scenes presented as real.
- **Reach lane:** Big Red and Bigfoot Barry. Fiction, friendly, harmless. Each clip teaches one correct legal point tied to a real, sourced case and links to the trust lane.

## The flow (one episode)

1. **Pick the story.** Start from a primary source: the NHVR court outcomes page, an NHVR notice, an ATSB report. Record the URL and the date checked. Facts on screen come only from the source.
2. **Scaffold.** `python3 tools/new_episode.py <slug> --title "..." --source "<url>" --characters presenter_a,big_red`. This creates `drafts/<slug>/` with script, shot list, captions and checklist files.
3. **Write the script.** Year 7 reading level. No em-dashes, no exclamation marks in scripts, no lists of exactly three, no formula openers. Add "General information, not legal advice." for regulatory content.
4. **Lint.** `python3 tools/voice_lint.py drafts/<slug>/script.txt --platform tiktok` (or the target platform). Fix every ERROR. Decide each WARN.
5. **Fact check.** Tick each figure and section number against the source. Note the source line and the "last verified" date.
6. **Voice audio.** Hedra `generate_speech`, model `elevenlabs-v3`, with the character's approved voice. Big Red is the exception: Higgsfield `text2speech_v2` (variant `elevenlabs`) with the Benji preset.
7. **Start frame.** Use an approved still from `characters.json`. For a new scene, generate it with the character's Element and check it (below) before animating.
8. **Lip-sync.**
   - Presenter A and Barry: Hedra Avatar (`hedra-avatar`, settings in `characters.json`).
   - Big Red: Higgsfield `seedance_2_5` `omni_reference` with the still as `start_image` and the imported audio as `audio_references`.
9. **B-roll.** Generate a still first, check orientation, then animate. See the orientation rules below.
10. **Edit list.** Timeline with cutaways every 4 to 6 seconds, on-screen text added in the editor (never by the models), captions, labels, end card.
11. **Owner review.** The owner watches and listens. The owner is the quality gate for faces, voices, mouths and orientation.
12. **Draft, not publish.** Save to RobinReach as a draft. Scheduling follows the Sunday review.

## Labels (mandatory)

- Persistent on-screen line: "Dramatisation - AI presenter" (presenters) or "Fiction. AI characters." (characters).
- End card for presenters: "AI presenter. Scripts written and checked by Herby Green." plus the source line.
- Switch on each platform's AI-generated content label.

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
| Voice does not match the original | Higgsfield tool `elevenlabs_v4` returns 422; `text2speech_v2` ignores stability settings | Use Hedra `elevenlabs-v3` with the cloned voice |
| Hedra rejects an audio or image link | External URLs must come from Hedra `upload_file`; links are one-hour signed URLs and easy to mistype | Upload, then use the exact URL immediately, or use a library asset ID. Uploaded files become library assets once used |
| Mouth movement shows AI tells | Video model lip-sync is weak | Use Hedra Avatar, cut away often, keep clips short |
| Lip-sync drifts in parts of a long take (seen on Presenter B, 49 s, Hedra Avatar) | Single long take | Compare VEED Fabric 1.0 and Kling AI Avatar v2 (pro) on the same still and audio; split the audio into 10 to 15 second takes; cover drifting sections with b-roll in the edit |
| Truck on the wrong side of the road | Model default | Orientation rules above, still first |
| Cartoonish character | Prompt too playful | Documentary phone-photo wording and the NOT list |
| Higgsfield 429 | Too many jobs at once | Wait for running jobs, resubmit the rest |
| Higgsfield "IN THE DARK" preset recommendation | Preset suggestion | Resubmit with `declined_preset_id` from `characters.json` |
| Hedra `generate_video` rejects a pasted signed URL or fails on a start frame | Long signed URLs are easy to corrupt when copied by hand; upload links expire after an hour | Pass Hedra library asset IDs (`asset_...`) where possible. If a start frame is missing from the library, ask the owner to drop the still into the Hedra library in the browser, then look it up with `query_assets` and use its short ID |
| Higgsfield tool rejects job lists | Schema expects `[{index, job_id}]` | Use that shape |

## Consistency checks before owner review

- [ ] Facts match the source; source line and date recorded.
- [ ] `voice_lint` passes.
- [ ] Voice is the approved one for each character.
- [ ] Trucks left of road, driver on the right, no coupling detail, no stray vehicles.
- [ ] Characters look like their approved stills; nothing frightening.
- [ ] Labels and end card present.
- [ ] Nothing published; draft only.

## Cost habits

Use the cheaper preview first: stills before video, short clips before long, one voice test before the full line. Hedra Avatar at 720p is about 5 US cents a second.
