"""Illustrations for Case 11, The Window Table: BLACK-AND-WHITE ink (bwkit) with the simple v1 peg-doll characters.
A seating-logic case: the Kettle and Gull's four tables in a row, door (table 1) to bay window (table 4).
PART sprites use part_open (clip only, never frame2).
Hook (render.py HOOK_STYLE="placecard"): borderless hero of the four numbered tables and the EMPTY windowsill.
Fairness: Mr Spargo, Loveday, Captain Quill and Wenna share one stance, height, arms-down pose and neutral face in
the cast strip and the lineup (no table numbers in the lineup); only the confession shows the captain sheepish.
Run: python3 art_case11.py [scene ...]"""
import os, sys
from functools import partial
import bwkit as B
from bwkit import plate_open, part_open, full_open, InkBW, nameplate, PW, AW, AH, V2, V3, CW, CH
import figures as F
from inkart import K, Wt
from layers import save_layers

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "art-11")

# ----------------------------------------------------------------------------- characters
def spargo(k, x, y, h, **kw): B.visitor(k, x, y, h, suit="check", hat="bowler", tie=True, moustache=True, **kw)
def loveday(k, x, y, h, **kw): kw.setdefault("jug_", False); F.loveday(k, x, y, h, **kw)
def quill(k, x, y, h, **kw): kw.setdefault("prop", False); F.quill(k, x, y, h, **kw)
def wenna(k, x, y, h, **kw): kw.setdefault("prop", False); F.wenna(k, x, y, h, **kw)
def kerensa(k, x, y, h, **kw): B.lady(k, x, y, h, dress="stripe", hair="curls", hat="sun", **kw)
def pip(k, x, y, h, **kw): kw.setdefault("prop", False); F.pip(k, x, y, h, **kw)
def agnes(k, x, y, h, **kw): kw.setdefault("teapot", False); F.agnes(k, x, y, h, **kw)

# ----------------------------------------------------------------------------- shared drawing
def _brooch(k, x, y, r=7):
    k.circle(x, y, r, lw=0.9, fill=Wt); k.circle(x, y, r * 0.78, lw=0.35, fill=None)
    k.line([(x - r * 0.6, y + r * 0.1), (x - r * 0.25, y + r * 0.35), (x, y), (x + r * 0.25, y + r * 0.35), (x + r * 0.6, y + r * 0.1)], lw=0.8, amp=0)
InkBW.brooch = _brooch

TX = (112, 206, 300, 386)        # table centres, door (left) -> window (right)
SILL = (418, 498, 156)           # windowsill x0, x1, y
def tearow(k, w, h, numbers=True, sill_dash=False):
    """The Kettle and Gull lengthwise: door at left, four small tables, bay window + sill at right."""
    k.floorboards(w, y=96)
    k.rect(14, 96, w - 28, 30, lw=0.8, fill=Wt)
    for i in range(int((w - 28) / 32)): k.rect(20 + i * 32, 100, 24, 22, lw=0.35, fill=None)
    # door
    k.rect(22, 30, 46, 150, lw=1.2, fill=Wt); k.rect(28, 110, 34, 60, lw=0.5, fill=None); k.rect(28, 40, 34, 60, lw=0.5, fill=None)
    k.circle(60, 104, 2.2, lw=0.5, fill=K); k.text(45, 190, "DOOR", size=10, font="Ink-Plex")
    # bay window (harbour view) and sill
    k.window_view(SILL[0] + 4, SILL[2] + 8, SILL[1] - SILL[0] - 8, 150)
    k.rect(SILL[0] - 4, SILL[2], SILL[1] - SILL[0] + 8, 8, lw=1.0, fill=Wt)
    k.text(100 + 160, 330, "THE KETTLE AND GULL", size=11, font="Ink-Plex")
    if sill_dash: k.dashed_outline(SILL[0] + 26, SILL[2] + 8, 18, 12)
    for i, x in enumerate(TX):
        k.table_cloth(x, 30, 72, 46)
        if numbers:
            k.circle(x, 142, 11, lw=0.9, fill=Wt); k.text(x, 137.5, str(i + 1), size=12, font="Ink-Playfair")

