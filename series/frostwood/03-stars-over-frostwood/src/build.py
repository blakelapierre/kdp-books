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
TITLE = "Stars over Frostwood"
TW = W - INNER - OUTER; TH = H - TOP - BOT

PARTS = {  # band: (part, place, snowflakes, blurb)
 "Easy": ("Part One", "The Village Green", 1, "Six-by-six skies with one star in every row, column and region. Start with the smallest regions, and remember that stars never touch, not even at the corners."),
 "Medium": ("Part Two", "Along the Railway", 2, "Eight-by-eight skies, still one star each. Look for a region that fits entirely inside one row or column, and for squares that would touch every square of a small region."),
 "Hard": ("Part Three", "The Mountain Path", 3, "Ten-by-ten skies with two stars in every row, column and region. Each one needs you to count stars across several regions at once: two regions squeezed into two rows claim those rows."),
 "Expert": ("Part Four", "The Lodge Observatory", 4, "Ten-by-ten skies, two stars each, and the hardest in the book. Somewhere in each one you will probably need to ask “what if a star were here?” and follow it until the rules break."),
}

# ---- one named viewpoint per puzzle
def viewpoints():
    P = {"Easy": ("Bakery Lane|the Mill Pond|Chapel Green|the Skating Pond|Holly Cottage|the Old Bridge|Market Cross|the Post Office|Lantern Row|the Well|the Schoolhouse|Rowan Terrace|"
                  "the Duck Pond|Church Walk|the Tea Room|Bell Street|Ivy Corner|the Bookshop|the Green|Orchard Lane|the Weir|Cobble Yard|the Bandstand|Willow Close|the Forge|"
                  "Candle Lane|the Toll House|Fir Row|the Mill Race|the Almshouses|Pudding Lane|the Pump|Wren Cottage|the Village Hall|Snowdrop Lane|the Sheepfold|Fox Lane|the Inn Yard|Hazel Row|the Chestnut Tree"),
         "Medium": ("Frostwood Station|the Signal Box|Silverbrook Viaduct|Pine Hollow Halt|the Water Tower|Larch Cutting|the Engine Shed|Birch Siding|Cedar Junction|the Goods Yard|Aspen Tunnel|the Level Crossing|"
                    "Rowan Halt|the Turntable|Hemlock Bend|the Footbridge|Alder Siding|Spruce Falls|the Coal Stage|Juniper Halt|the Booking Hall|Owl Tunnel|Mistletoe Bend|the Waiting Room|Heron Brook|"
                    "the Points|Otter Ford|the Lamp Room|Badger Cutting|Fox Glen Halt|the Platform End|Kestrel Bridge|the Milk Dock|Elder Siding|Starling Halt|the Buffer Stop|Rime Cutting|the Ticket Office|Crystal Bend|Cloud Halt"),
         "Hard": ("the Lower Trail|Hoarfrost Ridge|the Shepherd’s Hut|Eagle Crag|the Tarn|Rowan Falls|the Scree|Juniper Col|the Waymarker|Pine Shoulder|the Snowfield|Lark Rise|the Cairn|Silver Beck|"
                  "the Hanging Valley|Aspen Spur|the Ice Fall|Heather Moor|the Boulder Field|Cloudberry Knoll|the Saddle|Winter Gully|the Stone Stile|Ptarmigan Ridge|the Frozen Tarn|Mist Crag|the Old Mine|"
                  "Hare Knoll|the Zigzags|Bilberry Slope|the Upper Trail|Fern Gill|the Watershed|Grouse Moor|the Col|Raven Rocks|the Long Traverse|Snow Bunting Ledge|the Refuge|Glacier Steps|"
                  "the Viewpoint|Frost Hollow|the Sheep Track|Blue Ice Gully|the Stone Man|Crowberry Edge|the Stream Crossing|White Hare Rise|the Last Bend|Summit Ridge"),
         "Expert": ("the Dome|the Great Telescope|the Star Ledger|the Roof Walk|the Brass Orrery|the Map Room|the Clock Room|the Sky Hatch|the Warm Room|the Finder Scope|the Night Log|the Chart Table|"
                    "the Eyepiece Case|the Weather Vane|the Library Stair|the Lamp Shelf|the Cocoa Urn|the Window Seat|the Guest Book|the North Window|the Tower Stair|the Pole Star Room|the Lens Cabinet|"
                    "the Attic|the Sky Globe|the Fireside|the Record Book|the Iron Stair|the Gallery|the East Window|the Star Chart|the Balcony|the Old Clock|the Brass Rail|the Watch Room|the Hearth|"
                    "the Snug|the Lantern Room|the Top Landing|the West Window|the Meridian Line|the Moon Chart|the Plate Chest|the Star Drawer|the Snow Porch|the Boot Room|the Dome Shutter|"
                    "the Midnight Bench|the Last Lamp|the Summit Dome")}
    out = []
    for b in BANDS:
        names = P[b].split("|"); assert len(names) >= len(D[b]), (b, len(names)); out += names[:len(D[b])]
    return out
