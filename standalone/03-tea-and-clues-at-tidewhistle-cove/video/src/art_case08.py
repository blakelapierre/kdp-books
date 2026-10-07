"""Illustrations for Case 8, The Four Bakers: colour-detailed + animation layers (anim.py).
PART sprites use part_open (clip only) — never frame2 — so no border is baked into a moving sprite.
Unique open (render.py HOOK_STYLE="statements"): borderless full-bleed hero of the EMPTY tray (twelve flour rings)
under a chalkboard title, then a 2x2 grid of the four suspects whose speech bubbles pop up, and a "ONLY 1 IS TRUE"
stamp — a logic-puzzle preview, not the Case 6/7 banner + cast-strip template. Cinnamon / slate palette.
The four suspects share one stance, arm pose, head size, neutral face and colour weight everywhere before the
solution; Mr Fenwick is only sheepish in the confession scene.
Run: python3 art_case08.py [scene ...]"""
import math, os, sys, random
from functools import partial
import colorink
colorink.set_style("color-detailed")
import art_case04 as A4
colorink.set_style("color-detailed")
from inkart import lerp, K, Wt
from colorink import PAL, C, shade, mix
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import people4 as P4
from art import nameplate
from layers import save_layers

_fonts = os.environ.get("TIDEWHISTLE_FONTS", "/usr/share/fonts/truetype/sand-box/google/").rstrip("/") + "/"
pdfmetrics.registerFont(TTFont("Ink-Kalam", _fonts + "Kalam/Kalam-Bold.ttf"))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-08")

# ----------------------------------------------------------------------------- bakery palette (cinnamon / slate)
BRICK = C(214, 168, 130); BRICK2 = C(190, 140, 104); MORTAR = C(236, 220, 196)
DOOR = C(70, 112, 140); DOOR2 = C(52, 88, 114); COBBLE = C(176, 168, 156); COBBLE2 = C(150, 142, 132)
BUN = C(206, 138, 70); BUN2 = C(160, 96, 46); GLAZE = C(252, 246, 232); TRAY = C(150, 152, 160); TRAY2 = C(118, 120, 130)
FLOUR = C(246, 240, 226); WIRE = C(90, 92, 100); SLATE = C(46, 58, 60); SLATE2 = C(36, 46, 48)
CHALK = C(244, 240, 228); CHALK_Y = C(246, 218, 120); CHALK_R = C(240, 140, 128); CHALK_G = C(160, 220, 170)
SKY = C(196, 224, 236); SKY2 = C(160, 202, 222); SHOPWALL = C(250, 236, 206); SHELF = PAL.wood
CARD = C(250, 242, 226); CARD_EDGE = C(184, 110, 60)

