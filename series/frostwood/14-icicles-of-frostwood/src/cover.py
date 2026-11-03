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
from build import snowflake, draw_grid, D, NP, EX

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
        fx, fy, fs, fa = r.uniform(0.2, 5.8), r.uniform(2.6, 8.8), r.uniform(3, 10), r.uniform(0.12, 0.32)
        if 0.3 < fx < 5.7 and (4.75 < fy < 5.25 or 5.5 < fy < 7.95):
            continue  # keep the title, subtitle and feature line clear of flakes
        snowflake(c, fx * inch, fy * inch, fs, colors.Color(1, 1, 1, alpha=fa))
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
    # a few icicles under the cottage and lodge eaves
    def icy(x0, x1, y, n, lmax):
        rr = random.Random(int(x0 * 100)); c.setFillColor(colors.white)
        for k in range(n):
            x = x0 + (x1 - x0) * (k + 0.5) / n; L = lmax * rr.uniform(0.45, 1.0); ww = (x1 - x0) / n * 0.38
            p = c.beginPath(); p.moveTo(x - ww, y); p.lineTo(x + ww, y); p.lineTo(x, y - L); p.close(); c.drawPath(p, stroke=0, fill=1)
    icy(4.51 * inch, 5.01 * inch, 2.18 * inch, 6, 0.07 * inch)
    icy(3.5 * inch, 4.1 * inch, 3.3 * inch, 7, 0.06 * inch)
    # a frosted eave along the top edge, hung with long icicles
    c.setFillColor(DEEP); c.rect(-0.2 * inch, 8.93 * inch, 6.5 * inch, 0.4 * inch, stroke=0, fill=1)
    c.setFillColor(SNOW); p = c.beginPath(); p.moveTo(-0.2 * inch, 8.95 * inch)
    for k in range(14): p.curveTo((k * 0.47 - 0.05) * inch, 8.99 * inch, (k * 0.47 + 0.15) * inch, 8.88 * inch, ((k + 1) * 0.47 - 0.2) * inch, 8.95 * inch)
    p.lineTo(6.5 * inch, 9.1 * inch); p.lineTo(-0.2 * inch, 9.1 * inch); p.close(); c.drawPath(p, stroke=0, fill=1)
    rr = random.Random(41)
    for k in range(25):
        x = (0.12 + k * 0.24) * inch; L = rr.uniform(0.12, 0.42) * inch; ww = 0.055 * inch
        c.setFillColor(colors.Color(0.95, 0.97, 1.0)); p = c.beginPath(); p.moveTo(x - ww, 8.92 * inch); p.lineTo(x + ww, 8.92 * inch); p.lineTo(x, 8.92 * inch - L); p.close(); c.drawPath(p, stroke=0, fill=1)
        c.setFillColor(colors.Color(0.72, 0.8, 0.9)); p = c.beginPath(); p.moveTo(x + ww * 0.15, 8.92 * inch); p.lineTo(x + ww, 8.92 * inch); p.lineTo(x, 8.92 * inch - L); p.close(); c.drawPath(p, stroke=0, fill=1)
        if k % 3 == 0: c.setFillColor(GOLD); c.circle(x, 8.92 * inch - L - 0.03 * inch, 0.012 * inch, stroke=0, fill=1)
    # a gold-edged Futoshiki grid lying in the snow (the worked example, solved)
    n = EX["n"]; b = 0.22 * inch; g = b * 0.45; st = b + g; gw = n * b + (n - 1) * g
    gx = 0.62 * inch; gy = 1.72 * inch
    c.setFillColor(colors.white); c.roundRect(gx - 6, gy - gw - 6, gw + 12, gw + 12, 3, stroke=0, fill=1)
    c.setStrokeColor(GOLD); c.setLineWidth(1.6); c.roundRect(gx - 6, gy - gw - 6, gw + 12, gw + 12, 3, stroke=1, fill=0)
    c.setStrokeColor(NAVY); c.setLineWidth(0.8)
    for r in range(n):
        for cc in range(n):
            c.rect(gx + cc * st, gy - r * st - b, b, b, stroke=1, fill=0)
            c.setFillColor(NAVY); c.setFont("Plex-M", 9.5); c.drawCentredString(gx + cc * st + b / 2, gy - r * st - b / 2 - 3.3, str(EX["sol"][r][cc]))
    for r1, c1, r2, c2 in EX["ineq"]:
        if r1 == r2: build.chevron(c, gx + min(c1, c2) * st + b + g / 2, gy - r1 * st - b / 2, g * 0.95, "h", c1 < c2, NAVY, 0.9)
        else: build.chevron(c, gx + c1 * st + b / 2, gy - min(r1, r2) * st - b - g / 2, g * 0.95, "v", r1 < r2, NAVY, 0.9)
    # lantern posts along the path
    for lx, ly in ((2.3, 1.2), (4.25, 1.35), (5.3, 1.05)):
        c.setStrokeColor(DEEP); c.setLineWidth(1.6); c.line(lx * inch, ly * inch, lx * inch, (ly + 0.42) * inch)
        c.setFillColor(GOLD); c.circle(lx * inch, (ly + 0.45) * inch, 0.035 * inch, stroke=0, fill=1)
    W = TW * inch
    c.setFillColor(colors.white); c.setFont("PlayfairSC", 11.5); c.drawCentredString(W / 2, 8.1 * inch, "A Frozen-Eaves Puzzle Book")
    c.setStrokeColor(GOLD); c.setLineWidth(0.8); c.line(2.2 * inch, 7.95 * inch, 3.8 * inch, 7.95 * inch)
    c.setFont("PlayfairSC-B", 48); c.drawCentredString(W / 2, 7.08 * inch, "The Icicles"); c.drawCentredString(W / 2, 6.35 * inch, "of Frostwood")
    c.setFont("Crimson-I", 17); c.setFillColor(PALE)
    c.drawCentredString(W / 2, 5.68 * inch, f"{NP} Futoshiki Logic Puzzles")
    c.setFont("Crimson-I", 14); c.drawCentredString(W / 2, 5.38 * inch, "from the lodge eaves to the high meadows")
    c.setFont("PlayfairSC", 10.5); c.setFillColor(GOLD)
    c.drawCentredString(W / 2, 4.9 * inch, "Easy to Expert · Big, Clear Grids · Solutions Included")
    c.setFillColor(NAVY); c.setFont("PlayfairSC", 11); c.drawCentredString(W / 2, 0.72 * inch, "A Frostwood Puzzle Book")
    c.setFont("Crimson-I", 13); c.setFillColor(colors.HexColor("#3a4d66")); c.drawCentredString(W / 2, 0.44 * inch, "Blake La Pierre")
    c.restoreState()