VIEW = viewpoints()

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

def star(c, x, y, r, fill=DARK, stroke=None, lw=0.6, pts=5, inner=0.42):
    c.saveState(); p = c.beginPath()
    for i in range(2 * pts):
        a = math.pi / 2 + i * math.pi / pts; rr = r if i % 2 == 0 else r * inner
        (p.moveTo if i == 0 else p.lineTo)(x + rr * math.cos(a), y + rr * math.sin(a))
    p.close()
    c.setFillColor(fill)
    if stroke is not None: c.setStrokeColor(stroke); c.setLineWidth(lw); c.setLineJoin(1)
    c.drawPath(p, stroke=1 if stroke is not None else 0, fill=1); c.restoreState()

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
def draw_grid(c, x0, y0, s, p, mode="puzzle", stars=(), dots=(), labels=False, shade=None):
    """(x0, y0) = lower-left corner. mode puzzle | solution. stars/dots: lists of (r, c) to draw (partial panels)."""
    n = p["n"]; reg = p["regions"]; top = y0 + n * s
    X = lambda cc: x0 + cc * s + s / 2; Y = lambda r: top - r * s - s / 2
    c.saveState()
    if shade:
        c.setFillColor(ICE)
        for (r, cc) in shade: c.rect(x0 + cc * s, top - (r + 1) * s, s, s, stroke=0, fill=1)
    c.setStrokeColor(GRIDC); c.setLineWidth(0.4 if s > 12 else 0.25)
    for i in range(1, n):
        c.line(x0 + i * s, y0, x0 + i * s, top); c.line(x0, y0 + i * s, x0 + n * s, y0 + i * s)
    # region borders
    c.setStrokeColor(INK); c.setLineWidth(max(1.1, s * 0.075) if s > 12 else 0.9); c.setLineCap(2)
    for r in range(n):
        for cc in range(n):
            if cc + 1 < n and reg[r][cc] != reg[r][cc + 1]: c.line(x0 + (cc + 1) * s, top - r * s, x0 + (cc + 1) * s, top - (r + 1) * s)
            if r + 1 < n and reg[r][cc] != reg[r + 1][cc]: c.line(x0 + cc * s, top - (r + 1) * s, x0 + (cc + 1) * s, top - (r + 1) * s)
    c.setLineWidth(max(1.5, s * 0.09) if s > 12 else 1.1); c.setLineJoin(0); c.rect(x0, y0, n * s, n * s)
    st = [tuple(x) for x in p["solution"]] if mode == "solution" else list(stars)
    for (r, cc) in st: star(c, X(cc), Y(r) - s * 0.02, s * 0.36, fill=INK)
    c.setFillColor(MID)
    for (r, cc) in dots: c.circle(X(cc), Y(r), max(0.9, s * 0.07), stroke=0, fill=1)
    if labels:
        c.setFont("Plex", 7); c.setFillColor(MID)
        for i in range(n):
            c.drawCentredString(X(i), top + 3, str(i + 1)); c.drawRightString(x0 - 3, Y(i) - 2.4, str(i + 1))
    c.restoreState()

