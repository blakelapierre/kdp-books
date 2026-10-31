# Verification — The Fibbers of Frostwood

Total puzzles: **120** · seed `20261031` · `PYTHONHASHSEED=0`

## Result

**ALL 120 PUZZLES PASSED.**
Each has exactly one consistent assignment of truth-tellers and fibbers (equal to the printed answer), every statement is needed, each fits its band, every hint points the right way, and no puzzle repeats (duplicates: 0).

## Bands

| Band | Puzzles | Players | Statement kinds | Step depth | Hypotheses | Pass | Fail |
|---|---|---|---|---|---|---|---|
| Easy | 30 | 3 | is, same, diff, both, either | 0 | 0–0 | 30 | 0 |
| Medium | 35 | 4 | is, same, diff, both, either, count, if | 1 | 1–1 | 35 | 0 |
| Hard | 35 | 5 | is, same, diff, both, either, count, if | 1 | 2–3 | 35 | 0 |
| Expert | 20 | 6 | either, count, if, same, diff, both | 2 | 1–4 | 20 | 0 |

**Step depth** is measured by the verifier's own deduction ladder: 0 means the puzzle falls to reading one statement at a time (each statement, with what is already known, pins someone down). 1 means at least one "suppose X is a truth-teller…" test is needed, where the contradiction shows up from single statements. 2 means a supposition inside a supposition is needed. **Hypotheses** is how many such tests the ladder needs in its canonical order (players in book order, truth-teller tried first).

## Statement kinds used

| Kind | Statements |
|---|---|
| both | 50 |
| count | 86 |
| either/or | 62 |
| if-then | 57 |
| is a | 91 |
| same/different kind | 179 |

## Method

- `gen.py` builds random statements from a fixed seed, keeps a puzzle only if its own enumerator finds one world, its own step solver gives the band's depth and hypothesis count, and every statement is needed.
- `verify.py` imports nothing from the generator. It parses the **printed English sentence** of every statement back into a rule with regular expressions, so a wording mistake would show up as a parse failure or a wrong answer. It brute-forces all 2^n worlds with bitmasks, re-checks that each statement is needed, and re-measures difficulty with an independent world-set deduction ladder.

## Every puzzle

