"""Colour storybook illustrations for the Case 1 video: house inkart ink lines over soft watercolour-style
washes (colorink.py), with the simple v1 peg-doll characters (figures.py). Everything is drawn in code.
Seaside/summer additions live in the Sea subclass (no snow, no icicles). Output: ../work/art/*.png (RGB)
Run: python3 art.py [scene ...]        python3 art.py --detailed   (use the v2 detailed people.py instead)"""
import math, os, sys
from inkart import Ink, lerp, K, Wt
from colorink import ColorInk, PAL, render_color, shade, mix
import inkart, figures, people as detailed_people
people = detailed_people if "--detailed" in sys.argv else figures

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art")

class Sea(ColorInk, Ink):
    # --- summer roof: tiled, hatched, no snow ---------------------------------
    def roof(s, x0, x1, ybase, ypeak, overhang=4, snow=0, lw=0.9, color=None):
        xm = (x0 + x1) / 2
        pts = [(x0 - overhang, ybase), (xm, ypeak), (x1 + overhang, ybase)]
        col = color or PAL.roof
        with s.tint(col):
            s.shape(pts, lw=lw, fill=Wt, amp=0.2)
            s.hatch(pts, angle=0, gap=2.6, lw=0.4, jitter=0.1)
        s.wash([(xm, ypeak), (x1 + overhang, ybase), (xm, ybase)], shade(col, 0.9))
        with s.tint(col, hatch=shade(col, 0.66)):
            s.hatch([(xm, ypeak), (x1 + overhang, ybase), (xm, ybase)], angle=-60, gap=1.9, lw=0.35)
        s.shape(pts, lw=lw, fill=None, amp=0)

    def window(s, x, y, w, h, lit=True, arch=False, lw=0.6):
        with s.tint(PAL.glass): super().window(x, y, w, h, lit=lit, arch=arch, lw=lw)

    def wall(s, x, y, w, h, boards=True, gap=3.0, lw=0.9, color=None):
        with s.tint(color or PAL.walls[4]): super().wall(x, y, w, h, boards=boards, gap=gap, lw=lw)

    def chimney(s, x, y, w, h, smoke=True):
        with s.tint(PAL.chimney): super().chimney(x, y, w, h, smoke=smoke)

    def cottage(s, x, y, w, h, chimney=True, door_side=0.62, i=0):
        s.wall(x, y, w, h * 0.6, gap=2.6, color=PAL.walls[i % len(PAL.walls)])
        s.roof(x, x + w, y + h * 0.6, y + h, overhang=2.5, color=PAL.slate if i % 2 else PAL.roof)
        s.window(x + w * 0.14, y + h * 0.2, w * 0.22, h * 0.2)
        with s.tint(None, dark=PAL.doors[i % len(PAL.doors)]):
            s.shape([(x + w * door_side, y), (x + w * (door_side + 0.2), y), (x + w * (door_side + 0.2), y + h * 0.38), (x + w * door_side, y + h * 0.38)], lw=0.7, fill=K, amp=0)
        if chimney: s.chimney(x + w * 0.72, y + h * 0.78, w * 0.1, h * 0.28)

    def waves(s, x0, x1, y0, y1, rows=7, lw=0.5):
        for k in range(rows):
            y = lerp(y1, y0, k / max(1, rows - 1)); n = 3 + k
            for _ in range(n):
                L = s.r.uniform(10, 24) * (0.6 + 0.12 * k); x = s.r.uniform(x0, x1 - L)
                s.line([(x + L * t, y + 1.2 * math.sin(t * math.pi * 2)) for t in [i / 10 for i in range(11)]], lw=lw * (0.6 + 0.08 * k), amp=0)

    def gull(s, x, y, w, lw=0.8):
        s.line(s.arcpts(x - w / 4, y, w / 4, w * 0.18, 160, 20, 10), lw=lw, amp=0)
        s.line(s.arcpts(x + w / 4, y, w / 4, w * 0.18, 160, 20, 10), lw=lw, amp=0)

    def boat(s, x, y, w, sail=True):
        hull = [(x - w / 2, y + w * 0.16), (x + w / 2, y + w * 0.16), (x + w * 0.38, y), (x - w * 0.36, y)]
        with s.tint(s.r.choice([PAL.doors[1], PAL.doors[0], PAL.doors[3]])): s.shape(hull, lw=0.9, fill=Wt, amp=0.1)
        s.hatch([(x - w * 0.36, y), (x + w * 0.38, y), (x + w * 0.44, y + w * 0.07), (x - w * 0.43, y + w * 0.07)], angle=0, gap=1.2, lw=0.35)
        if sail:
            s.line([(x, y + w * 0.16), (x, y + w * 0.95)], lw=0.9, amp=0)
            with s.tint(PAL.cloud): s.shape([(x + 1.5, y + w * 0.92), (x + 1.5, y + w * 0.22), (x + w * 0.42, y + w * 0.22)], lw=0.8, fill=Wt, amp=0.1)
            with s.tint(PAL.sun): s.shape([(x - 1.5, y + w * 0.8), (x - 1.5, y + w * 0.24), (x - w * 0.3, y + w * 0.24)], lw=0.8, fill=Wt, amp=0.1)
            with s.tint(PAL.sun): s.hatch([(x - 1.5, y + w * 0.8), (x - 1.5, y + w * 0.24), (x - w * 0.3, y + w * 0.24)], angle=60, gap=1.5, lw=0.3)
        s.line([(x - w * 0.6, y + 0.5), (x + w * 0.6, y + 0.5)], lw=0.5, amp=0.3)

    def lighthouse(s, x, y, h):
        with s.tint(PAL.cloud, dark=PAL.lighthouse_red): s._lighthouse(x, y, h)

    def _lighthouse(s, x, y, h):
        w0, w1 = h * 0.16, h * 0.1
        body = [(x - w0 / 2, y), (x + w0 / 2, y), (x + w1 / 2, y + h * 0.78), (x - w1 / 2, y + h * 0.78)]
        s.shape(body, lw=0.9, fill=Wt, amp=0)
        for b in range(3):
            t0, t1 = 0.12 + b * 0.24, 0.24 + b * 0.24
            q = [(x - lerp(w0, w1, t0) / 2, y + h * t0), (x + lerp(w0, w1, t0) / 2, y + h * t0), (x + lerp(w0, w1, t1) / 2, y + h * t1), (x - lerp(w0, w1, t1) / 2, y + h * t1)]
            s.shape(q, lw=0.6, fill=K, amp=0)
        s.rect(x - w1 * 0.7, y + h * 0.78, w1 * 1.4, h * 0.03, lw=0.7, fill=K)
        with s.tint(PAL.glass_lit): s.rect(x - w1 * 0.45, y + h * 0.81, w1 * 0.9, h * 0.1, lw=0.8)
        s.c.setLineWidth(0.5)
        for u in (-0.15, 0.15): s.c.line(x + u * w1, y + h * 0.81, x + u * w1, y + h * 0.91)
        s.shape([(x - w1 * 0.6, y + h * 0.91), (x + w1 * 0.6, y + h * 0.91), (x, y + h)], lw=0.8, fill=K, amp=0)
        for sg in (-1, 1):
            s.line([(x + sg * w1 * 0.7, y + h * 0.86), (x + sg * h * 0.5, y + h * 0.95)], lw=0.4, amp=0)
            s.line([(x + sg * w1 * 0.7, y + h * 0.86), (x + sg * h * 0.5, y + h * 0.78)], lw=0.4, amp=0)

    def bunting(s, x0, x1, y, sag=10, n=10, size=6):
        pts = [(lerp(x0, x1, t), y - sag * math.sin(math.pi * t)) for t in [i / 40 for i in range(41)]]
        s.line(pts, lw=0.5, amp=0)
        for i in range(n):
            t = (i + 0.5) / n; px, py = lerp(x0, x1, t), y - sag * math.sin(math.pi * t)
            tri = [(px - size / 2, py), (px + size / 2, py), (px, py - size * 1.2)]
            s.shape(tri, lw=0.5, fill=PAL.bunting[i % len(PAL.bunting)], amp=0)

    def cloche(s, x, y, w, num=None, cloth=True):
        """Glass dome on a plate, white cloth over the top, number card in front. Nothing visible inside."""
        s.shape(s.arcpts(x, y, w * 0.62, w * 0.1, 0, 360, 30), lw=0.8, fill=PAL.cloud, amp=0)
        dome = s.arcpts(x, y + w * 0.04, w * 0.5, w * 0.62, 0, 180, 30)
        s.shape(dome, lw=0.9, fill=PAL.dome, amp=0)
        s.circle(x, y + w * 0.7, w * 0.05, lw=0.7, fill=K)
        if cloth:
            top = s.arcpts(x, y + w * 0.04, w * 0.54, w * 0.68, 8, 172, 30)
            hem = []
            for i in range(13):
                t = i / 12; hx = lerp(x - w * 0.56, x + w * 0.56, t)
                hem.append((hx, y + w * (0.14 if i % 2 else 0.2) + w * 0.05 * math.sin(t * 9)))
            cl = top + hem[::-1] if False else top + list(reversed(hem))
            s.shape([(x + w * 0.56, y + w * 0.2)] + top + [(x - w * 0.56, y + w * 0.2)] + hem, lw=0.9, fill=Wt, amp=0.2)
            for k in range(4):
                u = lerp(-0.38, 0.38, k / 3)
                s.line([(x + u * w * 0.6, y + w * 0.6), (x + u * w, y + w * 0.2)], lw=0.4, amp=0.3)
            s.hatch([(x + w * 0.2, y + w * 0.62)] + [p for p in top if p[0] > x + w * 0.2] + [(x + w * 0.56, y + w * 0.2), (x + w * 0.25, y + w * 0.18)], angle=-65, gap=1.6, lw=0.3)
        else:
            s.c.setLineWidth(0.6); s.c.arc(x - w * 0.36, y + w * 0.1, x + w * 0.1, y + w * 0.6, 110, 50)
        if num is not None: s.card(x + w * 0.34, y - w * 0.2, w * 0.42, str(num))

    def card(s, x, y, w, t):
        h = w * 0.75
        with s.tint(PAL.card): s.shape([(x - w / 2, y), (x + w / 2, y), (x + w * 0.42, y + h), (x - w * 0.42, y + h)], lw=0.7, fill=Wt, amp=0)
        s.text(x, y + h * 0.22, t, size=h * 0.62, font="Ink-Playfair")

    def table(s, x0, x1, y, depth=8, skirt=26):
        with s.tint(PAL.cloth_tbl): s._table(x0, x1, y, depth, skirt)

    def _table(s, x0, x1, y, depth=8, skirt=26):
        s.shape([(x0, y), (x1, y), (x1 - depth, y + depth), (x0 + depth, y + depth)], lw=0.9, fill=Wt, amp=0)
        sk = [(x0, y), (x1, y), (x1, y - skirt), (x0, y - skirt)]
        s.shape(sk, lw=0.9, fill=Wt, amp=0.1)
        for i in range(1, 14):
            xx = lerp(x0, x1, i / 14); s.line([(xx, y - 1), (xx + s.r.uniform(-1, 1), y - skirt + 1)], lw=0.35, amp=0.3)
        s.line([(lerp(x0, x1, t), y - skirt + 2.5 * abs(math.sin(t * 30))) for t in [i / 80 for i in range(81)]], lw=0.8, amp=0)

    def handbag(s, x, y, w, paper=True):
        with s.tint(PAL.bag, dark=PAL.bag_dk): s._handbag(x, y, w, paper)

    def _handbag(s, x, y, w, paper=True):
        h = w * 0.62
        body = [(x - w / 2, y), (x + w / 2, y), (x + w * 0.42, y + h), (x - w * 0.42, y + h)]
        if paper:
            pp = [(x - w * 0.12, y + h * 0.7), (x + w * 0.3, y + h * 0.75), (x + w * 0.26, y + h * 1.45), (x - w * 0.16, y + h * 1.38)]
            s.shape(pp, lw=0.8, fill=PAL.paper, amp=0.1)
            s.line([(x - w * 0.14, y + h * 1.05), (x + w * 0.28, y + h * 1.1)], lw=0.4, amp=0)
            s.c.saveState(); s.c.translate(x + w * 0.07, y + h * 1.24); s.c.rotate(6)
            s.text(0, 0, "ENTRY LIST", size=w * 0.065, font="Ink-Plex"); s.c.restoreState()
            for k in range(3):
                s.line([(x - w * 0.08, y + h * (1.14 - 0.1 * k) + w * 0.01 * k), (x + w * 0.22, y + h * (1.18 - 0.1 * k))], lw=0.3, amp=0.2)
        s.c.setStrokeColor(PAL.bag_dk); s.c.setLineWidth(3.0); s.c.arc(x - w * 0.28, y + h * 0.5, x + w * 0.28, y + h * 1.5, 0, 180)
        s.shape(body, lw=1.0, fill=Wt, amp=0.1)
        s.hatch([(x + w * 0.15, y), (x + w / 2, y), (x + w * 0.42, y + h), (x + w * 0.1, y + h)], angle=80, gap=1.6, lw=0.35)
        flap = [(x - w * 0.43, y + h)] + s.arcpts(x, y + h, w * 0.43, h * 0.45, 180, 360, 24)[1:]
        s.shape(flap, lw=0.9, fill=K, amp=0)
        s.circle(x, y + h * 0.58, w * 0.045, lw=0.8, fill=PAL.brass)
        s.shape(body, lw=1.0, fill=None, amp=0)

    def plate(s, x, y, w, crumbs=0):
        s.shape(s.arcpts(x, y, w / 2, w * 0.13, 0, 360, 36), lw=0.9, fill=PAL.cloud, amp=0)
        s.c.setStrokeColor(PAL.rosette); s.c.setLineWidth(1.0); s.c.ellipse(x - w * 0.44, y - w * 0.11, x + w * 0.44, y + w * 0.11)
        s.shape(s.arcpts(x, y + 0.5, w * 0.34, w * 0.08, 0, 360, 36), lw=0.5, fill=None, amp=0)
        for i in range(crumbs):
            a = s.r.uniform(0, 6.28); rr = s.r.uniform(0, 0.3)
            s.circle(x + w * rr * math.cos(a), y + w * 0.08 * rr / 0.3 * math.sin(a), s.r.uniform(0.6, 1.6), lw=0.4, fill=PAL.crust if i % 3 == 0 else PAL.lemon)

    def loaf(s, x, y, w):
        h = w * 0.45
        s.shape(s.arcpts(x, y, w / 2, h, 0, 180, 24) + [(x - w / 2, y)], lw=0.9, fill=PAL.bread, amp=0.1)
        for k in range(3):
            u = -0.25 + 0.25 * k; s.line([(x + u * w - w * 0.06, y + h * 0.45), (x + u * w + w * 0.06, y + h * 0.85)], lw=0.7, amp=0)
        with s.tint(PAL.bread): s.hatch([(x + w * 0.1, y)] + [p for p in s.arcpts(x, y, w / 2, h, 0, 70, 10)] + [(x + w * 0.1, y + h * 0.95)], angle=70, gap=1.4, lw=0.3)

    def vase(s, x, y, h):
        w = h * 0.35
        body = [(x - w * 0.35, y), (x + w * 0.35, y), (x + w / 2, y + h * 0.4), (x + w * 0.25, y + h * 0.62), (x - w * 0.25, y + h * 0.62), (x - w / 2, y + h * 0.4)]
        for i in range(9):
            a = math.radians(lerp(55, 125, i / 8)); L = h * s.r.uniform(0.55, 0.85)
            ex, ey = x + L * math.cos(a), y + h * 0.6 + L * math.sin(a) * 0.8
            s.line([(x, y + h * 0.6), (ex, ey)], lw=0.5, amp=0.3, color=shade(PAL.leaf, 0.8))
            for j in range(3):
                s.shape(s.arcpts(ex + s.r.uniform(-2, 2), ey + j * 2.2 - 2, 2.3, 1.7, 0, 360, 10), lw=0.5, fill=[PAL.pea_pink, PAL.pea_purple, PAL.pea_white][(i + j) % 3], amp=0)
        with s.tint(PAL.teal_lt):
            s.shape(body, lw=0.9, fill=Wt, amp=0)
            s.hatch(body, angle=0, gap=2.2, lw=0.35)
        s.shape(body, lw=0.9, fill=None, amp=0)

    def chair_stack(s, x, y, h, n=4):
        w = h * 0.42
        for i in range(n):
            yy = y + i * h * 0.09
            wc = shade(PAL.wood_dk, 0.85)
            s.line([(x - w / 2, yy), (x - w / 2, yy + h * 0.95)], lw=1.4, amp=0, color=wc)
            s.line([(x - w / 2, yy + h * 0.45), (x + w / 2, yy + h * 0.45)], lw=1.8, amp=0, color=wc)
            s.line([(x + w / 2, yy), (x + w / 2, yy + h * 0.45)], lw=1.4, amp=0, color=wc)
            s.line([(x - w / 2, yy + h * 0.8), (x - w / 2 + 6, yy + h * 0.82)], lw=1.2, amp=0, color=wc)

    def rosette(s, x, y, r, t="1st"):
        for sg in (-1, 1):
            s.shape([(x + sg * r * 0.15, y), (x + sg * r * 0.55, y - r * 1.8), (x + sg * r * 0.32, y - r * 1.55), (x + sg * r * 0.15, y - r * 1.85), (x - sg * r * 0.15, y)], lw=0.7, fill=PAL.rosette if sg > 0 else shade(PAL.rosette, 0.85), amp=0)
        pts = []
        for i in range(32):
            a = 2 * math.pi * i / 32; rr = r * (1.0 if i % 2 else 0.86)
            pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
        s.shape(pts, lw=0.8, fill=PAL.rosette, amp=0)
        s.circle(x, y, r * 0.66, lw=0.8, fill=PAL.rosette2)
        s.text(x, y - r * 0.22, t, size=r * 0.62, font="Ink-Playfair")

    def bubble(s, x0, y0, x1, y1, tail):
        r = 10
        pts = s.arcpts(x1 - r, y1 - r, r, r, 0, 90, 6) + s.arcpts(x0 + r, y1 - r, r, r, 90, 180, 6) + s.arcpts(x0 + r, y0 + r, r, r, 180, 270, 6)
        tx, ty = tail
        pts += [(x0 + (x1 - x0) * 0.25, y0), (tx, ty), (x0 + (x1 - x0) * 0.4, y0)] + s.arcpts(x1 - r, y0 + r, r, r, 270, 360, 6)
        s.shape(pts, lw=1.2, fill=PAL.paper, amp=0.15)

    def summer_ground(s, x0, x1, y, depth=40):
        pts = s.hills(x0, x1, y, amp=2, n=2)
        s.shape([(x0, y - depth)] + pts + [(x1, y - depth)], lw=0, fill=PAL.grass, stroke=False, amp=0)
        s.line(pts, lw=0.9, amp=0.2)
        for i in range(30):
            gx = s.r.uniform(x0, x1); gy = y - s.r.uniform(2, depth * 0.8)
            for d in (-1, 0, 1): s.line([(gx, gy), (gx + d * 1.4, gy + 3)], lw=0.4, amp=0, color=shade(PAL.grass, 0.65))

    def frame2(s, w, h, m=10):
        s.c.setStrokeColor(K); s.c.setLineWidth(1.3); s.c.rect(m, m, w - 2 * m, h - 2 * m, stroke=1, fill=0)
        s.c.setLineWidth(0.45); s.c.rect(m + 3.2, m + 3.2, w - 2 * m - 6.4, h - 2 * m - 6.4, stroke=1, fill=0)

