# A+ Content Kit

Back to the [marketing kit](../README.md).

Each book has:
- `module-text.md`: copy-paste text for every module, including headlines, body, image alt text and captions
- Ready images at Amazon's module sizes

**Folders**
- [the-thief-stayed-the-night/](the-thief-stayed-the-night/module-text.md)
- [frostwood-express/](frostwood-express/module-text.md)
- [stars-over-frostwood/](stars-over-frostwood/module-text.md)
- [the-advent-clock/](the-advent-clock/module-text.md)
- [comparison-chart/](comparison-chart/): cover images for the comparison chart

Images are rebuilt with `marketing/src/build_aplus.py`. They're drawn from each book's own `interior.pdf` and cover, using the house fonts: Playfair Display SC, Crimson Text and IBM Plex Sans Condensed.

---

## Module sizes (verified)

| Module | Image size used here | Amazon minimum | Text limits |
|---|---|---|---|
| Standard Image Header With Text | **970 × 600** | 970 × 600 | Headline 150 · Subheadline 150 · Body 6,000 · Alt text 100 |
| Standard Three Images & Text | **600 × 600** ×3 | 300 × 300 (KDP suggests 600 × 600) | Headline 200 · Block headline 160 · Block body 1,000 · Alt 100 |
| Standard Comparison Chart | **300 × 600** per book | 150 × 300 (max 3 MB) | Title 80 · Metric 250 · Up to 5 of **your own** ASINs |

Sources:
- Amazon SP-API, *A+ Content module examples* (minimum sizes and character limits): https://developer-docs.amazon.com/sp-api/docs/a-plus-content-examples
- KDP Help, *A+ Content examples* (suggested sizes, comparison chart limits): https://kdp.amazon.com/help/topic/GCKLH8V7ULLD5EXY
- KDP Help, *A+ Content guidelines* (what's not allowed): https://kdp.amazon.com/en_US/help/topic/G4WB7VPPEAREHAAD
- KDP Help, *Create A+ Content* (steps): https://kdp.amazon.com/en_US/help/topic/G8EP5W6H9CY7T8GS

All images here are RGB PNG files under 2 MB, as the guidelines require.

---

## Module plan (5 modules per book, which is the maximum per page)

1. **Standard Image Header With Text** using `1-header-970x600.png`
2. **Standard Three Images & Text** using the three `2-sample-*-600x600.png` files. These are real puzzle pages, with no added text on the image, as KDP suggests.
3. **Standard Image Header With Text** using `3-why-these-puzzles-970x600.png`
4. **Standard Image Header With Text** using `4-frostwood-series-970x600.png`. This is the Frostwood panel.
5. **Standard Comparison Chart** covering your books only. Images are in [comparison-chart/](comparison-chart/).

---

## Rules to remember

Summarized from the KDP guidelines page above:
- **No** "free", "affordable", "bonus", "buy now", prices or discounts.
- **No** customer reviews or quotes, "#1", "best-selling" or "top-rated".
- **No** time-sensitive words like "new", "now", "latest" or "yet".
- **No references to holidays.** ⚠️ This matters for *The Advent Clock*. Its A+ text is written without holiday words, and its sample images are cropped below the "December" page headers. The cover itself says "A Christmas Puzzle Countdown", and a reviewer could still object to that. If it's rejected, remove the header module that shows the cover and resubmit.
- **No** links, no email addresses, and no language that sends shoppers to other products. The series panel only *shows* the books. The comparison chart is the approved way to show your other titles.
- **No** competitor mentions.
- Spell out numbers under 10, use the serial comma, and use title case in headlines.
- Text in images must be readable on a phone. The images use large type for this reason.
- Images must be unique to A+. Don't reuse them as gallery images.

---

## How to submit (from KDP Help, *Create A+ Content*)

1. Open KDP → **Marketing** tab.
2. In the **A+ Content** section, pick the marketplace (Amazon.com) → **Manage A+ Content**.
3. Click **Start creating A+ content**. Enter a content name (e.g. `Thief A+ v1`) and choose English.
4. Click **Add Module**. Choose the module from the plan, and upload the images and paste the text from `module-text.md`. Repeat for up to five modules.
5. Click **Next: Apply ASINs**. Add the book's ASIN. Only your own KDP ASINs are allowed.
6. Click **Review and Submit**.
7. Content usually appears within **8 business days**. If it's rejected, KDP says why, so edit and resubmit.

Amazon doesn't resize images, so upload them exactly as provided.

---

## Timing

| Book | Submit A+ |
|---|---|
| The Thief Stayed the Night | Oct 5 |
| Frostwood Express | Oct 5 |
| Stars over Frostwood | The day it goes live. Then update the Thief and Express series panel and comparison chart to include it. |
| The Advent Clock | The day it goes live, aim Nov 1–8. Allow up to 8 business days for approval. |

Until Stars is live, you can either:
- skip module 4 on Thief and Express, or
- submit it anyway. It shows the book-three cover, but shoppers can't find Stars until it's live.

The first option is tidier.
