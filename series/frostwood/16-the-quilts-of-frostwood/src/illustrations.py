"""Draws the black-and-white ink illustrations for The Quilts of Frostwood -> ../illustrations/*.png
(300 DPI grayscale, pure black line art on white, same inkart house style as the other Frostwood books).
Subjects: patchwork quilts around Frostwood: on washing lines in the snow, on beds and armchairs at the
lodge, in the sewing basket, by the railway and outside the mountain huts. No people.
Deterministic: same seeds -> same images. Run from src/: python3 illustrations.py"""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inkart import render, Wt, K, lerp
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "illustrations")


# ----------------------------------------------------------------------------- local helpers
def split(rnd, x, y, w, h, depth):
    """Recursively cut a box into rectangles (a patchwork layout)."""
    if depth == 0 or (w < 6 and h < 6): return [(x, y, w, h)]
    if w >= h:
        t = rnd.choice((0.34, 0.5, 0.66)); a = w * t
        return split(rnd, x, y, a, h, depth - 1) + split(rnd, x + a, y, w - a, h, depth - 1)
    t = rnd.choice((0.34, 0.5, 0.66)); b = h * t
    return split(rnd, x, y, w, b, depth - 1) + split(rnd, x, y + b, w, h - b, depth - 1)


def patch_fill(k, x, y, w, h, kind):
    reg = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    if kind == 0: k.hatch(reg, angle=45, gap=1.5, lw=0.35, jitter=0.05)
    elif kind == 1: k.hatch(reg, angle=45, gap=1.9, lw=0.3, jitter=0.05, cross=True)
    elif kind == 2:
        r = min(w, h) * 0.16
        if r > 0.8: k.flake(x + w / 2, y + h / 2, r * 1.6, lw=0.4)
    elif kind == 3:
        step = max(2.2, min(w, h) / 3)
        yy = y + step / 2
        while yy < y + h:
            xx = x + step / 2
            while xx < x + w: k.circle(xx, yy, 0.35, lw=0.2, fill=K); xx += step
            yy += step
    elif kind == 4: k.hatch(reg, angle=0, gap=1.6, lw=0.35, jitter=0.03)
    elif kind == 5:
        k.shape(reg, lw=0, fill=K, stroke=False, amp=0)
        r = min(w, h) * 0.22
        if r > 0.8: k.star5(x + w / 2, y + h / 2, r, fill=Wt, lw=0.3)
    # kind 6: plain white


def quilt(k, x, y, w, h, seed=1, depth=4, border=True, lw=0.9):
    """A patchwork quilt as a flat rectangle with a border and stitched patches. (x, y) = bottom-left."""
    rnd = random.Random(seed)
    k.shape([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], lw=lw, fill=Wt, amp=0.15)
    b = min(w, h) * 0.07 if border else 0
    if border:
        k.hatch([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], angle=90, gap=1.3, lw=0.3, jitter=0.03)
        k.shape([(x + b, y + b), (x + w - b, y + b), (x + w - b, y + h - b), (x + b, y + h - b)], lw=0.6, fill=Wt, amp=0)
    boxes = split(rnd, x + b, y + b, w - 2 * b, h - 2 * b, depth)
    for i, (bx, by, bw, bh) in enumerate(boxes):
        patch_fill(k, bx, by, bw, bh, rnd.choice((0, 1, 2, 3, 4, 5, 6, 6)))
        k.shape([(bx, by), (bx + bw, by), (bx + bw, by + bh), (bx, by + bh)], lw=0.45, fill=None, amp=0.05)


def hung_quilt(k, x, y, w, h, seed=1):
    """A quilt hanging from a line at (x .. x+w, y), with a slight wave at the hem and two pegs."""
    quilt(k, x, y - h, w, h, seed=seed, depth=3)
    for u in (0.12, 0.88):
        px = x + w * u
        k.shape([(px - 1, y - 3.5), (px + 1, y - 3.5), (px + 1, y + 1.5), (px - 1, y + 1.5)], lw=0.5, fill=K, amp=0)


