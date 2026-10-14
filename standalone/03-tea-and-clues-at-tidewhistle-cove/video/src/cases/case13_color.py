"""Case 13: COLOUR-DETAILED version (render.py / make_shorts.py --case=13-color). Same narration, hook, clues,
timings and Shorts cuts as cases/case13.py; art is art_case13.py drawn with TW_KIT_STYLE=color-detailed
(TW_ART_SUFFIX=-color -> work/art-13-color). Outputs carry a -color suffix, so the B&W files are kept."""
from cases.case13 import *          # noqa: F401,F403
from cases import case13 as _bw
STYLE = "color-detailed"
ART = _bw.ART + "-color"
VARIANT = "color"
VIDEO_SLUG = _bw.SLUG + "-color"
SHORTS = dict(getattr(_bw, "SHORTS", {}), tag="color-")
