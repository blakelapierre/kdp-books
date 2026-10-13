"""Illustrations for Case 23, The Odd Glove: BLACK-AND-WHITE ink (bwkit) with the simple v1 peg-doll characters.
Morwenna's back windowsill with the rare white orchid, the open window and the single navy RIGHT-hand glove with white
anchors, three people in the lane whose hands/gloves are shown exactly as narrated, and a "whose glove?" board.
PART sprites use part_open (clip only, never frame2).
Hook (render.py HOOK_STYLE="glovepair"): borderless hero of the cobbled lane and the flower shop window.
Fairness: Kerensa, Mr Fenwick and Mr Lanyon share one stance, height, arms-down pose and neutral face in the cast strip and
the lineup; glove / pocket details and an equal-size tag pop on each as narrated. Only the confession shows Lanyon sheepish.
Run: python3 art_case23.py [scene ...]"""
import os, sys
from functools import partial
import bwkit as B
from bwkit import plate_open, part_open, full_open, InkBW, PW, AW, AH, V2, V3, CW, CH
import figures as F
from inkart import K, Wt
from layers import save_layers

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-23")

def kerensa(k, x, y, h, **kw): B.lady(k, x, y, h, dress="stripe", hair="curls", hat="sun", **kw)
def fenwick(k, x, y, h, **kw): B.visitor(k, x, y, h, suit="dark", hat="cap", tie=False, moustache=True, **kw)
def lanyon(k, x, y, h, **kw): B.visitor(k, x, y, h, suit="check", hat="panama", tie=True, **kw)
def morwenna(k, x, y, h, **kw): F.morwenna(k, x, y, h, **kw)
def agnes(k, x, y, h, **kw): kw.setdefault("teapot", False); F.agnes(k, x, y, h, **kw)

def _anchor(k, x, y, s, col=Wt):
    k.circle(x, y + s, s * 0.3, lw=0.4, fill=None); k.line([(x, y + s * 0.7), (x, y - s)], lw=0.5, amp=0)
    k.line([(x - s * 0.5, y + s * 0.3), (x + s * 0.5, y + s * 0.3)], lw=0.4, amp=0)
    k.shape(k.arcpts(x, y - s * 0.4, s * 0.7, s * 0.6, 180, 360, 10), lw=0.4, fill=None, amp=0)

def _glove(k, x, y, s, anchors=False, right=True):
    """A knitted glove seen from the back, fingers up; (x, y) = cuff bottom centre; s = height. Navy = dense cross-hatch."""
    w = s * 0.5; cuff = s * 0.22; sg = -1 if right else 1          # back of a right hand: thumb on the viewer's left
    k.rect(x - w / 2, y, w, cuff, lw=0.9, fill=Wt)
    palm = [(x - w / 2, y + cuff), (x + w / 2, y + cuff), (x + w / 2, y + s * 0.62), (x - w / 2, y + s * 0.62)]
    k.shape(palm, lw=0.9, fill=Wt, amp=0); k.hatch(palm, angle=45, gap=max(1.0, s * 0.03), lw=0.3, cross=True)
    fw = w / 4
    for i, fl in enumerate((0.3, 0.38, 0.36, 0.26) if right else (0.26, 0.36, 0.38, 0.3)):
        f = [(x - w / 2 + i * fw + 0.5, y + s * 0.62), (x - w / 2 + (i + 1) * fw - 0.5, y + s * 0.62), (x - w / 2 + (i + 1) * fw - 0.5, y + s * (0.62 + fl)), (x - w / 2 + i * fw + 0.5, y + s * (0.62 + fl))]
        k.shape(f, lw=0.8, fill=Wt, amp=0); k.hatch(f, angle=45, gap=max(1.0, s * 0.03), lw=0.3, cross=True)
    th = [(x + sg * w / 2, y + cuff + s * 0.05), (x + sg * (w / 2 + s * 0.16), y + s * 0.42), (x + sg * (w / 2 + s * 0.1), y + s * 0.5), (x + sg * w / 2, y + s * 0.36)]
    k.shape(th, lw=0.8, fill=Wt, amp=0); k.hatch(th, angle=45, gap=max(1.0, s * 0.03), lw=0.3, cross=True)
    for j in range(5): k.line([(x - w / 2 + j * w / 4, y + 1), (x - w / 2 + j * w / 4, y + cuff - 1)], lw=0.25, amp=0) if not anchors else None
    if anchors:
        for j in range(3): _anchor(k, x - w / 3 + j * w / 3, y + cuff / 2, cuff * 0.32)
