# Gosford steer axle, long form: shot list

Draft for owner approval. Not published. Target: YouTube, 16:9, about 4 minutes 30 seconds at Presenter A's pace. Also cut a 9:16 version from the same timeline for Shorts.

Source: NHVR court outcomes, https://www.nhvr.gov.au/law-policies/prosecutions/court-outcomes (entry: 22 September 2026, Gosford Local Court, Company, AS 69045). Checked 30 September 2026.

Facts from the entry: tray truck; M1 Pacific Motorway at Mount White; steer axle permitted 6.5 t, assessed 8.74 t, 134.5%; severe risk breach, 1 x s96(1)(c) HVNL; cause: load placed too far forward on the tray; no prior offences since 2015, first offence; "a big mistake", "incorrect loading puts pressure on the road"; specific and general deterrence; maximum $108,000; conviction; fine $21,000; the five educational points.

TRTT commentary, not the court's words: the explanation of why a forward load overloads the steer axle; the effect on tyres, steering and braking; the "Monday morning checklist" framing; the no-blame question; "a good record helps you, it does not make the loading plan optional".

Presenter: Presenter A, voice Marty V3 (cloned, Hedra `voice_6717b15d`), lip-sync Hedra Avatar. Record the script as three or four takes of 60 to 90 seconds rather than one 4-minute take, to avoid drift. Suggested breaks: after "severe risk breach"; after "where the weight sits"; after point five; to the end.

## Timeline

| Section | Voice (start) | Picture | On-screen text |
|---|---|---|---|
| Cold open 0:00 | "A tray truck is driving down the M1..." | Highway truck from behind (`5ddcd4b2`), then presenter | None until "Then it gets weighed." |
| The numbers 0:25 | "The steer axle..." | Presenter; cut to steer-axle close-up (`1bee6536` is the B-double, use the Gosford steer-axle clip `5e43d71a`) | Steer axle limit: 6.5 t. Measured: 8.74 t. 134.5% |
| The law 0:45 | "Under the Heavy Vehicle National Law..." | Presenter; graphic of the three breach bands (built in the editor) | s96(1)(c) HVNL. Severe risk breach. |
| The court 1:00 | "On 22 September 2026..." | Presenter; weighbridge (`51a2927f`) | Gosford Local Court, 22 Sep 2026. Fine $21,000. Maximum $108,000. |
| The cause 1:25 | "So how does a company..." | Forklift placing the crate forward (`5f1e8f02`); then a simple side-view diagram of a tray with the load forward and the steer axle highlighted (editor graphic) | Load placed too far forward |
| Why it matters 2:05 | "Why does the court care..." | Steer-axle close-up (`5e43d71a`); roadside inspection (`a8c63254`) | None |
| The five points 2:30 | "Let's look at what the regulator says..." | Presenter with numbered cards 1 to 5 appearing as spoken; cutaways: weigh pad (`6764c110`), pre-start walk-around (`04689b08` or `8b241abe`), depot paperwork clip | 1 Mass limits, told to loaders and drivers. 2 A way to weigh. 3 Training. 4 Pre-start checklist. 5 Load distribution plan. |
| No-blame question 3:35 | "Here is the no-blame question..." | Presenter only, no cutaway | Who notices before the truck reaches the motorway? |
| The fine 3:55 | "One last point on the fine..." | Presenter | $21,000 of a possible $108,000 |
| Close 3:17 | "The full case entry..." | Presenter | Source: NHVR court outcomes, 22 September 2026 |

## Labels

Owner decision 3 October 2026: no on-screen AI banner, no end card, no spoken disclaimer. YouTube's altered-or-synthetic content disclosure switched on at upload. Description carries the NHVR link and, if wanted, the disclaimer. The last caption is the source line.

## Status

- [x] Script written and passes `voice_lint`
- [x] Owner approved the render, 3 October 2026
- [x] Marty V3 audio as four takes (Hedra elevenlabs-v3): 35.7 s, 57.7 s, 65.1 s, 42.2 s. Takes in `takes/`
- [x] Hedra Avatar renders per take, 3:4 720p (Hedra Avatar ignores a 16:9 request and keeps the portrait's shape): take1 `job_7c423342`, take2 `job_1e8f1f07`, take3 `job_07adf6d6`, take4 `job_89bf93c2`. About 1,400 credits
- [x] Two editor graphics built with Pillow: `graphic-breach-bands.png`, `graphic-tray-side.png`
- [x] First cut assembled with `tools/stitch_video.py edit.json`: 3 min 23 s, 1920x1080. Presenter and the 9:16 b-roll are fitted over a blurred fill; 720p review copy sent to the owner 3 October 2026
- [ ] Owner reviews the first cut (timing of captions and cutaways is estimated from word position and may need nudging)
- [x] B-roll regenerated at 16:9 in Higgsfield, 3 October 2026 (job IDs in `edit.json` under `_sources.broll_16x9`); inspection still redone so the driver's door sits on the right-hand side. Owner uploaded the seven clips to the Hedra library (assets 396f48cf highway, 5fd80a3c steer, 2b316d25 weighbridge, 7d9b2d3f forklift, 403f4e37 prestart, 17d8475a bdouble, 2bffcec6 inspection)
- [x] Second cut assembled with the 16:9 clips, 3 min 23 s, cutaways fill the frame; 720p review and 1080p web master sent to the owner 3 October 2026
- [x] RobinReach draft created 3 October 2026, post 1056612, YouTube only, unlisted, playlist Chain of Responsibility, labels AI presenter / Trust lane / Gosford steer axle / Long-form. Nothing scheduled. Switch the altered-content disclosure on at publish
- [ ] Owner remark 3 October: prefers Esa (Presenter B) as the presenter for this one. Decision pending on re-voicing and re-rendering with Esa (Hedra Avatar about 1,400 credits, VEED about 5,600) and swapping the media on the draft
- [ ] 9:16 Shorts cut from the same takes
