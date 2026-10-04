"""Ink illustrations for the Case 1 video, drawn in code in the house inkart style (pure black/white strokes).
Seaside/summer additions live in the Sea subclass (no snow, no icicles). Output: ../work/art/*.png
Run: python3 art.py"""
import math, os
from inkart import Ink, render, lerp, K, Wt
import inkart

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art")
S = 384  # square canvas in points (5.33 in at 300 dpi = 1600 px)

class Sea(Ink):
    # --- summer roof: tiled, hatched, no snow ---------------------------------
    def roof(s, x0, x1, ybase, ypeak, overhang=4, snow=0, lw=0.9):
        xm = (x0 + x1) / 2
        pts = [(x0 - overhang, ybase), (xm, ypeak), (x1 + overhang, ybase)]
        s.shape(pts, lw=lw, fill=Wt, amp=0.2)
        s.hatch(pts, angle=0, gap=2.6, lw=0.4, jitter=0.1)
        s.hatch([(xm, ypeak), (x1 + overhang, ybase), (xm, ybase)], angle=-60, gap=1.9, lw=0.35)
        s.shape(pts, lw=lw, fill=None, amp=0)

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
        s.shape(hull, lw=0.9, fill=Wt, amp=0.1)
        s.hatch([(x - w * 0.36, y), (x + w * 0.38, y), (x + w * 0.44, y + w * 0.07), (x - w * 0.43, y + w * 0.07)], angle=0, gap=1.2, lw=0.35)
        if sail:
            s.line([(x, y + w * 0.16), (x, y + w * 0.95)], lw=0.9, amp=0)
            s.shape([(x + 1.5, y + w * 0.92), (x + 1.5, y + w * 0.22), (x + w * 0.42, y + w * 0.22)], lw=0.8, fill=Wt, amp=0.1)
            s.shape([(x - 1.5, y + w * 0.8), (x - 1.5, y + w * 0.24), (x - w * 0.3, y + w * 0.24)], lw=0.8, fill=Wt, amp=0.1)
            s.hatch([(x - 1.5, y + w * 0.8), (x - 1.5, y + w * 0.24), (x - w * 0.3, y + w * 0.24)], angle=60, gap=1.5, lw=0.3)
        s.line([(x - w * 0.6, y + 0.5), (x + w * 0.6, y + 0.5)], lw=0.5, amp=0.3)

    def lighthouse(s, x, y, h):
        w0, w1 = h * 0.16, h * 0.1
        body = [(x - w0 / 2, y), (x + w0 / 2, y), (x + w1 / 2, y + h * 0.78), (x - w1 / 2, y + h * 0.78)]
        s.shape(body, lw=0.9, fill=Wt, amp=0)
        for b in range(3):
            t0, t1 = 0.12 + b * 0.24, 0.24 + b * 0.24
            q = [(x - lerp(w0, w1, t0) / 2, y + h * t0), (x + lerp(w0, w1, t0) / 2, y + h * t0), (x + lerp(w0, w1, t1) / 2, y + h * t1), (x - lerp(w0, w1, t1) / 2, y + h * t1)]
            s.shape(q, lw=0.6, fill=K, amp=0)
        s.rect(x - w1 * 0.7, y + h * 0.78, w1 * 1.4, h * 0.03, lw=0.7, fill=K)
        s.rect(x - w1 * 0.45, y + h * 0.81, w1 * 0.9, h * 0.1, lw=0.8)
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
            s.shape(tri, lw=0.5, fill=K if i % 2 else Wt, amp=0)

    def figure(s, x, y, h, kind="agnes", hold=None):
        """Stylised peg-doll figure (feet at x, y). Not a portrait of anyone."""
        r = h * 0.1; hy = y + h * 0.75
        sh_y, hem_y = y + h * 0.62, y + h * 0.14
        body = [(x - h * 0.13, sh_y), (x + h * 0.13, sh_y), (x + h * 0.21, hem_y), (x - h * 0.21, hem_y)]
        for sx in (-0.07, 0.07):
            s.line([(x + sx * h, hem_y), (x + sx * h, y + 1)], lw=1.2, amp=0)
            s.shape(s.arcpts(x + sx * h + (h * 0.02 if sx > 0 else -h * 0.02), y + 1, h * 0.04, h * 0.018, 0, 360, 12), lw=0.6, fill=K, amp=0)
        fill_body = K if kind == "ollie" else Wt
        s.shape(body, lw=1.0, fill=fill_body, amp=0.15)
        if kind in ("agnes", "morwenna"):
            s.hatch(body, angle=-55 if kind == "agnes" else 90, gap=2.0 if kind == "agnes" else 2.6, lw=0.35)
        if kind in ("agnes", "jago"):  # apron
            ap = [(x - h * 0.09, sh_y - h * 0.1), (x + h * 0.09, sh_y - h * 0.1), (x + h * 0.14, hem_y + h * 0.04), (x - h * 0.14, hem_y + h * 0.04)]
            s.shape(ap, lw=0.7, fill=Wt, amp=0.1)
            s.line([(x - h * 0.13, sh_y - h * 0.16), (x + h * 0.13, sh_y - h * 0.16)], lw=0.6, amp=0)
            if kind == "agnes":
                s.rect(x - h * 0.05, sh_y - h * 0.3, h * 0.1, h * 0.07, lw=0.5)
        if kind == "ollie":
            for k in range(4): s.circle(x, sh_y - h * 0.08 - k * h * 0.09, h * 0.012 + 0.4, lw=0.4, fill=Wt)
            s.c.setStrokeColor(Wt); s.c.setLineWidth(1.0); s.c.line(x - h * 0.19, hem_y + h * 0.14, x + h * 0.19, hem_y + h * 0.14); s.c.setStrokeColor(K)
        if kind == "hedley":
            s.hatch(body, angle=45, gap=2.4, lw=0.35, cross=True)
        # arms
        if kind == "jago":
            s.rect(x - h * 0.16, sh_y - h * 0.2, h * 0.32, h * 0.07, lw=0.8)
            for i in range(9): s.circle(x + s.r.uniform(-h * 0.17, h * 0.17), sh_y - h * s.r.uniform(0.05, 0.28), 0.45, lw=0, fill=K, stroke=False)
        else:
            for sg in (-1, 1):
                if hold and sg == 1:
                    s.line([(x + sg * h * 0.12, sh_y - 1), (x + sg * h * 0.22, sh_y - h * 0.16), (x + sg * h * 0.3, sh_y - h * 0.12)], lw=1.3, amp=0)
                else:
                    s.line([(x + sg * h * 0.12, sh_y - 1), (x + sg * h * 0.2, sh_y - h * 0.3)], lw=1.3, amp=0)
                    s.circle(x + sg * h * 0.2, sh_y - h * 0.31, h * 0.022, lw=0.5, fill=Wt)
        # head
        s.circle(x, hy, r, lw=1.0, fill=Wt)
        for sx in (-0.35, 0.35): s.circle(x + sx * r, hy + r * 0.05, r * 0.08 + 0.2, lw=0, fill=K, stroke=False)
        s.c.setLineWidth(0.6); s.c.arc(x - r * 0.3, hy - r * 0.55, x + r * 0.3, hy - r * 0.1, 200, 140)
        if kind == "agnes":
            s.blob(s.arcpts(x, hy + r * 0.05, r * 1.04, r * 1.02, 15, 165, 20) + [(x - r * 0.6, hy + r * 0.55), (x + r * 0.6, hy + r * 0.55)], K)
            s.circle(x, hy + r * 1.25, r * 0.42, lw=0.6, fill=K)
            for sx in (-0.38, 0.38): s.circle(x + sx * r, hy + r * 0.05, r * 0.26, lw=0.55, fill=None)
            s.line([(x - r * 0.12, hy + r * 0.08), (x + r * 0.12, hy + r * 0.08)], lw=0.5, amp=0)
        elif kind == "ollie":
            hel = s.arcpts(x, hy + r * 0.5, r * 0.95, r * 1.7, 0, 180, 24)
            s.shape(hel, lw=0.8, fill=K, amp=0)
            s.rect(x - r * 1.15, hy + r * 0.38, r * 2.3, r * 0.22, lw=0.6, fill=K)
            s.star5(x, hy + r * 1.15, r * 0.35, fill=Wt, lw=0.4)
            s.circle(x, hy + r * 2.25, r * 0.15, lw=0.5, fill=K)
        elif kind == "morwenna":
            s.shape(s.arcpts(x, hy + r * 0.6, r * 1.9, r * 0.38, 0, 360, 30), lw=0.8, fill=Wt, amp=0)
            s.shape(s.arcpts(x, hy + r * 0.7, r * 0.9, r * 0.8, 0, 180, 20), lw=0.8, fill=Wt, amp=0)
            s.hatch([(x - r * 0.9, hy + r * 0.7), (x + r * 0.9, hy + r * 0.7), (x + r * 0.9, hy + r * 0.95), (x - r * 0.9, hy + r * 0.95)], angle=0, gap=0.9, lw=0.4)
            s.line([(x - r * 0.95, hy + r * 0.3), (x - r * 1.3, hy - r * 1.6)], lw=1.6, amp=0.2)
            s.line([(x + r * 0.95, hy + r * 0.3), (x + r * 1.3, hy - r * 1.6)], lw=1.6, amp=0.2)
        elif kind == "hedley":
            s.shape(s.arcpts(x, hy + r * 0.25, r * 1.02, r * 0.9, 0, 180, 20), lw=0.8, fill=K, amp=0)
            s.shape([(x + r * 0.2, hy + r * 0.35), (x + r * 1.7, hy + r * 0.3), (x + r * 1.6, hy + r * 0.5), (x + r * 0.3, hy + r * 0.62)], lw=0.6, fill=K, amp=0)
        elif kind == "jago":
            s.rect(x - r * 0.75, hy + r * 0.6, r * 1.5, r * 0.6, lw=0.8)
            for dx in (-0.55, 0.0, 0.55): s.circle(x + dx * r, hy + r * 1.55, r * 0.55, lw=0.8, fill=Wt)
            s.rect(x - r * 0.75, hy + r * 0.6, r * 1.5, r * 0.6, lw=0.8)
        return (x + h * 0.3, sh_y - h * 0.12)

    def cloche(s, x, y, w, num=None, cloth=True):
        """Glass dome on a plate, white cloth over the top, number card in front. Nothing visible inside."""
        s.shape(s.arcpts(x, y, w * 0.62, w * 0.1, 0, 360, 30), lw=0.8, fill=Wt, amp=0)
        dome = s.arcpts(x, y + w * 0.04, w * 0.5, w * 0.62, 0, 180, 30)
        s.shape(dome, lw=0.9, fill=Wt, amp=0)
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
        s.shape([(x - w / 2, y), (x + w / 2, y), (x + w * 0.42, y + h), (x - w * 0.42, y + h)], lw=0.7, fill=Wt, amp=0)
        s.text(x, y + h * 0.22, t, size=h * 0.62, font="Ink-Playfair")

    def table(s, x0, x1, y, depth=8, skirt=26):
        s.shape([(x0, y), (x1, y), (x1 - depth, y + depth), (x0 + depth, y + depth)], lw=0.9, fill=Wt, amp=0)
        sk = [(x0, y), (x1, y), (x1, y - skirt), (x0, y - skirt)]
        s.shape(sk, lw=0.9, fill=Wt, amp=0.1)
        for i in range(1, 14):
            xx = lerp(x0, x1, i / 14); s.line([(xx, y - 1), (xx + s.r.uniform(-1, 1), y - skirt + 1)], lw=0.35, amp=0.3)
        s.line([(lerp(x0, x1, t), y - skirt + 2.5 * abs(math.sin(t * 30))) for t in [i / 80 for i in range(81)]], lw=0.8, amp=0)

    def handbag(s, x, y, w, paper=True):
        h = w * 0.62
        body = [(x - w / 2, y), (x + w / 2, y), (x + w * 0.42, y + h), (x - w * 0.42, y + h)]
        if paper:
            pp = [(x - w * 0.12, y + h * 0.7), (x + w * 0.3, y + h * 0.75), (x + w * 0.26, y + h * 1.45), (x - w * 0.16, y + h * 1.38)]
            s.shape(pp, lw=0.8, fill=Wt, amp=0.1)
            s.line([(x - w * 0.14, y + h * 1.05), (x + w * 0.28, y + h * 1.1)], lw=0.4, amp=0)
            s.c.saveState(); s.c.translate(x + w * 0.07, y + h * 1.24); s.c.rotate(6)
            s.text(0, 0, "ENTRY LIST", size=w * 0.065, font="Ink-Plex"); s.c.restoreState()
            for k in range(3):
                s.line([(x - w * 0.08, y + h * (1.14 - 0.1 * k) + w * 0.01 * k), (x + w * 0.22, y + h * (1.18 - 0.1 * k))], lw=0.3, amp=0.2)
        s.c.setStrokeColor(K); s.c.setLineWidth(3.0); s.c.arc(x - w * 0.28, y + h * 0.5, x + w * 0.28, y + h * 1.5, 0, 180)
        s.shape(body, lw=1.0, fill=Wt, amp=0.1)
        s.hatch([(x + w * 0.15, y), (x + w / 2, y), (x + w * 0.42, y + h), (x + w * 0.1, y + h)], angle=80, gap=1.6, lw=0.35)
        flap = [(x - w * 0.43, y + h)] + s.arcpts(x, y + h, w * 0.43, h * 0.45, 180, 360, 24)[1:]
        s.shape(flap, lw=0.9, fill=K, amp=0)
        s.circle(x, y + h * 0.58, w * 0.045, lw=0.8, fill=Wt)
        s.shape(body, lw=1.0, fill=None, amp=0)

    def plate(s, x, y, w, crumbs=0):
        s.shape(s.arcpts(x, y, w / 2, w * 0.13, 0, 360, 36), lw=0.9, fill=Wt, amp=0)
        s.shape(s.arcpts(x, y + 0.5, w * 0.34, w * 0.08, 0, 360, 36), lw=0.5, fill=None, amp=0)
        for i in range(crumbs):
            a = s.r.uniform(0, 6.28); rr = s.r.uniform(0, 0.3)
            s.circle(x + w * rr * math.cos(a), y + w * 0.08 * rr / 0.3 * math.sin(a), s.r.uniform(0.5, 1.3), lw=0.4, fill=K if i % 3 == 0 else Wt)

    def loaf(s, x, y, w):
        h = w * 0.45
        s.shape(s.arcpts(x, y, w / 2, h, 0, 180, 24) + [(x - w / 2, y)], lw=0.9, fill=Wt, amp=0.1)
        for k in range(3):
            u = -0.25 + 0.25 * k; s.line([(x + u * w - w * 0.06, y + h * 0.45), (x + u * w + w * 0.06, y + h * 0.85)], lw=0.7, amp=0)
        s.hatch([(x + w * 0.1, y)] + [p for p in s.arcpts(x, y, w / 2, h, 0, 70, 10)] + [(x + w * 0.1, y + h * 0.95)], angle=70, gap=1.4, lw=0.3)

    def vase(s, x, y, h):
        w = h * 0.35
        body = [(x - w * 0.35, y), (x + w * 0.35, y), (x + w / 2, y + h * 0.4), (x + w * 0.25, y + h * 0.62), (x - w * 0.25, y + h * 0.62), (x - w / 2, y + h * 0.4)]
        for i in range(9):
            a = math.radians(lerp(55, 125, i / 8)); L = h * s.r.uniform(0.55, 0.85)
            ex, ey = x + L * math.cos(a), y + h * 0.6 + L * math.sin(a) * 0.8
            s.line([(x, y + h * 0.6), (ex, ey)], lw=0.5, amp=0.3)
            for j in range(3):
                s.shape(s.arcpts(ex + s.r.uniform(-2, 2), ey + j * 2.2 - 2, 2.3, 1.7, 0, 360, 10), lw=0.5, fill=Wt if j % 2 else K, amp=0)
        s.shape(body, lw=0.9, fill=Wt, amp=0)
        s.hatch(body, angle=0, gap=2.2, lw=0.35)
        s.shape(body, lw=0.9, fill=None, amp=0)

    def chair_stack(s, x, y, h, n=4):
        w = h * 0.42
        for i in range(n):
            yy = y + i * h * 0.09
            s.line([(x - w / 2, yy), (x - w / 2, yy + h * 0.95)], lw=1.2, amp=0)
            s.line([(x - w / 2, yy + h * 0.45), (x + w / 2, yy + h * 0.45)], lw=1.6, amp=0)
            s.line([(x + w / 2, yy), (x + w / 2, yy + h * 0.45)], lw=1.2, amp=0)
            s.line([(x - w / 2, yy + h * 0.8), (x - w / 2 + 6, yy + h * 0.82)], lw=1.0, amp=0)

    def rosette(s, x, y, r, t="1st"):
        for sg in (-1, 1):
            s.shape([(x + sg * r * 0.15, y), (x + sg * r * 0.55, y - r * 1.8), (x + sg * r * 0.32, y - r * 1.55), (x + sg * r * 0.15, y - r * 1.85), (x - sg * r * 0.15, y)], lw=0.7, fill=K if sg > 0 else Wt, amp=0)
        pts = []
        for i in range(32):
            a = 2 * math.pi * i / 32; rr = r * (1.0 if i % 2 else 0.86)
            pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
        s.shape(pts, lw=0.8, fill=Wt, amp=0)
        s.circle(x, y, r * 0.66, lw=0.8, fill=Wt)
        s.text(x, y - r * 0.22, t, size=r * 0.62, font="Ink-Playfair")

    def bubble(s, x0, y0, x1, y1, tail):
        r = 10
        pts = s.arcpts(x1 - r, y1 - r, r, r, 0, 90, 6) + s.arcpts(x0 + r, y1 - r, r, r, 90, 180, 6) + s.arcpts(x0 + r, y0 + r, r, r, 180, 270, 6)
        tx, ty = tail
        pts += [(x0 + (x1 - x0) * 0.25, y0), (tx, ty), (x0 + (x1 - x0) * 0.4, y0)] + s.arcpts(x1 - r, y0 + r, r, r, 270, 360, 6)
        s.shape(pts, lw=1.2, fill=Wt, amp=0.15)

    def summer_ground(s, x0, x1, y, depth=40):
        pts = s.hills(x0, x1, y, amp=2, n=2)
        s.shape([(x0, y - depth)] + pts + [(x1, y - depth)], lw=0, fill=Wt, stroke=False, amp=0)
        s.line(pts, lw=0.9, amp=0.2)
        for i in range(30):
            gx = s.r.uniform(x0, x1); gy = y - s.r.uniform(2, depth * 0.8)
            for d in (-1, 0, 1): s.line([(gx, gy), (gx + d * 1.4, gy + 3)], lw=0.35, amp=0)

    def frame2(s, w, h, m=10):
        s.c.setStrokeColor(K); s.c.setLineWidth(1.3); s.c.rect(m, m, w - 2 * m, h - 2 * m, stroke=1, fill=0)
        s.c.setLineWidth(0.45); s.c.rect(m + 3.2, m + 3.2, w - 2 * m - 6.4, h - 2 * m - 6.4, stroke=1, fill=0)

