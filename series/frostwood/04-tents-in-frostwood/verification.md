# Verification report

Generated 2026-10-01 09:45 PDT by `src/verify.py` in 16.0 s.

- Puzzles checked: **180** (+ the worked example: unique, solvable)
- Well formed and stored solution obeys every rule (one tent per tree, tents do not touch even diagonally, row/column counts): **180/180**
- Exactly one solution (independent SAT solver, CaDiCaL via python-sat), matching stored solution: **180/180**
- Independent backtracking counter agrees with SAT on each puzzle: **180/180**
- Meet difficulty band (grid size, tree count, solvable at band tier, not solvable at the band's fail tier): **180/180**
- Counter cross-check on mutated copies: SAT and backtracking counts agree in **180/180** cases (mutations gave 0 solutions: 165, 1: 15, 2+: 0)
- No duplicate puzzles: **True**; numbered 1..180 in order: **True**

Logic tiers: T1 = row/col fills & forced tree neighbours; T2 = + orphan-cell clearing; T3 = + small-set confinement; T4 = + one-step trial (what if?)

| Band | Grid | Trees | Puzzles | Nos. | Band rule | Tier needed (count) |
|---|---|---|---|---|---|---|
| Easy | 6×6 | 5–7 | 40 | 1–40 | solvable ≤T1 | T1: 40 |
| Medium | 8×8 | 9–12 | 40 | 41–80 | solvable ≤T4, not ≤T1 | T4: 40 |
| Hard | 10×10 | 14–18 | 50 | 81–130 | solvable ≤T4, not ≤T1 | T4: 50 |
| Expert | 12×12 | 20–26 | 50 | 131–180 | solvable ≤T4, not ≤T1 | T4: 50 |

## Per-puzzle results

| # | Band | Grid | Trees | SAT solutions | Unique | Tier needed | Counters agree |
|---|---|---|---|---|---|---|---|
| 1 | Easy | 6×6 | 5 | 1 | yes | T1 | yes |
| 2 | Easy | 6×6 | 5 | 1 | yes | T1 | yes |
| 3 | Easy | 6×6 | 6 | 1 | yes | T1 | yes |
| 4 | Easy | 6×6 | 6 | 1 | yes | T1 | yes |
| 5 | Easy | 6×6 | 5 | 1 | yes | T1 | yes |
| 6 | Easy | 6×6 | 6 | 1 | yes | T1 | yes |
| 7 | Easy | 6×6 | 7 | 1 | yes | T1 | yes |
| 8 | Easy | 6×6 | 6 | 1 | yes | T1 | yes |
| 9 | Easy | 6×6 | 6 | 1 | yes | T1 | yes |
| 10 | Easy | 6×6 | 5 | 1 | yes | T1 | yes |
| 11 | Easy | 6×6 | 6 | 1 | yes | T1 | yes |
| 12 | Easy | 6×6 | 6 | 1 | yes | T1 | yes |
| 13 | Easy | 6×6 | 5 | 1 | yes | T1 | yes |
| 14 | Easy | 6×6 | 5 | 1 | yes | T1 | yes |
| 15 | Easy | 6×6 | 5 | 1 | yes | T1 | yes |
| 16 | Easy | 6×6 | 6 | 1 | yes | T1 | yes |
| 17 | Easy | 6×6 | 6 | 1 | yes | T1 | yes |
| 18 | Easy | 6×6 | 5 | 1 | yes | T1 | yes |
| 19 | Easy | 6×6 | 5 | 1 | yes | T1 | yes |
| 20 | Easy | 6×6 | 5 | 1 | yes | T1 | yes |
| 21 | Easy | 6×6 | 6 | 1 | yes | T1 | yes |
| 22 | Easy | 6×6 | 5 | 1 | yes | T1 | yes |
| 23 | Easy | 6×6 | 7 | 1 | yes | T1 | yes |
| 24 | Easy | 6×6 | 6 | 1 | yes | T1 | yes |
| 25 | Easy | 6×6 | 5 | 1 | yes | T1 | yes |
| 26 | Easy | 6×6 | 7 | 1 | yes | T1 | yes |
| 27 | Easy | 6×6 | 7 | 1 | yes | T1 | yes |
| 28 | Easy | 6×6 | 5 | 1 | yes | T1 | yes |
| 29 | Easy | 6×6 | 5 | 1 | yes | T1 | yes |
| 30 | Easy | 6×6 | 5 | 1 | yes | T1 | yes |
| 31 | Easy | 6×6 | 7 | 1 | yes | T1 | yes |
| 32 | Easy | 6×6 | 7 | 1 | yes | T1 | yes |
| 33 | Easy | 6×6 | 5 | 1 | yes | T1 | yes |
| 34 | Easy | 6×6 | 6 | 1 | yes | T1 | yes |
| 35 | Easy | 6×6 | 7 | 1 | yes | T1 | yes |
| 36 | Easy | 6×6 | 6 | 1 | yes | T1 | yes |
| 37 | Easy | 6×6 | 5 | 1 | yes | T1 | yes |
| 38 | Easy | 6×6 | 7 | 1 | yes | T1 | yes |
| 39 | Easy | 6×6 | 6 | 1 | yes | T1 | yes |
| 40 | Easy | 6×6 | 6 | 1 | yes | T1 | yes |
| 41 | Medium | 8×8 | 11 | 1 | yes | T4 | yes |
| 42 | Medium | 8×8 | 11 | 1 | yes | T4 | yes |
| 43 | Medium | 8×8 | 11 | 1 | yes | T4 | yes |
| 44 | Medium | 8×8 | 9 | 1 | yes | T4 | yes |
| 45 | Medium | 8×8 | 10 | 1 | yes | T4 | yes |
| 46 | Medium | 8×8 | 10 | 1 | yes | T4 | yes |
| 47 | Medium | 8×8 | 11 | 1 | yes | T4 | yes |
| 48 | Medium | 8×8 | 12 | 1 | yes | T4 | yes |
| 49 | Medium | 8×8 | 12 | 1 | yes | T4 | yes |
| 50 | Medium | 8×8 | 11 | 1 | yes | T4 | yes |
| 51 | Medium | 8×8 | 9 | 1 | yes | T4 | yes |
| 52 | Medium | 8×8 | 12 | 1 | yes | T4 | yes |
| 53 | Medium | 8×8 | 9 | 1 | yes | T4 | yes |
| 54 | Medium | 8×8 | 12 | 1 | yes | T4 | yes |
| 55 | Medium | 8×8 | 9 | 1 | yes | T4 | yes |
| 56 | Medium | 8×8 | 9 | 1 | yes | T4 | yes |
| 57 | Medium | 8×8 | 10 | 1 | yes | T4 | yes |
| 58 | Medium | 8×8 | 12 | 1 | yes | T4 | yes |
| 59 | Medium | 8×8 | 12 | 1 | yes | T4 | yes |
| 60 | Medium | 8×8 | 12 | 1 | yes | T4 | yes |
| 61 | Medium | 8×8 | 11 | 1 | yes | T4 | yes |
| 62 | Medium | 8×8 | 12 | 1 | yes | T4 | yes |
| 63 | Medium | 8×8 | 12 | 1 | yes | T4 | yes |
| 64 | Medium | 8×8 | 9 | 1 | yes | T4 | yes |
| 65 | Medium | 8×8 | 9 | 1 | yes | T4 | yes |
| 66 | Medium | 8×8 | 10 | 1 | yes | T4 | yes |
| 67 | Medium | 8×8 | 12 | 1 | yes | T4 | yes |
| 68 | Medium | 8×8 | 12 | 1 | yes | T4 | yes |
| 69 | Medium | 8×8 | 12 | 1 | yes | T4 | yes |
| 70 | Medium | 8×8 | 12 | 1 | yes | T4 | yes |
| 71 | Medium | 8×8 | 9 | 1 | yes | T4 | yes |
| 72 | Medium | 8×8 | 11 | 1 | yes | T4 | yes |
| 73 | Medium | 8×8 | 11 | 1 | yes | T4 | yes |
| 74 | Medium | 8×8 | 12 | 1 | yes | T4 | yes |
| 75 | Medium | 8×8 | 10 | 1 | yes | T4 | yes |
| 76 | Medium | 8×8 | 11 | 1 | yes | T4 | yes |
| 77 | Medium | 8×8 | 11 | 1 | yes | T4 | yes |
| 78 | Medium | 8×8 | 12 | 1 | yes | T4 | yes |
| 79 | Medium | 8×8 | 11 | 1 | yes | T4 | yes |
| 80 | Medium | 8×8 | 10 | 1 | yes | T4 | yes |
| 81 | Hard | 10×10 | 16 | 1 | yes | T4 | yes |
| 82 | Hard | 10×10 | 14 | 1 | yes | T4 | yes |
| 83 | Hard | 10×10 | 15 | 1 | yes | T4 | yes |
| 84 | Hard | 10×10 | 15 | 1 | yes | T4 | yes |
| 85 | Hard | 10×10 | 17 | 1 | yes | T4 | yes |
| 86 | Hard | 10×10 | 15 | 1 | yes | T4 | yes |
| 87 | Hard | 10×10 | 16 | 1 | yes | T4 | yes |
| 88 | Hard | 10×10 | 14 | 1 | yes | T4 | yes |
| 89 | Hard | 10×10 | 16 | 1 | yes | T4 | yes |
| 90 | Hard | 10×10 | 18 | 1 | yes | T4 | yes |
| 91 | Hard | 10×10 | 18 | 1 | yes | T4 | yes |
| 92 | Hard | 10×10 | 17 | 1 | yes | T4 | yes |
| 93 | Hard | 10×10 | 18 | 1 | yes | T4 | yes |
| 94 | Hard | 10×10 | 17 | 1 | yes | T4 | yes |
| 95 | Hard | 10×10 | 16 | 1 | yes | T4 | yes |
| 96 | Hard | 10×10 | 15 | 1 | yes | T4 | yes |
| 97 | Hard | 10×10 | 14 | 1 | yes | T4 | yes |
| 98 | Hard | 10×10 | 15 | 1 | yes | T4 | yes |
| 99 | Hard | 10×10 | 17 | 1 | yes | T4 | yes |
| 100 | Hard | 10×10 | 14 | 1 | yes | T4 | yes |
| 101 | Hard | 10×10 | 16 | 1 | yes | T4 | yes |
| 102 | Hard | 10×10 | 14 | 1 | yes | T4 | yes |
| 103 | Hard | 10×10 | 16 | 1 | yes | T4 | yes |
| 104 | Hard | 10×10 | 15 | 1 | yes | T4 | yes |
| 105 | Hard | 10×10 | 17 | 1 | yes | T4 | yes |
| 106 | Hard | 10×10 | 15 | 1 | yes | T4 | yes |
| 107 | Hard | 10×10 | 15 | 1 | yes | T4 | yes |
| 108 | Hard | 10×10 | 17 | 1 | yes | T4 | yes |
| 109 | Hard | 10×10 | 17 | 1 | yes | T4 | yes |
| 110 | Hard | 10×10 | 17 | 1 | yes | T4 | yes |
| 111 | Hard | 10×10 | 14 | 1 | yes | T4 | yes |
| 112 | Hard | 10×10 | 16 | 1 | yes | T4 | yes |
| 113 | Hard | 10×10 | 15 | 1 | yes | T4 | yes |
| 114 | Hard | 10×10 | 15 | 1 | yes | T4 | yes |
| 115 | Hard | 10×10 | 17 | 1 | yes | T4 | yes |
| 116 | Hard | 10×10 | 17 | 1 | yes | T4 | yes |
| 117 | Hard | 10×10 | 17 | 1 | yes | T4 | yes |
| 118 | Hard | 10×10 | 18 | 1 | yes | T4 | yes |
| 119 | Hard | 10×10 | 16 | 1 | yes | T4 | yes |
| 120 | Hard | 10×10 | 18 | 1 | yes | T4 | yes |
| 121 | Hard | 10×10 | 16 | 1 | yes | T4 | yes |
| 122 | Hard | 10×10 | 16 | 1 | yes | T4 | yes |
| 123 | Hard | 10×10 | 17 | 1 | yes | T4 | yes |
| 124 | Hard | 10×10 | 18 | 1 | yes | T4 | yes |
| 125 | Hard | 10×10 | 17 | 1 | yes | T4 | yes |
| 126 | Hard | 10×10 | 15 | 1 | yes | T4 | yes |
| 127 | Hard | 10×10 | 18 | 1 | yes | T4 | yes |
| 128 | Hard | 10×10 | 14 | 1 | yes | T4 | yes |
| 129 | Hard | 10×10 | 18 | 1 | yes | T4 | yes |
| 130 | Hard | 10×10 | 18 | 1 | yes | T4 | yes |
| 131 | Expert | 12×12 | 21 | 1 | yes | T4 | yes |
| 132 | Expert | 12×12 | 22 | 1 | yes | T4 | yes |
| 133 | Expert | 12×12 | 22 | 1 | yes | T4 | yes |
| 134 | Expert | 12×12 | 25 | 1 | yes | T4 | yes |
| 135 | Expert | 12×12 | 26 | 1 | yes | T4 | yes |
| 136 | Expert | 12×12 | 21 | 1 | yes | T4 | yes |
| 137 | Expert | 12×12 | 20 | 1 | yes | T4 | yes |
| 138 | Expert | 12×12 | 21 | 1 | yes | T4 | yes |
| 139 | Expert | 12×12 | 23 | 1 | yes | T4 | yes |
| 140 | Expert | 12×12 | 23 | 1 | yes | T4 | yes |
| 141 | Expert | 12×12 | 25 | 1 | yes | T4 | yes |
| 142 | Expert | 12×12 | 23 | 1 | yes | T4 | yes |
| 143 | Expert | 12×12 | 21 | 1 | yes | T4 | yes |
| 144 | Expert | 12×12 | 25 | 1 | yes | T4 | yes |
| 145 | Expert | 12×12 | 23 | 1 | yes | T4 | yes |
| 146 | Expert | 12×12 | 22 | 1 | yes | T4 | yes |
| 147 | Expert | 12×12 | 23 | 1 | yes | T4 | yes |
| 148 | Expert | 12×12 | 25 | 1 | yes | T4 | yes |
| 149 | Expert | 12×12 | 21 | 1 | yes | T4 | yes |
| 150 | Expert | 12×12 | 21 | 1 | yes | T4 | yes |
| 151 | Expert | 12×12 | 21 | 1 | yes | T4 | yes |
| 152 | Expert | 12×12 | 25 | 1 | yes | T4 | yes |
| 153 | Expert | 12×12 | 23 | 1 | yes | T4 | yes |
| 154 | Expert | 12×12 | 26 | 1 | yes | T4 | yes |
| 155 | Expert | 12×12 | 22 | 1 | yes | T4 | yes |
| 156 | Expert | 12×12 | 21 | 1 | yes | T4 | yes |
| 157 | Expert | 12×12 | 23 | 1 | yes | T4 | yes |
| 158 | Expert | 12×12 | 24 | 1 | yes | T4 | yes |
| 159 | Expert | 12×12 | 25 | 1 | yes | T4 | yes |
| 160 | Expert | 12×12 | 24 | 1 | yes | T4 | yes |
| 161 | Expert | 12×12 | 23 | 1 | yes | T4 | yes |
| 162 | Expert | 12×12 | 23 | 1 | yes | T4 | yes |
| 163 | Expert | 12×12 | 25 | 1 | yes | T4 | yes |
| 164 | Expert | 12×12 | 24 | 1 | yes | T4 | yes |
| 165 | Expert | 12×12 | 25 | 1 | yes | T4 | yes |
| 166 | Expert | 12×12 | 21 | 1 | yes | T4 | yes |
| 167 | Expert | 12×12 | 26 | 1 | yes | T4 | yes |
| 168 | Expert | 12×12 | 21 | 1 | yes | T4 | yes |
| 169 | Expert | 12×12 | 24 | 1 | yes | T4 | yes |
| 170 | Expert | 12×12 | 24 | 1 | yes | T4 | yes |
| 171 | Expert | 12×12 | 25 | 1 | yes | T4 | yes |
| 172 | Expert | 12×12 | 21 | 1 | yes | T4 | yes |
| 173 | Expert | 12×12 | 22 | 1 | yes | T4 | yes |
| 174 | Expert | 12×12 | 23 | 1 | yes | T4 | yes |
| 175 | Expert | 12×12 | 26 | 1 | yes | T4 | yes |
| 176 | Expert | 12×12 | 24 | 1 | yes | T4 | yes |
| 177 | Expert | 12×12 | 26 | 1 | yes | T4 | yes |
| 178 | Expert | 12×12 | 25 | 1 | yes | T4 | yes |
| 179 | Expert | 12×12 | 24 | 1 | yes | T4 | yes |
| 180 | Expert | 12×12 | 21 | 1 | yes | T4 | yes |
