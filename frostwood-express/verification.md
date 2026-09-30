# Verification report

Generated 2026-09-30 08:57 PDT by `src/verify.py` in 6.4 s.

- Puzzles checked: **200** (+ the worked example: unique)
- Exactly one solution (independent SAT solver, CaDiCaL via python-sat, stray loops cut lazily), matching stored solution: **200/200**
- Stored solutions satisfy every row/column count, the entry/exit and every given piece: **200/200**
- Meet difficulty band (grid size, solvable at band tier, not solvable one tier lower): **200/200**
- Sanity check of the counter: removing any single given from a puzzle makes the SAT solver find a 2nd solution in **306/944** cases (the other givens are not needed for uniqueness but are kept so that each puzzle can be finished by its band’s logic without guessing)
- No duplicate puzzles: **True**; numbered 1..200 in order: **True**

Logic tiers: T1 = basic cell & count rules; T2 = + loop/fragment rules; T3 = + parity (crossing) rule; T4 = + one-step trial

| Band | Grid | Puzzles | Nos. | Band rule | Tier needed (count) | Givens (min-max) | Track cells (min-max) |
|---|---|---|---|---|---|---|---|
| Easy | 6×6 | 50 | 1–50 | solvable ≤T2 | T1: 23, T2: 27 | 2–4 | 16–22 |
| Medium | 8×8 | 50 | 51–100 | solvable ≤T3, not ≤T1 | T2: 39, T3: 11 | 2–6 | 27–38 |
| Hard | 10×10 | 50 | 101–150 | solvable ≤T3, not ≤T2 | T3: 50 | 2–10 | 40–58 |
| Expert | 12×12 | 50 | 151–200 | solvable ≤T4, not ≤T3 | T4: 50 | 3–12 | 58–80 |

## Per-puzzle results

