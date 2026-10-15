# Verification report: Fences of Frostwood

Generated 2026-10-15 10:14 PDT by `src/verify.py` in 26.0 s.

- Puzzles checked: **100** (+ the worked example: unique, solvable with the counting rules alone)
- Well formed and the stored fence is one closed loop that matches every number: **100/100**
- Exactly one solution (SAT solver CaDiCaL via python-sat, with single-loop cuts), equal to the stored fence: **100/100**
- Independent backtracking counter (`slither_bt.py`, no SAT, no shared code) finds exactly one solution, the same one: **100/100**
- Solvable by logic alone (the step-by-step solver finishes with no guessing) and inside their difficulty band: **100/100**
- Counter cross-check on copies with one number removed: SAT and backtracking agree in **100/100** cases (copies with exactly 1 solution: 10, 2+: 90, 0: 0)
- No duplicate puzzles: **True**; numbered 1..100 in order: **True**

Logic tiers (the generator's own step-by-step solver): T1 = counting rules (cell numbers, two fence ends per post, no early closed loop); T2 = + short what-if (a guess that breaks within 8 forced moves); T3 = + long what-if (a guess followed as far as it goes).

| Band | Grid | Numbers shown | Puzzles | Nos. | Band rule | Short what-ifs | Long what-ifs |
|---|---|---|---|---|---|---|---|
| Easy | 6×6 | 12–21 | 20 | 1–20 | needs exactly T1 | 0–0 | 0–0 |
| Medium | 7×7 | 14–23 | 30 | 21–50 | needs exactly T2 | 5–23 | 0–0 |
| Hard | 8×8 | 20–30 | 30 | 51–80 | needs exactly T3 | 12–34 | 1–3 |
| Expert | 10×10 | 32–45 | 20 | 81–100 | needs exactly T3 | 17–42 | 3–12 |

## Per-puzzle results

| # | Band | Grid | Numbers | Fence length | SAT solutions | Unique | Backtracking agrees | Tier | Short / long what-ifs |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Easy | 6×6 | 21 | 36 | 1 | yes | yes | T1 | 0 / 0 |
| 2 | Easy | 6×6 | 21 | 34 | 1 | yes | yes | T1 | 0 / 0 |
| 3 | Easy | 6×6 | 20 | 30 | 1 | yes | yes | T1 | 0 / 0 |
| 4 | Easy | 6×6 | 19 | 32 | 1 | yes | yes | T1 | 0 / 0 |
| 5 | Easy | 6×6 | 19 | 26 | 1 | yes | yes | T1 | 0 / 0 |
| 6 | Easy | 6×6 | 18 | 32 | 1 | yes | yes | T1 | 0 / 0 |
| 7 | Easy | 6×6 | 18 | 30 | 1 | yes | yes | T1 | 0 / 0 |
| 8 | Easy | 6×6 | 18 | 26 | 1 | yes | yes | T1 | 0 / 0 |
| 9 | Easy | 6×6 | 18 | 34 | 1 | yes | yes | T1 | 0 / 0 |
| 10 | Easy | 6×6 | 17 | 34 | 1 | yes | yes | T1 | 0 / 0 |
| 11 | Easy | 6×6 | 17 | 28 | 1 | yes | yes | T1 | 0 / 0 |
| 12 | Easy | 6×6 | 17 | 32 | 1 | yes | yes | T1 | 0 / 0 |
| 13 | Easy | 6×6 | 16 | 36 | 1 | yes | yes | T1 | 0 / 0 |
| 14 | Easy | 6×6 | 16 | 26 | 1 | yes | yes | T1 | 0 / 0 |
| 15 | Easy | 6×6 | 16 | 28 | 1 | yes | yes | T1 | 0 / 0 |
| 16 | Easy | 6×6 | 15 | 28 | 1 | yes | yes | T1 | 0 / 0 |
| 17 | Easy | 6×6 | 15 | 36 | 1 | yes | yes | T1 | 0 / 0 |
| 18 | Easy | 6×6 | 15 | 34 | 1 | yes | yes | T1 | 0 / 0 |
| 19 | Easy | 6×6 | 13 | 34 | 1 | yes | yes | T1 | 0 / 0 |
| 20 | Easy | 6×6 | 12 | 28 | 1 | yes | yes | T1 | 0 / 0 |
| 21 | Medium | 7×7 | 19 | 48 | 1 | yes | yes | T2 | 5 / 0 |
| 22 | Medium | 7×7 | 16 | 42 | 1 | yes | yes | T2 | 6 / 0 |
| 23 | Medium | 7×7 | 20 | 44 | 1 | yes | yes | T2 | 8 / 0 |
| 24 | Medium | 7×7 | 17 | 34 | 1 | yes | yes | T2 | 8 / 0 |
| 25 | Medium | 7×7 | 19 | 38 | 1 | yes | yes | T2 | 9 / 0 |
| 26 | Medium | 7×7 | 18 | 40 | 1 | yes | yes | T2 | 9 / 0 |
| 27 | Medium | 7×7 | 20 | 50 | 1 | yes | yes | T2 | 10 / 0 |
| 28 | Medium | 7×7 | 20 | 42 | 1 | yes | yes | T2 | 11 / 0 |
| 29 | Medium | 7×7 | 18 | 36 | 1 | yes | yes | T2 | 11 / 0 |
| 30 | Medium | 7×7 | 19 | 38 | 1 | yes | yes | T2 | 12 / 0 |
| 31 | Medium | 7×7 | 18 | 40 | 1 | yes | yes | T2 | 12 / 0 |
| 32 | Medium | 7×7 | 19 | 40 | 1 | yes | yes | T2 | 13 / 0 |
| 33 | Medium | 7×7 | 17 | 40 | 1 | yes | yes | T2 | 13 / 0 |
| 34 | Medium | 7×7 | 23 | 40 | 1 | yes | yes | T2 | 14 / 0 |
| 35 | Medium | 7×7 | 19 | 42 | 1 | yes | yes | T2 | 14 / 0 |
| 36 | Medium | 7×7 | 14 | 30 | 1 | yes | yes | T2 | 14 / 0 |
| 37 | Medium | 7×7 | 19 | 34 | 1 | yes | yes | T2 | 15 / 0 |
| 38 | Medium | 7×7 | 18 | 44 | 1 | yes | yes | T2 | 15 / 0 |
| 39 | Medium | 7×7 | 17 | 40 | 1 | yes | yes | T2 | 15 / 0 |
| 40 | Medium | 7×7 | 20 | 44 | 1 | yes | yes | T2 | 16 / 0 |
| 41 | Medium | 7×7 | 18 | 42 | 1 | yes | yes | T2 | 16 / 0 |
| 42 | Medium | 7×7 | 17 | 36 | 1 | yes | yes | T2 | 16 / 0 |
| 43 | Medium | 7×7 | 19 | 32 | 1 | yes | yes | T2 | 17 / 0 |
| 44 | Medium | 7×7 | 19 | 32 | 1 | yes | yes | T2 | 18 / 0 |
| 45 | Medium | 7×7 | 17 | 42 | 1 | yes | yes | T2 | 18 / 0 |
| 46 | Medium | 7×7 | 20 | 48 | 1 | yes | yes | T2 | 19 / 0 |
| 47 | Medium | 7×7 | 16 | 40 | 1 | yes | yes | T2 | 19 / 0 |
| 48 | Medium | 7×7 | 17 | 46 | 1 | yes | yes | T2 | 20 / 0 |
| 49 | Medium | 7×7 | 19 | 36 | 1 | yes | yes | T2 | 21 / 0 |
| 50 | Medium | 7×7 | 19 | 52 | 1 | yes | yes | T2 | 23 / 0 |
| 51 | Hard | 8×8 | 24 | 54 | 1 | yes | yes | T3 | 15 / 1 |
| 52 | Hard | 8×8 | 20 | 44 | 1 | yes | yes | T3 | 16 / 1 |
| 53 | Hard | 8×8 | 24 | 50 | 1 | yes | yes | T3 | 18 / 1 |
| 54 | Hard | 8×8 | 26 | 50 | 1 | yes | yes | T3 | 23 / 1 |
| 55 | Hard | 8×8 | 25 | 62 | 1 | yes | yes | T3 | 31 / 1 |
| 56 | Hard | 8×8 | 21 | 50 | 1 | yes | yes | T3 | 16 / 2 |
| 57 | Hard | 8×8 | 21 | 46 | 1 | yes | yes | T3 | 18 / 2 |
| 58 | Hard | 8×8 | 25 | 50 | 1 | yes | yes | T3 | 20 / 2 |
| 59 | Hard | 8×8 | 23 | 44 | 1 | yes | yes | T3 | 21 / 2 |
| 60 | Hard | 8×8 | 26 | 56 | 1 | yes | yes | T3 | 22 / 2 |
| 61 | Hard | 8×8 | 22 | 52 | 1 | yes | yes | T3 | 22 / 2 |
| 62 | Hard | 8×8 | 22 | 46 | 1 | yes | yes | T3 | 25 / 2 |
| 63 | Hard | 8×8 | 25 | 48 | 1 | yes | yes | T3 | 28 / 2 |
| 64 | Hard | 8×8 | 27 | 60 | 1 | yes | yes | T3 | 12 / 3 |
| 65 | Hard | 8×8 | 26 | 56 | 1 | yes | yes | T3 | 14 / 3 |
| 66 | Hard | 8×8 | 30 | 48 | 1 | yes | yes | T3 | 15 / 3 |
| 67 | Hard | 8×8 | 24 | 36 | 1 | yes | yes | T3 | 15 / 3 |
| 68 | Hard | 8×8 | 22 | 62 | 1 | yes | yes | T3 | 15 / 3 |
| 69 | Hard | 8×8 | 23 | 50 | 1 | yes | yes | T3 | 16 / 3 |
| 70 | Hard | 8×8 | 25 | 50 | 1 | yes | yes | T3 | 17 / 3 |
| 71 | Hard | 8×8 | 24 | 52 | 1 | yes | yes | T3 | 17 / 3 |
| 72 | Hard | 8×8 | 26 | 54 | 1 | yes | yes | T3 | 18 / 3 |
| 73 | Hard | 8×8 | 28 | 54 | 1 | yes | yes | T3 | 19 / 3 |
| 74 | Hard | 8×8 | 24 | 56 | 1 | yes | yes | T3 | 19 / 3 |
| 75 | Hard | 8×8 | 22 | 52 | 1 | yes | yes | T3 | 19 / 3 |
| 76 | Hard | 8×8 | 23 | 50 | 1 | yes | yes | T3 | 20 / 3 |
| 77 | Hard | 8×8 | 26 | 52 | 1 | yes | yes | T3 | 22 / 3 |
| 78 | Hard | 8×8 | 28 | 54 | 1 | yes | yes | T3 | 23 / 3 |
| 79 | Hard | 8×8 | 30 | 54 | 1 | yes | yes | T3 | 25 / 3 |
| 80 | Hard | 8×8 | 27 | 66 | 1 | yes | yes | T3 | 34 / 3 |
| 81 | Expert | 10×10 | 36 | 74 | 1 | yes | yes | T3 | 21 / 3 |
| 82 | Expert | 10×10 | 34 | 66 | 1 | yes | yes | T3 | 17 / 4 |
| 83 | Expert | 10×10 | 33 | 70 | 1 | yes | yes | T3 | 20 / 5 |
| 84 | Expert | 10×10 | 36 | 78 | 1 | yes | yes | T3 | 27 / 6 |
| 85 | Expert | 10×10 | 32 | 70 | 1 | yes | yes | T3 | 19 / 7 |
| 86 | Expert | 10×10 | 37 | 74 | 1 | yes | yes | T3 | 30 / 7 |
| 87 | Expert | 10×10 | 35 | 70 | 1 | yes | yes | T3 | 35 / 7 |
| 88 | Expert | 10×10 | 36 | 66 | 1 | yes | yes | T3 | 24 / 8 |
| 89 | Expert | 10×10 | 35 | 76 | 1 | yes | yes | T3 | 28 / 8 |
| 90 | Expert | 10×10 | 41 | 82 | 1 | yes | yes | T3 | 21 / 9 |
| 91 | Expert | 10×10 | 38 | 86 | 1 | yes | yes | T3 | 17 / 10 |
| 92 | Expert | 10×10 | 39 | 72 | 1 | yes | yes | T3 | 23 / 10 |
| 93 | Expert | 10×10 | 38 | 86 | 1 | yes | yes | T3 | 26 / 10 |
| 94 | Expert | 10×10 | 39 | 88 | 1 | yes | yes | T3 | 30 / 10 |
| 95 | Expert | 10×10 | 36 | 70 | 1 | yes | yes | T3 | 22 / 11 |
| 96 | Expert | 10×10 | 43 | 78 | 1 | yes | yes | T3 | 26 / 11 |
| 97 | Expert | 10×10 | 42 | 96 | 1 | yes | yes | T3 | 30 / 11 |
| 98 | Expert | 10×10 | 36 | 76 | 1 | yes | yes | T3 | 27 / 12 |
| 99 | Expert | 10×10 | 35 | 70 | 1 | yes | yes | T3 | 29 / 12 |
| 100 | Expert | 10×10 | 45 | 84 | 1 | yes | yes | T3 | 42 / 12 |