cnt = {b: len(D[b]) for b in ("Easy", "Medium", "Hard", "Expert")}
BLURB = [
 "<b>On the coldest nights of the winter, icicles hang from every eave in Frostwood, and the village children sort them by length, one of each in every row and column.</b>",
 f"{NP} of their grids are left, from the lodge eaves to the high meadows. Each one is a Futoshiki puzzle: fill the grid so no number repeats in any row or column, and every little sign between two squares points to the smaller one.",
 "Every puzzle has exactly one solution, checked by computer, and every one can be solved by logic alone, with no guessing.",
]
FEATS = [f"{NP} Futoshiki puzzles in four parts, from 5×5 to 8×8",
         f"{cnt['Easy']} Easy, {cnt['Medium']} Medium, {cnt['Hard']} Hard and {cnt['Expert']} Expert",
         "Large, clear grids with room for pencil notes",
         "How-to-play guide with a fully worked example",
         "Complete solutions at the back",
         "Book fourteen of the cozy Frostwood Puzzle Books"]

def back(c):
    r = random.Random(5)
    for _ in range(18):
        snowflake(c, (X_BACK + r.uniform(0.2, 5.8)) * inch, (BLEED + r.uniform(2.0, 8.8)) * inch, r.uniform(3, 8), colors.Color(1, 1, 1, alpha=r.uniform(0.1, 0.22)))
    x0 = (X_BACK + 0.55) * inch; w = (TW - 1.1) * inch
    c.setFillColor(colors.white); c.setFont("PlayfairSC-B", 18)
    c.drawCentredString((X_BACK + TW / 2) * inch, (BLEED + 8.1) * inch, "Sort the Icicles")
    c.setStrokeColor(GOLD); c.setLineWidth(0.8); c.line((X_BACK + 2.2) * inch, (BLEED + 7.9) * inch, (X_BACK + 3.8) * inch, (BLEED + 7.9) * inch)
    st = ParagraphStyle("bl", fontName="Crimson", fontSize=12, leading=16, textColor=colors.white, alignment=TA_JUSTIFY, spaceAfter=7)
    fl = [Paragraph(t, st) for t in BLURB]
    li = ParagraphStyle("li", parent=st, alignment=TA_LEFT, fontSize=11.3, leading=14.5, leftIndent=14, firstLineIndent=-12, spaceAfter=3, textColor=PALE)
    fl += [Paragraph("<font name='DejaVu' color='#ffd27a' size='8'>❄</font>&nbsp;&nbsp;" + t, li) for t in FEATS]
    f = Frame(x0, (BLEED + 2.05) * inch, w, 5.7 * inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
    f.addFromList(fl, c); assert not fl, "back cover text overflow"
    p = D["Easy"][1]; cs = 0.24 * inch; gw = gh = build.gsize(p["n"], cs)
    cx, cy = (X_BACK + 0.55) * inch, (BLEED + 0.35) * inch
    c.setFillColor(colors.white); c.roundRect(cx, cy, 1.85 * inch, 1.78 * inch, 4, stroke=0, fill=1)
    draw_grid(c, cx + (1.85 * inch - gw) / 2, cy + (1.78 * inch + gh) / 2, cs, p)
    tx = (X_BACK + 2.55) * inch
    LINES = ["Write 1 to 5 once", "in every row", "and every column.", "Each sign points", "to the smaller one."]
    c.setFillColor(PALE); c.setFont("PlayfairSC", 9.5); c.drawString(tx, (BLEED + 1.75) * inch, f"Puzzle No. {p['num']}")
    c.setFont("Crimson-I", 10)
    bx = X_BACK + TW - 0.25 - 2.0
    for i, t in enumerate(LINES):
        assert tx + pdfmetrics.stringWidth(t, "Crimson-I", 10) < (bx - 0.08) * inch, t   # stay clear of the barcode box
        c.drawString(tx, (BLEED + 1.53 - i * 0.18) * inch, t)
    c.setFont("PlayfairSC", 8.5); c.setFillColor(GOLD); c.drawString(tx, (BLEED + 0.45) * inch, "Puzzles & Games")
    c.setFont("Crimson-I", 9); c.setFillColor(PALE); c.drawString(tx, (BLEED + 0.28) * inch, "Ages 12 and up")

def main(out="../frostwood-14-icicles-of-frostwood-cover.pdf", guides=False):
    c = canvas.Canvas(out, pagesize=(CW * inch, CH * inch))
    c.setTitle("The Icicles of Frostwood — KDP cover"); c.setAuthor("Blake La Pierre")
    c.setFillColor(NAVY); c.rect(0, 0, CW * inch, CH * inch, stroke=0, fill=1)
    back(c)
    c.setFillColor(colors.HexColor("#17304f")); c.rect(X_SPINE * inch, 0, SPINE * inch, CH * inch, stroke=0, fill=1)
    assert PAGES >= 79 and SPINE >= 0.25
    c.saveState(); c.translate((X_SPINE + SPINE / 2) * inch, (BLEED + TH / 2) * inch); c.rotate(-90)
    c.setFillColor(colors.white); c.setFont("PlayfairSC-B", 13); c.drawCentredString(-0.8 * inch, -4.5, "The Icicles of Frostwood")
    c.setFillColor(GOLD); c.setFont("Crimson-I", 9.5); c.drawCentredString(1.55 * inch, -3.3, f"{NP} Futoshiki Puzzles")
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
    m = main(); main("../tmp/frostwood-14-icicles-of-frostwood-cover-guides.pdf", guides=True)
    print(m); json.dump(m, open("../cover-info.json", "w"), indent=1)
