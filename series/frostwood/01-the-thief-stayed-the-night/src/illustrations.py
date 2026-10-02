"""Draws the black-and-white ink illustrations for The Thief Stayed the Night -> ../illustrations/*.png
(300 DPI grayscale, pure black line art on white). Deterministic: same seeds -> same images.
Each case gets a small vignette of the thing that went missing (never of a suspect, so nothing is given away).
Run from src/: python3 illustrations.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inkart import render, Wt, K, lerp
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "illustrations")

def frontispiece(k, w, h):
    """The Frostwood Lodge, snowed in: drifts to the windowsills, the road buried, smoke from every chimney."""
    m = 9; k.frame(m, m, w - m, h - m)
    k.clip_rect(m + 4, m + 4, w - m - 4, h - m - 4)
    k.snowfall(0, 0, w, h, n=240, rmax=1.6)
    k.mountains(0, w, h * 0.52, [(w * 0.18, h * 0.78), (w * 0.52, h * 0.9), (w * 0.85, h * 0.76)])
    k.forest(0, w * 0.2, h * 0.5, 20, 40, 5); k.forest(w * 0.8, w, h * 0.5, 20, 40, 5)
    k.lodge(w * 0.12, h * 0.34, w * 0.76, h * 0.26)
    k.ground(0, w, h * 0.36, depth=h * 0.36, drifts=8)
    # drifts against the walls
    for (u, r) in [(0.2, 40), (0.45, 30), (0.7, 44)]:
        k.blob(k.arcpts(w * u, h * 0.335, r, 9, 0, 180, 20), Wt); k.line(k.arcpts(w * u, h * 0.335, r, 9, 10, 170, 20), lw=0.7, amp=0.2)
    k.lamppost(w * 0.38, h * 0.22, 46); k.lamppost(w * 0.66, h * 0.22, 46)
    k.signpost(w * 0.3, h * 0.07, 46, arrows=[("LODGE", 1), ("VILLAGE", -1)])
    # the buried road: a sledge track through the drifts
    k.c.setDash(3, 3); k.line([(w * 0.5 + 18 * math.sin(t * 4), h * (0.33 - 0.3 * t)) for t in [i / 30 for i in range(31)]], lw=0.6, amp=0); k.c.setDash()
    k.sled(w * 0.58, h * 0.1, 40)
    k.pine(w * 0.07, h * 0.02, 120); k.pine(w * 0.94, h * 0.02, 135)
    k.unclip()

def title(k, w, h):
    k.snowfall(w * 0.03, h * 0.2, w * 0.97, h, n=70)
    k.mountains(w * 0.02, w * 0.98, h * 0.3, [(w * 0.2, h * 0.62), (w * 0.5, h * 0.8), (w * 0.82, h * 0.6)])
    k.forest(w * 0.03, w * 0.22, h * 0.26, 18, 32, 4); k.forest(w * 0.78, w * 0.97, h * 0.26, 18, 32, 4)
    k.lodge(w * 0.22, h * 0.16, w * 0.56, h * 0.46)
    k.ground(w * 0.02, w * 0.98, h * 0.16, depth=h * 0.16, drifts=3)
    k.pine(w * 0.08, h * 0.02, 70); k.pine(w * 0.92, h * 0.02, 76)

def table_line(k, w, h, y=0.14):
    k.line([(w * 0.08, h * y), (w * 0.92, h * y)], lw=0.8, amp=0.3)

def flakes(k, w, h, n=5):
    for i in range(n): k.flake(w * k.r.uniform(0.06, 0.94), h * k.r.uniform(0.65, 0.93), k.r.uniform(2, 3.4), lw=0.45)

CASE_ART = {
    1: lambda k, w, h: (flakes(k, w, h), table_line(k, w, h), k.tin(w * 0.42, h * 0.14, h * 0.55), k.cup(w * 0.66, h * 0.15, h * 0.3)),
    2: lambda k, w, h: (flakes(k, w, h), k.ground(w * 0.1, w * 0.9, h * 0.14, depth=h * 0.14, drifts=0, ticks=False), k.snowman(w * 0.5, h * 0.12, h * 0.78, hat=False),
                        k.pine(w * 0.2, h * 0.12, h * 0.55), k.pine(w * 0.8, h * 0.12, h * 0.6)),
    3: lambda k, w, h: (table_line(k, w, h), k.gem(w * 0.5, h * 0.14, h * 0.5)),
    4: lambda k, w, h: (flakes(k, w, h), table_line(k, w, h), k.cake(w * 0.42, h * 0.15, h * 0.62), k.cup(w * 0.7, h * 0.15, h * 0.28)),
    5: lambda k, w, h: (flakes(k, w, h), table_line(k, w, h), k.book(w * 0.5, h * 0.15, h * 0.85, open_=True)),
    6: lambda k, w, h: (flakes(k, w, h), k.ground(w * 0.1, w * 0.9, h * 0.12, depth=h * 0.12, drifts=0, ticks=False), k.skate(w * 0.38, h * 0.12, h * 0.6), k.skate(w * 0.62, h * 0.12, h * 0.6, facing=-1)),
    7: lambda k, w, h: (table_line(k, w, h), k.teapot(w * 0.36, h * 0.14, h * 0.62), k.cake(w * 0.66, h * 0.15, h * 0.42), k.candle(w * 0.86, h * 0.14, h * 0.5)),
    8: lambda k, w, h: (table_line(k, w, h), k.snowglobe(w * 0.5, h * 0.14, h * 0.66)),
    9: lambda k, w, h: (k.stairs(w * 0.3, h * 0.1, w * 0.4, h * 0.6, steps=8), k.candle(w * 0.2, h * 0.1, h * 0.4), k.line([(w * 0.08, h * 0.1), (w * 0.92, h * 0.1)], lw=0.8, amp=0.3)),
    10: lambda k, w, h: (flakes(k, w, h), table_line(k, w, h), k.violin(w * 0.44, h * 0.16, h * 0.82), k.book(w * 0.7, h * 0.15, h * 0.42)),
    11: lambda k, w, h: (table_line(k, w, h), k.key(w * 0.36, h * 0.55, h * 0.8, tag="MASTER"), k.desk_bell(w * 0.75, h * 0.15, h * 0.4)),
    12: lambda k, w, h: (k.line([(w * 0.1, h * 0.06), (w * 0.9, h * 0.06)], lw=0.6, amp=0.3), k.portrait(w * 0.5, h * 0.08, h * 0.62)),
}

def prologue(k, w, h):
    k.snowfall(w * 0.05, h * 0.3, w * 0.95, h, n=30)
    k.ground(w * 0.04, w * 0.96, h * 0.2, depth=h * 0.2, drifts=1, ticks=False)
    k.lodge(w * 0.3, h * 0.18, w * 0.4, h * 0.5); k.pine(w * 0.16, h * 0.16, h * 0.6); k.pine(w * 0.84, h * 0.16, h * 0.66)

def epilogue(k, w, h):
    table_line(k, w, h)
    k.desk_bell(w * 0.3, h * 0.15, h * 0.4); k.key(w * 0.48, h * 0.32, h * 0.5, tag="314"); k.teapot(w * 0.76, h * 0.15, h * 0.5)

def thanks(k, w, h):
    k.snowfall(w * 0.05, h * 0.3, w * 0.95, h, n=40); k.stars(w * 0.06, h * 0.7, w * 0.94, h - 4, n=14)
    k.mountains(w * 0.03, w * 0.97, h * 0.3, [(w * 0.3, h * 0.66), (w * 0.72, h * 0.74)])
    k.lodge(w * 0.3, h * 0.2, w * 0.4, h * 0.44)
    k.forest(w * 0.04, w * 0.28, h * 0.2, 18, 30, 4); k.forest(w * 0.72, w * 0.96, h * 0.2, 18, 30, 4)
    k.ground(w * 0.03, w * 0.97, h * 0.2, depth=h * 0.2, drifts=2)

def v_blank(k, w, h):
    table_line(k, w, h, 0.18); k.key(w * 0.3, h * 0.45, h * 0.62, tag="101"); k.cup(w * 0.72, h * 0.19, h * 0.3)

VIGNETTES = ["v_blank"]
SPECS = {
    "frontispiece": (4.7, 7.0, frontispiece, 37),
    "title": (4.7, 2.9, title, 3),
    "prologue": (3.2, 1.4, prologue, 5),
    "epilogue": (2.6, 1.0, epilogue, 6),
    "thanks": (3.6, 1.8, thanks, 21),
    "v_blank": (1.9, 0.85, v_blank, 9),
    **{f"case-{n:02d}": (3.0, 1.45, CASE_ART[n], 200 + n) for n in range(1, 13)},
}

if __name__ == "__main__":
    only = set(sys.argv[1:])
    for name, (wi, hi, fn, seed) in SPECS.items():
        if only and name not in only: continue
        render(os.path.join(OUT, name + ".png"), wi, hi, fn, seed=seed); print("drew", name)
