"""Illustrations for Case 24, The Kite Festival: BLACK-AND-WHITE ink (bwkit) with the simple v1 peg-doll characters.
The long beach with the sea on the LEFT and the dunes / village / hills on the RIGHT, so the wind (sea -> land) always
blows left-to-right: flags, kites and Rosie's balloon all lean right. The judges' tent at the water's edge with the
carved wooden puffin, three people with equal tags, and a "which way was the wind?" board.
PART sprites use part_open (clip only, never frame2).
Hook (render.py HOOK_STYLE="weathervane"): borderless hero of the beach with kites.
Fairness: Pip, Tamsin and Mr Penberthy share one stance, height, arms-down pose and neutral face in the cast strip and the
lineup; each gets the same-size tag as narrated. Only the confession shows Penberthy sheepish.
Run: python3 art_case24.py [scene ...]"""
import os, sys, math
from functools import partial
import bwkit as B
from bwkit import plate_open, part_open, full_open, InkBW, PW, AW, AH, V2, V3, CW, CH
import figures as F
from inkart import K, Wt
from layers import save_layers

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-24")

def pip(k, x, y, h, **kw): kw.setdefault("prop", False); F.pip(k, x, y, h, **kw)
def tamsin(k, x, y, h, **kw): kw.setdefault("prop", None); kw.setdefault("expr", "neutral"); F.tamsin(k, x, y, h, **kw)
def penberthy(k, x, y, h, **kw): B.visitor(k, x, y, h, suit="stripe", hat="cap", tie=True, **kw)
def agnes(k, x, y, h, **kw): kw.setdefault("teapot", False); F.agnes(k, x, y, h, **kw)

def _kite(k, x, y, s, tail=True, lean=25):
    """Diamond kite leaning right (downwind); (x, y) = centre."""
    a = math.radians(lean); ca, sa = math.cos(a), math.sin(a)
    P = [(0, s * 0.6), (s * 0.35, 0), (0, -s * 0.5), (-s * 0.35, 0)]
    pts = [(x + px * ca + py * sa, y - px * sa + py * ca) for px, py in P]
    k.shape(pts, lw=0.9, fill=Wt, amp=0); k.line([pts[0], pts[2]], lw=0.4, amp=0); k.line([pts[1], pts[3]], lw=0.4, amp=0)
    if tail:
        bx, by = pts[2]
        k.line([(bx, by), (bx - s * 0.3, by - s * 0.3), (bx - s * 0.2, by - s * 0.6), (bx - s * 0.45, by - s * 0.9)], lw=0.5, amp=0.3)
        for j in range(3): k.circle(bx - s * (0.15 + j * 0.13), by - s * (0.22 + j * 0.25), 1.6, lw=0.4, fill=K)
InkBW.kite = _kite

def _flag(k, x, y, hp=60, fw=34):
    """Flagpole with a flag streaming to the RIGHT (inland)."""
    k.line([(x, y), (x, y + hp)], lw=1.1, amp=0)
    k.shape([(x, y + hp), (x + fw, y + hp - 4), (x + fw * 0.85, y + hp - 9), (x + fw, y + hp - 14), (x, y + hp - 16)], lw=0.8, fill=Wt, amp=0.1)
InkBW.flag = _flag

def _puffin(k, x, y, s):
    """Carved wooden puffin on a little plinth; (x, y) = plinth base centre."""
    k.rect(x - s * 0.35, y, s * 0.7, s * 0.14, lw=0.8, fill=Wt)
    body = k.arcpts(x, y + s * 0.5, s * 0.25, s * 0.36, 0, 360, 22); k.shape(body, lw=1.0, fill=K, amp=0)
    k.shape(k.arcpts(x + s * 0.05, y + s * 0.45, s * 0.14, s * 0.24, 0, 360, 18), lw=0.6, fill=Wt, amp=0)
    k.circle(x, y + s * 0.92, s * 0.17, lw=1.0, fill=K); k.circle(x + s * 0.06, y + s * 0.94, s * 0.1, lw=0.4, fill=Wt)
    k.circle(x + s * 0.08, y + s * 0.95, s * 0.025, lw=0, fill=K, stroke=False)
    k.shape([(x + s * 0.14, y + s * 0.96), (x + s * 0.36, y + s * 0.9), (x + s * 0.14, y + s * 0.82)], lw=0.8, fill=Wt, amp=0)
    k.line([(x + s * 0.18, y + s * 0.92), (x + s * 0.24, y + s * 0.86)], lw=0.4, amp=0)
InkBW.puffin = _puffin

