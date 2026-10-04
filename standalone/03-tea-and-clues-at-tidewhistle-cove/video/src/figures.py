"""figures: the SIMPLE peg-doll characters from the v1 video (commit ec8f22c, Ink.figure), now in colour.

Same call signature as people.py (the detailed v2 characters), so scenes can switch between them:

  agnes(k, x, y, h)      Agnes Bell: grey hair in a bun, round glasses, lavender dress, white apron, teapot
  ollie(k, x, y, h)      Constable Ollie Penrose: navy tunic and custodian helmet, brass buttons
  morwenna(k, x, y, h)   Morwenna Day: straw hat, long dark hair, sage flower dress, sweet peas
  hedley(k, x, y, h)     Hedley Truscott: flat cap, tweed jacket, folding chair
  jago(k, x, y, h)       Jago Penhallow: baker's toque and whites, blue striped apron, bread basket

(x, y) is between the feet, h is the figure height. Round head, dot eyes, a small smile, a trapezoid
body and line arms and legs, exactly the v1 construction; colour comes from k.tint() (colorink.py).
The three suspects share one face, one stance, one height, one prop-in-hand pose and the same colour
weight, so nothing singles anyone out before the solution. expr="sheepish" is for post-solution scenes."""
from colorink import PAL, K, Wt, shade

def _flip(k, x, flip):
    if flip:
        k.c.saveState(); k.c.translate(2 * x, 0); k.c.scale(-1, 1)
    return flip

def _unflip(k, flip):
    if flip: k.c.restoreState()

def _geom(x, y, h):
    return dict(r=h * 0.1, hy=y + h * 0.75, sh=y + h * 0.62, hem=y + h * 0.14)

def _legs(k, x, y, h, shoe=K, sock=None):
    g = _geom(x, y, h)
    for sx in (-0.07, 0.07):
        k.line([(x + sx * h, g["hem"]), (x + sx * h, y + 1)], lw=1.2, amp=0)
        with k.tint(None, dark=shoe):
            k.shape(k.arcpts(x + sx * h + (h * 0.02 if sx > 0 else -h * 0.02), y + 1, h * 0.04, h * 0.018, 0, 360, 12), lw=0.6, fill=K, amp=0)

def _body(k, x, y, h, fill, dark=None, hatch=None, hatch_kw=None):
    g = _geom(x, y, h)
    body = [(x - h * 0.13, g["sh"]), (x + h * 0.13, g["sh"]), (x + h * 0.21, g["hem"]), (x - h * 0.21, g["hem"])]
    with k.tint(fill, dark=dark, hatch=hatch):
        k.shape(body, lw=1.0, fill=Wt, amp=0.15)
        if hatch_kw: k.hatch(body, **hatch_kw)
    return body

def _arms(k, x, y, h, hold=True, skin=None):
    """Line arms with round hands; with hold=True the right arm bends forward to carry a prop.
    Returns the carry point (x, y)."""
    g = _geom(x, y, h); sh = g["sh"]; skin = skin or PAL.skin
    for sg in (-1, 1):
        if hold and sg == 1:
            pts = [(x + h * 0.12, sh - 1), (x + h * 0.22, sh - h * 0.16), (x + h * 0.3, sh - h * 0.12)]
            k.line(pts, lw=1.3, amp=0)
            with k.tint(skin): k.circle(pts[-1][0] + h * 0.012, pts[-1][1], h * 0.022, lw=0.5, fill=Wt)
        else:
            k.line([(x + sg * h * 0.12, sh - 1), (x + sg * h * 0.2, sh - h * 0.3)], lw=1.3, amp=0)
            with k.tint(skin): k.circle(x + sg * h * 0.2, sh - h * 0.31, h * 0.022, lw=0.5, fill=Wt)
    return (x + h * 0.3, sh - h * 0.12)

def _face(k, x, y, h, expr="smile", skin=None):
    g = _geom(x, y, h); r, hy = g["r"], g["hy"]
    with k.tint(skin or PAL.skin): k.circle(x, hy, r, lw=1.0, fill=Wt)
    sheep = expr == "sheepish"
    ck = PAL.blush if sheep else PAL.cheek
    for sx in (-0.56, 0.56):
        k.c.setFillColor(ck); k.c.circle(x + sx * r, hy - r * 0.28, r * (0.2 if sheep else 0.15), stroke=0, fill=1)
    k.c.setStrokeColor(K)
    if sheep:   # eyes looking down, small wobbly mouth, blush lines
        k.c.setLineWidth(0.6)
        for sx in (-0.35, 0.35): k.c.arc(x + sx * r - r * 0.12, hy - r * 0.12, x + sx * r + r * 0.12, hy + r * 0.12, 200, 140)
        k.line([(x - r * 0.22, hy - r * 0.42), (x - r * 0.08, hy - r * 0.36), (x + r * 0.08, hy - r * 0.44), (x + r * 0.22, hy - r * 0.38)], lw=0.6, amp=0)
        for sx in (-1, 1):
            for j in range(3):
                bx = x + sx * r * (0.42 + 0.12 * j); k.line([(bx, hy - r * 0.2), (bx - sx * r * 0.06, hy - r * 0.36)], lw=0.35, amp=0, color=shade(PAL.blush, 0.8))
    else:
        for sx in (-0.35, 0.35): k.circle(x + sx * r, hy + r * 0.05, r * 0.08 + 0.2, lw=0, fill=K, stroke=False)
        k.c.setStrokeColor(K); k.c.setLineWidth(0.6); k.c.arc(x - r * 0.3, hy - r * 0.55, x + r * 0.3, hy - r * 0.1, 200, 140)

