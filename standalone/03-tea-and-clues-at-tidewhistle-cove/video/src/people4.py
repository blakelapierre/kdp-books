"""people4: DETAILED colour ink characters for Case 4, The Sandbar at High Tide (same construction and line style as
people.py / people3.py: local 0..100 frame, feet at y=0, head centre at CY, Catmull-Rom outlines, colour under ink
through k.tint()). Every face goes through people.head, so the animation face states (people.FACE: eyes closed for a
blink frame, mouth open for a talking frame) work for all of them.

  quill(k, x, y, h, arm="down"|"chalk"|"compass")  Captain Quill, harbourmaster: white peaked cap, white beard,
                                                    navy reefer jacket with brass buttons, cream roll-neck
  rundle(k, x, y, h, prop=True)                     Mr Rundle, fisherman: rust knitted beanie, stubble beard,
                                                    blue canvas smock, corduroy trousers, green wellies, cockle fork
  morwenna(k, x, y, h, prop=True)                   Morwenna Day, florist: straw hat, long dark hair, sage flower dress,
                                                    rose cardigan, green wellies, white lilies
  pip(k, x, y, h)                                   Pip Carew (people3.pip) holding a hand brush
  ollie(k, x, y, h)                                 Constable Ollie Penrose: navy tunic and helmet, pocket notebook
  vicar(k, x, y, h)                                 the vicar: black cassock, white collar, grey hair, glasses, prayer book
  agnes(k, x, y, h, basket=True)                    Agnes Bell (people3.agnes) with a basket of scones

The three suspects (morwenna, pip, rundle) share ONE stance, ONE arm pose (people3 L_ARM / R_ARM: left arm down, right
forearm across the chest holding a small prop), the same head size, the same neutral face and the same level of detail
and colour weight. expr="sheepish" (eyes down, blush) is only used after the solution (Mr Rundle, returned scene)."""
import math
from colorink import PAL, C, shade, mix, K, Wt
from people import Fig, ell, tube, hand, shoe, neck, head, legs, CY
import people3 as P3
from people3 import sleeve_arm, skin_hand, face, L_ARM, L_HAND, R_ARM, R_HAND, SKIN

NAVY = C(50, 64, 104); NAVY2 = C(70, 88, 132); CREAM = C(240, 232, 212); BEARD = C(236, 234, 230); CAPTOP = C(250, 250, 246)
SMOCK = C(104, 140, 168); CORD = C(150, 112, 78); WELLY = C(66, 112, 84); BEANIE = C(188, 92, 64); STUBBLE = C(150, 112, 92)
HAIR_R = C(96, 70, 56); HAIR_M = C(84, 60, 52); DRESS_M = C(186, 210, 168); CARDI_M = C(226, 160, 160); STRAW = PAL.straw
LILY = C(252, 250, 242); STEM = C(110, 160, 96); POLLEN = C(236, 170, 70); CASSOCK = C(44, 44, 52)
BRASS = PAL.brass; BRASS_DK = C(176, 140, 64); WICKER = PAL.wicker; SCONE = C(226, 178, 112); BRUSH = C(178, 124, 80)

# ----------------------------------------------------------------------------- props (figure frame)
def compass_box(f, x, y, s=1.0):
    """Brass ship's compass in a little wooden box, seen from the front-top (figure frame, centre x, base y)."""
    k = f.k
    bx = [(x - 6 * s, y, 0), (x + 6 * s, y, 0), (x + 6 * s, y + 4.2 * s, 0), (x - 6 * s, y + 4.2 * s, 0)]
    with k.tint(PAL.wood): f.shape(bx, lw=0.7)
    f.shape(ell(x, y + 6.0 * s, 5.4 * s, 3.0 * s, n=24), lw=0.8, fill=BRASS)
    f.shape(ell(x, y + 6.3 * s, 4.2 * s, 2.2 * s, n=24), lw=0.5, fill=C(250, 246, 232))
    f.shape([(x - 3.4 * s, y + 6.6 * s, 0), (x, y + 7.0 * s, 0), (x + 3.4 * s, y + 6.0 * s, 0), (x, y + 5.6 * s, 0)], lw=0.3, fill=C(200, 70, 60))
    f.dot(x, y + 6.3 * s, 0.45 * s, fill=BRASS_DK)

def cockle_fork(f):
    """Short wooden-handled cockle fork held across the chest (same place as the other suspects' props)."""
    k = f.k
    f.shape([(2.4, 58.6, 0), (3.6, 58.4, 0), (7.2, 72.6, 0), (6.0, 72.8, 0)], lw=0.6, fill=PAL.wood)
    f.shape([(6.0, 72.0, 0), (8.0, 71.6, 0), (8.6, 74.2, 0), (6.2, 74.6, 0)], lw=0.5, fill=PAL.wood_dk)
    for j in range(4):
        x0 = 5.4 + j * 1.05; f.curve([(x0 + 0.6, 74.2), (x0 + 1.1, 78.6), (x0 + 1.5, 80.8)], lw=0.55, color=C(120, 120, 128))

