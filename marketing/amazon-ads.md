# Amazon Sponsored Products Ads

Back to the [marketing kit](README.md).

This doc has one plan per book. The two live books go first. *Stars over Frostwood* and *The Advent Clock* are ready to launch as soon as they go live.

**Contents**
1. [Budget and structure](#1-budget-and-structure)
2. [Break-even ACoS, simply](#2-break-even-acos-simply)
3. [Setup, step by step](#3-setup-step-by-step)
4. [Weekly optimization checklist](#4-weekly-optimization-checklist)
5. [Book plans](#5-book-plans): [Thief](#51-the-thief-stayed-the-night-live) · [Express](#52-frostwood-express-live) · [Advent](#53-the-advent-clock-prepared) · [Stars](#54-stars-over-frostwood-prepared)
6. [Negative keywords](#6-negative-keywords)
7. [Sources](#7-sources)

---

## 1. Budget and structure

Each book gets **three campaigns** and a total of **$5–10/day**.

| Campaign | Targeting | Start budget | Bidding strategy |
|---|---|---|---|
| A. Auto | Automatic | $3/day | Dynamic bids – down only |
| B. Keywords | Manual keyword, three ad groups (Exact, Phrase, Broad) | $3/day | Dynamic bids – down only |
| C. Products | Manual product (competitor ASINs and category) | $2/day | Dynamic bids – down only |

- The total is **$8/day per book**. Start at the low end ($5–6) if cash is tight. Raise to $10 only for campaigns that are selling.
- Amazon averages your daily budget over the month. You may spend more on some days, but a $10/day budget never costs more than $300 in a 30-day month (Author's guide, source 2).
- Why "down only": Amazon lowers your bid when a click looks less likely to sell. That's the safest setting while you're learning.
- Name campaigns like `THIEF | Auto | 2026-10`, `THIEF | KW | 2026-10` and `THIEF | ASIN | 2026-10`.
- Amazon puts a **$50 pre-authorization hold** on your payment method when you first register (KDP Advertising, source 1).

**Starting bids** are a guess to begin with, not a rule. Use the lower of these two values, then adjust with the weekly checklist:
- Exact match: **$0.45–0.70**
- Phrase match: **$0.35–0.55**
- Broad match: **$0.30–0.45**
- Auto and product targets: **$0.35–0.55**
- Or Amazon's suggested bid, whichever is lower.

Amazon's targeting guide says to bid highest on exact, then phrase, then broad (source 3).

---

## 2. Break-even ACoS, simply

**ACoS** (advertising cost of sales) is ad spend divided by ad sales.

> Example: you spend $3 on ads and sell one $9.99 book from those ads. ACoS = $3 ÷ $9.99 = 30%.

**Break-even ACoS** is the ACoS where the ad costs exactly what you earn in royalty, so you make $0 on that sale.

> **Break-even ACoS = royalty ÷ price**

| Book | Price | Royalty per copy | Break-even ACoS | In plain words |
|---|---|---|---|---|
| The Thief Stayed the Night | $9.99 | $3.39 | **33.9%** | Up to about $3.39 in ads per sale breaks even |
| Frostwood Express | $9.99 | $2.69 | **26.9%** | Up to about $2.69 per sale |
| The Advent Clock | $9.99 | $3.69 | **36.9%** | Up to about $3.69 per sale |
| Stars over Frostwood | $9.99 | $2.81 | **28.1%** | Up to about $2.81 per sale |

⚠️ **Frostwood Express is live at $11.99, not $9.99.** This was checked on the public Amazon page on Sep 30 2026. At $11.99 the royalty is about 60% × $11.99 − $3.30 printing = **$3.89**, so break-even ACoS is **32.4%**. Use the row that matches the live price. If you move it back to $9.99, use 26.9%.

- **Below break-even:** each ad sale makes a profit.
- **Above break-even:** each ad sale loses money. Some authors accept a small loss early on to get sales and reviews. Decide your limit up front, for example break-even + 10 points for the first 30 days.
- Ads reports only count sales within 14 days of a click. For paperbacks, sales show on the day of purchase (source 1). Ads can also lift sales that the report doesn't count, so look at your total royalties too.

**Break-even cost per click (CPC)** = royalty × conversion rate.
We don't know your conversion rate yet. Here it is under two *assumed* rates, which are not statistics:

| Book | If 1 in 20 clicks buys (5%) | If 1 in 10 clicks buys (10%) |
|---|---|---|
| Thief | $0.17 | $0.34 |
| Express ($9.99 / $11.99) | $0.13 / $0.19 | $0.27 / $0.39 |
| Advent | $0.18 | $0.37 |
| Stars | $0.14 | $0.28 |

After about 2 weeks, replace the assumed rate with your own: orders ÷ clicks.

---

## 3. Setup, step by step

Only steps shown on Amazon's public help pages are listed here. Screens change, so if a button name differs, follow the nearest match.

### 3.1 One-time setup
1. **Claim the books in Author Central.** On the Books tab, choose Add a Book, search for the title, click the cover, then Add this book. Amazon's help says books must be in Author Central to advertise them. Source 1; full steps in [author-central.md](author-central.md).
2. **Open the ads console from KDP.** Go to the KDP **Marketing** tab → **Amazon Ads** → **Learn more** → choose the marketplace (Amazon.com) → **Start Advertising** (source 1).
   - Another route: on the **Bookshelf**, click the **"…"** button next to the book → **Promote and Advertise** → choose the marketplace → **Create an ad campaign** (source 4).
3. Add a payment method. Expect the **$50 pre-authorization** hold (source 1).

### 3.2 Create each campaign
1. In the ads console, click **Create campaign** (sources 1 and 2).
2. Choose **Sponsored Products** (source 2).
3. **Products:** search your book by title or ASIN and add it (source 2). Add only the one book per campaign. Amazon suggests one ASIN per campaign when you have few (source 3).
4. **Targeting:** choose **Automatic** (campaign A) or **Manual** (campaigns B and C). ⚠️ **You can't change the targeting type after launch** (source 3).
   - Manual keyword: paste the keywords from the book's plan below and choose the match type for each ad group.
   - Manual product: paste the ASINs from the book's plan below. You can also add categories.
5. **Negative keywords:** in the same create window, use **Negative keyword targeting** to add the negatives from [section 6](#6-negative-keywords) (source 3). You can add more later in the campaign's **Negative keywords** tab.
6. **Bidding strategy:** choose **Dynamic bids – down only** (source 2).
7. **Daily budget:** enter the amount from the table in [section 1](#1-budget-and-structure).
8. **Custom ad text** (optional): KDP's getting-started guide for authors mentions custom text ads (source 5). Use the one-liner from the book's plan.
9. **Launch.** Amazon moderates ads, usually within 24 hours and at most 3 business days (source 1).

### 3.3 Reading results
- Metrics can take **up to 14 days** to fill in. Clicks can still register for 24 hours after you pause a campaign (KDP Timelines, source 6).
- Data can lag by about 12 hours (source 1).
- Search term report: go to **Measurement & reporting** → **Create a report** (source 2).
- Amazon's guide suggests waiting about 2 weeks before optimizing bids, then checking every 2 weeks (source 2). The weekly checklist below is a light touch that respects this.

---

## 4. Weekly optimization checklist

Every **Monday**, spend about 15 minutes on this. For the first 14 days after launch, only do the ✳️ steps.

- [ ] ✳️ Check that every campaign is **delivering**: impressions are rising and nothing is rejected.
- [ ] ✳️ Check spend against budget, and the total per book.
- [ ] Download the **search term report** for the last 14 days.
- [ ] Apply the rules below. Change each bid by **no more than 20% a week**.
- [ ] Write down each change in a note, with the date.

### The rules

| Situation | Action |
|---|---|
| A keyword or target has **≥ 20 clicks and 0 orders** | **Cut.** Pause it, or add it as a negative exact in the auto campaign if it's a search term. This matches Amazon's guidance to evaluate a negative after ≥20 clicks (source 3). |
| ACoS **above break-even**, with ≥ 2 orders or ≥ 30 clicks | **Lower** the bid by 15–20%. |
| ACoS **more than 10 points below break-even** | **Raise** the bid by 10–15%. |
| Fewer than about 100 impressions in a week | **Raise** the bid by 10–15%. It's probably underbid. |
| An auto search term has **≥ 1 order** | **Harvest.** Add it to the Exact ad group, and add it as a **negative exact** in the auto campaign. |
| A campaign has spent about **3× the royalty** (e.g. $10 for Thief) with **0 orders** | **Pause** it and look at the targets and listing. |
| A campaign is **out of budget** before evening with ACoS below break-even | **Raise the budget** by $1–2/day, staying within $10/day per book in total. |
| A new negative keyword | Let it run **at least 2 weeks** before judging (source 3). |
| Seasonal (Advent) | Ramp budget **Nov 15** and taper **Dec 15**. **Pause about Dec 21**, because orders arriving after Christmas Eve don't help. |

Also check TACoS (total ACoS) once a month: ad spend ÷ *all* royalties for the book. If it's falling over time, ads are helping overall. Amazon's author guide mentions TACoS (source 2).

---

## 5. Book plans

All links use `https://www.amazon.com/dp/ASIN`. Competitor ASINs were **checked on public Amazon pages on Sep 30 2026**. Ratings and prices change, so shown ratings are as seen that day. **Before launch, re-check that each ASIN still loads.**

### 5.1 The Thief Stayed the Night (live)
**ASIN:** B0HLMMS675 · https://www.amazon.com/dp/B0HLMMS675 · Break-even ACoS **33.9%**

**Custom ad text (optional):**
> Twelve cozy cases in a snowbound hotel. Cross suspects off the register and find the thief. No violence, just logic.

**Campaign B keywords (32)**

*Exact ad group, core ($0.45–0.70)*
1. mystery puzzle book
2. mystery puzzle book for adults
3. whodunit puzzle book
4. detective puzzle book
5. elimination puzzle book
6. cozy mystery puzzle book
7. solve the mystery puzzle book
8. logic mystery puzzles
9. detective logic puzzles for adults
10. mystery logic puzzle book

*Phrase ad group, theme ($0.35–0.55)*

11. hotel mystery puzzle book
12. snowbound mystery puzzle
13. winter mystery puzzle book
14. deduction puzzles for adults
15. deduction puzzle book
16. mystery brain teasers
17. who done it puzzle book
18. clue solving puzzle book
19. detective game book
20. mystery puzzle book for teens

*Broad ad group, audience, gift and comparables ($0.30–0.45)*

21. gifts for mystery lovers
22. cozy mystery gifts
23. logic puzzles for adults
24. brain teasers for adults
25. puzzle books for adults
26. clean puzzle book for adults
27. family puzzle game book
28. stocking stuffer puzzle book
29. murdle
30. murdle puzzle book
31. cozy crime puzzle book
32. armchair detective puzzles

> Note: most titles in this niche use the word "murder". To match the book's cozy, non-violent brand, the list leaves out "murder" keywords. Book titles as keywords (e.g. "murdle") are fine: they target shoppers, not content. If you later want more reach, test "murder mystery puzzle book" in its own ad group and watch ACoS.

**Campaign C product targets**

| ASIN | Title (as seen) | Author | Link |
|---|---|---|---|
| 1250892317 | Murdle: Volume 1 | G. T. Karber | https://www.amazon.com/dp/1250892317 |
| B0HJHTWFSG | Just One Murder Before Tea: Cozy… Elimination Puzzle Book | Ruth Ravenscroft | https://www.amazon.com/dp/B0HJHTWFSG |
| B0HFC4D8L4 | Who Killed Beatrix? | Ellis J Ward | https://www.amazon.com/dp/B0HFC4D8L4 |
| B0H32YQQQX | Murder at the Grand Hotel: A Cozy Mystery Logic Puzzle Book | Le petit atelier de Julie | https://www.amazon.com/dp/B0H32YQQQX |
| B0HFQ3LQ3H | Snowed in Murder Mystery Logic Puzzle Book | Melanie Collins | https://www.amazon.com/dp/B0HFQ3LQ3H |
| B0H8ZQCPHX | The Killer Never Left the Ski Lodge | Casebreaker Books | https://www.amazon.com/dp/B0H8ZQCPHX |
| B0H8Q6W1WV | Find the Killer Puzzle Book | J.N. Corven | https://www.amazon.com/dp/B0H8Q6W1WV |
| 150722527X | Murder Among the Stacks | Rosie A. Point | https://www.amazon.com/dp/150722527X |
| 1789298881 | Cute and Cozy Crime | Gareth Moore | https://www.amazon.com/dp/1789298881 |
| B0H6BPHSR7 | Whodunit?: 40 Murder Mystery Logic Puzzles | Joseph Morazza | https://www.amazon.com/dp/B0H6BPHSR7 |
| B0HLMB966Q | *Frostwood Express* (your own, series cross-sell) | Blake La Pierre | https://www.amazon.com/dp/B0HLMB966Q |

- Category target: **Logic & Brain Teasers** (Books).
- Tip: Murdle is a very large seller, and its clicks can be expensive. Start it at the low end of the bid range.

---

### 5.2 Frostwood Express (live)
**ASIN:** B0HLMB966Q · https://www.amazon.com/dp/B0HLMB966Q · Break-even ACoS **32.4% at the live $11.99** (26.9% at $9.99)

**Custom ad text (optional):**
> 200 Train Tracks logic puzzles from Easy 6×6 to Expert 12×12. Lay one railway from A to B. Solutions included.

**Campaign B keywords (32)**

*Exact ad group, core ($0.45–0.70)*
1. train tracks puzzles
2. train tracks puzzle book
3. train tracks logic puzzles
4. train track puzzles for adults
5. tracks puzzle book
6. rail puzzle book
7. railway logic puzzles
8. train tracks puzzles for adults
9. tracks logic puzzles
10. train track logic puzzle book

*Phrase ad group, theme ($0.35–0.55)*

11. logic puzzle book for adults
12. pencil puzzles for adults
13. path puzzles
14. grid logic puzzles
15. japanese logic puzzles
16. logic puzzles easy to hard
17. logic puzzles with solutions
18. nikoli style puzzles
19. brain teasers for teens
20. hard logic puzzles for adults

*Broad ad group, audience, gift and comparables ($0.30–0.45)*

21. gifts for train lovers
22. train lover gifts for men
23. train gifts for adults
24. model railway gifts
25. puzzle books for adults
26. brain teasers for adults
27. winter puzzle book
28. stocking stuffer puzzle book
29. puzzle gift for dad
30. alex smart train tracks
31. tracks puzzle a day
32. clarity media puzzles

**Campaign C product targets**

| ASIN | Title (as seen) | Author | Link |
|---|---|---|---|
| B0HF8NBYDS | 300 Train Track Logic Puzzles for Adults | Hazel Woods | https://www.amazon.com/dp/B0HF8NBYDS |
| 191879202X | Train Tracks: 200 Logic Puzzles for Adults | Alex Smart | https://www.amazon.com/dp/191879202X |
| 1918792208 | Tricky Train Tracks: 200 Logic Puzzles | Alex Smart | https://www.amazon.com/dp/1918792208 |
| B08C3MT6JG | Train Tracks Logic Puzzles: 150 8x8 | D.O. Puzzles | https://www.amazon.com/dp/B08C3MT6JG |
| B0CM6Q9PC3 | Train Tracks Puzzle Challenge Vol. 1 (Hard) | Silver Apricot Books | https://www.amazon.com/dp/B0CM6Q9PC3 |
| B0FQ55CKBG | Tracks Puzzle a Day 2026 | Clarity Media | https://www.amazon.com/dp/B0FQ55CKBG |
| B0HJ8K68VQ | Train Tracks: 300 Logic Puzzles | Alvaro Samuel Céspedes Ramirez | https://www.amazon.com/dp/B0HJ8K68VQ |
| B0HKB2XTS5 | Train Track Logic Puzzle Book: 300 | Brian Reitz | https://www.amazon.com/dp/B0HKB2XTS5 |
| B0HJ5B6B7F | Train Track Logic: 300 | Mols Brothers | https://www.amazon.com/dp/B0HJ5B6B7F |
| B0HLMMS675 | *The Thief Stayed the Night* (your own, series cross-sell) | Blake La Pierre | https://www.amazon.com/dp/B0HLMMS675 |

- Category target: **Logic & Brain Teasers** (Books).

---

### 5.3 The Advent Clock (prepared)
**Not live yet.** Launch these campaigns the day the book goes live. The target is Nov 1–8. Break-even ACoS **36.9%**.

**Seasonal budget**
- Launch to Nov 14: **$5/day** in total.
- Nov 15–Dec 15: **$10/day** in total.
- Dec 16–20: **$5/day**.
- About **Dec 21**: pause.

**Custom ad text (optional):**
> Twenty-four doors, one puzzle behind each. A cozy December countdown with codes, mazes and logic puzzles. Just a pencil.

**Campaign B keywords (34)**

*Exact ad group, core ($0.45–0.70)*
1. advent calendar puzzle book
2. puzzle advent calendar
3. advent calendar book for adults
4. escape room advent calendar
5. escape room advent calendar book
6. logic puzzle advent calendar
7. christmas puzzle book for adults
8. christmas puzzle book
9. advent calendar for adults
10. christmas countdown puzzle book
11. 24 days of puzzles

*Phrase ad group, theme ($0.35–0.55)*

12. christmas logic puzzles
13. christmas brain teasers
14. christmas escape room book
15. christmas activity book for adults
16. christmas code breaking puzzles
17. cipher puzzle book
18. secret code puzzle book
19. christmas riddles book
20. advent activity book
21. christmas mystery puzzle book
22. december puzzle book

*Broad ad group, audience, gift and comparables ($0.30–0.45)*

23. christmas stocking stuffers for adults
24. stocking stuffer puzzle book
25. stocking stuffers for teens
26. christmas gifts for puzzle lovers
27. family advent calendar activity
28. advent calendar for teens
29. puzzle gift for adults
30. brain teasers for adults
31. riddlehaus advent calendar
32. unicorn books logic puzzle advent calendar
33. enigmapolis advent calendar
34. advent calendar book

**Campaign C product targets** (all 5 candidates from the brief verified, plus 6 more)

| ASIN | Title (as seen) | Author | Link |
|---|---|---|---|
| B0FQC1V2XD | Mystery Escape Room Advent Calendar for Adults (Bramblewood Cabin) | Niklas Falkner / Riddlehaus | https://www.amazon.com/dp/B0FQC1V2XD |
| B0FT36DP73 | Escape Room Advent Calendar… no web app required | ENIGMAPOLIS | https://www.amazon.com/dp/B0FT36DP73 |
| B0FVX53TVZ | 24-Day Escape Room Advent Calendar for Adults | Marlies Larch | https://www.amazon.com/dp/B0FVX53TVZ |
| B0FT2YZ2NH | Escape Room Advent Calendar: … Streets of London | Escape Factory Club | https://www.amazon.com/dp/B0FT2YZ2NH |
| B0CMDHP1PB | The Logic Puzzle Advent Calendar | Unicorn Books | https://www.amazon.com/dp/B0CMDHP1PB |
| B0DJ8PHQD8 | Logic Puzzle Advent Calendar Vol. 2 | Unicorn Books | https://www.amazon.com/dp/B0DJ8PHQD8 |
| B0FYF5678N | Advent Calendar for Adults: 24 Days of Brain-Tickling Riddles | IQ Street | https://www.amazon.com/dp/B0FYF5678N |
| B0HG7CB2LV | Advent Calendar for Adults: Solve 24 puzzles… | Albert Gate | https://www.amazon.com/dp/B0HG7CB2LV |
| B0DJF4DRWV | Advent Calendar Puzzle Book… | BIG PRINT BOOKS | https://www.amazon.com/dp/B0DJF4DRWV |
| 1910929204 | The Christmas Countdown Logic Puzzle Challenge | Tarja Moles | https://www.amazon.com/dp/1910929204 |
| B0HHYRXZW1 | The Family Escape Room Advent Calendar | Cork & Pin Press | https://www.amazon.com/dp/B0HHYRXZW1 |

- Category targets: **Logic & Brain Teasers**, and **Party Games** if it's offered.

---

### 5.4 Stars over Frostwood (prepared)
**Not live yet.** Launch the day it goes live. Break-even ACoS **28.1%**.

**Custom ad text (optional):**
> 180 Star Battle puzzles, also called Two Not Touch or Queens. One-star and two-star grids, Easy to Expert, with solutions.

**Campaign B keywords (32)**

*Exact ad group, core ($0.45–0.70)*
1. star battle puzzle book
2. star battle puzzles
3. star battle
4. two not touch puzzles
5. two not touch
6. queens puzzle book
7. queens logic puzzle
8. queens puzzle
9. star battle puzzles for adults
10. star battle 10x10

*Phrase ad group, theme ($0.35–0.55)*

11. queens game puzzles
12. logic puzzle book for adults
13. japanese logic puzzles
14. nikoli puzzle book
15. pencil puzzles for adults
16. grid logic puzzles
17. hard logic puzzles
18. logic puzzles easy to hard
19. logic puzzles with solutions
20. star puzzles for adults

*Broad ad group, audience, gift and comparables ($0.30–0.45)*

21. krazydad two not touch
22. krazydad puzzles
23. krazydad
24. sudoku alternative puzzles
25. brain teasers for adults
26. puzzle books for adults
27. winter puzzle book
28. stocking stuffer puzzle book
29. puzzle gift for adults
30. brain games for adults
31. queens puzzles for adults
32. two not touch puzzle book

> Keep keywords and ad text to generic puzzle names (Star Battle, Two Not Touch, Queens). Don't name any app or platform.

**Campaign C product targets**

| ASIN | Title (as seen) | Author | Link |
|---|---|---|---|
| 1946855367 | Krazydad Two Not Touch Volume 1 | Jim Bumgardner | https://www.amazon.com/dp/1946855367 |
| 1946855375 | Krazydad Two Not Touch Volume 2 | Jim Bumgardner | https://www.amazon.com/dp/1946855375 |
| 1946855383 | Krazydad Two Not Touch Volume 3 | Jim Bumgardner | https://www.amazon.com/dp/1946855383 |
| 1946855154 | Krazydad Diabolical Two Not Touch Volume 1 | Jim Bumgardner | https://www.amazon.com/dp/1946855154 |
| 1454943661 | Star Battle Puzzles | Jim Bumgardner | https://www.amazon.com/dp/1454943661 |
| B0DLCKC6YL | Large Print Queens Star Battle Puzzle Book For Adults | Puzzling Puffin | https://www.amazon.com/dp/B0DLCKC6YL |
| B0H396P3Y1 | Star Battle Puzzle Book: 120 … 10x10 | BOTS PUZZLE PRESS | https://www.amazon.com/dp/B0H396P3Y1 |
| B09NR8CYDJ | The Big Puzzle Book of Star Battle: 500 | Nidhi Grover | https://www.amazon.com/dp/B09NR8CYDJ |
| B0HFX6LTHM | Queens Logic Puzzles Vol. 1: 216 | Remy Holden | https://www.amazon.com/dp/B0HFX6LTHM |
| B0GZHY1CWJ | Queens Puzzle Book for Adults: 120 | Puzzle Bee | https://www.amazon.com/dp/B0GZHY1CWJ |
| B0HLMB966Q | *Frostwood Express* (your own, series cross-sell) | Blake La Pierre | https://www.amazon.com/dp/B0HLMB966Q |

- Category target: **Logic & Brain Teasers** (Books).

---

## 6. Negative keywords

Add these as **negative phrase** in every campaign. They block searches that are unlikely to buy a paperback logic puzzle book.

**All books**
- free
- pdf
- download
- app
- kindle unlimited
- ebook
- large print
- for kids
- children
- toddler
- coloring
- jigsaw
- crossword
- spanish

**The Thief Stayed the Night:** also add
- sudoku
- word search book
- novel
- audiobook
- board game
- murder mystery party
- dinner party

**Frostwood Express:** also add
- sudoku
- word search book
- toy train
- train set
- lego
- thomas
- brio
- wooden

**Stars over Frostwood:** also add
- star wars
- stickers
- astronomy
- telescope
- chess

**The Advent Clock:** also add
- chocolate
- lego
- toy
- wine
- beer
- beauty
- jewelry
- tea
- kids advent calendar
- dog
- cat
- socks

A few notes:
- Don't negate words you also bid on. For example, "sudoku" is left out of the Stars negatives because "sudoku alternative puzzles" is a Stars keyword. "Word search" is left out for Advent because Door 1 is a word search.
- Add new negatives from the search term report each week (see the rules above).

---

## 7. Sources

All public pages were checked Sep 30 2026.

1. KDP Help, *Amazon Ads* (Author Central requirement, Marketing tab route, $50 hold, moderation, reporting window): https://kdp.amazon.com/en_US/help/topic/G201499010
2. Amazon Ads, *Author's guide to Sponsored Products* (Create campaign, bidding strategies, monthly budget averaging, reports, 2-week review, TACoS): https://advertising.amazon.com/library/guides/authors-guide-to-sponsored-products
3. Amazon Ads, *Targeting with Sponsored Products* (auto groups, match types, bid order, negatives, ≥20 clicks, targeting can't change after launch): https://advertising.amazon.com/library/guides/targeting-with-sponsored-products
4. KDP Community, *Accessing your Amazon Advertising console* (Bookshelf "…" → Promote and Advertise): https://www.kdpcommunity.com/s/article/Accessing-your-Amazon-Advertising-console
5. Amazon Ads, *Getting started guide for authors* (PDF): https://m.media-amazon.com/images/G/01/ams/AMS_getting_started_authors_10.pdf
6. KDP Help, *Timelines* (metrics up to 14 days; price changes 72 hours–5 business days): https://kdp.amazon.com/en_US/help/topic/G202173620
