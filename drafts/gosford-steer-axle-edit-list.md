# Gosford steer-axle short: edit list

Draft for owner approval. Not published or queued anywhere.

Script: `drafts/gosford-steer-axle-short.txt` (about 49 seconds spoken). Presenter A clip: Hedra job `job_03a7a0c3-0d6b-4f96-8a73-c8612d7715fc` (3:4, 720p). Times are approximate; trim to the actual audio in the editor.

## Layers

- Base: the presenter clip for the full length. Audio comes only from this clip.
- Cutaways (muted, 2 to 3 seconds each) laid over the presenter while his voice continues. Cut away every 4 to 6 seconds.
- On-screen text is added in the editor, never by the AI models.
- Captions burned in, matching the script word for word.

## Timeline

| Time | Voice | Picture | On-screen text |
|---|---|---|---|
| 0:00 to 0:06 | "A tray truck drove down the M1 at Mount White. Its steer axle was allowed to carry 6.5 tonnes. It was carrying 8.74 tonnes." | Presenter. At "drove down the M1" cut to the load-forward tray truck (5ddcd4b2) for 3 seconds. | Steer axle limit: 6.5 t / Measured: 8.74 t |
| 0:06 to 0:12 | "That is 134.5 percent of the limit. The offence was classed as a severe risk breach." | Weighbridge (51a2927f) for 3 seconds, back to presenter. | 134.5% of the limit. Severe risk breach. |
| 0:12 to 0:18 | "The cause was simple. The load sat too far forward on the tray." | Forklift and crate (5f1e8f02). | Load placed too far forward |
| 0:18 to 0:30 | "The company had no prior offences since 2015. On 22 September 2026, Gosford Local Court still convicted it and fined it $21,000. The maximum was $108,000." | Presenter throughout. | Gosford Local Court, 22 Sep 2026. Fine: $21,000. Maximum: $108,000. |
| 0:30 to 0:38 | "The court called it a big mistake. It said incorrect loading puts pressure on the road." | Roadside inspection (a8c63254) for 3 seconds, back to presenter. | None |
| 0:38 to 0:46 | "So who checked where that load sat before the truck left? If nobody can answer, the gap is in the system, not just the driver." | Presenter close, no cutaway on the question. | Who checked before it left? |
| 0:46 to 0:49 | "General information, not legal advice." | Presenter. | General information, not legal advice. |

## Labels and end card (mandatory)

- Persistent on-screen line for the whole clip: "Dramatisation - AI presenter".
- End card, 2 seconds: "AI presenter. Scripts written and checked by Herby Green." plus "Source: NHVR court outcomes, Gosford Local Court, 22 September 2026".
- Switch on TikTok's, YouTube's, Instagram's and Facebook's AI-generated content label when uploading.

## Checks before it goes into the draft queue

- Play the cutaways and confirm every truck is on the left of the road with the driver on the right.
- Check every figure on screen against the NHVR court outcomes page: 6.5 t, 8.74 t, 134.5%, $21,000, $108,000, 22 September 2026.
- Run the caption text through `python3 tools/voice_lint.py --platform tiktok`.
- Save as a RobinReach draft only. Publish after the Sunday review.
