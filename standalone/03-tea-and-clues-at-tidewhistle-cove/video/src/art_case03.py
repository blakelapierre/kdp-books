"""Illustrations for Case 3, The Dry Raincoat, in the BLACK-AND-WHITE ink style (colorink.set_style("bw"):
pure black ink and paper white, hatching for tone, no colour fills), with the simple v1 peg-doll characters
from figures.py. Output: ../work/art-03/*.png       Run: python3 art_case03.py [scene ...] [--color]
(--color draws the same scenes with colour washes instead; the case video uses black and white.)"""
import math, os, sys
import colorink
colorink.set_style("color" if "--color" in sys.argv else "bw")
from inkart import lerp, K, Wt
from colorink import PAL, C, render_color, shade
import figures as F
from art import Sea, nameplate

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-03")
SHOPWALL = C(236, 226, 206); SPINES = [C(150, 70, 60), C(70, 100, 130), C(90, 130, 90), C(200, 170, 90), C(30, 30, 40), C(240, 236, 226)]

class Shop(Sea):
    def spines(s, x0, x1, y, h, seed=0, gaps=False):
        """A shelf row of book spines standing on y (mixed widths: white, hatched or solid black)."""
        x = x0; i = seed
        while x < x1 - 4:
            w = 5 + (i * 7) % 6; hh = h * (0.72 + 0.28 * ((i * 5) % 7) / 6)
            if x + w > x1: break
            pts = [(x, y), (x + w, y), (x + w, y + hh), (x, y + hh)]
            kind = (i * 3) % 5
            k = s.shape(pts, lw=0.55, fill=K if kind == 0 else Wt, amp=0)
            if kind == 2: s.hatch(pts, angle=90, gap=1.4, lw=0.3, jitter=0)
            elif kind == 3: s.line([(x + 1, y + hh * 0.75), (x + w - 1, y + hh * 0.75)], lw=0.5, amp=0)
            x += w + (3 if gaps and i % 9 == 4 else 0.4); i += 1

    def bookcase(s, x, y, w, h, shelves=4, seed=0, label=None):
        s.rect(x, y, w, h, lw=1.0, fill=Wt)
        with s.tint(PAL.wood): s.hatch([(x, y), (x + 6, y), (x + 6, y + h), (x, y + h)], angle=90, gap=1.6, lw=0.35)
        sh = (h - 10) / shelves
        for j in range(shelves):
            yy = y + 6 + j * sh
            s.line([(x + 2, yy), (x + w - 2, yy)], lw=1.0, amp=0)
            s.spines(x + 9, x + w - 4, yy + 1, sh * 0.78, seed=seed + j * 11)
        s.rect(x - 3, y + h, w + 6, 5, lw=0.9, fill=Wt)
        if label:
            tw = s.c.stringWidth(label, "Ink-Plex", 9)
            s.rect(x + w / 2 - tw / 2 - 6, y + h + 8, tw + 12, 14, lw=0.7, fill=Wt)
            s.text(x + w / 2, y + h + 11.5, label, size=9, font="Ink-Plex")

    def puffin_book(s, x, y, w):
        """The signed first copy: a hardback cover with a little puffin, standing on a stand. (x, y) bottom centre."""
        h = w * 1.3
        s.rect(x - w / 2, y, w, h, lw=0.9, fill=Wt)
        s.rect(x - w / 2 + w * 0.08, y + h * 0.06, w * 0.84, h * 0.88, lw=0.4, fill=None)
        px, py, r = x, y + h * 0.42, w * 0.16   # the puffin
        s.shape(s.arcpts(px, py, r, r * 1.35, 0, 360, 20), lw=0.6, fill=K, amp=0)
        s.shape(s.arcpts(px + r * 0.15, py - r * 0.25, r * 0.6, r * 0.85, 0, 360, 16), lw=0.4, fill=Wt, amp=0)
        s.circle(px + r * 0.1, py + r * 1.6, r * 0.62, lw=0.6, fill=K)
        s.circle(px + r * 0.25, py + r * 1.7, r * 0.34, lw=0.3, fill=Wt)
        s.circle(px + r * 0.3, py + r * 1.72, r * 0.1, lw=0, fill=K, stroke=False)
        s.shape([(px + r * 0.6, py + r * 1.8), (px + r * 1.2, py + r * 1.55), (px + r * 0.62, py + r * 1.35)], lw=0.5, fill=Wt, amp=0)
        s.hatch([(px + r * 0.6, py + r * 1.8), (px + r * 1.2, py + r * 1.55), (px + r * 0.62, py + r * 1.35)], angle=90, gap=1.0, lw=0.3, jitter=0)
        for j in range(2): s.line([(x - w * 0.28, y + h * (0.84 - 0.07 * j)), (x + w * 0.28, y + h * (0.84 - 0.07 * j))], lw=0.6 - 0.2 * j, amp=0)
        s.line([(x - w * 0.22, y + h * 0.12), (x - w * 0.02, y + h * 0.16), (x + w * 0.1, y + h * 0.11), (x + w * 0.26, y + h * 0.15)], lw=0.6, amp=0.4)  # signature

    def glass_case(s, x, y, w, h, book=True, open_=False, lock=False):
        """Display case on legs at the back of the shop. (x, y) bottom centre of the legs."""
        legh = h * 0.42; by = y + legh
        for u in (-0.42, 0.42): s.rect(x + u * w - 2.5, y, 5, legh, lw=0.8, fill=Wt)
        s.rect(x - w / 2 - 4, by, w + 8, h * 0.08, lw=1.0, fill=Wt)
        with s.tint(PAL.wood): s.hatch([(x - w / 2 - 4, by), (x + w / 2 + 4, by), (x + w / 2 + 4, by + h * 0.08), (x - w / 2 - 4, by + h * 0.08)], angle=0, gap=1.4, lw=0.35)
        gy = by + h * 0.08; gh = h * 0.5
        s.rect(x - w / 2, gy, w, gh, lw=1.0, fill=Wt)
        s.rect(x - w * 0.18, gy, w * 0.36, h * 0.03, lw=0.6, fill=Wt)    # little velvet plinth
        s.hatch([(x - w * 0.18, gy), (x + w * 0.18, gy), (x + w * 0.18, gy + h * 0.03), (x - w * 0.18, gy + h * 0.03)], angle=0, gap=0.9, lw=0.3, jitter=0)
        if book: s.puffin_book(x, gy + h * 0.03, gh * 0.55)
        else:
            s.c.setStrokeColor(K); s.c.setLineWidth(0.4); s.c.setDash(2, 2)
            s.c.rect(x - gh * 0.275, gy + h * 0.03, gh * 0.55, gh * 0.55 * 1.3, stroke=1, fill=0); s.c.setDash()
        for g in (0.12, 0.2, 0.7):   # glass glints
            s.line([(x - w / 2 + w * g, gy + gh * 0.88), (x - w / 2 + w * g + gh * 0.25, gy + gh * 0.58)], lw=0.45, amp=0)
        s.rect(x - w / 2 - 2, gy + gh, w + 4, h * 0.05, lw=1.0, fill=Wt)
        if open_:   # front glass door swung open to the right
            s.shape([(x + w / 2, gy), (x + w / 2 + w * 0.32, gy - h * 0.04), (x + w / 2 + w * 0.32, gy + gh - h * 0.02), (x + w / 2, gy + gh)], lw=1.0, fill=Wt, amp=0)
            s.line([(x + w / 2 + w * 0.08, gy + gh * 0.7), (x + w / 2 + w * 0.2, gy + gh * 0.4)], lw=0.45, amp=0)
            s.circle(x + w / 2 + w * 0.28, gy + gh * 0.5, 1.6, lw=0.5, fill=K)
        else:
            s.circle(x + w / 2 - 5, gy + gh * 0.5, 1.6, lw=0.5, fill=K)
        if lock:
            lx, ly = x + w / 2 - 5, gy + gh * 0.5 - 12
            s.c.setStrokeColor(K); s.c.setLineWidth(1.4); s.c.arc(lx - 4, ly + 4, lx + 4, ly + 14, 0, 180)
            s.rect(lx - 6, ly, 12, 10, lw=0.9, fill=K)
            s.circle(lx, ly + 5, 1.3, lw=0, fill=Wt, stroke=False)

    def awning(s, x0, x1, y, depth=22, n=10):
        """Striped awning (bold black and white stripes) with a scalloped edge; y = top edge on the wall."""
        w = (x1 - x0) / n
        s.shape([(x0, y), (x1, y), (x1 + 6, y - depth), (x0 - 6, y - depth)], lw=1.0, fill=Wt, amp=0)
        for i in range(n):
            if i % 2 == 0:
                a0, a1 = x0 + i * w, x0 + (i + 1) * w
                b0, b1 = lerp(x0 - 6, x1 + 6, i / n), lerp(x0 - 6, x1 + 6, (i + 1) / n)
                s.shape([(a0, y), (a1, y), (b1, y - depth), (b0, y - depth)], lw=0.4, fill=K, amp=0)
        for i in range(n):
            b0 = lerp(x0 - 6, x1 + 6, i / n); bw = (x1 - x0 + 12) / n
            s.shape(s.arcpts(b0 + bw / 2, y - depth, bw / 2, 5, 180, 360, 10), lw=0.6, fill=K if i % 2 == 0 else Wt, amp=0)
        s.shape([(x0, y), (x1, y), (x1 + 6, y - depth), (x0 - 6, y - depth)], lw=1.0, fill=None, amp=0)

    def rain(s, x0, y0, x1, y1, n=160, L=12, lw=0.5, seed=0):
        import random
        rr = random.Random(seed)
        for _ in range(n):
            x = rr.uniform(x0, x1); y = rr.uniform(y0, y1); l = L * rr.uniform(0.6, 1.2)
            s.line([(x, y), (x - l * 0.28, y - l)], lw=lw, amp=0)

    def puddle(s, x, y, w):
        s.shape(s.arcpts(x, y, w / 2, w * 0.09, 0, 360, 24), lw=0.6, fill=Wt, amp=0.5)
        s.line(s.arcpts(x - w * 0.1, y, w * 0.12, w * 0.03, 200, 340, 8), lw=0.35, amp=0)

    def storm_sky(s, x0, y0, x1, y1):
        """Black storm clouds: dense cross-hatching under scalloped cloud edges."""
        pts = [(x0, y1), (x1, y1), (x1, y0 + 20)]
        for i in range(12, -1, -1):
            px = lerp(x0, x1, i / 12); pts.append((px, y0 + (8 if i % 2 else 0)))
        s.shape(pts, lw=0.9, fill=Wt, amp=0.6)
        s.hatch(pts, angle=30, gap=1.6, lw=0.4, cross=True)
        for i in range(6): s.shape(s.arcpts(lerp(x0, x1, (i + 0.5) / 6), y0 + 6, (x1 - x0) / 11, 12, 180, 360, 12), lw=0.8, fill=Wt, amp=0.3)

    def shopfront(s, x, y, w, h, sign="T. TREVELYAN \u00b7 BOOKS", awning=True, lit=True, bell=False):
        """The bookshop: rendered wall, big display window, door with fanlight, hanging sign, striped awning."""
        s.wall(x, y, w, h, gap=3.2, color=SHOPWALL)
        s.rect(x + w * 0.06, y + h * 0.8, w * 0.88, h * 0.12, lw=1.0, fill=K)
        s.text(x + w / 2, y + h * 0.83, sign, size=h * 0.065, font="Ink-Playfair", color=Wt)
        wx, ww, wy, wh = x + w * 0.06, w * 0.56, y + h * 0.14, h * 0.5
        s.rect(wx, wy, ww, wh, lw=1.0, fill=Wt)
        for j in range(2): s.spines(wx + 4, wx + ww - 4, wy + 3 + j * wh * 0.42, wh * 0.3, seed=j * 7)
        s.line([(wx, wy + wh * 0.42), (wx + ww, wy + wh * 0.42)], lw=0.7, amp=0)
        s.rect(wx - 3, wy - 6, ww + 6, 6, lw=0.8, fill=Wt)
        dx, dw = x + w * 0.7, w * 0.22
        s.shape([(dx, y), (dx + dw, y), (dx + dw, y + h * 0.66), (dx, y + h * 0.66)], lw=1.0, fill=K, amp=0)
        s.rect(dx + dw * 0.18, y + h * 0.34, dw * 0.64, h * 0.26, lw=0.7, fill=Wt)
        s.circle(dx + dw * 0.82, y + h * 0.3, 1.8, lw=0.4, fill=Wt)
        if awning: s.awning(x + w * 0.02, x + w * 0.66, y + h * 0.74, depth=h * 0.13, n=10)

    def cottage_row(s, x, y, w, h, i=0, label=None):
        s.wall(x, y, w, h * 0.62, gap=2.6, color=PAL.walls[i % 6])
        s.roof(x, x + w, y + h * 0.62, y + h, overhang=3, color=PAL.slate)
        s.window(x + w * 0.15, y + h * 0.3, w * 0.25, h * 0.2)
        s.shape([(x + w * 0.58, y), (x + w * 0.82, y), (x + w * 0.82, y + h * 0.4), (x + w * 0.58, y + h * 0.4)], lw=0.8, fill=K if i % 2 else Wt, amp=0)
        if label:
            s.rect(x + w * 0.08, y + h * 0.52, w * 0.84, h * 0.08, lw=0.7, fill=Wt)
            s.text(x + w / 2, y + h * 0.54, label, size=h * 0.05, font="Ink-Plex")

    def street(s, w, h, y=70, wet=False):
        """The cobbled main street rising gently uphill (y = kerb line)."""
        s.line([(14, y), (w - 14, y + 14)], lw=1.0, amp=0.3)
        s.line([(14, y - 8), (w - 14, y + 6)], lw=0.5, amp=0.3)
        for j in range(4):
            yy = y - 20 - j * 12
            for i in range(26):
                cx = 18 + i * 19 + (j % 2) * 9; s.shape(s.arcpts(cx, yy + cx * 0.027, 7.5, 3.6, 0, 360, 10), lw=0.4, fill=Wt, amp=0.2)
        if wet:
            for (px, py, pw) in ((90, 30, 70), (260, 40, 90), (420, 34, 60)): s.puddle(px, py, pw)

    def telephone(s, x, y, w, ringing=False):
        """Old desk telephone on (x, y)."""
        s.shape([(x - w / 2, y), (x + w / 2, y), (x + w * 0.35, y + w * 0.45), (x - w * 0.35, y + w * 0.45)], lw=0.8, fill=K, amp=0)
        s.circle(x, y + w * 0.24, w * 0.15, lw=0.5, fill=Wt)
        s.shape([(x - w * 0.5, y + w * 0.55), (x + w * 0.5, y + w * 0.55), (x + w * 0.42, y + w * 0.68), (x - w * 0.42, y + w * 0.68)], lw=0.8, fill=K, amp=0)
        if ringing:
            for sg in (-1, 1):
                for j in range(3):
                    r = w * (0.62 + 0.16 * j)
                    s.line(s.arcpts(x, y + w * 0.4, r, r * 0.9, (20 if sg > 0 else 140), (50 if sg > 0 else 170), 6), lw=0.6, amp=0)

    def door_bell(s, x, y, w, ringing=True):
        """Little brass shop bell on a curled bracket, hanging at (x, y)."""
        s.line([(x - w * 0.6, y + w * 1.1), (x, y + w * 1.1), (x, y + w * 0.75)], lw=1.2, amp=0)
        s.c.setStrokeColor(K); s.c.setLineWidth(1.0); s.c.arc(x - w * 0.9, y + w * 0.95, x - w * 0.5, y + w * 1.3, 90, 270)
        body = [(x - w * 0.5, y), (x + w * 0.5, y), (x + w * 0.32, y + w * 0.3), (x + w * 0.22, y + w * 0.72), (x - w * 0.22, y + w * 0.72), (x - w * 0.32, y + w * 0.3)]
        s.shape(body, lw=1.0, fill=Wt, amp=0)
        s.hatch([(x + w * 0.1, y), (x + w * 0.5, y), (x + w * 0.32, y + w * 0.3), (x + w * 0.22, y + w * 0.72), (x + w * 0.05, y + w * 0.72)], angle=80, gap=1.3, lw=0.35)
        s.circle(x, y - w * 0.08, w * 0.1, lw=0.7, fill=K)
        if ringing:
            for sg in (-1, 1):
                for j in range(3):
                    r = w * (0.75 + 0.22 * j)
                    s.line(s.arcpts(x, y + w * 0.35, r, r, (-25 if sg > 0 else 155), (25 if sg > 0 else 205), 6), lw=0.7, amp=0)

    def counter(s, x0, x1, y, h=70):
        s.rect(x0, y, x1 - x0, h, lw=1.0, fill=Wt)
        with s.tint(PAL.wood): s.hatch([(x0, y), (x1, y), (x1, y + h), (x0, y + h)], angle=0, gap=2.4, lw=0.35)
        for u in (0.33, 0.66): s.line([(lerp(x0, x1, u), y + 4), (lerp(x0, x1, u), y + h - 4)], lw=0.6, amp=0)
        s.rect(x0 - 4, y + h, x1 - x0 + 8, 7, lw=1.0, fill=Wt)

