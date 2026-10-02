"""KDP full-wrap paperback cover: 6x9 trim, 0.125in bleed, white paper B&W spine = pages x 0.002252in.
Same palette and layout as the other Frostwood Puzzle Book covers."""
import json, math, random, sys
sys.path.insert(0, ".")
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
import build
from build import snowflake, pine, tent_icon, draw_grid, D, NP

info = json.load(open("../build-info.json")); PAGES = info["pages"]
BLEED = 0.125; TW, TH = 6.0, 9.0
SPINE = PAGES * 0.002252
CW = BLEED + TW + SPINE + TW + BLEED; CH = BLEED + TH + BLEED
NAVY = colors.HexColor("#1f3a5f"); GOLD = colors.HexColor("#ffd27a"); PALE = colors.HexColor("#dbe6f1"); SNOW = colors.HexColor("#f4f7fb")
DEEP = colors.HexColor("#15293f"); SLATE = colors.HexColor("#2c4d74"); DIM = colors.HexColor("#27405e")
X_BACK = BLEED; X_SPINE = BLEED + TW; X_FRONT = BLEED + TW + SPINE

def cottage(c, x, y, w, h, sc=1.0):
    c.setFillColor(DEEP); c.rect(x, y, w, h, stroke=0, fill=1)
    p = c.beginPath(); p.moveTo(x - 0.04 * inch, y + h); p.lineTo(x + w / 2, y + h + 0.2 * inch * sc); p.lineTo(x + w + 0.04 * inch, y + h); p.close(); c.drawPath(p, stroke=0, fill=1)
    c.setFillColor(SNOW); p = c.beginPath(); p.moveTo(x - 0.04 * inch, y + h); p.lineTo(x + w / 2, y + h + 0.2 * inch * sc); p.lineTo(x + w + 0.04 * inch, y + h)
    p.lineTo(x + w - 0.02 * inch, y + h + 0.02 * inch); p.lineTo(x + w / 2, y + h + 0.15 * inch * sc); p.lineTo(x + 0.02 * inch, y + h + 0.02 * inch); p.close(); c.drawPath(p, stroke=0, fill=1)
    c.setFillColor(GOLD)
    for i in range(int(w / (0.16 * inch))): c.rect(x + 0.05 * inch + i * 0.16 * inch, y + h * 0.45, 0.07 * inch, 0.07 * inch, stroke=0, fill=1)

def cover_pine(c, x, y, h):
    c.setFillColor(DEEP)
    for k in range(3):
        yy = y + k * h * 0.28; ww = h * (0.42 - k * 0.1)
        p = c.beginPath(); p.moveTo(x - ww, yy); p.lineTo(x, yy + h * 0.5); p.lineTo(x + ww, yy); p.close(); c.drawPath(p, stroke=0, fill=1)

