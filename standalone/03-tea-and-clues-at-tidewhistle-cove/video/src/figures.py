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

_SEATED = [False]   # set by the seated() context: hips on a seat, knees forward, same head size

def _geom(x, y, h):
    if _SEATED[0]: return dict(r=h * 0.1, hy=y + h * 0.75, sh=y + h * 0.62, hem=y + h * 0.3)
    return dict(r=h * 0.1, hy=y + h * 0.75, sh=y + h * 0.62, hem=y + h * 0.14)

class seated:
    """with seated(): draw a character sitting (hips at y + 0.3 h on a bench / deckchair, shins down to y)."""
    def __enter__(s): _SEATED[0] = True
    def __exit__(s, *a): _SEATED[0] = False

def _legs(k, x, y, h, shoe=K, sock=None):
    g = _geom(x, y, h)
    if _SEATED[0]:   # 3/4 view: thighs forward to the right (drawn by _body as a lap), shins straight down
        for j, sx in enumerate((-0.07, 0.07)):
            kx = x + h * (0.24 + 0.05 * j)
            k.line([(kx, g["hem"] - h * 0.02), (kx, y + 1)], lw=1.2, amp=0)
            with k.tint(None, dark=shoe):
                k.shape(k.arcpts(kx + h * 0.025, y + 1, h * 0.04, h * 0.018, 0, 360, 12), lw=0.6, fill=K, amp=0)
        return
    for sx in (-0.07, 0.07):
        k.line([(x + sx * h, g["hem"]), (x + sx * h, y + 1)], lw=1.2, amp=0)
        with k.tint(None, dark=shoe):
            k.shape(k.arcpts(x + sx * h + (h * 0.02 if sx > 0 else -h * 0.02), y + 1, h * 0.04, h * 0.018, 0, 360, 12), lw=0.6, fill=K, amp=0)

def _body(k, x, y, h, fill, dark=None, hatch=None, hatch_kw=None):
    g = _geom(x, y, h)
    body = [(x - h * 0.13, g["sh"]), (x + h * 0.13, g["sh"]), (x + h * 0.21, g["hem"]), (x - h * 0.21, g["hem"])]
    with k.tint(fill, dark=dark, hatch=hatch):
        if _SEATED[0]:   # lap: the skirt / trousers run forward over the knees
            lap = [(x - h * 0.05, g["hem"] + h * 0.07), (x + h * 0.33, g["hem"] + h * 0.04), (x + h * 0.33, g["hem"] - h * 0.03), (x - h * 0.05, g["hem"] - h * 0.02)]
            k.shape(lap, lw=1.0, fill=Wt, amp=0.1)
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

# ----------------------------------------------------------------------------- Case 2 cast
from colorink import C as _C
LOVEDAY_DRESS = _C(244, 176, 156); DEMELZA_DRESS = _C(238, 150, 132); SUNHAT = _C(244, 214, 150); SUNHAT_BAND = _C(126, 180, 206)
QUILL_JUMPER = _C(96, 130, 166); QUILL_CAP = _C(48, 60, 92); LEDGER = _C(150, 72, 68); LINEN = _C(220, 200, 156); PANAMA = _C(240, 230, 204)
BOOK = _C(108, 160, 150); LEMONADE = _C(250, 236, 160); BEARD = _C(232, 230, 226)