# ============================================================================= scenes
# Every scene is a 4:3 canvas (512 x 384 pt), matching the video viewports. Characters come from figures.py.
def hall_interior(k, w, h, floor=120, windows=None, curtains=True):
    """Back wall of the village hall: warm cream walls, panelled dado, arched windows with rose curtains,
    colourful bunting and honey floorboards."""
    k.wash_rect(14, floor, w - 14, h - 14, PAL.hall_wall)
    k.wash_rect(14, floor, w - 14, floor + 44, PAL.dado)
    k.vgrad(14, 14, w - 14, floor, PAL.floor, PAL.floor2, steps=10)
    k.rect(14, floor, w - 28, h - floor - 14, lw=0, fill=None)
    n = windows or max(2, int((w - 28) / 125)); gap = (w - 28) / n
    for i in range(n):
        wx = 14 + gap * (i + 0.5) - 26
        k.window(wx, floor + 70, 52, 120, arch=True, lw=0.8)
        if curtains:
            for sg in (-1, 1):
                ex = wx + (60 if sg > 0 else -8); cx0 = wx + (52 if sg > 0 else 0)
                cur = [(cx0, floor + 222), (ex, floor + 222), (ex + sg * 2, floor + 150), (ex - sg * 1, floor + 70), (cx0 + sg * 2, floor + 70), (cx0 + sg * 8, floor + 130)]
                k.shape(cur, lw=0.7, fill=PAL.curtain, amp=0.2)
                for j in range(3): k.line([(cx0 + sg * (2 + j * 2.4), floor + 220), (cx0 + sg * (5 + j * 2), floor + 135), (cx0 + sg * (2 + j * 2.2), floor + 74)], lw=0.35, amp=0.2, color=shade(PAL.curtain, 0.7))
            k.rect(wx - 12, floor + 222, 76, 3, lw=0.6, fill=PAL.wood_dk)
    k.bunting(14, w - 14, h - 40, sag=16, n=int(w / 24), size=8)
    k.line([(14, floor + 44), (w - 14, floor + 44)], lw=0.8, amp=0.1)
    for i in range(int((w - 28) / 40) + 1):
        x = 18 + i * 40
        if x + 32 < w - 14: k.rect(x, floor + 6, 32, 32, lw=0.4, fill=None)
    k.line([(14, floor), (w - 14, floor)], lw=1.0, amp=0.1)
    for i in range(15):
        u = (i + 0.5) / 15; k.line([(w / 2 + (u - 0.5) * (w - 28) * 0.9, floor), (w / 2 + (u - 0.5) * (w - 28) * 1.9, 14)], lw=0.35, amp=0.1, color=shade(PAL.floor2, 0.7))
    for y in (floor * 0.72, floor * 0.42): k.line([(14, y), (w - 14, y)], lw=0.3, amp=0.2, color=shade(PAL.floor2, 0.7))