def front(c, ox):
    r = random.Random(19)
    c.saveState()
    cp = c.beginPath(); cp.rect(ox * inch, 0, (TW + BLEED) * inch, CH * inch); c.clipPath(cp, stroke=0, fill=0)
    c.translate(ox * inch, BLEED * inch)
    for _ in range(36):
        snowflake(c, r.uniform(0.2, 5.8) * inch, r.uniform(2.6, 8.8) * inch, r.uniform(3, 10), colors.Color(1, 1, 1, alpha=r.uniform(0.12, 0.32)))
    # mountains
    c.setFillColor(SLATE); p = c.beginPath(); p.moveTo(-0.2 * inch, 2.0 * inch)
    for x, y in [(0.9, 3.1), (1.8, 2.5), (3.0, 4.05), (4.2, 2.6), (5.2, 3.3), (6.3, 2.4), (6.3, -0.2), (-0.2, -0.2)]: p.lineTo(x * inch, y * inch)
    p.close(); c.drawPath(p, stroke=0, fill=1)
    c.setFillColor(colors.white)
    for (px, py, s) in [(0.9, 3.1, 0.24), (3.0, 4.05, 0.34), (5.2, 3.3, 0.24)]:
        p = c.beginPath(); p.moveTo(px * inch, py * inch); p.lineTo((px - s) * inch, (py - s * 0.8) * inch); p.lineTo((px + s) * inch, (py - s * 0.8) * inch); p.close(); c.drawPath(p, stroke=0, fill=1)
    # lodge on the peak shoulder
    lx, ly = 3.55 * inch, 3.02 * inch
    c.setFillColor(DEEP); c.rect(lx, ly, 0.5 * inch, 0.3 * inch, stroke=0, fill=1)
    p = c.beginPath(); p.moveTo(lx - 0.05 * inch, ly + 0.3 * inch); p.lineTo(lx + 0.25 * inch, ly + 0.46 * inch); p.lineTo(lx + 0.55 * inch, ly + 0.3 * inch); p.close(); c.drawPath(p, stroke=0, fill=1)
    c.setFillColor(GOLD)
    for i in range(4):
        for j in range(2): c.rect(lx + (0.06 + i * 0.105) * inch, ly + (0.06 + j * 0.11) * inch, 0.05 * inch, 0.05 * inch, stroke=0, fill=1)
    # dashed trail up through the pines
    c.setStrokeColor(colors.Color(1, 1, 1, alpha=0.5)); c.setLineWidth(1.2); c.setDash(2, 3)
    p = c.beginPath(); p.moveTo(1.8 * inch, 1.55 * inch); p.lineTo(2.8 * inch, 2.0 * inch); p.lineTo(2.3 * inch, 2.4 * inch); p.lineTo(3.4 * inch, 2.85 * inch); p.lineTo(3.7 * inch, 3.02 * inch)
    c.drawPath(p, stroke=1, fill=0); c.setDash()
    # snowy foreground grove with tents
    c.setFillColor(SNOW); p = c.beginPath(); p.moveTo(-0.2 * inch, 1.55 * inch)
    p.curveTo(1.5 * inch, 1.78 * inch, 3.8 * inch, 1.4 * inch, 6.3 * inch, 1.65 * inch); p.lineTo(6.3 * inch, -0.2 * inch); p.lineTo(-0.2 * inch, -0.2 * inch); p.close()
    c.drawPath(p, stroke=0, fill=1)
    for x, h in [(0.4, 0.55), (0.75, 0.4), (1.15, 0.62), (4.9, 0.5), (5.3, 0.68), (5.7, 0.45)]:
        cover_pine(c, x * inch, 1.45 * inch, h * inch)
    # tents in the clearing (gold/deep)
    for tx, ty, sc in [(2.0, 1.55, 0.42), (2.7, 1.48, 0.5), (3.5, 1.58, 0.38)]:
        c.setFillColor(DEEP)
        p = c.beginPath(); p.moveTo(tx * inch - sc * 0.5 * inch, ty * inch); p.lineTo(tx * inch, ty * inch + sc * 0.7 * inch); p.lineTo(tx * inch + sc * 0.5 * inch, ty * inch); p.close()
        c.drawPath(p, stroke=0, fill=1)
        c.setFillColor(GOLD); c.circle(tx * inch, ty * inch + sc * 0.22 * inch, 0.04 * inch, stroke=0, fill=1)
    cottage(c, 4.1 * inch, 1.48 * inch, 0.42 * inch, 0.24 * inch)
    W = TW * inch
    c.setFillColor(colors.white); c.setFont("PlayfairSC", 11.5); c.drawCentredString(W / 2, 8.1 * inch, "A Pine-Grove Puzzle Book")
    c.setStrokeColor(GOLD); c.setLineWidth(0.8); c.line(2.2 * inch, 7.95 * inch, 3.8 * inch, 7.95 * inch)
    c.setFont("PlayfairSC-B", 48); c.drawCentredString(W / 2, 7.08 * inch, "Tents in"); c.drawCentredString(W / 2, 6.35 * inch, "Frostwood")
    c.setFont("Crimson-I", 17); c.setFillColor(PALE)
    c.drawCentredString(W / 2, 5.68 * inch, f"{NP} Tents and Trees Logic Puzzles")
    c.setFont("Crimson-I", 14); c.drawCentredString(W / 2, 5.38 * inch, "from the meadow to the ridge")
    c.setFont("PlayfairSC", 10.5); c.setFillColor(GOLD)
    c.drawCentredString(W / 2, 4.9 * inch, "Easy to Expert · Big, Clear Grids · Solutions Included")
    c.setFillColor(NAVY); c.setFont("PlayfairSC", 11); c.drawCentredString(W / 2, 0.72 * inch, "A Frostwood Puzzle Book")
    c.setFont("Crimson-I", 13); c.setFillColor(colors.HexColor("#3a4d66")); c.drawCentredString(W / 2, 0.44 * inch, "Blake La Pierre")
    c.restoreState()

