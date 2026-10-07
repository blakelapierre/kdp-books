"""Case 16, The Lighthouse Path: BLACK-AND-WHITE ink with the simple v1 peg-doll characters, SIMPLE ANIMATIONS (anim.py),
mid-screen question bar (Case 7+ layout), clue notebook and a "next case" end card.
Times are ORIGINAL narration times (timing-case-16.json). render.py adds the hook shift and the countdown splice.
Art: art_case16.py -> work/art-16/ (bwkit). Part sprites use part_open (no frame2).
Opening: HOOK_STYLE="stopwatch" (render.py): the title beside a big stopwatch whose hand sweeps a fifteen-minute wedge,
borderless hero of the lighthouse on the point, three equal framed suspect cards, DO THE MATHS stamp.
Unlike Case 15 (wiper) and Case 14 (keyhole).
Fairness: Wenna, Mr Opie and Pip share pose, size and neutral faces; each gets two identical sighting tags and one path
time; the plain recap table has no marks. Only the confession shows Mr Opie sheepish. KEEP_ASPECT: crops match the view."""
NUM, NAME = 16, "The Lighthouse Path"
STYLE = "bw"
SLUG = "standalone-03-tidewhistle-case-16-the-lighthouse-path"
AUDIO = "standalone-03-tidewhistle-18-case-16-the-lighthouse-path.mp3"
TIMING = "timing-case-16.json"; CLUES = "clues/case-16.json"; ART = "work/art-16"; HOOK_WAV = "assets/hooks/hook-16.wav"
QUESTION = "Who could reach the lighthouse in time?"
HOOK_LINES = ["Who could", "make it?"]; HOOK_EMOJI = "\u23F1\uFE0F"   # stopwatch (greyed in B&W)
HOOK_SAY = ("A brass telescope vanishes from the lighthouse in fifteen minutes flat. Three people, six sightings, and steep "
            "paths up to the point. Who could make it in time?")
HOOK_STYLE = "stopwatch"
HOOK_STAMP = "DO THE MATHS"
HOOK_LABEL = "3 people \u00b7 6 sightings \u00b7 15 minutes"
HOOK_FOCUS = ((0.6, 0.4, 1.0), (0.7, 0.36, 1.15))
LINEUP_PANELS = 3
SHOW_QBAR = True
KEEP_ASPECT = True
NEXT_CARD = True
TRIM = 0.45
CUT, EXTRA = 129.5, 7.0          # after "...the solution follows." (ends ~129.27); "The Solution." ~133.77
NARR_END = 129.27
AUDIO_END = 213.1                # last word ends ~212.5; MP3 is ~214 s
NO_CAP = {0, 1, 11, 14}          # titles, question card, "The Solution."

SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=5.1),
    # the old lighthouse on the point, now a little museum; Hedley the keeper
    dict(k="art", img="museum", t0=5.1, t1=10.9, a=(0.55, 0.5, 1.0), b=(0.62, 0.48, 1.25)),
    # the lamp room and the first keeper's brass telescope; Hedley out on the gallery 2:00-2:15; it vanishes
    dict(k="art", img="lamp", t0=10.9, t1=30.9, a=(0.4, 0.55, 1.15), b=(0.5, 0.5, 1.0)),
    dict(k="pan", t0=30.9, t1=58.4, keys=[
        (30.9, 0, 1.15), (43.0, 0, 1.26),
        (43.4, 1, 1.15), (53.2, 1, 1.26),
        (53.6, 2, 1.15), (58.4, 2, 1.26),
    ]),
    # steep rocky paths: 15 / 20 / 10 minutes
    dict(k="art", img="map", t0=58.4, t1=83.6, a=(0.5, 0.5, 1.0), b=(0.5, 0.55, 1.1)),
    # Agnes, a pencil and an old receipt... does it in her head
    dict(k="art", img="agnes", t0=83.6, t1=91.8, a=(0.45, 0.55, 1.1), b=(0.5, 0.55, 1.2)),
    # the puzzle again: plain table, no marks
    dict(k="art", img="table", t0=91.8, t1=115.0, a=(0.5, 0.55, 1.0), b=(0.5, 0.55, 1.08)),
    dict(k="ask", t0=115.0, t1=133.6),
    dict(k="soltitle", t0=133.6, t1=135.7),
    dict(k="art", img="board", t0=135.7, t1=199.0, a=(0.5, 0.5, 1.0), b=(0.52, 0.5, 1.06)),
    dict(k="art", img="confess", t0=199.0, t1=212.9, a=(0.5, 0.55, 1.05), b=(0.6, 0.55, 1.2)),
    dict(k="end", t0=212.9, t1=None),
]
SHORTS = dict(tag="", p1_end=121.2, recap=(115.0, 120.9), card_t=120.7,
              suspects="Wenna, Mr Opie, or Pip?")

