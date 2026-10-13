"""Case 28, Truth and Fib Night: BLACK-AND-WHITE ink with the simple v1 peg-doll characters, SIMPLE ANIMATIONS (anim.py),
mid-screen question bar (Case 7+ layout), clue notebook and a "next case" end card. A one-truth-one-fib logic case.
Times are ORIGINAL narration times (timing-case-28.json). render.py adds the hook shift and the countdown splice.
Art: art_case28.py -> work/art-28/ (bwkit). Part sprites use part_open (no frame2).
Opening: HOOK_STYLE="cardflip" (render.py): two cards spin through TRUE / FIB and land one TRUE, one FIB ("1 truth + 1 fib");
borderless hall hero with the empty cake stand; four equal suspect cards; ONE TRUTH, ONE FIB stamp.
Unlike Case 27 (foghorn) and Case 22 (toggle switch).
Fairness: the four share pose, size, neutral faces and identical speech cards; tests, X marks and T/F tags only after
"The Solution". KEEP_ASPECT."""
NUM, NAME = 28, "Truth and Fib Night"
STYLE = "bw"
SLUG = "standalone-03-tidewhistle-case-28-truth-and-fib-night"
AUDIO = "standalone-03-tidewhistle-30-case-28-truth-and-fib-night.mp3"
TIMING = "timing-case-28.json"; CLUES = "clues/case-28.json"; ART = "work/art-28"; HOOK_WAV = "assets/hooks/hook-28.wav"
QUESTION = "Who took the chocolate cake?"
HOOK_LINES = ["One truth,", "one fib."]; HOOK_EMOJI = "\U0001F370"   # cake (greyed in B&W)
HOOK_SAY = ("On Truth and Fib Night, a chocolate cake vanishes, and four suspects each tell one truth and one fib. Who took it?")
HOOK_STYLE = "cardflip"
HOOK_STAMP = "ONE TRUTH, ONE FIB"
HOOK_LABEL = "4 suspects \u00b7 8 statements \u00b7 1 cake"
HOOK_FOCUS = ((0.5, 0.5, 1.0), (0.5, 0.4, 1.3))
LINEUP_PANELS = 4
SHOW_QBAR = True
KEEP_ASPECT = True
NEXT_CARD = True
TRIM = 0.45
CUT, EXTRA = 104.75, 7.0         # after "...the solution follows." (ends ~104.6); "The Solution." ~109.1
NARR_END = 104.6
AUDIO_END = 182.2
NO_CAP = {0, 1, 12, 15}          # titles, question card, "The Solution."

SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=4.7),
    dict(k="art", img="hall", t0=4.7, t1=23.4, a=(0.5, 0.5, 1.0), b=(0.5, 0.45, 1.1)),
    dict(k="art", img="table", t0=23.4, t1=48.6, a=(0.5, 0.45, 1.0), b=(0.5, 0.45, 1.15)),
    dict(k="art", img="hall", t0=48.6, t1=55.6, a=(0.6, 0.45, 1.1), b=(0.65, 0.45, 1.18)),
    dict(k="pan", t0=55.6, t1=76.0, keys=[
        (55.6, 0, 1.12), (59.9, 0, 1.18),
        (60.0, 1, 1.12), (63.9, 1, 1.18),
        (64.0, 2, 1.12), (67.9, 2, 1.18),
        (68.0, 3, 1.12), (76.0, 3, 1.22),
    ]),
    dict(k="art", img="board", t0=76.0, t1=93.6, a=(0.5, 0.5, 1.0), b=(0.5, 0.5, 1.05)),
    dict(k="ask", t0=93.6, t1=108.9),
    dict(k="soltitle", t0=108.9, t1=111.2),
    dict(k="art", img="board", t0=111.2, t1=166.7, a=(0.5, 0.5, 1.0), b=(0.5, 0.5, 1.06)),
    dict(k="art", img="confess", t0=166.7, t1=182.0, a=(0.5, 0.5, 1.05), b=(0.5, 0.45, 1.15)),
    dict(k="end", t0=182.0, t1=None),
]
SHORTS = dict(tag="", p1_end=98.9, recap=(93.6, 98.6), card_t=98.4,
              suspects="Hedley, Kerensa, Wenna, or Tamsin?")

def _pop(part, t, fade=0.3, s0=1.25, until=None):
    return dict(kind="sprite", part=part, show=(t, until), fade=fade, keys=[(t, dict(s=s0)), (t + 0.25, dict(s=1.0))], pivot="centre")

_SUS = ["s0", "s1", "s2", "s3"]
ANIM = {
    "hook": dict(art="hook", layers=[]),
    "cast": dict(art="cast", layers=[dict(kind="sprite", part=p, idle=True, blink=True) for p in _SUS]),
    "hall": dict(art="hall", layers=[_pop("april", 6.46, until=23.4), _pop("rule", 18.96, until=23.4),
        dict(kind="sprite", part="agnes", idle=True, blink=True, show=(49.1, None), fade=0.3, talk=[(51.6, 54.7)])]),
    "table": dict(art="table", layers=[dict(kind="sprite", part="cake", show=(None, 35.0), fade=0.4), _pop("gone", 35.2), _pop("four", 46.3)]),
    "lineup": dict(art="lineup", layers=[
        *[dict(kind="sprite", part=p, idle=True, blink=True, talk=[w]) for p, w in zip(_SUS, ((56.9, 59.0), (61.2, 63.0), (64.9, 66.9), (69.1, 71.2)))],
        _pop("p0", 57.2), _pop("p1", 61.5), _pop("p2", 65.3), _pop("p3", 69.5)]),
    "board": dict(art="board", layers=[
        _pop("r0", 78.14), _pop("r1", 81.2), _pop("r2", 83.48), _pop("r3", 86.9),
        _pop("inn", 121.2), _pop("x0", 140.56), _pop("x1", 147.16), _pop("x2", 150.78), _pop("tags", 159.2), _pop("ring", 165.4)]),
    "confess": dict(art="confess", layers=[
        dict(kind="sprite", part="tam", idle=True, blink=True, swaps=[(0.0, "sheepish", 0.01)]),
        _pop("cake", 168.76), _pop("best", 174.4), _pop("share", 179.66)]),
}
