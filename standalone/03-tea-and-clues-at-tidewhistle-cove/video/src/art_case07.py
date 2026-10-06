"""Illustrations for Case 7, The Dog That Stayed Quiet: colour-detailed + animation layers.
PART sprites use part_open (clip only) — never frame2 — so borders are not baked into rotating/bobbing sprites.
Unique hook: hero close-up of Sir Reginald the gnome (red hat) + empty pedestal / crushed grass — NOT the usual
bordered empty-scene + title-card formula. Garden green / gnome-red palette (distinct from Case 6 Sunday-gold).
Run: python3 art_case07.py [scene ...]"""
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
import figures as F
from art import nameplate
from layers import save_layers

pdfmetrics.registerFont(TTFont("Ink-Kalam", "/usr/share/fonts/truetype/sand-box/google/Kalam/Kalam-Bold.ttf"))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-07")

# ----------------------------------------------------------------------------- garden / gnome palette (vs case 6 Sunday-gold)
SKY = C(186, 220, 236); SKY2 = C(150, 196, 220)          # cool garden morning
GRASS = C(120, 168, 86); GRASS2 = C(96, 148, 70); GRASS3 = C(150, 190, 110)
HEDGE = C(58, 110, 62); HEDGE2 = C(40, 88, 48)
COTTAGE = C(240, 220, 190); ROOF = C(140, 78, 64)
GNOME_HAT = C(196, 48, 52); GNOME_BEARD = C(250, 248, 242); GNOME_BODY = C(70, 130, 170); GNOME_BOOT = C(50, 44, 40)
PEDESTAL = C(190, 178, 158); GATE = C(120, 84, 52); PATH = C(196, 178, 140)
NIGHT = C(40, 52, 78); NIGHT2 = C(28, 38, 58); MOON = C(240, 236, 210)

