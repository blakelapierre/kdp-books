"""Illustrations for Case 9, The Sunset over the Sea: colour-detailed + animation layers (anim.py).
PART sprites use part_open (clip only) — never frame2 — so no border is baked into a moving sprite.
Unique open (render.py HOOK_STYLE="compass"): borderless full-bleed empty easel on the sea front under a
compass-rose title ring, three equal suspect cards, a spinning compass that lands pointing EAST, and a
"ONE STORY FAILS" stamp — geography tease, not the Case 6/7/8 templates. Sunset coral / harbour palette.
Suspects (Tamsin, Hedley, Ashdown) share stance, size and neutral faces until the confession (Ashdown sheepish).
Run: python3 art_case09.py [scene ...]"""
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
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-09")

# ----------------------------------------------------------------------------- harbour / sunset palette
SKY_DUSK = C(255, 186, 140); SKY_DUSK2 = C(255, 140, 110); SKY_DAWN = C(255, 214, 170); SKY_DAWN2 = C(180, 210, 236)
SEA = A4.SEA; SEA2 = A4.SEA2; SAND = C(226, 210, 176); SAND2 = C(200, 184, 150)
WOOD = PAL.wood; WOOD_DK = PAL.wood_dk; CARD = C(250, 242, 226); CARD_EDGE = C(176, 84, 56)
BRASS = PAL.brass; SLATE = C(46, 58, 72); CHALK = C(244, 240, 228); CHALK_Y = C(246, 218, 120)
CHALK_R = C(240, 140, 128); CHALK_G = C(160, 220, 170); CORAL = C(196, 84, 64)

