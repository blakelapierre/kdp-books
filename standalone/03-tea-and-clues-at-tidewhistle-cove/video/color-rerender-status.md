# Colour re-render status: DETAILED colour redraw (Blake, Oct 13 2026)

The quick tinted mode was rejected and its queue stopped (9:40 PM PT). Each case is now redrawn in the Cases 4-9 style:
detailed people3/people4 characters (dkit.py swaps every peg-doll, same suspect pose/size), hand-painted plates in
`src/art_caseNN_color.py`, part sprites clip-only (no borders), same question bar / unique opening / narration / timings.
Build: `python3 src/art_color.py NN` on the box -> stills at 1/3/20/45/80 s checked -> art shipped to streambox ->
case appended to `/home/tidewhistle/color-queue.txt`; unit `tw-color-queue` encodes one case at a time via capped
`/usr/local/sbin/tw-render --case NN-color --format all --skip-art`. Log: `/home/tidewhistle/color-queue.log`.
Outputs: `<slug>-color-vertical.mp4`, `<slug>-color-wide.mp4`, `shorts/<slug>-color-short-part1/2.mp4` (B&W kept).

Updated Oct 13 9:46 PM PT. ETAs assume ~58 min per case, sequential.

| Case | Built (redrawn + stills OK) | Queued | Rendered | Copied | Uploaded | ETA (PT) |
|---|---|---|---|---|---|---|
| 25 | yes | yes | rendering | no | no | 10:41 PM |
| 26 | yes | yes | no | no | no | 11:39 PM |
| 20 | no | no | no | no | no |  |
| 21 | no | no | no | no | no |  |
| 22 | no | no | no | no | no |  |
| 23 | no | no | no | no | no |  |
| 24 | no | no | no | no | no |  |
| 10 | no | no | no | no | no |  |
| 11 | no | no | no | no | no |  |
| 12 | no | no | no | no | no |  |
| 13 | no | no | no | no | no |  |
| 14 | no | no | no | no | no |  |
| 15 | no | no | no | no | no |  |
| 16 | no | no | no | no | no |  |
| 17 | no | no | no | no | no |  |
| 18 | no | no | no | no | no |  |
| 19 | no | no | no | no | no |  |
| 27 | no | no | no | no | no |  |
| 28 | no | no | no | no | no |  |
| 29 | no | no | no | no | no |  |
| 30 | no | no | no | no | no |  |

Case 3 B&W copy: skipped (Case 3 already has a colour version).
