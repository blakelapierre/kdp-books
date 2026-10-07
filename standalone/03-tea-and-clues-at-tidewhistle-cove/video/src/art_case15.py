"""Illustrations for Case 15, The Warm Bonnet: BLACK-AND-WHITE ink (bwkit) with the simple v1 peg-doll characters.
Biscuit the ginger cat (striped loaf, hatched) sleeps on any warm car bonnet; three small blue cars (hatched bodies).
PART sprites use part_open (clip only, never frame2).
Hook (render.py HOOK_STYLE="wiper"): borderless hero of Mr Treloar's street with a small car and the sleeping cat.
Fairness: Mr Fenwick, Kerensa and Mr Treloar share one stance, height, arms-down pose and neutral face in the cast strip
and the lineup (each with the same small car); only the confession shows Mr Treloar sheepish.
Run: python3 art_case15.py [scene ...]"""
import os, sys, math, random
from functools import partial
import bwkit as B
from bwkit import plate_open, part_open, full_open, InkBW, nameplate, PW, AW, AH, V2, V3, CW, CH
import figures as F
from inkart import K, Wt
from layers import save_layers

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-15")

def fenwick(k, x, y, h, **kw): B.visitor(k, x, y, h, suit="dark", hat="cap", tie=False, moustache=True, **kw)
def kerensa(k, x, y, h, **kw): B.lady(k, x, y, h, dress="stripe", hair="curls", hat="sun", **kw)
def treloar(k, x, y, h, **kw): B.visitor(k, x, y, h, suit="plain", hat=None, tie=True, **kw)
def treloar_gown(k, x, y, h, **kw): B.visitor(k, x, y, h, suit="check", hat=None, tie=False, **kw)
def agnes(k, x, y, h, **kw): kw.setdefault("teapot", False); F.agnes(k, x, y, h, **kw)

# ----------------------------------------------------------------------------- Biscuit + cars
def _cat(k, x, y, s, eyes="shut"):
    """Biscuit curled like a loaf (x, y = bottom centre, s = body length): striped ginger as hatching."""
    body = k.arcpts(x, y, s * 0.5, s * 0.36, 0, 180, 24)
    k.shape(body, lw=1.1, fill=Wt, amp=0.1)
    for i in range(5):
        cx = x - s * 0.3 + i * s * 0.14; k.line([(cx, y + s * 0.05), (cx + s * 0.03, y + s * 0.3)], lw=0.9, amp=0.2)
    hx, hy, r = x + s * 0.42, y + s * 0.2, s * 0.2
    k.circle(hx, hy, r, lw=1.1, fill=Wt)
    for sg in (-1, 1): k.shape([(hx + sg * r * 0.85, hy + r * 0.35), (hx + sg * r * 0.85, hy + r * 1.25), (hx + sg * r * 0.25, hy + r * 0.85)], lw=0.9, fill=Wt, amp=0)
    for sg in (-1, 1):
        if eyes == "shut": k.shape(k.arcpts(hx + sg * r * 0.38, hy + r * 0.12, r * 0.2, r * 0.12, 180, 360, 8), lw=0.8, fill=None, amp=0)
        else: k.circle(hx + sg * r * 0.38, hy + r * 0.1, r * 0.1, lw=0, fill=K, stroke=False)
    k.shape([(hx - r * 0.1, hy - r * 0.15), (hx + r * 0.1, hy - r * 0.15), (hx, hy - r * 0.28)], lw=0.4, fill=K, amp=0)
    for sg in (-1, 1): k.line([(hx + sg * r * 0.2, hy - r * 0.25), (hx + sg * r * 1.2, hy - r * 0.15)], lw=0.4, amp=0)
    k.line([(x - s * 0.48, y + s * 0.04), (x - s * 0.6, y + s * 0.02), (x - s * 0.62, y + s * 0.14), (x - s * 0.5, y + s * 0.16)], lw=1.4, amp=0.2)
InkBW.cat = _cat

