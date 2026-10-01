# KDP Books

Source, print files and listing drafts for Blake La Pierre's Amazon KDP paperback puzzle books. Nothing here has been published or submitted to KDP.

## Repository layout

```
series/
  frostwood/                 # "A Frostwood Puzzle Book" series (cozy winter, lodge / railway / village / mountain)
    README.md                # series overview: theme, house style, list of books
    the-thief-stayed-the-night/
    frostwood-express/
    stars-over-frostwood/
standalone/                  # books that are not part of a series (one folder each)
  README.md
marketing/                   # marketing kit: ads, reviews, A+ Content, social, holiday plan
README.md                    # this file
ideas-log.md                 # every idea built or evaluated (check before choosing a new one)
requirements.txt             # Python dependencies for all the build scripts
```

A book in a series goes in `series/<series-name>/<book-slug>/`. A book that isn't in a series goes in `standalone/<book-slug>/`. Each book folder is self-contained: its scripts only use paths relative to the folder itself, so you can move a folder without breaking anything.

## Books

### Frostwood series ([series/frostwood/](series/frostwood/))

| # | Title | Puzzle type | Status | Pages | Price | Folder |
|---|-------|-------------|--------|-------|-------|--------|
| 1 | *The Thief Stayed the Night*: A Snowbound Hotel Mystery Puzzle Book (12 cozy elimination cases) | Elimination mystery | Draft, print-ready. Not yet published or submitted to KDP | 134 | $9.99 | [series/frostwood/the-thief-stayed-the-night/](series/frostwood/the-thief-stayed-the-night/) |
| 2 | *Frostwood Express*: 200 Train Tracks Logic Puzzles (Easy to Expert) | Train Tracks | Draft, print-ready. Not yet published or submitted to KDP | 192 | $9.99 | [series/frostwood/frostwood-express/](series/frostwood/frostwood-express/) |
| 3 | *Stars over Frostwood*: 180 Star Battle Logic Puzzles (Easy to Expert) | Star Battle (1-star and 2-star) | Draft, print-ready. Not yet published or submitted to KDP | 182 | $9.99 | [series/frostwood/stars-over-frostwood/](series/frostwood/stars-over-frostwood/) |

### Standalone ([standalone/](standalone/))

| Title | Puzzle type | Status | Pages | Price | Folder |
|-------|-------------|--------|-------|-------|--------|
| *The Advent Clock*: A Christmas Puzzle Countdown (24-day advent calendar puzzle book) | 24 mixed daily puzzles (19 kinds) with a hidden-message meta puzzle | Draft, print-ready. Not yet published or submitted to KDP | 89 | $9.99 | [standalone/the-advent-clock/](standalone/the-advent-clock/) |
| *Fireside Cryptograms*: 200 Large-Print Quote Puzzles for Adults (Easy to Expert) | Cryptograms (cryptoquotes) | Draft, print-ready. Not yet published or submitted to KDP | 160 | $9.99 | [standalone/fireside-cryptograms/](standalone/fireside-cryptograms/) |

All books are by Blake La Pierre and are 6 × 9 in paperbacks with black ink on white paper.

## Marketing

The marketing kit is in [marketing/](marketing/README.md). It covers the action calendar, Amazon ads, reviews, Author Central, A+ Content, free printable samples, Pinterest and social posts, and the holiday plan.

## What's in each book folder

- `interior.pdf`: the interior file to upload to KDP
- `cover.pdf`: the full-wrap cover (back, spine and front)
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
cd series/frostwood/the-thief-stayed-the-night/src
python3 gen.py        # regenerate ../data.json from master.py (guest list) and clues.py (cases); optional arg: max seeds
python3 build.py      # -> ../interior.pdf and ../build-info.json (the story text is in stories.py)
python3 cover.py      # -> ../cover.pdf and ../cover-info.json (reads the page count)
python3 verify.py     # independent re-check -> ../clue-checks.md
cd ../../../..

# Book 2: Frostwood Express
cd series/frostwood/frostwood-express/src
python3 master.py     # generate and grade the 200 puzzles -> ../data.json (tracks.py is the solver, gen.py sets the difficulty bands)
python3 build.py      # -> ../interior.pdf and ../build-info.json
python3 cover.py      # -> ../cover.pdf, ../cover-info.json and ../tmp/cover-guides.pdf
python3 verify.py     # checks each puzzle has one solution with a SAT solver (verify_sat.py) -> ../verification.md
cd ../../../..

# Book 3: Stars over Frostwood
cd series/frostwood/stars-over-frostwood/src
python3 master.py     # generate and grade the 180 puzzles -> ../data.json (about 20 min on 6 cores; stars.py is the logic solver, gen.py sets the bands)
python3 build.py      # -> ../interior.pdf and ../build-info.json (worked-example text is in example_text.py)
python3 cover.py      # -> ../cover.pdf, ../cover-info.json and ../tmp/cover-guides.pdf
python3 verify.py     # independent SAT check (verify_sat.py) of uniqueness + band fit -> ../verification.md
cd ../../../..

# Standalone: The Advent Clock
cd standalone/the-advent-clock/src
python3 gen.py        # generate all 24 door puzzles -> ../data.json (optional args: door numbers to regenerate only those; ~2 min)
python3 build.py      # -> ../interior.pdf and ../build-info.json (story, rules and hints text are in stories.py)
python3 cover.py      # -> ../cover.pdf, ../cover-info.json and ../tmp/cover-guides.pdf
python3 verify.py     # independent re-solve of every door + the Christmas Eve message -> ../verification.md
cd ../..

# Standalone: Fireside Cryptograms
cd standalone/fireside-cryptograms/src
PYTHONHASHSEED=0 python3 master.py   # generate 200 unique cryptograms -> ../data.json
python3 build.py      # -> ../interior.pdf and ../build-info.json
python3 cover.py      # -> ../cover.pdf, ../cover-info.json and ../tmp/cover-guides.pdf
python3 verify.py     # independent dictionary solver uniqueness check -> ../verification.md
```

The fonts come from system paths: `/usr/share/fonts/truetype/sand-box/google/` (Crimson Text, Playfair Display SC, IBM Plex Sans Condensed) and DejaVu Sans. Change `G` in `build.py` if your fonts are somewhere else.

See [ideas-log.md](ideas-log.md) for ideas that have already been built or evaluated.