def nameplate(k, x, y, text, size=13):
    tw = k.c.stringWidth(text, "Ink-Plex", size)
    k.shape([(x - tw / 2 - 12, y - 7), (x + tw / 2 + 12, y - 7), (x + tw / 2 + 12, y + size + 3), (x - tw / 2 - 12, y + size + 3)], lw=1.0, fill=PAL.card, amp=0)
    k.c.setLineWidth(0.4); k.c.rect(x - tw / 2 - 9, y - 4, tw + 18, size + 4, stroke=1, fill=0)
    k.text(x, y, text, size=size, font="Ink-Plex")

def sky(k, w, h, y0):
    k.vgrad(14, y0, w - 14, h - 14, PAL.sky, PAL.sky2, steps=20)

def village(k, w, h):
    k.frame2(w, h)
    k.clip_rect(14, 14, w - 14, h - 14)
    sky(k, w, h, h * 0.38)
    k.vgrad(14, 14, w - 14, h * 0.41, PAL.sea, PAL.sea2, steps=16)
    for i in range(6): k.gull(k.r.uniform(60, w - 60), k.r.uniform(h * 0.74, h * 0.92), k.r.uniform(10, 18))
    sx, sy = w * 0.84, h * 0.86
    k.circle(sx, sy, 22, lw=0.9, fill=PAL.sun)
    for i in range(12):
        a = 2 * math.pi * i / 12; k.line([(sx + 27 * math.cos(a), sy + 27 * math.sin(a)), (sx + 34 * math.cos(a), sy + 34 * math.sin(a))], lw=0.9, amp=0, color=shade(PAL.sun, 0.8))
    for cx, cy, cw in ((w * 0.36, h * 0.82, 60), (w * 0.6, h * 0.9, 44)):   # summer clouds
        pts = k.arcpts(cx, cy, cw / 2, cw * 0.18, 180, 360, 12)[::-1] + [(cx + cw * 0.4, cy + 6), (cx + cw * 0.15, cy + 14), (cx - cw * 0.1, cy + 10), (cx - cw * 0.35, cy + 6)]
        k.shape(pts, lw=0.7, fill=PAL.cloud, amp=0.3)
    head = [(14, h * 0.42), (14, h * 0.62), (w * 0.1, h * 0.64), (w * 0.2, h * 0.6), (w * 0.27, h * 0.48), (w * 0.3, h * 0.42)]
    with k.tint(PAL.headland):
        k.shape(head, lw=0.9, fill=Wt, amp=0.4)
        k.hatch(head, angle=-60, gap=2.2, lw=0.4)
    k.lighthouse(w * 0.1, h * 0.635, h * 0.25)
    with k.tint(PAL.foam):
        k.c.saveState(); k.c.setStrokeColor(shade(PAL.sea2, 0.7))
        Sea.waves(k, 14, w - 14, 14, h * 0.4, rows=9)
        k.c.restoreState()
    k.boat(w * 0.22, h * 0.2, 46); k.boat(w * 0.5, h * 0.3, 30); k.boat(w * 0.78, h * 0.14, 38)
    with k.tint(PAL.rock):
        k.rect(w * 0.3, h * 0.4, w * 0.7, 12, lw=0.9)
        k.hatch([(w * 0.3, h * 0.4), (w - 14, h * 0.4), (w - 14, h * 0.4 + 12), (w * 0.3, h * 0.4 + 12)], angle=0, gap=3, lw=0.35)
    for i in range(6): k.line([(w * 0.33 + i * 52, h * 0.4), (w * 0.33 + i * 52, h * 0.4 - 18)], lw=1.6, amp=0, color=PAL.wood_dk)   # harbour posts
    base = h * 0.4 + 12
    xs = [(w * 0.31, 44, 54), (w * 0.42, 76, 82), (w * 0.59, 40, 50), (w * 0.69, 44, 60), (w * 0.8, 38, 52), (w * 0.89, 36, 46)]
    for i, (x, cw, chh) in enumerate(xs):
        if i == 1:
            k.wall(x, base, cw, chh * 0.62, gap=2.6, color=PAL.hall_wall)
            k.roof(x, x + cw, base + chh * 0.62, base + chh, color=PAL.slate)
            k.rect(x + cw * 0.12, base + chh * 0.4, cw * 0.76, chh * 0.13, lw=0.6, fill=PAL.card)
            k.text(x + cw / 2, base + chh * 0.43, "VILLAGE HALL", size=chh * 0.075, font="Ink-Plex")
            k.shape([(x + cw * 0.4, base), (x + cw * 0.6, base), (x + cw * 0.6, base + chh * 0.32), (x + cw * 0.4, base + chh * 0.32)], lw=0.7, fill=PAL.teal, amp=0)
            for u in (0.12, 0.72): k.window(x + cw * u, base + chh * 0.1, cw * 0.16, chh * 0.2)
        else:
            k.cottage(x, base, cw, chh, i=i)
    bx0, bx1, by = w * 0.34, w * 0.96, base + 92
    k.line([(bx0, base + 60), (bx0, by + 6)], lw=1.2, amp=0, color=PAL.wood_dk); k.line([(bx1, base + 60), (bx1, by + 6)], lw=1.2, amp=0, color=PAL.wood_dk)
    k.rect(bx0 + 20, by - 4, bx1 - bx0 - 40, 20, lw=0.9, fill=PAL.card)
    k.text((bx0 + bx1) / 2, by + 1.5, "TIDEWHISTLE COVE SUMMER SHOW", size=11, font="Ink-Playfair")
    k.bunting(bx0, bx0 + 20, by + 10, sag=3, n=2, size=5); k.bunting(bx1 - 20, bx1, by + 10, sag=3, n=2, size=5)
    k.bunting(w * 0.3, w - 14, base + 74, sag=10, n=18, size=6)
    k.unclip()

