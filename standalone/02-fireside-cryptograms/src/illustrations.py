"""Draws the black-and-white ink illustrations for Fireside Cryptograms -> ../illustrations/*.png
(300 DPI grayscale, pure black line art on white). Deterministic: same seeds -> same images.
Run from src/: python3 illustrations.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inkart import render, Wt, K, lerp
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "illustrations")

def boards(k, w, y0, y1, gap=10):
    k.hatch([(0, y0), (w, y0), (w, y1), (0, y1)], angle=90, gap=gap, lw=0.35, jitter=0.6)

def frontispiece(k, w, h):
    """A cabin sitting room on a snowy evening: fire, wingback chair, sleeping cat, cocoa and a puzzle."""
    m = 9; k.frame(m, m, w - m, h - m)
    k.clip_rect(m + 4, m + 4, w - m - 4, h - m - 4)
    floor = h * 0.22
    boards(k, w, floor, h)
    k.line([(0, floor), (w, floor)], lw=0.9, amp=0.2)
    k.bookshelf(w * 0.06, floor, w * 0.2, h * 0.5)
    k.window_snow(w * 0.62, h * 0.6, w * 0.26, h * 0.22)
    k.fireplace(w * 0.3, floor + 2, w * 0.34, h * 0.3, stockings=0)
    top = floor + 2 + h * 0.3 + h * 0.021
    k.candle(w * 0.35, top, 18); k.clockface(w * 0.47, top + 12, 11, roman=False); k.books(w * 0.58, top, 22, n=3)
    for i in range(9): k.line([(w * 0.5 + (i - 4) * w * 0.06, floor), (w * 0.5 + (i - 4) * w * 0.24, 0)], lw=0.4, amp=0)
    k.rug(w * 0.45, floor * 0.48, w * 0.6, floor * 0.6)
    k.armchair(w * 0.8, floor * 0.55, w * 0.22, facing=-1)
    k.floor_lamp(w * 0.94, floor * 0.5, h * 0.36)
    t = k.side_table(w * 0.17, floor * 0.45, 34)
    k.mug(w * 0.13, t + 2, 10); k.notepad(w * 0.21, t + 1, 14, letters="Q = T")
    k.cat(w * 0.45, floor * 0.36, 34)
    k.firewood(w * 0.7, floor * 0.75, 30, rows=2)
    k.unclip()

def title(k, w, h):
    """The cabin in the snowy woods, smoke curling from the chimney."""
    k.snowfall(w * 0.04, h * 0.25, w * 0.96, h, n=50); k.stars(w * 0.06, h * 0.6, w * 0.94, h - 4, n=18); k.moon(w * 0.84, h * 0.82, 11)
    k.forest(w * 0.04, w * 0.36, h * 0.24, 22, 44, 6); k.forest(w * 0.64, w * 0.96, h * 0.24, 22, 44, 6)
    k.cabin(w * 0.38, h * 0.22, w * 0.24, h * 0.52)
    k.ground(w * 0.03, w * 0.97, h * 0.22, depth=h * 0.22, drifts=3)
    k.firewood(w * 0.68, h * 0.2, 26, rows=2)
    k.pine(w * 0.1, h * 0.04, h * 0.66); k.pine(w * 0.9, h * 0.04, h * 0.7)
    k.footprints([(w * (0.45 - 0.03 * i), h * (0.14 - 0.012 * i)) for i in range(7)])

def op_embers(k, w, h):
    floor = h * 0.18
    boards(k, w, floor, h * 0.95)
    k.line([(w * 0.02, floor), (w * 0.98, floor)], lw=0.9, amp=0.2)
    k.fireplace(w * 0.3, floor + 2, w * 0.4, h * 0.62, stockings=0)
    top = floor + 2 + h * 0.62 + h * 0.043
    k.clockface(w * 0.5, top + 14, 12, roman=False); k.candle(w * 0.36, top, 20); k.books(w * 0.62, top, 22, n=2)
    k.kettle(w * 0.2, floor * 0.6, 14); k.firewood(w * 0.82, floor * 0.5, 34, rows=3)

def op_kindling(k, w, h):
    k.snowfall(w * 0.03, h * 0.3, w * 0.97, h, n=40)
    k.forest(w * 0.03, w * 0.97, h * 0.3, 26, 52, 12)
    k.ground(w * 0.02, w * 0.98, h * 0.3, depth=h * 0.3, drifts=3)
    k.cabin(w * 0.12, h * 0.18, w * 0.26, h * 0.5)
    k.firewood(w * 0.55, h * 0.14, 70, rows=3); k.stump(w * 0.78, h * 0.12, 30); k.lantern(w * 0.78, h * 0.12 + 17, 18)
    k.sled(w * 0.42, h * 0.08, 34)

def op_flame(k, w, h):
    floor = h * 0.2
    boards(k, w, floor, h * 0.95)
    k.line([(w * 0.02, floor), (w * 0.98, floor)], lw=0.9, amp=0.2)
    k.fireplace(w * 0.08, floor + 2, w * 0.36, h * 0.55, stockings=0)
    k.rug(w * 0.5, floor * 0.5, w * 0.5, floor * 0.6)
    k.armchair(w * 0.66, floor * 0.5, w * 0.2, facing=-1)
    t = k.side_table(w * 0.86, floor * 0.45, 32); k.mug(w * 0.83, t + 2, 9); k.spectacles(w * 0.9, t + 3, 12)
    k.window_snow(w * 0.55, h * 0.5, w * 0.2, h * 0.36, curtains=False)
    k.cat(w * 0.36, floor * 0.36, 32)

def op_glow(k, w, h):
    k.window_snow(w * 0.3, h * 0.3, w * 0.4, h * 0.58)
    k.moon(w * 0.6, h * 0.76, 10)
    k.line([(w * 0.18, h * 0.24), (w * 0.82, h * 0.24)], lw=1.0, amp=0.2)
    k.candle(w * 0.36, h * 0.24, 40); k.mug(w * 0.5, h * 0.245, 16); k.books(w * 0.65, h * 0.24, 44, n=3)
    k.cat(w * 0.5, h * 0.03, 40)

def v_mug(k, w, h):
    k.line([(w * 0.1, h * 0.12), (w * 0.9, h * 0.12)], lw=0.7, amp=0.3)
    k.mug(w * 0.32, h * 0.13, h * 0.3); k.books(w * 0.62, h * 0.13, h * 0.7, n=3)

def v_pencil(k, w, h):
    k.notepad(w * 0.4, h * 0.1, h * 0.55); k.pencil(w * 0.52, h * 0.12, h * 0.85, ang=22); k.spectacles(w * 0.74, h * 0.25, h * 0.5)

def v_cat(k, w, h):
    k.rug(w * 0.5, h * 0.25, w * 0.62, h * 0.3); k.cat(w * 0.5, h * 0.2, h * 0.75)

def v_wood(k, w, h):
    k.line([(w * 0.1, h * 0.1), (w * 0.9, h * 0.1)], lw=0.7, amp=0.3)
    k.firewood(w * 0.42, h * 0.1, h * 0.75, rows=3); k.kettle(w * 0.74, h * 0.12, h * 0.22)

def v_candle(k, w, h):
    k.line([(w * 0.1, h * 0.12), (w * 0.9, h * 0.12)], lw=0.7, amp=0.3)
    k.candle(w * 0.36, h * 0.13, h * 0.62); k.clockface(w * 0.62, h * 0.42, h * 0.27, roman=False)

def v_cabin(k, w, h):
    k.snowfall(w * 0.1, h * 0.3, w * 0.9, h, n=8)
    k.ground(w * 0.05, w * 0.95, h * 0.2, depth=h * 0.2, drifts=1, ticks=False)
    k.cabin(w * 0.4, h * 0.18, h * 0.62, h * 0.55); k.pine(w * 0.24, h * 0.18, h * 0.62); k.pine(w * 0.8, h * 0.18, h * 0.66)

def thanks(k, w, h):
    k.line([(w * 0.06, h * 0.12), (w * 0.94, h * 0.12)], lw=0.8, amp=0.3)
    k.armchair(w * 0.32, h * 0.12, w * 0.2); t = k.side_table(w * 0.55, h * 0.12, 28)
    k.mug(w * 0.53, t + 2, 9); k.floor_lamp(w * 0.12, h * 0.12, h * 0.85); k.cat(w * 0.78, h * 0.05, 34)

VIGNETTES = ["v_mug", "v_pencil", "v_cat", "v_wood", "v_candle", "v_cabin"]
SPECS = {
    "frontispiece": (4.7, 7.0, frontispiece, 17),
    "title": (4.7, 2.2, title, 3),
    "opener-easy": (4.7, 2.4, op_embers, 11), "opener-medium": (4.7, 2.4, op_kindling, 12),
    "opener-hard": (4.7, 2.4, op_flame, 13), "opener-expert": (4.7, 2.4, op_glow, 14),
    "thanks": (3.4, 1.5, thanks, 21),
    **{n: (1.9, 0.85, globals()[n], 70 + i) for i, n in enumerate(VIGNETTES)},
}

if __name__ == "__main__":
    only = set(sys.argv[1:])
    for name, (wi, hi, fn, seed) in SPECS.items():
        if only and name not in only: continue
        render(os.path.join(OUT, name + ".png"), wi, hi, fn, seed=seed); print("drew", name)
