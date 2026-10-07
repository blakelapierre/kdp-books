> **Runner repo:** the extractable render CLI now lives in [`blakelapierre/tidewhistle-video`](https://github.com/blakelapierre/tidewhistle-video) (private). This folder remains the working tree inside kdp-books.

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

## Animation border fix (Case 5 onward)

In Case 4, every animated PART sprite called `frame_open`, which drew `frame2` (the decorative double black rectangle) onto the transparent sprite before clipping. When `anim.py` rotated, bobbed, or walked that sprite, the border spun with it — the “weird line artifacts / border that gets rotated around” on Case 4 Part 1 especially.

**Fix:** plates use `plate_open` (`frame2` + clip). Parts use `part_open` (clip only — no `frame2`). Applied in `art_case04.py` (for any future re-render) and `art_case05.py`. Case 4 videos already published are left as-is.

## Case 5: The Marrow Mix-up (colour-detailed + simple animations)
Configured in `src/cases/case05.py` (`STYLE = "color-detailed"`, with `ANIM`), art by `src/art_case05.py` → `work/art-05/`, characters in `src/people4.py` (jago / tamsin / hedley / morwenna). Narration is the audiobook's Kokoro af_heart chapter; the hook line was made locally with `hook_audio.py`. Part sprites use `part_open` (no baked border).

| File | Format | Length |
|---|---|---|
| `standalone-03-tidewhistle-case-05-the-marrow-mix-up-vertical.mp4` | 1080x1920 | 3:23 |
| `standalone-03-tidewhistle-case-05-the-marrow-mix-up-wide.mp4` | 1920x1080 | 3:23 |
| `shorts/standalone-03-tidewhistle-case-05-the-marrow-mix-up-short-part1.mp4` / `-part2.mp4` | Shorts | 1:53 / 1:27 |

- **Hook:** "Who took the prize marrow?" over the empty straw bed (dashed outline), with the four suspects equal underneath. Narration: "A prize marrow has vanished from Hedley's shed, and only one person is lying. Can you spot who?"
- **Scenes:** shed with the prize marrow on straw; empty straw; allotments + shed; Agnes on the bench with tea; 4-panel lineup (Jago / Tamsin / Hedley / Morwenna) with talk+nod on each statement; Agnes thinking; solution lineup eliminations; returned marrow on the harvest flower display, Morwenna sheepish.
- **Part 2 Short** opens with a ~2 s recap of the question (feed discovery).
- **Notebook** (`clues/case-05.json`): marrow on straw, empty Thursday, four at the allotments, "thief fibs / others truth", each suspect's statement. Solution: Morwenna circled, others struck through as each hypothesis fails, note that only her line is the lie.

Rebuild:
```
cd src
python3 art_case05.py
/tmp/tts/venv/bin/python hook_audio.py "A prize marrow has vanished from Hedley's shed, and only one person is lying. Can you spot who?" ../work/hook-05.wav
python3 render.py vertical --case=5 && python3 render.py wide --case=5 && python3 make_shorts.py --case=5
```
Previews: `previews/case05-*.png`. YouTube text: `shorts/case-05-youtube.md`.

## Case 6: The Closed Post Office (colour-detailed + simple animations + mid-screen question)
Configured in `src/cases/case06.py` (`STYLE = "color-detailed"`, `SHOW_QBAR = True`, with `ANIM`), art by `src/art_case06.py` → `work/art-06/`, characters in `src/people4.py` (new: `garland`, `wenna` wrapper; plus jago / tamsin / agnes). Narration is the audiobook's Kokoro af_heart chapter; the hook line was made locally with `hook_audio.py`. Part sprites use `part_open` (no baked border).

| File | Format | Length |
|---|---|---|
| `standalone-03-tidewhistle-case-06-the-closed-post-office-vertical.mp4` | 1080x1920 | 3:12 |
| `standalone-03-tidewhistle-case-06-the-closed-post-office-wide.mp4` | 1920x1080 | 3:12 |
| `shorts/standalone-03-tidewhistle-case-06-the-closed-post-office-short-part1.mp4` / `-part2.mp4` | Shorts | 2:00 / 1:10 |

- **Unique hook:** extreme close-up of the post-office door — striped blind, giant CLOSED / SUNDAY plaque, pale blue puffin blanket draped in the foreground — plus a postage-stamp cast strip. Warm Sunday-gold sky (not allotment green / harbour blue) so the first frames do not look like Cases 1–5.
- **Mid-screen question bar:** `SHOW_QBAR` in the case config; `render.py` draws a persistent "THE QUESTION" banner between the illustration and Agnes's Notebook for every art/pan/ask frame (Blake 2026-10-06).
- **Scenes:** Sunday street (church + Kettle & Gull + closed PO); porch with wrapped parcel; empty porch; street meet (Tamsin church / Jago bakery alibis); Garland at the inn with the blanket; Agnes looking down the street at the closed PO; ask + countdown; 3-panel lineup (Garland / Tamsin / Jago); returned Monday (PO open, sheepish Garland, postage).
- **Part 2 Short** opens with a ~2 s recap of the question (feed discovery).
- **Notebook** (`clues/case-06.json`): Sunday, blind down + CLOSED, puffin blanket, porch gone, craft counter, each suspect's alibi / claim. Solution: Garland circled, closed-Sunday facts ticked, Tamsin and Jago struck through, note that nobody could buy anything at a closed post office.
- **Visual checklist:** `shorts/case-06-visual-checklist.md`.

Rebuild:
```
cd src
python3 art_case06.py
/tmp/tts/venv/bin/python hook_audio.py "A knitted puffin blanket has vanished on a Sunday morning, and only one story cannot be true. Can you spot why?" ../work/hook-06.wav
python3 render.py vertical --case=6 && python3 render.py wide --case=6 && python3 make_shorts.py --case=6
```
Previews: `previews/case06-*.png`. YouTube text: `shorts/case-06-youtube.md`.

## Case 7: The Dog That Stayed Quiet
Colour-detailed art (`src/art_case07.py` → `work/art-07/`), mid-screen question bar, borderless hero-gnome hook (garden-green accent + banner title). Layout fix in shared `render.py`: case subtitle clear of the art frame; question text never sits under qbar borders.

| File | Format |
|---|---|
| `standalone-03-tidewhistle-case-07-the-dog-that-stayed-quiet-vertical.mp4` | 1080x1920 Shorts source |
| `standalone-03-tidewhistle-case-07-the-dog-that-stayed-quiet-wide.mp4` | 1920x1080 main channel |
| `shorts/...-short-part1.mp4` / `-part2.mp4` | Shorts split |

Rebuild:
```
cd src
python3 art_case07.py
/tmp/tts/venv/bin/python hook_audio.py "A prize garden gnome has vanished in the night, and the little dog who barks at everyone stayed perfectly quiet. Can you tell who took him?" ../work/hook-07.wav
python3 render.py vertical --case=7 && python3 render.py wide --case=7 && python3 make_shorts.py --case=7
```
YouTube text: `shorts/case-07-youtube.md`. Visual checklist: `shorts/case-07-visual-checklist.md`.

## Case 8: The Four Bakers
Colour-detailed art (`src/art_case08.py` → `work/art-08/`), mid-screen question bar, four suspects drawn identically until the solution (only the confession shows Mr Fenwick sheepish). New open `HOOK_STYLE="statements"` in shared `render.py`: chalkboard title slab, borderless full-bleed empty tray, 2x2 suspect grid with "?" bubbles on "four statements" and an ONLY 1 IS TRUE stamp on "one" (cinnamon accent). New opt-in `KEEP_ASPECT=True` crops art at the view's own aspect instead of stretching a 4:3 crop (Cases 1-7 unchanged). Solution marks are chalked on the same statement board. Rendered on streambox inside the capped `tidewhistle.slice` (tidewhistle-video repo).

| File | Format |
|---|---|
| `standalone-03-tidewhistle-case-08-the-four-bakers-vertical.mp4` | 1080x1920 Shorts source |
| `standalone-03-tidewhistle-case-08-the-four-bakers-wide.mp4` | 1920x1080 main channel |
| `shorts/...-short-part1.mp4` / `-part2.mp4` | Shorts split |

Rebuild:
```
cd src
python3 art_case08.py
/tmp/tts/venv/bin/python hook_audio.py "Twelve cinnamon buns have vanished. Four suspects, four statements, and only one of them is true. Can you find the thief?" ../work/hook-08.wav
python3 render.py vertical --case=8 && python3 render.py wide --case=8 && python3 make_shorts.py --case=8
```
(hook_audio's whisper pass returned no words for this line, so `work/hook-08.wav.json` word times were set by hand from head/tail passes.)
Previews: `previews/case08-*.png`. YouTube text: `shorts/case-08-youtube.md`. Visual checklist: `shorts/case-08-visual-checklist.md`.

## Case 9: The Sunset over the Sea
Colour-detailed art (`src/art_case09.py` → `work/art-09/`), mid-screen question bar, three suspects drawn identically until the solution (only the confession shows Mr Ashdown sheepish). New open `HOOK_STYLE="compass"` in shared `render.py`: navy compass-rose title ring, borderless full-bleed empty easel, three equal suspect cards, spinning compass landing EAST, ONE STORY FAILS stamp (sunset-coral accent). `KEEP_ASPECT=True`. Rendered on streambox inside the capped `tidewhistle.slice` (tidewhistle-video repo).

| File | Role |
|---|---|
| `standalone-03-tidewhistle-case-09-the-sunset-over-the-sea-vertical.mp4` | 1080x1920 Shorts source |
| `standalone-03-tidewhistle-case-09-the-sunset-over-the-sea-wide.mp4` | 1920x1080 main channel |
| `shorts/standalone-03-tidewhistle-case-09-the-sunset-over-the-sea-short-part1.mp4` | Shorts Part 1 |
| `shorts/standalone-03-tidewhistle-case-09-the-sunset-over-the-sea-short-part2.mp4` | Shorts Part 2 |

```bash
python3 art_case09.py
CASE=9 python3 render.py vertical
CASE=9 python3 render.py wide
CASE=9 python3 make_shorts.py
```

Previews: `previews/case09-*.png`. YouTube text: `shorts/case-09-youtube.md`. Visual checklist: `shorts/case-09-visual-checklist.md`.

## Cases 10–30: black-and-white kit + next-case end card
From Case 10 on, every case uses `STYLE="bw"` black-and-white ink with the simple v1 peg-doll characters (`src/figures.py`, which now blink and talk under `anim.py`), plus the shared scenery and character kit `src/bwkit.py` (harbour, tea room, inn, lifeboat station, case board, visitor/lady/overalls figures, picklable lineup/cast builders). The Case 7+ layout (mid-screen question bar, `KEEP_ASPECT=True`) and the clue notebook are unchanged. Each case gets its own `HOOK_STYLE`, and no style repeats back-to-back.

`NEXT_CARD=True` adds a 5 s B&W end card after the closing hold of both full videos, so it also lands at the end of Part 2. The card reads "NEXT CASE / Case N+1 / <title>", then the no-spoiler teaser from `src/cases/teasers.py`, then a bell box with "New case every 6 hours / subscribe so you don't miss it" (no clock time). Case 30 instead says it is the last case and points to the book (`TIDEWHISTLE_BOOK_STATUS`, default "COMING SOON TO KINDLE"). Each `shorts/case-NN-youtube.md` has a "Next case teaser" field.

Word timing for Cases 10+ comes from `src/align_whole.py` (one faster-whisper pass over the whole case MP3, script words mapped onto ASR words), because the per-segment `align.py` drifted.

On streambox the cases render one at a time through `/root/tw-queue.sh`, a sequential queue that only calls the capped `/usr/local/sbin/tw-render`. The queue file is `~tidewhistle/tw-queue.txt` and status goes to `~tidewhistle/logs/queue-status.log`, with per-case logs in `~tidewhistle/logs/cNN.log`.

## Case 10: The Wet Paint Bench
B&W ink (`src/art_case10.py` → `work/art-10/`), three suspects drawn identically until the solution (only the confession shows Mr Kemp sheepish). New open `HOOK_STYLE="wetpaint"`: a hand-lettered WET PAINT board swings in on two strings with growing ink drips, a feathered harbour-bench hero, three tag cards, and a ONE ALIBI CRACKS stamp on "cracks". Next card → Case 11 "The Window Table".

| File | Role |
|---|---|
| `standalone-03-tidewhistle-case-10-the-wet-paint-bench-vertical.mp4` | 1080x1920 Shorts source |
| `standalone-03-tidewhistle-case-10-the-wet-paint-bench-wide.mp4` | 1920x1080 main channel |
| `shorts/standalone-03-tidewhistle-case-10-the-wet-paint-bench-short-part1.mp4` | Shorts Part 1 |
| `shorts/standalone-03-tidewhistle-case-10-the-wet-paint-bench-short-part2.mp4` | Shorts Part 2 (recap + reveal + next card) |

```bash
python3 art_case10.py
/tmp/tts/venv/bin/python hook_audio.py "A lifeboat collection box has vanished on a freshly painted afternoon. Three alibis, and only one of them cracks. Can you spot it?" ../assets/hooks/hook-10.wav
python3 render.py vertical --case=10 && python3 render.py wide --case=10 && python3 make_shorts.py --case=10
```

Previews: `previews/case10-*.png`. YouTube text: `shorts/case-10-youtube.md`. Visual checklist: `shorts/case-10-visual-checklist.md`.

## Case 11: The Window Table
B&W ink (`src/art_case11.py` → `work/art-11/`), a seating-logic case: four tables in a row from the door to the bay window, four suspects drawn identically until the solution (only the confession shows Captain Quill sheepish). The solution is worked on Agnes's notebook page: two crossed-out trial rows, then the final row with a ring on the window table. New open `HOOK_STYLE="placecard"`: a RESERVED tent card flips up, a borderless hero of the four tables and the empty sill, four numbered seat chips with a hopping "?" ring that never settles, and a ONE SEAT HIDES IT stamp. Next card → Case 12 "The Stopped Clock". Segment 6 word times were re-spread by `src/timing_sanity.py` (ASR lost that stretch).

| File | Role |
|---|---|
| `standalone-03-tidewhistle-case-11-the-window-table-vertical.mp4` | 1080x1920 Shorts source |
| `standalone-03-tidewhistle-case-11-the-window-table-wide.mp4` | 1920x1080 main channel |
| `shorts/standalone-03-tidewhistle-case-11-the-window-table-short-part1.mp4` | Shorts Part 1 |
| `shorts/standalone-03-tidewhistle-case-11-the-window-table-short-part2.mp4` | Shorts Part 2 (recap + reveal + next card) |

```bash
python3 art_case11.py
/tmp/tts/venv/bin/python hook_audio.py "A silver brooch has vanished from a tea-room windowsill. Four guests, four tables, and only a few muddled clues. Who sat by the window?" ../assets/hooks/hook-11.wav
python3 render.py vertical --case=11 && python3 render.py wide --case=11 && python3 make_shorts.py --case=11
```

Previews: `previews/case11-*.png`. YouTube text: `shorts/case-11-youtube.md`. Visual checklist: `shorts/case-11-visual-checklist.md`.
