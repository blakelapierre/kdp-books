"""KDP full-wrap paperback cover for Porch Swing Crosswords: 6x9 trim, 0.125in bleed, white paper B&W spine = pages x 0.002252in.
Reads ../build-info.json for the page count -> ../standalone-05-porch-swing-crosswords-cover.pdf"""
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
from reportlab.lib.fonts import addMapping
addMapping("Crimson", 0, 0, "Crimson"); addMapping("Crimson", 0, 1, "Crimson-I")
addMapping("Crimson", 1, 0, "Crimson-B"); addMapping("Crimson", 1, 1, "Crimson-B")

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


def mini_grid(c, x, y, cell):
    """The SUN / SWING sample from the how-to page, letters filled in."""
    sample = {(0, 3): ("S", 1), (1, 3): ("U", None), (2, 0): ("S", 2), (2, 1): ("W", None), (2, 2): ("I", None), (2, 3): ("N", None), (2, 4): ("G", None)}
    for (r, q), (ch, nn) in sample.items():
        cx, cy = x + q * cell, y + (2 - r) * cell
        c.setStrokeColor(PALE); c.setLineWidth(0.8); c.rect(cx, cy, cell, cell, stroke=1, fill=0)
        if nn:
            c.setFillColor(SOFT); c.setFont("Plex", 6); c.drawString(cx + 1.5, cy + cell - 6.5, str(nn))
        c.setFillColor(GLOW); c.setFont("Plex", cell * 0.55); c.drawCentredString(cx + cell / 2, cy + cell * 0.25, ch)


# lantern on the cover scene: x = 0.88 w, its body centre about 26 + 13 pt below the beam line at 0.86 h
LANTERN = (0.88, 0.86 - (30 + 26 * 0.55) / (4.6 * 72))


def front(c, ox, scene):
    I = inch
    W = TW * I
    c.saveState()
    cp = c.beginPath(); cp.rect(ox * I, 0, (TW + BLEED) * I, CH * I); c.clipPath(cp, stroke=0, fill=0)
    c.translate(ox * I, BLEED * I)
    sw, sh = 5.4 * I, 4.6 * I
    sx, sy = (W - sw) / 2, 0.8 * I
    c.drawImage(scene, sx, sy, sw, sh)
    glow(c, sx + LANTERN[0] * sw, sy + LANTERN[1] * sh, 38)
    c.setFillColor(PALE)
    c.setFont("PlayfairSC", 11)
    c.drawCentredString(W / 2, 8.25 * I, "Cozy Themed Crosswords for Adults")
    c.setStrokeColor(SOFT); c.setLineWidth(0.8)
    c.line(2.0 * I, 8.1 * I, 4.0 * I, 8.1 * I)
    c.setFillColor(colors.white)
    c.setFont("PlayfairSC-B", 46)
    c.drawCentredString(W / 2, 7.3 * I, "Porch Swing")
    c.drawCentredString(W / 2, 6.6 * I, "Crosswords")
    c.setFont("Crimson-I", 17)
    c.setFillColor(GLOW)
    c.drawCentredString(W / 2, 6.1 * I, "80 Puzzles Through the Seasons")
    c.setFont("PlayfairSC", 10)
    c.setFillColor(SOFT)
    c.drawCentredString(W / 2, 5.72 * I, "Easy to Medium · Plain Clues · Word Banks & Solutions")
    c.setFont("Crimson-I", 14)
    c.setFillColor(PALE)
    c.drawCentredString(W / 2, 0.42 * I, "Blake La Pierre")
    c.restoreState()


BLURB = [
    "<b>Pull up a swing, pour a glass of lemonade and sharpen your pencil.</b>",
    "Eighty friendly crosswords follow the year around: spring cleaning and the flower show, seaside days and the county fair, "
    "apple picking and soup on the stove, snow days and cocoa by the fire. Every puzzle has its own cozy theme, so the answers belong together.",
    "The clues are plain and fair: no celebrity trivia, no obscure words, no cryptic tricks. Stuck? Each puzzle has a word bank at the back, "
    "and with it the grid fills in only one way.",
]
FEATS = [
    "80 themed crosswords in four seasons, 20 in each",
    "Easy (Spring, Summer) to Medium (Autumn, Winter)",
    "Clues on the left page, a roomy grid on the right",
    "A word bank and a full solution for every puzzle",
    "Every grid checked by computer",
    "Black-and-white ink illustrations",
]


def back(c):
    I = inch
    x0 = (X_BACK + 0.55) * I
    w = (TW - 1.1) * I
    c.setFillColor(colors.white)
    c.setFont("PlayfairSC-B", 16)
    c.drawCentredString((X_BACK + TW / 2) * I, (BLEED + 8.25) * I, "A Crossword for Every Season")
    c.setStrokeColor(SOFT); c.setLineWidth(0.8)
    c.line((X_BACK + 2.1) * I, (BLEED + 8.05) * I, (X_BACK + 3.9) * I, (BLEED + 8.05) * I)
    st = ParagraphStyle("bl", fontName="Crimson", fontSize=11.5, leading=15, textColor=colors.white, alignment=TA_JUSTIFY, spaceAfter=7)
    fl = [Paragraph(t, st) for t in BLURB]
    li = ParagraphStyle("li", parent=st, alignment=TA_LEFT, fontSize=11, leading=14, leftIndent=14, firstLineIndent=-12, spaceAfter=3, textColor=PALE)
    fl += [Paragraph("•&nbsp;&nbsp;" + t, li) for t in FEATS]
    f = Frame(x0, (BLEED + 2.05) * I, w, 5.85 * I, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
    f.addFromList(fl, c)
    assert not fl, "back cover text overflow"
    gx, gy = (X_BACK + 0.6) * I, (BLEED + 0.55) * I
    mini_grid(c, gx, gy, 0.24 * I)
    tx = (X_BACK + 2.05) * I
    c.setFillColor(PALE); c.setFont("PlayfairSC", 9)
    c.drawString(tx, (BLEED + 1.55) * I, "How it works")
    c.setFont("Crimson-I", 10)
    for i, t in enumerate(["Read the clue.", "Count the squares.", "Let the crossings help.", "Stuck? Use the word bank."]):
        c.drawString(tx, (BLEED + 1.33 - i * 0.18) * I, t)
    c.setFont("PlayfairSC", 8.5); c.setFillColor(SOFT)
    c.drawString(tx, (BLEED + 0.45) * I, "Puzzles & Games")


def main(out=None, guides=False):
    if out is None:
        out = os.path.join(ROOT, "standalone-05-porch-swing-crosswords-cover.pdf")
    I = inch
    scene = night_image()
    c = canvas.Canvas(out, pagesize=(CW * I, CH * I), initialFontName="Crimson")
    c.setTitle("Porch Swing Crosswords — KDP cover")
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
    c.drawCentredString(-1.25 * I, -cap / 2, "PORCH SWING CROSSWORDS")
    c.setFillColor(GLOW)
    c.drawCentredString(1.05 * I, -cap / 2, "80 COZY THEMED CROSSWORDS")
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
    main(os.path.join(ROOT, "tmp", "standalone-05-porch-swing-crosswords-cover-guides.pdf"), guides=True)
    print(m)
    json.dump(m, open(os.path.join(ROOT, "cover-info.json"), "w"), indent=1)
