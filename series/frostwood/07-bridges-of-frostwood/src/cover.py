"""KDP full-wrap paperback cover: 6x9 trim, 0.125in bleed, white paper B&W spine = pages x 0.002252in.
Same palette and layout as the other Frostwood Puzzle Book covers."""
import json, math, random, sys
sys.path.insert(0, ".")
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
import build
from build import snowflake, draw_hashi, grid_size, D, NP

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
    # snowy foreground with the frozen lodge pond
    c.setFillColor(SNOW); p = c.beginPath(); p.moveTo(-0.2 * inch, 2.05 * inch)
    p.curveTo(1.5 * inch, 2.2 * inch, 3.8 * inch, 1.9 * inch, 6.3 * inch, 2.1 * inch); p.lineTo(6.3 * inch, -0.2 * inch); p.lineTo(-0.2 * inch, -0.2 * inch); p.close()
    c.drawPath(p, stroke=0, fill=1)
    for x, h in [(0.35, 0.62), (0.72, 0.44), (5.25, 0.56), (5.62, 0.72)]:
        cover_pine(c, x * inch, 1.9 * inch, h * inch)
    cottage(c, 4.55 * inch, 1.94 * inch, 0.42 * inch, 0.24 * inch)
    # the pond (pale ice) with glints
    c.setFillColor(PALE); c.ellipse(0.25 * inch, 0.88 * inch, 5.75 * inch, 1.98 * inch, stroke=0, fill=1)
    c.setStrokeColor(colors.white); c.setLineWidth(0.8)
    for gx, gy, L in [(0.9, 1.25, 0.5), (3.9, 1.7, 0.6), (4.6, 1.15, 0.4), (1.6, 1.75, 0.35)]:
        c.line(gx * inch, gy * inch, (gx + L) * inch, gy * inch)
    # gold islands joined by bridges, a little Hashi map on the ice
    I = [(1.05, 1.43, "2"), (2.05, 1.43, "4"), (2.05, 1.84, "1"), (3.45, 1.43, "3"), (3.45, 1.05, "1"), (4.85, 1.43, "1")]
    def br(a, b, k):
        (x1, y1, _), (x2, y2, _) = I[a], I[b]
        c.setStrokeColor(GOLD); c.setLineWidth(1.6)
        offs = (0,) if k == 1 else (-0.035, 0.035)
        for o in offs:
            if y1 == y2: c.line(x1 * inch, (y1 + o) * inch, x2 * inch, (y2 + o) * inch)
            else: c.line((x1 + o) * inch, y1 * inch, (x2 + o) * inch, y2 * inch)
    br(0, 1, 2); br(1, 2, 1); br(1, 3, 1); br(3, 4, 1); br(3, 5, 1)
    for x, y, t in I:
        c.setFillColor(NAVY); c.setStrokeColor(GOLD); c.setLineWidth(1.4); c.circle(x * inch, y * inch, 0.115 * inch, stroke=1, fill=1)
        c.setFillColor(GOLD); c.setFont("Plex-M", 10); c.drawCentredString(x * inch, y * inch - 3.6, t)
    # arched footbridge in the near corner of the pond (deep silhouette, gold lanterns)
    bx0, bx1, by = 3.95, 4.55, 0.98
    c.setStrokeColor(DEEP); c.setLineWidth(2.4); p = c.beginPath(); p.moveTo(bx0 * inch, by * inch)
    p.curveTo((bx0 + 0.2) * inch, (by + 0.22) * inch, (bx1 - 0.2) * inch, (by + 0.22) * inch, bx1 * inch, by * inch); c.drawPath(p, stroke=1, fill=0)
    c.setLineWidth(1.0); p = c.beginPath(); p.moveTo(bx0 * inch, (by + 0.12) * inch)
    p.curveTo((bx0 + 0.2) * inch, (by + 0.34) * inch, (bx1 - 0.2) * inch, (by + 0.34) * inch, bx1 * inch, (by + 0.12) * inch); c.drawPath(p, stroke=1, fill=0)
    for t in (0.0, 0.25, 0.5, 0.75, 1.0):
        x = bx0 + (bx1 - bx0) * t; y = by + 0.165 * 4 * t * (1 - t) * 1.0
        c.line(x * inch, y * inch, x * inch, (y + 0.12) * inch)
    for x in (bx0, bx1):
        c.setFillColor(GOLD); c.circle(x * inch, (by + 0.17) * inch, 0.03 * inch, stroke=0, fill=1)
    W = TW * inch
    c.setFillColor(colors.white); c.setFont("PlayfairSC", 11.5); c.drawCentredString(W / 2, 8.1 * inch, "A Frozen-Pond Puzzle Book")
    c.setStrokeColor(GOLD); c.setLineWidth(0.8); c.line(2.2 * inch, 7.95 * inch, 3.8 * inch, 7.95 * inch)
    c.setFont("PlayfairSC-B", 48); c.drawCentredString(W / 2, 7.08 * inch, "Bridges of"); c.drawCentredString(W / 2, 6.35 * inch, "Frostwood")
    c.setFont("Crimson-I", 17); c.setFillColor(PALE)
    c.drawCentredString(W / 2, 5.68 * inch, f"{NP} Hashi Bridges Logic Puzzles")
    c.setFont("Crimson-I", 14); c.drawCentredString(W / 2, 5.38 * inch, "from the lodge pond to the lake of islands")
    c.setFont("PlayfairSC", 10.5); c.setFillColor(GOLD)
    c.drawCentredString(W / 2, 4.9 * inch, "Easy to Expert · Big, Clear Maps · Solutions Included")
    c.setFillColor(NAVY); c.setFont("PlayfairSC", 11); c.drawCentredString(W / 2, 0.72 * inch, "A Frostwood Puzzle Book")
    c.setFont("Crimson-I", 13); c.setFillColor(colors.HexColor("#3a4d66")); c.drawCentredString(W / 2, 0.44 * inch, "Blake La Pierre")
    c.restoreState()

