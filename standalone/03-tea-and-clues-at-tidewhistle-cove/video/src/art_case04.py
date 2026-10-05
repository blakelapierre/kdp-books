"""Illustrations for Case 4, The Sandbar at High Tide, in the COLOUR-DETAILED style (colour washes under ink,
detailed people4.py characters), drawn as ANIMATION LAYERS: every picture is a still plate plus moving parts
(characters with blink / talk variants, boats, gulls, wave strokes, bunting flags, steam, the chalk lettering, the
compass and its needle, clock hands, the rope coil...). layers.save_layers() writes ../work/art-04/<scene>.png,
<scene>.json and <scene>__<part>__<variant>.png; cases/case04.py choreographs them and anim.py plays them.
Run: python3 art_case04.py [scene ...]          (~1 min on 8 CPUs)
The three suspects (Morwenna, Pip, Mr Rundle) are drawn at the same height, stance, arm pose and colour weight in
every pre-solution picture and get the same idle / blink / nod animation; only Mr Rundle's after-solution reaction
(sheepish, blushing, handing the compass back) differs. Everything is drawn in code; no image generation."""
import math, os, sys, random
from functools import partial
import colorink
colorink.set_style("color-detailed")
import art_case03_color as A3
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
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-04")

# ----------------------------------------------------------------------------- palette
SLATE = C(52, 62, 64); SLATE2 = C(70, 82, 84); CHALK = C(244, 244, 236); CHALK2 = C(226, 232, 238)
STONE = C(206, 198, 182); STONE2 = C(184, 176, 160); QUAYTOP = C(222, 214, 196); SAND = C(238, 220, 178); SAND_WET = C(206, 186, 146)
SEA = C(140, 190, 208); SEA2 = C(104, 160, 190); SEA_DEEP = C(84, 136, 172); HORIZON = C(196, 222, 228)
OFFICE = C(206, 226, 238); PANEL = C(214, 176, 128); PANEL2 = C(190, 150, 104); WALLW = C(244, 232, 206)
ROCK = C(160, 152, 140); ROCK2 = C(128, 120, 112); GRASS = C(176, 206, 140); GRASS2 = C(150, 188, 116)
CHURCH = C(214, 206, 190); TEAWALL = C(250, 238, 214); BOATBLUE = C(84, 128, 168); BOATRED = C(196, 92, 80)
ROPE = C(214, 186, 132); ROPE2 = C(170, 140, 92); NET = C(120, 150, 130); BUOY = C(232, 112, 84)

