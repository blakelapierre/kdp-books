"""KDP full-wrap paperback cover: 6x9 trim, 0.125in bleed, white paper B&W spine = pages x 0.002252in."""
import json, math, random, sys
sys.path.insert(0, ".")
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
import build
from build import snowflake, draw_grid, D

info = json.load(open("../build-info.json")); PAGES = info["pages"]
BLEED = 0.125; TW, TH = 6.0, 9.0
SPINE = PAGES * 0.002252
CW = BLEED + TW + SPINE + TW + BLEED; CH = BLEED + TH + BLEED
NAVY = colors.HexColor("#1f3a5f"); GOLD = colors.HexColor("#ffd27a"); PALE = colors.HexColor("#dbe6f1"); SNOW = colors.HexColor("#f4f7fb")
DEEP = colors.HexColor("#15293f"); SLATE = colors.HexColor("#2c4d74"); DIM = colors.HexColor("#27405e")
X_BACK = BLEED; X_SPINE = BLEED + TW; X_FRONT = BLEED + TW + SPINE

def train(c, x, y, sc=1.0):
    """Little locomotive + 3 carriages, facing left, lit windows. (x, y) = rail level, left end."""
    c.saveState(); c.translate(x, y); c.scale(sc, sc)
    c.setFillColor(DEEP); c.setStrokeColor(DEEP)
    for k in range(3):
        bx = 70 + k * 50
        c.roundRect(bx, 5, 46, 21, 3, stroke=0, fill=1)
        c.setFillColor(GOLD)
        for j in range(3): c.rect(bx + 5 + j * 13.5, 13, 9, 8, stroke=0, fill=1)
        c.setFillColor(DEEP)
        for wx in (bx + 10, bx + 36): c.circle(wx, 4, 3.6, stroke=0, fill=1)
    c.rect(8, 5, 56, 16, stroke=0, fill=1)                    # boiler
    c.rect(44, 5, 22, 29, stroke=0, fill=1)                   # cab
    c.setFillColor(GOLD); c.rect(49, 22, 12, 8, stroke=0, fill=1)
    c.setFillColor(DEEP); c.rect(15, 21, 8, 10, stroke=0, fill=1)
    p = c.beginPath(); p.moveTo(8, 5); p.lineTo(-2, 5); p.lineTo(8, 15); p.close(); c.drawPath(p, stroke=0, fill=1)
    c.setFillColor(GOLD); c.circle(4, 13, 2.2, stroke=0, fill=1)        # headlamp
    c.setFillColor(DEEP)
    for wx in (18, 33, 55): c.circle(wx, 4, 5, stroke=0, fill=1)
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.55))
    for dx, dy, rr in [(22, 38, 5.5), (32, 47, 7.5), (46, 55, 9.5)]: c.circle(dx, dy, rr, stroke=0, fill=1)
    c.restoreState()

