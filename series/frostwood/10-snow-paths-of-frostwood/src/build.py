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
assert EX["clues"] == [[0, 0, 1], [1, 4, 2], [2, 0, 4], [4, 0, 1], [4, 3, 3]], EX["clues"]
assert EX["sol"] == [".####", "##.#.", "...#.", "#####", ".#..."], EX["sol"]

W, H = 6 * inch, 9 * inch
INNER, OUTER, TOP, BOT = 0.75 * inch, 0.55 * inch, 0.7 * inch, 0.75 * inch
DARK = colors.Color(0.17, 0.17, 0.17); MID = colors.Color(0.45, 0.45, 0.45); FROST = colors.Color(0.62, 0.62, 0.62)
INK = colors.Color(0.1, 0.1, 0.1); GRIDC = colors.Color(0.55, 0.55, 0.55); SHADE = colors.Color(0.42, 0.42, 0.42)
TITLE = "Snow Paths of Frostwood"
TW = W - INNER - OUTER; TH = H - TOP - BOT

PARTS = {
 "Easy": ("Part One", "The Lodge Garden", 1,
          "Seven-by-seven corners of the lodge garden. Start with the 1s and the squares squeezed between two numbers, and the path will soon show you where it wants to go."),
 "Medium": ("Part Two", "The Village Lanes", 2,
            "Nine-by-nine maps of the village after a heavy fall. The basic tricks still carry you, but now you will often need to list the few ways a small patch can be finished."),
 "Hard": ("Part Three", "The Station Yard", 3,
          "Ten-by-ten maps of the station yard. Somewhere in each one the direct tricks run out, and a short “what if?” in pencil shows which square must be path."),
 "Expert": ("Part Four", "The High Meadows", 4,
            "Twelve-by-twelve maps of the meadows below the peaks, the largest in the book, each needing several what-if steps. Take your time and keep a soft eraser close."),
}
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


def path_icon(c, x, y, s):
    """A tiny 3x3 map: an L of shaded path and a numbered patch, centred on (x, y)."""
    q = s / 3; x0 = x - s / 2; y0 = y - s / 2
    c.saveState(); c.setLineWidth(0.4); c.setStrokeColor(GRIDC)
    for (r, cc) in [(0, 2), (1, 2), (1, 1), (1, 0), (2, 0)]:
        c.setFillColor(SHADE); c.rect(x0 + cc * q, y0 + (2 - r) * q, q, q, stroke=0, fill=1)
    for i in range(4):
        c.line(x0 + i * q, y0, x0 + i * q, y0 + s); c.line(x0, y0 + i * q, x0 + s, y0 + i * q)
    c.setFillColor(INK); c.setFont("Plex-M", q * 0.8); c.drawCentredString(x0 + q / 2, y0 + 2 * q + q * 0.22, "2")
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


def draw_grid(c, x0, ytop, s, p, shade=None, dots=None, fs=None, lw_out=1.3):
    """(x0, ytop) = top-left corner. shade = set of (r, c) drawn as path; dots = set of (r, c) marked as snow."""
    w, h = p["w"], p["h"]
    c.saveState()
    if shade:
        c.setFillColor(SHADE)
        for (r, cc) in shade: c.rect(x0 + cc * s, ytop - (r + 1) * s, s, s, stroke=0, fill=1)
    c.setStrokeColor(GRIDC); c.setLineWidth(max(0.35, min(0.7, s * 0.02)))
    for i in range(1, w): c.line(x0 + i * s, ytop, x0 + i * s, ytop - h * s)
    for j in range(1, h): c.line(x0, ytop - j * s, x0 + w * s, ytop - j * s)
    c.setStrokeColor(INK); c.setLineWidth(lw_out); c.rect(x0, ytop - h * s, w * s, h * s, stroke=1, fill=0)
    fs = fs or s * 0.56
    c.setFillColor(INK); c.setFont("Plex-M", fs)
    for r, cc, n in p["clues"]:
        c.drawCentredString(x0 + (cc + 0.5) * s, ytop - (r + 0.5) * s - fs * 0.35, str(n))
    if dots:
        for (r, cc) in dots:
            c.circle(x0 + (cc + 0.5) * s, ytop - (r + 0.5) * s, max(0.9, s * 0.07), stroke=0, fill=1)
    c.restoreState()


def rating(c, x, y, k, r=4.2, gap=11):
    for i in range(4):
        snowflake(c, x - (3 - i) * gap, y, r, DARK if i < k else colors.Color(.78, .78, .78), lw=0.12)