def frame_open(k, w, h):
    k.frame2(w, h); k.clip_rect(14, 14, w - 14, h - 14)

def interior(k, w, h, floor=96, shelves=(30, 150, 370), label=None):
    """Back of the bookshop: floorboards, tall bookcases."""
    for i in range(10): k.line([(14, 14 + i * 9), (w - 14, 14 + i * 9)], lw=0.3, amp=0.2)
    k.line([(14, floor), (w - 14, floor)], lw=1.0, amp=0.1)
    for j, x in enumerate(shelves): k.bookcase(x, floor, 110, h - floor - 46, shelves=5, seed=j * 13, label=label if j == len(shelves) - 1 else None)

def hedley_b(k, x, y, h, **kw):
    """Hedley with a fishing book in hand (his carry prop for this case)."""
    F.hedley(k, x, y, h, chair=False, **kw); F.fishing_book(k, x + h * 0.34, y + h * 0.48, h)

# ============================================================================= scenes (4:3, 512 x 384)
def street_scene(k, w, h):
    frame_open(k, w, h)
    k.circle(w * 0.86, h * 0.86, 20, lw=0.9, fill=Wt)
    for i in range(12):
        a = 2 * math.pi * i / 12; k.line([(w * 0.86 + 25 * math.cos(a), h * 0.86 + 25 * math.sin(a)), (w * 0.86 + 31 * math.cos(a), h * 0.86 + 31 * math.sin(a))], lw=0.8, amp=0)
    k.gull(w * 0.3, h * 0.9, 16); k.gull(w * 0.4, h * 0.94, 11)
    k.street(w, h, y=74)
    k.cottage_row(20, 76, 100, 170, i=0, label="CHEMIST")
    k.shopfront(124, 78, 230, 200)
    k.cottage_row(358, 84, 80, 160, i=3); k.cottage_row(440, 88, 70, 150, i=2)
    k.unclip()

