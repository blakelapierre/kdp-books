"""KDP full-wrap paperback cover: 6x9 trim, 0.125in bleed, white paper B&W spine = pages x 0.002252in."""
import json, math, random, sys
sys.path.insert(0, ".")
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from draw import snowflake   # also registers the house fonts

info = json.load(open("../build-info.json")); PAGES = info["pages"]
BLEED = 0.125; TW, TH = 6.0, 9.0
SPINE = PAGES * 0.002252
CW = BLEED + TW + SPINE + TW + BLEED; CH = BLEED + TH + BLEED
NAVY = colors.HexColor("#1f3a5f"); GOLD = colors.HexColor("#ffd27a"); PALE = colors.HexColor("#dbe6f1"); SNOW = colors.HexColor("#f4f7fb")
DEEP = colors.HexColor("#15293f"); SLATE = colors.HexColor("#2c4d74"); WOOD = colors.HexColor("#122338"); TRIM = colors.HexColor("#c9a55a")
X_BACK = BLEED; X_SPINE = BLEED + TW; X_FRONT = BLEED + TW + SPINE

def star5(c, x, y, r, col):
    p = c.beginPath()
    for k in range(10):
        a = math.pi / 2 + k * math.pi / 5; rr = r if k % 2 == 0 else r * 0.42
        (p.moveTo if k == 0 else p.lineTo)(x + rr * math.cos(a), y + rr * math.sin(a))
    p.close(); c.setFillColor(col); c.drawPath(p, stroke=0, fill=1)

def pine(c, x, y, h, col):
    c.setFillColor(col)
    for k in range(3):
        w = h * (0.42 - k * 0.09); b = y + h * (0.12 + k * 0.24)
        p = c.beginPath(); p.moveTo(x - w, b); p.lineTo(x + w, b); p.lineTo(x, b + h * 0.42); p.close(); c.drawPath(p, stroke=0, fill=1)
    c.rect(x - h * 0.04, y, h * 0.08, h * 0.13, stroke=0, fill=1)

def clock(c, cx):
    """The Great Advent Clock: a tall case with 24 numbered doors and a moon-dial face at a quarter to midnight."""
    I = inch; cw, x0 = 2.3 * I, cx - 1.15 * I; base, top = 0.95 * I, 4.12 * I
    # glow
    for k in range(6, 0, -1):
        c.setFillColor(colors.Color(1, 0.82, 0.48, alpha=0.035)); c.circle(cx, 4.75 * I, (0.9 + k * 0.22) * I, stroke=0, fill=1)
    # plinth and case
    c.setFillColor(WOOD); c.rect(x0 - 0.12 * I, base - 0.2 * I, cw + 0.24 * I, 0.22 * I, stroke=0, fill=1)
    c.rect(x0, base, cw, top - base, stroke=0, fill=1)
    c.setStrokeColor(TRIM); c.setLineWidth(1.2); c.rect(x0 + 0.07 * I, base + 0.07 * I, cw - 0.14 * I, top - base - 0.14 * I, stroke=1, fill=0)
    # hood with face
    hb = top; hw = 1.7 * I
    c.setFillColor(WOOD); c.rect(cx - hw / 2, hb, hw, 1.05 * I, stroke=0, fill=1)
    p = c.beginPath(); p.moveTo(cx - hw / 2 - 0.1 * I, hb + 1.05 * I); p.lineTo(cx + hw / 2 + 0.1 * I, hb + 1.05 * I)
    p.lineTo(cx, hb + 1.42 * I); p.close(); c.drawPath(p, stroke=0, fill=1)
    fy = hb + 0.55 * I; fr = 0.46 * I
    c.setFillColor(SNOW); c.circle(cx, fy, fr, stroke=0, fill=1)
    c.setStrokeColor(TRIM); c.setLineWidth(2); c.circle(cx, fy, fr, stroke=1, fill=0)
    c.setStrokeColor(DEEP); c.setLineWidth(1)
    for k in range(12):
        a = math.pi / 2 - k * math.pi / 6; r1, r2 = fr * (0.8 if k % 3 else 0.72), fr * 0.9
        c.line(cx + r1 * math.cos(a), fy + r1 * math.sin(a), cx + r2 * math.cos(a), fy + r2 * math.sin(a))
    # a quarter to midnight
    for ang, ln, lw in [(math.pi / 2 + math.radians(7.5), 0.5, 2.4), (math.pi, 0.74, 1.4)]:
        c.setLineWidth(lw); c.setLineCap(1); c.line(cx, fy, cx + fr * ln * math.cos(ang), fy + fr * ln * math.sin(ang))
    c.setFillColor(DEEP); c.circle(cx, fy, 2.2, stroke=0, fill=1)
    star5(c, cx, hb + 1.62 * I, 0.17 * I, GOLD)
    # 24 doors, 4 across and 6 down
    dw, dh, gx, gy = 0.4 * I, 0.38 * I, 0.13 * I, 0.1 * I
    gx0 = cx - (4 * dw + 3 * gx) / 2; gy0 = top - 0.22 * I - dh
    n = 0
    for r in range(6):
        for k in range(4):
            n += 1; x = gx0 + k * (dw + gx); y = gy0 - r * (dh + gy)
            if n == 24:
                c.setFillColor(GOLD); c.roundRect(x, y, dw, dh, 2, stroke=0, fill=1)
                star5(c, x + dw / 2, y + dh / 2, 0.11 * I, WOOD)
                continue
            c.setFillColor(SLATE); c.roundRect(x, y, dw, dh, 2, stroke=0, fill=1)
            c.setStrokeColor(TRIM); c.setLineWidth(0.6); c.roundRect(x, y, dw, dh, 2, stroke=1, fill=0)
            c.setFillColor(GOLD); c.circle(x + dw - 5, y + dh / 2, 1.3, stroke=0, fill=1)
            c.setFillColor(PALE); c.setFont("PlayfairSC-B", 10); c.drawCentredString(x + dw / 2 - 1.5, y + dh / 2 - 3.5, str(n))

