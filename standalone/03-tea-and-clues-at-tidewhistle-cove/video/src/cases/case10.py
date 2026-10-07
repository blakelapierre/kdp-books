"""Case 10, The Wet Paint Bench: BLACK-AND-WHITE ink (Blake's preference for Cases 10+) with the simple v1 peg-doll
characters, SIMPLE ANIMATIONS (anim.py), mid-screen question bar (Case 7+ layout) and a "next case" end card.
Times are ORIGINAL narration times (timing-case-10.json, whole-file whisper alignment). render.py adds the hook shift
and the countdown splice. Art: art_case10.py -> work/art-10/ (bwkit). Part sprites use part_open (no frame2).
Opening: HOOK_STYLE="wetpaint" (render.py) — swinging hand-painted sign title with paint drips, borderless harbour hero
(fresh green bench + empty lifeboat-station step), three equal luggage-tag suspect cards, ONE ALIBI CRACKS stamp.
Deliberately unlike Case 8 (chalk statements) and Case 9 (compass).
Fairness: Hedley, Wenna and Mr Kemp share pose, size and neutral faces until the solution; only the confession shows
Mr Kemp sheepish. KEEP_ASPECT: crops match the view (no stretch)."""
NUM, NAME = 10, "The Wet Paint Bench"
STYLE = "bw"
SLUG = "standalone-03-tidewhistle-case-10-the-wet-paint-bench"
AUDIO = "standalone-03-tidewhistle-12-case-10-the-wet-paint-bench.mp3"
TIMING = "timing-case-10.json"; CLUES = "clues/case-10.json"; ART = "work/art-10"; HOOK_WAV = "assets/hooks/hook-10.wav"
QUESTION = "Who took the lifeboat collection box?"
HOOK_LINES = ["Who took the", "lifeboat box?"]; HOOK_EMOJI = "\U0001F58C"   # paintbrush (greyed in B&W)
HOOK_SAY = ("A lifeboat collection box has vanished on a freshly painted afternoon. Three alibis, and only one of "
            "them cracks. Can you spot it?")
HOOK_STYLE = "wetpaint"
HOOK_STAMP = "ONE ALIBI CRACKS"
HOOK_LABEL = "3 alibis \u00b7 1 missing box \u00b7 1 crack"
HOOK_FOCUS = ((0.55, 0.45, 1.02), (0.62, 0.36, 1.22))   # push toward the empty lifeboat-station step
LINEUP_PANELS = 3
SHOW_QBAR = True
KEEP_ASPECT = True
NEXT_CARD = True
TRIM = 0.45
CUT, EXTRA = 110.45, 7.0        # after "...the solution follows." (ends ~110.24); "The Solution." ~114.74
NARR_END = 110.24
AUDIO_END = 171.2                # last word ends ~170.9; MP3 is ~173.4 s
NO_CAP = {0, 1, 11, 14}          # titles, question card, "The Solution."

SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=5.0),
    # Hedley paints the benches; WET PAINT signs pop on "sign on each one"
    dict(k="art", img="harbour", t0=5.0, t1=22.6, a=(0.42, 0.42, 1.05), b=(0.4, 0.38, 1.3)),
    # "Six hours, it says on the tin"
    dict(k="art", img="tin", t0=22.6, t1=28.0, a=(0.5, 0.45, 1.1), b=(0.5, 0.42, 1.25)),
    # lifeboat station steps + the collection box
    dict(k="art", img="station", t0=28.0, t1=38.0, a=(0.5, 0.45, 1.0), b=(0.62, 0.32, 1.45)),
    # gone at four
    dict(k="art", img="station", t0=38.0, t1=42.8, a=(0.66, 0.3, 1.5), b=(0.68, 0.3, 1.7)),
    # Agnes and Ollie ask around
    dict(k="art", img="quay", t0=42.8, t1=48.6, a=(0.45, 0.45, 1.05), b=(0.45, 0.42, 1.2)),
    # equal lineup: Hedley / Wenna / Mr Kemp
    dict(k="pan", t0=48.6, t1=77.3, keys=[
        (48.6, 0, 1.15), (62.6, 0, 1.26),
        (63.3, 1, 1.15), (71.8, 1, 1.26),
        (72.4, 2, 1.15), (77.3, 2, 1.26),
    ]),
    # Mr Kemp's statement by the bench
    dict(k="art", img="kemp", t0=77.3, t1=90.6, a=(0.4, 0.45, 1.1), b=(0.42, 0.42, 1.3)),
    # the shining wet bench ... then the spotless cream trousers
    dict(k="art", img="bench", t0=90.6, t1=98.8, a=(0.34, 0.4, 1.25), b=(0.76, 0.3, 1.7)),
    dict(k="ask", t0=98.8, t1=114.6),
    dict(k="soltitle", t0=114.6, t1=116.8),
    dict(k="art", img="board", t0=116.8, t1=141.6, a=(0.5, 0.55, 1.05), b=(0.55, 0.6, 1.2)),
    dict(k="art", img="board", t0=141.6, t1=153.3, a=(0.55, 0.6, 1.2), b=(0.5, 0.55, 1.0)),
    # the box in the boot of Mr Kemp's car; coins back + a generous note
    dict(k="art", img="confess", t0=153.3, t1=171.0, a=(0.45, 0.42, 1.05), b=(0.5, 0.4, 1.2)),
    dict(k="end", t0=171.0, t1=None),
]
SHORTS = dict(tag="", p1_end=104.6, recap=(99.1, 104.5), card_t=104.2,
              suspects="Hedley, Wenna, or Mr Kemp?")