InkBW.glove = _glove

def _mitt(k, x, y, h, anchors=False):
    """Tiny glove over a peg-doll hand at (x, y) for a figure of height h (dark fill, white cuff band if anchors)."""
    r = h * 0.03; k.shape(k.arcpts(x, y, r, r * 1.25, 0, 360, 16), lw=0.6, fill=K, amp=0)
    k.circle(x + r * 0.9, y + r * 0.2, r * 0.45, lw=0.4, fill=K)
    k.rect(x - r, y + r * 0.9, 2 * r, r * 0.7, lw=0.5, fill=Wt if anchors else K)
    if anchors:
        for j in (-1, 0, 1): k.circle(x + j * r * 0.6, y + r * 1.25, r * 0.12, lw=0, fill=K, stroke=False)

def _orchid(k, x, y, s):
    k.shape([(x - s * 0.3, y), (x + s * 0.3, y), (x + s * 0.38, y + s * 0.4), (x - s * 0.38, y + s * 0.4)], lw=1.0, fill=Wt, amp=0)
    k.line([(x, y + s * 0.4), (x + s * 0.05, y + s * 1.1), (x + s * 0.3, y + s * 1.3)], lw=0.9, amp=0.2)
    for lx in (-1, 1): k.shape(k.arcpts(x + lx * s * 0.22, y + s * 0.5, s * 0.25, s * 0.08, 0, 360, 12), lw=0.6, fill=Wt, amp=0)
    for fx, fy in ((0.3, 1.3), (0.12, 1.12), (0.42, 1.12)):
        cx, cy = x + s * fx, y + s * fy
        for a in range(0, 360, 72): k.shape(k.arcpts(cx + s * 0.07 * B.math.cos(B.math.radians(a)), cy + s * 0.07 * B.math.sin(B.math.radians(a)), s * 0.07, s * 0.05, 0, 360, 10), lw=0.4, fill=Wt, amp=0)
        k.circle(cx, cy, s * 0.025, lw=0.3, fill=K)
InkBW.orchid = _orchid

def _shopfront(k, x, w, name, y=60, hgt=200):
    k.rect(x, y, w, hgt, lw=1.1, fill=Wt); k.rect(x + w * 0.1, y + hgt * 0.3, w * 0.5, hgt * 0.45, lw=0.9, fill=Wt)
    k.rect(x + w * 0.68, y, w * 0.22, hgt * 0.65, lw=0.9, fill=Wt)
    k.rect(x + 6, y + hgt * 0.82, w - 12, hgt * 0.14, lw=0.8, fill=Wt); k.text(x + w / 2, y + hgt * 0.86, name, size=10, font="Ink-Plex")

def _lane(k, w, h):
    k.stones(14, w - 14, 14, 60, rows=3); k.line([(14, 60), (w - 14, 60)], lw=1.0, amp=0)
    _shopfront(k, 30, 200, "MORWENNA'S FLOWERS"); _shopfront(k, 250, 150, "FENWICK GROCER")
    k.line([(440, 60), (440, 230)], lw=1.2, amp=0); k.rect(420, 222, 40, 26, lw=1.0, fill=Wt); k.text(440, 231, "BUS", size=9, font="Ink-Plex")

# ----------------------------------------------------------------------------- 1. hook hero
def hook_plate(k, w, h): full_open(k, w, h); _lane(k, w, h); k.unclip()

# ----------------------------------------------------------------------------- 2. cast
CAST = [("KERENSA", kerensa), ("MR FENWICK", fenwick), ("MR LANYON", lanyon)]
cast_plate = B.cast_plate_fn([n for n, _ in CAST], style="tags")