class Ink4(A3.ShopC):
    # --- sea and shore ---------------------------------------------------------
    def sky4(s, w, h, y0):
        s.vgrad(14, y0, w - 14, h - 14, PAL.sky, PAL.sky2, steps=18)

    def sea4(s, x0, x1, y0, y1, rows=6):
        s.vgrad(x0, y0, x1, y1, SEA, SEA2, steps=12)
        rr = random.Random(int(x0 + y0 * 3))
        for j in range(rows):   # faint still wave lines (moving foam strokes are animated on top)
            y = lerp(y1 - 4, y0 + 4, (j + 0.5) / rows); n = 4 + j
            for _ in range(n):
                L = rr.uniform(10, 22) * (0.6 + 0.1 * j); x = rr.uniform(x0, x1 - L)
                s.line([(x + L * t, y + 0.9 * math.sin(t * math.pi * 2)) for t in [i / 8 for i in range(9)]], lw=0.35 + 0.05 * j, amp=0, color=shade(SEA2, 0.86))

    def headland(s, x0, x1, y, hgt, col=PAL.headland):
        pts = [(x0, y)] + [(lerp(x0, x1, t), y + hgt * (math.sin(t * math.pi) ** 0.7) * (0.8 + 0.2 * math.sin(t * 9))) for t in [i / 16 for i in range(17)]] + [(x1, y)]
        with s.tint(col): s.shape(pts, lw=0.7, fill=Wt, amp=0.3)

    def quay(s, w, y, x0=14, x1=None):
        x1 = x1 or w - 14
        s.wash_rect(x0, 14, x1, y, STONE)
        rr = random.Random(int(y))
        for j in range(6):
            yy = y - 8 - j * 14
            for i in range(int((x1 - x0) / 22) + 1):
                cx = x0 + 6 + i * 22 + (j % 2) * 11
                if cx > x1 - 4 or yy < 16: continue
                s.shape(s.arcpts(cx, yy, 9.5, 5.2, 0, 360, 12), lw=0.45, fill=mix(STONE, K if rr.random() < 0.5 else Wt, rr.uniform(0.04, 0.14)), amp=0.25)
        s.rect(x0, y - 4, x1 - x0, 6, lw=0.9, fill=QUAYTOP)
        for i in range(int((x1 - x0) / 30)): s.line([(x0 + 15 + i * 30, y - 4), (x0 + 15 + i * 30, y + 2)], lw=0.5, amp=0)

    def boat4(s, x, y, w, col, sail=True, sailcol=None):
        hull = [(x - w / 2, y + w * 0.16), (x + w / 2, y + w * 0.16), (x + w * 0.38, y), (x - w * 0.36, y)]
        with s.tint(col): s.shape(hull, lw=0.9, fill=Wt, amp=0.1)
        s.wash([(x - w * 0.36, y), (x + w * 0.38, y), (x + w * 0.44, y + w * 0.06), (x - w * 0.42, y + w * 0.06)], shade(col, 0.75))
        s.line([(x - w * 0.47, y + w * 0.13), (x + w * 0.47, y + w * 0.13)], lw=0.6, amp=0, color=PAL.cloud)
        if sail:
            s.line([(x, y + w * 0.16), (x, y + w * 0.95)], lw=0.9, amp=0)
            with s.tint(sailcol or PAL.cloud): s.shape([(x + 1.5, y + w * 0.92), (x + 1.5, y + w * 0.22), (x + w * 0.42, y + w * 0.22)], lw=0.8, fill=Wt, amp=0.1)
            with s.tint(PAL.sun): s.shape([(x - 1.5, y + w * 0.8), (x - 1.5, y + w * 0.24), (x - w * 0.3, y + w * 0.24)], lw=0.8, fill=Wt, amp=0.1)
        s.line([(x - w * 0.55, y + 0.3), (x + w * 0.55, y + 0.3)], lw=0.45, amp=0.3, color=shade(SEA2, 0.8))

    def gull_rock(s, x, y, w, hgt):
        pts = [(x - w / 2, y), (x - w * 0.42, y + hgt * 0.5), (x - w * 0.24, y + hgt * 0.86), (x - w * 0.05, y + hgt), (x + w * 0.16, y + hgt * 0.92),
               (x + w * 0.34, y + hgt * 0.64), (x + w / 2, y)]
        with s.tint(ROCK, hatch=ROCK2):
            s.shape(pts, lw=1.0, fill=Wt, amp=0.6); s.hatch(pts, angle=-60, gap=2.2, lw=0.35)
        s.wash([(x + w * 0.05, y + hgt * 0.98), (x + w * 0.16, y + hgt * 0.92), (x + w * 0.3, y + hgt * 0.7), (x + w * 0.1, y + hgt * 0.8)], PAL.cloud)   # guano cap
        for (gx, gy) in ((x - w * 0.1, y + hgt * 1.0), (x + w * 0.12, y + hgt * 0.95)):   # gulls sitting on top
            s.shape(s.arcpts(gx, gy + 2.5, 3.6, 2.4, 0, 360, 12), lw=0.5, fill=PAL.cloud, amp=0)
            s.circle(gx + 3, gy + 5, 1.7, lw=0.5, fill=PAL.cloud); s.line([(gx + 4.5, gy + 5), (gx + 6.5, gy + 4.6)], lw=0.6, amp=0, color=PAL.sun)
        s.line([(x - w * 0.6, y + 1), (x + w * 0.6, y + 1)], lw=0.6, amp=0.3, color=PAL.foam)

    def office(s, x, y, w, h, win_compass=True):
        s.wall(x, y, w, h * 0.66, gap=3.0, color=OFFICE)
        s.roof(x, x + w, y + h * 0.66, y + h, overhang=6, color=PAL.slate)
        s.rect(x + w * 0.12, y + h * 0.5, w * 0.76, h * 0.12, lw=0.9, fill=PAL.card)
        s.text(x + w / 2, y + h * 0.525, "HARBOUR OFFICE", size=h * 0.06, font="Ink-Plex", color=PAL.navy)
        dx = x + w * 0.1
        s.shape([(dx, y), (dx + w * 0.22, y), (dx + w * 0.22, y + h * 0.42), (dx, y + h * 0.42)], lw=0.9, fill=PAL.navy_lt, amp=0)
        s.rect(dx + w * 0.04, y + h * 0.24, w * 0.14, h * 0.12, lw=0.5, fill=PAL.glass)
        s.circle(dx + w * 0.18, y + h * 0.2, 1.6, lw=0.4, fill=PAL.brass)
        wx, wy, ww, wh = x + w * 0.48, y + h * 0.16, w * 0.38, h * 0.26
        s.rect(wx - 3, wy - 3, ww + 6, wh + 6, lw=0.8, fill=PAL.cloud)
        s.rect(wx, wy, ww, wh, lw=0.8, fill=PAL.glass)
        s.line([(wx + ww / 2, wy), (wx + ww / 2, wy + wh)], lw=0.8, amp=0); s.line([(wx, wy + wh / 2), (wx + ww, wy + wh / 2)], lw=0.8, amp=0)
        s.rect(wx - 6, wy - 7, ww + 12, 5, lw=0.8, fill=PAL.cloud)   # sill
        if win_compass:
            s.shape(s.arcpts(wx + ww * 0.3, wy + 1.5, 5.5, 3, 0, 360, 14), lw=0.5, fill=PAL.brass, amp=0)
        with s.tint(PAL.cloud): s.chimney(x + w * 0.74, y + h * 0.8, w * 0.08, h * 0.2, smoke=False)
        s.line([(x + w + 2, y + h * 0.66), (x + w + 2, y + h * 1.25)], lw=1.2, amp=0)   # flagpole on the corner
        s.circle(x + w + 2, y + h * 1.26, 2.0, lw=0.6, fill=PAL.brass)

    def board(s, x, y, w, h, high=True, legs=True, scale=1.0):
        """Captain Quill's tide blackboard on an A-frame: TIDES TODAY / Low water 6:10 am / (High water at noon)."""
        if legs:
            for (ax, bx) in ((x + w * 0.12, x + w * 0.02), (x + w * 0.88, x + w * 0.98)):
                s.shape([(bx - 2.5, 14 if y > 30 else y - 30), (bx + 2.5, 14 if y > 30 else y - 30), (ax + 2.5, y + h + 6), (ax - 2.5, y + h + 6)], lw=0.8, fill=PAL.wood, amp=0)
        s.rect(x - 5, y - 5, w + 10, h + 10, lw=1.0, fill=PAL.wood)
        with s.tint(PAL.wood): s.hatch([(x - 5, y - 5), (x + w + 5, y - 5), (x + w + 5, y + h + 5), (x - 5, y + h + 5)], angle=0, gap=1.6, lw=0.3)
        s.rect(x, y, w, h, lw=0.9, fill=SLATE)
        rr = random.Random(5)
        for i in range(14):   # old chalk smudges
            cx, cy = x + rr.uniform(8, w - 8), y + rr.uniform(6, h - 6)
            s.c.saveState(); s.c.setFillColor(SLATE2); s.c.setFillAlpha(0.6); s.c.ellipse(cx - 9, cy - 3, cx + 9, cy + 3, stroke=0, fill=1); s.c.restoreState()
        s.text(x + w / 2, y + h * 0.78, "TIDES TODAY", size=h * 0.12 * scale, font="Ink-Kalam", color=CHALK)
        s.line([(x + w * 0.22, y + h * 0.74), (x + w * 0.78, y + h * 0.745)], lw=0.8, amp=0.3, color=CHALK2)
        s.text(x + w / 2, y + h * 0.53, "Low water 6:10 am", size=h * 0.1 * scale, font="Ink-Kalam", color=CHALK2)
        if high: s.board_high(x, y, w, h, scale)
        s.rect(x + w * 0.1, y - 4, w * 0.8, 4, lw=0.6, fill=PAL.wood_dk)   # chalk ledge
        s.rect(x + w * 0.2, y - 2.5, 7, 2, lw=0.3, fill=CHALK)

    def board_high(s, x, y, w, h, scale=1.0):
        s.text(x + w / 2, y + h * 0.18, "High water at noon", size=h * 0.125 * scale, font="Ink-Kalam", color=CHALK)
        tw = s.c.stringWidth("High water at noon", "Ink-Kalam", h * 0.125 * scale)
        s.line([(x + w / 2 - tw / 2, y + h * 0.13), (x + w / 2 + tw / 2, y + h * 0.125)], lw=1.0, amp=0.4, color=CHALK)

    def compass4(s, x, y, w, needle=True, box=True):
        """Brass ship's compass on the sill: wooden box, gimbal ring, card with the rose; base centre (x, y)."""
        if box:
            s.rect(x - w * 0.55, y, w * 1.1, w * 0.32, lw=0.9, fill=PAL.wood)
            with s.tint(PAL.wood): s.hatch([(x - w * 0.55, y), (x + w * 0.55, y), (x + w * 0.55, y + w * 0.32), (x - w * 0.55, y + w * 0.32)], angle=0, gap=1.4, lw=0.3)
            s.rect(x - w * 0.55, y + w * 0.32, w * 1.1, w * 0.05, lw=0.6, fill=PAL.wood_dk)
        cy = y + w * 0.62
        s.shape(s.arcpts(x, cy, w * 0.5, w * 0.27, 0, 360, 36), lw=1.0, fill=PAL.brass, amp=0)
        with s.tint(PAL.brass, hatch=shade(PAL.brass, 0.7)): s.hatch(s.arcpts(x, cy, w * 0.5, w * 0.27, 0, 360, 36), angle=-30, gap=1.6, lw=0.3)
        s.shape(s.arcpts(x, cy + w * 0.02, w * 0.4, w * 0.2, 0, 360, 36), lw=0.6, fill=C(252, 248, 232), amp=0)
        for i in range(16):
            a = math.radians(i * 22.5); L = 0.34 if i % 4 == 0 else 0.25 if i % 2 == 0 else 0.18
            s.line([(x + w * 0.1 * math.cos(a), cy + w * 0.02 + w * 0.05 * math.sin(a)), (x + w * L * math.cos(a), cy + w * 0.02 + w * L * 0.5 * math.sin(a))], lw=0.35, amp=0, color=shade(PAL.brass, 0.6))
        s.text(x, cy + w * 0.14, "N", size=w * 0.09, font="Ink-Plex", color=C(170, 60, 50))
        if needle: s.needle(x, cy + w * 0.02, w)
        s.line(s.arcpts(x - w * 0.14, cy + w * 0.12, w * 0.18, w * 0.06, 150, 60, 8), lw=0.8, amp=0, color=Wt)   # glass glint

    def needle(s, x, cy, w):
        s.shape([(x - w * 0.3, cy), (x, cy + w * 0.035), (x + w * 0.3, cy), (x, cy - w * 0.035)], lw=0.4, fill=C(70, 80, 100), amp=0)
        s.shape([(x, cy + w * 0.035), (x + w * 0.3, cy), (x, cy - w * 0.035)], lw=0.4, fill=C(206, 64, 54), amp=0)
        s.circle(x, cy, w * 0.025, lw=0.4, fill=PAL.brass)

    def rope_coil(s, x, y, w):
        for j in range(5):
            r = w * (0.5 - j * 0.07)
            with s.tint(ROPE, hatch=ROPE2): s.shape(s.arcpts(x, y + w * 0.12 + j * w * 0.035, r, r * 0.42, 0, 360, 30), lw=0.8, fill=Wt, amp=0.2)
            for i in range(14):
                a = math.radians(i * 360 / 14); px, py = x + r * 0.9 * math.cos(a), y + w * 0.12 + j * w * 0.035 + r * 0.38 * math.sin(a)
                s.line([(px - 1.2, py - 0.8), (px + 1.2, py + 0.8)], lw=0.35, amp=0, color=ROPE2)
        s.line([(x + w * 0.45, y + w * 0.12), (x + w * 0.62, y + w * 0.02), (x + w * 0.8, y + w * 0.06)], lw=2.2, amp=0.3, color=ROPE2)
        s.line([(x + w * 0.45, y + w * 0.12), (x + w * 0.62, y + w * 0.02), (x + w * 0.8, y + w * 0.06)], lw=1.4, amp=0.3, color=ROPE)

    def lobster_pot(s, x, y, w):
        s.shape(s.arcpts(x, y, w / 2, w * 0.55, 0, 180, 18) + [(x - w / 2, y)], lw=0.8, fill=C(196, 160, 110), amp=0.1)
        for i in range(5): s.line(s.arcpts(x, y, w / 2 * (1 - i * 0.18), w * 0.55, 0, 180, 12), lw=0.35, amp=0, color=shade(C(196, 160, 110), 0.6))
        s.rect(x - w / 2, y - 2, w, 3, lw=0.6, fill=C(150, 112, 76))

    def bollard(s, x, y, w):
        s.shape([(x - w * 0.4, y), (x + w * 0.4, y), (x + w * 0.3, y + w * 0.9), (x + w * 0.5, y + w * 1.1), (x - w * 0.5, y + w * 1.1), (x - w * 0.3, y + w * 0.9)], lw=0.9, fill=C(60, 66, 72), amp=0)
        s.line([(x - w * 0.2, y + w * 0.2), (x - w * 0.2, y + w * 0.8)], lw=0.6, amp=0, color=C(120, 128, 136))

    def flower_urn(s, x, y, w, flowers="lilies"):
        s.shape([(x - w * 0.3, y), (x + w * 0.3, y), (x + w * 0.45, y + w * 0.5), (x - w * 0.45, y + w * 0.5)], lw=0.8, fill=STONE, amp=0)
        rr = random.Random(int(x))
        for i in range(9):
            a = math.radians(rr.uniform(60, 120)); L = w * rr.uniform(0.6, 1.0)
            px, py = x + L * math.cos(a), y + w * 0.5 + L * math.sin(a)
            s.line([(x + rr.uniform(-4, 4), y + w * 0.5), (px, py)], lw=0.6, amp=0.2, color=P4.STEM)
            for pa in (-40, 0, 40):
                q = a + math.radians(pa); s.shape([(px, py), (px + w * 0.09 * math.cos(q) - 1.5, py + w * 0.09 * math.sin(q)), (px + w * 0.15 * math.cos(q), py + w * 0.15 * math.sin(q)),
                                                    (px + w * 0.09 * math.cos(q) + 1.5, py + w * 0.09 * math.sin(q))], lw=0.4, fill=P4.LILY, amp=0)

