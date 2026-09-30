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
from build import snowflake, star, draw_grid, D, NP

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

def pine(c, x, y, h):
    c.setFillColor(DEEP)
    for k in range(3):
        yy = y + k * h * 0.28; ww = h * (0.42 - k * 0.1)
        p = c.beginPath(); p.moveTo(x - ww, yy); p.lineTo(x, yy + h * 0.5); p.lineTo(x + ww, yy); p.close(); c.drawPath(p, stroke=0, fill=1)

def front(c, ox):
    r = random.Random(23)
    c.saveState()
    cp = c.beginPath(); cp.rect(ox * inch, 0, (TW + BLEED) * inch, CH * inch); c.clipPath(cp, stroke=0, fill=0)
    c.translate(ox * inch, BLEED * inch)
    for _ in range(26):
        snowflake(c, r.uniform(0.2, 5.8) * inch, r.uniform(2.6, 8.8) * inch, r.uniform(3, 9), colors.Color(1, 1, 1, alpha=r.uniform(0.10, 0.28)))
    for _ in range(38):   # small gold stars
        x, y = r.uniform(0.15, 5.85) * inch, r.uniform(3.5, 8.9) * inch
        if 4.6 * inch < y < 8.4 * inch and 0.5 * inch < x < 5.5 * inch and r.random() < 0.7: continue
        star(c, x, y, r.uniform(1.6, 3.6), fill=colors.Color(1, 0.82, 0.48, alpha=r.uniform(0.5, 0.95)))
    # a little constellation, top right
    pts = [(4.75, 8.72), (5.12, 8.52), (5.5, 8.66), (5.28, 8.25)]
    c.setStrokeColor(colors.Color(1, 0.82, 0.48, alpha=0.45)); c.setLineWidth(0.6)
    for a, b in zip(pts, pts[1:]): c.line(a[0] * inch, a[1] * inch, b[0] * inch, b[1] * inch)
    for x, y in pts: star(c, x * inch, y * inch, 4.2, fill=GOLD)
    # crescent moon, top left
    c.setFillColor(colors.Color(1, 0.9, 0.65)); c.circle(0.75 * inch, 8.45 * inch, 0.24 * inch, stroke=0, fill=1)
    c.setFillColor(NAVY); c.circle(0.86 * inch, 8.52 * inch, 0.22 * inch, stroke=0, fill=1)
    # mountains
    c.setFillColor(SLATE); p = c.beginPath(); p.moveTo(-0.2 * inch, 2.0 * inch)
    for x, y in [(0.9, 3.1), (1.8, 2.5), (3.0, 4.05), (4.2, 2.6), (5.2, 3.3), (6.3, 2.4), (6.3, -0.2), (-0.2, -0.2)]: p.lineTo(x * inch, y * inch)
    p.close(); c.drawPath(p, stroke=0, fill=1)
    c.setFillColor(colors.white)
    for (px, py, s) in [(0.9, 3.1, 0.24), (3.0, 4.05, 0.34), (5.2, 3.3, 0.24)]:
        p = c.beginPath(); p.moveTo(px * inch, py * inch); p.lineTo((px - s) * inch, (py - s * 0.8) * inch); p.lineTo((px + s) * inch, (py - s * 0.8) * inch); p.close(); c.drawPath(p, stroke=0, fill=1)
    # the lodge with its observatory dome, on a shoulder of the big peak
    lx, ly = 3.5 * inch, 3.02 * inch
    c.setFillColor(DEEP); c.rect(lx, ly, 0.5 * inch, 0.3 * inch, stroke=0, fill=1)
    p = c.beginPath(); p.moveTo(lx - 0.05 * inch, ly + 0.3 * inch); p.lineTo(lx + 0.2 * inch, ly + 0.46 * inch); p.lineTo(lx + 0.45 * inch, ly + 0.3 * inch); p.close(); c.drawPath(p, stroke=0, fill=1)
    c.rect(lx + 0.36 * inch, ly + 0.3 * inch, 0.16 * inch, 0.14 * inch, stroke=0, fill=1)
    c.wedge(lx + 0.33 * inch, ly + 0.36 * inch, lx + 0.55 * inch, ly + 0.58 * inch, 0, 180, stroke=0, fill=1)
    c.setStrokeColor(DEEP); c.setLineWidth(2.2); c.line(lx + 0.44 * inch, ly + 0.5 * inch, lx + 0.6 * inch, ly + 0.62 * inch)
    c.setFillColor(GOLD)
    for i in range(4):
        for j in range(2): c.rect(lx + (0.06 + i * 0.105) * inch, ly + (0.06 + j * 0.11) * inch, 0.05 * inch, 0.05 * inch, stroke=0, fill=1)
    c.setFillColor(GOLD); c.rect(lx + 0.42 * inch, ly + 0.36 * inch, 0.04 * inch, 0.04 * inch, stroke=0, fill=1)
    # zig-zag lantern trail up the mountain
    c.setStrokeColor(colors.Color(1, 1, 1, alpha=0.5)); c.setLineWidth(1.2); c.setDash(2, 3)
    p = c.beginPath(); p.moveTo(2.2 * inch, 1.5 * inch); p.lineTo(3.6 * inch, 1.95 * inch); p.lineTo(2.9 * inch, 2.35 * inch); p.lineTo(3.9 * inch, 2.7 * inch); p.lineTo(3.7 * inch, 3.02 * inch)
    c.drawPath(p, stroke=1, fill=0); c.setDash()
    for x, y in [(3.6, 1.95), (2.9, 2.35), (3.9, 2.7)]: c.setFillColor(GOLD); c.circle(x * inch, y * inch, 1.6, stroke=0, fill=1)
    # snowy foreground with the village
    c.setFillColor(SNOW); p = c.beginPath(); p.moveTo(-0.2 * inch, 1.5 * inch)
    p.curveTo(1.5 * inch, 1.72 * inch, 3.8 * inch, 1.35 * inch, 6.3 * inch, 1.6 * inch); p.lineTo(6.3 * inch, -0.2 * inch); p.lineTo(-0.2 * inch, -0.2 * inch); p.close()
    c.drawPath(p, stroke=0, fill=1)
    for x, h in [(0.35, 0.5), (0.62, 0.36), (5.25, 0.46), (5.55, 0.62), (5.8, 0.4)]: pine(c, x * inch, 1.42 * inch, h * inch)
    for x, w, h in [(1.0, 0.5, 0.26), (1.65, 0.38, 0.32), (4.35, 0.46, 0.24), (3.75, 0.36, 0.3)]: cottage(c, x * inch, 1.42 * inch, w * inch, h * inch)
    W = TW * inch
    c.setFillColor(colors.white); c.setFont("PlayfairSC", 11.5); c.drawCentredString(W / 2, 8.1 * inch, "A Winter Night-Sky Puzzle Book")
    c.setStrokeColor(GOLD); c.setLineWidth(0.8); c.line(2.2 * inch, 7.95 * inch, 3.8 * inch, 7.95 * inch)
    c.setFont("PlayfairSC-B", 50); c.drawCentredString(W / 2, 7.08 * inch, "Stars over"); c.drawCentredString(W / 2, 6.35 * inch, "Frostwood")
    c.setFont("Crimson-I", 17); c.setFillColor(PALE)
    c.drawCentredString(W / 2, 5.68 * inch, f"{NP} Star Battle Logic Puzzles")
    c.setFont("Crimson-I", 14); c.drawCentredString(W / 2, 5.38 * inch, "from the village to the summit")
    c.setFont("PlayfairSC", 10.5); c.setFillColor(GOLD)
    c.drawCentredString(W / 2, 4.9 * inch, "Easy to Expert · One & Two Stars · Solutions Included")
    c.setFillColor(NAVY); c.setFont("PlayfairSC", 11); c.drawCentredString(W / 2, 0.72 * inch, "A Frostwood Puzzle Book")
    c.setFont("Crimson-I", 13); c.setFillColor(colors.HexColor("#3a4d66")); c.drawCentredString(W / 2, 0.44 * inch, "Blake La Pierre")
    c.restoreState()

