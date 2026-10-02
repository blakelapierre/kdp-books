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
TITLE = "Tents in Frostwood"
TW = W - INNER - OUTER; TH = H - TOP - BOT

PARTS = {
 "Easy": ("Part One", "The Lodge Meadow", 1,
          "Six-by-six clearings with five to seven pines. Start with the zeros: any row or column numbered 0 is empty, and a pine with only one free neighbour must have its tent there."),
 "Medium": ("Part Two", "Pine Hollow Trail", 2,
            "Eight-by-eight stretches of the trail. The easy fills still help, but somewhere in each puzzle you will need to ask “what if a tent were here?” and follow the answer until a pine or a row runs out of room."),
 "Hard": ("Part Three", "The Upper Grove", 3,
          "Ten-by-ten groves with fourteen to eighteen pines. Keep the zero-rows and forced neighbours in mind, then lean on careful trial: one wrong tent will touch another or leave a pine stranded."),
 "Expert": ("Part Four", "Summit Ridge Camp", 4,
            "Twelve-by-twelve camps on the ridge, twenty to twenty-six pines each. The largest grids in the book. Pack a sharp pencil, and do not be shy of a short “what if?”."),
}

def viewpoints():
    P = {"Easy": ("the Gate Pines|the Cocoa Bench|Fir Corner|the Woodpile|Holly Path|the Bird Table|Lantern Stump|Snowdrop Dell|the Tool Shed|Rowan Seat|"
                  "the Meadow Gate|Chapel Pines|the Skating Path|Ivy Stile|the Well House|Orchard Edge|Bell Meadow|the Sheepfold|Willow Bench|the Duck Pond|"
                  "Candle Dell|the Toll Gate|Fir Row|the Mill Race|Pudding Stile|the Pump|Wren Dell|the Village Gate|Fox Meadow|Hazel Path|"
                  "the Chestnut|Cobble Dell|the Bandstand|Church Pines|the Tea Lawn|Market Edge|Post Path|the Green Gate|Bakery Dell|the Old Bridge"),
         "Medium": ("Pine Hollow|the Lower Switchback|Larch Bend|the Footbridge|Cedar Cut|Aspen Rise|the Waycairn|Hemlock Step|Birch Hollow|the Trail Sign|"
                    "Spruce Bend|Juniper Cut|the Ice Steps|Owl Hollow|Mistletoe Rise|Heron Bend|Otter Hollow|Badger Cut|Fox Glen|Kestrel Rise|"
                    "Elder Hollow|Starling Bend|Rime Cut|Crystal Rise|Cloud Hollow|the Milk Path|Lamp Hollow|Buffer Bend|Ticket Rise|Cloudberry Cut|"
                    "Raven Hollow|Grouse Bend|Fern Cut|Watershed Rise|Ptarmigan Hollow|Mist Bend|Hare Cut|Bilberry Rise|Zigzag Hollow|Summit Path"),
         "Hard": ("the Lower Grove|Hoarfrost Stand|the Shepherd’s Pines|Eagle Stand|the Tarn Grove|Rowan Stand|the Scree Pines|Juniper Stand|Waymarker Grove|Pine Shoulder|"
                  "the Snowfield Stand|Lark Grove|the Cairn Pines|Silver Stand|Hanging Grove|Aspen Stand|Ice-Fall Pines|Heather Grove|Boulder Stand|Cloudberry Grove|"
                  "the Saddle Pines|Winter Stand|Stone-Stile Grove|Ptarmigan Stand|Frozen-Tarn Grove|Mist Stand|Old-Mine Pines|Hare Grove|Zigzag Stand|Bilberry Grove|"
                  "the Upper Stand|Fern Grove|Watershed Stand|Grouse Grove|the Col Pines|Raven Stand|Long-Traverse Grove|Snow-Bunting Stand|the Refuge Pines|Glacier Grove|"
                  "Viewpoint Stand|Frost Hollow Grove|Sheep-Track Pines|Blue-Ice Stand|Stone-Man Grove|Crowberry Stand|Stream-Crossing Pines|White-Hare Grove|Last-Bend Stand|Summit Grove"),
         "Expert": ("Ridge Camp|the Windbreak|Star Ledger Tent|the Snow Porch|Brass Rail Camp|Map Tent|Clock Tent|Sky Hatch Camp|Warm Tent|Finder Camp|"
                    "Night Log Tent|Chart Tent|Eyepiece Camp|Weather Camp|Library Tent|Lamp Tent|Cocoa Tent|Window Camp|Guest Tent|North Camp|"
                    "Tower Tent|Pole Star Camp|Lens Tent|Attic Camp|Sky Globe Tent|Fireside Camp|Record Tent|Iron Stair Camp|Gallery Tent|East Camp|"
                    "Star Chart Tent|Balcony Camp|Old Clock Tent|Brass Camp|Watch Tent|Hearth Camp|Snug Tent|Lantern Camp|Top Landing Tent|West Camp|"
                    "Meridian Tent|Moon Chart Camp|Plate Tent|Star Drawer Camp|Snow Porch Tent|Boot Camp|Dome Shutter Tent|Midnight Camp|Last Lamp Tent|Summit Tent")}
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

