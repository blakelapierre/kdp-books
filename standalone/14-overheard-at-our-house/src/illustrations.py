"""Black-and-white ink illustrations for Overheard at Our House -> ../illustrations/*.png
Pure black line art on white at 300 DPI, drawn with the shared inkart house style (inkart.py), the
small home motifs from Two Cups of Tea (motifs.py), a few pieces from Twenty-Five Christmases
(xmotifs.py) and the new toy-box motifs below: speech bubbles, a teddy bear, ABC blocks, a rubber
duck, a paper aeroplane, crayons, balloons, a wagon, a tree swing, a little car and a bed.
No people in any scene. Deterministic: same seeds -> same images. Run from src/: python3 illustrations.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inkart import render, Wt, K, lerp
from motifs import (mug2, table, chair, hanging_lamp, vase, jug, garden_window, kite, songbird, tree,
                    picket, grass, sun, cloud, birds, heart, rocking_chair, apple, flower, daisy, pot, basket)
from xmotifs import gift

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "illustrations")


# ----------------------------------------------------------------------------- toy-box motifs
def bubble(k, x, y, w, h, tail=1, lw=1.0, fill=Wt, mark=None):
    """Rounded speech bubble; (x, y) = bottom-left of the body. tail: +1 tail at lower left, -1 lower right."""
    r = min(w, h) * 0.3
    pts = (k.arcpts(x + w - r, y + r, r, r, -90, 0, 8) + k.arcpts(x + w - r, y + h - r, r, r, 0, 90, 8)
           + k.arcpts(x + r, y + h - r, r, r, 90, 180, 8) + k.arcpts(x + r, y + r, r, r, 180, 270, 8))
    tx = x + w * (0.28 if tail > 0 else 0.72)
    # insert tail into the bottom edge (bottom edge runs from the last arc back to the first)
    tip = (tx - tail * w * 0.14, y - h * 0.3)
    pts = pts + [(tx - w * 0.07, y), tip, (tx + w * 0.07, y)]
    k.shape(pts, lw=lw, fill=fill, amp=0.15)
    if mark == "lines":
        for i in range(3):
            yy = y + h * (0.7 - 0.2 * i); k.line([(x + w * 0.18, yy), (x + w * (0.82 if i < 2 else 0.55), yy)], lw=lw * 0.6, amp=0.1)
    elif mark == "heart":
        heart(k, x + w / 2, y + h * 0.3, min(w, h) * 0.5, fill=K, lw=0.4)
    elif mark == "q":
        k.text(x + w / 2, y + h * 0.22, "?", size=h * 0.7, font="Ink-Playfair")
    elif mark == "!":
        k.text(x + w / 2, y + h * 0.22, "!", size=h * 0.7, font="Ink-Playfair")
    elif mark == "ha":
        k.text(x + w / 2, y + h * 0.3, "ha ha", size=h * 0.42, font="Ink-CrimsonI")
    elif mark == "dots":
        for i in range(3): k.circle(x + w * (0.3 + 0.2 * i), y + h * 0.5, min(w, h) * 0.06, lw=0.3, fill=K)
    return pts


def teddy(k, x, y, h):
    """Sitting teddy bear; (x, y) = centre bottom."""
    s = h
    # legs
    for sx in (-1, 1):
        k.shape(k.arcpts(x + sx * s * 0.2, y + s * 0.1, s * 0.15, s * 0.11, 0, 360, 20), lw=0.9, fill=Wt, amp=0)
        k.shape(k.arcpts(x + sx * s * 0.24, y + s * 0.1, s * 0.07, s * 0.08, 0, 360, 14), lw=0.5, fill=Wt, amp=0)
    body = k.arcpts(x, y + s * 0.32, s * 0.24, s * 0.25, 0, 360, 28)
    k.shape(body, lw=0.9, fill=Wt, amp=0.1)
    k.hatch([p for p in body if p[0] > x + s * 0.06] + [(x + s * 0.06, y + s * 0.1)], angle=70, gap=1.3, lw=0.32)
    k.shape(body, lw=0.9, fill=None, amp=0.1)
    k.shape(k.arcpts(x, y + s * 0.3, s * 0.12, s * 0.13, 0, 360, 20), lw=0.5, fill=Wt, amp=0)
    # arms
    for sx in (-1, 1):
        k.shape(k.arcpts(x + sx * s * 0.25, y + s * 0.34, s * 0.08, s * 0.15, 0, 360, 18), lw=0.9, fill=Wt, amp=0)
    # head and ears
    hy = y + s * 0.7
    for sx in (-1, 1):
        k.circle(x + sx * s * 0.17, hy + s * 0.15, s * 0.08, lw=0.9, fill=Wt)
        k.circle(x + sx * s * 0.17, hy + s * 0.15, s * 0.04, lw=0.4, fill=K)
    k.shape(k.arcpts(x, hy, s * 0.21, s * 0.19, 0, 360, 28), lw=0.9, fill=Wt, amp=0.1)
    k.shape(k.arcpts(x, hy - s * 0.06, s * 0.08, s * 0.06, 0, 360, 16), lw=0.6, fill=Wt, amp=0)
    k.shape(k.arcpts(x, hy - s * 0.035, s * 0.03, s * 0.02, 0, 360, 10), lw=0.3, fill=K, amp=0)
    for sx in (-1, 1): k.circle(x + sx * s * 0.08, hy + s * 0.04, s * 0.022, lw=0.2, fill=K)
    # bow tie
    for sx in (-1, 1):
        k.shape([(x, y + s * 0.53), (x + sx * s * 0.1, y + s * 0.58), (x + sx * s * 0.1, y + s * 0.47)], lw=0.6, fill=K, amp=0)
    k.circle(x, y + s * 0.53, s * 0.025, lw=0.4, fill=Wt)


def block(k, x, y, s, letter="A"):
    """ABC block in simple perspective; (x, y) = front bottom-left."""
    d = s * 0.32
    front = [(x, y), (x + s, y), (x + s, y + s), (x, y + s)]
    top = [(x, y + s), (x + s, y + s), (x + s + d, y + s + d * 0.7), (x + d, y + s + d * 0.7)]
    side = [(x + s, y), (x + s + d, y + d * 0.7), (x + s + d, y + s + d * 0.7), (x + s, y + s)]
    k.shape(front, lw=0.9, fill=Wt, amp=0.1)
    k.shape(top, lw=0.8, fill=Wt, amp=0.1)
    k.shape(side, lw=0.8, fill=Wt, amp=0.1)
    k.hatch(side, angle=90, gap=1.3, lw=0.35)
    k.shape(side, lw=0.8, fill=None, amp=0.1)
    k.rect(x + s * 0.1, y + s * 0.1, s * 0.8, s * 0.8, lw=0.45, fill=None)
    k.text(x + s / 2, y + s * 0.24, letter, size=s * 0.62, font="Ink-Playfair")


def duck(k, x, y, w, facing=1):
    f = facing
    body = [(x - f * w * 0.5, y + w * 0.3)] + [(x + f * (w * 0.45 * math.cos(math.radians(a))), y + w * 0.22 + w * 0.22 * math.sin(math.radians(a))) for a in range(180, 361, 12)] + [(x + f * w * 0.35, y + w * 0.32), (x + f * w * 0.1, y + w * 0.3)]
    k.shape(body, lw=0.9, fill=Wt, amp=0.1)
    k.hatch([p for p in body if p[1] < y + w * 0.16], angle=0, gap=1.2, lw=0.3)
    k.shape(body, lw=0.9, fill=None, amp=0.1)
    k.line(k.arcpts(x - f * w * 0.05, y + w * 0.28, w * 0.18, w * 0.09, 200, 340, 10), lw=0.6, amp=0)
    hx, hy = x + f * w * 0.24, y + w * 0.52
    k.circle(hx, hy, w * 0.17, lw=0.9, fill=Wt)
    k.circle(hx + f * w * 0.05, hy + w * 0.04, w * 0.03, lw=0.2, fill=K)
    k.shape([(hx + f * w * 0.14, hy + w * 0.0), (hx + f * w * 0.34, hy - w * 0.03), (hx + f * w * 0.14, hy - w * 0.08)], lw=0.6, fill=K, amp=0)


def plane(k, x, y, w, ang=10):
    """Folded paper aeroplane centred at (x, y)."""
    a = math.radians(ang)
    def P(u, v): return (x + u * w * math.cos(a) - v * w * math.sin(a), y + u * w * math.sin(a) + v * w * math.cos(a))
    k.shape([P(0.5, 0), P(-0.5, 0.18), P(-0.32, 0.0)], lw=0.8, fill=Wt, amp=0)
    k.shape([P(0.5, 0), P(-0.32, 0.0), P(-0.5, -0.2)], lw=0.8, fill=Wt, amp=0)
    k.hatch([P(0.5, 0), P(-0.32, 0.0), P(-0.5, -0.2)], angle=ang + 90, gap=1.2, lw=0.3)
    k.shape([P(0.5, 0), P(-0.32, 0.0), P(-0.5, -0.2)], lw=0.8, fill=None, amp=0)
    k.shape([P(0.5, 0), P(-0.32, 0.0), P(-0.4, -0.07)], lw=0.6, fill=Wt, amp=0)


def swoosh(k, pts, lw=0.5):
    """Dashed flight path."""
    for i in range(0, len(pts) - 1, 2):
        k.line([pts[i], pts[i + 1]], lw=lw, amp=0)


def crayon(k, x, y, L, ang=0, dark=False):
    a = math.radians(ang); d = L * 0.13
    def P(u, v): return (x + u * math.cos(a) - v * math.sin(a), y + u * math.sin(a) + v * math.cos(a))
    body = [P(0, -d / 2), P(L * 0.8, -d / 2), P(L * 0.8, d / 2), P(0, d / 2)]
    k.shape(body, lw=0.8, fill=K if dark else Wt, amp=0)
    if not dark: k.hatch(body, angle=ang + 90, gap=1.1, lw=0.3)
    k.shape(body, lw=0.8, fill=None, amp=0)
    lab = [P(L * 0.2, -d / 2), P(L * 0.62, -d / 2), P(L * 0.62, d / 2), P(L * 0.2, d / 2)]
    k.shape(lab, lw=0.6, fill=Wt, amp=0)
    for u in (0.28, 0.54): k.line([P(L * u, -d / 2), P(L * u, d / 2)], lw=0.4, amp=0)
    k.shape([P(L * 0.8, -d / 2), P(L, -d * 0.12), P(L, d * 0.12), P(L * 0.8, d / 2)], lw=0.8, fill=K if dark else Wt, amp=0)


def balloon(k, x, y, r, string_to, dark=False, shine=True):
    pts = k.arcpts(x, y, r * 0.85, r, 0, 360, 30)
    k.shape(pts, lw=0.9, fill=K if dark else Wt, amp=0.1)
    if not dark: k.hatch([p for p in pts if p[0] > x + r * 0.2], angle=60, gap=1.3, lw=0.32); k.shape(pts, lw=0.9, fill=None, amp=0.1)
    if shine: k.line(k.arcpts(x, y, r * 0.55, r * 0.65, 115, 160, 6), lw=0.8, amp=0, color=Wt if dark else K)
    k.shape([(x - r * 0.12, y - r - r * 0.16), (x + r * 0.12, y - r - r * 0.16), (x, y - r)], lw=0.5, fill=K, amp=0)
    sx, sy = string_to
    pts = [(lerp(x, sx, t) + r * 0.15 * math.sin(t * 9), lerp(y - r - r * 0.16, sy, t)) for t in [i / 20 for i in range(21)]]
    k.line(pts, lw=0.45, amp=0)


def wagon(k, x, y, w):
    """Little pull wagon; (x, y) = bottom of the wheels at the middle."""
    r = w * 0.13
    for dx in (-0.3, 0.3): k.wheel(x + dx * w, y + r, r, spokes=6)
    bed = [(x - w * 0.46, y + r * 1.3), (x + w * 0.46, y + r * 1.3), (x + w * 0.5, y + r * 1.3 + w * 0.22), (x - w * 0.5, y + r * 1.3 + w * 0.22)]
    k.shape(bed, lw=0.9, fill=Wt, amp=0.1)
    for i in range(1, 4):
        yy = y + r * 1.3 + w * 0.22 * i / 4; k.line([(x - w * 0.48, yy), (x + w * 0.48, yy)], lw=0.4, amp=0.1)
    k.line([(x + w * 0.5, y + r * 1.5), (x + w * 0.8, y + r * 2.4), (x + w * 0.86, y + r * 2.4)], lw=1.0, amp=0)
    k.circle(x + w * 0.88, y + r * 2.4, r * 0.25, lw=0.7, fill=Wt)


def ball(k, x, y, r):
    pts = k.arcpts(x, y + r, r, r, 0, 360, 30)
    k.shape(pts, lw=0.9, fill=Wt, amp=0)
    k.hatch(k.arcpts(x, y + r, r, r, -30, 60, 14) + [(x, y + r)], angle=45, gap=1.2, lw=0.35)
    k.line([(x - r, y + r), (x + r, y + r)], lw=0.6, amp=0)
    k.line(k.arcpts(x, y + r, r * 0.4, r, 90, 270, 16), lw=0.6, amp=0)
    k.shape(pts, lw=0.9, fill=None, amp=0)


def bucket(k, x, y, h):
    w = h * 0.9
    body = [(x - w * 0.38, y), (x + w * 0.38, y), (x + w * 0.5, y + h), (x - w * 0.5, y + h)]
    k.shape(body, lw=0.9, fill=Wt, amp=0.1)
    k.hatch([(x + w * 0.1, y), (x + w * 0.38, y), (x + w * 0.5, y + h), (x + w * 0.15, y + h)], angle=90, gap=1.2, lw=0.32)
    k.shape(body, lw=0.9, fill=None, amp=0.1)
    k.shape(k.arcpts(x, y + h, w * 0.5, h * 0.1, 0, 360, 20), lw=0.8, fill=Wt, amp=0)
    k.c.setStrokeColor(K); k.c.setLineWidth(0.7); k.c.arc(x - w * 0.5, y + h * 0.5, x + w * 0.5, y + h * 1.5, 0, 180)
    k.star5(x - w * 0.05, y + h * 0.45, h * 0.13, fill=K, lw=0.4)


def spade(k, x, y, L, ang=70):
    a = math.radians(ang)
    tip = (x + L * 0.62 * math.cos(a), y + L * 0.62 * math.sin(a))
    k.line([(x, y), tip], lw=1.4, amp=0)
    ex = (x + L * math.cos(a), y + L * math.sin(a))
    k.line([tip, ex], lw=2.2, amp=0)
    nx, ny = -math.sin(a), math.cos(a)
    k.shape([(x + nx * L * 0.12, y + ny * L * 0.12), (x - nx * L * 0.12, y - ny * L * 0.12), (x - L * 0.3 * math.cos(a), y - L * 0.3 * math.sin(a))], lw=0.8, fill=Wt, amp=0)


def swing(k, bx, by, L, w):
    """A board swing hanging from a branch at (bx, by)."""
    for dx in (-w * 0.42, w * 0.42): k.line([(bx + dx, by), (bx + dx, by - L)], lw=0.6, amp=0)
    seat = [(bx - w / 2, by - L), (bx + w / 2, by - L), (bx + w / 2, by - L - w * 0.12), (bx - w / 2, by - L - w * 0.12)]
    k.shape(seat, lw=0.9, fill=Wt, amp=0)
    k.hatch(seat, angle=0, gap=1.0, lw=0.3)
    k.shape(seat, lw=0.9, fill=None, amp=0)


def little_car(k, x, y, w, facing=1):
    """Rounded old-fashioned family car with a suitcase on the roof; (x, y) = road under the middle."""
    f = facing; r = w * 0.11
    X = lambda u: x + f * u * w
    body = [(X(-0.5), y + r * 0.9), (X(0.5), y + r * 0.9), (X(0.52), y + w * 0.2), (X(0.42), y + w * 0.26), (X(0.22), y + w * 0.28),
            (X(0.12), y + w * 0.44), (X(-0.3), y + w * 0.44), (X(-0.42), y + w * 0.28), (X(-0.5), y + w * 0.25)]
    k.shape(body, lw=1.0, fill=Wt, amp=0.12)
    k.hatch([(X(-0.5), y + r * 0.9), (X(0.5), y + r * 0.9), (X(0.52), y + w * 0.14), (X(-0.5), y + w * 0.14)], angle=0, gap=1.4, lw=0.35)
    k.shape(body, lw=1.0, fill=None, amp=0.12)
    # windows
    k.shape([(X(0.08), y + w * 0.29), (X(0.17), y + w * 0.29), (X(0.09), y + w * 0.4), (X(-0.08), y + w * 0.4), (X(-0.08), y + w * 0.29)], lw=0.7, fill=Wt, amp=0)
    k.shape([(X(-0.12), y + w * 0.29), (X(-0.12), y + w * 0.4), (X(-0.28), y + w * 0.4), (X(-0.37), y + w * 0.29)], lw=0.7, fill=Wt, amp=0)
    # a teddy peeking from the back window
    k.circle(X(-0.24), y + w * 0.33, w * 0.035, lw=0.5, fill=Wt)
    for sx in (-1, 1): k.circle(X(-0.24) + sx * w * 0.028, y + w * 0.36, w * 0.014, lw=0.4, fill=Wt)
    k.line([(X(-0.1), y + w * 0.16), (X(-0.1), y + w * 0.27)], lw=0.5, amp=0)
    k.line([(X(-0.02), y + w * 0.2), (X(0.04), y + w * 0.2)], lw=0.8, amp=0)
    k.circle(X(0.47), y + w * 0.2, w * 0.03, lw=0.6, fill=Wt)
    for dx in (-0.3, 0.3): k.wheel(X(dx), y + r, r, spokes=6)
    # suitcase on the roof
    sc = [(X(-0.24), y + w * 0.45), (X(0.04), y + w * 0.45), (X(0.04), y + w * 0.55), (X(-0.24), y + w * 0.55)]
    k.shape(sc, lw=0.8, fill=Wt, amp=0)
    for u in (-0.16, -0.04): k.line([(X(u), y + w * 0.45), (X(u), y + w * 0.55)], lw=0.5, amp=0)
    k.c.setStrokeColor(K); k.c.setLineWidth(0.6); k.c.arc(min(X(-0.13), X(-0.07)), y + w * 0.53, max(X(-0.13), X(-0.07)), y + w * 0.59, 0, 180)


def bed(k, x, y, w):
    """Child's bed with a patchwork quilt; (x, y) = floor at the left foot."""
    h = w * 0.55
    # headboard
    hb = [(x + w * 0.02, y), (x + w * 0.12, y)] + k.arcpts(x + w * 0.07, y + h * 0.85, w * 0.05, h * 0.15, 0, 180, 12)
    k.shape(hb, lw=0.9, fill=Wt, amp=0)
    k.hatch(hb, angle=90, gap=1.6, lw=0.35); k.shape(hb, lw=0.9, fill=None, amp=0)
    k.star5(x + w * 0.07, y + h * 0.78, w * 0.025, fill=Wt, lw=0.5)
    k.shape([(x + w * 0.9, y), (x + w * 0.97, y), (x + w * 0.97, y + h * 0.62), (x + w * 0.9, y + h * 0.62)], lw=0.9, fill=Wt, amp=0)
    mat = [(x + w * 0.12, y + h * 0.18), (x + w * 0.9, y + h * 0.18), (x + w * 0.9, y + h * 0.42), (x + w * 0.12, y + h * 0.42)]
    k.shape(mat, lw=0.9, fill=Wt, amp=0)
    # pillow
    k.shape(k.arcpts(x + w * 0.2, y + h * 0.5, w * 0.09, h * 0.08, 0, 360, 20), lw=0.8, fill=Wt, amp=0.1)
    # quilt
    q = [(x + w * 0.3, y + h * 0.44), (x + w * 0.88, y + h * 0.44), (x + w * 0.88, y + h * 0.1), (x + w * 0.3, y + h * 0.1)]
    k.shape(q, lw=0.9, fill=Wt, amp=0.1)
    cols, rows = 6, 3
    for i in range(cols):
        for j in range(rows):
            x0 = lerp(x + w * 0.3, x + w * 0.88, i / cols); x1 = lerp(x + w * 0.3, x + w * 0.88, (i + 1) / cols)
            y0 = lerp(y + h * 0.1, y + h * 0.44, j / rows); y1 = lerp(y + h * 0.1, y + h * 0.44, (j + 1) / rows)
            cell = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
            m = (i + j) % 3
            if m == 0: k.hatch(cell, angle=45, gap=1.3, lw=0.3)
            elif m == 1: k.circle((x0 + x1) / 2, (y0 + y1) / 2, min(x1 - x0, y1 - y0) * 0.2, lw=0.4, fill=K)
    for i in range(1, cols): xx = lerp(x + w * 0.3, x + w * 0.88, i / cols); k.line([(xx, y + h * 0.1), (xx, y + h * 0.44)], lw=0.4, amp=0)
    for j in range(1, rows): yy = lerp(y + h * 0.1, y + h * 0.44, j / rows); k.line([(x + w * 0.3, yy), (x + w * 0.88, yy)], lw=0.4, amp=0)
    k.shape(q, lw=0.9, fill=None, amp=0.1)
    for xx in (x + w * 0.12, x + w * 0.88): k.line([(xx, y), (xx, y + h * 0.18)], lw=1.2, amp=0)


