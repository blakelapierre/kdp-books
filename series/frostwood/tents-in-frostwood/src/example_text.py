"""Worked-example panels and step text for the how-to-play pages."""
# Example is a 5×5 with trees at (1,3), (2,0), (4,2) and tents at (1,0), (2,3), (4,1).
# Panels: (mode, tents_to_draw, empties_to_dot)
EX_PANELS = [
    ("puzzle", [], []),
    ("partial", [[2, 3]],
     [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4],
      [3, 0], [3, 1], [3, 2], [3, 3], [3, 4],
      [1, 2], [1, 4], [2, 2], [2, 4], [4, 0], [4, 3], [4, 4],
      [1, 1], [1, 3],  # 1,3 is tree — skipped in draw
      ]),
    ("solution", [], []),
]

EX_STEPS = [
    "Rows 0 and 3 (counting from the top) both say <b>0</b>, and so do columns 2 and 4. Mark every square in those rows and columns empty — no tent can go there.",
    "The pine in row 1, column 3 now has only one free neighbour left: the square below it. Put a tent there. Column 3 has its one tent, so the rest of that column is empty.",
    "The pine in the bottom row (row 4, column 2) likewise has only one free neighbour: the square to its left. Put a tent there. Row 4 is done.",
    "Row 2 already has its one tent (the one under the first pine), so its other open square is empty. That leaves the pine in row 2, column 0 with a single free neighbour above it. Put the last tent there, and the meadow is settled.",
]
