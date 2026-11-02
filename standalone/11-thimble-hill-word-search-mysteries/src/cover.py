"""KDP full-wrap paperback cover for The Thimble Hill Word Search Mysteries: 6x9 trim, 0.125in bleed, white paper B&W spine = pages x 0.002252in.
Reads ../build-info.json for the page count -> ../standalone-11-thimble-hill-word-search-mysteries-cover.pdf"""
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
BG = (0x2f, 0x3b, 0x2e)   # deep cottage-garden green
NIGHT = colors.Color(BG[0] / 255, BG[1] / 255, BG[2] / 255)
SPINEC = colors.HexColor("#263024")
PALE = colors.HexColor("#eef0e2")
SOFT = colors.HexColor("#b9c4a8")
GLOW = colors.HexColor("#f4dfa8")
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
    """A tiny word search sample: JAM hidden, leftover letters glowing."""
    rows = ["JAMP", "IEEI", "NAME"]
    for r, row in enumerate(rows):
        for q, ch in enumerate(row):
            cx, cy = x + q * cell, y + (2 - r) * cell
            c.setStrokeColor(SOFT); c.setLineWidth(0.5); c.rect(cx, cy, cell, cell, stroke=1, fill=0)
            hit = (r == 0 and q < 3)
            c.setFillColor(GLOW if not hit else PALE); c.setFont("Plex", cell * 0.55)
            c.drawCentredString(cx + cell / 2, cy + cell * 0.28, ch)
    c.setStrokeColor(GLOW); c.setLineWidth(cell * 0.75); c.setLineCap(1)
    c.setStrokeColor(colors.Color(1, 1, 1, alpha=0.25))
    c.line(x + cell * 0.5, y + 2.5 * cell, x + cell * 2.5, y + 2.5 * cell); c.setLineCap(0)


def front(c, ox, scene):
    I = inch
    W = TW * I
    c.saveState()
    cp = c.beginPath(); cp.rect(ox * I, 0, (TW + BLEED) * I, CH * I); c.clipPath(cp, stroke=0, fill=0)
    c.translate(ox * I, BLEED * I)
    sw, sh = 5.2 * I, 4.04 * I
    sx, sy = (W - sw) / 2, 0.8 * I
    c.drawImage(scene, sx, sy, sw, sh)
    c.setFillColor(PALE)
    c.setFont("PlayfairSC", 11)
    c.drawCentredString(W / 2, 8.3 * I, "60 Cozy Word Searches · 10 Gentle Mysteries")
    c.setStrokeColor(SOFT); c.setLineWidth(0.8)
    c.line(2.0 * I, 8.15 * I, 4.0 * I, 8.15 * I)
    c.setFillColor(GLOW); c.setFont("PlayfairSC", 16)
    c.drawCentredString(W / 2, 7.75 * I, "The")
    c.setFillColor(colors.white)
    c.setFont("PlayfairSC-B", 44)
    c.drawCentredString(W / 2, 7.1 * I, "Thimble Hill")
    c.setFont("PlayfairSC-B", 27)
    c.drawCentredString(W / 2, 6.55 * I, "Word Search Mysteries")
    c.setFont("Crimson-I", 15)
    c.setFillColor(GLOW)
    c.drawCentredString(W / 2, 6.1 * I, "Find the words. Read the hidden clue. Solve the case.")
    c.setFont("PlayfairSC", 10)
    c.setFillColor(SOFT)
    c.drawCentredString(W / 2, 5.75 * I, "Large 12 × 12 Grids · Three Levels · Full Solutions")
    c.setFont("Crimson-I", 14)
    c.setFillColor(PALE)
    c.drawCentredString(W / 2, 0.42 * I, "Blake La Pierre")
    c.restoreState()


BLURB = [
    "<b>Something has gone missing in Thimble Hill, and Hattie Bloom needs your sharp eyes.</b>",
    "A prize ribbon vanishes at the summer fair. A cherry pie disappears from a windowsill. A garden gnome goes for a walk. "
    "In each of ten gentle mysteries, Hattie, a retired knitter, and Pickle, her scruffy terrier, follow the clues round the village.",
    "Every case has six word searches. Find all the words, and the leftover letters spell out a clue. "
    "Collect six clues, cross off the suspects and work out who did it. No one is ever hurt. There is always a kind reason.",
]
FEATS = [
    "60 word searches in 10 cozy mysteries",
    "A hidden clue in every grid, with boxes to write it in",
    "One roomy 12 × 12 grid per page",
    "Gentle, Curious and Sharp-Eyed levels",
    "Suspect pages, case notes and full solutions",
    "Every grid checked by computer",
    "Black-and-white ink illustrations",
]


def back(c):
    I = inch
    x0 = (X_BACK + 0.55) * I
    w = (TW - 1.1) * I
    c.setFillColor(colors.white)
    c.setFont("PlayfairSC-B", 16)
    c.drawCentredString((X_BACK + TW / 2) * I, (BLEED + 8.25) * I, "Ten Little Mysteries, One Pencil")
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
    mini_grid(c, gx, gy + 0.3 * I, 0.27 * I)
    tx = (X_BACK + 2.05) * I
    c.setFillColor(PALE); c.setFont("PlayfairSC", 9)
    c.drawString(tx, (BLEED + 1.55) * I, "How it works")
    c.setFont("Crimson-I", 10)
    for i, t in enumerate(["Loop every word.", "Read the leftover letters.", "Write down the clue.", "Name the culprit."]):
        c.drawString(tx, (BLEED + 1.33 - i * 0.18) * I, t)
    c.setFont("PlayfairSC", 8.5); c.setFillColor(SOFT)
    c.drawString(tx, (BLEED + 0.45) * I, "Puzzles & Games")


def main(out=None, guides=False):
    if out is None:
        out = os.path.join(ROOT, "standalone-11-thimble-hill-word-search-mysteries-cover.pdf")
    I = inch
    scene = night_image()
    c = canvas.Canvas(out, pagesize=(CW * I, CH * I), initialFontName="Crimson")
    c.setTitle("The Thimble Hill Word Search Mysteries — KDP cover")
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
    c.drawCentredString(-1.4 * I, -cap / 2, "THIMBLE HILL WORD SEARCH MYSTERIES")
    c.setFillColor(GLOW)
    c.drawCentredString(1.15 * I, -cap / 2, "60 COZY PUZZLES")
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
    main(os.path.join(ROOT, "tmp", "standalone-11-thimble-hill-word-search-mysteries-cover-guides.pdf"), guides=True)
    print(m)
    json.dump(m, open(os.path.join(ROOT, "cover-info.json"), "w"), indent=1)