def lilies(f):
    """Bunch of white lilies with green stems, held at the shared prop position."""
    k = f.k
    for j in range(5):
        a = math.radians(70 + j * 9); L = 13.5 + (j % 2) * 2
        f.curve([(4.6, 60.0), (4.6 + 0.5 * L * math.cos(a), 60 + 0.5 * L * math.sin(a)), (4.6 + L * math.cos(a), 60 + L * math.sin(a))], lw=0.5, color=shade(STEM, 0.8))
    for j, (a, L) in enumerate(((72, 15.0), (88, 16.6), (100, 14.2), (80, 12.0))):
        r = math.radians(a); px, py = 4.6 + L * math.cos(r), 60 + L * math.sin(r)
        for pa in (-40, 0, 40):   # three petals of a trumpet
            q = math.radians(a + pa); tx, ty = px + 3.0 * math.cos(q), py + 3.0 * math.sin(q)
            with k.tint(LILY): f.shape([(px, py), ((px + tx) / 2 - 0.9 * math.sin(q), (py + ty) / 2 + 0.9 * math.cos(q)), (tx, ty, 0),
                                       ((px + tx) / 2 + 0.9 * math.sin(q), (py + ty) / 2 - 0.9 * math.cos(q))], lw=0.45)
        f.dot(px + 1.2 * math.cos(r), py + 1.2 * math.sin(r), 0.35, fill=POLLEN)
    with k.tint(STEM):
        for (lx, ly, ang) in ((2.6, 64.0, 120), (7.4, 66.0, 50)):
            q = math.radians(ang); f.shape([(lx, ly), (lx + 2.8 * math.cos(q) - 0.8, ly + 2.8 * math.sin(q)), (lx + 5.2 * math.cos(q), ly + 5.2 * math.sin(q), 0),
                                            (lx + 2.8 * math.cos(q) + 0.8, ly + 2.8 * math.sin(q))], lw=0.4)
    f.shape([(3.0, 62.6, 0), (6.6, 62.8, 0), (6.4, 59.6, 0), (3.2, 59.4, 0)], lw=0.45, fill=C(196, 160, 210))   # ribbon tie

def hand_brush(f):
    """Pip's dustpan brush: wooden back, bristles, held across the chest."""
    k = f.k
    bk = [(2.2, 64.0, 0), (9.6, 66.2, 0), (9.0, 69.0, 0), (1.8, 66.8, 0)]
    with k.tint(BRUSH): f.shape(bk, lw=0.7)
    f.shape([(9.4, 66.6, 0), (12.6, 67.8, 0), (12.4, 68.8, 0), (9.2, 68.2, 0)], lw=0.5, fill=BRUSH)   # handle
    for j in range(9):
        x0 = 2.4 + j * 0.8; f.curve([(x0, 64.6 + j * 0.27), (x0 - 0.3, 62.2 + j * 0.27)], lw=0.35, color=C(90, 80, 70))

def scone_basket(f):
    """Agnes's wicker basket of scones with a gingham cloth, carried in her right hand (figure frame)."""
    k = f.k
    f.curve([(10.2, 48.6), (12.6, 55.0), (15.6, 48.6)], lw=0.9)
    bk = [(7.8, 48.6, 0), (18.0, 48.6, 0), (16.6, 38.8, 0.6), (9.2, 38.8, 0.6)]
    with k.tint(WICKER, hatch=shade(WICKER, 0.66)):
        f.shape(bk, lw=0.9); f.hatch(bk, angle=60, gap=1.0, lw=0.28); f.hatch(bk, angle=-60, gap=1.0, lw=0.28)
        f.shape(bk, lw=0.9, fill=None)
    for (sx, sy) in ((10.6, 49.4), (13.0, 50.0), (15.4, 49.4)):
        with k.tint(SCONE): f.shape(ell(sx, sy, 1.6, 1.2, 0, 180, 10) + [(sx - 1.6, sy)], lw=0.5)
    cl = [(8.2, 48.8, 0), (12.0, 47.6, 0), (11.0, 44.4, 0), (8.4, 45.6, 0)]
    with k.tint(C(232, 140, 140)): f.shape(cl, lw=0.5)
    f.clip(cl)
    for j in range(4): f.curve([(8 + j * 1.2, 44), (8.6 + j * 1.2, 49)], lw=0.5, color=PAL.cloud)
    f.unclip()

