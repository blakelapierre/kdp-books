"""Case 9, The Sunset over the Sea: colour-detailed art with SIMPLE ANIMATIONS (anim.py).
Times are ORIGINAL narration times (timing-case-09.json). render.py adds the hook shift and the countdown splice.
Art: art_case09.py -> work/art-09/. Part sprites use part_open (no frame2), so no border rotates with a sprite.
Opening: HOOK_STYLE="compass" (render.py) — compass-rose title ring, borderless empty-easel hero, three equal
suspect cards, spinning compass landing EAST, ONE STORY FAILS stamp. Deliberately unlike cases 6/7/8
(closed-door / gnome banner / cinnamon-statements).
Fairness: Tamsin, Hedley and Ashdown get identical poses, sizes and neutral faces until the solution; only the
confession shows Mr Ashdown sheepish. KEEP_ASPECT: crops match the view (no stretch)."""
NUM, NAME = 9, "The Sunset over the Sea"
STYLE = "color-detailed"
SLUG = "standalone-03-tidewhistle-case-09-the-sunset-over-the-sea"
AUDIO = "standalone-03-tidewhistle-11-case-09-the-sunset-over-the-sea.mp3"
TIMING = "timing-case-09.json"; CLUES = "clues/case-09.json"; ART = "work/art-09"; HOOK_WAV = "assets/hooks/hook-09.wav"
QUESTION = "What is wrong with Mr Ashdown's story?"
HOOK_LINES = ["What's wrong", "with his story?"]; HOOK_EMOJI = "\U0001F305"  # sunrise over water
HOOK_SAY = ("A watercolour vanished from an easel on the sea front. Three people were nearby — "
            "and one story does not fit. Can you spot the lie?")
HOOK_STYLE = "compass"
HOOK_STAMP = "ONE STORY FAILS"
HOOK_LABEL = "3 people \u00b7 1 painting \u00b7 1 wrong story"
HOOK_FOCUS = ((0.62, 0.42, 1.05), (0.68, 0.48, 1.28))   # push into the empty easel
LINEUP_PANELS = 3
SHOW_QBAR = True
KEEP_ASPECT = True
ACCENT = (196, 84, 64)          # sunset coral (vs case 7 green / case 8 cinnamon)
SHADE = (196, 84, 64)
TRIM = 0.45
CUT, EXTRA = 110.3, 7.0         # after "...the solution follows." (~110.20); "The Solution." ~114.7
NARR_END = 110.20
AUDIO_END = 169.90               # last word ends ~169.73; MP3 is ~172.4 s
NO_CAP = {0, 1, 10, 13}         # titles, question card, "The Solution."

SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=5.0),
    # Agnes opens shutters: sun climbs out of the sea (cove faces east)
    dict(k="art", img="kettle", t0=5.0, t1=22.6, a=(0.55, 0.5, 1.05), b=(0.72, 0.55, 1.3)),
    # Demelza's stall + painting on the easel
    dict(k="art", img="stall", t0=22.6, t1=36.0, a=(0.5, 0.48, 1.05), b=(0.62, 0.45, 1.22)),
    # painting gone
    dict(k="art", img="stall", t0=36.0, t1=40.5, a=(0.66, 0.42, 1.3), b=(0.7, 0.4, 1.45)),
    # three people near the sea front
    dict(k="art", img="stall", t0=40.5, t1=47.5, a=(0.45, 0.5, 1.05), b=(0.5, 0.5, 1.1)),
    # equal lineup: Tamsin / Hedley / Ashdown
    dict(k="pan", t0=47.5, t1=72.5, keys=[
        (47.5, 0, 1.2), (54.5, 0, 1.28),   # Tamsin
        (55.5, 1, 1.2), (64.0, 1, 1.28),   # Hedley
        (65.0, 2, 1.2), (72.5, 2, 1.28),   # Ashdown
    ]),
    # Ashdown's clifftop story (neutral)
    dict(k="art", img="ashdown", t0=72.5, t1=91.5, a=(0.42, 0.5, 1.15), b=(0.38, 0.48, 1.32)),
    # Agnes remembering the morning sunrise
    dict(k="art", img="agnes", t0=91.5, t1=98.5, a=(0.36, 0.5, 1.2), b=(0.3, 0.48, 1.4)),
    dict(k="ask", t0=98.5, t1=114.5),
    dict(k="soltitle", t0=114.5, t1=116.8),
    # map board: cove faces east
    dict(k="art", img="board", t0=116.8, t1=139.5, a=(0.5, 0.5, 1.0), b=(0.52, 0.52, 1.08)),
    # Tamsin + Hedley alibis hold
    dict(k="art", img="board", t0=139.5, t1=149.2, a=(0.5, 0.48, 1.05), b=(0.5, 0.5, 1.0)),
    # confession
    dict(k="art", img="confess", t0=149.2, t1=169.7, a=(0.45, 0.5, 1.05), b=(0.4, 0.48, 1.15)),
    dict(k="end", t0=169.7, t1=None),
]
SHORTS = dict(tag="", p1_end=104.5, recap=(99.5, 104.5), card_t=104.1,
              suspects="Tamsin, Hedley, or Mr Ashdown?")