def pine(c, x, y, s):
    c.saveState(); c.setFillColor(DARK)
    for k, (w, yy) in enumerate([(0.62, -0.30), (0.48, -0.08), (0.34, 0.12)]):
        p = c.beginPath(); p.moveTo(x - w * s / 2, y + yy * s); p.lineTo(x + w * s / 2, y + yy * s); p.lineTo(x, y + (yy + 0.26) * s); p.close(); c.drawPath(p, stroke=0, fill=1)
    c.rect(x - 0.05 * s, y - 0.42 * s, 0.1 * s, 0.12 * s, stroke=0, fill=1); c.restoreState()

def tent_icon(c, x, y, s):
    """Simple A-frame tent centred on (x, y)."""
    c.saveState()
    c.setStrokeColor(INK); c.setFillColor(ICE); c.setLineWidth(max(0.7, s * 0.06)); c.setLineJoin(1)
    p = c.beginPath()
    p.moveTo(x - 0.38 * s, y - 0.28 * s); p.lineTo(x, y + 0.34 * s); p.lineTo(x + 0.38 * s, y - 0.28 * s); p.close()
    c.drawPath(p, stroke=1, fill=1)
    c.setFillColor(DARK)
    p = c.beginPath(); p.moveTo(x - 0.1 * s, y - 0.28 * s); p.lineTo(x, y + 0.05 * s); p.lineTo(x + 0.1 * s, y - 0.28 * s); p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.setStrokeColor(INK); c.line(x, y + 0.34 * s, x, y - 0.28 * s)
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

def draw_grid(c, x0, y0, s, p, mode="puzzle", tents=(), dots=(), labels=False):
    """(x0, y0) = lower-left of the cell grid (not including clue gutters)."""
    n = p["n"]; top = y0 + n * s
    trees = {tuple(t) for t in p["trees"]}
    c.saveState()
    # clues
    fs = min(11, max(7, s * 0.38))
    c.setFillColor(INK); c.setFont("Plex-M", fs)
    for i in range(n):
        c.drawCentredString(x0 + i * s + s / 2, top + s * 0.18, str(p["cols"][i]))
        c.drawCentredString(x0 + n * s + s * 0.42, y0 + (n - 1 - i) * s + s / 2 - fs * 0.35, str(p["rows"][i]))
    c.setStrokeColor(GRIDC); c.setLineWidth(0.4 if s > 12 else 0.25)
    for i in range(1, n):
        c.line(x0 + i * s, y0, x0 + i * s, top); c.line(x0, y0 + i * s, x0 + n * s, y0 + i * s)
    c.setStrokeColor(INK); c.setLineWidth(max(1.3, s * 0.08) if s > 12 else 1.0)
    c.rect(x0, y0, n * s, n * s)
    for (r, cc) in trees:
        pine(c, x0 + cc * s + s / 2, y0 + (n - 1 - r) * s + s / 2, s * 0.92)
    show = [tuple(t) for t in p["tents"]] if mode == "solution" else [tuple(t) for t in tents]
    for (r, cc) in show:
        tent_icon(c, x0 + cc * s + s / 2, y0 + (n - 1 - r) * s + s / 2, s * 0.9)
    c.setFillColor(MID)
    for (r, cc) in dots:
        if (r, cc) in trees: continue
        c.circle(x0 + cc * s + s / 2, y0 + (n - 1 - r) * s + s / 2, max(0.9, s * 0.07), stroke=0, fill=1)
    if labels:
        c.setFont("Plex", 7); c.setFillColor(MID)
        for i in range(n):
            c.drawCentredString(x0 + i * s + s / 2, top + s * 0.55, str(i))
            c.drawRightString(x0 - 3, y0 + (n - 1 - i) * s + s / 2 - 2.4, str(i))
    c.restoreState()

