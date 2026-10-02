"""KDP full-wrap paperback cover: 6x9 trim, 0.125in bleed, white paper B&W spine = pages x 0.002252in."""
import json, math, random, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

G = "/usr/share/fonts/truetype/sand-box/google/"
for n, p in [
    ("Crimson", "Crimson Text/CrimsonText-Regular.ttf"),
    ("Crimson-I", "Crimson Text/CrimsonText-Italic.ttf"),
    ("Crimson-B", "Crimson Text/CrimsonText-Bold.ttf"),
    ("PlayfairSC", "Playfair Display SC/PlayfairDisplaySC-Regular.ttf"),
    ("PlayfairSC-B", "Playfair Display SC/PlayfairDisplaySC-Bold.ttf"),
    ("Plex", "IBM Plex Sans Condensed/IBMPlexSansCondensed-Regular.ttf"),
]:
    pdfmetrics.registerFont(TTFont(n, G + p))
pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))

info = json.load(open(os.path.join(os.path.dirname(__file__), "..", "build-info.json")))
PAGES = info["pages"]
BLEED = 0.125
TW, TH = 6.0, 9.0
SPINE = PAGES * 0.002252
CW = BLEED + TW + SPINE + TW + BLEED
CH = BLEED + TH + BLEED
# Warm charcoal / ember grayscale palette (prints as B&W/grayscale on KDP)
INK = colors.HexColor("#1a1a1a")
CHAR = colors.HexColor("#2b2b2b")
SLATE = colors.HexColor("#3d3d3d")
ASH = colors.HexColor("#5a5a5a")
EMBER = colors.HexColor("#8a8a8a")
PALE = colors.HexColor("#d8d8d8")
SNOW = colors.HexColor("#f2f2f2")
GOLD = colors.HexColor("#c4c4c4")
X_BACK = BLEED
X_SPINE = BLEED + TW
X_FRONT = BLEED + TW + SPINE


def flame(c, x, y, s, col):
    c.setFillColor(col)
    p = c.beginPath()
    p.moveTo(x, y + 26 * s)
    p.curveTo(x + 12 * s, y + 12 * s, x + 10 * s, y, x, y)
    p.curveTo(x - 10 * s, y, x - 12 * s, y + 12 * s, x, y + 26 * s)
    p.close()
    c.drawPath(p, stroke=0, fill=1)


def hearth(c, cx, base):
    I = inch
    # mantel shelf
    c.setFillColor(CHAR)
    c.rect(cx - 1.55 * I, base + 1.55 * I, 3.1 * I, 0.18 * I, stroke=0, fill=1)
    # surround
    c.setFillColor(SLATE)
    c.rect(cx - 1.35 * I, base, 2.7 * I, 1.55 * I, stroke=0, fill=1)
    # opening
    c.setFillColor(INK)
    c.roundRect(cx - 1.05 * I, base + 0.15 * I, 2.1 * I, 1.2 * I, 6, stroke=0, fill=1)
    # fire
    for i, (dx, sc, col) in enumerate([(-0.25, 1.0, ASH), (0.0, 1.25, EMBER), (0.28, 0.95, ASH), (-0.05, 0.7, PALE)]):
        flame(c, cx + dx * I, base + 0.25 * I, sc * 0.85, col)
    # andirons
    c.setFillColor(GOLD)
    for dx in (-0.55, 0.55):
        c.rect(cx + dx * I - 3, base + 0.2 * I, 6, 0.35 * I, stroke=0, fill=1)
        c.circle(cx + dx * I, base + 0.55 * I, 5, stroke=0, fill=1)
    # rug
    c.setFillColor(SNOW)
    p = c.beginPath()
    p.moveTo(cx - 1.8 * I, base - 0.05 * I)
    p.curveTo(cx - 0.5 * I, base - 0.25 * I, cx + 0.5 * I, base - 0.25 * I, cx + 1.8 * I, base - 0.05 * I)
    p.lineTo(cx + 1.8 * I, base - 0.45 * I)
    p.curveTo(cx, base - 0.65 * I, cx - 1.8 * I, base - 0.45 * I, cx - 1.8 * I, base - 0.45 * I)
    p.close()
    c.drawPath(p, stroke=0, fill=1)