def case_scene(k, w, h):
    """Tamsin dusting the glass case at the back of the shop; the telephone ringing on the counter at the front."""
    frame_open(k, w, h)
    interior(k, w, h, shelves=(30, 370))
    k.glass_case(250, 74, 150, 230, book=True)
    F.tamsin(k, 120, 64, 220, prop="duster")
    k.rect(420, 150, 80, 6, lw=0.8, fill=Wt)
    k.telephone(460, 156, 30, ringing=True)
    k.unclip()

def storm_scene(k, w, h):
    frame_open(k, w, h)
    k.storm_sky(14, h * 0.62, w - 14, h - 14)
    k.street(w, h, y=74, wet=True)
    for i in range(6): k.line([(20 + i * 80, 46), (70 + i * 80, 52)], lw=0.6, amp=0.8)   # water running down the street
    k.cottage_row(20, 76, 100, 170, i=0, label="CHEMIST")
    k.shopfront(124, 78, 230, 200)
    k.cottage_row(358, 84, 80, 160, i=3); k.cottage_row(440, 88, 70, 150, i=2)
    for gx in (170, 300, 410):   # overflowing gutters
        for j in range(4): k.line([(gx + j * 3, 262 - j * 2), (gx + j * 3 - 2, 230 - j * 3)], lw=0.6, amp=0.4)
    k.rain(14, 20, w - 14, h - 20, n=260, L=14, lw=0.55, seed=4)
    k.unclip()

