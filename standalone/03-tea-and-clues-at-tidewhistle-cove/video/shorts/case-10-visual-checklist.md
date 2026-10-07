# Case 10 visual checklist

Style: black-and-white ink (`STYLE="bw"`, `colorink.set_style("bw")`) with the simple v1 peg-doll characters (`figures.py` + `bwkit.py`), which blink and talk via `anim.py`. This is the shared kit for Cases 10–30.

Confirmed on-screen (not narration-only), from `--frames` stills read back on the books box:

1. Harbour wall benches being painted, with WET PAINT signs: harbour plate, Hedley with brush; `sign1`/`sign2` pop on "Wet Paint"
2. "Tacky until eight" / the paint tin ("Six hours, it says on the tin"): tin plate
3. Lifeboat-shaped collection box on the station steps at three, then gone at four: station plate + `box` part (hidden on "gone")
4. Three equal suspects: cast strip with tags (Hedley / Wenna / Mr Kemp), same size, neutral faces, empty hands (Hedley's paint marks are his only distinguishing detail and are in the text)
5. Equal lineup pan: slipway (Hedley + Ollie with crates), tea-room window table (Wenna + Agnes), the green bench by the lifeboat station (Mr Kemp's claim); equal holds
6. Mr Kemp's statement: Kemp talks on his quote, cream suit, still neutral
7. The bench "still shining wet in the sun": bench plate with sparkle glint
8. Solution board "THE WET PAINT BENCH": bench with stripes part and X over "never sat" only after "The Solution"
9. Confession: car boot open with the little lifeboat box, Mr Kemp sheepish (the ONLY non-neutral suspect face), Ollie with the note
10. Next-case end card (B&W): "NEXT CASE / Case 11 / The Window Table", the no-spoiler teaser, bell + "New case every 6 hours / subscribe so you don't miss it" (wide video + vertical, so also Part 2)

Part sprites use `part_open` (clip only). No `frame2` on animated parts (borders are only in static plates).

Fairness:
- The three suspects share the same pose, height, neutral face, card size and treatment in the hook cast, lineup and statement scene
- Hedley's paint (hatched knee patches + dots on his hands) is in the text and is a red herring, so he is drawn painted from the start
- Notebook names are parallel ("who was where"); no early highlights beyond the usual "just added" flash
- No marks on the board, no reaction from anyone before "The Solution"; Mr Kemp is sheepish only in the confession

Layout (shared `render.py`, Case 7+ fixes kept): subtitle above the art frame, taller question bar with its own label band, air between qbar / captions / notebook, `KEEP_ASPECT=True`.

Open (Case 10-specific, `HOOK_STYLE="wetpaint"`): a hand-lettered WET PAINT board on two strings that swings in on a damped pendulum with green-ink drips growing from its lower edge, a feathered borderless harbour-bench hero, three tag-style suspect cards, and an ONE ALIBI CRACKS stamp on "cracks". Not Case 8's statements grid and not Case 9's compass ring. Frame 1 already shows the title, the bench and all three suspects.

Stills checked (vertical unless noted): hook 0.1 / 2.5 / 6.0 / 7.6 (+ wide 3.0), title 9.0, harbour/tin 30.0, lineup 60.0 (+ wide), Kemp/bench 90.0, ask/countdown 120.0, board/solution 150.0 / 175.0, confession 178.0 / 182.0, next card 193.0 (+ wide).

Issue found and fixed: on the vertical next card the bell overlapped the left edge of the subscribe box. The box text is now fitted to the box width, and the card block is centred vertically.

| Fact | Scene(s) where it appears |
|---|---|
| Benches painted at 2:30, tacky until eight | harbour, tin, board, notebook |
| Collection box at three / gone at four | station (`box` part), notebook |
| Hedley Truscott (with Ollie) | cast, lineup slipway, notebook |
| Wenna Polglaze (tea room) | cast, lineup window table, notebook |
| Mr Kemp, cream suit, "sat on the bench" | cast, lineup bench, kemp plate, board, confession |
| Spotless trousers | kemp plate, bench, board, notebook |