class Ink8(A4.Ink4):
    def brick_wall(s, x0, y0, x1, y1):
        s.wash_rect(x0, y0, x1, y1, BRICK)
        rr = random.Random(int(x0 * 7 + y0)); row = 0; y = y0
        while y < y1:
            off = 0 if row % 2 == 0 else 13
            s.line([(x0, y), (x1, y)], lw=0.35, amp=0, color=MORTAR)
            x = x0 + off
            while x < x1:
                s.line([(x, y), (x, min(y1, y + 10))], lw=0.3, amp=0, color=MORTAR)
                if rr.random() < 0.18: s.wash_rect(x + 1, y + 1, min(x1, x + 25), min(y1, y + 9), BRICK2)
                x += 26
            y += 10; row += 1

    def cobbles(s, x0, y0, x1, y1):
        s.wash_rect(x0, y0, x1, y1, COBBLE)
        rr = random.Random(int(x0 + y1))
        for j in range(int((y1 - y0) / 9) + 1):
            for i in range(int((x1 - x0) / 14) + 1):
                cx = x0 + i * 14 + (7 if j % 2 else 0) + rr.uniform(-1, 1); cy = y0 + j * 9 + 4
                if cx < x1 and cy < y1:
                    s.shape(s.arcpts(cx, cy, 6.2, 3.6, 0, 360, 10), lw=0.35, fill=COBBLE2 if rr.random() < 0.3 else COBBLE, amp=0.15)

    def back_door(s, x, y, w, h, sign=True):
        s.rect(x - 4, y, w + 8, h + 6, lw=1.0, fill=C(236, 226, 206))
        s.rect(x, y, w, h, lw=1.2, fill=DOOR)
        for (px, py, pw, ph) in ((0.14, 0.56, 0.72, 0.34), (0.14, 0.1, 0.72, 0.38)):
            s.rect(x + w * px, y + h * py, w * pw, h * ph, lw=0.6, fill=DOOR2)
        s.circle(x + w * 0.84, y + h * 0.5, 2.6, lw=0.5, fill=PAL.brass)
        s.rect(x - 8, y - 6, w + 16, 6, lw=0.8, fill=C(170, 160, 150))   # step
        if sign:
            s.rect(x - 14, y + h + 12, w + 28, 22, lw=0.9, fill=CARD)
            s.text(x + w / 2, y + h + 18, "PENHALLOW'S BAKERY", size=7.4, font="Ink-Plex", color=CARD_EDGE)

    def rack(s, x, y, w, h, shelves=3):
        """Wire cooling rack on legs (y = floor)."""
        for u in (0, 1):
            s.line([(x + u * w, y), (x + u * w, y + h)], lw=1.6, amp=0, color=WIRE)
        for j in range(shelves):
            yy = y + h * (0.35 + 0.3 * j)
            s.line([(x, yy), (x + w, yy)], lw=1.1, amp=0, color=WIRE)
            for i in range(1, 12):
                s.line([(x + i * w / 12, yy - 1.2), (x + i * w / 12, yy + 1.2)], lw=0.3, amp=0, color=WIRE)
        return y + h * (0.35 + 0.3 * (shelves - 1))   # top shelf height

    def tray(s, x, y, w, rings=True):
        """Baking tray (x = left, y = bottom). rings=True: twelve flour rings where the buns sat."""
        d = w * 0.62
        s.shape([(x, y), (x + w, y), (x + w - 4, y + 7), (x + 4, y + 7)], lw=0.9, fill=TRAY, amp=0)
        s.shape([(x + 4, y + 7), (x + w - 4, y + 7), (x + w - 10, y + d * 0.5), (x + 10, y + d * 0.5)], lw=0.8, fill=shade(TRAY, 1.08), amp=0)
        if rings:   # pale flour rings + dusting where the twelve buns sat
            rr0 = random.Random(int(w))
            for (bx, by, r) in s.bun_spots(x, y, w):
                s.line(s.arcpts(bx, by, r * 0.92, r * 0.5, 0, 360, 22), lw=max(0.8, r * 0.09), amp=0.05, color=FLOUR)
                for i in range(5):
                    a = rr0.uniform(0, 6.28); q = rr0.uniform(0.2, 0.8)
                    s.circle(bx + math.cos(a) * r * q, by + math.sin(a) * r * 0.45 * q, max(0.35, r * 0.04), lw=0, fill=FLOUR, stroke=False)
            rr = random.Random(int(x))
            for i in range(9):
                s.circle(x + rr.uniform(10, w - 10), y + 8 + rr.uniform(0, d * 0.3), rr.uniform(0.6, 1.4), lw=0, fill=BUN2, stroke=False)

    def bun_spots(s, x, y, w):
        """Twelve spots, BACK row first so front buns overlap the ones behind."""
        d = w * 0.62; out = []; r = (w - 28) / 10.0
        for j in (2, 1, 0):
            for i in range(4):
                bx = x + 14 + (w - 28) * (i + 0.5) / 4 + (j - 1) * 1.5
                by = y + 7 + r * 0.55 + (d * 0.5 - 7 - r * 1.2) * j / 2
                out.append((bx, by, r))
        return out

    def bun(s, x, y, r):
        s.shape(s.arcpts(x, y + r * 0.2, r, r * 0.62, 0, 360, 20), lw=0.7, fill=BUN, amp=0.1)
        pts = [(x + math.cos(a) * r * (a / 13.0) * 0.95, y + r * 0.28 + math.sin(a) * r * 0.55 * (a / 13.0)) for a in [i * 0.45 for i in range(2, 29)]]
        s.line(pts, lw=0.55, amp=0, color=BUN2)
        s.line([(x - r * 0.6, y + r * 0.45), (x - r * 0.1, y + r * 0.6), (x + r * 0.5, y + r * 0.35)], lw=0.9, amp=0.2, color=GLAZE)

    def chalkboard(s, x, y, w, h, frame=True):
        s.rect(x, y, w, h, lw=1.4, fill=SLATE)
        rr = random.Random(int(x + w))
        for i in range(40):
            px = x + rr.uniform(6, w - 6); py = y + rr.uniform(6, h - 6)
            s.line([(px, py), (px + rr.uniform(4, 14), py + rr.uniform(-1, 1))], lw=0.3, amp=0, color=SLATE2)
        if frame: s.rect(x - 5, y - 5, w + 10, h + 10, lw=1.0, fill=None); s.rect(x - 2, y - 2, w + 4, h + 4, lw=2.2, fill=None)