class Ink9(A4.Ink4):
    def stall(s, x, y, w, h):
        """Little seafront stall (awning + counter)."""
        s.rect(x, y, w, h * 0.55, lw=1.0, fill=WOOD)
        s.rect(x - 6, y + h * 0.55, w + 12, 8, lw=0.8, fill=WOOD_DK)
        # striped awning
        s.shape([(x - 10, y + h * 0.55 + 8), (x + w + 10, y + h * 0.55 + 8), (x + w + 4, y + h), (x - 4, y + h)], lw=0.9, fill=C(250, 246, 236), amp=0)
        for i in range(7):
            u0, u1 = i / 7, (i + 1) / 7
            if i % 2 == 0:
                s.shape([(x - 10 + (w + 20) * u0, y + h * 0.55 + 8), (x - 10 + (w + 20) * u1, y + h * 0.55 + 8),
                         (x - 4 + (w + 8) * u1, y + h), (x - 4 + (w + 8) * u0, y + h)], lw=0, fill=CORAL, stroke=False, amp=0)
        s.text(x + w / 2, y + h * 0.28, "DEMELZA'S", size=8, font="Ink-Plex", color=CARD_EDGE)

    def easel(s, x, y, h, painting=True):
        """Tripod easel; painting=True draws the lighthouse-at-dawn watercolour."""
        # legs
        s.line([(x - h * 0.22, y), (x, y + h * 0.92)], lw=2.0, amp=0, color=WOOD_DK)
        s.line([(x + h * 0.22, y), (x, y + h * 0.92)], lw=2.0, amp=0, color=WOOD_DK)
        s.line([(x - h * 0.18, y + h * 0.38), (x + h * 0.18, y + h * 0.38)], lw=1.6, amp=0, color=WOOD)
        s.line([(x, y + h * 0.38), (x, y + h * 0.92)], lw=1.4, amp=0, color=WOOD_DK)
        # canvas board
        cw, ch = h * 0.42, h * 0.34
        s.rect(x - cw / 2, y + h * 0.42, cw, ch, lw=1.0, fill=C(250, 246, 236))
        if painting:
            s.vgrad(x - cw / 2 + 2, y + h * 0.42 + ch * 0.45, x + cw / 2 - 2, y + h * 0.42 + ch - 2, SEA, SEA2, steps=6)
            s.vgrad(x - cw / 2 + 2, y + h * 0.42 + 2, x + cw / 2 - 2, y + h * 0.42 + ch * 0.5, SKY_DAWN, SKY_DAWN2, steps=6)
            s.circle(x - cw * 0.15, y + h * 0.42 + ch * 0.62, cw * 0.08, lw=0, fill=C(255, 210, 120), stroke=False)
            # tiny lighthouse
            s.rect(x + cw * 0.12, y + h * 0.42 + ch * 0.2, cw * 0.08, ch * 0.28, lw=0.4, fill=C(240, 236, 220))
            s.shape([(x + cw * 0.1, y + h * 0.42 + ch * 0.48), (x + cw * 0.22, y + h * 0.42 + ch * 0.48), (x + cw * 0.16, y + h * 0.42 + ch * 0.58)], lw=0.4, fill=CORAL, amp=0)
        else:
            # empty: pale board + "MISSING" tag
            s.line([(x - cw * 0.3, y + h * 0.42 + ch * 0.3), (x + cw * 0.3, y + h * 0.42 + ch * 0.7)], lw=1.2, amp=0, color=C(200, 190, 180))
            s.line([(x - cw * 0.3, y + h * 0.42 + ch * 0.7), (x + cw * 0.3, y + h * 0.42 + ch * 0.3)], lw=1.2, amp=0, color=C(200, 190, 180))
            s.rect(x - 28, y + h * 0.2, 56, 18, lw=0.8, fill=CARD)
            s.text(x, y + h * 0.26, "MISSING", size=9, font="Ink-Plex", color=CORAL)

    def compass_rose(s, cx, cy, r):
        """Decorative compass rose (N E S W)."""
        s.circle(cx, cy, r, lw=1.4, fill=C(250, 246, 236))
        s.circle(cx, cy, r * 0.92, lw=0.6, fill=None)
        for i, lab in enumerate("NESW"):
            a = math.radians(90 - i * 90)
            s.line([(cx, cy), (cx + math.cos(a) * r * 0.78, cy + math.sin(a) * r * 0.78)], lw=0.7 if i % 2 else 1.4, amp=0, color=SLATE if i else CORAL)
            s.text(cx + math.cos(a) * r * 1.12, cy + math.sin(a) * r * 1.12 - 2, lab, size=11, font="Ink-Plex", color=CORAL if i == 1 else SLATE)
        # east wedge filled as a hint (no spoiler text)
        a0, a1 = math.radians(20), math.radians(-20)
        s.shape([(cx, cy), (cx + math.cos(a0) * r * 0.7, cy + math.sin(a0) * r * 0.7), (cx + math.cos(a1) * r * 0.7, cy + math.sin(a1) * r * 0.7)],
                lw=0.5, fill=C(255, 210, 160), amp=0)
        s.circle(cx, cy, r * 0.08, lw=0, fill=BRASS, stroke=False)

    def harbour_front(s, w, h, dusk=False):
        sky1, sky2 = (SKY_DUSK, SKY_DUSK2) if dusk else (SKY_DAWN, SKY_DAWN2)
        s.vgrad(14, 200, w - 14, h - 14, sky1, sky2, steps=10)
        s.vgrad(14, 104, w - 14, 200, SEA, SEA2, steps=8)
        s.wash_rect(14, 14, w - 14, 104, SAND)
        # distant hills (west / behind the village) — only meaningful after the solution, but not a tell alone
        s.shape([(14, 210), (80, 250), (160, 230), (240, 260), (320, 235), (400, 255), (498, 220), (498, 200), (14, 200)], lw=0.6, fill=C(120, 110, 100), amp=0.2)
        # pier posts
        for x in (60, 120, 180, 300, 360):
            s.rect(x, 70, 8, 50, lw=0.6, fill=WOOD_DK)

