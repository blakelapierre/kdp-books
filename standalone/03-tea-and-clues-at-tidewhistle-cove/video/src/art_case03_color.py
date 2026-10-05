"""Illustrations for Case 3, The Dry Raincoat, in the COLOUR-DETAILED style (colorink.set_style("color-detailed")):
house ink lines over soft watercolour-style washes, with the DETAILED v2-style characters from people3.py
(proper faces, hair, clothing details) instead of the simple peg dolls. The black-and-white case 3 art
(art_case03.py -> work/art-03/) is untouched; this writes ../work/art-03-color/*.png.
Run: python3 art_case03_color.py [scene ...]
The three suspects are drawn at the same height, stance, arm pose and colour weight in every pre-solution
picture; only Wenna's after-solution reaction (returned scene) differs. Everything is drawn in code."""
import math, os, sys, random
import colorink
colorink.set_style("color-detailed")
import art_case03 as B          # reuse the case 3 scene helpers (Shop drawing methods)
colorink.set_style("color-detailed")
from inkart import lerp, K, Wt
from colorink import PAL, C, render_color, shade, mix
import people3 as P
from art import nameplate

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-03-color")

# ----------------------------------------------------------------------------- palette
SHOPWALL = C(250, 236, 196); SIGN = C(44, 86, 74); GOLD = C(240, 212, 132); DOOR = C(62, 112, 122)
WALL_IN = C(246, 232, 206); WAINSCOT = C(196, 150, 110); FLOOR = C(222, 186, 138); FLOOR2 = C(204, 166, 118)
WOOD = C(176, 124, 84); WOOD_DK = C(132, 90, 60); GLASS = C(214, 234, 240); VELVET = C(160, 60, 74)
STRIPE = C(214, 92, 84); STRIPE_LT = C(252, 244, 228); COBBLE = C(200, 192, 178); COBBLE_WET = C(150, 160, 170)
RAIN = C(128, 154, 182); STORM = C(92, 104, 122); STORM2 = C(140, 150, 162); WATER = C(150, 180, 204)
PHONE = C(196, 70, 64); CHEMIST = C(206, 232, 214)
SPINES = [C(170, 70, 64), C(64, 104, 140), C(92, 140, 96), C(214, 172, 86), C(120, 84, 130), C(236, 226, 206),
          C(196, 120, 80), C(80, 128, 136), C(150, 52, 60), C(232, 196, 120), C(60, 76, 110), C(176, 196, 150)]

