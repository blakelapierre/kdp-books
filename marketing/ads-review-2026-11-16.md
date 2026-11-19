# Amazon Ads review — 2026-11-16

Read-only review. No bids, budgets, keywords, negatives, or campaign statuses were changed. Blake must approve every change before anything is applied.

- **Profile:** 427992898389565
- **Date range:** 2026-10-18 through 2026-11-16
- **Source:** Adspirer `get_amazon_campaign_performance` and `get_amazon_search_terms` (Sponsored Products), pulled 2026-11-16
- **Adspirer calls used this review:** 4 (`list_tools`, `get_tool_schema`, campaign performance, search terms)
- **Campaign names** below are mapped from `marketing/amazon-ads.md` (2026-10-20 setup). The performance report returned campaign IDs only.

Blake reports two Advent Clock sales from ads, about $12 spent vs $8 earned (about $4 net loss). That lines up with this pull: **$12.66 spend**, **2 purchases**, **$35.98 sales** (2 × the live $17.99 hardcover price).

## Break-even ACOS

Royalty is about $3–4 per book. On these two Advent sales Blake earned about $8, so about **$4 royalty** each.

| Book | Live price | Royalty used here | Break-even ACOS |
|---|---|---|---|
| The Advent Clock (hardcover, B0HMW1MR5T) | $17.99 | $4 (Blake: $8 earned on 2 sales) | **22.2%** ($4 ÷ $17.99) |
| Paperbacks (Bridges, Porch Swing, etc.) | $9.99 | $3–4 | **30–40%** |

Overall ACOS in this window is **35.2%**, above Advent's 22.2% break-even, which is why the account is in the red even though ads produced both sales. The older break-even figure in `amazon-ads.md` (36.9%) assumed a $9.99 paperback and does not apply to the live hardcover.

## Campaign performance (2026-10-18 → 2026-11-16)

**Account totals:** 10,597 impressions · 14 clicks · 0.13% CTR · **$12.66 spend** · **2 purchases** · **$35.98 sales** · **35.2% ACOS** · 2.84 ROAS

| Campaign (name from Oct 20 setup) | Campaign ID | Impr | Clicks | Spend | Sales | ACOS |
|---|---|---|---|---|---|---|
| Oct 18 auto – Advent only ($5/day, B0HMW1MR5T) | `47473767889736` | 9,750 | 13 | $12.51 | $35.98 | 34.8% |
| Oct 18 auto – 7 ASINs ($5/day) | `277628141714115` | 703 | 1 | $0.15 | $0.00 | — |
| Auto - Advent Clock HC ($4/day) | `161403826749231` | 71 | 0 | $0.00 | $0.00 | — |
| Auto - Stories We Keep HC ($2/day) | `278315951110803` | 49 | 0 | $0.00 | $0.00 | — |
| Auto - Porch Swing Crosswords PB ($2/day) | `153725246462664` | 13 | 0 | $0.00 | $0.00 | — |
| Auto - Bridges of Frostwood PB ($2/day) | `112094854265272` | 11 | 0 | $0.00 | $0.00 | — |
| **Total** | | **10,597** | **14** | **$12.66** | **$35.98** | **35.2%** |

All two sales and virtually all spend are in the Oct 18 Advent-only auto campaign. Average CPC there is $12.51 ÷ 13 = **$0.96**. The four Oct 20 per-book autos (default bid $0.40) have had no clicks.

These totals are essentially unchanged from the 2026-10-26 review in `amazon-ads.md` (then 10,603 impr, 14 clicks, $12.66, 2 orders, $35.98). Impressions are slightly lower in this longer window (9,756 → 9,750 on the Advent-only campaign). There has been **no meaningful new spend or delivery in the three weeks since Oct 26**, despite a combined daily budget of about $20. Actual spend over the full window is only about $0.42/day, and about $0/day after that first week. Campaign state was not re-listed (to save Adspirer calls), so this review cannot say whether anything was paused; Blake should confirm in the Ads console that the campaigns are still enabled and eligible to serve.

## Search terms (2026-10-18 → 2026-11-16)

The report returned **10 terms**. Their spend sums to $12.66 and their clicks to 14, so they account for every click in the window. The report did not include campaign IDs. The $0.15 term matches the 7-ASIN campaign's only spend; the other $12.51 matches the Oct 18 Advent-only campaign. Product-page targets show up here as ASINs or an ISBN-10.

Titles for the ASIN/ISBN rows were read from the public Amazon product pages on 2026-11-16 (not from Adspirer).

### Converting term

| Search term | Impr | Clicks | Spend | Sales | Orders | ACOS |
|---|---|---|---|---|---|---|
| advent calendar | 1,609 | 4 | $3.77 | $35.98 | 2 | 10% |

Both sales came from **advent calendar**. CPC on this term was $3.77 ÷ 4 = $0.94. Against $8 royalty this term is profitable (about $4.23 net). No other term had a sale.

### Terms with spend and no sales