def rating(c, x, y, k, r=4.2, gap=11):
    for i in range(4):
        snowflake(c, x - (3 - i) * gap, y, r, DARK if i < k else colors.Color(.78, .78, .78), lw=0.12)

class PuzzleBlock(Flowable):
    def __init__(s, p, h, cell): s.p = p; s.h = h; s.cell = cell; s.width = TW; s.height = h
    def wrap(s, aw, ah): return TW, s.h
    def draw(s):
        c = s.canv; p = s.p; n = p["n"]; cs = s.cell; gw = n * cs
        full = s.h > TH / 2
        block = 0.36 * inch + 0.14 * inch + gw
        ytop = s.h - (s.h - block - (0.35 * inch if full else 0)) / 2 + (0 if full else 4)
        ytop = min(ytop, s.h)
        c.setFillColor(DARK); c.setFont("PlayfairSC-B", 15); c.drawString(0, ytop - 13, f"No. {p['num']}")
        wno = pdfmetrics.stringWidth(f"No. {p['num']}", "PlayfairSC-B", 15)
        c.setFont("Crimson-I", 10.5); c.setFillColor(MID); c.drawString(wno + 8, ytop - 13, {"Easy": "Over ", "Medium": "Over ", "Hard": "Above ", "Expert": "From "}[p["band"]] + VIEW[p["num"] - 1])
        rating(c, TW - 5, ytop - 9, PARTS[p["band"]][2])
        c.setFont("Plex", 7.5); c.setFillColor(MID)
        c.drawRightString(TW - 50, ytop - 12, f"{p['band'].upper()} · {n}×{n} · {p['k']} STAR{'S' if p['k'] > 1 else ''}")
        c.setStrokeColor(FROST); c.setLineWidth(0.5); c.line(0, ytop - 20, TW, ytop - 20)
        x0 = (TW - gw) / 2; y0 = ytop - 0.36 * inch - 0.14 * inch - gw
        draw_grid(c, x0, y0, cs, p)
        if full:
            yb = 6; c.setStrokeColor(FROST); c.setLineWidth(0.5); c.line(0, yb + 16, TW, yb + 16)
            c.setFont("PlayfairSC", 8.5); c.setFillColor(MID)
            c.drawString(0, yb, "Started"); c.line(40, yb - 1, 120, yb - 1)
            c.drawString(146, yb, "Finished"); c.line(190, yb - 1, 270, yb - 1)
            c.drawRightString(TW - 14, yb, "Clear skies"); star(c, TW - 5, yb + 3, 5, fill=colors.white, stroke=MID, lw=0.6)

class SolutionBlock(Flowable):
    def __init__(s, p, w, h, cell): s.p = p; s.width = w; s.height = h; s.cell = cell
    def wrap(s, aw, ah): return s.width, s.height
    def draw(s):
        c = s.canv; p = s.p; n = p["n"]; cs = s.cell; gw = n * cs
        c.setFont("PlayfairSC-B", 10); c.setFillColor(DARK); c.drawString(0, s.height - 10, f"No. {p['num']}")
        x0 = (s.width - gw) / 2; y0 = s.height - 16 - gw
        draw_grid(c, x0, y0, cs, p, mode="solution")

class Example(Flowable):
    def __init__(s, panels, cell, cap):
        s.panels = panels; s.cell = cell; s.cap = cap; s.width = TW; s.height = cell * EX["n"] + 30
    def wrap(s, aw, ah): return TW, s.height
    def draw(s):
        c = s.canv; n = EX["n"]; cs = s.cell; k = len(s.panels); gw = n * cs
        gap = (TW - k * gw - 12) / (k - 1); x = 12
        for i, (mode, stars_, dots) in enumerate(s.panels):
            draw_grid(c, x, 16, cs, EX, mode=mode, stars=stars_, dots=dots, labels=True)
            c.setFont("Crimson-I", 9); c.setFillColor(MID); c.drawCentredString(x + gw / 2, 2, s.cap[i])
            x += gw + gap

