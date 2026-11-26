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
assert EX["clues"] == [[0, 0, 4], [0, 2, 3], [1, 4, 3], [1, 1, 6], [3, 4, 4], [4, 1, 3], [4, 3, 2]], EX["clues"]
assert EX["rects"] == [[0, 0, 4, 1], [0, 1, 1, 3], [0, 4, 3, 1], [1, 1, 2, 3], [3, 1, 1, 4], [4, 0, 1, 3], [4, 3, 1, 2]], EX["rects"]

W, H = 6 * inch, 9 * inch
INNER, OUTER, TOP, BOT = 0.75 * inch, 0.55 * inch, 0.7 * inch, 0.75 * inch
DARK = colors.Color(0.17, 0.17, 0.17); MID = colors.Color(0.45, 0.45, 0.45); FROST = colors.Color(0.62, 0.62, 0.62)
INK = colors.Color(0.1, 0.1, 0.1); XC = colors.Color(0.42, 0.42, 0.42)
TITLE = "The Quilts of Frostwood"
TW = W - INNER - OUTER; TH = H - TOP - BOT

PARTS = {
 "Easy": ("Part One", "The Village Sewing Circle", 1,
          "Seven-by-seven squares, pieced on Tuesday afternoons in the village hall. Every quilt can be finished with the two first rules: a number with only one way left to go, and a square that only one patch can still reach."),
 "Medium": ("Part Two", "The Lodge Bedrooms", 2,
            "Nine-by-nine quilts for the lodge’s guest rooms. Now look at a square and ask which numbers could still reach it, and at a number and ask which squares all of its patches would share."),
 "Hard": ("Part Three", "The Sleeper Carriages", 3,
          "Ten-by-ten blankets for the berths of the Frostwood Express, with bigger patches and longer chains of reasoning. The same two questions, asked again and again, will see you through."),
 "Expert": ("Part Four", "The Mountain Huts", 4,
            "Twelve-by-twelve heirloom quilts from the huts high on the mountain. Each one needs one to three careful what-if steps: pencil in a patch, follow it until something breaks, then rub it out."),
}
PREP = {"Easy": "", "Medium": "", "Hard": "", "Expert": ""}
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



def thimble_icon(c, x, y, s):
    """A tiny thimble with a curl of thread, centred on (x, y)."""
    c.saveState(); c.setStrokeColor(INK); c.setLineWidth(max(0.6, s * 0.06)); c.setLineJoin(1); c.setLineCap(1)
    w0 = s * 0.42; w1 = s * 0.3; h = s * 0.5; yb = y - s * 0.35
    p = c.beginPath(); p.moveTo(x - w0 / 2, yb); p.lineTo(x - w1 / 2, yb + h * 0.8)
    p.curveTo(x - w1 / 2, yb + h * 1.08, x + w1 / 2, yb + h * 1.08, x + w1 / 2, yb + h * 0.8); p.lineTo(x + w0 / 2, yb); p.close()
    c.drawPath(p, stroke=1, fill=0)
    c.line(x - w0 / 2 - s * 0.03, yb, x + w0 / 2 + s * 0.03, yb)
    for k in range(3):
        for j in range(3):
            c.circle(x - w1 * 0.3 + j * w1 * 0.3, yb + h * (0.28 + 0.2 * k), s * 0.018, stroke=1, fill=1)
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



MARGIN = 0.0   # no clues outside the grid


def grid_size(p, s):
    n = p["n"]; return n * s, n * s


TONES = [colors.white, colors.Color(0.88, 0.88, 0.88), colors.Color(0.76, 0.76, 0.76), colors.Color(0.94, 0.94, 0.94)]


def tones(p):
    """Greedy colouring of the patches with 4 pale tones so neighbouring patches differ (solutions only)."""
    n = p["n"]; g = p["sol"]; k = len(p["clues"]); nb = [set() for _ in range(k)]
    for r in range(n):
        for c in range(n):
            for dr, dc in ((0, 1), (1, 0)):
                rr, cc = r + dr, c + dc
                if rr < n and cc < n and g[rr][cc] != g[r][c]: nb[g[r][c]].add(g[rr][cc]); nb[g[rr][cc]].add(g[r][c])
    order = sorted(range(k), key=lambda i: -len(nb[i])); col = {}
    def bt(x):                     # 4-colouring by backtracking (patch maps are planar, so one exists)
        if x == k: return True
        i = order[x]
        for t in (1, 0, 2, 3):
            if all(col.get(j) != t for j in nb[i]):
                col[i] = t
                if bt(x + 1): return True
                del col[i]
        return False
    assert bt(0)
    return col


