"""Illustrations for Case 25, The Teaspoon Thief: BLACK-AND-WHITE ink (bwkit) with the simple v1 peg-doll characters.
The Kettle and Gull's sideboard under the back window (open a hand's width at the top), the tray of silver teaspoons that
loses one spoon a morning, the untouched things (coin jar, wooden spoons, dull pewter spoon, sugar bowl, shortbread), the
three helpers with equal tags, the glossy black-and-white feather on the sill, a "shiny things only" board and the nest.
PART sprites use part_open (clip only, never frame2). Silver = white with sparkle ticks; pewter = grey hatch (dull).
Hook (render.py HOOK_STYLE="spooncount"): borderless hero of the sideboard and the back window.
Fairness: Pip, Mr Fenwick and Loveday share stance, height, arms-down pose and neutral face; equal-size tags. The magpie is
drawn only after "The Solution".
Run: python3 art_case25.py [scene ...]"""
import os, sys, math
from functools import partial
import bwkit as B
from bwkit import plate_open, part_open, full_open, InkBW, PW, AW, AH, V2, V3, CW, CH
import figures as F
from inkart import K, Wt
from layers import save_layers

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-25")

def pip(k, x, y, h, **kw): kw.setdefault("prop", False); F.pip(k, x, y, h, **kw)
def fenwick(k, x, y, h, **kw): B.visitor(k, x, y, h, suit="dark", hat="cap", tie=False, moustache=True, **kw)
def loveday(k, x, y, h, **kw): kw.setdefault("jug_", False); kw.setdefault("expr", "neutral"); F.loveday(k, x, y, h, **kw)
def agnes(k, x, y, h, **kw): kw.setdefault("teapot", False); F.agnes(k, x, y, h, **kw)

def _spoon(k, x, y, s, shiny=True, wood=False, ang=0):
    """Teaspoon lying flat, bowl at the right; (x, y) = handle end."""
    a = math.radians(ang); ca, sa = math.cos(a), math.sin(a); R = lambda u, v: (x + u * ca - v * sa, y + u * sa + v * ca)
    k.line([R(0, 0), R(s * 0.65, 0)], lw=1.6 if wood else 1.1, amp=0)
    bowl = [R(s * 0.65 + s * 0.18 * (1 + math.cos(t)), s * 0.11 * math.sin(t)) for t in [i * math.pi / 8 for i in range(17)]]
    k.shape(bowl, lw=0.9, fill=Wt, amp=0)
    if wood: k.hatch(bowl, angle=0, gap=1.4, lw=0.3)
    elif not shiny: k.hatch(bowl, angle=45, gap=1.2, lw=0.35, cross=True)
    else:
        cx, cy = R(s * 0.83, 0)
        for dx, dy in ((0, 1), (0.7, 0.7), (1, 0)): k.line([(cx + dx * s * 0.08, cy + dy * s * 0.08 + s * 0.08), (cx + dx * s * 0.15, cy + dy * s * 0.15 + s * 0.08)], lw=0.5, amp=0)
InkBW.spoon = _spoon

def _feather(k, x, y, s):
    """Long glossy black feather with a bright white patch near the end; (x, y) = quill tip, lying to the right."""
    pts = [(x, y)] + [(x + s * u, y + s * 0.09 * math.sin(math.pi * u)) for u in (0.2, 0.5, 0.8, 1.0)] + [(x + s * u, y - s * 0.07 * math.sin(math.pi * u)) for u in (0.8, 0.5, 0.2)]
    k.shape(pts, lw=0.8, fill=K, amp=0)
    k.shape([(x + s * 0.72, y + s * 0.06), (x + s * 0.9, y + s * 0.04), (x + s * 0.9, y - s * 0.03), (x + s * 0.72, y - s * 0.05)], lw=0.4, fill=Wt, amp=0)
    k.line([(x - s * 0.08, y), (x + s * 0.98, y)], lw=0.4, amp=0)
InkBW.feather = _feather