class SkyArt(Flowable):
    """Line-art vignette: mountains, the lodge with its observatory dome, stars and a crescent moon (grayscale)."""
    def __init__(s, w, h, seed=7, lodge=True, village=False, rail=False): s.width, s.height = w, h; s.seed = seed; s.lodge = lodge; s.village = village; s.rail = rail
    def draw(s):
        c = s.canv; w, h = s.width, s.height; r = random.Random(s.seed)
        for _ in range(18):
            x, y = r.uniform(0.04, 0.96) * w, r.uniform(0.6, 0.97) * h
            if r.random() < 0.55: star(c, x, y, r.uniform(2.2, 4.5), fill=colors.Color(.55, .55, .55))
            else: snowflake(c, x, y, r.uniform(2.5, 5.5), colors.Color(.72, .72, .72))
        # crescent moon
        mx, my, mr = 0.86 * w, 0.84 * h, 11
        c.setFillColor(colors.Color(.35, .35, .35)); c.circle(mx, my, mr, stroke=0, fill=1)
        c.setFillColor(colors.white); c.circle(mx + 5, my + 3, mr * 0.9, stroke=0, fill=1)
        c.setStrokeColor(MID); c.setLineWidth(1.1); c.setLineJoin(1)
        pts = [(0, 0.26), (0.16, 0.55), (0.30, 0.40), (0.50, 0.78), (0.70, 0.42), (0.84, 0.58), (1.0, 0.32)]
        pa = c.beginPath(); pa.moveTo(pts[0][0] * w, pts[0][1] * h * 0.75)
        for x, y in pts[1:]: pa.lineTo(x * w, y * h * 0.75)
        c.drawPath(pa, stroke=1, fill=0)
        if s.lodge:
            lx, ly = 0.5 * w, 0.78 * h * 0.75 - 2
            c.setFillColor(colors.white); c.setStrokeColor(DARK); c.setLineWidth(0.8)
            c.rect(lx - 16, ly - 16, 32, 14, stroke=1, fill=1)
            pa = c.beginPath(); pa.moveTo(lx - 19, ly - 2); pa.lineTo(lx - 2, ly + 7); pa.lineTo(lx + 15, ly - 2); pa.close(); c.drawPath(pa, stroke=1, fill=1)
            c.rect(lx + 9, ly - 2, 9, 8, stroke=1, fill=1)                    # tower
            c.wedge(lx + 6.5, ly + 1, lx + 20.5, ly + 15, 0, 180, stroke=1, fill=1)   # dome
            c.line(lx + 13.5, ly + 8, lx + 21, ly + 14)                         # telescope
            for i in range(4): c.setFillColor(DARK); c.rect(lx - 13 + i * 7, ly - 11, 3.4, 4, stroke=0, fill=1)
        base = 0.0
        c.setStrokeColor(DARK); c.setLineWidth(0.9); c.line(-0.1 * inch, base, w + 0.1 * inch, base)
        # pines along the foot
        for i in range(int(w / 26)):
            x = 8 + i * 26 + r.uniform(-5, 5); th = r.uniform(18, 30)
            if s.village and 0.3 * w < x < 0.7 * w: continue
            pa = c.beginPath(); pa.moveTo(x - th * 0.32, base); pa.lineTo(x, base + th); pa.lineTo(x + th * 0.32, base); pa.close()
            c.setFillColor(colors.white); c.setStrokeColor(MID); c.setLineWidth(0.8); c.drawPath(pa, stroke=1, fill=1)
        if s.rail:   # a stretch of the Frostwood line in front of the trees
            c.setFillColor(colors.white); c.setStrokeColor(colors.white); c.rect(-2, base + 0.5, w + 4, 9, stroke=0, fill=1)
            c.setStrokeColor(MID); c.setLineWidth(0.7)
            for i in range(int(w / 6) + 1): c.line(i * 6 + 1, base + 1, i * 6 + 1, base + 7)
            c.setStrokeColor(DARK); c.setLineWidth(0.9); c.line(0, base + 2.5, w, base + 2.5); c.line(0, base + 5.5, w, base + 5.5)
        if s.village:
            for j, (dx, bw, bh) in enumerate([(0.33, 30, 16), (0.43, 24, 20), (0.52, 34, 15), (0.62, 26, 18)]):
                x = dx * w; c.setFillColor(colors.white); c.setStrokeColor(DARK); c.setLineWidth(0.8)
                c.rect(x, base, bw, bh, stroke=1, fill=1)
                pa = c.beginPath(); pa.moveTo(x - 3, base + bh); pa.lineTo(x + bw / 2, base + bh + 10); pa.lineTo(x + bw + 3, base + bh); pa.close(); c.drawPath(pa, stroke=1, fill=1)
                c.setFillColor(DARK); c.rect(x + bw / 2 - 3, base + 5, 6, 5, stroke=0, fill=1)

