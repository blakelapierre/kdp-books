"""Case 3, The Dry Raincoat: COLOUR-DETAILED version (render.py / make_shorts.py --case=3-color).
Same narration, hook audio, clue notebook, scene timings and Shorts cuts as the black-and-white cases/case03.py;
only the art (art_case03_color.py -> work/art-03-color/: colour washes + detailed people3.py characters), the
frame/notebook style (colour) and the output names differ, so the black-and-white files are never overwritten:
  ../standalone-03-tidewhistle-case-03-the-dry-raincoat-color-vertical.mp4 / -color-wide.mp4
  ../shorts/standalone-03-tidewhistle-case-03-the-dry-raincoat-color-short-part1.mp4 / -part2.mp4"""
from cases.case03 import *          # noqa: F401,F403  (NUM, NAME, SLUG, AUDIO, TIMING, CLUES, HOOK_*, SCENES, CUT, ...)
from cases import case03 as _bw
STYLE = "color-detailed"
ART = "work/art-03-color"
VARIANT = "color"
VIDEO_SLUG = _bw.SLUG + "-color"
SHORTS = dict(_bw.SHORTS, tag="color-")

# Fix for the door-bell shots: the base config pushes in on cy=0.72 (image y runs DOWN, so that is the floor end)
# and the bell over the door (art y ~0.14 from the top) never comes into shot. Push up towards the bell instead.
SCENES = [dict(sc) for sc in _bw.SCENES]
for _sc in SCENES:
    if _sc.get("img") == "bell":
        if _sc["t0"] < _bw.CUT: _sc["a"], _sc["b"] = (0.5, 0.5, 1.08), (0.5, 0.36, 1.55)
        else: _sc["a"], _sc["b"] = (0.5, 0.36, 1.45), (0.5, 0.5, 1.1)
    if _sc.get("img") == "compare": _sc["b"] = (0.6, 0.56, 1.25)   # keep the two nameplates in shot at the end of the push