# ============================================================================= open helpers
def plate_open(k, w, h):
    k.frame2(w, h); k.clip_rect(14, 14, w - 14, h - 14)

def part_open(k, w, h):
    """Clip only — no frame2 (a border baked into a moving sprite rotates and leaves line artifacts)."""
    k.clip_rect(14, 14, w - 14, h - 14)

def full_open(k, w, h):
    k.clip_rect(0, 0, w, h)

gull_fx = A4.gull_fx; steam_fx = A4.steam_fx

# ----------------------------------------------------------------------------- 1. HOOK hero: the empty tray (full bleed, no frame)
def _hook_scene(k, w, h):
    k.brick_wall(0, 80, w, h)
    k.back_door(26, 80, 92, 190, sign=False)
    k.cobbles(0, 0, w, 80)
    top = k.rack(160, 40, 310, 160, shelves=3)
    k.tray(176, top + 1, 278, rings=True)
    # tag on the rack: what should be there
    k.rect(396, 96, 74, 34, lw=0.9, fill=CARD)
    k.text(433, 116, "12 BUNS", size=9, font="Ink-Plex", color=CARD_EDGE)
    k.text(433, 102, "Saturday", size=8, font="Ink-Kalam", color=C(90, 70, 60))
    rr = random.Random(4)   # a few crumbs on the cobbles (no direction, no tell)
    for i in range(14): k.circle(rr.uniform(200, 470), rr.uniform(12, 60), rr.uniform(0.8, 1.6), lw=0, fill=BUN2, stroke=False)

def hook_plate(k, w, h):
    full_open(k, w, h); _hook_scene(k, w, h); k.unclip()

# ----------------------------------------------------------------------------- 2. HOOK grid: four suspects, equal cards (render adds bubbles)
GW, GH = 720, 540
def _fig(k, who, x, y, h, **kw):
    """One call for every suspect: same props rule for all four (each holds one small everyday thing)."""
    if who == "fenwick": kw.setdefault("prop", "apple")
    getattr(P4, who)(k, x, y, h, **kw)
GRID = ["pip", "demelza", "fenwick", "kerensa"]
GNAMES = ["PIP CAREW", "DEMELZA ROWE", "MR FENWICK", "KERENSA HALE"]
def _fx(i):
    """Figure x as a fraction of its cell: left column at 0.3, right column mirrored at 0.7, so the
    centre of the grid (bubbles + the ONLY 1 IS TRUE stamp) never covers any suspect."""
    return 0.3 if i % 2 == 0 else 0.7

def _cell(i):
    col, row = i % 2, i // 2
    cw, ch = GW / 2, GH / 2
    return col * cw, GH - (row + 1) * ch, cw, ch     # x0, y0 (bottom), w, h  in pt

def grid_plate(k, w, h):
    k.wash_rect(0, 0, w, h, C(247, 240, 225))
    for i in range(4):
        x0, y0, cw, ch = _cell(i)
        k.shape([(x0 + 10, y0 + 10), (x0 + cw - 10, y0 + 10), (x0 + cw - 10, y0 + ch - 10), (x0 + 10, y0 + ch - 10)], lw=1.4, fill=CARD, amp=0)
        k.wash_rect(x0 + 12, y0 + 12, x0 + cw - 12, y0 + 52, C(232, 214, 186))   # same floor strip for all four
        nameplate(k, x0 + cw * _fx(i), y0 + 22, GNAMES[i], size=11)