def rating(c, x, y, k, r=4.2, gap=11):
    for i in range(4):
        snowflake(c, x - (3 - i) * gap, y, r, DARK if i < k else colors.Color(.78, .78, .78), lw=0.12)

class PuzzleBlock(Flowable):
    def __init__(s, p, h, cell): s.p = p; s.h = h; s.cell = cell; s.width = TW; s.height = h
    def wrap(s, aw, ah): return TW, s.h
    def draw(s):
        c = s.canv; p = s.p; n = p["n"]; cs = s.cell
        # grid needs clue gutter ~0.55*cs on top and right
        gw = n * cs; gh = n * cs; gpad = cs * 0.55
        full = s.h > TH / 2
        block = 0.36 * inch + 0.1 * inch + gh + gpad
        ytop = s.h - (s.h - block - (0.3 * inch if full else 0)) / 2
        ytop = min(ytop, s.h)
        c.setFillColor(DARK); c.setFont("PlayfairSC-B", 15); c.drawString(0, ytop - 13, f"No. {p['num']}")
        wno = pdfmetrics.stringWidth(f"No. {p['num']}", "PlayfairSC-B", 15)
        c.setFont("Crimson-I", 10.5); c.setFillColor(MID)
        prep = {"Easy": "In ", "Medium": "Along ", "Hard": "Among ", "Expert": "At "}[p["band"]]
        c.drawString(wno + 8, ytop - 13, prep + VIEW[p["num"] - 1])
        rating(c, TW - 5, ytop - 9, PARTS[p["band"]][2])
        c.setFont("Plex", 7.5); c.setFillColor(MID)
        c.drawRightString(TW - 50, ytop - 12, f"{p['band'].upper()} · {n}×{n} · {p['k']} TENTS")
        c.setStrokeColor(FROST); c.setLineWidth(0.5); c.line(0, ytop - 20, TW, ytop - 20)
        x0 = (TW - (gw + gpad)) / 2; y0 = ytop - 0.36 * inch - 0.08 * inch - gh - gpad + gpad
        # y0 is bottom of cells; top clue sits above
        y0 = ytop - 0.36 * inch - 0.12 * inch - gpad - gh
        draw_grid(c, x0, y0, cs, p)
        if full:
            free_lo, free_hi = 22 + 8, y0 - 8
            vh = min(0.85 * inch, free_hi - free_lo)
            if vh >= 0.55 * inch:
                draw_ill(c, VIGNETTES[p["num"] % len(VIGNETTES)], 0, free_lo + (free_hi - free_lo - vh) / 2, TW, vh)
            yb = 6; c.setStrokeColor(FROST); c.setLineWidth(0.5); c.line(0, yb + 16, TW, yb + 16)
            c.setFont("PlayfairSC", 8.5); c.setFillColor(MID)
            c.drawString(0, yb, "Started"); c.line(40, yb - 1, 120, yb - 1)
            c.drawString(146, yb, "Finished"); c.line(190, yb - 1, 270, yb - 1)
            c.drawRightString(TW - 14, yb, "Camp set"); tent_icon(c, TW - 5, yb + 3, 10)

