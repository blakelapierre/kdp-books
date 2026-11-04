"""Black-and-white ink illustrations for Twenty-Five Christmases -> ../illustrations/*.png
Pure black line art on white at 300 DPI, drawn with the shared inkart house style (inkart.py) plus
the small motifs from Two Cups of Tea (motifs.py) and new Christmas motifs below: wreaths, gifts,
stockings, holly, bells, baubles, gingerbread, candy canes and pine cones. No people in any scene.
Deterministic: same seeds -> same images. Run from src/: python3 illustrations.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inkart import render, Wt, K, lerp
from motifs import (teacup, mug2, leaf, table, chair, string_lights, steam, songbird, heart,
                    teapot2, jug, vase, corner_sprigs)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "illustrations")


# ----------------------------------------------------------------------------- christmas motifs
def holly_leaf(k, x, y, L, ang, fill=Wt, lw=0.6):
    """Spiky holly leaf from (x, y) pointing at angle ang (degrees), length L: scalloped edge with points."""
    a = math.radians(ang); ca, sa = math.cos(a), math.sin(a)
    T = lambda u, v: (x + u * ca - v * sa, y + u * sa + v * ca)
    n = 4; W = L * 0.3
    top, bot = [], []
    for i in range(n + 1):
        t = i / n; wdt = W * math.sin(math.pi * min(0.97, max(0.03, t))) ** 0.6
        top.append(T(t * L, wdt * (1.25 if 0 < i < n else 0)))
        bot.append(T(t * L, -wdt * (1.25 if 0 < i < n else 0)))
        if i < n:
            tm = (i + 0.5) / n; wm = W * math.sin(math.pi * tm) ** 0.6 * 0.62
            top.append(T(tm * L, wm)); bot.append(T(tm * L, -wm))
    pts = top + bot[::-1]
    k.shape(pts, lw=lw, fill=fill, amp=0)
    if fill == Wt:
        k.hatch(top + [T(L, 0), T(0, 0)], angle=ang + 70, gap=1.2, lw=0.3)
        k.shape(pts, lw=lw, fill=None, amp=0)
    k.c.setStrokeColor(Wt if fill == K else K); k.c.setLineWidth(0.45)
    p0, p1 = T(0, 0), T(L * 0.9, 0); k.c.line(p0[0], p0[1], p1[0], p1[1])

def berries(k, x, y, r, n=3):
    for i in range(n):
        a = math.radians(-90 + 120 * i)
        bx, by = x + r * 0.95 * math.cos(a), y + r * 0.95 * math.sin(a)
        k.circle(bx, by, r, lw=0.5, fill=K)
        k.circle(bx - r * 0.32, by + r * 0.32, r * 0.25, lw=0, fill=Wt, stroke=False)

def holly(k, x, y, L, ang=0):
    holly_leaf(k, x, y, L, ang + 160)
    holly_leaf(k, x, y, L, ang + 20)
    holly_leaf(k, x, y, L * 0.8, ang + 95, fill=K)
    berries(k, x, y, L * 0.11)

def bow(k, x, y, w, tails=True):
    for sx in (-1, 1):
        loop = [(x, y), (x + sx * w * 0.5, y + w * 0.32), (x + sx * w * 0.55, y + w * 0.05), (x + sx * w * 0.48, y - w * 0.15)]
        pts = [(x, y)] + [(x + sx * w * 0.5 * math.sin(math.pi * t) * (1 + 0.1 * t), y + w * 0.3 * math.sin(2 * math.pi * t + 0.2)) for t in [i / 16 for i in range(17)]]
        k.shape(pts, lw=0.7, fill=Wt, amp=0)
        k.line([(x + sx * w * 0.08, y + 0.6), (x + sx * w * 0.38, y + w * 0.12)], lw=0.35, amp=0)
        if tails:
            k.shape([(x, y), (x + sx * w * 0.25, y - w * 0.5), (x + sx * w * 0.34, y - w * 0.42), (x + sx * w * 0.06, y)], lw=0.6, fill=Wt, amp=0)
    k.circle(x, y, w * 0.08, lw=0.7, fill=K)


def wreath(k, x, y, r, bow_=True, candles=False):
    """Evergreen wreath centred at (x, y), outer radius r: dense needle sprays, berries, cones, a bow."""
    k.circle(x, y, r * 0.97, lw=0.8, fill=Wt)
    k.circle(x, y, r * 0.5, lw=0.8, fill=Wt)
    n = 26
    for ring, (rr, off) in enumerate([(0.62, 0.0), (0.84, 0.5), (0.73, 0.25)]):
        for i in range(n):
            a = 2 * math.pi * (i + off) / n
            px, py = x + r * rr * math.cos(a), y + r * rr * math.sin(a)
            tang = a + math.pi / 2
            L = r * 0.2
            # sprig: a stem with needles each side
            ex, ey = px + L * math.cos(tang), py + L * math.sin(tang)
            k.c.setStrokeColor(K); k.c.setLineWidth(0.4); k.c.line(px, py, ex, ey)
            for j in range(1, 6):
                t = j / 6; sx, sy = lerp(px, ex, t), lerp(py, ey, t)
                for sg in (-1, 1):
                    b = tang + sg * 0.9
                    k.c.line(sx, sy, sx + L * 0.28 * math.cos(b), sy + L * 0.28 * math.sin(b))
    k.circle(x, y, r * 0.47, lw=0.9, fill=Wt)
    for a in (30, 140, 200, 330):
        holly(k, x + r * 0.73 * math.cos(math.radians(a)), y + r * 0.73 * math.sin(math.radians(a)), r * 0.2, ang=a - 90)
    for a in (85, 255):
        cone(k, x + r * 0.73 * math.cos(math.radians(a)), y + r * 0.73 * math.sin(math.radians(a)), r * 0.22, a - 90)
    if bow_:
        bow(k, x, y - r * 0.73, r * 0.6)

def cone(k, x, y, h, ang=0):
    """Pine cone, base at (x, y), height h, rotated ang degrees: an egg of overlapping scales."""
    a = math.radians(ang); ca, sa = math.cos(a), math.sin(a)
    T = lambda u, v: (x + u * ca - v * sa, y + u * sa + v * ca)
    W = h * 0.34
    outline = [T(W * math.sin(math.pi * t) * (1.15 - 0.4 * t), h * t) for t in [i / 20 for i in range(21)]] + \
              [T(-W * math.sin(math.pi * t) * (1.15 - 0.4 * t), h * t) for t in [i / 20 for i in range(20, -1, -1)]]
    k.shape(outline, lw=0.8, fill=Wt, amp=0)
    k.c.saveState(); k.c.clipPath(k.path(outline, closed=True), stroke=0, fill=0)
    rows = 6
    for rI in range(rows):
        t = (rI + 0.5) / rows; v = h * t; ww = W * math.sin(math.pi * t) * (1.15 - 0.4 * t)
        for j in range(-2, 3):
            u = j * ww * 0.5 + (rI % 2) * ww * 0.25
            arc = [T(u + ww * 0.28 * math.cos(math.radians(q)), v + h * 0.08 * math.sin(math.radians(q)) - h * 0.04) for q in range(180, 361, 20)]
            k.shape(arc + [T(u, v + h * 0.05)], lw=0.4, fill=Wt, amp=0)
            k.line(arc, lw=0.7, amp=0)
    k.c.restoreState()
    k.shape(outline, lw=0.8, fill=None, amp=0)

def gift(k, x, y, w, h, lid=True, bow_=True, pattern="stripes", ribbon_dark=True):
    """Wrapped present; (x, y) = bottom-left."""
    k.rect(x, y, w, h, lw=0.9)
    if pattern == "stripes":
        k.hatch([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], angle=60, gap=max(2.6, w * 0.09), lw=0.5)
    elif pattern == "dots":
        for i in range(5):
            for j in range(4):
                k.circle(x + w * (0.1 + 0.2 * i) + (j % 2) * w * 0.1, y + h * (0.15 + 0.23 * j), max(0.6, w * 0.025), lw=0.2, fill=K)
    elif pattern == "stars":
        for i in range(3):
            for j in range(2):
                k.star5(x + w * (0.2 + 0.3 * i), y + h * (0.28 + 0.4 * j), max(1.2, w * 0.05), fill=Wt, lw=0.4)
    elif pattern == "dark":
        k.rect(x, y, w, h, lw=0.9, fill=K)
    k.rect(x, y, w, h, lw=0.9, fill=None)
    rw = max(2.0, w * 0.12)
    col = Wt if pattern == "dark" else (K if ribbon_dark else Wt)
    k.rect(x + w / 2 - rw / 2, y, rw, h, lw=0.5, fill=col)
    if lid:
        lh = h * 0.18
        k.rect(x - w * 0.04, y + h - lh, w * 1.08, lh, lw=0.9, fill=Wt if pattern != "dark" else K)
        k.rect(x + w / 2 - rw / 2, y + h - lh, rw, lh, lw=0.5, fill=col)
    if bow_:
        bow(k, x + w / 2, y + h + w * 0.05, w * 0.42, tails=False)


def gift_pile(k, x, y, s):
    gift(k, x, y, s * 1.2, s * 0.8, pattern="stripes")
    gift(k, x + s * 1.3, y, s * 0.9, s * 1.05, pattern="dots")
    gift(k, x + s * 0.35, y + s * 0.8, s * 0.7, s * 0.55, pattern="dark")
    gift(k, x + s * 2.3, y, s * 0.75, s * 0.55, pattern="stars")


def stocking(k, x, y, h, pattern=0):
    """Hanging stocking; (x, y) = top-left of the cuff, toe points right."""
    w = h * 0.42
    leg_bot = y - h * 0.62
    body = [(x + w * 0.04, y - h * 0.2), (x + w * 0.96, y - h * 0.2), (x + w * 0.96, leg_bot)] + \
           [(x + w * 0.96 + w * 0.55 * t, leg_bot - h * 0.06 * t) for t in (0.5, 1.0)] + \
           k.arcpts(x + w * 1.51, leg_bot - h * 0.18, w * 0.26, h * 0.12, 90, -90, 10)[1:] + \
           k.arcpts(x + w * 0.5, leg_bot - h * 0.12, w * 0.46, h * 0.18, 270, 180, 10)[1:]
    k.shape(body, lw=0.9, fill=Wt, amp=0)
    k.c.saveState(); k.c.clipPath(k.path(body, closed=True), stroke=0, fill=0)
    if pattern == 0:
        for j in range(4):
            k.rect(x - 5, y - h * (0.33 + 0.13 * j), w * 2.4, h * 0.05, lw=0.3, fill=K)
    elif pattern == 1:
        for j in range(4):
            for i in range(3):
                k.star5(x + w * (0.22 + 0.3 * i) + (j % 2) * w * 0.12, y - h * (0.3 + 0.14 * j), w * 0.09, fill=Wt, lw=0.4)
    else:
        k.hatch(body, angle=45, gap=2.0, lw=0.4, cross=True)
    k.c.restoreState()
    # heel and toe patches
    toe = k.arcpts(x + w * 1.51, leg_bot - h * 0.18, w * 0.26, h * 0.12, 90, -90, 10)
    k.shape(toe + [(x + w * 1.38, leg_bot - h * 0.18)], lw=0.5, fill=K, amp=0)
    k.shape(body, lw=0.9, fill=None, amp=0)
    k.rect(x - w * 0.06, y - h * 0.22, w * 1.12, h * 0.22, lw=0.8, fill=Wt)
    for i in range(7):
        k.circle(x + w * (0.04 + 0.15 * i), y - h * 0.11 + (i % 2) * 1.2, 0.8, lw=0.3, fill=Wt)
    k.line([(x + w * 0.12, y), (x + w * 0.18, y + h * 0.07), (x + w * 0.26, y)], lw=0.5, amp=0)

def bauble(k, x, y, r, style=0):
    """Hanging Christmas bauble; (x, y) = centre."""
    k.rect(x - r * 0.22, y + r * 0.92, r * 0.44, r * 0.25, lw=0.6, fill=K)
    k.c.setStrokeColor(K); k.c.setLineWidth(0.45); k.c.circle(x, y + r * 1.27, r * 0.12, stroke=1, fill=0)
    k.circle(x, y, r, lw=0.9, fill=Wt)
    k.c.saveState(); p = k.c.beginPath(); p.circle(x, y, r - 0.4); k.c.clipPath(p, stroke=0, fill=0)
    if style == 0:
        for dy in (-0.35, 0.0, 0.35):
            k.line([(x - r, y + dy * r), (x + r, y + dy * r)], lw=0.5, amp=0)
        for i in range(5): k.star5(x + r * (-0.6 + 0.3 * i), y + r * 0.17, r * 0.08, fill=K, lw=0.2)
        k.hatch([(x - r, y - r * 0.35), (x + r, y - r * 0.35), (x + r, y - r), (x - r, y - r)], angle=0, gap=1.2, lw=0.35)
    elif style == 1:
        for i in range(-3, 4):
            k.line([(x + i * r * 0.3 - r * 0.15, y - r), (x + i * r * 0.3, y), (x + i * r * 0.3 - r * 0.15, y + r)], lw=0.45, amp=0)
    else:
        k.hatch([(x - r, y - r), (x + r, y - r), (x + r, y + r), (x - r, y + r)], angle=45, gap=1.4, lw=0.4)
        k.circle(x - r * 0.35, y + r * 0.35, r * 0.22, lw=0, fill=Wt, stroke=False)
    k.c.restoreState()
    k.circle(x, y, r, lw=0.9, fill=None)


def bell(k, x, y, h, ang=0):
    """Hand bell hanging from (x, y) (top), height h, tilted ang degrees."""
    a = math.radians(ang); ca, sa = math.cos(a), math.sin(a)
    T = lambda u, v: (x + u * ca - v * sa, y + u * sa + v * ca)
    w = h * 0.95
    right = [(w * (0.14 + 0.36 * (t ** 2.2)), -h * t) for t in [i / 12 for i in range(13)]]
    prof = [T(-u, v) for (u, v) in right[::-1]] + [T(u, v) for (u, v) in right]
    k.shape(prof, lw=0.9, fill=Wt, amp=0)
    k.hatch([T(u, v) for (u, v) in right] + [T(w * 0.04, -h), T(w * 0.04, 0)], angle=ang + 90, gap=1.2, lw=0.35)
    k.shape(prof, lw=0.9, fill=None, amp=0)
    lip = [T(u, -h + w * 0.06 * math.sin(math.radians(q))) for q, u in [(q, w * 0.5 * math.cos(math.radians(q))) for q in range(0, 361, 20)]]
    k.shape(lip, lw=0.8, fill=Wt, amp=0)
    c = T(0, -h - h * 0.07); k.circle(c[0], c[1], h * 0.08, lw=0.6, fill=K)
    t = T(0, h * 0.06); k.circle(t[0], t[1], h * 0.07, lw=0.7, fill=None)

def bells(k, x, y, h):
    bell(k, x - h * 0.25, y, h, ang=18); bell(k, x + h * 0.25, y, h, ang=-18)
    holly(k, x, y + h * 0.1, h * 0.55, ang=0)


def gingerbread_man(k, x, y, h):
    """Gingerbread figure, (x, y) = bottom centre."""
    hr = h * 0.17
    hx, hy = x, y + h - hr
    body = []
    pts = [(x - h * 0.08, y + h * 0.66), (x - h * 0.38, y + h * 0.6), (x - h * 0.4, y + h * 0.48), (x - h * 0.13, y + h * 0.48),
           (x - h * 0.32, y + h * 0.05), (x - h * 0.2, y), (x, y + h * 0.25), (x + h * 0.2, y), (x + h * 0.32, y + h * 0.05),
           (x + h * 0.13, y + h * 0.48), (x + h * 0.4, y + h * 0.48), (x + h * 0.38, y + h * 0.6), (x + h * 0.08, y + h * 0.66)]
    k.shape(pts, lw=0.9, fill=Wt, amp=0.2)
    k.circle(hx, hy, hr, lw=0.9, fill=Wt)
    k.blob(k.arcpts(hx, hy - hr * 0.62, hr * 0.12, hr * 0.12, 0, 360, 8), Wt)
    for sx in (-1, 1): k.circle(hx + sx * hr * 0.35, hy + hr * 0.15, hr * 0.1, lw=0.3, fill=K)
    k.line(k.arcpts(hx, hy - hr * 0.05, hr * 0.4, hr * 0.35, 200, 340, 8), lw=0.5, amp=0)
    for dy in (0.56, 0.44, 0.32): k.circle(x, y + h * dy, h * 0.025, lw=0.3, fill=K)
    # icing zigzags
    for sx in (-1, 1):
        k.line([(x + sx * h * 0.3, y + h * 0.58), (x + sx * h * 0.33, y + h * 0.5), (x + sx * h * 0.36, y + h * 0.58)], lw=0.4, amp=0)
        k.line([(x + sx * h * 0.17, y + h * 0.1), (x + sx * h * 0.23, y + h * 0.04), (x + sx * h * 0.29, y + h * 0.1)], lw=0.4, amp=0)
    k.blob([(x - hr * 0.5, y + h * 0.69), (x, y + h * 0.64), (x + hr * 0.5, y + h * 0.69), (x, y + h * 0.72)], K)


def candy_cane(k, x, y, h, facing=1):
    f = facing; r = h * 0.18; w = h * 0.09
    outer = [(x - w / 2, y), (x - w / 2, y + h - r)] + [(x + f * r + f * (r + w / 2) * math.cos(math.radians(a)) * -1 * f * f, y + h - r + (r + w / 2) * math.sin(math.radians(a))) for a in [180 - 180 * i / 14 for i in range(15)]] + \
            [(x + f * (2 * r + w / 2), y + h - r - r * 0.5), (x + f * (2 * r - w / 2), y + h - r - r * 0.5)] + \
            [(x + f * r + f * (r - w / 2) * math.cos(math.radians(a)) * -1 * f * f, y + h - r + (r - w / 2) * math.sin(math.radians(a))) for a in [180 * i / 14 for i in range(15)]] + [(x + w / 2, y + h - r), (x + w / 2, y)]
    # simpler: draw as thick stroked path with stripes
    pts = [(x, y), (x, y + h - r)] + [(x + f * r - f * r * math.cos(math.radians(a)), y + h - r + r * math.sin(math.radians(a))) for a in range(0, 181, 10)] + [(x + f * 2 * r, y + h - r - r * 0.55)]
    k.c.setStrokeColor(K); k.c.setLineWidth(w + 1.6); k.c.drawPath(k.path(pts), stroke=1, fill=0)
    k.c.setStrokeColor(Wt); k.c.setLineWidth(w); k.c.drawPath(k.path(pts), stroke=1, fill=0)
    # stripes: dashes along the path
    k.c.setStrokeColor(K); k.c.setLineWidth(w); k.c.setLineCap(0); k.c.setDash(w * 0.7, w * 1.0)
    k.c.drawPath(k.path(pts), stroke=1, fill=0); k.c.setDash(); k.c.setLineCap(1)


def gingerbread_house(k, x, y, w):
    """Gingerbread house; (x, y) = bottom centre of the plate."""
    h = w * 0.55
    k.shape(k.arcpts(x, y, w * 0.7, w * 0.1, 0, 360, 30), lw=0.8, fill=Wt, amp=0)
    bx = x - w / 2; by = y + w * 0.03
    k.rect(bx, by, w, h, lw=1.0)
    for i in range(4):  # brick lines
        k.line([(bx, by + h * (0.2 + 0.2 * i)), (bx + w, by + h * (0.2 + 0.2 * i))], lw=0.3, amp=0.2)
    roof = [(bx - w * 0.12, by + h), (x, by + h + w * 0.48), (bx + w * 1.12, by + h)]
    k.shape(roof, lw=1.0, fill=Wt, amp=0)
    k.c.saveState(); k.c.clipPath(k.path(roof, closed=True), stroke=0, fill=0)
    for j in range(6):
        yy = by + h + j * w * 0.08
        for i in range(-8, 9):
            k.shape(k.arcpts(x + i * w * 0.1 + (j % 2) * w * 0.05, yy + w * 0.04, w * 0.05, w * 0.04, 180, 360, 8), lw=0.35, fill=Wt, amp=0)
    k.c.restoreState()
    k.shape(roof, lw=1.0, fill=None, amp=0)
    # icing drips along the eaves
    for i in range(12):
        t = i / 11
        for side in (0, 1):
            px = lerp(bx - w * 0.12, x, t) if side == 0 else lerp(x, bx + w * 1.12, t)
            py = lerp(by + h, by + h + w * 0.48, t) if side == 0 else lerp(by + h + w * 0.48, by + h, t)
            if i % 2 == 0: k.blob(k.arcpts(px, py - 1, 1.6, 2.6, 180, 360, 8), Wt); k.line(k.arcpts(px, py - 1, 1.6, 2.6, 180, 360, 8), lw=0.4, amp=0)
    # door + windows
    dw = w * 0.2
    door = [(x - dw / 2, by), (x - dw / 2, by + h * 0.5)] + k.arcpts(x, by + h * 0.5, dw / 2, dw / 2, 180, 0, 10)[1:] + [(x + dw / 2, by)]
    k.shape(door, lw=0.8, fill=K, amp=0)
    k.circle(x + dw * 0.25, by + h * 0.3, 0.8, lw=0, fill=Wt, stroke=False)
    for sx in (-1, 1):
        wx = x + sx * w * 0.3
        k.rect(wx - w * 0.08, by + h * 0.45, w * 0.16, w * 0.16, lw=0.8, fill=Wt)
        k.line([(wx, by + h * 0.45), (wx, by + h * 0.45 + w * 0.16)], lw=0.5, amp=0)
        k.line([(wx - w * 0.08, by + h * 0.45 + w * 0.08), (wx + w * 0.08, by + h * 0.45 + w * 0.08)], lw=0.5, amp=0)
    for i in range(5):
        k.circle(bx + w * (0.06 + 0.22 * i), by + 2.5, 1.6, lw=0.4, fill=K if i % 2 else Wt)
    candy_cane(k, bx - w * 0.06, by, h * 0.8, facing=-1)
    k.pine(bx + w * 1.12, by, h * 0.9, style="solid", snow=True)
    k.chimney(x + w * 0.22, by + h + w * 0.2, w * 0.09, w * 0.22, smoke=False) if hasattr(k, "chimney") else None


def cookie_plate(k, x, y, w):
    k.shape(k.arcpts(x, y, w * 0.55, w * 0.13, 0, 360, 30), lw=0.9, fill=Wt, amp=0)
    k.shape(k.arcpts(x, y + 1, w * 0.4, w * 0.08, 0, 360, 30), lw=0.4, fill=None, amp=0)
    for (dx, dy, kind) in [(-0.22, 0.08, "star"), (0.18, 0.07, "round"), (-0.02, 0.12, "man"), (0.3, 0.16, "round"), (-0.34, 0.14, "round")]:
        cx, cy = x + dx * w, y + dy * w
        if kind == "star": k.star5(cx, cy + w * 0.06, w * 0.11, fill=Wt, lw=0.7)
        elif kind == "man": gingerbread_man(k, cx, cy, w * 0.32)
        else:
            k.circle(cx, cy + w * 0.05, w * 0.08, lw=0.7, fill=Wt)
            for i in range(4): k.circle(cx + w * 0.04 * math.cos(i * 1.7), cy + w * 0.05 + w * 0.04 * math.sin(i * 1.7), 0.7, lw=0.2, fill=K)


def candle1(k, x, y, h):
    w = h * 0.22
    k.rect(x - w / 2, y, w, h, lw=0.9)
    k.hatch([(x + w * 0.15, y), (x + w / 2, y), (x + w / 2, y + h), (x + w * 0.15, y + h)], angle=90, gap=1.2, lw=0.35)
    k.rect(x - w / 2, y, w, h, lw=0.9, fill=None)
    k.blob(k.arcpts(x - w * 0.3, y + h, w * 0.12, w * 0.4, 180, 360, 8), Wt); k.line(k.arcpts(x - w * 0.3, y + h, w * 0.12, w * 0.4, 180, 360, 8), lw=0.5, amp=0)
    k.line([(x, y + h), (x, y + h + w * 0.25)], lw=0.6, amp=0)
    fl = [(x, y + h + w * 0.2), (x + w * 0.22, y + h + w * 0.5), (x, y + h + w * 1.05), (x - w * 0.22, y + h + w * 0.5)]
    k.shape(k.wob(fl, 0.1, closed=True), lw=0.6, fill=Wt, amp=0)
    k.blob(k.arcpts(x, y + h + w * 0.45, w * 0.08, w * 0.18, 0, 360, 10), K)
    for i in range(8):
        aa = math.pi / 4 * i; r0, r1 = w * 0.75, w * 1.0
        k.c.setStrokeColor(K); k.c.setLineWidth(0.35)
        k.c.line(x + r0 * math.cos(aa), y + h + w * 0.55 + r0 * math.sin(aa), x + r1 * math.cos(aa), y + h + w * 0.55 + r1 * math.sin(aa))

def candles3(k, x, y, h):
    k.shape(k.arcpts(x, y, h * 0.55, h * 0.07, 0, 360, 30), lw=0.8, fill=Wt, amp=0)
    for (dx, hh) in [(-0.3, 0.55), (0.3, 0.45), (0, 0.75)]:
        candle1(k, x + dx * h, y + 1, h * hh)
    holly(k, x - h * 0.42, y + h * 0.03, h * 0.2, ang=10)
    holly(k, x + h * 0.44, y + h * 0.03, h * 0.18, ang=-10)

def mini_tree(k, x, y, h):
    k.xmas_tree(x, y, h, star=True)


def star_burst(k, x, y, r):
    k.star5(x, y, r, fill=Wt, lw=0.9)
    for i in range(10):
        a = math.pi / 5 * i + math.pi / 10
        k.c.setStrokeColor(K); k.c.setLineWidth(0.5)
        k.c.line(x + r * 1.15 * math.cos(a), y + r * 1.15 * math.sin(a), x + r * 1.45 * math.cos(a), y + r * 1.45 * math.sin(a))


def bauble_garland(k, x0, x1, y, sag=12, n=7):
    k.line([(lerp(x0, x1, t), y - sag * math.sin(math.pi * t)) for t in [i / 40 for i in range(41)]], lw=0.8, amp=0)
    for i in range(n):
        t = (i + 0.5) / n
        bx, by = lerp(x0, x1, t), y - sag * math.sin(math.pi * t)
        L = 6 + 5 * (i % 2)
        k.line([(bx, by), (bx, by - L)], lw=0.35, amp=0)
        bauble(k, bx, by - L - 7, 5.5, style=i % 3)


def pine_bough(k, x0, x1, y, droop=6):
    """A horizontal swag of evergreen needles."""
    for i in range(int((x1 - x0) / 3)):
        t = i / ((x1 - x0) / 3); px = lerp(x0, x1, t); py = y - droop * math.sin(math.pi * t)
        for d in (-1, 1):
            k.line([(px, py), (px + 4, py + d * 4.5)], lw=0.4, amp=0)


# ----------------------------------------------------------------------------- scenes
def living_room(k, w, h, big=True):
    """Front cover / frontispiece: tree with star and gifts, fireplace with stockings, snowy window, armchair, cat."""
    floor = h * 0.16
    # wainscot / back wall line
    k.line([(0, floor), (w, floor)], lw=1.0, amp=0.2)
    for i in range(14):
        k.line([(w * i / 14, floor), (w * i / 14 + 6, 0)], lw=0.3, amp=0.1)
    k.rug(w * 0.55, floor * 0.45, w * 0.5, floor * 0.6)
    # window centre-left, high
    k.window_snow(w * 0.36, h * 0.47, w * 0.26, h * 0.32, panes=(2, 3), curtains=True)
    pine_bough(k, w * 0.33, w * 0.65, h * 0.82, droop=8)
    for i in range(5): bauble(k, w * (0.36 + 0.065 * i), h * 0.8 - 8 * math.sin(math.pi * (i + 0.5) / 5) - 8, 3.5, style=i % 3)
    # fireplace right
    fx, fw, fh = w * 0.66, w * 0.3, h * 0.4
    k.fireplace(fx, floor, fw, fh, fire=True, stockings=0)
    for i in range(3):
        stocking(k, fx + fw * (0.1 + 0.32 * i), floor + fh - fh * 0.02, fh * 0.32, pattern=i)
    # mantel things
    my = floor + fh * 1.07
    candles3(k, fx + fw * 0.2, my, fh * 0.2)
    wreath(k, fx + fw * 0.5, my + fh * 0.35, fh * 0.2)
    k.clockface(fx + fw * 0.84, my + fh * 0.1, fh * 0.08) if False else gingerbread_house(k, fx + fw * 0.84, my, fh * 0.2)
    # tree left
    k.xmas_tree(w * 0.17, floor - 2, h * 0.72, star=True)
    gift_pile(k, w * 0.01, floor - 4, w * 0.075)
    # armchair + cat
    k.armchair(w * 0.52, floor - 3, w * 0.2, facing=-1)
    k.cat(w * 0.46, floor - 4, w * 0.09)
    mug2(k, w * 0.63, floor - 3, h * 0.05)


def opener_tree(k, w, h):
    floor = h * 0.12
    k.line([(0, floor), (w, floor)], lw=0.9, amp=0.2)
    k.window_snow(w * 0.62, h * 0.5, w * 0.3, h * 0.34, panes=(2, 3), curtains=False)
    k.xmas_tree(w * 0.36, floor - 2, h * 0.8, star=True)
    gift_pile(k, w * 0.1, floor - 3, w * 0.09)
    gift(k, w * 0.6, floor - 3, w * 0.14, w * 0.1, pattern="dots")
    gift(k, w * 0.76, floor - 3, w * 0.1, w * 0.13, pattern="stripes")
    string_lights(k, w * 0.6, w * 0.95, h * 0.9, sag=10, n=9)
    k.cat(w * 0.88, floor - 3, w * 0.12)


def opener_lane(k, w, h):
    k.moon(w * 0.82, h * 0.86, w * 0.06)
    k.stars(0, h * 0.62, w, h, n=40, avoid=lambda x, y: math.hypot(x - w * 0.82, y - h * 0.86) < w * 0.1)
    k.hills(0, w, h * 0.32, amp=8, n=3)
    k.forest(0, w, h * 0.33, h * 0.08, h * 0.17, 18, style="solid")
    gy = h * 0.18
    k.ground(0, w, gy, drifts=5, depth=gy)
    k.cottage(w * 0.06, gy, w * 0.34, h * 0.3, chimney=True)
    wreath(k, w * 0.06 + w * 0.34 * 0.62, gy + h * 0.15, h * 0.035, bow_=True)
    k.cottage(w * 0.56, gy + 3, w * 0.3, h * 0.27, chimney=True, door_side=0.3)
    k.lamppost(w * 0.47, gy - 6, h * 0.36)
    garl_y = gy + h * 0.36
    k.pine(w * 0.92, gy - 4, h * 0.3, style="solid", snow=True)
    k.footprints([(w * (0.47 + 0.03 * i), gy - 8 - 3 * i) for i in range(8)], size=1.4)
    k.snowman(w * 0.88, gy - 10, h * 0.16)
    k.snowfall(0, gy, w, h * 0.62, n=60)


def opener_kitchen(k, w, h):
    top = h * 0.3
    k.window_snow(w * 0.26, h * 0.5, w * 0.48, h * 0.36, panes=(3, 3), curtains=True)
    bauble_garland(k, w * 0.2, w * 0.8, h * 0.95, sag=10, n=7)
    table(k, w * 0.02, w * 0.98, top, top * 0.9)
    gingerbread_house(k, w * 0.5, top + 1, w * 0.22)
    cookie_plate(k, w * 0.2, top + 2, w * 0.24)
    mug2(k, w * 0.78, top + 1, w * 0.09)
    teapot2(k, w * 0.9, top + 1, w * 0.13) if False else jug(k, w * 0.9, top + 1, w * 0.12)
    for i in range(3): k.star5(w * (0.32 + 0.04 * i), top + 3, 3.5, fill=Wt, lw=0.5)


def opener_hearth(k, w, h):
    floor = h * 0.1
    k.line([(0, floor), (w, floor)], lw=0.9, amp=0.2)
    fx, fw, fh = w * 0.25, w * 0.5, h * 0.5
    k.fireplace(fx, floor, fw, fh, fire=True, stockings=0)
    for i in range(4):
        stocking(k, fx + fw * (0.06 + 0.24 * i), floor + fh - fh * 0.02, fh * 0.3, pattern=i % 3)
    my = floor + fh * 1.07
    pine_bough(k, fx - fw * 0.05, fx + fw * 1.05, my + 2, droop=-1)
    candles3(k, fx + fw * 0.14, my, fh * 0.18)
    wreath(k, fx + fw * 0.5, my + fh * 0.36, fh * 0.22)
    k.snowglobe(fx + fw * 0.86, my, fh * 0.17)
    k.armchair(w * 0.13, floor - 2, w * 0.2, facing=1)
    k.armchair(w * 0.87, floor - 2, w * 0.2, facing=-1)
    k.cat(w * 0.47, floor - 3, w * 0.12)
    mug2(k, w * 0.28, floor - 2, h * 0.04); mug2(k, w * 0.72, floor - 2, h * 0.04)


def opener_eve(k, w, h):
    k.moon(w * 0.2, h * 0.85, w * 0.07)
    k.stars(0, h * 0.5, w, h, n=60, avoid=lambda x, y: math.hypot(x - w * 0.2, y - h * 0.85) < w * 0.1)
    star_burst(k, w * 0.74, h * 0.88, w * 0.035)
    k.mountains(0, w, h * 0.38, [(w * 0.15, h * 0.52), (w * 0.45, h * 0.58), (w * 0.8, h * 0.5)])
    k.forest(0, w, h * 0.3, h * 0.08, h * 0.2, 20, style="line")
    gy = h * 0.16
    k.ground(0, w, gy, drifts=4, depth=gy)
    k.cottage(w * 0.3, gy, w * 0.42, h * 0.33, chimney=True)
    wreath(k, w * 0.3 + w * 0.42 * 0.62, gy + h * 0.17, h * 0.04)
    k.xmas_tree(w * 0.12, gy - 6, h * 0.3, star=True)
    k.pine(w * 0.86, gy - 4, h * 0.26, style="solid", snow=True)
    k.sled(w * 0.8, gy - 12, w * 0.12)
    k.lantern(w * 0.24, gy - 10, h * 0.06)


# ----------------------------------------------------------------------------- small art
def half_title(k, w, h):
    holly(k, w * 0.5, h * 0.42, h * 0.42)
def title_art(k, w, h):
    bauble_garland(k, w * 0.08, w * 0.92, h * 0.8, sag=h * 0.22, n=9)
    for sx in (0.08, 0.92): holly(k, w * sx, h * 0.8, h * 0.18)
def wreath_big(k, w, h): wreath(k, w / 2, h * 0.52, min(w, h) * 0.45)
def glance_art(k, w, h):
    for i in range(5): k.xmas_tree(w * (0.12 + 0.19 * i), h * 0.05, h * (0.55 + 0.08 * (i % 3)), star=(i == 2), baubles=True)
def recipes_art(k, w, h):
    cookie_plate(k, w * 0.32, h * 0.12, w * 0.5)
    jug(k, w * 0.78, h * 0.06, h * 0.55)
def letters_art(k, w, h):
    k.envelope(w * 0.5, h * 0.12, w * 0.55)
    holly(k, w * 0.72, h * 0.62, h * 0.28)
def thanks_art(k, w, h):
    mug2(k, w * 0.3, h * 0.08, h * 0.5); mug2(k, w * 0.62, h * 0.08, h * 0.45)
    gift(k, w * 0.74, h * 0.06, w * 0.16, h * 0.3, pattern="stars")
    holly(k, w * 0.12, h * 0.15, h * 0.3)
def photo_corner(k, w, h):
    holly(k, w * 0.5, h * 0.5, h * 0.42)

def v_wreath(k, w, h): wreath(k, w / 2, h * 0.52, min(w, h) * 0.44)
def v_gifts(k, w, h): gift_pile(k, w * 0.05, h * 0.06, w * 0.27)
def v_stocking(k, w, h):
    stocking(k, w * 0.1, h * 0.9, h * 0.8, pattern=0); stocking(k, w * 0.44, h * 0.86, h * 0.72, pattern=1)
def v_holly(k, w, h): holly(k, w / 2, h * 0.35, h * 0.55)
def v_bells(k, w, h): bells(k, w / 2, h * 0.64, h * 0.55)
def v_baubles(k, w, h):
    pine_bough(k, w * 0.05, w * 0.95, h * 0.9, droop=4)
    for i, (dx, L, r) in enumerate([(0.25, 0.25, 0.16), (0.5, 0.4, 0.19), (0.75, 0.2, 0.14)]):
        k.line([(w * dx, h * 0.9), (w * dx, h * (0.9 - L))], lw=0.4, amp=0)
        bauble(k, w * dx, h * (0.9 - L) - h * r * 1.3, h * r, style=i)
def v_gingerbread(k, w, h):
    gingerbread_man(k, w * 0.32, h * 0.06, h * 0.85); gingerbread_man(k, w * 0.7, h * 0.06, h * 0.7)
def v_canes(k, w, h):
    candy_cane(k, w * 0.38, h * 0.08, h * 0.8, facing=1); candy_cane(k, w * 0.62, h * 0.08, h * 0.8, facing=-1)
    bow(k, w * 0.5, h * 0.45, w * 0.3)
def v_cones(k, w, h):
    for (dx, s, a) in [(0.3, 0.5, 15), (0.55, 0.6, -5), (0.75, 0.45, -20)]: cone(k, w * dx, h * 0.1, h * s, a)
def v_snowman(k, w, h): k.snowman(w / 2, h * 0.06, h * 0.9); k.snowfall(0, 0, w, h, n=18)
def v_cocoa(k, w, h): mug2(k, w * 0.38, h * 0.08, h * 0.45); cookie_plate(k, w * 0.72, h * 0.08, w * 0.32) if False else gingerbread_man(k, w * 0.74, h * 0.08, h * 0.55)
def v_globe(k, w, h): k.snowglobe(w / 2, h * 0.05, w * 0.55)
def v_candles(k, w, h): candles3(k, w / 2, h * 0.06, h * 0.75)
def v_tree(k, w, h): k.xmas_tree(w / 2, h * 0.04, h * 0.84, star=True); gift(k, w * 0.66, h * 0.02, w * 0.18, h * 0.14, pattern="dots")
def v_house(k, w, h): gingerbread_house(k, w / 2, h * 0.08, w * 0.5)

VIGNETTES = ["v-wreath", "v-gifts", "v-stocking", "v-holly", "v-bells", "v-baubles", "v-gingerbread", "v-canes",
             "v-cones", "v-snowman", "v-cocoa", "v-globe", "v-candles", "v-tree", "v-house"]

JOBS = [
    ("cover-scene", 4.9, 4.4, living_room, 50),
    ("frontispiece", 4.5, 4.4, living_room, 2),
    ("half-title", 2.0, 1.3, half_title, 1),
    ("title", 4.2, 1.5, title_art, 3),
    ("belongs", 2.4, 2.4, wreath_big, 4),
    ("opener-1", 4.4, 4.4, opener_tree, 5),
    ("opener-2", 4.4, 4.4, opener_lane, 6),
    ("opener-3", 4.4, 4.0, opener_kitchen, 7),
    ("opener-4", 4.4, 4.2, opener_hearth, 8),
    ("opener-5", 4.4, 4.4, opener_eve, 9),
    ("glance", 4.0, 0.9, glance_art, 10),
    ("recipes", 2.4, 1.2, recipes_art, 11),
    ("letters", 2.0, 1.3, letters_art, 12),
    ("thanks", 3.2, 1.6, thanks_art, 13),
    ("photo-corner", 0.8, 0.6, photo_corner, 14),
    ("v-wreath", 1.3, 1.3, v_wreath, 21), ("v-gifts", 1.5, 1.1, v_gifts, 22), ("v-stocking", 1.3, 1.3, v_stocking, 23),
    ("v-holly", 1.4, 1.0, v_holly, 24), ("v-bells", 1.3, 1.2, v_bells, 25), ("v-baubles", 1.5, 1.2, v_baubles, 26),
    ("v-gingerbread", 1.3, 1.2, v_gingerbread, 27), ("v-canes", 1.2, 1.2, v_canes, 28), ("v-cones", 1.5, 1.0, v_cones, 29),
    ("v-snowman", 1.1, 1.3, v_snowman, 30), ("v-cocoa", 1.4, 1.0, v_cocoa, 31), ("v-globe", 1.1, 1.2, v_globe, 32),
    ("v-candles", 1.3, 1.3, v_candles, 33), ("v-tree", 1.1, 1.4, v_tree, 34), ("v-house", 1.5, 1.2, v_house, 35),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = set(sys.argv[1:])
    for name, wi, hi, fn, seed in JOBS:
        if only and name not in only: continue
        render(os.path.join(OUT, f"{name}.png"), wi, hi, fn, seed=seed, dpi=300)
        print("drew", name)