cnt = {b: len(D[b]) for b in ("Easy", "Medium", "Hard", "Expert")}
BLURB = [
 "<b>On clear winter nights, the Frostwood Star Club climbs from the village green to the little observatory on the roof of the lodge. This year the snow clouds have smudged every chart.</b>",
 f"{NP} patches of sky need their stars put back. Each one is a Star Battle puzzle: place stars so that every row, every column and every outlined region holds the same number of them, one or two, and no two stars ever touch, not even at the corners.",
 "Every puzzle has exactly one solution, checked by computer, and every one can be solved by logic alone, with no guessing.",
]
FEATS = [f"{NP} Star Battle puzzles in four parts, from 6×6 to 10×10",
         f"{cnt['Easy']} Easy and {cnt['Medium']} Medium one-star puzzles, {cnt['Hard']} Hard and {cnt['Expert']} Expert two-star puzzles",
         "Large, clear grids with room for pencil marks",
         "How-to-play guide with a fully worked example",
         "Complete solutions at the back",
         "Book three of the cozy Frostwood Puzzle Books"]

def back(c):
    r = random.Random(5)
    for _ in range(18):
        snowflake(c, (X_BACK + r.uniform(0.2, 5.8)) * inch, (BLEED + r.uniform(2.0, 8.8)) * inch, r.uniform(3, 8), colors.Color(1, 1, 1, alpha=r.uniform(0.1, 0.22)))
    for _ in range(16):
        star(c, (X_BACK + r.uniform(0.2, 5.8)) * inch, (BLEED + r.uniform(8.45, 8.9)) * inch, r.uniform(1.5, 3), fill=colors.Color(1, 0.82, 0.48, alpha=0.6))
    x0 = (X_BACK + 0.55) * inch; w = (TW - 1.1) * inch
    c.setFillColor(colors.white); c.setFont("PlayfairSC-B", 18)
    c.drawCentredString((X_BACK + TW / 2) * inch, (BLEED + 8.1) * inch, "Clear Skies over Frostwood")
    c.setStrokeColor(GOLD); c.setLineWidth(0.8); c.line((X_BACK + 2.2) * inch, (BLEED + 7.9) * inch, (X_BACK + 3.8) * inch, (BLEED + 7.9) * inch)
    st = ParagraphStyle("bl", fontName="Crimson", fontSize=12, leading=16, textColor=colors.white, alignment=TA_JUSTIFY, spaceAfter=7)
    fl = [Paragraph(t, st) for t in BLURB]
    li = ParagraphStyle("li", parent=st, alignment=TA_LEFT, fontSize=11.3, leading=14.5, leftIndent=14, firstLineIndent=-12, spaceAfter=3, textColor=PALE)
    fl += [Paragraph("<font name='DejaVu' color='#ffd27a' size='8'>❄</font>&nbsp;&nbsp;" + t, li) for t in FEATS]
    f = Frame(x0, (BLEED + 2.05) * inch, w, 5.7 * inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
    f.addFromList(fl, c); assert not fl, "back cover text overflow"
    p = D["Easy"][0]; cs = 0.22 * inch; n = p["n"]
    cx, cy = (X_BACK + 0.55) * inch, (BLEED + 0.4) * inch
    c.setFillColor(colors.white); c.roundRect(cx, cy, 1.75 * inch, 1.72 * inch, 4, stroke=0, fill=1)
    draw_grid(c, cx + (1.75 * inch - n * cs) / 2, cy + (1.72 * inch - n * cs) / 2, cs, p)
    tx = (X_BACK + 2.45) * inch
    LINES = ["One star in every row,", "every column and", "every region.", "Stars never touch,", "not even diagonally."]
    c.setFillColor(PALE); c.setFont("PlayfairSC", 9.5); c.drawString(tx, (BLEED + 1.75) * inch, "Puzzle No. 1")
    c.setFont("Crimson-I", 10)
    for i, t in enumerate(LINES): c.drawString(tx, (BLEED + 1.53 - i * 0.18) * inch, t)
    c.setFont("PlayfairSC", 8.5); c.setFillColor(GOLD); c.drawString(tx, (BLEED + 0.45) * inch, "Puzzles & Games")
    c.setFont("Crimson-I", 9); c.setFillColor(PALE); c.drawString(tx, (BLEED + 0.28) * inch, "Ages 12 and up")
    assert tx + max(c.stringWidth(t, "Crimson-I", 10) for t in LINES) < (X_BACK + TW - 0.25 - 2.0) * inch - 6

def main(out="../cover.pdf", guides=False):
    c = canvas.Canvas(out, pagesize=(CW * inch, CH * inch))
    c.setTitle("Stars over Frostwood — KDP cover"); c.setAuthor("Blake La Pierre")
    c.setFillColor(NAVY); c.rect(0, 0, CW * inch, CH * inch, stroke=0, fill=1)
    back(c)
    c.setFillColor(colors.HexColor("#17304f")); c.rect(X_SPINE * inch, 0, SPINE * inch, CH * inch, stroke=0, fill=1)
    assert PAGES >= 79 and SPINE >= 0.25
    c.saveState(); c.translate((X_SPINE + SPINE / 2) * inch, (BLEED + TH / 2) * inch); c.rotate(-90)
    c.setFillColor(colors.white); c.setFont("PlayfairSC-B", 13); c.drawCentredString(-0.9 * inch, -4.5, "Stars over Frostwood")
    c.setFillColor(GOLD); c.setFont("Crimson-I", 9.5); c.drawCentredString(1.15 * inch, -3.3, f"{NP} Star Battle Puzzles")
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
