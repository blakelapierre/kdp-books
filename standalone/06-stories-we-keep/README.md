# Stories We Keep: KDP publishing checklist

Format: hardcover

**Status: print-ready HARDCOVER, not yet published.** Nothing has been submitted to KDP.

| | |
|---|---|
| **Format** | **Hardcover** (case laminate) |
| Pages | **102** |
| Trim | 6 × 9 in |
| Interior | Black & white on **white** paper, **no bleed** |
| Cover finish | **Matte** (recommended) |
| Price | **$17.99** USD |
| Printing cost | **$6.80** flat (black-ink hardcover, regular trim, 75–108 pages, Amazon.com) |
| Royalty (60%) | 0.60 × 17.99 − 6.80 = **$3.99** per copy |
| Spine (hardcover) | 102 × 0.002252 + 0.189 = **0.4187 in** |
| Full cover | **13.9947 × 10.418 in** (includes 0.591 in wrap on every edge) |

Printing cost source: KDP Help, [Hardcover Printing Cost](https://kdp.amazon.com/en_US/help/topic/GHT976ZKSKUXBB6H) (fetched 2026-10-14): black-ink hardcover, regular trim, **75–108 pages → $6.80 USD fixed, no per-page charge** on Amazon.com. Cover wrap / hinge dimensions follow the same formula used for *The Advent Clock* hardcover (`standalone/01-the-advent-clock/src/cover_hardcover.py`) and KDP’s [Create a Hardcover Cover](https://kdp.amazon.com/help/topic/GDTKFJPNQCBTMRV6) help (0.591 in wrap, 0.394 in hinge, boards = trim + 0.197 W / + 0.236 H, spine = pages × 0.002252 + 0.189).

## 1. Files (download to your phone)

- **Interior PDF** (phone-friendly name first): [view](https://github.com/blakelapierre/kdp-books/blob/main/standalone/06-stories-we-keep/interior-standalone-06-stories-we-keep.pdf) · [download](https://github.com/blakelapierre/kdp-books/blob/main/standalone/06-stories-we-keep/interior-standalone-06-stories-we-keep.pdf?raw=true)  
  `interior-standalone-06-stories-we-keep.pdf` (same bytes as `standalone-06-stories-we-keep-interior.pdf`)
- **Cover PDF** (hardcover wrap): [view](https://github.com/blakelapierre/kdp-books/blob/main/standalone/06-stories-we-keep/cover-standalone-06-stories-we-keep.pdf) · [download](https://github.com/blakelapierre/kdp-books/blob/main/standalone/06-stories-we-keep/cover-standalone-06-stories-we-keep.pdf?raw=true)  
  `cover-standalone-06-stories-we-keep.pdf` (same bytes as `standalone-06-stories-we-keep-cover.pdf`)
- Previews: [cover wrap](https://github.com/blakelapierre/kdp-books/blob/main/standalone/06-stories-we-keep/previews/cover-full-wrap.png) · [frontispiece](https://github.com/blakelapierre/kdp-books/blob/main/standalone/06-stories-we-keep/previews/interior-002.png) · [title](https://github.com/blakelapierre/kdp-books/blob/main/standalone/06-stories-we-keep/previews/interior-003.png) · [a prompt page](https://github.com/blakelapierre/kdp-books/blob/main/standalone/06-stories-we-keep/previews/interior-021.png)

The repo is private, so be signed in to GitHub in your phone's browser. Tap *download*, then pick the file from Downloads in the KDP upload box.

## 2. Create the HARDCOVER in KDP

1. **kdp.amazon.com** → **Bookshelf** → **+ Create** → **Hardcover**.
2. Fill in **Hardcover Details** with the copy-paste blocks in section 3.
3. **Hardcover Content**: ISBN → **Get a free KDP ISBN**; Publication date → leave blank; Print options → **Black & white interior with white paper**, trim **6 × 9 in**, **No bleed**, cover finish **Matte**.
4. **Manuscript** → upload `interior-standalone-06-stories-we-keep.pdf`.
5. **Book cover** → **Upload a cover you already have** → upload `cover-standalone-06-stories-we-keep.pdf` (this is the **hardcover** wrap with hinge and wrap margin — not a paperback cover).
6. Answer the **AI-generated content** questions (section 4).
7. **Launch Previewer** → check every item in section 5 → **Approve** → **Save and Continue**.
8. **Hardcover Rights & Pricing**: Territories **All territories**; Primary marketplace **Amazon.com**; list price **$17.99** (60% royalty, about $3.99/copy).
9. Order a **proof copy** first if you can (section 5), then **Publish Your Hardcover Book**.

## 3. Copy-paste fields

**Language:** English

**Book title**
```
Stories We Keep
```

**Subtitle**
```
A Guided Memory Keepsake for the Ones We Love | Writing Prompts for Parents & Grandparents
```

**Series:** none (standalone book). Leave the series fields empty.

**Edition number:** leave blank

**Author** (first name / last name). No co-authors or contributors.
```
Blake
```
```
La Pierre
```

**Description** (KDP accepts this HTML)
```html
<b>Some stories only live as long as someone remembers to write them down.</b>

This hardcover keepsake invites a parent or grandparent — or anyone whose life you want to hold on to — to answer gentle prompts about childhood, home, love, work, holidays, favorites and the wisdom they hope to leave behind.

<b>Inside you'll find:</b>
<ul>
<li>Eight life chapters with guided writing prompts and lined pages</li>
<li>Space for a family tree and a simple timeline</li>
<li>Letter pages to children, grandchildren and the person who gave the book</li>
<li>Extra lined pages when a story needs more room</li>
<li>Black-and-white ink illustrations of cottages, lamps and fireside rooms</li>
<li>6 × 9 inch case-laminate hardcover — a gift that feels permanent</li>
</ul>

A calm, screen-free heirloom for holidays, birthdays, Mother's Day, Father's Day and Grandparents Day.

Keep the stories.
```

**Keywords** (one per box)
1.
```
guided memory keepsake journal
```
2.
```
life story book for grandparents
```
3.
```
family heirloom writing prompts
```
4.
```
hardcover memory book gift
```
5.
```
parent grandparent story journal
```
6.
```
tell me your story keepsake
```
7.
```
family tree timeline letter journal
```

**Categories** (pick up to 3 in the picker)
- Parenting & Relationships › Family Relationships › Family History
- Self-Help › Journal Writing
- Crafts, Hobbies & Home › Crafts & Hobbies › Scrapbooking (optional third — check picker names)

**Primary audience:** sexually explicit content → **No**; reading age → leave blank.
**Low-content book:** Yes (guided journal / keepsake with lined writing pages). **Large-print:** leave unchecked.

## 4. AI-generated content answers

KDP asks this on the Content page. Truthful answers for this book:

- **Texts: Yes.** The prompts, how-to pages and cover blurb were written with AI. Choose *Entire work* and the editing level that matches how much you changed it.
- **Images: Yes.** The cover and interior illustrations were drawn by AI-written code. Choose *Entire work* and the editing level that fits.
- **Translations: No.**

## 5. Proof check (Previewer or printed proof)

- [ ] Page count in the KDP previewer matches **102** and the spine text sits centred on the hardcover spine with no wrap onto the covers.
- [ ] The cover file is the **hardcover** wrap (about 14 × 10.4 in), not a paperback wrap — check hinge gaps and wrap margins in the previewer.
- [ ] Frontispiece and section-opener art print as crisp black ink: solid blacks are even, no gray haze.
- [ ] Lined writing pages have comfortable spacing; nothing closer than ~0.5 in to the trim.
- [ ] Back-cover barcode box is empty white (KDP prints the barcode there).
- [ ] Author on the front cover, spine and title page reads **Blake La Pierre** only.
- [ ] Section openers start on right-hand pages.

## What this book is

A giftable **hardcover guided memory keepsake** (not a puzzle book): eight life chapters of writing prompts, a family tree, a timeline, letter pages and extra lined pages, with richer black-and-white ink illustrations. No puzzle verification file — there are no puzzles.

## More detail

- [listing.md](listing.md): full listing draft with demand evidence, pricing and notes
- Rebuild: `cd src && python3 illustrations.py && python3 build.py && python3 cover.py`
