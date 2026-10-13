"""Illustrations for Case 26, The Winning Ticket: BLACK-AND-WHITE ink (bwkit) with the simple v1 peg-doll characters.
The summer fair's giant hamper, Loveday's single raffle ticket in her basket, the tea-stall queue of five (drawn as plain
anonymous outlines so the order is never given away), the gust that lifts the ticket, the vicar's draw, four suspects
with equal nameplates, Agnes's four clue cards, and a "THE QUEUE" board with five numbered places (FRONT = 1, on the left)
that is filled in only after "The Solution".
PART sprites use part_open (clip only, never frame2).
Hook (render.py HOOK_STYLE="queueslots"): borderless hero of the tea stall and the hamper.
Fairness: Mr Fenwick, Pip, Demelza and Hedley share one stance, height, arms-down pose and neutral face; nobody is placed in
the queue before "The Solution". Only the confession shows Demelza pink.
Run: python3 art_case26.py [scene ...]"""
import os, sys, math
from functools import partial
import bwkit as B
from bwkit import plate_open, part_open, full_open, InkBW, PW, AW, AH, V2, V3, CW, CH
import figures as F
from inkart import K, Wt
from layers import save_layers

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-26")

def fenwick(k, x, y, h, **kw): B.visitor(k, x, y, h, suit="dark", hat="cap", tie=False, moustache=True, **kw)
def pip(k, x, y, h, **kw): kw.setdefault("prop", False); F.pip(k, x, y, h, **kw)
def demelza(k, x, y, h, **kw): kw.setdefault("prop", False); F.demelza(k, x, y, h, **kw)
def hedley(k, x, y, h, **kw): kw.setdefault("chair", False); F.hedley(k, x, y, h, **kw)
def loveday(k, x, y, h, **kw): kw.setdefault("jug_", False); F.loveday(k, x, y, h, **kw)
def agnes(k, x, y, h, **kw): kw.setdefault("teapot", True); F.agnes(k, x, y, h, **kw)

def _ticket(k, x, y, s, ang=0, num=True):
    a = math.radians(ang); ca, sa = math.cos(a), math.sin(a); R = lambda u, v: (x + u * ca - v * sa, y + u * sa + v * ca)
    pts = [R(-s / 2, -s * 0.25), R(s / 2, -s * 0.25), R(s / 2, s * 0.25), R(-s / 2, s * 0.25)]
    k.shape(pts, lw=0.9, fill=Wt, amp=0); k.line([R(s * 0.22, -s * 0.25), R(s * 0.22, s * 0.25)], lw=0.4, amp=0)
    if num: k.text(*R(-s * 0.12, -s * 0.06), "No. 47", size=max(5, s * 0.16), font="Ink-Plex")
InkBW.ticket = _ticket

def _hamper(k, x, y, w):
    h = w * 0.55; k.rect(x - w / 2, y, w, h, lw=1.3, fill=Wt)
    for j in range(1, 6): k.line([(x - w / 2, y + j * h / 6), (x + w / 2, y + j * h / 6)], lw=0.4, amp=0.1)
    for j in range(1, 10): k.line([(x - w / 2 + j * w / 10, y), (x - w / 2 + j * w / 10, y + h)], lw=0.3, amp=0.1)
    k.shape(k.arcpts(x, y + h, w * 0.4, h * 0.5, 0, 180, 18), lw=1.4, fill=None, amp=0)
    k.shape([(x - w * 0.1, y + h * 0.4), (x + w * 0.1, y + h * 0.4), (x, y + h * 0.6)], lw=0.8, fill=Wt, amp=0)
InkBW.big_hamper = _hamper

def _anon(k, x, y, h):
    """Plain anonymous queue outline: no face, no clothes detail (never reveals who stood where)."""
    k.circle(x, y + h * 0.86, h * 0.11, lw=0.9, fill=Wt)
    k.shape([(x - h * 0.13, y + h * 0.18), (x + h * 0.13, y + h * 0.18), (x + h * 0.09, y + h * 0.72), (x - h * 0.09, y + h * 0.72)], lw=0.9, fill=Wt, amp=0)
    for lx in (-0.05, 0.05): k.line([(x + h * lx, y + h * 0.18), (x + h * lx, y)], lw=0.9, amp=0)