def _gull(area=(18, 250, 494, 370), n=2, seed=3):
    return [dict(kind="fly", part="gull", area=area, n=n, speed=(12, 22), flap=2.2, size=(0.5, 0.85), seed=seed)]

def _pop(part, t, fade=0.3, s0=1.25):
    return dict(kind="sprite", part=part, show=(t, None), fade=fade, keys=[(t, dict(s=s0)), (t + 0.25, dict(s=1.0))], pivot="centre")

_SUS = ["s0", "s1", "s2"]
ANIM = {
    "hook": dict(art="hook", layers=[*_gull(area=(18, 290, 494, 370), n=2, seed=1)]),
    "cast": dict(art="cast", layers=[dict(kind="sprite", part=p, idle=True, blink=True) for p in _SUS]),
    "harbour": dict(art="harbour", layers=[
        dict(kind="sprite", part="hedley", idle=True, blink=True, keys=[(5.0, dict(rot=0)), (9.0, dict(rot=-2)), (9.6, dict(rot=1.5)), (10.2, dict(rot=-2)), (10.8, dict(rot=0))]),
        _pop("sign1", 14.3), _pop("sign2", 14.9),
        *_gull(seed=5),
    ]),
    "tin": dict(art="tin", layers=[
        dict(kind="sprite", part="hedley", idle=True, blink=True, talk=dict(seg=3, quotes=True)),
        dict(kind="sprite", part="agnes", idle=True, blink=True, nods=[26.6]),
    ]),
    "station": dict(art="station", layers=[
        dict(kind="sprite", part="box", show=(None, 41.4), fade=0.45),
        *_gull(seed=7),
    ]),
    "quay": dict(art="quay", layers=[
        dict(kind="sprite", part="agnes", idle=True, blink=True, talk=[(44.6, 46.4)]),
        dict(kind="sprite", part="ollie", idle=True, blink=True, nods=[45.8]),
        *_gull(seed=9),
    ]),
    "lineup": dict(art="lineup", layers=[
        *[dict(kind="sprite", part=p, idle=True, blink=True, nods=[t]) for p, t in zip(_SUS, (49.2, 63.6, 72.6))],
        dict(kind="sprite", part="ollie", idle=True, blink=True),
        dict(kind="sprite", part="agnes", idle=True, blink=True),
    ]),
    "kemp": dict(art="kemp", layers=[
        dict(kind="sprite", part="kemp", idle=True, blink=True, talk=dict(seg=9, quotes=True)),
        dict(kind="sprite", part="agnes", idle=True, blink=True),
    ]),
    "bench": dict(art="bench", layers=[
        dict(kind="glint", part="sparkle", area=(70, 100, 280, 170), n=7, life=1.6, drift=0.0, seed=4),
        dict(kind="sprite", part="kemp", idle=True, blink=True),
    ]),
    "board": dict(art="board", layers=[
        _pop("stripes", 133.6, fade=0.4),
        _pop("x", 139.4, fade=0.35),
    ]),
    "confess": dict(art="confess", layers=[
        dict(kind="sprite", part="kemp", idle=True, blink=True, swaps=[(0.0, "sheepish", 0.01)]),
        dict(kind="sprite", part="ollie", idle=True, blink=True, nods=[167.2]),
        _pop("note", 168.6, fade=0.35),
    ]),
}
