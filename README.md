# KDP Books

Source, print files and listing drafts for Blake La Pierre's Amazon KDP paperback puzzle books. Two books are live on Amazon: *The Thief Stayed the Night* and *Frostwood Express* (see the tables below). The others are built and print-ready but not yet published.

## Repository layout

```
series/
  frostwood/                 # "A Frostwood Puzzle Book" series (cozy winter, lodge / railway / village / mountain)
    README.md                # series overview: theme, house style, list of books
    01-the-thief-stayed-the-night/
    02-frostwood-express/
    03-stars-over-frostwood/
    04-tents-in-frostwood/
    05-riddles-by-the-frostwood-fire/
    06-the-frostwood-sketchbook/
    07-bridges-of-frostwood/
    08-fences-of-frostwood/
    09-the-lockboxes-of-frostwood/
    10-snow-paths-of-frostwood/
    11-chimneys-of-frostwood/
standalone/                  # books that are not part of a series (one folder each)
  README.md
  01-the-advent-clock/
  02-fireside-cryptograms/
  03-tea-and-clues-at-tidewhistle-cove/
  04-logic-on-lantern-lane/
  05-porch-swing-crosswords/
  06-stories-we-keep/
  07-three-clues-by-candlelight/
  08-window-seat-codewords/
marketing/                   # marketing kit: ads, reviews, A+ Content, social, holiday plan
README.md                    # this file
ideas-log.md                 # every idea built or evaluated (check before choosing a new one)
requirements.txt             # Python dependencies for all the build scripts
```

A book in a series goes in `series/<series-name>/NN-<book-slug>/`. A book that isn't in a series goes in `standalone/NN-<book-slug>/`. Each book folder is self-contained: its scripts only use paths relative to the folder itself, so you can move a folder without breaking anything.

### Folder numbering

Every book folder starts with a two-digit number and a hyphen: `NN-<book-slug>` (for example `03-stars-over-frostwood`). The slug is lowercase words joined with hyphens.

- Numbers count up separately inside each folder (`series/frostwood/` has its own 01, 02, ...; `standalone/` has its own 01, 02, ...). A new series folder starts again at 01.
- The number is the order the book was created in that folder (published books came first). For Frostwood it matches the series book number.
- **A new book gets the next number:** take the highest `NN` already in that folder and add 1, zero-padded to two digits (after `04-...` comes `05-...`).
- Never renumber or reuse a number, even if a book is dropped.

Current books:

