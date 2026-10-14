"""Illustrations for Case 28, Truth and Fib Night: BLACK-AND-WHITE ink (bwkit) with the simple v1 peg-doll characters.
The village hall on the first of April with the TRUTH AND FIB NIGHT banner and the rule card (two things in a row = exactly
one true, one fib), Jago's chocolate cake with a sugar fish on the prize table (then gone), four people with equal two-line
speech cards, and a statement board whose tests, X marks and T/F tags appear only after "The Solution".
PART sprites use part_open (clip only, never frame2).
Hook (render.py HOOK_STYLE="cardflip"): borderless hero of the hall stage and the empty cake stand.
Fairness: Hedley, Kerensa, Wenna and Tamsin share stance, height, arms-down pose and neutral face and identical speech cards.
Only the confession shows Tamsin (laughing) non-neutral.
Run: python3 art_case28.py [scene ...]"""
import os, sys
from functools import partial
import bwkit as B
from bwkit import plate_open, part_open, full_open, InkBW, PW, AW, AH, V2, V3, CW, CH
import figures as F
from inkart import K, Wt
from layers import save_layers

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-28" + os.environ.get("TW_ART_SUFFIX", ""))

def hedley(k, x, y, h, **kw): kw.setdefault("chair", False); F.hedley(k, x, y, h, **kw)
def kerensa(k, x, y, h, **kw): B.lady(k, x, y, h, dress="stripe", hair="curls", hat="sun", **kw)
def wenna(k, x, y, h, **kw): kw.setdefault("prop", False); F.wenna(k, x, y, h, **kw)
def tamsin(k, x, y, h, **kw): kw.setdefault("prop", None); kw.setdefault("expr", "neutral"); F.tamsin(k, x, y, h, **kw)
def agnes(k, x, y, h, **kw): kw.setdefault("teapot", False); F.agnes(k, x, y, h, **kw)

def _cake(k, x, y, w, fish=True):
    k.shape(k.arcpts(x, y, w * 0.6, w * 0.08, 0, 360, 20), lw=0.9, fill=Wt, amp=0)
    k.rect(x - w / 2, y + 2, w, w * 0.5, lw=1.1, fill=K)
    k.shape(k.arcpts(x, y + w * 0.52, w / 2, w * 0.1, 0, 360, 20), lw=1.0, fill=K, amp=0)
    for j in range(5): k.circle(x - w * 0.4 + j * w * 0.2, y + w * 0.45, w * 0.03, lw=0, fill=Wt, stroke=False)
    if fish:
        fx, fy = x, y + w * 0.62
        k.shape(k.arcpts(fx, fy, w * 0.14, w * 0.06, 0, 360, 14), lw=0.6, fill=Wt, amp=0)
        k.shape([(fx - w * 0.13, fy), (fx - w * 0.22, fy + w * 0.05), (fx - w * 0.22, fy - w * 0.05)], lw=0.6, fill=Wt, amp=0)
InkBW.choc_cake = _cake

def _hall(k, w, h):
    k.floorboards(w, y=60); k.rect(14, 60, w - 28, 26, lw=1.0, fill=Wt)
    k.rect(110, 230, 292, 34, lw=1.1, fill=Wt); k.text(256, 242, "TRUTH AND FIB NIGHT", size=13, font="Ink-Plex")
    for i in range(10): k.line([(20 + i * 48, 330), (44 + i * 48, 314), (68 + i * 48, 330)], lw=0.6, amp=0.2)

# ----------------------------------------------------------------------------- 1. hook hero
def hook_plate(k, w, h): full_open(k, w, h); _hall(k, w, h); k.rect(206, 86, 100, 50, lw=1.0, fill=Wt); k.dashed_outline(256, 136, 70, 40); k.unclip()

# ----------------------------------------------------------------------------- 2. cast
CAST = [("HEDLEY", hedley), ("KERENSA", kerensa), ("WENNA", wenna), ("TAMSIN", tamsin)]
cast_plate = B.cast_plate_fn([n for n, _ in CAST], style="cards")

