"""Illustrations for Case 5, The Marrow Mix-up: colour-detailed + animation layers (same pipeline as art_case04).
PART sprites use part_open (clip only) — never frame2 — so borders are not baked into rotating/bobbing sprites.
Run: python3 art_case05.py [scene ...]"""
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
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-05")

# ----------------------------------------------------------------------------- palette (allotment / shed)
GRASS = C(176, 206, 140); GRASS2 = C(150, 188, 116); EARTH = C(166, 130, 92); EARTH2 = C(140, 108, 74)
STRAW = C(236, 210, 140); STRAW2 = C(210, 180, 110); WOOD = PAL.wood; WOOD2 = PAL.wood_dk
MARROW = C(120, 168, 78); MARROW2 = C(86, 132, 56); MARROW_LT = C(168, 204, 110)
SHED = C(196, 168, 120); SHED2 = C(170, 140, 96); SKY = PAL.sky; SKY2 = PAL.sky2
BENCH = C(150, 112, 78); FLASK = C(70, 110, 150)

class Ink5(A4.Ink4):
    def allotment_sky(s, w, h, y_horizon=200):
        s.vgrad(14, y_horizon, w - 14, h - 14, SKY, SKY2, steps=16)

    def allotment_ground(s, w, h, y_top=200):
        s.vgrad(14, 14, w - 14, y_top, GRASS, GRASS2, steps=10)
        rr = random.Random(11)
        for i in range(50):
            gx = rr.uniform(20, w - 20); gy = rr.uniform(20, y_top - 8)
            for d in (-1, 0, 1): s.line([(gx, gy), (gx + d * 1.2, gy + 3.2)], lw=0.35, amp=0, color=shade(GRASS, 0.72))
        # vegetable beds
        for (x0, x1, y0, y1) in ((30, 150, 40, 110), (170, 300, 50, 120), (320, 470, 36, 100)):
            s.wash_rect(x0, y0, x1, y1, EARTH)
            s.rect(x0, y0, x1 - x0, y1 - y0, lw=0.7, fill=None)
            for j in range(4):
                yy = y0 + 10 + j * ((y1 - y0 - 16) / 4)
                s.line([(x0 + 6, yy), (x1 - 6, yy)], lw=0.4, amp=0.3, color=EARTH2)
                for i in range(int((x1 - x0) / 18)):
                    cx = x0 + 12 + i * 18
                    with s.tint(rr.choice([PAL.leaf, MARROW_LT, C(220, 120, 90)])):
                        s.circle(cx, yy + 3, 3.2, lw=0.4, fill=Wt)

    def shed5(s, x, y, w, h, door_open=False):
        s.wall(x, y, w, h * 0.7, gap=2.6, color=SHED)
        s.roof(x, x + w, y + h * 0.7, y + h, overhang=8, color=PAL.slate)
        with s.tint(SHED, hatch=SHED2):
            s.hatch([(x, y), (x + w, y), (x + w, y + h * 0.7), (x, y + h * 0.7)], angle=90, gap=4.5, lw=0.3)
        # door
        dx, dw, dh = x + w * 0.32, w * 0.36, h * 0.52
        if door_open:
            s.wash_rect(dx, y, dx + dw, y + dh, C(70, 56, 40))
            s.shape([(dx + dw, y), (dx + dw + w * 0.22, y + 6), (dx + dw + w * 0.22, y + dh - 4), (dx + dw, y + dh)], lw=0.9, fill=WOOD2, amp=0)
        else:
            s.rect(dx, y, dw, dh, lw=0.9, fill=WOOD)
            s.line([(dx + dw / 2, y), (dx + dw / 2, y + dh)], lw=0.5, amp=0)
            s.circle(dx + dw * 0.78, y + dh * 0.45, 1.8, lw=0.4, fill=PAL.brass)
        s.window(x + w * 0.08, y + h * 0.28, w * 0.16, h * 0.18)
        s.window(x + w * 0.74, y + h * 0.28, w * 0.16, h * 0.18)

    def marrow5(s, x, y, L=120, fat=38):
        """Prize marrow: long green striped, lying on its side; (x,y) = left tip."""
        body = []
        for i in range(25):
            t = i / 24; px = x + L * t
            r = fat * (0.35 + 0.65 * math.sin(t * math.pi) ** 0.7)
            body.append((px, y + r * 0.15 * math.sin(t * 4)))
        bot = []
        for i in range(25):
            t = 1 - i / 24; px = x + L * t
            r = fat * (0.35 + 0.65 * math.sin(t * math.pi) ** 0.7)
            bot.append((px, y - r * 0.85))
        pts = body + bot
        with s.tint(MARROW, hatch=MARROW2): s.shape(pts, lw=1.1, fill=Wt, amp=0.2)
        for i in range(7):
            t0, t1 = 0.08 + i * 0.12, 0.18 + i * 0.12
            s.line([(x + L * t0, y + fat * 0.05), (x + L * t1, y - fat * 0.55)], lw=0.7, amp=0.2, color=MARROW2)
        # stem / blossom end
        s.shape([(x + L - 2, y), (x + L + 8, y + 4), (x + L + 6, y - 6)], lw=0.6, fill=C(90, 120, 50), amp=0)
        s.circle(x + 3, y - 2, 4, lw=0.5, fill=C(220, 160, 60))

    def straw_bed(s, x, y, w, h):
        s.wash_rect(x, y, x + w, y + h, STRAW)
        rr = random.Random(3)
        for i in range(40):
            x0 = x + rr.uniform(2, w - 4); y0 = y + rr.uniform(2, h - 4)
            a = rr.uniform(-0.6, 0.6); L = rr.uniform(8, 18)
            s.line([(x0, y0), (x0 + L * math.cos(a), y0 + L * 0.3 * math.sin(a))], lw=0.55, amp=0, color=rr.choice([STRAW2, shade(STRAW, 0.85), C(190, 160, 90)]))

    def bench5(s, x, y, w, seat=22):
        for u in (-0.46, 0.46):
            s.line([(x + u * w, y), (x + u * w, y + seat + 48)], lw=2.4, amp=0, color=WOOD2)
        s.rect(x - w / 2 - 2, y + seat - 4, w + 4, 8, lw=0.8, fill=WOOD)
        for j in range(3): s.rect(x - w / 2, y + seat + 14 + 12 * j, w, 8, lw=0.7, fill=WOOD)

    def flask5(s, x, y, h=36):
        s.rect(x - 8, y, 16, h * 0.55, lw=0.8, fill=FLASK)
        s.rect(x - 10, y + h * 0.55, 20, h * 0.12, lw=0.7, fill=WOOD)
        s.circle(x, y + h * 0.78, 7, lw=0.7, fill=C(240, 236, 220))
        s.rect(x - 4, y + h * 0.85, 8, h * 0.12, lw=0.6, fill=C(50, 80, 110))

