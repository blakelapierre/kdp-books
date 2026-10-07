"""bwkit: shared BLACK-AND-WHITE ink scenery + helpers for Cases 10-30 (Blake: B&W ink, simple v1 characters).

Built on art_case03.Shop (the Case 3 B&W kit: shopfronts, street, bookcases, rain, awning, counter...) and
figures.py (the simple v1 peg-doll characters, now with blink / talk FACE states for anim.py).
Everything is pure ink: tone comes from hatching, never from colour washes (colorink.set_style("bw")).

Conventions (same as the colour cases 4-9):
  * plate_open(): frame2 + clip — ONLY on still plates.
  * part_open():  clip only — every animated PART sprite (no border ever rotates / bobs with a sprite).
  * art pages are 512 x 384 pt (4:3); lineups are N x 512 wide; the hook cast strip is CW x CH.
"""
import math, os, random
import colorink
colorink.set_style("bw")
import art_case03 as A3
colorink.set_style("bw")
from inkart import lerp, K, Wt
from colorink import PAL, C, shade
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import figures as F
from art import nameplate

_fonts = os.environ.get("TIDEWHISTLE_FONTS", "/usr/share/fonts/truetype/sand-box/google/").rstrip("/") + "/"
try: pdfmetrics.registerFont(TTFont("Ink-Kalam", _fonts + "Kalam/Kalam-Bold.ttf"))
except Exception: pass

AW, AH = 512, 384
PW = 512
V3 = ["base", "base+blink", "base+talk"]; V2 = ["base", "base+blink"]

