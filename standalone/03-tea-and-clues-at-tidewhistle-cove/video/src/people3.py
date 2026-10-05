"""people3: DETAILED ink characters for Case 3 (The Dry Raincoat) in the v2 people.py line style, with soft colour
fills under the ink (colorink k.tint()). Same construction as people.py: a local 0..100 frame (feet at y=0, head
centre at CY), Catmull-Rom outlines, ink hatching, real faces (ears, eyes with glints, brows, nose, mouth), hair,
and clothing details (collars, cuffs, buttons, belts, pockets, ribbing, stripes).

  tamsin(k, x, y, h, prop="duster"|"book"|None)   Tamsin Trevelyan, bookseller: dark bob and fringe, plum cardigan,
                                                  sage dress, pencil behind the ear
  hedley(k, x, y, h, wet=False)                   Hedley Truscott: flat cap, moustache, tweed waistcoat, rolled sleeves,
                                                  fishing book
  pip(k, x, y, h)                                 Pip Carew: tousled ginger hair, freckles, striped jumper, rolled comic
  wenna(k, x, y, h, prop=True, scarf=False)       Wenna Polglaze: curly hair in a bun, belted camel raincoat, tote bag
  agnes(k, x, y, h)                               Agnes Bell: grey bun, round glasses, lavender sprig dress, apron

The three suspects (hedley, pip, wenna) share ONE stance, ONE arm pose (left arm down, right forearm across the
chest holding a small prop), the same head size, the same neutral face and the same level of detail and colour
weight. expr="sheepish" (eyes down, blush) is only used after the solution (Wenna in the returned scene).
Hedley's wet=True (darker, soaked cloth + drips at scene level) matches the narration ("dripping all over the floor")."""
import math
from colorink import PAL, C, shade, mix, K, Wt
from people import Fig, ell, tube, hand, shoe, neck, head, legs, CY

# ----------------------------------------------------------------------------- palette for the case 3 cast
SKIN = PAL.skin; SKIN2 = C(236, 198, 170)
CARDIGAN = C(156, 112, 150); DRESS_T = C(196, 214, 182); TIGHTS = C(96, 84, 92)
TWEED = PAL.tweed; SHIRT = C(226, 232, 238); CAP = PAL.cap; TROUS_H = C(120, 112, 100); BOOT = C(70, 60, 54)
JUMPER = C(212, 112, 92); JUMPER2 = C(246, 230, 200); TROUS_P = C(72, 88, 128); TRAINER = C(232, 236, 240)
COAT = C(214, 184, 132); COAT_DK = C(170, 136, 88); BLOUSE = C(240, 226, 230); HAIR_W = C(226, 196, 140)
TOTE = C(232, 220, 190); SCARF = C(196, 84, 104); STOCK = C(150, 120, 104)
HAIR_T = C(70, 50, 44); HAIR_P = PAL.hair_ginger; FRECKLE = C(196, 128, 96)
FISHBOOK = C(92, 140, 150); COMIC = C(244, 206, 96); PENCIL = C(244, 200, 80)

def _wet(c, wet): return shade(c, 0.8) if wet else c

def sleeve_arm(f, pts, sw, sleeve, skin_from=None, hatch=None, cuff=None, cuff_col=None):
    """people.arm, but the sleeve and the bare skin get their own colours (sleeve tint vs SKIN tint)."""
    k = f.k; n = len(pts); w = [sw * (1 - 0.28 * i / (n - 1)) for i in range(n)]; w[0] *= 0.72
    if skin_from is not None:
        with k.tint(SKIN): f.shape(tube(pts[skin_from - 1:], [x * 0.8 for x in w[skin_from - 1:]]), lw=0.9)
        sl, ws = pts[:skin_from], w[:skin_from]
    else: sl, ws = pts, w
    with k.tint(sleeve):
        o = tube(sl, ws, False); f.shape(o, lw=0.9)
        if hatch: f.hatch(o, **hatch)
        f.shape(o, lw=0.9, fill=None)
        if cuff:
            i = cuff; (x0, y0), (x1, y1) = sl[i - 1], sl[i]; dx, dy = x1 - x0, y1 - y0; d = math.hypot(dx, dy) or 1
            ux, uy = dx / d, dy / d; nx, ny = -uy, ux; ww = ws[i] * 1.12
            q = [(x1 - ux * 1.8 + nx * ww, y1 - uy * 1.8 + ny * ww, 0), (x1 + nx * ww, y1 + ny * ww, 0), (x1 - nx * ww, y1 - ny * ww, 0), (x1 - ux * 1.8 - nx * ww, y1 - uy * 1.8 - ny * ww, 0)]
            with k.tint(cuff_col or sleeve): f.shape(q, lw=0.7)
            f.curve([((q[0][0] + q[1][0]) / 2, (q[0][1] + q[1][1]) / 2), ((q[2][0] + q[3][0]) / 2, (q[2][1] + q[3][1]) / 2)], lw=0.35)

def skin_hand(f, x, y, ang, size=1.0):
    with f.k.tint(SKIN): hand(f, x, y, ang=ang, size=size)

def face(f, expr="neutral", **kw):
    """Head in skin colour; soft pink cheeks in colour (blush only for 'sheepish')."""
    k = f.k
    with k.tint(SKIN, hatch=shade(SKIN, 0.78)): head(f, 0, CY, expr=expr, **kw)
    cheek = PAL.blush if expr == "sheepish" else PAL.cheek
    rx = kw.get("rx", 6.0)
    for sg in (-1, 1):
        f.shape(ell(sg * rx * 0.55, CY - 1.7, 1.25 if expr != "sheepish" else 1.6, 0.75 if expr != "sheepish" else 0.95, n=14), lw=0, stroke=False, fill=mix(cheek, SKIN, 0.35 if expr != "sheepish" else 0.0))

