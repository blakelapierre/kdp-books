"""Draws the black-and-white ink illustrations for Logic on Lantern Lane -> ../illustrations/*.png
(300 DPI grayscale, pure black line art on white). Deterministic: same seeds -> same images.
Run from src/: python3 illustrations.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inkart import render, Wt, K, lerp
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "illustrations")


def lane(k, w, y0, y1, x0, x1, x2, x3):
    """A lane running into the distance: edges from (x0,y0)-(x1,y1) and (x3,y0)-(x2,y1)."""
    k.line([(x0, y0), (x1, y1)], lw=0.8, amp=0.3)
    k.line([(x3, y0), (x2, y1)], lw=0.8, amp=0.3)
    for i in range(7):
        t = i / 7
        ya = lerp(y0, y1, t); xa = lerp(x0, x1, t); xb = lerp(x3, x2, t)
        for j in range(4):
            u = (j + 0.5 + 0.3 * (i % 2)) / 4.3
            xx = lerp(xa, xb, u); L = (xb - xa) * 0.05
            k.line([(xx - L, ya + 1.5), (xx + L, ya + 1.5)], lw=0.35, amp=0.2)


def frontispiece(k, w, h):
    """Lantern Lane at dusk: cottages on both sides, lit lampposts, a cat on a wall, snow falling."""
    m = 9; k.frame(m, m, w - m, h - m)
    k.clip_rect(m + 4, m + 4, w - m - 4, h - m - 4)
    hz = h * 0.42
    k.snowfall(m + 6, hz + 40, w - m - 6, h - m - 6, n=70)
    k.stars(m + 10, h * 0.78, w - m - 10, h - m - 10, n=16)
    k.moon(w * 0.78, h * 0.86, 14)
    k.hills(m, w - m, hz + 6, amp=8, n=3)
    k.forest(w * 0.36, w * 0.64, hz + 4, 14, 26, 8)
    # far cottages first, then the near ones in front of them
    k.cottage(w * 0.25, hz - 2, w * 0.15, h * 0.13, door_side=0.5)
    k.cottage(w * 0.60, hz - 2, w * 0.15, h * 0.13, door_side=0.3)
    k.cottage(w * 0.02, hz - 46, w * 0.26, h * 0.24)
    k.cottage(w * 0.72, hz - 46, w * 0.26, h * 0.25, door_side=0.2)
    for x0, x1 in ((m + 4, w * 0.2), (w * 0.8, w - m - 4)):
        k.line([(x0, hz - 58), (x1, hz - 58)], lw=0.7, amp=0.2)
        k.line([(x0, hz - 66), (x1, hz - 66)], lw=0.7, amp=0.2)
        xx = x0 + 3
        while xx < x1:
            k.shape([(xx - 2, hz - 74), (xx + 2, hz - 74), (xx + 2, hz - 52), (xx, hz - 49), (xx - 2, hz - 52)], lw=0.6, fill=Wt, amp=0)
            xx += 9
    lane(k, w, m + 4, hz - 4, w * 0.14, w * 0.45, w * 0.55, w * 0.88)
    k.lamppost(w * 0.2, m + 30, h * 0.4)
    k.lamppost(w * 0.82, m + 30, h * 0.4)
    k.lamppost(w * 0.42, hz - 30, h * 0.16)
    k.lamppost(w * 0.6, hz - 30, h * 0.16)
    k.signpost(w * 0.5, m + 20, 70, text="LANTERN LANE")
    k.bench(w * 0.9, m + 24, 40)
    k.cat(w * 0.9, m + 24 + 40 * 0.26, 18)
    k.lantern(w * 0.3, m + 14, 22)
    k.footprints([(w * (0.5 + 0.025 * math.sin(i)), m + 60 + i * 14) for i in range(8)])
    k.unclip()


def title(k, w, h):
    """A row of three cottages with a lamppost and a bench."""
    k.snowfall(w * 0.04, h * 0.45, w * 0.96, h, n=40)
    k.ground(w * 0.03, w * 0.97, h * 0.14, depth=h * 0.14, drifts=2)
    k.cottage(w * 0.1, h * 0.14, w * 0.24, h * 0.62)
    k.cottage(w * 0.38, h * 0.14, w * 0.2, h * 0.52, door_side=0.4)
    k.cottage(w * 0.62, h * 0.14, w * 0.26, h * 0.66, door_side=0.2)
    k.lamppost(w * 0.06, h * 0.12, h * 0.85)
    k.lamppost(w * 0.94, h * 0.12, h * 0.85)
    k.bench(w * 0.5, h * 0.0 + 2, 30)


def op_easy(k, w, h):
    """Tea table by a window: teapot, cups and a cake."""
    k.window_snow(w * 0.3, h * 0.42, w * 0.4, h * 0.52)
    k.line([(w * 0.06, h * 0.3), (w * 0.94, h * 0.3)], lw=1.0, amp=0.2)
    k.line([(w * 0.08, h * 0.27), (w * 0.92, h * 0.27)], lw=0.6, amp=0.2)
    for x in (w * 0.12, w * 0.88):
        k.line([(x, h * 0.27), (x, h * 0.02)], lw=1.0, amp=0.2)
    k.teapot(w * 0.36, h * 0.31, 46)
    k.cup(w * 0.54, h * 0.31, 22)
    k.cup(w * 0.66, h * 0.31, 22)
    k.cake(w * 0.2, h * 0.31, 30)
    k.candle(w * 0.8, h * 0.31, 30)
    k.cat(w * 0.5, h * 0.02, 34)


def op_medium(k, w, h):
    """The village green with the bandstand, a pond and a bench."""
    k.snowfall(w * 0.03, h * 0.35, w * 0.97, h, n=40)
    k.forest(w * 0.02, w * 0.98, h * 0.3, 18, 36, 14)
    k.ground(w * 0.02, w * 0.98, h * 0.3, depth=h * 0.3, drifts=3)
    k.bandstand(w * 0.5, h * 0.22, w * 0.24)
    k.pond(w * 0.2, h * 0.12, w * 0.24)
    k.bench(w * 0.8, h * 0.1, 40)
    k.lamppost(w * 0.66, h * 0.06, h * 0.72)
    k.lamppost(w * 0.04, h * 0.06, h * 0.72)


def op_hard(k, w, h):
    """The bookshop corner: a shelf of books, an armchair and a lamp."""
    floor = h * 0.18
    k.line([(w * 0.02, floor), (w * 0.98, floor)], lw=0.9, amp=0.2)
    k.bookshelf(w * 0.06, floor, w * 0.3, h * 0.76)
    k.armchair(w * 0.55, floor * 0.55, w * 0.22, facing=-1)
    k.floor_lamp(w * 0.72, floor * 0.5, h * 0.7)
    t = k.side_table(w * 0.86, floor * 0.45, 30)
    k.books(w * 0.86, t + 1, 22, n=3)
    k.window_snow(w * 0.42, h * 0.52, w * 0.2, h * 0.38, curtains=False)
    k.rug(w * 0.6, floor * 0.4, w * 0.5, floor * 0.5)


def op_expert(k, w, h):
    """The lantern parade at night: a line of lanterns going down the lane under the moon."""
    k.stars(w * 0.04, h * 0.55, w * 0.96, h - 4, n=26)
    k.moon(w * 0.85, h * 0.8, 12)
    k.hills(w * 0.02, w * 0.98, h * 0.4, amp=7, n=3)
    k.cottage(w * 0.04, h * 0.3, w * 0.18, h * 0.36)
    k.cottage(w * 0.78, h * 0.3, w * 0.18, h * 0.38, door_side=0.2)
    k.ground(w * 0.02, w * 0.98, h * 0.3, depth=h * 0.3, drifts=2, ticks=False)
    for i in range(7):
        t = i / 6
        x = lerp(w * 0.28, w * 0.7, t); y = lerp(h * 0.06, h * 0.3, t); s = lerp(34, 14, t)
        k.line([(x, y), (x, y + s * 1.4)], lw=0.8, amp=0)
        k.lantern(x, y + s * 1.4, s * 0.6)


def thanks(k, w, h):
    k.line([(w * 0.06, h * 0.12), (w * 0.94, h * 0.12)], lw=0.8, amp=0.3)
    k.lamppost(w * 0.12, h * 0.12, h * 0.85)
    k.bench(w * 0.42, h * 0.12, 46)
    k.cat(w * 0.42, h * 0.12 + 46 * 0.26, 22)
    k.cottage(w * 0.64, h * 0.12, w * 0.26, h * 0.7)


def v_teapot(k, w, h):
    k.line([(w * 0.1, h * 0.12), (w * 0.9, h * 0.12)], lw=0.7, amp=0.3)
    k.teapot(w * 0.38, h * 0.13, h * 0.95); k.cup(w * 0.7, h * 0.13, h * 0.4)


def v_lamp(k, w, h):
    k.snowfall(w * 0.1, h * 0.3, w * 0.9, h, n=8)
    k.line([(w * 0.1, h * 0.08), (w * 0.9, h * 0.08)], lw=0.7, amp=0.3)
    k.lamppost(w * 0.5, h * 0.08, h * 0.9)
    k.bench(w * 0.72, h * 0.08, h * 0.45)


def v_cat(k, w, h):
    k.rug(w * 0.5, h * 0.25, w * 0.62, h * 0.3); k.cat(w * 0.5, h * 0.2, h * 0.75)


def v_books(k, w, h):
    k.line([(w * 0.1, h * 0.1), (w * 0.9, h * 0.1)], lw=0.7, amp=0.3)
    k.books(w * 0.36, h * 0.1, h * 0.75, n=4); k.mug(w * 0.66, h * 0.11, h * 0.35)


def v_pencil(k, w, h):
    k.notepad(w * 0.4, h * 0.1, h * 0.55, letters="X  X  O"); k.pencil(w * 0.52, h * 0.12, h * 0.85, ang=22); k.spectacles(w * 0.74, h * 0.25, h * 0.5)


def v_cottage(k, w, h):
    k.snowfall(w * 0.1, h * 0.3, w * 0.9, h, n=8)
    k.ground(w * 0.05, w * 0.95, h * 0.2, depth=h * 0.2, drifts=1, ticks=False)
    k.cottage(w * 0.32, h * 0.18, h * 0.8, h * 0.62); k.pine(w * 0.22, h * 0.18, h * 0.62); k.lamppost(w * 0.8, h * 0.18, h * 0.75)


def v_cake(k, w, h):
    k.line([(w * 0.1, h * 0.1), (w * 0.9, h * 0.1)], lw=0.7, amp=0.3)
    k.cake(w * 0.4, h * 0.11, h * 0.7); k.candle(w * 0.68, h * 0.11, h * 0.6)


def v_lantern(k, w, h):
    k.line([(w * 0.1, h * 0.1), (w * 0.9, h * 0.1)], lw=0.7, amp=0.3)
    k.lantern(w * 0.36, h * 0.11, h * 0.62); k.lantern(w * 0.56, h * 0.11, h * 0.45); k.mug(w * 0.74, h * 0.11, h * 0.3)


def cover_scene(k, w, h):
    """Front-cover scene (printed white-on-dark by cover.py): Lantern Lane at night with lit lamps."""
    hz = h * 0.5
    k.snowfall(6, hz + 30, w - 6, h - 6, n=60)
    k.moon(w * 0.82, h * 0.86, 16)
    k.hills(0, w, hz + 6, amp=8, n=3)
    k.forest(w * 0.36, w * 0.64, hz + 4, 16, 30, 8)
    k.cottage(w * 0.25, hz - 2, w * 0.15, h * 0.15, door_side=0.5)
    k.cottage(w * 0.60, hz - 2, w * 0.15, h * 0.15, door_side=0.3)
    k.cottage(w * 0.0, hz - 50, w * 0.27, h * 0.28)
    k.cottage(w * 0.73, hz - 50, w * 0.27, h * 0.29, door_side=0.2)
    lane(k, w, 2, hz - 4, w * 0.12, w * 0.45, w * 0.55, w * 0.88)
    k.lamppost(w * 0.2, 14, h * 0.46)
    k.lamppost(w * 0.8, 14, h * 0.46)
    k.lamppost(w * 0.42, hz - 30, h * 0.18)
    k.lamppost(w * 0.58, hz - 30, h * 0.18)
    k.cat(w * 0.33, 10, 34)
    k.lantern(w * 0.66, 8, 26)
    k.footprints([(w * (0.5 + 0.025 * math.sin(i)), 20 + i * 15) for i in range(9)])


VIGNETTES = ["v_teapot", "v_lamp", "v_cat", "v_books", "v_pencil", "v_cottage", "v_cake", "v_lantern"]
SPECS = {
    "frontispiece": (4.7, 7.0, frontispiece, 41),
    "title": (4.7, 2.0, title, 43),
    "opener-easy": (4.7, 2.4, op_easy, 51), "opener-medium": (4.7, 2.4, op_medium, 52),
    "opener-hard": (4.7, 2.4, op_hard, 53), "opener-expert": (4.7, 2.4, op_expert, 54),
    "thanks": (3.4, 1.5, thanks, 61),
    "cover-scene": (5.4, 4.3, cover_scene, 71),
    **{n: (1.9, 0.85, globals()[n], 80 + i) for i, n in enumerate(VIGNETTES)},
}

if __name__ == "__main__":
    only = set(sys.argv[1:])
    for name, (wi, hi, fn, seed) in SPECS.items():
        if only and name not in only:
            continue
        render(os.path.join(OUT, name + ".png"), wi, hi, fn, seed=seed); print("drew", name)
