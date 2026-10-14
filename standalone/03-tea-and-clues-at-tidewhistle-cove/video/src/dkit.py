"""dkit: DETAILED COLOUR kit for re-drawing the black-and-white Cases 10-30 in the Cases 4-9 style (Blake, Oct 13 2026).

Import this BEFORE an art_caseNN module. It
  * switches colorink to "color-detailed" (watercolour washes + paper grain),
  * replaces every simple peg-doll character the B&W scripts call (figures.F.<name>, bwkit.visitor / lady / overalls)
    with the DETAILED people3 / people4 characters (proper faces, hair, clothes, blink / talk FACE states for anim.py),
    keeping one shared suspect stance / arm pose / head size so fairness rules still hold,
  * gives the case scripts InkD (Ink4 colour scenery + every bwkit helper), with each bwkit scenery helper painted in
    its house colour and any plain-white case prop given a soft local colour (tiny fills stay paper),
  * keeps part_open (clip only) for every animated sprite, so no border ever rotates with a sprite.
Per-case colour plates (hand-painted backdrops) live in art_caseNN_color.py, which imports dkit then overrides plates.
Run any case: python3 art_color.py NN   (writes work/art-NN-color)."""
import math, os, random
os.environ.setdefault("TW_KIT_STYLE", "bw")      # bwkit's own (rejected) tint mode stays OFF; dkit does the colour
import colorink
colorink.set_style("color-detailed")
import art_case04 as A4
import bwkit as B
import figures as F
colorink.set_style("color-detailed")
from colorink import PAL, C, shade, mix, K, Wt
from people import Fig, ell, legs, shoe, neck, CY
import people3 as P3
import people4 as P4
from people3 import sleeve_arm, skin_hand, face, L_ARM, L_HAND, R_ARM, R_HAND, SKIN

# ============================================================================= detailed generic townsfolk
_EXPRS = {"neutral", "smile", "sheepish", "eyebrow", "kind"}
def _e(expr): return expr if expr in _EXPRS else "neutral"

def _hand_world(x, y, h, flip):
    return x + (-1 if flip else 1) * R_HAND[0] * h / 100, y + R_HAND[1] * h / 100

