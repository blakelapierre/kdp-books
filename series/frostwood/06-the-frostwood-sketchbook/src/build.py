"""Builds the 6x9 interior PDF (grayscale, no bleed, mirrored margins, embedded fonts).
Same fonts / palette / page furniture as the other Frostwood Puzzle Books."""
import json, sys, math, random
sys.path.insert(0, ".")
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.lib.fonts import addMapping

G = "/usr/share/fonts/truetype/sand-box/google/"
for n, p in [("Crimson", "Crimson Text/CrimsonText-Regular.ttf"), ("Crimson-I", "Crimson Text/CrimsonText-Italic.ttf"),
             ("Crimson-B", "Crimson Text/CrimsonText-Bold.ttf"), ("Crimson-SB", "Crimson Text/CrimsonText-SemiBold.ttf"),
             ("Crimson-BI", "Crimson Text/CrimsonText-BoldItalic.ttf"),
             ("PlayfairSC", "Playfair Display SC/PlayfairDisplaySC-Regular.ttf"), ("PlayfairSC-B", "Playfair Display SC/PlayfairDisplaySC-Bold.ttf"),
             ("Plex", "IBM Plex Sans Condensed/IBMPlexSansCondensed-Regular.ttf"), ("Plex-M", "IBM Plex Sans Condensed/IBMPlexSansCondensed-SemiBold.ttf")]:
    pdfmetrics.registerFont(TTFont(n, G + p))
pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
from reportlab import rl_config
rl_config.canvas_basefontname = "Crimson"
ParagraphStyle.defaults["fontName"] = "Crimson"; ParagraphStyle.defaults["bulletFontName"] = "Crimson"
addMapping("Crimson", 0, 0, "Crimson"); addMapping("Crimson", 0, 1, "Crimson-I"); addMapping("Crimson", 1, 0, "Crimson-B"); addMapping("Crimson", 1, 1, "Crimson-BI")

D = json.load(open("../data.json"))
BANDS = ["Easy", "Medium", "Hard", "Expert"]
ALL = [p for b in BANDS for p in D[b]]
EX = D["Example"][0]
NP = len(ALL)
assert [p["num"] for p in ALL] == list(range(1, NP + 1))

W, H = 6 * inch, 9 * inch
INNER, OUTER, TOP, BOT = 0.75 * inch, 0.55 * inch, 0.7 * inch, 0.75 * inch
DARK = colors.Color(0.17, 0.17, 0.17); MID = colors.Color(0.45, 0.45, 0.45); FROST = colors.Color(0.62, 0.62, 0.62)
ICE = colors.Color(0.925, 0.925, 0.925); INK = colors.Color(0.1, 0.1, 0.1); GRIDC = colors.Color(0.62, 0.62, 0.62)
TITLE = "The Frostwood Sketchbook"
TW = W - INNER - OUTER; TH = H - TOP - BOT
from places import PLACES
from nonogram import solve as line_solve_grid, line_solve

PARTS = {
 "Easy": ("Part One", "The Lodge Sitting Room", 1,
          "Fifteen-by-fifteen sketches made indoors, by the fire and around the lodge. Start with the big numbers: a long run in a short row always covers its middle squares."),
 "Medium": ("Part Two", "The Village Green", 2,
            "Twenty-by-twenty sketches from the village below the lodge. More rows have several runs now, so work back and forth between rows and columns, a few squares at a time."),
 "Hard": ("Part Three", "The Pine Woods", 3,
          "Twenty-five-by-twenty-five sketches from the woods on the way up. Bigger grids and finer lines: dot the empty squares as you go, and the picture will start to show."),
 "Expert": ("Part Four", "The High Mountain", 4,
            "The largest and longest sketches in the book, drawn on the mountain. Each needs many passes over the rows and columns, but never a guess: there is always a next square to find."),
}
PREP = {"Easy": "", "Medium": "", "Hard": "", "Expert": ""}
VIEW = {}
for b in BANDS:
    assert len(PLACES[b]) >= len(D[b])
    for p, pl in zip(D[b], PLACES[b]): VIEW[p["num"]] = "Sketched " + pl