# ============================================================================= scenes
def hall_interior(k, w, h, floor=120):
    """Back wall of the village hall with tall windows and bunting."""
    k.rect(14, floor, w - 28, h - floor - 14, lw=0)
    for i in range(3):
        k.window(42 + i * 115, floor + 70, 52, 120, arch=True, lw=0.8)
    k.bunting(14, w - 14, h - 40, sag=16, n=16, size=8)
    k.line([(14, floor), (w - 14, floor)], lw=1.0, amp=0.2)
    k.hatch([(14, 14), (w - 14, 14), (w - 14, floor), (14, floor)], angle=0, gap=5.5, lw=0.35)

def village(k, w, h):
    k.frame2(w, h)
    k.clip_rect(14, 14, w - 14, h - 14)
    for i in range(5): k.gull(k.r.uniform(60, w - 60), k.r.uniform(h * 0.72, h * 0.9), k.r.uniform(10, 18))
    k.circle(w * 0.78, h * 0.86, 22, lw=0.9, fill=Wt)
    for i in range(12):
        a = 2 * math.pi * i / 12; k.line([(w * 0.78 + 27 * math.cos(a), h * 0.86 + 27 * math.sin(a)), (w * 0.78 + 34 * math.cos(a), h * 0.86 + 34 * math.sin(a))], lw=0.8, amp=0)
    # headland + lighthouse
    head = [(14, h * 0.42), (14, h * 0.6), (w * 0.12, h * 0.62), (w * 0.24, h * 0.58), (w * 0.33, h * 0.46), (w * 0.36, h * 0.42)]
    k.shape(head, lw=0.9, fill=Wt, amp=0.4)
    k.hatch(head, angle=-60, gap=2.2, lw=0.4)
    k.lighthouse(w * 0.13, h * 0.615, h * 0.25)
    # sea
    k.waves(14, w - 14, 14, h * 0.4, rows=9)
    k.boat(w * 0.3, h * 0.2, 46); k.boat(w * 0.58, h * 0.32, 30)
    # harbour wall + village hall + cottages
    k.rect(w * 0.36, h * 0.4, w * 0.64, 12, lw=0.9)
    k.hatch([(w * 0.36, h * 0.4), (w - 14, h * 0.4), (w - 14, h * 0.4 + 12), (w * 0.36, h * 0.4 + 12)], angle=0, gap=3, lw=0.35)
    base = h * 0.4 + 12
    xs = [(w * 0.38, 46, 54), (w * 0.52, 76, 82), (w * 0.74, 40, 50), (w * 0.86, 40, 58)]
    for i, (x, cw, chh) in enumerate(xs):
        if i == 1:
            k.wall(x, base, cw, chh * 0.62, gap=2.6)
            k.roof(x, x + cw, base + chh * 0.62, base + chh)
            k.rect(x + cw * 0.12, base + chh * 0.4, cw * 0.76, chh * 0.13, lw=0.6)
            k.text(x + cw / 2, base + chh * 0.43, "VILLAGE HALL", size=chh * 0.075, font="Ink-Plex")
            k.shape([(x + cw * 0.4, base), (x + cw * 0.6, base), (x + cw * 0.6, base + chh * 0.32), (x + cw * 0.4, base + chh * 0.32)], lw=0.7, fill=K, amp=0)
            for u in (0.12, 0.72): k.window(x + cw * u, base + chh * 0.1, cw * 0.16, chh * 0.2)
        else:
            k.cottage(x, base, cw, chh)
    # banner
    bx0, bx1, by = w * 0.4, w * 0.95, base + 92
    k.line([(bx0, base + 60), (bx0, by + 6)], lw=1.0, amp=0); k.line([(bx1, base + 60), (bx1, by + 6)], lw=1.0, amp=0)
    k.rect(bx0 + 20, by - 4, bx1 - bx0 - 40, 20, lw=0.9)
    k.text((bx0 + bx1) / 2, by + 1.5, "SUMMER SHOW", size=12, font="Ink-Playfair")
    k.bunting(bx0, bx0 + 20, by + 10, sag=3, n=2, size=5); k.bunting(bx1 - 20, bx1, by + 10, sag=3, n=2, size=5)
    k.bunting(w * 0.36, w - 14, base + 74, sag=10, n=14, size=6)
    k.unclip()