def _tent(k, x, y, w):
    h = w * 0.7
    k.shape([(x - w / 2, y), (x + w / 2, y), (x + w / 2, y + h * 0.6), (x, y + h), (x - w / 2, y + h * 0.6)], lw=1.2, fill=Wt, amp=0.1)
    for j in range(1, 6): k.line([(x - w / 2 + j * w / 6, y + h * 0.6 + (h * 0.4) * (1 - abs(j - 3) / 3)), (x - w / 2 + j * w / 6, y)], lw=0.35, amp=0)
    k.line([(x, y + h), (x, y + h + 14)], lw=0.8, amp=0)
    k.shape([(x, y + h + 14), (x + 14, y + h + 10), (x, y + h + 6)], lw=0.6, fill=Wt, amp=0)   # pennant blowing right
InkBW.judges_tent = _tent

def _beach(k, w, h, sea=True):
    """Sea on the left, sand, dunes and village/hills on the right."""
    if sea: k.sea(14, 170, 60, 150, rows=5)
    k.line([(14, 60), (w - 14, 60)], lw=0.9, amp=0.1)
    k.shape([(170, 60), (190, 150), (14, 150), (14, 60)], lw=0, fill=None, amp=0)
    k.line([(170, 60), (200, 150)], lw=0.8, amp=0.2)   # water's edge
    for dx in (360, 420, 470):
        k.shape(k.arcpts(dx, 60, 40, 30, 0, 180, 14), lw=0.9, fill=Wt, amp=0.2)
        for j in range(4): k.line([(dx - 10 + j * 6, 80), (dx - 6 + j * 6, 96)], lw=0.4, amp=0.2)
    k.line([(300, 150), (350, 180), (400, 172), (450, 200), (498, 190)], lw=0.8, amp=0.3)
    for hx in (360, 400, 440):
        k.rect(hx, 150, 26, 22, lw=0.7, fill=Wt); k.shape([(hx - 2, 172), (hx + 13, 184), (hx + 28, 172)], lw=0.7, fill=Wt, amp=0)

def _wind_arrows(k, y0=250):
    for i, (x, y) in enumerate(((40, y0), (170, y0 + 30), (300, y0 - 10))):
        k.line([(x, y), (x + 80, y)], lw=1.0, amp=0.2); k.shape([(x + 80, y + 6), (x + 94, y), (x + 80, y - 6)], lw=0.8, fill=K, amp=0)

# ----------------------------------------------------------------------------- 1. hook hero
def hook_plate(k, w, h):
    full_open(k, w, h); _beach(k, w, h)
    for x, y, s in ((120, 300, 40), (240, 320, 34), (360, 290, 46)): k.kite(x, y, s)
    k.flag(210, 150); k.unclip()

# ----------------------------------------------------------------------------- 2. cast
CAST = [("PIP", pip), ("TAMSIN", tamsin), ("MR PENBERTHY", penberthy)]
cast_plate = B.cast_plate_fn([n for n, _ in CAST], style="cards")

# ----------------------------------------------------------------------------- 3. the beach: wind from the sea toward the land
def beach_plate(k, w, h): plate_open(k, w, h); _beach(k, w, h); k.text(70, 40, "SEA", size=11, font="Ink-Plex"); k.text(430, 40, "LAND", size=11, font="Ink-Plex"); k.unclip()
def wind_part(k, w, h, v): part_open(k, w, h); _wind_arrows(k); k.pin_card(150, 300, 210, 34, ["breeze: from the sea toward the land"], size=10); k.unclip()
def flags_part(k, w, h, v): part_open(k, w, h); [k.flag(x, 150, 50, 30) for x in (200, 250)]; k.text(230, 214, "flags point inland", size=10, font="Ink-Kalam"); k.unclip()
def kites_part(k, w, h, v): part_open(k, w, h); [k.kite(x, y, s) for x, y, s in ((300, 240, 34), (380, 260, 30), (450, 230, 26))]; k.unclip()
def balloon_part(k, w, h, v):
    part_open(k, w, h); k.shape(k.arcpts(470, 300, 12, 15, 0, 360, 16), lw=0.9, fill=Wt, amp=0); k.line([(470, 285), (462, 262)], lw=0.4, amp=0.3)
    k.text(440, 330, "Rosie's balloon \u2192 hills", size=9, font="Ink-Kalam"); k.unclip()
def agnes_b(k, w, h, v): part_open(k, w, h); agnes(k, 290, 30, 150); k.unclip()
def still_part(k, w, h, v): part_open(k, w, h); k.pin_card(30, 300, 190, 34, ["still pointing toward the hills"], size=10); k.unclip()

# ----------------------------------------------------------------------------- 4. the judges' tent at the water's edge
def tent_plate(k, w, h):
    plate_open(k, w, h); _beach(k, w, h); k.judges_tent(250, 60, 180)
    k.rect(210, 60, 80, 40, lw=0.9, fill=Wt); k.text(250, 30, "the judges' tent, by the water's edge", size=10, font="Ink-Kalam"); k.unclip()
