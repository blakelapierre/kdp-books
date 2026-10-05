"""Builds the 6x9 interior PDF for Logic on Lantern Lane (grayscale, no bleed, mirrored margins,
embedded fonts) -> ../standalone-04-logic-on-lantern-lane-interior.pdf and ../build-info.json"""
from __future__ import annotations
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak, Table, TableStyle, Flowable
from reportlab.lib.fonts import addMapping
from layout import W, H, INNER, OUTER, TOP, BOT, TW, TH, BAND_LAYOUT, CLUE_INDENT, HEADER_H, INTRO_GAP

G = "/usr/share/fonts/truetype/sand-box/google/"
for n, p in [
    ("Crimson", "Crimson Text/CrimsonText-Regular.ttf"), ("Crimson-I", "Crimson Text/CrimsonText-Italic.ttf"),
    ("Crimson-B", "Crimson Text/CrimsonText-Bold.ttf"), ("Crimson-SB", "Crimson Text/CrimsonText-SemiBold.ttf"),
    ("Crimson-BI", "Crimson Text/CrimsonText-BoldItalic.ttf"),
    ("PlayfairSC", "Playfair Display SC/PlayfairDisplaySC-Regular.ttf"), ("PlayfairSC-B", "Playfair Display SC/PlayfairDisplaySC-Bold.ttf"),
    ("Plex", "IBM Plex Sans Condensed/IBMPlexSansCondensed-Regular.ttf"), ("Plex-M", "IBM Plex Sans Condensed/IBMPlexSansCondensed-SemiBold.ttf"),
]:
    pdfmetrics.registerFont(TTFont(n, G + p))
from reportlab import rl_config
rl_config.canvas_basefontname = "Crimson"
ParagraphStyle.defaults["fontName"] = "Crimson"
ParagraphStyle.defaults["bulletFontName"] = "Crimson"
addMapping("Crimson", 0, 0, "Crimson"); addMapping("Crimson", 0, 1, "Crimson-I")
addMapping("Crimson", 1, 0, "Crimson-B"); addMapping("Crimson", 1, 1, "Crimson-BI")

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "..", "data.json")))
BANDS = ["Easy", "Medium", "Hard", "Expert"]
ALL = [p for b in BANDS for p in D[b]]
EX = D["Example"][0]
assert len(ALL) == 120
TITLE = "Logic on Lantern Lane"
OUTNAME = "standalone-04-logic-on-lantern-lane-interior.pdf"

DARK = colors.Color(0.15, 0.15, 0.15)
MID = colors.Color(0.42, 0.42, 0.42)
LINE = colors.Color(0.55, 0.55, 0.55)
PALE = colors.Color(0.9, 0.9, 0.9)
INK = colors.Color(0.08, 0.08, 0.08)

PARTS = {
    "Easy": ("Part One", "Morning Tea", "Three categories of four. Gentle warm-ups with plenty of direct clues."),
    "Medium": ("Part Two", "On the Green", "Four categories of four. Either-or and neither-nor clues join in."),
    "Hard": ("Part Three", "The Bookshop Corner", "Four categories of five. Fewer direct clues, more comparing and counting."),
    "Expert": ("Part Four", "The Lantern Parade", "Five categories of five, on a two-page spread: clues on the left, grid on the right."),
}
DOTS = {"Easy": 1, "Medium": 2, "Hard": 3, "Expert": 4}

ILL = os.path.join(HERE, "..", "illustrations")
VIGNETTES = __import__("illustrations").VIGNETTES


def draw_ill(c, name, x, y, w, h):
    from reportlab.lib.utils import ImageReader
    path = os.path.join(ILL, name + ".png")
    iw, ih = ImageReader(path).getSize()
    sc = min(w / iw, h / ih)
    c.drawImage(path, x + (w - iw * sc) / 2, y + (h - ih * sc) / 2, iw * sc, ih * sc)


class Doc(BaseDocTemplate):
    def handle_pageBegin(self):
        p = self.page + 1
        left = INNER if p % 2 == 1 else OUTER
        for t in self.pageTemplates:
            for f in t.frames:
                f._x1 = left
                f._geom()
        super().handle_pageBegin()


class Kind(Flowable):
    def __init__(s, kind=None, section=None, mark=None):
        s.kind, s.section, s.mark = kind, section, mark
        s.width = s.height = 0

    def wrap(s, aw, ah):
        return 0, 0

    def draw(s):
        doc = s.canv._doctemplate
        if s.kind:
            doc.pkind[doc.page] = s.kind
        if s.section is not None:
            doc.section = s.section
        if s.mark:
            doc.marks[s.mark] = doc.page


