"""Draws the black-and-white ink illustrations for The Frostwood Sketchbook -> ../illustrations/*.png
(300 DPI grayscale, pure black line art on white, same inkart house style as the other Frostwood books).
Deterministic: same seeds -> same images. Run from src/: python3 illustrations.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inkart import render, Wt, K, lerp
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "illustrations")

PINE = ["....#....", "...###...", "..#####..", "....#....", "..#####..", ".#######.", "....#....", "###...###", "#########"]

def sketchbook(k, x, y, w, pattern=PINE, ang=0):
    """A spiral-bound sketchbook lying open on its page of squares, part-shaded with a little picture."""
    h = w * 0.78
    k.rect(x - w / 2 + 2.2, y - 2.2, w, h, lw=0.6, fill=Wt)
    k.rect(x - w / 2, y, w, h, lw=0.9, fill=Wt)
    for i in range(9): k.circle(x - w * 0.42 + i * w * 0.105, y + h, max(1.0, w * 0.018), lw=0.5, fill=Wt)
    n = len(pattern); g = min(w * 0.62, h * 0.72) / n
    gx = x - n * g / 2 + w * 0.06; gy = y + h * 0.12
    for r, row in enumerate(pattern):
        for c, v in enumerate(row):
            if v == "#" and r < n - 2: k.rect(gx + c * g, gy + (n - 1 - r) * g, g, g, lw=0.2, fill=K)
    for i in range(n + 1):
        k.line([(gx + i * g, gy), (gx + i * g, gy + n * g)], lw=0.3, amp=0)
        k.line([(gx, gy + i * g), (gx + n * g, gy + i * g)], lw=0.3, amp=0)
    # clue ticks to the left and above
    for i in range(n):
        k.line([(gx - g * 1.6, gy + (i + 0.5) * g), (gx - g * 0.5, gy + (i + 0.5) * g)], lw=0.35, amp=0)
        k.line([(gx + (i + 0.5) * g, gy + n * g + g * 0.4), (gx + (i + 0.5) * g, gy + n * g + g * 1.2)], lw=0.35, amp=0)
    return y + h

def boards(k, w, y0, y1, gap=10):
    k.hatch([(0, y0), (w, y0), (w, y1), (0, y1)], angle=90, gap=gap, lw=0.35, jitter=0.6)

def frontispiece(k, w, h):
    """The lodge sitting room on a snowy evening: a window seat, the sketchbook and pencil on the side table."""
    m = 9; k.frame(m, m, w - m, h - m)
    k.clip_rect(m + 4, m + 4, w - m - 4, h - m - 4)
    floor = h * 0.22
    boards(k, w, floor, h)
    k.line([(0, floor), (w, floor)], lw=0.9, amp=0.2)
    k.window_snow(w * 0.08, h * 0.42, w * 0.36, h * 0.36)
    k.bookshelf(w * 0.72, floor, w * 0.22, h * 0.52)
    k.fireplace(w * 0.47, floor + 2, w * 0.22, h * 0.26, stockings=0)
    top = floor + 2 + h * 0.26 + h * 0.018
    k.candle(w * 0.5, top, 16); k.clockface(w * 0.6, top + 10, 9, roman=False)
    for i in range(9): k.line([(w * 0.5 + (i - 4) * w * 0.06, floor), (w * 0.5 + (i - 4) * w * 0.24, 0)], lw=0.4, amp=0)
    k.rug(w * 0.5, floor * 0.5, w * 0.62, floor * 0.6)
    k.armchair(w * 0.22, floor * 0.55, w * 0.24, facing=1)
    t = k.side_table(w * 0.62, floor * 0.42, 40)
    sketchbook(k, w * 0.6, t + 1, 40); k.pencil(w * 0.66, t + 4, 26, ang=15)
    k.mug(w * 0.52, t + 2, 9)
    k.floor_lamp(w * 0.06, floor * 0.5, h * 0.36)
    k.cat(w * 0.84, floor * 0.3, 36)
    k.unclip()

def title(k, w, h):
    """The lodge on its snowy hill above the pines, with the sketchbook in the foreground."""
    k.snowfall(w * 0.04, h * 0.3, w * 0.96, h, n=46); k.stars(w * 0.06, h * 0.62, w * 0.94, h - 4, n=18); k.moon(w * 0.86, h * 0.84, 10)
    k.summit(w * 0.2, w * 0.8, h * 0.28, w * 0.38, w * 0.62, h * 0.6)
    k.lodge(w * 0.4, h * 0.6, w * 0.2, h * 0.16)
    k.forest(w * 0.02, w * 0.3, h * 0.26, 20, 40, 7); k.forest(w * 0.7, w * 0.98, h * 0.26, 20, 40, 7)
    k.ground(w * 0.02, w * 0.98, h * 0.26, depth=h * 0.26, drifts=3)
    sketchbook(k, w * 0.5, h * 0.03, 70); k.pencil(w * 0.62, h * 0.05, 40, ang=18)
    k.pine(w * 0.08, h * 0.03, h * 0.6); k.pine(w * 0.92, h * 0.03, h * 0.64)

def op_room(k, w, h):
    floor = h * 0.2
    boards(k, w, floor, h * 0.95)
    k.line([(w * 0.02, floor), (w * 0.98, floor)], lw=0.9, amp=0.2)
    k.fireplace(w * 0.08, floor + 2, w * 0.34, h * 0.56, stockings=0)
    k.window_snow(w * 0.56, h * 0.48, w * 0.2, h * 0.38, curtains=True)
    k.rug(w * 0.5, floor * 0.5, w * 0.5, floor * 0.6)
    k.armchair(w * 0.82, floor * 0.5, w * 0.18, facing=-1)
    t = k.side_table(w * 0.58, floor * 0.42, 30); sketchbook(k, w * 0.58, t + 1, 28)
    k.cat(w * 0.38, floor * 0.34, 30)

def op_village(k, w, h):
    k.snowfall(w * 0.03, h * 0.3, w * 0.97, h, n=40); k.stars(w * 0.05, h * 0.7, w * 0.95, h - 4, n=16)
    k.forest(w * 0.02, w * 0.98, h * 0.4, 16, 30, 16)
    k.ground(w * 0.02, w * 0.98, h * 0.38, depth=h * 0.38, drifts=3)
    k.cottage(w * 0.06, h * 0.34, 46, 44); k.cottage(w * 0.2, h * 0.36, 38, 46, door_side=0.2)
    k.cottage(w * 0.72, h * 0.35, 44, 42); k.cottage(w * 0.86, h * 0.34, 36, 44, door_side=0.2)
    k.bandstand(w * 0.5, h * 0.3, 56)
    k.pond(w * 0.5, h * 0.12, 96); k.lamppost(w * 0.3, h * 0.06, 36); k.lamppost(w * 0.7, h * 0.06, 36)

def op_woods(k, w, h):
    k.snowfall(0, 0, w, h, n=50); k.stars(6, h * 0.86, w - 6, h - 4, n=12)
    k.forest(0, w, h * 0.4, 40, 70, 18)
    k.ground(0, w, h * 0.4, depth=h * 0.4, drifts=3)
    k.forest(-5, w * 0.28, h * 0.12, 60, 100, 4); k.forest(w * 0.74, w + 5, h * 0.12, 60, 100, 4)
    k.ground(0, w, h * 0.12, depth=h * 0.12, drifts=2)
    k.signpost(w * 0.42, h * 0.1, 34, arrows=[("LODGE", 1), ("VILLAGE", -1)])
    k.footprints([(w * (0.34 + 0.035 * i), h * (0.04 + 0.01 * i)) for i in range(9)])
    k.stump(w * 0.62, h * 0.06, 22); k.lantern(w * 0.62, h * 0.06 + 12, 14)

def op_mountain(k, w, h):
    k.snowfall(0, 0, w, h, n=36); k.stars(6, h * 0.62, w - 6, h - 4, n=40, big=0.25); k.moon(w * 0.14, h * 0.84, 12)
    k.mountains(0, w, h * 0.3, [(w * 0.12, h * 0.6), (w * 0.86, h * 0.66)])
    k.summit(w * 0.26, w * 0.74, h * 0.25, w * 0.42, w * 0.6, h * 0.62)
    k.lodge(w * 0.43, h * 0.62, w * 0.16, h * 0.12, dome=True)
    k.ground(0, w, h * 0.24, depth=h * 0.24, drifts=2)
    k.pine(w * 0.06, h * 0.02, 60); k.pine(w * 0.94, h * 0.02, 64)
    sketchbook(k, w * 0.3, h * 0.04, 34); k.lantern(w * 0.7, h * 0.08, 16)

def v_pencil(k, w, h):
    sketchbook(k, w * 0.42, h * 0.1, h * 0.95); k.pencil(w * 0.62, h * 0.12, h * 0.85, ang=22)

def v_mug(k, w, h):
    k.line([(w * 0.1, h * 0.12), (w * 0.9, h * 0.12)], lw=0.7, amp=0.3)
    k.mug(w * 0.32, h * 0.13, h * 0.3); k.books(w * 0.62, h * 0.13, h * 0.7, n=3)

def v_cat(k, w, h):
    k.rug(w * 0.5, h * 0.25, w * 0.62, h * 0.3); k.cat(w * 0.5, h * 0.2, h * 0.75)

def v_lantern(k, w, h):
    k.ground(0, w, h * 0.2, depth=h * 0.2, drifts=1, ticks=False)
    k.stump(w * 0.42, h * 0.16, h * 0.5); k.lantern(w * 0.42, h * 0.16 + h * 0.28, h * 0.4); k.mug(w * 0.62, h * 0.18, h * 0.22)
    k.pine(w * 0.15, h * 0.18, h * 0.7, style="line"); k.pine(w * 0.86, h * 0.18, h * 0.62)

def v_cottage(k, w, h):
    k.snowfall(w * 0.1, h * 0.3, w * 0.9, h, n=8)
    k.ground(w * 0.05, w * 0.95, h * 0.2, depth=h * 0.2, drifts=1, ticks=False)
    k.cottage(w * 0.38, h * 0.18, h * 0.6, h * 0.55); k.pine(w * 0.22, h * 0.18, h * 0.6); k.pine(w * 0.78, h * 0.18, h * 0.66)

def v_moon(k, w, h):
    k.stars(4, h * 0.4, w - 4, h - 4, n=12); k.moon(w * 0.75, h * 0.72, h * 0.14)
    k.ground(0, w, h * 0.2, depth=h * 0.2, drifts=1, ticks=False)
    k.pine(w * 0.3, h * 0.18, h * 0.6); k.pine(w * 0.45, h * 0.18, h * 0.45); k.lamppost(w * 0.62, h * 0.18, h * 0.55)

def thanks(k, w, h):
    k.line([(w * 0.06, h * 0.12), (w * 0.94, h * 0.12)], lw=0.8, amp=0.3)
    k.armchair(w * 0.3, h * 0.12, w * 0.2); t = k.side_table(w * 0.54, h * 0.12, 28)
    sketchbook(k, w * 0.54, t + 1, 24); k.floor_lamp(w * 0.1, h * 0.12, h * 0.85); k.cat(w * 0.78, h * 0.05, 34)

VIGNETTES = ["v_pencil", "v_mug", "v_cat", "v_lantern", "v_cottage", "v_moon"]
SPECS = {  # name: (width in, height in, function, seed)
    "frontispiece": (4.7, 7.0, frontispiece, 61),
    "title": (4.7, 2.5, title, 3),
    "opener-easy": (4.7, 2.4, op_room, 11), "opener-medium": (4.7, 2.4, op_village, 12),
    "opener-hard": (4.7, 2.4, op_woods, 13), "opener-expert": (4.7, 2.4, op_mountain, 14),
    "thanks": (3.4, 1.5, thanks, 21),
    **{n: (1.9, 0.85, globals()[n], 80 + i) for i, n in enumerate(VIGNETTES)},
}

if __name__ == "__main__":
    only = set(sys.argv[1:])
    for name, (wi, hi, fn, seed) in SPECS.items():
        if only and name not in only: continue
        render(os.path.join(OUT, name + ".png"), wi, hi, fn, seed=seed); print("drew", name)