class ShopC(B.Shop):
    """Colour versions of the bookshop drawing methods (same geometry as art_case03.Shop)."""
    def spines(s, x0, x1, y, h, seed=0, gaps=False):
        x = x0; i = seed
        while x < x1 - 4:
            w = 5 + (i * 7) % 6; hh = h * (0.72 + 0.28 * ((i * 5) % 7) / 6)
            if x + w > x1: break
            col = SPINES[(i * 5 + seed) % len(SPINES)]
            pts = [(x, y), (x + w, y), (x + w, y + hh), (x, y + hh)]
            s.shape(pts, lw=0.55, fill=col, amp=0)
            s.wash([(x + w * 0.62, y), (x + w, y), (x + w, y + hh), (x + w * 0.62, y + hh)], shade(col, 0.82))
            kind = (i * 3) % 5
            if kind == 1: s.line([(x + 1, y + hh * 0.78), (x + w - 1, y + hh * 0.78)], lw=0.6, amp=0, color=GOLD)
            if kind in (1, 3): s.line([(x + 1, y + hh * 0.22), (x + w - 1, y + hh * 0.22)], lw=0.5, amp=0, color=GOLD if kind == 1 else shade(col, 0.6))
            if kind == 4: s.rect(x + 1.2, y + hh * 0.5, w - 2.4, hh * 0.16, lw=0.3, fill=PAL.paper)
            s.shape(pts, lw=0.55, fill=None, amp=0)
            x += w + (3 if gaps and i % 9 == 4 else 0.4); i += 1

    def bookcase(s, x, y, w, h, shelves=4, seed=0, label=None):
        s.rect(x, y, w, h, lw=1.0, fill=WOOD)
        s.rect(x + 6, y + 4, w - 10, h - 8, lw=0.5, fill=shade(WOOD, 0.62))   # dark back board
        sh = (h - 10) / shelves
        for j in range(shelves):
            yy = y + 6 + j * sh
            s.rect(x + 2, yy - 2.4, w - 4, 3.4, lw=0.7, fill=WOOD)
            s.spines(x + 9, x + w - 4, yy + 1, sh * 0.78, seed=seed + j * 11)
        with s.tint(WOOD): s.hatch([(x, y), (x + 6, y), (x + 6, y + h), (x, y + h)], angle=90, gap=1.6, lw=0.35)
        s.rect(x - 3, y + h, w + 6, 5, lw=0.9, fill=WOOD_DK)
        s.rect(x - 1, y - 2, w + 2, 4, lw=0.7, fill=WOOD_DK)
        if label:
            tw = s.c.stringWidth(label, "Ink-Plex", 9)
            s.rect(x + w / 2 - tw / 2 - 6, y + h + 8, tw + 12, 14, lw=0.7, fill=PAL.card)
            s.text(x + w / 2, y + h + 11.5, label, size=9, font="Ink-Plex")

    def puffin_book(s, x, y, w):
        h = w * 1.3
        s.rect(x - w / 2 - 2, y - 1, w + 4, 3, lw=0.6, fill=WOOD_DK)                 # little stand
        s.rect(x - w / 2, y, w, h, lw=0.9, fill=C(84, 132, 156))
        s.rect(x - w / 2 + w * 0.08, y + h * 0.06, w * 0.84, h * 0.88, lw=0.4, fill=C(222, 236, 238))
        s.wash([(x - w * 0.42, y + h * 0.06), (x + w * 0.42, y + h * 0.06), (x + w * 0.42, y + h * 0.3), (x - w * 0.42, y + h * 0.3)], C(150, 196, 214))   # sea
        px, py, r = x, y + h * 0.42, w * 0.16
        s.shape(s.arcpts(px, py, r, r * 1.35, 0, 360, 20), lw=0.6, fill=C(40, 44, 52), amp=0)
        s.shape(s.arcpts(px + r * 0.15, py - r * 0.25, r * 0.6, r * 0.85, 0, 360, 16), lw=0.4, fill=Wt, amp=0)
        s.circle(px + r * 0.1, py + r * 1.6, r * 0.62, lw=0.6, fill=C(40, 44, 52))
        s.circle(px + r * 0.25, py + r * 1.7, r * 0.34, lw=0.3, fill=Wt)
        s.circle(px + r * 0.3, py + r * 1.72, r * 0.1, lw=0, fill=K, stroke=False)
        s.shape([(px + r * 0.6, py + r * 1.8), (px + r * 1.2, py + r * 1.55), (px + r * 0.62, py + r * 1.35)], lw=0.5, fill=C(240, 140, 70), amp=0)
        for sg in (-1, 1): s.shape([(px + sg * r * 0.3, py - r * 1.35), (px + sg * r * 0.7, py - r * 1.45), (px + sg * r * 0.4, py - r * 1.2)], lw=0.4, fill=C(240, 140, 70), amp=0)
        for j in range(2): s.line([(x - w * 0.28, y + h * (0.84 - 0.07 * j)), (x + w * 0.28, y + h * (0.84 - 0.07 * j))], lw=0.6 - 0.2 * j, amp=0, color=C(60, 80, 110))
        s.line([(x - w * 0.22, y + h * 0.12), (x - w * 0.02, y + h * 0.16), (x + w * 0.1, y + h * 0.11), (x + w * 0.26, y + h * 0.15)], lw=0.6, amp=0.4, color=C(40, 50, 120))   # signature

    def glass_case(s, x, y, w, h, book=True, open_=False, lock=False):
        legh = h * 0.42; by = y + legh
        for u in (-0.42, 0.42):
            s.rect(x + u * w - 2.5, y, 5, legh, lw=0.8, fill=WOOD)
            s.wash([(x + u * w + 0.8, y), (x + u * w + 2.5, y), (x + u * w + 2.5, y + legh), (x + u * w + 0.8, y + legh)], shade(WOOD, 0.8))
        s.rect(x - w * 0.42, y + legh * 0.3, w * 0.84, 3, lw=0.6, fill=WOOD_DK)   # stretcher rail
        s.rect(x - w / 2 - 4, by, w + 8, h * 0.08, lw=1.0, fill=WOOD)
        with s.tint(WOOD): s.hatch([(x - w / 2 - 4, by), (x + w / 2 + 4, by), (x + w / 2 + 4, by + h * 0.08), (x - w / 2 - 4, by + h * 0.08)], angle=0, gap=1.4, lw=0.35)
        gy = by + h * 0.08; gh = h * 0.5
        s.rect(x - w / 2, gy, w, gh, lw=1.0, fill=GLASS)
        s.wash([(x - w / 2 + 2, gy + 2), (x + w / 2 - 2, gy + 2), (x + w / 2 - 2, gy + gh * 0.28), (x - w / 2 + 2, gy + gh * 0.4)], mix(GLASS, VELVET, 0.18))
        s.rect(x - w * 0.18, gy, w * 0.36, h * 0.03, lw=0.6, fill=VELVET)
        if book: s.puffin_book(x, gy + h * 0.03, gh * 0.55)
        else:
            s.c.setStrokeColor(shade(GLASS, 0.5)); s.c.setLineWidth(0.5); s.c.setDash(2, 2)
            s.c.rect(x - gh * 0.275, gy + h * 0.03, gh * 0.55, gh * 0.55 * 1.3, stroke=1, fill=0); s.c.setDash()
            s.wash([(x - gh * 0.3, gy + h * 0.03), (x + gh * 0.3, gy + h * 0.03), (x + gh * 0.24, gy + h * 0.045), (x - gh * 0.24, gy + h * 0.045)], shade(VELVET, 0.8))
        for g in (0.12, 0.2, 0.7):
            s.line([(x - w / 2 + w * g, gy + gh * 0.88), (x - w / 2 + w * g + gh * 0.25, gy + gh * 0.58)], lw=0.8, amp=0, color=Wt)
        s.rect(x - w / 2 - 2, gy + gh, w + 4, h * 0.05, lw=1.0, fill=WOOD)
        s.rect(x - w / 2 + 6, gy + gh + h * 0.05, w - 12, 3, lw=0.6, fill=WOOD_DK)
        if open_:
            s.shape([(x + w / 2, gy), (x + w / 2 + w * 0.32, gy - h * 0.04), (x + w / 2 + w * 0.32, gy + gh - h * 0.02), (x + w / 2, gy + gh)], lw=1.0, fill=mix(GLASS, Wt, 0.3), amp=0)
            s.line([(x + w / 2 + w * 0.08, gy + gh * 0.7), (x + w / 2 + w * 0.2, gy + gh * 0.4)], lw=0.8, amp=0, color=Wt)
            s.circle(x + w / 2 + w * 0.28, gy + gh * 0.5, 1.8, lw=0.5, fill=PAL.brass)
            s.line([(x + w / 2 + 2, gy + gh * 0.5), (x + w / 2 + 7, gy + gh * 0.44)], lw=0.8, amp=0)   # key in the lock
        else:
            s.circle(x + w / 2 - 5, gy + gh * 0.5, 1.8, lw=0.5, fill=PAL.brass)
        if lock:
            lx, ly = x + w / 2 - 5, gy + gh * 0.5 - 12
            s.c.setStrokeColor(shade(PAL.silver, 0.6)); s.c.setLineWidth(1.6); s.c.arc(lx - 4, ly + 4, lx + 4, ly + 14, 0, 180)
            s.rect(lx - 6, ly, 12, 10, lw=0.9, fill=PAL.brass)
            s.circle(lx, ly + 5, 1.3, lw=0, fill=K, stroke=False)

    def awning(s, x0, x1, y, depth=22, n=10):
        with s.tint(STRIPE_LT, dark=STRIPE): super().awning(x0, x1, y, depth=depth, n=n)
        s.c.saveState()   # soft shadow under the wall edge; s.c.setFillColor(C(60, 30, 30)); s.c.setFillAlpha(0.14)
        s.c.drawPath(s.path([(x0, y), (x1, y), (x1 + 3, y - depth * 0.35), (x0 - 3, y - depth * 0.35)], closed=True), stroke=0, fill=1); s.c.restoreState()

    def rain(s, x0, y0, x1, y1, n=160, L=12, lw=0.5, seed=0, color=None):
        rr = random.Random(seed)
        for _ in range(n):
            x = rr.uniform(x0, x1); y = rr.uniform(y0, y1); l = L * rr.uniform(0.6, 1.2)
            s.line([(x, y), (x - l * 0.28, y - l)], lw=lw, amp=0, color=color or RAIN)

    def puddle(s, x, y, w):
        s.shape(s.arcpts(x, y, w / 2, w * 0.09, 0, 360, 24), lw=0.5, fill=WATER, amp=0.5)
        s.line(s.arcpts(x - w * 0.1, y, w * 0.12, w * 0.03, 200, 340, 8), lw=0.6, amp=0, color=Wt)

    def storm_sky(s, x0, y0, x1, y1):
        s.vgrad(x0, y0, x1, y1, STORM, STORM2, steps=14)
        rr = random.Random(int(x0 + y0))
        for i in range(7):
            cx = lerp(x0, x1, (i + 0.5) / 7) + rr.uniform(-12, 12); cy = y0 + (y1 - y0) * rr.uniform(0.25, 0.7)
            s.shape(s.arcpts(cx, cy, (x1 - x0) / 7.5, (y1 - y0) * 0.22, 0, 360, 20), lw=0.7, fill=mix(STORM, K, 0.12 + 0.06 * (i % 3)), amp=0.6)
        for i in range(6): s.shape(s.arcpts(lerp(x0, x1, (i + 0.5) / 6), y0 + 6, (x1 - x0) / 11, 12, 180, 360, 12), lw=0.8, fill=mix(STORM2, PAL.cloud, 0.2), amp=0.3)

    def shopfront(s, x, y, w, h, sign="T. TREVELYAN \u00b7 BOOKS", awning=True, lit=True, bell=False):
        s.wall(x, y, w, h, gap=3.2, color=SHOPWALL)
        s.rect(x - 3, y + h - 4, w + 6, 7, lw=0.9, fill=SIGN)                                     # cornice
        s.rect(x + w * 0.06, y + h * 0.8, w * 0.88, h * 0.12, lw=1.0, fill=SIGN)
        s.rect(x + w * 0.07, y + h * 0.81, w * 0.86, h * 0.10, lw=0.4, fill=None)
        s.text(x + w / 2, y + h * 0.83, sign, size=h * 0.065, font="Ink-Playfair", color=GOLD)
        wx, ww, wy, wh = x + w * 0.06, w * 0.56, y + h * 0.14, h * 0.5
        s.rect(wx - 4, wy - 4, ww + 8, wh + 8, lw=1.0, fill=SIGN)
        s.rect(wx, wy, ww, wh, lw=1.0, fill=C(255, 240, 200) if lit else GLASS)
        for j in range(2): s.spines(wx + 4, wx + ww - 4, wy + 3 + j * wh * 0.42, wh * 0.3, seed=j * 7)
        s.rect(wx, wy + wh * 0.42 - 1.5, ww, 3, lw=0.6, fill=WOOD)
        for u in (0.33, 0.66): s.line([(wx + ww * u, wy), (wx + ww * u, wy + wh)], lw=1.2, amp=0, color=SIGN)
        s.line([(wx + 6, wy + wh - 6), (wx + 26, wy + wh - 26)], lw=1.2, amp=0, color=Wt)
        s.rect(wx - 6, wy - 8, ww + 12, 6, lw=0.8, fill=WOOD_DK)                                       # sill
        for i in range(5): s.circle(wx + 12 + i * (ww - 24) / 4, wy - 12, 4.5, lw=0.5, fill=[PAL.pea_pink, PAL.sun, PAL.pea_purple, PAL.cloud, PAL.pea_pink][i])   # flower box
        s.rect(wx + 4, wy - 18, ww - 8, 8, lw=0.7, fill=C(110, 150, 110))
        dx, dw = x + w * 0.7, w * 0.22
        s.shape([(dx - 3, y), (dx + dw + 3, y), (dx + dw + 3, y + h * 0.69), (dx - 3, y + h * 0.69)], lw=0.9, fill=SIGN, amp=0)
        s.shape([(dx, y), (dx + dw, y), (dx + dw, y + h * 0.66), (dx, y + h * 0.66)], lw=1.0, fill=DOOR, amp=0)
        s.rect(dx + dw * 0.18, y + h * 0.34, dw * 0.64, h * 0.26, lw=0.7, fill=C(255, 236, 190))
        s.rect(dx + dw * 0.18, y + h * 0.06, dw * 0.64, h * 0.2, lw=0.6, fill=shade(DOOR, 0.86))
        s.circle(dx + dw * 0.82, y + h * 0.3, 1.8, lw=0.4, fill=PAL.brass)
        s.rect(dx + dw * 0.3, y + h * 0.43, dw * 0.4, h * 0.07, lw=0.4, fill=PAL.cloud); s.text(dx + dw * 0.5, y + h * 0.445, "OPEN", size=h * 0.04, font="Ink-Plex", color=SIGN)
        # hanging sign on a bracket, with a little book
        bx, byy = x + w + 2, y + h * 0.72
        s.line([(x + w - 4, byy + 18), (bx + 30, byy + 18)], lw=1.2, amp=0)
        s.rect(bx + 4, byy - 14, 26, 26, lw=0.9, fill=SIGN)
        s.rect(bx + 10, byy - 8, 14, 14, lw=0.6, fill=GOLD); s.line([(bx + 17, byy - 8), (bx + 17, byy + 6)], lw=0.5, amp=0)
        if awning: s.awning(x + w * 0.02, x + w * 0.66, y + h * 0.74, depth=h * 0.13, n=10)

    def street(s, w, h, y=70, wet=False):
        top = [(14, y), (w - 14, y + 14)]
        s.wash([(14, 14), (w - 14, 14), (w - 14, y + 14), (14, y)], COBBLE_WET if wet else COBBLE)
        s.wash([(14, y - 8), (w - 14, y + 6), (w - 14, y + 14), (14, y)], C(214, 206, 192) if not wet else C(176, 182, 188))   # pavement
        s.line(top, lw=1.0, amp=0.3)
        s.line([(14, y - 8), (w - 14, y + 6)], lw=0.5, amp=0.3)
        rr = random.Random(7)
        for j in range(4):
            yy = y - 20 - j * 12
            for i in range(26):
                cx = 18 + i * 19 + (j % 2) * 9
                col = mix(COBBLE_WET if wet else COBBLE, Wt if rr.random() < 0.5 else K, rr.uniform(0.04, 0.16))
                s.shape(s.arcpts(cx, yy + cx * 0.027, 7.5, 3.6, 0, 360, 10), lw=0.4, fill=col, amp=0.2)
                if wet and rr.random() < 0.3: s.line([(cx - 3, yy + cx * 0.027 + 1), (cx + 1, yy + cx * 0.027 + 1.6)], lw=0.5, amp=0, color=Wt)
        if wet:
            for (px, py, pw) in ((90, 30, 70), (260, 40, 90), (420, 34, 60)): s.puddle(px, py, pw)

    def telephone(s, x, y, w, ringing=False):
        with s.tint(PHONE, dark=PHONE): super().telephone(x, y, w, ringing=False)
        s.circle(x, y + w * 0.24, w * 0.15, lw=0.5, fill=PAL.cloud)
        if ringing:
            for sg in (-1, 1):
                for j in range(3):
                    r = w * (0.62 + 0.16 * j)
                    s.line(s.arcpts(x, y + w * 0.4, r, r * 0.9, (20 if sg > 0 else 140), (50 if sg > 0 else 170), 6), lw=0.8, amp=0, color=shade(PHONE, 0.8))

    def door_bell(s, x, y, w, ringing=True):
        with s.tint(PAL.brass, hatch=shade(PAL.brass, 0.7)): super().door_bell(x, y, w, ringing=False)
        if ringing:
            for sg in (-1, 1):
                for j in range(3):
                    r = w * (0.75 + 0.22 * j)
                    s.line(s.arcpts(x, y + w * 0.35, r, r, (-25 if sg > 0 else 155), (25 if sg > 0 else 205), 6), lw=0.9, amp=0, color=shade(PAL.brass, 0.6))

    def counter(s, x0, x1, y, h=70):
        s.rect(x0, y, x1 - x0, h, lw=1.0, fill=WOOD)
        with s.tint(WOOD): s.hatch([(x0, y), (x1, y), (x1, y + h), (x0, y + h)], angle=0, gap=2.4, lw=0.35)
        for u in (0.33, 0.66): s.line([(lerp(x0, x1, u), y + 4), (lerp(x0, x1, u), y + h - 4)], lw=0.6, amp=0)
        for j in range(3): s.rect(lerp(x0, x1, j / 3) + 5, y + 8, (x1 - x0) / 3 - 10, h - 16, lw=0.4, fill=None)
        s.rect(x0 - 4, y + h, x1 - x0 + 8, 7, lw=1.0, fill=WOOD_DK)

    def cottage_row(s, x, y, w, h, i=0, label=None):
        s.wall(x, y, w, h * 0.62, gap=2.6, color=PAL.walls[i % 6])
        s.roof(x, x + w, y + h * 0.62, y + h, overhang=3, color=PAL.slate if i % 2 == 0 else PAL.roof)
        s.window(x + w * 0.15, y + h * 0.3, w * 0.25, h * 0.2)
        s.rect(x + w * 0.13, y + h * 0.29, w * 0.29, h * 0.02, lw=0.5, fill=PAL.cloud)   # sill
        dc = PAL.doors[(i + 1) % len(PAL.doors)]
        s.shape([(x + w * 0.58, y), (x + w * 0.82, y), (x + w * 0.82, y + h * 0.4), (x + w * 0.58, y + h * 0.4)], lw=0.8, fill=dc, amp=0)
        s.rect(x + w * 0.62, y + h * 0.24, w * 0.16, h * 0.1, lw=0.4, fill=shade(dc, 0.85))
        s.circle(x + w * 0.78, y + h * 0.18, 1.2, lw=0.3, fill=PAL.brass)
        s.chimney(x + w * 0.7, y + h * 0.8, w * 0.1, h * 0.22, smoke=False)
        if label:
            s.rect(x + w * 0.08, y + h * 0.52, w * 0.84, h * 0.08, lw=0.7, fill=C(250, 252, 248))
            s.text(x + w / 2, y + h * 0.54, label, size=h * 0.05, font="Ink-Plex", color=C(50, 120, 80))
            cx, cy, a = x + w * 0.38, y + h * 0.42, h * 0.035   # green chemist's cross
            for (dx, dy, ww, hh) in ((-a, -a * 3, 2 * a, 6 * a), (-a * 3, -a, 6 * a, 2 * a)): s.rect(cx + dx, cy + dy, ww, hh, lw=0.4, fill=C(80, 170, 110))

    def lamppost(s, x, y, h):
        s.rect(x - 2, y, 4, h, lw=0.8, fill=C(54, 70, 72))
        s.rect(x - 5, y, 10, 6, lw=0.7, fill=C(54, 70, 72))
        s.shape([(x - 8, y + h), (x + 8, y + h), (x + 5, y + h + 16), (x - 5, y + h + 16)], lw=0.8, fill=C(255, 236, 180), amp=0)
        s.shape([(x - 9, y + h + 16), (x + 9, y + h + 16), (x, y + h + 24)], lw=0.8, fill=C(54, 70, 72), amp=0)

    def flower_tub(s, x, y, w):
        s.shape([(x - w / 2, y + w * 0.5), (x + w / 2, y + w * 0.5), (x + w * 0.38, y), (x - w * 0.38, y)], lw=0.8, fill=C(150, 104, 80), amp=0)
        rr = random.Random(int(x))
        for i in range(9):
            px = x + rr.uniform(-w * 0.45, w * 0.45); py = y + w * 0.5 + rr.uniform(2, w * 0.5)
            s.circle(px, py, w * 0.09, lw=0.4, fill=PAL.leaf)
        for i in range(7):
            px = x + rr.uniform(-w * 0.42, w * 0.42); py = y + w * 0.6 + rr.uniform(2, w * 0.5)
            s.circle(px, py, w * 0.07, lw=0.4, fill=rr.choice([PAL.pea_pink, PAL.sun, PAL.pea_purple, STRIPE]))