def tearoom(k, w, h):
    k.frame2(w, h)
    k.clip_rect(14, 14, w - 14, h - 14)
    k.summer_ground(14, w - 14, 70, depth=56)
    x0, x1 = 50, w - 50; yb = 70; top = 300
    k.wall(x0, yb, x1 - x0, top - yb - 60, gap=3.2)
    k.roof(x0, x1, top - 60, top + 20, overhang=8)
    k.chimney(x1 - 70, top - 20, 16, 40)
    # sign board
    k.rect(x0 + 30, top - 92, x1 - x0 - 60, 30, lw=1.0)
    k.text(w / 2, top - 83, "THE KETTLE AND GULL", size=15, font="Ink-Playfair")
    # bay window with cups
    k.rect(x0 + 18, yb + 40, 120, 90, lw=1.0)
    k.c.setLineWidth(0.8)
    for u in (1 / 3, 2 / 3): k.c.line(x0 + 18 + 120 * u, yb + 40, x0 + 18 + 120 * u, yb + 130)
    k.line([(x0 + 18, yb + 70), (x0 + 138, yb + 70)], lw=0.9, amp=0)
    for i in range(3): k.cup(x0 + 38 + i * 40, yb + 74, 18)
    k.teapot(x0 + 78, yb + 100, 26)
    k.rect(x0 + 12, yb + 34, 132, 6, lw=0.8, fill=K)
    # door
    dx = x1 - 110
    k.shape([(dx, yb), (dx + 50, yb), (dx + 50, yb + 100), (dx, yb + 100)], lw=1.0, fill=K, amp=0)
    k.window(dx + 12, yb + 56, 26, 30, lw=0.6)
    k.circle(dx + 42, yb + 46, 2, lw=0.5, fill=Wt)
    # hanging kettle sign + gull
    k.line([(x1 - 6, top - 120), (x1 + 20, top - 120)], lw=1.4, amp=0)
    k.line([(x1 + 12, top - 120), (x1 + 12, top - 130)], lw=0.6, amp=0)
    k.kettle(x1 + 12, top - 152, 18)
    k.gull(w * 0.25, h * 0.9, 18); k.gull(w * 0.4, h * 0.94, 12)
    # Agnes on the step with a teapot
    k.figure(w * 0.47, yb - 4, 120, "agnes", hold=True)
    k.teapot(w * 0.47 + 44, yb + 66, 26)
    k.unclip()

