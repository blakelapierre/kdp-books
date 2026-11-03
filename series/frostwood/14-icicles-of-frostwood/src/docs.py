"""Writes ../README.md (phone-friendly KDP paperback checklist) and ../listing.md from the built files,
so every number (pages, spine, cover size, printing cost, royalty) comes from build-info.json / cover-info.json."""
import json
from gen import BANDS
D = json.load(open("../data.json")); info = json.load(open("../build-info.json")); cov = json.load(open("../cover-info.json"))
ver = open("../verification.md").read()
PAGES = info["pages"]; marks = info["marks"]
NP = sum(len(D[b]) for b in ("Easy", "Medium", "Hard", "Expert"))
cnt = {b: len(D[b]) for b in ("Easy", "Medium", "Hard", "Expert")}
PRICE = 9.99
PRINT = 2.30 if 24 <= PAGES <= 110 else round(1.00 + 0.012 * PAGES, 3)
ROY = round(0.60 * PRICE - PRINT, 2)
print_txt = "$2.30 flat (24–110 pages)" if PRINT == 2.30 else f"$1.00 + {PAGES} × $0.012 = ${PRINT:.3f}"
SLUG = "frostwood-14-icicles-of-frostwood"
BASE = "https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/14-icicles-of-frostwood/"
tr = {b: (min(p["grade"]["trials"] for p in D[b]), max(p["grade"]["trials"] for p in D[b])) for b in ("Hard", "Expert")}
allpass = "ALL CHECKS PASSED" in ver
SUB = f"{NP} Futoshiki Logic Puzzles for Adults and Teens: Easy to Expert More-or-Less Number Puzzles with Solutions"
pv = lambda name, label: f"[{label}]({BASE}previews/{name})"
P = lambda k: marks[k]
DESC = f"""<b>On the coldest nights of the winter, icicles hang from every eave in Frostwood: the lodge porch, the village cottages, the station canopy and the frozen falls below the peaks. The village children sort them by length, one of each in every row and every column, and leave little signs between them to show which is the longer.</b>

{NP} of their grids are left, with only a few lengths and signs filled in. Every grid is a <b>Futoshiki</b> puzzle (also called More or Less, or Inequality). Fill in the numbers so that none repeats in any row or column, and every sign between two squares points to the smaller number.

Every puzzle has <b>exactly one solution</b>, checked by computer, and every one can be solved by logic alone, with <b>no guessing</b>.

<b>Inside you'll find:</b>
<ul>
<li>{NP} Futoshiki puzzles in four parts, in order of difficulty</li>
<li>{cnt['Easy']} Easy (5×5) and {cnt['Medium']} Medium (6×6), two per page</li>
<li>{cnt['Hard']} Hard (7×7) and {cnt['Expert']} Expert (8×8), one per page</li>
<li>Big, clear squares with room for pencil notes</li>
<li>A how-to-play guide with a fully worked example and the key solving tricks</li>
<li>Complete solutions at the back</li>
<li>6 × 9 inch paperback, easy to carry and easy to write in</li>
<li>Black-and-white ink illustrations: a frontispiece of the lodge seen from its icicled porch, a scene opening each section and small drawings on the puzzle pages</li>
</ul>

From the Lodge Eaves to the High Meadows, the puzzles grow step by step. First you'll follow the signs and fill the squares with only one number left. Then you'll spot pairs of squares that shut other numbers out. By the end you'll be asking “what if this square were a 5?” and following it until something breaks.

Book fourteen of the cozy Frostwood Puzzle Books. A good fit for adults, teens and families who enjoy Futoshiki, Sudoku, KenKen, logic puzzles and brain teasers, and a calm, screen-free winter gift.

Sharpen a pencil, pour some cocoa, and start sorting."""
assert len(DESC) < 4000
KW = ["futoshiki puzzle book", "futoshiki puzzles for adults", "more or less logic puzzles", "logic puzzles with solutions",
      "number puzzles like sudoku", "winter puzzle book for adults", "cozy puzzle gift for puzzle lovers"]