def dim(k, w, h, col=C(40, 56, 80), a=0.22):
    """Storm light: a translucent blue-grey veil over everything drawn so far."""
    k.c.saveState(); k.c.setFillColor(col); k.c.setFillAlpha(a); k.c.rect(0, 0, w, h, stroke=0, fill=1); k.c.restoreState()

def frame_open(k, w, h):
    k.frame2(w, h); k.clip_rect(14, 14, w - 14, h - 14)

def interior(k, w, h, floor=96, shelves=(30, 150, 370), label=None, lamp=True):
    """Back of the bookshop: cream walls over a panelled wainscot, honey floorboards, tall wooden bookcases."""
    k.wash_rect(14, floor, w - 14, h - 14, WALL_IN)
    k.wash_rect(14, floor, w - 14, floor + 34, WAINSCOT)
    for i in range(int((w - 28) / 36) + 1):
        x = 18 + i * 36
        if x + 28 < w - 14: k.rect(x, floor + 5, 28, 24, lw=0.4, fill=shade(WAINSCOT, 0.92))
    k.line([(14, floor + 34), (w - 14, floor + 34)], lw=0.8, amp=0.1)
    k.vgrad(14, 14, w - 14, floor, FLOOR, FLOOR2, steps=10)
    for i in range(10): k.line([(14, 14 + i * 9), (w - 14, 14 + i * 9)], lw=0.35, amp=0.2, color=shade(FLOOR2, 0.72))
    rr = random.Random(int(w + floor))
    for i in range(10):
        for j in range(4):
            xx = rr.uniform(20, w - 20); k.line([(xx, 14 + i * 9), (xx, 23 + i * 9)], lw=0.35, amp=0, color=shade(FLOOR2, 0.72))
    k.line([(14, floor), (w - 14, floor)], lw=1.0, amp=0.1)
    if lamp:   # warm pendant lamps
        for lx in (w * 0.36, w * 0.7):
            k.line([(lx, h - 14), (lx, h - 52)], lw=0.6, amp=0)
            k.shape([(lx - 13, h - 64), (lx + 13, h - 64), (lx + 5, h - 52), (lx - 5, h - 52)], lw=0.8, fill=C(92, 140, 120), amp=0)
            k.circle(lx, h - 66, 4, lw=0.5, fill=C(255, 236, 170))
    for j, x in enumerate(shelves): k.bookcase(x, floor, 110, h - floor - 46, shelves=5, seed=j * 13, label=label if j == len(shelves) - 1 else None)

