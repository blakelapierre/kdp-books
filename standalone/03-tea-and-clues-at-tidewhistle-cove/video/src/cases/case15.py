"""Case 15, The Warm Bonnet: BLACK-AND-WHITE ink with the simple v1 peg-doll characters, SIMPLE ANIMATIONS (anim.py),
mid-screen question bar (Case 7+ layout), clue notebook and a "next case" end card.
Times are ORIGINAL narration times (timing-case-15.json). render.py adds the hook shift and the countdown splice.
Art: art_case15.py -> work/art-15/ (bwkit). Part sprites use part_open (no frame2).
Opening: HOOK_STYLE="wiper" (render.py): the title on a frosted windscreen that a wiper sweeps clear, borderless hero
of the street with a small car and the sleeping cat, three equal suspect cards, THE CAT KNOWS stamp.
Unlike Case 14 (keyhole) and Case 13 (red pen).
Fairness: Mr Fenwick, Kerensa and Mr Treloar share pose, size and neutral faces until the solution, and the three cars are
the same drawing; only the confession shows Mr Treloar sheepish. KEEP_ASPECT: crops match the view."""
NUM, NAME = 15, "The Warm Bonnet"
STYLE = "bw"
SLUG = "standalone-03-tidewhistle-case-15-the-warm-bonnet"
AUDIO = "standalone-03-tidewhistle-17-case-15-the-warm-bonnet.mp3"
TIMING = "timing-case-15.json"; CLUES = "clues/case-15.json"; ART = "work/art-15"; HOOK_WAV = "assets/hooks/hook-15.wav"
QUESTION = "Why does Agnes not believe Mr Treloar?"
HOOK_LINES = ["Which car", "moved?"]; HOOK_EMOJI = "\U0001F408"   # cat (greyed in B&W)
HOOK_SAY = ("A silver trophy vanishes at dawn, and a small blue car speeds away. Three blue cars, three owners, and one "
            "sleepy ginger cat. Can you spot the fib?")
HOOK_STYLE = "wiper"
HOOK_STAMP = "THE CAT KNOWS"
HOOK_LABEL = "3 blue cars \u00b7 1 trophy \u00b7 1 cat"
HOOK_FOCUS = ((0.5, 0.55, 1.0), (0.68, 0.7, 1.35))
LINEUP_PANELS = 3
SHOW_QBAR = True
KEEP_ASPECT = True
NEXT_CARD = True
TRIM = 0.45
CUT, EXTRA = 113.7, 7.0          # after "...the solution follows." (ends ~113.49); "The Solution." ~117.99
NARR_END = 113.49
AUDIO_END = 175.7                # last word ends ~175.06; MP3 is ~177.9 s
NO_CAP = {0, 1, 11, 14}          # titles, question card, "The Solution."

SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=5.1),
    # Biscuit, the Kettle and Gull's ginger cat; warm bonnets
    dict(k="art", img="biscuit", t0=5.1, t1=25.6, a=(0.5, 0.55, 1.0), b=(0.68, 0.7, 1.4)),
    # a chilly grey morning, sharp wind off the sea
    dict(k="art", img="chilly", t0=25.6, t1=31.2, a=(0.5, 0.5, 1.0), b=(0.5, 0.45, 1.12)),
    # Polwhele sailing club at seven: the trophy goes
    dict(k="art", img="club", t0=31.2, t1=43.6, a=(0.45, 0.55, 1.0), b=(0.5, 0.5, 1.25)),
    # a small blue car heads for Tidewhistle Cove at 7:15
    dict(k="art", img="road", t0=43.6, t1=51.6, a=(0.45, 0.6, 1.1), b=(0.6, 0.6, 1.1)),
    dict(k="pan", t0=51.6, t1=72.8, keys=[
        (51.6, 0, 1.15), (61.9, 0, 1.26),
        (62.3, 1, 1.15), (70.2, 1, 1.26),
        (70.6, 2, 1.15), (72.8, 2, 1.26),
    ]),
    # Agnes fetches the milk and finds the third car, Biscuit asleep on its bonnet
    dict(k="art", img="tstreet", t0=72.8, t1=84.2, a=(0.45, 0.6, 1.05), b=(0.68, 0.62, 1.3)),
    # Mr Treloar at the door in his dressing gown
    dict(k="art", img="door", t0=84.2, t1=96.4, a=(0.42, 0.58, 1.1), b=(0.4, 0.55, 1.2)),
    # Agnes rests her hand on the bonnet: warm
    dict(k="art", img="touch", t0=96.4, t1=101.5, a=(0.6, 0.6, 1.1), b=(0.72, 0.6, 1.35)),
    dict(k="ask", t0=101.5, t1=117.8),
    dict(k="soltitle", t0=117.8, t1=120.0),
    dict(k="art", img="board", t0=120.0, t1=158.6, a=(0.5, 0.5, 1.0), b=(0.6, 0.5, 1.15)),
    dict(k="art", img="confess", t0=158.6, t1=175.5, a=(0.5, 0.55, 1.05), b=(0.6, 0.55, 1.2)),
    dict(k="end", t0=175.5, t1=None),
]
SHORTS = dict(tag="", p1_end=107.0, recap=(101.5, 106.7), card_t=106.5,
              suspects="Mr Fenwick, Kerensa, or Mr Treloar?")

