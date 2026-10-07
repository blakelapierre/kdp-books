"""Illustrations for Case 14, The Blue Ribbon Key: BLACK-AND-WHITE ink (bwkit) with the simple v1 peg-doll characters.
The village hall's spare key on a short ribbon under the terracotta pot; the raffle hamper vanishes from the locked hall.
(B&W: the "blue" ribbon is drawn as a hatched ribbon.) PART sprites use part_open (clip only, never frame2).
Hook (render.py HOOK_STYLE="keyhole"): borderless hero of the hall's front door and the plant pot, seen through an
opening keyhole. Fairness: Demelza, Pip and Mr Spargo share one stance, height, arms-down pose and neutral face in the
cast strip and the lineup; only the confession shows Mr Spargo sheepish.   Run: python3 art_case14.py [scene ...]"""
import os, sys, math
from functools import partial
import bwkit as B
from bwkit import plate_open, part_open, full_open, InkBW, nameplate, PW, AW, AH, V2, V3, CW, CH
import figures as F
from inkart import K, Wt
from layers import save_layers

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-14")

def demelza(k, x, y, h, **kw): kw.setdefault("prop", False); F.demelza(k, x, y, h, **kw)
def pip(k, x, y, h, **kw): kw.setdefault("prop", False); F.pip(k, x, y, h, **kw)
def spargo(k, x, y, h, **kw): B.visitor(k, x, y, h, suit="check", hat="bowler", tie=True, moustache=True, **kw)
def ollie(k, x, y, h, **kw): F.ollie(k, x, y, h, **kw)
def agnes(k, x, y, h, **kw): kw.setdefault("teapot", False); F.agnes(k, x, y, h, **kw)

# ----------------------------------------------------------------------------- props
def _pot(k, x, y, w):
    """Big terracotta plant pot (hatched) with a leafy plant (x, y = base centre)."""
    body = [(x - w * 0.36, y), (x + w * 0.36, y), (x + w * 0.5, y + w * 0.7), (x - w * 0.5, y + w * 0.7)]
    k.shape(body, lw=1.2, fill=Wt, amp=0.1); k.hatch(body, angle=60, gap=2.4, lw=0.3)
    k.rect(x - w * 0.55, y + w * 0.7, w * 1.1, w * 0.12, lw=1.1, fill=Wt)
    for a in range(-60, 61, 24):
        r = math.radians(90 + a); L = w * (0.7 + 0.15 * math.cos(math.radians(a * 2)))
        tip = (x + L * math.cos(r), y + w * 0.82 + L * math.sin(r))
        k.shape([(x, y + w * 0.82), (tip[0] - w * 0.07, (y + w * 0.82 + tip[1]) / 2), tip, (tip[0] + w * 0.07, (y + w * 0.82 + tip[1]) / 2)], lw=0.7, fill=Wt, amp=0.1)
InkBW.pot = _pot

def _key(k, x, y, s, ribbon=True):
    """Spare key lying flat with a short ribbon loop through the bow (x, y = bow centre)."""
    k.circle(x, y, s * 0.18, lw=1.0, fill=Wt); k.circle(x, y, s * 0.07, lw=0.6, fill=Wt)
    k.rect(x + s * 0.17, y - s * 0.04, s * 0.6, s * 0.08, lw=0.9, fill=Wt)
    for dx in (0.6, 0.7): k.rect(x + s * dx, y - s * 0.16, s * 0.06, s * 0.12, lw=0.8, fill=Wt)
    if ribbon:
        rb = [(x - s * 0.12, y + s * 0.08), (x - s * 0.55, y + s * 0.3), (x - s * 0.6, y + s * 0.18), (x - s * 0.62, y - s * 0.1), (x - s * 0.5, y - s * 0.16), (x - s * 0.1, y - s * 0.06)]
        k.shape(rb, lw=0.8, fill=Wt, amp=0.1); k.hatch(rb, angle=45, gap=1.4, lw=0.35, cross=True)
InkBW.key = _key

