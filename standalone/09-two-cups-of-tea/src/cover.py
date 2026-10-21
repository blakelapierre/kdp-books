"""KDP case-laminate HARDCOVER cover for Two Cups of Tea, 6x9 trim, white paper.

Formula (KDP "Create a Hardcover Cover", https://kdp.amazon.com/en_US/help/topic/GDTKFJPNQCBTMRV6,
cross-checked with the cover-wrap maths used for our earlier hardcovers):
  wrap      = 15 mm  = 0.5906 in on every outside edge (KDP prints "0.51 in (15 mm)"; 15 mm is 0.5906 in)
  board     = trim + 5 mm wide (0.1969 in) and + 6 mm tall (0.2362 in)  -> 6.1969 x 9.2362 in
  spine     = pages x 0.002252 in + 4.8 mm (0.1890 in)   (white paper)
  hinge     = 10 mm = 0.3937 in each side of the spine (keep text out)
  safe text = 0.635 in (16 mm) from the book edges
  full width  = 2 x wrap + 2 x board width + spine
  full height = 2 x wrap + board height
-> ../standalone-09-two-cups-of-tea-cover.pdf, ../previews/*.png and ../cover-info.json
"""
import json, os
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image

G = "/usr/share/fonts/truetype/sand-box/google/"
for n, p in [("Crimson", "Crimson Text/CrimsonText-Regular.ttf"),
             ("Crimson-I", "Crimson Text/CrimsonText-Italic.ttf"),
             ("Crimson-B", "Crimson Text/CrimsonText-Bold.ttf"),
             ("PlayfairSC", "Playfair Display SC/PlayfairDisplaySC-Regular.ttf"),
             ("PlayfairSC-B", "Playfair Display SC/PlayfairDisplaySC-Bold.ttf")]:
    pdfmetrics.registerFont(TTFont(n, G + p))

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SLUG = "standalone-09-two-cups-of-tea"
PAGES = json.load(open(os.path.join(ROOT, "build-info.json")))["pages"]
MM = 1 / 25.4
WRAP = 15 * MM
TW, TH = 6.0 + 5 * MM, 9.0 + 6 * MM
HINGE = 10 * MM
SAFE = 16 * MM
SPINE = PAGES * 0.002252 + 4.8 * MM
CW = WRAP + TW + SPINE + TW + WRAP
CH = WRAP + TH + WRAP
X_BACK, X_SPINE, X_FRONT = WRAP, WRAP + TW, WRAP + TW + SPINE

CREAM = colors.HexColor("#f4ecdc")
PAPER = (0xf4, 0xec, 0xdc)
BROWN = colors.HexColor("#3d2b22")
INKB = (0x3d, 0x2b, 0x22)
TERRA = colors.HexColor("#a9482f")
SAGE = colors.HexColor("#6f7d5c")
SOFT = colors.HexColor("#8a7663")
I = inch


def tinted_scene():
    return tinted("cover-scene")


def tinted(name):
    im = Image.open(os.path.join(ROOT, "illustrations", f"{name}.png")).convert("L")
    rgb = Image.merge("RGB", [im.point(lambda v, a=a, b=b: int(a + (b - a) * v / 255)) for a, b in zip(INKB, PAPER)])
    path = os.path.join(ROOT, "tmp", f"{name}-tinted.png")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    rgb.save(path, dpi=(300, 300))
    return path


def heart(c, cx, cy, size, col):
    import math
    p = c.beginPath()
    for i in range(41):
        t = 2 * math.pi * i / 40
        x = 16 * math.sin(t) ** 3; y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pt = (cx + x * size / 32, cy + y * size / 32 - size * 0.05)
        p.moveTo(*pt) if i == 0 else p.lineTo(*pt)
    p.close(); c.setFillColor(col); c.setStrokeColor(col); c.drawPath(p, fill=1, stroke=0)


def ornament(c, cx, y, half, col):
    c.setStrokeColor(col); c.setLineWidth(0.9)
    c.line(cx - half, y, cx - 10, y); c.line(cx + 10, y, cx + half, y)
    heart(c, cx, y, 9, col)


