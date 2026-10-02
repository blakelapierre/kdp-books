# KDP listing draft: *Tents in Frostwood*

> Draft only. Nothing has been published or submitted to KDP. Step-by-step publishing checklist: [README.md](README.md).

## Title
**Tents in Frostwood**

## Subtitle
**180 Tents and Trees Logic Puzzles for Adults and Teens: Easy to Expert Grid Puzzles with Solutions**

## Author
**Blake La Pierre** (matches the title page, the copyright page, the front cover and the spine).

## Series
Book 4 of **"A Frostwood Puzzle Book"**, after *The Thief Stayed the Night* (book 1), *Frostwood Express* (book 2) and *Stars over Frostwood* (book 3). The cover and title page already say "A Frostwood Puzzle Book". If you set up the series on KDP, add this book as number 4.

## Description (1,819 characters; KDP limit is 4,000)
KDP accepts limited HTML (`<b>`, `<i>`, `<ul>`, `<li>`, `<br>`) in the description box.

```html
<b>Each winter the Frostwood campers pitch their tents beside the mountain pines, from the lodge meadow up the hollow trail to the ridge. This year the trail maps are smudged.</b>

180 clearings need their tents put back. Each one is a <b>Tents</b> puzzle (also called Tents and Trees). Place one tent beside every pine, keep the tents from touching even at the corners, and match the numbers on the rows and columns.

Every puzzle has <b>exactly one solution</b>, checked by computer, and every one can be solved by logic alone, with no guessing.

<b>Inside you'll find:</b>
<ul>
<li>180 Tents and Trees puzzles in four parts, in order of difficulty</li>
<li>40 Easy (6×6) and 40 Medium (8×8)</li>
<li>50 Hard (10×10) and 50 Expert (12×12)</li>
<li>Big, clear grids with room for pencil marks: two per page for Easy and Medium, one per page for Hard and Expert</li>
<li>A how-to-play guide with a fully worked example and the key solving tricks</li>
<li>Complete solutions at the back</li>
<li>6 × 9 inch paperback, easy to carry and easy to write in</li>
<li>Black-and-white ink illustrations: a frontispiece of the camp under the stars, a scene opening each section and small campsite drawings on the puzzle pages</li>
</ul>

From the Lodge Meadow to Summit Ridge Camp, the puzzles grow step by step. First you'll clear the zero-rows and force a pine's last free neighbour. Then you'll learn to ask “what if a tent were here?” and follow the answer until a pine or a row runs out of room.

Book four of the cozy Frostwood Puzzle Books, after <i>The Thief Stayed the Night</i>, <i>Frostwood Express</i> and <i>Stars over Frostwood</i>. A good fit for adults, teens and families who enjoy logic puzzles, Sudoku, Nonograms, Battleships and brain teasers.

Grab a pencil, pour some cocoa, and pitch camp among the pines.
```

## Keywords (7 slots)
1. tents and trees puzzle book
2. tents logic puzzles for adults
3. logic grid puzzles with solutions
4. brain teasers for teens and adults
5. tents puzzle book easy to hard
6. winter puzzle book for adults
7. cozy puzzle gift for puzzle lovers

## Suggested categories (pick 2–3 in KDP's category picker)
- Humor & Entertainment › Puzzles & Games › Logic & Brain Teasers
- Humor & Entertainment › Puzzles & Games › Puzzles
- Humor & Entertainment › Puzzles & Games › Math Games (optional third)

## Print specs used
- Trim 6 × 9 in (regular trim), black ink on **white** paper, no bleed interior, matte or glossy cover
- Interior: **184 pages** (includes the black-and-white ink illustrations: solid black line art on white, 300 DPI, no gray washes), grayscale only, all fonts embedded and subset (Crimson Text, Playfair Display SC, IBM Plex Sans Condensed, and DejaVu Sans for the ❄ symbol). Mirrored margins: inside 0.75 in, outside 0.55 in, top 0.70 in, bottom 0.75 in. KDP's minimum for 151–300 pages is 0.5 in inside and 0.25 in outside.
- Spine width: 184 × 0.002252 in = **0.4144 in** (spine text is allowed; KDP recommends 79+ pages)
- Full-wrap cover: 0.125 + 6 + 0.4144 + 6 + 0.125 = **12.6644 in × 9.25 in**. The barcode area (2 × 1.2 in, lower right of the back cover, 0.25 in in from the trim) has no text or art.

## Suggested price
**$9.99 USD** (Amazon.com), the lowest price that earns the 60% royalty rate. At $9.98 or below the rate drops to 50%.

## Royalty math (from the actual 184-page interior)
KDP black-ink printing for white paper, pages over 110: **$1.00 + $0.012 × 184 = $3.208** per copy.
Paperback royalty at 60%: **0.60 × $9.99 − $3.208 = $2.79** per copy sold on Amazon.com (expanded distribution and other marketplaces pay less).

## Files to upload
- Interior: [`frostwood-04-tents-in-frostwood-interior.pdf`](frostwood-04-tents-in-frostwood-interior.pdf) (184 pages)
- Cover: [`frostwood-04-tents-in-frostwood-cover.pdf`](frostwood-04-tents-in-frostwood-cover.pdf) (full wrap, 12.6644 × 9.25 in; see `cover-info.json`)
- Illustration sources: [`illustrations/`](illustrations/) (drawn by `src/illustrations.py`)

## Things to decide or do before publishing
- **Author field**: **Blake La Pierre** only. Remove "Grok Bot" or any other co-author/contributor if KDP shows one.
- **AI-content disclosure applies.** The puzzles were generated by AI-written code, the text (how-to, blurb, description) was AI-written, and the cover and interior illustrations were drawn by AI-written code. Answer "yes" for text, and also for images if that is how you read KDP's guidance.
- **ISBN**: the plan is KDP's free ISBN. KDP prints the barcode in the blank area on the back cover.
- **Proof copy**: order a printed proof and check the 12×12 Expert grids, the tree and tent symbols, and the illustrations (solid black should print evenly).
- **Page count**: if the page count changes, rebuild the cover (`src/cover.py` reads `build-info.json`).

## Verification
Every puzzle was checked by an independent SAT solver (CaDiCaL via python-sat) and an independent backtracking counter. All 180 puzzles (plus the worked example) have exactly one solution matching the stored answer, and each fits its difficulty band. See `verification.md`.
