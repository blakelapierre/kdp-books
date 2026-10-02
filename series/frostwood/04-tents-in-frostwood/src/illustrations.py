"""Draws the black-and-white ink illustrations for Tents in Frostwood -> ../illustrations/*.png
(300 DPI grayscale, pure black line art on white). Deterministic: same seeds -> same images.
Run from src/: python3 illustrations.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inkart import render, Wt, K, lerp
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "illustrations")

def camp_scene(k, w, h, base, tents=((0.42, 34), (0.62, 28)), fire=(0.52, 16), big=True):
    k.snowfall(0, base, w, h, n=int(w * h / 900))
    k.stars(6, base + (h - base) * 0.55, w - 6, h - 4, n=int(w / 9))
    k.moon(w * 0.84, h - (h - base) * 0.2, min(14, (h - base) * 0.12))
    k.mountains(0, w, base + (h - base) * 0.1, [(w * 0.12, base + (h - base) * 0.48), (w * 0.38, base + (h - base) * 0.7), (w * 0.66, base + (h - base) * 0.52), (w * 0.9, base + (h - base) * 0.62)])
    k.forest(0, w * 0.3, base + (h - base) * 0.06, (h - base) * 0.16, (h - base) * 0.3, int(w / 40))
    k.forest(w * 0.74, w, base + (h - base) * 0.06, (h - base) * 0.16, (h - base) * 0.3, int(w / 45))
    k.ground(0, w, base + (h - base) * 0.06, depth=(h - base) * 0.06 + base, drifts=5)
    for (u, tw) in tents: k.tent(w * u, base + 2, tw)
    if fire: k.campfire(w * fire[0], base - 4, fire[1])

def frontispiece(k, w, h):
    m = 9; k.frame(m, m, w - m, h - m)
    k.clip_rect(m + 4, m + 4, w - m - 4, h - m - 4)
    base = h * 0.3
    k.snowfall(0, 0, w, h, n=120)
    k.stars(20, h * 0.62, w - 20, h - 20, n=70, big=0.18, rmax=3.6)
    k.constellation([(w * 0.18, h * 0.86), (w * 0.26, h * 0.9), (w * 0.33, h * 0.88), (w * 0.38, h * 0.84), (w * 0.46, h * 0.85), (w * 0.47, h * 0.8), (w * 0.39, h * 0.79)])
    k.moon(w * 0.78, h * 0.86, 22)
    k.mountains(0, w, h * 0.42, [(w * 0.1, h * 0.6), (w * 0.35, h * 0.72), (w * 0.62, h * 0.58), (w * 0.88, h * 0.68)])
    k.lodge(w * 0.62, h * 0.42, w * 0.22, h * 0.09)
    k.forest(0, w * 0.55, h * 0.4, 18, 34, 12)
    k.forest(w * 0.85, w, h * 0.4, 18, 30, 3)
    k.ground(0, w, h * 0.41, depth=h * 0.1, drifts=2)
    k.forest(-10, w * 0.25, h * 0.3, 40, 75, 4)
    k.forest(w * 0.8, w + 10, h * 0.3, 45, 80, 3)
    k.ground(0, w, h * 0.3, depth=h * 0.3, drifts=6)
    k.tent(w * 0.4, h * 0.27, 62); k.tent(w * 0.62, h * 0.31, 44, glow=True)
    k.campfire(w * 0.52, h * 0.17, 34)
    k.stump(w * 0.3, h * 0.13, 22); k.lantern(w * 0.3, h * 0.13 + 12, 16)
    k.kettle(w * 0.66, h * 0.14, 10)
    k.firewood(w * 0.78, h * 0.13, 40)
    k.footprints([(w * (0.45 - 0.035 * i), h * (0.08 - 0.012 * i) + 4) for i in range(0, 8)])
    k.pine(w * 0.08, h * 0.04, 120); k.pine(w * 0.93, h * 0.02, 140)
    k.unclip()

def title(k, w, h):
    camp_scene(k, w, h, h * 0.3, tents=((0.4, 40), (0.6, 32)), fire=(0.5, 20))
    k.pine(w * 0.06, h * 0.05, 70); k.pine(w * 0.94, h * 0.05, 78); k.pine(w * 0.16, h * 0.06, 48, style="line")

def op_meadow(k, w, h):
    base = h * 0.32
    k.snowfall(0, base, w, h, n=40); k.stars(6, h * 0.7, w - 6, h - 4, n=26)
    k.mountains(0, w, h * 0.45, [(w * 0.2, h * 0.75), (w * 0.5, h * 0.88), (w * 0.8, h * 0.72)])
    k.forest(0, w * 0.32, h * 0.42, 20, 34, 6); k.forest(w * 0.66, w, h * 0.42, 20, 32, 6)
    k.lodge(w * 0.34, h * 0.42, w * 0.32, h * 0.26)
    k.ground(0, w, h * 0.42, depth=h * 0.42, drifts=4)
    k.snowman_free_fence(w * 0.05, w * 0.32, h * 0.22, 9); k.snowman_free_fence(w * 0.68, w * 0.95, h * 0.22, 9)
    k.tent(w * 0.5, h * 0.18, 34); k.sled(w * 0.68, h * 0.08, 30)
    k.footprints([(w * (0.32 + 0.03 * i), h * 0.1 + i * 0.7) for i in range(8)])

def op_trail(k, w, h):
    base = h * 0.3
    k.snowfall(0, base, w, h, n=40); k.stars(6, h * 0.72, w - 6, h - 4, n=22); k.moon(w * 0.15, h * 0.85, 11)
    k.mountains(0, w, h * 0.45, [(w * 0.3, h * 0.82), (w * 0.62, h * 0.7), (w * 0.86, h * 0.8)])
    k.forest(0, w, h * 0.4, 24, 44, 22)
    k.ground(0, w, h * 0.4, depth=h * 0.4, drifts=3)
    # winding trail
    L = [(w * (0.15 + 0.7 * t), h * (0.05 + 0.33 * t) + 10 * math.sin(t * 6)) for t in [i / 30 for i in range(31)]]
    k.c.setDash(2, 2.5); k.line(L, lw=0.7, amp=0); k.c.setDash()
    k.signpost(w * 0.32, h * 0.12, 34, arrows=[("RIDGE", 1), ("LODGE", -1)])
    k.tent(w * 0.66, h * 0.2, 32)
    k.pine(w * 0.07, h * 0.0, 72); k.pine(w * 0.93, h * 0.0, 66); k.pine(w * 0.5, h * 0.12, 40, style="line")

def op_grove(k, w, h):
    k.snowfall(0, 0, w, h, n=50); k.stars(6, h * 0.85, w - 6, h - 4, n=14)
    k.forest(0, w, h * 0.38, 40, 70, 18)
    k.ground(0, w, h * 0.38, depth=h * 0.38, drifts=3)
    k.forest(-5, w * 0.3, h * 0.12, 60, 100, 4); k.forest(w * 0.72, w + 5, h * 0.12, 60, 100, 4)
    k.ground(0, w, h * 0.12, depth=h * 0.12, drifts=2)
    k.tent(w * 0.45, h * 0.14, 40); k.campfire(w * 0.6, h * 0.07, 20); k.firewood(w * 0.33, h * 0.06, 26)

def op_ridge(k, w, h):
    k.snowfall(0, 0, w, h, n=40); k.stars(6, h * 0.62, w - 6, h - 4, n=40, big=0.25); k.moon(w * 0.86, h * 0.84, 13)
    k.mountains(0, w, h * 0.25, [(w * 0.18, h * 0.62), (w * 0.45, h * 0.8), (w * 0.75, h * 0.6)])
    k.ground(0, w, h * 0.3, depth=h * 0.3, drifts=2)
    k.tent(w * 0.3, h * 0.28, 30); k.tent(w * 0.5, h * 0.31, 26); k.tent(w * 0.7, h * 0.27, 30)
    k.campfire(w * 0.42, h * 0.14, 18); k.lantern(w * 0.6, h * 0.12, 14)
    k.pine(w * 0.06, h * 0.02, 60); k.pine(w * 0.94, h * 0.02, 64)

def v_tent(k, w, h):
    k.ground(0, w, h * 0.22, depth=h * 0.22, drifts=1, ticks=False)
    k.pine(w * 0.15, h * 0.2, h * 0.75); k.pine(w * 0.85, h * 0.2, h * 0.66)
    k.tent(w * 0.45, h * 0.2, h * 0.55); k.campfire(w * 0.67, h * 0.12, h * 0.28)

def v_lantern(k, w, h):
    k.ground(0, w, h * 0.2, depth=h * 0.2, drifts=1, ticks=False)
    k.stump(w * 0.42, h * 0.16, h * 0.5); k.lantern(w * 0.42, h * 0.16 + h * 0.28, h * 0.4); k.mug(w * 0.62, h * 0.18, h * 0.22)
    k.pine(w * 0.15, h * 0.18, h * 0.7, style="line"); k.pine(w * 0.86, h * 0.18, h * 0.62)

def v_sled(k, w, h):
    k.ground(0, w, h * 0.22, depth=h * 0.22, drifts=1, ticks=False)
    k.pine(w * 0.2, h * 0.2, h * 0.7); k.pine(w * 0.32, h * 0.2, h * 0.5); k.sled(w * 0.6, h * 0.14, h * 0.6)
    k.firewood(w * 0.84, h * 0.14, h * 0.4, rows=2)

def v_sign(k, w, h):
    k.ground(0, w, h * 0.22, depth=h * 0.22, drifts=1, ticks=False)
    k.signpost(w * 0.45, h * 0.18, h * 0.6, arrows=[("CAMP", 1), ("", -1)])
    k.pine(w * 0.18, h * 0.2, h * 0.72); k.pine(w * 0.8, h * 0.2, h * 0.6, style="line")

def v_kettle(k, w, h):
    k.ground(0, w, h * 0.22, depth=h * 0.22, drifts=1, ticks=False)
    k.campfire(w * 0.48, h * 0.12, h * 0.42); k.kettle(w * 0.7, h * 0.16, h * 0.16); k.mug(w * 0.28, h * 0.16, h * 0.2)
    k.pine(w * 0.1, h * 0.2, h * 0.6); k.pine(w * 0.9, h * 0.2, h * 0.7)

def v_moon(k, w, h):
    k.stars(4, h * 0.4, w - 4, h - 4, n=12); k.moon(w * 0.75, h * 0.72, h * 0.14)
    k.ground(0, w, h * 0.2, depth=h * 0.2, drifts=1, ticks=False)
    k.pine(w * 0.3, h * 0.18, h * 0.6); k.pine(w * 0.45, h * 0.18, h * 0.45); k.tent(w * 0.62, h * 0.18, h * 0.3)

def thanks(k, w, h):
    camp_scene(k, w, h, h * 0.32, tents=((0.38, 30), (0.6, 26)), fire=(0.5, 18))
    k.pine(w * 0.06, h * 0.05, 56); k.pine(w * 0.94, h * 0.05, 60)

VIGNETTES = ["v_tent", "v_lantern", "v_sled", "v_sign", "v_kettle", "v_moon"]
SPECS = {  # name: (width in, height in, function, seed)
    "frontispiece": (4.7, 7.0, frontispiece, 41),
    "title": (4.7, 2.6, title, 3),
    "opener-easy": (4.7, 2.4, op_meadow, 11), "opener-medium": (4.7, 2.4, op_trail, 12),
    "opener-hard": (4.7, 2.4, op_grove, 13), "opener-expert": (4.7, 2.4, op_ridge, 14),
    "thanks": (3.6, 1.7, thanks, 21),
    **{n: (1.9, 0.85, globals()[n], 50 + i) for i, n in enumerate(VIGNETTES)},
}

if __name__ == "__main__":
    only = set(sys.argv[1:])
    for name, (wi, hi, fn, seed) in SPECS.items():
        if only and name not in only: continue
        render(os.path.join(OUT, name + ".png"), wi, hi, fn, seed=seed); print("drew", name)