def plate_open(k, w, h):
    k.frame2(w, h); k.clip_rect(14, 14, w - 14, h - 14)

def part_open(k, w, h):
    k.clip_rect(14, 14, w - 14, h - 14)

def full_open(k, w, h):
    k.clip_rect(0, 0, w, h)

gull_fx = A4.gull_fx; steam_fx = A4.steam_fx

# ----------------------------------------------------------------------------- 1. HOOK hero: empty easel at dusk (full bleed)
def _hook_scene(k, w, h):
    k.harbour_front(w, h, dusk=True)
    k.stall(40, 30, 150, 140)
    k.easel(320, 40, 220, painting=False)
    # soft evening sun disc sinking toward the HILLS (left/back), not the sea — no label
    k.circle(90, 300, 28, lw=0, fill=C(255, 200, 120), stroke=False)

def hook_plate(k, w, h):
    full_open(k, w, h); _hook_scene(k, w, h); k.unclip()

# ----------------------------------------------------------------------------- 2. CAST: three equal suspects
CW, CH = 900, 420
CAST = ["tamsin", "hedley", "ashdown"]
CNAMES = ["TAMSIN TREVELYAN", "HEDLEY TRUSCOTT", "MR ASHDOWN"]

def _fig(k, who, x, y, h, **kw):
    if who == "tamsin": kw.setdefault("prop", "book")
    getattr(P4, who)(k, x, y, h, **kw)

def cast_plate(k, w, h):
    k.wash_rect(0, 0, w, h, C(247, 240, 225))
    for i, who in enumerate(CAST):
        x0 = i * w / 3
        k.shape([(x0 + 12, 12), (x0 + w / 3 - 12, 12), (x0 + w / 3 - 12, h - 12), (x0 + 12, h - 12)], lw=1.4, fill=CARD, amp=0)
        k.wash_rect(x0 + 14, 14, x0 + w / 3 - 14, 56, C(232, 214, 186))
        nameplate(k, x0 + w / 6, 28, CNAMES[i], size=12)

def cast_fig(k, w, h, v, i=0, who="tamsin"):
    x0 = i * w / 3
    k.c.saveState(); k.clip_rect(x0 + 14, 14, x0 + w / 3 - 14, h - 14)
    _fig(k, who, x0 + w / 6, 50, h * 0.72)
    k.c.restoreState()

# ----------------------------------------------------------------------------- 3. Kettle and Gull: Agnes opens shutters on a sunrise-over-sea
def kettle_plate(k, w, h):
    plate_open(k, w, h)
    A4._tearoom(k, w, h)
    # big east window: sunrise climbing out of the sea
    k.rect(300, 160, 180, 160, lw=1.2, fill=SKY_DAWN)
    k.vgrad(302, 162, 478, 240, SEA, SEA2, steps=6)
    k.vgrad(302, 240, 478, 318, SKY_DAWN, SKY_DAWN2, steps=6)
    k.circle(430, 280, 18, lw=0, fill=C(255, 220, 120), stroke=False)
    k.line([(390, 160), (390, 320)], lw=1.2, amp=0); k.line([(300, 240), (480, 240)], lw=1.2, amp=0)
    k.unclip()

def agnes_kettle(k, w, h, v):
    part_open(k, w, h); P4.agnes(k, 140, 22, 240, basket=False); k.unclip()

# ----------------------------------------------------------------------------- 4. seafront stall with painting on easel
def stall_plate(k, w, h):
    plate_open(k, w, h)
    k.harbour_front(w, h, dusk=True)
    k.stall(60, 40, 160, 150)
    k.easel(340, 50, 230, painting=False)  # painting is a part
    k.unclip()