# ----------------------------------------------------------------------------- shared suspect lower body helpers
def _wellies(f, col=WELLY, top=20.0):
    k = f.k
    for sg in (-1, 1):
        s = sg; xx = sg * 4.0
        bt = [(xx - 2.6 * s, top, 0), (xx + 2.5 * s, top, 0), (xx + 2.6 * s, 3.0), (xx + 5.0 * s, 1.8), (xx + 5.2 * s, 0.2, 0), (xx - 2.9 * s, 0.2, 0), (xx - 2.9 * s, 2.6)]
        with k.tint(col, hatch=shade(col, 0.7)):
            f.shape(bt, lw=0.9); f.hatch(bt, angle=80, gap=1.5, lw=0.25, box=(xx + 0.8 * s - 2, 0, xx + 2.8 * s + 2, top))
            f.shape(bt, lw=0.9, fill=None)
        f.curve([(xx - 2.5 * s, top - 1.4), (xx + 2.4 * s, top - 1.4)], lw=0.35)
        f.curve([(xx - 2.6 * s, 1.0), (xx + 4.9 * s, 1.0)], lw=0.35, color=shade(col, 0.6))

# ----------------------------------------------------------------------------- characters
def rundle(k, x, y, h, expr="neutral", flip=False, prop=True, compass=False):
    """Mr Rundle, a fisherman from along the coast. compass=True (after the solution only): holding the compass."""
    with Fig(k, x, y, h, flip) as f:
        trou = [(-8.2, 46, 0), (-7.9, 30), (-7.2, 18.0, 0), (-1.2, 18.0, 0), (-0.8, 36), (0.8, 36), (1.2, 18.0, 0), (7.2, 18.0, 0), (7.9, 30), (8.2, 46, 0)]
        with k.tint(CORD, hatch=shade(CORD, 0.72)):
            f.shape(trou, lw=1.0); f.hatch(trou, angle=90, gap=0.9, lw=0.25); f.shape(trou, lw=1.0, fill=None)
        _wellies(f)
        sm = [(-2.9, 81.8), (-11.8, 79.4), (-12.8, 72), (-12.4, 60), (-13.4, 41.0, 0.6), (0, 40.2), (13.4, 41.0, 0.6), (12.4, 60), (12.8, 72), (11.8, 79.4), (2.9, 81.8)]
        with k.tint(SMOCK, hatch=shade(SMOCK, 0.72)):
            f.shape(sm, lw=1.1); f.hatch(sm, angle=-58, gap=1.5, lw=0.28, box=(7.6, 40, 14, 82)); f.shape(sm, lw=1.1, fill=None)
            pk = [(-7.6, 54.0, 0), (7.6, 54.0, 0), (8.4, 45.0, 0), (-8.4, 45.0, 0)]   # kangaroo pocket
            f.shape(pk, lw=0.7)
            for sg in (-1, 1): f.curve([(sg * 7.6, 54.0), (sg * 6.2, 49.4), (sg * 8.4, 45.0)], lw=0.35)
            f.shape([(-2.6, 81.4, 0), (2.6, 81.4, 0), (1.8, 71.0, 0), (-1.8, 71.0, 0)], lw=0.6)   # neck placket
        for by in (78.6, 74.6): f.dot(0.0, by, 0.5, fill=PAL.cloud, lw=0.35)
        for u in (-9, -4.5, 4.5, 9): f.curve([(u * 0.95, 44), (u * 1.02, 41.6)], lw=0.3)
        sleeve_arm(f, L_ARM, 2.9, SMOCK, cuff=4, hatch=dict(angle=-58, gap=2.0, lw=0.25))
        skin_hand(f, *L_HAND[:2], L_HAND[2], 1.05)
        sleeve_arm(f, R_ARM, 2.9, SMOCK, cuff=4, hatch=dict(angle=-58, gap=2.0, lw=0.25))
        if compass: compass_box(f, 5.6, 60.6, 0.95)
        elif prop: cockle_fork(f)
        skin_hand(f, *R_HAND[:2], R_HAND[2], 1.05)
        with k.tint(SKIN): neck(f, CY, w=2.4)
        with k.tint(SKIN, hatch=STUBBLE): head(f, 0, CY, rx=6.1, ry=7.4, jaw=0.74, expr=expr, nose="long", brows="thick", lines=1, beard=True)
        cheek = PAL.blush if expr == "sheepish" else PAL.cheek
        for sg in (-1, 1):
            f.shape(ell(sg * 3.3, CY - 1.1, 1.2 if expr != "sheepish" else 1.6, 0.7 if expr != "sheepish" else 0.95, n=14), lw=0, stroke=False,
                    fill=mix(cheek, SKIN, 0.4 if expr != "sheepish" else 0.0))
        with k.tint(HAIR_R):
            for sg in (-1, 1): f.shape([(sg * 5.6, CY + 3.6), (sg * 6.8, CY + 2.6), (sg * 6.9, CY - 0.8), (sg * 6.0, CY - 1.0), (sg * 5.7, CY + 1.2)], lw=0.6)
        bn = [(-6.9, CY + 3.2, 0), (-7.3, CY + 7.4), (-5.4, CY + 11.4), (0, CY + 12.8), (5.4, CY + 11.4), (7.3, CY + 7.4), (6.9, CY + 3.2, 0)]
        with k.tint(BEANIE, hatch=shade(BEANIE, 0.7)):
            f.shape(bn, lw=1.0)
            for j in range(9): f.curve([(-5.6 + j * 1.4, CY + 6.6), (-5.0 + j * 1.25, CY + 9.8), (-3.6 + j * 0.9, CY + 12.0)], lw=0.3, color=shade(BEANIE, 0.7))
            rib = [(-7.2, CY + 2.6, 0), (7.2, CY + 2.6, 0), (7.5, CY + 6.4, 0), (-7.5, CY + 6.4, 0)]
            f.shape(rib, lw=0.9); f.hatch(rib, angle=90, gap=0.9, lw=0.3)

