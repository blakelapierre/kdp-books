# The Lockboxes of Frostwood: KDP ebook publishing checklist

**Status: ebook-ready, not yet published.** Nothing has been submitted to KDP.

| | |
|---|---|
| Format | **Kindle ebook** (EPUB 3, reflowable, phone-friendly, nothing to write in) |
| Series | **A Frostwood Puzzle Book** · number **9** |
| Puzzles | **120** crack-the-code lockboxes (30 Easy · 35 Medium · 35 Hard · 20 Expert) |
| Type | Crack the code (number-lock deduction): tried codes with exact "right place / wrong place / nothing is right" notes |
| Length | ebook, no page count (EPUB 929,372 bytes; 120 boxes + 120 hints + 120 answers) |
| Author | **Blake La Pierre** |
| Price | **$3.99** USD (70% royalty option) |
| Printing cost | none (ebook) |
| Delivery fee (est.) | **$0.13** (929,372 bytes ≈ 0.887 MB × $0.15/MB) |
| Royalty (est.) | 0.70 × 3.99 − 0.13 = **$2.66** per sale on Amazon.com |

## 1. Files (download to your phone)

- **EPUB** (upload this one): [view](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/09-the-lockboxes-of-frostwood/frostwood-09-the-lockboxes-of-frostwood.epub) · [download](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/09-the-lockboxes-of-frostwood/frostwood-09-the-lockboxes-of-frostwood.epub?raw=true)  
  `frostwood-09-the-lockboxes-of-frostwood.epub`
- **Cover JPG** (1600 × 2560, KDP's ideal portrait ebook cover): [view](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/09-the-lockboxes-of-frostwood/frostwood-09-the-lockboxes-of-frostwood-cover.jpg) · [download](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/09-the-lockboxes-of-frostwood/frostwood-09-the-lockboxes-of-frostwood-cover.jpg?raw=true)  
  `frostwood-09-the-lockboxes-of-frostwood-cover.jpg`
- Previews: [phone pages](previews/phone-pages.png) · [cover thumbnail](previews/cover-thumb.png)

The repo is private, so be signed in to GitHub in your phone's browser. Tap *download*, then pick the file from Downloads in the KDP upload box.

Cover size note: the routine brief says 2560 × 1600, but KDP's ideal ebook cover is 2560 px tall × 1600 px wide, so the file is portrait 1600 × 2560 (same as book 5).

## 2. Create the Kindle ebook in KDP

1. **kdp.amazon.com** → **Bookshelf** → **+ Create** → **Kindle eBook**.
2. Fill in **Kindle eBook Details** with the copy-paste blocks in section 3.
3. **Kindle eBook Content**:
   - Manuscript → upload `frostwood-09-the-lockboxes-of-frostwood.epub`
   - Cover → **Upload a cover you already have** → upload `frostwood-09-the-lockboxes-of-frostwood-cover.jpg`
4. Answer the **AI-generated content** questions (section 4).
5. **Launch Previewer** (phone + tablet + Kindle) → check every item in section 5 → **Save and Continue**.
6. **Kindle eBook Pricing**: Territories **All territories**; Primary marketplace **Amazon.com**; royalty plan **70%**; list price **$3.99**. KDP Select is your choice.
7. Confirm the on-screen delivery fee is close to **$0.13** (Amazon measures its converted file, so small differences are normal).
8. **Publish Your Kindle eBook**.

## 3. Copy-paste fields

**Language:** English

**Book title**
```
The Lockboxes of Frostwood
```

**Subtitle**
```
120 Crack-the-Code Logic Puzzles for Kindle: Cozy Winter Brain Teasers, Easy to Expert, with Tap-to-Jump Hints and Answers
```

**Series name** (number **9**)
```
A Frostwood Puzzle Book
```
Series number: `9`

**Edition number:** leave blank

**Author** (first name / last name). No co-authors or contributors.
```
Blake
```
```
La Pierre
```

**Description**, **keywords** and **categories**: copy them from [listing.md](listing.md) (the description block is HTML that KDP accepts).

**Publishing rights:** I own the copyright. **Adult content:** No. **Reading age:** leave blank (or 10+).

## 4. AI-generated content answers

- **Text:** Yes. The puzzles were generated and verified by code, and the framing text was written with AI assistance and reviewed.
- **Images:** Yes. The black-and-white illustrations and the cover were drawn by code (procedural ink line art and a programmatic cover), not a generative image model.
- **Translations:** No.

## 5. Proof / preview checks

In the online Previewer (and on your phone after it's live):

- [ ] Cover fills the thumbnail; title and author readable
- [ ] Front matter: frontispiece, title page, copyright © 2026 Blake La Pierre, contents, how to play with the worked example (code 483)
- [ ] Clue lines read cleanly on a phone: the spaced digits (e.g. "7 5 2") sit on their own line above the note
- [ ] Tap **Need a hint?** on a few boxes → lands on the right hint; **Back to the box** returns
- [ ] Tap **Show answer** → lands on the right answer with the note-by-note check; **Back to the box** returns
- [ ] Section openers (lodge, village, railway, mountain) and the small vignettes display in black and white
- [ ] "Also by" lists Frostwood books 1–8
- [ ] No Christmas-specific content; no violence

## 6. Verification and rebuild

All 120 puzzles pass: exactly one code fits each box (found by the independent depth-first solver and again by an exhaustive check), every note is needed, no answer code or location repeats, and each box sits inside its band (digits, note count, "nothing is right" rule and solver effort). Full table: [verification.md](verification.md).

| Band | Boxes | Digits | Notes | "Nothing is right" note | Solver effort (nodes) |
|---|---|---|---|---|---|
| Easy · the Lodge | 30 | 3 | 4–5 | exactly one | 1–18 |
| Medium · the Village | 35 | 3 | 5–6 | none | 19–40 |
| Hard · the Railway | 35 | 4 | 5–7 | at most one | 41–90 |
| Expert · the Mountain | 20 | 5 | 7–9 | none | 91+ |

```bash
cd series/frostwood/09-the-lockboxes-of-frostwood/src
PYTHONHASHSEED=0 python3 master.py   # gen → verify → illustrations → cover → epub (about 2 minutes)
```

Seed `20261017` (recorded in `build-info.json`). `gen.py` writes a byte-identical `data.json` every run. The EPUB passed a structural check (XML well-formed, no broken internal links, every manifest file present, `mimetype` stored first); EPUBCheck itself wasn't run because Java isn't installed on the build machine, and KDP's own upload check will flag anything left.