# ============================================================================= helpers
def frame_open(k, w, h): k.frame2(w, h); k.clip_rect(14, 14, w - 14, h - 14)

def harbour_backdrop(k, w, h, sea_y0=104, sea_y1=176, office=True):
    k.sky4(w, h, sea_y1)
    k.headland(14, 190, sea_y1 - 1, 34); k.lighthouse(80, sea_y1 + 18, 56)
    k.sea4(14, w - 14, sea_y0, sea_y1)
    k.quay(w, sea_y0 + 4)
    if office: k.office(300, sea_y0 + 2, 180, 210)

# ----------------------------------------------------------------------------- 1. harbour: Quill chalks the tide board
def harbour_plate(k, w, h):
    frame_open(k, w, h); harbour_backdrop(k, w, h)
    k.bunting(310, 482, 252, sag=12, n=0)       # the string only: the flags are animated parts
    k.board(116, 92, 130, 128, high=False)
    k.lobster_pot(470, 106, 28); k.bollard(30, 100, 14)
    k.unclip()

BUNT = [(310 + (482 - 310) * (i + 0.5) / 9, 252 - 12 * math.sin(math.pi * (i + 0.5) / 9)) for i in range(9)]
def flag(k, w, h, v, i=0, pts=BUNT, size=8):
    frame_open(k, w, h); px, py = pts[i]
    k.shape([(px - size / 2, py), (px + size / 2, py), (px, py - size * 1.2)], lw=0.5, fill=PAL.bunting[i % len(PAL.bunting)], amp=0)
    k.unclip()

def pennant(k, w, h, v, x=482, y=330):
    frame_open(k, w, h)
    with k.tint(C(200, 70, 64)): k.shape([(x, y), (x + 26, y - 5), (x, y - 11)], lw=0.6, fill=Wt, amp=0)
    k.unclip()

def chalk_line(k, w, h, v):
    frame_open(k, w, h); k.board_high(116, 92, 130, 128); k.unclip()

def quill_chalk(k, w, h, v): frame_open(k, w, h); P4.quill(k, 300, 40, 226, flip=True, arm="chalk"); k.unclip()
def agnes_walk(k, w, h, v): frame_open(k, w, h); P4.agnes(k, 64, 34, 208); k.unclip()
def boat_part(k, w, h, v, x=0, y=0, bw=40, col=BOATRED, sail=True, sailcol=None):
    frame_open(k, w, h); k.boat4(x, y, bw, col, sail=sail, sailcol=sailcol); k.unclip()
def cloud_part(k, w, h, v, x=0, y=0, s_=1.0):
    frame_open(k, w, h)
    for (dx, dy, r) in ((0, 0, 16), (16, 4, 13), (-15, 2, 11), (6, 10, 11), (28, -1, 9)):
        k.circle(x + dx * s_, y + dy * s_, r * s_, lw=0, fill=PAL.cloud, stroke=False)
    k.unclip()

# fx sprites (small pages)
def gull_fx(k, w, h, v):
    up = {"f0": 1.0, "f1": 0.45, "f2": -0.1, "f3": -0.5}[v]; x, y = w / 2, h / 2
    for sg in (-1, 1):
        tip = (x + sg * w * 0.46, y + up * h * 0.4); mid = (x + sg * w * 0.22, y + up * h * 0.25 + h * 0.18)
        k.line([(x + sg * 1.5, y), mid, tip], lw=1.0, amp=0, color=C(60, 64, 72))
    k.shape(k.arcpts(x, y - 0.6, 3.2, 1.6, 0, 360, 12), lw=0.5, fill=PAL.cloud, amp=0)
def wave_fx(k, w, h, v):
    L = {"w0": 0.9, "w1": 0.7, "w2": 0.5}[v] * w; x0 = (w - L) / 2
    k.line([(x0 + L * t, h / 2 + 1.1 * math.sin(t * math.pi * 2 + 0.6)) for t in [i / 12 for i in range(13)]], lw=0.9, amp=0, color=C(248, 252, 252))
