"""Illustrations for Case 22, The Honest Fishermen: BLACK-AND-WHITE ink (bwkit) with the simple v1 peg-doll characters.
Two quay signs (HONEST: always true / FIBBER: never true), Captain Quill's vanished net, three fishermen with equal speech
cards, and a statement board on which the solution's test and HONEST/FIBBER tags appear only after "The Solution".
PART sprites use part_open (clip only, never frame2).
Hook (render.py HOOK_STYLE="toggle"): borderless hero of the harbour wall with the empty net hooks.
Fairness: Ned, Bran and Col share one stance, height, arms-down pose and neutral face in the cast strip and the lineup;
each gets the same speech card when he speaks. Only the confession shows Bran sheepish.
Run: python3 art_case22.py [scene ...]"""
import os, sys
from functools import partial
import bwkit as B
from bwkit import plate_open, part_open, full_open, InkBW, PW, AW, AH, V2, V3, CW, CH
import figures as F
from inkart import K, Wt
from layers import save_layers

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-22")

def ned(k, x, y, h, **kw): B.overalls(k, x, y, h, cap=True, **kw)
def bran(k, x, y, h, **kw): B.visitor(k, x, y, h, suit="stripe", hat="cap", tie=False, **kw)
def col(k, x, y, h, **kw): B.visitor(k, x, y, h, suit="check", hat=None, tie=False, **kw)
def quill(k, x, y, h, **kw): kw.setdefault("prop", False); F.quill(k, x, y, h, **kw)
def agnes(k, x, y, h, **kw): kw.setdefault("teapot", False); F.agnes(k, x, y, h, **kw)

def _net(k, x, y, w, h, holes=False):
    """A fishing net hung in a loose bag shape: a mesh of crossing lines with float corks on top."""
    pts = [(x, y + h), (x + w, y + h), (x + w * 0.85, y + h * 0.3), (x + w * 0.5, y), (x + w * 0.15, y + h * 0.3)]
    k.shape(pts, lw=1.0, fill=Wt, amp=0.2); k.hatch(pts, angle=40, gap=5, lw=0.35, cross=True)
    for i in range(5): k.circle(x + w * (0.1 + i * 0.2), y + h, 3.2, lw=0.6, fill=Wt)
    if holes:
        for hx, hy in ((0.35, 0.5), (0.62, 0.35), (0.55, 0.7)): k.circle(x + w * hx, y + h * hy, 6, lw=0.7, fill=Wt)
InkBW.net = _net

def _bun(k, x, y, r):
    k.shape(k.arcpts(x, y, r, r * 0.65, 0, 360, 22), lw=0.9, fill=Wt, amp=0.1)
    for i in range(4): k.circle(x - r * 0.5 + i * r * 0.33, y + r * 0.1 * (i % 2), 1.2, lw=0, fill=K, stroke=False)
InkBW.bun = _bun

def _hooks(k, x0, n, y=110):
    for i in range(n): k.line([(x0 + i * 30, y + 2), (x0 + i * 30, y + 14), (x0 + i * 30 + 5, y + 14)], lw=0.9, amp=0)
InkBW.net_hooks = _hooks

# ----------------------------------------------------------------------------- 1. hook hero
def hook_plate(k, w, h): full_open(k, w, h); k.harbour(w, h); k.net_hooks(200, 5); k.unclip()

# ----------------------------------------------------------------------------- 2. cast
CAST = [("NED", ned), ("BRAN", bran), ("COL", col)]
cast_plate = B.cast_plate_fn([n for n, _ in CAST], style="frames")

# ----------------------------------------------------------------------------- 3. the two kinds of fishermen (quay signs)
def rules_plate(k, w, h):
    plate_open(k, w, h); k.harbour(w, h, boats=True)
    for x in (130, 382): k.line([(x, 110), (x, 200)], lw=1.4, amp=0)
    k.unclip()
def sign_part(k, w, h, v, i=0):
    part_open(k, w, h); x = (60, 312)[i]
    k.rect(x, 196, 140, 64, lw=1.3, fill=Wt)
    k.text(x + 70, 238, ("HONEST", "FIBBER")[i], size=15, font="Ink-Plex")
    k.text(x + 70, 214, ("always tells the truth", "never tells the truth")[i], size=10, font="Ink-Kalam"); k.unclip()
def never_part(k, w, h, v): part_open(k, w, h); k.pin_card(176, 290, 160, 46, ["one or the other,", "and nobody changes"], size=11); k.unclip()

