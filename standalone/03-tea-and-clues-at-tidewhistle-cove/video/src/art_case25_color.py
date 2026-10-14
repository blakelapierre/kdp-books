"""Case 25, The Teaspoon Thief: hand-painted colour plates for the detailed colour version (art_color.py 25).
Same layout / coordinates as art_case25.py (so every animated part still lands in place); only the backdrops are
repainted: duck-egg tea-room wall, oak sideboard, a garden view through the back window, the apple tree at dusk."""
import random
import dkit
from dkit import C, PAL, shade, mix, K, Wt
import bwkit as B

WALL = C(232, 222, 196); DADO = C(196, 222, 214); OAK = C(176, 124, 84); OAK_DK = C(128, 88, 60); MARBLE = C(240, 236, 228)
SKY = C(200, 224, 238); SKY2 = C(246, 230, 200); LAWN = C(150, 190, 120); LEAF = C(112, 160, 96); BARK = C(126, 92, 66)

def _room(k, w, h, floor_y=60):
    k.wash_rect(14, floor_y, w - 14, h - 14, WALL)
    for i in range(14, int(w), 26): k.line([(i, floor_y + 40), (i, h - 14)], lw=0.25, amp=0, color=shade(WALL, 0.9))   # paper stripes
    k.wash_rect(14, floor_y, w - 14, floor_y + 38, DADO); k.line([(14, floor_y + 38), (w - 14, floor_y + 38)], lw=0.7, amp=0.1)
    k.floorboards(w, y=floor_y)

def _garden_window(k, x, y, w, h):
    """Back window, top sash open a hand's width; garden + apple tree outside."""
    k.vgrad(x, y, x + w, y + h, SKY, SKY2, steps=8)
    k.wash_rect(x, y, x + w, y + h * 0.28, LAWN)
    k.shape([(x + w * 0.62, y + h * 0.28), (x + w * 0.66, y + h * 0.28), (x + w * 0.66, y + h * 0.6), (x + w * 0.62, y + h * 0.6)], lw=0.5, fill=BARK, amp=0)
    for cx, cy, r in ((0.55, 0.7, 0.14), (0.7, 0.75, 0.15), (0.63, 0.86, 0.12)):
        k.circle(x + w * cx, y + h * cy, w * r, lw=0.5, fill=LEAF)

def _sideboard(k, w, h):
    _room(k, w, h, floor_y=60)
    # back window (frame drawn over the painted view; the open top gap stays dark)
    k.rect(150, 190, 210, 160, lw=1.3, fill=C(240, 236, 226))
    _garden_window(k, 156, 196, 198, 120)
    k.rect(156, 196, 198, 120, lw=0.8, fill=None); k.line([(255, 196), (255, 316)], lw=1.0, amp=0)
    k.rect(156, 330, 198, 14, lw=0.8, fill=C(48, 56, 70))
    k.text(255, 360, "BACK WINDOW", size=9, font="Ink-Plex", color=PAL.navy)
    # oak sideboard with marble top
    k.rect(60, 60, 392, 90, lw=1.3, fill=OAK)
    with k.tint(OAK): k.hatch([(60, 60), (452, 60), (452, 150), (60, 150)], angle=0, gap=3.0, lw=0.3)
    k.rect(56, 146, 400, 8, lw=1.2, fill=MARBLE)
    for dx in (160, 256, 352):
        k.line([(dx, 64), (dx, 142)], lw=0.6, amp=0, color=OAK_DK); k.circle(dx - 10, 104, 2.4, lw=0.4, fill=PAL.brass)
    # untouched things
    k.rect(80, 154, 34, 40, lw=0.9, fill=C(214, 70, 64)); k.text(97, 170, "RNLI", size=6, font="Ink-Plex", color=C(250, 250, 246)); k.coins(97, 182, n=5)
    k.spoon(380, 162, 50, wood=True); k.spoon(380, 172, 50, wood=True); k.spoon(380, 184, 46, shiny=False)
    with k.tint(C(236, 236, 244)):
        k.shape(k.arcpts(130, 162, 16, 8, 180, 360, 12), lw=0.9, fill=Wt, amp=0); k.rect(114, 162, 32, 14, lw=0.9, fill=Wt)
    k.text(130, 166, "SUGAR", size=5, font="Ink-Plex", color=PAL.navy)
    with k.tint(C(214, 176, 120)): k.shape(k.arcpts(440, 154, 26, 18, 0, 180, 14), lw=0.9, fill=Wt, amp=0)
    k.text(440, 160, "cloth", size=7, font="Ink-Kalam")
    k.rect(200, 154, 110, 16, lw=1.0, fill=PAL.silver); k.text(255, 136, "tray of clean spoons", size=9, font="Ink-Kalam", color=C(250, 244, 226))

