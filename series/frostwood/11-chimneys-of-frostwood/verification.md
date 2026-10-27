# Verification report: Chimneys of Frostwood

Generated 2026-10-27 10:10 PDT by `src/verify.py` in 1531.4 s.

- Puzzles checked: **100** (+ the worked example: unique, solvable with the edge rules and singles alone)
- Well formed and the stored answer uses every height once per row and column and matches every clue: **100/100**
- Exactly one solution (SAT solver CaDiCaL via python-sat), equal to the stored answer: **100/100**
- Independent backtracking counter (`sky_bt.py`, no SAT, no shared code) finds exactly one solution, the same one: **100/100**
- Solvable by logic alone (the step-by-step solver finishes with no guessing) and inside their difficulty band: **100/100**
- Counter cross-check on copies with one clue removed: SAT and backtracking agree in **100/100** cases (copies with exactly 1 solution: 19, 2+: 81, 0: 0)
- No duplicate puzzles: **True**; numbered 1..100 in order: **True**

Logic tiers (the generator's own step-by-step solver): T1 = edge rules and singles; T2 = + whole-lane reasoning; T3 = + what-if tries.

| Band | Grid | Clues shown | Puzzles | Nos. | Band rule | What-if steps |
|---|---|---|---|---|---|---|
| Easy | 5×5 | 9–9 | 20 | 1–20 | needs exactly T1 | 0–0 |
| Medium | 6×6 | 10–15 | 30 | 21–50 | needs exactly T2 | 0–0 |
| Hard | 7×7 | 11–20 | 30 | 51–80 | needs exactly T2 | 0–0 |
| Expert | 6×6 | 7–15 | 20 | 81–100 | needs exactly T3 | 1–6 |

## Per-puzzle results

| # | Band | Grid | Clues | SAT solutions | Unique | Backtracking agrees | Tier | What-ifs |
|---|---|---|---|---|---|---|---|---|
| 1 | Easy | 5×5 | 9 | 1 | yes | yes | T1 | 0 |
| 2 | Easy | 5×5 | 9 | 1 | yes | yes | T1 | 0 |
| 3 | Easy | 5×5 | 9 | 1 | yes | yes | T1 | 0 |
| 4 | Easy | 5×5 | 9 | 1 | yes | yes | T1 | 0 |
| 5 | Easy | 5×5 | 9 | 1 | yes | yes | T1 | 0 |
| 6 | Easy | 5×5 | 9 | 1 | yes | yes | T1 | 0 |
| 7 | Easy | 5×5 | 9 | 1 | yes | yes | T1 | 0 |
| 8 | Easy | 5×5 | 9 | 1 | yes | yes | T1 | 0 |
| 9 | Easy | 5×5 | 9 | 1 | yes | yes | T1 | 0 |
| 10 | Easy | 5×5 | 9 | 1 | yes | yes | T1 | 0 |
| 11 | Easy | 5×5 | 9 | 1 | yes | yes | T1 | 0 |
| 12 | Easy | 5×5 | 9 | 1 | yes | yes | T1 | 0 |
| 13 | Easy | 5×5 | 9 | 1 | yes | yes | T1 | 0 |
| 14 | Easy | 5×5 | 9 | 1 | yes | yes | T1 | 0 |
| 15 | Easy | 5×5 | 9 | 1 | yes | yes | T1 | 0 |
| 16 | Easy | 5×5 | 9 | 1 | yes | yes | T1 | 0 |
| 17 | Easy | 5×5 | 9 | 1 | yes | yes | T1 | 0 |
| 18 | Easy | 5×5 | 9 | 1 | yes | yes | T1 | 0 |
| 19 | Easy | 5×5 | 9 | 1 | yes | yes | T1 | 0 |
| 20 | Easy | 5×5 | 9 | 1 | yes | yes | T1 | 0 |
| 21 | Medium | 6×6 | 15 | 1 | yes | yes | T2 | 0 |
| 22 | Medium | 6×6 | 13 | 1 | yes | yes | T2 | 0 |
| 23 | Medium | 6×6 | 13 | 1 | yes | yes | T2 | 0 |
| 24 | Medium | 6×6 | 12 | 1 | yes | yes | T2 | 0 |
| 25 | Medium | 6×6 | 12 | 1 | yes | yes | T2 | 0 |
| 26 | Medium | 6×6 | 12 | 1 | yes | yes | T2 | 0 |
| 27 | Medium | 6×6 | 12 | 1 | yes | yes | T2 | 0 |
| 28 | Medium | 6×6 | 12 | 1 | yes | yes | T2 | 0 |
| 29 | Medium | 6×6 | 12 | 1 | yes | yes | T2 | 0 |
| 30 | Medium | 6×6 | 12 | 1 | yes | yes | T2 | 0 |
| 31 | Medium | 6×6 | 12 | 1 | yes | yes | T2 | 0 |
| 32 | Medium | 6×6 | 12 | 1 | yes | yes | T2 | 0 |
| 33 | Medium | 6×6 | 11 | 1 | yes | yes | T2 | 0 |
| 34 | Medium | 6×6 | 11 | 1 | yes | yes | T2 | 0 |
| 35 | Medium | 6×6 | 11 | 1 | yes | yes | T2 | 0 |
| 36 | Medium | 6×6 | 11 | 1 | yes | yes | T2 | 0 |
| 37 | Medium | 6×6 | 11 | 1 | yes | yes | T2 | 0 |
| 38 | Medium | 6×6 | 11 | 1 | yes | yes | T2 | 0 |
| 39 | Medium | 6×6 | 10 | 1 | yes | yes | T2 | 0 |
| 40 | Medium | 6×6 | 10 | 1 | yes | yes | T2 | 0 |
| 41 | Medium | 6×6 | 10 | 1 | yes | yes | T2 | 0 |
| 42 | Medium | 6×6 | 10 | 1 | yes | yes | T2 | 0 |
| 43 | Medium | 6×6 | 10 | 1 | yes | yes | T2 | 0 |
| 44 | Medium | 6×6 | 10 | 1 | yes | yes | T2 | 0 |
| 45 | Medium | 6×6 | 10 | 1 | yes | yes | T2 | 0 |
| 46 | Medium | 6×6 | 10 | 1 | yes | yes | T2 | 0 |
| 47 | Medium | 6×6 | 10 | 1 | yes | yes | T2 | 0 |
| 48 | Medium | 6×6 | 10 | 1 | yes | yes | T2 | 0 |
| 49 | Medium | 6×6 | 10 | 1 | yes | yes | T2 | 0 |
| 50 | Medium | 6×6 | 10 | 1 | yes | yes | T2 | 0 |
| 51 | Hard | 7×7 | 20 | 1 | yes | yes | T2 | 0 |
| 52 | Hard | 7×7 | 17 | 1 | yes | yes | T2 | 0 |
| 53 | Hard | 7×7 | 17 | 1 | yes | yes | T2 | 0 |
| 54 | Hard | 7×7 | 17 | 1 | yes | yes | T2 | 0 |
| 55 | Hard | 7×7 | 16 | 1 | yes | yes | T2 | 0 |
| 56 | Hard | 7×7 | 16 | 1 | yes | yes | T2 | 0 |
| 57 | Hard | 7×7 | 16 | 1 | yes | yes | T2 | 0 |
| 58 | Hard | 7×7 | 16 | 1 | yes | yes | T2 | 0 |
| 59 | Hard | 7×7 | 16 | 1 | yes | yes | T2 | 0 |
| 60 | Hard | 7×7 | 16 | 1 | yes | yes | T2 | 0 |
| 61 | Hard | 7×7 | 16 | 1 | yes | yes | T2 | 0 |
| 62 | Hard | 7×7 | 15 | 1 | yes | yes | T2 | 0 |
| 63 | Hard | 7×7 | 15 | 1 | yes | yes | T2 | 0 |
| 64 | Hard | 7×7 | 15 | 1 | yes | yes | T2 | 0 |
| 65 | Hard | 7×7 | 15 | 1 | yes | yes | T2 | 0 |
| 66 | Hard | 7×7 | 15 | 1 | yes | yes | T2 | 0 |
| 67 | Hard | 7×7 | 15 | 1 | yes | yes | T2 | 0 |
| 68 | Hard | 7×7 | 15 | 1 | yes | yes | T2 | 0 |
| 69 | Hard | 7×7 | 15 | 1 | yes | yes | T2 | 0 |
| 70 | Hard | 7×7 | 14 | 1 | yes | yes | T2 | 0 |
| 71 | Hard | 7×7 | 14 | 1 | yes | yes | T2 | 0 |
| 72 | Hard | 7×7 | 14 | 1 | yes | yes | T2 | 0 |
| 73 | Hard | 7×7 | 14 | 1 | yes | yes | T2 | 0 |
| 74 | Hard | 7×7 | 13 | 1 | yes | yes | T2 | 0 |
| 75 | Hard | 7×7 | 13 | 1 | yes | yes | T2 | 0 |
| 76 | Hard | 7×7 | 13 | 1 | yes | yes | T2 | 0 |
| 77 | Hard | 7×7 | 12 | 1 | yes | yes | T2 | 0 |
| 78 | Hard | 7×7 | 12 | 1 | yes | yes | T2 | 0 |
| 79 | Hard | 7×7 | 11 | 1 | yes | yes | T2 | 0 |
| 80 | Hard | 7×7 | 11 | 1 | yes | yes | T2 | 0 |
| 81 | Expert | 6×6 | 12 | 1 | yes | yes | T3 | 1 |
| 82 | Expert | 6×6 | 12 | 1 | yes | yes | T3 | 1 |
| 83 | Expert | 6×6 | 10 | 1 | yes | yes | T3 | 1 |
| 84 | Expert | 6×6 | 9 | 1 | yes | yes | T3 | 1 |
| 85 | Expert | 6×6 | 7 | 1 | yes | yes | T3 | 1 |
| 86 | Expert | 6×6 | 10 | 1 | yes | yes | T3 | 2 |
| 87 | Expert | 6×6 | 10 | 1 | yes | yes | T3 | 2 |
| 88 | Expert | 6×6 | 12 | 1 | yes | yes | T3 | 3 |
| 89 | Expert | 6×6 | 10 | 1 | yes | yes | T3 | 3 |
| 90 | Expert | 6×6 | 9 | 1 | yes | yes | T3 | 3 |
| 91 | Expert | 6×6 | 13 | 1 | yes | yes | T3 | 4 |
| 92 | Expert | 6×6 | 12 | 1 | yes | yes | T3 | 4 |
| 93 | Expert | 6×6 | 11 | 1 | yes | yes | T3 | 4 |
| 94 | Expert | 6×6 | 12 | 1 | yes | yes | T3 | 5 |
| 95 | Expert | 6×6 | 12 | 1 | yes | yes | T3 | 5 |
| 96 | Expert | 6×6 | 10 | 1 | yes | yes | T3 | 5 |
| 97 | Expert | 6×6 | 15 | 1 | yes | yes | T3 | 6 |
| 98 | Expert | 6×6 | 12 | 1 | yes | yes | T3 | 6 |
| 99 | Expert | 6×6 | 11 | 1 | yes | yes | T3 | 6 |
| 100 | Expert | 6×6 | 10 | 1 | yes | yes | T3 | 6 |