STEP = {"Easy": 0.44 * inch, "Medium": 0.335 * inch, "Hard": 0.44 * inch, "Expert": 0.38 * inch}


class PuzzleBlock(Flowable):
    def __init__(s, p, h): s.p = p; s.h = h; s.width = TW; s.height = h
    def wrap(s, aw, ah): return TW, s.h
    def draw(s):
        c = s.canv; p = s.p; cs = STEP[p["band"]]
        gw, gh = p["w"] * cs, p["h"] * cs
        full = s.h > TH / 2
        foot = 0.42 * inch if full else 0
        hdr = 0.3 * inch; gap = 0.16 * inch
        block = hdr + gap + gh
        ytop = s.h if full else s.h - max(0, (s.h - block) / 2 - 2)
        c.setFillColor(DARK); c.setFont("PlayfairSC-B", 15); c.drawString(0, ytop - 13, f"No. {p['num']}")
        wno = pdfmetrics.stringWidth(f"No. {p['num']}", "PlayfairSC-B", 15)
        c.setFont("Crimson-I", 10.5); c.setFillColor(MID)
        c.drawString(wno + 8, ytop - 13, VIEW[p["num"] - 1][0].upper() + VIEW[p["num"] - 1][1:])
        rating(c, TW - 5, ytop - 9, PARTS[p["band"]][2])
        c.setFont("Plex", 7.5); c.setFillColor(MID)
        c.drawRightString(TW - 50, ytop - 12, f"{p['band'].upper()} · {p['w']}×{p['h']}")
        c.setStrokeColor(FROST); c.setLineWidth(0.5); c.line(0, ytop - 20, TW, ytop - 20)
        gtop = ytop - hdr - gap
        draw_grid(c, (TW - gw) / 2, gtop, cs, p)
        if full:
            free_lo, free_hi = foot, gtop - gh - 6
            vh = min(0.85 * inch, free_hi - free_lo - 6)
            if vh >= 0.5 * inch:
                draw_ill(c, VIGNETTES[p["num"] % len(VIGNETTES)], 0, free_lo + (free_hi - free_lo - vh) / 2, TW, vh)
            yb = 6; c.setStrokeColor(FROST); c.setLineWidth(0.5); c.line(0, yb + 16, TW, yb + 16)
            c.setFont("PlayfairSC", 8.5); c.setFillColor(MID)
            c.drawString(0, yb, "Started"); c.line(40, yb - 1, 120, yb - 1)
            c.drawString(146, yb, "Finished"); c.line(190, yb - 1, 270, yb - 1)
            c.drawRightString(TW - 22, yb, "Path dug"); path_icon(c, TW - 8, yb + 3, 13)


def shade_of(p, sol=None):
    sol = sol or p["sol"]
    return {(r, c) for r in range(p["h"]) for c in range(p["w"]) if sol[r][c] == "#"}


class SolutionBlock(Flowable):
    def __init__(s, p, w, h, cell): s.p = p; s.width = w; s.height = h; s.cell = cell
    def wrap(s, aw, ah): return s.width, s.height
    def draw(s):
        c = s.canv; p = s.p; cs = s.cell
        gw = p["w"] * cs
        c.setFont("PlayfairSC-B", 10); c.setFillColor(DARK); c.drawString(0, s.height - 10, f"No. {p['num']}")
        draw_grid(c, (s.width - gw) / 2, s.height - 15, cs, p, shade=shade_of(p), fs=max(4.8, cs * 0.6), lw_out=0.9)


# worked example: 1-based rows/columns in the text
def rc(cells): return {(r - 1, c - 1) for r, c in cells}
EX_STEP4_SHADE = rc([(1, 2), (2, 1), (4, 1), (5, 2), (1, 3), (1, 4), (2, 2), (4, 2)])
EX_STEP4_DOTS = rc([(3, 2)])


class Example(Flowable):
    def __init__(s, panels, cell, cap):
        s.panels = panels; s.cell = cell; s.cap = cap; s.width = TW
        s.height = EX["h"] * cell + 24
    def wrap(s, aw, ah): return TW, s.height
    def draw(s):
        c = s.canv; cs = s.cell; k = len(s.panels)
        gw = EX["w"] * cs
        gap = (TW - k * gw - 16) / max(k - 1, 1); x = 8
        for i, (sh, dt) in enumerate(s.panels):
            draw_grid(c, x, s.height - 4, cs, EX, shade=sh, dots=dt, lw_out=1.0)
            c.setFont("Crimson-I", 9); c.setFillColor(MID); c.drawCentredString(x + gw / 2, 2, s.cap[i])
            x += gw + gap