def toy_stack(k, x, y, s):
    block(k, x, y, s, "A"); block(k, x + s * 1.15, y, s, "B"); block(k, x + s * 0.55, y + s * 1.0, s, "C")


# ----------------------------------------------------------------------------- scenes
def opener_kitchen(k, w, h):
    """Around the Kitchen Table."""
    floor = h * 0.06
    garden_window(k, w * 0.27, h * 0.5, w * 0.46, h * 0.36, view="spring")
    hanging_lamp(k, w * 0.12, h, h * 0.14, w * 0.11)
    hanging_lamp(k, w * 0.88, h, h * 0.14, w * 0.11)
    top = h * 0.36
    chair(k, w * 0.1, floor, w * 0.16, facing=1)
    chair(k, w * 0.9, floor, w * 0.16, facing=-1)
    table(k, w * 0.14, w * 0.86, top, top - floor)
    jug(k, w * 0.27, top + 1, w * 0.09)
    vase(k, w * 0.5, top + 1, w * 0.12)
    mug2(k, w * 0.66, top + 1, w * 0.07)
    for i in range(3): apple(k, w * (0.36 + 0.035 * i), top + 4, 4, dark=(i == 1))
    crayon(k, w * 0.72, top + 2, w * 0.1, ang=0); crayon(k, w * 0.74, top + 5, w * 0.09, ang=8, dark=True)
    k.line([(0, floor), (w, floor)], lw=0.9, amp=0.2)
    k.cat(w * 0.5, floor - 2, w * 0.12)
    block(k, w * 0.28, floor - 1, w * 0.05, "A"); block(k, w * 0.66, floor - 1, w * 0.05, "Z")
    bubble(k, w * 0.04, h * 0.66, w * 0.15, h * 0.08, tail=1, mark="!")
    bubble(k, w * 0.8, h * 0.6, w * 0.16, h * 0.08, tail=-1, mark="q")


