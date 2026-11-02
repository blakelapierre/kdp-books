"""Black-and-white ink illustrations for The Thimble Hill Word Search Mysteries -> ../illustrations/*.png
(300 DPI, pure black line art on white, deterministic). Run from src/: python3 illustrations.py [names]"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inkart import render, Wt, K, lerp
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "illustrations")


# ------------------------------------------------------------------ village pieces (summer, no snow)
def roof(k, x0, x1, yb, yp, oh=3):
    xm = (x0 + x1) / 2
    pts = [(x0 - oh, yb), (xm, yp), (x1 + oh, yb)]
    k.shape(pts, lw=0.9, fill=Wt, amp=0.15)
    k.hatch([(xm, yp), (x1 + oh, yb), (xm + (x1 - x0) * 0.08, yb)], angle=-35, gap=1.6, lw=0.35)
    for i in range(1, 5):
        t = i / 5
        k.line([(lerp(xm, x0 - oh, t), lerp(yp, yb, t)), (lerp(xm, x1 + oh, t), lerp(yp, yb, t))], lw=0.3, amp=0.2)


def house(k, x, y, w, h, sign=None, door=0.6, chimney=True, smoke=True, flowers=True):
    k.wall(x, y, w, h * 0.6, gap=2.8)
    roof(k, x, x + w, y + h * 0.6, y + h)
    if chimney:
        cx = x + w * 0.7
        k.rect(cx, y + h * 0.78, w * 0.1, h * 0.26, lw=0.8)
        k.hatch([(cx, y + h * 0.78), (cx + w * 0.1, y + h * 0.78), (cx + w * 0.1, y + h * 1.04), (cx, y + h * 1.04)], angle=0, gap=1.6, lw=0.35)
        if smoke: k.smoke(cx + w * 0.05, y + h * 1.06, h * 0.35, curl=1)
    k.window(x + w * 0.12, y + h * 0.2, w * 0.24, h * 0.22)
    dx = x + w * door
    k.shape([(dx, y), (dx + w * 0.2, y), (dx + w * 0.2, y + h * 0.4), (dx, y + h * 0.4)], lw=0.7, fill=K, amp=0)
    k.circle(dx + w * 0.16, y + h * 0.2, 0.8, lw=0.3, fill=Wt)
    if flowers:
        for i in range(5):
            fx = x + w * (0.1 + 0.07 * i)
            k.line([(fx, y), (fx, y + h * 0.1)], lw=0.4, amp=0); k.circle(fx, y + h * 0.11, 1.3, lw=0.4, fill=Wt if i % 2 else K)
    if sign:
        sw = w * 0.7; sx = x + (w - sw) / 2; sy = y + h * 0.62 - h * 0.13
        k.rect(sx, sy, sw, h * 0.11, lw=0.8)
        k.text(sx + sw / 2, sy + h * 0.025, sign, size=min(h * 0.075, sw / max(4, len(sign)) * 1.45), font="Ink-Playfair")


def tree(k, x, y, h):
    k.shape([(x - h * 0.04, y), (x + h * 0.04, y), (x + h * 0.03, y + h * 0.45), (x - h * 0.03, y + h * 0.45)], lw=0.7, fill=Wt, amp=0.1)
    k.hatch([(x, y), (x + h * 0.04, y), (x + h * 0.03, y + h * 0.45), (x, y + h * 0.45)], angle=90, gap=1.2, lw=0.3)
    for (u, v, r) in [(0, 0.72, 0.26), (-0.17, 0.58, 0.18), (0.18, 0.6, 0.19), (0, 0.9, 0.16)]:
        q = k.arcpts(x + u * h, y + v * h, r * h, r * h * 0.85, 0, 360, 26)
        k.shape(q, lw=0.8, fill=Wt, amp=0.6)
    for i in range(14):
        a = k.r.uniform(0, 6.28); rr = k.r.uniform(0, h * 0.25)
        px, py = x + rr * math.cos(a), y + h * 0.72 + rr * math.sin(a) * 0.8
        k.c.setLineWidth(0.35); k.c.arc(px - 2, py - 1, px + 2, py + 2, 200, 140)


def dog(k, x, y, w, facing=1, sit=False):
    """Pickle, a scruffy little terrier. (x, y) is between the feet."""
    f = facing; X = lambda u: x + f * u * w; h = w * 0.7
    body = [(X(-0.38), y + h * 0.35), (X(-0.4), y + h * 0.62), (X(-0.1), y + h * 0.7), (X(0.28), y + h * 0.68), (X(0.34), y + h * 0.42), (X(0.18), y + h * 0.32), (X(-0.3), y + h * 0.3)]
    for u in (-0.32, -0.2, 0.14, 0.26):
        k.shape([(X(u - 0.05), y + h * 0.4), (X(u + 0.05), y + h * 0.4), (X(u + 0.05), y), (X(u - 0.05), y)], lw=0.7, fill=Wt, amp=0.05)
        k.line([(X(u - 0.06), y), (X(u + 0.07), y)], lw=1.0, amp=0)
    k.shape(body, lw=0.9, fill=Wt, amp=0.35)
    for i in range(9):
        u = lerp(-0.34, 0.28, i / 8)
        k.line([(X(u), y + h * 0.33), (X(u - 0.02), y + h * 0.26)], lw=0.4, amp=0)
    k.hatch([(X(-0.15), y + h * 0.66), (X(0.2), y + h * 0.66), (X(0.2), y + h * 0.48), (X(-0.15), y + h * 0.48)], angle=60, gap=1.4, lw=0.35)
    k.line([(X(-0.38), y + h * 0.6), (X(-0.5), y + h * 0.92), (X(-0.46), y + h * 0.98)], lw=1.3, amp=0.1)
    head = [(X(0.22), y + h * 0.62), (X(0.24), y + h * 0.95), (X(0.42), y + h * 1.02), (X(0.56), y + h * 0.88), (X(0.6), y + h * 0.72), (X(0.42), y + h * 0.62)]
    k.shape(head, lw=0.9, fill=Wt, amp=0.3)
    k.shape([(X(0.27), y + h * 0.95), (X(0.25), y + h * 1.15), (X(0.38), y + h * 1.0)], lw=0.8, fill=K, amp=0)
    k.circle(X(0.6), y + h * 0.78, w * 0.035, lw=0.5, fill=K)
    k.circle(X(0.44), y + h * 0.86, w * 0.022, lw=0.4, fill=K)
    for i in range(4): k.line([(X(0.5 + 0.02 * i), y + h * 0.7), (X(0.48 + 0.025 * i), y + h * 0.6)], lw=0.4, amp=0)
    k.shape([(X(0.22), y + h * 0.7), (X(0.32), y + h * 0.66), (X(0.32), y + h * 0.62), (X(0.22), y + h * 0.65)], lw=0.5, fill=K, amp=0)


def lady(k, x, y, h, facing=1):
    """Hattie Bloom: long skirt, cardigan, hair bun, knitting bag."""
    f = facing; X = lambda u: x + f * u * h
    skirt = [(X(-0.16), y), (X(0.16), y), (X(0.09), y + h * 0.5), (X(-0.09), y + h * 0.5)]
    k.shape(skirt, lw=0.9, fill=Wt, amp=0.1)
    k.hatch(skirt, angle=80, gap=1.6, lw=0.3)
    k.line([(X(-0.05), y), (X(-0.05), y - 0.5)], lw=1.4, amp=0); k.line([(X(0.05), y), (X(0.05), y - 0.5)], lw=1.4, amp=0)
    torso = [(X(-0.1), y + h * 0.48), (X(0.1), y + h * 0.48), (X(0.08), y + h * 0.78), (X(-0.08), y + h * 0.78)]
    k.shape(torso, lw=0.9, fill=Wt, amp=0.05)
    for i in range(4): k.circle(X(0.0), y + h * (0.53 + 0.06 * i), 0.6, lw=0.3, fill=K)
    k.line([(X(0.08), y + h * 0.76), (X(0.16), y + h * 0.58), (X(0.2), y + h * 0.5)], lw=1.2, amp=0)
    k.line([(X(-0.08), y + h * 0.76), (X(-0.12), y + h * 0.6), (X(-0.1), y + h * 0.48)], lw=1.2, amp=0)
    bag = [(X(0.12), y + h * 0.48), (X(0.3), y + h * 0.48), (X(0.28), y + h * 0.32), (X(0.14), y + h * 0.32)]
    k.shape(bag, lw=0.8, fill=Wt, amp=0); k.c.setLineWidth(0.6); k.c.arc(min(X(0.15), X(0.27)), y + h * 0.42, max(X(0.15), X(0.27)), y + h * 0.56, 0, 180)
    k.circle(X(0.24), y + h * 0.53, h * 0.035, lw=0.6, fill=Wt)
    k.line([(X(0.2), y + h * 0.5), (X(0.3), y + h * 0.62)], lw=0.5, amp=0); k.line([(X(0.25), y + h * 0.5), (X(0.32), y + h * 0.6)], lw=0.5, amp=0)
    k.circle(X(0.0), y + h * 0.86, h * 0.075, lw=0.9, fill=Wt)
    k.circle(X(-0.06), y + h * 0.94, h * 0.045, lw=0.6, fill=K)
    k.spectacles(X(0.02), y + h * 0.86, h * 0.09)


def jar(k, x, y, w, label=None):
    h = w * 1.25
    k.shape([(x - w / 2, y), (x + w / 2, y), (x + w / 2, y + h * 0.8), (x - w / 2, y + h * 0.8)], lw=0.9, fill=Wt, amp=0)
    k.hatch([(x + w * 0.15, y), (x + w / 2, y), (x + w / 2, y + h * 0.8), (x + w * 0.15, y + h * 0.8)], angle=75, gap=1.4, lw=0.35)
    lid = [(x - w * 0.56, y + h * 0.8), (x + w * 0.56, y + h * 0.8), (x + w * 0.5, y + h), (x - w * 0.5, y + h)]
    k.shape(lid, lw=0.8, fill=Wt, amp=0.1); k.hatch(lid, angle=0, gap=1.0, lw=0.3, cross=True)
    k.rect(x - w * 0.36, y + h * 0.25, w * 0.72, h * 0.3, lw=0.6)
    if label: k.text(x, y + h * 0.33, label, size=w * 0.2, font="Ink-Plex")


def rosette(k, x, y, r):
    for i in range(14):
        a = 2 * math.pi * i / 14
        q = k.arcpts(x + r * 0.6 * math.cos(a), y + r * 0.6 * math.sin(a), r * 0.42, r * 0.42, 0, 360, 12)
        k.shape(q, lw=0.5, fill=Wt, amp=0)
    k.circle(x, y, r * 0.55, lw=0.8, fill=Wt); k.circle(x, y, r * 0.38, lw=0.5, fill=K)
    for sx in (-1, 1): k.shape([(x + sx * r * 0.1, y - r * 0.5), (x + sx * r * 0.55, y - r * 1.9), (x + sx * r * 0.32, y - r * 1.75), (x + sx * r * 0.2, y - r * 1.95), (x + sx * r * 0.0, y - r * 0.5)], lw=0.6, fill=Wt, amp=0)


def pie(k, x, y, w):
    k.shape(k.arcpts(x, y, w * 0.58, w * 0.1, 0, 360, 26), lw=0.8, fill=Wt, amp=0)
    dome = k.arcpts(x, y + w * 0.06, w / 2, w * 0.26, 0, 180, 26)
    k.shape(dome, lw=0.9, fill=Wt, amp=0)
    for i in range(-3, 4):
        k.line([(x + i * w * 0.12 - w * 0.06, y + w * 0.08), (x + i * w * 0.12 + w * 0.06, y + w * 0.06 + w * 0.26 * math.cos(i * 0.4))], lw=0.4, amp=0)
    for i in range(3):
        k.c.setLineWidth(0.6); k.c.arc(x - w * 0.15 + i * w * 0.1, y + w * 0.36 + i * 3, x - w * 0.08 + i * w * 0.1, y + w * 0.46 + i * 3, 0, 180)


def gnome(k, x, y, h):
    w = h * 0.5
    k.shape([(x - w * 0.45, y), (x + w * 0.45, y), (x + w * 0.35, y + h * 0.45), (x - w * 0.35, y + h * 0.45)], lw=0.9, fill=Wt, amp=0.1)
    k.hatch([(x + w * 0.1, y), (x + w * 0.45, y), (x + w * 0.35, y + h * 0.45), (x + w * 0.1, y + h * 0.45)], angle=70, gap=1.4, lw=0.35)
    k.line([(x - w * 0.45, y + h * 0.12), (x + w * 0.45, y + h * 0.12)], lw=1.4, amp=0)
    beard = [(x - w * 0.36, y + h * 0.58), (x + w * 0.36, y + h * 0.58), (x + w * 0.2, y + h * 0.26), (x, y + h * 0.16), (x - w * 0.2, y + h * 0.26)]
    k.shape(beard, lw=0.8, fill=Wt, amp=0.5)
    k.circle(x, y + h * 0.6, w * 0.1, lw=0.7, fill=Wt)
    for sx in (-1, 1): k.circle(x + sx * w * 0.13, y + h * 0.66, 0.9, lw=0.3, fill=K)
    hat = [(x - w * 0.4, y + h * 0.62), (x + w * 0.4, y + h * 0.62), (x + w * 0.12, y + h * 1.0)]
    k.shape(hat, lw=0.9, fill=K, amp=0.1)
    k.line([(x + w * 0.4, y + h * 0.3), (x + w * 1.1, y + h * 0.9), (x + w * 1.25, y + h * 0.2)], lw=0.6, amp=0)


def spool(k, x, y, h):
    w = h * 0.7
    for yy in (y, y + h * 0.88): k.shape(k.arcpts(x, yy + h * 0.06, w / 2, h * 0.07, 0, 360, 20), lw=0.8, fill=Wt, amp=0)
    body = [(x - w * 0.36, y + h * 0.1), (x + w * 0.36, y + h * 0.1), (x + w * 0.36, y + h * 0.9), (x - w * 0.36, y + h * 0.9)]
    k.shape(body, lw=0.8, fill=Wt, amp=0); k.hatch(body, angle=8, gap=1.0, lw=0.35)
    k.line([(x + w * 0.36, y + h * 0.5), (x + w * 0.8, y + h * 0.3), (x + w * 1.1, y + h * 0.45), (x + w * 1.4, y + h * 0.2)], lw=0.5, amp=0.3)


def thimble(k, x, y, h):
    w = h * 0.8
    body = [(x - w / 2, y), (x + w / 2, y)] + k.arcpts(x, y + h * 0.75, w * 0.42, h * 0.25, 0, 180, 18)
    k.shape(body, lw=0.9, fill=Wt, amp=0)
    for r in range(4):
        for c in range(5):
            k.circle(x - w * 0.3 + c * w * 0.15 + (r % 2) * w * 0.07, y + h * (0.25 + r * 0.16), 0.55, lw=0.3, fill=K)
    k.line([(x - w * 0.52, y + h * 0.06), (x + w * 0.52, y + h * 0.06)], lw=1.4, amp=0)


def hen(k, x, y, w):
    body = k.arcpts(x, y + w * 0.38, w * 0.4, w * 0.3, -20, 200, 24) + [(x - w * 0.55, y + w * 0.6), (x - w * 0.42, y + w * 0.3)]
    k.shape(body, lw=0.9, fill=Wt, amp=0.2)
    for i in range(4): k.c.setLineWidth(0.4); k.c.arc(x - w * 0.15 + i * w * 0.08, y + w * 0.3, x + w * 0.05 + i * w * 0.08, y + w * 0.5, 200, 120)
    k.circle(x + w * 0.36, y + w * 0.64, w * 0.13, lw=0.8, fill=Wt)
    k.shape([(x + w * 0.5, y + w * 0.66), (x + w * 0.6, y + w * 0.62), (x + w * 0.48, y + w * 0.59)], lw=0.5, fill=K, amp=0)
    for i in range(3): k.circle(x + w * (0.32 + 0.06 * i), y + w * 0.78 + (i % 2) * 1.5, w * 0.04, lw=0.4, fill=K)
    k.circle(x + w * 0.4, y + w * 0.66, 0.7, lw=0.3, fill=K)
    for u in (-0.08, 0.1): k.line([(x + w * u, y + w * 0.28), (x + w * u, y)], lw=0.8, amp=0); k.line([(x + w * u - 2, y), (x + w * u + 3, y)], lw=0.8, amp=0)


def sunflower(k, x, y, h):
    k.line([(x, y), (x + 1, y + h * 0.7)], lw=1.0, amp=0.2)
    for sx in (-1, 1): k.shape([(x, y + h * 0.3), (x + sx * h * 0.18, y + h * 0.4), (x + sx * h * 0.05, y + h * 0.28)], lw=0.6, fill=Wt, amp=0)
    cx, cy, r = x + 1, y + h * 0.82, h * 0.12
    for i in range(16):
        a = 2 * math.pi * i / 16
        k.shape([(cx + r * 0.9 * math.cos(a - 0.2), cy + r * 0.9 * math.sin(a - 0.2)), (cx + r * 1.8 * math.cos(a), cy + r * 1.8 * math.sin(a)), (cx + r * 0.9 * math.cos(a + 0.2), cy + r * 0.9 * math.sin(a + 0.2))], lw=0.5, fill=Wt, amp=0)
    k.circle(cx, cy, r, lw=0.8, fill=K)


def packet(k, x, y, w, text="SEEDS"):
    h = w * 1.35
    k.rect(x - w / 2, y, w, h, lw=0.9)
    k.line([(x - w / 2, y + h * 0.85), (x + w / 2, y + h * 0.85)], lw=0.5, amp=0)
    k.text(x, y + h * 0.1, text, size=w * 0.17, font="Ink-Plex")
    k.circle(x, y + h * 0.52, w * 0.16, lw=0.6, fill=K)
    for i in range(10):
        a = 2 * math.pi * i / 10
        k.line([(x + w * 0.18 * math.cos(a), y + h * 0.52 + w * 0.18 * math.sin(a)), (x + w * 0.32 * math.cos(a), y + h * 0.52 + w * 0.32 * math.sin(a))], lw=0.6, amp=0)


def dove(k, x, y, w, f=1):
    X = lambda u: x + f * u * w
    body = [(X(-0.5), y + w * 0.2), (X(-0.1), y), (X(0.3), y + w * 0.05), (X(0.45), y + w * 0.25), (X(0.35), y + w * 0.35), (X(0.1), y + w * 0.22), (X(-0.3), y + w * 0.3)]
    k.shape(body, lw=0.8, fill=Wt, amp=0.1)
    k.shape([(X(-0.1), y + w * 0.2), (X(-0.25), y + w * 0.55), (X(0.15), y + w * 0.25)], lw=0.6, fill=Wt, amp=0.1)
    k.circle(X(0.36), y + w * 0.26, 0.6, lw=0.3, fill=K)
    k.shape([(X(0.45), y + w * 0.27), (X(0.55), y + w * 0.24), (X(0.45), y + w * 0.22)], lw=0.4, fill=K, amp=0)


def notes(k, x, y, s):
    for i, (dx, dy) in enumerate([(0, 0), (s * 1.3, s * 0.5), (s * 2.6, s * 0.2)]):
        k.shape(k.arcpts(x + dx, y + dy, s * 0.32, s * 0.24, 0, 360, 14), lw=0.5, fill=K, amp=0)
        k.line([(x + dx + s * 0.3, y + dy), (x + dx + s * 0.3, y + dy + s * 1.3)], lw=0.7, amp=0)
    k.line([(x + s * 0.3, y + s * 1.3), (x + s * 1.6, y + s * 1.8)], lw=1.6, amp=0)
    k.line([(x + s * 1.6, y + s * 1.8), (x + s * 2.9, y + s * 1.5)], lw=1.6, amp=0)


def paper_lantern(k, x, y, h):
    w = h * 0.8
    body = k.arcpts(x, y + h / 2, w / 2, h / 2, 0, 360, 30)
    k.shape(body, lw=0.9, fill=Wt, amp=0)
    for u in (-0.3, 0, 0.3):
        q = k.arcpts(x, y + h / 2, abs(u) * w + 0.5, h / 2, 270, 450 if u >= 0 else 90, 20) if u else [(x, y), (x, y + h)]
        k.line(q, lw=0.4, amp=0)
    for v in (0.2, 0.8): k.line([(x - w * 0.4, y + h * v), (x + w * 0.4, y + h * v)], lw=0.3, amp=0)
    k.rect(x - w * 0.2, y + h - 1, w * 0.4, 3, lw=0.5, fill=K); k.rect(x - w * 0.2, y - 2, w * 0.4, 3, lw=0.5, fill=K)
    k.line([(x, y + h + 2), (x, y + h + h * 0.4)], lw=0.5, amp=0)


def ground(k, w, y):
    k.line([(w * 0.08, y), (w * 0.92, y)], lw=0.7, amp=0.3)


# ------------------------------------------------------------------ scenes
def village(k, w, h, people=True):
    gy = h * 0.14
    k.hills(0, w, gy + h * 0.32, amp=8, n=3)
    for i, tx in enumerate((0.06, 0.94)): tree(k, w * tx, gy + h * 0.28, h * 0.32)
    k.c.saveState()
    house(k, w * 0.04, gy, w * 0.26, h * 0.5, sign=None, door=0.62)
    house(k, w * 0.66, gy, w * 0.3, h * 0.55, sign="POST OFFICE", door=0.15, smoke=False)
    house(k, w * 0.33, gy, w * 0.3, h * 0.66, sign="BLOOM'S WOOLS", door=0.4, smoke=False)
    k.c.restoreState()
    k.line([(0, gy), (w, gy)], lw=1.0, amp=0.4)
    k.lamppost(w * 0.645, gy, h * 0.42)
    for i in range(30):
        X = k.r.uniform(w * 0.02, w * 0.98); k.line([(X, gy - k.r.uniform(2, 6)), (X + 2, gy - k.r.uniform(2, 6))], lw=0.3, amp=0)
    if people:
        lady(k, w * 0.22, gy - h * 0.06, h * 0.34)
        dog(k, w * 0.36, gy - h * 0.06, h * 0.16)
    # bunting
    pts = [(w * 0.02 + w * 0.96 * t, h * 0.93 - 10 * math.sin(math.pi * t)) for t in [i / 30 for i in range(31)]]
    k.line(pts, lw=0.5, amp=0)
    for i in range(1, 30, 2):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        k.shape([(x0, y0), (x1, y1), ((x0 + x1) / 2, (y0 + y1) / 2 - 7)], lw=0.5, fill=K if i % 4 == 1 else Wt, amp=0)


def frontispiece(k, w, h):
    village(k, w, h)


def cover_scene(k, w, h):
    village(k, w, h)


def title(k, w, h):
    ground(k, w, h * 0.1)
    lady(k, w * 0.42, h * 0.1, h * 0.85); dog(k, w * 0.6, h * 0.1, h * 0.36)


def thanks(k, w, h):
    ground(k, w, h * 0.1)
    k.armchair(w * 0.42, h * 0.1, w * 0.36)
    dog(k, w * 0.72, h * 0.1, h * 0.32, facing=-1)
    k.teapot(w * 0.17, h * 0.1, h * 0.3)


def op_solutions(k, w, h):
    ground(k, w, h * 0.1)
    k.book(w * 0.3, h * 0.1, h * 0.7, open_=True); k.spectacles(w * 0.55, h * 0.2, h * 0.35); k.pencil(w * 0.7, h * 0.12, h * 0.7, ang=25)


def c1(k, w, h):
    ground(k, w, h * 0.1); jar(k, w * 0.3, h * 0.1, h * 0.4, "JAM"); jar(k, w * 0.43, h * 0.1, h * 0.34); rosette(k, w * 0.66, h * 0.62, h * 0.16)


def c2(k, w, h):
    ground(k, w, h * 0.1); k.books(w * 0.28, h * 0.1, h * 0.72, n=3); k.book(w * 0.56, h * 0.1, h * 0.55, open_=True); k.spectacles(w * 0.76, h * 0.2, h * 0.3)


def c3(k, w, h):
    k.window(w * 0.32, h * 0.32, w * 0.36, h * 0.6, lit=True)
    k.rect(w * 0.26, h * 0.24, w * 0.48, h * 0.08, lw=0.9)
    pie(k, w * 0.43, h * 0.32, h * 0.38)
    # a crow perched at the end of the sill
    cx, cy = w * 0.66, h * 0.33
    k.shape([(cx - 9, cy + 6), (cx, cy), (cx + 7, cy + 3), (cx + 9, cy + 10), (cx + 3, cy + 14), (cx - 2, cy + 10)], lw=0.7, fill=K, amp=0.1)
    k.circle(cx + 6, cy + 15, 3.4, lw=0.6, fill=K); k.shape([(cx + 9, cy + 16), (cx + 14, cy + 15), (cx + 9, cy + 14)], lw=0.5, fill=K, amp=0)
    k.circle(cx + 7, cy + 16, 0.6, lw=0.1, fill=Wt)


def c4(k, w, h):
    ground(k, w, h * 0.1); gnome(k, w * 0.38, h * 0.1, h * 0.8)
    for i in range(4): sunflower(k, w * (0.62 + 0.07 * i), h * 0.1, h * (0.55 + 0.1 * (i % 2)))


def c5(k, w, h):
    ground(k, w, h * 0.1); spool(k, w * 0.3, h * 0.1, h * 0.5); thimble(k, w * 0.58, h * 0.1, h * 0.3)
    k.line([(w * 0.66, h * 0.15), (w * 0.82, h * 0.6)], lw=0.8, amp=0); k.circle(w * 0.815, h * 0.57, 1.0, lw=0.4, fill=Wt)


def c6(k, w, h):
    k.clockface(w * 0.4, h * 0.52, h * 0.4, moon=False, roman=True); k.key(w * 0.58, h * 0.5, w * 0.25)


def c7(k, w, h):
    ground(k, w, h * 0.1); hen(k, w * 0.26, h * 0.1, h * 0.55); packet(k, w * 0.58, h * 0.1, h * 0.42, "SEEDS"); sunflower(k, w * 0.76, h * 0.1, h * 0.85)


def c8(k, w, h):
    ground(k, w, h * 0.1); k.cake(w * 0.42, h * 0.1, h * 0.6)
    dove(k, w * 0.38, h * 0.5, h * 0.22, 1); dove(k, w * 0.47, h * 0.5, h * 0.22, -1)
    k.teapot(w * 0.72, h * 0.1, h * 0.4)


def c9(k, w, h):
    ground(k, w, h * 0.1); k.violin(w * 0.3, h * 0.1, h * 0.85); notes(k, w * 0.5, h * 0.35, h * 0.2)


def c10(k, w, h):
    k.line([(w * 0.1, h * 0.86), (w * 0.9, h * 0.8)], lw=0.5, amp=0.2)
    for i, x in enumerate((0.22, 0.42, 0.78)): paper_lantern(k, w * x, h * (0.32 + 0.06 * (i % 2)), h * 0.32)
    k.star5(w * 0.6, h * 0.55, h * 0.28, fill=Wt, lw=0.9)
    dog(k, w * 0.6, h * 0.04, h * 0.28, facing=-1)


CASES = ["c%d" % i for i in range(1, 11)]
SPECS = {
    "frontispiece": (4.7, 3.6, frontispiece, 41),
    "title": (2.6, 1.6, title, 43),
    "opener-solutions": (3.4, 1.6, op_solutions, 54),
    "thanks": (3.0, 1.8, thanks, 61),
    "cover-scene": (5.4, 4.2, cover_scene, 71),
    **{n: (2.6, 1.3, globals()[n], 80 + i) for i, n in enumerate(CASES)},
}

if __name__ == "__main__":
    only = set(sys.argv[1:])
    for name, (wi, hi, fn, seed) in SPECS.items():
        if only and name not in only: continue
        render(os.path.join(OUT, name + ".png"), wi, hi, fn, seed=seed); print("drew", name)
