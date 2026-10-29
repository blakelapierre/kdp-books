# Verification report: Snow Paths of Frostwood

Generated 2026-10-27 13:18 PDT by `src/verify.py` in 12073.2 s.

- Puzzles checked: **160** (+ the worked example: unique, solvable with the basic rules alone)
- Well formed and the stored solution obeys every rule (each number's patch has exactly that many squares, one number per patch, one connected path, no 2×2 block of path): **160/160**
- Exactly one solution (SAT solver CaDiCaL via python-sat, with connectivity cuts), equal to the stored solution: **160/160**
- Independent backtracking counter (`nk_bt.py`, no SAT, no shared code) finds exactly one solution, the same one: **160/160**
- Meet their difficulty band (grid size, logic tier needed, number of what-if steps): **160/160**
- Counter cross-check on mutated copies: SAT and backtracking agree in **160/160** cases (mutations gave 0 solutions: 114, exactly 1: 16, 2+: 30)
- No duplicate puzzles: **True**; numbered 1..160 in order: **True**

Logic tiers (the generator's own step-by-step solver, `nurikabe.py`): T1 = basic rules (finished patches, squares between two numbers, out-of-reach squares, the 2×2 rule, one way out for a patch or for the path); T2 = + listing every way a small patch can finish, and squares the path cannot do without; T3 = + one-step trial (what if?).

| Band | Grid | Puzzles | Nos. | Band rule | Numbers per puzzle | Biggest number | What-if steps (range) |
|---|---|---|---|---|---|---|---|
| Easy | 7×7 | 40 | 1–40 | no what-if (T1 or T2) | 5–11 | 6 | 0–0 |
| Medium | 9×9 | 40 | 41–80 | needs exactly T2 | 8–14 | 7 | 0–0 |
| Hard | 10×10 | 40 | 81–120 | needs T3 | 10–18 | 9 | 1–6 |
| Expert | 12×12 | 40 | 121–160 | needs T3 | 17–23 | 10 | 4–38 |

## Per-puzzle results

| # | Band | Grid | Numbers | Path squares | SAT solutions | Unique | Backtracking agrees | Tier | What-if steps |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Easy | 7×7 | 7 | 30 | 1 | yes | yes | T1 | 0 |
| 2 | Easy | 7×7 | 8 | 31 | 1 | yes | yes | T1 | 0 |
| 3 | Easy | 7×7 | 9 | 30 | 1 | yes | yes | T1 | 0 |
| 4 | Easy | 7×7 | 10 | 28 | 1 | yes | yes | T1 | 0 |
| 5 | Easy | 7×7 | 6 | 30 | 1 | yes | yes | T2 | 0 |
| 6 | Easy | 7×7 | 11 | 28 | 1 | yes | yes | T2 | 0 |
| 7 | Easy | 7×7 | 7 | 29 | 1 | yes | yes | T2 | 0 |
| 8 | Easy | 7×7 | 8 | 31 | 1 | yes | yes | T2 | 0 |
| 9 | Easy | 7×7 | 9 | 30 | 1 | yes | yes | T2 | 0 |
| 10 | Easy | 7×7 | 9 | 30 | 1 | yes | yes | T2 | 0 |
| 11 | Easy | 7×7 | 9 | 26 | 1 | yes | yes | T2 | 0 |
| 12 | Easy | 7×7 | 6 | 30 | 1 | yes | yes | T2 | 0 |
| 13 | Easy | 7×7 | 6 | 28 | 1 | yes | yes | T2 | 0 |
| 14 | Easy | 7×7 | 7 | 31 | 1 | yes | yes | T2 | 0 |
| 15 | Easy | 7×7 | 7 | 28 | 1 | yes | yes | T2 | 0 |
| 16 | Easy | 7×7 | 8 | 31 | 1 | yes | yes | T2 | 0 |
| 17 | Easy | 7×7 | 7 | 26 | 1 | yes | yes | T2 | 0 |
| 18 | Easy | 7×7 | 7 | 31 | 1 | yes | yes | T2 | 0 |
| 19 | Easy | 7×7 | 7 | 29 | 1 | yes | yes | T2 | 0 |
| 20 | Easy | 7×7 | 9 | 26 | 1 | yes | yes | T2 | 0 |
| 21 | Easy | 7×7 | 7 | 28 | 1 | yes | yes | T2 | 0 |
| 22 | Easy | 7×7 | 9 | 28 | 1 | yes | yes | T2 | 0 |
| 23 | Easy | 7×7 | 8 | 30 | 1 | yes | yes | T2 | 0 |
| 24 | Easy | 7×7 | 5 | 28 | 1 | yes | yes | T2 | 0 |
| 25 | Easy | 7×7 | 7 | 28 | 1 | yes | yes | T2 | 0 |
| 26 | Easy | 7×7 | 5 | 32 | 1 | yes | yes | T2 | 0 |
| 27 | Easy | 7×7 | 7 | 30 | 1 | yes | yes | T2 | 0 |
| 28 | Easy | 7×7 | 7 | 31 | 1 | yes | yes | T2 | 0 |
| 29 | Easy | 7×7 | 7 | 31 | 1 | yes | yes | T2 | 0 |
| 30 | Easy | 7×7 | 7 | 27 | 1 | yes | yes | T2 | 0 |
| 31 | Easy | 7×7 | 7 | 30 | 1 | yes | yes | T2 | 0 |
| 32 | Easy | 7×7 | 5 | 29 | 1 | yes | yes | T2 | 0 |
| 33 | Easy | 7×7 | 6 | 29 | 1 | yes | yes | T2 | 0 |
| 34 | Easy | 7×7 | 7 | 29 | 1 | yes | yes | T2 | 0 |
| 35 | Easy | 7×7 | 7 | 29 | 1 | yes | yes | T2 | 0 |
| 36 | Easy | 7×7 | 5 | 29 | 1 | yes | yes | T2 | 0 |
| 37 | Easy | 7×7 | 7 | 28 | 1 | yes | yes | T2 | 0 |
| 38 | Easy | 7×7 | 7 | 31 | 1 | yes | yes | T2 | 0 |
| 39 | Easy | 7×7 | 8 | 27 | 1 | yes | yes | T2 | 0 |
| 40 | Easy | 7×7 | 6 | 28 | 1 | yes | yes | T2 | 0 |
| 41 | Medium | 9×9 | 14 | 49 | 1 | yes | yes | T2 | 0 |
| 42 | Medium | 9×9 | 12 | 47 | 1 | yes | yes | T2 | 0 |
| 43 | Medium | 9×9 | 13 | 47 | 1 | yes | yes | T2 | 0 |
| 44 | Medium | 9×9 | 12 | 49 | 1 | yes | yes | T2 | 0 |
| 45 | Medium | 9×9 | 11 | 52 | 1 | yes | yes | T2 | 0 |
| 46 | Medium | 9×9 | 12 | 50 | 1 | yes | yes | T2 | 0 |
| 47 | Medium | 9×9 | 13 | 48 | 1 | yes | yes | T2 | 0 |
| 48 | Medium | 9×9 | 12 | 48 | 1 | yes | yes | T2 | 0 |
| 49 | Medium | 9×9 | 9 | 47 | 1 | yes | yes | T2 | 0 |
| 50 | Medium | 9×9 | 13 | 45 | 1 | yes | yes | T2 | 0 |
| 51 | Medium | 9×9 | 14 | 49 | 1 | yes | yes | T2 | 0 |
| 52 | Medium | 9×9 | 12 | 48 | 1 | yes | yes | T2 | 0 |
| 53 | Medium | 9×9 | 13 | 51 | 1 | yes | yes | T2 | 0 |
| 54 | Medium | 9×9 | 9 | 47 | 1 | yes | yes | T2 | 0 |
| 55 | Medium | 9×9 | 12 | 51 | 1 | yes | yes | T2 | 0 |
| 56 | Medium | 9×9 | 11 | 48 | 1 | yes | yes | T2 | 0 |
| 57 | Medium | 9×9 | 12 | 46 | 1 | yes | yes | T2 | 0 |
| 58 | Medium | 9×9 | 11 | 50 | 1 | yes | yes | T2 | 0 |
| 59 | Medium | 9×9 | 11 | 46 | 1 | yes | yes | T2 | 0 |
| 60 | Medium | 9×9 | 13 | 48 | 1 | yes | yes | T2 | 0 |
| 61 | Medium | 9×9 | 11 | 47 | 1 | yes | yes | T2 | 0 |
| 62 | Medium | 9×9 | 12 | 48 | 1 | yes | yes | T2 | 0 |
| 63 | Medium | 9×9 | 14 | 49 | 1 | yes | yes | T2 | 0 |
| 64 | Medium | 9×9 | 10 | 47 | 1 | yes | yes | T2 | 0 |
| 65 | Medium | 9×9 | 11 | 49 | 1 | yes | yes | T2 | 0 |
| 66 | Medium | 9×9 | 12 | 50 | 1 | yes | yes | T2 | 0 |
| 67 | Medium | 9×9 | 13 | 48 | 1 | yes | yes | T2 | 0 |
| 68 | Medium | 9×9 | 11 | 45 | 1 | yes | yes | T2 | 0 |
| 69 | Medium | 9×9 | 11 | 53 | 1 | yes | yes | T2 | 0 |
| 70 | Medium | 9×9 | 9 | 48 | 1 | yes | yes | T2 | 0 |
| 71 | Medium | 9×9 | 11 | 50 | 1 | yes | yes | T2 | 0 |
| 72 | Medium | 9×9 | 9 | 48 | 1 | yes | yes | T2 | 0 |
| 73 | Medium | 9×9 | 9 | 49 | 1 | yes | yes | T2 | 0 |
| 74 | Medium | 9×9 | 14 | 49 | 1 | yes | yes | T2 | 0 |
| 75 | Medium | 9×9 | 12 | 50 | 1 | yes | yes | T2 | 0 |
| 76 | Medium | 9×9 | 11 | 51 | 1 | yes | yes | T2 | 0 |
| 77 | Medium | 9×9 | 12 | 50 | 1 | yes | yes | T2 | 0 |
| 78 | Medium | 9×9 | 10 | 47 | 1 | yes | yes | T2 | 0 |
| 79 | Medium | 9×9 | 11 | 50 | 1 | yes | yes | T2 | 0 |
| 80 | Medium | 9×9 | 8 | 51 | 1 | yes | yes | T2 | 0 |
| 81 | Hard | 10×10 | 16 | 61 | 1 | yes | yes | T3 | 1 |
| 82 | Hard | 10×10 | 15 | 60 | 1 | yes | yes | T3 | 1 |
| 83 | Hard | 10×10 | 15 | 56 | 1 | yes | yes | T3 | 1 |
| 84 | Hard | 10×10 | 17 | 62 | 1 | yes | yes | T3 | 1 |
| 85 | Hard | 10×10 | 13 | 59 | 1 | yes | yes | T3 | 1 |
| 86 | Hard | 10×10 | 12 | 60 | 1 | yes | yes | T3 | 1 |
| 87 | Hard | 10×10 | 15 | 61 | 1 | yes | yes | T3 | 1 |
| 88 | Hard | 10×10 | 12 | 61 | 1 | yes | yes | T3 | 1 |
| 89 | Hard | 10×10 | 13 | 60 | 1 | yes | yes | T3 | 2 |
| 90 | Hard | 10×10 | 15 | 61 | 1 | yes | yes | T3 | 2 |
| 91 | Hard | 10×10 | 16 | 62 | 1 | yes | yes | T3 | 2 |
| 92 | Hard | 10×10 | 15 | 57 | 1 | yes | yes | T3 | 2 |
| 93 | Hard | 10×10 | 16 | 60 | 1 | yes | yes | T3 | 2 |
| 94 | Hard | 10×10 | 13 | 60 | 1 | yes | yes | T3 | 2 |
| 95 | Hard | 10×10 | 12 | 62 | 1 | yes | yes | T3 | 2 |
| 96 | Hard | 10×10 | 12 | 56 | 1 | yes | yes | T3 | 2 |
| 97 | Hard | 10×10 | 13 | 58 | 1 | yes | yes | T3 | 3 |
| 98 | Hard | 10×10 | 18 | 54 | 1 | yes | yes | T3 | 3 |
| 99 | Hard | 10×10 | 15 | 57 | 1 | yes | yes | T3 | 3 |
| 100 | Hard | 10×10 | 11 | 58 | 1 | yes | yes | T3 | 3 |
| 101 | Hard | 10×10 | 14 | 57 | 1 | yes | yes | T3 | 4 |
| 102 | Hard | 10×10 | 12 | 61 | 1 | yes | yes | T3 | 4 |
| 103 | Hard | 10×10 | 14 | 60 | 1 | yes | yes | T3 | 4 |
| 104 | Hard | 10×10 | 15 | 60 | 1 | yes | yes | T3 | 4 |
| 105 | Hard | 10×10 | 13 | 57 | 1 | yes | yes | T3 | 4 |
| 106 | Hard | 10×10 | 14 | 60 | 1 | yes | yes | T3 | 5 |
| 107 | Hard | 10×10 | 15 | 54 | 1 | yes | yes | T3 | 5 |
| 108 | Hard | 10×10 | 13 | 58 | 1 | yes | yes | T3 | 5 |
| 109 | Hard | 10×10 | 14 | 59 | 1 | yes | yes | T3 | 5 |
| 110 | Hard | 10×10 | 15 | 58 | 1 | yes | yes | T3 | 5 |
| 111 | Hard | 10×10 | 15 | 60 | 1 | yes | yes | T3 | 5 |
| 112 | Hard | 10×10 | 13 | 59 | 1 | yes | yes | T3 | 5 |
| 113 | Hard | 10×10 | 12 | 59 | 1 | yes | yes | T3 | 5 |
| 114 | Hard | 10×10 | 12 | 61 | 1 | yes | yes | T3 | 5 |
| 115 | Hard | 10×10 | 13 | 59 | 1 | yes | yes | T3 | 5 |
| 116 | Hard | 10×10 | 15 | 57 | 1 | yes | yes | T3 | 6 |
| 117 | Hard | 10×10 | 14 | 60 | 1 | yes | yes | T3 | 6 |
| 118 | Hard | 10×10 | 10 | 59 | 1 | yes | yes | T3 | 6 |
| 119 | Hard | 10×10 | 13 | 60 | 1 | yes | yes | T3 | 6 |
| 120 | Hard | 10×10 | 14 | 59 | 1 | yes | yes | T3 | 6 |
| 121 | Expert | 12×12 | 22 | 84 | 1 | yes | yes | T3 | 4 |
| 122 | Expert | 12×12 | 20 | 87 | 1 | yes | yes | T3 | 4 |
| 123 | Expert | 12×12 | 21 | 88 | 1 | yes | yes | T3 | 5 |
| 124 | Expert | 12×12 | 19 | 79 | 1 | yes | yes | T3 | 5 |
| 125 | Expert | 12×12 | 20 | 89 | 1 | yes | yes | T3 | 6 |
| 126 | Expert | 12×12 | 20 | 80 | 1 | yes | yes | T3 | 6 |
| 127 | Expert | 12×12 | 21 | 85 | 1 | yes | yes | T3 | 7 |
| 128 | Expert | 12×12 | 21 | 82 | 1 | yes | yes | T3 | 7 |
| 129 | Expert | 12×12 | 21 | 84 | 1 | yes | yes | T3 | 7 |
| 130 | Expert | 12×12 | 18 | 85 | 1 | yes | yes | T3 | 8 |
| 131 | Expert | 12×12 | 19 | 81 | 1 | yes | yes | T3 | 9 |
| 132 | Expert | 12×12 | 23 | 86 | 1 | yes | yes | T3 | 10 |
| 133 | Expert | 12×12 | 21 | 85 | 1 | yes | yes | T3 | 10 |
| 134 | Expert | 12×12 | 20 | 82 | 1 | yes | yes | T3 | 10 |
| 135 | Expert | 12×12 | 22 | 85 | 1 | yes | yes | T3 | 11 |
| 136 | Expert | 12×12 | 20 | 79 | 1 | yes | yes | T3 | 11 |
| 137 | Expert | 12×12 | 18 | 83 | 1 | yes | yes | T3 | 12 |
| 138 | Expert | 12×12 | 20 | 87 | 1 | yes | yes | T3 | 13 |
| 139 | Expert | 12×12 | 20 | 86 | 1 | yes | yes | T3 | 13 |
| 140 | Expert | 12×12 | 18 | 82 | 1 | yes | yes | T3 | 14 |
| 141 | Expert | 12×12 | 18 | 80 | 1 | yes | yes | T3 | 15 |
| 142 | Expert | 12×12 | 21 | 81 | 1 | yes | yes | T3 | 16 |
| 143 | Expert | 12×12 | 21 | 86 | 1 | yes | yes | T3 | 17 |
| 144 | Expert | 12×12 | 19 | 80 | 1 | yes | yes | T3 | 17 |
| 145 | Expert | 12×12 | 19 | 83 | 1 | yes | yes | T3 | 19 |
| 146 | Expert | 12×12 | 17 | 87 | 1 | yes | yes | T3 | 19 |
| 147 | Expert | 12×12 | 20 | 84 | 1 | yes | yes | T3 | 20 |
| 148 | Expert | 12×12 | 17 | 81 | 1 | yes | yes | T3 | 20 |
| 149 | Expert | 12×12 | 21 | 82 | 1 | yes | yes | T3 | 21 |
| 150 | Expert | 12×12 | 19 | 83 | 1 | yes | yes | T3 | 22 |
| 151 | Expert | 12×12 | 18 | 78 | 1 | yes | yes | T3 | 23 |
| 152 | Expert | 12×12 | 20 | 80 | 1 | yes | yes | T3 | 26 |
| 153 | Expert | 12×12 | 18 | 81 | 1 | yes | yes | T3 | 26 |
| 154 | Expert | 12×12 | 20 | 78 | 1 | yes | yes | T3 | 27 |
| 155 | Expert | 12×12 | 20 | 80 | 1 | yes | yes | T3 | 28 |
| 156 | Expert | 12×12 | 19 | 83 | 1 | yes | yes | T3 | 28 |
| 157 | Expert | 12×12 | 19 | 82 | 1 | yes | yes | T3 | 29 |
| 158 | Expert | 12×12 | 18 | 78 | 1 | yes | yes | T3 | 29 |
| 159 | Expert | 12×12 | 17 | 83 | 1 | yes | yes | T3 | 35 |
| 160 | Expert | 12×12 | 18 | 78 | 1 | yes | yes | T3 | 38 |

**Result: ALL CHECKS PASSED**
