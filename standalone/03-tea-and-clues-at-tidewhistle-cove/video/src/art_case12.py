"""Illustrations for Case 12, The Stopped Clock: BLACK-AND-WHITE ink (bwkit) with the simple v1 peg-doll characters.
The Kettle and Gull's old wall clock has stood at TEN TO NINE all week; the silver acorn caddy vanishes on Thursday.
PART sprites use part_open (clip only, never frame2).
Hook (render.py HOOK_STYLE="calendar"): borderless hero of the stopped clock above the caddy shelf with the empty spot.
Fairness: Demelza, Hedley and Mr Prowse share one stance, height, arms-down pose and neutral face in the cast strip
and the lineup; only the confession shows Mr Prowse sheepish.   Run: python3 art_case12.py [scene ...]"""
import os, sys, math
from functools import partial
import bwkit as B
from bwkit import plate_open, part_open, full_open, InkBW, nameplate, PW, AW, AH, V2, V3, CW, CH
import figures as F
from inkart import K, Wt
from layers import save_layers

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-12")

# ----------------------------------------------------------------------------- characters
def demelza(k, x, y, h, **kw): kw.setdefault("prop", False); F.demelza(k, x, y, h, **kw)
def hedley(k, x, y, h, **kw): B.overalls(k, x, y, h, paint=False, **kw)
def prowse(k, x, y, h, **kw): B.visitor(k, x, y, h, suit="stripe", hat="cap", tie=False, **kw)
def quill(k, x, y, h, **kw): kw.setdefault("prop", False); F.quill(k, x, y, h, **kw)
def agnes(k, x, y, h, **kw): kw.setdefault("teapot", False); F.agnes(k, x, y, h, **kw)
def guest1(k, x, y, h, **kw): B.lady(k, x, y, h, dress="dots", hair="bun", **kw)
def guest2(k, x, y, h, **kw): B.visitor(k, x, y, h, suit="plain", hat=None, tie=True, moustache=True, **kw)

# ----------------------------------------------------------------------------- props
def _wall_clock(k, x, y, r, hh=8, mm=50, pendulum=True):
    """Old wall clock: carved wooden case, round dial, pendulum box below (x, y = dial centre)."""
    k.rect(x - r * 1.25, y - r * 2.6, r * 2.5, r * 3.9, lw=1.3, fill=Wt)
    k.hatch([(x - r * 1.25, y - r * 2.6), (x + r * 1.25, y - r * 2.6), (x + r * 1.25, y + r * 1.3), (x - r * 1.25, y + r * 1.3)], angle=90, gap=2.4, lw=0.25)
    k.shape(k.arcpts(x, y + r * 1.3, r * 1.25, r * 0.5, 0, 180, 16), lw=1.1, fill=Wt, amp=0)
    k.circle(x, y + r * 1.55, r * 0.12, lw=0.6, fill=K)
    k.clock_face(x, y, r, hh, mm)
    if pendulum:
        k.rect(x - r * 0.6, y - r * 2.4, r * 1.2, r * 1.15, lw=0.8, fill=Wt)
        k.line([(x, y - r * 1.3), (x, y - r * 2.0)], lw=0.7, amp=0); k.circle(x, y - r * 2.08, r * 0.17, lw=0.6, fill=K)
InkBW.wall_clock = _wall_clock

def _acorn(k, x, y, s):
    """Little silver acorn-shaped tea caddy (x, y = base centre)."""
    k.shape(k.arcpts(x, y + s * 0.55, s * 0.42, s * 0.55, 180, 360, 18) + [(x + s * 0.42, y + s * 0.62), (x - s * 0.42, y + s * 0.62)], lw=0.9, fill=Wt, amp=0)
    k.line([(x - s * 0.15, y + s * 0.2), (x - s * 0.22, y + s * 0.45)], lw=0.35, amp=0)
    cap = k.arcpts(x, y + s * 0.6, s * 0.5, s * 0.36, 0, 180, 16)
    k.shape(cap, lw=0.9, fill=Wt, amp=0); k.hatch(cap, angle=45, gap=1.6, lw=0.3, cross=True)
    k.line([(x, y + s * 0.95), (x + s * 0.06, y + s * 1.12)], lw=1.0, amp=0)
