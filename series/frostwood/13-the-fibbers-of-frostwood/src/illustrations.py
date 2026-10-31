"""B&W ink illustrations for The Fibbers of Frostwood -> ../illustrations/*.png
Uses the shared house-style inkart.py unchanged; the pinecones and game tin are drawn here
from inkart primitives. Run from src/: python3 illustrations.py
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inkart import render, K, Wt
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "illustrations")

def pinecone(k, x, y, h, snowy=True, angle=0):
    """Pinecone, (x, y) = bottom tip. Egg-shaped body covered in scalloped scales, stem on top.
    snowy=True: white, snow-tipped scales (the truth-teller cone); snowy=False: solid black
    with white scale lines (the fibber cone)."""
    w = h * 0.62
    ink, paper = (Wt, K) if snowy else (K, Wt)
    k.c.saveState()
    k.c.translate(x, y); k.c.rotate(angle)
    # body outline: egg, narrow at the bottom tip, broadest high up
    pts = []
    for i in range(41):
        t = i / 40 * 2 * math.pi
        yy = h * 0.45 - math.cos(t) * h * 0.43
        r = math.sin(t) * w / 2 * (0.55 + 0.45 * ((yy / h) ** 0.6))
        pts.append((r, yy))
    k.shape(pts, lw=0.9, fill=ink, amp=0.08)
    # scallop rows of scales
    rows = 7
    for r in range(rows):
        yy = h * (0.12 + 0.11 * r)
        half = w / 2 * (0.55 + 0.45 * ((yy / h) ** 0.6)) * math.sin(math.acos(max(-1, min(1, (h * 0.45 - yy) / (h * 0.43)))))
        n = max(2, int(half * 2 / (w * 0.22)))
        sw = half * 2 / n
        off = (sw / 2) if r % 2 else 0
        for j in range(n + (1 if r % 2 else 0)):
            cx = -half + sw / 2 + j * sw - off
            if abs(cx) > half - sw * 0.25:
                continue
            arc = [(cx + sw * 0.5 * math.cos(u), yy - sw * 0.45 * math.sin(u)) for u in [math.pi * q / 8 for q in range(9)]]
            k.line(arc, lw=0.55, amp=0.03, color=paper)
            if snowy and r >= 3:
                k.blob([(cx - sw * 0.28, yy + sw * 0.02), (cx, yy + sw * 0.22), (cx + sw * 0.28, yy + sw * 0.02), (cx, yy - sw * 0.05)], Wt)
    # stem
    k.line([(0, h * 0.88), (h * 0.03, h * 1.0)], lw=max(0.9, h * 0.05), amp=0)
    if snowy:  # snow cap
        cap = [(-w * 0.28, h * 0.8), (-w * 0.12, h * 0.89), (w * 0.1, h * 0.9), (w * 0.28, h * 0.8), (w * 0.12, h * 0.83), (-w * 0.1, h * 0.82)]
        k.shape(cap, lw=0.7, fill=Wt, amp=0.05)
    k.c.restoreState()

def cone_tin(k, x, y, w):
    """The lodge's game tin with two pinecones peeking out, (x, y) = bottom centre."""
    pinecone(k, x - w * 0.17, y + w * 0.74, w * 0.7, snowy=True, angle=14)
    pinecone(k, x + w * 0.15, y + w * 0.76, w * 0.7, snowy=False, angle=-12)
    k.tin(x, y, w, label="GAME")

def pair(k, x, y, h):
    pinecone(k, x - h * 0.38, y, h, snowy=True)
    pinecone(k, x + h * 0.38, y, h, snowy=False)

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
    cone_tin(k, w * 0.47, h * 0.09, 70); pinecone(k, w * 0.58, h * 0.085, 30, snowy=False, angle=70)
    k.lantern(w * 0.22, h * 0.09, 30)
    pinecone(k, w * 0.7, h * 0.09, 34, snowy=True)
    k.mug(w * 0.31, h * 0.08, 16)
    k.pine(w * 0.07, h * 0.02, 110); k.pine(w * 0.93, h * 0.02, 120)
    k.unclip()

def title(k, w, h):
    lodge_scene(k, w, h, h * 0.3)
    pair(k, w * 0.5, h * 0.06, 46)
    k.pine(w * 0.06, h * 0.04, 64); k.pine(w * 0.94, h * 0.04, 70)

def op_lodge(k, w, h):
    k.snowfall(0, h * 0.3, w, h, n=36); k.stars(6, h * 0.7, w - 6, h - 4, n=22)
    k.mountains(0, w, h * 0.42, [(w * 0.2, h * 0.72), (w * 0.5, h * 0.85), (w * 0.8, h * 0.7)])
    k.lodge(w * 0.34, h * 0.4, w * 0.32, h * 0.24)
    k.ground(0, w, h * 0.42, depth=h * 0.42, drifts=4)
    cone_tin(k, w * 0.5, h * 0.08, 50); k.lantern(w * 0.3, h * 0.08, 22); k.mug(w * 0.68, h * 0.08, 12)
    k.pine(w * 0.08, h * 0.05, 60); k.pine(w * 0.92, h * 0.05, 64)

