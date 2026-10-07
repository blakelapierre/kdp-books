"""Illustrations for Case 19, The Ship's Bell: BLACK-AND-WHITE ink (bwkit) with the simple v1 peg-doll characters.
The sailing club door with the brass bell on its very high hook, the locked ladder cupboard, Agnes's key ring, the broken
stool, and a height chart on the solution board. PART sprites use part_open (clip only, never frame2).
Hook (render.py HOOK_STYLE="ruler"): borderless hero of the club door and the high bell.
Fairness: Loveday, Mr Fenwick and Tobias are drawn at the SAME size, stance and neutral face in the cast strip and the
lineup; their heights (all narrated) appear only as identical text tags. Only the confession shows Tobias sheepish.
Run: python3 art_case19.py [scene ...]"""
import os, sys, math
from functools import partial
import bwkit as B
from bwkit import plate_open, part_open, full_open, InkBW, PW, AW, AH, V2, V3, CW, CH
import figures as F
from inkart import K, Wt
from layers import save_layers

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-19")

def loveday(k, x, y, h, **kw): kw.setdefault("jug_", False); F.loveday(k, x, y, h, **kw)
def fenwick(k, x, y, h, **kw): B.visitor(k, x, y, h, suit="dark", hat="cap", tie=False, moustache=True, **kw)
def tobias(k, x, y, h, **kw): B.visitor(k, x, y, h, suit="check", hat=None, tie=False, **kw)
def agnes(k, x, y, h, **kw): kw.setdefault("teapot", False); F.agnes(k, x, y, h, **kw)

def _bell(k, x, y, s, crack=False):
    """Ship's bell hanging from (x, y) (top of the crown), s = height."""
    k.rect(x - s * 0.08, y - s * 0.16, s * 0.16, s * 0.16, lw=0.9, fill=Wt)
    body = [(x - s * 0.22, y - s * 0.16), (x + s * 0.22, y - s * 0.16), (x + s * 0.3, y - s * 0.75), (x + s * 0.42, y - s * 0.86), (x - s * 0.42, y - s * 0.86), (x - s * 0.3, y - s * 0.75)]
    k.shape(body, lw=1.2, fill=Wt, amp=0); k.hatch(body, angle=80, gap=3.0, lw=0.3)
    k.line([(x - s * 0.3, y - s * 0.7), (x + s * 0.3, y - s * 0.7)], lw=0.8, amp=0)
    k.line([(x, y - s * 0.86), (x, y - s * 1.0)], lw=0.9, amp=0); k.circle(x, y - s * 1.02, s * 0.05, lw=0.8, fill=K)
    if crack: k.line([(x + s * 0.05, y - s * 0.3), (x + s * 0.12, y - s * 0.45), (x + s * 0.06, y - s * 0.55), (x + s * 0.14, y - s * 0.7)], lw=1.2, amp=0)
InkBW.bell = _bell

def _hook(k, x, y):
    k.rect(x - 14, y, 28, 8, lw=0.9, fill=Wt); k.c.setStrokeColor(K); k.c.setLineWidth(1.6); k.c.arc(x - 8, y - 16, x + 8, y, 180, 270)
    k.line([(x, y), (x, y - 8)], lw=1.6, amp=0)
InkBW.hookpeg = _hook

def door_front(k, w, h):
    k.stones(14, w - 14, 14, 44, rows=2)
    k.rect(150, 44, 212, 300, lw=1.3, fill=Wt); k.text(256, 318, "SAILING CLUB", size=13, font="Ink-Plex")
    k.rect(200, 44, 112, 190, lw=1.2, fill=Wt); k.circle(296, 140, 3, lw=0.6, fill=K)
    k.hookpeg(256, 296)

def _stool(k, x, y, s):
    k.rect(x - s * 0.4, y + s * 0.5, s * 0.8, s * 0.1, lw=0.9, fill=Wt)
    k.line([(x - s * 0.3, y + s * 0.5), (x - s * 0.36, y)], lw=1.0, amp=0); k.line([(x + s * 0.3, y + s * 0.5), (x + s * 0.18, y + s * 0.22)], lw=1.0, amp=0)
    k.line([(x + s * 0.24, y + s * 0.12), (x + s * 0.4, y)], lw=1.0, amp=0)
InkBW.stool = _stool

def _keyring(k, x, y, s=1.0):
    k.circle(x, y, 12 * s, lw=1.2, fill=None)
    for i, a in enumerate((-60, -100, -140)):
        ex, ey = x + 12 * s * math.cos(math.radians(a)), y + 12 * s * math.sin(math.radians(a))
        dx, dy = math.cos(math.radians(a)), math.sin(math.radians(a))
        k.circle(ex + dx * 6 * s, ey + dy * 6 * s, 5 * s, lw=0.9, fill=Wt); k.line([(ex + dx * 11 * s, ey + dy * 11 * s), (ex + dx * 30 * s, ey + dy * 30 * s)], lw=1.3, amp=0)