class Ink7(A4.Ink4):
    def garden_sky(s, w, h, y_horizon=200):
        s.vgrad(14, y_horizon, w - 14, h - 14, SKY, SKY2, steps=16)

    def grass_lawn(s, w, h, y_top=90):
        s.wash_rect(14, 14, w - 14, y_top, GRASS)
        rr = random.Random(11)
        for i in range(40):
            x = rr.uniform(20, w - 20); y = rr.uniform(18, y_top - 8)
            s.line([(x, y), (x + rr.uniform(-3, 3), y + rr.uniform(6, 12))], lw=0.45, amp=0,
                   color=GRASS2 if rr.random() < 0.5 else GRASS3)

    def hedge_wall(s, x, y, w, h):
        """High thick hedge — the garden barrier."""
        s.wash_rect(x, y, x + w, y + h * 0.85, HEDGE)
        rr = random.Random(int(x + y))
        for i in range(int(w / 8)):
            cx = x + 6 + i * 8
            col = mix(HEDGE, HEDGE2 if i % 2 == 0 else GRASS3, rr.uniform(0.2, 0.5))
            s.shape(s.arcpts(cx, y + h * 0.7, 10, 14, 0, 360, 12), lw=0.4, fill=col, amp=0.3)
        # top scallops
        for i in range(int(w / 14)):
            cx = x + 8 + i * 14
            s.shape(s.arcpts(cx, y + h * 0.88, 9, 7, 0, 360, 10), lw=0.5, fill=HEDGE2, amp=0.2)

    def wooden_gate(s, x, y, w, h, open_=False):
        s.rect(x, y, w, h, lw=1.2, fill=GATE)
        for i in range(4):
            yy = y + 6 + i * (h - 12) / 3
            s.line([(x + 4, yy), (x + w - 4, yy)], lw=1.0, amp=0, color=shade(GATE, 0.75))
        s.line([(x + w / 2, y + 4), (x + w / 2, y + h - 4)], lw=1.4, amp=0, color=shade(GATE, 0.7))
        s.circle(x + w * 0.78, y + h * 0.55, 3.5, lw=0.6, fill=PAL.brass)

    def cottage7(s, x, y, w, h):
        s.wall(x, y, w, h * 0.7, gap=3.0, color=COTTAGE)
        s.roof(x, x + w, y + h * 0.7, y + h, overhang=10, color=ROOF)
        s.window(x + w * 0.15, y + h * 0.28, w * 0.22, h * 0.28)
        s.window(x + w * 0.55, y + h * 0.28, w * 0.22, h * 0.28)
        s.rect(x + w * 0.38, y, w * 0.18, h * 0.42, lw=0.9, fill=GATE)

    def porch7(s, x, y, w):
        """Shallow porch floor + posts where Pickle sleeps facing the gate."""
        s.wash_rect(x - w / 2, y, x + w / 2, y + 36, C(200, 180, 150))
        for u in (-0.48, 0.48):
            s.line([(x + u * w, y + 4), (x + u * w, y + 70)], lw=2.4, amp=0, color=PAL.wood_dk)
        s.roof(x - w / 2 - 8, x + w / 2 + 8, y + 70, y + 100, overhang=4, color=ROOF)

    def gnome(s, x, y, scale=1.0, faded=False):
        """Sir Reginald: red hat, white beard, blue coat, fishing rod. scale~1 → ~90pt tall."""
        sc = scale
        hat = GNOME_HAT if not faded else C(180, 120, 110)
        # boots
        s.shape([(x - 14 * sc, y), (x + 14 * sc, y), (x + 10 * sc, y + 10 * sc), (x - 10 * sc, y + 10 * sc)],
                lw=0.8, fill=GNOME_BOOT, amp=0)
        # body
        s.shape([(x - 16 * sc, y + 10 * sc), (x + 16 * sc, y + 10 * sc), (x + 14 * sc, y + 42 * sc),
                 (x - 14 * sc, y + 42 * sc)], lw=1.0, fill=GNOME_BODY, amp=0.2)
        # belt
        s.rect(x - 14 * sc, y + 22 * sc, 28 * sc, 5 * sc, lw=0.5, fill=C(50, 40, 30))
        s.circle(x, y + 24.5 * sc, 2.2 * sc, lw=0.4, fill=PAL.brass)
        # head
        s.circle(x, y + 52 * sc, 12 * sc, lw=0.9, fill=PAL.skin)
        # beard
        s.shape([(x - 11 * sc, y + 48 * sc), (x - 13 * sc, y + 36 * sc), (x, y + 28 * sc),
                 (x + 13 * sc, y + 36 * sc), (x + 11 * sc, y + 48 * sc)], lw=0.7, fill=GNOME_BEARD, amp=0.3)
        # eyes / smile
        s.circle(x - 4 * sc, y + 54 * sc, 1.1 * sc, fill=K, lw=0, stroke=False)
        s.circle(x + 4 * sc, y + 54 * sc, 1.1 * sc, fill=K, lw=0, stroke=False)
        s.line([(x - 4 * sc, y + 49 * sc), (x, y + 47.5 * sc), (x + 4 * sc, y + 49 * sc)], lw=0.6)
        # red hat (pointy)
        s.shape([(x - 14 * sc, y + 58 * sc), (x, y + 88 * sc), (x + 14 * sc, y + 58 * sc)],
                lw=1.0, fill=hat, amp=0.15)
        s.circle(x, y + 58 * sc, 3 * sc, lw=0.4, fill=GNOME_BEARD)  # pom-ish brim fluff
        # fishing rod over shoulder
        s.line([(x + 12 * sc, y + 40 * sc), (x + 38 * sc, y + 78 * sc)], lw=1.3, amp=0, color=PAL.wood)
        s.line([(x + 38 * sc, y + 78 * sc), (x + 42 * sc, y + 70 * sc)], lw=0.5, amp=0, color=C(80, 80, 90))
        s.circle(x + 42 * sc, y + 69 * sc, 2.0 * sc, lw=0.4, fill=C(220, 160, 80))  # little fish

    def pedestal(s, x, y, w=36, h=14, empty=False, crushed=False):
        s.rect(x - w / 2, y, w, h, lw=1.0, fill=PEDESTAL)
        s.rect(x - w / 2 - 4, y - 4, w + 8, 5, lw=0.8, fill=shade(PEDESTAL, 0.9))
        if empty:
            # dashed ghost outline of missing gnome boots
            s.c.setDash(2, 2); s.c.setStrokeColor(C(100, 90, 70)); s.c.setLineWidth(1.0)
            s.c.ellipse(x - 12, y + h + 2, 24, 10, stroke=1, fill=0); s.c.setDash([])
        if crushed:
            rr = random.Random(5)
            for i in range(8):
                gx = x + rr.uniform(-28, 28); gy = y - 2 + rr.uniform(-6, 4)
                s.line([(gx, gy), (gx + rr.uniform(-5, 5), gy - rr.uniform(4, 10))], lw=0.7, amp=0, color=shade(GRASS2, 0.7))

    def pickle(s, x, y, scale=1.0, sleeping=False):
        """Pickle the terrier — small, scruffy, white/tan."""
        sc = scale
        body = C(236, 220, 190); ear = C(180, 130, 90); nose = C(40, 36, 34)
        # body
        s.shape(s.arcpts(x, y + 10 * sc, 22 * sc, 12 * sc, 0, 360, 16), lw=0.9, fill=body, amp=0.25)
        # head
        s.circle(x + 16 * sc, y + 18 * sc, 11 * sc, lw=0.9, fill=body)
        # ears
        s.shape([(x + 10 * sc, y + 24 * sc), (x + 4 * sc, y + 36 * sc), (x + 14 * sc, y + 28 * sc)], lw=0.6, fill=ear, amp=0)
        s.shape([(x + 22 * sc, y + 24 * sc), (x + 28 * sc, y + 36 * sc), (x + 18 * sc, y + 28 * sc)], lw=0.6, fill=ear, amp=0)
        # face
        if sleeping:
            s.line([(x + 12 * sc, y + 18 * sc), (x + 14 * sc, y + 17 * sc), (x + 16 * sc, y + 18 * sc)], lw=0.7)
            s.line([(x + 18 * sc, y + 18 * sc), (x + 20 * sc, y + 17 * sc), (x + 22 * sc, y + 18 * sc)], lw=0.7)
            # zzz
            s.text(x + 30 * sc, y + 32 * sc, "z", size=8 * sc, font="Ink-Kalam", color=C(100, 100, 120))
        else:
            s.circle(x + 13 * sc, y + 19 * sc, 1.3 * sc, fill=K, lw=0, stroke=False)
            s.circle(x + 19 * sc, y + 19 * sc, 1.3 * sc, fill=K, lw=0, stroke=False)
            s.circle(x + 13.4 * sc, y + 19.3 * sc, 0.35 * sc, fill=Wt, lw=0, stroke=False)
            s.circle(x + 19.4 * sc, y + 19.3 * sc, 0.35 * sc, fill=Wt, lw=0, stroke=False)
        s.circle(x + 16 * sc, y + 14 * sc, 2.2 * sc, lw=0.5, fill=nose)
        # legs / tail
        for dx in (-12, -4, 4, 10):
            s.line([(x + dx * sc, y + 4 * sc), (x + dx * sc, y - 2 * sc)], lw=2.0, amp=0, color=shade(body, 0.85))
        s.line([(x - 20 * sc, y + 12 * sc), (x - 28 * sc, y + 20 * sc), (x - 24 * sc, y + 28 * sc)], lw=1.6, color=body)
        # collar
        s.rect(x + 10 * sc, y + 12 * sc, 12 * sc, 2.5 * sc, lw=0.4, fill=C(196, 48, 52))
        s.circle(x + 16 * sc, y + 11 * sc, 1.6 * sc, lw=0.3, fill=PAL.brass)

