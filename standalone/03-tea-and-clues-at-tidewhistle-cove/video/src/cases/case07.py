"""Case 7, The Dog That Stayed Quiet: colour-detailed art with SIMPLE ANIMATIONS (anim.py).
Times are ORIGINAL narration times (timing-case-07.json). render.py adds the hook shift and the countdown splice.
Art: art_case07.py -> work/art-07/. Part sprites use part_open (no frame2) to avoid rotating-border artifacts.
Mid-screen question bar via SHOW_QBAR. Less-templatey hook: borderless hero gnome + banner title + garden accent."""
NUM, NAME = 7, "The Dog That Stayed Quiet"
STYLE = "color-detailed"
SLUG = "standalone-03-tidewhistle-case-07-the-dog-that-stayed-quiet"
AUDIO = "standalone-03-tidewhistle-09-case-07-the-dog-that-stayed-quiet.mp3"
TIMING = "timing-case-07.json"; CLUES = "clues/case-07.json"; ART = "work/art-07"; HOOK_WAV = "work/hook-07.wav"
QUESTION = "Who took Sir Reginald the gnome?"
HOOK_LINES = ["Who took", "Sir Reginald?"]; HOOK_EMOJI = "🐕"  # dog
HOOK_SAY = "A prize garden gnome has vanished in the night, and the little dog who barks at everyone stayed perfectly quiet. Can you tell who took him?"
HOOK_FOCUS = ((0.58, 0.42, 1.05), (0.62, 0.48, 1.35))   # push into Sir Reginald's red hat
LINEUP_PANELS = 3
SHOW_QBAR = True
# Less templatey open (Blake 2026-10-06)
HOOK_BORDER = False
HOOK_TITLE_STYLE = "banner"
HOOK_TITLE_Y = 48
HOOK_ART_SIZE = (1040, 820)
HOOK_ART_Y = 260
ACCENT = (46, 110, 72)          # garden green (vs crimson / Sunday-gold)
SHADE = (46, 110, 72)
TRIM = 0.45
CUT, EXTRA = 114.0, 7.0         # after "...the solution follows." (~113.96); "The Solution." ~118.46
NARR_END = 113.96
AUDIO_END = 172.69
NO_CAP = {0, 1, 9, 12}          # titles, question card, "The Solution."
SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=5.0),
    # Sir Reginald on his pedestal (gnome part visible)
    dict(k="art", img="garden", t0=5.0, t1=20.6, a=(0.5, 0.48, 1.08), b=(0.5, 0.52, 1.28)),
    # empty pedestal after "gone"
    dict(k="art", img="garden", t0=20.6, t1=24.2, a=(0.5, 0.45, 1.2), b=(0.5, 0.5, 1.4)),
    # hedge + gate + Pickle on porch (barks at everyone)
    dict(k="art", img="porch", t0=24.2, t1=56.5, a=(0.48, 0.5, 1.1), b=(0.55, 0.48, 1.3)),
    # still night — no bark
    dict(k="art", img="night", t0=56.5, t1=73.5, a=(0.45, 0.5, 1.08), b=(0.55, 0.52, 1.28)),
    # kitchen tea
    dict(k="art", img="kitchen", t0=73.5, t1=84.0, a=(0.5, 0.5, 1.1), b=(0.48, 0.52, 1.22)),
    # three suspects on the street (Ashby / Fenwick / Pip) + Pickle thump still in kitchen audio
    dict(k="art", img="street", t0=84.0, t1=99.2, a=(0.45, 0.5, 1.08), b=(0.55, 0.48, 1.28)),
    dict(k="art", img="kitchen", t0=99.2, t1=102.5, a=(0.5, 0.48, 1.15), b=(0.5, 0.52, 1.3)),
    dict(k="ask", t0=102.5, t1=119.2),
    dict(k="soltitle", t0=119.2, t1=121.2),
    dict(k="pan", t0=121.2, t1=151.2, keys=[
        (121.2, 0, 1.14), (135.0, 0, 1.24),   # Pip
        (135.8, 1, 1.14), (143.0, 1, 1.22),   # Fenwick
        (143.8, 2, 1.14), (151.2, 2, 1.22),   # Ashby
    ]),
    dict(k="art", img="shed", t0=151.2, t1=162.0, a=(0.48, 0.5, 1.1), b=(0.55, 0.48, 1.28)),
    dict(k="art", img="returned", t0=162.0, t1=172.6, a=(0.5, 0.5, 1.1), b=(0.5, 0.48, 1.28)),
    dict(k="end", t0=172.6, t1=None),
]
SHORTS = dict(tag="", p1_end=107.9, recap=(102.9, 107.9), card_t=107.5,
              suspects="Pip, Mr Fenwick, or Mrs Ashby?")