# the shared suspect pose (identical for Hedley, Pip and Wenna)
L_ARM = [(-10.6, 77.6), (-13.4, 70), (-14.2, 62), (-14.0, 55), (-13.7, 50.8)]; L_HAND = (-13.7, 49.6, -92)
R_ARM = [(10.6, 77.6), (13.6, 70), (14.2, 62.5), (11.0, 63.2), (7.8, 64.6)]; R_HAND = (8.3, 65.0, 165)

# ----------------------------------------------------------------------------- props (figure frame)
def fishing_book(f):
    k = f.k; nb = [(2.0, 61.8, 0), (9.0, 62.6, 0), (8.4, 72.6, 0), (1.4, 71.8, 0)]
    with k.tint(FISHBOOK): f.shape(nb, lw=0.8)
    f.shape([(1.4, 71.8, 0), (2.0, 61.8, 0), (2.9, 61.9, 0), (2.3, 71.9, 0)], lw=0.4, fill=shade(FISHBOOK, 0.7))   # spine
    with k.tint(PAL.cloud): f.shape([(3.4, 70.2, 0), (7.8, 70.7, 0), (7.7, 69.6, 0), (3.5, 69.1, 0)], lw=0.3)       # title label
    fx, fy = 5.4, 66.0
    with k.tint(C(236, 196, 120)):
        f.shape(ell(fx, fy, 1.9, 0.95, n=16), lw=0.45)
        f.shape([(fx + 1.6, fy, 0), (fx + 2.9, fy + 0.9, 0), (fx + 2.9, fy - 0.9, 0)], lw=0.45)
    f.dot(fx - 1.0, fy + 0.2, 0.22)

def comic(f):
    k = f.k; tub = [(3.4, 59.6, 0), (7.6, 59.9, 0), (7.4, 74.2, 0), (3.2, 73.9, 0)]
    with k.tint(COMIC): f.shape(tub, lw=0.8)
    for j in range(4): f.curve([(3.4, 61.6 + j * 3.4), (5.6, 62.6 + j * 3.4), (7.6, 61.9 + j * 3.4)], lw=0.32)
    f.shape(ell(5.4, 74.05, 2.1, 0.7, n=14), lw=0.6, fill=shade(COMIC, 0.82))
    f.curve(ell(5.4, 74.05, 1.1, 0.35, 0, 300, 10), lw=0.3)
    with k.tint(C(214, 92, 84)): f.shape([(4.0, 70.4, 0), (7.0, 70.6, 0), (7.0, 72.0, 0), (4.0, 71.8, 0)], lw=0.3)   # red title band

def tote(f, scarf=False, book=False):
    """Canvas tote whose straps hang over the right hand; bag below the forearm."""
    k = f.k
    for x0, x1 in ((5.6, 10.4), (6.6, 11.6)):
        f.curve([(x0, 50.2), (x0 + 0.6, 60.0), (8.4, 66.2), (x1 - 0.4, 60.0), (x1, 50.2)], lw=0.9, color=shade(TOTE, 0.6))
    if book:
        with k.tint(C(214, 92, 84)): f.shape([(4.4, 49.0, 0), (8.6, 49.0, 0), (8.6, 56.0, 0), (4.4, 56.0, 0)], lw=0.6)
    if scarf:
        with k.tint(SCARF):
            sc = [(5.0, 49.6), (9.8, 51.6), (13.6, 50.4), (12.6, 48.0), (8.0, 47.6)]
            f.shape(sc, lw=0.6); f.hatch(sc, angle=45, gap=1.0, lw=0.3)
    bag = [(2.2, 50.4, 0), (14.8, 50.4, 0), (14.2, 34.6, 0.6), (2.8, 34.6, 0.6)]
    with k.tint(TOTE):
        f.shape(bag, lw=0.9); f.hatch(bag, angle=-50, gap=1.4, lw=0.25, box=(10.5, 34, 15, 51))
    f.curve([(2.5, 48.6), (14.6, 48.6)], lw=0.35, color=shade(TOTE, 0.6))
    with k.tint(C(150, 176, 196)):   # printed anchor badge on the canvas
        f.shape(ell(8.5, 41.6, 2.6, 2.6, n=18), lw=0.4)
    f.curve([(8.5, 43.4), (8.5, 39.6)], lw=0.4); f.curve([(7.2, 40.6), (8.5, 39.5), (9.8, 40.6)], lw=0.4); f.curve([(7.6, 42.6), (9.4, 42.6)], lw=0.35)

def duster(f):
    k = f.k
    f.shape([(7.0, 60.0, 0), (8.0, 60.0, 0), (10.4, 76.0, 0), (9.4, 76.2, 0)], lw=0.6, fill=PAL.wood_dk)
    for j in range(9):
        a = math.radians(55 + j * 9); L = 7.4 + (j % 3) * 0.9; ox, oy = 10.0, 76.2
        fe = [(ox, oy, 0), (ox + L * 0.55 * math.cos(a) - 1.2, oy + L * 0.55 * math.sin(a)), (ox + L * math.cos(a), oy + L * math.sin(a), 0),
              (ox + L * 0.55 * math.cos(a) + 1.2, oy + L * 0.55 * math.sin(a))]
        with k.tint([C(244, 176, 186), C(250, 226, 160), C(200, 220, 236)][j % 3]): f.shape(fe, lw=0.4)