def grid_fig(k, w, h, v, i=0, who="pip"):
    x0, y0, cw, ch = _cell(i)
    k.c.saveState(); k.clip_rect(x0 + 12, y0 + 12, x0 + cw - 12, y0 + ch - 12)
    _fig(k, who, x0 + cw * _fx(i), y0 + 44, ch * 0.78)
    k.c.restoreState()

# ----------------------------------------------------------------------------- 3. bakery back door with the tray of twelve
def bakery_plate(k, w, h):
    plate_open(k, w, h)
    k.vgrad(14, 300, w - 14, h - 14, SKY, SKY2, steps=8)
    k.brick_wall(14, 96, w - 14, 300)
    k.roof(10, w - 10, 300, 360, overhang=8, color=C(120, 70, 56))
    k.back_door(70, 96, 92, 170)
    k.window(220, 200, 70, 60)
    k.cobbles(14, 14, w - 14, 96)
    top = k.rack(300, 60, 170, 140, shelves=3)
    k.tray(312, top + 1, 146, rings=True)       # buns are a part on top (hidden once the tray is gone)
    k.unclip()

def buns_part(k, w, h, v):
    part_open(k, w, h)
    top = 60 + 140 * (0.35 + 0.3 * 2)
    for (bx, by, r) in k.bun_spots(312, top + 1, 146): k.bun(bx, by, r)
    k.unclip()

# ----------------------------------------------------------------------------- 4. shop front: Jago serving
def front_plate(k, w, h):
    plate_open(k, w, h)
    k.wash_rect(14, 14, w - 14, h - 14, SHOPWALL)
    k.vgrad(14, 14, w - 14, 70, PAL.floor, PAL.floor2, steps=6)
    for j in range(3):   # bread shelves
        y = 190 + j * 50; k.rect(40, y, 260, 6, lw=0.8, fill=SHELF)
        for i in range(7):
            with k.tint(C(210, 160, 96)): k.shape(k.arcpts(62 + i * 36, y + 16, 14, 9, 0, 180, 12) + [(48 + i * 36, y + 7)], lw=0.6, amp=0.1)
    k.rect(330, 170, 150, 150, lw=1.0, fill=SKY)   # shop window, lettering reversed is not needed
    k.line([(405, 170), (405, 320)], lw=1.0, amp=0); k.text(405, 296, "PENHALLOW'S", size=10, font="Ink-Plex", color=CARD_EDGE)
    k.rect(30, 70, 330, 64, lw=1.1, fill=PAL.wood)   # counter
    with k.tint(PAL.wood): k.hatch([(30, 70), (360, 70), (360, 134), (30, 134)], angle=0, gap=2.6, lw=0.3)
    k.rect(24, 134, 342, 8, lw=0.9, fill=PAL.wood_dk)
    for i in range(3): k.bun(80 + i * 34, 150, 11)   # a few buns at the counter (for sale)
    k.unclip()

def jago_front(k, w, h, v): part_open(k, w, h); P4.jago(k, 220, 96, 200, expr="smile", prop=False); k.unclip()
def customer_front(k, w, h, v): part_open(k, w, h); P4.vicar(k, 420, 30, 214); k.unclip()

# ----------------------------------------------------------------------------- 5. the back lane: four people pass the back door
def lane_plate(k, w, h):
    plate_open(k, w, h)
    k.vgrad(14, 300, w - 14, h - 14, SKY, SKY2, steps=8)
    k.brick_wall(14, 110, w - 14, 300)
    k.back_door(30, 110, 80, 160)
    top = k.rack(124, 80, 90, 120, shelves=3)
    k.tray(130, top + 1, 78, rings=True)
    k.cobbles(14, 14, w - 14, 110)
    k.unclip()

LANE_X = dict(pip=236, demelza=312, fenwick=388, kerensa=464)
def lane_fig(k, w, h, v, who="pip"):
    part_open(k, w, h); _fig(k, who, LANE_X[who], 30, 184); k.unclip()

