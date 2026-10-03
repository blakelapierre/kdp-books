# Verification: Tea and Clues at Tidewhistle Cove

Run: `cd src && python3 verify.py`. Result: **PASS**.

- Cases: **30** (7 logic cases checked by brute force, 23 clue-based story cases checked against a fair-play table)
- Total words in the book text: **15,404**
- Read-aloud rules: no digits anywhere, no tables, grids, images, footnotes or symbols inside chapters; every case ends with *Can you solve it?*, then *Think about it...*, then the solution.
- Content rule: no violent vocabulary (murder, kill, dead, death, blood, weapon and similar words are all checked). Every case is a theft, a borrowing or a missing item, and every item is returned.

## Logic cases

| # | Case | Answer | Check |
|---|------|--------|-------|
| 5 | The Marrow Mix-up | Morwenna Day | Brute force over every possibility gives exactly one answer: ['Morwenna'] |
| 8 | The Four Bakers | Mr Fenwick | Brute force over every possibility gives exactly one answer: ['Fenwick'] |
| 11 | The Window Table | Captain Quill | Brute force over every possibility gives exactly one answer: ['Quill'] |
| 16 | The Lighthouse Path | Mr Opie | Brute force over every possibility gives exactly one answer: ['Opie'] |
| 22 | The Honest Fishermen | Bran | Brute force over every possibility gives exactly one answer: ['Bran'] |
| 26 | The Winning Ticket | Demelza Rowe | Brute force over every possibility gives exactly one answer: ['Demelza'] |
| 28 | Truth and Fib Night | Tamsin Trevelyan | Brute force over every possibility gives exactly one answer: ['Tamsin'] |

## Story cases: fair-play table

Each decisive clue appears in the story before the question; each other suspect is ruled out by something stated in the story.

