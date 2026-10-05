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

## Black-and-white style option
Blake prefers black-and-white ink art for the Shorts (it stands out in a colour-saturated feed), so the pipeline now has a style switch. Colour stays the default, and cases 1 and 2 are unchanged.
- **Art:** `colorink.set_style("bw")` (or `TIDE_STYLE=bw`) before drawing. The same scene code then draws pure ink like the v1 video: `k.tint()` keeps white fills white and black fills black, hatching is black ink, `k.wash()` / `k.vgrad()` draw nothing, explicit colours snap to ink (dark fills become solid black, the rest paper white), and `render_color()` rasterises in grey with the `inkart.render()` levels (no paper grain). Tone comes from hatching, as in v1.
- **Frame and notebook:** set `STYLE = "bw"` in `cases/caseNN.py`. `render.py` then uses neutral paper and ink, a grey hook emoji and a grey countdown ring, and `tracker.set_style("bw")` gives grey ruled lines, a grey highlighter swipe (still the same for every clue) and a white note slip. The solution marks (strikes, circles, ticks, note text) and the small accent line stay red.

## Case 3: The Dry Raincoat (black and white)
Configured in `src/cases/case03.py` (`STYLE = "bw"`), with art drawn by `src/art_case03.py` (into `work/art-03/`). Narration is the audiobook's Kokoro af_heart chapter; the hook line was made locally with `hook_audio.py`.

| File | Format | Length |
|---|---|---|
| `standalone-03-tidewhistle-case-03-the-dry-raincoat-vertical.mp4` | 1080x1920 | 3:46.7 |
| `standalone-03-tidewhistle-case-03-the-dry-raincoat-wide.mp4` | 1920x1080 | 3:46.7 |
| `shorts/standalone-03-tidewhistle-case-03-the-dry-raincoat-short-part1.mp4` / `-part2.mp4` | Shorts | 2:18 / 1:27 |

- **Hook (0:00 to 0:05.1):** "Who took the signed book? 📚" over the open, empty glass case at the back of the bookshop, pushing in from frame 1, with the three suspects (Hedley with a fishing book, Pip with a rolled-up comic, Wenna with a tote bag) under it, all at the same size, pose and ink weight. Narration from 0.2 s: "A signed book has vanished, and only one clue gives the thief away. Can you spot it?"
- **Scenes:** the main street with Tamsin's bookshop (black-and-white striped awning) and the chemist's; Tamsin dusting the case with the puffin book in it while the telephone rings; the downpour (storm sky, rain, the street running like a river); the empty case; Agnes arriving from the chemist's; a 3-panel lineup (Hedley dripping at the counter as the narration says, Pip under the awning outside, Wenna by the POETRY shelves) with a cut to the door bell between Pip and Wenna; Agnes in the shop afterwards. Solution: Hedley soaked beside Wenna dry, the bell, the alibis, the empty case, and Tamsin handing a sheepish Wenna an ordinary copy while the signed one sits back in its case with a padlock.
- **New characters** in `figures.py`: Tamsin Trevelyan, Pip Carew, Wenna Polglaze, plus `drips()` (water off a soaked figure), `fishing_book()`, `comic()` and `tote_bag()`.
- **Notebook** (`clues/case-03.json`): the signed copy in the case, 2:55 unlocked, the 3:00 downpour, the street like a river and the 3:20 stop, case open and book gone, the bell rang only once (Hedley), and for each suspect where they were and what was seen or said. Every line gets the same highlight. Solution: Wenna circled, her "run in from the harbour" line and "coat, hair and shoes: dry" circled, the downpour, river and Hedley's soaking ticked, a note ("Dry after running through that downpour? She must have been inside the shop before the rain began."), the bell ticked, then Hedley and Pip struck through as the narrator clears them.
- Countdown starts at 2:21.2, after the last pre-solution line.

Rebuild case 3:
```
cd src
python3 art_case03.py            # black and white by default (--color for a colour version)
/tmp/tts/venv/bin/python hook_audio.py "A signed book has vanished, and only one clue gives the thief away. Can you spot it?" ../work/hook-03.wav
#   check ../work/hook-03.wav.json: faster-whisper heard the first words as "A sign vanished,"; the words were set back to
#   "A signed book has vanished," (0.00-1.40 s) so the hook caption matches the audio
python3 render.py vertical --case=3 && python3 render.py wide --case=3 && python3 make_shorts.py --case=3
```
Previews: `previews/case03-bw-*.png`.

