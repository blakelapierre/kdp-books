# Side by Side in Frostwood: KDP ebook publishing checklist

**Status: ebook-ready, not yet published.** Nothing has been submitted to KDP.

| | |
|---|---|
| Format | **Kindle ebook** (EPUB 3, reflowable, phone-friendly, nothing to write in) |
| Series | **A Frostwood Puzzle Book** · number **15** |
| Puzzles | **120** line-up logic puzzles (30 Easy · 30 Medium · 30 Hard · 30 Expert) |
| Type | Line-up / seating-order logic: 4 to 7 people in a numbered row; short clues; work out who has which place |
| Length | ebook, no page count (EPUB 969,199 bytes; 120 puzzles + 120 hints + 120 answers) |
| Author | **Blake La Pierre** |
| Price | **$3.99** USD (70% royalty option) |
| Printing cost | none (ebook) |
| Delivery fee (est.) | **$0.14** (969,199 bytes ≈ 0.925 MB × $0.15/MB) |
| Royalty (est.) | 0.70 × 3.99 − 0.14 = **$2.65** per sale on Amazon.com |

## 1. Files (download to your phone)

- **EPUB** (upload this one): [view](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/15-side-by-side-in-frostwood/frostwood-15-side-by-side-in-frostwood.epub) · [download](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/15-side-by-side-in-frostwood/frostwood-15-side-by-side-in-frostwood.epub?raw=true)  
  `frostwood-15-side-by-side-in-frostwood.epub`
- **Cover JPG** (1600 wide × 2560 tall, KDP's ideal ebook cover): [view](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/15-side-by-side-in-frostwood/frostwood-15-side-by-side-in-frostwood-cover.jpg) · [download](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/15-side-by-side-in-frostwood/frostwood-15-side-by-side-in-frostwood-cover.jpg?raw=true)  
  `frostwood-15-side-by-side-in-frostwood-cover.jpg`
- Previews: [phone pages](previews/phone-pages.png) · [cover thumbnail](previews/cover-thumb.png)
- Listing text: [listing.md](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/15-side-by-side-in-frostwood/listing.md) · Verification: [verification.md](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/15-side-by-side-in-frostwood/verification.md)

The repo is private, so be signed in to GitHub in your phone's browser. Tap *download*, then pick the file from Downloads in the KDP upload box.

## 2. Create the Kindle ebook in KDP

1. **kdp.amazon.com** → **Bookshelf** → **+ Create** → **Kindle eBook**.
2. Fill in **Kindle eBook Details** with the copy-paste blocks in section 3.
3. **Kindle eBook Content**:
   - Manuscript → upload `frostwood-15-side-by-side-in-frostwood.epub`
   - Cover → **Upload a cover you already have** → upload `frostwood-15-side-by-side-in-frostwood-cover.jpg`
4. Answer the **AI-generated content** questions (section 4).
5. **Launch Previewer** (phone + tablet + Kindle) → check every item in section 5 → **Save and Continue**.
6. **Kindle eBook Pricing**: Territories **All territories**; Primary marketplace **Amazon.com**; royalty plan **70%**; list price **$3.99**.
7. **KDP Select:** your choice. Enrolling puts the book in Kindle Unlimited but makes it Amazon-exclusive for 90 days (no other ebook stores). It is optional for a puzzle ebook like this.
8. Confirm the on-screen delivery fee is close to **$0.14** (Amazon measures its converted file, so small differences are normal).
9. **Publish Your Kindle eBook**.

## 3. Copy-paste fields

**Language:** English

**Book title**
```
Side by Side in Frostwood
```

**Subtitle**
```
120 Cozy Line-Up Logic Puzzles for Kindle: Who Sits Where? Winter Seating and Ordering Brain Teasers, Easy to Expert, with Tap-to-Jump Hints and Answers
```

**Series name** (number **15**). Use the same series name as the live Frostwood books so they link up on Amazon:
```
A Frostwood Puzzle Book
```
Series number: `15`

**Edition number:** leave blank

**Author** (first name / last name). No co-authors or contributors.
```
Blake
```
```
La Pierre
```

**Description**, **keywords** and **categories**: copy them from [listing.md](listing.md) (the description block is HTML that KDP accepts).

**Keywords** (7 boxes)
```
seating logic puzzles for adults
```
```
who sits where brain teasers
```
```
logic puzzles for kindle
```
```
brain teasers for adults with answers
```
```
cozy winter puzzle book
```
```
ordering and lineup logic puzzles
```
```
deduction puzzles for teens
```

**Categories:** Logic & Brain Teasers · Puzzles · Trivia (all under Kindle eBooks › Humor & Entertainment › Puzzles & Games).

**Publishing rights:** I own the copyright. **Adult content:** No. **Reading age:** leave blank (or 10+).

## 4. AI-generated content answers

- **Text:** Yes. The puzzles were generated and verified by code, and the framing text was written with AI assistance and reviewed.
- **Images:** Yes. The black-and-white illustrations and the cover were drawn by code (procedural ink line art and a programmatic cover), not a generative image model.
- **Translations:** No.

## 5. Proof / preview checks

In the online Previewer (and on your phone after it's live):

- [ ] Cover fills the thumbnail; title and author readable
- [ ] Front matter: frontispiece, title page, copyright © 2026 Blake La Pierre, contents, how to play with the worked example (answer: 1 Dov · 2 Bram · 3 Clara · 4 Ada)
- [ ] Each puzzle reads cleanly on a phone: cast line in italics, numbered clue list, "Who has which …?"
- [ ] Tap **Need a hint?** on a few puzzles → lands on the right hint; **Back to the puzzle** returns
- [ ] Tap **Show answer** → lands on the right line-up with every clue ticked; **Back to the puzzle** returns
- [ ] Section openers (lodge peg rail, village cottages, railway carriages, mountain sledges) and the small vignettes display in black and white
- [ ] "Also by" lists Frostwood books 1–11, 13 and 14
- [ ] No Christmas-specific content; no violence

## 6. Verification and rebuild

All 120 puzzles pass: exactly one line-up fits each puzzle (it matches the printed answer), every clue is needed, no puzzle repeats, and each puzzle sits inside its band. The independent verifier reads the **printed English** of every clue back into a rule, so a wording slip would fail. Full table: [verification.md](verification.md).

| Band | Puzzles | People | Clue kinds | Depth | "Suppose…" tests |
|---|---|---|---|---|---|
| Easy · the Lodge | 30 | 4 | has / not place k, end, not end, odd/even, next to, directly left, somewhere left | 0 (one clue at a time) | 0 |
| Medium · the Village | 30 | 5 | all, incl. not next to, gaps and between (at most 1 "has place k") | 0 | 0 |
| Hard · the Railway | 30 | 6 | all except "has place k" | 1 | 1–2 |
| Expert · the Mountain | 30 | 7 | all except "has place k" | 1 | 3–6 |

```bash
cd series/frostwood/15-side-by-side-in-frostwood/src
PYTHONHASHSEED=0 python3 master.py   # gen → verify → illustrations → cover → epub (about 15 seconds)
# optional EPUBCheck: EPUBCHECK_JAR=/path/epubcheck.jar JAVA=/path/java PYTHONHASHSEED=0 python3 master.py
```

Seed `20261119` (recorded in `build-info.json`). `gen.py` writes a byte-identical `data.json` every run. **EPUBCheck 5.1.0: 0 fatals / 0 errors / 0 warnings** (EPUB 3.3 rules).
