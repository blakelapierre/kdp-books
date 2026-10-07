"""inkart: procedural black-and-white ink / line-art illustrations for the KDP books.

Everything is drawn with pure black and white vector strokes and fills (no gray washes),
then rasterised at 300 DPI to a clean grayscale PNG (see render()). The same file is copied
into each book's src/ folder so every book folder stays self-contained."""
import os
import math, random, subprocess, tempfile
from reportlab.pdfgen import canvas as rlcanvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

K = colors.black
Wt = colors.white
_GF = os.environ.get("TIDEWHISTLE_FONTS", "/usr/share/fonts/truetype/sand-box/google/").rstrip("/") + "/"
for _n, _p in [("Ink-Playfair", "Playfair Display SC/PlayfairDisplaySC-Bold.ttf"),
               ("Ink-PlayfairR", "Playfair Display SC/PlayfairDisplaySC-Regular.ttf"),
               ("Ink-Crimson", "Crimson Text/CrimsonText-Regular.ttf"),
               ("Ink-CrimsonI", "Crimson Text/CrimsonText-Italic.ttf"),
               ("Ink-Plex", "IBM Plex Sans Condensed/IBMPlexSansCondensed-SemiBold.ttf")]:
    try: pdfmetrics.registerFont(TTFont(_n, _GF + _p))
    except Exception: pass

# ----------------------------------------------------------------------------- rendering
def render(path, w_in, h_in, fn, seed=1, dpi=300):
    """Draw fn(ink, w_pt, h_pt) on a w_in x h_in canvas and save a clean 300 DPI grayscale PNG."""
    from PIL import Image
    tmpd = tempfile.mkdtemp()
    pdf = os.path.join(tmpd, "a.pdf")
    c = rlcanvas.Canvas(pdf, pagesize=(w_in * 72, h_in * 72))
    ink = Ink(c, seed)
    fn(ink, w_in * 72, h_in * 72)
    c.showPage(); c.save()
    subprocess.run(["pdftoppm", "-r", str(dpi), "-gray", "-png", "-singlefile", pdf, os.path.join(tmpd, "a")], check=True)
    im = Image.open(os.path.join(tmpd, "a.png")).convert("L")
    # levels: snap paper to pure white and ink to pure black; keep only a thin anti-aliased edge
    lut = [255 if v >= 200 else 0 if v <= 70 else int((v - 70) * 255 / 130) for v in range(256)]
    im = im.point(lut)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    im.save(path, dpi=(dpi, dpi), optimize=True)
    return path

# ----------------------------------------------------------------------------- helpers
def lerp(a, b, t): return a + (b - a) * t

