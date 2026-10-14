"""Draws the black-and-white ink illustrations for Porch Swing Crosswords -> ../illustrations/*.png
(300 DPI grayscale, pure black line art on white). Deterministic: same seeds -> same images.
Run from src/: python3 illustrations.py   (optional args: names of the images to redraw)"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inkart import render, Wt, K, lerp
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "illustrations")


# ----------------------------------------------------------------------------- props
def tree(k, x, y, h, lw=0.8):
    """A round leafy tree: trunk and a scalloped crown."""
    k.shape([(x - h * 0.04, y), (x + h * 0.04, y), (x + h * 0.03, y + h * 0.45), (x - h * 0.03, y + h * 0.45)], lw=lw, fill=Wt, amp=0.2)
    r = h * 0.3; cy = y + h * 0.66
    pts = []
    for i in range(15):
        a = 2 * math.pi * i / 14
        rr = r * (1 + 0.1 * math.sin(i * 2.7))
        pts += k.arcpts(x + rr * math.cos(a) * 0.82, cy + rr * math.sin(a) * 0.82, r * 0.28, r * 0.28, math.degrees(a) - 80, math.degrees(a) + 80, 6)
    q = k.shape(pts, lw=lw, fill=Wt, amp=0.15)
    k.hatch([(x + r * 0.15, cy - r), (x + r * 1.1, cy - r * 0.3), (x + r * 1.0, cy + r * 0.4), (x + r * 0.35, cy - r * 0.2)], angle=-50, gap=1.8, lw=0.35)


def flower(k, x, y, r, kind=0):
    if kind == 0:      # daisy
        for i in range(8):
            a = 2 * math.pi * i / 8
            k.shape(k.arcpts(x + r * 0.62 * math.cos(a), y + r * 0.62 * math.sin(a), r * 0.42, r * 0.22, 0, 360, 12), lw=0.5, fill=Wt, amp=0)
        k.circle(x, y, r * 0.3, lw=0.5, fill=K)
    else:              # tulip
        k.shape([(x - r * 0.5, y + r * 0.6), (x - r * 0.55, y - r * 0.1), (x, y - r * 0.6), (x + r * 0.55, y - r * 0.1), (x + r * 0.5, y + r * 0.6),
                 (x + r * 0.22, y + r * 0.2), (x, y + r * 0.65), (x - r * 0.22, y + r * 0.2)], lw=0.6, fill=Wt, amp=0)


def flowerpot(k, x, y, w, kind=0, n=3):
    h = w * 0.8
    k.shape([(x - w * 0.38, y), (x + w * 0.38, y), (x + w * 0.5, y + h * 0.78), (x - w * 0.5, y + h * 0.78)], lw=0.9, fill=Wt, amp=0.2)
    k.shape([(x - w * 0.56, y + h * 0.78), (x + w * 0.56, y + h * 0.78), (x + w * 0.56, y + h), (x - w * 0.56, y + h)], lw=0.9, fill=Wt, amp=0.2)
    k.hatch([(x + w * 0.12, y), (x + w * 0.38, y), (x + w * 0.5, y + h * 0.78), (x + w * 0.2, y + h * 0.78)], angle=70, gap=1.6, lw=0.35)
    for i in range(n):
        t = (i + 0.5) / n
        bx = x + lerp(-w * 0.3, w * 0.3, t); top = y + h + w * (0.55 + 0.35 * math.sin(i * 2.1 + 1))
        tx = bx + w * 0.12 * math.sin(i * 1.7)
        k.line([(bx, y + h), (tx, top)], lw=0.6, amp=0.2)
        lx = lerp(bx, tx, 0.45); ly = lerp(y + h, top, 0.45); sg = 1 if i % 2 else -1
        k.shape([(lx, ly), (lx + sg * w * 0.16, ly + w * 0.08), (lx + sg * w * 0.24, ly + w * 0.2), (lx + sg * w * 0.08, ly + w * 0.14)], lw=0.5, fill=K, amp=0)
        flower(k, tx, top, w * 0.15, kind)


def watering_can(k, x, y, w):
    h = w * 0.55
    k.shape([(x - w * 0.3, y), (x + w * 0.25, y), (x + w * 0.22, y + h), (x - w * 0.27, y + h)], lw=0.9, fill=Wt, amp=0.2)
    k.hatch([(x + w * 0.05, y), (x + w * 0.25, y), (x + w * 0.22, y + h), (x + w * 0.04, y + h)], angle=80, gap=1.5, lw=0.35)
    k.line([(x + w * 0.2, y + h * 0.25), (x + w * 0.55, y + h * 0.95)], lw=1.6, amp=0)
    k.shape([(x + w * 0.5, y + h * 0.9), (x + w * 0.66, y + h * 1.08), (x + w * 0.6, y + h * 0.82)], lw=0.8, fill=Wt, amp=0)
    k.c.setLineWidth(1.1); k.c.arc(x - w * 0.22, y + h * 0.75, x + w * 0.12, y + h * 1.35, 0, 180)
    k.line([(x - w * 0.27, y + h * 0.8), (x - w * 0.45, y + h * 0.55)], lw=1.0, amp=0)


def pitcher(k, x, y, h):
    w = h * 0.62
    body = [(x - w * 0.38, y), (x + w * 0.38, y), (x + w * 0.46, y + h * 0.55), (x + w * 0.34, y + h * 0.92), (x + w * 0.45, y + h),
            (x - w * 0.5, y + h), (x - w * 0.38, y + h * 0.9), (x - w * 0.48, y + h * 0.5)]
    k.shape(body, lw=0.9, fill=Wt, amp=0.15)
    k.line([(x - w * 0.42, y + h * 0.7), (x + w * 0.42, y + h * 0.7)], lw=0.5, amp=0.2)   # lemonade level
    k.hatch([(x - w * 0.38, y), (x + w * 0.38, y), (x + w * 0.46, y + h * 0.55), (x + w * 0.42, y + h * 0.7), (x - w * 0.43, y + h * 0.7), (x - w * 0.48, y + h * 0.5)], angle=-60, gap=2.6, lw=0.3)
    for i in range(3):
        cx, cy = x - w * 0.15 + i * w * 0.15, y + h * (0.3 + 0.12 * (i % 2))
        k.circle(cx, cy, w * 0.09, lw=0.5, fill=Wt)
    k.c.setLineWidth(1.3); k.c.arc(x + w * 0.3, y + h * 0.3, x + w * 0.78, y + h * 0.82, -80, 80)


def glass(k, x, y, h, straw=True):
    w = h * 0.55
    k.shape([(x - w * 0.42, y), (x + w * 0.42, y), (x + w * 0.5, y + h), (x - w * 0.5, y + h)], lw=0.8, fill=Wt, amp=0.1)
    k.hatch([(x - w * 0.42, y), (x + w * 0.42, y), (x + w * 0.47, y + h * 0.7), (x - w * 0.47, y + h * 0.7)], angle=-60, gap=2.4, lw=0.3)
    k.line([(x - w * 0.47, y + h * 0.7), (x + w * 0.47, y + h * 0.7)], lw=0.5, amp=0)
    if straw:
        k.line([(x + w * 0.1, y + h * 0.15), (x + w * 0.45, y + h * 1.35)], lw=1.4, amp=0)
    k.shape(k.arcpts(x - w * 0.5, y + h * 0.98, w * 0.3, w * 0.3, 90, 270, 10), lw=0.6, fill=Wt, amp=0)


def pumpkin(k, x, y, w):
    h = w * 0.62
    for dx, sc in ((-0.28, 0.55), (0.28, 0.55), (0, 0.62)):
        k.shape(k.arcpts(x + dx * w, y + h / 2, w * sc / 1.25, h / 2, 0, 360, 30), lw=0.9, fill=Wt, amp=0.15)
    k.hatch(k.arcpts(x + 0.28 * w, y + h / 2, w * 0.44, h / 2, -90, 90, 16), angle=75, gap=1.6, lw=0.35)
    k.shape([(x - w * 0.03, y + h * 0.95), (x + w * 0.04, y + h * 0.95), (x + w * 0.1, y + h * 1.25), (x + w * 0.04, y + h * 1.27)], lw=0.8, fill=K, amp=0)


def leaf(k, x, y, s, ang=0, fill=Wt):
    a = math.radians(ang)
    def P(u, v): return (x + (u * math.cos(a) - v * math.sin(a)) * s, y + (u * math.sin(a) + v * math.cos(a)) * s)
    pts = [P(0, 0), P(0.3, 0.25), P(0.42, 0.42), P(0.3, 0.55), P(0.5, 0.7), P(0.18, 0.75), P(0, 1.0), P(-0.18, 0.75), P(-0.5, 0.7), P(-0.3, 0.55), P(-0.42, 0.42), P(-0.3, 0.25)]
    k.shape(pts, lw=0.6, fill=fill, amp=0)
    k.line([P(0, -0.2), P(0, 0.8)], lw=0.5, amp=0)
    for sg in (-1, 1): k.line([P(0, 0.3), P(sg * 0.32, 0.55)], lw=0.4, amp=0)


def sun(k, x, y, r):
    k.circle(x, y, r, lw=0.9, fill=Wt)
    for i in range(12):
        a = 2 * math.pi * i / 12
        k.line([(x + r * 1.3 * math.cos(a), y + r * 1.3 * math.sin(a)), (x + r * 1.75 * math.cos(a), y + r * 1.75 * math.sin(a))], lw=0.8, amp=0)


def bird(k, x, y, s):
    k.line([(x - s, y + s * 0.3)] + k.arcpts(x - s / 2, y, s / 2, s * 0.35, 160, 20, 6)[1:] + k.arcpts(x + s / 2, y, s / 2, s * 0.35, 160, 20, 6), lw=0.7, amp=0)


def crossword_sheet(k, x, y, cell, light=False):
    """A little crossword grid (5x5) with a few black squares and letters."""
    blacks = {(0, 3), (1, 1), (1, 3), (3, 1), (3, 3), (4, 1)}
    letters = {(0, 0): "T", (0, 1): "E", (0, 2): "A", (2, 0): "S", (2, 1): "W", (2, 2): "I", (2, 3): "N", (2, 4): "G"}
    k.rect(x - cell * 0.4, y - cell * 0.4, cell * 5.8, cell * 5.8, lw=0.6)
    for r in range(5):
        for c in range(5):
            cx, cy = x + c * cell, y + (4 - r) * cell
            k.rect(cx, cy, cell, cell, lw=0.5, fill=K if (r, c) in blacks else Wt)
            if (r, c) in letters:
                k.text(cx + cell / 2, cy + cell * 0.22, letters[(r, c)], size=cell * 0.7, font="Ink-Plex")


def swing(k, cx, beam_y, seat_y, w, cushion=True):
    """A porch swing hanging on two chains from the beam."""
    for sx in (-1, 1):
        x = cx + sx * w * 0.5
        n = 9
        for i in range(n):
            y0 = lerp(beam_y, seat_y + w * 0.36, i / n); y1 = lerp(beam_y, seat_y + w * 0.36, (i + 1) / n)
            k.shape(k.arcpts(x, (y0 + y1) / 2, 1.3 if i % 2 else 0.6, (y1 - y0) / 2 + 0.6, 0, 360, 10), lw=0.5, fill=None, amp=0)
        k.circle(x, beam_y, 1.6, lw=0.6, fill=K)
    # back rest (white backing so nothing behind shows through the slats)
    k.shape([(cx - w * 0.55, seat_y), (cx + w * 0.55, seat_y), (cx + w * 0.55, seat_y + w * 0.36), (cx - w * 0.55, seat_y + w * 0.36)], lw=0, fill=Wt, stroke=False, amp=0)
    for i in range(7):
        x = lerp(cx - w * 0.47, cx + w * 0.47, i / 6)
        k.line([(x, seat_y + w * 0.06), (x, seat_y + w * 0.32)], lw=1.0, amp=0)
    k.rect(cx - w * 0.52, seat_y + w * 0.31, w * 1.04, w * 0.05, lw=0.8)
    k.rect(cx - w * 0.52, seat_y + w * 0.15, w * 1.04, w * 0.03, lw=0.6)
    # seat and arms
    k.rect(cx - w * 0.55, seat_y, w * 1.1, w * 0.06, lw=0.9)
    k.hatch([(cx - w * 0.55, seat_y), (cx + w * 0.55, seat_y), (cx + w * 0.55, seat_y + w * 0.02), (cx - w * 0.55, seat_y + w * 0.02)], angle=0, gap=1.2, lw=0.3)
    for sx in (-1, 1):
        k.line([(cx + sx * w * 0.55, seat_y + w * 0.06), (cx + sx * w * 0.55, seat_y + w * 0.2), (cx + sx * w * 0.42, seat_y + w * 0.2)], lw=1.1, amp=0)
    if cushion:
        px, py, pw = cx - w * 0.36, seat_y + w * 0.06, w * 0.2
        pil = [(px - pw / 2, py), (px + pw / 2, py + pw * 0.04), (px + pw / 2 + pw * 0.06, py + pw * 0.8), (px - pw / 2 + pw * 0.08, py + pw * 0.86)]
        k.shape(pil, lw=0.8, fill=Wt, amp=0.3)
        k.hatch(pil, angle=45, gap=2.6, lw=0.3, cross=True)
        k.circle(px + pw * 0.04, py + pw * 0.43, 1.4, lw=0.5, fill=K)


def porch(k, x0, x1, floor_y, beam_y, roof_y, rail=True):
    """Porch frame: boards, two posts, a beam with a scalloped trim and an eave."""
    k.line([(x0, floor_y), (x1, floor_y)], lw=1.1, amp=0.2)
    for i in range(1, 4):
        k.line([(x0 + 2 * i, floor_y - i * 5), (x1 - 2 * i, floor_y - i * 5)], lw=0.4, amp=0.3)
    pw = 9
    for px in (x0 + 6, x1 - 6 - pw):
        k.rect(px, floor_y, pw, roof_y - floor_y, lw=0.9)
        k.hatch([(px + pw * 0.55, floor_y), (px + pw, floor_y), (px + pw, roof_y), (px + pw * 0.55, roof_y)], angle=90, gap=1.4, lw=0.35)
    k.rect(x0, beam_y, x1 - x0, roof_y - beam_y, lw=0.9)
    xx = x0 + 6
    while xx < x1 - 12:
        k.c.setLineWidth(0.6); k.c.arc(xx, beam_y - 5, xx + 12, beam_y + 5, 180, 180)
        xx += 12
    k.shape([(x0 - 8, roof_y), (x1 + 8, roof_y), (x1 - 4, roof_y + 16), (x0 + 4, roof_y + 16)], lw=1.0, fill=Wt, amp=0.2)
    for i in range(1, 4):
        k.line([(x0 - 8 + i * 4, roof_y + i * 4), (x1 + 8 - i * 4, roof_y + i * 4)], lw=0.35, amp=0.2)
    if rail:
        for (a, b) in ((x0 + 15, x0 + (x1 - x0) * 0.24), (x1 - (x1 - x0) * 0.24, x1 - 15)):
            k.rect(a, floor_y + 30, b - a, 3, lw=0.7)
            xx = a + 3
            while xx < b - 2:
                k.line([(xx, floor_y), (xx, floor_y + 30)], lw=0.8, amp=0)
                xx += 5


# ----------------------------------------------------------------------------- pictures
def frontispiece(k, w, h):
    """The porch swing on a summer afternoon: cat on the cushion, lemonade, a crossword and pencil, garden beyond."""
    m = 9; k.frame(m, m, w - m, h - m, corner_flakes=False)
    k.clip_rect(m + 4, m + 4, w - m - 4, h - m - 4)
    floor = h * 0.13; beam = h * 0.84; roof = h * 0.88
    # garden beyond
    hz = h * 0.36
    k.hills(m, w - m, hz + 40, amp=12, n=3)
    k.line([(m, hz), (w - m, hz)], lw=0.7, amp=0.4)
    tree(k, w * 0.25, hz, h * 0.26); tree(k, w * 0.74, hz, h * 0.22); tree(k, w * 0.52, hz + 2, h * 0.15)
    for i in range(14):
        x = lerp(m + 20, w - m - 20, i / 13); k.line([(x - 3, hz - 4), (x, hz + 2), (x + 3, hz - 4)], lw=0.4, amp=0)
    sun(k, w * 0.8, h * 0.72, 11)
    for bx, by, s in ((0.3, 0.7, 5), (0.36, 0.73, 4), (0.42, 0.69, 3.5)): bird(k, w * bx, h * by, s)
    porch(k, m + 4, w - m - 4, floor, beam, roof)
    swing(k, w * 0.5, beam, floor + h * 0.17, w * 0.5)
    sy = floor + h * 0.17
    k.cat(w * 0.62, sy + w * 0.5 * 0.06, w * 0.13)
    crossword_sheet(k, w * 0.33, sy + w * 0.5 * 0.065, 3.2)
    k.pencil(w * 0.43, sy + w * 0.5 * 0.07, 22, ang=10)
    t = k.side_table(w * 0.86, floor, 34)
    pitcher(k, w * 0.83, t + 2, 28); glass(k, w * 0.9, t + 2, 14)
    flowerpot(k, w * 0.14, floor, 26, kind=0); flowerpot(k, w * 0.24, floor, 18, kind=1, n=2)
    watering_can(k, w * 0.66, floor - 1, 26)
    k.unclip()


def title(k, w, h):
    """Title-page art: the swing between two pots of flowers."""
    beam = h * 0.95
    k.line([(w * 0.12, beam), (w * 0.88, beam)], lw=1.4, amp=0.2)
    swing(k, w * 0.5, beam, h * 0.2, w * 0.36)
    k.line([(w * 0.06, h * 0.04), (w * 0.94, h * 0.04)], lw=0.9, amp=0.3)
    flowerpot(k, w * 0.12, h * 0.04, 30, kind=0); flowerpot(k, w * 0.88, h * 0.04, 30, kind=1)


def op_spring(k, w, h):
    """Spring: pots of tulips and daisies on the step, a watering can and birds on a blossom branch."""
    k.line([(w * 0.04, h * 0.1), (w * 0.96, h * 0.1)], lw=0.9, amp=0.3)
    k.line([(w * 0.08, h * 0.04), (w * 0.92, h * 0.04)], lw=0.5, amp=0.3)
    for i, (x, s, kind) in enumerate(((0.16, 34, 1), (0.3, 26, 0), (0.42, 30, 1))):
        flowerpot(k, w * x, h * 0.1, s, kind=kind, n=3)
    watering_can(k, w * 0.62, h * 0.1, 46)
    br = [(w * 0.55, h * 0.95), (w * 0.7, h * 0.86), (w * 0.85, h * 0.8), (w * 0.98, h * 0.78)]
    k.line(br, lw=1.4, amp=0.3)
    for i in range(9):
        t = (i + 0.5) / 9; x = lerp(w * 0.56, w * 0.97, t); y = lerp(h * 0.93, h * 0.78, t) + (5 if i % 2 else -5)
        flower(k, x, y, 4.5, 0)
    for bx, by, s in ((0.3, 0.8, 6), (0.38, 0.86, 5), (0.22, 0.88, 4)): bird(k, w * bx, h * by, s)


def op_summer(k, w, h):
    """Summer: lemonade on a little table, a straw hat and the sun."""
    floor = h * 0.08
    k.line([(w * 0.04, floor), (w * 0.96, floor)], lw=0.9, amp=0.3)
    t = k.side_table(w * 0.38, floor, 70)
    pitcher(k, w * 0.33, t + 2, 50); glass(k, w * 0.45, t + 2, 26)
    sun(k, w * 0.82, h * 0.72, 16)
    # straw hat on the step
    hx, hy = w * 0.66, floor
    k.shape(k.arcpts(hx, hy + 6, 36, 7, 0, 360, 30), lw=0.9, fill=Wt, amp=0.1)
    k.shape(k.arcpts(hx, hy + 9, 17, 18, 0, 180, 20) + [(hx - 17, hy + 9)], lw=0.9, fill=Wt, amp=0.1)
    k.hatch(k.arcpts(hx, hy + 9, 17, 18, 0, 180, 20) + [(hx - 17, hy + 9)], angle=30, gap=2.0, lw=0.35, cross=True)
    k.rect(hx - 17, hy + 9, 34, 5, lw=0.7, fill=K)
    for bx, by, s in ((0.62, 0.86, 6), (0.7, 0.9, 4.5)): bird(k, w * bx, h * by, s)
    flowerpot(k, w * 0.12, floor, 30, kind=0)


def op_autumn(k, w, h):
    """Autumn: pumpkins on the porch steps, a rake, falling leaves."""
    for i in range(3):
        y = h * 0.05 + i * h * 0.12; x0 = w * (0.08 + i * 0.06); x1 = w * (0.62 - i * 0.04)
        k.line([(x0, y), (x1, y)], lw=0.9, amp=0.2); k.line([(x1, y), (x1, y - h * 0.12 if i else 0)], lw=0.7, amp=0)
    pumpkin(k, w * 0.2, h * 0.05, 56); pumpkin(k, w * 0.38, h * 0.17, 40); pumpkin(k, w * 0.5, h * 0.29, 28)
    # rake leaning
    k.line([(w * 0.74, h * 0.05), (w * 0.86, h * 0.92)], lw=1.4, amp=0)
    k.shape([(w * 0.66, h * 0.02), (w * 0.82, h * 0.02), (w * 0.755, h * 0.14)], lw=0.8, fill=Wt, amp=0)
    for i in range(7):
        x = lerp(w * 0.665, w * 0.815, i / 6); k.line([(x, h * 0.02), (w * 0.755, h * 0.13)], lw=0.5, amp=0)
    for i, (x, y, a) in enumerate(((0.12, 0.7, 20), (0.25, 0.85, -30), (0.4, 0.62, 60), (0.58, 0.8, -10), (0.92, 0.6, 40), (0.95, 0.25, -50), (0.62, 0.5, 15))):
        leaf(k, w * x, h * y, 13, a, fill=K if i % 3 == 0 else Wt)


def op_winter(k, w, h):
    """Winter: a frosty window, a mug of cocoa and the cat asleep on the sill."""
    k.window_snow(w * 0.3, h * 0.2, w * 0.4, h * 0.75)
    k.line([(w * 0.06, h * 0.2), (w * 0.94, h * 0.2)], lw=1.0, amp=0.2)
    k.line([(w * 0.08, h * 0.17), (w * 0.92, h * 0.17)], lw=0.6, amp=0.2)
    k.cat(w * 0.82, h * 0.2, 46)
    k.mug(w * 0.16, h * 0.2, 30)
    crossword_sheet(k, w * 0.04, h * 0.32, 4.2)
    k.candle(w * 0.24, h * 0.2, 36)


def thanks(k, w, h):
    k.line([(w * 0.06, h * 0.08), (w * 0.94, h * 0.08)], lw=0.8, amp=0.3)
    k.line([(w * 0.2, h * 0.97), (w * 0.8, h * 0.97)], lw=1.2, amp=0.2)
    swing(k, w * 0.5, h * 0.97, h * 0.25, w * 0.4)
    k.cat(w * 0.56, h * 0.25 + w * 0.4 * 0.06, 26)
    flowerpot(k, w * 0.1, h * 0.08, 20, kind=1, n=2)


def v_pencil(k, w, h):
    crossword_sheet(k, w * 0.32, h * 0.12, h * 0.13); k.pencil(w * 0.52, h * 0.1, h * 0.85, ang=22)


def v_lemonade(k, w, h):
    k.line([(w * 0.12, h * 0.08), (w * 0.88, h * 0.08)], lw=0.7, amp=0.3)
    pitcher(k, w * 0.42, h * 0.09, h * 0.7); glass(k, w * 0.62, h * 0.09, h * 0.38)


def v_cat(k, w, h):
    k.rug(w * 0.5, h * 0.22, w * 0.62, h * 0.3); k.cat(w * 0.5, h * 0.18, h * 0.75)


def v_flowers(k, w, h):
    k.line([(w * 0.12, h * 0.08), (w * 0.88, h * 0.08)], lw=0.7, amp=0.3)
    flowerpot(k, w * 0.36, h * 0.08, h * 0.38, kind=0); flowerpot(k, w * 0.62, h * 0.08, h * 0.3, kind=1, n=2)


def v_leaves(k, w, h):
    for i, (x, y, a) in enumerate(((0.3, 0.2, 20), (0.45, 0.45, -35), (0.6, 0.18, 50), (0.72, 0.5, -10))):
        leaf(k, w * x, h * y, h * 0.42, a, fill=K if i % 2 else Wt)


def v_teacup(k, w, h):
    k.line([(w * 0.12, h * 0.08), (w * 0.88, h * 0.08)], lw=0.7, amp=0.3)
    k.teapot(w * 0.4, h * 0.09, h * 0.9); k.cup(w * 0.68, h * 0.09, h * 0.38)


def v_swing(k, w, h):
    k.line([(w * 0.25, h * 0.96), (w * 0.75, h * 0.96)], lw=1.0, amp=0.2)
    swing(k, w * 0.5, h * 0.96, h * 0.12, h * 0.95, cushion=True)


def v_pumpkin(k, w, h):
    k.line([(w * 0.12, h * 0.08), (w * 0.88, h * 0.08)], lw=0.7, amp=0.3)
    pumpkin(k, w * 0.42, h * 0.08, h * 0.9); pumpkin(k, w * 0.64, h * 0.08, h * 0.55)


def cover_scene(k, w, h):
    """Front-cover scene (printed pale-on-dark by cover.py): the porch swing at dusk with a hanging lantern."""
    floor = h * 0.12; beam = h * 0.86; roof = h * 0.9
    hz = h * 0.36
    k.stars(10, h * 0.55, w - 10, h * 0.84, n=24)
    k.moon(w * 0.6, h * 0.74, 13)
    k.hills(0, w, hz + 20, amp=10, n=3)
    tree(k, w * 0.22, hz + 6, h * 0.26); tree(k, w * 0.74, hz + 12, h * 0.2); tree(k, w * 0.5, hz + 18, h * 0.13)
    porch(k, 4, w - 4, floor, beam, roof)
    swing(k, w * 0.48, beam, floor + h * 0.16, w * 0.5)
    sy = floor + h * 0.16
    k.cat(w * 0.6, sy + w * 0.5 * 0.06, w * 0.13)
    crossword_sheet(k, w * 0.31, sy + w * 0.5 * 0.065, 3.4)
    k.pencil(w * 0.41, sy + w * 0.5 * 0.07, 22, ang=10)
    k.line([(w * 0.88, beam), (w * 0.88, beam - 30)], lw=0.7, amp=0)
    k.lantern(w * 0.88, beam - 30 - 26, 26)
    t = k.side_table(w * 0.86, floor, 30)
    glass(k, w * 0.86, t + 2, 16)
    flowerpot(k, w * 0.13, floor, 26, kind=0)


VIGNETTES = ["v_pencil", "v_lemonade", "v_cat", "v_flowers", "v_leaves", "v_teacup", "v_swing", "v_pumpkin"]
SPECS = {
    "frontispiece": (4.7, 7.0, frontispiece, 41),
    "title": (4.0, 2.0, title, 43),
    "opener-spring": (4.7, 2.6, op_spring, 51), "opener-summer": (4.7, 2.6, op_summer, 52),
    "opener-autumn": (4.7, 2.6, op_autumn, 53), "opener-winter": (4.7, 2.6, op_winter, 54),
    "thanks": (3.4, 1.6, thanks, 61),
    "cover-scene": (5.4, 4.6, cover_scene, 71),
    **{n: (1.9, 0.85, globals()[n], 80 + i) for i, n in enumerate(VIGNETTES)},
}

if __name__ == "__main__":
    only = set(sys.argv[1:])
    for name, (wi, hi, fn, seed) in SPECS.items():
        if only and name not in only:
            continue
        render(os.path.join(OUT, name + ".png"), wi, hi, fn, seed=seed); print("drew", name)