def puffin_part(k, w, h, v): part_open(k, w, h); k.puffin(250, 100, 50); k.unclip()
def prize_part(k, w, h, v): part_open(k, w, h); k.pin_card(330, 270, 160, 40, ["prize for the best kite:", "a carved wooden puffin"], size=10); k.unclip()
def lobster_part(k, w, h, v):
    part_open(k, w, h); x, y = 90, 300
    k.shape(k.arcpts(x, y, 30, 14, 0, 360, 20), lw=1.0, fill=Wt, amp=0.1)
    for s_ in (-1, 1): k.shape(k.arcpts(x + 36, y + s_ * 14, 10, 6, 0, 360, 12), lw=0.8, fill=Wt, amp=0)
    k.text(x, y - 30, "the lobster kite", size=10, font="Ink-Kalam"); k.unclip()
def gone_t(k, w, h, v): part_open(k, w, h); k.dashed_outline(250, 100, 40, 54); k.pin_card(330, 200, 120, 34, ["4 o'clock: gone!"], size=11); k.unclip()

# ----------------------------------------------------------------------------- 5. lineup
def _dunes(k, pw, h):
    k.line([(14, 50), (pw - 14, 50)], lw=0.9, amp=0.1)
    for dx in (300, 380, 450): k.shape(k.arcpts(dx, 50, 44, 34, 0, 180, 14), lw=0.9, fill=Wt, amp=0.2)
def _stall(k, pw, h):
    k.line([(14, 50), (pw - 14, 50)], lw=0.9, amp=0.1); k.rect(300, 50, 170, 60, lw=1.0, fill=Wt); k.text(385, 80, "BOOKS", size=12, font="Ink-Plex")
    for j in range(5): k.rect(310 + j * 30, 112, 22, 30, lw=0.6, fill=Wt)
    k.text(385, 160, "car park \u2192", size=9, font="Ink-Kalam")
def _edge(k, pw, h): k.sea(14, pw - 14, 50, 120, rows=4); k.line([(14, 50), (pw - 14, 50)], lw=0.9, amp=0.1); k.judges_tent(420, 50, 110)
lineup_plate = B.lineup_plate_fn([_dunes, _stall, _edge], [n for n, _ in CAST])
FX, FY, FH = PW / 2 - 160, 50, 220
TAGS = [["top of the beach, by the dunes;", "class says he never moved"], ["book stall by the car park,", "queue all afternoon"], ["seen hurrying from the", "water's edge near the tent, ~4"]]
def ltag(k, w, h, v, i=0):
    part_open(k, w, h); x = i * PW + 236; k.rect(x, 286, 250, 50, lw=1.1, fill=Wt)
    for j, ln in enumerate(TAGS[i]): k.text(x + 125, 318 - j * 20, ln, size=11, font="Ink-Kalam")
    k.unclip()
def pip_kite(k, w, h, v): part_open(k, w, h); k.kite(330, 230, 36); k.line([(FX + 30, FY + 0.45 * FH), (318, 210)], lw=0.4, amp=0.1); k.unclip()
SAID = ["\u201cMy kite string snapped. The kite flew off", "out over the SEA, so I ran down to the", "water's edge after it. Halfway to France!\u201d"]
def said_part(k, w, h, v):
    part_open(k, w, h); x = 2 * PW + 196; k.rect(x, 190, 300, 78, lw=1.1, fill=Wt)
    for j, ln in enumerate(SAID): k.text(x + 150, 250 - j * 20, ln, size=10, font="Ink-Kalam")
    k.unclip()

# ----------------------------------------------------------------------------- 6. solution board
def board_plate(k, w, h):
    plate_open(k, w, h); k.floorboards(w, y=56); k.case_board(24, 66, 464, 292, title="WHICH WAY WAS THE WIND?")
    k.text(110, 300, "SEA", size=12, font="Ink-Plex"); k.text(400, 300, "LAND / HILLS", size=12, font="Ink-Plex")
def b_wind(k, w, h, v):
    part_open(k, w, h); k.line([(150, 300), (330, 300)], lw=2.0, amp=0.1); k.shape([(330, 308), (350, 300), (330, 292)], lw=1, fill=K, amp=0)
    k.text(250, 276, "flags, kites, balloon: all inland", size=10, font="Ink-Kalam"); k.unclip()
def b_story(k, w, h, v):
    part_open(k, w, h); k.line([(330, 230), (160, 230)], lw=1.4, amp=0.1); k.shape([(160, 238), (140, 230), (160, 222)], lw=1, fill=K, amp=0)
    k.text(250, 206, "his story: kite blew OUT to sea", size=10, font="Ink-Kalam")
    for a, b in (((220, 218), (280, 246)), ((280, 218), (220, 246))): k.line([a, b], lw=2.4, amp=0.3)
    k.unclip()