def tearoom(k, w, h):
    k.frame2(w, h)
    k.clip_rect(14, 14, w - 14, h - 14)
    sky(k, w, h, 60)
    k.summer_ground(14, w - 14, 70, depth=56)
    x0, x1, yb = 64, w - 64, 70; top = 336
    k.wall(x0, yb, x1 - x0, top - yb - 60, gap=3.2, color=PAL.walls[2])
    k.roof(x0, x1, top - 60, top + 20, overhang=8, color=PAL.slate)
    k.chimney(x1 - 80, top - 20, 16, 40)
    k.rect(x0 + 40, top - 92, x1 - x0 - 80, 30, lw=1.0, fill=PAL.card)
    k.text(w / 2, top - 83, "THE KETTLE AND GULL", size=16, font="Ink-Playfair")
    # bay window with cups and a teapot, striped awning
    with k.tint(PAL.glass_lit): k.rect(x0 + 18, yb + 40, 120, 90, lw=1.0)
    k.c.setLineWidth(0.8); k.c.setStrokeColor(K)
    for u in (1 / 3, 2 / 3): k.c.line(x0 + 18 + 120 * u, yb + 40, x0 + 18 + 120 * u, yb + 130)
    k.line([(x0 + 18, yb + 70), (x0 + 138, yb + 70)], lw=0.9, amp=0)
    for i in range(3):
        with k.tint([PAL.pea_pink, PAL.teal_lt, PAL.sun][i]): k.cup(x0 + 38 + i * 40, yb + 74, 18)
    with k.tint(PAL.teapot): k.teapot(x0 + 78, yb + 100, 26)
    k.rect(x0 + 12, yb + 34, 132, 6, lw=0.8, fill=PAL.wood)
    aw = [(x0 + 10, yb + 132), (x0 + 146, yb + 132), (x0 + 140, yb + 152), (x0 + 16, yb + 152)]
    k.shape(aw, lw=0.9, fill=PAL.awning_lt, amp=0)
    for i in range(8):
        sx = x0 + 10 + i * 17
        if i % 2 == 0: k.shape([(sx, yb + 132), (sx + 17, yb + 132), (sx + 16.3, yb + 152), (sx + 0.7, yb + 152)], lw=0.4, fill=PAL.stripe, amp=0)
    for i in range(9): k.shape(k.arcpts(x0 + 18 + i * 15, yb + 132, 7.5, 4, 180, 360, 8), lw=0.6, fill=PAL.stripe if i % 2 else PAL.awning_lt, amp=0)
    # door with fanlight
    dx = x1 - 112
    k.shape([(dx, yb), (dx + 52, yb), (dx + 52, yb + 104), (dx, yb + 104)], lw=1.0, fill=PAL.teal, amp=0)
    k.window(dx + 12, yb + 58, 28, 30, lw=0.6)
    k.circle(dx + 44, yb + 48, 2, lw=0.5, fill=PAL.brass)
    k.shape(k.arcpts(dx + 26, yb + 106, 26, 14, 0, 180, 16), lw=0.8, fill=PAL.glass_lit, amp=0)
    for a in range(30, 180, 30): k.line([(dx + 26, yb + 106), (dx + 26 + 24 * math.cos(math.radians(a)), yb + 106 + 12 * math.sin(math.radians(a)))], lw=0.4, amp=0)
    # chalkboard menu, flower tubs, hanging kettle sign, gulls
    k.shape([(x1 + 4, yb - 2), (x1 + 44, yb - 2), (x1 + 40, yb + 56), (x1 + 8, yb + 56)], lw=1.0, fill=PAL.slateboard, amp=0)
    k.c.setFillColor(PAL.cloud); k.c.setFont("Ink-Plex", 7)
    for j, t in enumerate(["TODAY", "TEA", "SCONES", "CAKE"]): k.c.drawCentredString(x1 + 24, yb + 44 - j * 11, t)
    for tx in (x0 + 4, x0 + 150):
        tub = [(tx, yb - 4), (tx + 24, yb - 4), (tx + 21, yb + 14), (tx + 3, yb + 14)]
        with k.tint(PAL.copper):
            k.shape(tub, lw=0.8, fill=Wt, amp=0); k.hatch(tub, angle=0, gap=2, lw=0.35)
        for j in range(6): k.circle(tx + 4 + j * 3.4, yb + 17 + (j % 2) * 3, 2.4, lw=0.5, fill=[PAL.pea_pink, PAL.sun, PAL.pea_purple][j % 3])
    k.line([(x1 - 6, top - 120), (x1 + 20, top - 120)], lw=1.4, amp=0)
    k.line([(x1 + 12, top - 120), (x1 + 12, top - 130)], lw=0.6, amp=0)
    with k.tint(None, dark=PAL.copper): k.kettle(x1 + 12, top - 152, 18)
    k.gull(w * 0.25, h * 0.9, 18); k.gull(w * 0.4, h * 0.94, 12); k.gull(w * 0.74, h * 0.92, 14)
    people.agnes(k, w * 0.53, yb - 6, 150, expr="smile")
    k.unclip()