def _pop(part, t, fade=0.3, s0=1.25, until=None):
    return dict(kind="sprite", part=part, show=(t, until), fade=fade, keys=[(t, dict(s=s0)), (t + 0.25, dict(s=1.0))], pivot="centre")

def _warm(t, at):
    return dict(kind="rise", part="warm", at=at, n=4, life=2.4, height=34, alpha=0.8, show=(t, None))

_SUS = ["s0", "s1", "s2"]
ANIM = {
    "hook": dict(art="hook", layers=[]),
    "cast": dict(art="cast", layers=[dict(kind="sprite", part=p, idle=True, blink=True) for p in _SUS]),
    "biscuit": dict(art="biscuit", layers=[
        dict(kind="sprite", part="car"),
        _pop("sardine", 14.2, until=17.4),
        _warm(18.4, (372, 112)),
        dict(kind="sprite", part="cat", show=(20.5, None), fade=0.4, keys=[(20.5, dict(dy=-40)), (21.3, dict(dy=0))]),
    ]),
    "chilly": dict(art="chilly", layers=[dict(kind="sprite", part="wind", show=(28.6, None), fade=0.5, keys=[(28.6, dict(dx=-30)), (31.2, dict(dx=30))]),
                                         dict(kind="fly", part="gull", area=(18, 250, 494, 370), n=2, speed=(12, 22), flap=2.2, size=(0.5, 0.85), seed=3)]),
    "club": dict(art="club", layers=[dict(kind="sprite", part="trophy", show=(None, 40.0), fade=0.5)]),
    "road": dict(art="road", layers=[dict(kind="sprite", part="car", keys=[(44.4, dict(dx=0)), (51.2, dict(dx=230))])]),
    "lineup": dict(art="lineup", layers=[
        dict(kind="sprite", part=p, idle=True, blink=True, nods=[t]) for p, t in zip(_SUS, (58.0, 64.0, 71.2))]),
    "tstreet": dict(art="tstreet", layers=[
        dict(kind="sprite", part="agnes", idle=True, blink=True, keys=[(72.8, dict(dx=-170)), (77.8, dict(dx=0))]),
        dict(kind="sprite", part="cat"),
        _pop("purr", 80.6),
    ]),
    "door": dict(art="door", layers=[
        dict(kind="sprite", part="treloar", idle=True, blink=True, talk=dict(seg=9, quotes=True)),
        dict(kind="sprite", part="agnes", idle=True, blink=True, nods=[95.4]),
    ]),
    "touch": dict(art="touch", layers=[
        dict(kind="sprite", part="hand", show=(96.6, None), fade=0.4, keys=[(96.6, dict(dx=50, dy=40)), (97.4, dict(dx=0, dy=0))]),
        _warm(99.6, (436, 132)),
    ]),
    "board": dict(art="board", layers=[_pop("cat", 131.0), _pop("driven", 143.0), _pop("x0", 150.3), _pop("x1", 155.0)]),
    "confess": dict(art="confess", layers=[
        dict(kind="sprite", part="treloar", idle=True, blink=True, swaps=[(0.0, "sheepish", 0.01)]),
        _pop("zzz", 172.6),
    ]),
}