# ============================================================================= open helpers
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

def star_fx(k, w, h, v):
    k.circle(w / 2, h / 2, 2.2, lw=0, fill=MOON, stroke=False)

# ----------------------------------------------------------------------------- 1. UNIQUE HOOK: hero gnome (no empty-scene formula)
def hook_plate(k, w, h):
    """First-frame hero: Sir Reginald fills most of the frame on crushed grass — breaks the bordered 4:3 template."""
    # NO plate_open / frame2 — irregular soft edge via wash to paper at margins (render HOOK_BORDER=False)
    k.wash_rect(0, 0, w, h, GRASS)
    rr = random.Random(7)
    for i in range(50):
        x = rr.uniform(10, w - 10); y = rr.uniform(10, h * 0.45)
        k.line([(x, y), (x + rr.uniform(-4, 4), y + rr.uniform(8, 16))], lw=0.5, amp=0,
               color=GRASS2 if rr.random() < 0.5 else GRASS3)
    # soft vignette wash at corners (paper colour) so he "breaks out"
    k.wash_rect(0, h * 0.72, w, h, SKY2)
    # empty pedestal with crushed grass — the crime
    k.pedestal(w * 0.28, 40, w=50, h=16, empty=True, crushed=True)
    # Sir Reginald HUGE, slightly off-centre, fishing rod exiting frame
    k.gnome(w * 0.58, 30, scale=2.35, faded=False)  # vivid prize-gnome red for the hero open
    # small "GONE?" chalk tag
    k.rect(28, h * 0.55, 100, 40, lw=1.2, fill=C(250, 244, 230))
    k.text(78, h * 0.575, "GONE?", size=18, font="Ink-Playfair", color=GNOME_HAT)