class Doc(BaseDocTemplate):
    def handle_pageBegin(self):
        p = self.page + 1
        left = INNER if p % 2 == 1 else OUTER
        for t in self.pageTemplates:
            for f in t.frames:
                f._x1 = left; f._geom()
        super().handle_pageBegin()
    def afterFlowable(self, fl):
        if getattr(fl, "section", None) is not None: self.section = fl.section
        if getattr(fl, "mark", None): self.marks[fl.mark] = self.page

def snowflake(c, x, y, r, col, lw=0.09):
    c.saveState(); c.setStrokeColor(col); c.setLineWidth(r * lw); c.setLineCap(1)
    for i in range(6):
        a = math.pi / 3 * i; c.line(x, y, x + r * math.cos(a), y + r * math.sin(a))
        bx, by = x + r * 0.55 * math.cos(a), y + r * 0.55 * math.sin(a)
        for s in (-1, 1):
            b = a + s * math.pi / 4; c.line(bx, by, bx + r * 0.3 * math.cos(b), by + r * 0.3 * math.sin(b))
    c.restoreState()

def pencil_icon(c, x, y, s):
    c.saveState(); c.translate(x, y); c.rotate(35)
    c.setStrokeColor(INK); c.setFillColor(colors.white); c.setLineWidth(0.6)
    c.rect(-s * 0.5, -s * 0.09, s * 0.78, s * 0.18, stroke=1, fill=1)
    p = c.beginPath(); p.moveTo(s * 0.28, -s * 0.09); p.lineTo(s * 0.5, 0); p.lineTo(s * 0.28, s * 0.09); p.close(); c.drawPath(p, stroke=1, fill=0)
    c.setFillColor(INK); p = c.beginPath(); p.moveTo(s * 0.43, -s * 0.03); p.lineTo(s * 0.5, 0); p.lineTo(s * 0.43, s * 0.03); p.close(); c.drawPath(p, stroke=0, fill=1)
    c.restoreState()

def page_end(c, doc):
    p = doc.page; kind = getattr(doc, "pkind", {}).get(p, "normal")
    if kind == "blank":
        draw_ill(c, "v_moon", (INNER if p % 2 else OUTER) + (TW - 1.9 * inch) / 2, BOT + TH / 2 - 0.42 * inch, 1.9 * inch, 0.85 * inch); return
    if kind in ("title", "nofolio"): return
    c.saveState()
    c.setFont("Crimson", 9); c.setFillColor(MID)
    c.drawCentredString(W / 2 + ((INNER - OUTER) / 2 if p % 2 else -(INNER - OUTER) / 2), 0.42 * inch, str(p))
    if kind != "opener":
        c.setFont("PlayfairSC", 7.5); c.setFillColor(MID)
        hdr = TITLE if p % 2 == 0 else getattr(doc, "section", "")
        if p % 2 == 0: c.drawString(OUTER, H - 0.42 * inch, hdr)
        else: c.drawRightString(W - OUTER, H - 0.42 * inch, hdr)
    c.restoreState()

class Kind(Flowable):
    def __init__(s, kind=None, section=None, mark=None): s.kind = kind; s.section = section; s.mark = mark; s.width = s.height = 0
    def wrap(s, aw, ah): return 0, 0
    def draw(s):
        doc = s.canv._doctemplate
        if s.kind: doc.pkind[doc.page] = s.kind

body = ParagraphStyle("b", fontName="Crimson", fontSize=11.2, leading=15, alignment=TA_JUSTIFY, firstLineIndent=14, textColor=INK)
body0 = ParagraphStyle("b0", parent=body, firstLineIndent=0)
h1 = ParagraphStyle("h1", fontName="PlayfairSC-B", fontSize=20, leading=24, alignment=TA_CENTER, textColor=DARK, spaceAfter=2)
kick = ParagraphStyle("k", fontName="PlayfairSC", fontSize=9.5, leading=12, alignment=TA_CENTER, textColor=MID, spaceAfter=4)
small = ParagraphStyle("s", fontName="Crimson-I", fontSize=10, leading=13, alignment=TA_CENTER, textColor=colors.Color(.3, .3, .3))
bullet = ParagraphStyle("li", parent=body0, alignment=TA_LEFT, leftIndent=14, firstLineIndent=-12, spaceAfter=3)
FL = "<font name='DejaVu' color='#9e9e9e' size='9'>❄</font>&nbsp;&nbsp;"

