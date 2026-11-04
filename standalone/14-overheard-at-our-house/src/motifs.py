"""Black-and-white ink illustrations for Two Cups of Tea -> ../illustrations/*.png
Pure black line art on white at 300 DPI, drawn with the shared inkart house style plus local
helpers for the four seasons (tulips, picnic baskets, pumpkins, mugs by the fire). No people:
every scene shows two of something -- two cups, two chairs, two bicycles' worth of company.
Deterministic: same seeds -> same images. Run from src/: python3 illustrations.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inkart import render, Wt, K, lerp

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "illustrations")

# ----------------------------------------------------------------------------- small motifs
def heart(k, x, y, s, fill=K, lw=0.7):
    pts = []
    for i in range(41):
        t = math.pi * 2 * i / 40
        px = 16 * math.sin(t) ** 3
        py = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((x + px * s / 32, y + py * s / 32))
    k.shape(pts, lw=lw, fill=fill, amp=0)

def steam(k, x, y, L, lw=0.55, phase=0.0):
    pts = [(x + 2.2 * math.sin(t / L * 6.0 + phase) * (0.4 + t / L), y + t) for t in [L * i / 30 for i in range(31)]]
    k.line(pts, lw=lw, amp=0)

def teacup(k, x, y, w, steam_=True, pattern="dots", saucer=True):
    """Teacup on a saucer; (x, y) = centre of the saucer's bottom."""
    h = w * 0.55
    if saucer:
        k.shape(k.arcpts(x, y + w * 0.06, w * 0.68, w * 0.12, 0, 360, 36), lw=0.8, fill=Wt, amp=0)
        k.shape(k.arcpts(x, y + w * 0.09, w * 0.34, w * 0.055, 0, 360, 24), lw=0.45, fill=None, amp=0)
    by = y + w * 0.1
    body = [(x - w / 2, by + h)] + k.arcpts(x, by + h, w / 2, h, 180, 360, 26)[1:]
    # handle
    k.c.setStrokeColor(K); k.c.setLineWidth(max(0.8, w * 0.045))
    k.c.ellipse(x + w * 0.36, by + h * 0.28, x + w * 0.68, by + h * 0.86, stroke=1, fill=0)
    k.shape(body, lw=0.9, fill=Wt, amp=0)
    # shading on the right
    k.hatch([p for p in body if p[0] > x + w * 0.18] + [(x + w * 0.18, by + h)], angle=80, gap=max(1.1, w * 0.045), lw=0.35)
    if pattern == "dots":
        for i in range(7):
            u = lerp(-0.36, 0.36, i / 6); yy = by + h * (0.62 - 0.25 * u * u)
            k.circle(x + u * w, yy, max(0.6, w * 0.022), lw=0.3, fill=K)
    elif pattern == "band":
        k.line([(x - w * 0.47, by + h * 0.78)] + [(x + w * 0.47 * math.cos(math.radians(a)), by + h * 0.78 - h * 0.18 * math.sin(math.radians(a))) for a in range(180, 361, 15)], lw=0.5, amp=0)
        for i in range(6):
            u = lerp(-0.35, 0.35, i / 5); flower(k, x + u * w, by + h * 0.6 - h * 0.12 * (1 - abs(u) * 2), w * 0.045)
    elif pattern == "heart":
        heart(k, x - w * 0.06, by + h * 0.5, w * 0.18, fill=K, lw=0.4)
    k.shape(body, lw=0.9, fill=None, amp=0)
    k.shape(k.arcpts(x, by + h, w / 2, w * 0.09, 0, 360, 26), lw=0.8, fill=Wt, amp=0)
    k.shape(k.arcpts(x, by + h - w * 0.01, w * 0.43, w * 0.065, 0, 360, 26), lw=0.4, fill=K, amp=0)
    if steam_:
        for i, dx in enumerate((-w * 0.14, w * 0.1)):
            steam(k, x + dx, by + h + w * 0.12, w * 0.55, lw=max(0.45, w * 0.018), phase=i * 2.1)

def mug2(k, x, y, h, steam_=True, stripes=True):
    """A plump striped mug; (x, y) = centre bottom."""
    w = h * 0.85
    k.c.setStrokeColor(K); k.c.setLineWidth(max(0.9, h * 0.06))
    k.c.ellipse(x + w * 0.38, y + h * 0.22, x + w * 0.78, y + h * 0.78, stroke=1, fill=0)
    body = [(x - w / 2, y + h), (x - w / 2, y + h * 0.1), (x - w * 0.4, y), (x + w * 0.4, y), (x + w / 2, y + h * 0.1), (x + w / 2, y + h)]
    k.shape(body, lw=0.95, fill=Wt, amp=0)
    if stripes:
        for v in (0.3, 0.42, 0.7):
            k.c.setLineWidth(max(0.8, h * 0.05)); k.c.line(x - w / 2, y + h * v, x + w / 2, y + h * v)
    k.hatch([(x + w * 0.22, y), (x + w * 0.4, y), (x + w / 2, y + h * 0.1), (x + w / 2, y + h), (x + w * 0.22, y + h)], angle=90, gap=max(1.1, h * 0.05), lw=0.35)
    k.shape(body, lw=0.95, fill=None, amp=0)
    k.shape(k.arcpts(x, y + h, w / 2, h * 0.1, 0, 360, 26), lw=0.85, fill=Wt, amp=0)
    k.shape(k.arcpts(x, y + h - h * 0.015, w * 0.43, h * 0.07, 0, 360, 26), lw=0.4, fill=K, amp=0)
    if steam_:
        for i, dx in enumerate((-w * 0.16, w * 0.12)):
            steam(k, x + dx, y + h + h * 0.14, h * 0.6, lw=max(0.45, h * 0.02), phase=0.7 + i * 1.9)

def flower(k, x, y, r, petals=5, centre=True, lw=0.4):
    for i in range(petals):
        a = 2 * math.pi * i / petals + 0.3
        k.shape(k.arcpts(x + r * 0.9 * math.cos(a), y + r * 0.9 * math.sin(a), r * 0.55, r * 0.55, 0, 360, 10), lw=lw, fill=Wt, amp=0)
    if centre: k.circle(x, y, r * 0.42, lw=lw, fill=K)

def daisy(k, x, y, r, lw=0.5):
    for i in range(12):
        a = 2 * math.pi * i / 12
        tip = (x + r * math.cos(a), y + r * math.sin(a))
        sideA = (x + r * 0.45 * math.cos(a + 0.22), y + r * 0.45 * math.sin(a + 0.22))
        sideB = (x + r * 0.45 * math.cos(a - 0.22), y + r * 0.45 * math.sin(a - 0.22))
        k.shape([(x, y), sideA, tip, sideB], lw=lw, fill=Wt, amp=0)
    k.circle(x, y, r * 0.28, lw=lw, fill=K)
    k.circle(x - r * 0.08, y + r * 0.08, r * 0.08, lw=0, fill=Wt, stroke=False)

def leaf(k, x, y, L, ang, fill=Wt, lw=0.6, vein=True):
    a = math.radians(ang); dx, dy = math.cos(a), math.sin(a); nx, ny = -dy, dx
    pts = []
    for i in range(17):
        t = i / 16; wv = L * 0.28 * math.sin(math.pi * t)
        pts.append((x + dx * L * t + nx * wv, y + dy * L * t + ny * wv))
    for i in range(15, 0, -1):
        t = i / 16; wv = L * 0.28 * math.sin(math.pi * t)
        pts.append((x + dx * L * t - nx * wv, y + dy * L * t - ny * wv))
    k.shape(pts, lw=lw, fill=fill, amp=0)
    if vein and fill is not K:
        k.line([(x, y), (x + dx * L * 0.92, y + dy * L * 0.92)], lw=0.35, amp=0)

def tulip(k, x, y, h, lean=0.0, lw=0.7, dark=False):
    top = (x + lean * h, y + h)
    k.line([(x, y), (x + lean * h * 0.5, y + h * 0.5), top], lw=lw * 1.1, amp=0.1)
    leaf(k, x, y + h * 0.05, h * 0.55, 72 + lean * 30, lw=0.5)
    leaf(k, x, y + h * 0.12, h * 0.45, 112 + lean * 30, lw=0.5)
    cx, cy = top; r = h * 0.17
    cupp = [(cx - r, cy + r * 1.5), (cx - r * 0.95, cy + r * 0.4)] + k.arcpts(cx, cy + r * 0.4, r * 0.95, r * 0.9, 180, 360, 16)[1:] + [(cx + r, cy + r * 1.5), (cx + r * 0.5, cy + r * 1.05), (cx, cy + r * 1.6), (cx - r * 0.5, cy + r * 1.05)]
    k.shape(cupp, lw=lw, fill=K if dark else Wt, amp=0)
    if not dark:
        k.hatch([(cx + r * 0.2, cy - r * 0.4), (cx + r, cy + r * 0.4), (cx + r, cy + r * 1.5), (cx + r * 0.5, cy + r * 1.05), (cx + r * 0.2, cy + r * 1.2)], angle=80, gap=1.1, lw=0.3)
        k.line([(cx, cy - r * 0.45), (cx, cy + r * 1.5)], lw=0.4, amp=0)

