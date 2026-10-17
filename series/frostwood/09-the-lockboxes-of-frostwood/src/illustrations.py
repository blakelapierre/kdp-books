"""B&W ink illustrations for The Lockboxes of Frostwood -> ../illustrations/*.png
Uses the shared house-style inkart.py unchanged; the lockbox and padlock are drawn here
from inkart primitives. Run from src/: python3 illustrations.py
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inkart import render, K, Wt
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "illustrations")

def padlock(k, x, y, w):
    """Small padlock, (x, y) = bottom centre."""
    h = w * 0.8
    k.c.setStrokeColor(K); k.c.setLineWidth(max(1.0, w * 0.13)); k.c.setFillColor(Wt)
    k.c.arc(x - w * 0.3, y + h * 0.55, x + w * 0.3, y + h * 1.45, 0, 180)
    k.c.line(x - w * 0.3, y + h * 0.75, x - w * 0.3, y + h); k.c.line(x + w * 0.3, y + h * 0.75, x + w * 0.3, y + h)
    k.rect(x - w / 2, y, w, h, lw=0.9)
    k.hatch([(x + w * 0.2, y), (x + w / 2, y), (x + w / 2, y + h), (x + w * 0.2, y + h)], angle=90, gap=1.2, lw=0.35)
    k.circle(x, y + h * 0.55, w * 0.09, lw=0.6, fill=K)
    k.line([(x, y + h * 0.5), (x, y + h * 0.25)], lw=max(0.8, w * 0.08), amp=0)

def lockbox(k, x, y, w, digits=3):
    """Brass-cornered lockbox with a dial window, (x, y) = bottom centre."""
    h = w * 0.55
    k.rect(x - w / 2, y, w, h, lw=1.0)
    lid = [(x - w * 0.52, y + h), (x + w * 0.52, y + h), (x + w * 0.48, y + h * 1.32), (x - w * 0.48, y + h * 1.32)]
    k.shape(lid, lw=1.0, fill=Wt, amp=0.1)
    k.hatch(lid, angle=-35, gap=1.6, lw=0.35)
    k.hatch([(x + w * 0.34, y), (x + w / 2, y), (x + w / 2, y + h), (x + w * 0.34, y + h)], angle=90, gap=1.3, lw=0.35)
    for cx in (x - w / 2, x + w / 2):
        for cy in (y, y + h):
            k.blob([(cx - w * 0.05, cy - w * 0.05), (cx + w * 0.05, cy - w * 0.05), (cx + w * 0.05, cy + w * 0.05), (cx - w * 0.05, cy + w * 0.05)], K)
    # dial window
    dw = w * 0.13
    x0 = x - dw * digits / 2
    k.rect(x0 - 2, y + h * 0.42, dw * digits + 4, h * 0.36, lw=0.9)
    for i in range(digits):
        k.rect(x0 + i * dw + 0.6, y + h * 0.46, dw - 1.2, h * 0.28, lw=0.6)
        k.line([(x0 + i * dw + dw * 0.3, y + h * 0.6), (x0 + i * dw + dw * 0.7, y + h * 0.6)], lw=0.5, amp=0)
    k.line([(x - w * 0.36, y + h * 0.15), (x + w * 0.3, y + h * 0.15)], lw=0.4, amp=0.2)

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
    k.snowfall(0, 0, w, h, n=100)
    k.stars(20, h * 0.62, w - 20, h - 20, n=60, big=0.18, rmax=3.4)
    k.moon(w * 0.78, h * 0.86, 20)
    k.mountains(0, w, h * 0.4, [(w * 0.12, h * 0.58), (w * 0.38, h * 0.72), (w * 0.65, h * 0.55), (w * 0.9, h * 0.66)])
    k.lodge(w * 0.3, h * 0.38, w * 0.4, h * 0.18)
    k.forest(0, w * 0.28, h * 0.38, 18, 34, 8)
    k.forest(w * 0.72, w, h * 0.38, 18, 32, 6)
    k.ground(0, w, h * 0.4, depth=h * 0.12, drifts=3)
    k.ground(0, w, h * 0.22, depth=h * 0.22, drifts=5)
    lockbox(k, w * 0.45, h * 0.09, 92)
    k.lantern(w * 0.22, h * 0.09, 30)
    k.key(w * 0.66, h * 0.1, 40, tag="No.1")
    k.mug(w * 0.31, h * 0.08, 16)
    k.pine(w * 0.07, h * 0.02, 110); k.pine(w * 0.93, h * 0.02, 120)
    k.unclip()

def title(k, w, h):
    lodge_scene(k, w, h, h * 0.3)
    lockbox(k, w * 0.5, h * 0.06, 70)
    k.pine(w * 0.06, h * 0.04, 64); k.pine(w * 0.94, h * 0.04, 70)

def op_lodge(k, w, h):
    k.snowfall(0, h * 0.3, w, h, n=36); k.stars(6, h * 0.7, w - 6, h - 4, n=22)
    k.mountains(0, w, h * 0.42, [(w * 0.2, h * 0.72), (w * 0.5, h * 0.85), (w * 0.8, h * 0.7)])
    k.lodge(w * 0.34, h * 0.4, w * 0.32, h * 0.24)
    k.ground(0, w, h * 0.42, depth=h * 0.42, drifts=4)
    lockbox(k, w * 0.5, h * 0.08, 64); k.lantern(w * 0.3, h * 0.08, 22); k.mug(w * 0.68, h * 0.08, 12)
    k.pine(w * 0.08, h * 0.05, 60); k.pine(w * 0.92, h * 0.05, 64)

def op_village(k, w, h):
    k.snowfall(0, 0, w, h, n=40); k.stars(6, h * 0.74, w - 6, h - 4, n=20); k.moon(w * 0.85, h * 0.85, 10)
    k.mountains(0, w, h * 0.45, [(w * 0.25, h * 0.75), (w * 0.55, h * 0.68), (w * 0.85, h * 0.76)])
    k.cottage(w * 0.06, h * 0.32, w * 0.2, h * 0.3)
    k.cottage(w * 0.72, h * 0.32, w * 0.2, h * 0.32)
    k.bandstand(w * 0.48, h * 0.32, w * 0.2)
    k.ground(0, w, h * 0.32, depth=h * 0.32, drifts=3)
    k.lamppost(w * 0.3, h * 0.06, 60); lockbox(k, w * 0.56, h * 0.06, 54, digits=3)

def op_railway(k, w, h):
    k.snowfall(0, 0, w, h, n=40); k.stars(6, h * 0.78, w - 6, h - 4, n=16)
    k.mountains(0, w, h * 0.42, [(w * 0.2, h * 0.7), (w * 0.5, h * 0.82), (w * 0.82, h * 0.68)])
    k.forest(0, w, h * 0.4, 18, 34, 16)
    k.ground(0, w, h * 0.4, depth=h * 0.4, drifts=3)
    k.station(w * 0.06, h * 0.26, w * 0.3, h * 0.3, name="FROSTWOOD")
    k.rails(0, w, h * 0.24)
    k.locomotive(w * 0.5, h * 0.24, w * 0.3, facing=1)
    lockbox(k, w * 0.22, h * 0.03, 48, digits=4)

def op_mountain(k, w, h):
    k.snowfall(0, 0, w, h, n=40); k.stars(6, h * 0.55, w - 6, h - 4, n=36, big=0.22); k.moon(w * 0.84, h * 0.82, 12)
    k.mountains(0, w, h * 0.28, [(w * 0.2, h * 0.6), (w * 0.48, h * 0.8), (w * 0.78, h * 0.58)])
    k.cabin(w * 0.56, h * 0.28, w * 0.18, h * 0.22)
    k.ground(0, w, h * 0.3, depth=h * 0.3, drifts=2)
    lockbox(k, w * 0.36, h * 0.06, 52, digits=5); k.lantern(w * 0.52, h * 0.06, 20)
    k.pine(w * 0.08, h * 0.02, 58); k.pine(w * 0.92, h * 0.02, 62)

def _g(k, w, h):
    k.ground(0, w, h * 0.2, depth=h * 0.2, drifts=1, ticks=False)

def v_key(k, w, h):
    _g(k, w, h); k.key(w * 0.32, h * 0.45, w * 0.4, tag="BOX"); k.pine(w * 0.88, h * 0.18, h * 0.6)

def v_lockbox(k, w, h):
    _g(k, w, h); lockbox(k, w * 0.5, h * 0.18, h * 1.0); k.pine(w * 0.12, h * 0.18, h * 0.6)

def v_padlock(k, w, h):
    _g(k, w, h); padlock(k, w * 0.5, h * 0.2, h * 0.38); k.pine(w * 0.16, h * 0.18, h * 0.6, style="line"); k.pine(w * 0.84, h * 0.18, h * 0.55)

def v_tin(k, w, h):
    _g(k, w, h); k.tin(w * 0.42, h * 0.18, h * 0.42); k.mug(w * 0.62, h * 0.18, h * 0.24); k.pine(w * 0.12, h * 0.18, h * 0.6)

def v_lantern(k, w, h):
    _g(k, w, h); k.stump(w * 0.4, h * 0.14, h * 0.45); k.lantern(w * 0.4, h * 0.14 + h * 0.25, h * 0.38)
    k.pine(w * 0.15, h * 0.18, h * 0.65, style="line"); k.pine(w * 0.85, h * 0.18, h * 0.6)

def v_sign(k, w, h):
    _g(k, w, h); k.signpost(w * 0.45, h * 0.16, h * 0.55, arrows=[("LODGE", 1), ("", -1)]); k.pine(w * 0.18, h * 0.18, h * 0.7)

def thanks(k, w, h):
    lodge_scene(k, w, h, h * 0.3)
    padlock(k, w * 0.5, h * 0.06, 26)
    k.pine(w * 0.06, h * 0.04, 50); k.pine(w * 0.94, h * 0.04, 54)

VIGNETTES = ["v_key", "v_lockbox", "v_padlock", "v_tin", "v_lantern", "v_sign"]
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