InkBW.acorn = _acorn

def _caddy(k, x, y, w, hgt, pattern=0):
    k.rect(x - w / 2, y, w, hgt, lw=0.9, fill=Wt); k.rect(x - w / 2 - 2, y + hgt, w + 4, hgt * 0.18, lw=0.8, fill=Wt)
    if pattern == 1: k.hatch([(x - w / 2, y), (x + w / 2, y), (x + w / 2, y + hgt), (x - w / 2, y + hgt)], angle=90, gap=2.6, lw=0.3)
    elif pattern == 2: k.rect(x - w * 0.3, y + hgt * 0.25, w * 0.6, hgt * 0.45, lw=0.5, fill=None)
    elif pattern == 3: k.circle(x, y + hgt * 0.5, w * 0.22, lw=0.5, fill=None)
InkBW.caddy = _caddy

SHELF_Y = 214; ACORN_X = 300
def caddy_shelf(k, x0, x1, y=SHELF_Y, acorn=False, outline=False):
    k.rect(x0, y - 6, x1 - x0, 6, lw=1.0, fill=Wt)
    for (cx, w, hh, p) in ((x0 + 26, 26, 32, 1), (x0 + 64, 22, 26, 2), (x0 + 100, 30, 36, 3), (x1 - 92, 24, 30, 2), (x1 - 56, 28, 34, 1), (x1 - 22, 20, 24, 3)):
        k.caddy(cx, y, w, hh, p)
    if acorn: k.acorn(ACORN_X, y, 34)
    if outline: k.dashed_outline(ACORN_X, y, 30, 34)

def tearoom_wall(k, w, h, clock=True, shelf=True, acorn=False, outline=False, counter=True):
    k.floorboards(w, y=80)
    k.rect(14, 80, w - 28, 30, lw=0.8, fill=Wt)
    for i in range(int((w - 28) / 32)): k.rect(20 + i * 32, 84, 24, 22, lw=0.35, fill=None)
    if clock: k.wall_clock(110, 262, 40)
    if shelf: caddy_shelf(k, 190, 480, acorn=acorn, outline=outline)
    if counter:
        k.rect(196, 14, 280, 92, lw=1.0, fill=Wt); k.hatch([(196, 14), (476, 14), (476, 106), (196, 106)], angle=0, gap=2.8, lw=0.3)
        k.rect(190, 106, 292, 8, lw=1.0, fill=Wt); k.teapot(440, 114, 30)

# ----------------------------------------------------------------------------- 1. hook hero (full bleed, no border)
def hook_plate(k, w, h):
    full_open(k, w, h); tearoom_wall(k, w, h, outline=True)
    k.text(ACORN_X, SHELF_Y + 42, "?", size=20, font="Ink-Playfair"); k.unclip()

# ----------------------------------------------------------------------------- 2. cast strip
CAST = [("DEMELZA ROWE", demelza), ("HEDLEY TRUSCOTT", hedley), ("MR PROWSE", prowse)]
cast_plate = B.cast_plate_fn([n for n, _ in CAST], style="cards")

# ----------------------------------------------------------------------------- 3. the clock stops (Monday), clockmaker Friday
def clock_plate(k, w, h):
    plate_open(k, w, h); tearoom_wall(k, w, h, shelf=False, counter=False)
    k.text(110, 352, "THE KETTLE AND GULL", size=10, font="Ink-Plex")
    # week strip
    for i, dname in enumerate(("MON", "TUE", "WED", "THU", "FRI")):
        x = 230 + i * 50; k.rect(x, 220, 44, 52, lw=0.9, fill=Wt); k.rect(x, 258, 44, 14, lw=0.9, fill=K)
        k.text(x + 22, 261, dname, size=9, font="Ink-Plex", color=Wt); k.text(x + 22, 230, "8:50", size=11, font="Ink-Kalam")
    k.unclip()
