"""Illustrations for Case 13, The Misspelled Note: BLACK-AND-WHITE ink (bwkit) with the simple v1 peg-doll characters.
Hedley's hand-painted NO PARKING ON THE PEIR sign; the captain's ship in a bottle replaced by a friendly note.
PART sprites use part_open (clip only, never frame2).
Hook (render.py HOOK_STYLE="redpen"): borderless hero of the harbour office shelf, empty, with the folded note.
Fairness: Tamsin, Jago and Hedley share one stance, height, arms-down pose and neutral face in the cast strip and
the lineup; only the confession shows Hedley sheepish.   Run: python3 art_case13.py [scene ...]"""
import os, sys, math
from functools import partial
import bwkit as B
from bwkit import plate_open, part_open, full_open, InkBW, nameplate, PW, AW, AH, V2, V3, CW, CH
import figures as F
from inkart import K, Wt
from layers import save_layers

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-13")

def tamsin(k, x, y, h, **kw): kw.setdefault("prop", None); F.tamsin(k, x, y, h, **kw)
def jago(k, x, y, h, **kw): kw.setdefault("basket", False); F.jago(k, x, y, h, **kw)
def hedley(k, x, y, h, **kw): B.overalls(k, x, y, h, paint=False, **kw)
def quill(k, x, y, h, **kw): kw.setdefault("prop", False); F.quill(k, x, y, h, **kw)
def agnes(k, x, y, h, **kw): kw.setdefault("teapot", False); F.agnes(k, x, y, h, **kw)

# ----------------------------------------------------------------------------- props
def _bottle_ship(k, x, y, s, lop=False):
    """Ship in a bottle lying on a little stand (x, y = base centre, s = bottle length)."""
    k.rect(x - s * 0.3, y, s * 0.6, s * 0.06, lw=0.8, fill=Wt)
    by = y + s * 0.06 + s * 0.17
    k.shape(k.arcpts(x - s * 0.08, by, s * 0.38, s * 0.17, 0, 360, 30), lw=1.0, fill=Wt, amp=0)
    k.rect(x + s * 0.28, by - s * 0.05, s * 0.16, s * 0.1, lw=0.9, fill=Wt); k.rect(x + s * 0.44, by - s * 0.055, s * 0.05, s * 0.11, lw=0.8, fill=K)
    hx = x - s * 0.1; hy = by - s * 0.09
    k.shape([(hx - s * 0.2, hy + s * 0.03), (hx + s * 0.2, hy + s * 0.03), (hx + s * 0.15, hy - s * 0.03), (hx - s * 0.16, hy - s * 0.03)], lw=0.7, fill=K, amp=0)
    tilt = 0.04 if lop else 0
    for i, mx in enumerate((-0.12, 0.0, 0.12)):
        tx = hx + s * mx; top = hy + s * (0.2 if i == 1 else 0.16)
        k.line([(tx, hy + s * 0.03), (tx + s * tilt, top)], lw=0.6, amp=0)
        k.shape([(tx + s * 0.01, hy + s * 0.06), (tx + s * 0.07, hy + s * 0.07), (tx + s * tilt + s * 0.01, top - s * 0.01)], lw=0.4, fill=Wt, amp=0)
InkBW.bottle_ship = _bottle_ship

def _folded_note(k, x, y, w):
    k.shape([(x - w / 2, y), (x + w / 2, y), (x + w / 2 - w * 0.06, y + w * 0.5), (x - w / 2 + w * 0.06, y + w * 0.5)], lw=0.9, fill=Wt, amp=0)
    k.line([(x - w / 2 + w * 0.03, y + w * 0.25), (x + w / 2 - w * 0.03, y + w * 0.25)], lw=0.5, amp=0)
    for j in range(3): k.line([(x - w * 0.3, y + w * (0.33 + 0.05 * j)), (x + w * 0.25, y + w * (0.33 + 0.05 * j))], lw=0.3, amp=0.3)
InkBW.folded_note = _folded_note