def washing_line(k, x0, x1, y, post_h, quilts):
    """Two posts, a sagging line and quilts [(u0, u1, h, seed)] hung along it."""
    for xx in (x0, x1):
        k.line([(xx, y - post_h), (xx, y + 3)], lw=1.4, amp=0.1)
        k.line([(xx - 3, y + 2), (xx + 3, y + 2)], lw=1.0, amp=0)
    pts = [(lerp(x0, x1, t), y - 3 * math.sin(math.pi * t)) for t in [i / 20 for i in range(21)]]
    k.line(pts, lw=0.6, amp=0)
    for u0, u1, h, seed in quilts:
        xm = lerp(x0, x1, (u0 + u1) / 2)
        yy = y - 3 * math.sin(math.pi * (u0 + u1) / 2)
        hung_quilt(k, lerp(x0, x1, u0), yy, lerp(x0, x1, u1) - lerp(x0, x1, u0), h, seed)


def bed(k, x, y, w, h, seed=3):
    """A wooden bed seen from the side-front with a patchwork quilt; (x, y) = bottom-left."""
    hb = h * 0.95
    k.shape([(x, y), (x + w * 0.06, y), (x + w * 0.06, y + hb), (x, y + hb)], lw=0.9, fill=Wt, amp=0)
    k.hatch([(x, y), (x + w * 0.06, y), (x + w * 0.06, y + hb), (x, y + hb)], angle=90, gap=1.2, lw=0.3)
    k.circle(x + w * 0.03, y + hb + 1.6, 2.0, lw=0.7, fill=Wt)
    k.shape([(x + w * 0.94, y), (x + w, y), (x + w, y + h * 0.6), (x + w * 0.94, y + h * 0.6)], lw=0.9, fill=Wt, amp=0)
    k.hatch([(x + w * 0.94, y), (x + w, y), (x + w, y + h * 0.6), (x + w * 0.94, y + h * 0.6)], angle=90, gap=1.2, lw=0.3)
    # mattress + pillow
    k.shape([(x + w * 0.06, y + h * 0.3), (x + w * 0.94, y + h * 0.3), (x + w * 0.94, y + h * 0.5), (x + w * 0.06, y + h * 0.5)], lw=0.8, fill=Wt, amp=0.1)
    k.shape(k.arcpts(x + w * 0.17, y + h * 0.58, w * 0.1, h * 0.09, 0, 360, 30), lw=0.8, fill=Wt, amp=0)
    quilt(k, x + w * 0.28, y + h * 0.14, w * 0.66, h * 0.42, seed=seed, depth=3)
    k.line([(x + w * 0.28, y + h * 0.5), (x + w * 0.94, y + h * 0.5)], lw=0.5, amp=0.1)
    for u in (0.08, 0.92):
        k.line([(x + w * u, y), (x + w * u, y - 3)], lw=1.2, amp=0)


def basket(k, x, y, w):
    """A sewing basket with fabric rolls, a pincushion and a spool; (x, y) = centre bottom."""
    h = w * 0.42
    body = [(x - w / 2, y + h), (x - w * 0.42, y), (x + w * 0.42, y), (x + w / 2, y + h)]
    # fabric rolls peeking out
    for i, (u, hh, kind) in enumerate([(-0.3, 0.3, 0), (-0.08, 0.38, 1), (0.16, 0.32, 4), (0.34, 0.24, 3)]):
        cx = x + u * w; r = w * 0.1
        k.shape([(cx - r, y + h * 0.6), (cx + r, y + h * 0.6), (cx + r, y + h + w * hh), (cx - r, y + h + w * hh)], lw=0.7, fill=Wt, amp=0.1)
        patch_fill(k, cx - r, y + h * 0.6, 2 * r, h * 0.4 + w * hh, kind)
        k.shape(k.arcpts(cx, y + h + w * hh, r, r * 0.35, 0, 360, 20), lw=0.6, fill=Wt, amp=0)
        k.circle(cx, y + h + w * hh, r * 0.12, lw=0.3, fill=K)
    k.shape(body, lw=1.0, fill=Wt, amp=0.1)
    for i in range(1, 9):
        xx = lerp(x - w * 0.46, x + w * 0.46, i / 9); k.line([(xx, y + 1), (xx + w * 0.02, y + h - 1)], lw=0.35, amp=0.1)
    for j in range(1, 4):
        yy = y + h * j / 4; k.line([(x - w * (0.42 + 0.08 * j / 4), yy), (x + w * (0.42 + 0.08 * j / 4), yy)], lw=0.35, amp=0.1)
    k.line([(x - w / 2 - 1, y + h), (x + w / 2 + 1, y + h)], lw=1.2, amp=0)


