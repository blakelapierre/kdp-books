"""Case 20, The Scent of Lavender: BLACK-AND-WHITE ink with the simple v1 peg-doll characters, SIMPLE ANIMATIONS (anim.py),
mid-screen question bar (Case 7+ layout), clue notebook and a "next case" end card.
Times are ORIGINAL narration times (timing-case-20.json). render.py adds the hook shift and the countdown splice.
Art: art_case20.py -> work/art-20/ (bwkit). Part sprites use part_open (no frame2).
Opening: HOOK_STYLE="scent" (render.py): the title rippling as curling scent trails drift up through it from a little
bottle, settling still; borderless drawer hero; three equal framed suspect cards; FOLLOW YOUR NOSE stamp.
Unlike Case 19 (ruler) and Case 18 (starfield).
Fairness: Captain Quill, Hedley and Mrs Vosper share pose, size and neutral faces; each gets the same whiff lines and smell
tag when narrated; Mrs Vosper's lavender sprig appears only when it is narrated. Only the confession shows Mrs Vosper
sheepish. KEEP_ASPECT."""
NUM, NAME = 20, "The Scent of Lavender"
STYLE = "bw"
SLUG = "standalone-03-tidewhistle-case-20-the-scent-of-lavender"
AUDIO = "standalone-03-tidewhistle-22-case-20-the-scent-of-lavender.mp3"
TIMING = "timing-case-20.json"; CLUES = "clues/case-20.json"; ART = "work/art-20"; HOOK_WAV = "assets/hooks/hook-20.wav"
QUESTION = "Who took the silver fountain pen?"
HOOK_LINES = ["Follow", "the scent"]; HOOK_EMOJI = "\U0001F443"   # nose (greyed in B&W)
HOOK_SAY = ("A silver fountain pen is taken from a velvet drawer, and three customers all had a look inside. Agnes has the "
            "best nose in Tidewhistle Cove. Can you follow it?")
HOOK_STYLE = "scent"
HOOK_STAMP = "FOLLOW YOUR NOSE"
HOOK_LABEL = "3 customers \u00b7 1 drawer \u00b7 1 nose"
HOOK_FOCUS = ((0.6, 0.5, 1.0), (0.68, 0.42, 1.35))
LINEUP_PANELS = 3
SHOW_QBAR = True
KEEP_ASPECT = True
NEXT_CARD = True
TRIM = 0.45
CUT, EXTRA = 111.4, 7.0          # after "...the solution follows." (ends ~111.16); "The Solution." ~115.66
NARR_END = 111.16
AUDIO_END = 163.7                # last word ends ~163.18
NO_CAP = {0, 1, 11, 14}          # titles, question card, "The Solution."

SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=5.2),
    # Agnes's nose: breakfast vs afternoon tea, scones a minute from burning
    dict(k="art", img="nose", t0=5.2, t1=17.1, a=(0.5, 0.5, 1.0), b=(0.68, 0.4, 1.35)),
    # Tamsin's bookshop: the pen in the velvet drawer; three customers looked in; gone
    dict(k="art", img="shop", t0=17.1, t1=39.6, a=(0.5, 0.5, 1.0), b=(0.68, 0.5, 1.35)),
    dict(k="pan", t0=39.6, t1=47.0, keys=[
        (39.6, 0, 1.15), (41.9, 0, 1.2), (42.2, 1, 1.15), (43.2, 1, 1.2), (43.5, 2, 1.15), (47.0, 2, 1.22)]),
    # Agnes bends over the drawer: lavender water
    dict(k="art", img="shop", t0=47.0, t1=57.4, a=(0.6, 0.55, 1.2), b=(0.7, 0.6, 1.4)),
    dict(k="pan", t0=57.4, t1=91.7, keys=[
        (57.4, 0, 1.15), (65.9, 0, 1.26),
        (66.3, 1, 1.15), (74.8, 1, 1.26),
        (75.2, 2, 1.15), (91.7, 2, 1.3),
    ]),
    # Mrs Vosper: "I barely glanced into that drawer"
    dict(k="art", img="talk", t0=91.7, t1=99.95, a=(0.45, 0.5, 1.1), b=(0.4, 0.45, 1.25)),
    dict(k="ask", t0=99.95, t1=115.5),
    dict(k="soltitle", t0=115.5, t1=117.7),
    dict(k="art", img="board", t0=117.7, t1=142.8, a=(0.5, 0.5, 1.0), b=(0.55, 0.5, 1.1)),
    dict(k="art", img="confess", t0=142.8, t1=163.6, a=(0.5, 0.5, 1.05), b=(0.45, 0.45, 1.2)),
    dict(k="end", t0=163.6, t1=None),
]
SHORTS = dict(tag="", p1_end=105.6, recap=(99.95, 105.3), card_t=105.1,
              suspects="Captain Quill, Hedley, or Mrs Vosper?")

def _pop(part, t, fade=0.3, s0=1.25, until=None):
    return dict(kind="sprite", part=part, show=(t, until), fade=fade, keys=[(t, dict(s=s0)), (t + 0.25, dict(s=1.0))], pivot="centre")

def _whiff(t, at, until=None):
    return dict(kind="rise", part="whiff", at=at, n=4, life=2.4, height=40, alpha=0.8, show=(t, until))

_SUS = ["s0", "s1", "s2"]
ANIM = {
    "hook": dict(art="hook", layers=[]),
    "cast": dict(art="cast", layers=[dict(kind="sprite", part=p, idle=True, blink=True) for p in _SUS]),
    "nose": dict(art="nose", layers=[
        dict(kind="sprite", part="agnes", idle=True, blink=True), _pop("tea", 9.6), _whiff(9.6, (313, 128)), _pop("scone", 14.2), _whiff(14.4, (412, 112))]),
    "shop": dict(art="shop", layers=[
        dict(kind="sprite", part="pen", show=(None, 37.9), fade=0.4), _pop("gone", 38.0),
        dict(kind="sprite", part="tamsin", idle=True, blink=True, show=(20.0, None), fade=0.4),
        _pop("three", 29.7, until=39.5),
        dict(kind="sprite", part="agnes", idle=True, blink=True, show=(47.0, None), fade=0.4),
        _whiff(49.0, (355, 238)), _pop("lav", 52.6),
    ]),
    "lineup": dict(art="lineup", layers=[
        *[dict(kind="sprite", part=p, idle=True, blink=True, nods=[t]) for p, t in zip(_SUS, (41.0, 42.3, 43.3))],
        _whiff(64.1, (120, 250)), _pop("m0", 64.1), _whiff(71.8, (632, 250)), _pop("m1", 71.8), _whiff(80.8, (1144, 250)), _pop("m2", 80.8),
        _pop("sprig", 85.1),
    ]),
    "talk": dict(art="talk", layers=[
        dict(kind="sprite", part="vosper", idle=True, blink=True, talk=dict(seg=10, quotes=True)),
        dict(kind="sprite", part="agnes", idle=True, blink=True, nods=[98.0]),
        _whiff(91.7, (150, 250)),
    ]),
    "board": dict(art="board", layers=[_pop("lav", 122.9), _pop("b2", 126.7), _pop("ring", 127.6), _pop("b0", 130.8), _pop("b1", 133.0), _pop("note", 140.8)]),
    "confess": dict(art="confess", layers=[
        dict(kind="sprite", part="vosper", idle=True, blink=True, swaps=[(0.0, "sheepish", 0.01)]),
        dict(kind="sprite", part="tamsin", idle=True, blink=True),
        _pop("pen", 145.1), _pop("ink", 156.5), _whiff(162.5, (355, 238)),
    ]),
}
