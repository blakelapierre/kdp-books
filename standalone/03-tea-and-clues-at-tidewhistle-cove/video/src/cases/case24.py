"""Case 24, The Kite Festival: BLACK-AND-WHITE ink with the simple v1 peg-doll characters, SIMPLE ANIMATIONS (anim.py),
mid-screen question bar (Case 7+ layout), clue notebook and a "next case" end card.
Times are ORIGINAL narration times (timing-case-24.json; seg 2 and 18 word times re-spread evenly, ASR had collapsed them).
Art: art_case24.py -> work/art-24/ (bwkit). Sea on the LEFT, land on the RIGHT everywhere, so the wind always blows left->right.
Opening: HOOK_STYLE="weathervane" (render.py): a weathervane arrow spins and settles pointing from SEA to LAND beside the
title, borderless beach hero, three equal suspect cards, WHICH WAY? stamp. Unlike Case 23 (glovepair) and Case 22 (toggle).
Fairness: Pip, Tamsin and Mr Penberthy share pose, size and neutral faces; equal-size tags. The wind-vs-story arrows and
the X appear only after "The Solution". Only the confession shows Penberthy sheepish. KEEP_ASPECT."""
NUM, NAME = 24, "The Kite Festival"
STYLE = "bw"
SLUG = "standalone-03-tidewhistle-case-24-the-kite-festival"
AUDIO = "standalone-03-tidewhistle-26-case-24-the-kite-festival.mp3"
TIMING = "timing-case-24.json"; CLUES = "clues/case-24.json"; ART = "work/art-24"; HOOK_WAV = "assets/hooks/hook-24.wav"
QUESTION = "What's wrong with Mr Penberthy's story?"
HOOK_LINES = ["Which way", "did it blow?"]; HOOK_EMOJI = "\U0001FA81"   # kite (greyed in B&W)
HOOK_SAY = ("A carved wooden puffin has vanished from the kite festival, and one man's story goes against the wind. "
            "Can you see why?")
HOOK_STYLE = "weathervane"
HOOK_STAMP = "WHICH WAY?"
HOOK_LABEL = "3 people \u00b7 1 breeze \u00b7 1 puffin"
HOOK_FOCUS = ((0.5, 0.5, 1.0), (0.45, 0.45, 1.3))
LINEUP_PANELS = 3
SHOW_QBAR = True
KEEP_ASPECT = True
NEXT_CARD = True
TRIM = 0.45
CUT, EXTRA = 112.75, 7.0         # after "...the solution follows." (ends ~112.6); "The Solution." ~117.4
NARR_END = 112.6
AUDIO_END = 182.4
NO_CAP = {0, 1, 11, 14}          # titles, question card, "The Solution."

SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=4.6),
    dict(k="art", img="beach", t0=4.6, t1=30.0, a=(0.5, 0.5, 1.0), b=(0.55, 0.55, 1.12)),
    dict(k="art", img="tent", t0=30.0, t1=52.4, a=(0.5, 0.5, 1.0), b=(0.5, 0.42, 1.15)),
    dict(k="pan", t0=52.4, t1=94.9, keys=[
        (52.4, 0, 1.12), (62.4, 0, 1.22),
        (62.5, 1, 1.12), (71.0, 1, 1.2),
        (71.1, 2, 1.12), (94.9, 2, 1.24),
    ]),
    dict(k="art", img="beach", t0=94.9, t1=100.6, a=(0.5, 0.5, 1.05), b=(0.45, 0.55, 1.15)),
    dict(k="ask", t0=100.6, t1=117.2),
    dict(k="soltitle", t0=117.2, t1=119.4),
    dict(k="art", img="board", t0=119.4, t1=160.9, a=(0.5, 0.5, 1.0), b=(0.5, 0.5, 1.06)),
    dict(k="art", img="confess", t0=160.9, t1=182.0, a=(0.5, 0.5, 1.05), b=(0.55, 0.45, 1.2)),
    dict(k="end", t0=182.0, t1=None),
]
SHORTS = dict(tag="", p1_end=105.9, recap=(100.6, 105.6), card_t=105.4,
              suspects="Pip, Tamsin, or Mr Penberthy?")

def _pop(part, t, fade=0.3, s0=1.25, until=None):
    return dict(kind="sprite", part=part, show=(t, until), fade=fade, keys=[(t, dict(s=s0)), (t + 0.25, dict(s=1.0))], pivot="centre")

_SUS = ["s0", "s1", "s2"]
ANIM = {
    "hook": dict(art="hook", layers=[]),
    "cast": dict(art="cast", layers=[dict(kind="sprite", part=p, idle=True, blink=True) for p in _SUS]),
    "beach": dict(art="beach", layers=[
        _pop("wind", 12.4), _pop("flags", 15.2), _pop("kites", 20.3), _pop("balloon", 26.1),
        dict(kind="sprite", part="agnes", idle=True, blink=True, show=(95.0, None), fade=0.3), _pop("still", 98.32),
        dict(kind="fly", part="gull", area=(18, 200, 160, 360), n=2, speed=(12, 22), flap=2.2, size=(0.5, 0.85), seed=7)]),
    "tent": dict(art="tent", layers=[
        dict(kind="sprite", part="puffin", show=(None, 46.2), fade=0.4), _pop("prize", 31.78),
        _pop("lobster", 44.36), _pop("gone", 46.69),
        dict(kind="sprite", part="agnes", idle=True, blink=True, show=(48.73, None), fade=0.3)]),
    "lineup": dict(art="lineup", layers=[
        *[dict(kind="sprite", part=p, idle=True, blink=True, talk=w) for p, w in zip(_SUS, ([], [], [(79.54, 93.9)]))],
        _pop("kite", 54.66), _pop("p0", 59.6), _pop("p1", 66.38), _pop("p2", 73.7), _pop("said", 83.42),
    ]),
    "board": dict(art="board", layers=[
        _pop("wind", 123.46), _pop("story", 137.66), _pop("r0", 147.68), _pop("r1", 150.5), _pop("ring", 155.38)]),
    "confess": dict(art="confess", layers=[
        dict(kind="sprite", part="pen", idle=True, blink=True, swaps=[(0.0, "sheepish", 0.01)]),
        _pop("bag", 163.5), _pop("second", 167.62), _pop("joke", 177.96),
    ]),
}
