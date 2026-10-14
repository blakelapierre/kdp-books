"""Case 23, The Odd Glove: painted plates for the detailed colour version (art_color.py 23).
Navy knitted gloves with white anchors (the key clue, now in real colour), a cobbled lane at dusk with painted
shopfronts, a white moth orchid in a terracotta pot. Lineup glove / pocket overlays are re-aimed at the DETAILED
characters' hands (people3 L_HAND / R_HAND) instead of the old peg-doll hand points."""
import math
import dkit
from dkit import C, PAL, shade, K, Wt, L_HAND, R_HAND
import bwkit as B
import art_case23 as _A

NAVY = C(44, 58, 104); NAVY2 = C(70, 88, 140); WHITE = C(250, 250, 246); DUSK = C(236, 176, 150); DUSK2 = C(150, 160, 200)
POT = C(200, 110, 70); PETAL = C(252, 246, 250); LEAF = C(80, 140, 80)

def _anchor(k, x, y, s):
    k.circle(x, y + s, s * 0.3, lw=0.5, fill=None); k.line([(x, y + s * 0.7), (x, y - s)], lw=0.7, amp=0, color=NAVY)
    k.line([(x - s * 0.5, y + s * 0.3), (x + s * 0.5, y + s * 0.3)], lw=0.6, amp=0, color=NAVY)
    k.shape(k.arcpts(x, y - s * 0.4, s * 0.7, s * 0.6, 180, 360, 10), lw=0.6, fill=None, amp=0)

def _glove(k, x, y, s, anchors=False, right=True):
    w = s * 0.5; cuff = s * 0.22; sg = -1 if right else 1
    k.rect(x - w / 2, y, w, cuff, lw=0.9, fill=WHITE if anchors else NAVY)
    palm = [(x - w / 2, y + cuff), (x + w / 2, y + cuff), (x + w / 2, y + s * 0.62), (x - w / 2, y + s * 0.62)]
    def knit(p):
        k.shape(p, lw=0.9, fill=NAVY, amp=0)
        with k.tint(NAVY, hatch=NAVY2): k.hatch(p, angle=45, gap=max(1.0, s * 0.03), lw=0.3, cross=True)
    knit(palm); fw = w / 4
    for i, fl in enumerate((0.3, 0.38, 0.36, 0.26) if right else (0.26, 0.36, 0.38, 0.3)):
        knit([(x - w / 2 + i * fw + 0.5, y + s * 0.62), (x - w / 2 + (i + 1) * fw - 0.5, y + s * 0.62), (x - w / 2 + (i + 1) * fw - 0.5, y + s * (0.62 + fl)), (x - w / 2 + i * fw + 0.5, y + s * (0.62 + fl))])
    knit([(x + sg * w / 2, y + cuff + s * 0.05), (x + sg * (w / 2 + s * 0.16), y + s * 0.42), (x + sg * (w / 2 + s * 0.1), y + s * 0.5), (x + sg * w / 2, y + s * 0.36)])
    if anchors:
        for j in range(3): _anchor(k, x - w / 3 + j * w / 3, y + cuff / 2, cuff * 0.32)
    else:
        for j in range(5): k.line([(x - w / 2 + j * w / 4, y + 1), (x - w / 2 + j * w / 4, y + cuff - 1)], lw=0.3, amp=0, color=NAVY2)

def _mitt(k, x, y, h, anchors=False):
    r = h * 0.032; k.shape(k.arcpts(x, y, r, r * 1.25, 0, 360, 16), lw=0.6, fill=NAVY, amp=0)
    k.circle(x + r * 0.9, y + r * 0.2, r * 0.45, lw=0.4, fill=NAVY)
    k.rect(x - r, y + r * 0.9, 2 * r, r * 0.7, lw=0.5, fill=WHITE if anchors else NAVY)
    if anchors:
        for j in (-1, 0, 1): k.circle(x + j * r * 0.6, y + r * 1.25, r * 0.14, lw=0, fill=NAVY, stroke=False)

def _orchid(k, x, y, s):
    k.shape([(x - s * 0.3, y), (x + s * 0.3, y), (x + s * 0.38, y + s * 0.4), (x - s * 0.38, y + s * 0.4)], lw=1.0, fill=POT, amp=0)
    k.line([(x, y + s * 0.4), (x + s * 0.05, y + s * 1.1), (x + s * 0.3, y + s * 1.3)], lw=1.1, amp=0.2, color=C(90, 120, 70))
    for lx in (-1, 1): k.shape(k.arcpts(x + lx * s * 0.22, y + s * 0.5, s * 0.25, s * 0.08, 0, 360, 12), lw=0.6, fill=LEAF, amp=0)
    for fx, fy in ((0.3, 1.3), (0.12, 1.12), (0.42, 1.12)):
        cx, cy = x + s * fx, y + s * fy
        for a in range(0, 360, 72): k.shape(k.arcpts(cx + s * 0.07 * math.cos(math.radians(a)), cy + s * 0.07 * math.sin(math.radians(a)), s * 0.07, s * 0.05, 0, 360, 10), lw=0.4, fill=PETAL, amp=0)
        k.circle(cx, cy, s * 0.025, lw=0.3, fill=C(220, 90, 140))

