"""Case 17, The Talking Parrot: BLACK-AND-WHITE ink with the simple v1 peg-doll characters, SIMPLE ANIMATIONS (anim.py),
mid-screen question bar (Case 7+ layout), clue notebook and a "next case" end card.
Times are ORIGINAL narration times (timing-case-17.json). render.py adds the hook shift and the countdown splice.
Art: art_case17.py -> work/art-17/ (bwkit). Part sprites use part_open (no frame2).
Opening: HOOK_STYLE="bubble" (render.py): the title inside a big comic speech bubble that inflates with a wobble and an
echo bubble, its tail pointing down at Admiral in the borderless shop hero; three equal tag suspect cards; LISTEN CLOSELY
stamp. Unlike Case 16 (stopwatch) and Case 15 (wiper).
Fairness: Tamsin, Mr Fenwick and Mr Pascoe share pose, size and neutral faces and each gets the same key tag; Mr Pascoe's
saying is narrated for everyone before the question. Only the confession shows Mr Pascoe sheepish. KEEP_ASPECT."""
NUM, NAME = 17, "The Talking Parrot"
STYLE = "bw"
SLUG = "standalone-03-tidewhistle-case-17-the-talking-parrot"
AUDIO = "standalone-03-tidewhistle-19-case-17-the-talking-parrot.mp3"
TIMING = "timing-case-17.json"; CLUES = "clues/case-17.json"; ART = "work/art-17"; HOOK_WAV = "assets/hooks/hook-17.wav"
QUESTION = "Who took the silver thimble?"
HOOK_LINES = ["Who taught", "the parrot?"]; HOOK_EMOJI = "\U0001F99C"   # parrot (greyed in B&W)
HOOK_SAY = ("A silver thimble vanishes from a locked shop, and the only witness is a very clever parrot. Three keyholders, "
            "and one brand new phrase. Can you listen closely?")
HOOK_STYLE = "bubble"
HOOK_STAMP = "LISTEN CLOSELY"
HOOK_LABEL = "3 keyholders \u00b7 1 locked shop \u00b7 1 parrot"
HOOK_FOCUS = ((0.45, 0.4, 1.0), (0.42, 0.35, 1.3))
LINEUP_PANELS = 3
SHOW_QBAR = True
KEEP_ASPECT = True
NEXT_CARD = True
TRIM = 0.45
CUT, EXTRA = 123.8, 7.0          # after "...the solution follows." (ends ~123.62); "The Solution." ~128.12
NARR_END = 123.62
AUDIO_END = 189.0                # last word ends ~188.42
NO_CAP = {0, 1, 11, 14}          # titles, question card, "The Solution."

SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=5.1),
    # Mr Pascoe the window cleaner outside the Kettle and Gull: "Mind how you go, my lovely"
    dict(k="art", img="tea", t0=5.1, t1=36.3, a=(0.5, 0.5, 1.0), b=(0.6, 0.45, 1.3)),
    # Wenna's antique shop and Admiral's three phrases; Wenna pops out, shop locked
    dict(k="art", img="shop", t0=36.3, t1=66.1, a=(0.5, 0.5, 1.0), b=(0.52, 0.38, 1.25)),
    dict(k="pan", t0=66.1, t1=78.3, keys=[
        (66.1, 0, 1.15), (72.6, 0, 1.22),
        (73.0, 1, 1.15), (74.0, 1, 1.2),
        (74.3, 2, 1.15), (78.3, 2, 1.26),
    ]),
    # back in the shop: the thimble gone; Admiral's new phrase; Wenna in the doorway
    dict(k="art", img="shop", t0=78.3, t1=99.4, a=(0.6, 0.55, 1.15), b=(0.55, 0.4, 1.3)),
    # Agnes asks around: what each keyholder said
    dict(k="pan", t0=99.4, t1=112.75, keys=[
        (99.4, 0, 1.15), (105.0, 0, 1.22),
        (105.3, 1, 1.15), (107.8, 1, 1.22),
        (108.1, 2, 1.15), (112.75, 2, 1.26),
    ]),
    dict(k="ask", t0=112.75, t1=127.9),
    dict(k="soltitle", t0=127.9, t1=130.2),
    dict(k="art", img="board", t0=130.2, t1=166.4, a=(0.5, 0.5, 1.0), b=(0.6, 0.5, 1.12)),
    dict(k="art", img="confess", t0=166.4, t1=188.9, a=(0.5, 0.5, 1.05), b=(0.55, 0.45, 1.2)),
    dict(k="end", t0=188.9, t1=None),
]
SHORTS = dict(tag="", p1_end=118.2, recap=(112.75, 117.9), card_t=117.7,
              suspects="Tamsin, Mr Fenwick, or Mr Pascoe?")

def _pop(part, t, fade=0.3, s0=1.25, until=None):
    return dict(kind="sprite", part=part, show=(t, until), fade=fade, keys=[(t, dict(s=s0)), (t + 0.25, dict(s=1.0))], pivot="centre")

_BOB = [(84.2 + i * 0.35, dict(dy=(6 if i % 2 else 0))) for i in range(34)]
_SUS = ["s0", "s1", "s2"]
ANIM = {
    "hook": dict(art="hook", layers=[]),
    "cast": dict(art="cast", layers=[dict(kind="sprite", part=p, idle=True, blink=True) for p in _SUS]),
    "tea": dict(art="tea", layers=[
        dict(kind="sprite", part="pascoe", idle=True, blink=True, talk=dict(seg=3, quotes=True), nods=[24.9]),
        dict(kind="sprite", part="agnes", idle=True, blink=True),
        _pop("say", 22.4, until=27.4), _pop("tease", 27.6),
    ]),
    "shop": dict(art="shop", layers=[
        dict(kind="sprite", part="thimble", show=(None, 80.6), fade=0.4),
        _pop("gone", 80.7),
        dict(kind="sprite", part="wenna", idle=True, blink=True, show=(None, 61.2), fade=0.5),
        dict(kind="sprite", part="wenna", idle=True, blink=True, show=(95.9, None), fade=0.4, seed=1),
        dict(kind="sprite", part="admiral", idle=True, talk=[(53.2, 58.5), (88.6, 95.2)], keys=_BOB),
        _pop("p0", 53.3, until=61.4), _pop("p1", 54.4, until=61.4), _pop("p2", 57.4, until=61.4),
        _pop("lock", 61.5, until=79.0),
        _pop("mind", 89.4),
    ]),
    "lineup": dict(art="lineup", layers=[
        *[dict(kind="sprite", part=p, idle=True, blink=True, nods=[t]) for p, t in zip(_SUS, (71.4, 73.0, 73.9))],
        _pop("k0", 66.8), _pop("k1", 66.8), _pop("k2", 66.8),
        _pop("a0", 103.0), _pop("a1", 106.6), _pop("a2", 108.3),
    ]),
    "board": dict(art="board", layers=[_pop("new", 144.4), _pop("ring", 149.4), _pop("who", 155.4), _pop("key", 162.0)]),
    "confess": dict(art="confess", layers=[
        dict(kind="sprite", part="pascoe", idle=True, blink=True, swaps=[(0.0, "sheepish", 0.01)]),
        dict(kind="sprite", part="wenna", idle=True, blink=True, nods=[178.8]),
        dict(kind="sprite", part="admiral", idle=True, talk=[(184.3, 186.2)]),
        _pop("thimble", 178.1), _pop("price", 181.9), _pop("mind", 184.4),
    ]),
}
