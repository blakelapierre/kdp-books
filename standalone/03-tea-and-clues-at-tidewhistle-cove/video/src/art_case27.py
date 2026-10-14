"""Illustrations for Case 27, The Silent Foghorn: BLACK-AND-WHITE ink (bwkit) with the simple v1 peg-doll characters.
The foghorn at the end of the harbour wall (booms by itself in fog, heard from every house), Agnes awake 10 pm-3 am with her
window open on a CLEAR, STARRY night (silent foghorn), the yacht in the bay missing its brass barometer, the dinghy on the
wrong side of the jetty, three people with equal tags, and a "FOG OR CLEAR?" board.
PART sprites use part_open (clip only, never frame2).
Hook (render.py HOOK_STYLE="foghorn"): borderless hero of the harbour wall and the foghorn under the stars.
Fairness: Captain Quill, Tamsin and Mr Keast share stance, height, arms-down pose and neutral face; equal-size tags.
Only the confession shows Keast red-faced.
Run: python3 art_case27.py [scene ...]"""
import os, sys, math, random
from functools import partial
import bwkit as B
from bwkit import plate_open, part_open, full_open, InkBW, PW, AW, AH, V2, V3, CW, CH
import figures as F
from inkart import K, Wt
from layers import save_layers

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-27" + os.environ.get("TW_ART_SUFFIX", ""))

def quill(k, x, y, h, **kw): kw.setdefault("prop", False); F.quill(k, x, y, h, **kw)
def tamsin(k, x, y, h, **kw): kw.setdefault("prop", None); kw.setdefault("expr", "neutral"); F.tamsin(k, x, y, h, **kw)
def keast(k, x, y, h, **kw): B.visitor(k, x, y, h, suit="check", hat="panama", tie=True, **kw)
def agnes(k, x, y, h, **kw): kw.setdefault("teapot", False); F.agnes(k, x, y, h, **kw)

def _night(k, x0, y0, x1, y1, seed=27, n=34):
    sky = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    k.hatch(sky, angle=-30, gap=3.0, lw=0.35, cross=True)
    rr = random.Random(seed)
    for _ in range(n):
        x, y, r = rr.uniform(x0 + 8, x1 - 8), rr.uniform(y0 + 8, y1 - 8), rr.uniform(1.4, 3.2)
        k.circle(x, y, r * 1.4, lw=0, fill=Wt, stroke=False)
        k.line([(x - r * 1.6, y), (x + r * 1.6, y)], lw=0.5, amp=0); k.line([(x, y - r * 1.6), (x, y + r * 1.6)], lw=0.5, amp=0)
InkBW.night27 = _night

def _foghorn(k, x, y, s):
    """Foghorn on a little stone plinth at the end of the wall; trumpet facing right; (x, y) = plinth base centre."""
    k.rect(x - s * 0.25, y, s * 0.5, s * 0.4, lw=1.1, fill=Wt); k.hatch([(x - s * 0.25, y), (x + s * 0.25, y), (x + s * 0.25, y + s * 0.4), (x - s * 0.25, y + s * 0.4)], angle=0, gap=4, lw=0.3)
    k.rect(x - s * 0.08, y + s * 0.4, s * 0.16, s * 0.3, lw=1.0, fill=Wt)
    k.shape([(x - s * 0.1, y + s * 0.68), (x + s * 0.2, y + s * 0.72), (x + s * 0.55, y + s * 0.58), (x + s * 0.55, y + s * 1.02), (x + s * 0.2, y + s * 0.86), (x - s * 0.1, y + s * 0.9)], lw=1.2, fill=Wt, amp=0)
    k.shape(k.arcpts(x + s * 0.55, y + s * 0.8, s * 0.06, s * 0.22, 0, 360, 16), lw=1.0, fill=K, amp=0)
InkBW.foghorn = _foghorn

def _fog(k, x0, x1, y0, y1, n=7, seed=3):
    rr = random.Random(seed)
    for i in range(n):
        y = y0 + (y1 - y0) * i / n; xs = rr.uniform(x0, x0 + 30)
        k.line([(xs, y), (xs + 60, y + 6), (xs + 140, y), (xs + 220, y + 6), (min(x1, xs + 300), y)], lw=0.6, amp=0.5)
InkBW.fogbank = _fog

def _yacht(k, x, y, w, baro=True):
    hull = [(x - w / 2, y + w * 0.12), (x + w / 2, y + w * 0.12), (x + w * 0.38, y), (x - w * 0.4, y)]
    k.shape(hull, lw=1.1, fill=Wt, amp=0); k.rect(x - w * 0.18, y + w * 0.12, w * 0.3, w * 0.1, lw=0.9, fill=Wt)
    k.line([(x, y + w * 0.22), (x, y + w * 0.95)], lw=1.2, amp=0)
    k.shape([(x + 2, y + w * 0.93), (x + w * 0.4, y + w * 0.26), (x + 2, y + w * 0.26)], lw=0.9, fill=Wt, amp=0)
    if baro: _barometer(k, x - w * 0.05, y + w * 0.17, w * 0.06)