class Ink:
    def __init__(s, c, seed=1):
        s.c = c; s.r = random.Random(seed); s.taper = True
        s.c.setLineCap(1); s.c.setLineJoin(1)

    # --- basic stroking -------------------------------------------------------
    def noise(s):
        ph = [s.r.uniform(0, 6.28) for _ in range(3)]; fr = [s.r.uniform(0.05, 0.09), s.r.uniform(0.15, 0.25), s.r.uniform(0.4, 0.6)]
        return lambda t: 0.6 * math.sin(fr[0] * t + ph[0]) + 0.3 * math.sin(fr[1] * t + ph[1]) + 0.1 * math.sin(fr[2] * t + ph[2])

    def wob(s, pts, amp=0.35, step=2.5, closed=False):
        """Densify a polyline and add a gentle hand-drawn wobble perpendicular to it."""
        if closed: pts = list(pts) + [pts[0]]
        out = []; nz = s.noise(); dist = 0
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            L = math.hypot(x1 - x0, y1 - y0); n = max(1, int(L / step))
            nx, ny = (-(y1 - y0) / L, (x1 - x0) / L) if L else (0, 0)
            for i in range(n):
                t = i / n; d = amp * nz(dist + L * t)
                out.append((lerp(x0, x1, t) + nx * d, lerp(y0, y1, t) + ny * d))
            dist += L
        out.append(pts[-1] if not closed else out[0])
        return out

    def path(s, pts, closed=False):
        p = s.c.beginPath(); p.moveTo(*pts[0])
        for q in pts[1:]: p.lineTo(*q)
        if closed: p.close()
        return p

    def line(s, pts, lw=0.8, amp=0.3, color=K):
        s.c.setStrokeColor(color); s.c.setLineWidth(lw)
        s.c.drawPath(s.path(s.wob(pts, amp) if amp else pts), stroke=1, fill=0)

    def shape(s, pts, lw=0.8, fill=Wt, stroke=True, amp=0.3):
        q = s.wob(pts, amp, closed=True) if amp else list(pts)
        s.c.setStrokeColor(K); s.c.setLineWidth(lw)
        if fill is not None: s.c.setFillColor(fill)
        s.c.drawPath(s.path(q, closed=True), stroke=1 if stroke else 0, fill=1 if fill is not None else 0)
        return q

    def blob(s, pts, fill=K):
        s.c.setFillColor(fill); s.c.drawPath(s.path(pts, closed=True), stroke=0, fill=1)

    def circle(s, x, y, r, lw=0.8, fill=Wt, stroke=True):
        s.c.setStrokeColor(K); s.c.setLineWidth(lw)
        if fill is not None: s.c.setFillColor(fill)
        s.c.circle(x, y, r, stroke=1 if stroke else 0, fill=1 if fill is not None else 0)

    def arcpts(s, cx, cy, rx, ry, a0, a1, n=40):
        return [(cx + rx * math.cos(math.radians(lerp(a0, a1, i / n))), cy + ry * math.sin(math.radians(lerp(a0, a1, i / n)))) for i in range(n + 1)]

    def hatch(s, region, angle=-55, gap=2.4, lw=0.45, jitter=0.25, cross=False):
        """Ink hatching clipped to a polygon region."""
        c = s.c; c.saveState()
        c.clipPath(s.path(region, closed=True), stroke=0, fill=0)
        xs = [p[0] for p in region]; ys = [p[1] for p in region]
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        R = math.hypot(max(xs) - min(xs), max(ys) - min(ys)) / 2 + 2
        c.setStrokeColor(K); c.setLineWidth(lw)
        for ang in ([angle, angle + 90] if cross else [angle]):
            a = math.radians(ang); dx, dy = math.cos(a), math.sin(a); nx, ny = -dy, dx
            k = -R
            while k <= R:
                o = k + s.r.uniform(-jitter, jitter)
                x0, y0 = cx + nx * o - dx * R, cy + ny * o - dy * R
                x1, y1 = cx + nx * o + dx * R, cy + ny * o + dy * R
                c.line(x0, y0, x1, y1); k += gap
        c.restoreState()

    def text(s, x, y, t, size=10, font="Ink-Playfair", align="c", color=K):
        s.c.setFillColor(color); s.c.setFont(font, size)
        {"c": s.c.drawCentredString, "l": s.c.drawString, "r": s.c.drawRightString}[align](x, y, t)

    # --- sky -------------------------------------------------------------------
    def sparkle(s, x, y, r, fill=K):
        pts = []
        for i in range(8):
            a = math.pi / 4 * i; rr = r if i % 2 == 0 else r * 0.22
            pts.append((x + rr * math.cos(a + math.pi / 2), y + rr * math.sin(a + math.pi / 2)))
        s.blob(pts, fill)

    def flake(s, x, y, r, lw=None, color=K):
        c = s.c; c.saveState(); c.setStrokeColor(color); c.setLineWidth(lw or max(0.35, r * 0.13))
        for i in range(6):
            a = math.pi / 3 * i + math.pi / 6
            c.line(x, y, x + r * math.cos(a), y + r * math.sin(a))
            bx, by = x + r * 0.55 * math.cos(a), y + r * 0.55 * math.sin(a)
            for sg in (-1, 1):
                b = a + sg * math.pi / 4; c.line(bx, by, bx + r * 0.3 * math.cos(b), by + r * 0.3 * math.sin(b))
        c.restoreState()

    def stars(s, x0, y0, x1, y1, n=30, big=0.15, rmax=3.2, avoid=None):
        for i in range(n):
            for _ in range(20):
                x, y = s.r.uniform(x0, x1), s.r.uniform(y0, y1)
                if not avoid or not avoid(x, y): break
            else: continue
            u = s.r.random()
            if u < big: s.sparkle(x, y, s.r.uniform(rmax * 0.6, rmax))
            elif u < 0.55: s.circle(x, y, s.r.uniform(0.35, 0.7), fill=K, stroke=False)
            else: s.sparkle(x, y, s.r.uniform(0.9, 1.6))

    def snowfall(s, x0, y0, x1, y1, n=40, avoid=None, rmin=0.6, rmax=1.4):
        for i in range(n):
            x, y = s.r.uniform(x0, x1), s.r.uniform(y0, y1)
            if avoid and avoid(x, y): continue
            if s.r.random() < 0.18: s.flake(x, y, s.r.uniform(1.8, 3.0), lw=0.4)
            else: s.circle(x, y, s.r.uniform(rmin, rmax), lw=0.45, fill=Wt)

    def moon(s, x, y, r, phase=0.35):
        s.circle(x, y, r, lw=0.9, fill=Wt)
        reg = s.arcpts(x, y, r, r, 90, 270, 40) + s.arcpts(x, y, r * phase, r, 270, 90, 40)
        s.hatch(reg, angle=30, gap=1.3, lw=0.42, jitter=0.05)
        s.circle(x, y, r, lw=0.9, fill=None)
        for (dx, dy, cr) in [(0.35, 0.3, 0.12), (0.2, -0.4, 0.09), (0.6, -0.1, 0.07)]:
            s.circle(x + dx * r, y + dy * r, cr * r, lw=0.4, fill=None)

    def constellation(s, pts, r=1.8):
        s.c.setDash(1, 1.6); s.line(pts, lw=0.4, amp=0)
        s.c.setDash()
        for (x, y) in pts: s.sparkle(x, y, r)

    # --- terrain ---------------------------------------------------------------
    def ridge(s, x0, x1, base, peaks, rough=1.2):
        """peaks: list of (x, y) apexes; returns jagged ridge polyline from x0 to x1."""
        pts = [(x0, base + (peaks[0][1] - base) * (0.0 if s.taper else 0.35))]
        for i, (px, py) in enumerate(peaks):
            pts.append((px, py))
            nxp = peaks[i + 1] if i + 1 < len(peaks) else (x1, base + (py - base) * 0.3)
            vx = lerp(px, nxp[0], s.r.uniform(0.4, 0.6)); vy = lerp(base, min(py, nxp[1]), s.r.uniform(0.45, 0.65))
            pts.append((vx, vy))
        pts[-1] = (x1, base if s.taper else pts[-1][1])
        # jag
        out = []
        for (a, b) in zip(pts, pts[1:]):
            n = max(2, int(abs(b[0] - a[0]) / 5))
            for i in range(n):
                t = i / n; out.append((lerp(a[0], b[0], t), lerp(a[1], b[1], t) + (s.r.uniform(-rough, rough) if 0 < i else 0)))
        out.append(pts[-1])
        return out, pts

    def mountains(s, x0, x1, base, peaks, cap=0.3, gap=2.0, lw=0.9):
        rid, key = s.ridge(x0, x1, base, peaks)
        poly = [(x0, base)] + rid + [(x1, base)]
        s.shape(poly, lw=lw, fill=Wt, amp=0)
        for i in range(1, len(key) - 1, 2):
            px, py = key[i]; vx, vy = key[i + 1]
            fl = [p for p in rid if px <= p[0] <= vx]
            if len(fl) < 2: continue
            fx = px + (vx - px) * 0.12; fy = base + (py - base) * 0.05
            capy = py - (py - base) * cap
            # ragged snow line from the fall line across to the flank
            cl = [(lerp(px, fx, (py - capy) / (py - fy)) , capy)]
            for j in range(1, 6):
                t = j / 6; xx = lerp(cl[0][0], lerp(px, vx, 0.5), t)
                cl.append((xx, capy - (py - base) * 0.12 * t + s.r.uniform(-3, 3)))
            fl2 = [p for p in fl if p[0] >= cl[-1][0]]
            reg = cl + fl2 + [(fx, fy)]
            s.hatch(reg, angle=-60 if True else 0, gap=gap, lw=0.42)
            # a couple of gully lines
            for g in range(2):
                gx = lerp(px, vx, s.r.uniform(0.2, 0.6)); gy = lerp(py, vy, (gx - px) / max(1, vx - px)) - 3
                s.line([(gx, gy), (gx - 4, gy - (py - base) * 0.18), (gx - 2, gy - (py - base) * 0.32)], lw=0.4, amp=0.3)
        s.line(rid, lw=lw, amp=0)
        return rid

    def hills(s, x0, x1, y, amp=6, n=3, lw=0.8, fill=Wt):
        ph = s.r.uniform(0, 6)
        pts = [(x, y + amp * math.sin(ph + (x - x0) / (x1 - x0) * math.pi * n) * 0.6 + amp * 0.4 * math.sin(ph * 2 + (x - x0) / (x1 - x0) * math.pi * n * 2.3))
               for x in [lerp(x0, x1, i / 80) for i in range(81)]]
        return pts

    def ground(s, x0, x1, y, lw=0.9, drifts=4, ticks=True, depth=40):
        pts = s.hills(x0, x1, y, amp=3, n=2)
        s.shape([(x0, y - depth)] + pts + [(x1, y - depth)], lw=0, fill=Wt, stroke=False, amp=0)
        s.line(pts, lw=lw, amp=0.2)
        for i in range(drifts):
            xa = s.r.uniform(x0, x1 - 30); L = s.r.uniform(18, 50); yy = y - s.r.uniform(5, depth * 0.7)
            arc = [(xa + L * t, yy + 2.5 * math.sin(math.pi * t)) for t in [i / 12 for i in range(13)]]
            s.line(arc, lw=0.5, amp=0.15)
            if ticks:
                for j in range(4):
                    tx = xa + L * (0.2 + 0.2 * j); s.line([(tx, yy - 1), (tx - 1.5, yy - 3.5)], lw=0.35, amp=0)
        return pts

    # --- trees -----------------------------------------------------------------
    def pine(s, x, y, h, style="solid", snow=True, tiers=None, lw=0.7):
        """Snowy fir. style 'solid' = black silhouette with snow-laden white tier tops; 'line' = outline + hatched shade."""
        r = s.r; tiers = tiers or max(3, min(6, int(h / 11) + 2))
        w = h * 0.5; trunk = h * 0.08; top = y + h
        polys = []
        for k in range(tiers):
            t0 = k / tiers; t1 = (k + 1.35) / tiers
            yt = top - (h - trunk) * t0 * 0.9; yb = top - (h - trunk) * min(1.0, t1)
            hw = w * (0.22 + 0.78 * min(1.0, t1)) / 2
            pts = [(x, yt + (h * 0.02 if k == 0 else 0))]
            for u in (0.35, 0.7):
                pts.append((x - hw * u * 0.95, lerp(yt, yb, u * 0.92)))
            pts.append((x - hw, yb - h * 0.012))
            teeth = 2 + min(3, k)
            for j in range(1, teeth * 2):
                xx = lerp(x - hw, x + hw, j / (teeth * 2))
                pts.append((xx + r.uniform(-0.3, 0.3), yb + (h * 0.03 if j % 2 else -h * 0.004)))
            pts.append((x + hw, yb - h * 0.012))
            for u in (0.7, 0.35):
                pts.append((x + hw * u * 0.95, lerp(yt, yb, u * 0.92)))
            polys.append((s.wob(pts, 0.15, closed=True), yt, yb, hw))
        c = s.c
        if style == "solid":
            c.setFillColor(K); c.rect(x - h * 0.03, y, h * 0.06, trunk + 2, stroke=0, fill=1)
            for q, yt, yb, hw in reversed(polys):
                s.blob(q, K)
                if snow:
                    c.saveState(); c.clipPath(s.path(q, closed=True), stroke=0, fill=0)
                    cut = lerp(yt, yb, r.uniform(0.42, 0.55))
                    wav = [(lerp(x - hw * 1.1, x + hw * 1.1, i / 10), cut + (yt - yb) * 0.1 * math.sin(i * 1.7 + r.uniform(0, 1)) + (yt - yb) * 0.12 * (i / 10 - 0.5))
                           for i in range(11)]
                    s.blob([(x - hw * 1.2, yt + 5)] + wav + [(x + hw * 1.2, yt + 5)], Wt)
                    c.restoreState()
                    c.setStrokeColor(K); c.setLineWidth(lw * 0.9); c.drawPath(s.path(q, closed=True), stroke=1, fill=0)
        else:
            for q, yt, yb, hw in reversed(polys):
                s.blob(q, Wt)
                s.hatch([(x + hw * 0.08, yt)] + [(px, py) for (px, py) in q if px >= x + hw * 0.08] + [(x + hw * 0.08, yb - 2)], angle=-62, gap=1.8, lw=0.35)
                c.setStrokeColor(K); c.setLineWidth(lw); c.drawPath(s.path(q, closed=True), stroke=1, fill=0)
            c.setFillColor(K); c.rect(x - h * 0.025, y, h * 0.05, trunk + 1, stroke=0, fill=1)

    def forest(s, x0, x1, y, hmin, hmax, n, style="solid", seedshift=0):
        for _ in range(n):
            hh = s.r.uniform(hmin, hmax); m = hh * 0.27
            x = s.r.uniform(x0 + m, x1 - m) if x1 - x0 > 2 * m else (x0 + x1) / 2
            s.pine(x, y + s.r.uniform(-1.5, 1.5), hh, style=style)

    # --- buildings -------------------------------------------------------------
    def window(s, x, y, w, h, lit=True, arch=False, lw=0.6):
        pts = [(x, y), (x + w, y), (x + w, y + h)] + ([(x + w / 2 + w / 2 * math.cos(math.radians(a)), y + h + w / 2 * math.sin(math.radians(a))) for a in range(0, 181, 15)] if arch else []) + [(x, y + h)]
        s.shape(pts, lw=lw, fill=Wt if lit else K, amp=0)
        s.c.setStrokeColor(K if lit else Wt); s.c.setLineWidth(lw * 0.7)
        s.c.line(x + w / 2, y, x + w / 2, y + h + (w / 2 if arch else 0)); s.c.line(x, y + h * 0.55, x + w, y + h * 0.55)
        s.c.setStrokeColor(K); s.c.setLineWidth(lw * 1.4); s.c.line(x - 1, y - 0.6, x + w + 1, y - 0.6)

    def roof(s, x0, x1, ybase, ypeak, overhang=4, snow=3.0, lw=0.9):
        """Snow-covered gable roof: white snow slab with icicles under the eaves."""
        xm = (x0 + x1) / 2
        pts = [(x0 - overhang, ybase), (xm, ypeak), (x1 + overhang, ybase)]
        slab = [(x0 - overhang - 1, ybase - 0.5), (xm, ypeak + snow), (x1 + overhang + 1, ybase - 0.5), (x1 + overhang - 1, ybase - snow * 0.8), (xm, ypeak - snow * 0.5), (x0 - overhang + 1, ybase - snow * 0.8)]
        # soffit shadow
        s.blob([(x0 - overhang + 1, ybase - snow * 0.8), (xm, ypeak - snow * 0.5), (x1 + overhang - 1, ybase - snow * 0.8), (x1 + overhang - 3, ybase - snow * 1.8), (xm, ypeak - snow * 1.6), (x0 - overhang + 3, ybase - snow * 1.8)], K)
        s.shape(slab, lw=lw, fill=Wt, amp=0.2)
        # icicles
        for side in (0, 1):
            for j in range(1, 7):
                t = j / 7
                ex = lerp(x0 - overhang + 2, xm, t) if side == 0 else lerp(x1 + overhang - 2, xm, t)
                ey = lerp(ybase - snow * 1.8, ypeak - snow * 1.6, t)
                L = s.r.uniform(1.5, 4)
                s.blob([(ex - 0.7, ey), (ex + 0.7, ey), (ex, ey - L)], K)

    def wall(s, x, y, w, h, boards=True, gap=3.0, lw=0.9):
        s.shape([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], lw=lw, fill=Wt, amp=0.15)
        if boards: s.hatch([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], angle=0, gap=gap, lw=0.35, jitter=0.15)

    def chimney(s, x, y, w, h, smoke=True):
        s.shape([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], lw=0.8, fill=Wt, amp=0)
        s.hatch([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], angle=0, gap=1.6, lw=0.35, cross=False)
        s.shape([(x - 1.2, y + h), (x + w + 1.2, y + h), (x + w + 1.2, y + h + 2.2), (x - 1.2, y + h + 2.2)], lw=0.7, fill=Wt, amp=0)
        if smoke: s.smoke(x + w / 2, y + h + 3, 22, curl=1)

    def smoke(s, x, y, L, curl=1, lw=0.55):
        pts = []
        for i in range(40):
            t = i / 39; pts.append((x + curl * L * 0.5 * t + 3 * math.sin(t * 7) * t, y + L * t))
        s.line(pts, lw=lw, amp=0)
        pts2 = [(px + 2.2 + 1.2 * math.sin(i * 0.3), py + 1) for i, (px, py) in enumerate(pts[6:])]
        s.line(pts2, lw=lw * 0.7, amp=0)

    def lodge(s, x, y, w, h, tower=False, dome=False, sign=None):
        """The Frostwood Lodge: a big timber chalet with a central gable, wings and a porch."""
        wing = w * 0.3; cw = w - 2 * wing
        if tower or dome:
            tw = wing * 0.42; tx = x + wing * 0.5 - tw / 2
            s.wall(tx, y + h * 0.5, tw, h * 0.52, gap=2.4)
            s.window(tx + tw * 0.3, y + h * 0.84, tw * 0.4, h * 0.1, arch=True)
            s.observatory(tx + tw / 2, y + h * 1.02, tw * 1.25)
        # wings
        for wx in (x, x + w - wing):
            s.wall(wx, y, wing, h * 0.55)
            s.roof(wx, wx + wing, y + h * 0.55, y + h * 0.82, overhang=3)
            for j in range(2):
                for i in range(2):
                    s.window(wx + wing * (0.2 + 0.4 * i), y + h * (0.08 + 0.24 * j), wing * 0.2, h * 0.13)
        # centre
        cx = x + wing
        s.wall(cx, y, cw, h * 0.75)
        s.roof(cx, cx + cw, y + h * 0.75, y + h * 1.12, overhang=4)
        s.window(cx + cw / 2 - cw * 0.08, y + h * 0.82, cw * 0.16, h * 0.09, arch=True)
        for i in range(3):
            s.window(cx + cw * (0.14 + 0.28 * i), y + h * 0.45, cw * 0.16, h * 0.15)
        # door + porch
        dw = cw * 0.24
        s.shape([(cx + cw / 2 - dw / 2, y), (cx + cw / 2 + dw / 2, y), (cx + cw / 2 + dw / 2, y + h * 0.28)] + s.arcpts(cx + cw / 2, y + h * 0.28, dw / 2, dw / 2, 0, 180, 12)[1:-1] + [(cx + cw / 2 - dw / 2, y + h * 0.28)], lw=0.8, fill=K, amp=0)
        s.c.setStrokeColor(Wt); s.c.setLineWidth(0.5); s.c.line(cx + cw / 2, y + 1, cx + cw / 2, y + h * 0.28 + dw / 2 - 1)
        s.circle(cx + cw / 2 - dw / 2 - 4, y + h * 0.25, 1.8, lw=0.5, fill=Wt)
        s.circle(cx + cw / 2 + dw / 2 + 4, y + h * 0.25, 1.8, lw=0.5, fill=Wt)
        s.chimney(cx + cw * 0.78, y + h * 0.9, cw * 0.07, h * 0.3)
        if sign:
            s.signpost(x - w * 0.08, y - 2, w * 0.2, sign)

    def observatory(s, x, y, w):
        """Small dome on a drum, shutter slit open, telescope peeking out."""
        h = w * 0.35
        s.shape([(x - w / 2, y), (x + w / 2, y), (x + w / 2, y + h), (x - w / 2, y + h)], lw=0.8, fill=Wt, amp=0)
        s.hatch([(x - w / 2, y), (x + w / 2, y), (x + w / 2, y + h), (x - w / 2, y + h)], angle=90, gap=2, lw=0.35)
        dome = s.arcpts(x, y + h, w / 2 + 1, w / 2 * 0.9, 0, 180, 30)
        s.shape(dome, lw=0.9, fill=Wt, amp=0)
        s.hatch([p for p in dome if p[0] >= x + w * 0.1] + [(x + w * 0.1, y + h)], angle=-60, gap=1.8, lw=0.35)
        s.shape(dome, lw=0.9, fill=None, amp=0)
        s.blob([(x - w * 0.07, y + h + 1), (x + w * 0.07, y + h + 1), (x + w * 0.05, y + h + w * 0.44), (x - w * 0.05, y + h + w * 0.44)], K)
        ang = math.radians(62); L = w * 0.55
        bx, by = x, y + h + w * 0.28
        s.c.setStrokeColor(K); s.c.setLineWidth(w * 0.09); s.c.setLineCap(0)
        s.c.line(bx, by, bx + L * math.cos(ang), by + L * math.sin(ang)); s.c.setLineCap(1)

    def cabin(s, x, y, w, h, lit=True):
        s.wall(x, y, w, h * 0.62, gap=2.6)
        s.roof(x, x + w, y + h * 0.62, y + h, overhang=3.5)
        s.window(x + w * 0.16, y + h * 0.2, w * 0.2, h * 0.2)
        s.shape([(x + w * 0.58, y), (x + w * 0.8, y), (x + w * 0.8, y + h * 0.42), (x + w * 0.58, y + h * 0.42)], lw=0.8, fill=K, amp=0)
        s.chimney(x + w * 0.7, y + h * 0.8, w * 0.1, h * 0.3)

    # --- railway ---------------------------------------------------------------
    def rails(s, x0, x1, y, ties=True):
        s.c.setStrokeColor(K); s.c.setLineWidth(1.0); s.c.line(x0, y, x1, y)
        s.c.setLineWidth(0.5); s.c.line(x0, y - 2.3, x1, y - 2.3)
        if ties:
            x = x0
            while x < x1:
                s.c.setLineWidth(1.6); s.c.line(x, y - 3.4, x + 3.2, y - 3.4); x += 7

    def wheel(s, x, y, r, spokes=8):
        s.circle(x, y, r, lw=0.9, fill=Wt)
        s.circle(x, y, r * 0.78, lw=0.5, fill=None)
        s.c.setLineWidth(0.45)
        for i in range(spokes):
            a = math.pi * 2 * i / spokes; s.c.line(x, y, x + r * 0.78 * math.cos(a), y + r * 0.78 * math.sin(a))
        s.circle(x, y, r * 0.18, lw=0.5, fill=K)

    def locomotive(s, x, y, L, facing=1, smoke=True):
        """Small steam engine with snowplough. (x, y) = rail level at the rear; L = length."""
        f = facing; X = lambda u: x + f * u * L
        H = L * 0.62
        def box(u0, u1, v0, v1, fill=Wt, lw=0.9):
            return s.shape([(X(u0), y + v0 * H), (X(u1), y + v0 * H), (X(u1), y + v1 * H), (X(u0), y + v1 * H)], lw=lw, fill=fill, amp=0.1)
        # frame
        box(0.0, 0.92, 0.12, 0.2, fill=K)
        # cab
        box(0.0, 0.3, 0.2, 0.86)
        s.hatch([(X(0.0), y + 0.2 * H), (X(0.3), y + 0.2 * H), (X(0.3), y + 0.86 * H), (X(0.0), y + 0.86 * H)], angle=90, gap=2.2, lw=0.35)
        s.window(min(X(0.07), X(0.23)), y + 0.5 * H, abs(X(0.23) - X(0.07)), 0.22 * H, lw=0.7)
        box(-0.03, 0.33, 0.86, 0.93, fill=K)
        # boiler
        box(0.3, 0.86, 0.22, 0.6)
        s.hatch([(X(0.3), y + 0.22 * H), (X(0.86), y + 0.22 * H), (X(0.86), y + 0.34 * H), (X(0.3), y + 0.34 * H)], angle=0, gap=1.4, lw=0.4)
        for u in (0.45, 0.6, 0.75): s.c.setLineWidth(0.6); s.c.line(X(u), y + 0.22 * H, X(u), y + 0.6 * H)
        box(0.86, 0.92, 0.2, 0.62, fill=K)
        # dome + stack
        s.shape(s.arcpts(X(0.55), y + 0.6 * H, L * 0.06, H * 0.12, 0, 180, 16), lw=0.8, fill=Wt, amp=0)
        stack = [(X(0.74), y + 0.6 * H), (X(0.82), y + 0.6 * H), (X(0.85), y + 0.9 * H), (X(0.71), y + 0.9 * H)]
        s.shape(stack, lw=0.8, fill=K, amp=0)
        # headlamp
        s.shape([(X(0.88), y + 0.62 * H), (X(0.95), y + 0.62 * H), (X(0.95), y + 0.72 * H), (X(0.88), y + 0.72 * H)], lw=0.6, fill=Wt, amp=0)
        # plough
        s.shape([(X(0.92), y + 0.2 * H), (X(1.08), y + 0.01 * H), (X(0.92), y + 0.01 * H)], lw=0.8, fill=Wt, amp=0)
        s.hatch([(X(0.92), y + 0.2 * H), (X(1.08), y + 0.01 * H), (X(0.92), y + 0.01 * H)], angle=60 * f, gap=1.6, lw=0.35)
        # wheels
        for u in (0.36, 0.52, 0.68): s.wheel(X(u), y + 0.11 * H, 0.11 * H)
        s.wheel(X(0.85), y + 0.07 * H, 0.07 * H, spokes=6); s.wheel(X(0.12), y + 0.07 * H, 0.07 * H, spokes=6)
        s.c.setLineWidth(1.4); s.c.line(X(0.36), y + 0.08 * H, X(0.68), y + 0.08 * H)
        if smoke: s.plume(X(0.78), y + 0.95 * H, L * 0.9, f, H * 0.11)

    def plume(s, x, y, L, f=1, r0=4):
        """Billowing smoke drifting back and up from the chimney: clusters of puffs that grow as they rise."""
        puffs = []
        for i in range(6):
            t = i / 5; px = x - f * L * t; py = y + r0 + L * 0.3 * t ** 0.8 + r0 * 0.8 * math.sin(t * 6)
            r = r0 * (0.75 + 1.5 * t)
            puffs.append((px, py, r))
            for j in range(2):
                a = s.r.uniform(0, 6.28); puffs.append((px + math.cos(a) * r * 0.7, py + abs(math.sin(a)) * r * 0.55, r * s.r.uniform(0.55, 0.75)))
        for (px, py, r) in reversed(puffs):
            s.circle(px, py, r, lw=0.6, fill=Wt)
        for (px, py, r) in puffs[::3]:
            s.c.setLineWidth(0.35); s.c.arc(px - r * 0.55, py - r * 0.55, px + r * 0.55, py + r * 0.55, 200, 70)

    def carriage(s, x, y, L, facing=1, n_win=5):
        f = facing; X = lambda u: x + f * u * L; H = L * 0.5
        body = [(X(0.03), y + 0.18 * H), (X(0.97), y + 0.18 * H), (X(0.97), y + 0.85 * H), (X(0.03), y + 0.85 * H)]
        s.shape(body, lw=0.9, fill=Wt, amp=0.1)
        s.hatch([(X(0.03), y + 0.18 * H), (X(0.97), y + 0.18 * H), (X(0.97), y + 0.34 * H), (X(0.03), y + 0.34 * H)], angle=90, gap=1.8, lw=0.35)
        rf = [(X(0.0), y + 0.85 * H), (X(1.0), y + 0.85 * H), (X(0.95), y + 0.98 * H), (X(0.05), y + 0.98 * H)]
        s.shape(rf, lw=0.8, fill=Wt, amp=0.1)
        s.line([(X(0.05), y + 1.01 * H), (X(0.3), y + 1.03 * H), (X(0.6), y + 1.01 * H), (X(0.95), y + 1.02 * H)], lw=0.6, amp=0.4)
        for i in range(n_win):
            u = 0.1 + 0.8 * i / max(1, n_win - 1) - 0.05
            xa, xb = sorted([X(u), X(u + 0.1)])
            s.window(xa, y + 0.45 * H, xb - xa, 0.3 * H, lw=0.6)
        for u in (0.15, 0.27, 0.73, 0.85): s.wheel(X(u), y + 0.1 * H, 0.1 * H, spokes=6)
        s.c.setLineWidth(1.2); s.c.line(X(0.0), y + 0.2 * H, X(-0.04), y + 0.2 * H)

    def trestle(s, x0, x1, ytop, ybot, bents=6):
        s.c.setStrokeColor(K)
        s.c.setLineWidth(1.4); s.c.line(x0, ytop, x1, ytop); s.c.line(x0, ytop - 3, x1, ytop - 3)
        xs = [lerp(x0, x1, i / bents) for i in range(bents + 1)]
        for xa, xb in zip(xs, xs[1:]):
            s.c.setLineWidth(0.6); s.c.line(xa, ytop - 3, xb, ybot); s.c.line(xb, ytop - 3, xa, ybot)
            yh = lerp(ytop, ybot, 0.5); s.c.line(xa, yh, xb, yh)
        for xa in xs: s.c.setLineWidth(1.0); s.c.line(xa, ytop - 3, xa, ybot)

    def signal(s, x, y, h):
        s.c.setStrokeColor(K); s.c.setLineWidth(1.0); s.c.line(x, y, x, y + h)
        s.shape([(x, y + h * 0.82), (x + h * 0.32, y + h * 0.86), (x + h * 0.32, y + h * 0.94), (x, y + h * 0.95)], lw=0.6, fill=K, amp=0)
        s.circle(x, y + h * 0.75, h * 0.06, lw=0.5, fill=Wt)

    # --- camp ------------------------------------------------------------------
    def tent(s, x, y, w, open_=True, glow=True, side=1):
        """A-frame tent in 3/4 view; (x, y) = centre of front at ground."""
        h = w * 0.78; d = w * 0.75 * side
        apex = (x, y + h); bl = (x - w / 2, y); br = (x + w / 2, y)
        back_apex = (x + d, y + h + w * 0.08); back_br = (x + w / 2 + d, y + w * 0.08)
        side_poly = [apex, back_apex, back_br, br] if side > 0 else [apex, back_apex, (x - w / 2 + d, y + w * 0.08), bl]
        s.shape(side_poly, lw=0.9, fill=Wt, amp=0.2)
        s.hatch(side_poly, angle=-20 * side + 90, gap=2.0, lw=0.35)
        s.shape(side_poly, lw=0.9, fill=None, amp=0)
        front = [bl, apex, br]
        s.shape(front, lw=0.9, fill=Wt, amp=0.2)
        if open_:
            dw = w * 0.2
            door = [(x - dw, y), (x, y + h * 0.75), (x + dw, y)]
            s.shape(door, lw=0.6, fill=K, amp=0)
            if glow:
                lx, ly = x, y + h * 0.12; lh = h * 0.2
                s.blob(s.arcpts(lx, ly + lh * 0.45, lh * 0.22, lh * 0.38, 0, 360, 16), Wt)
                s.c.setStrokeColor(Wt); s.c.setLineWidth(0.5); s.c.line(lx, ly + lh * 0.85, lx, ly + lh * 1.1)
            # tied-back flaps
            s.shape([(x - dw, y), (x, y + h * 0.75), (x - dw * 1.5, y + h * 0.25), (x - dw * 1.6, y)], lw=0.6, fill=Wt, amp=0)
            s.shape([(x + dw, y), (x, y + h * 0.75), (x + dw * 1.5, y + h * 0.25), (x + dw * 1.6, y)], lw=0.6, fill=Wt, amp=0)
        # snow on ridge
        s.line([apex, back_apex], lw=1.6, amp=0)
        # guy lines and pegs
        gx = x - w * 0.72 * side; s.line([apex, (gx, y - 1)], lw=0.35, amp=0)
        s.c.setLineWidth(0.9); s.c.line(gx, y - 1, gx, y + 2)
        s.c.line(x, y + h, x, y + h + 3.5)
        s.line([(x - w * 0.62, y - 1.2), (x + w * 0.55 + d * 0.8, y - 1.0)], lw=0.6, amp=0.4)

    def campfire(s, x, y, w):
        # logs
        for ang in (18, -18):
            a = math.radians(ang); dx, dy = math.cos(a) * w / 2, math.sin(a) * w / 2; t = w * 0.09
            nx, ny = -math.sin(a) * t, math.cos(a) * t
            s.shape([(x - dx - nx, y + w * 0.08 - dy - ny), (x + dx - nx, y + w * 0.08 + dy - ny), (x + dx + nx, y + w * 0.08 + dy + ny), (x - dx + nx, y + w * 0.08 - dy + ny)], lw=0.7, fill=Wt, amp=0)
            s.hatch([(x - dx - nx, y + w * 0.08 - dy - ny), (x + dx - nx, y + w * 0.08 + dy - ny), (x + dx + nx, y + w * 0.08 + dy + ny), (x - dx + nx, y + w * 0.08 - dy + ny)], angle=ang, gap=1.4, lw=0.3)
        # flames
        def flame(cx, by, fh, fw):
            pts = [(cx - fw / 2, by)]
            pts += [(cx - fw / 2 - fw * 0.1, by + fh * 0.35), (cx - fw * 0.15, by + fh * 0.7), (cx - fw * 0.05, by + fh), (cx + fw * 0.2, by + fh * 0.62), (cx + fw * 0.55, by + fh * 0.35), (cx + fw / 2, by)]
            return pts
        s.blob(s.wob(flame(x, y + w * 0.1, w * 0.85, w * 0.5), 0.3, closed=True), K)
        s.blob(s.wob(flame(x + w * 0.02, y + w * 0.12, w * 0.45, w * 0.24), 0.2, closed=True), Wt)
        for i in range(6):
            s.circle(x + s.r.uniform(-w * 0.4, w * 0.4), y + w * s.r.uniform(1.0, 1.5), s.r.uniform(0.4, 0.8), fill=K, stroke=False)
        # ring of stones
        for i in range(5):
            u = lerp(-w * 0.62, w * 0.62, i / 4)
            s.shape(s.arcpts(x + u, y + 0.5, w * 0.08, w * 0.05, 0, 360, 12), lw=0.6, fill=Wt, amp=0)

    def lantern(s, x, y, h):
        w = h * 0.45
        s.shape([(x - w / 2, y), (x + w / 2, y), (x + w / 2 * 0.85, y + h * 0.7), (x - w / 2 * 0.85, y + h * 0.7)], lw=0.8, fill=Wt, amp=0)
        s.blob([(x - w * 0.12, y + h * 0.15), (x + w * 0.12, y + h * 0.15), (x, y + h * 0.5)], K)
        s.c.setLineWidth(0.5); s.c.line(x - w / 2 * 0.9, y + h * 0.35, x + w / 2 * 0.9, y + h * 0.35)
        s.shape([(x - w / 2 * 1.05, y + h * 0.7), (x + w / 2 * 1.05, y + h * 0.7), (x, y + h * 0.88)], lw=0.8, fill=K, amp=0)
        s.c.setLineWidth(0.6); s.c.arc(x - w * 0.22, y + h * 0.82, x + w * 0.22, y + h * 1.05, 0, 180)
        s.shape([(x - w / 2 - 1, y - 1.5), (x + w / 2 + 1, y - 1.5), (x + w / 2 + 1, y), (x - w / 2 - 1, y)], lw=0.6, fill=K, amp=0)

    def telescope(s, x, y, h, ang=55):
        a = math.radians(ang); L = h * 0.95; r = h * 0.07
        px, py = x, y + h * 0.55
        for dx in (-0.32, 0.05, 0.3):
            s.line([(px, py), (x + dx * h, y)], lw=0.9, amp=0)
        ux, uy = math.cos(a), math.sin(a); nx, ny = -uy, ux
        p0 = (px - ux * L * 0.35, py - uy * L * 0.35); p1 = (px + ux * L * 0.65, py + uy * L * 0.65)
        tube = [(p0[0] + nx * r * 0.7, p0[1] + ny * r * 0.7), (p1[0] + nx * r, p1[1] + ny * r), (p1[0] - nx * r, p1[1] - ny * r), (p0[0] - nx * r * 0.7, p0[1] - ny * r * 0.7)]
        s.shape(tube, lw=0.9, fill=Wt, amp=0)
        s.hatch([(p0[0] - nx * r * 0.7, p0[1] - ny * r * 0.7), (p1[0] - nx * r, p1[1] - ny * r), (p1[0], p1[1]), (p0[0], p0[1])], angle=ang, gap=1.2, lw=0.35)
        s.shape(tube, lw=0.9, fill=None, amp=0)
        q0 = (p1[0] - ux * 2, p1[1] - uy * 2)
        s.shape([(q0[0] + nx * r * 1.25, q0[1] + ny * r * 1.25), (p1[0] + ux * 3 + nx * r * 1.25, p1[1] + uy * 3 + ny * r * 1.25), (p1[0] + ux * 3 - nx * r * 1.25, p1[1] + uy * 3 - ny * r * 1.25), (q0[0] - nx * r * 1.25, q0[1] - ny * r * 1.25)], lw=0.8, fill=K, amp=0)
        s.shape([(p0[0] + nx * r * 0.4, p0[1] + ny * r * 0.4), (p0[0] - ux * 4 + nx * r * 0.4, p0[1] - uy * 4 + ny * r * 0.4), (p0[0] - ux * 4 - nx * r * 0.4, p0[1] - uy * 4 - ny * r * 0.4), (p0[0] - nx * r * 0.4, p0[1] - ny * r * 0.4)], lw=0.7, fill=K, amp=0)

    def sled(s, x, y, w):
        s.shape([(x - w / 2, y + w * 0.12), (x + w / 2, y + w * 0.12), (x + w / 2, y + w * 0.2), (x - w / 2, y + w * 0.2)], lw=0.7, fill=Wt, amp=0)
        s.hatch([(x - w / 2, y + w * 0.12), (x + w / 2, y + w * 0.12), (x + w / 2, y + w * 0.2), (x - w / 2, y + w * 0.2)], angle=0, gap=1.4, lw=0.35)
        s.line([(x - w / 2, y)] + s.arcpts(x + w / 2, y + w * 0.07, w * 0.07, w * 0.07, -90, 120, 10), lw=0.9, amp=0)
        for u in (-0.3, 0.3): s.line([(x + u * w, y), (x + u * w, y + w * 0.12)], lw=0.7, amp=0)

    def snowman_free_fence(s, x0, x1, y, h):
        """Split-rail fence half buried in snow."""
        n = int((x1 - x0) / (h * 1.4)) + 1
        for i in range(n + 1):
            xx = lerp(x0, x1, i / max(1, n)); s.shape([(xx - 1.2, y - 2), (xx + 1.2, y - 2), (xx + 1, y + h), (xx - 1, y + h + 0.8)], lw=0.6, fill=Wt, amp=0)
            s.blob([(xx - 1.8, y + h), (xx + 1.8, y + h), (xx, y + h + 2)], Wt)
        for v in (0.35, 0.75):
            s.line([(x0, y + h * v), (x1, y + h * v + 1)], lw=0.9, amp=0.3)

    # --- frames, signs, small props ------------------------------------------
    def frame(s, x0, y0, x1, y1, corner_flakes=True):
        c = s.c; c.setStrokeColor(K)
        c.setLineWidth(1.3); c.rect(x0, y0, x1 - x0, y1 - y0, stroke=1, fill=0)
        c.setLineWidth(0.45); c.rect(x0 + 3.2, y0 + 3.2, x1 - x0 - 6.4, y1 - y0 - 6.4, stroke=1, fill=0)
        if corner_flakes:
            for (cx, cy) in [(x0, y0), (x1, y0), (x0, y1), (x1, y1)]:
                c.setFillColor(Wt); c.circle(cx, cy, 6.5, stroke=0, fill=1)
                s.flake(cx, cy, 5.2, lw=0.7)

    def clip_rect(s, x0, y0, x1, y1):
        s.c.saveState(); p = s.c.beginPath(); p.rect(x0, y0, x1 - x0, y1 - y0); s.c.clipPath(p, stroke=0, fill=0)

    def unclip(s): s.c.restoreState()

    def signpost(s, x, y, w, text=None, arrows=None):
        h = w * 1.1
        s.shape([(x - 1.3, y), (x + 1.3, y), (x + 1.1, y + h), (x - 1.1, y + h)], lw=0.6, fill=K, amp=0)
        boards = arrows or ([(text, 1)] if text else [("", 1), ("", -1)])
        for i, (t, d) in enumerate(boards):
            by = y + h * (0.82 - 0.26 * i); bw = w * 0.95; bh = w * 0.2
            xa, xb = (x - bw * 0.2, x + bw * 0.8) if d > 0 else (x - bw * 0.8, x + bw * 0.2)
            tip = (xb + bh * 0.5, by) if d > 0 else (xa - bh * 0.5, by)
            pts = [(xa, by - bh / 2), (xb, by - bh / 2), tip, (xb, by + bh / 2), (xa, by + bh / 2)] if d > 0 else [(xb, by - bh / 2), (xa, by - bh / 2), tip, (xa, by + bh / 2), (xb, by + bh / 2)]
            s.shape(pts, lw=0.7, fill=Wt, amp=0)
            s.line([(xa + 1, by + bh / 2 + 0.8), (xb, by + bh / 2 + 1.2)], lw=1.4, amp=0.2)
            if t: s.text((xa + xb) / 2, by - bh * 0.28, t, size=bh * 0.62, font="Ink-Playfair")
        s.blob([(x - 4, y), (x + 4, y), (x + 2, y + 2.5), (x - 2, y + 2.5)], Wt)
        s.line([(x - 6, y + 0.5), (x - 2, y + 2.2), (x + 2, y + 2.2), (x + 6, y + 0.5)], lw=0.5, amp=0)

    def footprints(s, pts, size=1.6):
        for i, (x, y) in enumerate(pts):
            o = size * (1 if i % 2 else -1)
            s.shape(s.arcpts(x, y + o, size * 1.2, size * 0.55, 0, 360, 10), lw=0.4, fill=Wt, amp=0)

    def mug(s, x, y, h, steam=True, cocoa=True):
        w = h * 0.8
        body = [(x - w / 2, y + h), (x - w / 2 * 0.9, y), (x + w / 2 * 0.9, y), (x + w / 2, y + h)]
        s.c.setLineWidth(1.0); s.c.setStrokeColor(K); s.c.ellipse(x + w / 2 - 1, y + h * 0.25, x + w / 2 + h * 0.38, y + h * 0.8, stroke=1, fill=0)
        s.shape(body, lw=0.9, fill=Wt, amp=0)
        s.hatch([(x + w * 0.12, y + h), (x + w * 0.1, y), (x + w / 2 * 0.9, y), (x + w / 2, y + h)], angle=90, gap=1.4, lw=0.35)
        s.shape(body, lw=0.9, fill=None, amp=0)
        s.shape(s.arcpts(x, y + h, w / 2, h * 0.12, 0, 360, 24), lw=0.8, fill=K if cocoa else Wt, amp=0)
        if steam:
            for dx in (-w * 0.18, w * 0.15):
                s.line([(x + dx + 2 * math.sin(t * 0.6), y + h + 3 + t) for t in range(0, int(h * 0.9))], lw=0.5, amp=0)

    def stump(s, x, y, w):
        h = w * 0.55
        s.shape([(x - w / 2, y), (x + w / 2, y), (x + w / 2 * 0.9, y + h), (x - w / 2 * 0.9, y + h)], lw=0.8, fill=Wt, amp=0.2)
        s.hatch([(x - w / 2, y), (x + w / 2, y), (x + w / 2 * 0.9, y + h), (x - w / 2 * 0.9, y + h)], angle=90, gap=1.6, lw=0.35)
        s.shape(s.arcpts(x, y + h, w / 2 * 0.9, w * 0.13, 0, 360, 24), lw=0.8, fill=Wt, amp=0)
        s.shape(s.arcpts(x, y + h, w * 0.2, w * 0.05, 0, 360, 16), lw=0.4, fill=None, amp=0)

    def kettle(s, x, y, h):
        w = h * 1.1
        body = s.arcpts(x, y, w / 2, h * 0.75, 0, 180, 24)
        s.shape(body, lw=0.9, fill=K, amp=0)
        s.c.setStrokeColor(Wt); s.c.setLineWidth(0.6); s.c.arc(x - w * 0.3, y + h * 0.05, x - w * 0.05, y + h * 0.55, 100, 60)
        s.shape([(x + w * 0.42, y + h * 0.2), (x + w * 0.75, y + h * 0.55), (x + w * 0.7, y + h * 0.62), (x + w * 0.38, y + h * 0.4)], lw=0.7, fill=K, amp=0)
        s.c.setStrokeColor(K); s.c.setLineWidth(0.8); s.c.arc(x - w * 0.3, y + h * 0.45, x + w * 0.3, y + h * 1.15, 0, 180)
        s.circle(x, y + h * 0.78, 1.2, lw=0.5, fill=K)

    def firewood(s, x, y, w, rows=3):
        r = w / 8
        for row in range(rows):
            n = 4 - row
            for i in range(n):
                cx = x - (n - 1) * r + i * 2 * r; cy = y + r + row * r * 1.75
                s.circle(cx, cy, r, lw=0.7, fill=Wt); s.circle(cx, cy, r * 0.5, lw=0.35, fill=None); s.circle(cx, cy, r * 0.12, lw=0.3, fill=K)
        s.blob(s.arcpts(x, y + r * (1 + (rows - 1) * 1.75) + r * 0.7, (4 - rows + 1) * r * 1.0, r * 0.45, 0, 180, 12) + [(x - (4 - rows + 1) * r, y + r * (1 + (rows - 1) * 1.75) + r * 0.7)], Wt)
        s.line(s.arcpts(x, y + r * (1 + (rows - 1) * 1.75) + r * 0.7, (4 - rows + 1) * r * 1.0, r * 0.45, 0, 180, 12), lw=0.6, amp=0)

    # --- village -------------------------------------------------------------
    def cottage(s, x, y, w, h, chimney=True, door_side=0.62):
        s.wall(x, y, w, h * 0.6, gap=2.6)
        s.roof(x, x + w, y + h * 0.6, y + h, overhang=2.5, snow=2.4)
        s.window(x + w * 0.14, y + h * 0.2, w * 0.22, h * 0.2)
        s.shape([(x + w * door_side, y), (x + w * (door_side + 0.2), y), (x + w * (door_side + 0.2), y + h * 0.38), (x + w * door_side, y + h * 0.38)], lw=0.7, fill=K, amp=0)
        if chimney: s.chimney(x + w * 0.72, y + h * 0.78, w * 0.1, h * 0.28)

    def lamppost(s, x, y, h):
        s.c.setStrokeColor(K); s.c.setLineWidth(1.2); s.c.line(x, y, x, y + h * 0.8)
        s.c.setLineWidth(2.2); s.c.line(x - 2, y + 0.8, x + 2, y + 0.8)
        s.lantern(x, y + h * 0.8, h * 0.22)

    def bandstand(s, x, y, w):
        h = w * 0.8
        s.shape([(x - w / 2, y), (x + w / 2, y), (x + w / 2, y + h * 0.12), (x - w / 2, y + h * 0.12)], lw=0.8, fill=Wt, amp=0)
        s.hatch([(x - w / 2, y), (x + w / 2, y), (x + w / 2, y + h * 0.12), (x - w / 2, y + h * 0.12)], angle=90, gap=1.6, lw=0.35)
        for u in (-0.45, -0.15, 0.15, 0.45):
            s.c.setLineWidth(0.9); s.c.setStrokeColor(K); s.c.line(x + u * w, y + h * 0.12, x + u * w, y + h * 0.6)
        s.line([(x - w / 2, y + h * 0.3), (x + w / 2, y + h * 0.3)], lw=0.5, amp=0)
        s.c.setLineWidth(0.4)
        for i in range(13):
            xx = x - w / 2 + w * i / 12; s.c.line(xx, y + h * 0.12, xx, y + h * 0.3)
        roof = [(x - w * 0.58, y + h * 0.6), (x + w * 0.58, y + h * 0.6), (x, y + h)]
        s.shape(roof, lw=0.9, fill=Wt, amp=0.2)
        s.hatch([(x, y + h), (x + w * 0.58, y + h * 0.6), (x + w * 0.1, y + h * 0.6)], angle=-60, gap=1.7, lw=0.35)
        s.line([(x - w * 0.58, y + h * 0.6), (x, y + h + 1.2), (x + w * 0.58, y + h * 0.6)], lw=1.5, amp=0.2)
        s.c.setLineWidth(0.8); s.c.line(x, y + h, x, y + h + 4); s.sparkle(x, y + h + 5.5, 2.2)

    def star5(s, x, y, r, fill=Wt, lw=0.7, inner=0.42):
        pts = []
        for i in range(10):
            a = math.pi / 2 + math.pi * i / 5; rr = r if i % 2 == 0 else r * inner
            pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
        s.shape(pts, lw=lw, fill=fill, amp=0)

    def pond(s, x, y, w):
        pts = s.arcpts(x, y, w / 2, w * 0.12, 0, 360, 40)
        s.shape(pts, lw=0.8, fill=Wt, amp=0.2)
        for i in range(3):
            yy = y + w * 0.06 * (i - 1); L = w * (0.35 - 0.08 * abs(i - 1))
            s.line([(x - L / 2 + i * 3, yy), (x + L / 2 + i * 3, yy)], lw=0.4, amp=0)
        # skate tracks
        s.line([(x - w * 0.3 + w * 0.6 * t, y + w * 0.04 * math.sin(t * 9)) for t in [i / 20 for i in range(21)]], lw=0.35, amp=0)

    def ledge(s, x0, x1, y, depth=10):
        """A snowy shoulder of ground to stand a building on (top edge at y)."""
        top = [(lerp(x0, x1, t), y + 1.2 * math.sin(t * math.pi)) for t in [i / 20 for i in range(21)]]
        bot = [(lerp(x1 + depth * 0.8, x0 - depth * 0.8, t), y - depth + depth * 0.25 * math.sin(t * math.pi)) for t in [i / 20 for i in range(21)]]
        q = top + bot
        s.blob(q, Wt)
        s.line([(x0 - depth * 0.8, y - depth)] + top + [(x1 + depth * 0.8, y - depth)], lw=0.8, amp=0.2)
        s.hatch([(lerp(x0, x1, 0.6), y - 1)] + [(x1, y - 0.5), (x1 + depth * 0.8, y - depth), (lerp(x0, x1, 0.55), y - depth)], angle=-60, gap=1.8, lw=0.35)

    def summit(s, x0, x1, base, px0, px1, py, lw=0.9):
        """A mountain with a flat, snowy summit (px0..px1 at height py) for the lodge to sit on."""
        def jag(a, b, n):
            return [(lerp(a[0], b[0], i / n), lerp(a[1], b[1], i / n) + (s.r.uniform(-1.3, 1.3) if 0 < i < n else 0)) for i in range(n + 1)]
        left = jag((x0, base), (px0, py), max(4, int((px0 - x0) / 5)))
        top = [(lerp(px0, px1, t), py + 0.8 * math.sin(t * math.pi)) for t in [i / 12 for i in range(13)]]
        right = jag((px1, py), (x1, base), max(4, int((x1 - px1) / 5)))
        rid = left + top[1:] + right[1:]
        s.shape(rid, lw=lw, fill=Wt, amp=0)
        fx = px1 + (x1 - px1) * 0.06
        capy = py - (py - base) * 0.22
        fl = [p for p in right if p[1] <= capy]
        reg = [(px1 - 2, capy + s.r.uniform(-2, 2)), (lerp(px1, x1, 0.12), capy - 4), (lerp(px1, x1, 0.22), capy + 1)] + fl + [(fx, base + 1)]
        s.hatch(reg, angle=-60, gap=2.0, lw=0.42)
        for g in range(2):
            gx = lerp(px1, x1, s.r.uniform(0.2, 0.5)); gy = lerp(py, base, (gx - px1) / max(1, x1 - px1)) - 3
            s.line([(gx, gy), (gx - 4, gy - (py - base) * 0.18), (gx - 2, gy - (py - base) * 0.3)], lw=0.4, amp=0.3)
        s.line(rid, lw=lw, amp=0)

    # --- interiors -------------------------------------------------------------
    def rect(s, x, y, w, h, lw=0.8, fill=Wt):
        return s.shape([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], lw=lw, fill=fill, amp=0.12)

    def clockface(s, x, y, r, moon=True, roman=True):
        s.circle(x, y, r, lw=1.0, fill=Wt); s.circle(x, y, r * 0.86, lw=0.5, fill=None)
        R = ["XII", "I", "II", "III", "IIII", "V", "VI", "VII", "VIII", "IX", "X", "XI"]
        for i in range(12):
            a = math.pi / 2 - i * math.pi / 6
            if roman and r > 14:
                s.c.saveState(); s.c.translate(x + r * 0.7 * math.cos(a), y + r * 0.7 * math.sin(a)); s.c.rotate(math.degrees(a) - 90)
                s.c.setFillColor(K); s.c.setFont("Ink-Crimson", r * 0.17); s.c.drawCentredString(0, -r * 0.06, R[i]); s.c.restoreState()
            else:
                s.c.setLineWidth(1.0 if i % 3 == 0 else 0.5); s.c.line(x + r * 0.7 * math.cos(a), y + r * 0.7 * math.sin(a), x + r * 0.84 * math.cos(a), y + r * 0.84 * math.sin(a))
        if moon:  # painted moon in the arch above the dial
            pass
        s.c.setStrokeColor(K); s.c.setLineWidth(max(0.8, r * 0.06)); s.c.line(x, y, x + r * 0.42 * math.cos(math.radians(60)), y + r * 0.42 * math.sin(math.radians(60)))
        s.c.setLineWidth(max(0.6, r * 0.04)); s.c.line(x, y, x + r * 0.6 * math.cos(math.radians(-80)), y + r * 0.6 * math.sin(math.radians(-80)))
        s.circle(x, y, max(0.8, r * 0.05), lw=0.4, fill=K)

    def advent_door(s, x, y, w, h, num=None, open_=False, lw=0.8):
        """A little arched door (centre-bottom at x, y) with its number and a tiny letter dial."""
        pts = [(x - w / 2, y), (x + w / 2, y), (x + w / 2, y + h - w / 2)] + s.arcpts(x, y + h - w / 2, w / 2, w / 2, 0, 180, 18)[1:-1] + [(x - w / 2, y + h - w / 2)]
        s.shape(pts, lw=lw, fill=Wt, amp=0)
        inner = [(px + (x - px) * 0.18, py + (y + h * 0.45 - py) * 0.12) for px, py in pts]
        s.shape(inner, lw=lw * 0.5, fill=None, amp=0)
        if num is not None:
            fs = min(h * 0.3, w * (0.62 if num < 10 else 0.42))
            s.text(x, y + h * 0.5, str(num), size=fs, font="Ink-Playfair")
        s.circle(x, y + h * 0.24, w * 0.11, lw=0.5, fill=Wt)
        for i in range(8):
            a = math.pi * 2 * i / 8; s.c.setLineWidth(0.3); s.c.line(x + w * 0.07 * math.cos(a), y + h * 0.24 + w * 0.07 * math.sin(a), x + w * 0.11 * math.cos(a), y + h * 0.24 + w * 0.11 * math.sin(a))
        s.circle(x + w * 0.32, y + h * 0.42, max(0.6, w * 0.04), lw=0.3, fill=K)

    def grandfather_clock(s, x, y, w, h, doors=True):
        """The Great Advent Clock: hood with arched dial and painted moon, a case of 24 little doors, plinth."""
        hood_h = h * 0.27; plinth = h * 0.08; case_w = w * 0.84
        cx = x
        # plinth
        s.rect(cx - w / 2, y, w, plinth, lw=1.0); s.hatch([(cx - w / 2, y), (cx + w / 2, y), (cx + w / 2, y + plinth), (cx - w / 2, y + plinth)], angle=90, gap=1.8, lw=0.35)
        s.rect(cx - w / 2 - 2, y + plinth, w + 4, 3, lw=0.8, fill=K)
        # case
        cy0 = y + plinth + 3; ch = h - hood_h - plinth - 3
        s.rect(cx - case_w / 2, cy0, case_w, ch, lw=1.1)
        s.hatch([(cx + case_w * 0.38, cy0), (cx + case_w / 2, cy0), (cx + case_w / 2, cy0 + ch), (cx + case_w * 0.38, cy0 + ch)], angle=90, gap=1.4, lw=0.4)
        if doors:
            cols, rows = 4, 6; mx = case_w * 0.1; dw = (case_w * 0.76 - mx * 2) / cols; dh = (ch - 8) / rows
            for k in range(24):
                r, q = divmod(k, cols)
                dx = cx - case_w / 2 + mx + case_w * 0.02 + (q + 0.5) * dw; dy = cy0 + ch - 4 - (r + 1) * dh
                s.advent_door(dx, dy + dh * 0.08, dw * 0.74, dh * 0.84, num=k + 1, lw=0.6)
        # hood
        hy = y + h - hood_h
        s.rect(cx - w / 2, hy, w, 3.5, lw=0.9, fill=K)
        hood = [(cx - w * 0.46, hy + 3.5), (cx + w * 0.46, hy + 3.5), (cx + w * 0.46, hy + hood_h * 0.72)] + s.arcpts(cx, hy + hood_h * 0.72, w * 0.46, hood_h * 0.25, 0, 180, 24)[1:-1] + [(cx - w * 0.46, hy + hood_h * 0.72)]
        s.shape(hood, lw=1.1, fill=Wt, amp=0)
        s.hatch([(cx + w * 0.36, hy + 3.5), (cx + w * 0.46, hy + 3.5), (cx + w * 0.46, hy + hood_h * 0.72), (cx + w * 0.36, hy + hood_h * 0.82)], angle=90, gap=1.4, lw=0.4)
        for sx in (-1, 1):  # finials
            s.c.setFillColor(K); s.c.circle(cx + sx * w * 0.4, hy + hood_h * 0.98, w * 0.03, stroke=0, fill=1)
            s.line([(cx + sx * w * 0.4, hy + hood_h * 0.72), (cx + sx * w * 0.4, hy + hood_h * 0.96)], lw=1.2, amp=0)
        fr = min(w * 0.3, hood_h * 0.36)
        s.clockface(cx, hy + hood_h * 0.42, fr)
        # painted moon in the arch
        my = hy + hood_h * 0.42 + fr + (hood_h * 0.97 - hood_h * 0.42 - fr) * 0.45
        mr = min(fr * 0.3, (hy + hood_h * 0.95 - my) * 0.8)
        s.circle(cx, my, mr, lw=0.6, fill=Wt)
        s.hatch(s.arcpts(cx, my, mr, mr, 90, 270, 16) + s.arcpts(cx, my, mr * 0.3, mr, 270, 90, 16), angle=30, gap=1.0, lw=0.35)
        for sx in (-1, 1): s.sparkle(cx + sx * fr * 0.7, my, 1.6)

    def xmas_tree(s, x, y, h, star=False, baubles=True, garland=True):
        s.pine(x, y + h * 0.1, h * 0.9, style="line", tiers=6)
        # pot / stand
        s.shape([(x - h * 0.08, y), (x + h * 0.08, y), (x + h * 0.1, y + h * 0.1), (x - h * 0.1, y + h * 0.1)], lw=0.8, fill=Wt, amp=0)
        s.hatch([(x - h * 0.08, y), (x + h * 0.08, y), (x + h * 0.1, y + h * 0.1), (x - h * 0.1, y + h * 0.1)], angle=45, gap=1.6, lw=0.35, cross=True)
        if garland:
            for k in range(4):
                yy = y + h * (0.28 + 0.16 * k); hw = h * 0.21 * (1 - (yy - y) / h * 0.9)
                s.line([(x - hw + 2 * hw * t, yy - 4 * math.sin(math.pi * t) + 6 * t) for t in [i / 16 for i in range(17)]], lw=0.5, amp=0)
        if baubles:
            n = 0
            for k in range(4):
                yy = y + h * (0.28 + 0.16 * k); hw = h * 0.21 * (1 - (yy - y) / h * 0.9)
                for t in ((0.15, 0.5, 0.85) if k < 3 else (0.3, 0.7)):
                    bx = x - hw + 2 * hw * t; by = yy - 4 * math.sin(math.pi * t) + 6 * t - h * 0.02
                    s.c.setLineWidth(0.3); s.c.line(bx, by, bx, by + h * 0.02)
                    s.circle(bx, by, h * 0.016 + 0.5, lw=0.5, fill=K if n % 2 else Wt); n += 1
        if star:
            s.star5(x, y + h * 1.02, h * 0.06, fill=Wt, lw=0.9)
            for i in range(8):
                a = math.pi / 4 * i; s.c.setLineWidth(0.5); s.c.line(x + h * 0.08 * math.cos(a), y + h * 1.02 + h * 0.08 * math.sin(a), x + h * 0.11 * math.cos(a), y + h * 1.02 + h * 0.11 * math.sin(a))

    def fireplace(s, x, y, w, h, fire=True, stockings=0):
        """Stone fireplace with mantel; (x, y) = bottom-left."""
        s.rect(x, y, w, h, lw=1.0)
        # stones
        rows = 6; rh = h / rows
        for r in range(rows):
            off = (r % 2) * 0.5; n = 5
            for i in range(-1, n + 1):
                x0 = x + (i + off) * w / n; x1 = x0 + w / n
                x0, x1 = max(x, x0), min(x + w, x1)
                if x1 - x0 < 2: continue
                s.c.saveState(); p = s.c.beginPath(); p.rect(x, y, w, h); s.c.clipPath(p, stroke=0, fill=0)
                s.c.setStrokeColor(K); s.c.setLineWidth(0.45); s.c.roundRect(x0 + 0.8, y + r * rh + 0.8, x1 - x0 - 1.6, rh - 1.6, 1.8, stroke=1, fill=0)
                s.c.restoreState()
        # mantel
        s.rect(x - w * 0.06, y + h, w * 1.12, h * 0.07, lw=1.0)
        s.rect(x - w * 0.03, y + h - h * 0.04, w * 1.06, h * 0.04, lw=0.6, fill=K)
        # firebox
        fw, fh = w * 0.56, h * 0.55; fx = x + (w - fw) / 2
        box = [(fx, y), (fx + fw, y), (fx + fw, y + fh * 0.7)] + s.arcpts(fx + fw / 2, y + fh * 0.7, fw / 2, fh * 0.3, 0, 180, 20)[1:-1] + [(fx, y + fh * 0.7)]
        s.shape(box, lw=1.0, fill=K, amp=0)
        if fire:
            for (u, sc) in [(0.32, 0.7), (0.52, 1.0), (0.7, 0.75)]:
                cx = fx + fw * u; fh2 = fh * 0.55 * sc; fw2 = fw * 0.22 * sc
                pts = [(cx - fw2 / 2, y + fh * 0.12), (cx - fw2 * 0.6, y + fh * 0.12 + fh2 * 0.4), (cx - fw2 * 0.1, y + fh * 0.12 + fh2 * 0.75), (cx, y + fh * 0.12 + fh2), (cx + fw2 * 0.25, y + fh * 0.12 + fh2 * 0.6), (cx + fw2 * 0.6, y + fh * 0.12 + fh2 * 0.35), (cx + fw2 / 2, y + fh * 0.12)]
                s.blob(s.wob(pts, 0.3, closed=True), Wt)
            # logs
            for (a, b) in [(0.18, 0.62), (0.4, 0.84)]:
                s.shape([(fx + fw * a, y + 1), (fx + fw * b, y + 1), (fx + fw * b, y + fh * 0.12), (fx + fw * a, y + fh * 0.12)], lw=0.6, fill=Wt, amp=0)
        # hearth stone
        s.rect(x - w * 0.08, y - h * 0.05, w * 1.16, h * 0.05, lw=0.9)
        for i in range(stockings):
            sx = x + w * (0.2 + 0.6 * i / max(1, stockings - 1)); sy = y + h - h * 0.04
            sh = h * 0.22
            st = [(sx - sh * 0.15, sy), (sx + sh * 0.15, sy), (sx + sh * 0.15, sy - sh * 0.7), (sx + sh * 0.42, sy - sh * 0.82), (sx + sh * 0.36, sy - sh), (sx - sh * 0.15, sy - sh * 0.92)]
            s.shape(st, lw=0.7, fill=Wt, amp=0)
            s.rect(sx - sh * 0.17, sy - sh * 0.18, sh * 0.34, sh * 0.18, lw=0.6, fill=Wt)
            s.hatch(st[:3] + [(sx - sh * 0.15, sy - sh * 0.7)], angle=45, gap=1.5, lw=0.35)

    def window_snow(s, x, y, w, h, panes=(2, 3), curtains=True):
        s.rect(x - 3, y - 3, w + 6, h + 6, lw=1.0)
        s.rect(x, y, w, h, lw=0.8)
        c = s.c; c.saveState(); p = c.beginPath(); p.rect(x, y, w, h); c.clipPath(p, stroke=0, fill=0)
        s.snowfall(x, y, x + w, y + h, n=int(w * h / 60))
        for i in range(3): s.pine(x + w * (0.2 + 0.3 * i), y + 1, h * s.r.uniform(0.35, 0.55))
        s.line([(x, y + h * 0.12), (x + w, y + h * 0.16)], lw=0.6, amp=0.3)
        c.restoreState()
        c.setStrokeColor(K); c.setLineWidth(1.2)
        for i in range(1, panes[0]): c.line(x + w * i / panes[0], y, x + w * i / panes[0], y + h)
        for j in range(1, panes[1]): c.line(x, y + h * j / panes[1], x + w, y + h * j / panes[1])
        s.rect(x - 5, y - 6, w + 10, 3.5, lw=0.8)
        if curtains:
            for sx in (-1, 1):
                ex = x if sx < 0 else x + w
                cur = [(ex - sx * 4, y + h + 6), (ex + sx * w * 0.18, y + h + 6), (ex + sx * w * 0.05, y + h * 0.45), (ex + sx * w * 0.12, y - 8), (ex - sx * 4, y - 8)]
                s.shape(cur, lw=0.8, fill=Wt, amp=0.2)
                for k in range(3):
                    u = (k + 1) / 4
                    s.line([(ex - sx * 4 + sx * w * 0.2 * u, y + h + 5), (ex + sx * w * 0.02 * (1 + u), y + h * 0.45), (ex + sx * w * 0.1 * u, y - 7)], lw=0.35, amp=0.2)

    def stairs(s, x, y, w, h, steps=9, side=1):
        sw = w / steps; sh = h / steps
        pts = [(x, y)]
        for i in range(steps):
            pts += [(x + side * i * sw, y + (i + 1) * sh), (x + side * (i + 1) * sw, y + (i + 1) * sh)]
        pts += [(x + side * w, y)]
        s.shape(pts, lw=0.9, fill=Wt, amp=0)
        s.hatch([(x + side * w * 0.0, y)] + pts[1:-1] + [(x + side * w, y)], angle=0, gap=sh / 2.2, lw=0.3)
        s.shape(pts, lw=0.9, fill=None, amp=0)
        # banister
        s.line([(x + side * 2, y + sh * 3.2), (x + side * w, y + h + sh * 2.2)], lw=1.2, amp=0)
        for i in range(0, steps, 1):
            bx = x + side * (i + 0.5) * sw; by = y + (i + 1) * sh
            s.line([(bx, by), (bx, by + sh * 2.2 - (sh * 2.2 - (sh * 3.2 - sh)) * 0)], lw=0.5, amp=0)
        s.rect(x - side * 2 - 2.2, y, 4.4, sh * 3.6, lw=0.8, fill=K)

    def rug(s, x, y, w, d):
        pts = s.arcpts(x, y, w / 2, d / 2, 0, 360, 40)
        s.shape(pts, lw=0.9, fill=Wt, amp=0)
        s.shape(s.arcpts(x, y, w / 2 * 0.8, d / 2 * 0.75, 0, 360, 40), lw=0.5, fill=None, amp=0)
        s.shape(s.arcpts(x, y, w / 2 * 0.55, d / 2 * 0.45, 0, 360, 40), lw=0.5, fill=None, amp=0)
        for i in range(24):
            a = 2 * math.pi * i / 24; s.c.setLineWidth(0.4)
            s.c.line(x + w / 2 * math.cos(a), y + d / 2 * math.sin(a), x + w / 2 * 1.06 * math.cos(a), y + d / 2 * 1.08 * math.sin(a))

    def armchair(s, x, y, w, facing=1):
        """Wingback armchair, three-quarter view; (x, y) = centre bottom."""
        h = w * 1.15; f = facing
        X = lambda u: x + f * u * w
        back = [(X(-0.42), y + h * 0.35), (X(-0.45), y + h * 0.9), (X(-0.3), y + h), (X(0.25), y + h), (X(0.38), y + h * 0.9), (X(0.36), y + h * 0.35)]
        s.shape(back, lw=1.0, fill=Wt, amp=0.2)
        s.hatch([(X(0.1), y + h * 0.35), (X(0.36), y + h * 0.35), (X(0.38), y + h * 0.9), (X(0.25), y + h), (X(0.1), y + h)], angle=90 - 20 * f, gap=1.6, lw=0.35)
        # buttons
        for i in range(3):
            for j in range(2): s.circle(X(-0.2 + 0.18 * i), y + h * (0.62 + 0.16 * j), 0.6, lw=0.3, fill=K)
        seat = [(X(-0.48), y + h * 0.28), (X(0.46), y + h * 0.28), (X(0.5), y + h * 0.42), (X(-0.44), y + h * 0.42)]
        s.shape(seat, lw=0.9, fill=Wt, amp=0.2)
        s.shape([(X(-0.5), y + h * 0.1), (X(0.5), y + h * 0.1), (X(0.48), y + h * 0.3), (X(-0.48), y + h * 0.3)], lw=0.9, fill=Wt, amp=0.2)
        s.hatch([(X(0.15), y + h * 0.1), (X(0.5), y + h * 0.1), (X(0.48), y + h * 0.3), (X(0.15), y + h * 0.3)], angle=90, gap=1.6, lw=0.35)
        for sx in (-1, 1):  # rolled arms
            ax = X(sx * 0.48)
            s.shape([(ax - 5, y + h * 0.1), (ax + 5, y + h * 0.1), (ax + 5, y + h * 0.5), (ax - 5, y + h * 0.5)], lw=0.9, fill=Wt, amp=0.2)
            s.shape(s.arcpts(ax, y + h * 0.5, 6, 4, 0, 360, 16), lw=0.9, fill=Wt, amp=0)
        for u in (-0.42, 0.42):
            s.shape([(X(u) - 1.5, y), (X(u) + 1.5, y), (X(u) + 1.2, y + h * 0.1), (X(u) - 1.2, y + h * 0.1)], lw=0.6, fill=K, amp=0)

    def cat(s, x, y, w):
        """A cat curled up asleep."""
        h = w * 0.45
        body = s.arcpts(x, y + h * 0.45, w / 2, h * 0.5, 0, 180, 30) + [(x - w / 2, y + h * 0.45), (x - w / 2 + 2, y), (x + w / 2 - 2, y), (x + w / 2, y + h * 0.45)]
        s.shape(body, lw=0.9, fill=Wt, amp=0.2)
        s.hatch([(x, y), (x + w / 2 - 2, y), (x + w / 2, y + h * 0.45)] + s.arcpts(x, y + h * 0.45, w / 2, h * 0.5, 0, 60, 10), angle=60, gap=1.5, lw=0.35)
        hx, hy = x - w * 0.32, y + h * 0.42
        s.circle(hx, hy, h * 0.36, lw=0.9, fill=Wt)
        for sx in (-1, 1):
            s.shape([(hx + sx * h * 0.32 - h * 0.06, hy + h * 0.15), (hx + sx * h * 0.22, hy + h * 0.5), (hx + sx * h * 0.08, hy + h * 0.3)], lw=0.8, fill=Wt, amp=0)
            s.c.setLineWidth(0.6); s.c.arc(hx + sx * h * 0.13 - h * 0.06, hy - h * 0.02, hx + sx * h * 0.13 + h * 0.06, hy + h * 0.06, 200, 140)
        tail = [(x + w * 0.4, y + h * 0.1)] + [(x + w * 0.4 - w * 0.75 * t, y + h * 0.02 - 2 * math.sin(t * 3)) for t in [i / 10 for i in range(1, 11)]]
        s.line(tail, lw=2.2, amp=0)
        for sx in (-1, 1): s.line([(hx + sx * 1, hy - h * 0.12), (hx + sx * h * 0.55, hy - h * 0.1 + sx * 0)], lw=0.3, amp=0)

    def books(s, x, y, w, n=3):
        hh = w * 0.16
        for i in range(n):
            bw = w * (1 - 0.08 * i); off = s.r.uniform(-w * 0.06, w * 0.06)
            s.rect(x - bw / 2 + off, y + i * hh, bw, hh, lw=0.8)
            s.hatch([(x - bw / 2 + off, y + i * hh), (x - bw / 2 + off + bw * 0.15, y + i * hh), (x - bw / 2 + off + bw * 0.15, y + (i + 1) * hh), (x - bw / 2 + off, y + (i + 1) * hh)], angle=90, gap=1.2, lw=0.35)
            s.line([(x + bw / 2 + off - 2, y + i * hh + 1.5), (x + bw / 2 + off - 2, y + (i + 1) * hh - 1.5)], lw=0.4, amp=0)

    def envelope(s, x, y, w):
        h = w * 0.62
        s.rect(x - w / 2, y, w, h, lw=0.9)
        s.line([(x - w / 2, y + h), (x, y + h * 0.42), (x + w / 2, y + h)], lw=0.8, amp=0.1)
        s.line([(x - w / 2, y), (x - w * 0.08, y + h * 0.48)], lw=0.5, amp=0); s.line([(x + w / 2, y), (x + w * 0.08, y + h * 0.48)], lw=0.5, amp=0)
        s.circle(x, y + h * 0.42, w * 0.08, lw=0.7, fill=K)
        s.flake(x, y + h * 0.42, w * 0.05, lw=0.4, color=Wt)

    def garland(s, x0, x1, y, sag=8, lw=1.0, swags=1):
        """Evergreen swags: a rope of short needle strokes, with a small bow at each hook."""
        for j in range(swags):
            a0, a1 = lerp(x0, x1, j / swags), lerp(x0, x1, (j + 1) / swags)
            pts = [(lerp(a0, a1, t), y - sag * math.sin(math.pi * t)) for t in [i / 40 for i in range(41)]]
            s.line(pts, lw=lw, amp=0.3)
            for (px, py) in pts:
                for a in (60, 120, 240, 300):
                    r = math.radians(a + s.r.uniform(-25, 25)); L = s.r.uniform(2.2, 4.2) * lw
                    s.c.setLineWidth(0.45); s.c.line(px, py, px + L * math.cos(r), py + L * math.sin(r))
        for j in range(swags + 1):
            bx = lerp(x0, x1, j / swags)
            for sx in (-1, 1): s.shape([(bx, y), (bx + sx * 4.5 * lw, y + 2.5 * lw), (bx + sx * 4.5 * lw, y - 2.5 * lw)], lw=0.5, fill=K, amp=0)
            s.line([(bx, y), (bx - 2, y - 7 * lw)], lw=0.7, amp=0); s.line([(bx, y), (bx + 2, y - 7 * lw)], lw=0.7, amp=0)

    def candle(s, x, y, h, holder=True):
        w = h * 0.22
        if holder:
            s.shape(s.arcpts(x, y, w * 1.8, w * 0.5, 0, 360, 24), lw=0.8, fill=Wt, amp=0)
            s.c.setLineWidth(0.8); s.c.arc(x + w * 1.6, y - w * 0.4, x + w * 2.6, y + w * 0.6, -90, 180)
        s.rect(x - w / 2, y, w, h * 0.65, lw=0.8)
        s.hatch([(x + w * 0.1, y), (x + w / 2, y), (x + w / 2, y + h * 0.65), (x + w * 0.1, y + h * 0.65)], angle=90, gap=1.2, lw=0.35)
        s.line([(x, y + h * 0.65), (x, y + h * 0.72)], lw=0.5, amp=0)
        fl = [(x, y + h * 0.7), (x + w * 0.4, y + h * 0.8), (x, y + h)]
        s.shape([(x, y + h * 0.69), (x + w * 0.42, y + h * 0.8), (x + w * 0.05, y + h), (x - w * 0.38, y + h * 0.82)], lw=0.6, fill=K, amp=0)

    def pencil(s, x, y, L, ang=20):
        a = math.radians(ang); ux, uy = math.cos(a), math.sin(a); nx, ny = -uy, ux; t = L * 0.05
        p0 = (x, y); p1 = (x + ux * L * 0.8, y + uy * L * 0.8); tip = (x + ux * L, y + uy * L)
        body = [(p0[0] + nx * t, p0[1] + ny * t), (p1[0] + nx * t, p1[1] + ny * t), (p1[0] - nx * t, p1[1] - ny * t), (p0[0] - nx * t, p0[1] - ny * t)]
        s.shape(body, lw=0.7, fill=Wt, amp=0)
        s.hatch([(p0[0], p0[1]), (p1[0], p1[1]), (p1[0] - nx * t, p1[1] - ny * t), (p0[0] - nx * t, p0[1] - ny * t)], angle=ang, gap=1.0, lw=0.3)
        s.shape([(p1[0] + nx * t, p1[1] + ny * t), tip, (p1[0] - nx * t, p1[1] - ny * t)], lw=0.7, fill=Wt, amp=0)
        s.blob([(p1[0] + ux * L * 0.13 + nx * t * 0.35, p1[1] + uy * L * 0.13 + ny * t * 0.35), tip, (p1[0] + ux * L * 0.13 - nx * t * 0.35, p1[1] + uy * L * 0.13 - ny * t * 0.35)], K)
        e0 = (p0[0] - ux * L * 0.06, p0[1] - uy * L * 0.06)
        s.shape([(p0[0] + nx * t, p0[1] + ny * t), (e0[0] + nx * t, e0[1] + ny * t), (e0[0] - nx * t, e0[1] - ny * t), (p0[0] - nx * t, p0[1] - ny * t)], lw=0.7, fill=K, amp=0)

    def notepad(s, x, y, w, letters="E T A O"):
        h = w * 1.25
        s.rect(x - w / 2 + 2, y - 2, w, h, lw=0.6, fill=Wt)
        s.rect(x - w / 2, y, w, h, lw=0.8, fill=Wt)
        for i in range(6):
            yy = y + h * (0.15 + 0.12 * i); s.line([(x - w * 0.4, yy), (x + w * 0.4, yy)], lw=0.3, amp=0)
        for i in range(7): s.circle(x - w * 0.36 + i * w * 0.12, y + h, 1.2, lw=0.5, fill=Wt)
        s.text(x, y + h * 0.66, letters, size=w * 0.13, font="Ink-Plex")
        s.text(x, y + h * 0.42, "_ _ _   _ _ _ _", size=w * 0.11, font="Ink-Plex")

    def spectacles(s, x, y, w):
        r = w * 0.2
        for sx in (-1, 1):
            s.circle(x + sx * w * 0.24, y, r, lw=0.8, fill=Wt)
            s.c.setLineWidth(0.4); s.c.arc(x + sx * w * 0.24 - r * 0.6, y - r * 0.6, x + sx * w * 0.24 + r * 0.6, y + r * 0.6, 100, 60)
        s.c.setLineWidth(0.8); s.c.arc(x - w * 0.06, y - w * 0.02, x + w * 0.06, y + w * 0.1, 20, 140)
        s.line([(x - w * 0.44, y + r * 0.3), (x - w * 0.6, y + r * 0.9)], lw=0.7, amp=0)
        s.line([(x + w * 0.44, y + r * 0.3), (x + w * 0.6, y + r * 0.9)], lw=0.7, amp=0)

    def side_table(s, x, y, w):
        h = w * 0.9
        s.shape(s.arcpts(x, y + h, w / 2, w * 0.1, 0, 360, 24), lw=0.9, fill=Wt, amp=0)
        s.line([(x, y + h - w * 0.1), (x, y + h * 0.2)], lw=1.6, amp=0)
        for sx in (-1, 0.3, 1): s.line([(x, y + h * 0.25), (x + sx * w * 0.35, y)], lw=1.0, amp=0)
        return y + h

    def bookshelf(s, x, y, w, h, shelves=4):
        s.rect(x, y, w, h, lw=1.0)
        sh = h / shelves
        for i in range(shelves):
            yy = y + i * sh
            s.rect(x, yy, w, 2.2, lw=0.6, fill=K)
            bx = x + 2
            while bx < x + w - 5:
                bw = s.r.uniform(3, 6); bh = sh * s.r.uniform(0.55, 0.85)
                if s.r.random() < 0.12 and bx < x + w - 14:
                    s.shape([(bx, yy + 2.2), (bx + bw, yy + 2.2), (bx + bw + bh * 0.4, yy + 2.2 + bh * 0.9), (bx + bh * 0.4, yy + 2.2 + bh)], lw=0.5, fill=Wt, amp=0); bx += bw + bh * 0.45; continue
                s.rect(bx, yy + 2.2, bw, bh, lw=0.5, fill=K if s.r.random() < 0.35 else Wt)
                if s.r.random() < 0.5: s.line([(bx + 0.8, yy + 2.2 + bh * 0.8), (bx + bw - 0.8, yy + 2.2 + bh * 0.8)], lw=0.35, amp=0)
                bx += bw + 0.6

    def floor_lamp(s, x, y, h):
        s.shape(s.arcpts(x, y, h * 0.1, h * 0.025, 0, 360, 16), lw=0.8, fill=K, amp=0)
        s.line([(x, y), (x, y + h * 0.82)], lw=1.2, amp=0)
        sh = [(x - h * 0.14, y + h * 0.78), (x + h * 0.14, y + h * 0.78), (x + h * 0.08, y + h), (x - h * 0.08, y + h)]
        s.shape(sh, lw=0.9, fill=Wt, amp=0.1)
        s.hatch([(x + h * 0.02, y + h * 0.78), (x + h * 0.14, y + h * 0.78), (x + h * 0.08, y + h), (x + h * 0.02, y + h)], angle=90, gap=1.4, lw=0.35)

    # --- more railway ------------------------------------------------------------
    def tunnel(s, x, y, w, h):
        """Stone tunnel portal cut into a hillside; (x, y) = centre of rail level."""
        hill = [(x - w * 1.1, y)] + [(x - w * 1.1 + w * 2.2 * t, y + h * 1.6 * math.sin(math.pi * t) ** 0.7) for t in [i / 30 for i in range(1, 30)]] + [(x + w * 1.1, y)]
        s.shape(hill, lw=0.9, fill=Wt, amp=0.3)
        s.hatch([(x + w * 0.2, y), (x + w * 1.1, y)] + [p for p in hill if p[0] > x + w * 0.2][::-1][:1] + [(x + w * 0.3, y + h * 1.3)], angle=-60, gap=2, lw=0.35)
        arch = [(x - w / 2, y), (x - w / 2, y + h * 0.55)] + s.arcpts(x, y + h * 0.55, w / 2, h * 0.45, 180, 0, 20)[1:] + [(x + w / 2, y)]
        outer = [(x - w * 0.68, y), (x - w * 0.68, y + h * 0.6)] + s.arcpts(x, y + h * 0.6, w * 0.68, h * 0.58, 180, 0, 20)[1:] + [(x + w * 0.68, y)]
        s.shape(outer, lw=0.9, fill=Wt, amp=0)
        for i in range(9):  # voussoirs
            a = math.radians(180 - i * 22.5)
            s.line([(x + w / 2 * math.cos(a), y + h * 0.55 + h * 0.45 * math.sin(a)), (x + w * 0.68 * math.cos(a), y + h * 0.6 + h * 0.58 * math.sin(a))], lw=0.5, amp=0)
        s.shape(arch, lw=0.9, fill=K, amp=0)

    def station(s, x, y, w, h, name=None):
        s.wall(x, y, w, h * 0.55, gap=2.6)
        s.roof(x - w * 0.05, x + w * 1.05, y + h * 0.55, y + h * 0.9, overhang=3)
        for i in range(3): s.window(x + w * (0.1 + 0.3 * i), y + h * 0.12, w * 0.16, h * 0.26, arch=True)
        if name:
            s.rect(x + w * 0.2, y + h * 0.43, w * 0.6, h * 0.1, lw=0.6)
            s.text(x + w * 0.5, y + h * 0.455, name, size=h * 0.07)
        s.chimney(x + w * 0.75, y + h * 0.75, w * 0.07, h * 0.25)
        # platform
        s.rect(x - w * 0.15, y - 3, w * 1.3, 3, lw=0.7, fill=K)

    def water_tower(s, x, y, h):
        w = h * 0.5
        for sx in (-1, 1): s.line([(x + sx * w * 0.42, y), (x + sx * w * 0.3, y + h * 0.55)], lw=1.0, amp=0)
        s.line([(x - w * 0.4, y + h * 0.18), (x + w * 0.36, y + h * 0.42)], lw=0.5, amp=0); s.line([(x + w * 0.4, y + h * 0.18), (x - w * 0.36, y + h * 0.42)], lw=0.5, amp=0)
        s.rect(x - w / 2, y + h * 0.55, w, h * 0.3, lw=0.9)
        s.hatch([(x - w / 2, y + h * 0.55), (x + w / 2, y + h * 0.55), (x + w / 2, y + h * 0.85), (x - w / 2, y + h * 0.85)], angle=90, gap=2, lw=0.35)
        s.shape([(x - w * 0.58, y + h * 0.85), (x + w * 0.58, y + h * 0.85), (x, y + h)], lw=0.9, fill=Wt, amp=0)
        s.line([(x + w / 2, y + h * 0.6), (x + w * 0.85, y + h * 0.5), (x + w * 0.85, y + h * 0.42)], lw=1.0, amp=0)

    def bench(s, x, y, w):
        s.rect(x - w / 2, y + w * 0.22, w, w * 0.05, lw=0.7)
        s.rect(x - w / 2, y + w * 0.34, w, w * 0.05, lw=0.7)
        for sx in (-0.4, 0.4): s.line([(x + sx * w, y), (x + sx * w, y + w * 0.4)], lw=1.0, amp=0)

    # --- hotel mystery props ---------------------------------------------------
    def tin(s, x, y, w, label="COCOA"):
        h = w * 0.9
        s.rect(x - w / 2, y, w, h, lw=0.9)
        s.hatch([(x + w * 0.25, y), (x + w / 2, y), (x + w / 2, y + h), (x + w * 0.25, y + h)], angle=90, gap=1.3, lw=0.35)
        s.shape(s.arcpts(x, y + h, w / 2 + 1.5, w * 0.12, 0, 360, 24), lw=0.9, fill=Wt, amp=0)
        s.rect(x - w * 0.38, y + h * 0.3, w * 0.76, h * 0.34, lw=0.6)
        s.text(x, y + h * 0.4, label, size=w * 0.16, font="Ink-Playfair")

    def snowman(s, x, y, h, hat=True):
        r1, r2, r3 = h * 0.22, h * 0.16, h * 0.11
        s.circle(x, y + r1, r1, lw=0.9); s.circle(x, y + 2 * r1 + r2 * 0.8, r2, lw=0.9)
        hy = y + 2 * r1 + 1.6 * r2 + r3 * 0.8; s.circle(x, hy, r3, lw=0.9)
        for dy in (0.3, 0.0, -0.3): s.circle(x, y + 2 * r1 + r2 * 0.8 + dy * r2, 0.9, lw=0.3, fill=K)
        for sx in (-1, 1): s.circle(x + sx * r3 * 0.35, hy + r3 * 0.2, 0.7, lw=0.3, fill=K)
        s.blob([(x, hy - r3 * 0.05), (x + r3 * 0.7, hy - r3 * 0.2), (x, hy - r3 * 0.25)], K)
        s.line([(x - r3 * 0.9, hy - r3 * 0.85), (x + r3 * 0.9, hy - r3 * 0.85)], lw=1.6, amp=0)
        for sx in (-1, 1): s.line([(x + sx * r2 * 0.9, y + 2 * r1 + r2), (x + sx * r2 * 2.2, y + 2 * r1 + r2 * 1.9), (x + sx * r2 * 2.5, y + 2 * r1 + r2 * 2.3)], lw=0.7, amp=0.1)
        if hat:
            ty = hy + r3 * 0.75
            s.rect(x - r3 * 1.2, ty, r3 * 2.4, r3 * 0.25, lw=0.6, fill=K)
            s.rect(x - r3 * 0.75, ty, r3 * 1.5, r3 * 1.5, lw=0.6, fill=K)
            s.c.setStrokeColor(Wt); s.c.setLineWidth(0.8); s.c.line(x - r3 * 0.74, ty + r3 * 0.35, x + r3 * 0.74, ty + r3 * 0.35)

    def gem(s, x, y, w):
        h = w * 0.75
        top = [(x - w * 0.3, y + h), (x + w * 0.3, y + h), (x + w / 2, y + h * 0.7), (x, y), (x - w / 2, y + h * 0.7)]
        s.shape(top, lw=0.9, fill=Wt, amp=0)
        s.line([(x - w / 2, y + h * 0.7), (x + w / 2, y + h * 0.7)], lw=0.6, amp=0)
        for (a, b) in [((x - w * 0.3, y + h), (x - w * 0.15, y + h * 0.7)), ((x + w * 0.3, y + h), (x + w * 0.15, y + h * 0.7)), ((x, y + h), (x - w * 0.15, y + h * 0.7)), ((x, y + h), (x + w * 0.15, y + h * 0.7)),
                       ((x - w * 0.15, y + h * 0.7), (x, y)), ((x + w * 0.15, y + h * 0.7), (x, y))]:
            s.line([a, b], lw=0.45, amp=0)
        s.hatch([(x + w * 0.15, y + h * 0.7), (x + w / 2, y + h * 0.7), (x, y)], angle=60, gap=1.2, lw=0.35)
        for (dx, dy, r) in [(-0.7, 1.1, 2.4), (0.75, 0.9, 1.8), (0.0, 1.35, 1.5)]: s.sparkle(x + dx * w, y + dy * h, r)

    def cake(s, x, y, w):
        h = w * 0.55
        s.shape(s.arcpts(x, y, w * 0.62, w * 0.12, 0, 360, 30), lw=0.8, fill=Wt, amp=0)
        body = [(x - w / 2, y + w * 0.04), (x + w / 2, y + w * 0.04), (x + w / 2, y + h), (x - w / 2, y + h)]
        s.shape(body, lw=0.9, fill=Wt, amp=0)
        s.hatch([(x - w / 2, y + h * 0.42), (x + w / 2, y + h * 0.42), (x + w / 2, y + h * 0.56), (x - w / 2, y + h * 0.56)], angle=0, gap=1.1, lw=0.4)
        s.shape(s.arcpts(x, y + h, w / 2, w * 0.1, 0, 360, 30), lw=0.9, fill=Wt, amp=0)
        for i in range(7):
            dx = lerp(-w * 0.45, w * 0.45, i / 6); s.blob(s.arcpts(x + dx, y + h - 1, w * 0.05, w * 0.07, 180, 360, 8), Wt); s.line(s.arcpts(x + dx, y + h - 1, w * 0.05, w * 0.07, 180, 360, 8), lw=0.5, amp=0)

    def book(s, x, y, w, open_=False):
        h = w * 0.22
        if open_:
            for sx in (-1, 1):
                pg = [(x, y), (x + sx * w / 2, y + h * 0.4), (x + sx * w / 2, y + h * 2.6), (x, y + h * 2.2)]
                s.shape(pg, lw=0.9, fill=Wt, amp=0)
                for k in range(5):
                    t = 0.25 + 0.13 * k
                    s.line([(x + sx * w * 0.06, y + h * (0.3 + 1.8 * t)), (x + sx * w * 0.44, y + h * (0.6 + 1.8 * t))], lw=0.3, amp=0)
            return
        s.rect(x - w / 2, y, w, h, lw=0.9)
        s.hatch([(x - w / 2, y), (x - w * 0.38, y), (x - w * 0.38, y + h), (x - w / 2, y + h)], angle=90, gap=1.1, lw=0.4)
        for k in range(3): s.line([(x - w * 0.3, y + h * (0.25 + 0.25 * k)), (x + w * 0.46, y + h * (0.25 + 0.25 * k))], lw=0.3, amp=0)

    def skate(s, x, y, w, facing=1):
        f = facing; X = lambda u: x + f * u * w; h = w * 0.7
        boot = [(X(-0.4), y + h * 0.2), (X(0.42), y + h * 0.2), (X(0.48), y + h * 0.38), (X(0.15), y + h * 0.45), (X(0.0), y + h), (X(-0.38), y + h), (X(-0.42), y + h * 0.6)]
        s.shape(boot, lw=0.9, fill=Wt, amp=0.1)
        for k in range(4): s.line([(X(-0.3), y + h * (0.55 + 0.1 * k)), (X(-0.02), y + h * (0.5 + 0.1 * k))], lw=0.5, amp=0)
        s.rect(min(X(-0.42), X(-0.32)), y + h * 0.18, w * 0.1, 2, lw=0.4, fill=K)
        s.line([(X(-0.5), y + 2), (X(0.5), y + 2), (X(0.58), y + 4.5)], lw=1.4, amp=0)
        for u in (-0.3, 0.3): s.line([(X(u), y + 2), (X(u), y + h * 0.2)], lw=0.8, amp=0)

    def teapot(s, x, y, w):
        h = w * 0.62
        body = s.arcpts(x, y + h * 0.42, w * 0.38, h * 0.48, 0, 360, 30)
        s.shape([(x + w * 0.3, y + h * 0.35), (x + w * 0.62, y + h * 0.75), (x + w * 0.58, y + h * 0.8), (x + w * 0.26, y + h * 0.55)], lw=0.8, fill=Wt, amp=0)
        s.c.setLineWidth(1.0); s.c.setStrokeColor(K); s.c.arc(x - w * 0.56, y + h * 0.2, x - w * 0.2, y + h * 0.7, 90, 180)
        s.shape(body, lw=0.9, fill=Wt, amp=0)
        s.hatch([p for p in body if p[0] > x + w * 0.1] + [(x + w * 0.1, y + h * 0.42)], angle=70, gap=1.4, lw=0.35)
        s.shape(body, lw=0.9, fill=None, amp=0)
        s.shape(s.arcpts(x, y + h * 0.88, w * 0.18, h * 0.07, 0, 360, 16), lw=0.7, fill=Wt, amp=0)
        s.circle(x, y + h * 1.0, w * 0.04, lw=0.6, fill=K)
        s.line([(x - w * 0.36, y + h * 0.5), (x + w * 0.36, y + h * 0.5)], lw=0.4, amp=0)

    def cup(s, x, y, w):
        h = w * 0.55
        s.shape(s.arcpts(x, y, w * 0.6, w * 0.1, 0, 360, 24), lw=0.7, fill=Wt, amp=0)
        body = [(x - w / 2, y + h)] + s.arcpts(x, y + h, w / 2, h, 180, 360, 20)[1:]
        s.shape(body, lw=0.8, fill=Wt, amp=0)
        s.c.setLineWidth(0.9); s.c.arc(x + w * 0.38, y + h * 0.3, x + w * 0.72, y + h * 0.85, -90, 90)
        s.shape(s.arcpts(x, y + h, w / 2, w * 0.08, 0, 360, 20), lw=0.7, fill=K, amp=0)

    def snowglobe(s, x, y, w):
        r = w * 0.4
        s.shape([(x - w / 2, y), (x + w / 2, y), (x + w * 0.38, y + w * 0.22), (x - w * 0.38, y + w * 0.22)], lw=0.9, fill=Wt, amp=0)
        s.hatch([(x + w * 0.15, y), (x + w / 2, y), (x + w * 0.38, y + w * 0.22), (x + w * 0.12, y + w * 0.22)], angle=90, gap=1.3, lw=0.35)
        cy = y + w * 0.22 + r * 0.92
        s.circle(x, cy, r, lw=1.0, fill=Wt)
        s.c.saveState(); p = s.c.beginPath(); p.circle(x, cy, r - 0.6); s.c.clipPath(p, stroke=0, fill=0)
        s.line([(x - r, cy - r * 0.45), (x + r, cy - r * 0.4)], lw=0.6, amp=0.2)
        s.pine(x - r * 0.35, cy - r * 0.45, r * 0.8); s.cottage(x + r * 0.0, cy - r * 0.45, r * 0.6, r * 0.6, chimney=False)
        for i in range(14): s.circle(x + s.r.uniform(-r, r), cy + s.r.uniform(-r * 0.3, r), 0.5, lw=0.3, fill=Wt)
        s.c.restoreState()
        s.c.setStrokeColor(K); s.c.setLineWidth(0.5); s.c.arc(x - r * 0.75, cy - r * 0.75, x + r * 0.75, cy + r * 0.75, 100, 60)

    def violin(s, x, y, h, ang=-12):
        """Upright violin (body, fingerboard, scroll, f-holes, bridge, strings) standing at (x, y), height h."""
        c = s.c; c.saveState(); c.translate(x, y); c.rotate(ang)
        bh = h * 0.6; w = h * 0.36
        ctrl = [(0.0, 0.0), (0.04, 0.62), (0.14, 0.92), (0.27, 1.0), (0.42, 0.86), (0.52, 0.64), (0.6, 0.66), (0.7, 0.8), (0.82, 0.8), (0.93, 0.6), (1.0, 0.0)]
        def hw(t):
            for (t0, v0), (t1, v1) in zip(ctrl, ctrl[1:]):
                if t <= t1:
                    u = (t - t0) / (t1 - t0); u = (1 - math.cos(math.pi * u)) / 2
                    return w / 2 * (v0 + (v1 - v0) * u)
            return 0
        n = 60
        right = [(hw(i / n), bh * i / n) for i in range(n + 1)]
        body = right + [(-px, py) for px, py in reversed(right)]
        s.shape(body, lw=1.0, fill=Wt, amp=0)
        s.hatch([(px, py) for px, py in right if py > bh * 0.03] + [(w * 0.18, bh * 0.97), (w * 0.18, bh * 0.03)], angle=75, gap=1.4, lw=0.35)
        s.shape(body, lw=1.0, fill=None, amp=0)
        # fingerboard and neck
        s.shape([(-w * 0.07, bh * 0.38), (w * 0.07, bh * 0.38), (w * 0.05, h * 0.9), (-w * 0.05, h * 0.9)], lw=0.6, fill=K, amp=0)
        # pegbox and scroll
        s.shape([(-w * 0.05, h * 0.9), (w * 0.05, h * 0.9), (w * 0.06, h * 0.95), (-w * 0.06, h * 0.95)], lw=0.6, fill=Wt, amp=0)
        s.circle(0, h * 0.975, w * 0.075, lw=0.8, fill=Wt); s.circle(w * 0.01, h * 0.975, w * 0.03, lw=0.6, fill=Wt)
        for sx in (-1, 1): s.line([(sx * w * 0.06, h * 0.93), (sx * w * 0.14, h * 0.935)], lw=0.9, amp=0)
        # f-holes
        for sx in (-1, 1):
            s.line([(sx * w * 0.19, bh * 0.58), (sx * w * 0.15, bh * 0.5), (sx * w * 0.19, bh * 0.4), (sx * w * 0.15, bh * 0.32)], lw=0.7, amp=0)
        # bridge, tailpiece, strings
        s.line([(-w * 0.12, bh * 0.45), (w * 0.12, bh * 0.45)], lw=1.1, amp=0)
        s.shape([(-w * 0.07, bh * 0.05), (w * 0.07, bh * 0.05), (w * 0.05, bh * 0.25), (-w * 0.05, bh * 0.25)], lw=0.6, fill=K, amp=0)
        c.setStrokeColor(K); c.setLineWidth(0.3)
        for dx in (-0.03, -0.01, 0.01, 0.03): c.line(dx * w, bh * 0.25, dx * w * 0.8, h * 0.9)
        c.restoreState()

    def key(s, x, y, L, tag=None):
        s.circle(x, y, L * 0.16, lw=1.2, fill=Wt); s.circle(x, y, L * 0.07, lw=0.8, fill=Wt)
        s.line([(x + L * 0.16, y), (x + L, y)], lw=1.8, amp=0)
        for (u, d) in [(0.78, 0.14), (0.9, 0.2)]: s.line([(x + L * u, y), (x + L * u, y - L * d)], lw=1.8, amp=0)
        if tag:
            tx, ty = x - L * 0.16, y - L * 0.05
            s.line([(tx, ty), (tx - L * 0.12, ty - L * 0.25)], lw=0.5, amp=0)
            q = [(tx - L * 0.3, ty - L * 0.28), (tx + L * 0.04, ty - L * 0.28), (tx + L * 0.04, ty - L * 0.48), (tx - L * 0.3, ty - L * 0.48)]
            s.shape(q, lw=0.7, fill=Wt, amp=0); s.text(tx - L * 0.13, ty - L * 0.41, tag, size=min(L * 0.11, L * 0.5 / max(1, len(tag))), font="Ink-Plex")

    def portrait(s, x, y, w):
        h = w * 1.25
        s.rect(x - w / 2, y, w, h, lw=1.0)
        s.hatch([(x - w / 2, y), (x + w / 2, y), (x + w / 2, y + h), (x - w / 2, y + h)], angle=45, gap=1.5, lw=0.3, cross=True)
        s.rect(x - w * 0.38, y + h * 0.1, w * 0.76, h * 0.8, lw=0.8)
        # an imaginary founder, drawn as a silhouette bust
        s.circle(x, y + h * 0.6, w * 0.13, lw=0.6, fill=K)
        s.blob(s.arcpts(x, y + h * 0.1, w * 0.3, h * 0.36, 0, 180, 20), K)
        s.line([(x - w * 0.12, y + h + 1), (x, y + h + w * 0.25), (x + w * 0.12, y + h + 1)], lw=0.5, amp=0)
        s.circle(x, y + h + w * 0.25, 1, lw=0.4, fill=K)

    def desk_bell(s, x, y, w):
        s.rect(x - w / 2, y, w, w * 0.08, lw=0.8, fill=K)
        dome = s.arcpts(x, y + w * 0.08, w * 0.4, w * 0.38, 0, 180, 24)
        s.shape(dome, lw=0.9, fill=Wt, amp=0)
        s.hatch([p for p in dome if p[0] > x + w * 0.1] + [(x + w * 0.1, y + w * 0.08)], angle=70, gap=1.3, lw=0.35)
        s.line([(x, y + w * 0.46), (x, y + w * 0.56)], lw=1.0, amp=0); s.circle(x, y + w * 0.58, w * 0.05, lw=0.6, fill=K)
