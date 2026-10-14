"""Case 18: COLOUR-DETAILED version (render.py / make_shorts.py --case=18-color). Same narration, hook, clues,
timings and Shorts cuts as cases/case18.py; art is art_case18.py drawn with TW_KIT_STYLE=color-detailed
(TW_ART_SUFFIX=-color -> work/art-18-color). Outputs carry a -color suffix, so the B&W files are kept."""
from cases.case18 import *          # noqa: F401,F403
from cases import case18 as _bw
STYLE = "color-detailed"
ART = _bw.ART + "-color"
VARIANT = "color"
VIDEO_SLUG = _bw.SLUG + "-color"
SHORTS = dict(getattr(_bw, "SHORTS", {}), tag="color-")