def _gull(area=(18, 250, 494, 370), n=2, seed=3):
    return [dict(kind="fly", part="gull", area=area, n=n, speed=(12, 22), flap=2.2, size=(0.5, 0.85), seed=seed)]

def _mark(part, t, fade=0.3):
    return dict(kind="sprite", part=part, show=(t, None), fade=fade, keys=[(t, dict(s=1.25)), (t + 0.25, dict(s=1.0))], pivot="centre")

_SUS = ["tamsin", "hedley", "ashdown"]
ANIM = {
    "hook": dict(art="hook", layers=[*_gull(area=(18, 300, 494, 380), n=2, seed=1)]),
    "cast": dict(art="cast", layers=[dict(kind="sprite", part=p, idle=True, blink=True) for p in _SUS]),
    "kettle": dict(art="kettle", layers=[
        dict(kind="sprite", part="agnes", idle=True, blink=True, nods=[12.0, 18.0]),
        dict(kind="rise", part="steam", at=(200, 100), n=3, life=2.8, height=24, alpha=0.75),
        *_gull(seed=5),
    ]),
    "stall": dict(art="stall", layers=[
        dict(kind="sprite", part="painting", show=(None, 39.2), fade=0.35),
        dict(kind="sprite", part="demelza", idle=True, blink=True, show=(23.5, 36.0), fade=0.3),
        *_gull(area=(18, 310, 494, 372), seed=7),
    ]),
    "bookshop": dict(art="bookshop", layers=[
        dict(kind="sprite", part="tamsin", idle=True, blink=True, talk=dict(seg=5, quotes=False)),
    ]),
    "inn": dict(art="inn", layers=[
        dict(kind="sprite", part="hedley", idle=True, blink=True, talk=dict(seg=6, quotes=False)),
    ]),
    "lineup": dict(art="lineup", layers=[
        dict(kind="sprite", part=p, idle=True, blink=True) for p in _SUS
    ]),
    "ashdown": dict(art="ashdown", layers=[
        dict(kind="sprite", part="ashdown", idle=True, blink=True, talk=dict(seg=8, quotes=True)),
        dict(kind="sprite", part="agnes", idle=True, blink=True),
    ]),
    "agnes": dict(art="agnes", layers=[
        dict(kind="sprite", part="agnes", idle=True, blink=True, nods=[94.5]),
        dict(kind="rise", part="steam", at=(400, 108), n=3, life=2.8, height=24, alpha=0.75),
    ]),
    "board": dict(art="board", layers=[
        _mark("east", 121.0),
        _mark("x_sunset", 131.5, fade=0.45),
        _mark("tick_ash", 136.5),
    ]),
    "confess": dict(art="confess", layers=[
        dict(kind="sprite", part="ashdown", idle=True, blink=True, swaps=[(0.0, "sheepish", 0.01)]),
        dict(kind="sprite", part="demelza", idle=True, blink=True),
    ]),
}
