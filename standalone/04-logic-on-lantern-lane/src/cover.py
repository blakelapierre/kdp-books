"""KDP full-wrap paperback cover: 6x9 trim, 0.125in bleed, white paper B&W spine = pages x 0.002252in.
Reads ../build-info.json for the page count -> ../standalone-04-logic-on-lantern-lane-cover.pdf"""
import json, random, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

G = "/usr/share/fonts/truetype/sand-box/google/"
for n, p in [("Crimson", "Crimson Text/CrimsonText-Regular.ttf"), ("Crimson-I", "Crimson Text/CrimsonText-Italic.ttf"),
             ("Crimson-B", "Crimson Text/CrimsonText-Bold.ttf"), ("PlayfairSC", "Playfair Display SC/PlayfairDisplaySC-Regular.ttf"),
             ("PlayfairSC-B", "Playfair Display SC/PlayfairDisplaySC-Bold.ttf"), ("Plex", "IBM Plex Sans Condensed/IBMPlexSansCondensed-Regular.ttf")]:
    pdfmetrics.registerFont(TTFont(n, G + p))

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
info = json.load(open(os.path.join(ROOT, "build-info.json")))
PAGES = info["pages"]
BLEED = 0.125
TW, TH = 6.0, 9.0
SPINE = PAGES * 0.002252
CW = BLEED + TW + SPINE + TW + BLEED
CH = BLEED + TH + BLEED
BG = (0x1d, 0x1d, 0x1f)
NIGHT = colors.Color(BG[0] / 255, BG[1] / 255, BG[2] / 255)
SPINEC = colors.HexColor("#2a2a2c")
PALE = colors.HexColor("#d9d9d9")
SOFT = colors.HexColor("#a8a8a8")
GLOW = colors.HexColor("#f3e9c8")
X_BACK, X_SPINE, X_FRONT = BLEED, BLEED + TW, BLEED + TW + SPINE


def night_image():
    """The cover scene as pale lines on the night colour (inverted ink drawing)."""
    from PIL import Image
    im = Image.open(os.path.join(ROOT, "illustrations", "cover-scene.png")).convert("L")
    inv = im.point(lambda v: 255 - v)
    rgb = Image.merge("RGB", [inv.point(lambda v, b=b: int(b + (238 - b) * v / 255)) for b in BG])
    path = os.path.join(ROOT, "tmp", "cover-scene-night.png")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    rgb.save(path, dpi=(300, 300))
    return path


def glow(c, x, y, r):
    for i in range(10, 0, -1):
        c.setFillColor(colors.Color(1, 0.95, 0.8, alpha=0.035))
        c.circle(x, y, r * i / 10, stroke=0, fill=1)


def mini_grid(c, x, y, cell, marks, light=True):
    n = 4
    col = PALE if light else colors.black
    c.setStrokeColor(col)
    c.setLineWidth(0.5)
    for i in range(n + 1):
        c.line(x, y + i * cell, x + n * cell, y + i * cell)
        c.line(x + i * cell, y, x + i * cell, y + n * cell)
    c.setLineWidth(1.2)
    c.rect(x, y, n * cell, n * cell, stroke=1, fill=0)
    for (r, q), m in marks.items():
        cx, cy = x + q * cell + cell / 2, y + (n - 1 - r) * cell + cell / 2
        if m == "o":
            c.setFillColor(GLOW); c.circle(cx, cy, cell * 0.22, stroke=0, fill=1)
        else:
            c.setStrokeColor(SOFT); c.setLineWidth(0.9)
            d = cell * 0.17
            c.line(cx - d, cy - d, cx + d, cy + d); c.line(cx - d, cy + d, cx + d, cy - d)