# ----------------------------------------------------------------------------- 1. hook hero (full bleed, no border)
def hook_plate(k, w, h):
    full_open(k, w, h); tearow(k, w, h, numbers=True, sill_dash=True)
    k.text(SILL[0] + 35, SILL[2] + 26, "?", size=20, font="Ink-Playfair")
    k.unclip()

# ----------------------------------------------------------------------------- 2. cast strip (four equal cards)
CAST = [("MR SPARGO", spargo), ("LOVEDAY", loveday), ("CAPTAIN QUILL", quill), ("WENNA", wenna)]
cast_plate = B.cast_plate_fn([n for n, _ in CAST], style="frames")

# ----------------------------------------------------------------------------- 3. the four tables (numbers pop)
def tables_plate(k, w, h): plate_open(k, w, h); tearow(k, w, h, numbers=False); k.unclip()
def num_part(k, w, h, v, i=0):
    part_open(k, w, h); x = TX[i]
    k.circle(x, 142, 11, lw=0.9, fill=Wt); k.text(x, 137.5, str(i + 1), size=12, font="Ink-Playfair")
    if i == 3: k.text(x, 160, "window table", size=10, font="Ink-Kalam")
    k.unclip()

# ----------------------------------------------------------------------------- 4. Kerensa + the brooch on the sill
def sill_plate(k, w, h): plate_open(k, w, h); tearow(k, w, h, numbers=True); k.unclip()
def kerensa_part(k, w, h, v): part_open(k, w, h); kerensa(k, 352, 30, 150); k.unclip()
def brooch_part(k, w, h, v): part_open(k, w, h); k.brooch(SILL[0] + 35, SILL[2] + 15, 7); k.unclip()
def reach_part(k, w, h, v):
    """Only the window table reaches the sill; from anywhere else you'd climb over it."""
    part_open(k, w, h)
    k.line([(TX[3] + 20, 80), (SILL[0] + 10, 120), (SILL[0] + 28, SILL[2] + 2)], lw=1.2, amp=0.2)
    k.shape([(SILL[0] + 28, SILL[2] + 2), (SILL[0] + 20, SILL[2] - 6), (SILL[0] + 31, SILL[2] - 8)], lw=0.6, fill=K, amp=0)
    k.text(TX[3] - 6, 196, "only from here", size=11, font="Ink-Kalam")
    k.unclip()
def gone_part(k, w, h, v):
    part_open(k, w, h); k.dashed_outline(SILL[0] + 26, SILL[2] + 8, 18, 12)
    k.text(SILL[0] + 35, SILL[2] + 26, "?", size=18, font="Ink-Playfair"); k.unclip()

# ----------------------------------------------------------------------------- 5. lineup: four equal panels (no numbers)
def _tea_panel(k, pw, h):
    k.tearoom(pw, h, window=False, counter=False, sign=False)
    k.table_cloth(360, 14, 84, 44); k.teapot(350, 58, 22); k.cup(380, 58, 11)
lineup_plate = B.lineup_plate_fn([_tea_panel] * 4, [n for n, _ in CAST])