def townsman(k, x, y, h, expr="neutral", flip=False, jacket=C(150, 120, 90), trousers=C(84, 84, 100), shirt=C(236, 236, 230),
             tie=None, hat=None, hat_col=C(232, 214, 160), hair=C(110, 84, 64), moustache=False, beard=False, bald=False,
             stripe=False, check=False, apron=None, prop=None):
    """Detailed man (fenwick construction): trousers, shoes, jacket / shirt, optional tie / apron, hat (panama / bowler /
    cap / beanie), hair, moustache. prop: callable(k, hx, hy, h) in world coords at the right hand."""
    with Fig(k, x, y, h, flip) as f:
        trou = [(-8.0, 50, 0), (-7.7, 26), (-7.0, 3.6, 0), (-1.2, 3.6, 0), (-0.8, 38), (0.8, 38), (1.2, 3.6, 0), (7.0, 3.6, 0), (7.7, 26), (8.0, 50, 0)]
        with k.tint(trousers):
            f.shape(trou, lw=1.0); f.hatch(trou, angle=80, gap=1.8, lw=0.22); f.shape(trou, lw=1.0, fill=None)
        with k.tint(None, dark=C(54, 44, 40)):
            for sg in (-1, 1): shoe(f, sg * 4.0, sg, top=3.6)
        coat = [(-2.8, 82.0), (-11.4, 79.6), (-12.0, 72), (-11.2, 58), (-11.0, 44.0, 0), (11.0, 44.0, 0), (11.2, 58), (12.0, 72), (11.4, 79.6), (2.8, 82.0)]
        with k.tint(jacket, hatch=shade(jacket, 0.72)):
            f.shape(coat, lw=1.0)
            if stripe: f.hatch(coat, angle=90, gap=2.6, lw=0.25)
            if check: f.hatch(coat, angle=0, gap=3.0, lw=0.22, cross=True)
            f.shape(coat, lw=1.0, fill=None)
        with k.tint(shirt):
            f.shape([(-2.8, 81.6, 0), (2.8, 81.6, 0), (1.2, 64.0, 0), (-1.2, 64.0, 0)], lw=0.6)
        if tie is not None:
            with k.tint(tie): f.shape([(-0.8, 80.6, 0), (0.8, 80.6, 0), (1.3, 68.0, 0), (0, 66.0, 0), (-1.3, 68.0, 0)], lw=0.4)
        f.curve([(-2.8, 81.6), (-1.4, 64.0), (-2.0, 45.0)], lw=0.5); f.curve([(2.8, 81.6), (1.4, 64.0), (2.0, 45.0)], lw=0.5)
        if apron is not None:
            ap = [(-9.0, 74.0, 0), (-10.4, 48.0, 0), (-9.6, 30.0, 0), (9.6, 30.0, 0), (10.4, 48.0, 0), (9.0, 74.0, 0), (0, 76.0, 0)]
            with k.tint(apron, hatch=shade(apron, 0.8)): f.shape(ap, lw=1.0)
        for by_ in (60, 54, 48): f.dot(3.0, by_, 0.45, fill=shade(jacket, 0.55))
        sleeve_arm(f, L_ARM, 2.6, jacket, cuff=2); skin_hand(f, *L_HAND[:2], L_HAND[2], 1.0)
        sleeve_arm(f, R_ARM, 2.6, jacket, cuff=2); skin_hand(f, *R_HAND[:2], R_HAND[2], 1.0)
        with k.tint(SKIN): neck(f, CY, w=2.4)
        face(f, _e(expr), rx=6.2, ry=7.4, jaw=0.72, nose="long" if moustache else "small", brows="thick")
        with k.tint(hair, hatch=shade(hair, 0.75)):
            for sg in (-1, 1):
                f.shape([(sg * 5.6, CY + 2.8, 0), (sg * 6.4, CY - 0.4), (sg * 5.2, CY - 0.6), (sg * 5.0, CY + 2.4, 0)], lw=0.4)
            if not bald and hat in (None, "cap", "beanie"):
                f.shape([(-6.0, CY + 2.4), (-5.6, CY + 6.4), (-2.6, CY + 8.4), (0, CY + 8.8), (2.6, CY + 8.4), (5.6, CY + 6.4), (6.0, CY + 2.4),
                         (4.0, CY + 4.6), (0, CY + 5.2), (-4.0, CY + 4.6)], lw=0.6)
            if moustache:
                f.shape([(-3.0, CY - 3.0), (-1.2, CY - 2.2), (0, CY - 2.5), (1.2, CY - 2.2), (3.0, CY - 3.0), (1.4, CY - 3.4), (-1.4, CY - 3.4)], lw=0.4)
            if beard:
                f.shape([(-5.6, CY - 0.5), (-4.6, CY - 6.0), (0, CY - 8.6), (4.6, CY - 6.0), (5.6, CY - 0.5), (3.0, CY - 3.6), (0, CY - 4.2), (-3.0, CY - 3.6)], lw=0.5)
        if hat == "panama" or hat == "bowler":
            col = hat_col if hat == "panama" else C(52, 50, 56)
            with k.tint(col):
                f.shape(ell(0, CY + 4.2, 10.0 if hat == "panama" else 8.0, 1.8, n=24), lw=0.8)
                f.shape([(-5.6, CY + 4.4), (-5.4, CY + 9.6), (0, CY + 10.6), (5.4, CY + 9.6), (5.6, CY + 4.4)], lw=0.8)
            if hat == "panama":
                with k.tint(C(60, 60, 70)): f.shape([(-5.6, CY + 4.6, 0), (5.6, CY + 4.6, 0), (5.5, CY + 6.0, 0), (-5.5, CY + 6.0, 0)], lw=0.3)
        elif hat == "cap":
            with k.tint(hat_col, hatch=shade(hat_col, 0.7)):
                cp = [(-6.2, CY + 4.0), (-5.8, CY + 8.2), (0, CY + 9.8), (5.8, CY + 8.2), (6.2, CY + 4.0)]
                f.shape(cp, lw=0.8); f.hatch(cp, angle=45, gap=1.2, lw=0.2, cross=True); f.shape(cp, lw=0.8, fill=None)
                f.shape([(2.0, CY + 4.4, 0), (10.0, CY + 3.6, 0), (9.6, CY + 5.0, 0), (3.0, CY + 6.0, 0)], lw=0.6)
        elif hat == "beanie":
            with k.tint(hat_col, hatch=shade(hat_col, 0.7)):
                bp = [(-6.4, CY + 3.6), (-6.0, CY + 8.6), (0, CY + 11.0), (6.0, CY + 8.6), (6.4, CY + 3.6)]
                f.shape(bp, lw=0.8); f.hatch(bp, angle=90, gap=1.0, lw=0.2); f.shape(bp, lw=0.8, fill=None)
    if prop:
        hx, hy = _hand_world(x, y, h, flip); prop(k, hx, hy, h)