def _magpie(k, x, y, s):
    body = k.arcpts(x, y + s * 0.35, s * 0.3, s * 0.2, 0, 360, 22); k.shape(body, lw=1.0, fill=K, amp=0)
    k.shape(k.arcpts(x - s * 0.02, y + s * 0.3, s * 0.16, s * 0.1, 0, 360, 16), lw=0.5, fill=Wt, amp=0)   # white belly
    k.circle(x + s * 0.32, y + s * 0.5, s * 0.12, lw=0.9, fill=K); k.circle(x + s * 0.35, y + s * 0.53, s * 0.025, lw=0, fill=Wt, stroke=False)
    k.shape([(x + s * 0.42, y + s * 0.52), (x + s * 0.56, y + s * 0.48), (x + s * 0.42, y + s * 0.45)], lw=0.6, fill=K, amp=0)
    k.shape([(x - s * 0.25, y + s * 0.38), (x - s * 0.8, y + s * 0.55), (x - s * 0.82, y + s * 0.48), (x - s * 0.25, y + s * 0.3)], lw=0.8, fill=K, amp=0)  # long tail
    k.shape(k.arcpts(x + s * 0.02, y + s * 0.42, s * 0.14, s * 0.06, 0, 360, 12), lw=0.4, fill=Wt, amp=0)   # wing patch
    for lx in (-0.05, 0.08): k.line([(x + s * lx, y + s * 0.16), (x + s * lx, y)], lw=0.7, amp=0)
InkBW.magpie = _magpie

def _dog(k, x, y, s):
    k.shape(k.arcpts(x, y + s * 0.35, s * 0.32, s * 0.16, 0, 360, 18), lw=0.9, fill=Wt, amp=0.1)
    k.circle(x + s * 0.34, y + s * 0.5, s * 0.13, lw=0.9, fill=Wt); k.circle(x + s * 0.4, y + s * 0.52, s * 0.02, lw=0, fill=K, stroke=False)
    k.shape([(x + s * 0.28, y + s * 0.6), (x + s * 0.3, y + s * 0.72), (x + s * 0.36, y + s * 0.6)], lw=0.6, fill=K, amp=0)
    for lx in (-0.22, -0.1, 0.12, 0.22): k.line([(x + s * lx, y + s * 0.22), (x + s * lx, y)], lw=0.9, amp=0)
    k.line([(x - s * 0.3, y + s * 0.4), (x - s * 0.42, y + s * 0.55)], lw=0.8, amp=0.2)
InkBW.dog = _dog

def _sideboard(k, w, h):
    k.floorboards(w, y=60)
    k.rect(60, 60, 392, 90, lw=1.3, fill=Wt); k.line([(60, 150), (452, 150)], lw=1.6, amp=0)
    for dx in (160, 256, 352): k.line([(dx, 64), (dx, 146)], lw=0.5, amp=0)
    # back window above: open a hand's width at the top
    k.rect(150, 190, 210, 160, lw=1.3, fill=Wt); k.rect(156, 196, 198, 120, lw=0.8, fill=Wt)
    k.rect(156, 330, 198, 14, lw=0.8, fill=K)
    k.text(255, 360, "BACK WINDOW", size=9, font="Ink-Plex")
    # untouched things
    k.rect(80, 150, 34, 40, lw=0.9, fill=Wt); k.text(97, 166, "RNLI", size=6, font="Ink-Plex"); k.coins(97, 178, n=5)
    k.spoon(380, 158, 50, wood=True); k.spoon(380, 168, 50, wood=True)
    k.spoon(380, 180, 46, shiny=False)
    k.shape(k.arcpts(130, 158, 16, 8, 180, 360, 12), lw=0.9, fill=Wt, amp=0); k.rect(114, 158, 32, 14, lw=0.9, fill=Wt); k.text(130, 162, "SUGAR", size=5, font="Ink-Plex")
    k.shape(k.arcpts(440, 150, 26, 18, 0, 180, 14), lw=0.9, fill=Wt, amp=0); k.text(440, 156, "cloth", size=7, font="Ink-Kalam")
    k.rect(200, 150, 110, 16, lw=1.0, fill=Wt); k.text(255, 136, "tray of clean spoons", size=9, font="Ink-Kalam")

# ----------------------------------------------------------------------------- 1. hook hero
def hook_plate(k, w, h):
    full_open(k, w, h); _sideboard(k, w, h)
    for i in range(3): k.spoon(206 + i * 34, 160, 30)
    k.unclip()

