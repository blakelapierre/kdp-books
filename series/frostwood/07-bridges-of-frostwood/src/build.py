"""Builds the 6x9 interior PDF (grayscale, no bleed, mirrored margins, embedded fonts).
Same fonts / palette / page furniture as the other Frostwood Puzzle Books."""
import json, sys, math, os
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
from names import NAMES

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

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "..", "data.json")))
BANDS = ["Easy", "Medium", "Hard", "Expert"]
ALL = [p for b in BANDS for p in D[b]]
EX = D["Example"][0]
NP = len(ALL)
assert [p["num"] for p in ALL] == list(range(1, NP + 1))
# the worked-example text below describes exactly this puzzle
assert EX["islands"] == [[0, 0, 3], [0, 2, 5], [0, 4, 3], [3, 0, 2], [3, 2, 3], [4, 1, 2], [4, 4, 4]], EX["islands"]
assert EX["bridges"] == [[0, 1, 2], [0, 3, 1], [1, 2, 1], [1, 4, 2], [2, 6, 2], [3, 4, 1], [5, 6, 2]]

W, H = 6 * inch, 9 * inch
INNER, OUTER, TOP, BOT = 0.75 * inch, 0.55 * inch, 0.7 * inch, 0.75 * inch
DARK = colors.Color(0.17, 0.17, 0.17); MID = colors.Color(0.45, 0.45, 0.45); FROST = colors.Color(0.62, 0.62, 0.62)
ICE = colors.Color(0.925, 0.925, 0.925); INK = colors.Color(0.1, 0.1, 0.1); DOT = colors.Color(0.66, 0.66, 0.66)
TITLE = "Bridges of Frostwood"
TW = W - INNER - OUTER; TH = H - TOP - BOT

PARTS = {
 "Easy": ("Part One", "The Lodge Pond", 1,
          "Seven-by-seven corners of the pond, ten to fourteen islands each. Start with the islands that have only one or two neighbours, and with the big numbers: a 4 in a corner or a 6 on an edge has no choice at all."),
 "Medium": ("Part Two", "The Mill Stream", 2,
            "Nine-by-nine stretches of the village stream. Counting still does most of the work, but now and then you will need the network rule: no little group of islands may be closed off from the rest."),
 "Hard": ("Part Three", "The Reed Marsh", 3,
          "Eleven-by-eleven pools in the marsh, up to thirty islands. Somewhere in each one, counting and the network rule stop, and you will need a short “what if?” to see which bridge must be built."),
 "Expert": ("Part Four", "The Lake of Islands", 4,
            "Thirteen-by-fifteen maps of the frozen lake, thirty-four to forty-four islands each, the largest in the book. Several what-if steps each. Take your time and keep a soft eraser close."),
}
PREP = {"Easy": "At ", "Medium": "Along ", "Hard": "Across ", "Expert": "Among "}
VIEW = [NAMES[b][i] for b in BANDS for i in range(len(D[b]))]


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


def bridge_icon(c, x, y, s):
    """Two islands joined by a double bridge, centred on (x, y)."""
    c.saveState(); c.setStrokeColor(INK); c.setLineWidth(max(0.6, s * 0.06))
    c.line(x - 0.35 * s, y + 0.08 * s, x + 0.35 * s, y + 0.08 * s); c.line(x - 0.35 * s, y - 0.08 * s, x + 0.35 * s, y - 0.08 * s)
    c.setFillColor(colors.white)
    for sx in (-1, 1): c.circle(x + sx * 0.38 * s, y, 0.17 * s, stroke=1, fill=1)
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


RAD = 0.36   # island radius as a fraction of the grid step

def grid_size(p, s):
    """Width and height of the drawn grid (outer edges of the outer islands) at step s."""
    return (p["w"] - 1) * s + 2 * RAD * s, (p["h"] - 1) * s + 2 * RAD * s