| No. | Band | Players | Solutions | Depth | Hypotheses | Fibbers | Result |
|---|---|---|---|---|---|---|---|
| 1 | Easy | 3 | 1 | 0 | 0 | 1 | PASS |
| 2 | Easy | 3 | 1 | 0 | 0 | 0 | PASS |
| 3 | Easy | 3 | 1 | 0 | 0 | 1 | PASS |
| 4 | Easy | 3 | 1 | 0 | 0 | 1 | PASS |
| 5 | Easy | 3 | 1 | 0 | 0 | 0 | PASS |
| 6 | Easy | 3 | 1 | 0 | 0 | 1 | PASS |
| 7 | Easy | 3 | 1 | 0 | 0 | 2 | PASS |
| 8 | Easy | 3 | 1 | 0 | 0 | 3 | PASS |
| 9 | Easy | 3 | 1 | 0 | 0 | 2 | PASS |
| 10 | Easy | 3 | 1 | 0 | 0 | 0 | PASS |
| 11 | Easy | 3 | 1 | 0 | 0 | 1 | PASS |
| 12 | Easy | 3 | 1 | 0 | 0 | 1 | PASS |
| 13 | Easy | 3 | 1 | 0 | 0 | 1 | PASS |
| 14 | Easy | 3 | 1 | 0 | 0 | 2 | PASS |
| 15 | Easy | 3 | 1 | 0 | 0 | 1 | PASS |
| 16 | Easy | 3 | 1 | 0 | 0 | 2 | PASS |
| 17 | Easy | 3 | 1 | 0 | 0 | 2 | PASS |
| 18 | Easy | 3 | 1 | 0 | 0 | 0 | PASS |
| 19 | Easy | 3 | 1 | 0 | 0 | 2 | PASS |
| 20 | Easy | 3 | 1 | 0 | 0 | 2 | PASS |
| 21 | Easy | 3 | 1 | 0 | 0 | 2 | PASS |
| 22 | Easy | 3 | 1 | 0 | 0 | 2 | PASS |
| 23 | Easy | 3 | 1 | 0 | 0 | 2 | PASS |
| 24 | Easy | 3 | 1 | 0 | 0 | 2 | PASS |
| 25 | Easy | 3 | 1 | 0 | 0 | 1 | PASS |
| 26 | Easy | 3 | 1 | 0 | 0 | 1 | PASS |
| 27 | Easy | 3 | 1 | 0 | 0 | 2 | PASS |
| 28 | Easy | 3 | 1 | 0 | 0 | 3 | PASS |
| 29 | Easy | 3 | 1 | 0 | 0 | 1 | PASS |
| 30 | Easy | 3 | 1 | 0 | 0 | 1 | PASS |
| 31 | Medium | 4 | 1 | 1 | 1 | 3 | PASS |
| 32 | Medium | 4 | 1 | 1 | 1 | 3 | PASS |
| 33 | Medium | 4 | 1 | 1 | 1 | 3 | PASS |
| 34 | Medium | 4 | 1 | 1 | 1 | 2 | PASS |
| 35 | Medium | 4 | 1 | 1 | 1 | 3 | PASS |
| 36 | Medium | 4 | 1 | 1 | 1 | 2 | PASS |
| 37 | Medium | 4 | 1 | 1 | 1 | 4 | PASS |
| 38 | Medium | 4 | 1 | 1 | 1 | 1 | PASS |
| 39 | Medium | 4 | 1 | 1 | 1 | 2 | PASS |
| 40 | Medium | 4 | 1 | 1 | 1 | 2 | PASS |
| 41 | Medium | 4 | 1 | 1 | 1 | 3 | PASS |
| 42 | Medium | 4 | 1 | 1 | 1 | 1 | PASS |
| 43 | Medium | 4 | 1 | 1 | 1 | 2 | PASS |
| 44 | Medium | 4 | 1 | 1 | 1 | 2 | PASS |
| 45 | Medium | 4 | 1 | 1 | 1 | 3 | PASS |
| 46 | Medium | 4 | 1 | 1 | 1 | 2 | PASS |
| 47 | Medium | 4 | 1 | 1 | 1 | 1 | PASS |
| 48 | Medium | 4 | 1 | 1 | 1 | 2 | PASS |
| 49 | Medium | 4 | 1 | 1 | 1 | 2 | PASS |
| 50 | Medium | 4 | 1 | 1 | 1 | 1 | PASS |
| 51 | Medium | 4 | 1 | 1 | 1 | 1 | PASS |
| 52 | Medium | 4 | 1 | 1 | 1 | 2 | PASS |
| 53 | Medium | 4 | 1 | 1 | 1 | 2 | PASS |
| 54 | Medium | 4 | 1 | 1 | 1 | 2 | PASS |
| 55 | Medium | 4 | 1 | 1 | 1 | 3 | PASS |
| 56 | Medium | 4 | 1 | 1 | 1 | 3 | PASS |
| 57 | Medium | 4 | 1 | 1 | 1 | 3 | PASS |
| 58 | Medium | 4 | 1 | 1 | 1 | 1 | PASS |
| 59 | Medium | 4 | 1 | 1 | 1 | 2 | PASS |
| 60 | Medium | 4 | 1 | 1 | 1 | 1 | PASS |
| 61 | Medium | 4 | 1 | 1 | 1 | 3 | PASS |
| 62 | Medium | 4 | 1 | 1 | 1 | 2 | PASS |
| 63 | Medium | 4 | 1 | 1 | 1 | 4 | PASS |
| 64 | Medium | 4 | 1 | 1 | 1 | 2 | PASS |
| 65 | Medium | 4 | 1 | 1 | 1 | 1 | PASS |
| 66 | Hard | 5 | 1 | 1 | 2 | 4 | PASS |
| 67 | Hard | 5 | 1 | 1 | 3 | 5 | PASS |
| 68 | Hard | 5 | 1 | 1 | 2 | 3 | PASS |
| 69 | Hard | 5 | 1 | 1 | 2 | 2 | PASS |
| 70 | Hard | 5 | 1 | 1 | 2 | 4 | PASS |
| 71 | Hard | 5 | 1 | 1 | 2 | 5 | PASS |
| 72 | Hard | 5 | 1 | 1 | 2 | 3 | PASS |
| 73 | Hard | 5 | 1 | 1 | 2 | 1 | PASS |
| 74 | Hard | 5 | 1 | 1 | 2 | 1 | PASS |
| 75 | Hard | 5 | 1 | 1 | 2 | 3 | PASS |
| 76 | Hard | 5 | 1 | 1 | 2 | 2 | PASS |
| 77 | Hard | 5 | 1 | 1 | 2 | 3 | PASS |
| 78 | Hard | 5 | 1 | 1 | 2 | 3 | PASS |
| 79 | Hard | 5 | 1 | 1 | 2 | 2 | PASS |
| 80 | Hard | 5 | 1 | 1 | 2 | 4 | PASS |
| 81 | Hard | 5 | 1 | 1 | 2 | 4 | PASS |
| 82 | Hard | 5 | 1 | 1 | 2 | 1 | PASS |
| 83 | Hard | 5 | 1 | 1 | 2 | 3 | PASS |
| 84 | Hard | 5 | 1 | 1 | 2 | 4 | PASS |
| 85 | Hard | 5 | 1 | 1 | 2 | 1 | PASS |
| 86 | Hard | 5 | 1 | 1 | 2 | 2 | PASS |
| 87 | Hard | 5 | 1 | 1 | 2 | 3 | PASS |
| 88 | Hard | 5 | 1 | 1 | 2 | 3 | PASS |
| 89 | Hard | 5 | 1 | 1 | 2 | 2 | PASS |
| 90 | Hard | 5 | 1 | 1 | 2 | 3 | PASS |
| 91 | Hard | 5 | 1 | 1 | 2 | 4 | PASS |
| 92 | Hard | 5 | 1 | 1 | 2 | 2 | PASS |
| 93 | Hard | 5 | 1 | 1 | 2 | 1 | PASS |
| 94 | Hard | 5 | 1 | 1 | 2 | 3 | PASS |
| 95 | Hard | 5 | 1 | 1 | 2 | 3 | PASS |
| 96 | Hard | 5 | 1 | 1 | 2 | 3 | PASS |
| 97 | Hard | 5 | 1 | 1 | 2 | 3 | PASS |
| 98 | Hard | 5 | 1 | 1 | 2 | 2 | PASS |
| 99 | Hard | 5 | 1 | 1 | 2 | 2 | PASS |
| 100 | Hard | 5 | 1 | 1 | 2 | 3 | PASS |
| 101 | Expert | 6 | 1 | 2 | 2 | 4 | PASS |
| 102 | Expert | 6 | 1 | 2 | 3 | 4 | PASS |
| 103 | Expert | 6 | 1 | 2 | 2 | 4 | PASS |
| 104 | Expert | 6 | 1 | 2 | 2 | 5 | PASS |
| 105 | Expert | 6 | 1 | 2 | 3 | 3 | PASS |
| 106 | Expert | 6 | 1 | 2 | 2 | 3 | PASS |
| 107 | Expert | 6 | 1 | 2 | 2 | 1 | PASS |
| 108 | Expert | 6 | 1 | 2 | 2 | 6 | PASS |
| 109 | Expert | 6 | 1 | 2 | 2 | 3 | PASS |
| 110 | Expert | 6 | 1 | 2 | 2 | 2 | PASS |
| 111 | Expert | 6 | 1 | 2 | 3 | 6 | PASS |
| 112 | Expert | 6 | 1 | 2 | 3 | 4 | PASS |
| 113 | Expert | 6 | 1 | 2 | 2 | 4 | PASS |
| 114 | Expert | 6 | 1 | 2 | 2 | 4 | PASS |
| 115 | Expert | 6 | 1 | 2 | 2 | 4 | PASS |
| 116 | Expert | 6 | 1 | 2 | 3 | 4 | PASS |
| 117 | Expert | 6 | 1 | 2 | 2 | 4 | PASS |
| 118 | Expert | 6 | 1 | 2 | 1 | 5 | PASS |
| 119 | Expert | 6 | 1 | 2 | 2 | 4 | PASS |
| 120 | Expert | 6 | 1 | 2 | 2 | 3 | PASS |
