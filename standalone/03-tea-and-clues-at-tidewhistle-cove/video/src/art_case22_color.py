"""Case 22, The Honest Fishermen: painted plates for the detailed colour version (art_color.py 22).
Harbour in colour (dkit harbour: sky, sea, stone quay), a tan rope net with red floats, glazed saffron buns."""
import dkit
from dkit import C, PAL, shade, K, Wt
import bwkit as B

ROPE = C(196, 150, 96); FLOAT = C(220, 80, 64); BUN = C(232, 176, 80)

def _net(k, x, y, w, h, holes=False):
    pts = [(x, y + h), (x + w, y + h), (x + w * 0.85, y + h * 0.3), (x + w * 0.5, y), (x + w * 0.15, y + h * 0.3)]
    k.shape(pts, lw=1.0, fill=C(236, 214, 170), amp=0.2)
    with k.tint(ROPE, hatch=shade(ROPE, 0.7)): k.hatch(pts, angle=40, gap=5, lw=0.5, cross=True)
    for i in range(5): k.circle(x + w * (0.1 + i * 0.2), y + h, 3.2, lw=0.6, fill=FLOAT)
    if holes:
        for hx, hy in ((0.35, 0.5), (0.62, 0.35), (0.55, 0.7)): k.circle(x + w * hx, y + h * hy, 6, lw=0.7, fill=C(140, 190, 210))

def _bun(k, x, y, r):
    k.shape(k.arcpts(x, y, r, r * 0.65, 0, 360, 22), lw=0.9, fill=BUN, amp=0.1)
    for i in range(4): k.circle(x - r * 0.5 + i * r * 0.33, y + r * 0.1 * (i % 2), 1.2, lw=0, fill=C(110, 60, 40), stroke=False)

def _p(k, pw, h):
    k.vgrad(14, 108, pw - 14, h - 14, C(190, 222, 242), C(246, 236, 214), steps=8)
    k.stones(14, pw - 14, 14, 50, rows=2); k.sea(14, pw - 14, 50, 110, rows=3); k.line([(14, 50), (pw - 14, 50)], lw=1.0, amp=0)

def apply(A):
    B.InkBW.net = _net; B.InkBW.bun = _bun
    A.lineup_plate = B.lineup_plate_fn([_p, _p, _p], [n for n, _ in A.CAST])