def _painted_sign(k, x, y, w, text="NO PARKING ON THE PEIR"):
    """Hand-painted board on two posts (x, y = ground centre)."""
    for sg in (-1, 1): k.rect(x + sg * w * 0.35 - 3, y, 6, w * 0.32, lw=0.9, fill=Wt)
    k.rect(x - w / 2, y + w * 0.3, w, w * 0.28, lw=1.3, fill=Wt)
    lines = text.split(" ON ")
    k.text(x, y + w * 0.47, lines[0], size=w * 0.085, font="Ink-Plex")
    if len(lines) > 1: k.text(x, y + w * 0.36, "ON " + lines[1], size=w * 0.085, font="Ink-Plex")
InkBW.painted_sign = _painted_sign

def office(k, w, h, ship=True, note=False):
    """Captain Quill's harbour office: plank floor, chart on the wall, porthole window, the shelf."""
    k.floorboards(w, y=90)
    for x in range(14, int(w) - 14, 26): k.line([(x, 90), (x, h - 14)], lw=0.25, amp=0)
    k.circle(410, 270, 46, lw=1.6, fill=Wt); k.circle(410, 270, 38, lw=0.8, fill=None)
    k.c.saveState(); p = k.c.beginPath(); p.circle(410, 270, 37); k.c.clipPath(p, stroke=0, fill=0)
    k.sea(360, 460, 236, 262, rows=3); k.c.restoreState()
    k.rect(50, 220, 120, 100, lw=1.0, fill=Wt); k.text(110, 300, "CHART", size=9, font="Ink-Plex")
    k.line([(60, 240), (100, 280), (150, 250)], lw=0.5, amp=0.4); k.circle(100, 280, 2, lw=0.4, fill=K)
    k.rect(200, 170, 140, 6, lw=1.0, fill=Wt)
    for sx in (210, 330): k.shape([(sx, 170), (sx + 8, 170), (sx + 4, 156)], lw=0.6, fill=Wt, amp=0)
    if ship: k.bottle_ship(270, 176, 110)
    if note: k.folded_note(270, 176, 46)
    k.rect(30, 14, 140, 60, lw=1.0, fill=Wt); k.rect(24, 74, 152, 6, lw=1.0, fill=Wt)          # desk
    k.text(250, 340, "HARBOUR OFFICE", size=10, font="Ink-Plex")

# ----------------------------------------------------------------------------- 1. hook hero
def hook_plate(k, w, h):
    full_open(k, w, h); office(k, w, h, ship=False, note=True)
    k.dashed_outline(270, 182, 118, 40); k.unclip()

# ----------------------------------------------------------------------------- 2. cast
CAST = [("TAMSIN TREVELYAN", tamsin), ("JAGO PENHALLOW", jago), ("HEDLEY TRUSCOTT", hedley)]
cast_plate = B.cast_plate_fn([n for n, _ in CAST], style="frames")

# ----------------------------------------------------------------------------- 3. the sign by the slipway
def sign_plate(k, w, h):
    plate_open(k, w, h); k.harbour(w, h, sea_y0=140, sea_y1=200, wall_top=60, boats=True)
    k.slipway(40, 200, 14, 120); k.painted_sign(330, 40, 230); k.unclip()
def ring_part(k, w, h, v):
    part_open(k, w, h); k.shape(k.arcpts(368, 129, 30, 14, 0, 360, 30), lw=1.8, fill=None, amp=0.4); k.unclip()
def tally_part(k, w, h, v):
    part_open(k, w, h); k.text(330, 214, "corrected: IIII", size=13, font="Ink-Kalam"); k.unclip()

# ----------------------------------------------------------------------------- 4. "I before E, Hedley" / "Looks right to me"
def chat_plate(k, w, h):
    plate_open(k, w, h); k.harbour(w, h, sea_y0=150, sea_y1=210, wall_top=60, boats=False)
    k.painted_sign(256, 40, 170); k.unclip()
def agnes_chat(k, w, h, v): part_open(k, w, h); agnes(k, 100, 30, 210); k.unclip()
def hedley_chat(k, w, h, v): part_open(k, w, h); hedley(k, 410, 30, 220, flip=True); k.unclip()