class Flake(Flowable):
    def __init__(s, r=6): s.r = r; s.width = 0; s.height = 2 * r + 6
    def wrap(s, aw, ah): s.aw = aw; return aw, s.height
    def draw(s):
        c = s.canv; c.setStrokeColor(FROST); c.setLineWidth(0.5)
        c.line(s.aw / 2 - 60, s.r + 3, s.aw / 2 - s.r - 6, s.r + 3); c.line(s.aw / 2 + s.r + 6, s.r + 3, s.aw / 2 + 60, s.r + 3)
        snowflake(c, s.aw / 2, s.r + 3, s.r, DARK)
def heading(k, t): return [Paragraph(k, kick), Paragraph(t, h1), Flake(), Spacer(1, 8)]

# ----------------------------------------------------------------------------- nonogram drawing
def clue_font(s): return min(8.6, max(5.8, s * 0.62))
GAP = 2.3
def row_clue_width(clue, fs):
    nums = clue or [0]
    return sum(pdfmetrics.stringWidth(str(v), "Plex-M", fs) for v in nums) + GAP * (len(nums) - 1) + 3
def gutters(p, s):
    fs = clue_font(s)
    left = max(row_clue_width(r, fs) for r in p["rows"]) + 2
    top = max(len(c) or 1 for c in p["cols"]) * fs * 1.08 + 3
    return left, top

def fit_cell(ps, wmax, hmax, smax):
    """Largest cell size (pt) so every puzzle in ps fits in wmax x hmax with its clue gutters."""
    s = smax
    while s > 4:
        if all((lambda g: p["n"] * s + g[0] <= wmax and p["n"] * s + g[1] <= hmax)(gutters(p, s)) for p in ps): return s
        s -= 0.1
    raise SystemExit("cannot fit")

def draw_nono(c, x0, y0, s, p, mode="puzzle", state=None, clues=True, labels=False, lw_scale=1.0):
    """(x0, y0) = lower-left corner of the cell grid. Row clues sit to its left, column clues above.
    mode 'puzzle' = empty grid; 'state' = draw a partial state (1 shaded, 0 dotted); 'solution' = the picture."""
    n = p["n"]; top = y0 + n * s; fs = clue_font(s)
    c.saveState()
    if mode == "solution":
        c.setFillColor(INK)
        for r, line in enumerate(p["picture"]):
            for cc, v in enumerate(line):
                if v == "#": c.rect(x0 + cc * s, y0 + (n - 1 - r) * s, s, s, stroke=0, fill=1)
    elif mode == "state" and state:
        for r in range(n):
            for cc in range(n):
                v = state[r][cc]; x = x0 + cc * s; y = y0 + (n - 1 - r) * s
                if v == 1: c.setFillColor(INK); c.rect(x, y, s, s, stroke=0, fill=1)
                elif v == 0: c.setFillColor(MID); c.circle(x + s / 2, y + s / 2, max(0.8, s * 0.08), stroke=0, fill=1)
    if clues:
        c.setFillColor(INK); c.setFont("Plex-M", fs)
        for r, clue in enumerate(p["rows"]):
            nums = clue or [0]; x = x0 - 3; y = y0 + (n - 1 - r) * s + s / 2 - fs * 0.35
            for v in reversed(nums):
                t = str(v); c.drawRightString(x, y, t); x -= pdfmetrics.stringWidth(t, "Plex-M", fs) + GAP
        for cc, clue in enumerate(p["cols"]):
            nums = clue or [0]; y = top + 3 + fs * 0.12
            for v in reversed(nums):
                c.drawCentredString(x0 + cc * s + s / 2, y, str(v)); y += fs * 1.08
        # faint guide bands for the clue gutters, every fifth line
    thin = (0.35 if s > 8 else 0.25) * lw_scale; thick = (0.95 if s > 8 else 0.6) * lw_scale
    c.setStrokeColor(GRIDC if mode != "solution" else colors.Color(0.75, 0.75, 0.75)); c.setLineWidth(thin)
    for i in range(1, n):
        if i % 5 and True:
            c.line(x0 + i * s, y0, x0 + i * s, top); c.line(x0, y0 + i * s, x0 + n * s, y0 + i * s)
    c.setStrokeColor(DARK); c.setLineWidth(thick * 0.8)
    for i in range(5, n, 5):
        c.line(x0 + i * s, y0, x0 + i * s, top); c.line(x0, y0 + i * s, x0 + n * s, y0 + i * s)
    c.setStrokeColor(INK); c.setLineWidth(thick * 1.3); c.rect(x0, y0, n * s, n * s)
    if labels:
        c.setFont("Plex", 6.5); c.setFillColor(MID)
        for i in range(n):
            c.drawRightString(x0 - gutters(p, s)[0] - 2, y0 + (n - 1 - i) * s + s / 2 - 2.2, str(i + 1))
    c.restoreState()

