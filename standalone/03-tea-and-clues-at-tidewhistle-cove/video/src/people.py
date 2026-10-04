"""people: detailed procedural ink characters for the Tidewhistle Cove videos (house inkart line style).

Every figure is drawn in a local 0..100 coordinate frame (feet at y=0, top of head near y=100) with smooth
Catmull-Rom bezier outlines, ink hatching and solid black fills, then placed with Fig(k, x, y, height).
Line widths and hatch gaps are given in output points, so a figure looks the same weight at any size.

  agnes(k, x, y, h)        Agnes Bell: grey bun, round glasses, sprig dress, frilled apron, teapot
  ollie(k, x, y, h)        Constable Ollie Penrose: custodian helmet, tunic, belt, pocket notebook
  morwenna(k, x, y, h)     Morwenna Day: straw hat, long dark hair, cardigan, flower dress, sweet peas
  hedley(k, x, y, h)       Hedley Truscott: flat cap, moustache, rolled sleeves, waistcoat, folding chair
  jago(k, x, y, h)         Jago Penhallow: baker's toque, short beard, striped shirt, apron, bread basket

The three suspects share one neutral expression, one stance and one level of detail, so no picture hints
at the answer before the solution. expr="sheepish" exists only for post-solution scenes."""
import math
from reportlab.lib import colors

K = colors.black; Wt = colors.white

def _crpath(c, pts, closed=True, t=1.0):
    """Catmull-Rom spline through pts as cubic beziers. A point (x, y, 0) is a sharp corner."""
    P = [(p[0], p[1]) for p in pts]; S = [p[2] if len(p) > 2 else 1.0 for p in pts]; n = len(P)
    path = c.beginPath(); path.moveTo(*P[0])
    segs = range(n) if closed else range(n - 1)
    for i in segs:
        i0 = (i - 1) % n if closed else max(i - 1, 0); i2 = (i + 1) % n; i3 = (i + 2) % n if closed else min(i + 2, n - 1)
        p0, p1, p2, p3 = P[i0], P[i], P[i2], P[i3]
        a, b = t * S[i] / 6, t * S[i2] / 6
        path.curveTo(p1[0] + (p2[0] - p0[0]) * a, p1[1] + (p2[1] - p0[1]) * a,
                     p2[0] - (p3[0] - p1[0]) * b, p2[1] - (p3[1] - p1[1]) * b, p2[0], p2[1])
    if closed: path.close()
    return path

def ell(cx, cy, rx, ry, a0=0, a1=360, n=24):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + (0 if (a1 - a0) % 360 == 0 else 1))]

def tube(cl, w, sharp_start=True):
    """Outline (closed point list) of a limb along centreline cl with half-widths w."""
    L, R = [], []
    for i, (x, y) in enumerate(cl):
        xa, ya = cl[max(0, i - 1)]; xb, yb = cl[min(len(cl) - 1, i + 1)]
        dx, dy = xb - xa, yb - ya; d = math.hypot(dx, dy) or 1; nx, ny = -dy / d, dx / d
        L.append((x + nx * w[i], y + ny * w[i])); R.append((x - nx * w[i], y - ny * w[i]))
    L[-1] = L[-1] + (0,); R[-1] = R[-1] + (0,)
    if sharp_start:
        L[0] = L[0] + (0,); R[0] = R[0] + (0,)
        return L + R[::-1]
    return [((L[0][0] + R[0][0]) / 2 + (cl[0][0] - cl[1][0]) * 0.18, (L[0][1] + R[0][1]) / 2 + (cl[0][1] - cl[1][1]) * 0.18)] + L + R[::-1]

class Fig:
    def __init__(s, k, x, y, h, flip=False):
        s.k, s.c, s.r = k, k.c, k.r; s.sc = h / 100.0; s.x, s.y, s.flip = x, y, flip
    def __enter__(s):
        c = s.c; c.saveState(); c.translate(s.x, s.y); c.scale(-s.sc if s.flip else s.sc, s.sc)
        c.setLineCap(1); c.setLineJoin(1); return s
    def __exit__(s, *a): s.c.restoreState()
    def W(s, lw): return lw / s.sc
    def shape(s, pts, lw=1.0, fill=Wt, stroke=True, t=1.0, color=K):
        c = s.c; p = _crpath(c, pts, True, t); c.setStrokeColor(color); c.setLineWidth(s.W(lw))
        if fill is not None: c.setFillColor(fill)
        c.drawPath(p, stroke=1 if stroke and lw > 0 else 0, fill=1 if fill is not None else 0)
    def curve(s, pts, lw=0.6, t=1.0, color=K):
        c = s.c; c.setStrokeColor(color); c.setLineWidth(s.W(lw)); c.drawPath(_crpath(c, pts, False, t), stroke=1, fill=0)
    def clip(s, pts, t=1.0):
        s.c.saveState(); s.c.clipPath(_crpath(s.c, pts, True, t), stroke=0, fill=0)
    def unclip(s): s.c.restoreState()
    def hatch(s, pts, angle=-50, gap=1.8, lw=0.35, cross=False, t=1.0, box=None, color=K):
        """Parallel ink lines (gap in output points) clipped to the smooth region pts (and optional box)."""
        c = s.c; s.clip(pts, t)
        if box: c.clipPath(_crpath(c, [(box[0], box[1], 0), (box[2], box[1], 0), (box[2], box[3], 0), (box[0], box[3], 0)], True), stroke=0, fill=0)
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        R = math.hypot(max(xs) - min(xs), max(ys) - min(ys)) / 2 + 1; g = gap / s.sc
        c.setStrokeColor(color); c.setLineWidth(s.W(lw))
        for ang in ([angle, angle + 90] if cross else [angle]):
            a = math.radians(ang); dx, dy = math.cos(a), math.sin(a); nx, ny = -dy, dx; o = -R
            while o <= R:
                oo = o + s.r.uniform(-0.12, 0.12) * g
                c.line(cx + nx * oo - dx * R, cy + ny * oo - dy * R, cx + nx * oo + dx * R, cy + ny * oo + dy * R); o += g
        s.unclip()
    def dot(s, x, y, r, fill=K, lw=0.0):
        c = s.c; c.setFillColor(fill); c.setStrokeColor(K); c.setLineWidth(s.W(max(lw, 0.01)))
        c.circle(x, y, r, stroke=1 if lw else 0, fill=1)
    def ring(s, x, y, r, lw=0.5, fill=None):
        c = s.c; c.setStrokeColor(K); c.setLineWidth(s.W(lw))
        if fill is not None: c.setFillColor(fill)
        c.circle(x, y, r, stroke=1, fill=0 if fill is None else 1)

# ============================================================================ shared body parts
def hand(f, x, y, ang=-90, size=1.0, lw=0.8):
    """Mitten hand with a thumb; ang = direction the fingers point (degrees)."""
    a = math.radians(ang); ux, uy = math.cos(a), math.sin(a); vx, vy = -uy, ux
    def P(u, v): return (x + (ux * u + vx * v) * size, y + (uy * u + vy * v) * size)
    f.shape([P(-1.2, -1.45), P(0.4, -1.75), P(1.9, -1.4), P(2.7, -0.4), P(2.7, 0.6), P(1.9, 1.35), P(0.4, 1.6), P(-1.2, 1.4)], lw=lw)
    f.curve([P(-0.3, 1.45), P(0.9, 2.35), P(1.7, 2.1), P(1.2, 1.1)], lw=lw * 0.8)
    for v in (-0.55, 0.35): f.curve([P(1.3, v), P(2.4, v + 0.05)], lw=0.35)