def glint_fx(k, w, h, v):
    r = w * (0.42 if v == "s0" else 0.3); x, y = w / 2, h / 2
    k.shape([(x - r, y), (x - r * 0.18, y + r * 0.18), (x, y + r), (x + r * 0.18, y + r * 0.18), (x + r, y), (x + r * 0.18, y - r * 0.18), (x, y - r), (x - r * 0.18, y - r * 0.18)], lw=0, stroke=False, fill=C(255, 252, 230), amp=0)
def steam_fx(k, w, h, v):
    ph = {"s0": 0, "s1": 1.6, "s2": 3.1}[v]
    pts = [(w / 2 + 2.6 * math.sin(t * 5 + ph), 2 + t * (h - 4)) for t in [i / 16 for i in range(17)]]
    k.line(pts, lw=1.1, amp=0, color=C(255, 255, 255)); k.line([(x + 1.6, y) for x, y in pts[3:]], lw=0.6, amp=0, color=C(240, 240, 240))

# ----------------------------------------------------------------------------- 2. sandbar at low / high tide
SAND_PTS = [(60, 116), (110, 128), (170, 136), (240, 140), (300, 136), (350, 126), (392, 116)]
def sandbar_plate(k, w, h, high=False):
    frame_open(k, w, h)
    k.sky4(w, h, 236)
    for (cx, cy, s_) in ((w * 0.2, h * 0.84, 1.0), (w * 0.62, h * 0.9, 0.7)): pass
    k.headland(14, 150, 235, 24, col=PAL.headland); k.headland(330, w - 14, 235, 18, col=shade(PAL.headland, 0.95))
    k.sea4(14, w - 14, 70, 236, rows=8)
    if not high:   # the long ridge of sand, wet at the edges, with cockle diggers' holes and footprints
        top = [(x, y + 2) for x, y in SAND_PTS]
        k.shape([(40, 112)] + top + [(412, 112)], lw=0.9, fill=SAND, amp=0.4)
        k.wash([(40, 112)] + [(x, y - 6) for x, y in SAND_PTS] + [(412, 112)], SAND_WET)
        rr = random.Random(9)
        for i in range(26):
            x = rr.uniform(80, 370); y = rr.uniform(118, 132)
            if rr.random() < 0.6: k.shape(k.arcpts(x, y, 2.2, 0.9, 0, 360, 8), lw=0.3, fill=SAND_WET, amp=0)
            else: k.line([(x, y), (x + 2, y + 0.4)], lw=0.5, amp=0, color=shade(SAND, 0.7))
        k.line([(40, 112), (412, 112)], lw=0.6, amp=0.4, color=PAL.foam)
        for (bx, by) in ((150, 129), (260, 133)):   # buckets and forks left on the sand
            k.shape([(bx - 4, by), (bx + 4, by), (bx + 5, by + 8), (bx - 5, by + 8)], lw=0.6, fill=C(110, 150, 200), amp=0)
    else:
        k.wash([(40, 112)] + [(x, y + 26) for x, y in SAND_PTS] + [(412, 112)], mix(SEA, SEA2, 0.5))
        rr = random.Random(11)
        for j in range(5):
            y = 120 + j * 9
            for i in range(5):
                x = rr.uniform(60, 380); L = rr.uniform(12, 24)
                k.line([(x + L * t, y + 1.0 * math.sin(t * 6.28)) for t in [q / 8 for q in range(9)]], lw=0.45, amp=0, color=shade(SEA2, 0.86))
    k.gull_rock(420, 150, 120, 120)
    k.wash_rect(14, 14, w - 14, 62, SAND)   # foreground beach
    k.line([(14, 62), (w - 14, 66)], lw=0.8, amp=0.4, color=PAL.foam)
    rr = random.Random(4)
    for i in range(14):
        x, y = rr.uniform(30, w - 30), rr.uniform(20, 56)
        k.shape(k.arcpts(x, y, 2.4, 1.6, 0, 180, 8) + [(x - 2.4, y)], lw=0.4, fill=rr.choice([PAL.cloud, C(240, 200, 190), C(230, 220, 200)]), amp=0)
    k.unclip()

def diggers(k, w, h, v):
    frame_open(k, w, h)
    for (x, col, hat) in ((176, PAL.walls[1], PAL.straw), (226, PAL.walls[2], None), (300, PAL.walls[0], None)):
        F.guest(k, x, 132, 30, col, hat=hat, hair=PAL.hair_dark if hat is None else None)
        k.shape([(x + 6, 132), (x + 10, 132), (x + 10.6, 137), (x + 5.4, 137)], lw=0.45, fill=C(110, 150, 200), amp=0)
    k.unclip()

def ghost(k, w, h, v):
    """Solution: a dashed outline of a digger standing on the sandbar, labelled with Mr Rundle's claim."""
    frame_open(k, w, h)
    k.c.saveState(); k.c.setDash(3, 2); k.c.setStrokeColor(C(150, 50, 40)); k.c.setLineWidth(1.0)
    x, y, hh = 236, 140, 54
    k.c.circle(x, y + hh * 0.86, hh * 0.1, stroke=1, fill=0)
    p = k.c.beginPath(); p.moveTo(x - hh * 0.12, y + hh * 0.74); p.lineTo(x + hh * 0.12, y + hh * 0.74); p.lineTo(x + hh * 0.16, y + hh * 0.36); p.lineTo(x - hh * 0.16, y + hh * 0.36); p.close(); k.c.drawPath(p, stroke=1, fill=0)
    k.c.line(x - hh * 0.06, y + hh * 0.36, x - hh * 0.08, y); k.c.line(x + hh * 0.06, y + hh * 0.36, x + hh * 0.08, y)
    k.c.line(x + hh * 0.12, y + hh * 0.66, x + hh * 0.36, y + hh * 0.2); k.c.restoreState()
    lab = "\u201cDigging here, 11 until 1\u201d"
    tw = k.c.stringWidth(lab, "Ink-CrimsonI", 15)
    k.shape([(x - tw / 2 - 10, y + hh + 10), (x + tw / 2 + 10, y + hh + 10), (x + tw / 2 + 10, y + hh + 32), (x - tw / 2 - 10, y + hh + 32)], lw=0.9, fill=PAL.card, amp=0.2)
    k.text(x, y + hh + 15.5, lab, size=15, font="Ink-CrimsonI", color=C(150, 50, 40))
    k.unclip()

def tideboard_inset(k, w, h, v):
    frame_open(k, w, h); k.board(30, 252, 120, 86, high=True, legs=False, scale=1.0); k.unclip()

def depth(k, w, h, v):
    """Solution: the depth of water over the sandbar at noon, against a man's height."""
    frame_open(k, w, h)
    x = 318; ytop, ybot = 228, 138
    col = C(150, 50, 40)
    k.line([(x, ybot + 2), (x, ytop - 2)], lw=1.4, amp=0, color=col)
    for (yy, sg) in ((ytop, 1), (ybot, -1)): k.shape([(x - 5, yy - sg * 8), (x + 5, yy - sg * 8), (x, yy)], lw=0, stroke=False, fill=col, amp=0)
    k.c.saveState(); k.c.setDash(2, 2); k.c.setStrokeColor(col); k.c.setLineWidth(0.9)
    sx = 352; hh = 66   # a man's height, for scale
    k.c.circle(sx, ybot + hh * 0.9, hh * 0.09, stroke=1, fill=0); k.c.line(sx, ybot + hh * 0.81, sx, ybot + hh * 0.4)
    k.c.line(sx, ybot + hh * 0.4, sx - 7, ybot); k.c.line(sx, ybot + hh * 0.4, sx + 7, ybot); k.c.line(sx - 10, ybot + hh * 0.62, sx + 10, ybot + hh * 0.62)
    k.c.restoreState()
    lab1, lab2 = "more than a", "man\u2019s height of sea"
    for j, lab in enumerate((lab1, lab2)):
        tw = k.c.stringWidth(lab, "Ink-CrimsonI", 14)
        if j == 0: k.shape([(x - 128, ytop - 30), (x - 8, ytop - 30), (x - 8, ytop + 8), (x - 128, ytop + 8)], lw=0.9, fill=PAL.card, amp=0.2)
        k.text(x - 68, ytop - 6 - j * 17, lab, size=14, font="Ink-CrimsonI", color=col)
    k.unclip()