def opener_road(k, w, h):
    """On the Way There."""
    sun(k, w * 0.82, h * 0.84, w * 0.05)
    cloud(k, w * 0.25, h * 0.86, w * 0.22); cloud(k, w * 0.55, h * 0.92, w * 0.15)
    birds(k, [(w * 0.4, h * 0.78), (w * 0.47, h * 0.81), (w * 0.62, h * 0.76)], s=4)
    pts = k.hills(0, w, h * 0.5, amp=10, n=3)
    k.shape([(0, h * 0.2)] + pts + [(w, h * 0.2)], lw=0.8, fill=Wt, amp=0)
    tree(k, w * 0.12, h * 0.42, h * 0.28, kind="leafy")
    tree(k, w * 0.86, h * 0.44, h * 0.22, kind="blossom")
    tree(k, w * 0.66, h * 0.47, h * 0.14, kind="leafy")
    # winding road
    roadL = [(w * lerp(0.42, 0.0, t) + w * 0.08 * math.sin(t * 3), lerp(h * 0.47, 0, t)) for t in [i / 30 for i in range(31)]]
    roadR = [(w * lerp(0.47, 0.75, t) + w * 0.08 * math.sin(t * 3), lerp(h * 0.47, 0, t)) for t in [i / 30 for i in range(31)]]
    k.shape(roadL + list(reversed(roadR)), lw=0.9, fill=Wt, amp=0.1)
    for i in range(3, 30, 4):
        a = [((roadL[i][0] + roadR[i][0]) / 2, roadL[i][1]), ((roadL[i + 1][0] + roadR[i + 1][0]) / 2, roadL[i + 1][1])]
        k.line(a, lw=0.9 + i * 0.05, amp=0)
    picket(k, w * 0.74, w * 1.0, h * 0.24, h * 0.07)
    grass(k, 0, w * 0.3, h * 0.12, n=30, hmax=5)
    for i in range(5): flower(k, w * (0.05 + 0.05 * i), h * (0.06 + 0.03 * (i % 2)), 3)
    k.signpost(w * 0.86, h * 0.06, w * 0.18, text="PICNIC")
    little_car(k, w * 0.38, h * 0.1, w * 0.4, facing=1)
    bubble(k, w * 0.08, h * 0.46, w * 0.16, h * 0.075, tail=-1, mark="q")
    bubble(k, w * 0.58, h * 0.6, w * 0.22, h * 0.075, tail=1, mark="dots")


