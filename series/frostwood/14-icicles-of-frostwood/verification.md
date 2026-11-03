# Verification report: The Icicles of Frostwood

Generated 2026-11-03 10:21 PST by `src/verify.py` in 316.2 s.

- Puzzles checked: **160** (+ the worked example: unique, solvable with the basic rules alone)
- Well formed and the stored solution obeys every rule (each row and column holds every length once, every given number, every sign): **160/160**
- Exactly one solution (SAT solver CaDiCaL via python-sat), equal to the stored solution: **160/160**
- Independent backtracking counter (`fut_bt.py`, no SAT, no shared code) finds exactly one solution, the same one: **160/160**
- Meet their difficulty band (grid size, logic tier needed, number of what-if steps): **160/160**
- Counter cross-check on mutated copies (one clue removed, one sign flipped): SAT and backtracking agree in **160/160** cases (mutations gave 0 solutions: 4, exactly 1: 4, 2+: 152)
- No duplicate puzzles: **True**; numbered 1..160 in order: **True**

Logic tiers (the generator's own step-by-step solver, `futoshiki.py`): T1 = basic rules (a length used once per row and column, the only square left for a length, and pushing limits across each sign); T2 = + pairs and triples of squares that share the same two or three lengths, hidden pairs, and chains of signs; T3 = + one-step trial (what if?).

| Band | Grid | Puzzles | Nos. | Band rule | Given numbers | Signs | What-if steps (range) |
|---|---|---|---|---|---|---|---|
| Easy | 5×5 | 40 | 1–40 | basic rules only (T1) | 0–2 | 6–14 | 0–0 |
| Medium | 6×6 | 40 | 41–80 | needs exactly T2 | 0–4 | 12–21 | 0–0 |
| Hard | 7×7 | 40 | 81–120 | needs T3 | 0–5 | 15–31 | 1–3 |
| Expert | 8×8 | 40 | 121–160 | needs T3, more what-ifs | 0–8 | 25–47 | 5–12 |

## Per-puzzle results

| # | Band | Grid | Numbers | Signs | SAT solutions | Unique | Backtracking agrees | Tier | What-if steps |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Easy | 5×5 | 0 | 14 | 1 | yes | yes | T1 | 0 |
| 2 | Easy | 5×5 | 2 | 11 | 1 | yes | yes | T1 | 0 |
| 3 | Easy | 5×5 | 1 | 11 | 1 | yes | yes | T1 | 0 |
| 4 | Easy | 5×5 | 1 | 11 | 1 | yes | yes | T1 | 0 |
| 5 | Easy | 5×5 | 0 | 12 | 1 | yes | yes | T1 | 0 |
| 6 | Easy | 5×5 | 0 | 12 | 1 | yes | yes | T1 | 0 |
| 7 | Easy | 5×5 | 1 | 11 | 1 | yes | yes | T1 | 0 |
| 8 | Easy | 5×5 | 1 | 11 | 1 | yes | yes | T1 | 0 |
| 9 | Easy | 5×5 | 1 | 11 | 1 | yes | yes | T1 | 0 |
| 10 | Easy | 5×5 | 0 | 11 | 1 | yes | yes | T1 | 0 |
| 11 | Easy | 5×5 | 0 | 11 | 1 | yes | yes | T1 | 0 |
| 12 | Easy | 5×5 | 1 | 10 | 1 | yes | yes | T1 | 0 |
| 13 | Easy | 5×5 | 0 | 11 | 1 | yes | yes | T1 | 0 |
| 14 | Easy | 5×5 | 2 | 9 | 1 | yes | yes | T1 | 0 |
| 15 | Easy | 5×5 | 0 | 11 | 1 | yes | yes | T1 | 0 |
| 16 | Easy | 5×5 | 1 | 9 | 1 | yes | yes | T1 | 0 |
| 17 | Easy | 5×5 | 2 | 8 | 1 | yes | yes | T1 | 0 |
| 18 | Easy | 5×5 | 2 | 8 | 1 | yes | yes | T1 | 0 |
| 19 | Easy | 5×5 | 1 | 9 | 1 | yes | yes | T1 | 0 |
| 20 | Easy | 5×5 | 2 | 8 | 1 | yes | yes | T1 | 0 |
| 21 | Easy | 5×5 | 0 | 10 | 1 | yes | yes | T1 | 0 |
| 22 | Easy | 5×5 | 0 | 10 | 1 | yes | yes | T1 | 0 |
| 23 | Easy | 5×5 | 1 | 9 | 1 | yes | yes | T1 | 0 |
| 24 | Easy | 5×5 | 0 | 10 | 1 | yes | yes | T1 | 0 |
| 25 | Easy | 5×5 | 0 | 10 | 1 | yes | yes | T1 | 0 |
| 26 | Easy | 5×5 | 0 | 9 | 1 | yes | yes | T1 | 0 |
| 27 | Easy | 5×5 | 0 | 9 | 1 | yes | yes | T1 | 0 |
| 28 | Easy | 5×5 | 1 | 8 | 1 | yes | yes | T1 | 0 |
| 29 | Easy | 5×5 | 1 | 8 | 1 | yes | yes | T1 | 0 |
| 30 | Easy | 5×5 | 1 | 8 | 1 | yes | yes | T1 | 0 |
| 31 | Easy | 5×5 | 1 | 8 | 1 | yes | yes | T1 | 0 |
| 32 | Easy | 5×5 | 0 | 9 | 1 | yes | yes | T1 | 0 |
| 33 | Easy | 5×5 | 0 | 9 | 1 | yes | yes | T1 | 0 |
| 34 | Easy | 5×5 | 0 | 9 | 1 | yes | yes | T1 | 0 |
| 35 | Easy | 5×5 | 1 | 8 | 1 | yes | yes | T1 | 0 |
| 36 | Easy | 5×5 | 1 | 7 | 1 | yes | yes | T1 | 0 |
| 37 | Easy | 5×5 | 0 | 8 | 1 | yes | yes | T1 | 0 |
| 38 | Easy | 5×5 | 1 | 7 | 1 | yes | yes | T1 | 0 |
| 39 | Easy | 5×5 | 1 | 6 | 1 | yes | yes | T1 | 0 |
| 40 | Easy | 5×5 | 1 | 6 | 1 | yes | yes | T1 | 0 |
| 41 | Medium | 6×6 | 2 | 18 | 1 | yes | yes | T2 | 0 |
| 42 | Medium | 6×6 | 4 | 12 | 1 | yes | yes | T2 | 0 |
| 43 | Medium | 6×6 | 0 | 18 | 1 | yes | yes | T2 | 0 |
| 44 | Medium | 6×6 | 0 | 16 | 1 | yes | yes | T2 | 0 |
| 45 | Medium | 6×6 | 0 | 18 | 1 | yes | yes | T2 | 0 |
| 46 | Medium | 6×6 | 2 | 13 | 1 | yes | yes | T2 | 0 |
| 47 | Medium | 6×6 | 1 | 20 | 1 | yes | yes | T2 | 0 |
| 48 | Medium | 6×6 | 0 | 18 | 1 | yes | yes | T2 | 0 |
| 49 | Medium | 6×6 | 1 | 17 | 1 | yes | yes | T2 | 0 |
| 50 | Medium | 6×6 | 2 | 15 | 1 | yes | yes | T2 | 0 |
| 51 | Medium | 6×6 | 0 | 16 | 1 | yes | yes | T2 | 0 |
| 52 | Medium | 6×6 | 1 | 15 | 1 | yes | yes | T2 | 0 |
| 53 | Medium | 6×6 | 3 | 12 | 1 | yes | yes | T2 | 0 |
| 54 | Medium | 6×6 | 1 | 14 | 1 | yes | yes | T2 | 0 |
| 55 | Medium | 6×6 | 2 | 13 | 1 | yes | yes | T2 | 0 |
| 56 | Medium | 6×6 | 0 | 20 | 1 | yes | yes | T2 | 0 |
| 57 | Medium | 6×6 | 1 | 16 | 1 | yes | yes | T2 | 0 |
| 58 | Medium | 6×6 | 1 | 14 | 1 | yes | yes | T2 | 0 |
| 59 | Medium | 6×6 | 3 | 12 | 1 | yes | yes | T2 | 0 |
| 60 | Medium | 6×6 | 1 | 18 | 1 | yes | yes | T2 | 0 |
| 61 | Medium | 6×6 | 1 | 17 | 1 | yes | yes | T2 | 0 |
| 62 | Medium | 6×6 | 2 | 15 | 1 | yes | yes | T2 | 0 |
| 63 | Medium | 6×6 | 1 | 15 | 1 | yes | yes | T2 | 0 |
| 64 | Medium | 6×6 | 0 | 16 | 1 | yes | yes | T2 | 0 |
| 65 | Medium | 6×6 | 1 | 14 | 1 | yes | yes | T2 | 0 |
| 66 | Medium | 6×6 | 0 | 19 | 1 | yes | yes | T2 | 0 |
| 67 | Medium | 6×6 | 2 | 14 | 1 | yes | yes | T2 | 0 |
| 68 | Medium | 6×6 | 2 | 14 | 1 | yes | yes | T2 | 0 |
| 69 | Medium | 6×6 | 0 | 16 | 1 | yes | yes | T2 | 0 |
| 70 | Medium | 6×6 | 2 | 13 | 1 | yes | yes | T2 | 0 |
| 71 | Medium | 6×6 | 0 | 14 | 1 | yes | yes | T2 | 0 |
| 72 | Medium | 6×6 | 1 | 12 | 1 | yes | yes | T2 | 0 |
| 73 | Medium | 6×6 | 0 | 21 | 1 | yes | yes | T2 | 0 |
| 74 | Medium | 6×6 | 1 | 15 | 1 | yes | yes | T2 | 0 |
| 75 | Medium | 6×6 | 2 | 12 | 1 | yes | yes | T2 | 0 |
| 76 | Medium | 6×6 | 2 | 15 | 1 | yes | yes | T2 | 0 |
| 77 | Medium | 6×6 | 1 | 17 | 1 | yes | yes | T2 | 0 |
| 78 | Medium | 6×6 | 0 | 16 | 1 | yes | yes | T2 | 0 |
| 79 | Medium | 6×6 | 1 | 16 | 1 | yes | yes | T2 | 0 |
| 80 | Medium | 6×6 | 2 | 14 | 1 | yes | yes | T2 | 0 |
| 81 | Hard | 7×7 | 2 | 21 | 1 | yes | yes | T3 | 1 |
| 82 | Hard | 7×7 | 2 | 21 | 1 | yes | yes | T3 | 1 |
| 83 | Hard | 7×7 | 1 | 24 | 1 | yes | yes | T3 | 1 |
| 84 | Hard | 7×7 | 3 | 22 | 1 | yes | yes | T3 | 1 |
| 85 | Hard | 7×7 | 1 | 27 | 1 | yes | yes | T3 | 2 |
| 86 | Hard | 7×7 | 1 | 24 | 1 | yes | yes | T3 | 2 |
| 87 | Hard | 7×7 | 1 | 24 | 1 | yes | yes | T3 | 2 |
| 88 | Hard | 7×7 | 4 | 18 | 1 | yes | yes | T3 | 2 |
| 89 | Hard | 7×7 | 1 | 31 | 1 | yes | yes | T3 | 2 |
| 90 | Hard | 7×7 | 1 | 23 | 1 | yes | yes | T3 | 2 |
| 91 | Hard | 7×7 | 4 | 19 | 1 | yes | yes | T3 | 2 |
| 92 | Hard | 7×7 | 3 | 18 | 1 | yes | yes | T3 | 2 |
| 93 | Hard | 7×7 | 4 | 27 | 1 | yes | yes | T3 | 3 |
| 94 | Hard | 7×7 | 1 | 29 | 1 | yes | yes | T3 | 3 |
| 95 | Hard | 7×7 | 2 | 26 | 1 | yes | yes | T3 | 3 |
| 96 | Hard | 7×7 | 5 | 21 | 1 | yes | yes | T3 | 3 |
| 97 | Hard | 7×7 | 5 | 19 | 1 | yes | yes | T3 | 3 |
| 98 | Hard | 7×7 | 1 | 21 | 1 | yes | yes | T3 | 3 |
| 99 | Hard | 7×7 | 2 | 27 | 1 | yes | yes | T3 | 3 |
| 100 | Hard | 7×7 | 5 | 21 | 1 | yes | yes | T3 | 3 |
| 101 | Hard | 7×7 | 2 | 24 | 1 | yes | yes | T3 | 3 |
| 102 | Hard | 7×7 | 1 | 25 | 1 | yes | yes | T3 | 3 |
| 103 | Hard | 7×7 | 2 | 23 | 1 | yes | yes | T3 | 3 |
| 104 | Hard | 7×7 | 1 | 22 | 1 | yes | yes | T3 | 3 |
| 105 | Hard | 7×7 | 2 | 20 | 1 | yes | yes | T3 | 3 |
| 106 | Hard | 7×7 | 2 | 27 | 1 | yes | yes | T3 | 3 |
| 107 | Hard | 7×7 | 1 | 25 | 1 | yes | yes | T3 | 3 |
| 108 | Hard | 7×7 | 2 | 23 | 1 | yes | yes | T3 | 3 |
| 109 | Hard | 7×7 | 0 | 26 | 1 | yes | yes | T3 | 3 |
| 110 | Hard | 7×7 | 5 | 15 | 1 | yes | yes | T3 | 3 |
| 111 | Hard | 7×7 | 2 | 23 | 1 | yes | yes | T3 | 3 |
| 112 | Hard | 7×7 | 3 | 18 | 1 | yes | yes | T3 | 3 |
| 113 | Hard | 7×7 | 2 | 21 | 1 | yes | yes | T3 | 3 |
| 114 | Hard | 7×7 | 0 | 21 | 1 | yes | yes | T3 | 3 |
| 115 | Hard | 7×7 | 1 | 27 | 1 | yes | yes | T3 | 3 |
| 116 | Hard | 7×7 | 3 | 23 | 1 | yes | yes | T3 | 3 |
| 117 | Hard | 7×7 | 1 | 24 | 1 | yes | yes | T3 | 3 |
| 118 | Hard | 7×7 | 2 | 27 | 1 | yes | yes | T3 | 3 |
| 119 | Hard | 7×7 | 3 | 20 | 1 | yes | yes | T3 | 3 |
| 120 | Hard | 7×7 | 2 | 21 | 1 | yes | yes | T3 | 3 |
| 121 | Expert | 8×8 | 2 | 36 | 1 | yes | yes | T3 | 5 |
| 122 | Expert | 8×8 | 5 | 26 | 1 | yes | yes | T3 | 5 |
| 123 | Expert | 8×8 | 6 | 29 | 1 | yes | yes | T3 | 7 |
| 124 | Expert | 8×8 | 8 | 27 | 1 | yes | yes | T3 | 8 |
| 125 | Expert | 8×8 | 6 | 28 | 1 | yes | yes | T3 | 9 |
| 126 | Expert | 8×8 | 3 | 33 | 1 | yes | yes | T3 | 9 |
| 127 | Expert | 8×8 | 4 | 33 | 1 | yes | yes | T3 | 10 |
| 128 | Expert | 8×8 | 5 | 32 | 1 | yes | yes | T3 | 10 |
| 129 | Expert | 8×8 | 2 | 35 | 1 | yes | yes | T3 | 10 |
| 130 | Expert | 8×8 | 7 | 25 | 1 | yes | yes | T3 | 10 |
| 131 | Expert | 8×8 | 2 | 43 | 1 | yes | yes | T3 | 11 |
| 132 | Expert | 8×8 | 4 | 33 | 1 | yes | yes | T3 | 11 |
| 133 | Expert | 8×8 | 2 | 38 | 1 | yes | yes | T3 | 11 |
| 134 | Expert | 8×8 | 2 | 42 | 1 | yes | yes | T3 | 11 |
| 135 | Expert | 8×8 | 1 | 38 | 1 | yes | yes | T3 | 11 |
| 136 | Expert | 8×8 | 4 | 30 | 1 | yes | yes | T3 | 11 |
| 137 | Expert | 8×8 | 1 | 38 | 1 | yes | yes | T3 | 11 |
| 138 | Expert | 8×8 | 4 | 33 | 1 | yes | yes | T3 | 11 |
| 139 | Expert | 8×8 | 8 | 29 | 1 | yes | yes | T3 | 11 |
| 140 | Expert | 8×8 | 3 | 32 | 1 | yes | yes | T3 | 11 |
| 141 | Expert | 8×8 | 8 | 29 | 1 | yes | yes | T3 | 12 |
| 142 | Expert | 8×8 | 3 | 44 | 1 | yes | yes | T3 | 12 |
| 143 | Expert | 8×8 | 6 | 33 | 1 | yes | yes | T3 | 12 |
| 144 | Expert | 8×8 | 1 | 47 | 1 | yes | yes | T3 | 12 |
| 145 | Expert | 8×8 | 3 | 40 | 1 | yes | yes | T3 | 12 |
| 146 | Expert | 8×8 | 2 | 38 | 1 | yes | yes | T3 | 12 |
| 147 | Expert | 8×8 | 5 | 32 | 1 | yes | yes | T3 | 12 |
| 148 | Expert | 8×8 | 2 | 40 | 1 | yes | yes | T3 | 12 |
| 149 | Expert | 8×8 | 2 | 41 | 1 | yes | yes | T3 | 12 |
| 150 | Expert | 8×8 | 2 | 40 | 1 | yes | yes | T3 | 12 |
| 151 | Expert | 8×8 | 5 | 36 | 1 | yes | yes | T3 | 12 |
| 152 | Expert | 8×8 | 2 | 44 | 1 | yes | yes | T3 | 12 |
| 153 | Expert | 8×8 | 4 | 41 | 1 | yes | yes | T3 | 12 |
| 154 | Expert | 8×8 | 4 | 36 | 1 | yes | yes | T3 | 12 |
| 155 | Expert | 8×8 | 2 | 42 | 1 | yes | yes | T3 | 12 |
| 156 | Expert | 8×8 | 3 | 32 | 1 | yes | yes | T3 | 12 |
| 157 | Expert | 8×8 | 7 | 33 | 1 | yes | yes | T3 | 12 |
| 158 | Expert | 8×8 | 0 | 38 | 1 | yes | yes | T3 | 12 |
| 159 | Expert | 8×8 | 1 | 38 | 1 | yes | yes | T3 | 12 |
| 160 | Expert | 8×8 | 3 | 38 | 1 | yes | yes | T3 | 12 |

**Result: ALL CHECKS PASSED**
