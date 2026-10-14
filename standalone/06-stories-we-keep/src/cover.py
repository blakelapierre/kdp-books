"""KDP case-laminate HARDCOVER cover, 6x9 trim, white paper.
Spec from Advent Clock hardcover (cover_hardcover.py) + KDP Create a Hardcover Cover help
https://kdp.amazon.com/help/topic/GDTKFJPNQCBTMRV6 :
  wrap/bleed 0.591 in (15 mm class), boards = trim + 0.197 W / + 0.236 H,
  spine = pages * 0.002252 + 0.189, hinge 0.394 in, text >= 0.635 in from book edges.
-> ../standalone-06-stories-we-keep-cover.pdf and ../cover-info.json
"""
import json, os, sys, random
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
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
info = json.load(open(os.path.join(ROOT, "build-info.json")))
PAGES = info["pages"]
BLEED = 0.591
TW, TH = 6.0 + 0.197, 9.0 + 0.236  # board size
HINGE = 0.394
SAFE = 0.635
SPINE = PAGES * 0.002252 + 0.189
CW = BLEED + TW + SPINE + TW + BLEED
CH = BLEED + TH + BLEED
X_BACK = BLEED
X_SPINE = BLEED + TW
X_FRONT = BLEED + TW + SPINE

NAVY = colors.HexColor("#1a2433")
SLATE = colors.HexColor("#2a3a4d")
PALE = colors.HexColor("#d8dee6")
SOFT = colors.HexColor("#a8b2c0")
GLOW = colors.HexColor("#f0e6c8")
BG = (0x1a, 0x24, 0x33)

def night_scene():
    im = Image.open(os.path.join(ROOT, "illustrations", "cover-scene.png")).convert("L")
    inv = im.point(lambda v: 255 - v)
    rgb = Image.merge("RGB", [inv.point(lambda v, b=b: int(b + (230 - b) * v / 255)) for b in BG])
    path = os.path.join(ROOT, "tmp", "cover-scene-night.png")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    rgb.save(path, dpi=(300, 300))
    return path

def front(c, ox, scene):
    I = inch
    W = TW * I
    c.saveState()
    cp = c.beginPath(); cp.rect(ox * I, 0, (TW + BLEED) * I, CH * I); c.clipPath(cp, stroke=0, fill=0)
    c.translate(ox * I, BLEED * I)
    # scene
    sw, sh = 5.0 * I, 5.4 * I
    sx, sy = (W - sw) / 2, 0.85 * I
    c.drawImage(scene, sx, sy, sw, sh)
    c.setFillColor(PALE)
    c.setFont("PlayfairSC", 10)
    c.drawCentredString(W / 2, 8.45 * I, "A Guided Memory Keepsake")
    c.setStrokeColor(SOFT); c.setLineWidth(0.8)
    c.line(1.8 * I, 8.28 * I, 4.4 * I, 8.28 * I)
    c.setFillColor(colors.white)
    c.setFont("PlayfairSC-B", 36)
    c.drawCentredString(W / 2, 7.55 * I, "Stories")
    c.drawCentredString(W / 2, 6.95 * I, "We Keep")
    c.setFont("Crimson-I", 13)
    c.setFillColor(GLOW)
    c.drawCentredString(W / 2, 6.45 * I, "For the ones we love")
    c.setFont("PlayfairSC", 9)
    c.setFillColor(SOFT)
    c.drawCentredString(W / 2, 6.1 * I, "Writing Prompts · Family Tree · Letters to Leave")
    c.setFont("Crimson-I", 13)
    c.setFillColor(PALE)
    c.drawCentredString(W / 2, 0.55 * I, "Blake La Pierre")
    c.restoreState()

BLURB = [
    "<b>Some stories only live as long as someone remembers to write them down.</b>",
    "This hardcover keepsake invites a parent or grandparent — or anyone whose life you want to hold on to — to answer gentle prompts about childhood, home, love, work, holidays, favorites and the wisdom they hope to leave behind.",
    "There is room for a family tree, a simple timeline, letters to children and grandchildren, and extra lined pages when a story needs more space. Black-and-white ink drawings of cottages, lamps and fireside rooms make each section feel like home.",
]
FEATS = [
    "Eight life chapters with guided writing prompts",
    "Pages for a family tree and a simple timeline",
    "Letter pages to children, grandchildren and the giver",
    "Extra lined pages for longer stories",
    "Black-and-white ink illustrations throughout",
    "A lasting hardcover gift for holidays, birthdays and milestones",
]