def _bluecar(k, x, y, w, bricks=False, dew=False):
    """Small blue car (hatched body) side-on, bonnet to the right. bricks=True: up on bricks with a flat tyre."""
    lift = w * 0.07 if bricks else 0
    if bricks:
        for wx in (-0.3, 0.3):
            for j in range(2): k.rect(x + wx * w - w * 0.07, y + j * lift / 2, w * 0.14, lift / 2, lw=0.8, fill=Wt)
    k.car(x, y + lift, w)
    hgt = w * 0.34; yy = y + lift
    body = [(x - w / 2, yy + hgt * 0.25), (x + w / 2, yy + hgt * 0.25), (x + w / 2, yy + hgt * 0.6), (x + w * 0.25, yy + hgt * 0.65), (x - w * 0.32, yy + hgt * 0.65), (x - w / 2, yy + hgt * 0.6)]
    k.hatch(body, angle=45, gap=2.6, lw=0.3)
    if bricks:   # flat front tyre: squashed black blob
        k.shape(k.arcpts(x + 0.3 * w, yy + hgt * 0.1, hgt * 0.26, hgt * 0.12, 0, 360, 16), lw=0.8, fill=K, amp=0)
    if dew:
        rr = random.Random(int(w))
        for _ in range(60):
            u, v = rr.random(), rr.random()
            px = x + w * (0.01 + 0.17 * u - 0.09 * v * u); py = yy + hgt * (0.7 + 0.22 * v)
            k.circle(px, py, 0.6 + rr.random() * 0.8, lw=0.3, fill=Wt)
    return (x + w * 0.37, yy + hgt * 0.63)   # bonnet top (cat spot)
InkBW.bluecar = _bluecar

def warm_fx(k, w, h, v):
    ph = {"s0": 0, "s1": 1.6, "s2": 3.1}[v]
    pts = [(w / 2 + 2.6 * math.sin(t * 7 + ph), 2 + t * (h - 4)) for t in [i / 16 for i in range(17)]]
    k.line(pts, lw=0.7, amp=0)
FX_WARM = dict(warm=dict(fn=warm_fx, variants=["s0", "s1", "s2"], page=(12, 26)))

def street(k, w, h, house=True):
    k.stones(14, w - 14, 14, 50, rows=2)
    k.line([(14, 50), (w - 14, 50)], lw=1.0, amp=0.1)
    if house:
        k.rect(30, 50, 190, 200, lw=1.2, fill=Wt); k.shape([(20, 250), (230, 250), (125, 320)], lw=1.2, fill=Wt, amp=0)
        k.rect(100, 50, 50, 100, lw=1.0, fill=Wt); k.circle(140, 100, 2.4, lw=0.5, fill=K)
        k.window_view(42, 170, 46, 52, view="street"); k.window_view(160, 170, 46, 52, view="street")
        k.text(125, 160, "No. 4", size=9, font="Ink-Plex")

# ----------------------------------------------------------------------------- 1. hook hero
def hook_plate(k, w, h):
    full_open(k, w, h); k.cloud(380, 330, 1.0); k.cloud(120, 320, 0.8)
    street(k, w, h); cx, cy = k.bluecar(360, 50, 220); k.cat(cx - 6, cy, 50); k.unclip()

# ----------------------------------------------------------------------------- 2. cast
CAST = [("MR FENWICK", fenwick), ("KERENSA HALE", kerensa), ("MR TRELOAR", treloar)]
cast_plate = B.cast_plate_fn([n for n, _ in CAST], style="cards")

# ----------------------------------------------------------------------------- 3. Biscuit's passion: warm bonnets
def biscuit_plate(k, w, h):
    plate_open(k, w, h); k.cloud(110, 320, 0.9); street(k, w, h, house=False)
    k.text(256, 330, "THE KETTLE AND GULL", size=10, font="Ink-Plex")
    k.unclip()
def car_part(k, w, h, v): part_open(k, w, h); k.bluecar(256, 50, 260); k.unclip()
def cat_part(k, w, h, v): part_open(k, w, h); k.cat(256 + 260 * 0.37 - 6, 50 + 260 * 0.34 * 0.63, 58); k.unclip()
def sardine_part(k, w, h, v):
    part_open(k, w, h); x, y = 120, 250
    k.shape(k.arcpts(x, y, 30, 9, 0, 360, 20), lw=0.9, fill=Wt, amp=0); k.shape([(x + 28, y), (x + 40, y + 9), (x + 40, y - 9)], lw=0.8, fill=Wt, amp=0)
    k.circle(x - 20, y + 2, 1.4, lw=0, fill=K, stroke=False); k.text(x, y + 18, "sardines", size=10, font="Ink-Kalam"); k.unclip()

