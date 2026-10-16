"""Assembles the book text (front matter, ten rounds of riddles, back matter). Shared by build.py and verify.py."""
from rounds_01_05 import ROUNDS_A
from rounds_06_10 import ROUNDS_B

TITLE = "Three Clues by Candlelight"
SUBTITLE = ("150 Cozy What-Am-I Riddles in Three Clues Each: Kitchen, Garden, "
            "Bookstore and Fireside Guessing for Adults and Families, with the Answer After Every Pause")
BOOK_SUBTITLE = "One Hundred Fifty Cozy What-Am-I Riddles in Three Clues Each"
AUTHOR = "Blake La Pierre"
PREFIX = "standalone-07-three-clues-by-candlelight"

ROUNDS = ROUNDS_A + ROUNDS_B

ROUND_WORDS = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"]
RIDDLE_WORDS = [
    "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
    "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen",
]

THINK = "Think about it..."
THINK_AFTER = "Take a moment, or pause here if you are listening. When you are ready, the answer follows."

def paras(text):
    return [" ".join(p.split()) for p in text.strip().split("\n\n") if p.strip()]

HOW_TO = """
Welcome to Candlewick Hollow, a quiet little village tucked among low hills, where the cottages keep their lamps lit early and the evenings smell of beeswax and woodsmoke.

In the middle of the village stands a stone cottage with leaded windows and a garden that never quite sleeps. Its sitting room is the heart of these pages: a round table, a circle of chairs, and a thick white candle that burns low while friends take turns guessing. The game is simple, and it works just as well read aloud on a car journey or whispered at bedtime.

Each riddle is a What Am I. You will hear three clues. The first is the hardest, the second opens the door a little wider, and the third almost gives the game away. Then comes a pause, marked Think about it. If you are reading, look away from the page. If you are listening, pause the recording. Every answer is fair: the three clues alone point to one clear everyday thing. The answer follows straight after the pause, with a short cozy fact or tip.

There are ten themed rounds and fifteen riddles in each round, one hundred fifty in all. The themes wander through a cottage evening: the kitchen cupboard, the herb garden, the rainy window, the bookstore shelf, the fireside, the sewing basket, the porch at dusk, the market basket, the attic trunk, and the candlelit table.

Nothing in this book is frightening. There are no mysteries of crime, only the quiet pleasure of naming the teapot, the bookmark, the firefly and the quilt.

So light a candle, or imagine one, settle in, and take the first clue.
"""

NAMES_NOTE = """
Candlewick Hollow is an imaginary village. The cottage, the garden and every object in these riddles are made up for the game. Any resemblance to a real place is only the shared comfort of a warm room on a cool evening.
"""

HOW_PLAY = """
How to listen, and how to play.

One person reads a riddle aloud, stopping after Clue Three at the line Think about it. Everyone else guesses. When you are ready, the reader continues to the answer.

You may also play alone with a book or an audiobook. Pause after Think about it, then press play again for the answer.

Clues get easier as they go. If you guess on Clue One, tip your hat. If you need all three, that is the design. The answer is always something ordinary you could find in a cozy cottage life.

Names of rounds and riddle numbers are spoken as words in the body of the book, so a narrator can read them smoothly. Round and riddle titles may still use arabic numerals on the page for a clear table of contents.
"""

CLOSING = """
The candle on the table has burned down to a soft pool of wax, and the last riddle has found its answer. Thank you for sitting a while in Candlewick Hollow.

If these three-clue rounds made you smile, a short review on Amazon would mean a great deal. It helps other readers and listeners find the book, and it tells me you would like another evening by the candle.

Until then, keep a spare candle on the shelf, and keep guessing.
"""

ABOUT = """
Blake La Pierre is an independent puzzle maker who writes cozy, gentle puzzle books: snowy lodges, mountain railways, seaside tea rooms, and now a candlelit cottage full of What-Am-I riddles. Every book is clean and kind, with nothing frightening in it at all, and every puzzle is checked so that it has exactly one fair answer.
"""

COPYRIGHT = [
    f"{TITLE}",
    f"Copyright \u00a9 2026 {AUTHOR}. All rights reserved.",
    "No part of this book may be reproduced in any form without written permission from the author, except for brief quotations in a review.",
    "This is a work of fiction for a guessing game. Candlewick Hollow and every setting in these riddles are imaginary. Any resemblance to real people or places is coincidental.",
    "First edition, 2026.",
]

def round_heading(i, round_meta):
    return f"Round {ROUND_WORDS[i]}: {round_meta['title']}"

def riddle_heading(j):
    return f"Riddle {j + 1}"

def sections():
    """Return list of (id, heading, [(kind, text)]) in reading order. kind: p, ask, think, h2."""
    out = []
    out.append(("howto", "How to Listen and How to Play",
                [("p", t) for t in paras(HOW_TO)] + [("p", t) for t in paras(HOW_PLAY)]))
    out.append(("names", "Names and Places",
                [("p", t) for t in paras(NAMES_NOTE)]))
    for i, rnd in enumerate(ROUNDS):
        blocks = []
        if rnd.get("intro"):
            blocks += [("p", t) for t in paras(rnd["intro"])]
        for j, r in enumerate(rnd["riddles"]):
            blocks.append(("h2", riddle_heading(j)))
            if r.get("scene"):
                blocks.append(("p", r["scene"].strip()))
            blocks.append(("p", "Clue One. " + r["clue1"].strip()))
            blocks.append(("p", "Clue Two. " + r["clue2"].strip()))
            blocks.append(("p", "Clue Three. " + r["clue3"].strip()))
            blocks.append(("think", THINK))
            blocks.append(("p", THINK_AFTER))
            blocks.append(("ask", "The answer is " + r["answer"].strip() + "."))
            blocks.append(("p", r["fact"].strip()))
        out.append((f"round{i+1:02d}", round_heading(i, rnd), blocks))
    out.append(("closing", "The Candle Burns Low", [("p", t) for t in paras(CLOSING)]))
    out.append(("about", "About the Author", [("p", t) for t in paras(ABOUT)]))
    return out

def all_text(include_copyright=True):
    parts = [TITLE, BOOK_SUBTITLE, AUTHOR] + (COPYRIGHT if include_copyright else [])
    for _id, h, blocks in sections():
        parts.append(h)
        parts += [t for _, t in blocks]
    return "\n".join(parts)

def all_riddles():
    return [r for rnd in ROUNDS for r in rnd["riddles"]]