def sunny_sky(k, w, h, y0, cloud=True):
    k.vgrad(14, y0, w - 14, h - 14, PAL.sky, PAL.sky2, steps=18)
    if cloud:
        for (cx, cy, s_) in ((w * 0.18, h * 0.86, 1.0), (w * 0.6, h * 0.9, 0.7)):
            for (dx, dy, r) in ((0, 0, 16), (16, 4, 13), (-15, 2, 11), (6, 10, 11)):
                k.circle(cx + dx * s_, cy + dy * s_, r * s_, lw=0, fill=PAL.cloud, stroke=False)

def hedley_s(k, x, y, h, **kw): P.hedley(k, x, y, h, **kw)

# ============================================================================= scenes (4:3, 512 x 384)
def street_scene(k, w, h):
    frame_open(k, w, h)
    sunny_sky(k, w, h, 74)
    k.circle(w * 0.88, h * 0.86, 18, lw=0.9, fill=PAL.sun)
    k.gull(w * 0.3, h * 0.9, 16); k.gull(w * 0.4, h * 0.94, 11)
    k.street(w, h, y=74)
    k.cottage_row(20, 76, 100, 170, i=2, label="CHEMIST")
    k.shopfront(124, 78, 230, 200)
    k.cottage_row(370, 84, 70, 160, i=0); k.cottage_row(442, 88, 70, 150, i=1)
    k.lamppost(362, 82, 120)
    k.flower_tub(112, 76, 18); k.flower_tub(452, 88, 16)
    k.unclip()