def _pop(part, t, fade=0.3, s0=1.25, until=None):
    return dict(kind="sprite", part=part, show=(t, until), fade=fade, keys=[(t, dict(s=s0)), (t + 0.25, dict(s=1.0))], pivot="centre")

def _gull(area=(18, 250, 494, 370), n=2, seed=3):
    return [dict(kind="fly", part="gull", area=area, n=n, speed=(12, 22), flap=2.2, size=(0.5, 0.85), seed=seed)]

_SUS = ["s0", "s1", "s2"]
ANIM = {
    "hook": dict(art="hook", layers=[]),
    "cast": dict(art="cast", layers=[dict(kind="sprite", part=p, idle=True, blink=True) for p in _SUS]),
    "museum": dict(art="museum", layers=[dict(kind="sprite", part="hedley", idle=True, blink=True, show=(8.4, None), fade=0.4)] + _gull()),
    "lamp": dict(art="lamp", layers=[
        dict(kind="sprite", part="tel", show=(None, 29.7), fade=0.5),
        dict(kind="sprite", part="gone", show=(29.8, None), fade=0.4),
        dict(kind="sprite", part="clock", swaps=[(24.9, "q", 0.4)]),
        dict(kind="sprite", part="hin", idle=True, blink=True, show=(None, 22.4), fade=0.4),
        dict(kind="sprite", part="hout", show=(22.6, 25.9), fade=0.4, bob=dict(amp=2.0, period=1.2)),
        dict(kind="sprite", part="hin2", idle=True, blink=True, show=(26.1, None), fade=0.4),
    ]),
    "lineup": dict(art="lineup", layers=[
        *[dict(kind="sprite", part=p, idle=True, blink=True, nods=[t]) for p, t in zip(_SUS, (37.7, 43.9, 53.3))],
        _pop("t00", 39.9), _pop("t01", 41.9), _pop("t10", 49.4), _pop("t11", 51.2), _pop("t20", 55.0), _pop("t21", 56.6),
    ]),
    "map": dict(art="map", layers=[_pop("m0", 70.4), _pop("m1", 73.4), _pop("m2", 76.5)]),
    "agnes": dict(art="agnes", layers=[
        dict(kind="sprite", part="agnes", idle=True, blink=True),
        _pop("receipt", 85.9),
        dict(kind="sprite", part="pencil", show=(84.9, None), fade=0.3, keys=[(87.6, dict(dy=0, rot=0)), (88.3, dict(dy=-90, rot=-20))], pivot="centre"),
        _pop("think", 89.8),
    ]),
    "table": dict(art="table", layers=[_pop("r0", 98.0), _pop("r1", 103.3), _pop("r2", 108.4)]),
    "board": dict(art="board", layers=[_pop("b0", 142.8), _pop("x0", 158.2), _pop("b1", 163.5), _pop("x1", 176.1), _pop("b2", 180.0), _pop("win", 192.6)]),
    "confess": dict(art="confess", layers=[
        dict(kind="sprite", part="opie", idle=True, blink=True, swaps=[(0.0, "sheepish", 0.01)]),
        dict(kind="sprite", part="hedley", idle=True, blink=True, nods=[207.2]),
        _pop("tues", 210.2),
    ]),
}