# ----------------------------------------------------------------------------- 2. cast
CAST = [("PIP", pip), ("MR FENWICK", fenwick), ("LOVEDAY", loveday)]
cast_plate = B.cast_plate_fn([n for n, _ in CAST], style="frames")

# ----------------------------------------------------------------------------- 3. tea room front
def tea_plate(k, w, h): plate_open(k, w, h); k.tearoom(w, h, window=True, counter=True); k.unclip()
def three_part(k, w, h, v): part_open(k, w, h); k.pin_card(170, 290, 180, 40, ["3 mornings in a row:", "a silver teaspoon gone"], size=11); k.unclip()

# ----------------------------------------------------------------------------- 4. the sideboard
def sb_plate(k, w, h): plate_open(k, w, h); _sideboard(k, w, h); k.unclip()
def spoon_i(k, w, h, v, i=0): part_open(k, w, h); k.spoon(206 + i * 34, 160, 30); k.unclip()
def agnes_s(k, w, h, v): part_open(k, w, h); agnes(k, 40, 30, 150); k.unclip()
def keys_part(k, w, h, v): part_open(k, w, h); k.pin_card(370, 290, 120, 46, ["both doors locked;", "only keys: Agnes"], size=10); k.unclip()
def gap_part(k, w, h, v):
    part_open(k, w, h); k.line([(366, 330), (366, 344)], lw=0.8, amp=0)
    k.pin_card(366, 230, 130, 46, ["open at the top:", "a hand's width"], size=10); k.line([(366, 276), (356, 334)], lw=0.6, amp=0); k.unclip()
def nobody_part(k, w, h, v): part_open(k, w, h); k.pin_card(20, 290, 130, 46, ["too small for", "anyone, even a child"], size=9); k.unclip()
def day_part(k, w, h, v, i=0):
    part_open(k, w, h); x = 200 + i * 40; lab = ("MON", "TUE", "WED")[i]
    k.rect(x - 2, 100, 36, 22, lw=0.9, fill=Wt); k.text(x + 16, 106, lab + " \u22121", size=8, font="Ink-Plex"); k.unclip()
def foil_part(k, w, h, v):
    part_open(k, w, h); k.shape([(320, 154), (334, 158), (330, 166), (318, 163)], lw=0.7, fill=Wt, amp=0.3)
    k.pin_card(300, 80, 130, 30, ["+ Pip's silver foil"], size=9); k.unclip()
def untouched_part(k, w, h, v, i=0):
    part_open(k, w, h); x, y = ((97, 200), (404, 196), (404, 210), (130, 182), (440, 182))[i]
    k.rect(x - 22, y, 44, 12, lw=0.6, fill=Wt); k.text(x, y + 3, "untouched", size=6, font="Ink-Kalam"); k.unclip()
def shiny_part(k, w, h, v): part_open(k, w, h); k.pin_card(20, 230, 130, 34, ["only the SHINY went"], size=10); k.unclip()

# ----------------------------------------------------------------------------- 5. lineup
def _bigspoon(k, pw, h): k.floorboards(pw, y=50); k.tearoom(pw, h, window=True, counter=False) if False else k.rect(320, 50, 150, 100, lw=1.0, fill=Wt)
def _grocer(k, pw, h):
    k.stones(14, pw - 14, 14, 50, rows=2); k.rect(250, 50, 220, 200, lw=1.1, fill=Wt); k.rect(260, 210, 200, 28, lw=0.8, fill=Wt); k.text(360, 218, "FENWICK GROCER", size=10, font="Ink-Plex")
    k.text(360, 150, "open from 5 am", size=9, font="Ink-Kalam")
def _bed(k, pw, h):
    k.floorboards(pw, y=50); k.rect(300, 50, 180, 50, lw=1.0, fill=Wt); k.rect(300, 100, 40, 50, lw=1.0, fill=Wt); k.shape(k.arcpts(360, 100, 50, 14, 0, 180, 12), lw=0.8, fill=Wt, amp=0)
