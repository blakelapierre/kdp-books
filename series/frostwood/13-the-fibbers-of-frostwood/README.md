# The Fibbers of Frostwood: KDP ebook publishing checklist

**Status: ebook-ready, not yet published.** Nothing has been submitted to KDP.

| | |
|---|---|
| Format | **Kindle ebook** (EPUB 3, reflowable, phone-friendly, nothing to write in) |
| Series | **A Frostwood Puzzle Book** · number **13** |
| Puzzles | **120** truth-teller and fibber games (30 Easy · 35 Medium · 35 Hard · 20 Expert) |
| Type | Truth-tellers and fibbers (knights and knaves): each player makes one statement; work out who is which |
| Length | ebook, no page count (EPUB 1,000,523 bytes; 120 games + 120 hints + 120 answers) |
| Author | **Blake La Pierre** |
| Price | **$3.99** USD (70% royalty option) |
| Printing cost | none (ebook) |
| Delivery fee (est.) | **$0.14** (1,000,523 bytes ≈ 0.955 MB × $0.15/MB) |
| Royalty (est.) | 0.70 × 3.99 − 0.14 = **$2.65** per sale on Amazon.com |

## 1. Files (download to your phone)

- **EPUB** (upload this one): [view](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/13-the-fibbers-of-frostwood/frostwood-13-the-fibbers-of-frostwood.epub) · [download](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/13-the-fibbers-of-frostwood/frostwood-13-the-fibbers-of-frostwood.epub?raw=true)  
  `frostwood-13-the-fibbers-of-frostwood.epub`
- **Cover JPG** (1600 wide × 2560 tall, KDP's ideal ebook cover): [view](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/13-the-fibbers-of-frostwood/frostwood-13-the-fibbers-of-frostwood-cover.jpg) · [download](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/13-the-fibbers-of-frostwood/frostwood-13-the-fibbers-of-frostwood-cover.jpg?raw=true)  
  `frostwood-13-the-fibbers-of-frostwood-cover.jpg`
- Previews: [phone pages](previews/phone-pages.png) · [cover thumbnail](previews/cover-thumb.png)
- Listing text: [listing.md](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/13-the-fibbers-of-frostwood/listing.md) · Verification: [verification.md](https://github.com/blakelapierre/kdp-books/blob/main/series/frostwood/13-the-fibbers-of-frostwood/verification.md)

The repo is private, so be signed in to GitHub in your phone's browser. Tap *download*, then pick the file from Downloads in the KDP upload box.

## 2. Create the Kindle ebook in KDP

1. **kdp.amazon.com** → **Bookshelf** → **+ Create** → **Kindle eBook**.
2. Fill in **Kindle eBook Details** with the copy-paste blocks in section 3.
3. **Kindle eBook Content**:
   - Manuscript → upload `frostwood-13-the-fibbers-of-frostwood.epub`
   - Cover → **Upload a cover you already have** → upload `frostwood-13-the-fibbers-of-frostwood-cover.jpg`
4. Answer the **AI-generated content** questions (section 4).
5. **Launch Previewer** (phone + tablet + Kindle) → check every item in section 5 → **Save and Continue**.
6. **Kindle eBook Pricing**: Territories **All territories**; Primary marketplace **Amazon.com**; royalty plan **70%**; list price **$3.99**. KDP Select is your choice.
7. Confirm the on-screen delivery fee is close to **$0.14** (Amazon measures its converted file, so small differences are normal).
8. **Publish Your Kindle eBook**.

## 3. Copy-paste fields

**Language:** English

**Book title**
```
The Fibbers of Frostwood
```

**Subtitle**
```
120 Truth-Teller and Fibber Logic Puzzles for Kindle: Cozy Winter Knights and Knaves Brain Teasers, Easy to Expert, with Tap-to-Jump Hints and Answers
```

**Series name** (number **13**). Use the same series name as the live Frostwood books so they link up on Amazon:
```
A Frostwood Puzzle Book
```
Series number: `13`

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
knights and knaves logic puzzles
```
```
truth teller and liar puzzles
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
who is lying riddles
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
- [ ] Front matter: frontispiece, title page, copyright © 2026 Blake La Pierre, contents, how to play with the worked example (Ada, Bram and Clara: Ada truth-teller, Bram and Clara fibbers)
- [ ] Each statement reads cleanly on a phone, speaker name in bold blue, then the quote
- [ ] Tap **Need a hint?** on a few games → lands on the right hint; **Back to the game** returns
- [ ] Tap **Show answer** → lands on the right answer with the statement-by-statement check; **Back to the game** returns
- [ ] Section openers (lodge, village, railway, mountain) and the small pinecone vignettes display in black and white
- [ ] "Also by" lists Frostwood books 1–11
- [ ] No Christmas-specific content; no violence

## 6. Verification and rebuild

All 120 puzzles pass: exactly one assignment of truth-tellers and fibbers fits each game (it matches the printed answer), every statement is needed, no game repeats, and each game sits inside its band. The independent verifier reads the **printed English** of every statement back into a rule, so a wording slip would fail. Full table: [verification.md](verification.md).

| Band | Games | Players | Statement kinds | Depth (supposition inside supposition) | "Suppose…" tests |
|---|---|---|---|---|---|
| Easy · the Lodge | 30 | 3 | is, same/different, both, either | 0 (one statement at a time) | 0 |
| Medium · the Village | 35 | 4 | all, incl. counting and if-then | 1 | 1 |
| Hard · the Railway | 35 | 5 | all | 1 | 2–3 |
| Expert · the Mountain | 20 | 6 | no plain "X is a …" | 2 | 1–3 |

```bash
cd series/frostwood/13-the-fibbers-of-frostwood/src
PYTHONHASHSEED=0 python3 master.py   # gen → verify → illustrations → cover → epub (about 15 seconds)
# optional EPUBCheck: EPUBCHECK_JAR=/path/epubcheck.jar JAVA=/path/java PYTHONHASHSEED=0 python3 master.py
```

Seed `20261031` (recorded in `build-info.json`). `gen.py` writes a byte-identical `data.json` every run. **EPUBCheck 5.1.0: 0 fatals / 0 errors / 0 warnings** (EPUB 3.3 rules).