def gnome_hook_part(k, w, h, v):
    """Optional bobbing gnome overlay (subtle) — drawn without frame2."""
    part_open(k, w, h)
    # already on plate; leave empty or a dew glint
    k.circle(w * 0.72, h * 0.62, 3, lw=0, fill=C(255, 255, 240), stroke=False)
    k.unclip()

# ----------------------------------------------------------------------------- 2. garden overview (hedge + gate + pedestal empty)
def garden_plate(k, w, h):
    plate_open(k, w, h)
    k.garden_sky(w, h, 190)
    k.grass_lawn(w, h, 100)
    # high hedge L and R with gate in the middle
    k.hedge_wall(14, 70, 150, 160)
    k.hedge_wall(w - 164, 70, 150, 160)
    k.wooden_gate(w / 2 - 28, 70, 56, 90)
    # cottage behind hedge peek
    k.cottage7(180, 200, 150, 130)
    # empty pedestal centre-front
    k.pedestal(w / 2, 50, w=44, h=14, empty=True, crushed=True)
    k.unclip()

def cloud_part(k, w, h, v, x=0, y=0, s_=1.0):
    part_open(k, w, h)
    for (dx, dy, r) in ((0, 0, 16), (16, 4, 13), (-15, 2, 11), (6, 10, 11), (28, -1, 9)):
        k.circle(x + dx * s_, y + dy * s_, r * s_, lw=0, fill=PAL.cloud, stroke=False)
    k.unclip()

# ----------------------------------------------------------------------------- 3. porch with Pickle facing gate
def porch_plate(k, w, h):
    plate_open(k, w, h)
    k.garden_sky(w, h, 170)
    k.grass_lawn(w, h, 70)
    k.wall(14, 80, w - 28, 180, gap=3.0, color=COTTAGE)
    k.porch7(w / 2, 40, 300)
    # gate visible ahead (what Pickle faces)
    k.hedge_wall(40, 200, 80, 100)
    k.hedge_wall(w - 120, 200, 80, 100)
    k.wooden_gate(w / 2 - 22, 200, 44, 70)
    k.unclip()

def pickle_porch(k, w, h, v):
    part_open(k, w, h)
    sleep = "sleep" in v
    k.pickle(w * 0.42, 55, scale=1.35, sleeping=sleep)
    k.unclip()

# ----------------------------------------------------------------------------- 4. night / no-bark (Mr Hocking window)
def night_plate(k, w, h):
    plate_open(k, w, h)
    k.vgrad(14, 200, w - 14, h - 14, NIGHT, NIGHT2, steps=14)
    k.wash_rect(14, 14, w - 14, 90, C(40, 70, 50))  # night grass
    k.circle(w * 0.78, 300, 28, lw=0, fill=MOON, stroke=False)
    k.circle(w * 0.78, 300, 22, lw=0, fill=C(255, 252, 230), stroke=False)
    # Hocking cottage window lit
    k.wall(60, 80, 160, 160, gap=3.0, color=C(90, 80, 70))
    k.roof(60, 220, 240, 300, overhang=8, color=C(60, 50, 45))
    k.rect(100, 140, 50, 55, lw=1.0, fill=C(255, 220, 140))  # lit window
    k.line([(125, 140), (125, 195)], lw=0.8, amp=0, color=C(120, 90, 50))
    k.line([(100, 167), (150, 167)], lw=0.8, amp=0, color=C(120, 90, 50))
    # porch silhouette with sleeping Pickle outline
    k.wash_rect(280, 40, 480, 90, C(50, 45, 40))
    k.unclip()