def shoe(f, x, side=1, kind="shoe", top=3.2):
    """side: +1 right foot (toe points right), -1 left."""
    s = side
    if kind == "boot":   # black wellies / police boots
        pts = [(x - 2.6 * s, top, 0), (x + 2.4 * s, top, 0), (x + 2.5 * s, 2.6), (x + 4.6 * s, 1.6), (x + 4.8 * s, 0.2, 0), (x - 2.9 * s, 0.2, 0), (x - 2.9 * s, 2.4)]
        f.shape(pts, lw=0.9, fill=K)
        f.curve([(x - 2.4 * s, 0.9), (x + 4.4 * s, 0.9)], lw=0.35, color=Wt)
    else:
        pts = [(x - 2.4 * s, 3.3), (x + 1.9 * s, 3.4), (x + 4.3 * s, 2.0), (x + 4.6 * s, 0.3, 0), (x - 2.7 * s, 0.3, 0), (x - 2.8 * s, 1.8)]
        f.shape(pts, lw=0.9, fill=K)
        f.curve([(x - 2.2 * s, 2.6), (x + 1.4 * s, 2.7)], lw=0.35, color=Wt)

def neck(f, cy, w=2.2, base=79.5):
    f.shape([(-w, base, 0), (-w * 0.92, cy - 4.5), (w * 0.92, cy - 4.5), (w, base, 0)], lw=0.8)
    f.hatch([(-w, base), (-w, cy - 4.6), (w, cy - 4.6), (w, base)], angle=-20, gap=1.5, lw=0.3, box=(-w, cy - 7.2, w, cy - 4.4))

def face_shape(cx, cy, rx, ry, jaw=0.62):
    pts = []
    for i in range(40):
        a = 2 * math.pi * i / 40; x = math.cos(a) * rx; y = math.sin(a) * ry
        if y < 0: x *= 1 - (1 - jaw) * (-math.sin(a)) ** 1.6
        if y > 0: x *= 1 + 0.04 * math.sin(a)
        pts.append((cx + x, cy + y))
    return pts

def head(f, cx, cy, rx=6.0, ry=7.4, jaw=0.62, expr="neutral", glasses=False, brows="soft", nose="small",
         lines=0, moustache=False, beard=False, blush=False, ears=True, shade=True):
    """Face with ears, eyes, brows, nose, mouth. expr: smile | kind | neutral | sheepish."""
    if ears:
        for sg in (-1, 1):
            e = ell(cx + sg * rx * 0.96, cy - 0.3, 1.25, 1.9, n=16)
            f.shape(e, lw=0.8)
            f.curve([(cx + sg * rx * 1.02, cy + 0.9), (cx + sg * rx * 1.25, cy - 0.2), (cx + sg * rx * 1.05, cy - 1.3)], lw=0.35)
            if blush: f.hatch(e, angle=70, gap=0.9, lw=0.3)
    fs = face_shape(cx, cy, rx, ry, jaw)
    f.shape(fs, lw=1.0)
    if shade:   # light from the upper left: soft hatching down the right cheek and under the chin
        f.hatch(fs, angle=62, gap=1.35, lw=0.28, box=(cx + rx * 0.52, cy - ry - 1, cx + rx + 1, cy + ry * 0.55))
    if beard:
        bd = [(cx - rx * 0.98, cy - 0.5)] + [(cx + math.cos(a) * rx * (1 - 0.38 * max(0.0, -math.sin(a)) ** 1.6) * 1.02, cy + math.sin(a) * ry * 1.06)
                                              for a in [math.radians(180 + 180 * i / 16) for i in range(17)]] + \
             [(cx + rx * 0.98, cy - 0.5), (cx + rx * 0.6, cy - 2.6), (cx + 2.3, cy - 3.1), (cx, cy - 2.7), (cx - 2.3, cy - 3.1), (cx - rx * 0.6, cy - 2.6)]
        f.shape(bd, lw=0.8, fill=Wt)
        f.hatch(bd, angle=80, gap=0.8, lw=0.32)
        f.hatch(bd, angle=60, gap=1.6, lw=0.3)
    ey = cy + 0.4; ex = rx * 0.38
    for sg in (-1, 1):
        x = cx + sg * ex
        if expr == "sheepish":
            f.curve([(x - 1.0, ey + 0.1), (x, ey - 0.5), (x + 1.0, ey + 0.1)], lw=0.7)     # eyes cast down
        else:
            f.shape(ell(x, ey, 0.62, 0.82, n=14), lw=0.2, fill=K)
            f.dot(x - 0.2, ey + 0.3, 0.2, fill=Wt)
            f.curve([(x - 1.15, ey + 0.55), (x - 0.3, ey + 1.05), (x + 0.6, ey + 1.0), (x + 1.15, ey + 0.55)], lw=0.45)
            if expr in ("smile", "kind"): f.curve([(x - 0.9, ey - 0.95), (x, ey - 1.15), (x + 0.9, ey - 0.95)], lw=0.3)
        by = ey + 2.0
        if brows == "bushy":
            br = [(x - 1.6 * sg * -1 if False else x - 1.6, by - 0.1), (x, by + 0.55), (x + 1.6, by - 0.1), (x + 1.4, by - 0.75), (x, by - 0.15), (x - 1.5, by - 0.75)]
            f.shape(br, lw=0.3, fill=K)
        else:
            if expr == "sheepish": pts = [(x - 1.3 * sg, by + 0.5), (x, by + 0.15), (x + 1.3 * sg, by - 0.4)]
            elif expr in ("smile", "kind"): pts = [(x - 1.4, by - 0.2), (x, by + 0.55), (x + 1.4, by - 0.1)]
            else: pts = [(x - 1.4, by), (x, by + 0.3), (x + 1.4, by + 0.05)]
            f.curve(pts, lw=0.8 if brows == "thick" else 0.6)
    if glasses:
        for sg in (-1, 1): f.ring(cx + sg * ex, ey + 0.05, 1.75, lw=0.55)
        f.curve([(cx - ex + 1.7, ey + 0.4), (cx, ey + 0.8), (cx + ex - 1.7, ey + 0.4)], lw=0.45)
        for sg in (-1, 1): f.curve([(cx + sg * (ex + 1.75), ey + 0.3), (cx + sg * rx * 0.97, ey + 0.6)], lw=0.45)
    if nose == "button":
        f.curve([(cx + 0.1, ey - 0.6), (cx + 0.75, ey - 2.2), (cx + 0.1, ey - 2.75), (cx - 0.6, ey - 2.4)], lw=0.55)
    elif nose == "long":
        f.curve([(cx + 0.1, ey + 0.4), (cx + 0.6, ey - 1.9), (cx + 1.0, ey - 3.0), (cx + 0.2, ey - 3.35), (cx - 0.6, ey - 3.0)], lw=0.55)
    else:
        f.curve([(cx + 0.15, ey - 0.4), (cx + 0.75, ey - 2.3), (cx + 0.1, ey - 2.8), (cx - 0.5, ey - 2.55)], lw=0.5)
    my = cy - 3.7
    if moustache:
        m = [(cx - 3.2, my + 0.5), (cx - 1.7, my + 1.3), (cx, my + 1.35), (cx + 1.7, my + 1.3), (cx + 3.2, my + 0.5), (cx + 1.8, my + 0.35), (cx, my + 0.55), (cx - 1.8, my + 0.35)]
        f.shape(m, lw=0.4, fill=K)
        f.curve([(cx - 1.2, my - 0.7), (cx, my - 0.85), (cx + 1.2, my - 0.7)], lw=0.5)
    elif expr == "smile":
        f.curve([(cx - 2.0, my + 0.35), (cx - 0.9, my - 0.55), (cx + 0.9, my - 0.55), (cx + 2.0, my + 0.35)], lw=0.7)
        for sg in (-1, 1): f.curve([(cx + sg * 2.0, my + 0.6), (cx + sg * 2.35, my + 0.2)], lw=0.35)
    elif expr == "kind":
        f.curve([(cx - 1.7, my + 0.2), (cx - 0.6, my - 0.4), (cx + 0.6, my - 0.4), (cx + 1.7, my + 0.2)], lw=0.65)
    elif expr == "sheepish":
        f.curve([(cx - 1.3, my - 0.1), (cx - 0.4, my + 0.15), (cx + 0.4, my - 0.15), (cx + 1.3, my + 0.05)], lw=0.65)
    else:   # neutral, identical for every suspect
        f.curve([(cx - 1.35, my - 0.05), (cx, my - 0.2), (cx + 1.35, my - 0.05)], lw=0.65)
    if not beard and not moustache: f.curve([(cx - 0.6, my - 1.15), (cx + 0.6, my - 1.15)], lw=0.3)
    if blush:
        for sg in (-1, 1):
            f.hatch(ell(cx + sg * rx * 0.55, cy - 1.6, 1.4, 0.8, n=12), angle=75, gap=0.7, lw=0.3)
    if lines:
        for sg in (-1, 1):
            for j in range(lines):
                f.curve([(cx + sg * (ex + 1.6), ey - 0.2 + j * 0.55), (cx + sg * (ex + 2.4), ey - 0.5 + j * 0.8)], lw=0.3)
            f.curve([(cx + sg * 1.9, my + 2.0), (cx + sg * 2.6, my + 0.4)], lw=0.3)

