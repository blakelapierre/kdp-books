"""Case 21, The Spanish Coin: BLACK-AND-WHITE ink with the simple v1 peg-doll characters, SIMPLE ANIMATIONS (anim.py),
mid-screen question bar (Case 7+ layout), clue notebook and a "next case" end card.
Times are ORIGINAL narration times (timing-case-21.json). render.py adds the hook shift and the countdown splice.
Art: art_case21.py -> work/art-21/ (bwkit). Part sprites use part_open (no frame2).
Opening: HOOK_STYLE="coinflip" (render.py): a big silver coin spins (edge-on squash) beside the title and lands crown up,
borderless ice-cream-van hero, three equal suspect cards, FOLLOW THE MONEY stamp.
Unlike Case 20 (scent) and Case 19 (ruler).
Fairness: Demelza, Pip and Mr Nankervis share pose, size and neutral faces and each gets the same "how they paid" tag when
narrated. Only the confession shows Mr Nankervis sheepish. KEEP_ASPECT."""
NUM, NAME = 21, "The Spanish Coin"
STYLE = "bw"
SLUG = "standalone-03-tidewhistle-case-21-the-spanish-coin"
AUDIO = "standalone-03-tidewhistle-23-case-21-the-spanish-coin.mp3"
TIMING = "timing-case-21.json"; CLUES = "clues/case-21.json"; ART = "work/art-21"; HOOK_WAV = "assets/hooks/hook-21.wav"
QUESTION = "Who took the Spanish coins?"
HOOK_LINES = ["Who spent", "the treasure?"]; HOOK_EMOJI = "\U0001FA99"   # coin (greyed in B&W)
HOOK_SAY = ("Six old Spanish coins vanish from the museum, and one turns up in an ice cream van's till. Three customers, three "
            "ways to pay. Can you follow the money?")
HOOK_STYLE = "coinflip"
HOOK_STAMP = "FOLLOW THE MONEY"
HOOK_LABEL = "3 customers \u00b7 1 till \u00b7 1 Spanish coin"
HOOK_FOCUS = ((0.55, 0.55, 1.0), (0.6, 0.5, 1.3))
LINEUP_PANELS = 3
SHOW_QBAR = True
KEEP_ASPECT = True
NEXT_CARD = True
TRIM = 0.45
CUT, EXTRA = 115.9, 7.0          # after "...the solution follows." (ends ~115.7); "The Solution." ~120.2
NARR_END = 115.7
AUDIO_END = 185.9                # last word ends ~185.38
NO_CAP = {0, 1, 11, 14}          # titles, question card, "The Solution."

SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=5.15),
    # the museum's glass case of beach coins; the silver Spanish coins with a crown; the velvet bag taken
    dict(k="art", img="museum", t0=5.15, t1=27.45, a=(0.5, 0.5, 1.0), b=(0.55, 0.42, 1.3)),
    # Jenna's ice cream van at ten: till emptied every night, a sealed float of new coins every morning
    dict(k="art", img="van", t0=27.45, t1=46.75, a=(0.45, 0.5, 1.0), b=(0.72, 0.55, 1.25)),
    # eleven o'clock: Jenna at the Kettle and Gull with a Spanish coin on her palm
    dict(k="art", img="tea", t0=46.75, t1=72.95, a=(0.5, 0.5, 1.0), b=(0.45, 0.45, 1.2)),
    dict(k="pan", t0=72.95, t1=95.4, keys=[
        (72.95, 0, 1.15), (78.4, 0, 1.26),
        (78.8, 1, 1.15), (86.3, 1, 1.26),
        (86.7, 2, 1.15), (95.4, 2, 1.28),
    ]),
    # "And you put his coins straight into the till?" "Straight in. Without looking."
    dict(k="art", img="tea", t0=95.4, t1=104.8, a=(0.45, 0.5, 1.05), b=(0.42, 0.45, 1.15)),
    dict(k="ask", t0=104.8, t1=120.0),
    dict(k="soltitle", t0=120.0, t1=122.3),
    dict(k="art", img="board", t0=122.3, t1=161.7, a=(0.5, 0.5, 1.0), b=(0.55, 0.5, 1.1)),
    dict(k="art", img="confess", t0=161.7, t1=185.8, a=(0.45, 0.5, 1.05), b=(0.55, 0.45, 1.2)),
    dict(k="end", t0=185.8, t1=None),
]
SHORTS = dict(tag="", p1_end=110.3, recap=(104.8, 110.0), card_t=109.8,
              suspects="Demelza, Pip, or Mr Nankervis?")

def _pop(part, t, fade=0.3, s0=1.25, until=None):
    return dict(kind="sprite", part=part, show=(t, until), fade=fade, keys=[(t, dict(s=s0)), (t + 0.25, dict(s=1.0))], pivot="centre")

_SUS = ["s0", "s1", "s2"]
ANIM = {
    "hook": dict(art="hook", layers=[]),
    "cast": dict(art="cast", layers=[dict(kind="sprite", part=p, idle=True, blink=True) for p in _SUS]),
    "museum": dict(art="museum", layers=[
        dict(kind="sprite", part="bag", show=(None, 24.9), fade=0.4), _pop("gone", 25.0), _pop("zoom", 17.9, until=23.0)]),
    "van": dict(art="van", layers=[
        dict(kind="sprite", part="jenna", idle=True, blink=True, show=(29.0, None), fade=0.4), _pop("clock", 32.4),
        _pop("till", 35.9), _pop("float", 42.1),
        dict(kind="fly", part="gull", area=(18, 250, 494, 370), n=2, speed=(12, 22), flap=2.2, size=(0.5, 0.85), seed=4)]),
    "tea": dict(art="tea", layers=[
        dict(kind="sprite", part="jenna", idle=True, blink=True, talk=[(56.2, 66.8), (99.5, 103.0)], walk=dict(t0=47.0, t1=49.5, dx=-120, steps=4, bob=1.6)),
        dict(kind="sprite", part="agnes", idle=True, blink=True, talk=[(95.4, 98.0)]),
        _pop("coin", 51.4, until=72.9), _pop("mist", 62.9), _pop("cup", 68.7),
    ]),
    "lineup": dict(art="lineup", layers=[
        *[dict(kind="sprite", part=p, idle=True, blink=True, nods=[t]) for p, t in zip(_SUS, (73.6, 79.0, 86.8))],
        _pop("p0", 77.0), _pop("p1", 82.9), _pop("p2", 92.6),
    ]),
    "board": dict(art="board", layers=[_pop("open", 128.4), _pop("r0", 139.9), _pop("r1", 144.5), _pop("r2", 151.8), _pop("ring", 156.4)]),
    "confess": dict(art="confess", layers=[
        dict(kind="sprite", part="nank", idle=True, blink=True, swaps=[(0.0, "sheepish", 0.01)]),
        _pop("pocket", 166.0), _pop("card", 181.0),
    ]),
}