| # | Case | Answer | Decisive clue | Others ruled out |
|---|------|--------|---------------|------------------|
| 1 | The Prize Sponge | Jago Penhallow | Names the cake as a lemon drizzle when Ollie only said entry number seven; cakes were under glass domes and cloths and the only entry list was in Agnes's handbag. | Morwenna Day: Never names the cake; at the far end with flowers.; Hedley Truscott: Never names the cake; says he couldn't tell one from another. |
| 2 | The Lemonade on the Lawn | Mr Bramble | Sharp-edged ice in a frosty glass on the hottest afternoon, when the outdoor ice ran out at two and the only ice left was in the kitchen freezer beside the locket. | Demelza Rowe: Asleep in a deckchair since before two, three witnesses.; Captain Quill: With Agnes at the harbour office from one o'clock until they arrived together. |
| 3 | The Dry Raincoat | Wenna Polglaze | Claims she just ran in from the harbour through the downpour, yet is completely dry; door bell rang only for Hedley. | Hedley Truscott: At the counter in Tamsin's view from the moment he arrived.; Pip Carew: Outside under the awning, seen through the window throughout; never came in. |
| 4 | The Sandbar at High Tide | Mr Rundle | Claims to be digging on the sandbar during high water at noon, when it is under more than a man's height of sea. | Morwenna Day: With the vicar eleven to one.; Pip Carew: With Agnes all morning. |
| 6 | The Closed Post Office | Mr Garland | Claims he bought the blanket at the post office on Sunday morning; the post office is always closed on Sundays. | Tamsin Trevelyan: In church since ten.; Jago Penhallow: Baking since five with two helpers. |
| 7 | The Dog That Stayed Quiet | Pip Carew | Pickle barks at everyone at the only gate except Loveday and Pip; a wakeful neighbour heard no barking. | Mr Fenwick: Pickle would have barked.; Mrs Ashby: Pickle would have barked. |
| 9 | The Sunset over the Sea | Mr Ashdown | Tidewhistle Cove faces east; the sun rises over the sea and sets behind the hills, so no sunset into the sea. | Tamsin Trevelyan: Running book club, eight witnesses.; Hedley Truscott: Darts team all evening. |
| 10 | The Wet Paint Bench | Mr Kemp | Claims an hour on a bench painted at half past two that stays tacky till eight, but his cream trousers are spotless. | Hedley Truscott: Paint on hands, but with Ollie all afternoon.; Wenna Polglaze: In the tea room with Agnes three to four. |
| 12 | The Stopped Clock | Mr Prowse | Claims the tea room clock read a quarter past three; it has been stopped at ten to nine since Monday. | Demelza Rowe: Left before half past three, then with Captain Quill.; Hedley Truscott: Asleep at home from twenty past three, wife confirms. |
| 13 | The Misspelled Note | Hedley Truscott | The note spells pier p, e, i, r, exactly like Hedley's slipway sign. | Tamsin Trevelyan: Her poster spells pier correctly.; Jago Penhallow: His chalkboard spells pier correctly. |
| 14 | The Blue Ribbon Key | Mr Spargo | Mentions the blue ribbon, which only committee members or a user of the key would know; Ollie mentioned only the key. | Demelza Rowe: At her sister's from five, confirmed.; Pip Carew: Shows no knowledge of the key. |
| 15 | The Warm Bonnet | Mr Treloar | Biscuit sleeps on recently run engines; Mr Treloar's bonnet is warm on a chilly morning though he says the car hasn't moved. | Mr Fenwick: Car up on bricks with a flat tyre.; Kerensa Hale: Untouched overnight dew on the windscreen. |
| 17 | The Talking Parrot | Mr Pascoe | Admiral suddenly repeats Mr Pascoe's unique catchphrase, which he learns only by hearing it several times in a row; Pascoe has a key. | Tamsin Trevelyan: Never says the phrase; nobody but Pascoe does.; Mr Fenwick: Never says the phrase; nobody but Pascoe does. |
| 18 | The Moonlit Walk | Miss Clemo | Describes a bright full moon on the night the Gazette gives as a new moon. | Demelza Rowe: Left before eleven with Captain Quill, while the chart was still there.; Captain Quill: Walked Demelza home before eleven. |
| 19 | The Ship's Bell | Tobias Ferris | Only the tallest person can reach the hook on tiptoe; ladder locked, only key with Agnes, no furniture, stool broken. | Loveday Nance: A little over five feet, cannot reach.; Mr Fenwick: Not much taller than Loveday, cannot reach. |
| 20 | The Scent of Lavender | Mrs Vosper | Drawer velvet smells strongly of lavender water; only Mrs Vosper wears it. | Captain Quill: Smells of fish and seaweed.; Hedley Truscott: Smells only of engine oil. |
| 21 | The Spanish Coin | Mr Nankervis | The till started empty except a sealed bank float; only Mr Nankervis put coins into it. | Demelza Rowe: Paid by card.; Pip Carew: Paid with a banknote; coins went out to him as change. |
| 23 | The Odd Glove | Mr Lanyon | The right glove with anchors matches the left glove Mr Lanyon is wearing. | Kerensa Hale: Wearing both of a plain pair.; Mr Fenwick: Never wears gloves. |
| 24 | The Kite Festival | Mr Penberthy | Wind blew from the sea inland all day, so a snapped kite could not fly out to sea. | Pip Carew: At the top of the beach with his class.; Tamsin Trevelyan: At the book stall by the car park all afternoon. |
| 25 | The Teaspoon Thief | a magpie | Doors locked, gap a hand's width, only shiny objects taken, magpie feather on the sill: the thief is a bird. | Pip Carew: No key; gap too small for any person.; Mr Fenwick: At the grocer's from five, confirmed; no key.; Loveday Nance: No key; gap too small. |
| 27 | The Silent Foghorn | Mr Keast | Claims the foghorn boomed all night; it sounds whenever there is fog, and Agnes, awake with the window open, heard none on a clear night. | Captain Quill: On watch with two crew all night.; Tamsin Trevelyan: At her sister's in town overnight. |
| 29 | The Sugar Bowl | Mr Bolitho | Tea drunk black with three sugars (twelve lumps down to nine, milk untouched); only Mr Bolitho takes it that way. | Captain Quill: Plenty of milk, no sugar.; Loveday Nance: Milk and one sugar. |
| 30 | The Missing Sign | Constable Ollie Penrose | The note is in green ink; only Ollie writes in green ink. | Hedley Truscott: Writes only in pencil, has no pen.; Tamsin Trevelyan: Writes only in blue ink. |