def held_book(f):
    k = f.k; bk = [(1.6, 61.4, 0), (10.2, 62.2, 0), (9.6, 73.6, 0), (1.0, 72.8, 0)]
    with k.tint(C(98, 146, 170)): f.shape(bk, lw=0.8)
    with k.tint(PAL.cloud): f.shape([(3.0, 69.0, 0), (8.6, 69.5, 0), (8.5, 71.4, 0), (2.9, 70.9, 0)], lw=0.3)
    f.shape(ell(5.6, 66.0, 1.4, 1.8, n=14), lw=0.4, fill=K); f.shape([(6.9, 66.6, 0), (8.2, 66.2, 0), (6.9, 65.6, 0)], lw=0.3, fill=PAL.copper)

# ----------------------------------------------------------------------------- characters
def hedley(k, x, y, h, expr="neutral", flip=False, wet=False, prop=True):
    with Fig(k, x, y, h, flip) as f:
        tr = _wet(TROUS_H, wet); tw = _wet(TWEED, wet); sh_ = _wet(SHIRT, wet); cp = _wet(CAP, wet)
        trou = [(-8.2, 52, 0), (-7.9, 26), (-7.3, 3.6, 0), (-1.2, 3.6, 0), (-0.8, 40), (0.8, 40), (1.2, 3.6, 0), (7.3, 3.6, 0), (7.9, 26), (8.2, 52, 0)]
        with k.tint(tr):
            f.shape(trou, lw=1.0); f.hatch(trou, angle=88, gap=1.6, lw=0.28); f.shape(trou, lw=1.0, fill=None)
        with k.tint(None, dark=BOOT):
            for sg in (-1, 1): shoe(f, sg * 4.2, sg, "boot", top=4.6)
        shirt = [(-2.8, 82.4), (-11.6, 80.0), (-12.2, 72), (-10.4, 60), (-9.2, 50.5, 0), (9.2, 50.5, 0), (10.4, 60), (12.2, 72), (11.6, 80.0), (2.8, 82.4)]
        with k.tint(sh_):
            f.shape(shirt, lw=1.1)
            for sg in (-1, 1): f.shape([(0, 79.0, 0), (sg * 0.8, 83.4, 0), (sg * 3.6, 82.2, 0), (sg * 2.6, 78.4, 0)], lw=0.6)
        vest = [(-4.0, 79.2, 0), (-9.8, 77.6), (-10.4, 66), (-9.4, 51.0), (-8.6, 48.4, 0), (-0.5, 46.4, 0), (0.5, 46.4, 0), (8.6, 48.4, 0), (9.4, 51.0), (10.4, 66), (9.8, 77.6), (4.0, 79.2, 0), (0, 63.0, 0)]
        with k.tint(tw, hatch=shade(tw, 0.7)):
            f.shape(vest, lw=1.0); f.hatch(vest, angle=45, gap=1.3, lw=0.3, cross=True); f.shape(vest, lw=1.0, fill=None)
        f.curve([(0, 63), (0, 46.4)], lw=0.5)
        for by in (61, 57, 53, 49.2): f.dot(0.9, by, 0.62, fill=PAL.brass, lw=0.4)
        for sg in (-1, 1): f.shape([(sg * 3.4, 56.2, 0), (sg * 7.8, 56.6, 0), (sg * 7.8, 55.2, 0), (sg * 3.4, 54.8, 0)], lw=0.4, fill=shade(tw, 0.85))
        f.curve([(-3.6, 55.2), (-5.4, 53.6), (-7.0, 54.0)], lw=0.5, color=shade(PAL.brass, 0.7))   # watch chain
        sleeve_arm(f, L_ARM, 2.6, sh_, skin_from=3, cuff=2)
        for j in range(3): f.curve([(-13.2 + j * 0.9, 67 - j * 1.4), (-11.8 + j * 0.9, 69 - j * 1.4)], lw=0.3)
        skin_hand(f, *L_HAND[:2], L_HAND[2], 1.05)
        sleeve_arm(f, R_ARM, 2.6, sh_, skin_from=3, cuff=2)
        if prop: fishing_book(f)
        skin_hand(f, *R_HAND[:2], R_HAND[2], 1.0)
        with k.tint(SKIN): neck(f, CY, w=2.3, base=80.5)
        face(f, expr, rx=5.9, ry=7.8, jaw=0.72, nose="long", brows="thick", lines=2, moustache=False)
        mo = [(-3.2, CY - 3.2), (-1.7, CY - 2.4), (0, CY - 2.35), (1.7, CY - 2.4), (3.2, CY - 3.2), (1.8, CY - 3.35), (0, CY - 3.15), (-1.8, CY - 3.35)]
        f.shape(mo, lw=0.4, fill=PAL.hair_grey)   # grey moustache
        f.curve([(-1.2, CY - 4.4), (0, CY - 4.55), (1.2, CY - 4.4)], lw=0.5)
        with k.tint(PAL.hair_grey):
            for sg in (-1, 1):   # grey hair over the ears
                f.shape([(sg * 5.4, CY + 3.8), (sg * 6.6, CY + 3.0), (sg * 6.8, CY - 0.6), (sg * 6.0, CY - 1.2), (sg * 5.6, CY + 1.2)], lw=0.6)
                for j in range(3): f.curve([(sg * (5.7 + j * 0.3), CY + 3.2 - j * 0.3), (sg * (6.3 + j * 0.15), CY - 0.4)], lw=0.3)
        cap = [(-6.8, CY + 3.6, 0), (-7.6, CY + 6.6), (-5.4, CY + 9.4), (0, CY + 10.0), (5.6, CY + 9.2), (8.4, CY + 6.6), (7.0, CY + 4.2, 0)]
        with k.tint(cp, dark=shade(cp, 0.6)):
            f.shape(cap, lw=1.0); f.hatch(cap, angle=55, gap=1.3, lw=0.3); f.hatch(cap, angle=-55, gap=1.3, lw=0.3, box=(-8, CY + 3, 0, CY + 11))
            f.shape(cap, lw=1.0, fill=None)
            f.curve([(-5.0, CY + 7.6), (0.4, CY + 8.0), (6.4, CY + 6.2)], lw=0.4)
            f.dot(0.6, CY + 9.8, 0.55, fill=K)
            f.shape([(-6.9, CY + 3.8), (0, CY + 4.6), (7.2, CY + 4.0), (7.6, CY + 2.4), (0, CY + 2.5), (-6.6, CY + 2.6)], lw=0.8, fill=K)
        if wet:   # soaked: water streaks running down the cloth
            for (sx, sy, L) in ((-6, 74, 9), (5, 70, 8), (-3, 44, 10), (4, 36, 9), (-8.5, 60, 7), (8.2, 58, 6), (-4.5, 22, 9), (5, 18, 8)):
                f.curve([(sx, sy), (sx + 0.3, sy - L * 0.5), (sx - 0.1, sy - L)], lw=0.45, color=C(110, 150, 190))
            for (sx, sy) in ((-4, CY + 4.2), (3, CY + 4.4), (7.6, CY + 2.0)):
                f.shape([(sx, sy - 0.2), (sx - 0.5, sy - 1.3), (sx, sy - 1.8), (sx + 0.5, sy - 1.3)], lw=0.3, fill=C(190, 220, 240))