cnt = {b: len(D[b]) for b in ("Easy", "Medium", "Hard", "Expert")}
BLURB = [
 "<b>Every winter the ponds and lakes around Frostwood freeze hard, and the village lays little footbridges from island to island. This year the plans have blown away in the snow.</b>",
 f"{NP} maps are left, from the lodge pond to the great lake of islands. Each one is a Hashi puzzle (also called Bridges or Hashiwokakero): join the islands with straight bridges so every island has as many as its number, no bridges cross, and all the islands link up.",
 "Every puzzle has exactly one solution, checked by computer, and every one can be solved by logic alone, with no guessing.",
]
FEATS = [f"{NP} Hashi bridges puzzles in four parts, from 7×7 to 13×15",
         f"{cnt['Easy']} Easy, {cnt['Medium']} Medium, {cnt['Hard']} Hard and {cnt['Expert']} Expert",
         "Large, clear maps with room to draw every bridge",
         "How-to-play guide with a fully worked example",
         "Complete solutions at the back",
         "Book seven of the cozy Frostwood Puzzle Books"]

def back(c):
    r = random.Random(5)
    for _ in range(18):
        snowflake(c, (X_BACK + r.uniform(0.2, 5.8)) * inch, (BLEED + r.uniform(2.0, 8.8)) * inch, r.uniform(3, 8), colors.Color(1, 1, 1, alpha=r.uniform(0.1, 0.22)))
    x0 = (X_BACK + 0.55) * inch; w = (TW - 1.1) * inch
    c.setFillColor(colors.white); c.setFont("PlayfairSC-B", 18)
    c.drawCentredString((X_BACK + TW / 2) * inch, (BLEED + 8.1) * inch, "Bridge the Frozen Ponds")
    c.setStrokeColor(GOLD); c.setLineWidth(0.8); c.line((X_BACK + 2.2) * inch, (BLEED + 7.9) * inch, (X_BACK + 3.8) * inch, (BLEED + 7.9) * inch)
    st = ParagraphStyle("bl", fontName="Crimson", fontSize=12, leading=16, textColor=colors.white, alignment=TA_JUSTIFY, spaceAfter=7)
    fl = [Paragraph(t, st) for t in BLURB]
    li = ParagraphStyle("li", parent=st, alignment=TA_LEFT, fontSize=11.3, leading=14.5, leftIndent=14, firstLineIndent=-12, spaceAfter=3, textColor=PALE)
    fl += [Paragraph("<font name='DejaVu' color='#ffd27a' size='8'>❄</font>&nbsp;&nbsp;" + t, li) for t in FEATS]
    f = Frame(x0, (BLEED + 2.05) * inch, w, 5.7 * inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
    f.addFromList(fl, c); assert not fl, "back cover text overflow"
    p = D["Easy"][1]; cs = 0.235 * inch; gw, gh = grid_size(p, cs)
    cx, cy = (X_BACK + 0.55) * inch, (BLEED + 0.35) * inch
    c.setFillColor(colors.white); c.roundRect(cx, cy, 1.85 * inch, 1.78 * inch, 4, stroke=0, fill=1)
    draw_hashi(c, cx + (1.85 * inch - gw) / 2, cy + (1.78 * inch + gh) / 2, cs, p)
    tx = (X_BACK + 2.55) * inch
    LINES = ["Each number counts", "its bridges.", "One or two per pair,", "never crossing.", "Join every island."]
    c.setFillColor(PALE); c.setFont("PlayfairSC", 9.5); c.drawString(tx, (BLEED + 1.75) * inch, f"Puzzle No. {p['num']}")
    c.setFont("Crimson-I", 10)
    bx = X_BACK + TW - 0.25 - 2.0
    for i, t in enumerate(LINES):
        assert tx + pdfmetrics.stringWidth(t, "Crimson-I", 10) < (bx - 0.08) * inch, t   # stay clear of the barcode box
        c.drawString(tx, (BLEED + 1.53 - i * 0.18) * inch, t)
    c.setFont("PlayfairSC", 8.5); c.setFillColor(GOLD); c.drawString(tx, (BLEED + 0.45) * inch, "Puzzles & Games")
    c.setFont("Crimson-I", 9); c.setFillColor(PALE); c.drawString(tx, (BLEED + 0.28) * inch, "Ages 12 and up")

def main(out="../frostwood-07-bridges-of-frostwood-cover.pdf", guides=False):
    c = canvas.Canvas(out, pagesize=(CW * inch, CH * inch))
    c.setTitle("Bridges of Frostwood — KDP cover"); c.setAuthor("Blake La Pierre")
    c.setFillColor(NAVY); c.rect(0, 0, CW * inch, CH * inch, stroke=0, fill=1)
    back(c)
    c.setFillColor(colors.HexColor("#17304f")); c.rect(X_SPINE * inch, 0, SPINE * inch, CH * inch, stroke=0, fill=1)
    assert PAGES >= 79 and SPINE >= 0.25
    c.saveState(); c.translate((X_SPINE + SPINE / 2) * inch, (BLEED + TH / 2) * inch); c.rotate(-90)
    c.setFillColor(colors.white); c.setFont("PlayfairSC-B", 13); c.drawCentredString(-0.9 * inch, -4.5, "Bridges of Frostwood")
    c.setFillColor(GOLD); c.setFont("Crimson-I", 9.5); c.drawCentredString(1.35 * inch, -3.3, f"{NP} Hashi Puzzles")
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
    m = main(); main("../tmp/frostwood-07-bridges-of-frostwood-cover-guides.pdf", guides=True)
    print(m); json.dump(m, open("../cover-info.json", "w"), indent=1)
