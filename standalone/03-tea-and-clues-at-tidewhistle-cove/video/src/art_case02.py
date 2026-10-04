"""Colour illustrations for Case 2, The Lemonade on the Lawn (same house style as art.py / colorink.py,
simple coloured characters from figures.py). Output: ../work/art-02/*.png      Run: python3 art_case02.py [scene ...]"""
import math, os, sys
from inkart import lerp, K, Wt
from colorink import PAL, C, render_color, shade, mix
import figures as F
from art import Sea, nameplate, sky

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-02")
LAWN = C(178, 210, 140); LAWN2 = C(156, 196, 122); PATH = C(236, 220, 186); ROSE = C(226, 108, 120); ROSE2 = C(244, 170, 176)
KITCHEN = C(240, 232, 206); TILE = C(206, 228, 222); FREEZER = C(236, 240, 240); CANVAS = [C(232, 128, 118), C(252, 244, 232)]
HOT = C(252, 214, 120); HOT2 = C(250, 236, 196); VELVET = C(138, 70, 96)

class Garden(Sea):
    def sun_big(s, x, y, r):
        s.circle(x, y, r * 1.5, lw=0, fill=mix(PAL.sun, PAL.sky2, 0.6), stroke=False)
        s.circle(x, y, r, lw=0.9, fill=PAL.sun)
        for i in range(16):
            a = 2 * math.pi * i / 16; L = 1.3 if i % 2 else 1.55
            s.line([(x + r * 1.15 * math.cos(a), y + r * 1.15 * math.sin(a)), (x + r * L * math.cos(a), y + r * L * math.sin(a))], lw=1.1, amp=0, color=shade(PAL.sun, 0.78))

    def lawn(s, x0, x1, y, depth):
        s.vgrad(x0, y - depth, x1, y, LAWN, LAWN2, steps=8)
        for i in range(60):
            gx = s.r.uniform(x0, x1); gy = y - s.r.uniform(2, depth * 0.95)
            for d in (-1, 0, 1): s.line([(gx, gy), (gx + d * 1.3, gy + 3)], lw=0.4, amp=0, color=shade(LAWN, 0.7))
        s.line([(x0, y), (x1, y)], lw=0.8, amp=0.3)

    def picket(s, x0, x1, y, h=26):
        with s.tint(PAL.cloud):
            s.rect(x0, y + h * 0.3, x1 - x0, 3, lw=0.6); s.rect(x0, y + h * 0.7, x1 - x0, 3, lw=0.6)
            x = x0
            while x < x1 - 4:
                s.shape([(x, y), (x + 6, y), (x + 6, y + h), (x + 3, y + h + 4), (x, y + h)], lw=0.6, fill=Wt, amp=0); x += 11

    def rosebush(s, x, y, w):
        with s.tint(PAL.leaf):
            s.shape(s.arcpts(x, y, w / 2, w * 0.42, 0, 180, 18) + [(x - w / 2, y)], lw=0.8, fill=Wt, amp=0.5)
        for i in range(9):
            rx = x + s.r.uniform(-0.38, 0.38) * w; ry = y + s.r.uniform(0.08, 0.36) * w
            s.circle(rx, ry, w * 0.06, lw=0.5, fill=ROSE if i % 3 else ROSE2)
            s.c.setStrokeColor(shade(ROSE, 0.6)); s.c.setLineWidth(0.3); s.c.circle(rx, ry, w * 0.03, stroke=1, fill=0)

    def deckchair(s, x, y, w):
        """Striped deckchair (front 3/4), seat at about y + 0.32 w."""
        wood = shade(PAL.wood_dk, 0.9)
        s.line([(x - w * 0.42, y), (x - w * 0.3, y + w * 0.95)], lw=1.6, amp=0, color=wood)
        s.line([(x + w * 0.42, y), (x + w * 0.3, y + w * 0.95)], lw=1.6, amp=0, color=wood)
        s.line([(x - w * 0.45, y + w * 0.32), (x + w * 0.62, y)], lw=1.4, amp=0, color=wood)
        s.line([(x + w * 0.45, y + w * 0.32), (x - w * 0.55, y)], lw=1.4, amp=0, color=wood)
        cv = [(x - w * 0.32, y + w * 0.92), (x + w * 0.32, y + w * 0.92), (x + w * 0.4, y + w * 0.3), (x - w * 0.4, y + w * 0.3)]
        s.shape(cv, lw=0.9, fill=CANVAS[1], amp=0)
        for i in range(5):
            if i % 2 == 0:
                u0, u1 = i / 5, (i + 1) / 5
                s.shape([(lerp(cv[3][0], cv[2][0], u0), cv[3][1]), (lerp(cv[3][0], cv[2][0], u1), cv[3][1]), (lerp(cv[0][0], cv[1][0], u1), cv[0][1]), (lerp(cv[0][0], cv[1][0], u0), cv[0][1])], lw=0.4, fill=CANVAS[0], amp=0)
        s.shape(cv, lw=0.9, fill=None, amp=0)

    def bench(s, x, y, w, seat=68):
        """Garden bench w wide standing on y, seat top at y + seat, slatted back above it."""
        wd, dk = PAL.wood, shade(PAL.wood_dk, 0.9)
        for u in (-0.45, 0.45):
            s.line([(x + u * w, y), (x + u * w, y + seat)], lw=2.4, amp=0, color=dk)
            s.line([(x + u * w, y + seat), (x + u * w, y + seat + 70)], lw=2.2, amp=0, color=dk)
        for j in range(3): s.rect(x - w / 2, y + seat + 24 + 15 * j, w, 9, lw=0.7, fill=wd)
        s.rect(x - w / 2 - 3, y + seat - 8, w + 6, 9, lw=0.8, fill=wd)

    def garden_table(s, x0, x1, y, h=50):
        dk = shade(PAL.wood_dk, 0.9)
        for u in (0.12, 0.88): s.line([(lerp(x0, x1, u), y - h), (lerp(x0, x1, u), y)], lw=2.2, amp=0, color=dk)
        with s.tint(PAL.cloud): s._table(x0, x1, y, depth=8, skirt=16)
        s.c.setStrokeColor(PAL.sea2); s.c.setLineWidth(0.6)
        for i in range(int((x1 - x0) / 10)): s.c.line(x0 + 4 + i * 10, y - 15, x0 + 4 + i * 10, y - 1)

    def ice_bowl(s, x, y, w, full=True):
        s.shape(s.arcpts(x, y + w * 0.2, w / 2, w * 0.36, 180, 360, 20), lw=0.9, fill=PAL.teal_lt, amp=0)
        s.shape(s.arcpts(x, y + w * 0.2, w / 2, w * 0.1, 0, 360, 24), lw=0.8, fill=PAL.foam if full else shade(PAL.teal_lt, 0.9), amp=0)
        if full:
            for i in range(6):
                cx = x + (i - 2.5) * w * 0.13; cy = y + w * 0.25 + (i % 2) * w * 0.05
                s.rect(cx - w * 0.06, cy - w * 0.04, w * 0.12, w * 0.1, lw=0.6, fill=PAL.foam)
        else:
            s.c.setFillColor(shade(PAL.glass, 0.95)); s.c.ellipse(x - w * 0.2, y + w * 0.17, x + w * 0.16, y + w * 0.23, stroke=0, fill=1)

    def cottage_big(s, x, y, w, h):
        s.wall(x, y, w, h * 0.62, gap=3.0, color=PAL.walls[4])
        s.roof(x, x + w, y + h * 0.62, y + h, overhang=6, color=PAL.slate)
        s.chimney(x + w * 0.76, y + h * 0.8, w * 0.07, h * 0.28)
        for u in (0.1, 0.68): s.window(x + w * u, y + h * 0.28, w * 0.2, h * 0.2)
        s.shape([(x + w * 0.42, y), (x + w * 0.58, y), (x + w * 0.58, y + h * 0.44), (x + w * 0.42, y + h * 0.44)], lw=0.8, fill=PAL.doors[3], amp=0)
        s.circle(x + w * 0.55, y + h * 0.22, 1.5, lw=0.4, fill=PAL.brass)
        for u in (0.05, 0.92): s.rosebush(x + w * u, y, w * 0.14)

    def locket(s, x, y, r, chain=True):
        if chain:
            s.c.setStrokeColor(shade(PAL.silver, 0.75)); s.c.setLineWidth(0.6)
            p = s.c.beginPath(); p.moveTo(x - r * 2.2, y - r * 0.6); p.curveTo(x - r * 1.4, y + r * 1.8, x + r * 1.2, y + r * 2.0, x + r * 2.4, y - r * 0.4); s.c.drawPath(p, stroke=1, fill=0)
        s.circle(x, y, r, lw=0.8, fill=PAL.silver)
        s.circle(x, y, r * 0.62, lw=0.4, fill=None)
        s.circle(x, y + r * 1.08, r * 0.18, lw=0.4, fill=PAL.silver)

    def jewel_box(s, x, y, w, empty=False):
        h = w * 0.4
        s.shape([(x - w / 2, y + h), (x + w / 2, y + h), (x + w * 0.44, y + h + w * 0.42), (x - w * 0.44, y + h + w * 0.42)], lw=0.8, fill=VELVET, amp=0)  # open lid
        s.shape([(x - w * 0.38, y + h + 2), (x + w * 0.38, y + h + 2), (x + w * 0.34, y + h + w * 0.36), (x - w * 0.34, y + h + w * 0.36)], lw=0.4, fill=C(236, 214, 222), amp=0)
        s.rect(x - w / 2, y, w, h, lw=0.9, fill=VELVET)
        s.shape(s.arcpts(x, y + h, w * 0.4, w * 0.08, 0, 360, 20), lw=0.5, fill=C(236, 214, 222), amp=0)
        if empty: s.shape(s.arcpts(x, y + h, w * 0.14, w * 0.04, 0, 360, 16), lw=0.4, fill=shade(C(236, 214, 222), 0.85), amp=0)

    def freezer(s, x, y, w, h, open_=False):
        """Tall fridge-freezer; freezer on top."""
        s.rect(x, y, w, h, lw=1.0, fill=FREEZER)
        s.line([(x, y + h * 0.62), (x + w, y + h * 0.62)], lw=0.9, amp=0)
        for (y0, y1) in ((y + h * 0.66, y + h * 0.9), (y + h * 0.1, y + h * 0.5)):
            s.line([(x + w * 0.85, y0), (x + w * 0.85, y1)], lw=1.8, amp=0, color=PAL.slate)
        s.rect(x + w * 0.12, y + h * 0.8, w * 0.36, h * 0.08, lw=0.5, fill=PAL.card)
        s.text(x + w * 0.3, y + h * 0.82, "ICE", size=h * 0.05, font="Ink-Plex")

    def window_view(s, x, y, w, h):
        """Kitchen window looking out on the hot garden, with a sill along the bottom."""
        s.rect(x, y, w, h, lw=1.0, fill=PAL.sky)
        s.wash_rect(x + 1, y + 1, x + w - 1, y + h * 0.4, LAWN)
        s.circle(x + w * 0.78, y + h * 0.78, h * 0.1, lw=0.6, fill=PAL.sun)
        s.c.setStrokeColor(K); s.c.setLineWidth(1.1); s.c.line(x + w / 2, y, x + w / 2, y + h); s.c.line(x, y + h * 0.5, x + w, y + h * 0.5)
        s.rect(x - 12, y - 10, w + 24, 10, lw=1.0, fill=PAL.wood)
        for sg in (-1, 1):
            cx0 = x if sg < 0 else x + w
            s.shape([(cx0, y + h + 4), (cx0 - sg * 26, y + h + 4), (cx0 - sg * 14, y + h * 0.45), (cx0 - sg * 4, y + h * 0.2), (cx0, y + h * 0.2)], lw=0.7, fill=C(244, 220, 120), amp=0.2)
        s.rect(x - 16, y + h + 2, w + 32, 4, lw=0.6, fill=PAL.wood_dk)

    def harbour_office(s, x, y, w, h):
        s.wall(x, y, w, h * 0.66, gap=3.0, color=PAL.walls[2])
        s.roof(x, x + w, y + h * 0.66, y + h, overhang=5, color=PAL.roof)
        s.rect(x + w * 0.1, y + h * 0.5, w * 0.8, h * 0.12, lw=0.8, fill=PAL.card)
        s.text(x + w / 2, y + h * 0.525, "HARBOUR OFFICE", size=h * 0.06, font="Ink-Plex")
        s.shape([(x + w * 0.38, y), (x + w * 0.62, y), (x + w * 0.62, y + h * 0.42), (x + w * 0.38, y + h * 0.42)], lw=0.8, fill=PAL.navy_lt, amp=0)
        for u in (0.08, 0.72): s.window(x + w * u, y + h * 0.18, w * 0.2, h * 0.2)

