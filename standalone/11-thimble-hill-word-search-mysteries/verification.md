# Verification report

Independent re-solve of every grid by `src/verify.py` (it does not trust the generator's placement records).

Result: **ALL 60 PUZZLES PASS**

Checks: each listed word appears exactly once in all 8 directions; it runs only in that level's directions; the unused squares read in order spell the hidden clue exactly; no offensive word appears in any line outside a real list word.

| Puzzle | Case | Level | Words | Directions | Hidden clue | Result |
|---|---|---|---|---|---|---|
| 1 | 1 | Gentle | 19 | ESSE | THE RIBBON VANISHED AT NOON | OK |
| 2 | 1 | Gentle | 21 | ESSE | THE THIEF WORE NO GLOVES | OK |
| 3 | 1 | Gentle | 18 | ESSE | NO WHEEL TRACKS IN THE MUD | OK |
| 4 | 1 | Gentle | 19 | ESSE | RUPERT WAS ON STAGE AT NOON | OK |
| 5 | 1 | Gentle | 22 | ESSE | THE PRINT IS PINK AND SWEET | OK |
| 6 | 1 | Gentle | 22 | ESSE | IT SMELLS OF STRAWBERRY | OK |
| 7 | 2 | Gentle | 18 | ESSE | IT WAS TAKEN IN STORY HOUR | OK |
| 8 | 2 | Gentle | 20 | ESSE | MISS PATEL READ ALL HOUR | OK |
| 9 | 2 | Gentle | 22 | ESSE | NELL WAS AT THE DESK | OK |
| 10 | 2 | Gentle | 22 | ESSE | A NOTE WAS LEFT INSIDE | OK |
| 11 | 2 | Gentle | 22 | ESSE | IT IS NEATLY HANDWRITTEN | OK |
| 12 | 2 | Gentle | 24 | ESSE | THE INK IS GREEN | OK |
| 13 | 3 | Gentle | 22 | ESSE | THE PIE WAS THERE AT TEN | OK |
| 14 | 3 | Gentle | 23 | ESSE | THE SILL IS VERY HIGH UP | OK |
| 15 | 3 | Gentle | 24 | ESSE | ROSA WAS AT THE DENTIST | OK |
| 16 | 3 | Gentle | 22 | ESSE | GREGOR NEVER LEFT HIS SHOP | OK |
| 17 | 3 | Gentle | 24 | ESSE | JUICE DRIPPED ON A MAILBAG | OK |
| 18 | 3 | Gentle | 24 | ESSE | A BIG CROW WAS ON THE SILL | OK |
| 19 | 4 | Curious | 18 | ENESSE | THE GNOME WAS GONE BY TWO | OK |
| 20 | 4 | Curious | 18 | ENESSE | JASPER CAME AT THREE | OK |
| 21 | 4 | Curious | 21 | ENESSE | BLUE PAINT ON THE GATE | OK |
| 22 | 4 | Curious | 19 | ENESSE | NO HEEL MARKS IN THE SOIL | OK |
| 23 | 4 | Curious | 18 | ENESSE | HUGO WAS AWAY AT SUMMER CAMP | OK |
| 24 | 4 | Curious | 23 | ENESSE | THE GNOME IS IN A PAINTING | OK |
| 25 | 5 | Curious | 20 | ENESSE | IT WENT AFTER THE TEA | OK |
| 26 | 5 | Curious | 18 | ENESSE | HAZEL LEFT AT THREE | OK |
| 27 | 5 | Curious | 22 | ENESSE | A GOLD THREAD WAS ON THE FLOOR | OK |
| 28 | 5 | Curious | 22 | ENESSE | AGNES NEVER LEFT HER CHAIR | OK |
| 29 | 5 | Curious | 23 | ENESSE | FELIX WAS UP ON THE ROOF | OK |
| 30 | 5 | Curious | 21 | ENESSE | IRIS WANTED TO ADD A STAR | OK |
| 31 | 6 | Curious | 21 | ENESSE | THE CLOCK STOPPED AT DAWN | OK |
| 32 | 6 | Curious | 20 | ENESSE | WINNIE WAS AWAY ALL WEEK | OK |
| 33 | 6 | Curious | 23 | ENESSE | OIL ON THE STAIR RAIL | OK |
| 34 | 6 | Curious | 22 | ENESSE | OTTO WILL NOT CLIMB UP | OK |
| 35 | 6 | Curious | 23 | ENESSE | DOT WAS SINGING AT DAWN | OK |
| 36 | 6 | Curious | 23 | ENESSE | THE KEY WAS BEING POLISHED | OK |
| 37 | 7 | Curious | 18 | ENESSE | THE SWAP HAPPENED AT LUNCH | OK |
| 38 | 7 | Curious | 23 | ENESSE | WALT WAS SERVING SOUP | OK |
| 39 | 7 | Curious | 19 | ENESSE | THE NEW SEEDS ARE STRIPED | OK |
| 40 | 7 | Curious | 20 | ENESSE | POPPY STAYED HOME WITH A COLD | OK |
| 41 | 7 | Curious | 24 | ENESSE | NO MUD ON THE FLOOR | OK |
| 42 | 7 | Curious | 21 | ENESSE | A FEATHER WAS IN THE TIN | OK |
| 43 | 8 | Sharp-Eyed | 18 | ENNENWSSESWW | THE DOVES FLEW OFF AT NIGHT | OK |
| 44 | 8 | Sharp-Eyed | 21 | ENNENWSSESWW | LEO WAS ON THE LATE TRAIN | OK |
| 45 | 8 | Sharp-Eyed | 18 | ENNENWSSESWW | THE ROOM SMELLED OF LAVENDER | OK |
| 46 | 8 | Sharp-Eyed | 19 | ENNENWSSESWW | MAISIE SLEPT AT HER SISTERS | OK |
| 47 | 8 | Sharp-Eyed | 24 | ENNENWSSESWW | THE DOME IS VERY HEAVY | OK |
| 48 | 8 | Sharp-Eyed | 24 | ENNENWSSESWW | THE DOVES WERE ON HER OWN CAKE | OK |
| 49 | 9 | Sharp-Eyed | 20 | ENNENWSSESWW | THE MUSIC VANISHED AT SIX | OK |
| 50 | 9 | Sharp-Eyed | 21 | ENNENWSSESWW | PERCY WAS TUNING HIS TUBA | OK |
| 51 | 9 | Sharp-Eyed | 23 | ENNENWSSESWW | A PEPPERMINT WRAPPER | OK |
| 52 | 9 | Sharp-Eyed | 22 | ENNENWSSESWW | NED WAS SWEEPING THE STEPS | OK |
| 53 | 9 | Sharp-Eyed | 24 | ENNENWSSESWW | WILMA WAS AT HER SINGING LESSON | OK |
| 54 | 9 | Sharp-Eyed | 24 | ENNENWSSESWW | GRETA WAS COPYING THE MUSIC | OK |
| 55 | 10 | Sharp-Eyed | 18 | ENNENWSSESWW | THE STAR WAS GONE BY DUSK | OK |
| 56 | 10 | Sharp-Eyed | 17 | ENNENWSSESWW | ARLO WAS LIGHTING THE LAMPS | OK |
| 57 | 10 | Sharp-Eyed | 23 | ENNENWSSESWW | CYRIL WAS IN A MEETING | OK |
| 58 | 10 | Sharp-Eyed | 23 | ENNENWSSESWW | BESS WAS TEACHING A CLASS | OK |
| 59 | 10 | Sharp-Eyed | 23 | ENNENWSSESWW | MUDDY PAW PRINTS | OK |
| 60 | 10 | Sharp-Eyed | 22 | ENNENWSSESWW | THE STRING LED HOME | OK |