def click_part(k, w, h, v):
    part_open(k, w, h)
    for a in (30, 60, 120, 150): k.line([(110 + 52 * math.cos(math.radians(a)), 262 + 52 * math.sin(math.radians(a))), (110 + 64 * math.cos(math.radians(a)), 262 + 64 * math.sin(math.radians(a)))], lw=1.1, amp=0)
    k.text(110, 336, "click.", size=12, font="Ink-Kalam"); k.unclip()
def friday_part(k, w, h, v):
    part_open(k, w, h); x = 230 + 4 * 50
    k.shape(k.arcpts(x + 22, 246, 30, 34, 0, 360, 30), lw=1.6, fill=None, amp=0.4)
    k.text(x - 10, 186, "clockmaker", size=11, font="Ink-Kalam"); k.unclip()

# ----------------------------------------------------------------------------- 4. "tell the time by your stomachs"
def laugh_plate(k, w, h): plate_open(k, w, h); tearoom_wall(k, w, h, shelf=False, counter=False); k.table_cloth(330, 30, 80, 42); k.cup(320, 72, 11); k.cup(345, 72, 11); k.unclip()
def agnes_laugh(k, w, h, v): part_open(k, w, h); agnes(k, 200, 30, 210, teapot=True); k.unclip()
def g1_part(k, w, h, v): part_open(k, w, h); guest1(k, 290, 30, 190, expr="smile" if "smile" in v else "neutral", flip=True); k.unclip()
def g2_part(k, w, h, v): part_open(k, w, h); guest2(k, 410, 30, 200, expr="smile" if "smile" in v else "neutral", flip=True); k.unclip()

# ----------------------------------------------------------------------------- 5. the caddy shelf: dusted 3:30, gone 4:30
def shelf_plate(k, w, h): plate_open(k, w, h); tearoom_wall(k, w, h, clock=True, acorn=False); k.unclip()
def acorn_part(k, w, h, v): part_open(k, w, h); k.acorn(ACORN_X, SHELF_Y, 34); k.unclip()
def time_tag(k, w, h, v, x=0, label=""):
    part_open(k, w, h); k.pin_card(x, 268, 92, 50, label, size=12, rot=-3 if x < 300 else 3); k.unclip()
def gone_part(k, w, h, v): part_open(k, w, h); k.dashed_outline(ACORN_X, SHELF_Y, 30, 34); k.text(ACORN_X, SHELF_Y + 42, "?", size=18, font="Ink-Playfair"); k.unclip()

# ----------------------------------------------------------------------------- 6. lineup: Demelza (sea front) / Hedley (armchair) / Mr Prowse (back door)
def _seafront(k, pw, h):
    k.harbour(pw, h, sea_y0=150, sea_y1=214, wall_top=70, boats=True)
def _armchair(k, pw, h):
    k.floorboards(pw, y=96); k.rect(14, 96, pw - 28, 200, lw=0, fill=None)
    k.window_view(60, 200, 110, 100)
    x = 380; k.rect(x - 60, 40, 120, 70, lw=1.1, fill=Wt); k.rect(x - 56, 110, 112, 90, lw=1.1, fill=Wt)
    k.hatch([(x - 56, 110), (x + 56, 110), (x + 56, 200), (x - 56, 200)], angle=45, gap=3, lw=0.3, cross=True)
    for sg in (-1, 1): k.rect(x + sg * 66 - 12, 40, 24, 100, lw=1.0, fill=Wt)
    k.clock_face(440, 300, 22, 3, 20); k.text(440, 266, "3:20 \u2192 supper", size=9, font="Ink-Kalam")
def _backdoor(k, pw, h):
    k.stones(14, pw - 14, 14, 60, rows=3)
    k.rect(300, 60, 120, 230, lw=1.3, fill=Wt); k.rect(312, 72, 96, 90, lw=0.6, fill=None); k.rect(312, 176, 96, 100, lw=0.6, fill=None)
    k.circle(398, 170, 3, lw=0.6, fill=K); k.text(360, 300, "BACK DOOR", size=10, font="Ink-Plex")
    k.crate(410, 60, 40)
    for i in range(4): k.rect(416 + i * 8, 100, 6, 18, lw=0.6, fill=Wt)
