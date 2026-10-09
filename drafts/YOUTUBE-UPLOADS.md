# YouTube upload pack

Finished videos ready for YouTube, as of 9 October 2026. Each video has its own folder with the video file, the YouTube text (title, description, chapters, tags, pinned comment, upload settings) and, for the long-form videos, a 1280x720 thumbnail.

| # | Video | Format | Length | Presenter | RobinReach |
|---|---|---|---|---|---|
| 01 | Albury work diary | Short, 1080x1920 | 0:45 | Esa | Drafted, post 1056383 |
| 02 | Gosford steer axle | Long-form, 1920x1080 | 3:23 | Marty | Drafted, post 1056612 |
| 03 | Scheduling: the text at 9 pm | Long-form, 1920x1080 | 5:20 | Esa | Not yet |

Source of truth for the text is `drafts/<video>/youtube-description.txt`. Thumbnails are `drafts/<video>/youtube-thumbnail.png`. Video files are not kept in git; full-quality masters can be rebuilt with `tools/stitch_video.py` or `tools/stitch_short.py` from each folder's `edit.json`.

Every upload: altered or synthetic content disclosure ON, not made for kids, category Education, playlist Chain of Responsibility in Heavy Vehicle National Law. Publish each video once, either through RobinReach or directly in YouTube Studio, not both.

Suggested release order: 03 first as the anchor long-form, then 01 as a Short that points to it, then 02.
