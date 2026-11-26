# Verification report: The Quilts of Frostwood

Generated 2026-11-26 09:37 PST by `src/verify.py` in 0.4 s (puzzles made by `PYTHONHASHSEED=0 python3 master.py`, fixed seeds).

- Puzzles checked: **100** (+ the worked example: unique, solvable with the T1 rules alone)
- Well formed (every stored patch is a rectangle holding exactly one number equal to its area, and the patches tile the grid): **100/100**
- Exactly one solution (SAT solver CaDiCaL via python-sat, `sk_sat.py`), equal to the stored answer: **100/100**
- Independent backtracking counter (`sk_bt.py`, no SAT, no shared code) finds exactly one solution, the same one: **100/100**
- Solvable by logic alone (the step-by-step solver in `shikaku.py` finishes with no guessing) and inside their difficulty band: **100/100**
- Counter cross-check on copies with one number moved to a neighbouring square: SAT and backtracking agree in **100/100** cases (copies with exactly 1 solution: 45, 2+: 7, 0: 48)
- No duplicate puzzles: **True**; numbered 1..100 in order: **True**

Logic tiers (the generator's own step-by-step solver): T1 = single patch for a number, single patch for a square; T2 = + only-one-number squares and shared squares of all a number's patches; T3 = + what-if tries.

| Band | Grid | Numbers (patches) | Patch sizes | Puzzles | Nos. | Band rule | Deduction steps | What-if steps |
|---|---|---|---|---|---|---|---|---|
| Easy | 7×7 | 11–16 | 1–8 | 20 | 1–20 | needs exactly T1, ≥ 2 steps | 2–7 | 0–0 |
| Medium | 9×9 | 15–24 | 1–10 | 30 | 21–50 | needs exactly T2, ≥ 6 steps | 6–21 | 0–0 |
| Hard | 10×10 | 14–29 | 1–14 | 30 | 51–80 | needs exactly T2, ≥ 10 steps | 10–26 | 0–0 |
| Expert | 12×12 | 18–34 | 1–16 | 20 | 81–100 | needs exactly T3, ≥ 0 steps | 7–37 | 1–3 |

## Per-puzzle results

| # | Band | Grid | Numbers | SAT solutions | Unique | Backtracking agrees | Tier | Steps | What-ifs |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Easy | 7×7 | 13 | 1 | yes | yes | T1 | 2 | 0 |
| 2 | Easy | 7×7 | 15 | 1 | yes | yes | T1 | 2 | 0 |
| 3 | Easy | 7×7 | 14 | 1 | yes | yes | T1 | 2 | 0 |
| 4 | Easy | 7×7 | 12 | 1 | yes | yes | T1 | 2 | 0 |
| 5 | Easy | 7×7 | 12 | 1 | yes | yes | T1 | 2 | 0 |
| 6 | Easy | 7×7 | 16 | 1 | yes | yes | T1 | 2 | 0 |
| 7 | Easy | 7×7 | 13 | 1 | yes | yes | T1 | 2 | 0 |
| 8 | Easy | 7×7 | 14 | 1 | yes | yes | T1 | 2 | 0 |
| 9 | Easy | 7×7 | 11 | 1 | yes | yes | T1 | 3 | 0 |
| 10 | Easy | 7×7 | 15 | 1 | yes | yes | T1 | 3 | 0 |
| 11 | Easy | 7×7 | 13 | 1 | yes | yes | T1 | 3 | 0 |
| 12 | Easy | 7×7 | 13 | 1 | yes | yes | T1 | 3 | 0 |
| 13 | Easy | 7×7 | 15 | 1 | yes | yes | T1 | 3 | 0 |
| 14 | Easy | 7×7 | 12 | 1 | yes | yes | T1 | 4 | 0 |
| 15 | Easy | 7×7 | 11 | 1 | yes | yes | T1 | 4 | 0 |
| 16 | Easy | 7×7 | 13 | 1 | yes | yes | T1 | 5 | 0 |
| 17 | Easy | 7×7 | 14 | 1 | yes | yes | T1 | 5 | 0 |
| 18 | Easy | 7×7 | 15 | 1 | yes | yes | T1 | 5 | 0 |
| 19 | Easy | 7×7 | 13 | 1 | yes | yes | T1 | 6 | 0 |
| 20 | Easy | 7×7 | 14 | 1 | yes | yes | T1 | 7 | 0 |
| 21 | Medium | 9×9 | 17 | 1 | yes | yes | T2 | 6 | 0 |
| 22 | Medium | 9×9 | 20 | 1 | yes | yes | T2 | 6 | 0 |
| 23 | Medium | 9×9 | 22 | 1 | yes | yes | T2 | 7 | 0 |
| 24 | Medium | 9×9 | 20 | 1 | yes | yes | T2 | 7 | 0 |
| 25 | Medium | 9×9 | 15 | 1 | yes | yes | T2 | 8 | 0 |
| 26 | Medium | 9×9 | 17 | 1 | yes | yes | T2 | 8 | 0 |
| 27 | Medium | 9×9 | 20 | 1 | yes | yes | T2 | 8 | 0 |
| 28 | Medium | 9×9 | 20 | 1 | yes | yes | T2 | 8 | 0 |
| 29 | Medium | 9×9 | 24 | 1 | yes | yes | T2 | 8 | 0 |
| 30 | Medium | 9×9 | 23 | 1 | yes | yes | T2 | 9 | 0 |
| 31 | Medium | 9×9 | 20 | 1 | yes | yes | T2 | 9 | 0 |
| 32 | Medium | 9×9 | 18 | 1 | yes | yes | T2 | 9 | 0 |
| 33 | Medium | 9×9 | 16 | 1 | yes | yes | T2 | 9 | 0 |
| 34 | Medium | 9×9 | 19 | 1 | yes | yes | T2 | 9 | 0 |
| 35 | Medium | 9×9 | 21 | 1 | yes | yes | T2 | 9 | 0 |
| 36 | Medium | 9×9 | 23 | 1 | yes | yes | T2 | 10 | 0 |
| 37 | Medium | 9×9 | 19 | 1 | yes | yes | T2 | 10 | 0 |
| 38 | Medium | 9×9 | 20 | 1 | yes | yes | T2 | 11 | 0 |
| 39 | Medium | 9×9 | 21 | 1 | yes | yes | T2 | 11 | 0 |
| 40 | Medium | 9×9 | 22 | 1 | yes | yes | T2 | 12 | 0 |
| 41 | Medium | 9×9 | 18 | 1 | yes | yes | T2 | 12 | 0 |
| 42 | Medium | 9×9 | 18 | 1 | yes | yes | T2 | 13 | 0 |
| 43 | Medium | 9×9 | 21 | 1 | yes | yes | T2 | 13 | 0 |
| 44 | Medium | 9×9 | 17 | 1 | yes | yes | T2 | 14 | 0 |
| 45 | Medium | 9×9 | 19 | 1 | yes | yes | T2 | 14 | 0 |
| 46 | Medium | 9×9 | 20 | 1 | yes | yes | T2 | 15 | 0 |
| 47 | Medium | 9×9 | 17 | 1 | yes | yes | T2 | 16 | 0 |
| 48 | Medium | 9×9 | 23 | 1 | yes | yes | T2 | 17 | 0 |
| 49 | Medium | 9×9 | 21 | 1 | yes | yes | T2 | 17 | 0 |
| 50 | Medium | 9×9 | 18 | 1 | yes | yes | T2 | 21 | 0 |
| 51 | Hard | 10×10 | 21 | 1 | yes | yes | T2 | 10 | 0 |
| 52 | Hard | 10×10 | 29 | 1 | yes | yes | T2 | 10 | 0 |
| 53 | Hard | 10×10 | 19 | 1 | yes | yes | T2 | 10 | 0 |
| 54 | Hard | 10×10 | 22 | 1 | yes | yes | T2 | 10 | 0 |
| 55 | Hard | 10×10 | 18 | 1 | yes | yes | T2 | 10 | 0 |
| 56 | Hard | 10×10 | 19 | 1 | yes | yes | T2 | 11 | 0 |
| 57 | Hard | 10×10 | 26 | 1 | yes | yes | T2 | 11 | 0 |
| 58 | Hard | 10×10 | 19 | 1 | yes | yes | T2 | 11 | 0 |
| 59 | Hard | 10×10 | 23 | 1 | yes | yes | T2 | 11 | 0 |
| 60 | Hard | 10×10 | 19 | 1 | yes | yes | T2 | 11 | 0 |
| 61 | Hard | 10×10 | 19 | 1 | yes | yes | T2 | 12 | 0 |
| 62 | Hard | 10×10 | 14 | 1 | yes | yes | T2 | 12 | 0 |
| 63 | Hard | 10×10 | 23 | 1 | yes | yes | T2 | 12 | 0 |
| 64 | Hard | 10×10 | 22 | 1 | yes | yes | T2 | 13 | 0 |
| 65 | Hard | 10×10 | 21 | 1 | yes | yes | T2 | 13 | 0 |
| 66 | Hard | 10×10 | 22 | 1 | yes | yes | T2 | 14 | 0 |
| 67 | Hard | 10×10 | 18 | 1 | yes | yes | T2 | 14 | 0 |
| 68 | Hard | 10×10 | 16 | 1 | yes | yes | T2 | 14 | 0 |
| 69 | Hard | 10×10 | 20 | 1 | yes | yes | T2 | 14 | 0 |
| 70 | Hard | 10×10 | 23 | 1 | yes | yes | T2 | 14 | 0 |
| 71 | Hard | 10×10 | 16 | 1 | yes | yes | T2 | 15 | 0 |
| 72 | Hard | 10×10 | 26 | 1 | yes | yes | T2 | 15 | 0 |
| 73 | Hard | 10×10 | 22 | 1 | yes | yes | T2 | 16 | 0 |
| 74 | Hard | 10×10 | 22 | 1 | yes | yes | T2 | 16 | 0 |
| 75 | Hard | 10×10 | 19 | 1 | yes | yes | T2 | 17 | 0 |
| 76 | Hard | 10×10 | 24 | 1 | yes | yes | T2 | 17 | 0 |
| 77 | Hard | 10×10 | 24 | 1 | yes | yes | T2 | 19 | 0 |
| 78 | Hard | 10×10 | 23 | 1 | yes | yes | T2 | 20 | 0 |
| 79 | Hard | 10×10 | 23 | 1 | yes | yes | T2 | 21 | 0 |
| 80 | Hard | 10×10 | 19 | 1 | yes | yes | T2 | 26 | 0 |
| 81 | Expert | 12×12 | 31 | 1 | yes | yes | T3 | 7 | 1 |
| 82 | Expert | 12×12 | 34 | 1 | yes | yes | T3 | 11 | 1 |
| 83 | Expert | 12×12 | 26 | 1 | yes | yes | T3 | 14 | 1 |
| 84 | Expert | 12×12 | 28 | 1 | yes | yes | T3 | 15 | 1 |
| 85 | Expert | 12×12 | 25 | 1 | yes | yes | T3 | 17 | 1 |
| 86 | Expert | 12×12 | 24 | 1 | yes | yes | T3 | 18 | 1 |
| 87 | Expert | 12×12 | 28 | 1 | yes | yes | T3 | 21 | 1 |
| 88 | Expert | 12×12 | 34 | 1 | yes | yes | T3 | 21 | 1 |
| 89 | Expert | 12×12 | 25 | 1 | yes | yes | T3 | 22 | 1 |
| 90 | Expert | 12×12 | 18 | 1 | yes | yes | T3 | 24 | 1 |
| 91 | Expert | 12×12 | 32 | 1 | yes | yes | T3 | 25 | 1 |
| 92 | Expert | 12×12 | 32 | 1 | yes | yes | T3 | 28 | 1 |
| 93 | Expert | 12×12 | 27 | 1 | yes | yes | T3 | 30 | 1 |
| 94 | Expert | 12×12 | 22 | 1 | yes | yes | T3 | 33 | 1 |
| 95 | Expert | 12×12 | 28 | 1 | yes | yes | T3 | 37 | 1 |
| 96 | Expert | 12×12 | 23 | 1 | yes | yes | T3 | 18 | 2 |
| 97 | Expert | 12×12 | 23 | 1 | yes | yes | T3 | 20 | 2 |
| 98 | Expert | 12×12 | 26 | 1 | yes | yes | T3 | 27 | 2 |
| 99 | Expert | 12×12 | 22 | 1 | yes | yes | T3 | 32 | 2 |
| 100 | Expert | 12×12 | 24 | 1 | yes | yes | T3 | 34 | 3 |

## Reproducibility

`cd src && PYTHONHASHSEED=0 python3 master.py` was run twice on 2026-11-26; both runs wrote a byte-identical `data.json` (SHA-256 `2c6f71c5b44ec134d226021570f9bbcb8b4d66c8b1c7141185908c62ab7e6050`). Seed ranges: Easy from 1000, Medium from 20000, Hard from 300000, Expert from 4000000; worked example seed 7.
