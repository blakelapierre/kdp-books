"""Case 18, The Moonlit Walk: painted plates for the detailed colour version (art_color.py 18).
The night is a real night: deep navy-to-indigo sky with warm stars (no moon anywhere outside Miss Clemo's bubble),
a dark grassy clifftop, warm lamp-lit windows; the club tent in striped canvas."""
import random
import dkit
from dkit import C, PAL, shade, K, Wt
import bwkit as B

NIGHT = C(26, 34, 70); NIGHT2 = C(58, 64, 112); STAR = C(252, 240, 190); GRASS_N = C(60, 92, 70); LAMP = C(252, 220, 140)

def _night(k, x0, y0, x1, y1, seed=18, n=40):
    k.vgrad(x0, 14, x1, y1, NIGHT, NIGHT2, steps=12)
    rr = random.Random(seed)
    for _ in range(n):
        x, y, r = rr.uniform(x0 + 8, x1 - 8), rr.uniform(y0 + 8, y1 - 8), rr.uniform(1.0, 2.4)
        k.circle(x, y, r, lw=0, fill=STAR, stroke=False)
        k.line([(x - r * 1.8, y), (x + r * 1.8, y)], lw=0.4, amp=0, color=STAR); k.line([(x, y - r * 1.8), (x, y + r * 1.8)], lw=0.4, amp=0, color=STAR)

def _tent(k, x, y, w, h):
    k.shape([(x, y), (x + w, y), (x + w / 2, y + h)], lw=1.3, fill=C(236, 214, 170), amp=0.1)
    k.shape([(x + w * 0.3, y), (x + w * 0.7, y), (x + w / 2, y + h * 0.7)], lw=0.9, fill=LAMP, amp=0)
    k.text(x + w / 2, y + h * 0.78 - 12, "CLUB", size=9, font="Ink-Plex", color=C(120, 60, 40))

def _scope(k, x, y, s):
    for dx in (-0.3, 0, 0.3): k.line([(x + dx * s, y), (x, y + s * 0.6)], lw=1.0, amp=0, color=C(170, 140, 100))
    tube = [(x - s * 0.3, y + s * 0.5), (x + s * 0.35, y + s * 0.95), (x + s * 0.3, y + s * 1.02), (x - s * 0.35, y + s * 0.58)]
    k.shape(tube, lw=1.0, fill=PAL.brass, amp=0)

def clifftop(k, w, h, seed=18):
    k.night(14, 150, w - 14, h - 14, seed=seed)
    k.vgrad(14, 100, 220, 150, C(40, 60, 100), C(30, 46, 84), steps=6)
    with k.tint(C(40, 60, 100), hatch=C(90, 110, 160)): B.InkBW.sea(k, 14, 220, 100, 150, rows=3)
    k.shape([(200, 150)] + [(200 + (w - 214) * t / 16, 150 + 40 * (abs(((t / 16) * 3.14) % 3.14 - 1.57) < 9) * (0.6 + 0.4 * ((t * 7) % 5) / 5)) for t in range(17)] + [(w - 14, 150), (w - 14, 60), (200, 60)], lw=0.8, fill=GRASS_N, amp=0.2)
    k.wash_rect(14, 60, 220, 100, GRASS_N); k.line([(14, 100), (220, 100)], lw=0.8, amp=0)
    k.stones(14, w - 14, 14, 60, rows=2)
    for x in (110, 250): k.scope(x, 140 if x > 200 else 100, 46)

def _p_cott(k, pw, h):
    k.night(14, 230, pw - 14, h - 14, seed=3, n=14); k.stones(14, pw - 14, 14, 50, rows=2)
    k.rect(300, 50, 170, 150, lw=1.2, fill=C(214, 200, 176)); k.shape([(290, 200), (480, 200), (385, 240)], lw=1.2, fill=C(120, 80, 70), amp=0)
    k.rect(360, 50, 40, 80, lw=1.0, fill=C(84, 128, 160)); k.rect(320, 130, 30, 30, lw=0.8, fill=LAMP); k.rect(420, 130, 30, 30, lw=0.8, fill=LAMP)
    k.text(385, 168, "Demelza's cottage", size=10, font="Ink-Kalam", color=C(60, 40, 30))
def _p_path(k, pw, h):
    k.night(14, 230, pw - 14, h - 14, seed=5, n=14)
    k.shape([(14, 90)] + [(14 + (pw - 28) * t / 10, 90 + 60 * (1 - abs(t - 5) / 5)) for t in range(11)] + [(pw - 14, 14), (14, 14)], lw=0.8, fill=GRASS_N, amp=0.2)
    for i in range(10): k.line([(250 + i * 24, 90 + (i % 3) * 6), (264 + i * 24, 96 + (i % 2) * 6)], lw=1.0, amp=0.3, color=C(200, 190, 160))
    k.rect(400, 120, 80, 70, lw=1.1, fill=C(214, 200, 176)); k.rect(420, 140, 20, 20, lw=0.6, fill=LAMP); k.text(440, 170, "INN", size=10, font="Ink-Plex", color=C(60, 40, 30))

def apply(A):
    B.InkBW.night = _night; B.InkBW.tent = _tent; B.InkBW.scope = _scope; A.clifftop = clifftop
    A.lineup_plate = B.lineup_plate_fn([_p_cott, _p_cott, _p_path], [n for n, _ in A.CAST])
