"""Illustrations for Case 10, The Wet Paint Bench: BLACK-AND-WHITE ink (bwkit / colorink "bw") with the simple v1
peg-doll characters (figures.py + bwkit.visitor / overalls), drawn as animation layers (layers.save_layers -> anim.py).
PART sprites use part_open (clip only, never frame2), so no border rotates with a sprite.
Hook (render.py HOOK_STYLE="wetpaint"): borderless harbour hero — fresh-painted bench with its WET PAINT sign and the
empty lifeboat-station step (dashed outline where the box stood) — under a swinging hand-painted sign title.
Fairness: Hedley, Wenna and Mr Kemp share one stance, height, arms-down pose and neutral face in the cast strip and the
lineup; only the confession shows Mr Kemp sheepish.   Run: python3 art_case10.py [scene ...]"""
import math, os, sys
from functools import partial
import bwkit as B
from bwkit import plate_open, part_open, full_open, InkBW, nameplate, PW, AW, AH, V2, V3, CW, CH
import figures as F
from inkart import K, Wt
from layers import save_layers

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-10")

# ----------------------------------------------------------------------------- characters (same pose for suspects)
def hedley(k, x, y, h, **kw): B.overalls(k, x, y, h, paint=True, **kw)
def wenna(k, x, y, h, **kw): kw.setdefault("prop", False); F.wenna(k, x, y, h, **kw)
def kemp(k, x, y, h, **kw): B.visitor(k, x, y, h, suit="plain", hat="panama", tie=True, **kw)
def ollie(k, x, y, h, **kw): F.ollie(k, x, y, h, **kw)
def agnes(k, x, y, h, **kw): kw.setdefault("teapot", False); F.agnes(k, x, y, h, **kw)

STATION_X = 330   # lifeboat station (x, width) used in several scenes
def seafront(k, w, h, benches=((120, 92),), station=True, signs=True, box=None):
    """Harbour wall promenade: sea + headland behind, stone wall, painted benches, the lifeboat station at right."""
    k.harbour(w, h, sea_y0=150, sea_y1=214, wall_top=70, boats=True)
    k.line([(14, 70), (w - 14, 70)], lw=1.2, amp=0.1)
    if station:
        k.lifeboat_station(STATION_X, 86, 150, 190, steps=True)
    for (bx, bw) in benches: k.wet_bench(bx, 72, bw, sign=signs)

# ----------------------------------------------------------------------------- 1. hook hero (full bleed, no border)
def hook_plate(k, w, h):
    full_open(k, w, h)
    k.sun(70, 330, 16); k.cloud(200, 340, 0.9)
    seafront(k, w, h, benches=((150, 110),), station=True)
    k.dashed_outline(STATION_X + 75, 86, 26, 30)   # where the box stood
    k.text(STATION_X + 75, 122, "?", size=22, font="Ink-Playfair")
    k.unclip()

# ----------------------------------------------------------------------------- 2. cast strip (luggage tags)
CAST = [("HEDLEY TRUSCOTT", hedley), ("WENNA POLGLAZE", wenna), ("MR KEMP", kemp)]
cast_plate = B.cast_plate_fn([n for n, _ in CAST], style="tags")

# ----------------------------------------------------------------------------- 3. harbour: Hedley painting the benches
def harbour_plate(k, w, h):
    plate_open(k, w, h); k.sun(450, 330, 15)
    seafront(k, w, h, benches=((90, 80), (230, 80)), station=True, signs=False)
    k.paint_tin(160, 72, 20)
    k.unclip()

def _tin(k, x, y, w, label=True):
    k.rect(x - w / 2, y, w, w * 0.9, lw=0.9, fill=Wt)
    k.shape(k.arcpts(x, y + w * 0.9, w / 2, w * 0.12, 0, 360, 18), lw=0.8, fill=K, amp=0)
    k.c.setStrokeColor(K); k.c.setLineWidth(0.7); k.c.arc(x - w * 0.45, y + w * 0.7, x + w * 0.45, y + w * 1.5, 0, 180)
    if label:
        k.rect(x - w * 0.38, y + w * 0.25, w * 0.76, w * 0.34, lw=0.5, fill=Wt)
        k.text(x, y + w * 0.32, "6 HRS", size=w * 0.16, font="Ink-Plex")
