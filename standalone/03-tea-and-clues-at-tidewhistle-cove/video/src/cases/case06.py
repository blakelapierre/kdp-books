"""Case 6, The Closed Post Office: colour-detailed art with SIMPLE ANIMATIONS (anim.py).
Times are ORIGINAL narration times (timing-case-06.json). render.py adds the hook shift and the countdown splice.
Art: art_case06.py -> work/art-06/. Part sprites use part_open (no frame2) to avoid rotating-border artifacts.
Mid-screen question bar is enabled via SHOW_QBAR (render.py)."""
NUM, NAME = 6, "The Closed Post Office"
STYLE = "color-detailed"
SLUG = "standalone-03-tidewhistle-case-06-the-closed-post-office"
AUDIO = "standalone-03-tidewhistle-08-case-06-the-closed-post-office.mp3"
TIMING = "timing-case-06.json"; CLUES = "clues/case-06.json"; ART = "work/art-06"; HOOK_WAV = "work/hook-06.wav"
QUESTION = "How does Agnes know that Mr Garland is not telling the truth?"
HOOK_LINES = ["Who took the", "puffin blanket?"]; HOOK_EMOJI = "\U0001F54A"   # dove (closest bird); puffin-ish
HOOK_SAY = "A knitted puffin blanket has vanished on a Sunday morning, and only one story cannot be true. Can you spot why?"
HOOK_FOCUS = ((0.5, 0.42, 1.15), (0.52, 0.48, 1.45))   # push into CLOSED plaque
LINEUP_PANELS = 3
SHOW_QBAR = True          # persistent mid-screen question bar (Blake 2026-10-06)
TRIM = 0.45
CUT, EXTRA = 116.4, 7.0   # after "...the solution follows." (~116.25); "The Solution." ~121.05
NARR_END = 116.25
AUDIO_END = 173.39
NO_CAP = {0, 1, 11, 14}   # titles, question card, "The Solution."
SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=5.0),
    dict(k="art", img="sunday", t0=5.0, t1=19.8, a=(0.55, 0.5, 1.08), b=(0.7, 0.48, 1.32)),  # push toward closed PO
    dict(k="art", img="porch", t0=19.8, t1=39.5, a=(0.5, 0.48, 1.1), b=(0.48, 0.52, 1.28)),
    dict(k="art", img="empty", t0=39.5, t1=42.5, a=(0.5, 0.5, 1.12), b=(0.5, 0.52, 1.3)),
    dict(k="art", img="street", t0=42.5, t1=61.2, a=(0.45, 0.5, 1.08), b=(0.55, 0.48, 1.25)),
    dict(k="art", img="garland", t0=61.2, t1=86.5, a=(0.48, 0.5, 1.1), b=(0.42, 0.52, 1.3)),
    dict(k="art", img="looking", t0=86.5, t1=103.3, a=(0.55, 0.5, 1.1), b=(0.65, 0.48, 1.35)),  # PO at end of street
    dict(k="ask", t0=103.3, t1=121.0),
    dict(k="soltitle", t0=121.0, t1=123.0),
    dict(k="pan", t0=123.0, t1=152.0, keys=[
        (123.0, 0, 1.14), (138.5, 0, 1.24),   # Garland
        (139.2, 1, 1.14), (145.5, 1, 1.22),   # Tamsin / church
        (146.2, 2, 1.14), (152.0, 2, 1.22),   # Jago / bakery
    ]),
    dict(k="art", img="returned", t0=152.0, t1=173.3, a=(0.48, 0.5, 1.1), b=(0.52, 0.48, 1.28)),
    dict(k="end", t0=173.3, t1=None),
]
# Shorts: Part 1 ends after "Think about it."; Part 2 opens with question recap for feed discovery.
SHORTS = dict(tag="", p1_end=110.5, recap=(103.4, 110.5), card_t=110.0,
              suspects="Mr Garland, Tamsin, or Jago?")

def _gull(area=(18, 220, 494, 360), n=2, seed=3):
    return [dict(kind="fly", part="gull", area=area, n=n, speed=(12, 22), flap=2.2, size=(0.5, 0.85), seed=seed)]