class InkBW(A3.Shop):
    # ------------------------------------------------------------------ sky / sea
    def sun(s, x, y, r=18, rays=12):
        s.circle(x, y, r, lw=0.9, fill=Wt)
        for i in range(rays):
            a = 2 * math.pi * i / rays
            s.line([(x + (r + 5) * math.cos(a), y + (r + 5) * math.sin(a)), (x + (r + 11) * math.cos(a), y + (r + 11) * math.sin(a))], lw=0.8, amp=0)

    def cloud(s, x, y, sc=1.0):
        pts = []
        for (dx, dy, r, a0, a1) in ((-22, 0, 10, 90, 270), (-10, 7, 12, 60, 200), (6, 10, 13, 20, 160), (22, 3, 10, -60, 120)):
            pts += s.arcpts(x + dx * sc, y + dy * sc, r * sc, r * sc, a0, a1, 10)
        pts += [(x + 30 * sc, y - 6 * sc), (x - 30 * sc, y - 6 * sc)]
        s.shape(pts, lw=0.7, fill=Wt, amp=0.2)

    def sea(s, x0, x1, y0, y1, rows=6, lw=0.45, seed=0):
        rr = random.Random(seed + int(x0) * 7 + int(y0))
        s.line([(x0, y1), (x1, y1)], lw=0.8, amp=0.2)
        for j in range(rows):
            y = lerp(y1 - 5, y0 + 4, (j + 0.5) / rows); n = 4 + j
            for _ in range(n):
                L = rr.uniform(8, 20) * (0.6 + 0.12 * j); x = rr.uniform(x0, x1 - L)
                s.line([(x + L * t, y + 1.0 * math.sin(t * math.pi * 2)) for t in [i / 8 for i in range(9)]], lw=lw, amp=0)

    def headland(s, x0, x1, y, hgt, hatch=True):
        pts = [(x0, y)] + [(lerp(x0, x1, t), y + hgt * (math.sin(t * math.pi) ** 0.7) * (0.85 + 0.15 * math.sin(t * 9))) for t in [i / 16 for i in range(17)]] + [(x1, y)]
        s.shape(pts, lw=0.8, fill=Wt, amp=0.3)
        if hatch: s.hatch(pts, angle=-30, gap=3.0, lw=0.3)

    def stones(s, x0, x1, y0, y1, rows=4, seed=1):
        """Harbour-wall masonry: staggered stone courses."""
        rr = random.Random(seed)
        s.rect(x0, y0, x1 - x0, y1 - y0, lw=1.0, fill=Wt)
        hh = (y1 - y0) / rows
        for j in range(rows):
            yy = y0 + j * hh
            if j: s.line([(x0, yy), (x1, yy)], lw=0.5, amp=0.2)
            x = x0 + (j % 2) * 9
            while x < x1 - 6:
                x += rr.uniform(16, 26)
                if x < x1 - 4: s.line([(x, yy), (x, yy + hh)], lw=0.45, amp=0.1)

    def harbour(s, w, h, sea_y0=110, sea_y1=180, lighthouse=True, boats=True, wall_top=110):
        """Harbour backdrop: headland + lighthouse, sea with wave strokes, little boats, a stone quay in front."""
        s.headland(14, 200, sea_y1 - 1, 36)
        if lighthouse: s.lighthouse(86, sea_y1 + 20, 58)
        s.headland(380, w - 14, sea_y1 - 1, 18)
        s.sea(14, w - 14, sea_y0, sea_y1)
        if boats:
            s.boat(250, sea_y0 + 22, 46); s.boat(400, sea_y0 + 34, 32, sail=False)
        s.stones(14, w - 14, 14, wall_top, rows=4)
        s.line([(14, wall_top), (w - 14, wall_top)], lw=1.2, amp=0.1)

    # ------------------------------------------------------------------ interiors
    def floorboards(s, w, y=96, n=9):
        for i in range(n): s.line([(14, 14 + i * (y - 14) / n), (w - 14, 14 + i * (y - 14) / n)], lw=0.3, amp=0.2)
        s.line([(14, y), (w - 14, y)], lw=1.0, amp=0.1)

    def window_view(s, x, y, w, h, view="harbour"):
        """A paned window looking out on the harbour (or 'street' / 'night')."""
        s.rect(x, y, w, h, lw=1.2, fill=Wt)
        s.clip_rect(x + 2, y + 2, x + w - 2, y + h - 2)
        if view == "harbour":
            s.sea(x, x + w, y + 4, y + h * 0.45, rows=3)
            s.headland(x + w * 0.45, x + w, y + h * 0.45, h * 0.18)
            s.gull(x + w * 0.3, y + h * 0.78, 12)
        elif view == "night":
            s.rect(x, y, w, h, lw=0, fill=K)
            s.circle(x + w * 0.7, y + h * 0.7, h * 0.1, lw=0, fill=Wt, stroke=False)
            for (a, b) in ((0.2, 0.8), (0.35, 0.6), (0.5, 0.85), (0.15, 0.5)): s.circle(x + w * a, y + h * b, 0.9, lw=0, fill=Wt, stroke=False)
        s.unclip()
        s.line([(x + w / 2, y), (x + w / 2, y + h)], lw=1.0, amp=0); s.line([(x, y + h / 2), (x + w, y + h / 2)], lw=1.0, amp=0)
        s.rect(x - 4, y - 6, w + 8, 6, lw=0.9, fill=Wt)

    def tearoom(s, w, h, window=True, counter=True, sign=True):
        """The Kettle and Gull tea room: floorboards, panelled dado, harbour window, shelf of cups, counter, teapot."""
        s.floorboards(w)
        s.rect(14, 96, w - 28, 34, lw=0.8, fill=Wt)
        for i in range(int((w - 28) / 32) + 1): s.rect(20 + i * 32, 101, 24, 24, lw=0.4, fill=None)
        if window: s.window_view(40, 196, 120, 110)
        if sign: s.text(100, 318, "THE KETTLE AND GULL", size=11, font="Ink-Plex")
        s.rect(300, 240, 180, 5, lw=0.7, fill=Wt)
        for i in range(6): s.cup(318 + i * 28, 245, 14)
        if counter:
            s.rect(296, 70, 190, 70, lw=1.0, fill=Wt)
            s.hatch([(296, 70), (486, 70), (486, 140), (296, 140)], angle=0, gap=2.6, lw=0.3)
            s.rect(290, 140, 202, 7, lw=0.9, fill=Wt)
            s.teapot(450, 147, 34)

    def table_cloth(s, x, y, w, h=40):
        """Small round tea table with a cloth (x, y = floor centre)."""
        s.rect(x - 3, y, 6, h, lw=0.8, fill=Wt)
        s.shape([(x - w / 2, y + h), (x + w / 2, y + h), (x + w / 2 + 4, y + h - 16), (x - w / 2 - 4, y + h - 16)], lw=0.9, fill=Wt, amp=0.1)
        s.shape(s.arcpts(x, y + h, w / 2, 5, 0, 360, 20), lw=0.9, fill=Wt, amp=0)

    def inn(s, w, h, sign="THE ANCHOR INN"):
        """Inn / pub: dark beams, wood panelling, bar with pumps, a dartboard."""
        s.floorboards(w)
        for x in range(14, w - 14, 22): s.line([(x, 96), (x, 150)], lw=0.4, amp=0)
        s.line([(14, 150), (w - 14, 150)], lw=0.9, amp=0)
        for y in (h - 40, h - 70):
            s.rect(14, y, w - 28, 10, lw=0.8, fill=K)
        s.rect(40, h - 110, 170, 22, lw=0.9, fill=K); s.text(125, h - 104, sign, size=11, font="Ink-Plex", color=Wt)
        s.circle(400, 230, 40, lw=1.2, fill=Wt); s.circle(400, 230, 30, lw=0.6, fill=None); s.circle(400, 230, 8, lw=0.6, fill=K)
        for i in range(10):
            a = i * math.pi / 5; s.line([(400 + 8 * math.cos(a), 230 + 8 * math.sin(a)), (400 + 40 * math.cos(a), 230 + 40 * math.sin(a))], lw=0.35, amp=0)

    def bar(s, x0, x1, y=14, hgt=80):
        s.rect(x0, y, x1 - x0, hgt, lw=1.0, fill=Wt)
        s.hatch([(x0, y), (x1, y), (x1, y + hgt), (x0, y + hgt)], angle=90, gap=3.0, lw=0.3)
        s.rect(x0 - 4, y + hgt, x1 - x0 + 8, 7, lw=1.0, fill=Wt)
        for px in (x0 + 30, x0 + 52):
            s.rect(px - 3, y + hgt + 7, 6, 26, lw=0.8, fill=Wt); s.circle(px, y + hgt + 36, 4, lw=0.7, fill=K)

    # ------------------------------------------------------------------ harbour props
    def lifeboat_station(s, x, y, w, hgt, steps=True):
        """Lifeboat station: big boathouse doors, pitched roof, LIFEBOAT sign, steps at the front."""
        s.wall(x, y, w, hgt * 0.7, gap=3.0)
        s.roof(x, x + w, y + hgt * 0.7, y + hgt, overhang=4)
        s.shape([(x + w * 0.2, y), (x + w * 0.8, y), (x + w * 0.8, y + hgt * 0.5)] + s.arcpts(x + w * 0.5, y + hgt * 0.5, w * 0.3, hgt * 0.12, 0, 180, 14)[1:] + [(x + w * 0.2, y + hgt * 0.5)], lw=1.0, fill=Wt, amp=0)
        s.line([(x + w * 0.5, y), (x + w * 0.5, y + hgt * 0.6)], lw=0.8, amp=0)
        for j in range(5): s.line([(x + w * 0.2, y + j * hgt * 0.1), (x + w * 0.8, y + j * hgt * 0.1)], lw=0.35, amp=0)
        s.rect(x + w * 0.18, y + hgt * 0.62, w * 0.64, hgt * 0.1, lw=0.9, fill=K)
        s.text(x + w / 2, y + hgt * 0.64, "LIFEBOAT", size=hgt * 0.065, font="Ink-Plex", color=Wt)
        if steps:
            for j in range(3): s.rect(x + w * 0.05 - j * 6, y - 8 * (j + 1), w * 0.9 + j * 12, 8, lw=0.8, fill=Wt)

    def collection_box(s, x, y, w):
        """Charity collection box shaped like a little model lifeboat on a stand; (x, y) = base centre."""
        s.rect(x - w * 0.18, y, w * 0.36, w * 0.25, lw=0.8, fill=Wt)
        hull = [(x - w / 2, y + w * 0.45), (x + w / 2, y + w * 0.45), (x + w * 0.38, y + w * 0.25), (x - w * 0.36, y + w * 0.25)]
        s.shape(hull, lw=1.0, fill=Wt, amp=0)
        s.hatch([(x - w * 0.36, y + w * 0.25), (x + w * 0.38, y + w * 0.25), (x + w * 0.44, y + w * 0.33), (x - w * 0.43, y + w * 0.33)], angle=0, gap=1.1, lw=0.35)
        s.rect(x - w * 0.18, y + w * 0.45, w * 0.36, w * 0.18, lw=0.8, fill=Wt)
        s.rect(x - w * 0.08, y + w * 0.6, w * 0.16, w * 0.03, lw=0.5, fill=K)   # coin slot
        s.line([(x + w * 0.05, y + w * 0.63), (x + w * 0.05, y + w * 0.85)], lw=0.8, amp=0)
        s.shape([(x + w * 0.05, y + w * 0.85), (x + w * 0.22, y + w * 0.79), (x + w * 0.05, y + w * 0.73)], lw=0.5, fill=K, amp=0)

    def dashed_outline(s, x, y, w, hgt):
        s.c.setStrokeColor(K); s.c.setLineWidth(0.7); s.c.setDash(3, 2.5)
        s.c.rect(x - w / 2, y, w, hgt, stroke=1, fill=0); s.c.setDash()

    def wet_bench(s, x, y, w, sign=True, wet=True):
        """Slatted harbour bench, freshly painted: glossy highlight dashes; optional WET PAINT sign."""
        for sx in (-0.42, 0.42):
            s.line([(x + sx * w, y), (x + sx * w, y + w * 0.2)], lw=1.4, amp=0)
        for j in range(3): s.rect(x - w / 2, y + w * (0.18 + 0.045 * j), w, w * 0.035, lw=0.8, fill=Wt)
        for j in range(3): s.rect(x - w / 2, y + w * (0.34 + 0.06 * j), w, w * 0.04, lw=0.8, fill=Wt)
        for sx in (-0.45, 0.45): s.line([(x + sx * w, y + w * 0.2), (x + sx * w, y + w * 0.5)], lw=1.2, amp=0)
        if wet:
            rr = random.Random(int(x))
            for j in range(9):
                gx = x + rr.uniform(-0.45, 0.4) * w; gy = y + w * rr.choice((0.2, 0.245, 0.36, 0.42, 0.48)) + w * 0.012
                s.line([(gx, gy), (gx + w * 0.05, gy)], lw=0.5, amp=0)
        if sign:
            px = x + w * 0.2
            s.line([(px, y + w * 0.3), (px, y + w * 0.62)], lw=1.0, amp=0)
            s.rect(px - w * 0.17, y + w * 0.6, w * 0.34, w * 0.16, lw=0.9, fill=Wt)
            s.text(px, y + w * 0.66, "WET PAINT", size=w * 0.07, font="Ink-Plex")

    def crate(s, x, y, w):
        s.rect(x - w / 2, y, w, w * 0.7, lw=0.9, fill=Wt)
        for j in range(1, 3): s.line([(x - w / 2, y + j * w * 0.233), (x + w / 2, y + j * w * 0.233)], lw=0.5, amp=0)
        s.line([(x - w / 2, y), (x + w / 2, y + w * 0.7)], lw=0.5, amp=0)

    def slipway(s, x0, x1, y0, y1):
        s.shape([(x0, y0), (x1, y0), (x1 - 40, y1), (x0 + 40, y1)], lw=0.9, fill=Wt, amp=0.1)
        for j in range(8): s.line([(lerp(x0, x0 + 40, j / 8), lerp(y0, y1, j / 8)), (lerp(x1, x1 - 40, j / 8), lerp(y0, y1, j / 8))], lw=0.35, amp=0)

    def car(s, x, y, w, boot_open=False):
        """Little old motor car side-on; (x, y) = ground centre."""
        hgt = w * 0.34
        body = [(x - w / 2, y + hgt * 0.25), (x + w / 2, y + hgt * 0.25), (x + w / 2, y + hgt * 0.6), (x + w * 0.25, y + hgt * 0.65), (x + w * 0.12, y + hgt), (x - w * 0.22, y + hgt), (x - w * 0.32, y + hgt * 0.65), (x - w / 2, y + hgt * 0.6)]
        s.shape(body, lw=1.0, fill=Wt, amp=0.1)
        s.shape([(x - w * 0.2, y + hgt * 0.68), (x - w * 0.03, y + hgt * 0.68), (x - w * 0.03, y + hgt * 0.94), (x - w * 0.18, y + hgt * 0.94)], lw=0.7, fill=Wt, amp=0)
        s.shape([(x + w * 0.01, y + hgt * 0.68), (x + w * 0.2, y + hgt * 0.68), (x + w * 0.1, y + hgt * 0.94), (x + w * 0.01, y + hgt * 0.94)], lw=0.7, fill=Wt, amp=0)
        for wx in (-0.3, 0.3):
            s.circle(x + wx * w, y + hgt * 0.22, hgt * 0.22, lw=1.0, fill=K); s.circle(x + wx * w, y + hgt * 0.22, hgt * 0.09, lw=0.4, fill=Wt)
        if boot_open:
            s.shape([(x - w / 2, y + hgt * 0.6), (x - w * 0.32, y + hgt * 0.65), (x - w * 0.6, y + hgt * 1.05), (x - w * 0.66, y + hgt * 0.98)], lw=0.9, fill=Wt, amp=0)

    def coins(s, x, y, n=6, r=3.2, seed=2):
        rr = random.Random(seed)
        for i in range(n):
            cx, cy = x + rr.uniform(-12, 12), y + rr.uniform(-4, 4)
            s.shape(s.arcpts(cx, cy, r, r * 0.55, 0, 360, 12), lw=0.6, fill=Wt, amp=0)

    def banknote(s, x, y, w):
        s.rect(x - w / 2, y, w, w * 0.5, lw=0.8, fill=Wt)
        s.rect(x - w / 2 + 3, y + 3, w - 6, w * 0.5 - 6, lw=0.4, fill=None)
        s.circle(x, y + w * 0.25, w * 0.12, lw=0.5, fill=None)

    # ------------------------------------------------------------------ boards / solution
    def case_board(s, x, y, w, hgt, title="AGNES'S CASE BOARD"):
        """Cork-style pin board in ink: thick frame, title card, drawing pins."""
        s.rect(x - 5, y - 5, w + 10, hgt + 10, lw=1.4, fill=Wt)
        s.rect(x, y, w, hgt, lw=0.8, fill=Wt)
        rr = random.Random(5)
        for _ in range(140):
            px, py = rr.uniform(x + 3, x + w - 3), rr.uniform(y + 3, y + hgt - 3)
            s.circle(px, py, 0.45, lw=0, fill=K, stroke=False)
        tw = s.c.stringWidth(title, "Ink-Plex", 12)
        s.rect(x + w / 2 - tw / 2 - 10, y + hgt - 30, tw + 20, 22, lw=0.9, fill=Wt)
        s.text(x + w / 2, y + hgt - 24, title, size=12, font="Ink-Plex")

    def pin_card(s, x, y, w, hgt, lines, size=10, font="Ink-Kalam", rot=0):
        s.c.saveState(); s.c.translate(x + w / 2, y + hgt / 2); s.c.rotate(rot); s.c.translate(-(x + w / 2), -(y + hgt / 2))
        s.rect(x, y, w, hgt, lw=0.8, fill=Wt)
        yy = y + hgt - size * 1.6
        for ln in lines:
            s.text(x + w / 2, yy, ln, size=size, font=font); yy -= size * 1.25
        s.circle(x + w / 2, y + hgt - 3, 2.6, lw=0.5, fill=K)
        s.c.restoreState()

    def clock_face(s, x, y, r, hh=None, mm=None):
        s.circle(x, y, r, lw=1.2, fill=Wt); s.circle(x, y, r * 0.9, lw=0.4, fill=None)
        for i in range(12):
            a = math.pi / 2 - i * math.pi / 6
            s.line([(x + r * 0.78 * math.cos(a), y + r * 0.78 * math.sin(a)), (x + r * 0.88 * math.cos(a), y + r * 0.88 * math.sin(a))], lw=0.8 if i % 3 == 0 else 0.4, amp=0)
        if hh is not None:
            ah = math.pi / 2 - (hh % 12 + (mm or 0) / 60) * math.pi / 6; am = math.pi / 2 - (mm or 0) * math.pi / 30
            s.line([(x, y), (x + r * 0.5 * math.cos(ah), y + r * 0.5 * math.sin(ah))], lw=1.6, amp=0)
            s.line([(x, y), (x + r * 0.75 * math.cos(am), y + r * 0.75 * math.sin(am))], lw=1.0, amp=0)
        s.circle(x, y, r * 0.06, lw=0, fill=K, stroke=False)