lineup_plate = B.lineup_plate_fn([_bigspoon, _grocer, _bed], [n for n, _ in CAST])
FX, FY, FH = PW / 2 - 160, 50, 220
TAGS = [["can't stand teaspoons;", "only ever uses a big spoon"], ["at the grocer's from 5 a.m.;", "delivery driver confirms"], ["at home in bed with Pickle;", "neither had keys"]]
def ltag(k, w, h, v, i=0):
    part_open(k, w, h); x = i * PW + 236; k.rect(x, 286, 250, 50, lw=1.1, fill=Wt)
    for j, ln in enumerate(TAGS[i]): k.text(x + 125, 318 - j * 20, ln, size=11, font="Ink-Kalam")
    k.unclip()
def pickle_part(k, w, h, v): part_open(k, w, h); k.dog(2 * PW + 380, 102, 50); k.text(2 * PW + 380, 172, "Pickle", size=9, font="Ink-Kalam"); k.unclip()

# ----------------------------------------------------------------------------- 6. the windowsill: the feather
def sill_plate(k, w, h):
    plate_open(k, w, h); k.rect(60, 60, 392, 240, lw=1.4, fill=Wt); k.rect(70, 70, 372, 170, lw=0.9, fill=Wt)
    k.rect(70, 262, 372, 30, lw=0.9, fill=K); k.rect(40, 52, 432, 14, lw=1.1, fill=Wt)
    k.text(256, 310, "the back windowsill, under the gap", size=10, font="Ink-Kalam"); k.unclip()
def feather_part(k, w, h, v): part_open(k, w, h); k.feather(120, 110, 170); k.unclip()
def fcard_part(k, w, h, v): part_open(k, w, h); k.pin_card(110, 170, 150, 46, ["long, glossy, black;", "white patch near the end"], size=10); k.unclip()
def agnes_w(k, w, h, v): part_open(k, w, h); agnes(k, 440, 30, 130, flip=True); k.unclip()

# ----------------------------------------------------------------------------- 7. solution board
def board_plate(k, w, h): plate_open(k, w, h); k.floorboards(w, y=56); k.case_board(24, 66, 464, 292, title="WHO COULD GET IN?")
def b_bird(k, w, h, v): part_open(k, w, h); k.magpie(380, 220, 80); k.pin_card(330, 170, 120, 26, ["a MAGPIE"], size=12); k.unclip()
def b_gap(k, w, h, v): part_open(k, w, h); k.pin_card(44, 270, 230, 44, ["doors locked, Agnes's keys;", "gap: too small for a person, not a bird"], size=9); k.unclip()
def b_took(k, w, h, v):
    part_open(k, w, h); k.text(150, 236, "TOOK: silver spoons, silver foil", size=10, font="Ink-Kalam")
    for i in range(3): k.spoon(60 + i * 30, 210, 26)
    k.unclip()
def b_left(k, w, h, v): part_open(k, w, h); k.text(150, 180, "LEFT: coins, pewter, wood, shortbread", size=10, font="Ink-Kalam"); k.line([(46, 184), (256, 184)], lw=1.2, amp=0.2); k.unclip()
def b_feather(k, w, h, v): part_open(k, w, h); k.feather(60, 110, 120); k.pin_card(200, 96, 140, 30, ["a magpie feather!"], size=10); k.unclip()

# ----------------------------------------------------------------------------- 8. the nest in the apple tree
def nest_plate(k, w, h):
    plate_open(k, w, h); k.line([(14, 60), (w - 14, 60)], lw=0.9, amp=0.1)
    k.rect(240, 60, 30, 170, lw=1.2, fill=Wt)
    for a, b in (((255, 200), (140, 290)), ((255, 220), (380, 300)), ((255, 180), (400, 230))): k.line([a, b], lw=2.0, amp=0.3)
    for cx, cy in ((150, 300), (200, 320), (330, 320), (390, 300), (260, 340)): k.circle(cx, cy, 30, lw=0.8, fill=Wt)
    k.unclip()
def nest_part(k, w, h, v):
    part_open(k, w, h); k.shape(k.arcpts(360, 226, 40, 14, 180, 360, 16), lw=1.2, fill=Wt, amp=0.3)
    for j in range(8): k.line([(325 + j * 9, 222), (330 + j * 9, 214)], lw=0.4, amp=0.3)
    k.unclip()
