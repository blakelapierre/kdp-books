# Case 1 video: The Prize Sponge

A storybook-style video of Case 1 from *Tea and Clues at Tidewhistle Cove*, by Blake La Pierre. It uses the same Kokoro narration as the audiobook preview. Every frame is drawn locally by code (Python + Pillow + ffmpeg), with no paid or AI video services.

| File | Format | Length | Size |
|---|---|---|---|
| `standalone-03-tidewhistle-case-01-the-prize-sponge-vertical.mp4` | 1080x1920, 30 fps, H.264 + AAC 128k (Shorts, Reels, TikTok) | 3:48 | ~45 MB |
| `standalone-03-tidewhistle-case-01-the-prize-sponge-wide.mp4` | 1920x1080, 30 fps, H.264 + AAC 128k (YouTube, Facebook) | 3:48 | ~48 MB |

## What's in it
- **Agnes's Notebook clue tracker.** A notepad panel (spiral binding, ruled lines, red margin, handwriting font) fills in at the exact word each clue is spoken: the key facts (domes and cloths, number cards only, the entry list in Agnes's handbag, the noon-to-one window, the missing #7, what Ollie told the helpers) and who's who (Morwenna, Hedley, Jago, each with where they were and then what they said). Each new line pops in with the same yellow highlighter swipe, so no clue, including the one that cracks the case, is marked differently from the others before the solution.
  - Vertical: the notebook fills the lower part of the screen, under the captions. Wide: the notebook is a right-hand column, with captions under the picture.
  - **Countdown:** the full notebook stays on screen with an "Every clue so far" tag.
  - **Solution:** Morwenna and Hedley are struck through as they're cleared. Jago's name is circled, the supporting facts get red ticks as the narrator explains them, and his "lemon drizzle" line is circled. Then a red note slip sums it up: nobody said which cake, so only someone who lifted the cloth could know.
- **Detailed ink characters** (`src/people.py`): bezier outlines, hatching and solid blacks in the house inkart style. Agnes has a grey bun, round glasses, a sprig dress, a frilled apron and a teapot. Constable Ollie has a custodian helmet, a tunic with buttons and belt, and a pocket notebook. Morwenna has a straw hat, long hair, a cardigan, a flower dress and sweet peas. Hedley has a flat cap, a moustache, rolled sleeves, a waistcoat and a folding chair. Jago has a baker's toque, a short beard, a striped shirt, an apron and a bread basket. The three suspects share one neutral face, one stance and one level of detail. Jago only looks sheepish in the van scene, after the solution.
- **Richer scenes:** a harbour with six cottages and the show banner, the tea room front with an awning, chalkboard and flower tubs, the hall with curtains, panelling and floorboards (Agnes judging behind the covered cakes), and a lineup with a backdrop for each person: Ollie by the stage, Morwenna at the flower table, Hedley by the chair cupboard, Jago at the bread display. All art is 4:3 to match the video frame.
- **Captions** break only at phrase boundaries: sentence ends, commas, or before words like "and" or "because". They never split pairs like "cake table" or "had been", and very short sentences are joined into one card. Curly quotes throughout.
- **Countdown timing:** 7 s of silence is spliced into the narration after "...the solution follows." The 10-to-1 countdown starts only after the narrator has finished (at 2:33.7) and ends just before "The Solution."
- **End card:** title, by Blake La Pierre, **Coming soon to Kindle**. Change this to "Available on Kindle" once the ebook is live.

Sample frames are in `previews/`.

## Reusing the tracker for later cases
Clues live in a data file per case: `clues/case-01.json`. Each item has a `section` (`facts` or `who`), its text (plus `name` for a person, and `parent` for a later quote under that person), and an `at` anchor `{seg, phrase}` that points at the words in that case's `timing.json`. The item appears on the phrase's last word. `solution` lists the marks (`strike`, `circle` with an optional `span: "name"`, `check`, `note`), each anchored the same way. `src/tracker.py` sizes the font to fit the panel, wraps lines without widows, and renders any time `t`. For a new case, write `clues/case-NN.json`, make its `timing.json` with `align.py`, and point `render.py` at both.

## Rebuild
```
cd src
python3 art.py                   # illustrations -> ../work/art/  (people.py draws the characters)
python3 render.py vertical       # ~1.7 min on 8 CPUs
python3 render.py wide
python3 render.py vertical --frames 44,131,158,203   # stills for checking -> ../work/frames/
python3 render.py vertical --captions               # print the caption chunks and times
# timing (only if the narration changes; needs the TTS venv with faster-whisper):
/tmp/tts/venv/bin/python align.py /tmp/tts/work/chapters.json <case01 16k wav> ../timing.json
```
Needs Python 3, Pillow, reportlab, poppler-utils (pdftoppm), ffmpeg, and the Kalam, Crimson Text, Playfair Display SC and IBM Plex Sans Condensed fonts.

## Sharing note
The repo is private, so download the MP4 and upload it to the platform yourself. If a platform asks, say the narration is AI-generated (a synthetic voice), which matches the audiobook disclosure.
