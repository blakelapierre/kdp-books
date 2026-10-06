"""Illustrations for Case 6, The Closed Post Office: colour-detailed + animation layers.
PART sprites use part_open (clip only) — never frame2 — so borders are not baked into rotating/bobbing sprites.
Unique hook: extreme close-up of the CLOSED post-office door + striped blind + puffin blanket (not the usual empty-crime-scene + cast formula).
Run: python3 art_case06.py [scene ...]"""
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

pdfmetrics.registerFont(TTFont("Ink-Kalam", "/usr/share/fonts/truetype/sand-box/google/Kalam/Kalam-Bold.ttf"))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-06")

# ----------------------------------------------------------------------------- Sunday / post-office palette (distinct from allotment greens of case 5)
SKY = C(255, 214, 168); SKY2 = C(255, 186, 140)          # warm Sunday-morning gold
COBBLE = C(196, 184, 168); COBBLE2 = C(176, 164, 148)
PO_WALL = C(236, 220, 196); PO_SIGN = C(140, 42, 48); PO_DOOR = C(92, 64, 48)
BLIND = C(214, 198, 160); BLIND2 = C(170, 150, 110)
BLANKET = C(176, 210, 230); BLANKET2 = C(150, 186, 210)
CHURCH = C(214, 206, 190); BAKERY = C(250, 236, 210); INN = C(196, 150, 110)
PAPER = C(214, 186, 140); GRASS = C(176, 206, 140)