InkBW.yacht = _yacht

def _barometer(k, x, y, r):
    k.circle(x, y, r, lw=1.0, fill=Wt); k.circle(x, y, r * 0.75, lw=0.4, fill=None)
    k.line([(x, y), (x + r * 0.5, y + r * 0.45)], lw=0.6, amp=0)
    for a in range(0, 360, 45): k.line([(x + r * 0.78 * math.cos(math.radians(a)), y + r * 0.78 * math.sin(math.radians(a))), (x + r * 0.9 * math.cos(math.radians(a)), y + r * 0.9 * math.sin(math.radians(a)))], lw=0.4, amp=0)
InkBW.barometer = _barometer

def _wall(k, w, h, night=True):
    if night: k.night27(14, 150, w - 14, h - 14)
    k.sea(14, w - 14, 60, 150, rows=5); k.rect(14, 60, 330, 60, lw=1.2, fill=Wt); k.stones(14, 344, 62, 118, rows=3)

# ----------------------------------------------------------------------------- 1. hook hero
def hook_plate(k, w, h): full_open(k, w, h); _wall(k, w, h); k.foghorn(300, 120, 90); k.unclip()

# ----------------------------------------------------------------------------- 2. cast
CAST = [("CAPTAIN QUILL", quill), ("TAMSIN", tamsin), ("MR KEAST", keast)]
cast_plate = B.cast_plate_fn([n for n, _ in CAST], style="cards")

# ----------------------------------------------------------------------------- 3. the foghorn (daytime explainer)
def horn_plate(k, w, h): plate_open(k, w, h); _wall(k, w, h, night=False); k.foghorn(300, 120, 90); k.unclip()
def fog_part(k, w, h, v): part_open(k, w, h); k.fogbank(14, w - 14, 160, 330); k.unclip()
def boom_part(k, w, h, v):
    part_open(k, w, h)
    for r in (20, 34, 48): k.shape(k.arcpts(356, 195, r, r * 1.2, -50, 50, 10), lw=1.0, fill=None, amp=0)
    k.pin_card(330, 270, 160, 46, ["fog = BOOM by itself,", "every half a minute"], size=10); k.unclip()
def houses_part(k, w, h, v): part_open(k, w, h); k.pin_card(20, 290, 170, 40, ["heard from every", "house in the village"], size=10); k.unclip()
def cat_part(k, w, h, v): part_open(k, w, h); k.pin_card(20, 230, 170, 30, ["(it only wakes the cat)"], size=10); k.unclip()

# ----------------------------------------------------------------------------- 4. Agnes awake: window open, clear starry night
def bed_plate(k, w, h):
    plate_open(k, w, h); k.floorboards(w, y=56)
    k.rect(260, 150, 210, 180, lw=1.4, fill=Wt); k.night27(266, 156, 464, 324, seed=8)
    k.line([(365, 156), (365, 324)], lw=1.0, amp=0)
    k.rect(40, 56, 230, 60, lw=1.2, fill=Wt); k.rect(40, 116, 40, 70, lw=1.2, fill=Wt); k.shape(k.arcpts(170, 116, 90, 16, 0, 180, 14), lw=0.9, fill=Wt, amp=0)
    k.unclip()
def agnes_b(k, w, h, v): part_open(k, w, h); agnes(k, 130, 90, 120); k.unclip()
def lemon_part(k, w, h, v): part_open(k, w, h); k.rect(214, 120, 18, 22, lw=0.8, fill=Wt); k.text(223, 104, "honey & lemon", size=8, font="Ink-Kalam"); k.unclip()
def open_part(k, w, h, v): part_open(k, w, h); k.pin_card(290, 100, 170, 30, ["window open"], size=10); k.unclip()
def hours_part(k, w, h, v): part_open(k, w, h); k.pin_card(20, 290, 170, 40, ["awake, reading:", "10 p.m. \u2013 3 a.m."], size=10); k.unclip()
def clear_part(k, w, h, v): part_open(k, w, h); k.pin_card(290, 336, 170, 30, ["clear and starry"], size=10); k.unclip()
def silent_part(k, w, h, v): part_open(k, w, h); k.pin_card(20, 230, 170, 40, ["the foghorn never", "sounded once"], size=10); k.unclip()

