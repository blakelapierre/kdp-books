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
standalone/                  # books that are not part of a series (one folder each)
  README.md
  01-the-advent-clock/
  02-fireside-cryptograms/
  03-tea-and-clues-at-tidewhistle-cove/
  04-logic-on-lantern-lane/
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

`standalone/`
1. `01-the-advent-clock`: built, not published
2. `02-fireside-cryptograms`: built, not published
3. `03-tea-and-clues-at-tidewhistle-cove`: built Kindle ebook (audio-first), not published
4. `04-logic-on-lantern-lane`: built, not published

## Books

### Frostwood series ([series/frostwood/](series/frostwood/))

| # | Title | Puzzle type | Status | Pages | Price | Royalty* | Publishing checklist |
|---|-------|-------------|--------|-------|-------|----------|----------------------|
| 1 | *The Thief Stayed the Night*: A Snowbound Hotel Mystery Puzzle Book (12 cozy elimination cases) | Elimination mystery | Live on Amazon ([B0HLMMS675](https://www.amazon.com/dp/B0HLMMS675)) | 136 | $9.99 | $3.36 | [01-the-thief-stayed-the-night/README.md](series/frostwood/01-the-thief-stayed-the-night/README.md) |
| 2 | *Frostwood Express*: 200 Train Tracks Logic Puzzles (Easy to Expert) | Train Tracks | Live on Amazon ([B0HLMB966Q](https://www.amazon.com/dp/B0HLMB966Q)) | 194 | $11.99 | $3.87 | [02-frostwood-express/README.md](series/frostwood/02-frostwood-express/README.md) |
| 3 | *Stars over Frostwood*: 180 Star Battle Logic Puzzles (Easy to Expert) | Star Battle (1-star and 2-star) | Draft, print-ready. Not yet published or submitted to KDP | 184 | $9.99 | $2.79 | [03-stars-over-frostwood/README.md](series/frostwood/03-stars-over-frostwood/README.md) |
| 4 | *Tents in Frostwood*: 180 Tents and Trees Logic Puzzles (Easy to Expert) | Tents / Tents and Trees | Draft, print-ready. Not yet published or submitted to KDP | 184 | $9.99 | $2.79 | [04-tents-in-frostwood/README.md](series/frostwood/04-tents-in-frostwood/README.md) |
| 5 | *Riddles by the Frostwood Fire*: 140 Cozy Winter Riddles & Text Logic Puzzles (Kindle) | Riddles + text logic (no grids) | Draft, ebook-ready. Not yet published or submitted to KDP | — (ebook) | $3.99 | $2.66† | [05-riddles-by-the-frostwood-fire/README.md](series/frostwood/05-riddles-by-the-frostwood-fire/README.md) |

### Standalone ([standalone/](standalone/))

| Title | Puzzle type | Status | Pages | Price | Royalty* | Publishing checklist |
|-------|-------------|--------|-------|-------|----------|----------------------|
| *The Advent Clock*: A Christmas Puzzle Countdown (24-day advent calendar puzzle book) | 24 mixed daily puzzles (19 kinds) with a hidden-message meta puzzle | Draft, print-ready. Not yet published or submitted to KDP | 92 | $9.99 | $3.69 | [01-the-advent-clock/README.md](standalone/01-the-advent-clock/README.md) |
| *Fireside Cryptograms*: 200 Large-Print Quote Puzzles for Adults (Easy to Expert) | Cryptograms (cryptoquotes) | Draft, print-ready. Not yet published or submitted to KDP | 158 | $9.99 | $3.10 | [02-fireside-cryptograms/README.md](standalone/02-fireside-cryptograms/README.md) |
| *Tea and Clues at Tidewhistle Cove*: 30 Cozy Mini-Mysteries to Solve by Ear (Kindle, audio-first) | Solve-it-yourself cozy mini-mysteries + text logic (no grids) | Draft, ebook-ready. Not yet published or submitted to KDP | — (ebook, 15,404 words) | $3.99 | $2.75† | [03-tea-and-clues-at-tidewhistle-cove/README.md](standalone/03-tea-and-clues-at-tidewhistle-cove/README.md) |
| *Logic on Lantern Lane*: 120 Cozy Logic Grid Puzzles for Adults (Easy to Expert) | Logic grid (Einstein / zebra) puzzles with story clues | Draft, print-ready. Not yet published or submitted to KDP | 194 | $9.99 | $2.67 | [04-logic-on-lantern-lane/README.md](standalone/04-logic-on-lantern-lane/README.md) |

All books are by Blake La Pierre and are 6 × 9 in paperbacks with black ink on white paper. Every interior is illustrated with black-and-white ink drawings (frontispiece, title art, section openers and small vignettes).

\*Royalty per copy on Amazon.com at the listed price: 0.60 × price − printing, where printing is $2.30 flat for 24–110 pages, otherwise $1.00 + $0.012 × pages. †Kindle 70% royalty ≈ 0.70 × price − delivery fee ($0.15/MB). Each book's README is a phone-friendly KDP publishing checklist with download links for its files.

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
```

The fonts come from system paths: `/usr/share/fonts/truetype/sand-box/google/` (Crimson Text, Playfair Display SC, IBM Plex Sans Condensed) and DejaVu Sans. Change `G` in `build.py` if your fonts are somewhere else.

See [ideas-log.md](ideas-log.md) for ideas that have already been built or evaluated.
