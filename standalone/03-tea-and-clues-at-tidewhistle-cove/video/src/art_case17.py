"""Illustrations for Case 17, The Talking Parrot: BLACK-AND-WHITE ink (bwkit) with the simple v1 peg-doll characters.
Admiral the grey parrot (hatched) on his perch in Wenna's antique shop, speech bubbles for every phrase he knows,
Mr Pascoe's ladder outside the Kettle and Gull, the silver thimble. PART sprites use part_open (clip only, never frame2).
Hook (render.py HOOK_STYLE="bubble"): borderless hero of the antique shop with Admiral on his perch.
Fairness: Tamsin, Mr Fenwick and Mr Pascoe share one stance, height, arms-down pose and neutral face in the cast strip and
the lineup, each with a key tag; only the confession shows Mr Pascoe sheepish.
Run: python3 art_case17.py [scene ...]"""
import os, sys, math
from functools import partial
import bwkit as B
from bwkit import plate_open, part_open, full_open, InkBW, PW, AW, AH, V2, V3, CW, CH
import figures as F
from inkart import K, Wt
from layers import save_layers

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-17")

def tamsin(k, x, y, h, **kw): kw.setdefault("prop", None); kw.setdefault("expr", "neutral"); F.tamsin(k, x, y, h, **kw)
def fenwick(k, x, y, h, **kw): B.visitor(k, x, y, h, suit="dark", hat="cap", tie=False, moustache=True, **kw)
def pascoe(k, x, y, h, **kw): B.overalls(k, x, y, h, paint=False, cap=True, **kw)
def wenna(k, x, y, h, **kw): kw.setdefault("prop", False); F.wenna(k, x, y, h, **kw)
def agnes(k, x, y, h, **kw): kw.setdefault("teapot", False); F.agnes(k, x, y, h, **kw)

# ----------------------------------------------------------------------------- Admiral, bubbles, thimble
def _parrot(k, x, y, s, beak_open=False):
    """Admiral perched (x, y = the perch point under his feet, s = height)."""
    body = k.arcpts(x, y + s * 0.42, s * 0.2, s * 0.36, 0, 360, 28)
    k.shape(body, lw=1.1, fill=Wt, amp=0.1); k.hatch(body, angle=-50, gap=2.6, lw=0.3)
    wing = [(x + s * 0.02, y + s * 0.62), (x + s * 0.2, y + s * 0.5), (x + s * 0.16, y + s * 0.14), (x + s * 0.02, y + s * 0.3)]
    k.shape(wing, lw=0.9, fill=Wt, amp=0.1); k.hatch(wing, angle=40, gap=2.0, lw=0.3, cross=True)
    k.shape([(x - s * 0.06, y + s * 0.12), (x + s * 0.08, y + s * 0.12), (x + s * 0.04, y - s * 0.22), (x - s * 0.04, y - s * 0.22)], lw=0.9, fill=K, amp=0)  # tail
    hx, hy, r = x - s * 0.02, y + s * 0.82, s * 0.16
    k.circle(hx, hy, r, lw=1.1, fill=Wt)
    k.circle(hx - r * 0.25, hy + r * 0.15, r * 0.32, lw=0.6, fill=Wt); k.circle(hx - r * 0.25, hy + r * 0.15, r * 0.12, lw=0, fill=K, stroke=False)
    if beak_open:
        k.shape([(hx - r * 0.85, hy + r * 0.2), (hx - r * 1.6, hy + r * 0.05), (hx - r * 1.2, hy - r * 0.15)], lw=0.9, fill=K, amp=0)
        k.shape([(hx - r * 0.85, hy - r * 0.25), (hx - r * 1.35, hy - r * 0.55), (hx - r * 0.95, hy - r * 0.6)], lw=0.9, fill=K, amp=0)
    else:
        k.shape([(hx - r * 0.85, hy + r * 0.2), (hx - r * 1.5, hy - r * 0.05), (hx - r * 1.1, hy - r * 0.5), (hx - r * 0.8, hy - r * 0.3)], lw=0.9, fill=K, amp=0)
    for dx in (-0.05, 0.05): k.line([(x + dx * s, y + s * 0.08), (x + dx * s, y)], lw=1.0, amp=0)
