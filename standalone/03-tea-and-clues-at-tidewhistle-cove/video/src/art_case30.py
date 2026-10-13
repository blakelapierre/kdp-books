"""Illustrations for Case 30, The Missing Sign (LAST CASE): BLACK-AND-WHITE ink (bwkit) with the simple v1 peg-doll characters.
The Kettle and Gull front door on its tenth birthday with an EMPTY iron bracket, a brown paper bag of four brass bolts on the
doorstep marked "Back soon" in green ink (drawn as heavy ink lettering + "GREEN INK" label in B&W), three suspects with equal
"how they write" tags (pencil / blue fountain pen / fat green pen), the village hall lit early, a "WHO WRITES IN GREEN?" board,
and the finale: the repainted sign back up, "Ten years of tea and clues".
PART sprites use part_open (clip only, never frame2).
Hook (render.py HOOK_STYLE="emptybracket"): borderless hero of the shopfront with the empty bracket.
Fairness: Hedley, Tamsin and Ollie share stance, height, arms-down pose and neutral faces; equal tags. Only the finale shows
smiles. Run: python3 art_case30.py [scene ...]"""
import os, sys
from functools import partial
import bwkit as B
from bwkit import plate_open, part_open, full_open, InkBW, PW, AW, AH, V2, V3, CW, CH
import figures as F
from inkart import K, Wt
from layers import save_layers

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-30")

def hedley(k, x, y, h, **kw): kw.setdefault("chair", False); F.hedley(k, x, y, h, **kw)
def tamsin(k, x, y, h, **kw): kw.setdefault("prop", None); kw.setdefault("expr", "neutral"); F.tamsin(k, x, y, h, **kw)
def ollie(k, x, y, h, **kw): kw.setdefault("expr", "neutral"); F.ollie(k, x, y, h, **kw)
def agnes(k, x, y, h, **kw): kw.setdefault("teapot", False); F.agnes(k, x, y, h, **kw)

def _front(k, w, h):
    k.stones(0, w, 0, 50, rows=2)
    k.rect(60, 50, 330, 250, lw=1.4, fill=Wt); k.rect(180, 50, 90, 170, lw=1.2, fill=Wt); k.rect(80, 120, 80, 90, lw=1.0, fill=Wt); k.rect(290, 120, 80, 90, lw=1.0, fill=Wt)
    k.text(225, 260, "THE KETTLE AND GULL", size=12, font="Ink-Plex")
    k.line([(390, 290), (450, 290)], lw=2.4, amp=0); k.line([(400, 290), (390, 270)], lw=1.6, amp=0)   # iron bracket
def _sign(k, x, y, s=1.0, under=False):
    k.line([(x + 10, y), (x + 10, y - 12)], lw=1.0, amp=0); k.line([(x + 60, y), (x + 60, y - 12)], lw=1.0, amp=0)
    k.rect(x - 5, y - 70 * s, 80 * s, 58 * s, lw=1.3, fill=Wt); k.text(x + 35 * s, y - 40 * s, "\u2615 \u2708", size=int(14 * s), font="Ink-Plex")
    if under: k.text(x + 35 * s, y - 64 * s, "10 yrs of tea & clues", size=5, font="Ink-Kalam")
def _bag(k, x, y, s=1.0, label=True):
    k.rect(x, y, 50 * s, 44 * s, lw=1.1, fill=Wt); k.line([(x, y + 44 * s), (x + 8 * s, y + 52 * s), (x + 42 * s, y + 52 * s), (x + 50 * s, y + 44 * s)], lw=1.0, amp=0)
    if label: k.text(x + 25 * s, y + 22 * s, "Back soon", size=int(9 * s), font="Ink-Kalam")

# ----------------------------------------------------------------------------- 1. hook hero
def hook_plate(k, w, h): full_open(k, w, h); _front(k, w, h); _bag(k, 196, 50); k.unclip()

CAST = [("HEDLEY TRUSCOTT", hedley), ("TAMSIN TREVELYAN", tamsin), ("CONSTABLE OLLIE", ollie)]
cast_plate = B.cast_plate_fn([n for n, _ in CAST], style="tags")