def opener_garden(k, w, h):
    """Out in the Garden."""
    gy = h * 0.14
    cloud(k, w * 0.68, h * 0.9, w * 0.2)
    sun(k, w * 0.9, h * 0.9, w * 0.04)
    # big tree with a swing
    tx = w * 0.26; th = h * 0.62
    tree(k, tx, gy, th, kind="leafy")
    by = gy + th * 0.5
    k.shape([(tx, by - 3), (tx + w * 0.34, by + 3), (tx + w * 0.35, by + 6), (tx, by + 3)], lw=0.9, fill=Wt, amp=0.2)
    swing(k, tx + w * 0.25, by + 2, by - gy - h * 0.22, w * 0.12)
    kite(k, w * 0.74, h * 0.72, w * 0.12, tail_to=(w * 0.62, h * 0.4))
    picket(k, w * 0.48, w, gy + 2, h * 0.11)
    k.line([(0, gy), (w, gy)], lw=0.9, amp=0.3)
    grass(k, 0, w, gy, n=70, hmax=6)
    wagon(k, w * 0.66, gy - 6, w * 0.22)
    ball(k, w * 0.48, gy - 8, w * 0.04)
    bucket(k, w * 0.9, gy - 10, w * 0.07)
    spade(k, w * 0.82, gy - 10, w * 0.1, ang=75)
    for i in range(6): daisy(k, w * (0.05 + 0.07 * i), gy - 12 - 4 * (i % 2), 3.2)
    songbird(k, w * 0.6, gy + h * 0.12 + 2, 4)
    bubble(k, w * 0.6, h * 0.36, w * 0.17, h * 0.075, tail=1, mark="!")


