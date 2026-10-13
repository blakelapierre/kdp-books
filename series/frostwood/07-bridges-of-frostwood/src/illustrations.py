"""Draws the black-and-white ink illustrations for Bridges of Frostwood -> ../illustrations/*.png
(300 DPI grayscale, pure black line art on white, same inkart house style as the other Frostwood books).
Subjects: frozen ponds, footbridges, village streams, the reed marsh and the lake of islands. No people.
Deterministic: same seeds -> same images. Run from src/: python3 illustrations.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inkart import render, Wt, K, lerp
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "illustrations")


# ----------------------------------------------------------------------------- local helpers
def ice(k, x0, x1, y0, y1, glints=4, tracks=True):
    """A frozen stretch of water: white sheet, a few short horizontal glints and a curling skate track."""
    w = x1 - x0; h = y1 - y0
    for i in range(glints):
        yy = y0 + h * (0.2 + 0.6 * k.r.random()); xx = x0 + w * (0.1 + 0.7 * k.r.random()); L = w * k.r.uniform(0.06, 0.16)
        k.line([(xx, yy), (xx + L, yy)], lw=0.4, amp=0)
        k.line([(xx + L * 0.2, yy - 1.6), (xx + L * 0.7, yy - 1.6)], lw=0.3, amp=0)
    if tracks:   # two long, lazy skate tracks
        for j in range(2):
            ph = k.r.uniform(0, 6); yy = y0 + h * (0.3 + 0.35 * j); xa = x0 + w * k.r.uniform(0.05, 0.25); xb = x0 + w * k.r.uniform(0.6, 0.9)
            k.line([(lerp(xa, xb, t), yy + h * 0.12 * math.sin(ph + t * 4.5)) for t in [i / 30 for i in range(31)]], lw=0.3, amp=0)


def bank(k, pts, side=1, gap=1.7):
    """A snowy bank edge: the line plus short hatching dropping toward the water."""
    k.line(pts, lw=0.8, amp=0.25)
    for (x, y) in pts[::3]:
        k.line([(x, y), (x + 1.2, y - side * 3.2)], lw=0.35, amp=0)


def footbridge(k, x, y, w, arch=0.18, rails=True, posts=6, snow=True):
    """An arched timber footbridge, ends at (x - w/2, y) and (x + w/2, y)."""
    h = w * arch
    deck = [(x - w / 2 + w * t, y + h * math.sin(math.pi * t)) for t in [i / 30 for i in range(31)]]
    under = [(px, py - w * 0.035) for px, py in deck]
    k.shape(deck + under[::-1], lw=0.8, fill=Wt, amp=0.1)
    k.hatch(deck + under[::-1], angle=90, gap=max(1.4, w * 0.018), lw=0.35, jitter=0.1)
    if snow:
        k.line([(px, py + 0.7) for px, py in deck[2:-2]], lw=1.3, amp=0.15)
    if rails:
        rh = w * 0.09
        tops = []
        for i in range(posts + 1):
            t = i / posts; px = x - w / 2 + w * t; py = y + h * math.sin(math.pi * t)
            k.line([(px, py), (px, py + rh)], lw=0.9, amp=0); tops.append((px, py + rh))
        k.line(tops, lw=0.9, amp=0.15)
        k.line([(px, py - rh * 0.48) for px, py in tops], lw=0.5, amp=0.15)
        for px, py in tops: k.blob([(px - 1.4, py), (px + 1.4, py), (px, py + 1.6)], Wt); k.line([(px - 1.4, py + 0.2), (px, py + 1.4), (px + 1.4, py + 0.2)], lw=0.4, amp=0)
    # stone footings
    for sx in (-1, 1):
        fx = x + sx * w / 2
        k.shape([(fx - 3, y - 4), (fx + 3, y - 4), (fx + 2.4, y + 0.5), (fx - 2.4, y + 0.5)], lw=0.6, fill=Wt, amp=0.2)


def plank_bridge(k, x0, x1, y, rail=True):
    """A flat plank footbridge or boardwalk with low posts."""
    k.shape([(x0, y), (x1, y), (x1, y + 3), (x0, y + 3)], lw=0.7, fill=Wt, amp=0.1)
    n = max(2, int((x1 - x0) / 3))
    for i in range(1, n): xx = lerp(x0, x1, i / n); k.line([(xx, y), (xx, y + 3)], lw=0.3, amp=0)
    m = max(2, int((x1 - x0) / 14))
    for i in range(m + 1):
        xx = lerp(x0, x1, i / m); k.line([(xx, y - 5), (xx, y)], lw=0.8, amp=0)
        if rail: k.line([(xx, y + 3), (xx, y + 9)], lw=0.7, amp=0)
    if rail: k.line([(x0, y + 9), (x1, y + 9)], lw=0.7, amp=0.2)


def reeds(k, x, y, h, n=7):
    for i in range(n):
        dx = (i - n / 2) * h * 0.06 + k.r.uniform(-1, 1); hh = h * k.r.uniform(0.6, 1.0); lean = k.r.uniform(-0.12, 0.12) * hh
        k.line([(x + dx, y), (x + dx + lean * 0.5, y + hh * 0.6), (x + dx + lean, y + hh)], lw=0.5, amp=0.1)
        if i % 2 == 0:
            cx, cy = x + dx + lean * 0.8, y + hh * 0.86
            k.shape(k.arcpts(cx, cy, h * 0.022, h * 0.075, 0, 360, 12), lw=0.5, fill=K, amp=0)


def stepping_stones(k, x0, y0, x1, y1, n=5, r=4):
    for i in range(n):
        t = (i + 0.5) / n; x = lerp(x0, x1, t); y = lerp(y0, y1, t) + 2 * math.sin(t * 6)
        k.shape(k.arcpts(x, y, r * k.r.uniform(0.9, 1.2), r * 0.5, 0, 360, 14), lw=0.7, fill=Wt, amp=0.2)
        k.line(k.arcpts(x, y + 0.6, r * 0.8, r * 0.28, 20, 160, 8), lw=0.9, amp=0)


def islet(k, x, y, w, trees=2, h=None):
    """A small snowy island on the ice, with a pine or two."""
    h = h or w * 0.9
    top = [(x - w / 2 + w * t, y + w * 0.09 * math.sin(math.pi * t) + k.r.uniform(-0.6, 0.6) * (0 < t < 1)) for t in [i / 14 for i in range(15)]]
    k.shape(top + [(x + w / 2 + 2, y - 2.5), (x - w / 2 - 2, y - 2.5)], lw=0.8, fill=Wt, amp=0.15)
    k.line([(x - w / 2 - 1, y - 2.6), (x + w / 2 + 1, y - 2.6)], lw=0.4, amp=0.2)
    for i in range(trees):
        tx = x + (i - (trees - 1) / 2) * w * 0.32; k.pine(tx, y + w * 0.04, h * (0.9 + 0.2 * ((i * 7) % 3) / 2))


def boathouse(k, x, y, w, h):
    k.wall(x, y, w, h * 0.55, gap=2.4)
    k.roof(x, x + w, y + h * 0.55, y + h, overhang=3, snow=2.6)
    k.shape([(x + w * 0.25, y), (x + w * 0.75, y), (x + w * 0.75, y + h * 0.34), (x + w * 0.25, y + h * 0.34)], lw=0.7, fill=K, amp=0)
    k.window(x + w * 0.42, y + h * 0.4, w * 0.16, h * 0.1)
    plank_bridge(k, x - w * 0.4, x, y, rail=False)


def duck_house(k, x, y, w):
    h = w * 0.8
    k.line([(x, y - 6), (x, y)], lw=1.2, amp=0)
    k.wall(x - w / 2, y, w, h * 0.5, gap=1.8)
    k.roof(x - w / 2, x + w / 2, y + h * 0.5, y + h, overhang=2, snow=1.8)
    k.shape(k.arcpts(x, y + h * 0.22, w * 0.14, w * 0.14, 0, 360, 16), lw=0.6, fill=K, amp=0)


def lantern_post(k, x, y, h):
    k.c.setStrokeColor(K); k.c.setLineWidth(1.0); k.c.line(x, y, x, y + h * 0.78)
    k.c.line(x, y + h * 0.74, x + h * 0.16, y + h * 0.74)
    k.lantern(x + h * 0.16, y + h * 0.5, h * 0.22)


def stream(k, x0, x1, y, width, wav=4, phase=0.0):
    """A frozen stream running left-right: two wavy banks, ice between."""
    top = [(lerp(x0, x1, t), y + width / 2 + wav * math.sin(t * 5 + phase)) for t in [i / 40 for i in range(41)]]
    bot = [(lerp(x0, x1, t), y - width / 2 + wav * math.sin(t * 5 + phase + 0.6)) for t in [i / 40 for i in range(41)]]
    k.shape(top + bot[::-1], lw=0, fill=Wt, stroke=False, amp=0)
    bank(k, top, side=1); bank(k, bot, side=-1)
    ice(k, x0, x1, y - width * 0.3, y + width * 0.3, glints=5, tracks=False)
    return top, bot


# ----------------------------------------------------------------------------- scenes
def frontispiece(k, w, h):
    """The lodge above the frozen pond at dusk, the arched footbridge to the little island, lanterns lit."""
    m = 9; k.frame(m, m, w - m, h - m)
    k.clip_rect(m + 4, m + 4, w - m - 4, h - m - 4)
    k.snowfall(0, h * 0.35, w, h, n=90); k.stars(20, h * 0.66, w - 20, h - 22, n=46, big=0.15); k.moon(w * 0.8, h * 0.87, 20)
    k.mountains(0, w, h * 0.55, [(w * 0.14, h * 0.71), (w * 0.4, h * 0.78), (w * 0.7, h * 0.7), (w * 0.92, h * 0.75)])
    k.forest(0, w * 0.32, h * 0.53, 18, 34, 10); k.forest(w * 0.7, w, h * 0.53, 18, 34, 9)
    k.ground(0, w, h * 0.54, depth=h * 0.06, drifts=2)
    k.lodge(w * 0.38, h * 0.54, w * 0.26, h * 0.1)
    # far bank, the pond, near bank
    k.ground(0, w, h * 0.48, depth=h * 0.06, drifts=2, ticks=False)
    pond = [(lerp(0, w, t), h * 0.45 + 3 * math.sin(t * 7)) for t in [i / 40 for i in range(41)]]
    bank(k, pond, side=1)
    ice(k, w * 0.04, w * 0.96, h * 0.25, h * 0.42, glints=9)
    islet(k, w * 0.7, h * 0.33, w * 0.2, trees=3, h=h * 0.08)
    islet(k, w * 0.2, h * 0.33, w * 0.14, trees=0)
    footbridge(k, w * 0.435, h * 0.335, w * 0.33, arch=0.15, posts=8)
    duck_house(k, w * 0.86, h * 0.29, 22)
    near = [(lerp(0, w, t), h * 0.22 + 5 * math.sin(t * 4 + 1)) for t in [i / 40 for i in range(41)]]
    k.shape([(0, 0)] + near + [(w, 0)], lw=0, fill=Wt, stroke=False, amp=0); bank(k, near, side=-1)
    reeds(k, w * 0.08, h * 0.2, 46, 9); reeds(k, w * 0.92, h * 0.19, 40, 7)
    k.bench(w * 0.32, h * 0.12, 54)
    k.skate(w * 0.28, h * 0.12 + 54 * 0.4 + 1, 14); k.skate(w * 0.36, h * 0.12 + 54 * 0.4 + 1, 14, facing=-1)
    lantern_post(k, w * 0.56, h * 0.1, 70); k.mug(w * 0.64, h * 0.08, 10)
    k.footprints([(w * (0.42 + 0.03 * i), h * (0.06 + 0.012 * i)) for i in range(8)])
    k.pine(w * 0.18, h * 0.03, 110); k.pine(w * 0.86, h * 0.04, 96)
    k.unclip()


def title(k, w, h):
    """A frozen stream winding down from the lodge, crossed by three little footbridges."""
    k.snowfall(w * 0.04, h * 0.35, w * 0.96, h, n=40); k.stars(w * 0.06, h * 0.66, w * 0.94, h - 4, n=16); k.moon(w * 0.88, h * 0.84, 9)
    k.summit(w * 0.26, w * 0.74, h * 0.48, w * 0.42, w * 0.58, h * 0.72)
    k.lodge(w * 0.425, h * 0.72, w * 0.15, h * 0.12)
    k.forest(w * 0.02, w * 0.3, h * 0.46, 16, 32, 7); k.forest(w * 0.7, w * 0.98, h * 0.46, 16, 32, 7)
    k.ground(w * 0.02, w * 0.98, h * 0.47, depth=h * 0.47, drifts=0, ticks=False)
    stream(k, w * 0.02, w * 0.98, h * 0.2, h * 0.16, wav=5)
    footbridge(k, w * 0.22, h * 0.2 - h * 0.05, w * 0.16, arch=0.2, posts=5)
    plank_bridge(k, w * 0.46, w * 0.58, h * 0.215)
    footbridge(k, w * 0.8, h * 0.2 - h * 0.05, w * 0.14, arch=0.22, posts=4)
    reeds(k, w * 0.06, h * 0.06, 26, 6); reeds(k, w * 0.66, h * 0.07, 22, 5)
    lantern_post(k, w * 0.36, h * 0.3, 32)


def op_pond(k, w, h):
    """Part One: the lodge pond, boathouse, stepping stones and the first little bridge."""
    k.snowfall(0, h * 0.4, w, h, n=40); k.stars(6, h * 0.75, w - 6, h - 4, n=14)
    k.forest(0, w, h * 0.55, 16, 34, 16)
    k.ground(0, w, h * 0.56, depth=h * 0.06, drifts=1, ticks=False)
    k.lodge(w * 0.62, h * 0.56, w * 0.24, h * 0.18)
    pond = [(lerp(0, w, t), h * 0.5 + 2.5 * math.sin(t * 6)) for t in [i / 40 for i in range(41)]]
    bank(k, pond)
    ice(k, w * 0.05, w * 0.95, h * 0.18, h * 0.45, glints=7)
    boathouse(k, w * 0.12, h * 0.44, 40, 34)
    islet(k, w * 0.27, h * 0.3, w * 0.1, trees=0)
    footbridge(k, w * 0.43, h * 0.305, w * 0.22, arch=0.18, posts=6)
    islet(k, w * 0.62, h * 0.3, w * 0.12, trees=2, h=h * 0.2)
    stepping_stones(k, w * 0.69, h * 0.27, w * 0.9, h * 0.17, n=4, r=6)
    near = [(lerp(0, w, t), h * 0.14 + 3 * math.sin(t * 5)) for t in [i / 40 for i in range(41)]]
    k.shape([(0, 0)] + near + [(w, 0)], lw=0, fill=Wt, stroke=False, amp=0); bank(k, near, side=-1)
    reeds(k, w * 0.05, h * 0.12, 30, 7); k.bench(w * 0.3, h * 0.03, 34); lantern_post(k, w * 0.94, h * 0.03, 44)


def op_village(k, w, h):
    """Part Two: the village mill stream, a stone bridge, cottages on both banks."""
    k.snowfall(0, h * 0.35, w, h, n=40); k.stars(6, h * 0.72, w - 6, h - 4, n=14)
    k.forest(0, w, h * 0.5, 14, 26, 14)
    k.ground(0, w, h * 0.48, depth=h * 0.48, drifts=0, ticks=False)
    k.cottage(w * 0.04, h * 0.48, 44, 42); k.cottage(w * 0.18, h * 0.5, 36, 44, door_side=0.2)
    k.cottage(w * 0.72, h * 0.49, 42, 40); k.cottage(w * 0.86, h * 0.48, 36, 44, door_side=0.2)
    # mill wheel by the stream
    k.wheel(w * 0.66, h * 0.38, 14, spokes=10)
    stream(k, 0, w, h * 0.24, h * 0.18, wav=4)
    # stone arch bridge
    bx = w * 0.42; bw = w * 0.22; by = h * 0.3
    arch = k.arcpts(bx, h * 0.17, bw * 0.3, h * 0.14, 0, 180, 20)
    body = [(bx - bw / 2, h * 0.14), (bx - bw / 2, by), (bx + bw / 2, by), (bx + bw / 2, h * 0.14), (bx + bw * 0.3, h * 0.14)] + arch + [(bx - bw * 0.3, h * 0.14)]
    k.shape(body, lw=0.9, fill=Wt, amp=0.15)
    for j in range(3):
        yy = lerp(h * 0.16, by - 2, j / 3)
        for i in range(6):
            xx = bx - bw / 2 + bw * (i + 0.5 * (j % 2)) / 6
            if abs(xx - bx) > bw * 0.32 or yy > h * 0.31: k.line([(xx, yy), (xx, yy + (by - h * 0.16) / 3)], lw=0.3, amp=0)
        k.line([(bx - bw / 2, yy), (bx + bw / 2, yy)], lw=0.3, amp=0)
    k.line([(bx - bw / 2 - 2, by + 1), (bx + bw / 2 + 2, by + 1)], lw=1.6, amp=0.2)
    k.lamppost(bx - bw / 2 + 4, by, 30); k.lamppost(bx + bw / 2 - 4, by, 30)
    plank_bridge(k, w * 0.8, w * 0.93, h * 0.25)
    k.ground(0, w, h * 0.1, depth=h * 0.1, drifts=1, ticks=False)
    k.signpost(w * 0.14, h * 0.02, 24, arrows=[("MILL", 1)])
    k.pine(w * 0.94, h * 0.02, 44)


def op_marsh(k, w, h):
    """Part Three: the reed marsh, a long zig-zag boardwalk between frozen pools."""
    k.snowfall(0, h * 0.3, w, h, n=46); k.stars(6, h * 0.76, w - 6, h - 4, n=10); k.moon(w * 0.12, h * 0.84, 10)
    k.mountains(0, w, h * 0.52, [(w * 0.2, h * 0.7), (w * 0.55, h * 0.78), (w * 0.85, h * 0.68)])
    k.forest(0, w, h * 0.5, 12, 22, 18)
    k.ground(0, w, h * 0.5, depth=h * 0.5, drifts=0, ticks=False)
    for (cx, cy, rx, ry) in [(0.18, 0.36, 0.14, 0.06), (0.5, 0.42, 0.12, 0.04), (0.78, 0.33, 0.16, 0.07), (0.38, 0.17, 0.18, 0.07), (0.82, 0.12, 0.12, 0.05)]:
        pts = k.arcpts(w * cx, h * cy, w * rx, h * ry, 0, 360, 36)
        k.shape(pts, lw=0.7, fill=Wt, amp=0.3)
        k.line([(w * (cx - rx * 0.4), h * cy), (w * (cx - rx * 0.05), h * cy)], lw=0.35, amp=0)
    for (rx, ry, rh) in [(0.06, 0.3, 30), (0.3, 0.38, 22), (0.62, 0.4, 24), (0.95, 0.3, 28), (0.2, 0.08, 34), (0.6, 0.1, 30), (0.66, 0.24, 22), (0.04, 0.12, 28)]:
        reeds(k, w * rx, h * ry, rh, 7)
    plank_bridge(k, w * 0.08, w * 0.3, h * 0.24); plank_bridge(k, w * 0.3, w * 0.52, h * 0.27)
    plank_bridge(k, w * 0.52, w * 0.78, h * 0.22); plank_bridge(k, w * 0.78, w * 0.98, h * 0.25)
    duck_house(k, w * 0.5, h * 0.42, 16)
    lantern_post(k, w * 0.3, h * 0.27, 28); lantern_post(k, w * 0.78, h * 0.22, 28)


def op_lake(k, w, h):
    """Part Four: the great frozen lake of islands, long bridges hopping from island to island."""
    k.snowfall(0, h * 0.4, w, h, n=36); k.stars(6, h * 0.68, w - 6, h - 4, n=40, big=0.25); k.moon(w * 0.86, h * 0.84, 12)
    k.mountains(0, w, h * 0.5, [(w * 0.1, h * 0.72), (w * 0.38, h * 0.82), (w * 0.66, h * 0.7), (w * 0.9, h * 0.78)])
    k.forest(0, w, h * 0.49, 10, 18, 22)
    shore = [(lerp(0, w, t), h * 0.48 + 1.5 * math.sin(t * 9)) for t in [i / 50 for i in range(51)]]
    k.shape([(0, 0)] + shore + [(w, 0)], lw=0, fill=Wt, stroke=False, amp=0); bank(k, shore)
    ice(k, w * 0.03, w * 0.97, h * 0.06, h * 0.42, glints=10)
    rows = [(h * 0.33, [(0.08, 24, 1), (0.3, 30, 2), (0.54, 26, 1), (0.78, 34, 2), (0.95, 18, 1)]),
            (h * 0.12, [(0.14, 34, 2), (0.42, 26, 1), (0.66, 30, 2), (0.9, 26, 1)])]
    for y, row in rows:
        for (xa, sa, _), (xb, sb, _) in zip(row, row[1:]):
            plank_bridge(k, w * xa + sa * 0.48, w * xb - sb * 0.48, y)
        for (x, s_, n) in row: islet(k, w * x, y, s_, trees=n, h=s_ * 0.85)
    lantern_post(k, w * 0.42 - 6, h * 0.12, 22); lantern_post(k, w * 0.54 + 6, h * 0.33, 20)


def v_bridge(k, w, h):
    k.ground(0, w, h * 0.22, depth=h * 0.22, drifts=0, ticks=False)
    stream(k, w * 0.05, w * 0.95, h * 0.16, h * 0.18, wav=2)
    footbridge(k, w * 0.5, h * 0.2, w * 0.44, arch=0.2, posts=6)
    k.pine(w * 0.12, h * 0.24, h * 0.62); k.pine(w * 0.88, h * 0.24, h * 0.7)


def v_skates(k, w, h):
    k.ground(0, w, h * 0.12, depth=h * 0.12, drifts=0, ticks=False)
    k.bench(w * 0.5, h * 0.12, h * 1.1)
    k.skate(w * 0.42, h * 0.12 + h * 0.44 + 0.5, h * 0.34); k.skate(w * 0.6, h * 0.12 + h * 0.44 + 0.5, h * 0.34, facing=-1)
    k.mug(w * 0.18, h * 0.12, h * 0.28); reeds(k, w * 0.86, h * 0.12, h * 0.6, 6)


def v_ducks(k, w, h):
    ice(k, w * 0.05, w * 0.95, h * 0.05, h * 0.3, glints=3, tracks=False)
    k.line([(w * 0.04, h * 0.32), (w * 0.96, h * 0.32)], lw=0.6, amp=0.3)
    duck_house(k, w * 0.5, h * 0.4, h * 0.42); reeds(k, w * 0.2, h * 0.32, h * 0.6, 7); reeds(k, w * 0.8, h * 0.32, h * 0.55, 6)


def v_stones(k, w, h):
    stream(k, w * 0.02, w * 0.98, h * 0.3, h * 0.36, wav=2)
    stepping_stones(k, w * 0.25, h * 0.3, w * 0.75, h * 0.3, n=5, r=h * 0.07)
    k.ground(0, w, h * 0.06, depth=h * 0.06, drifts=0, ticks=False)
    lantern_post(k, w * 0.12, h * 0.48, h * 0.5); k.pine(w * 0.88, h * 0.48, h * 0.5)


def v_islet(k, w, h):
    k.stars(4, h * 0.55, w - 4, h - 4, n=8)
    ice(k, w * 0.06, w * 0.94, h * 0.05, h * 0.25, glints=3, tracks=False)
    islet(k, w * 0.3, h * 0.24, h * 0.5, trees=2, h=h * 0.45); islet(k, w * 0.72, h * 0.24, h * 0.42, trees=1, h=h * 0.5)
    plank_bridge(k, w * 0.3 + h * 0.24, w * 0.72 - h * 0.2, h * 0.26)


def v_moon(k, w, h):
    k.stars(4, h * 0.4, w - 4, h - 4, n=12); k.moon(w * 0.75, h * 0.72, h * 0.14)
    k.ground(0, w, h * 0.2, depth=h * 0.2, drifts=0, ticks=False)
    plank_bridge(k, w * 0.36, w * 0.6, h * 0.2)
    k.pine(w * 0.2, h * 0.18, h * 0.6); k.pine(w * 0.3, h * 0.18, h * 0.45); lantern_post(k, w * 0.66, h * 0.18, h * 0.55)


def thanks(k, w, h):
    stream(k, 0, w, h * 0.14, h * 0.16, wav=2)
    footbridge(k, w * 0.36, h * 0.18, w * 0.3, arch=0.16, posts=6)
    k.bench(w * 0.72, h * 0.25, 30); k.mug(w * 0.72, h * 0.25 + 12.5, 7)
    lantern_post(k, w * 0.9, h * 0.25, h * 0.7); k.pine(w * 0.08, h * 0.24, h * 0.7)
    k.stars(w * 0.1, h * 0.7, w * 0.9, h - 3, n=8)


def halftitle(k, w, h):
    v_bridge(k, w, h)


VIGNETTES = ["v_bridge", "v_skates", "v_ducks", "v_stones", "v_islet", "v_moon"]
SPECS = {  # name: (width in, height in, function, seed)
    "frontispiece": (4.7, 7.0, frontispiece, 61),
    "title": (4.7, 2.5, title, 3),
    "opener-easy": (4.7, 2.4, op_pond, 11), "opener-medium": (4.7, 2.4, op_village, 12),
    "opener-hard": (4.7, 2.4, op_marsh, 13), "opener-expert": (4.7, 2.4, op_lake, 14),
    "thanks": (3.4, 1.5, thanks, 21),
    **{n: (1.9, 0.85, globals()[n], 80 + i) for i, n in enumerate(VIGNETTES)},
}

if __name__ == "__main__":
    only = set(sys.argv[1:])
    for name, (wi, hi, fn, seed) in SPECS.items():
        if only and name not in only: continue
        render(os.path.join(OUT, name + ".png"), wi, hi, fn, seed=seed); print("drew", name)