def spool(k, x, y, h):
    w = h * 0.7
    k.shape([(x - w * 0.35, y + h * 0.12), (x + w * 0.35, y + h * 0.12), (x + w * 0.35, y + h * 0.88), (x - w * 0.35, y + h * 0.88)], lw=0.6, fill=Wt, amp=0)
    k.hatch([(x - w * 0.35, y + h * 0.12), (x + w * 0.35, y + h * 0.12), (x + w * 0.35, y + h * 0.88), (x - w * 0.35, y + h * 0.88)], angle=8, gap=0.9, lw=0.3, jitter=0.02)
    for yy in (y, y + h * 0.88):
        k.shape([(x - w / 2, yy), (x + w / 2, yy), (x + w / 2, yy + h * 0.12), (x - w / 2, yy + h * 0.12)], lw=0.7, fill=Wt, amp=0)


def scissors(k, x, y, L):
    for s in (-1, 1):
        k.line([(x, y), (x + L, y + s * L * 0.08)], lw=1.0, amp=0)
        k.circle(x - L * 0.2, y - s * L * 0.14, L * 0.13, lw=0.9, fill=Wt)
    k.circle(x, y, 0.8, lw=0.3, fill=K)


def table(k, x, y, w, h):
    k.shape([(x, y + h), (x + w, y + h), (x + w, y + h + 3), (x, y + h + 3)], lw=0.9, fill=Wt, amp=0)
    for u in (0.06, 0.94):
        k.line([(x + w * u, y), (x + w * u, y + h)], lw=1.3, amp=0)


def hoop(k, x, y, r, seed=5):
    """An embroidery / quilting hoop holding a patch of quilt."""
    c = k.c
    c.saveState(); p = c.beginPath(); p.circle(x, y, r); c.clipPath(p, stroke=0, fill=0)
    quilt(k, x - r, y - r, 2 * r, 2 * r, seed=seed, depth=3, border=False, lw=0.5)
    c.restoreState()
    k.circle(x, y, r, lw=1.3, fill=None); k.circle(x, y, r + 2, lw=0.7, fill=None)
    k.shape([(x - 2, y + r + 1), (x + 2, y + r + 1), (x + 2, y + r + 5), (x - 2, y + r + 5)], lw=0.6, fill=Wt, amp=0)