InkBW.paint_tin = _tin

def sign_part(k, w, h, v, x=90, bw=80):
    part_open(k, w, h)
    px = x + bw * 0.2
    k.line([(px, 72 + bw * 0.3), (px, 72 + bw * 0.62)], lw=1.0, amp=0)
    k.rect(px - bw * 0.17, 72 + bw * 0.6, bw * 0.34, bw * 0.16, lw=0.9, fill=Wt)
    k.text(px, 72 + bw * 0.66, "WET PAINT", size=bw * 0.07, font="Ink-Plex")
    k.unclip()

def hedley_paint(k, w, h, v): part_open(k, w, h); hedley(k, 330 - 170, 40, 210, prop=B.paintbrush); k.unclip()

# ----------------------------------------------------------------------------- 4. "Six hours, it says on the tin"
def tin_plate(k, w, h):
    plate_open(k, w, h)
    seafront(k, w, h, benches=((256, 120),), station=False, signs=True)
    k.paint_tin(330, 60, 30)
    k.unclip()

def hedley_tin(k, w, h, v): part_open(k, w, h); hedley(k, 120, 30, 230); k.unclip()
def agnes_tin(k, w, h, v): part_open(k, w, h); agnes(k, 420, 30, 220, flip=True); k.unclip()

# ----------------------------------------------------------------------------- 5. lifeboat station steps + collection box
def station_plate(k, w, h):
    plate_open(k, w, h); k.cloud(110, 330, 1.0)
    k.harbour(w, h, sea_y0=150, sea_y1=214, wall_top=70)
    k.lifeboat_station(250, 86, 200, 230, steps=True)
    k.wet_bench(70, 72, 80, sign=True)
    k.unclip()

def box_part(k, w, h, v): part_open(k, w, h); k.collection_box(350, 86, 34); k.unclip()

# ----------------------------------------------------------------------------- 6. Agnes + Ollie asking around
def quay_plate(k, w, h):
    plate_open(k, w, h)
    seafront(k, w, h, benches=((420, 80),), station=False, signs=True)
    k.crate(60, 72, 30); k.crate(78, 93, 24)
    k.unclip()

def agnes_quay(k, w, h, v): part_open(k, w, h); agnes(k, 170, 40, 220); k.unclip()
def ollie_quay(k, w, h, v): part_open(k, w, h); ollie(k, 300, 40, 230, flip=True); k.unclip()

# ----------------------------------------------------------------------------- 7. lineup: three equal panels
def _slipway(k, pw, h):
    k.harbour(pw, h, sea_y0=140, sea_y1=200, wall_top=60, boats=False)
    k.slipway(250, 480, 14, 120)
    for (x, y) in ((400, 70), (430, 70), (415, 91)): k.crate(x, y, 28)
def _tearoom(k, pw, h):
    k.tearoom(pw, h, counter=False)
    k.table_cloth(330, 14, 90, 48); k.teapot(320, 62, 26); k.cup(352, 62, 12)
def _bench(k, pw, h):
    k.harbour(pw, h, sea_y0=150, sea_y1=214, wall_top=70, boats=True)
    k.wet_bench(350, 72, 110, sign=True)
lineup_plate = B.lineup_plate_fn([_slipway, _tearoom, _bench], [n for n, _ in CAST])

def ollie_line(k, w, h, v):
    k.clip_rect(14, 14, PW - 14, h - 14); ollie(k, 380, 120, 180); k.unclip()

def agnes_line(k, w, h, v):
    k.c.saveState(); k.c.translate(PW, 0); k.clip_rect(14, 14, PW - 14, h - 14); F.agnes(k, 420, 70, 200, teapot=True, flip=True); k.unclip(); k.c.restoreState()