def townswoman(k, x, y, h, expr="neutral", flip=False, dress=C(178, 196, 226), dress2=None, cardigan=None, hair=C(110, 78, 58),
               hairstyle="bob", hat=None, hat_col=C(244, 214, 150), apron=None, dots=None, stripe=False, shawl=None, legs_col=C(226, 206, 192),
               prop=None):
    """Detailed woman (kerensa / demelza construction): dress, optional cardigan / apron / shawl, hair (bob / bun / long /
    curls / plait), optional hat (sun / bonnet). prop: callable(k, hx, hy, h) in world coords at the right hand."""
    with Fig(k, x, y, h, flip) as f:
        if hairstyle == "long":
            with k.tint(hair): f.shape([(-6.6, CY + 2.0), (-8.4, CY - 16.0), (8.4, CY - 16.0), (6.6, CY + 2.0)], lw=0.7)
        with k.tint(legs_col): legs(f, x=3.2, top=34, w0=1.9, w1=1.5, ankle=6)
        with k.tint(None, dark=C(90, 60, 50)):
            for sg in (-1, 1): shoe(f, sg * 3.5, sg, top=2.8)
        d = [(-2.6, 81.4), (-11.0, 79.0), (-12.2, 70), (-13.2, 48), (-14.0, 28.0, 0.6), (0, 26.5), (14.0, 28.0, 0.6), (13.2, 48), (12.2, 70), (11.0, 79.0), (2.6, 81.4)]
        with k.tint(dress, hatch=dress2 or shade(dress, 0.78)):
            f.shape(d, lw=1.1)
            if stripe: f.hatch(d, angle=90, gap=2.4, lw=0.3)
            else: f.hatch(d, angle=-40, gap=2.2, lw=0.24, box=(7, 27, 15, 82))
            f.shape(d, lw=1.1, fill=None)
        if dots is not None:
            for (fx, fy) in ((-7, 34), (-2, 40), (4, 34), (8, 44), (-6, 50), (1, 52), (6, 58), (-4, 62), (-9, 42), (3, 46)):
                f.dot(fx, fy, 0.8, fill=dots)
        if cardigan is not None:
            top = [(-2.6, 81.4), (-11.0, 79.0), (-12.0, 70), (-11.0, 56), (-10.4, 50.0, 0), (-2.0, 50.0, 0), (-1.6, 66, 0), (1.6, 66, 0), (2.0, 50.0, 0), (10.4, 50.0, 0), (11.0, 56), (12.0, 70), (11.0, 79.0), (2.6, 81.4)]
            with k.tint(cardigan, hatch=shade(cardigan, 0.75)): f.shape(top, lw=1.0)
        if apron is not None:
            ap = [(-8.0, 70.0, 0), (-9.6, 46.0, 0), (-10.4, 30.0, 0), (10.4, 30.0, 0), (9.6, 46.0, 0), (8.0, 70.0, 0)]
            with k.tint(apron, hatch=shade(apron, 0.85)): f.shape(ap, lw=0.9)
        if shawl is not None:
            sw = [(-11.4, 80.0), (11.4, 80.0), (9.0, 66.0), (0, 58.0), (-9.0, 66.0)]
            with k.tint(shawl, hatch=shade(shawl, 0.7)):
                f.shape(sw, lw=0.9); f.hatch(sw, angle=45, gap=1.6, lw=0.22, cross=True); f.shape(sw, lw=0.9, fill=None)
        sl = cardigan or dress
        sleeve_arm(f, L_ARM, 2.5, sl, cuff=2); skin_hand(f, *L_HAND[:2], L_HAND[2], 0.95)
        sleeve_arm(f, R_ARM, 2.5, sl, cuff=2); skin_hand(f, *R_HAND[:2], R_HAND[2], 0.95)
        with k.tint(SKIN): neck(f, CY, w=2.1)
        face(f, _e(expr), rx=5.8, ry=7.0, jaw=0.62, nose="small", brows="soft")
        with k.tint(hair, hatch=shade(hair, 0.75)):
            f.shape([(-6.2, CY + 2.0), (-5.8, CY + 6.4), (-2.8, CY + 8.6), (0, CY + 9.0), (2.8, CY + 8.6), (5.8, CY + 6.4), (6.2, CY + 2.0),
                     (4.6, CY + 4.4), (0.6, CY + 5.2), (-3.6, CY + 4.2)], lw=0.7)
            for sg in (-1, 1): f.shape([(sg * 5.6, CY + 3.0), (sg * 6.8, CY - (3.0 if hairstyle == "bob" else 0.6)), (sg * 6.0, CY - (4.0 if hairstyle == "bob" else 1.6)), (sg * 5.0, CY + 0.8)], lw=0.5)
            if hairstyle == "bun": f.shape(ell(0, CY + 9.6, 3.0, 2.4, n=16), lw=0.6)
            if hairstyle == "plait":
                for j in range(5): f.shape(ell(-6.4 + j * 0.25, CY - 3.0 - j * 3.0, 1.5, 1.7, n=12), lw=0.45)
            if hairstyle == "curls":
                for i in range(9):
                    a = math.radians(15 + i * 18.75); f.shape(ell(6.6 * math.cos(a), CY + 2.0 + 6.4 * math.sin(a), 1.8, 1.8, n=10), lw=0.4)
        if hat == "sun":
            with k.tint(hat_col):
                f.shape([(-10.5, CY + 3.0), (-8, CY + 5.2), (0, CY + 6.0), (8, CY + 5.2), (10.5, CY + 3.0), (8, CY + 1.8), (0, CY + 2.0), (-8, CY + 1.8)], lw=0.9)
                f.shape([(-5.0, CY + 3.2), (-5.4, CY + 8.0), (-2.5, CY + 11.0), (0, CY + 11.6), (2.5, CY + 11.0), (5.4, CY + 8.0), (5.0, CY + 3.2)], lw=0.9)
            f.shape([(-5.2, CY + 5.4, 0), (5.2, CY + 5.4, 0), (5.2, CY + 6.8, 0), (-5.2, CY + 6.8, 0)], lw=0.4, fill=C(196, 84, 104))
        elif hat == "bonnet":
            with k.tint(hat_col, hatch=shade(hat_col, 0.75)):
                bn = [(-8.0, CY - 2.0), (-8.6, CY + 6.0), (-4.0, CY + 11.0), (0, CY + 11.6), (4.0, CY + 11.0), (8.6, CY + 6.0), (8.0, CY - 2.0), (6.4, CY + 4.0), (0, CY + 7.4), (-6.4, CY + 4.0)]
                f.shape(bn, lw=0.9); f.hatch(bn, angle=0, gap=1.4, lw=0.2); f.shape(bn, lw=0.9, fill=None)
    if prop:
        hx, hy = _hand_world(x, y, h, flip); prop(k, hx, hy, h)