# ----------------------------------------------------------------------------- 5. the bay: yacht, barometer gone, dinghy
def bay_plate(k, w, h):
    plate_open(k, w, h); k.sea(14, w - 14, 60, 220, rows=7)
    k.rect(14, 60, 120, 24, lw=1.0, fill=Wt); [k.line([(20 + j * 20, 60), (20 + j * 20, 40)], lw=0.8, amp=0) for j in range(6)]
    k.text(70, 90, "JETTY", size=9, font="Ink-Plex"); k.unclip()
def yacht_part(k, w, h, v): part_open(k, w, h); k.yacht(320, 140, 160); k.unclip()
def yacht_nob(k, w, h, v): part_open(k, w, h); k.yacht(320, 140, 160, baro=False); k.dashed_outline(312, 159, 20, 20); k.unclip()
def gone_part(k, w, h, v): part_open(k, w, h); k.pin_card(330, 300, 160, 40, ["Wednesday morning:", "brass barometer gone"], size=10); k.unclip()
def dinghy_part(k, w, h, v):
    part_open(k, w, h); k.shape([(140, 70), (190, 70), (182, 58), (148, 58)], lw=1.0, fill=Wt, amp=0)
    k.pin_card(130, 140, 160, 40, ["dinghy tied up on the", "WRONG side of the jetty"], size=9); k.unclip()

# ----------------------------------------------------------------------------- 6. lineup
def _office(k, pw, h): k.line([(14, 50), (pw - 14, 50)], lw=0.9, amp=0.1); k.rect(290, 50, 180, 170, lw=1.1, fill=Wt); k.text(380, 196, "HARBOUR OFFICE", size=9, font="Ink-Plex"); k.window(320, 100, 50, 50) if False else k.rect(320, 100, 50, 50, lw=0.8, fill=Wt)
def _bus(k, pw, h): k.line([(14, 50), (pw - 14, 50)], lw=0.9, amp=0.1); k.line([(380, 50), (380, 250)], lw=1.4, amp=0); k.rect(352, 244, 56, 30, lw=1.0, fill=Wt); k.text(380, 254, "BUS", size=10, font="Ink-Plex")
def _home(k, pw, h): k.floorboards(pw, y=50); k.rect(300, 140, 160, 120, lw=1.1, fill=Wt); k.rect(306, 146, 148, 108, lw=0.6, fill=Wt)
lineup_plate = B.lineup_plate_fn([_office, _bus, _home], [n for n, _ in CAST])
FX, FY, FH = PW / 2 - 160, 50, 220
TAGS = [["night watch, harbour office,", "2 lifeboat crew, 10 \u2013 dawn"], ["at her sister's in town;", "first bus back"], ["visitor; admired the yacht's", "brass fittings all week"]]
def ltag(k, w, h, v, i=0):
    part_open(k, w, h); x = i * PW + 236; k.rect(x, 286, 250, 50, lw=1.1, fill=Wt)
    for j, ln in enumerate(TAGS[i]): k.text(x + 125, 318 - j * 20, ln, size=11, font="Ink-Kalam")
    k.unclip()
SAID = ["\u201cHome all night. Fog so thick you", "couldn't see your hand. That foghorn", "kept me awake half the night, booming.\u201d"]
def said_part(k, w, h, v):
    part_open(k, w, h); x = 2 * PW + 196; k.rect(x, 190, 300, 78, lw=1.1, fill=Wt)
    for j, ln in enumerate(SAID): k.text(x + 150, 250 - j * 20, ln, size=10, font="Ink-Kalam")
    k.unclip()

# ----------------------------------------------------------------------------- 7. board
def board_plate(k, w, h):
    plate_open(k, w, h); k.floorboards(w, y=56); k.case_board(24, 66, 464, 292, title="FOG OR CLEAR?")
    k.line([(256, 110), (256, 316)], lw=0.8, amp=0.1)
def b_keast(k, w, h, v): part_open(k, w, h); k.text(140, 300, "KEAST SAYS", size=11, font="Ink-Plex"); k.pin_card(50, 220, 180, 60, ["thick fog,", "foghorn booming", "half the night"], size=10); k.unclip()
def b_agnes(k, w, h, v): part_open(k, w, h); k.text(372, 300, "AGNES HEARD", size=11, font="Ink-Plex"); k.pin_card(282, 220, 180, 60, ["window open 10 \u2013 3,", "clear and starry,", "not one boom"], size=10); k.unclip()
def b_x(k, w, h, v):
    part_open(k, w, h)
    for a, b in (((60, 214), (220, 290)), ((220, 214), (60, 290))): k.line([a, b], lw=2.6, amp=0.3)
    k.text(140, 196, "no fog, no booming", size=10, font="Ink-Kalam"); k.unclip()
def b_row(k, w, h, v, i=0):
    part_open(k, w, h); y = (150, 124)[i]; txt = ("Quill: on watch with two crew", "Tamsin: in town all night")[i]
    k.text(256, y, txt, size=11, font="Ink-Kalam"); k.line([(140, y + 4), (372, y + 4)], lw=1.6, amp=0.2); k.unclip()