# ----------------------------------------------------------------------------- 8. Mr Kemp's statement
def kemp_plate(k, w, h):
    plate_open(k, w, h)
    seafront(k, w, h, benches=((250, 110),), station=False, signs=True)
    k.lifeboat_station(400, 86, 120, 170, steps=True)
    k.unclip()

def kemp_talk(k, w, h, v): part_open(k, w, h); kemp(k, 120, 30, 230); k.unclip()
def agnes_listen(k, w, h, v): part_open(k, w, h); agnes(k, 330, 30, 210, flip=True); k.unclip()

# ----------------------------------------------------------------------------- 9. the shining wet bench vs. the spotless trousers
def bench_plate(k, w, h):
    plate_open(k, w, h); k.sun(80, 330, 18)
    k.harbour(w, h, sea_y0=170, sea_y1=230, wall_top=60, boats=True)
    k.wet_bench(170, 62, 220, sign=True)
    k.unclip()

def kemp_still(k, w, h, v): part_open(k, w, h); kemp(k, 400, 30, 250); k.unclip()

def sparkle_fx(k, w, h, v):
    r = w * (0.45 if v == "s0" else 0.32); x, y = w / 2, h / 2
    k.shape([(x - r, y), (x - r * 0.18, y + r * 0.18), (x, y + r), (x + r * 0.18, y + r * 0.18), (x + r, y), (x + r * 0.18, y - r * 0.18), (x, y - r), (x - r * 0.18, y - r * 0.18)], lw=0.5, fill=Wt, amp=0)

# ----------------------------------------------------------------------------- 10. solution: Agnes's case board
def board_plate(k, w, h):
    plate_open(k, w, h)
    k.floorboards(w)
    k.case_board(40, 110, 432, 250)
    k.pin_card(56, 250, 120, 70, ["BENCH PAINTED", "2:30"], size=11, rot=-3)
    k.pin_card(56, 160, 120, 70, ["TACKY UNTIL", "8 O'CLOCK"], size=11, rot=2)
    k.pin_card(196, 230, 120, 90, ["MR KEMP:", "\u201csat there", "3 till 4\u201d"], size=11, rot=-1)
    # Kemp's trousers card: clean cream trousers drawn in ink
    k.rect(340, 150, 116, 170, lw=0.8, fill=Wt); k.circle(398, 317, 2.6, lw=0.5, fill=K)
    tr = [(372, 300), (424, 300), (432, 172), (404, 172), (398, 250), (392, 172), (364, 172)]
    k.shape(tr, lw=1.0, fill=Wt, amp=0)
    k.text(398, 156, "spotless", size=11, font="Ink-Kalam")
    k.unclip()

def stripes_part(k, w, h, v):
    """What sitting for an hour would have left: paint stripes across the seat of the trousers."""
    part_open(k, w, h)
    for j in range(3):
        y = 262 - j * 14
        k.shape([(368, y), (428, y), (428, y - 6), (368, y - 6)], lw=0.5, fill=K, amp=0.2)
    k.text(398, 330, "if he'd sat there\u2026", size=10, font="Ink-Kalam")
    k.unclip()

def x_part(k, w, h, v):
    part_open(k, w, h)
    k.line([(192, 236), (318, 322)], lw=2.6, amp=0.4); k.line([(192, 322), (318, 236)], lw=2.6, amp=0.4)
    k.text(256, 205, "never sat there", size=13, font="Ink-Kalam")
    k.unclip()

def tick_part(k, w, h, v, x=0, y=0, label=""):
    part_open(k, w, h)
    k.line([(x, y), (x + 8, y - 9), (x + 24, y + 12)], lw=2.2, amp=0.2)
    k.text(x + 60, y - 6, label, size=11, font="Ink-Kalam")
    k.unclip()

# ----------------------------------------------------------------------------- 11. the box found in the car boot
def confess_plate(k, w, h):
    plate_open(k, w, h)
    k.harbour(w, h, sea_y0=170, sea_y1=230, wall_top=60, boats=True)
    k.car(250, 62, 230, boot_open=True)
    k.collection_box(150, 105, 34)
    k.unclip()