InkBW.parrot = _parrot

def _perch(k, x, y, s):
    k.line([(x - s * 0.4, y), (x + s * 0.4, y)], lw=2.0, amp=0); k.line([(x + s * 0.3, y), (x + s * 0.3, y - s * 1.3)], lw=1.4, amp=0)
    k.line([(x + s * 0.1, y - s * 1.3), (x + s * 0.5, y - s * 1.3)], lw=1.6, amp=0)
InkBW.perch = _perch

def _bubble(k, x, y, w, h, text, tail, size=12):
    """Rounded speech bubble, (x, y) lower-left, tail = point it speaks from."""
    c = k.c; c.setStrokeColor(K); c.setFillColor(Wt); c.setLineWidth(1.2)
    tx, ty = tail
    if tx < x:   # tail from the left side
        by = min(max(ty, y + 10), y + h - 10)
        p = c.beginPath(); p.moveTo(x + 2, by - 7); p.lineTo(tx, ty); p.lineTo(x + 2, by + 7); c.drawPath(p, stroke=1, fill=1)
        c.roundRect(x, y, w, h, min(h / 2, 16), stroke=1, fill=1)
        c.setStrokeColor(Wt); c.setLineWidth(2.4); c.line(x + 1.5, by - 6, x + 1.5, by + 6)
    else:
        bx = min(max(tx, x + 20), x + w - 20)
        p = c.beginPath(); p.moveTo(bx - 10, y + 2); p.lineTo(tx, ty); p.lineTo(bx + 10, y + 2); c.drawPath(p, stroke=1, fill=1)
        c.roundRect(x, y, w, h, min(h / 2, 16), stroke=1, fill=1)
        c.setStrokeColor(Wt); c.setLineWidth(2.4); c.line(bx - 9, y + 1.5, bx + 9, y + 1.5)
    lines = text.split("\n"); lh = size * 1.15; y0 = y + h / 2 + (len(lines) - 1) * lh / 2 - size * 0.35
    for i, ln in enumerate(lines): k.text(x + w / 2, y0 - i * lh, ln, size=size, font="Ink-Kalam")
InkBW.bubble = _bubble

def _thimble(k, x, y, s):
    k.shape(k.arcpts(x, y, s * 0.75, s * 0.14, 0, 360, 20), lw=0.8, fill=Wt, amp=0); k.hatch(k.arcpts(x, y, s * 0.75, s * 0.14, 0, 360, 20), angle=0, gap=1.6, lw=0.3)
    dome = [(x - s * 0.4, y), (x + s * 0.4, y)] + k.arcpts(x, y + s * 0.55, s * 0.36, s * 0.45, 0, 180, 16)[::-1]
    k.shape(dome, lw=1.0, fill=Wt, amp=0)
    for r in range(3):
        for j in range(5): k.circle(x - s * 0.24 + j * s * 0.12, y + s * 0.3 + r * s * 0.18, s * 0.03, lw=0, fill=K, stroke=False)
    k.rect(x - s * 0.42, y, s * 0.84, s * 0.1, lw=0.8, fill=Wt)
    for a in (30, 75, 120): k.line([(x + s * 0.55 * math.cos(math.radians(a)) * 1.6, y + s * 0.5 + s * 0.6 * math.sin(math.radians(a))),
                                    (x + s * 0.75 * math.cos(math.radians(a)) * 1.6, y + s * 0.5 + s * 0.8 * math.sin(math.radians(a)))], lw=0.7, amp=0)
InkBW.thimble = _thimble

