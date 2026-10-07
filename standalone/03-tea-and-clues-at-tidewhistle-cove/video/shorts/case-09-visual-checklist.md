# Case 9 visual checklist

Confirmed on-screen (not narration-only), from `--frames` stills read back on the books box:

1. Empty easel on the sea front at dusk with MISSING tag: hook hero (full bleed) + stall plate after "gone"
2. Demelza's stall with the lighthouse-at-dawn watercolour on the easel: stall plate + `painting` part (hidden after "gone")
3. Agnes opens the Kettle and Gull shutters on a sunrise-over-sea: kettle plate (sun disc rising from the east window)
4. Three equal suspects: cast strip (Tamsin / Hedley / Ashdown), same size, neutral faces, one everyday prop each (book / fishing book / sketchbook)
5. Equal lineup pan: three IDENTICAL tea-room panels with nameplates; equal holds
6. Ashdown's clifftop story: tea-room plate, Ashdown talks on his quote, Agnes listens — still neutral
7. Agnes remembering the morning sunrise: window-table plate, Agnes `eyebrow` + nod, steam off her cup
8. Map board "TIDEWHISTLE COVE": hills (west) / sea (east), SUNRISE arrow from the sea, SUNSET arrow into the hills
9. Solution marks on the SAME board, only after "The Solution": circle EAST (121), X over "sunset into the sea" (131.5), "Mr Ashdown invented the clifftop" (136.5)
10. Confession: wrapped painting on the table, Mr Ashdown sheepish (the ONLY non-neutral suspect face), Demelza beside him

Part sprites use `part_open` (clip only). No `frame2` on animated parts (borders are only in static plates).

Fairness:
- The three suspects share the same pose, height, neutral face, card size and treatment in the hook cast, lineup and statement scene; each holds one small everyday prop
- Notebook names are parallel ("who was where"); no early highlights beyond the usual "just added" flash
- Countdown notebook: whole notebook in review mode ("Every clue so far"), all items styled the same
- No marks on the board, no reaction from anyone before "The Solution"; Mr Ashdown is sheepish only in the confession

Layout (shared `render.py`, Case 7+ fixes kept):
- Case subtitle above the art frame with clear padding (no text through the border)
- Taller question bar; "THE QUESTION" label in its own band; question never under a border line
- Air between qbar, captions and notebook
- `KEEP_ASPECT=True` (Case 8+): crops use the view's own aspect

Open (Case 9-specific, `HOOK_STYLE="compass"`): navy compass-rose title ring with N/E/S/W ticks (not cream banner, not chalkboard slab), borderless full-bleed empty-easel hero with feathered edges, three equal suspect cards (not a 2x2 statements grid), a spinning brass compass that lands pointing EAST on "story", and a ONE STORY FAILS stamp on "lie". Sunset-coral accent (vs Case 7 garden green / Case 8 cinnamon). Frame 1 already shows the title, the empty easel and all three suspects.

Stills checked (vertical unless noted; video time ≈ original + 7.97 s, + 7 s more after the countdown splice):
hook 0.5 / 3.0 / 5.5 / 7.5 (vertical + wide), title/kettle 14.0, stall 32.0 / 45.0, lineup 55.0 / 64.0 / 72.0, Ashdown 85.0, Agnes 100.0, ask/countdown 110.0 / 122.0 (+ wide), board/solution 130.0 / 145.0 / 160.0, confession 175.0 (+ wide), end 185.0.

| Fact | Scene(s) where it appears |
|---|---|
| Cove faces east / sunrise from the sea | kettle window, board map, notebook |
| Sunset behind the hills | board map (west arrow), notebook |
| Demelza's stall + easel | hook, stall |
| Painting on easel / gone | stall (`painting` part) |
| Tamsin Trevelyan | cast, lineup panel 1, notebook |
| Hedley Truscott | cast, lineup panel 2, notebook |
| Mr Ashdown | cast, lineup panel 3, ashdown plate, board, confession |
| Agnes Bell | kettle, ashdown plate, window table |
| "Sun setting into the sea" claim | ashdown talk, notebook quote, board X |