def pot(k, x, y, w, plant="herb"):
    h = w * 0.8
    body = [(x - w * 0.4, y), (x + w * 0.4, y), (x + w * 0.5, y + h * 0.78), (x - w * 0.5, y + h * 0.78)]
    k.shape(body, lw=0.9, fill=Wt, amp=0)
    k.hatch([(x + w * 0.15, y), (x + w * 0.4, y), (x + w * 0.5, y + h * 0.78), (x + w * 0.2, y + h * 0.78)], angle=95, gap=1.3, lw=0.35)
    k.shape([(x - w * 0.56, y + h * 0.72), (x + w * 0.56, y + h * 0.72), (x + w * 0.56, y + h * 0.95), (x - w * 0.56, y + h * 0.95)], lw=0.9, fill=Wt, amp=0)
    top = y + h * 0.95
    if plant == "herb":
        for i in range(9):
            a = lerp(60, 120, i / 8) + k.r.uniform(-6, 6); L = w * k.r.uniform(0.55, 0.9)
            bx = x + w * lerp(-0.35, 0.35, i / 8)
            k.line([(bx, top), (bx + L * math.cos(math.radians(a)), top + L * math.sin(math.radians(a)))], lw=0.5, amp=0.1)
            for j in range(3):
                t = 0.35 + 0.25 * j; px = bx + L * t * math.cos(math.radians(a)); py = top + L * t * math.sin(math.radians(a))
                leaf(k, px, py, w * 0.18, a + (40 if j % 2 else -40), lw=0.4, vein=False)
    elif plant == "tulips":
        for i, (dx, hh, ln) in enumerate([(-0.18, 1.3, -0.12), (0.02, 1.55, 0.0), (0.2, 1.25, 0.12)]):
            tulip(k, x + w * dx, top, w * hh, lean=ln, lw=0.6, dark=(i == 1))
    elif plant == "daisies":
        for (dx, hh) in [(-0.25, 1.0), (0.0, 1.35), (0.26, 1.1)]:
            k.line([(x + w * dx * 0.5, top), (x + w * dx, top + w * hh)], lw=0.6, amp=0.1)
            leaf(k, x + w * dx * 0.6, top + w * hh * 0.3, w * 0.3, 60 if dx > 0 else 120, lw=0.4)
            daisy(k, x + w * dx, top + w * hh, w * 0.2)

def sun(k, x, y, r, rays=14):
    k.circle(x, y, r, lw=0.9, fill=Wt)
    k.hatch(k.arcpts(x, y, r * 0.98, r * 0.98, -60, 120, 30), angle=30, gap=1.4, lw=0.3)
    k.circle(x, y, r, lw=0.9, fill=None)
    for i in range(rays):
        a = 2 * math.pi * i / rays; L = r * (0.55 if i % 2 else 0.85)
        k.line([(x + r * 1.25 * math.cos(a), y + r * 1.25 * math.sin(a)), (x + (r * 1.25 + L) * math.cos(a), y + (r * 1.25 + L) * math.sin(a))], lw=0.8, amp=0)

def cloud(k, x, y, w):
    bumps = [(-0.32, 0.0, 0.2), (-0.12, 0.12, 0.25), (0.12, 0.1, 0.22), (0.32, 0.0, 0.17)]
    pts = []
    for (dx, dy, r) in bumps:
        pts += k.arcpts(x + dx * w, y + dy * w, r * w, r * w * 0.85, 180 if dx < -0.3 else 160, 20 if dx < 0.3 else 0, 12)
    pts = [(x - 0.52 * w, y)] + pts + [(x + 0.49 * w, y)]
    k.shape(pts + [(x + 0.49 * w, y - 0.04 * w), (x - 0.52 * w, y - 0.04 * w)], lw=0.8, fill=Wt, amp=0.15)
    k.line([(x - 0.3 * w, y + 0.02 * w), (x + 0.25 * w, y + 0.02 * w)], lw=0.35, amp=0.1)

def birds(k, pts, s=4):
    for (x, y) in pts:
        k.line([(x - s, y + s * 0.4), (x - s * 0.5, y + s * 0.55), (x, y)], lw=0.6, amp=0)
        k.line([(x, y), (x + s * 0.5, y + s * 0.55), (x + s, y + s * 0.4)], lw=0.6, amp=0)

def songbird(k, x, y, s, facing=1):
    f = facing
    body = k.arcpts(x, y, s, s * 0.72, 0, 360, 24)
    k.shape(body, lw=0.8, fill=Wt, amp=0)
    k.hatch([p for p in body if p[1] < y - s * 0.1], angle=0, gap=1.0, lw=0.3)
    k.shape(body, lw=0.8, fill=None, amp=0)
    k.circle(x + f * s * 0.75, y + s * 0.55, s * 0.5, lw=0.8, fill=Wt)
    k.circle(x + f * s * 0.9, y + s * 0.65, s * 0.09, lw=0.2, fill=K)
    k.shape([(x + f * s * 1.2, y + s * 0.7), (x + f * s * 1.55, y + s * 0.55), (x + f * s * 1.2, y + s * 0.48)], lw=0.5, fill=K, amp=0)
    k.shape([(x - f * s * 0.85, y + s * 0.15), (x - f * s * 1.7, y + s * 0.55), (x - f * s * 1.6, y + s * 0.15), (x - f * s * 0.9, y - s * 0.15)], lw=0.7, fill=K, amp=0)
    k.shape([(x - f * s * 0.3, y + s * 0.2), (x + f * s * 0.35, y + s * 0.1), (x - f * s * 0.5, y - s * 0.3)], lw=0.5, fill=Wt, amp=0)
    for dx in (-0.15, 0.2): k.line([(x + f * s * dx, y - s * 0.7), (x + f * s * dx, y - s * 1.05)], lw=0.5, amp=0)

def tree(k, x, y, h, kind="leafy", lean=0.0):
    """Round-canopy tree. kind: leafy | blossom | autumn | bare"""
    tw = h * 0.07
    trunk = [(x - tw, y), (x + tw, y), (x + tw * 0.6 + lean * h * 0.2, y + h * 0.5), (x - tw * 0.6 + lean * h * 0.2, y + h * 0.5)]
    k.shape(trunk, lw=0.8, fill=Wt, amp=0.15)
    k.hatch([(x + tw * 0.1, y), (x + tw, y), (x + tw * 0.6 + lean * h * 0.2, y + h * 0.5), (x + lean * h * 0.2, y + h * 0.5)], angle=90, gap=1.2, lw=0.35)
    for sx in (-1, 1):
        k.line([(x + lean * h * 0.15, y + h * 0.42), (x + sx * h * 0.18 + lean * h * 0.2, y + h * 0.62)], lw=1.0, amp=0.2)
    cx, cy = x + lean * h * 0.22, y + h * 0.68; R = h * 0.33
    if kind == "bare":
        for i in range(7):
            a = math.radians(lerp(25, 155, i / 6)); L = R * k.r.uniform(0.8, 1.1)
            p0 = (cx, cy - R * 0.25); p1 = (cx + L * math.cos(a), cy - R * 0.25 + L * math.sin(a))
            k.line([p0, p1], lw=0.7, amp=0.3)
            for j in range(2):
                t = 0.5 + 0.25 * j; bx, by = lerp(p0[0], p1[0], t), lerp(p0[1], p1[1], t)
                b = a + (0.6 if j else -0.6)
                k.line([(bx, by), (bx + L * 0.3 * math.cos(b), by + L * 0.3 * math.sin(b))], lw=0.45, amp=0.2)
        return
    canopy = []
    n = 14
    for i in range(n):
        a0 = 360 * i / n; a1 = 360 * (i + 1) / n
        mx, my = cx + R * math.cos(math.radians((a0 + a1) / 2)), cy + R * 0.85 * math.sin(math.radians((a0 + a1) / 2))
        canopy += k.arcpts(mx, my, R * 0.26, R * 0.24, (a0 + a1) / 2 - 95, (a0 + a1) / 2 + 95, 8)
    k.shape(canopy, lw=0.9, fill=Wt, amp=0.1)
    k.hatch([p for p in canopy if p[0] > cx + R * 0.1 or p[1] < cy - R * 0.4] + [(cx + R * 0.2, cy - R * 0.2)], angle=-50, gap=1.6, lw=0.35)
    k.shape(canopy, lw=0.9, fill=None, amp=0.1)
    if kind == "blossom":
        for i in range(26):
            a = k.r.uniform(0, 2 * math.pi); rr = R * math.sqrt(k.r.uniform(0.05, 0.85))
            flower(k, cx + rr * math.cos(a), cy + rr * 0.85 * math.sin(a), h * 0.022, lw=0.35)
    elif kind == "autumn":
        for i in range(22):
            a = k.r.uniform(0, 2 * math.pi); rr = R * math.sqrt(k.r.uniform(0.05, 0.8))
            leaf(k, cx + rr * math.cos(a), cy + rr * 0.85 * math.sin(a), h * 0.06, k.r.uniform(0, 360), fill=K if k.r.random() < 0.4 else Wt, lw=0.35, vein=False)
    else:
        for i in range(16):
            a = k.r.uniform(0, 2 * math.pi); rr = R * math.sqrt(k.r.uniform(0.05, 0.8))
            px, py = cx + rr * math.cos(a), cy + rr * 0.85 * math.sin(a)
            k.line(k.arcpts(px, py, h * 0.03, h * 0.02, 200, 340, 6), lw=0.4, amp=0)

def picket(k, x0, x1, y, h, gap=None):
    gap = gap or max(3.2, h * 0.3); n = int((x1 - x0) / gap)
    k.line([(x0, y + h * 0.3), (x0 + n * gap, y + h * 0.3)], lw=0.7, amp=0.1)
    k.line([(x0, y + h * 0.68), (x0 + n * gap, y + h * 0.68)], lw=0.7, amp=0.1)
    pw = gap * 0.55
    for i in range(n + 1):
        xx = x0 + i * gap
        k.shape([(xx - pw / 2, y), (xx + pw / 2, y), (xx + pw / 2, y + h * 0.86), (xx, y + h), (xx - pw / 2, y + h * 0.86)], lw=0.55, fill=Wt, amp=0)

def grass(k, x0, x1, y, n=40, hmax=5):
    for i in range(n):
        x = lerp(x0, x1, (i + k.r.random()) / n); hh = k.r.uniform(hmax * 0.4, hmax)
        k.line([(x, y), (x + k.r.uniform(-1.5, 1.5), y + hh)], lw=0.4, amp=0)