def op_village(k, w, h):
    k.snowfall(0, 0, w, h, n=40); k.stars(6, h * 0.74, w - 6, h - 4, n=20); k.moon(w * 0.85, h * 0.85, 10)
    k.mountains(0, w, h * 0.45, [(w * 0.25, h * 0.75), (w * 0.55, h * 0.68), (w * 0.85, h * 0.76)])
    k.cottage(w * 0.06, h * 0.32, w * 0.2, h * 0.3)
    k.cottage(w * 0.72, h * 0.32, w * 0.2, h * 0.32)
    k.bandstand(w * 0.48, h * 0.32, w * 0.2)
    k.ground(0, w, h * 0.32, depth=h * 0.32, drifts=3)
    k.lamppost(w * 0.3, h * 0.06, 60); k.bench(w * 0.6, h * 0.06, 70); pair(k, w * 0.6, h * 0.06 + 70 * 0.39, 22)

def op_railway(k, w, h):
    k.snowfall(0, 0, w, h, n=40); k.stars(6, h * 0.78, w - 6, h - 4, n=16)
    k.mountains(0, w, h * 0.42, [(w * 0.2, h * 0.7), (w * 0.5, h * 0.82), (w * 0.82, h * 0.68)])
    k.forest(0, w, h * 0.4, 18, 34, 16)
    k.ground(0, w, h * 0.4, depth=h * 0.4, drifts=3)
    k.station(w * 0.06, h * 0.26, w * 0.3, h * 0.3, name="FROSTWOOD")
    k.rails(0, w, h * 0.24)
    k.locomotive(w * 0.5, h * 0.24, w * 0.3, facing=1)
    cone_tin(k, w * 0.2, h * 0.03, 40)

def op_mountain(k, w, h):
    k.snowfall(0, 0, w, h, n=40); k.stars(6, h * 0.55, w - 6, h - 4, n=36, big=0.22); k.moon(w * 0.84, h * 0.82, 12)
    k.mountains(0, w, h * 0.28, [(w * 0.2, h * 0.6), (w * 0.48, h * 0.8), (w * 0.78, h * 0.58)])
    k.cabin(w * 0.56, h * 0.28, w * 0.18, h * 0.22)
    k.ground(0, w, h * 0.3, depth=h * 0.3, drifts=2)
    pair(k, w * 0.36, h * 0.06, 34); k.lantern(w * 0.52, h * 0.06, 20)
    k.pine(w * 0.08, h * 0.02, 58); k.pine(w * 0.92, h * 0.02, 62)

def _g(k, w, h):
    k.ground(0, w, h * 0.2, depth=h * 0.2, drifts=1, ticks=False)

def v_pair(k, w, h):
    _g(k, w, h); pair(k, w * 0.5, h * 0.18, h * 0.55); k.pine(w * 0.12, h * 0.18, h * 0.6)

def v_tin(k, w, h):
    _g(k, w, h); cone_tin(k, w * 0.45, h * 0.18, h * 0.4); k.mug(w * 0.66, h * 0.18, h * 0.24); k.pine(w * 0.12, h * 0.18, h * 0.6)

def v_bench(k, w, h):
    _g(k, w, h); k.bench(w * 0.5, h * 0.18, h * 0.9); pinecone(k, w * 0.44, h * 0.18 + h * 0.35, h * 0.26, snowy=True); pinecone(k, w * 0.58, h * 0.18 + h * 0.35, h * 0.26, snowy=False)
    k.pine(w * 0.12, h * 0.18, h * 0.6, style="line"); k.pine(w * 0.88, h * 0.18, h * 0.55)

def v_mug(k, w, h):
    _g(k, w, h); k.mug(w * 0.42, h * 0.18, h * 0.32); pinecone(k, w * 0.58, h * 0.18, h * 0.32, snowy=True); k.pine(w * 0.86, h * 0.18, h * 0.6)

def v_lantern(k, w, h):
    _g(k, w, h); k.stump(w * 0.4, h * 0.14, h * 0.45); k.lantern(w * 0.4, h * 0.14 + h * 0.25, h * 0.38)
    pinecone(k, w * 0.58, h * 0.18, h * 0.26, snowy=False)
    k.pine(w * 0.15, h * 0.18, h * 0.65, style="line"); k.pine(w * 0.85, h * 0.18, h * 0.6)

def v_sign(k, w, h):
    _g(k, w, h); k.signpost(w * 0.45, h * 0.16, h * 0.55, arrows=[("LODGE", 1), ("", -1)]); k.pine(w * 0.18, h * 0.18, h * 0.7)

def thanks(k, w, h):
    lodge_scene(k, w, h, h * 0.3)
    pair(k, w * 0.5, h * 0.06, 24)
    k.pine(w * 0.06, h * 0.04, 50); k.pine(w * 0.94, h * 0.04, 54)

VIGNETTES = ["v_pair", "v_tin", "v_bench", "v_mug", "v_lantern", "v_sign"]
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
