"""Illustrations for Case 16, The Lighthouse Path: BLACK-AND-WHITE ink (bwkit) with the simple v1 peg-doll characters.
The lighthouse museum, the lamp room and its brass telescope (hatched), a village path map and a timeline board.
PART sprites use part_open (clip only, never frame2).
Hook (render.py HOOK_STYLE="stopwatch"): borderless hero of the lighthouse on the point.
Fairness: Wenna, Mr Opie and Pip share one stance, height, arms-down pose and neutral face in the cast strip and the lineup;
each gets two sighting tags in the same style; only the confession shows Mr Opie sheepish.
Run: python3 art_case16.py [scene ...]"""
import os, sys, math
from functools import partial
import bwkit as B
from bwkit import plate_open, part_open, full_open, InkBW, PW, AW, AH, V2, V3, CW, CH
import figures as F
from inkart import K, Wt
from layers import save_layers

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-16")

def wenna(k, x, y, h, **kw): kw.setdefault("prop", False); F.wenna(k, x, y, h, **kw)
def pip(k, x, y, h, **kw): kw.setdefault("prop", False); F.pip(k, x, y, h, **kw)
def opie(k, x, y, h, **kw):
    """Mr Opie, a visitor with binoculars always round his neck (drawn on the chest, same in every scene)."""
    B.visitor(k, x, y, h, suit="plain", hat="panama", tie=False, **kw)
    bx, by, s = x, y + h * 0.56, h * 0.05
    k.line([(x - h * 0.035, y + h * 0.72), (bx - s, by + s)], lw=0.6, amp=0); k.line([(x + h * 0.035, y + h * 0.72), (bx + s, by + s)], lw=0.6, amp=0)
    for sg in (-1, 1): k.rect(bx + sg * s * 0.55 - s * 0.45, by - s * 0.9, s * 0.9, s * 1.6, lw=0.8, fill=K)
    k.rect(bx - s * 0.2, by - s * 0.3, s * 0.4, s * 0.5, lw=0.5, fill=Wt)
def hedley(k, x, y, h, **kw): B.overalls(k, x, y, h, paint=False, **kw)
def agnes(k, x, y, h, **kw): kw.setdefault("teapot", False); F.agnes(k, x, y, h, **kw)

def _telescope(k, x, y, s):
    """Brass telescope on a tripod (x, y = tripod feet centre, s = height)."""
    for dx in (-0.3, 0, 0.3): k.line([(x + dx * s, y), (x, y + s * 0.6)], lw=1.0, amp=0)
    tube = [(x - s * 0.45, y + s * 0.5), (x + s * 0.45, y + s * 0.78), (x + s * 0.43, y + s * 0.88), (x - s * 0.47, y + s * 0.6)]
    k.shape(tube, lw=1.1, fill=Wt, amp=0); k.hatch(tube, angle=70, gap=2.2, lw=0.3)
    for u in (0.3, 0.6): k.line([(x - s * 0.45 + u * s * 0.9, y + s * (0.5 + u * 0.28)), (x - s * 0.47 + u * s * 0.9, y + s * (0.6 + u * 0.28))], lw=1.2, amp=0)
    k.circle(x + s * 0.44, y + s * 0.83, s * 0.06, lw=0.8, fill=Wt)
InkBW.telescope = _telescope

# ----------------------------------------------------------------------------- 1. hook hero / lighthouse on the point
def _point(k, w, h):
    k.sea(14, w - 14, 40, 150, rows=5); k.headland(150, w - 14, 150, 50)
    k.lighthouse(380, 196, 150); k.cloud(110, 320, 0.9); k.cloud(230, 340, 0.7)
    for i in range(7): k.line([(160 + i * 28, 150 - i * 0 + 18 + (i % 2) * 8), (186 + i * 28, 168 + ((i + 1) % 2) * 8)], lw=0.6, amp=0.3)
def hook_plate(k, w, h): full_open(k, w, h); _point(k, w, h); k.unclip()

# ----------------------------------------------------------------------------- 2. cast
CAST = [("WENNA", wenna), ("MR OPIE", opie), ("PIP", pip)]
cast_plate = B.cast_plate_fn([n for n, _ in CAST], style="frames")