def front(c, ox):
    r = random.Random(11)
    c.saveState()
    cp = c.beginPath(); cp.rect(ox * inch, 0, (TW + BLEED) * inch, CH * inch); c.clipPath(cp, stroke=0, fill=0)
    c.translate(ox * inch, BLEED * inch)
    for _ in range(40):
        snowflake(c, r.uniform(0.2, 5.8) * inch, r.uniform(2.6, 8.8) * inch, r.uniform(3, 11), colors.Color(1, 1, 1, alpha=r.uniform(0.12, 0.35)))
    # mountains
    c.setFillColor(SLATE); p = c.beginPath(); p.moveTo(-0.2 * inch, 2.0 * inch)
    for x, y in [(0.9, 3.1), (1.8, 2.5), (3.0, 4.05), (4.2, 2.6), (5.2, 3.3), (6.3, 2.4), (6.3, -0.2), (-0.2, -0.2)]: p.lineTo(x * inch, y * inch)
    p.close(); c.drawPath(p, stroke=0, fill=1)
    c.setFillColor(colors.white)
    for (px, py, s) in [(0.9, 3.1, 0.24), (3.0, 4.05, 0.34), (5.2, 3.3, 0.24)]:
        p = c.beginPath(); p.moveTo(px * inch, py * inch); p.lineTo((px - s) * inch, (py - s * 0.8) * inch); p.lineTo((px + s) * inch, (py - s * 0.8) * inch); p.close(); c.drawPath(p, stroke=0, fill=1)
    # the lodge (book one) on a shoulder of the big peak
    lx, ly = 3.55 * inch, 3.02 * inch
    c.setFillColor(DEEP); c.rect(lx, ly, 0.5 * inch, 0.3 * inch, stroke=0, fill=1)
    p = c.beginPath(); p.moveTo(lx - 0.05 * inch, ly + 0.3 * inch); p.lineTo(lx + 0.25 * inch, ly + 0.46 * inch); p.lineTo(lx + 0.55 * inch, ly + 0.3 * inch); p.close(); c.drawPath(p, stroke=0, fill=1)
    c.setFillColor(GOLD)
    for i in range(4):
        for j in range(2): c.rect(lx + (0.06 + i * 0.105) * inch, ly + (0.06 + j * 0.11) * inch, 0.05 * inch, 0.05 * inch, stroke=0, fill=1)
    # winding track up the mountain (dashed sleepers)
    c.setStrokeColor(colors.Color(1, 1, 1, alpha=0.5)); c.setLineWidth(1.3); c.setDash(2, 3)
    p = c.beginPath(); p.moveTo(5.6 * inch, 1.72 * inch); p.curveTo(5.0 * inch, 2.3 * inch, 3.2 * inch, 2.0 * inch, 4.0 * inch, 2.55 * inch)
    p.curveTo(4.5 * inch, 2.85 * inch, 3.9 * inch, 2.95 * inch, 3.8 * inch, 3.02 * inch); c.drawPath(p, stroke=1, fill=0); c.setDash()
    # viaduct
    deck = 1.72 * inch; c.setFillColor(DEEP)
    c.rect(-0.2 * inch, deck - 0.12 * inch, 6.4 * inch, 0.12 * inch, stroke=0, fill=1)
    span = 0.75 * inch
    for i in range(-1, 9):
        x = i * span
        c.rect(x - 0.07 * inch, 0.9 * inch, 0.14 * inch, deck - 0.9 * inch, stroke=0, fill=1)
        p = c.beginPath(); p.moveTo(x, deck - 0.12 * inch); p.lineTo(x + span, deck - 0.12 * inch); p.lineTo(x + span, deck - 0.28 * inch)
        p.arcTo(x, 0.95 * inch, x + span, deck - 0.1 * inch, 0, 180); p.close(); c.drawPath(p, stroke=0, fill=1)
    c.setStrokeColor(GOLD); c.setLineWidth(0.7); c.line(-0.2 * inch, deck, 6.4 * inch, deck)
    train(c, 1.25 * inch, deck + 1, 1.05)
    # snowy foreground
    c.setFillColor(SNOW); p = c.beginPath(); p.moveTo(-0.2 * inch, 1.08 * inch)
    p.curveTo(1.5 * inch, 1.3 * inch, 3.8 * inch, 0.95 * inch, 6.3 * inch, 1.2 * inch); p.lineTo(6.3 * inch, -0.2 * inch); p.lineTo(-0.2 * inch, -0.2 * inch); p.close()
    c.drawPath(p, stroke=0, fill=1)
    W = TW * inch
    c.setFillColor(colors.white); c.setFont("PlayfairSC", 11.5); c.drawCentredString(W / 2, 8.1 * inch, "A Snowy Mountain Railway Puzzle Book")
    c.setStrokeColor(GOLD); c.setLineWidth(0.8); c.line(2.2 * inch, 7.95 * inch, 3.8 * inch, 7.95 * inch)
    c.setFont("PlayfairSC-B", 50); c.drawCentredString(W / 2, 7.08 * inch, "Frostwood"); c.drawCentredString(W / 2, 6.35 * inch, "Express")
    c.setFont("Crimson-I", 17); c.setFillColor(PALE)
    c.drawCentredString(W / 2, 5.68 * inch, "200 Train Tracks Logic Puzzles")
    c.setFont("Crimson-I", 14); c.drawCentredString(W / 2, 5.38 * inch, "from the foothills to the summit")
    c.setFont("PlayfairSC", 10.5); c.setFillColor(GOLD)
    c.drawCentredString(W / 2, 4.9 * inch, "Easy to Expert · Big, Clear Grids · Solutions Included")
    c.setFillColor(NAVY); c.setFont("PlayfairSC", 11); c.drawCentredString(W / 2, 0.72 * inch, "A Frostwood Puzzle Book")
    c.setFont("Crimson-I", 13); c.setFillColor(colors.HexColor("#3a4d66")); c.drawCentredString(W / 2, 0.44 * inch, "Blake La Pierre")
    c.restoreState()

BLURB = [
 "<b>The snow came down all night. Now the line to the mountain is buried, and the Frostwood Express can’t run until the track is re-laid.</b>",
 "Two hundred stretches of line lie between the valley and the old lodge at the summit. On each one, the numbers beside the rows and columns tell you how many squares hold track, and a few pieces are already in place. Your job: lay one unbroken track from A to B.",
 "Every puzzle has exactly one solution, checked by computer, and every one can be solved by logic alone, with no guessing.",
]
FEATS = ["200 Train Tracks puzzles in four parts, from 6×6 to 12×12",
         "50 Easy, 50 Medium, 50 Hard and 50 Expert, in order of difficulty",
         "Large, clear grids with room for pencil, one or two per page",
         "How-to-play guide with a fully worked example",
         "Complete solutions at the back",
         "A calm, cozy companion to The Thief Stayed the Night"]

