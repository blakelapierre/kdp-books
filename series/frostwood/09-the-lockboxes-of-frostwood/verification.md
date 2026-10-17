# Verification: The Lockboxes of Frostwood

Seed `20261017`, `PYTHONHASHSEED=0`. Rebuild with `cd src && PYTHONHASHSEED=0 python3 master.py`; the generator output is byte-identical between runs.

## What is checked

- **Generator** (`lockgen.py`): builds each puzzle against the full code space (every code of distinct digits) and keeps only clue sets with exactly one surviving code, then drops every clue it can.
- **Independent solver** (`solver.py`): a depth-first search with partial-code pruning that never enumerates the code space and scores guesses with set arithmetic. It must find exactly one code, equal to the answer.
- **Second exhaustive check** (`verify.py`): re-tests every code of distinct digits with the solver's scoring rule. Exactly one may pass.
- **No repeats**: every answer code and every location is used once in the book.
- **Every clue is needed**: removing any single clue leaves more than one code.
- **Difficulty band**: digit count, clue count, the 'nothing is right' rule, and the solver's search effort (nodes visited) must all sit inside the band.

| Band | Puzzles | Digits | Clues | 'Nothing is right' clue | Solver nodes |
|---|---|---|---|---|---|
| Easy | 30 | 3 | 4–5 | exactly one | 1–18 |
| Medium | 35 | 3 | 5–6 | none | 19–40 |
| Hard | 35 | 4 | 5–7 | at most one | 41–90 |
| Expert | 20 | 5 | 7–9 | none | 91–∞ |

## Result: **120 / 120 PASS**

