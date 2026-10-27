"""Draws the black-and-white ink illustrations for Chimneys of Frostwood -> ../illustrations/*.png
(300 DPI grayscale, pure black line art on white, same inkart house style as the other Frostwood books).
Subjects: snowy rooftops and their smoking chimneys: the village lanes, the lodge, the railway
station and the mountain hamlet. No people.
Deterministic: same seeds -> same images. Run from src/: python3 illustrations.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inkart import render, Wt, K, lerp
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "illustrations")


# ----------------------------------------------------------------------------- local helpers
def stack(k, x, y, w, h, pots=1, smoke=True, curl=1, sm=None):
    """A brick chimney stack whose base is at y (hidden later by the roof), with chimney pots and smoke."""
    k.shape([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], lw=0.8, fill=Wt, amp=0)
    # brick courses
    rows = max(2, int(h / 2.6))
    for i in range(1, rows):
        yy = y + h * i / rows
        k.line([(x, yy), (x + w, yy)], lw=0.3, amp=0)
        off = 0.5 if i % 2 else 0.0
        for j in range(3):
            xx = x + w * (off + j) / 2.4
            if x + 0.6 < xx < x + w - 0.6: k.line([(xx, yy - h / rows), (xx, yy)], lw=0.25, amp=0)
    k.hatch([(x + w * 0.62, y), (x + w, y), (x + w, y + h), (x + w * 0.62, y + h)], angle=90, gap=1.1, lw=0.3, jitter=0.05)
    cap = [(x - 1.2, y + h), (x + w + 1.2, y + h), (x + w + 1.2, y + h + 2.0), (x - 1.2, y + h + 2.0)]
    k.shape(cap, lw=0.7, fill=Wt, amp=0)
    k.blob([(x - 1.4, y + h + 2.0), (x + w / 2, y + h + 3.4), (x + w + 1.4, y + h + 2.0)], Wt)
    k.line([(x - 1.4, y + h + 2.0), (x + w / 2, y + h + 3.2), (x + w + 1.4, y + h + 2.0)], lw=0.4, amp=0)
    top = y + h + 2.6
    pw = min(w * 0.36, 3.2)
    for i in range(pots):
        px = x + w * (i + 1) / (pots + 1)
        ph = pw * 1.4
        k.shape([(px - pw / 2, top), (px + pw / 2, top), (px + pw * 0.42, top + ph), (px - pw * 0.42, top + ph)], lw=0.55, fill=Wt, amp=0)
        k.shape([(px - pw * 0.55, top + ph), (px + pw * 0.55, top + ph), (px + pw * 0.55, top + ph + 0.9), (px - pw * 0.55, top + ph + 0.9)], lw=0.5, fill=K, amp=0)
        if smoke: k.smoke(px, top + ph + 1.6, sm or max(14, h * 1.4), curl=curl)
    return top


def house(k, x, y, w, h, chim=None, lit=True, door=True, boards=True, roof_h=None, pots=1, smoke=True, curl=1):
    """A cottage whose wall base is at y. chim = (fraction along, height above the roof ridge level)."""
    wall_h = h * 0.58; rh = roof_h or h * 0.42
    if chim:
        f, ch = chim; cw = max(4.5, w * 0.13)
        cx = x + w * f - cw / 2
        # chimney base below the roof slope so the roof covers it
        stack(k, cx, y + wall_h + rh * 0.3, cw, rh * 0.7 + ch, pots=pots, smoke=smoke, curl=curl)
    k.wall(x, y, w, wall_h, boards=boards, gap=2.4)
    k.roof(x, x + w, y + wall_h, y + wall_h + rh, overhang=max(2.0, w * 0.06), snow=max(1.8, w * 0.05))
    if door:
        dw = w * 0.16
        k.shape([(x + w * 0.62, y), (x + w * 0.62 + dw, y), (x + w * 0.62 + dw, y + wall_h * 0.62), (x + w * 0.62, y + wall_h * 0.62)], lw=0.7, fill=K, amp=0)
        k.window(x + w * 0.16, y + wall_h * 0.32, w * 0.2, wall_h * 0.32, lit=lit)
    else:
        k.window(x + w * 0.4, y + wall_h * 0.32, w * 0.2, wall_h * 0.32, lit=lit)


def lane(k, x0, x1, y, heights, h=40, gap=2, tag=None, pots=None, curl=1, smoke=True):
    """A row of cottages along a lane; chimney i stands heights[i] 'storeys' above its ridge.
    If tag is given (a clue number) a little lantern-sign with that number is drawn at the left end."""
    n = len(heights); w = (x1 - x0 - gap * (n - 1)) / n
    unit = h * 0.16
    for i, hv in enumerate(heights):
        xx = x0 + i * (w + gap)
        house(k, xx, y, w, h * (0.92 + 0.12 * ((i * 7) % 3) / 2), chim=(0.3 + 0.4 * ((i * 5) % 3) / 2, unit * hv),
              lit=(i % 3 != 1), pots=(pots[i] if pots else 1 + (hv % 2)), curl=curl, smoke=smoke)
    if tag is not None:
        sign(k, x0 - 9, y, 16, tag)


def sign(k, x, y, h, num):
    """A little lane sign on a post with a number on it (the clue)."""
    k.line([(x, y), (x, y + h)], lw=1.0, amp=0)
    s = h * 0.5
    k.shape([(x - s / 2, y + h - s * 0.2), (x + s / 2, y + h - s * 0.2), (x + s / 2, y + h + s * 0.8), (x - s / 2, y + h + s * 0.8)], lw=0.7, fill=Wt, amp=0)
    k.blob([(x - s / 2 - 0.5, y + h + s * 0.8), (x, y + h + s * 1.05), (x + s / 2 + 0.5, y + h + s * 0.8)], Wt)
    k.line([(x - s / 2 - 0.5, y + h + s * 0.8), (x, y + h + s * 1.02), (x + s / 2 + 0.5, y + h + s * 0.8)], lw=0.4, amp=0)
    k.text(x, y + h + s * 0.02, str(num), size=s * 0.8, font="Ink-Plex")


def brush(k, x, y, L, ang=70):
    """A sweep's round chimney brush on its rod."""
    a = math.radians(ang); ex, ey = x + L * math.cos(a), y + L * math.sin(a)
    k.line([(x, y), (ex, ey)], lw=1.0, amp=0)
    r = L * 0.16
    for i in range(16):
        t = 2 * math.pi * i / 16
        k.line([(ex, ey), (ex + r * math.cos(t), ey + r * math.sin(t))], lw=0.45, amp=0)
    k.circle(ex, ey, r * 0.18, lw=0.4, fill=K)