# ----------------------------------------------------------------------------- 5. the harbour office: ship gone, note left
def office_plate(k, w, h): plate_open(k, w, h); office(k, w, h, ship=False); k.unclip()
def ship_part(k, w, h, v): part_open(k, w, h); k.bottle_ship(270, 176, 110); k.unclip()
def note_part(k, w, h, v): part_open(k, w, h); k.folded_note(270, 176, 46); k.unclip()
def quill_off(k, w, h, v): part_open(k, w, h); quill(k, 120, 30, 200); k.unclip()

# ----------------------------------------------------------------------------- 6. the note close-up
def notepaper(k, x, y, w, hgt, lines, size=15, rot=-2):
    k.c.saveState(); k.c.translate(x + w / 2, y + hgt / 2); k.c.rotate(rot); k.c.translate(-(x + w / 2), -(y + hgt / 2))
    k.rect(x, y, w, hgt, lw=1.1, fill=Wt)
    for yy in range(int(y + 24), int(y + hgt - 10), 26): k.line([(x + 10, yy), (x + w - 10, yy)], lw=0.3, amp=0)
    k.line([(x + 34, y + 6), (x + 34, y + hgt - 6)], lw=0.5, amp=0)
    yy = y + hgt - 44
    for ln in lines: k.text(x + w / 2 + 12, yy, ln, size=size, font="Ink-Kalam"); yy -= 26
    k.c.restoreState()
NOTE = ["Don't worry.", "Your ship will be back", "by the peir at sunset."]
def notec_plate(k, w, h): plate_open(k, w, h); k.floorboards(w, y=h - 14, n=16); notepaper(k, 96, 70, 320, 230, NOTE, size=18); k.unclip()
def peir_ring(k, w, h, v):
    part_open(k, w, h); k.shape(k.arcpts(243, 212, 30, 15, 0, 360, 30), lw=1.8, fill=None, amp=0.4)
    k.text(250, 92, "p \u00b7 e \u00b7 i \u00b7 r", size=13, font="Ink-Kalam"); k.unclip()

# ----------------------------------------------------------------------------- 7. Quill brings the note to the Kettle and Gull
def kettle_plate(k, w, h): plate_open(k, w, h); k.tearoom(w, h, window=True, counter=True); k.unclip()
def quill_k(k, w, h, v): part_open(k, w, h); quill(k, 140, 30, 220, prop=False); k.folded_note(140 + 46, 30 + 100, 22); k.unclip()
def agnes_k(k, w, h, v): part_open(k, w, h); agnes(k, 360, 30, 210, flip=True); k.unclip()

# ----------------------------------------------------------------------------- 8. lineup: book / pasty / floorboard
def _shop(k, pw, h):
    k.floorboards(pw, y=96); k.bookcase(300, 96, 180, 220, shelves=4, seed=3)
def _bakery(k, pw, h):
    k.floorboards(pw, y=96); k.rect(290, 96, 190, 110, lw=1.0, fill=Wt)
    for i in range(5): k.shape(k.arcpts(310 + i * 34, 206, 13, 10, 0, 180, 12), lw=0.7, fill=Wt, amp=0)
    k.text(385, 300, "PENHALLOW'S BAKERY", size=10, font="Ink-Plex")
def _office_floor(k, pw, h):
    k.floorboards(pw, y=96)
    for x in range(14, int(pw) - 14, 26): k.line([(x, 96), (x, h - 14)], lw=0.25, amp=0)
    k.rect(300, 40, 140, 14, lw=0.9, fill=Wt); k.text(370, 22, "loose board", size=10, font="Ink-Kalam")
    k.circle(410, 270, 40, lw=1.4, fill=Wt)
lineup_plate = B.lineup_plate_fn([_shop, _bakery, _office_floor], [n for n, _ in CAST])

# ----------------------------------------------------------------------------- 9. Tamsin's poster, Jago's chalkboard
def spell_plate(k, w, h):
    plate_open(k, w, h); k.street(w, h, y=70) if hasattr(k, "street") else None
    k.unclip()