# ----------------------------------------------------------------------------- 4. chilly grey morning, sharp wind
def chilly_plate(k, w, h):
    plate_open(k, w, h); k.harbour(w, h, sea_y0=120, sea_y1=200, wall_top=60, boats=True)
    for (cx, cy, sc) in ((100, 320, 1.0), (260, 300, 1.2), (420, 325, 0.9)): k.cloud(cx, cy, sc)
    k.unclip()
def wind_part(k, w, h, v):
    part_open(k, w, h)
    for j in range(4):
        y = 230 + j * 18; x0 = 80 + j * 30
        k.line([(x0 + i * 12, y + 4 * math.sin(i * 0.8)) for i in range(20)], lw=0.8, amp=0)
    k.unclip()

# ----------------------------------------------------------------------------- 5. Polwhele sailing club: trophy gone; blue car heading off
def club_plate(k, w, h):
    plate_open(k, w, h); k.floorboards(w, y=90)
    k.text(256, 334, "POLWHELE SAILING CLUB", size=12, font="Ink-Plex")
    k.rect(170, 90, 170, 200, lw=1.3, fill=Wt); k.rect(180, 100, 150, 180, lw=0.5, fill=None)
    for yy in (150, 220): k.rect(180, yy, 150, 4, lw=0.7, fill=Wt)
    k.window_view(380, 180, 90, 90); k.clock_face(90, 270, 26, 7, 0); k.text(90, 232, "7 o'clock", size=10, font="Ink-Kalam")
    k.unclip()
def _trophy(k, x, y, s):
    k.rect(x - s * 0.25, y, s * 0.5, s * 0.15, lw=0.9, fill=Wt); k.rect(x - s * 0.06, y + s * 0.15, s * 0.12, s * 0.25, lw=0.8, fill=Wt)
    k.shape(k.arcpts(x, y + s * 0.85, s * 0.35, s * 0.45, 180, 360, 18), lw=1.0, fill=Wt, amp=0)
    for sg in (-1, 1): k.c.setStrokeColor(K); k.c.setLineWidth(1.0); k.c.arc(x + sg * s * 0.35 - s * 0.12, y + s * 0.55, x + sg * s * 0.35 + s * 0.12, y + s * 0.8, 90 if sg > 0 else -90, 180)
InkBW.trophy = _trophy
def trophy_part(k, w, h, v): part_open(k, w, h); k.trophy(255, 154, 56); k.unclip()
def road_plate(k, w, h):
    plate_open(k, w, h); k.headland(14, w - 14, 120, 60); k.sea(14, w - 14, 60, 120, rows=3)
    k.line([(14, 60), (w - 14, 60)], lw=1.0, amp=0.1); k.stones(14, w - 14, 14, 60, rows=2)
    k.rect(400, 60, 6, 120, lw=0.8, fill=Wt); k.rect(330, 160, 150, 34, lw=1.1, fill=Wt); k.text(405, 172, "TIDEWHISTLE COVE \u2192", size=10, font="Ink-Plex")
    k.clock_face(80, 290, 24, 7, 15); k.text(80, 254, "7:15", size=10, font="Ink-Kalam")
    k.unclip()
def roadcar_part(k, w, h, v): part_open(k, w, h); k.bluecar(140, 60, 150); k.unclip()

# ----------------------------------------------------------------------------- 6. lineup: three small blue cars and their owners
def _p_bricks(k, pw, h): street(k, pw, h, house=False); k.text(380, 300, "GROCER'S", size=11, font="Ink-Plex"); k.bluecar(380, 50, 200, bricks=True)
def _p_dew(k, pw, h): street(k, pw, h, house=False); k.text(380, 300, "Kerensa's cottage", size=11, font="Ink-Kalam"); k.bluecar(380, 50, 200, dew=True)
def _p_tre(k, pw, h): street(k, pw, h, house=False); k.text(380, 300, "Mr Treloar's house", size=11, font="Ink-Kalam"); k.bluecar(380, 50, 200)
lineup_plate = B.lineup_plate_fn([_p_bricks, _p_dew, _p_tre], [n for n, _ in CAST])