def _ladder(k, x, y, hgt):
    for dx in (0, 30): k.line([(x + dx, y), (x + dx + 20, y + hgt)], lw=1.2, amp=0)
    for i in range(1, 9): u = i / 9; k.line([(x + 20 * u, y + hgt * u), (x + 30 + 20 * u, y + hgt * u)], lw=0.8, amp=0)
InkBW.ladder = _ladder

def shop_interior(k, w, h):
    k.floorboards(w, y=80)
    k.text(110, 334, "POLGLAZE ANTIQUES", size=12, font="Ink-Plex")
    k.rect(300, 80, 190, 70, lw=1.2, fill=Wt); k.line([(300, 150), (490, 150)], lw=1.5, amp=0)     # counter
    k.rect(40, 100, 110, 210, lw=1.0, fill=Wt)                                                   # cabinet
    for yy in (160, 230): k.line([(40, yy), (150, yy)], lw=0.8, amp=0)
    k.circle(70, 112, 10, lw=0.7, fill=Wt); k.rect(95, 102, 30, 40, lw=0.7, fill=Wt); k.circle(80, 190, 14, lw=0.7, fill=Wt); k.rect(110, 236, 26, 40, lw=0.7, fill=Wt)
    k.window_view(330, 210, 120, 90, view="street")
    k.perch(220, 230, 70)

# ----------------------------------------------------------------------------- 1. hook hero
def hook_plate(k, w, h): full_open(k, w, h); shop_interior(k, w, h); k.parrot(220, 230, 80); k.thimble(400, 150, 28); k.unclip()

# ----------------------------------------------------------------------------- 2. cast
CAST = [("TAMSIN", tamsin), ("MR FENWICK", fenwick), ("MR PASCOE", pascoe)]
cast_plate = B.cast_plate_fn([n for n, _ in CAST], style="tags")

# ----------------------------------------------------------------------------- 3. Mr Pascoe and his ladder outside the Kettle and Gull
def tea_plate(k, w, h): plate_open(k, w, h); k.tearoom(w, h, window=True, counter=False); k.ladder(330, 30, 250); k.unclip()
def pascoe_l(k, w, h, v): part_open(k, w, h); pascoe(k, 300, 30, 200); k.rect(340, 30, 30, 26, lw=0.9, fill=Wt); k.unclip()
def agnes_t(k, w, h, v): part_open(k, w, h); agnes(k, 120, 30, 200); k.unclip()
def say_part(k, w, h, v): part_open(k, w, h); k.bubble(330, 270, 170, 60, "Mind how you go,\nmy lovely!", (310, 235), size=14); k.unclip()
def tease_part(k, w, h, v): part_open(k, w, h); k.pin_card(150, 300, 150, 44, ["nobody else", "says it"], size=12); k.unclip()

# ----------------------------------------------------------------------------- 4. the antique shop: Wenna and Admiral's three phrases
def shop_plate(k, w, h): plate_open(k, w, h); shop_interior(k, w, h); k.unclip()
def admiral(k, w, h, v): part_open(k, w, h); k.parrot(220, 230, 80, beak_open=("talk" in v)); k.unclip()
def wenna_s(k, w, h, v): part_open(k, w, h); wenna(k, 400, 80, 200, flip=True); k.unclip()
def thimble_part(k, w, h, v): part_open(k, w, h); k.thimble(330, 150, 24); k.unclip()
def thimble_gone(k, w, h, v): part_open(k, w, h); k.dashed_outline(316, 150, 30, 30); k.text(330, 190, "gone!", size=11, font="Ink-Kalam"); k.unclip()
PH = [("Good morning", 0, 318), ("Pieces of eight", 0, 278), ("Put the kettle on", 0, 238)]
def ph_part(k, w, h, v, i=0):
    part_open(k, w, h); t, dx, y = PH[i]; k.bubble(262 + dx, y - 16, 160, 32, t, (236, 300), size=13); k.unclip()