def painting_part(k, w, h, v):
    part_open(k, w, h)
    # redraw only the canvas area of the easel at the same coords
    x, y, hh = 340, 50, 230
    cw, ch = hh * 0.42, hh * 0.34
    k.rect(x - cw / 2, y + hh * 0.42, cw, ch, lw=1.0, fill=C(250, 246, 236))
    k.vgrad(x - cw / 2 + 2, y + hh * 0.42 + ch * 0.45, x + cw / 2 - 2, y + hh * 0.42 + ch - 2, SEA, SEA2, steps=6)
    k.vgrad(x - cw / 2 + 2, y + hh * 0.42 + 2, x + cw / 2 - 2, y + hh * 0.42 + ch * 0.5, SKY_DAWN, SKY_DAWN2, steps=6)
    k.circle(x - cw * 0.15, y + hh * 0.42 + ch * 0.62, cw * 0.08, lw=0, fill=C(255, 210, 120), stroke=False)
    k.rect(x + cw * 0.12, y + hh * 0.42 + ch * 0.2, cw * 0.08, ch * 0.28, lw=0.4, fill=C(240, 236, 220))
    k.shape([(x + cw * 0.1, y + hh * 0.42 + ch * 0.48), (x + cw * 0.22, y + hh * 0.42 + ch * 0.48), (x + cw * 0.16, y + hh * 0.42 + ch * 0.58)], lw=0.4, fill=CORAL, amp=0)
    k.unclip()

def demelza_stall(k, w, h, v):
    part_open(k, w, h); P4.demelza(k, 160, 30, 200); k.unclip()

# ----------------------------------------------------------------------------- 5. bookshop (Tamsin)
def bookshop_plate(k, w, h):
    plate_open(k, w, h)
    k.wash_rect(14, 14, w - 14, h - 14, C(246, 236, 214))
    k.vgrad(14, 14, w - 14, 70, PAL.floor, PAL.floor2, steps=6)
    for j in range(3):
        y = 120 + j * 70
        k.rect(40, y, 200, 8, lw=0.8, fill=WOOD)
        for i in range(8):
            col = [C(160, 90, 90), C(90, 120, 160), C(120, 140, 90), C(160, 130, 70)][i % 4]
            k.rect(48 + i * 24, y + 8, 18, 40 + (i % 3) * 6, lw=0.5, fill=col)
    k.rect(280, 160, 180, 140, lw=1.0, fill=SKY_DAWN)  # window
    k.text(370, 300, "TREVELYAN BOOKS", size=11, font="Ink-Plex", color=CARD_EDGE)
    # little "BOOK CLUB 7–9" slate
    k.rect(300, 80, 140, 40, lw=0.9, fill=SLATE)
    k.text(370, 102, "BOOK CLUB  7–9", size=10, font="Ink-Kalam", color=CHALK)
    k.unclip()

def tamsin_shop(k, w, h, v):
    part_open(k, w, h); P4.tamsin(k, 200, 30, 220, prop="book"); k.unclip()

# ----------------------------------------------------------------------------- 6. inn darts (Hedley)
def inn_plate(k, w, h):
    plate_open(k, w, h)
    k.wash_rect(14, 14, w - 14, h - 14, C(120, 84, 64))
    k.vgrad(14, 14, w - 14, 80, C(90, 70, 55), C(70, 55, 42), steps=6)
    # dartboard
    k.circle(380, 240, 70, lw=1.4, fill=C(240, 236, 220))
    k.circle(380, 240, 55, lw=0.8, fill=None)
    k.circle(380, 240, 20, lw=0.8, fill=C(200, 70, 70))
    for i in range(8):
        a = i * math.pi / 4
        k.line([(380, 240), (380 + math.cos(a) * 70, 240 + math.sin(a) * 70)], lw=0.4, amp=0, color=C(80, 60, 50))
    k.rect(40, 60, 160, 20, lw=0.8, fill=WOOD)
    k.text(120, 68, "THE ANCHOR INN", size=10, font="Ink-Plex", color=CARD)
    k.unclip()

def hedley_inn(k, w, h, v):
    part_open(k, w, h); P4.hedley(k, 160, 30, 230, prop=False); k.unclip()