# ----------------------------------------------------------------------------- props
def teapot_prop(k, x, y, w):
    with k.tint(PAL.teapot): k.teapot(x, y, w)

def sweetpeas(k, x, y, s):
    """Posy of sweet peas held at (x, y); s = figure height."""
    import math
    stems = []
    for i in range(7):
        a = math.radians(62 + i * 9); L = s * (0.13 + 0.03 * (i % 3))
        stems.append((x + L * math.cos(a), y + L * math.sin(a)))
    for ex, ey in stems: k.line([(x, y - s * 0.03), (ex, ey)], lw=0.6, amp=0.1, color=shade(PAL.leaf, 0.8))
    cols = [PAL.pea_pink, PAL.pea_purple, PAL.pea_white, PAL.pea_pink, PAL.pea_purple, PAL.pea_pink, PAL.pea_purple]
    for (ex, ey), cl in zip(stems, cols):
        with k.tint(cl):
            for j in range(2):
                k.shape(k.arcpts(ex + (j - 0.5) * s * 0.014, ey + j * s * 0.01, s * 0.016, s * 0.013, 0, 360, 10), lw=0.5, fill=Wt, amp=0)
    with k.tint(PAL.leaf):
        k.shape([(x - s * 0.012, y - s * 0.035), (x + s * 0.012, y - s * 0.035), (x + s * 0.008, y + s * 0.015), (x - s * 0.008, y + s * 0.015)], lw=0.5, fill=Wt, amp=0)

def folding_chair(k, x, y, s):
    """Little slatted folding chair standing on the floor at (x, y); s = figure height."""
    w, hb, hs = s * 0.2, s * 0.5, s * 0.25
    with k.tint(PAL.wood):
        k.line([(x - w / 2, y), (x - w / 2, y + hb)], lw=1.6, amp=0, color=shade(PAL.wood_dk, 0.8))
        k.line([(x + w / 2, y), (x + w / 2, y + hb)], lw=1.6, amp=0, color=shade(PAL.wood_dk, 0.8))
        k.line([(x - w / 2, y + hs * 0.2), (x + w / 2, y + hs * 0.95)], lw=1.0, amp=0, color=shade(PAL.wood_dk, 0.8))
        k.rect(x - w / 2 - 1, y + hs, w + 2, s * 0.025, lw=0.7)
        for j in range(3): k.rect(x - w / 2, y + hb * (0.7 + 0.11 * j), w, s * 0.03, lw=0.7)

def bread_basket(k, x, y, s):
    """Wicker basket with loaves carried at (x, y); s = figure height."""
    w, hh = s * 0.17, s * 0.07
    with k.tint(PAL.bread):
        k.shape(k.arcpts(x - w * 0.18, y + hh * 0.9, w * 0.28, w * 0.2, 0, 180, 14) + [(x - w * 0.46, y + hh * 0.9)], lw=0.7, fill=Wt, amp=0)
        k.shape([(x + w * 0.05, y + hh * 0.8), (x + w * 0.42, y + hh * 1.9), (x + w * 0.5, y + hh * 1.7), (x + w * 0.16, y + hh * 0.7)], lw=0.7, fill=Wt, amp=0)
        for j in range(3): k.line([(x + w * (0.14 + 0.09 * j), y + hh * (1.0 + 0.24 * j)), (x + w * (0.2 + 0.09 * j), y + hh * (0.95 + 0.24 * j))], lw=0.4, amp=0)
    body = [(x - w / 2, y + hh), (x + w / 2, y + hh), (x + w * 0.4, y), (x - w * 0.4, y)]
    with k.tint(PAL.wicker):
        k.shape(body, lw=0.8, fill=Wt, amp=0)
        k.hatch(body, angle=0, gap=s * 0.012, lw=0.35)
    k.c.setStrokeColor(K); k.c.setLineWidth(0.9)
    k.c.arc(x - w * 0.42, y + hh * 0.2, x + w * 0.42, y + hh * 2.6, 20, 140)

