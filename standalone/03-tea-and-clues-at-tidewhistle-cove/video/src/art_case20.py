"""Illustrations for Case 20, The Scent of Lavender: BLACK-AND-WHITE ink (bwkit) with the simple v1 peg-doll characters.
Scents are drawn as wavy "whiff" lines (rise layers) with a small text tag naming the smell. Tamsin's bookshop counter
with the velvet-lined drawer and the silver fountain pen. PART sprites use part_open (clip only, never frame2).
Hook (render.py HOOK_STYLE="scent"): borderless hero of the open drawer on the counter.
Fairness: Captain Quill, Hedley and Mrs Vosper share one stance, height, arms-down pose and neutral face in the cast strip and
the lineup; each panel gets the same style of smell tag. Mrs Vosper's lavender sprig only appears when it is narrated.
Only the confession shows Mrs Vosper sheepish.
Run: python3 art_case20.py [scene ...]"""
import os, sys, math
from functools import partial
import bwkit as B
from bwkit import plate_open, part_open, full_open, InkBW, PW, AW, AH, V2, V3, CW, CH
import figures as F
from inkart import K, Wt
from layers import save_layers

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-20")

def quill(k, x, y, h, **kw): kw.setdefault("prop", False); F.quill(k, x, y, h, **kw)
def hedley(k, x, y, h, **kw): B.overalls(k, x, y, h, paint=False, **kw)
def vosper(k, x, y, h, **kw): B.lady(k, x, y, h, dress="dots", hair="curls", hat=None, **kw)
def tamsin(k, x, y, h, **kw): kw.setdefault("prop", None); kw.setdefault("expr", "neutral"); F.tamsin(k, x, y, h, **kw)
def agnes(k, x, y, h, **kw): kw.setdefault("teapot", False); F.agnes(k, x, y, h, **kw)

def whiff_fx(k, w, h, v):
    ph = {"s0": 0, "s1": 1.6, "s2": 3.1}[v]
    pts = [(w / 2 + 3.2 * math.sin(t * 8 + ph), 2 + t * (h - 4)) for t in [i / 18 for i in range(19)]]
    k.line(pts, lw=0.8, amp=0)
FX_WHIFF = dict(whiff=dict(fn=whiff_fx, variants=["s0", "s1", "s2"], page=(14, 30)))

def _pen(k, x, y, s):
    body = [(x - s * 0.5, y - s * 0.05), (x + s * 0.3, y - s * 0.06), (x + s * 0.3, y + s * 0.06), (x - s * 0.5, y + s * 0.05)]
    k.shape(body, lw=1.0, fill=Wt, amp=0); k.hatch(body, angle=0, gap=1.6, lw=0.3)
    k.shape([(x + s * 0.3, y - s * 0.06), (x + s * 0.5, y), (x + s * 0.3, y + s * 0.06)], lw=0.9, fill=Wt, amp=0)
    k.line([(x - s * 0.35, y + s * 0.06), (x - s * 0.05, y + s * 0.08)], lw=1.2, amp=0)
InkBW.pen = _pen

def _drawer(k, x, y, w, h):
    """Open velvet-lined drawer seen from the front-above (x, y lower-left)."""
    k.shape([(x, y), (x + w, y), (x + w + 20, y + h), (x - 20, y + h)], lw=1.2, fill=Wt, amp=0)
    inner = [(x + 10, y + 8), (x + w - 10, y + 8), (x + w + 8, y + h - 6), (x - 8, y + h - 6)]
    k.shape(inner, lw=0.8, fill=Wt, amp=0); k.hatch(inner, angle=-60, gap=2.0, lw=0.25, cross=True)
    k.rect(x, y - 24, w, 24, lw=1.1, fill=Wt); k.circle(x + w / 2, y - 12, 4, lw=0.8, fill=Wt)
InkBW.drawer = _drawer

