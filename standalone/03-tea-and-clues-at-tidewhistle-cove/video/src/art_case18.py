"""Illustrations for Case 18, The Moonlit Walk: BLACK-AND-WHITE ink (bwkit) with the simple v1 peg-doll characters.
The Gazette's back-page notice (NEW MOON THIS SATURDAY), a night clifftop under a hatched, moonless, starry sky, the
stargazing club's tent and antique star chart, and Miss Clemo's story in a speech bubble (her "full moon" is drawn only
inside her bubble; the real sky never has a moon). PART sprites use part_open (clip only, never frame2).
Hook (render.py HOOK_STYLE="starfield"): borderless hero of the clifftop tent under the stars.
Fairness: Demelza, Captain Quill and Miss Clemo share one stance, height, arms-down pose and neutral face in the cast strip
and the lineup; only the confession shows Miss Clemo sheepish (blushing).
Run: python3 art_case18.py [scene ...]"""
import os, sys, math, random
from functools import partial
import bwkit as B
from bwkit import plate_open, part_open, full_open, InkBW, PW, AW, AH, V2, V3, CW, CH
import figures as F
from inkart import K, Wt
from layers import save_layers

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-18")

def demelza(k, x, y, h, **kw): kw.setdefault("prop", False); F.demelza(k, x, y, h, **kw)
def quill(k, x, y, h, **kw): kw.setdefault("prop", False); F.quill(k, x, y, h, **kw)
def clemo(k, x, y, h, **kw): B.lady(k, x, y, h, dress="plain", hair="bun", hat=None, shawl=True, **kw)
def agnes(k, x, y, h, **kw): kw.setdefault("teapot", False); F.agnes(k, x, y, h, **kw)
def ollie(k, x, y, h, **kw): kw.setdefault("expr", "neutral"); F.ollie(k, x, y, h, **kw)

def _night(k, x0, y0, x1, y1, seed=18, n=40):
    sky = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    k.hatch(sky, angle=-30, gap=3.0, lw=0.35, cross=True)
    rr = random.Random(seed)
    for _ in range(n):
        x, y, r = rr.uniform(x0 + 8, x1 - 8), rr.uniform(y0 + 8, y1 - 8), rr.uniform(1.4, 3.2)
        k.circle(x, y, r * 1.4, lw=0, fill=Wt, stroke=False)
        k.line([(x - r * 1.6, y), (x + r * 1.6, y)], lw=0.5, amp=0); k.line([(x, y - r * 1.6), (x, y + r * 1.6)], lw=0.5, amp=0)
InkBW.night = _night

def _starchart(k, x, y, w, h, rolled=False):
    if rolled:
        k.rect(x, y, w, h * 0.22, lw=1.0, fill=Wt); k.circle(x, y + h * 0.11, h * 0.11, lw=0.9, fill=Wt); k.circle(x + w, y + h * 0.11, h * 0.11, lw=0.9, fill=Wt); return
    k.rect(x, y, w, h, lw=1.1, fill=Wt); k.circle(x + w / 2, y + h / 2, min(w, h) * 0.42, lw=0.8, fill=None)
    rr = random.Random(int(w))
    pts = [(x + w / 2 + min(w, h) * 0.38 * rr.uniform(-1, 1) * 0.8, y + h / 2 + min(w, h) * 0.38 * rr.uniform(-1, 1) * 0.8) for _ in range(9)]
    for p in pts: k.circle(p[0], p[1], 1.4, lw=0, fill=K, stroke=False)
    k.line(pts[:5], lw=0.4, amp=0)
InkBW.starchart = _starchart

def _tent(k, x, y, w, h):
    k.shape([(x, y), (x + w, y), (x + w / 2, y + h)], lw=1.3, fill=Wt, amp=0.1)
    k.shape([(x + w * 0.3, y), (x + w * 0.7, y), (x + w / 2, y + h * 0.7)], lw=0.9, fill=Wt, amp=0)
    k.text(x + w / 2, y + h * 0.78 - 12, "CLUB", size=9, font="Ink-Plex")
InkBW.tent = _tent