cnt = {b: len(D[b]) for b in ("Easy", "Medium", "Hard", "Expert")}
BLURB = [
 "<b>Each winter the Frostwood campers pitch their tents beside the mountain pines. This year the trail maps are smudged, and every clearing needs its tents put back.</b>",
 f"{NP} clearings wait between the lodge meadow and the ridge. Each one is a Tents puzzle (also called Tents and Trees): place one tent beside every pine, keep the tents from touching even at the corners, and match the numbers on the rows and columns.",
 "Every puzzle has exactly one solution, checked by computer, and every one can be solved by logic alone, with no guessing.",
]
FEATS = [f"{NP} Tents and Trees puzzles in four parts, from 6×6 to 12×12",
         f"{cnt['Easy']} Easy, {cnt['Medium']} Medium, {cnt['Hard']} Hard and {cnt['Expert']} Expert",
         "Large, clear grids with room for pencil marks",
         "How-to-play guide with a fully worked example",
         "Complete solutions at the back",
         "Book four of the cozy Frostwood Puzzle Books"]

def back(c):
    r = random.Random(5)
    for _ in range(18):
        snowflake(c, (X_BACK + r.uniform(0.2, 5.8)) * inch, (BLEED + r.uniform(2.0, 8.8)) * inch, r.uniform(3, 8), colors.Color(1, 1, 1, alpha=r.uniform(0.1, 0.22)))
    x0 = (X_BACK + 0.55) * inch; w = (TW - 1.1) * inch
    c.setFillColor(colors.white); c.setFont("PlayfairSC-B", 18)
    c.drawCentredString((X_BACK + TW / 2) * inch, (BLEED + 8.1) * inch, "Camp Among the Pines")
    c.setStrokeColor(GOLD); c.setLineWidth(0.8); c.line((X_BACK + 2.2) * inch, (BLEED + 7.9) * inch, (X_BACK + 3.8) * inch, (BLEED + 7.9) * inch)
    st = ParagraphStyle("bl", fontName="Crimson", fontSize=12, leading=16, textColor=colors.white, alignment=TA_JUSTIFY, spaceAfter=7)
    fl = [Paragraph(t, st) for t in BLURB]
    li = ParagraphStyle("li", parent=st, alignment=TA_LEFT, fontSize=11.3, leading=14.5, leftIndent=14, firstLineIndent=-12, spaceAfter=3, textColor=PALE)
    fl += [Paragraph("<font name='DejaVu' color='#ffd27a' size='8'>❄</font>&nbsp;&nbsp;" + t, li) for t in FEATS]
    f = Frame(x0, (BLEED + 2.05) * inch, w, 5.7 * inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
    f.addFromList(fl, c); assert not fl, "back cover text overflow"
    p = D["Easy"][0]; cs = 0.20 * inch; n = p["n"]
    cx, cy = (X_BACK + 0.55) * inch, (BLEED + 0.35) * inch
    c.setFillColor(colors.white); c.roundRect(cx, cy, 1.85 * inch, 1.78 * inch, 4, stroke=0, fill=1)
    draw_grid(c, cx + 0.12 * inch, cy + 0.12 * inch, cs, p)
    tx = (X_BACK + 2.55) * inch
    LINES = ["One tent beside", "every pine.", "Tents never touch,", "not even diagonally.", "Match the numbers."]
    c.setFillColor(PALE); c.setFont("PlayfairSC", 9.5); c.drawString(tx, (BLEED + 1.75) * inch, "Puzzle No. 1")
    c.setFont("Crimson-I", 10)
    for i, t in enumerate(LINES): c.drawString(tx, (BLEED + 1.53 - i * 0.18) * inch, t)
    c.setFont("PlayfairSC", 8.5); c.setFillColor(GOLD); c.drawString(tx, (BLEED + 0.45) * inch, "Puzzles & Games")
    c.setFont("Crimson-I", 9); c.setFillColor(PALE); c.drawString(tx, (BLEED + 0.28) * inch, "Ages 12 and up")

def main(out="../frostwood-04-tents-in-frostwood-cover.pdf", guides=False):
    c = canvas.Canvas(out, pagesize=(CW * inch, CH * inch))
    c.setTitle("Tents in Frostwood — KDP cover"); c.setAuthor("Blake La Pierre")
    c.setFillColor(NAVY); c.rect(0, 0, CW * inch, CH * inch, stroke=0, fill=1)
    back(c)
    c.setFillColor(colors.HexColor("#17304f")); c.rect(X_SPINE * inch, 0, SPINE * inch, CH * inch, stroke=0, fill=1)
    assert PAGES >= 79 and SPINE >= 0.25
    c.saveState(); c.translate((X_SPINE + SPINE / 2) * inch, (BLEED + TH / 2) * inch); c.rotate(-90)
    c.setFillColor(colors.white); c.setFont("PlayfairSC-B", 13); c.drawCentredString(-0.9 * inch, -4.5, "Tents in Frostwood")
    c.setFillColor(GOLD); c.setFont("Crimson-I", 9.5); c.drawCentredString(1.2 * inch, -3.3, f"{NP} Tents Puzzles")
    c.setFillColor(PALE); c.setFont("Crimson-I", 11); c.drawCentredString(2.95 * inch, -3.8, "Blake La Pierre")
    c.restoreState()
    front(c, X_FRONT)
    bx, by = X_BACK + TW - 0.25 - 2.0, BLEED + 0.25
    if guides:
        c.setLineWidth(0.6)
        c.setStrokeColor(colors.red); c.rect(BLEED * inch, BLEED * inch, (CW - 2 * BLEED) * inch, TH * inch)
        c.setStrokeColor(colors.magenta); c.line(X_SPINE * inch, 0, X_SPINE * inch, CH * inch); c.line(X_FRONT * inch, 0, X_FRONT * inch, CH * inch)
        c.setStrokeColor(colors.lime); c.setDash(3, 3)
        c.rect((X_BACK + 0.125) * inch, (BLEED + 0.125) * inch, (TW - 0.25) * inch, (TH - 0.25) * inch)
        c.rect((X_FRONT + 0.125) * inch, (BLEED + 0.125) * inch, (TW - 0.25) * inch, (TH - 0.25) * inch)
        c.setStrokeColor(colors.yellow); c.setDash()
        c.rect(bx * inch, by * inch, 2.0 * inch, 1.2 * inch)
    c.showPage(); c.save()
    return dict(pages=PAGES, spine_in=round(SPINE, 6), width_in=round(CW, 6), height_in=CH, barcode_box_in=[round(bx, 4), by, 2.0, 1.2])

if __name__ == "__main__":
    m = main(); main("../tmp/frostwood-04-tents-in-frostwood-cover-guides.pdf", guides=True)
    print(m); json.dump(m, open("../cover-info.json", "w"), indent=1)
