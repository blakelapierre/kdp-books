"""Case 20, The Scent of Lavender: painted plates for the detailed colour version (art_color.py 20).
Tamsin's bookshop in warm colour (sage wall, coloured spines, oak counter, plum velvet drawer), harbour quay, boatyard."""
import dkit
from dkit import C, PAL, shade, K, Wt
import bwkit as B
import art_case20 as _A

WALL = C(214, 228, 206); OAK = C(176, 124, 84); OAK_DK = C(128, 88, 60); VELVET = C(120, 70, 120); BRASS = PAL.brass
SPINES = [C(170, 70, 64), C(64, 104, 140), C(92, 140, 96), C(214, 172, 86), C(120, 84, 130), C(236, 226, 206), C(196, 120, 80), C(80, 128, 136)]

def _drawer(k, x, y, w, h):
    k.shape([(x, y), (x + w, y), (x + w + 20, y + h), (x - 20, y + h)], lw=1.2, fill=OAK, amp=0)
    inner = [(x + 10, y + 8), (x + w - 10, y + 8), (x + w + 8, y + h - 6), (x - 8, y + h - 6)]
    k.shape(inner, lw=0.8, fill=VELVET, amp=0)
    with k.tint(VELVET, hatch=shade(VELVET, 0.7)): k.hatch(inner, angle=-60, gap=2.0, lw=0.25, cross=True)
    k.rect(x, y - 24, w, 24, lw=1.1, fill=OAK); k.circle(x + w / 2, y - 12, 4, lw=0.8, fill=BRASS)

def _pen(k, x, y, s):
    body = [(x - s * 0.5, y - s * 0.05), (x + s * 0.3, y - s * 0.06), (x + s * 0.3, y + s * 0.06), (x - s * 0.5, y + s * 0.05)]
    k.shape(body, lw=1.0, fill=C(40, 60, 110), amp=0)
    k.shape([(x + s * 0.3, y - s * 0.06), (x + s * 0.5, y), (x + s * 0.3, y + s * 0.06)], lw=0.9, fill=BRASS, amp=0)
    k.line([(x - s * 0.35, y + s * 0.06), (x - s * 0.05, y + s * 0.08)], lw=1.2, amp=0, color=BRASS)

def counter_scene(k, w, h):
    k.wash_rect(14, 60, w - 14, h - 14, WALL); k.floorboards(w, y=60)
    k.rect(170, 322, 172, 24, lw=0.9, fill=C(60, 90, 80)); k.text(256, 330, "TAMSIN'S BOOKSHOP", size=12, font="Ink-Plex", color=C(246, 226, 160))
    for r in range(3):
        y = 200 + r * 40; k.rect(26, y - 4, 158, 5, lw=0.7, fill=OAK)
        for j in range(10): k.rect(32 + j * 14, y + 1, 10, 26 + (j * 5 % 9), lw=0.4, fill=SPINES[(j + r * 3) % 8])
    k.rect(220, 60, 270, 110, lw=1.3, fill=OAK)
    with k.tint(OAK): k.hatch([(220, 60), (490, 60), (490, 170), (220, 170)], angle=0, gap=3.0, lw=0.3)
    k.rect(214, 166, 282, 8, lw=1.2, fill=OAK_DK)
    k.drawer(300, 182, 110, 50)

def hook_plate(k, w, h): B.full_open(k, w, h); counter_scene(k, w, h); k.pen(355, 210, 60); k.unclip()
def shop_plate(k, w, h): B.plate_open(k, w, h); counter_scene(k, w, h); k.unclip()
def conf_plate(k, w, h): B.plate_open(k, w, h); counter_scene(k, w, h); k.unclip()
def _cloth(k, x, y, w, h):
    k.rect(x, y + h - 8, w, 8, lw=0.9, fill=C(240, 190, 196))
    for i in range(int(w / 10)): k.rect(x + i * 10, y + h - 8, 5, 8, lw=0, fill=C(220, 120, 136))
    k.line([(x + 8, y), (x + 8, y + h - 8)], lw=2, amp=0, color=OAK_DK); k.line([(x + w - 8, y), (x + w - 8, y + h - 8)], lw=2, amp=0, color=OAK_DK)
def nose_plate(k, w, h): B.plate_open(k, w, h); k.tearoom(w, h); _cloth(k, 250, 30, 200, 70); k.unclip()
def talk_plate(k, w, h): B.plate_open(k, w, h); k.tearoom(w, h); _cloth(k, 200, 30, 140, 60); k.unclip()
def _p_yard(k, pw, h):
    k.wash_rect(14, 50, pw - 14, h - 14, C(206, 196, 176)); k.floorboards(pw, y=50); k.boat(380, 70, 110)
    k.rect(420, 90, 40, 50, lw=1.0, fill=C(200, 70, 60)); k.line([(440, 90), (440, 60)], lw=1.2, amp=0)
    k.text(400, 250, "BOATYARD", size=11, font="Ink-Plex", color=PAL.navy)
def _p_tea(k, pw, h): k.tearoom(pw, h); _cloth(k, 310, 30, 150, 60)

def apply(A):
    B.InkBW.drawer = _drawer; B.InkBW.pen = _pen; A.counter_scene = counter_scene
    A.hook_plate, A.shop_plate, A.conf_plate, A.nose_plate, A.talk_plate = hook_plate, shop_plate, conf_plate, nose_plate, talk_plate
    A.lineup_plate = B.lineup_plate_fn([A._p_quay, _p_yard, _p_tea], [n for n, _ in A.CAST])