def front(c, ox, scene):
    I = inch
    W = TW * I
    c.saveState()
    cp = c.beginPath(); cp.rect(ox * I, 0, (TW + BLEED) * I, CH * I); c.clipPath(cp, stroke=0, fill=0)
    c.translate(ox * I, BLEED * I)
    # scene
    sw, sh = 5.4 * I, 4.3 * I
    sx, sy = (W - sw) / 2, 0.85 * I
    c.drawImage(scene, sx, sy, sw, sh)
    # lamp glows (positions match cover_scene's lampposts)
    for fx, fy, r in [(0.2, 14 / 72 / 4.3 + 0.46 * 0.8 + 0.46 * 0.22 * 0.5, 34), (0.8, 14 / 72 / 4.3 + 0.46 * 0.8 + 0.46 * 0.22 * 0.5, 34),
                      (0.42, 0.5 - 30 / 72 / 4.3 + 0.18 * 0.8 + 0.18 * 0.22 * 0.5, 16), (0.58, 0.5 - 30 / 72 / 4.3 + 0.18 * 0.8 + 0.18 * 0.22 * 0.5, 16)]:
        glow(c, sx + fx * sw, sy + fy * sh, r)
    c.setFillColor(PALE)
    c.setFont("PlayfairSC", 11)
    c.drawCentredString(W / 2, 8.25 * I, "Cozy Logic Grid Puzzles for Adults")
    c.setStrokeColor(SOFT); c.setLineWidth(0.8)
    c.line(2.0 * I, 8.1 * I, 4.0 * I, 8.1 * I)
    c.setFillColor(colors.white)
    c.setFont("PlayfairSC-B", 44)
    c.drawCentredString(W / 2, 7.3 * I, "Logic on")
    c.drawCentredString(W / 2, 6.6 * I, "Lantern Lane")
    c.setFont("Crimson-I", 16)
    c.setFillColor(GLOW)
    c.drawCentredString(W / 2, 6.1 * I, "120 Village Puzzles to Solve with a Pencil")
    c.setFont("PlayfairSC", 10)
    c.setFillColor(SOFT)
    c.drawCentredString(W / 2, 5.72 * I, "Easy to Expert · Hints & Solutions · One Answer Each")
    c.setFont("Crimson-I", 14)
    c.setFillColor(PALE)
    c.drawCentredString(W / 2, 0.45 * I, "Blake La Pierre")
    c.restoreState()


BLURB = [
    "<b>Welcome to Lantern Lane, where the lamps come on early and every villager has a little puzzle to share.</b>",
    "Who brought the lemon tart, and what did it cost? Which skater drank cocoa after six laps? Each page is a short scene from cozy village life: "
    "bake sales, knitting circles, a lantern parade and a snowman contest. Match everyone to the right things using the clues and the grid.",
    "No murders, no crime scenes. Just warm stories and clean logic. Every puzzle has exactly one answer, checked by computer, and can be solved by reasoning alone.",
]
FEATS = [
    "120 logic grid puzzles in four parts, 30 of each level",
    "Easy 3×4 · Medium 4×4 · Hard 4×5 · Expert 5×5",
    "Expert puzzles on a two-page spread with an answer table",
    "A how-to guide and a fully worked example",
    "A first-step hint and full solution for every puzzle",
    "Black-and-white ink illustrations of the village",
]


