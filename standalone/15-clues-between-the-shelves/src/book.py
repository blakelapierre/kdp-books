"""Assembles the book text (front matter, twenty-eight bookshop cases, back matter). Shared by build.py and verify.py."""
from cases_a import CASES_A
from cases_b import CASES_B

TITLE = "Clues Between the Shelves"
SUBTITLE = ("Twenty-Eight Cozy Bookshop Mini-Mysteries to Solve by Ear: Gentle Solve-It-Yourself Cases "
            "from an Independent Bookshop, with the Answer After Every Pause")
BOOK_SUBTITLE = "Twenty-Eight Cozy Bookshop Mysteries to Solve by Ear"
AUTHOR = "Blake La Pierre"
PREFIX = "standalone-15-clues-between-the-shelves"

CASES = CASES_A + CASES_B

NUM_WORDS = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
             "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen",
             "Eighteen", "Nineteen", "Twenty", "Twenty-One", "Twenty-Two", "Twenty-Three",
             "Twenty-Four", "Twenty-Five", "Twenty-Six", "Twenty-Seven", "Twenty-Eight"]

ASK = "Can you solve it?"
THINK = "Think about it..."
THINK_AFTER = "Take a moment, or pause here if you are listening. When you are ready, the solution follows."

def paras(text):
    return [" ".join(p.split()) for p in text.strip().split("\n\n") if p.strip()]

HOW_TO = """
Welcome to Willow Quill Books.

Willow Quill Books is a small independent bookshop on a quiet corner of Maple Lane, with tall windows, creaking floorboards, a cat named Quill who prefers the mystery shelf, and a kettle that is almost always warm. It is run by Iris Quill, who knows every regular by their favourite genre, who remembers which customer takes sugar in tea and which one never does, and who has a habit of noticing the little things other people miss. Her helper Theo Vale shelves the new arrivals, wraps gifts in brown paper and string, runs special orders to the post office, and asks the questions Iris has already answered in her head.

Outside, Maple Lane smells of rain and Nora Peake's cafe next door. Inside, the shop smells of paper, polish and whatever cake someone has brought to share. There is a window seat for lingering, a back room for book clubs and reading circles, a locked glass case for special copies, and a holds shelf that causes more gentle mix-ups than Iris likes to admit.

And the bookshop has a great many little mysteries. A cookbook turns up in travel. A bookmark goes missing. Two tote bags are swapped at the counter. A special order ends up in the wrong hands. A cat turns on a lamp. Nobody in this book ever comes to any harm, and nothing truly terrible happens. There are only missing books, mis-shelved clues, borrowed items, mixed-up orders, small fibs, lost bookmarks and swapped bags — the gentle, puzzling things that happen in any bookshop, if you keep your eyes open.
"""

HOW_PLAY = """
How to listen, and how to play.

This book is made for reading aloud or listening through, one short chapter at a time, on a commute, at a kitchen table, or in a bath that has gone lukewarm because you would not pause the chapter. Each chapter is a mini-mystery set in or around Willow Quill Books, and every clue you need is in the story. Nothing important is kept back until the end.

When the story is finished, you will hear the words Can you solve it, and a question. Then comes a pause, marked Think about it. If you are reading, look away from the page for a moment. If you are listening, press pause. Talk it over. Who did it, where is it, or what really happened?

When you are ready, read on or press play again. The solution comes straight after the pause and explains every clue, the way Iris would explain it to Theo while the kettle boiled.

Most cases turn on something somebody said, noticed, or left behind — a coffee ring, a paint fleck, a label under a label. A few are little logic puzzles, where you weigh up who sat where, who stood in which order, or who is telling the truth. Those cases repeat the key facts just before the question, so that you do not have to remember everything at once.

Some cases are easy, and some will make you think twice. If you get one wrong, that is part of being a bookshop detective. Iris gets things wrong too, sometimes, usually right before she gets them right. Quill the cat never admits to getting anything wrong at all.
"""

NAMES_NOTE = """
Iris Quill, Theo Vale, Quill the cat, and every regular who walks through the door of Willow Quill Books are made up for this book, and so is the shop itself, with its maple-lane windows and creaking shelves. You will meet Pearl of the book club, Owen the history teacher, Clara the poet, Mabel with her knitting, Nora from the cafe, Benji the mailman, Ruth the retired librarian, Sam the gardener, Jules the art teacher, Pip who helps at the cafe, Harper the travel writer, Greta from the bakery, Marcus the architect, Dot from the antique shop, Linnea the florist and Edna from the choir. Any resemblance to a real bookshop or person is only the shared cosiness of a place that smells of paper and tea.
"""

CLOSING = """
The lights are low on Maple Lane. Quill the cat is asleep on the mystery shelf, one paw over a paperback he has no intention of paying for. Theo has locked the till, counted the special-order slips twice, and set the umbrella stand straight. Iris has one last cup of tea before she turns the sign to Closed.

Thank you for spending time between the shelves. If these mysteries made your evenings a little cosier, a short review on Amazon would mean a great deal. It helps other readers and listeners find the book, and it tells me Iris and Theo should open the door again for another season of quiet puzzles.

Until then, keep your eyes open. There is a small mystery waiting on every shelf, and the kettle is almost always warm.
"""

ABOUT = """
Blake La Pierre is an independent puzzle maker who writes cozy, gentle puzzle books: snowy lodges, seaside tea rooms, candlelit riddles, village post offices, and now a little independent bookshop. Every book is clean and kind, with nothing frightening in it at all, and every puzzle is checked so that the clues point to one fair answer.
"""

COPYRIGHT = [
    f"{TITLE}",
    f"Copyright \u00a9 2026 {AUTHOR}. All rights reserved.",
    "No part of this book may be reproduced in any form without written permission from the author, except for brief quotations in a review.",
    "This is a work of fiction. Willow Quill Books, Maple Lane, and every person in these stories are imaginary. Any resemblance to real people or places is coincidental.",
    "First edition, 2026.",
]

def case_heading(i, c):
    return f"Case {NUM_WORDS[i]}: {c['title']}"

def sections():
    """Return list of (id, heading, [(kind, text)]) in reading order. kind: p, ask, think."""
    out = []
    out.append(("howto", "How to Listen and How to Play",
                [("p", t) for t in paras(HOW_TO)] + [("p", t) for t in paras(HOW_PLAY)]))
    out.append(("names", "Willow Quill Books", [("p", t) for t in paras(NAMES_NOTE)]))
    for i, c in enumerate(CASES):
        blocks = [("p", t) for t in paras(c["story"])]
        blocks.append(("ask", ASK + " " + c["ask"].strip()))
        blocks.append(("think", THINK))
        blocks.append(("p", THINK_AFTER))
        blocks.append(("ask", "The solution."))
        blocks += [("p", t) for t in paras(c["solution"])]
        out.append((f"case{i+1:02d}", case_heading(i, c), blocks))
    out.append(("closing", "Closing Time", [("p", t) for t in paras(CLOSING)]))
    out.append(("about", "About the Author", [("p", t) for t in paras(ABOUT)]))
    return out

def all_text(include_copyright=True):
    parts = [TITLE, BOOK_SUBTITLE, AUTHOR] + (COPYRIGHT if include_copyright else [])
    for _id, h, blocks in sections():
        parts.append(h)
        parts += [t for _, t in blocks]
    return "\n".join(parts)
