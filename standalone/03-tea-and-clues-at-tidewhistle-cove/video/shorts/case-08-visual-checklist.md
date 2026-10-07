# Case 8 visual checklist

Confirmed on-screen (not narration-only), from `--frames` stills read back on the books box:

1. Tray of twelve cinnamon buns on the cooling rack by the back door: bakery plate + `buns` part (hidden after "disappeared"), steam rising off the buns, vignette title/end card
2. Empty tray, twelve flour rings and a "12 BUNS · Saturday" tag: hook hero (full bleed), bakery after "disappeared", lane background
3. Jago serving at the front: shop-front plate (Jago + customer, buns for sale on the counter)
4. Four people passed the back door: lane plate, with Pip / Demelza / Mr Fenwick / Kerensa each fading in and stepping in as named (same size, same walk, same gap)
5. Jago in a terrible mood, marching all four into the Kettle and Gull: tea-room plate (Jago `cross` face, four small identical suspects, Agnes)
6. The four statements: lineup pan over four IDENTICAL tea-room panels with nameplates; each suspect talks only during their own quote; equal holds (about 3 s each)
7. "Just one of them is telling the truth": tea-room close on Jago (talk synced to his quote)
8. Agnes raises an eyebrow: window-table plate, Agnes `eyebrow` face + nod, steam off her cup
9. Statement recap: chalk board "WHO SAID WHAT?" with all four statements + "Exactly ONE of them is telling the truth."
10. Solution marks on the SAME board, only after "The Solution": circle Mr Fenwick (106.3), yellow underlines under Demelza's and Kerensa's lines (108.5), "exactly one of these two is true" (120.5), X Pip (131.7), X Fenwick's statement (133.9), X Demelza (143.1), tick Kerensa (145.9)
11. Confession at the back door: buns back on the rack, Mr Fenwick sheepish (the ONLY non-neutral suspect face in the video), Jago smiling, "recipe?" notebook on the step

Part sprites use `part_open` (clip only). No `frame2` on animated parts (borders are only in static plates).

Fairness:
- The four suspects share the same pose, height, neutral face, card size and treatment in the hook grid, lane, tea room and lineup; each holds one small everyday prop (brush, book, apple, posy)
- Notebook names are parallel ("passed the back door"; Fenwick's adds "(grocer)" because the narration says so); no early highlights beyond the usual "just added" flash
- Countdown notebook: whole notebook in review mode ("Every clue so far"), all items styled the same
- No marks on the board, no reaction from anyone before "The Solution"; Mr Fenwick is sheepish only in the confession

Layout (shared `render.py`, Case 7 fixes kept):
- Case subtitle above the art frame with clear padding (no text through the border)
- Taller question bar; "THE QUESTION" label in its own band; question never under a border line
- Air between qbar, captions and notebook
- NEW `KEEP_ASPECT=True` (Case 8 only): crops use the view's own aspect, so the art is no longer stretched sideways to fit the 920x560 / 904x594 view (Cases 1-7 keep the old 4:3 crop for identical re-renders)

Open (Case 8-specific, `HOOK_STYLE="statements"`): chalkboard title slab (not the cream banner), borderless full-bleed empty-tray hero with feathered edges (not a framed/vignetted 4:3 box), a 2x2 suspect grid instead of the bottom cast strip, "?" bubbles popping on "four statements", an ONLY 1 IS TRUE stamp landing on "one" and clearing every suspect, label "4 suspects · 4 statements · 1 truth". Cinnamon accent (vs Case 7 garden green). Frame 1 already shows the title, the empty tray and all four suspects.

Stills checked (vertical unless noted; video time = original + 6.95 s, + 7 s more after the countdown splice):
hook 0.5 / 3.0 / 5.5 / 7.0 (vertical + wide), title 8.0, bakery 17.0, front 25.0, empty tray 28.0, lane 37.0, tea room 42.0, lineup Pip 49.8 (+ wide), lineup Fenwick 56.0, Jago 67.0, Agnes 76.0, board recap 87.0, notebook full / ask 102.0 (+ wide), countdown 109.3, solution title 118.0, board marks 135.9 / 148.4 / 154.9 (note) / 161.4 (+ wide), confession 173.9, end card 183.9 (+ wide); plus a 1.7 s sweep of the whole vertical timeline (no errors).

| Fact | Scene(s) where it appears |
|---|---|
| Tray of twelve buns on the rack | bakery (buns part), vignette |
| Empty tray / flour rings | hook hero, bakery after "disappeared", lane |
| Back door of the bakery | hook, bakery, lane, confession |
| Jago serving at the front | front |
| Jago cross / "one is telling the truth" | tea room (cross face, talk on his quote) |
| Pip Carew | hook grid, lane, tea room, lineup panel 1, board |
| Demelza Rowe | hook grid, lane, tea room, lineup panel 2, board |
| Mr Fenwick (grocer) | hook grid, lane, tea room, lineup panel 3, board, confession |
| Kerensa Hale | hook grid, lane, tea room, lineup panel 4, board |
| Agnes Bell / raised eyebrow | tea room, window table |
| The four statements | lineup (spoken), board recap, notebook "Who said what" |