# ----------------------------------------------------------------------------- 7. lineup: three equal panels
PW = 512
def lineup_plate(k, w, h):
    for i in range(3):
        k.c.saveState(); k.c.translate(i * PW, 0)
        k.frame2(PW, h); k.clip_rect(14, 14, PW - 14, h - 14)
        A4._tearoom(k, PW, h)
        nameplate(k, PW / 2, 40, CNAMES[i])
        k.unclip(); k.c.restoreState()

def lineup_fig(k, w, h, v, i=0, who="tamsin"):
    k.c.saveState(); k.c.translate(i * PW, 0); k.clip_rect(14, 14, PW - 14, h - 14)
    _fig(k, who, PW / 2 - 40, 70, 230)
    k.unclip(); k.c.restoreState()

# ----------------------------------------------------------------------------- 8. Ashdown statement (equal treatment — sketchbook, neutral)
def ashdown_plate(k, w, h):
    plate_open(k, w, h)
    A4._tearoom(k, w, h)
    k.unclip()

def ashdown_talk(k, w, h, v):
    part_open(k, w, h); P4.ashdown(k, 220, 30, 250); k.unclip()

def agnes_listen(k, w, h, v):
    part_open(k, w, h); P4.agnes(k, 400, 30, 220, basket=False, flip=True); k.unclip()

# ----------------------------------------------------------------------------- 9. Agnes thinking at the window (sunrise memory)
def agnes_plate(k, w, h):
    plate_open(k, w, h)
    k.wash_rect(14, 14, w - 14, h - 14, A4.TEAWALL)
    k.vgrad(14, 14, w - 14, 80, PAL.floor, PAL.floor2, steps=6)
    k.rect(280, 150, 190, 170, lw=1.2, fill=SKY_DAWN)
    k.vgrad(282, 152, 468, 230, SEA, SEA2, steps=6)
    k.vgrad(282, 230, 468, 318, SKY_DAWN, SKY_DAWN2, steps=6)
    k.circle(420, 270, 16, lw=0, fill=C(255, 220, 120), stroke=False)
    k.line([(375, 150), (375, 320)], lw=1.2, amp=0); k.line([(280, 235), (470, 235)], lw=1.2, amp=0)
    k.rect(240, 80, 230, 12, lw=1.0, fill=PAL.wood)
    with k.tint(PAL.teapot): k.teapot(300, 92, 40)
    with k.tint(PAL.walls[2]): k.cup(400, 92, 22)
    k.unclip()

def agnes_eye(k, w, h, v):
    part_open(k, w, h); P4.agnes(k, 130, 22, 240, expr="eyebrow", basket=False); k.unclip()

# ----------------------------------------------------------------------------- 10. map board (recap + solution): cove faces EAST
def board_plate(k, w, h):
    plate_open(k, w, h)
    k.wash_rect(14, 14, w - 14, h - 14, A4.TEAWALL)
    k.rect(34, 40, 444, 306, lw=1.4, fill=SLATE)
    k.rect(29, 35, 454, 316, lw=2.0, fill=None)
    k.text(256, 310, "TIDEWHISTLE COVE", size=18, font="Ink-Playfair", color=CHALK_Y)
    # simple map: sea on the RIGHT (east), hills on the LEFT (west)
    k.wash_rect(60, 100, 240, 250, C(160, 150, 130))  # hills / village
    k.wash_rect(240, 100, 450, 250, mix(SEA, SEA2, 0.5))  # sea
    k.text(150, 220, "HILLS", size=14, font="Ink-Kalam", color=CHALK)
    k.text(150, 200, "(west)", size=11, font="Ink-Kalam", color=CHALK)
    k.text(345, 220, "SEA", size=16, font="Ink-Kalam", color=CHALK)
    k.text(345, 200, "(east)", size=12, font="Ink-Kalam", color=CHALK_Y)
    # sun rise arrow from sea
    k.line([(400, 180), (400, 260)], lw=2.0, amp=0, color=CHALK_Y)
    k.shape([(390, 250), (400, 270), (410, 250)], lw=0.5, fill=CHALK_Y, amp=0)
    k.text(400, 160, "SUNRISE", size=11, font="Ink-Plex", color=CHALK_Y)
    # sun set arrow into hills
    k.line([(120, 260), (120, 180)], lw=1.6, amp=0, color=CHALK)
    k.shape([(110, 190), (120, 170), (130, 190)], lw=0.5, fill=CHALK, amp=0)
    k.text(120, 140, "SUNSET", size=11, font="Ink-Plex", color=CHALK)
    k.text(256, 70, "The cove faces EAST. The sea is the sunrise side.", size=12, font="Ink-Kalam", color=CHALK_G)
    k.unclip()

