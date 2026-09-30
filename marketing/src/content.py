"""Per-book copy and crop choices used by the image builders."""

# Crop boxes are (x0, y0, x1, y1) in inches on the 6 x 9 in interior page.
TILES = {
    "the-thief-stayed-the-night": [
        (10, (0.4, 0.70, 5.6, 3.47), "register"),
        (12, (0.4, 0.70, 5.6, 3.30), "clues"),
        (14, (0.4, 0.88, 5.6, 3.20), "verdict"),
    ],
    "frostwood-express": [
        (8, (0.4, 0.75, 5.6, 4.40), "no-1-easy"),
        (34, (0.4, 0.70, 5.6, 4.45), "no-51-medium"),
        (60, (0.4, 0.70, 5.6, 8.20), "no-101-hard"),
    ],
    "stars-over-frostwood": [
        (8, (0.4, 0.85, 5.6, 4.30), "no-1-easy"),
        (30, (0.4, 0.80, 5.6, 4.35), "no-41-medium"),
        (52, (0.4, 0.80, 5.6, 8.20), "no-81-hard"),
    ],
    "the-advent-clock": [
        # Crops start below the "Door N / December N" running header, because A+ rules forbid holiday references.
        (11, (0.4, 1.08, 5.6, 8.15), "door-2-shift-code"),
        (17, (0.4, 1.08, 5.6, 8.15), "door-5-maze"),
        (23, (0.4, 1.08, 5.6, 5.80), "door-8-pigpen-code"),
    ],
}

HEADER = {
    "the-thief-stayed-the-night": dict(
        kicker="A FROSTWOOD PUZZLE BOOK  \u00b7  BOOK ONE",
        head=["Twelve Cozy Cases.", "One Snowbound Week."],
        body="Cross suspects off the guest register until only the thief remains.",
        chips=["12 cases, 40 to 152 suspects", "Hints and step-by-step solutions", "No violence, ever"]),
    "frostwood-express": dict(
        kicker="A FROSTWOOD PUZZLE BOOK  \u00b7  BOOK TWO",
        head=["Lay the Line.", "Climb the Mountain."],
        body="Build one unbroken railway from A to B in every snowy grid.",
        chips=["200 Train Tracks puzzles", "Easy 6\u00d76 to Expert 12\u00d712", "Worked example and solutions"]),
    "stars-over-frostwood": dict(
        kicker="A FROSTWOOD PUZZLE BOOK  \u00b7  BOOK THREE",
        head=["Put the Stars", "Back in the Sky."],
        body="Place stars so no two touch, not even diagonally.",
        chips=["180 Star Battle puzzles", "One-star and two-star grids", "Worked example and solutions"]),
    "the-advent-clock": dict(
        kicker="A PUZZLE COUNTDOWN IN 24 DOORS",
        head=["Twenty-Four Doors.", "One Hidden Star."],
        body="Open one door a day, solve the puzzle, and keep the key letter.",
        chips=["24 puzzles of 19 kinds", "Three hint levels for every door", "Just a pencil, no app"]),
}

WHY = {
    "the-thief-stayed-the-night": dict(
        cols=[("check", "Exactly One", "Culprit"), ("list", "Fair, Complete", "Clues"), ("bulb", "Hints and Full", "Solutions")],
        foot="Every case checked by computer  \u00b7  No violence, ever"),
    "frostwood-express": dict(
        cols=[("check", "Exactly One", "Route"), ("logic", "Logic, Not", "Guessing"), ("steps", "Easy to", "Expert")],
        foot="Every puzzle checked by computer  \u00b7  Solutions at the back"),
    "stars-over-frostwood": dict(
        cols=[("check", "Exactly One", "Solution"), ("logic", "Logic, Not", "Guessing"), ("star", "One Star to", "Two Stars")],
        foot="Every puzzle checked by computer  \u00b7  Solutions at the back"),
    "the-advent-clock": dict(
        cols=[("check", "Exactly One", "Answer"), ("bulb", "Three Hint", "Levels"), ("star", "Cozy, With", "No Crime")],
        foot="Every puzzle checked by computer  \u00b7  Just a pencil"),
}

SERIES = [
    ("the-thief-stayed-the-night", "Book One", "Elimination Mysteries"),
    ("frostwood-express", "Book Two", "Train Tracks"),
    ("stars-over-frostwood", "Book Three", "Star Battle"),
]

PINS = {
    "the-thief-stayed-the-night": dict(
        p1_kicker="A COZY MYSTERY PUZZLE BOOK", p1_head=["Can You Find", "the Thief?"],
        p2_head="Who Took the Cocoa Tin?", p2_sub="Cross off the suspects, one clue at a time",
        tile=1, box=(12, (0.4, 0.70, 5.6, 5.80))),
    "frostwood-express": dict(
        p1_kicker="TRAIN TRACKS LOGIC PUZZLES", p1_head=["Lay One Railway", "from A to B"],
        p2_head="Try This Train Tracks Puzzle", p2_sub="Numbers count the track squares in each row and column",
        tile=0),
    "stars-over-frostwood": dict(
        p1_kicker="STAR BATTLE LOGIC PUZZLES", p1_head=["Put the Stars", "Back in the Sky"],
        p2_head="Try This Star Battle Puzzle", p2_sub="One star in every row, column and region. No two stars touch",
        tile=0),
    "the-advent-clock": dict(
        p1_kicker="A 24-DAY PUZZLE COUNTDOWN", p1_head=["One Puzzle", "Behind Every Door"],
        p2_head="Door One: Can You Solve It?", p2_sub="Find every word, then read the leftover letters",
        tile=0, box=(9, (0.4, 0.70, 5.6, 5.70))),
}