# ----------------------------------------------------------------------------- 7. Agnes fetching the milk finds Biscuit on the third car
def tstreet_plate(k, w, h): plate_open(k, w, h); street(k, w, h, house=True); k.bluecar(360, 50, 220); k.unclip()
def cat_t(k, w, h, v): part_open(k, w, h); k.cat(360 + 220 * 0.37 - 6, 50 + 220 * 0.34 * 0.63, 50); k.unclip()
def agnes_milk(k, w, h, v): part_open(k, w, h); agnes(k, 250, 30, 190); k.rect(272, 112, 8, 18, lw=0.7, fill=Wt); k.unclip()
def purr_part(k, w, h, v): part_open(k, w, h); k.text(470, 160, "purr\u2026", size=11, font="Ink-Kalam"); k.unclip()

# ----------------------------------------------------------------------------- 8. Mr Treloar at the door in his dressing gown
def door_plate(k, w, h): plate_open(k, w, h); street(k, w, h, house=True); k.bluecar(390, 50, 200); k.cat(390 + 200 * 0.37 - 6, 50 + 200 * 0.34 * 0.63, 46); k.unclip()
def treloar_door(k, w, h, v): part_open(k, w, h); treloar_gown(k, 125, 50, 180, prop=B.newspaper); k.unclip()
def agnes_door(k, w, h, v): part_open(k, w, h); agnes(k, 250, 30, 180, flip=True); k.unclip()

# ----------------------------------------------------------------------------- 9. Agnes's hand on the bonnet: warm
def touch_plate(k, w, h):
    plate_open(k, w, h); street(k, w, h, house=False); cx, cy = k.bluecar(240, 50, 380); k.cat(cx - 52, cy, 66); k.unclip()
def hand_part(k, w, h, v):
    """Agnes's hand flat on the bonnet beside the cat; her sleeve comes in from the upper right."""
    part_open(k, w, h); x, y = 404, 50 + 380 * 0.34 * 0.63
    k.shape([(x - 26, y + 1), (x + 18, y + 1), (x + 30, y + 14), (x + 6, y + 16), (x - 24, y + 9)], lw=1.0, fill=Wt, amp=0.1)
    for j in range(3): k.line([(x - 22 + j * 2, y + 3 + j * 2), (x - 6, y + 3 + j * 2)], lw=0.4, amp=0)
    k.shape([(x + 18, y + 8), (x + 34, y + 18), (x + 120, y + 96), (x + 100, y + 112), (x + 14, y + 24)], lw=1.0, fill=Wt, amp=0.1)
    k.unclip()

# ----------------------------------------------------------------------------- 10. solution board
def board_plate(k, w, h):
    plate_open(k, w, h); k.floorboards(w)
    k.case_board(40, 110, 432, 250, title="THREE SMALL BLUE CARS")
    for i, (nm, note) in enumerate((("FENWICK", "up on bricks"), ("KERENSA", "dew untouched"), ("TRELOAR", "bonnet WARM"))):
        x = 56 + i * 140; k.rect(x, 140, 124, 180, lw=0.9, fill=Wt); k.text(x + 62, 300, nm, size=12, font="Ink-Plex")
        k.bluecar(x + 62, 200, 100, bricks=(i == 0), dew=(i == 1)); k.text(x + 62, 160, note, size=11, font="Ink-Kalam")
    k.unclip()
def boardcat(k, w, h, v): part_open(k, w, h); k.cat(56 + 280 + 62 + 100 * 0.37 - 4, 200 + 100 * 0.34 * 0.63, 26); k.unclip()
def x_part(k, w, h, v, i=0):
    part_open(k, w, h); x = 56 + i * 140; k.text(x + 62, 120, "didn't move", size=11, font="Ink-Kalam"); k.unclip()
def driven_part(k, w, h, v):
    part_open(k, w, h); x = 56 + 280; k.shape(k.arcpts(x + 62, 232, 70, 100, 0, 360, 36), lw=2.2, fill=None, amp=0.4)
    k.text(x + 62, 120, "driven at 7:15", size=11, font="Ink-Kalam"); k.unclip()

