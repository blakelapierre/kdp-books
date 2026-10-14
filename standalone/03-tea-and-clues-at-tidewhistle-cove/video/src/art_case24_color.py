"""Case 24, The Kite Festival: painted plates for the detailed colour version (art_color.py 24).
Breezy beach: sky, sea on the LEFT, golden sand, marram dunes, green hills and pastel beach huts on the RIGHT;
bright kites, red-striped judges' tent, a carved puffin (black, white, orange beak). Wind direction unchanged."""
import math
import dkit
from dkit import C, PAL, shade, K, Wt
import bwkit as B

SKY = C(186, 220, 244); SKY2 = C(240, 240, 226); SAND = C(238, 218, 168); DUNE = C(222, 200, 146); MARRAM = C(120, 160, 90)
HILL = C(150, 190, 120); KITES = [C(226, 84, 84), C(80, 140, 210), C(246, 196, 70), C(140, 90, 170)]
HUTS = [C(244, 186, 196), C(170, 210, 236), C(246, 222, 130)]; STRIPE = C(214, 76, 70); CANVAS = C(252, 248, 236)
_ki = [0]

def _kite(k, x, y, s, tail=True, lean=25):
    a = math.radians(lean); ca, sa = math.cos(a), math.sin(a)
    P = [(0, s * 0.6), (s * 0.35, 0), (0, -s * 0.5), (-s * 0.35, 0)]
    pts = [(x + px * ca + py * sa, y - px * sa + py * ca) for px, py in P]
    col = KITES[int(x + y) % 4]
    k.shape(pts, lw=0.9, fill=col, amp=0)
    k.shape([pts[0], pts[1], (x, y)], lw=0, fill=shade(col, 0.8), stroke=False, amp=0)
    k.line([pts[0], pts[2]], lw=0.4, amp=0); k.line([pts[1], pts[3]], lw=0.4, amp=0)
    if tail:
        bx, by = pts[2]
        k.line([(bx, by), (bx - s * 0.3, by - s * 0.3), (bx - s * 0.2, by - s * 0.6), (bx - s * 0.45, by - s * 0.9)], lw=0.5, amp=0.3)
        for j in range(3): k.circle(bx - s * (0.15 + j * 0.13), by - s * (0.22 + j * 0.25), 1.8, lw=0.4, fill=KITES[(j + 1) % 4])

def _flag(k, x, y, hp=60, fw=34):
    k.line([(x, y), (x, y + hp)], lw=1.3, amp=0, color=C(110, 90, 70))
    k.shape([(x, y + hp), (x + fw, y + hp - 4), (x + fw * 0.85, y + hp - 9), (x + fw, y + hp - 14), (x, y + hp - 16)], lw=0.8, fill=C(226, 84, 84), amp=0.1)

def _puffin(k, x, y, s):
    k.rect(x - s * 0.35, y, s * 0.7, s * 0.14, lw=0.8, fill=C(176, 124, 84))
    body = k.arcpts(x, y + s * 0.5, s * 0.25, s * 0.36, 0, 360, 22); k.shape(body, lw=1.0, fill=C(40, 40, 48), amp=0)
    k.shape(k.arcpts(x + s * 0.05, y + s * 0.45, s * 0.14, s * 0.24, 0, 360, 18), lw=0.6, fill=C(250, 250, 246), amp=0)
    k.circle(x, y + s * 0.92, s * 0.17, lw=1.0, fill=C(40, 40, 48)); k.circle(x + s * 0.06, y + s * 0.94, s * 0.1, lw=0.4, fill=C(250, 250, 246))
    k.circle(x + s * 0.08, y + s * 0.95, s * 0.025, lw=0, fill=K, stroke=False)
    k.shape([(x + s * 0.14, y + s * 0.96), (x + s * 0.36, y + s * 0.9), (x + s * 0.14, y + s * 0.82)], lw=0.8, fill=C(240, 130, 50), amp=0)

def _tent(k, x, y, w):
    h = w * 0.7
    k.shape([(x - w / 2, y), (x + w / 2, y), (x + w / 2, y + h * 0.6), (x, y + h), (x - w / 2, y + h * 0.6)], lw=1.2, fill=CANVAS, amp=0.1)
    for j in range(6):
        if j % 2 == 0:
            x0, x1 = x - w / 2 + j * w / 6, x - w / 2 + (j + 1) * w / 6
            top = lambda xx: y + h * 0.6 + (h * 0.4) * (1 - abs(xx - x) / (w / 2))
            k.shape([(x0, y), (x1, y), (x1, top(x1)), (x0, top(x0))], lw=0, fill=STRIPE, stroke=False, amp=0)
    k.shape([(x - w / 2, y), (x + w / 2, y), (x + w / 2, y + h * 0.6), (x, y + h), (x - w / 2, y + h * 0.6)], lw=1.2, fill=None, amp=0.1)
    k.line([(x, y + h), (x, y + h + 14)], lw=0.8, amp=0)
    k.shape([(x, y + h + 14), (x + 14, y + h + 10), (x, y + h + 6)], lw=0.6, fill=C(246, 196, 70), amp=0)

