# Colour re-render status: DETAILED colour redraw (Blake, Oct 13 2026)

The quick tinted mode was rejected and its queue stopped (9:40 PM PT). Each case is now redrawn in the Cases 4-9 style:
detailed people3/people4 characters (dkit.py swaps every peg-doll, same suspect pose/size), hand-painted plates in
`src/art_caseNN_color.py`, part sprites clip-only (no borders), same question bar / unique opening / narration / timings.
Build: `python3 src/art_color.py NN` on the box -> stills at 1/3/20/45/80 s checked -> art shipped to streambox ->
case appended to `/home/tidewhistle/color-queue.txt`; unit `tw-color-queue` encodes one case at a time via capped
`/usr/local/sbin/tw-render --case NN-color --format all --skip-art`. Log: `/home/tidewhistle/color-queue.log`.
Outputs: `<slug>-color-vertical.mp4`, `<slug>-color-wide.mp4`, `shorts/<slug>-color-short-part1/2.mp4` (B&W kept).

Updated Oct 13 10:04 PM PT. ETAs assume ~58 min per case, sequential.

| Case | Built (redrawn + stills OK) | Queued | Rendered | Copied | Uploaded | ETA (PT) |
|---|---|---|---|---|---|---|
| 25 | yes | yes | rendering | no | no | 10:41 PM |
| 26 | yes | yes | no | no | no | 11:39 PM |
| 20 | yes | yes | no | no | no | 12:37 AM |
| 21 | yes | yes | no | no | no | 1:35 AM |
| 22 | yes | yes | no | no | no | 2:33 AM |
| 23 | yes | yes | no | no | no | 3:31 AM |
| 24 | yes | yes | no | no | no | 4:29 AM |
| 10 | yes | yes | no | no | no | 5:27 AM |
| 11 | yes | yes | no | no | no | 6:25 AM |
| 12 | yes | yes | no | no | no | 7:23 AM |
| 13 | yes | yes | no | no | no | 8:21 AM |
| 14 | yes | yes | no | no | no | 9:19 AM |
| 15 | yes | yes | no | no | no | 10:17 AM |
| 16 | yes | yes | no | no | no | 11:15 AM |
| 17 | yes | yes | no | no | no | 12:13 PM |
| 18 | yes | yes | no | no | no | 1:11 PM |
| 19 | yes | yes | no | no | no | 2:09 PM |
| 27 | no | no | no | no | no |  |
| 28 | no | no | no | no | no |  |
| 29 | no | no | no | no | no |  |
| 30 | no | no | no | no | no |  |

Case 3 B&W copy: skipped (Case 3 already has a colour version).