def rating(c, x, y, k, r=4.2, gap=11):
    for i in range(4):
        snowflake(c, x - (3 - i) * gap, y, r, DARK if i < k else colors.Color(.78, .78, .78), lw=0.12)

HEAD = 0.36 * inch
CELL = {}
def band_cell(band):
    if band not in CELL:
        ps = D["Hard"] + D["Expert"] if band in ("Hard", "Expert") else D[band]
        if band == "Easy": CELL[band] = fit_cell(ps, TW - 4, TH / 2 - HEAD - 22, 12.0)
        else: CELL[band] = fit_cell(ps, TW - 4, TH - HEAD - 1.45 * inch, 14.0)
    return CELL[band]

class PuzzleBlock(Flowable):
    def __init__(s, p, h): s.p = p; s.h = h; s.width = TW; s.height = h
    def wrap(s, aw, ah): return TW, s.h
    def draw(s):
        c = s.canv; p = s.p; n = p["n"]; cs = band_cell(p["band"]); gl, gt = gutters(p, cs)
        full = s.h > TH / 2
        block = HEAD + gt + n * cs
        ytop = s.h if full else s.h - max(0, (s.h - block - 10) / 2)
        c.setFillColor(DARK); c.setFont("PlayfairSC-B", 15); c.drawString(0, ytop - 13, f"No. {p['num']}")
        wno = pdfmetrics.stringWidth(f"No. {p['num']}", "PlayfairSC-B", 15)
        c.setFont("Crimson-I", 10.5); c.setFillColor(MID); c.drawString(wno + 8, ytop - 13, VIEW[p["num"]])
        rating(c, TW - 5, ytop - 9, PARTS[p["band"]][2])
        c.setFont("Plex", 7.5); c.setFillColor(MID)
        c.drawRightString(TW - 50, ytop - 12, f"{p['band'].upper()} · {n}×{n}")
        c.setStrokeColor(FROST); c.setLineWidth(0.5); c.line(0, ytop - 20, TW, ytop - 20)
        gw = n * cs; x0 = (TW - (gw + gl)) / 2 + gl
        y0 = ytop - HEAD - gt - gw
        draw_nono(c, x0, y0, cs, p)
        if full:
            yb = 6
            free_lo, free_hi = yb + 30, y0 - 10
            vh = min(0.85 * inch, free_hi - free_lo)
            if vh >= 0.5 * inch:
                draw_ill(c, VIGNETTES[p["num"] % len(VIGNETTES)], 0, free_lo + (free_hi - free_lo - vh) / 2, TW, vh)
            c.setStrokeColor(FROST); c.setLineWidth(0.5); c.line(0, yb + 16, TW, yb + 16)
            c.setFont("PlayfairSC", 8.5); c.setFillColor(MID)
            c.drawString(0, yb, "Started"); c.line(40, yb - 1, 110, yb - 1)
            c.drawString(128, yb, "Finished"); c.line(172, yb - 1, 242, yb - 1)
            c.drawString(258, yb, "It shows"); c.line(300, yb - 1, TW, yb - 1)

