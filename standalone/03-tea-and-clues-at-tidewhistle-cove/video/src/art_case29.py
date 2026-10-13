"""Illustrations for Case 29, The Sugar Bowl: BLACK-AND-WHITE ink (bwkit) with the simple v1 peg-doll characters.
The vicar's study with the tiny 200-year-old book of sea shanties on its stand, the housekeeper's tea tray (pot, milk jug,
cup, sugar bowl of exactly TWELVE lumps), the same tray at three o'clock (book gone, cup of dark tea with no milk, jug still
full, NINE lumps), three visitors with equal "how they take their tea" tags, and a "WHO TAKES IT BLACK + 3?" board.
PART sprites use part_open (clip only, never frame2). Dark tea = solid ink; milky tea = light hatch.
Hook (render.py HOOK_STYLE="sugarlumps"): borderless hero of the study window and the tray.
Fairness: Captain Quill, Loveday and Mr Bolitho share stance, height, arms-down pose and neutral face; equal tags.
Only the confession shows Bolitho sheepish.
Run: python3 art_case29.py [scene ...]"""
import os, sys
from functools import partial
import bwkit as B
from bwkit import plate_open, part_open, full_open, InkBW, PW, AW, AH, V2, V3, CW, CH
import figures as F
from inkart import K, Wt
from layers import save_layers

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-29")

def quill(k, x, y, h, **kw): kw.setdefault("prop", False); F.quill(k, x, y, h, **kw)
def loveday(k, x, y, h, **kw): kw.setdefault("jug_", False); kw.setdefault("expr", "neutral"); F.loveday(k, x, y, h, **kw)
def bolitho(k, x, y, h, **kw): B.visitor(k, x, y, h, suit="stripe", hat="panama", tie=True, moustache=True, **kw)
def agnes(k, x, y, h, **kw): kw.setdefault("teapot", True); F.agnes(k, x, y, h, **kw)

