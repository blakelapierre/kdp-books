"""Case 22, The Honest Fishermen: BLACK-AND-WHITE ink with the simple v1 peg-doll characters, SIMPLE ANIMATIONS (anim.py),
mid-screen question bar (Case 7+ layout), clue notebook and a "next case" end card.
Times are ORIGINAL narration times (timing-case-22.json). render.py adds the hook shift and the countdown splice.
Art: art_case22.py -> work/art-22/ (bwkit). Part sprites use part_open (no frame2).
Opening: HOOK_STYLE="toggle" (render.py): a big TRUE / FIB switch flicks back and forth beside the title and sticks on "?",
borderless harbour-wall hero, three equal suspect cards, HONEST OR FIBBER? stamp.
Unlike Case 21 (coinflip) and Case 20 (scent).
Fairness: Ned, Bran and Col share pose, size and neutral faces and each gets the same speech card when he speaks.
The HONEST / FIBBER tags appear on the board only after "The Solution". Only the confession shows Bran sheepish. KEEP_ASPECT."""
NUM, NAME = 22, "The Honest Fishermen"
STYLE = "bw"
SLUG = "standalone-03-tidewhistle-case-22-the-honest-fishermen"
AUDIO = "standalone-03-tidewhistle-24-case-22-the-honest-fishermen.mp3"
TIMING = "timing-case-22.json"; CLUES = "clues/case-22.json"; ART = "work/art-22"; HOOK_WAV = "assets/hooks/hook-22.wav"
QUESTION = "Who took Captain Quill's net?"
HOOK_LINES = ["Who's telling", "the truth?"]; HOOK_EMOJI = "\U0001F3A3"   # fishing pole (greyed in B&W)
HOOK_SAY = ("In Tidewhistle Cove, every fisherman always tells the truth, or never does. Captain Quill's net is gone, and three "
            "fishermen have something to say. Who's fibbing?")
HOOK_STYLE = "toggle"
HOOK_STAMP = "HONEST OR FIBBER?"
HOOK_LABEL = "3 fishermen \u00b7 3 statements \u00b7 1 net"
HOOK_FOCUS = ((0.5, 0.55, 1.0), (0.48, 0.45, 1.3))
LINEUP_PANELS = 3
SHOW_QBAR = True
KEEP_ASPECT = True
NEXT_CARD = True
TRIM = 0.45
CUT, EXTRA = 94.75, 7.0          # after "...the solution follows." (ends ~94.55); "The Solution." ~99.05
NARR_END = 94.55
AUDIO_END = 162.2                # last word ends ~161.74
NO_CAP = {0, 1, 10, 13}          # titles, question card, "The Solution."

SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=5.2),
    # two kinds of fishermen: HONEST / FIBBER signs on the quay
    dict(k="art", img="rules", t0=5.2, t1=24.4, a=(0.5, 0.5, 1.0), b=(0.5, 0.6, 1.15)),
    # Captain Quill's brand new net vanished from the harbour wall; exactly one of three took it
    dict(k="art", img="wall", t0=24.4, t1=36.5, a=(0.45, 0.5, 1.0), b=(0.55, 0.55, 1.2)),
    # Agnes and the saffron buns; she doesn't know who is honest
    dict(k="art", img="tea", t0=36.5, t1=49.9, a=(0.5, 0.5, 1.0), b=(0.48, 0.42, 1.1)),
    dict(k="pan", t0=49.9, t1=61.5, keys=[
        (49.9, 0, 1.12), (53.9, 0, 1.22),
        (54.0, 1, 1.12), (56.4, 1, 1.2),
        (56.5, 2, 1.12), (61.5, 2, 1.24),
    ]),
    dict(k="art", img="tea", t0=61.5, t1=66.0, a=(0.5, 0.42, 1.08), b=(0.5, 0.42, 1.15)),
    # "Here are the statements again" -> the statement board (no marks yet)
    dict(k="art", img="board", t0=66.0, t1=83.5, a=(0.5, 0.5, 1.0), b=(0.45, 0.6, 1.12)),
    dict(k="ask", t0=83.5, t1=98.85),
    dict(k="soltitle", t0=98.85, t1=101.17),
    dict(k="art", img="board", t0=101.17, t1=144.9, a=(0.5, 0.5, 1.0), b=(0.5, 0.5, 1.05)),
    dict(k="art", img="confess", t0=144.9, t1=162.1, a=(0.45, 0.5, 1.05), b=(0.55, 0.5, 1.2)),
    dict(k="end", t0=162.1, t1=None),
]
SHORTS = dict(tag="", p1_end=88.8, recap=(83.5, 88.5), card_t=88.3,
              suspects="Ned, Bran, or Col?")

def _pop(part, t, fade=0.3, s0=1.25, until=None):
    return dict(kind="sprite", part=part, show=(t, until), fade=fade, keys=[(t, dict(s=s0)), (t + 0.25, dict(s=1.0))], pivot="centre")

_SUS = ["s0", "s1", "s2"]
ANIM = {
    "hook": dict(art="hook", layers=[]),
    "cast": dict(art="cast", layers=[dict(kind="sprite", part=p, idle=True, blink=True) for p in _SUS]),
    "rules": dict(art="rules", layers=[_pop("g0", 9.48), _pop("g1", 14.54), _pop("never", 21.38),
        dict(kind="fly", part="gull", area=(18, 250, 494, 370), n=2, speed=(12, 22), flap=2.2, size=(0.5, 0.85), seed=5)]),
    "wall": dict(art="wall", layers=[
        dict(kind="sprite", part="quill", idle=True, blink=True),
        dict(kind="sprite", part="net", show=(None, 26.7), fade=0.4), _pop("gone", 26.75), _pop("one", 32.0)]),
    "tea": dict(art="tea", layers=[
        dict(kind="sprite", part="agnes", idle=True, blink=True),
        _pop("buns", 38.36), _pop("know", 41.92, until=49.9), _pop("bun", 62.56)]),
    "lineup": dict(art="lineup", layers=[
        *[dict(kind="sprite", part=p, idle=True, blink=True, talk=[w]) for p, w in zip(_SUS, ((50.4, 53.24), (54.7, 56.03), (57.5, 60.67)))],
        _pop("p0", 50.08), _pop("p1", 54.10), _pop("p2", 56.60),
    ]),
    "board": dict(art="board", layers=[
        _pop("r0", 68.1), _pop("r1", 71.16), _pop("r2", 73.06),
        _pop("test", 105.8), _pop("cross", 118.34), _pop("t2", 121.84), _pop("t0", 125.4), _pop("t1", 131.5),
        _pop("false", 137.7), _pop("ring", 143.2)]),
    "confess": dict(art="confess", layers=[
        dict(kind="sprite", part="bran", idle=True, blink=True, swaps=[(0.0, "sheepish", 0.01)]),
        _pop("holes", 147.34), _pop("borrow", 153.22), _pop("mend", 156.94),
    ]),
}