# ----------------------------------------------------------------------------- 3. the lane on a bitter windy evening
def lane_plate(k, w, h): plate_open(k, w, h); _lane(k, w, h); k.unclip()
def wind_part(k, w, h, v):
    part_open(k, w, h)
    for i, (x, y) in enumerate(((60, 300), (200, 330), (330, 290), (120, 260))):
        k.line([(x, y), (x + 50, y + 4), (x + 80, y - 2)], lw=0.7, amp=0.4); k.shape(k.arcpts(x + 86, y + 4, 6, 6, 200, 520, 14), lw=0.6, fill=None, amp=0)
    k.text(390, 330, "bitter and windy", size=11, font="Ink-Kalam"); k.unclip()
def morwenna_l(k, w, h, v): part_open(k, w, h); morwenna(k, 120, 22, 150); k.unclip()
def agnes_l(k, w, h, v): part_open(k, w, h); agnes(k, 200, 22, 150); k.unclip()
def three_part(k, w, h, v): part_open(k, w, h); k.pin_card(290, 300, 150, 40, ["3 people nearby"], size=12); k.unclip()

# ----------------------------------------------------------------------------- 4. the back windowsill: the orchid
def sill_plate(k, w, h):
    plate_open(k, w, h); k.floorboards(w, y=60)
    k.rect(150, 150, 220, 170, lw=1.4, fill=Wt); k.rect(140, 140, 240, 12, lw=1.0, fill=Wt)
    k.text(256, 340, "the back windowsill", size=11, font="Ink-Plex")
def win_shut(k, w, h, v): part_open(k, w, h); k.line([(260, 152), (260, 318)], lw=1.0, amp=0); k.line([(152, 236), (368, 236)], lw=1.0, amp=0); k.unclip()
def win_open(k, w, h, v):
    part_open(k, w, h); k.rect(152, 152, 216, 166, lw=0.1, fill=K)
    k.text(260, 230, "open!", size=14, font="Ink-Kalam", color=Wt) if False else k.pin_card(400, 200, 90, 30, ["open!"], size=11)
    k.unclip()
def orchid_part(k, w, h, v): part_open(k, w, h); k.orchid(240, 152, 90); k.unclip()
def bloom_part(k, w, h, v): part_open(k, w, h); k.pin_card(24, 260, 110, 52, ["3 years:", "first bloom!"], size=11); k.unclip()
def gone_s(k, w, h, v): part_open(k, w, h); k.dashed_outline(206, 152, 70, 36); k.pin_card(24, 190, 110, 36, ["gone, pot and all"], size=10); k.unclip()
def morwenna_s(k, w, h, v): part_open(k, w, h); morwenna(k, 420, 30, 200, flip=True); k.unclip()

# ----------------------------------------------------------------------------- 5. under the window: the single glove
def cobble_plate(k, w, h):
    plate_open(k, w, h); k.stones(14, w - 14, 14, 140, rows=5); k.wall(14, 140, w - 28, 230, gap=3.0)
    k.rect(170, 220, 170, 120, lw=1.4, fill=K)
    k.unclip()
def glove_part(k, w, h, v): part_open(k, w, h); k.glove(160, 70, 60, anchors=True, right=True); k.text(160, 54, "a single glove", size=11, font="Ink-Kalam"); k.unclip()
def gzoom_part(k, w, h, v):
    part_open(k, w, h); k.rect(300, 40, 190, 150, lw=1.3, fill=Wt); k.glove(395, 66, 90, anchors=True, right=True)
    k.text(395, 48, "navy \u00b7 RIGHT hand", size=11, font="Ink-Kalam"); k.unclip()
def anch_part(k, w, h, v): part_open(k, w, h); k.pin_card(320, 200, 150, 30, ["white anchors at the wrist"], size=10); k.unclip()

# ----------------------------------------------------------------------------- 6. lineup: the three people's hands, as narrated
def _bus(k, pw, h):
    k.stones(14, pw - 14, 14, 50, rows=2); k.line([(300, 50), (300, 250)], lw=1.4, amp=0); k.rect(276, 244, 48, 30, lw=1.0, fill=Wt); k.text(300, 254, "BUS", size=10, font="Ink-Plex")
