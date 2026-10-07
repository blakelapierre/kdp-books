"""Illustrations for Case 21, The Spanish Coin: BLACK-AND-WHITE ink (bwkit) with the simple v1 peg-doll characters.
The museum coin case, the worn silver Spanish coin (crown), Jenna's ice cream van and its till, and a "what went into the
till?" board with in/out arrows. PART sprites use part_open (clip only, never frame2).
Hook (render.py HOOK_STYLE="coinflip"): borderless hero of the ice cream van on the sea front.
Fairness: Demelza, Pip and Mr Nankervis share one stance, height, arms-down pose and neutral face in the cast strip and the
lineup; each gets the same style of "how they paid" tag when narrated. Only the confession shows Mr Nankervis sheepish.
Run: python3 art_case21.py [scene ...]"""
import os, sys, math
from functools import partial
import bwkit as B
from bwkit import plate_open, part_open, full_open, InkBW, PW, AW, AH, V2, V3, CW, CH
import figures as F
from inkart import K, Wt
from layers import save_layers

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-21")

def demelza(k, x, y, h, **kw): kw.setdefault("prop", False); F.demelza(k, x, y, h, **kw)
def pip(k, x, y, h, **kw): kw.setdefault("prop", False); F.pip(k, x, y, h, **kw)
def nankervis(k, x, y, h, **kw): B.visitor(k, x, y, h, suit="plain", hat="bowler", tie=True, **kw)
def jenna(k, x, y, h, **kw): B.lady(k, x, y, h, dress="stripe", hair="long", hat=None, **kw)
def agnes(k, x, y, h, **kw): kw.setdefault("teapot", False); F.agnes(k, x, y, h, **kw)

def _coin(k, x, y, r, crown=True):
    k.circle(x, y, r, lw=1.2, fill=Wt); k.circle(x, y, r * 0.82, lw=0.5, fill=None)
    if crown:
        pts = [(x - r * 0.45, y - r * 0.25), (x + r * 0.45, y - r * 0.25), (x + r * 0.5, y + r * 0.3), (x + r * 0.25, y + r * 0.05), (x, y + r * 0.4), (x - r * 0.25, y + r * 0.05), (x - r * 0.5, y + r * 0.3)]
        k.shape(pts, lw=0.9, fill=Wt, amp=0); k.hatch(pts, angle=45, gap=max(1.2, r * 0.12), lw=0.3)
    else:
        for i in range(-2, 3): k.line([(x - r * 0.4, y + i * r * 0.15), (x + r * 0.4, y + i * r * 0.15)], lw=0.4, amp=0)
InkBW.coin = _coin

def _till(k, x, y, w, h):
    k.rect(x, y, w, h, lw=1.2, fill=Wt); k.rect(x + 6, y + h * 0.55, w - 12, h * 0.35, lw=0.8, fill=Wt)
    for i in range(4): k.rect(x + 8 + i * (w - 16) / 4, y + 6, (w - 16) / 4 - 4, h * 0.45, lw=0.6, fill=Wt)
InkBW.till = _till

def _van(k, x, y, w):
    h = w * 0.55
    k.shape([(x, y + h * 0.15), (x + w, y + h * 0.15), (x + w, y + h * 0.8), (x + w * 0.82, y + h), (x, y + h)], lw=1.3, fill=Wt, amp=0.1)
    k.rect(x + w * 0.12, y + h * 0.45, w * 0.5, h * 0.4, lw=1.0, fill=Wt)                          # serving hatch
    k.shape([(x + w * 0.08, y + h * 0.88), (x + w * 0.66, y + h * 0.88), (x + w * 0.7, y + h * 0.98), (x + w * 0.04, y + h * 0.98)], lw=0.9, fill=Wt, amp=0)
    for i in range(6): k.line([(x + w * 0.08 + i * w * 0.1, y + h * 0.88), (x + w * 0.1 + i * w * 0.1, y + h * 0.98)], lw=0.4, amp=0)
    for wx in (0.2, 0.8): k.circle(x + w * wx, y + h * 0.15, h * 0.13, lw=1.0, fill=K); k.circle(x + w * wx, y + h * 0.15, h * 0.05, lw=0.4, fill=Wt)
    # cone on the roof
    cx, cy = x + w * 0.4, y + h
    k.shape([(cx - 12, cy + 10), (cx + 12, cy + 10), (cx, cy - 2)], lw=0.9, fill=Wt, amp=0); k.circle(cx, cy + 18, 11, lw=0.9, fill=Wt)
    k.text(x + w * 0.37, y + h * 0.28, "JENNA'S ICES", size=10, font="Ink-Plex")
