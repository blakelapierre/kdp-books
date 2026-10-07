# Case 12 visual checklist

Style: black-and-white ink (`STYLE="bw"`) with the simple v1 peg-doll characters (`figures.py` + `bwkit.py`).

Confirmed on-screen (not narration-only), from `--frames` stills read back on the books box:

1. The old wall clock (carved case, pendulum) standing at TEN TO NINE; "click." pops on "tired little click"; a MON–FRI strip all reading 8:50, with FRI ringed "clockmaker" on "until Friday"
2. "Tell the time by your stomachs": Agnes talks, two customers laugh (smile swap on "they all laughed")
3. The caddy shelf: the silver acorn caddy (`acorn` part), "3:30 dusted" and "4:30 gone!" tags as narrated, then the dashed empty spot on "gone"
4. Three equal suspects: cast cards (Demelza / Hedley / Mr Prowse), same size, neutral faces, empty hands
5. Equal lineup: sea front (Demelza, with Captain Quill), Hedley's armchair at home (3:20 → supper clock), the tea room's back door with the milk crate (Mr Prowse)
6. Mr Prowse's statement at the back door with a thought bubble of a clock at a quarter past three (on "It said a quarter past three")
7. Agnes looks up at the clock: still ten to nine
8. Solution board, only after "The Solution": Prowse's quote card, the stopped clock ("stopped Monday"), caddy times; small 3:15 clock pops, gets an X and "impossible" on "could not have said"; "made up the time to sound early" card
9. Confession: Mr Prowse sheepish (the ONLY non-neutral suspect face) holding the acorn caddy; the caddy on a "higher shelf" at the end
10. Next-case end card: "NEXT CASE / Case 13 / The Misspelled Note" + teaser + bell box

Fairness: the three suspects share pose, height, neutral face and card treatment; notebook names are parallel; no marks before "The Solution".

Layout: subtitle above the art, taller question bar (this question wraps to two lines and fits), `KEEP_ASPECT=True`.

Open (Case 12-specific, `HOOK_STYLE="calendar"`): a tear-off desk calendar beside the title, with MON, TUE and WED pages tearing off and falling away to THU; a borderless hero of the stopped clock over the caddy shelf with the empty spot; three equal suspect cards; a ONE TIME IS WRONG stamp on "times". Not Case 10's sign and not Case 11's tent card.

Stills checked (vertical unless noted; video ≈ original + 6.9 s, + 7 s after the countdown splice): hook 0.1 / 1.4 / 4.0 / 6.6 (+ wide 7.2), title 12, clock 21, laugh 36.4, shelf 51.9 / 53.9, lineup 61.9 / 76.9 / 86.9, Prowse 100.9, look 109.9, ask 116.9, board 145.9 / 155.9 / 160 (+ wide 160), confession 178.9 / 187.4, next card 194.

Issues found and fixed:
- The hook title overlapped the calendar: its font now shrinks to fit the space beside the pad.
- The stamp on "he" fired only ~0.4 s before the crossfade; it now fires on "times".
- The solution note covered the X'd 3:15 clock; the note now shows on "Only Mr Prowse".
- Agnes was a floating head under the zoomed clock; she is drawn taller and the zoom is gentler.

| Fact | Scene(s) where it appears |
|---|---|
| Clock stopped at 8:50 since Monday | clock, look, board, notebook |
| Acorn caddy: there 3:30, gone 4:30 | shelf, board, notebook |
| Demelza with Captain Quill from 3:30 | lineup panel 1, notebook |
| Hedley asleep 3:20 → supper | lineup panel 2, notebook |
| Prowse: "your clock said a quarter past three" | prowse bubble, board, notebook (struck in the solution) |