def _cloud(*names, dx=16, period=50):
    return [dict(kind="sprite", part=n, keys=[(0.0, dict(dx=0)), (period, dict(dx=dx * (1 if i % 2 == 0 else -0.7)))])
            for i, n in enumerate(names)]

def _leaves(n=6, seed=7):
    return [dict(kind="glint", part="leaf", area=(20, 40, 490, 160), n=n, life=3.2, drift=8.0, alpha=0.75, seed=seed)]

ANIM = {
    "hook": dict(art="hook", layers=[
        dict(kind="sprite", part="blanket", idle=False,
             keys=[(0.0, dict(a=1.0, dy=0)), (6.0, dict(a=1.0, dy=4))]),
        *_gull(seed=1),
    ]),
    "cast": dict(art="cast", layers=[
        dict(kind="sprite", part="garland", idle=True, blink=True),
        dict(kind="sprite", part="tamsin", idle=True, blink=True),
        dict(kind="sprite", part="jago", idle=True, blink=True),
    ]),
    "sunday": dict(art="sunday", layers=[
        *_cloud("cloud1", "cloud2"),
        *_gull(seed=5), *_leaves(5, seed=6),
    ]),
    "porch": dict(art="porch", layers=[
        dict(kind="sprite", part="parcel"),
        dict(kind="sprite", part="wenna", idle=True, blink=True, show=(20.0, 36.0), fade=0.4),
        *_gull(seed=9),
    ]),
    "empty": dict(art="empty", layers=[*_gull(seed=11), *_leaves(4, seed=12)]),
    "street": dict(art="street", layers=[
        dict(kind="sprite", part="agnes", idle=True, blink=True),
        dict(kind="sprite", part="wenna", idle=True, blink=True),
        dict(kind="sprite", part="tamsin", idle=True, blink=True, talk=dict(seg=5, quotes=False),
             walk=dict(t0=44.0, t1=47.5, dx=-40, steps=3, bob=1.4), show=(43.0, None), fade=0.4),
        dict(kind="sprite", part="jago", idle=True, blink=True,
             walk=dict(t0=48.0, t1=51.5, dx=-50, steps=3, bob=1.4), show=(47.5, None), fade=0.4),
        *_cloud("cloud1", dx=12, period=45),
        *_gull(seed=15),
    ]),
    "garland": dict(art="garland", layers=[
        dict(kind="sprite", part="garland", idle=True, blink=True, talk=dict(seg=8, quotes=True),
             walk=dict(t0=61.5, t1=65.0, dx=-50, steps=4, bob=1.5), show=(61.3, None), fade=0.4),
        dict(kind="sprite", part="agnes", idle=True, blink=True, nods=[87.0, 92.0]),
        dict(kind="sprite", part="wenna", idle=True, blink=True, show=(71.5, 76.0), fade=0.3),
        *_gull(seed=19),
    ]),
    "looking": dict(art="looking", layers=[
        dict(kind="sprite", part="agnes", idle=True, blink=True, nods=[98.5, 100.5]),
        *_cloud("cloud1", dx=10, period=40),
        *_gull(seed=23),
    ]),
    "lineup": dict(art="lineup", layers=[
        dict(kind="sprite", part="garland", idle=True, blink=True),
        dict(kind="sprite", part="tamsin", idle=True, blink=True),
        dict(kind="sprite", part="jago", idle=True, blink=True),
        *_gull(area=(18, 220, 3 * 512 - 18, 360), n=3, seed=27),
    ]),
    "returned": dict(art="returned", layers=[
        dict(kind="sprite", part="garland", idle=True, blink=True,
             # no "base" art variant — start on sheepish (see art_case06 returned parts)
             swaps=[(0.0, "sheepish", 0.01), (165.0, "smile", 0.5)]),
        dict(kind="sprite", part="wenna", idle=True, blink=True, show=(160.0, None), fade=0.5),
        dict(kind="sprite", part="parcel", show=(162.0, None), fade=0.4),
        *_gull(seed=31),
    ]),
}