def mind_part(k, w, h, v):
    part_open(k, w, h); k.bubble(262, 262, 200, 66, "Mind how you go,\nmy lovely!", (236, 300), size=15); k.unclip()
def lock_part(k, w, h, v):
    part_open(k, w, h); x, y = 470, 300
    k.rect(x - 14, y - 14, 28, 22, lw=1.0, fill=K); k.c.setStrokeColor(K); k.c.setLineWidth(2.0); k.c.arc(x - 9, y, x + 9, y + 20, 0, 180)
    k.text(x, y - 30, "locked", size=10, font="Ink-Kalam"); k.unclip()

# ----------------------------------------------------------------------------- 5. lineup: three keyholders (equal key tags)
def _key(k, x, y, s=1.0):
    k.circle(x, y, 7 * s, lw=1.0, fill=Wt); k.line([(x + 7 * s, y), (x + 30 * s, y)], lw=1.4, amp=0)
    for d in (18, 25): k.line([(x + d * s, y), (x + d * s, y - 6 * s)], lw=1.2, amp=0)
def _p_tams(k, pw, h): k.floorboards(pw, y=50); k.rect(290, 50, 190, 220, lw=1.1, fill=Wt); k.text(385, 250, "TAMSIN'S BOOKS", size=10, font="Ink-Plex")
def _p_fen(k, pw, h): k.floorboards(pw, y=50); k.rect(290, 50, 190, 220, lw=1.1, fill=Wt); k.text(385, 250, "GROCER'S", size=10, font="Ink-Plex")
def _p_pas(k, pw, h): k.floorboards(pw, y=50); k.rect(290, 50, 190, 220, lw=1.1, fill=Wt); k.text(385, 250, "WINDOWS CLEANED", size=10, font="Ink-Plex")
lineup_plate = B.lineup_plate_fn([_p_tams, _p_fen, _p_pas], [n for n, _ in CAST])
def keytag(k, w, h, v, i=0):
    part_open(k, w, h); x = i * PW + 330; k.rect(x, 150, 110, 50, lw=1.0, fill=Wt); _key(k, x + 22, 175); k.text(x + 80, 168, "key", size=13, font="Ink-Kalam"); k.unclip()
ALIBI = ["\u201cin my own shop\u201d", "\u201cat the grocer's\u201d", "\u201cnot there today\u201d"]
def alibi(k, w, h, v, i=0):
    part_open(k, w, h); x = i * PW + 300; k.bubble(x, 90, 170, 40, ALIBI[i], (x - 30, 140), size=12); k.unclip()

# ----------------------------------------------------------------------------- 6. solution board
def board_plate(k, w, h):
    plate_open(k, w, h); k.floorboards(w, y=60)
    k.case_board(30, 76, 452, 280, title="WHAT DOES ADMIRAL SAY?")
    k.text(140, 296, "before (knew)", size=11, font="Ink-Plex"); k.text(372, 296, "after the half hour", size=11, font="Ink-Plex")
    for i, (t, _, _) in enumerate(PH): k.text(140, 266 - i * 26, t, size=13, font="Ink-Kalam")
    k.line([(256, 110), (256, 300)], lw=0.6, amp=0)
def bnew(k, w, h, v): part_open(k, w, h); k.bubble(290, 220, 170, 56, "Mind how you go,\nmy lovely!", (280, 210), size=13); k.text(372, 196, "said over and over", size=11, font="Ink-Kalam"); k.unclip()
def bwho(k, w, h, v):
    part_open(k, w, h); k.pin_card(300, 160, 150, 54, ["MR PASCOE", "20 years"], size=12); k.unclip()
def bkey(k, w, h, v): part_open(k, w, h); _key(k, 330, 116, 1.2); k.text(400, 110, "had a key", size=12, font="Ink-Kalam"); k.unclip()
def bring(k, w, h, v): part_open(k, w, h); k.shape(k.arcpts(375, 248, 105, 44, 0, 360, 36), lw=2.2, fill=None, amp=0.4); k.unclip()