# ----------------------------------------------------------------------------- characters
def agnes(k, x, y, h, expr="smile", flip=False, teapot=True):
    f = _flip(k, x, flip); g = _geom(x, y, h); r, hy, sh, hem = g["r"], g["hy"], g["sh"], g["hem"]
    _legs(k, x, y, h, shoe=PAL.bag_dk)
    _body(k, x, y, h, PAL.agnes_dress, hatch_kw=dict(angle=-55, gap=2.6, lw=0.35))
    with k.tint(PAL.apron):
        ap = [(x - h * 0.09, sh - h * 0.1), (x + h * 0.09, sh - h * 0.1), (x + h * 0.14, hem + h * 0.04), (x - h * 0.14, hem + h * 0.04)]
        k.shape(ap, lw=0.7, fill=Wt, amp=0.1)
        k.line([(x - h * 0.13, sh - h * 0.16), (x + h * 0.13, sh - h * 0.16)], lw=0.6, amp=0)
        k.rect(x - h * 0.05, sh - h * 0.3, h * 0.1, h * 0.07, lw=0.5)
    hx, hyy = _arms(k, x, y, h, hold=teapot)
    if teapot: teapot_prop(k, hx + h * 0.08, hyy - h * 0.05, h * 0.2)
    _face(k, x, y, h, expr)
    with k.tint(PAL.hair_grey):
        k.shape(k.arcpts(x, hy + r * 0.05, r * 1.04, r * 1.02, 15, 165, 20) + [(x - r * 0.6, hy + r * 0.55), (x + r * 0.6, hy + r * 0.55)], lw=0.6, fill=Wt, amp=0)
        k.circle(x, hy + r * 1.25, r * 0.42, lw=0.6, fill=Wt)
    for sx in (-0.38, 0.38): k.circle(x + sx * r, hy + r * 0.05, r * 0.26, lw=0.55, fill=None)
    k.line([(x - r * 0.12, hy + r * 0.08), (x + r * 0.12, hy + r * 0.08)], lw=0.5, amp=0)
    _unflip(k, f)

def ollie(k, x, y, h, expr="smile", flip=False):
    f = _flip(k, x, flip); g = _geom(x, y, h); r, hy, sh, hem = g["r"], g["hy"], g["sh"], g["hem"]
    _legs(k, x, y, h)
    _body(k, x, y, h, PAL.navy)
    for j in range(4): k.circle(x, sh - h * 0.08 - j * h * 0.09, h * 0.012 + 0.4, lw=0.4, fill=PAL.brass)
    k.c.setStrokeColor(PAL.navy_lt); k.c.setLineWidth(1.4); k.c.line(x - h * 0.19, hem + h * 0.14, x + h * 0.19, hem + h * 0.14); k.c.setStrokeColor(K)
    with k.tint(PAL.paper):   # pocket notebook in hand (same carry pose as everyone)
        hx, hyy = _arms(k, x, y, h, hold=True)
        k.rect(hx + h * 0.02, hyy - h * 0.02, h * 0.06, h * 0.08, lw=0.6)
        k.line([(hx + h * 0.03, hyy + h * 0.035), (hx + h * 0.07, hyy + h * 0.035)], lw=0.3, amp=0)
    _face(k, x, y, h, expr)
    with k.tint(PAL.navy, dark=PAL.navy):
        k.shape(k.arcpts(x, hy + r * 0.5, r * 0.95, r * 1.7, 0, 180, 24), lw=0.8, fill=K, amp=0)
        k.rect(x - r * 1.15, hy + r * 0.38, r * 2.3, r * 0.22, lw=0.6, fill=K)
        k.circle(x, hy + r * 2.25, r * 0.15, lw=0.5, fill=K)
    k.star5(x, hy + r * 1.15, r * 0.35, fill=PAL.silver, lw=0.4)
    _unflip(k, f)

