"""Builds the 6x9 interior PDF (grayscale, no bleed, mirrored margins, embedded fonts) for the
HARDCOVER edition. Same fonts / palette / page furniture as the other Frostwood Puzzle Books."""
import json, sys, math, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
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
# the worked-example text below describes exactly this puzzle
assert EX["clues"] == {"top": [None, 3, 4, 2], "bottom": [None, None, None, None], "left": [1, 3, None, 2], "right": [None, 1, None, None]}, EX["clues"]
assert EX["sol"] == [[4, 2, 1, 3], [1, 3, 2, 4], [2, 4, 3, 1], [3, 1, 4, 2]], EX["sol"]

W, H = 6 * inch, 9 * inch
INNER, OUTER, TOP, BOT = 0.75 * inch, 0.55 * inch, 0.7 * inch, 0.75 * inch
DARK = colors.Color(0.17, 0.17, 0.17); MID = colors.Color(0.45, 0.45, 0.45); FROST = colors.Color(0.62, 0.62, 0.62)
INK = colors.Color(0.1, 0.1, 0.1); XC = colors.Color(0.42, 0.42, 0.42)
TITLE = "Chimneys of Frostwood"
TW = W - INNER - OUTER; TH = H - TOP - BOT

PARTS = {
 "Easy": ("Part One", "The Village Lanes", 1,
          "Five-by-five lanes of cottages. Every puzzle can be finished with the edge rules and simple counting: start with the 1s and the 5s, then make sure each row and column has one chimney of every height."),
 "Medium": ("Part Two", "The Lodge Roofs", 2,
            "Six-by-six rows of lodge roofs and terraces. The edge rules still help, but now you will need to look at a whole lane at once and ask which orders of chimneys could give the clue at each end."),
 "Hard": ("Part Three", "The Station Yard", 3,
          "Seven-by-seven yards of sheds, signal boxes and goods stores, with more heights to place and fewer clues around the edge. Whole-lane thinking does the heavy lifting here."),
 "Expert": ("Part Four", "The Mountain Hamlet", 4,
            "Six-by-six hamlets of huts high on the mountain, with very few clues. Each one needs between one and six careful what-if steps: pencil in a height, follow it until a clue breaks, then rub it out."),
}
PREP = {"Easy": "On ", "Medium": "On ", "Hard": "In ", "Expert": "At "}
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



def chimney_icon(c, x, y, s):
    """A tiny chimney stack with a pot and a curl of smoke, centred on (x, y)."""
    c.saveState(); c.setStrokeColor(INK); c.setLineWidth(max(0.7, s * 0.07)); c.setLineJoin(1); c.setLineCap(1)
    w = s * 0.34; h = s * 0.5
    c.rect(x - w / 2, y - s * 0.45, w, h, stroke=1, fill=0)
    c.line(x - w / 2, y - s * 0.45 + h * 0.5, x + w / 2, y - s * 0.45 + h * 0.5)
    c.rect(x - w / 2 - s * 0.06, y - s * 0.45 + h, w + s * 0.12, s * 0.08, stroke=1, fill=0)
    p = c.beginPath(); p.moveTo(x, y + s * 0.15)
    p.curveTo(x + s * 0.25, y + s * 0.25, x - s * 0.1, y + s * 0.4, x + s * 0.2, y + s * 0.55)
    c.setLineWidth(max(0.5, s * 0.05)); c.drawPath(p, stroke=1, fill=0)
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



MARGIN = 0.62   # clue margin around the grid, in cells


def grid_size(p, s):
    n = p["n"]; return (n + 2 * MARGIN) * s, (n + 2 * MARGIN) * s


