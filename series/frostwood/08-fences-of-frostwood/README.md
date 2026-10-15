# Fences of Frostwood: KDP publishing checklist (HARDCOVER)

Format: hardcover

**Status: print-ready HARDCOVER, not yet published.** Nothing has been submitted to KDP.
**Format: Hardcover** (case laminate; built for the Thursday Frostwood hardcover slot; Frostwood book 8).

| | |
|---|---|
| **Format** | **Hardcover** (case laminate) |
| Series | A Frostwood Puzzle Book, **book 8** |
| Puzzles | **100** Slitherlink (Loop the Loop / Fences) puzzles: 20 Easy 6×6, 30 Medium 7×7, 30 Hard 8×8, 20 Expert 10×10 |
| Pages | **88** |
| Trim | 6 × 9 in |
| Interior | Black & white on **white** paper, **no bleed** |
| Cover finish | **Matte** (recommended) |
| Price | **$17.99** USD |
| Printing cost | **$6.80** flat (black-ink hardcover, regular trim, 75–108 pages, Amazon.com) |
| Royalty (60%) | 0.60 × 17.99 − 6.80 = **$3.99** per copy |
| Spine (hardcover) | 88 × 0.002252 + 0.189 = **0.3872 in** |
| Full cover | **13.9632 × 10.418 in** (includes 0.591 in wrap on every edge) |