# ----------------------------------------------------------------------------- 3. the lighthouse museum + Hedley
def museum_plate(k, w, h):
    plate_open(k, w, h); _point(k, w, h)
    k.rect(254, 150, 4, 50, lw=0.7, fill=Wt); k.rect(206, 196, 100, 30, lw=1.0, fill=Wt); k.text(256, 206, "MUSEUM", size=10, font="Ink-Plex"); k.unclip()
def hedley_m(k, w, h, v): part_open(k, w, h); hedley(k, 318, 150, 112); k.unclip()

# ----------------------------------------------------------------------------- 4. the lamp room: telescope, window to the gallery, clock
def lamp_plate(k, w, h):
    plate_open(k, w, h); k.floorboards(w, y=80)
    k.rect(250, 80, 248, 260, lw=1.3, fill=Wt)
    for i in range(1, 4): k.line([(250 + i * 62, 80), (250 + i * 62, 340)], lw=0.9, amp=0)
    k.line([(250, 150), (498, 150)], lw=1.4, amp=0)   # gallery rail seen through the glass
    for i in range(12): k.line([(258 + i * 20, 110), (258 + i * 20, 150)], lw=0.5, amp=0)
    k.sea(252, 496, 160, 220, rows=3)
    k.text(120, 330, "LAMP ROOM", size=11, font="Ink-Plex")
    k.circle(170, 230, 40, lw=1.0, fill=Wt); k.circle(170, 230, 26, lw=0.6, fill=None)
    for a in range(0, 360, 45): k.line([(170, 230), (170 + 40 * math.cos(math.radians(a)), 230 + 40 * math.sin(math.radians(a)))], lw=0.3, amp=0)
    k.rect(150, 80, 40, 110, lw=1.0, fill=Wt)
def lamp_tel(k, w, h, v): part_open(k, w, h); k.telescope(90, 80, 120); k.text(90, 62, "first keeper's telescope", size=9, font="Ink-Kalam"); k.unclip()
def lamp_clock(k, w, h, v):
    part_open(k, w, h); k.clock_face(60, 300, 26, 2, 15 if v == "q" else 0); k.unclip()
def hedley_in(k, w, h, v): part_open(k, w, h); hedley(k, 215, 30, 200); k.unclip()
def hedley_out(k, w, h, v):
    part_open(k, w, h); k.c.saveState(); p = k.c.beginPath(); p.rect(252, 150, 244, 188); k.c.clipPath(p, stroke=0)
    hedley(k, 380, 120, 190, prop=_cloth); k.c.restoreState(); k.unclip()
def _cloth(k, hx, hyy, h): k.rect(hx - h * 0.03, hyy - h * 0.02, h * 0.07, h * 0.06, lw=0.7, fill=Wt)
def gone_part(k, w, h, v): part_open(k, w, h); k.dashed_outline(40, 80, 100, 110); k.text(90, 62, "gone!", size=11, font="Ink-Kalam"); k.unclip()

# ----------------------------------------------------------------------------- 5. lineup: each seen twice (equal tags)
def _bookshop(k, pw, h):
    k.rect(260, 50, 220, 214, lw=1.2, fill=Wt); k.text(370, 244, "BOOKSHOP", size=11, font="Ink-Plex")
    for r in range(4):
        y = 70 + r * 46; k.line([(270, y), (470, y)], lw=0.8, amp=0)
        for j in range(14): k.rect(272 + j * 14, y, 10, 30 + (j * 7 % 11), lw=0.4, fill=Wt)
def _p_tea(k, pw, h): k.tearoom(pw, h, window=True, counter=False)
def _p_harb(k, pw, h): k.harbour(pw, h, sea_y0=110, sea_y1=180, lighthouse=False, boats=True, wall_top=50)
def _p_book(k, pw, h): k.floorboards(pw, y=50); _bookshop(k, pw, h)
lineup_plate = B.lineup_plate_fn([_p_tea, _p_harb, _p_book], [n for n, _ in CAST])
def _tag(k, x, y, t):
    k.rect(x, y, 96, 40, lw=1.1, fill=Wt); k.circle(x + 12, y + 20, 3, lw=0.6, fill=Wt); k.text(x + 54, y + 12, t, size=16, font="Ink-Kalam")