def _grocer(k, pw, h): k.stones(14, pw - 14, 14, 50, rows=2); _shopfront(k, 250, 220, "FENWICK GROCER", y=50, hgt=200)
def _walk(k, pw, h): k.stones(14, pw - 14, 14, 50, rows=2); k.wall(250, 50, 240, 160, gap=3.0)
lineup_plate = B.lineup_plate_fn([_bus, _grocer, _walk], [n for n, _ in CAST])
FX, FY, FH = PW / 2 - 160, 50, 220
HANDL, HANDR = (FX - 0.2 * FH, FY + 0.31 * FH), (FX + 0.2 * FH, FY + 0.31 * FH)   # viewer's left = his/her RIGHT hand
TAGS = [["navy gloves, PLAIN,", "one on each hand"], ["no gloves at all,", "fingers red with cold"], ["navy LEFT glove, anchors;", "right hand in his pocket"]]
def ltag(k, w, h, v, i=0):
    part_open(k, w, h); x = i * PW + 236; k.rect(x, 286, 250, 50, lw=1.1, fill=Wt)
    for j, ln in enumerate(TAGS[i]): k.text(x + 125, 318 - j * 20, ln, size=12, font="Ink-Kalam")
    k.unclip()
def gl_ker(k, w, h, v): part_open(k, w, h); [_mitt(k, x, y, FH) for x, y in (HANDL, HANDR)]; k.unclip()
def gl_fen(k, w, h, v):
    part_open(k, w, h); x0 = PW
    for x, y in (HANDL, HANDR):
        for a in (-1, 0, 1): k.line([(x0 + x + a * 6, y - 10), (x0 + x + a * 8, y - 16)], lw=0.6, amp=0)
    k.unclip()
def gl_lan(k, w, h, v): part_open(k, w, h); _mitt(k, 2 * PW + HANDR[0], HANDR[1], FH, anchors=True); k.unclip()
def pocket_lan(k, w, h, v):
    part_open(k, w, h); x, y = 2 * PW + HANDL[0], HANDL[1]
    k.rect(x - 8, y - 10, 24, 20, lw=0.9, fill=Wt); k.line([(x - 8, y + 6), (x + 16, y + 6)], lw=0.6, amp=0); k.unclip()
def lanyon_zoom(k, w, h, v):
    part_open(k, w, h); x = 2 * PW + 330; k.rect(x, 110, 140, 140, lw=1.2, fill=Wt); k.glove(x + 70, 136, 80, anchors=True, right=False)
    k.text(x + 70, 118, "his LEFT glove", size=10, font="Ink-Kalam"); k.unclip()

# ----------------------------------------------------------------------------- 7. solution board: whose glove?
def board_plate(k, w, h):
    plate_open(k, w, h); k.floorboards(w, y=56); k.case_board(24, 66, 464, 292, title="WHOSE GLOVE?")
    k.glove(160, 160, 100, anchors=True, right=True); k.text(160, 140, "dropped: RIGHT, anchors", size=10, font="Ink-Kalam")
def b_pair(k, w, h, v):
    part_open(k, w, h); k.glove(330, 160, 100, anchors=True, right=False); k.text(330, 140, "Lanyon's LEFT, anchors", size=10, font="Ink-Kalam")
    k.text(245, 290, "a pair!", size=14, font="Ink-Kalam"); k.line([(200, 282), (290, 282)], lw=0.8, amp=0.2); k.unclip()
def b_row(k, w, h, v, i=0):
    part_open(k, w, h); y = (110, 84)[i]; txt = ("Kerensa: both gloves on, plain", "Mr Fenwick: never wears gloves")[i]
    k.text(250, y, txt, size=11, font="Ink-Kalam"); k.line([(150, y + 4), (350, y + 4)], lw=1.6, amp=0.2); k.unclip()
def b_ring(k, w, h, v): part_open(k, w, h); k.shape(k.arcpts(330, 210, 60, 82, 0, 360, 30), lw=2.2, fill=None, amp=0.4); k.pin_card(400, 260, 80, 40, ["Lanyon", "took it"], size=11); k.unclip()