def draw_hashi(c, x0, ytop, s, p, bridges=(), dots=True, fs=None):
    """(x0, ytop) = top-left corner of the drawn grid. Island (r, c) sits at x0 + R + c*s, ytop - R - r*s."""
    R = RAD * s; isl = p["islands"]
    X = lambda cc: x0 + R + cc * s; Y = lambda rr: ytop - R - rr * s
    occ = {(r, cc) for r, cc, _ in isl}
    c.saveState()
    if dots:
        c.setFillColor(DOT); dr = max(0.45, s * 0.028)
        for r in range(p["h"]):
            for cc in range(p["w"]):
                if (r, cc) not in occ: c.circle(X(cc), Y(r), dr, stroke=0, fill=1)
    lw = max(0.6, min(1.5, s * 0.05)); off = s * 0.1
    c.setStrokeColor(INK); c.setLineWidth(lw); c.setLineCap(0)
    for i, j, k in bridges:
        (r1, c1, _), (r2, c2, _) = isl[i], isl[j]
        if r1 == r2:
            for o in ((0,) if k == 1 else (-off, off)): c.line(X(c1), Y(r1) + o, X(c2), Y(r2) + o)
        else:
            for o in ((0,) if k == 1 else (-off, off)): c.line(X(c1) + o, Y(r1), X(c2) + o, Y(r2))
    fs = fs or R * 1.18
    c.setLineWidth(max(0.5, min(1.1, s * 0.035))); c.setFillColor(colors.white)
    for r, cc, n in isl:
        c.setFillColor(colors.white); c.circle(X(cc), Y(r), R, stroke=1, fill=1)
        c.setFillColor(INK); c.setFont("Plex-M", fs); c.drawCentredString(X(cc), Y(r) - fs * 0.35, str(n))
    c.restoreState()


def rating(c, x, y, k, r=4.2, gap=11):
    for i in range(4):
        snowflake(c, x - (3 - i) * gap, y, r, DARK if i < k else colors.Color(.78, .78, .78), lw=0.12)


STEP = {"Easy": 0.42 * inch, "Medium": 0.33 * inch, "Hard": 0.42 * inch, "Expert": 0.36 * inch}


class PuzzleBlock(Flowable):
    def __init__(s, p, h): s.p = p; s.h = h; s.width = TW; s.height = h
    def wrap(s, aw, ah): return TW, s.h
    def draw(s):
        c = s.canv; p = s.p; cs = STEP[p["band"]]
        gw, gh = grid_size(p, cs)
        full = s.h > TH / 2
        foot = 0.42 * inch if full else 0
        hdr = 0.3 * inch; gap = 0.16 * inch
        block = hdr + gap + gh
        if full: ytop = s.h
        else: ytop = s.h - max(0, (s.h - block) / 2 - 2)
        c.setFillColor(DARK); c.setFont("PlayfairSC-B", 15); c.drawString(0, ytop - 13, f"No. {p['num']}")
        wno = pdfmetrics.stringWidth(f"No. {p['num']}", "PlayfairSC-B", 15)
        c.setFont("Crimson-I", 10.5); c.setFillColor(MID)
        c.drawString(wno + 8, ytop - 13, PREP[p["band"]] + VIEW[p["num"] - 1])
        rating(c, TW - 5, ytop - 9, PARTS[p["band"]][2])
        c.setFont("Plex", 7.5); c.setFillColor(MID)
        c.drawRightString(TW - 50, ytop - 12, f"{p['band'].upper()} · {len(p['islands'])} ISLANDS")
        c.setStrokeColor(FROST); c.setLineWidth(0.5); c.line(0, ytop - 20, TW, ytop - 20)
        gtop = ytop - hdr - gap
        draw_hashi(c, (TW - gw) / 2, gtop, cs, p)
        if full:
            free_lo, free_hi = foot, gtop - gh - 6
            vh = min(0.85 * inch, free_hi - free_lo - 6)
            if vh >= 0.5 * inch:
                draw_ill(c, VIGNETTES[p["num"] % len(VIGNETTES)], 0, free_lo + (free_hi - free_lo - vh) / 2, TW, vh)
            yb = 6; c.setStrokeColor(FROST); c.setLineWidth(0.5); c.line(0, yb + 16, TW, yb + 16)
            c.setFont("PlayfairSC", 8.5); c.setFillColor(MID)
            c.drawString(0, yb, "Started"); c.line(40, yb - 1, 120, yb - 1)
            c.drawString(146, yb, "Finished"); c.line(190, yb - 1, 270, yb - 1)
            c.drawRightString(TW - 22, yb, "All joined"); bridge_icon(c, TW - 9, yb + 3, 16)