def hall_table(k, w, h):
    k.frame2(w, h)
    k.clip_rect(14, 14, w - 14, h - 14)
    hall_interior(k, w, h, floor=150)
    people.agnes(k, w - 74, 96, 190, expr="kind", teapot=False)   # judging, standing behind the table
    k.table(24, w - 24, 150, depth=10, skirt=60)
    for i, n in enumerate([3, 4, 5, 6, 7, 8]):
        k.cloche(56 + i * 62, 156, 44, num=n)
    k.unclip()

def handbag_scene(k, w, h):
    k.frame2(w, h)
    k.clip_rect(14, 14, w - 14, h - 14)
    k.wash_rect(14, 110, w - 14, h - 14, PAL.hall_wall)
    k.table(14, w - 14, 110, depth=14, skirt=100)
    k.handbag(w * 0.42, 124, 190)
    k.cloche(w * 0.84, 124, 70, num=None)
    with k.tint(PAL.teal_lt): k.cup(w * 0.12, 124, 40)
    with k.tint(PAL.glass): k.spectacles(w * 0.24, 118, 40)
    k.unclip()

def plate_scene(k, w, h, question=True):
    k.frame2(w, h)
    k.clip_rect(14, 14, w - 14, h - 14)
    hall_interior(k, w, h, floor=160)
    k.table(14, w - 14, 140, depth=14, skirt=128)
    k.plate(w * 0.44, 160, 150, crumbs=18)
    k.cloche(w * 0.82, 152, 80, cloth=False)
    cl = [(40, 150), (100, 152), (112, 172), (90, 190), (60, 186), (38, 168)]
    k.shape(cl, lw=0.9, fill=PAL.cloud, amp=0.6)
    for j in range(3): k.line([(50 + j * 16, 156), (64 + j * 12, 182)], lw=0.4, amp=0.4)
    k.card(w * 0.44 + 46, 132, 40, "7")
    if question: k.text(w * 0.44, 262, "?", size=60, font="Ink-Playfair", color=shade(PAL.stage, 0.9))
    k.unclip()