def morwenna(k, x, y, h, expr="neutral", flip=False):
    f = _flip(k, x, flip); g = _geom(x, y, h); r, hy, sh, hem = g["r"], g["hy"], g["sh"], g["hem"]
    with k.tint(PAL.hair_dark):   # long hair, behind the head and shoulders
        k.shape([(x - r * 0.95, hy + r * 0.3), (x - r * 1.3, hy - r * 1.7), (x + r * 1.3, hy - r * 1.7), (x + r * 0.95, hy + r * 0.3)], lw=0.8, fill=Wt, amp=0.2)
    _legs(k, x, y, h, shoe=PAL.hair_dark)
    body = _body(k, x, y, h, PAL.sage, hatch_kw=dict(angle=90, gap=3.2, lw=0.3))
    import random
    rr = random.Random(11)
    for i in range(14):   # little flowers on the dress
        u, v = rr.uniform(0.1, 0.9), rr.uniform(0.08, 0.85)
        half = (h * 0.13) + (h * 0.08) * (1 - v)
        fx = x + (u - 0.5) * 2 * half * 0.85; fy = hem + v * (sh - hem)
        k.c.setFillColor(PAL.pea_pink if i % 2 else PAL.pea_white); k.c.circle(fx, fy, h * 0.009, stroke=0, fill=1)
    hx, hyy = _arms(k, x, y, h, hold=True)
    sweetpeas(k, hx + h * 0.01, hyy + h * 0.01, h)
    _face(k, x, y, h, expr)
    with k.tint(PAL.straw):
        k.shape(k.arcpts(x, hy + r * 0.6, r * 1.9, r * 0.38, 0, 360, 30), lw=0.8, fill=Wt, amp=0)
        k.shape(k.arcpts(x, hy + r * 0.7, r * 0.9, r * 0.8, 0, 180, 20), lw=0.8, fill=Wt, amp=0)
    with k.tint(PAL.pea_pink):
        k.shape([(x - r * 0.9, hy + r * 0.7), (x + r * 0.9, hy + r * 0.7), (x + r * 0.88, hy + r * 0.95), (x - r * 0.88, hy + r * 0.95)], lw=0.5, fill=Wt, amp=0)
    _unflip(k, f)

def hedley(k, x, y, h, expr="neutral", flip=False, chair=True):
    f = _flip(k, x, flip); g = _geom(x, y, h); r, hy, sh, hem = g["r"], g["hy"], g["sh"], g["hem"]
    if chair: folding_chair(k, x + h * 0.34, y, h)
    _legs(k, x, y, h, shoe=PAL.cap)
    _body(k, x, y, h, PAL.tweed, hatch_kw=dict(angle=45, gap=3.0, lw=0.3, cross=True))
    with k.tint(PAL.shirt):   # open collar
        k.shape([(x - h * 0.05, sh), (x + h * 0.05, sh), (x, sh - h * 0.07)], lw=0.6, fill=Wt, amp=0)
    hx, hyy = _arms(k, x, y, h, hold=True)
    _face(k, x, y, h, expr)
    with k.tint(PAL.cap, dark=PAL.cap):
        k.shape(k.arcpts(x, hy + r * 0.25, r * 1.02, r * 0.9, 0, 180, 20), lw=0.8, fill=Wt, amp=0)
        k.shape([(x + r * 0.2, hy + r * 0.35), (x + r * 1.7, hy + r * 0.3), (x + r * 1.6, hy + r * 0.5), (x + r * 0.3, hy + r * 0.62)], lw=0.6, fill=Wt, amp=0)
        k.hatch(k.arcpts(x, hy + r * 0.25, r * 1.02, r * 0.9, 0, 180, 20), angle=45, gap=2.4, lw=0.3, cross=True)
    _unflip(k, f)

def jago(k, x, y, h, expr="neutral", flip=False, basket=True):
    f = _flip(k, x, flip); g = _geom(x, y, h); r, hy, sh, hem = g["r"], g["hy"], g["sh"], g["hem"]
    _legs(k, x, y, h, shoe=PAL.crust)
    _body(k, x, y, h, PAL.baker)
    with k.tint(PAL.apron_blue):
        ap = [(x - h * 0.1, sh - h * 0.12), (x + h * 0.1, sh - h * 0.12), (x + h * 0.15, hem + h * 0.03), (x - h * 0.15, hem + h * 0.03)]
        k.shape(ap, lw=0.7, fill=Wt, amp=0.1)
        k.hatch(ap, angle=90, gap=3.2, lw=0.6, color=shade(PAL.apron_blue, 0.82))
        k.line([(x - h * 0.13, sh - h * 0.18), (x + h * 0.13, sh - h * 0.18)], lw=0.6, amp=0)
        k.shape([(x - h * 0.05, sh), (x + h * 0.05, sh), (x, sh - h * 0.06)], lw=0.6, fill=Wt, amp=0)   # neckerchief
    hx, hyy = _arms(k, x, y, h, hold=basket)
    if basket: bread_basket(k, hx + h * 0.04, hyy - h * 0.035, h)
    _face(k, x, y, h, expr)
    with k.tint(PAL.baker):
        k.rect(x - r * 0.75, hy + r * 0.6, r * 1.5, r * 0.6, lw=0.8)
        for dx in (-0.55, 0.0, 0.55): k.circle(x + dx * r, hy + r * 1.55, r * 0.55, lw=0.8, fill=Wt)
        k.rect(x - r * 0.75, hy + r * 0.6, r * 1.5, r * 0.6, lw=0.8)
    _unflip(k, f)

CHARACTERS = dict(agnes=agnes, ollie=ollie, morwenna=morwenna, hedley=hedley, jago=jago)
