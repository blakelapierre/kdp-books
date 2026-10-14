# Verification report: *Porch Swing Crosswords*

Produced by `src/verify.py`, which does not use the generator code (`src/cross.py`). It reads only `data.json` (the printed grids and clue lists).

## Summary

- Puzzles checked: **80** (40 Easy, 40 Medium), **1378** clues in total
- Clue list matches the grid exactly (every across/down run of 2+ letters is a numbered answer, numbered the standard way, and nothing else): **80 / 80**
- Grid is one connected piece and every answer crosses at least one other: **80 / 80**
- **Exactly one way to fill the grid from its word bank** (independent SAT solver, Minisat via python-sat; the solver finds a fill, blocks it and must then find no other): **80 / 80**
- No clue contains its own answer or the answer's stem: **80 / 80**
- Answers repeated anywhere in the book: **0**; puzzles where one answer is a prefix of another (e.g. SKI/SKIS): **0**
- Every answer is an English dictionary word (wordfreq word list): **yes**
- Content scan of titles, scene lines and clues for violent words (kill, murder, dead, death, die, blood, gun, knife, stab, shoot, weapon, poison, corpse, victim, crime, attack, fight, war, bomb, cannon, hunter, hunt, trap, prey, slaughter): **none found**

**Result: ALL CHECKS PASSED**

## What "exactly one solution" means for a crossword

A crossword's answers come from its clues, so a computer can't prove a clue has only one possible answer. What it can prove is that the grid itself is sound: every word in the grid is one of the clued answers, all crossings agree, and, given the puzzle's word bank (printed in the back for solvers who get stuck), there is only one way to place the words. That last property means the word bank alone is enough to finish any puzzle with no guessing. The clues were also written to be plain and fair: definitions and simple fill-in-the-blanks, no cryptic wordplay, no trivia about celebrities.

## Per puzzle

