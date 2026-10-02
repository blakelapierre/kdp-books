"""Worked-example panels and step text. The text is written for the specific 5x5 example in data.json;
the assertion below stops the build if the example ever changes."""
import json
_EX = json.load(open("../data.json"))["Example"][0]
assert _EX["regions"] == [[1, 1, 0, 0, 0], [1, 1, 1, 0, 3], [1, 4, 2, 0, 3], [1, 4, 4, 3, 3], [4, 4, 4, 3, 3]], "example changed: rewrite example_text.py"
assert sorted(map(tuple, _EX["solution"])) == [(0, 3), (1, 0), (2, 2), (3, 4), (4, 1)]

_mid_stars = [(2, 2), (1, 0)]
_mid_dots = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2), (3, 3), (2, 0), (2, 4), (0, 2), (4, 2), (1, 4), (0, 0), (0, 1), (3, 0), (4, 0)]
EX_PANELS = [("puzzle", [], []), ("puzzle", _mid_stars, _mid_dots), ("solution", [], [])]
EX_STEPS = [
    "<b>The one-square region.</b> The region in the very middle (row 3, column 3) is a single square, so it must hold that region’s star. "
    "Dot its eight neighbours, and the rest of row 3 and column 3, because they now have their star.",
    "<b>The top-right region</b> has only two open squares left: row 1, columns 4 and 5. Whichever one gets the star, it will touch "
    "the square in row 2, column 5. So that square can’t be a star. Dot it.",
    "<b>Row 2</b> now has just one open square, in column 1, so that’s a star. It fills the big top-left region and column 1, so dot the rest of both. "
    "That is the middle picture.",
    "<b>The bottom-left region</b> has only one open square left, in row 5, column 2. Star. Row 5 is now full, so dot the rest of it.",
    "<b>The right-hand region</b> is left with one open square, in row 4, column 5. Star. Column 5 is full, so the top-right region’s star goes in row 1, column 4. "
    "Every row, column and region now has one star, and no two stars touch.",
]