def _shopfront(k, x, w, name, y=60, hgt=200):
    wall = C(206, 230, 208) if "FLOWER" in name else C(200, 220, 234)
    k.rect(x, y, w, hgt, lw=1.1, fill=wall); k.rect(x + w * 0.1, y + hgt * 0.3, w * 0.5, hgt * 0.45, lw=0.9, fill=C(252, 236, 180))   # lit window
    k.rect(x + w * 0.68, y, w * 0.22, hgt * 0.65, lw=0.9, fill=C(84, 128, 160) if "FLOWER" in name else C(92, 140, 112))
    k.rect(x + 6, y + hgt * 0.82, w - 12, hgt * 0.14, lw=0.8, fill=C(60, 90, 80)); k.text(x + w / 2, y + hgt * 0.86, name, size=10, font="Ink-Plex", color=C(246, 226, 160))

def _sky(k, w, h, y=60): k.vgrad(14, y, w - 14, h - 14, DUSK2, DUSK, steps=10)

def _lane(k, w, h):
    _sky(k, w, h); k.stones(14, w - 14, 14, 60, rows=3); k.line([(14, 60), (w - 14, 60)], lw=1.0, amp=0)
    _shopfront(k, 30, 200, "MORWENNA'S FLOWERS"); _shopfront(k, 250, 150, "FENWICK GROCER")
    k.line([(440, 60), (440, 230)], lw=1.6, amp=0, color=C(70, 70, 80)); k.rect(420, 222, 40, 26, lw=1.0, fill=C(214, 70, 64)); k.text(440, 231, "BUS", size=9, font="Ink-Plex", color=WHITE)

def hook_plate(k, w, h): B.full_open(k, w, h); _lane(k, w, h); k.unclip()
def lane_plate(k, w, h): B.plate_open(k, w, h); _lane(k, w, h); k.unclip()
def sill_plate(k, w, h):
    B.plate_open(k, w, h); k.wash_rect(14, 60, w - 14, h - 14, C(236, 222, 200)); k.floorboards(w, y=60)
    k.rect(150, 150, 220, 170, lw=1.4, fill=C(240, 236, 226)); k.vgrad(152, 152, 368, 318, DUSK2, DUSK, steps=8); k.rect(152, 152, 216, 166, lw=0.8, fill=None)
    k.rect(140, 140, 240, 12, lw=1.0, fill=C(176, 124, 84))
    k.text(256, 340, "the back windowsill", size=11, font="Ink-Plex", color=PAL.navy)
def win_open(k, w, h, v):
    B.part_open(k, w, h); k.rect(152, 152, 216, 166, lw=0.1, fill=C(40, 44, 70)); k.pin_card(250, 96, 90, 30, ["open!"], size=11); k.unclip()
def cobble_plate(k, w, h):
    B.plate_open(k, w, h); k.stones(14, w - 14, 14, 140, rows=5)
    k.wash_rect(14, 140, w - 14, h - 14, C(214, 190, 160))
    with k.tint(C(214, 190, 160), hatch=C(170, 140, 110)): k.wall(14, 140, w - 28, 230, gap=3.0, color=C(214, 190, 160))
    k.rect(170, 220, 170, 120, lw=1.4, fill=C(40, 44, 70)); k.unclip()
def gzoom_part(k, w, h, v):
    B.part_open(k, w, h); k.rect(300, 40, 190, 150, lw=1.3, fill=C(250, 244, 226)); k.glove(395, 66, 90, anchors=True, right=True)
    k.text(395, 48, "navy \u00b7 RIGHT hand", size=11, font="Ink-Kalam", color=NAVY); k.unclip()
def _bus(k, pw, h):
    _sky(k, pw, h, y=50); k.stones(14, pw - 14, 14, 50, rows=2); k.line([(300, 50), (300, 250)], lw=1.6, amp=0, color=C(70, 70, 80))
    k.rect(276, 244, 48, 30, lw=1.0, fill=C(214, 70, 64)); k.text(300, 254, "BUS", size=10, font="Ink-Plex", color=WHITE)
def _grocer(k, pw, h): _sky(k, pw, h, y=50); k.stones(14, pw - 14, 14, 50, rows=2); _shopfront(k, 250, 220, "FENWICK GROCER", y=50, hgt=200)
def _walk(k, pw, h):
    _sky(k, pw, h, y=50); k.stones(14, pw - 14, 14, 50, rows=2)
    k.wash_rect(250, 50, 490, 210, C(214, 190, 160))
    with k.tint(C(214, 190, 160), hatch=C(170, 140, 110)): k.wall(250, 50, 240, 160, gap=3.0, color=C(214, 190, 160))
FX, FY, FH = _A.FX, _A.FY, _A.FH
HANDL = (FX + L_HAND[0] / 100 * FH, FY + L_HAND[1] / 100 * FH)
HANDR = (FX + R_HAND[0] / 100 * FH, FY + R_HAND[1] / 100 * FH)

def apply(A):
    B.InkBW.glove = _glove; B.InkBW.orchid = _orchid; A._mitt = _mitt; A._shopfront = _shopfront; A._lane = _lane
    A.hook_plate, A.lane_plate, A.sill_plate, A.win_open, A.cobble_plate, A.gzoom_part = hook_plate, lane_plate, sill_plate, win_open, cobble_plate, gzoom_part
    A.HANDL, A.HANDR = HANDL, HANDR
    A.lineup_plate = B.lineup_plate_fn([_bus, _grocer, _walk], [n for n, _ in A.CAST])
