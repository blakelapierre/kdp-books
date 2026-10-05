"""Case 4, The Sandbar at High Tide: colour-detailed art with SIMPLE ANIMATIONS (anim.py).

Times are ORIGINAL narration times (timing-case-04.json). render.py adds the hook shift and the countdown splice.
Art: art_case04.py -> work/art-04/ (plates + part sprites). ANIM below choreographs each picture.
The three suspects (Morwenna, Pip, Mr Rundle) share idle / blink / nod treatment before the solution; only
Mr Rundle's after-solution reaction (sheepish, handing the compass back) differs."""
NUM, NAME = 4, "The Sandbar at High Tide"
STYLE = "color-detailed"
SLUG = "standalone-03-tidewhistle-case-04-the-sandbar-at-high-tide"
AUDIO = "standalone-03-tidewhistle-06-case-04-the-sandbar-at-high-tide.mp3"
TIMING = "timing-case-04.json"; CLUES = "clues/case-04.json"; ART = "work/art-04"; HOOK_WAV = "work/hook-04.wav"
QUESTION = "Who took the brass compass, and what gave them away?"
HOOK_LINES = ["Who took the", "brass compass?"]; HOOK_EMOJI = "\U0001F9ED"   # compass
HOOK_SAY = "A brass compass has vanished, and only one clue gives the thief away. Can you spot it?"
HOOK_FOCUS = ((0.48, 0.55, 1.25), (0.46, 0.58, 1.65))   # push in on the empty sill / dashed ring
LINEUP_PANELS = 3
TRIM = 0.45
CUT, EXTRA = 119.8, 7.0          # after "...the solution follows." (119.26); "The Solution." was 123.76
NARR_END = 119.26
AUDIO_END = 176.31               # last word of the closing paragraph
NO_CAP = {0, 1, 12, 15}          # case title, question and "The Solution." are shown as cards
SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=4.5),
    dict(k="art", img="harbour", t0=4.5, t1=28.0, a=(0.5, 0.5, 1.08), b=(0.55, 0.48, 1.28)),
    dict(k="art", img="sandbar", t0=28.0, t1=43.0, a=(0.5, 0.52, 1.08), b=(0.62, 0.48, 1.28)),
    dict(k="art", img="window", t0=43.0, t1=58.0, a=(0.48, 0.52, 1.12), b=(0.46, 0.55, 1.45)),
    dict(k="art", img="quay", t0=58.0, t1=65.2, a=(0.5, 0.5, 1.08), b=(0.48, 0.48, 1.22)),
    dict(k="pan", t0=65.2, t1=103.2, keys=[
        (65.2, 0, 1.12), (77.4, 0, 1.24),
        (78.2, 1, 1.14), (84.0, 1, 1.24),
        (84.8, 2, 1.14), (103.2, 2, 1.28),
    ]),
    dict(k="art", img="thinking", t0=103.2, t1=108.2, a=(0.5, 0.5, 1.08), b=(0.45, 0.5, 1.22)),
    dict(k="ask", t0=108.2, t1=123.7),
    dict(k="soltitle", t0=123.7, t1=125.8),
    dict(k="art", img="sandbar", t0=125.8, t1=148.4, a=(0.55, 0.5, 1.12), b=(0.58, 0.46, 1.3)),
    dict(k="pan", t0=148.4, t1=160.1, keys=[(148.4, 0, 1.14), (154.0, 0, 1.2), (154.6, 1, 1.14), (160.1, 1, 1.2)]),
    dict(k="art", img="boat", t0=160.1, t1=168.5, a=(0.5, 0.5, 1.1), b=(0.52, 0.48, 1.3)),
    dict(k="art", img="returned", t0=168.5, t1=176.2, a=(0.5, 0.5, 1.08), b=(0.48, 0.48, 1.22)),
    dict(k="end", t0=176.2, t1=None),
]
# Shorts cuts inside narration pauses: 113.5 after "Think about it." (ends 113.14);
# 107.9 between "...handwriting." (107.30) and "Can you solve it?" (108.40).
SHORTS = dict(tag="", p1_end=113.5, recap=(107.9, 113.5), card_t=112.7, suspects="Morwenna, Pip, or Mr Rundle?")