def _beach(k, w, h, sea=True):
    k.vgrad(14, 60, w - 14, h - 14, SKY, SKY2, steps=10)
    k.shape([(300, 150), (350, 180), (400, 172), (450, 200), (w - 14, 190), (w - 14, 60), (300, 60)], lw=0.8, fill=HILL, amp=0.3)
    k.wash_rect(14, 14, w - 14, 60, SAND)
    if sea: k.sea(14, 170, 60, 150, rows=5)
    k.shape([(14, 60), (170, 60), (200, 150), (14, 150)], lw=0, fill=None, amp=0)
    k.shape([(170, 60), (200, 150), (14, 150), (14, 60)], lw=0, fill=None, amp=0)
    k.wash([(14, 14), (w - 14, 14), (w - 14, 60), (14, 60)], SAND)
    k.line([(14, 60), (w - 14, 60)], lw=0.9, amp=0.1)
    k.line([(170, 60), (200, 150)], lw=0.8, amp=0.2)
    for i, hx in enumerate((360, 400, 440)):
        k.rect(hx, 150, 26, 22, lw=0.7, fill=HUTS[i]); k.shape([(hx - 2, 172), (hx + 13, 184), (hx + 28, 172)], lw=0.7, fill=C(206, 136, 108), amp=0)
    k.wash([(170, 60), (300, 60), (300, 150), (200, 150)], SAND)
    for dx in (360, 420, 470):
        k.shape(k.arcpts(dx, 60, 40, 30, 0, 180, 14), lw=0.9, fill=DUNE, amp=0.2)
        for j in range(4): k.line([(dx - 10 + j * 6, 80), (dx - 6 + j * 6, 96)], lw=0.6, amp=0.2, color=MARRAM)

def tent_plate(k, w, h):
    B.plate_open(k, w, h); _beach(k, w, h); k.judges_tent(250, 60, 180)
    k.rect(210, 60, 80, 40, lw=0.9, fill=C(176, 124, 84)); k.text(110, 30, "the judges' tent, by the water's edge", size=10, font="Ink-Kalam", color=PAL.navy); k.unclip()
def lobster_part(k, w, h, v):
    B.part_open(k, w, h); x, y = 90, 300
    k.shape(k.arcpts(x, y, 30, 14, 0, 360, 20), lw=1.0, fill=C(220, 70, 56), amp=0.1)
    for s_ in (-1, 1): k.shape(k.arcpts(x + 36, y + s_ * 14, 10, 6, 0, 360, 12), lw=0.8, fill=C(220, 70, 56), amp=0)
    k.text(x, y - 30, "the lobster kite", size=10, font="Ink-Kalam", color=PAL.navy); k.unclip()
def balloon_part(k, w, h, v):
    B.part_open(k, w, h); k.shape(k.arcpts(470, 300, 12, 15, 0, 360, 16), lw=0.9, fill=C(236, 100, 140), amp=0); k.line([(470, 285), (462, 262)], lw=0.4, amp=0.3)
    k.text(440, 330, "Rosie's balloon \u2192 hills", size=9, font="Ink-Kalam", color=PAL.navy); k.unclip()
def _sky50(k, pw, h): k.vgrad(14, 50, pw - 14, h - 14, SKY, SKY2, steps=8); k.wash_rect(14, 14, pw - 14, 50, SAND)
def _dunes(k, pw, h):
    _sky50(k, pw, h); k.line([(14, 50), (pw - 14, 50)], lw=0.9, amp=0.1)
    for dx in (300, 380, 450): k.shape(k.arcpts(dx, 50, 44, 34, 0, 180, 14), lw=0.9, fill=DUNE, amp=0.2)
def _stall(k, pw, h):
    _sky50(k, pw, h); k.line([(14, 50), (pw - 14, 50)], lw=0.9, amp=0.1); k.rect(300, 50, 170, 60, lw=1.0, fill=C(92, 140, 112))
    k.text(385, 80, "BOOKS", size=12, font="Ink-Plex", color=CANVAS)
    for j in range(5): k.rect(310 + j * 30, 112, 22, 30, lw=0.6, fill=[C(170, 70, 64), C(64, 104, 140), C(214, 172, 86), C(120, 84, 130), C(92, 140, 96)][j])
    k.text(385, 160, "car park \u2192", size=9, font="Ink-Kalam", color=PAL.navy)
def _edge(k, pw, h): _sky50(k, pw, h); k.sea(14, pw - 14, 50, 120, rows=4); k.line([(14, 50), (pw - 14, 50)], lw=0.9, amp=0.1); k.judges_tent(420, 50, 110)

def apply(A):
    B.InkBW.kite = _kite; B.InkBW.flag = _flag; B.InkBW.puffin = _puffin; B.InkBW.judges_tent = _tent; A._beach = _beach
    A.tent_plate, A.lobster_part, A.balloon_part = tent_plate, lobster_part, balloon_part
    A.lineup_plate = B.lineup_plate_fn([_dunes, _stall, _edge], [n for n, _ in A.CAST])