def basket(k, x, y, w):
    h = w * 0.5
    body = [(x - w / 2, y + h), (x - w * 0.44, y), (x + w * 0.44, y), (x + w / 2, y + h)]
    k.shape(body, lw=0.9, fill=Wt, amp=0)
    k.hatch(body, angle=35, gap=2.0, lw=0.4, cross=True)
    k.shape(body, lw=0.9, fill=None, amp=0)
    lid = [(x - w * 0.54, y + h), (x + w * 0.54, y + h), (x + w * 0.5, y + h * 1.22), (x - w * 0.5, y + h * 1.22)]
    k.shape(lid, lw=0.9, fill=Wt, amp=0)
    k.hatch(lid, angle=90, gap=1.6, lw=0.35)
    k.shape(lid, lw=0.9, fill=None, amp=0)
    k.c.setStrokeColor(K); k.c.setLineWidth(1.3)
    k.c.arc(x - w * 0.32, y + h * 0.75, x + w * 0.32, y + h * 2.05, 0, 180)
    # gingham cloth peeking out
    cl = [(x - w * 0.2, y + h * 1.22), (x - w * 0.05, y + h * 1.5), (x + w * 0.12, y + h * 1.3), (x + w * 0.25, y + h * 1.45), (x + w * 0.3, y + h * 1.22)]
    k.shape(cl, lw=0.6, fill=Wt, amp=0)
    k.hatch(cl, angle=0, gap=1.4, lw=0.35); k.hatch(cl, angle=90, gap=2.8, lw=0.35)

def blanket(k, quad, rows=6, cols=8):
    (ax, ay), (bx, by), (cx, cy), (dx, dy) = quad   # near-left, near-right, far-right, far-left
    k.shape(quad, lw=0.9, fill=Wt, amp=0)
    def P(u, v):
        return (lerp(lerp(ax, bx, u), lerp(dx, cx, u), v), lerp(lerp(ay, by, u), lerp(dy, cy, u), v))
    for i in range(rows):
        for j in range(cols):
            if (i + j) % 2 == 0:
                cell = [P(j / cols, i / rows), P((j + 1) / cols, i / rows), P((j + 1) / cols, (i + 1) / rows), P(j / cols, (i + 1) / rows)]
                k.hatch(cell, angle=45, gap=1.2, lw=0.35, jitter=0.05)
    k.shape(quad, lw=0.9, fill=None, amp=0)