def opener_bedtime(k, w, h):
    """At Bedtime."""
    floor = h * 0.1
    # window with moon and stars
    wx, wy, ww, wh = w * 0.52, h * 0.5, w * 0.38, h * 0.36
    k.rect(wx - 4, wy - 4, ww + 8, wh + 8, lw=1.1)
    k.rect(wx, wy, ww, wh, lw=0.8, fill=K)
    k.c.saveState(); p = k.c.beginPath(); p.rect(wx, wy, ww, wh); k.c.clipPath(p, stroke=0, fill=0)
    for i in range(22):
        k.sparkle(k.r.uniform(wx + 3, wx + ww - 3), k.r.uniform(wy + 3, wy + wh - 3), k.r.uniform(1.2, 2.8), fill=Wt)
    k.circle(wx + ww * 0.7, wy + wh * 0.72, ww * 0.12, lw=0, fill=Wt, stroke=False)
    k.circle(wx + ww * 0.76, wy + wh * 0.76, ww * 0.11, lw=0, fill=K, stroke=False)
    k.c.restoreState()
    k.c.setStrokeColor(Wt); k.c.setLineWidth(1.6); k.c.line(wx + ww / 2, wy, wx + ww / 2, wy + wh); k.c.line(wx, wy + wh / 2, wx + ww, wy + wh / 2)
    k.rect(wx - 7, wy - 8, ww + 14, 4.5, lw=0.9)
    # bunting of stars over the bed
    pts = [(lerp(w * 0.04, w * 0.46, t), h * 0.88 - h * 0.05 * math.sin(math.pi * t)) for t in [i / 30 for i in range(31)]]
    k.line(pts, lw=0.5, amp=0)
    for i in range(1, 6):
        t = i / 6; k.star5(lerp(w * 0.04, w * 0.46, t), h * 0.86 - h * 0.05 * math.sin(math.pi * t), 5, fill=K if i % 2 else Wt, lw=0.5)
    k.line([(0, floor), (w, floor)], lw=0.9, amp=0.2)
    bed(k, w * 0.02, floor, w * 0.56)
    teddy(k, w * 0.4, floor + w * 0.56 * 0.55 * 0.44, w * 0.14)
    k.books(w * 0.6, floor, w * 0.14, n=4)
    k.floor_lamp(w * 0.86, floor, h * 0.42)
    k.rug(w * 0.62, floor - 10, w * 0.32, 8)
    duck(k, w * 0.73, floor - 1, w * 0.06)
    bubble(k, w * 0.08, h * 0.62, w * 0.16, h * 0.075, tail=1, mark="heart")


