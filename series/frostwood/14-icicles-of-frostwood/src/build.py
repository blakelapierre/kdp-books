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
assert EX["n"] == 4 and EX["givens"] == [[3, 1, 3]], EX["givens"]
assert EX["ineq"] == [[0, 1, 0, 0], [2, 0, 1, 0], [2, 1, 2, 0], [2, 2, 3, 2]], EX["ineq"]
assert EX["sol"] == [[4, 2, 1, 3], [3, 4, 2, 1], [2, 1, 3, 4], [1, 3, 4, 2]], EX["sol"]

W, H = 6 * inch, 9 * inch
INNER, OUTER, TOP, BOT = 0.75 * inch, 0.55 * inch, 0.7 * inch, 0.75 * inch
DARK = colors.Color(0.17, 0.17, 0.17); MID = colors.Color(0.45, 0.45, 0.45); FROST = colors.Color(0.62, 0.62, 0.62)
INK = colors.Color(0.1, 0.1, 0.1); GRIDC = colors.Color(0.55, 0.55, 0.55); SHADE = colors.Color(0.42, 0.42, 0.42)
TITLE = "The Icicles of Frostwood"
TW = W - INNER - OUTER; TH = H - TOP - BOT

PARTS = {
 "Easy": ("Part One", "The Lodge Eaves", 1,
          "Five-by-five rows of icicles along the lodge eaves. Follow the signs from the smallest icicle up, and every row and column soon falls into place."),
 "Medium": ("Part Two", "The Village Lanes", 2,
            "Six-by-six grids from the cottages of the village. Now and then two squares in a row will share the same two lengths, and that pair shuts the others out."),
 "Hard": ("Part Three", "The Station Yard", 3,
          "Seven-by-seven grids from the station canopy. Somewhere in each one the direct tricks run out, and a short \u201cwhat if?\u201d in pencil shows which length must go where."),
 "Expert": ("Part Four", "The High Meadows", 4,
            "Eight-by-eight grids from the frozen falls below the peaks, the largest in the book, each needing several what-if steps. Take your time and keep a soft eraser close."),
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


def sign_icon(c, x, y, s):
    """Two tiny squares with a 'less than' chevron between them, centred on (x, y)."""
    b = s * 0.36; c.saveState(); c.setLineWidth(0.5); c.setStrokeColor(GRIDC)
    c.rect(x - s / 2, y - b / 2, b, b, stroke=1, fill=0); c.rect(x + s / 2 - b, y - b / 2, b, b, stroke=1, fill=0)
    chevron(c, x, y, b * 0.5, "h", True, INK, 0.7); c.restoreState()


def chevron(c, x, y, a, orient, small_first, col=None, lw=None):
    """A < or > (orient 'h') or an up/down chevron (orient 'v') centred on (x, y), size a.
    The point always faces the smaller square: small_first means the left (or upper) square is smaller."""
    c.saveState(); c.setStrokeColor(col or INK); c.setLineWidth(lw or max(0.6, a * 0.16)); c.setLineCap(1); c.setLineJoin(1)
    d = a * 0.42; e = a * 0.36
    p = c.beginPath()
    if orient == "h":
        if small_first: p.moveTo(x + e, y + d); p.lineTo(x - e, y); p.lineTo(x + e, y - d)
        else: p.moveTo(x - e, y + d); p.lineTo(x + e, y); p.lineTo(x - e, y - d)
    else:
        if small_first: p.moveTo(x - d, y - e); p.lineTo(x, y + e); p.lineTo(x + d, y - e)
        else: p.moveTo(x - d, y + e); p.lineTo(x, y - e); p.lineTo(x + d, y + e)
    c.drawPath(p, stroke=1, fill=0); c.restoreState()


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


GAPF = 0.45
def gsize(n, b): return n * b + (n - 1) * b * GAPF


def draw_grid(c, x0, ytop, b, p, vals=None, given_only=False, fs=None, lw=None, signs=True):
    """(x0, ytop) = top-left corner, b = square size. vals = {(r, c): v} written in pencil-gray (or the full solution)."""
    n = p["n"]; g = b * GAPF; st = b + g
    c.saveState()
    c.setStrokeColor(INK); c.setLineWidth(lw or max(0.5, min(1.1, b * 0.035)))
    for r in range(n):
        for cc in range(n):
            c.rect(x0 + cc * st, ytop - r * st - b, b, b, stroke=1, fill=0)
    fs = fs or b * 0.6
    given = {(r, cc): v for r, cc, v in p["givens"]}
    for (r, cc), v in given.items():
        c.setFillColor(INK); c.setFont("Plex-M", fs)
        c.drawCentredString(x0 + cc * st + b / 2, ytop - r * st - b / 2 - fs * 0.35, str(v))
    if vals:
        c.setFont("Crimson-SB", fs * 1.08); c.setFillColor(SHADE)
        for (r, cc), v in vals.items():
            if (r, cc) in given: continue
            c.drawCentredString(x0 + cc * st + b / 2, ytop - r * st - b / 2 - fs * 0.36, str(v))
    if signs:
        a = min(g * 0.95, b * 0.42)
        for r1, c1, r2, c2 in p["ineq"]:
            if r1 == r2:
                cl = min(c1, c2); x = x0 + cl * st + b + g / 2; y = ytop - r1 * st - b / 2
                chevron(c, x, y, a, "h", c1 < c2)
            else:
                rt = min(r1, r2); x = x0 + c1 * st + b / 2; y = ytop - rt * st - b - g / 2
                chevron(c, x, y, a, "v", r1 < r2)
    c.restoreState()


def sol_vals(p): return {(r, cc): p["sol"][r][cc] for r in range(p["n"]) for cc in range(p["n"])}


def rating(c, x, y, k, r=4.2, gap=11):
    for i in range(4):
        snowflake(c, x - (3 - i) * gap, y, r, DARK if i < k else colors.Color(.78, .78, .78), lw=0.12)


STEP = {"Easy": 0.44 * inch, "Medium": 0.36 * inch, "Hard": 0.47 * inch, "Expert": 0.41 * inch}


class PuzzleBlock(Flowable):
    def __init__(s, p, h): s.p = p; s.h = h; s.width = TW; s.height = h
    def wrap(s, aw, ah): return TW, s.h
    def draw(s):
        c = s.canv; p = s.p; cs = STEP[p["band"]]
        gw = gh = gsize(p["n"], cs)
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
        c.drawRightString(TW - 50, ytop - 12, f"{p['band'].upper()} · {p['n']}×{p['n']}")
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
            c.drawRightString(TW - 26, yb, "Icicles hung"); sign_icon(c, TW - 10, yb + 3, 18)


class SolutionBlock(Flowable):
    def __init__(s, p, w, h, cell): s.p = p; s.width = w; s.height = h; s.cell = cell
    def wrap(s, aw, ah): return s.width, s.height
    def draw(s):
        c = s.canv; p = s.p; cs = s.cell
        gw = gsize(p["n"], cs)
        c.setFont("PlayfairSC-B", 10); c.setFillColor(DARK); c.drawString(0, s.height - 10, f"No. {p['num']}")
        draw_grid(c, (s.width - gw) / 2, s.height - 15, cs, p, vals=sol_vals(p), fs=max(5.0, cs * 0.6), lw=0.45)


# worked example: 1-based rows/columns in the text
def rc(d): return {(r - 1, c - 1): v for (r, c), v in d.items()}
EX_STEP4 = rc({(3, 4): 4, (4, 1): 1, (2, 2): 4, (2, 1): 3, (3, 1): 2, (3, 2): 1})


class Example(Flowable):
    def __init__(s, panels, cell, cap):
        s.panels = panels; s.cell = cell; s.cap = cap; s.width = TW
        s.height = gsize(EX["n"], cell) + 24
    def wrap(s, aw, ah): return TW, s.height
    def draw(s):
        c = s.canv; cs = s.cell; k = len(s.panels)
        gw = gsize(EX["n"], cs)
        gap = (TW - k * gw - 16) / max(k - 1, 1); x = 8
        for i, v in enumerate(s.panels):
            draw_grid(c, x, s.height - 4, cs, EX, vals=v)
            c.setFont("Crimson-I", 9); c.setFillColor(MID); c.drawCentredString(x + gw / 2, 2, s.cap[i])
            x += gw + gap


class RuleArt(Flowable):
    """Three tiny grids: a finished 3x3 (yes), a row with two 2s (no), a broken sign (no)."""
    def __init__(s): s.width = TW; s.height = 1.02 * inch
    def wrap(s, aw, ah): return TW, s.height
    def draw(s):
        c = s.canv; b = 0.2 * inch
        def cross(x, y):
            c.setStrokeColor(INK); c.setLineWidth(1.6); d = 4.2
            c.line(x - d, y - d, x + d, y + d); c.line(x - d, y + d, x + d, y - d)
        ok = dict(n=3, givens=[], ineq=[[0, 1, 0, 0], [1, 2, 2, 2]], sol=[[2, 1, 3], [3, 2, 1], [1, 3, 2]])
        dup = dict(n=3, givens=[], ineq=[], sol=[[2, 1, 2], [3, 2, 1], [1, 3, 3]])
        brk = dict(n=3, givens=[], ineq=[[0, 1, 0, 2]], sol=[[1, 3, 2], [3, 2, 1], [2, 1, 3]])
        grids = [(ok, "A finished grid: yes"), (dup, "Two 2s in a row: no"), (brk, "3 smaller than 2? No")]
        cols = [TW * 0.17, TW * 0.5, TW * 0.83]; gw = gsize(3, b); st = b * (1 + GAPF)
        ytop = s.height - 2
        for (p, cap), cx in zip(grids, cols):
            x0 = cx - gw / 2
            draw_grid(c, x0, ytop, b, p, vals=sol_vals(p), fs=b * 0.62, lw=0.6)
            c.setFont("Crimson-I", 9); c.setFillColor(MID); c.drawCentredString(cx, 2, cap)
        x0 = cols[1] - gw / 2; cross(x0 + 2 * st + b + 6, ytop - b / 2)       # beside the bad row
        x0 = cols[2] - gw / 2; cross(x0 + 1.5 * st + b / 2 - st / 2 + b / 2 + b * GAPF / 2, ytop - b - 6)  # under the broken sign


ILL = os.path.join(HERE, "..", "illustrations")
VIGNETTES = ["v_icicles", "v_lantern", "v_mug", "v_snowman", "v_cottage"]
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
    "Start with the chain in rows 2 and 3: row 3, column 2 is smaller than row 3, column 1, which is smaller than row 2, column 1. Three different lengths in a chain, so row 2, column 1 is at least <b>3</b>, row 3, column 1 is <b>2</b> or <b>3</b>, and row 3, column 2 is at most <b>2</b>.",
    "Row 3 needs a <b>4</b>. It can\u2019t go in its first two squares (they are too small), and row 3, column 3 is smaller than the square below it, so it can\u2019t be <b>4</b> either. The <b>4</b> goes in row 3, column 4.",
    "Column 1 needs a <b>1</b>. Row 1, column 1 is bigger than its neighbour, and rows 2 and 3 are at least <b>3</b> and <b>2</b>, so the <b>1</b> goes at the bottom, in row 4.",
    "Column 2 needs a <b>4</b>. Row 1 is smaller than its neighbour, row 3 is at most <b>2</b> and row 4 is the given <b>3</b>, so row 2, column 2 is <b>4</b>. Now row 2, column 1 must be <b>3</b>, which leaves <b>2</b> for row 3, column 1 and <b>1</b> for row 3, column 2. (This is the middle picture.)",
    "Column 1 is missing only <b>4</b>, at the top. Row 4 still needs <b>2</b> and <b>4</b>; column 4 already has a <b>4</b>, so row 4, column 4 is <b>2</b> and row 4, column 3 is <b>4</b>. Column 2\u2019s last square, row 1, is <b>2</b>, and row 3\u2019s last square is <b>3</b> (and 3 is smaller than the 4 below it).",
    "Row 2 still needs <b>1</b> and <b>2</b>. Column 4 already has a <b>2</b>, so row 2, column 4 is <b>1</b> and row 2, column 3 is <b>2</b>. Row 1 finishes with <b>1</b> in column 3 and <b>3</b> in column 4.",
]