# ----------------------------------------------------------------------------- 2. the doorstep
def door_plate(k, w, h): plate_open(k, w, h); _front(k, w, h); k.unclip()
def agnes_d(k, w, h, v): part_open(k, w, h); agnes(k, 225, 50, 160); k.unclip()
def gone_part(k, w, h, v): part_open(k, w, h); k.dashed_outline(395, 210, 70, 60); k.pin_card(40, 320, 200, 30, ["10th birthday: sign GONE"], size=10); k.unclip()
def bracket_part(k, w, h, v): part_open(k, w, h); k.pin_card(300, 320, 190, 40, ["painted sign, 10 years", "on its iron bracket"], size=10); k.unclip()
def bag_part(k, w, h, v): part_open(k, w, h); _bag(k, 300, 52, label=False); k.pin_card(40, 214, 200, 40, ["paper bag on the step:", "the 4 brass bolts"], size=10); k.unclip()
def note_part(k, w, h, v): part_open(k, w, h); _bag(k, 300, 52); k.unclip()
def green_part(k, w, h, v): part_open(k, w, h); k.pin_card(356, 112, 140, 40, ["\u201cBack soon\u201d", "in bright GREEN ink"], size=10); k.unclip()

# ----------------------------------------------------------------------------- 3. lineup with writing tags
def _p(k, pw, h): k.stones(14, pw - 14, 14, 50, rows=2); k.rect(300, 50, 170, 130, lw=1.0, fill=Wt); k.text(385, 150, "HARBOUR ST", size=10, font="Ink-Plex")
lineup_plate = B.lineup_plate_fn([_p, _p, _p], [n for n, _ in CAST])
FX, FY, FH = PW / 2 - 160, 50, 220
TAGS = [["tallest ladder; writes in", "PENCIL, no pen for years"], ["writes the most; only", "BLUE ink, fountain pen"], ["notebook in GREEN ink,", "grandfather's fat pen"]]
def ltag(k, w, h, v, i=0):
    part_open(k, w, h); x = i * PW + 236; k.rect(x, 286, 250, 50, lw=1.1, fill=Wt)
    for j, ln in enumerate(TAGS[i]): k.text(x + 125, 318 - j * 20, ln, size=11, font="Ink-Kalam")
    k.unclip()

# ----------------------------------------------------------------------------- 4. the street: hall lights on
def hall_plate(k, w, h):
    plate_open(k, w, h); k.stones(0, w, 0, 50, rows=2); k.rect(260, 50, 220, 200, lw=1.3, fill=Wt)
    k.shape([(250, 250), (370, 320), (490, 250)], lw=1.3, fill=Wt, amp=0); k.text(370, 262, "VILLAGE HALL", size=11, font="Ink-Plex"); k.rect(345, 50, 50, 90, lw=1.0, fill=Wt); k.unclip()
def lights_part(k, w, h, v):
    part_open(k, w, h)
    for x in (280, 420):
        k.rect(x, 140, 40, 50, lw=1.0, fill=Wt); k.hatch([(x, 140), (x + 40, 140), (x + 40, 190), (x, 190)], angle=45, gap=3, lw=0.4)
    k.pin_card(30, 300, 190, 40, ["lights on, very early,", "Saturday morning"], size=10); k.unclip()

# ----------------------------------------------------------------------------- 5. board
def board_plate(k, w, h): plate_open(k, w, h); k.floorboards(w, y=56); k.case_board(24, 66, 464, 292, title="WHO WRITES IN GREEN?")
def b_note(k, w, h, v): part_open(k, w, h); _bag(k, 60, 250, s=1.2); k.pin_card(150, 262, 160, 40, ["note: GREEN ink"], size=12); k.unclip()
ROWS = ["Hedley: pencil, no pen", "Tamsin: blue only"]
def b_row(k, w, h, v, i=0):
    part_open(k, w, h); x, y = ((140, 200), (370, 200))[i]
    k.text(x, y, ROWS[i], size=11, font="Ink-Kalam"); k.line([(x - 95, y + 4), (x + 95, y + 4)], lw=1.4, amp=0.2); k.unclip()
def b_ring(k, w, h, v): part_open(k, w, h); k.pin_card(150, 110, 210, 46, ["Ollie: green pen,", "whole village knows"], size=12); k.shape(k.arcpts(255, 133, 120, 34, 0, 360, 30), lw=2.2, fill=None, amp=0.4); k.unclip()