def poster_part(k, w, h, v):
    part_open(k, w, h); k.rect(40, 120, 200, 210, lw=1.4, fill=Wt); k.rect(48, 128, 184, 194, lw=0.5, fill=None)
    for i, ln in enumerate(("STORY TIME", "ON THE PIER", "SATURDAY")): k.text(140, 280 - i * 40, ln, size=17, font="Ink-Playfair")
    k.text(140, 148, "T. Trevelyan \u00b7 Books", size=10, font="Ink-Kalam"); k.unclip()
def chalk_part(k, w, h, v):
    part_open(k, w, h)
    k.shape([(300, 70), (330, 320), (360, 320), (390, 70)], lw=0, fill=None, amp=0)
    k.line([(300, 70), (330, 320)], lw=1.2, amp=0); k.line([(470, 70), (440, 320)], lw=1.2, amp=0)
    k.rect(296, 150, 178, 170, lw=1.4, fill=K)
    for i, ln in enumerate(("PASTIES", "TWO DOORS FROM", "THE PIER")): k.text(385, 280 - i * 40, ln, size=15, font="Ink-Kalam", color=Wt)
    k.unclip()
def ok_part(k, w, h, v, x=0, y=0):
    part_open(k, w, h); k.line([(x, y), (x + 8, y - 9), (x + 24, y + 12)], lw=2.4, amp=0.2); k.unclip()

# ----------------------------------------------------------------------------- 10. solution board
def board_plate(k, w, h):
    plate_open(k, w, h); k.floorboards(w)
    k.case_board(40, 110, 432, 250, title="WHO SPELLS IT P-E-I-R?")
    k.pin_card(60, 240, 120, 80, ["THE NOTE:", "\u201cby the peir\u201d"], size=12, rot=-3)
    k.pin_card(60, 140, 120, 80, ["HEDLEY'S SIGN:", "\u201cON THE PEIR\u201d"], size=12, rot=2)
    k.pin_card(320, 240, 130, 80, ["TAMSIN'S POSTER:", "\u201cON THE PIER\u201d"], size=12, rot=2)
    k.pin_card(320, 140, 130, 80, ["JAGO'S BOARD:", "\u201cFROM THE PIER\u201d"], size=12, rot=-2)
    k.unclip()
def match_part(k, w, h, v):
    part_open(k, w, h); k.line([(190, 280), (215, 250), (215, 200), (190, 180)], lw=2.2, amp=0.3)
    k.text(250, 228, "same", size=13, font="Ink-Kalam"); k.text(250, 212, "mistake", size=13, font="Ink-Kalam"); k.unclip()
def tick_part(k, w, h, v, y=0):
    part_open(k, w, h); x = 300; k.line([(x, y), (x + 6, y - 7), (x + 18, y + 9)], lw=2.2, amp=0.2); k.unclip()

# ----------------------------------------------------------------------------- 11. confession: the bigger ship for the birthday
def confess_plate(k, w, h): plate_open(k, w, h); office(k, w, h, ship=False); k.unclip()
def hedley_conf(k, w, h, v): part_open(k, w, h); hedley(k, 330, 30, 220, expr="sheepish" if "sheepish" in v else "neutral"); k.unclip()
def quill_conf(k, w, h, v): part_open(k, w, h); quill(k, 130, 30, 210); k.unclip()
def bigship_part(k, w, h, v): part_open(k, w, h); k.bottle_ship(98, 80, 120, lop=True); k.unclip()

# ----------------------------------------------------------------------------- 12. sunset: ship back on the pier; the birthday card
def sunset_plate(k, w, h):
    plate_open(k, w, h); k.harbour(w, h, sea_y0=140, sea_y1=210, wall_top=60, boats=False)
    k.shape(k.arcpts(380, 210, 46, 46, 0, 180, 24), lw=1.0, fill=Wt, amp=0)
    for i in range(7):
        a = math.radians(15 + i * 25); k.line([(380 + 54 * math.cos(a), 210 + 54 * math.sin(a)), (380 + 70 * math.cos(a), 210 + 70 * math.sin(a))], lw=0.7, amp=0)
    k.rect(120, 60, 200, 10, lw=1.0, fill=Wt)
    k.unclip()