def frame_open(k, w, h):
    k.frame2(w, h); k.clip_rect(14, 14, w - 14, h - 14)

# ============================================================================= scenes (4:3, 512 x 384)
def hillparty(k, w, h):
    frame_open(k, w, h)
    k.vgrad(14, 120, w - 14, h - 14, HOT, HOT2, steps=20)      # heat-hazy sky
    k.vgrad(14, 110, w - 14, 150, PAL.sea, PAL.sea2, steps=6)  # sea below the hill
    k.sun_big(w * 0.8, h * 0.8, 30)
    for i in range(3): k.gull(60 + i * 40, h * 0.86 + (i % 2) * 6, 12)   # the gulls sit still on the wall, so only two fly
    hill = [(14, 14), (14, 150), (w * 0.3, 196), (w * 0.62, 214), (w * 0.9, 188), (w - 14, 170), (w - 14, 14)]
    k.shape(hill, lw=0.9, fill=LAWN, amp=0.6)
    with k.tint(LAWN): k.hatch(hill, angle=0, gap=5, lw=0.3)
    k.cottage_big(w * 0.36, 196, 150, 110)
    k.picket(30, w * 0.34, 176, 18); k.picket(w * 0.68, w - 30, 170, 18)
    k.bunting(w * 0.2, w * 0.36, 280, sag=6, n=6, size=6); k.bunting(w * 0.65, w * 0.86, 278, sag=6, n=7, size=6)
    k.garden_table(w * 0.12, w * 0.32, 120, 30)
    F.jug(k, w * 0.2, 121, 26)
    cols = [PAL.walls[0], PAL.walls[2], PAL.walls[1], PAL.walls[3], PAL.walls[5], PAL.pea_purple]
    for i, (gx, gy) in enumerate([(w * 0.08, 60), (w * 0.4, 70), (w * 0.52, 58), (w * 0.66, 72), (w * 0.8, 60), (w * 0.92, 74)]):
        F.guest(k, gx, gy, 70, cols[i], hat=PAL.straw if i % 2 else None, hair=PAL.hair_dark if i % 2 == 0 else None)
    k.unclip()