InkBW.keyring = _keyring

# ----------------------------------------------------------------------------- 1. hook hero
def hook_plate(k, w, h): full_open(k, w, h); door_front(k, w, h); k.bell(256, 282, 46); k.unclip()

# ----------------------------------------------------------------------------- 2. cast
CAST = [("LOVEDAY", loveday), ("MR FENWICK", fenwick), ("TOBIAS", tobias)]
cast_plate = B.cast_plate_fn([n for n, _ in CAST], style="tags")

# ----------------------------------------------------------------------------- 3. the bell high above the club door
def door_plate(k, w, h): plate_open(k, w, h); door_front(k, w, h); k.unclip()
def bell_part(k, w, h, v): part_open(k, w, h); k.bell(256, 282, 46); k.unclip()
def tiptoe_part(k, w, h, v): part_open(k, w, h); k.pin_card(400, 250, 100, 52, ["even the tallest:", "on tiptoe!"], size=11); k.unclip()
def empty_part(k, w, h, v): part_open(k, w, h); k.text(330, 266, "empty hook", size=13, font="Ink-Kalam"); k.unclip()
def race_part(k, w, h, v): part_open(k, w, h); k.pin_card(40, 250, 100, 44, ["rung for", "every race"], size=11); k.unclip()

# ----------------------------------------------------------------------------- 4. Tobias ducks through a doorway (6 1/2 ft)
def lb_plate(k, w, h):
    plate_open(k, w, h); k.stones(14, w - 14, 14, 44, rows=2)
    k.rect(60, 44, 390, 240, lw=1.3, fill=Wt); k.text(255, 262, "LIFEBOAT STATION", size=12, font="Ink-Plex")
    k.rect(200, 44, 110, 170, lw=1.2, fill=Wt); k.unclip()
def tobias_duck(k, w, h, v):
    part_open(k, w, h); k.c.saveState(); k.c.translate(255, 44); k.c.rotate(-10); tobias(k, 0, 0, 190); k.c.restoreState(); k.unclip()
def tall_tag(k, w, h, v): part_open(k, w, h); k.rect(340, 120, 100, 40, lw=1.1, fill=Wt); k.text(390, 132, "6\u00bd ft", size=16, font="Ink-Kalam"); k.unclip()

# ----------------------------------------------------------------------------- 5. the locked ladder cupboard, Agnes's key, the broken stool
def porch_plate(k, w, h):
    plate_open(k, w, h); k.floorboards(w, y=60); k.text(256, 334, "THE PORCH", size=12, font="Ink-Plex")
    k.rect(40, 60, 170, 250, lw=1.3, fill=Wt); k.line([(125, 60), (125, 310)], lw=0.8, amp=0); k.text(125, 280, "LADDER", size=11, font="Ink-Plex")
def lock_part(k, w, h, v):
    part_open(k, w, h); x, y = 140, 180
    k.rect(x - 12, y - 12, 24, 20, lw=1.0, fill=K); k.c.setStrokeColor(K); k.c.setLineWidth(2.0); k.c.arc(x - 8, y, x + 8, y + 18, 0, 180)
    k.text(x + 34, y - 6, "locked", size=11, font="Ink-Kalam"); k.unclip()
def ladder_peek(k, w, h, v):
    part_open(k, w, h); k.text(125, 100, "(ladder inside)", size=10, font="Ink-Kalam"); k.unclip()
def keys_part(k, w, h, v):
    part_open(k, w, h); k.keyring(430, 215, 1.4); k.pin_card(380, 300, 110, 44, ["the ONLY key:", "Agnes"], size=11); k.unclip()
def stool_part(k, w, h, v): part_open(k, w, h); k.stool(380, 60, 70); k.text(380, 150, "broken", size=12, font="Ink-Kalam"); k.unclip()
def agnes_p(k, w, h, v): part_open(k, w, h); agnes(k, 270, 60, 180); k.unclip()