# ----------------------------------------------------------------------------- scenes
def frontispiece(k, w, h):
    """The lodge sitting room on a snowy evening: fire, armchair with a quilt, quilts on the wall and a rack, cat on the rug."""
    m = 9; k.frame(m, m, w - m, h - m)
    k.clip_rect(m + 4, m + 4, w - m - 4, h - m - 4)
    fl = h * 0.2
    # floorboards
    for i in range(9):
        yy = m + 4 + (fl - m - 4) * i / 9; k.line([(m + 4, yy), (w - m - 4, yy)], lw=0.3, amp=0.2)
    k.line([(m + 4, fl), (w - m - 4, fl)], lw=1.0, amp=0)
    # wainscot
    k.line([(m + 4, fl + h * 0.12), (w - m - 4, fl + h * 0.12)], lw=0.6, amp=0)
    for i in range(1, 16):
        xx = lerp(m + 4, w - m - 4, i / 16); k.line([(xx, fl), (xx, fl + h * 0.12)], lw=0.3, amp=0)
    # window with snow
    k.window_snow(w * 0.6, h * 0.52, w * 0.3, h * 0.3)
    # big quilt hung on the wall
    k.line([(w * 0.08, h * 0.88), (w * 0.52, h * 0.88)], lw=1.4, amp=0)
    for xx in (w * 0.08, w * 0.52): k.circle(xx, h * 0.88, 2.2, lw=0.7, fill=K)
    quilt(k, w * 0.1, h * 0.54, w * 0.4, h * 0.33, seed=16, depth=5)
    # fireplace
    k.fireplace(w * 0.58, fl, w * 0.36, h * 0.27, fire=True, stockings=0)
    # armchair with quilt draped over the arm
    k.armchair(w * 0.3, fl, w * 0.3, facing=1)
    qx, qy = w * 0.13, fl + w * 0.3 * 0.3
    k.shape([(qx, qy - 22), (qx + 16, qy - 24), (qx + 18, qy + 12), (qx + 2, qy + 14)], lw=0.8, fill=Wt, amp=0.2)
    patch_fill(k, qx + 2, qy - 20, 7, 10, 1); patch_fill(k, qx + 9, qy - 8, 7, 10, 5); patch_fill(k, qx + 2, qy + 2, 7, 9, 0)
    k.line([(qx + 9, qy - 23), (qx + 10, qy + 13)], lw=0.4, amp=0.1); k.line([(qx + 1, qy - 9), (qx + 17, qy - 7)], lw=0.4, amp=0.1)
    # rug and cat
    k.rug(w * 0.55, fl - h * 0.06, w * 0.5, h * 0.07)
    k.cat(w * 0.6, fl - h * 0.075, w * 0.14)
    # quilt rack with folded quilts and a basket
    rx = w * 0.04 + m
    basket(k, w * 0.86, m + 10, w * 0.16)
    for i in range(3):
        qy = fl + 4 + i * 9
        k.shape([(rx + 4, qy), (rx + 40, qy), (rx + 40, qy + 8), (rx + 4, qy + 8)], lw=0.7, fill=Wt, amp=0.1)
        patch_fill(k, rx + 4, qy, 36, 8, (0, 3, 4)[i])
    k.side_table(w * 0.5, fl, w * 0.08)
    k.mug(w * 0.5, fl + w * 0.08 * 0.95, 7)
    k.unclip()


def title(k, w, h):
    """Three quilts on a washing line between two posts in the snow, pines and stars behind."""
    k.snowfall(w * 0.04, h * 0.5, w * 0.96, h, n=30); k.stars(w * 0.06, h * 0.75, w * 0.94, h - 4, n=12); k.moon(w * 0.9, h * 0.86, 8)
    k.forest(0, w, h * 0.2, 14, 30, 14)
    k.ground(0, w, h * 0.2, depth=h * 0.2, drifts=1, ticks=False)
    washing_line(k, w * 0.12, w * 0.88, h * 0.7, h * 0.52, [(0.04, 0.3, h * 0.38, 2), (0.36, 0.64, h * 0.44, 7), (0.7, 0.96, h * 0.36, 9)])
    k.footprints([(w * (0.2 + 0.07 * i), h * (0.07 + 0.012 * (i % 2))) for i in range(9)])


def op_village(k, w, h):
    """Part One: the sewing circle table in the village hall: a quilt spread out, a basket, scissors, spools, a window of snow."""
    k.window_snow(w * 0.06, h * 0.5, w * 0.2, h * 0.42)
    k.window_snow(w * 0.74, h * 0.5, w * 0.2, h * 0.42)
    k.line([(0, h * 0.18), (w, h * 0.18)], lw=0.9, amp=0)
    table(k, w * 0.28, h * 0.02, w * 0.44, h * 0.36)
    quilt(k, w * 0.3, h * 0.41, w * 0.4, h * 0.42, seed=21, depth=4)
    k.shape([(w * 0.3, h * 0.41), (w * 0.7, h * 0.41), (w * 0.69, h * 0.3), (w * 0.31, h * 0.3)], lw=0.8, fill=Wt, amp=0.2)
    patch_fill(k, w * 0.32, h * 0.31, w * 0.36, h * 0.09, 0)
    basket(k, w * 0.15, h * 0.02, w * 0.18)
    spool(k, w * 0.78, h * 0.02, h * 0.12); spool(k, w * 0.83, h * 0.02, h * 0.1)
    scissors(k, w * 0.88, h * 0.08, h * 0.12)
    k.flake(w * 0.5, h * 0.92, 4)