def hall_table(k, w, h):
    k.frame2(w, h)
    k.clip_rect(14, 14, w - 14, h - 14)
    hall_interior(k, w, h, floor=150)
    k.table(30, w - 30, 150, depth=10, skirt=60)
    for i, n in enumerate([3, 4, 5, 6, 7]):
        k.cloche(62 + i * 65, 156, 46, num=n)
    k.unclip()

def handbag_scene(k, w, h):
    k.frame2(w, h)
    k.clip_rect(14, 14, w - 14, h - 14)
    k.table(14, w - 14, 110, depth=14, skirt=100)
    k.handbag(w * 0.42, 124, 190)
    k.cloche(w * 0.84, 124, 70, num=None)
    k.cup(w * 0.13, 124, 40)
    k.unclip()

def plate_scene(k, w, h):
    k.frame2(w, h)
    k.clip_rect(14, 14, w - 14, h - 14)
    hall_interior(k, w, h, floor=160)
    k.table(14, w - 14, 140, depth=14, skirt=128)
    k.plate(w * 0.42, 160, 150, crumbs=14)
    # lifted empty dome to the right, cloth crumpled to the left
    k.cloche(w * 0.8, 152, 80, cloth=False)
    cl = [(40, 150), (100, 152), (112, 172), (90, 190), (60, 186), (38, 168)]
    k.shape(cl, lw=0.9, fill=Wt, amp=0.6)
    for j in range(3): k.line([(50 + j * 16, 156), (64 + j * 12, 182)], lw=0.4, amp=0.4)
    k.card(w * 0.42 + 46, 132, 40, "7")
    k.text(w * 0.42, 260, "?", size=60, font="Ink-Playfair")
    k.unclip()