# ----------------------------------------------------------------------------- 8. confession: the orchid on his back seat; a proper cutting
def conf_plate(k, w, h): plate_open(k, w, h); k.stones(14, w - 14, 14, 60, rows=3); k.car(330, 60, 260); k.unclip()
def lanyon_c(k, w, h, v): part_open(k, w, h); lanyon(k, 100, 40, 200, expr="sheepish" if "sheepish" in v else "neutral"); k.unclip()
def box_part(k, w, h, v): part_open(k, w, h); k.rect(318, 120, 40, 26, lw=0.9, fill=Wt); k.orchid(338, 146, 30); k.pin_card(380, 270, 110, 40, ["back seat:", "safe and sound"], size=10); k.unclip()
def miles_part(k, w, h, v): part_open(k, w, h); k.pin_card(200, 310, 150, 40, ["drove 300 miles", "to see it bloom"], size=10); k.unclip()
def cut_part(k, w, h, v): part_open(k, w, h); k.pin_card(200, 254, 150, 40, ["a proper cutting,", "glove back on"], size=10); k.unclip()

def _vig(k, w, h): k.glove(w / 2, h * 0.22, h * 0.55, anchors=True)
vignette = B.vignette_fn(_vig)

def jobs():
    J = []
    J.append(dict(name="hook", w=AW, h=AH, plate=hook_plate, seed=2301))
    J.append(dict(name="cast", w=CW, h=CH, plate=cast_plate, seed=2302, parts={
        f"s{i}": dict(fn=B.cast_fig_fn(i, 3, fn), variants=V2) for i, (_, fn) in enumerate(CAST)}))
    J.append(dict(name="lane", w=AW, h=AH, plate=lane_plate, seed=2303, parts=dict(
        wind=dict(fn=wind_part, variants=["base"]), morwenna=dict(fn=morwenna_l, variants=V2), agnes=dict(fn=agnes_l, variants=V2), three=dict(fn=three_part, variants=["base"]))))
    J.append(dict(name="sill", w=AW, h=AH, plate=sill_plate, seed=2304, parts=dict(
        shut=dict(fn=win_shut, variants=["base"]), open=dict(fn=win_open, variants=["base"]), orchid=dict(fn=orchid_part, variants=["base"]),
        bloom=dict(fn=bloom_part, variants=["base"]), gone=dict(fn=gone_s, variants=["base"]), morwenna=dict(fn=morwenna_s, variants=V2))))
    J.append(dict(name="cobble", w=AW, h=AH, plate=cobble_plate, seed=2305, parts=dict(
        glove=dict(fn=glove_part, variants=["base"]), zoom=dict(fn=gzoom_part, variants=["base"]), anch=dict(fn=anch_part, variants=["base"]))))
    J.append(dict(name="lineup", w=3 * PW, h=AH, plate=lineup_plate, seed=2306, parts={
        **{f"s{i}": dict(fn=B.lineup_fig_fn(i, fn, x=FX, y=FY, fh=FH), variants=V3) for i, (_, fn) in enumerate(CAST)},
        **{f"p{i}": dict(fn=partial(ltag, i=i), variants=["base"]) for i in range(3)},
        "gk": dict(fn=gl_ker, variants=["base"]), "gf": dict(fn=gl_fen, variants=["base"]), "gl": dict(fn=gl_lan, variants=["base"]),
        "pocket": dict(fn=pocket_lan, variants=["base"]), "lz": dict(fn=lanyon_zoom, variants=["base"])}))
    J.append(dict(name="board", w=AW, h=AH, plate=board_plate, seed=2307, parts={
        "pair": dict(fn=b_pair, variants=["base"]), **{f"r{i}": dict(fn=partial(b_row, i=i), variants=["base"]) for i in range(2)}, "ring": dict(fn=b_ring, variants=["base"])}))
    J.append(dict(name="confess", w=AW, h=AH, plate=conf_plate, seed=2308, parts=dict(
        lanyon=dict(fn=lanyon_c, variants=["sheepish", "sheepish+blink"]), box=dict(fn=box_part, variants=["base"]),
        miles=dict(fn=miles_part, variants=["base"]), cut=dict(fn=cut_part, variants=["base"]))))
    J.append(dict(name="vignette", w=384, h=384, plate=vignette, seed=2309))
    return J

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    J = [j for j in jobs() if not want or j["name"] in want]
    save_layers(OUT, J, B.make_ink)
