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
from slither import Geo

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
assert EX["clues"] == [[None, None, 0, 2, None], [0, None, 1, None, None], [0, None, 2, 1, 1], [None, None, 2, None, 1], [3, None, None, 1, 2]], EX["clues"]
assert EX["loop"] == [4, 8, 17, 20, 21, 25, 26, 27, 28, 29, 34, 35, 39, 41, 45, 47, 50, 53, 54, 59], EX["loop"]

W, H = 6 * inch, 9 * inch
INNER, OUTER, TOP, BOT = 0.75 * inch, 0.55 * inch, 0.7 * inch, 0.75 * inch
DARK = colors.Color(0.17, 0.17, 0.17); MID = colors.Color(0.45, 0.45, 0.45); FROST = colors.Color(0.62, 0.62, 0.62)
INK = colors.Color(0.1, 0.1, 0.1); XC = colors.Color(0.42, 0.42, 0.42)
TITLE = "Fences of Frostwood"
TW = W - INNER - OUTER; TH = H - TOP - BOT

PARTS = {
 "Easy": ("Part One", "The Village Lots", 1,
          "Six-by-six garden lots behind the cottages. Every number can be worked out by counting alone: start with the 0s, the corners and the numbers on the edge of the map, and follow the fence from post to post."),
 "Medium": ("Part Two", "The Lodge Meadow", 2,
            "Seven-by-seven paddocks below the lodge. Counting still does most of the work, but now and then you will need a quick “what if?”: pencil in one edge and watch it break a rule within a few moves."),
 "Hard": ("Part Three", "The Mill Yard", 3,
          "Eight-by-eight plots around the mill. Somewhere in each one the short tricks run out, and you will have to follow a what-if fence a long way before it breaks."),
 "Expert": ("Part Four", "The High Orchard", 4,
            "Ten-by-ten lots on the orchard terraces, the largest maps in the book. Several long what-if steps each. Take your time and keep a soft eraser close."),
}
PREP = {"Easy": "At ", "Medium": "In ", "Hard": "At ", "Expert": "In "}
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


def fence_icon(c, x, y, s):
    """A tiny closed fence loop round two posts' worth of lot, centred on (x, y)."""
    c.saveState(); c.setStrokeColor(INK); c.setLineWidth(max(0.8, s * 0.08)); c.setLineJoin(1); c.setLineCap(1)
    u = s * 0.28
    pts = [(-1.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5), (-0.5, 1.0), (-1.5, 1.0)]
    p = c.beginPath(); p.moveTo(x + pts[0][0] * u + 0.5 * u, y + (pts[0][1] - 0.25) * u)
    for px, py in pts[1:]: p.lineTo(x + px * u + 0.5 * u, y + (py - 0.25) * u)
    p.close(); c.drawPath(p, stroke=1, fill=0)
    c.setFillColor(INK)
    for i in range(-1, 2):
        for j in range(-1, 2): c.circle(x + i * u + 0.0 * u, y + (j - 0.25) * u * 0.5 + 0.0, 0.5, stroke=0, fill=1)
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


def grid_size(p, s):
    return p["w"] * s, p["h"] * s


def draw_slither(c, x0, ytop, s, p, loop=(), crosses=(), fs=None, numbers=True):
    """(x0, ytop) = top-left post. Post (r, c) sits at x0 + c*s, ytop - r*s."""
    g = Geo(p["w"], p["h"])
    X = lambda cc: x0 + cc * s; Y = lambda rr: ytop - rr * s
    c.saveState(); c.setLineCap(1); c.setLineJoin(1)
    if loop:
        c.setStrokeColor(INK); c.setLineWidth(max(1.1, min(3.2, s * 0.085)))
        for e in loop:
            a, b = g.ends[e]
            (r1, c1), (r2, c2) = divmod(a, g.w + 1), divmod(b, g.w + 1)
            c.line(X(c1), Y(r1), X(c2), Y(r2))
    if crosses:
        c.setStrokeColor(XC); c.setLineWidth(max(0.5, s * 0.03)); d = s * 0.075
        for e in crosses:
            a, b = g.ends[e]
            (r1, c1), (r2, c2) = divmod(a, g.w + 1), divmod(b, g.w + 1)
            mx, my = (X(c1) + X(c2)) / 2, (Y(r1) + Y(r2)) / 2
            c.line(mx - d, my - d, mx + d, my + d); c.line(mx - d, my + d, mx + d, my - d)
    c.setFillColor(INK); dr = max(0.75, min(2.0, s * 0.05))
    for r in range(p["h"] + 1):
        for cc in range(p["w"] + 1): c.circle(X(cc), Y(r), dr, stroke=0, fill=1)
    if numbers:
        fs = fs or s * 0.56
        c.setFont("Plex-M", fs); c.setFillColor(INK)
        for r in range(p["h"]):
            for cc in range(p["w"]):
                n = p["clues"][r][cc]
                if n is not None: c.drawCentredString(X(cc) + s / 2, Y(r) - s / 2 - fs * 0.35, str(n))
    c.restoreState()