class Ink6(A4.Ink4):
    def sunday_sky(s, w, h, y_horizon=210):
        s.vgrad(14, y_horizon, w - 14, h - 14, SKY, SKY2, steps=16)
        # soft sun disc
        s.circle(w * 0.78, h * 0.72, 28, lw=0, fill=C(255, 236, 180), stroke=False)
        s.circle(w * 0.78, h * 0.72, 18, lw=0, fill=C(255, 250, 220), stroke=False)

    def cobbles(s, w, h, y_top=90):
        s.wash_rect(14, 14, w - 14, y_top, COBBLE)
        rr = random.Random(9)
        for j in range(5):
            yy = 20 + j * 14
            for i in range(22):
                cx = 22 + i * 22 + (j % 2) * 11
                col = mix(COBBLE, Wt if rr.random() < 0.5 else K, rr.uniform(0.04, 0.14))
                s.shape(s.arcpts(cx, yy, 8, 4, 0, 360, 10), lw=0.35, fill=col, amp=0.2)

    def post_office(s, x, y, w, h, closed=True, blind=True):
        """Village post office: red sign, door with CLOSED plaque, striped blind in the window."""
        s.wall(x, y, w, h * 0.72, gap=3.0, color=PO_WALL)
        s.roof(x, x + w, y + h * 0.72, y + h, overhang=10, color=PAL.slate)
        # cornice / sign board
        s.rect(x + w * 0.06, y + h * 0.52, w * 0.88, h * 0.14, lw=1.0, fill=PO_SIGN)
        s.text(x + w / 2, y + h * 0.555, "POST OFFICE", size=h * 0.07, font="Ink-Playfair", color=C(250, 230, 180))
        # window
        wx, wy, ww, wh = x + w * 0.1, y + h * 0.14, w * 0.48, h * 0.32
        s.rect(wx - 3, wy - 3, ww + 6, wh + 6, lw=1.0, fill=PO_SIGN)
        if blind:
            s.rect(wx, wy, ww, wh, lw=0.8, fill=BLIND)
            for i in range(9):
                yy = wy + 3 + i * (wh - 6) / 8
                s.line([(wx + 2, yy), (wx + ww - 2, yy)], lw=1.4 if i % 2 == 0 else 0.5, amp=0,
                       color=BLIND2 if i % 2 == 0 else shade(BLIND, 0.92))
        else:
            s.rect(wx, wy, ww, wh, lw=0.8, fill=C(255, 240, 200))
            # craft counter yarn balls visible when open
            for i, col in enumerate([C(226, 108, 120), BLANKET, C(244, 200, 80), C(120, 160, 200)]):
                s.circle(wx + 18 + i * 28, wy + wh * 0.35, 9, lw=0.5, fill=col)
        # door
        dx, dw = x + w * 0.64, w * 0.26
        s.rect(dx - 3, y, dw + 6, h * 0.52, lw=0.9, fill=PO_SIGN)
        s.rect(dx, y, dw, h * 0.5, lw=1.0, fill=PO_DOOR)
        s.rect(dx + dw * 0.15, y + h * 0.28, dw * 0.7, h * 0.16, lw=0.6, fill=C(200, 180, 150) if closed else C(255, 236, 190))
        s.circle(dx + dw * 0.8, y + h * 0.22, 2.0, lw=0.4, fill=PAL.brass)
        # CLOSED / OPEN plaque
        px, py, pw, ph = dx + dw * 0.12, y + h * 0.06, dw * 0.76, h * 0.1
        s.rect(px, py, pw, ph, lw=0.8, fill=C(250, 244, 230) if closed else C(210, 240, 210))
        s.text(dx + dw / 2, py + ph * 0.28, "CLOSED" if closed else "OPEN", size=h * 0.055, font="Ink-Plex",
               color=PO_SIGN if closed else C(40, 100, 60))

    def church6(s, x, y, w, h):
        s.rect(x, y, w * 0.7, h * 0.7, lw=1.0, fill=CHURCH)
        with s.tint(CHURCH, hatch=shade(CHURCH, 0.8)):
            s.hatch([(x, y), (x + w * 0.7, y), (x + w * 0.7, y + h * 0.7), (x, y + h * 0.7)], angle=0, gap=5, lw=0.3)
        s.roof(x, x + w * 0.7, y + h * 0.7, y + h * 0.95, overhang=5, color=PAL.slate)
        # tower + bell
        s.rect(x - w * 0.18, y, w * 0.22, h * 0.95, lw=1.0, fill=CHURCH)
        s.window(x - w * 0.12, y + h * 0.55, w * 0.1, h * 0.18, arch=True)
        s.circle(x - w * 0.07, y + h * 0.78, w * 0.06, lw=0.6, fill=PAL.brass)  # bell hint
        s.window(x + w * 0.25, y + h * 0.35, w * 0.14, h * 0.22, arch=True)

    def bakery6(s, x, y, w, h):
        s.wall(x, y, w, h * 0.7, gap=2.8, color=BAKERY)
        s.roof(x, x + w, y + h * 0.7, y + h, overhang=8, color=C(180, 90, 70))
        s.rect(x + w * 0.1, y + h * 0.5, w * 0.8, h * 0.14, lw=0.9, fill=C(140, 60, 50))
        s.text(x + w / 2, y + h * 0.53, "JAGO'S BAKERY", size=h * 0.055, font="Ink-Plex", color=C(250, 230, 180))
        s.rect(x + w * 0.12, y + h * 0.12, w * 0.5, h * 0.32, lw=0.9, fill=C(255, 240, 210))
        for i in range(4):
            s.shape(s.arcpts(x + w * 0.22 + i * w * 0.1, y + h * 0.28, 7, 5, 0, 180, 8) +
                    [(x + w * 0.22 + i * w * 0.1 - 7, y + h * 0.28)], lw=0.5, fill=C(226, 178, 112), amp=0)
        s.rect(x + w * 0.68, y, w * 0.22, h * 0.48, lw=0.9, fill=C(160, 100, 70))

    def kettle_gull(s, x, y, w, h):
        s.wall(x, y, w, h * 0.7, gap=2.8, color=C(250, 238, 214))
        s.roof(x, x + w, y + h * 0.7, y + h, overhang=8, color=PAL.slate)
        s.rect(x + w * 0.08, y + h * 0.5, w * 0.84, h * 0.14, lw=0.9, fill=C(40, 70, 90))
        s.text(x + w / 2, y + h * 0.535, "THE KETTLE & GULL", size=h * 0.05, font="Ink-Plex", color=C(250, 230, 180))
        s.rect(x + w * 0.12, y + h * 0.14, w * 0.4, h * 0.3, lw=0.8, fill=PAL.sky)
        s.rect(x + w * 0.6, y, w * 0.25, h * 0.48, lw=0.9, fill=C(120, 80, 60))

    def porch_bench(s, x, y, w):
        for u in (-0.46, 0.46):
            s.line([(x + u * w, y), (x + u * w, y + 50)], lw=2.2, amp=0, color=PAL.wood_dk)
        s.rect(x - w / 2 - 2, y + 18, w + 4, 8, lw=0.8, fill=PAL.wood)
        for j in range(2):
            s.rect(x - w / 2, y + 30 + 10 * j, w, 7, lw=0.7, fill=PAL.wood)

    def parcel(s, x, y, w=70, h=36):
        s.rect(x - w / 2, y, w, h, lw=1.0, fill=PAPER)
        s.line([(x - w / 2, y + h / 2), (x + w / 2, y + h / 2)], lw=1.2, amp=0, color=C(140, 70, 60))
        s.line([(x, y), (x, y + h)], lw=1.2, amp=0, color=C(140, 70, 60))
        # puffin peeking from a torn corner
        s.shape([(x + w / 2 - 8, y + 4), (x + w / 2 + 2, y + 4), (x + w / 2 + 2, y + 18), (x + w / 2 - 8, y + 18)],
                lw=0.5, fill=BLANKET, amp=0)
        s.circle(x + w / 2 - 2, y + 12, 4, lw=0.4, fill=C(250, 250, 248))
        s.circle(x + w / 2 - 1, y + 14, 2.2, lw=0.3, fill=C(40, 44, 52))

    def blanket_drape(s, x, y, L=120, fat=48):
        """Pale blue puffin blanket, folded, for prop / hook foreground."""
        pts = [(x, y), (x + L, y + 6), (x + L - 8, y - fat), (x - 10, y - fat - 4)]
        with s.tint(BLANKET, hatch=BLANKET2):
            s.shape(pts, lw=1.1, fill=Wt, amp=0.2)
            s.hatch(pts, angle=16, gap=2.2, lw=0.35)
        for i, px in enumerate([x + 12 + i * 22 for i in range(5)]):
            py = y - fat + 14 + (i % 2) * 3
            s.circle(px, py, 7, lw=0.5, fill=C(250, 250, 248))
            s.circle(px + 1, py + 5, 4.5, lw=0.4, fill=C(40, 44, 52))
            s.circle(px + 2.2, py + 5.5, 1.0, lw=0, fill=Wt, stroke=False)
            s.shape([(px + 4, py + 5), (px + 10, py + 3.5), (px + 4.5, py + 2)], lw=0.4, fill=C(240, 140, 70), amp=0)

