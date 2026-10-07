"""Case 8, The Four Bakers: colour-detailed art with SIMPLE ANIMATIONS (anim.py).
Times are ORIGINAL narration times (timing-case-08.json). render.py adds the hook shift and the countdown splice.
Art: art_case08.py -> work/art-08/. Part sprites use part_open (no frame2), so no border rotates with a sprite.
Opening: HOOK_STYLE="statements" (render.py) — chalkboard title, borderless full-bleed empty tray, 2x2 suspect grid
with "?" bubbles on "four statements" and an ONLY 1 IS TRUE stamp on "one". Deliberately unlike the case 6/7 open.
Fairness: the four suspects get identical poses, sizes, screen time and neutral faces until the solution; only the
confession scene (after the answer) shows Mr Fenwick sheepish. KEEP_ASPECT: crops match the view (no stretch)."""
NUM, NAME = 8, "The Four Bakers"
STYLE = "color-detailed"
SLUG = "standalone-03-tidewhistle-case-08-the-four-bakers"
AUDIO = "standalone-03-tidewhistle-10-case-08-the-four-bakers.mp3"
TIMING = "timing-case-08.json"; CLUES = "clues/case-08.json"; ART = "work/art-08"; HOOK_WAV = "work/hook-08.wav"
QUESTION = "Who took the cinnamon buns?"
HOOK_LINES = ["Who took the", "cinnamon buns?"]; HOOK_EMOJI = "\U0001F950"  # croissant (closest bakery emoji in Noto)
HOOK_SAY = ("Twelve cinnamon buns have vanished. Four suspects, four statements, and only one of them is true. "
            "Can you find the thief?")
HOOK_STYLE = "statements"
HOOK_STAMP = "ONLY 1 IS TRUE"
HOOK_LABEL = "4 suspects \u00b7 4 statements \u00b7 1 truth"
HOOK_FOCUS = ((0.5, 0.42, 1.0), (0.6, 0.36, 1.22))   # push into the empty tray's flour rings
LINEUP_PANELS = 4
SHOW_QBAR = True
KEEP_ASPECT = True
ACCENT = (168, 84, 40)          # cinnamon (vs case 7 garden green)
SHADE = (168, 84, 40)
TRIM = 0.45
CUT, EXTRA = 98.9, 7.0          # after "...the solution follows." (ends 98.74); "The Solution." ~103.6
NARR_END = 98.74
AUDIO_END = 169.0               # last word ends ~168.0; MP3 is 170.76 s
NO_CAP = {0, 1, 13, 16}         # titles, question card, "The Solution."

SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=4.8),
    # tray of twelve on the cooling rack by the back door (buns part visible)
    dict(k="art", img="bakery", t0=4.8, t1=16.3, a=(0.45, 0.5, 1.0), b=(0.66, 0.42, 1.3)),
    # Jago serving at the front
    dict(k="art", img="front", t0=16.3, t1=19.6, a=(0.5, 0.5, 1.02), b=(0.46, 0.48, 1.16)),
    # back at the rack: the tray is gone ("disappeared" ~20.1)
    dict(k="art", img="bakery", t0=19.6, t1=21.7, a=(0.68, 0.4, 1.35), b=(0.7, 0.38, 1.5)),
    # the back lane: four people pass, one by one as they are named (same size, same timing gap)
    dict(k="art", img="lane", t0=21.7, t1=30.5, a=(0.55, 0.52, 1.0), b=(0.6, 0.5, 1.06)),
    # Jago marches all four into the Kettle and Gull; Agnes
    dict(k="art", img="tearoom", t0=30.5, t1=38.8, a=(0.5, 0.5, 1.0), b=(0.52, 0.5, 1.08)),
    # four statements: identical tea-room panels, equal holds
    dict(k="pan", t0=38.8, t1=53.9, keys=[
        (38.8, 0, 1.25), (43.9, 0, 1.31),   # Pip
        (44.7, 1, 1.25), (47.5, 1, 1.31),   # Demelza
        (48.1, 2, 1.25), (50.6, 2, 1.31),   # Mr Fenwick
        (51.2, 3, 1.25), (53.9, 3, 1.31),   # Kerensa
    ]),
    # Jago, still cross: "just one of them is telling the truth"
    dict(k="art", img="tearoom", t0=53.9, t1=65.5, a=(0.3, 0.5, 1.25), b=(0.28, 0.48, 1.4)),
    # Agnes raises an eyebrow
    dict(k="art", img="agnes", t0=65.5, t1=71.6, a=(0.36, 0.5, 1.25), b=(0.3, 0.46, 1.5)),
    # chalk board recap of the four statements
    dict(k="art", img="board", t0=71.6, t1=87.6, a=(0.5, 0.5, 1.0), b=(0.5, 0.5, 1.05)),
    dict(k="ask", t0=87.6, t1=103.3),
    dict(k="soltitle", t0=103.3, t1=105.3),
    # solution on the same board: circle, underline pair, crosses, tick
    dict(k="art", img="board", t0=105.3, t1=124.4, a=(0.5, 0.5, 1.0), b=(0.52, 0.52, 1.1)),
    dict(k="art", img="board", t0=124.4, t1=135.0, a=(0.46, 0.48, 1.08), b=(0.42, 0.46, 1.16)),
    dict(k="art", img="board", t0=135.0, t1=148.6, a=(0.5, 0.52, 1.1), b=(0.5, 0.5, 1.0)),
    # confession at the back door (Fenwick sheepish only here)
    dict(k="art", img="confess", t0=148.6, t1=168.4, a=(0.45, 0.52, 1.0), b=(0.4, 0.5, 1.12)),
    dict(k="end", t0=168.4, t1=None),
]
SHORTS = dict(tag="", p1_end=93.4, recap=(88.4, 93.4), card_t=93.0,
              suspects="Pip, Demelza, Mr Fenwick, or Kerensa?")