def mark_east(k, w, h, v):
    part_open(k, w, h)
    k.c.setStrokeColor(CHALK_R); k.c.setLineWidth(2.2)
    k.c.ellipse(300, 170, 420, 260, stroke=1, fill=0)
    k.text(360, 270, "EAST", size=14, font="Ink-Plex", color=CHALK_R)
    k.unclip()

def mark_x_sunset(k, w, h, v):
    """Cross out the impossible 'sunset into the sea'."""
    part_open(k, w, h)
    k.line([(280, 180), (440, 260)], lw=2.4, amp=0.3, color=CHALK_R)
    k.line([(280, 260), (440, 180)], lw=2.4, amp=0.3, color=CHALK_R)
    k.text(360, 120, "no sunset into the sea", size=12, font="Ink-Kalam", color=CHALK_R)
    k.unclip()

def mark_tick_ash(k, w, h, v):
    part_open(k, w, h)
    k.text(256, 55, "Mr Ashdown invented the clifftop.", size=13, font="Ink-Kalam", color=CHALK_G)
    k.unclip()

# ----------------------------------------------------------------------------- 11. confession at the inn room / with Demelza
def confess_plate(k, w, h):
    plate_open(k, w, h)
    k.wash_rect(14, 14, w - 14, h - 14, C(236, 220, 196))
    k.vgrad(14, 14, w - 14, 70, PAL.floor, PAL.floor2, steps=6)
    k.rect(40, 200, 140, 120, lw=1.0, fill=SKY_DAWN)  # window
    k.vgrad(42, 202, 178, 260, SEA, SEA2, steps=5)
    # wrapped painting on the table
    k.rect(280, 90, 120, 90, lw=1.0, fill=C(250, 246, 236))
    k.line([(280, 135), (400, 135)], lw=0.6, amp=0, color=C(180, 160, 140))
    k.line([(340, 90), (340, 180)], lw=0.6, amp=0, color=C(180, 160, 140))
    k.rect(300, 70, 80, 22, lw=0.8, fill=CARD)
    k.text(340, 80, "wrapped", size=9, font="Ink-Kalam", color=CARD_EDGE)
    k.unclip()

def ashdown_conf(k, w, h, v):
    part_open(k, w, h)
    P4.ashdown(k, 140, 26, 240, expr="sheepish" if "sheepish" in v else "neutral", prop=False)
    k.unclip()

def demelza_conf(k, w, h, v):
    part_open(k, w, h); P4.demelza(k, 360, 30, 220, prop=False); k.unclip()

