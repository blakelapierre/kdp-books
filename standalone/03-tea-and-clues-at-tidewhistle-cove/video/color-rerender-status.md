# Colour re-render status (Blake, Oct 13 2026: detailed animated colour for every B&W case)

Style: TW_KIT_STYLE=color-detailed over the existing case art (bwkit colour mode: washes, tinted scenery, auto-coloured props,
colour chrome/notebook). Configs: src/cases/caseNN_color.py. Art: work/art-NN-color. Outputs keep B&W originals:
`<slug>-color-vertical.mp4`, `<slug>-color-wide.mp4`, `shorts/<slug>-color-short-part1/2.mp4`.

Queue: streambox systemd unit `tw-color-queue` -> deploy/color-queue.sh -> /usr/local/sbin/tw-render (capped), one case at a time.
Log: streambox:/home/tidewhistle/color-queue.log (START/DONE/FAIL per case), per-case log color-queue-NN.log. Started 9:12 PM PT Oct 13.
Preview check (Case 25 colour, frames 1/3/20/45/80 s): no sprite borders, no text overlaps. ETAs PT, ~65 min per case.

| Order | Case | Built | Queued | Rendered | Copied | Uploaded | ETA (PT) |
|---|---|---|---|---|---|---|---|
| 1 | 25 | yes | yes | rendering | no | no | 10:15 PM Oct 13 |
| 2 | 26 | yes | yes | no | no | no | 11:20 PM Oct 13 |
| 3 | 20 | yes | yes | no | no | no | 12:25 AM Oct 14 |
| 4 | 21 | yes | yes | no | no | no | 1:30 AM |
| 5 | 22 | yes | yes | no | no | no | 2:35 AM |
| 6 | 23 | yes | yes | no | no | no | 3:40 AM |
| 7 | 24 | yes | yes | no | no | no | 4:45 AM |
| 8 | 10 | yes | yes | no | no | no | 5:50 AM |
| 9 | 11 | yes | yes | no | no | no | 6:55 AM |
| 10 | 12 | yes | yes | no | no | no | 8:00 AM |
| 11 | 13 | yes | yes | no | no | no | 9:05 AM |
| 12 | 14 | yes | yes | no | no | no | 10:10 AM |
| 13 | 15 | yes | yes | no | no | no | 11:15 AM |
| 14 | 16 | yes | yes | no | no | no | 12:20 PM |
| 15 | 17 | yes | yes | no | no | no | 1:25 PM |
| 16 | 18 | yes | yes | no | no | no | 2:30 PM |
| 17 | 19 | yes | yes | no | no | no | 3:35 PM |
| 18 | 27 | yes | yes | no | no | no | 4:40 PM |
| 19 | 28 | yes | yes | no | no | no | 5:45 PM |
| 20 | 29 | yes | yes | no | no | no | 6:50 PM |
| 21 | 30 | yes | yes | no | no | no | 7:55 PM Oct 14 |
| - | 3 (B&W copy) | skipped: Case 3 already has a colour version (case03_color) | | | | | |

Known gap: characters are still the simple peg-doll figures (now in colour), not the detailed people4 characters of Cases 4-9.