def lawn_scene(k, w, h):
    frame_open(k, w, h)
    k.vgrad(14, 150, w - 14, h - 14, HOT, HOT2, steps=16)
    k.sun_big(w * 0.86, h * 0.84, 24)
    k.lawn(14, w - 14, 150, 136)
    k.cottage_big(w * 0.55, 150, 190, 150)
    k.bunting(14, w - 14, h - 34, sag=14, n=20, size=7)
    k.garden_table(30, 220, 110, 70)
    k.ice_bowl(80, 112, 60, full=True)
    for i in range(4): F.lemonade_glass(k, 140 + i * 18, 112, 26, ice="fresh")
    F.loveday(k, 300, 34, 210)
    F.guest(k, 430, 60, 120, PAL.walls[2], hat=PAL.straw)
    k.unclip()

def kitchen(k, w, h, locket=True, hook=False):
    frame_open(k, w, h)
    k.wash_rect(14, 14, w - 14, h - 14, KITCHEN)
    k.wash_rect(14, 14, w - 14, 40, C(214, 186, 150))
    for i in range(12):   # tiled splashback
        for j in range(4): k.rect(20 + i * 40, 140 + j * 16, 40, 16, lw=0.3, fill=TILE)
    k.window_view(150, 230 if not hook else 210, 200, 110)
    sill_y = 222 if not hook else 202
    k.rect(14, 104, w - 28, 34, lw=0.9, fill=PAL.wood)            # worktop
    with k.tint(C(214, 196, 168)): k.rect(14, 14, w - 28, 90, lw=0.9)
    for u in (0.08, 0.36, 0.64): k.rect(w * u, 24, w * 0.24, 70, lw=0.6, fill=C(222, 206, 178))
    k.freezer(w - 140, 14, 110, 300)
    with k.tint(PAL.copper): k.kettle(70, 138, 22)
    F.jug(k, 110, 138, 40, level=0.35)
    k.ice_bowl(220 if not hook else 90, 138, 54, full=False)
    # the windowsill: locket + its open box (or the empty box)
    k.jewel_box(230, sill_y, 26, empty=not locket)
    if locket: k.locket(262, sill_y + 8, 7)
    with k.tint(PAL.copper): k.shape([(300, sill_y), (322, sill_y), (319, sill_y + 16), (303, sill_y + 16)], lw=0.7, fill=Wt, amp=0)
    for j in range(5): k.circle(304 + j * 3.4, sill_y + 19 + (j % 2) * 3, 2.6, lw=0.4, fill=[ROSE, PAL.sun, ROSE2][j % 3])
    if not locket and not hook: k.text(250, 300, "?", size=44, font="Ink-Playfair", color=shade(PAL.stage, 0.9))
    k.unclip()

