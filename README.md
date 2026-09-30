# KDP Books

Source, print files and listing drafts for Blake La Pierre's Amazon KDP paperback puzzle books. Each book has its own folder.

| # | Title | Author | Status | Pages | Price | Folder |
|---|-------|--------|--------|-------|-------|--------|
| 1 | *The Thief Stayed the Night*: A Snowbound Hotel Mystery Puzzle Book (12 cozy elimination cases) | Blake La Pierre | Draft, print-ready. Not yet published or submitted to KDP | 134 | $9.99 | [the-thief-stayed-the-night/](the-thief-stayed-the-night/) |
| 2 | *Frostwood Express*: 200 Train Tracks Logic Puzzles (Easy to Expert) | Blake La Pierre | Draft, print-ready. Not yet published or submitted to KDP | 192 | $9.99 | [frostwood-express/](frostwood-express/) |

Both books are 6 × 9 in paperbacks with black ink on white paper, and they share a "Frostwood" setting. They could be linked on KDP as a series called "A Frostwood Puzzle Book".

## What's in each book folder

- `interior.pdf`: the interior file to upload to KDP
- `cover.pdf`: the full-wrap cover (back, spine and front)
- `listing.md`: listing draft with title, subtitle, description, keywords, categories, specs and pricing/royalty math
- `previews/`: PNG renders of the cover and some sample pages
- `data.json`: the generated puzzle data that the book is built from
- `build-info.json` / `cover-info.json`: page count, section page numbers and cover dimensions
- `clue-checks.md` (book 1) / `verification.md` (book 2): the report from the independent verification run
- `src/`: scripts for generating, building and verifying the book

## Rebuilding a book

Run the scripts from inside the book's `src/` folder. They read and write files in the book folder (`../`) using relative paths.

```bash
python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt

# Book 1: The Thief Stayed the Night
cd the-thief-stayed-the-night/src
python3 gen.py        # regenerate ../data.json from master.py (guest list) and clues.py (cases); optional arg: max seeds
python3 build.py      # -> ../interior.pdf and ../build-info.json (the story text is in stories.py)
python3 cover.py      # -> ../cover.pdf and ../cover-info.json (reads the page count)
python3 verify.py     # independent re-check -> ../clue-checks.md
cd ../..

# Book 2: Frostwood Express
cd frostwood-express/src
python3 master.py     # generate and grade the 200 puzzles -> ../data.json (tracks.py is the solver, gen.py sets the difficulty bands)
python3 build.py      # -> ../interior.pdf and ../build-info.json
python3 cover.py      # -> ../cover.pdf, ../cover-info.json and ../tmp/cover-guides.pdf
python3 verify.py     # checks each puzzle has one solution with a SAT solver (verify_sat.py) -> ../verification.md
```

The fonts come from system paths: `/usr/share/fonts/truetype/sand-box/google/` (Crimson Text, Playfair Display SC, IBM Plex Sans Condensed) and DejaVu Sans. Change `G` in `build.py` if your fonts are somewhere else.

See [ideas-log.md](ideas-log.md) for ideas that have already been built or evaluated.