def tag_part(k, w, h, v, i=0, j=0, t=""):
    part_open(k, w, h); _tag(k, i * PW + 290 + j * 104, 286, t); k.unclip()
TAGS = [("2:00", "2:20"), ("1:45", "2:30"), ("1:55", "2:10")]

# ----------------------------------------------------------------------------- 6. the paths map
PLACES = [("KETTLE & GULL", 90, 80, "15 min"), ("HARBOUR", 256, 60, "20 min"), ("BOOKSHOP", 420, 90, "10 min")]
LH = (256, 300)
def map_plate(k, w, h):
    plate_open(k, w, h); k.text(256, 345, "PATHS TO THE POINT  (steep and rocky)", size=11, font="Ink-Plex")
    k.lighthouse(LH[0], LH[1] - 30, 54)
    for nm, x, y, _ in PLACES:
        k.rect(x - 56, y - 16, 112, 32, lw=1.1, fill=Wt); k.text(x, y - 5, nm, size=10, font="Ink-Plex")
        n = 14
        for i in range(0, n, 2):
            a, b = i / n, (i + 1) / n
            px = lambda u: x + (LH[0] - x) * u + 18 * math.sin(u * 7 + x); py = lambda u: y + 16 + (LH[1] - 40 - y - 16) * u
            k.line([(px(a), py(a)), (px(b), py(b))], lw=0.9, amp=0)
def mins_part(k, w, h, v, i=0):
    part_open(k, w, h); nm, x, y, m = PLACES[i]; mx, my = x + (LH[0] - x) * 0.5 + (40 if i == 2 else -40), y + (LH[1] - 40 - y) * 0.5
    k.rect(mx - 34, my - 13, 68, 26, lw=1.0, fill=Wt); k.text(mx, my - 5, m, size=13, font="Ink-Kalam"); k.unclip()

# ----------------------------------------------------------------------------- 7. Agnes, pencil and receipt
def agnes_plate(k, w, h): plate_open(k, w, h); k.tearoom(w, h, window=True, counter=True); k.unclip()
def agnes_sit(k, w, h, v): part_open(k, w, h); agnes(k, 200, 30, 220); k.unclip()
def receipt_part(k, w, h, v):
    part_open(k, w, h); x, y = 300, 120
    k.shape([(x, y), (x + 70, y), (x + 70, y + 90), (x, y + 90)], lw=0.9, fill=Wt, amp=0.1)
    for j in range(5): k.line([(x + 8, y + 74 - j * 14), (x + 60, y + 74 - j * 14)], lw=0.3, amp=0.2)
    k.unclip()
def pencil_part(k, w, h, v):
    part_open(k, w, h); x, y = 300, 230
    k.shape([(x, y), (x + 60, y + 30), (x + 56, y + 36), (x - 4, y + 6)], lw=0.9, fill=Wt, amp=0); k.shape([(x, y), (x - 4, y + 6), (x - 10, y - 2)], lw=0.6, fill=K, amp=0)
    k.unclip()
def think_part(k, w, h, v): part_open(k, w, h); k.text(240, 300, "15 \u00b7 20 \u00b7 10 \u2026", size=14, font="Ink-Kalam"); k.unclip()

# ----------------------------------------------------------------------------- 8. the puzzle again: a plain table (no marks)
ROWS = [("WENNA", "tea room", "2:00", "2:20", "15 min"), ("MR OPIE", "harbour", "1:45", "2:30", "20 min"), ("PIP", "bookshop", "1:55", "2:10", "10 min")]
def table_plate(k, w, h):
    plate_open(k, w, h); k.floorboards(w, y=60)
    k.case_board(30, 80, 452, 270, title="VANISHED 2:00 \u2013 2:15")
    for j, hd in enumerate(("", "seen at", "seen again", "to lighthouse")): k.text(110 + j * 100, 284, hd, size=11, font="Ink-Plex")
    k.line([(50, 276), (460, 276)], lw=0.8, amp=0)