class RuleArt(Flowable):
    """Three tiny maps: a finished map (yes), a 2x2 block of path (no), a path in two pieces (no)."""
    def __init__(s): s.width = TW; s.height = 0.98 * inch
    def wrap(s, aw, ah): return TW, s.height
    def draw(s):
        c = s.canv; st = 0.24 * inch
        def cross(x, y):
            c.setStrokeColor(INK); c.setLineWidth(1.6); d = 4.2
            c.line(x - d, y - d, x + d, y + d); c.line(x - d, y + d, x + d, y - d)
        maps = [
            (dict(w=3, h=3, clues=[[0, 0, 3], [2, 2, 1]]), ["..#", ".##", "##."], "A finished map: yes", None),
            (dict(w=3, h=3, clues=[[2, 2, 5]]), ["##.", "##.", "..."], "A 2×2 of path: no", (0, 0)),
            (dict(w=3, h=3, clues=[[1, 1, 3]]), ["#.#", "#.#", "#.#"], "Path in two pieces: no", None),
        ]
        cols = [TW * 0.17, TW * 0.5, TW * 0.83]
        for (p, sol, cap, _), cx in zip(maps, cols):
            x0 = cx - 1.5 * st; ytop = s.height - 2
            draw_grid(c, x0, ytop, st, p, shade=shade_of(p, sol), lw_out=0.9)
            c.setFont("Crimson-I", 9); c.setFillColor(MID); c.drawCentredString(cx, 2, cap)
        cross(cols[1] - 0.5 * st, s.height - 2 - st)          # the 2x2 block
        cross(cols[2], s.height - 2 - 0.5 * st)                # the split


ILL = os.path.join(HERE, "..", "illustrations")
VIGNETTES = ["v_shovel", "v_sled", "v_lantern", "v_mug", "v_snowman"]
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


EX_STEPS = [
    "Each <b>1</b> is a finished patch on its own, so shade the squares beside them: right of and below the top <b>1</b>, above and right of the bottom <b>1</b>.",
    "The third and fourth squares of the top row are out of reach. The <b>4</b> can add only three more squares and the <b>2</b> only one, and neither could get that far. Shade them.",
    "The <b>4</b> now has path above and below it, so it must grow to the right: mark the square beside it as snow with a dot.",
    "The shaded square under the top <b>1</b> is boxed in on three sides, and the path must stay in one piece, so the square to its right is path. The same goes for the square above the bottom <b>1</b>. (This is the middle picture.)",
    "At the top, three squares of a 2×2 block are now path, so row 2, column 3 is snow. The square to its right is path (the <b>2</b> would get too big), so that snow must join the <b>4</b> through the square below it. The <b>4</b> is finished: shade around it.",
    "At the bottom left, three squares of a 2×2 block are path, so the square left of the <b>3</b> is snow and part of the <b>3</b>.",
    "Row 4, column 5 is out of reach, so shade it. The long run of path in row 4 can only get out through column 4, so shade that too. Now a 2×2 on the right has three path squares, so row 3, column 5 is snow: the <b>2</b> is finished, the top-right corner is path, and the last square completes the <b>3</b>.",
]