# ----------------------------------------------------------------------------- 6. lineup: quiz night (equal sizes; heights as identical tags)
def _p_quiz(k, pw, h): k.floorboards(pw, y=50); k.rect(300, 50, 170, 70, lw=1.1, fill=Wt); k.text(385, 130, "QUIZ NIGHT", size=11, font="Ink-Plex"); k.rect(320, 120, 40, 4, lw=0.6, fill=Wt)
def _p_door(k, pw, h): k.stones(14, pw - 14, 14, 50, rows=2); k.rect(320, 50, 110, 170, lw=1.2, fill=Wt); k.text(375, 230, "CLUB DOOR", size=10, font="Ink-Plex")
def _p_home(k, pw, h):
    k.stones(14, pw - 14, 14, 50, rows=2); k.rect(300, 50, 170, 140, lw=1.2, fill=Wt); k.shape([(290, 190), (480, 190), (385, 240)], lw=1.2, fill=Wt, amp=0)
    k.clock_face(385, 140, 22, 10, 0)
lineup_plate = B.lineup_plate_fn([_p_quiz, _p_door, _p_home], [n for n, _ in CAST])
HT = ["just over 5 ft", "not much taller", "6\u00bd ft"]
def htag(k, w, h, v, i=0):
    part_open(k, w, h); x = i * PW + 300; k.rect(x, 280, 170, 40, lw=1.1, fill=Wt); k.text(x + 85, 292, HT[i], size=14, font="Ink-Kalam"); k.unclip()
SAID = ["\u201cat the quiz table\u201d", "\u201cleft early, headache\u201d", "\u201chome at ten\u201d"]
def said(k, w, h, v, i=0):
    part_open(k, w, h); x = i * PW + 300; k.rect(x, 236, 170, 36, lw=0.9, fill=Wt); k.text(x + 85, 247, SAID[i], size=12, font="Ink-Kalam"); k.unclip()

# ----------------------------------------------------------------------------- 7. Tobias: "I didn't touch the bell"; Agnes jingles her keys
def talk_plate(k, w, h): plate_open(k, w, h); door_front(k, w, h); k.unclip()
def tobias_t(k, w, h, v): part_open(k, w, h); tobias(k, 110, 30, 200); k.unclip()
def agnes_t(k, w, h, v): part_open(k, w, h); agnes(k, 410, 30, 190, flip=True); k.unclip()
def jingle(k, w, h, v): part_open(k, w, h); k.keyring(440, 150, 1.0); k.text(470, 120, "jingle", size=10, font="Ink-Kalam"); k.unclip()

# ----------------------------------------------------------------------------- 8. solution board: who could reach the hook?
GY, FT = 96, 30            # ground y and points per foot on the chart
def board_plate(k, w, h):
    plate_open(k, w, h); k.floorboards(w, y=60)
    k.case_board(24, 70, 464, 290, title="WHO COULD REACH THE HOOK?")
    k.line([(60, GY), (300, GY)], lw=1.0, amp=0)
    for f in range(0, 8):
        k.line([(60, GY + f * FT), (68, GY + f * FT)], lw=0.8, amp=0); k.text(48, GY + f * FT - 4, f"{f}", size=9, font="Ink-Plex")
    k.text(48, GY + 7.4 * FT + 4, "ft", size=9, font="Ink-Plex")
def b_hook(k, w, h, v):
    part_open(k, w, h); y = GY + 6.5 * FT + 22
    for i in range(12): k.line([(70 + i * 20, y), (80 + i * 20, y)], lw=1.0, amp=0)
    k.text(170, y + 6, "the hook: tallest on tiptoe", size=10, font="Ink-Kalam"); k.unclip()
def b_bar(k, w, h, v, i=0):
    part_open(k, w, h); ft = (5.1, 5.4, 6.5)[i]; x = 100 + i * 70
    k.rect(x, GY, 40, ft * FT, lw=1.0, fill=Wt); k.hatch([(x, GY), (x + 40, GY), (x + 40, GY + ft * FT), (x, GY + ft * FT)], angle=45, gap=4, lw=0.3)
    k.text(x + 20, GY - 12, ("LOVEDAY", "FENWICK", "TOBIAS")[i], size=8, font="Ink-Plex"); k.unclip()
def b_ladder(k, w, h, v):
    part_open(k, w, h); k.pin_card(330, 240, 140, 46, ["ladder: locked,", "Agnes has the key"], size=10)
    k.line([(320, 230), (480, 290)], lw=2.0, amp=0); k.unclip()
def b_stool(k, w, h, v):
    part_open(k, w, h); k.pin_card(330, 170, 140, 40, ["stool: broken"], size=11); k.line([(320, 166), (480, 214)], lw=2.0, amp=0); k.unclip()
def b_only(k, w, h, v): part_open(k, w, h); k.shape(k.arcpts(260, GY + 6.6 * FT, 38, 26, 0, 360, 30), lw=2.2, fill=None, amp=0.4); k.text(400, 120, "only Tobias", size=14, font="Ink-Kalam"); k.unclip()