def _hamper(k, x, y, w, lid=True):
    k.rect(x - w / 2, y, w, w * 0.55, lw=1.2, fill=Wt)
    for i in range(1, 6): k.line([(x - w / 2, y + w * 0.55 * i / 6), (x + w / 2, y + w * 0.55 * i / 6)], lw=0.35, amp=0)
    for i in range(1, 10): k.line([(x - w / 2 + w * i / 10, y), (x - w / 2 + w * i / 10, y + w * 0.55)], lw=0.25, amp=0)
    if lid: k.rect(x - w / 2 - 3, y + w * 0.55, w + 6, w * 0.1, lw=1.1, fill=Wt)
    k.c.setStrokeColor(K); k.c.setLineWidth(1.2); k.c.arc(x - w * 0.3, y + w * 0.45, x + w * 0.3, y + w * 1.0, 0, 180)
InkBW.hamper = _hamper

def hall_front(k, w, h, pot=True, key=False):
    """The village hall front: brick-ish wall, big double door, notice board, the terracotta pot at the door."""
    k.floorboards(w, y=60, n=4)
    for yy in range(60, int(h) - 14, 16):
        k.line([(14, yy), (w - 14, yy)], lw=0.25, amp=0)
    k.rect(170, 60, 170, 250, lw=1.4, fill=Wt); k.line([(255, 60), (255, 310)], lw=1.0, amp=0)
    k.circle(245, 180, 3, lw=0.6, fill=K); k.circle(265, 180, 3, lw=0.6, fill=K)
    k.rect(240, 196, 10, 16, lw=0.7, fill=Wt)
    k.shape([(150, 310), (360, 310), (255, 360)], lw=1.2, fill=Wt, amp=0); k.text(255, 322, "VILLAGE HALL", size=10, font="Ink-Plex")
    k.rect(40, 150, 100, 110, lw=1.0, fill=Wt); k.text(90, 240, "NOTICES", size=9, font="Ink-Plex")
    k.pin_card(52, 170, 76, 50, ["SUMMER", "FAIR"], size=9, rot=-3)
    k.rect(400, 120, 80, 110, lw=1.0, fill=Wt); k.line([(440, 120), (440, 230)], lw=0.6, amp=0); k.line([(400, 175), (480, 175)], lw=0.6, amp=0)
    if key: k.key(375, 66, 34)
    if pot: k.pot(380, 60, 70)

def hall_inside(k, w, h, hamper=True):
    k.floorboards(w, y=90)
    k.rect(14, 90, w - 28, 26, lw=0.7, fill=Wt)
    for i in range(6): k.shape([(40 + i * 80, 330), (80 + i * 80, 330), (60 + i * 80, 300)], lw=0.6, fill=Wt, amp=0)   # bunting
    k.line([(20, 330), (w - 20, 330)], lw=0.6, amp=0.3)
    k.rect(180, 60, 220, 8, lw=1.0, fill=Wt); k.rect(190, 14, 6, 46, lw=0.8, fill=Wt); k.rect(384, 14, 6, 46, lw=0.8, fill=Wt)
    k.rect(220, 190, 140, 34, lw=1.0, fill=Wt); k.text(290, 202, "GRAND RAFFLE", size=11, font="Ink-Plex")
    if hamper: k.hamper(290, 68, 90)
    k.rect(40, 14, 80, 210, lw=1.2, fill=Wt); k.rect(70, 110, 10, 16, lw=0.7, fill=Wt)        # side door
    k.window_view(420, 200, 70, 90, view="night")

# ----------------------------------------------------------------------------- 1. hook hero
def hook_plate(k, w, h): full_open(k, w, h); hall_front(k, w, h, pot=True); k.unclip()

# ----------------------------------------------------------------------------- 2. cast
CAST = [("DEMELZA ROWE", demelza), ("PIP CAREW", pip), ("MR SPARGO", spargo)]
cast_plate = B.cast_plate_fn([n for n, _ in CAST], style="tags")

# ----------------------------------------------------------------------------- 3. the hidden key
def front_plate(k, w, h): plate_open(k, w, h); hall_front(k, w, h, pot=False); k.unclip()
def pot_part(k, w, h, v): part_open(k, w, h); k.pot(380, 60, 70); k.unclip()
def key_part(k, w, h, v): part_open(k, w, h); k.key(375, 66, 34); k.unclip()
def committee_part(k, w, h, v): part_open(k, w, h); k.pin_card(392, 250, 96, 54, ["HALL", "COMMITTEE", "ONLY"], size=9, rot=3); k.unclip()