# ----------------------------------------------------------------------------- 3. inside the office: the windowsill
WIN = (112, 150, 228, 186)   # window x, y, w, h
def window_plate(k, w, h, hook=False):
    frame_open(k, w, h)
    k.wash_rect(14, 14, w - 14, h - 14, WALLW)
    k.wash_rect(14, 14, w - 14, 104, PANEL)   # panelled dado
    for i in range(int((w - 28) / 46) + 1):
        x = 20 + i * 46
        if x + 38 < w - 14: k.rect(x, 22, 38, 72, lw=0.5, fill=shade(PANEL, 0.93))
    k.line([(14, 104), (w - 14, 104)], lw=0.9, amp=0.1)
    x, y, ww, hh = WIN
    # the view: sky, sea, a distant headland
    k.vgrad(x, y + hh * 0.42, x + ww, y + hh, PAL.sky, PAL.sky2, steps=10)
    k.headland(x, x + ww * 0.45, y + hh * 0.42, 14)
    k.vgrad(x, y, x + ww, y + hh * 0.42, SEA, SEA2, steps=8)
    k.lighthouse(x + ww * 0.82, y + hh * 0.42, 40)
    # deep sill
    k.rect(x - 16, y - 12, ww + 32, 12, lw=1.0, fill=PAL.cloud)
    k.rect(x - 20, y - 18, ww + 40, 6, lw=0.8, fill=shade(PAL.cloud, 0.92))
    # ship's wheel, chart and clock face (hands are parts)
    cx, cy, R = 54, 262, 30
    for i in range(8):
        a = math.radians(i * 45); k.line([(cx + R * 0.2 * math.cos(a), cy + R * 0.2 * math.sin(a)), (cx + R * 1.3 * math.cos(a), cy + R * 1.3 * math.sin(a))], lw=2.2, amp=0, color=PAL.wood_dk)
        k.circle(cx + R * 1.32 * math.cos(a), cy + R * 1.32 * math.sin(a), 3, lw=0.6, fill=PAL.wood)
    k.circle(cx, cy, R, lw=1.6, fill=None); k.circle(cx, cy, R * 0.86, lw=0.6, fill=None); k.circle(cx, cy, R * 0.22, lw=0.8, fill=PAL.brass)
    k.rect(370, 168, 116, 86, lw=0.8, fill=C(240, 230, 200))   # chart of the bay
    k.wash([(374, 172), (482, 172), (482, 204), (450, 214), (410, 206), (374, 220)], C(196, 222, 228))
    k.line([(374, 220), (410, 206), (450, 214), (482, 204)], lw=0.6, amp=0.4)
    k.text(428, 236, "TIDEWHISTLE BAY", size=8, font="Ink-Plex", color=PAL.navy)
    for (px, py) in ((372, 252), (484, 252), (372, 170), (484, 170)): k.circle(px, py, 1.6, lw=0.4, fill=C(200, 70, 60))
    ccx, ccy, cr = 428, 318, 30
    k.circle(ccx, ccy, cr + 4, lw=1.0, fill=PAL.wood); k.circle(ccx, ccy, cr, lw=0.8, fill=C(252, 250, 240))
    for i in range(12):
        a = math.radians(90 - i * 30); L = 0.84 if i % 3 else 0.74
        k.line([(ccx + cr * 0.92 * math.cos(a), ccy + cr * 0.92 * math.sin(a)), (ccx + cr * L * math.cos(a), ccy + cr * L * math.sin(a))], lw=0.9 if i % 3 == 0 else 0.5, amp=0)
    k.text(ccx, ccy + cr * 0.42, "XII", size=6, font="Ink-Playfair")
    # desk with the ledger and a lamp
    k.rect(360, 84, 140, 8, lw=0.9, fill=PAL.wood_dk); k.rect(366, 20, 128, 64, lw=0.9, fill=PAL.wood)
    with k.tint(PAL.wood): k.hatch([(366, 20), (494, 20), (494, 84), (366, 84)], angle=0, gap=2.2, lw=0.3)
    k.rect(380, 92, 46, 8, lw=0.7, fill=C(150, 72, 68)); k.rect(382, 99, 42, 3, lw=0.4, fill=PAL.cloud)
    k.line([(462, 92), (462, 128), (476, 140)], lw=1.4, amp=0, color=C(60, 90, 80))
    k.shape([(466, 140), (490, 140), (482, 152), (470, 152)], lw=0.8, fill=C(92, 140, 120), amp=0)
    if hook: pass
    k.unclip()

def mullions(k, w, h, v):
    frame_open(k, w, h); x, y, ww, hh = WIN
    k.c.setStrokeColor(K); k.c.setLineWidth(1.2); k.c.rect(x, y, ww, hh, stroke=1, fill=0)
    for (x0, y0, x1, y1) in ((x + ww / 2, y, x + ww / 2, y + hh), (x, y + hh * 0.55, x + ww, y + hh * 0.55)):
        k.rect(min(x0, x1) - 2.5 if x0 == x1 else x0, min(y0, y1) - 2.5 if y0 == y1 else y0, 5 if x0 == x1 else x1 - x0, 5 if y0 == y1 else y1 - y0, lw=0.7, fill=PAL.cloud)
    k.rect(x - 8, y - 2, 8, hh + 4, lw=0.8, fill=PAL.cloud); k.rect(x + ww, y - 2, 8, hh + 4, lw=0.8, fill=PAL.cloud); k.rect(x - 8, y + hh, ww + 16, 8, lw=0.8, fill=PAL.cloud)
    for sg in (-1, 1):   # curtains
        cx0 = x - 8 if sg < 0 else x + ww + 8
        pts = [(cx0, y + hh + 14), (cx0 - sg * 30, y + hh + 14), (cx0 - sg * 24, y + hh * 0.5), (cx0 - sg * 34, y - 14), (cx0, y - 14)]
        with k.tint(C(214, 120, 110), hatch=C(180, 96, 90)): k.shape(pts, lw=0.8, fill=Wt, amp=0.3); k.hatch(pts, angle=90, gap=3.0, lw=0.35)
    k.rect(x - 46, y + hh + 12, ww + 92, 5, lw=0.7, fill=PAL.wood_dk)
    k.unclip()

CMP = (226, 150, 66)   # compass base centre x, y and width on the sill
def compass_part(k, w, h, v):
    frame_open(k, w, h); k.compass4(*CMP, needle=False); k.unclip()
def needle_part(k, w, h, v):
    frame_open(k, w, h); x, y, cw = CMP; k.needle(x, y + cw * 0.64, cw); k.unclip()
def ring_part(k, w, h, v):
    frame_open(k, w, h); x, y, cw = CMP
    k.c.saveState(); k.c.setDash(2, 2); k.c.setStrokeColor(shade(PAL.cloud, 0.6)); k.c.setLineWidth(0.8)
    k.c.rect(x - cw * 0.55, y + 0.6, cw * 1.1, 2.2, stroke=1, fill=0); k.c.restoreState()
    k.unclip()
