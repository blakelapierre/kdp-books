# Case 11 visual checklist

Style: black-and-white ink (`STYLE="bw"`) with the simple v1 peg-doll characters (`figures.py` + `bwkit.py`), the shared Cases 10–30 kit.

Confirmed on-screen (not narration-only), from `--frames` stills read back on the books box:

1. The four tables in a row, DOOR at the left and the bay window at the right: tables plate; numbers 1–4 pop on "first, second, third and fourth"
2. Kerensa at the window table; the silver seagull brooch on the sill (`brooch` part from "on the windowsill"); Kerensa leaves on "hurried out"
3. "Only from here" arrow from the window table to the sill (`reach`, from "can only be reached")
4. Four equal suspects: cast strip (Mr Spargo / Loveday / Captain Quill / Wenna), same size, neutral faces, empty hands; lineup of four identical tea-room panels with no table numbers
5. Brooch gone: zoom on the empty sill with dashed outline + "?" (`gone`, on "the brooch was gone")
6. Agnes in the kitchen with the tray of pasties; Pip serving
7. Pip's four clues pop as pinned notes while he says them (seg 6)
8. Agnes's four squares (door → window, numbered) with the recap rules and the four name tokens on "The four guests were…"
9. Solution page, only after "The Solution": QUILL in square 4 with a ring ("window table") on "Captain Quill sat at the window table"; trial 1 (Loveday at 3, Wenna 1, Quill 2, Spargo 4) crossed on "breaks a clue"; trial 2 (Quill 1, Wenna 2) crossed on "the same clue"; final row Spargo / Loveday / Wenna / Quill filled in as narrated
10. Confession: Captain Quill sheepish (the ONLY non-neutral suspect face), brooch from his coat pocket, a gust through the window, Kerensa's next pot of tea
11. Next-case end card: "NEXT CASE / Case 12 / The Stopped Clock" + teaser + bell box (wide video + vertical, so also Part 2)

Part sprites use `part_open` (clip only). No `frame2` on animated parts.

Fairness:
- The four suspects share pose, height, neutral face, card size and treatment in the hook cast and the lineup; the lineup panels are identical and carry no table numbers
- Notebook clue names are parallel ("Pip remembers"); no early highlights beyond the usual "just added" flash
- The hook's "?" ring hops seat to seat and never settles on one (no spoiler)

Layout: subtitle above the art frame, taller question bar with its own label band, `KEEP_ASPECT=True`. Tea-room cameras sit low (cy ≈ 0.6) so the tables are not cut off by the view's aspect.

Open (Case 11-specific, `HOOK_STYLE="placecard"`): a folded RESERVED tent card (title) that flips up from its fold, a feathered borderless hero of the four numbered tables and the empty sill, four numbered seat chips with a hopping "?" ring, four equal framed suspect cards, and a ONE SEAT HIDES IT stamp on "Who". Not Case 9's compass and not Case 10's wet-paint sign. Frame 1 already shows the title, the room and all four suspects.

Stills checked (vertical unless noted; video ≈ original + 8.5 s, + 7 s more after the countdown splice): hook 0.1 / 3.0 / 8.2 (+ wide 3.0 / 8.2), title 12, tables 23, sill 38.5 / 46.5, lineup 55.5, gone 62.5, kitchen 68.5, Pip 88.5, squares 111.5, ask 123.5, solution 145.5 / 165.5 / 181.5 / 197 / 203 (+ wide 198 / 203), confession 206 / 210.5, next card 227 (+ wide).

Issues found and fixed:
- ASR lost most of segment 6 (Pip's clues): every word was squeezed into ~2 s. `timing_sanity.py` now re-spreads such segments by character count (and interpolates odd out-of-order words in other cases), so the clue notes and notebook items pop when Pip says them.
- The default tea-room camera cut the tables off at the bottom; cameras lowered.
- The solution note covered the final row as Mr Spargo's token popped; the note now shows on "beside her at the window" and is gone before "closest to the door".
- The hook stamp didn't fire: `_word_t` matches lowercase words ("who").

| Fact | Scene(s) where it appears |
|---|---|
| 4 tables, door = 1, window = 4 | tables, sill, squares, board, notebook |
| Brooch on the sill; reachable only from table 4 | sill (`brooch`, `reach`), notebook |
| One guest per table, nobody moved; brooch gone | lineup, sill (`gone`), notebook |
| Pip's four clues | pip notes, squares rules, notebook |
| Captain Quill at the window table | board ring + final row, confession |
