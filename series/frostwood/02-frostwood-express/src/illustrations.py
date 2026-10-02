"""Draws the black-and-white ink illustrations for Frostwood Express -> ../illustrations/*.png
(300 DPI grayscale, pure black line art on white). Deterministic: same seeds -> same images.
Run from src/: python3 illustrations.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inkart import render, Wt, K, lerp
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "illustrations")

def train(k, x, y, L, cars=2, facing=1):
    k.locomotive(x, y, L, facing=facing)
    cx = x - 3 * facing
    for i in range(cars):
        k.carriage(cx, y, L * 0.85, facing=-facing, n_win=4); cx -= (L * 0.85 + 3) * facing

def frontispiece(k, w, h):
    """The Frostwood Express crossing the Silverbrook Viaduct, the lodge high above."""
    m = 9; k.frame(m, m, w - m, h - m)
    k.clip_rect(m + 4, m + 4, w - m - 4, h - m - 4)
    k.snowfall(0, h * 0.3, w, h, n=100)
    k.stars(20, h * 0.72, w - 20, h - 20, n=40)
    k.moon(w * 0.2, h * 0.88, 18)
    k.mountains(0, w, h * 0.55, [(w * 0.62, h * 0.86), (w * 0.9, h * 0.76)])
    k.summit(w * 0.0, w * 0.55, h * 0.55, w * 0.18, w * 0.34, h * 0.75)
    k.lodge(w * 0.19, h * 0.75, w * 0.14, h * 0.045)
    k.forest(0, w, h * 0.53, 16, 30, 16)
    k.ground(0, w, h * 0.53, depth=h * 0.1, drifts=2)
    # valley with the viaduct
    deck = h * 0.42
    for side in (0, 1):   # the two banks of the gorge
        xa, xb = (0, w * 0.2) if side == 0 else (w, w * 0.8)
        bank = [(xa, deck - 3), (lerp(xa, xb, 0.4), deck - 6), (xb, h * 0.2), (xa, h * 0.2)]
        k.shape(bank, lw=0.9, fill=Wt, amp=0.3)
        k.hatch([(lerp(xa, xb, 0.45), deck - 8), (xb, h * 0.2), (lerp(xa, xb, 0.6), h * 0.2)], angle=-60 if side else 60, gap=1.9, lw=0.35)
        k.forest(min(xa, lerp(xa, xb, 0.3)), max(xa, lerp(xa, xb, 0.3)), deck - 4, 14, 22, 2)
    k.trestle(w * 0.16, w * 0.84, deck, h * 0.2, bents=5)
    k.rails(0, w, deck + 1, ties=False)
    train(k, w * 0.66, deck + 2, 52, cars=3)
    # frozen river
    k.line([(0, h * 0.2), (w, h * 0.2)], lw=0.8, amp=0.3)
    for i in range(5): k.line([(w * (0.1 + 0.18 * i), h * 0.17), (w * (0.18 + 0.18 * i), h * 0.17)], lw=0.4, amp=0)
    k.ground(0, w, h * 0.15, depth=h * 0.15, drifts=4)
    k.pine(w * 0.08, h * 0.02, 110); k.pine(w * 0.92, h * 0.03, 125); k.pine(w * 0.2, h * 0.04, 60, style="line")
    k.signal(w * 0.78, h * 0.12, 40)
    k.unclip()

def title(k, w, h):
    k.snowfall(w * 0.03, h * 0.35, w * 0.97, h, n=50); k.stars(8, h * 0.7, w - 8, h - 4, n=20)
    k.mountains(w * 0.02, w * 0.98, h * 0.35, [(w * 0.2, h * 0.68), (w * 0.5, h * 0.82), (w * 0.82, h * 0.66)])
    k.forest(w * 0.03, w * 0.97, h * 0.32, 18, 34, 16)
    k.ground(w * 0.02, w * 0.98, h * 0.32, depth=h * 0.32, drifts=3)
    k.rails(w * 0.03, w * 0.97, h * 0.18)
    train(k, w * 0.62, h * 0.18 + 1, 64, cars=2)
    k.pine(w * 0.07, h * 0.03, 70); k.pine(w * 0.93, h * 0.03, 76)

def op_foothills(k, w, h):
    k.snowfall(w * 0.03, h * 0.35, w * 0.97, h, n=40)
    k.mountains(w * 0.02, w * 0.98, h * 0.4, [(w * 0.3, h * 0.66), (w * 0.7, h * 0.72)])
    k.forest(w * 0.03, w * 0.4, h * 0.36, 16, 30, 6); k.forest(w * 0.75, w * 0.97, h * 0.36, 16, 30, 4)
    k.ground(w * 0.02, w * 0.98, h * 0.36, depth=h * 0.36, drifts=2)
    k.station(w * 0.44, h * 0.24, w * 0.26, h * 0.42, name="VALLEY")
    k.rails(w * 0.03, w * 0.97, h * 0.18)
    train(k, w * 0.36, h * 0.18 + 1, 56, cars=1)
    k.lamppost(w * 0.76, h * 0.2, 34); k.bench(w * 0.84, h * 0.2, 22)

def op_viaduct(k, w, h):
    k.snowfall(w * 0.03, h * 0.5, w * 0.97, h, n=40); k.stars(8, h * 0.75, w - 8, h - 4, n=16)
    k.mountains(w * 0.02, w * 0.98, h * 0.4, [(w * 0.18, h * 0.72), (w * 0.5, h * 0.62), (w * 0.84, h * 0.78)])
    deck = h * 0.5
    k.trestle(w * 0.04, w * 0.96, deck, h * 0.1, bents=6)
    k.rails(w * 0.02, w * 0.98, deck + 1, ties=False)
    train(k, w * 0.6, deck + 2, 48, cars=2)
    k.ground(w * 0.02, w * 0.98, h * 0.1, depth=h * 0.1, drifts=2)
    k.pine(w * 0.05, h * 0.06, 50); k.pine(w * 0.95, h * 0.06, 54)

def op_pass(k, w, h):
    k.snowfall(w * 0.03, h * 0.4, w * 0.97, h, n=40)
    k.mountains(w * 0.02, w * 0.98, h * 0.25, [(w * 0.25, h * 0.85), (w * 0.62, h * 0.95), (w * 0.88, h * 0.7)])
    k.tunnel(w * 0.68, h * 0.2, 46, 44)
    k.ground(w * 0.02, w * 0.98, h * 0.2, depth=h * 0.2, drifts=2)
    k.rails(w * 0.03, w * 0.6, h * 0.2)
    train(k, w * 0.41, h * 0.2 + 1, 54, cars=1)
    k.forest(w * 0.03, w * 0.16, h * 0.18, 30, 50, 2)

def op_summit(k, w, h):
    k.snowfall(w * 0.03, h * 0.4, w * 0.97, h, n=40); k.stars(8, h * 0.72, w - 8, h - 4, n=26); k.moon(w * 0.88, h * 0.84, 12)
    k.lodge(w * 0.5, h * 0.24, w * 0.36, h * 0.44)
    k.station(w * 0.12, h * 0.24, w * 0.26, h * 0.4, name="SUMMIT")
    k.ground(w * 0.02, w * 0.98, h * 0.24, depth=h * 0.24, drifts=2)
    k.rails(w * 0.03, w * 0.97, h * 0.12)
    train(k, w * 0.42, h * 0.12 + 1, 54, cars=1, facing=1)
    k.pine(w * 0.94, h * 0.05, 56)

def v_signal(k, w, h):
    k.ground(w * 0.04, w * 0.96, h * 0.22, depth=h * 0.22, drifts=0, ticks=False); k.rails(w * 0.06, w * 0.94, h * 0.2)
    k.signal(w * 0.6, h * 0.22, h * 0.7); k.pine(w * 0.2, h * 0.24, h * 0.64); k.pine(w * 0.84, h * 0.24, h * 0.56)

def v_engine(k, w, h):
    k.rails(w * 0.04, w * 0.96, h * 0.16); k.locomotive(w * 0.32, h * 0.16 + 1, h * 0.8, smoke=True)

def v_tower(k, w, h):
    k.ground(w * 0.04, w * 0.96, h * 0.2, depth=h * 0.2, drifts=0, ticks=False)
    k.water_tower(w * 0.42, h * 0.2, h * 0.72); k.pine(w * 0.16, h * 0.2, h * 0.6); k.pine(w * 0.78, h * 0.2, h * 0.68)

def v_platform(k, w, h):
    k.line([(w * 0.06, h * 0.18), (w * 0.94, h * 0.18)], lw=0.8, amp=0.3)
    k.lamppost(w * 0.3, h * 0.18, h * 0.72); k.bench(w * 0.52, h * 0.18, h * 0.5); k.mug(w * 0.7, h * 0.18, h * 0.18)

def v_tunnel(k, w, h):
    k.tunnel(w * 0.5, h * 0.18, h * 0.42, h * 0.4); k.rails(w * 0.06, w * 0.94, h * 0.18)
    k.pine(w * 0.12, h * 0.18, h * 0.5); k.pine(w * 0.88, h * 0.18, h * 0.56)

def v_carriage(k, w, h):
    k.rails(w * 0.04, w * 0.96, h * 0.16); k.carriage(w * 0.12, h * 0.16 + 1, h * 0.95, facing=1, n_win=4)
    k.stars(w * 0.6, h * 0.5, w * 0.95, h * 0.95, n=8)

def thanks(k, w, h):
    k.snowfall(w * 0.03, h * 0.35, w * 0.97, h, n=24)
    k.station(w * 0.15, h * 0.2, w * 0.3, h * 0.5, name="SUMMIT")
    k.ground(w * 0.03, w * 0.97, h * 0.2, depth=h * 0.2, drifts=1)
    k.rails(w * 0.04, w * 0.96, h * 0.12); train(k, w * 0.72, h * 0.12 + 1, 40, cars=1)

VIGNETTES = ["v_signal", "v_engine", "v_tower", "v_platform", "v_tunnel", "v_carriage"]
SPECS = {
    "frontispiece": (4.7, 7.0, frontispiece, 27),
    "title": (4.7, 2.6, title, 3),
    "opener-easy": (4.7, 2.4, op_foothills, 11), "opener-medium": (4.7, 2.4, op_viaduct, 12),
    "opener-hard": (4.7, 2.4, op_pass, 13), "opener-expert": (4.7, 2.4, op_summit, 14),
    "thanks": (3.6, 1.6, thanks, 21),
    **{n: (1.9, 0.85, globals()[n], 80 + i) for i, n in enumerate(VIGNETTES)},
}

if __name__ == "__main__":
    only = set(sys.argv[1:])
    for name, (wi, hi, fn, seed) in SPECS.items():
        if only and name not in only: continue
        render(os.path.join(OUT, name + ".png"), wi, hi, fn, seed=seed); print("drew", name)
