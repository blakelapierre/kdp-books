"""Case 25, The Teaspoon Thief: BLACK-AND-WHITE ink with the simple v1 peg-doll characters, SIMPLE ANIMATIONS (anim.py),
mid-screen question bar (Case 7+ layout), clue notebook and a "next case" end card.
Times are ORIGINAL narration times (timing-case-25.json). render.py adds the hook shift and the countdown splice.
Art: art_case25.py -> work/art-25/ (bwkit). Part sprites use part_open (no frame2).
Opening: HOOK_STYLE="spooncount" (render.py): three silver teaspoons drop onto a tray, then vanish one by one as MON / TUE /
WED tags take their place, leaving a "?"; borderless sideboard hero; three equal suspect cards; LOCKED TIGHT? stamp.
Unlike Case 24 (weathervane) and Case 23 (glovepair).
Fairness: Pip, Mr Fenwick and Loveday share pose, size and neutral faces; equal tags. The feather is shown as narrated
(a clue); the magpie itself is drawn only after "The Solution". KEEP_ASPECT."""
NUM, NAME = 25, "The Teaspoon Thief"
STYLE = "bw"
SLUG = "standalone-03-tidewhistle-case-25-the-teaspoon-thief"
AUDIO = "standalone-03-tidewhistle-27-case-25-the-teaspoon-thief.mp3"
TIMING = "timing-case-25.json"; CLUES = "clues/case-25.json"; ART = "work/art-25"; HOOK_WAV = "assets/hooks/hook-25.wav"
QUESTION = "Who has been taking the teaspoons?"
HOOK_LINES = ["Who takes", "the spoons?"]; HOOK_EMOJI = "\U0001F944"   # spoon (greyed in B&W)
HOOK_SAY = ("Silver teaspoons keep vanishing from a locked tea room, and nothing else is ever touched. Who's the thief?")
HOOK_STYLE = "spooncount"
HOOK_STAMP = "LOCKED TIGHT?"
HOOK_LABEL = "3 helpers \u00b7 3 spoons \u00b7 1 feather"
HOOK_FOCUS = ((0.5, 0.5, 1.0), (0.5, 0.45, 1.3))
LINEUP_PANELS = 3
SHOW_QBAR = True
KEEP_ASPECT = True
NEXT_CARD = True
TRIM = 0.45
CUT, EXTRA = 112.6, 7.0          # after "...the solution follows." (ends ~112.45); "The Solution." ~116.9
NARR_END = 112.45
AUDIO_END = 185.8
NO_CAP = {0, 1, 8, 11}           # titles, question card, "The Solution."

SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=4.6),
    dict(k="art", img="tea", t0=4.6, t1=10.3, a=(0.5, 0.5, 1.0), b=(0.5, 0.5, 1.1)),
    dict(k="art", img="sideboard", t0=10.3, t1=34.0, a=(0.5, 0.55, 1.0), b=(0.5, 0.6, 1.12)),
    dict(k="art", img="sideboard", t0=34.0, t1=65.6, a=(0.5, 0.45, 1.12), b=(0.5, 0.4, 1.2)),
    dict(k="pan", t0=65.6, t1=88.4, keys=[
        (65.6, 0, 1.12), (75.9, 0, 1.22),
        (76.0, 1, 1.12), (81.3, 1, 1.2),
        (81.4, 2, 1.12), (88.4, 2, 1.22),
    ]),
    dict(k="art", img="sill", t0=88.4, t1=100.9, a=(0.5, 0.5, 1.0), b=(0.42, 0.42, 1.15)),
    dict(k="ask", t0=100.9, t1=116.8),
    dict(k="soltitle", t0=116.8, t1=119.0),
    dict(k="art", img="board", t0=119.0, t1=162.4, a=(0.5, 0.5, 1.0), b=(0.5, 0.5, 1.06)),
    dict(k="art", img="nest", t0=162.4, t1=185.6, a=(0.5, 0.5, 1.0), b=(0.6, 0.6, 1.18)),
    dict(k="end", t0=185.6, t1=None),
]
SHORTS = dict(tag="", p1_end=106.2, recap=(100.9, 105.9), card_t=105.7,
              suspects="Pip, Mr Fenwick, Loveday, or someone else?")

def _pop(part, t, fade=0.3, s0=1.25, until=None):
    return dict(kind="sprite", part=part, show=(t, until), fade=fade, keys=[(t, dict(s=s0)), (t + 0.25, dict(s=1.0))], pivot="centre")

_SUS = ["s0", "s1", "s2"]
ANIM = {
    "hook": dict(art="hook", layers=[]),
    "cast": dict(art="cast", layers=[dict(kind="sprite", part=p, idle=True, blink=True) for p in _SUS]),
    "tea": dict(art="tea", layers=[_pop("three", 7.5)]),
    "sideboard": dict(art="sideboard", layers=[
        dict(kind="sprite", part="sp0", show=(None, 35.54), fade=0.3), dict(kind="sprite", part="sp1", show=(None, 38.76), fade=0.3),
        dict(kind="sprite", part="sp2", show=(None, 40.68), fade=0.3),
        dict(kind="sprite", part="agnes", idle=True, blink=True, show=(11.6, 34.0), fade=0.3),
        _pop("keys", 20.98, until=34.0), _pop("gap", 24.34, until=34.0), _pop("nobody", 29.74, until=34.0),
        _pop("d0", 35.54), _pop("d1", 38.76), _pop("d2", 40.68), _pop("foil", 44.30),
        _pop("u0", 53.76), _pop("u1", 55.86), _pop("u2", 57.92), _pop("u3", 59.70), _pop("u4", 61.50), _pop("shiny", 63.44)]),
    "lineup": dict(art="lineup", layers=[
        *[dict(kind="sprite", part=p, idle=True, blink=True) for p in _SUS],
        _pop("p0", 72.5), _pop("p1", 78.92), _pop("p2", 85.08), _pop("pickle", 85.08),
    ]),
    "sill": dict(art="sill", layers=[
        dict(kind="sprite", part="agnes", idle=True, blink=True), _pop("feather", 95.8), _pop("fcard", 98.4)]),
    "board": dict(art="board", layers=[
        _pop("bird", 122.33), _pop("gap", 129.21), _pop("took", 139.21), _pop("left", 142.88), _pop("feather", 155.86)]),
    "nest": dict(art="nest", layers=[
        dict(kind="sprite", part="pip", idle=True, blink=True), _pop("nest", 167.92), _pop("loot", 169.52),
        _pop("bird", 172.0), _pop("thanks", 180.64),
    ]),
}