class SolutionBlock(Flowable):
    def __init__(s, p, w, h, cell): s.p = p; s.width = w; s.height = h; s.cell = cell
    def wrap(s, aw, ah): return s.width, s.height
    def draw(s):
        c = s.canv; p = s.p; cs = s.cell
        gw, gh = grid_size(p, cs)
        c.setFont("PlayfairSC-B", 10); c.setFillColor(DARK); c.drawString(0, s.height - 10, f"No. {p['num']}")
        draw_hashi(c, (s.width - gw) / 2, s.height - 15, cs, p, bridges=p["bridges"], dots=False, fs=max(4.6, RAD * cs * 1.25))


class Example(Flowable):
    def __init__(s, panels, cell, cap):
        s.panels = panels; s.cell = cell; s.cap = cap; s.width = TW
        s.height = grid_size(EX, cell)[1] + 24
    def wrap(s, aw, ah): return TW, s.height
    def draw(s):
        c = s.canv; cs = s.cell; k = len(s.panels)
        gw, gh = grid_size(EX, cs)
        gap = (TW - k * gw - 16) / max(k - 1, 1); x = 8
        for i, br in enumerate(s.panels):
            c.setStrokeColor(FROST); c.setLineWidth(0.5); c.roundRect(x - 6, 14, gw + 12, gh + 12, 4, stroke=1, fill=0)
            draw_hashi(c, x, s.height - 4, cs, EX, bridges=br)
            c.setFont("Crimson-I", 9); c.setFillColor(MID); c.drawCentredString(x + gw / 2, 2, s.cap[i])
            x += gw + gap


class RuleArt(Flowable):
    """Three tiny diagrams: a legal single and double bridge, a crossing (not allowed), a diagonal (not allowed)."""
    def __init__(s): s.width = TW; s.height = 0.95 * inch
    def wrap(s, aw, ah): return TW, s.height
    def draw(s):
        c = s.canv; st = 0.27 * inch; R = RAD * st
        def isl(x, y, n):
            c.setStrokeColor(INK); c.setLineWidth(0.8); c.setFillColor(colors.white); c.circle(x, y, R, stroke=1, fill=1)
            c.setFillColor(INK); c.setFont("Plex-M", R * 1.18); c.drawCentredString(x, y - R * 0.41, str(n))
        def cross(x, y):
            c.setStrokeColor(INK); c.setLineWidth(1.3); d = 3.6
            c.line(x - d, y - d, x + d, y + d); c.line(x - d, y + d, x + d, y - d)
        yc = s.height - 0.42 * inch; cap = 2
        cols = [TW * 0.17, TW * 0.5, TW * 0.83]
        # 1: single and double
        x = cols[0] - 1.5 * st
        c.setStrokeColor(INK); c.setLineWidth(1.2)
        c.line(x, yc, x + 1.5 * st, yc)
        c.line(x + 1.5 * st, yc + 0.1 * st, x + 3 * st, yc + 0.1 * st); c.line(x + 1.5 * st, yc - 0.1 * st, x + 3 * st, yc - 0.1 * st)
        isl(x, yc, 1); isl(x + 1.5 * st, yc, 3); isl(x + 3 * st, yc, 2)
        c.setFont("Crimson-I", 9); c.setFillColor(MID); c.drawCentredString(cols[0], cap, "One or two bridges: yes")
        # 2: crossing
        x = cols[1]; c.setStrokeColor(INK); c.setLineWidth(1.2)
        c.line(x - 1.4 * st, yc, x + 1.4 * st, yc); c.line(x, yc + 1.1 * st, x, yc - 1.1 * st)
        isl(x - 1.4 * st, yc, 1); isl(x + 1.4 * st, yc, 1); isl(x, yc + 1.1 * st, 1); isl(x, yc - 1.1 * st, 1)
        cross(x + 0.42 * st, yc + 0.4 * st)
        c.setFont("Crimson-I", 9); c.setFillColor(MID); c.drawCentredString(cols[1], cap, "Crossing: no")
        # 3: diagonal
        x = cols[2]; c.setStrokeColor(INK); c.setLineWidth(1.2)
        c.line(x - 1.0 * st, yc - 0.8 * st, x + 1.0 * st, yc + 0.8 * st)
        isl(x - 1.0 * st, yc - 0.8 * st, 1); isl(x + 1.0 * st, yc + 0.8 * st, 1); cross(x, yc)
        c.setFont("Crimson-I", 9); c.setFillColor(MID); c.drawCentredString(cols[2], cap, "Diagonal: no")