class SolutionBlock(Flowable):
    def __init__(s, p, w, h, cell): s.p = p; s.width = w; s.height = h; s.cell = cell
    def wrap(s, aw, ah): return s.width, s.height
    def draw(s):
        c = s.canv; p = s.p; n = p["n"]; cs = s.cell; gw = n * cs; gpad = cs * 0.5
        c.setFont("PlayfairSC-B", 10); c.setFillColor(DARK); c.drawString(0, s.height - 10, f"No. {p['num']}")
        x0 = (s.width - (gw + gpad)) / 2; y0 = s.height - 14 - gpad - gw
        draw_grid(c, x0, y0, cs, p, mode="solution")

class Example(Flowable):
    def __init__(s, panels, cell, cap):
        s.panels = panels; s.cell = cell; s.cap = cap; s.width = TW
        n = EX["n"]; s.height = cell * n + cell * 0.6 + 30
    def wrap(s, aw, ah): return TW, s.height
    def draw(s):
        c = s.canv; n = EX["n"]; cs = s.cell; k = len(s.panels)
        gw = n * cs; gpad = cs * 0.55; box = gw + gpad
        gap = (TW - k * box - 8) / max(k - 1, 1); x = 4
        for i, (mode, tents_, dots) in enumerate(s.panels):
            m = "solution" if mode == "solution" else "puzzle"
            draw_grid(c, x, 16, cs, EX, mode=m, tents=tents_, dots=dots, labels=True)
            c.setFont("Crimson-I", 9); c.setFillColor(MID); c.drawCentredString(x + gw / 2, 2, s.cap[i])
            x += box + gap

class GroveArt(Flowable):
    """Line-art vignette: pines, a couple of tents, mountains (grayscale)."""
    def __init__(s, w, h, seed=7, ridge=False, trail=False, meadow=False):
        s.width, s.height = w, h; s.seed = seed; s.ridge = ridge; s.trail = trail; s.meadow = meadow
    def draw(s):
        c = s.canv; w, h = s.width, s.height; r = random.Random(s.seed)
        for _ in range(14):
            snowflake(c, r.uniform(0.04, 0.96) * w, r.uniform(0.55, 0.97) * h, r.uniform(2.5, 5.5), colors.Color(.72, .72, .72))
        c.setStrokeColor(MID); c.setLineWidth(1.1); c.setLineJoin(1)
        pts = [(0, 0.28), (0.18, 0.55), (0.34, 0.40), (0.52, 0.72), (0.70, 0.44), (0.86, 0.58), (1.0, 0.34)]
        pa = c.beginPath(); pa.moveTo(pts[0][0] * w, pts[0][1] * h * 0.7)
        for x, y in pts[1:]: pa.lineTo(x * w, y * h * 0.7)
        c.drawPath(pa, stroke=1, fill=0)
        base = 0.0
        c.setStrokeColor(DARK); c.setLineWidth(0.9); c.line(-0.1 * inch, base, w + 0.1 * inch, base)
        for i in range(int(w / 22)):
            x = 6 + i * 22 + r.uniform(-4, 4); th = r.uniform(16, 28)
            if s.meadow and 0.35 * w < x < 0.65 * w: continue
            pa = c.beginPath(); pa.moveTo(x - th * 0.32, base); pa.lineTo(x, base + th); pa.lineTo(x + th * 0.32, base); pa.close()
            c.setFillColor(colors.white); c.setStrokeColor(MID); c.setLineWidth(0.8); c.drawPath(pa, stroke=1, fill=1)
        if s.trail:
            c.setStrokeColor(DARK); c.setLineWidth(0.9); c.setDash(2, 3)
            pa = c.beginPath(); pa.moveTo(0.05 * w, base + 4); pa.curveTo(0.3 * w, base + 10, 0.6 * w, base + 2, 0.95 * w, base + 8)
            c.drawPath(pa, stroke=1, fill=0); c.setDash()
        # a few tents in the clearing
        for tx, sc in [(0.28 * w, 14), (0.48 * w, 16), (0.68 * w, 13)]:
            if s.ridge or s.meadow or s.trail:
                tent_icon(c, tx, base + sc * 0.35, sc)