def quill(k, x, y, h, expr="smile", flip=False, arm="down"):
    """Captain Quill, harbourmaster. arm: 'down', 'chalk' (right arm raised, chalk in hand) or 'compass' (holding it)."""
    with Fig(k, x, y, h, flip) as f:
        trou = [(-8.0, 44, 0), (-7.8, 26), (-7.0, 3.6, 0), (-1.2, 3.6, 0), (-0.8, 36), (0.8, 36), (1.2, 3.6, 0), (7.0, 3.6, 0), (7.8, 26), (8.0, 44, 0)]
        with k.tint(NAVY, hatch=shade(NAVY, 0.7)):
            f.shape(trou, lw=1.0); f.hatch(trou, angle=88, gap=1.8, lw=0.25, box=(3, 0, 9, 44)); f.shape(trou, lw=1.0, fill=None)
        with k.tint(None, dark=C(40, 36, 36)):
            for sg in (-1, 1): shoe(f, sg * 4.0, sg)
        jk = [(-3.0, 81.8), (-12.0, 79.4), (-13.0, 72), (-12.6, 60), (-13.4, 38.0, 0.6), (0, 37.4), (13.4, 38.0, 0.6), (12.6, 60), (13.0, 72), (12.0, 79.4), (3.0, 81.8)]
        with k.tint(NAVY, hatch=shade(NAVY, 0.68)):
            f.shape(jk, lw=1.1); f.hatch(jk, angle=-60, gap=1.6, lw=0.28, box=(8, 37, 14, 82)); f.shape(jk, lw=1.1, fill=None)
        with k.tint(CREAM, hatch=shade(CREAM, 0.8)):   # roll-neck jumper showing at the throat
            rn = [(-3.4, 82.6), (-3.6, 79.6), (0, 78.4), (3.6, 79.6), (3.4, 82.6), (0, 83.4)]
            f.shape(rn, lw=0.7); f.hatch(rn, angle=90, gap=0.8, lw=0.28)
            f.shape([(-2.4, 79.4, 0), (2.4, 79.4, 0), (0.0, 70.0, 0)], lw=0.5)
        with k.tint(NAVY2):   # lapels
            for sg in (-1, 1): f.shape([(sg * 2.8, 80.6, 0), (sg * 8.0, 79.4), (sg * 8.6, 72.4, 0), (sg * 4.2, 67.2, 0), (sg * 0.6, 64.0, 0), (sg * 2.0, 72.0)], lw=0.8)
        for j in range(3):
            for sg in (-1, 1): f.dot(sg * 4.0, 60.0 - j * 6.2, 0.75, fill=BRASS, lw=0.4)
        for sg in (-1, 1): f.curve([(sg * 4.4, 46.0), (sg * 10.4, 46.4)], lw=0.45)   # pocket slits
        sleeve_arm(f, L_ARM, 2.9, NAVY, cuff=4, cuff_col=NAVY2, hatch=dict(angle=-60, gap=2.0, lw=0.25))
        f.curve([(-15.8, 52.8), (-11.8, 52.4)], lw=0.6, color=BRASS)   # gold cuff braid
        skin_hand(f, *L_HAND[:2], L_HAND[2], 1.05)
        if arm == "chalk":
            ra = [(10.6, 77.6), (15.0, 71.0), (19.4, 67.4), (24.0, 68.6), (27.6, 71.0)]   # forearm forward, writing on the board
            sleeve_arm(f, ra, 2.9, NAVY, cuff=4, cuff_col=NAVY2, hatch=dict(angle=-60, gap=2.0, lw=0.25))
            f.shape([(29.4, 73.4, 0), (31.8, 75.0, 0), (31.3, 75.8, 0), (28.9, 74.2, 0)], lw=0.4, fill=PAL.cloud)   # chalk stick
            skin_hand(f, 28.2, 71.8, 30, 1.0)
        elif arm == "compass":
            sleeve_arm(f, R_ARM, 2.9, NAVY, cuff=4, cuff_col=NAVY2, hatch=dict(angle=-60, gap=2.0, lw=0.25))
            compass_box(f, 5.6, 60.6, 0.95)
            skin_hand(f, *R_HAND[:2], R_HAND[2], 1.05)
        else:
            sleeve_arm(f, [(10.6, 77.6), (13.4, 70), (14.2, 62), (14.0, 55), (13.7, 50.8)], 2.9, NAVY, cuff=4, cuff_col=NAVY2, hatch=dict(angle=-60, gap=2.0, lw=0.25))
            skin_hand(f, 13.7, 49.6, -88, 1.05)
        with k.tint(SKIN): neck(f, CY, w=2.4)
        face(f, expr, rx=6.1, ry=7.4, jaw=0.7, nose="button", brows="soft", lines=2)
        with k.tint(BEARD, hatch=shade(BEARD, 0.8)):
            bd = [(-6.0, CY - 0.6), (-5.6, CY - 4.6), (-3.4, CY - 7.6), (0, CY - 8.6), (3.4, CY - 7.6), (5.6, CY - 4.6), (6.0, CY - 0.6),
                  (5.0, CY - 1.6), (3.6, CY - 4.6), (1.6, CY - 5.2), (0, CY - 5.0), (-1.6, CY - 5.2), (-3.6, CY - 4.6), (-5.0, CY - 1.6)]
            f.shape(bd, lw=0.7); f.hatch(bd, angle=80, gap=1.0, lw=0.25)
            mo = [(-3.3, CY - 3.0), (-1.7, CY - 2.2), (0, CY - 2.15), (1.7, CY - 2.2), (3.3, CY - 3.0), (1.8, CY - 3.15), (0, CY - 2.95), (-1.8, CY - 3.15)]
            f.shape(mo, lw=0.4)
            for sg in (-1, 1): f.shape([(sg * 5.4, CY + 3.6), (sg * 6.6, CY + 2.8), (sg * 6.8, CY - 0.6), (sg * 6.0, CY - 1.2), (sg * 5.6, CY + 1.2)], lw=0.6)
        cap = [(-7.0, CY + 4.0, 0), (-8.2, CY + 7.6), (-6.4, CY + 9.6), (0, CY + 10.4), (6.4, CY + 9.6), (8.2, CY + 7.6), (7.0, CY + 4.0, 0)]
        with k.tint(CAPTOP, hatch=shade(CAPTOP, 0.82)): f.shape(cap, lw=1.0); f.hatch(cap, angle=60, gap=1.4, lw=0.25, box=(4, CY + 3, 9, CY + 11))
        band = [(-7.0, CY + 2.8, 0), (7.0, CY + 2.8, 0), (7.1, CY + 5.0, 0), (-7.1, CY + 5.0, 0)]
        with k.tint(NAVY): f.shape(band, lw=0.8)
        f.shape([(-7.2, CY + 3.0), (0, CY + 3.6), (7.2, CY + 3.0), (6.2, CY + 1.2), (0, CY + 1.4), (-6.2, CY + 1.2)], lw=0.7, fill=C(30, 34, 46))   # peak
        f.shape(ell(0, CY + 6.6, 1.5, 1.1, n=14), lw=0.4, fill=BRASS)   # badge
        f.curve([(-1.0, CY + 6.6), (1.0, CY + 6.6)], lw=0.3, color=BRASS_DK)