def frontispiece(k, w, h):
    """The house with a garden full of toys."""
    gy = h * 0.2
    cloud(k, w * 0.2, h * 0.88, w * 0.22); sun(k, w * 0.86, h * 0.86, w * 0.05)
    birds(k, [(w * 0.5, h * 0.84), (w * 0.57, h * 0.87)], s=4)
    tree(k, w * 0.12, gy, h * 0.55, kind="blossom")
    k.cottage(w * 0.3, gy, w * 0.46, h * 0.36, chimney=True)
    tree(k, w * 0.88, gy, h * 0.4, kind="leafy")
    picket(k, 0, w, gy - 14, h * 0.07)
    k.line([(0, gy - 14), (w, gy - 14)], lw=0.9, amp=0.3)
    grass(k, 0, w, gy - 14, n=60, hmax=5)
    wagon(k, w * 0.24, gy - 30, w * 0.16)
    ball(k, w * 0.5, gy - 30, w * 0.03)
    k.cat(w * 0.66, gy - 28, w * 0.1)
    bucket(k, w * 0.82, gy - 30, w * 0.05)
    bubble(k, w * 0.6, h * 0.74, w * 0.16, h * 0.07, tail=1, mark="ha")


def cover_scene(k, w, h):
    """Front cover: the kitchen table, toys and speech bubbles."""
    garden_window(k, w * 0.22, h * 0.46, w * 0.56, h * 0.4, view="spring")
    top = h * 0.3
    table(k, w * 0.04, w * 0.96, top, h * 0.24)
    jug(k, w * 0.2, top + 1, w * 0.1)
    vase(k, w * 0.5, top + 1, w * 0.11)
    mug2(k, w * 0.66, top + 1, w * 0.08)
    teddy(k, w * 0.84, top + 1, w * 0.17)
    toy_stack(k, w * 0.28, top + 1, w * 0.055)
    crayon(k, w * 0.56, top + 2, w * 0.09, ang=0)
    bubble(k, w * 0.02, h * 0.72, w * 0.17, h * 0.09, tail=1, mark="!")
    bubble(k, w * 0.82, h * 0.74, w * 0.16, h * 0.09, tail=-1, mark="q")
    bubble(k, w * 0.05, h * 0.48, w * 0.13, h * 0.075, tail=1, mark="heart")
    bubble(k, w * 0.83, h * 0.5, w * 0.14, h * 0.075, tail=-1, mark="dots")
    k.line([(0, h * 0.06), (w, h * 0.06)], lw=0.9, amp=0.2)
    plane(k, w * 0.5, h * 0.93, w * 0.1, ang=8)
    swoosh(k, [(w * (0.2 + 0.025 * i), h * (0.9 + 0.025 * math.sin(i * 0.5))) for i in range(10)])