# ============================================================================= helpers
def plate_open(k, w, h):
    """Still plate: decorative double frame + clip. Plates never move."""
    k.frame2(w, h); k.clip_rect(14, 14, w - 14, h - 14)

def part_open(k, w, h):
    """Animated PART: clip only, no frame2 (a border baked into a sprite rotates with it — the Case 4 artifact)."""
    k.clip_rect(14, 14, w - 14, h - 14)

def full_open(k, w, h): k.clip_rect(0, 0, w, h)

def part(fn):
    """Decorator: wrap a figure-drawing fn(k, w, h, v) in part_open/unclip."""
    def wrapped(k, w, h, v, **kw):
        part_open(k, w, h); fn(k, w, h, v, **kw); k.unclip()
    return wrapped

# small fx pages (ink versions: black strokes on transparent)
def gull_fx(k, w, h, v):
    up = {"f0": 1.0, "f1": 0.45, "f2": -0.1, "f3": -0.5}[v]; x, y = w / 2, h / 2
    for sg in (-1, 1):
        tip = (x + sg * w * 0.46, y + up * h * 0.4); mid = (x + sg * w * 0.22, y + up * h * 0.25 + h * 0.18)
        k.line([(x + sg * 1.5, y), mid, tip], lw=1.0, amp=0)
    k.shape(k.arcpts(x, y - 0.6, 3.2, 1.6, 0, 360, 12), lw=0.5, fill=Wt, amp=0)

