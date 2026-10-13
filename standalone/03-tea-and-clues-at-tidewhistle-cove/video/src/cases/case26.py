"""Case 26, The Winning Ticket: BLACK-AND-WHITE ink with the simple v1 peg-doll characters, SIMPLE ANIMATIONS (anim.py),
mid-screen question bar (Case 7+ layout), clue notebook and a "next case" end card. A queue-order logic case.
Times are ORIGINAL narration times (timing-case-26.json). render.py adds the hook shift and the countdown splice.
Art: art_case26.py -> work/art-26/ (bwkit). Part sprites use part_open (no frame2).
Opening: HOOK_STYLE="queueslots" (render.py): five numbered queue places (FRONT = 1); a raffle ticket tumbles in and drops
between places 3 and 4, where a "?" appears; borderless tea-stall hero; four equal suspect cards; WHO PICKED IT UP? stamp.
Unlike Case 25 (spooncount) and Case 24 (weathervane).
Fairness: the queue is drawn as anonymous outlines; the four suspects share pose, size and neutral faces; the THE QUEUE
board is filled only after "The Solution". Only the confession shows Demelza pink. KEEP_ASPECT."""
NUM, NAME = 26, "The Winning Ticket"
STYLE = "bw"
SLUG = "standalone-03-tidewhistle-case-26-the-winning-ticket"
AUDIO = "standalone-03-tidewhistle-28-case-26-the-winning-ticket.mp3"
TIMING = "timing-case-26.json"; CLUES = "clues/case-26.json"; ART = "work/art-26"; HOOK_WAV = "assets/hooks/hook-26.wav"
QUESTION = "Who stood directly behind Loveday?"
HOOK_LINES = ["Who was", "behind her?"]; HOOK_EMOJI = "\U0001F39F"   # admission ticket (greyed in B&W)
HOOK_SAY = ("A winning raffle ticket blew away in a queue of five, and somebody else claimed the prize. Who picked it up?")
HOOK_STYLE = "queueslots"
HOOK_STAMP = "WHO PICKED IT UP?"
HOOK_LABEL = "5 in a queue \u00b7 4 clues \u00b7 1 ticket"
HOOK_FOCUS = ((0.5, 0.5, 1.0), (0.4, 0.45, 1.3))
LINEUP_PANELS = 4
SHOW_QBAR = True
KEEP_ASPECT = True
NEXT_CARD = True
TRIM = 0.45
CUT, EXTRA = 103.45, 7.0         # after "...the solution follows." (ends ~103.3); "The Solution." ~108.2
NARR_END = 103.3
AUDIO_END = 166.4
NO_CAP = {0, 1, 8, 11}           # titles, question card, "The Solution."

SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=4.6),
    dict(k="art", img="fair", t0=4.6, t1=18.4, a=(0.5, 0.5, 1.0), b=(0.45, 0.45, 1.12)),
    dict(k="art", img="queue", t0=18.4, t1=49.5, a=(0.5, 0.5, 1.0), b=(0.5, 0.5, 1.1)),
    dict(k="pan", t0=49.5, t1=62.0, keys=[
        (49.5, 0, 1.12), (52.3, 0, 1.18),
        (52.4, 1, 1.12), (54.3, 1, 1.16),
        (54.4, 2, 1.12), (55.6, 2, 1.15),
        (55.7, 3, 1.12), (62.0, 3, 1.22),
    ]),
    dict(k="art", img="clues", t0=62.0, t1=75.4, a=(0.5, 0.5, 1.0), b=(0.45, 0.5, 1.08)),
    dict(k="art", img="board", t0=75.4, t1=90.8, a=(0.5, 0.5, 1.0), b=(0.5, 0.5, 1.05)),
    dict(k="ask", t0=90.8, t1=108.1),
    dict(k="soltitle", t0=108.1, t1=110.3),
    dict(k="art", img="board", t0=110.3, t1=146.0, a=(0.5, 0.5, 1.0), b=(0.5, 0.55, 1.06)),
    dict(k="art", img="confess", t0=146.0, t1=166.2, a=(0.45, 0.5, 1.05), b=(0.5, 0.5, 1.15)),
    dict(k="end", t0=166.2, t1=None),
]
SHORTS = dict(tag="", p1_end=96.1, recap=(90.8, 95.8), card_t=95.6,
              suspects="Mr Fenwick, Pip, Demelza, or Hedley?")

def _pop(part, t, fade=0.3, s0=1.25, until=None):
    return dict(kind="sprite", part=part, show=(t, until), fade=fade, keys=[(t, dict(s=s0)), (t + 0.25, dict(s=1.0))], pivot="centre")

_SUS = ["s0", "s1", "s2", "s3"]
ANIM = {
    "hook": dict(art="hook", layers=[]),
    "cast": dict(art="cast", layers=[dict(kind="sprite", part=p, idle=True, blink=True) for p in _SUS]),
    "fair": dict(art="fair", layers=[_pop("hamper", 7.6), dict(kind="sprite", part="loveday", idle=True, blink=True, show=(10.58, None), fade=0.3),
        _pop("ticket", 13.04)]),
    "queue": dict(art="queue", layers=[
        _pop("gust", 24.06, until=28.0), _pop("ground", 28.14, until=33.9), _pop("behind", 31.04),
        _pop("draw", 37.26), _pop("other", 41.68), _pop("pickle", 47.9)]),
    "lineup": dict(art="lineup", layers=[dict(kind="sprite", part=p, idle=True, blink=True) for p in _SUS]),
    "clues": dict(art="clues", layers=[
        dict(kind="sprite", part="agnes", idle=True, blink=True, talk=[(62.1, 74.4)]),
        _pop("c0", 63.48), _pop("c1", 66.98), _pop("c2", 69.78), _pop("c3", 74.34)]),
    "board": dict(art="board", layers=[
        _pop("r0", 81.12), _pop("r1", 83.12), _pop("r2", 85.54), _pop("r3", 89.44),
        _pop("q0", 115.78), _pop("q2", 120.46), _pop("x5", 129.48), _pop("x2", 132.8), _pop("q3", 134.38), _pop("ring", 135.58),
        _pop("q1", 143.48), _pop("q4", 144.56)]),
    "confess": dict(art="confess", layers=[
        dict(kind="sprite", part="dem", idle=True, blink=True, swaps=[(0.0, "sheepish", 0.01)]),
        dict(kind="sprite", part="lov", idle=True, blink=True), _pop("thought", 152.1), _pop("ham", 160.12), _pop("share", 161.48)]),
}