def front(c, scene):
    ox, oy = X_FRONT * I, WRAP * I
    w = TW * I
    cx = ox + w / 2
    # double rule frame inside the safe area
    for inset, lw in ((SAFE, 1.2), (SAFE + 0.07, 0.5)):
        c.setStrokeColor(BROWN); c.setLineWidth(lw)
        c.rect(ox + inset * I, oy + inset * I, w - 2 * inset * I, TH * I - 2 * inset * I, stroke=1, fill=0)
    c.setFillColor(SAGE); c.setFont("PlayfairSC", 11)
    c.drawCentredString(cx, oy + (TH - 1.05) * I, "A COUPLE'S QUESTION JOURNAL")
    c.setFillColor(TERRA); c.setFont("PlayfairSC-B", 46)
    c.drawCentredString(cx, oy + (TH - 1.8) * I, "Two Cups")
    c.drawCentredString(cx, oy + (TH - 2.45) * I, "of Tea")
    ornament(c, cx, oy + (TH - 2.75) * I, 1.3 * I, BROWN)
    c.setFillColor(BROWN); c.setFont("Crimson-I", 14.5)
    c.drawCentredString(cx, oy + (TH - 3.12) * I, "52 weeks of gentle questions to answer side by side")
    sw, sh = 4.3 * I, 4.3 * 5.0 / 4.9 * I
    c.drawImage(scene, cx - sw / 2, oy + 1.25 * I, sw, sh)
    c.setFillColor(BROWN); c.setFont("PlayfairSC", 14)
    c.drawCentredString(cx, oy + 0.88 * I, "BLAKE LA PIERRE")


BLURB = [
    "<b>One cup for each of you. One question at a time.</b>",
    "Two Cups of Tea is a cozy year-long journal for couples. Each week brings a gentle theme and three "
    "thoughtful questions, with separate space for each of you to answer in your own words, so you can "
    "compare notes, laugh, and learn something new about each other.",
    "Choose who is the Teacup and who is the Mug, put the kettle on, and begin wherever you are: new love, "
    "newlyweds, or many happy years in. Charming black-and-white illustrations of porches, picnics and "
    "fireside evenings follow you through the seasons.",
]
FEATS = [
    "52 weekly themes and 156 questions, arranged by season",
    "Separate answer space for each partner on every question",
    "A small \u201ctogether this week\u201d idea to tick off",
    "Season check-ins with a framed memory page",
    "Our story, our someday list and letters to each other",
    "A keepsake hardcover gift for anniversaries and weddings",
]


def back(c):
    x0 = (X_BACK + SAFE) * I
    x1 = (X_SPINE - SAFE) * I
    tw = x1 - x0
    y = (WRAP + TH - SAFE) * I - 14
    c.setFillColor(TERRA); c.setFont("PlayfairSC-B", 16); c.drawString(x0, y, "Pour Two Cups")
    y -= 10; c.setStrokeColor(BROWN); c.setLineWidth(0.8); c.line(x0, y, x0 + 150, y); y -= 18
    st = ParagraphStyle("b", fontName="Crimson", fontSize=10.5, leading=14, textColor=BROWN, alignment=TA_JUSTIFY)
    for t in BLURB:
        p = Paragraph(t, st); _, h = p.wrap(tw, 400); p.drawOn(c, x0, y - h); y -= h + 10
    y -= 6
    c.setFillColor(SAGE); c.setFont("PlayfairSC-B", 9); c.drawString(x0, y, "INSIDE"); y -= 16
    c.setFont("Crimson", 10.5); c.setFillColor(BROWN)
    for f in FEATS:
        heart(c, x0 + 3, y + 3.5, 6, TERRA); c.setFillColor(BROWN); c.drawString(x0 + 12, y, f); y -= 15
    art = tinted("thanks")
    aw = 2.6 * I; ah = aw * 540 / 960
    c.drawImage(art, (x0 + x1) / 2 - aw / 2, y - 14 - ah, aw, ah)
    return y - 14 - ah