def hook_scene(k, w, h):
    """Opening hook: the empty prize plate with crumbs (no '?', the video lays big text over it)."""
    plate_scene(k, w, h, question=False)

PW = 512   # lineup panel width (each panel is a 4:3 scene)
def lineup(k, w, h):
    """Wide strip: Ollie | Morwenna | Hedley | Jago, one 4:3 panel each (the video pans between them).
    The three suspects get the same height, framing, face, carry pose and colour weight."""
    for i in range(4):
        k.c.saveState(); k.c.translate(i * PW, 0)
        pw = PW; k.frame2(pw, h)
        k.clip_rect(14, 14, pw - 14, h - 14)
        hall_interior(k, pw, h, floor=96)
        cx = pw / 2; fy, fh = 70, 236
        if i == 0:   # the stage behind, curtains drawn back
            k.rect(cx + 40, 96, 200, 40, lw=1.0, fill=PAL.wood)
            with k.tint(PAL.wood): k.hatch([(cx + 40, 96), (cx + 240, 96), (cx + 240, 136), (cx + 40, 136)], angle=0, gap=3, lw=0.35)
            for x0c in (cx + 44, cx + 200):
                cur = [(x0c, 138), (x0c + 36, 138), (x0c + 36, 300), (x0c, 300)]
                with k.tint(PAL.stage):
                    k.shape(cur, lw=0.9, fill=Wt, amp=0.1); k.hatch(cur, angle=90, gap=2.2, lw=0.35)
                k.line([(x0c + 2, 200), (x0c + 34, 206)], lw=1.4, amp=0, color=PAL.brass)
            k.rect(cx + 34, 300, 212, 12, lw=0.9, fill=PAL.stage)
            people.ollie(k, cx - 40, fy, fh)
            nameplate(k, cx, 40, "CONSTABLE OLLIE PENROSE")
        elif i == 1:   # flower table: vases of sweet peas
            k.rect(cx + 40, 46, 150, 92, lw=0.9, fill=PAL.cloth_tbl)
            with k.tint(PAL.cloth_tbl): k.hatch([(cx + 40, 46), (cx + 190, 46), (cx + 190, 138), (cx + 40, 138)], angle=90, gap=6, lw=0.35)
            k.vase(cx + 80, 138, 74); k.vase(cx + 150, 138, 92)
            k.shape([(cx + 100, 138), (cx + 126, 138), (cx + 124, 156), (cx + 102, 156)], lw=0.8, fill=PAL.teal, amp=0)   # watering can
            k.line([(cx + 126, 150), (cx + 142, 166)], lw=1.4, amp=0)
            people.morwenna(k, cx - 46, fy, fh)
            nameplate(k, cx, 40, "MORWENNA DAY")
        elif i == 2:   # chair stacks and the chair cupboard
            k.rect(cx + 70, 96, 110, 160, lw=1.0, fill=PAL.wood)
            k.rect(cx + 78, 104, 46, 144, lw=0.6, fill=mix(PAL.wood, PAL.cloud, 0.25)); k.rect(cx + 126, 104, 46, 144, lw=0.6, fill=mix(PAL.wood, PAL.cloud, 0.25))
            k.circle(cx + 120, 170, 2, lw=0.5, fill=PAL.brass); k.circle(cx + 130, 170, 2, lw=0.5, fill=PAL.brass)
            k.rect(cx + 98, 230, 54, 14, lw=0.6, fill=PAL.card); k.text(cx + 125, 233.5, "CHAIRS", size=8, font="Ink-Plex")
            k.chair_stack(cx + 196, 46, 110, n=5)
            people.hedley(k, cx - 46, fy, fh)
            nameplate(k, cx, 40, "HEDLEY TRUSCOTT")
        else:   # bread display
            k.rect(cx + 40, 46, 160, 80, lw=0.9, fill=PAL.wood)
            with k.tint(PAL.wood): k.hatch([(cx + 40, 46), (cx + 200, 46), (cx + 200, 126), (cx + 40, 126)], angle=0, gap=4, lw=0.35)
            for dx, dy in ((70, 126), (120, 126), (170, 126), (95, 146), (145, 146)): k.loaf(cx + dx, dy, 44)
            nameplate(k, cx + 120, 104, "BREAD CLASS", size=9)
            people.jago(k, cx - 46, fy, fh)
            nameplate(k, cx, 40, "JAGO PENHALLOW, BAKER")
        k.unclip(); k.c.restoreState()