def _scope(k, x, y, s):
    for dx in (-0.3, 0, 0.3): k.line([(x + dx * s, y), (x, y + s * 0.6)], lw=0.9, amp=0)
    tube = [(x - s * 0.3, y + s * 0.5), (x + s * 0.35, y + s * 0.95), (x + s * 0.3, y + s * 1.02), (x - s * 0.35, y + s * 0.58)]
    k.shape(tube, lw=1.0, fill=Wt, amp=0)
InkBW.scope = _scope

def clifftop(k, w, h, seed=18):
    k.night(14, 150, w - 14, h - 14, seed=seed)
    k.sea(14, 220, 100, 150, rows=3); k.headland(200, w - 14, 150, 40, hatch=False)
    k.line([(14, 100), (220, 100)], lw=0.8, amp=0)
    k.stones(14, w - 14, 14, 60, rows=2)
    for x in (110, 250): k.scope(x, 140 if x > 200 else 100, 46)

# ----------------------------------------------------------------------------- 1. hook hero
def hook_plate(k, w, h): full_open(k, w, h); clifftop(k, w, h); k.tent(330, 150, 150, 120); k.unclip()

# ----------------------------------------------------------------------------- 2. cast
CAST = [("DEMELZA", demelza), ("CAPTAIN QUILL", quill), ("MISS CLEMO", clemo)]
cast_plate = B.cast_plate_fn([n for n, _ in CAST], style="cards")

# ----------------------------------------------------------------------------- 3. Agnes reads the Gazette over breakfast
def breakfast_plate(k, w, h): plate_open(k, w, h); k.tearoom(w, h, window=True, counter=False); k.table_cloth(220, 30, 200, 70); k.unclip()
def agnes_read(k, w, h, v): part_open(k, w, h); agnes(k, 170, 30, 210, prop=False) if False else agnes(k, 170, 30, 210); k.unclip()
def gazette_part(k, w, h, v):
    part_open(k, w, h); x, y = 250, 110
    k.rect(x, y, 130, 150, lw=1.1, fill=Wt); k.text(x + 65, y + 132, "THE GAZETTE", size=11, font="Ink-Playfair"); k.line([(x + 8, y + 124), (x + 122, y + 124)], lw=0.8, amp=0)
    for j in range(9): k.line([(x + 10, y + 108 - j * 11), (x + (120 if j % 3 else 70), y + 108 - j * 11)], lw=0.35, amp=0.2)
    k.unclip()
def cup_part(k, w, h, v): part_open(k, w, h); k.rect(420, 100, 22, 22, lw=0.9, fill=Wt); k.shape(k.arcpts(431, 100, 22, 5, 0, 360, 14), lw=0.8, fill=Wt, amp=0); k.unclip()

# ----------------------------------------------------------------------------- 4. the back-page notice
def notice_plate(k, w, h):
    plate_open(k, w, h)
    k.rect(30, 24, 452, 330, lw=1.2, fill=Wt); k.text(256, 326, "THE TIDEWHISTLE COVE GAZETTE \u00b7 back page", size=11, font="Ink-Playfair")
    k.line([(46, 316), (466, 316)], lw=0.8, amp=0)
    for j in range(16): k.line([(48, 296 - j * 16), (150, 296 - j * 16)], lw=0.35, amp=0.2); k.line([(362, 296 - j * 16), (464, 296 - j * 16)], lw=0.35, amp=0.2)
    k.rect(166, 60, 180, 240, lw=1.6, fill=Wt); k.rect(172, 66, 168, 228, lw=0.5, fill=None)
    k.text(256, 270, "STARGAZING CLUB", size=13, font="Ink-Plex")
def nline(k, w, h, v, i=0):
    part_open(k, w, h)
    L = [("New moon", 236, 20, "Ink-Playfair"), ("this Saturday", 214, 16, "Ink-Playfair"), ("The darkest night", 180, 12, "Ink-Kalam"),
         ("of the month.", 164, 12, "Ink-Kalam"), ("Perfect for meteors.", 136, 12, "Ink-Kalam"), ("Bring a blanket", 110, 12, "Ink-Kalam"), ("and a flask.", 94, 12, "Ink-Kalam")]
    for t, y, s, f in ([L[0], L[1]] if i == 0 else [L[2], L[3]] if i == 1 else [L[4]] if i == 2 else [L[5], L[6]]): k.text(256, y, t, size=s, font=f)
    k.unclip()