# ----------------------------------------------------------------------------- vignette
def vignette(k, w, h):
    k.circle(w / 2, h / 2, w * 0.46, lw=1.5, fill=C(255, 200, 150)); k.circle(w / 2, h / 2, w * 0.44, lw=0.5, fill=None)
    for i in range(24):
        a = 2 * math.pi * i / 24
        k.circle(w / 2 + w * 0.46 * math.cos(a), h / 2 + w * 0.46 * math.sin(a), 3.5, lw=0, fill=C(247, 240, 225), stroke=False)
    k.c.saveState(); p = k.c.beginPath(); p.circle(w / 2, h / 2, w * 0.44 - 1); k.c.clipPath(p, stroke=0, fill=0)
    k.vgrad(0, h * 0.35, w, h, SKY_DAWN, SKY_DAWN2, steps=8)
    k.vgrad(0, 0, w, h * 0.4, SEA, SEA2, steps=6)
    k.circle(w * 0.7, h * 0.55, 22, lw=0, fill=C(255, 220, 120), stroke=False)
    k.compass_rose(w * 0.35, h * 0.55, 40)
    k.c.restoreState()

# ============================================================================= jobs
AW, AH = 512, 384
V3 = ["base", "base+blink", "base+talk"]; V2 = ["base", "base+blink"]
FX = dict(gull=dict(fn=gull_fx, variants=["f0", "f1", "f2", "f3"], page=(44, 22)))
STEAM = dict(steam=dict(fn=steam_fx, variants=["s0", "s1", "s2"], page=(12, 22)))

def jobs():
    J = []
    J.append(dict(name="hook", w=AW, h=AH, plate=hook_plate, seed=91, parts=dict(**FX)))
    J.append(dict(name="cast", w=CW, h=CH, plate=cast_plate, seed=92, parts={
        who: dict(fn=partial(cast_fig, i=i, who=who), variants=V2) for i, who in enumerate(CAST)}))
    J.append(dict(name="kettle", w=AW, h=AH, plate=kettle_plate, seed=93, parts=dict(
        agnes=dict(fn=agnes_kettle, variants=V2), **FX, **STEAM)))
    J.append(dict(name="stall", w=AW, h=AH, plate=stall_plate, seed=94, parts=dict(
        painting=dict(fn=painting_part, variants=["base"]),
        demelza=dict(fn=demelza_stall, variants=V2), **FX)))
    J.append(dict(name="bookshop", w=AW, h=AH, plate=bookshop_plate, seed=95, parts=dict(
        tamsin=dict(fn=tamsin_shop, variants=V3))))
    J.append(dict(name="inn", w=AW, h=AH, plate=inn_plate, seed=96, parts=dict(
        hedley=dict(fn=hedley_inn, variants=V3))))
    J.append(dict(name="lineup", w=3 * PW, h=AH, plate=lineup_plate, seed=97, parts={
        who: dict(fn=partial(lineup_fig, i=i, who=who), variants=V3) for i, who in enumerate(CAST)}))
    J.append(dict(name="ashdown", w=AW, h=AH, plate=ashdown_plate, seed=98, parts=dict(
        ashdown=dict(fn=ashdown_talk, variants=V3),
        agnes=dict(fn=agnes_listen, variants=V2))))
    J.append(dict(name="agnes", w=AW, h=AH, plate=agnes_plate, seed=99, parts=dict(
        agnes=dict(fn=agnes_eye, variants=V2), **STEAM)))
    J.append(dict(name="board", w=AW, h=AH, plate=board_plate, seed=100, parts=dict(
        east=dict(fn=mark_east, variants=["base"]),
        x_sunset=dict(fn=mark_x_sunset, variants=["base"]),
        tick_ash=dict(fn=mark_tick_ash, variants=["base"]))))
    J.append(dict(name="confess", w=AW, h=AH, plate=confess_plate, seed=101, parts=dict(
        ashdown=dict(fn=ashdown_conf, variants=["sheepish", "sheepish+blink"]),
        demelza=dict(fn=demelza_conf, variants=V3))))
    J.append(dict(name="vignette", w=384, h=384, plate=vignette, seed=102))
    return J

def make_ink(c, seed): return Ink9(c, seed=seed)

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    J = [j for j in jobs() if not want or j["name"] in want]
    save_layers(OUT, J, make_ink)