def cast_strip(k, w, h):
    """Three suspects side by side for the opening hook (same height, pose and colour weight)."""
    k.c.saveState(); k.c.translate(-14, -14); hall_interior(k, w + 28, h + 28, floor=84); k.c.restoreState()
    for i, fn in enumerate([people.morwenna, people.hedley, people.jago]):
        fn(k, w * (0.17 + 0.32 * i), 20, h * 0.86)
    k.c.setStrokeColor(K); k.c.setLineWidth(1.3); k.c.rect(1, 1, w - 2, h - 2, stroke=1, fill=0)

def clue_scene(k, w, h):
    k.frame2(w, h)
    k.clip_rect(14, 14, w - 14, h - 14)
    k.wash_rect(14, 100, w - 14, h - 14, PAL.hall_wall)
    k.bunting(14, w - 14, h - 26, sag=10, n=20, size=7)
    k.table(14, w - 14, 100, depth=12, skirt=90)
    k.cloche(w * 0.25, 112, 110, num=7)
    k.handbag(w * 0.72, 112, 120)
    k.bubble(60, 250, w - 60, 350, tail=(w * 0.3, 222))
    k.text(w / 2, 316, "\u201c\u2026somebody else\u2019s", size=20, font="Ink-CrimsonI")
    k.text(w / 2, 276, "LEMON DRIZZLE?\u201d", size=30, font="Ink-Playfair")
    k.line([(w / 2 - 120, 268), (w / 2 + 120, 268)], lw=1.4, amp=0.6, color=PAL.jam)
    k.line([(w / 2 - 110, 263), (w / 2 + 116, 264)], lw=0.8, amp=0.6, color=PAL.jam)
    k.unclip()