def kitchen_gone(k, w, h): kitchen(k, w, h, locket=False)
def hook_scene(k, w, h): kitchen(k, w, h, locket=False, hook=True)

PW = 512
def lineup(k, w, h):
    """Quill (with Agnes, at the harbour office) | Demelza (deckchair by the roses) | Mr Bramble (bench in the shade).
    Same figure height, framing, nameplate and colour weight for the three suspects."""
    for i in range(3):
        k.c.saveState(); k.c.translate(i * PW, 0); pw = PW
        k.frame2(pw, h); k.clip_rect(14, 14, pw - 14, h - 14); cx = pw / 2; fh = 236
        if i == 0:
            k.vgrad(14, 120, pw - 14, h - 14, PAL.sky, PAL.sky2, steps=14)
            k.vgrad(14, 96, pw - 14, 130, PAL.sea, PAL.sea2, steps=6)
            k.wash_rect(14, 14, pw - 14, 96, PAL.rock)
            with k.tint(PAL.rock): k.hatch([(14, 14), (pw - 14, 14), (pw - 14, 96), (14, 96)], angle=0, gap=6, lw=0.3)
            k.harbour_office(cx + 40, 96, 190, 190)
            k.boat(80, 104, 40)
            F.agnes(k, cx + 150, 70, 200, teapot=False)
            F.quill(k, cx - 46, 70, fh)
            nameplate(k, cx, 40, "CAPTAIN QUILL, HARBOURMASTER")
        elif i == 1:
            k.vgrad(14, 140, pw - 14, h - 14, HOT, HOT2, steps=14)
            k.lawn(14, pw - 14, 140, 126)
            k.picket(14, pw - 14, 140, 30)
            for rx in (cx + 90, cx + 170, 60): k.rosebush(rx, 140, 80)
            k.deckchair(cx - 10, 70, 150)
            with F.seated(): F.demelza(k, cx - 46, 70, fh, asleep=True)
            F.lemonade_glass(k, cx + 110, 72, 30, ice="melted", full=0.85)
            nameplate(k, cx, 40, "DEMELZA ROWE")
        else:
            k.vgrad(14, 140, pw - 14, h - 14, HOT, HOT2, steps=14)
            k.lawn(14, pw - 14, 140, 126)
            k.wash([(14, 14), (pw - 14, 14), (pw - 14, 120), (14, 150)], shade(LAWN, 0.86))   # shade of the tree
            k.rect(pw - 90, 120, 26, 250, lw=1.0, fill=PAL.wood_dk)
            with k.tint(PAL.leaf): k.shape(k.arcpts(pw - 100, 330, 180, 70, 0, 360, 30), lw=0.9, fill=Wt, amp=1.0)
            k.bench(cx + 10, 40, 240, seat=100)
            with F.seated(): F.bramble(k, cx - 46, 70, fh, ice="fresh", frost=True)
            nameplate(k, cx, 40, "MR BRAMBLE")
        k.unclip(); k.c.restoreState()

