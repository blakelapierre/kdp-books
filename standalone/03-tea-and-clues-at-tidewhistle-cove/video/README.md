# Case 1 video: The Prize Sponge

A storybook-style video of Case 1 from *Tea and Clues at Tidewhistle Cove*, by Blake La Pierre. It uses the same Kokoro narration as the audiobook (voice af_heart), plus a short spoken hook made locally with the same voice. Every frame is drawn locally by code (Python + Pillow + reportlab + ffmpeg), with no paid or AI image/video services.

**v3 (current):** colour watercolour-style art, the simple v1 characters (now in colour), and a 5 s hook opening. v2 (detailed ink characters, black and white) is commit `9223a2a`; v1 is `ec8f22c`.

| File | Format | Length | Size |
|---|---|---|---|
| `standalone-03-tidewhistle-case-01-the-prize-sponge-vertical.mp4` | 1080x1920, 30 fps, H.264 + AAC 128k (Shorts, Reels, TikTok) | 3:53 | ~42 MB |
| `standalone-03-tidewhistle-case-01-the-prize-sponge-wide.mp4` | 1920x1080, 30 fps, H.264 + AAC 128k (YouTube, Facebook) | 3:53 | ~43 MB |
| `shorts/standalone-03-tidewhistle-case-01-the-prize-sponge-color-short-part1.mp4` | Shorts Part 1 (hook + story + question + "Comment your guess!" card) | 2:35 | |
| `shorts/standalone-03-tidewhistle-case-01-the-prize-sponge-color-short-part2.mp4` | Shorts Part 2 (recap, 4 s countdown, solution, end card) | 1:17 | |

## What's in it
- **Hook opening (0:00 to 0:05).** Frame 1 already shows the big title "Who stole the prize cake? 🍰" over a colour shot of the empty prize plate with crumbs, slowly pushing in, with the three suspects ("3 suspects · 1 clue") sliding up underneath. Narration starts at 0.2 s: "A prize cake has vanished, and only one clue gives the thief away. Can you spot it?" (`src/hook_audio.py`, Kokoro af_heart at the audiobook speed, mastered to the same -20 dBFS RMS). Then "Case One. The Prize Sponge." over the title card. No spoilers: the suspects are shown equally. Everything after the hook (captions, notebook, countdown, solution) is shifted by 4.7 s to match.
- **Colour art** (`src/colorink.py`): soft flat washes under the ink lines, with a light paper grain. The palette is cozy seaside: sea and sky blues, pastel cottages, colourful bunting, a warm cream hall with honey floorboards and rose curtains. Ink outlines stay. Agnes has a lavender dress and white apron, Ollie a navy uniform, Morwenna a sage flower dress, straw hat and pink and purple sweet peas, Hedley tweed and a brown cap with a wooden folding chair, Jago baker's whites, a blue striped apron and a basket of bread. The three suspects have the same height, pose, face, prop-in-hand and colour weight. Only after the solution does Jago blush (van scene).
- **Simple characters** (`src/figures.py`): the v1 peg-doll figures (round head, dot eyes, small smile, trapezoid body, line arms and legs), now in colour. Same call signature as the detailed v2 `src/people.py`, which is kept (`python3 art.py --detailed` switches back).
- **Agnes's Notebook clue tracker.** A notepad panel (spiral binding, ruled lines, red margin, handwriting font) fills in at the exact word each clue is spoken: the key facts (domes and cloths, number cards only, the entry list in Agnes's handbag, the noon-to-one window, the missing #7, what Ollie told the helpers) and who's who (Morwenna, Hedley, Jago, each with where they were and then what they said). Each new line pops in with the same yellow highlighter swipe, so no clue, including the one that cracks the case, is marked differently from the others before the solution.
  - Vertical: the notebook fills the lower part of the screen, under the captions. Wide: the notebook is a right-hand column, with captions under the picture.
  - **Countdown:** the full notebook stays on screen with an "Every clue so far" tag.
  - **Solution:** Morwenna and Hedley are struck through as they're cleared. Jago's name is circled, the supporting facts get red ticks as the narrator explains them, and his "lemon drizzle" line is circled. Then a red note slip sums it up: nobody said which cake, so only someone who lifted the cloth could know.
- **Richer scenes:** a harbour with six cottages and the show banner, the tea room front with an awning, chalkboard and flower tubs, the hall with curtains, panelling and floorboards (Agnes judging behind the covered cakes), and a lineup with a backdrop for each person: Ollie by the stage, Morwenna at the flower table, Hedley by the chair cupboard, Jago at the bread display. All art is 4:3 to match the video frame. The lineup pan is anchored low so the nameplates are never cut off.
- **Captions** break only at phrase boundaries: sentence ends, commas, or before words like "and" or "because". They never split pairs like "cake table" or "had been", and very short sentences are joined into one card. Curly quotes throughout.
- **Countdown timing:** 7 s of silence is spliced into the narration after "...the solution follows." The 10-to-1 countdown starts only after the narrator has finished (at 2:38.4) and ends just before "The Solution."
- **End card:** title, by Blake La Pierre, **Coming soon to Kindle**. Change this to "Available on Kindle" once the ebook is live.

Sample frames are in `previews/` (`color-*` are v3; the others are v2).

