"""Draws the black-and-white ink illustrations for Stars over Frostwood -> ../illustrations/*.png
(300 DPI grayscale, pure black line art on white). Deterministic: same seeds -> same images.
Run from src/: python3 illustrations.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inkart import render, Wt, K, lerp
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "illustrations")

PLOUGH = [(0.0, 0.0), (0.09, 0.03), (0.17, 0.02), (0.24, -0.02), (0.33, -0.01), (0.35, -0.08), (0.26, -0.1)]
CASSIO = [(0.0, 0.0), (0.06, -0.06), (0.12, 0.0), (0.18, -0.07), (0.24, -0.01)]

def sky(k, w, h, y0, dense=1.0, moon=(0.84, 0.86, 14), cons=True):
    k.snowfall(0, y0, w, h, n=int(w * h / 1500))
    k.stars(6, y0, w - 6, h - 4, n=int(w * (h - y0) / 260 * dense), big=0.2, rmax=3.6)
    if moon: k.moon(w * moon[0], h * moon[1], moon[2])
    if cons:
        ox, oy = w * 0.12, h * 0.9
        k.constellation([(ox + u * w, oy + v * w) for u, v in PLOUGH], r=2.2)

def frontispiece(k, w, h):
    m = 9; k.frame(m, m, w - m, h - m)
    k.clip_rect(m + 4, m + 4, w - m - 4, h - m - 4)
    sky(k, w, h, h * 0.45, dense=1.3, moon=(0.8, 0.88, 22))
    ox, oy = w * 0.55, h * 0.72
    k.constellation([(ox + u * w, oy + v * w) for u, v in CASSIO], r=2.4)
    k.mountains(0, w, h * 0.3, [(w * 0.14, h * 0.5), (w * 0.86, h * 0.53)])
    k.summit(w * 0.05, w * 0.95, h * 0.3, w * 0.35, w * 0.65, h * 0.57)
    k.lodge(w * 0.37, h * 0.57, w * 0.26, h * 0.075, dome=True)
    # winding path with lamps up the mountain
    P = [(w * (lerp(0.47, 0.39, t) + 0.1 * math.sin(t * 9) * (1 - t)), h * lerp(0.21, 0.575, t)) for t in [i / 40 for i in range(41)]]
    k.c.setDash(1.8, 2.2); k.line(P, lw=0.6, amp=0); k.c.setDash()
    k.forest(0, w * 0.32, h * 0.3, 22, 40, 7); k.forest(w * 0.68, w, h * 0.3, 22, 40, 7)
    k.ground(0, w, h * 0.3, depth=h * 0.3, drifts=6)
    for t in (0.12, 0.3, 0.5, 0.72): x, y = P[int(t * 40)]; k.lamppost(x + 6, y, 36 * (1.05 - t * 0.7))
    k.cottage(w * 0.14, h * 0.22, 44, 40); k.cottage(w * 0.3, h * 0.2, 38, 44, door_side=0.2)
    k.ground(0, w, h * 0.21, depth=h * 0.21, drifts=3)
    k.telescope(w * 0.66, h * 0.1, 74, ang=58)
    k.sled(w * 0.4, h * 0.1, 30); k.mug(w * 0.32, h * 0.14, 9)
    k.pine(w * 0.08, h * 0.03, 125); k.pine(w * 0.93, h * 0.02, 140)
    k.unclip()

def title(k, w, h):
    sky(k, w, h, h * 0.45)
    k.mountains(0, w, h * 0.25, [(w * 0.14, h * 0.48), (w * 0.86, h * 0.5)])
    k.summit(w * 0.12, w * 0.88, h * 0.22, w * 0.38, w * 0.6, h * 0.56)
    k.lodge(w * 0.4, h * 0.56, w * 0.18, h * 0.12, dome=True)
    k.forest(0, w * 0.35, h * 0.22, 18, 32, 7); k.forest(w * 0.65, w, h * 0.22, 18, 32, 7)
    k.ground(0, w, h * 0.22, depth=h * 0.22, drifts=4)
    k.telescope(w * 0.5, h * 0.06, 40, ang=60)
    k.pine(w * 0.06, h * 0.03, 66); k.pine(w * 0.94, h * 0.03, 72)

def op_village(k, w, h):
    sky(k, w, h, h * 0.55, moon=(0.85, 0.85, 12))
    k.mountains(0, w, h * 0.45, [(w * 0.3, h * 0.7), (w * 0.7, h * 0.66)])
    k.forest(0, w, h * 0.42, 16, 26, 14)
    k.ground(0, w, h * 0.42, depth=h * 0.42, drifts=2)
    for (u, cw, ch) in [(0.05, 50, 42), (0.2, 42, 50), (0.68, 46, 44), (0.83, 44, 48)]:
        k.cottage(w * u, h * 0.3, cw, ch)
    k.bandstand(w * 0.5, h * 0.28, 52)
    k.ground(0, w, h * 0.3, depth=h * 0.3, drifts=3)
    k.pond(w * 0.5, h * 0.13, 90); k.lamppost(w * 0.3, h * 0.08, 34); k.lamppost(w * 0.7, h * 0.08, 34)

def op_railway(k, w, h):
    sky(k, w, h, h * 0.5)
    k.mountains(0, w, h * 0.35, [(w * 0.2, h * 0.68), (w * 0.55, h * 0.78), (w * 0.85, h * 0.62)])
    k.forest(0, w, h * 0.32, 18, 36, 18)
    k.ground(0, w, h * 0.32, depth=h * 0.32, drifts=2)
    k.rails(w * 0.02, w * 0.98, h * 0.17)
    k.locomotive(w * 0.5, h * 0.17 + 1, 74); k.carriage(w * 0.5 - 3, h * 0.17 + 1, 62, facing=-1, n_win=4)
    k.signal(w * 0.9, h * 0.17, 40)

def op_path(k, w, h):
    sky(k, w, h, h * 0.55, moon=(0.12, 0.84, 12), cons=False)
    k.mountains(0, w, h * 0.12, [(w * 0.5, h * 0.78)])
    P = [(w * (0.5 + 0.22 * math.sin(t * 7) * (1 - t)), h * (0.06 + 0.66 * t)) for t in [i / 40 for i in range(41)]]
    k.c.setDash(1.8, 2.2); k.line(P, lw=0.7, amp=0); k.c.setDash()
    for t in (0.15, 0.45, 0.75): x, y = P[int(t * 40)]; k.lamppost(x + 6, y, 40 * (1.1 - t * 0.7))
    k.forest(0, w * 0.3, h * 0.08, 30, 56, 6); k.forest(w * 0.7, w, h * 0.08, 30, 56, 6)
    k.ground(0, w, h * 0.08, depth=h * 0.08, drifts=1)
    k.signpost(w * 0.37, h * 0.04, 28, arrows=[("DOME", 1)])

def op_observatory(k, w, h):
    sky(k, w, h, h * 0.35, dense=1.5, moon=(0.86, 0.85, 14))
    ox, oy = w * 0.6, h * 0.85
    k.constellation([(ox + u * w, oy + v * w) for u, v in CASSIO], r=2.2)
    k.lodge(w * 0.25, h * 0.12, w * 0.5, h * 0.42, dome=True)
    k.forest(0, w * 0.24, h * 0.1, 26, 46, 4); k.forest(w * 0.77, w, h * 0.1, 26, 46, 4)
    k.ground(0, w, h * 0.12, depth=h * 0.12, drifts=1)

def v_scope(k, w, h):
    k.stars(4, h * 0.45, w - 4, h - 4, n=14)
    k.ground(w * 0.03, w * 0.97, h * 0.2, depth=h * 0.2, drifts=1, ticks=False)
    k.telescope(w * 0.5, h * 0.18, h * 0.62, ang=55); k.pine(w * 0.16, h * 0.18, h * 0.66); k.pine(w * 0.84, h * 0.18, h * 0.58, style="line")

def v_moon(k, w, h):
    k.stars(4, h * 0.3, w - 4, h - 4, n=18); k.moon(w * 0.5, h * 0.6, h * 0.24)
    k.ground(w * 0.03, w * 0.97, h * 0.16, depth=h * 0.16, drifts=1, ticks=False)
    k.pine(w * 0.18, h * 0.14, h * 0.55); k.pine(w * 0.82, h * 0.14, h * 0.6)

def v_dome(k, w, h):
    k.stars(4, h * 0.5, w - 4, h - 4, n=16)
    k.ground(w * 0.03, w * 0.97, h * 0.2, depth=h * 0.2, drifts=1, ticks=False)
    k.observatory(w * 0.5, h * 0.2, h * 0.5); k.pine(w * 0.2, h * 0.18, h * 0.6); k.pine(w * 0.8, h * 0.18, h * 0.65)

def v_lamp(k, w, h):
    k.stars(4, h * 0.45, w - 4, h - 4, n=14)
    k.ground(w * 0.03, w * 0.97, h * 0.2, depth=h * 0.2, drifts=1, ticks=False)
    k.lamppost(w * 0.42, h * 0.18, h * 0.66); k.sled(w * 0.6, h * 0.14, h * 0.4); k.pine(w * 0.15, h * 0.18, h * 0.6); k.pine(w * 0.86, h * 0.18, h * 0.55)

def v_stars(k, w, h):
    k.constellation([(w * (0.18 + u * 2.0), h * (0.62 + v * 2.0)) for u, v in PLOUGH], r=2.4)
    k.ground(w * 0.03, w * 0.97, h * 0.18, depth=h * 0.18, drifts=1, ticks=False)
    k.forest(w * 0.05, w * 0.95, h * 0.16, h * 0.25, h * 0.4, 7)

def v_cottage(k, w, h):
    k.stars(4, h * 0.55, w - 4, h - 4, n=12)
    k.ground(w * 0.03, w * 0.97, h * 0.2, depth=h * 0.2, drifts=1, ticks=False)
    k.cottage(w * 0.38, h * 0.18, h * 0.6, h * 0.55); k.pine(w * 0.22, h * 0.18, h * 0.6); k.pine(w * 0.78, h * 0.18, h * 0.66)

def thanks(k, w, h):
    sky(k, w, h, h * 0.45, cons=False, moon=(0.85, 0.82, 11))
    k.mountains(0, w, h * 0.25, [(w * 0.3, h * 0.6), (w * 0.7, h * 0.72)])
    k.lodge(w * 0.36, h * 0.25, w * 0.28, h * 0.32, dome=True)
    k.forest(0, w * 0.34, h * 0.24, 18, 30, 5); k.forest(w * 0.66, w, h * 0.24, 18, 30, 5)
    k.ground(0, w, h * 0.25, depth=h * 0.25, drifts=2)

VIGNETTES = ["v_scope", "v_moon", "v_dome", "v_lamp", "v_stars", "v_cottage"]
SPECS = {
    "frontispiece": (4.7, 7.0, frontispiece, 31),
    "title": (4.7, 2.6, title, 3),
    "opener-easy": (4.7, 2.4, op_village, 11), "opener-medium": (4.7, 2.4, op_railway, 12),
    "opener-hard": (4.7, 2.4, op_path, 13), "opener-expert": (4.7, 2.4, op_observatory, 14),
    "thanks": (3.6, 1.7, thanks, 21),
    **{n: (1.9, 0.85, globals()[n], 60 + i) for i, n in enumerate(VIGNETTES)},
}

if __name__ == "__main__":
    only = set(sys.argv[1:])
    for name, (wi, hi, fn, seed) in SPECS.items():
        if only and name not in only: continue
        render(os.path.join(OUT, name + ".png"), wi, hi, fn, seed=seed); print("drew", name)