class SolutionBlock(Flowable):
    def __init__(s, p, w, h, pic): s.p = p; s.width = w; s.height = h; s.pic = pic
    def wrap(s, aw, ah): return s.width, s.height
    def draw(s):
        c = s.canv; p = s.p; n = p["n"]; cs = s.pic / n
        c.setFont("PlayfairSC-B", 9.5); c.setFillColor(DARK); c.drawCentredString(s.width / 2, s.height - 10, f"No. {p['num']}")
        x0 = (s.width - s.pic) / 2; y0 = s.height - 15 - s.pic
        draw_nono(c, x0, y0, cs, p, mode="solution", clues=False, lw_scale=0.6)
        c.setFont("Crimson-I", 9); c.setFillColor(MID); c.drawCentredString(s.width / 2, y0 - 10, p["name"])

EX_STATE = None
def example_state():
    """Partial state for the worked example: rows 4 and 8 filled, middle four squares of rows 3 and 7 (one pass over the rows)."""
    global EX_STATE
    if EX_STATE is None:
        n = EX["n"]; g = [[-1] * n for _ in range(n)]
        for r in range(n):
            new = line_solve(EX["rows"][r], g[r]); assert new is not None; g[r] = new
        EX_STATE = g
    return EX_STATE

class Example(Flowable):
    def __init__(s, cell, cap):
        s.cell = cell; s.cap = cap; s.width = TW
        gl, gt = gutters(EX, cell); s.gl, s.gt = gl, gt
        s.height = cell * EX["n"] + gt + 18
    def wrap(s, aw, ah): return TW, s.height
    def draw(s):
        c = s.canv; n = EX["n"]; cs = s.cell; gw = n * cs; box = gw + s.gl
        gap = (TW - 3 * box) / 2; x = 0
        for i, mode in enumerate(("puzzle", "state", "solution")):
            draw_nono(c, x + s.gl, 16, cs, EX, mode=mode, state=example_state() if mode == "state" else None)
            c.setFont("Crimson-I", 9); c.setFillColor(MID); c.drawCentredString(x + s.gl + gw / 2, 3, s.cap[i])
            x += box + gap

import os
ILL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "illustrations")
VIGNETTES = ["v_pencil", "v_mug", "v_cat", "v_lantern", "v_cottage", "v_moon"]
def ill(name): return os.path.join(ILL, name + ".png")
def draw_ill(c, name, x, y, w, h):
    from reportlab.lib.utils import ImageReader
    img = ImageReader(ill(name)); iw, ih = img.getSize()
    sc = min(w / iw, h / ih); dw, dh = iw * sc, ih * sc
    c.drawImage(ill(name), x + (w - dw) / 2, y + (h - dh) / 2, dw, dh)
class Art(Flowable):
    def __init__(s, name, w, h): s.name = name; s.width = w; s.height = h
    def wrap(s, aw, ah): return s.width, s.height
    def draw(s): draw_ill(s.canv, s.name, 0, 0, s.width, s.height)