def steam_fx(k, w, h, v):
    ph = {"s0": 0, "s1": 1.6, "s2": 3.1}[v]
    pts = [(w / 2 + 2.6 * math.sin(t * 5 + ph), 2 + t * (h - 4)) for t in [i / 16 for i in range(17)]]
    k.line(pts, lw=0.6, amp=0)

def wave_fx(k, w, h, v):
    L = {"w0": 0.9, "w1": 0.7, "w2": 0.5}[v] * w; x0 = (w - L) / 2
    k.line([(x0 + L * t, h / 2 + 1.1 * math.sin(t * math.pi * 2 + 0.6)) for t in [i / 12 for i in range(13)]], lw=0.7, amp=0)

FX_GULL = dict(gull=dict(fn=gull_fx, variants=["f0", "f1", "f2", "f3"], page=(44, 22)))
FX_STEAM = dict(steam=dict(fn=steam_fx, variants=["s0", "s1", "s2"], page=(12, 22)))
FX_WAVE = dict(wave=dict(fn=wave_fx, variants=["w0", "w1", "w2"], page=(30, 8)))

# ------------------------------------------------------------------ new simple characters (Cases 10+)
SUIT = C(236, 228, 206)

def visitor(k, x, y, h, expr="neutral", flip=False, suit="plain", hat="panama", tie=True, prop=None, moustache=False):
    """Generic visiting gentleman in the v1 peg-doll construction: suit (plain / stripe / check / dark),
    optional hat (panama / bowler / cap / None), tie, moustache; prop in the carry hand (callable(k, hx, hy, h))."""
    f = F._flip(k, x, flip); g = F._geom(x, y, h); r, hy, sh, hem = g["r"], g["hy"], g["sh"], g["hem"]
    F._legs(k, x, y, h)
    if suit == "dark": body = F._body(k, x, y, h, PAL.navy, hatch_kw=dict(angle=45, gap=1.5, lw=0.35, cross=True))
    elif suit == "stripe": body = F._body(k, x, y, h, SUIT, hatch_kw=dict(angle=90, gap=3.6, lw=0.3))
    elif suit == "check": body = F._body(k, x, y, h, SUIT, hatch_kw=dict(angle=0, gap=4.0, lw=0.3, cross=True))
    else: body = F._body(k, x, y, h, SUIT)
    k.shape([(x - h * 0.05, sh), (x + h * 0.05, sh), (x + h * 0.02, sh - h * 0.2), (x - h * 0.02, sh - h * 0.2)], lw=0.6, fill=Wt, amp=0)
    if tie: k.shape([(x - h * 0.012, sh - h * 0.02), (x + h * 0.012, sh - h * 0.02), (x + h * 0.018, sh - h * 0.16), (x, sh - h * 0.19), (x - h * 0.018, sh - h * 0.16)], lw=0.4, fill=K, amp=0)
    for sg in (-1, 1): k.line([(x + sg * h * 0.05, sh), (x + sg * h * 0.025, sh - h * 0.2), (x + sg * h * 0.035, hem + h * 0.02)], lw=0.5, amp=0)
    k.rect(x + h * 0.07, sh - h * 0.3, h * 0.07, h * 0.012, lw=0.5, fill=Wt)
    hx, hyy = F._arms(k, x, y, h, hold=prop is not None)
    if prop: prop(k, hx, hyy, h)
    F._face(k, x, y, h, expr)
    if moustache: k.shape(k.arcpts(x, hy - r * 0.25, r * 0.38, r * 0.14, 180, 360, 10) + [(x + r * 0.38, hy - r * 0.2), (x - r * 0.38, hy - r * 0.2)], lw=0.4, fill=K, amp=0)
    if hat == "panama":
        k.shape(k.arcpts(x, hy + r * 0.6, r * 1.6, r * 0.32, 0, 360, 30), lw=0.8, fill=Wt, amp=0)
        k.shape([(x - r * 0.85, hy + r * 0.62), (x + r * 0.85, hy + r * 0.62), (x + r * 0.75, hy + r * 1.35), (x, hy + r * 1.2), (x - r * 0.75, hy + r * 1.35)], lw=0.8, fill=Wt, amp=0)
        k.shape([(x - r * 0.85, hy + r * 0.62), (x + r * 0.85, hy + r * 0.62), (x + r * 0.83, hy + r * 0.82), (x - r * 0.83, hy + r * 0.82)], lw=0.5, fill=K, amp=0)
    elif hat == "bowler":
        k.shape(k.arcpts(x, hy + r * 0.62, r * 1.35, r * 0.22, 0, 360, 24), lw=0.7, fill=K, amp=0)
        k.shape(k.arcpts(x, hy + r * 0.66, r * 0.88, r * 0.9, 0, 180, 18), lw=0.7, fill=K, amp=0)
    elif hat == "cap":
        k.shape(k.arcpts(x, hy + r * 0.25, r * 1.02, r * 0.9, 0, 180, 20), lw=0.8, fill=Wt, amp=0)
        k.shape([(x + r * 0.2, hy + r * 0.35), (x + r * 1.7, hy + r * 0.3), (x + r * 1.6, hy + r * 0.5), (x + r * 0.3, hy + r * 0.62)], lw=0.6, fill=Wt, amp=0)
        k.hatch(k.arcpts(x, hy + r * 0.25, r * 1.02, r * 0.9, 0, 180, 20), angle=45, gap=2.4, lw=0.3, cross=True)
    else:
        k.shape(k.arcpts(x, hy + r * 0.1, r * 1.05, r * 1.0, 10, 170, 16) + [(x - r * 0.9, hy + r * 0.5), (x + r * 0.9, hy + r * 0.5)], lw=0.6, fill=K, amp=0)
    F._unflip(k, f)