def morwenna(k, x, y, h, expr="neutral", flip=False, prop=True):
    """Morwenna Day (people.morwenna, in colour), in the shared suspect pose, holding white lilies."""
    with Fig(k, x, y, h, flip) as f:
        hair_back = [(-6.6, CY + 3), (-8.2, CY - 4), (-8.8, CY - 10), (-9.6, CY - 15.5), (-6.4, CY - 17.0), (0, CY - 16.2), (6.4, CY - 17.0), (9.6, CY - 15.5), (8.8, CY - 10), (8.2, CY - 4), (6.6, CY + 3)]
        with k.tint(HAIR_M, dark=HAIR_M): f.shape(hair_back, lw=0.9)
        for j in range(5): f.curve([(-7.5 + j * 0.3, CY - 2 - j), (-8.4 + j * 0.4, CY - 9 - j * 0.6), (-8.0 + j * 0.5, CY - 15 + j * 0.3)], lw=0.3, color=shade(HAIR_M, 1.6))
        with k.tint(C(236, 226, 214)): legs(f, x=3.0, top=24, w0=1.9, w1=1.5, ankle=14)
        _wellies(f, top=15.0)
        dress = [(-2.6, 81.0), (-8.8, 79.0), (-9.6, 72), (-8.2, 60), (-9.6, 44), (-12.6, 21.5, 0.6), (0, 20.6), (12.6, 21.5, 0.6), (9.6, 44), (8.2, 60), (9.6, 72), (8.8, 79.0), (2.6, 81.0)]
        with k.tint(DRESS_M): f.shape(dress, lw=1.1)
        f.clip(dress)   # flower print
        for gy in range(22, 82, 6):
            for gx in range(-14, 15, 6):
                px = gx + (3 if (gy // 6) % 2 else 0) + f.r.uniform(-0.8, 0.8); py = gy + f.r.uniform(-0.8, 0.8)
                for a in range(0, 360, 72): f.shape(ell(px + 0.8 * math.cos(math.radians(a)), py + 0.8 * math.sin(math.radians(a)), 0.55, 0.55, n=8), lw=0.25, fill=PAL.cloud)
                f.dot(px, py, 0.4, fill=PAL.sun)
        f.unclip()
        f.shape(dress, lw=1.1, fill=None)
        with k.tint(CARDI_M, hatch=shade(CARDI_M, 0.72)):
            for sg in (-1, 1):   # open cardigan, ribbed, to the hip
                pan = [(sg * 2.4, 81.0, 0), (sg * 8.9, 79.2), (sg * 10.0, 72), (sg * 9.4, 60), (sg * 10.4, 42.5, 0), (sg * 4.4, 42.0, 0), (sg * 3.6, 58), (sg * 2.4, 72)]
                f.shape(pan, lw=1.0); f.hatch(pan, angle=90, gap=1.1, lw=0.26); f.shape(pan, lw=1.0, fill=None)
                f.shape([(sg * 4.4, 44.6, 0), (sg * 10.3, 45.0, 0), (sg * 10.4, 42.5, 0), (sg * 4.4, 42.0, 0)], lw=0.6)
        for by in (74, 66, 58, 50): f.dot(-3.4, by, 0.6, fill=PAL.cloud, lw=0.4)
        sleeve_arm(f, L_ARM, 2.6, CARDI_M, cuff=4, hatch=dict(angle=90, gap=1.1, lw=0.26))
        skin_hand(f, *L_HAND[:2], L_HAND[2], 1.0)
        sleeve_arm(f, R_ARM, 2.6, CARDI_M, cuff=4, hatch=dict(angle=90, gap=1.1, lw=0.26))
        if prop: lilies(f)
        skin_hand(f, *R_HAND[:2], R_HAND[2], 1.0)
        with k.tint(SKIN): neck(f, CY, w=2.0)
        face(f, expr, rx=5.8, ry=7.3, jaw=0.6, nose="small")
        with k.tint(HAIR_M, dark=HAIR_M):
            for sg in (-1, 1):   # front locks framing the face
                f.shape([(sg * 1.0, CY + 6.4), (sg * 4.6, CY + 6.6), (sg * 6.9, CY + 3.0), (sg * 7.4, CY - 4.0), (sg * 7.8, CY - 9.5), (sg * 6.2, CY - 6.0), (sg * 5.9, CY - 1.0), (sg * 5.2, CY + 3.2), (sg * 2.8, CY + 4.6)], lw=0.6, fill=K)
        brim = ell(0, CY + 5.8, 14.2, 2.9, n=36)
        crown = [(-6.3, CY + 6.4, 0), (-6.6, CY + 9.5), (-5.0, CY + 12.2), (0, CY + 12.9), (5.0, CY + 12.2), (6.6, CY + 9.5), (6.3, CY + 6.4, 0)]
        with k.tint(STRAW, hatch=shade(STRAW, 0.7)):
            f.shape(brim, lw=1.0)
            for i in range(36):
                a = math.radians(i * 10); f.curve([(8.4 * math.cos(a), CY + 5.8 + 1.7 * math.sin(a)), (13.6 * math.cos(a), CY + 5.8 + 2.75 * math.sin(a))], lw=0.3, color=shade(STRAW, 0.7))
            f.shape(crown, lw=1.0); f.hatch(crown, angle=30, gap=1.3, lw=0.26, cross=True)
        band = [(-6.4, CY + 6.4, 0), (6.4, CY + 6.4, 0), (6.5, CY + 8.4, 0), (-6.5, CY + 8.4, 0)]
        rib = C(150, 120, 190)
        f.shape(band, lw=0.5, fill=rib)
        f.shape([(4.0, CY + 7.4), (6.6, CY + 9.2), (6.8, CY + 6.0)], lw=0.5, fill=rib); f.shape([(4.0, CY + 7.4), (6.0, CY + 4.4), (7.6, CY + 5.0)], lw=0.5, fill=rib)
        f.curve(ell(0, CY + 5.8, 14.2, 2.9, 180, 360, 18), lw=1.0)

def pip(k, x, y, h, expr="neutral", flip=False, prop=True):
    P3.pip(k, x, y, h, expr=expr, flip=flip, prop=hand_brush if prop else False)

def agnes(k, x, y, h, expr="smile", flip=False, basket=True):
    P3.agnes(k, x, y, h, expr=expr, flip=flip, bag=scone_basket if basket else False)

def vicar(k, x, y, h, expr="kind", flip=False):
    with Fig(k, x, y, h, flip) as f:
        with k.tint(None, dark=C(30, 30, 34)):
            for sg in (-1, 1): shoe(f, sg * 3.6, sg)
        cs = [(-2.8, 81.6), (-11.0, 79.4), (-12.0, 72), (-11.2, 60), (-11.8, 40), (-13.0, 3.6, 0.6), (0, 3.0), (13.0, 3.6, 0.6), (11.8, 40), (11.2, 60), (12.0, 72), (11.0, 79.4), (2.8, 81.6)]
        with k.tint(CASSOCK, dark=CASSOCK, hatch=C(90, 90, 100)):
            f.shape(cs, lw=1.1); f.hatch(cs, angle=-60, gap=1.6, lw=0.28, box=(7.0, 2, 14, 82))
        f.curve([(0, 78.0), (0, 4.0)], lw=0.35, color=C(110, 110, 120))
        for j in range(9): f.dot(0.7, 76.0 - j * 4.0, 0.4, fill=C(120, 120, 130))
        f.shape([(-3.0, 81.8, 0), (3.0, 81.8, 0), (3.2, 79.6, 0), (-3.2, 79.6, 0)], lw=0.6, fill=PAL.cloud)   # clerical collar
        for sg in (-1, 1):
            sleeve_arm(f, [(sg * 10.4, 77.6), (sg * 13.2, 70), (sg * 13.4, 62.5), (sg * 10.0, 58.4), (sg * 5.4, 57.4)], 2.7, CASSOCK)
        with k.tint(C(60, 50, 60)): f.shape([(-4.6, 54.6, 0), (4.6, 54.6, 0), (4.4, 61.6, 0), (-4.4, 61.6, 0)], lw=0.7)   # prayer book
        f.curve([(-3.8, 60.4), (3.8, 60.4)], lw=0.3, color=PAL.brass)
        for sg in (-1, 1): skin_hand(f, sg * 4.6, 57.8, 90 - sg * 80, 0.95)
        with k.tint(SKIN): neck(f, CY, w=2.2)
        face(f, expr, rx=6.0, ry=7.4, jaw=0.64, glasses=True, nose="long", lines=2)
        with k.tint(PAL.hair_grey):
            hr = [(-6.4, CY - 0.4), (-7.0, CY + 3.2), (-5.6, CY + 7.0), (-2.6, CY + 8.6), (1.0, CY + 8.8), (4.6, CY + 7.8), (6.8, CY + 4.6), (6.4, CY - 0.4),
                  (5.4, CY + 3.0), (2.0, CY + 5.6), (-2.0, CY + 5.0), (-5.4, CY + 3.0)]
            f.shape(hr, lw=0.8)

def ollie(k, x, y, h, expr="smile", flip=False):
    """Constable Ollie Penrose (people.ollie, in colour: navy uniform, skin-coloured face and hands)."""
    from people import arm
    with Fig(k, x, y, h, flip) as f:
        with k.tint(None, dark=NAVY):
            trou = [(-8.0, 46, 0), (-7.8, 26), (-7.0, 3.4, 0), (-1.2, 3.4, 0), (-0.8, 36), (0.8, 36), (1.2, 3.4, 0), (7.0, 3.4, 0), (7.8, 26), (8.0, 46, 0)]
            f.shape(trou, lw=1.0, fill=K)
            for sg in (-1, 1): f.curve([(sg * 4.2, 34), (sg * 4.1, 6)], lw=0.3, color=NAVY2)
        with k.tint(None, dark=C(30, 30, 36)):
            for sg in (-1, 1): shoe(f, sg * 4.0, sg, "boot", top=4.0)
        with k.tint(None, dark=NAVY):
            tun = [(-2.9, 81.6), (-11.6, 79.0), (-12.6, 72), (-12.0, 60), (-12.8, 43.5, 0), (12.8, 43.5, 0), (12.0, 60), (12.6, 72), (11.6, 79.0), (2.9, 81.6)]
            f.shape(tun, lw=1.1, fill=K)
            f.curve([(0, 80.5), (0, 43.8)], lw=0.4, color=NAVY2)
            for by in (75.5, 69.5, 63.5, 50.0): f.dot(0.9, by, 0.75, fill=PAL.silver, lw=0.35)
            for sg in (-1, 1):
                px = sg * 6.6
                f.curve([(px - 3.0, 72.5), (px + 3.0, 72.5), (px + 3.0, 70.4), (px, 69.6), (px - 3.0, 70.4), (px - 3.0, 72.5)], lw=0.45, color=NAVY2, t=0.3)
                f.curve([(px - 3.0, 70.2), (px - 3.0, 64.5), (px + 3.0, 64.5), (px + 3.0, 70.2)], lw=0.35, color=NAVY2, t=0.3)
                f.dot(px, 70.6, 0.42, fill=PAL.silver)
            f.shape([(-12.9, 58.6, 0), (12.9, 58.6, 0), (12.9, 55.4, 0), (-12.9, 55.4, 0)], lw=0.5, fill=C(30, 30, 36))
            f.shape([(-2.2, 59.2, 0), (2.2, 59.2, 0), (2.2, 54.8, 0), (-2.2, 54.8, 0)], lw=0.5, fill=PAL.silver)
            f.shape([(-3.6, 80.0, 0), (-3.2, 83.2, 0), (3.2, 83.2, 0), (3.6, 80.0, 0), (0, 79.0)], lw=0.6, fill=K)
            for sg in (-1, 1):
                for j in range(2): f.shape([(sg * (1.4 + j * 0.8), 80.9, 0), (sg * (2.0 + j * 0.8), 80.9, 0), (sg * (2.0 + j * 0.8), 82.1, 0), (sg * (1.4 + j * 0.8), 82.1, 0)], lw=0.01, fill=PAL.silver, stroke=False)
            arm(f, [(-10.8, 77.6), (-13.6, 70), (-14.4, 62), (-14.2, 55), (-13.9, 50.8)], 2.9, sleeve_fill=K)
        skin_hand(f, -13.9, 49.6, -92, 1.05)
        with k.tint(None, dark=NAVY): arm(f, [(10.8, 77.6), (13.8, 70), (14.4, 62.5), (11.2, 63.2), (7.8, 64.6)], 2.9, sleeve_fill=K)
        nb = [(2.6, 62.6, 0), (8.6, 63.4, 0), (8.0, 71.8, 0), (2.0, 71.0, 0)]
        f.shape(nb, lw=0.8, fill=PAL.cloud)
        for j in range(4): f.curve([(3.0, 64.6 + j * 1.6), (7.6, 65.2 + j * 1.6)], lw=0.3, color=C(120, 140, 180))
        f.shape([(2.0, 71.0, 0), (8.0, 71.8, 0), (8.0, 72.6, 0), (2.0, 71.8, 0)], lw=0.5, fill=C(150, 70, 60))
        skin_hand(f, 8.3, 65.0, 165, 1.0)
        with k.tint(SKIN): neck(f, CY, w=2.4)
        face(f, expr, rx=6.2, ry=7.3, jaw=0.7, nose="button", brows="soft")
        with k.tint(None, dark=PAL.hair_dark):
            for sg in (-1, 1): f.shape([(sg * 6.2, CY + 3.6, 0), (sg * 6.5, CY + 0.6), (sg * 5.6, CY + 0.4), (sg * 5.5, CY + 3.4, 0)], lw=0.4, fill=K)
        with k.tint(None, dark=NAVY):
            hel = [(-6.9, CY + 3.9, 0), (-7.2, CY + 8.6), (-6.0, CY + 13.8), (-3.2, CY + 17.0), (0, CY + 17.8), (3.2, CY + 17.0), (6.0, CY + 13.8), (7.2, CY + 8.6), (6.9, CY + 3.9, 0)]
            f.shape(hel, lw=1.0, fill=K)
            f.curve([(-5.3, CY + 6.0), (-5.6, CY + 10.4), (-4.2, CY + 14.2), (-2.4, CY + 15.8)], lw=0.6, color=NAVY2)
            f.shape([(-1.0, CY + 17.6, 0), (1.0, CY + 17.6, 0), (0.9, CY + 19.2), (0, CY + 19.7), (-0.9, CY + 19.2)], lw=0.5, fill=K)
            f.shape([(-8.0, CY + 4.4), (0, CY + 5.0), (8.0, CY + 4.4), (7.6, CY + 3.0), (0, CY + 3.0), (-7.6, CY + 3.0)], lw=0.7, fill=K)
        bx, by, R = 0, CY + 9.4, 2.9
        star = []
        for i in range(16):
            a = math.pi / 2 + 2 * math.pi * i / 16; rr = R if i % 2 == 0 else R * 0.68
            star.append((bx + rr * math.cos(a), by + rr * math.sin(a), 0))
        f.shape(star, lw=0.45, fill=PAL.silver)
        f.ring(bx, by, R * 0.45, lw=0.4, fill=NAVY); f.dot(bx, by, R * 0.18, fill=PAL.silver)
        f.curve([(-6.4, CY + 3.0), (-5.6, CY - 4.4), (-2.0, CY - 7.0), (2.0, CY - 7.0), (5.6, CY - 4.4), (6.4, CY + 3.0)], lw=0.45)

CHARACTERS = dict(quill=quill, rundle=rundle, morwenna=morwenna, pip=pip, agnes=agnes, vicar=vicar, ollie=ollie)