# ------------------------------------------------------------------ worked example
from example_text import EX_PANELS, EX_STEPS

def build(recto_fix):
    S = []
    def recto(tag):
        S.append(PageBreak())
        if tag in recto_fix: S.extend([Kind("blank"), PageBreak()])
        S.append(Kind(mark=tag))
    S += [Kind("title"), Spacer(1, 0.5 * inch), Paragraph("A Winter Night-Sky Puzzle Book", ParagraphStyle("t0", parent=kick, fontSize=11, textColor=MID)),
          Spacer(1, 10), Paragraph("Stars over<br/>Frostwood", ParagraphStyle("tt", fontName="PlayfairSC-B", fontSize=38, leading=42, alignment=TA_CENTER, textColor=DARK)),
          Spacer(1, 14), Paragraph(f"{NP} Star Battle logic puzzles<br/>from the village to the summit", ParagraphStyle("t2", parent=small, fontSize=13, leading=17)),
          Spacer(1, 0.45 * inch), SkyArt(TW, 2.6 * inch), Spacer(1, 0.45 * inch),
          Paragraph("A Frostwood Puzzle Book", ParagraphStyle("t3", parent=kick, fontSize=10, textColor=DARK)),
          Paragraph("Blake La Pierre", ParagraphStyle("t4", parent=small, fontSize=11))]
    S += [PageBreak(), Kind("nofolio"), Spacer(1, 3.6 * inch)]
    cs = ParagraphStyle("cp", parent=body0, fontSize=9, leading=12, alignment=TA_LEFT)
    for t in [f"<i>Stars over Frostwood: {NP} Star Battle Logic Puzzles</i>",
              "Copyright © 2026 Blake La Pierre. All rights reserved.",
              "No part of this book may be reproduced in any form without written permission from the author, except for brief quotations in reviews. Readers are welcome to photocopy puzzle pages for their own personal use while solving.",
              "Frostwood, its village, railway, lodge and observatory are imaginary. Any resemblance to real places is coincidental.",
              "First edition, 2026",
              "Set in Crimson Text, Playfair Display SC and IBM Plex Sans Condensed, used under the SIL Open Font License."]:
        S += [Paragraph(t, cs), Spacer(1, 6)]
    recto("contents")
    S += [Kind(section="Contents"), Spacer(1, 0.3 * inch)] + heading("Stars over Frostwood", "Contents")
    S.append(("TOC",))
    S += [Spacer(1, 0.35 * inch), Paragraph("On clear winter nights, the Frostwood Star Club climbs from the village green to the little observatory on the roof of the lodge, "
          f"charting the sky as it goes. The snow clouds have smudged their charts. {NP} skies need their stars put back in place before the club’s winter star ledger is complete. "
          "Every puzzle has exactly one solution, and every one can be solved by logic alone, with no guessing.", ParagraphStyle("in", parent=small, fontSize=10.5, leading=14))]
    recto("howto")
    S += [Kind(section="How to Play"), Spacer(1, 0.1 * inch)] + heading("Before the Sky Clears", "How to Play")[:-1] + [Spacer(1, 4)]
    hb = ParagraphStyle("hb", parent=bullet, fontSize=10.5, leading=13.6, spaceAfter=2.5)
    S += [Paragraph("Each puzzle is a patch of night sky, drawn as a square grid divided by thick lines into <b>regions</b>. "
                    "Your job is to put stars in some of the squares, following three rules:", ParagraphStyle("hb0", parent=body0, fontSize=10.8, leading=14)), Spacer(1, 3)]
    for t in ["Every <b>row</b> and every <b>column</b> holds the same number of stars: <b>one star</b> in Parts One and Two, <b>two stars</b> in Parts Three and Four. "
              "The number is printed above each puzzle.",
              "Every <b>region</b> (the areas outlined by thick lines) holds that same number of stars.",
              "Stars <b>never touch</b>: no two stars may be in neighbouring squares, not even diagonally."]:
        S.append(Paragraph(FL + t, hb))
    S += [Spacer(1, 4), Paragraph("<b>Useful Tricks</b>", ParagraphStyle("x", parent=body0, alignment=TA_CENTER, textColor=DARK)), Spacer(1, 3)]
    for t in ["<b>Mark the empties.</b> Put a small dot in every square that cannot hold a star. When you place a star, dot its eight neighbours, "
              "and when a row, column or region has all its stars, dot the rest of it.",
              "<b>Last squares standing.</b> When a row, column or region has only as many open squares as the stars it still needs, they are all stars.",
              "<b>Small regions first.</b> List the ways a small region (or a nearly full row) can still hold its stars. A square that every way uses is a star; "
              "a square that every way touches is empty.",
              "<b>Squeezed regions.</b> If a region’s open squares all lie in one row, that region’s star is that row’s star, so the rest of the row is empty. "
              "The same goes for columns, and in reverse (a row whose open squares all lie in one region).",
              "<b>Counting across several regions.</b> If two regions fit entirely inside two rows (in two-star puzzles: they need four stars and the two rows hold four), "
              "every other square in those two rows is empty. It works for three regions in three rows, and so on.",
              "<b>What if?</b> In the Expert puzzles, you may have to suppose a square holds a star, follow the consequences, and see a row or region run out of room. "
              "Then you know that square is empty."]:
        S.append(Paragraph(FL + t, hb))
    S += [PageBreak(), Kind(section="How to Play"), Spacer(1, 0.05 * inch)] + heading("Let’s Chart the Sky", "A Worked Example")
    S.append(Example(EX_PANELS, 0.27 * inch, ["The puzzle", "Halfway there", "Solved"]))
    S.append(Spacer(1, 8))
    S.append(Paragraph("This small 5×5 sky has one star per row, column and region. Rows are numbered from the top and columns from the left.", ParagraphStyle("exi", parent=body0, fontSize=10.4, leading=13.4, spaceAfter=3)))
    ex = ParagraphStyle("exs", parent=bullet, fontSize=10.4, leading=13.4, spaceAfter=2.5)
    for i, t in enumerate(EX_STEPS, 1):
        S.append(Paragraph(f"<font name='PlayfairSC-B' color='#2b2b2b'>{i}.</font>&nbsp;&nbsp;" + t, ex))
    S.append(Spacer(1, 4))
    S.append(Paragraph("Solutions are at the back of the book.", ParagraphStyle("sm2", parent=small, fontSize=9.5)))
    for band in BANDS:
        part, place, k, blurb = PARTS[band]; ps = D[band]; n = ps[0]["n"]; ks = ps[0]["k"]
        recto(band)
        S += [Kind("opener"), Kind(section=f"{part} · {place}"), Spacer(1, 1.3 * inch)] + heading(f"{part} · {band} · {n}×{n} · {ks} star{'s' if ks > 1 else ''}", place)
        S += [Paragraph(f"Puzzles {ps[0]['num']} to {ps[-1]['num']}", ParagraphStyle("pn", parent=small, fontSize=11)), Spacer(1, 14),
              Paragraph(blurb, ParagraphStyle("bl", parent=small, fontSize=11, leading=15)), Spacer(1, 0.5 * inch),
              SkyArt(TW, 1.9 * inch, seed=k + 10, lodge=(band in ("Hard", "Expert")), village=(band == "Easy"), rail=(band == "Medium"))]
        S.append(PageBreak())
        if n <= 8:
            cell = 0.46 * inch if n == 6 else 0.36 * inch
            for i in range(0, len(ps), 2):
                S += [PuzzleBlock(ps[i], TH / 2 - 1, cell)]
                if i + 1 < len(ps): S.append(PuzzleBlock(ps[i + 1], TH / 2 - 1, cell))
                S.append(PageBreak())
        else:
            cell = 0.44 * inch
            for p in ps: S += [PuzzleBlock(p, TH - 2, cell), PageBreak()]
        S.pop()
    recto("solutions")
    S += [Kind("opener"), Kind(section="Solutions"), Spacer(1, 2.4 * inch)] + heading("The Star Ledger", "Solutions")
    S.append(Paragraph("Each solution shows every star in its place.", small))
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
                        m = ps[j]["n"]; cell = min((bw - 20) / m, (bh - 26) / m, 0.2 * inch if m <= 8 else 0.19 * inch)
                        row.append(SolutionBlock(ps[j], bw - 6, bh - 4, cell))
                    else: row.append("")
                grid.append(row)
            t = Table(grid, colWidths=[bw] * cols, rowHeights=[bh] * rows)
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Crimson", 10), ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3), ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            S.append(t)
    recto("about")
    S += [Kind("nofolio"), Spacer(1, 1.0 * inch)] + heading("Thank You for Stargazing", "Stars over Frostwood")
    S.append(Paragraph("If you enjoyed charting the winter sky, a short review helps other puzzlers find the book. "
                       "The Star Club reads every one, usually by the fire in the lodge after the dome is closed for the night.", ParagraphStyle("ty", parent=body0, alignment=TA_CENTER)))
    S += [Spacer(1, 0.4 * inch), Flake(), Spacer(1, 10), Paragraph("Also by Blake La Pierre", ParagraphStyle("ab", parent=kick, fontSize=11, textColor=DARK)),
          Paragraph("A Frostwood Puzzle Book", ParagraphStyle("ab0", parent=small, fontSize=9.5)), Spacer(1, 8)]
    for t, d in [("The Thief Stayed the Night", "A snowbound hotel mystery puzzle book. Twelve cozy elimination cases at the Frostwood Lodge, at the top of the line."),
                 ("Frostwood Express", "200 Train Tracks logic puzzles. Lay the railway that climbs from the valley to the lodge, from the foothills to the summit.")]:
        S += [Paragraph(f"<i>{t}</i>", ParagraphStyle("ab2", parent=body0, alignment=TA_CENTER, fontSize=13)),
              Paragraph(d, ParagraphStyle("ab3", parent=small)), Spacer(1, 10)]
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
                rows.append((f"{part} · {place}<br/><font size='9.5' color='#737373'>{b} · {ps[0]['n']}×{ps[0]['n']} · {ps[0]['k']} star{'s' if ps[0]['k'] > 1 else ''} · Puzzles {ps[0]['num']}–{ps[-1]['num']}</font>", toc.get(b, 0)))
            rows += [("Solutions", toc.get("solutions", 0))]
            t = Table([[Paragraph(a, ParagraphStyle("tc", parent=body0, fontSize=11.5, leading=14)), str(b)] for a, b in rows], colWidths=[TW - 0.5 * inch, 0.5 * inch])
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Crimson", 11), ("FONT", (1, 0), (1, -1), "Crimson", 11.5), ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), 0.3, FROST), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
            S[i] = t
    fr = Frame(INNER, BOT, TW, TH, id="f", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc = Doc(out, pagesize=(W, H), initialFontName="Crimson", title=f"Stars over Frostwood: {NP} Star Battle Logic Puzzles", author="Blake La Pierre",
              subject="Star Battle logic puzzle book", pageTemplates=[PageTemplate("normal", [fr], onPageEnd=page_end)])
    doc.pkind = {}; doc.marks = {}; doc.section = ""
    doc.build(S)
    return doc.marks, doc.page

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "../interior.pdf"
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
