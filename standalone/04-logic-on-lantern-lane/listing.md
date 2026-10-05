# KDP listing draft: *Logic on Lantern Lane*

> Draft only. Nothing has been published or submitted to KDP. Step-by-step publishing checklist: [README.md](README.md).

## Title
**Logic on Lantern Lane**

## Subtitle
**120 Cozy Logic Grid Puzzles for Adults | Easy to Expert | Hints & Solutions**

## Author
**Blake La Pierre** (matches the title page, the copyright page, the front cover and the spine). No co-authors.

## Series
Standalone (not part of the Frostwood series: a year-round village, not a winter lodge, and a puzzle type the series hasn't used).

## Description
The copy-paste HTML is in [README.md](README.md#3-copy-paste-fields) (about 1,650 characters; KDP limit is 4,000).

## Keywords (7 slots)
1. logic grid puzzles for adults
2. cozy logic puzzle book
3. einstein zebra puzzles easy to hard
4. logic problems with solutions and hints
5. brain teasers for adults deduction
6. non violent puzzle book gift
7. village mystery logic puzzles

## Suggested categories (pick 2–3 in KDP's category picker)
- Humor & Entertainment › Puzzles & Games › Logic & Brain Teasers
- Humor & Entertainment › Puzzles & Games › Puzzles
- Science & Math › Mathematics › Pure Mathematics › Logic (optional third)

(Check the exact names in the KDP picker before choosing.)

## Demand evidence (public Amazon pages, researched 2026-10-05)
Dedicated logic grid books sell steadily and are reviewed well: *The Ultimate Logic Grid Puzzle Book for Adults* (100 puzzles) 4.6★ from 423 ratings; *Logic Puzzle Book for Adults Volume 1* (50 puzzles, 6×9) 4.0★ from 269 ratings; *Detective Logic Puzzles for Adults* (Oct 2025) 4.6★ from 96 ratings, BSR ~#140k, #897 in Logic & Brain Teasers. The newest titles are crime- or detective-themed, and a 2025 "verified solutions" title with plain 4×5 grids sits at 2.8★ from 14 ratings (reviews point to bland themes). Gap: a cozy, non-violent, story-led logic grid book at 6×9 / $9.99 with a gentle difficulty ramp, a worked example and a first-step hint for every puzzle.

## What's inside
- 120 puzzles: 30 Easy (3 categories × 4), 30 Medium (4 × 4), 30 Hard (4 × 5), 30 Expert (5 × 5, two-page spreads)
- 40 village scenes (bake sale, knitting circle, tea room, bookshop, snowman contest, lantern parade, soup supper, bell ringers, piano recital, jam judging and more), each used once in three different levels with a different title and opening
- Clue types: direct matches, not-matches, comparisons (earlier / more / higher), exact gaps, either-or (exactly one), neither-nor, and "of A and B, one … the other …"
- Every puzzle is solvable by the grid rules alone (a human-style solver that never guesses filled every grid), and every puzzle has exactly one solution (independent SAT check, [verification.md](verification.md))
- Front matter: how to solve, reading the clues, a worked example with a step-by-step walkthrough; back matter: one hint per puzzle (the smallest set of clues that gives a sure first match) and full solution tables

## Print specs used
- Trim 6 × 9 in (regular trim), black ink on **white** paper, no bleed interior, matte cover
- Interior: **194 pages** (includes black-and-white ink illustrations: solid black line art on white, 300 DPI), grayscale, all fonts embedded (Crimson Text, Playfair Display SC, IBM Plex Sans Condensed), mirrored margins: inside 0.75 in, outside 0.55 in, top 0.70 in, bottom 0.75 in
- Spine width: 194 × 0.002252 in = **0.4369 in** (spine text included; KDP recommends 79+ pages)
- Full-wrap cover: 0.125 + 6 + 0.4369 + 6 + 0.125 = **12.6869 in × 9.25 in**. The barcode area (2 × 1.2 in, lower right of the back cover, 0.25 in in from the trim) has no text or art.

## Suggested price
**$9.99 USD** (Amazon.com), the lowest price that earns the 60% paperback royalty rate. At $9.98 or below the rate drops to 50%.

## Estimated royalty per copy (Amazon.com)
From KDP's published formula for black-ink paperbacks, regular trim, 110–828 pages, Amazon.com: fixed cost **$1.00** plus **$0.012 per page**.

- Printing cost = $1.00 + 194 × $0.012 = **$3.328 ≈ $3.33**
- Royalty = 60% × list price − printing cost
- At **$9.99**: 0.60 × 9.99 − 3.328 = 5.994 − 3.328 = **$2.67 per copy**

| List price | Royalty rate | Royalty per copy |
|---|---|---|
| $8.99 | 50% | $1.17 |
| **$9.99** | **60%** | **$2.67** |
| $10.99 | 60% | $3.27 |
| $11.99 | 60% | $3.87 |
| $9.99 via Expanded Distribution | 40% | $0.67 |

The two-page Expert spreads add 30 pages (about $0.36 of printing per copy). If you'd rather earn more per copy, $10.99 still undercuts most competitors ($12.99–$16.97).

**Sources**:
- Printing cost: KDP Help, "Paperback Printing Cost": https://kdp.amazon.com/en_US/help/topic/G201834340
- Royalty rate: KDP Help, "Paperback Royalty": https://kdp.amazon.com/en_US/help/topic/G201834330

These figures are estimates. Confirm them with KDP's Printing Cost & Royalty Calculator on the Rights & Pricing page before you set the price.

## Files to upload
- Interior: [`standalone-04-logic-on-lantern-lane-interior.pdf`](standalone-04-logic-on-lantern-lane-interior.pdf) (194 pages)
- Cover: [`standalone-04-logic-on-lantern-lane-cover.pdf`](standalone-04-logic-on-lantern-lane-cover.pdf) (full wrap, 12.6869 × 9.25 in; see `cover-info.json`)
- Illustration sources: [`illustrations/`](illustrations/) (drawn by `src/illustrations.py`)

## Things to decide or do before publishing
- **AI-content disclosure applies.** The puzzles were generated by AI-written code, the scenes, clues and listing text were AI-written, and the cover and interior art was drawn by AI-written code. Answer "yes" for text and for images.
- **ISBN**: plan is KDP's free ISBN. The copyright page has no ISBN line; KDP prints the barcode in the blank area on the back cover.
- **Proof copy**: order a printed proof and check that the grid labels and the Expert grid boxes (0.18 in) are comfortable to write in.
- **Page count**: if the page count changes, rebuild the cover (`src/cover.py` reads `build-info.json`).
- **Author field**: enter **Blake La Pierre** only. Don't add any co-author.

## Verification
See `verification.md`: all 120 puzzles and the worked example have exactly one solution according to an independent SAT solver that reads only the stated clues, every printed clue sentence matches its structure and is true of the printed answer, and a content scan found no violent words.