# ----------------------------------------------------------------------------- 4. the harbour wall: Captain Quill's net vanished
def wall_plate(k, w, h): plate_open(k, w, h); k.harbour(w, h, boats=False); k.net_hooks(230, 5); k.unclip()
def quill_w(k, w, h, v): part_open(k, w, h); quill(k, 120, 40, 200); k.unclip()
def net_part(k, w, h, v): part_open(k, w, h); k.net(226, 110, 130, 70); k.text(292, 196, "brand new net", size=10, font="Ink-Kalam"); k.unclip()
def gone_w(k, w, h, v): part_open(k, w, h); k.dashed_outline(226, 110, 130, 70); k.text(292, 196, "vanished!", size=11, font="Ink-Kalam"); k.unclip()
def one_part(k, w, h, v): part_open(k, w, h); k.pin_card(330, 300, 160, 48, ["Ned, Bran or Col:", "exactly ONE took it"], size=11); k.unclip()

# ----------------------------------------------------------------------------- 5. the tea room: saffron buns
def tea_plate(k, w, h): plate_open(k, w, h); k.tearoom(w, h, window=True, counter=True); k.unclip()
def agnes_t(k, w, h, v): part_open(k, w, h); agnes(k, 330, 30, 210); k.unclip()
def buns_part(k, w, h, v):
    part_open(k, w, h); k.shape(k.arcpts(170, 128, 56, 12, 0, 360, 26), lw=1.0, fill=Wt, amp=0)
    for bx, by in ((146, 136), (170, 140), (194, 136), (158, 150), (182, 150)): k.bun(bx, by, 13)
    k.text(170, 104, "saffron buns", size=10, font="Ink-Kalam"); k.unclip()
def know_part(k, w, h, v): part_open(k, w, h); k.pin_card(160, 282, 190, 48, ["who's honest? who fibs?", "Agnes doesn't know"], size=11); k.unclip()
def bun_part(k, w, h, v): part_open(k, w, h); k.pin_card(160, 290, 190, 40, ["a whole bun, very slowly"], size=11); k.unclip()

# ----------------------------------------------------------------------------- 6. lineup: what each fisherman said (equal speech cards)
def _p(k, pw, h):
    k.stones(14, pw - 14, 14, 50, rows=2); k.sea(14, pw - 14, 50, 110, rows=3); k.line([(14, 50), (pw - 14, 50)], lw=1.0, amp=0)
lineup_plate = B.lineup_plate_fn([_p, _p, _p], [n for n, _ in CAST])
SAID = [["\u201cI didn't take the net.", "And Bran is a fibber.\u201d"], ["\u201cCol took the net.\u201d"], ["\u201cNed is an honest man.", "And I didn't take the net.\u201d"]]
def stag(k, w, h, v, i=0):
    part_open(k, w, h); x = i * PW + 236; n = len(SAID[i])
    k.rect(x, 300 - 22 * n, 250, 18 + 22 * n, lw=1.1, fill=Wt)
    k.shape([(x + 10, 310 - 22 * n), (x - 14, 290 - 22 * n), (x + 26, 300 - 22 * n)], lw=1.0, fill=Wt, amp=0)
    for j, ln in enumerate(SAID[i]): k.text(x + 125, 296 - 22 * (j + 1) + 8, ln, size=13, font="Ink-Kalam")
    k.unclip()

# ----------------------------------------------------------------------------- 7. the statement board (recap; solution marks only after "The Solution")
ROWS = [("NED", "I didn't take it. Bran is a fibber."), ("BRAN", "Col took it."), ("COL", "Ned is honest. I didn't take it.")]
RY = [270, 222, 174]
def board_plate(k, w, h):
    plate_open(k, w, h); k.floorboards(w, y=56)
    k.case_board(24, 66, 464, 292, title="HONEST OR FIBBER?")
def b_row(k, w, h, v, i=0):
    part_open(k, w, h); y = RY[i]; k.rect(40, y - 8, 330, 34, lw=0.8, fill=Wt)
    k.text(70, y + 4, ROWS[i][0], size=12, font="Ink-Plex"); k.text(232, y + 3, ROWS[i][1], size=11, font="Ink-Kalam"); k.unclip()
def b_test(k, w, h, v):
    part_open(k, w, h); k.pin_card(40, 76, 300, 76, ["If Col fibbed: Ned fibs AND Col took it.", "But then Ned's \u201cI didn't take it\u201d is false,", "so Ned took it too: two thieves!"], size=10); k.unclip()
def b_cross(k, w, h, v):
    part_open(k, w, h)
    for a, b in (((350, 82), (392, 140)), ((392, 82), (350, 140))): k.line([a, b], lw=2.4, amp=0.3)
    k.text(371, 64, "impossible", size=10, font="Ink-Kalam"); k.unclip()
def b_tag(k, w, h, v, i=0):
    part_open(k, w, h); y = RY[i]; lab = ("HONEST", "FIBBER", "HONEST")[i]
    k.rect(384, y - 6, 92, 30, lw=1.4, fill=Wt); k.text(430, y + 3, lab, size=12, font="Ink-Plex"); k.unclip()