def hand_part(k, w, h, v, L=0.5, wd=2.2):
    frame_open(k, w, h); ccx, ccy, cr = 428, 318, 30
    k.shape([(ccx - wd, ccy), (ccx, ccy + cr * L), (ccx + wd, ccy), (ccx, ccy - 4)], lw=0.5, fill=C(40, 40, 46), amp=0)
    k.circle(ccx, ccy, 2.2, lw=0.4, fill=PAL.brass)
    k.unclip()
def win_boat(k, w, h, v):
    frame_open(k, w, h); x, y, ww, hh = WIN; k.boat4(x + ww * 0.3, y + hh * 0.3, 30, BOATRED, sailcol=PAL.cloud); k.unclip()

# ----------------------------------------------------------------------------- 4. Ollie on the quay
def quay_plate(k, w, h):
    frame_open(k, w, h); harbour_backdrop(k, w, h, office=False)
    k.office(330, 106, 170, 200, win_compass=False)
    for (x, y, s_) in ((60, 110, 30), (92, 110, 26), (74, 136, 24)): k.lobster_pot(x, y, s_)
    k.bollard(150, 100, 16); k.rope_coil(196, 92, 40)
    k.flower_tub(306, 108, 18)
    k.unclip()
def ollie_part(k, w, h, v): frame_open(k, w, h); P4.ollie(k, 240, 38, 228); k.unclip()

# ----------------------------------------------------------------------------- 5. lineup: Morwenna | Pip | Mr Rundle
PW = 512
def _church(k, pw, h):
    k.sky4(pw, h, 150)
    k.wash_rect(14, 14, pw - 14, 152, GRASS)
    hill = [(14, 150), (pw * 0.3, 170), (pw * 0.7, 176), (pw - 14, 160), (pw - 14, 14), (14, 14)]
    with k.tint(GRASS, hatch=GRASS2): k.shape(hill, lw=0.8, fill=Wt, amp=0.4); k.hatch(hill, angle=0, gap=6, lw=0.3)
    cx = pw * 0.72
    k.rect(cx - 70, 150, 140, 120, lw=1.0, fill=CHURCH)
    with k.tint(CHURCH, hatch=shade(CHURCH, 0.8)): k.hatch([(cx - 70, 150), (cx + 70, 150), (cx + 70, 270), (cx - 70, 270)], angle=0, gap=5, lw=0.3)
    k.roof(cx - 70, cx + 70, 270, 318, overhang=6, color=PAL.slate)
    k.rect(cx - 112, 150, 44, 186, lw=1.0, fill=CHURCH)   # tower
    with k.tint(CHURCH, hatch=shade(CHURCH, 0.8)): k.hatch([(cx - 112, 150), (cx - 68, 150), (cx - 68, 336), (cx - 112, 336)], angle=0, gap=5, lw=0.3)
    for i in range(5): k.rect(cx - 114 + i * 10, 336, 6, 8, lw=0.6, fill=CHURCH)
    k.window(cx - 98, 280, 16, 26, arch=True)
    k.shape([(cx - 16, 150), (cx + 16, 150), (cx + 16, 196)] + [(cx + 16 * math.cos(math.radians(a)), 196 + 16 * math.sin(math.radians(a))) for a in range(0, 181, 15)] + [(cx - 16, 196)], lw=1.0, fill=C(120, 84, 64), amp=0)
    for wx in (cx + 36, cx - 50): k.window(wx, 200, 16, 34, arch=True)
    for gx in (40, 92, 140):
        k.shape([(gx - 7, 150), (gx + 7, 150), (gx + 7, 170)] + [(gx + 7 * math.cos(math.radians(a)), 170 + 7 * math.sin(math.radians(a))) for a in range(0, 181, 30)] + [(gx - 7, 170)], lw=0.7, fill=STONE, amp=0)
    k.flower_urn(cx + 50, 128, 32); k.flower_urn(cx - 40, 128, 32)

def _tearoom(k, pw, h):
    k.wash_rect(14, 96, pw - 14, h - 14, TEAWALL)
    k.vgrad(14, 14, pw - 14, 96, PAL.floor, PAL.floor2, steps=8)
    for i in range(8): k.line([(14, 14 + i * 11), (pw - 14, 14 + i * 11)], lw=0.35, amp=0.2, color=shade(PAL.floor2, 0.75))
    k.line([(14, 96), (pw - 14, 96)], lw=0.9, amp=0.1)
    k.wash_rect(14, 96, pw - 14, 130, C(196, 222, 214))   # tiled dado
    for i in range(int((pw - 28) / 16) + 1): k.line([(14 + i * 16, 96), (14 + i * 16, 130)], lw=0.3, amp=0, color=shade(C(196, 222, 214), 0.8))
    k.line([(14, 130), (pw - 14, 130)], lw=0.7, amp=0.1)
    k.rect(40, 200, 120, 110, lw=1.0, fill=PAL.sky)   # window with a view of the harbour
    k.vgrad(42, 202, 158, 250, SEA, SEA2, steps=6); k.text(100, 318, "THE KETTLE AND GULL", size=11, font="Ink-Plex", color=PAL.navy)
    k.line([(100, 200), (100, 310)], lw=1.2, amp=0); k.line([(40, 255), (160, 255)], lw=1.2, amp=0)
    for j in range(3):   # shelf of cups and teapots
        k.rect(300, 240 + j * 0, 180, 5, lw=0.7, fill=PAL.wood)
    for i in range(6):
        with k.tint([PAL.teapot, PAL.walls[2], PAL.walls[1], PAL.pea_purple, PAL.walls[3], PAL.walls[0]][i]): k.cup(318 + i * 28, 245, 14)
    k.rect(296, 70, 190, 70, lw=1.0, fill=PAL.wood)   # counter
    with k.tint(PAL.wood): k.hatch([(296, 70), (486, 70), (486, 140), (296, 140)], angle=0, gap=2.4, lw=0.3)
    k.rect(290, 140, 202, 7, lw=0.9, fill=PAL.wood_dk)
    with k.tint(PAL.teapot): k.teapot(450, 147, 34)
    k.shape(k.arcpts(380, 150, 18, 4, 0, 360, 16), lw=0.6, fill=PAL.cloud, amp=0)   # cake stand
    for (sx, sy) in ((372, 154), (384, 155)): k.shape(k.arcpts(sx, sy, 5, 4, 0, 180, 8) + [(sx - 5, sy)], lw=0.5, fill=P4.SCONE, amp=0)
    # broom leaning by the door
    k.line([(36, 30), (70, 170)], lw=2.0, amp=0, color=PAL.wood_dk)
    k.shape([(26, 14), (48, 14), (40, 36), (32, 36)], lw=0.7, fill=C(214, 180, 110), amp=0)