def ladder(k, x, y, h, ang=78):
    a = math.radians(ang); dx, dy = math.cos(a) * h, math.sin(a) * h; w = h * 0.16
    for o in (0, w):
        k.line([(x + o, y), (x + o + dx, y + dy)], lw=0.9, amp=0)
    for i in range(1, 8):
        t = i / 8; k.line([(x + dx * t, y + dy * t), (x + w + dx * t, y + dy * t)], lw=0.6, amp=0)


def pots_row(k, x0, x1, y, heights, w=7):
    """Chimney pots of different heights in a row on a ridge (a little 'clue' picture)."""
    n = len(heights); step = (x1 - x0) / n
    for i, hv in enumerate(heights):
        stack(k, x0 + i * step + (step - w) / 2, y, w, hv * w * 0.9, pots=1, smoke=(hv == max(heights)), sm=w * 3)
    k.shape([(x0 - 3, y - 4), (x1 + 3, y - 4), (x1 + 3, y + 1), (x0 - 3, y + 1)], lw=0.8, fill=Wt, amp=0.1)
    k.blob([(x0 - 4, y + 1), (lerp(x0, x1, 0.3), y + 2.6), (lerp(x0, x1, 0.7), y + 2.2), (x1 + 4, y + 1)], Wt)


# ----------------------------------------------------------------------------- scenes
def frontispiece(k, w, h):
    """Frostwood village from the hill road on a still winter night: lanes of rooftops, every chimney smoking."""
    m = 9; k.frame(m, m, w - m, h - m)
    k.clip_rect(m + 4, m + 4, w - m - 4, h - m - 4)
    k.snowfall(0, h * 0.45, w, h, n=90); k.stars(20, h * 0.72, w - 20, h - 22, n=40, big=0.15); k.moon(w * 0.78, h * 0.88, 18)
    k.mountains(0, w, h * 0.62, [(w * 0.12, h * 0.74), (w * 0.45, h * 0.82), (w * 0.75, h * 0.75), (w * 0.95, h * 0.79)])
    k.forest(0, w * 0.32, h * 0.6, 16, 30, 9); k.forest(w * 0.72, w, h * 0.6, 16, 30, 9)
    k.ground(0, w, h * 0.61, depth=h * 0.08, drifts=1, ticks=False)
    k.lodge(w * 0.38, h * 0.61, w * 0.26, h * 0.09)
    k.ground(0, w, h * 0.55, depth=h * 0.55, drifts=0, ticks=False)
    lane(k, w * 0.06, w * 0.94, h * 0.47, [2, 4, 1, 5, 3, 2, 4], h=40, curl=1)
    k.ground(0, w, h * 0.45, depth=h * 0.45, drifts=0, ticks=False)
    lane(k, w * 0.04, w * 0.96, h * 0.32, [3, 1, 4, 2, 5, 1], h=52, curl=1)
    k.ground(0, w, h * 0.3, depth=h * 0.3, drifts=0, ticks=False)
    lane(k, w * 0.1, w * 0.9, h * 0.12, [1, 4, 2, 3], h=72, curl=1)
    k.ground(0, w, h * 0.1, depth=h * 0.1, drifts=2, ticks=True)
    k.lamppost(w * 0.05 + 8, h * 0.05, 64); k.pine(w * 0.95, h * 0.03, 80)
    k.footprints([(w * (0.3 + 0.05 * i), h * (0.04 + 0.006 * (i % 2))) for i in range(8)])
    k.unclip()