def draw_sky(c, x0, ytop, s, p, vals=None, fs=None, clues=True):
    """(x0, ytop) = top-left corner of the whole block, clue margin included. vals[r][c] = height or None."""
    n = p["n"]; m = MARGIN * s
    gx, gy = x0 + m, ytop - m
    X = lambda cc: gx + cc * s; Y = lambda rr: gy - rr * s
    c.saveState(); c.setLineCap(1); c.setLineJoin(1)
    c.setStrokeColor(MID); c.setLineWidth(max(0.4, s * 0.012))
    for i in range(1, n):
        c.line(X(i), Y(0), X(i), Y(n)); c.line(X(0), Y(i), X(n), Y(i))
    c.setStrokeColor(INK); c.setLineWidth(max(0.9, s * 0.035)); c.rect(X(0), Y(n), n * s, n * s, stroke=1, fill=0)
    if clues:
        fs = fs or s * 0.5
        c.setFont("Plex-M", fs); c.setFillColor(INK)
        cl = p["clues"]; off = m * 0.5
        for i in range(n):
            if cl["top"][i] is not None: c.drawCentredString(X(i) + s / 2, Y(0) + off - fs * 0.35, str(cl["top"][i]))
            if cl["bottom"][i] is not None: c.drawCentredString(X(i) + s / 2, Y(n) - off - fs * 0.35, str(cl["bottom"][i]))
            if cl["left"][i] is not None: c.drawCentredString(X(0) - off, Y(i) - s / 2 - fs * 0.35, str(cl["left"][i]))
            if cl["right"][i] is not None: c.drawCentredString(X(n) + off, Y(i) - s / 2 - fs * 0.35, str(cl["right"][i]))
    if vals:
        vf = s * 0.6
        c.setFont("Crimson-SB", vf); c.setFillColor(INK)
        for r in range(n):
            for cc in range(n):
                v = vals[r][cc]
                if v is not None: c.drawCentredString(X(cc) + s / 2, Y(r) - s / 2 - vf * 0.33, str(v))
    c.restoreState()


def rating(c, x, y, k, r=4.2, gap=11):
    for i in range(4):
        snowflake(c, x - (3 - i) * gap, y, r, DARK if i < k else colors.Color(.78, .78, .78), lw=0.12)



STEP = {"Easy": 0.46 * inch, "Medium": 0.42 * inch, "Hard": 0.37 * inch, "Expert": 0.56 * inch}



class PuzzleBlock(Flowable):
    def __init__(s, p, h): s.p = p; s.h = h; s.width = TW; s.height = h
    def wrap(s, aw, ah): return TW, s.h
    def draw(s):
        c = s.canv; p = s.p; cs = STEP[p["band"]]
        gw, gh = grid_size(p, cs)
        full = s.h > TH / 2
        foot = 0.42 * inch if full else 0
        hdr = 0.3 * inch; gap = 0.2 * inch
        block = hdr + gap + gh
        if full: ytop = s.h
        else: ytop = s.h - max(0, (s.h - block) / 2 - 2)
        c.setFillColor(DARK); c.setFont("PlayfairSC-B", 15); c.drawString(0, ytop - 13, f"No. {p['num']}")
        wno = pdfmetrics.stringWidth(f"No. {p['num']}", "PlayfairSC-B", 15)
        c.setFont("Crimson-I", 10.5); c.setFillColor(MID)
        c.drawString(wno + 8, ytop - 13, PREP[p["band"]] + VIEW[p["num"] - 1])
        rating(c, TW - 5, ytop - 9, PARTS[p["band"]][2])
        c.setFont("Plex", 7.5); c.setFillColor(MID)
        c.drawRightString(TW - 50, ytop - 12, f"{p['band'].upper()} · {p['n']}×{p['n']}")
        c.setStrokeColor(FROST); c.setLineWidth(0.5); c.line(0, ytop - 20, TW, ytop - 20)
        gtop = ytop - hdr - gap
        draw_sky(c, (TW - gw) / 2, gtop, cs, p)
        if full:
            free_lo, free_hi = foot, gtop - gh - 6
            vh = min(0.85 * inch, free_hi - free_lo - 6)
            if vh >= 0.5 * inch:
                draw_ill(c, VIGNETTES[p["num"] % len(VIGNETTES)], 0, free_lo + (free_hi - free_lo - vh) / 2, TW, vh)
            yb = 6; c.setStrokeColor(FROST); c.setLineWidth(0.5); c.line(0, yb + 16, TW, yb + 16)
            c.setFont("PlayfairSC", 8.5); c.setFillColor(MID)
            c.drawString(0, yb, "Started"); c.line(40, yb - 1, 120, yb - 1)
            c.drawString(146, yb, "Finished"); c.line(190, yb - 1, 250, yb - 1)
            c.drawRightString(TW - 22, yb, f"Heights 1 to {p['n']}"); chimney_icon(c, TW - 9, yb + 3, 14)


