"""Draws the black-and-white ink illustrations for Snow Paths of Frostwood -> ../illustrations/*.png
(300 DPI grayscale, pure black line art on white, same inkart house style as the other Frostwood books).
Subjects: snow shovels, freshly dug paths, the lodge garden, the village lanes, the station yard and the
high meadows. No people. Deterministic: same seeds -> same images. Run from src/: python3 illustrations.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inkart import render, Wt, K, lerp
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "illustrations")


# ----------------------------------------------------------------------------- local helpers
def shovel(k, x, y, h, ang=12, snow=True):
    """A snow shovel standing with its blade at (x, y), handle leaning `ang` degrees to the right."""
    a = math.radians(ang); bw = h * 0.34; bh = h * 0.2
    # blade (a slightly flared scoop)
    blade = [(x - bw / 2, y), (x + bw / 2, y), (x + bw * 0.4, y + bh * 0.8), (x + bw * 0.12, y + bh), (x - bw * 0.12, y + bh), (x - bw * 0.4, y + bh * 0.8)]
    k.shape(blade, lw=0.9, fill=Wt, amp=0.1)
    k.hatch(blade, angle=90, gap=max(1.2, bw * 0.09), lw=0.35, jitter=0.05)
    if snow: k.line([(x - bw * 0.48, y + 1.0), (x + bw * 0.48, y + 1.0)], lw=1.6, amp=0.2)
    # shaft and D-grip
    x0, y0 = x, y + bh; x1, y1 = x + math.sin(a) * h * 0.74, y + bh + math.cos(a) * h * 0.74
    for o in (-0.8, 0.8): k.line([(x0 + o, y0), (x1 + o, y1)], lw=0.7, amp=0)
    gx, gy = x1 + math.sin(a) * h * 0.05, y1 + math.cos(a) * h * 0.05
    k.shape(k.arcpts(gx, gy + h * 0.035, h * 0.06, h * 0.05, 0, 360, 18), lw=1.0, fill=Wt, amp=0)
    k.shape(k.arcpts(gx, gy + h * 0.035, h * 0.03, h * 0.022, 0, 360, 14), lw=0.6, fill=Wt, amp=0)


def snowpile(k, x, y, w, h=None):
    """A heap of shovelled snow: a lumpy mound with a few shadow strokes on its right side."""
    h = h or w * 0.42
    top = [(x - w / 2 + w * t, y + h * math.sin(math.pi * t) ** 0.8 * (1 + 0.12 * math.sin(t * 17))) for t in [i / 24 for i in range(25)]]
    k.shape(top + [(x + w / 2, y - 1), (x - w / 2, y - 1)], lw=0.8, fill=Wt, amp=0.2)
    for i in range(5):
        t = 0.6 + 0.07 * i; px = x - w / 2 + w * t; py = y + h * math.sin(math.pi * t) ** 0.8 * 0.85
        k.line([(px, py), (px + 1.5, py - h * 0.45)], lw=0.35, amp=0)


def drifts(k, x0, x1, y0, y1, n=6):
    """Soft drift lines across open snow, each with a few short shadow ticks underneath."""
    for i in range(n):
        L = (x1 - x0) * k.r.uniform(0.12, 0.26); xa = k.r.uniform(x0, x1 - L); yy = lerp(y0, y1, (i + 0.5) / n) + k.r.uniform(-3, 3)
        arc = [(xa + L * t, yy + 2.2 * math.sin(math.pi * t)) for t in [j / 12 for j in range(13)]]
        k.line(arc, lw=0.5, amp=0.15)
        for j in range(3):
            tx = xa + L * (0.3 + 0.2 * j); k.line([(tx, yy - 0.8), (tx - 1.2, yy - 3.2)], lw=0.3, amp=0)


def dug_path(k, pts, w0, w1, wall=4.0, steps=True):
    """A path dug through deep snow, given as a centre line from near (wide, w0) to far (narrow, w1).
    Both edges get a cut snow wall, hatched on the face toward the path; the path itself stays white."""
    n = len(pts); L = []; R = []
    for i, (x, y) in enumerate(pts):
        t = i / (n - 1); ww = lerp(w0, w1, t)
        L.append((x - ww / 2, y)); R.append((x + ww / 2, y))
    k.shape(L + R[::-1], lw=0, fill=Wt, stroke=False, amp=0)
    for edge, side in ((L, -1), (R, 1)):
        k.line(edge, lw=0.8, amp=0.2)
        top = [(ex + side * 0.6, ey + wall * lerp(1.0, 0.45, i / (n - 1))) for i, (ex, ey) in enumerate(edge)]
        k.line(top, lw=0.6, amp=0.25)
        for i in range(0, n, 2):
            (ex, ey), (tx, ty) = edge[i], top[i]
            k.line([(ex, ey), (tx, ty)], lw=0.35, amp=0)
    if steps:   # boot prints down the middle of the dug path
        fp = []
        for i in range(1, n - 1, 3):
            x, y = pts[i]; t = i / (n - 1); o = lerp(w0, w1, t) * 0.12 * (1 if (i // 3) % 2 else -1)
            fp.append((x + o, y, lerp(1.0, 0.45, t)))
        for x, y, sc in fp:
            k.shape(k.arcpts(x, y, 1.1 * sc * (w0 / 30 + 0.6), 2.0 * sc * (w0 / 30 + 0.6), 0, 360, 10), lw=0.35, fill=Wt, amp=0)
    return L, R


def lantern_post(k, x, y, h):
    k.c.setStrokeColor(K); k.c.setLineWidth(1.0); k.c.line(x, y, x, y + h * 0.78)
    k.c.line(x, y + h * 0.74, x + h * 0.16, y + h * 0.74)
    k.lantern(x + h * 0.16, y + h * 0.5, h * 0.22)


def fence(k, x0, x1, y, h):
    k.snowman_free_fence(x0, x1, y, h)   # split-rail fence half buried in snow


# ----------------------------------------------------------------------------- scenes
def frontispiece(k, w, h):
    """The lodge at dawn after a snowfall, the first paths dug from its door down through the garden."""
    m = 9; k.frame(m, m, w - m, h - m)
    k.clip_rect(m + 4, m + 4, w - m - 4, h - m - 4)
    k.snowfall(0, h * 0.4, w, h, n=80); k.stars(20, h * 0.7, w - 20, h - 22, n=36, big=0.15); k.moon(w * 0.18, h * 0.87, 18)
    k.mountains(0, w, h * 0.6, [(w * 0.12, h * 0.74), (w * 0.42, h * 0.82), (w * 0.72, h * 0.73), (w * 0.94, h * 0.78)])
    k.forest(0, w * 0.3, h * 0.58, 18, 34, 10); k.forest(w * 0.72, w, h * 0.58, 18, 34, 9)
    k.ground(0, w, h * 0.585, depth=h * 0.6, drifts=3, ticks=False)
    k.lodge(w * 0.3, h * 0.585, w * 0.4, h * 0.13)
    # main path from the door down to the foreground, and a branch to the woodshed
    main = [(lerp(w * 0.52, w * 0.5, t) + w * 0.08 * math.sin(t * 3.4), lerp(h * 0.05, h * 0.575, t)) for t in [i / 40 for i in range(41)]]
    dug_path(k, main, w * 0.2, w * 0.05, wall=10)
    drifts(k, w * 0.04, w * 0.96, h * 0.06, h * 0.5, n=9)
    branch = [(lerp(w * 0.56, w * 0.86, t), lerp(h * 0.36, h * 0.44, t) + 6 * math.sin(t * 3)) for t in [i / 24 for i in range(25)]]
    dug_path(k, branch, w * 0.05, w * 0.035, wall=4)
    k.cabin(w * 0.8, h * 0.44, w * 0.13, h * 0.06)
    k.firewood(w * 0.93, h * 0.44, w * 0.05, rows=3)
    fence(k, w * 0.04, w * 0.3, h * 0.3, 14); fence(k, w * 0.66, w * 0.96, h * 0.22, 14)
    shovel(k, w * 0.27, h * 0.16, 90, ang=-10); snowpile(k, w * 0.2, h * 0.12, 60)
    k.sled(w * 0.76, h * 0.1, 46)
    lantern_post(k, w * 0.36, h * 0.38, 46); lantern_post(k, w * 0.62, h * 0.26, 58)
    k.pine(w * 0.08, h * 0.04, 120); k.pine(w * 0.92, h * 0.28, 70)
    k.unclip()


def title(k, w, h):
    """The lodge on its hill with one winding path dug down the slope, a shovel in the bank."""
    k.snowfall(w * 0.04, h * 0.35, w * 0.96, h, n=40); k.stars(w * 0.06, h * 0.66, w * 0.94, h - 4, n=16); k.moon(w * 0.88, h * 0.84, 9)
    k.summit(w * 0.22, w * 0.78, h * 0.42, w * 0.42, w * 0.58, h * 0.7)
    k.lodge(w * 0.415, h * 0.7, w * 0.17, h * 0.12)
    k.forest(w * 0.02, w * 0.28, h * 0.42, 16, 32, 7); k.forest(w * 0.72, w * 0.98, h * 0.42, 16, 32, 7)
    k.ground(w * 0.02, w * 0.98, h * 0.43, depth=h * 0.43, drifts=0, ticks=False)
    path = [(w * 0.5 + w * 0.16 * math.sin(t * 5.2), lerp(h * 0.0, h * 0.42, t)) for t in [i / 40 for i in range(41)]]
    dug_path(k, path, w * 0.12, w * 0.04, wall=6)
    drifts(k, w * 0.04, w * 0.96, h * 0.05, h * 0.36, n=4)
    shovel(k, w * 0.2, h * 0.05, 52, ang=8); snowpile(k, w * 0.14, h * 0.03, 30)
    lantern_post(k, w * 0.8, h * 0.06, 40)


def op_garden(k, w, h):
    """Part One: the lodge garden, paths dug between fences, a bench and a shovel by the gate."""
    k.snowfall(0, h * 0.4, w, h, n=40); k.stars(6, h * 0.75, w - 6, h - 4, n=14)
    k.forest(0, w, h * 0.6, 16, 34, 16)
    k.ground(0, w, h * 0.6, depth=h * 0.6, drifts=1, ticks=False)
    k.lodge(w * 0.55, h * 0.6, w * 0.3, h * 0.2)
    p1 = [(lerp(w * 0.3, w * 0.66, t), lerp(h * 0.02, h * 0.59, t) + 3 * math.sin(t * 6)) for t in [i / 30 for i in range(31)]]
    dug_path(k, p1, w * 0.12, w * 0.04, wall=6)
    drifts(k, w * 0.04, w * 0.96, h * 0.05, h * 0.55, n=5)
    p2 = [(lerp(w * 0.38, w * 0.04, t), lerp(h * 0.18, h * 0.3, t)) for t in [i / 20 for i in range(21)]]
    dug_path(k, p2, w * 0.035, w * 0.025, wall=3.5)
    fence(k, w * 0.03, w * 0.24, h * 0.42, 12); fence(k, w * 0.72, w * 0.98, h * 0.3, 12)
    k.bench(w * 0.86, h * 0.08, 40); k.mug(w * 0.86, h * 0.08 + 16.5, 7)
    shovel(k, w * 0.16, h * 0.04, 54, ang=-8); snowpile(k, w * 0.08, h * 0.02, 26)
    lantern_post(k, w * 0.5, h * 0.3, 40)


def op_village(k, w, h):
    """Part Two: the village lanes, cottages on both sides and the lanes dug out between them."""
    k.snowfall(0, h * 0.35, w, h, n=40); k.stars(6, h * 0.72, w - 6, h - 4, n=14)
    k.forest(0, w, h * 0.55, 14, 26, 14)
    k.ground(0, w, h * 0.55, depth=h * 0.55, drifts=0, ticks=False)
    k.cottage(w * 0.03, h * 0.5, 44, 42); k.cottage(w * 0.2, h * 0.53, 36, 44, door_side=0.2)
    k.cottage(w * 0.66, h * 0.52, 42, 40); k.cottage(w * 0.84, h * 0.5, 36, 44, door_side=0.2)
    lane = [(lerp(w * 0.5, w * 0.48, t) + w * 0.04 * math.sin(t * 4), lerp(h * 0.0, h * 0.53, t)) for t in [i / 30 for i in range(31)]]
    dug_path(k, lane, w * 0.16, w * 0.05, wall=6)
    drifts(k, w * 0.04, w * 0.96, h * 0.05, h * 0.25, n=4)
    cross = [(lerp(w * 0.04, w * 0.96, t), h * 0.3 + 3 * math.sin(t * 5)) for t in [i / 40 for i in range(41)]]
    dug_path(k, cross, w * 0.04, w * 0.04, wall=3.5)
    k.lamppost(w * 0.36, h * 0.33, 40); k.lamppost(w * 0.64, h * 0.33, 40)
    k.signpost(w * 0.12, h * 0.05, 24, arrows=[("LODGE", 1)])
    shovel(k, w * 0.8, h * 0.06, 46, ang=10); snowpile(k, w * 0.88, h * 0.04, 26)
    k.pine(w * 0.95, h * 0.04, 40)


def op_station(k, w, h):
    """Part Three: the station yard, the platform swept, paths dug across the yard to the lamps."""
    k.snowfall(0, h * 0.3, w, h, n=46); k.stars(6, h * 0.76, w - 6, h - 4, n=10); k.moon(w * 0.12, h * 0.84, 10)
    k.mountains(0, w, h * 0.56, [(w * 0.2, h * 0.72), (w * 0.55, h * 0.8), (w * 0.85, h * 0.7)])
    k.forest(0, w, h * 0.54, 12, 22, 18)
    k.ground(0, w, h * 0.54, depth=h * 0.54, drifts=0, ticks=False)
    k.station(w * 0.32, h * 0.56, w * 0.34, h * 0.3, name="FROSTWOOD")
    k.water_tower(w * 0.84, h * 0.53, 54)
    k.rails(0, w, h * 0.46)
    yard = [(lerp(w * 0.5, w * 0.5, t) + w * 0.1 * math.sin(t * 3), lerp(h * 0.0, h * 0.44, t)) for t in [i / 30 for i in range(31)]]
    dug_path(k, yard, w * 0.14, w * 0.05, wall=6)
    drifts(k, w * 0.04, w * 0.96, h * 0.06, h * 0.4, n=5)
    side = [(lerp(w * 0.55, w * 0.95, t), lerp(h * 0.2, h * 0.26, t)) for t in [i / 20 for i in range(21)]]
    dug_path(k, side, w * 0.035, w * 0.03, wall=3.5)
    lantern_post(k, w * 0.3, h * 0.2, 36); lantern_post(k, w * 0.7, h * 0.28, 30)
    k.signal(w * 0.1, h * 0.46, 34)
    shovel(k, w * 0.16, h * 0.04, 46, ang=-10); snowpile(k, w * 0.24, h * 0.03, 28)
    k.sled(w * 0.86, h * 0.06, 34)


def op_meadows(k, w, h):
    """Part Four: the high meadows, a long path zig-zagging up to a mountain hut below the peaks."""
    k.snowfall(0, h * 0.4, w, h, n=36); k.stars(6, h * 0.7, w - 6, h - 4, n=40, big=0.25); k.moon(w * 0.86, h * 0.86, 12)
    k.mountains(0, w, h * 0.5, [(w * 0.1, h * 0.74), (w * 0.38, h * 0.86), (w * 0.66, h * 0.72), (w * 0.9, h * 0.8)])
    k.ground(0, w, h * 0.5, depth=h * 0.5, drifts=2, ticks=False)
    k.cabin(w * 0.6, h * 0.5, w * 0.12, h * 0.1)
    zz = [(w * 0.3, h * 0.0), (w * 0.62, h * 0.14), (w * 0.34, h * 0.27), (w * 0.6, h * 0.38), (w * 0.64, h * 0.49)]
    pts = []
    for (xa, ya), (xb, yb) in zip(zz, zz[1:]):
        pts += [(lerp(xa, xb, t), lerp(ya, yb, t)) for t in [i / 12 for i in range(12)]]
    pts.append(zz[-1])
    dug_path(k, pts, w * 0.1, w * 0.03, wall=5)
    drifts(k, w * 0.04, w * 0.96, h * 0.04, h * 0.46, n=6)
    k.forest(w * 0.02, w * 0.22, h * 0.22, 14, 30, 6); k.forest(w * 0.78, w * 0.98, h * 0.18, 14, 30, 6)
    k.signpost(w * 0.76, h * 0.42, 20, arrows=[("HUT", -1)])
    shovel(k, w * 0.14, h * 0.04, 44, ang=6); snowpile(k, w * 0.07, h * 0.02, 24)
    for i, (x, y) in enumerate(zz[1:4]): lantern_post(k, x + (10 if i % 2 == 0 else -14), y + 2, 24)


def v_shovel(k, w, h):
    k.ground(0, w, h * 0.16, depth=h * 0.16, drifts=0, ticks=False)
    snowpile(k, w * 0.42, h * 0.16, w * 0.32, h * 0.32); shovel(k, w * 0.6, h * 0.12, h * 0.66, ang=-14)
    k.pine(w * 0.12, h * 0.16, h * 0.6); k.pine(w * 0.88, h * 0.16, h * 0.66)


def v_sled(k, w, h):
    k.ground(0, w, h * 0.16, depth=h * 0.16, drifts=0, ticks=False)
    k.sled(w * 0.5, h * 0.16, w * 0.3); k.footprints([(w * (0.14 + 0.045 * i), h * (0.07 + 0.012 * (i % 2))) for i in range(7)])
    k.pine(w * 0.86, h * 0.16, h * 0.6)


def v_lantern(k, w, h):
    path = [(lerp(w * 0.5, w * 0.47, t), lerp(h * 0.0, h * 0.5, t)) for t in [i / 16 for i in range(17)]]
    k.ground(0, w, h * 0.52, depth=h * 0.52, drifts=0, ticks=False)
    k.stars(4, h * 0.62, w - 4, h - 4, n=8)
    dug_path(k, path, w * 0.2, w * 0.06, wall=3)
    lantern_post(k, w * 0.26, h * 0.12, h * 0.62); lantern_post(k, w * 0.7, h * 0.3, h * 0.46)


def v_mug(k, w, h):
    k.ground(0, w, h * 0.12, depth=h * 0.12, drifts=0, ticks=False)
    k.bench(w * 0.5, h * 0.12, h * 1.1); k.mug(w * 0.44, h * 0.12 + h * 0.44 + 0.5, h * 0.24)
    shovel(k, w * 0.82, h * 0.1, h * 0.64, ang=-12)


def v_snowman(k, w, h):
    k.ground(0, w, h * 0.12, depth=h * 0.12, drifts=0, ticks=False)
    k.snowman(w * 0.5, h * 0.12, h * 0.8); snowpile(k, w * 0.22, h * 0.12, w * 0.2, h * 0.22)
    k.pine(w * 0.84, h * 0.12, h * 0.66)


def v_moon(k, w, h):
    k.stars(4, h * 0.4, w - 4, h - 4, n=12); k.moon(w * 0.88, h * 0.76, h * 0.12)
    k.ground(0, w, h * 0.22, depth=h * 0.22, drifts=0, ticks=False)
    path = [(lerp(w * 0.08, w * 0.62, t), h * 0.12 + 2 * math.sin(t * 4)) for t in [i / 16 for i in range(17)]]
    dug_path(k, path, h * 0.12, h * 0.1, wall=2.5)
    k.pine(w * 0.2, h * 0.2, h * 0.6); k.pine(w * 0.3, h * 0.2, h * 0.45); lantern_post(k, w * 0.64, h * 0.18, h * 0.5)


def thanks(k, w, h):
    k.ground(0, w, h * 0.3, depth=h * 0.3, drifts=0, ticks=False)
    k.cottage(w * 0.62, h * 0.3, 40, 36)
    path = [(lerp(w * 0.3, w * 0.7, t), lerp(h * 0.0, h * 0.29, t)) for t in [i / 16 for i in range(17)]]
    dug_path(k, path, w * 0.1, w * 0.05, wall=3)
    shovel(k, w * 0.2, h * 0.08, h * 0.46, ang=-8); k.pine(w * 0.9, h * 0.3, h * 0.6)
    k.stars(w * 0.1, h * 0.7, w * 0.9, h - 3, n=8)


VIGNETTES = ["v_shovel", "v_sled", "v_lantern", "v_mug", "v_snowman"]
SPECS = {  # name: (width in, height in, function, seed)
    "frontispiece": (4.7, 7.0, frontispiece, 61),
    "title": (4.7, 2.5, title, 3),
    "opener-easy": (4.7, 2.4, op_garden, 11), "opener-medium": (4.7, 2.4, op_village, 12),
    "opener-hard": (4.7, 2.4, op_station, 13), "opener-expert": (4.7, 2.4, op_meadows, 14),
    "thanks": (3.4, 1.5, thanks, 21),
    "v_moon": (1.9, 0.85, v_moon, 90),
    **{n: (1.9, 0.85, globals()[n], 80 + i) for i, n in enumerate(VIGNETTES)},
}

if __name__ == "__main__":
    only = set(sys.argv[1:])
    for name, (wi, hi, fn, seed) in SPECS.items():
        if only and name not in only: continue
        render(os.path.join(OUT, name + ".png"), wi, hi, fn, seed=seed); print("drew", name)