# ----------------------------------------------------------------------------- 4. the hamper vanishes from the locked hall
def inside_plate(k, w, h): plate_open(k, w, h); hall_inside(k, w, h, hamper=False); k.unclip()
def hamper_part(k, w, h, v): part_open(k, w, h); k.hamper(290, 68, 90); k.unclip()
def gone_part(k, w, h, v): part_open(k, w, h); k.dashed_outline(290, 68, 96, 56); k.text(290, 140, "?", size=22, font="Ink-Playfair"); k.unclip()
def lock_part(k, w, h, v):
    part_open(k, w, h); x, y = 80, 150
    k.rect(x - 16, y - 14, 32, 26, lw=1.2, fill=Wt); k.c.setStrokeColor(K); k.c.setLineWidth(2); k.c.arc(x - 10, y + 2, x + 10, y + 24, 0, 180)
    k.circle(x, y, 3, lw=0.6, fill=K); k.text(x, y - 34, "locked", size=11, font="Ink-Kalam"); k.unclip()

# ----------------------------------------------------------------------------- 5. Ollie lifts the pot
def ollie_front(k, w, h, v): part_open(k, w, h); ollie(k, 300, 40, 220); k.unclip()

# ----------------------------------------------------------------------------- 6. lineup: sister's supper / home / tombola
def _sister(k, pw, h):
    k.floorboards(pw, y=96); k.window_view(60, 200, 110, 100, view="night")
    k.table_cloth(380, 14, 120, 60); k.teapot(370, 74, 24); k.cup(405, 74, 11); k.text(380, 300, "her sister's", size=11, font="Ink-Kalam")
def _home(k, pw, h):
    k.floorboards(pw, y=96); k.window_view(320, 200, 120, 100, view="night")
    k.clock_face(120, 280, 26, 6, 0); k.text(120, 240, "home at six", size=10, font="Ink-Kalam")
def _tombola(k, pw, h):
    k.floorboards(pw, y=96); k.rect(300, 96, 160, 90, lw=1.0, fill=Wt)
    k.circle(380, 240, 46, lw=1.2, fill=Wt); k.line([(334, 240), (426, 240)], lw=0.6, amp=0); k.line([(380, 194), (380, 286)], lw=0.6, amp=0)
    k.line([(426, 240), (450, 262)], lw=1.0, amp=0); k.text(380, 112, "TOMBOLA", size=12, font="Ink-Plex")
lineup_plate = B.lineup_plate_fn([_sister, _home, _tombola], [n for n, _ in CAST])

# ----------------------------------------------------------------------------- 7. Mr Spargo's statement
def spargo_plate(k, w, h): plate_open(k, w, h); hall_inside(k, w, h, hamper=False); k.unclip()
def spargo_talk(k, w, h, v): part_open(k, w, h); spargo(k, 130, 30, 230); k.unclip()
def ollie_l(k, w, h, v): part_open(k, w, h); ollie(k, 300, 30, 220, flip=True); k.unclip()
def agnes_l(k, w, h, v): part_open(k, w, h); agnes(k, 420, 30, 200, flip=True); k.unclip()

# ----------------------------------------------------------------------------- 8. solution board
def board_plate(k, w, h):
    plate_open(k, w, h); k.floorboards(w)
    k.case_board(40, 110, 432, 250, title="WHAT WAS SAID?")
    k.pin_card(60, 230, 160, 96, ["OLLIE SAID:", "\u201cthe spare key", "is still there\u201d"], size=12, rot=-2)
    k.pin_card(270, 230, 180, 96, ["MR SPARGO:", "\u201cI never knew it existed\u2026", "a key on a blue ribbon\u201d"], size=12, rot=2)
    k.unclip()
def ring_part(k, w, h, v): part_open(k, w, h); k.shape(k.arcpts(398, 282, 40, 12, 0, 360, 36), lw=2.0, fill=None, amp=0.4); k.unclip()
def nobody_part(k, w, h, v): part_open(k, w, h); k.pin_card(70, 130, 160, 66, ["nobody mentioned", "the ribbon"], size=12, rot=-3); k.unclip()
def only_part(k, w, h, v):
    part_open(k, w, h); k.pin_card(270, 126, 180, 76, ["who knows the ribbon?", "the committee\u2026 or", "whoever used the key"], size=11, rot=2); k.unclip()

