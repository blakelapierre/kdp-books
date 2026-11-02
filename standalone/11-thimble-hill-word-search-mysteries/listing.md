# KDP listing draft: *The Thimble Hill Word Search Mysteries*

> Draft only. Nothing has been published or submitted to KDP. Step-by-step publishing checklist: [README.md](README.md).

**Format: paperback** (Monday paperback slot). Started earlier as an unfinished folder (puzzles generated and verified); finished, illustrated, typeset and covered on 2026-11-02.

## Title
**The Thimble Hill Word Search Mysteries**

## Subtitle
**60 Cozy Word Search Puzzles with a Hidden Clue in Every Grid | 10 Gentle Village Mysteries to Solve | Large 12 × 12 Grids, Full Solutions**

## Author
**Blake La Pierre** (matches the title page, copyright page, front cover and spine). No co-authors.

## Series
Standalone (not Frostwood). New puzzle type for the catalog: story-led hidden-message word searches. Different from the rejected 2026-09-30 plain winter/autumn word search ideas (those were themed word-search collections with no story), and *The Advent Clock* used only two word searches.

## Description
The copy-paste HTML is in [README.md](README.md#3-copy-paste-fields).

## Keywords (7 slots)
1. cozy mystery word search puzzle book adults
2. word search with hidden message clue
3. whodunit word search story puzzles
4. gentle mystery puzzle book for seniors
5. detective word find book no murder
6. cozy village mystery activity book gift
7. word search 6x9 travel size with solutions

## Suggested categories
- Humor & Entertainment › Puzzles & Games › Word Search
- Humor & Entertainment › Puzzles & Games › Word Games
- Humor & Entertainment › Puzzles & Games › Logic & Brain Teasers (optional third)

## Demand evidence (public Amazon pages, researched 2026-11-02)
- *Murder Among the Stacks* (Adams Media, Cranberry Creek Book 1 of 5, 150722527X): BSR **#803 in Books** (#6 Word Search Games, #8 Word Games, #10 Activity Books), 4.6★ from 330 ratings, 128 pp, 6 × 9, $11.98.
- *Murder on Vacation* (same series, 1507226365): BSR #10,213 (#98 Word Search Games), 4.8★ from 35 ratings, 128 pp, 6 × 9, $14.23.
- *Murder in the Hollow* (B0GXPPNMCC): BSR #303,640 (#1,939 Word Search Games), 4.7★ from 93 ratings, 146 pp, 8.5 × 11, $14.99.
- Other titles in the niche: *Who Done It Word Search* (B0863TQ1TK, 158 pp), *The Hidden Confession* (B0H59NMH4Q, $9.99, 114 pp), *CRIMESEARCH* (1996805045), *Murder Mystery Word Search 120 Cold Case* (B0GYQ1HZZH).
- **Gap:** every leader found is murder-themed. No gentle, non-violent cozy word-search mystery (missing things, kind reasons) was found at 6 × 9 and $9.99, under the series leader's $11.98.

## Pricing
| List | Pages | Printing | Royalty (60%) |
|---|---|---|---|
| $9.99 | 118 | $1.00 + 118 × $0.012 = $2.416 | **$3.58** |

## How the puzzles work and were checked
- 12 × 12 grids, 17–24 words each. The unused letters, read left to right and top to bottom, spell that puzzle's clue.
- Gentle: right, down, diagonal down-right. Curious: adds diagonal up-right. Sharp-Eyed: all eight directions.
- `src/gen.py` builds the grids; `src/verify.py` independently re-solves each one: every word appears exactly once, only in its level's directions, the leftover letters match the clue exactly, and no offensive words appear in any direction. Result: all 60 pass ([verification.md](verification.md)).
