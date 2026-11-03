"""Draws the black-and-white ink illustrations for The Icicles of Frostwood -> ../illustrations/*.png
(300 DPI grayscale, pure black line art on white, same inkart house style as the other Frostwood books).
Subjects: icicles hanging from eaves, the lodge, the village lanes, the station canopy and the high
meadows in frost. No people. Deterministic: same seeds -> same images. Run from src/: python3 illustrations.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inkart import render, Wt, K, lerp
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "illustrations")


# ----------------------------------------------------------------------------- local helpers
def icicle(k, x, y, L, w):
    """One long icicle hanging from (x, y): a tapered white spike with a shaded right flank, a few
    ripple rings and a drop forming at the tip."""
    n = 14; left = []; right = []
    for i in range(n + 1):
        t = i / n; ww = w * (1 - t) ** 1.15 * (1 + 0.1 * math.sin(t * 13 + x))
        left.append((x - ww / 2, y - L * t)); right.append((x + ww / 2, y - L * t))
    k.shape(left + right[::-1], lw=0.6, fill=Wt, amp=0.05)
    k.blob([right[i] for i in range(0, n)] + [(px - w * 0.18 * (1 - i / n), py) for i, (px, py) in list(enumerate(right))[n - 1::-1]], K)
    for i in range(2, n - 3, 3):
        t = i / n; ww = w * (1 - t) ** 1.15 * 0.5
        k.line([(x - ww, y - L * t), (x, y - L * t - 0.6), (x + ww * 0.4, y - L * t)], lw=0.3, amp=0)
    k.circle(x, y - L - 1.2, max(0.35, w * 0.09), lw=0.3, fill=Wt)


def eave(k, x0, x1, y, depth=5, snow=3):
    """A straight roof edge seen from below: a hatched beam with a soft snow cap on top."""
    k.shape([(x0, y), (x1, y), (x1, y + depth), (x0, y + depth)], lw=0.9, fill=Wt, amp=0.1)
    k.hatch([(x0, y), (x1, y), (x1, y + depth), (x0, y + depth)], angle=0, gap=1.4, lw=0.35, jitter=0.05)
    top = [(x0 - 2 + (x1 - x0 + 4) * t, y + depth + snow * (0.7 + 0.3 * math.sin(t * 23))) for t in [i / 40 for i in range(41)]]
    k.shape([(x0 - 2, y + depth)] + top + [(x1 + 2, y + depth)], lw=0.8, fill=Wt, amp=0.15)


def icicle_row(k, x0, x1, y, lens, w):
    """Icicles of the given lengths, evenly spaced under an edge from x0 to x1."""
    n = len(lens)
    for i, L in enumerate(lens):
        icicle(k, lerp(x0, x1, (i + 0.5) / n), y, L, w)


def random_lens(k, n, lo, hi):
    return [k.r.uniform(lo, hi) * (0.55 + 0.45 * abs(math.sin(i * 1.7 + 0.4))) for i in range(n)]


def lantern_post(k, x, y, h):
    k.c.setStrokeColor(K); k.c.setLineWidth(1.0); k.c.line(x, y, x, y + h * 0.78)
    k.c.line(x, y + h * 0.74, x + h * 0.16, y + h * 0.74)
    k.lantern(x + h * 0.16, y + h * 0.5, h * 0.22)
    icicle_row(k, x + h * 0.02, x + h * 0.14, y + h * 0.74, [h * 0.08, h * 0.13, h * 0.06], h * 0.025)


def fence(k, x0, x1, y, h):
    k.snowman_free_fence(x0, x1, y, h)   # split-rail fence half buried in snow


def drifts(k, x0, x1, y0, y1, n=6):
    """Soft drift lines across open snow, each with a few short shadow ticks underneath."""
    for i in range(n):
        L = (x1 - x0) * k.r.uniform(0.12, 0.26); xa = k.r.uniform(x0, x1 - L); yy = lerp(y0, y1, (i + 0.5) / n) + k.r.uniform(-3, 3)
        arc = [(xa + L * t, yy + 2.2 * math.sin(math.pi * t)) for t in [j / 12 for j in range(13)]]
        k.line(arc, lw=0.5, amp=0.15)
        for j in range(3):
            tx = xa + L * (0.3 + 0.2 * j); k.line([(tx, yy - 0.8), (tx - 1.2, yy - 3.2)], lw=0.3, amp=0)


def frozen_falls(k, x, y, w, h):
    """A small waterfall frozen solid on a rock ledge: a curtain of long icicles."""
    k.ledge(x - w * 0.6, x + w * 0.6, y + h, depth=8)
    lens = [h * (0.55 + 0.45 * abs(math.sin(i * 2.3))) for i in range(9)]
    icicle_row(k, x - w / 2, x + w / 2, y + h - 7, lens, w / 9 * 0.9)


# ----------------------------------------------------------------------------- scenes
def frontispiece(k, w, h):
    """The lodge at night seen from under the porch eave, a long row of icicles framing the view."""
    m = 9; k.frame(m, m, w - m, h - m)
    k.clip_rect(m + 4, m + 4, w - m - 4, h - m - 4)
    k.snowfall(0, h * 0.35, w, h * 0.8, n=70); k.stars(20, h * 0.55, w - 20, h * 0.78, n=30, big=0.15); k.moon(w * 0.78, h * 0.7, 16)
    k.mountains(0, w, h * 0.46, [(w * 0.12, h * 0.6), (w * 0.42, h * 0.68), (w * 0.72, h * 0.59), (w * 0.94, h * 0.64)])
    k.forest(0, w * 0.3, h * 0.44, 18, 34, 10); k.forest(w * 0.72, w, h * 0.44, 18, 34, 9)
    k.ground(0, w, h * 0.445, depth=h * 0.45, drifts=3, ticks=False)
    k.lodge(w * 0.28, h * 0.445, w * 0.44, h * 0.14)
    drifts(k, w * 0.04, w * 0.96, h * 0.06, h * 0.4, n=9)
    fence(k, w * 0.04, w * 0.32, h * 0.26, 14); fence(k, w * 0.66, w * 0.96, h * 0.2, 14)
    k.footprints([(w * (0.5 + 0.03 * math.sin(i)), h * (0.06 + 0.035 * i)) for i in range(10)])
    k.sled(w * 0.76, h * 0.08, 46)
    lantern_post(k, w * 0.36, h * 0.3, 46); lantern_post(k, w * 0.62, h * 0.22, 58)
    k.pine(w * 0.1, h * 0.03, 120); k.pine(w * 0.9, h * 0.22, 70)
    # the porch eave across the top, with long icicles of every length
    ey = h * 0.9
    eave(k, 0, w, ey, depth=h * 0.03, snow=5)
    k.blob([(0, ey + h * 0.03 + 5), (w, ey + h * 0.03 + 5), (w, h), (0, h)], K)
    icicle_row(k, m + 6, w - m - 6, ey, random_lens(k, 15, h * 0.05, h * 0.2), 7.5)
    k.unclip()


def title(k, w, h):
    """The lodge on its hill under the moon, framed by an icicled eave above."""
    k.snowfall(w * 0.04, h * 0.3, w * 0.96, h * 0.72, n=36); k.stars(w * 0.06, h * 0.5, w * 0.94, h * 0.72, n=14); k.moon(w * 0.86, h * 0.62, 8)
    k.summit(w * 0.22, w * 0.78, h * 0.3, w * 0.42, w * 0.58, h * 0.52)
    k.lodge(w * 0.415, h * 0.52, w * 0.17, h * 0.1)
    k.forest(w * 0.02, w * 0.28, h * 0.3, 16, 30, 7); k.forest(w * 0.72, w * 0.98, h * 0.3, 16, 30, 7)
    k.ground(w * 0.02, w * 0.98, h * 0.31, depth=h * 0.31, drifts=2, ticks=False)
    lantern_post(k, w * 0.2, h * 0.03, 40); lantern_post(k, w * 0.8, h * 0.03, 40)
    ey = h * 0.86
    eave(k, w * 0.02, w * 0.98, ey, depth=5, snow=4)
    icicle_row(k, w * 0.04, w * 0.96, ey, random_lens(k, 17, h * 0.06, h * 0.2), 5.5)


def op_eaves(k, w, h):
    """Part One: the lodge with its eaves full of icicles, a bench and a mug by the door."""
    k.snowfall(0, h * 0.4, w, h, n=40); k.stars(6, h * 0.75, w - 6, h - 4, n=14)
    k.forest(0, w, h * 0.3, 16, 34, 16)
    k.ground(0, w, h * 0.3, depth=h * 0.3, drifts=1, ticks=False)
    k.lodge(w * 0.3, h * 0.3, w * 0.4, h * 0.38)
    for (x0, x1, yy, n) in ((w * 0.33, w * 0.44, h * 0.3 + h * 0.38 * 0.55, 5), (w * 0.56, w * 0.67, h * 0.3 + h * 0.38 * 0.55, 5)):
        icicle_row(k, x0, x1, yy - 3, random_lens(k, n, 5, 12), 2.2)
    drifts(k, w * 0.04, w * 0.96, h * 0.04, h * 0.26, n=4)
    fence(k, w * 0.03, w * 0.24, h * 0.16, 12); fence(k, w * 0.76, w * 0.98, h * 0.12, 12)
    k.bench(w * 0.86, h * 0.04, 40); k.mug(w * 0.86, h * 0.04 + 16.5, 7)
    lantern_post(k, w * 0.16, h * 0.04, 44)


def op_village(k, w, h):
    """Part Two: the village lane at night, icicles hanging from every cottage roof."""
    k.snowfall(0, h * 0.35, w, h, n=40); k.stars(6, h * 0.72, w - 6, h - 4, n=14)
    k.forest(0, w, h * 0.55, 14, 26, 14)
    k.ground(0, w, h * 0.55, depth=h * 0.55, drifts=0, ticks=False)
    for (x, y, cw, ch) in ((w * 0.03, h * 0.5, 44, 42), (w * 0.2, h * 0.53, 36, 44), (w * 0.66, h * 0.52, 42, 40), (w * 0.84, h * 0.5, 36, 44)):
        k.cottage(x, y, cw, ch)
        icicle_row(k, x - 1, x + cw + 1, y + ch * 0.6 - 3, random_lens(k, 6, 3, 9), 1.8)
    drifts(k, w * 0.04, w * 0.96, h * 0.05, h * 0.25, n=4)
    k.footprints([(w * (0.47 + 0.02 * (i % 2)), h * (0.04 + 0.05 * i)) for i in range(9)])
    k.lamppost(w * 0.36, h * 0.33, 40); k.lamppost(w * 0.64, h * 0.33, 40)
    k.signpost(w * 0.12, h * 0.05, 24, arrows=[("LODGE", 1)])
    k.sled(w * 0.82, h * 0.06, 34)
    k.pine(w * 0.95, h * 0.04, 40)


def op_station(k, w, h):
    """Part Three: the station platform under a long canopy hung with icicles, the water tower beyond."""
    k.snowfall(0, h * 0.3, w, h * 0.8, n=40); k.stars(6, h * 0.62, w - 6, h * 0.8, n=10); k.moon(w * 0.12, h * 0.7, 9)
    k.mountains(0, w, h * 0.4, [(w * 0.2, h * 0.56), (w * 0.55, h * 0.64), (w * 0.85, h * 0.54)])
    k.forest(0, w, h * 0.38, 12, 22, 18)
    k.ground(0, w, h * 0.38, depth=h * 0.38, drifts=0, ticks=False)
    k.station(w * 0.34, h * 0.4, w * 0.3, h * 0.26, name="FROSTWOOD")
    k.water_tower(w * 0.84, h * 0.37, 50)
    k.rails(0, w, h * 0.3)
    drifts(k, w * 0.04, w * 0.96, h * 0.04, h * 0.24, n=4)
    k.signal(w * 0.1, h * 0.3, 34)
    k.bench(w * 0.3, h * 0.05, 36); lantern_post(k, w * 0.7, h * 0.04, 40)
    ey = h * 0.84
    eave(k, 0, w, ey, depth=6, snow=4)
    k.blob([(0, ey + 10), (w, ey + 10), (w, h), (0, h)], K)
    icicle_row(k, 4, w - 4, ey, random_lens(k, 24, h * 0.04, h * 0.16), 4.2)


def op_meadows(k, w, h):
    """Part Four: the high meadows, a frozen waterfall of icicles below the peaks and a hut beside it."""
    k.snowfall(0, h * 0.4, w, h, n=36); k.stars(6, h * 0.7, w - 6, h - 4, n=40, big=0.25); k.moon(w * 0.86, h * 0.86, 12)
    k.mountains(0, w, h * 0.5, [(w * 0.1, h * 0.74), (w * 0.38, h * 0.86), (w * 0.66, h * 0.72), (w * 0.9, h * 0.8)])
    k.ground(0, w, h * 0.5, depth=h * 0.5, drifts=2, ticks=False)
    k.cabin(w * 0.66, h * 0.5, w * 0.12, h * 0.1)
    frozen_falls(k, w * 0.34, h * 0.14, w * 0.2, h * 0.3)
    k.pond(w * 0.34, h * 0.06, w * 0.3)
    drifts(k, w * 0.55, w * 0.96, h * 0.04, h * 0.42, n=4)
    k.forest(w * 0.02, w * 0.18, h * 0.22, 14, 30, 5); k.forest(w * 0.8, w * 0.98, h * 0.18, 14, 30, 6)
    k.signpost(w * 0.76, h * 0.42, 20, arrows=[("HUT", -1)])
    lantern_post(k, w * 0.6, h * 0.1, 34)


def v_icicles(k, w, h):
    eave(k, w * 0.1, w * 0.9, h * 0.8, depth=4, snow=3)
    icicle_row(k, w * 0.12, w * 0.88, h * 0.8, [h * f for f in (0.3, 0.55, 0.18, 0.66, 0.42, 0.24, 0.5)], 6)
    k.stars(4, h * 0.05, w * 0.1, h * 0.7, n=3); k.stars(w * 0.9, h * 0.05, w - 4, h * 0.7, n=3)


def v_lantern(k, w, h):
    k.ground(0, w, h * 0.14, depth=h * 0.14, drifts=0, ticks=False)
    k.stars(4, h * 0.62, w - 4, h - 4, n=8)
    lantern_post(k, w * 0.4, h * 0.14, h * 0.8); k.pine(w * 0.16, h * 0.14, h * 0.6); k.pine(w * 0.82, h * 0.14, h * 0.5)


def v_mug(k, w, h):
    k.ground(0, w, h * 0.12, depth=h * 0.12, drifts=0, ticks=False)
    k.bench(w * 0.5, h * 0.12, h * 1.1); k.mug(w * 0.44, h * 0.12 + h * 0.44 + 0.5, h * 0.24)
    icicle_row(k, w * 0.5 - h * 0.5, w * 0.5 + h * 0.5, h * 0.12 + h * 0.4, [h * 0.08, h * 0.14, h * 0.06, h * 0.11], 1.6)


def v_snowman(k, w, h):
    k.ground(0, w, h * 0.12, depth=h * 0.12, drifts=0, ticks=False)
    k.snowman(w * 0.5, h * 0.12, h * 0.8)
    k.pine(w * 0.18, h * 0.12, h * 0.55); k.pine(w * 0.84, h * 0.12, h * 0.66)


def v_cottage(k, w, h):
    k.ground(0, w, h * 0.12, depth=h * 0.12, drifts=0, ticks=False)
    cw = h * 0.85; x = w * 0.5 - cw / 2
    k.cottage(x, h * 0.12, cw, h * 0.78)
    icicle_row(k, x - 1, x + cw + 1, h * 0.12 + h * 0.78 * 0.6 - 3, [h * f for f in (0.08, 0.16, 0.1, 0.2, 0.07, 0.13)], 2.2)
    k.pine(w * 0.14, h * 0.12, h * 0.5); k.pine(w * 0.86, h * 0.12, h * 0.6)


def v_moon(k, w, h):
    k.stars(4, h * 0.3, w - 4, h * 0.6, n=8); k.moon(w * 0.2, h * 0.42, h * 0.1)
    k.ground(0, w, h * 0.14, depth=h * 0.14, drifts=0, ticks=False)
    k.pine(w * 0.7, h * 0.12, h * 0.5); k.pine(w * 0.82, h * 0.12, h * 0.38)
    eave(k, w * 0.05, w * 0.95, h * 0.82, depth=3, snow=2.5)
    icicle_row(k, w * 0.06, w * 0.94, h * 0.82, random_lens(k, 11, h * 0.08, h * 0.22), 3)


def thanks(k, w, h):
    k.ground(0, w, h * 0.22, depth=h * 0.22, drifts=0, ticks=False)
    k.cottage(w * 0.42, h * 0.22, 46, 40)
    icicle_row(k, w * 0.42 - 1, w * 0.42 + 47, h * 0.22 + 24 - 3, [4, 8, 5, 10, 6, 7], 2)
    k.pine(w * 0.12, h * 0.22, h * 0.6); k.pine(w * 0.9, h * 0.22, h * 0.6)
    k.mug(w * 0.24, h * 0.06, 12)
    k.stars(w * 0.1, h * 0.7, w * 0.9, h - 3, n=8)


VIGNETTES = ["v_icicles", "v_lantern", "v_mug", "v_snowman", "v_cottage"]
SPECS = {  # name: (width in, height in, function, seed)
    "frontispiece": (4.7, 7.0, frontispiece, 61),
    "title": (4.7, 2.5, title, 3),
    "opener-easy": (4.7, 2.4, op_eaves, 11), "opener-medium": (4.7, 2.4, op_village, 12),
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