def arm(f, pts, sleeve_w, skin_from=None, sleeve_fill=Wt, lw=0.9, sleeve_hatch=None, cuff=None):
    """Arm along pts (shoulder..wrist). skin_from = index where bare skin starts (rolled sleeves / short sleeves)."""
    n = len(pts); w = [sleeve_w * (1 - 0.28 * i / (n - 1)) for i in range(n)]; w[0] *= 0.72
    if skin_from is None:
        o = tube(pts, w, False); f.shape(o, lw=lw, fill=sleeve_fill)
        if sleeve_hatch: f.hatch(o, **sleeve_hatch)
        if sleeve_fill == K: f.curve(pts[1:], lw=0.3, color=Wt)
    else:
        sk = pts[skin_from - 1: ]; sw = [x * 0.8 for x in w[skin_from - 1:]]
        f.shape(tube(sk, sw), lw=lw)
        sl = pts[:skin_from + 0]; o = tube(sl, w[:skin_from], False); f.shape(o, lw=lw, fill=sleeve_fill)
        if sleeve_hatch: f.hatch(o, **sleeve_hatch)
    if cuff:
        i = cuff; (x0, y0), (x1, y1) = pts[i - 1], pts[i]; dx, dy = x1 - x0, y1 - y0; d = math.hypot(dx, dy) or 1
        ux, uy = dx / d, dy / d; nx, ny = -uy, ux; ww = w[i] * 1.12
        q = [(x1 - ux * 1.6 + nx * ww, y1 - uy * 1.6 + ny * ww), (x1 + nx * ww, y1 + ny * ww), (x1 - nx * ww, y1 - ny * ww), (x1 - ux * 1.6 - nx * ww, y1 - uy * 1.6 - ny * ww)]
        f.shape([(p[0], p[1], 0) for p in q], lw=0.7, fill=Wt)
        f.curve([((q[0][0] + q[1][0]) / 2, (q[0][1] + q[1][1]) / 2), ((q[2][0] + q[3][0]) / 2, (q[2][1] + q[3][1]) / 2)], lw=0.35)

def legs(f, x=3.4, top=22, w0=2.1, w1=1.55, ankle=3.0):
    for sg in (-1, 1):
        f.shape(tube([(sg * x, top), (sg * (x + 0.15), (top + ankle) / 2 + 2), (sg * (x - 0.1), ankle)], [w0, w0 * 0.9, w1]), lw=0.8)

# ============================================================================ characters
CY = 90.5   # head centre in the local frame