def case_scene(k, w, h):
    frame_open(k, w, h)
    interior(k, w, h, shelves=(30, 370))
    k.glass_case(250, 74, 150, 230, book=True)
    P.tamsin(k, 128, 64, 220, prop="duster")
    k.rect(420, 150, 80, 6, lw=0.8, fill=WOOD_DK); k.rect(428, 74, 64, 76, lw=0.8, fill=WOOD)   # little side table
    k.telephone(460, 156, 30, ringing=True)
    k.unclip()

def storm_scene(k, w, h):
    frame_open(k, w, h)
    k.storm_sky(14, h * 0.62, w - 14, h - 14)
    k.wash_rect(14, 74, w - 14, h * 0.62, STORM2)
    k.street(w, h, y=74, wet=True)
    k.cottage_row(20, 76, 100, 170, i=2, label="CHEMIST")
    k.shopfront(124, 78, 230, 200)
    k.cottage_row(370, 84, 70, 160, i=0); k.cottage_row(442, 88, 70, 150, i=1)
    k.lamppost(362, 82, 120)
    dim(k, w, h)
    # the street running like a river
    k.wash([(14, 14), (w - 14, 14), (w - 14, 60), (14, 48)], mix(WATER, STORM, 0.3))
    for i in range(14):
        x0 = 20 + (i * 37) % 470; y0 = 18 + (i * 13) % 36
        k.line([(x0, y0), (x0 + 18, y0 + 2), (x0 + 36, y0 + 1)], lw=0.8, amp=0.6, color=Wt)
    for gx in (170, 300, 410):   # overflowing gutters
        for j in range(4): k.line([(gx + j * 3, 262 - j * 2), (gx + j * 3 - 2, 230 - j * 3)], lw=0.8, amp=0.4, color=C(200, 222, 240))
    k.rain(14, 20, w - 14, h - 20, n=300, L=14, lw=0.6, seed=4, color=C(214, 226, 240))
    k.unclip()

