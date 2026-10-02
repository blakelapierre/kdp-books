"""Builds the 6x9 interior PDF (grayscale, no bleed, mirrored margins, embedded fonts).
Same fonts / palette / page furniture as 'The Thief Stayed the Night' (companion series)."""
import json, sys, math, random
sys.path.insert(0, ".")
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
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
assert len(ALL) == 200 and [p["num"] for p in ALL] == list(range(1, 201))

W, H = 6 * inch, 9 * inch
INNER, OUTER, TOP, BOT = 0.75 * inch, 0.55 * inch, 0.7 * inch, 0.75 * inch
DARK = colors.Color(0.17, 0.17, 0.17); MID = colors.Color(0.45, 0.45, 0.45); FROST = colors.Color(0.62, 0.62, 0.62)
ICE = colors.Color(0.925, 0.925, 0.925); INK = colors.Color(0.1, 0.1, 0.1); GRIDC = colors.Color(0.55, 0.55, 0.55)
TITLE = "Frostwood Express"
TW = W - INNER - OUTER; TH = H - TOP - BOT

PARTS = {  # band: (part, line name, snowflakes, blurb)
 "Easy": ("Part One", "The Foothills Line", 1, "Six-by-six grids to warm up on. The counts and the given pieces do most of the work; look for full rows, empty rows and dead ends."),
 "Medium": ("Part Two", "The Silverbrook Viaduct", 2, "Eight-by-eight grids with fewer pieces to lean on. Watch for track that would close into a loop, and for the crossing rule on the How to Play page."),
 "Hard": ("Part Three", "Frostwood Pass", 3, "Ten-by-ten grids. Every one of these needs the crossing rule at least once: count the track that must cross each line between two rows or columns."),
 "Expert": ("Part Four", "The Summit Run", 4, "Twelve-by-twelve grids with only a handful of pieces. Somewhere in each one you will probably need to ask “what if this square were track?” and follow it to a contradiction."),
}

# ---- station names: one stop on the line per puzzle
def stations():
    a = ("Pine Birch Larch Cedar Alder Rowan Aspen Hazel Holly Juniper Spruce Willow Maple Ash Elder Fir Hemlock Linden Oak Yew "
         "Frost Snow Ice Rime Hoar Winter Silver Crystal Cloud Mist Starling Robin Wren Finch Lark Owl Heron Otter Badger Fox").split()
    b = ("Hollow Crossing Junction Halt Siding Brook Falls Ridge Meadow Glen Summit Bend Cutting Tunnel Bridge Hill Vale Moor Ford Lake").split()
    r = random.Random(2026); out = []; seen = set()
    while len(out) < 200:
        s = f"{r.choice(a)} {r.choice(b)}"
        if s in seen or s.split()[0] in {x.split()[0] for x in out[-6:]}: continue
        seen.add(s); out.append(s)
    return out
STATION = stations()

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

def page_end(c, doc):
    p = doc.page; kind = getattr(doc, "pkind", {}).get(p, "normal")
    if kind in ("blank", "title", "nofolio"): return
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
h2 = ParagraphStyle("h2", fontName="PlayfairSC-B", fontSize=12.5, leading=15, textColor=DARK, spaceBefore=4, spaceAfter=1)
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

# ------------------------------------------------------------------ grid drawing
DV = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}