def lemonade_glass(k, x, y, s, ice="none", frost=False, full=0.8):
    """Tumbler of lemonade standing at (x, y); s = height. ice: none | fresh (large sharp cubes) | melted."""
    w = s * 0.62
    body = [(x - w / 2, y + s), (x + w / 2, y + s), (x + w * 0.42, y), (x - w * 0.42, y)]
    k.shape(body, lw=0.8, fill=PAL.glass, amp=0)
    lv = y + s * full
    k.shape([(x - w * 0.42 - (w * 0.08) * full, lv), (x + w * 0.42 + (w * 0.08) * full, lv), (x + w * 0.42, y + 1), (x - w * 0.42, y + 1)], lw=0.4, fill=LEMONADE, amp=0)
    if ice == "fresh":
        for dx, dy, a in ((-0.2, 0.62, 12), (0.14, 0.66, -8), (-0.02, 0.45, 20)):
            cx, cy, r = x + dx * w, y + dy * s, w * 0.17
            import math
            pts = [(cx + r * math.cos(math.radians(a + 90 * i + 45)), cy + r * math.sin(math.radians(a + 90 * i + 45))) for i in range(4)]
            k.shape(pts, lw=0.7, fill=PAL.foam, amp=0)
            k.line([pts[0], (cx, cy)], lw=0.3, amp=0, color=PAL.sea2)
    elif ice == "melted":
        k.line([(x - w * 0.3, lv - s * 0.04), (x + w * 0.3, lv - s * 0.04)], lw=0.3, amp=0.2, color=shade(LEMONADE, 0.8))
    if frost:
        k.c.setFillColor(PAL.cloud)
        import random
        rr = random.Random(int(x * 10))
        for i in range(26):
            u = rr.uniform(-0.4, 0.4); v = rr.uniform(0.08, 0.95)
            k.c.circle(x + u * w * (0.84 + 0.16 * v), y + v * s, s * 0.018, stroke=0, fill=1)
        for sg in (-1, 1):
            k.line([(x + sg * w * 0.43, y + s * 0.15), (x + sg * w * 0.47, y + s * 0.85)], lw=0.9, amp=0, color=PAL.cloud)
    k.shape(body, lw=0.8, fill=None, amp=0)

def jug(k, x, y, s, level=0.75):
    """Glass jug of lemonade with lemon slices; s = height."""
    w = s * 0.62
    body = [(x - w * 0.42, y), (x + w * 0.42, y), (x + w * 0.5, y + s * 0.55), (x + w * 0.4, y + s), (x - w * 0.5, y + s), (x - w * 0.4, y + s * 0.55)]
    k.shape(body, lw=0.9, fill=PAL.glass, amp=0)
    lv = y + s * level
    k.shape([(x - w * 0.42, y + 1), (x + w * 0.42, y + 1), (x + w * 0.5, y + s * 0.55), (x + w * 0.45, lv), (x - w * 0.45, lv), (x - w * 0.4, y + s * 0.55)], lw=0.4, fill=LEMONADE, amp=0)
    for dx, dy in ((-0.15, 0.3), (0.18, 0.5)):
        k.circle(x + dx * w, y + dy * s, w * 0.14, lw=0.5, fill=PAL.lemon)
        k.circle(x + dx * w, y + dy * s, w * 0.09, lw=0.3, fill=PAL.cream)
    k.c.setStrokeColor(K); k.c.setLineWidth(1.2); k.c.arc(x + w * 0.3, y + s * 0.3, x + w * 0.85, y + s * 0.85, -80, 80)
    k.shape(body, lw=0.9, fill=None, amp=0)

def ledger(k, x, y, s):
    with k.tint(LEDGER):
        k.rect(x - s * 0.07, y - s * 0.02, s * 0.14, s * 0.1, lw=0.7)
    k.line([(x - s * 0.07, y + s * 0.005), (x + s * 0.07, y + s * 0.005)], lw=0.4, amp=0, color=PAL.brass)

def book(k, x, y, s):
    with k.tint(BOOK): k.rect(x - s * 0.05, y - s * 0.03, s * 0.1, s * 0.12, lw=0.7)
    k.line([(x - s * 0.03, y + s * 0.06), (x + s * 0.03, y + s * 0.06)], lw=0.4, amp=0, color=PAL.cloud)

def loveday(k, x, y, h, expr="smile", flip=False, jug_=True):
    f = _flip(k, x, flip); g = _geom(x, y, h); r, hy, sh, hem = g["r"], g["hy"], g["sh"], g["hem"]
    _legs(k, x, y, h, shoe=PAL.bag)
    _body(k, x, y, h, LOVEDAY_DRESS, hatch_kw=dict(angle=-40, gap=3.4, lw=0.3))
    with k.tint(PAL.apron):
        k.shape([(x - h * 0.09, sh - h * 0.14), (x + h * 0.09, sh - h * 0.14), (x + h * 0.14, hem + h * 0.04), (x - h * 0.14, hem + h * 0.04)], lw=0.7, fill=Wt, amp=0.1)
    k.c.setFillColor(PAL.lemon)
    for j in range(3): k.c.circle(x + (j - 1) * h * 0.06, hem + h * 0.12, h * 0.018, stroke=0, fill=1)
    hx, hyy = _arms(k, x, y, h, hold=jug_)
    if jug_: jug(k, hx + h * 0.06, hyy - h * 0.1, h * 0.2)
    _face(k, x, y, h, expr)
    with k.tint(PAL.hair_ginger):
        k.shape(k.arcpts(x, hy + r * 0.05, r * 1.08, r * 1.06, 0, 180, 20) + [(x - r * 1.08, hy - r * 0.5), (x - r * 0.8, hy - r * 0.5), (x - r * 0.75, hy + r * 0.5), (x + r * 0.75, hy + r * 0.5), (x + r * 0.8, hy - r * 0.5), (x + r * 1.08, hy - r * 0.5)], lw=0.7, fill=Wt, amp=0)
    _unflip(k, f)