# ============================================================================= open helpers (border on plates ONLY)
def plate_open(k, w, h):
    k.frame2(w, h); k.clip_rect(14, 14, w - 14, h - 14)

def part_open(k, w, h):
    """Clip only — no frame2 (avoids Case 4 rotating-border artifact)."""
    k.clip_rect(14, 14, w - 14, h - 14)

# ----------------------------------------------------------------------------- FX (small pages; no full-frame border)
def gull_fx(k, w, h, v):
    up = {"f0": 1.0, "f1": 0.45, "f2": -0.1, "f3": -0.5}[v]; x, y = w / 2, h / 2
    for sg in (-1, 1):
        tip = (x + sg * w * 0.46, y + up * h * 0.4); mid = (x + sg * w * 0.22, y + up * h * 0.25 + h * 0.18)
        k.line([(x + sg * 1.5, y), mid, tip], lw=1.0, amp=0, color=C(60, 64, 72))
    k.shape(k.arcpts(x, y - 0.6, 3.2, 1.6, 0, 360, 12), lw=0.5, fill=PAL.cloud, amp=0)

def leaf_fx(k, w, h, v):
    ph = {"f0": 0, "f1": 0.4, "f2": 0.8}[v]
    k.shape([(2, h / 2), (w * 0.55, h * (0.2 + 0.15 * math.sin(ph * 5))), (w - 2, h / 2), (w * 0.55, h * (0.8 - 0.1 * math.sin(ph * 5)))], lw=0.5, fill=PAL.leaf, amp=0)

def steam_fx(k, w, h, v):
    ph = {"s0": 0, "s1": 1.6, "s2": 3.1}[v]
    pts = [(w / 2 + 2.6 * math.sin(t * 5 + ph), 2 + t * (h - 4)) for t in [i / 16 for i in range(17)]]
    k.line(pts, lw=1.1, amp=0, color=C(255, 255, 255)); k.line([(x + 1.6, y) for x, y in pts[3:]], lw=0.6, amp=0, color=C(240, 240, 240))