# ----------------------------------------------------------------------------- 5. the clifftop tent, the star chart; 11 o'clock to midnight
def cliff_plate(k, w, h):
    plate_open(k, w, h); clifftop(k, w, h)
    k.shape([(300, 60), (500, 60), (400, 300)], lw=1.4, fill=Wt, amp=0.1); k.text(400, 250, "CLUB TENT", size=10, font="Ink-Plex")
    k.rect(345, 60, 110, 6, lw=0.8, fill=Wt); k.rect(360, 60, 80, 50, lw=1.0, fill=Wt); k.rect(352, 108, 96, 6, lw=0.9, fill=Wt)
    k.unclip()
def chart_part(k, w, h, v): part_open(k, w, h); k.starchart(362, 114, 76, 52); k.unclip()
def gone_part(k, w, h, v): part_open(k, w, h); k.dashed_outline(362, 114, 76, 52); k.text(400, 176, "gone!", size=12, font="Ink-Kalam"); k.unclip()
def clemo_g(k, w, h, v): part_open(k, w, h); clemo(k, 250, 60, 150); k.unclip()
def guest_part(k, w, h, v): part_open(k, w, h); k.pin_card(170, 300, 150, 44, ["special guest:", "astronomer"], size=11); k.unclip()
def clock_part(k, w, h, v):
    part_open(k, w, h); k.clock_face(60, 300, 26, 12 if v == "mid" else 11, 0); k.text(60, 262, "midnight" if v == "mid" else "11 o'clock", size=10, font="Ink-Kalam"); k.unclip()
def club_part(k, w, h, v):
    part_open(k, w, h)
    for i, x in enumerate((90, 150, 200)): B.visitor(k, x, 60, 90, suit="plain", hat=None, tie=False, flip=bool(i % 2))
    k.unclip()

# ----------------------------------------------------------------------------- 6. lineup: who left early
def _p_cott(k, pw, h):
    k.night(14, 230, pw - 14, h - 14, seed=3, n=14); k.stones(14, pw - 14, 14, 50, rows=2)
    k.rect(300, 50, 170, 150, lw=1.2, fill=Wt); k.shape([(290, 200), (480, 200), (385, 240)], lw=1.2, fill=Wt, amp=0); k.rect(360, 50, 40, 80, lw=1.0, fill=Wt)
    k.text(385, 160, "Demelza's cottage", size=10, font="Ink-Kalam")
def _p_path(k, pw, h):
    k.night(14, 230, pw - 14, h - 14, seed=5, n=14); k.headland(14, pw - 14, 90, 60, hatch=False)
    for i in range(10): k.line([(250 + i * 24, 90 + (i % 3) * 6), (264 + i * 24, 96 + (i % 2) * 6)], lw=0.8, amp=0.3)
    k.rect(400, 120, 80, 70, lw=1.1, fill=Wt); k.text(440, 160, "INN", size=10, font="Ink-Plex")
lineup_plate = B.lineup_plate_fn([_p_cott, _p_cott, _p_path], [n for n, _ in CAST])
TAGS = ["left 10:30", "walked her home", "left about 11:15"]
def ltag(k, w, h, v, i=0):
    part_open(k, w, h); x = i * PW + 300; k.rect(x, 258, 170, 40, lw=1.1, fill=Wt); k.text(x + 85, 270, TAGS[i], size=14, font="Ink-Kalam"); k.unclip()
def home_tag(k, w, h, v, i=0):
    part_open(k, w, h); x = i * PW + 300; k.rect(x, 214, 170, 36, lw=1.0, fill=Wt); k.text(x + 85, 225, "home before 11", size=13, font="Ink-Kalam"); k.unclip()