InkBW.anon = _anon

def _stall(k, x, y, w):
    k.rect(x, y, w, 70, lw=1.2, fill=Wt); k.text(x + w / 2, y + 30, "TEAS", size=14, font="Ink-Plex")
    k.shape([(x - 10, y + 130), (x + w + 10, y + 130), (x + w, y + 110), (x, y + 110)], lw=1.0, fill=Wt, amp=0)
    for j in range(6): k.line([(x + j * w / 5, y + 110), (x + j * w / 5 + 4, y + 130)], lw=0.5, amp=0)
    k.line([(x + 4, y + 70), (x + 4, y + 110)], lw=1.0, amp=0); k.line([(x + w - 4, y + 70), (x + w - 4, y + 110)], lw=1.0, amp=0)

QX = [120, 180, 240, 300, 360]   # queue places 1..5 (front at the stall on the left)

# ----------------------------------------------------------------------------- 1. hook hero
def hook_plate(k, w, h): full_open(k, w, h); k.line([(14, 60), (w - 14, 60)], lw=0.9, amp=0.1); _stall(k, 20, 60, 80); [k.anon(x, 60, 110) for x in QX]; k.big_hamper(440, 60, 90); k.unclip()

# ----------------------------------------------------------------------------- 2. cast
CAST = [("MR FENWICK", fenwick), ("PIP", pip), ("DEMELZA", demelza), ("HEDLEY", hedley)]
cast_plate = B.cast_plate_fn([n for n, _ in CAST], style="tags")

# ----------------------------------------------------------------------------- 3. the fair: hamper, Loveday's ticket
def fair_plate(k, w, h):
    plate_open(k, w, h); k.line([(14, 60), (w - 14, 60)], lw=0.9, amp=0.1)
    for i in range(9): k.line([(30 + i * 52, 340), (56 + i * 52, 322), (82 + i * 52, 340)], lw=0.6, amp=0.2)   # bunting
    k.text(256, 300, "SUMMER FAIR \u00b7 RAFFLE", size=12, font="Ink-Plex"); k.unclip()
def hamper_part(k, w, h, v): part_open(k, w, h); k.big_hamper(370, 60, 170); k.pin_card(300, 220, 150, 30, ["so big it takes two to lift"], size=9); k.unclip()
def lov_f(k, w, h, v): part_open(k, w, h); loveday(k, 130, 40, 200); k.unclip()
def tick_part(k, w, h, v): part_open(k, w, h); k.ticket(110, 250, 50, ang=-10); k.pin_card(20, 290, 160, 30, ["one ticket, top of her basket"], size=9); k.unclip()

# ----------------------------------------------------------------------------- 4. the tea-stall queue (anonymous)
def queue_plate(k, w, h):
    plate_open(k, w, h); k.line([(14, 60), (w - 14, 60)], lw=0.9, amp=0.1); _stall(k, 20, 60, 80)
    for x in QX: k.anon(x, 60, 120)
    k.text(240, 30, "5 people, one behind the other", size=10, font="Ink-Kalam"); k.unclip()
def gust_part(k, w, h, v):
    part_open(k, w, h)
    for y in (240, 270): k.line([(160, y), (230, y + 6), (280, y)], lw=0.8, amp=0.3)
    k.ticket(300, 250, 34, ang=30); k.text(230, 300, "a gust!", size=11, font="Ink-Kalam"); k.unclip()