# ============================================================================= swap the simple characters for detailed ones
def _p4(fn, prop_kw="prop", **fixed):
    def g(k, x, y, h, expr="neutral", flip=False, **kw):
        a = dict(fixed); pr = kw.get("prop")
        if callable(pr): a[prop_kw] = False
        elif prop_kw: a.setdefault(prop_kw, False)
        fn(k, x, y, h, expr=_e(expr), flip=flip, **a)
        if callable(pr): hx, hy = _hand_world(x, y, h, flip); pr(k, hx, hy, h)
    return g

LOVEDAY = dict(dress=C(246, 214, 110), apron=C(252, 248, 238), hair=PAL.hair_ginger, hairstyle="bob", dots=C(236, 150, 60))
SWAP = dict(
    agnes=lambda k, x, y, h, expr="smile", flip=False, **kw: P4.agnes(k, x, y, h, expr=_e(expr), flip=flip, basket=False),
    ollie=lambda k, x, y, h, expr="smile", flip=False, **kw: P4.ollie(k, x, y, h, expr=_e(expr), flip=flip),
    morwenna=_p4(P4.morwenna), hedley=_p4(P4.hedley), jago=_p4(P4.jago), quill=lambda k, x, y, h, expr="neutral", flip=False, **kw: P4.quill(k, x, y, h, expr=_e(expr), flip=flip),
    demelza=_p4(P4.demelza), tamsin=_p4(P4.tamsin), pip=_p4(P4.pip), wenna=_p4(P4.wenna),
    loveday=lambda k, x, y, h, expr="smile", flip=False, **kw: townswoman(k, x, y, h, expr=expr, flip=flip, **LOVEDAY),
    bramble=lambda k, x, y, h, expr="neutral", flip=False, **kw: townsman(k, x, y, h, expr=expr, flip=flip, jacket=C(232, 222, 196), shirt=PAL.glass, hat="panama"),
)
for _n, _fn in SWAP.items(): setattr(F, _n, _fn)