def gone_scene(k, w, h, mark=True):
    frame_open(k, w, h)
    interior(k, w, h, shelves=(30, 370))
    k.glass_case(250, 74, 150, 230, book=False, open_=True)
    if mark: k.text(250, 316, "?", size=48, font="Ink-Playfair", color=VELVET)
    k.unclip()

def hook_scene(k, w, h): gone_scene(k, w, h, mark=False)

def chemist_scene(k, w, h):
    """After the rain: Agnes comes over from the chemist's next door, Tamsin at the bookshop door."""
    frame_open(k, w, h)
    k.vgrad(14, 74, w - 14, h - 14, C(196, 214, 226), C(226, 230, 228), steps=14)
    k.street(w, h, y=74, wet=True)
    k.cottage_row(20, 76, 120, 200, i=2, label="CHEMIST")
    k.shopfront(150, 78, 300, 260)
    for i in range(6): k.line([(166 + i * 40, 300), (163 + i * 40, 288)], lw=0.8, amp=0, color=C(150, 190, 220))   # last drips from the awning
    P.agnes(k, 110, 40, 200, bag=True)
    P.tamsin(k, 392, 40, 200, prop=None)
    k.unclip()

PW = 512
def lineup(k, w, h):
    """Hedley at the counter | Pip under the striped awning outside | Wenna by the poetry shelves.
    Same height, stance, face, carry pose and nameplate for all three suspects."""
    for i in range(3):
        k.c.saveState(); k.c.translate(i * PW, 0); pw = PW
        k.frame2(pw, h); k.clip_rect(14, 14, pw - 14, h - 14); cx = pw / 2; fh = 236
        if i == 0:
            interior(k, pw, h, shelves=(300,))
            P.tamsin(k, cx + 150, 88, 210, prop=None)
            k.counter(cx + 50, pw - 24, 70, 74)
            k.rect(cx + 70, 151, 40, 26, lw=0.8, fill=C(150, 60, 56)); k.rect(cx + 76, 160, 28, 10, lw=0.4, fill=PAL.cloud)   # till
            k.rect(cx + 120, 151, 30, 8, lw=0.6, fill=C(70, 110, 140)); k.rect(cx + 122, 159, 26, 6, lw=0.6, fill=C(214, 172, 86))   # fishing books on the counter
            P.drips(k, cx - 46, 70, fh)
            P.hedley(k, cx - 46, 70, fh, wet=True)
            nameplate(k, cx, 40, "HEDLEY TRUSCOTT")
        elif i == 1:
            k.vgrad(14, 60, pw - 14, h - 14, STORM, STORM2, steps=12)
            k.street(pw, h, y=60, wet=True)
            k.shopfront(30, 62, 460, 380, awning=False)     # taller crop: the awning sits clear above Pip's head
            k.awning(20, 330, 362, depth=50, n=11)
            k.rain(304, 20, pw - 14, h - 20, n=80, L=13, lw=0.6, seed=8)
            k.rain(14, 20, 304, 120, n=60, L=12, lw=0.6, seed=9)
            P.pip(k, cx - 46, 70, fh)
            nameplate(k, cx, 40, "PIP CAREW")
        else:
            interior(k, pw, h, shelves=(250, 370), label="POETRY")
            k.rect(40, 96, 90, 40, lw=0.8, fill=WOOD); k.spines(46, 124, 137, 22, seed=40)   # low table of books
            P.wenna(k, cx - 46, 70, fh)
            nameplate(k, cx, 40, "WENNA POLGLAZE")
        k.unclip(); k.c.restoreState()