def b_ring(k, w, h, v): part_open(k, w, h); k.pin_card(150, 76, 210, 34, ["Keast's story doesn't fit the night"], size=10); k.unclip()

# ----------------------------------------------------------------------------- 8. confession
def conf_plate(k, w, h): plate_open(k, w, h); k.floorboards(w, y=56); k.unclip()
def keast_c(k, w, h, v): part_open(k, w, h); keast(k, 140, 56, 200, expr="sheepish" if "sheepish" in v else "neutral"); k.unclip()
def case_part(k, w, h, v):
    part_open(k, w, h); k.rect(270, 56, 170, 70, lw=1.2, fill=Wt); k.line([(270, 100), (440, 100)], lw=0.8, amp=0)
    k.shape(k.arcpts(355, 126, 50, 16, 0, 180, 14), lw=0.8, fill=Wt, amp=0); k.barometer(355, 146, 22); k.text(355, 70, "SUITCASE", size=9, font="Ink-Plex")
    k.text(420, 160, "in a towel", size=9, font="Ink-Kalam"); k.unclip()
def collect_part(k, w, h, v): part_open(k, w, h); k.pin_card(270, 290, 210, 40, ["collects old weather", "instruments; returned it"], size=10); k.unclip()
def check_part(k, w, h, v): part_open(k, w, h); k.pin_card(270, 220, 210, 40, ["next time: check the", "weather first!"], size=10); k.unclip()

def _vig(k, w, h): k.foghorn(w * 0.4, h * 0.2, h * 0.6)
vignette = B.vignette_fn(_vig)

def jobs():
    J = []
    J.append(dict(name="hook", w=AW, h=AH, plate=hook_plate, seed=2701))
    J.append(dict(name="cast", w=CW, h=CH, plate=cast_plate, seed=2702, parts={
        f"s{i}": dict(fn=B.cast_fig_fn(i, 3, fn), variants=V2) for i, (_, fn) in enumerate(CAST)}))
    J.append(dict(name="horn", w=AW, h=AH, plate=horn_plate, seed=2703, parts=dict(
        fog=dict(fn=fog_part, variants=["base"]), boom=dict(fn=boom_part, variants=["base"]), houses=dict(fn=houses_part, variants=["base"]),
        cat=dict(fn=cat_part, variants=["base"]), **B.FX_GULL)))
    J.append(dict(name="bed", w=AW, h=AH, plate=bed_plate, seed=2704, parts=dict(
        agnes=dict(fn=agnes_b, variants=V2), lemon=dict(fn=lemon_part, variants=["base"]), open=dict(fn=open_part, variants=["base"]),
        hours=dict(fn=hours_part, variants=["base"]), clear=dict(fn=clear_part, variants=["base"]), silent=dict(fn=silent_part, variants=["base"]))))
    J.append(dict(name="bay", w=AW, h=AH, plate=bay_plate, seed=2705, parts=dict(
        yacht=dict(fn=yacht_part, variants=["base"]), nob=dict(fn=yacht_nob, variants=["base"]), gone=dict(fn=gone_part, variants=["base"]),
        dinghy=dict(fn=dinghy_part, variants=["base"]))))
    J.append(dict(name="lineup", w=3 * PW, h=AH, plate=lineup_plate, seed=2706, parts={
        **{f"s{i}": dict(fn=B.lineup_fig_fn(i, fn, x=FX, y=FY, fh=FH), variants=V3) for i, (_, fn) in enumerate(CAST)},
        **{f"p{i}": dict(fn=partial(ltag, i=i), variants=["base"]) for i in range(3)}, "said": dict(fn=said_part, variants=["base"])}))
    J.append(dict(name="board", w=AW, h=AH, plate=board_plate, seed=2707, parts={
        "keast": dict(fn=b_keast, variants=["base"]), "agnes": dict(fn=b_agnes, variants=["base"]), "x": dict(fn=b_x, variants=["base"]),
        **{f"r{i}": dict(fn=partial(b_row, i=i), variants=["base"]) for i in range(2)}, "ring": dict(fn=b_ring, variants=["base"])}))
    J.append(dict(name="confess", w=AW, h=AH, plate=conf_plate, seed=2708, parts=dict(
        keast=dict(fn=keast_c, variants=["sheepish", "sheepish+blink"]), case=dict(fn=case_part, variants=["base"]),
        collect=dict(fn=collect_part, variants=["base"]), check=dict(fn=check_part, variants=["base"]))))
    J.append(dict(name="vignette", w=384, h=384, plate=vignette, seed=2709))
    return J

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    J = [j for j in jobs() if not want or j["name"] in want]
    save_layers(OUT, J, B.make_ink)