def lineup(k, w, h):
    """Wide strip: Ollie | Morwenna | Hedley | Jago, each in its own panel (pan target)."""
    k.c.setStrokeColor(K)
    n = 4; pw = w / n
    for i in range(n):
        k.frame2(pw, h) if i == 0 else None
    for i in range(n):
        x0 = i * pw
        k.c.saveState(); k.c.translate(x0, 0)
        k.frame2(pw, h)
        k.clip_rect(14, 14, pw - 14, h - 14)
        hall_interior(k, pw, h, floor=90)
        cx = pw / 2
        if i == 0:
            k.figure(cx - 10, 60, 220, "ollie")
            k.c.saveState(); k.text(cx, 30, "CONSTABLE OLLIE", size=13, font="Ink-Plex"); k.c.restoreState()
        elif i == 1:
            k.rect(cx + 30, 60, 110, 90, lw=0.9)
            k.figure(cx - 40, 60, 200, "morwenna")
            k.vase(cx + 85, 150, 90)
            k.text(cx, 30, "MORWENNA", size=13, font="Ink-Plex")
        elif i == 2:
            k.figure(cx - 40, 60, 200, "hedley")
            k.chair_stack(cx + 70, 60, 120)
            k.text(cx, 30, "HEDLEY", size=13, font="Ink-Plex")
        else:
            k.rect(cx + 30, 60, 110, 70, lw=0.9)
            k.hatch([(cx + 30, 60), (cx + 140, 60), (cx + 140, 130), (cx + 30, 130)], angle=0, gap=4, lw=0.35)
            for j, (dx, dy) in enumerate([(55, 130), (105, 130), (80, 152)]): k.loaf(cx + dx, dy, 44)
            k.figure(cx - 40, 60, 200, "jago")
            k.text(cx, 30, "JAGO THE BAKER", size=13, font="Ink-Plex")
        k.unclip(); k.c.restoreState()