def _gull(area=(18, 250, 494, 370), n=2, seed=3):
    return [dict(kind="fly", part="gull", area=area, n=n, speed=(12, 22), flap=2.2, size=(0.5, 0.85), seed=seed)]

def _mark(part, t, fade=0.3):
    return dict(kind="sprite", part=part, show=(t, None), fade=fade, keys=[(t, dict(s=1.25)), (t + 0.25, dict(s=1.0))], pivot="centre")

_SUS = ["pip", "demelza", "fenwick", "kerensa"]
ANIM = {
    "hook": dict(art="hook", layers=[*_gull(area=(18, 300, 494, 380), n=2, seed=1)]),
    "grid": dict(art="grid", layers=[dict(kind="sprite", part=p, idle=True, blink=True) for p in _SUS]),
    "bakery": dict(art="bakery", layers=[
        dict(kind="sprite", part="buns", show=(None, 20.0), fade=0.35),
        dict(kind="rise", part="steam", at=(385, 232), n=4, life=3.0, height=30, show=(4.8, 16.0), alpha=0.75),
        *_gull(area=(18, 310, 494, 372), seed=5),
    ]),
    "front": dict(art="front", layers=[
        dict(kind="sprite", part="jago", idle=True, blink=True),
        dict(kind="sprite", part="customer", idle=True, blink=True),
    ]),
    # named one by one; each walks in the same short way, same gap
    "lane": dict(art="lane", layers=[
        *[dict(kind="sprite", part=p, idle=True, blink=True, show=(t, None), fade=0.35,
               walk=dict(t0=t, t1=t + 0.8, dx=-18, steps=3))
          for p, t in zip(_SUS, (25.3, 26.3, 27.4, 29.0))],
        *_gull(area=(18, 310, 494, 372), seed=7),
    ]),
    "tearoom": dict(art="tearoom", layers=[
        dict(kind="sprite", part="jago", idle=True, blink=True, talk=dict(seg=10, quotes=True)),
        dict(kind="sprite", part="agnes", idle=True, blink=True, nods=[37.0]),
    ]),
    "lineup": dict(art="lineup", layers=[
        dict(kind="sprite", part=p, idle=True, blink=True, talk=dict(seg=6 + i, quotes=True)) for i, p in enumerate(_SUS)
    ]),
    "agnes": dict(art="agnes", layers=[
        dict(kind="sprite", part="agnes", idle=True, blink=True, nods=[69.5]),
        dict(kind="rise", part="steam", at=(400, 108), n=3, life=2.8, height=24, alpha=0.75),
    ]),
    "board": dict(art="board", layers=[
        _mark("circle_fen", 106.3),
        _mark("pair", 108.5, fade=0.5),
        _mark("pair_lbl", 120.5),
        _mark("x_pip", 131.7),
        _mark("x_fen", 133.9),
        _mark("x_dem", 143.1),
        _mark("tick_ker", 145.9),
    ]),
    "confess": dict(art="confess", layers=[
        dict(kind="sprite", part="fenwick", idle=True, blink=True, swaps=[(0.0, "sheepish", 0.01)]),
        dict(kind="sprite", part="jago", idle=True, blink=True),
        *_gull(area=(18, 310, 494, 372), seed=9),
    ]),
}