# ----------------------------------------------------------------------------- 7. Miss Clemo's story (her moon only in her bubble)
def story_plate(k, w, h): plate_open(k, w, h); k.floorboards(w, y=80); k.rect(30, 80, 150, 220, lw=1.0, fill=Wt); k.text(105, 280, "THE INN", size=11, font="Ink-Plex"); k.unclip()
def clemo_s(k, w, h, v): part_open(k, w, h); clemo(k, 150, 40, 210); k.unclip()
def agnes_s(k, w, h, v): part_open(k, w, h); agnes(k, 360, 40, 200, flip=True); k.unclip()
def ollie_s(k, w, h, v): part_open(k, w, h); ollie(k, 450, 40, 216, flip=True); k.unclip()
def story_bubble(k, w, h, v):
    part_open(k, w, h); x, y, bw, bh = 196, 216, 230, 140
    c = k.c; c.setStrokeColor(K); c.setFillColor(Wt); c.setLineWidth(1.2); c.roundRect(x, y, bw, bh, 16, stroke=1, fill=1)
    for (cx, cy, r) in ((x - 6, y - 4, 6), (x - 18, y - 16, 4)): k.circle(cx, cy, r, lw=1.0, fill=Wt)
    k.c.saveState(); p = c.beginPath(); p.roundRect(x + 2, y + 2, bw - 4, bh - 4, 14); c.clipPath(p, stroke=0)
    k.headland(x, x + bw, y + 40, 20, hatch=False)
    for i in range(9): k.line([(x + 20 + i * 22, y + 30 + (i % 2) * 4), (x + 32 + i * 22, y + 34)], lw=0.8, amp=0.2)
    k.circle(x + bw - 50, y + bh - 42, 24, lw=1.2, fill=Wt); k.circle(x + bw - 50, y + bh - 42, 30, lw=0.4, fill=None)
    for a in range(0, 360, 30): k.line([(x + bw - 50 + 34 * math.cos(math.radians(a)), y + bh - 42 + 34 * math.sin(math.radians(a))), (x + bw - 50 + 40 * math.cos(math.radians(a)), y + bh - 42 + 40 * math.sin(math.radians(a)))], lw=0.5, amp=0)
    k.c.restoreState(); k.text(x + 70, y + bh - 30, "\u201cfull and", size=12, font="Ink-Kalam"); k.text(x + 70, y + bh - 46, "bright\u201d", size=12, font="Ink-Kalam")
    k.unclip()

# ----------------------------------------------------------------------------- 8. solution board
def board_plate(k, w, h):
    plate_open(k, w, h); k.floorboards(w, y=60)
    k.case_board(30, 76, 452, 280, title="SATURDAY NIGHT'S MOON")
    k.text(140, 296, "THE GAZETTE", size=11, font="Ink-Plex"); k.text(372, 296, "MISS CLEMO", size=11, font="Ink-Plex")
    k.line([(256, 110), (256, 300)], lw=0.6, amp=0)
def b_new(k, w, h, v):
    part_open(k, w, h); k.circle(140, 236, 30, lw=1.2, fill=K); k.text(140, 186, "NEW MOON", size=13, font="Ink-Plex"); k.text(140, 168, "no moonlight at all", size=11, font="Ink-Kalam"); k.unclip()
def b_full(k, w, h, v):
    part_open(k, w, h); k.circle(372, 236, 30, lw=1.4, fill=Wt)
    for a in range(0, 360, 30): k.line([(372 + 36 * math.cos(math.radians(a)), 236 + 36 * math.sin(math.radians(a))), (372 + 44 * math.cos(math.radians(a)), 236 + 44 * math.sin(math.radians(a)))], lw=0.6, amp=0)
    k.text(372, 186, "\u201cFULL & BRIGHT\u201d", size=13, font="Ink-Plex"); k.text(372, 168, "every pebble lit", size=11, font="Ink-Kalam"); k.unclip()
def b_x(k, w, h, v):
    part_open(k, w, h); k.line([(330, 200), (414, 272)], lw=2.6, amp=0); k.line([(330, 272), (414, 200)], lw=2.6, amp=0)
    k.text(372, 140, "made up", size=14, font="Ink-Kalam"); k.unclip()
def b_pair(k, w, h, v):
    part_open(k, w, h); k.pin_card(70, 130, 150, 50, ["Demelza & Quill:", "home before 11"], size=11); k.unclip()