# ----------------------------------------------------------------------------- animation choreography (ORIGINAL narration times)
def _sea(area=(18, 100, 494, 176), n_wave=16, n_glint=10, n_gull=3, seed=3):
    rows = [area[1] + (area[3] - area[1]) * (i + 0.5) / 5 for i in range(5)]
    return [
        dict(kind="glint", part="wave", area=area, n=n_wave, life=2.6, drift=5.5, rows=rows, alpha=0.8, seed=seed),
        dict(kind="glint", part="glint", area=area, n=n_glint, life=1.7, drift=1.8, alpha=0.65, seed=seed + 11),
        dict(kind="fly", part="gull", area=(area[0], area[3] - 10, area[2], area[3] + 90), n=n_gull,
             speed=(14, 26), flap=2.3, size=(0.55, 0.95), seed=seed + 19),
    ]

def _flags(n=9, amp=7.0, period=2.4):
    return [dict(kind="sprite", part=f"flag{i}", pivot="top", wobble=dict(amp=amp, period=period + 0.15 * (i % 3), amp2=2.5, period2=1.1))
            for i in range(n)]

def _boats(*names, amp=1.4, period=4.2, rock=1.2):
    return [dict(kind="sprite", part=n, bob=dict(amp=amp, period=period + 0.4 * i, rock=rock)) for i, n in enumerate(names)]

def _cloud(*names, dx=18, period=55):
    out = []
    for i, n in enumerate(names):
        out.append(dict(kind="sprite", part=n, keys=[(0.0, dict(dx=0)), (period, dict(dx=dx * (1 if i % 2 == 0 else -0.7)))]))
    return out

# Equal suspect treatment: same idle / blink / nod on introduction (no special reaction before the solution).
_SUSPECT_NOD = dict(morwenna=66.0, pip=79.0, rundle=85.5)   # a gentle nod as each is named