def back(c):
    I = inch
    x0 = (X_BACK + 0.55) * I
    w = (TW - 1.1) * I
    c.setFillColor(colors.white)
    c.setFont("PlayfairSC-B", 16)
    c.drawCentredString((X_BACK + TW / 2) * I, (BLEED + 8.25) * I, "A Village Full of Puzzles")
    c.setStrokeColor(SOFT); c.setLineWidth(0.8)
    c.line((X_BACK + 2.1) * I, (BLEED + 8.05) * I, (X_BACK + 3.9) * I, (BLEED + 8.05) * I)
    st = ParagraphStyle("bl", fontName="Crimson", fontSize=11.5, leading=15, textColor=colors.white, alignment=TA_JUSTIFY, spaceAfter=7)
    fl = [Paragraph(t, st) for t in BLURB]
    li = ParagraphStyle("li", parent=st, alignment=TA_LEFT, fontSize=11, leading=14, leftIndent=14, firstLineIndent=-12, spaceAfter=3, textColor=PALE)
    fl += [Paragraph("•&nbsp;&nbsp;" + t, li) for t in FEATS]
    f = Frame(x0, (BLEED + 2.05) * I, w, 5.85 * I, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
    f.addFromList(fl, c)
    assert not fl, "back cover text overflow"
    # sample grid card
    gx, gy = (X_BACK + 0.6) * I, (BLEED + 0.45) * I
    mini_grid(c, gx, gy, 0.3 * I, {(0, 0): "x", (0, 1): "o", (0, 2): "x", (0, 3): "x", (1, 1): "x", (2, 1): "x", (3, 1): "x",
                                    (1, 0): "x", (2, 2): "o", (3, 3): "x"})
    tx = (X_BACK + 2.05) * I
    c.setFillColor(PALE); c.setFont("PlayfairSC", 9)
    c.drawString(tx, (BLEED + 1.55) * I, "How it works")
    c.setFont("Crimson-I", 10)
    for i, t in enumerate(["Read the clues.", "Cross out what can't be.", "Dot what must be.", "One answer, every time."]):
        c.drawString(tx, (BLEED + 1.33 - i * 0.18) * I, t)
    c.setFont("PlayfairSC", 8.5); c.setFillColor(SOFT)
    c.drawString(tx, (BLEED + 0.45) * I, "Puzzles & Games")


def main(out=None, guides=False):
    if out is None:
        out = os.path.join(ROOT, "standalone-04-logic-on-lantern-lane-cover.pdf")
    I = inch
    scene = night_image()
    c = canvas.Canvas(out, pagesize=(CW * I, CH * I), initialFontName="Crimson")
    c.setTitle("Logic on Lantern Lane — KDP cover")
    c.setAuthor("Blake La Pierre")
    c.setFillColor(NIGHT)
    c.rect(0, 0, CW * I, CH * I, stroke=0, fill=1)
    r = random.Random(7)
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.35))
    for _ in range(60):
        x = r.uniform(0, CW); y = r.uniform(BLEED + 6.0, CH)
        if X_SPINE - 0.1 < x < X_FRONT + 0.1:
            continue
        c.circle(x * I, y * I, r.uniform(0.4, 1.1), stroke=0, fill=1)
    back(c)
    c.setFillColor(SPINEC)
    c.rect(X_SPINE * I, 0, SPINE * I, CH * I, stroke=0, fill=1)
    assert PAGES >= 79
    fs = 8.5
    cap = 0.71 * fs
    assert cap <= (SPINE - 2 * 0.0625) * 72 + 0.01, (cap, SPINE)
    c.saveState()
    c.translate((X_SPINE + SPINE / 2) * I, (BLEED + TH / 2) * I)
    c.rotate(-90)
    c.setFont("PlayfairSC-B", fs)
    c.setFillColor(colors.white)
    c.drawCentredString(-1.25 * I, -cap / 2, "LOGIC ON LANTERN LANE")
    c.setFillColor(GLOW)
    c.drawCentredString(1.05 * I, -cap / 2, "120 COZY LOGIC GRID PUZZLES")
    c.setFillColor(PALE)
    c.drawCentredString(3.25 * I, -cap / 2, "BLAKE LA PIERRE")
    c.restoreState()
    front(c, X_FRONT, scene)
    bx, by = X_BACK + TW - 0.25 - 2.0, BLEED + 0.25
    if guides:
        c.setLineWidth(0.6)
        c.setStrokeColor(colors.red); c.rect(BLEED * I, BLEED * I, (CW - 2 * BLEED) * I, TH * I)
        c.setStrokeColor(colors.magenta); c.line(X_SPINE * I, 0, X_SPINE * I, CH * I); c.line(X_FRONT * I, 0, X_FRONT * I, CH * I)
        c.setStrokeColor(colors.yellow); c.rect(bx * I, by * I, 2.0 * I, 1.2 * I)
    c.showPage()
    c.save()
    return dict(pages=PAGES, spine_in=round(SPINE, 6), width_in=round(CW, 6), height_in=CH, bleed_in=BLEED,
                barcode_box_in=[round(bx, 4), by, 2.0, 1.2], spine_text_pt=fs)


if __name__ == "__main__":
    m = main()
    main(os.path.join(ROOT, "tmp", "standalone-04-logic-on-lantern-lane-cover-guides.pdf"), guides=True)
    print(m)
    json.dump(m, open(os.path.join(ROOT, "cover-info.json"), "w"), indent=1)