def lady(k, x, y, h, expr="neutral", flip=False, dress="dots", hair="bun", hat=None, prop=None, shawl=False):
    """Generic lady in the v1 construction: dress (dots / stripe / plain / dark), hair (bun / bob / long / curls), optional hat."""
    f = F._flip(k, x, flip); g = F._geom(x, y, h); r, hy, sh, hem = g["r"], g["hy"], g["sh"], g["hem"]
    if hair == "long": k.shape([(x - r * 0.95, hy + r * 0.3), (x - r * 1.25, hy - r * 1.6), (x + r * 1.25, hy - r * 1.6), (x + r * 0.95, hy + r * 0.3)], lw=0.8, fill=K, amp=0.2)
    F._legs(k, x, y, h)
    if dress == "stripe": body = F._body(k, x, y, h, PAL.cloud, hatch_kw=dict(angle=90, gap=3.0, lw=0.5))
    elif dress == "dark": body = F._body(k, x, y, h, PAL.navy, hatch_kw=dict(angle=-45, gap=1.5, lw=0.35, cross=True))
    elif dress == "plain": body = F._body(k, x, y, h, PAL.cloud)
    else:
        body = F._body(k, x, y, h, PAL.cloud)
        rr = random.Random(int(h))
        for i in range(16):
            u, v = rr.uniform(0.1, 0.9), rr.uniform(0.08, 0.85); half = (h * 0.13) + (h * 0.08) * (1 - v)
            k.circle(x + (u - 0.5) * 2 * half * 0.85, hem + v * (sh - hem), h * 0.008, lw=0, fill=K, stroke=False)
    if shawl:
        k.shape([(x - h * 0.15, sh + 1), (x + h * 0.15, sh + 1), (x + h * 0.12, sh - h * 0.12), (x, sh - h * 0.18), (x - h * 0.12, sh - h * 0.12)], lw=0.7, fill=Wt, amp=0.1)
        k.hatch([(x - h * 0.15, sh + 1), (x + h * 0.15, sh + 1), (x + h * 0.12, sh - h * 0.12), (x, sh - h * 0.18), (x - h * 0.12, sh - h * 0.12)], angle=45, gap=2.0, lw=0.3, cross=True)
    hx, hyy = F._arms(k, x, y, h, hold=prop is not None)
    if prop: prop(k, hx, hyy, h)
    F._face(k, x, y, h, expr)
    if hair == "bun":
        k.shape(k.arcpts(x, hy + r * 0.05, r * 1.04, r * 1.02, 15, 165, 20) + [(x - r * 0.6, hy + r * 0.55), (x + r * 0.6, hy + r * 0.55)], lw=0.6, fill=K, amp=0)
        k.circle(x, hy + r * 1.25, r * 0.42, lw=0.6, fill=K)
    elif hair == "bob":
        k.shape(k.arcpts(x, hy + r * 0.1, r * 1.12, r * 1.05, 0, 180, 20) + [(x - r * 1.12, hy - r * 0.55), (x - r * 0.82, hy - r * 0.55), (x - r * 0.82, hy + r * 0.55), (x + r * 0.82, hy + r * 0.55), (x + r * 0.82, hy - r * 0.55), (x + r * 1.12, hy - r * 0.55)], lw=0.7, fill=Wt, amp=0)
        k.hatch(k.arcpts(x, hy + r * 0.1, r * 1.12, r * 1.05, 0, 180, 20), angle=70, gap=1.8, lw=0.35)
    elif hair == "curls":
        for i in range(9):
            a = math.radians(15 + i * 18.75)
            k.circle(x + r * 0.92 * math.cos(a), hy + r * 0.25 + r * 0.82 * math.sin(a), r * 0.3, lw=0.55, fill=Wt)
    else:
        k.shape(k.arcpts(x, hy + r * 0.1, r * 1.05, r * 1.0, 10, 170, 16) + [(x - r * 0.9, hy + r * 0.5), (x + r * 0.9, hy + r * 0.5)], lw=0.6, fill=K, amp=0)
    if hat == "sun":
        k.shape(k.arcpts(x, hy + r * 0.6, r * 2.0, r * 0.4, 0, 360, 30), lw=0.8, fill=Wt, amp=0)
        k.shape(k.arcpts(x, hy + r * 0.7, r * 0.9, r * 0.8, 0, 180, 20), lw=0.8, fill=Wt, amp=0)
        k.shape([(x - r * 0.9, hy + r * 0.7), (x + r * 0.9, hy + r * 0.7), (x + r * 0.88, hy + r * 0.95), (x - r * 0.88, hy + r * 0.95)], lw=0.5, fill=K, amp=0)
    elif hat == "bonnet":
        k.shape(k.arcpts(x, hy + r * 0.2, r * 1.35, r * 1.3, -20, 200, 24), lw=0.8, fill=Wt, amp=0)
        k.hatch(k.arcpts(x, hy + r * 0.2, r * 1.35, r * 1.3, -20, 200, 24), angle=0, gap=2.2, lw=0.3)
        F._face(k, x, y, h, expr)
    F._unflip(k, f)