def bell_scene(k, w, h):
    """The shop door from inside: the little brass bell over it, wet street through the glass."""
    frame_open(k, w, h)
    interior(k, w, h, shelves=(), lamp=False)
    dx, dw, dh = 190, 132, 230
    k.rect(dx - 10, 96, dw + 20, dh + 10, lw=1.2, fill=WOOD_DK)
    k.rect(dx, 96, dw, dh, lw=1.0, fill=DOOR)
    k.rect(dx + 14, 200, dw - 28, 110, lw=0.9, fill=STORM2)
    k.c.saveState(); k.clip_rect(dx + 15, 201, dx + dw - 15, 309)
    k.wash_rect(dx + 15, 201, dx + dw - 15, 236, COBBLE_WET)
    k.rain(dx + 16, 204, dx + dw - 16, 306, n=50, L=10, lw=0.55, seed=2, color=C(220, 230, 240))
    k.c.restoreState()
    k.rect(dx + 30, 230, dw - 60, 22, lw=0.8, fill=PAL.cloud); k.text(dx + dw / 2, 236, "OPEN", size=12, font="Ink-Plex", color=SIGN)
    k.line([(dx + 34, 252), (dx + dw / 2, 272), (dx + dw - 34, 252)], lw=0.6, amp=0)
    k.circle(dx + dw - 16, 180, 3.2, lw=0.6, fill=PAL.brass)
    for j in range(3): k.rect(dx + 14, 110 + j * 28, dw - 28, 20, lw=0.6, fill=shade(DOOR, 0.88))
    k.door_bell(dx + dw / 2, 330, 22, ringing=True)
    k.bookcase(30, 96, 110, 240, shelves=5, seed=5); k.bookcase(370, 96, 110, 240, shelves=5, seed=9)
    k.unclip()

def thinking_scene(k, w, h):
    """Agnes in the bookshop, looking things over; the shower has passed and the street outside is wet."""
    frame_open(k, w, h)
    interior(k, w, h, shelves=(30,), lamp=False)
    k.rect(190, 150, 290, 170, lw=1.2, fill=PAL.sky)
    k.c.saveState(); k.clip_rect(192, 152, 478, 318)
    k.c.translate(190, 150); k.c.scale(290 / w, 170 / h)
    k.vgrad(0, 0, w, h, C(196, 214, 226), C(230, 234, 230), steps=10)
    k.street(w, h, y=74, wet=True); k.cottage_row(40, 76, 140, 200, i=1); k.cottage_row(200, 80, 140, 200, i=4); k.cottage_row(360, 84, 140, 200, i=3)
    k.c.restoreState()
    k.line([(335, 150), (335, 320)], lw=2.0, amp=0, color=WOOD_DK); k.line([(190, 235), (480, 235)], lw=2.0, amp=0, color=WOOD_DK)
    k.rect(184, 142, 302, 8, lw=0.9, fill=WOOD)
    for i in range(4): k.circle(214 + i * 78, 154, 5, lw=0.5, fill=[PAL.pea_pink, PAL.sun, PAL.pea_purple, PAL.pea_pink][i])
    P.agnes(k, 240, 50, 230)
    k.unclip()

def compare_scene(k, w, h):
    """Solution: Hedley, soaked after a short walk, beside Wenna, completely dry."""
    frame_open(k, w, h)
    k.c.saveState(); k.clip_rect(14, 14, w / 2, h - 14)
    k.vgrad(14, 96, w / 2, h - 14, STORM, STORM2, steps=12)
    k.street(w, h, y=96, wet=True)
    k.storm_sky(14, h - 70, w / 2 - 4, h - 14)
    k.rain(20, 120, w / 2 - 10, h - 74, n=90, L=12, lw=0.6, seed=12)
    k.c.restoreState()
    k.c.saveState(); k.clip_rect(w / 2, 14, w - 14, h - 14)
    interior(k, w, h, shelves=(300, 400), lamp=False)
    k.c.restoreState()
    k.line([(w / 2, 14), (w / 2, h - 14)], lw=1.2, amp=0.2)
    P.drips(k, w * 0.25, 70, 200, n=12)
    P.hedley(k, w * 0.25, 70, 200, wet=True)
    P.wenna(k, w * 0.72, 70, 200)
    nameplate(k, w * 0.25, 30, "HEDLEY: A SHORT WALK", size=11)
    nameplate(k, w * 0.72, 30, "WENNA: \u201cRAN FROM THE HARBOUR\u201d", size=11)
    for (lx, txt, sz, col) in ((w * 0.25, "soaked", 22, C(40, 70, 120)), (w * 0.72, "coat, hair, shoes: dry!", 19, C(150, 50, 40))):
        tw = k.c.stringWidth(txt, "Ink-CrimsonI", sz)
        k.shape([(lx - tw / 2 - 10, 280), (lx + tw / 2 + 10, 280), (lx + tw / 2 + 10, 280 + sz + 8), (lx - tw / 2 - 10, 280 + sz + 8)], lw=0.9, fill=PAL.card, amp=0.2)
        k.text(lx, 285, txt, size=sz, font="Ink-CrimsonI", color=col)
    k.unclip()