def garden(k, w, h):
    frame_open(k, w, h)
    k.vgrad(14, 140, w - 14, h - 14, HOT, HOT2, steps=16)
    k.sun_big(w * 0.82, h * 0.8, 34)
    k.lawn(14, w - 14, 140, 126)
    k.picket(14, w - 14, 140, 34)
    for rx in (60, 150, 420): k.rosebush(rx, 140, 90)
    F.agnes(k, w * 0.36, 40, 230, teapot=False)
    F.loveday(k, w * 0.62, 40, 230, jug_=False)
    k.unclip()

def glasses(k, w, h):
    """Solution: everyone else's glass (ice long melted) vs Mr Bramble's (frosty, large sharp cubes)."""
    frame_open(k, w, h)
    k.vgrad(14, 120, w - 14, h - 14, HOT, HOT2, steps=16)
    k.sun_big(w * 0.5, h * 0.82, 30)
    with k.tint(PAL.cloud): k._table(14, w - 14, 120, depth=10, skirt=106)
    F.lemonade_glass(k, w * 0.28, 124, 130, ice="melted", full=0.55)
    F.lemonade_glass(k, w * 0.72, 124, 130, ice="fresh", frost=True, full=0.8)
    for x, t in ((w * 0.28, "EVERYONE ELSE\u2019S"), (w * 0.72, "MR BRAMBLE\u2019S")): nameplate(k, x, 80, t, size=12)
    k.text(w * 0.28, 268, "melted", size=18, font="Ink-CrimsonI", color=shade(PAL.sea2, 0.7))
    k.text(w * 0.72, 268, "fresh ice!", size=18, font="Ink-CrimsonI", color=shade(PAL.stage, 0.9))
    k.unclip()