# ============================================================================= open helpers (border on plates ONLY)
def plate_open(k, w, h):
    k.frame2(w, h); k.clip_rect(14, 14, w - 14, h - 14)

def part_open(k, w, h):
    """Clip only — no frame2 (avoids Case 4 rotating-border artifact)."""
    k.clip_rect(14, 14, w - 14, h - 14)

# ----------------------------------------------------------------------------- FX
def gull_fx(k, w, h, v):
    up = {"f0": 1.0, "f1": 0.45, "f2": -0.1, "f3": -0.5}[v]; x, y = w / 2, h / 2
    for sg in (-1, 1):
        tip = (x + sg * w * 0.46, y + up * h * 0.4); mid = (x + sg * w * 0.22, y + up * h * 0.25 + h * 0.18)
        k.line([(x + sg * 1.5, y), mid, tip], lw=1.0, amp=0, color=C(60, 64, 72))
    k.shape(k.arcpts(x, y - 0.6, 3.2, 1.6, 0, 360, 12), lw=0.5, fill=PAL.cloud, amp=0)

def leaf_fx(k, w, h, v):
    ph = {"f0": 0, "f1": 0.4, "f2": 0.8}[v]
    k.shape([(2, h / 2), (w * 0.55, h * (0.2 + 0.15 * math.sin(ph * 5))), (w - 2, h / 2),
             (w * 0.55, h * (0.8 - 0.1 * math.sin(ph * 5)))], lw=0.5, fill=PAL.leaf, amp=0)