# ----------------------------------------------------------------------------- 6. Kettle and Gull: Jago marches all four in
def tearoom_plate(k, w, h):
    plate_open(k, w, h)
    A4._tearoom(k, w, h)
    for i, who in enumerate(GRID):   # all four, small and identical in treatment, waiting by the counter
        _fig(k, who, 214 + i * 46, 26, 124)
    k.unclip()

def jago_tea(k, w, h, v):
    part_open(k, w, h); P4.jago(k, 104, 22, 236, expr="cross", prop=False); k.unclip()
def agnes_tea(k, w, h, v):
    part_open(k, w, h); P4.agnes(k, 440, 22, 220, basket=False); k.unclip()

# ----------------------------------------------------------------------------- 7. lineup: same tea-room backdrop for all four
PW = 512
def lineup_plate(k, w, h):
    for i in range(4):
        k.c.saveState(); k.c.translate(i * PW, 0)
        k.frame2(PW, h); k.clip_rect(14, 14, PW - 14, h - 14)
        A4._tearoom(k, PW, h)
        nameplate(k, PW / 2, 40, GNAMES[i])
        k.unclip(); k.c.restoreState()

def lineup_fig(k, w, h, v, i=0, who="pip"):
    k.c.saveState(); k.c.translate(i * PW, 0); k.clip_rect(14, 14, PW - 14, h - 14)
    _fig(k, who, PW / 2 - 46, 70, 236)
    k.unclip(); k.c.restoreState()

# ----------------------------------------------------------------------------- 8. Agnes raises an eyebrow (window table)
def agnes_plate(k, w, h):
    plate_open(k, w, h)
    k.wash_rect(14, 14, w - 14, h - 14, A4.TEAWALL)
    k.vgrad(14, 14, w - 14, 80, PAL.floor, PAL.floor2, steps=6)
    k.rect(250, 150, 200, 170, lw=1.2, fill=SKY)
    k.vgrad(252, 152, 448, 220, A4.SEA, A4.SEA2, steps=6)
    k.line([(350, 150), (350, 320)], lw=1.2, amp=0); k.line([(250, 235), (450, 235)], lw=1.2, amp=0)
    k.rect(240, 80, 230, 12, lw=1.0, fill=PAL.wood)   # table top
    for u in (260, 450): k.line([(u, 20), (u, 80)], lw=2.0, amp=0, color=PAL.wood_dk)
    with k.tint(PAL.teapot): k.teapot(300, 92, 40)
    with k.tint(PAL.walls[2]): k.cup(400, 92, 22)
    k.unclip()

def agnes_eye(k, w, h, v): part_open(k, w, h); P4.agnes(k, 130, 22, 240, expr="eyebrow", basket=False); k.unclip()

# ----------------------------------------------------------------------------- 9. the statement board (recap + solution chalk marks)
ROWS = [("PIP:", "\u201cDemelza took them.\u201d"), ("DEMELZA:", "\u201cKerensa took them.\u201d"),
        ("MR FENWICK:", "\u201cI didn't take them.\u201d"), ("KERENSA:", "\u201cDemelza is lying.\u201d")]
ROW_Y = [252, 206, 160, 114]
BX0, BY0, BX1, BY1 = 34, 40, 478, 346
def board_plate(k, w, h):
    plate_open(k, w, h)
    k.wash_rect(14, 14, w - 14, h - 14, A4.TEAWALL)
    k.chalkboard(BX0, BY0, BX1 - BX0, BY1 - BY0)
    k.text(256, 306, "WHO SAID WHAT?", size=20, font="Ink-Playfair", color=CHALK_Y)
    k.line([(150, 298), (362, 298)], lw=0.8, amp=0.3, color=CHALK)
    for (nm, st), y in zip(ROWS, ROW_Y):
        k.text(64, y, nm, size=13, font="Ink-Plex", align="l", color=CHALK_Y)
        k.text(186, y - 1, st, size=17, font="Ink-Kalam", align="l", color=CHALK)
    k.line([(60, 92), (452, 92)], lw=0.6, amp=0.3, color=CHALK)
    k.text(256, 62, "Exactly ONE of them is telling the truth.", size=14, font="Ink-Kalam", color=CHALK_G)
    k.unclip()