def loot_part(k, w, h, v):
    part_open(k, w, h); [k.spoon(328 + i * 8, 228 + i * 3, 24, ang=15) for i in range(3)]; k.circle(390, 230, 3, lw=0.6, fill=Wt); k.circle(398, 228, 3, lw=0.6, fill=Wt)
    k.pin_card(330, 120, 150, 46, ["3 spoons, foil, 2 bottle tops,", "Loveday's lost button"], size=9); k.unclip()
def pip_n(k, w, h, v): part_open(k, w, h); pip(k, 120, 40, 150); k.unclip()
def bird_n(k, w, h, v): part_open(k, w, h); k.magpie(420, 310, 50); k.unclip()
def thanks_part(k, w, h, v): part_open(k, w, h); k.pin_card(20, 290, 160, 46, ["window shut at night;", "a bottle top: thank you!"], size=10); k.unclip()

def _vig(k, w, h): k.spoon(w * 0.18, h * 0.5, w * 0.6)
vignette = B.vignette_fn(_vig)

def jobs():
    J = []
    J.append(dict(name="hook", w=AW, h=AH, plate=hook_plate, seed=2501))
    J.append(dict(name="cast", w=CW, h=CH, plate=cast_plate, seed=2502, parts={
        f"s{i}": dict(fn=B.cast_fig_fn(i, 3, fn), variants=V2) for i, (_, fn) in enumerate(CAST)}))
    J.append(dict(name="tea", w=AW, h=AH, plate=tea_plate, seed=2503, parts=dict(three=dict(fn=three_part, variants=["base"]))))
    J.append(dict(name="sideboard", w=AW, h=AH, plate=sb_plate, seed=2504, parts={
        **{f"sp{i}": dict(fn=partial(spoon_i, i=i), variants=["base"]) for i in range(3)},
        **{f"d{i}": dict(fn=partial(day_part, i=i), variants=["base"]) for i in range(3)},
        **{f"u{i}": dict(fn=partial(untouched_part, i=i), variants=["base"]) for i in range(5)},
        "agnes": dict(fn=agnes_s, variants=V2), "keys": dict(fn=keys_part, variants=["base"]), "gap": dict(fn=gap_part, variants=["base"]),
        "nobody": dict(fn=nobody_part, variants=["base"]), "foil": dict(fn=foil_part, variants=["base"]), "shiny": dict(fn=shiny_part, variants=["base"])}))
    J.append(dict(name="lineup", w=3 * PW, h=AH, plate=lineup_plate, seed=2505, parts={
        **{f"s{i}": dict(fn=B.lineup_fig_fn(i, fn, x=FX, y=FY, fh=FH), variants=V3) for i, (_, fn) in enumerate(CAST)},
        **{f"p{i}": dict(fn=partial(ltag, i=i), variants=["base"]) for i in range(3)}, "pickle": dict(fn=pickle_part, variants=["base"])}))
    J.append(dict(name="sill", w=AW, h=AH, plate=sill_plate, seed=2506, parts=dict(
        feather=dict(fn=feather_part, variants=["base"]), fcard=dict(fn=fcard_part, variants=["base"]), agnes=dict(fn=agnes_w, variants=V2))))
    J.append(dict(name="board", w=AW, h=AH, plate=board_plate, seed=2507, parts=dict(
        bird=dict(fn=b_bird, variants=["base"]), gap=dict(fn=b_gap, variants=["base"]), took=dict(fn=b_took, variants=["base"]),
        left=dict(fn=b_left, variants=["base"]), feather=dict(fn=b_feather, variants=["base"]))))
    J.append(dict(name="nest", w=AW, h=AH, plate=nest_plate, seed=2508, parts=dict(
        nest=dict(fn=nest_part, variants=["base"]), loot=dict(fn=loot_part, variants=["base"]), pip=dict(fn=pip_n, variants=V2),
        bird=dict(fn=bird_n, variants=["base"]), thanks=dict(fn=thanks_part, variants=["base"]))))
    J.append(dict(name="vignette", w=384, h=384, plate=vignette, seed=2509))
    return J

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    J = [j for j in jobs() if not want or j["name"] in want]
    save_layers(OUT, J, B.make_ink)