SUB = f"{NP} Nonogram Picture Logic Puzzles"
def build(recto_fix):
    S = []
    def recto(tag):
        S.append(PageBreak())
        if tag in recto_fix: S.extend([Kind("blank"), PageBreak()])
        S.append(Kind(mark=tag))
    S += [Kind("title"), Spacer(1, 2.2 * inch),
          Paragraph("The Frostwood<br/>Sketchbook", ParagraphStyle("ht", fontName="PlayfairSC-B", fontSize=26, leading=30, alignment=TA_CENTER, textColor=DARK)),
          Spacer(1, 10), Flake(), Spacer(1, 0.5 * inch), Art("v_pencil", TW, 0.85 * inch),
          PageBreak(), Kind("title"), Spacer(1, 0.05 * inch), Art("frontispiece", TW, 7.0 * inch), Spacer(1, 6),
          Paragraph("The sketchbook on the sitting-room table", ParagraphStyle("fc", parent=small, fontSize=10)),
          PageBreak()]
    S += [Kind("title"), Spacer(1, 0.5 * inch),
          Paragraph("A Picture Logic Puzzle Book", ParagraphStyle("t0", parent=kick, fontSize=11, textColor=MID)),
          Spacer(1, 10),
          Paragraph("The Frostwood<br/>Sketchbook", ParagraphStyle("tt", fontName="PlayfairSC-B", fontSize=36, leading=40, alignment=TA_CENTER, textColor=DARK)),
          Spacer(1, 14),
          Paragraph(f"{SUB}<br/>from the fireside to the mountaintop", ParagraphStyle("t2", parent=small, fontSize=13, leading=17)),
          Spacer(1, 0.35 * inch), Art("title", TW, 2.5 * inch), Spacer(1, 0.35 * inch),
          Paragraph("A Frostwood Puzzle Book", ParagraphStyle("t3", parent=kick, fontSize=10, textColor=DARK)),
          Paragraph("Blake La Pierre", ParagraphStyle("t4", parent=small, fontSize=11))]
    S += [PageBreak(), Kind("nofolio"), Spacer(1, 3.4 * inch)]
    cs = ParagraphStyle("cp", parent=body0, fontSize=9, leading=12, alignment=TA_LEFT)
    for t in [f"<i>The Frostwood Sketchbook: {SUB}</i>",
              "Copyright © 2026 Blake La Pierre. All rights reserved.",
              "No part of this book may be reproduced in any form without written permission from the author, except for brief quotations in reviews. Readers are welcome to photocopy puzzle pages for their own personal use while solving.",
              "Frostwood, its village, railway, lodge, woods and mountain are imaginary. Any resemblance to real places is coincidental.",
              "The puzzle pictures are drawn from the Noto Emoji typeface (Google, SIL Open Font License), redrawn as grids of squares.",
              "First edition, 2026",
              "Set in Crimson Text, Playfair Display SC and IBM Plex Sans Condensed, used under the SIL Open Font License."]:
        S += [Paragraph(t, cs), Spacer(1, 6)]
    recto("contents")
    S += [Kind(section="Contents"), Spacer(1, 0.3 * inch)] + heading(TITLE, "Contents")
    S.append(("TOC",))
    S += [Spacer(1, 0.3 * inch),
          Paragraph("Every winter someone at the Frostwood Lodge keeps a sketchbook on the sitting-room table, and every guest adds a drawing. "
                    "This year the drawings were written down in numbers instead of pencil lines, so that anyone could draw them again. "
                    f"{NP} sketches wait inside, from the fireside to the mountaintop. Each one has exactly one solution, and each can be finished by logic alone, with no guessing.",
                    ParagraphStyle("in", parent=small, fontSize=10.5, leading=14))]
    recto("howto")
    S += [Kind(section="How to Play"), Spacer(1, 0.1 * inch)] + heading("Sharpen Your Pencil", "How to Play")[:-1] + [Spacer(1, 4)]
    hb = ParagraphStyle("hb", parent=bullet, fontSize=10.5, leading=13.6, spaceAfter=2.5)
    S += [Paragraph("Each puzzle is a square grid hiding a picture. Shade the right squares and the sketch appears. These puzzles are often called <b>nonograms</b>, <b>hanjie</b> or <b>paint-by-number grids</b>.",
                    ParagraphStyle("hb0", parent=body0, fontSize=10.8, leading=14)), Spacer(1, 3)]
    for t in ["The numbers beside each <b>row</b> give the lengths of the runs of shaded squares in that row, in order from left to right.",
              "The numbers above each <b>column</b> give the runs in that column, in order from top to bottom.",
              "Between two runs there is <b>at least one empty square</b>. A row marked <b>0</b> is empty.",
              "Shade squares that must be filled, and put a small dot in squares you know are empty."]:
        S.append(Paragraph(FL + t, hb))
    S += [Spacer(1, 4), Paragraph("<b>Useful Tricks</b>", ParagraphStyle("x", parent=body0, alignment=TA_CENTER, textColor=DARK)), Spacer(1, 3)]
    for t in ["<b>Big runs first.</b> Slide a run as far left as it can go, then as far right. Any squares it covers both times must be shaded. A run of 12 in a row of 15 always covers the middle 9.",
              "<b>Add them up.</b> For a row with several runs, add the runs plus one gap between each. If the total is close to the row length, the same sliding trick shades squares inside each run.",
              "<b>Finished lines.</b> When a row or column has all its runs, dot every other square in it.",
              "<b>Edges.</b> A shaded square at the edge of the grid starts the first run (or ends the last one), so you can shade the rest of that run at once.",
              "<b>Back and forth.</b> Every square you settle in a row is a new clue for its column. Keep switching between rows and columns. Every puzzle in this book can be finished this way, one line at a time, with no guessing."]:
        S.append(Paragraph(FL + t, hb))
    S += [PageBreak(), Kind(section="How to Play"), Spacer(1, 0.05 * inch)] + heading("Let’s Draw a Cottage", "A Worked Example")
    S.append(Example(11.5, ["The puzzle", "After the rows", "Solved"]))
    S.append(Spacer(1, 8))
    S.append(Paragraph("This small 8×8 sketch is a good place to start. Rows are counted from the top and columns from the left.",
                       ParagraphStyle("exi", parent=body0, fontSize=10.4, leading=13.4, spaceAfter=3)))
    ex = ParagraphStyle("exs", parent=bullet, fontSize=10.4, leading=13.4, spaceAfter=2.5)
    for i, t in enumerate(EX_STEPS, 1):
        S.append(Paragraph(f"<font name='PlayfairSC-B' color='#2b2b2b'>{i}.</font>&nbsp;&nbsp;" + t, ex))
    S.append(Spacer(1, 4))
    S.append(Paragraph("Solutions, with the name of every picture, are at the back of the book.", ParagraphStyle("sm2", parent=small, fontSize=9.5)))
    for band in BANDS:
        part, place, k, blurb = PARTS[band]; ps = D[band]; n = ps[0]["n"]
        recto(band)
        S += [Kind("opener"), Kind(section=f"{part} · {place}"), Spacer(1, 0.9 * inch)] + heading(f"{part} · {band} · {n}×{n}", place)
        S += [Paragraph(f"Puzzles {ps[0]['num']} to {ps[-1]['num']}", ParagraphStyle("pn", parent=small, fontSize=11)), Spacer(1, 14),
              Paragraph(blurb, ParagraphStyle("bl", parent=small, fontSize=11, leading=15)), Spacer(1, 0.4 * inch),
              Art("opener-" + band.lower(), TW, 2.4 * inch)]
        S.append(PageBreak())
        if band == "Easy":
            for i in range(0, len(ps), 2):
                S += [PuzzleBlock(ps[i], TH / 2 - 1)]
                if i + 1 < len(ps): S.append(PuzzleBlock(ps[i + 1], TH / 2 - 1))
                S.append(PageBreak())
        else:
            for p in ps: S += [PuzzleBlock(p, TH - 2), PageBreak()]
        S.pop()
    recto("solutions")
    S += [Kind("opener"), Kind(section="Solutions"), Spacer(1, 2.4 * inch)] + heading("The Finished Sketches", "Solutions")
    S.append(Paragraph("Each solution shows the finished picture and its name.", small))
    cols, rows = 3, 4; per = cols * rows; bw = TW / cols; bh = (TH - 4) / rows
    pic = min(bw - 22, bh - 32)
    for i in range(0, NP, per):
        chunk = ALL[i:i + per]
        S += [PageBreak(), Kind(section=f"Solutions · Nos. {chunk[0]['num']}–{chunk[-1]['num']}")]
        grid = []
        for r in range(rows):
            row = []
            for j in range(i + r * cols, i + r * cols + cols):
                row.append(SolutionBlock(ALL[j], bw - 6, bh - 4, pic) if j < NP else "")
            grid.append(row)
        t = Table(grid, colWidths=[bw] * cols, rowHeights=[bh] * rows)
        t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Crimson", 10), ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                               ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
        S.append(t)
    recto("about")
    S += [Kind("nofolio"), Spacer(1, 0.7 * inch)] + heading("Thank You for Sketching", TITLE)
    S.append(Paragraph("If you enjoyed bringing the Frostwood sketches back to life, a short review helps other puzzlers find the book. "
                       "The lodge keeps every one, tucked inside the back cover of next winter’s sketchbook.",
                       ParagraphStyle("ty", parent=body0, alignment=TA_CENTER)))
    S += [Spacer(1, 0.3 * inch), Flake(), Spacer(1, 8),
          Paragraph("Also by Blake La Pierre", ParagraphStyle("ab", parent=kick, fontSize=11, textColor=DARK)),
          Paragraph("A Frostwood Puzzle Book", ParagraphStyle("ab0", parent=small, fontSize=9.5)), Spacer(1, 6)]
    for t, d in [("The Thief Stayed the Night", "A snowbound hotel mystery puzzle book. Twelve cozy elimination cases at the Frostwood Lodge."),
                 ("Frostwood Express", "200 Train Tracks logic puzzles. Lay the railway that climbs from the valley to the lodge."),
                 ("Stars over Frostwood", "180 Star Battle logic puzzles. Chart the winter sky from the village green to the lodge observatory."),
                 ("Tents in Frostwood", "180 Tents and Trees logic puzzles. Pitch camp among the pines, from the lodge meadow to the ridge."),
                 ("Riddles by the Frostwood Fire", "140 cozy winter riddles and text logic puzzles, made for reading on a Kindle.")]:
        S += [Paragraph(f"<i>{t}</i>", ParagraphStyle("ab2", parent=body0, alignment=TA_CENTER, fontSize=12.5, leading=15)),
              Paragraph(d, ParagraphStyle("ab3", parent=small, fontSize=9.5, leading=12)), Spacer(1, 6)]
    S += [Spacer(1, 0.08 * inch), Art("thanks", TW, 1.2 * inch)]
    S.append(("PAD",))
    return S

