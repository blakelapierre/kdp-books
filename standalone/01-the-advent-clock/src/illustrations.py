"""Draws the black-and-white ink illustrations for The Advent Clock -> ../illustrations/*.png
(300 DPI grayscale, pure black line art on white). Deterministic: same seeds -> same images.
Spoiler care: nothing before the Midnight page shows the star, the clock tower, a candle or a bell
(two of the doors are picture puzzles of a candle and a bell). Run from src/: python3 illustrations.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inkart import render, Wt, K, lerp
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "illustrations")

def frontispiece(k, w, h):
    """The lobby of Snowberry Lodge: the Great Advent Clock between the fireplace and the stairs."""
    m = 9; k.frame(m, m, w - m, h - m)
    k.clip_rect(m + 4, m + 4, w - m - 4, h - m - 4)
    floor = h * 0.2
    # back wall: timber boards
    k.hatch([(0, floor), (w, floor), (w, h), (0, h)], angle=90, gap=9, lw=0.35, jitter=0.6)
    k.line([(0, h * 0.62), (w, h * 0.62)], lw=0.6, amp=0); k.line([(0, h * 0.625), (w, h * 0.625)], lw=0.35, amp=0)
    k.window_snow(w * 0.62, h * 0.66, w * 0.26, h * 0.2)
    k.garland(w * 0.06, w * 0.56, h * 0.92, sag=10, swags=3)
    # floor
    k.rect(0, 0, w, floor, lw=0.9)
    for i in range(9):
        k.line([(w * 0.5 + (i - 4) * w * 0.05, floor), (w * 0.5 + (i - 4) * w * 0.22, 0)], lw=0.4, amp=0)
    k.rug(w * 0.38, floor * 0.5, w * 0.62, floor * 0.6)
    # fireplace (left), clock (centre), tree (right), stairs (far right)
    k.fireplace(w * 0.05, floor + 2, w * 0.32, h * 0.26, stockings=3)
    k.mug(w * 0.12, floor + h * 0.26 + h * 0.018 + 2, 10, steam=True)
    k.books(w * 0.27, floor + h * 0.26 + h * 0.018 + 2, 26, n=2)
    k.grandfather_clock(w * 0.5, floor - 6, w * 0.22, h * 0.6)
    k.stairs(w * 0.86, floor, w * 0.2, h * 0.3, steps=8, side=1)
    k.xmas_tree(w * 0.76, floor - 8, h * 0.42, star=False)
    k.cat(w * 0.27, floor * 0.42, 30)
    k.unclip()

def title(k, w, h):
    k.snowfall(w * 0.05, h * 0.15, w * 0.95, h, n=60)
    k.ground(w * 0.04, w * 0.96, h * 0.12, depth=h * 0.12, drifts=2, ticks=False)
    k.grandfather_clock(w * 0.5, h * 0.1, w * 0.26, h * 0.86)
    for (u, hh) in [(0.14, 0.62), (0.25, 0.42), (0.86, 0.6), (0.75, 0.44)]:
        k.pine(w * u, h * 0.1, h * hh)

def prologue(k, w, h):
    """Snowberry Lodge in the snow (no tower)."""
    k.snowfall(0, h * 0.25, w, h, n=40)
    k.mountains(w * 0.02, w * 0.98, h * 0.3, [(w * 0.25, h * 0.75), (w * 0.72, h * 0.85)])
    k.forest(w * 0.02, w * 0.3, h * 0.25, 18, 30, 5); k.forest(w * 0.7, w * 0.98, h * 0.25, 18, 30, 5)
    k.lodge(w * 0.3, h * 0.22, w * 0.4, h * 0.48)
    k.ground(w * 0.02, w * 0.98, h * 0.22, depth=h * 0.22, drifts=3)
    k.pine(w * 0.08, h * 0.04, h * 0.6); k.pine(w * 0.92, h * 0.04, h * 0.66)

def letter(k, w, h):
    k.envelope(w * 0.5, h * 0.12, w * 0.36)
    for (x, y, r) in [(0.15, 0.7, 6), (0.85, 0.6, 7), (0.25, 0.3, 4), (0.78, 0.25, 5), (0.5, 0.92, 4)]:
        k.flake(w * x, h * y, r, lw=0.6)

def door(n):
    def f(k, w, h):
        k.ground(w * 0.06, w * 0.94, h * 0.12, depth=h * 0.12, drifts=0, ticks=False)
        for i in range(5): k.flake(w * k.r.uniform(0.05, 0.95), h * k.r.uniform(0.6, 0.92), k.r.uniform(2, 3.2), lw=0.45)
        k.advent_door(w * 0.5, h * 0.12, h * 0.48, h * 0.78, num=n)
        sides = [(0.2, 0.5), (0.8, 0.5)] if n % 2 else [(0.22, 0.6), (0.33, 0.4), (0.78, 0.55)]
        for (u, hh) in sides: k.pine(w * u, h * 0.1, h * hh)
    return f

def midnight(k, w, h):
    """After the reveal: the star back on top of the tree beside the clock."""
    floor = h * 0.12
    k.line([(w * 0.06, floor - 5), (w * 0.94, floor - 5)], lw=0.8, amp=0.3); k.rug(w * 0.5, floor * 0.45, w * 0.7, floor * 0.6)
    k.grandfather_clock(w * 0.32, floor - 4, w * 0.17, h * 0.8)
    k.xmas_tree(w * 0.66, floor - 6, h * 0.72, star=True)
    for i in range(10): k.sparkle(w * k.r.uniform(0.45, 0.9), h * k.r.uniform(0.75, 0.98), k.r.uniform(1.2, 2.6))

def thanks(k, w, h):
    floor = h * 0.15
    k.fireplace(w * 0.28, floor, w * 0.44, h * 0.62, stockings=3)
    k.mug(w * 0.33, floor + h * 0.62 + h * 0.05, 9); k.books(w * 0.62, floor + h * 0.62 + h * 0.05, 22, n=2)
    k.cat(w * 0.82, floor * 0.3, 28)
    k.line([(w * 0.04, floor * 0.2), (w * 0.96, floor * 0.2)], lw=0.6, amp=0.3)

def v_blank(k, w, h):
    k.ground(w * 0.06, w * 0.94, h * 0.2, depth=h * 0.2, drifts=1, ticks=False)
    k.pine(w * 0.36, h * 0.18, h * 0.62); k.pine(w * 0.5, h * 0.18, h * 0.78); k.pine(w * 0.64, h * 0.18, h * 0.58)
    for i in range(6): k.flake(w * k.r.uniform(0.1, 0.9), h * k.r.uniform(0.55, 0.92), k.r.uniform(2, 3.2), lw=0.45)

SPECS = {
    "frontispiece": (4.7, 7.0, frontispiece, 7),
    "title": (4.7, 3.0, title, 3),
    "prologue": (3.4, 1.6, prologue, 5),
    "letter": (2.4, 1.2, letter, 6),
    "midnight": (3.4, 2.4, midnight, 8),
    "thanks": (3.2, 1.7, thanks, 9),
    "v_blank": (1.9, 0.85, v_blank, 10),
    **{f"door-{n:02d}": (1.9, 1.0, door(n), 100 + n) for n in range(1, 25)},
}

if __name__ == "__main__":
    only = set(sys.argv[1:])
    for name, (wi, hi, fn, seed) in SPECS.items():
        if only and name not in only: continue
        render(os.path.join(OUT, name + ".png"), wi, hi, fn, seed=seed); print("drew", name)