# ----------------------------------------------------------------------------- 9. confession: the mended bell
def conf_plate(k, w, h): plate_open(k, w, h); door_front(k, w, h); k.unclip()
def tobias_c(k, w, h, v): part_open(k, w, h); tobias(k, 110, 30, 200, expr="sheepish" if "sheepish" in v else "neutral"); k.unclip()
def bell_c(k, w, h, v): part_open(k, w, h); k.bell(256, 282, 46); k.unclip()
def crack_part(k, w, h, v): part_open(k, w, h); k.bell(410, 160, 60, crack=True); k.text(410, 70, "cracked", size=11, font="Ink-Kalam"); k.unclip()
def ring_part(k, w, h, v):
    part_open(k, w, h)
    for r in (20, 30, 40): k.c.setStrokeColor(K); k.c.setLineWidth(0.9); k.c.arc(256 - r - 30, 260 - r, 256 + r - 30, 260 + r, 120, 120); k.c.arc(256 - r + 30, 260 - r, 256 + r + 30, 260 + r, -60, 120)
    k.unclip()
def clap_part(k, w, h, v): part_open(k, w, h); k.pin_card(370, 300, 120, 44, ["round of", "applause!"], size=12); k.unclip()

def _vig(k, w, h): k.hookpeg(w / 2, h * 0.8); k.bell(w / 2, h * 0.78, h * 0.5)
vignette = B.vignette_fn(_vig)

def jobs():
    J = []
    J.append(dict(name="hook", w=AW, h=AH, plate=hook_plate, seed=1901))
    J.append(dict(name="cast", w=CW, h=CH, plate=cast_plate, seed=1902, parts={
        f"s{i}": dict(fn=B.cast_fig_fn(i, 3, fn), variants=V2) for i, (_, fn) in enumerate(CAST)}))
    J.append(dict(name="door", w=AW, h=AH, plate=door_plate, seed=1903, parts=dict(
        bell=dict(fn=bell_part, variants=["base"]), tiptoe=dict(fn=tiptoe_part, variants=["base"]), empty=dict(fn=empty_part, variants=["base"]), race=dict(fn=race_part, variants=["base"]))))
    J.append(dict(name="lb", w=AW, h=AH, plate=lb_plate, seed=1904, parts=dict(tobias=dict(fn=tobias_duck, variants=V2), tall=dict(fn=tall_tag, variants=["base"]))))
    J.append(dict(name="porch", w=AW, h=AH, plate=porch_plate, seed=1905, parts=dict(
        lock=dict(fn=lock_part, variants=["base"]), peek=dict(fn=ladder_peek, variants=["base"]), keys=dict(fn=keys_part, variants=["base"]),
        stool=dict(fn=stool_part, variants=["base"]), agnes=dict(fn=agnes_p, variants=V2))))
    J.append(dict(name="lineup", w=3 * PW, h=AH, plate=lineup_plate, seed=1906, parts={
        **{f"s{i}": dict(fn=B.lineup_fig_fn(i, fn, x=PW / 2 - 140, y=50, fh=220), variants=V3) for i, (_, fn) in enumerate(CAST)},
        **{f"h{i}": dict(fn=partial(htag, i=i), variants=["base"]) for i in range(3)},
        **{f"q{i}": dict(fn=partial(said, i=i), variants=["base"]) for i in range(3)}}))
    J.append(dict(name="talk", w=AW, h=AH, plate=talk_plate, seed=1907, parts=dict(
        tobias=dict(fn=tobias_t, variants=V3), agnes=dict(fn=agnes_t, variants=V2), jingle=dict(fn=jingle, variants=["base"]))))
    J.append(dict(name="board", w=AW, h=AH, plate=board_plate, seed=1908, parts={
        "hook": dict(fn=b_hook, variants=["base"]), **{f"b{i}": dict(fn=partial(b_bar, i=i), variants=["base"]) for i in range(3)},
        "ladder": dict(fn=b_ladder, variants=["base"]), "stool": dict(fn=b_stool, variants=["base"]), "only": dict(fn=b_only, variants=["base"])}))
    J.append(dict(name="confess", w=AW, h=AH, plate=conf_plate, seed=1909, parts=dict(
        tobias=dict(fn=tobias_c, variants=["sheepish", "sheepish+blink"]), bell=dict(fn=bell_c, variants=["base"]), crack=dict(fn=crack_part, variants=["base"]),
        ring=dict(fn=ring_part, variants=["base"]), clap=dict(fn=clap_part, variants=["base"]))))
    J.append(dict(name="vignette", w=384, h=384, plate=vignette, seed=1910))
    return J

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    J = [j for j in jobs() if not want or j["name"] in want]
    save_layers(OUT, J, B.make_ink)