def overalls(k, x, y, h, expr="neutral", flip=False, paint=False, cap=True, prop=None):
    """Hedley in work overalls (bib + straps), flat cap; paint=True adds smears on the hands and knees."""
    f = F._flip(k, x, flip); g = F._geom(x, y, h); r, hy, sh, hem = g["r"], g["hy"], g["sh"], g["hem"]
    F._legs(k, x, y, h)
    for sg in (-1, 1):
        leg = [(x + sg * h * 0.01, hem + h * 0.1), (x + sg * h * 0.13, hem + h * 0.1), (x + sg * h * 0.12, y + h * 0.03), (x + sg * h * 0.02, y + h * 0.03)]
        k.shape(leg, lw=0.8, fill=Wt, amp=0)
        if paint:   # paint-smeared knees: a small cross-hatched patch on each trouser leg
            kp = [(x + sg * h * 0.035, y + h * 0.07), (x + sg * h * 0.115, y + h * 0.07), (x + sg * h * 0.115, y + h * 0.13), (x + sg * h * 0.035, y + h * 0.13)]
            k.hatch(kp, angle=45, gap=1.1, lw=0.45, cross=True)
    body = [(x - h * 0.13, sh), (x + h * 0.13, sh), (x + h * 0.15, hem + h * 0.12), (x - h * 0.15, hem + h * 0.12)]
    k.shape(body, lw=1.0, fill=Wt, amp=0.15)
    k.hatch(body, angle=45, gap=3.0, lw=0.3)
    k.rect(x - h * 0.07, sh - h * 0.2, h * 0.14, h * 0.12, lw=0.7, fill=Wt)
    for sg in (-1, 1): k.line([(x + sg * h * 0.06, sh - h * 0.08), (x + sg * h * 0.1, sh)], lw=0.9, amp=0)
    hx, hyy = F._arms(k, x, y, h, hold=prop is not None)
    if prop: prop(k, hx, hyy, h)
    if paint:   # paint on both hands (hand positions as figures._arms draws them)
        rh = (hx + h * 0.012, hyy) if prop is not None else (x + h * 0.2, sh - h * 0.31)
        for (px, py) in ((x - h * 0.2, sh - h * 0.31), rh):
            k.circle(px, py, h * 0.024, lw=0.4, fill=K)
    F._face(k, x, y, h, expr)
    if cap:
        k.shape(k.arcpts(x, hy + r * 0.25, r * 1.02, r * 0.9, 0, 180, 20), lw=0.8, fill=Wt, amp=0)
        k.shape([(x + r * 0.2, hy + r * 0.35), (x + r * 1.7, hy + r * 0.3), (x + r * 1.6, hy + r * 0.5), (x + r * 0.3, hy + r * 0.62)], lw=0.6, fill=Wt, amp=0)
        k.hatch(k.arcpts(x, hy + r * 0.25, r * 1.02, r * 0.9, 0, 180, 20), angle=45, gap=2.4, lw=0.3, cross=True)
    F._unflip(k, f)

