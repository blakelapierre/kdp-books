# Colour re-render status: DETAILED colour redraw (Blake, Oct 13 2026)

The quick tinted mode was rejected and its queue stopped (9:40 PM PT). Each case is now redrawn in the Cases 4-9 style:
detailed people3/people4 characters (dkit.py swaps every peg-doll, same suspect pose/size), hand-painted plates in
`src/art_caseNN_color.py`, part sprites clip-only (no borders), same question bar / unique opening / narration / timings.
Build: `python3 src/art_color.py NN` on the box -> stills at 1/3/20/45/80 s checked -> art shipped to streambox ->
case appended to `/home/tidewhistle/color-queue.txt`; unit `tw-color-queue` encodes one case at a time via capped
`/usr/local/sbin/tw-render --case NN-color --format all --skip-art`. Log: `/home/tidewhistle/color-queue.log`.
Outputs: `<slug>-color-vertical.mp4`, `<slug>-color-wide.mp4`, `shorts/<slug>-color-short-part1/2.mp4` (B&W kept).

Updated Oct 14 4:20 AM PT. ETAs assume ~72 min per case, sequential (Case 28 started ~3:59 AM PT / 11:59 BST).
Queue reordered Oct 14 2:30 AM PT so upcoming Cases 27-30 render before their go-public slots (27 Wed 12:39 PM, 28 Wed 6:39 PM, 29 Thu 12:39 AM, 30 Thu 6:39 AM); live Cases 23, 24, 10-19 follow for reposts. Old order backed up as color-queue.txt.bak-20261014.

| Case | Built (redrawn + stills OK) | Queued | Rendered | Copied | Uploaded | ETA (PT) |
|---|---|---|---|---|---|---|
| 25 | yes | yes | yes | yes (swapped over B&W names, B&W kept as -bw) | n/a (upcoming; posts colour at its slot) | done |
| 26 | yes | yes | yes | yes (swapped over B&W names, B&W kept as -bw) | n/a (upcoming; posts colour at its slot) | done |
| 20 | yes | yes | yes | yes (-color names, md5 + Part 1 frames OK) | reposted Oct 14 ~2:40 AM PT (YT 2HzQbhzdJ9w/Sn3a6eijSms/NNJSMdN8zP8 + TikTok) | done |
| 21 | yes | yes | yes | yes (-color names, md5 + Part 1 frames OK) | reposted Oct 14 ~2:40 AM PT (YT fwFwjG50pNU/5BeGitjjtD0/TFvZhbShSEc + TikTok) | done |
| 22 | yes | yes | yes | yes (-color names, md5 + Part 1 frames OK) | reposted Oct 14 ~4:25 AM PT (YT v0WwIe3-TyU/FxOGkwy4t7c/fc417s2eMUw + TikTok) | done |
| 27 | yes | yes | yes | yes (swapped over B&W names, B&W kept as -bw) | n/a (upcoming; posts colour at its slot) | done |
| 28 | yes | yes | rendering | no | no | 5:10 AM |
| 29 | yes | yes | no | no | no | 6:20 AM |
| 30 | yes | yes | no | no | no | 7:30 AM |
| 23 | yes | yes | no | no | no | 8:40 AM |
| 24 | yes | yes | no | no | no | 9:50 AM |
| 10 | yes | yes | no | no | no | 11:00 AM |
| 11 | yes | yes | no | no | no | 12:10 PM |
| 12 | yes | yes | no | no | no | 1:20 PM |
| 13 | yes | yes | no | no | no | 2:30 PM |
| 14 | yes | yes | no | no | no | 3:40 PM |
| 15 | yes | yes | no | no | no | 4:50 PM |
| 16 | yes | yes | no | no | no | 6:00 PM |
| 17 | yes | yes | no | no | no | 7:10 PM |
| 18 | yes | yes | no | no | no | 8:20 PM |
| 19 | yes | yes | no | no | no | 9:30 PM |

Case 3 B&W copy: skipped (Case 3 already has a colour version).