def quill(k, x, y, h, expr="neutral", flip=False, prop=True):
    f = _flip(k, x, flip); g = _geom(x, y, h); r, hy, sh, hem = g["r"], g["hy"], g["sh"], g["hem"]
    _legs(k, x, y, h)
    _body(k, x, y, h, QUILL_JUMPER, hatch_kw=dict(angle=90, gap=2.6, lw=0.35))
    hx, hyy = _arms(k, x, y, h, hold=prop)
    if prop: ledger(k, hx + h * 0.04, hyy - h * 0.02, h)
    with k.tint(BEARD):   # short white beard
        k.shape(k.arcpts(x, hy - r * 0.15, r * 0.95, r * 1.0, 190, 350, 16) + [(x + r * 0.5, hy - r * 0.35), (x - r * 0.5, hy - r * 0.35)], lw=0.6, fill=Wt, amp=0)
    _face(k, x, y, h, expr)
    with k.tint(BEARD):
        k.shape(k.arcpts(x, hy - r * 0.15, r * 0.95, r * 1.0, 190, 350, 16) + [(x + r * 0.5, hy - r * 0.38), (x - r * 0.5, hy - r * 0.38)], lw=0.6, fill=Wt, amp=0)
    k.c.setStrokeColor(K); k.c.setLineWidth(0.6); k.c.arc(x - r * 0.3, hy - r * 0.55, x + r * 0.3, hy - r * 0.1, 200, 140)
    with k.tint(Wt, dark=QUILL_CAP):   # peaked harbourmaster's cap with a brass badge
        k.shape([(x - r * 1.05, hy + r * 0.6), (x + r * 1.05, hy + r * 0.6), (x + r * 1.15, hy + r * 1.15), (x - r * 1.15, hy + r * 1.15)], lw=0.8, fill=PAL.cloud, amp=0)
        k.rect(x - r * 1.05, hy + r * 0.45, r * 2.1, r * 0.25, lw=0.6, fill=K)
        k.shape([(x - r * 1.0, hy + r * 0.47), (x + r * 1.0, hy + r * 0.47), (x + r * 0.7, hy + r * 0.25), (x - r * 0.7, hy + r * 0.25)], lw=0.6, fill=K, amp=0)
    k.circle(x, hy + r * 0.82, r * 0.16, lw=0.4, fill=PAL.brass)
    _unflip(k, f)