def _chalk_x(k, x, y, s=9):
    k.line([(x - s, y - s), (x + s, y + s)], lw=2.2, amp=0.4, color=CHALK_R)
    k.line([(x - s, y + s), (x + s, y - s)], lw=2.2, amp=0.4, color=CHALK_R)

def mark_x(k, w, h, v, row=0):
    part_open(k, w, h); _chalk_x(k, 50, ROW_Y[row] + 5); k.unclip()

def mark_tick(k, w, h, v, row=3):
    part_open(k, w, h)
    y = ROW_Y[row] + 5
    k.line([(40, y), (48, y - 8), (62, y + 12)], lw=2.4, amp=0.3, color=CHALK_G); k.unclip()

def mark_circle(k, w, h, v, row=2):
    part_open(k, w, h)
    y = ROW_Y[row] + 5
    k.c.setStrokeColor(CHALK_R); k.c.setLineWidth(2.0); k.c.ellipse(56, y - 13, 178, y + 17, stroke=1, fill=0)
    k.unclip()

def mark_pair(k, w, h, v):
    """Yellow underlines on Demelza's and Kerensa's lines (not adjacent, so no bracket across Fenwick's row)."""
    part_open(k, w, h)
    for row in (1, 3):
        y = ROW_Y[row] - 6
        k.line([(186 + i * 10, y + (0.9 if i % 2 else -0.9)) for i in range(23)], lw=1.6, amp=0.2, color=CHALK_Y)
        k.text(446, ROW_Y[row] + 1, "?", size=16, font="Ink-Kalam", color=CHALK_Y)
    k.unclip()

def mark_pair_lbl(k, w, h, v):
    part_open(k, w, h)
    k.text(452, ROW_Y[3] - 22, "exactly one of these two is true", size=10, font="Ink-Kalam", align="r", color=CHALK_Y)
    k.unclip()

# ----------------------------------------------------------------------------- 10. confession at the back door (after the solution only)
def confess_plate(k, w, h):
    plate_open(k, w, h)
    k.vgrad(14, 300, w - 14, h - 14, SKY, SKY2, steps=8)
    k.brick_wall(14, 96, w - 14, 300)
    k.roof(10, w - 10, 300, 360, overhang=8, color=C(120, 70, 56))
    k.back_door(214, 96, 84, 160)
    k.cobbles(14, 14, w - 14, 96)
    top = k.rack(320, 60, 150, 130, shelves=3)
    k.tray(330, top + 1, 130, rings=False)
    for (bx, by, r) in k.bun_spots(330, top + 1, 130)[1:]: k.bun(bx, by, r)   # eleven back; one "studied"
    # a little notebook on the step: "recipe?"
    k.shape([(166, 40), (210, 43), (208, 64), (164, 61)], lw=0.8, fill=CARD, amp=0)
    k.text(187, 48, "recipe?", size=9, font="Ink-Kalam", color=C(80, 70, 60))
    k.unclip()

def fenwick_conf(k, w, h, v):
    part_open(k, w, h); P4.fenwick(k, 120, 26, 230, expr="sheepish" if "sheepish" in v else "neutral", prop=False); k.unclip()
def jago_conf(k, w, h, v):
    part_open(k, w, h); P4.jago(k, 268, 30, 222, expr="smile", prop=False, flip=True); k.unclip()