def returned_scene(k, w, h):
    """Tamsin gives Wenna an ordinary copy; the signed one is back in its case, locked."""
    frame_open(k, w, h)
    interior(k, w, h, shelves=(30, 380))
    k.glass_case(256, 74, 120, 200, book=True, lock=True)
    P.wenna(k, 132, 50, 220, expr="sheepish", scarf=True)
    P.tamsin(k, 392, 50, 220, prop="book", flip=True)
    k.unclip()

def cast_strip(k, w, h):
    """Three suspects side by side for the opening hook (same height, pose and colour weight)."""
    k.wash_rect(0, 0, w, h, WALL_IN)
    k.wash_rect(0, 22, w, 64, WAINSCOT); k.line([(0, 64), (w, 64)], lw=0.8, amp=0.1)
    for i in range(int(w / 40) + 1): k.rect(6 + i * 40, 28, 32, 32, lw=0.4, fill=shade(WAINSCOT, 0.92))
    k.wash_rect(0, 0, w, 22, FLOOR); k.line([(0, 22), (w, 22)], lw=1.0, amp=0)
    for i in range(4): k.line([(0, 6 + i * 4), (w, 6 + i * 4)], lw=0.3, amp=0.2, color=shade(FLOOR2, 0.72))
    k.rect(-4, h - 34, w + 8, 4, lw=0.9, fill=WOOD); k.spines(4, w - 4, h - 30, 26, seed=3)
    for i, fn in enumerate([P.hedley, P.pip, P.wenna]):
        fn(k, w * (0.17 + 0.32 * i), 20, h * 0.8)
    k.c.setStrokeColor(K); k.c.setLineWidth(1.3); k.c.rect(1, 1, w - 2, h - 2, stroke=1, fill=0)

def vignette(k, w, h):
    k.circle(w / 2, h / 2, w * 0.46, lw=1.3, fill=PAL.cloud); k.circle(w / 2, h / 2, w * 0.44, lw=0.45, fill=None)
    k.c.saveState(); p = k.c.beginPath(); p.circle(w / 2, h / 2, w * 0.44 - 1); k.c.clipPath(p, stroke=0, fill=0)
    k.wash_rect(0, 0, w, h * 0.36, WAINSCOT)
    for i in range(6): k.rect(w * 0.06 + i * w * 0.15, h * 0.08, w * 0.12, h * 0.22, lw=0.5, fill=shade(WAINSCOT, 0.92))
    k.storm_sky(0, h * 0.72, w, h)
    k.wash_rect(0, h * 0.36, w, h * 0.72, STORM2)
    k.rain(0, h * 0.4, w, h * 0.72, n=70, L=12, lw=0.6, seed=1, color=C(220, 230, 240))
    k.rect(w * 0.1, h * 0.34, w * 0.8, 10, lw=0.9, fill=WOOD)
    bks = ((150, 22, SPINES[1]), (130, 20, SPINES[0]), (140, 24, SPINES[3]))
    for j, (bw, bh, col) in enumerate(bks):
        y0 = h * 0.37 + sum(b[1] for b in bks[:j])
        k.rect(w * 0.3 - bw / 2 + j * 6, y0, bw, bh, lw=0.9, fill=col)
        k.rect(w * 0.3 - bw / 2 + j * 6 + bw - 14, y0 + 2, 10, bh - 4, lw=0.4, fill=PAL.paper)
    with k.tint(PAL.teapot): k.teapot(w * 0.7, h * 0.37, 80)
    k.c.restoreState()

AW, AH = 512, 384
SCENES = dict(street=(street_scene, AW, AH), case=(case_scene, AW, AH), storm=(storm_scene, AW, AH), gone=(gone_scene, AW, AH),
              hook=(hook_scene, AW, AH), chemist=(chemist_scene, AW, AH), lineup=(lineup, 3 * PW, AH), bell=(bell_scene, AW, AH),
              thinking=(thinking_scene, AW, AH), compare=(compare_scene, AW, AH), returned=(returned_scene, AW, AH),
              cast=(cast_strip, 600, 260), vignette=(vignette, 384, 384))

def _one(args):
    i, name = args
    fn, pw, ph = SCENES[name]
    def draw(c, W, H, fn=fn, i=i):
        k = ShopC(c, seed=31 + i); fn(k, W, H)
    render_color(os.path.join(OUT, name + ".png"), pw / 72, ph / 72, draw, seed=31 + i)
    return name

if __name__ == "__main__":
    from concurrent.futures import ProcessPoolExecutor
    os.makedirs(OUT, exist_ok=True)
    want = [a for a in sys.argv[1:] if not a.startswith("--")] or list(SCENES)
    idx = {n: i for i, n in enumerate(SCENES)}
    with ProcessPoolExecutor(min(8, len(want))) as ex:
        for n in ex.map(_one, [(idx[n], n) for n in want]): print(n, flush=True)
