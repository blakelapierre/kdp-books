"""Assembles the book text (front matter, twenty-four road trip cases, back matter). Shared by build.py and verify.py."""
from cases_a import CASES_A
from cases_b import CASES_B

TITLE = "The Backseat Detectives"
SUBTITLE = ("24 Road Trip Mysteries to Solve Out Loud: Cozy Read-Aloud Puzzle Stories for Kids, Families "
            "and Car Rides, with the Answer After Every Pause")
BOOK_SUBTITLE = "Twenty-Four Road Trip Mysteries to Solve Out Loud"
AUTHOR = "Blake La Pierre"
PREFIX = "standalone-10-the-backseat-detectives"

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
Meet the Backseat Detectives.

June is eleven. She notices everything: a smear of icing, a crooked sticker, a feather on a windowsill. Theo is eight. He asks about everything, and sometimes his questions crack a case wide open. Every summer they ride in the back of Biscuit, their grandparents' cream-coloured camper van, for a long, slow road trip with Grandpa Gus at the wheel, Grandma Rosie with the map and the snacks, and Pickles the dog asleep on whoever's feet are nearest.

Somehow, wherever Biscuit stops, there is a small mystery waiting. A missing pie. A lost ticket. A price tag in the wrong place. Nothing frightening ever happens, and nobody is ever hurt. These are the kind of puzzles you could find at any gas station, diner or campground, if you kept your eyes open.

This book holds twenty-four of those cases, in the order the family met them, from the first morning in the driveway to the last afternoon back home.
"""

HOW_PLAY = """
How to listen, and how to play.

Each case is a short story. Listen carefully, because every clue you need is in the story. Nothing important is hidden until the end.

When the story is finished, you will hear the words Can you solve it, and a question. Then comes a pause, marked Think about it. If you are reading aloud, stop there and let everyone guess. If you are listening to the audiobook, press pause. Talk it over. Who did it, or where is it, or what really happened? Try to say why, too, because a good detective can always point to the clue.

When you are ready, read on or press play again. The solution comes straight after the pause and explains every clue.

You can play with the whole car, take turns being the reader, or keep score if you like. Some cases are easy, and some will make the grown-ups think hard. If you get one wrong, that is part of being a detective. June gets things wrong too, sometimes. Usually right before she gets them right.
"""

NAMES_NOTE = """
June, Theo, Grandpa Gus, Grandma Rosie, Pickles the dog and Biscuit the camper van are made up for this book, and so is every town, diner, campground and shop they visit. Any resemblance to a real place or person is only the shared fun of a long summer drive.
"""

CLOSING = """
Biscuit is parked in the driveway again, with sand in the floor mats and a sticky spot on the steering wheel that will never quite come off. Pickles is asleep. Grandma Rosie is wearing her new locket. And somewhere in the back seat, two detectives are already planning next summer.

Thank you for riding along. If these cases made the miles go faster, a short review on Amazon would mean a great deal. It helps other families find the book, and it tells me the Backseat Detectives should hit the road again.

Until then, keep your eyes open. There is a small mystery waiting at every stop.
"""

ABOUT = """
Blake La Pierre is an independent puzzle maker who writes cozy, gentle puzzle books: snowy lodges, mountain railways, seaside tea rooms, candlelit riddles, and now a camper van full of road trip mysteries. Every book is clean and kind, with nothing frightening in it at all, and every puzzle is checked so that the clues point to one fair answer.
"""

COPYRIGHT = [
    f"{TITLE}",
    f"Copyright \u00a9 2026 {AUTHOR}. All rights reserved.",
    "No part of this book may be reproduced in any form without written permission from the author, except for brief quotations in a review.",
    "This is a work of fiction. All characters, towns and businesses in it are imaginary. Any resemblance to real people or places is coincidental.",
    "First edition, 2026.",
]

def case_heading(i, c):
    return f"Case {NUM_WORDS[i]}: {c['title']}"

def sections():
    """Return list of (id, heading, [(kind, text)]) in reading order. kind: p, ask, think."""
    out = []
    out.append(("howto", "How to Listen and How to Play",
                [("p", t) for t in paras(HOW_TO)] + [("p", t) for t in paras(HOW_PLAY)]))
    out.append(("names", "Names and Places", [("p", t) for t in paras(NAMES_NOTE)]))
    for i, c in enumerate(CASES):
        blocks = [("p", t) for t in paras(c["story"])]
        blocks.append(("ask", ASK + " " + c["ask"].strip()))
        blocks.append(("think", THINK))
        blocks.append(("p", THINK_AFTER))
        blocks.append(("ask", "The solution."))
        blocks += [("p", t) for t in paras(c["solution"])]
        out.append((f"case{i+1:02d}", case_heading(i, c), blocks))
    out.append(("closing", "Home Again", [("p", t) for t in paras(CLOSING)]))
    out.append(("about", "About the Author", [("p", t) for t in paras(ABOUT)]))
    return out

def all_text(include_copyright=True):
    parts = [TITLE, BOOK_SUBTITLE, AUTHOR] + (COPYRIGHT if include_copyright else [])
    for _id, h, blocks in sections():
        parts.append(h)
        parts += [t for _, t in blocks]
    return "\n".join(parts)