class Art(Flowable):
    def __init__(s, name, w, h):
        s.name, s.width, s.height = name, w, h

    def wrap(s, aw, ah):
        return s.width, s.height

    def draw(s):
        draw_ill(s.canv, s.name, 0, 0, s.width, s.height)


class EvenStart(Flowable):
    """Placed right after a PageBreak: if the new page is odd, mark it blank and break again (handled in build loop)."""


def page_end(c, doc):
    p = doc.page
    kind = getattr(doc, "pkind", {}).get(p, "normal")
    if kind == "blank":
        draw_ill(c, "v_lamp", (INNER if p % 2 else OUTER) + (TW - 1.9 * inch) / 2, BOT + TH / 2 - 0.42 * inch, 1.9 * inch, 0.85 * inch)
        return
    if kind in ("title", "nofolio"):
        return
    c.saveState()
    c.setFont("Crimson", 9)
    c.setFillColor(MID)
    c.drawCentredString(W / 2 + ((INNER - OUTER) / 2 if p % 2 else -(INNER - OUTER) / 2), 0.42 * inch, str(p))
    if kind != "opener":
        c.setFont("PlayfairSC", 7.5)
        if p % 2 == 0:
            c.drawString(OUTER, H - 0.42 * inch, TITLE)
        else:
            c.drawRightString(W - OUTER, H - 0.42 * inch, getattr(doc, "section", ""))
    c.restoreState()


# ------------------------------------------------------------------------------------------ grids
def grid_size(P, cell, lab):
    return lab + (P["k"] - 1) * P["n"] * cell


def fit_font(texts, font, size, maxw, minsize=5.6):
    while size > minsize and max(pdfmetrics.stringWidth(t, font, size) for t in texts) > maxw:
        size -= 0.2
    return size


def draw_grid(c, P, x0, ytop, cell, lab, solved=False):
    """Standard logic grid. Top-left corner at (x0, ytop). If solved, ticks and crosses are filled in."""
    k, n, cats = P["k"], P["n"], P["cats"]
    cols = list(range(1, k))
    rows = [0] + list(range(k - 1, 1, -1))
    cs = 12.5  # category-name strip
    xg, yg = x0 + lab, ytop - lab
    labels = [t for cat in cats for t in cat["items"]]
    fs = fit_font(labels, "Plex", 7.6, lab - cs - 6)
    names = [cat["name"] for cat in cats]
    cfs = fit_font(names, "PlayfairSC-B", 7.6, n * cell - 4, 5.4)
    sol = P["solution"]
    ent = lambda ca, i: sol[ca].index(i)
    # column headers
    for ci, ca in enumerate(cols):
        bx = xg + ci * n * cell
        c.setFillColor(DARK); c.setFont("PlayfairSC-B", cfs)
        c.drawCentredString(bx + n * cell / 2, ytop - cs + 3.5, cats[ca]["name"])
        c.setFont("Plex", fs); c.setFillColor(INK)
        for i, t in enumerate(cats[ca]["items"]):
            c.saveState()
            c.translate(bx + i * cell + cell / 2 + fs * 0.35, yg + 3)
            c.rotate(90)
            c.drawString(0, 0, t)
            c.restoreState()
    # row headers
    for ri, ra in enumerate(rows):
        by = yg - ri * n * cell
        c.saveState()
        c.translate(x0 + cs - 4, by - n * cell / 2)
        c.rotate(90)
        c.setFillColor(DARK); c.setFont("PlayfairSC-B", cfs)
        c.drawCentredString(0, 0, cats[ra]["name"])
        c.restoreState()
        c.setFont("Plex", fs); c.setFillColor(INK)
        for i, t in enumerate(cats[ra]["items"]):
            c.drawRightString(xg - 3, by - i * cell - cell / 2 - fs * 0.35, t)
    # blocks
    for ri, ra in enumerate(rows):
        for ci, ca in enumerate(cols):
            if ri + ci > k - 2:
                continue
            bx, by = xg + ci * n * cell, yg - ri * n * cell
            c.setStrokeColor(LINE); c.setLineWidth(0.45)
            for t in range(1, n):
                c.line(bx + t * cell, by, bx + t * cell, by - n * cell)
                c.line(bx, by - t * cell, bx + n * cell, by - t * cell)
            c.setStrokeColor(INK); c.setLineWidth(1.1)
            c.rect(bx, by - n * cell, n * cell, n * cell, stroke=1, fill=0)
            if solved:
                for i in range(n):
                    for j in range(n):
                        cx, cy = bx + j * cell + cell / 2, by - i * cell - cell / 2
                        if ent(ra, i) == ent(ca, j):
                            c.setFillColor(INK); c.circle(cx, cy, cell * 0.22, stroke=0, fill=1)
                        else:
                            c.setStrokeColor(MID); c.setLineWidth(0.6)
                            d = cell * 0.16
                            c.line(cx - d, cy - d, cx + d, cy + d); c.line(cx - d, cy + d, cx + d, cy - d)
    return grid_size(P, cell, lab)