None of these have 5 or more clicks (Amazon's usual bar for cutting a term is about 20 clicks). Five have **more than $1 spend and no sale**. Data is thin; the proposals below treat off-intent terms more firmly than close, on-theme terms.

| Search term | What it is | Impr | Clicks | Spend | Notes |
|---|---|---|---|---|---|
| advent calendar for adults | keyword | 118 | 2 | $1.81 | Closest cousin of the converting term; already a planned Exact keyword in `amazon-ads.md`. Do **not** negate yet. |
| 8167282538 | ISBN-10 / product page: *Mystery Advent Calendar for Adults* by Alistair Penhurst, $15.99 | 13 | 1 | $1.12 | Close adult competitor. One click is not enough to negate. |
| b0hmpmtppv | *The Killer Kept the Receipt* (Josephine Thorne) — adult murder-mystery advent puzzle, $12.99 | 1 | 1 | $1.10 | Close adult competitor. Watch, don't negate yet. |
| book advent calendar | keyword | 445 | 1 | $1.09 | On-theme, decent impression volume. Do **not** negate yet. |
| brain games for adults | keyword | 1 | 1 | $1.09 | Generic, not Advent-specific. Best keyword negative. |
| b0hlslpdtg | *Who Stole the Advent Calendar?* (S.S. Calloway) — kids ages 8–12, $13.49 | 1 | 1 | $0.86 | Wrong audience. Good negative product target. |
| b0hmnm8l4r | *The Hollybrook Christmas Village Murder* (Casebreaker Books) — adult mystery advent, $14.99 | 21 | 1 | $0.86 | Close adult competitor (strong seller). Watch, don't negate yet. |
| b0hjzjfcv9 | *Family Games Advent Calendar* (Ananda tales) — family games, reading age 5+, $14.47 | 2 | 1 | $0.81 | Family games, not an adult puzzle book. Good negative product target. |
| activity books about buildings adults | keyword | 1 | 1 | $0.15 | Matches the 7-ASIN campaign's only click. Odd / off-theme; low priority if that campaign is paused. |

Waste outside the converting term is **$8.89** with 10 clicks and 0 sales.

## Proposed changes (not applied)

Do not raise the Advent daily budget. A 35.2% ACOS on a 22.2% break-even offer will lose money faster if spend scales as-is. The $20/day cap is not the problem; delivery has already stalled, and the converting term is profitable while everything else is not.

1. **Harvest the winner.** Create a new paused Exact-match manual Sponsored Products campaign for The Advent Clock (B0HMW1MR5T) and add **advent calendar** as Exact at a starting bid of **$0.80** (winning auto CPC on this term was about $0.94; $0.80 should stay competitive without copying the wasteful ~$1 CPC on other auto clicks). After Blake launches it, add **advent calendar** as a negative Exact on the Oct 18 Advent auto so the two campaigns do not bid against each other.

2. **Add these negatives** to the Oct 18 Advent auto (`47473767889736`), and to the newer Advent auto if it stays on:
   - Negative Exact keyword: **brain games for adults**
   - Negative product targets: **B0HLSLPDTG** (kids 8–12 advent mystery) and **B0HJZJFCV9** (family games advent, ages 5+)
   - Do **not** negate *advent calendar for adults* or *book advent calendar* yet (on-theme, 1–2 clicks only). Optionally add both as Exact in the new manual campaign at a lower test bid of **$0.50**, still paused for Blake's go-ahead.

3. **Pause two campaigns:**
   - Pause the Oct 18 7-ASIN auto (`277628141714115`, $5/day). It is a catch-all duplicate of the per-book campaigns, and its only click was a $0.15 off-theme term.
   - Pause the newer Auto - Advent Clock HC (`161403826749231`, $4/day, $0.40 default bid). It has 71 impressions and no clicks, and it competes with the only campaign that has sold. Keep the Oct 18 Advent-only auto (`47473767889736`) running — that is the campaign that produced both sales.

4. **Lower the auto bid on the winning Advent campaign**, rather than raising its budget. Observed CPC is about $0.96, which is too high for non-converting clicks when royalty is about $4. Aim for a typical CPC of about **$0.50–$0.60** on the remaining auto traffic (this review does not know the current default bid, so the change should be made by inspecting that bid in the console first). Close adult competitor product pages (Penhurst, Thorne, Hollybrook) can stay in auto for now; revisit after more than one click each.

5. **Do not raise budgets on Bridges, Porch Swing, or Stories We Keep.** After the 7-ASIN campaign is paused, optionally raise those three default bids from $0.40 to **$0.50** so they can actually serve, then review in two weeks. No converting terms exist for them yet.

6. **Confirm delivery.** Because spend has been flat since the Oct 26 review, check in the Amazon Ads console that the kept campaigns are still enabled, that billing is in good standing, and that they are eligible to serve before December demand picks up.

If Blake approves, apply this list and nothing else.

## Changes applied 2026-11-17

Blake approved all proposed changes ("Yes, make all the ad changes"). Applied via Adspirer (`profile_id` 427992898389565) starting about 1:03 AM PT. No budgets were raised. Nothing new was enabled. Amazon Ads console was not signed into.

**Adspirer quota:** started this apply at **10 / 15** used (5 remaining). Ended at **15 / 15** (0 remaining). Resets **2026-11-19**. This apply used 5 successful quota calls (4 writes + 1 list) plus one write that was refused at the cap. `list_tools` and `get_usage_status` are free and were not counted.

### Succeeded

1. **Negative exact keyword on Oct 18 Advent-only auto (`47473767889736`), campaign level:**
   - `brain games for adults` — keyword ID `252174178167038`, state ENABLED (the negative is on; the campaign was not newly enabled).
2. **Negative product targets on the same campaign, campaign level:**
   - `B0HLSLPDTG` (*Who Stole the Advent Calendar?*, kids 8–12) — target ID `90163849354708`
   - `B0HJZJFCV9` (*Family Games Advent Calendar*, ages 5+) — target ID `36445487422042`
3. **Paused two campaigns** (`pause_amazon_campaigns` returned "Updated: 2"):
   - Oct 18 7-ASIN auto `277628141714115`
   - Auto - Advent Clock HC `161403826749231`
4. **Created new manual Exact-match campaign, left PAUSED:**
   - Name: `Exact - Advent Clock HC`
   - Campaign ID: `49035542833902`
   - Ad group ID: `162109319537166`
   - ASIN: `B0HMW1MR5T`
   - Daily budget: $5 (not enabled)
   - Bidding: Dynamic bids – down only
   - Keywords (3): `advent calendar` Exact $0.80; `advent calendar for adults` Exact $0.50; `book advent calendar` Exact $0.50
   - State: **PAUSED**. Do not resume until Blake says to launch it. If it is resumed later, also confirm the ad group and product ad are enabled or it will not serve.
5. **Negative exact keyword `advent calendar` on Oct 18 Advent-only auto (`47473767889736`), campaign level** — keyword ID `209752362864803`, so the auto campaign will not bid against the new Exact campaign once that campaign is launched.

### Failed / not applied (quota exhausted)

6. **Default bid changes were not applied.** `list_amazon_ad_groups` succeeded and confirmed current bids, but `update_amazon_ad_groups` was refused with "You've used all 15 tool calls this billing period." The refusal means the write did not run; nothing was retried. Current values and the intended one-call update after the **2026-11-19** reset:

| Campaign | Campaign ID | Ad group ID | Current default bid | Intended bid |
|---|---|---|---|---|
| Oct 18 auto – Advent only | `47473767889736` | `468958781138144` | **$0.75** (still ENABLED) | **$0.55** |
| Auto - Stories We Keep HC | `278315951110803` | `352356397158880` | $0.40 | $0.50 |
| Auto - Porch Swing Crosswords PB | `153725246462664` | `515521541065983` | $0.40 | $0.50 |
| Auto - Bridges of Frostwood PB | `112094854265272` | `281526585158354` | $0.40 | $0.50 |

The $0.55 cut on the winning Advent auto is the remaining priority-3 change. The three $0.40 → $0.50 raises are the optional priority-5 changes. Both can be done in a single `update_amazon_ad_groups` call after quota resets. Do not raise any budget. Do not enable the new Exact campaign until Blake confirms.

## Changes applied 2026-11-19

The remaining default-bid changes from the 2026-11-17 approval were applied after the Adspirer free-plan quota reset (0 / 15 at the start of this run). Applied via Adspirer (`profile_id` 427992898389565) about 10:12 AM PT. No budgets were changed. No campaign was enabled or paused in this run. Amazon Ads console was not signed into.

`list_amazon_ad_groups` confirmed the Nov 17 values were still in place (Advent auto $0.75, Stories / Porch Swing / Bridges $0.40). One batched `update_amazon_ad_groups` call then succeeded for all 4 ad groups:

| Campaign | Campaign ID | Ad group ID | Previous default bid | New default bid | Ad group state |
|---|---|---|---|---|---|
| Oct 18 auto – Advent only | `47473767889736` | `468958781138144` | $0.75 | **$0.55** | ENABLED (unchanged) |
| Auto - Stories We Keep HC | `278315951110803` | `352356397158880` | $0.40 | **$0.50** | ENABLED (unchanged) |
| Auto - Porch Swing Crosswords PB | `153725246462664` | `515521541065983` | $0.40 | **$0.50** | ENABLED (unchanged) |
| Auto - Bridges of Frostwood PB | `112094854265272` | `281526585158354` | $0.40 | **$0.50** | ENABLED (unchanged) |

**Exact campaign check:** `Exact - Advent Clock HC` (`49035542833902`) is already **ENABLED** (daily budget $5, MANUAL targeting). It was left paused on 2026-11-17 and was not changed in this run. Because it is on, the term "advent calendar" is being bid on there, and it remains a negative exact on the Oct 18 Advent auto.

**Adspirer quota:** started this apply at **0 / 15**. This apply used 3 quota calls (2 lists + 1 write). `list_tools`, `get_tool_schema`, and `get_usage_status` are free. Ended at **3 / 15** (12 remaining). Resets **2026-12-19**.
