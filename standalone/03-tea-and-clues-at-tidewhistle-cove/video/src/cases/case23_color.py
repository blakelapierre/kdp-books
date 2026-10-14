"""Case 23: COLOUR-DETAILED version (render.py / make_shorts.py --case=23-color). Same narration, hook, clues,
timings and Shorts cuts as cases/case23.py; art is art_case23.py drawn with TW_KIT_STYLE=color-detailed
(TW_ART_SUFFIX=-color -> work/art-23-color). Outputs carry a -color suffix, so the B&W files are kept."""
from cases.case23 import *          # noqa: F401,F403
from cases import case23 as _bw
STYLE = "color-detailed"
ART = _bw.ART + "-color"
VARIANT = "color"
VIDEO_SLUG = _bw.SLUG + "-color"
SHORTS = dict(getattr(_bw, "SHORTS", {}), tag="color-")