def gone_scene(k, w, h, mark=True):
    frame_open(k, w, h)
    interior(k, w, h, shelves=(30, 370))
    k.glass_case(250, 74, 150, 230, book=False, open_=True)
    if mark: k.text(250, 316, "?", size=48, font="Ink-Playfair")
    k.unclip()

def hook_scene(k, w, h): gone_scene(k, w, h, mark=False)

def chemist_scene(k, w, h):
    """After the rain: Agnes comes over from the chemist's next door, Tamsin at the bookshop door."""
    frame_open(k, w, h)
    k.street(w, h, y=74, wet=True)
    k.cottage_row(20, 76, 120, 200, i=0, label="CHEMIST")
    k.shopfront(150, 78, 300, 260)
    for i in range(5): k.line([(170 + i * 50, 300), (166 + i * 50, 286)], lw=0.5, amp=0)   # last drips from the awning
    F.agnes(k, 110, 40, 200, teapot=False)
    F.tamsin(k, 390, 40, 200, prop=None)
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
            F.tamsin(k, cx + 150, 88, 210, prop=None)
            k.counter(cx + 50, pw - 24, 70, 74)
            k.rect(cx + 70, 151, 40, 26, lw=0.8, fill=K); k.rect(cx + 76, 160, 28, 10, lw=0.4, fill=Wt)   # till
            hedley_b(k, cx - 46, 70, fh)
            F.drips(k, cx - 46, 70, fh)
            nameplate(k, cx, 40, "HEDLEY TRUSCOTT")
        elif i == 1:
            k.street(pw, h, y=60, wet=True)
            k.shopfront(30, 62, 460, 250, awning=False)
            k.awning(20, 300, 245, depth=34, n=10)
            k.rain(304, 20, pw - 14, h - 20, n=70, L=13, lw=0.5, seed=8)
            k.rain(14, 20, 304, 120, n=50, L=12, lw=0.5, seed=9)
            F.pip(k, cx - 46, 70, fh)
            nameplate(k, cx, 40, "PIP CAREW")
        else:
            interior(k, pw, h, shelves=(250, 370), label="POETRY")
            F.wenna(k, cx - 46, 70, fh)
            nameplate(k, cx, 40, "WENNA POLGLAZE")
        k.unclip(); k.c.restoreState()