| # | Band | Grid | Solutions | Unique | Tier needed | Givens | Track cells |
|---|---|---|---|---|---|---|---|
| 1 | Easy | 6×6 | 1 | yes | T1 | 4 | 22 |
| 2 | Easy | 6×6 | 1 | yes | T1 | 4 | 22 |
| 3 | Easy | 6×6 | 1 | yes | T1 | 3 | 19 |
| 4 | Easy | 6×6 | 1 | yes | T1 | 3 | 19 |
| 5 | Easy | 6×6 | 1 | yes | T1 | 3 | 21 |
| 6 | Easy | 6×6 | 1 | yes | T1 | 3 | 22 |
| 7 | Easy | 6×6 | 1 | yes | T1 | 3 | 22 |
| 8 | Easy | 6×6 | 1 | yes | T1 | 2 | 16 |
| 9 | Easy | 6×6 | 1 | yes | T1 | 2 | 16 |
| 10 | Easy | 6×6 | 1 | yes | T1 | 2 | 17 |
| 11 | Easy | 6×6 | 1 | yes | T1 | 2 | 17 |
| 12 | Easy | 6×6 | 1 | yes | T1 | 2 | 18 |
| 13 | Easy | 6×6 | 1 | yes | T1 | 2 | 18 |
| 14 | Easy | 6×6 | 1 | yes | T1 | 2 | 18 |
| 15 | Easy | 6×6 | 1 | yes | T1 | 2 | 19 |
| 16 | Easy | 6×6 | 1 | yes | T1 | 2 | 19 |
| 17 | Easy | 6×6 | 1 | yes | T1 | 2 | 19 |
| 18 | Easy | 6×6 | 1 | yes | T1 | 2 | 21 |
| 19 | Easy | 6×6 | 1 | yes | T1 | 2 | 21 |
| 20 | Easy | 6×6 | 1 | yes | T1 | 2 | 21 |
| 21 | Easy | 6×6 | 1 | yes | T1 | 2 | 22 |
| 22 | Easy | 6×6 | 1 | yes | T1 | 2 | 22 |
| 23 | Easy | 6×6 | 1 | yes | T1 | 2 | 22 |
| 24 | Easy | 6×6 | 1 | yes | T2 | 3 | 22 |
| 25 | Easy | 6×6 | 1 | yes | T2 | 3 | 22 |
| 26 | Easy | 6×6 | 1 | yes | T2 | 3 | 22 |
| 27 | Easy | 6×6 | 1 | yes | T2 | 3 | 22 |
| 28 | Easy | 6×6 | 1 | yes | T2 | 2 | 16 |
| 29 | Easy | 6×6 | 1 | yes | T2 | 2 | 17 |
| 30 | Easy | 6×6 | 1 | yes | T2 | 2 | 18 |
| 31 | Easy | 6×6 | 1 | yes | T2 | 2 | 18 |
| 32 | Easy | 6×6 | 1 | yes | T2 | 2 | 19 |
| 33 | Easy | 6×6 | 1 | yes | T2 | 2 | 19 |
| 34 | Easy | 6×6 | 1 | yes | T2 | 2 | 19 |
| 35 | Easy | 6×6 | 1 | yes | T2 | 2 | 19 |
| 36 | Easy | 6×6 | 1 | yes | T2 | 2 | 19 |
| 37 | Easy | 6×6 | 1 | yes | T2 | 2 | 20 |
| 38 | Easy | 6×6 | 1 | yes | T2 | 2 | 20 |
| 39 | Easy | 6×6 | 1 | yes | T2 | 2 | 20 |
| 40 | Easy | 6×6 | 1 | yes | T2 | 2 | 21 |
| 41 | Easy | 6×6 | 1 | yes | T2 | 2 | 21 |
| 42 | Easy | 6×6 | 1 | yes | T2 | 2 | 21 |
| 43 | Easy | 6×6 | 1 | yes | T2 | 2 | 21 |
| 44 | Easy | 6×6 | 1 | yes | T2 | 2 | 22 |
| 45 | Easy | 6×6 | 1 | yes | T2 | 2 | 22 |
| 46 | Easy | 6×6 | 1 | yes | T2 | 2 | 22 |
| 47 | Easy | 6×6 | 1 | yes | T2 | 2 | 22 |
| 48 | Easy | 6×6 | 1 | yes | T2 | 2 | 22 |
| 49 | Easy | 6×6 | 1 | yes | T2 | 2 | 22 |
| 50 | Easy | 6×6 | 1 | yes | T2 | 2 | 22 |
| 51 | Medium | 8×8 | 1 | yes | T2 | 6 | 35 |
| 52 | Medium | 8×8 | 1 | yes | T2 | 6 | 36 |
| 53 | Medium | 8×8 | 1 | yes | T2 | 5 | 33 |
| 54 | Medium | 8×8 | 1 | yes | T2 | 5 | 35 |
| 55 | Medium | 8×8 | 1 | yes | T2 | 5 | 37 |
| 56 | Medium | 8×8 | 1 | yes | T2 | 4 | 27 |
| 57 | Medium | 8×8 | 1 | yes | T2 | 4 | 28 |
| 58 | Medium | 8×8 | 1 | yes | T2 | 4 | 29 |
| 59 | Medium | 8×8 | 1 | yes | T2 | 4 | 30 |
| 60 | Medium | 8×8 | 1 | yes | T2 | 4 | 32 |
| 61 | Medium | 8×8 | 1 | yes | T2 | 4 | 32 |
| 62 | Medium | 8×8 | 1 | yes | T2 | 4 | 33 |
| 63 | Medium | 8×8 | 1 | yes | T2 | 4 | 34 |
| 64 | Medium | 8×8 | 1 | yes | T2 | 4 | 35 |
| 65 | Medium | 8×8 | 1 | yes | T2 | 4 | 37 |
| 66 | Medium | 8×8 | 1 | yes | T2 | 4 | 37 |
| 67 | Medium | 8×8 | 1 | yes | T2 | 4 | 38 |
| 68 | Medium | 8×8 | 1 | yes | T2 | 4 | 38 |
| 69 | Medium | 8×8 | 1 | yes | T2 | 3 | 27 |
| 70 | Medium | 8×8 | 1 | yes | T2 | 3 | 30 |
| 71 | Medium | 8×8 | 1 | yes | T2 | 3 | 31 |
| 72 | Medium | 8×8 | 1 | yes | T2 | 3 | 32 |
| 73 | Medium | 8×8 | 1 | yes | T2 | 3 | 32 |
| 74 | Medium | 8×8 | 1 | yes | T2 | 3 | 32 |
| 75 | Medium | 8×8 | 1 | yes | T2 | 3 | 33 |
| 76 | Medium | 8×8 | 1 | yes | T2 | 3 | 33 |
| 77 | Medium | 8×8 | 1 | yes | T2 | 3 | 33 |
| 78 | Medium | 8×8 | 1 | yes | T2 | 3 | 33 |
| 79 | Medium | 8×8 | 1 | yes | T2 | 3 | 35 |
| 80 | Medium | 8×8 | 1 | yes | T2 | 3 | 37 |
| 81 | Medium | 8×8 | 1 | yes | T2 | 3 | 37 |
| 82 | Medium | 8×8 | 1 | yes | T2 | 2 | 27 |
| 83 | Medium | 8×8 | 1 | yes | T2 | 2 | 28 |
| 84 | Medium | 8×8 | 1 | yes | T2 | 2 | 28 |
| 85 | Medium | 8×8 | 1 | yes | T2 | 2 | 29 |
| 86 | Medium | 8×8 | 1 | yes | T2 | 2 | 29 |
| 87 | Medium | 8×8 | 1 | yes | T2 | 2 | 32 |
| 88 | Medium | 8×8 | 1 | yes | T2 | 2 | 33 |
| 89 | Medium | 8×8 | 1 | yes | T2 | 2 | 35 |
| 90 | Medium | 8×8 | 1 | yes | T3 | 5 | 32 |
| 91 | Medium | 8×8 | 1 | yes | T3 | 5 | 33 |
| 92 | Medium | 8×8 | 1 | yes | T3 | 4 | 29 |
| 93 | Medium | 8×8 | 1 | yes | T3 | 4 | 30 |
| 94 | Medium | 8×8 | 1 | yes | T3 | 4 | 32 |
| 95 | Medium | 8×8 | 1 | yes | T3 | 4 | 34 |
| 96 | Medium | 8×8 | 1 | yes | T3 | 3 | 29 |
| 97 | Medium | 8×8 | 1 | yes | T3 | 2 | 27 |
| 98 | Medium | 8×8 | 1 | yes | T3 | 2 | 28 |
| 99 | Medium | 8×8 | 1 | yes | T3 | 2 | 30 |
| 100 | Medium | 8×8 | 1 | yes | T3 | 2 | 34 |
| 101 | Hard | 10×10 | 1 | yes | T3 | 10 | 48 |
| 102 | Hard | 10×10 | 1 | yes | T3 | 10 | 53 |
| 103 | Hard | 10×10 | 1 | yes | T3 | 10 | 56 |
| 104 | Hard | 10×10 | 1 | yes | T3 | 10 | 57 |
| 105 | Hard | 10×10 | 1 | yes | T3 | 9 | 47 |
| 106 | Hard | 10×10 | 1 | yes | T3 | 9 | 48 |
| 107 | Hard | 10×10 | 1 | yes | T3 | 9 | 48 |
| 108 | Hard | 10×10 | 1 | yes | T3 | 9 | 52 |
| 109 | Hard | 10×10 | 1 | yes | T3 | 9 | 53 |
| 110 | Hard | 10×10 | 1 | yes | T3 | 9 | 57 |
| 111 | Hard | 10×10 | 1 | yes | T3 | 8 | 41 |
| 112 | Hard | 10×10 | 1 | yes | T3 | 8 | 45 |
| 113 | Hard | 10×10 | 1 | yes | T3 | 8 | 47 |
| 114 | Hard | 10×10 | 1 | yes | T3 | 8 | 50 |
| 115 | Hard | 10×10 | 1 | yes | T3 | 8 | 50 |
| 116 | Hard | 10×10 | 1 | yes | T3 | 8 | 51 |
| 117 | Hard | 10×10 | 1 | yes | T3 | 8 | 52 |
| 118 | Hard | 10×10 | 1 | yes | T3 | 8 | 53 |
| 119 | Hard | 10×10 | 1 | yes | T3 | 8 | 54 |
| 120 | Hard | 10×10 | 1 | yes | T3 | 8 | 58 |
| 121 | Hard | 10×10 | 1 | yes | T3 | 7 | 42 |
| 122 | Hard | 10×10 | 1 | yes | T3 | 7 | 45 |
| 123 | Hard | 10×10 | 1 | yes | T3 | 7 | 46 |
| 124 | Hard | 10×10 | 1 | yes | T3 | 7 | 47 |
| 125 | Hard | 10×10 | 1 | yes | T3 | 7 | 47 |
| 126 | Hard | 10×10 | 1 | yes | T3 | 7 | 48 |
| 127 | Hard | 10×10 | 1 | yes | T3 | 7 | 51 |
| 128 | Hard | 10×10 | 1 | yes | T3 | 7 | 53 |
| 129 | Hard | 10×10 | 1 | yes | T3 | 7 | 56 |
| 130 | Hard | 10×10 | 1 | yes | T3 | 6 | 40 |
| 131 | Hard | 10×10 | 1 | yes | T3 | 6 | 42 |
| 132 | Hard | 10×10 | 1 | yes | T3 | 6 | 44 |
| 133 | Hard | 10×10 | 1 | yes | T3 | 6 | 44 |
| 134 | Hard | 10×10 | 1 | yes | T3 | 6 | 46 |
| 135 | Hard | 10×10 | 1 | yes | T3 | 6 | 48 |
| 136 | Hard | 10×10 | 1 | yes | T3 | 6 | 48 |
| 137 | Hard | 10×10 | 1 | yes | T3 | 6 | 50 |
| 138 | Hard | 10×10 | 1 | yes | T3 | 6 | 54 |
| 139 | Hard | 10×10 | 1 | yes | T3 | 6 | 58 |
| 140 | Hard | 10×10 | 1 | yes | T3 | 5 | 41 |
| 141 | Hard | 10×10 | 1 | yes | T3 | 5 | 41 |
| 142 | Hard | 10×10 | 1 | yes | T3 | 5 | 42 |
| 143 | Hard | 10×10 | 1 | yes | T3 | 5 | 43 |
| 144 | Hard | 10×10 | 1 | yes | T3 | 5 | 48 |
| 145 | Hard | 10×10 | 1 | yes | T3 | 5 | 48 |
| 146 | Hard | 10×10 | 1 | yes | T3 | 4 | 41 |
| 147 | Hard | 10×10 | 1 | yes | T3 | 4 | 46 |
| 148 | Hard | 10×10 | 1 | yes | T3 | 4 | 48 |
| 149 | Hard | 10×10 | 1 | yes | T3 | 3 | 46 |
| 150 | Hard | 10×10 | 1 | yes | T3 | 2 | 57 |
| 151 | Expert | 12×12 | 1 | yes | T4 | 12 | 77 |
| 152 | Expert | 12×12 | 1 | yes | T4 | 11 | 74 |
| 153 | Expert | 12×12 | 1 | yes | T4 | 10 | 77 |
| 154 | Expert | 12×12 | 1 | yes | T4 | 10 | 79 |
| 155 | Expert | 12×12 | 1 | yes | T4 | 9 | 69 |
| 156 | Expert | 12×12 | 1 | yes | T4 | 9 | 75 |
| 157 | Expert | 12×12 | 1 | yes | T4 | 9 | 76 |
| 158 | Expert | 12×12 | 1 | yes | T4 | 9 | 71 |
| 159 | Expert | 12×12 | 1 | yes | T4 | 8 | 59 |
| 160 | Expert | 12×12 | 1 | yes | T4 | 8 | 71 |
| 161 | Expert | 12×12 | 1 | yes | T4 | 8 | 76 |
| 162 | Expert | 12×12 | 1 | yes | T4 | 8 | 75 |
| 163 | Expert | 12×12 | 1 | yes | T4 | 8 | 71 |
| 164 | Expert | 12×12 | 1 | yes | T4 | 8 | 78 |
| 165 | Expert | 12×12 | 1 | yes | T4 | 7 | 78 |
| 166 | Expert | 12×12 | 1 | yes | T4 | 7 | 80 |
| 167 | Expert | 12×12 | 1 | yes | T4 | 7 | 62 |
| 168 | Expert | 12×12 | 1 | yes | T4 | 7 | 64 |
| 169 | Expert | 12×12 | 1 | yes | T4 | 7 | 66 |
| 170 | Expert | 12×12 | 1 | yes | T4 | 7 | 66 |
| 171 | Expert | 12×12 | 1 | yes | T4 | 7 | 70 |
| 172 | Expert | 12×12 | 1 | yes | T4 | 7 | 71 |
| 173 | Expert | 12×12 | 1 | yes | T4 | 6 | 66 |
| 174 | Expert | 12×12 | 1 | yes | T4 | 6 | 71 |
| 175 | Expert | 12×12 | 1 | yes | T4 | 6 | 64 |
| 176 | Expert | 12×12 | 1 | yes | T4 | 6 | 72 |
| 177 | Expert | 12×12 | 1 | yes | T4 | 6 | 76 |
| 178 | Expert | 12×12 | 1 | yes | T4 | 6 | 68 |
| 179 | Expert | 12×12 | 1 | yes | T4 | 6 | 67 |
| 180 | Expert | 12×12 | 1 | yes | T4 | 5 | 73 |
| 181 | Expert | 12×12 | 1 | yes | T4 | 5 | 58 |
| 182 | Expert | 12×12 | 1 | yes | T4 | 5 | 76 |
| 183 | Expert | 12×12 | 1 | yes | T4 | 5 | 67 |
| 184 | Expert | 12×12 | 1 | yes | T4 | 5 | 66 |
| 185 | Expert | 12×12 | 1 | yes | T4 | 5 | 64 |
| 186 | Expert | 12×12 | 1 | yes | T4 | 5 | 66 |
| 187 | Expert | 12×12 | 1 | yes | T4 | 5 | 69 |
| 188 | Expert | 12×12 | 1 | yes | T4 | 5 | 63 |
| 189 | Expert | 12×12 | 1 | yes | T4 | 5 | 63 |
| 190 | Expert | 12×12 | 1 | yes | T4 | 5 | 67 |
| 191 | Expert | 12×12 | 1 | yes | T4 | 4 | 63 |
| 192 | Expert | 12×12 | 1 | yes | T4 | 4 | 58 |
| 193 | Expert | 12×12 | 1 | yes | T4 | 4 | 61 |
| 194 | Expert | 12×12 | 1 | yes | T4 | 4 | 59 |
| 195 | Expert | 12×12 | 1 | yes | T4 | 4 | 65 |
| 196 | Expert | 12×12 | 1 | yes | T4 | 4 | 66 |
| 197 | Expert | 12×12 | 1 | yes | T4 | 3 | 58 |
| 198 | Expert | 12×12 | 1 | yes | T4 | 3 | 58 |
| 199 | Expert | 12×12 | 1 | yes | T4 | 3 | 62 |
| 200 | Expert | 12×12 | 1 | yes | T4 | 3 | 59 |