# ----------------------------------------------------------------------------- small art
def half_title(k, w, h): bubble(k, w * 0.3, h * 0.3, w * 0.4, h * 0.55, tail=1, mark="heart")
def title_art(k, w, h):
    toy_stack(k, w * 0.08, h * 0.08, h * 0.24)
    duck(k, w * 0.6, h * 0.06, h * 0.42)
    teddy(k, w * 0.44, h * 0.05, h * 0.85)
    plane(k, w * 0.27, h * 0.8, h * 0.36, ang=12)
    crayon(k, w * 0.7, h * 0.08, h * 0.55, ang=0); crayon(k, w * 0.71, h * 0.22, h * 0.5, ang=6, dark=True)
    balloon(k, w * 0.92, h * 0.68, h * 0.18, (w * 0.9, h * 0.06))
def belongs_art(k, w, h):
    teddy(k, w * 0.5, h * 0.04, h * 0.66)
    bubble(k, w * 0.6, h * 0.66, w * 0.34, h * 0.24, tail=1, mark="heart")
def speakers_art(k, w, h):
    for i, m in enumerate(["!", "heart", "q", "ha"]):
        bubble(k, w * (0.02 + 0.25 * i), h * (0.3 + 0.12 * (i % 2)), w * 0.2, h * 0.45, tail=1 if i % 2 else -1, mark=m)
def dictionary_art(k, w, h):
    k.book(w * 0.4, h * 0.08, w * 0.5, open_=True)
    k.pencil(w * 0.68, h * 0.2, w * 0.3, ang=25)
def questions_art(k, w, h):
    k.moon(w * 0.25, h * 0.6, h * 0.25)
    k.stars(w * 0.4, h * 0.2, w, h, n=14)
    bubble(k, w * 0.5, h * 0.18, w * 0.3, h * 0.5, tail=1, mark="q")
def sure_art(k, w, h):
    for i, (dx, dk) in enumerate([(0.3, False), (0.5, True), (0.7, False)]):
        balloon(k, w * dx, h * (0.62 + 0.1 * (i % 2)), h * 0.18, (w * 0.5, h * 0.05), dark=dk)
def jokes_art(k, w, h):
    bubble(k, w * 0.1, h * 0.35, w * 0.4, h * 0.5, tail=1, mark="ha")
    duck(k, w * 0.72, h * 0.06, w * 0.28, facing=-1)
def talk_art(k, w, h):
    mug2(k, w * 0.32, h * 0.06, h * 0.42); mug2(k, w * 0.62, h * 0.06, h * 0.36)
    bubble(k, w * 0.08, h * 0.6, w * 0.3, h * 0.32, tail=1, mark="dots")
    bubble(k, w * 0.6, h * 0.62, w * 0.3, h * 0.32, tail=-1, mark="heart")
def letters_art(k, w, h):
    k.envelope(w * 0.42, h * 0.12, w * 0.5)
    heart(k, w * 0.78, h * 0.62, h * 0.3, fill=K)
