# Verification report

Generated 2026-09-30 10:12 PDT by `src/verify.py` in 34.1 s.

- Puzzles checked: **180** (+ the worked example: unique, solvable at T2)
- Well formed (n×n, n connected regions) and stored solution obeys every rule (k per row/column/region, no touching): **180/180**
- Exactly one solution (independent SAT solver, CaDiCaL via python-sat, blocking-clause enumeration), matching stored solution: **180/180**
- Meet difficulty band (grid size, stars per unit, solvable at band tier, not solvable at the band's fail tier): **180/180**
- Counter cross-check on mutated copies (one square moved to a neighbouring region): SAT and backtracking counts agree in **180/180** cases (mutations gave 0 solutions: 28, 1: 119, 2+: 33, so the SAT counter demonstrably detects both broken and ambiguous grids)
- No duplicate puzzles: **True**; numbered 1..180 in order: **True**

Logic tiers: T1 = singles; T2 = + one-unit placements & single confinement; T3 = + multi-unit confinement (2–4 units); T4 = + one-step trial

| Band | Grid | Stars | Puzzles | Nos. | Band rule | Tier needed (count) |
|---|---|---|---|---|---|---|
| Easy | 6×6 | 1 | 40 | 1–40 | solvable ≤T2 | T1: 11, T2: 29 |
| Medium | 8×8 | 1 | 40 | 41–80 | solvable ≤T3, not ≤T1 | T2: 30, T3: 10 |
| Hard | 10×10 | 2 | 50 | 81–130 | solvable ≤T3, not ≤T2 | T3: 50 |
| Expert | 10×10 | 2 | 50 | 131–180 | solvable ≤T4, not ≤T3 | T4: 50 |

## Per-puzzle results

| # | Band | Grid | Stars | SAT solutions | Unique | Tier needed | Counters agree |
|---|---|---|---|---|---|---|---|
| 1 | Easy | 6×6 | 1 | 1 | yes | T1 | yes |
| 2 | Easy | 6×6 | 1 | 1 | yes | T1 | yes |
| 3 | Easy | 6×6 | 1 | 1 | yes | T1 | yes |
| 4 | Easy | 6×6 | 1 | 1 | yes | T1 | yes |
| 5 | Easy | 6×6 | 1 | 1 | yes | T1 | yes |
| 6 | Easy | 6×6 | 1 | 1 | yes | T1 | yes |
| 7 | Easy | 6×6 | 1 | 1 | yes | T1 | yes |
| 8 | Easy | 6×6 | 1 | 1 | yes | T1 | yes |
| 9 | Easy | 6×6 | 1 | 1 | yes | T1 | yes |
| 10 | Easy | 6×6 | 1 | 1 | yes | T1 | yes |
| 11 | Easy | 6×6 | 1 | 1 | yes | T1 | yes |
| 12 | Easy | 6×6 | 1 | 1 | yes | T2 | yes |
| 13 | Easy | 6×6 | 1 | 1 | yes | T2 | yes |
| 14 | Easy | 6×6 | 1 | 1 | yes | T2 | yes |
| 15 | Easy | 6×6 | 1 | 1 | yes | T2 | yes |
| 16 | Easy | 6×6 | 1 | 1 | yes | T2 | yes |
| 17 | Easy | 6×6 | 1 | 1 | yes | T2 | yes |
| 18 | Easy | 6×6 | 1 | 1 | yes | T2 | yes |
| 19 | Easy | 6×6 | 1 | 1 | yes | T2 | yes |
| 20 | Easy | 6×6 | 1 | 1 | yes | T2 | yes |
| 21 | Easy | 6×6 | 1 | 1 | yes | T2 | yes |
| 22 | Easy | 6×6 | 1 | 1 | yes | T2 | yes |
| 23 | Easy | 6×6 | 1 | 1 | yes | T2 | yes |
| 24 | Easy | 6×6 | 1 | 1 | yes | T2 | yes |
| 25 | Easy | 6×6 | 1 | 1 | yes | T2 | yes |
| 26 | Easy | 6×6 | 1 | 1 | yes | T2 | yes |
| 27 | Easy | 6×6 | 1 | 1 | yes | T2 | yes |
| 28 | Easy | 6×6 | 1 | 1 | yes | T2 | yes |
| 29 | Easy | 6×6 | 1 | 1 | yes | T2 | yes |
| 30 | Easy | 6×6 | 1 | 1 | yes | T2 | yes |
| 31 | Easy | 6×6 | 1 | 1 | yes | T2 | yes |
| 32 | Easy | 6×6 | 1 | 1 | yes | T2 | yes |
| 33 | Easy | 6×6 | 1 | 1 | yes | T2 | yes |
| 34 | Easy | 6×6 | 1 | 1 | yes | T2 | yes |
| 35 | Easy | 6×6 | 1 | 1 | yes | T2 | yes |
| 36 | Easy | 6×6 | 1 | 1 | yes | T2 | yes |
| 37 | Easy | 6×6 | 1 | 1 | yes | T2 | yes |
| 38 | Easy | 6×6 | 1 | 1 | yes | T2 | yes |
| 39 | Easy | 6×6 | 1 | 1 | yes | T2 | yes |
| 40 | Easy | 6×6 | 1 | 1 | yes | T2 | yes |
| 41 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 42 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 43 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 44 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 45 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 46 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 47 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 48 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 49 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 50 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 51 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 52 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 53 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 54 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 55 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 56 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 57 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 58 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 59 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 60 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 61 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 62 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 63 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 64 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 65 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 66 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 67 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 68 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 69 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 70 | Medium | 8×8 | 1 | 1 | yes | T2 | yes |
| 71 | Medium | 8×8 | 1 | 1 | yes | T3 | yes |
| 72 | Medium | 8×8 | 1 | 1 | yes | T3 | yes |
| 73 | Medium | 8×8 | 1 | 1 | yes | T3 | yes |
| 74 | Medium | 8×8 | 1 | 1 | yes | T3 | yes |
| 75 | Medium | 8×8 | 1 | 1 | yes | T3 | yes |
| 76 | Medium | 8×8 | 1 | 1 | yes | T3 | yes |
| 77 | Medium | 8×8 | 1 | 1 | yes | T3 | yes |
| 78 | Medium | 8×8 | 1 | 1 | yes | T3 | yes |
| 79 | Medium | 8×8 | 1 | 1 | yes | T3 | yes |
| 80 | Medium | 8×8 | 1 | 1 | yes | T3 | yes |
| 81 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 82 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 83 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 84 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 85 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 86 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 87 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 88 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 89 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 90 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 91 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 92 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 93 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 94 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 95 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 96 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 97 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 98 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 99 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 100 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 101 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 102 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 103 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 104 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 105 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 106 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 107 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 108 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 109 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 110 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 111 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 112 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 113 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 114 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 115 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 116 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 117 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 118 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 119 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 120 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 121 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 122 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 123 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 124 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 125 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 126 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 127 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 128 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 129 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 130 | Hard | 10×10 | 2 | 1 | yes | T3 | yes |
| 131 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 132 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 133 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 134 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 135 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 136 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 137 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 138 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 139 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 140 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 141 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 142 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 143 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 144 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 145 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 146 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 147 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 148 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 149 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 150 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 151 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 152 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 153 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 154 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 155 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 156 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 157 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 158 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 159 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 160 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 161 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 162 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 163 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 164 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 165 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 166 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 167 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 168 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 169 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 170 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 171 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 172 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 173 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 174 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 175 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 176 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 177 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 178 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 179 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
| 180 | Expert | 10×10 | 2 | 1 | yes | T4 | yes |