# ----------------------------------------------------------------------------- 7. confession
def conf_plate(k, w, h): plate_open(k, w, h); shop_interior(k, w, h); k.unclip()
def pascoe_c(k, w, h, v):
    part_open(k, w, h); pascoe(k, 330, 80, 190, expr="sheepish" if "sheepish" in v else "neutral", flip=True); k.unclip()
def wenna_c(k, w, h, v): part_open(k, w, h); wenna(k, 440, 80, 190, flip=True); k.unclip()
def thim_c(k, w, h, v): part_open(k, w, h); k.thimble(380, 152, 22); k.unclip()
def price_part(k, w, h, v): part_open(k, w, h); k.pin_card(60, 330, 130, 40, ["a very kind price"], size=11); k.unclip()

def _vig(k, w, h): k.perch(w * 0.45, h * 0.35, w * 0.3); k.parrot(w * 0.45, h * 0.35, h * 0.4)
vignette = B.vignette_fn(_vig)

def jobs():
    J = []
    J.append(dict(name="hook", w=AW, h=AH, plate=hook_plate, seed=1701))
    J.append(dict(name="cast", w=CW, h=CH, plate=cast_plate, seed=1702, parts={
        f"s{i}": dict(fn=B.cast_fig_fn(i, 3, fn), variants=V2) for i, (_, fn) in enumerate(CAST)}))
    J.append(dict(name="tea", w=AW, h=AH, plate=tea_plate, seed=1703, parts=dict(
        pascoe=dict(fn=pascoe_l, variants=V3), agnes=dict(fn=agnes_t, variants=V2), say=dict(fn=say_part, variants=["base"]), tease=dict(fn=tease_part, variants=["base"]))))
    J.append(dict(name="shop", w=AW, h=AH, plate=shop_plate, seed=1704, parts={
        "admiral": dict(fn=admiral, variants=["base", "base+talk"]), "wenna": dict(fn=wenna_s, variants=V2),
        "thimble": dict(fn=thimble_part, variants=["base"]), "gone": dict(fn=thimble_gone, variants=["base"]),
        "mind": dict(fn=mind_part, variants=["base"]), "lock": dict(fn=lock_part, variants=["base"]),
        **{f"p{i}": dict(fn=partial(ph_part, i=i), variants=["base"]) for i in range(3)}}))
    J.append(dict(name="lineup", w=3 * PW, h=AH, plate=lineup_plate, seed=1705, parts={
        **{f"s{i}": dict(fn=B.lineup_fig_fn(i, fn, x=PW / 2 - 140, y=50, fh=220), variants=V3) for i, (_, fn) in enumerate(CAST)},
        **{f"k{i}": dict(fn=partial(keytag, i=i), variants=["base"]) for i in range(3)},
        **{f"a{i}": dict(fn=partial(alibi, i=i), variants=["base"]) for i in range(3)}}))
    J.append(dict(name="board", w=AW, h=AH, plate=board_plate, seed=1706, parts=dict(
        new=dict(fn=bnew, variants=["base"]), ring=dict(fn=bring, variants=["base"]), who=dict(fn=bwho, variants=["base"]), key=dict(fn=bkey, variants=["base"]))))
    J.append(dict(name="confess", w=AW, h=AH, plate=conf_plate, seed=1707, parts=dict(
        pascoe=dict(fn=pascoe_c, variants=["sheepish", "sheepish+blink"]), wenna=dict(fn=wenna_c, variants=V2),
        admiral=dict(fn=admiral, variants=["base", "base+talk"]), thimble=dict(fn=thim_c, variants=["base"]), price=dict(fn=price_part, variants=["base"]),
        mind=dict(fn=mind_part, variants=["base"]))))
    J.append(dict(name="vignette", w=384, h=384, plate=vignette, seed=1708))
    return J

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    J = [j for j in jobs() if not want or j["name"] in want]
    save_layers(OUT, J, B.make_ink)