def ground_part(k, w, h, v): part_open(k, w, h); k.ticket(270, 66, 28, ang=-8); k.unclip()
def behind_part(k, w, h, v): part_open(k, w, h); k.pin_card(300, 290, 190, 46, ["picked up by the person", "DIRECTLY behind her"], size=10); k.unclip()
def draw_part(k, w, h, v): part_open(k, w, h); k.pin_card(300, 220, 190, 46, ["3 o'clock: the winner is", "Loveday's number!"], size=10); k.unclip()
def else_part(k, w, h, v): part_open(k, w, h); k.pin_card(300, 160, 190, 46, ["but somebody ELSE", "claimed the hamper"], size=10); k.unclip()
def pickle_part(k, w, h, v): part_open(k, w, h); k.pin_card(20, 290, 170, 40, ["Loveday: \u201cI was talking", "about Pickle\u2026\u201d"], size=10); k.unclip()

# ----------------------------------------------------------------------------- 5. lineup (4 suspects; Loveday is the victim)
def _p(k, pw, h): k.line([(14, 50), (pw - 14, 50)], lw=0.9, amp=0.1); k.rect(300, 50, 160, 60, lw=0.9, fill=Wt); k.text(380, 74, "TEAS", size=11, font="Ink-Plex")
lineup_plate = B.lineup_plate_fn([_p, _p, _p, _p], [n for n, _ in CAST])

# ----------------------------------------------------------------------------- 6. Agnes's clues at the tea stall
def clues_plate(k, w, h): plate_open(k, w, h); k.line([(14, 60), (w - 14, 60)], lw=0.9, amp=0.1); _stall(k, 300, 60, 180); k.unclip()
def agnes_c(k, w, h, v): part_open(k, w, h); agnes(k, 390, 60, 150); k.unclip()
CL = [["Mr Fenwick:", "the very FRONT"], ["Hedley: somewhere", "behind Pip"], ["Loveday: exactly", "in the MIDDLE"], ["Demelza: not last, not", "next to Mr Fenwick"]]
def clue_part(k, w, h, v, i=0):
    part_open(k, w, h); x, y = ((24, 290), (24, 224), (24, 158), (24, 92))[i]
    k.pin_card(x, y, 200, 50, CL[i], size=11); k.unclip()

# ----------------------------------------------------------------------------- 7. THE QUEUE board
SX = [76, 166, 256, 346, 436]
def board_plate(k, w, h):
    plate_open(k, w, h); k.floorboards(w, y=56); k.case_board(24, 66, 464, 292, title="THE QUEUE")
    k.text(60, 318, "FRONT", size=9, font="Ink-Plex"); k.line([(40, 312), (80, 312)], lw=0.8, amp=0)
    for i, x in enumerate(SX):
        k.rect(x - 38, 220, 76, 76, lw=1.0, fill=Wt); k.text(x, 280, str(i + 1), size=13, font="Ink-Plex")
RULES = ["Fenwick: front", "Hedley: behind Pip", "Loveday: middle", "Demelza: not last, not next to F."]
def rule_part(k, w, h, v, i=0):
    part_open(k, w, h); x, y = ((140, 180), (370, 180), (140, 140), (370, 140))[i]
    k.rect(x - 105, y - 6, 210, 26, lw=0.7, fill=Wt); k.text(x, y + 2, RULES[i], size=10, font="Ink-Kalam"); k.unclip()
def slot_part(k, w, h, v, i=0, name=""):
    part_open(k, w, h); x = SX[i]; k.text(x, 238, name, size=11 if len(name) < 8 else 9, font="Ink-Plex"); k.unclip()
def notslot_part(k, w, h, v, i=0):
    part_open(k, w, h); x = SX[i]; k.text(x, 256, "not D.", size=9, font="Ink-Kalam")
    k.line([(x - 30, 228), (x + 30, 292)], lw=1.4, amp=0.2); k.unclip()
def ring_part(k, w, h, v): part_open(k, w, h); k.shape(k.arcpts(SX[3], 258, 46, 46, 0, 360, 30), lw=2.2, fill=None, amp=0.4); k.pin_card(300, 90, 170, 40, ["4th: directly behind", "Loveday = Demelza"], size=10); k.unclip()