# ----------------------------------------------------------------------------- 9. confession: the hamper back, one jam short
def confess_plate(k, w, h): plate_open(k, w, h); hall_inside(k, w, h, hamper=False); k.unclip()
def spargo_conf(k, w, h, v): part_open(k, w, h); spargo(k, 400, 30, 220, expr="sheepish" if "sheepish" in v else "neutral"); k.unclip()
def ollie_conf(k, w, h, v): part_open(k, w, h); ollie(k, 150, 30, 210); k.unclip()
def hamper_back(k, w, h, v): part_open(k, w, h); k.hamper(290, 68, 90); k.unclip()
def jam_part(k, w, h, v):
    part_open(k, w, h); k.rect(300, 200, 28, 34, lw=1.0, fill=Wt); k.rect(298, 234, 32, 8, lw=0.9, fill=K)
    k.line([(292, 196), (336, 246)], lw=2, amp=0.2); k.text(314, 252, "\u2212 1 jam", size=11, font="Ink-Kalam"); k.unclip()
def tickets_part(k, w, h, v):
    part_open(k, w, h)
    for i in range(4): k.rect(160 + i * 6, 150 - i * 5, 60, 30, lw=0.8, fill=Wt)
    k.text(202, 136, "RAFFLE", size=9, font="Ink-Plex"); k.unclip()

def _vig(k, w, h):
    k.pot(w * 0.35, h * 0.18, 120); k.key(w * 0.62, h * 0.22, 80)
vignette = B.vignette_fn(_vig)

def jobs():
    J = []
    J.append(dict(name="hook", w=AW, h=AH, plate=hook_plate, seed=1401))
    J.append(dict(name="cast", w=CW, h=CH, plate=cast_plate, seed=1402, parts={
        f"s{i}": dict(fn=B.cast_fig_fn(i, 3, fn), variants=V2) for i, (_, fn) in enumerate(CAST)}))
    J.append(dict(name="front", w=AW, h=AH, plate=front_plate, seed=1403, parts=dict(
        key=dict(fn=key_part, variants=["base"]), pot=dict(fn=pot_part, variants=["base"]),
        committee=dict(fn=committee_part, variants=["base"]), ollie=dict(fn=ollie_front, variants=V2))))
    J.append(dict(name="inside", w=AW, h=AH, plate=inside_plate, seed=1404, parts=dict(
        hamper=dict(fn=hamper_part, variants=["base"]), gone=dict(fn=gone_part, variants=["base"]), lock=dict(fn=lock_part, variants=["base"]))))
    J.append(dict(name="lineup", w=3 * PW, h=AH, plate=lineup_plate, seed=1405, parts={
        f"s{i}": dict(fn=B.lineup_fig_fn(i, fn), variants=V3) for i, (_, fn) in enumerate(CAST)}))
    J.append(dict(name="spargo", w=AW, h=AH, plate=spargo_plate, seed=1406, parts=dict(
        spargo=dict(fn=spargo_talk, variants=V3), ollie=dict(fn=ollie_l, variants=V2), agnes=dict(fn=agnes_l, variants=V2))))
    J.append(dict(name="board", w=AW, h=AH, plate=board_plate, seed=1407, parts=dict(
        ring=dict(fn=ring_part, variants=["base"]), nobody=dict(fn=nobody_part, variants=["base"]), only=dict(fn=only_part, variants=["base"]))))
    J.append(dict(name="confess", w=AW, h=AH, plate=confess_plate, seed=1408, parts=dict(
        spargo=dict(fn=spargo_conf, variants=["sheepish", "sheepish+blink"]), ollie=dict(fn=ollie_conf, variants=V2),
        hamper=dict(fn=hamper_back, variants=["base"]), jam=dict(fn=jam_part, variants=["base"]), tickets=dict(fn=tickets_part, variants=["base"]))))
    J.append(dict(name="vignette", w=384, h=384, plate=vignette, seed=1409))
    return J

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    J = [j for j in jobs() if not want or j["name"] in want]
    save_layers(OUT, J, B.make_ink)