def draw_quilt(c, x0, ytop, s, p, show=None, fs=None):
    """(x0, ytop) = top-left corner of the grid. show = set of patch indexes to draw (outlined and toned)."""
    n = p["n"]
    X = lambda cc: x0 + cc * s; Y = lambda rr: ytop - rr * s
    c.saveState(); c.setLineCap(1); c.setLineJoin(1)
    if show:
        tn = tones(p)
        for i in show:
            r0, c0, h, w = p["rects"][i]
            c.setFillColor(TONES[tn[i]]); c.rect(X(c0), Y(r0 + h), w * s, h * s, stroke=0, fill=1)
    # thin stitched grid lines (dotted like stitching)
    c.setStrokeColor(MID); c.setLineWidth(max(0.35, s * 0.012)); c.setDash(max(1.0, s * 0.06), max(1.2, s * 0.07))
    for i in range(1, n):
        c.line(X(i), Y(0), X(i), Y(n)); c.line(X(0), Y(i), X(n), Y(i))
    c.setDash()
    if show:
        c.setStrokeColor(INK); c.setLineWidth(max(1.1, s * 0.07))
        for i in show:
            r0, c0, h, w = p["rects"][i]
            c.rect(X(c0), Y(r0 + h), w * s, h * s, stroke=1, fill=0)
    c.setStrokeColor(INK); c.setLineWidth(max(1.0, s * 0.05)); c.rect(X(0), Y(n), n * s, n * s, stroke=1, fill=0)
    fs = fs or s * 0.52
    c.setFont("Plex-M", fs); c.setFillColor(INK)
    for r, cc, a in p["clues"]:
        c.drawCentredString(X(cc) + s / 2, Y(r) - s / 2 - fs * 0.35, str(a))
    c.restoreState()


def rating(c, x, y, k, r=4.2, gap=11):
    for i in range(4):
        snowflake(c, x - (3 - i) * gap, y, r, DARK if i < k else colors.Color(.78, .78, .78), lw=0.12)



STEP = {"Easy": 0.42 * inch, "Medium": 0.35 * inch, "Hard": 0.315 * inch, "Expert": 0.37 * inch}



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
        draw_quilt(c, (TW - gw) / 2, gtop, cs, p)
        if full:
            free_lo, free_hi = foot, gtop - gh - 6
            vh = min(0.85 * inch, free_hi - free_lo - 6)
            if vh >= 0.5 * inch:
                draw_ill(c, VIGNETTES[p["num"] % len(VIGNETTES)], 0, free_lo + (free_hi - free_lo - vh) / 2, TW, vh)
            yb = 6; c.setStrokeColor(FROST); c.setLineWidth(0.5); c.line(0, yb + 16, TW, yb + 16)
            c.setFont("PlayfairSC", 8.5); c.setFillColor(MID)
            c.drawString(0, yb, "Started"); c.line(40, yb - 1, 120, yb - 1)
            c.drawString(146, yb, "Finished"); c.line(190, yb - 1, 250, yb - 1)
            c.drawRightString(TW - 22, yb, f"{len(p['clues'])} patches"); thimble_icon(c, TW - 9, yb + 3, 14)


class SolutionBlock(Flowable):
    def __init__(s, p, w, h, cell): s.p = p; s.width = w; s.height = h; s.cell = cell
    def wrap(s, aw, ah): return s.width, s.height
    def draw(s):
        c = s.canv; p = s.p; cs = s.cell
        gw, gh = grid_size(p, cs)
        c.setFont("PlayfairSC-B", 10); c.setFillColor(DARK); c.drawString(0, s.height - 10, f"No. {p['num']}")
        draw_quilt(c, (s.width - gw) / 2, s.height - 14, cs, p, show=range(len(p["clues"])), fs=max(4.6, cs * 0.5))



# partway picture: after step 3 (the 4s and the climbing column)
EX_PART = {0, 1, 2}


