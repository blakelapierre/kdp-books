# Verification report

Generated 2026-10-06 10:06 PDT by `src/verify.py` in 0.7 s.

- Puzzles checked: **140** (+ the worked example: all printed statements hold)
- Well formed, and printed clues match the picture (clues re-counted independently): **140/140**
- Exactly one solution (independent SAT solver, CaDiCaL via python-sat), equal to the picture: **140/140**
- Generator's line solver finishes the grid line by line, no guessing, to the same picture: **140/140**
- Meet difficulty band (grid size and line-solver sweeps in range): **140/140**
- Pixels adjusted to make a picture line-solvable within the limit (15×15: ≤2, 20×20: ≤3, 25×25: ≤5): **140/140**; pictures left exactly as drawn: 114
- Each subject used once: **True**; no duplicate pictures: **True**; numbered 1..140 in order: **True**

A *sweep* is one pass of exact line deduction over every row and then every column; the count includes the final pass that finds nothing left to do.

| Band | Grid | Puzzles | Nos. | Band rule (sweeps) | Sweeps seen |
|---|---|---|---|---|---|
| Easy | 15×15 | 30 | 1–30 | 1–9 | 2–9 |
| Medium | 20×20 | 40 | 31–70 | 3–12 | 3–12 |
| Hard | 25×25 | 40 | 71–110 | 6–13 | 6–12 |
| Expert | 25×25 | 30 | 111–140 | ≥ 14 | 14–25 |

## Worked example checks

- rows 4 and 8 say 8: **yes**
- rows 3 and 7 say 6: **yes**
- after one pass over the rows exactly rows 4, 8 and columns 3-6 of rows 3, 7 are shaded, nothing dotted: **yes**
- columns 1 and 8 say 1 1: **yes**
- columns 2 and 7 say 6, filling rows 3 to 8: **yes**
- unique (SAT) and line-solvable: **yes**

## Per-puzzle results

