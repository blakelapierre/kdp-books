"""Case 19, The Ship's Bell: BLACK-AND-WHITE ink with the simple v1 peg-doll characters, SIMPLE ANIMATIONS (anim.py),
mid-screen question bar (Case 7+ layout), clue notebook and a "next case" end card.
Times are ORIGINAL narration times (timing-case-19.json). render.py adds the hook shift and the countdown splice.
Art: art_case19.py -> work/art-19/ (bwkit). Part sprites use part_open (no frame2).
Opening: HOOK_STYLE="ruler" (render.py): a tall measuring rule grows down the left with foot marks while a little bell
swings from a hook at its top; the title beside it; borderless club-door hero; three equal tag suspect cards; LOOK UP
stamp. Unlike Case 18 (starfield) and Case 17 (bubble).
Fairness: Loveday, Mr Fenwick and Tobias are drawn the same size, stance and neutral face; their narrated heights appear only
as identical text tags; only the confession shows Tobias sheepish. KEEP_ASPECT."""
NUM, NAME = 19, "The Ship's Bell"
STYLE = "bw"
SLUG = "standalone-03-tidewhistle-case-19-the-ships-bell"
AUDIO = "standalone-03-tidewhistle-21-case-19-the-ships-bell.mp3"
TIMING = "timing-case-19.json"; CLUES = "clues/case-19.json"; ART = "work/art-19"; HOOK_WAV = "assets/hooks/hook-19.wav"
QUESTION = "Who took the ship's bell?"
HOOK_LINES = ["Who could", "reach it?"]; HOOK_EMOJI = "\U0001F514"   # bell (greyed in B&W)
HOOK_SAY = ("A brass ship's bell vanishes from a hook so high, nobody can easily reach it. No ladder, nothing to stand on, "
            "and three people at quiz night. Look up, and work it out.")
HOOK_STYLE = "ruler"
HOOK_STAMP = "LOOK UP"
HOOK_LABEL = "3 quizzers \u00b7 1 high hook \u00b7 no ladder"
HOOK_FOCUS = ((0.5, 0.45, 1.0), (0.5, 0.3, 1.35))
LINEUP_PANELS = 3
SHOW_QBAR = True
KEEP_ASPECT = True
NEXT_CARD = True
TRIM = 0.45
CUT, EXTRA = 102.4, 7.0          # after "...the solution follows." (ends ~102.2); "The Solution." ~106.7
NARR_END = 102.2
AUDIO_END = 159.5                # last word ends ~158.94
NO_CAP = {0, 1, 12, 15}          # titles, question card, "The Solution."

SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=4.95),
    # the brass bell above the sailing club door, so high even the tallest must stretch on tiptoe
    dict(k="art", img="door", t0=4.95, t1=22.45, a=(0.5, 0.5, 1.0), b=(0.5, 0.3, 1.4)),
    # Tobias Ferris, lifeboat crew, 6 1/2 ft, ducks through doorways
    dict(k="art", img="lb", t0=22.45, t1=32.45, a=(0.5, 0.5, 1.0), b=(0.55, 0.45, 1.25)),
    # the locked ladder cupboard, Agnes's only key, the broken stool
    dict(k="art", img="porch", t0=32.45, t1=53.15, a=(0.3, 0.5, 1.2), b=(0.65, 0.5, 1.15)),
    # Sunday morning: the hook is empty
    dict(k="art", img="door", t0=53.15, t1=56.9, a=(0.5, 0.35, 1.3), b=(0.5, 0.3, 1.45)),
    dict(k="pan", t0=56.9, t1=81.7, keys=[
        (56.9, 0, 1.15), (71.2, 0, 1.26),
        (71.6, 1, 1.15), (77.0, 1, 1.26),
        (77.4, 2, 1.15), (81.7, 2, 1.26),
    ]),
    # Tobias: "I didn't touch the bell"; Agnes jingles her key ring
    dict(k="art", img="talk", t0=81.7, t1=91.5, a=(0.45, 0.5, 1.1), b=(0.6, 0.45, 1.25)),
    dict(k="ask", t0=91.5, t1=106.5),
    dict(k="soltitle", t0=106.5, t1=108.6),
    dict(k="art", img="board", t0=108.6, t1=134.9, a=(0.5, 0.5, 1.0), b=(0.55, 0.5, 1.1)),
    dict(k="art", img="confess", t0=134.9, t1=159.4, a=(0.45, 0.5, 1.05), b=(0.5, 0.42, 1.2)),
    dict(k="end", t0=159.4, t1=None),
]
SHORTS = dict(tag="", p1_end=97.0, recap=(91.5, 96.7), card_t=96.5,
              suspects="Loveday, Mr Fenwick, or Tobias?")

def _pop(part, t, fade=0.3, s0=1.25, until=None):
    return dict(kind="sprite", part=part, show=(t, until), fade=fade, keys=[(t, dict(s=s0)), (t + 0.25, dict(s=1.0))], pivot="centre")

_SUS = ["s0", "s1", "s2"]
ANIM = {
    "hook": dict(art="hook", layers=[]),
    "cast": dict(art="cast", layers=[dict(kind="sprite", part=p, idle=True, blink=True) for p in _SUS]),
    "door": dict(art="door", layers=[
        dict(kind="sprite", part="bell", show=(None, 54.4), fade=0.5, wobble=dict(amp=2.0, period=3.0), pivot="top"),
        _pop("race", 9.2, until=22.3), _pop("tiptoe", 20.4, until=22.3), _pop("empty", 54.5),
    ]),
    "lb": dict(art="lb", layers=[dict(kind="sprite", part="tobias", idle=True, blink=True, show=(24.2, None), fade=0.4), _pop("tall", 28.0)]),
    "porch": dict(art="porch", layers=[
        _pop("lock", 34.7), dict(kind="sprite", part="agnes", idle=True, blink=True, show=(36.8, None), fade=0.4), _pop("keys", 38.9),
        _pop("peek", 44.5), _pop("stool", 49.5),
    ]),
    "lineup": dict(art="lineup", layers=[
        *[dict(kind="sprite", part=p, idle=True, blink=True, nods=[t]) for p, t in zip(_SUS, (61.7, 71.5, 77.3))],
        _pop("h0", 63.4), _pop("q0", 65.9), _pop("h1", 72.0), _pop("q1", 75.9), _pop("h2", 77.6), _pop("q2", 80.2),
    ]),
    "talk": dict(art="talk", layers=[
        dict(kind="sprite", part="tobias", idle=True, blink=True, talk=dict(seg=10, quotes=True)),
        dict(kind="sprite", part="agnes", idle=True, blink=True),
        dict(kind="sprite", part="jingle", show=(87.3, None), fade=0.2, wobble=dict(amp=8.0, period=0.4), pivot="top"),
    ]),
    "board": dict(art="board", layers=[_pop("hook", 112.0), _pop("b0", 121.0), _pop("b1", 121.6), _pop("b2", 117.3),
                                       _pop("ladder", 126.3), _pop("stool", 129.8), _pop("only", 131.5)]),
    "confess": dict(art="confess", layers=[
        dict(kind="sprite", part="tobias", idle=True, blink=True, swaps=[(0.0, "sheepish", 0.01)]),
        _pop("crack", 137.3, until=150.0),
        dict(kind="sprite", part="bell", show=(150.4, None), fade=0.5, wobble=dict(amp=4.0, period=0.8), pivot="top"),
        _pop("ring", 153.2), _pop("clap", 156.2),
    ]),
}