def van_scene(k, w, h):
    k.frame2(w, h)
    k.clip_rect(14, 14, w - 14, h - 14)
    sky(k, w, h, 60)
    k.vgrad(14, 120, w - 14, 150, PAL.sea, PAL.sea2, steps=6)
    k.summer_ground(14, w - 14, 70, depth=56)
    k.wash_rect(14, 14, w - 14, 70, PAL.grass)
    x0, x1, yb = 40, 300, 84
    body = [(x0, yb), (x1, yb), (x1, yb + 110), (x0 + 70, yb + 110), (x0 + 40, yb + 70), (x0, yb + 64)]
    k.shape(body, lw=1.1, fill=PAL.van, amp=0.2)
    k.window(x0 + 46, yb + 72, 26, 30, lw=0.7)
    k.rect(x0 + 92, yb + 40, x1 - x0 - 128, 46, lw=0.7, fill=PAL.card)
    k.text((x0 + 100 + x1) / 2 - 20, yb + 66, "PENHALLOW", size=16, font="Ink-Playfair")
    k.text((x0 + 100 + x1) / 2 - 20, yb + 48, "BAKERY", size=12, font="Ink-Plex")
    k.loaf((x0 + 100 + x1) / 2 - 20, yb + 18, 40)
    for wx in (x0 + 50, x1 - 50):
        with k.tint(PAL.silver, dark=PAL.slateboard): k.wheel(wx, yb, 20)
    cx = x1 - 40
    k.rect(cx - 90, 30, 130, 50, lw=1.0, fill=PAL.wicker)
    with k.tint(PAL.wicker): k.hatch([(cx - 90, 30), (cx + 40, 30), (cx + 40, 80), (cx - 90, 80)], angle=0, gap=6, lw=0.6)
    k.text(cx - 25, 46, "BREAD", size=12, font="Ink-Plex")
    k.loaf(cx - 65, 80, 36); k.loaf(cx + 15, 80, 36)
    lemon_cake(k, cx - 25, 82, 34)
    people.jago(k, w - 96, 52, 230, expr="sheepish", basket=False)   # pink to the tips of his ears
    k.unclip()

def lemon_cake(k, x, y, w):
    with k.tint(PAL.sponge, hatch=PAL.cream, hatch_lw=0.8): k.cake(x, y, w)
    h = w * 0.55
    k.shape(k.arcpts(x, y + h, w / 2, w * 0.1, 0, 360, 30), lw=0.9, fill=PAL.lemon, amp=0)

def prize_scene(k, w, h):
    k.frame2(w, h)
    k.clip_rect(14, 14, w - 14, h - 14)
    hall_interior(k, w, h, floor=150)
    people.agnes(k, 80, 96, 190, expr="smile", teapot=False)
    k.table(24, w - 24, 150, depth=10, skirt=60)
    cx = w / 2 + 30
    k.shape([(cx - 34, 158), (cx + 34, 158), (cx + 8, 176), (cx - 8, 176)], lw=0.9, fill=PAL.cloud, amp=0)
    lemon_cake(k, cx, 178, 120)
    for i in range(8):
        dx = lerp(-52, 52, i / 7); L = k.r.uniform(8, 22)
        k.line([(cx + dx, 244), (cx + dx + 1, 244 - L)], lw=2.0, amp=0, color=PAL.cream); k.circle(cx + dx + 1, 244 - L, 1.8, lw=0.4, fill=PAL.cream)
    for i in range(3):
        k.shape(k.arcpts(cx - 30 + i * 30, 252, 9, 3, 0, 360, 12), lw=0.6, fill=PAL.lemon, amp=0)
        k.c.setLineWidth(0.4); k.c.line(cx - 39 + i * 30, 252, cx - 21 + i * 30, 252)
    k.rosette(cx + 96, 196, 22)
    k.card(cx - 86, 160, 40, "7")
    k.unclip()

def title_vignette(k, w, h):
    """Small round vignette for the title card: teapot and cup, gull, lighthouse."""
    k.circle(w / 2, h / 2, w * 0.46, lw=1.3, fill=PAL.sky); k.circle(w / 2, h / 2, w * 0.44, lw=0.45, fill=None)
    k.c.saveState(); p = k.c.beginPath(); p.circle(w / 2, h / 2, w * 0.44 - 1); k.c.clipPath(p, stroke=0, fill=0)
    k.vgrad(0, 0, w, h * 0.37, PAL.sea, PAL.sea2, steps=12)
    k.c.saveState(); k.c.setStrokeColor(shade(PAL.sea2, 0.7)); Sea.waves(k, 0, w, h * 0.06, h * 0.36, rows=6); k.c.restoreState()
    k.lighthouse(w * 0.2, h * 0.38, h * 0.3)
    k.gull(w * 0.62, h * 0.76, 22); k.gull(w * 0.76, h * 0.7, 14)
    k.rect(w * 0.3, h * 0.36, w * 0.6, 10, lw=0.9, fill=PAL.wood)
    with k.tint(PAL.teapot): k.teapot(w * 0.52, h * 0.39, 90)
    with k.tint(PAL.teal_lt): k.cup(w * 0.78, h * 0.39, 44)
    k.c.restoreState()

def cast_sheet(k, w, h):
    """Reference sheet (not used in the video): every character at the same scale."""
    for i, fn in enumerate([people.agnes, people.ollie, people.morwenna, people.hedley, people.jago]):
        fn(k, 60 + i * 98, 20, 260)

AW, AH = 512, 384
SCENES = dict(village=(village, AW, AH), tearoom=(tearoom, AW, AH), hall=(hall_table, AW, AH), handbag=(handbag_scene, AW, AH),
              plate=(plate_scene, AW, AH), hook=(hook_scene, AW, AH), lineup=(lineup, 4 * PW, AH), cast=(cast_strip, 600, 260),
              clue=(clue_scene, AW, AH), van=(van_scene, AW, AH), prize=(prize_scene, AW, AH), vignette=(title_vignette, 384, 384),
              castsheet=(cast_sheet, AW, 300))
DEFAULT = [n for n in SCENES if n != "castsheet"]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    want = [a for a in sys.argv[1:] if not a.startswith("--")] or DEFAULT
    for i, name in enumerate(want):
        fn, pw, ph = SCENES[name]
        def draw(c, W, H, fn=fn, i=i):
            k = Sea(c, seed=7 + i); fn(k, W, H)
        render_color(os.path.join(OUT, name + ".png"), pw / 72, ph / 72, draw, seed=7 + i)
        print(name)