assert all(len(k) <= 50 for k in KW)
spine = cov["spine_in"]; cw = cov["width_in"]

readme = f"""# The Icicles of Frostwood: KDP publishing checklist (paperback)

**Status: print-ready, not yet published.** Nothing has been submitted to KDP.
**Format: Paperback** (built for the Tuesday paperback slot; Frostwood book 14).

| | |
|---|---|
| Format | **Paperback** |
| Series | A Frostwood Puzzle Book, **book 14** |
| Puzzles | **{NP}** Futoshiki puzzles: {cnt['Easy']} Easy 5×5, {cnt['Medium']} Medium 6×6, {cnt['Hard']} Hard 7×7, {cnt['Expert']} Expert 8×8 |
| Pages | **{PAGES}** |
| Trim | 6 × 9 in |
| Interior | Black & white on **white** paper, **no bleed** |
| Cover finish | **Matte** (recommended) |
| Price | **${PRICE:.2f}** USD |
| Printing cost | {print_txt} ≈ ${PRINT:.2f} |
| Royalty (60%) | 0.60 × {PRICE:.2f} − {PRINT:.3f} = **${ROY:.2f}** per copy |
| Spine | {PAGES} × 0.002252 = {spine:.4f} in |
| Full cover | {cw:.4f} × 9.25 in (with 0.125 in bleed) |

## 1. Files (download to your phone)

- **Interior PDF** (phone-friendly name first): [view]({BASE}interior-{SLUG}.pdf) · [download]({BASE}interior-{SLUG}.pdf?raw=true)  
  `interior-{SLUG}.pdf` (same bytes as `{SLUG}-interior.pdf`: [view]({BASE}{SLUG}-interior.pdf) · [download]({BASE}{SLUG}-interior.pdf?raw=true))
- **Cover PDF** (paperback wrap): [view]({BASE}cover-{SLUG}.pdf) · [download]({BASE}cover-{SLUG}.pdf?raw=true)  
  `cover-{SLUG}.pdf` (same bytes as `{SLUG}-cover.pdf`: [view]({BASE}{SLUG}-cover.pdf) · [download]({BASE}{SLUG}-cover.pdf?raw=true))
- Previews: {pv('cover-full-wrap.png', 'cover')} · {pv('cover-with-kdp-guides.png', 'cover with KDP guides')} · {pv('interior-p003.png', 'title page')} · {pv('interior-p%03d.png' % P('howto'), 'how to play')} · {pv('interior-p%03d.png' % (P('howto') + 1), 'worked example')} · {pv('interior-p%03d.png' % (P('Easy') + 1), 'Easy page')} · {pv('interior-p%03d.png' % (P('Medium') + 1), 'Medium page')} · {pv('interior-p%03d.png' % (P('Hard') + 1), 'Hard page')} · {pv('interior-p%03d.png' % (P('Expert') + 1), 'Expert page')} · {pv('interior-p%03d.png' % (P('solutions') + 1), 'solutions page')} · {pv('interior-p%03d.png' % P('about'), 'thank you / also by')}

The repo is private, so be signed in to GitHub in your phone's browser. Tap *download*, then pick the file from Downloads in the KDP upload box.

## 2. Create the paperback in KDP

1. **kdp.amazon.com** → **Bookshelf** → **+ Create** → **Paperback**.
2. Fill in **Paperback Details** with the copy-paste blocks in section 3.
3. **Paperback Content**: ISBN → **Get a free KDP ISBN**; Publication date → leave blank; Print options → **Black & white interior with white paper**, trim **6 × 9 in**, **No bleed**, cover finish **Matte**.
4. **Manuscript** → upload `interior-{SLUG}.pdf`.
5. **Book cover** → **Upload a cover you already have** → upload `cover-{SLUG}.pdf`.
6. Answer the **AI-generated content** questions (section 4).
7. **Launch Previewer** → check every item in section 5 → **Approve** → **Save and Continue**.
8. **Paperback Rights & Pricing**: Territories **All territories**; Primary marketplace **Amazon.com**; list price **${PRICE:.2f}** (60% royalty, about ${ROY:.2f}/copy). Expanded Distribution is optional (40% rate).
9. Order a **proof copy** first if you can (section 5), then **Publish Your Paperback Book**.

## 3. Copy-paste fields

**Language:** English

**Book title**
```
The Icicles of Frostwood
```

**Subtitle**
```
{SUB}
```

**Series name** (number **14**)
```
A Frostwood Puzzle Book
```
Series number: `14`

**Edition number:** leave blank

**Author** (first name / last name). No co-authors or contributors.
```
Blake
```
```
La Pierre
```

**Description** (KDP accepts this HTML; {len(DESC):,} characters, limit 4,000)
```html
{DESC}
```

**Keywords** (one per box)
""" + "\n".join(f"{i}.\n```\n{k}\n```" for i, k in enumerate(KW, 1)) + f"""

**Categories** (pick up to 3 in the picker)
- Humor & Entertainment › Puzzles & Games › Logic & Brain Teasers
- Humor & Entertainment › Puzzles & Games › Puzzles
- Humor & Entertainment › Puzzles & Games › Math Games (optional third)

**Primary audience:** sexually explicit content → **No**; reading age → leave blank (or 13+).
**Low-content book:** No. **Large-print:** leave unchecked.

## 4. AI-generated content answers

KDP asks this on the Content page. Truthful answers for this book:

- **Texts: Yes.** The text (how-to pages, framing story, descriptions) was written with AI. Choose *Entire work* and the editing level that matches how much you changed it.
- **Images: Yes.** The cover and interior illustrations were drawn by AI-written code. Choose *Entire work* and the editing level that fits.
- **Translations: No.**
- The puzzles were generated and checked by AI-written code (covered by the text answer).

## 5. Proof check (Previewer or printed proof)

- [ ] Page count in the KDP previewer matches **{PAGES}** and the spine text sits centred on the spine with no wrap-around onto the covers.
- [ ] Numbers are easy to read on every band, including the smaller Medium grids (6×6, two per page), and every < > sign between squares is clear and points the right way.
- [ ] Each square has room for a written number plus small pencil notes in a corner.
- [ ] Easy and Medium pages: both puzzles fit on the page with clear space between them, and nothing touches the running head or page number.
- [ ] Solutions pages: the given numbers (black) are easy to tell from the filled-in ones (gray), and the numbers stay readable on the small Expert solutions (6 per page).
- [ ] The frontispiece (page 2) and title-page art print as crisp black ink: solid blacks are even, no gray haze, no banding.
- [ ] Vignettes on the Hard and Expert pages sit between the grid and the Started / Finished line without touching either.
- [ ] Blank pages show only the small centred vignette; section openers start on right-hand pages.
- [ ] Author on the front cover, spine and title page reads **Blake La Pierre** only.
- [ ] The back-cover barcode box is empty (KDP prints the barcode there), and the sample puzzle card on the back is clear of it.

## Illustrations in this edition

- Half-title vignette (a row of icicles hanging from a snowy eave)
- Full-page framed frontispiece: the lodge seen from under its icicled porch eave on a still evening (caption: *Icicles along the lodge porch on a still winter evening*)
- Title-page art: the lodge on its hill under the moon, framed by an icicled eave above
- 4 section-opener scenes: the lodge eaves (icicles along the lodge eaves, a bench and a mug by the door), the village lanes (cottages hung with icicles, lamps, signpost, sled), the station yard (the platform under a long icicled canopy, rails, water tower), the high meadows (a frozen waterfall below the peaks and a hut beside it)
- 5 rotating vignettes (icicles on an eave, a lantern post, a cocoa mug, a snowman, a cottage) under the {cnt['Hard'] + cnt['Expert']} full-page Hard and Expert puzzles
- Thank-you page art and a blank-page vignette

All illustrations are black ink on white, 300 DPI, no gray washes, inside the page margins (no bleed). Sources: [illustrations/](illustrations/), drawn by [src/illustrations.py](src/illustrations.py) with the shared house-style library [src/inkart.py](src/inkart.py) (identical to the other Frostwood books). No people appear in any scene.

## Verification

All {NP} puzzles (and the worked example): exactly one solution, found by both an independent SAT solver (CaDiCaL via python-sat) and an independent plain backtracking counter, and equal to the stored answer. Each fits its band: Easy and Medium need no what-if steps (Easy needs only the basic rules; Medium needs pairs or chains), Hard needs {tr['Hard'][0]} to {tr['Hard'][1]} one-step "what if?" deductions and Expert {tr['Expert'][0]} to {tr['Expert'][1]}. Generation is deterministic (fixed seeds, `PYTHONHASHSEED=0`). Full report: [verification.md](verification.md) ({'all checks passed' if allpass else 'SEE FAILURES'}).

## More detail

- [listing.md](listing.md): the full listing draft with competition, pricing and verification notes
- Rebuild commands: see the [main README](../../../README.md#rebuilding-a-book)
"""
open("../README.md", "w").write(readme)