lineup_plate = B.lineup_plate_fn([_seafront, _armchair, _backdoor], [n for n, _ in CAST])
def quill_line(k, w, h, v): k.clip_rect(14, 14, PW - 14, h - 14); quill(k, 390, 120, 170, flip=True); k.unclip()

# ----------------------------------------------------------------------------- 7. Mr Prowse's statement: "your clock said a quarter past three"
def prowse_plate(k, w, h):
    plate_open(k, w, h); k.stones(14, w - 14, 14, 60, rows=3)
    k.rect(330, 60, 130, 240, lw=1.3, fill=Wt); k.rect(342, 72, 106, 96, lw=0.6, fill=None); k.rect(342, 182, 106, 104, lw=0.6, fill=None)
    k.crate(390, 60, 46)
    for i in range(5): k.rect(396 + i * 8, 106, 6, 20, lw=0.6, fill=Wt)
    k.unclip()
def prowse_talk(k, w, h, v): part_open(k, w, h); prowse(k, 170, 30, 230); k.unclip()
def bubble_part(k, w, h, v):
    part_open(k, w, h); cx, cy = 300, 290
    k.shape(k.arcpts(cx, cy, 70, 52, 0, 360, 36), lw=1.1, fill=Wt, amp=0.4)
    for (bx, by, r) in ((228, 228, 9), (212, 210, 6)): k.circle(bx, by, r, lw=0.9, fill=Wt)
    k.clock_face(cx, cy + 4, 36, 3, 15); k.text(cx, cy - 46, "\u201ca quarter past three\u201d", size=10, font="Ink-Kalam")
    k.unclip()

# ----------------------------------------------------------------------------- 8. Agnes looks up: ten to nine, as all week
def look_plate(k, w, h): plate_open(k, w, h); tearoom_wall(k, w, h, shelf=True, outline=True); k.unclip()
def agnes_look(k, w, h, v): part_open(k, w, h); agnes(k, 205, 30, 236); k.unclip()

# ----------------------------------------------------------------------------- 9. solution board
def board_plate(k, w, h):
    plate_open(k, w, h); k.floorboards(w)
    k.case_board(40, 110, 432, 250)
    k.pin_card(60, 236, 130, 90, ["MR PROWSE:", "\u201cyour clock said", "a quarter past 3\u201d"], size=11, rot=-2)
    k.rect(214, 150, 110, 170, lw=0.8, fill=Wt); k.clock_face(269, 252, 44, 8, 50); k.text(269, 168, "stopped Monday", size=10, font="Ink-Kalam")
    k.pin_card(346, 236, 110, 80, ["CADDY", "3:30 there", "4:30 gone"], size=11, rot=3)
    k.unclip()
def bubble_small(k, w, h, v):
    part_open(k, w, h); k.circle(125, 196, 30, lw=1.0, fill=Wt); k.clock_face(125, 196, 26, 3, 15); k.unclip()
def x_part(k, w, h, v):
    part_open(k, w, h); k.line([(88, 160), (162, 232)], lw=2.6, amp=0.4); k.line([(88, 232), (162, 160)], lw=2.6, amp=0.4)
    k.text(125, 140, "impossible", size=12, font="Ink-Kalam"); k.unclip()
def made_part(k, w, h, v):
    part_open(k, w, h); k.pin_card(330, 140, 132, 60, ["made up the time", "to sound early"], size=11, rot=-3); k.unclip()