InkBW.van = _van

def _cabinet(k, x, y, w, h):
    k.rect(x, y, w, h, lw=1.2, fill=Wt); k.rect(x + 8, y + h - 60, w - 16, 52, lw=0.8, fill=Wt)
    k.line([(x + 8, y + h - 8), (x + w - 8, y + h - 60)], lw=0.3, amp=0)
InkBW.cabinet = _cabinet

# ----------------------------------------------------------------------------- 1. hook hero
def _seafront(k, w, h):
    k.sea(14, w - 14, 120, 190, rows=4); k.headland(14, 180, 190, 30); k.lighthouse(80, 210, 50)
    k.stones(14, w - 14, 14, 60, rows=2); k.line([(14, 120), (w - 14, 120)], lw=1.0, amp=0)
def hook_plate(k, w, h): full_open(k, w, h); _seafront(k, w, h); k.van(220, 60, 240); k.unclip()

# ----------------------------------------------------------------------------- 2. cast
CAST = [("DEMELZA", demelza), ("PIP", pip), ("MR NANKERVIS", nankervis)]
cast_plate = B.cast_plate_fn([n for n, _ in CAST], style="cards")

# ----------------------------------------------------------------------------- 3. the museum coin case
def museum_plate(k, w, h):
    plate_open(k, w, h); k.floorboards(w, y=70); k.text(256, 334, "MUSEUM \u00b7 above the post office", size=12, font="Ink-Plex")
    k.cabinet(110, 70, 290, 200)
    for i, (x, y) in enumerate(((160, 220), (210, 230), (330, 222), (360, 236))): k.coin(x, y, 9, crown=bool(i % 2))
    k.text(255, 150, "FOUND ON TIDEWHISTLE BEACH", size=10, font="Ink-Plex")
def bag_part(k, w, h, v):
    part_open(k, w, h); x, y = 268, 214
    k.shape([(x - 18, y), (x + 18, y), (x + 14, y + 26), (x + 4, y + 30), (x - 4, y + 30), (x - 14, y + 26)], lw=1.0, fill=Wt, amp=0.1)
    k.hatch([(x - 18, y), (x + 18, y), (x + 14, y + 26), (x - 14, y + 26)], angle=-50, gap=1.8, lw=0.3, cross=True); k.text(x, y - 14, "6 Spanish coins", size=9, font="Ink-Kalam"); k.unclip()
def gone_part(k, w, h, v): part_open(k, w, h); k.dashed_outline(248, 210, 40, 36); k.text(268, 254, "gone!", size=11, font="Ink-Kalam"); k.unclip()
def zoom_part(k, w, h, v):
    part_open(k, w, h); k.circle(440, 300, 46, lw=1.4, fill=Wt); k.coin(440, 300, 34); k.text(440, 240, "a crown on one side", size=10, font="Ink-Kalam"); k.unclip()
def lid_part(k, w, h, v): part_open(k, w, h); k.shape([(118, 270), (392, 270), (392, 300), (118, 290)], lw=0.9, fill=None, amp=0); k.unclip()

# ----------------------------------------------------------------------------- 4. the van; empty till every night; sealed float every morning
def van_plate(k, w, h): plate_open(k, w, h); _seafront(k, w, h); k.van(160, 60, 240); k.unclip()
def jenna_v(k, w, h, v): part_open(k, w, h); jenna(k, 210, 92, 90); k.unclip()
def clock_part(k, w, h, v): part_open(k, w, h); k.clock_face(450, 300, 24, 10, 0); k.text(450, 264, "10 o'clock", size=10, font="Ink-Kalam"); k.unclip()
def till_empty(k, w, h, v):
    part_open(k, w, h); k.till(420, 120, 70, 56); k.text(455, 100, "emptied every night", size=10, font="Ink-Kalam"); k.unclip()