def rating(c, x, y, k, r=4.2, gap=11):
    for i in range(4):
        snowflake(c, x - (3 - i) * gap, y, r, DARK if i < k else colors.Color(.78, .78, .78), lw=0.12)


STEP = {"Easy": 0.45 * inch, "Medium": 0.41 * inch, "Hard": 0.375 * inch, "Expert": 0.44 * inch}


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
        c.drawRightString(TW - 50, ytop - 12, f"{p['band'].upper()} · {p['w']}×{p['h']}")
        c.setStrokeColor(FROST); c.setLineWidth(0.5); c.line(0, ytop - 20, TW, ytop - 20)
        gtop = ytop - hdr - gap
        draw_slither(c, (TW - gw) / 2, gtop, cs, p)
        if full:
            free_lo, free_hi = foot, gtop - gh - 6
            vh = min(0.85 * inch, free_hi - free_lo - 6)
            if vh >= 0.5 * inch:
                draw_ill(c, VIGNETTES[p["num"] % len(VIGNETTES)], 0, free_lo + (free_hi - free_lo - vh) / 2, TW, vh)
            yb = 6; c.setStrokeColor(FROST); c.setLineWidth(0.5); c.line(0, yb + 16, TW, yb + 16)
            c.setFont("PlayfairSC", 8.5); c.setFillColor(MID)
            c.drawString(0, yb, "Started"); c.line(40, yb - 1, 120, yb - 1)
            c.drawString(146, yb, "Finished"); c.line(190, yb - 1, 250, yb - 1)
            c.drawRightString(TW - 22, yb, "One fence"); fence_icon(c, TW - 9, yb + 3, 14)


class SolutionBlock(Flowable):
    def __init__(s, p, w, h, cell): s.p = p; s.width = w; s.height = h; s.cell = cell
    def wrap(s, aw, ah): return s.width, s.height
    def draw(s):
        c = s.canv; p = s.p; cs = s.cell
        gw, gh = grid_size(p, cs)
        c.setFont("PlayfairSC-B", 10); c.setFillColor(DARK); c.drawString(0, s.height - 10, f"No. {p['num']}")
        draw_slither(c, (s.width - gw) / 2, s.height - 16, cs, p, loop=p["loop"], fs=max(4.8, cs * 0.5))


def edge_ids(w, h, names):
    """'H13' = horizontal edge in post row 1 from post column 3; 'V04' = vertical edge from post row 0 in column 4."""
    out = []
    for n in names:
        r, cc = int(n[1]), int(n[2])
        out.append(r * w + cc if n[0] == "H" else (h + 1) * w + r * (w + 1) + cc)
    return out


EX_X = edge_ids(5, 5, "H02 H12 V02 V03 H10 H20 V10 V11 H30 V20 V21 V30 H21 V00 H00 H01 H03".split())
EX_L = edge_ids(5, 5, ["H13", "V04"])
assert not set(EX_X) & set(EX["loop"]) and set(EX_L) <= set(EX["loop"])


class Example(Flowable):
    def __init__(s, panels, cell, cap):
        s.panels = panels; s.cell = cell; s.cap = cap; s.width = TW
        s.height = grid_size(EX, cell)[1] + 30
    def wrap(s, aw, ah): return TW, s.height
    def draw(s):
        c = s.canv; cs = s.cell; k = len(s.panels)
        gw, gh = grid_size(EX, cs)
        gap = (TW - k * gw - 24) / max(k - 1, 1); x = 12
        for i, (lp, xs) in enumerate(s.panels):
            c.setStrokeColor(FROST); c.setLineWidth(0.5); c.roundRect(x - 9, 15, gw + 18, gh + 18, 4, stroke=1, fill=0)
            draw_slither(c, x, s.height - 6, cs, EX, loop=lp, crosses=xs)
            c.setFont("Crimson-I", 9); c.setFillColor(MID); c.drawCentredString(x + gw / 2, 3, s.cap[i])
            x += gw + gap