def _sprig(k, x, y, s=1.0):
    k.line([(x, y), (x + 4 * s, y + 22 * s)], lw=0.9, amp=0)
    for j in range(5): k.circle(x + 4 * s * (0.5 + j / 8) + (2 if j % 2 else -2) * s, y + (10 + j * 3.2) * s, 1.6 * s, lw=0.5, fill=K)
InkBW.sprig = _sprig

def counter_scene(k, w, h):
    k.floorboards(w, y=60); k.text(256, 334, "TAMSIN'S BOOKSHOP", size=12, font="Ink-Plex")
    for r in range(3):
        y = 200 + r * 40; k.line([(30, y), (180, y)], lw=0.8, amp=0)
        for j in range(10): k.rect(32 + j * 14, y, 10, 26 + (j * 5 % 9), lw=0.4, fill=Wt)
    k.rect(220, 60, 270, 110, lw=1.3, fill=Wt); k.line([(214, 170), (496, 170)], lw=1.6, amp=0)
    k.drawer(300, 182, 110, 50)

# ----------------------------------------------------------------------------- 1. hook hero
def hook_plate(k, w, h): full_open(k, w, h); counter_scene(k, w, h); k.pen(355, 210, 60); k.unclip()

# ----------------------------------------------------------------------------- 2. cast
CAST = [("CAPTAIN QUILL", quill), ("HEDLEY", hedley), ("MRS VOSPER", vosper)]
cast_plate = B.cast_plate_fn([n for n, _ in CAST], style="frames")

# ----------------------------------------------------------------------------- 3. Agnes's nose: tea and scones
def nose_plate(k, w, h): plate_open(k, w, h); k.tearoom(w, h, window=True, counter=True); k.table_cloth(250, 30, 200, 70); k.unclip()
def agnes_n(k, w, h, v): part_open(k, w, h); agnes(k, 170, 30, 220); k.unclip()
def tea_part(k, w, h, v):
    part_open(k, w, h); k.rect(300, 100, 26, 24, lw=0.9, fill=Wt); k.shape(k.arcpts(313, 124, 13, 4, 0, 360, 14), lw=0.7, fill=Wt, amp=0)
    k.text(313, 160, "breakfast or afternoon?", size=10, font="Ink-Kalam"); k.unclip()
def scone_part(k, w, h, v):
    part_open(k, w, h)
    for i in range(3): k.shape(k.arcpts(390 + i * 22, 102, 10, 9, 0, 180, 10) + [(400 + i * 22, 100), (380 + i * 22, 100)], lw=0.9, fill=Wt, amp=0.1)
    k.text(412, 130, "1 minute from burning!", size=10, font="Ink-Kalam"); k.unclip()

# ----------------------------------------------------------------------------- 4. the bookshop drawer and the pen; 3 customers looked inside
def shop_plate(k, w, h): plate_open(k, w, h); counter_scene(k, w, h); k.unclip()
def pen_part(k, w, h, v): part_open(k, w, h); k.pen(355, 210, 60); k.unclip()
def _behind_counter(k, fn):
    k.c.saveState(); p = k.c.beginPath(); p.rect(214, 171, 290, 200); k.c.clipPath(p, stroke=0); fn(); k.c.restoreState()
def tamsin_s(k, w, h, v): part_open(k, w, h); _behind_counter(k, lambda: tamsin(k, 445, 60, 210, flip=True)); k.unclip()
def three_part(k, w, h, v): part_open(k, w, h); k.pin_card(60, 140, 140, 50, ["shown to 3 customers,", "one after another"], size=11); k.unclip()
def gone_part(k, w, h, v): part_open(k, w, h); k.dashed_outline(325, 202, 64, 16); k.text(355, 250, "gone!", size=12, font="Ink-Kalam"); k.unclip()
def agnes_sniff(k, w, h, v): part_open(k, w, h); k.c.saveState(); k.c.translate(250, 60); k.c.rotate(-12); agnes(k, 0, 0, 170); k.c.restoreState(); k.unclip()
def lav_tag(k, w, h, v): part_open(k, w, h); k.rect(330, 290, 150, 36, lw=1.1, fill=Wt); k.text(405, 301, "lavender water!", size=13, font="Ink-Kalam"); k.unclip()

