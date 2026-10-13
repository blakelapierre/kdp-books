# Verification report: Bridges of Frostwood

Generated 2026-10-13 10:27 PDT by `src/verify.py` in 0.5 s.

- Puzzles checked: **180** (+ the worked example: unique, solvable with island counting alone)
- Well formed and the stored solution obeys every rule (each island's number met, 1 or 2 bridges per pair, no crossings, one connected network): **180/180**
- Exactly one solution (SAT solver CaDiCaL via python-sat, with connectivity cuts), equal to the stored solution: **180/180**
- Independent backtracking counter (`hashi_bt.py`, no SAT, no shared code) finds exactly one solution, the same one: **180/180**
- Layout (numbers 1–8, no two islands side by side, islands on all four edges of the grid): **180/180**
- Meet their difficulty band (grid size, island count, logic tier needed, number of what-if steps): **180/180**
- Counter cross-check on mutated copies: SAT and backtracking agree in **180/180** cases (mutations gave 0 solutions: 149, exactly 1: 15, 2+: 16)
- No duplicate puzzles: **True**; numbered 1..180 in order: **True**

Logic tiers (the generator's own step-by-step solver): T1 = island counting + crossings; T2 = + network (isolation) rules; T3 = + one-step trial (what if?).

| Band | Grid | Islands | Puzzles | Nos. | Band rule | What-if steps (range) | Highest number |
|---|---|---|---|---|---|---|---|
| Easy | 7×7 | 10–14 | 40 | 1–40 | needs exactly T1 | 0–0 | 8 |
| Medium | 9×9 | 16–22 | 40 | 41–80 | needs exactly T2 | 0–0 | 8 |
| Hard | 11×11 | 22–30 | 50 | 81–130 | needs exactly T3 | 1–3 | 7 |
| Expert | 13×15 | 34–44 | 50 | 131–180 | needs exactly T3 | 2–6 | 8 |

## Per-puzzle results

| # | Band | Grid | Islands | Bridges (doubles) | SAT solutions | Unique | Backtracking agrees | Tier | What-if steps |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Easy | 7×7 | 10 | 9 (4) | 1 | yes | yes | T1 | 0 |
| 2 | Easy | 7×7 | 11 | 11 (6) | 1 | yes | yes | T1 | 0 |
| 3 | Easy | 7×7 | 11 | 10 (4) | 1 | yes | yes | T1 | 0 |
| 4 | Easy | 7×7 | 11 | 10 (7) | 1 | yes | yes | T1 | 0 |
| 5 | Easy | 7×7 | 11 | 11 (5) | 1 | yes | yes | T1 | 0 |
| 6 | Easy | 7×7 | 11 | 10 (5) | 1 | yes | yes | T1 | 0 |
| 7 | Easy | 7×7 | 12 | 12 (6) | 1 | yes | yes | T1 | 0 |
| 8 | Easy | 7×7 | 12 | 13 (11) | 1 | yes | yes | T1 | 0 |
| 9 | Easy | 7×7 | 12 | 13 (9) | 1 | yes | yes | T1 | 0 |
| 10 | Easy | 7×7 | 12 | 14 (7) | 1 | yes | yes | T1 | 0 |
| 11 | Easy | 7×7 | 12 | 11 (7) | 1 | yes | yes | T1 | 0 |
| 12 | Easy | 7×7 | 12 | 11 (4) | 1 | yes | yes | T1 | 0 |
| 13 | Easy | 7×7 | 12 | 13 (7) | 1 | yes | yes | T1 | 0 |
| 14 | Easy | 7×7 | 12 | 11 (5) | 1 | yes | yes | T1 | 0 |
| 15 | Easy | 7×7 | 12 | 13 (5) | 1 | yes | yes | T1 | 0 |
| 16 | Easy | 7×7 | 13 | 12 (6) | 1 | yes | yes | T1 | 0 |
| 17 | Easy | 7×7 | 13 | 13 (6) | 1 | yes | yes | T1 | 0 |
| 18 | Easy | 7×7 | 13 | 12 (5) | 1 | yes | yes | T1 | 0 |
| 19 | Easy | 7×7 | 13 | 12 (7) | 1 | yes | yes | T1 | 0 |
| 20 | Easy | 7×7 | 13 | 12 (6) | 1 | yes | yes | T1 | 0 |
| 21 | Easy | 7×7 | 13 | 13 (5) | 1 | yes | yes | T1 | 0 |
| 22 | Easy | 7×7 | 13 | 12 (4) | 1 | yes | yes | T1 | 0 |
| 23 | Easy | 7×7 | 13 | 14 (8) | 1 | yes | yes | T1 | 0 |
| 24 | Easy | 7×7 | 13 | 12 (7) | 1 | yes | yes | T1 | 0 |
| 25 | Easy | 7×7 | 13 | 12 (6) | 1 | yes | yes | T1 | 0 |
| 26 | Easy | 7×7 | 13 | 13 (4) | 1 | yes | yes | T1 | 0 |
| 27 | Easy | 7×7 | 13 | 12 (4) | 1 | yes | yes | T1 | 0 |
| 28 | Easy | 7×7 | 14 | 14 (9) | 1 | yes | yes | T1 | 0 |
| 29 | Easy | 7×7 | 14 | 13 (4) | 1 | yes | yes | T1 | 0 |
| 30 | Easy | 7×7 | 14 | 13 (5) | 1 | yes | yes | T1 | 0 |
| 31 | Easy | 7×7 | 14 | 15 (10) | 1 | yes | yes | T1 | 0 |
| 32 | Easy | 7×7 | 14 | 14 (9) | 1 | yes | yes | T1 | 0 |
| 33 | Easy | 7×7 | 14 | 14 (6) | 1 | yes | yes | T1 | 0 |
| 34 | Easy | 7×7 | 14 | 13 (6) | 1 | yes | yes | T1 | 0 |
| 35 | Easy | 7×7 | 14 | 13 (4) | 1 | yes | yes | T1 | 0 |
| 36 | Easy | 7×7 | 14 | 14 (9) | 1 | yes | yes | T1 | 0 |
| 37 | Easy | 7×7 | 14 | 15 (9) | 1 | yes | yes | T1 | 0 |
| 38 | Easy | 7×7 | 14 | 13 (5) | 1 | yes | yes | T1 | 0 |
| 39 | Easy | 7×7 | 14 | 14 (8) | 1 | yes | yes | T1 | 0 |
| 40 | Easy | 7×7 | 14 | 14 (9) | 1 | yes | yes | T1 | 0 |
| 41 | Medium | 9×9 | 16 | 15 (7) | 1 | yes | yes | T2 | 0 |
| 42 | Medium | 9×9 | 18 | 18 (8) | 1 | yes | yes | T2 | 0 |
| 43 | Medium | 9×9 | 18 | 18 (9) | 1 | yes | yes | T2 | 0 |
| 44 | Medium | 9×9 | 18 | 18 (8) | 1 | yes | yes | T2 | 0 |
| 45 | Medium | 9×9 | 19 | 19 (6) | 1 | yes | yes | T2 | 0 |
| 46 | Medium | 9×9 | 19 | 19 (13) | 1 | yes | yes | T2 | 0 |
| 47 | Medium | 9×9 | 20 | 21 (7) | 1 | yes | yes | T2 | 0 |
| 48 | Medium | 9×9 | 20 | 21 (10) | 1 | yes | yes | T2 | 0 |
| 49 | Medium | 9×9 | 20 | 20 (5) | 1 | yes | yes | T2 | 0 |
| 50 | Medium | 9×9 | 21 | 22 (7) | 1 | yes | yes | T2 | 0 |
| 51 | Medium | 9×9 | 21 | 20 (3) | 1 | yes | yes | T2 | 0 |
| 52 | Medium | 9×9 | 21 | 23 (7) | 1 | yes | yes | T2 | 0 |
| 53 | Medium | 9×9 | 21 | 23 (9) | 1 | yes | yes | T2 | 0 |
| 54 | Medium | 9×9 | 22 | 22 (8) | 1 | yes | yes | T2 | 0 |
| 55 | Medium | 9×9 | 22 | 22 (8) | 1 | yes | yes | T2 | 0 |
| 56 | Medium | 9×9 | 19 | 20 (11) | 1 | yes | yes | T2 | 0 |
| 57 | Medium | 9×9 | 19 | 19 (8) | 1 | yes | yes | T2 | 0 |
| 58 | Medium | 9×9 | 20 | 23 (13) | 1 | yes | yes | T2 | 0 |
| 59 | Medium | 9×9 | 20 | 22 (13) | 1 | yes | yes | T2 | 0 |
| 60 | Medium | 9×9 | 20 | 21 (6) | 1 | yes | yes | T2 | 0 |
| 61 | Medium | 9×9 | 21 | 20 (10) | 1 | yes | yes | T2 | 0 |
| 62 | Medium | 9×9 | 21 | 20 (9) | 1 | yes | yes | T2 | 0 |
| 63 | Medium | 9×9 | 21 | 22 (6) | 1 | yes | yes | T2 | 0 |
| 64 | Medium | 9×9 | 21 | 22 (8) | 1 | yes | yes | T2 | 0 |
| 65 | Medium | 9×9 | 21 | 21 (6) | 1 | yes | yes | T2 | 0 |
| 66 | Medium | 9×9 | 22 | 22 (11) | 1 | yes | yes | T2 | 0 |
| 67 | Medium | 9×9 | 22 | 22 (11) | 1 | yes | yes | T2 | 0 |
| 68 | Medium | 9×9 | 22 | 21 (8) | 1 | yes | yes | T2 | 0 |
| 69 | Medium | 9×9 | 20 | 19 (2) | 1 | yes | yes | T2 | 0 |
| 70 | Medium | 9×9 | 20 | 21 (6) | 1 | yes | yes | T2 | 0 |
| 71 | Medium | 9×9 | 21 | 21 (4) | 1 | yes | yes | T2 | 0 |
| 72 | Medium | 9×9 | 22 | 23 (4) | 1 | yes | yes | T2 | 0 |
| 73 | Medium | 9×9 | 18 | 18 (6) | 1 | yes | yes | T2 | 0 |
| 74 | Medium | 9×9 | 18 | 17 (3) | 1 | yes | yes | T2 | 0 |
| 75 | Medium | 9×9 | 19 | 20 (9) | 1 | yes | yes | T2 | 0 |
| 76 | Medium | 9×9 | 21 | 22 (7) | 1 | yes | yes | T2 | 0 |
| 77 | Medium | 9×9 | 21 | 21 (7) | 1 | yes | yes | T2 | 0 |
| 78 | Medium | 9×9 | 22 | 21 (4) | 1 | yes | yes | T2 | 0 |
| 79 | Medium | 9×9 | 22 | 22 (4) | 1 | yes | yes | T2 | 0 |
| 80 | Medium | 9×9 | 21 | 21 (2) | 1 | yes | yes | T2 | 0 |
| 81 | Hard | 11×11 | 22 | 21 (9) | 1 | yes | yes | T3 | 1 |
| 82 | Hard | 11×11 | 24 | 25 (8) | 1 | yes | yes | T3 | 1 |
| 83 | Hard | 11×11 | 24 | 23 (10) | 1 | yes | yes | T3 | 1 |
| 84 | Hard | 11×11 | 25 | 26 (12) | 1 | yes | yes | T3 | 1 |
| 85 | Hard | 11×11 | 25 | 25 (9) | 1 | yes | yes | T3 | 1 |
| 86 | Hard | 11×11 | 25 | 25 (10) | 1 | yes | yes | T3 | 1 |
| 87 | Hard | 11×11 | 27 | 29 (11) | 1 | yes | yes | T3 | 1 |
| 88 | Hard | 11×11 | 28 | 31 (20) | 1 | yes | yes | T3 | 1 |
| 89 | Hard | 11×11 | 28 | 27 (14) | 1 | yes | yes | T3 | 1 |
| 90 | Hard | 11×11 | 28 | 28 (13) | 1 | yes | yes | T3 | 1 |
| 91 | Hard | 11×11 | 28 | 30 (12) | 1 | yes | yes | T3 | 1 |
| 92 | Hard | 11×11 | 29 | 29 (7) | 1 | yes | yes | T3 | 1 |
| 93 | Hard | 11×11 | 30 | 29 (15) | 1 | yes | yes | T3 | 1 |
| 94 | Hard | 11×11 | 22 | 22 (9) | 1 | yes | yes | T3 | 1 |
| 95 | Hard | 11×11 | 23 | 23 (7) | 1 | yes | yes | T3 | 1 |
| 96 | Hard | 11×11 | 24 | 25 (8) | 1 | yes | yes | T3 | 1 |
| 97 | Hard | 11×11 | 27 | 29 (9) | 1 | yes | yes | T3 | 1 |
| 98 | Hard | 11×11 | 27 | 27 (15) | 1 | yes | yes | T3 | 1 |
| 99 | Hard | 11×11 | 29 | 30 (16) | 1 | yes | yes | T3 | 1 |
| 100 | Hard | 11×11 | 22 | 22 (9) | 1 | yes | yes | T3 | 1 |
| 101 | Hard | 11×11 | 23 | 23 (4) | 1 | yes | yes | T3 | 1 |
| 102 | Hard | 11×11 | 25 | 26 (10) | 1 | yes | yes | T3 | 1 |
| 103 | Hard | 11×11 | 29 | 28 (3) | 1 | yes | yes | T3 | 1 |
| 104 | Hard | 11×11 | 23 | 23 (7) | 1 | yes | yes | T3 | 1 |
| 105 | Hard | 11×11 | 27 | 28 (13) | 1 | yes | yes | T3 | 1 |
| 106 | Hard | 11×11 | 28 | 30 (10) | 1 | yes | yes | T3 | 1 |
| 107 | Hard | 11×11 | 23 | 22 (4) | 1 | yes | yes | T3 | 1 |
| 108 | Hard | 11×11 | 26 | 27 (5) | 1 | yes | yes | T3 | 1 |
| 109 | Hard | 11×11 | 27 | 28 (8) | 1 | yes | yes | T3 | 1 |
| 110 | Hard | 11×11 | 29 | 29 (9) | 1 | yes | yes | T3 | 1 |
| 111 | Hard | 11×11 | 28 | 30 (9) | 1 | yes | yes | T3 | 1 |
| 112 | Hard | 11×11 | 26 | 27 (6) | 1 | yes | yes | T3 | 1 |
| 113 | Hard | 11×11 | 29 | 29 (8) | 1 | yes | yes | T3 | 1 |
| 114 | Hard | 11×11 | 22 | 21 (8) | 1 | yes | yes | T3 | 2 |
| 115 | Hard | 11×11 | 25 | 24 (9) | 1 | yes | yes | T3 | 2 |
| 116 | Hard | 11×11 | 25 | 27 (9) | 1 | yes | yes | T3 | 2 |
| 117 | Hard | 11×11 | 27 | 29 (9) | 1 | yes | yes | T3 | 2 |
| 118 | Hard | 11×11 | 29 | 30 (10) | 1 | yes | yes | T3 | 2 |
| 119 | Hard | 11×11 | 30 | 31 (19) | 1 | yes | yes | T3 | 2 |
| 120 | Hard | 11×11 | 25 | 26 (11) | 1 | yes | yes | T3 | 2 |
| 121 | Hard | 11×11 | 28 | 29 (9) | 1 | yes | yes | T3 | 2 |
| 122 | Hard | 11×11 | 28 | 29 (10) | 1 | yes | yes | T3 | 2 |
| 123 | Hard | 11×11 | 23 | 24 (6) | 1 | yes | yes | T3 | 2 |
| 124 | Hard | 11×11 | 22 | 22 (5) | 1 | yes | yes | T3 | 2 |
| 125 | Hard | 11×11 | 23 | 23 (3) | 1 | yes | yes | T3 | 2 |
| 126 | Hard | 11×11 | 23 | 26 (11) | 1 | yes | yes | T3 | 3 |
| 127 | Hard | 11×11 | 26 | 26 (12) | 1 | yes | yes | T3 | 3 |
| 128 | Hard | 11×11 | 27 | 29 (14) | 1 | yes | yes | T3 | 3 |
| 129 | Hard | 11×11 | 26 | 28 (12) | 1 | yes | yes | T3 | 3 |
| 130 | Hard | 11×11 | 28 | 30 (8) | 1 | yes | yes | T3 | 3 |
| 131 | Expert | 13×15 | 35 | 37 (20) | 1 | yes | yes | T3 | 2 |
| 132 | Expert | 13×15 | 36 | 40 (17) | 1 | yes | yes | T3 | 2 |
| 133 | Expert | 13×15 | 37 | 38 (17) | 1 | yes | yes | T3 | 2 |
| 134 | Expert | 13×15 | 38 | 41 (21) | 1 | yes | yes | T3 | 2 |
| 135 | Expert | 13×15 | 38 | 43 (12) | 1 | yes | yes | T3 | 2 |
| 136 | Expert | 13×15 | 40 | 40 (16) | 1 | yes | yes | T3 | 2 |
| 137 | Expert | 13×15 | 41 | 43 (24) | 1 | yes | yes | T3 | 2 |
| 138 | Expert | 13×15 | 42 | 44 (14) | 1 | yes | yes | T3 | 2 |
| 139 | Expert | 13×15 | 42 | 48 (23) | 1 | yes | yes | T3 | 2 |
| 140 | Expert | 13×15 | 36 | 37 (20) | 1 | yes | yes | T3 | 2 |
| 141 | Expert | 13×15 | 37 | 38 (16) | 1 | yes | yes | T3 | 2 |
| 142 | Expert | 13×15 | 38 | 40 (23) | 1 | yes | yes | T3 | 2 |
| 143 | Expert | 13×15 | 38 | 39 (15) | 1 | yes | yes | T3 | 2 |
| 144 | Expert | 13×15 | 39 | 42 (23) | 1 | yes | yes | T3 | 2 |
| 145 | Expert | 13×15 | 41 | 45 (16) | 1 | yes | yes | T3 | 2 |
| 146 | Expert | 13×15 | 43 | 47 (25) | 1 | yes | yes | T3 | 2 |
| 147 | Expert | 13×15 | 39 | 38 (18) | 1 | yes | yes | T3 | 2 |
| 148 | Expert | 13×15 | 41 | 42 (18) | 1 | yes | yes | T3 | 2 |
| 149 | Expert | 13×15 | 43 | 44 (11) | 1 | yes | yes | T3 | 2 |
| 150 | Expert | 13×15 | 37 | 39 (11) | 1 | yes | yes | T3 | 2 |
| 151 | Expert | 13×15 | 37 | 41 (20) | 1 | yes | yes | T3 | 2 |
| 152 | Expert | 13×15 | 39 | 41 (11) | 1 | yes | yes | T3 | 2 |
| 153 | Expert | 13×15 | 41 | 45 (18) | 1 | yes | yes | T3 | 2 |
| 154 | Expert | 13×15 | 42 | 45 (18) | 1 | yes | yes | T3 | 2 |
| 155 | Expert | 13×15 | 39 | 41 (12) | 1 | yes | yes | T3 | 2 |
| 156 | Expert | 13×15 | 40 | 42 (15) | 1 | yes | yes | T3 | 2 |
| 157 | Expert | 13×15 | 42 | 42 (17) | 1 | yes | yes | T3 | 2 |
| 158 | Expert | 13×15 | 42 | 47 (16) | 1 | yes | yes | T3 | 2 |
| 159 | Expert | 13×15 | 42 | 44 (16) | 1 | yes | yes | T3 | 2 |
| 160 | Expert | 13×15 | 44 | 45 (14) | 1 | yes | yes | T3 | 2 |
| 161 | Expert | 13×15 | 36 | 36 (11) | 1 | yes | yes | T3 | 2 |
| 162 | Expert | 13×15 | 38 | 42 (21) | 1 | yes | yes | T3 | 2 |
| 163 | Expert | 13×15 | 44 | 46 (11) | 1 | yes | yes | T3 | 2 |
| 164 | Expert | 13×15 | 37 | 40 (16) | 1 | yes | yes | T3 | 2 |
| 165 | Expert | 13×15 | 44 | 47 (13) | 1 | yes | yes | T3 | 2 |
| 166 | Expert | 13×15 | 36 | 38 (9) | 1 | yes | yes | T3 | 2 |
| 167 | Expert | 13×15 | 42 | 44 (15) | 1 | yes | yes | T3 | 3 |
| 168 | Expert | 13×15 | 37 | 39 (16) | 1 | yes | yes | T3 | 3 |
| 169 | Expert | 13×15 | 39 | 42 (22) | 1 | yes | yes | T3 | 3 |
| 170 | Expert | 13×15 | 40 | 42 (18) | 1 | yes | yes | T3 | 3 |
| 171 | Expert | 13×15 | 37 | 40 (16) | 1 | yes | yes | T3 | 3 |
| 172 | Expert | 13×15 | 40 | 45 (15) | 1 | yes | yes | T3 | 3 |
| 173 | Expert | 13×15 | 34 | 35 (7) | 1 | yes | yes | T3 | 3 |
| 174 | Expert | 13×15 | 36 | 37 (12) | 1 | yes | yes | T3 | 3 |
| 175 | Expert | 13×15 | 43 | 48 (19) | 1 | yes | yes | T3 | 4 |
| 176 | Expert | 13×15 | 34 | 38 (19) | 1 | yes | yes | T3 | 5 |
| 177 | Expert | 13×15 | 37 | 39 (15) | 1 | yes | yes | T3 | 5 |
| 178 | Expert | 13×15 | 40 | 43 (15) | 1 | yes | yes | T3 | 5 |
| 179 | Expert | 13×15 | 42 | 43 (16) | 1 | yes | yes | T3 | 5 |
| 180 | Expert | 13×15 | 38 | 39 (10) | 1 | yes | yes | T3 | 6 |