def pip(k, x, y, h, expr="neutral", flip=False, prop=True):
    with Fig(k, x, y, h, flip) as f:
        trou = [(-8.0, 50, 0), (-7.8, 26), (-7.0, 4.0, 0), (-1.2, 4.0, 0), (-0.8, 36), (0.8, 36), (1.2, 4.0, 0), (7.0, 4.0, 0), (7.8, 26), (8.0, 50, 0)]
        with k.tint(TROUS_P):
            f.shape(trou, lw=1.0); f.hatch(trou, angle=80, gap=1.7, lw=0.25, box=(3, 0, 9, 50)); f.shape(trou, lw=1.0, fill=None)
            for sg in (-1, 1): f.curve([(sg * 4.1, 34), (sg * 4.2, 6)], lw=0.3)
            for sg in (-1, 1): f.shape([(sg * 1.2, 7.4, 0), (sg * 7.1, 7.4, 0), (sg * 7.0, 4.0, 0), (sg * 1.2, 4.0, 0)], lw=0.5)   # turn-ups
        for sg in (-1, 1):   # trainers: white with a coloured flash and laces
            s = sg; xx = sg * 4.2
            tr = [(xx - 2.6 * s, 4.4), (xx + 1.8 * s, 4.6), (xx + 4.6 * s, 2.6), (xx + 4.9 * s, 0.3, 0), (xx - 2.9 * s, 0.3, 0), (xx - 3.0 * s, 2.2)]
            with k.tint(TRAINER): f.shape(tr, lw=0.9)
            f.curve([(xx - 2.8 * s, 1.1), (xx + 4.8 * s, 1.1)], lw=0.4)
            f.curve([(xx - 1.4 * s, 2.0), (xx + 1.0 * s, 3.4), (xx + 3.0 * s, 2.2)], lw=0.7, color=shade(JUMPER, 0.9))
            for j in range(3): f.curve([(xx + (0.2 + j * 0.9) * s, 4.3 - j * 0.4), (xx + (0.9 + j * 0.9) * s, 3.7 - j * 0.4)], lw=0.3)
        jum = [(-2.8, 82.2), (-11.6, 79.6), (-12.6, 72), (-12.2, 60), (-12.4, 46.5, 0), (12.4, 46.5, 0), (12.2, 60), (12.6, 72), (11.6, 79.6), (2.8, 82.2)]
        with k.tint(JUMPER2): f.shape(jum, lw=1.1)
        f.clip(jum)   # bold horizontal stripes
        for j in range(8):
            yy = 50.0 + j * 4.2
            f.shape([(-14, yy, 0), (14, yy, 0), (14, yy + 2.1, 0), (-14, yy + 2.1, 0)], lw=0, stroke=False, fill=JUMPER)
        f.unclip()
        f.hatch(jum, angle=62, gap=1.5, lw=0.28, box=(7.5, 46, 14, 83), color=shade(JUMPER, 0.6))
        f.shape(jum, lw=1.1, fill=None)
        with k.tint(JUMPER):   # ribbed hem and crew neck
            hem = [(-12.4, 49.0, 0), (12.4, 49.0, 0), (12.4, 46.5, 0), (-12.4, 46.5, 0)]
            f.shape(hem, lw=0.7); f.hatch(hem, angle=90, gap=0.9, lw=0.3)
            nk = [(-3.6, 81.6), (-2.4, 79.4), (0, 78.8), (2.4, 79.4), (3.6, 81.6), (2.6, 82.6), (0, 81.4), (-2.6, 82.6)]
            f.shape(nk, lw=0.7); f.hatch(nk, angle=90, gap=0.8, lw=0.28)
        sleeve_arm(f, L_ARM, 2.8, JUMPER, cuff=4, hatch=dict(angle=0, gap=2.1, lw=0.7, color=JUMPER2))
        skin_hand(f, *L_HAND[:2], L_HAND[2], 1.0)
        sleeve_arm(f, R_ARM, 2.8, JUMPER, cuff=4, hatch=dict(angle=0, gap=2.1, lw=0.7, color=JUMPER2))
        if prop: comic(f)
        skin_hand(f, *R_HAND[:2], R_HAND[2], 1.0)
        with k.tint(SKIN): neck(f, CY, w=2.1)
        face(f, expr, rx=5.9, ry=7.2, jaw=0.62, nose="button", brows="soft")
        for (fx, fy) in ((-3.6, CY - 0.9), (-2.8, CY - 1.6), (-4.2, CY - 1.9), (3.6, CY - 0.9), (2.8, CY - 1.6), (4.2, CY - 1.9), (-0.6, CY - 1.0), (0.7, CY - 1.1)):
            f.dot(fx, fy, 0.22, fill=FRECKLE)
        # tousled ginger hair: spiky outline over the crown, choppy fringe
        out = []
        for i in range(19):
            a = math.radians(178 - i * 9.8); rr = 1.0 if i % 2 == 0 else 1.13
            out.append((7.0 * rr * math.cos(a), CY + 0.8 + 8.4 * rr * math.sin(a), 0 if i % 2 else 1.0))
        fr = [(6.3, CY + 1.6, 0), (5.2, CY + 4.6, 0), (4.0, CY + 3.2, 0), (2.4, CY + 5.6, 0), (0.6, CY + 3.8, 0), (-1.4, CY + 5.8, 0), (-3.0, CY + 3.6, 0), (-4.6, CY + 5.4, 0), (-6.3, CY + 1.6, 0)]
        with k.tint(HAIR_P, hatch=shade(HAIR_P, 0.7)):
            f.shape(out + fr, lw=0.9)
            f.hatch(out + fr, angle=70, gap=1.3, lw=0.3, box=(2.5, CY, 9, CY + 11))
            f.shape(out + fr, lw=0.9, fill=None)
        for j in range(5):
            u = -4.4 + j * 2.2; f.curve([(u, CY + 5.8), (u * 1.1 + 0.4, CY + 7.6), (u * 0.8, CY + 9.0)], lw=0.32)