def ship_back(k, w, h, v): part_open(k, w, h); k.bottle_ship(220, 70, 100); k.unclip()
def card_part(k, w, h, v):
    part_open(k, w, h); notepaper(k, 250, 190, 230, 160, ["Happy Birthday", "from Hedley,", "Down by the Peir"], size=14, rot=4); k.unclip()

def _vig(k, w, h):
    k.bottle_ship(w / 2, h * 0.28, w * 0.7); k.folded_note(w * 0.7, h * 0.12, 60)
vignette = B.vignette_fn(_vig)

def jobs():
    FX = B.FX_GULL; J = []
    J.append(dict(name="hook", w=AW, h=AH, plate=hook_plate, seed=1301))
    J.append(dict(name="cast", w=CW, h=CH, plate=cast_plate, seed=1302, parts={
        f"s{i}": dict(fn=B.cast_fig_fn(i, 3, fn), variants=V2) for i, (_, fn) in enumerate(CAST)}))
    J.append(dict(name="sign", w=AW, h=AH, plate=sign_plate, seed=1303, parts=dict(
        ring=dict(fn=ring_part, variants=["base"]), tally=dict(fn=tally_part, variants=["base"]), **FX)))
    J.append(dict(name="chat", w=AW, h=AH, plate=chat_plate, seed=1304, parts=dict(
        agnes=dict(fn=agnes_chat, variants=V3), hedley=dict(fn=hedley_chat, variants=V3), **FX)))
    J.append(dict(name="office", w=AW, h=AH, plate=office_plate, seed=1305, parts=dict(
        ship=dict(fn=ship_part, variants=["base"]), note=dict(fn=note_part, variants=["base"]))))
    J.append(dict(name="notec", w=AW, h=AH, plate=notec_plate, seed=1306, parts=dict(ring=dict(fn=peir_ring, variants=["base"]))))
    J.append(dict(name="kettle", w=AW, h=AH, plate=kettle_plate, seed=1307, parts=dict(
        quill=dict(fn=quill_k, variants=V3), agnes=dict(fn=agnes_k, variants=V2))))
    J.append(dict(name="lineup", w=3 * PW, h=AH, plate=lineup_plate, seed=1308, parts={
        f"s{i}": dict(fn=B.lineup_fig_fn(i, fn), variants=V3) for i, (_, fn) in enumerate(CAST)}))
    J.append(dict(name="spell", w=AW, h=AH, plate=spell_plate, seed=1309, parts=dict(
        poster=dict(fn=poster_part, variants=["base"]), chalk=dict(fn=chalk_part, variants=["base"]),
        ok1=dict(fn=partial(ok_part, x=196, y=240), variants=["base"]), ok2=dict(fn=partial(ok_part, x=444, y=200), variants=["base"]))))
    J.append(dict(name="board", w=AW, h=AH, plate=board_plate, seed=1310, parts=dict(
        match=dict(fn=match_part, variants=["base"]),
        tk1=dict(fn=partial(tick_part, y=284), variants=["base"]), tk2=dict(fn=partial(tick_part, y=184), variants=["base"]))))
    J.append(dict(name="confess", w=AW, h=AH, plate=confess_plate, seed=1311, parts=dict(
        hedley=dict(fn=hedley_conf, variants=["sheepish", "sheepish+blink"]), quill=dict(fn=quill_conf, variants=V2),
        bigship=dict(fn=bigship_part, variants=["base"]))))
    J.append(dict(name="sunset", w=AW, h=AH, plate=sunset_plate, seed=1312, parts=dict(
        ship=dict(fn=ship_back, variants=["base"]), card=dict(fn=card_part, variants=["base"]), **FX)))
    J.append(dict(name="vignette", w=384, h=384, plate=vignette, seed=1313))
    return J

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    J = [j for j in jobs() if not want or j["name"] in want]
    save_layers(OUT, J, B.make_ink)
