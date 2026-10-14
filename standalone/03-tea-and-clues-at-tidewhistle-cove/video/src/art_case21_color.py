"""Case 21, The Spanish Coin: painted plates for the detailed colour version (art_color.py 21).
Sunny sea front with a mint-and-pink ice-cream van, a mahogany museum case with gold coins, silver modern coins."""
import dkit
from dkit import C, PAL, shade, K, Wt
import bwkit as B

SKY = C(190, 222, 242); SKY2 = C(246, 236, 214); MINT = C(178, 228, 206); PINK = C(244, 186, 196); MAHOG = C(132, 72, 52)
GOLD = C(236, 196, 92); SILVER = C(214, 218, 226); GLASS = C(220, 238, 244)

def _coin(k, x, y, r, crown=True):
    col = GOLD if crown else SILVER
    k.circle(x, y, r, lw=1.2, fill=col); k.circle(x, y, r * 0.82, lw=0.5, fill=None)
    if crown:
        pts = [(x - r * 0.45, y - r * 0.25), (x + r * 0.45, y - r * 0.25), (x + r * 0.5, y + r * 0.3), (x + r * 0.25, y + r * 0.05), (x, y + r * 0.4), (x - r * 0.25, y + r * 0.05), (x - r * 0.5, y + r * 0.3)]
        k.shape(pts, lw=0.9, fill=shade(GOLD, 0.85), amp=0)
    else:
        for i in range(-2, 3): k.line([(x - r * 0.4, y + i * r * 0.15), (x + r * 0.4, y + i * r * 0.15)], lw=0.4, amp=0, color=shade(SILVER, 0.6))

def _till(k, x, y, w, h):
    k.rect(x, y, w, h, lw=1.2, fill=C(196, 70, 64)); k.rect(x + 6, y + h * 0.55, w - 12, h * 0.35, lw=0.8, fill=C(236, 230, 214))
    for i in range(4): k.rect(x + 8 + i * (w - 16) / 4, y + 6, (w - 16) / 4 - 4, h * 0.45, lw=0.6, fill=[SILVER, GOLD, SILVER, C(200, 140, 90)][i])

def _van(k, x, y, w):
    h = w * 0.55
    k.shape([(x, y + h * 0.15), (x + w, y + h * 0.15), (x + w, y + h * 0.8), (x + w * 0.82, y + h), (x, y + h)], lw=1.3, fill=MINT, amp=0.1)
    k.wash_rect(x + 2, y + h * 0.15, x + w - 2, y + h * 0.3, PINK)
    k.rect(x + w * 0.12, y + h * 0.45, w * 0.5, h * 0.4, lw=1.0, fill=C(250, 244, 226))
    k.shape([(x + w * 0.08, y + h * 0.88), (x + w * 0.66, y + h * 0.88), (x + w * 0.7, y + h * 0.98), (x + w * 0.04, y + h * 0.98)], lw=0.9, fill=C(250, 250, 246), amp=0)
    for i in range(6):
        if i % 2 == 0: k.shape([(x + w * 0.08 + i * w * 0.1, y + h * 0.88), (x + w * 0.18 + i * w * 0.1, y + h * 0.88), (x + w * 0.2 + i * w * 0.1, y + h * 0.98), (x + w * 0.1 + i * w * 0.1, y + h * 0.98)], lw=0, fill=PINK, stroke=False, amp=0)
    for wx in (0.2, 0.8): k.circle(x + w * wx, y + h * 0.15, h * 0.13, lw=1.0, fill=C(50, 50, 56)); k.circle(x + w * wx, y + h * 0.15, h * 0.05, lw=0.4, fill=SILVER)
    cx, cy = x + w * 0.4, y + h
    k.shape([(cx - 12, cy + 10), (cx + 12, cy + 10), (cx, cy - 2)], lw=0.9, fill=C(222, 178, 112), amp=0); k.circle(cx, cy + 18, 11, lw=0.9, fill=PINK)
    k.text(x + w * 0.37, y + h * 0.28, "JENNA'S ICES", size=10, font="Ink-Plex", color=C(150, 50, 70))

def _cabinet(k, x, y, w, h):
    k.rect(x, y, w, h, lw=1.2, fill=MAHOG); k.rect(x + 8, y + h - 60, w - 16, 52, lw=0.8, fill=C(150, 40, 50))   # red velvet bed
    k.wash_rect(x + 9, y + h - 59, x + w - 9, y + h - 9, C(170, 60, 70))
    k.line([(x + 8, y + h - 8), (x + w - 8, y + h - 60)], lw=0.4, amp=0, color=C(250, 250, 250))

def _seafront(k, w, h):
    k.vgrad(14, 190, w - 14, h - 14, SKY, SKY2, steps=10)
    k.sea(14, w - 14, 120, 190, rows=4); k.headland(14, 180, 190, 30)
    with k.tint(C(250, 246, 236)): k.lighthouse(80, 210, 50)
    k.wash_rect(14, 14, w - 14, 120, C(214, 200, 176)); k.stones(14, w - 14, 14, 60, rows=2); k.line([(14, 120), (w - 14, 120)], lw=1.0, amp=0)

def apply(A):
    B.InkBW.coin = _coin; B.InkBW.till = _till; B.InkBW.van = _van; B.InkBW.cabinet = _cabinet; A._seafront = _seafront