class Example(Flowable):
    def __init__(s, panels, cell, cap):
        s.panels = panels; s.cell = cell; s.cap = cap; s.width = TW
        s.height = grid_size(EX, cell)[1] + 20
    def wrap(s, aw, ah): return TW, s.height
    def draw(s):
        c = s.canv; cs = s.cell; k = len(s.panels)
        gw, gh = grid_size(EX, cs)
        gap = (TW - k * gw - 24) / max(k - 1, 1); x = 12
        for i, cells in enumerate(s.panels):
            c.setStrokeColor(FROST); c.setLineWidth(0.5); c.roundRect(x - 6, 13, gw + 12, gh + 6, 4, stroke=1, fill=0)
            draw_quilt(c, x, s.height - 3, cs, EX, show=cells)
            c.setFont("Crimson-I", 9); c.setFillColor(MID); c.drawCentredString(x + gw / 2, 2, s.cap[i])
            x += gw + gap


class RuleArt(Flowable):
    """The three ways to shape a patch of 4 inside a small grid, outlined and toned."""
    def __init__(s): s.width = TW; s.height = 0.98 * inch
    def wrap(s, aw, ah): return TW, s.height
    def draw(s):
        c = s.canv; st = 0.19 * inch
        def mini(cx, rect, cap):
            n = 4; x0 = cx - n * st / 2; ytop = s.height - 4
            q = dict(n=n, clues=[[1, 1, 4]], rects=[rect], sol=None)
            r0, c0, h, w = rect
            c.saveState(); c.setFillColor(TONES[1]); c.rect(x0 + c0 * st, ytop - (r0 + h) * st, w * st, h * st, stroke=0, fill=1)
            c.setStrokeColor(MID); c.setLineWidth(0.4); c.setDash(1.0, 1.2)
            for i in range(1, n):
                c.line(x0 + i * st, ytop, x0 + i * st, ytop - n * st); c.line(x0, ytop - i * st, x0 + n * st, ytop - i * st)
            c.setDash(); c.setStrokeColor(INK); c.setLineWidth(1.3); c.rect(x0 + c0 * st, ytop - (r0 + h) * st, w * st, h * st, stroke=1, fill=0)
            c.setLineWidth(0.9); c.rect(x0, ytop - n * st, n * st, n * st, stroke=1, fill=0)
            c.setFont("Plex-M", 9.5); c.setFillColor(INK); c.drawCentredString(x0 + 1.5 * st, ytop - 1.5 * st - 3.2, "4")
            c.setFont("Crimson-I", 9); c.setFillColor(MID); c.drawCentredString(cx, 2, cap)
            c.restoreState()
        cols = [TW * 0.17, TW * 0.5, TW * 0.83]
        mini(cols[0], [1, 0, 1, 4], "a strip, 1 by 4")
        mini(cols[1], [0, 0, 2, 2], "a square, 2 by 2")
        mini(cols[2], [0, 1, 4, 1], "a column, 4 by 1")

ILL = os.path.join(HERE, "..", "illustrations")
VIGNETTES = ["v_line", "v_basket", "v_chair", "v_bed", "v_mug", "v_frame"]
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


EX_PANELS = [set(), EX_PART, set(range(len(EX["clues"])))]
EX_STEPS = [
    "Start with the <b>4</b> in the top-left corner. Going right, its patch would swallow the 3, so it must run straight down the first column: four squares.",
    "Look at the second square of the top row. The corner 4 is used up and the 6 sits lower down, so only the top <b>3</b> can reach it. That 3 takes the second, third and fourth squares of the top row.",
    "Now the top-right corner can only be reached by the <b>3</b> on the right edge, so that 3 runs down the last column, rows one to three. (This is the middle picture.)",
    "The bottom-left corner can only be reached by the <b>3</b> in the bottom row, so it takes the first three squares of that row. Then the bottom-right corner can only belong to the <b>2</b>: the last two squares.",
    "The <b>4</b> on the right edge could make a 2 by 2 block, but that would overlap the 3 above it, so it lies flat along the fourth row, from the second square to the edge.",
    "What is left is a 2 by 3 block in the middle, rows two and three, columns two to four, and it holds the <b>6</b>. Every square is in exactly one patch, and the quilt is done.",
]