def front(c, ox):
    r = random.Random(11)
    I = inch
    c.saveState()
    cp = c.beginPath()
    cp.rect(ox * I, 0, (TW + BLEED) * I, CH * I)
    c.clipPath(cp, stroke=0, fill=0)
    c.translate(ox * I, BLEED * I)
    # soft spark dots
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.15))
    for _ in range(35):
        c.circle(r.uniform(0.2, 5.8) * I, r.uniform(2.5, 8.7) * I, r.uniform(0.6, 1.8), stroke=0, fill=1)
    hearth(c, TW * I / 2, 1.35 * I)
    W = TW * I
    c.setFillColor(colors.white)
    c.setFont("PlayfairSC", 11)
    c.drawCentredString(W / 2, 8.15 * I, "Large-Print Quote Puzzles for Adults")
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.line(2.1 * I, 8.0 * I, 3.9 * I, 8.0 * I)
    c.setFont("PlayfairSC-B", 42)
    c.drawCentredString(W / 2, 7.15 * I, "Fireside")
    c.drawCentredString(W / 2, 6.45 * I, "Cryptograms")
    c.setFont("Crimson-I", 15)
    c.setFillColor(PALE)
    c.drawCentredString(W / 2, 5.95 * I, "200 Warm Wisdom Puzzles")
    c.setFont("PlayfairSC", 10)
    c.setFillColor(GOLD)
    c.drawCentredString(W / 2, 5.55 * I, "Easy to Hard · Hints & Solutions · Unique Answers")
    c.setFont("Crimson-I", 13)
    c.setFillColor(colors.HexColor("#b0b0b0"))
    c.drawCentredString(W / 2, 0.42 * I, "Blake La Pierre")
    c.restoreState()


BLURB = [
    "<b>Pull a chair close. The fire is low, the pencil is sharp, and two hundred sayings wait in secret alphabets.</b>",
    "Each page is a classic cryptogram: every letter swapped for another, word lengths kept honest. Famous public-domain wisdom and original fireside aphorisms, from easy warm-ups with starter letters to expert puzzles with none.",
    "Every puzzle has exactly one solution, checked by an independent computer solver. Large print, room to write, hints and full answers at the back.",
]
FEATS = [
    "200 cryptogram quote puzzles in four parts",
    "50 Easy, 50 Medium, 50 Hard and 50 Expert",
    "Large-print cipher lines with write-in blanks",
    "Starter letters on Easy–Hard; none on Expert",
    "Public-domain quotes and original cozy aphorisms",
    "Hints, full solutions and a worked example",
]


