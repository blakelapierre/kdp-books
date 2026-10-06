"""Case 5, The Marrow Mix-up: colour-detailed art with SIMPLE ANIMATIONS (anim.py).
Times are ORIGINAL narration times (timing-case-05.json). render.py adds the hook shift and the countdown splice.
Art: art_case05.py -> work/art-05/. Part sprites use part_open (no frame2) to avoid Case 4 rotating-border artifacts."""
NUM, NAME = 5, "The Marrow Mix-up"
STYLE = "color-detailed"
SLUG = "standalone-03-tidewhistle-case-05-the-marrow-mix-up"
AUDIO = "standalone-03-tidewhistle-07-case-05-the-marrow-mix-up.mp3"
TIMING = "timing-case-05.json"; CLUES = "clues/case-05.json"; ART = "work/art-05"; HOOK_WAV = "work/hook-05.wav"
QUESTION = "Who took the prize marrow?"
HOOK_LINES = ["Who took the", "prize marrow?"]; HOOK_EMOJI = "\U0001F955"   # carrot (closest veggie); marrow-ish
HOOK_SAY = "A prize marrow has vanished from Hedley's shed, and only one person is lying. Can you spot who?"
HOOK_FOCUS = ((0.45, 0.48, 1.2), (0.48, 0.52, 1.55))
LINEUP_PANELS = 4
TRIM = 0.45
CUT, EXTRA = 110.5, 7.0          # after "...the solution follows." (~109.97); "The Solution." ~114.41
NARR_END = 109.97
AUDIO_END = 185.59
NO_CAP = {0, 1, 13, 16}          # titles, question card, "The Solution."
SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=4.8),
    dict(k="art", img="shed", t0=4.8, t1=20.5, a=(0.5, 0.48, 1.08), b=(0.48, 0.52, 1.28)),
    dict(k="art", img="empty", t0=20.5, t1=24.5, a=(0.5, 0.5, 1.1), b=(0.5, 0.52, 1.3)),
    dict(k="art", img="allotments", t0=24.5, t1=44.5, a=(0.55, 0.5, 1.08), b=(0.6, 0.48, 1.25)),
    dict(k="art", img="bench", t0=44.5, t1=61.0, a=(0.45, 0.5, 1.1), b=(0.42, 0.52, 1.28)),
    dict(k="pan", t0=61.0, t1=82.0, keys=[
        (61.0, 0, 1.12), (65.5, 0, 1.24),
        (66.2, 1, 1.14), (69.5, 1, 1.24),
        (70.2, 2, 1.14), (73.5, 2, 1.24),
        (74.2, 3, 1.14), (82.0, 3, 1.28),
    ]),
    dict(k="art", img="thinking", t0=82.0, t1=99.0, a=(0.45, 0.5, 1.08), b=(0.42, 0.5, 1.22)),
    dict(k="ask", t0=99.0, t1=115.4),
    dict(k="soltitle", t0=115.4, t1=117.5),
    dict(k="pan", t0=117.5, t1=155.0, keys=[
        (117.5, 0, 1.14), (129.5, 0, 1.22),
        (130.2, 1, 1.14), (143.5, 1, 1.22),
        (144.2, 2, 1.14), (154.5, 2, 1.22),
        (154.8, 3, 1.14), (155.0, 3, 1.2),
    ]),
    dict(k="art", img="returned", t0=155.0, t1=185.4, a=(0.48, 0.5, 1.1), b=(0.52, 0.48, 1.28)),
    dict(k="end", t0=185.4, t1=None),
]
# Shorts: Part 1 ends after "Think about it."; Part 2 opens with question recap for feed discovery.
SHORTS = dict(tag="", p1_end=104.4, recap=(99.4, 104.4), card_t=103.8,
              suspects="Jago, Tamsin, Hedley, or Morwenna?")

def _gull(area=(18, 220, 494, 360), n=2, seed=3):
    return [dict(kind="fly", part="gull", area=area, n=n, speed=(12, 22), flap=2.2, size=(0.5, 0.85), seed=seed)]

def _cloud(*names, dx=16, period=50):
    return [dict(kind="sprite", part=n, keys=[(0.0, dict(dx=0)), (period, dict(dx=dx * (1 if i % 2 == 0 else -0.7)))])
            for i, n in enumerate(names)]

