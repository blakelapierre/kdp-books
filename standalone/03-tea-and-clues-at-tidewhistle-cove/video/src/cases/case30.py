"""Case 30, The Missing Sign (LAST CASE, book end card): BLACK-AND-WHITE ink with the simple v1 peg-doll characters, SIMPLE
ANIMATIONS (anim.py), mid-screen question bar, clue notebook. Times are ORIGINAL narration times (timing-case-30.json).
Art: art_case30.py -> work/art-30/. Opening: HOOK_STYLE="emptybracket" (render.py): empty swinging bracket, a "Back soon" bag
drops in, label flashes; borderless shopfront hero; three equal suspect cards; READ THE NOTE stamp. Unlike Case 29 (sugarlumps).
Fairness: Hedley, Tamsin and Ollie share pose, size and neutral faces; equal "how they write" tags. Board marks only after
"The Solution". Smiles only in the surprise/finale. NUM == TZ.LAST_CASE -> end card promotes the book. KEEP_ASPECT."""
NUM, NAME = 30, "The Missing Sign"
STYLE = "bw"
SLUG = "standalone-03-tidewhistle-case-30-the-missing-sign"
AUDIO = "standalone-03-tidewhistle-32-case-30-the-missing-sign.mp3"
TIMING = "timing-case-30.json"; CLUES = "clues/case-30.json"; ART = "work/art-30"; HOOK_WAV = "assets/hooks/hook-30.wav"
QUESTION = "Who took the sign, and why?"
HOOK_LINES = ["Where is", "the sign?"]; HOOK_EMOJI = "\U0001FAA7"   # placard
HOOK_SAY = ("On the tea room's tenth birthday, its sign has vanished, leaving only a bag of bolts and a note in green ink. "
            "Can you solve it?")
HOOK_STYLE = "emptybracket"
HOOK_STAMP = "READ THE NOTE"
HOOK_LABEL = "3 suspects \u00b7 1 bag \u00b7 2 words"
HOOK_FOCUS = ((0.5, 0.5, 1.0), (0.6, 0.45, 1.25))
LINEUP_PANELS = 3
SHOW_QBAR = True
KEEP_ASPECT = True
NEXT_CARD = True
TRIM = 0.45
CUT, EXTRA = 106.3, 5.0          # after "...the solution follows." (ends ~106.0); "The Solution." ~111.4
NARR_END = 106.1
AUDIO_END = 177.2
NO_CAP = {0, 1, 11, 14}

SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=4.6),
    dict(k="art", img="door", t0=4.6, t1=43.3, a=(0.5, 0.5, 1.0), b=(0.62, 0.42, 1.12)),
    dict(k="pan", t0=43.3, t1=85.0, keys=[
        (43.3, 0, 1.12), (54.4, 0, 1.22),
        (54.5, 1, 1.12), (67.6, 1, 1.18),
        (67.7, 2, 1.12), (85.0, 2, 1.22),
    ]),
    dict(k="art", img="hall", t0=85.0, t1=95.6, a=(0.5, 0.5, 1.0), b=(0.6, 0.5, 1.12)),
    dict(k="ask", t0=95.6, t1=110.9),
    dict(k="soltitle", t0=110.9, t1=113.1),
    dict(k="art", img="board", t0=113.1, t1=132.6, a=(0.5, 0.5, 1.0), b=(0.5, 0.5, 1.06)),
    dict(k="art", img="surprise", t0=132.6, t1=158.4, a=(0.45, 0.5, 1.02), b=(0.55, 0.5, 1.12)),
    dict(k="art", img="finale", t0=158.4, t1=176.9, a=(0.5, 0.5, 1.0), b=(0.66, 0.4, 1.15)),
    dict(k="end", t0=176.9, t1=None),
]
SHORTS = dict(tag="", p1_end=100.4, recap=(95.6, 100.2), card_t=100.0,
              suspects="Hedley, Tamsin, or Constable Ollie?")

def _pop(part, t, fade=0.3, s0=1.25, until=None):
    return dict(kind="sprite", part=part, show=(t, until), fade=fade, keys=[(t, dict(s=s0)), (t + 0.25, dict(s=1.0))], pivot="centre")

_SUS = ["s0", "s1", "s2"]
ANIM = {
    "hook": dict(art="hook", layers=[]),
    "cast": dict(art="cast", layers=[dict(kind="sprite", part=p, idle=True, blink=True) for p in _SUS]),
    "door": dict(art="door", layers=[dict(kind="sprite", part="agnes", idle=True, blink=True),
        _pop("gone", 13.06), _pop("bracket", 19.98), _pop("bag", 26.14, until=33.3), _pop("note", 33.78), _pop("green", 36.92)]),
    "lineup": dict(art="lineup", layers=[
        *[dict(kind="sprite", part=p, idle=True, blink=True) for p in _SUS],
        _pop("p0", 49.02), _pop("p1", 62.68), _pop("p2", 73.22)]),
    "hall": dict(art="hall", layers=[_pop("lights", 90.28)]),
    "board": dict(art="board", layers=[_pop("note", 118.98), _pop("r0", 122.56), _pop("r1", 124.80), _pop("ring", 127.46)]),
    "surprise": dict(art="surprise", layers=[dict(kind="sprite", part="ollie", idle=True, blink=True),
        _pop("crowd", 137.36), _pop("why", 150.32)]),
    "finale": dict(art="finale", layers=[dict(kind="sprite", part="agnes", idle=True, blink=True),
        _pop("sign", 159.46), _pop("words", 167.94)]),
}