| # | Band | Grid | Picture | SAT solutions | Unique | Line-solved | Sweeps | Pixels adjusted | Shaded |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Easy | 15×15 | A Window | 1 | yes | yes | 2 | 0 | 61% |
| 2 | Easy | 15×15 | A Ladder | 1 | yes | yes | 3 | 0 | 37% |
| 3 | Easy | 15×15 | A Door | 1 | yes | yes | 3 | 0 | 39% |
| 4 | Easy | 15×15 | A Glass of Milk | 1 | yes | yes | 3 | 0 | 31% |
| 5 | Easy | 15×15 | A Chess Pawn | 1 | yes | yes | 3 | 0 | 36% |
| 6 | Easy | 15×15 | A Paper Lantern | 1 | yes | yes | 3 | 0 | 36% |
| 7 | Easy | 15×15 | A Snowflake | 1 | yes | yes | 3 | 0 | 48% |
| 8 | Easy | 15×15 | An Apple | 1 | yes | yes | 3 | 0 | 59% |
| 9 | Easy | 15×15 | An Umbrella | 1 | yes | yes | 4 | 0 | 28% |
| 10 | Easy | 15×15 | A Top Hat | 1 | yes | yes | 4 | 0 | 35% |
| 11 | Easy | 15×15 | The Mountain | 1 | yes | yes | 4 | 0 | 28% |
| 12 | Easy | 15×15 | A Jar | 1 | yes | yes | 4 | 0 | 36% |
| 13 | Easy | 15×15 | A Musical Note | 1 | yes | yes | 4 | 0 | 38% |
| 14 | Easy | 15×15 | A Mushroom | 1 | yes | yes | 4 | 0 | 44% |
| 15 | Easy | 15×15 | A Candle | 1 | yes | yes | 5 | 0 | 18% |
| 16 | Easy | 15×15 | A Light Bulb | 1 | yes | yes | 5 | 0 | 31% |
| 17 | Easy | 15×15 | A Winter Boot | 1 | yes | yes | 5 | 0 | 28% |
| 18 | Easy | 15×15 | A Cupcake | 1 | yes | yes | 5 | 0 | 35% |
| 19 | Easy | 15×15 | A Cup of Cocoa | 1 | yes | yes | 5 | 0 | 39% |
| 20 | Easy | 15×15 | A Cottage | 1 | yes | yes | 5 | 0 | 46% |
| 21 | Easy | 15×15 | A Cup of Tea | 1 | yes | yes | 6 | 0 | 28% |
| 22 | Easy | 15×15 | Warm Socks | 1 | yes | yes | 6 | 0 | 39% |
| 23 | Easy | 15×15 | An Hourglass | 1 | yes | yes | 6 | 0 | 40% |
| 24 | Easy | 15×15 | A Swan | 1 | yes | yes | 6 | 0 | 28% |
| 25 | Easy | 15×15 | A Tent | 1 | yes | yes | 7 | 0 | 23% |
| 26 | Easy | 15×15 | A Teddy Bear | 1 | yes | yes | 7 | 0 | 36% |
| 27 | Easy | 15×15 | An Ice Skate | 1 | yes | yes | 8 | 0 | 34% |
| 28 | Easy | 15×15 | A Pine Tree | 1 | yes | yes | 8 | 0 | 30% |
| 29 | Easy | 15×15 | A Hiking Boot | 1 | yes | yes | 8 | 0 | 36% |
| 30 | Easy | 15×15 | The Crescent Moon | 1 | yes | yes | 9 | 0 | 23% |
| 31 | Medium | 20×20 | Spectacles | 1 | yes | yes | 3 | 0 | 14% |
| 32 | Medium | 20×20 | An Open Book | 1 | yes | yes | 3 | 0 | 33% |
| 33 | Medium | 20×20 | A Bicycle | 1 | yes | yes | 3 | 0 | 32% |
| 34 | Medium | 20×20 | A Camera | 1 | yes | yes | 3 | 0 | 41% |
| 35 | Medium | 20×20 | A Postbox | 1 | yes | yes | 3 | 0 | 32% |
| 36 | Medium | 20×20 | A Ferris Wheel | 1 | yes | yes | 3 | 0 | 47% |
| 37 | Medium | 20×20 | A Radio | 1 | yes | yes | 3 | 0 | 42% |
| 38 | Medium | 20×20 | The Sofa | 1 | yes | yes | 3 | 0 | 35% |
| 39 | Medium | 20×20 | A Bed | 1 | yes | yes | 4 | 0 | 22% |
| 40 | Medium | 20×20 | A Battery | 1 | yes | yes | 4 | 0 | 21% |
| 41 | Medium | 20×20 | Skis | 1 | yes | yes | 4 | 0 | 27% |
| 42 | Medium | 20×20 | A Bus | 1 | yes | yes | 4 | 0 | 26% |
| 43 | Medium | 20×20 | A Castle | 1 | yes | yes | 4 | 0 | 42% |
| 44 | Medium | 20×20 | A Telephone | 1 | yes | yes | 4 | 0 | 36% |
| 45 | Medium | 20×20 | A Bear | 1 | yes | yes | 4 | 0 | 60% |
| 46 | Medium | 20×20 | A Chestnut | 1 | yes | yes | 4 | 0 | 50% |
| 47 | Medium | 20×20 | Scissors | 1 | yes | yes | 5 | 0 | 33% |
| 48 | Medium | 20×20 | A Basket | 1 | yes | yes | 5 | 0 | 51% |
| 49 | Medium | 20×20 | The Steam Engine | 1 | yes | yes | 5 | 0 | 42% |
| 50 | Medium | 20×20 | A Rucksack | 1 | yes | yes | 5 | 0 | 46% |
| 51 | Medium | 20×20 | A Magnet | 1 | yes | yes | 6 | 0 | 28% |
| 52 | Medium | 20×20 | A Slipper | 1 | yes | yes | 6 | 0 | 19% |
| 53 | Medium | 20×20 | A Fondue Pot | 1 | yes | yes | 6 | 0 | 30% |
| 54 | Medium | 20×20 | A Pretzel | 1 | yes | yes | 6 | 0 | 38% |
| 55 | Medium | 20×20 | A Set Square | 1 | yes | yes | 8 | 0 | 21% |
| 56 | Medium | 20×20 | A Cake | 1 | yes | yes | 8 | 0 | 34% |
| 57 | Medium | 20×20 | A Potted Plant | 1 | yes | yes | 8 | 0 | 28% |
| 58 | Medium | 20×20 | A Pig | 1 | yes | yes | 8 | 0 | 25% |
| 59 | Medium | 20×20 | A Gem | 1 | yes | yes | 9 | 0 | 28% |
| 60 | Medium | 20×20 | A Die | 1 | yes | yes | 9 | 0 | 33% |
| 61 | Medium | 20×20 | The Globe | 1 | yes | yes | 9 | 0 | 38% |
| 62 | Medium | 20×20 | A Campsite | 1 | yes | yes | 9 | 0 | 27% |
| 63 | Medium | 20×20 | A Ring | 1 | yes | yes | 10 | 0 | 28% |
| 64 | Medium | 20×20 | A Sled | 1 | yes | yes | 10 | 0 | 23% |
| 65 | Medium | 20×20 | A Cat | 1 | yes | yes | 10 | 1 | 32% |
| 66 | Medium | 20×20 | Grapes | 1 | yes | yes | 10 | 1 | 32% |
| 67 | Medium | 20×20 | Fallen Leaves | 1 | yes | yes | 11 | 1 | 30% |
| 68 | Medium | 20×20 | A Tortoise | 1 | yes | yes | 11 | 0 | 32% |
| 69 | Medium | 20×20 | A Llama | 1 | yes | yes | 12 | 1 | 25% |
| 70 | Medium | 20×20 | A Loaf of Bread | 1 | yes | yes | 12 | 0 | 43% |
| 71 | Hard | 25×25 | The Salt Shaker | 1 | yes | yes | 6 | 0 | 24% |
| 72 | Hard | 25×25 | A Doughnut | 1 | yes | yes | 6 | 0 | 46% |
| 73 | Hard | 25×25 | A Penguin | 1 | yes | yes | 6 | 0 | 28% |
| 74 | Hard | 25×25 | The Mantel Clock | 1 | yes | yes | 6 | 0 | 35% |
| 75 | Hard | 25×25 | A Crackling Fire | 1 | yes | yes | 6 | 0 | 33% |
| 76 | Hard | 25×25 | A Deer | 1 | yes | yes | 6 | 0 | 28% |
| 77 | Hard | 25×25 | A Puppy | 1 | yes | yes | 6 | 0 | 36% |
| 78 | Hard | 25×25 | A Tractor | 1 | yes | yes | 6 | 0 | 33% |
| 79 | Hard | 25×25 | A Ball of Yarn | 1 | yes | yes | 6 | 0 | 46% |
| 80 | Hard | 25×25 | A Honey Pot | 1 | yes | yes | 6 | 0 | 40% |
| 81 | Hard | 25×25 | Pancakes | 1 | yes | yes | 6 | 0 | 50% |
| 82 | Hard | 25×25 | A Pot of Stew | 1 | yes | yes | 7 | 0 | 26% |
| 83 | Hard | 25×25 | A Chair | 1 | yes | yes | 7 | 0 | 23% |
| 84 | Hard | 25×25 | An Owl | 1 | yes | yes | 7 | 0 | 35% |
| 85 | Hard | 25×25 | A Scarf | 1 | yes | yes | 7 | 0 | 34% |
| 86 | Hard | 25×25 | A Raccoon | 1 | yes | yes | 7 | 0 | 33% |
| 87 | Hard | 25×25 | A Hedgehog | 1 | yes | yes | 7 | 0 | 40% |
| 88 | Hard | 25×25 | A Coconut | 1 | yes | yes | 7 | 0 | 39% |
| 89 | Hard | 25×25 | A Maple Leaf | 1 | yes | yes | 8 | 0 | 30% |
| 90 | Hard | 25×25 | Mittens | 1 | yes | yes | 8 | 0 | 26% |
| 91 | Hard | 25×25 | The Cable Car | 1 | yes | yes | 8 | 0 | 34% |
| 92 | Hard | 25×25 | A Sunflower | 1 | yes | yes | 8 | 0 | 31% |
| 93 | Hard | 25×25 | A Slice of Cake | 1 | yes | yes | 8 | 0 | 39% |
| 94 | Hard | 25×25 | A Bathtub | 1 | yes | yes | 8 | 0 | 34% |
| 95 | Hard | 25×25 | A Kitten | 1 | yes | yes | 9 | 0 | 25% |
| 96 | Hard | 25×25 | A Butterfly | 1 | yes | yes | 9 | 0 | 39% |
| 97 | Hard | 25×25 | A Dog | 1 | yes | yes | 9 | 0 | 34% |
| 98 | Hard | 25×25 | A Bison | 1 | yes | yes | 9 | 0 | 38% |
| 99 | Hard | 25×25 | A Goat | 1 | yes | yes | 10 | 0 | 22% |
| 100 | Hard | 25×25 | A Koala | 1 | yes | yes | 10 | 0 | 28% |
| 101 | Hard | 25×25 | A Cow | 1 | yes | yes | 10 | 0 | 30% |
| 102 | Hard | 25×25 | A Bucket | 1 | yes | yes | 10 | 0 | 35% |
| 103 | Hard | 25×25 | A Fox | 1 | yes | yes | 11 | 0 | 30% |
| 104 | Hard | 25×25 | A Panda | 1 | yes | yes | 11 | 0 | 37% |
| 105 | Hard | 25×25 | A Wave | 1 | yes | yes | 11 | 0 | 37% |
| 106 | Hard | 25×25 | A Compass | 1 | yes | yes | 11 | 0 | 40% |
| 107 | Hard | 25×25 | A Lemon | 1 | yes | yes | 12 | 0 | 23% |
| 108 | Hard | 25×25 | A Waffle | 1 | yes | yes | 12 | 0 | 28% |
| 109 | Hard | 25×25 | A Squirrel | 1 | yes | yes | 12 | 0 | 32% |
| 110 | Hard | 25×25 | A Drum | 1 | yes | yes | 12 | 0 | 37% |
| 111 | Expert | 25×25 | A Bowl of Porridge | 1 | yes | yes | 14 | 1 | 27% |
| 112 | Expert | 25×25 | A Bunny | 1 | yes | yes | 14 | 0 | 27% |
| 113 | Expert | 25×25 | An Otter | 1 | yes | yes | 14 | 2 | 28% |
| 114 | Expert | 25×25 | A Microscope | 1 | yes | yes | 14 | 0 | 27% |
| 115 | Expert | 25×25 | A Ladybird | 1 | yes | yes | 14 | 1 | 35% |
| 116 | Expert | 25×25 | An Eagle | 1 | yes | yes | 14 | 0 | 30% |
| 117 | Expert | 25×25 | A Car | 1 | yes | yes | 15 | 2 | 21% |
| 118 | Expert | 25×25 | A Cap | 1 | yes | yes | 15 | 2 | 22% |
| 119 | Expert | 25×25 | A Pie | 1 | yes | yes | 15 | 1 | 28% |
| 120 | Expert | 25×25 | A Strawberry | 1 | yes | yes | 15 | 1 | 33% |
| 121 | Expert | 25×25 | An Alarm Clock | 1 | yes | yes | 15 | 2 | 38% |
| 122 | Expert | 25×25 | An Avocado | 1 | yes | yes | 15 | 3 | 35% |
| 123 | Expert | 25×25 | A Bee | 1 | yes | yes | 15 | 0 | 36% |
| 124 | Expert | 25×25 | The Teapot | 1 | yes | yes | 16 | 0 | 21% |
| 125 | Expert | 25×25 | A Badger | 1 | yes | yes | 16 | 1 | 22% |
| 126 | Expert | 25×25 | A Snail | 1 | yes | yes | 16 | 2 | 32% |
| 127 | Expert | 25×25 | A Fountain | 1 | yes | yes | 16 | 0 | 34% |
| 128 | Expert | 25×25 | A Beaver | 1 | yes | yes | 16 | 1 | 27% |
| 129 | Expert | 25×25 | An Ice Cube | 1 | yes | yes | 16 | 4 | 32% |
| 130 | Expert | 25×25 | A Yo-yo | 1 | yes | yes | 17 | 3 | 37% |
| 131 | Expert | 25×25 | A House and Garden | 1 | yes | yes | 18 | 1 | 36% |
| 132 | Expert | 25×25 | A Duck | 1 | yes | yes | 18 | 4 | 28% |
| 133 | Expert | 25×25 | A Rooster | 1 | yes | yes | 18 | 0 | 30% |
| 134 | Expert | 25×25 | A Wedge of Cheese | 1 | yes | yes | 19 | 2 | 26% |
| 135 | Expert | 25×25 | A Fish | 1 | yes | yes | 20 | 2 | 22% |
| 136 | Expert | 25×25 | A Dove | 1 | yes | yes | 20 | 1 | 27% |
| 137 | Expert | 25×25 | A Wolf | 1 | yes | yes | 20 | 1 | 33% |
| 138 | Expert | 25×25 | A Pudding | 1 | yes | yes | 20 | 1 | 31% |
| 139 | Expert | 25×25 | An Old Cabin | 1 | yes | yes | 23 | 1 | 40% |
| 140 | Expert | 25×25 | A Tulip | 1 | yes | yes | 25 | 0 | 24% |