def agnes(k, x, y, h, expr="smile", flip=False, teapot=True):
    with Fig(k, x, y, h, flip) as f:
        legs(f, x=3.4, top=24, ankle=3.0)
        for sg in (-1, 1): shoe(f, sg * 3.3, sg)
        for sg in (-1, 1): f.curve([(sg * 2.3, 3.0), (sg * 3.2, 4.0), (sg * 4.4, 3.0)], lw=0.5)  # shoe straps
        dress = [(-2.6, 81.5), (-9.4, 79.4), (-11.0, 73), (-11.2, 63), (-12.2, 50), (-14.6, 24, 0.6), (-7, 22.6), (0, 22.2), (7, 22.6), (14.6, 24, 0.6), (12.2, 50), (11.2, 63), (11.0, 73), (9.4, 79.4), (2.6, 81.5)]
        f.shape(dress, lw=1.1)
        f.clip(dress)   # little sprig print
        for gy in range(24, 82, 5):
            for gx in range(-16, 17, 5):
                px = gx + (2.5 if (gy // 5) % 2 else 0) + f.r.uniform(-0.6, 0.6); py = gy + f.r.uniform(-0.6, 0.6)
                for a in (90, 210, 330): f.dot(px + 0.55 * math.cos(math.radians(a)), py + 0.55 * math.sin(math.radians(a)), 0.32)
        f.unclip()
        f.hatch(dress, angle=-60, gap=1.6, lw=0.3, box=(7, 20, 16, 82))
        f.shape(dress, lw=1.1, fill=None)
        # apron: bib, straps, gathered skirt with frill and pocket
        f.curve([(-4.6, 74), (-3.0, 79.8)], lw=0.9); f.curve([(4.6, 74), (3.0, 79.8)], lw=0.9)
        bib = [(-5.2, 74.5, 0), (5.2, 74.5, 0), (6.2, 62, 0), (-6.2, 62, 0)]
        f.shape(bib, lw=0.9)
        f.curve([(-4.2, 73.2), (4.2, 73.2)], lw=0.35)
        sk = [(-9.6, 61.5, 0), (9.6, 61.5, 0), (10.6, 45), (11.8, 28.5, 0), (-11.8, 28.5, 0), (-10.6, 45)]
        f.shape(sk, lw=0.9)
        for u in (-6, -2.5, 2.5, 6): f.curve([(u * 0.9, 60.5), (u * 1.05, 44), (u * 1.15, 31)], lw=0.3)
        fr = [(-12.2, 28.5, 0)]
        for j in range(12): fr += [(-12.2 + 24.4 * (j + 0.5) / 12, 26.1), (-12.2 + 24.4 * (j + 1) / 12, 28.0, 0)]
        f.shape(fr + [(12.2, 28.6, 0)], lw=0.8, t=0.9)
        f.hatch(fr + [(12.2, 28.6, 0)], angle=90, gap=1.1, lw=0.3)
        f.shape([(-11.2, 62.2, 0), (11.2, 62.2, 0), (11.2, 60.4, 0), (-11.2, 60.4, 0)], lw=0.8)   # waistband
        f.shape([(-3.6, 50, 0), (3.6, 50, 0), (3.4, 43.5), (0, 42.8), (-3.4, 43.5)], lw=0.7)          # pocket
        f.curve([(-3.4, 48.6), (3.4, 48.6)], lw=0.3)
        # collar
        for sg in (-1, 1): f.shape([(0, 79.0), (sg * 1.2, 81.6), (sg * 4.6, 80.8), (sg * 4.6, 78.6), (sg * 2.0, 77.6)], lw=0.7)
        f.dot(0, 77.4, 0.55, fill=Wt, lw=0.4)
        # arms: three-quarter sleeves; right arm holds the teapot forward
        arm(f, [(-9.4, 77.2), (-12.6, 70), (-13.4, 62.5), (-13.2, 55.5), (-12.9, 51.2)], 2.7, skin_from=4, sleeve_hatch=dict(angle=-60, gap=1.7, lw=0.3), cuff=3)
        hand(f, -12.9, 50.2, ang=-92, size=1.0)
        if teapot:
            arm(f, [(9.4, 77.2), (12.8, 70), (13.8, 63.0), (17.2, 61.6), (20.0, 61.4)], 2.7, skin_from=4, sleeve_hatch=dict(angle=-60, gap=1.7, lw=0.3), cuff=3)
            pot(f, 26.3, 57.8, 1.0)
            hand(f, 21.0, 61.3, ang=-10, size=0.95)
        else:
            arm(f, [(9.4, 77.2), (12.6, 70), (13.4, 62.5), (13.2, 55.5), (12.9, 51.2)], 2.7, skin_from=4, sleeve_hatch=dict(angle=-60, gap=1.7, lw=0.3), cuff=3)
            hand(f, 12.9, 50.2, ang=-88, size=1.0)
        neck(f, CY, w=2.2)
        # hair behind ears, bun on top
        f.shape(ell(0, CY + 9.2, 3.0, 2.6, n=18), lw=0.9)
        for j in range(3): f.curve(ell(0, CY + 9.2, 2.4 - j * 0.7, 2.0 - j * 0.55, 20, 300, 10), lw=0.35)
        head(f, 0, CY, rx=6.0, ry=7.3, jaw=0.66, expr=expr, glasses=True, nose="button", lines=2)
        hair = [(-6.5, CY - 0.6), (-7.0, CY + 3.0), (-6.0, CY + 6.6), (-3.2, CY + 8.4), (0, CY + 8.8), (3.2, CY + 8.4), (6.0, CY + 6.6), (7.0, CY + 3.0), (6.5, CY - 0.6),
                (5.6, CY + 2.6), (3.6, CY + 4.6), (0.6, CY + 5.0), (-1.6, CY + 5.8), (-4.4, CY + 4.6), (-5.7, CY + 2.4)]
        f.shape(hair, lw=0.9)
        for j in range(6):
            u = -5 + j * 2; f.curve([(u * 0.9, CY + 5.0 + 0.4 * (j % 2)), (u * 1.05, CY + 7.0), (u * 0.6, CY + 8.3)], lw=0.35)
        f.curve([(-5.9, CY + 2.0), (-6.6, CY + 4.2), (-5.2, CY + 6.6)], lw=0.35); f.curve([(5.9, CY + 2.0), (6.6, CY + 4.2), (5.2, CY + 6.6)], lw=0.35)
        f.dot(-5.9, CY - 2.6, 0.45, fill=Wt, lw=0.4); f.dot(5.9, CY - 2.6, 0.45, fill=Wt, lw=0.4)   # pearl earrings

def pot(f, x, y, s=1.0):
    """Round teapot in the figure frame (handle on the left at x - 5.4 s)."""
    body = ell(x, y, 5.2 * s, 4.3 * s, n=28)
    f.shape([(x + 4.4 * s, y + 0.6 * s), (x + 7.4 * s, y + 2.6 * s), (x + 8.9 * s, y + 5.4 * s), (x + 9.6 * s, y + 5.5 * s), (x + 8.4 * s, y + 3.2 * s), (x + 5.0 * s, y - 1.4 * s)], lw=0.8)
    f.curve(ell(x - 5.0 * s, y + 0.6 * s, 2.2 * s, 2.7 * s, 95, 265, 14), lw=1.1)
    f.shape(body, lw=1.0)
    f.hatch(body, angle=60, gap=1.2, lw=0.3, box=(x + 1.8 * s, y - 5 * s, x + 6 * s, y + 5 * s))
    band = [(x - 5.0 * s, y + 0.4 * s), (x + 5.0 * s, y + 0.4 * s), (x + 4.9 * s, y - 1.1 * s), (x - 4.9 * s, y - 1.1 * s)]
    f.clip(body); f.hatch([(p[0], p[1], 0) for p in band], angle=0, gap=0.7, lw=0.3); f.unclip()
    f.shape(ell(x, y + 4.0 * s, 2.8 * s, 0.8 * s, n=16), lw=0.7)
    f.shape(ell(x, y + 4.5 * s, 1.8 * s, 1.0 * s, 0, 180, 10) + [(x - 1.8 * s, y + 4.5 * s)], lw=0.7)
    f.dot(x, y + 5.7 * s, 0.6 * s, fill=K)
    f.curve([(x - 1.8 * s, y + 2.4 * s), (x - 3.4 * s, y + 0.8 * s)], lw=0.4, color=K)
    for j, dx in enumerate((8.6, 10.4)):   # steam
        f.curve([(x + dx * s, y + 7.0 * s), (x + (dx + 0.9) * s, y + 9.0 * s), (x + (dx - 0.5) * s, y + 10.8 * s), (x + (dx + 0.4) * s, y + 12.6 * s)], lw=0.4)

def ollie(k, x, y, h, expr="smile", flip=False):
    with Fig(k, x, y, h, flip) as f:
        trou = [(-8.0, 46, 0), (-7.8, 26), (-7.0, 3.4, 0), (-1.2, 3.4, 0), (-0.8, 36), (0.8, 36), (1.2, 3.4, 0), (7.0, 3.4, 0), (7.8, 26), (8.0, 46, 0)]
        f.shape(trou, lw=1.0, fill=K)
        for sg in (-1, 1): f.curve([(sg * 4.2, 34), (sg * 4.1, 6)], lw=0.3, color=Wt)
        for sg in (-1, 1): shoe(f, sg * 4.0, sg, "boot", top=4.0)
        tun = [(-2.9, 81.6), (-11.6, 79.0), (-12.6, 72), (-12.0, 60), (-12.8, 43.5, 0), (12.8, 43.5, 0), (12.0, 60), (12.6, 72), (11.6, 79.0), (2.9, 81.6)]
        f.shape(tun, lw=1.1, fill=K)
        f.curve([(0, 80.5), (0, 43.8)], lw=0.4, color=Wt)
        for by in (75.5, 69.5, 63.5, 50.0): f.dot(0.9, by, 0.75, fill=Wt, lw=0.35)
        for sg in (-1, 1):   # breast pockets
            px = sg * 6.6
            f.curve([(px - 3.0, 72.5), (px + 3.0, 72.5), (px + 3.0, 70.4), (px, 69.6), (px - 3.0, 70.4), (px - 3.0, 72.5)], lw=0.45, color=Wt, t=0.3)
            f.curve([(px - 3.0, 70.2), (px - 3.0, 64.5), (px + 3.0, 64.5), (px + 3.0, 70.2)], lw=0.35, color=Wt, t=0.3)
            f.dot(px, 70.6, 0.42, fill=Wt)
            f.curve([(sg * 3.6, 80.2), (sg * 10.4, 78.4)], lw=0.4, color=Wt)   # epaulette
        f.shape([(-12.9, 58.6, 0), (12.9, 58.6, 0), (12.9, 55.4, 0), (-12.9, 55.4, 0)], lw=0.5, fill=K)
        f.curve([(-12.6, 58.4), (12.6, 58.4)], lw=0.4, color=Wt); f.curve([(-12.6, 55.6), (12.6, 55.6)], lw=0.4, color=Wt)
        f.shape([(-2.2, 59.2, 0), (2.2, 59.2, 0), (2.2, 54.8, 0), (-2.2, 54.8, 0)], lw=0.5, fill=Wt)
        f.shape([(-1.2, 58.2, 0), (1.2, 58.2, 0), (1.2, 55.8, 0), (-1.2, 55.8, 0)], lw=0.4, fill=None)
        # collar with numbers
        f.shape([(-3.6, 80.0, 0), (-3.2, 83.2, 0), (3.2, 83.2, 0), (3.6, 80.0, 0), (0, 79.0)], lw=0.6, fill=K)
        f.curve([(-3.4, 80.2), (0, 79.3), (3.4, 80.2)], lw=0.35, color=Wt)
        for sg in (-1, 1):
            for j in range(2): f.shape([(sg * (1.4 + j * 0.8), 80.9, 0), (sg * (2.0 + j * 0.8), 80.9, 0), (sg * (2.0 + j * 0.8), 82.1, 0), (sg * (1.4 + j * 0.8), 82.1, 0)], lw=0.01, fill=Wt, stroke=False)
        # left arm down, right arm up holding a pocket notebook and pencil
        arm(f, [(-10.8, 77.6), (-13.6, 70), (-14.4, 62), (-14.2, 55), (-13.9, 50.8)], 2.9, sleeve_fill=K)
        f.curve([(-16.4, 52.6), (-11.5, 52.0)], lw=0.4, color=Wt)
        hand(f, -13.9, 49.6, ang=-92, size=1.05)
        arm(f, [(10.8, 77.6), (13.8, 70), (14.4, 62.5), (11.2, 63.2), (7.8, 64.6)], 2.9, sleeve_fill=K)
        nb = [(2.6, 62.6, 0), (8.6, 63.4, 0), (8.0, 71.8, 0), (2.0, 71.0, 0)]
        f.shape(nb, lw=0.8)
        for j in range(4): f.curve([(3.0, 64.6 + j * 1.6), (7.6, 65.2 + j * 1.6)], lw=0.3)
        f.shape([(2.0, 71.0, 0), (8.0, 71.8, 0), (8.0, 72.6, 0), (2.0, 71.8, 0)], lw=0.5, fill=K)
        hand(f, 8.3, 65.0, ang=165, size=1.0)
        neck(f, CY, w=2.4)
        head(f, 0, CY, rx=6.2, ry=7.3, jaw=0.7, expr=expr, nose="button", brows="soft")
        for sg in (-1, 1): f.shape([(sg * 6.2, CY + 3.6, 0), (sg * 6.5, CY + 0.6), (sg * 5.6, CY + 0.4), (sg * 5.5, CY + 3.4, 0)], lw=0.4, fill=K)
        # custodian helmet
        hel = [(-6.9, CY + 3.9, 0), (-7.2, CY + 8.6), (-6.0, CY + 13.8), (-3.2, CY + 17.0), (0, CY + 17.8), (3.2, CY + 17.0), (6.0, CY + 13.8), (7.2, CY + 8.6), (6.9, CY + 3.9, 0)]
        f.shape(hel, lw=1.0, fill=K)
        f.curve([(-5.3, CY + 6.0), (-5.6, CY + 10.4), (-4.2, CY + 14.2), (-2.4, CY + 15.8)], lw=0.6, color=Wt)
        f.curve([(0, CY + 17.8), (0, CY + 14.4)], lw=0.35, color=Wt)
        f.shape([(-1.0, CY + 17.6, 0), (1.0, CY + 17.6, 0), (0.9, CY + 19.2), (0, CY + 19.7), (-0.9, CY + 19.2)], lw=0.5, fill=K)
        f.shape([(-8.0, CY + 4.4), (0, CY + 5.0), (8.0, CY + 4.4), (7.6, CY + 3.0), (0, CY + 3.0), (-7.6, CY + 3.0)], lw=0.7, fill=K)
        f.curve([(-7.4, CY + 3.7), (0, CY + 4.05), (7.4, CY + 3.7)], lw=0.3, color=Wt)
        # Brunswick star badge
        bx, by, R = 0, CY + 9.4, 2.9
        star = []
        for i in range(16):
            a = math.pi / 2 + 2 * math.pi * i / 16; rr = R if i % 2 == 0 else R * 0.68
            star.append((bx + rr * math.cos(a), by + rr * math.sin(a), 0))
        f.shape(star, lw=0.45, fill=Wt)
        f.ring(bx, by, R * 0.45, lw=0.4, fill=K); f.dot(bx, by, R * 0.18, fill=Wt)
        f.curve([(-6.4, CY + 3.0), (-5.6, CY - 4.4), (-2.0, CY - 7.0), (2.0, CY - 7.0), (5.6, CY - 4.4), (6.4, CY + 3.0)], lw=0.45)   # chin strap

def morwenna(k, x, y, h, expr="neutral", flip=False):
    with Fig(k, x, y, h, flip) as f:
        hair_back = [(-6.6, CY + 3), (-8.2, CY - 4), (-8.8, CY - 10), (-9.6, CY - 15.5), (-6.4, CY - 17.0), (0, CY - 16.2), (6.4, CY - 17.0), (9.6, CY - 15.5), (8.8, CY - 10), (8.2, CY - 4), (6.6, CY + 3)]
        f.shape(hair_back, lw=0.9, fill=K)
        for j in range(5): f.curve([(-7.5 + j * 0.3, CY - 2 - j), (-8.4 + j * 0.4, CY - 9 - j * 0.6), (-8.0 + j * 0.5, CY - 15 + j * 0.3)], lw=0.3, color=Wt)
        legs(f, x=3.0, top=24, w0=1.9, w1=1.5, ankle=8)
        for sg in (-1, 1):   # gardening wellies
            f.shape([(sg * 0.9, 13.5, 0), (sg * 5.3, 13.5, 0), (sg * 5.0, 3.0), (sg * 7.4, 1.6), (sg * 7.6, 0.2, 0), (sg * 0.6, 0.2, 0), (sg * 0.9, 3.0)], lw=0.9, fill=K)
            f.curve([(sg * 1.1, 12.4), (sg * 5.1, 12.4)], lw=0.35, color=Wt); f.curve([(sg * 0.9, 1.0), (sg * 7.2, 1.0)], lw=0.35, color=Wt)
        dress = [(-2.6, 81.0), (-8.8, 79.0), (-9.6, 72), (-8.2, 60), (-9.6, 44), (-12.6, 21.5, 0.6), (0, 20.6), (12.6, 21.5, 0.6), (9.6, 44), (8.2, 60), (9.6, 72), (8.8, 79.0), (2.6, 81.0)]
        f.shape(dress, lw=1.1)
        f.clip(dress)   # flower print
        for gy in range(22, 82, 6):
            for gx in range(-14, 15, 6):
                px = gx + (3 if (gy // 6) % 2 else 0) + f.r.uniform(-0.8, 0.8); py = gy + f.r.uniform(-0.8, 0.8)
                for a in range(0, 360, 72): f.shape(ell(px + 0.8 * math.cos(math.radians(a)), py + 0.8 * math.sin(math.radians(a)), 0.55, 0.55, n=8), lw=0.3)
                f.dot(px, py, 0.4)
        f.unclip()
        f.shape(dress, lw=1.1, fill=None)
        for sg in (-1, 1):   # open cardigan, ribbed, to the hip
            pan = [(sg * 2.4, 81.0, 0), (sg * 8.9, 79.2), (sg * 10.0, 72), (sg * 9.4, 60), (sg * 10.4, 42.5, 0), (sg * 4.4, 42.0, 0), (sg * 3.6, 58), (sg * 2.4, 72)]
            f.shape(pan, lw=1.0)
            f.hatch(pan, angle=90, gap=1.1, lw=0.28)
            f.shape([(sg * 4.4, 44.6, 0), (sg * 10.3, 45.0, 0), (sg * 10.4, 42.5, 0), (sg * 4.4, 42.0, 0)], lw=0.6)
        for by in (74, 66, 58, 50): f.dot(-3.4, by, 0.6, fill=Wt, lw=0.4)
        # right arm cradles a bunch of sweet peas; left arm down
        arm(f, [(-8.9, 77.2), (-11.8, 70), (-12.6, 62), (-12.4, 55), (-12.0, 51.5)], 2.4, sleeve_hatch=dict(angle=90, gap=1.1, lw=0.28), cuff=4)
        hand(f, -12.0, 50.4, ang=-92, size=0.95)
        arm(f, [(8.9, 77.2), (12.2, 70), (12.6, 62.5), (9.0, 61.4), (5.4, 62.6)], 2.4, sleeve_hatch=dict(angle=90, gap=1.1, lw=0.28), cuff=4)
        sweetpeas(f, 1.0, 62.0)
        hand(f, 5.2, 63.0, ang=170, size=0.95)
        neck(f, CY, w=2.0)
        head(f, 0, CY, rx=5.8, ry=7.3, jaw=0.6, expr=expr, nose="small")
        for sg in (-1, 1):   # front locks framing the face
            f.shape([(sg * 1.0, CY + 6.4), (sg * 4.6, CY + 6.6), (sg * 6.9, CY + 3.0), (sg * 7.4, CY - 4.0), (sg * 7.8, CY - 9.5), (sg * 6.2, CY - 6.0), (sg * 5.9, CY - 1.0), (sg * 5.2, CY + 3.2), (sg * 2.8, CY + 4.6)], lw=0.6, fill=K)
            f.curve([(sg * 6.4, CY + 2.0), (sg * 6.9, CY - 4.0), (sg * 7.1, CY - 8.0)], lw=0.3, color=Wt)
        # wide straw hat with a ribbon bow
        brim = ell(0, CY + 5.8, 14.2, 2.9, n=36)
        crown = [(-6.3, CY + 6.4, 0), (-6.6, CY + 9.5), (-5.0, CY + 12.2), (0, CY + 12.9), (5.0, CY + 12.2), (6.6, CY + 9.5), (6.3, CY + 6.4, 0)]
        f.shape(brim, lw=1.0)
        for i in range(36):
            a = math.radians(i * 10); f.curve([(8.4 * math.cos(a), CY + 5.8 + 1.7 * math.sin(a)), (13.6 * math.cos(a), CY + 5.8 + 2.75 * math.sin(a))], lw=0.3)
        f.shape(crown, lw=1.0)
        f.hatch(crown, angle=30, gap=1.3, lw=0.28, cross=True)
        band = [(-6.4, CY + 6.4, 0), (6.4, CY + 6.4, 0), (6.5, CY + 8.4, 0), (-6.5, CY + 8.4, 0)]
        f.shape(band, lw=0.5, fill=K)
        f.shape([(4.0, CY + 7.4), (6.6, CY + 9.2), (6.8, CY + 6.0)], lw=0.5, fill=K); f.shape([(4.0, CY + 7.4), (6.0, CY + 4.4), (7.6, CY + 5.0)], lw=0.5, fill=K)
        f.shape(ell(0, CY + 5.8, 14.2, 2.9, 180, 360, 18) + [(14.2, CY + 5.8), (6.3, CY + 6.4), (-6.3, CY + 6.4)], lw=0.01, fill=None, stroke=False)
        f.curve(ell(0, CY + 5.8, 14.2, 2.9, 180, 360, 18), lw=1.0)

def sweetpeas(f, x, y):
    """Bunch of ruffled sweet peas with twining stems, held at (x, y) in the figure frame."""
    for j in range(7):
        a = math.radians(100 + j * 9); L = 7.5 + (j % 3) * 1.2
        f.curve([(x + 1.0, y), (x + 1.0 + 0.5 * L * math.cos(a), y + 0.5 * L * math.sin(a)), (x + L * math.cos(a), y + L * math.sin(a))], lw=0.45)
    for j in range(9):
        a = math.radians(96 + j * 7.5); L = 7.8 + (j % 3) * 1.6; px, py = x + L * math.cos(a), y + L * math.sin(a)
        petals = [(px - 1.6, py), (px - 1.2, py + 1.3), (px, py + 1.8), (px + 1.2, py + 1.3), (px + 1.6, py), (px + 0.6, py - 0.9), (px - 0.6, py - 0.9)]
        f.shape(petals, lw=0.5, fill=K if j % 3 == 1 else Wt)
        f.curve([(px - 0.9, py + 0.2), (px, py + 1.0), (px + 0.9, py + 0.2)], lw=0.3, color=Wt if j % 3 == 1 else K)
    f.curve([(x - 3.0, y + 9.6), (x - 4.6, y + 10.8), (x - 4.0, y + 12.2), (x - 3.0, y + 11.6)], lw=0.35)   # tendril
    f.shape([(x - 0.6, y + 2.6), (x + 3.0, y + 2.8), (x + 2.6, y - 1.2), (x - 0.2, y - 1.4)], lw=0.5)   # ribbon tie
    f.hatch([(x - 0.6, y + 2.6), (x + 3.0, y + 2.8), (x + 2.6, y - 1.2), (x - 0.2, y - 1.4)], angle=0, gap=0.8, lw=0.3)

def hedley(k, x, y, h, expr="neutral", flip=False, chair=True):
    with Fig(k, x, y, h, flip) as f:
        if chair: folding_chair(f, -21.5, 0)
        trou = [(-8.2, 52, 0), (-7.9, 26), (-7.3, 3.6, 0), (-1.2, 3.6, 0), (-0.8, 40), (0.8, 40), (1.2, 3.6, 0), (7.3, 3.6, 0), (7.9, 26), (8.2, 52, 0)]
        f.shape(trou, lw=1.0)
        f.hatch(trou, angle=88, gap=1.4, lw=0.28); f.hatch(trou, angle=-2, gap=2.6, lw=0.22)
        f.shape(trou, lw=1.0, fill=None)
        for sg in (-1, 1): shoe(f, sg * 4.2, sg, "boot", top=4.6)
        shirt = [(-2.8, 82.4), (-11.6, 80.0), (-12.2, 72), (-10.4, 60), (-9.2, 50.5, 0), (9.2, 50.5, 0), (10.4, 60), (12.2, 72), (11.6, 80.0), (2.8, 82.4)]
        f.shape(shirt, lw=1.1)
        for sg in (-1, 1): f.shape([(0, 79.0, 0), (sg * 0.8, 83.4, 0), (sg * 3.6, 82.2, 0), (sg * 2.6, 78.4, 0)], lw=0.6)
        vest = [(-4.0, 79.2, 0), (-9.8, 77.6), (-10.4, 66), (-9.4, 51.0), (-8.6, 48.4, 0), (-0.5, 46.4, 0), (0.5, 46.4, 0), (8.6, 48.4, 0), (9.4, 51.0), (10.4, 66), (9.8, 77.6), (4.0, 79.2, 0), (0, 63.0, 0)]
        f.shape(vest, lw=1.0)
        f.hatch(vest, angle=45, gap=1.1, lw=0.3, cross=True)
        f.shape(vest, lw=1.0, fill=None)
        f.curve([(0, 63), (0, 46.4)], lw=0.5)
        for by in (61, 57, 53, 49.2): f.dot(0.9, by, 0.62, fill=Wt, lw=0.4)
        for sg in (-1, 1): f.shape([(sg * 3.4, 56.2, 0), (sg * 7.8, 56.6, 0), (sg * 7.8, 55.2, 0), (sg * 3.4, 54.8, 0)], lw=0.4, fill=Wt)
        f.curve([(-3.6, 55.2), (-5.4, 53.6), (-7.0, 54.0)], lw=0.4)   # watch chain
        # sleeves rolled to the elbow, both arms down; left hand rests on the chair back
        arm(f, [(-10.4, 78.4), (-13.8, 70), (-16.0, 61.5), (-18.0, 54), (-19.6, 47.8)], 2.6, skin_from=3, cuff=2)
        for j in range(3): f.curve([(-14.6 + j * 0.9, 66 - j * 1.6), (-13.0 + j * 0.9, 68.5 - j * 1.6)], lw=0.3)
        hand(f, -20.0, 46.6, ang=-115, size=1.05)
        arm(f, [(10.4, 78.4), (12.9, 70), (14.0, 61.5), (14.0, 55), (13.6, 50.0)], 2.6, skin_from=3, cuff=2)
        for j in range(3): f.curve([(12.0 + j * 0.9, 74 - j * 2), (13.8 + j * 0.6, 72.6 - j * 2)], lw=0.3)
        hand(f, 13.6, 48.8, ang=-90, size=1.05)
        neck(f, CY, w=2.3, base=80.5)
        head(f, 0, CY, rx=5.9, ry=7.8, jaw=0.72, expr=expr, nose="long", brows="thick", lines=2, moustache=True)
        for sg in (-1, 1):   # grey hair over the ears
            f.shape([(sg * 5.4, CY + 3.8), (sg * 6.6, CY + 3.0), (sg * 6.8, CY - 0.6), (sg * 6.0, CY - 1.2), (sg * 5.6, CY + 1.2)], lw=0.6)
            for j in range(3): f.curve([(sg * (5.7 + j * 0.3), CY + 3.2 - j * 0.3), (sg * (6.3 + j * 0.15), CY - 0.4)], lw=0.3)
        cap = [(-6.8, CY + 3.6, 0), (-7.6, CY + 6.6), (-5.4, CY + 9.4), (0, CY + 10.0), (5.6, CY + 9.2), (8.4, CY + 6.6), (7.0, CY + 4.2, 0)]
        f.shape(cap, lw=1.0)
        f.hatch(cap, angle=55, gap=1.2, lw=0.3); f.hatch(cap, angle=-55, gap=1.2, lw=0.3, box=(-8, CY + 3, 0, CY + 11))
        f.shape(cap, lw=1.0, fill=None)
        f.curve([(-5.0, CY + 7.6), (0.4, CY + 8.0), (6.4, CY + 6.2)], lw=0.4)
        f.dot(0.6, CY + 9.8, 0.55, fill=K)
        f.shape([(-6.9, CY + 3.8), (0, CY + 4.6), (7.2, CY + 4.0), (7.6, CY + 2.4), (0, CY + 2.5), (-6.6, CY + 2.6)], lw=0.8, fill=K)

def folding_chair(f, x, y):
    """Wooden slatted folding chair standing on the floor, front view, in the figure frame."""
    lw = 0.9
    for sx in (-6.5, 6.5):
        f.shape([(x + sx - 0.8, y + 47, 0), (x + sx + 0.8, y + 47, 0), (x + sx * 1.08 + 0.8, y, 0), (x + sx * 1.08 - 0.8, y, 0)], lw=lw)
    for yy in (44.5, 40.5, 36.5):
        f.shape([(x - 6.8, yy, 0), (x + 6.8, yy, 0), (x + 6.8, yy - 2.6, 0), (x - 6.8, yy - 2.6, 0)], lw=0.7)
        f.hatch([(x - 6.8, yy, 0), (x + 6.8, yy, 0), (x + 6.8, yy - 2.6, 0), (x - 6.8, yy - 2.6, 0)], angle=2, gap=1.0, lw=0.25)
    f.shape([(x - 8.4, 25, 0), (x + 8.4, 25, 0), (x + 7.4, 22, 0), (x - 7.4, 22, 0)], lw=0.8)
    f.hatch([(x - 8.4, 25, 0), (x + 8.4, 25, 0), (x + 7.4, 22, 0), (x - 7.4, 22, 0)], angle=0, gap=0.9, lw=0.25)
    f.curve([(x - 6.2, 21.5), (x + 6.6, 4)], lw=0.8); f.curve([(x + 6.2, 21.5), (x - 6.6, 4)], lw=0.8)
    f.dot(x, 13.2, 0.6, fill=K)

def jago(k, x, y, h, expr="neutral", flip=False, basket=True):
    with Fig(k, x, y, h, flip) as f:
        trou = [(-8.6, 30, 0), (-8.0, 3.6, 0), (-1.4, 3.6, 0), (-0.9, 26), (0.9, 26), (1.4, 3.6, 0), (8.0, 3.6, 0), (8.6, 30, 0)]
        f.shape(trou, lw=1.0); f.hatch(trou, angle=45, gap=1.0, lw=0.32, cross=True); f.shape(trou, lw=1.0, fill=None)
        for sg in (-1, 1): shoe(f, sg * 4.6, sg, top=3.6)
        shirt = [(-3.2, 82.0), (-12.8, 79.4), (-13.6, 71), (-13.0, 60), (-12.4, 46, 0), (12.4, 46, 0), (13.0, 60), (13.6, 71), (12.8, 79.4), (3.2, 82.0)]
        f.shape(shirt, lw=1.1)
        f.hatch(shirt, angle=90, gap=1.9, lw=0.32)
        f.shape(shirt, lw=1.1, fill=None)
        for sg in (-1, 1): f.shape([(0, 78.6, 0), (sg * 1.0, 83.0, 0), (sg * 4.0, 81.6, 0), (sg * 2.8, 78.0, 0)], lw=0.6)
        f.curve([(-3.6, 75.5), (-5.5, 80.8)], lw=0.9); f.curve([(3.6, 75.5), (5.5, 80.8)], lw=0.9)   # apron straps
        apr = [(-6.2, 75.8, 0), (6.2, 75.8, 0), (7.0, 62, 0), (11.4, 58.0, 0), (12.4, 40), (12.8, 19.0, 0), (-12.8, 19.0, 0), (-12.4, 40), (-11.4, 58.0, 0), (-7.0, 62, 0)]
        f.shape(apr, lw=1.0)
        f.curve([(-11.4, 57.6), (-14.2, 55.2), (-13.6, 52.6)], lw=0.6); f.curve([(11.4, 57.6), (14.0, 54.6)], lw=0.6)
        for u in (-7.5, -3, 3, 7.5): f.curve([(u * 0.8, 56), (u, 38), (u * 1.05, 21)], lw=0.28)
        f.shape([(-4.6, 72.2, 0), (-0.8, 72.2, 0), (-0.8, 67.6, 0), (-4.6, 67.6, 0)], lw=0.6)   # bib pocket with pencil
        f.curve([(-3.6, 72.0), (-3.0, 74.8)], lw=0.9)
        for i in range(16): f.ring(f.r.uniform(-11, 11), f.r.uniform(22, 70), f.r.uniform(0.25, 0.6), lw=0.25)   # flour dust
        # rolled sleeves, floury forearms, both hands carrying a bread basket
        for sg in (-1, 1):
            if basket: cl = [(sg * 11.4, 78.4), (sg * 14.4, 70), (sg * 15.4, 61.5), (sg * 13.4, 56.8), (sg * 9.8, 55.0)]
            else: cl = [(sg * 11.4, 78.4), (sg * 14.4, 70), (sg * 15.6, 61.5), (sg * 15.4, 55), (sg * 15.0, 50.4)]
            arm(f, cl, 3.0, skin_from=3, cuff=2, sleeve_hatch=dict(angle=90, gap=1.9, lw=0.32))
            for j in range(5): f.ring(sg * (14.0 + f.r.uniform(-1.0, 1.4)), f.r.uniform(53.5, 59.5), 0.35, lw=0.25)
        if basket:
            bread_basket(f, 0, 48.6)
            for sg in (-1, 1): hand(f, sg * 9.4, 54.6, ang=-90 + sg * 70, size=1.05)
        else:
            for sg in (-1, 1): hand(f, sg * 15.0, 49.2, ang=-90, size=1.05)
        neck(f, CY, w=2.7)
        head(f, 0, CY, rx=6.6, ry=7.3, jaw=0.78, expr=expr, nose="button", brows="thick", beard=True, blush=(expr == "sheepish"))
        for sg in (-1, 1): f.shape([(sg * 6.4, CY + 4.2, 0), (sg * 6.9, CY + 0.4), (sg * 6.0, CY + 0.2), (sg * 5.8, CY + 3.6, 0)], lw=0.4, fill=K)
        # baker's toque: band + pleated puff
        band = [(-6.6, CY + 3.6, 0), (6.6, CY + 3.6, 0), (6.9, CY + 7.4, 0), (-6.9, CY + 7.4, 0)]
        puff = [(-6.8, CY + 7.0), (-9.2, CY + 9.6), (-9.0, CY + 13.4), (-6.0, CY + 15.8), (-2.6, CY + 16.4), (0, CY + 17.4), (2.8, CY + 16.4), (6.2, CY + 15.8), (9.0, CY + 13.4), (9.2, CY + 9.6), (6.8, CY + 7.0)]
        f.shape(puff, lw=1.0)
        for u in (-5.6, -2.8, 0, 2.8, 5.6): f.curve([(u * 0.95, CY + 7.6), (u * 1.2, CY + 11.6), (u * 1.0, CY + 15.6)], lw=0.35)
        f.hatch(puff, angle=60, gap=1.3, lw=0.28, box=(5.0, CY + 6, 10, CY + 18))
        f.shape(band, lw=0.9)
        for u in range(-6, 7, 2): f.curve([(u, CY + 3.8), (u + 0.1, CY + 7.2)], lw=0.3)

def bread_basket(f, x, y):
    """Wicker basket with a cob loaf and a baguette (figure frame)."""
    f.shape([(x - 4.6, y + 7.0), (x + 5.4, y + 13.6), (x + 7.0, y + 12.4), (x - 3.0, y + 5.4)], lw=0.8)        # baguette
    for j in range(4): f.curve([(x - 2.4 + j * 2.4, y + 7.6 + j * 1.6), (x - 1.0 + j * 2.4, y + 7.0 + j * 1.6)], lw=0.4)
    f.shape(ell(x + 1.2, y + 7.4, 5.0, 3.6, 0, 180, 16) + [(x - 3.8, y + 7.4)], lw=0.9)                        # cob
    f.curve([(x - 1.4, y + 8.6), (x + 1.2, y + 10.2), (x + 3.4, y + 8.8)], lw=0.4)
    f.hatch(ell(x + 1.2, y + 7.4, 5.0, 3.6, 0, 180, 16) + [(x - 3.8, y + 7.4)], angle=70, gap=1.2, lw=0.28, box=(x + 3, y, x + 7, y + 12))
    bk = [(x - 11.0, y + 7.6, 0), (x + 11.0, y + 7.6, 0), (x + 9.0, y - 0.6, 0.6), (x - 9.0, y - 0.6, 0.6)]
    f.shape(bk, lw=1.0)
    f.hatch(bk, angle=60, gap=1.1, lw=0.32); f.hatch(bk, angle=-60, gap=2.2, lw=0.3)
    f.shape(bk, lw=1.0, fill=None)
    f.shape([(x - 11.4, y + 8.6, 0), (x + 11.4, y + 8.6, 0), (x + 11.0, y + 7.0, 0), (x - 11.0, y + 7.0, 0)], lw=0.7)
    f.hatch([(x - 11.4, y + 8.6, 0), (x + 11.4, y + 8.6, 0), (x + 11.0, y + 7.0, 0), (x - 11.0, y + 7.0, 0)], angle=-70, gap=0.9, lw=0.3)

CHARACTERS = dict(agnes=agnes, ollie=ollie, morwenna=morwenna, hedley=hedley, jago=jago)