# ----------------------------------------------------------------------------- 11. confession; Biscuit back to sleep
def confess_plate(k, w, h): plate_open(k, w, h); street(k, w, h, house=True); cx, cy = k.bluecar(380, 50, 200); k.cat(cx - 6, cy, 46); k.unclip()
def treloar_conf(k, w, h, v):
    part_open(k, w, h); treloar(k, 250, 30, 200, expr="sheepish" if "sheepish" in v else "neutral", prop=_trophy_prop); k.unclip()
def _trophy_prop(k, hx, hyy, h): k.trophy(hx + h * 0.04, hyy - h * 0.06, h * 0.16)
def zzz_part(k, w, h, v): part_open(k, w, h); k.text(470, 170, "z z z", size=12, font="Ink-Kalam"); k.unclip()

def _vig(k, w, h):
    cx, cy = k.bluecar(w * 0.45, h * 0.2, w * 0.8); k.cat(cx - 10, cy, w * 0.2)
vignette = B.vignette_fn(_vig)

def jobs():
    J = []
    J.append(dict(name="hook", w=AW, h=AH, plate=hook_plate, seed=1501, parts=dict(**FX_WARM)))
    J.append(dict(name="cast", w=CW, h=CH, plate=cast_plate, seed=1502, parts={
        f"s{i}": dict(fn=B.cast_fig_fn(i, 3, fn), variants=V2) for i, (_, fn) in enumerate(CAST)}))
    J.append(dict(name="biscuit", w=AW, h=AH, plate=biscuit_plate, seed=1503, parts=dict(
        car=dict(fn=car_part, variants=["base"]), cat=dict(fn=cat_part, variants=["base"]), sardine=dict(fn=sardine_part, variants=["base"]), **FX_WARM)))
    J.append(dict(name="chilly", w=AW, h=AH, plate=chilly_plate, seed=1504, parts=dict(wind=dict(fn=wind_part, variants=["base"]), **B.FX_GULL)))
    J.append(dict(name="club", w=AW, h=AH, plate=club_plate, seed=1505, parts=dict(trophy=dict(fn=trophy_part, variants=["base"]))))
    J.append(dict(name="road", w=AW, h=AH, plate=road_plate, seed=1506, parts=dict(car=dict(fn=roadcar_part, variants=["base"]))))
    J.append(dict(name="lineup", w=3 * PW, h=AH, plate=lineup_plate, seed=1507, parts={
        f"s{i}": dict(fn=B.lineup_fig_fn(i, fn, x=PW / 2 - 120, y=50, fh=220), variants=V3) for i, (_, fn) in enumerate(CAST)}))
    J.append(dict(name="tstreet", w=AW, h=AH, plate=tstreet_plate, seed=1508, parts=dict(
        cat=dict(fn=cat_t, variants=["base"]), agnes=dict(fn=agnes_milk, variants=V2), purr=dict(fn=purr_part, variants=["base"]))))
    J.append(dict(name="door", w=AW, h=AH, plate=door_plate, seed=1509, parts=dict(
        treloar=dict(fn=treloar_door, variants=V3), agnes=dict(fn=agnes_door, variants=V2))))
    J.append(dict(name="touch", w=AW, h=AH, plate=touch_plate, seed=1510, parts=dict(hand=dict(fn=hand_part, variants=["base"]), **FX_WARM)))
    J.append(dict(name="board", w=AW, h=AH, plate=board_plate, seed=1511, parts=dict(
        cat=dict(fn=boardcat, variants=["base"]), x0=dict(fn=partial(x_part, i=0), variants=["base"]), x1=dict(fn=partial(x_part, i=1), variants=["base"]),
        driven=dict(fn=driven_part, variants=["base"]))))
    J.append(dict(name="confess", w=AW, h=AH, plate=confess_plate, seed=1512, parts=dict(
        treloar=dict(fn=treloar_conf, variants=["sheepish", "sheepish+blink"]), zzz=dict(fn=zzz_part, variants=["base"]))))
    J.append(dict(name="vignette", w=384, h=384, plate=vignette, seed=1513))
    return J

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    J = [j for j in jobs() if not want or j["name"] in want]
    save_layers(OUT, J, B.make_ink)