# ----------------------------------------------------------------------------- 3. the hall + the rule
def hall_plate(k, w, h): plate_open(k, w, h); _hall(k, w, h); k.unclip()
def april_part(k, w, h, v): part_open(k, w, h); k.pin_card(30, 160, 120, 34, ["1st of April"], size=11); k.unclip()
def rule_part(k, w, h, v): part_open(k, w, h); k.pin_card(150, 110, 212, 64, ["THE RULE: say two things", "in a row = exactly ONE true", "and exactly ONE fib"], size=11); k.unclip()
def agnes_h(k, w, h, v): part_open(k, w, h); agnes(k, 420, 86, 130); k.unclip()

# ----------------------------------------------------------------------------- 4. the prize table: cake, then gone
def table_plate(k, w, h):
    plate_open(k, w, h); _hall(k, w, h); k.rect(150, 86, 212, 60, lw=1.2, fill=Wt); k.text(256, 104, "PRIZE: BEST FIB", size=10, font="Ink-Plex"); k.unclip()
def cake_part(k, w, h, v): part_open(k, w, h); k.choc_cake(256, 150, 80); k.pin_card(370, 160, 120, 40, ["Jago's chocolate", "cake, sugar fish"], size=10); k.unclip()
def gone_part(k, w, h, v): part_open(k, w, h); k.dashed_outline(256, 150, 84, 50); k.pin_card(30, 160, 110, 30, ["vanished!"], size=11); k.unclip()
def four_part(k, w, h, v): part_open(k, w, h); k.pin_card(130, 290, 250, 34, ["4 near the table: exactly ONE took it"], size=10); k.unclip()

# ----------------------------------------------------------------------------- 5. lineup: two-line speech cards
def _p(k, pw, h): k.floorboards(pw, y=50); k.rect(310, 50, 150, 50, lw=1.0, fill=Wt)
lineup_plate = B.lineup_plate_fn([_p, _p, _p, _p], [n for n, _ in CAST])
SAID = [["\u201cI didn't take the cake.", "Kerensa took it.\u201d"], ["\u201cI didn't take the cake.", "Wenna took it.\u201d"],
        ["\u201cI didn't take the cake.", "Hedley took it.\u201d"], ["\u201cI didn't take the cake.", "And it wasn't Wenna.\u201d"]]
def stag(k, w, h, v, i=0):
    part_open(k, w, h); x = i * PW + 236
    k.rect(x, 256, 250, 62, lw=1.1, fill=Wt); k.shape([(x + 10, 266), (x - 14, 246), (x + 26, 256)], lw=1.0, fill=Wt, amp=0)
    for j, ln in enumerate(SAID[i]): k.text(x + 125, 294 - j * 24, ln, size=12, font="Ink-Kalam")
    k.unclip()

# ----------------------------------------------------------------------------- 6. statement board
ROWS = [("HEDLEY", "didn't take it \u00b7 Kerensa took it"), ("KERENSA", "didn't take it \u00b7 Wenna took it"),
        ("WENNA", "didn't take it \u00b7 Hedley took it"), ("TAMSIN", "didn't take it \u00b7 not Wenna")]
RY = [284, 246, 208, 170]
def board_plate(k, w, h): plate_open(k, w, h); k.floorboards(w, y=56); k.case_board(24, 66, 464, 292, title="ONE TRUTH, ONE FIB")
def b_row(k, w, h, v, i=0):
    part_open(k, w, h); y = RY[i]; k.rect(40, y - 8, 340, 30, lw=0.8, fill=Wt)
    k.text(84, y + 2, ROWS[i][0], size=11, font="Ink-Plex"); k.text(250, y + 2, ROWS[i][1], size=10, font="Ink-Kalam"); k.unclip()
def b_innocent(k, w, h, v): part_open(k, w, h); k.pin_card(40, 78, 300, 46, ["innocent = 1st is TRUE,", "so their 2nd must be the FIB"], size=10); k.unclip()
def b_x(k, w, h, v, i=0):
    part_open(k, w, h); y = RY[i]
    for a, b in (((392, y - 6), (424, y + 20)), ((424, y - 6), (392, y + 20))): k.line([a, b], lw=2.2, amp=0.3)
    k.text(452, y + 2, "2 truths", size=8, font="Ink-Kalam"); k.unclip()