class RuleArt(Flowable):
    """Three tiny diagrams: one closed fence (yes), a branching fence (no), two separate loops (no)."""
    def __init__(s): s.width = TW; s.height = 1.12 * inch
    def wrap(s, aw, ah): return TW, s.height
    def draw(s):
        c = s.canv; st = 0.205 * inch
        def grid(x0, y0, nw, nh, segs, bad=None):
            c.saveState(); c.setLineCap(1); c.setLineJoin(1)
            c.setStrokeColor(INK); c.setLineWidth(1.5)
            for (r1, c1, r2, c2) in segs: c.line(x0 + c1 * st, y0 - r1 * st, x0 + c2 * st, y0 - r2 * st)
            c.setFillColor(INK)
            for r in range(nh + 1):
                for cc in range(nw + 1): c.circle(x0 + cc * st, y0 - r * st, 0.9, stroke=0, fill=1)
            if bad:
                bx, by = x0 + bad[1] * st, y0 - bad[0] * st; d = 3.4
                c.setStrokeColor(INK); c.setLineWidth(1.2); c.setFillColor(colors.white)
                c.circle(bx, by, 5.6, stroke=1, fill=1)
                c.line(bx - d * 0.6, by - d * 0.6, bx + d * 0.6, by + d * 0.6); c.line(bx - d * 0.6, by + d * 0.6, bx + d * 0.6, by - d * 0.6)
            c.restoreState()
        yt = s.height - 6; cols = [TW * 0.17, TW * 0.5, TW * 0.83]
        def sq(r, cc, r2, c2): return [(r, cc, r, c2), (r, c2, r2, c2), (r2, c2, r2, cc), (r2, cc, r, cc)]
        # 1: one closed loop, bending round
        segs = [(0, 0, 0, 3), (0, 3, 2, 3), (2, 3, 2, 2), (2, 2, 3, 2), (3, 2, 3, 0), (3, 0, 0, 0)]
        grid(cols[0] - 2 * st, yt, 4, 3, segs)
        c.setFont("Crimson-I", 9); c.setFillColor(MID); c.drawCentredString(cols[0], 2, "One closed fence: yes")
        # 2: a branch (three fence ends at one post)
        segs = [(0, 0, 0, 4), (0, 4, 3, 4), (3, 4, 3, 0), (3, 0, 0, 0), (0, 2, 2, 2)]
        grid(cols[1] - 2 * st, yt, 4, 3, segs, bad=(0, 2))
        c.setFont("Crimson-I", 9); c.setFillColor(MID); c.drawCentredString(cols[1], 2, "Branching: no")
        # 3: two loops
        segs = sq(0, 0, 2, 2) + sq(1, 3, 3, 4)
        grid(cols[2] - 2 * st, yt, 4, 3, segs, bad=(1.5, 2.5))
        c.setFont("Crimson-I", 9); c.setFillColor(MID); c.drawCentredString(cols[2], 2, "Two fences: no")


ILL = os.path.join(HERE, "..", "illustrations")
VIGNETTES = ["v_posts", "v_gate", "v_picket", "v_logs", "v_orchard", "v_stile"]
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


EX_PANELS = [([], []), (EX_L, EX_X), (EX["loop"], [])]
EX_STEPS = [
    "Start with the <b>0</b>s. No fence touches a 0, so put a small × on all four of its sides.",
    "Every post has either no fence or exactly two fence ends. Down the left edge, and either side of the top <b>0</b>, some posts now have only one open edge left. A single fence end is not allowed, so those edges get an × too. The top-left corner goes the same way.",
    "Now the <b>2</b> in the top row: its left side touches the 0 and its top side has just been crossed, so its bottom and right sides must both be fence. (This is the middle picture.)",
    "Follow the fence. From the 2’s top-right corner it can only turn right along the top edge and run down the right side of the map. From its bottom-left corner it can only go down, past the <b>1</b> beside it. That 1 now has its one fence, so cross its other sides.",
    "The middle <b>2</b> has its top and left sides ruled out, so its bottom and right sides are fence. The <b>1</b> to its right is touched on its left by that fence: cross its other three sides.",
    "Down the right side and along the bottom row, each number is settled by its neighbours, and the fence runs all the way along the bottom to the <b>3</b> in the corner. The 3 takes its bottom, left and top sides, and the fence runs back up the left side of the lower 2 to join the piece you started with. One closed fence, and every number counts its fenced sides.",
]