def demelza(k, x, y, h, expr="neutral", flip=False, asleep=False, prop=True):
    f = _flip(k, x, flip); g = _geom(x, y, h); r, hy, sh, hem = g["r"], g["hy"], g["sh"], g["hem"]
    _legs(k, x, y, h, shoe=PAL.stripe)
    _body(k, x, y, h, DEMELZA_DRESS)
    k.c.setFillColor(PAL.cloud)
    for i in range(5):
        for j in range(4):
            k.c.circle(x + (i - 2) * h * 0.06 + (j % 2) * h * 0.03, hem + h * (0.06 + 0.1 * j), h * 0.01, stroke=0, fill=1)
    hx, hyy = _arms(k, x, y, h, hold=prop and not asleep)
    if prop and not asleep: book(k, hx + h * 0.03, hyy - h * 0.03, h)
    with k.tint(PAL.hair_dark):
        k.shape([(x - r * 1.0, hy + r * 0.3), (x - r * 1.1, hy - r * 0.9), (x + r * 1.1, hy - r * 0.9), (x + r * 1.0, hy + r * 0.3)], lw=0.7, fill=Wt, amp=0.2)
    _face(k, x, y, h, expr)
    if asleep:   # sunhat tipped over the face
        with k.tint(SUNHAT):
            k.shape(k.arcpts(x, hy - r * 0.05, r * 1.55, r * 1.25, 0, 360, 30), lw=0.8, fill=Wt, amp=0)
            k.shape(k.arcpts(x, hy - r * 0.05, r * 0.85, r * 0.7, 0, 360, 24), lw=0.6, fill=Wt, amp=0)
        k.c.setStrokeColor(SUNHAT_BAND); k.c.setLineWidth(r * 0.18); k.c.ellipse(x - r * 0.85, hy - r * 0.75, x + r * 0.85, hy + r * 0.65)
        for j, (dx, dy, sz) in enumerate(((1.6, 1.0, 0.5), (2.1, 1.6, 0.65), (2.7, 2.3, 0.8))):
            k.text(x + r * dx, hy + r * dy, "z", size=r * sz * 1.4, font="Ink-Playfair", color=PAL.sea2)
    else:
        with k.tint(SUNHAT):
            k.shape(k.arcpts(x, hy + r * 0.6, r * 2.1, r * 0.42, 0, 360, 30), lw=0.8, fill=Wt, amp=0)
            k.shape(k.arcpts(x, hy + r * 0.7, r * 0.92, r * 0.85, 0, 180, 20), lw=0.8, fill=Wt, amp=0)
        with k.tint(SUNHAT_BAND):
            k.shape([(x - r * 0.92, hy + r * 0.7), (x + r * 0.92, hy + r * 0.7), (x + r * 0.9, hy + r * 0.95), (x - r * 0.9, hy + r * 0.95)], lw=0.5, fill=Wt, amp=0)
    _unflip(k, f)

def bramble(k, x, y, h, expr="neutral", flip=False, ice="none", frost=False, prop=True, locket=False):
    f = _flip(k, x, flip); g = _geom(x, y, h); r, hy, sh, hem = g["r"], g["hy"], g["sh"], g["hem"]
    _legs(k, x, y, h, shoe=PAL.crust)
    _body(k, x, y, h, LINEN)
    with k.tint(PAL.glass):   # open-necked shirt between the lapels
        k.shape([(x - h * 0.05, sh), (x + h * 0.05, sh), (x + h * 0.02, sh - h * 0.2), (x - h * 0.02, sh - h * 0.2)], lw=0.6, fill=Wt, amp=0)
    k.line([(x - h * 0.05, sh), (x - h * 0.02, sh - h * 0.2), (x - h * 0.03, hem + h * 0.02)], lw=0.5, amp=0)
    k.line([(x + h * 0.05, sh), (x + h * 0.02, sh - h * 0.2), (x + h * 0.03, hem + h * 0.02)], lw=0.5, amp=0)
    k.rect(x + h * 0.07, sh - h * 0.3, h * 0.07, h * 0.012, lw=0.5, fill=shade(LINEN, 0.85))   # jacket pocket
    hx, hyy = _arms(k, x, y, h, hold=prop or locket)
    if prop: lemonade_glass(k, hx + h * 0.035, hyy - h * 0.04, h * 0.12, ice=ice, frost=frost)
    if locket:
        k.c.setStrokeColor(PAL.silver); k.c.setLineWidth(0.7); k.c.arc(hx - h * 0.01, hyy - h * 0.06, hx + h * 0.05, hyy + h * 0.01, 180, 360)
        k.circle(hx + h * 0.02, hyy - h * 0.06, h * 0.022, lw=0.6, fill=PAL.silver)
    _face(k, x, y, h, expr)
    with k.tint(PANAMA):
        k.shape(k.arcpts(x, hy + r * 0.6, r * 1.6, r * 0.32, 0, 360, 30), lw=0.8, fill=Wt, amp=0)
        k.shape([(x - r * 0.85, hy + r * 0.62), (x + r * 0.85, hy + r * 0.62), (x + r * 0.75, hy + r * 1.35), (x, hy + r * 1.2), (x - r * 0.75, hy + r * 1.35)], lw=0.8, fill=Wt, amp=0)
    with k.tint(PAL.slateboard):
        k.shape([(x - r * 0.85, hy + r * 0.62), (x + r * 0.85, hy + r * 0.62), (x + r * 0.83, hy + r * 0.82), (x - r * 0.83, hy + r * 0.82)], lw=0.5, fill=Wt, amp=0)
    _unflip(k, f)