_SUITS = dict(plain=dict(jacket=C(214, 196, 160)), dark=dict(jacket=C(56, 70, 108)), stripe=dict(jacket=C(196, 210, 226), stripe=True),
              check=dict(jacket=C(186, 150, 110), check=True))
def visitor(k, x, y, h, expr="neutral", flip=False, suit="plain", hat="panama", tie=True, prop=None, moustache=False):
    townsman(k, x, y, h, expr=expr, flip=flip, tie=C(150, 60, 64) if tie else None, hat=hat, moustache=moustache, prop=prop,
             hat_col=C(232, 214, 160) if hat == "panama" else C(120, 110, 96), **_SUITS.get(suit, _SUITS["plain"]))
_DRESSES = dict(dots=dict(dress=C(236, 236, 244), dots=C(196, 84, 104)), stripe=dict(dress=C(200, 222, 236), stripe=True),
                plain=dict(dress=C(214, 226, 196)), dark=dict(dress=C(70, 84, 120)))
_HAIRS = dict(bun=C(176, 172, 180), bob=C(110, 78, 58), long=C(70, 52, 44), curls=C(150, 96, 60))
def lady(k, x, y, h, expr="neutral", flip=False, dress="dots", hair="bun", hat=None, prop=None, shawl=False):
    townswoman(k, x, y, h, expr=expr, flip=flip, hairstyle=hair, hair=_HAIRS.get(hair, C(110, 78, 58)), hat=hat,
               shawl=C(200, 120, 120) if shawl else None, prop=prop, **_DRESSES.get(dress, _DRESSES["plain"]))
def overalls(k, x, y, h, expr="neutral", flip=False, paint=False, cap=True, prop=None):
    townsman(k, x, y, h, expr=expr, flip=flip, jacket=C(92, 120, 160), trousers=C(80, 104, 140), apron=C(110, 140, 176),
             hat="cap" if cap else None, hat_col=C(140, 120, 96), prop=prop)
    if paint:
        for sx in (-0.05, 0.05):
            k.circle(x + sx * h, y + h * 0.12, h * 0.02, lw=0, fill=C(250, 250, 246), stroke=False)
B.visitor, B.lady, B.overalls = visitor, lady, overalls

# ============================================================================= ink: colour scenery + every bwkit helper
_HOUSE = dict(sun=PAL.sun, cloud=PAL.cloud, headland=PAL.headland, stones=PAL.rock, floorboards=PAL.floor,
              window_view=PAL.glass, table_cloth=PAL.cloth_tbl, bar=PAL.wood, collection_box=PAL.bag,
              wet_bench=PAL.teal, crate=PAL.wood, slipway=PAL.rock, car=PAL.doors[0], coins=PAL.brass, banknote=PAL.sage,
              pin_card=PAL.note_yellow, clock_face=PAL.cream, dashed_outline=PAL.sand, lifeboat_station=PAL.walls[2], inn=PAL.walls[1])
_PROPS = [C(206, 160, 112), C(178, 206, 222), C(232, 180, 170), C(186, 214, 176), C(240, 214, 140), C(214, 190, 222), C(170, 124, 90)]