def title(k, w, h):
    """One snowy lane of five cottages, chimneys of five heights, smoke curling up."""
    k.snowfall(w * 0.04, h * 0.4, w * 0.96, h, n=34); k.stars(w * 0.06, h * 0.72, w * 0.94, h - 4, n=14); k.moon(w * 0.9, h * 0.86, 8)
    k.forest(w * 0.0, w * 1.0, h * 0.3, 14, 26, 14)
    k.ground(w * 0.0, w * 1.0, h * 0.3, depth=h * 0.3, drifts=0, ticks=False)
    lane(k, w * 0.12, w * 0.9, h * 0.18, [2, 3, 5, 1, 4], h=60)
    sign(k, w * 0.07, h * 0.12, 22, 3)
    k.ground(w * 0.0, w * 1.0, h * 0.14, depth=h * 0.14, drifts=1, ticks=False)


def op_village(k, w, h):
    """Part One: the village lanes, a terrace of cottages, the well and a sledge."""
    k.snowfall(0, h * 0.45, w, h, n=40); k.stars(6, h * 0.78, w - 6, h - 4, n=14)
    k.forest(0, w, h * 0.5, 14, 28, 14)
    k.ground(0, w, h * 0.5, depth=h * 0.5, drifts=0, ticks=False)
    lane(k, w * 0.08, w * 0.94, h * 0.34, [3, 1, 5, 2, 4], h=62)
    sign(k, w * 0.04, h * 0.3, 22, 2)
    k.ground(0, w, h * 0.32, depth=h * 0.32, drifts=1, ticks=False)
    k.sled(w * 0.66, h * 0.06, 32)
    k.footprints([(w * (0.12 + 0.04 * i), h * (0.08 + 0.006 * (i % 2))) for i in range(10)])
    k.lamppost(w * 0.94, h * 0.04, 40); k.firewood(w * 0.18, h * 0.05, 30, rows=2)