def b_row(k, w, h, v, i=0):
    part_open(k, w, h); y = (150, 124)[i]; txt = ("Pip: top of the beach, whole class", "Tamsin: book stall by the car park")[i]
    k.text(250, y, txt, size=11, font="Ink-Kalam"); k.line([(130, y + 4), (370, y + 4)], lw=1.6, amp=0.2); k.unclip()
def b_ring(k, w, h, v): part_open(k, w, h); k.pin_card(330, 80, 140, 40, ["Penberthy: near the tent,", "story against the wind"], size=10); k.shape(k.arcpts(400, 100, 80, 30, 0, 360, 30), lw=2.2, fill=None, amp=0.4); k.unclip()

# ----------------------------------------------------------------------------- 7. confession
def conf_plate(k, w, h): plate_open(k, w, h); _beach(k, w, h); k.unclip()
def pen_c(k, w, h, v): part_open(k, w, h); penberthy(k, 260, 40, 200, expr="sheepish" if "sheepish" in v else "neutral"); k.unclip()
def bag_part(k, w, h, v):
    part_open(k, w, h); k.rect(320, 60, 70, 40, lw=1.0, fill=Wt); k.text(355, 70, "KITE BAG", size=8, font="Ink-Plex"); k.puffin(355, 100, 34)
    k.kite(420, 120, 30, tail=False, lean=0); k.text(420, 160, "never broken", size=9, font="Ink-Kalam"); k.unclip()
def second_part(k, w, h, v): part_open(k, w, h); k.pin_card(30, 290, 170, 46, ["second, five years running:", "wanted it just once"], size=10); k.unclip()
def joke_part(k, w, h, v): part_open(k, w, h); k.pin_card(30, 220, 170, 46, ["special prize: most", "imaginative kite story"], size=10); k.unclip()

def _vig(k, w, h): k.kite(w / 2, h / 2, h * 0.4)
vignette = B.vignette_fn(_vig)

def jobs():
    J = []
    J.append(dict(name="hook", w=AW, h=AH, plate=hook_plate, seed=2401))
    J.append(dict(name="cast", w=CW, h=CH, plate=cast_plate, seed=2402, parts={
        f"s{i}": dict(fn=B.cast_fig_fn(i, 3, fn), variants=V2) for i, (_, fn) in enumerate(CAST)}))
    J.append(dict(name="beach", w=AW, h=AH, plate=beach_plate, seed=2403, parts=dict(
        wind=dict(fn=wind_part, variants=["base"]), flags=dict(fn=flags_part, variants=["base"]), kites=dict(fn=kites_part, variants=["base"]),
        balloon=dict(fn=balloon_part, variants=["base"]), agnes=dict(fn=agnes_b, variants=V2), still=dict(fn=still_part, variants=["base"]), **B.FX_GULL)))
    J.append(dict(name="tent", w=AW, h=AH, plate=tent_plate, seed=2404, parts=dict(
        puffin=dict(fn=puffin_part, variants=["base"]), prize=dict(fn=prize_part, variants=["base"]), lobster=dict(fn=lobster_part, variants=["base"]),
        gone=dict(fn=gone_t, variants=["base"]), agnes=dict(fn=agnes_b, variants=V2))))
    J.append(dict(name="lineup", w=3 * PW, h=AH, plate=lineup_plate, seed=2405, parts={
        **{f"s{i}": dict(fn=B.lineup_fig_fn(i, fn, x=FX, y=FY, fh=FH), variants=V3) for i, (_, fn) in enumerate(CAST)},
        **{f"p{i}": dict(fn=partial(ltag, i=i), variants=["base"]) for i in range(3)},
        "kite": dict(fn=pip_kite, variants=["base"]), "said": dict(fn=said_part, variants=["base"])}))
    J.append(dict(name="board", w=AW, h=AH, plate=board_plate, seed=2406, parts={
        "wind": dict(fn=b_wind, variants=["base"]), "story": dict(fn=b_story, variants=["base"]),
        **{f"r{i}": dict(fn=partial(b_row, i=i), variants=["base"]) for i in range(2)}, "ring": dict(fn=b_ring, variants=["base"])}))
    J.append(dict(name="confess", w=AW, h=AH, plate=conf_plate, seed=2407, parts=dict(
        pen=dict(fn=pen_c, variants=["sheepish", "sheepish+blink"]), bag=dict(fn=bag_part, variants=["base"]),
        second=dict(fn=second_part, variants=["base"]), joke=dict(fn=joke_part, variants=["base"]))))
    J.append(dict(name="vignette", w=384, h=384, plate=vignette, seed=2408))
    return J

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    J = [j for j in jobs() if not want or j["name"] in want]
    save_layers(OUT, J, B.make_ink)