def _beach(k, pw, h):
    k.sky4(pw, h, 196)
    k.headland(240, pw - 14, 195, 20)
    k.sea4(14, pw - 14, 120, 196)
    k.gull_rock(420, 168, 70, 64)
    k.wash_rect(14, 14, pw - 14, 120, SAND)
    k.line([(14, 120), (pw - 14, 124)], lw=0.8, amp=0.4, color=PAL.foam)
    rr = random.Random(7)
    for i in range(20):
        x, y = rr.uniform(24, pw - 24), rr.uniform(20, 112)
        k.shape(k.arcpts(x, y, 2.2, 1.4, 0, 180, 8) + [(x - 2.2, y)], lw=0.35, fill=rr.choice([PAL.cloud, C(240, 200, 190)]), amp=0)
    k.boat4(90, 132, 50, BOATBLUE, sail=False)
    # Mr Rundle's sandy bucket at his feet
    bx, by = 290, 70
    k.shape([(bx - 13, by), (bx + 13, by), (bx + 16, by + 26), (bx - 16, by + 26)], lw=0.9, fill=C(110, 150, 200), amp=0)
    k.shape(k.arcpts(bx, by + 26, 16, 4, 0, 360, 18), lw=0.7, fill=SAND_WET, amp=0)
    k.line(k.arcpts(bx, by + 26, 15, 18, 10, 170, 12), lw=0.8, amp=0, color=C(90, 90, 100))
    for (sx, sy) in ((bx - 6, by + 27.5), (bx + 4, by + 28)): k.shape(k.arcpts(sx, sy, 3, 2, 0, 180, 8) + [(sx - 3, sy)], lw=0.4, fill=C(236, 226, 206), amp=0)
    for i in range(10): k.circle(bx + rr.uniform(-18, 18), by + rr.uniform(-2, 2), 0.8, lw=0, fill=SAND_WET, stroke=False)

def lineup_plate(k, w, h):
    for i in range(3):
        k.c.saveState(); k.c.translate(i * PW, 0); pw = PW
        k.frame2(pw, h); k.clip_rect(14, 14, pw - 14, h - 14); cx = pw / 2
        [_church, _tearoom, _beach][i](k, pw, h)
        nameplate(k, cx, 40, ["MORWENNA DAY", "PIP CAREW", "MR RUNDLE"][i])
        k.unclip(); k.c.restoreState()

def lineup_fig(k, w, h, v, i=0, who="morwenna", **kw):
    k.c.saveState(); k.c.translate(i * PW, 0); k.clip_rect(14, 14, PW - 14, h - 14)
    getattr(P4, who)(k, PW / 2 - 46, 70, 236, **kw)
    k.unclip(); k.c.restoreState()
def lineup_vicar(k, w, h, v): k.c.saveState(); k.clip_rect(14, 14, PW - 14, h - 14); P4.vicar(k, PW / 2 + 150, 80, 206); k.unclip(); k.c.restoreState()
def lineup_agnes(k, w, h, v): k.c.saveState(); k.c.translate(PW, 0); k.clip_rect(14, 14, PW - 14, h - 14); P4.agnes(k, PW / 2 + 130, 80, 200, basket=False); k.unclip(); k.c.restoreState()

# ----------------------------------------------------------------------------- 6. Agnes at the blackboard
def thinking_plate(k, w, h):
    frame_open(k, w, h)
    k.sky4(w, h, 170); k.sea4(14, w - 14, 110, 172); k.headland(300, w - 14, 171, 20); k.quay(w, 114)
    k.board(196, 70, 270, 236, high=True)
    k.unclip()
def agnes_think(k, w, h, v): frame_open(k, w, h); P4.agnes(k, 110, 30, 236); k.unclip()

# ----------------------------------------------------------------------------- 7. the boat (solution)
def boat_plate(k, w, h):
    frame_open(k, w, h)
    k.vgrad(14, 14, w - 14, h - 14, SEA, SEA2, steps=14)
    rr = random.Random(3)
    for j in range(10):
        y = 30 + j * 34
        for i in range(4):
            x = rr.uniform(20, w - 60); L = rr.uniform(16, 30)
            k.line([(x + L * t, y + 1.2 * math.sin(t * 6.28)) for t in [q / 8 for q in range(9)]], lw=0.5, amp=0, color=shade(SEA2, 0.86))
    hull = [(40, 70), (w * 0.5, 40), (w - 40, 70), (w - 20, 200), (w * 0.5, 330), (20, 200)]
    with k.tint(BOATBLUE, hatch=shade(BOATBLUE, 0.7)): k.shape(hull, lw=1.4, fill=Wt, amp=0.3)
    inner = [(58, 82), (w * 0.5, 56), (w - 58, 82), (w - 40, 198), (w * 0.5, 312), (40, 198)]
    with k.tint(PAL.wood): k.shape(inner, lw=1.0, fill=Wt, amp=0.3)
    k.c.saveState(); k.c.clipPath(k.path(inner, closed=True), stroke=0, fill=0)
    for i in range(14): k.line([(14, 60 + i * 20), (w - 14, 60 + i * 20)], lw=0.5, amp=0.2, color=shade(PAL.wood, 0.7))
    k.c.restoreState()
    for ty in (120, 236):   # thwarts
        k.rect(40, ty, w - 80, 16, lw=1.0, fill=PAL.wood_dk)
    k.shape([(80, 150), (190, 140), (220, 196), (120, 214), (70, 190)], lw=0.8, fill=NET, amp=0.6)   # heap of nets
    with k.tint(NET):
        for i in range(10): k.line([(84 + i * 12, 150), (100 + i * 10, 208)], lw=0.4, amp=0.3, color=shade(NET, 0.6))
    k.circle(410, 180, 14, lw=0.9, fill=BUOY); k.line([(410, 194), (430, 214)], lw=0.8, amp=0.2)
    k.line([(330, 90), (470, 300)], lw=4, amp=0, color=PAL.wood); k.line([(330, 90), (470, 300)], lw=0.6, amp=0)   # an oar
    k.unclip()
def boat_compass(k, w, h, v): frame_open(k, w, h); k.compass4(286, 146, 58); k.unclip()
def boat_rope(k, w, h, v): frame_open(k, w, h); k.rope_coil(286, 150, 120); k.unclip()
def sparkle_part(k, w, h, v):
    frame_open(k, w, h); x, y, r = 300, 196, 12
    k.shape([(x - r, y), (x - r * 0.16, y + r * 0.16), (x, y + r), (x + r * 0.16, y + r * 0.16), (x + r, y), (x + r * 0.16, y - r * 0.16), (x, y - r), (x - r * 0.16, y - r * 0.16)], lw=0, stroke=False, fill=C(255, 250, 220), amp=0)
    k.unclip()

# ----------------------------------------------------------------------------- 8. returned: the compass goes home
def returned_plate(k, w, h):
    frame_open(k, w, h)
    k.sky4(w, h, 120); k.sea4(14, w - 14, 100, 122, rows=3); k.quay(w, 104)
    k.office(110, 102, 300, 300, win_compass=False)
    k.bunting(30, 110, 300, sag=8, n=0)
    k.unclip()
RET_BUNT = [(30 + 80 * (i + 0.5) / 4, 300 - 8 * math.sin(math.pi * (i + 0.5) / 4)) for i in range(4)]
def quill_ret(k, w, h, v):
    frame_open(k, w, h); P4.quill(k, 170, 44, 236, arm="compass" if v.startswith("compass") else "down"); k.unclip()
def rundle_ret(k, w, h, v):
    frame_open(k, w, h)
    if v.startswith("base"): P4.rundle(k, 346, 44, 236, expr="sheepish", compass=True)
    elif v.startswith("given"): P4.rundle(k, 346, 44, 236, expr="sheepish", prop=False)
    else: P4.rundle(k, 346, 44, 236, expr="kind", prop=False)
    k.unclip()

# ----------------------------------------------------------------------------- hook cast strip and title vignette
def cast_plate(k, w, h):
    k.wash_rect(0, 0, w, h, PAL.sky2)
    k.vgrad(0, 30, w, 84, SEA, SEA2, steps=6); k.wash_rect(0, 0, w, 30, SAND)
    k.line([(0, 30), (w, 31)], lw=0.8, amp=0.3, color=PAL.foam)
    k.c.setStrokeColor(K); k.c.setLineWidth(1.3); k.c.rect(1, 1, w - 2, h - 2, stroke=1, fill=0)
