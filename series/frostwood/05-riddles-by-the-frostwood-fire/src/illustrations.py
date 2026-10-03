"""B&W ink illustrations for Riddles by the Frostwood Fire -> ../illustrations/*.png
Run from src/: python3 illustrations.py
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inkart import render
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "illustrations")

def fireside_scene(k, w, h, base):
    k.snowfall(0, base, w, h, n=int(w * h / 1000))
    k.stars(6, base + (h - base) * 0.55, w - 6, h - 4, n=int(w / 10))
    k.moon(w * 0.82, h - (h - base) * 0.18, min(12, (h - base) * 0.11))
    k.mountains(0, w, base + (h - base) * 0.08, [(w * 0.15, base + (h - base) * 0.5), (w * 0.4, base + (h - base) * 0.72), (w * 0.7, base + (h - base) * 0.48), (w * 0.92, base + (h - base) * 0.6)])
    k.lodge(w * 0.32, base + (h - base) * 0.08, w * 0.36, (h - base) * 0.28)
    k.forest(0, w * 0.28, base + (h - base) * 0.05, (h - base) * 0.14, (h - base) * 0.28, int(w / 45))
    k.forest(w * 0.72, w, base + (h - base) * 0.05, (h - base) * 0.14, (h - base) * 0.28, int(w / 50))
    k.ground(0, w, base + (h - base) * 0.08, depth=(h - base) * 0.08 + base, drifts=4)
    k.campfire(w * 0.5, base - 2, min(22, (h - base) * 0.2))

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
    k.campfire(w * 0.48, h * 0.12, 36)
    k.stump(w * 0.28, h * 0.1, 20); k.lantern(w * 0.28, h * 0.1 + 12, 14)
    k.kettle(w * 0.64, h * 0.11, 11)
    k.mug(w * 0.72, h * 0.1, 10)
    k.firewood(w * 0.18, h * 0.08, 36)
    k.pine(w * 0.07, h * 0.02, 110); k.pine(w * 0.93, h * 0.02, 120)
    k.unclip()

def title(k, w, h):
    fireside_scene(k, w, h, h * 0.28)
    k.pine(w * 0.06, h * 0.04, 64); k.pine(w * 0.94, h * 0.04, 70)

def op_easy(k, w, h):
    base = h * 0.3
    k.snowfall(0, base, w, h, n=36); k.stars(6, h * 0.7, w - 6, h - 4, n=22)
    k.mountains(0, w, h * 0.42, [(w * 0.2, h * 0.72), (w * 0.5, h * 0.85), (w * 0.8, h * 0.7)])
    k.lodge(w * 0.34, h * 0.4, w * 0.32, h * 0.24)
    k.ground(0, w, h * 0.42, depth=h * 0.42, drifts=4)
    k.campfire(w * 0.5, h * 0.12, 22); k.mug(w * 0.62, h * 0.1, 9)

def op_medium(k, w, h):
    k.snowfall(0, 0, w, h, n=40); k.stars(6, h * 0.72, w - 6, h - 4, n=20); k.moon(w * 0.18, h * 0.84, 10)
    k.mountains(0, w, h * 0.4, [(w * 0.25, h * 0.78), (w * 0.55, h * 0.68), (w * 0.85, h * 0.76)])
    k.forest(0, w, h * 0.38, 22, 40, 18)
    k.ground(0, w, h * 0.38, depth=h * 0.38, drifts=3)
    k.signpost(w * 0.35, h * 0.12, 32, arrows=[("LODGE", 1), ("VILLAGE", -1)])
    k.lantern(w * 0.62, h * 0.14, 14)

def op_hard(k, w, h):
    k.snowfall(0, 0, w, h, n=45); k.stars(6, h * 0.8, w - 6, h - 4, n=16)
    k.lodge(w * 0.28, h * 0.36, w * 0.44, h * 0.28)
    k.ground(0, w, h * 0.38, depth=h * 0.38, drifts=4)
    k.piano = None
    k.campfire(w * 0.22, h * 0.1, 16); k.kettle(w * 0.7, h * 0.12, 12)
    k.rocking = None
    k.bench = None
    k.pine(w * 0.08, h * 0.05, 55); k.pine(w * 0.92, h * 0.05, 58)

def op_expert(k, w, h):
    k.snowfall(0, 0, w, h, n=40); k.stars(6, h * 0.55, w - 6, h - 4, n=36, big=0.22); k.moon(w * 0.84, h * 0.82, 12)
    k.mountains(0, w, h * 0.28, [(w * 0.2, h * 0.6), (w * 0.48, h * 0.78), (w * 0.78, h * 0.58)])
    k.lodge(w * 0.55, h * 0.42, w * 0.22, h * 0.1)
    k.ground(0, w, h * 0.3, depth=h * 0.3, drifts=2)
    k.campfire(w * 0.4, h * 0.12, 18); k.lantern(w * 0.55, h * 0.1, 12)
    k.pine(w * 0.08, h * 0.02, 58); k.pine(w * 0.92, h * 0.02, 62)

def v_fire(k, w, h):
    k.ground(0, w, h * 0.2, depth=h * 0.2, drifts=1, ticks=False)
    k.campfire(w * 0.48, h * 0.1, h * 0.45); k.mug(w * 0.7, h * 0.14, h * 0.2)
    k.pine(w * 0.12, h * 0.18, h * 0.65); k.pine(w * 0.88, h * 0.18, h * 0.55)

def v_lantern(k, w, h):
    k.ground(0, w, h * 0.2, depth=h * 0.2, drifts=1, ticks=False)
    k.stump(w * 0.4, h * 0.14, h * 0.45); k.lantern(w * 0.4, h * 0.14 + h * 0.25, h * 0.38)
    k.pine(w * 0.15, h * 0.18, h * 0.65, style="line"); k.pine(w * 0.85, h * 0.18, h * 0.6)

def v_kettle(k, w, h):
    k.ground(0, w, h * 0.2, depth=h * 0.2, drifts=1, ticks=False)
    k.campfire(w * 0.4, h * 0.1, h * 0.35); k.kettle(w * 0.62, h * 0.14, h * 0.18); k.mug(w * 0.22, h * 0.14, h * 0.18)
    k.pine(w * 0.1, h * 0.18, h * 0.55)

def v_sled(k, w, h):
    k.ground(0, w, h * 0.22, depth=h * 0.22, drifts=1, ticks=False)
    k.pine(w * 0.2, h * 0.2, h * 0.65); k.sled(w * 0.58, h * 0.12, h * 0.55)

def v_moon(k, w, h):
    k.stars(4, h * 0.4, w - 4, h - 4, n=10); k.moon(w * 0.72, h * 0.7, h * 0.14)
    k.ground(0, w, h * 0.2, depth=h * 0.2, drifts=1, ticks=False)
    k.lodge(w * 0.3, h * 0.22, w * 0.35, h * 0.28)

def v_sign(k, w, h):
    k.ground(0, w, h * 0.22, depth=h * 0.22, drifts=1, ticks=False)
    k.signpost(w * 0.45, h * 0.16, h * 0.55, arrows=[("FIRE", 1), ("", -1)])
    k.pine(w * 0.18, h * 0.18, h * 0.7)

def thanks(k, w, h):
    fireside_scene(k, w, h, h * 0.3)
    k.pine(w * 0.06, h * 0.04, 50); k.pine(w * 0.94, h * 0.04, 54)

VIGNETTES = ["v_fire", "v_lantern", "v_kettle", "v_sled", "v_moon", "v_sign"]
SPECS = {
    "frontispiece": (4.7, 7.0, frontispiece, 51),
    "title": (4.7, 2.6, title, 7),
    "opener-easy": (4.7, 2.4, op_easy, 21),
    "opener-medium": (4.7, 2.4, op_medium, 22),
    "opener-hard": (4.7, 2.4, op_hard, 23),
    "opener-expert": (4.7, 2.4, op_expert, 24),
    "thanks": (3.6, 1.7, thanks, 31),
    **{n: (1.9, 0.85, globals()[n], 60 + i) for i, n in enumerate(VIGNETTES)},
}

if __name__ == "__main__":
    only = set(sys.argv[1:])
    os.makedirs(OUT, exist_ok=True)
    for name, (wi, hi, fn, seed) in SPECS.items():
        if only and name not in only: continue
        render(os.path.join(OUT, name + ".png"), wi, hi, fn, seed=seed); print("drew", name)