listing = f"""# KDP listing draft: *The Icicles of Frostwood*

> Draft only. Nothing has been published or submitted to KDP. Step-by-step publishing checklist: [README.md](README.md).

**Format: Paperback** (6 × 9 in, built for the Tuesday paperback slot).

## Title
**The Icicles of Frostwood**

## Subtitle
**{SUB}**

## Author
**Blake La Pierre** (matches the title page, the copyright page, the front cover and the spine).

## Series
Book 14 of **"A Frostwood Puzzle Book"**. The cover and title page already say "A Frostwood Puzzle Book". If you set up the series on KDP, add this book as number 14. The "Also by" page lists books 1–11 and 13.

## Description ({len(DESC):,} characters; KDP limit is 4,000)
KDP accepts limited HTML (`<b>`, `<i>`, `<ul>`, `<li>`, `<br>`) in the description box.

```html
{DESC}
```

## Keywords (7 slots)
""" + "\n".join(f"{i}. {k}" for i, k in enumerate(KW, 1)) + f"""

## Suggested categories (pick 2–3 in KDP's category picker)
- Humor & Entertainment › Puzzles & Games › Logic & Brain Teasers
- Humor & Entertainment › Puzzles & Games › Puzzles
- Humor & Entertainment › Puzzles & Games › Math Games (optional third)

## Why Futoshiki, and the competition
Futoshiki had not been used anywhere in the Frostwood series. It fits Frostwood well: each square holds an icicle of a given length, and the signs show which of two neighbouring icicles is longer. It is close to Sudoku, so it appeals to a wide audience. Public Amazon listings seen in a web search on 2026-11-03 (figures as shown in the search results; nothing else was checked):

| Book | Details shown | Price | Rating |
|---|---|---|---|
| *Futoshiki Puzzle Book: 500 Puzzles with Full Solution, Easy to Hard* (NavZ Books, B09L3RC9MN) | 136 pp, 4×4 to 8×8, Nov 2021 | $9.99 | 4.9★ / 16 |
| *Futoshiki Puzzle Book for Adults Volume 1: 207 Easy to Hard* (Willie Howard, B0B4G1XWYY) | 127 pp, 4×4 to 9×9, Jun 2022 | $6.99 | none shown |
| *Futoshiki Puzzle Book: 208 Puzzles - Easy, Medium and Hard* (VisCulture Publishing, B091G579DR) | 8.5 × 11, 101 pp, 5×5 / 7×7 / 9×9, Mar 2021 | $9.99 | 4.1★ / 10 |
| *Hard Futoshiki Puzzles: A 9x9 Logic Game Collection* (Willmer Piedra, B0GSN3G4DK) | 8.5 × 11, 154 pp, Mar 2026 | not shown in USD | none shown |
| *Futoshiki Easy 6x6 Puzzles and Solutions* (Genius Publishing, B09RWJ3C7G) | 8.5 × 11, 170 pp, 400 puzzles, Feb 2022 | $9.98 | none shown |

Sales ranks weren't shown, so demand is unmeasured. The competition is mostly plain, unthemed grids with no teaching pages. **Gap:** a cozy, illustrated, themed Futoshiki book with a smooth Easy-to-Expert curve (5×5 up to 8×8), a worked example, and computer-verified unique, no-guess puzzles at $9.99.

## Print specs used
- Trim 6 × 9 in (regular trim), black ink on **white** paper, no bleed interior, matte cover
- Interior: **{PAGES} pages** (includes the black-and-white ink illustrations: solid black line art on white, 300 DPI, no gray washes), grayscale only, all fonts embedded and subset (Crimson Text, Playfair Display SC, IBM Plex Sans Condensed, and DejaVu Sans for the ❄ symbol). Mirrored margins: inside 0.75 in, outside 0.55 in, top 0.70 in, bottom 0.75 in, above KDP's minimums.
- Layout: Easy (5×5) and Medium (6×6) two per page; Hard (7×7) and Expert (8×8) one per page with a vignette and a Started / Finished line. Solutions: 12 per page (Easy, Medium), 6 per page (Hard, Expert); givens in black, filled-in numbers in gray.
- Spine width: {PAGES} × 0.002252 in = **{spine:.4f} in** (spine text is allowed; KDP recommends 79+ pages)
- Full-wrap cover: 0.125 + 6 + {spine:.4f} + 6 + 0.125 = **{cw:.4f} in × 9.25 in**. The barcode area (2 × 1.2 in, lower right of the back cover, 0.25 in in from the trim) has no text or art.

## Suggested price
**${PRICE:.2f} USD** (Amazon.com), the lowest price that earns the 60% royalty rate, and the same price as the NavZ and VisCulture Futoshiki books.

## Royalty math (from the actual {PAGES}-page interior)
KDP black-ink printing for white paper: **{print_txt}** per copy.
Paperback royalty at 60%: **0.60 × ${PRICE:.2f} − ${PRINT:.3f} = ${ROY:.2f}** per copy sold on Amazon.com (expanded distribution and other marketplaces pay less).

## Files to upload
- Interior: [`{SLUG}-interior.pdf`]({SLUG}-interior.pdf) ({PAGES} pages)
- Cover: [`{SLUG}-cover.pdf`]({SLUG}-cover.pdf) (full wrap, {cw:.4f} × 9.25 in; see `cover-info.json`)
- Illustration sources: [`illustrations/`](illustrations/) (drawn by `src/illustrations.py`)

## Things to decide or do before publishing
- **Author field**: **Blake La Pierre** only. Remove any other co-author/contributor if KDP shows one.
- **AI-content disclosure applies** (text and images; see README section 4).
- **ISBN**: KDP's free ISBN. KDP prints the barcode in the blank area on the back cover.
- **Proof copy**: check that the < > signs between squares print crisply, and that the 6×6 Medium grids (two per page) leave enough room to write in.
- **Page count**: if it changes, rebuild the cover (`src/cover.py` reads `build-info.json`) and rerun `src/docs.py`.

## Verification
Every puzzle was checked by an independent SAT solver (CaDiCaL via python-sat) and by an independent backtracking counter (`src/fut_bt.py`, which shares no code with the generator). All {NP} puzzles, plus the worked example, have exactly one solution, and it matches the stored answer. Each fits its band, graded by the generator's step-by-step logic solver (`src/futoshiki.py`): Easy needs only the basic rules, Medium needs pairs or sign chains, Hard needs {tr['Hard'][0]}–{tr['Hard'][1]} what-if steps and Expert {tr['Expert'][0]}–{tr['Expert'][1]}. Full report: [verification.md](verification.md).

## Rebuild
From `src/`: `PYTHONHASHSEED=0 python3 master.py` (puzzles → `data.json`), `python3 verify.py`, `python3 illustrations.py`, `python3 build.py`, `python3 cover.py`, `python3 check_margins.py`, `python3 docs.py`, then copy the two PDFs to the `interior-…` / `cover-…` names.
"""
open("../listing.md", "w").write(listing)
print("pages", PAGES, "print", PRINT, "royalty", ROY, "desc", len(DESC))