def answer_table_height(P, rh=15):
    return (P["n"] + 1) * rh


def draw_answer_table(c, P, x0, ytop, width, rh=15, filled=False):
    k, n, cats = P["k"], P["n"], P["cats"]
    cw = width / k
    c.setFillColor(PALE)
    c.rect(x0, ytop - rh, width, rh, stroke=0, fill=1)
    c.setFillColor(DARK)
    hf = fit_font([cat["name"] for cat in cats], "PlayfairSC-B", 8.2, cw - 6, 5.6)
    for j, cat in enumerate(cats):
        c.setFont("PlayfairSC-B", hf)
        c.drawCentredString(x0 + j * cw + cw / 2, ytop - rh + 4.5, cat["name"])
    sol = P["solution"]
    body = [t for cat in cats for t in cat["items"]]
    bf = fit_font(body, "Crimson", 9.2, cw - 6, 6)
    for e in range(n):
        y = ytop - rh * (e + 2)
        c.setFont("Crimson", bf); c.setFillColor(INK)
        c.drawCentredString(x0 + cw / 2, y + 4.5, cats[0]["items"][e])
        if filled:
            for j in range(1, k):
                c.drawCentredString(x0 + j * cw + cw / 2, y + 4.5, cats[j]["items"][sol[j][e]])
    c.setStrokeColor(LINE); c.setLineWidth(0.45)
    for e in range(n + 2):
        c.line(x0, ytop - rh * e, x0 + width, ytop - rh * e)
    for j in range(k + 1):
        c.line(x0 + j * cw, ytop, x0 + j * cw, ytop - rh * (n + 1))


# ------------------------------------------------------------------------------------------ puzzle pages
def header(c, P, y, width, label=None, sub=None):
    c.setFillColor(DARK)
    c.setFont("PlayfairSC-B", 13)
    lab = label or f"{P['num']} · {P['title']}"
    c.drawString(0, y - 12, lab)
    band = P["band"]
    if band in DOTS:
        c.setFont("Crimson-I", 9.5); c.setFillColor(MID)
        dots = DOTS[band]
        r = 2.6
        xr = width
        for i in range(4):
            cx = xr - (3 - i) * 8 - r
            if i < dots:
                c.setFillColor(DARK); c.circle(cx, y - 8.5, r, stroke=0, fill=1)
            else:
                c.setStrokeColor(MID); c.setLineWidth(0.6); c.circle(cx, y - 8.5, r, stroke=1, fill=0)
        c.setFillColor(MID)
        c.drawRightString(xr - 4 * 8 - 3, y - 11.5, sub or band)
    c.setStrokeColor(LINE); c.setLineWidth(0.6)
    c.line(0, y - 17, width, y - 17)
    return y - 24


def para(c, text, style, x, y, width):
    p = Paragraph(text, style)
    w, h = p.wrap(width, 1000)
    p.drawOn(c, x, y - h)
    return y - h


def clue_styles(band):
    from layout import styles
    return styles(band)


def draw_clues(c, P, y, width, band):
    st, intro = clue_styles(band)
    y = para(c, P["intro"], intro, 0, y, width) - INTRO_GAP
    for i, cl in enumerate(P["clues"], 1):
        p = Paragraph(cl["text"], st, bulletText=f"{i}.")
        w, h = p.wrap(width, 1000)
        p.drawOn(c, 0, y - h)
        y -= h + st.spaceAfter
    return y


class PuzzlePage(Flowable):
    """One whole page: header, story, clues, and the grid anchored at the bottom."""

    def __init__(s, P, band=None, label=None, sub=None, vignette=None):
        s.P, s.band, s.label, s.sub, s.vig = P, band or P["band"], label, sub, vignette
        s.width, s.height = TW, TH - 1

    def wrap(s, aw, ah):
        return s.width, s.height

    def draw(s):
        c, P = s.canv, s.P
        L = BAND_LAYOUT[s.band]
        y = header(c, P, s.height, s.width, s.label, s.sub)
        y = draw_clues(c, P, y, s.width, s.band)
        gs = grid_size(P, L["cell"], L["lab"])
        gx = (s.width - gs) / 2
        draw_grid(c, P, gx, gs, L["cell"], L["lab"])
        room = y - gs
        assert room >= 6, f"puzzle {P['num']} overflows by {6 - room:.1f}pt"
        th = answer_table_height(P)
        if s.band in ("Easy",) and room >= th + 22:
            tw = min(s.width, 70 * P["k"])
            draw_answer_table(c, P, (s.width - tw) / 2, gs + (room + th) / 2, tw)
        elif room >= 0.72 * inch and s.vig:
            h = min(0.85 * inch, room - 14)
            draw_ill(c, s.vig, 0, gs + (room - h) / 2, s.width, h)