# ----------------------------------------------------------------------------- 6. the kitchen (Agnes + pasties), Pip serving
def kitchen_plate(k, w, h):
    plate_open(k, w, h)
    k.floorboards(w, y=70)
    w, h = int(w), int(h)
    for yy in range(70, h - 14, 22):
        k.line([(14, yy), (w - 14, yy)], lw=0.3, amp=0)
        for xx in range(14 + (11 if (yy // 22) % 2 else 0), w - 14, 22): k.line([(xx, yy), (xx, yy + 22)], lw=0.3, amp=0)
    k.rect(300, 14, 170, 120, lw=1.2, fill=Wt); k.rect(318, 30, 134, 66, lw=0.9, fill=K)     # range + oven door
    for i in range(4): k.circle(326 + i * 38, 118, 8, lw=0.7, fill=Wt)
    k.rect(40, 14, 190, 104, lw=1.0, fill=Wt); k.rect(34, 118, 202, 8, lw=1.0, fill=Wt)      # table
    k.rect(70, 126, 130, 10, lw=0.8, fill=Wt)                                               # tray
    for i in range(5):
        x = 84 + i * 25; k.shape(k.arcpts(x, 136, 11, 9, 0, 180, 12), lw=0.7, fill=Wt, amp=0)
        k.line([(x - 9, 140), (x + 9, 140)], lw=0.4, amp=0)
    k.rect(w - 60, 150, 36, 200, lw=1.0, fill=Wt); k.text(w - 42, 250, "\u2192", size=14, font="Ink-Plex")   # door to tea room
    k.unclip()
def agnes_kit(k, w, h, v): part_open(k, w, h); agnes(k, 250, 30, 210, flip=True); k.unclip()
def pip_kit(k, w, h, v): part_open(k, w, h); pip(k, 430, 30, 200, flip=True); k.unclip()

# ----------------------------------------------------------------------------- 7. Pip remembers: four clue notes
def pip_plate(k, w, h): plate_open(k, w, h); k.tearoom(w, h, window=True, counter=True); k.unclip()
def pip_talk(k, w, h, v): part_open(k, w, h); pip(k, 130, 30, 220); k.unclip()
def agnes_listen(k, w, h, v): part_open(k, w, h); agnes(k, 380, 30, 210, flip=True); k.unclip()
CLUES = [["CAPTAIN QUILL", "next to WENNA"], ["LOVEDAY", "not at an end"], ["MR SPARGO nearer", "the door than QUILL"],
         ["WENNA not at", "the window table"]]
def clue_part(k, w, h, v, i=0):
    part_open(k, w, h)
    x = 30 + i * 118; y = 268 if i % 2 == 0 else 258
    k.pin_card(x, y, 112, 74, CLUES[i], size=10, rot=(-3, 2, -2, 3)[i]); k.unclip()

# ----------------------------------------------------------------------------- 8. Agnes's four squares (notebook page)
SQ = 74; SQX = [70 + i * 96 for i in range(4)]
def page(k, w, h, title=None):
    k.rect(30, 22, w - 60, h - 44, lw=1.0, fill=Wt)
    for yy in range(46, int(h) - 30, 18): k.line([(40, yy), (w - 40, yy)], lw=0.25, amp=0)
    k.line([(70, 26), (70, h - 26)], lw=0.4, amp=0)
    if title: k.text(w / 2, h - 56, title, size=13, font="Ink-Plex")
def squares(k, y, s=SQ, label=True, xs=None):
    xs = xs or SQX
    for i, x in enumerate(xs):
        k.rect(x, y, s, s, lw=1.2, fill=Wt)
        if label: k.text(x + s / 2, y + s + 6, str(i + 1), size=11, font="Ink-Playfair")
def squares_plate(k, w, h):
    plate_open(k, w, h); page(k, w, h)
    squares(k, 170)
    k.text(SQX[0] + SQ / 2, 146, "DOOR", size=11, font="Ink-Kalam"); k.text(SQX[3] + SQ / 2, 146, "WINDOW", size=11, font="Ink-Kalam")
    k.unclip()
ICON = ["Q next to W", "L not at an end", "S nearer door than Q", "W not at 4"]
def rule_part(k, w, h, v, i=0):
    part_open(k, w, h); x = 60 + (i % 2) * 200; y = 108 - (i // 2) * 22
    k.text(x + 90, y, f"\u2022 {ICON[i]}", size=12, font="Ink-Kalam"); k.unclip()
def names_part(k, w, h, v):
    part_open(k, w, h)
    for i, nm in enumerate(("SPARGO", "LOVEDAY", "QUILL", "WENNA")): token(k, SQX[i] + SQ / 2, 64, nm, 9)
    k.unclip()
def token(k, x, y, nm, size=10):
    tw = k.c.stringWidth(nm, "Ink-Plex", size) + 12
    k.rect(x - tw / 2, y - 4, tw, size + 9, lw=0.9, fill=Wt); k.text(x, y, nm, size=size, font="Ink-Plex")

# ----------------------------------------------------------------------------- 9. solution board: two failed tries + the answer
RS = 56; RX = [150 + i * 74 for i in range(4)]; RY = {"a": 256, "b": 176, "c": 62}
def board_plate(k, w, h):
    plate_open(k, w, h); page(k, w, h)
    k.text(w / 2, h - 52, "DOOR  1 \u2192 4  WINDOW", size=12, font="Ink-Plex")
    for r, lab in (("a", "If LOVEDAY at 3\u2026"), ("b", "\u2026or this way?"), ("c", "So:")):
        s = RS if r != "c" else 62; xs = RX if r != "c" else [140 + i * 80 for i in range(4)]
        squares(k, RY[r], s=s, label=(r == "c"), xs=xs)
        k.text(92, RY[r] + s / 2 - 4, lab, size=10, font="Ink-Kalam")
    k.unclip()
def tok_part(k, w, h, v, row="a", col=0, nm=""):
    part_open(k, w, h)
    if row == "c": x = 140 + col * 80 + 31; y = RY["c"] + 27; sz = 10
    else: x = RX[col] + RS / 2; y = RY[row] + 22; sz = 7
    token(k, x, y, nm, sz); k.unclip()
def cross_part(k, w, h, v, row="a"):
    part_open(k, w, h); y = RY[row]; x0, x1 = RX[0] - 6, RX[3] + RS + 6
    k.line([(x0, y - 4), (x1, y + RS + 4)], lw=2.4, amp=0.3); k.line([(x0, y + RS + 4), (x1, y - 4)], lw=2.4, amp=0.3)
    k.text(x1 + 34, y + RS / 2 - 4, "breaks a clue", size=10, font="Ink-Kalam"); k.unclip()
def ring_part(k, w, h, v):
    part_open(k, w, h); x = 140 + 3 * 80 + 31; y = RY["c"] + 31
    k.shape(k.arcpts(x, y - 3, 44, 38, 0, 360, 36), lw=2.2, fill=None, amp=0.4)
    k.text(x, RY["c"] - 22, "window table", size=11, font="Ink-Kalam"); k.unclip()

# ----------------------------------------------------------------------------- 10. confession: the brooch in the captain's pocket
def confess_plate(k, w, h): plate_open(k, w, h); tearow(k, w, h, numbers=False); k.unclip()
def quill_conf(k, w, h, v): part_open(k, w, h); quill(k, 330, 30, 220, expr="sheepish" if "sheepish" in v else "neutral"); k.unclip()
def kerensa_conf(k, w, h, v): part_open(k, w, h); kerensa(k, 160, 30, 210); k.unclip()
def pocket_part(k, w, h, v): part_open(k, w, h); k.brooch(330 + 52, 30 + 92, 9); k.unclip()
def wind_part(k, w, h, v):
    part_open(k, w, h)
    for j in range(3):
        y = 250 - j * 18; k.line([(SILL[0] - 10 - j * 10, y), (SILL[0] - 70 - j * 16, y - 6), (SILL[0] - 120 - j * 10, y + 4)], lw=0.8, amp=0.5)
    k.unclip()
def teapot_part(k, w, h, v): part_open(k, w, h); k.teapot(TX[1], 72, 26); k.unclip()

# ----------------------------------------------------------------------------- vignette (title card)
def _vig(k, w, h):
    k.floorboards(w, y=h * 0.32)
    k.window_view(w * 0.52, h * 0.42, w * 0.34, h * 0.36); k.rect(w * 0.5, h * 0.4, w * 0.38, 7, lw=1.0, fill=Wt)
    k.table_cloth(w * 0.4, h * 0.12, 120, 70); k.brooch(w * 0.7, h * 0.43, 9)
vignette = B.vignette_fn(_vig)

# ============================================================================= jobs
def jobs():
    FX = B.FX_GULL; ST = B.FX_STEAM
    J = []
    J.append(dict(name="hook", w=AW, h=AH, plate=hook_plate, seed=1101, parts=dict(**FX)))
    J.append(dict(name="cast", w=CW, h=CH, plate=cast_plate, seed=1102, parts={
        f"s{i}": dict(fn=B.cast_fig_fn(i, 4, fn), variants=V2) for i, (_, fn) in enumerate(CAST)}))
    J.append(dict(name="tables", w=AW, h=AH, plate=tables_plate, seed=1103, parts={
        f"n{i}": dict(fn=partial(num_part, i=i), variants=["base"]) for i in range(4)}))
    J.append(dict(name="sill", w=AW, h=AH, plate=sill_plate, seed=1104, parts=dict(
        kerensa=dict(fn=kerensa_part, variants=V2), brooch=dict(fn=brooch_part, variants=["base"]),
        reach=dict(fn=reach_part, variants=["base"]), gone=dict(fn=gone_part, variants=["base"]))))
    J.append(dict(name="lineup", w=4 * PW, h=AH, plate=lineup_plate, seed=1105, parts={
        f"s{i}": dict(fn=B.lineup_fig_fn(i, fn), variants=V3) for i, (_, fn) in enumerate(CAST)}))
    J.append(dict(name="kitchen", w=AW, h=AH, plate=kitchen_plate, seed=1106, parts=dict(
        agnes=dict(fn=agnes_kit, variants=V2), pip=dict(fn=pip_kit, variants=V2), **ST)))
    J.append(dict(name="pip", w=AW, h=AH, plate=pip_plate, seed=1107, parts={
        "pip": dict(fn=pip_talk, variants=V3), "agnes": dict(fn=agnes_listen, variants=V2),
        **{f"c{i}": dict(fn=partial(clue_part, i=i), variants=["base"]) for i in range(4)}}))
    J.append(dict(name="squares", w=AW, h=AH, plate=squares_plate, seed=1108, parts={
        **{f"r{i}": dict(fn=partial(rule_part, i=i), variants=["base"]) for i in range(4)},
        "names": dict(fn=names_part, variants=["base"])}))
    BT = {}
    for r, seq in (("a", ("WENNA", "QUILL", "LOVEDAY", "SPARGO")), ("b", ("QUILL", "WENNA", "LOVEDAY", "SPARGO")),
                   ("c", ("SPARGO", "LOVEDAY", "WENNA", "QUILL"))):
        for col, nm in enumerate(seq): BT[f"{r}{col}"] = dict(fn=partial(tok_part, row=r, col=col, nm=nm), variants=["base"])
    BT["xa"] = dict(fn=partial(cross_part, row="a"), variants=["base"]); BT["xb"] = dict(fn=partial(cross_part, row="b"), variants=["base"])
    BT["ring"] = dict(fn=ring_part, variants=["base"])
    J.append(dict(name="board", w=AW, h=AH, plate=board_plate, seed=1109, parts=BT))
    J.append(dict(name="confess", w=AW, h=AH, plate=confess_plate, seed=1110, parts=dict(
        quill=dict(fn=quill_conf, variants=["sheepish", "sheepish+blink"]), kerensa=dict(fn=kerensa_conf, variants=V2),
        pocket=dict(fn=pocket_part, variants=["base"]), wind=dict(fn=wind_part, variants=["base"]),
        teapot=dict(fn=teapot_part, variants=["base"]))))
    J.append(dict(name="vignette", w=384, h=384, plate=vignette, seed=1111))
    return J

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    J = [j for j in jobs() if not want or j["name"] in want]
    save_layers(OUT, J, B.make_ink)