ANIM = {
    "hook": dict(art="hook", layers=[
        dict(kind="sprite", part="ring", idle=False),
        dict(kind="sprite", part="mullions"),
        dict(kind="sprite", part="boat", bob=dict(amp=1.2, period=3.8, rock=1.0)),
        dict(kind="clock", part="hour", pivot=(428, 318), keys=[(0.0, dict(rot=-15)), (5.3, dict(rot=-12))]),
        dict(kind="clock", part="minute", pivot=(428, 318), keys=[(0.0, dict(rot=180)), (5.3, dict(rot=186))]),
        *_sea(area=(112, 150, 340, 336), n_wave=8, n_glint=6, n_gull=2, seed=1),
    ]),
    "cast": dict(art="cast", layers=[
        dict(kind="sprite", part="morwenna", idle=True, blink=True),
        dict(kind="sprite", part="pip", idle=True, blink=True),
        dict(kind="sprite", part="rundle", idle=True, blink=True),
    ]),
    "harbour": dict(art="harbour", layers=[
        dict(kind="sprite", part="quill", idle=True, blink=True, talk=dict(seg=3, quotes=True),
             nods=[22.5]),
        dict(kind="sprite", part="agnes", idle=True, blink=True,
             walk=dict(t0=5.5, t1=8.5, dx=-70, steps=5, bob=1.8),
             show=(5.4, None), fade=0.5),
        dict(kind="sprite", part="chalk", reveal=dict(t0=18.8, t1=21.5, soft=8)),
        *_boats("boat1", "boat2"),
        *_cloud("cloud1", "cloud2"),
        dict(kind="sprite", part="pennant", pivot="top", wobble=dict(amp=9, period=2.1, amp2=3, period2=0.9)),
        *_flags(9),
        *_sea(seed=5),
    ]),
    "sandbar": dict(art="sandbar", layers=[
        # Pre-solution: diggers on the bar at low tide; tide rises as the narration describes high water.
        dict(kind="sprite", part="diggers", show=(28.0, 37.0), fade=0.6, idle=True),
        dict(kind="reveal_plate", plate="sandbar_high", area=(40, 100, 420, 170),
             keys=[(28.0, 108), (36.5, 108), (39.5, 145), (42.5, 155),
                   (125.8, 155), (134.0, 155), (138.0, 155)],   # stay high through the solution beat
             wave=(1.4, 36.0, 0.55)),
        # Solution overlays (only after "The Solution.")
        dict(kind="sprite", part="ghost", show=(128.5, None), fade=0.5),
        dict(kind="sprite", part="tideboard", show=(133.5, None), fade=0.5),
        dict(kind="sprite", part="depth", show=(140.0, None), fade=0.5),
        *_cloud("cloud1", "cloud2", dx=14, period=48),
        *_sea(area=(18, 70, 494, 236), n_wave=20, n_glint=12, n_gull=4, seed=9),
    ]),
    "window": dict(art="window", layers=[
        dict(kind="sprite", part="compass", show=(None, 56.6), fade=0.45),
        dict(kind="sprite", part="needle", pivot=(226, 192.2), show=(None, 56.6), fade=0.45,
             wobble=dict(amp=2.5, period=3.2)),
        dict(kind="sprite", part="ring", show=(56.5, None), fade=0.5),   # empty sill mark after it vanishes
        dict(kind="sprite", part="mullions"),
        dict(kind="sprite", part="boat", bob=dict(amp=1.1, period=3.6, rock=0.9)),
        # Clock advances from half past eleven toward half past twelve (0° = XII, clockwise positive via -rot in engine)
        dict(kind="clock", part="hour", pivot=(428, 318),
             keys=[(43.0, dict(rot=-15)), (57.0, dict(rot=15))]),
        dict(kind="clock", part="minute", pivot=(428, 318),
             keys=[(43.0, dict(rot=180)), (50.0, dict(rot=0)), (57.0, dict(rot=180))]),
        *_sea(area=(112, 150, 340, 336), n_wave=8, n_glint=6, n_gull=2, seed=13),
    ]),
    "quay": dict(art="quay", layers=[
        dict(kind="sprite", part="ollie", idle=True, blink=True, nods=[58.5],
             walk=dict(t0=58.0, t1=60.5, dx=-55, steps=4, bob=1.6)),
        *_boats("boat1", "boat2"),
        *_cloud("cloud1"),
        *_sea(seed=17),
    ]),
    "lineup": dict(art="lineup", layers=[
        dict(kind="sprite", part="morwenna", idle=True, blink=True, nods=[_SUSPECT_NOD["morwenna"]]),
        dict(kind="sprite", part="pip", idle=True, blink=True, nods=[_SUSPECT_NOD["pip"]]),
        dict(kind="sprite", part="rundle", idle=True, blink=True, talk=dict(seg=10, quotes=True),
             nods=[_SUSPECT_NOD["rundle"]]),
        dict(kind="sprite", part="vicar", idle=True, blink=True, show=(65.2, 78.0), fade=0.4),
        dict(kind="sprite", part="agnes", idle=True, blink=True, show=(78.0, 84.5), fade=0.4),
        dict(kind="rise", part="steam", at=(512 + 450, 155), n=4, life=3.0, height=28, show=(78.0, 84.5), alpha=0.8),
        *_boats("boat"),
        *_cloud("cloud1"),
        *_sea(area=(18, 100, 1520, 196), n_wave=22, n_glint=14, n_gull=5, seed=21),
    ]),
    "thinking": dict(art="thinking", layers=[
        dict(kind="sprite", part="agnes", idle=True, blink=True, nods=[103.5]),
        *_boats("boat1"),
        *_sea(seed=25),
    ]),
    "boat": dict(art="boat", layers=[
        dict(kind="sprite", part="rope", show=(160.1, 163.5), fade=0.4),
        dict(kind="sprite", part="compass", show=(162.8, None), fade=0.5),
        dict(kind="sprite", part="sparkle", show=(163.2, 166.0), fade=0.3,
             keys=[(163.2, dict(a=0.2, s=0.7)), (164.0, dict(a=1.0, s=1.15)), (165.5, dict(a=0.0, s=1.3))]),
        *_sea(area=(18, 14, 494, 370), n_wave=14, n_glint=10, n_gull=2, seed=29),
    ]),
    "returned": dict(art="returned", layers=[
        dict(kind="sprite", part="rundle", idle=True, blink=True,
             swaps=[(170.5, "given", 0.6), (172.5, "smile", 0.5)]),
        dict(kind="sprite", part="quill", idle=True, blink=True,
             swaps=[(170.5, "compass", 0.6)]),
        *_cloud("cloud1"),
        *_flags(4, amp=6.5, period=2.2),
        *_sea(area=(18, 100, 494, 122), n_wave=10, n_glint=6, n_gull=2, seed=31),
    ]),
}

