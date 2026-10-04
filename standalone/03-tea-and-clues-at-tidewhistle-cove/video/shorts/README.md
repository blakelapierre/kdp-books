# Case 1 "The Prize Sponge": YouTube Shorts

These are two YouTube Shorts (1080x1920, H.264/AAC, faststart) cut from the **original v1 vertical video**
(commit `ec8f22c`, 3:41). It is split in two because Shorts must be 3:00 or less.

| File | Length | Contents |
|---|---|---|
| `standalone-03-tidewhistle-case-01-the-prize-sponge-short-part1.mp4` | 2:30.4 | v1 0:00.0 to 2:27.4: the full story, the "Can you solve it?" question and "Think about it." This is followed by a 3 s end card: "Comment your guess! / Morwenna, Hedley, or Jago? / ANSWER IN PART 2" |
| `standalone-03-tidewhistle-case-01-the-prize-sponge-short-part2.mp4` | 1:15.0 | A 1 s silent card ("PART 2 · THE ANSWER / Did you work it out?") on the question screen, then the question narration (v1 audio 2:20.4 to 2:27.4) over that card. Next comes a shortened countdown and the solution through the end card (v1 2:34.5 to 3:41.5) |
| `standalone-03-tidewhistle-case-01-the-prize-sponge-vertical-v1.mp4` | 3:41.5 | Unmodified v1 vertical source, kept as-is |

Every cut falls in a narration pause listed in the v1 `../timing.json` (as of commit `ec8f22c`), so no words are clipped:
- 147.4 s falls inside the pause after "Think about it." (146.95 to 147.85)
- 140.4 s falls inside the pause before "Can you solve it?…" (139.64 to 140.74)
- 154.5 s falls inside the 4.5 s countdown pause before "The Solution." (153.08 to 157.58). This cut drops "Take a moment, or pause here…" and most of the countdown.

The cards use the v1 fonts and colours: Playfair Display SC, Crimson Text and IBM Plex Sans Condensed, in ink, soft brown and accent red. They were drawn with PIL onto a still frame of the v1 question screen and put together with ffmpeg.

## v3 colour Shorts (cut from the v3 colour vertical)

| File | Length | Contents |
|---|---|---|
| `standalone-03-tidewhistle-case-01-the-prize-sponge-color-short-part1.mp4` | 2:35.2 | v3 0:00.0 to 2:32.1: the 5 s hook ("Who stole the prize cake?"), the full story, "Can you solve it?" and "Think about it." Then a 3 s card: "Comment your guess! / Morwenna, Hedley, or Jago? / ANSWER IN PART 2" |
| `standalone-03-tidewhistle-case-01-the-prize-sponge-color-short-part2.mp4` | 1:16.8 | A 1 s silent card ("PART 2 · THE ANSWER / Did you work it out?"), the question recap with the full notebook (v3 2:25.1 to 2:32.1), the last 4 s of the countdown, then the solution through the end card (v3 2:44.4 to 3:53.2) |

Cuts (v3 time = original narration time + 4.705 s hook shift, + 7 s after the countdown splice), all in narration pauses:
- 152.1 s = 147.4 original, in the pause after "Think about it." (146.95 to 147.85)
- 145.1 s = 140.4 original, in the pause before "Can you solve it?" (139.64 to 140.74)
- 164.4 s is inside the silent countdown (narration ends at 157.8, "The Solution." starts at 169.1)

Made by `../src/make_shorts.py` (cuts configured in `SHORTS_CFG` in `../src/render.py`). The v1 Shorts above are untouched.