def cast_fig(k, w, h, v, i=0, who="morwenna"):
    getattr(P4, who)(k, w * (0.17 + 0.32 * i), 20, h * 0.8)

def vignette(k, w, h):
    k.circle(w / 2, h / 2, w * 0.46, lw=1.3, fill=PAL.cloud); k.circle(w / 2, h / 2, w * 0.44, lw=0.45, fill=None)
    k.c.saveState(); p = k.c.beginPath(); p.circle(w / 2, h / 2, w * 0.44 - 1); k.c.clipPath(p, stroke=0, fill=0)
    k.vgrad(0, h * 0.45, w, h, PAL.sky, PAL.sky2, steps=10); k.vgrad(0, h * 0.25, w, h * 0.46, SEA, SEA2, steps=6)
    k.gull_rock(w * 0.74, h * 0.45, 90, 80); k.wash_rect(0, 0, w, h * 0.26, SAND); k.line([(0, h * 0.26), (w, h * 0.27)], lw=0.8, amp=0.3, color=PAL.foam)
    k.compass4(w * 0.36, h * 0.2, 120)
    k.gull(w * 0.3, h * 0.82, 20); k.gull(w * 0.44, h * 0.88, 14)
    k.c.restoreState()

# ============================================================================= jobs
AW, AH = 512, 384
V3 = ["base", "base+blink", "base+talk"]; V2 = ["base", "base+blink"]
FX = dict(gull=dict(fn=gull_fx, variants=["f0", "f1", "f2", "f3"], page=(44, 22)),
          wave=dict(fn=wave_fx, variants=["w0", "w1", "w2"], page=(30, 5)),
          glint=dict(fn=glint_fx, variants=["s0", "s1"], page=(10, 10)))
STEAM = dict(steam=dict(fn=steam_fx, variants=["s0", "s1", "s2"], page=(12, 22)))

def jobs():
    J = []
    hp = dict(quill=dict(fn=quill_chalk, variants=V3), agnes=dict(fn=agnes_walk, variants=V2), chalk=dict(fn=chalk_line, variants=["base"]),
              boat1=dict(fn=partial(boat_part, x=272, y=140, bw=34, col=BOATRED), variants=["base"]),
              boat2=dict(fn=partial(boat_part, x=36, y=152, bw=20, col=BOATBLUE, sailcol=C(250, 230, 190)), variants=["base"]),
              cloud1=dict(fn=partial(cloud_part, x=120, y=330, s_=1.0), variants=["base"]), cloud2=dict(fn=partial(cloud_part, x=330, y=350, s_=0.7), variants=["base"]),
              pennant=dict(fn=pennant, variants=["base"]), **FX)
    for i in range(9): hp[f"flag{i}"] = dict(fn=partial(flag, i=i), variants=["base"])
    J.append(dict(name="harbour", w=AW, h=AH, plate=harbour_plate, parts=hp, seed=41))
    J.append(dict(name="sandbar", w=AW, h=AH, plate=sandbar_plate, seed=42, parts=dict(diggers=dict(fn=diggers, variants=["base"]), ghost=dict(fn=ghost, variants=["base"]),
              tideboard=dict(fn=tideboard_inset, variants=["base"]), depth=dict(fn=depth, variants=["base"]),
              cloud1=dict(fn=partial(cloud_part, x=100, y=330, s_=1.1), variants=["base"]), cloud2=dict(fn=partial(cloud_part, x=360, y=300, s_=0.8), variants=["base"]), **FX)))
    J.append(dict(name="sandbar_high", w=AW, h=AH, plate=partial(sandbar_plate, high=True), seed=42))
    J.append(dict(name="window", w=AW, h=AH, plate=window_plate, seed=43, parts=dict(compass=dict(fn=compass_part, variants=["base"]), needle=dict(fn=needle_part, variants=["base"]),
              ring=dict(fn=ring_part, variants=["base"]), mullions=dict(fn=mullions, variants=["base"]), boat=dict(fn=win_boat, variants=["base"]),
              hour=dict(fn=partial(hand_part, L=0.5, wd=2.4), variants=["base"]), minute=dict(fn=partial(hand_part, L=0.82, wd=1.6), variants=["base"]), **FX)))
    J.append(dict(name="quay", w=AW, h=AH, plate=quay_plate, seed=44, parts=dict(ollie=dict(fn=ollie_part, variants=V2),
              boat1=dict(fn=partial(boat_part, x=168, y=146, bw=40, col=PAL.doors[3]), variants=["base"]),
              boat2=dict(fn=partial(boat_part, x=110, y=160, bw=28, col=BOATBLUE), variants=["base"]),
              cloud1=dict(fn=partial(cloud_part, x=200, y=330, s_=0.9), variants=["base"]), **FX)))
    J.append(dict(name="lineup", w=3 * PW, h=AH, plate=lineup_plate, seed=45, parts=dict(
              morwenna=dict(fn=partial(lineup_fig, i=0, who="morwenna"), variants=V2), pip=dict(fn=partial(lineup_fig, i=1, who="pip"), variants=V2),
              rundle=dict(fn=partial(lineup_fig, i=2, who="rundle"), variants=V3), vicar=dict(fn=lineup_vicar, variants=V2), agnes=dict(fn=lineup_agnes, variants=V2),
              cloud1=dict(fn=partial(cloud_part, x=120, y=330, s_=1.0), variants=["base"]), boat=dict(fn=partial(boat_part, x=2 * PW + 340, y=150, bw=30, col=BOATRED), variants=["base"]),
              **FX, **STEAM)))
    J.append(dict(name="thinking", w=AW, h=AH, plate=thinking_plate, seed=46, parts=dict(agnes=dict(fn=agnes_think, variants=V2),
              boat1=dict(fn=partial(boat_part, x=164, y=138, bw=26, col=BOATBLUE), variants=["base"]), **FX)))
    J.append(dict(name="boat", w=AW, h=AH, plate=boat_plate, seed=47, parts=dict(compass=dict(fn=boat_compass, variants=["base"]), rope=dict(fn=boat_rope, variants=["base"]),
              sparkle=dict(fn=sparkle_part, variants=["base"]), **FX)))
    rp = dict(quill=dict(fn=quill_ret, variants=["base", "base+blink", "compass", "compass+blink"]),
              rundle=dict(fn=rundle_ret, variants=["base", "given", "smile", "smile+blink"]),
              cloud1=dict(fn=partial(cloud_part, x=420, y=340, s_=0.9), variants=["base"]), **FX)
    for i in range(4): rp[f"flag{i}"] = dict(fn=partial(flag, i=i, pts=RET_BUNT), variants=["base"])
    J.append(dict(name="returned", w=AW, h=AH, plate=returned_plate, seed=48, parts=rp))
    J.append(dict(name="cast", w=600, h=260, plate=cast_plate, seed=49, parts={
              who: dict(fn=partial(cast_fig, i=i, who=who), variants=V2) for i, who in enumerate(["morwenna", "pip", "rundle"])}))
    J.append(dict(name="vignette", w=384, h=384, plate=vignette, seed=50))
    J.append(dict(name="hook", w=AW, h=AH, plate=partial(window_plate, hook=True), seed=43, parts=dict(ring=dict(fn=ring_part, variants=["base"]),
              mullions=dict(fn=mullions, variants=["base"]), boat=dict(fn=win_boat, variants=["base"]),
              hour=dict(fn=partial(hand_part, L=0.5, wd=2.4), variants=["base"]), minute=dict(fn=partial(hand_part, L=0.82, wd=1.6), variants=["base"]), **FX)))
    return J

def make_ink(c, seed): return Ink4(c, seed=seed)

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    J = [j for j in jobs() if not want or j["name"] in want]
    save_layers(OUT, J, make_ink)