def guest(k, x, y, h, dress, hat=None, hair=None):
    """Background party guest (small, generic, never one of the suspects)."""
    _legs(k, x, y, h); _body(k, x, y, h, dress); _arms(k, x, y, h, hold=False); _face(k, x, y, h)
    g = _geom(x, y, h); r, hy = g["r"], g["hy"]
    if hair: 
        with k.tint(hair): k.shape(k.arcpts(x, hy + r * 0.05, r * 1.04, r * 1.02, 10, 170, 16), lw=0.6, fill=Wt, amp=0)
    if hat:
        with k.tint(hat):
            k.shape(k.arcpts(x, hy + r * 0.6, r * 1.6, r * 0.3, 0, 360, 24), lw=0.6, fill=Wt, amp=0)
            k.shape(k.arcpts(x, hy + r * 0.65, r * 0.85, r * 0.7, 0, 180, 16), lw=0.6, fill=Wt, amp=0)

CHARACTERS = dict(agnes=agnes, ollie=ollie, morwenna=morwenna, hedley=hedley, jago=jago,
                  loveday=loveday, quill=quill, demelza=demelza, bramble=bramble)

# ----------------------------------------------------------------------------- Case 3 cast (drawn for the black-and-white ink style;
# the colours below only matter if a scene is rendered in colour)
CARDIGAN = _C(150, 120, 170); TROUSERS = _C(90, 96, 120); JUMPER = _C(214, 120, 96); TRENCH = _C(206, 180, 132); SCARF = _C(200, 90, 110)
TOTE = _C(226, 214, 186)

def fishing_book(k, x, y, s):
    """Small book with a fish on the cover, held at (x, y); s = figure height."""
    k.rect(x - s * 0.05, y - s * 0.035, s * 0.1, s * 0.12, lw=0.7)
    fx, fy, fw = x, y + s * 0.03, s * 0.035
    k.shape(k.arcpts(fx, fy, fw, fw * 0.45, 0, 360, 14), lw=0.4, fill=Wt, amp=0)
    k.shape([(fx + fw * 0.9, fy), (fx + fw * 1.5, fy + fw * 0.45), (fx + fw * 1.5, fy - fw * 0.45)], lw=0.4, fill=Wt, amp=0)

def comic(k, x, y, s):
    """Rolled-up comic held at (x, y)."""
    k.rect(x - s * 0.02, y - s * 0.05, s * 0.04, s * 0.14, lw=0.7)
    for j in range(3): k.line([(x - s * 0.02, y - s * 0.02 + j * s * 0.04), (x + s * 0.02, y - s * 0.01 + j * s * 0.04)], lw=0.35, amp=0)

def tote_bag(k, x, y, s, scarf=False, book=False):
    """Canvas tote hanging from the hand at (x, y) (straps up to the hand); optional scarf / book peeping out."""
    w, hh = s * 0.15, s * 0.14
    top = y - s * 0.05
    k.c.setStrokeColor(K); k.c.setLineWidth(1.0)
    k.c.arc(x - w * 0.3, top - hh * 0.1, x + w * 0.3, y + s * 0.03, 20, 160)
    if book:
        k.rect(x - w * 0.3, top - s * 0.01, w * 0.4, s * 0.07, lw=0.7, fill=Wt)
        k.text(x - w * 0.1, top + s * 0.02, "\u2605", size=s * 0.03, font="Ink-Plex")
    if scarf:
        with k.tint(SCARF):
            k.shape([(x - w * 0.1, top - s * 0.005), (x + w * 0.42, top - s * 0.005), (x + w * 0.38, top + s * 0.04), (x + w * 0.05, top + s * 0.05)], lw=0.6, fill=Wt, amp=0.3)
            k.hatch([(x - w * 0.1, top - s * 0.005), (x + w * 0.42, top - s * 0.005), (x + w * 0.38, top + s * 0.04), (x + w * 0.05, top + s * 0.05)], angle=45, gap=2.0, lw=0.35)
    with k.tint(TOTE):
        bag = [(x - w / 2, top), (x + w / 2, top), (x + w * 0.46, top - hh), (x - w * 0.46, top - hh)]
        k.shape(bag, lw=0.9, fill=Wt, amp=0.1)
        k.line([(x - w * 0.3, top - hh * 0.35), (x + w * 0.3, top - hh * 0.35)], lw=0.4, amp=0.2)