def draw_rails(c, cx, cy, s, piece, rail=DARK, tie=colors.Color(.6, .6, .6)):
    """A railway piece (two rails + sleepers) centred at (cx, cy) in a cell of size s."""
    d1, d2 = piece[0], piece[1]
    g = 0.17 * s; tl = 0.31 * s
    c.saveState(); c.setLineCap(0)
    if set(piece) in ({"N", "S"}, {"E", "W"}):
        vx, vy = DV[d1] if d1 in "NS" else (1, 0)
        if set(piece) == {"N", "S"}: vx, vy = 0, 1
        px, py = -vy, vx
        c.setStrokeColor(tie); c.setLineWidth(0.085 * s)
        for k in (-1, 0, 1):
            t = k * s / 3; c.line(cx + vx * t - px * tl, cy + vy * t - py * tl, cx + vx * t + px * tl, cy + vy * t + py * tl)
        c.setStrokeColor(rail); c.setLineWidth(0.05 * s)
        for o in (-g, g):
            c.line(cx - vx * s / 2 + px * o, cy - vy * s / 2 + py * o, cx + vx * s / 2 + px * o, cy + vy * s / 2 + py * o)
    else:
        a1, a2 = DV[d1], DV[d2]
        kx, ky = cx + (a1[0] + a2[0]) * s / 2, cy + (a1[1] + a2[1]) * s / 2       # corner of the cell
        t1 = math.degrees(math.atan2(-a1[1], -a1[0])); t2 = math.degrees(math.atan2(-a2[1], -a2[0]))
        ext = ((t2 - t1 + 180) % 360) - 180
        c.setStrokeColor(tie); c.setLineWidth(0.085 * s)
        for k in range(3):
            th = math.radians(t1 + ext * (k + 0.5) / 3)
            c.line(kx + (s / 2 - tl) * math.cos(th), ky + (s / 2 - tl) * math.sin(th), kx + (s / 2 + tl) * math.cos(th), ky + (s / 2 + tl) * math.sin(th))
        c.setStrokeColor(rail); c.setLineWidth(0.05 * s)
        for rr in (s / 2 - g, s / 2 + g):
            c.arc(kx - rr, ky - rr, kx + rr, ky + rr, t1, ext)
    c.restoreState()

def pieces_of(p):
    n = p["n"]; path = [tuple(x) for x in p["solution"]]; out = {}
    D4 = {(-1, 0): "N", (1, 0): "S", (0, -1): "W", (0, 1): "E"}
    for i, (r, c) in enumerate(path):
        ds = ["W"] if i == 0 else [D4[(path[i - 1][0] - r, path[i - 1][1] - c)]]
        ds.append("S" if i == len(path) - 1 else D4[(path[i + 1][0] - r, path[i + 1][1] - c)])
        out[(r, c)] = "".join(ds)
    return out

def draw_grid(c, x0, y0, s, p, mode="puzzle", edges=None, xs=(), labels=True, fs=None):
    """(x0, y0) = lower-left corner of the grid. mode: puzzle | solution | partial (edges = list of cell pairs)."""
    n = p["n"]; top = y0 + n * s
    fs = fs or min(13, max(5.5, s * 0.46))
    givens = {divmod(int(k), n): v for k, v in p["givens"].items()}
    X = lambda cc: x0 + cc * s + s / 2; Y = lambda r: top - r * s - s / 2
    c.saveState()
    if mode == "solution":
        c.setFillColor(ICE)
        for (r, cc) in givens: c.rect(x0 + cc * s, top - (r + 1) * s, s, s, stroke=0, fill=1)
    c.setStrokeColor(GRIDC); c.setLineWidth(0.5 if s > 12 else 0.3)
    for i in range(1, n):
        c.line(x0 + i * s, y0, x0 + i * s, top); c.line(x0, y0 + i * s, x0 + n * s, y0 + i * s)
    # entry / exit stubs
    er, ec = p["er"], p["ec"]
    stub = 0.55 * s
    if mode == "solution":
        c.setStrokeColor(INK); c.setLineWidth(max(1.2, s * 0.16)); c.setLineCap(1); c.setLineJoin(1)
        pts = [(x0 - stub, Y(er))] + [(X(cc), Y(r)) for r, cc in p["solution"]] + [(X(ec), y0 - stub)]
        pa = c.beginPath(); pa.moveTo(*pts[0])
        for q in pts[1:]: pa.lineTo(*q)
        c.drawPath(pa, stroke=1, fill=0)
    else:
        c.saveState(); cp = c.beginPath(); cp.rect(x0 - stub, Y(er) - s, stub, 2 * s); cp.rect(X(ec) - s, y0 - stub, 2 * s, stub)
        c.clipPath(cp, stroke=0, fill=0)
        draw_rails(c, x0 - s / 2, Y(er), s, "EW"); draw_rails(c, X(ec), y0 - s / 2, s, "NS")
        c.restoreState()
        for (r, cc), pc in givens.items(): draw_rails(c, X(cc), Y(r), s, pc)
        if edges:
            c.setStrokeColor(INK); c.setLineWidth(max(1.2, s * 0.12)); c.setLineCap(1)
            for (a, b) in edges:
                ax, ay = (x0 - s / 2, Y(a[0])) if a[1] < 0 else ((X(a[1]), y0 - s / 2) if a[0] >= n else (X(a[1]), Y(a[0])))
                bx, by = (X(b[1]), y0 - s / 2) if b[0] >= n else (X(b[1]), Y(b[0]))
                c.line(ax, ay, bx, by)
        c.setStrokeColor(MID); c.setLineWidth(max(0.8, s * 0.05))
        for (r, cc) in xs:
            d = s * 0.16; c.line(X(cc) - d, Y(r) - d, X(cc) + d, Y(r) + d); c.line(X(cc) - d, Y(r) + d, X(cc) + d, Y(r) - d)
    c.setStrokeColor(DARK); c.setLineWidth(1.3 if s > 12 else 0.8); c.rect(x0, y0, n * s, n * s)
    # counts: columns on top, rows on the right
    c.setFillColor(INK); c.setFont("Plex-M", fs)
    for i in range(n):
        c.drawCentredString(X(i), top + s * 0.22 + (0 if s > 12 else 1), str(p["cols"][i]))
        c.drawCentredString(x0 + n * s + s * 0.45 + (0 if s > 12 else 1), Y(i) - fs * 0.35, str(p["rows"][i]))
    if labels:
        c.setFont("PlayfairSC-B", fs * 0.95); c.setFillColor(DARK)
        c.drawRightString(x0 - stub - 3, Y(er) - fs * 0.35, "A")
        c.drawCentredString(X(ec), y0 - stub - fs * 0.95, "B")
    c.restoreState()