# ----------------------------------------------------------------------------- 1. shed interior: marrow on straw / empty / hook
def shed_interior_plate(k, w, h, empty=False, hook=False):
    plate_open(k, w, h)
    # wooden shed walls
    k.wash_rect(14, 14, w - 14, h - 14, C(214, 190, 150))
    for i in range(14):
        x = 14 + i * ((w - 28) / 13)
        k.line([(x, 14), (x, h - 14)], lw=0.45, amp=0.15, color=shade(SHED2, 0.9))
    # floor boards
    k.wash_rect(14, 14, w - 14, 90, C(170, 140, 100))
    for i in range(8): k.line([(14, 20 + i * 9), (w - 14, 22 + i * 9)], lw=0.4, amp=0.2, color=WOOD2)
    # window light
    k.wash_rect(w * 0.55, 200, w - 30, h - 30, C(240, 230, 190))
    k.rect(w * 0.55, 200, w * 0.38, h - 230, lw=1.0, fill=None)
    k.line([(w * 0.55 + w * 0.19, 200), (w * 0.55 + w * 0.19, h - 30)], lw=0.8, amp=0)
    k.line([(w * 0.55, 200 + (h - 230) / 2), (w - 30, 200 + (h - 230) / 2)], lw=0.8, amp=0)
    # straw bed
    k.straw_bed(50, 40, 280, 90)
    if not empty and not hook:
        pass  # marrow is a part
    if empty or hook:
        # dashed outline where the marrow was
        k.c.setDash(3, 3); k.c.setStrokeColor(C(120, 100, 70)); k.c.setLineWidth(1.2)
        k.c.ellipse(70, 55, 300, 110, stroke=1, fill=0); k.c.setDash([])
    k.unclip()

def marrow_part(k, w, h, v, x=80, y=78, L=200, fat=48):
    part_open(k, w, h); k.marrow5(x, y, L=L, fat=fat); k.unclip()

def sparkle_part(k, w, h, v):
    part_open(k, w, h); x, y, r = 180, 100, 14
    k.shape([(x - r, y), (x - r * 0.16, y + r * 0.16), (x, y + r), (x + r * 0.16, y + r * 0.16),
             (x + r, y), (x + r * 0.16, y - r * 0.16), (x, y - r), (x - r * 0.16, y - r * 0.16)],
            lw=0, stroke=False, fill=C(255, 250, 220), amp=0)
    k.unclip()

# ----------------------------------------------------------------------------- 2. allotments exterior
def allotments_plate(k, w, h):
    plate_open(k, w, h)
    k.allotment_sky(w, h, 210)
    k.allotment_ground(w, h, 210)
    k.shed5(300, 100, 180, 200, door_open=True)
    # path
    k.wash([(40, 14), (120, 14), (200, 90), (80, 90)], C(214, 196, 150))
    k.flower_urn(90, 100, 28); k.flower_urn(250, 95, 24)
    k.unclip()

def cloud_part(k, w, h, v, x=0, y=0, s_=1.0):
    part_open(k, w, h)
    for (dx, dy, r) in ((0, 0, 16), (16, 4, 13), (-15, 2, 11), (6, 10, 11), (28, -1, 9)):
        k.circle(x + dx * s_, y + dy * s_, r * s_, lw=0, fill=PAL.cloud, stroke=False)
    k.unclip()

def hedley_walk(k, w, h, v):
    part_open(k, w, h); P4.hedley(k, 120, 30, 200); k.unclip()

# ----------------------------------------------------------------------------- 3. bench: Agnes + flask, suspects walk in
def bench_plate(k, w, h):
    plate_open(k, w, h)
    k.allotment_sky(w, h, 160)
    k.vgrad(14, 14, w - 14, 160, GRASS, GRASS2, steps=8)
    k.shed5(340, 70, 150, 170, door_open=False)
    k.bench5(256, 40, 300, seat=28)
    k.unclip()

def agnes_bench(k, w, h, v):
    part_open(k, w, h); P4.agnes(k, 90, 36, 210, basket=False); k.unclip()

def flask_part(k, w, h, v):
    part_open(k, w, h); k.flask5(200, 78, 40); k.unclip()

def cup_steam(k, w, h, v):
    part_open(k, w, h)
    k.circle(188, 100, 7, lw=0.6, fill=C(250, 246, 230))
    k.circle(188, 100, 5, lw=0.4, fill=C(220, 200, 160))
    k.unclip()

# ----------------------------------------------------------------------------- 4. lineup: 4 suspects
PW = 512
def _panel_bed(k, pw, h, soil=True):
    k.allotment_sky(pw, h, 170)
    k.vgrad(14, 14, pw - 14, 170, GRASS, GRASS2, steps=8)
    if soil:
        k.wash_rect(40, 40, pw - 40, 100, EARTH)
        rr = random.Random(int(pw))
        for i in range(12):
            k.circle(60 + i * 30, 70 + (i % 3) * 8, 4, lw=0.4, fill=rr.choice([PAL.leaf, MARROW_LT, C(200, 100, 80)]))