from example_text import EX_PANELS, EX_STEPS

import os
ILL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "illustrations")
VIGNETTES = ["v_tent", "v_lantern", "v_sled", "v_sign", "v_kettle", "v_moon"]

def ill(name): return os.path.join(ILL, name + ".png")

def draw_ill(c, name, x, y, w, h):
    """Place a 300 DPI ink illustration (made by illustrations.py) inside the box, keeping its aspect ratio."""
    from reportlab.lib.utils import ImageReader
    img = ImageReader(ill(name)); iw, ih = img.getSize()
    sc = min(w / iw, h / ih); dw, dh = iw * sc, ih * sc
    c.drawImage(ill(name), x + (w - dw) / 2, y + (h - dh) / 2, dw, dh)

class Art(Flowable):
    """A line-art illustration from ../illustrations, centred in the text column."""
    def __init__(s, name, w, h): s.name = name; s.width = w; s.height = h
    def wrap(s, aw, ah): return s.width, s.height
    def draw(s): draw_ill(s.canv, s.name, 0, 0, s.width, s.height)


def build(recto_fix):
    S = []
    def recto(tag):
        S.append(PageBreak())
        if tag in recto_fix: S.extend([Kind("blank"), PageBreak()])
        S.append(Kind(mark=tag))
    S += [Kind("title"), Spacer(1, 2.2 * inch),
          Paragraph("Tents in<br/>Frostwood", ParagraphStyle("ht", fontName="PlayfairSC-B", fontSize=26, leading=30, alignment=TA_CENTER, textColor=DARK)),
          Spacer(1, 10), Flake(), Spacer(1, 0.5 * inch), Art("v_moon", TW, 0.85 * inch),
          PageBreak(), Kind("title"), Spacer(1, 0.05 * inch), Art("frontispiece", TW, 7.0 * inch), Spacer(1, 6),
          Paragraph("Evening at Summit Ridge Camp", ParagraphStyle("fc", parent=small, fontSize=10)),
          PageBreak()]
    S += [Kind("title"), Spacer(1, 0.5 * inch),
          Paragraph("A Pine-Grove Puzzle Book", ParagraphStyle("t0", parent=kick, fontSize=11, textColor=MID)),
          Spacer(1, 10),
          Paragraph("Tents in<br/>Frostwood", ParagraphStyle("tt", fontName="PlayfairSC-B", fontSize=38, leading=42, alignment=TA_CENTER, textColor=DARK)),
          Spacer(1, 14),
          Paragraph(f"{NP} Tents and Trees logic puzzles<br/>from the meadow to the ridge", ParagraphStyle("t2", parent=small, fontSize=13, leading=17)),
          Spacer(1, 0.4 * inch), Art("title", TW, 2.6 * inch), Spacer(1, 0.4 * inch),
          Paragraph("A Frostwood Puzzle Book", ParagraphStyle("t3", parent=kick, fontSize=10, textColor=DARK)),
          Paragraph("Blake La Pierre", ParagraphStyle("t4", parent=small, fontSize=11))]
    S += [PageBreak(), Kind("nofolio"), Spacer(1, 3.6 * inch)]
    cs = ParagraphStyle("cp", parent=body0, fontSize=9, leading=12, alignment=TA_LEFT)
    for t in [f"<i>Tents in Frostwood: {NP} Tents and Trees Logic Puzzles</i>",
              "Copyright © 2026 Blake La Pierre. All rights reserved.",
              "No part of this book may be reproduced in any form without written permission from the author, except for brief quotations in reviews. Readers are welcome to photocopy puzzle pages for their own personal use while solving.",
              "Frostwood, its village, railway, lodge, pine groves and mountain camps are imaginary. Any resemblance to real places is coincidental.",
              "First edition, 2026",
              "Set in Crimson Text, Playfair Display SC and IBM Plex Sans Condensed, used under the SIL Open Font License."]:
        S += [Paragraph(t, cs), Spacer(1, 6)]
    recto("contents")
    S += [Kind(section="Contents"), Spacer(1, 0.3 * inch)] + heading("Tents in Frostwood", "Contents")
    S.append(("TOC",))
    S += [Spacer(1, 0.35 * inch),
          Paragraph("Each winter the Frostwood campers pitch their tents beside the mountain pines, from the lodge meadow up the hollow trail to the ridge. "
                    f"This year the maps are smudged. {NP} clearings need their tents put back beside the trees before the first cocoa of the evening. "
                    "Every puzzle has exactly one solution, and every one can be solved by logic alone, with no guessing.",
                    ParagraphStyle("in", parent=small, fontSize=10.5, leading=14))]
    recto("howto")
    S += [Kind(section="How to Play"), Spacer(1, 0.1 * inch)] + heading("Before You Pitch Camp", "How to Play")[:-1] + [Spacer(1, 4)]
    hb = ParagraphStyle("hb", parent=bullet, fontSize=10.5, leading=13.6, spaceAfter=2.5)
    S += [Paragraph("Each puzzle is a square clearing dotted with <b>pines</b>. Your job is to pitch a <b>tent</b> for every pine, following three rules:",
                    ParagraphStyle("hb0", parent=body0, fontSize=10.8, leading=14)), Spacer(1, 3)]
    for t in ["Every pine has <b>exactly one tent</b>, and that tent sits in a square sharing a side with the pine (not only a corner).",
              "Tents <b>never touch</b>, not even at the corners. Two tents may not sit in neighbouring squares.",
              "The numbers beside each <b>row</b> and above each <b>column</b> tell you how many tents that row or column holds."]:
        S.append(Paragraph(FL + t, hb))
    S += [Spacer(1, 4), Paragraph("<b>Useful Tricks</b>", ParagraphStyle("x", parent=body0, alignment=TA_CENTER, textColor=DARK)), Spacer(1, 3)]
    for t in ["<b>Start with the zeros.</b> A row or column numbered 0 has no tents at all — mark every open square in it empty.",
              "<b>Forced neighbours.</b> When a pine has only one free square beside it, that square is its tent. When you place a tent, mark its eight neighbours empty (tents never touch), and tick off its pine.",
              "<b>Last squares standing.</b> When a row or column still needs as many tents as it has open squares, they are all tents.",
              "<b>Orphan squares.</b> A square that is not beside any pine still waiting for a tent cannot hold a tent — mark it empty.",
              "<b>What if?</b> From Part Two on, you may have to suppose a square holds a tent, follow the consequences, and see a pine or a row run out of room. Then you know that square is empty (or the other way around)."]:
        S.append(Paragraph(FL + t, hb))
    S += [PageBreak(), Kind(section="How to Play"), Spacer(1, 0.05 * inch)] + heading("Let’s Pitch a Tent", "A Worked Example")
    S.append(Example(EX_PANELS, 0.30 * inch, ["The puzzle", "Zeros filled in", "Solved"]))
    S.append(Spacer(1, 8))
    S.append(Paragraph("This small 5×5 clearing has three pines. Rows are numbered from the top (starting at 0 in the labels below) and columns from the left.",
                       ParagraphStyle("exi", parent=body0, fontSize=10.4, leading=13.4, spaceAfter=3)))
    ex = ParagraphStyle("exs", parent=bullet, fontSize=10.4, leading=13.4, spaceAfter=2.5)
    for i, t in enumerate(EX_STEPS, 1):
        S.append(Paragraph(f"<font name='PlayfairSC-B' color='#2b2b2b'>{i}.</font>&nbsp;&nbsp;" + t, ex))
    S.append(Spacer(1, 4))
    S.append(Paragraph("Solutions are at the back of the book.", ParagraphStyle("sm2", parent=small, fontSize=9.5)))
    for band in BANDS:
        part, place, k, blurb = PARTS[band]; ps = D[band]; n = ps[0]["n"]
        recto(band)
        S += [Kind("opener"), Kind(section=f"{part} · {place}"), Spacer(1, 0.9 * inch)] + heading(f"{part} · {band} · {n}×{n}", place)
        S += [Paragraph(f"Puzzles {ps[0]['num']} to {ps[-1]['num']}", ParagraphStyle("pn", parent=small, fontSize=11)), Spacer(1, 14),
              Paragraph(blurb, ParagraphStyle("bl", parent=small, fontSize=11, leading=15)), Spacer(1, 0.4 * inch),
              Art("opener-" + band.lower(), TW, 2.4 * inch)]
        S.append(PageBreak())
        if n <= 8:
            cell = 0.42 * inch if n == 6 else 0.34 * inch
            for i in range(0, len(ps), 2):
                S += [PuzzleBlock(ps[i], TH / 2 - 1, cell)]
                if i + 1 < len(ps): S.append(PuzzleBlock(ps[i + 1], TH / 2 - 1, cell))
                S.append(PageBreak())
        else:
            cell = 0.40 * inch if n == 10 else 0.34 * inch
            for p in ps: S += [PuzzleBlock(p, TH - 2, cell), PageBreak()]
        S.pop()
    recto("solutions")
    S += [Kind("opener"), Kind(section="Solutions"), Spacer(1, 2.4 * inch)] + heading("The Camp Ledger", "Solutions")
    S.append(Paragraph("Each solution shows every tent in its place beside its pine.", small))
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
                        m = ps[j]["n"]; cell = min((bw - 24) / (m + 0.55), (bh - 30) / (m + 0.55), 0.18 * inch if m <= 8 else 0.155 * inch)
                        row.append(SolutionBlock(ps[j], bw - 6, bh - 4, cell))
                    else: row.append("")
                grid.append(row)
            t = Table(grid, colWidths=[bw] * cols, rowHeights=[bh] * rows)
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Crimson", 10), ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                                   ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            S.append(t)
    recto("about")
    S += [Kind("nofolio"), Spacer(1, 1.0 * inch)] + heading("Thank You for Camping", "Tents in Frostwood")
    S.append(Paragraph("If you enjoyed pitching tents among the Frostwood pines, a short review helps other puzzlers find the book. "
                       "The campers read every one, usually by the fire after the last tent is guyed down for the night.",
                       ParagraphStyle("ty", parent=body0, alignment=TA_CENTER)))
    S += [Spacer(1, 0.4 * inch), Flake(), Spacer(1, 10),
          Paragraph("Also by Blake La Pierre", ParagraphStyle("ab", parent=kick, fontSize=11, textColor=DARK)),
          Paragraph("A Frostwood Puzzle Book", ParagraphStyle("ab0", parent=small, fontSize=9.5)), Spacer(1, 8)]
    for t, d in [("The Thief Stayed the Night", "A snowbound hotel mystery puzzle book. Twelve cozy elimination cases at the Frostwood Lodge, at the top of the line."),
                 ("Frostwood Express", "200 Train Tracks logic puzzles. Lay the railway that climbs from the valley to the lodge, from the foothills to the summit."),
                 ("Stars over Frostwood", "180 Star Battle logic puzzles. Chart the winter sky from the village green to the lodge observatory.")]:
        S += [Paragraph(f"<i>{t}</i>", ParagraphStyle("ab2", parent=body0, alignment=TA_CENTER, fontSize=13)),
              Paragraph(d, ParagraphStyle("ab3", parent=small)), Spacer(1, 10)]
    S += [Spacer(1, 0.12 * inch), Art("thanks", TW, 1.3 * inch)]
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
    doc = Doc(out, pagesize=(W, H), initialFontName="Crimson", title=f"Tents in Frostwood: {NP} Tents and Trees Logic Puzzles", author="Blake La Pierre",
              subject="Tents and Trees logic puzzle book", pageTemplates=[PageTemplate("normal", [fr], onPageEnd=page_end)])
    doc.pkind = {}; doc.marks = {}; doc.section = ""
    doc.build(S)
    return doc.marks, doc.page

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "../frostwood-04-tents-in-frostwood-interior.pdf"
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