def kite(k, x, y, w, tail_to=None):
    h = w * 1.35
    pts = [(x, y + h), (x + w / 2, y + h * 0.62), (x, y), (x - w / 2, y + h * 0.62)]
    k.shape(pts, lw=0.9, fill=Wt, amp=0)
    k.hatch([(x, y + h), (x + w / 2, y + h * 0.62), (x, y + h * 0.62)], angle=0, gap=1.3, lw=0.35)
    k.hatch([(x, y), (x - w / 2, y + h * 0.62), (x, y + h * 0.62)], angle=90, gap=1.3, lw=0.35)
    k.shape(pts, lw=0.9, fill=None, amp=0)
    k.line([(x, y), (x, y + h)], lw=0.5, amp=0); k.line([(x - w / 2, y + h * 0.62), (x + w / 2, y + h * 0.62)], lw=0.5, amp=0)
    tail = [(x + 6 * math.sin(t * 0.18), y - t) for t in range(0, int(h * 1.4), 2)]
    k.line(tail, lw=0.5, amp=0)
    for i in range(1, 5):
        tx, ty = tail[min(len(tail) - 1, i * len(tail) // 5)]
        k.shape([(tx, ty), (tx - 3, ty + 1.8), (tx - 3, ty - 1.8)], lw=0.4, fill=K, amp=0)
        k.shape([(tx, ty), (tx + 3, ty + 1.8), (tx + 3, ty - 1.8)], lw=0.4, fill=K, amp=0)
    if tail_to:
        k.c.setDash(0.8, 1.6); k.line([(x, y + h * 0.4), tail_to], lw=0.4, amp=0); k.c.setDash()

def sailboat(k, x, y, w):
    hull = [(x - w / 2, y + w * 0.12), (x + w / 2, y + w * 0.12), (x + w * 0.38, y), (x - w * 0.36, y)]
    k.shape(hull, lw=0.8, fill=K, amp=0)
    k.line([(x, y + w * 0.12), (x, y + w * 0.95)], lw=0.7, amp=0)
    k.shape([(x + 1, y + w * 0.18), (x + 1, y + w * 0.9), (x + w * 0.42, y + w * 0.18)], lw=0.7, fill=Wt, amp=0)
    k.shape([(x - 1, y + w * 0.24), (x - 1, y + w * 0.75), (x - w * 0.3, y + w * 0.24)], lw=0.7, fill=Wt, amp=0)
    k.hatch([(x - 1, y + w * 0.24), (x - 1, y + w * 0.75), (x - w * 0.3, y + w * 0.24)], angle=90, gap=1.2, lw=0.3)

def waves(k, x0, x1, y, rows=4, gap=5):
    for r in range(rows):
        yy = y - r * gap; ph = k.r.uniform(0, 6)
        xs = [lerp(x0, x1, i / 60) for i in range(61)]
        for j in range(0, 60, 6):
            seg = [(xs[i] + r * 3, yy + 1.2 * math.sin(i * 0.9 + ph)) for i in range(j, min(60, j + 4))]
            if len(seg) > 1: k.line(seg, lw=0.45, amp=0)

def rocking_chair(k, x, y, w, facing=1):
    f = facing; X = lambda u: x + f * u * w; h = w * 1.5
    # rocker
    k.line([(X(-0.55), y + h * 0.06)] + [(X(-0.55 + 1.1 * t), y + h * 0.06 * (1 - math.sin(math.pi * t)) ) for t in [i / 16 for i in range(17)]], lw=1.3, amp=0)
    for u in (-0.35, 0.3):
        k.line([(X(u), y + h * 0.03), (X(u), y + h * 0.36)], lw=1.1, amp=0)
    k.shape([(X(-0.42), y + h * 0.33), (X(0.4), y + h * 0.33), (X(0.36), y + h * 0.4), (X(-0.46), y + h * 0.4)], lw=0.9, fill=Wt, amp=0)
    k.hatch([(X(-0.42), y + h * 0.33), (X(0.4), y + h * 0.33), (X(0.36), y + h * 0.4), (X(-0.46), y + h * 0.4)], angle=0, gap=1.2, lw=0.3)
    # back with spindles
    k.line([(X(-0.42), y + h * 0.4), (X(-0.52), y + h)], lw=1.2, amp=0)
    k.line([(X(-0.14), y + h * 0.4), (X(-0.2), y + h)], lw=1.2, amp=0)
    k.shape([(X(-0.56), y + h * 0.95), (X(-0.16), y + h * 0.95), (X(-0.17), y + h * 1.04), (X(-0.55), y + h * 1.04)], lw=0.8, fill=Wt, amp=0)
    for i in range(1, 4):
        t = i / 4; k.line([(lerp(X(-0.42), X(-0.14), t), y + h * 0.4), (lerp(X(-0.52), X(-0.2), t), y + h * 0.95)], lw=0.5, amp=0)
    # arm
    k.line([(X(-0.48), y + h * 0.62), (X(0.32), y + h * 0.6)], lw=1.0, amp=0)
    k.line([(X(0.3), y + h * 0.6), (X(0.3), y + h * 0.4)], lw=0.8, amp=0)
    # cushion & blanket over the back
    bl = [(X(-0.5), y + h * 0.86), (X(-0.2), y + h * 0.88), (X(-0.16), y + h * 0.55), (X(-0.3), y + h * 0.5), (X(-0.47), y + h * 0.56)]
    k.shape(bl, lw=0.7, fill=Wt, amp=0.2)
    k.hatch(bl, angle=0, gap=2.2, lw=0.35); k.hatch(bl, angle=90, gap=2.2, lw=0.35)

def pumpkin(k, x, y, w):
    h = w * 0.62
    for dx, sc in [(-0.25, 0.55), (0.25, 0.55), (0.0, 0.62)]:
        body = k.arcpts(x + dx * w, y + h / 2, w * sc / 2 + w * 0.05, h / 2, 0, 360, 28)
        k.shape(body, lw=0.85, fill=Wt, amp=0)
        if dx >= 0:
            k.hatch([p for p in body if p[0] > x + dx * w + w * 0.08], angle=85, gap=1.3, lw=0.32)
        k.shape(body, lw=0.85, fill=None, amp=0)
    k.shape([(x - w * 0.04, y + h * 0.95), (x + w * 0.04, y + h * 0.95), (x + w * 0.08, y + h * 1.25), (x + w * 0.0, y + h * 1.25)], lw=0.7, fill=K, amp=0)
    k.line([(x + w * 0.05, y + h * 1.18), (x + w * 0.18, y + h * 1.3), (x + w * 0.24, y + h * 1.2), (x + w * 0.2, y + h * 1.12)], lw=0.5, amp=0)
    leaf(k, x - w * 0.03, y + h * 1.02, w * 0.25, 150, lw=0.5)

def apple(k, x, y, r, dark=False):
    pts = k.arcpts(x - r * 0.35, y, r * 0.75, r, 90, 270, 16) + k.arcpts(x + r * 0.35, y, r * 0.75, r, 270, 450, 16)
    k.shape(pts, lw=0.8, fill=K if dark else Wt, amp=0)
    if not dark: k.hatch([p for p in pts if p[0] > x + r * 0.2], angle=80, gap=1.1, lw=0.3); k.shape(pts, lw=0.8, fill=None, amp=0)
    k.line([(x, y + r * 0.8), (x + r * 0.15, y + r * 1.3)], lw=0.8, amp=0)
    leaf(k, x + r * 0.1, y + r * 1.15, r * 0.7, 25, lw=0.45, fill=Wt)

def acorn(k, x, y, s):
    nut = k.arcpts(x, y + s * 0.5, s * 0.38, s * 0.55, 180, 360, 16)
    k.shape([(x - s * 0.38, y + s * 0.5)] + nut[1:], lw=0.7, fill=Wt, amp=0)
    capp = k.arcpts(x, y + s * 0.5, s * 0.46, s * 0.32, 0, 180, 16)
    k.shape(capp, lw=0.7, fill=Wt, amp=0); k.hatch(capp, angle=45, gap=1.0, lw=0.3, cross=True); k.shape(capp, lw=0.7, fill=None, amp=0)
    k.line([(x, y + s * 0.82), (x + s * 0.08, y + s * 1.0)], lw=0.8, amp=0)

def maple(k, x, y, s, ang=0, fill=Wt):
    """Five-lobed maple leaf, stem at (x, y), height s, rotated by ang degrees."""
    half = [(0.0, 0.0), (0.07, 0.1), (0.3, 0.05), (0.26, 0.17), (0.48, 0.34), (0.36, 0.38), (0.42, 0.6), (0.22, 0.52), (0.18, 0.72), (0.07, 0.63), (0.0, 0.96)]
    prof = half + [(-u, v) for (u, v) in reversed(half[1:-1])]
    a = math.radians(ang)
    R = lambda u, v: (x + s * (u * math.cos(a) - v * math.sin(a)), y + s * (u * math.sin(a) + v * math.cos(a)))
    k.shape([R(u, v) for (u, v) in prof], lw=0.55, fill=fill, amp=0)
    vc = Wt if fill is K else K
    k.line([R(0, -0.2), R(0, 0.85)], lw=0.4, amp=0, color=vc if fill is K else K)
    for sx in (-1, 1):
        k.line([R(0, 0.12), R(sx * 0.38, 0.4)], lw=0.3, amp=0, color=vc if fill is K else K)
        k.line([R(0, 0.06), R(sx * 0.24, 0.12)], lw=0.3, amp=0, color=vc if fill is K else K)
    k.line([R(0, 0), R(0, -0.2)], lw=0.5, amp=0)

def teapot2(k, x, y, w):
    h = w * 0.62
    body = k.arcpts(x, y + h * 0.42, w * 0.38, h * 0.48, 0, 360, 30)
    k.shape([(x + w * 0.3, y + h * 0.35), (x + w * 0.62, y + h * 0.75), (x + w * 0.58, y + h * 0.8), (x + w * 0.26, y + h * 0.55)], lw=0.8, fill=Wt, amp=0)
    k.c.setLineWidth(1.6); k.c.setStrokeColor(K); k.c.arc(x - w * 0.56, y + h * 0.18, x - w * 0.2, y + h * 0.72, 90, 180)
    k.c.arc(x - w * 0.56, y + h * 0.18, x - w * 0.2, y + h * 0.72, 180, 180)
    k.shape(body, lw=0.9, fill=Wt, amp=0)
    k.hatch([p for p in body if p[0] > x + w * 0.1] + [(x + w * 0.1, y + h * 0.42)], angle=70, gap=1.4, lw=0.35)
    k.shape(body, lw=0.9, fill=None, amp=0)
    k.shape(k.arcpts(x, y + h * 0.88, w * 0.18, h * 0.07, 0, 360, 16), lw=0.7, fill=Wt, amp=0)
    k.circle(x, y + h * 1.0, w * 0.04, lw=0.6, fill=K)
    k.line([(x - w * 0.36, y + h * 0.5), (x + w * 0.36, y + h * 0.5)], lw=0.4, amp=0)

def watering_can(k, x, y, w):
    h = w * 0.62
    body = [(x - w * 0.32, y), (x + w * 0.32, y), (x + w * 0.3, y + h), (x - w * 0.3, y + h)]
    k.c.setStrokeColor(K); k.c.setLineWidth(1.4); k.c.arc(x - w * 0.46, y + h * 0.2, x - w * 0.18, y + h * 0.85, 90, 180)
    k.shape([(x + w * 0.25, y + h * 0.25), (x + w * 0.7, y + h * 0.95), (x + w * 0.74, y + h * 0.88), (x + w * 0.3, y + h * 0.1)], lw=0.8, fill=Wt, amp=0)
    k.shape([(x + w * 0.66, y + h * 0.98), (x + w * 0.82, y + h * 1.06), (x + w * 0.84, y + h * 0.8), (x + w * 0.7, y + h * 0.86)], lw=0.7, fill=K, amp=0)
    k.shape(body, lw=0.9, fill=Wt, amp=0)
    k.hatch([(x + w * 0.1, y), (x + w * 0.32, y), (x + w * 0.3, y + h), (x + w * 0.1, y + h)], angle=90, gap=1.3, lw=0.35)
    k.shape(body, lw=0.9, fill=None, amp=0)
    for v in (0.2, 0.8): k.line([(x - w * 0.32, y + h * v), (x + w * 0.31, y + h * v)], lw=0.5, amp=0)
    k.c.setStrokeColor(K); k.c.setLineWidth(1.3)
    k.c.arc(x - w * 0.25, y + h * 0.75, x + w * 0.25, y + h * 1.35, 0, 180)

def jug(k, x, y, h, label=None):
    w = h * 0.55
    body = [(x - w * 0.42, y), (x + w * 0.42, y), (x + w * 0.5, y + h * 0.55), (x + w * 0.34, y + h * 0.9), (x - w * 0.34, y + h * 0.9), (x - w * 0.5, y + h * 0.55)]
    k.c.setStrokeColor(K); k.c.setLineWidth(1.2); k.c.ellipse(x + w * 0.35, y + h * 0.25, x + w * 0.78, y + h * 0.78, stroke=1, fill=0)
    k.shape(body, lw=0.9, fill=Wt, amp=0)
    k.shape([(x - w * 0.34, y + h * 0.9), (x + w * 0.34, y + h * 0.9), (x + w * 0.36, y + h * 1.0), (x - w * 0.5, y + h * 1.02)], lw=0.8, fill=Wt, amp=0)
    k.hatch([(x - w * 0.44, y + h * 0.05), (x + w * 0.44, y + h * 0.05), (x + w * 0.49, y + h * 0.55), (x - w * 0.49, y + h * 0.55)], angle=0, gap=1.4, lw=0.35)
    for (dx, dy) in [(-0.2, 0.68), (0.15, 0.74), (0.0, 0.62)]:
        k.circle(x + dx * w, y + dy * h, w * 0.07, lw=0.4, fill=Wt)   # lemon slices
    k.shape(body, lw=0.9, fill=None, amp=0)

def glass(k, x, y, h, straw=True):
    w = h * 0.5
    body = [(x - w * 0.42, y), (x + w * 0.42, y), (x + w / 2, y + h), (x - w / 2, y + h)]
    k.shape(body, lw=0.8, fill=Wt, amp=0)
    k.hatch([(x - w * 0.45, y + h * 0.05), (x + w * 0.45, y + h * 0.05), (x + w * 0.48, y + h * 0.7), (x - w * 0.48, y + h * 0.7)], angle=0, gap=1.4, lw=0.32)
    k.shape(body, lw=0.8, fill=None, amp=0)
    if straw: k.line([(x + w * 0.1, y + h * 0.3), (x + w * 0.35, y + h * 1.35), (x + w * 0.6, y + h * 1.45)], lw=1.0, amp=0)
    k.circle(x - w * 0.3, y + h * 1.0, w * 0.22, lw=0.5, fill=Wt)

def chair(k, x, y, w, facing=1, cushion=True):
    """Simple wooden kitchen chair in three-quarter view, back on the far side."""
    f = facing; X = lambda u: x + f * u * w; h = w * 1.9
    seat = [(X(-0.5), y + h * 0.42), (X(0.42), y + h * 0.42), (X(0.5), y + h * 0.48), (X(-0.42), y + h * 0.48)]
    for u, top in [(-0.46, 0.42), (0.4, 0.42)]:
        k.line([(X(u), y), (X(u), y + h * top)], lw=1.3, amp=0)
    for u in (-0.38, 0.46):
        k.line([(X(u), y + h * 0.06), (X(u), y + h * 0.45)], lw=1.0, amp=0)
    k.line([(X(-0.46), y + h * 0.14), (X(0.4), y + h * 0.14)], lw=0.6, amp=0)
    k.shape(seat, lw=0.9, fill=Wt, amp=0)
    if cushion:
        cu = [(X(-0.44), y + h * 0.48), (X(0.4), y + h * 0.48), (X(0.44), y + h * 0.53), (X(-0.38), y + h * 0.53)]
        k.shape(cu, lw=0.7, fill=Wt, amp=0.1); k.hatch(cu, angle=45, gap=1.6, lw=0.3, cross=True); k.shape(cu, lw=0.7, fill=None, amp=0.1)
    # back
    k.line([(X(-0.42), y + h * 0.48), (X(-0.42), y + h)], lw=1.3, amp=0)
    k.line([(X(0.5), y + h * 0.48), (X(0.5), y + h)], lw=1.3, amp=0)
    k.shape([(X(-0.46), y + h * 0.93), (X(0.54), y + h * 0.93), (X(0.54), y + h * 1.02), (X(-0.46), y + h * 1.02)], lw=0.8, fill=Wt, amp=0)
    for i in range(1, 4):
        xx = lerp(X(-0.42), X(0.5), i / 4); k.line([(xx, y + h * 0.53), (xx, y + h * 0.93)], lw=0.6, amp=0)

def table(k, x0, x1, ytop, h, cloth=True):
    k.shape([(x0, ytop), (x1, ytop), (x1 - 2, ytop - 4), (x0 + 2, ytop - 4)], lw=0.9, fill=Wt, amp=0)
    for xx in (x0 + 8, x1 - 8):
        k.shape([(xx - 2.5, ytop - 4), (xx + 2.5, ytop - 4), (xx + 1.8, ytop - h), (xx - 1.8, ytop - h)], lw=0.8, fill=Wt, amp=0)
        k.hatch([(xx, ytop - 4), (xx + 2.5, ytop - 4), (xx + 1.8, ytop - h), (xx, ytop - h)], angle=90, gap=1.0, lw=0.3)
    if cloth:
        w = x1 - x0; cx = (x0 + x1) / 2
        run = [(cx - w * 0.2, ytop + 0.5), (cx + w * 0.2, ytop + 0.5), (cx + w * 0.2, ytop - h * 0.32), (cx - w * 0.2, ytop - h * 0.32)]
        k.shape(run, lw=0.7, fill=Wt, amp=0)
        k.hatch(run, angle=0, gap=2.4, lw=0.35); k.hatch(run, angle=90, gap=2.4, lw=0.35)
        for i in range(9):
            xx = lerp(cx - w * 0.2, cx + w * 0.2, i / 8); k.line([(xx, ytop - h * 0.32), (xx, ytop - h * 0.36)], lw=0.4, amp=0)

def hanging_lamp(k, x, ytop, L, w):
    k.line([(x, ytop), (x, ytop - L)], lw=0.6, amp=0)
    sh = [(x - w / 2, ytop - L - w * 0.45), (x + w / 2, ytop - L - w * 0.45)] + k.arcpts(x, ytop - L - w * 0.45, w / 2, w * 0.5, 0, 180, 20)[1:-1]
    k.shape(sh, lw=0.9, fill=K, amp=0)
    k.line(k.arcpts(x, ytop - L - w * 0.45, w * 0.35, w * 0.33, 25, 75, 8), lw=0.6, amp=0, color=Wt)
    k.shape(k.arcpts(x, ytop - L - w * 0.47, w * 0.15, w * 0.08, 180, 360, 10), lw=0.6, fill=Wt, amp=0)
    for i in range(7):
        a = math.radians(lerp(-150, -30, i / 6)); r0 = w * 0.6; r1 = w * 0.85
        k.line([(x + r0 * math.cos(a), ytop - L - w * 0.5 + r0 * math.sin(a) * 0.6), (x + r1 * math.cos(a), ytop - L - w * 0.5 + r1 * math.sin(a) * 0.6)], lw=0.4, amp=0)

def vase(k, x, y, h, flowers="mixed"):
    w = h * 0.42
    body = k.arcpts(x, y + h * 0.35, w / 2, h * 0.35, -90, 90, 14) + [(x + w * 0.18, y + h * 0.75), (x + w * 0.24, y + h * 0.82), (x - w * 0.24, y + h * 0.82), (x - w * 0.18, y + h * 0.75)] + k.arcpts(x, y + h * 0.35, w / 2, h * 0.35, 90, 270, 14)
    stems = []
    for i in range(7):
        a = math.radians(lerp(60, 120, i / 6) + k.r.uniform(-5, 5)); L = h * k.r.uniform(0.8, 1.2)
        stems.append((x + L * math.cos(a), y + h * 0.8 + L * math.sin(a)))
        k.line([(x, y + h * 0.75), stems[-1]], lw=0.55, amp=0.1)
    for i, (sx, sy) in enumerate(stems):
        if i % 3 == 0: daisy(k, sx, sy, h * 0.13)
        elif i % 3 == 1: flower(k, sx, sy, h * 0.09, lw=0.45)
        else:
            for j in range(4): k.circle(sx + h * 0.04 * math.cos(j * 1.6), sy + h * 0.05 * j * 0.4, h * 0.035, lw=0.4, fill=Wt)
    for i in range(3):
        leaf(k, x, y + h * 0.82, h * 0.35, lerp(30, 150, i / 2), lw=0.45)
    k.shape(body, lw=0.9, fill=Wt, amp=0)
    k.hatch([p for p in body if p[0] > x + w * 0.1] + [(x + w * 0.1, y + h * 0.2)], angle=80, gap=1.2, lw=0.32)
    k.shape(body, lw=0.9, fill=None, amp=0)
    k.line([(x - w * 0.45, y + h * 0.4), (x + w * 0.45, y + h * 0.4)], lw=0.5, amp=0)

def garden_window(k, x, y, w, h, view="spring"):
    """Window with a sash, tie-back curtains and a seasonal view outside."""
    k.rect(x - 4, y - 4, w + 8, h + 8, lw=1.1)
    k.rect(x, y, w, h, lw=0.8)
    c = k.c; c.saveState(); p = c.beginPath(); p.rect(x, y, w, h); c.clipPath(p, stroke=0, fill=0)
    if view == "spring":
        pts = k.hills(x, x + w, y + h * 0.32, amp=6, n=2)
        k.shape([(x, y)] + pts + [(x + w, y)], lw=0.7, fill=Wt, amp=0)
        tree(k, x + w * 0.72, y + h * 0.28, h * 0.62, kind="blossom")
        cloud(k, x + w * 0.28, y + h * 0.8, w * 0.32)
        birds(k, [(x + w * 0.45, y + h * 0.66), (x + w * 0.53, y + h * 0.7)], s=3)
        picket(k, x - 2, x + w + 2, y + h * 0.05, h * 0.16)
    elif view == "rain":
        pts = k.hills(x, x + w, y + h * 0.3, amp=5, n=2)
        k.shape([(x, y)] + pts + [(x + w, y)], lw=0.7, fill=Wt, amp=0)
        tree(k, x + w * 0.3, y + h * 0.25, h * 0.55, kind="leafy")
        for i in range(70):
            rx, ry = k.r.uniform(x, x + w), k.r.uniform(y, y + h)
            k.line([(rx, ry), (rx - 1.2, ry - 4)], lw=0.4, amp=0)
        cloud(k, x + w * 0.65, y + h * 0.86, w * 0.4)
    elif view == "autumn":
        pts = k.hills(x, x + w, y + h * 0.3, amp=5, n=2)
        k.shape([(x, y)] + pts + [(x + w, y)], lw=0.7, fill=Wt, amp=0)
        tree(k, x + w * 0.3, y + h * 0.22, h * 0.6, kind="autumn")
        tree(k, x + w * 0.78, y + h * 0.26, h * 0.4, kind="autumn")
        for i in range(6):
            maple(k, k.r.uniform(x + 4, x + w - 4), k.r.uniform(y + h * 0.1, y + h * 0.8), 5, ang=k.r.uniform(-70, 70), fill=K if i % 2 else Wt)
        birds(k, [(x + w * 0.55, y + h * 0.8), (x + w * 0.63, y + h * 0.84)], s=3)
    c.restoreState()
    c.setStrokeColor(K); c.setLineWidth(1.4); c.line(x + w / 2, y, x + w / 2, y + h); c.line(x, y + h * 0.5, x + w, y + h * 0.5)
    k.rect(x - 7, y - 8, w + 14, 4.5, lw=0.9)
    for sx in (-1, 1):
        ex = x if sx < 0 else x + w
        cur = [(ex - sx * 5, y + h + 8), (ex + sx * w * 0.2, y + h + 8), (ex + sx * w * 0.06, y + h * 0.42), (ex + sx * w * 0.14, y - 2), (ex - sx * 5, y - 2)]
        k.shape(cur, lw=0.8, fill=Wt, amp=0.2)
        for j in range(3):
            u = (j + 1) / 4
            k.line([(ex - sx * 5 + sx * w * 0.22 * u, y + h + 7), (ex + sx * w * 0.03 * (1 + u), y + h * 0.42), (ex + sx * w * 0.12 * u, y - 1)], lw=0.35, amp=0.2)
        k.circle(ex + sx * w * 0.06, y + h * 0.42, 1.6, lw=0.5, fill=K)
    k.rect(x - 8, y + h + 8, w + 16, 3.2, lw=0.8, fill=K)

def string_lights(k, x0, x1, y, sag=10, n=11):
    pts = [(lerp(x0, x1, t), y - sag * math.sin(math.pi * t)) for t in [i / 40 for i in range(41)]]
    k.line(pts, lw=0.5, amp=0)
    for i in range(1, n):
        t = i / n; bx, by = lerp(x0, x1, t), y - sag * math.sin(math.pi * t)
        k.shape(k.arcpts(bx, by - 3.2, 1.6, 2.6, 0, 360, 10), lw=0.5, fill=Wt, amp=0)
        k.rect(bx - 1, by - 1, 2, 1.2, lw=0.3, fill=K)
        for a in (-60, -90, -120):
            r = math.radians(a); k.line([(bx + 4 * math.cos(r), by - 3.2 + 4 * math.sin(r)), (bx + 6 * math.cos(r), by - 3.2 + 6 * math.sin(r))], lw=0.3, amp=0)

def corner_sprigs(k, x0, y0, x1, y1):
    k.c.setStrokeColor(K); k.c.setLineWidth(1.3); k.c.rect(x0, y0, x1 - x0, y1 - y0, stroke=1, fill=0)
    k.c.setLineWidth(0.45); k.c.rect(x0 + 3.2, y0 + 3.2, x1 - x0 - 6.4, y1 - y0 - 6.4, stroke=1, fill=0)
    for (cx, cy, a) in [(x0, y0, 45), (x1, y0, 135), (x0, y1, -45), (x1, y1, -135)]:
        k.c.setFillColor(Wt); k.c.circle(cx, cy, 7.5, stroke=0, fill=1)
        heart(k, cx, cy - 3.2, 8.5, fill=K, lw=0.3)

# ----------------------------------------------------------------------------- scenes
def half_title(k, w, h):
    teacup(k, w * 0.33, h * 0.14, w * 0.3, pattern="dots")
    mug2(k, w * 0.66, h * 0.14, w * 0.26)
    heart(k, w * 0.5, h * 0.8, w * 0.07, fill=K)

def frontispiece(k, w, h):
    """The kitchen table by the window: two cups, a teapot, flowers, two chairs, a cat on the sill."""
    m = 14
    corner_sprigs(k, m, m, w - m, h - m)
    # back wall: wainscot + wallpaper dots
    k.line([(m + 4, h * 0.36), (w - m - 4, h * 0.36)], lw=0.7, amp=0)
    k.c.saveState(); p = k.c.beginPath(); p.rect(m + 4, m + 4, w - 2 * m - 8, h * 0.36 - m - 4); k.c.clipPath(p, stroke=0, fill=0)
    for i in range(int((w - 2 * m) / 9) + 1):
        xx = m + 4 + i * 9; k.line([(xx, m + 4), (xx, h * 0.36)], lw=0.35, amp=0)
    k.c.restoreState()
    for i in range(9):
        for j in range(6):
            xx = m + 22 + i * (w - 2 * m - 40) / 8 + (8 if j % 2 else 0); yy = h * 0.42 + j * (h * 0.5) / 5.5
            if (w * 0.24 < xx < w * 0.76 and h * 0.47 < yy < h * 0.86): continue
            flower(k, xx, yy, 2.2, lw=0.3)
    # window
    garden_window(k, w * 0.25, h * 0.5, w * 0.5, h * 0.32, view="spring")
    k.cat(w * 0.66, h * 0.5 - 3.5, 30)
    pot(k, w * 0.33, h * 0.5 - 3.5, 16, plant="tulips")
    # hanging lamp
    hanging_lamp(k, w * 0.5, h - m - 4, h * 0.05, 34)
    # table and chairs
    chair(k, w * 0.16, m + 26, w * 0.18, facing=1)
    chair(k, w * 0.84, m + 26, w * 0.18, facing=-1)
    table(k, w * 0.2, w * 0.8, h * 0.3, h * 0.22)
    teapot2(k, w * 0.5, h * 0.3 + 1, w * 0.17)
    teacup(k, w * 0.33, h * 0.3 - 1, w * 0.1, pattern="dots")
    mug2(k, w * 0.67, h * 0.3 + 1, w * 0.085)
    vase(k, w * 0.43, h * 0.3 + 1, w * 0.08)
    # floor
    k.line([(m + 4, m + 26), (w - m - 4, m + 26)], lw=0.7, amp=0)
    for i in range(1, 8):
        k.line([(m + 4 + (w - 2 * m) * i / 8, m + 4), (m + 4 + (w - 2 * m) * i / 8 + 6, m + 26)], lw=0.35, amp=0)
    k.rug(w * 0.5, m + 18, w * 0.5, 14)

def title_art(k, w, h):
    teapot2(k, w * 0.5, h * 0.12, w * 0.3)
    teacup(k, w * 0.2, h * 0.08, w * 0.2, pattern="band")
    mug2(k, w * 0.8, h * 0.08, w * 0.16)
    for i, a in enumerate((150, 30)):
        leaf(k, w * 0.5 + (-1 if i == 0 else 1) * w * 0.38, h * 0.82, w * 0.08, a, lw=0.5)
    heart(k, w * 0.5, h * 0.86, w * 0.05)
    k.line([(w * 0.08, h * 0.06), (w * 0.92, h * 0.06)], lw=0.6, amp=0.2)

def opener_spring(k, w, h):
    m = 12
    corner_sprigs(k, m, m, w - m, h - m)
    k.clip_rect(m + 4, m + 4, w - m - 4, h - m - 4)
    sun(k, w * 0.8, h * 0.82, 16)
    cloud(k, w * 0.3, h * 0.84, w * 0.26); cloud(k, w * 0.6, h * 0.72, w * 0.18)
    birds(k, [(w * 0.5, h * 0.88), (w * 0.57, h * 0.85), (w * 0.62, h * 0.9)], s=4)
    pts = k.hills(m, w - m, h * 0.5, amp=10, n=2)
    k.shape([(m, h * 0.3)] + pts + [(w - m, h * 0.3)], lw=0.8, fill=Wt, amp=0)
    k.cottage(w * 0.12, h * 0.46, w * 0.22, h * 0.17, chimney=True)
    tree(k, w * 0.72, h * 0.3, h * 0.52, kind="blossom")
    tree(k, w * 0.42, h * 0.45, h * 0.18, kind="leafy")
    k.line([(m, h * 0.3), (w - m, h * 0.3)], lw=0.7, amp=0.3)
    # garden bench with two cups
    k.bench(w * 0.4, h * 0.3, w * 0.34)
    teacup(k, w * 0.33, h * 0.3 + w * 0.13, w * 0.06, steam_=True, pattern="dots")
    mug2(k, w * 0.46, h * 0.3 + w * 0.135, w * 0.05)
    picket(k, m, w * 0.24, h * 0.3, h * 0.08)
    picket(k, w * 0.6, w - m, h * 0.3, h * 0.08)
    for i in range(14):
        x = lerp(w * 0.06, w * 0.94, i / 13) + k.r.uniform(-4, 4)
        tulip(k, x, h * 0.1 + k.r.uniform(0, 12), h * k.r.uniform(0.1, 0.14), lean=k.r.uniform(-0.15, 0.15), lw=0.6, dark=(i % 3 == 1))
    grass(k, m, w - m, h * 0.1, n=80, hmax=6)
    watering_can(k, w * 0.86, h * 0.22, w * 0.1)
    songbird(k, w * 0.62, h * 0.33 + w * 0.02, 5, facing=-1)
    k.unclip()

def opener_summer(k, w, h):
    m = 12
    corner_sprigs(k, m, m, w - m, h - m)
    k.clip_rect(m + 4, m + 4, w - m - 4, h - m - 4)
    sun(k, w * 0.2, h * 0.82, 18)
    cloud(k, w * 0.62, h * 0.86, w * 0.24)
    kite(k, w * 0.74, h * 0.66, w * 0.1)
    # sea with a sailboat
    k.line([(m, h * 0.5), (w - m, h * 0.5)], lw=0.7, amp=0.2)
    waves(k, m, w * 0.6, h * 0.47, rows=4, gap=6)
    sailboat(k, w * 0.3, h * 0.5, w * 0.12)
    sailboat(k, w * 0.5, h * 0.5, w * 0.06)
    head = [(w * 0.02, h * 0.5)] + [(lerp(w * 0.02, w * 0.2, t), h * 0.5 + h * 0.07 * math.sin(math.pi * t) ** 0.6) for t in [i / 20 for i in range(21)]]
    k.shape(head + [(w * 0.2, h * 0.49)], lw=0.8, fill=Wt, amp=0.2)
    k.hatch(head[10:] + [(w * 0.2, h * 0.5)], angle=-60, gap=1.6, lw=0.35)
    lx, ly = w * 0.1, h * 0.565; lh = h * 0.13
    k.shape([(lx - 5, ly), (lx + 5, ly), (lx + 3, ly + lh), (lx - 3, ly + lh)], lw=0.8, fill=Wt, amp=0)
    for v in (0.25, 0.55): k.shape([(lx - 5 + 2 * v, ly + lh * v), (lx + 5 - 2 * v, ly + lh * v), (lx + 4.6 - 2 * v, ly + lh * (v + 0.13)), (lx - 4.6 + 2 * v, ly + lh * (v + 0.13))], lw=0.5, fill=K, amp=0)
    k.rect(lx - 3.5, ly + lh, 7, 5, lw=0.7); k.shape([(lx - 4.5, ly + lh + 5), (lx + 4.5, ly + lh + 5), (lx, ly + lh + 10)], lw=0.7, fill=K, amp=0)
    for a in (-15, 0, 15): k.line([(lx + 6, ly + lh + 2.5), (lx + 22, ly + lh + 2.5 + 22 * math.tan(math.radians(a)))], lw=0.35, amp=0)
    # hill
    pts = [(lerp(w * 0.35, w - m, t), h * 0.24 + h * 0.24 * math.sin(math.pi * 0.5 * (1 - t)) ** 0.5 * (1 - 0.3 * t)) for t in [i / 40 for i in range(41)]]
    hill = [(w * 0.35, h * 0.2)] + pts + [(w - m, h * 0.1), (m, h * 0.1), (m, h * 0.3)]
    pts2 = k.hills(m, w - m, h * 0.3, amp=4, n=1)
    k.shape([(m, m)] + pts2 + [(w - m, m)], lw=0.8, fill=Wt, amp=0)
    tree(k, w * 0.82, h * 0.27, h * 0.45, kind="leafy")
    # beach umbrella
    ux, uy = w * 0.2, h * 0.11
    k.line([(ux, uy), (ux + 4, uy + h * 0.3 + h * 0.07)], lw=1.1, amp=0)
    cx, base, R, H = ux + 4, uy + h * 0.3, w * 0.13, h * 0.07
    apex = (cx, base + H)
    def rib(xe):
        bulge = (xe - cx) * 0.25
        return [((1 - t) ** 2 * cx + 2 * (1 - t) * t * (xe + bulge * 0.2) + t * t * xe, (1 - t) ** 2 * (base + H) + 2 * (1 - t) * t * (base + H * 0.9) + t * t * base) for t in [i / 10 for i in range(11)]]
    edges = [cx - R + 2 * R * i / 6 for i in range(7)]
    outline = rib(edges[0])[::-1] + rib(edges[-1])
    k.shape(rib(edges[0]) + [(edges[-1], base)] + rib(edges[-1])[::-1], lw=0.9, amp=0)
    for i in range(6):
        if i % 2 == 0:
            k.hatch(rib(edges[i]) + rib(edges[i + 1])[::-1], angle=90, gap=1.3, lw=0.35)
    for e in edges[1:-1]: k.line(rib(e), lw=0.5, amp=0)
    for i in range(6):
        k.line(k.arcpts((edges[i] + edges[i + 1]) / 2, base, R / 6, 2.5, 180, 360, 6), lw=0.6, amp=0)
    blanket(k, [(w * 0.18, h * 0.12), (w * 0.66, h * 0.12), (w * 0.6, h * 0.25), (w * 0.26, h * 0.25)])
    basket(k, w * 0.32, h * 0.17, w * 0.15)
    jug(k, w * 0.5, h * 0.17, w * 0.1)
    glass(k, w * 0.58, h * 0.155, w * 0.06)
    glass(k, w * 0.43, h * 0.15, w * 0.06)
    for i in range(3): apple(k, w * (0.22 + 0.04 * i), h * 0.14, 3.2, dark=(i == 1))
    grass(k, m, w - m, h * 0.07, n=70, hmax=6)
    for i in range(6): daisy(k, lerp(w * 0.68, w * 0.92, i / 5), h * 0.08 + k.r.uniform(0, 8), 3.0)
    k.unclip()

def opener_autumn(k, w, h):
    m = 12
    corner_sprigs(k, m, m, w - m, h - m)
    k.clip_rect(m + 4, m + 4, w - m - 4, h - m - 4)
    # porch: board wall with a window onto an autumn garden, posts, a beam and string lights
    k.wall(m, h * 0.28, w - 2 * m, h * 0.55, gap=4.2)
    garden_window(k, w * 0.36, h * 0.45, w * 0.28, h * 0.26, view="autumn")
    k.shape([(m, h * 0.83), (w - m, h * 0.83), (w - m, h * 0.9), (m, h * 0.9)], lw=0.9, fill=Wt, amp=0)
    k.hatch([(m, h * 0.83), (w - m, h * 0.83), (w - m, h * 0.9), (m, h * 0.9)], angle=0, gap=1.5, lw=0.35)
    for xx in (w * 0.12, w * 0.88):
        k.shape([(xx - 4, h * 0.2), (xx + 4, h * 0.2), (xx + 4, h * 0.83), (xx - 4, h * 0.83)], lw=0.9, fill=Wt, amp=0)
        k.hatch([(xx, h * 0.2), (xx + 4, h * 0.2), (xx + 4, h * 0.83), (xx, h * 0.83)], angle=90, gap=1.2, lw=0.3)
    string_lights(k, w * 0.14, w * 0.86, h * 0.8, sag=12, n=13)
    # wreath of leaves on the post? a hanging fern basket instead
    for sx in (0.22, 0.78):
        k.line([(w * sx, h * 0.83), (w * sx, h * 0.76)], lw=0.4, amp=0)
        pot(k, w * sx, h * 0.68, 14, plant="herb")
    # porch floor
    k.shape([(m, h * 0.2), (w - m, h * 0.2), (w - m, h * 0.28), (m, h * 0.28)], lw=0.8, fill=Wt, amp=0)
    for i in range(12): k.line([(m + (w - 2 * m) * i / 12, h * 0.2), (m + (w - 2 * m) * i / 12 + 6, h * 0.28)], lw=0.35, amp=0)
    rocking_chair(k, w * 0.27, h * 0.25, w * 0.2, facing=1)
    rocking_chair(k, w * 0.73, h * 0.25, w * 0.2, facing=-1)
    top = k.side_table(w * 0.5, h * 0.25, w * 0.11)
    teacup(k, w * 0.47, top - 1, w * 0.05, pattern="dots"); mug2(k, w * 0.535, top, w * 0.042)
    # porch steps with pumpkins, a basket of apples and fallen leaves
    k.shape([(m, m), (w - m, m), (w - m, h * 0.2), (m, h * 0.2)], lw=0.8, fill=Wt, amp=0)
    for j in range(1, 3):
        yy = m + (h * 0.2 - m) * j / 3
        k.line([(m, yy), (w - m, yy)], lw=0.7, amp=0.1)
        k.hatch([(m, yy - 4), (w - m, yy - 4), (w - m, yy), (m, yy)], angle=0, gap=1.2, lw=0.3)
    pumpkin(k, w * 0.12, h * 0.135, w * 0.13)
    pumpkin(k, w * 0.22, h * 0.07, w * 0.1)
    pumpkin(k, w * 0.88, h * 0.135, w * 0.11)
    basket(k, w * 0.78, h * 0.065, w * 0.12)
    for i in range(4): apple(k, w * (0.745 + 0.023 * i), h * 0.065 + w * 0.12 * 0.62 + (i % 2) * 2, 3.3, dark=(i % 2 == 0))
    for i in range(16):
        maple(k, k.r.uniform(w * 0.3, w * 0.7), k.r.uniform(m + 4, h * 0.19), k.r.uniform(7, 10), ang=k.r.uniform(-80, 80), fill=K if i % 3 == 0 else Wt)
    for i in range(5):
        maple(k, k.r.uniform(w * 0.18, w * 0.82), k.r.uniform(h * 0.28, h * 0.42), k.r.uniform(6, 8), ang=k.r.uniform(-80, 80), fill=K if i % 2 else Wt)
    k.unclip()

def opener_winter(k, w, h):
    m = 12
    corner_sprigs(k, m, m, w - m, h - m)
    k.clip_rect(m + 4, m + 4, w - m - 4, h - m - 4)
    k.window_snow(w * 0.76, h * 0.5, w * 0.15, h * 0.3, panes=(2, 3), curtains=True)
    k.bookshelf(w * 0.07, h * 0.45, w * 0.17, h * 0.4, shelves=4)
    k.fireplace(w * 0.29, h * 0.24, w * 0.42, h * 0.46, fire=True, stockings=2)
    k.garland(w * 0.28, w * 0.72, h * 0.72, sag=8, swags=2)
    k.candle(w * 0.34, h * 0.705, 18); k.candle(w * 0.66, h * 0.705, 18)
    k.armchair(w * 0.19, h * 0.1, w * 0.25, facing=1)
    k.armchair(w * 0.81, h * 0.1, w * 0.25, facing=-1)
    k.rug(w * 0.5, h * 0.12, w * 0.42, 22)
    top = k.side_table(w * 0.5, h * 0.05, w * 0.13)
    mug2(k, w * 0.465, top, w * 0.05); mug2(k, w * 0.54, top, w * 0.05)
    k.cat(w * 0.33, h * 0.04, 26)
    k.floor_lamp(w * 0.93, h * 0.1, h * 0.4)
    k.line([(m, h * 0.24), (w * 0.29 - 4, h * 0.24)], lw=0.6, amp=0.1); k.line([(w * 0.71 + 4, h * 0.24), (w - m, h * 0.24)], lw=0.6, amp=0.1)
    k.unclip()

def interlude_spring(k, w, h):
    """Rainy windowsill: potted tulips, daisies and herbs, a teacup on the sill."""
    garden_window(k, w * 0.15, h * 0.35, w * 0.7, h * 0.55, view="rain")
    sill = h * 0.35 - 8 + 3.2
    pot(k, w * 0.26, sill, w * 0.12, plant="tulips")
    pot(k, w * 0.5, sill, w * 0.1, plant="herb")
    pot(k, w * 0.74, sill, w * 0.12, plant="daisies")
    teacup(k, w * 0.38, sill, w * 0.09, pattern="band")
    mug2(k, w * 0.62, sill, w * 0.07)
    songbird(k, w * 0.66, h * 0.62, 6, facing=-1) if False else None

def interlude_summer(k, w, h):
    """Two deck chairs on the sand at sunset."""
    k.line([(0, h * 0.45), (w, h * 0.45)], lw=0.7, amp=0.2)
    k.circle(w * 0.5, h * 0.45, w * 0.14, lw=0.9, fill=Wt)
    k.c.saveState(); p = k.c.beginPath(); p.rect(0, h * 0.45, w, h); k.c.clipPath(p, stroke=0, fill=0)
    k.hatch(k.arcpts(w * 0.5, h * 0.45, w * 0.14, w * 0.14, 0, 180, 30), angle=0, gap=2.2, lw=0.4)
    k.c.restoreState()
    k.blob([(0, h * 0.45 - 0.1), (w, h * 0.45 - 0.1), (w, h * 0.44 - 0.2), (0, h * 0.44 - 0.2)], Wt)
    for i in range(6):
        yy = h * 0.43 - i * 4; L = w * (0.28 - 0.03 * i)
        k.line([(w * 0.5 - L / 2, yy), (w * 0.5 + L / 2, yy)], lw=0.5, amp=0)
    waves(k, 0, w, h * 0.36, rows=2, gap=5)
    birds(k, [(w * 0.3, h * 0.75), (w * 0.37, h * 0.8), (w * 0.7, h * 0.72)], s=4)
    k.line([(0, h * 0.25), (w, h * 0.28)], lw=0.7, amp=0.3)
    for sx, f in ((0.35, 1), (0.65, -1)):
        x = w * sx; y = h * 0.1; cw = w * 0.16
        X = lambda u: x + f * u * cw
        k.line([(X(-0.5), y), (X(0.2), y + cw * 0.9)], lw=1.2, amp=0)
        k.line([(X(0.4), y), (X(-0.2), y + cw * 0.5)], lw=1.2, amp=0)
        canvas_ = [(X(-0.35), y + cw * 0.25), (X(0.15), y + cw * 1.0), (X(0.4), y + cw * 0.92), (X(0.0), y + cw * 0.2)]
        k.shape(canvas_, lw=0.8, fill=Wt, amp=0)
        k.hatch(canvas_, angle=90 - 30 * f, gap=2.5, lw=0.4)
    glass(k, w * 0.5, h * 0.12, w * 0.07)
    k.ground(0, w, h * 0.06, drifts=0, ticks=False, depth=10)

def interlude_autumn(k, w, h):
    """Reading nook: armchair, lamp, books and two cups on a table, leaves at the window."""
    garden_window(k, w * 0.2, h * 0.62, w * 0.3, h * 0.28, view="autumn")
    k.bookshelf(w * 0.62, h * 0.12, w * 0.3, h * 0.62, shelves=5)
    k.floor_lamp(w * 0.1, h * 0.1, h * 0.62)
    k.armchair(w * 0.3, h * 0.1, w * 0.34, facing=1)
    top = k.side_table(w * 0.52, h * 0.1, w * 0.13)
    teacup(k, w * 0.49, top - 1, w * 0.055, pattern="dots"); mug2(k, w * 0.56, top, w * 0.048)
    k.books(w * 0.3, h * 0.1 + w * 0.34 * 0.5, w * 0.12, n=2)
    k.line([(0, h * 0.1), (w, h * 0.1)], lw=0.7, amp=0.2)
    k.rug(w * 0.4, h * 0.06, w * 0.5, 12)

def checkin_art(k, w, h):
    teacup(k, w * 0.35, h * 0.1, w * 0.24, pattern="heart")
    mug2(k, w * 0.67, h * 0.1, w * 0.22)

def review_art(k, w, h):
    for i, (dx, kind) in enumerate([(0.15, "blossom"), (0.38, "leafy"), (0.62, "autumn"), (0.85, "bare")]):
        tree(k, w * dx, h * 0.1, h * 0.75, kind=kind)
    k.line([(0, h * 0.1), (w, h * 0.1)], lw=0.7, amp=0.2)
    grass(k, 0, w, h * 0.1, n=50, hmax=4)

def love_envelope(k, x, y, ew):
    eh = ew * 0.62
    k.rect(x - ew / 2, y, ew, eh, lw=0.9)
    k.line([(x - ew / 2, y + eh), (x, y + eh * 0.42), (x + ew / 2, y + eh)], lw=0.8, amp=0.1)
    k.line([(x - ew / 2, y), (x - ew * 0.08, y + eh * 0.48)], lw=0.5, amp=0); k.line([(x + ew / 2, y), (x + ew * 0.08, y + eh * 0.48)], lw=0.5, amp=0)
    k.circle(x, y + eh * 0.42, ew * 0.08, lw=0.7, fill=K)
    heart(k, x, y + eh * 0.42, ew * 0.09, fill=Wt, lw=0.3)

def letters_art(k, w, h):
    love_envelope(k, w * 0.35, h * 0.15, w * 0.36)
    love_envelope(k, w * 0.65, h * 0.25, w * 0.36)
    heart(k, w * 0.5, h * 0.82, w * 0.08)

def thanks_art(k, w, h):
    teapot2(k, w * 0.5, h * 0.12, w * 0.38)
    teacup(k, w * 0.16, h * 0.08, w * 0.22, pattern="dots"); mug2(k, w * 0.84, h * 0.08, w * 0.18)
    k.line([(w * 0.02, h * 0.07), (w * 0.98, h * 0.07)], lw=0.6, amp=0.2)

# --- small vignettes (16, four per season) and the two partner icons
def v_tulips(k, w, h): pot(k, w * 0.5, h * 0.06, w * 0.38, plant="tulips")
def v_can(k, w, h): watering_can(k, w * 0.42, h * 0.1, w * 0.55)
def v_bird(k, w, h):
    k.line([(w * 0.05, h * 0.3), (w * 0.95, h * 0.38)], lw=1.4, amp=0.3)
    for i in range(5): leaf(k, lerp(w * 0.1, w * 0.9, i / 4), lerp(h * 0.3, h * 0.38, i / 4), w * 0.16, -60 if i % 2 else -110, lw=0.5)
    for i in range(3): flower(k, lerp(w * 0.15, w * 0.85, i / 2), h * 0.38 + 6, 3.2, lw=0.4)
    songbird(k, w * 0.5, h * 0.36 + 9, w * 0.1, facing=1)
def v_cupflowers(k, w, h):
    teacup(k, w * 0.5, h * 0.08, w * 0.5, steam_=False, pattern="band")
    for i in range(5): flower(k, w * (0.32 + 0.09 * i), h * 0.58 + (i % 2) * 6, w * 0.05, lw=0.45)
def v_basket(k, w, h): basket(k, w * 0.5, h * 0.08, w * 0.62)
def v_kite(k, w, h): kite(k, w * 0.5, h * 0.38, w * 0.38)
def v_lemonade(k, w, h):
    jug(k, w * 0.38, h * 0.08, h * 0.68); glass(k, w * 0.72, h * 0.08, h * 0.42)
def v_boat(k, w, h):
    sailboat(k, w * 0.5, h * 0.3, w * 0.5); waves(k, w * 0.1, w * 0.9, h * 0.28, rows=3, gap=5)
def v_pumpkin(k, w, h): pumpkin(k, w * 0.5, h * 0.08, w * 0.62)
def v_leaves(k, w, h):
    for i, (dx, dy, a, f) in enumerate([(0.3, 0.45, -20, Wt), (0.62, 0.55, 25, K), (0.48, 0.2, 5, Wt)]):
        maple(k, w * dx, h * dy, w * 0.32, ang=a, fill=f)
def v_apples(k, w, h):
    basket(k, w * 0.5, h * 0.08, w * 0.6)
    for i in range(4): apple(k, w * (0.3 + 0.13 * i), h * 0.5 + (i % 2) * 4, w * 0.07, dark=(i % 2 == 1))
def v_acorns(k, w, h):
    for i, (dx, s) in enumerate([(0.3, 0.3), (0.55, 0.38), (0.78, 0.26)]): acorn(k, w * dx, h * 0.12, w * s)
    leaf(k, w * 0.1, h * 0.15, w * 0.32, 20, lw=0.5)
def v_mugs(k, w, h): mug2(k, w * 0.33, h * 0.08, w * 0.34); mug2(k, w * 0.7, h * 0.08, w * 0.3)
def v_candle(k, w, h):
    k.candle(w * 0.42, h * 0.08, h * 0.65)
    for i in range(3): k.sparkle(w * (0.2 + 0.3 * i), h * (0.75 + 0.06 * (i % 2)), 3)
def v_teapot(k, w, h): teapot2(k, w * 0.5, h * 0.1, w * 0.62)
def v_mittens(k, w, h):
    for sx, side in ((0.3, 1), (0.7, -1)):
        x, y = w * sx, h * 0.12; mw = w * 0.26
        tx = x + side * mw * 0.5
        k.shape(k.arcpts(tx, y + mw * 0.72, mw * 0.17, mw * 0.3, 0, 360, 16), lw=0.85, fill=Wt, amp=0)
        body = k.arcpts(x, y + mw * 1.1, mw / 2, mw * 0.55, 0, 180, 16) + [(x - mw / 2, y + mw * 0.3), (x + mw / 2, y + mw * 0.3)]
        k.shape(body, lw=0.9, fill=Wt, amp=0)
        for j in range(3): k.line([(x - mw * 0.5, y + mw * (0.55 + 0.12 * j)), (x + mw * 0.5, y + mw * (0.55 + 0.12 * j))], lw=0.3, amp=0) if j == 1 else None
        heart(k, x, y + mw * 0.95, mw * 0.28, fill=K, lw=0.3)
        cuff = [(x - mw * 0.55, y), (x + mw * 0.55, y), (x + mw * 0.55, y + mw * 0.32), (x - mw * 0.55, y + mw * 0.32)]
        k.shape(cuff, lw=0.8, fill=Wt, amp=0); k.hatch(cuff, angle=90, gap=1.4, lw=0.4)
def icon_teacup(k, w, h): teacup(k, w * 0.48, h * 0.04, w * 0.62, steam_=True, pattern="dots")
def icon_mug(k, w, h): mug2(k, w * 0.44, h * 0.04, h * 0.55)

def cover_scene(k, w, h):
    """Front cover centrepiece: window, table, two cups, teapot and flowers."""
    garden_window(k, w * 0.2, h * 0.38, w * 0.6, h * 0.5, view="spring")
    k.cat(w * 0.7, h * 0.38 - 8 + 3.2 + 1, 34)
    pot(k, w * 0.3, h * 0.38 - 8 + 3.2, 18, plant="tulips")
    table(k, w * 0.04, w * 0.96, h * 0.24, h * 0.2)
    teapot2(k, w * 0.5, h * 0.24 + 1, w * 0.2)
    teacup(k, w * 0.27, h * 0.24 - 1, w * 0.13, pattern="dots")
    mug2(k, w * 0.74, h * 0.24 + 1, w * 0.11)
    vase(k, w * 0.38, h * 0.24 + 1, w * 0.1)
    for i in range(3): apple(k, w * (0.6 + 0.04 * i), h * 0.24 + 4, 4, dark=(i == 1))

SEASON_VIG = {"spring": ["v-tulips", "v-can", "v-bird", "v-cupflowers"],
              "summer": ["v-basket", "v-kite", "v-lemonade", "v-boat"],
              "autumn": ["v-pumpkin", "v-leaves", "v-apples", "v-acorns"],
              "winter": ["v-mugs", "v-candle", "v-teapot", "v-mittens"]}

JOBS = [
    ("half-title", 3.0, 1.9, half_title, 1),
    ("frontispiece", 4.5, 6.6, frontispiece, 2),
    ("title", 4.2, 2.0, title_art, 3),
    ("opener-spring", 4.5, 4.9, opener_spring, 4),
    ("opener-summer", 4.5, 4.9, opener_summer, 5),
    ("opener-autumn", 4.5, 4.9, opener_autumn, 6),
    ("opener-winter", 4.5, 4.9, opener_winter, 7),
    ("interlude-spring", 4.4, 4.6, interlude_spring, 8),
    ("interlude-summer", 4.4, 4.0, interlude_summer, 9),
    ("interlude-autumn", 4.4, 4.4, interlude_autumn, 10),
    ("checkin", 2.0, 1.2, checkin_art, 11),
    ("review", 4.4, 1.6, review_art, 12),
    ("letters", 2.2, 1.4, letters_art, 13),
    ("thanks", 3.2, 1.8, thanks_art, 14),
    ("v-tulips", 1.3, 1.5, v_tulips, 21), ("v-can", 1.4, 1.1, v_can, 22), ("v-bird", 1.5, 1.0, v_bird, 23), ("v-cupflowers", 1.3, 1.2, v_cupflowers, 24),
    ("v-basket", 1.4, 1.2, v_basket, 25), ("v-kite", 1.1, 1.5, v_kite, 26), ("v-lemonade", 1.4, 1.2, v_lemonade, 27), ("v-boat", 1.4, 1.2, v_boat, 28),
    ("v-pumpkin", 1.4, 1.1, v_pumpkin, 29), ("v-leaves", 1.4, 1.2, v_leaves, 30), ("v-apples", 1.4, 1.2, v_apples, 31), ("v-acorns", 1.4, 1.0, v_acorns, 32),
    ("v-mugs", 1.4, 1.1, v_mugs, 33), ("v-candle", 1.0, 1.4, v_candle, 34), ("v-teapot", 1.4, 1.1, v_teapot, 35), ("v-mittens", 1.4, 1.1, v_mittens, 36),
    ("icon-teacup", 0.6, 0.6, icon_teacup, 41), ("icon-mug", 0.6, 0.6, icon_mug, 42),
    ("cover-scene", 4.9, 5.0, cover_scene, 50),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = set(sys.argv[1:])
    for name, wi, hi, fn, seed in JOBS:
        if only and name not in only: continue
        render(os.path.join(OUT, f"{name}.png"), wi, hi, fn, seed=seed, dpi=300)
        print("drew", name)