def lineup_plate(k, w, h):
    names = ["JAGO PENHALLOW", "TAMSIN TREVELYAN", "HEDLEY TRUSCOTT", "MORWENNA DAY"]
    for i in range(4):
        k.c.saveState(); k.c.translate(i * PW, 0); pw = PW
        k.frame2(pw, h); k.clip_rect(14, 14, pw - 14, h - 14)
        _panel_bed(k, pw, h)
        nameplate(k, pw / 2, 40, names[i])
        k.unclip(); k.c.restoreState()

def lineup_fig(k, w, h, v, i=0, who="jago"):
    k.c.saveState(); k.c.translate(i * PW, 0); k.clip_rect(14, 14, PW - 14, h - 14)
    getattr(P4, who)(k, PW / 2 - 46, 70, 236)
    k.unclip(); k.c.restoreState()

def lineup_agnes(k, w, h, v):
    """Agnes listening from the side of panel 0 during statements."""
    k.c.saveState(); k.clip_rect(14, 14, PW - 14, h - 14)
    P4.agnes(k, PW / 2 + 140, 80, 190, basket=False)
    k.unclip(); k.c.restoreState()

# ----------------------------------------------------------------------------- 5. thinking
def thinking_plate(k, w, h):
    plate_open(k, w, h)
    k.allotment_sky(w, h, 180)
    k.vgrad(14, 14, w - 14, 180, GRASS, GRASS2, steps=8)
    k.shed5(320, 80, 160, 180, door_open=True)
    k.bench5(200, 50, 220, seat=26)
    k.unclip()

def agnes_think(k, w, h, v):
    part_open(k, w, h); P4.agnes(k, 140, 34, 230, basket=False); k.unclip()

# ----------------------------------------------------------------------------- 6. returned / confession
def returned_plate(k, w, h):
    plate_open(k, w, h)
    k.allotment_sky(w, h, 150)
    k.vgrad(14, 14, w - 14, 150, GRASS, GRASS2, steps=8)
    # flower display table
    k.rect(60, 50, 280, 18, lw=1.0, fill=WOOD)
    for u in (0.15, 0.85): k.line([(60 + 280 * u, 14), (60 + 280 * u, 50)], lw=2.0, amp=0, color=WOOD2)
    k.shed5(360, 60, 130, 160, door_open=True)
    k.unclip()

def marrow_display(k, w, h, v):
    part_open(k, w, h); k.marrow5(90, 78, L=160, fat=40); k.unclip()

def flowers_part(k, w, h, v):
    part_open(k, w, h)
    for (x, y, col) in ((100, 90, C(226, 108, 120)), (130, 100, C(244, 200, 80)), (160, 88, C(180, 120, 200)),
                        (200, 96, C(226, 108, 120)), (230, 92, C(120, 180, 200))):
        k.line([(x, 68), (x, y)], lw=0.7, amp=0, color=PAL.leaf)
        k.circle(x, y, 7, lw=0.5, fill=col)
    k.unclip()

def morwenna_ret(k, w, h, v):
    part_open(k, w, h)
    expr = "sheepish" if v.startswith("sheepish") or v.startswith("base") else "smile"
    P4.morwenna(k, 340, 40, 230, expr=expr, prop=not v.startswith("empty"))
    k.unclip()

def hedley_ret(k, w, h, v):
    part_open(k, w, h); P4.hedley(k, 200, 40, 220, expr="smile"); k.unclip()

# ----------------------------------------------------------------------------- cast strip + vignette
def cast_plate(k, w, h):
    k.wash_rect(0, 0, w, h, SKY2)
    k.vgrad(0, 40, w, 100, GRASS, GRASS2, steps=6)
    k.wash_rect(0, 0, w, 40, EARTH)
    k.c.setStrokeColor(K); k.c.setLineWidth(1.3); k.c.rect(1, 1, w - 2, h - 2, stroke=1, fill=0)

def cast_fig(k, w, h, v, i=0, who="jago"):
    getattr(P4, who)(k, w * (0.12 + 0.24 * i), 18, h * 0.78)