def drips(k, x, y, h, n=9, seed=3):
    """Water dripping off a soaked figure standing at (x, y): drops beside the body and a puddle at the feet."""
    import random
    rr = random.Random(seed)
    for i in range(n):
        dx = rr.uniform(-0.26, 0.26) * h; dy = rr.uniform(0.05, 0.62) * h
        if abs(dx) < 0.17 * h and dy > 0.15 * h: dx = (0.2 + rr.uniform(0, 0.06)) * h * (1 if dx >= 0 else -1)
        px, py, r = x + dx, y + dy, h * 0.012
        k.shape([(px, py + r * 2.6)] + k.arcpts(px, py, r, r, 200, 340, 8)[::-1] + [(px, py + r * 2.6)], lw=0.5, fill=Wt, amp=0)
    k.shape(k.arcpts(x, y - 1, h * 0.3, h * 0.035, 0, 360, 30), lw=0.7, fill=Wt, amp=0.3)
    for j in range(3): k.line(k.arcpts(x + (j - 1) * h * 0.09, y - 1, h * 0.04, h * 0.01, 200, 340, 6), lw=0.35, amp=0)

def tamsin(k, x, y, h, expr="smile", flip=False, prop="duster"):
    """Tamsin Trevelyan, bookseller: bob with a fringe, long cardigan over a plain dress, pencil behind the ear."""
    f = _flip(k, x, flip); g = _geom(x, y, h); r, hy, sh, hem = g["r"], g["hy"], g["sh"], g["hem"]
    _legs(k, x, y, h)
    body = _body(k, x, y, h, PAL.cloud)
    with k.tint(CARDIGAN):   # open cardigan: two front panels, ribbed
        for sg in (-1, 1):
            pnl = [(x + sg * h * 0.04, sh), (x + sg * h * 0.13, sh), (x + sg * h * 0.2, hem + h * 0.04), (x + sg * h * 0.07, hem + h * 0.04)]
            k.shape(pnl, lw=0.8, fill=Wt, amp=0.1); k.hatch(pnl, angle=90, gap=2.2, lw=0.35)
    hx, hyy = _arms(k, x, y, h, hold=prop is not None)
    if prop == "duster":
        k.line([(hx, hyy), (hx + h * 0.03, hyy + h * 0.14)], lw=1.0, amp=0)
        for j in range(7): k.line([(hx + h * 0.03, hyy + h * 0.14), (hx + h * (0.03 + 0.012 * (j - 3)), hyy + h * 0.22)], lw=0.7, amp=0.2)
    elif prop == "book":
        k.rect(hx - h * 0.01, hyy - h * 0.04, h * 0.09, h * 0.11, lw=0.7, fill=Wt)
    _face(k, x, y, h, expr)
    with k.tint(PAL.hair_dark, dark=PAL.hair_dark):   # dark bob with a straight fringe
        k.shape(k.arcpts(x, hy + r * 0.1, r * 1.12, r * 1.05, 0, 180, 20) + [(x - r * 1.12, hy - r * 0.55), (x - r * 0.82, hy - r * 0.55), (x - r * 0.82, hy + r * 0.55), (x + r * 0.82, hy + r * 0.55), (x + r * 0.82, hy - r * 0.55), (x + r * 1.12, hy - r * 0.55)], lw=0.7, fill=K, amp=0)
    k.line([(x + r * 0.8, hy + r * 0.9), (x + r * 1.5, hy + r * 0.4)], lw=1.4, amp=0)   # pencil behind the ear
    _unflip(k, f)