class ExpertLeft(Flowable):
    def __init__(s, P, vignette):
        s.P, s.vig = P, vignette
        s.width, s.height = TW, TH - 1

    def wrap(s, aw, ah):
        return s.width, s.height

    def draw(s):
        c, P = s.canv, s.P
        y = header(c, P, s.height, s.width)
        y = draw_clues(c, P, y, s.width, "Expert")
        y -= 10
        c.setFillColor(MID); c.setFont("PlayfairSC", 8.5)
        if y > 90:
            c.drawString(0, y - 8, "Notes")
            y -= 22
            c.setStrokeColor(PALE); c.setLineWidth(0.6)
            while y > 4:
                c.line(0, y, s.width, y)
                y -= 19


class ExpertRight(Flowable):
    def __init__(s, P):
        s.P = P
        s.width, s.height = TW, TH - 1

    def wrap(s, aw, ah):
        return s.width, s.height

    def draw(s):
        c, P = s.canv, s.P
        L = BAND_LAYOUT["Expert"]
        y = header(c, P, s.height, s.width, label=f"{P['num']} · Grid", sub="Expert")
        gs = grid_size(P, L["cell"], L["lab"])
        draw_grid(c, P, (s.width - gs) / 2, y - 6, L["cell"], L["lab"])
        y = y - 6 - gs - 22
        c.setFillColor(MID); c.setFont("PlayfairSC", 8.5)
        c.drawString(0, y + 6, "Answers")
        draw_answer_table(c, P, 0, y, s.width, rh=16)


class SolvedExample(Flowable):
    """Walkthrough page for the worked example, with the finished grid."""

    def __init__(s, P, steps):
        s.P, s.steps = P, steps
        s.width, s.height = TW, TH - 1

    def wrap(s, aw, ah):
        return s.width, s.height

    def draw(s):
        c, P = s.canv, s.P
        y = header(c, P, s.height, s.width, label="Solving the Example", sub=" ")
        st = ParagraphStyle("ws", fontName="Crimson", fontSize=10.3, leading=13.1, leftIndent=14, bulletIndent=0,
                            bulletFontName="PlayfairSC-B", textColor=INK, spaceAfter=3, alignment=TA_LEFT)
        for i, t in enumerate(s.steps, 1):
            p = Paragraph(t, st, bulletText=f"{i}")
            w, h = p.wrap(s.width, 1000)
            p.drawOn(c, 0, y - h)
            y -= h + 3
        cell, lab = 15, 78
        gs = grid_size(P, cell, lab)
        tw = s.width - gs - 12
        th = answer_table_height(P)
        draw_grid(c, P, 0, gs, cell, lab, solved=True)
        draw_answer_table(c, P, s.width - tw, gs - lab + 4, tw, filled=True)
        assert y >= gs + 6, f"example walkthrough overflows by {gs + 6 - y:.1f}"


# ------------------------------------------------------------------------------------------ hints & solutions
class SolutionBlock(Flowable):
    def __init__(s, P, width):
        s.P = P
        s.width = width
        s.rh = 10.6
        s.height = 15 + (P["n"] + 1) * s.rh + 9

    def wrap(s, aw, ah):
        return s.width, s.height

    def draw(s):
        c, P = s.canv, s.P
        y = s.height
        c.setFillColor(DARK)
        ttl = f"{P['num']} · {P['title']}"
        c.setFont("PlayfairSC-B", fit_font([ttl], "PlayfairSC-B", 9.4, s.width - 2, 6.8))
        c.drawString(0, y - 10, ttl)
        y -= 15
        k, n, cats = P["k"], P["n"], P["cats"]
        cw = s.width / k
        hf = fit_font([cat["name"] for cat in cats], "PlayfairSC", 7.6, cw - 4, 5.5)
        bf = fit_font([t for cat in cats for t in cat["items"]], "Crimson", 8.8, cw - 4, 5.8)
        c.setFillColor(PALE); c.rect(0, y - s.rh, s.width, s.rh, stroke=0, fill=1)
        c.setFillColor(DARK)
        for j, cat in enumerate(cats):
            c.setFont("PlayfairSC", hf); c.drawString(j * cw + 3, y - s.rh + 3, cat["name"])
        sol = P["solution"]
        for e in range(n):
            yy = y - s.rh * (e + 2)
            c.setFillColor(INK)
            for j in range(k):
                c.setFont("Crimson-SB" if j == 0 else "Crimson", bf)
                c.drawString(j * cw + 3, yy + 3, cats[j]["items"][sol[j][e]])
            c.setStrokeColor(PALE); c.setLineWidth(0.4)
            c.line(0, yy, s.width, yy)