| # | Title | Level | Grid | Clues | Clue list = grid | Connected | Word-bank fills | Clues |
|---|---|---|---|---|---|---|---|---|
| 1 | Spring Cleaning | Easy | 12×13 | 16 | yes | yes | 1 | ok |
| 2 | The Vegetable Patch | Easy | 12×13 | 16 | yes | yes | 1 | ok |
| 3 | Birdsong | Easy | 12×13 | 16 | yes | yes | 1 | ok |
| 4 | April Showers | Easy | 12×13 | 16 | yes | yes | 1 | ok |
| 5 | The Flower Show | Easy | 11×13 | 16 | yes | yes | 1 | ok |
| 6 | Baby Animals on the Farm | Easy | 8×13 | 16 | yes | yes | 1 | ok |
| 7 | Kite Day | Easy | 12×10 | 16 | yes | yes | 1 | ok |
| 8 | At the Bakery | Easy | 12×11 | 16 | yes | yes | 1 | ok |
| 9 | Afternoon Tea | Easy | 11×13 | 16 | yes | yes | 1 | ok |
| 10 | Butterflies and Bugs | Easy | 12×13 | 16 | yes | yes | 1 | ok |
| 11 | By the Pond | Easy | 12×11 | 16 | yes | yes | 1 | ok |
| 12 | The Picnic Basket | Easy | 12×13 | 16 | yes | yes | 1 | ok |
| 13 | Bicycle Ride | Easy | 11×13 | 16 | yes | yes | 1 | ok |
| 14 | The Herb Garden | Easy | 12×12 | 16 | yes | yes | 1 | ok |
| 15 | The Knitting Circle | Easy | 11×13 | 16 | yes | yes | 1 | ok |
| 16 | Library Day | Easy | 12×12 | 16 | yes | yes | 1 | ok |
| 17 | The Breakfast Table | Easy | 12×12 | 15 | yes | yes | 1 | ok |
| 18 | Orchard in Blossom | Easy | 11×12 | 16 | yes | yes | 1 | ok |
| 19 | The Music Lesson | Easy | 11×13 | 16 | yes | yes | 1 | ok |
| 20 | Puppy School | Easy | 12×10 | 16 | yes | yes | 1 | ok |
| 21 | At the Seaside | Easy | 12×14 | 17 | yes | yes | 1 | ok |
| 22 | The Ice Cream Parlor | Easy | 13×13 | 17 | yes | yes | 1 | ok |
| 23 | Camping Out | Easy | 13×13 | 17 | yes | yes | 1 | ok |
| 24 | The Lemonade Stand | Easy | 13×14 | 17 | yes | yes | 1 | ok |
| 25 | Summer Fruits | Easy | 13×13 | 17 | yes | yes | 1 | ok |
| 26 | The County Fair | Easy | 12×14 | 17 | yes | yes | 1 | ok |
| 27 | Set Sail | Easy | 11×14 | 17 | yes | yes | 1 | ok |
| 28 | A Night of Stars | Easy | 13×14 | 17 | yes | yes | 1 | ok |
| 29 | Rock Pools | Easy | 13×14 | 17 | yes | yes | 1 | ok |
| 30 | The Garden Party | Easy | 13×14 | 17 | yes | yes | 1 | ok |
| 31 | Road Trip | Easy | 13×14 | 17 | yes | yes | 1 | ok |
| 32 | Backyard Cookout | Easy | 12×14 | 17 | yes | yes | 1 | ok |
| 33 | Swimming Pool | Easy | 12×14 | 17 | yes | yes | 1 | ok |
| 34 | Trail Walk | Easy | 13×13 | 17 | yes | yes | 1 | ok |
| 35 | Bees and Sunflowers | Easy | 13×14 | 17 | yes | yes | 1 | ok |
| 36 | Games on the Lawn | Easy | 13×14 | 17 | yes | yes | 1 | ok |
| 37 | Pack Your Suitcase | Easy | 13×14 | 15 | yes | yes | 1 | ok |
| 38 | At the Zoo | Easy | 12×14 | 17 | yes | yes | 1 | ok |
| 39 | Island Life | Easy | 12×14 | 17 | yes | yes | 1 | ok |
| 40 | The Art Class | Easy | 13×14 | 17 | yes | yes | 1 | ok |
| 41 | Falling Leaves | Medium | 13×15 | 19 | yes | yes | 1 | ok |
| 42 | Apple Picking | Medium | 13×15 | 19 | yes | yes | 1 | ok |
| 43 | The Pumpkin Patch | Medium | 13×15 | 19 | yes | yes | 1 | ok |
| 44 | Harvest Supper | Medium | 13×15 | 19 | yes | yes | 1 | ok |
| 45 | Back to School | Medium | 13×15 | 18 | yes | yes | 1 | ok |
| 46 | The Soup Kettle | Medium | 13×15 | 19 | yes | yes | 1 | ok |
| 47 | Woodland Friends | Medium | 13×15 | 19 | yes | yes | 1 | ok |
| 48 | Sweater Weather | Medium | 13×14 | 18 | yes | yes | 1 | ok |
| 49 | Board Game Night | Medium | 13×15 | 19 | yes | yes | 1 | ok |
| 50 | The Craft Fair | Medium | 13×15 | 19 | yes | yes | 1 | ok |
| 51 | The Writing Desk | Medium | 13×15 | 17 | yes | yes | 1 | ok |
| 52 | Down on the Farm | Medium | 13×14 | 19 | yes | yes | 1 | ok |
| 53 | Pie Baking Day | Medium | 13×15 | 19 | yes | yes | 1 | ok |
| 54 | Autumn Weather | Medium | 13×15 | 18 | yes | yes | 1 | ok |
| 55 | The Spice Rack | Medium | 13×15 | 19 | yes | yes | 1 | ok |
| 56 | The Corner Coffee Shop | Medium | 13×15 | 19 | yes | yes | 1 | ok |
| 57 | A Rainy Day Indoors | Medium | 13×15 | 19 | yes | yes | 1 | ok |
| 58 | Nuts and Seeds | Medium | 13×15 | 17 | yes | yes | 1 | ok |
| 59 | The Cozy Cottage | Medium | 13×15 | 19 | yes | yes | 1 | ok |
| 60 | Family Gathering | Medium | 13×15 | 18 | yes | yes | 1 | ok |
| 61 | Snow Day | Medium | 12×15 | 16 | yes | yes | 1 | ok |
| 62 | Hot Drinks | Medium | 13×15 | 18 | yes | yes | 1 | ok |
| 63 | Fireside Evening | Medium | 13×14 | 19 | yes | yes | 1 | ok |
| 64 | On the Ice | Medium | 12×15 | 20 | yes | yes | 1 | ok |
| 65 | Holiday Cookies | Medium | 13×15 | 15 | yes | yes | 1 | ok |
| 66 | Gift Wrapping | Medium | 13×15 | 20 | yes | yes | 1 | ok |
| 67 | Winter Birds | Medium | 12×15 | 16 | yes | yes | 1 | ok |
| 68 | Snowy Mountains | Medium | 13×14 | 15 | yes | yes | 1 | ok |
| 69 | The Pantry Shelves | Medium | 13×14 | 16 | yes | yes | 1 | ok |
| 70 | Puzzle Night | Medium | 13×15 | 20 | yes | yes | 1 | ok |
| 71 | Polar Animals | Medium | 13×15 | 20 | yes | yes | 1 | ok |
| 72 | Lights and Decorations | Medium | 13×14 | 16 | yes | yes | 1 | ok |
| 73 | The Toy Shop | Medium | 13×15 | 15 | yes | yes | 1 | ok |
| 74 | New Year's Eve | Medium | 13×15 | 17 | yes | yes | 1 | ok |
| 75 | At the Theater | Medium | 13×15 | 19 | yes | yes | 1 | ok |
| 76 | Comfort Food | Medium | 13×15 | 15 | yes | yes | 1 | ok |
| 77 | The Train Journey | Medium | 13×15 | 16 | yes | yes | 1 | ok |
| 78 | Bedtime | Medium | 13×15 | 18 | yes | yes | 1 | ok |
| 79 | Cats by the Fire | Medium | 13×15 | 19 | yes | yes | 1 | ok |
| 80 | Waiting for Spring | Medium | 12×15 | 19 | yes | yes | 1 | ok |