def vignette(k, w, h):
    k.circle(w / 2, h / 2, w * 0.46, lw=1.3, fill=PAL.cloud); k.circle(w / 2, h / 2, w * 0.44, lw=0.45, fill=None)
    k.c.saveState(); p = k.c.beginPath(); p.circle(w / 2, h / 2, w * 0.44 - 1); k.c.clipPath(p, stroke=0, fill=0)
    k.vgrad(0, h * 0.4, w, h, SKY, SKY2, steps=10)
    k.vgrad(0, 0, w, h * 0.42, GRASS, GRASS2, steps=6)
    k.straw_bed(w * 0.18, h * 0.12, w * 0.64, h * 0.22)
    k.marrow5(w * 0.22, h * 0.22, L=w * 0.5, fat=w * 0.1)
    k.c.restoreState()

# ============================================================================= jobs
AW, AH = 512, 384
V3 = ["base", "base+blink", "base+talk"]; V2 = ["base", "base+blink"]
FX = dict(gull=dict(fn=gull_fx, variants=["f0", "f1", "f2", "f3"], page=(44, 22)),
          leaf=dict(fn=leaf_fx, variants=["f0", "f1", "f2"], page=(18, 12)))
STEAM = dict(steam=dict(fn=steam_fx, variants=["s0", "s1", "s2"], page=(12, 22)))

def jobs():
    J = []
    J.append(dict(name="shed", w=AW, h=AH, plate=shed_interior_plate, seed=51, parts=dict(
        marrow=dict(fn=partial(marrow_part, x=70, y=78, L=220, fat=52), variants=["base"]),
        sparkle=dict(fn=sparkle_part, variants=["base"]), **FX)))
    J.append(dict(name="empty", w=AW, h=AH, plate=partial(shed_interior_plate, empty=True), seed=52, parts=dict(**FX)))
    J.append(dict(name="hook", w=AW, h=AH, plate=partial(shed_interior_plate, hook=True), seed=52, parts=dict(**FX)))
    J.append(dict(name="allotments", w=AW, h=AH, plate=allotments_plate, seed=53, parts=dict(
        hedley=dict(fn=hedley_walk, variants=V2),
        cloud1=dict(fn=partial(cloud_part, x=100, y=330, s_=1.0), variants=["base"]),
        cloud2=dict(fn=partial(cloud_part, x=340, y=350, s_=0.7), variants=["base"]), **FX)))
    J.append(dict(name="bench", w=AW, h=AH, plate=bench_plate, seed=54, parts=dict(
        agnes=dict(fn=agnes_bench, variants=V3), flask=dict(fn=flask_part, variants=["base"]),
        cup=dict(fn=cup_steam, variants=["base"]),
        cloud1=dict(fn=partial(cloud_part, x=120, y=320, s_=0.9), variants=["base"]), **FX, **STEAM)))
    J.append(dict(name="lineup", w=4 * PW, h=AH, plate=lineup_plate, seed=55, parts=dict(
        jago=dict(fn=partial(lineup_fig, i=0, who="jago"), variants=V3),
        tamsin=dict(fn=partial(lineup_fig, i=1, who="tamsin"), variants=V3),
        hedley=dict(fn=partial(lineup_fig, i=2, who="hedley"), variants=V3),
        morwenna=dict(fn=partial(lineup_fig, i=3, who="morwenna"), variants=V3),
        agnes=dict(fn=lineup_agnes, variants=V2), **FX, **STEAM)))
    J.append(dict(name="thinking", w=AW, h=AH, plate=thinking_plate, seed=56, parts=dict(
        agnes=dict(fn=agnes_think, variants=V2),
        cloud1=dict(fn=partial(cloud_part, x=80, y=320, s_=0.8), variants=["base"]), **FX)))
    J.append(dict(name="returned", w=AW, h=AH, plate=returned_plate, seed=57, parts=dict(
        marrow=dict(fn=marrow_display, variants=["base"]),
        flowers=dict(fn=flowers_part, variants=["base"]),
        morwenna=dict(fn=morwenna_ret, variants=["base", "base+blink", "sheepish", "sheepish+blink", "empty", "empty+blink"]),
        hedley=dict(fn=hedley_ret, variants=V2),
        sparkle=dict(fn=sparkle_part, variants=["base"]), **FX)))
    whos = ["jago", "tamsin", "hedley", "morwenna"]
    J.append(dict(name="cast", w=720, h=260, plate=cast_plate, seed=58, parts={
        who: dict(fn=partial(cast_fig, i=i, who=who), variants=V2) for i, who in enumerate(whos)}))
    J.append(dict(name="vignette", w=384, h=384, plate=vignette, seed=59))
    return J

def make_ink(c, seed): return Ink5(c, seed=seed)

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    J = [j for j in jobs() if not want or j["name"] in want]
    save_layers(OUT, J, make_ink)