def fits_half(P):
    w = TW / 2 - 8
    cw = w / P["k"]
    items = [t for cat in P["cats"] for t in cat["items"]]
    names = [cat["name"] for cat in P["cats"]]
    return (max(pdfmetrics.stringWidth(t, "Crimson", 7.4) for t in items) <= cw - 4 and
            max(pdfmetrics.stringWidth(t, "PlayfairSC", 6.6) for t in names) <= cw - 4)


class SolPair(Flowable):
    def __init__(s, a, b, width):
        s.a, s.b = SolutionBlock(a, width / 2 - 8), (SolutionBlock(b, width / 2 - 8) if b else None)
        s.width = width
        s.height = max(s.a.height, s.b.height if s.b else 0)

    def wrap(s, aw, ah):
        return s.width, s.height

    def draw(s):
        s.a.drawOn(s.canv, 0, s.height - s.a.height)
        if s.b:
            s.b.drawOn(s.canv, s.width / 2 + 8, s.height - s.b.height)


body = ParagraphStyle("b", fontName="Crimson", fontSize=11, leading=14.6, alignment=TA_JUSTIFY, textColor=INK)
bullet = ParagraphStyle("bu", parent=body, leftIndent=13, bulletIndent=0, spaceAfter=3.5, alignment=TA_LEFT)
small = ParagraphStyle("s", fontName="Crimson-I", fontSize=10, leading=13, alignment=TA_CENTER, textColor=colors.Color(0.3, 0.3, 0.3))


def heading(kicker, title):
    return [
        Paragraph(kicker, ParagraphStyle("k", fontName="PlayfairSC", fontSize=9.5, leading=12, alignment=TA_CENTER, textColor=MID, spaceAfter=4)),
        Paragraph(title, ParagraphStyle("h1", fontName="PlayfairSC-B", fontSize=20, leading=24, alignment=TA_CENTER, textColor=DARK, spaceAfter=2)),
        Spacer(1, 8),
    ]


EX_STEPS_EXPECT = [
    "Arthur collected it later than the child who lost the red mitten.",
    "Arthur collected it 15 minutes after Harold.",
    "Ernest did not lose the green mitten.",
    "The child who collected it at 3:30 did not lose the blue mitten.",
    "Arthur collected it 15 minutes before the child who lost the green mitten.",
    "The child who lost the blue mitten collected it half an hour before Monty.",
]
EX_STEPS = [
    "<b>Clue 6</b> puts the blue mitten half an hour before Monty, so blue was collected at 3:30 or 3:45. "
    "<b>Clue 4</b> rules out 3:30. Tick <b>blue = 3:45</b>, and so <b>Monty = 4:15</b>. Cross out the rest of those rows and columns.",
    "<b>Clues 2 and 5</b> make a chain: Harold, then Arthur 15 minutes later, then the green mitten 15 minutes after that. "
    "So neither Harold nor Arthur lost the green mitten, and <b>clue 3</b> says Ernest didn't either. Only one name is left: <b>Monty lost the green mitten</b>.",
    "Monty came at 4:15, so the chain reads backwards: <b>Arthur = 4:00</b> and <b>Harold = 3:45</b>. That leaves <b>Ernest = 3:30</b>.",
    "Carry the tick across the grid: blue was collected at 3:45, and Harold came at 3:45, so <b>Harold lost the blue mitten</b>.",
    "<b>Clue 1</b>: the red mitten was collected before Arthur's 4:00, so at 3:30 or 3:45. 3:45 is blue, so red is 3:30: <b>Ernest lost the red mitten</b>. "
    "The only mitten left, yellow, is <b>Arthur's</b>.",
    "Check every clue against the finished grid. Each one holds, and every row and column has exactly one tick.",
]