# ----------------------------------------------------------------------------- 1. UNIQUE HOOK: CLOSED door close-up + blanket
def hook_plate(k, w, h):
    """First-frame hero: striped blind + big CLOSED plaque + craft-counter edge. No empty-shed formula."""
    plate_open(k, w, h)
    # warm dark door wood filling most of the frame
    k.wash_rect(14, 14, w - 14, h - 14, PO_DOOR)
    for i in range(10):
        x = 14 + i * ((w - 28) / 9)
        k.line([(x, 14), (x, h - 14)], lw=0.5, amp=0.15, color=shade(PO_DOOR, 0.85))
    # striped blind (upper half) — diagonal crop for uniqueness
    k.wash_rect(14, h * 0.42, w - 14, h - 14, BLIND)
    for i in range(14):
        yy = h * 0.44 + i * ((h * 0.56 - 28) / 13)
        k.line([(20, yy), (w - 20, yy + 4)], lw=2.2 if i % 2 == 0 else 0.6, amp=0,
               color=BLIND2 if i % 2 == 0 else shade(BLIND, 0.9))
    # giant CLOSED plaque (y-up: higher y = visually higher)
    k.rect(w * 0.14, 36, w * 0.72, 120, lw=2.2, fill=C(250, 244, 230))
    k.rect(w * 0.16, 44, w * 0.68, 104, lw=1.4, fill=None)
    k.text(w / 2, 110, "CLOSED", size=52, font="Ink-Playfair", color=PO_SIGN)
    k.text(w / 2, 55, "—  SUNDAY  —", size=16, font="Ink-Plex", color=shade(PO_SIGN, 0.8))
    # brass handle
    k.circle(w * 0.84, 100, 16, lw=1.0, fill=PAL.brass)
    k.circle(w * 0.84, 100, 7, lw=0.5, fill=shade(PAL.brass, 0.7))
    k.unclip()

def blanket_hook(k, w, h, v):
    part_open(k, w, h); k.blanket_drape(60, 100, L=200, fat=70); k.unclip()

# ----------------------------------------------------------------------------- 2. Sunday street (PO closed at end)
def sunday_plate(k, w, h):
    plate_open(k, w, h)
    k.sunday_sky(w, h, 200)
    k.cobbles(w, h, 90)
    # church left (bells have rung)
    k.church6(40, 100, 120, 200)
    # kettle & gull mid
    k.kettle_gull(180, 90, 140, 170)
    # post office RIGHT, closed, blind down — the visual clue
    k.post_office(340, 80, 160, 210, closed=True, blind=True)
    # "Sunday" postmark stamp floating
    k.circle(100, 320, 36, lw=1.5, fill=None)
    k.circle(100, 320, 30, lw=0.8, fill=None)
    k.text(100, 308, "SUNDAY", size=11, font="Ink-Plex", color=PO_SIGN)
    k.unclip()

def cloud_part(k, w, h, v, x=0, y=0, s_=1.0):
    part_open(k, w, h)
    for (dx, dy, r) in ((0, 0, 16), (16, 4, 13), (-15, 2, 11), (6, 10, 11), (28, -1, 9)):
        k.circle(x + dx * s_, y + dy * s_, r * s_, lw=0, fill=PAL.cloud, stroke=False)
    k.unclip()

# ----------------------------------------------------------------------------- 3. porch with parcel / empty
def porch_plate(k, w, h, empty=False):
    plate_open(k, w, h)
    k.sunday_sky(w, h, 180)
    # cottage wall + porch roof
    k.wall(14, 80, w - 28, 200, gap=3.2, color=C(236, 214, 180))
    k.roof(40, w - 40, 260, 340, overhang=20, color=PAL.slate)
    k.wash_rect(60, 14, w - 60, 90, C(200, 180, 150))  # porch floor
    k.porch_bench(w / 2, 40, 280)
    if not empty:
        pass  # parcel is a part
    else:
        # dashed outline where parcel was
        k.c.setDash(3, 3); k.c.setStrokeColor(C(120, 100, 70)); k.c.setLineWidth(1.2)
        k.c.rect(w / 2 - 40, 55, 80, 40, stroke=1, fill=0); k.c.setDash([])
    k.unclip()