def build(recto_fix):
    S = []
    def recto(tag):
        S.append(PageBreak())
        if tag in recto_fix: S.extend([Kind("blank"), PageBreak()])
        S.append(Kind(mark=tag))
    S += [Kind("title"), Spacer(1, 2.2 * inch),
          Paragraph("The Icicles of<br/>Frostwood", ParagraphStyle("ht", fontName="PlayfairSC-B", fontSize=26, leading=30, alignment=TA_CENTER, textColor=DARK)),
          Spacer(1, 10), Flake(), Spacer(1, 0.5 * inch), Art("v_icicles", TW, 0.85 * inch),
          PageBreak(), Kind("title"), Spacer(1, 0.05 * inch), Art("frontispiece", TW, 7.0 * inch), Spacer(1, 6),
          Paragraph("Icicles along the lodge porch on a still winter evening", ParagraphStyle("fc", parent=small, fontSize=10)),
          PageBreak()]
    S += [Kind("title"), Spacer(1, 0.5 * inch),
          Paragraph("A Frozen-Eaves Puzzle Book", ParagraphStyle("t0", parent=kick, fontSize=11, textColor=MID)),
          Spacer(1, 10),
          Paragraph("The Icicles of<br/>Frostwood", ParagraphStyle("tt", fontName="PlayfairSC-B", fontSize=38, leading=42, alignment=TA_CENTER, textColor=DARK)),
          Spacer(1, 14),
          Paragraph(f"{NP} Futoshiki logic puzzles<br/>from the lodge eaves to the high meadows", ParagraphStyle("t2", parent=small, fontSize=13, leading=17)),
          Spacer(1, 0.4 * inch), Art("title", TW, 2.6 * inch), Spacer(1, 0.4 * inch),
          Paragraph("A Frostwood Puzzle Book", ParagraphStyle("t3", parent=kick, fontSize=10, textColor=DARK)),
          Paragraph("Blake La Pierre", ParagraphStyle("t4", parent=small, fontSize=11))]
    S += [PageBreak(), Kind("nofolio"), Spacer(1, 3.6 * inch)]
    cs = ParagraphStyle("cp", parent=body0, fontSize=9, leading=12, alignment=TA_LEFT)
    for t in [f"<i>The Icicles of Frostwood: {NP} Futoshiki Logic Puzzles</i>",
              "Copyright © 2026 Blake La Pierre. All rights reserved.",
              "No part of this book may be reproduced in any form without written permission from the author, except for brief quotations in reviews. Readers are welcome to photocopy puzzle pages for their own personal use while solving.",
              "Frostwood, its lodge, village, station and meadows are imaginary. Any resemblance to real places is coincidental.",
              "First edition, 2026",
              "Set in Crimson Text, Playfair Display SC and IBM Plex Sans Condensed, used under the SIL Open Font License."]:
        S += [Paragraph(t, cs), Spacer(1, 6)]
    recto("contents")
    S += [Kind(section="Contents"), Spacer(1, 0.3 * inch)] + heading("The Icicles of Frostwood", "Contents")
    S.append(("TOC",))
    S += [Spacer(1, 0.35 * inch),
          Paragraph("On the coldest nights of the winter, icicles grow along every eave in Frostwood: on the lodge porch, the cottages, the station canopy and the frozen falls. "
                    "The village children like to sort them, so that every row and every column holds one icicle of each length, and they leave little signs between them to show which is the longer. "
                    f"{NP} of their grids are left, with only a few lengths and signs filled in. Every puzzle has exactly one solution, and every one can be solved by logic alone, with no guessing.",
                    ParagraphStyle("in", parent=small, fontSize=10.5, leading=14))]
    recto("howto")
    S += [Kind(section="How to Play"), Spacer(1, 0.05 * inch)] + heading("Before You Begin", "How to Play")[:-1] + [Spacer(1, 2)]
    hb = ParagraphStyle("hb", parent=bullet, fontSize=10.2, leading=13.0, spaceAfter=2.0)
    S += [Paragraph("Each puzzle is a square grid of icicles. A grid of 5 squares across holds lengths <b>1</b> to <b>5</b>, a grid of 6 holds <b>1</b> to <b>6</b>, and so on. Write a number in every square so that:",
                    ParagraphStyle("hb0", parent=body0, fontSize=10.6, leading=13.8)), Spacer(1, 2)]
    for t in ["Every <b>row</b> holds each number exactly once.",
              "Every <b>column</b> holds each number exactly once.",
              "Every <b>sign</b> between two squares is obeyed. The point of the sign always faces the <b>smaller</b> number: in 2 &lt; 3 the point faces the 2, and a sign pointing up means the upper square is smaller.",
              "Numbers already printed in the grid are fixed. Write small pencil notes in a corner of a square for the numbers it could still be."]:
        S.append(Paragraph(FL + t, hb))
    S += [Spacer(1, 3), RuleArt(), Spacer(1, 5),
          Paragraph("<b>Useful Tricks</b>", ParagraphStyle("x", parent=body0, alignment=TA_CENTER, textColor=DARK)), Spacer(1, 2)]
    for t in ["<b>Only one place.</b> If a number can go in just one square of a row or column, it goes there.",
              "<b>Only one number.</b> If a square has just one number left that fits, write it in.",
              "<b>Ends of the signs.</b> The smaller side of a sign can never be the largest number, and the bigger side can never be <b>1</b>.",
              "<b>Chains.</b> In a chain of signs like a &lt; b &lt; c, every step adds at least one, so the top of a three-square chain is at least <b>3</b>.",
              "<b>Pairs.</b> From Part Two on, if two squares in a row can only be the same two numbers, those numbers can\u2019t go anywhere else in that row.",
              "<b>What if?</b> From Part Three on, pencil in a number and follow it until something breaks, then rub it out: that square can\u2019t be that number."]:
        S.append(Paragraph(FL + t, hb))
    S += [PageBreak(), Kind(section="How to Play"), Spacer(1, 0.05 * inch)] + heading("Let’s Hang Some Icicles", "A Worked Example")
    S.append(Example([None, EX_STEP4, sol_vals(EX)], 0.26 * inch, ["The puzzle", "After step 4", "Solved"]))
    S.append(Spacer(1, 8))
    S.append(Paragraph("This little 4×4 grid uses the lengths 1 to 4. It has one given (the <b>3</b> in row 4, column 2) and four signs. Rows count from the top and columns from the left.",
                       ParagraphStyle("exi", parent=body0, fontSize=10.3, leading=13.3, spaceAfter=3)))
    ex = ParagraphStyle("exs", parent=bullet, fontSize=10.1, leading=12.9, spaceAfter=2.2)
    for i, t in enumerate(EX_STEPS, 1):
        S.append(Paragraph(f"<font name='PlayfairSC-B' color='#2b2b2b'>{i}.</font>&nbsp;&nbsp;" + t, ex))
    S.append(Spacer(1, 3))
    S.append(Paragraph("Every row and column now holds 1 to 4 once, and every sign is obeyed. Solutions are at the back of the book.", ParagraphStyle("sm2", parent=small, fontSize=9.5)))
    for band in BANDS:
        part, place, k, blurb = PARTS[band]; ps = D[band]
        recto(band)
        S += [Kind("opener"), Kind(section=f"{part} · {place}"), Spacer(1, 0.9 * inch)] + heading(f"{part} · {band} · {ps[0]['n']}×{ps[0]['n']}", place)
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
    S += [Kind("opener"), Kind(section="Solutions"), Spacer(1, 2.4 * inch)] + heading("The Icicle Keepers’ Ledger", "Solutions")
    S.append(Paragraph("Each solution shows the full grid. The given numbers are printed in black and the ones you fill in are in gray.", small))
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
                        q = ps[j]; cell = min((bw - 14), (bh - 22)) / (q["n"] + (q["n"] - 1) * GAPF)
                        row.append(SolutionBlock(q, bw - 6, bh - 4, cell))
                    else: row.append("")
                grid.append(row)
            t = Table(grid, colWidths=[bw] * cols, rowHeights=[bh] * rows)
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Crimson", 10), ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                                   ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            S.append(t)
    recto("about")
    S += [Kind("nofolio"), Spacer(1, 0.05 * inch)] + heading("Thank You for Puzzling", "The Icicles of Frostwood")
    S.append(Paragraph("If you enjoyed sorting the icicles of Frostwood, a short review helps other puzzlers find the book. "
                       "The icicle keepers read every one, usually with a mug of cocoa once the porch lamps are lit.",
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
                 ("Snow Paths of Frostwood", "160 Nurikabe logic puzzles."),
                 ("Chimneys of Frostwood", "100 Skyscrapers logic puzzles."),
                 ("The Fibbers of Frostwood", "120 truth-teller and fibber logic puzzles for Kindle.")]:
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
                rows.append((f"{part} · {place}<br/><font size='9.5' color='#737373'>{b} · {ps[0]['n']}×{ps[0]['n']} · Puzzles {ps[0]['num']}–{ps[-1]['num']}</font>", toc.get(b, 0)))
            rows += [("Solutions", toc.get("solutions", 0))]
            t = Table([[Paragraph(a, ParagraphStyle("tc", parent=body0, fontSize=11.5, leading=14)), str(b)] for a, b in rows], colWidths=[TW - 0.5 * inch, 0.5 * inch])
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Crimson", 11), ("FONT", (1, 0), (1, -1), "Crimson", 11.5), ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), 0.3, FROST), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
            S[i] = t
    fr = Frame(INNER, BOT, TW, TH, id="f", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc = Doc(out, pagesize=(W, H), initialFontName="Crimson", title=f"The Icicles of Frostwood: {NP} Futoshiki Logic Puzzles", author="Blake La Pierre",
              subject="Futoshiki logic puzzle book", pageTemplates=[PageTemplate("normal", [fr], onPageEnd=page_end)])
    doc.pkind = {}; doc.marks = {}; doc.section = ""
    doc.build(S)
    return doc.marks, doc.page


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "../frostwood-14-icicles-of-frostwood-interior.pdf"
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