def b_false(k, w, h, v): part_open(k, w, h); k.line([(186, 230), (282, 230)], lw=1.8, amp=0.2); k.text(310, 246, "false", size=10, font="Ink-Kalam"); k.unclip()
def b_ring(k, w, h, v):
    part_open(k, w, h); k.shape(k.arcpts(72, 230, 40, 22, 0, 360, 30), lw=2.2, fill=None, amp=0.4)
    k.pin_card(400, 96, 80, 40, ["Bran", "took it"], size=11); k.unclip()

# ----------------------------------------------------------------------------- 8. confession: Bran mends his own net on the harbour wall
def conf_plate(k, w, h): plate_open(k, w, h); k.harbour(w, h, boats=True); k.unclip()
def bran_c(k, w, h, v): part_open(k, w, h); bran(k, 150, 40, 210, expr="sheepish" if "sheepish" in v else "neutral"); k.unclip()
def holes_part(k, w, h, v): part_open(k, w, h); k.net(250, 112, 110, 60, holes=True); k.text(305, 190, "his own net: full of holes", size=10, font="Ink-Kalam"); k.unclip()
def borrow_part(k, w, h, v): part_open(k, w, h); k.pin_card(320, 300, 170, 46, ["\u201cnothing to do", "with me!\u201d (a fibber)"], size=11); k.unclip()
def mend_part(k, w, h, v): part_open(k, w, h); k.pin_card(300, 240, 190, 40, ["mending it where all can see"], size=11); k.unclip()

def _vig(k, w, h): k.net(w * 0.2, h * 0.25, w * 0.6, h * 0.45)
vignette = B.vignette_fn(_vig)

def jobs():
    J = []
    J.append(dict(name="hook", w=AW, h=AH, plate=hook_plate, seed=2201))
    J.append(dict(name="cast", w=CW, h=CH, plate=cast_plate, seed=2202, parts={
        f"s{i}": dict(fn=B.cast_fig_fn(i, 3, fn), variants=V2) for i, (_, fn) in enumerate(CAST)}))
    J.append(dict(name="rules", w=AW, h=AH, plate=rules_plate, seed=2203, parts={
        **{f"g{i}": dict(fn=partial(sign_part, i=i), variants=["base"]) for i in range(2)}, "never": dict(fn=never_part, variants=["base"]), **B.FX_GULL}))
    J.append(dict(name="wall", w=AW, h=AH, plate=wall_plate, seed=2204, parts=dict(
        quill=dict(fn=quill_w, variants=V2), net=dict(fn=net_part, variants=["base"]), gone=dict(fn=gone_w, variants=["base"]), one=dict(fn=one_part, variants=["base"]))))
    J.append(dict(name="tea", w=AW, h=AH, plate=tea_plate, seed=2205, parts=dict(
        agnes=dict(fn=agnes_t, variants=V3), buns=dict(fn=buns_part, variants=["base"]), know=dict(fn=know_part, variants=["base"]), bun=dict(fn=bun_part, variants=["base"]))))
    J.append(dict(name="lineup", w=3 * PW, h=AH, plate=lineup_plate, seed=2206, parts={
        **{f"s{i}": dict(fn=B.lineup_fig_fn(i, fn, x=PW / 2 - 160, y=50, fh=220), variants=V3) for i, (_, fn) in enumerate(CAST)},
        **{f"p{i}": dict(fn=partial(stag, i=i), variants=["base"]) for i in range(3)}}))
    J.append(dict(name="board", w=AW, h=AH, plate=board_plate, seed=2207, parts={
        **{f"r{i}": dict(fn=partial(b_row, i=i), variants=["base"]) for i in range(3)},
        "test": dict(fn=b_test, variants=["base"]), "cross": dict(fn=b_cross, variants=["base"]),
        **{f"t{i}": dict(fn=partial(b_tag, i=i), variants=["base"]) for i in range(3)},
        "false": dict(fn=b_false, variants=["base"]), "ring": dict(fn=b_ring, variants=["base"])}))
    J.append(dict(name="confess", w=AW, h=AH, plate=conf_plate, seed=2208, parts=dict(
        bran=dict(fn=bran_c, variants=["sheepish", "sheepish+blink"]), holes=dict(fn=holes_part, variants=["base"]),
        borrow=dict(fn=borrow_part, variants=["base"]), mend=dict(fn=mend_part, variants=["base"]))))
    J.append(dict(name="vignette", w=384, h=384, plate=vignette, seed=2209))
    return J

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    J = [j for j in jobs() if not want or j["name"] in want]
    save_layers(OUT, J, B.make_ink)
