# Verification — Riddles by the Frostwood Fire

Total puzzles: **140**
Seed: `20261003`

## Summary by difficulty

| Band | Pass | Fail |
|------|------|------|
| Easy | 40 | 0 |
| Medium | 40 | 0 |
| Hard | 40 | 0 |
| Expert | 20 | 0 |

## Summary by kind

| Kind | Pass | Fail |
|------|------|------|
| anagram | 6 | 0 |
| caesar | 11 | 0 |
| order_arrival | 7 | 0 |
| riddle | 92 | 0 |
| room_item | 10 | 0 |
| sequence | 7 | 0 |
| who_drink | 7 | 0 |

Duplicate prompts: **0**

## Result

**ALL PUZZLES PASSED.** Every logic puzzle has exactly one solution under an independent solver; every riddle has a non-empty intended answer present in its accept set.

## Method

- **Riddles:** independent of the wording generator; checks answer normalization and membership in the accept list.
- **Logic (who_drink, order_arrival, room_item, caesar, anagram, sequence):** re-solved from stored constraints/meta using `logic_gen.SOLVERS`, which enumerates or decodes without trusting the stored answer field until the final comparison.