def stars(c, x, y, k, r=4.2, gap=11, right=True):
    for i in range(4):
        xx = x - (3 - i) * gap if right else x + i * gap
        snowflake(c, xx, y, r, DARK if i < k else colors.Color(.78, .78, .78), lw=0.12)

class PuzzleBlock(Flowable):
    """One puzzle with its header, centred in a box of height h."""
    def __init__(s, p, h, cell):
        s.p = p; s.h = h; s.cell = cell; s.width = TW; s.height = h
    def wrap(s, aw, ah): return TW, s.h
    def draw(s):
        c = s.canv; p = s.p; n = p["n"]; cs = s.cell
        gw = n * cs
        block = 0.36 * inch + cs * 0.9 + gw + cs * 1.2          # header, col counts, grid, exit label
        ytop = s.h - (s.h - block) / 2 + (14 if s.h > TH / 2 else 0)
        # header row
        c.setFillColor(DARK); c.setFont("PlayfairSC-B", 15); c.drawString(0, ytop - 13, f"No. {p['num']}")
        wno = pdfmetrics.stringWidth(f"No. {p['num']}", "PlayfairSC-B", 15)
        c.setFont("Crimson-I", 10.5); c.setFillColor(MID); c.drawString(wno + 8, ytop - 13, STATION[p["num"] - 1])
        k = PARTS[p["band"]][2]
        stars(c, TW - 5, ytop - 9, k)
        c.setFont("Plex", 7.5); c.setFillColor(MID); c.drawRightString(TW - 50, ytop - 12, f"{p['band'].upper()} · {n}×{n}")
        c.setStrokeColor(FROST); c.setLineWidth(0.5); c.line(0, ytop - 20, TW, ytop - 20)
        x0 = (TW - gw) / 2 + cs * 0.1
        y0 = ytop - 0.36 * inch - cs * 0.9 - gw
        draw_grid(c, x0, y0, cs, p)
        if s.h > TH / 2:
            yb = 6; c.setStrokeColor(FROST); c.setLineWidth(0.5); c.line(0, yb + 16, TW, yb + 16)
            c.setFont("PlayfairSC", 8.5); c.setFillColor(MID)
            c.drawString(0, yb, "Departed"); c.line(44, yb - 1, 124, yb - 1)
            c.drawString(150, yb, "Arrived"); c.line(186, yb - 1, 266, yb - 1)
            c.drawRightString(TW - 14, yb, "On time"); c.rect(TW - 9, yb - 1, 8, 8, stroke=1, fill=0)

