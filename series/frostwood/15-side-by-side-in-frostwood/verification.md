# Verification — Side by Side in Frostwood

Total puzzles: **120** · seed `20261119` · `PYTHONHASHSEED=0`

## Result

**ALL 120 PUZZLES PASSED.**
Each has exactly one line-up that fits every clue (equal to the printed answer), every clue is needed, each fits its band, every hint points the right way, everyone is named in at least one clue, the cast list (alphabetical) never equals the answer, and no puzzle repeats (duplicates: 0).

## Bands

| Band | Puzzles | People | Clue kinds | Plain “has place k” clues (max) | Step depth | Suppositions | Clues per puzzle | Pass | Fail |
|---|---|---|---|---|---|---|---|---|---|
| Easy | 30 | 4 | at, notat, end, notend, even, adj, left1, before | 1 | 0 | 0–0 | 3–5 (max 6) | 30 | 0 |
| Medium | 30 | 5 | at, notat, end, notend, even, adj, notadj, left1, before, gap, between | 1 | 0 | 0–0 | 4–6 (max 7) | 30 | 0 |
| Hard | 30 | 6 | notat, end, notend, even, adj, notadj, left1, before, gap, between | 0 | 1 | 1–2 | 5–9 (max 9) | 30 | 0 |
| Expert | 30 | 7 | notat, end, notend, even, adj, notadj, left1, before, gap, between | 0 | 1 | 3–6 | 6–10 (max 10) | 30 | 0 |

**Step depth** is measured by the verifier's own deduction ladder: 0 means the puzzle falls to reading one clue at a time (each clue, together with what is already known about who can sit where, narrows someone down). 1 means at least one “suppose X has place k…” test is needed, where the clash shows up from single clues. **Suppositions** is how many such tests the ladder needs in its canonical order (people in cast order, places low to high).

## Clue kinds used

| Kind | Clues |
|---|---|
| has place k | 28 |
| does not have place k | 50 |
| at one end | 48 |
| not at either end | 36 |
| odd/even-numbered place | 111 |
| right next to | 81 |
| not next to | 60 |
| directly to the left of | 48 |
| somewhere to the left of | 105 |
| exactly g places between | 32 |
| somewhere between | 96 |

## Method

- `gen.py` (with `lineup.py`) picks a random line-up from a fixed seed, adds random true clues until its numpy enumerator finds exactly one line-up, removes every clue that is not needed, and keeps the puzzle only if its own step solver gives the band's depth and supposition count.
- `verify.py` imports nothing from the generator. It parses the **printed English sentence** of every clue back into a rule with regular expressions, so a wording slip would show up as a parse failure or a wrong answer. It tries all n! line-ups in pure Python, re-checks that every clue is needed, and re-measures difficulty with its own line-up-set ladder.

## Every puzzle