| No. | Band | Digits | Clues | Nothing clues | Solver nodes | DFS solutions | Exhaustive solutions | Every clue needed | Result |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Easy | 3 | 4 | 1 | 16 | 1 | 1 | yes | PASS |
| 2 | Easy | 3 | 4 | 1 | 10 | 1 | 1 | yes | PASS |
| 3 | Easy | 3 | 4 | 1 | 12 | 1 | 1 | yes | PASS |
| 4 | Easy | 3 | 4 | 1 | 18 | 1 | 1 | yes | PASS |
| 5 | Easy | 3 | 4 | 1 | 14 | 1 | 1 | yes | PASS |
| 6 | Easy | 3 | 4 | 1 | 12 | 1 | 1 | yes | PASS |
| 7 | Easy | 3 | 4 | 1 | 17 | 1 | 1 | yes | PASS |
| 8 | Easy | 3 | 4 | 1 | 17 | 1 | 1 | yes | PASS |
| 9 | Easy | 3 | 5 | 1 | 12 | 1 | 1 | yes | PASS |
| 10 | Easy | 3 | 4 | 1 | 8 | 1 | 1 | yes | PASS |
| 11 | Easy | 3 | 5 | 1 | 14 | 1 | 1 | yes | PASS |
| 12 | Easy | 3 | 4 | 1 | 14 | 1 | 1 | yes | PASS |
| 13 | Easy | 3 | 5 | 1 | 11 | 1 | 1 | yes | PASS |
| 14 | Easy | 3 | 4 | 1 | 15 | 1 | 1 | yes | PASS |
| 15 | Easy | 3 | 5 | 1 | 15 | 1 | 1 | yes | PASS |
| 16 | Easy | 3 | 5 | 1 | 17 | 1 | 1 | yes | PASS |
| 17 | Easy | 3 | 5 | 1 | 10 | 1 | 1 | yes | PASS |
| 18 | Easy | 3 | 4 | 1 | 15 | 1 | 1 | yes | PASS |
| 19 | Easy | 3 | 5 | 1 | 10 | 1 | 1 | yes | PASS |
| 20 | Easy | 3 | 4 | 1 | 15 | 1 | 1 | yes | PASS |
| 21 | Easy | 3 | 4 | 1 | 11 | 1 | 1 | yes | PASS |
| 22 | Easy | 3 | 4 | 1 | 18 | 1 | 1 | yes | PASS |
| 23 | Easy | 3 | 5 | 1 | 14 | 1 | 1 | yes | PASS |
| 24 | Easy | 3 | 5 | 1 | 16 | 1 | 1 | yes | PASS |
| 25 | Easy | 3 | 4 | 1 | 17 | 1 | 1 | yes | PASS |
| 26 | Easy | 3 | 4 | 1 | 12 | 1 | 1 | yes | PASS |
| 27 | Easy | 3 | 5 | 1 | 12 | 1 | 1 | yes | PASS |
| 28 | Easy | 3 | 4 | 1 | 12 | 1 | 1 | yes | PASS |
| 29 | Easy | 3 | 4 | 1 | 12 | 1 | 1 | yes | PASS |
| 30 | Easy | 3 | 4 | 1 | 15 | 1 | 1 | yes | PASS |
| 31 | Medium | 3 | 5 | 0 | 24 | 1 | 1 | yes | PASS |
| 32 | Medium | 3 | 5 | 0 | 27 | 1 | 1 | yes | PASS |
| 33 | Medium | 3 | 6 | 0 | 24 | 1 | 1 | yes | PASS |
| 34 | Medium | 3 | 5 | 0 | 21 | 1 | 1 | yes | PASS |
| 35 | Medium | 3 | 5 | 0 | 23 | 1 | 1 | yes | PASS |
| 36 | Medium | 3 | 5 | 0 | 21 | 1 | 1 | yes | PASS |
| 37 | Medium | 3 | 5 | 0 | 19 | 1 | 1 | yes | PASS |
| 38 | Medium | 3 | 5 | 0 | 27 | 1 | 1 | yes | PASS |
| 39 | Medium | 3 | 5 | 0 | 20 | 1 | 1 | yes | PASS |
| 40 | Medium | 3 | 5 | 0 | 25 | 1 | 1 | yes | PASS |
| 41 | Medium | 3 | 6 | 0 | 20 | 1 | 1 | yes | PASS |
| 42 | Medium | 3 | 5 | 0 | 38 | 1 | 1 | yes | PASS |
| 43 | Medium | 3 | 5 | 0 | 19 | 1 | 1 | yes | PASS |
| 44 | Medium | 3 | 5 | 0 | 21 | 1 | 1 | yes | PASS |
| 45 | Medium | 3 | 5 | 0 | 19 | 1 | 1 | yes | PASS |
| 46 | Medium | 3 | 5 | 0 | 26 | 1 | 1 | yes | PASS |
| 47 | Medium | 3 | 5 | 0 | 23 | 1 | 1 | yes | PASS |
| 48 | Medium | 3 | 5 | 0 | 23 | 1 | 1 | yes | PASS |
| 49 | Medium | 3 | 5 | 0 | 19 | 1 | 1 | yes | PASS |
| 50 | Medium | 3 | 5 | 0 | 26 | 1 | 1 | yes | PASS |
| 51 | Medium | 3 | 5 | 0 | 20 | 1 | 1 | yes | PASS |
| 52 | Medium | 3 | 5 | 0 | 20 | 1 | 1 | yes | PASS |
| 53 | Medium | 3 | 5 | 0 | 25 | 1 | 1 | yes | PASS |
| 54 | Medium | 3 | 5 | 0 | 35 | 1 | 1 | yes | PASS |
| 55 | Medium | 3 | 5 | 0 | 27 | 1 | 1 | yes | PASS |
| 56 | Medium | 3 | 5 | 0 | 21 | 1 | 1 | yes | PASS |
| 57 | Medium | 3 | 5 | 0 | 20 | 1 | 1 | yes | PASS |
| 58 | Medium | 3 | 5 | 0 | 20 | 1 | 1 | yes | PASS |
| 59 | Medium | 3 | 5 | 0 | 21 | 1 | 1 | yes | PASS |
| 60 | Medium | 3 | 5 | 0 | 22 | 1 | 1 | yes | PASS |
| 61 | Medium | 3 | 5 | 0 | 22 | 1 | 1 | yes | PASS |
| 62 | Medium | 3 | 5 | 0 | 20 | 1 | 1 | yes | PASS |
| 63 | Medium | 3 | 6 | 0 | 28 | 1 | 1 | yes | PASS |
| 64 | Medium | 3 | 6 | 0 | 25 | 1 | 1 | yes | PASS |
| 65 | Medium | 3 | 5 | 0 | 24 | 1 | 1 | yes | PASS |
| 66 | Hard | 4 | 5 | 0 | 47 | 1 | 1 | yes | PASS |
| 67 | Hard | 4 | 5 | 0 | 57 | 1 | 1 | yes | PASS |
| 68 | Hard | 4 | 6 | 0 | 47 | 1 | 1 | yes | PASS |
| 69 | Hard | 4 | 5 | 0 | 60 | 1 | 1 | yes | PASS |
| 70 | Hard | 4 | 5 | 0 | 57 | 1 | 1 | yes | PASS |
| 71 | Hard | 4 | 5 | 0 | 42 | 1 | 1 | yes | PASS |
| 72 | Hard | 4 | 6 | 0 | 78 | 1 | 1 | yes | PASS |
| 73 | Hard | 4 | 5 | 0 | 72 | 1 | 1 | yes | PASS |
| 74 | Hard | 4 | 6 | 0 | 51 | 1 | 1 | yes | PASS |
| 75 | Hard | 4 | 5 | 0 | 46 | 1 | 1 | yes | PASS |
| 76 | Hard | 4 | 6 | 0 | 60 | 1 | 1 | yes | PASS |
| 77 | Hard | 4 | 5 | 0 | 81 | 1 | 1 | yes | PASS |
| 78 | Hard | 4 | 5 | 0 | 80 | 1 | 1 | yes | PASS |
| 79 | Hard | 4 | 5 | 0 | 67 | 1 | 1 | yes | PASS |
| 80 | Hard | 4 | 5 | 0 | 54 | 1 | 1 | yes | PASS |
| 81 | Hard | 4 | 6 | 0 | 42 | 1 | 1 | yes | PASS |
| 82 | Hard | 4 | 5 | 0 | 43 | 1 | 1 | yes | PASS |
| 83 | Hard | 4 | 5 | 0 | 59 | 1 | 1 | yes | PASS |
| 84 | Hard | 4 | 5 | 0 | 45 | 1 | 1 | yes | PASS |
| 85 | Hard | 4 | 5 | 0 | 83 | 1 | 1 | yes | PASS |
| 86 | Hard | 4 | 7 | 0 | 41 | 1 | 1 | yes | PASS |
| 87 | Hard | 4 | 5 | 0 | 55 | 1 | 1 | yes | PASS |
| 88 | Hard | 4 | 6 | 0 | 61 | 1 | 1 | yes | PASS |
| 89 | Hard | 4 | 5 | 0 | 47 | 1 | 1 | yes | PASS |
| 90 | Hard | 4 | 5 | 0 | 61 | 1 | 1 | yes | PASS |
| 91 | Hard | 4 | 6 | 0 | 58 | 1 | 1 | yes | PASS |
| 92 | Hard | 4 | 6 | 0 | 72 | 1 | 1 | yes | PASS |
| 93 | Hard | 4 | 6 | 0 | 52 | 1 | 1 | yes | PASS |
| 94 | Hard | 4 | 6 | 0 | 63 | 1 | 1 | yes | PASS |
| 95 | Hard | 4 | 5 | 0 | 70 | 1 | 1 | yes | PASS |
| 96 | Hard | 4 | 6 | 0 | 50 | 1 | 1 | yes | PASS |
| 97 | Hard | 4 | 5 | 0 | 49 | 1 | 1 | yes | PASS |
| 98 | Hard | 4 | 5 | 0 | 60 | 1 | 1 | yes | PASS |
| 99 | Hard | 4 | 5 | 0 | 68 | 1 | 1 | yes | PASS |
| 100 | Hard | 4 | 6 | 0 | 53 | 1 | 1 | yes | PASS |
| 101 | Expert | 5 | 7 | 0 | 165 | 1 | 1 | yes | PASS |
| 102 | Expert | 5 | 7 | 0 | 120 | 1 | 1 | yes | PASS |
| 103 | Expert | 5 | 7 | 0 | 270 | 1 | 1 | yes | PASS |
| 104 | Expert | 5 | 7 | 0 | 114 | 1 | 1 | yes | PASS |
| 105 | Expert | 5 | 7 | 0 | 153 | 1 | 1 | yes | PASS |
| 106 | Expert | 5 | 7 | 0 | 186 | 1 | 1 | yes | PASS |
| 107 | Expert | 5 | 7 | 0 | 156 | 1 | 1 | yes | PASS |
| 108 | Expert | 5 | 7 | 0 | 105 | 1 | 1 | yes | PASS |
| 109 | Expert | 5 | 7 | 0 | 124 | 1 | 1 | yes | PASS |
| 110 | Expert | 5 | 7 | 0 | 103 | 1 | 1 | yes | PASS |
| 111 | Expert | 5 | 7 | 0 | 190 | 1 | 1 | yes | PASS |
| 112 | Expert | 5 | 7 | 0 | 91 | 1 | 1 | yes | PASS |
| 113 | Expert | 5 | 7 | 0 | 149 | 1 | 1 | yes | PASS |
| 114 | Expert | 5 | 7 | 0 | 137 | 1 | 1 | yes | PASS |
| 115 | Expert | 5 | 7 | 0 | 109 | 1 | 1 | yes | PASS |
| 116 | Expert | 5 | 7 | 0 | 151 | 1 | 1 | yes | PASS |
| 117 | Expert | 5 | 7 | 0 | 118 | 1 | 1 | yes | PASS |
| 118 | Expert | 5 | 7 | 0 | 137 | 1 | 1 | yes | PASS |
| 119 | Expert | 5 | 7 | 0 | 148 | 1 | 1 | yes | PASS |
| 120 | Expert | 5 | 7 | 0 | 193 | 1 | 1 | yes | PASS |