def wenna(k, x, y, h, expr="neutral", flip=False, prop=True, scarf=False, book=False):
    with Fig(k, x, y, h, flip) as f:
        with k.tint(STOCK): legs(f, x=3.3, top=31, w0=1.9, w1=1.5, ankle=6)
        for sg in (-1, 1):   # ankle boots with a low heel
            s = sg; xx = sg * 3.6
            bt = [(xx - 2.0 * s, 9.0, 0), (xx + 1.9 * s, 9.0, 0), (xx + 2.2 * s, 3.4), (xx + 4.6 * s, 1.8), (xx + 4.8 * s, 0.3, 0), (xx - 2.6 * s, 0.3, 0), (xx - 2.5 * s, 3.0)]
            with k.tint(None, dark=C(120, 72, 60)): f.shape(bt, lw=0.9, fill=K)
            f.curve([(xx - 2.3 * s, 1.2), (xx + 4.6 * s, 1.2)], lw=0.35, color=Wt)
        coat = [(-2.8, 81.6), (-11.4, 79.4), (-12.4, 72), (-11.6, 60), (-11.8, 50), (-14.2, 29.0, 0.6), (0, 28.2), (14.2, 29.0, 0.6), (11.8, 50), (11.6, 60), (12.4, 72), (11.4, 79.4), (2.8, 81.6)]
        with k.tint(COAT, hatch=shade(COAT, 0.72)):
            f.shape(coat, lw=1.1)
            f.hatch(coat, angle=-60, gap=1.6, lw=0.3, box=(8.0, 27, 15, 82))
            f.shape(coat, lw=1.1, fill=None)
            f.curve([(1.6, 54.0), (2.4, 40.0), (3.2, 28.6)], lw=0.6)   # overlap edge of the front
            for u in (-8, -4.5, 6.5, 10): f.curve([(u * 0.95, 50), (u * 1.08, 38), (u * 1.18, 30)], lw=0.3)   # skirt folds
        with k.tint(BLOUSE): f.shape([(-3.0, 81.2, 0), (3.0, 81.2, 0), (0, 72.0, 0)], lw=0.6)
        with k.tint(COAT):
            for sg in (-1, 1):   # wide collar and lapels
                f.shape([(sg * 2.6, 81.8, 0), (sg * 8.4, 80.2), (sg * 9.0, 74.6, 0), (sg * 4.4, 70.0, 0), (sg * 0.4, 66.0, 0), (sg * 1.0, 72.0)], lw=0.8)
                f.curve([(sg * 4.4, 70.0), (sg * 5.6, 75.8)], lw=0.35)
            for sg in (-1, 1):   # pocket flaps
                f.shape([(sg * 3.6, 44.0, 0), (sg * 9.6, 44.6, 0), (sg * 9.4, 42.0, 0), (sg * 3.8, 41.6, 0)], lw=0.6)
        with k.tint(COAT_DK):   # belt and buckle
            bl = [(-11.9, 55.6, 0), (11.9, 55.6, 0), (11.8, 52.4, 0), (-11.8, 52.4, 0)]
            f.shape(bl, lw=0.8)
        f.shape([(-2.0, 56.4, 0), (2.0, 56.4, 0), (2.0, 51.6, 0), (-2.0, 51.6, 0)], lw=0.6, fill=None)
        f.curve([(-0.2, 54.0), (2.6, 54.0)], lw=0.5)
        for j in range(3):   # double row of buttons
            for sg in (-1, 1): f.dot(sg * 4.2, 66.0 - j * 5.2 - (12 if j == 2 else 0), 0.7, fill=COAT_DK, lw=0.4)
        sleeve_arm(f, L_ARM, 2.9, COAT, cuff=4, cuff_col=COAT_DK, hatch=dict(angle=-60, gap=2.0, lw=0.25))
        skin_hand(f, *L_HAND[:2], L_HAND[2], 1.0)
        if prop: tote(f, scarf=scarf, book=book)
        sleeve_arm(f, R_ARM, 2.9, COAT, cuff=4, cuff_col=COAT_DK, hatch=dict(angle=-60, gap=2.0, lw=0.25))
        skin_hand(f, *R_HAND[:2], R_HAND[2], 1.0)
        with k.tint(SKIN): neck(f, CY, w=2.0)
        face(f, expr, rx=5.8, ry=7.3, jaw=0.6, nose="small", lines=1)
        for sg in (-1, 1): f.dot(sg * 5.75, CY - 2.7, 0.55, fill=PAL.rosette, lw=0.35)   # little blue earrings
        # curly hair (honey blonde) framing the face, and a bun
        with k.tint(HAIR_W, hatch=shade(HAIR_W, 0.72)):
            f.shape(ell(0, CY + 10.4, 3.4, 2.9, n=20), lw=0.9)
            for j in range(3): f.curve(ell(0, CY + 10.4, 2.6 - j * 0.75, 2.2 - j * 0.6, 30, 320, 12), lw=0.32)
            for i in range(11):
                a = math.radians(-12 + i * 20.4); cx_, cy_ = 6.4 * math.cos(a), CY + 1.4 + 7.2 * math.sin(a)
                cu = ell(cx_, cy_, 2.1, 2.0, n=16); f.shape(cu, lw=0.7)
                f.curve(ell(cx_ + 0.2, cy_ - 0.1, 1.0, 0.9, 40, 300, 8), lw=0.3)