def b_tags(k, w, h, v): part_open(k, w, h); k.text(452, RY[3] + 2, "1st FIB", size=8, font="Ink-Kalam"); k.text(452, RY[3] - 10, "2nd TRUE", size=8, font="Ink-Kalam"); k.unclip()
def b_ring(k, w, h, v): part_open(k, w, h); k.shape(k.arcpts(84, RY[3] + 6, 40, 20, 0, 360, 30), lw=2.2, fill=None, amp=0.4); k.pin_card(360, 78, 110, 40, ["Tamsin", "took it"], size=11); k.unclip()

# ----------------------------------------------------------------------------- 7. confession: cake from under the stage
def conf_plate(k, w, h): plate_open(k, w, h); _hall(k, w, h); k.unclip()
def tam_c(k, w, h, v): part_open(k, w, h); tamsin(k, 150, 86, 190, expr="smile" if "sheepish" in v else "neutral"); k.unclip()
def cake_c(k, w, h, v): part_open(k, w, h); k.choc_cake(280, 160, 70); k.text(280, 140, "from under the stage", size=9, font="Ink-Kalam"); k.unclip()
def best_part(k, w, h, v): part_open(k, w, h); k.pin_card(330, 170, 160, 40, ["\u201cthe best fib", "of the night!\u201d"], size=10); k.unclip()
def share_part(k, w, h, v): part_open(k, w, h); k.pin_card(330, 110, 160, 40, ["shared with", "everyone in the hall"], size=10); k.unclip()

def _vig(k, w, h): k.choc_cake(w / 2, h * 0.3, w * 0.45)
vignette = B.vignette_fn(_vig)

def jobs():
    J = []
    J.append(dict(name="hook", w=AW, h=AH, plate=hook_plate, seed=2801))
    J.append(dict(name="cast", w=CW, h=CH, plate=cast_plate, seed=2802, parts={
        f"s{i}": dict(fn=B.cast_fig_fn(i, 4, fn), variants=V2) for i, (_, fn) in enumerate(CAST)}))
    J.append(dict(name="hall", w=AW, h=AH, plate=hall_plate, seed=2803, parts=dict(
        april=dict(fn=april_part, variants=["base"]), rule=dict(fn=rule_part, variants=["base"]), agnes=dict(fn=agnes_h, variants=V3))))
    J.append(dict(name="table", w=AW, h=AH, plate=table_plate, seed=2804, parts=dict(
        cake=dict(fn=cake_part, variants=["base"]), gone=dict(fn=gone_part, variants=["base"]), four=dict(fn=four_part, variants=["base"]))))
    J.append(dict(name="lineup", w=4 * PW, h=AH, plate=lineup_plate, seed=2805, parts={
        **{f"s{i}": dict(fn=B.lineup_fig_fn(i, fn), variants=V3) for i, (_, fn) in enumerate(CAST)},
        **{f"p{i}": dict(fn=partial(stag, i=i), variants=["base"]) for i in range(4)}}))
    J.append(dict(name="board", w=AW, h=AH, plate=board_plate, seed=2806, parts={
        **{f"r{i}": dict(fn=partial(b_row, i=i), variants=["base"]) for i in range(4)},
        **{f"x{i}": dict(fn=partial(b_x, i=i), variants=["base"]) for i in range(3)},
        "inn": dict(fn=b_innocent, variants=["base"]), "tags": dict(fn=b_tags, variants=["base"]), "ring": dict(fn=b_ring, variants=["base"])}))
    J.append(dict(name="confess", w=AW, h=AH, plate=conf_plate, seed=2807, parts=dict(
        tam=dict(fn=tam_c, variants=["sheepish", "sheepish+blink"]), cake=dict(fn=cake_c, variants=["base"]),
        best=dict(fn=best_part, variants=["base"]), share=dict(fn=share_part, variants=["base"]))))
    J.append(dict(name="vignette", w=384, h=384, plate=vignette, seed=2808))
    return J

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    J = [j for j in jobs() if not want or j["name"] in want]
    save_layers(OUT, J, B.make_ink)