class SolutionBlock(Flowable):
    def __init__(s, p, w, h, cell): s.p = p; s.width = w; s.height = h; s.cell = cell
    def wrap(s, aw, ah): return s.width, s.height
    def draw(s):
        c = s.canv; p = s.p; n = p["n"]; cs = s.cell; gw = n * cs
        c.setFont("PlayfairSC-B", 10); c.setFillColor(DARK)
        c.drawString(0, s.height - 10, f"No. {p['num']}")
        x0 = (s.width - gw) / 2 - cs * 0.1; y0 = s.height - 16 - cs * 1.0 - gw
        draw_grid(c, x0, y0, cs, p, mode="solution", labels=False, fs=max(5.2, min(7.5, cs * 0.62)))

class Example(Flowable):
    """Three panels for the worked example."""
    def __init__(s, panels, cell, cap):
        s.panels = panels; s.cell = cell; s.cap = cap; s.width = TW; s.height = cell * (EX["n"] + 2.3) + 16
    def wrap(s, aw, ah): return TW, s.height
    def draw(s):
        c = s.canv; n = EX["n"]; cs = s.cell; k = len(s.panels)
        lab = 14; core = 0.55 * cs + n * cs + 0.85 * cs
        widths = [lab + core] + [core] * (k - 1)
        gap = (TW - sum(widths)) / (k - 1); x = 0
        for i, (mode, edges, xs) in enumerate(s.panels):
            x0 = x + (lab if i == 0 else 0) + 0.55 * cs; y0 = 16 + cs * 1.2
            draw_grid(c, x0, y0, cs, EX, mode=mode, edges=edges, xs=xs, fs=7.5, labels=(i == 0))
            c.setFont("Crimson-I", 9); c.setFillColor(MID); c.drawCentredString(x0 + n * cs / 2, 2, s.cap[i])
            x += widths[i] + gap

class RailArt(Flowable):
    """Line-art title vignette: mountains, a viaduct and a little train (grayscale)."""
    def __init__(s, w, h, seed=7, lodge=True): s.width, s.height = w, h; s.seed = seed; s.lodge = lodge
    def draw(s):
        c = s.canv; w, h = s.width, s.height; r = random.Random(s.seed)
        for _ in range(14):
            snowflake(c, r.uniform(0.05, 0.95) * w, r.uniform(0.62, 0.98) * h, r.uniform(3, 7), colors.Color(.72, .72, .72))
        c.setStrokeColor(MID); c.setLineWidth(1.1); c.setLineJoin(1)
        pts = [(0, 0.30), (0.16, 0.62), (0.30, 0.44), (0.50, 0.82), (0.70, 0.46), (0.84, 0.64), (1.0, 0.36)]
        pa = c.beginPath(); pa.moveTo(pts[0][0] * w, pts[0][1] * h * 0.75)
        for x, y in pts[1:]: pa.lineTo(x * w, y * h * 0.75)
        c.drawPath(pa, stroke=1, fill=0)
        if s.lodge:   # the lodge from book one, tiny, up on the summit
            lx, ly = 0.5 * w, 0.82 * h * 0.75 - 2
            c.setFillColor(colors.white); c.setStrokeColor(DARK); c.setLineWidth(0.8)
            c.rect(lx - 14, ly - 16, 28, 14, stroke=1, fill=1)
            pa = c.beginPath(); pa.moveTo(lx - 17, ly - 2); pa.lineTo(lx, ly + 7); pa.lineTo(lx + 17, ly - 2); pa.close(); c.drawPath(pa, stroke=1, fill=1)
            for i in range(4): c.setFillColor(DARK); c.rect(lx - 11 + i * 6, ly - 11, 3, 4, stroke=0, fill=1)
        # viaduct
        base = 0.0; deck = 0.22 * h
        c.setStrokeColor(DARK); c.setLineWidth(1.2); c.line(0, deck, w, deck); c.line(0, deck - 5, w, deck - 5)
        span = w / 6
        c.setLineWidth(0.9)
        for i in range(6):
            x = i * span; c.arc(x + 6, base - span * 0.35, x + span - 6, deck - 9, 0, 180)
        for i in range(7): c.line(i * span, base, i * span, deck - 5)
        c.line(-0.1 * inch, base, w + 0.1 * inch, base)
        # ties on deck
        c.setLineWidth(0.6); c.setStrokeColor(MID)
        for i in range(int(w / 7)): c.line(i * 7 + 2, deck, i * 7 + 2, deck + 3)
        c.setStrokeColor(DARK); c.setLineWidth(0.9); c.line(0, deck + 3, w, deck + 3)
        # train
        tx = 0.28 * w; ty = deck + 4
        c.setFillColor(colors.white); c.setStrokeColor(DARK); c.setLineWidth(1)
        for k in range(3):   # carriages
            x = tx + 62 + k * 44
            c.roundRect(x, ty + 3, 40, 18, 2.5, stroke=1, fill=1)
            for j in range(3): c.setFillColor(DARK); c.rect(x + 5 + j * 11.5, ty + 11, 7, 6, stroke=0, fill=1); c.setFillColor(colors.white)
            c.circle(x + 9, ty + 3, 3, stroke=1, fill=1); c.circle(x + 31, ty + 3, 3, stroke=1, fill=1)
        c.rect(tx + 8, ty + 3, 52, 14, stroke=1, fill=1)             # boiler
        c.rect(tx + 40, ty + 3, 20, 25, stroke=1, fill=1)            # cab
        c.setFillColor(DARK); c.rect(tx + 44, ty + 19, 12, 6, stroke=0, fill=1)
        c.setFillColor(colors.white); c.rect(tx + 14, ty + 17, 7, 9, stroke=1, fill=1)   # chimney
        pa = c.beginPath(); pa.moveTo(tx + 8, ty + 3); pa.lineTo(tx, ty + 3); pa.lineTo(tx + 8, ty + 12); pa.close(); c.drawPath(pa, stroke=1, fill=1)
        for wx in (tx + 16, tx + 30, tx + 50): c.circle(wx, ty + 3, 4.2, stroke=1, fill=1)
        c.setFillColor(colors.Color(.85, .85, .85)); c.setStrokeColor(colors.Color(.6, .6, .6))
        for k, (dx, dy, rr) in enumerate([(18, 33, 5), (10, 42, 7), (-2, 50, 9)]): c.circle(tx + dx, ty + dy, rr, stroke=1, fill=1)