def tamsin(k, x, y, h, expr="smile", flip=False, prop="duster"):
    with Fig(k, x, y, h, flip) as f:
        hb = [(-7.6, CY - 5.0, 0), (-8.0, CY + 1.0), (-7.2, CY + 6.6), (-4.2, CY + 9.6), (0, CY + 10.2), (4.2, CY + 9.6), (7.2, CY + 6.6), (8.0, CY + 1.0), (7.6, CY - 5.0, 0)]
        with k.tint(HAIR_T, dark=HAIR_T): f.shape(hb, lw=0.9)
        with k.tint(TIGHTS): legs(f, x=3.2, top=24, w0=1.9, w1=1.5, ankle=3.0)
        with k.tint(None, dark=C(150, 70, 70)):
            for sg in (-1, 1): shoe(f, sg * 3.2, sg)
        for sg in (-1, 1): f.curve([(sg * 2.2, 3.0), (sg * 3.1, 4.0), (sg * 4.3, 3.0)], lw=0.5)
        dress = [(-2.6, 81.0), (-8.8, 79.0), (-9.6, 72), (-8.4, 60), (-9.8, 44), (-12.4, 22.0, 0.6), (0, 21.2), (12.4, 22.0, 0.6), (9.8, 44), (8.4, 60), (9.6, 72), (8.8, 79.0), (2.6, 81.0)]
        with k.tint(DRESS_T): f.shape(dress, lw=1.1)
        f.clip(dress)   # small white polka dots
        for gy in range(23, 82, 4):
            for gx in range(-14, 15, 4):
                f.dot(gx + (2 if (gy // 4) % 2 else 0), gy, 0.42, fill=PAL.cloud)
        f.unclip()
        f.shape(dress, lw=1.1, fill=None)
        with k.tint(CARDIGAN, hatch=shade(CARDIGAN, 0.72)):
            for sg in (-1, 1):   # long open cardigan, ribbed, with patch pockets
                pan = [(sg * 2.4, 81.0, 0), (sg * 8.9, 79.2), (sg * 10.2, 72), (sg * 9.6, 60), (sg * 11.0, 34.0, 0), (sg * 4.6, 33.4, 0), (sg * 3.6, 56), (sg * 2.4, 72)]
                f.shape(pan, lw=1.0); f.hatch(pan, angle=90, gap=1.2, lw=0.26); f.shape(pan, lw=1.0, fill=None)
                pk = [(sg * 5.2, 47.0, 0), (sg * 9.8, 47.4, 0), (sg * 10.2, 40.6, 0), (sg * 5.4, 40.2, 0)]
                f.shape(pk, lw=0.6)
                f.shape([(sg * 4.6, 36.0, 0), (sg * 11.0, 36.4, 0), (sg * 11.0, 34.0, 0), (sg * 4.6, 33.4, 0)], lw=0.6)
        for by in (74, 67, 60, 53): f.dot(-3.4, by, 0.6, fill=PAL.cloud, lw=0.4)
        sleeve_arm(f, [(-8.9, 77.2), (-11.8, 70), (-12.6, 62), (-12.4, 55), (-12.0, 51.5)], 2.5, CARDIGAN, cuff=4, hatch=dict(angle=90, gap=1.2, lw=0.26))
        skin_hand(f, -12.0, 50.4, -92, 0.95)
        if prop is None:
            sleeve_arm(f, [(8.9, 77.2), (11.8, 70), (12.6, 62), (12.4, 55), (12.0, 51.5)], 2.5, CARDIGAN, cuff=4, hatch=dict(angle=90, gap=1.2, lw=0.26))
            skin_hand(f, 12.0, 50.4, -88, 0.95)
        else:
            sleeve_arm(f, [(8.9, 77.2), (12.2, 70), (12.8, 62.5), (9.6, 62.4), (7.0, 63.4)], 2.5, CARDIGAN, cuff=4, hatch=dict(angle=90, gap=1.2, lw=0.26))
            if prop == "duster": duster(f)
            elif prop == "book": held_book(f)
            skin_hand(f, 7.6, 63.8, 165, 0.95)
        with k.tint(SKIN): neck(f, CY, w=2.0)
        face(f, expr, rx=5.8, ry=7.2, jaw=0.6, nose="small", ears=False)
        with k.tint(HAIR_T, hatch=shade(HAIR_T, 0.6)):   # bob sides and a straight fringe
            for sg in (-1, 1):
                f.shape([(sg * 5.4, CY + 4.0), (sg * 7.0, CY + 4.6), (sg * 8.0, CY + 0.6), (sg * 7.8, CY - 5.0, 0), (sg * 5.6, CY - 5.2, 0), (sg * 5.9, CY - 1.0)], lw=0.7)
            fr = [(-6.8, CY + 1.6), (-7.0, CY + 5.6), (-5.0, CY + 8.6), (0, CY + 9.4), (5.0, CY + 8.6), (7.0, CY + 5.6), (6.8, CY + 1.6), (6.0, CY + 3.6, 0), (-6.0, CY + 3.6, 0)]
            f.shape(fr, lw=0.9)
        for j in range(7): f.curve([(-5.0 + j * 1.65, CY + 3.8), (-5.2 + j * 1.7, CY + 6.8)], lw=0.3, color=shade(HAIR_T, 1.9))
        f.curve([(-4.0, CY + 8.6), (0, CY + 9.0), (3.0, CY + 8.8)], lw=0.35, color=shade(HAIR_T, 2.2))
        # pencil behind the ear
        pc = [(4.6, CY + 3.0, 0), (10.2, CY - 1.4, 0), (9.6, CY - 2.2, 0), (4.0, CY + 2.2, 0)]
        with k.tint(PENCIL): f.shape(pc, lw=0.5)
        f.shape([(10.2, CY - 1.4, 0), (11.5, CY - 2.7, 0), (9.6, CY - 2.2, 0)], lw=0.4, fill=PAL.wood)
        f.dot(11.3, CY - 2.55, 0.25)

def agnes(k, x, y, h, expr="smile", flip=False, bag=False):
    """Agnes Bell (people.agnes, in colour): lavender sprig dress, white frilled apron, grey bun, glasses. bag=True:
    a little paper chemist's bag in her right hand."""
    with Fig(k, x, y, h, flip) as f:
        with k.tint(C(240, 236, 230)): legs(f, x=3.4, top=24, ankle=3.0)
        with k.tint(None, dark=C(110, 82, 120)):
            for sg in (-1, 1): shoe(f, sg * 3.3, sg)
        for sg in (-1, 1): f.curve([(sg * 2.3, 3.0), (sg * 3.2, 4.0), (sg * 4.4, 3.0)], lw=0.5)
        dress = [(-2.6, 81.5), (-9.4, 79.4), (-11.0, 73), (-11.2, 63), (-12.2, 50), (-14.6, 24, 0.6), (-7, 22.6), (0, 22.2), (7, 22.6), (14.6, 24, 0.6), (12.2, 50), (11.2, 63), (11.0, 73), (9.4, 79.4), (2.6, 81.5)]
        with k.tint(PAL.agnes_dress, hatch=shade(PAL.agnes_dress, 0.72)):
            f.shape(dress, lw=1.1)
            f.clip(dress)
            for gy in range(24, 82, 5):
                for gx in range(-16, 17, 5):
                    px = gx + (2.5 if (gy // 5) % 2 else 0) + f.r.uniform(-0.6, 0.6); py = gy + f.r.uniform(-0.6, 0.6)
                    for a in (90, 210, 330): f.dot(px + 0.55 * math.cos(math.radians(a)), py + 0.55 * math.sin(math.radians(a)), 0.32, fill=PAL.cloud)
            f.unclip()
            f.hatch(dress, angle=-60, gap=1.6, lw=0.3, box=(7, 20, 16, 82))
            f.shape(dress, lw=1.1, fill=None)
        with k.tint(PAL.apron, hatch=C(214, 206, 196)):
            f.curve([(-4.6, 74), (-3.0, 79.8)], lw=0.9); f.curve([(4.6, 74), (3.0, 79.8)], lw=0.9)
            f.shape([(-5.2, 74.5, 0), (5.2, 74.5, 0), (6.2, 62, 0), (-6.2, 62, 0)], lw=0.9)
            f.curve([(-4.2, 73.2), (4.2, 73.2)], lw=0.35)
            sk = [(-9.6, 61.5, 0), (9.6, 61.5, 0), (10.6, 45), (11.8, 28.5, 0), (-11.8, 28.5, 0), (-10.6, 45)]
            f.shape(sk, lw=0.9)
            for u in (-6, -2.5, 2.5, 6): f.curve([(u * 0.9, 60.5), (u * 1.05, 44), (u * 1.15, 31)], lw=0.3)
            fr = [(-12.2, 28.5, 0)]
            for j in range(12): fr += [(-12.2 + 24.4 * (j + 0.5) / 12, 26.1), (-12.2 + 24.4 * (j + 1) / 12, 28.0, 0)]
            f.shape(fr + [(12.2, 28.6, 0)], lw=0.8, t=0.9); f.hatch(fr + [(12.2, 28.6, 0)], angle=90, gap=1.1, lw=0.3)
            f.shape([(-11.2, 62.2, 0), (11.2, 62.2, 0), (11.2, 60.4, 0), (-11.2, 60.4, 0)], lw=0.8)
            f.shape([(-3.6, 50, 0), (3.6, 50, 0), (3.4, 43.5), (0, 42.8), (-3.4, 43.5)], lw=0.7)
            f.curve([(-3.4, 48.6), (3.4, 48.6)], lw=0.3)
            for sg in (-1, 1): f.shape([(0, 79.0), (sg * 1.2, 81.6), (sg * 4.6, 80.8), (sg * 4.6, 78.6), (sg * 2.0, 77.6)], lw=0.7)
        f.dot(0, 77.4, 0.55, fill=PAL.rosette, lw=0.4)   # brooch
        hs = dict(angle=-60, gap=1.7, lw=0.3)
        sleeve_arm(f, [(-9.4, 77.2), (-12.6, 70), (-13.4, 62.5), (-13.2, 55.5), (-12.9, 51.2)], 2.7, PAL.agnes_dress, skin_from=4, hatch=hs, cuff=3)
        skin_hand(f, -12.9, 50.2, -92, 1.0)
        sleeve_arm(f, [(9.4, 77.2), (12.6, 70), (13.4, 62.5), (13.2, 55.5), (12.9, 51.2)], 2.7, PAL.agnes_dress, skin_from=4, hatch=hs, cuff=3)
        if bag:
            pb = [(9.6, 49.0, 0), (16.6, 49.0, 0), (16.0, 37.0, 0), (10.2, 37.0, 0)]
            with k.tint(C(236, 222, 196)): f.shape(pb, lw=0.8)
            for j in range(3): f.curve([(9.8 + j * 0.2, 48.6 - j * 0.9), (16.4 - j * 0.2, 48.6 - j * 0.9)], lw=0.28)
            f.shape([(11.8, 44.6, 0), (14.6, 44.6, 0), (14.6, 41.4, 0), (11.8, 41.4, 0)], lw=0.4, fill=C(120, 180, 150))
            f.curve([(13.2, 44.0), (13.2, 42.0)], lw=0.5, color=Wt); f.curve([(12.2, 43.0), (14.2, 43.0)], lw=0.5, color=Wt)
        skin_hand(f, 12.9, 50.2, -88, 1.0)
        with k.tint(SKIN): neck(f, CY, w=2.2)
        with k.tint(PAL.hair_grey):
            f.shape(ell(0, CY + 9.2, 3.0, 2.6, n=18), lw=0.9)
            for j in range(3): f.curve(ell(0, CY + 9.2, 2.4 - j * 0.7, 2.0 - j * 0.55, 20, 300, 10), lw=0.35)
        face(f, expr, rx=6.0, ry=7.3, jaw=0.66, glasses=True, nose="button", lines=2)
        hair = [(-6.5, CY - 0.6), (-7.0, CY + 3.0), (-6.0, CY + 6.6), (-3.2, CY + 8.4), (0, CY + 8.8), (3.2, CY + 8.4), (6.0, CY + 6.6), (7.0, CY + 3.0), (6.5, CY - 0.6),
                (5.6, CY + 2.6), (3.6, CY + 4.6), (0.6, CY + 5.0), (-1.6, CY + 5.8), (-4.4, CY + 4.6), (-5.7, CY + 2.4)]
        with k.tint(PAL.hair_grey): f.shape(hair, lw=0.9)
        for j in range(6):
            u = -5 + j * 2; f.curve([(u * 0.9, CY + 5.0 + 0.4 * (j % 2)), (u * 1.05, CY + 7.0), (u * 0.6, CY + 8.3)], lw=0.35)
        f.curve([(-5.9, CY + 2.0), (-6.6, CY + 4.2), (-5.2, CY + 6.6)], lw=0.35); f.curve([(5.9, CY + 2.0), (6.6, CY + 4.2), (5.2, CY + 6.6)], lw=0.35)
        f.dot(-5.9, CY - 2.6, 0.45, fill=Wt, lw=0.4); f.dot(5.9, CY - 2.6, 0.45, fill=Wt, lw=0.4)

def drips(k, x, y, h, n=10, seed=3):
    """Water drops beside a soaked figure standing at (x, y) and a puddle at its feet (k frame, blue water)."""
    import random
    rr = random.Random(seed); water = C(170, 206, 232)
    with k.tint(mix(water, PAL.cloud, 0.45)):
        k.shape(k.arcpts(x, y - 1, h * 0.3, h * 0.035, 0, 360, 30), lw=0.7, fill=Wt, amp=0.3)
    for j in range(3): k.line(k.arcpts(x + (j - 1) * h * 0.09, y - 1, h * 0.04, h * 0.01, 200, 340, 6), lw=0.35, amp=0, color=shade(water, 0.7))
    for i in range(n):
        dx = rr.uniform(-0.26, 0.26) * h; dy = rr.uniform(0.05, 0.62) * h
        if abs(dx) < 0.17 * h and dy > 0.12 * h: dx = (0.19 + rr.uniform(0, 0.06)) * h * (1 if dx >= 0 else -1)
        px, py, r = x + dx, y + dy, h * 0.011
        with k.tint(water): k.shape([(px, py + r * 2.6)] + k.arcpts(px, py, r, r, 200, 340, 8)[::-1] + [(px, py + r * 2.6)], lw=0.5, fill=Wt, amp=0)

CHARACTERS = dict(tamsin=tamsin, hedley=hedley, pip=pip, wenna=wenna, agnes=agnes)