def bell_scene(k, w, h):
    """The shop door from inside: the little brass bell over it, wet street through the glass."""
    frame_open(k, w, h)
    for i in range(10): k.line([(14, 14 + i * 9), (w - 14, 14 + i * 9)], lw=0.3, amp=0.2)
    k.line([(14, 96), (w - 14, 96)], lw=1.0, amp=0.1)
    dx, dw, dh = 190, 132, 230
    k.rect(dx - 10, 96, dw + 20, dh + 10, lw=1.2, fill=Wt)
    k.rect(dx, 96, dw, dh, lw=1.0, fill=Wt)
    k.rect(dx + 14, 200, dw - 28, 110, lw=0.9, fill=Wt)
    k.rain(dx + 16, 204, dx + dw - 16, 306, n=40, L=10, lw=0.45, seed=2)
    k.rect(dx + 30, 230, dw - 60, 22, lw=0.8, fill=K); k.text(dx + dw / 2, 236, "OPEN", size=12, font="Ink-Plex", color=Wt)
    k.circle(dx + dw - 16, 180, 3, lw=0.6, fill=K)
    for j in range(3): k.rect(dx + 14, 110 + j * 28, dw - 28, 20, lw=0.6, fill=None)
    k.door_bell(dx + dw / 2, 330, 22, ringing=True)
    k.bookcase(30, 96, 110, 240, shelves=5, seed=5); k.bookcase(370, 96, 110, 240, shelves=5, seed=9)
    k.unclip()