def _leaves(n=6, seed=7):
    return [dict(kind="glint", part="leaf", area=(20, 40, 490, 160), n=n, life=3.2, drift=8.0, alpha=0.75, seed=seed)]

_NOD = dict(jago=62.0, tamsin=66.5, hedley=70.5, morwenna=74.5)

ANIM = {
    "hook": dict(art="hook", layers=[*_gull(seed=1), *_leaves(4, seed=2)]),
    "cast": dict(art="cast", layers=[
        dict(kind="sprite", part="jago", idle=True, blink=True),
        dict(kind="sprite", part="tamsin", idle=True, blink=True),
        dict(kind="sprite", part="hedley", idle=True, blink=True),
        dict(kind="sprite", part="morwenna", idle=True, blink=True),
    ]),
    "shed": dict(art="shed", layers=[
        dict(kind="sprite", part="marrow", idle=False,
             keys=[(5.0, dict(a=1.0, s=1.0)), (18.0, dict(a=1.0, s=1.02))]),
        dict(kind="sprite", part="sparkle", show=(14.5, 19.0), fade=0.4,
             keys=[(14.5, dict(a=0.2, s=0.7)), (16.0, dict(a=1.0, s=1.15)), (18.5, dict(a=0.0, s=1.3))]),
        *_gull(seed=5),
    ]),
    "empty": dict(art="empty", layers=[*_gull(seed=9), *_leaves(5, seed=10)]),
    "allotments": dict(art="allotments", layers=[
        dict(kind="sprite", part="hedley", idle=True, blink=True,
             walk=dict(t0=25.0, t1=28.5, dx=-60, steps=4, bob=1.6), show=(24.8, None), fade=0.4),
        *_cloud("cloud1", "cloud2"),
        *_gull(seed=13), *_leaves(8, seed=14),
    ]),
    "bench": dict(art="bench", layers=[
        dict(kind="sprite", part="agnes", idle=True, blink=True, talk=dict(seg=6, quotes=True), nods=[50.0]),
        dict(kind="sprite", part="flask"),
        dict(kind="sprite", part="cup"),
        dict(kind="rise", part="steam", at=(188, 110), n=3, life=2.8, height=24, alpha=0.75),
        *_cloud("cloud1", dx=12, period=45),
        *_gull(seed=17),
    ]),
    "lineup": dict(art="lineup", layers=[
        dict(kind="sprite", part="jago", idle=True, blink=True, talk=dict(seg=7, quotes=True), nods=[_NOD["jago"]]),
        dict(kind="sprite", part="tamsin", idle=True, blink=True, talk=dict(seg=8, quotes=True), nods=[_NOD["tamsin"]]),
        dict(kind="sprite", part="hedley", idle=True, blink=True, talk=dict(seg=9, quotes=True), nods=[_NOD["hedley"]]),
        dict(kind="sprite", part="morwenna", idle=True, blink=True, talk=dict(seg=10, quotes=True), nods=[_NOD["morwenna"]]),
        dict(kind="sprite", part="agnes", idle=True, blink=True, show=(61.0, 66.0), fade=0.4),
        *_gull(area=(18, 220, 4 * 512 - 18, 360), n=4, seed=21),
    ]),
    "thinking": dict(art="thinking", layers=[
        dict(kind="sprite", part="agnes", idle=True, blink=True, nods=[83.0, 90.0]),
        *_cloud("cloud1", dx=10, period=40),
        *_gull(seed=25),
    ]),
    "returned": dict(art="returned", layers=[
        dict(kind="sprite", part="marrow", show=(170.5, None), fade=0.5),
        dict(kind="sprite", part="flowers", show=(172.0, None), fade=0.5),
        dict(kind="sprite", part="sparkle", show=(171.0, 176.0), fade=0.3,
             keys=[(171.0, dict(a=0.3, s=0.8)), (173.0, dict(a=1.0, s=1.2)), (175.5, dict(a=0.0, s=1.35))]),
        dict(kind="sprite", part="morwenna", idle=True, blink=True,
             swaps=[(171.5, "sheepish", 0.5), (178.0, "empty", 0.5)]),
        dict(kind="sprite", part="hedley", idle=True, blink=True, show=(175.0, None), fade=0.5),
        *_gull(seed=29),
    ]),
}