def _gull(area=(18, 220, 494, 360), n=2, seed=3):
    return [dict(kind="fly", part="gull", area=area, n=n, speed=(12, 22), flap=2.2, size=(0.5, 0.85), seed=seed)]

def _cloud(*names, dx=16, period=50):
    return [dict(kind="sprite", part=n, keys=[(0.0, dict(dx=0)), (period, dict(dx=dx * (1 if i % 2 == 0 else -0.7)))])
            for i, n in enumerate(names)]

def _leaves(n=6, seed=7):
    return [dict(kind="glint", part="leaf", area=(20, 40, 490, 160), n=n, life=3.2, drift=8.0, alpha=0.75, seed=seed)]

ANIM = {
    "hook": dict(art="hook", layers=[
        dict(kind="sprite", part="glint", idle=False,
             keys=[(0.0, dict(a=0.7, dy=0)), (6.0, dict(a=1.0, dy=3))]),
        *_gull(seed=1), *_leaves(4, seed=2),
    ]),
    "cast": dict(art="cast", layers=[
        dict(kind="sprite", part="pip", idle=True, blink=True),
        dict(kind="sprite", part="fenwick", idle=True, blink=True),
        dict(kind="sprite", part="ashby", idle=True, blink=True),
    ]),
    "garden": dict(art="garden", layers=[
        # gnome visible for intro (5–20.6); hidden after "gone" via show=
        dict(kind="sprite", part="gnome", show=(5.0, 20.55), fade=0.35),
        *_cloud("cloud1", "cloud2"),
        *_gull(seed=5), *_leaves(5, seed=6),
    ]),
    "porch": dict(art="porch", layers=[
        dict(kind="sprite", part="pickle", idle=False),  # awake — he barks; sleep is night plate
        *_gull(seed=9), *_leaves(4, seed=10),
    ]),
    "night": dict(art="night", layers=[
        dict(kind="sprite", part="pickle"),
        dict(kind="glint", part="star", area=(40, 240, 480, 360), n=8, life=2.8, drift=2.0, alpha=0.85, seed=11),
        *_gull(area=(18, 260, 494, 360), n=1, seed=12),
    ]),
    "kitchen": dict(art="kitchen", layers=[
        dict(kind="sprite", part="agnes", idle=True, blink=True, nods=[76.0, 100.0]),
        dict(kind="sprite", part="loveday", idle=True, blink=True, talk=dict(seg=7, quotes=True)),
        dict(kind="sprite", part="pickle",
             keys=[(0.0, dict(dy=0)), (99.3, dict(dy=0)), (99.5, dict(dy=6)), (100.2, dict(dy=0)), (101.5, dict(dy=0))]),
        *_gull(seed=15),
    ]),
    "street": dict(art="street", layers=[
        dict(kind="sprite", part="ashby", idle=True, blink=True, show=(84.5, None), fade=0.35),
        dict(kind="sprite", part="fenwick", idle=True, blink=True, show=(89.0, None), fade=0.35),
        dict(kind="sprite", part="pip", idle=True, blink=True, talk=dict(seg=7, quotes=False),
             show=(93.5, None), fade=0.35),
        *_gull(seed=17), *_leaves(4, seed=18),
    ]),
    "lineup": dict(art="lineup", layers=[
        dict(kind="sprite", part="pip", idle=True, blink=True),
        dict(kind="sprite", part="fenwick", idle=True, blink=True),
        dict(kind="sprite", part="ashby", idle=True, blink=True),
        *_gull(area=(18, 220, 3 * 512 - 18, 360), n=3, seed=19),
    ]),
    "shed": dict(art="shed", layers=[
        dict(kind="sprite", part="pip", idle=True, blink=True,
             swaps=[(0.0, "sheepish", 0.01), (158.0, "smile", 0.5)]),
        dict(kind="sprite", part="gnome", show=(154.0, None), fade=0.4),
        *_gull(seed=23),
    ]),
    "returned": dict(art="returned", layers=[
        dict(kind="sprite", part="gnome"),
        dict(kind="sprite", part="loveday", idle=True, blink=True, show=(164.0, None), fade=0.4),
        dict(kind="sprite", part="pip", idle=True, blink=True, show=(166.0, None), fade=0.4),
        *_gull(seed=27), *_leaves(5, seed=28),
    ]),
}