# ----------------------------------------------------------------------------- 9. confession
def conf_plate(k, w, h): plate_open(k, w, h); k.floorboards(w, y=80); k.rect(330, 80, 150, 70, lw=1.1, fill=Wt); k.unclip()
def clemo_c(k, w, h, v):
    part_open(k, w, h); clemo(k, 200, 40, 210, expr="sheepish" if "sheepish" in v else "neutral")
    for sg in (-1, 1):
        for j in range(3): k.line([(200 + sg * 14 - 4 + j * 3, 40 + 210 * 0.8), (200 + sg * 14 + j * 3, 40 + 210 * 0.8 + 5)], lw=0.5, amp=0)
    k.unclip()
def chart_c(k, w, h, v): part_open(k, w, h); k.starchart(350, 150, 110, 80); k.unclip()
def talk_part(k, w, h, v): part_open(k, w, h); k.pin_card(330, 300, 150, 46, ["free talk:", "THE MOON"], size=12); k.unclip()

def _vig(k, w, h): k.night(0, h * 0.35, w, h); k.tent(w * 0.25, h * 0.2, w * 0.5, h * 0.4)
vignette = B.vignette_fn(_vig)

def jobs():
    J = []
    J.append(dict(name="hook", w=AW, h=AH, plate=hook_plate, seed=1801))
    J.append(dict(name="cast", w=CW, h=CH, plate=cast_plate, seed=1802, parts={
        f"s{i}": dict(fn=B.cast_fig_fn(i, 3, fn), variants=V2) for i, (_, fn) in enumerate(CAST)}))
    J.append(dict(name="breakfast", w=AW, h=AH, plate=breakfast_plate, seed=1803, parts=dict(
        agnes=dict(fn=agnes_read, variants=V2), gazette=dict(fn=gazette_part, variants=["base"]), cup=dict(fn=cup_part, variants=["base"]))))
    J.append(dict(name="notice", w=AW, h=AH, plate=notice_plate, seed=1804, parts={f"n{i}": dict(fn=partial(nline, i=i), variants=["base"]) for i in range(4)}))
    J.append(dict(name="cliff", w=AW, h=AH, plate=cliff_plate, seed=1805, parts=dict(
        chart=dict(fn=chart_part, variants=["base"]), gone=dict(fn=gone_part, variants=["base"]), clemo=dict(fn=clemo_g, variants=V2),
        guest=dict(fn=guest_part, variants=["base"]), clock=dict(fn=clock_part, variants=["base", "mid"]), club=dict(fn=club_part, variants=["base"]))))
    J.append(dict(name="lineup", w=3 * PW, h=AH, plate=lineup_plate, seed=1806, parts={
        **{f"s{i}": dict(fn=B.lineup_fig_fn(i, fn, x=PW / 2 - 140, y=50, fh=220), variants=V3) for i, (_, fn) in enumerate(CAST)},
        **{f"t{i}": dict(fn=partial(ltag, i=i), variants=["base"]) for i in range(3)},
        **{f"h{i}": dict(fn=partial(home_tag, i=i), variants=["base"]) for i in range(2)}}))
    J.append(dict(name="story", w=AW, h=AH, plate=story_plate, seed=1807, parts=dict(
        clemo=dict(fn=clemo_s, variants=V3), agnes=dict(fn=agnes_s, variants=V2), ollie=dict(fn=ollie_s, variants=V2), bubble=dict(fn=story_bubble, variants=["base"]))))
    J.append(dict(name="board", w=AW, h=AH, plate=board_plate, seed=1808, parts=dict(
        new=dict(fn=b_new, variants=["base"]), full=dict(fn=b_full, variants=["base"]), x=dict(fn=b_x, variants=["base"]), pair=dict(fn=b_pair, variants=["base"]))))
    J.append(dict(name="confess", w=AW, h=AH, plate=conf_plate, seed=1809, parts=dict(
        clemo=dict(fn=clemo_c, variants=["sheepish", "sheepish+blink"]), chart=dict(fn=chart_c, variants=["base"]), talk=dict(fn=talk_part, variants=["base"]))))
    J.append(dict(name="vignette", w=384, h=384, plate=vignette, seed=1810))
    return J

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    J = [j for j in jobs() if not want or j["name"] in want]
    save_layers(OUT, J, B.make_ink)
