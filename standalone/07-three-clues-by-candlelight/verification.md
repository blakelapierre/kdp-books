# Verification: Three Clues by Candlelight

Run: `cd src && python3 verify.py`.

- Rounds: **10**
- Riddles: **150** (fifteen per round)
- Total words in the book text: **14,669**
- Answers: **all unique** (150 distinct)
- Structure: every riddle has Clue One, Clue Two, Clue Three, answer and fact
- Read-aloud rules: no digits in riddle bodies or front/back prose; no grids, tables, images or footnotes
- Every riddle ends with *Think about it...*, then the answer
- Content rule: no violent vocabulary; cozy household and cottage themes only

## Fairness

Each answer was written to be the unique everyday object that fits all three clues in order (harder → easier).
Verification checks uniqueness of answers across the book, required clue structure, audio-first constraints and non-violence.
Clue Three is intentionally the most specific so listeners who need all three clues still land on one clear answer.

## Round answer list

| Round | Theme | Answers |
|-------|-------|---------|
| 1 | The Kitchen Cupboard | a kettle; a wooden spoon; a salt shaker; a rolling pin; a measuring cup; a colander; a whisk; a cutting board; an oven mitt; a can opener; a grater; a ladle; a mixing bowl; a cork; an apron |
| 2 | The Herb Garden | rosemary; basil; mint; thyme; lavender; parsley; sage; chives; dill; oregano; a bay leaf; cilantro; lemon balm; chamomile; a watering can |
| 3 | The Rainy Window | an umbrella; a rain boot; a puddle; a raincoat; a windowpane; fog; a rainbow; a doormat; a weather vane; a gutter; a raindrop; a thermos; wool socks; a newspaper; hot chocolate |
| 4 | The Bookstore Shelf | a bookmark; a magnifying glass; a hardcover book; a paperback; a library card; a reading lamp; a dictionary; an atlas; a bookplate; a dust jacket; a chapter; a bookend; reading glasses; a table of contents; a novel |
| 5 | By the Fireside | a fireplace poker; a firewood log; a mantelpiece; a rocking chair; a throw blanket; the hearth; bellows; a chimney; a match; kindling; andirons; a fire screen; cocoa; a slipper; a cat |
| 6 | The Sewing Basket | a needle; a thimble; thread; sewing scissors; a button; a pincushion; a measuring tape; a spool; an embroidery hoop; a zipper; a seam ripper; a sewing pattern; yarn; a knitting needle; a snap fastener |
| 7 | The Porch at Dusk | a porch swing; a firefly; lemonade; a wind chime; a lantern; a hammock; a cricket; a bird feeder; a screen door; a flower box; a porch light; twilight; a hummingbird; an iced tea pitcher; a porch step |
| 8 | The Market Basket | a loaf of bread; an apple; cheese; a jar of honey; an egg; a tomato; a jar of jam; a fresh fish; a carrot; a pie; a strawberry; butter; a peach; a market basket; an ear of corn |
| 9 | The Attic Trunk | a photograph; a quilt; a letter; a pocket watch; a hat box; a diary; a postcard; a phonograph record; a wedding dress; a stamp collection; an old map; a music box; a locket; a steamer trunk; a kaleidoscope |
| 10 | The Candlelit Table | a candle; a candlestick; candle wax; a napkin ring; a place card; a wine glass; a fork; a tablecloth; a centerpiece; a butter dish; a salt cellar; a dessert plate; a candle snuffer; a goblet; a menu card |

## Result: **PASS**


## EPUBCheck

Not run on the build box (Java / epubcheck.jar not available). EPUB 3 was built with the same Tidewhistle pattern (reflowable, nav + NCX, mimetype stored uncompressed). Validate locally with EPUBCheck 5.x before upload if desired.