def build(blank_before):
    S = []

    def recto(tag):
        S.append(PageBreak())
        if tag in blank_before:
            S.extend([Kind("blank"), PageBreak()])
        S.append(Kind(mark=tag))

    # Half title + frontispiece
    S += [Kind("title"), Spacer(1, 2.1 * inch),
          Paragraph("Logic on<br/>Lantern Lane", ParagraphStyle("ht", fontName="PlayfairSC-B", fontSize=26, leading=31, alignment=TA_CENTER, textColor=DARK)),
          Spacer(1, 0.5 * inch), Art("v_lantern", TW, 0.85 * inch),
          PageBreak(), Kind("title"), Spacer(1, 0.05 * inch), Art("frontispiece", TW, 7.0 * inch), Spacer(1, 6),
          Paragraph("Lantern Lane, just after the lamps are lit", ParagraphStyle("fc", parent=small, fontSize=10)), PageBreak()]
    # Title page
    S += [Kind("title"), Spacer(1, 0.5 * inch),
          Paragraph("Cozy Logic Grid Puzzles for Adults", ParagraphStyle("t0", fontName="PlayfairSC", fontSize=10, leading=13, alignment=TA_CENTER, textColor=MID)),
          Spacer(1, 12),
          Paragraph("Logic on<br/>Lantern Lane", ParagraphStyle("tt", fontName="PlayfairSC-B", fontSize=36, leading=41, alignment=TA_CENTER, textColor=DARK)),
          Spacer(1, 12),
          Paragraph("120 village puzzles to solve with a pencil<br/>Easy to Expert · Hints &amp; Solutions",
                    ParagraphStyle("t2", parent=small, fontSize=12.5, leading=16)),
          Spacer(1, 0.3 * inch), Art("title", TW, 2.0 * inch), Spacer(1, 0.3 * inch),
          Paragraph("Blake La Pierre", ParagraphStyle("t4", parent=small, fontSize=12))]
    # Copyright
    S += [PageBreak(), Kind("nofolio"), Spacer(1, 3.6 * inch)]
    cs = ParagraphStyle("cp", parent=body, fontSize=9, leading=12, alignment=TA_LEFT)
    for t in ["<i>Logic on Lantern Lane: 120 Cozy Logic Grid Puzzles for Adults</i>",
              "Copyright © 2026 Blake La Pierre. All rights reserved.",
              "No part of this book may be reproduced in any form without written permission from the author, except for brief quotations in reviews. Readers may photocopy puzzle pages for their own solving.",
              "Lantern Lane and everyone who lives there are made up. Any resemblance to real people or places is a happy accident.",
              "First edition, 2026",
              "Set in Crimson Text, Playfair Display SC and IBM Plex Sans Condensed, used under the SIL Open Font License."]:
        S += [Paragraph(t, cs), Spacer(1, 6)]

    # Contents
    recto("contents")
    S += [Kind(section="Contents"), Spacer(1, 0.25 * inch)] + heading(TITLE, "Contents")
    S.append(("TOC",))
    S += [Spacer(1, 0.3 * inch), Paragraph(
        "Welcome to Lantern Lane, a small village with a bake sale every winter, a pond for skating and a lamp at every gate. "
        "Each puzzle is a little scene from village life. Match everyone to the right things using the clues and the grid. "
        "Every puzzle has exactly one answer, and you can always reach it by reasoning alone. No guessing is needed.",
        ParagraphStyle("in", parent=small, fontSize=10.5, leading=14))]

    # How to solve
    recto("howto")
    S += [Kind(section="How to Solve"), Spacer(1, 0.05 * inch)] + heading("Before You Begin", "How to Solve")
    hb = ParagraphStyle("hb", parent=body, fontSize=10.6, leading=13.9, spaceAfter=5)
    hl = ParagraphStyle("hl", parent=bullet, fontSize=10.4, leading=13.5)
    S.append(Paragraph(
        "Each puzzle tells a short story about a few villagers. Every villager is matched with <b>exactly one</b> item from each category "
        "(a bake, a price, a time, and so on), and no two villagers share an item. The clues tell you just enough to work out who has what.", hb))
    for t in [
        "<b>Use the grid.</b> Each small square of the grid compares two categories. Put an <b>X</b> in a box when the clues rule a match out, and a <b>dot</b> when a match is certain.",
        "<b>One dot per row and column.</b> When you place a dot, cross out every other box in its row and its column inside that square.",
        "<b>Carry it across.</b> If Martha brought the scones and the scones cost $3, then Martha paid $3. If Martha brought the scones and the scones did <i>not</i> cost $3, then Martha didn't pay $3. Copy each discovery into the other squares.",
        "<b>Last box standing.</b> When only one box in a row or column is left without an X, it must be a dot.",
        "<b>Read every clue again.</b> A clue that told you nothing at first often settles everything later.",
        "<b>Use the answer table</b> on the Easy pages and the Expert spreads to write in the final matches.",
    ]:
        S.append(Paragraph(t, hl, bulletText="•"))
    S += [PageBreak(), Kind(section="How to Solve"), Spacer(1, 0.05 * inch)] + heading("Before You Begin", "Reading the Clues")
    for t in [
        "<b>“Earlier”, “later”, “more”, “fewer”, “higher”, “farther”</b> compare two <i>different</i> villagers. "
        "If Ada arrived earlier than the baker with the red cloth, Ada didn't use the red cloth, and Ada can't have the latest time.",
        "<b>Exact gaps.</b> “Arrived 15 minutes before” or “two places ahead of” gives the exact distance on the list. The times, prices and counts in each puzzle go up in even steps, so check the grid labels.",
        "<b>“Either … or …”</b> means <i>exactly one</i> of the two is true, never both. So the two things named after “either” and “or” belong to different villagers.",
        "<b>“Neither A nor B …”</b> gives two separate facts: A isn't it, and B isn't it.",
        "<b>“Of A and B, one … and the other …”</b> means A and B are two different villagers, and between them they hold exactly those two items.",
        "<b>“The baker who brought the fudge”</b> is just another way of naming one villager. They may turn out to be someone you already know by name.",
        "<b>Order labels.</b> In “placed first” or “was second in line”, first is at the top: placing higher means a smaller number.",
    ]:
        S.append(Paragraph(t, hl, bulletText="•"))
    S += [Spacer(1, 6), Paragraph(
        "<b>Difficulty.</b> Easy puzzles have three categories of four. Medium have four of four, Hard four of five, and Expert five of five on a two-page spread. "
        "Stuck? The hints at the back show one sure first step for every puzzle, and the solutions follow.", hb)]

    # Worked example
    recto("example")
    for a, b in zip(EX["clues"], EX_STEPS_EXPECT):
        assert a["text"] == b, ("worked example changed; rewrite EX_STEPS", a["text"])
    S += [Kind(section="A Worked Example"), PuzzlePage(EX, band="Easy", label="Worked Example · The Lost Mittens", sub="Try it first")]
    S += [PageBreak(), Kind(section="A Worked Example"), SolvedExample(EX, EX_STEPS)]

    # Puzzles
    for band in BANDS:
        part, line, blurb = PARTS[band]
        ps = D[band]
        recto(band)
        S += [Kind("opener"), Kind(section=f"{part} · {line}"), Spacer(1, 1.0 * inch)] + heading(f"{part} · {band}", line)
        S += [Paragraph(f"Puzzles {ps[0]['num']} to {ps[-1]['num']}", ParagraphStyle("pn", parent=small, fontSize=11)), Spacer(1, 12),
              Paragraph(blurb, ParagraphStyle("bl", parent=small, fontSize=11, leading=15)), Spacer(1, 0.4 * inch),
              Art("opener-" + band.lower(), TW, 2.4 * inch)]
        for i, P in enumerate(ps):
            vig = VIGNETTES[(P["num"] * 3) % len(VIGNETTES)]
            S += [PageBreak(), Kind(section=f"{part} · {line}")]
            if band == "Expert":
                S += [Kind(mark=f"exp{P['num']}"), ExpertLeft(P, vig), PageBreak(), Kind(section=f"{part} · {line}"), ExpertRight(P)]
            else:
                S.append(PuzzlePage(P, vignette=vig))

    # Hints
    recto("hints")
    S += [Kind("opener"), Kind(section="Hints"), Spacer(1, 1.8 * inch)] + heading("A Gentle Nudge", "Hints")
    S.append(Paragraph("Each hint gives one sure first step for its puzzle and the clues that lead to it. "
                       "Everything else follows from there.", small))
    S += [PageBreak(), Kind(section="Hints")]
    hs = ParagraphStyle("hs", fontName="Crimson", fontSize=9.6, leading=12, leftIndent=24, bulletIndent=0,
                        bulletFontName="PlayfairSC-B", bulletFontSize=9.4, spaceAfter=3.2, textColor=INK)
    for band in BANDS:
        S.append(Paragraph(band, ParagraphStyle("hh", fontName="PlayfairSC-B", fontSize=11, textColor=DARK, spaceBefore=4, spaceAfter=4)))
        for P in D[band]:
            S.append(Paragraph(P["hint"], hs, bulletText=str(P["num"])))

    # Solutions
    recto("solutions")
    S += [Kind("opener"), Kind(section="Solutions"), Spacer(1, 1.8 * inch)] + heading("Every Match, Revealed", "Solutions")
    S.append(Paragraph("The full answer for every puzzle, one row per villager.", small))
    for band in BANDS:
        ps = D[band]
        S += [PageBreak(), Kind(section=f"Solutions · {band}")]
        S.append(Paragraph(band, ParagraphStyle("sh", fontName="PlayfairSC-B", fontSize=11, textColor=DARK, spaceAfter=6)))
        i = 0
        while i < len(ps):
            if i + 1 < len(ps) and fits_half(ps[i]) and fits_half(ps[i + 1]):
                S.append(SolPair(ps[i], ps[i + 1], TW)); i += 2
            else:
                S.append(SolutionBlock(ps[i], TW)); i += 1

    # About
    recto("about")
    S += [Kind("nofolio"), Spacer(1, 1.5 * inch)] + heading("Thank You", "For Visiting Lantern Lane")
    S.append(Paragraph("If these puzzles kept you company, a short, honest review helps other puzzlers find the book. "
                       "Thank you for your pencil, your patience and your quiet hour.", ParagraphStyle("ty", parent=body, alignment=TA_CENTER)))
    S += [Spacer(1, 0.45 * inch),
          Paragraph("Also by Blake La Pierre", ParagraphStyle("ab", parent=body, alignment=TA_CENTER, fontName="PlayfairSC", fontSize=10, textColor=DARK)),
          Spacer(1, 6),
          Paragraph("<i>The Thief Stayed the Night</i> · <i>Frostwood Express</i> · <i>Stars over Frostwood</i> · <i>Tents in Frostwood</i> · <i>Fireside Cryptograms</i>",
                    ParagraphStyle("ab2", parent=small, fontSize=9.5, leading=13)),
          Spacer(1, 0.35 * inch), Art("thanks", TW, 1.5 * inch)]
    return S


