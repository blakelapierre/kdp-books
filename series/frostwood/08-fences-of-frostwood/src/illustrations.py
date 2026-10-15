"""Draws the black-and-white ink illustrations for Fences of Frostwood -> ../illustrations/*.png
(300 DPI grayscale, pure black line art on white, same inkart house style as the other Frostwood books).
Subjects: snowed-under village lots, the lodge meadow fences, the mill yard and the high orchard,
with only the numbered fence posts showing above the drifts. No people.
Deterministic: same seeds -> same images. Run from src/: python3 illustrations.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inkart import render, Wt, K, lerp
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "illustrations")


# ----------------------------------------------------------------------------- local helpers
def post(k, x, y, h, w=None, cap=True, tag=None):
    """A square timber fence post with a snow cap and, optionally, a little numbered tag."""
    w = w or max(2.2, h * 0.16)
    body = [(x - w / 2, y), (x + w / 2, y), (x + w / 2, y + h), (x - w / 2, y + h)]
    k.shape(body, lw=0.7, fill=Wt, amp=0.08)
    k.hatch([(x + w * 0.05, y), (x + w / 2, y), (x + w / 2, y + h), (x + w * 0.05, y + h)], angle=90, gap=max(0.9, w * 0.3), lw=0.3, jitter=0.05)
    if cap:
        k.shape([(x - w * 0.75, y + h), (x + w * 0.75, y + h)] + k.arcpts(x, y + h, w * 0.75, w * 0.55, 0, 180, 10)[::-1], lw=0.6, fill=Wt, amp=0.05)
    if tag is not None:
        tw = max(5.5, w * 1.9); th = tw * 0.95; ty = y + h * 0.5
        k.shape([(x - tw / 2, ty - th / 2), (x + tw / 2, ty - th / 2), (x + tw / 2, ty + th / 2), (x - tw / 2, ty + th / 2)], lw=0.7, fill=Wt, amp=0)
        k.circle(x, ty + th / 2 + 1.1, 0.6, lw=0.4, fill=K)
        k.text(x, ty - th * 0.3, str(tag), size=th * 0.82, font="Ink-Plex")


def drift(k, x0, x1, y, hgt, lw=0.8, ticks=True):
    """A rounded snow drift whose top edge is at y + hgt in the middle, covering what is behind it."""
    top = [(lerp(x0, x1, t), y + hgt * math.sin(math.pi * t) ** 0.8 + hgt * 0.06 * math.sin(t * 13 + x0)) for t in [i / 30 for i in range(31)]]
    k.shape([(x0, y - 3)] + top + [(x1, y - 3)], lw=0, fill=Wt, stroke=False, amp=0)
    k.line(top, lw=lw, amp=0.15)
    if ticks:
        for i in range(2, 29, 5):
            px, py = top[i]; k.line([(px, py - 2.2), (px - 1.4, py - 4.6)], lw=0.3, amp=0)
    return top


def buried_posts(k, x0, y0, x1, y1, n, h, tags=None, drifts=True):
    """A line of fence posts poking out of the snow from (x0, y0) to (x1, y1); the rails are buried."""
    pts = []
    for i in range(n):
        t = i / max(1, n - 1); x = lerp(x0, x1, t); y = lerp(y0, y1, t); hh = h * (0.75 + 0.5 * k.r.random())
        post(k, x, y, hh, tag=(tags[i] if tags and i < len(tags) else None)); pts.append((x, y))
    if drifts:
        for i in range(n - 1):
            (xa, ya), (xb, yb) = pts[i], pts[i + 1]
            # a soft hump of snow between neighbouring posts, hiding the rails
            hump = [(lerp(xa, xb, t), lerp(ya, yb, t) + h * 0.18 * math.sin(math.pi * t)) for t in [j / 10 for j in range(11)]]
            k.line(hump[1:-1], lw=0.45, amp=0.1)
    return pts


def rail_fence(k, x0, y0, x1, y1, h, n=None, rails=2, caps=True, lw=0.85):
    """A post-and-rail fence from (x0, y0) to (x1, y1)."""
    L = math.hypot(x1 - x0, y1 - y0); n = n or max(2, int(L / (h * 1.5)) + 1)
    for v in [0.38, 0.78][:rails] if rails <= 2 else [0.25, 0.5, 0.75]:
        k.line([(x0, y0 + h * v), (x1, y1 + h * v)], lw=lw, amp=0.2)
        k.line([(x0, y0 + h * v + 1.4), (x1, y1 + h * v + 1.4)], lw=lw * 0.5, amp=0.2)   # snow on the rail
    for i in range(n):
        t = i / (n - 1); post(k, lerp(x0, x1, t), lerp(y0, y1, t) - h * 0.08, h * 1.02, w=max(2.0, h * 0.13), cap=caps)


def picket(k, x0, x1, y, h, gap=None):
    gap = gap or max(3.2, h * 0.32); n = int((x1 - x0) / gap)
    k.line([(x0, y + h * 0.3), (x0 + n * gap, y + h * 0.3)], lw=0.7, amp=0.1)
    k.line([(x0, y + h * 0.7), (x0 + n * gap, y + h * 0.7)], lw=0.7, amp=0.1)
    pw = gap * 0.55
    for i in range(n + 1):
        xx = x0 + i * gap
        k.shape([(xx - pw / 2, y), (xx + pw / 2, y), (xx + pw / 2, y + h * 0.88), (xx, y + h), (xx - pw / 2, y + h * 0.88)], lw=0.55, fill=Wt, amp=0)
        k.blob([(xx - pw / 2 - 0.3, y + h * 0.86), (xx, y + h + 1.2), (xx + pw / 2 + 0.3, y + h * 0.86), (xx, y + h * 0.97)], Wt)
        k.line([(xx - pw / 2, y + h * 0.88), (xx, y + h + 0.6), (xx + pw / 2, y + h * 0.88)], lw=0.4, amp=0)


def gate(k, x, y, w, h, open_=0.0):
    """A five-bar farm gate between two stout posts (open_ 0 = shut)."""
    post(k, x, y, h * 1.15, w=h * 0.13); post(k, x + w, y, h * 1.15, w=h * 0.13)
    gx1 = x + w * (1 - open_ * 0.6); gy1 = y - open_ * h * 0.18
    for j in range(5):
        v = 0.12 + 0.19 * j
        k.line([(x + 1.5, y + h * v), (gx1 - 1.5, gy1 + h * v)], lw=0.9, amp=0.05)
    k.line([(x + 1.5, y + h * 0.12), (gx1 - 1.5, gy1 + h * 0.88)], lw=0.9, amp=0.05)   # brace
    k.line([(gx1 - 1.5, gy1 + h * 0.1), (gx1 - 1.5, gy1 + h * 0.9)], lw=1.0, amp=0)
    k.line([(x + 1.5, y + h * 0.88 + 1.3), (gx1 - 1.5, gy1 + h * 0.88 + 1.3)], lw=0.45, amp=0.1)


def stile(k, x, y, h):
    """A wooden step stile over a rail fence."""
    rail_fence(k, x - h * 1.8, y, x + h * 1.8, y, h, n=3)
    for sx, sy in ((-0.35, 0.28), (0.35, 0.28)):
        k.shape([(x + sx * h - h * 0.3, y + sy * h), (x + sx * h + h * 0.3, y + sy * h), (x + sx * h + h * 0.3, y + sy * h + 2.2), (x + sx * h - h * 0.3, y + sy * h + 2.2)], lw=0.6, fill=Wt, amp=0)
    k.shape([(x - h * 0.25, y + h * 0.56), (x + h * 0.25, y + h * 0.56), (x + h * 0.25, y + h * 0.56 + 2.2), (x - h * 0.25, y + h * 0.56 + 2.2)], lw=0.6, fill=Wt, amp=0)


def bare_tree(k, x, y, h, lean=0.0, depth=5, spread=0.62):
    """A leafless winter fruit tree: tapered black trunk and branching limbs."""
    def limb(x0, y0, ang, L, wdt, d):
        x1 = x0 + L * math.cos(ang); y1 = y0 + L * math.sin(ang)
        nx, ny = -math.sin(ang) * wdt / 2, math.cos(ang) * wdt / 2
        w2 = wdt * 0.62
        mx, my = -math.sin(ang) * w2 / 2, math.cos(ang) * w2 / 2
        k.blob([(x0 + nx, y0 + ny), (x1 + mx, y1 + my), (x1 - mx, y1 - my), (x0 - nx, y0 - ny)], K)
        if d == 0 or L < 2.2:
            return
        nb = 2 if d > 2 else k.r.choice((2, 3))
        for i in range(nb):
            a = ang + (i - (nb - 1) / 2) * spread * k.r.uniform(0.7, 1.3) + k.r.uniform(-0.12, 0.12)
            limb(x1, y1, a, L * k.r.uniform(0.62, 0.8), w2, d - 1)
    limb(x, y, math.pi / 2 + lean, h * 0.36, max(1.6, h * 0.075), depth)
    k.shape(k.arcpts(x, y, h * 0.16, h * 0.035, 0, 360, 16), lw=0.5, fill=Wt, amp=0.1)


def ladder(k, x, y, h, ang=78):
    a = math.radians(ang); dx, dy = math.cos(a) * h, math.sin(a) * h; w = h * 0.16
    for o in (0, w):
        k.line([(x + o, y), (x + o + dx, y + dy)], lw=0.9, amp=0)
    for i in range(1, 8):
        t = i / 8; k.line([(x + dx * t, y + dy * t), (x + w + dx * t, y + dy * t)], lw=0.6, amp=0)


def skep(k, x, y, w):
    """A straw bee skep on a little stand, wrapped for winter."""
    h = w * 0.85
    k.line([(x - w * 0.55, y + h * 0.18), (x + w * 0.55, y + h * 0.18)], lw=1.2, amp=0)
    for sx in (-0.4, 0.4): k.line([(x + sx * w, y), (x + sx * w, y + h * 0.18)], lw=0.9, amp=0)
    dome = k.arcpts(x, y + h * 0.18, w / 2, h * 0.8, 0, 180, 20)
    k.shape(dome, lw=0.8, fill=Wt, amp=0.1)
    for j in range(1, 5):
        yy = y + h * 0.18 + h * 0.8 * j / 5; ww = w / 2 * math.sqrt(max(0, 1 - (j / 5) ** 2))
        k.line([(x - ww, yy), (x + ww, yy)], lw=0.4, amp=0.05)
    k.blob(k.arcpts(x, y + h * 0.18, w * 0.09, w * 0.08, 0, 180, 8), K)
    k.blob(k.arcpts(x, y + h * 0.18 + h * 0.62, w * 0.36, h * 0.24, 0, 180, 14) + [(x - w * 0.36, y + h * 0.18 + h * 0.62)], Wt)
    k.line(k.arcpts(x, y + h * 0.18 + h * 0.62, w * 0.36, h * 0.24, 0, 180, 14), lw=0.6, amp=0)


def sawhorse(k, x, y, w):
    h = w * 0.55
    k.shape([(x - w / 2, y + h), (x + w / 2, y + h), (x + w / 2, y + h + 3), (x - w / 2, y + h + 3)], lw=0.7, fill=Wt, amp=0)
    for sx in (-0.38, 0.38):
        k.line([(x + sx * w - h * 0.2, y), (x + sx * w + h * 0.05, y + h)], lw=0.9, amp=0)
        k.line([(x + sx * w + h * 0.2, y), (x + sx * w - h * 0.05, y + h)], lw=0.9, amp=0)
    r = w * 0.08; ly = y + h + 3 + r    # a log lying along the horse
    k.shape([(x - w * 0.42, ly - r), (x + w * 0.3, ly - r), (x + w * 0.3, ly + r), (x - w * 0.42, ly + r)], lw=0.6, fill=Wt, amp=0.05)
    k.hatch([(x - w * 0.42, ly - r), (x + w * 0.3, ly - r), (x + w * 0.3, ly - r * 0.2), (x - w * 0.42, ly - r * 0.2)], angle=0, gap=1.2, lw=0.3)
    k.circle(x + w * 0.3, ly, r, lw=0.6, fill=Wt); k.circle(x + w * 0.3, ly, r * 0.45, lw=0.3, fill=None)


def logstack(k, x, y, w, rows=3):
    k.firewood(x, y, w, rows=rows)


def mill(k, x, y, w, h):
    """The village saw-and-grain mill: tall timber house, a wheel at its side and a little loft door."""
    k.wall(x, y, w, h * 0.68, gap=2.4)
    k.roof(x, x + w, y + h * 0.68, y + h, overhang=3, snow=2.6)
    k.window(x + w * 0.18, y + h * 0.36, w * 0.2, h * 0.14); k.window(x + w * 0.62, y + h * 0.36, w * 0.2, h * 0.14)
    k.shape([(x + w * 0.38, y), (x + w * 0.62, y), (x + w * 0.62, y + h * 0.28), (x + w * 0.38, y + h * 0.28)], lw=0.7, fill=K, amp=0)
    k.shape([(x + w * 0.42, y + h * 0.5), (x + w * 0.58, y + h * 0.5), (x + w * 0.58, y + h * 0.62), (x + w * 0.42, y + h * 0.62)], lw=0.6, fill=K, amp=0)
    k.wheel(x + w + h * 0.22, y + h * 0.26, h * 0.26, spokes=10)


def barn(k, x, y, w, h):
    k.wall(x, y, w, h * 0.55, gap=2.0)
    k.roof(x, x + w, y + h * 0.55, y + h, overhang=2.5, snow=2.4)
    k.shape([(x + w * 0.3, y), (x + w * 0.7, y), (x + w * 0.7, y + h * 0.42), (x + w * 0.3, y + h * 0.42)], lw=0.7, fill=Wt, amp=0)
    k.line([(x + w * 0.3, y), (x + w * 0.7, y + h * 0.42)], lw=0.5, amp=0); k.line([(x + w * 0.7, y), (x + w * 0.3, y + h * 0.42)], lw=0.5, amp=0)


def pump(k, x, y, h):
    k.shape([(x - h * 0.08, y), (x + h * 0.08, y), (x + h * 0.08, y + h * 0.75), (x - h * 0.08, y + h * 0.75)], lw=0.7, fill=K, amp=0)
    k.line([(x + h * 0.08, y + h * 0.55), (x + h * 0.3, y + h * 0.5), (x + h * 0.3, y + h * 0.42)], lw=1.0, amp=0)
    k.line([(x - h * 0.08, y + h * 0.7), (x - h * 0.42, y + h * 0.9)], lw=1.0, amp=0)
    k.blob(k.arcpts(x, y + h * 0.75, h * 0.12, h * 0.07, 0, 180, 8), Wt); k.line(k.arcpts(x, y + h * 0.75, h * 0.12, h * 0.07, 0, 180, 8), lw=0.5, amp=0)
    k.shape([(x + h * 0.15, y), (x + h * 0.48, y), (x + h * 0.45, y + h * 0.18), (x + h * 0.18, y + h * 0.18)], lw=0.6, fill=Wt, amp=0)


def bird_table(k, x, y, h):
    k.line([(x, y), (x, y + h * 0.7)], lw=1.1, amp=0)
    k.shape([(x - h * 0.22, y + h * 0.7), (x + h * 0.22, y + h * 0.7), (x + h * 0.22, y + h * 0.74), (x - h * 0.22, y + h * 0.74)], lw=0.6, fill=Wt, amp=0)
    k.roof(x - h * 0.2, x + h * 0.2, y + h * 0.9, y + h, overhang=1.5, snow=1.4)
    for sx in (-0.18, 0.18): k.line([(x + sx * h, y + h * 0.74), (x + sx * h, y + h * 0.9)], lw=0.5, amp=0)
    # a robin on the rail
    bx, by = x + h * 0.08, y + h * 0.745
    k.blob(k.arcpts(bx, by + h * 0.05, h * 0.06, h * 0.045, 0, 360, 12), K)
    k.blob(k.arcpts(bx + h * 0.05, by + h * 0.09, h * 0.03, h * 0.03, 0, 360, 10), K)


# ----------------------------------------------------------------------------- scenes
def frontispiece(k, w, h):
    """Frostwood village after the deep snow: cottages, the lodge on the hill, and rows of numbered
    fence posts poking out of the drifts where the lot fences used to be."""
    m = 9; k.frame(m, m, w - m, h - m)
    k.clip_rect(m + 4, m + 4, w - m - 4, h - m - 4)
    k.snowfall(0, h * 0.4, w, h, n=100); k.stars(20, h * 0.7, w - 20, h - 22, n=40, big=0.15); k.moon(w * 0.2, h * 0.88, 18)
    k.mountains(0, w, h * 0.6, [(w * 0.12, h * 0.72), (w * 0.45, h * 0.8), (w * 0.75, h * 0.73), (w * 0.95, h * 0.77)])
    k.forest(0, w * 0.3, h * 0.58, 16, 30, 9); k.forest(w * 0.72, w, h * 0.58, 16, 30, 9)
    k.ground(0, w, h * 0.59, depth=h * 0.08, drifts=1, ticks=False)
    k.lodge(w * 0.4, h * 0.59, w * 0.24, h * 0.09)
    k.ground(0, w, h * 0.52, depth=h * 0.52, drifts=0, ticks=False)
    # village row
    k.cottage(w * 0.05, h * 0.47, 46, 46); k.cottage(w * 0.24, h * 0.48, 40, 48, door_side=0.2)
    mill(k, w * 0.58, h * 0.46, 48, 62)
    k.cottage(w * 0.84, h * 0.47, 38, 44)
    picket(k, w * 0.04, w * 0.42, h * 0.43, 9)
    k.ground(0, w, h * 0.43, depth=h * 0.43, drifts=0, ticks=False)
    # the snowed-under lots: three receding rows of numbered posts
    buried_posts(k, w * 0.08, h * 0.36, w * 0.92, h * 0.355, 9, 10, tags=[None, 2, None, 3, None, 1, None, None, 2])
    drift(k, -10, w * 0.55, h * 0.33, 10); drift(k, w * 0.45, w + 10, h * 0.335, 9)
    buried_posts(k, w * 0.06, h * 0.25, w * 0.94, h * 0.245, 8, 15, tags=[3, None, None, 2, 0, None, 3, None])
    drift(k, -10, w * 0.6, h * 0.215, 14); drift(k, w * 0.5, w + 10, h * 0.22, 12)
    buried_posts(k, w * 0.12, h * 0.1, w * 0.8, h * 0.105, 5, 26, tags=[2, None, 3, None, 1])
    drift(k, -10, w * 0.4, h * 0.07, 20); drift(k, w * 0.3, w * 0.75, h * 0.06, 24); drift(k, w * 0.66, w + 10, h * 0.07, 20)
    k.firewood(w * 0.47, h * 0.43, 26, rows=2)
    k.pine(w * 0.08, h * 0.275, 26); k.pine(w * 0.93, h * 0.27, 30)
    k.sled(w * 0.6, h * 0.065, 34)
    k.pine(w * 0.94, h * 0.03, 92); k.lamppost(w * 0.04 + 8, h * 0.05, 64)
    k.unclip()


def title(k, w, h):
    """The lodge meadow with a winding post-and-rail fence half buried in snow."""
    k.snowfall(w * 0.04, h * 0.35, w * 0.96, h, n=36); k.stars(w * 0.06, h * 0.7, w * 0.94, h - 4, n=14); k.moon(w * 0.1, h * 0.84, 8)
    k.summit(w * 0.26, w * 0.74, h * 0.5, w * 0.42, w * 0.58, h * 0.74)
    k.lodge(w * 0.425, h * 0.74, w * 0.15, h * 0.12)
    k.forest(w * 0.02, w * 0.3, h * 0.48, 16, 30, 7); k.forest(w * 0.7, w * 0.98, h * 0.48, 16, 30, 7)
    k.ground(w * 0.02, w * 0.98, h * 0.49, depth=h * 0.49, drifts=0, ticks=False)
    rail_fence(k, w * 0.06, h * 0.3, w * 0.36, h * 0.38, 14, n=5)
    rail_fence(k, w * 0.36, h * 0.38, w * 0.64, h * 0.3, 14, n=5)
    rail_fence(k, w * 0.64, h * 0.3, w * 0.94, h * 0.36, 14, n=5)
    drift(k, w * 0.02, w * 0.5, h * 0.22, 12); drift(k, w * 0.44, w * 0.98, h * 0.22, 10)
    buried_posts(k, w * 0.12, h * 0.1, w * 0.88, h * 0.1, 7, 16, tags=[None, 3, None, 2, None, 1, None])
    drift(k, w * 0.02, w * 0.98, h * 0.03, 12)


def op_village(k, w, h):
    """Part One: the village lots, little gardens behind picket fences, the pump and the post office."""
    k.snowfall(0, h * 0.4, w, h, n=40); k.stars(6, h * 0.76, w - 6, h - 4, n=14)
    k.forest(0, w, h * 0.55, 14, 28, 14)
    k.ground(0, w, h * 0.55, depth=h * 0.55, drifts=0, ticks=False)
    k.cottage(w * 0.03, h * 0.5, 44, 44); k.cottage(w * 0.2, h * 0.52, 38, 46, door_side=0.2)
    k.cottage(w * 0.58, h * 0.51, 42, 42); k.cottage(w * 0.76, h * 0.5, 40, 46, door_side=0.2)
    k.lodge(w * 0.39, h * 0.66, w * 0.16, h * 0.1)
    picket(k, w * 0.02, w * 0.36, h * 0.43, 10); picket(k, w * 0.56, w * 0.97, h * 0.43, 10)
    k.ground(0, w, h * 0.42, depth=h * 0.42, drifts=0, ticks=False)
    pump(k, w * 0.46, h * 0.38, 30)
    buried_posts(k, w * 0.06, h * 0.22, w * 0.4, h * 0.22, 5, 13, tags=[2, None, 3, None, 1])
    buried_posts(k, w * 0.58, h * 0.22, w * 0.94, h * 0.22, 5, 13, tags=[None, 0, None, 2, None])
    drift(k, -6, w * 0.5, h * 0.17, 9); drift(k, w * 0.5, w + 6, h * 0.17, 9)
    bird_table(k, w * 0.5, h * 0.12, 34)
    k.footprints([(w * (0.12 + 0.04 * i), h * (0.06 + 0.005 * i)) for i in range(8)])
    k.signpost(w * 0.86, h * 0.04, 22, arrows=[("LODGE", 1)])


def op_meadow(k, w, h):
    """Part Two: the lodge meadow, split-rail fences crossing the slope, a hay barn and a sledge."""
    k.snowfall(0, h * 0.35, w, h, n=40); k.stars(6, h * 0.74, w - 6, h - 4, n=14); k.moon(w * 0.86, h * 0.84, 10)
    k.mountains(0, w, h * 0.58, [(w * 0.18, h * 0.74), (w * 0.52, h * 0.82), (w * 0.84, h * 0.72)])
    k.forest(0, w * 0.35, h * 0.56, 14, 28, 9); k.forest(w * 0.7, w, h * 0.56, 14, 28, 8)
    k.lodge(w * 0.4, h * 0.57, w * 0.26, h * 0.17)
    k.ground(0, w, h * 0.57, depth=h * 0.57, drifts=0, ticks=False)
    barn(k, w * 0.06, h * 0.38, 46, 38)
    rail_fence(k, w * 0.02, h * 0.34, w * 0.34, h * 0.42, 13, n=5)
    rail_fence(k, w * 0.34, h * 0.42, w * 0.66, h * 0.36, 13, n=5)
    rail_fence(k, w * 0.66, h * 0.36, w * 0.98, h * 0.44, 13, n=5)
    drift(k, -6, w * 0.45, h * 0.28, 9); drift(k, w * 0.4, w + 6, h * 0.3, 8)
    gate(k, w * 0.42, h * 0.12, 46, 22)
    rail_fence(k, w * 0.02, h * 0.12, w * 0.42, h * 0.12, 22, n=4)
    rail_fence(k, w * 0.42 + 46, h * 0.12, w * 0.98, h * 0.12, 22, n=4)
    drift(k, -6, w * 0.36, h * 0.06, 9); drift(k, w * 0.68, w + 6, h * 0.06, 9)
    k.sled(w * 0.84, h * 0.005, 30)
    k.footprints([(w * (0.5 + 0.03 * i), h * (0.01 + 0.03 * i)) for i in range(6)])


def op_mill(k, w, h):
    """Part Three: the mill yard, the wheel on the frozen race, log stacks, a cart shed and the yard gate."""
    k.snowfall(0, h * 0.35, w, h, n=40); k.stars(6, h * 0.76, w - 6, h - 4, n=12)
    k.forest(0, w, h * 0.55, 14, 26, 16)
    k.ground(0, w, h * 0.54, depth=h * 0.54, drifts=0, ticks=False)
    mill(k, w * 0.12, h * 0.36, 70, 84)
    barn(k, w * 0.62, h * 0.38, 54, 40)
    logstack(k, w * 0.52, h * 0.36, 30, rows=3); logstack(k, w * 0.9, h * 0.38, 26, rows=2)
    k.ground(0, w, h * 0.36, depth=h * 0.36, drifts=0, ticks=False)
    # frozen mill race under the wheel
    k.line([(w * 0.0, h * 0.33), (w * 0.4, h * 0.34)], lw=0.6, amp=0.2)
    rail_fence(k, w * 0.02, h * 0.16, w * 0.3, h * 0.2, 16, n=4)
    gate(k, w * 0.3, h * 0.2, 44, 18, open_=0.0)
    rail_fence(k, w * 0.3 + 44, h * 0.2, w * 0.98, h * 0.16, 16, n=6)
    drift(k, -6, w * 0.3, h * 0.12, 8); drift(k, w * 0.48, w + 6, h * 0.12, 8)
    sawhorse(k, w * 0.6, h * 0.02, 34)
    buried_posts(k, w * 0.06, h * 0.03, w * 0.4, h * 0.04, 5, 12, tags=[None, 3, None, 2, None])
    drift(k, -6, w * 0.45, h * 0.0, 8)
    k.lamppost(w * 0.95, h * 0.0, 22)


def op_orchard(k, w, h):
    """Part Four: the high orchard, terraces of bare apple trees between snowed-under fences, a ladder and bee skeps."""
    k.snowfall(0, h * 0.4, w, h, n=36); k.stars(6, h * 0.66, w - 6, h - 4, n=36, big=0.25); k.moon(w * 0.82, h * 0.84, 12)
    k.mountains(0, w, h * 0.56, [(w * 0.12, h * 0.74), (w * 0.4, h * 0.84), (w * 0.68, h * 0.72), (w * 0.92, h * 0.8)])
    k.ground(0, w, h * 0.56, depth=h * 0.56, drifts=0, ticks=False)
    for i in range(9): bare_tree(k, w * (0.06 + 0.11 * i), h * 0.5, 22, lean=k.r.uniform(-0.1, 0.1), depth=4)
    rail_fence(k, w * 0.0, h * 0.44, w, h * 0.46, 10, n=12)
    k.ground(0, w, h * 0.43, depth=h * 0.43, drifts=0, ticks=False)
    for i in range(6): bare_tree(k, w * (0.08 + 0.17 * i), h * 0.32, 36, lean=k.r.uniform(-0.12, 0.12), depth=5)
    ladder(k, w * 0.47, h * 0.32, 30, ang=80)
    buried_posts(k, w * 0.03, h * 0.24, w * 0.97, h * 0.25, 10, 12, tags=[None, None, 2, None, None, 3, None, None, 1, None])
    drift(k, -6, w * 0.5, h * 0.2, 9); drift(k, w * 0.46, w + 6, h * 0.21, 9)
    skep(k, w * 0.12, h * 0.05, 18); skep(k, w * 0.2, h * 0.05, 18); skep(k, w * 0.28, h * 0.05, 18)
    bare_tree(k, w * 0.72, h * 0.03, 64, lean=0.05, depth=6)
    k.firewood(w * 0.9, h * 0.03, 24, rows=2)


def v_posts(k, w, h):
    k.stars(4, h * 0.62, w - 4, h - 4, n=6)
    buried_posts(k, w * 0.14, h * 0.18, w * 0.86, h * 0.18, 5, h * 0.42, tags=[2, None, 3, None, 1])
    drift(k, -2, w * 0.55, h * 0.12, h * 0.16); drift(k, w * 0.45, w + 2, h * 0.12, h * 0.14)
    k.ground(0, w, h * 0.12, depth=h * 0.12, drifts=0, ticks=False)


def v_gate(k, w, h):
    k.ground(0, w, h * 0.16, depth=h * 0.16, drifts=0, ticks=False)
    rail_fence(k, w * 0.04, h * 0.16, w * 0.35, h * 0.16, h * 0.42, n=3)
    gate(k, w * 0.35, h * 0.16, w * 0.3, h * 0.42)
    rail_fence(k, w * 0.65, h * 0.16, w * 0.96, h * 0.16, h * 0.42, n=3)
    drift(k, w * 0.02, w * 0.34, h * 0.1, h * 0.12); drift(k, w * 0.66, w * 0.98, h * 0.1, h * 0.12)


def v_picket(k, w, h):
    k.ground(0, w, h * 0.12, depth=h * 0.12, drifts=0, ticks=False)
    picket(k, w * 0.05, w * 0.62, h * 0.12, h * 0.36)
    bird_table(k, w * 0.8, h * 0.12, h * 0.8)
    drift(k, w * 0.02, w * 0.4, h * 0.08, h * 0.1)


def v_logs(k, w, h):
    k.ground(0, w, h * 0.12, depth=h * 0.12, drifts=0, ticks=False)
    sawhorse(k, w * 0.32, h * 0.12, h * 0.75)
    logstack(k, w * 0.66, h * 0.12, h * 0.6, rows=3)
    post(k, w * 0.9, h * 0.12, h * 0.5, tag=2); post(k, w * 0.1, h * 0.12, h * 0.42, tag=3)


def v_orchard(k, w, h):
    k.ground(0, w, h * 0.12, depth=h * 0.12, drifts=0, ticks=False)
    bare_tree(k, w * 0.38, h * 0.12, h * 0.68, depth=5)
    ladder(k, w * 0.43, h * 0.12, h * 0.55, ang=76)
    skep(k, w * 0.75, h * 0.12, h * 0.3); skep(k, w * 0.86, h * 0.12, h * 0.3)
    post(k, w * 0.12, h * 0.12, h * 0.4, tag=1)


def v_stile(k, w, h):
    k.stars(4, h * 0.6, w - 4, h - 4, n=6); k.moon(w * 0.86, h * 0.76, h * 0.1)
    k.ground(0, w, h * 0.16, depth=h * 0.16, drifts=0, ticks=False)
    stile(k, w * 0.5, h * 0.16, h * 0.4)
    k.pine(w * 0.08, h * 0.14, h * 0.6); k.pine(w * 0.92, h * 0.14, h * 0.5)
    drift(k, w * 0.1, w * 0.42, h * 0.1, h * 0.1)


def v_moon(k, w, h):
    k.stars(4, h * 0.4, w - 4, h - 4, n=12); k.moon(w * 0.66, h * 0.74, h * 0.13)
    k.ground(0, w, h * 0.2, depth=h * 0.2, drifts=0, ticks=False)
    buried_posts(k, w * 0.3, h * 0.2, w * 0.62, h * 0.2, 4, h * 0.28)
    k.pine(w * 0.15, h * 0.18, h * 0.6); k.pine(w * 0.24, h * 0.18, h * 0.45); k.lamppost(w * 0.9, h * 0.18, h * 0.55)


def thanks(k, w, h):
    k.ground(0, w, h * 0.22, depth=h * 0.22, drifts=0, ticks=False)
    rail_fence(k, w * 0.02, h * 0.22, w * 0.31, h * 0.22, h * 0.32, n=3)
    gate(k, w * 0.31, h * 0.22, w * 0.18, h * 0.32)
    rail_fence(k, w * 0.49, h * 0.22, w * 0.62, h * 0.22, h * 0.32, n=2)
    k.bench(w * 0.75, h * 0.22, 30); k.mug(w * 0.75, h * 0.22 + 12.5, 7)
    k.lamppost(w * 0.92, h * 0.22, h * 0.7)
    k.stars(w * 0.1, h * 0.7, w * 0.9, h - 3, n=8)


VIGNETTES = ["v_posts", "v_gate", "v_picket", "v_logs", "v_orchard", "v_stile"]
SPECS = {  # name: (width in, height in, function, seed)
    "frontispiece": (4.7, 7.0, frontispiece, 61),
    "title": (4.7, 2.5, title, 3),
    "opener-easy": (4.7, 2.4, op_village, 11), "opener-medium": (4.7, 2.4, op_meadow, 12),
    "opener-hard": (4.7, 2.4, op_mill, 13), "opener-expert": (4.7, 2.4, op_orchard, 14),
    "thanks": (3.4, 1.5, thanks, 21),
    "v_moon": (1.9, 0.85, v_moon, 79),
    **{n: (1.9, 0.85, globals()[n], 80 + i) for i, n in enumerate(VIGNETTES)},
}

if __name__ == "__main__":
    only = set(sys.argv[1:])
    for name, (wi, hi, fn, seed) in SPECS.items():
        if only and name not in only: continue
        render(os.path.join(OUT, name + ".png"), wi, hi, fn, seed=seed); print("drew", name)