# ----------------------------------------------------------------------------- 6. the hall: surprise; 7. finale
def surp_plate(k, w, h): plate_open(k, w, h); k.floorboards(w, y=56); k.rect(40, 200, 430, 120, lw=1.0, fill=Wt); k.text(255, 300, "HAPPY 10th, KETTLE AND GULL", size=12, font="Ink-Plex"); k.unclip()
def ollie_s(k, w, h, v): part_open(k, w, h); ollie(k, 110, 56, 190, expr="smile"); k.unclip()
def crowd_part(k, w, h, v):
    part_open(k, w, h); hedley(k, 250, 56, 170, expr="smile"); tamsin(k, 350, 56, 170, expr="smile"); k.unclip()
def why_part(k, w, h, v): part_open(k, w, h); _sign(k, 400, 200, 1.0); k.pin_card(150, 330, 260, 30, ["borrowed at dawn: a surprise repaint"], size=10); k.unclip()
def final_plate(k, w, h): plate_open(k, w, h); _front(k, w, h); k.unclip()
def sign_part(k, w, h, v): part_open(k, w, h); _sign(k, 395, 290, 1.0, under=True); k.unclip()
def words_part(k, w, h, v): part_open(k, w, h); k.pin_card(40, 320, 230, 34, ["\u201cTen years of tea and clues\u201d"], size=11); k.unclip()
def agnes_f(k, w, h, v): part_open(k, w, h); agnes(k, 225, 50, 160, expr="smile"); k.unclip()

def _vig(k, w, h): _sign(k, w * 0.3, h * 0.75, 2.0, under=True)
vignette = B.vignette_fn(_vig)

def jobs():
    b = ["base"]; J = []
    J.append(dict(name="hook", w=AW, h=AH, plate=hook_plate, seed=3001))
    J.append(dict(name="cast", w=CW, h=CH, plate=cast_plate, seed=3002, parts={
        f"s{i}": dict(fn=B.cast_fig_fn(i, 3, fn), variants=V2) for i, (_, fn) in enumerate(CAST)}))
    J.append(dict(name="door", w=AW, h=AH, plate=door_plate, seed=3003, parts=dict(
        agnes=dict(fn=agnes_d, variants=V3), gone=dict(fn=gone_part, variants=b), bracket=dict(fn=bracket_part, variants=b),
        bag=dict(fn=bag_part, variants=b), note=dict(fn=note_part, variants=b), green=dict(fn=green_part, variants=b))))
    J.append(dict(name="lineup", w=3 * PW, h=AH, plate=lineup_plate, seed=3004, parts={
        **{f"s{i}": dict(fn=B.lineup_fig_fn(i, fn, x=FX, y=FY, fh=FH), variants=V3) for i, (_, fn) in enumerate(CAST)},
        **{f"p{i}": dict(fn=partial(ltag, i=i), variants=b) for i in range(3)}}))
    J.append(dict(name="hall", w=AW, h=AH, plate=hall_plate, seed=3005, parts=dict(lights=dict(fn=lights_part, variants=b))))
    J.append(dict(name="board", w=AW, h=AH, plate=board_plate, seed=3006, parts={
        "note": dict(fn=b_note, variants=b), **{f"r{i}": dict(fn=partial(b_row, i=i), variants=b) for i in range(2)}, "ring": dict(fn=b_ring, variants=b)}))
    J.append(dict(name="surprise", w=AW, h=AH, plate=surp_plate, seed=3007, parts=dict(
        ollie=dict(fn=ollie_s, variants=V2), crowd=dict(fn=crowd_part, variants=b), why=dict(fn=why_part, variants=b))))
    J.append(dict(name="finale", w=AW, h=AH, plate=final_plate, seed=3008, parts=dict(
        sign=dict(fn=sign_part, variants=b), words=dict(fn=words_part, variants=b), agnes=dict(fn=agnes_f, variants=V3))))
    J.append(dict(name="vignette", w=384, h=384, plate=vignette, seed=3009))
    return J

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    J = [j for j in jobs() if not want or j["name"] in want]
    save_layers(OUT, J, B.make_ink)