def pip(k, x, y, h, expr="neutral", flip=False, prop=True):
    """Pip Carew, cheerful teenager: tousled hair, striped jumper, trousers, holding a rolled-up comic."""
    f = _flip(k, x, flip); g = _geom(x, y, h); r, hy, sh, hem = g["r"], g["hy"], g["sh"], g["hem"]
    _legs(k, x, y, h)
    with k.tint(TROUSERS):   # trousers: two short legs below the jumper
        for sg in (-1, 1): k.shape([(x + sg * h * 0.02, hem + h * 0.12), (x + sg * h * 0.12, hem + h * 0.12), (x + sg * h * 0.11, hem - h * 0.02), (x + sg * h * 0.03, hem - h * 0.02)], lw=0.8, fill=Wt, amp=0)
    body = [(x - h * 0.13, sh), (x + h * 0.13, sh), (x + h * 0.17, hem + h * 0.12), (x - h * 0.17, hem + h * 0.12)]
    with k.tint(JUMPER):
        k.shape(body, lw=1.0, fill=Wt, amp=0.15)
        k.hatch(body, angle=0, gap=h * 0.04, lw=1.1, jitter=0)
        k.shape(body, lw=1.0, fill=None, amp=0)
    hx, hyy = _arms(k, x, y, h, hold=prop)
    if prop: comic(k, hx + h * 0.01, hyy, h)
    _face(k, x, y, h, expr)
    with k.tint(PAL.hair_ginger):   # tousled tufts
        pts = k.arcpts(x, hy + r * 0.15, r * 1.06, r * 1.0, 10, 170, 20)
        tuft = []
        for i, (px, py) in enumerate(pts): tuft.append((px, py + (r * 0.22 if i % 3 == 1 else 0)))
        k.shape(tuft + [(x - r * 0.8, hy + r * 0.45), (x + r * 0.8, hy + r * 0.45)], lw=0.7, fill=Wt, amp=0)
        k.hatch(tuft + [(x - r * 0.8, hy + r * 0.45), (x + r * 0.8, hy + r * 0.45)], angle=70, gap=2.0, lw=0.35)
    _unflip(k, f)

def wenna(k, x, y, h, expr="neutral", flip=False, prop=True, scarf=False, book=False):
    """Wenna Polglaze, antique dealer: belted knee-length coat with a wide collar, curly hair in a bun, tote bag."""
    f = _flip(k, x, flip); g = _geom(x, y, h); r, hy, sh, hem = g["r"], g["hy"], g["sh"], g["hem"]
    _legs(k, x, y, h)
    body = _body(k, x, y, h, TRENCH, hatch_kw=dict(angle=-35, gap=3.4, lw=0.3))
    with k.tint(TRENCH):
        for sg in (-1, 1): k.shape([(x, sh - h * 0.02), (x + sg * h * 0.13, sh), (x + sg * h * 0.1, sh - h * 0.12)], lw=0.7, fill=Wt, amp=0)   # collar
        k.rect(x - h * 0.175, hem + h * 0.2, h * 0.35, h * 0.035, lw=0.7)   # belt
        k.rect(x - h * 0.02, hem + h * 0.195, h * 0.04, h * 0.045, lw=0.6, fill=None)
    for j in range(3):
        for sg in (-1, 1): k.circle(x + sg * h * 0.04, sh - h * 0.17 - j * h * 0.11, h * 0.009 + 0.3, lw=0.4, fill=K)
    hx, hyy = _arms(k, x, y, h, hold=prop)
    if prop: tote_bag(k, hx + h * 0.01, hyy, h, scarf=scarf, book=book)
    _face(k, x, y, h, expr)
    with k.tint(PAL.hair_grey):   # curly hair and a bun
        for i in range(9):
            a = 15 + i * 18.75; import math as _m
            k.circle(x + r * 0.92 * _m.cos(_m.radians(a)), hy + r * 0.25 + r * 0.82 * _m.sin(_m.radians(a)), r * 0.3, lw=0.55, fill=Wt)
        k.circle(x, hy + r * 1.35, r * 0.42, lw=0.6, fill=Wt)
        k.c.setStrokeColor(K); k.c.setLineWidth(0.4); k.c.arc(x - r * 0.22, hy + r * 1.15, x + r * 0.22, hy + r * 1.55, 200, 220)
    _unflip(k, f)

CHARACTERS.update(tamsin=tamsin, pip=pip, wenna=wenna)