# ----------------------------------------------------------------------------- 5. lineup: what each customer smells of
def _p_quay(k, pw, h):
    k.harbour(pw, h, sea_y0=110, sea_y1=180, lighthouse=False, boats=True, wall_top=50)
    for i in range(3): k.rect(330 + i * 40, 50, 34, 26, lw=0.9, fill=Wt)
def _p_yard(k, pw, h):
    k.floorboards(pw, y=50); k.boat(380, 70, 110)
    k.rect(420, 90, 40, 50, lw=1.0, fill=Wt); k.line([(440, 90), (440, 60)], lw=1.2, amp=0); k.text(400, 250, "BOATYARD", size=11, font="Ink-Plex")
def _p_tea(k, pw, h): k.tearoom(pw, h, window=True, counter=False); k.table_cloth(310, 30, 150, 60)
lineup_plate = B.lineup_plate_fn([_p_quay, _p_yard, _p_tea], [n for n, _ in CAST])
SMELL = ["fish & seaweed", "engine oil", "lavender"]
def stag(k, w, h, v, i=0):
    part_open(k, w, h); x = i * PW + 300; k.rect(x, 290, 170, 38, lw=1.1, fill=Wt); k.text(x + 85, 301, SMELL[i], size=14, font="Ink-Kalam"); k.unclip()
def sprig_part(k, w, h, v): part_open(k, w, h); k.sprig(2 * PW + PW / 2 - 140 + 14, 50 + 220 * 0.66, 1.2); k.unclip()

# ----------------------------------------------------------------------------- 6. Mrs Vosper: "I barely glanced into that drawer"
def talk_plate(k, w, h): plate_open(k, w, h); k.tearoom(w, h, window=True, counter=False); k.table_cloth(200, 30, 140, 60); k.unclip()
def vosper_t(k, w, h, v):
    part_open(k, w, h); vosper(k, 140, 30, 210); k.sprig(154, 30 + 210 * 0.66, 1.3); k.unclip()
def agnes_t(k, w, h, v): part_open(k, w, h); agnes(k, 400, 30, 200, flip=True); k.unclip()

# ----------------------------------------------------------------------------- 7. solution board
def board_plate(k, w, h):
    plate_open(k, w, h); k.floorboards(w, y=60)
    k.case_board(24, 70, 464, 290, title="WHAT DOES THE DRAWER SMELL OF?")
    k.drawer(70, 220, 90, 40); k.text(115, 280, "the velvet:", size=11, font="Ink-Plex")
    for i, nm in enumerate(("QUILL", "HEDLEY", "MRS VOSPER")): k.text(300, 260 - i * 50, nm, size=12, font="Ink-Plex")
def b_lav(k, w, h, v): part_open(k, w, h); k.text(115, 186, "LAVENDER WATER", size=13, font="Ink-Plex"); k.unclip()
def b_sm(k, w, h, v, i=0):
    part_open(k, w, h); k.text(410, 260 - i * 50, SMELL[i], size=12, font="Ink-Kalam")
    if i < 2: k.line([(250, 254 - i * 50), (470, 270 - i * 50)], lw=1.8, amp=0)
    k.unclip()
def b_ring(k, w, h, v): part_open(k, w, h); k.shape(k.arcpts(360, 164, 110, 22, 0, 360, 36), lw=2.2, fill=None, amp=0.4); k.unclip()
def b_note(k, w, h, v): part_open(k, w, h); k.pin_card(250, 92, 220, 46, ["\u201cbarely glanced\u201d? No:", "she reached right inside"], size=11); k.unclip()

# ----------------------------------------------------------------------------- 8. confession
def conf_plate(k, w, h): plate_open(k, w, h); counter_scene(k, w, h); k.unclip()
def vosper_c(k, w, h, v):
    part_open(k, w, h); vosper(k, 140, 60, 200, expr="sheepish" if "sheepish" in v else "neutral"); k.sprig(154, 60 + 200 * 0.66, 1.3)
    k.rect(170, 80, 40, 34, lw=1.0, fill=Wt); k.unclip()