# ------------------------------------------------------------------ worked example panels
def ex_panels():
    path = [tuple(x) for x in EX["solution"]]; n = EX["n"]
    def E(cells): return list(zip(cells, cells[1:]))
    exit_seg = [((3, 2), (3, 1)), ((3, 1), (3, 0)), ((3, 0), (4, 0)), ((4, 0), (5, 0))]
    entry_seg = [((1, -1), (1, 0)), ((1, 0), (0, 0)), ((0, 0), (0, 1)), ((0, 1), (0, 2))]
    xs_mid = [(4, 1), (4, 2), (4, 3), (4, 4), (1, 1), (2, 1), (2, 0), (3, 3), (3, 4), (0, 3), (0, 4)]
    return [("puzzle", None, ()), ("partial", entry_seg + exit_seg, xs_mid), ("solution", None, ())]

# ------------------------------------------------------------------ the book
def build(recto_fix):
    S = []
    def recto(tag):
        S.append(PageBreak())
        if tag in recto_fix: S.extend([Kind("blank"), PageBreak()])
        S.append(Kind(mark=tag))
    S += [Kind("title"), Spacer(1, 0.5 * inch), Paragraph("A Snowy Mountain Railway Puzzle Book", ParagraphStyle("t0", parent=kick, fontSize=11, textColor=MID)),
          Spacer(1, 10), Paragraph("Frostwood<br/>Express", ParagraphStyle("tt", fontName="PlayfairSC-B", fontSize=38, leading=42, alignment=TA_CENTER, textColor=DARK)),
          Spacer(1, 14), Paragraph("200 Train Tracks logic puzzles<br/>from the foothills to the summit", ParagraphStyle("t2", parent=small, fontSize=13, leading=17)),
          Spacer(1, 0.45 * inch), RailArt(TW, 2.6 * inch), Spacer(1, 0.45 * inch),
          Paragraph("A Frostwood Puzzle Book", ParagraphStyle("t3", parent=kick, fontSize=10, textColor=DARK)),
          Paragraph("Blake La Pierre", ParagraphStyle("t4", parent=small, fontSize=11))]
    S += [PageBreak(), Kind("nofolio"), Spacer(1, 3.6 * inch)]
    cs = ParagraphStyle("cp", parent=body0, fontSize=9, leading=12, alignment=TA_LEFT)
    for t in ["<i>Frostwood Express: 200 Train Tracks Logic Puzzles</i>",
              "Copyright © 2026 Blake La Pierre. All rights reserved.",
              "No part of this book may be reproduced in any form without written permission from the author, except for brief quotations in reviews. Readers are welcome to photocopy puzzle pages for their own personal use while solving.",
              "The Frostwood Express, its line and its stations are imaginary. Any resemblance to real railways is coincidental.",
              "First edition, 2026",
              "Set in Crimson Text, Playfair Display SC and IBM Plex Sans Condensed, used under the SIL Open Font License."]:
        S += [Paragraph(t, cs), Spacer(1, 6)]
    recto("contents")
    S += [Kind(section="Contents"), Spacer(1, 0.3 * inch)] + heading("Frostwood Express", "Contents")
    S.append(("TOC",))
    S += [Spacer(1, 0.35 * inch), Paragraph("All aboard. The Frostwood Express climbs from the valley to the old lodge on the mountain, and the snow has "
          "buried the timetable, the signals and most of the track. Two hundred stretches of line need re-laying before the next train can run. "
          "Every puzzle has exactly one solution, and every one can be solved by logic alone, with no guessing.", ParagraphStyle("in", parent=small, fontSize=10.5, leading=14))]
    # how to play
    recto("howto")
    S += [Kind(section="How to Play"), Spacer(1, 0.1 * inch)] + heading("Before You Board", "How to Play")[:-1] + [Spacer(1, 4)]
    hb = ParagraphStyle("hb", parent=bullet, fontSize=10.5, leading=13.6, spaceAfter=2.5)
    for t in ["Each puzzle is a map of a stretch of line, drawn as a grid of squares. Your job is to lay <b>one continuous railway track</b> through the grid, "
              "square by square, following these rules:"]:
        S += [Paragraph(t, ParagraphStyle("hb0", parent=body0, fontSize=10.8, leading=14)), Spacer(1, 3)]
    for t in ["The track enters the grid at <b>A</b>, on the left edge, and leaves it at <b>B</b>, on the bottom edge.",
              "Every square is either <b>track</b> or <b>empty</b>. A track square holds a straight piece or a curve: it joins exactly two of its four sides. "
              "The track never branches, never crosses itself and never forms a closed loop.",
              "The number above each column and beside each row tells you <b>how many squares</b> in that column or row contain track.",
              "Some pieces of track are already laid for you. They are part of the answer, exactly as drawn.",
              "Track squares may sit side by side without being joined. Only the pieces you draw connect them."]:
        S.append(Paragraph(FL + t, hb))
    S += [Spacer(1, 4), Paragraph("<b>Useful Tricks</b>", ParagraphStyle("x", parent=body0, alignment=TA_CENTER, textColor=DARK)), Spacer(1, 3)]
    for t in ["<b>Full and finished lines.</b> When a row or column already has as many track squares as its number, mark every other square in it with a small ×. "
              "When it has only just enough undecided squares left, they must all be track.",
              "<b>Dead ends.</b> A track square needs two exits. If a square can reach only one neighbour that is not ruled out, it cannot be track.",
              "<b>No loops, no shortcuts.</b> Never join two ends of the same piece of track. And don’t join the piece that starts at A to the piece that ends at B until every row and column total is met.",
              "<b>The crossing rule.</b> Draw an imaginary line between two neighbouring columns. The track starts on the left of it at A. If B is on the right, "
              "the track must cross that line an <i>odd</i> number of times; if B is on the left, an <i>even</i> number. The same works between two rows: "
              "the crossings are odd if A is above the line and even if A is below it. When all the crossings but one are known, the last one is decided.",
              "<b>What if?</b> In the Expert puzzles, you may have to suppose a square is track, follow the consequences, and see the rules break. "
              "Then you know that square is empty."]:
        S.append(Paragraph(FL + t, hb))
    S += [PageBreak(), Kind(section="How to Play"), Spacer(1, 0.05 * inch)] + heading("Let’s Lay Some Track", "A Worked Example")
    S.append(Example(ex_panels(), 0.22 * inch, ["The puzzle", "Halfway there", "Solved"]))
    S.append(Spacer(1, 8))
    S.append(Paragraph("Rows are numbered from the top and columns from the left. Here is one way to solve it:", ParagraphStyle("exi", parent=body0, fontSize=10.4, leading=13.4, spaceAfter=3)))
    ex = ParagraphStyle("exs", parent=bullet, fontSize=10.4, leading=13.4, spaceAfter=2.5)
    for i, t in enumerate([
        "<b>Row 5 (the bottom row) needs 1 square.</b> The square above B is track, because the track leaves the grid there, so the other four squares of row 5 are empty. "
        "That square can only continue upward, into row 4.",
        "<b>The curve in row 4</b> joins the square to its left and the square above it, so row 4 already has three track squares: its first three. "
        "The last two squares of row 4 are empty.",
        "<b>Column 2 needs 2.</b> The curve at the top points left, into column 2, and the track in row 4 is in column 2 too. That makes two, so the middle "
        "squares of column 2 are empty. The track in row 4 therefore runs straight across to column 1 and turns down to B.",
        "<b>Column 1 needs 4.</b> A, row 4 and row 5 are three. The fourth is either row 1 or row 3. Row 3 would be a dead end (its only open neighbour is A), so it is empty, "
        "and row 1 is track: A turns up, then right into the top curve. Row 1 now has its 3, so its last two squares are empty. That is the middle picture.",
        "<b>Finish.</b> Column 3 needs all four of its top squares. Joining the two loose ends straight down the middle of column 3 would link A to B far too early, "
        "so both turn right instead. Column 4 has its 2, row 2 needs one more square at the far right, and the last three pieces fall into place.",
    ], 1):
        S.append(Paragraph(f"<font name='PlayfairSC-B' color='#2b2b2b'>{i}.</font>&nbsp;&nbsp;" + t, ex))
    S.append(Spacer(1, 4))
    S.append(Paragraph("Solutions are at the back of the book, with every pre-laid piece shaded.", ParagraphStyle("sm2", parent=small, fontSize=9.5)))
    # puzzles
    for band in BANDS:
        part, line, k, blurb = PARTS[band]; ps = D[band]; n = ps[0]["n"]
        recto(band)
        S += [Kind("opener"), Kind(section=f"{part} · {line}"), Spacer(1, 1.3 * inch)] + heading(f"{part} · {band} · {n}×{n}", line)
        S += [Paragraph(f"Puzzles {ps[0]['num']} to {ps[-1]['num']}", ParagraphStyle("pn", parent=small, fontSize=11)), Spacer(1, 14),
              Paragraph(blurb, ParagraphStyle("bl", parent=small, fontSize=11, leading=15)), Spacer(1, 0.5 * inch), RailArt(TW, 1.9 * inch, seed=k + 10, lodge=(band == "Expert"))]
        S.append(PageBreak())
        if n <= 8:
            cell = 0.40 * inch if n == 6 else 0.325 * inch
            for i in range(0, len(ps), 2):
                S += [PuzzleBlock(ps[i], TH / 2 - 1, cell), PuzzleBlock(ps[i + 1], TH / 2 - 1, cell), PageBreak()]
        else:
            cell = 0.40 * inch if n == 10 else 0.335 * inch
            for p in ps: S += [PuzzleBlock(p, TH - 2, cell), PageBreak()]
        S.pop()
    # solutions
    recto("solutions")
    S += [Kind("opener"), Kind(section="Solutions"), Spacer(1, 2.4 * inch)] + heading("End of the Line", "Solutions")
    S.append(Paragraph("Each solution shows the complete track from A to B. The squares that were already laid in the puzzle are shaded.", small))
    for group in (("Easy", "Medium"), ("Hard", "Expert")):
        ps = [p for b in group for p in D[b]]; n = max(p["n"] for p in ps)
        cols, rows = (3, 4) if n <= 8 else (2, 3)
        per = cols * rows; bw = TW / cols; bh = (TH - 4) / rows
        for i in range(0, len(ps), per):
            chunk = ps[i:i + per]
            S += [PageBreak(), Kind(section=f"Solutions · Nos. {chunk[0]['num']}–{chunk[-1]['num']}")]
            grid = []
            for r in range(rows):
                row = []
                for j in range(i + r * cols, i + r * cols + cols):
                    if j < len(ps):
                        m = ps[j]["n"]; cell = min((bw - 26) / (m + 1), (bh - 34) / (m + 1))
                        row.append(SolutionBlock(ps[j], bw - 6, bh - 4, cell))
                    else: row.append("")
                grid.append(row)
            t = Table(grid, colWidths=[bw] * cols, rowHeights=[bh] * rows)
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Crimson", 10), ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3), ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            S.append(t)
    # back matter
    recto("about")
    S += [Kind("nofolio"), Spacer(1, 1.4 * inch)] + heading("Thank You for Riding", "The Frostwood Express")
    S.append(Paragraph("If you enjoyed laying track through the snow, a short review helps other puzzlers find the book. "
                       "The conductor reads every one, usually over a cup of cocoa in the summit waiting room.", ParagraphStyle("ty", parent=body0, alignment=TA_CENTER)))
    S += [Spacer(1, 0.5 * inch), Flake(), Spacer(1, 10), Paragraph("Also by Blake La Pierre", ParagraphStyle("ab", parent=kick, fontSize=11, textColor=DARK)), Spacer(1, 4),
          Paragraph("<i>The Thief Stayed the Night</i>", ParagraphStyle("ab2", parent=body0, alignment=TA_CENTER, fontSize=13)),
          Paragraph("A snowbound hotel mystery puzzle book. Twelve cozy elimination cases at the Frostwood Lodge, at the top of the line.", ParagraphStyle("ab3", parent=small))]
    S.append(("PAD",))
    return S