def op_lodge(k, w, h):
    """Part Two: the Frostwood Lodge, all its wings and huts sending up smoke."""
    k.snowfall(0, h * 0.4, w, h, n=40); k.stars(6, h * 0.76, w - 6, h - 4, n=14); k.moon(w * 0.1, h * 0.84, 10)
    k.mountains(0, w, h * 0.6, [(w * 0.18, h * 0.76), (w * 0.52, h * 0.84), (w * 0.84, h * 0.74)])
    k.forest(0, w, h * 0.56, 14, 28, 14)
    k.ground(0, w, h * 0.56, depth=h * 0.56, drifts=0, ticks=False)
    k.lodge(w * 0.32, h * 0.3, w * 0.36, h * 0.3)
    house(k, w * 0.04, h * 0.28, 50, 48, chim=(0.3, 14), pots=2)
    house(k, w * 0.78, h * 0.28, 48, 50, chim=(0.7, 7))
    k.ground(0, w, h * 0.29, depth=h * 0.29, drifts=1, ticks=False)
    k.firewood(w * 0.14, h * 0.05, 34, rows=3); k.sled(w * 0.7, h * 0.04, 30)
    k.signpost(w * 0.5, h * 0.02, 24, arrows=[("LODGE", 1)])


def op_station(k, w, h):
    """Part Three: the railway station roofs, water tower and engine shed, a locomotive waiting."""
    k.snowfall(0, h * 0.4, w, h, n=36); k.stars(6, h * 0.76, w - 6, h - 4, n=12)
    k.forest(0, w, h * 0.55, 14, 26, 14)
    k.ground(0, w, h * 0.55, depth=h * 0.55, drifts=0, ticks=False)
    house(k, w * 0.05, h * 0.3, 64, 64, chim=(0.25, 16), pots=2, door=False)
    house(k, w * 0.3, h * 0.3, 54, 58, chim=(0.7, 8))
    k.water_tower(w * 0.62, h * 0.3, 70)
    house(k, w * 0.74, h * 0.3, 60, 52, chim=(0.55, 22), pots=1, door=False)
    k.ground(0, w, h * 0.3, depth=h * 0.3, drifts=0, ticks=False)
    k.rails(0, w, h * 0.17)
    k.locomotive(w * 0.3, h * 0.18, 92, facing=1, smoke=True)
    k.ground(0, w, h * 0.12, depth=h * 0.12, drifts=1, ticks=False)
    k.signal(w * 0.92, h * 0.12, 40)


def op_hamlet(k, w, h):
    """Part Four: the high hamlet, huts and barns on the snowfield below the summit."""
    k.snowfall(0, h * 0.45, w, h, n=36); k.stars(6, h * 0.66, w - 6, h - 4, n=36, big=0.25); k.moon(w * 0.82, h * 0.86, 12)
    k.summit(w * 0.15, w * 0.85, h * 0.45, w * 0.4, w * 0.6, h * 0.92)
    k.ground(0, w, h * 0.46, depth=h * 0.46, drifts=0, ticks=False)
    for i, (fx, fy, s, ch) in enumerate([(0.05, 0.42, 30, 5), (0.22, 0.44, 26, 10), (0.66, 0.43, 28, 3), (0.84, 0.41, 30, 8)]):
        house(k, w * fx, h * fy, s, s * 0.9, chim=(0.35 + 0.3 * (i % 2), ch), door=(i % 2 == 0))
    k.ground(0, w, h * 0.4, depth=h * 0.4, drifts=1, ticks=False)
    house(k, w * 0.08, h * 0.12, 62, 60, chim=(0.3, 18), pots=2)
    house(k, w * 0.62, h * 0.12, 56, 64, chim=(0.65, 9))
    k.pine(w * 0.47, h * 0.1, 52); k.pine(w * 0.54, h * 0.1, 40)
    k.ground(0, w, h * 0.12, depth=h * 0.12, drifts=2, ticks=False)
    k.footprints([(w * (0.36 + 0.04 * i), h * (0.04 + 0.01 * i)) for i in range(7)])


def v_pots(k, w, h):
    k.stars(4, h * 0.7, w - 4, h - 4, n=5)
    pots_row(k, w * 0.22, w * 0.78, h * 0.18, [2, 4, 1, 3, 5][:5], w=h * 0.13)


def v_cottage(k, w, h):
    k.ground(0, w, h * 0.12, depth=h * 0.12, drifts=0, ticks=False)
    house(k, w * 0.36, h * 0.12, h * 0.6, h * 0.5, chim=(0.3, h * 0.14), pots=2)
    k.pine(w * 0.2, h * 0.1, h * 0.6); k.pine(w * 0.82, h * 0.1, h * 0.45)