def clue_scene(k, w, h):
    k.frame2(w, h)
    k.clip_rect(14, 14, w - 14, h - 14)
    k.table(14, w - 14, 100, depth=12, skirt=90)
    k.cloche(w * 0.25, 112, 110, num=7)
    k.handbag(w * 0.72, 112, 120)
    k.bubble(40, 250, w - 40, 350, tail=(w * 0.3, 222))
    k.text(w / 2, 316, "\u201c\u2026somebody else\u2019s", size=20, font="Ink-CrimsonI")
    k.text(w / 2, 276, "LEMON DRIZZLE?\u201d", size=30, font="Ink-Playfair")
    k.line([(w / 2 - 120, 268), (w / 2 + 120, 268)], lw=1.4, amp=0.6)
    k.line([(w / 2 - 110, 263), (w / 2 + 116, 264)], lw=0.8, amp=0.6)
    k.unclip()

def van_scene(k, w, h):
    k.frame2(w, h)
    k.clip_rect(14, 14, w - 14, h - 14)
    k.summer_ground(14, w - 14, 70, depth=56)
    x0, x1, yb = 60, 320, 84
    body = [(x0, yb), (x1, yb), (x1, yb + 110), (x0 + 70, yb + 110), (x0 + 40, yb + 70), (x0, yb + 64)]
    k.shape(body, lw=1.1, fill=Wt, amp=0.2)
    k.window(x0 + 46, yb + 72, 26, 30, lw=0.7)
    k.text((x0 + 100 + x1) / 2 - 20, yb + 66, "PENHALLOW", size=16, font="Ink-Playfair")
    k.text((x0 + 100 + x1) / 2 - 20, yb + 48, "BAKERY", size=12, font="Ink-Plex")
    k.loaf((x0 + 100 + x1) / 2 - 20, yb + 18, 40)
    for wx in (x0 + 50, x1 - 50): k.wheel(wx, yb, 20)
    # open rear crate shown in front
    cx = x1 - 30
    k.rect(cx - 90, 30, 130, 50, lw=1.0)
    k.hatch([(cx - 90, 30), (cx + 40, 30), (cx + 40, 80), (cx - 90, 80)], angle=0, gap=6, lw=0.6)
    k.text(cx - 25, 46, "BREAD", size=12, font="Ink-Plex")
    k.loaf(cx - 65, 80, 36); k.loaf(cx + 15, 80, 36)
    k.cake(cx - 25, 82, 34)
    k.unclip()