def paintbrush(k, hx, hyy, h):
    k.line([(hx, hyy), (hx + h * 0.06, hyy + h * 0.1)], lw=1.2, amp=0)
    k.shape([(hx + h * 0.05, hyy + h * 0.1), (hx + h * 0.08, hyy + h * 0.09), (hx + h * 0.1, hyy + h * 0.15), (hx + h * 0.07, hyy + h * 0.16)], lw=0.6, fill=K, amp=0)

def teacup_prop(k, hx, hyy, h): k.cup(hx + h * 0.03, hyy - h * 0.01, h * 0.07)

def newspaper(k, hx, hyy, h):
    k.rect(hx - h * 0.02, hyy - h * 0.06, h * 0.08, h * 0.13, lw=0.7, fill=Wt)
    for j in range(4): k.line([(hx - h * 0.01, hyy + h * (0.04 - 0.025 * j)), (hx + h * 0.05, hyy + h * (0.04 - 0.025 * j))], lw=0.35, amp=0)

# ------------------------------------------------------------------ lineup / cast builders
# (functools.partial of module-level functions, so save_layers can pickle them into its process pool)
from functools import partial as _partial

def _lineup_plate(k, w, h, backdrops=(), names=()):
    for i, (bd, nm) in enumerate(zip(backdrops, names)):
        k.c.saveState(); k.c.translate(i * PW, 0)
        k.frame2(PW, h); k.clip_rect(14, 14, PW - 14, h - 14)
        bd(k, PW, h); nameplate(k, PW / 2, 40, nm)
        k.unclip(); k.c.restoreState()