def pickle_night(k, w, h, v):
    part_open(k, w, h)
    k.pickle(360, 50, scale=1.1, sleeping=True)
    k.unclip()

# ----------------------------------------------------------------------------- 5. kitchen tea (Loveday + Agnes + Pickle basket)
def kitchen_plate(k, w, h):
    plate_open(k, w, h)
    k.wash_rect(14, 14, w - 14, h - 14, C(250, 238, 214))
    # dresser / window
    k.rect(40, 160, 120, 140, lw=1.0, fill=C(255, 240, 200))
    k.line([(100, 160), (100, 300)], lw=0.7, amp=0, color=C(160, 140, 100))
    k.line([(40, 230), (160, 230)], lw=0.7, amp=0, color=C(160, 140, 100))
    k.rect(300, 100, 180, 120, lw=1.0, fill=PAL.wood)  # dresser
    for i in range(3):
        k.circle(330 + i * 40, 160, 12, lw=0.5, fill=C(220, 100, 90) if i == 0 else C(100, 140, 180))
    # table
    k.rect(80, 40, 280, 18, lw=1.0, fill=PAL.wood)
    k.unclip()

def agnes_kit(k, w, h, v):
    part_open(k, w, h); P4.agnes(k, 120, 28, 210, basket=False); k.unclip()

def loveday_kit(k, w, h, v):
    part_open(k, w, h); F.loveday(k, 300, 28, 210, jug_=False); k.unclip()

def pickle_basket(k, w, h, v):
    part_open(k, w, h)
    # basket
    k.rect(200, 30, 70, 28, lw=0.9, fill=PAL.wicker)
    k.pickle(220, 42, scale=0.85, sleeping=False)
    k.unclip()

# ----------------------------------------------------------------------------- 6. suspects meet (Ashby / Fenwick / Pip)
def street_plate(k, w, h):
    plate_open(k, w, h)
    k.garden_sky(w, h, 180)
    k.grass_lawn(w, h, 80)
    k.cottage7(30, 120, 140, 160)
    # grocer hint
    k.wall(340, 100, 140, 150, gap=2.8, color=C(250, 236, 210))
    k.roof(340, 480, 250, 320, overhang=8, color=C(100, 120, 90))
    k.rect(355, 220, 110, 28, lw=0.9, fill=C(60, 110, 70))
    k.text(410, 228, "FENWICK'S", size=11, font="Ink-Plex", color=C(250, 230, 180))
    k.unclip()

def ashby_meet(k, w, h, v):
    part_open(k, w, h); P4.ashby(k, 100, 28, 200); k.unclip()

def fenwick_meet(k, w, h, v):
    part_open(k, w, h); P4.fenwick(k, 240, 28, 200); k.unclip()

def pip_meet(k, w, h, v):
    part_open(k, w, h); P4.pip(k, 380, 28, 200); k.unclip()

# ----------------------------------------------------------------------------- 7. lineup
PW = 512
def _garden_panel(k, pw, h):
    k.garden_sky(pw, h, 160); k.grass_lawn(pw, h, 70)
    k.hedge_wall(20, 90, 100, 120); k.wooden_gate(pw / 2 - 20, 90, 40, 70)

def _shop_panel(k, pw, h):
    k.garden_sky(pw, h, 160); k.wash_rect(14, 14, pw - 14, 70, PATH)
    k.wall(60, 90, 180, 150, gap=2.8, color=C(250, 236, 210))
    k.roof(60, 240, 240, 300, overhang=8, color=C(100, 120, 90))
    k.text(150, 220, "GROCER", size=12, font="Ink-Plex", color=C(60, 110, 70))

def _beach_panel(k, pw, h):
    k.garden_sky(pw, h, 160)
    k.wash_rect(14, 14, pw - 14, 80, C(238, 220, 178))  # sand holiday
    k.wash_rect(14, 80, pw - 14, 120, C(140, 190, 208))