ILL = os.path.join(HERE, "..", "illustrations")
VIGNETTES = ["v_bridge", "v_skates", "v_ducks", "v_stones", "v_islet", "v_moon"]
def ill(name): return os.path.join(ILL, name + ".png")

def draw_ill(c, name, x, y, w, h):
    """Place a 300 DPI ink illustration (made by illustrations.py) inside the box, keeping its aspect ratio."""
    from reportlab.lib.utils import ImageReader
    img = ImageReader(ill(name)); iw, ih = img.getSize()
    sc = min(w / iw, h / ih); dw, dh = iw * sc, ih * sc
    c.drawImage(ill(name), x + (w - dw) / 2, y + (h - dh) / 2, dw, dh)

class Art(Flowable):
    def __init__(s, name, w, h): s.name = name; s.width = w; s.height = h
    def wrap(s, aw, ah): return s.width, s.height
    def draw(s): draw_ill(s.canv, s.name, 0, 0, s.width, s.height)


B = {tuple(b[:2]): b for b in EX["bridges"]}
EX_PANELS = [[], [B[(5, 6)], B[(2, 6)], B[(1, 2)]], EX["bridges"]]
EX_STEPS = [
    "The <b>2</b> in the bottom row has only one neighbour: the <b>4</b> at the right end of its row (there is no island above it or to its left). Both of its bridges must go there, so draw a double bridge.",
    "The <b>4</b> in the bottom-right corner has only two neighbours and can take at most two bridges from each. It needs four, so it needs two from each: draw a double bridge up to the <b>3</b> in the top-right corner.",
    "That <b>3</b> now has two bridges and needs one more. Its only other neighbour is the <b>5</b>, so draw a single bridge across to it. (This is the middle picture.)",
    "The <b>5</b> has one bridge and needs four more, from its two other neighbours: the <b>3</b> to its left and the <b>3</b> below it. Each can take at most two, so both are double bridges.",
    "The <b>3</b> below the <b>5</b> now needs one more bridge, and its only other neighbour is the <b>2</b> to its left: a single bridge.",
    "The top-left <b>3</b> has two bridges from the <b>5</b> and needs one more, so it goes down to the <b>2</b>. Every island now has its number and all seven are joined in one network.",
]


