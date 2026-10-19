"""Draws the black-and-white ink illustrations for Window Seat Codewords -> ../illustrations/*.png
(300 DPI grayscale, pure black line art on white). Deterministic. Run from src/: python3 illustrations.py [names]"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inkart import render, Wt, K, lerp
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "illustrations")


def plant(k, x, y, w, kind=0):
    """A potted plant: kind 0 trailing ivy, kind 1 upright leaves, kind 2 little cactus."""
    h = w * 0.75
    k.shape([(x - w * 0.36, y), (x + w * 0.36, y), (x + w * 0.46, y + h), (x - w * 0.46, y + h)], lw=0.9, fill=Wt, amp=0.15)
    k.hatch([(x + w * 0.1, y), (x + w * 0.36, y), (x + w * 0.46, y + h), (x + w * 0.16, y + h)], angle=75, gap=1.5, lw=0.35)
    k.line([(x - w * 0.48, y + h), (x + w * 0.48, y + h)], lw=1.1, amp=0)
    if kind == 0:
        for i in range(9):
            a = math.radians(25 + i * 16); L = w * (0.55 + 0.2 * ((i * 7) % 3) / 2)
            tx, ty = x + L * math.cos(a), y + h + L * math.sin(a) * 0.9
            k.line([(x, y + h), (tx, ty)], lw=0.5, amp=0.1)
            ang = math.degrees(a)
            q = k.arcpts(tx, ty, w * 0.13, w * 0.07, 0, 360, 14)
            q = [(tx + (px - tx) * math.cos(a) - (py - ty) * math.sin(a), ty + (px - tx) * math.sin(a) + (py - ty) * math.cos(a)) for px, py in q]
            k.shape(q, lw=0.6, fill=K if i % 3 == 1 else Wt, amp=0)
            if i % 3 != 1: k.line([(tx - w * 0.1 * math.cos(a), ty - w * 0.1 * math.sin(a)), (tx + w * 0.1 * math.cos(a), ty + w * 0.1 * math.sin(a))], lw=0.3, amp=0)
    elif kind == 1:
        for i in range(7):
            a = math.radians(40 + i * 16.5); L = w * (0.75 + 0.25 * math.sin(i * 1.3))
            tx, ty = x + L * math.cos(a), y + h + L * math.sin(a)
            mx, my = x + L * 0.5 * math.cos(a), y + h + L * 0.5 * math.sin(a)
            nx, ny = -math.sin(a) * w * 0.09, math.cos(a) * w * 0.09
            k.shape([(x, y + h), (mx + nx, my + ny), (tx, ty), (mx - nx, my - ny)], lw=0.6, fill=K if i % 2 else Wt, amp=0)
    else:
        bw = w * 0.32
        k.shape(k.arcpts(x, y + h, bw / 2, w * 0.6, 0, 180, 24), lw=0.8, fill=Wt, amp=0)
        for i in range(-2, 3): k.line([(x + i * bw * 0.18, y + h), (x + i * bw * 0.16, y + h + w * 0.55 * (1 - abs(i) * 0.15))], lw=0.35, amp=0)
        k.circle(x, y + h + w * 0.62, 2.2, lw=0.5, fill=K)


def code_sheet(k, x, y, cell, n=5):
    """A little codeword grid with tiny numbers and a few letters filled in."""
    blacks = {(1, 1), (1, 3), (3, 1), (3, 3)}
    nums = [[3, 14, 7, 22, 9], [5, 0, 11, 0, 18], [21, 8, 3, 19, 2], [6, 0, 25, 0, 14], [12, 3, 16, 8, 4]]
    letters = {3: "E", 8: "A", 14: "T"}
    k.rect(x - cell * 0.4, y - cell * 0.4, cell * (n + 0.8), cell * (n + 0.8), lw=0.6)
    for r in range(n):
        for c in range(n):
            cx, cy = x + c * cell, y + (n - 1 - r) * cell
            k.rect(cx, cy, cell, cell, lw=0.5, fill=K if (r, c) in blacks else Wt)
            v = nums[r][c]
            if v:
                k.text(cx + 0.6, cy + cell * 0.72, str(v), size=cell * 0.26, font="Ink-Plex", align="l")
                if v in letters:
                    k.text(cx + cell / 2, cy + cell * 0.14, letters[v], size=cell * 0.56, font="Ink-Plex")


def outside(k, x, y, w, h, weather):
    c = k.c; c.saveState(); p = c.beginPath(); p.rect(x, y, w, h); c.clipPath(p, stroke=0, fill=0)
    if weather == "sun":
        k.hills(x, x + w, y + h * 0.18, amp=6, n=3)
        for i, tx in enumerate((0.18, 0.5, 0.8)):
            k.pine(x + w * tx, y + h * 0.15, h * (0.32 + 0.1 * (i % 2)), snow=False)
        from math import cos, sin, pi
        sx, sy, r = x + w * 0.72, y + h * 0.74, h * 0.09
        k.circle(sx, sy, r, lw=0.9, fill=Wt)
        for i in range(12):
            a = 2 * pi * i / 12
            k.line([(sx + r * 1.35 * cos(a), sy + r * 1.35 * sin(a)), (sx + r * 1.8 * cos(a), sy + r * 1.8 * sin(a))], lw=0.7, amp=0)
        for bx, by in ((0.3, 0.7), (0.4, 0.78), (0.24, 0.8)):
            s_ = h * 0.025; X, Y = x + w * bx, y + h * by
            k.line([(X - s_, Y + s_ * 0.3)] + k.arcpts(X - s_ / 2, Y, s_ / 2, s_ * 0.35, 160, 20, 6)[1:] + k.arcpts(X + s_ / 2, Y, s_ / 2, s_ * 0.35, 160, 20, 6), lw=0.6, amp=0)
    elif weather == "rain":
        k.hills(x, x + w, y + h * 0.16, amp=5, n=2)
        for i, tx in enumerate((0.14, 0.42, 0.7, 0.92)):
            k.pine(x + w * tx, y + h * 0.13, h * (0.26 + 0.08 * (i % 2)), snow=False)
        for i in range(int(w * h / 90)):
            X = x + k.r.uniform(0, w); Y = y + k.r.uniform(0, h * 0.8); L = k.r.uniform(4, 8)
            k.line([(X, Y), (X - L * 0.25, Y - L)], lw=0.4, amp=0)
        for i in range(int(w * h / 500)):
            X = x + k.r.uniform(3, w - 3); Y = y + k.r.uniform(3, h - 3)
            k.shape([(X, Y + 2.0)] + k.arcpts(X, Y, 1.2, 1.3, 0, -180, 8), lw=0.4, fill=Wt, amp=0)
    else:  # snow at night
        k.moon(x + w * 0.74, y + h * 0.76, h * 0.07)
        k.stars(x + 4, y + h * 0.55, x + w - 4, y + h - 4, n=int(w * h / 900) + 4, rmax=2.0)
        k.snowfall(x, y, x + w, y + h, n=int(w * h / 70))
        for i, tx in enumerate((0.15, 0.4, 0.62, 0.88)):
            k.pine(x + w * tx, y + h * 0.1, h * (0.3 + 0.1 * (i % 2)), snow=True)
        k.line([(x, y + h * 0.1), (x + w, y + h * 0.13)], lw=0.6, amp=0.3)
    c.restoreState()


def window_seat(k, x, y, w, h, weather="rain", cat=True, props=True):
    """An alcove window seat: window with panes over a cushioned bench, curtains, the view outside."""
    seat_h = h * 0.26
    wy = y + seat_h + h * 0.06
    wh = h * 0.6
    wx, ww = x + w * 0.1, w * 0.8
    # alcove wall
    k.shape([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], lw=1.1, fill=Wt, amp=0.1)
    k.shape([(x + w * 0.04, y + seat_h), (x + w * 0.96, y + seat_h), (x + w * 0.96, y + h * 0.95), (x + w * 0.04, y + h * 0.95)], lw=0.7, fill=Wt, amp=0.1)
    k.hatch([(x + w * 0.04, y + seat_h), (x + w * 0.1, wy), (x + w * 0.1, wy + wh), (x + w * 0.04, y + h * 0.95)], angle=90, gap=1.6, lw=0.35)
    k.hatch([(x + w * 0.96, y + seat_h), (x + w * 0.9, wy), (x + w * 0.9, wy + wh), (x + w * 0.96, y + h * 0.95)], angle=90, gap=2.4, lw=0.3)
    # window
    k.rect(wx - 3, wy - 3, ww + 6, wh + 6, lw=1.0)
    k.rect(wx, wy, ww, wh, lw=0.8)
    outside(k, wx, wy, ww, wh, weather)
    k.c.setStrokeColor(K); k.c.setLineWidth(1.4)
    for i in (1, 2): k.c.line(wx + ww * i / 3, wy, wx + ww * i / 3, wy + wh)
    k.c.line(wx, wy + wh * 0.6, wx + ww, wy + wh * 0.6)
    # curtain rod and tied-back curtains
    k.line([(x + w * 0.02, wy + wh + 12), (x + w * 0.98, wy + wh + 12)], lw=1.4, amp=0)
    for sx in (-1, 1):
        ex = wx if sx < 0 else wx + ww
        cur = [(ex - sx * ww * 0.06, wy + wh + 12), (ex + sx * ww * 0.13, wy + wh + 12), (ex + sx * ww * 0.02, wy + wh * 0.45),
               (ex + sx * ww * 0.08, wy - 2), (ex - sx * ww * 0.06, wy - 2)]
        k.shape(cur, lw=0.8, fill=Wt, amp=0.2)
        for j in range(3):
            u = (j + 1) / 4
            k.line([(ex - sx * ww * 0.06 + sx * ww * 0.18 * u, wy + wh + 11), (ex - sx * ww * 0.03 + sx * ww * 0.05 * u, wy + wh * 0.45), (ex - sx * ww * 0.05 + sx * ww * 0.12 * u, wy - 1)], lw=0.35, amp=0.2)
        k.line([(ex - sx * ww * 0.06, wy + wh * 0.45), (ex + sx * ww * 0.03, wy + wh * 0.47)], lw=1.2, amp=0)
    # bench with a long cushion and drawers below
    k.shape([(x + w * 0.02, y), (x + w * 0.98, y), (x + w * 0.98, y + seat_h * 0.78), (x + w * 0.02, y + seat_h * 0.78)], lw=1.0, fill=Wt, amp=0.1)
    for i in range(3):
        dx0 = x + w * (0.06 + 0.31 * i); dx1 = dx0 + w * 0.27
        k.rect(dx0, y + seat_h * 0.12, dx1 - dx0, seat_h * 0.5, lw=0.6)
        k.circle((dx0 + dx1) / 2, y + seat_h * 0.4, 1.3, lw=0.5, fill=K)
    cush = [(x + w * 0.03, y + seat_h * 0.78), (x + w * 0.97, y + seat_h * 0.78), (x + w * 0.965, y + seat_h * 1.05), (x + w * 0.035, y + seat_h * 1.05)]
    k.shape(cush, lw=0.9, fill=Wt, amp=0.3)
    k.hatch([(x + w * 0.03, y + seat_h * 0.78), (x + w * 0.97, y + seat_h * 0.78), (x + w * 0.97, y + seat_h * 0.86), (x + w * 0.03, y + seat_h * 0.86)], angle=0, gap=1.2, lw=0.3)
    top = y + seat_h * 1.05
    # pillows
    for px, ang in ((0.1, 1), (0.88, -1)):
        X = x + w * px; ph = h * 0.13
        pts = [(X - ph * 0.5, top), (X + ph * 0.5, top), (X + ph * 0.45 + ang * 2, top + ph), (X - ph * 0.45 + ang * 2, top + ph)]
        k.shape(pts, lw=0.8, fill=Wt, amp=0.4)
        k.hatch(pts, angle=45 * ang, gap=2.0, lw=0.3, cross=True)
        k.shape(pts, lw=0.8, fill=None, amp=0.4)
    if cat: k.cat(x + w * 0.66, top, w * 0.2)
    if props:
        k.books(x + w * 0.27, top, w * 0.15, n=3)
        k.mug(x + w * 0.27, top + w * 0.15 * 0.16 * 3, h * 0.07)
        code_sheet(k, x + w * 0.38, top + 2, w * 0.026)
        k.pencil(x + w * 0.5, top + 1.5, w * 0.11, ang=12)
    return top


# ----------------------------------------------------------------------------- pieces
def frontispiece(k, w, h):
    floor = h * 0.1
    k.line([(0, floor), (w, floor)], lw=0.9, amp=0.3)
    for i in range(9):
        k.line([(w * i / 8 - 10, floor - 1), (w * i / 8 - 30, 0)], lw=0.35, amp=0.2)
    window_seat(k, w * 0.05, floor, w * 0.9, h * 0.8, "rain")
    k.rug(w * 0.5, floor * 0.5, w * 0.7, floor * 0.75)


def title(k, w, h):
    k.line([(w * 0.08, h * 0.1), (w * 0.92, h * 0.1)], lw=0.8, amp=0.3)
    code_sheet(k, w * 0.3, h * 0.14, h * 0.11)
    k.pencil(w * 0.5, h * 0.12, h * 0.75, ang=25)
    k.mug(w * 0.72, h * 0.11, h * 0.4)
    k.cat(w * 0.14, h * 0.1, h * 0.75)


def op_easy(k, w, h):
    """Morning light: a sunny window, a teapot and cup and a plant on the sill."""
    sill = h * 0.18
    k.rect(w * 0.28, sill + 4, w * 0.44, h * 0.74, lw=1.0)
    outside(k, w * 0.28 + 3, sill + 7, w * 0.44 - 6, h * 0.74 - 6, "sun")
    k.c.setLineWidth(1.3); k.c.line(w * 0.5, sill + 7, w * 0.5, sill + h * 0.74 + 1); k.c.line(w * 0.28 + 3, sill + h * 0.45, w * 0.72 - 3, sill + h * 0.45)
    k.line([(w * 0.04, sill), (w * 0.96, sill)], lw=1.1, amp=0.2); k.line([(w * 0.06, sill - 4), (w * 0.94, sill - 4)], lw=0.6, amp=0.2)
    k.teapot(w * 0.13, sill, h * 0.42); k.cup(w * 0.22, sill, h * 0.2)
    plant(k, w * 0.82, sill, h * 0.3, kind=1); plant(k, w * 0.92, sill, h * 0.18, kind=2)


def op_medium(k, w, h):
    """Rainy afternoon: the window seat with the cat asleep and rain on the glass."""
    window_seat(k, w * 0.22, h * 0.04, w * 0.56, h * 0.94, "rain", props=False)
    k.books(w * 0.1, h * 0.04, w * 0.12, n=4)
    plant(k, w * 0.9, h * 0.04, h * 0.28, kind=0)


def op_hard(k, w, h):
    """Snowy evening: a frosty night window, a candle, cocoa and the codeword sheet."""
    sill = h * 0.18
    k.rect(w * 0.3, sill + 4, w * 0.4, h * 0.74, lw=1.0)
    outside(k, w * 0.3 + 3, sill + 7, w * 0.4 - 6, h * 0.74 - 6, "snow")
    k.c.setLineWidth(1.3); k.c.line(w * 0.5, sill + 7, w * 0.5, sill + h * 0.74 + 1); k.c.line(w * 0.3 + 3, sill + h * 0.45, w * 0.7 - 3, sill + h * 0.45)
    k.line([(w * 0.04, sill), (w * 0.96, sill)], lw=1.1, amp=0.2); k.line([(w * 0.06, sill - 4), (w * 0.94, sill - 4)], lw=0.6, amp=0.2)
    k.candle(w * 0.2, sill, h * 0.5); k.mug(w * 0.1, sill, h * 0.22)
    code_sheet(k, w * 0.76, sill + 3, h * 0.055); k.pencil(w * 0.88, sill + 2, h * 0.3, ang=15)


def op_solutions(k, w, h):
    k.line([(w * 0.1, h * 0.12), (w * 0.9, h * 0.12)], lw=0.8, amp=0.3)
    k.key(w * 0.3, h * 0.35, w * 0.32)
    k.notepad(w * 0.68, h * 0.13, h * 0.6, letters="A B C D")
    k.spectacles(w * 0.5, h * 0.16, w * 0.13)


def thanks(k, w, h):
    window_seat(k, w * 0.2, h * 0.04, w * 0.6, h * 0.94, "snow", props=False)


def v_mug(k, w, h):
    k.line([(w * 0.15, h * 0.08), (w * 0.85, h * 0.08)], lw=0.7, amp=0.3); k.mug(w * 0.4, h * 0.08, h * 0.5); k.books(w * 0.66, h * 0.08, h * 0.7, n=2)


def v_cat(k, w, h):
    k.line([(w * 0.12, h * 0.08), (w * 0.88, h * 0.08)], lw=0.7, amp=0.3); k.cat(w * 0.5, h * 0.08, h * 0.95)


def v_key(k, w, h):
    k.key(w * 0.32, h * 0.45, w * 0.38)


def v_sheet(k, w, h):
    code_sheet(k, w * 0.32, h * 0.12, h * 0.14); k.pencil(w * 0.6, h * 0.1, h * 0.85, ang=22)


def v_tea(k, w, h):
    k.line([(w * 0.12, h * 0.08), (w * 0.88, h * 0.08)], lw=0.7, amp=0.3); k.teapot(w * 0.4, h * 0.09, h * 0.9); k.cup(w * 0.66, h * 0.09, h * 0.38)


def v_plant(k, w, h):
    k.line([(w * 0.12, h * 0.08), (w * 0.88, h * 0.08)], lw=0.7, amp=0.3); plant(k, w * 0.36, h * 0.08, h * 0.45, 1); plant(k, w * 0.62, h * 0.08, h * 0.5, 0)


def v_candle(k, w, h):
    k.line([(w * 0.12, h * 0.08), (w * 0.88, h * 0.08)], lw=0.7, amp=0.3); k.candle(w * 0.42, h * 0.08, h * 0.85); k.spectacles(w * 0.62, h * 0.14, h * 0.6)


def cover_scene(k, w, h):
    floor = h * 0.06
    window_seat(k, w * 0.04, floor, w * 0.92, h * 0.9, "snow")


VIGNETTES = ["v_mug", "v_cat", "v_key", "v_sheet", "v_tea", "v_plant", "v_candle"]
SPECS = {
    "frontispiece": (4.7, 6.6, frontispiece, 41),
    "title": (4.0, 1.8, title, 43),
    "opener-easy": (4.7, 2.6, op_easy, 51), "opener-medium": (4.7, 2.6, op_medium, 52),
    "opener-hard": (4.7, 2.6, op_hard, 53), "opener-solutions": (4.0, 1.8, op_solutions, 54),
    "thanks": (3.4, 2.2, thanks, 61),
    "cover-scene": (5.0, 4.4, cover_scene, 71),
    **{n: (1.9, 0.8, globals()[n], 80 + i) for i, n in enumerate(VIGNETTES)},
}

if __name__ == "__main__":
    only = set(sys.argv[1:])
    for name, (wi, hi, fn, seed) in SPECS.items():
        if only and name not in only: continue
        render(os.path.join(OUT, name + ".png"), wi, hi, fn, seed=seed); print("drew", name)