def lineup_plate(k, w, h):
    for i, fn in enumerate((_garden_panel, _shop_panel, _beach_panel)):
        x = i * PW
        k.c.saveState(); k.c.translate(x, 0)
        k.frame2(PW, h); k.clip_rect(14, 14, PW - 14, h - 14)
        fn(k, PW, h); k.unclip(); k.c.restoreState()
        nameplate(k, x + PW / 2, 18, ["Pip Carew", "Mr Fenwick", "Mrs Ashby"][i])

def lineup_fig(k, w, h, v, i=0, who="pip"):
    part_open(k, w, h)
    x = i * PW + PW * 0.42
    getattr(P4, who)(k, x, 30, 230)
    k.unclip()

# ----------------------------------------------------------------------------- 8. solution: shed + bright hat return
def shed_plate(k, w, h):
    plate_open(k, w, h)
    k.garden_sky(w, h, 170)
    k.grass_lawn(w, h, 80)
    # Pip's shed
    k.wall(80, 80, 200, 160, gap=3.2, color=C(180, 150, 110))
    k.roof(80, 280, 240, 320, overhang=12, color=C(100, 70, 50))
    k.rect(150, 80, 50, 90, lw=1.0, fill=C(90, 70, 50))
    # paint pots
    for i, col in enumerate([GNOME_HAT, GNOME_BODY, C(250, 248, 242)]):
        k.circle(320 + i * 36, 55, 14, lw=0.8, fill=col)
    k.unclip()

def pip_shed(k, w, h, v):
    part_open(k, w, h)
    expr = "sheepish" if "sheepish" in v else ("smile" if "smile" in v else "neutral")
    P4.pip(k, 200, 30, 230, expr=expr)
    k.unclip()

def gnome_bright(k, w, h, v):
    part_open(k, w, h)
    k.gnome(360, 40, scale=1.1, faded=False)
    k.unclip()

def returned_plate(k, w, h):
    plate_open(k, w, h)
    k.garden_sky(w, h, 180)
    k.grass_lawn(w, h, 90)
    k.hedge_wall(14, 80, 120, 140)
    k.hedge_wall(w - 134, 80, 120, 140)
    k.wooden_gate(w / 2 - 24, 80, 48, 80)
    k.pedestal(w / 2, 45, w=40, h=14, empty=False, crushed=False)
    k.unclip()

def gnome_ret(k, w, h, v):
    part_open(k, w, h); k.gnome(w / 2, 55, scale=1.2, faded=False); k.unclip()

def loveday_ret(k, w, h, v):
    part_open(k, w, h); F.loveday(k, 120, 30, 220, jug_=False); k.unclip()

def pip_ret(k, w, h, v):
    part_open(k, w, h); P4.pip(k, 360, 30, 220, expr="smile"); k.unclip()

# ----------------------------------------------------------------------------- cast strip (Pickle-forward)
def cast_plate(k, w, h):
    k.wash_rect(0, 0, w, h, GRASS3)
    k.wash_rect(0, 0, w, 40, PATH)
    # leaf-edge instead of stamp perforations — garden feel
    for i in range(0, int(w), 16):
        k.shape([(i, h - 2), (i + 8, h - 10), (i + 16, h - 2)], lw=0, fill=GRASS, stroke=False)
    k.c.setStrokeColor(K); k.c.setLineWidth(1.3); k.c.rect(1, 1, w - 2, h - 2, stroke=1, fill=0)

def cast_fig(k, w, h, v, i=0, who="pip"):
    getattr(P4, who)(k, w * (0.14 + 0.34 * i), 16, h * 0.78)

def vignette(k, w, h):
    """Circular garden vignette: bright Sir Reginald + Pickle — unique end-card art."""
    k.circle(w / 2, h / 2, w * 0.46, lw=1.5, fill=GRASS3); k.circle(w / 2, h / 2, w * 0.44, lw=0.5, fill=None)
    for i in range(24):
        a = 2 * math.pi * i / 24
        k.circle(w / 2 + w * 0.46 * math.cos(a), h / 2 + w * 0.46 * math.sin(a), 3.5, lw=0, fill=C(247, 240, 225), stroke=False)
    k.c.saveState(); p = k.c.beginPath(); p.circle(w / 2, h / 2, w * 0.44 - 1); k.c.clipPath(p, stroke=0, fill=0)
    k.wash_rect(0, 0, w, h, SKY)
    k.gnome(w / 2, h * 0.22, scale=1.5, faded=False)
    k.pickle(w * 0.22, h * 0.28, scale=1.0, sleeping=False)
    k.c.restoreState()