# ----------------------------------------------------------------------------- vignette (title + end card; no suspects, no spoiler)
def vignette(k, w, h):
    k.circle(w / 2, h / 2, w * 0.46, lw=1.5, fill=C(240, 214, 176)); k.circle(w / 2, h / 2, w * 0.44, lw=0.5, fill=None)
    for i in range(24):
        a = 2 * math.pi * i / 24
        k.circle(w / 2 + w * 0.46 * math.cos(a), h / 2 + w * 0.46 * math.sin(a), 3.5, lw=0, fill=C(247, 240, 225), stroke=False)
    k.c.saveState(); p = k.c.beginPath(); p.circle(w / 2, h / 2, w * 0.44 - 1); k.c.clipPath(p, stroke=0, fill=0)
    k.wash_rect(0, 0, w, h, SHOPWALL); k.wash_rect(0, 0, w, h * 0.34, PAL.wood)
    k.tray(w * 0.16, h * 0.3, w * 0.68, rings=False)
    for (bx, by, r) in k.bun_spots(w * 0.16, h * 0.3, w * 0.68): k.bun(bx, by, r)
    for i, dx in enumerate((-0.12, 0.0, 0.12)):
        k.line([(w * (0.5 + dx) + 4 * math.sin(t * 6 + i), h * 0.62 + t * h * 0.2) for t in [j / 10 for j in range(11)]], lw=1.4, amp=0, color=C(255, 255, 255))
    with k.tint(PAL.walls[2]): k.cup(w * 0.82, h * 0.31, 30)
    k.c.restoreState()

# ============================================================================= jobs
AW, AH = 512, 384
V3 = ["base", "base+blink", "base+talk"]; V2 = ["base", "base+blink"]
FX = dict(gull=dict(fn=gull_fx, variants=["f0", "f1", "f2", "f3"], page=(44, 22)))
STEAM = dict(steam=dict(fn=steam_fx, variants=["s0", "s1", "s2"], page=(12, 22)))

def jobs():
    J = []
    J.append(dict(name="hook", w=AW, h=AH, plate=hook_plate, seed=81, parts=dict(**FX)))
    J.append(dict(name="grid", w=GW, h=GH, plate=grid_plate, seed=82, parts={
        who: dict(fn=partial(grid_fig, i=i, who=who), variants=V2) for i, who in enumerate(GRID)}))
    J.append(dict(name="bakery", w=AW, h=AH, plate=bakery_plate, seed=83, parts=dict(
        buns=dict(fn=buns_part, variants=["base"]), **FX, **STEAM)))
    J.append(dict(name="front", w=AW, h=AH, plate=front_plate, seed=84, parts=dict(
        jago=dict(fn=jago_front, variants=V2), customer=dict(fn=customer_front, variants=V2))))
    J.append(dict(name="lane", w=AW, h=AH, plate=lane_plate, seed=85, parts=dict(
        **{who: dict(fn=partial(lane_fig, who=who), variants=V2) for who in GRID}, **FX)))
    J.append(dict(name="tearoom", w=AW, h=AH, plate=tearoom_plate, seed=86, parts=dict(
        jago=dict(fn=jago_tea, variants=V3), agnes=dict(fn=agnes_tea, variants=V2))))
    J.append(dict(name="lineup", w=4 * PW, h=AH, plate=lineup_plate, seed=87, parts={
        who: dict(fn=partial(lineup_fig, i=i, who=who), variants=V3) for i, who in enumerate(GRID)}))
    J.append(dict(name="agnes", w=AW, h=AH, plate=agnes_plate, seed=88, parts=dict(
        agnes=dict(fn=agnes_eye, variants=V2), **STEAM)))
    J.append(dict(name="board", w=AW, h=AH, plate=board_plate, seed=89, parts=dict(
        pair=dict(fn=mark_pair, variants=["base"]),
        pair_lbl=dict(fn=mark_pair_lbl, variants=["base"]),
        x_pip=dict(fn=partial(mark_x, row=0), variants=["base"]),
        x_fen=dict(fn=partial(mark_x, row=2), variants=["base"]),
        x_dem=dict(fn=partial(mark_x, row=1), variants=["base"]),
        circle_fen=dict(fn=partial(mark_circle, row=2), variants=["base"]),
        tick_ker=dict(fn=partial(mark_tick, row=3), variants=["base"]))))
    J.append(dict(name="confess", w=AW, h=AH, plate=confess_plate, seed=90, parts=dict(
        fenwick=dict(fn=fenwick_conf, variants=["sheepish", "sheepish+blink"]),
        jago=dict(fn=jago_conf, variants=V3), **FX)))
    J.append(dict(name="vignette", w=384, h=384, plate=vignette, seed=91))
    return J

def make_ink(c, seed): return Ink8(c, seed=seed)

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    J = [j for j in jobs() if not want or j["name"] in want]
    save_layers(OUT, J, make_ink)