def build(recto_fix):
    S = []
    def recto(tag):
        S.append(PageBreak())
        if tag in recto_fix: S.extend([Kind("blank"), PageBreak()])
        S.append(Kind(mark=tag))
    S += [Kind("title"), Spacer(1, 2.2 * inch),
          Paragraph("Bridges of<br/>Frostwood", ParagraphStyle("ht", fontName="PlayfairSC-B", fontSize=26, leading=30, alignment=TA_CENTER, textColor=DARK)),
          Spacer(1, 10), Flake(), Spacer(1, 0.5 * inch), Art("v_bridge", TW, 0.85 * inch),
          PageBreak(), Kind("title"), Spacer(1, 0.05 * inch), Art("frontispiece", TW, 7.0 * inch), Spacer(1, 6),
          Paragraph("The footbridge on the lodge pond", ParagraphStyle("fc", parent=small, fontSize=10)),
          PageBreak()]
    S += [Kind("title"), Spacer(1, 0.5 * inch),
          Paragraph("A Frozen-Pond Puzzle Book", ParagraphStyle("t0", parent=kick, fontSize=11, textColor=MID)),
          Spacer(1, 10),
          Paragraph("Bridges of<br/>Frostwood", ParagraphStyle("tt", fontName="PlayfairSC-B", fontSize=38, leading=42, alignment=TA_CENTER, textColor=DARK)),
          Spacer(1, 14),
          Paragraph(f"{NP} Hashi bridges logic puzzles<br/>from the lodge pond to the lake of islands", ParagraphStyle("t2", parent=small, fontSize=13, leading=17)),
          Spacer(1, 0.4 * inch), Art("title", TW, 2.6 * inch), Spacer(1, 0.4 * inch),
          Paragraph("A Frostwood Puzzle Book", ParagraphStyle("t3", parent=kick, fontSize=10, textColor=DARK)),
          Paragraph("Blake La Pierre", ParagraphStyle("t4", parent=small, fontSize=11))]
    S += [PageBreak(), Kind("nofolio"), Spacer(1, 3.6 * inch)]
    cs = ParagraphStyle("cp", parent=body0, fontSize=9, leading=12, alignment=TA_LEFT)
    for t in [f"<i>Bridges of Frostwood: {NP} Hashi Bridges Logic Puzzles</i>",
              "Copyright © 2026 Blake La Pierre. All rights reserved.",
              "No part of this book may be reproduced in any form without written permission from the author, except for brief quotations in reviews. Readers are welcome to photocopy puzzle pages for their own personal use while solving.",
              "Frostwood, its village, lodge, ponds, marsh and lake are imaginary. Any resemblance to real places is coincidental.",
              "First edition, 2026",
              "Set in Crimson Text, Playfair Display SC and IBM Plex Sans Condensed, used under the SIL Open Font License."]:
        S += [Paragraph(t, cs), Spacer(1, 6)]
    recto("contents")
    S += [Kind(section="Contents"), Spacer(1, 0.3 * inch)] + heading("Bridges of Frostwood", "Contents")
    S.append(("TOC",))
    S += [Spacer(1, 0.35 * inch),
          Paragraph("Every winter the ponds, streams and lakes around Frostwood freeze hard, and the village lays little timber footbridges from island to island so everyone can walk out on the ice. "
                    f"This year the plans have blown away in the snow. {NP} maps are left, each showing only the islands and how many bridges each one needs. "
                    "Every puzzle has exactly one solution, and every one can be solved by logic alone, with no guessing.",
                    ParagraphStyle("in", parent=small, fontSize=10.5, leading=14))]
    recto("howto")
    S += [Kind(section="How to Play"), Spacer(1, 0.05 * inch)] + heading("Before You Cross", "How to Play")[:-1] + [Spacer(1, 2)]
    hb = ParagraphStyle("hb", parent=bullet, fontSize=10.3, leading=13.2, spaceAfter=2.2)
    S += [Paragraph("Each puzzle is a map of <b>islands</b>, the circles with numbers. Join them with <b>bridges</b> so that:",
                    ParagraphStyle("hb0", parent=body0, fontSize=10.6, leading=13.8)), Spacer(1, 2)]
    for t in ["Every island has <b>as many bridges as its number</b>.",
              "Bridges run in <b>straight lines</b> across or down the map, never diagonally, and never pass over an island.",
              "Two islands may be joined by <b>one or two bridges</b>, never more.",
              "Bridges <b>never cross</b> each other.",
              "When you are done, <b>all the islands are joined</b> in one network: you can walk from any island to any other."]:
        S.append(Paragraph(FL + t, hb))
    S += [Spacer(1, 3), RuleArt(), Spacer(1, 5),
          Paragraph("<b>Useful Tricks</b>", ParagraphStyle("x", parent=body0, alignment=TA_CENTER, textColor=DARK)), Spacer(1, 2)]
    for t in ["<b>Count the neighbours.</b> An island can take at most two bridges from each neighbour. A <b>4</b> with two neighbours, a <b>6</b> with three or an <b>8</b> with four must have two bridges to every one of them.",
              "<b>One short.</b> A <b>3</b> with two neighbours, a <b>5</b> with three or a <b>7</b> with four must have at least one bridge to each.",
              "<b>Lonely islands.</b> An island with just one neighbour sends all its bridges there.",
              "<b>Keep the network open.</b> Two <b>1</b>s can never be joined to each other, and two <b>2</b>s never by a double bridge: they would make a little group cut off from everything else. The same goes for any finished group. A group with only one way out must use it.",
              "<b>What if?</b> From Part Three on, try a bridge in pencil and follow it until something breaks, then rub it out: you know that bridge is not there."]:
        S.append(Paragraph(FL + t, hb))
    S += [PageBreak(), Kind(section="How to Play"), Spacer(1, 0.05 * inch)] + heading("Let’s Build a Bridge", "A Worked Example")
    S.append(Example(EX_PANELS, 0.26 * inch, ["The puzzle", "After step 3", "Solved"]))
    S.append(Spacer(1, 8))
    S.append(Paragraph("This little 5×5 map has seven islands. Draw single bridges as one line and double bridges as two lines side by side.",
                       ParagraphStyle("exi", parent=body0, fontSize=10.4, leading=13.4, spaceAfter=3)))
    ex = ParagraphStyle("exs", parent=bullet, fontSize=10.3, leading=13.2, spaceAfter=2.4)
    for i, t in enumerate(EX_STEPS, 1):
        S.append(Paragraph(f"<font name='PlayfairSC-B' color='#2b2b2b'>{i}.</font>&nbsp;&nbsp;" + t, ex))
    S.append(Spacer(1, 4))
    S.append(Paragraph("Tick each island lightly as its number is met. Solutions are at the back of the book.", ParagraphStyle("sm2", parent=small, fontSize=9.5)))
    for band in BANDS:
        part, place, k, blurb = PARTS[band]; ps = D[band]
        recto(band)
        S += [Kind("opener"), Kind(section=f"{part} · {place}"), Spacer(1, 0.9 * inch)] + heading(f"{part} · {band} · {ps[0]['w']}×{ps[0]['h']}", place)
        S += [Paragraph(f"Puzzles {ps[0]['num']} to {ps[-1]['num']}", ParagraphStyle("pn", parent=small, fontSize=11)), Spacer(1, 14),
              Paragraph(blurb, ParagraphStyle("bl", parent=small, fontSize=11, leading=15)), Spacer(1, 0.4 * inch),
              Art("opener-" + band.lower(), TW, 2.4 * inch)]
        S.append(PageBreak())
        if band in ("Easy", "Medium"):
            for i in range(0, len(ps), 2):
                S += [PuzzleBlock(ps[i], TH / 2 - 1)]
                if i + 1 < len(ps): S.append(PuzzleBlock(ps[i + 1], TH / 2 - 1))
                S.append(PageBreak())
        else:
            for p in ps: S += [PuzzleBlock(p, TH - 2), PageBreak()]
        S.pop()
    recto("solutions")
    S += [Kind("opener"), Kind(section="Solutions"), Spacer(1, 2.4 * inch)] + heading("The Bridge-Keeper’s Ledger", "Solutions")
    S.append(Paragraph("Each solution shows every bridge in place. Double lines are double bridges.", small))
    for group, (cols, rows) in ((("Easy", "Medium"), (3, 4)), (("Hard",), (2, 3)), (("Expert",), (2, 2))):
        ps = [p for b in group for p in D[b]]
        per = cols * rows; bw = TW / cols; bh = (TH - 4) / rows
        for i in range(0, len(ps), per):
            chunk = ps[i:i + per]
            S += [PageBreak(), Kind(section=f"Solutions · Nos. {chunk[0]['num']}–{chunk[-1]['num']}")]
            grid = []
            for r in range(rows):
                row = []
                for j in range(i + r * cols, i + r * cols + cols):
                    if j < len(ps):
                        q = ps[j]; cell = min((bw - 14) / (q["w"] - 1 + 2 * RAD), (bh - 24) / (q["h"] - 1 + 2 * RAD))
                        row.append(SolutionBlock(q, bw - 6, bh - 4, cell))
                    else: row.append("")
                grid.append(row)
            t = Table(grid, colWidths=[bw] * cols, rowHeights=[bh] * rows)
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Crimson", 10), ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                                   ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            S.append(t)
    recto("about")
    S += [Kind("nofolio"), Spacer(1, 0.55 * inch)] + heading("Thank You for Crossing", "Bridges of Frostwood")
    S.append(Paragraph("If you enjoyed building bridges across the Frostwood ice, a short review helps other puzzlers find the book. "
                       "The bridge-keepers read every one, usually with a mug of cocoa after the last plank is laid.",
                       ParagraphStyle("ty", parent=body0, alignment=TA_CENTER)))
    S += [Spacer(1, 0.25 * inch), Flake(), Spacer(1, 6),
          Paragraph("Also by Blake La Pierre", ParagraphStyle("ab", parent=kick, fontSize=11, textColor=DARK)),
          Paragraph("A Frostwood Puzzle Book", ParagraphStyle("ab0", parent=small, fontSize=9.5)), Spacer(1, 4)]
    for t, d in [("The Thief Stayed the Night", "A snowbound hotel mystery puzzle book. Twelve cozy elimination cases at the Frostwood Lodge."),
                 ("Frostwood Express", "200 Train Tracks logic puzzles. Lay the railway that climbs from the valley to the lodge."),
                 ("Stars over Frostwood", "180 Star Battle logic puzzles. Chart the winter sky from the village green to the lodge observatory."),
                 ("Tents in Frostwood", "180 Tents and Trees logic puzzles. Pitch camp among the pines, from the lodge meadow to the ridge."),
                 ("Riddles by the Frostwood Fire", "140 cozy winter riddles and text logic puzzles, made for reading on a Kindle."),
                 ("The Frostwood Sketchbook", "140 nonogram picture puzzles. Shade the grids to reveal the sketches in the lodge’s winter sketchbook.")]:
        S += [Paragraph(f"<i>{t}</i>", ParagraphStyle("ab2", parent=body0, alignment=TA_CENTER, fontSize=12.5, leading=15)),
              Paragraph(d, ParagraphStyle("ab3", parent=small, fontSize=9.5, leading=12)), Spacer(1, 5)]
    S += [Spacer(1, 0.06 * inch), Art("thanks", TW, 1.15 * inch)]
    S.append(("PAD",))
    return S