Printing cost source: KDP Help, [Hardcover Printing Cost](https://kdp.amazon.com/en_US/help/topic/GHT976ZKSKUXBB6H) (fetched 2026-10-15): "Black ink hardcover books with 75 - 108 pages only incur the fixed cost", **$6.80 USD per book, no per-page charge** on Amazon.com for regular trim. (At 110+ pages it would be $5.65 + $0.012 × pages.) Cover wrap / hinge dimensions use the same formula as *The Advent Clock* hardcover (`standalone/01-the-advent-clock/src/cover_hardcover.py`) and KDP's [Create a Hardcover Cover](https://kdp.amazon.com/help/topic/GDTKFJPNQCBTMRV6) help (0.591 in wrap, 0.394 in hinge, boards = trim + 0.197 W / + 0.236 H, spine = pages × 0.002252 + 0.189).

## 1. Files (download to your phone)

- **Interior PDF** (phone-friendly name first): [view](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/08-fences-of-frostwood/interior-frostwood-08-fences-of-frostwood.pdf) · [download](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/08-fences-of-frostwood/interior-frostwood-08-fences-of-frostwood.pdf?raw=true)  
  `interior-frostwood-08-fences-of-frostwood.pdf` (same bytes as `frostwood-08-fences-of-frostwood-interior.pdf`)
- **Cover PDF** (HARDCOVER wrap): [view](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/08-fences-of-frostwood/cover-frostwood-08-fences-of-frostwood.pdf) · [download](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/08-fences-of-frostwood/cover-frostwood-08-fences-of-frostwood.pdf?raw=true)  
  `cover-frostwood-08-fences-of-frostwood.pdf` (same bytes as `frostwood-08-fences-of-frostwood-cover.pdf`)
- Previews: [cover wrap](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/08-fences-of-frostwood/previews/cover-full-wrap.png) · [cover with KDP guides](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/08-fences-of-frostwood/previews/cover-with-kdp-guides.png) · [frontispiece](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/08-fences-of-frostwood/previews/interior-p002.png) · [title](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/08-fences-of-frostwood/previews/interior-p003.png) · [how to play](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/08-fences-of-frostwood/previews/interior-p007.png) · [worked example](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/08-fences-of-frostwood/previews/interior-p008.png) · [Easy opener](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/08-fences-of-frostwood/previews/interior-p009.png) · [Easy page](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/08-fences-of-frostwood/previews/interior-p010.png) · [Medium page](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/08-fences-of-frostwood/previews/interior-p022.png) · [Hard page](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/08-fences-of-frostwood/previews/interior-p038.png) · [Expert page](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/08-fences-of-frostwood/previews/interior-p054.png) · [solutions](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/08-fences-of-frostwood/previews/interior-p076.png) · [Expert solutions](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/08-fences-of-frostwood/previews/interior-p084.png) · [thank you / also by](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/08-fences-of-frostwood/previews/interior-p087.png)

The repo is private, so be signed in to GitHub in your phone's browser. Tap *download*, then pick the file from Downloads in the KDP upload box.

## 2. Create the HARDCOVER in KDP

1. **kdp.amazon.com** → **Bookshelf** → **+ Create** → **Hardcover**.
2. Fill in **Hardcover Details** with the copy-paste blocks in section 3.
3. **Hardcover Content**: ISBN → **Get a free KDP ISBN**; Publication date → leave blank; Print options → **Black & white interior with white paper**, trim **6 × 9 in**, **No bleed**, cover finish **Matte**.
4. **Manuscript** → upload `interior-frostwood-08-fences-of-frostwood.pdf`.
5. **Book cover** → **Upload a cover you already have** → upload `cover-frostwood-08-fences-of-frostwood.pdf` (this is the **hardcover** wrap with hinge and wrap margin, not a paperback cover).
6. Answer the **AI-generated content** questions (section 4).
7. **Launch Previewer** → check every item in section 5 → **Approve** → **Save and Continue**.
8. **Hardcover Rights & Pricing**: Territories **All territories**; Primary marketplace **Amazon.com**; list price **$17.99** (60% royalty, about $3.99/copy).
9. Order a **proof copy** first if you can (section 5), then **Publish Your Hardcover Book**.

## 3. Copy-paste fields

**Language:** English

**Book title**
```
Fences of Frostwood
```

**Subtitle**
```
100 Slitherlink Logic Puzzles for Adults and Teens: Easy to Expert Fence-Loop Puzzles with Solutions
```

**Series name** (number **8**)
```
A Frostwood Puzzle Book
```
Series number: `8`

**Edition number:** leave blank

**Author** (first name / last name). No co-authors or contributors.
```
Blake
```
```
La Pierre
```

**Description** (KDP accepts this HTML; 2,001 characters, limit 4,000)
```html
<b>After the deepest snow in years, the timber fences around Frostwood have vanished under the drifts: the village garden lots, the lodge meadow paddocks, the mill-yard plots and the high orchard terraces. Only the tops of the posts still show, and on some of them the lot-keeper has hung a little number.</b>

100 maps are left. Every map is a <b>Slitherlink</b> puzzle (also called Loop the Loop or Fences). Draw one closed fence from post to post, across or down, so that every number tells how many of the four sides of its square are fence. No loose ends, no branches, and no second loop.

Every puzzle has <b>exactly one solution</b>, checked by computer, and every one can be solved by logic alone, with <b>no guessing</b>.

<b>Inside you'll find:</b>
<ul>
<li>100 Slitherlink fence-loop puzzles in four parts, in order of difficulty</li>
<li>20 Easy (6×6), 30 Medium (7×7) and 30 Hard (8×8), two per page</li>
<li>20 Expert (10×10), one big map per page</li>
<li>Large, clear dot grids with plenty of room to draw and to mark ruled-out edges</li>
<li>A how-to-play guide with a fully worked example and the key solving tricks</li>
<li>Complete solutions at the back</li>
<li>6 × 9 inch case-laminate hardcover, sturdy and made to give</li>
<li>Black-and-white ink illustrations: a frontispiece of the snowed-under village, a scene opening each section and small drawings on the puzzle pages</li>
</ul>

From the Village Lots to the High Orchard, the puzzles grow step by step. First you'll count the sides of each square and follow the fence from post to post. Then you'll spot the quick “what if?” that breaks in a move or two. By the end you'll be following a pencilled fence all the way across the map until something gives.

Book eight of the cozy Frostwood Puzzle Books. A good fit for adults, teens and families who enjoy Slitherlink, logic puzzles, Sudoku, nonograms and brain teasers, and a calm, screen-free winter gift.

Sharpen a pencil, pour some cocoa, and find the buried fences.
```

**Keywords** (one per box)
1.
```
slitherlink puzzle book
```
2.
```
loop the loop puzzles for adults
```
3.
```
fences logic puzzles with solutions
```
4.
```
japanese logic puzzle book
```
5.
```
brain teasers for teens and adults
```
6.
```
winter puzzle book hardcover gift
```
7.
```
cozy puzzle gift for puzzle lovers
```

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

- [ ] Page count in the KDP previewer matches **88** and the spine text sits centred on the hardcover spine with no wrap onto the boards.
- [ ] The cover file is the **hardcover** wrap (13.96 × 10.42 in), not a paperback wrap: check the hinge gaps and wrap margins in the previewer. Nothing important sits in the 0.591 in wrap.
- [ ] Numbers and posts are easy to read on every band, including the 8×8 Hard maps (two per page) and the 10×10 Expert maps; the posts print as crisp dots.
- [ ] Two-per-page pages (Easy, Medium, Hard): both maps fit with clear space between them, and nothing touches the running head or page number.
- [ ] Solutions pages: the fence line is bold and easy to follow, even on the 8×8 solutions (12 per page) and the 10×10 solutions (6 per page).
- [ ] The frontispiece (page 2) and title-page art print as crisp black ink: solid blacks are even, no gray haze, no banding.
- [ ] Vignettes on the Expert pages sit between the map and the Started / Finished line without touching either.
- [ ] Blank pages show only the small centred vignette; section openers start on right-hand pages.
- [ ] Author on the front cover, spine and title page reads **Blake La Pierre** only.
- [ ] The back-cover barcode box is empty (KDP prints the barcode there), and the sample puzzle card on the back is clear of it.

## Illustrations in this edition

- Half-title vignette (numbered fence posts poking out of a drift)
- Full-page framed frontispiece: the snowed-under village below the lodge, with rows of numbered posts where the lot fences used to be (caption: *The posts above the drifts*)
- Title-page art: the lodge on its hill above the meadow, a winding post-and-rail fence and a row of buried posts
- 4 section-opener scenes: the village lots (cottages, picket fences, the pump, a bird table), the lodge meadow (split-rail fences, hay barn, five-bar gate, sledge), the mill yard (mill and wheel, cart shed, log stacks, yard gate, saw-horse), the high orchard (terraces of bare apple trees, a ladder, bee skeps)
- 6 rotating vignettes (numbered posts, a field gate, a picket fence and bird table, logs and a saw-horse, an orchard tree with a ladder, a stile by moonlight) under the 20 full-page Expert puzzles
- Thank-you page art and a blank-page vignette

All illustrations are black ink on white, 300 DPI, no gray washes, inside the page margins (no bleed). Sources: [illustrations/](illustrations/), drawn by [src/illustrations.py](src/illustrations.py) with the shared house-style library [src/inkart.py](src/inkart.py) (copied from book 7). No people appear in any scene.

## Verification

All 100 puzzles (and the worked example): exactly one solution, found by both an independent SAT solver (CaDiCaL via python-sat, with single-loop cuts) and an independent backtracking counter, and equal to the stored fence. Every puzzle is solvable by logic alone (the step-by-step solver finishes with no guessing) and fits its band: Easy needs only the counting rules; Medium also needs short what-ifs (a guess that breaks within 8 forced moves); Hard needs 1–3 long what-ifs; Expert 3–12. Generation is deterministic (fixed seeds, `PYTHONHASHSEED=0`); a second run produced a byte-identical `data.json`. Full report: [verification.md](verification.md).

## More detail

- [listing.md](listing.md): the full listing draft with research, pricing and verification notes
- Rebuild: `cd src && PYTHONHASHSEED=0 python3 master.py && python3 verify.py && python3 illustrations.py && python3 build.py && python3 cover.py && python3 check_margins.py`, then copy the two PDFs to the `interior-…` / `cover-…` names.