def prize_scene(k, w, h):
    k.frame2(w, h)
    k.clip_rect(14, 14, w - 14, h - 14)
    hall_interior(k, w, h, floor=150)
    k.table(30, w - 30, 150, depth=10, skirt=60)
    cx = w / 2
    k.shape([(cx - 34, 158), (cx + 34, 158), (cx + 8, 176), (cx - 8, 176)], lw=0.9, fill=Wt, amp=0)
    k.cake(cx, 178, 120)
    for i in range(8):  # lemon drizzle drips
        dx = lerp(-52, 52, i / 7); L = k.r.uniform(8, 22)
        k.line([(cx + dx, 244), (cx + dx + 1, 244 - L)], lw=2.0, amp=0); k.circle(cx + dx + 1, 244 - L, 1.8, lw=0.4, fill=Wt)
    for i in range(3):
        k.shape(k.arcpts(cx - 30 + i * 30, 252, 9, 3, 0, 360, 12), lw=0.6, fill=Wt, amp=0)
        k.c.setLineWidth(0.4); k.c.line(cx - 39 + i * 30, 252, cx - 21 + i * 30, 252)
    k.rosette(cx + 92, 196, 22)
    k.card(cx - 84, 160, 40, "7")
    k.unclip()

def title_vignette(k, w, h):
    """Small round vignette for the title card: teapot and cup, gull, lighthouse."""
    k.circle(w / 2, h / 2, w * 0.46, lw=1.3, fill=Wt); k.circle(w / 2, h / 2, w * 0.44, lw=0.45, fill=None)
    k.c.saveState(); p = k.c.beginPath(); p.circle(w / 2, h / 2, w * 0.44 - 1); k.c.clipPath(p, stroke=0, fill=0)
    k.waves(0, w, h * 0.06, h * 0.36, rows=6)
    k.lighthouse(w * 0.2, h * 0.38, h * 0.3)
    k.gull(w * 0.62, h * 0.76, 22); k.gull(w * 0.76, h * 0.7, 14)
    k.rect(w * 0.3, h * 0.36, w * 0.6, 10, lw=0.9)
    k.teapot(w * 0.52, h * 0.39, 90)
    k.cup(w * 0.78, h * 0.39, 44)
    k.c.restoreState()

SCENES = dict(village=(village, 1, 1), tearoom=(tearoom, 1, 1), hall=(hall_table, 1, 1), handbag=(handbag_scene, 1, 1),
              plate=(plate_scene, 1, 1), lineup=(lineup, 4, 1), clue=(clue_scene, 1, 1), van=(van_scene, 1, 1),
              prize=(prize_scene, 1, 1), vignette=(title_vignette, 1, 1))

if __name__ == "__main__":
    import sys
    inkart.Ink = Sea
    os.makedirs(OUT, exist_ok=True)
    want = sys.argv[1:] or list(SCENES)
    for i, name in enumerate(want):
        fn, wx, hy = SCENES[name]
        def draw(ink, W, H, fn=fn):
            k = Sea(ink.c, seed=7 + i); fn(k, W, H)
        render(os.path.join(OUT, name + ".png"), S * wx / 72, S * hy / 72, draw, seed=7 + i)
        print(name)