def float_part(k, w, h, v):
    part_open(k, w, h); x, y = 430, 200
    k.rect(x, y, 50, 36, lw=1.0, fill=Wt); k.line([(x, y + 30), (x + 50, y + 30)], lw=0.8, amp=0)
    for i in range(3): k.circle(x + 12 + i * 13, y + 14, 5, lw=0.6, fill=Wt)
    k.text(x + 25, y + 46, "sealed bag: NEW coins", size=10, font="Ink-Kalam"); k.unclip()

# ----------------------------------------------------------------------------- 5. the tea room: Jenna with the coin on her palm
def tea_plate(k, w, h): plate_open(k, w, h); k.tearoom(w, h, window=True, counter=True); k.unclip()
def jenna_t(k, w, h, v): part_open(k, w, h); jenna(k, 150, 30, 210); k.unclip()
def agnes_t(k, w, h, v): part_open(k, w, h); agnes(k, 390, 30, 200, flip=True); k.unclip()
def palm_coin(k, w, h, v): part_open(k, w, h); k.circle(230, 150, 26, lw=1.2, fill=Wt); k.coin(230, 150, 18); k.text(230, 112, "in my till!", size=11, font="Ink-Kalam"); k.unclip()
def mist_part(k, w, h, v):
    part_open(k, w, h); k.pin_card(250, 300, 150, 44, ["sea mist:", "only 3 customers"], size=11); k.unclip()
def cup_part(k, w, h, v): part_open(k, w, h); k.rect(300, 120, 22, 20, lw=0.9, fill=Wt); k.unclip()

# ----------------------------------------------------------------------------- 6. lineup: how each customer paid (equal tags)
def _p(k, pw, h, what):
    k.stones(14, pw - 14, 14, 50, rows=2); k.van(300, 50, 190)
    k.text(395, 230, what, size=11, font="Ink-Kalam")
lineup_plate = B.lineup_plate_fn([partial(_p, what="lemon sorbet"), partial(_p, what="double mint"), partial(_p, what="vanilla cone")], [n for n, _ in CAST])
PAID = ["tapped her card", "banknote; change OUT", "coins from his pocket IN"]
def ptag(k, w, h, v, i=0):
    part_open(k, w, h); x = i * PW + 270; k.rect(x, 290, 220, 38, lw=1.1, fill=Wt); k.text(x + 110, 301, PAID[i], size=13, font="Ink-Kalam"); k.unclip()

# ----------------------------------------------------------------------------- 7. solution board
def board_plate(k, w, h):
    plate_open(k, w, h); k.floorboards(w, y=60)
    k.case_board(24, 70, 464, 290, title="WHAT WENT INTO THE TILL?")
    k.till(220, 110, 80, 64); k.text(260, 96, "the till", size=11, font="Ink-Plex")
def b_open(k, w, h, v): part_open(k, w, h); k.pin_card(186, 270, 150, 46, ["10:00: only NEW coins", "from the bank"], size=11); k.unclip()
def b_row(k, w, h, v, i=0):
    part_open(k, w, h)
    if i == 0: k.text(90, 220, "DEMELZA", size=11, font="Ink-Plex"); k.text(90, 204, "card: nothing in", size=10, font="Ink-Kalam")
    if i == 1:
        k.text(90, 150, "PIP", size=11, font="Ink-Plex"); k.text(90, 134, "note in, coins OUT", size=10, font="Ink-Kalam")
        k.line([(214, 140), (150, 140)], lw=1.4, amp=0); k.shape([(150, 140), (160, 146), (160, 134)], lw=0.8, fill=K, amp=0)
    if i == 2:
        k.text(420, 160, "MR NANKERVIS", size=11, font="Ink-Plex"); k.text(420, 144, "coins IN, unchecked", size=10, font="Ink-Kalam")
        k.line([(370, 150), (306, 150)], lw=1.4, amp=0); k.shape([(306, 150), (316, 156), (316, 144)], lw=0.8, fill=K, amp=0)
    k.unclip()