def lineup_plate_fn(backdrops, names):
    """Plate for an N-panel lineup: each panel gets its own backdrop fn(k, pw, h) and a nameplate."""
    return _partial(_lineup_plate, backdrops=tuple(backdrops), names=tuple(names))

def _lineup_fig(k, w, h, v, i=0, drawer=None, x=PW / 2 - 46, y=70, fh=236):
    k.c.saveState(); k.c.translate(i * PW, 0); k.clip_rect(14, 14, PW - 14, h - 14)
    drawer(k, x, y, fh); k.unclip(); k.c.restoreState()

def lineup_fig_fn(i, drawer, x=PW / 2 - 46, y=70, fh=236):
    return _partial(_lineup_fig, i=i, drawer=drawer, x=x, y=y, fh=fh)

CW, CH = 900, 420
def _cast_plate(k, w, h, names=(), style="cards"):
    n = len(names)
    for i, nm in enumerate(names):
        x0 = i * w / n; x1 = x0 + w / n
        if style == "tags":
            k.shape([(x0 + 14, 14), (x1 - 14, 14), (x1 - 14, h - 50), (x0 + w / n / 2, h - 14), (x0 + 14, h - 50)], lw=1.4, fill=Wt, amp=0)
            k.circle(x0 + w / n / 2, h - 40, 7, lw=1.0, fill=Wt)
        elif style == "frames":
            k.rect(x0 + 12, 12, w / n - 24, h - 24, lw=2.0, fill=Wt); k.rect(x0 + 20, 20, w / n - 40, h - 40, lw=0.6, fill=None)
        else:
            k.rect(x0 + 12, 12, w / n - 24, h - 24, lw=1.4, fill=Wt)
        k.line([(x0 + 24, 62), (x1 - 24, 62)], lw=0.6, amp=0.1)
        nameplate(k, x0 + w / n / 2, 28, nm, size=12)

def cast_plate_fn(names, style="cards"):
    """Hook cast strip: N equal cards, a nameplate on each. style: 'cards' | 'tags' (luggage tags) | 'frames'."""
    return _partial(_cast_plate, names=tuple(names), style=style)

def _cast_fig(k, w, h, v, i=0, n=3, drawer=None):
    x0 = i * w / n
    k.clip_rect(x0 + 16, 16, x0 + w / n - 16, h - 16)
    drawer(k, x0 + w / n / 2, 64, h * 0.68); k.unclip()

def cast_fig_fn(i, n, drawer): return _partial(_cast_fig, i=i, n=n, drawer=drawer)

def _vignette(k, w, h, inside=None):
    k.circle(w / 2, h / 2, w * 0.46, lw=1.4, fill=Wt); k.circle(w / 2, h / 2, w * 0.44, lw=0.5, fill=None)
    k.c.saveState(); p = k.c.beginPath(); p.circle(w / 2, h / 2, w * 0.44 - 1); k.c.clipPath(p, stroke=0, fill=0)
    inside(k, w, h); k.c.restoreState()

def vignette_fn(draw_inside): return _partial(_vignette, inside=draw_inside)

def make_ink(c, seed): return InkBW(c, seed=seed)