def parcel_part(k, w, h, v):
    part_open(k, w, h); k.parcel(w / 2, 55, w=80, h=40); k.unclip()

def wenna_porch(k, w, h, v):
    part_open(k, w, h); P4.wenna(k, 100, 30, 220, prop=False); k.unclip()

# ----------------------------------------------------------------------------- 4. street meet (alibis)
def street_meet_plate(k, w, h):
    plate_open(k, w, h)
    k.sunday_sky(w, h, 190)
    k.cobbles(w, h, 85)
    k.kettle_gull(30, 90, 160, 180)
    k.bakery6(220, 85, 140, 175)
    k.church6(380, 95, 110, 185)
    k.unclip()

def agnes_meet(k, w, h, v):
    part_open(k, w, h); P4.agnes(k, 80, 28, 200, basket=False); k.unclip()

def wenna_meet(k, w, h, v):
    part_open(k, w, h); P4.wenna(k, 160, 28, 195, prop=False); k.unclip()

def tamsin_meet(k, w, h, v):
    part_open(k, w, h); P4.tamsin(k, 280, 28, 200, prop=None); k.unclip()

def jago_meet(k, w, h, v):
    part_open(k, w, h); P4.jago(k, 380, 28, 200); k.unclip()

# ----------------------------------------------------------------------------- 5. Garland with blanket
def garland_plate(k, w, h):
    plate_open(k, w, h)
    k.sunday_sky(w, h, 180)
    k.cobbles(w, h, 80)
    # inn behind him
    k.wall(280, 90, 200, 180, gap=3.0, color=INN)
    k.roof(280, 480, 270, 340, overhang=10, color=PAL.slate)
    k.rect(300, 250, 160, 30, lw=0.9, fill=C(80, 50, 40))
    k.text(380, 258, "THE ANCHOR INN", size=12, font="Ink-Plex", color=C(250, 230, 180))
    k.window(320, 140, 40, 50); k.window(400, 140, 40, 50)
    k.rect(360, 90, 40, 80, lw=0.9, fill=C(100, 70, 50))
    # PO visible down the street (small, closed)
    k.post_office(40, 120, 90, 120, closed=True, blind=True)
    k.unclip()

def garland_part(k, w, h, v):
    part_open(k, w, h)
    expr = "sheepish" if v.startswith("sheepish") else ("smile" if v.startswith("smile") else "neutral")
    P4.garland(k, 220, 30, 250, expr=expr, prop=not v.startswith("empty"))
    k.unclip()

def agnes_garland(k, w, h, v):
    part_open(k, w, h); P4.agnes(k, 60, 34, 210, basket=False); k.unclip()

def wenna_garland(k, w, h, v):
    part_open(k, w, h); P4.wenna(k, 360, 34, 210, prop=False); k.unclip()

# ----------------------------------------------------------------------------- 6. lineup: Garland | Tamsin | Jago
PW = 512
def _inn_panel(k, pw, h):
    k.sunday_sky(pw, h, 160)
    k.cobbles(pw, h, 70)
    k.wall(60, 90, 200, 160, gap=3.0, color=INN)
    k.roof(60, 260, 250, 310, overhang=8, color=PAL.slate)
    k.text(160, 240, "THE ANCHOR INN", size=11, font="Ink-Plex", color=C(80, 50, 40))

def _church_panel(k, pw, h):
    k.sunday_sky(pw, h, 160)
    k.wash_rect(14, 14, pw - 14, 80, GRASS)
    k.church6(pw * 0.35, 90, 180, 220)

def _bakery_panel(k, pw, h):
    k.sunday_sky(pw, h, 160)
    k.cobbles(pw, h, 70)
    k.bakery6(80, 85, 220, 200)