def kemp_conf(k, w, h, v): part_open(k, w, h); kemp(k, 410, 30, 220, expr="sheepish" if "sheepish" in v else "neutral"); k.unclip()
def ollie_conf(k, w, h, v): part_open(k, w, h); ollie(k, 70, 30, 220); k.unclip()
def note_part(k, w, h, v): part_open(k, w, h); k.banknote(160, 150, 26); k.unclip()

# ----------------------------------------------------------------------------- vignette (title card)
def _vig(k, w, h):
    k.sea(0, w, h * 0.42, h * 0.6, rows=4); k.lighthouse(w * 0.2, h * 0.6, 60)
    k.stones(0, w, 0, h * 0.3, rows=3)
    k.wet_bench(w * 0.6, h * 0.3, 160, sign=True)
vignette = B.vignette_fn(_vig)

# ============================================================================= jobs
def jobs():
    FX = B.FX_GULL; SP = dict(sparkle=dict(fn=sparkle_fx, variants=["s0", "s1"], page=(14, 14)))
    J = []
    J.append(dict(name="hook", w=AW, h=AH, plate=hook_plate, seed=1001, parts=dict(**FX)))
    J.append(dict(name="cast", w=CW, h=CH, plate=cast_plate, seed=1002, parts={
        f"s{i}": dict(fn=B.cast_fig_fn(i, 3, fn), variants=V2) for i, (_, fn) in enumerate(CAST)}))
    J.append(dict(name="harbour", w=AW, h=AH, plate=harbour_plate, seed=1003, parts=dict(
        hedley=dict(fn=hedley_paint, variants=V2),
        sign1=dict(fn=partial(sign_part, x=90, bw=80), variants=["base"]),
        sign2=dict(fn=partial(sign_part, x=230, bw=80), variants=["base"]), **FX)))
    J.append(dict(name="tin", w=AW, h=AH, plate=tin_plate, seed=1004, parts=dict(
        hedley=dict(fn=hedley_tin, variants=V3), agnes=dict(fn=agnes_tin, variants=V2))))
    J.append(dict(name="station", w=AW, h=AH, plate=station_plate, seed=1005, parts=dict(
        box=dict(fn=box_part, variants=["base"]), **FX)))
    J.append(dict(name="quay", w=AW, h=AH, plate=quay_plate, seed=1006, parts=dict(
        agnes=dict(fn=agnes_quay, variants=V3), ollie=dict(fn=ollie_quay, variants=V3), **FX)))
    J.append(dict(name="lineup", w=3 * PW, h=AH, plate=lineup_plate, seed=1007, parts={
        **{f"s{i}": dict(fn=B.lineup_fig_fn(i, fn), variants=V3) for i, (_, fn) in enumerate(CAST)},
        "ollie": dict(fn=ollie_line, variants=V2), "agnes": dict(fn=agnes_line, variants=V2)}))
    J.append(dict(name="kemp", w=AW, h=AH, plate=kemp_plate, seed=1008, parts=dict(
        kemp=dict(fn=kemp_talk, variants=V3), agnes=dict(fn=agnes_listen, variants=V2))))
    J.append(dict(name="bench", w=AW, h=AH, plate=bench_plate, seed=1009, parts=dict(
        kemp=dict(fn=kemp_still, variants=V2), **SP)))
    J.append(dict(name="board", w=AW, h=AH, plate=board_plate, seed=1010, parts=dict(
        stripes=dict(fn=stripes_part, variants=["base"]), x=dict(fn=x_part, variants=["base"]))))
    J.append(dict(name="confess", w=AW, h=AH, plate=confess_plate, seed=1011, parts=dict(
        kemp=dict(fn=kemp_conf, variants=["sheepish", "sheepish+blink"]), ollie=dict(fn=ollie_conf, variants=V2),
        note=dict(fn=note_part, variants=["base"]))))
    J.append(dict(name="vignette", w=384, h=384, plate=vignette, seed=1012))
    return J

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    J = [j for j in jobs() if not want or j["name"] in want]
    save_layers(OUT, J, B.make_ink)
