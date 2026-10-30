"""Assembles the book text (front matter, twenty-four Christmas nights, back matter). Shared by build.py and verify.py."""
from cases_a import CASES_A
from cases_b import CASES_B

TITLE = "Twenty-Four Nights at the Christmas Post"
SUBTITLE = ("Cozy Read-Aloud Christmas Mysteries for Kids and Families, One to Solve Every Night of December, "
            "with the Answer After Every Pause")
BOOK_SUBTITLE = "Cozy Christmas Mysteries to Solve Out Loud, One for Every Night of December"
AUTHOR = "Blake La Pierre"
PREFIX = "standalone-13-twenty-four-nights-at-the-christmas-post"

CASES = CASES_A + CASES_B

NUM_WORDS = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
             "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen",
             "Eighteen", "Nineteen", "Twenty", "Twenty-One", "Twenty-Two", "Twenty-Three", "Twenty-Four"]

ASK = "Can you solve it?"
THINK = "Think about it..."
THINK_AFTER = "Take a moment to talk it over, or pause here if you are listening. When you are ready, the answer follows."

def paras(text):
    return [" ".join(p.split()) for p in text.strip().split("\n\n") if p.strip()]

HOW_TO = """
Welcome to Bellwick.

Bellwick is a small snowy village with a church, a bakery, a frozen pond, a tall Christmas tree on the green, and a little red-brick post office run by Grandma Nell and Grandpa Walt Hartley. This December, their grandchildren are staying for the whole month. Wren is ten, and she notices everything. Felix is seven, and he asks about everything, and sometimes, without meaning to, he solves things.

Behind the post office counter hangs a big wooden calendar with twenty-four little doors, one for every night until Christmas. And every night in Bellwick, there is a small mystery. A missing carrot nose. A letter with no name. A wreath on the wrong door. Nothing frightening ever happens, and nobody is ever hurt. These are the gentle, puzzling things that happen in any village at Christmas, if you keep your eyes open.

There is one more mystery, too, that runs all the way through the month. Every night, a paper snowflake with a single letter on it appears in the calendar, and nobody will say who puts it there. Keep a note of the letters as you go. By Christmas Eve, they will spell out a message.
"""

HOW_PLAY = """
How to listen, and how to play.

This book is made for reading aloud, one chapter every night from the first of December to Christmas Eve, though you can also enjoy it all at once, any time of year. Each chapter is a short story, and every clue you need is in the story. Nothing important is kept back until the end.

When the story is finished, you will hear the words Can you solve it, and a question. Then comes a pause, marked Think about it. If you are reading aloud, stop there and let everyone guess. If you are listening to the audiobook, press pause. Talk it over. Who did it, where is it, or what really happened?

When you are ready, read on or press play again. The solution comes straight after the pause and explains every clue. At the very end of each chapter, you will hear that night's snowflake letter. Write it down, or ask someone to remember it for you.

Some nights are easy, and some will make the grown-ups think hard. If you get one wrong, that is part of being a detective. Wren gets things wrong too, sometimes, usually right before she gets them right.
"""

NAMES_NOTE = """
Wren and Felix Hartley, Grandma Nell and Grandpa Walt, Marzipan the cat, Clover the pony, Pudding the dog, and everybody else in Bellwick are made up for this book, and so is the village itself, with its post office, bakery, pond and Ivy Row. Any resemblance to a real place or person is only the shared cosiness of a snowy December.
"""

CLOSING = """
The calendar on the post office wall is empty now, all twenty-four doors open, with the ribbons hanging loose and Marzipan asleep on top. Wren's notebook is full. Felix has switched his new torch on and off so many times that Grandpa Walt has hidden the batteries. And outside, the banner in the window still says, Thank you for every kindness.

Thank you for spending December in Bellwick. If these mysteries made your evenings a little cosier, a short review on Amazon would mean a great deal. It helps other families find the book, and it tells me Wren and Felix should come back to the post office next Christmas.

Until then, keep your eyes open. There is a small mystery waiting on every snowy night.
"""

ABOUT = """
Blake La Pierre is an independent puzzle maker who writes cozy, gentle puzzle books: snowy lodges, seaside tea rooms, candlelit riddles, a camper van full of road trip mysteries, and now a little village post office at Christmas. Every book is clean and kind, with nothing frightening in it at all, and every puzzle is checked so that the clues point to one fair answer.
"""

COPYRIGHT = [
    f"{TITLE}",
    f"Copyright \u00a9 2026 {AUTHOR}. All rights reserved.",
    "No part of this book may be reproduced in any form without written permission from the author, except for brief quotations in a review.",
    "This is a work of fiction. All characters, towns and businesses in it are imaginary. Any resemblance to real people or places is coincidental.",
    "First edition, 2026.",
]

def case_heading(i, c):
    return f"Night {NUM_WORDS[i]}: {c['title']}"

def sections():
    """Return list of (id, heading, [(kind, text)]) in reading order. kind: p, ask, think."""
    out = []
    out.append(("howto", "How to Listen and How to Play",
                [("p", t) for t in paras(HOW_TO)] + [("p", t) for t in paras(HOW_PLAY)]))
    out.append(("names", "The Village of Bellwick", [("p", t) for t in paras(NAMES_NOTE)]))
    for i, c in enumerate(CASES):
        blocks = [("p", t) for t in paras(c["story"])]
        blocks.append(("ask", ASK + " " + c["ask"].strip()))
        blocks.append(("think", THINK))
        blocks.append(("p", THINK_AFTER))
        blocks.append(("ask", "The solution."))
        blocks += [("p", t) for t in paras(c["solution"])]
        out.append((f"case{i+1:02d}", case_heading(i, c), blocks))
    out.append(("closing", "After Christmas", [("p", t) for t in paras(CLOSING)]))
    out.append(("about", "About the Author", [("p", t) for t in paras(ABOUT)]))
    return out

def all_text(include_copyright=True):
    parts = [TITLE, BOOK_SUBTITLE, AUTHOR] + (COPYRIGHT if include_copyright else [])
    for _id, h, blocks in sections():
        parts.append(h)
        parts += [t for _, t in blocks]
    return "\n".join(parts)