def render(recto_fix, out, toc):
    S = build(recto_fix)
    if toc.get("_odd"): S += [PageBreak(), Kind("blank")]
    for i, x in enumerate(S):
        if x == ("PAD",): S[i] = Spacer(0, 0); continue
        if isinstance(x, tuple):
            rows = [("How to Play", toc.get("howto", 0)), ("A Worked Example", toc.get("howto", 0) + 1)]
            for b in BANDS:
                part, place, k, _ = PARTS[b]; ps = D[b]
                rows.append((f"{part} · {place}<br/><font size='9.5' color='#737373'>{b} · {ps[0]['w']}×{ps[0]['h']} · Puzzles {ps[0]['num']}–{ps[-1]['num']}</font>", toc.get(b, 0)))
            rows += [("Solutions", toc.get("solutions", 0))]
            t = Table([[Paragraph(a, ParagraphStyle("tc", parent=body0, fontSize=11.5, leading=14)), str(b)] for a, b in rows], colWidths=[TW - 0.5 * inch, 0.5 * inch])
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Crimson", 11), ("FONT", (1, 0), (1, -1), "Crimson", 11.5), ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), 0.3, FROST), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
            S[i] = t
    fr = Frame(INNER, BOT, TW, TH, id="f", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc = Doc(out, pagesize=(W, H), initialFontName="Crimson", title=f"Bridges of Frostwood: {NP} Hashi Bridges Logic Puzzles", author="Blake La Pierre",
              subject="Hashi (Hashiwokakero / Bridges) logic puzzle book", pageTemplates=[PageTemplate("normal", [fr], onPageEnd=page_end)])
    doc.pkind = {}; doc.marks = {}; doc.section = ""
    doc.build(S)
    return doc.marks, doc.page


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "../frostwood-07-bridges-of-frostwood-interior.pdf"
    fix = set(); toc = {}
    for it in range(40):
        marks, pages = render(fix, out, toc)
        bad = sorted((p, k) for k, p in marks.items() if p % 2 == 0)
        marks["_odd"] = toc.get("_odd", False) ^ (pages % 2 == 1)
        if not bad and marks == toc: break
        if bad: fix ^= {bad[0][1]}
        toc = marks
    marks.pop("_odd", None)
    print("pages", pages, "marks", marks)
    json.dump(dict(pages=pages, marks=marks), open("../build-info.json", "w"))