## Reusing the art for later cases
`colorink.py` is case-independent: mix `ColorInk` into an `inkart.Ink` subclass, wrap any ink drawing in `with k.tint(colour, dark=..., hatch=...)` (white fills take the colour, black fills take `dark`, hatching becomes a deeper shade), lay backgrounds with `k.wash()` / `k.vgrad()`, and save with `render_color()`. The palette lives in `PAL`. `figures.py` holds the reusable peg-doll builder (`_legs`, `_body`, `_arms`, `_face`), so a new character is a few lines.

## Reusing the tracker for later cases
Clues live in a data file per case: `clues/case-01.json`. Each item has a `section` (`facts` or `who`), its text (plus `name` for a person, and `parent` for a later quote under that person), and an `at` anchor `{seg, phrase}` that points at the words in that case's `timing.json`. The item appears on the phrase's last word. `solution` lists the marks (`strike`, `circle` with an optional `span: "name"`, `check`, `note`), each anchored the same way. `src/tracker.py` sizes the font to fit the panel, wraps lines without widows, and renders any time `t`. For a new case, write `clues/case-NN.json`, make its `timing.json` with `align.py`, and point `render.py` at both.

## Rebuild
```
cd src
python3 art.py                   # colour illustrations -> ../work/art/ (~2 min; figures.py draws the characters)
/tmp/tts/venv/bin/python hook_audio.py "A prize cake has vanished, and only one clue gives the thief away. Can you spot it?" ../work/hook.wav
python3 render.py vertical       # ~2 min on 8 CPUs
python3 render.py wide
python3 make_shorts.py           # Shorts Part 1 / Part 2 from the vertical -> ../shorts/
# (render.py / make_shorts.py default to case 1; per-case settings live in cases/case01.py)
python3 render.py vertical --frames 44,131,158,203   # stills for checking -> ../work/frames/
python3 render.py vertical --captions               # print the caption chunks and times
# timing (only if the narration changes; needs the TTS venv with faster-whisper):
/tmp/tts/venv/bin/python align.py /tmp/tts/work/chapters.json <case01 16k wav> ../timing.json
```
Needs Python 3, Pillow, reportlab, poppler-utils (pdftoppm), ffmpeg, and the Kalam, Crimson Text, Playfair Display SC and IBM Plex Sans Condensed fonts.

## Case 2: The Lemonade on the Lawn
Same pipeline, configured in `src/cases/case02.py`, with art drawn by `src/art_case02.py` (into `work/art-02/`). Narration is the audiobook's Kokoro af_heart chapter; the hook line was made locally with `hook_audio.py`.

| File | Format | Length |
|---|---|---|
| `standalone-03-tidewhistle-case-02-the-lemonade-on-the-lawn-vertical.mp4` | 1080x1920 | 3:33 |
| `standalone-03-tidewhistle-case-02-the-lemonade-on-the-lawn-wide.mp4` | 1920x1080 | 3:33 |
| `shorts/standalone-03-tidewhistle-case-02-the-lemonade-on-the-lawn-short-part1.mp4` / `-part2.mp4` | Shorts | 2:10 / 1:21 |

- **Hook (0:00 to 0:05.5):** "Who took the silver locket? 🍋" over Loveday's kitchen windowsill with the empty open jewellery box, pushing in from frame 1, with the three suspects (Captain Quill with his ledger, Demelza with a book, Mr Bramble with a plain glass of lemonade) under it. Narration from 0.2 s: "A silver locket has vanished, and only one clue gives the thief away. Can you spot it?"
- **Scenes:** the cottage on the hill on a heat-hazy afternoon, Loveday pouring lemonade by the ice bowl, the kitchen (fridge-freezer marked ICE, the locket on the sill, then the empty box), a 3-panel lineup (Captain Quill with Agnes at the harbour office; Demelza asleep in a striped deckchair by the roses, sunhat over her face; Mr Bramble on a bench in the shade with his frosty glass), Agnes and Loveday in the garden under the blazing sun. Solution: the two glasses side by side (melted vs fresh ice), the kitchen again, the alibis, and Mr Bramble, red-faced, handing back the locket. Mr Bramble only blushes after the solution.
- **New characters** in `figures.py`: Loveday Nance, Captain Quill, Demelza Rowe, Mr Bramble, background guests, and a `seated()` pose (deckchair, bench).
- **Notebook** (`clues/case-02.json`): the heat, the ice bowl at 1:15, everyone's ice melted by 2, the only ice left in the kitchen freezer, the locket on the windowsill (seen at 2, gone by 2:30), and for each suspect where they were and what was seen or said. Every line gets the same highlight. Solution: Mr Bramble circled, his "past hour" claim and the frosty glass circled, the supporting facts ticked, a note ("Ice that fresh can't have sat an hour in this heat…"), then Demelza and Captain Quill struck through as the narrator clears them.
- Countdown starts at 2:12.8, after the last pre-solution line.

Rebuild case 2:
```
cd src
python3 art_case02.py
/tmp/tts/venv/bin/python hook_audio.py "A silver locket has vanished, and only one clue gives the thief away. Can you spot it?" ../work/hook-02.wav
python3 render.py vertical --case=2 && python3 render.py wide --case=2 && python3 make_shorts.py --case=2
```
Previews: `previews/case02-color-*.png`.

## Adding another case
Write `src/cases/caseNN.py` (copy case02.py: slug, audio, scene list, cuts), `clues/case-NN.json`, an art script, and make `timing-case-NN.json` with `align.py ... case-NN`. Then run the commands above with `--case=NN`.

## Sharing note
The repo is private, so download the MP4 and upload it to the platform yourself. If a platform asks, say the narration is AI-generated (a synthetic voice), which matches the audiobook disclosure.