def back(c):
    I = inch
    c.setFillColor(colors.white)
    c.setFont("PlayfairSC-B", 14)
    # stay clear of hinge and wrap: text inset by SAFE from board edge, and HINGE from spine
    x0 = (X_BACK + SAFE) * I
    x1 = (X_SPINE - HINGE - 0.05) * I
    tw = x1 - x0
    y = (BLEED + TH - SAFE) * I - 10
    c.drawString(x0, y, "KEEP THE STORIES")
    y -= 8
    c.setStrokeColor(SOFT); c.setLineWidth(0.7); c.line(x0, y, x0 + 120, y)
    y -= 18
    style = ParagraphStyle("b", fontName="Crimson", fontSize=9.5, leading=12.5, textColor=PALE, alignment=TA_JUSTIFY)
    for para in BLURB:
        p = Paragraph(para, style)
        w, h = p.wrap(tw, 200)
        p.drawOn(c, x0, y - h)
        y -= h + 10
    y -= 6
    c.setFillColor(GLOW); c.setFont("PlayfairSC", 8)
    c.drawString(x0, y, "INSIDE")
    y -= 14
    c.setFont("Crimson", 9.5); c.setFillColor(PALE)
    for f in FEATS:
        c.drawString(x0, y, "•  " + f); y -= 13
    # genre label above barcode zone
    c.setFillColor(SOFT); c.setFont("PlayfairSC", 8)
    c.drawString(x0, (BLEED + 0.76 + 1.35) * I, "FAMILY · MEMORY · GIFT")

def main(path=None, guides=False):
    path = path or os.path.join(ROOT, "standalone-06-stories-we-keep-cover.pdf")
    scene = night_scene()
    c = canvas.Canvas(path, pagesize=(CW * inch, CH * inch))
    c.setTitle("Stories We Keep — KDP hardcover cover")
    c.setAuthor("Blake La Pierre")
    I = inch
    c.setFillColor(NAVY); c.rect(0, 0, CW * I, CH * I, stroke=0, fill=1)
    back(c)
    c.setFillColor(SLATE); c.rect(X_SPINE * I, 0, SPINE * I, CH * I, stroke=0, fill=1)
    assert PAGES > 79
    fs = 8.0; cap = 0.71 * fs
    assert cap <= (SPINE - 2 * 0.0625) * 72 + 0.01, (cap, SPINE)
    c.saveState(); c.translate((X_SPINE + SPINE / 2) * I, (BLEED + TH / 2) * I); c.rotate(-90)
    c.setFillColor(colors.white); c.setFont("PlayfairSC-B", fs); c.drawCentredString(-1.2 * I, -cap / 2, "STORIES WE KEEP")
    c.setFillColor(GLOW); c.setFont("PlayfairSC-B", fs); c.drawCentredString(1.1 * I, -cap / 2, "A MEMORY KEEPSAKE")
    c.setFillColor(PALE); c.setFont("PlayfairSC-B", fs); c.drawCentredString(3.4 * I, -cap / 2, "BLAKE LA PIERRE")
    c.restoreState()
    front(c, X_FRONT, scene)
    # barcode clear box (KDP fills this)
    bx = X_BACK + TW - HINGE - 0.25 - 2.0
    by = BLEED + 0.76
    c.setFillColor(colors.white)
    c.rect(bx * I, by * I, 2.0 * I, 1.2 * I, stroke=0, fill=1)
    if guides:
        c.setLineWidth(0.8)
        c.setStrokeColor(colors.red); c.rect(BLEED * I, BLEED * I, (CW - 2 * BLEED) * I, TH * I)
        c.setStrokeColor(colors.magenta); c.line(X_SPINE * I, 0, X_SPINE * I, CH * I); c.line(X_FRONT * I, 0, X_FRONT * I, CH * I)
        c.setStrokeColor(colors.orange)
        for x in (X_SPINE - HINGE, X_FRONT + HINGE): c.line(x * I, 0, x * I, CH * I)
        c.setStrokeColor(colors.yellow); c.rect(bx * I, by * I, 2.0 * I, 1.2 * I)
    c.showPage(); c.save()
    meta = dict(pages=PAGES, spine_in=round(SPINE, 6), width_in=round(CW, 6), height_in=round(CH, 6),
                bleed_in=BLEED, barcode_box_in=[round(bx, 4), by, 2.0, 1.2], spine_text_pt=fs,
                wrap_in=BLEED, hinge_in=HINGE, board_in=[TW, TH], kind="hardcover case laminate")
    return meta

if __name__ == "__main__":
    m = main()
    main(os.path.join(ROOT, "tmp", "cover-hardcover-guides.pdf"), guides=True)
    json.dump(m, open(os.path.join(ROOT, "cover-info.json"), "w"), indent=1)
    print(m)