class SolutionBlock(Flowable):
    def __init__(s, p, w, h, cell): s.p = p; s.width = w; s.height = h; s.cell = cell
    def wrap(s, aw, ah): return s.width, s.height
    def draw(s):
        c = s.canv; p = s.p; cs = s.cell
        gw, gh = grid_size(p, cs)
        c.setFont("PlayfairSC-B", 10); c.setFillColor(DARK); c.drawString(0, s.height - 10, f"No. {p['num']}")
        draw_sky(c, (s.width - gw) / 2, s.height - 14, cs, p, vals=p["sol"], fs=max(4.8, cs * 0.46))



# partway picture: after step 3 (the 4s and the climbing column)
EX_PART = {(0, 0), (1, 3), (0, 2), (1, 2), (2, 2), (3, 2), (2, 1)}


class Example(Flowable):
    def __init__(s, panels, cell, cap):
        s.panels = panels; s.cell = cell; s.cap = cap; s.width = TW
        s.height = grid_size(EX, cell)[1] + 22
    def wrap(s, aw, ah): return TW, s.height
    def draw(s):
        c = s.canv; cs = s.cell; k = len(s.panels)
        gw, gh = grid_size(EX, cs)
        gap = (TW - k * gw - 24) / max(k - 1, 1); x = 12
        for i, cells in enumerate(s.panels):
            c.setStrokeColor(FROST); c.setLineWidth(0.5); c.roundRect(x - 6, 13, gw + 12, gh + 6, 4, stroke=1, fill=0)
            vals = [[EX["sol"][r][cc] if (r, cc) in cells else None for cc in range(EX["n"])] for r in range(EX["n"])]
            draw_sky(c, x, s.height - 3, cs, EX, vals=vals)
            c.setFont("Crimson-I", 9); c.setFillColor(MID); c.drawCentredString(x + gw / 2, 2, s.cap[i])
            x += gw + gap


class RuleArt(Flowable):
    """Three one-lane diagrams with chimney bars above the squares: seen chimneys dark, hidden ones pale."""
    def __init__(s): s.width = TW; s.height = 1.2 * inch
    def wrap(s, aw, ah): return TW, s.height
    def draw(s):
        c = s.canv; st = 0.2 * inch
        def lane(cx, clue, hs, cap):
            n = len(hs); x0 = cx - n * st / 2 + st * 0.3; yb = 16
            c.saveState()
            c.setStrokeColor(INK); c.setLineWidth(0.8); c.rect(x0, yb, n * st, st, stroke=1, fill=0)
            for i in range(1, n): c.line(x0 + i * st, yb, x0 + i * st, yb + st)
            c.setFont("Plex-M", 9.5); c.setFillColor(INK); c.drawCentredString(x0 - st * 0.55, yb + st * 0.28, str(clue))
            c.setFont("Crimson-SB", 10)
            top = 0
            for i, h in enumerate(hs):
                c.setFillColor(INK); c.drawCentredString(x0 + (i + 0.5) * st, yb + st * 0.27, str(h))
                seen = h > top; top = max(top, h)
                bh = h * st * 0.42; bx = x0 + i * st + st * 0.3
                c.setFillColor(INK if seen else colors.Color(.85, .85, .85)); c.setStrokeColor(INK if seen else colors.Color(.6, .6, .6)); c.setLineWidth(0.5)
                c.rect(bx, yb + st + 3, st * 0.4, bh, stroke=1, fill=1)
            c.setFont("Crimson-I", 9); c.setFillColor(MID); c.drawCentredString(cx, 2, cap)
            c.restoreState()
        cols = [TW * 0.17, TW * 0.5, TW * 0.83]
        lane(cols[0], 2, [2, 1, 4, 3], "2: the 2 and the 4 are seen")
        lane(cols[1], 1, [4, 2, 3, 1], "1: the tallest is first")
        lane(cols[2], 4, [1, 2, 3, 4], "4: they climb 1, 2, 3, 4")