def render(blank_before, out, toc):
    S = build(blank_before)
    if toc.get("_odd"):
        S += [PageBreak(), Kind("blank")]
    for i, x in enumerate(S):
        if isinstance(x, tuple) and x[0] == "TOC":
            rows = [("How to Solve", toc.get("howto", 0)), ("A Worked Example", toc.get("example", 0))]
            for b in BANDS:
                part, line, _ = PARTS[b]
                ps = D[b]
                rows.append((f"{part} · {line}<br/><font size='9.5' color='#6b6b6b'>{b} · Puzzles {ps[0]['num']}–{ps[-1]['num']}</font>", toc.get(b, 0)))
            rows += [("Hints", toc.get("hints", 0)), ("Solutions", toc.get("solutions", 0))]
            t = Table([[Paragraph(a, ParagraphStyle("tc", parent=body, fontSize=11.5, leading=14)), str(b)] for a, b in rows],
                      colWidths=[TW - 0.5 * inch, 0.5 * inch])
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Crimson", 11), ("FONT", (1, 0), (1, -1), "Crimson", 11.5), ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), 0.3, LINE),
                                   ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
            S[i] = t
    fr = Frame(INNER, BOT, TW, TH, id="f", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc = Doc(out, pagesize=(W, H), initialFontName="Crimson", title="Logic on Lantern Lane: 120 Cozy Logic Grid Puzzles",
              author="Blake La Pierre", subject="Logic grid puzzle book",
              pageTemplates=[PageTemplate("normal", [fr], onPageEnd=page_end)])
    doc.pkind, doc.marks, doc.section = {}, {}, ""
    doc.build(S)
    return doc.marks, doc.page


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", OUTNAME)
    fix, toc = set(), {}
    care = {"howto", "hints", "solutions", "contents", "about", "example", "Easy", "Medium", "Hard", "Expert"}
    for it in range(14):
        marks, pages = render(fix, out, toc)
        bad = [k for k, p in marks.items() if k in care and p % 2 == 0]
        # Expert spreads must start on a left-hand (even) page
        marks["_odd"] = toc.get("_odd", False) ^ (pages % 2 == 1)
        if not bad and marks.get("_odd") == toc.get("_odd", False) and all(toc.get(k) == marks.get(k) for k in care):
            toc = marks
            break
        fix ^= set(bad)
        toc = marks
    bad_exp = [k for k, p in toc.items() if str(k).startswith("exp") and p % 2 == 1]
    assert not bad_exp, bad_exp
    info = {"pages": pages, "marks": {k: v for k, v in toc.items() if not str(k).startswith(("_", "exp"))}}
    json.dump(info, open(os.path.join(HERE, "..", "build-info.json"), "w"), indent=1)
    print(json.dumps(info, indent=1))
    print(f"Wrote {out} ({pages} pages)")