def thanks_art(k, w, h):
    teddy(k, w * 0.3, h * 0.04, h * 0.82)
    toy_stack(k, w * 0.48, h * 0.04, h * 0.2)
    balloon(k, w * 0.82, h * 0.66, h * 0.16, (w * 0.78, h * 0.04))
    bubble(k, w * 0.02, h * 0.62, w * 0.16, h * 0.28, tail=-1, mark="heart")

def v_teddy(k, w, h): teddy(k, w / 2, h * 0.04, h * 0.9)
def v_blocks(k, w, h): toy_stack(k, w * 0.14, h * 0.06, h * 0.36)
def v_duck(k, w, h): duck(k, w * 0.45, h * 0.1, w * 0.6); k.line([(w * 0.05, h * 0.12), (w * 0.95, h * 0.12)], lw=0.5, amp=0.4)
def v_plane(k, w, h):
    plane(k, w * 0.62, h * 0.66, w * 0.5, ang=14)
    swoosh(k, [(w * (0.05 + 0.04 * i), h * (0.2 + 0.03 * i + 0.06 * math.sin(i * 0.8))) for i in range(10)])
def v_crayons(k, w, h):
    for i, (a, d) in enumerate([(14, False), (6, True), (-2, False)]): crayon(k, w * (0.1 + 0.04 * i), h * (0.16 + 0.22 * i), w * 0.72, ang=a, dark=d)
def v_balloons(k, w, h):
    balloon(k, w * 0.35, h * 0.62, h * 0.2, (w * 0.5, h * 0.04)); balloon(k, w * 0.65, h * 0.7, h * 0.2, (w * 0.5, h * 0.04), dark=True)
def v_wagon(k, w, h): wagon(k, w * 0.42, h * 0.08, w * 0.62); ball(k, w * 0.38, h * 0.08 + w * 0.62 * 0.36, w * 0.06)
def v_kite(k, w, h): kite(k, w * 0.5, h * 0.5, w * 0.22)
def v_bucket(k, w, h): bucket(k, w * 0.36, h * 0.06, h * 0.5); spade(k, w * 0.7, h * 0.3, h * 0.6, ang=80)
def v_books(k, w, h): k.books(w * 0.5, h * 0.08, w * 0.6, n=4)
def v_cat(k, w, h): k.cat(w * 0.5, h * 0.06, w * 0.7)
def v_bird(k, w, h): songbird(k, w * 0.5, h * 0.4, w * 0.18); k.line([(w * 0.1, h * 0.12), (w * 0.9, h * 0.16)], lw=1.4, amp=0.3)
def v_car(k, w, h): little_car(k, w * 0.5, h * 0.06, w * 0.86); k.line([(0, h * 0.06), (w, h * 0.06)], lw=0.6, amp=0.2)
def v_bed(k, w, h): k.moon(w * 0.5, h * 0.55, h * 0.3); k.stars(0, 0, w, h, n=10, avoid=lambda x, y: math.hypot(x - w * 0.5, y - h * 0.55) < h * 0.38)
def v_mug(k, w, h): mug2(k, w * 0.38, h * 0.06, h * 0.55); apple(k, w * 0.74, h * 0.14, h * 0.12)
def v_gift(k, w, h): gift(k, w * 0.25, h * 0.04, w * 0.5, h * 0.5, pattern="dots")

VIGNETTES = ["v-teddy", "v-blocks", "v-duck", "v-plane", "v-crayons", "v-balloons", "v-wagon", "v-kite", "v-bucket",
             "v-books", "v-cat", "v-bird", "v-car", "v-bed", "v-mug", "v-gift"]

JOBS = [
    ("cover-scene", 4.9, 4.4, cover_scene, 50),
    ("frontispiece", 4.5, 4.4, frontispiece, 2),
    ("half-title", 2.0, 1.3, half_title, 1),
    ("title", 4.2, 1.5, title_art, 3),
    ("belongs", 2.4, 2.4, belongs_art, 4),
    ("speakers", 4.2, 0.9, speakers_art, 15),
    ("opener-1", 4.4, 4.2, opener_kitchen, 5),
    ("opener-2", 4.4, 4.2, opener_road, 6),
    ("opener-3", 4.4, 4.2, opener_garden, 7),
    ("opener-4", 4.4, 4.2, opener_bedtime, 8),
    ("dictionary", 2.2, 1.1, dictionary_art, 10),
    ("questions", 2.4, 1.1, questions_art, 11),
    ("sure", 2.0, 1.2, sure_art, 16),
    ("jokes", 2.2, 1.1, jokes_art, 17),
    ("talk", 2.2, 1.1, talk_art, 18),
    ("letters", 2.0, 1.3, letters_art, 12),
    ("thanks", 3.2, 1.6, thanks_art, 13),
] + [(v, 1.4, 1.2, globals()[v.replace("-", "_")], 21 + i) for i, v in enumerate(VIGNETTES)]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = set(sys.argv[1:])
    for name, wi, hi, fn, seed in JOBS:
        if only and name not in only: continue
        render(os.path.join(OUT, f"{name}.png"), wi, hi, fn, seed=seed, dpi=300)
        print("drew", name)