def op_lodge(k, w, h):
    """Part Two: a lodge guest room: bed with a quilt, window of falling snow, a lamp and a folded quilt on a chest."""
    k.line([(0, h * 0.08), (w, h * 0.08)], lw=0.9, amp=0)
    k.window_snow(w * 0.42, h * 0.46, w * 0.2, h * 0.44)
    bed(k, w * 0.2, h * 0.1, w * 0.56, h * 0.42, seed=31)
    k.floor_lamp(w * 0.88, h * 0.08, h * 0.8)
    k.shape([(w * 0.05, h * 0.08), (w * 0.17, h * 0.08), (w * 0.17, h * 0.26), (w * 0.05, h * 0.26)], lw=0.9, fill=Wt, amp=0.1)
    for i in range(3):
        y0 = h * 0.26 + i * h * 0.05
        k.shape([(w * 0.055, y0), (w * 0.165, y0), (w * 0.165, y0 + h * 0.05), (w * 0.055, y0 + h * 0.05)], lw=0.6, fill=Wt, amp=0.1)
        patch_fill(k, w * 0.055, y0, w * 0.11, h * 0.05, (1, 3, 4)[i])
    quilt(k, w * 0.08, h * 0.62, w * 0.24, h * 0.28, seed=33, depth=3)


def op_station(k, w, h):
    """Part Three: the Frostwood Express at the halt, with sleeper-berth blankets airing on a line by the platform."""
    k.snowfall(0, h * 0.5, w, h, n=36); k.stars(6, h * 0.8, w - 6, h - 4, n=10)
    k.mountains(0, w, h * 0.45, [(w * 0.2, h * 0.72), (w * 0.6, h * 0.8), (w * 0.9, h * 0.7)])
    k.ground(0, w, h * 0.45, depth=h * 0.45, drifts=0, ticks=False)
    k.rails(0, w, h * 0.12)
    k.carriage(w * 0.02, h * 0.14, w * 0.28, n_win=5)
    k.locomotive(w * 0.31, h * 0.14, w * 0.3, facing=1, smoke=True)
    washing_line(k, w * 0.68, w * 0.97, h * 0.62, h * 0.32, [(0.05, 0.47, h * 0.24, 41), (0.53, 0.95, h * 0.28, 42)])
    k.signal(w * 0.66, h * 0.12, h * 0.4)


def op_hut(k, w, h):
    """Part Four: a mountain hut under the peaks, heirloom quilts airing on a line beside it."""
    k.snowfall(0, h * 0.45, w, h, n=40); k.stars(6, h * 0.78, w - 6, h - 4, n=14); k.moon(w * 0.86, h * 0.86, 9)
    k.mountains(0, w, h * 0.42, [(w * 0.15, h * 0.85), (w * 0.5, h * 0.72), (w * 0.8, h * 0.9)])
    k.forest(0, w * 0.25, h * 0.4, 14, 30, 7); k.forest(w * 0.8, w, h * 0.4, 14, 30, 5)
    k.ground(0, w, h * 0.4, depth=h * 0.4, drifts=1, ticks=False)
    k.cabin(w * 0.08, h * 0.12, w * 0.3, h * 0.5)
    washing_line(k, w * 0.46, w * 0.92, h * 0.56, h * 0.42, [(0.04, 0.32, h * 0.28, 51), (0.36, 0.64, h * 0.32, 52), (0.68, 0.96, h * 0.26, 53)])
    k.footprints([(w * (0.4 + 0.05 * i), h * (0.05 + 0.01 * (i % 2))) for i in range(8)])


def v_line(k, w, h):
    k.ground(0, w, h * 0.14, depth=h * 0.14, drifts=0, ticks=False)
    washing_line(k, w * 0.2, w * 0.8, h * 0.82, h * 0.68, [(0.06, 0.46, h * 0.45, 61), (0.54, 0.94, h * 0.5, 62)])
    k.pine(w * 0.1, h * 0.12, h * 0.6); k.pine(w * 0.9, h * 0.12, h * 0.5)