def thinking_scene(k, w, h):
    """Agnes in the bookshop, looking things over; the shower has passed and the street outside is wet."""
    frame_open(k, w, h)
    interior(k, w, h, shelves=(30,))
    k.rect(190, 150, 290, 170, lw=1.2, fill=Wt)
    k.c.saveState(); k.clip_rect(192, 152, 478, 318)
    k.c.translate(190, 150); k.c.scale(290 / w, 170 / h)
    k.street(w, h, y=74, wet=True); k.cottage_row(40, 76, 140, 200, i=1); k.cottage_row(200, 80, 140, 200, i=4); k.cottage_row(360, 84, 140, 200, i=2)
    k.c.restoreState()
    k.line([(335, 150), (335, 320)], lw=1.0, amp=0); k.line([(190, 235), (480, 235)], lw=1.0, amp=0)
    k.rect(184, 142, 302, 8, lw=0.9, fill=Wt)
    F.agnes(k, 240, 50, 230, teapot=False)
    k.unclip()

def compare_scene(k, w, h):
    """Solution: Hedley, soaked after a short walk, beside Wenna, completely dry."""
    frame_open(k, w, h)
    for i in range(10): k.line([(14, 14 + i * 9), (w - 14, 14 + i * 9)], lw=0.3, amp=0.2)
    k.line([(14, 96), (w - 14, 96)], lw=1.0, amp=0.1)
    k.line([(w / 2, 20), (w / 2, h - 20)], lw=0.6, amp=0.4)
    k.storm_sky(14, h - 70, w / 2 - 4, h - 14)
    k.rain(20, 150, w / 2 - 10, h - 74, n=70, L=12, lw=0.5, seed=12)
    hedley_b(k, w * 0.25, 70, 200); F.drips(k, w * 0.25, 70, 200, n=12)
    F.wenna(k, w * 0.72, 70, 200, prop=False)
    nameplate(k, w * 0.25, 30, "HEDLEY: A SHORT WALK", size=11)
    nameplate(k, w * 0.72, 30, "WENNA: \u201cRAN FROM THE HARBOUR\u201d", size=11)
    k.text(w * 0.25, 272, "soaked", size=22, font="Ink-CrimsonI")
    k.text(w * 0.72, 272, "coat, hair, shoes: dry!", size=20, font="Ink-CrimsonI")
    k.unclip()