def row_part(k, w, h, v, i=0):
    part_open(k, w, h); y = 240 - i * 56; r = ROWS[i]
    k.text(110, y, r[0], size=12, font="Ink-Plex"); k.text(110, y - 16, r[1], size=10, font="Ink-Kalam")
    for j, c in enumerate(r[2:]): k.text(210 + j * 100, y - 6, c, size=16, font="Ink-Kalam")
    k.unclip()

# ----------------------------------------------------------------------------- 9. solution board: timelines
X0, X1, T0, T1 = 130, 470, -15, 30          # minutes after 2:00 on the axis
def tx(m): return X0 + (m - T0) * (X1 - X0) / (T1 - T0)
SROWS = [("WENNA", 0, 20, 15), ("PIP", -5, 10, 10), ("MR OPIE", -15, 30, 20)]
def board_plate(k, w, h):
    plate_open(k, w, h); k.floorboards(w, y=60)
    k.case_board(24, 70, 464, 284, title="WHO COULD REACH THE LAMP ROOM?")
    band = [(tx(0), 96), (tx(15), 96), (tx(15), 300), (tx(0), 300)]; k.hatch(band, angle=45, gap=5, lw=0.25)
    k.text((tx(0) + tx(15)) / 2, 302, "telescope gone", size=9, font="Ink-Kalam")
    k.line([(X0, 100), (X1, 100)], lw=1.0, amp=0)
    for m, lab in ((-15, "1:45"), (-5, "1:55"), (0, "2:00"), (5, "2:05"), (10, "2:10"), (15, "2:15"), (20, "2:20"), (30, "2:30")):
        k.line([(tx(m), 96), (tx(m), 104)], lw=0.8, amp=0); k.text(tx(m), 84, lab, size=8, font="Ink-Plex")
    for i, (nm, a, b, d) in enumerate(SROWS):
        y = 260 - i * 66; k.text(72, y - 4, nm, size=11, font="Ink-Plex")
        for m in (a, b): k.circle(tx(m), y, 4, lw=0.8, fill=K)
def srow_part(k, w, h, v, i=0):
    """Earliest arrival (seen + d) and latest leave (seen again - d), with arrows."""
    part_open(k, w, h); nm, a, b, d = SROWS[i]; y = 260 - i * 66; arr, lv = a + d, b - d
    k.line([(tx(a), y), (tx(arr), y + 20)], lw=1.0, amp=0); k.line([(tx(lv), y + 20), (tx(b), y)], lw=1.0, amp=0)
    k.text(tx(arr), y + 26, f"arrive {2 if arr >= 0 else 1}:{arr % 60:02d}", size=10, font="Ink-Kalam")
    k.text(tx(lv), y - 18, f"leave by {2 if lv >= 0 else 1}:{lv % 60:02d}", size=10, font="Ink-Kalam")
    k.circle(tx(arr), y + 20, 3, lw=0.8, fill=Wt); k.circle(tx(lv), y + 20, 3, lw=0.8, fill=Wt)
    k.unclip()
def x_part(k, w, h, v, i=0):
    part_open(k, w, h); y = 260 - i * 66; x = X1 - 4
    k.line([(x - 12, y - 12), (x + 12, y + 12)], lw=2.2, amp=0); k.line([(x - 12, y + 12), (x + 12, y - 12)], lw=2.2, amp=0); k.unclip()
def win_part(k, w, h, v):
    part_open(k, w, h); y = 260 - 2 * 66 + 20
    k.shape(k.arcpts((tx(5) + tx(10)) / 2, y, 40, 18, 0, 360, 30), lw=2.0, fill=None, amp=0.3)
    k.text((tx(5) + tx(10)) / 2 + 6, y + 26, "5 minutes", size=12, font="Ink-Kalam"); k.unclip()