def v_sweep(k, w, h):
    k.ground(0, w, h * 0.12, depth=h * 0.12, drifts=0, ticks=False)
    ladder(k, w * 0.3, h * 0.12, h * 0.7, ang=82)
    brush(k, w * 0.5, h * 0.12, h * 0.7, ang=74)
    k.kettle(w * 0.78, h * 0.12, h * 0.3)


def v_lane(k, w, h):
    k.stars(4, h * 0.72, w - 4, h - 4, n=6)
    k.ground(0, w, h * 0.14, depth=h * 0.14, drifts=0, ticks=False)
    lane(k, w * 0.22, w * 0.86, h * 0.14, [1, 3, 2], h=h * 0.48, smoke=True)
    sign(k, w * 0.15, h * 0.12, h * 0.26, 2)


def v_mug(k, w, h):
    k.ground(0, w, h * 0.14, depth=h * 0.14, drifts=0, ticks=False)
    k.bench(w * 0.42, h * 0.14, h * 0.9); k.mug(w * 0.3, h * 0.14 + h * 0.9 * 0.27, h * 0.2)
    k.lamppost(w * 0.75, h * 0.12, h * 0.8)


def v_smoke(k, w, h):
    k.stars(4, h * 0.55, w - 4, h - 4, n=8); k.moon(w * 0.2, h * 0.76, h * 0.1)
    k.shape([(w * 0.25, h * 0.0), (w * 0.75, h * 0.0), (w * 0.62, h * 0.22), (w * 0.38, h * 0.22)], lw=0.8, fill=Wt, amp=0.1)
    stack(k, w * 0.44, h * 0.08, h * 0.16, h * 0.3, pots=2, sm=h * 0.4)
    k.blob([(w * 0.2, h * 0.0), (w * 0.5, h * 0.12), (w * 0.8, h * 0.0)], Wt)
    k.line([(w * 0.22, h * 0.0), (w * 0.5, h * 0.1), (w * 0.78, h * 0.0)], lw=0.6, amp=0.1)


def v_moon(k, w, h):
    k.stars(4, h * 0.4, w - 4, h - 4, n=12); k.moon(w * 0.66, h * 0.74, h * 0.13)
    k.ground(0, w, h * 0.2, depth=h * 0.2, drifts=0, ticks=False)
    house(k, w * 0.3, h * 0.2, h * 0.5, h * 0.42, chim=(0.65, h * 0.08), door=False)
    k.pine(w * 0.15, h * 0.18, h * 0.6); k.pine(w * 0.24, h * 0.18, h * 0.45); k.lamppost(w * 0.9, h * 0.18, h * 0.55)


def thanks(k, w, h):
    k.ground(0, w, h * 0.22, depth=h * 0.22, drifts=0, ticks=False)
    lane(k, w * 0.04, w * 0.56, h * 0.22, [2, 1, 3], h=h * 0.4)
    k.bench(w * 0.75, h * 0.22, 30); k.mug(w * 0.7, h * 0.22 + 30 * 0.27, 6)
    k.lamppost(w * 0.93, h * 0.22, h * 0.7)
    k.stars(w * 0.1, h * 0.8, w * 0.9, h - 3, n=8)


VIGNETTES = ["v_pots", "v_cottage", "v_sweep", "v_lane", "v_mug", "v_smoke"]
SPECS = {  # name: (width in, height in, function, seed)
    "frontispiece": (4.7, 7.0, frontispiece, 61),
    "title": (4.7, 2.5, title, 3),
    "opener-easy": (4.7, 2.4, op_village, 11), "opener-medium": (4.7, 2.4, op_lodge, 12),
    "opener-hard": (4.7, 2.4, op_station, 13), "opener-expert": (4.7, 2.4, op_hamlet, 14),
    "thanks": (3.4, 1.5, thanks, 21),
    "v_moon": (1.9, 0.85, v_moon, 79),
    **{n: (1.9, 0.85, globals()[n], 80 + i) for i, n in enumerate(VIGNETTES)},
}

if __name__ == "__main__":
    only = set(sys.argv[1:])
    os.makedirs(OUT, exist_ok=True)
    for name, (wi, hi, fn, seed) in SPECS.items():
        if only and name not in only: continue
        render(os.path.join(OUT, name + ".png"), wi, hi, fn, seed=seed); print("drew", name)