## Case 3: The Dry Raincoat (colour, detailed characters)
A colour version of case 3 with the **detailed** ink characters (the v2 style from commit `9223a2a`: real faces with ears, eyes, brows, nose and mouth, hair, collars, cuffs, buttons, belts and pockets) and soft colour washes under the ink (the colour style from `315c547`). Configured in `src/cases/case03_color.py` (`--case=3-color`, `STYLE = "color-detailed"`), art by `src/art_case03_color.py` (into `work/art-03-color/`), characters in `src/people3.py`. The narration, hook audio, notebook (`clues/case-03.json`), scene timings, countdown and Shorts cuts are the same as the black-and-white version, whose files are untouched.

| File | Format | Length |
|---|---|---|
| `standalone-03-tidewhistle-case-03-the-dry-raincoat-color-vertical.mp4` | 1080x1920 | 3:46.7 |
| `standalone-03-tidewhistle-case-03-the-dry-raincoat-color-wide.mp4` | 1920x1080 | 3:46.7 |
| `shorts/standalone-03-tidewhistle-case-03-the-dry-raincoat-color-short-part1.mp4` / `-part2.mp4` | Shorts | 2:18.1 / 1:27.3 |

- **Style option:** `colorink.set_style("color-detailed")` is the colour style (same washes, tints and paper grain; `is_bw()` is False) with `is_detailed()` True. `people.Fig` is now colour-aware: inside `k.tint(...)` its white fills take the tint, black fills take `dark` and default hatching becomes a deeper shade of the tint. With no tint (case 1 v2, the black-and-white cases) it draws exactly as before; `art_case03.py` output is pixel-identical.
- **Characters** (`people3.py`, built on the `people.py` parts): Tamsin (dark bob and fringe, long plum cardigan with patch pockets over a sage polka-dot dress, pencil behind the ear, feather duster or book), Hedley (flat cap, grey moustache, tweed waistcoat with brass buttons and watch chain, rolled shirt sleeves, a fishing book; `wet=True` darkens the cloth and adds water streaks, plus `drips()` and a puddle, because the narration says he is "dripping all over the floor"), Pip (tousled ginger hair, freckles, red-and-cream striped jumper with ribbed hem, navy trousers with turn-ups, trainers, a rolled-up comic), Wenna (honey-blonde curls and a bun, belted camel raincoat with wide lapels, double buttons and pocket flaps, ankle boots, a canvas tote with an anchor badge), Agnes (lavender sprig dress, frilled apron, glasses, grey bun, a chemist's paper bag). The three suspects share one stance, one arm pose (left arm down, right forearm across the chest holding a small prop), one head size, the same neutral face and the same detail and colour weight in the hook strip and the lineup. Only after the solution does Wenna look down and blush (returned scene).
- **Scenes:** the main street on a bright afternoon (pastel cottages with coloured doors, the chemist's with its green cross, Tamsin's butter-yellow shop with a green and gold sign, a lit window of books, a teal door, a hanging sign, a red-and-cream striped awning, a lamppost and flower tubs); the back of the shop (cream walls, panelled wainscot, honey floorboards, pendant lamps, tall bookcases of coloured spines) with the wood-and-glass case, the puffin book on its velvet plinth, Tamsin dusting and the red telephone ringing; the downpour (storm sky, blue-grey light, rain, the street running like a river, overflowing gutters); the empty open case; Agnes and Tamsin on the wet street after the rain; the lineup (Hedley dripping at the counter with Tamsin behind it; Pip under the awning, with rain beyond it; Wenna by the POETRY shelves); the door with its brass bell; Agnes by the shop window. Solution: Hedley soaked in the rain beside Wenna dry in the shop, the bell, the alibis, the empty case, and the signed copy back in its case with a brass padlock.
- **Fix:** the door-bell shot in the base case 3 config pushes in on `cy=0.72`, which is the floor end (image y runs downward), so the bell over the door never appears on screen. The colour config pushes up towards the bell instead, and holds the compare scene's nameplates in shot.

Rebuild:
```
cd src
python3 art_case03_color.py      # ~20 s on 8 CPUs
python3 render.py vertical --case=3-color && python3 render.py wide --case=3-color && python3 make_shorts.py --case=3-color
```
Previews: `previews/case03-color-*.png`.

## Simple animation system (reusable from Case 4)

From Case 4 on, a picture can be drawn as a still **plate** plus moving **parts**, and played by a small local engine. No paid or AI video tools.

1. **`src/layers.py`** — `save_layers(out_dir, jobs, make_ink)` renders each job's plate (`<scene>.png`) and part sprites (`<scene>__<part>__<variant>.png` + a `<scene>.json` manifest). Variants of one part share a crop box so blink / talk / reaction swaps are clean. `face("+blink")` / `face("+talk")` set `people.FACE` while a variant is drawn.
2. **`src/anim.py`** — cut-out engine. A case config's `ANIM = {key: dict(art=<scene>, layers=[...])}` choreographs each picture. Layer kinds: `sprite` (idle sway/breathe, blink, talk+bob, walk-in, nods, keyframed dx/dy/rot/s/a, wobble, bob, reveal wipe, swaps), `fly` (gulls), `glint` (wave strokes / sparkles), `rise` (steam), `reveal_plate` (rising tide), `clock` (rotating hands). All times are **original narration times**; `render.py` passes `tmap=sh` so the hook shift and countdown splice apply exactly like the scene list. Deterministic (seeded) so any frame can be re-rendered alone.
3. **`src/colorink.py`** — `render_rgba()` / `grain_rgba()` for transparent sprites; `people.FACE` (in `people.py`) adds closed-eye and open-mouth variants without changing static art.
4. **`render.py`** — if `cases/caseNN.py` defines `ANIM`, art and pan scenes (and the hook / cast strip) are drawn through `anim.Scene` instead of a flat PNG. Cases 1–3 have no `ANIM` and are unchanged.

Art scripts that use layers (e.g. `art_case04.py`) still work as stills: the plate alone is a valid picture. Cases without `ANIM` keep the old flat-PNG path.

## Case 4: The Sandbar at High Tide (colour-detailed + simple animations)
Configured in `src/cases/case04.py` (`STYLE = "color-detailed"`, with `ANIM`), art by `src/art_case04.py` → `work/art-04/` (plates + parts), characters in `src/people4.py`. Narration is the audiobook's Kokoro af_heart chapter; the hook line was made locally with `hook_audio.py`.

| File | Format | Length |
|---|---|---|
| `standalone-03-tidewhistle-case-04-the-sandbar-at-high-tide-vertical.mp4` | 1080x1920 | ~3:13 |
| `standalone-03-tidewhistle-case-04-the-sandbar-at-high-tide-wide.mp4` | 1920x1080 | ~3:13 |
| `shorts/standalone-03-tidewhistle-case-04-the-sandbar-at-high-tide-short-part1.mp4` / `-part2.mp4` | Shorts | ~2:01 / ~1:09 |

- **Hook (0:00 to 0:05.3):** "Who took the brass compass? 🧭" over the empty office windowsill (dashed ring where the compass sat), clock hands ticking, a boat bobbing beyond the mullions, gulls and wave glints, with the three suspects (Morwenna with flowers, Pip with a pamphlet, Mr Rundle with his pipe) under it, all equal. Narration: "A brass compass has vanished, and only one clue gives the thief away. Can you spot it?"
- **Animated scenes:** harbour (Quill chalks "High water at noon" with a write-on wipe, talks, Agnes walks in with scones, bunting flaps, boats bob, gulls, waves); sandbar (diggers at low tide, then a rising-tide reveal of the high-water plate); office window (compass + needle, then empty ring after 12:30, clock from 11:30 toward 12:30); quay (Ollie walks in); 3-panel lineup (Morwenna / Pip / Mr Rundle, equal idle+blink+nod; Mr Rundle talks on his line; steam over the tearoom teapot); Agnes at the tide board; solution sandbar (ghost digger, tide-board inset, depth mark); boat (rope lifts to reveal the compass with a sparkle); returned (Mr Rundle sheepish → hands compass to Quill → smile).
- **Suspects stay equal before the solution.** Same height, stance, idle, blink and nod on introduction. Only after "The Solution." does Mr Rundle look sheepish and hand the compass back.
- **Notebook** (`clues/case-04.json`): tide board "High water at noon", big tide over the sandbar, man's-height depth, compass on the sill (seen 11:30, gone 12:30), and for each suspect where they were / what they said. Solution: Mr Rundle circled, his sandbar claim circled, the tide facts ticked, a note, then Morwenna and Pip struck through.
- Countdown starts after "...the solution follows."

Rebuild:
```
cd src
python3 art_case04.py            # plates + part sprites -> ../work/art-04/ (~1–2 min on 8 CPUs)
/tmp/tts/venv/bin/python hook_audio.py "A brass compass has vanished, and only one clue gives the thief away. Can you spot it?" ../work/hook-04.wav
python3 render.py vertical --case=4 && python3 render.py wide --case=4 && python3 make_shorts.py --case=4
```
Previews: `previews/case04-anim-*.png`, short clip `previews/case04-anim-preview.mp4`. YouTube text: `shorts/case-04-youtube.md`.