# ----------------------------------------------------------------------------- 10. confession; the caddy moves to a higher shelf
def confess_plate(k, w, h): plate_open(k, w, h); tearoom_wall(k, w, h, shelf=True, outline=False); k.unclip()
def prowse_conf(k, w, h, v): part_open(k, w, h); prowse(k, 160, 30, 220, expr="sheepish" if "sheepish" in v else "neutral", prop=_acorn_prop); k.unclip()
def _acorn_prop(k, hx, hyy, h): k.acorn(hx + h * 0.03, hyy - h * 0.04, h * 0.1)
def agnes_conf(k, w, h, v): part_open(k, w, h); agnes(k, 360, 30, 200, flip=True); k.unclip()
def high_part(k, w, h, v):
    part_open(k, w, h); k.rect(270, 318, 120, 6, lw=1.0, fill=Wt); k.acorn(330, 324, 30)
    k.text(330, 300, "higher shelf", size=10, font="Ink-Kalam"); k.unclip()

# ----------------------------------------------------------------------------- vignette (title card)
def _vig(k, w, h):
    k.wall_clock(w * 0.42, h * 0.62, 50, pendulum=False); k.acorn(w * 0.72, h * 0.2, 60)
    k.rect(w * 0.55, h * 0.2 - 6, w * 0.4, 6, lw=1.0, fill=Wt)
vignette = B.vignette_fn(_vig)

# ============================================================================= jobs
def jobs():
    FX = B.FX_GULL; J = []
    J.append(dict(name="hook", w=AW, h=AH, plate=hook_plate, seed=1201))
    J.append(dict(name="cast", w=CW, h=CH, plate=cast_plate, seed=1202, parts={
        f"s{i}": dict(fn=B.cast_fig_fn(i, 3, fn), variants=V2) for i, (_, fn) in enumerate(CAST)}))
    J.append(dict(name="clock", w=AW, h=AH, plate=clock_plate, seed=1203, parts=dict(
        click=dict(fn=click_part, variants=["base"]), friday=dict(fn=friday_part, variants=["base"]))))
    J.append(dict(name="laugh", w=AW, h=AH, plate=laugh_plate, seed=1204, parts=dict(
        agnes=dict(fn=agnes_laugh, variants=V3), g1=dict(fn=g1_part, variants=["base", "base+blink", "smile", "smile+blink"]),
        g2=dict(fn=g2_part, variants=["base", "base+blink", "smile", "smile+blink"]))))
    J.append(dict(name="shelf", w=AW, h=AH, plate=shelf_plate, seed=1205, parts=dict(
        acorn=dict(fn=acorn_part, variants=["base"]),
        t1=dict(fn=partial(time_tag, x=200, label=["3:30", "dusted"]), variants=["base"]),
        t2=dict(fn=partial(time_tag, x=360, label=["4:30", "gone!"]), variants=["base"]),
        gone=dict(fn=gone_part, variants=["base"]))))
    J.append(dict(name="lineup", w=3 * PW, h=AH, plate=lineup_plate, seed=1206, parts={
        **{f"s{i}": dict(fn=B.lineup_fig_fn(i, fn), variants=V3) for i, (_, fn) in enumerate(CAST)},
        "quill": dict(fn=quill_line, variants=V2), **FX}))
    J.append(dict(name="prowse", w=AW, h=AH, plate=prowse_plate, seed=1207, parts=dict(
        prowse=dict(fn=prowse_talk, variants=V3), bubble=dict(fn=bubble_part, variants=["base"]))))
    J.append(dict(name="look", w=AW, h=AH, plate=look_plate, seed=1208, parts=dict(agnes=dict(fn=agnes_look, variants=V2))))
    J.append(dict(name="board", w=AW, h=AH, plate=board_plate, seed=1209, parts=dict(
        bub=dict(fn=bubble_small, variants=["base"]), x=dict(fn=x_part, variants=["base"]), made=dict(fn=made_part, variants=["base"]))))
    J.append(dict(name="confess", w=AW, h=AH, plate=confess_plate, seed=1210, parts=dict(
        prowse=dict(fn=prowse_conf, variants=["sheepish", "sheepish+blink"]), agnes=dict(fn=agnes_conf, variants=V2),
        high=dict(fn=high_part, variants=["base"]))))
    J.append(dict(name="vignette", w=384, h=384, plate=vignette, seed=1211))
    return J

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    J = [j for j in jobs() if not want or j["name"] in want]
    save_layers(OUT, J, B.make_ink)
