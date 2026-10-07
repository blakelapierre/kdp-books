# Case 19 visual checklist

Style: black-and-white ink (`STYLE="bw"`) with the simple v1 peg-doll characters. The suspects are drawn the SAME size everywhere; the (narrated) heights appear only as identical text tags and on the post-solution chart.

Confirmed on-screen (not narration-only), from `--frames` stills read back on the books box:

1. The SAILING CLUB door with the brass bell (gently swaying) on its hook high above the door; "rung for every race" and "even the tallest: on tiptoe!" cards
2. Tobias ducking through the LIFEBOAT STATION doorway; "6½ ft" tag
3. The porch: the LADDER cupboard with a padlock ("locked", "ladder inside"), Agnes, her key ring with "the ONLY key: Agnes", the broken stool ("broken")
4. Sunday morning: the bell gone, "empty hook"
5. Three equal quizzers (tag cast cards; lineup at the quiz table / club door / home with a clock at ten): height tags "just over 5 ft" / "not much taller" / "6½ ft" and statement tags "at the quiz table" / "left early, headache" / "home at ten"
6. Tobias at the club door: "I didn't touch the bell…" (talking on the quote), Agnes jingling her key ring
7. Solution board "WHO COULD REACH THE HOOK?", only after "The Solution": a 0–7 ft chart, the hook line ("tallest on tiptoe"), bars for Loveday / Fenwick / Tobias, "ladder: locked, Agnes has the key" and "stool: broken" crossed out, Tobias's bar ringed, "only Tobias"
8. Confession: Tobias sheepish (the ONLY non-neutral suspect face), the cracked bell, then the bell back on its hook ringing, "round of applause!"
9. Next-case end card: "NEXT CASE / Case 20 / The Scent of Lavender" + teaser + bell box

Fairness: same size, stance, neutral face and card treatment for all three suspects; every fact is narrated and shown before the question; no marks before "The Solution".

Open (Case 19-specific, `HOOK_STYLE="ruler"`): a measuring rule grows down beside the title with foot marks while a little bell swings from a hook at its top; borderless club-door hero; tag suspect cards; LOOK UP stamp on "look". Not Case 18's starfield and not Case 17's speech bubble.

Stills checked (vertical unless noted; video ≈ original + 10.5 s, + 7 s after the countdown splice): hook 0.1 / 0.5 / 1.0 / 10.3 (+ wide 0.6 / 10.3), door 31.5, lifeboat 39.5, porch 60.5, empty hook 65.5, lineup 76.5 / 90.5, talk 98.5, ask 105.5, board 149.5, confession 169.5, next card 184 (+ wide).

Issues found and fixed:
- Mr Fenwick's moustache (shared `bwkit.visitor`) was a lower half-ellipse that read as a big grin; it is now a flat brush, so his face is as neutral as the others (this also applies to Cases 11, 12, 14, 15 and 17 when they render).
- Agnes's key-ring card sat on her head; moved to the upper right.
- The solution note would have covered the height bars; dropped (the board says "only Tobias").

| Fact | Scene(s) where it appears |
|---|---|
| Hook needs the tallest on tiptoe | door (card), board, notebook |
| Tobias 6½ ft | lifeboat tag, lineup tag, board bar, notebook |
| Ladder locked, Agnes's only key; stool broken | porch, board, notebook |
| Loveday / Fenwick much shorter | lineup tags, board bars, notebook |