# ----------------------------------------------------------------------------- 8. confession: Demelza pink, hamper to Loveday
def conf_plate(k, w, h): plate_open(k, w, h); k.line([(14, 60), (w - 14, 60)], lw=0.9, amp=0.1); _stall(k, 360, 60, 130); k.unclip()
def dem_c(k, w, h, v): part_open(k, w, h); demelza(k, 120, 40, 200, expr="sheepish" if "sheepish" in v else "neutral"); k.unclip()
def lov_c(k, w, h, v): part_open(k, w, h); loveday(k, 300, 40, 200); k.unclip()
def ham_c(k, w, h, v): part_open(k, w, h); k.big_hamper(210, 60, 80); k.unclip()
def thought_part(k, w, h, v): part_open(k, w, h); k.pin_card(20, 300, 200, 40, ["\u201cI thought it was one", "I'd bought and forgotten!\u201d"], size=10); k.unclip()
def share_part(k, w, h, v): part_open(k, w, h); k.pin_card(250, 300, 230, 40, ["handed straight to Loveday:", "shortbread for the whole queue"], size=10); k.unclip()

def _vig(k, w, h): k.ticket(w / 2, h / 2, w * 0.6, ang=-12)
vignette = B.vignette_fn(_vig)

NAMES = {0: "FENWICK", 1: "PIP", 2: "LOVEDAY", 3: "DEMELZA", 4: "HEDLEY"}
def jobs():
    J = []
    J.append(dict(name="hook", w=AW, h=AH, plate=hook_plate, seed=2601))
    J.append(dict(name="cast", w=CW, h=CH, plate=cast_plate, seed=2602, parts={
        f"s{i}": dict(fn=B.cast_fig_fn(i, 4, fn), variants=V2) for i, (_, fn) in enumerate(CAST)}))
    J.append(dict(name="fair", w=AW, h=AH, plate=fair_plate, seed=2603, parts=dict(
        hamper=dict(fn=hamper_part, variants=["base"]), loveday=dict(fn=lov_f, variants=V2), ticket=dict(fn=tick_part, variants=["base"]))))
    J.append(dict(name="queue", w=AW, h=AH, plate=queue_plate, seed=2604, parts=dict(
        gust=dict(fn=gust_part, variants=["base"]), ground=dict(fn=ground_part, variants=["base"]), behind=dict(fn=behind_part, variants=["base"]),
        draw=dict(fn=draw_part, variants=["base"]), other=dict(fn=else_part, variants=["base"]), pickle=dict(fn=pickle_part, variants=["base"]))))
    J.append(dict(name="lineup", w=4 * PW, h=AH, plate=lineup_plate, seed=2605, parts={
        f"s{i}": dict(fn=B.lineup_fig_fn(i, fn), variants=V3) for i, (_, fn) in enumerate(CAST)}))
    J.append(dict(name="clues", w=AW, h=AH, plate=clues_plate, seed=2606, parts={
        "agnes": dict(fn=agnes_c, variants=V3), **{f"c{i}": dict(fn=partial(clue_part, i=i), variants=["base"]) for i in range(4)}}))
    J.append(dict(name="board", w=AW, h=AH, plate=board_plate, seed=2607, parts={
        **{f"r{i}": dict(fn=partial(rule_part, i=i), variants=["base"]) for i in range(4)},
        **{f"q{i}": dict(fn=partial(slot_part, i=i, name=NAMES[i]), variants=["base"]) for i in range(5)},
        "x5": dict(fn=partial(notslot_part, i=4), variants=["base"]), "x2": dict(fn=partial(notslot_part, i=1), variants=["base"]),
        "ring": dict(fn=ring_part, variants=["base"])}))
    J.append(dict(name="confess", w=AW, h=AH, plate=conf_plate, seed=2608, parts=dict(
        dem=dict(fn=dem_c, variants=["sheepish", "sheepish+blink"]), lov=dict(fn=lov_c, variants=V2), ham=dict(fn=ham_c, variants=["base"]),
        thought=dict(fn=thought_part, variants=["base"]), share=dict(fn=share_part, variants=["base"]))))
    J.append(dict(name="vignette", w=384, h=384, plate=vignette, seed=2609))
    return J

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    J = [j for j in jobs() if not want or j["name"] in want]
    save_layers(OUT, J, B.make_ink)