| No. | Band | People | Clues | Solutions | Depth | Suppositions | Result |
|---|---|---|---|---|---|---|---|
| 1 | Easy | 4 | 3 | 1 | 0 | 0 | PASS |
| 2 | Easy | 4 | 4 | 1 | 0 | 0 | PASS |
| 3 | Easy | 4 | 3 | 1 | 0 | 0 | PASS |
| 4 | Easy | 4 | 4 | 1 | 0 | 0 | PASS |
| 5 | Easy | 4 | 3 | 1 | 0 | 0 | PASS |
| 6 | Easy | 4 | 4 | 1 | 0 | 0 | PASS |
| 7 | Easy | 4 | 4 | 1 | 0 | 0 | PASS |
| 8 | Easy | 4 | 4 | 1 | 0 | 0 | PASS |
| 9 | Easy | 4 | 4 | 1 | 0 | 0 | PASS |
| 10 | Easy | 4 | 4 | 1 | 0 | 0 | PASS |
| 11 | Easy | 4 | 4 | 1 | 0 | 0 | PASS |
| 12 | Easy | 4 | 4 | 1 | 0 | 0 | PASS |
| 13 | Easy | 4 | 4 | 1 | 0 | 0 | PASS |
| 14 | Easy | 4 | 3 | 1 | 0 | 0 | PASS |
| 15 | Easy | 4 | 4 | 1 | 0 | 0 | PASS |
| 16 | Easy | 4 | 3 | 1 | 0 | 0 | PASS |
| 17 | Easy | 4 | 3 | 1 | 0 | 0 | PASS |
| 18 | Easy | 4 | 4 | 1 | 0 | 0 | PASS |
| 19 | Easy | 4 | 4 | 1 | 0 | 0 | PASS |
| 20 | Easy | 4 | 5 | 1 | 0 | 0 | PASS |
| 21 | Easy | 4 | 4 | 1 | 0 | 0 | PASS |
| 22 | Easy | 4 | 4 | 1 | 0 | 0 | PASS |
| 23 | Easy | 4 | 4 | 1 | 0 | 0 | PASS |
| 24 | Easy | 4 | 4 | 1 | 0 | 0 | PASS |
| 25 | Easy | 4 | 4 | 1 | 0 | 0 | PASS |
| 26 | Easy | 4 | 4 | 1 | 0 | 0 | PASS |
| 27 | Easy | 4 | 4 | 1 | 0 | 0 | PASS |
| 28 | Easy | 4 | 3 | 1 | 0 | 0 | PASS |
| 29 | Easy | 4 | 4 | 1 | 0 | 0 | PASS |
| 30 | Easy | 4 | 4 | 1 | 0 | 0 | PASS |
| 31 | Medium | 5 | 6 | 1 | 0 | 0 | PASS |
| 32 | Medium | 5 | 5 | 1 | 0 | 0 | PASS |
| 33 | Medium | 5 | 4 | 1 | 0 | 0 | PASS |
| 34 | Medium | 5 | 4 | 1 | 0 | 0 | PASS |
| 35 | Medium | 5 | 4 | 1 | 0 | 0 | PASS |
| 36 | Medium | 5 | 5 | 1 | 0 | 0 | PASS |
| 37 | Medium | 5 | 6 | 1 | 0 | 0 | PASS |
| 38 | Medium | 5 | 4 | 1 | 0 | 0 | PASS |
| 39 | Medium | 5 | 4 | 1 | 0 | 0 | PASS |
| 40 | Medium | 5 | 5 | 1 | 0 | 0 | PASS |
| 41 | Medium | 5 | 5 | 1 | 0 | 0 | PASS |
| 42 | Medium | 5 | 5 | 1 | 0 | 0 | PASS |
| 43 | Medium | 5 | 5 | 1 | 0 | 0 | PASS |
| 44 | Medium | 5 | 5 | 1 | 0 | 0 | PASS |
| 45 | Medium | 5 | 4 | 1 | 0 | 0 | PASS |
| 46 | Medium | 5 | 4 | 1 | 0 | 0 | PASS |
| 47 | Medium | 5 | 5 | 1 | 0 | 0 | PASS |
| 48 | Medium | 5 | 6 | 1 | 0 | 0 | PASS |
| 49 | Medium | 5 | 5 | 1 | 0 | 0 | PASS |
| 50 | Medium | 5 | 6 | 1 | 0 | 0 | PASS |
| 51 | Medium | 5 | 5 | 1 | 0 | 0 | PASS |
| 52 | Medium | 5 | 6 | 1 | 0 | 0 | PASS |
| 53 | Medium | 5 | 4 | 1 | 0 | 0 | PASS |
| 54 | Medium | 5 | 4 | 1 | 0 | 0 | PASS |
| 55 | Medium | 5 | 4 | 1 | 0 | 0 | PASS |
| 56 | Medium | 5 | 6 | 1 | 0 | 0 | PASS |
| 57 | Medium | 5 | 4 | 1 | 0 | 0 | PASS |
| 58 | Medium | 5 | 5 | 1 | 0 | 0 | PASS |
| 59 | Medium | 5 | 4 | 1 | 0 | 0 | PASS |
| 60 | Medium | 5 | 4 | 1 | 0 | 0 | PASS |
| 61 | Hard | 6 | 9 | 1 | 1 | 2 | PASS |
| 62 | Hard | 6 | 9 | 1 | 1 | 2 | PASS |
| 63 | Hard | 6 | 6 | 1 | 1 | 2 | PASS |
| 64 | Hard | 6 | 6 | 1 | 1 | 1 | PASS |
| 65 | Hard | 6 | 7 | 1 | 1 | 1 | PASS |
| 66 | Hard | 6 | 6 | 1 | 1 | 2 | PASS |
| 67 | Hard | 6 | 6 | 1 | 1 | 1 | PASS |
| 68 | Hard | 6 | 8 | 1 | 1 | 1 | PASS |
| 69 | Hard | 6 | 7 | 1 | 1 | 1 | PASS |
| 70 | Hard | 6 | 8 | 1 | 1 | 2 | PASS |
| 71 | Hard | 6 | 8 | 1 | 1 | 1 | PASS |
| 72 | Hard | 6 | 6 | 1 | 1 | 2 | PASS |
| 73 | Hard | 6 | 5 | 1 | 1 | 2 | PASS |
| 74 | Hard | 6 | 6 | 1 | 1 | 1 | PASS |
| 75 | Hard | 6 | 6 | 1 | 1 | 1 | PASS |
| 76 | Hard | 6 | 6 | 1 | 1 | 2 | PASS |
| 77 | Hard | 6 | 7 | 1 | 1 | 1 | PASS |
| 78 | Hard | 6 | 9 | 1 | 1 | 1 | PASS |
| 79 | Hard | 6 | 5 | 1 | 1 | 1 | PASS |
| 80 | Hard | 6 | 6 | 1 | 1 | 1 | PASS |
| 81 | Hard | 6 | 6 | 1 | 1 | 1 | PASS |
| 82 | Hard | 6 | 6 | 1 | 1 | 1 | PASS |
| 83 | Hard | 6 | 6 | 1 | 1 | 1 | PASS |
| 84 | Hard | 6 | 5 | 1 | 1 | 2 | PASS |
| 85 | Hard | 6 | 6 | 1 | 1 | 1 | PASS |
| 86 | Hard | 6 | 6 | 1 | 1 | 1 | PASS |
| 87 | Hard | 6 | 7 | 1 | 1 | 2 | PASS |
| 88 | Hard | 6 | 6 | 1 | 1 | 2 | PASS |
| 89 | Hard | 6 | 7 | 1 | 1 | 1 | PASS |
| 90 | Hard | 6 | 7 | 1 | 1 | 1 | PASS |
| 91 | Expert | 7 | 7 | 1 | 1 | 6 | PASS |
| 92 | Expert | 7 | 10 | 1 | 1 | 4 | PASS |
| 93 | Expert | 7 | 9 | 1 | 1 | 3 | PASS |
| 94 | Expert | 7 | 10 | 1 | 1 | 3 | PASS |
| 95 | Expert | 7 | 10 | 1 | 1 | 4 | PASS |
| 96 | Expert | 7 | 7 | 1 | 1 | 3 | PASS |
| 97 | Expert | 7 | 8 | 1 | 1 | 4 | PASS |
| 98 | Expert | 7 | 9 | 1 | 1 | 5 | PASS |
| 99 | Expert | 7 | 7 | 1 | 1 | 6 | PASS |
| 100 | Expert | 7 | 7 | 1 | 1 | 3 | PASS |
| 101 | Expert | 7 | 6 | 1 | 1 | 4 | PASS |
| 102 | Expert | 7 | 9 | 1 | 1 | 5 | PASS |
| 103 | Expert | 7 | 9 | 1 | 1 | 4 | PASS |
| 104 | Expert | 7 | 8 | 1 | 1 | 3 | PASS |
| 105 | Expert | 7 | 7 | 1 | 1 | 6 | PASS |
| 106 | Expert | 7 | 6 | 1 | 1 | 3 | PASS |
| 107 | Expert | 7 | 9 | 1 | 1 | 5 | PASS |
| 108 | Expert | 7 | 7 | 1 | 1 | 3 | PASS |
| 109 | Expert | 7 | 9 | 1 | 1 | 4 | PASS |
| 110 | Expert | 7 | 7 | 1 | 1 | 3 | PASS |
| 111 | Expert | 7 | 7 | 1 | 1 | 3 | PASS |
| 112 | Expert | 7 | 8 | 1 | 1 | 5 | PASS |
| 113 | Expert | 7 | 8 | 1 | 1 | 5 | PASS |
| 114 | Expert | 7 | 8 | 1 | 1 | 3 | PASS |
| 115 | Expert | 7 | 8 | 1 | 1 | 5 | PASS |
| 116 | Expert | 7 | 8 | 1 | 1 | 5 | PASS |
| 117 | Expert | 7 | 7 | 1 | 1 | 6 | PASS |
| 118 | Expert | 7 | 9 | 1 | 1 | 3 | PASS |
| 119 | Expert | 7 | 7 | 1 | 1 | 3 | PASS |
| 120 | Expert | 7 | 9 | 1 | 1 | 5 | PASS |