def build(recto_fix):
    S = []
    def recto(tag):
        S.append(PageBreak())
        if tag in recto_fix: S.extend([Kind("blank"), PageBreak()])
        S.append(Kind(mark=tag))
    S += [Kind("title"), Spacer(1, 2.2 * inch),
          Paragraph("Snow Paths of<br/>Frostwood", ParagraphStyle("ht", fontName="PlayfairSC-B", fontSize=26, leading=30, alignment=TA_CENTER, textColor=DARK)),
          Spacer(1, 10), Flake(), Spacer(1, 0.5 * inch), Art("v_shovel", TW, 0.85 * inch),
          PageBreak(), Kind("title"), Spacer(1, 0.05 * inch), Art("frontispiece", TW, 7.0 * inch), Spacer(1, 6),
          Paragraph("The first paths of the morning, from the lodge door", ParagraphStyle("fc", parent=small, fontSize=10)),
          PageBreak()]
    S += [Kind("title"), Spacer(1, 0.5 * inch),
          Paragraph("A Snowed-In Puzzle Book", ParagraphStyle("t0", parent=kick, fontSize=11, textColor=MID)),
          Spacer(1, 10),
          Paragraph("Snow Paths of<br/>Frostwood", ParagraphStyle("tt", fontName="PlayfairSC-B", fontSize=38, leading=42, alignment=TA_CENTER, textColor=DARK)),
          Spacer(1, 14),
          Paragraph(f"{NP} Nurikabe logic puzzles<br/>from the lodge garden to the high meadows", ParagraphStyle("t2", parent=small, fontSize=13, leading=17)),
          Spacer(1, 0.4 * inch), Art("title", TW, 2.6 * inch), Spacer(1, 0.4 * inch),
          Paragraph("A Frostwood Puzzle Book", ParagraphStyle("t3", parent=kick, fontSize=10, textColor=DARK)),
          Paragraph("Blake La Pierre", ParagraphStyle("t4", parent=small, fontSize=11))]
    S += [PageBreak(), Kind("nofolio"), Spacer(1, 3.6 * inch)]
    cs = ParagraphStyle("cp", parent=body0, fontSize=9, leading=12, alignment=TA_LEFT)
    for t in [f"<i>Snow Paths of Frostwood: {NP} Nurikabe Logic Puzzles</i>",
              "Copyright © 2026 Blake La Pierre. All rights reserved.",
              "No part of this book may be reproduced in any form without written permission from the author, except for brief quotations in reviews. Readers are welcome to photocopy puzzle pages for their own personal use while solving.",
              "Frostwood, its lodge, village, station and meadows are imaginary. Any resemblance to real places is coincidental.",
              "First edition, 2026",
              "Set in Crimson Text, Playfair Display SC and IBM Plex Sans Condensed, used under the SIL Open Font License."]:
        S += [Paragraph(t, cs), Spacer(1, 6)]
    recto("contents")
    S += [Kind(section="Contents"), Spacer(1, 0.3 * inch)] + heading("Snow Paths of Frostwood", "Contents")
    S.append(("TOC",))
    S += [Spacer(1, 0.35 * inch),
          Paragraph("After the deepest snowfall of the winter, Frostwood wakes up snowed in. The lodge keepers and the villagers take up their shovels and dig "
                    "one long path that links every corner, leaving neat patches of untouched snow in between, each marked with a little numbered stake. "
                    f"{NP} maps of the digging are left, showing only the stakes. Every puzzle has exactly one solution, and every one can be solved by logic alone, with no guessing.",
                    ParagraphStyle("in", parent=small, fontSize=10.5, leading=14))]
    recto("howto")
    S += [Kind(section="How to Play"), Spacer(1, 0.05 * inch)] + heading("Before You Dig", "How to Play")[:-1] + [Spacer(1, 2)]
    hb = ParagraphStyle("hb", parent=bullet, fontSize=10.2, leading=13.0, spaceAfter=2.0)
    S += [Paragraph("Each puzzle is a snowed-in map. <b>Shade</b> squares to dig the path, and leave the others as <b>snow</b>, so that:",
                    ParagraphStyle("hb0", parent=body0, fontSize=10.6, leading=13.8)), Spacer(1, 2)]
    for t in ["Every number sits in a <b>snow patch of exactly that many squares</b> (its own square counts).",
              "Each snow patch holds <b>exactly one number</b>. Two patches may touch at a corner, never side by side.",
              "All the shaded squares join up into <b>one path</b>: you can walk from any path square to any other, moving across or down.",
              "The path never makes a <b>2×2 block</b> anywhere on the map.",
              "Numbered squares are always snow. Shade the path, and mark squares you know are snow with a dot."]:
        S.append(Paragraph(FL + t, hb))
    S += [Spacer(1, 3), RuleArt(), Spacer(1, 5),
          Paragraph("<b>Useful Tricks</b>", ParagraphStyle("x", parent=body0, alignment=TA_CENTER, textColor=DARK)), Spacer(1, 2)]
    for t in ["<b>Finished patches.</b> A <b>1</b> is finished on its own. Shade every square beside a finished patch.",
              "<b>Between two numbers.</b> A square touching two different patches must be path, or the patches would join.",
              "<b>Out of reach.</b> A square that no number can reach with the squares it has left is path.",
              "<b>One way out.</b> A patch that still needs squares, or a piece of path cut off from the rest, with only one open square beside it, must grow into that square.",
              "<b>No 2×2.</b> If three squares of a 2×2 block are path, the fourth is snow.",
              "<b>List the ways.</b> From Part Two on, a small patch often has only a few ways to finish. Squares in all of them are snow; squares beside all of them are path.",
              "<b>What if?</b> From Part Three on, shade a square in pencil and follow it until something breaks, then rub it out: that square is snow."]:
        S.append(Paragraph(FL + t, hb))
    S += [PageBreak(), Kind(section="How to Play"), Spacer(1, 0.05 * inch)] + heading("Let’s Dig a Path", "A Worked Example")
    S.append(Example([(set(), set()), (EX_STEP4_SHADE, EX_STEP4_DOTS), (shade_of(EX), set())], 0.27 * inch, ["The puzzle", "After step 4", "Solved"]))
    S.append(Spacer(1, 8))
    S.append(Paragraph("This little 5×5 map has five numbers. Rows count from the top and columns from the left.",
                       ParagraphStyle("exi", parent=body0, fontSize=10.3, leading=13.3, spaceAfter=3)))
    ex = ParagraphStyle("exs", parent=bullet, fontSize=10.1, leading=12.9, spaceAfter=2.2)
    for i, t in enumerate(EX_STEPS, 1):
        S.append(Paragraph(f"<font name='PlayfairSC-B' color='#2b2b2b'>{i}.</font>&nbsp;&nbsp;" + t, ex))
    S.append(Spacer(1, 3))
    S.append(Paragraph("Every patch now has its number of squares, the path is one piece, and there is no 2×2 of path anywhere. Solutions are at the back of the book.", ParagraphStyle("sm2", parent=small, fontSize=9.5)))
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
    S += [Kind("opener"), Kind(section="Solutions"), Spacer(1, 2.4 * inch)] + heading("The Path-Diggers’ Ledger", "Solutions")
    S.append(Paragraph("Each solution shows the finished path shaded in gray. The white squares are the snow patches.", small))
    for group, (cols, rows) in ((("Easy", "Medium"), (3, 4)), (("Hard",), (2, 3)), (("Expert",), (2, 3))):
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
                        q = ps[j]; cell = min((bw - 14) / q["w"], (bh - 22) / q["h"])
                        row.append(SolutionBlock(q, bw - 6, bh - 4, cell))
                    else: row.append("")
                grid.append(row)
            t = Table(grid, colWidths=[bw] * cols, rowHeights=[bh] * rows)
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Crimson", 10), ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                                   ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            S.append(t)
    recto("about")
    S += [Kind("nofolio"), Spacer(1, 0.05 * inch)] + heading("Thank You for Digging In", "Snow Paths of Frostwood")
    S.append(Paragraph("If you enjoyed digging the paths of Frostwood, a short review helps other puzzlers find the book. "
                       "The path-diggers read every one, usually with a mug of cocoa once the shovels are back in the shed.",
                       ParagraphStyle("ty", parent=body0, alignment=TA_CENTER, fontSize=10.8, leading=14)))
    S += [Spacer(1, 0.15 * inch), Flake(), Spacer(1, 4),
          Paragraph("Also by Blake La Pierre", ParagraphStyle("ab", parent=kick, fontSize=11, textColor=DARK)),
          Paragraph("A Frostwood Puzzle Book", ParagraphStyle("ab0", parent=small, fontSize=9.5)), Spacer(1, 3)]
    for t, d in [("The Thief Stayed the Night", "A snowbound hotel mystery puzzle book: twelve cozy elimination cases."),
                 ("Frostwood Express", "200 Train Tracks logic puzzles."),
                 ("Stars over Frostwood", "180 Star Battle logic puzzles."),
                 ("Tents in Frostwood", "180 Tents and Trees logic puzzles."),
                 ("Riddles by the Frostwood Fire", "140 cozy winter riddles and text logic puzzles for Kindle."),
                 ("The Frostwood Sketchbook", "140 nonogram picture puzzles."),
                 ("Bridges of Frostwood", "180 Hashi bridges logic puzzles."),
                 ("Fences of Frostwood", "100 Slitherlink logic puzzles."),
                 ("The Lockboxes of Frostwood", "120 crack-the-code logic puzzles for Kindle."),
                 ("Chimneys of Frostwood", "100 Skyscrapers logic puzzles.")]:
        S += [Paragraph(f"<i>{t}</i>", ParagraphStyle("ab2", parent=body0, alignment=TA_CENTER, fontSize=11.5, leading=13.5)),
              Paragraph(d, ParagraphStyle("ab3", parent=small, fontSize=9, leading=11)), Spacer(1, 1.5)]
    S += [Spacer(1, 0.04 * inch), Art("thanks", TW, 1.0 * inch)]
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
    doc = Doc(out, pagesize=(W, H), initialFontName="Crimson", title=f"Snow Paths of Frostwood: {NP} Nurikabe Logic Puzzles", author="Blake La Pierre",
              subject="Nurikabe logic puzzle book", pageTemplates=[PageTemplate("normal", [fr], onPageEnd=page_end)])
    doc.pkind = {}; doc.marks = {}; doc.section = ""
    doc.build(S)
    return doc.marks, doc.page


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "../frostwood-10-snow-paths-of-frostwood-interior.pdf"
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