def build(recto_fix):
    S = []
    def recto(tag):
        S.append(PageBreak())
        if tag in recto_fix: S.extend([Kind("blank"), PageBreak()])
        S.append(Kind(mark=tag))
    S += [Kind("title"), Spacer(1, 2.2 * inch),
          Paragraph("Fences of<br/>Frostwood", ParagraphStyle("ht", fontName="PlayfairSC-B", fontSize=26, leading=30, alignment=TA_CENTER, textColor=DARK)),
          Spacer(1, 10), Flake(), Spacer(1, 0.5 * inch), Art("v_posts", TW, 0.85 * inch),
          PageBreak(), Kind("title"), Spacer(1, 0.05 * inch), Art("frontispiece", TW, 7.0 * inch), Spacer(1, 6),
          Paragraph("The posts above the drifts", ParagraphStyle("fc", parent=small, fontSize=10)),
          PageBreak()]
    S += [Kind("title"), Spacer(1, 0.5 * inch),
          Paragraph("A Snowed-Under Puzzle Book", ParagraphStyle("t0", parent=kick, fontSize=11, textColor=MID)),
          Spacer(1, 10),
          Paragraph("Fences of<br/>Frostwood", ParagraphStyle("tt", fontName="PlayfairSC-B", fontSize=38, leading=42, alignment=TA_CENTER, textColor=DARK)),
          Spacer(1, 14),
          Paragraph(f"{NP} Slitherlink fence-loop logic puzzles<br/>from the village lots to the high orchard", ParagraphStyle("t2", parent=small, fontSize=13, leading=17)),
          Spacer(1, 0.4 * inch), Art("title", TW, 2.6 * inch), Spacer(1, 0.4 * inch),
          Paragraph("A Frostwood Puzzle Book", ParagraphStyle("t3", parent=kick, fontSize=10, textColor=DARK)),
          Paragraph("Blake La Pierre", ParagraphStyle("t4", parent=small, fontSize=11))]
    S += [PageBreak(), Kind("nofolio"), Spacer(1, 3.6 * inch)]
    cs = ParagraphStyle("cp", parent=body0, fontSize=9, leading=12, alignment=TA_LEFT)
    for t in [f"<i>Fences of Frostwood: {NP} Slitherlink Logic Puzzles</i>",
              "Copyright © 2026 Blake La Pierre. All rights reserved.",
              "No part of this book may be reproduced in any form without written permission from the author, except for brief quotations in reviews. Readers are welcome to photocopy puzzle pages for their own personal use while solving.",
              "Frostwood, its village, lodge, meadow, mill and orchard are imaginary. Any resemblance to real places is coincidental.",
              "First edition, 2026. Hardcover.",
              "Set in Crimson Text, Playfair Display SC and IBM Plex Sans Condensed, used under the SIL Open Font License."]:
        S += [Paragraph(t, cs), Spacer(1, 6)]
    recto("contents")
    S += [Kind(section="Contents"), Spacer(1, 0.3 * inch)] + heading("Fences of Frostwood", "Contents")
    S.append(("TOC",))
    S += [Spacer(1, 0.35 * inch),
          Paragraph("After the deepest snow in years, the timber fences around Frostwood have vanished under the drifts: the village garden lots, the lodge meadow paddocks, the mill-yard plots and the high orchard terraces. "
                    f"Only the tops of the posts still show, and on some of them the lot-keeper has hung a little number. {NP} maps are left. "
                    "Every puzzle has exactly one solution, and every one can be solved by logic alone, with no guessing.",
                    ParagraphStyle("in", parent=small, fontSize=10.5, leading=14))]
    recto("howto")
    S += [Kind(section="How to Play"), Spacer(1, 0.05 * inch)] + heading("Before You Walk the Bounds", "How to Play")[:-1] + [Spacer(1, 2)]
    hb = ParagraphStyle("hb", parent=bullet, fontSize=10.3, leading=13.2, spaceAfter=2.2)
    S += [Paragraph("Each puzzle is a map of fence <b>posts</b>, the dots, with some squares holding a number. Draw <b>one fence</b> along the dotted lines so that:",
                    ParagraphStyle("hb0", parent=body0, fontSize=10.6, leading=13.8)), Spacer(1, 2)]
    for t in ["The fence runs from post to post, <b>across or down</b>, never diagonally.",
              "It is <b>one closed loop</b>: no loose ends, no branches, and it never crosses or touches itself. Every post has either no fence or exactly two fence ends.",
              "Each <b>number</b> says how many of the four sides of its square are fence. Squares without a number may have any number of fence sides.",
              "There is only <b>one</b> fence. Two separate loops are not allowed."]:
        S.append(Paragraph(FL + t, hb))
    S += [Spacer(1, 3), RuleArt(), Spacer(1, 5),
          Paragraph("<b>Useful Tricks</b>", ParagraphStyle("x", parent=body0, alignment=TA_CENTER, textColor=DARK)), Spacer(1, 2)]
    for t in ["<b>Mark what you know.</b> Put a small × on every edge that cannot be fence. A <b>0</b> gets four of them straight away.",
              "<b>Count the ends.</b> A post with one fence end and one open edge must carry on along it. A post with only one open edge left cannot use it.",
              "<b>Corners.</b> A <b>3</b> in a corner of the map always uses both sides that meet at the corner post; a <b>1</b> in a corner never does.",
              "<b>Side-by-side 3s.</b> When two 3s touch, the edge between them is fence, and so are the two outer edges parallel to it.",
              "<b>Don’t close early.</b> Never join the two ends of a piece of fence unless that finishes the whole puzzle.",
              "<b>What if?</b> From Part Two on, pencil in one edge and follow it until something breaks, then rub it out and cross that edge."]:
        S.append(Paragraph(FL + t, hb))
    S += [PageBreak(), Kind(section="How to Play"), Spacer(1, 0.05 * inch)] + heading("Let’s Mend a Fence", "A Worked Example")
    S.append(Example(EX_PANELS, 0.25 * inch, ["The puzzle", "After step 3", "Solved"]))
    S.append(Spacer(1, 8))
    S.append(Paragraph("This little 5×5 map has thirteen numbers. Draw fence edges as firm lines and mark the edges you rule out with a small ×.",
                       ParagraphStyle("exi", parent=body0, fontSize=10.4, leading=13.4, spaceAfter=3)))
    ex = ParagraphStyle("exs", parent=bullet, fontSize=10.1, leading=12.9, spaceAfter=2.2)
    for i, t in enumerate(EX_STEPS, 1):
        S.append(Paragraph(f"<font name='PlayfairSC-B' color='#2b2b2b'>{i}.</font>&nbsp;&nbsp;" + t, ex))
    S.append(Spacer(1, 4))
    S.append(Paragraph("Solutions are at the back of the book.", ParagraphStyle("sm2", parent=small, fontSize=9.5)))
    for band in BANDS:
        part, place, k, blurb = PARTS[band]; ps = D[band]
        recto(band)
        S += [Kind("opener"), Kind(section=f"{part} · {place}"), Spacer(1, 0.9 * inch)] + heading(f"{part} · {band} · {ps[0]['w']}×{ps[0]['h']}", place)
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
    S += [Kind("opener"), Kind(section="Solutions"), Spacer(1, 2.4 * inch)] + heading("The Lot-Keeper’s Ledger", "Solutions")
    S.append(Paragraph("Each solution shows the one closed fence.", small))
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
                        q = ps[j]; cell = min((bw - 16) / q["w"], (bh - 26) / q["h"])
                        row.append(SolutionBlock(q, bw - 6, bh - 4, cell))
                    else: row.append("")
                grid.append(row)
            t = Table(grid, colWidths=[bw] * cols, rowHeights=[bh] * rows)
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Crimson", 10), ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                                   ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            S.append(t)
    recto("about")
    S += [Kind("nofolio"), Spacer(1, 0.45 * inch)] + heading("Thank You for Walking the Bounds", "Fences of Frostwood")
    S.append(Paragraph("If you enjoyed mending the fences of Frostwood, a short review helps other puzzlers find the book. "
                       "The lot-keepers read every one, usually with a mug of cocoa after the last post is found.",
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
                 ("Bridges of Frostwood", "180 Hashi bridges puzzles. Lay the footbridges across the frozen ponds and the lake of islands.")]:
        S += [Paragraph(f"<i>{t}</i>", ParagraphStyle("ab2", parent=body0, alignment=TA_CENTER, fontSize=12, leading=14.4)),
              Paragraph(d, ParagraphStyle("ab3", parent=small, fontSize=9.3, leading=11.6)), Spacer(1, 4)]
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
    doc = Doc(out, pagesize=(W, H), initialFontName="Crimson", title=f"Fences of Frostwood: {NP} Slitherlink Logic Puzzles", author="Blake La Pierre",
              subject="Slitherlink (Loop the Loop / Fences) logic puzzle book", pageTemplates=[PageTemplate("normal", [fr], onPageEnd=page_end)])
    doc.pkind = {}; doc.marks = {}; doc.section = ""
    doc.build(S)
    return doc.marks, doc.page


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "frostwood-08-fences-of-frostwood-interior.pdf")
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
