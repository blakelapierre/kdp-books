"""Draw black-ink illustrations for Stories We Keep -> ../illustrations/*.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inkart import render, Ink

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "illustrations")

def half_title(k, w, h):
    k.envelope(w * 0.28, h * 0.25, w * 0.44)

def frontispiece(k, w, h):
    """A lit cottage at dusk with a lamppost, armchair glow in the window, hills beyond."""
    m = 18
    k.frame(m, m, w - m, h - m)
    k.hills(m + 4, w - m - 4, h * 0.42, amp=10, n=4)
    k.cottage(w * 0.28, h * 0.28, w * 0.38, h * 0.42, chimney=True)
    k.lamppost(w * 0.78, h * 0.28, h * 0.48)
    k.pine(w * 0.12, h * 0.28, h * 0.4)
    k.pine(w * 0.18, h * 0.28, h * 0.32)
    k.cat(w * 0.72, h * 0.28, 28)
    k.ground(m + 4, w - m - 4, h * 0.28, drifts=3)

def title_art(k, w, h):
    k.lamppost(w * 0.18, h * 0.1, h * 0.8)
    k.lamppost(w * 0.82, h * 0.1, h * 0.8)
    k.books(w * 0.35, h * 0.18, w * 0.3, n=4)
    k.envelope(w * 0.42, h * 0.42, w * 0.16)

def opener_beginnings(k, w, h):
    k.frame(12, 12, w - 12, h - 12)
    k.cottage(w * 0.22, h * 0.2, w * 0.45, h * 0.55)
    k.lamppost(w * 0.78, h * 0.2, h * 0.6)
    k.pine(w * 0.08, h * 0.2, h * 0.5)

def opener_childhood(k, w, h):
    k.frame(12, 12, w - 12, h - 12)
    k.hills(20, w - 20, h * 0.35, amp=8, n=3)
    k.pond(w * 0.55, h * 0.22, w * 0.28)
    # simple swing suggestion: rope + seat via lines
    k.line([(w * 0.25, h * 0.85), (w * 0.25, h * 0.35)], lw=1.0, amp=0.2)
    k.line([(w * 0.45, h * 0.85), (w * 0.45, h * 0.35)], lw=1.0, amp=0.2)
    k.rect(w * 0.22, h * 0.32, w * 0.26, 10, lw=0.9)
    k.pine(w * 0.7, h * 0.35, h * 0.45)
    k.cat(w * 0.15, h * 0.2, 26)

def opener_growing(k, w, h):
    k.frame(12, 12, w - 12, h - 12)
    k.signpost(w * 0.35, h * 0.15, w * 0.35, arrows=[("HOME", 1), ("AWAY", -1)])
    k.rect(w * 0.55, h * 0.2, w * 0.22, h * 0.18, lw=1.0)
    k.line([(w * 0.55, h * 0.29), (w * 0.77, h * 0.29)], lw=0.7)
    k.lamppost(w * 0.15, h * 0.15, h * 0.7)

def opener_love(k, w, h):
    k.frame(12, 12, w - 12, h - 12)
    k.fireplace(w * 0.28, h * 0.18, w * 0.44, h * 0.55, fire=True, stockings=2)
    k.armchair(w * 0.08, h * 0.18, w * 0.22, facing=1)
    k.armchair(w * 0.7, h * 0.18, w * 0.22, facing=-1)
    k.rug(w * 0.3, h * 0.12, w * 0.4, 18)
    k.cat(w * 0.48, h * 0.14, 24)

def opener_work(k, w, h):
    k.frame(12, 12, w - 12, h - 12)
    k.window_snow(w * 0.15, h * 0.35, w * 0.35, h * 0.4, panes=(2, 2), curtains=False)
    k.books(w * 0.58, h * 0.25, w * 0.28, n=5)
    k.mug(w * 0.62, h * 0.15, 36)
    k.rect(w * 0.15, h * 0.18, w * 0.35, 8, lw=0.9)  # desk edge

def opener_holidays(k, w, h):
    k.frame(12, 12, w - 12, h - 12)
    k.fireplace(w * 0.25, h * 0.15, w * 0.5, h * 0.55, fire=True, stockings=3)
    k.garland(w * 0.2, w * 0.8, h * 0.78, sag=12)
    k.candle(w * 0.12, h * 0.2, 40)
    k.candle(w * 0.85, h * 0.2, 40)

def opener_favorites(k, w, h):
    k.frame(12, 12, w - 12, h - 12)
    k.mug(w * 0.2, h * 0.25, 50)
    k.books(w * 0.42, h * 0.22, w * 0.35, n=4)
    k.armchair(w * 0.55, h * 0.15, w * 0.35, facing=-1)

def opener_wisdom(k, w, h):
    k.frame(12, 12, w - 12, h - 12)
    k.lamppost(w * 0.15, h * 0.15, h * 0.7)
    k.envelope(w * 0.35, h * 0.35, w * 0.35)
    k.books(w * 0.4, h * 0.15, w * 0.25, n=3)

def thanks(k, w, h):
    k.lamppost(w * 0.5, h * 0.1, h * 0.8)

def vignette_lamp(k, w, h):
    k.lamppost(w * 0.5, h * 0.05, h * 0.9)

def vignette_envelope(k, w, h):
    k.envelope(w * 0.2, h * 0.25, w * 0.6)

def vignette_mug(k, w, h):
    k.mug(w * 0.3, h * 0.15, h * 0.7)

def vignette_books(k, w, h):
    k.books(w * 0.2, h * 0.2, w * 0.6, n=4)

def cover_scene(k, w, h):
    """Night scene for hardcover front: cottage, lamp, stars."""
    k.stars(10, h * 0.45, w - 10, h - 10, n=40, rmax=2.8)
    k.moon(w * 0.82, h * 0.78, 28)
    k.hills(0, w, h * 0.38, amp=14, n=5)
    k.cottage(w * 0.22, h * 0.2, w * 0.42, h * 0.42, chimney=True)
    k.lamppost(w * 0.75, h * 0.2, h * 0.5)
    k.pine(w * 0.08, h * 0.2, h * 0.45)
    k.pine(w * 0.88, h * 0.18, h * 0.4)
    k.ground(0, w, h * 0.2, drifts=4)
    k.cat(w * 0.68, h * 0.2, 22)

JOBS = [
    ("half-title", 3.2, 2.0, half_title, 1),
    ("frontispiece", 4.6, 6.2, frontispiece, 2),
    ("title", 4.2, 2.4, title_art, 3),
    ("opener-beginnings", 4.6, 5.0, opener_beginnings, 4),
    ("opener-childhood", 4.6, 5.0, opener_childhood, 5),
    ("opener-growing", 4.6, 5.0, opener_growing, 6),
    ("opener-love", 4.6, 5.0, opener_love, 7),
    ("opener-work", 4.6, 5.0, opener_work, 8),
    ("opener-holidays", 4.6, 5.0, opener_holidays, 9),
    ("opener-favorites", 4.6, 5.0, opener_favorites, 10),
    ("opener-wisdom", 4.6, 5.0, opener_wisdom, 11),
    ("thanks", 3.0, 3.5, thanks, 12),
    ("v-lamp", 1.4, 2.0, vignette_lamp, 13),
    ("v-envelope", 1.6, 1.2, vignette_envelope, 14),
    ("v-mug", 1.4, 1.4, vignette_mug, 15),
    ("v-books", 1.6, 1.2, vignette_books, 16),
    ("cover-scene", 5.2, 5.6, cover_scene, 17),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, wi, hi, fn, seed in JOBS:
        path = os.path.join(OUT, f"{name}.png")
        print("drawing", name)
        render(path, wi, hi, fn, seed=seed, dpi=300)
    print("done", len(JOBS), "illustrations ->", OUT)