def sill_plate(k, w, h):
    B.plate_open(k, w, h); _room(k, w, h, floor_y=40)
    k.rect(60, 60, 392, 240, lw=1.4, fill=C(240, 236, 226))
    _garden_window(k, 70, 70, 372, 170); k.rect(70, 70, 372, 170, lw=0.9, fill=None)
    k.rect(70, 262, 372, 30, lw=0.9, fill=C(48, 56, 70)); k.rect(40, 52, 432, 14, lw=1.1, fill=MARBLE)
    k.text(256, 310, "the back windowsill, under the gap", size=10, font="Ink-Kalam", color=PAL.navy); k.unclip()

def nest_plate(k, w, h):
    B.plate_open(k, w, h)
    k.vgrad(14, 60, w - 14, h - 14, C(250, 206, 160), C(200, 214, 236), steps=10)   # morning sky
    k.wash_rect(14, 14, w - 14, 60, LAWN); k.line([(14, 60), (w - 14, 60)], lw=0.9, amp=0.1)
    k.rect(240, 60, 30, 170, lw=1.2, fill=BARK)
    with k.tint(BARK): k.hatch([(240, 60), (270, 60), (270, 230), (240, 230)], angle=80, gap=3, lw=0.4)
    for a, b in (((255, 200), (140, 290)), ((255, 220), (380, 300)), ((255, 180), (400, 230))): k.line([a, b], lw=3.0, amp=0.3, color=BARK)
    for cx, cy in ((150, 300), (200, 320), (330, 320), (390, 300), (260, 340)): k.circle(cx, cy, 30, lw=0.8, fill=LEAF)
    for cx, cy in ((160, 296), (214, 314), (340, 330), (380, 290)): k.circle(cx, cy, 4, lw=0.5, fill=C(214, 70, 64))   # apples
    k.unclip()

def board_plate(k, w, h):
    B.plate_open(k, w, h); _room(k, w, h, floor_y=56); k.case_board(24, 66, 464, 292, title="WHO COULD GET IN?")

def tea_plate(k, w, h): B.plate_open(k, w, h); k.tearoom(w, h); k.unclip()

# lineup backdrops
def _bigspoon(k, pw, h):
    _room(k, pw, h, floor_y=50); k.rect(320, 50, 150, 100, lw=1.0, fill=OAK)
    with k.tint(PAL.teapot): k.teapot(360, 150, 40)
    k.line([(420, 150), (470, 190)], lw=3, amp=0, color=PAL.silver); k.circle(472, 192, 8, lw=0.8, fill=PAL.silver)   # the big spoon
def _grocer(k, pw, h):
    k.vgrad(14, 50, pw - 14, h - 14, SKY, SKY2, steps=8); k.stones(14, pw - 14, 14, 50, rows=2)
    k.rect(250, 50, 220, 200, lw=1.1, fill=C(206, 230, 208)); k.rect(260, 210, 200, 28, lw=0.8, fill=C(86, 140, 92))
    k.text(360, 218, "FENWICK GROCER", size=10, font="Ink-Plex", color=C(250, 246, 236))
    for i in range(5): k.circle(280 + i * 40, 80, 12, lw=0.6, fill=[C(214, 70, 64), C(246, 200, 80), C(150, 190, 90), C(230, 140, 60), C(200, 60, 80)][i])
    k.text(360, 150, "open from 5 am", size=9, font="Ink-Kalam", color=PAL.navy)
def _bed(k, pw, h):
    _room(k, pw, h, floor_y=50); k.rect(300, 50, 180, 50, lw=1.0, fill=C(236, 214, 230)); k.rect(300, 100, 40, 50, lw=1.0, fill=OAK)
    k.shape(k.arcpts(360, 100, 50, 14, 0, 180, 12), lw=0.8, fill=C(250, 246, 236), amp=0)
    k.vgrad(380, 200, 470, 300, C(40, 50, 90), C(80, 90, 140), steps=6); k.rect(380, 200, 90, 100, lw=1.0, fill=None)   # night window
    k.circle(440, 270, 8, lw=0, fill=C(250, 240, 200), stroke=False)

def apply(A):
    A._sideboard = _sideboard; A.sill_plate = sill_plate; A.nest_plate = nest_plate; A.board_plate = board_plate; A.tea_plate = tea_plate
    A.lineup_plate = B.lineup_plate_fn([_bigspoon, _grocer, _bed], [n for n, _ in A.CAST])