def main(path, guides=False):
    scene = tinted_scene()
    c = canvas.Canvas(path, pagesize=(CW * I, CH * I), initialFontName="Crimson", initialFontSize=11)
    c.setTitle("Two Cups of Tea \u2014 KDP hardcover cover"); c.setAuthor("Blake La Pierre")
    c.setFillColor(CREAM); c.rect(0, 0, CW * I, CH * I, stroke=0, fill=1)
    low = back(c)
    # spine band
    c.setFillColor(TERRA); c.rect(X_SPINE * I, 0, SPINE * I, CH * I, stroke=0, fill=1)
    fs = 10.0; cap = 0.71 * fs
    assert PAGES >= 79 and cap <= (SPINE - 2 * 0.0625) * 72, (cap, SPINE)
    c.saveState(); c.translate((X_SPINE + SPINE / 2) * I, (WRAP + TH / 2) * I); c.rotate(-90)
    c.setFillColor(CREAM); c.setFont("PlayfairSC-B", fs); c.drawCentredString(-1.55 * I, -cap / 2, "TWO CUPS OF TEA")
    heart(c, 0.25 * I, 0, 7, CREAM)
    c.setFont("PlayfairSC", fs - 1); c.drawCentredString(1.3 * I, -cap / 2 * 0.9, "A COUPLE'S QUESTION JOURNAL")
    c.setFont("PlayfairSC-B", fs - 1); c.drawCentredString(3.35 * I, -cap / 2 * 0.9, "BLAKE LA PIERRE")
    c.restoreState()
    front(c, scene)
    # barcode clear box (KDP prints the barcode here): 2 x 1.2 in, >= 0.76 in from the bottom
    # of the cover's board area and 0.25 in from the hinge
    bx = X_BACK + TW - HINGE - 0.25 - 2.0
    by = WRAP + 0.76
    assert low > (by + 1.2 + 0.15) * I, "back text runs into the barcode box"
    c.setFillColor(colors.white); c.rect(bx * I, by * I, 2.0 * I, 1.2 * I, stroke=0, fill=1)
    c.setFillColor(SOFT); c.setFont("PlayfairSC", 8.5)
    c.drawString((X_BACK + SAFE) * I, (by + 0.2) * I, "COUPLES \u00b7 RELATIONSHIPS \u00b7 GIFT")
    if guides:
        c.setLineWidth(0.8)
        c.setStrokeColor(colors.red); c.rect(WRAP * I, WRAP * I, (CW - 2 * WRAP) * I, TH * I)
        c.setStrokeColor(colors.magenta); c.line(X_SPINE * I, 0, X_SPINE * I, CH * I); c.line(X_FRONT * I, 0, X_FRONT * I, CH * I)
        c.setStrokeColor(colors.orange)
        for x in (X_SPINE - HINGE, X_FRONT + HINGE): c.line(x * I, 0, x * I, CH * I)
        c.setStrokeColor(colors.blue)
        for x0 in (X_BACK, X_FRONT):
            c.rect((x0 + SAFE) * I, (WRAP + SAFE) * I, (TW - 2 * SAFE) * I, (TH - 2 * SAFE) * I)
        c.setStrokeColor(colors.green); c.rect(bx * I, by * I, 2.0 * I, 1.2 * I)
    c.showPage(); c.save()
    return dict(pages=PAGES, spine_in=round(SPINE, 4), width_in=round(CW, 4), height_in=round(CH, 4),
                wrap_in=round(WRAP, 4), board_in=[round(TW, 4), round(TH, 4)], hinge_in=round(HINGE, 4),
                safe_in=round(SAFE, 4), barcode_box_in=[round(bx, 4), round(by, 4), 2.0, 1.2],
                spine_text_pt=fs, kind="hardcover case laminate", paper="white", interior="black ink",
                formula="width = 2*15mm wrap + 2*(6in+5mm) board + spine; spine = pages*0.002252in + 4.8mm; height = 2*15mm + 9in + 6mm")


if __name__ == "__main__":
    m = main(os.path.join(ROOT, f"{SLUG}-cover.pdf"))
    main(os.path.join(ROOT, "tmp", "cover-guides.pdf"), guides=True)
    json.dump(m, open(os.path.join(ROOT, "cover-info.json"), "w"), indent=1)
    print(m)