def _lumps(k, x, y, n, s=7):
    for i in range(n):
        cx, cy = x + (i % 4) * (s + 2), y + (i // 4) * (s + 1)
        k.rect(cx, cy, s, s, lw=0.6, fill=Wt)
InkBW.lumps = _lumps

def _tray(k, x, y, cup="none", lumps=12, jug_full=True):
    k.rect(x, y, 240, 14, lw=1.1, fill=Wt)
    k.teapot(x + 40, y + 14, 50) if hasattr(k, "teapot") else None
    k.rect(x + 86, y + 14, 26, 34, lw=0.9, fill=Wt); k.text(x + 99, y + 52, "MILK", size=6, font="Ink-Plex")
    if jug_full: k.rect(x + 88, y + 16, 22, 26, lw=0, fill=None); k.hatch([(x + 88, y + 16), (x + 110, y + 16), (x + 110, y + 42), (x + 88, y + 42)], angle=0, gap=2.2, lw=0.25)
    k.shape([(x + 126, y + 14), (x + 158, y + 14), (x + 162, y + 40), (x + 122, y + 40)], lw=0.9, fill=Wt, amp=0)
    if cup == "dark": k.shape([(x + 125, y + 28), (x + 159, y + 28), (x + 160, y + 36), (x + 124, y + 36)], lw=0, fill=K, amp=0)
    k.shape(k.arcpts(x + 200, y + 14, 30, 22, 0, 180, 16), lw=1.0, fill=Wt, amp=0); k.text(x + 200, y + 18, "SUGAR", size=6, font="Ink-Plex")
    k.lumps(x + 182, y + 40, lumps, s=6)
InkBW.tea_tray = _tray

def _shanty_book(k, x, y, s):
    k.rect(x - s / 2, y, s, s * 0.7, lw=1.0, fill=Wt); k.line([(x, y), (x, y + s * 0.7)], lw=0.6, amp=0)
    for j in range(4): k.line([(x - s * 0.42, y + s * (0.15 + 0.12 * j)), (x - s * 0.08, y + s * (0.15 + 0.12 * j))], lw=0.3, amp=0.2); k.line([(x + s * 0.08, y + s * (0.15 + 0.12 * j)), (x + s * 0.42, y + s * (0.15 + 0.12 * j))], lw=0.3, amp=0.2)
InkBW.shanty_book = _shanty_book

def _study(k, w, h):
    k.floorboards(w, y=60); k.rect(290, 150, 180, 170, lw=1.3, fill=Wt); k.line([(380, 150), (380, 320)], lw=0.8, amp=0); k.line([(290, 235), (470, 235)], lw=0.8, amp=0)
    k.line([(330, 60), (330, 120)], lw=1.2, amp=0); k.rect(300, 120, 60, 10, lw=1.0, fill=Wt)
    k.rect(40, 60, 250, 70, lw=1.2, fill=Wt)

# ----------------------------------------------------------------------------- 1. hook hero
def hook_plate(k, w, h): full_open(k, w, h); _study(k, w, h); k.tea_tray(44, 130, cup="dark", lumps=9, jug_full=True); k.unclip()

# ----------------------------------------------------------------------------- 2. cast
CAST = [("CAPTAIN QUILL", quill), ("LOVEDAY", loveday), ("MR BOLITHO", bolitho)]
cast_plate = B.cast_plate_fn([n for n, _ in CAST], style="tags")

# ----------------------------------------------------------------------------- 3. Agnes knows how everyone takes their tea
def tea_plate(k, w, h): plate_open(k, w, h); k.tearoom(w, h, window=True, counter=True); k.unclip()
def agnes_t(k, w, h, v): part_open(k, w, h); agnes(k, 330, 30, 210); k.unclip()
def know_part(k, w, h, v): part_open(k, w, h); k.pin_card(40, 290, 200, 40, ["10 years: knows how everyone", "takes their tea"], size=10); k.unclip()

# ----------------------------------------------------------------------------- 4. the study: the shanty book; the tray at 2
def study_plate(k, w, h): plate_open(k, w, h); _study(k, w, h); k.unclip()
def book_part(k, w, h, v): part_open(k, w, h); k.shanty_book(330, 130, 50); k.pin_card(370, 60, 120, 46, ["sea shanties,", "200+ years old"], size=10); k.unclip()
def tray2_part(k, w, h, v): part_open(k, w, h); k.tea_tray(44, 130, cup="none", lumps=12); k.pin_card(40, 260, 180, 40, ["2 o'clock: tea tray,", "sugar bowl: exactly 12"], size=10); k.unclip()
def tray3_part(k, w, h, v): part_open(k, w, h); k.tea_tray(44, 130, cup="dark", lumps=9); k.unclip()
def gone_part(k, w, h, v): part_open(k, w, h); k.dashed_outline(330, 130, 54, 38); k.pin_card(370, 60, 120, 30, ["3 o'clock: gone!"], size=10); k.unclip()
def dark_part(k, w, h, v): part_open(k, w, h); k.pin_card(40, 260, 180, 40, ["cup: dark tea, NO milk;", "milk jug still full"], size=10); k.unclip()
def nine_part(k, w, h, v): part_open(k, w, h); k.pin_card(40, 214, 180, 30, ["sugar bowl: only 9 left"], size=10); k.unclip()
def vicar_part(k, w, h, v): part_open(k, w, h); k.pin_card(250, 330, 230, 40, ["vicar: milk, no sugar, in the garden;", "housekeeper: only cocoa"], size=9); k.unclip()

# ----------------------------------------------------------------------------- 5. lineup with tea tags
def _p(k, pw, h): k.stones(14, pw - 14, 14, 50, rows=2); k.rect(300, 50, 170, 130, lw=1.0, fill=Wt); k.text(385, 150, "VICARAGE", size=10, font="Ink-Plex")
lineup_plate = B.lineup_plate_fn([_p, _p, _p], [n for n, _ in CAST])
FX, FY, FH = PW / 2 - 160, 50, 220
TAGS = [["strong, plenty of milk,", "NO sugar"], ["milk and", "ONE sugar"], ["BLACK, three sugars;", "staying at the inn"]]
def ltag(k, w, h, v, i=0):
    part_open(k, w, h); x = i * PW + 236; k.rect(x, 286, 250, 50, lw=1.1, fill=Wt)
    for j, ln in enumerate(TAGS[i]): k.text(x + 125, 318 - j * 20, ln, size=11, font="Ink-Kalam")
    k.unclip()

# ----------------------------------------------------------------------------- 6. board
def board_plate(k, w, h): plate_open(k, w, h); k.floorboards(w, y=56); k.case_board(24, 66, 464, 292, title="HOW WAS THIS TEA TAKEN?")
def b_cup(k, w, h, v): part_open(k, w, h); k.pin_card(40, 260, 200, 50, ["no milk (jug untouched)", "12 \u2212 9 = 3 lumps"], size=11); k.unclip()
def b_black(k, w, h, v): part_open(k, w, h); k.pin_card(260, 260, 200, 50, ["= BLACK", "with THREE sugars"], size=13); k.unclip()
ROWS = ["Quill: milk, no sugar", "Loveday: milk, one sugar", "vicar: milk, no sugar", "housekeeper: cocoa only"]
def b_row(k, w, h, v, i=0):
    part_open(k, w, h); x, y = ((140, 200), (370, 200), (140, 160), (370, 160))[i]
    k.text(x, y, ROWS[i], size=10, font="Ink-Kalam"); k.line([(x - 95, y + 4), (x + 95, y + 4)], lw=1.4, amp=0.2); k.unclip()
def b_ring(k, w, h, v): part_open(k, w, h); k.pin_card(150, 86, 210, 46, ["Mr Bolitho: black,", "three sugars"], size=12); k.shape(k.arcpts(255, 109, 120, 34, 0, 360, 30), lw=2.2, fill=None, amp=0.4); k.unclip()

# ----------------------------------------------------------------------------- 7. confession at the Kettle and Gull
def conf_plate(k, w, h): plate_open(k, w, h); k.tearoom(w, h, window=True, counter=True); k.unclip()
def bol_c(k, w, h, v): part_open(k, w, h); bolitho(k, 140, 30, 210, expr="sheepish" if "sheepish" in v else "neutral"); k.unclip()
def sing_part(k, w, h, v): part_open(k, w, h); k.pin_card(270, 290, 210, 40, ["a shanty singer: \u201conly meant", "to copy a song or two\u201d"], size=10); k.unclip()
def ret_part(k, w, h, v): part_open(k, w, h); k.shanty_book(380, 200, 50); k.pin_card(270, 140, 210, 40, ["returned that evening; sang", "three shanties in church"], size=10); k.unclip()

def _vig(k, w, h): k.lumps(w * 0.32, h * 0.4, 9, s=22)
vignette = B.vignette_fn(_vig)

def jobs():
    J = []
    J.append(dict(name="hook", w=AW, h=AH, plate=hook_plate, seed=2901))
    J.append(dict(name="cast", w=CW, h=CH, plate=cast_plate, seed=2902, parts={
        f"s{i}": dict(fn=B.cast_fig_fn(i, 3, fn), variants=V2) for i, (_, fn) in enumerate(CAST)}))
    J.append(dict(name="tea", w=AW, h=AH, plate=tea_plate, seed=2903, parts=dict(agnes=dict(fn=agnes_t, variants=V3), know=dict(fn=know_part, variants=["base"]))))
    J.append(dict(name="study", w=AW, h=AH, plate=study_plate, seed=2904, parts=dict(
        book=dict(fn=book_part, variants=["base"]), tray2=dict(fn=tray2_part, variants=["base"]), tray3=dict(fn=tray3_part, variants=["base"]),
        gone=dict(fn=gone_part, variants=["base"]), dark=dict(fn=dark_part, variants=["base"]), nine=dict(fn=nine_part, variants=["base"]),
        vicar=dict(fn=vicar_part, variants=["base"]))))
    J.append(dict(name="lineup", w=3 * PW, h=AH, plate=lineup_plate, seed=2905, parts={
        **{f"s{i}": dict(fn=B.lineup_fig_fn(i, fn, x=FX, y=FY, fh=FH), variants=V3) for i, (_, fn) in enumerate(CAST)},
        **{f"p{i}": dict(fn=partial(ltag, i=i), variants=["base"]) for i in range(3)}}))
    J.append(dict(name="board", w=AW, h=AH, plate=board_plate, seed=2906, parts={
        "cup": dict(fn=b_cup, variants=["base"]), "black": dict(fn=b_black, variants=["base"]),
        **{f"r{i}": dict(fn=partial(b_row, i=i), variants=["base"]) for i in range(4)}, "ring": dict(fn=b_ring, variants=["base"])}))
    J.append(dict(name="confess", w=AW, h=AH, plate=conf_plate, seed=2907, parts=dict(
        bol=dict(fn=bol_c, variants=["sheepish", "sheepish+blink"]), sing=dict(fn=sing_part, variants=["base"]), ret=dict(fn=ret_part, variants=["base"]))))
    J.append(dict(name="vignette", w=384, h=384, plate=vignette, seed=2908))
    return J

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    J = [j for j in jobs() if not want or j["name"] in want]
    save_layers(OUT, J, B.make_ink)
