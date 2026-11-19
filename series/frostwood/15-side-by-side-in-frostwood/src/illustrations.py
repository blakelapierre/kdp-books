"""B&W ink illustrations for Side by Side in Frostwood -> ../illustrations/*.png
Uses the shared house-style inkart.py unchanged; the numbered peg rail, mug shelf and
scarves are drawn here from inkart primitives. Run from src/: python3 illustrations.py
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inkart import render, K, Wt
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "illustrations")

def scarf(k, x, y, h, striped=True):
    """Scarf hanging from a peg at (x, y): two tails with stripes and fringe."""
    w = h * 0.16
    for dx, L in ((-w * 0.55, h), (w * 0.55, h * 0.82)):
        pts = [(x + dx - w / 2, y), (x + dx + w / 2, y), (x + dx + w / 2 + 1, y - L), (x + dx - w / 2 + 1, y - L)]
        k.shape(pts, lw=0.8, fill=Wt, amp=0.05)
        if striped:
            for t in (0.3, 0.55, 0.8):
                yy = y - L * t
                k.blob([(x + dx - w / 2 + 0.2, yy), (x + dx + w / 2 + 0.5, yy), (x + dx + w / 2 + 0.6, yy - L * 0.07), (x + dx - w / 2 + 0.3, yy - L * 0.07)], K)
        for f in range(4):
            fx = x + dx - w / 2 + 1 + w * (f + 0.5) / 4
            k.line([(fx, y - L), (fx, y - L - h * 0.07)], lw=0.5, amp=0)
    k.shape(k.arcpts(x, y, w * 1.1, w * 0.5, 0, 360, 20), lw=0.8, fill=Wt, amp=0)

def mittens(k, x, y, h):
    """A pair of mittens on a string hanging from (x, y)."""
    k.line([(x - h * 0.3, y - h * 0.35), (x, y), (x + h * 0.3, y - h * 0.35)], lw=0.5, amp=0.1)
    for sx, fill in ((-1, Wt), (1, K)):
        cx = x + sx * h * 0.3
        body = [(cx - h * 0.16, y - h * 0.35), (cx + h * 0.16, y - h * 0.35), (cx + h * 0.18, y - h * 0.8), (cx + h * 0.05, y - h), (cx - h * 0.12, y - h * 0.98), (cx - h * 0.18, y - h * 0.8)]
        k.shape(body, lw=0.8, fill=fill, amp=0.05)
        th = [(cx + sx * h * 0.17, y - h * 0.62), (cx + sx * h * 0.3, y - h * 0.68), (cx + sx * h * 0.28, y - h * 0.8), (cx + sx * h * 0.17, y - h * 0.8)]
        k.shape(th, lw=0.8, fill=fill, amp=0.05)
        k.rect(cx - h * 0.17, y - h * 0.44, h * 0.34, h * 0.09, lw=0.6)

def hat(k, x, y, h):
    """Bobble hat hanging from (x, y)."""
    w = h * 0.8
    dome = k.arcpts(x, y - h * 0.75, w / 2, h * 0.6, 0, 180, 20)
    k.shape(dome + [(x - w / 2, y - h * 0.75)], lw=0.8, fill=Wt, amp=0.05)
    k.rect(x - w / 2 - 1, y - h, w + 2, h * 0.25, lw=0.8)
    k.hatch([(x - w / 2, y - h), (x + w / 2, y - h), (x + w / 2, y - h * 0.75), (x - w / 2, y - h * 0.75)], angle=90, gap=1.6, lw=0.4)
    k.circle(x, y - h * 0.12, h * 0.13, lw=0.7, fill=Wt)

def peg_rail(k, x0, x1, y, n, h, numbers=True):
    """A plank of n numbered pegs, left to right, with scarves, mittens and hats hanging."""
    k.rect(x0, y, x1 - x0, h * 0.16, lw=0.9)
    k.hatch([(x0, y), (x1, y), (x1, y + h * 0.16), (x0, y + h * 0.16)], angle=0, gap=2.2, lw=0.35)
    step = (x1 - x0) / n
    items = [scarf, mittens, hat, scarf, hat, mittens, scarf]
    for i in range(n):
        px = x0 + step * (i + 0.5)
        k.circle(px, y - h * 0.02, h * 0.035, lw=0.7, fill=K)
        if numbers:
            k.circle(px, y + h * 0.3, h * 0.09, lw=0.6, fill=Wt)
            k.text(px, y + h * 0.27, str(i + 1), size=h * 0.11, font="Ink-Playfair")
        f = items[i % len(items)]
        if f is scarf: scarf(k, px, y - h * 0.02, h * 0.62, striped=i % 2 == 0)
        elif f is mittens: mittens(k, px, y - h * 0.02, h * 0.42)
        else: hat(k, px, y - h * 0.08, h * 0.36)

def mug_shelf(k, x0, x1, y, n, h):
    """A shelf with n mugs side by side."""
    k.rect(x0, y - h * 0.08, x1 - x0, h * 0.08, lw=0.8)
    for sx in (0.12, 0.88):
        bx = x0 + (x1 - x0) * sx
        k.line([(bx, y - h * 0.08), (bx, y - h * 0.3), (bx + (h * 0.15 if sx < 0.5 else -h * 0.15), y - h * 0.08)], lw=0.7, amp=0)
    step = (x1 - x0) / n
    for i in range(n):
        k.mug(x0 + step * (i + 0.42), y, h * 0.36, steam=(i % 2 == 0), cocoa=(i % 3 != 1))

def sled_row(k, x0, x1, y, n, w):
    step = (x1 - x0) / n
    for i in range(n):
        k.sled(x0 + step * (i + 0.5), y, w)

def lodge_scene(k, w, h, base):
    k.snowfall(0, base, w, h, n=int(w * h / 1000))
    k.stars(6, base + (h - base) * 0.55, w - 6, h - 4, n=int(w / 10))
    k.moon(w * 0.82, h - (h - base) * 0.18, min(12, (h - base) * 0.11))
    k.mountains(0, w, base + (h - base) * 0.08, [(w * 0.15, base + (h - base) * 0.5), (w * 0.4, base + (h - base) * 0.72), (w * 0.7, base + (h - base) * 0.48), (w * 0.92, base + (h - base) * 0.6)])
    k.lodge(w * 0.32, base + (h - base) * 0.08, w * 0.36, (h - base) * 0.28)
    k.forest(0, w * 0.28, base + (h - base) * 0.05, (h - base) * 0.14, (h - base) * 0.28, int(w / 45))
    k.forest(w * 0.72, w, base + (h - base) * 0.05, (h - base) * 0.14, (h - base) * 0.28, int(w / 50))
    k.ground(0, w, base + (h - base) * 0.08, depth=(h - base) * 0.08 + base, drifts=4)

def frontispiece(k, w, h):
    m = 9; k.frame(m, m, w - m, h - m)
    k.clip_rect(m + 4, m + 4, w - m - 4, h - m - 4)
    k.snowfall(0, h * 0.45, w, h, n=80)
    k.stars(20, h * 0.72, w - 20, h - 20, n=50, big=0.18, rmax=3.4)
    k.moon(w * 0.78, h * 0.88, 18)
    k.mountains(0, w, h * 0.6, [(w * 0.12, h * 0.74), (w * 0.38, h * 0.84), (w * 0.65, h * 0.72), (w * 0.9, h * 0.8)])
    k.lodge(w * 0.3, h * 0.58, w * 0.4, h * 0.14)
    k.forest(0, w * 0.28, h * 0.58, 16, 30, 7)
    k.forest(w * 0.72, w, h * 0.58, 16, 28, 6)
    k.ground(0, w, h * 0.6, depth=h * 0.04, drifts=3)
    # the boot-room wall below: the numbered peg rail
    k.rect(m + 4, m + 4, w - 2 * m - 8, h * 0.54, lw=0.9)
    peg_rail(k, w * 0.1, w * 0.9, h * 0.45, 5, 92)
    k.bench(w * 0.5, m + 10, w * 0.5)
    for i, x in enumerate((0.36, 0.45, 0.55, 0.64)):
        k.mug(w * x, m + 10 + w * 0.5 * 0.39, 14, steam=i % 2 == 0)
    k.lantern(w * 0.13, m + 12, 30); k.lantern(w * 0.87, m + 12, 30)
    k.unclip()

def title(k, w, h):
    lodge_scene(k, w, h, h * 0.36)
    peg_rail(k, w * 0.2, w * 0.8, h * 0.3, 5, 48, numbers=False)
    k.pine(w * 0.06, h * 0.04, 64); k.pine(w * 0.94, h * 0.04, 70)

def op_lodge(k, w, h):
    k.snowfall(0, h * 0.5, w, h, n=30); k.stars(6, h * 0.78, w - 6, h - 4, n=18)
    k.mountains(0, w, h * 0.56, [(w * 0.2, h * 0.8), (w * 0.5, h * 0.9), (w * 0.8, h * 0.78)])
    k.lodge(w * 0.36, h * 0.54, w * 0.28, h * 0.2)
    k.ground(0, w, h * 0.56, depth=h * 0.04, drifts=3)
    peg_rail(k, w * 0.14, w * 0.86, h * 0.42, 6, 50)
    k.pine(w * 0.05, h * 0.02, 56); k.pine(w * 0.95, h * 0.02, 60)

def op_village(k, w, h):
    k.snowfall(0, 0, w, h, n=40); k.stars(6, h * 0.74, w - 6, h - 4, n=20); k.moon(w * 0.88, h * 0.86, 10)
    k.mountains(0, w, h * 0.45, [(w * 0.25, h * 0.75), (w * 0.55, h * 0.68), (w * 0.85, h * 0.76)])
    for i in range(5):
        k.cottage(w * (0.05 + i * 0.185), h * 0.3, w * 0.15, h * (0.26 + 0.04 * (i % 2)), door_side=0.62)
    k.ground(0, w, h * 0.3, depth=h * 0.3, drifts=3)
    k.lamppost(w * 0.04, h * 0.04, 54); k.lamppost(w * 0.96, h * 0.04, 54)
    k.bench(w * 0.5, h * 0.04, 90); mug_shelf(k, w * 0.5 - 36, w * 0.5 + 36, h * 0.04 + 90 * 0.39 + 1, 4, 24)

def op_railway(k, w, h):
    k.snowfall(0, 0, w, h, n=40); k.stars(6, h * 0.78, w - 6, h - 4, n=16)
    k.mountains(0, w, h * 0.42, [(w * 0.2, h * 0.7), (w * 0.5, h * 0.82), (w * 0.82, h * 0.68)])
    k.forest(0, w, h * 0.4, 18, 34, 16)
    k.ground(0, w, h * 0.4, depth=h * 0.4, drifts=3)
    k.rails(0, w, h * 0.24)
    k.carriage(w * 0.02, h * 0.24, w * 0.3, facing=1, n_win=6)
    k.carriage(w * 0.33, h * 0.24, w * 0.3, facing=1, n_win=6)
    k.locomotive(w * 0.66, h * 0.24, w * 0.3, facing=1)
    k.ground(0, w, h * 0.2, depth=h * 0.2, drifts=2, ticks=False)
    for i, x in enumerate((0.2, 0.32, 0.44, 0.56, 0.68, 0.8)): k.lantern(w * x, h * 0.03, 22)

def op_mountain(k, w, h):
    k.snowfall(0, 0, w, h, n=40); k.stars(6, h * 0.6, w - 6, h - 4, n=36, big=0.22); k.moon(w * 0.84, h * 0.84, 12)
    k.mountains(0, w, h * 0.3, [(w * 0.2, h * 0.62), (w * 0.48, h * 0.82), (w * 0.78, h * 0.6)])
    k.ground(0, w, h * 0.3, depth=h * 0.3, drifts=2)
    for i in range(4):
        k.cabin(w * (0.14 + i * 0.2), h * 0.3, w * 0.13, h * 0.16)
    sled_row(k, w * 0.12, w * 0.88, h * 0.05, 5, w * 0.12)
    k.pine(w * 0.05, h * 0.02, 58); k.pine(w * 0.95, h * 0.02, 62)

def _g(k, w, h):
    k.ground(0, w, h * 0.2, depth=h * 0.2, drifts=1, ticks=False)

def v_pegs(k, w, h):
    peg_rail(k, w * 0.12, w * 0.88, h * 0.8, 5, h * 0.95, numbers=False)

def v_mugs(k, w, h):
    mug_shelf(k, w * 0.2, w * 0.8, h * 0.28, 4, h * 0.6); k.pine(w * 0.08, h * 0.05, h * 0.55); k.pine(w * 0.92, h * 0.05, h * 0.5)

def v_bench(k, w, h):
    _g(k, w, h); k.bench(w * 0.5, h * 0.18, h * 0.9)
    for i, x in enumerate((0.42, 0.5, 0.58)): k.mug(w * x, h * 0.18 + h * 0.35, h * 0.16, steam=i != 1)
    k.pine(w * 0.12, h * 0.18, h * 0.6, style="line"); k.pine(w * 0.88, h * 0.18, h * 0.55)

def v_sleds(k, w, h):
    _g(k, w, h); sled_row(k, w * 0.22, w * 0.78, h * 0.2, 3, h * 0.3); k.pine(w * 0.1, h * 0.18, h * 0.62); k.pine(w * 0.9, h * 0.18, h * 0.56)

def v_lantern(k, w, h):
    _g(k, w, h)
    for x in (0.35, 0.5, 0.65): k.lantern(w * x, h * 0.2, h * 0.36)
    k.pine(w * 0.15, h * 0.18, h * 0.65, style="line"); k.pine(w * 0.85, h * 0.18, h * 0.6)

def v_sign(k, w, h):
    _g(k, w, h); k.signpost(w * 0.45, h * 0.16, h * 0.55, arrows=[("LODGE", 1), ("", -1)]); k.pine(w * 0.18, h * 0.18, h * 0.7)

def thanks(k, w, h):
    lodge_scene(k, w, h, h * 0.3)
    mug_shelf(k, w * 0.38, w * 0.62, h * 0.12, 4, 22)
    k.pine(w * 0.06, h * 0.04, 50); k.pine(w * 0.94, h * 0.04, 54)

VIGNETTES = ["v_pegs", "v_mugs", "v_bench", "v_sleds", "v_lantern", "v_sign"]
SPECS = {
    "frontispiece": (4.7, 7.0, frontispiece, 51),
    "title": (4.7, 2.6, title, 7),
    "opener-easy": (4.7, 2.4, op_lodge, 21),
    "opener-medium": (4.7, 2.4, op_village, 22),
    "opener-hard": (4.7, 2.4, op_railway, 23),
    "opener-expert": (4.7, 2.4, op_mountain, 24),
    "thanks": (3.6, 1.7, thanks, 31),
    **{n: (1.9, 0.85, globals()[n], 60 + i) for i, n in enumerate(VIGNETTES)},
}

if __name__ == "__main__":
    only = set(sys.argv[1:])
    os.makedirs(OUT, exist_ok=True)
    for name, (wi, hi, fn, seed) in SPECS.items():
        if only and name not in only: continue
        render(os.path.join(OUT, name + ".png"), wi, hi, fn, seed=seed); print("drew", name)