# ----------------------------------------------------------------------------- 10. confession: Tuesdays at two, under supervision
def confess_plate(k, w, h): lamp_plate(k, w, h); k.telescope(90, 80, 120); k.unclip()
def opie_conf(k, w, h, v): part_open(k, w, h); opie(k, 230, 30, 200, expr="sheepish" if "sheepish" in v else "neutral"); k.unclip()
def hedley_conf(k, w, h, v): part_open(k, w, h); hedley(k, 400, 30, 200, flip=True); k.unclip()
def tues_part(k, w, h, v): part_open(k, w, h); k.pin_card(330, 270, 150, 50, ["Tuesdays at 2", "(supervised)"], size=12); k.unclip()

def _vig(k, w, h): k.lighthouse(w * 0.5, h * 0.3, h * 0.5); k.telescope(w * 0.25, h * 0.18, h * 0.3)
vignette = B.vignette_fn(_vig)

def jobs():
    J = []
    J.append(dict(name="hook", w=AW, h=AH, plate=hook_plate, seed=1601, parts=dict(**B.FX_GULL)))
    J.append(dict(name="cast", w=CW, h=CH, plate=cast_plate, seed=1602, parts={
        f"s{i}": dict(fn=B.cast_fig_fn(i, 3, fn), variants=V2) for i, (_, fn) in enumerate(CAST)}))
    J.append(dict(name="museum", w=AW, h=AH, plate=museum_plate, seed=1603, parts=dict(hedley=dict(fn=hedley_m, variants=V2), **B.FX_GULL)))
    J.append(dict(name="lamp", w=AW, h=AH, plate=lamp_plate, seed=1604, parts=dict(
        tel=dict(fn=lamp_tel, variants=["base"]), gone=dict(fn=gone_part, variants=["base"]), clock=dict(fn=lamp_clock, variants=["base", "q"]),
        hin=dict(fn=hedley_in, variants=V2), hin2=dict(fn=hedley_in, variants=V2), hout=dict(fn=hedley_out, variants=["base"]))))
    tags = {f"t{i}{j}": dict(fn=partial(tag_part, i=i, j=j, t=TAGS[i][j]), variants=["base"]) for i in range(3) for j in range(2)}
    J.append(dict(name="lineup", w=3 * PW, h=AH, plate=lineup_plate, seed=1605, parts={
        **{f"s{i}": dict(fn=B.lineup_fig_fn(i, fn, x=PW / 2 - 140, y=50, fh=220), variants=V3) for i, (_, fn) in enumerate(CAST)}, **tags}))
    J.append(dict(name="map", w=AW, h=AH, plate=map_plate, seed=1606, parts={f"m{i}": dict(fn=partial(mins_part, i=i), variants=["base"]) for i in range(3)}))
    J.append(dict(name="agnes", w=AW, h=AH, plate=agnes_plate, seed=1607, parts=dict(
        agnes=dict(fn=agnes_sit, variants=V2), receipt=dict(fn=receipt_part, variants=["base"]), pencil=dict(fn=pencil_part, variants=["base"]),
        think=dict(fn=think_part, variants=["base"]))))
    J.append(dict(name="table", w=AW, h=AH, plate=table_plate, seed=1608, parts={f"r{i}": dict(fn=partial(row_part, i=i), variants=["base"]) for i in range(3)}))
    J.append(dict(name="board", w=AW, h=AH, plate=board_plate, seed=1609, parts={
        **{f"b{i}": dict(fn=partial(srow_part, i=i), variants=["base"]) for i in range(3)},
        **{f"x{i}": dict(fn=partial(x_part, i=i), variants=["base"]) for i in range(2)}, "win": dict(fn=win_part, variants=["base"])}))
    J.append(dict(name="confess", w=AW, h=AH, plate=confess_plate, seed=1610, parts=dict(
        opie=dict(fn=opie_conf, variants=["sheepish", "sheepish+blink"]), hedley=dict(fn=hedley_conf, variants=V2), tues=dict(fn=tues_part, variants=["base"]))))
    J.append(dict(name="vignette", w=384, h=384, plate=vignette, seed=1611))
    return J

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    J = [j for j in jobs() if not want or j["name"] in want]
    save_layers(OUT, J, B.make_ink)