def returned(k, w, h):
    frame_open(k, w, h)
    k.vgrad(14, 140, w - 14, h - 14, HOT, HOT2, steps=16)
    k.lawn(14, w - 14, 140, 126)
    k.cottage_big(w * 0.6, 140, 170, 140)
    k.bunting(14, w - 14, h - 34, sag=12, n=18, size=7)
    F.bramble(k, w * 0.28, 40, 230, expr="sheepish", prop=False, locket=True)
    F.loveday(k, w * 0.56, 40, 230)
    k.unclip()

def cast_strip(k, w, h):
    """Three suspects side by side for the opening hook (same height, pose, props and colour weight)."""
    k.vgrad(0, 70, w, h, HOT, HOT2, steps=10); k.lawn(0, w, 70, 70)
    for rx in (40, 300, 560): k.rosebush(rx, 70, 60)
    for i, fn in enumerate([F.quill, F.demelza, F.bramble]):
        fn(k, w * (0.16 + 0.32 * i), 20, h * 0.86)
    k.c.setStrokeColor(K); k.c.setLineWidth(1.3); k.c.rect(1, 1, w - 2, h - 2, stroke=1, fill=0)

def vignette(k, w, h):
    k.circle(w / 2, h / 2, w * 0.46, lw=1.3, fill=HOT2); k.circle(w / 2, h / 2, w * 0.44, lw=0.45, fill=None)
    k.c.saveState(); p = k.c.beginPath(); p.circle(w / 2, h / 2, w * 0.44 - 1); k.c.clipPath(p, stroke=0, fill=0)
    k.vgrad(0, 0, w, h * 0.38, LAWN, LAWN2, steps=8)
    k.sun_big(w * 0.7, h * 0.74, 26)
    k.picket(0, w, h * 0.36, 26)
    k.rect(w * 0.16, h * 0.34, w * 0.68, 10, lw=0.9, fill=PAL.wood)
    F.jug(k, w * 0.4, h * 0.365, 110)
    F.lemonade_glass(k, w * 0.66, h * 0.365, 56, ice="melted")
    k.c.restoreState()

AW, AH = 512, 384
SCENES = dict(hillparty=(hillparty, AW, AH), lawn=(lawn_scene, AW, AH), kitchen=(kitchen, AW, AH), kitchen_gone=(kitchen_gone, AW, AH),
              hook=(hook_scene, AW, AH), lineup=(lineup, 3 * PW, AH), garden=(garden, AW, AH), glasses=(glasses, AW, AH),
              returned=(returned, AW, AH), cast=(cast_strip, 600, 260), vignette=(vignette, 384, 384))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    want = [a for a in sys.argv[1:] if not a.startswith("--")] or list(SCENES)
    for i, name in enumerate(want):
        fn, pw, ph = SCENES[name]
        def draw(c, W, H, fn=fn, i=i):
            k = Garden(c, seed=21 + i); fn(k, W, H)
        render_color(os.path.join(OUT, name + ".png"), pw / 72, ph / 72, draw, seed=21 + i)
        print(name, flush=True)