def lineup_plate(k, w, h):
    names = ["MR GARLAND", "TAMSIN TREVELYAN", "JAGO PENHALLOW"]
    for i in range(3):
        k.c.saveState(); k.c.translate(i * PW, 0); pw = PW
        k.frame2(pw, h); k.clip_rect(14, 14, pw - 14, h - 14)
        [_inn_panel, _church_panel, _bakery_panel][i](k, pw, h)
        nameplate(k, pw / 2, 40, names[i])
        k.unclip(); k.c.restoreState()

def lineup_fig(k, w, h, v, i=0, who="garland"):
    k.c.saveState(); k.c.translate(i * PW, 0); k.clip_rect(14, 14, PW - 14, h - 14)
    getattr(P4, who)(k, PW / 2 - 46, 70, 236)
    k.unclip(); k.c.restoreState()

# ----------------------------------------------------------------------------- 7. Agnes looking at closed PO
def looking_plate(k, w, h):
    plate_open(k, w, h)
    k.sunday_sky(w, h, 190)
    k.cobbles(w, h, 85)
    # street perspective toward PO
    k.kettle_gull(40, 100, 100, 140)
    k.bakery6(160, 95, 100, 145)
    k.post_office(300, 70, 190, 240, closed=True, blind=True)  # large, end of street
    k.unclip()

def agnes_look(k, w, h, v):
    part_open(k, w, h); P4.agnes(k, 90, 28, 230, basket=False); k.unclip()

# ----------------------------------------------------------------------------- 8. returned / Monday open
def returned_plate(k, w, h):
    plate_open(k, w, h)
    k.sunday_sky(w, h, 180)  # still warm
    k.cobbles(w, h, 80)
    k.post_office(200, 70, 220, 260, closed=False, blind=False)
    k.unclip()

def garland_ret(k, w, h, v):
    part_open(k, w, h)
    expr = "sheepish" if "sheepish" in v else "smile"
    P4.garland(k, 120, 30, 230, expr=expr, prop=False)
    k.unclip()

def wenna_ret(k, w, h, v):
    part_open(k, w, h); P4.wenna(k, 340, 30, 230, prop=False); k.unclip()

def parcel_ret(k, w, h, v):
    part_open(k, w, h); k.parcel(280, 70, w=70, h=36); k.unclip()

# ----------------------------------------------------------------------------- cast strip + vignette (postal stamp style)
def cast_plate(k, w, h):
    k.wash_rect(0, 0, w, h, SKY2)
    k.wash_rect(0, 0, w, 50, COBBLE)
    # perforated stamp edge
    for i in range(0, int(w), 12):
        k.circle(i + 6, 4, 3, lw=0, fill=C(247, 240, 225), stroke=False)
        k.circle(i + 6, h - 4, 3, lw=0, fill=C(247, 240, 225), stroke=False)
    k.c.setStrokeColor(K); k.c.setLineWidth(1.3); k.c.rect(1, 1, w - 2, h - 2, stroke=1, fill=0)

def cast_fig(k, w, h, v, i=0, who="garland"):
    getattr(P4, who)(k, w * (0.15 + 0.32 * i), 18, h * 0.78)

def vignette(k, w, h):
    """Circular postal-stamp vignette: CLOSED sign + puffin blanket — unique end-card art."""
    k.circle(w / 2, h / 2, w * 0.46, lw=1.5, fill=C(250, 244, 230)); k.circle(w / 2, h / 2, w * 0.44, lw=0.5, fill=None)
    # perforations
    for i in range(24):
        a = 2 * math.pi * i / 24
        k.circle(w / 2 + w * 0.46 * math.cos(a), h / 2 + w * 0.46 * math.sin(a), 3.5, lw=0, fill=C(247, 240, 225), stroke=False)
    k.c.saveState(); p = k.c.beginPath(); p.circle(w / 2, h / 2, w * 0.44 - 1); k.c.clipPath(p, stroke=0, fill=0)
    k.wash_rect(0, 0, w, h, PO_DOOR)
    k.rect(w * 0.22, h * 0.55, w * 0.56, h * 0.22, lw=1.5, fill=C(250, 244, 230))
    k.text(w / 2, h * 0.6, "CLOSED", size=28, font="Ink-Playfair", color=PO_SIGN)
    k.blanket_drape(w * 0.18, h * 0.35, L=w * 0.55, fat=w * 0.18)
    k.c.restoreState()