def v_basket(k, w, h):
    basket(k, w * 0.42, h * 0.04, h * 0.95)
    spool(k, w * 0.72, h * 0.04, h * 0.28); scissors(k, w * 0.2, h * 0.1, h * 0.25)
    k.line([(w * 0.08, h * 0.04), (w * 0.92, h * 0.04)], lw=0.8, amp=0)


def v_chair(k, w, h):
    k.line([(w * 0.1, h * 0.04), (w * 0.9, h * 0.04)], lw=0.8, amp=0)
    k.armchair(w * 0.5, h * 0.04, h * 0.75, facing=1)
    quilt(k, w * 0.38, h * 0.18, h * 0.38, h * 0.36, seed=71, depth=3)
    k.side_table(w * 0.8, h * 0.04, h * 0.35); k.mug(w * 0.8, h * 0.04 + h * 0.35 * 0.95, h * 0.16)


def v_bed(k, w, h):
    k.line([(w * 0.1, h * 0.06), (w * 0.9, h * 0.06)], lw=0.8, amp=0)
    bed(k, w * 0.2, h * 0.1, w * 0.6, h * 0.62, seed=81)


def v_mug(k, w, h):
    k.line([(w * 0.15, h * 0.06), (w * 0.85, h * 0.06)], lw=0.8, amp=0)
    quilt(k, w * 0.2, h * 0.06, w * 0.32, h * 0.2, seed=91, depth=2)
    quilt(k, w * 0.22, h * 0.26, w * 0.28, h * 0.18, seed=92, depth=2)
    k.mug(w * 0.66, h * 0.06, h * 0.42)


def v_frame(k, w, h):
    hoop(k, w * 0.5, h * 0.5, h * 0.4, seed=101)
    spool(k, w * 0.22, h * 0.06, h * 0.32); scissors(k, w * 0.72, h * 0.12, h * 0.26)


def v_moon(k, w, h):
    k.stars(4, h * 0.4, w - 4, h - 4, n=12); k.moon(w * 0.8, h * 0.74, h * 0.13)
    k.ground(0, w, h * 0.16, depth=h * 0.16, drifts=0, ticks=False)
    washing_line(k, w * 0.25, w * 0.62, h * 0.7, h * 0.55, [(0.1, 0.9, h * 0.38, 111)])
    k.pine(w * 0.12, h * 0.14, h * 0.6)


def thanks(k, w, h):
    k.line([(w * 0.05, h * 0.1), (w * 0.95, h * 0.1)], lw=0.8, amp=0)
    k.armchair(w * 0.3, h * 0.1, h * 0.72, facing=1)
    quilt(k, w * 0.2, h * 0.24, h * 0.36, h * 0.34, seed=121, depth=3)
    k.side_table(w * 0.52, h * 0.1, h * 0.3); k.mug(w * 0.52, h * 0.1 + h * 0.3 * 0.95, h * 0.14)
    basket(k, w * 0.78, h * 0.1, h * 0.5)
    k.stars(w * 0.6, h * 0.75, w * 0.95, h - 3, n=6)


VIGNETTES = ["v_line", "v_basket", "v_chair", "v_bed", "v_mug", "v_frame"]
SPECS = {  # name: (width in, height in, function, seed)
    "frontispiece": (4.7, 7.0, frontispiece, 61),
    "title": (4.7, 2.5, title, 3),
    "opener-easy": (4.7, 2.4, op_village, 11), "opener-medium": (4.7, 2.4, op_lodge, 12),
    "opener-hard": (4.7, 2.4, op_station, 13), "opener-expert": (4.7, 2.4, op_hut, 14),
    "thanks": (3.4, 1.5, thanks, 21),
    "v_moon": (1.9, 0.85, v_moon, 79),
    **{n: (1.9, 0.85, globals()[n], 80 + i) for i, n in enumerate(VIGNETTES)},
}

if __name__ == "__main__":
    only = set(sys.argv[1:])
    os.makedirs(OUT, exist_ok=True)
    for name, (wi, hi, fn, seed) in SPECS.items():
        if only and name not in only: continue
        render(os.path.join(OUT, name + ".png"), wi, hi, fn, seed=seed); print("drew", name)