def back(c):
    r = random.Random(5)
    I = inch
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.12))
    for _ in range(20):
        c.circle((X_BACK + r.uniform(0.3, 5.7)) * I, (BLEED + r.uniform(1.8, 8.6)) * I, r.uniform(0.5, 1.5), stroke=0, fill=1)
    x0 = (X_BACK + 0.55) * I
    w = (TW - 1.1) * I
    c.setFillColor(colors.white)
    c.setFont("PlayfairSC-B", 16)
    c.drawCentredString((X_BACK + TW / 2) * I, (BLEED + 8.25) * I, "Warm Wisdom in Cipher")
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.line((X_BACK + 2.1) * I, (BLEED + 8.05) * I, (X_BACK + 3.9) * I, (BLEED + 8.05) * I)
    st = ParagraphStyle("bl", fontName="Crimson", fontSize=11.5, leading=15, textColor=colors.white,
                        alignment=TA_JUSTIFY, spaceAfter=7)
    fl = [Paragraph(t, st) for t in BLURB]
    li = ParagraphStyle("li", parent=st, alignment=TA_LEFT, fontSize=11, leading=14, leftIndent=14,
                        firstLineIndent=-12, spaceAfter=3, textColor=PALE)
    fl += [Paragraph("◆&nbsp;&nbsp;" + t, li) for t in FEATS]
    f = Frame(x0, (BLEED + 2.05) * I, w, 5.85 * I, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
    f.addFromList(fl, c)
    assert not fl, "back cover text overflow"
    # sample card
    cx, cy = (X_BACK + 0.55) * I, (BLEED + 0.4) * I
    c.setFillColor(SNOW)
    c.roundRect(cx, cy, 1.7 * I, 1.45 * I, 4, stroke=0, fill=1)
    c.setFillColor(INK)
    c.setFont("PlayfairSC-B", 11)
    c.drawCentredString(cx + 0.85 * I, cy + 1.1 * I, "No. 1")
    c.setFont("Plex", 8)
    c.setFillColor(CHAR)
    c.drawCentredString(cx + 0.85 * I, cy + 0.75 * I, "A B C D  E F G")
    c.setStrokeColor(ASH)
    c.setLineWidth(0.6)
    c.line(cx + 0.2 * I, cy + 0.65 * I, cx + 1.5 * I, cy + 0.65 * I)
    c.setFont("Crimson-I", 8)
    c.setFillColor(ASH)
    c.drawCentredString(cx + 0.85 * I, cy + 0.35 * I, "write beneath")
    c.drawCentredString(cx + 0.85 * I, cy + 0.18 * I, "each letter")
    tx = (X_BACK + 2.45) * I
    LINES = ["Swap letters back", "to English.", "One mapping,", "one solution.", "Pencil recommended."]
    c.setFillColor(PALE)
    c.setFont("PlayfairSC", 9)
    c.drawString(tx, (BLEED + 1.7) * I, "Inside")
    c.setFont("Crimson-I", 10)
    for i, t in enumerate(LINES):
        c.drawString(tx, (BLEED + 1.48 - i * 0.18) * I, t)
    c.setFont("PlayfairSC", 8.5)
    c.setFillColor(GOLD)
    c.drawString(tx, (BLEED + 0.45) * I, "Puzzles & Games")
    c.setFont("Crimson-I", 9)
    c.setFillColor(PALE)
    c.drawString(tx, (BLEED + 0.28) * I, "Ages 12 and up")


def main(out=None, guides=False):
    if out is None:
        out = os.path.join(os.path.dirname(__file__), "..", "standalone-02-fireside-cryptograms-cover.pdf")
    I = inch
    c = canvas.Canvas(out, pagesize=(CW * I, CH * I), initialFontName="Crimson")
    c.setTitle("Fireside Cryptograms — KDP cover")
    c.setAuthor("Blake La Pierre")
    c.setFillColor(INK)
    c.rect(0, 0, CW * I, CH * I, stroke=0, fill=1)
    back(c)
    c.setFillColor(CHAR)
    c.rect(X_SPINE * I, 0, SPINE * I, CH * I, stroke=0, fill=1)
    assert PAGES >= 79
    fs = 8.0
    cap = 0.71 * fs
    assert cap <= (SPINE - 2 * 0.0625) * 72 + 0.01, (cap, SPINE)
    c.saveState()
    c.translate((X_SPINE + SPINE / 2) * I, (BLEED + TH / 2) * I)
    c.rotate(-90)
    c.setFillColor(colors.white)
    c.setFont("PlayfairSC-B", fs)
    c.drawCentredString(-1.0 * I, -cap / 2, "FIRESIDE CRYPTOGRAMS")
    c.setFillColor(GOLD)
    c.setFont("PlayfairSC-B", fs)
    c.drawCentredString(1.0 * I, -cap / 2, "200 LARGE-PRINT QUOTE PUZZLES")
    c.setFillColor(PALE)
    c.setFont("PlayfairSC-B", fs)
    c.drawCentredString(3.15 * I, -cap / 2, "BLAKE LA PIERRE")
    c.restoreState()
    front(c, X_FRONT)
    bx, by = X_BACK + TW - 0.25 - 2.0, BLEED + 0.25
    if guides:
        c.setLineWidth(0.6)
        c.setStrokeColor(colors.red)
        c.rect(BLEED * I, BLEED * I, (CW - 2 * BLEED) * I, TH * I)
        c.setStrokeColor(colors.magenta)
        c.line(X_SPINE * I, 0, X_SPINE * I, CH * I)
        c.line(X_FRONT * I, 0, X_FRONT * I, CH * I)
        c.setStrokeColor(colors.yellow)
        c.rect(bx * I, by * I, 2.0 * I, 1.2 * I)
    c.showPage()
    c.save()
    return dict(pages=PAGES, spine_in=round(SPINE, 6), width_in=round(CW, 6), height_in=CH,
                bleed_in=BLEED, barcode_box_in=[round(bx, 4), by, 2.0, 1.2], spine_text_pt=fs)


if __name__ == "__main__":
    root = os.path.join(os.path.dirname(__file__), "..")
    m = main()
    main(os.path.join(root, "tmp", "standalone-02-fireside-cryptograms-cover-guides.pdf"), guides=True)
    print(m)
    json.dump(m, open(os.path.join(root, "cover-info.json"), "w"), indent=1)