def gnome_garden(k, w, h, v):
    part_open(k, w, h); k.gnome(w / 2, 55, scale=1.15, faded=True); k.unclip()

# ============================================================================= jobs
AW, AH = 512, 384
V3 = ["base", "base+blink", "base+talk"]; V2 = ["base", "base+blink"]
FX = dict(gull=dict(fn=gull_fx, variants=["f0", "f1", "f2", "f3"], page=(44, 22)),
          leaf=dict(fn=leaf_fx, variants=["f0", "f1", "f2"], page=(18, 12)))
FXN = dict(star=dict(fn=star_fx, variants=["f0", "f1"], page=(10, 10)), **FX)

def jobs():
    J = []
    J.append(dict(name="hook", w=AW, h=AH, plate=hook_plate, seed=71, parts=dict(
        glint=dict(fn=gnome_hook_part, variants=["base"]), **FX)))
    J.append(dict(name="garden", w=AW, h=AH, plate=garden_plate, seed=72, parts=dict(
        gnome=dict(fn=gnome_garden, variants=["base"]),
        cloud1=dict(fn=partial(cloud_part, x=120, y=330, s_=1.0), variants=["base"]),
        cloud2=dict(fn=partial(cloud_part, x=360, y=350, s_=0.7), variants=["base"]), **FX)))
    J.append(dict(name="porch", w=AW, h=AH, plate=porch_plate, seed=73, parts=dict(
        pickle=dict(fn=pickle_porch, variants=["base", "sleep"]), **FX)))
    J.append(dict(name="night", w=AW, h=AH, plate=night_plate, seed=74, parts=dict(
        pickle=dict(fn=pickle_night, variants=["base"]), **FXN)))
    J.append(dict(name="kitchen", w=AW, h=AH, plate=kitchen_plate, seed=75, parts=dict(
        agnes=dict(fn=agnes_kit, variants=V2),
        loveday=dict(fn=loveday_kit, variants=V3),
        pickle=dict(fn=pickle_basket, variants=["base"]), **FX)))
    J.append(dict(name="street", w=AW, h=AH, plate=street_plate, seed=76, parts=dict(
        ashby=dict(fn=ashby_meet, variants=V2),
        fenwick=dict(fn=fenwick_meet, variants=V2),
        pip=dict(fn=pip_meet, variants=V3), **FX)))
    J.append(dict(name="lineup", w=3 * PW, h=AH, plate=lineup_plate, seed=77, parts=dict(
        pip=dict(fn=partial(lineup_fig, i=0, who="pip"), variants=V3),
        fenwick=dict(fn=partial(lineup_fig, i=1, who="fenwick"), variants=V3),
        ashby=dict(fn=partial(lineup_fig, i=2, who="ashby"), variants=V3), **FX)))
    J.append(dict(name="shed", w=AW, h=AH, plate=shed_plate, seed=78, parts=dict(
        pip=dict(fn=pip_shed, variants=["sheepish", "sheepish+blink", "smile", "smile+blink"]),
        gnome=dict(fn=gnome_bright, variants=["base"]), **FX)))
    J.append(dict(name="returned", w=AW, h=AH, plate=returned_plate, seed=79, parts=dict(
        gnome=dict(fn=gnome_ret, variants=["base"]),
        loveday=dict(fn=loveday_ret, variants=V2),
        pip=dict(fn=pip_ret, variants=V2), **FX)))
    whos = ["pip", "fenwick", "ashby"]
    J.append(dict(name="cast", w=720, h=260, plate=cast_plate, seed=80, parts={
        who: dict(fn=partial(cast_fig, i=i, who=who), variants=V2) for i, who in enumerate(whos)}))
    J.append(dict(name="vignette", w=384, h=384, plate=vignette, seed=81))
    return J

def make_ink(c, seed): return Ink7(c, seed=seed)

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    J = [j for j in jobs() if not want or j["name"] in want]
    save_layers(OUT, J, make_ink)