def front(c, ox):
    r = random.Random(24); I = inch; W = TW * I
    c.saveState()
    cp = c.beginPath(); cp.rect(ox * I, 0, (TW + BLEED) * I, CH * I); c.clipPath(cp, stroke=0, fill=0)
    c.translate(ox * I, BLEED * I)
    for _ in range(46):
        snowflake(c, r.uniform(0.15, 5.85) * I, r.uniform(1.2, 8.85) * I, r.uniform(3, 11), colors.Color(1, 1, 1, alpha=r.uniform(0.12, 0.33)))
    # distant hills
    c.setFillColor(SLATE); p = c.beginPath(); p.moveTo(-0.2 * I, 1.5 * I)
    p.curveTo(1.2 * I, 2.3 * I, 2.2 * I, 1.6 * I, 3.2 * I, 1.9 * I); p.curveTo(4.4 * I, 2.25 * I, 5.2 * I, 1.5 * I, 6.3 * I, 2.0 * I)
    p.lineTo(6.3 * I, -0.2 * I); p.lineTo(-0.2 * I, -0.2 * I); p.close(); c.drawPath(p, stroke=0, fill=1)
    for x, h in [(0.45, 1.25), (0.95, 0.9), (5.1, 1.0), (5.6, 1.35)]: pine(c, x * I, 0.95 * I, h * I, DEEP)
    clock(c, W / 2)
    # snowy foreground
    c.setFillColor(SNOW); p = c.beginPath(); p.moveTo(-0.2 * I, 0.98 * I)
    p.curveTo(1.6 * I, 1.12 * I, 4.0 * I, 0.82 * I, 6.3 * I, 1.05 * I); p.lineTo(6.3 * I, -0.2 * I); p.lineTo(-0.2 * I, -0.2 * I); p.close(); c.drawPath(p, stroke=0, fill=1)
    # type
    c.setFillColor(colors.white); c.setFont("PlayfairSC", 12); c.drawCentredString(W / 2, 8.3 * I, "A Christmas Puzzle Countdown")
    c.setStrokeColor(GOLD); c.setLineWidth(0.8); c.line(2.2 * I, 8.15 * I, 3.8 * I, 8.15 * I)
    c.setFont("PlayfairSC-B", 50); c.drawCentredString(W / 2, 7.3 * I, "The Advent"); c.drawCentredString(W / 2, 6.6 * I, "Clock")
    c.setFont("Crimson-I", 16.5); c.setFillColor(PALE); c.drawCentredString(W / 2, 6.2 * I, "24 doors · 24 puzzles · one hidden star")
    c.setFont("PlayfairSC", 10); c.setFillColor(GOLD)
    c.drawCentredString(W / 2, 5.92 * I, "Logic Puzzles · Codes · Brain Teasers · Hints & Solutions")
    c.setFont("Crimson-I", 14); c.setFillColor(colors.HexColor("#3a4d66")); c.drawCentredString(W / 2, 0.42 * I, "Blake La Pierre")
    c.restoreState()