`series/frostwood/`
1. `01-the-thief-stayed-the-night`: live ([Amazon](https://www.amazon.com/dp/B0HLMMS675))
2. `02-frostwood-express`: live ([Amazon](https://www.amazon.com/dp/B0HLMB966Q), $11.99)
3. `03-stars-over-frostwood`: built, not published
4. `04-tents-in-frostwood`: built, not published
5. `05-riddles-by-the-frostwood-fire`: built Kindle ebook, not published
6. `06-the-frostwood-sketchbook`: built paperback, not published
7. `07-bridges-of-frostwood`: built paperback, not published
8. `08-fences-of-frostwood`: built hardcover, not published
9. `09-the-lockboxes-of-frostwood`: built Kindle ebook, not published
10. `10-snow-paths-of-frostwood`: built paperback, not published
11. `11-chimneys-of-frostwood`: built hardcover, not published

`standalone/`
1. `01-the-advent-clock`: built, not published
2. `02-fireside-cryptograms`: built, not published
3. `03-tea-and-clues-at-tidewhistle-cove`: built Kindle ebook (audio-first), not published
4. `04-logic-on-lantern-lane`: built, not published
5. `05-porch-swing-crosswords`: built paperback, not published
6. `06-stories-we-keep`: built hardcover, not published
7. `07-three-clues-by-candlelight`: built Kindle ebook (audio-first), not published
8. `08-window-seat-codewords`: built paperback, not published

## Books

### Frostwood series ([series/frostwood/](series/frostwood/))

| # | Title | Puzzle type | Status | Pages | Price | Royalty* | Publishing checklist |
|---|-------|-------------|--------|-------|-------|----------|----------------------|
| 1 | *The Thief Stayed the Night*: A Snowbound Hotel Mystery Puzzle Book (12 cozy elimination cases) | Elimination mystery | Live on Amazon ([B0HLMMS675](https://www.amazon.com/dp/B0HLMMS675)) | 136 | $9.99 | $3.36 | [01-the-thief-stayed-the-night/README.md](series/frostwood/01-the-thief-stayed-the-night/README.md) |
| 2 | *Frostwood Express*: 200 Train Tracks Logic Puzzles (Easy to Expert) | Train Tracks | Live on Amazon ([B0HLMB966Q](https://www.amazon.com/dp/B0HLMB966Q)) | 194 | $11.99 | $3.87 | [02-frostwood-express/README.md](series/frostwood/02-frostwood-express/README.md) |
| 3 | *Stars over Frostwood*: 180 Star Battle Logic Puzzles (Easy to Expert) | Star Battle (1-star and 2-star) | Draft, print-ready. Not yet published or submitted to KDP | 184 | $9.99 | $2.79 | [03-stars-over-frostwood/README.md](series/frostwood/03-stars-over-frostwood/README.md) |
| 4 | *Tents in Frostwood*: 180 Tents and Trees Logic Puzzles (Easy to Expert) | Tents / Tents and Trees | Draft, print-ready. Not yet published or submitted to KDP | 184 | $9.99 | $2.79 | [04-tents-in-frostwood/README.md](series/frostwood/04-tents-in-frostwood/README.md) |
| 5 | *Riddles by the Frostwood Fire*: 140 Cozy Winter Riddles & Text Logic Puzzles (Kindle) | Riddles + text logic (no grids) | Draft, ebook-ready. Not yet published or submitted to KDP | — (ebook) | $3.99 | $2.66† | [05-riddles-by-the-frostwood-fire/README.md](series/frostwood/05-riddles-by-the-frostwood-fire/README.md) |
| 6 | *The Frostwood Sketchbook*: 140 Nonogram Picture Logic Puzzles (Easy to Expert) | Nonograms (hanjie picture logic) | Draft, print-ready paperback. Not yet published or submitted to KDP | 156 | $9.99 | $3.12 | [06-the-frostwood-sketchbook/README.md](series/frostwood/06-the-frostwood-sketchbook/README.md) |
| 7 | *Bridges of Frostwood*: 180 Hashi Bridges Logic Puzzles (Easy to Expert) | Hashi / Bridges (Hashiwokakero) | Draft, print-ready paperback. Not yet published or submitted to KDP | 188 | $9.99 | $2.74 | [07-bridges-of-frostwood/README.md](series/frostwood/07-bridges-of-frostwood/README.md) |
| 8 | *Fences of Frostwood*: 100 Slitherlink Logic Puzzles (Easy to Expert) | Slitherlink / Loop the Loop (hardcover) | Draft, print-ready hardcover. Not yet published or submitted to KDP | 88 | $17.99 | $3.99 | [08-fences-of-frostwood/README.md](series/frostwood/08-fences-of-frostwood/README.md) |
| 9 | *The Lockboxes of Frostwood*: 120 Crack-the-Code Logic Puzzles (Kindle) | Crack the code / number-lock deduction (no grids) | Draft, ebook-ready. Not yet published or submitted to KDP | — (ebook) | $3.99 | $2.66† | [09-the-lockboxes-of-frostwood/README.md](series/frostwood/09-the-lockboxes-of-frostwood/README.md) |
| 10 | *Snow Paths of Frostwood*: 160 Nurikabe Logic Puzzles (Easy to Expert) | Nurikabe (paperback) | Draft, print-ready paperback. Not yet published or submitted to KDP | 160 | $9.99 | $3.07 | [10-snow-paths-of-frostwood/README.md](series/frostwood/10-snow-paths-of-frostwood/README.md) |
| 11 | *Chimneys of Frostwood*: 100 Skyscrapers Logic Puzzles (Easy to Expert) | Skyscrapers / Towers (hardcover) | Draft, print-ready hardcover. Not yet published or submitted to KDP | 88 | $17.99 | $3.99 | [11-chimneys-of-frostwood/README.md](series/frostwood/11-chimneys-of-frostwood/README.md) |

### Standalone ([standalone/](standalone/))

| Title | Puzzle type | Status | Pages | Price | Royalty* | Publishing checklist |
|-------|-------------|--------|-------|-------|----------|----------------------|
| *The Advent Clock*: A Christmas Puzzle Countdown (24-day advent calendar puzzle book) | 24 mixed daily puzzles (19 kinds) with a hidden-message meta puzzle | ✅ Live, hardcover ([B0HMW1MR5T](https://www.amazon.com/dp/B0HMW1MR5T)) | 92 | $17.99 | ~$2.90 | [01-the-advent-clock/README.md](standalone/01-the-advent-clock/README.md) |
| *Fireside Cryptograms*: 200 Large-Print Quote Puzzles for Adults (Easy to Expert) | Cryptograms (cryptoquotes) | Draft, print-ready. Not yet published or submitted to KDP | 158 | $9.99 | $3.10 | [02-fireside-cryptograms/README.md](standalone/02-fireside-cryptograms/README.md) |
| *Tea and Clues at Tidewhistle Cove*: 30 Cozy Mini-Mysteries to Solve by Ear (Kindle, audio-first) | Solve-it-yourself cozy mini-mysteries + text logic (no grids) | Draft, ebook-ready. Not yet published or submitted to KDP | — (ebook, 15,404 words) | $3.99 | $2.75† | [03-tea-and-clues-at-tidewhistle-cove/README.md](standalone/03-tea-and-clues-at-tidewhistle-cove/README.md) |
| *Logic on Lantern Lane*: 120 Cozy Logic Grid Puzzles for Adults (Easy to Expert) | Logic grid (Einstein / zebra) puzzles with story clues | Draft, print-ready. Not yet published or submitted to KDP | 194 | $9.99 | $2.67 | [04-logic-on-lantern-lane/README.md](standalone/04-logic-on-lantern-lane/README.md) |
| *Porch Swing Crosswords*: 80 Cozy Themed Crossword Puzzles for Adults (Easy to Medium) | Freeform themed crosswords with plain clues and word banks | Draft, print-ready paperback. Not yet published or submitted to KDP | 196 | $9.99 | $2.64 | [05-porch-swing-crosswords/README.md](standalone/05-porch-swing-crosswords/README.md) |
| *Stories We Keep*: A Guided Memory Keepsake for the Ones We Love (hardcover) | Guided life-story prompts + family tree, timeline, letters | Draft, print-ready **hardcover**. Not yet published or submitted to KDP | 102 | $17.99 | $3.99 | [06-stories-we-keep/README.md](standalone/06-stories-we-keep/README.md) |
| *Three Clues by Candlelight*: 150 Cozy What-Am-I Riddles in Three Clues Each (Kindle, audio-first) | Three-clue What-Am-I riddles (no grids) | Draft, ebook-ready. Not yet published or submitted to KDP | — (ebook, 14,669 words) | $3.99 | $2.77† | [07-three-clues-by-candlelight/README.md](standalone/07-three-clues-by-candlelight/README.md) |
| *Window Seat Codewords*: 120 Cozy Codeword Puzzles for Adults (Easy, Medium & Hard) | Codewords (number-coded crosswords with no clues, American English) | Draft, print-ready paperback. Not yet published or submitted to KDP | 154 | $9.99 | $3.15 | [08-window-seat-codewords/README.md](standalone/08-window-seat-codewords/README.md) |
| *Two Cups of Tea*: A Couple's Question Journal (hardcover) | Couples question journal: 52 weekly spreads, 156 questions, an answer space for each partner | Draft, print-ready **hardcover**. Not yet published or submitted to KDP | 138 | $19.99 | $4.69 | [09-two-cups-of-tea/README.md](standalone/09-two-cups-of-tea/README.md) |
| *The Backseat Detectives*: 24 Road Trip Mysteries to Solve Out Loud (Kindle, audio-first) | Solve-it-yourself road-trip mini-mysteries for kids and families (no grids) | Draft, ebook-ready. Not yet published or submitted to KDP | — (ebook, 11,409 words) | $3.99 | $2.75† | [10-the-backseat-detectives/README.md](standalone/10-the-backseat-detectives/README.md) |
| *Twenty-Five Christmases*: A Family Christmas Memory Book to Fill In Year by Year (hardcover) | Fill-in family Christmas memory book: 25 years × 4 pages (photo, guests, tree, Eve and morning, table, gifts, best moment, wish), traditions, recipes | Draft, print-ready **hardcover**. Not yet published or submitted to KDP | 132 | $19.99 | $4.76 | [12-twenty-five-christmases/README.md](standalone/12-twenty-five-christmases/README.md) |
| *Twenty-Four Nights at the Christmas Post*: Cozy Christmas Mysteries to Solve Out Loud (Kindle, audio-first) | Solve-it-yourself Christmas countdown mini-mysteries for kids and families, one per December night (no grids) | Draft, ebook-ready. Not yet published or submitted to KDP | — (ebook, 12,562 words) | $3.99 | $2.74† | [13-twenty-four-nights-at-the-christmas-post/README.md](standalone/13-twenty-four-nights-at-the-christmas-post/README.md) |

All books are by Blake La Pierre and are 6 × 9 in (paperback or hardcover) with black ink on white paper. Every interior is illustrated with black-and-white ink drawings (frontispiece, title art, section openers and small vignettes).

\*Royalty per copy on Amazon.com at the listed price: 0.60 × price − printing, where paperback printing is $2.30 flat for 24–110 pages, otherwise $1.00 + $0.012 × pages; hardcover black-ink regular trim is $6.80 flat for 75–108 pages, otherwise $5.65 + $0.012 × pages (see KDP Hardcover Printing Cost). †Kindle 70% royalty ≈ 0.70 × price − delivery fee ($0.15/MB). Each book's README is a phone-friendly KDP publishing checklist with download links for its files.

## Marketing

The marketing kit is in [marketing/](marketing/README.md). It covers the action calendar, Amazon ads, reviews, Author Central, A+ Content, free printable samples, Pinterest and social posts, and the holiday plan.

## What's in each book folder

- `README.md`: phone-friendly KDP publishing checklist (status, download links, copy-paste listing fields, proof checks)
- `<prefix>-interior.pdf`: the interior file to upload to KDP (print books)
- `<prefix>-cover.pdf`: the full-wrap cover (back, spine and front) for print
- `<prefix>.epub` + `<prefix>-cover.jpg`: Kindle ebook manuscript and flat front cover (ebook books)
- File names are unique across the repo. The prefix is `frostwood-NN-<slug>` for series books and `standalone-NN-<slug>` for standalones, e.g. `frostwood-04-tents-in-frostwood-interior.pdf` and `standalone-02-fireside-cryptograms-cover.pdf`
- `illustrations/`: the 300 DPI black-and-white ink illustrations (drawn in code by `src/illustrations.py` using `src/inkart.py`)
- `listing.md`: listing draft with title, subtitle, description, keywords, categories, specs and pricing/royalty math
- `previews/`: PNG renders of the cover and some sample pages
- `data.json`: the generated puzzle data that the book is built from
- `build-info.json` / `cover-info.json`: page count, section page numbers and cover dimensions
- `clue-checks.md` (Frostwood book 1) / `verification.md` (the other books): the report from the independent verification run
- `src/`: scripts for generating, building and verifying the book

## Rebuilding a book

Run the scripts from inside the book's `src/` folder. Install the dependencies from the repo root first. They read and write files in the book folder (`../`) using relative paths.

```bash
python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt

# Book 1: The Thief Stayed the Night
cd series/frostwood/01-the-thief-stayed-the-night/src
python3 gen.py        # regenerate ../data.json from master.py (guest list) and clues.py (cases); optional arg: max seeds
python3 illustrations.py   # draw the ink illustrations -> ../illustrations/*.png (deterministic)
python3 build.py      # -> ../frostwood-01-the-thief-stayed-the-night-interior.pdf and ../build-info.json (the story text is in stories.py)
python3 cover.py      # -> ../frostwood-01-the-thief-stayed-the-night-cover.pdf and ../cover-info.json (reads the page count)
python3 verify.py     # independent re-check -> ../clue-checks.md
cd ../../../..

# Book 2: Frostwood Express
cd series/frostwood/02-frostwood-express/src
python3 master.py     # generate and grade the 200 puzzles -> ../data.json (tracks.py is the solver, gen.py sets the difficulty bands)
python3 illustrations.py   # draw the ink illustrations -> ../illustrations/*.png (deterministic)
python3 build.py      # -> ../frostwood-02-frostwood-express-interior.pdf and ../build-info.json
python3 cover.py      # -> ../frostwood-02-frostwood-express-cover.pdf, ../cover-info.json and ../tmp/frostwood-02-frostwood-express-cover-guides.pdf
python3 verify.py     # checks each puzzle has one solution with a SAT solver (verify_sat.py) -> ../verification.md
cd ../../../..

# Book 3: Stars over Frostwood
cd series/frostwood/03-stars-over-frostwood/src
python3 master.py     # generate and grade the 180 puzzles -> ../data.json (about 20 min on 6 cores; stars.py is the logic solver, gen.py sets the bands)
python3 illustrations.py   # draw the ink illustrations -> ../illustrations/*.png (deterministic)
python3 build.py      # -> ../frostwood-03-stars-over-frostwood-interior.pdf and ../build-info.json (worked-example text is in example_text.py)
python3 cover.py      # -> ../frostwood-03-stars-over-frostwood-cover.pdf, ../cover-info.json and ../tmp/frostwood-03-stars-over-frostwood-cover-guides.pdf
python3 verify.py     # independent SAT check (verify_sat.py) of uniqueness + band fit -> ../verification.md
cd ../../../..

# Book 4: Tents in Frostwood
cd series/frostwood/04-tents-in-frostwood/src
PYTHONHASHSEED=0 python3 master.py   # generate and grade the 180 puzzles -> ../data.json (tents.py is the logic/SAT solver, gen.py sets the bands)
python3 illustrations.py   # draw the ink illustrations -> ../illustrations/*.png (deterministic)
python3 build.py      # -> ../frostwood-04-tents-in-frostwood-interior.pdf and ../build-info.json (worked-example text is in example_text.py)
python3 cover.py      # -> ../frostwood-04-tents-in-frostwood-cover.pdf, ../cover-info.json and ../tmp/frostwood-04-tents-in-frostwood-cover-guides.pdf
python3 verify.py     # independent SAT + backtracking uniqueness check + band fit -> ../verification.md
cd ../../../..

# Book 6: The Frostwood Sketchbook (paperback)
cd series/frostwood/06-the-frostwood-sketchbook/src
PYTHONHASHSEED=0 python3 master.py   # rasterise every candidate picture (Noto Emoji glyphs, src/fonts/) and make it line-solvable -> ../tmp/candidates.json (~20 s)
python3 choose.py     # pick the 140 puzzles into their bands -> ../data.json (deterministic: same file every run)
python3 verify.py     # independent SAT uniqueness check + line-solve + band fit + worked-example statements -> ../verification.md
python3 illustrations.py   # draw the ink illustrations -> ../illustrations/*.png (deterministic)
python3 build.py      # -> ../frostwood-06-the-frostwood-sketchbook-interior.pdf and ../build-info.json
python3 cover.py      # -> ../frostwood-06-the-frostwood-sketchbook-cover.pdf, ../cover-info.json and ../tmp/frostwood-06-the-frostwood-sketchbook-cover-guides.pdf
cd ../../../..

# Book 7: Bridges of Frostwood (paperback)
cd series/frostwood/07-bridges-of-frostwood/src
PYTHONHASHSEED=0 python3 master.py   # generate and grade the 180 Hashi puzzles -> ../data.json (~2 min on 8 cores; hashi.py is the SAT counter + logic solver, gen.py sets the bands)
python3 verify.py     # independent SAT + backtracking (hashi_bt.py) uniqueness check + band fit -> ../verification.md
python3 illustrations.py   # draw the ink illustrations -> ../illustrations/*.png (deterministic)
python3 build.py      # -> ../frostwood-07-bridges-of-frostwood-interior.pdf and ../build-info.json (worked-example text is in build.py)
python3 cover.py      # -> ../frostwood-07-bridges-of-frostwood-cover.pdf, ../cover-info.json and ../tmp/frostwood-07-bridges-of-frostwood-cover-guides.pdf
cd ../../../..

# Book 9: The Lockboxes of Frostwood (Kindle ebook)
cd series/frostwood/09-the-lockboxes-of-frostwood/src
PYTHONHASHSEED=0 python3 master.py   # gen.py (lockgen.py brute force) -> verify.py (independent DFS solver.py + exhaustive check) -> illustrations -> cover JPG -> EPUB (~2 min)
cd ../../../..

# Book 10: Snow Paths of Frostwood (paperback)
cd series/frostwood/10-snow-paths-of-frostwood/src
PYTHONHASHSEED=0 python3 master.py   # generate and grade the 160 Nurikabe puzzles -> ../data.json (nurikabe.py is the SAT counter + logic grader, gen.py sets the bands)
python3 verify.py     # independent SAT + backtracking (nk_bt.py) uniqueness check + band fit -> ../verification.md
python3 illustrations.py   # draw the ink illustrations -> ../illustrations/*.png (deterministic)
python3 build.py      # -> ../frostwood-10-snow-paths-of-frostwood-interior.pdf and ../build-info.json (worked-example text is in build.py)
python3 cover.py      # -> ../frostwood-10-snow-paths-of-frostwood-cover.pdf, ../cover-info.json and ../tmp/frostwood-10-snow-paths-of-frostwood-cover-guides.pdf
python3 check_margins.py   # no ink outside the text area / near the trim
python3 docs.py       # -> ../README.md and ../listing.md
cd ../../../..

# Book 11: Chimneys of Frostwood (hardcover)
cd series/frostwood/11-chimneys-of-frostwood/src
PYTHONHASHSEED=0 python3 master.py   # generate and grade the 100 Skyscrapers puzzles -> ../data.json (~4 min on 8 cores; sky.py is the logic solver, gen.py sets the bands)
python3 verify.py     # independent SAT (sky_sat.py) + backtracking (sky_bt.py) uniqueness check + band fit -> ../verification.md
python3 illustrations.py   # draw the ink illustrations -> ../illustrations/*.png (deterministic)
python3 build.py      # -> ../frostwood-11-chimneys-of-frostwood-interior.pdf and ../build-info.json
python3 cover.py      # hardcover wrap -> ../frostwood-11-chimneys-of-frostwood-cover.pdf, ../cover-info.json and ../tmp/ guides PDF
cd ../../../..

# Standalone: The Advent Clock
cd standalone/01-the-advent-clock/src
python3 gen.py        # generate all 24 door puzzles -> ../data.json (optional args: door numbers to regenerate only those; ~2 min). Not repeatable (the Queens doors come out different): don't rerun unless you want new puzzles
python3 illustrations.py   # draw the ink illustrations -> ../illustrations/*.png (deterministic)
python3 build.py      # -> ../standalone-01-the-advent-clock-interior.pdf and ../build-info.json (story, rules and hints text are in stories.py)
python3 cover.py      # -> ../standalone-01-the-advent-clock-cover.pdf, ../cover-info.json and ../tmp/standalone-01-the-advent-clock-cover-guides.pdf
python3 verify.py     # independent re-solve of every door + the Christmas Eve message -> ../verification.md
cd ../..

# Standalone: Fireside Cryptograms
cd standalone/02-fireside-cryptograms/src
PYTHONHASHSEED=0 python3 master.py   # generate 200 unique cryptograms -> ../data.json
python3 illustrations.py   # draw the ink illustrations -> ../illustrations/*.png (deterministic)
python3 build.py      # -> ../standalone-02-fireside-cryptograms-interior.pdf and ../build-info.json
python3 cover.py      # -> ../standalone-02-fireside-cryptograms-cover.pdf, ../cover-info.json and ../tmp/standalone-02-fireside-cryptograms-cover-guides.pdf
python3 verify.py     # independent dictionary solver uniqueness check -> ../verification.md
cd ../..

# Standalone: Tea and Clues at Tidewhistle Cove (Kindle ebook, audio-first)
cd standalone/03-tea-and-clues-at-tidewhistle-cove/src
python3 verify.py     # brute-force logic cases, fair-play table, read-aloud and content checks -> ../verification.md
python3 cover.py      # -> ../standalone-03-tea-and-clues-at-tidewhistle-cove-cover.jpg
python3 build.py      # -> ../standalone-03-tea-and-clues-at-tidewhistle-cove.epub, .docx and ../build-info.json
cd ../..

# Standalone: Logic on Lantern Lane
cd standalone/04-logic-on-lantern-lane/src
PYTHONHASHSEED=0 python3 master.py   # generate 120 logic grid puzzles + the worked example -> ../data.json (~10 s; logic.py is the no-guessing solver, gen.py makes clues and hints)
python3 verify.py     # independent SAT uniqueness check + clue-text truth + content scan -> ../verification.md
python3 illustrations.py   # draw the ink illustrations -> ../illustrations/*.png (deterministic)
python3 build.py      # -> ../standalone-04-logic-on-lantern-lane-interior.pdf and ../build-info.json
python3 cover.py      # -> ../standalone-04-logic-on-lantern-lane-cover.pdf, ../cover-info.json and ../tmp/standalone-04-logic-on-lantern-lane-cover-guides.pdf
cd ../..

# Standalone: Porch Swing Crosswords (paperback)
cd standalone/05-porch-swing-crosswords/src
PYTHONHASHSEED=0 python3 master.py   # generate the 80 themed crosswords -> ../data.json (~7 min; cross.py is the generator, themes_*.py hold the word lists and clues)
python3 verify.py     # independent checks: SAT one-fill-per-word-bank, numbering, repeats, clue and content scans -> ../verification.md (uses wordfreq if installed)
python3 illustrations.py   # draw the ink illustrations -> ../illustrations/*.png (deterministic)
python3 build.py      # -> ../standalone-05-porch-swing-crosswords-interior.pdf and ../build-info.json
python3 cover.py      # -> ../standalone-05-porch-swing-crosswords-cover.pdf, ../cover-info.json and ../tmp/standalone-05-porch-swing-crosswords-cover-guides.pdf
cp ../standalone-05-porch-swing-crosswords-interior.pdf ../interior-standalone-05-porch-swing-crosswords.pdf; cp ../standalone-05-porch-swing-crosswords-cover.pdf ../cover-standalone-05-porch-swing-crosswords.pdf   # phone-friendly copies

# Standalone: Stories We Keep (hardcover)
cd standalone/06-stories-we-keep/src
python3 illustrations.py   # draw ink illustrations -> ../illustrations/*.png
python3 build.py           # -> ../standalone-06-stories-we-keep-interior.pdf and ../build-info.json
python3 cover.py           # hardcover wrap -> ../standalone-06-stories-we-keep-cover.pdf and ../cover-info.json
cp ../standalone-06-stories-we-keep-interior.pdf ../interior-standalone-06-stories-we-keep.pdf
cp ../standalone-06-stories-we-keep-cover.pdf ../cover-standalone-06-stories-we-keep.pdf
cd ../../..

# Standalone: Window Seat Codewords (paperback)
cd standalone/08-window-seat-codewords/src
python3 words.py      # word lists: enable1.txt + wordfreq + en_US.dic (proper-noun filter) -> fill.txt
python3 master.py     # generate the 120 codewords -> ../data.json (~1 min; gen.py fills the grids and picks starters with its own solver)
python3 verify.py     # independent SAT check over the full ENABLE list (one key per puzzle), plus word/coverage/A-Z checks -> ../verification.md (~5 min)
python3 illustrations.py   # draw the ink illustrations -> ../illustrations/*.png (deterministic)
python3 build.py      # -> ../standalone-08-window-seat-codewords-interior.pdf and ../build-info.json
python3 cover.py      # -> ../standalone-08-window-seat-codewords-cover.pdf and ../tmp/standalone-08-window-seat-codewords-cover-guides.pdf
cp ../standalone-08-window-seat-codewords-interior.pdf ../interior-standalone-08-window-seat-codewords.pdf; cp ../standalone-08-window-seat-codewords-cover.pdf ../cover-standalone-08-window-seat-codewords.pdf   # phone-friendly copies
cd ../../..

# Standalone: Two Cups of Tea (hardcover)
cd standalone/09-two-cups-of-tea/src
python3 content.py         # checks 52 weeks, 156 unique questions, 52 unique themes
python3 illustrations.py   # draw the ink illustrations -> ../illustrations/*.png (deterministic)
python3 build.py           # -> ../standalone-09-two-cups-of-tea-interior.pdf and ../build-info.json
python3 cover.py           # hardcover wrap -> ../standalone-09-two-cups-of-tea-cover.pdf, ../cover-info.json and ../tmp/cover-guides.pdf
cd .. && python3 src/check_margins.py standalone-09-two-cups-of-tea-interior.pdf

# Standalone: The Backseat Detectives (Kindle ebook, audio-first)
cd standalone/10-the-backseat-detectives/src
python3 verify.py   # clue placement, audio-first and content checks -> ../verification.md
python3 cover.py    # -> ../standalone-10-the-backseat-detectives-cover.jpg
python3 build.py    # -> ../standalone-10-the-backseat-detectives.epub, .docx, ../build-info.json
cd ../../..

# Standalone: Twenty-Four Nights at the Christmas Post (Kindle ebook, audio-first)
cd standalone/13-twenty-four-nights-at-the-christmas-post/src
python3 verify.py   # clue placement, snowflake message, Secret Santa logic, audio-first and content checks -> ../verification.md
python3 cover.py    # -> ../standalone-13-twenty-four-nights-at-the-christmas-post-cover.jpg
python3 build.py    # -> ../standalone-13-twenty-four-nights-at-the-christmas-post.epub, .docx, ../build-info.json
cd ../../..

# Standalone: Twenty-Five Christmases (hardcover)
cd standalone/12-twenty-five-christmases/src
python3 content.py         # checks 25 unique yearly questions and the traditions list
python3 illustrations.py   # draw the ink illustrations -> ../illustrations/*.png (deterministic)
python3 build.py           # -> ../standalone-12-twenty-five-christmases-interior.pdf and ../build-info.json
python3 cover.py           # hardcover wrap -> ../standalone-12-twenty-five-christmases-cover.pdf, ../cover-info.json and ../tmp/cover-guides.pdf
cd .. && python3 src/check_margins.py standalone-12-twenty-five-christmases-interior.pdf
cd ../..
```

The fonts come from system paths: `/usr/share/fonts/truetype/sand-box/google/` (Crimson Text, Playfair Display SC, IBM Plex Sans Condensed) and DejaVu Sans. Change `G` in `build.py` if your fonts are somewhere else.

See [ideas-log.md](ideas-log.md) for ideas that have already been built or evaluated.