# ============================================================================= jobs
AW, AH = 512, 384
V3 = ["base", "base+blink", "base+talk"]; V2 = ["base", "base+blink"]
FX = dict(gull=dict(fn=gull_fx, variants=["f0", "f1", "f2", "f3"], page=(44, 22)),
          leaf=dict(fn=leaf_fx, variants=["f0", "f1", "f2"], page=(18, 12)))

def jobs():
    J = []
    J.append(dict(name="hook", w=AW, h=AH, plate=hook_plate, seed=61, parts=dict(
        blanket=dict(fn=blanket_hook, variants=["base"]), **FX)))
    J.append(dict(name="sunday", w=AW, h=AH, plate=sunday_plate, seed=62, parts=dict(
        cloud1=dict(fn=partial(cloud_part, x=120, y=330, s_=1.0), variants=["base"]),
        cloud2=dict(fn=partial(cloud_part, x=360, y=350, s_=0.7), variants=["base"]), **FX)))
    J.append(dict(name="porch", w=AW, h=AH, plate=porch_plate, seed=63, parts=dict(
        parcel=dict(fn=parcel_part, variants=["base"]),
        wenna=dict(fn=wenna_porch, variants=V2), **FX)))
    J.append(dict(name="empty", w=AW, h=AH, plate=partial(porch_plate, empty=True), seed=64, parts=dict(**FX)))
    J.append(dict(name="street", w=AW, h=AH, plate=street_meet_plate, seed=65, parts=dict(
        agnes=dict(fn=agnes_meet, variants=V2),
        wenna=dict(fn=wenna_meet, variants=V2),
        tamsin=dict(fn=tamsin_meet, variants=V3),
        jago=dict(fn=jago_meet, variants=V3),
        cloud1=dict(fn=partial(cloud_part, x=100, y=320, s_=0.9), variants=["base"]), **FX)))
    J.append(dict(name="garland", w=AW, h=AH, plate=garland_plate, seed=66, parts=dict(
        garland=dict(fn=garland_part, variants=V3 + ["sheepish", "sheepish+blink"]),
        agnes=dict(fn=agnes_garland, variants=V2),
        wenna=dict(fn=wenna_garland, variants=V2), **FX)))
    J.append(dict(name="lineup", w=3 * PW, h=AH, plate=lineup_plate, seed=67, parts=dict(
        garland=dict(fn=partial(lineup_fig, i=0, who="garland"), variants=V3),
        tamsin=dict(fn=partial(lineup_fig, i=1, who="tamsin"), variants=V3),
        jago=dict(fn=partial(lineup_fig, i=2, who="jago"), variants=V3), **FX)))
    J.append(dict(name="looking", w=AW, h=AH, plate=looking_plate, seed=68, parts=dict(
        agnes=dict(fn=agnes_look, variants=V2),
        cloud1=dict(fn=partial(cloud_part, x=80, y=320, s_=0.8), variants=["base"]), **FX)))
    J.append(dict(name="returned", w=AW, h=AH, plate=returned_plate, seed=69, parts=dict(
        garland=dict(fn=garland_ret, variants=["sheepish", "sheepish+blink", "smile", "smile+blink"]),
        wenna=dict(fn=wenna_ret, variants=V2),
        parcel=dict(fn=parcel_ret, variants=["base"]), **FX)))
    whos = ["garland", "tamsin", "jago"]
    J.append(dict(name="cast", w=720, h=260, plate=cast_plate, seed=70, parts={
        who: dict(fn=partial(cast_fig, i=i, who=who), variants=V2) for i, who in enumerate(whos)}))
    J.append(dict(name="vignette", w=384, h=384, plate=vignette, seed=71))
    return J

def make_ink(c, seed): return Ink6(c, seed=seed)

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    J = [j for j in jobs() if not want or j["name"] in want]
    save_layers(OUT, J, make_ink)
