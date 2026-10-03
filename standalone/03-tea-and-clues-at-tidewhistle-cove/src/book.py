"""Assembles the book text (front matter, 30 cases, back matter). Shared by build.py and verify.py."""
from cases_a import CASES_A
from cases_b import CASES_B
from cases_c import CASES_C

TITLE = "Tea and Clues at Tidewhistle Cove"
SUBTITLE = "30 Cozy Mini-Mysteries to Solve by Ear: Gentle Seaside Whodunits Where Nobody Gets Hurt, with the Answer After Every Case"
AUTHOR = "Blake La Pierre"
PREFIX = "standalone-03-tea-and-clues-at-tidewhistle-cove"
CASES = CASES_A + CASES_B + CASES_C

NUM_WORDS = ["One","Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Eleven","Twelve",
 "Thirteen","Fourteen","Fifteen","Sixteen","Seventeen","Eighteen","Nineteen","Twenty","Twenty-One",
 "Twenty-Two","Twenty-Three","Twenty-Four","Twenty-Five","Twenty-Six","Twenty-Seven","Twenty-Eight",
 "Twenty-Nine","Thirty"]

THINK = "Think about it..."
THINK_AFTER = "Take a moment, or pause here if you are listening. When you are ready, the solution follows."

def paras(text):
    return [" ".join(p.split()) for p in text.strip().split("\n\n") if p.strip()]

def heading(i, case):
    return f"Case {NUM_WORDS[i]}: {case['title']}"

WELCOME = """
Welcome to Tidewhistle Cove, a little fishing village on a rocky stretch of coast, where the gulls are cheeky, the pasties are hot, and the kettle is always on.

At the heart of the village, right on the harbour front, stands the Kettle and Gull tea room. It is run by Agnes Bell, who knows how everyone in the village takes their tea, who notices everything, and who has a habit of solving the little mysteries that come through her door.

And Tidewhistle Cove has a great many little mysteries. A prize cake goes missing from the village show. A garden gnome vanishes overnight. A parrot learns a brand new phrase. Nobody in this book ever comes to any harm, and nothing truly terrible happens. There are only missing treasures, borrowed belongings, small fibs and a great deal of tea.

Each of the thirty cases is a short story that you can read in a few minutes, or listen to in about five. Every story ends with a question: Can you solve it? Then comes a pause, marked Think about it. If you are reading, look away from the page for a moment. If you are listening, pause the recording. Every clue you need is in the story, told fairly, and every case has one clear answer. The solution follows straight after the pause, with Agnes's reasoning, step by step.

Some cases turn on a single thing that somebody says or notices. Others are little logic puzzles, where you weigh up who is telling the truth, who sat where, or who could have walked where in time. Those cases repeat the key facts just before the question, so that you don't have to remember everything at once.

The cases work well read aloud, too. Try one at the breakfast table, on a car journey, or at bedtime, and see who in your family solves it first.

So pour yourself a cup of tea, settle into your favourite chair, and step into the Kettle and Gull. Agnes has kept a table for you by the window.
"""

PEOPLE_INTRO = """
Here are some of the people you will meet in Tidewhistle Cove. Don't worry about remembering them all. Each story tells you everything you need.

Agnes Bell runs the Kettle and Gull tea room and solves the village's mysteries.

Constable Ollie Penrose is the kindly village constable, who often asks Agnes for help.

Pip Carew is a cheerful teenager who helps out at the tea room.

Captain Quill is the harbourmaster, a retired sailor with a great love of brass instruments.

Tamsin Trevelyan runs the bookshop. Jago Penhallow runs the bakery. Morwenna Day runs the flower shop. Wenna Polglaze runs the antique shop on the corner. Mr Fenwick runs the grocer's.

Hedley Truscott is the village handyman, who can fix anything but spell.

Loveday Nance lives in a cottage on the hill with her terrier, Pickle. Demelza Rowe paints watercolours of the harbour. Kerensa Hale is a keen baker.

And Biscuit is the ginger cat who lives at the Kettle and Gull, and who is far too lazy to solve anything at all.
"""

THANKS = """
Thank you for spending some time in Tidewhistle Cove. Agnes hopes you solved a few cases before she did.

If you enjoyed these mysteries, a short review on Amazon would mean a great deal. It helps other readers and listeners find the book, and it tells me that you would like to visit the Kettle and Gull again.
"""

ABOUT = """
Blake La Pierre is an independent puzzle maker who writes cozy, gentle puzzle books: snowy lodges, mountain railways, starry winter skies, and now a little seaside village with a tea room at its heart. Every book is clean and kind, with nothing frightening in it at all, and every puzzle is checked to make sure it has exactly one fair answer.
"""

COPYRIGHT = [
 f"{TITLE}",
 f"Copyright \u00a9 2026 {AUTHOR}. All rights reserved.",
 "No part of this book may be reproduced in any form without written permission from the author, except for brief quotations in a review.",
 "This is a work of fiction. Tidewhistle Cove, the Kettle and Gull, and every person in these stories are imaginary. Any resemblance to real people or places is coincidental.",
 "First edition, 2026.",
]

def sections():
    """Return list of (id, heading, [(kind, text)]) in reading order. kind: p, ask, think, h2."""
    out = []
    out.append(("welcome", "Welcome to Tidewhistle Cove", [("p", t) for t in paras(WELCOME)]))
    out.append(("people", "The People of Tidewhistle Cove", [("p", t) for t in paras(PEOPLE_INTRO)]))
    for i, c in enumerate(CASES):
        blocks = [("p", t) for t in paras(c["story"])]
        blocks.append(("ask", "Can you solve it? " + c["question"]))
        blocks.append(("think", THINK))
        blocks.append(("p", THINK_AFTER))
        blocks.append(("h2", "The Solution"))
        blocks += [("p", t) for t in paras(c["solution"])]
        out.append((f"case{i+1:02d}", heading(i, c), blocks))
    out.append(("thanks", "A Last Cup of Tea", [("p", t) for t in paras(THANKS)]))
    out.append(("about", "About the Author", [("p", t) for t in paras(ABOUT)]))
    return out

BOOK_SUBTITLE = "Thirty Cozy Mini-Mysteries to Solve by Ear"

def all_text(include_copyright=True):
    parts = [TITLE, BOOK_SUBTITLE, AUTHOR] + (COPYRIGHT if include_copyright else [])
    for _id, h, blocks in sections():
        parts.append(h)
        parts += [t for _, t in blocks]
    return "\n".join(parts)