ILL = os.path.join(HERE, "..", "illustrations")
VIGNETTES = ["v_pots", "v_cottage", "v_sweep", "v_lane", "v_mug", "v_smoke"]
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


EX_PANELS = [set(), EX_PART, {(r, cc) for r in range(4) for cc in range(4)}]
EX_STEPS = [
    "Start with the <b>1</b>s. Seeing only one chimney means the tallest, the 4, stands right beside the clue. So the top row starts with a 4, and the second row ends with one.",
    "Now the <b>4</b> above the third column. Seeing all four chimneys means they must climb 1, 2, 3, 4 going down. Fill that column in.",
    "Every row has exactly one 4. Rows one, two and four already have theirs, in the first, fourth and third columns, so the third row’s 4 must go in the second column. (This is the middle picture.)",
    "Look down the second column from its <b>3</b>. The 4 is third, so both chimneys above it must be seen: the top one is shorter than the one below it. The top row can only use a 2 or a 3 there, so it takes the 2, the second row takes the 3, and the bottom gets the 1. The top row’s last square is then a 3.",
    "The second row is missing only a 1, at its start, and its clue <b>3</b> checks out: you see the 1, the 3 and the 4.",
    "The third row needs a 1 and a 2. The first column already has a 1, so the 2 goes there and the 1 at the end. The bottom row takes the last 3 and 2, and every clue checks out.",
]