def render(recto_fix, out, toc):
    S = build(recto_fix)
    if toc.get("_odd"): S += [PageBreak(), Kind("blank")]
    for i, x in enumerate(S):
        if x == ("PAD",):
            S[i] = Spacer(0, 0); continue
        if isinstance(x, tuple):
            rows = [("How to Play", toc.get("howto", 0)), ("A Worked Example", toc.get("howto", 0) + 1)]
            for b in BANDS:
                part, line, k, _ = PARTS[b]; ps = D[b]
                rows.append((f"{part} · {line}<br/><font size='9.5' color='#737373'>{b} · {ps[0]['n']}×{ps[0]['n']} · Puzzles {ps[0]['num']}–{ps[-1]['num']}</font>", toc.get(b, 0)))
            rows += [("Solutions", toc.get("solutions", 0))]
            t = Table([[Paragraph(a, ParagraphStyle("tc", parent=body0, fontSize=11.5, leading=14)), str(b)] for a, b in rows], colWidths=[TW - 0.5 * inch, 0.5 * inch])
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Crimson", 11), ("FONT", (1, 0), (1, -1), "Crimson", 11.5), ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), 0.3, FROST), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
            S[i] = t
    fr = Frame(INNER, BOT, TW, TH, id="f", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc = Doc(out, pagesize=(W, H), initialFontName="Crimson", title="Frostwood Express: 200 Train Tracks Logic Puzzles", author="Blake La Pierre",
              subject="Train Tracks logic puzzle book", pageTemplates=[PageTemplate("normal", [fr], onPageEnd=page_end)])
    doc.pkind = {}; doc.marks = {}; doc.section = ""
    doc.build(S)
    return doc.marks, doc.page

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "../interior.pdf"
    fix = set(); toc = {}
    for it in range(40):
        marks, pages = render(fix, out, toc)
        bad = sorted((p, k) for k, p in marks.items() if p % 2 == 0)
        marks["_odd"] = toc.get("_odd", False) ^ (pages % 2 == 1)   # pad to an even page count
        if not bad and marks == toc: break
        if bad: fix ^= {bad[0][1]}
        toc = marks
    marks.pop("_odd", None)
    print("pages", pages, "marks", marks)
    json.dump(dict(pages=pages, marks=marks), open("../build-info.json", "w"))