class InkD(A4.Ink4, B.InkBW):
    _auto_seed = 0
    def _plain(s, fill, area, round_=False):
        if fill is None or s._top() is not None or not colorink._is(fill, Wt) or area < 260: return fill
        if area > 60000: return C(246, 234, 210)
        if round_ and area > 2500: return C(132, 176, 112)
        s._ai = getattr(s, "_ai", 0) + 1
        return _PROPS[(s._ai * 3 + s._auto_seed) % len(_PROPS)]
    def shape(s, pts, lw=0.8, fill=Wt, stroke=True, amp=0.3):
        xs = [p[0] for p in pts] or [0]; ys = [p[1] for p in pts] or [0]
        return super().shape(pts, lw=lw, fill=s._plain(fill, (max(xs) - min(xs)) * (max(ys) - min(ys))), stroke=stroke, amp=amp)
    def circle(s, x, y, r, lw=0.8, fill=Wt, stroke=True):
        return super().circle(x, y, r, lw=lw, fill=s._plain(fill, 3.14 * r * r, True), stroke=stroke)
    def sea(s, x0, x1, y0, y1, *a, **kw):
        s.vgrad(x0, y0, x1, y1, A4.SEA, A4.SEA2, steps=8)
        with s.tint(A4.SEA, hatch=shade(A4.SEA2, 0.8)): return B.InkBW.sea(s, x0, x1, y0, y1, *a, **kw)
    def floorboards(s, w, y=96, n=9):
        s.vgrad(14, 14, w - 14, y, PAL.floor, PAL.floor2, steps=8)
        with s.tint(PAL.floor, hatch=shade(PAL.floor2, 0.8)): return B.InkBW.floorboards(s, w, y=y, n=n)
    def tearoom(s, w, h, window=True, counter=True, sign=True):
        A4._tearoom(s, w, h)
    def case_board(s, x, y, w, hgt, title="AGNES'S CASE BOARD"):
        s.rect(x - 6, y - 6, w + 12, hgt + 12, lw=1.4, fill=PAL.wood_dk)
        s.wash_rect(x, y, x + w, y + hgt, C(196, 160, 112))
        rr = random.Random(7)
        for _ in range(140): s.circle(x + rr.uniform(4, w - 4), y + rr.uniform(4, hgt - 4), 0.8, lw=0, fill=C(170, 132, 90), stroke=False)
        s.rect(x + w / 2 - 110, y + hgt - 34, 220, 24, lw=0.9, fill=C(250, 244, 226))
        s.text(x + w / 2, y + hgt - 26, title, size=12, font="Ink-Plex", color=PAL.navy)

def _house(name, col):
    orig = getattr(B.InkBW, name, None)
    if orig is None: return
    def f(s, *a, **kw):
        with s.tint(col): return orig(s, *a, **kw)
    setattr(InkD, name, f)
for _n, _c in _HOUSE.items(): _house(_n, _c)

def floor_wall(k, w, h, y=96, wall=C(246, 232, 206), floor=PAL.floor):
    """Interior backdrop: papered wall + plank floor (use first in a plate)."""
    k.wash_rect(14, y, w - 14, h - 14, wall); k.vgrad(14, 14, w - 14, y, floor, PAL.floor2, steps=8)
    for i in range(int((y - 14) / 11) + 1): k.line([(14, 14 + i * 11), (w - 14, 14 + i * 11)], lw=0.35, amp=0.2, color=shade(PAL.floor2, 0.75))
    k.line([(14, y), (w - 14, y)], lw=0.9, amp=0.1)

def outdoor(k, w, h, horizon=180, ground=C(214, 200, 168), sky=(C(214, 233, 240), C(246, 238, 220))):
    k.vgrad(14, horizon, w - 14, h - 14, sky[0], sky[1], steps=10); k.wash_rect(14, 14, w - 14, horizon, ground)

# every plate gets a painted backdrop first (cases that paint their own cover it)
def plate_open(k, w, h):
    k.frame2(w, h); k.clip_rect(14, 14, w - 14, h - 14); floor_wall(k, w, h, y=60)
def full_open(k, w, h):
    k.clip_rect(0, 0, w, h); floor_wall(k, w + 28, h + 28, y=60)
B.plate_open, B.full_open = plate_open, full_open

def make_ink(c, seed):
    k = InkD(c, seed=seed); k._auto_seed = seed % 7; return k
B.make_ink = make_ink

# bwkit cast / lineup / vignette backdrops in colour
_cast0 = B._cast_plate
def _cast_plate(k, w, h, names=(), style="cards"):
    k.wash_rect(0, 0, w, h, C(247, 240, 225)); _cast0(k, w, h, names=names, style=style)
B._cast_plate = _cast_plate
_lp0 = B._lineup_plate
def _lineup_plate(k, w, h, backdrops=(), names=()):
    _lp0(k, w, h, backdrops=backdrops, names=names)
B._lineup_plate = _lineup_plate
_vg0 = B._vignette
def _vignette(k, w, h, inside=None):
    k.circle(w / 2, h / 2, w * 0.46, lw=1.4, fill=C(250, 214, 168))
    def ins(k, w, h):
        k.vgrad(0, 0, w, h, C(214, 233, 240), C(246, 232, 206), steps=10); inside(k, w, h)
    _vg0(k, w, h, inside=ins)
B._vignette = _vignette