EX_STEPS = [
    "Rows 4 and 8 both say <b>8</b>, the full width of the grid, so every square in them is shaded.",
    "Rows 3 and 7 say <b>6</b>. Slide a run of six all the way left, then all the way right: either way it covers columns 3 to 6, so shade those four squares in both rows. That is the middle picture.",
    "Now the columns. Columns 1 and 8 say <b>1 1</b> and already have their two shaded squares (rows 4 and 8), so dot the rest. Columns 2 and 7 say <b>6</b>: one run must reach both row 4 and row 8, so it fills rows 3 to 8.",
    "Back to the rows, then the columns again. Each pass settles a few more squares, and soon the sketch is done: a little cottage with its door, standing on the snow.",
]

def render(recto_fix, out, toc):
    S = build(recto_fix)
    if toc.get("_odd"): S += [PageBreak(), Kind("blank")]
    for i, x in enumerate(S):
        if x == ("PAD",): S[i] = Spacer(0, 0); continue
        if isinstance(x, tuple):
            rows = [("How to Play", toc.get("howto", 0)), ("A Worked Example", toc.get("howto", 0) + 1)]
            for b in BANDS:
                part, place, k, _ = PARTS[b]; ps = D[b]
                rows.append((f"{part} · {place}<br/><font size='9.5' color='#737373'>{b} · {ps[0]['n']}×{ps[0]['n']} · Puzzles {ps[0]['num']}–{ps[-1]['num']}</font>", toc.get(b, 0)))
            rows += [("Solutions", toc.get("solutions", 0))]
            t = Table([[Paragraph(a, ParagraphStyle("tc", parent=body0, fontSize=11.5, leading=14)), str(b)] for a, b in rows], colWidths=[TW - 0.5 * inch, 0.5 * inch])
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Crimson", 11), ("FONT", (1, 0), (1, -1), "Crimson", 11.5), ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), 0.3, FROST), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
            S[i] = t
    fr = Frame(INNER, BOT, TW, TH, id="f", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc = Doc(out, pagesize=(W, H), initialFontName="Crimson", title=f"The Frostwood Sketchbook: {SUB}", author="Blake La Pierre",
              subject="Nonogram picture logic puzzle book", pageTemplates=[PageTemplate("normal", [fr], onPageEnd=page_end)])
    doc.pkind = {}; doc.marks = {}; doc.section = ""
    doc.build(S)
    return doc.marks, doc.page

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "../frostwood-06-the-frostwood-sketchbook-interior.pdf"
    fix = set(); toc = {}
    for it in range(40):
        marks, pages = render(fix, out, toc)
        bad = sorted((p, k) for k, p in marks.items() if p % 2 == 0)
        marks["_odd"] = toc.get("_odd", False) ^ (pages % 2 == 1)
        if not bad and marks == toc: break
        if bad: fix ^= {bad[0][1]}
        toc = marks
    marks.pop("_odd", None)
    print("pages", pages, "marks", marks, "cells", {b: round(v, 2) for b, v in CELL.items()})
    json.dump(dict(pages=pages, marks=marks, cell_pt={b: round(v, 2) for b, v in CELL.items()}), open("../build-info.json", "w"))