BLURB = [
 "<b>Every December the Great Advent Clock in the lobby of Snowberry Lodge hides a silver star behind one of its twenty-four little doors, and every year the old clockmaker leaves a puzzle to find it.</b>",
 "Open one door a day from December 1 to Christmas Eve. Behind each one is a short story scene and a puzzle: a secret code, a snowy maze, a hidden picture, a word grid, a logic problem. Each puzzle gives you one word, and each word gives you one key letter. On Christmas Eve the twenty-four letters spell out where the star is hidden.",
 "Every puzzle was checked by a computer program to make sure it has exactly one answer, so there are no broken days.",
]
FEATS = ["24 daily puzzles of 19 different kinds, getting harder towards Christmas",
         "A cozy, festive story that runs through the whole book",
         "Three levels of hints for every door: Nudge, Foothold and Last Step",
         "Full solutions, one per page, with a short explanation",
         "No phone, app or internet needed, just a pencil",
         "A thoughtful stocking stuffer for puzzle-loving adults and teens"]

def back(c):
    r = random.Random(5); I = inch
    for _ in range(24):
        snowflake(c, (X_BACK + r.uniform(0.2, 5.8)) * I, (BLEED + r.uniform(1.6, 8.8)) * I, r.uniform(3, 8), colors.Color(1, 1, 1, alpha=r.uniform(0.1, 0.25)))
    x0 = (X_BACK + 0.55) * I; w = (TW - 1.1) * I
    c.setFillColor(colors.white); c.setFont("PlayfairSC-B", 18)
    c.drawCentredString((X_BACK + TW / 2) * I, (BLEED + 8.25) * I, "Twenty-Four Doors to Christmas")
    c.setStrokeColor(GOLD); c.setLineWidth(0.8); c.line((X_BACK + 2.2) * I, (BLEED + 8.05) * I, (X_BACK + 3.8) * I, (BLEED + 8.05) * I)
    st = ParagraphStyle("bl", fontName="Crimson", fontSize=12, leading=16, textColor=colors.white, alignment=TA_JUSTIFY, spaceAfter=7)
    fl = [Paragraph(t, st) for t in BLURB]
    li = ParagraphStyle("li", parent=st, alignment=TA_LEFT, fontSize=11.3, leading=14.5, leftIndent=14, firstLineIndent=-12, spaceAfter=3, textColor=PALE)
    fl += [Paragraph("<font name='DejaVu' color='#ffd27a' size='8'>❄</font>&nbsp;&nbsp;" + t, li) for t in FEATS]
    f = Frame(x0, (BLEED + 1.9) * I, w, 6.0 * I, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
    f.addFromList(fl, c); assert not fl, "back cover text overflow"
    # lower left: a little door log card (clear of the barcode area)
    cx, cy = (X_BACK + 0.55) * I, (BLEED + 0.4) * I
    c.setFillColor(SLATE); c.roundRect(cx, cy, 1.1 * I, 1.2 * I, 4, stroke=0, fill=1)
    c.setStrokeColor(TRIM); c.setLineWidth(0.8); c.roundRect(cx + 4, cy + 4, 1.1 * I - 8, 1.2 * I - 8, 3, stroke=1, fill=0)
    c.setFillColor(PALE); c.setFont("PlayfairSC-B", 26); c.drawCentredString(cx + 0.55 * I, cy + 0.45 * I, "24")
    c.setFillColor(GOLD); c.circle(cx + 0.93 * I, cy + 0.6 * I, 2.2, stroke=0, fill=1)
    tx = (X_BACK + 1.9) * I
    LINES = ["One door a day,", "December 1 to 24.", "One letter each day.", "One message at the end."]
    c.setFont("Crimson-I", 10.5); c.setFillColor(PALE)
    for i, t in enumerate(LINES): c.drawString(tx, (BLEED + 1.45 - i * 0.19) * I, t)
    c.setFont("PlayfairSC", 8.5); c.setFillColor(GOLD); c.drawString(tx, (BLEED + 0.55) * I, "Puzzles & Games")
    c.setFont("Crimson-I", 9); c.setFillColor(PALE); c.drawString(tx, (BLEED + 0.38) * I, "Ages 12 and up")
    assert tx + max(c.stringWidth(t, "Crimson-I", 10.5) for t in LINES) < (X_BACK + TW - 0.25 - 2.0) * I - 6

def main(out="../standalone-01-the-advent-clock-cover.pdf", guides=False):
    I = inch
    c = canvas.Canvas(out, pagesize=(CW * I, CH * I), initialFontName="Crimson")
    c.setTitle("The Advent Clock — KDP cover"); c.setAuthor("Blake La Pierre")
    c.setFillColor(NAVY); c.rect(0, 0, CW * I, CH * I, stroke=0, fill=1)
    back(c)
    c.setFillColor(colors.HexColor("#17304f")); c.rect(X_SPINE * I, 0, SPINE * I, CH * I, stroke=0, fill=1)
    # spine text only when KDP allows it (more than 79 pages); keep 0.0625in clear on each side of the text
    assert PAGES > 79
    fs = 7.5; cap = 0.71 * fs
    assert cap <= (SPINE - 2 * 0.0625) * 72 + 0.01, (cap, SPINE)
    c.saveState(); c.translate((X_SPINE + SPINE / 2) * I, (BLEED + TH / 2) * I); c.rotate(-90)
    c.setFillColor(colors.white); c.setFont("PlayfairSC-B", fs); c.drawCentredString(-1.1 * I, -cap / 2, "THE ADVENT CLOCK")
    c.setFillColor(GOLD); c.setFont("PlayfairSC-B", fs); c.drawCentredString(0.75 * I, -cap / 2, "A CHRISTMAS PUZZLE COUNTDOWN")
    c.setFillColor(PALE); c.setFont("PlayfairSC-B", fs); c.drawCentredString(3.1 * I, -cap / 2, "BLAKE LA PIERRE")
    c.restoreState()
    front(c, X_FRONT)
    bx, by = X_BACK + TW - 0.25 - 2.0, BLEED + 0.25
    if guides:
        c.setLineWidth(0.6)
        c.setStrokeColor(colors.red); c.rect(BLEED * I, BLEED * I, (CW - 2 * BLEED) * I, TH * I)
        c.setStrokeColor(colors.magenta); c.line(X_SPINE * I, 0, X_SPINE * I, CH * I); c.line(X_FRONT * I, 0, X_FRONT * I, CH * I)
        c.setStrokeColor(colors.lime); c.setDash(3, 3)
        c.rect((X_BACK + 0.125) * I, (BLEED + 0.125) * I, (TW - 0.25) * I, (TH - 0.25) * I)
        c.rect((X_FRONT + 0.125) * I, (BLEED + 0.125) * I, (TW - 0.25) * I, (TH - 0.25) * I)
        c.setStrokeColor(colors.yellow); c.setDash()
        c.rect(bx * I, by * I, 2.0 * I, 1.2 * I)
    c.showPage(); c.save()
    return dict(pages=PAGES, spine_in=round(SPINE, 6), width_in=round(CW, 6), height_in=CH, bleed_in=BLEED,
                barcode_box_in=[round(bx, 4), by, 2.0, 1.2], spine_text_pt=fs)

if __name__ == "__main__":
    m = main(); main("../tmp/standalone-01-the-advent-clock-cover-guides.pdf", guides=True)
    print(m); json.dump(m, open("../cover-info.json", "w"), indent=1)