def b_ring(k, w, h, v): part_open(k, w, h); k.shape(k.arcpts(420, 156, 70, 24, 0, 360, 30), lw=2.2, fill=None, amp=0.4); k.unclip()

# ----------------------------------------------------------------------------- 8. confession
def conf_plate(k, w, h):
    plate_open(k, w, h); k.floorboards(w, y=70); k.cabinet(220, 70, 260, 180)
    for i in range(6): k.coin(260 + i * 34, 216, 10, crown=True)
    k.unclip()
def nank_c(k, w, h, v): part_open(k, w, h); nankervis(k, 120, 40, 210, expr="sheepish" if "sheepish" in v else "neutral"); k.unclip()
def pocket_part(k, w, h, v): part_open(k, w, h); k.pin_card(150, 320, 140, 40, ["the other five"], size=11); k.unclip()
def card_part(k, w, h, v): part_open(k, w, h); k.pin_card(350, 300, 160, 50, ["the most expensive", "vanilla cone in the Cove"], size=10); k.unclip()

def _vig(k, w, h): k.coin(w / 2, h / 2, w * 0.3)
vignette = B.vignette_fn(_vig)

def jobs():
    J = []
    J.append(dict(name="hook", w=AW, h=AH, plate=hook_plate, seed=2101))
    J.append(dict(name="cast", w=CW, h=CH, plate=cast_plate, seed=2102, parts={
        f"s{i}": dict(fn=B.cast_fig_fn(i, 3, fn), variants=V2) for i, (_, fn) in enumerate(CAST)}))
    J.append(dict(name="museum", w=AW, h=AH, plate=museum_plate, seed=2103, parts=dict(
        bag=dict(fn=bag_part, variants=["base"]), gone=dict(fn=gone_part, variants=["base"]), zoom=dict(fn=zoom_part, variants=["base"]), lid=dict(fn=lid_part, variants=["base"]))))
    J.append(dict(name="van", w=AW, h=AH, plate=van_plate, seed=2104, parts=dict(
        jenna=dict(fn=jenna_v, variants=V2), clock=dict(fn=clock_part, variants=["base"]), till=dict(fn=till_empty, variants=["base"]), float=dict(fn=float_part, variants=["base"]), **B.FX_GULL)))
    J.append(dict(name="tea", w=AW, h=AH, plate=tea_plate, seed=2105, parts=dict(
        jenna=dict(fn=jenna_t, variants=V3), agnes=dict(fn=agnes_t, variants=V3), coin=dict(fn=palm_coin, variants=["base"]), mist=dict(fn=mist_part, variants=["base"]), cup=dict(fn=cup_part, variants=["base"]))))
    J.append(dict(name="lineup", w=3 * PW, h=AH, plate=lineup_plate, seed=2106, parts={
        **{f"s{i}": dict(fn=B.lineup_fig_fn(i, fn, x=PW / 2 - 160, y=50, fh=220), variants=V3) for i, (_, fn) in enumerate(CAST)},
        **{f"p{i}": dict(fn=partial(ptag, i=i), variants=["base"]) for i in range(3)}}))
    J.append(dict(name="board", w=AW, h=AH, plate=board_plate, seed=2107, parts={
        "open": dict(fn=b_open, variants=["base"]), **{f"r{i}": dict(fn=partial(b_row, i=i), variants=["base"]) for i in range(3)}, "ring": dict(fn=b_ring, variants=["base"])}))
    J.append(dict(name="confess", w=AW, h=AH, plate=conf_plate, seed=2108, parts=dict(
        nank=dict(fn=nank_c, variants=["sheepish", "sheepish+blink"]), pocket=dict(fn=pocket_part, variants=["base"]), card=dict(fn=card_part, variants=["base"]))))
    J.append(dict(name="vignette", w=384, h=384, plate=vignette, seed=2109))
    return J

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    J = [j for j in jobs() if not want or j["name"] in want]
    save_layers(OUT, J, B.make_ink)