def build(recto_fix):
    S = []
    def recto(tag):
        S.append(PageBreak())
        if tag in recto_fix: S.extend([Kind("blank"), PageBreak()])
        S.append(Kind(mark=tag))
    S += [Kind("title"), Spacer(1, 2.2 * inch),
          Paragraph("Chimneys of<br/>Frostwood", ParagraphStyle("ht", fontName="PlayfairSC-B", fontSize=26, leading=30, alignment=TA_CENTER, textColor=DARK)),
          Spacer(1, 10), Flake(), Spacer(1, 0.5 * inch), Art("v_pots", TW, 0.85 * inch),
          PageBreak(), Kind("title"), Spacer(1, 0.05 * inch), Art("frontispiece", TW, 7.0 * inch), Spacer(1, 6),
          Paragraph("Every chimney in the village, on a still winter night", ParagraphStyle("fc", parent=small, fontSize=10)),
          PageBreak()]
    S += [Kind("title"), Spacer(1, 0.5 * inch),
          Paragraph("A Winter Rooftop Puzzle Book", ParagraphStyle("t0", parent=kick, fontSize=11, textColor=MID)),
          Spacer(1, 10),
          Paragraph("Chimneys of<br/>Frostwood", ParagraphStyle("tt", fontName="PlayfairSC-B", fontSize=38, leading=42, alignment=TA_CENTER, textColor=DARK)),
          Spacer(1, 14),
          Paragraph(f"{NP} Skyscrapers logic puzzles<br/>from the village lanes to the mountain hamlet", ParagraphStyle("t2", parent=small, fontSize=13, leading=17)),
          Spacer(1, 0.4 * inch), Art("title", TW, 2.6 * inch), Spacer(1, 0.4 * inch),
          Paragraph("A Frostwood Puzzle Book", ParagraphStyle("t3", parent=kick, fontSize=10, textColor=DARK)),
          Paragraph("Blake La Pierre", ParagraphStyle("t4", parent=small, fontSize=11))]
    S += [PageBreak(), Kind("nofolio"), Spacer(1, 3.6 * inch)]
    cs = ParagraphStyle("cp", parent=body0, fontSize=9, leading=12, alignment=TA_LEFT)
    for t in [f"<i>Chimneys of Frostwood: {NP} Skyscrapers Logic Puzzles</i>",
              "Copyright © 2026 Blake La Pierre. All rights reserved.",
              "No part of this book may be reproduced in any form without written permission from the author, except for brief quotations in reviews. Readers are welcome to photocopy puzzle pages for their own personal use while solving.",
              "Frostwood, its village, lodge, station and mountain hamlet are imaginary. Any resemblance to real places is coincidental.",
              "First edition, 2026. Hardcover.",
              "Set in Crimson Text, Playfair Display SC and IBM Plex Sans Condensed, used under the SIL Open Font License."]:
        S += [Paragraph(t, cs), Spacer(1, 6)]
    recto("contents")
    S += [Kind(section="Contents"), Spacer(1, 0.3 * inch)] + heading("Chimneys of Frostwood", "Contents")
    S.append(("TOC",))
    S += [Spacer(1, 0.35 * inch),
          Paragraph("On a still winter evening every fire in Frostwood is lit, and every chimney sends up its curl of smoke: along the village lanes, over the lodge roofs, in the station yard and up in the mountain hamlet. "
                    f"Before the next big snow, the sweep walks the rounds and notes, at the end of each lane, how many chimneys can be seen from there. Those notes are all that is left of {NP} rooftop maps. "
                    "Every puzzle has exactly one solution, and every one can be solved by logic alone, with no guessing.",
                    ParagraphStyle("in", parent=small, fontSize=10.5, leading=14))]
    recto("howto")
    S += [Kind(section="How to Play"), Spacer(1, 0.05 * inch)] + heading("Before You Walk the Rounds", "How to Play")[:-1] + [Spacer(1, 2)]
    hb = ParagraphStyle("hb", parent=bullet, fontSize=10.3, leading=13.2, spaceAfter=2.2)
    S += [Paragraph("Each puzzle is a square map of rooftops. Every square holds one <b>chimney</b>, with a height from 1 up to the size of the grid. Write a height in every square so that:",
                    ParagraphStyle("hb0", parent=body0, fontSize=10.6, leading=13.8)), Spacer(1, 2)]
    for t in ["Each <b>row</b> and each <b>column</b> (a <b>lane</b>) has every height exactly once, like a Sudoku.",
              "A <b>number outside the grid</b> says how many chimneys you can see looking along that lane from that end.",
              "A taller chimney <b>hides</b> every shorter one behind it, so you see a chimney only if it is taller than all the ones in front of it.",
              "Lanes without a number may show any count. Every puzzle has exactly one answer."]:
        S.append(Paragraph(FL + t, hb))
    S += [Spacer(1, 3), RuleArt(), Spacer(1, 5),
          Paragraph("<b>Useful Tricks</b>", ParagraphStyle("x", parent=body0, alignment=TA_CENTER, textColor=DARK)), Spacer(1, 2)]
    for t in ["<b>A 1.</b> Only one chimney is seen, so the tallest stands right beside the clue.",
              "<b>The biggest clue.</b> When the clue equals the grid size, every chimney is seen: the lane climbs 1, 2, 3 and so on, all the way up.",
              "<b>The edge rule.</b> Next to a clue of <i>k</i> in a grid of size <i>n</i>, a chimney is at most <i>n</i> − <i>k</i> + 1 tall, and that limit grows by one for each square further in. A clue of 3 in a 5×5 grid means at most 3, then 4, then 5.",
              "<b>One of each.</b> When a height has only one possible square left in a lane, it goes there. Pencil small candidate heights in the corners of squares.",
              "<b>Whole lanes.</b> From Part Two on, list the ways a lane can be filled that fit its clues and the heights already placed, and keep only what they all agree on.",
              "<b>What if?</b> In Part Four, pencil in one height and follow it until a clue or a lane breaks, then rub it out: that height is wrong."]:
        S.append(Paragraph(FL + t, hb))
    S += [PageBreak(), Kind(section="How to Play"), Spacer(1, 0.05 * inch)] + heading("Let’s Walk One Map", "A Worked Example")
    S.append(Example(EX_PANELS, 0.235 * inch, ["The puzzle", "After step 3", "Solved"]))
    S.append(Spacer(1, 8))
    S.append(Paragraph(f"This little 4×4 map has {EX['nclues']} clues and uses the heights 1 to 4. Work in pencil.",
                       ParagraphStyle("exi", parent=body0, fontSize=10.4, leading=13.4, spaceAfter=3)))
    ex = ParagraphStyle("exs", parent=bullet, fontSize=10.1, leading=12.9, spaceAfter=2.2)
    for i, t in enumerate(EX_STEPS, 1):
        S.append(Paragraph(f"<font name='PlayfairSC-B' color='#2b2b2b'>{i}.</font>&nbsp;&nbsp;" + t, ex))
    S.append(Spacer(1, 4))
    S.append(Paragraph("Solutions are at the back of the book.", ParagraphStyle("sm2", parent=small, fontSize=9.5)))
    for band in BANDS:
        part, place, k, blurb = PARTS[band]; ps = D[band]
        recto(band)
        S += [Kind("opener"), Kind(section=f"{part} · {place}"), Spacer(1, 0.9 * inch)] + heading(f"{part} · {band} · {ps[0]['n']}×{ps[0]['n']}", place)
        S += [Paragraph(f"Puzzles {ps[0]['num']} to {ps[-1]['num']}", ParagraphStyle("pn", parent=small, fontSize=11)), Spacer(1, 14),
              Paragraph(blurb, ParagraphStyle("bl", parent=small, fontSize=11, leading=15)), Spacer(1, 0.4 * inch),
              Art("opener-" + band.lower(), TW, 2.4 * inch)]
        S.append(PageBreak())
        if band in ("Easy", "Medium", "Hard"):
            for i in range(0, len(ps), 2):
                S += [PuzzleBlock(ps[i], TH / 2 - 1)]
                if i + 1 < len(ps): S.append(PuzzleBlock(ps[i + 1], TH / 2 - 1))
                S.append(PageBreak())
        else:
            for p in ps: S += [PuzzleBlock(p, TH - 2), PageBreak()]
        S.pop()
    recto("solutions")
    S += [Kind("opener"), Kind(section="Solutions"), Spacer(1, 2.4 * inch)] + heading("The Sweep’s Notebook", "Solutions")
    S.append(Paragraph("Each solution shows every chimney’s height.", small))
    for group, (cols, rows) in ((("Easy", "Medium", "Hard"), (3, 4)), (("Expert",), (2, 3))):
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
                        q = ps[j]; cell = min((bw - 10) / (q["n"] + 2 * MARGIN), (bh - 20) / (q["n"] + 2 * MARGIN))
                        row.append(SolutionBlock(q, bw - 6, bh - 4, cell))
                    else: row.append("")
                grid.append(row)
            t = Table(grid, colWidths=[bw] * cols, rowHeights=[bh] * rows)
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Crimson", 10), ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                                   ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            S.append(t)
    recto("about")
    S += [Kind("nofolio"), Spacer(1, 0.1 * inch)] + heading("Thank You for Walking the Rounds", "Chimneys of Frostwood")
    S.append(Paragraph("If you enjoyed counting the chimneys of Frostwood, a short review helps other puzzlers find the book. "
                       "The sweep reads every one, usually by the fire with a mug of cocoa once the last lane is done.",
                       ParagraphStyle("ty", parent=body0, alignment=TA_CENTER)))
    S += [Spacer(1, 0.2 * inch), Flake(), Spacer(1, 4),
          Paragraph("Also by Blake La Pierre", ParagraphStyle("ab", parent=kick, fontSize=11, textColor=DARK)),
          Paragraph("A Frostwood Puzzle Book", ParagraphStyle("ab0", parent=small, fontSize=9.5)), Spacer(1, 3)]
    for t, d in [("The Thief Stayed the Night", "A snowbound hotel mystery puzzle book. Twelve cozy elimination cases at the Frostwood Lodge."),
                 ("Frostwood Express", "200 Train Tracks logic puzzles. Lay the railway that climbs from the valley to the lodge."),
                 ("Stars over Frostwood", "180 Star Battle logic puzzles. Chart the winter sky from the village green to the lodge observatory."),
                 ("Tents in Frostwood", "180 Tents and Trees logic puzzles. Pitch camp among the pines, from the lodge meadow to the ridge."),
                 ("Riddles by the Frostwood Fire", "140 cozy winter riddles and text logic puzzles, made for reading on a Kindle."),
                 ("The Frostwood Sketchbook", "140 nonogram picture puzzles. Shade the grids to reveal the sketches in the lodge’s winter sketchbook."),
                 ("Bridges of Frostwood", "180 Hashi bridges puzzles. Lay the footbridges across the frozen ponds and the lake of islands."),
                 ("Fences of Frostwood", "100 Slitherlink puzzles. Trace the snowed-under fences from the village lots to the high orchard."),
                 ("The Lockboxes of Frostwood", "120 crack-the-code puzzles. Open the lodge keepers’ winter lockboxes, made for reading on a Kindle.")]:
        S += [Paragraph(f"<i>{t}</i>", ParagraphStyle("ab2", parent=body0, alignment=TA_CENTER, fontSize=12, leading=14.4)),
              Paragraph(d, ParagraphStyle("ab3", parent=small, fontSize=9.0, leading=11)), Spacer(1, 2)]
    S += [Spacer(1, 0.02 * inch), Art("thanks", TW, 0.85 * inch)]
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
                rows.append((f"{part} · {place}<br/><font size='9.5' color='#737373'>{b} · {ps[0]['n']}×{ps[0]['n']} · Puzzles {ps[0]['num']}–{ps[-1]['num']}</font>", toc.get(b, 0)))
            rows += [("Solutions", toc.get("solutions", 0))]
            t = Table([[Paragraph(a, ParagraphStyle("tc", parent=body0, fontSize=11.5, leading=14)), str(b)] for a, b in rows], colWidths=[TW - 0.5 * inch, 0.5 * inch])
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Crimson", 11), ("FONT", (1, 0), (1, -1), "Crimson", 11.5), ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), 0.3, FROST), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
            S[i] = t
    fr = Frame(INNER, BOT, TW, TH, id="f", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc = Doc(out, pagesize=(W, H), initialFontName="Crimson", title=f"Chimneys of Frostwood: {NP} Skyscrapers Logic Puzzles", author="Blake La Pierre",
              subject="Skyscrapers (Towers) logic puzzle book", pageTemplates=[PageTemplate("normal", [fr], onPageEnd=page_end)])
    doc.pkind = {}; doc.marks = {}; doc.section = ""
    doc.build(S)
    return doc.marks, doc.page


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "frostwood-11-chimneys-of-frostwood-interior.pdf")
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
    json.dump(dict(pages=pages, marks=marks), open(os.path.join(HERE, "..", "build-info.json"), "w"))