def pen_c(k, w, h, v): part_open(k, w, h); k.pen(210, 150, 50); k.unclip()
def tamsin_c(k, w, h, v): part_open(k, w, h); _behind_counter(k, lambda: tamsin(k, 445, 60, 210, flip=True)); k.unclip()
def ink_part(k, w, h, v):
    part_open(k, w, h); k.pin_card(250, 300, 160, 44, ["a plain pen", "+ a bottle of blue ink"], size=11)
    k.rect(270, 182, 20, 24, lw=0.9, fill=K); k.rect(274, 206, 12, 8, lw=0.8, fill=Wt); k.unclip()

def _vig(k, w, h): k.drawer(w * 0.25, h * 0.3, w * 0.5, h * 0.2); k.pen(w * 0.5, h * 0.4, w * 0.3)
vignette = B.vignette_fn(_vig)

def jobs():
    J = []
    J.append(dict(name="hook", w=AW, h=AH, plate=hook_plate, seed=2001))
    J.append(dict(name="cast", w=CW, h=CH, plate=cast_plate, seed=2002, parts={
        f"s{i}": dict(fn=B.cast_fig_fn(i, 3, fn), variants=V2) for i, (_, fn) in enumerate(CAST)}))
    J.append(dict(name="nose", w=AW, h=AH, plate=nose_plate, seed=2003, parts=dict(
        agnes=dict(fn=agnes_n, variants=V2), tea=dict(fn=tea_part, variants=["base"]), scone=dict(fn=scone_part, variants=["base"]), **FX_WHIFF)))
    J.append(dict(name="shop", w=AW, h=AH, plate=shop_plate, seed=2004, parts=dict(
        pen=dict(fn=pen_part, variants=["base"]), tamsin=dict(fn=tamsin_s, variants=V2), three=dict(fn=three_part, variants=["base"]),
        gone=dict(fn=gone_part, variants=["base"]), agnes=dict(fn=agnes_sniff, variants=V2), lav=dict(fn=lav_tag, variants=["base"]), **FX_WHIFF)))
    J.append(dict(name="lineup", w=3 * PW, h=AH, plate=lineup_plate, seed=2005, parts={
        **{f"s{i}": dict(fn=B.lineup_fig_fn(i, fn, x=PW / 2 - 140, y=50, fh=220), variants=V3) for i, (_, fn) in enumerate(CAST)},
        **{f"m{i}": dict(fn=partial(stag, i=i), variants=["base"]) for i in range(3)}, "sprig": dict(fn=sprig_part, variants=["base"]), **FX_WHIFF}))
    J.append(dict(name="talk", w=AW, h=AH, plate=talk_plate, seed=2006, parts=dict(
        vosper=dict(fn=vosper_t, variants=V3), agnes=dict(fn=agnes_t, variants=V2), **FX_WHIFF)))
    J.append(dict(name="board", w=AW, h=AH, plate=board_plate, seed=2007, parts={
        "lav": dict(fn=b_lav, variants=["base"]), **{f"b{i}": dict(fn=partial(b_sm, i=i), variants=["base"]) for i in range(3)},
        "ring": dict(fn=b_ring, variants=["base"]), "note": dict(fn=b_note, variants=["base"])}))
    J.append(dict(name="confess", w=AW, h=AH, plate=conf_plate, seed=2008, parts=dict(
        vosper=dict(fn=vosper_c, variants=["sheepish", "sheepish+blink"]), pen=dict(fn=pen_c, variants=["base"]), tamsin=dict(fn=tamsin_c, variants=V2),
        ink=dict(fn=ink_part, variants=["base"]), **FX_WHIFF)))
    J.append(dict(name="vignette", w=384, h=384, plate=vignette, seed=2009))
    return J

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    J = [j for j in jobs() if not want or j["name"] in want]
    save_layers(OUT, J, B.make_ink)
