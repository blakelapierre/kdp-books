"""KDP full-wrap paperback cover: 6x9 trim, 0.125in bleed, white paper B&W spine = pages x 0.002252in."""
import json, math, random, sys
sys.path.insert(0, ".")
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
import build  # registers fonts
from build import snowflake

info = json.load(open("../build-info.json")); PAGES = info["pages"]
BLEED = 0.125; TW, TH = 6.0, 9.0
SPINE = PAGES * 0.002252
CW = BLEED + TW + SPINE + TW + BLEED; CH = BLEED + TH + BLEED
NAVY = colors.HexColor("#1f3a5f"); GOLD = colors.HexColor("#ffd27a"); PALE = colors.HexColor("#dbe6f1"); SNOW = colors.HexColor("#f4f7fb")
X_BACK = BLEED                      # back trim left edge
X_SPINE = BLEED + TW                # spine left
X_FRONT = BLEED + TW + SPINE        # front trim left edge

def front_art(c, ox):
    """Sample title art, drawn in a 6x9 box whose lower-left trim corner is (ox, BLEED)."""
    r = random.Random(7)
    c.saveState()
    cp = c.beginPath(); cp.rect(ox * inch, 0, (TW + BLEED) * inch, CH * inch); c.clipPath(cp, stroke=0, fill=0)
    c.translate(ox * inch, BLEED * inch)
    for _ in range(38):
        snowflake(c, r.uniform(0.2, 5.8) * inch, r.uniform(0.2, 8.8) * inch, r.uniform(3, 11), colors.Color(1, 1, 1, alpha=r.uniform(0.12, 0.35)))
    c.setFillColor(colors.HexColor("#2c4d74")); p = c.beginPath(); p.moveTo(-0.2 * inch, 1.6 * inch)
    for x, y in [(1.2, 3.0), (2.0, 2.3), (3.1, 3.6), (4.3, 2.4), (5.1, 3.0), (6.2, 2.2), (6.2, -0.2), (-0.2, -0.2)]: p.lineTo(x * inch, y * inch)
    p.close(); c.drawPath(p, stroke=0, fill=1)
    c.setFillColor(colors.white)
    for (px, py, s) in [(1.2, 3.0, 0.28), (3.1, 3.6, 0.32), (5.1, 3.0, 0.22)]:
        p = c.beginPath(); p.moveTo(px * inch, py * inch); p.lineTo((px - s) * inch, (py - s * 0.8) * inch); p.lineTo((px + s) * inch, (py - s * 0.8) * inch); p.close(); c.drawPath(p, stroke=0, fill=1)
    c.setFillColor(SNOW); c.rect(-0.2 * inch, -0.2 * inch, 6.4 * inch, 1.45 * inch, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#15293f")); c.rect(2.05 * inch, 1.25 * inch, 1.9 * inch, 1.25 * inch, stroke=0, fill=1)
    p = c.beginPath(); p.moveTo(1.9 * inch, 2.5 * inch); p.lineTo(3 * inch, 3.05 * inch); p.lineTo(4.1 * inch, 2.5 * inch); p.close(); c.drawPath(p, stroke=0, fill=1)
    c.setFillColor(SNOW); p = c.beginPath(); p.moveTo(1.9 * inch, 2.5 * inch); p.lineTo(3 * inch, 3.05 * inch); p.lineTo(4.1 * inch, 2.5 * inch)
    p.lineTo(4.0 * inch, 2.47 * inch); p.lineTo(3 * inch, 2.95 * inch); p.lineTo(2.0 * inch, 2.47 * inch); p.close(); c.drawPath(p, stroke=0, fill=1)
    for row in range(4):
        for col in range(6):
            lit = r.random() < 0.7
            c.setFillColor(GOLD if lit else colors.HexColor("#27405e"))
            c.rect((2.2 + col * 0.28) * inch, (1.38 + row * 0.27) * inch, 0.14 * inch, 0.15 * inch, stroke=0, fill=1)
    c.setFillColor(GOLD); c.rect(2.88 * inch, 1.25 * inch, 0.24 * inch, 0.3 * inch, stroke=0, fill=1)
    W = 6 * inch
    c.setFillColor(colors.white); c.setFont("PlayfairSC", 11.5); c.drawCentredString(W / 2, 7.95 * inch, "A Snowbound Hotel Mystery")
    c.setStrokeColor(GOLD); c.setLineWidth(0.8); c.line(2.2 * inch, 7.8 * inch, 3.8 * inch, 7.8 * inch)
    c.setFont("PlayfairSC-B", 40); c.drawCentredString(W / 2, 7.0 * inch, "The Thief"); c.drawCentredString(W / 2, 6.33 * inch, "Stayed the Night")
    c.setFont("Crimson-I", 15); c.setFillColor(PALE)
    c.drawCentredString(W / 2, 5.62 * inch, "Twelve cozy cases. One snowbound week.")
    c.drawCentredString(W / 2, 5.34 * inch, "Can you find who did it?")
    c.setFont("PlayfairSC", 10); c.setFillColor(GOLD)
    c.drawCentredString(W / 2, 4.85 * inch, "12 Elimination Puzzles · 40 to 152 Suspects")
    c.setFillColor(NAVY); c.setFont("PlayfairSC", 11); c.drawCentredString(W / 2, 0.78 * inch, "An Elimination Puzzle Book")
    c.setFont("Crimson-I", 12); c.setFillColor(colors.HexColor("#3a4d66")); c.drawCentredString(W / 2, 0.5 * inch, "Blake La Pierre")
    c.restoreState()

BLURB = [
 "<b>The road is gone. The snowplough is a week away. And things keep going missing.</b>",
 "When a blizzard seals off the Frostwood Lodge, its one hundred and fifty-two guests settle in for a week of cocoa, skating and cake. Then Mrs. Brisket’s secret cocoa tin vanishes. Then the snowman’s top hat. Then Lady Winifred’s famous sapphire necklace, straight from her bedside table.",
 "With a developer circling to buy the lodge and knock it down, the manager needs a detective, fast. That’s you.",
 "Each case gives you the story, a guest register and a set of clues. Cross suspects off one by one until only the culprit remains. Every puzzle has exactly one answer, and every clue is fair.",
]
FEATS = ["12 connected, cozy cases across one snowbound week",
         "Grows from 40 suspects and 6 clues to 152 suspects and 14 clues",
         "Floor, room, neighbour and roommate logic in the later cases",
         "Hints and full step-by-step solutions for every case",
         "No violence: just pranks, pinched pastries and one very salty cake. For teens and adults."]

def back(c):
    x0 = (X_BACK + 0.55) * inch; w = (TW - 1.1) * inch
    r = random.Random(11)
    for _ in range(26):
        snowflake(c, r.uniform(X_BACK + 0.2, X_BACK + TW - 0.2) * inch, r.uniform(2.0, 9.0) * inch, r.uniform(3, 9), colors.Color(1, 1, 1, alpha=r.uniform(0.1, 0.25)))
    c.setFillColor(colors.white); c.setFont("PlayfairSC-B", 17)
    c.drawCentredString((X_BACK + TW / 2) * inch, (BLEED + 8.25) * inch, "Twelve Mysteries.")
    c.drawCentredString((X_BACK + TW / 2) * inch, (BLEED + 7.97) * inch, "One Snowbound Week.")
    c.setStrokeColor(GOLD); c.setLineWidth(0.8); c.line((X_BACK + 2.2) * inch, (BLEED + 7.8) * inch, (X_BACK + 3.8) * inch, (BLEED + 7.8) * inch)
    st = ParagraphStyle("bl", fontName="Crimson", fontSize=12, leading=16, textColor=colors.white, alignment=TA_JUSTIFY, spaceAfter=7)
    fl = [Paragraph(t, st) for t in BLURB]
    li = ParagraphStyle("li", parent=st, alignment=TA_LEFT, fontSize=11.3, leading=14.5, leftIndent=14, firstLineIndent=-12, spaceAfter=3, textColor=PALE)
    fl += [Paragraph("<font name='DejaVu' color='#ffd27a' size='8'>❄</font>&nbsp;&nbsp;" + t, li) for t in FEATS]
    f = Frame(x0, (BLEED + 1.8) * inch, w, 5.85 * inch, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
    rest = f.addFromList(fl, c); assert not fl, "back cover text overflow"
    # small lodge vignette, lower left (clear of the barcode area)
    c.saveState(); c.translate((X_BACK + 0.6) * inch, (BLEED + 0.45) * inch)
    c.setFillColor(colors.HexColor("#15293f")); c.rect(0, 0, 0.9 * inch, 0.6 * inch, stroke=0, fill=1)
    p = c.beginPath(); p.moveTo(-0.07 * inch, 0.6 * inch); p.lineTo(0.45 * inch, 0.88 * inch); p.lineTo(0.97 * inch, 0.6 * inch); p.close(); c.drawPath(p, stroke=0, fill=1)
    rr = random.Random(3)
    for row in range(3):
        for col in range(4):
            c.setFillColor(GOLD if rr.random() < 0.7 else colors.HexColor("#27405e"))
            c.rect((0.09 + col * 0.2) * inch, (0.1 + row * 0.16) * inch, 0.09 * inch, 0.09 * inch, stroke=0, fill=1)
    c.restoreState()
    c.setFillColor(PALE); c.setFont("PlayfairSC", 9); c.drawString((X_BACK + 1.7) * inch, (BLEED + 0.95) * inch, "Frostwood Lodge")
    c.setFont("Crimson-I", 9.5); c.drawString((X_BACK + 1.7) * inch, (BLEED + 0.75) * inch, "Puzzles & Games · Ages 12 and up")

def main(out="../cover.pdf", guides=False):
    c = canvas.Canvas(out, pagesize=(CW * inch, CH * inch))
    c.setTitle("The Thief Stayed the Night — KDP cover"); c.setAuthor("Blake La Pierre")
    c.setFillColor(NAVY); c.rect(0, 0, CW * inch, CH * inch, stroke=0, fill=1)
    back(c)
    # spine
    c.setFillColor(colors.HexColor("#17304f")); c.rect(X_SPINE * inch, 0, SPINE * inch, CH * inch, stroke=0, fill=1)
    c.saveState(); c.translate((X_SPINE + SPINE / 2) * inch, (BLEED + TH / 2) * inch); c.rotate(-90)
    c.setFillColor(colors.white); c.setFont("PlayfairSC-B", 11); c.drawCentredString(-0.55 * inch, -3.8, "The Thief Stayed the Night")
    c.setFillColor(GOLD); c.setFont("Crimson-I", 10); c.drawCentredString(2.75 * inch, -3.4, "Blake La Pierre")
    c.restoreState()
    front_art(c, X_FRONT)
    if guides:   # preview only: trim, spine, safe zone and barcode area
        c.setLineWidth(0.6)
        c.setStrokeColor(colors.red); c.rect(BLEED * inch, BLEED * inch, (CW - 2 * BLEED) * inch, TH * inch)
        c.setStrokeColor(colors.magenta); c.line(X_SPINE * inch, 0, X_SPINE * inch, CH * inch); c.line(X_FRONT * inch, 0, X_FRONT * inch, CH * inch)
        c.setStrokeColor(colors.lime); c.setDash(3, 3)
        c.rect((X_BACK + 0.125) * inch, (BLEED + 0.125) * inch, (TW - 0.25) * inch, (TH - 0.25) * inch)
        c.rect((X_FRONT + 0.125) * inch, (BLEED + 0.125) * inch, (TW - 0.25) * inch, (TH - 0.25) * inch)
        c.setStrokeColor(colors.yellow); c.setDash()
    bx, by = X_BACK + TW - 0.25 - 2.0, BLEED + 0.25
    if guides: c.rect(bx * inch, by * inch, 2.0 * inch, 1.2 * inch)
    c.showPage(); c.save()
    return dict(pages=PAGES, spine_in=SPINE, width_in=CW, height_in=CH, barcode_box_in=[bx, by, 2.0, 1.2])

if __name__ == "__main__":
    m = main(); main("/tmp/cover-guides.pdf", guides=True)
    print(m); json.dump(m, open("../cover-info.json", "w"), indent=1)