def back(c):
    r = random.Random(5)
    for _ in range(22):
        snowflake(c, (X_BACK + r.uniform(0.2, 5.8)) * inch, (BLEED + r.uniform(1.6, 8.8)) * inch, r.uniform(3, 8), colors.Color(1, 1, 1, alpha=r.uniform(0.1, 0.25)))
    x0 = (X_BACK + 0.55) * inch; w = (TW - 1.1) * inch
    c.setFillColor(colors.white); c.setFont("PlayfairSC-B", 18)
    c.drawCentredString((X_BACK + TW / 2) * inch, (BLEED + 8.25) * inch, "All Aboard for Frostwood")
    c.setStrokeColor(GOLD); c.setLineWidth(0.8); c.line((X_BACK + 2.2) * inch, (BLEED + 8.05) * inch, (X_BACK + 3.8) * inch, (BLEED + 8.05) * inch)
    st = ParagraphStyle("bl", fontName="Crimson", fontSize=12, leading=16, textColor=colors.white, alignment=TA_JUSTIFY, spaceAfter=7)
    fl = [Paragraph(t, st) for t in BLURB]
    li = ParagraphStyle("li", parent=st, alignment=TA_LEFT, fontSize=11.3, leading=14.5, leftIndent=14, firstLineIndent=-12, spaceAfter=3, textColor=PALE)
    fl += [Paragraph("<font name='DejaVu' color='#ffd27a' size='8'>❄</font>&nbsp;&nbsp;" + t, li) for t in FEATS]
    f = Frame(x0, (BLEED + 2.0) * inch, w, 5.9 * inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
    f.addFromList(fl, c); assert not fl, "back cover text overflow"
    # a sample puzzle card, lower left (clear of the barcode area)
    p = D["Easy"][0]; cs = 0.2 * inch; n = p["n"]
    cx, cy = (X_BACK + 0.55) * inch, (BLEED + 0.4) * inch
    c.setFillColor(colors.white); c.roundRect(cx, cy, 1.75 * inch, 1.72 * inch, 4, stroke=0, fill=1)
    draw_grid(c, cx + 0.3 * inch, cy + 0.3 * inch, cs, p, fs=7)
    tx = (X_BACK + 2.45) * inch
    LINES = ["Lay one track", "from A to B.", "Each number counts", "the track squares", "in its row or column."]
    c.setFillColor(PALE); c.setFont("PlayfairSC", 9.5); c.drawString(tx, (BLEED + 1.75) * inch, "Puzzle No. 1")
    c.setFont("Crimson-I", 10)
    for i, t in enumerate(LINES):
        c.drawString(tx, (BLEED + 1.53 - i * 0.18) * inch, t)
    c.setFont("PlayfairSC", 8.5); c.setFillColor(GOLD); c.drawString(tx, (BLEED + 0.45) * inch, "Puzzles & Games")
    c.setFont("Crimson-I", 9); c.setFillColor(PALE); c.drawString(tx, (BLEED + 0.28) * inch, "Ages 12 and up")
    assert tx + max(c.stringWidth(t, "Crimson-I", 10) for t in LINES) < (X_BACK + TW - 0.25 - 2.0) * inch - 6

def main(out="../cover.pdf", guides=False):
    c = canvas.Canvas(out, pagesize=(CW * inch, CH * inch))
    c.setTitle("Frostwood Express — KDP cover"); c.setAuthor("Blake La Pierre")
    c.setFillColor(NAVY); c.rect(0, 0, CW * inch, CH * inch, stroke=0, fill=1)
    back(c)
    c.setFillColor(colors.HexColor("#17304f")); c.rect(X_SPINE * inch, 0, SPINE * inch, CH * inch, stroke=0, fill=1)
    assert PAGES >= 79 and SPINE >= 0.25
    c.saveState(); c.translate((X_SPINE + SPINE / 2) * inch, (BLEED + TH / 2) * inch); c.rotate(-90)
    c.setFillColor(colors.white); c.setFont("PlayfairSC-B", 13); c.drawCentredString(-0.9 * inch, -4.5, "Frostwood Express")
    c.setFillColor(GOLD); c.setFont("Crimson-I", 9.5); c.drawCentredString(1.05 * inch, -3.3, "200 Train Tracks Puzzles")
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
    m = main(); main("../tmp/cover-guides.pdf", guides=True)
    print(m); json.dump(m, open("../cover-info.json", "w"), indent=1)