def build(recto_fix):
    S = []
    def recto(tag):
        S.append(PageBreak())
        if tag in recto_fix: S.extend([Kind("blank"), PageBreak()])
        S.append(Kind(mark=tag))
    S += [Kind("title"), Spacer(1, 2.2 * inch),
          Paragraph("The Quilts of<br/>Frostwood", ParagraphStyle("ht", fontName="PlayfairSC-B", fontSize=26, leading=30, alignment=TA_CENTER, textColor=DARK)),
          Spacer(1, 10), Flake(), Spacer(1, 0.5 * inch), Art("v_line", TW, 0.85 * inch),
          PageBreak(), Kind("title"), Spacer(1, 0.05 * inch), Art("frontispiece", TW, 7.0 * inch), Spacer(1, 6),
          Paragraph("The lodge sitting room on a snowy evening, quilts at the ready", ParagraphStyle("fc", parent=small, fontSize=10)),
          PageBreak()]
    S += [Kind("title"), Spacer(1, 0.5 * inch),
          Paragraph("A Winter Patchwork Puzzle Book", ParagraphStyle("t0", parent=kick, fontSize=11, textColor=MID)),
          Spacer(1, 10),
          Paragraph("The Quilts of<br/>Frostwood", ParagraphStyle("tt", fontName="PlayfairSC-B", fontSize=38, leading=42, alignment=TA_CENTER, textColor=DARK)),
          Spacer(1, 14),
          Paragraph(f"{NP} Shikaku logic puzzles<br/>from the village sewing circle to the mountain huts", ParagraphStyle("t2", parent=small, fontSize=13, leading=17)),
          Spacer(1, 0.4 * inch), Art("title", TW, 2.6 * inch), Spacer(1, 0.4 * inch),
          Paragraph("A Frostwood Puzzle Book", ParagraphStyle("t3", parent=kick, fontSize=10, textColor=DARK)),
          Paragraph("Blake La Pierre", ParagraphStyle("t4", parent=small, fontSize=11))]
    S += [PageBreak(), Kind("nofolio"), Spacer(1, 3.6 * inch)]
    cs = ParagraphStyle("cp", parent=body0, fontSize=9, leading=12, alignment=TA_LEFT)
    for t in [f"<i>The Quilts of Frostwood: {NP} Shikaku Logic Puzzles</i>",
              "Copyright © 2026 Blake La Pierre. All rights reserved.",
              "No part of this book may be reproduced in any form without written permission from the author, except for brief quotations in reviews. Readers are welcome to photocopy puzzle pages for their own personal use while solving.",
              "Frostwood, its village, lodge, railway and mountain huts are imaginary. Any resemblance to real places is coincidental.",
              "First edition, 2026. Hardcover.",
              "Set in Crimson Text, Playfair Display SC and IBM Plex Sans Condensed, used under the SIL Open Font License."]:
        S += [Paragraph(t, cs), Spacer(1, 6)]
    recto("contents")
    S += [Kind(section="Contents"), Spacer(1, 0.3 * inch)] + heading("The Quilts of Frostwood", "Contents")
    S.append(("TOC",))
    S += [Spacer(1, 0.35 * inch),
          Paragraph("When the snow settles in, Frostwood sews. The sewing circle meets in the village hall, the lodge keepers piece new quilts for every guest room, the railway stitches blankets for the sleeper berths, and up in the mountain huts the old heirloom quilts are pieced again by lamplight. "
                    f"Each pattern is pinned up with only a few numbers chalked on its squares. Those chalk marks are all that is left of {NP} quilt patterns. "
                    "Every puzzle has exactly one solution, and every one can be solved by logic alone, with no guessing.",
                    ParagraphStyle("in", parent=small, fontSize=10.5, leading=14))]
    recto("howto")
    S += [Kind(section="How to Play"), Spacer(1, 0.05 * inch)] + heading("Before You Start Stitching", "How to Play")[:-1] + [Spacer(1, 2)]
    hb = ParagraphStyle("hb", parent=bullet, fontSize=10.3, leading=13.2, spaceAfter=2.2)
    S += [Paragraph("Each puzzle is a square quilt pattern, with numbers chalked on some of its squares. Draw lines along the stitching to cut the whole quilt into <b>patches</b> so that:",
                    ParagraphStyle("hb0", parent=body0, fontSize=10.6, leading=13.8)), Spacer(1, 2)]
    for t in ["Every patch is a <b>rectangle</b> (a square counts too), cut along the grid lines.",
              "Every patch holds <b>exactly one number</b>, and that number is the patch’s <b>size</b>: how many squares it covers.",
              "Every square of the quilt belongs to <b>exactly one</b> patch. Nothing is left over and nothing overlaps.",
              "This puzzle is also known as <i>Shikaku</i>, <i>Rectangles</i> or <i>Divide by Squares</i>. Every quilt has exactly one answer."]:
        S.append(Paragraph(FL + t, hb))
    S += [Spacer(1, 3), RuleArt(), Spacer(1, 5),
          Paragraph("<b>Useful Tricks</b>", ParagraphStyle("x", parent=body0, alignment=TA_CENTER, textColor=DARK)), Spacer(1, 2)]
    for t in ["<b>Count the shapes.</b> A 4 can be a strip of 4 or a 2 by 2 block; a 5 or a 7 can only be a straight strip; a 6 can be 1 by 6 or 2 by 3, either way round.",
              "<b>Only one way.</b> When a number has only one shape and place left that does not hit another number or a finished patch, draw it.",
              "<b>Lonely squares.</b> Corners and edges are good places to look: when only one number can still reach a square, that square is in its patch.",
              "<b>Shared squares.</b> From Part Two on, if every possible patch for a number covers some square, that square is the number’s, and no other patch may use it.",
              "<b>What if?</b> In Part Four, pencil in one patch and follow it until a number has no room left or a square cannot be reached, then rub it out: that patch is wrong."]:
        S.append(Paragraph(FL + t, hb))
    S += [PageBreak(), Kind(section="How to Play"), Spacer(1, 0.05 * inch)] + heading("Let’s Piece One Quilt", "A Worked Example")
    S.append(Example(EX_PANELS, 0.26 * inch, ["The puzzle", "After step 3", "Solved"]))
    S.append(Spacer(1, 8))
    S.append(Paragraph(f"This little 5×5 quilt has {EX['nclues']} numbers, so it is cut into {EX['nclues']} patches. Rows are counted from the top and columns from the left. Work in pencil.",
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
    S += [Kind("opener"), Kind(section="Solutions"), Spacer(1, 2.4 * inch)] + heading("The Pattern Book", "Solutions")
    S.append(Paragraph("Each solution shows every patch outlined and lightly shaded.", small))
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
    S += [Kind("nofolio"), Spacer(1, 0.1 * inch)] + heading("Thank You for Puzzling", "The Quilts of Frostwood")
    S.append(Paragraph("If you enjoyed piecing the quilts of Frostwood, a short review helps other puzzlers find the book. "
                       "The sewing circle reads every one, usually with a mug of cocoa and a quilt across their knees.",
                       ParagraphStyle("ty", parent=body0, alignment=TA_CENTER)))
    S += [Spacer(1, 0.2 * inch), Flake(), Spacer(1, 4),
          Paragraph("Also by Blake La Pierre", ParagraphStyle("ab", parent=kick, fontSize=11, textColor=DARK)),
          Paragraph("A Frostwood Puzzle Book", ParagraphStyle("ab0", parent=small, fontSize=9.5)), Spacer(1, 3)]
    for t, d in [("The Thief Stayed the Night", "A snowbound hotel mystery puzzle book."),
                 ("Frostwood Express", "200 Train Tracks logic puzzles."),
                 ("Stars over Frostwood", "180 Star Battle logic puzzles."),
                 ("Tents in Frostwood", "180 Tents and Trees logic puzzles."),
                 ("Riddles by the Frostwood Fire", "140 riddles and text logic puzzles for Kindle."),
                 ("The Frostwood Sketchbook", "140 nonogram picture puzzles."),
                 ("Bridges of Frostwood", "180 Hashi bridges logic puzzles."),
                 ("Fences of Frostwood", "100 Slitherlink logic puzzles."),
                 ("The Lockboxes of Frostwood", "120 crack-the-code puzzles for Kindle."),
                 ("Snow Paths of Frostwood", "160 Nurikabe logic puzzles."),
                 ("Chimneys of Frostwood", "100 Skyscrapers logic puzzles."),
                 ("The Fibbers of Frostwood", "120 truth-teller and fibber puzzles for Kindle."),
                 ("The Icicles of Frostwood", "160 Futoshiki logic puzzles."),
                 ("Side by Side in Frostwood", "120 line-up logic puzzles for Kindle.")]:
        S += [Paragraph(f"<i>{t}</i> · <font size='8.5' color='#555555'>{d}</font>", ParagraphStyle("ab2", parent=body0, alignment=TA_CENTER, fontSize=10.5, leading=13.2))]
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
    doc = Doc(out, pagesize=(W, H), initialFontName="Crimson", title=f"The Quilts of Frostwood: {NP} Shikaku Logic Puzzles", author="Blake La Pierre",
              subject="Shikaku (Rectangles / Divide by Squares) logic puzzle book", pageTemplates=[PageTemplate("normal", [fr], onPageEnd=page_end)])
    doc.pkind = {}; doc.marks = {}; doc.section = ""
    doc.build(S)
    return doc.marks, doc.page


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "frostwood-16-the-quilts-of-frostwood-interior.pdf")
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