def returned_scene(k, w, h):
    """Tamsin gives Wenna an ordinary copy; the signed one is back in its case, locked."""
    frame_open(k, w, h)
    interior(k, w, h, shelves=(30, 380))
    k.glass_case(256, 74, 120, 200, book=True, lock=True)
    F.wenna(k, 120, 50, 220, expr="sheepish", scarf=True)
    F.tamsin(k, 400, 50, 220, prop="book", flip=True)
    k.unclip()

def cast_strip(k, w, h):
    """Three suspects side by side for the opening hook (same height, pose and ink weight)."""
    k.line([(0, 22), (w, 22)], lw=1.0, amp=0)
    for i in range(4): k.line([(0, 6 + i * 4), (w, 6 + i * 4)], lw=0.3, amp=0.2)
    k.rect(-4, h - 34, w + 8, 4, lw=0.9, fill=Wt); k.spines(4, w - 4, h - 30, 26, seed=3)   # one shelf of books along the top
    for i, fn in enumerate([hedley_b, F.pip, F.wenna]):
        fn(k, w * (0.17 + 0.32 * i), 20, h * 0.8)
    k.c.setStrokeColor(K); k.c.setLineWidth(1.3); k.c.rect(1, 1, w - 2, h - 2, stroke=1, fill=0)

def vignette(k, w, h):
    k.circle(w / 2, h / 2, w * 0.46, lw=1.3, fill=Wt); k.circle(w / 2, h / 2, w * 0.44, lw=0.45, fill=None)
    k.c.saveState(); p = k.c.beginPath(); p.circle(w / 2, h / 2, w * 0.44 - 1); k.c.clipPath(p, stroke=0, fill=0)
    k.storm_sky(0, h * 0.72, w, h)
    k.rain(0, h * 0.4, w, h * 0.72, n=60, L=12, lw=0.5, seed=1)
    k.rect(w * 0.1, h * 0.34, w * 0.8, 10, lw=0.9, fill=Wt)
    for j, (bw, bh) in enumerate(((150, 22), (130, 20), (140, 24))):
        y0 = h * 0.37 + sum(b[1] for b in ((150, 22), (130, 20), (140, 24))[:j])
        k.rect(w * 0.3 - bw / 2 + j * 6, y0, bw, bh, lw=0.9, fill=K if j == 1 else Wt)
        if j != 1: k.hatch([(w * 0.3 - bw / 2 + j * 6, y0), (w * 0.3 - bw / 2 + j * 6 + 12, y0), (w * 0.3 - bw / 2 + j * 6 + 12, y0 + bh), (w * 0.3 - bw / 2 + j * 6, y0 + bh)], angle=90, gap=1.4, lw=0.35)
    k.teapot(w * 0.7, h * 0.37, 80)
    k.c.restoreState()

AW, AH = 512, 384
SCENES = dict(street=(street_scene, AW, AH), case=(case_scene, AW, AH), storm=(storm_scene, AW, AH), gone=(gone_scene, AW, AH),
              hook=(hook_scene, AW, AH), chemist=(chemist_scene, AW, AH), lineup=(lineup, 3 * PW, AH), bell=(bell_scene, AW, AH),
              thinking=(thinking_scene, AW, AH), compare=(compare_scene, AW, AH), returned=(returned_scene, AW, AH),
              cast=(cast_strip, 600, 260), vignette=(vignette, 384, 384))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    want = [a for a in sys.argv[1:] if not a.startswith("--")] or list(SCENES)
    for i, name in enumerate(want):
        fn, pw, ph = SCENES[name]
        def draw(c, W, H, fn=fn, i=i):
            k = Shop(c, seed=31 + i); fn(k, W, H)
        render_color(os.path.join(OUT, name + ".png"), pw / 72, ph / 72, draw, seed=31 + i)
        print(name, flush=True)
