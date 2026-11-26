"""KDP case-laminate HARDCOVER cover, 6x9 trim, white paper, B&W interior.
Spec (KDP Create a Hardcover Cover help + cover calculator layout, same formula as
standalone/01-the-advent-clock/src/cover_hardcover.py): 0.591in (15mm) wrap on every edge,
boards = trim + 0.197in wide / + 0.236in tall, spine = pages x 0.002252 + 0.189in, 0.394in (10mm)
hinge beside the spine, text >= 0.635in from the board edges, barcode 2 x 1.2in clear of the hinge.
Same navy-and-gold palette as the other Frostwood Puzzle Book covers."""
import json, math, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
import build
from build import snowflake, draw_quilt, grid_size, D, NP, EX

HERE = os.path.dirname(os.path.abspath(__file__))
info = json.load(open(os.path.join(HERE, "..", "build-info.json"))); PAGES = info["pages"]
BLEED = 0.591; TW, TH = 6.0 + 0.197, 9.0 + 0.236; HINGE = 0.394; SAFE = 0.635
SPINE = PAGES * 0.002252 + 0.189
CW = BLEED + TW + SPINE + TW + BLEED; CH = BLEED + TH + BLEED
NAVY = colors.HexColor("#1f3a5f"); GOLD = colors.HexColor("#ffd27a"); PALE = colors.HexColor("#dbe6f1"); SNOW = colors.HexColor("#f4f7fb")
DEEP = colors.HexColor("#15293f"); SLATE = colors.HexColor("#2c4d74")
X_BACK = BLEED; X_SPINE = BLEED + TW; X_FRONT = BLEED + TW + SPINE
I = inch


def cottage(c, x, y, w, h, sc=1.0):
    c.setFillColor(DEEP); c.rect(x, y, w, h, stroke=0, fill=1)
    p = c.beginPath(); p.moveTo(x - 0.04 * I, y + h); p.lineTo(x + w / 2, y + h + 0.2 * I * sc); p.lineTo(x + w + 0.04 * I, y + h); p.close(); c.drawPath(p, stroke=0, fill=1)
    c.setFillColor(SNOW); p = c.beginPath(); p.moveTo(x - 0.04 * I, y + h); p.lineTo(x + w / 2, y + h + 0.2 * I * sc); p.lineTo(x + w + 0.04 * I, y + h)
    p.lineTo(x + w - 0.02 * I, y + h + 0.02 * I); p.lineTo(x + w / 2, y + h + 0.15 * I * sc); p.lineTo(x + 0.02 * I, y + h + 0.02 * I); p.close(); c.drawPath(p, stroke=0, fill=1)
    c.setFillColor(GOLD)
    for i in range(int(w / (0.16 * I))): c.rect(x + 0.05 * I + i * 0.16 * I, y + h * 0.45, 0.07 * I, 0.07 * I, stroke=0, fill=1)


def cover_pine(c, x, y, h):
    c.setFillColor(DEEP)
    for k in range(3):
        yy = y + k * h * 0.28; ww = h * (0.42 - k * 0.1)
        p = c.beginPath(); p.moveTo(x - ww, yy); p.lineTo(x, yy + h * 0.5); p.lineTo(x + ww, yy); p.close(); c.drawPath(p, stroke=0, fill=1)


# three patchwork quilts on a washing line in the snow. The middle (largest) quilt is the solved worked
# example from the How to Play pages: its patches are the 7 rectangles of that 5x5 Quilts puzzle.
PAL = None


def quilt_cover(c, x, y, w, h, rects, n, seed):
    """Quilt with a pale border; rects = [r0, c0, h, w] patches of an n x n grid. (x, y) = bottom-left."""
    r = random.Random(seed)
    fills = [GOLD, SLATE, PALE, colors.HexColor("#c79a4a"), colors.white, colors.HexColor("#3d6390")]
    b = 0.06 * I
    c.setFillColor(SNOW); c.rect(x, y, w, h, stroke=0, fill=1)
    ix, iy, iw, ih = x + b, y + b, w - 2 * b, h - 2 * b; sx, sy = iw / n, ih / n
    order = list(range(len(rects))); r.shuffle(order)
    for k, i in enumerate(order):
        r0, c0, hh, ww = rects[i]
        c.setFillColor(fills[k % len(fills)])
        c.rect(ix + c0 * sx, iy + ih - (r0 + hh) * sy, ww * sx, hh * sy, stroke=0, fill=1)
    c.setStrokeColor(DEEP); c.setLineWidth(1.1)
    for r0, c0, hh, ww in rects:
        c.rect(ix + c0 * sx, iy + ih - (r0 + hh) * sy, ww * sx, hh * sy, stroke=1, fill=0)
    # running stitches along the border
    c.setStrokeColor(DEEP); c.setLineWidth(0.6); c.setDash(2, 2.4)
    c.rect(x + b * 0.5, y + b * 0.5, w - b, h - b, stroke=1, fill=0); c.setDash()
    c.setStrokeColor(DEEP); c.setLineWidth(1.2); c.rect(x, y, w, h, stroke=1, fill=0)
    # pegs
    c.setFillColor(DEEP)
    for u in (0.12, 0.88): c.rect(x + w * u - 0.025 * I, y + h - 0.06 * I, 0.05 * I, 0.14 * I, stroke=0, fill=1)


def washing_line(c, x0, x1, ytop):
    c.setFillColor(DEEP)
    for xx in (x0, x1):
        c.rect(xx - 0.04 * I, ytop - 2.35 * I, 0.08 * I, 2.4 * I, stroke=0, fill=1)
    c.setStrokeColor(PALE); c.setLineWidth(1.0)
    p = c.beginPath(); p.moveTo(x0, ytop); p.curveTo(x0 + (x1 - x0) * 0.3, ytop - 0.1 * I, x0 + (x1 - x0) * 0.7, ytop - 0.1 * I, x1, ytop); c.drawPath(p, stroke=1, fill=0)
    A = [[0, 0, 2, 2], [0, 2, 1, 2], [1, 2, 1, 1], [1, 3, 1, 1], [2, 0, 2, 1], [2, 1, 1, 3], [3, 1, 1, 3]]
    B = EX["rects"]
    C = [[0, 0, 1, 3], [0, 3, 2, 1], [1, 0, 2, 1], [1, 1, 1, 2], [2, 1, 2, 3], [3, 0, 1, 1]]
    span = x1 - x0
    for (u, w, h, rects, n, seed) in [(0.03, 0.28, 1.4, A, 4, 3), (0.34, 0.32, 1.8, B, 5, 5), (0.69, 0.28, 1.45, C, 4, 9)]:
        qx = x0 + span * u; qw = span * w
        sag = 0.075 * I * (1 - (2 * (u + w / 2) - 1) ** 2)
        quilt_cover(c, qx, ytop - sag - h * I, qw, h * I, rects, n, seed)
    # snow drift at the posts
    c.setFillColor(SNOW); p = c.beginPath(); p.moveTo(x0 - 0.6 * I, ytop - 2.34 * I)
    p.curveTo(x0 + 1.2 * I, ytop - 2.26 * I, x1 - 1.2 * I, ytop - 2.38 * I, x1 + 0.6 * I, ytop - 2.3 * I); p.lineTo(x1 + 0.6 * I, ytop - 2.8 * I); p.lineTo(x0 - 0.6 * I, ytop - 2.8 * I); p.close(); c.drawPath(p, stroke=0, fill=1)


def front(c, ox):
    r = random.Random(19); W = TW * I
    c.saveState()
    cp = c.beginPath(); cp.rect(ox * I, 0, (TW + BLEED) * I, CH * I); c.clipPath(cp, stroke=0, fill=0)
    c.translate(ox * I, BLEED * I)
    for _ in range(40):
        snowflake(c, r.uniform(0.2, 6.0) * I, r.uniform(3.0, 9.6) * I, r.uniform(3, 10), colors.Color(1, 1, 1, alpha=r.uniform(0.12, 0.32)))
    c.saveState(); c.translate(0, 0.42 * I)   # the scene sits a little higher, clear of the series line and author
    # mountains
    c.setFillColor(SLATE); p = c.beginPath(); p.moveTo(-0.7 * I, 2.4 * I)
    for x, y in [(0.9, 3.4), (1.8, 2.8), (3.1, 4.05), (4.3, 2.9), (5.3, 3.45), (6.9, 2.7), (6.9, -0.7), (-0.7, -0.7)]: p.lineTo(x * I, y * I)
    p.close(); c.drawPath(p, stroke=0, fill=1)
    c.setFillColor(colors.white)
    for (px, py, s) in [(0.9, 3.4, 0.24), (3.1, 4.05, 0.34), (5.3, 3.45, 0.24)]:
        p = c.beginPath(); p.moveTo(px * I, py * I); p.lineTo((px - s) * I, (py - s * 0.8) * I); p.lineTo((px + s) * I, (py - s * 0.8) * I); p.close(); c.drawPath(p, stroke=0, fill=1)
    # the lodge on the shoulder
    lx, ly = 3.65 * I, 3.3 * I
    c.setFillColor(DEEP); c.rect(lx, ly, 0.5 * I, 0.3 * I, stroke=0, fill=1)
    p = c.beginPath(); p.moveTo(lx - 0.05 * I, ly + 0.3 * I); p.lineTo(lx + 0.25 * I, ly + 0.46 * I); p.lineTo(lx + 0.55 * I, ly + 0.3 * I); p.close(); c.drawPath(p, stroke=0, fill=1)
    c.setFillColor(GOLD)
    for i in range(4):
        for j in range(2): c.rect(lx + (0.06 + i * 0.105) * I, ly + (0.06 + j * 0.11) * I, 0.05 * I, 0.05 * I, stroke=0, fill=1)
    # the snowed-under fields
    c.setFillColor(SNOW); p = c.beginPath(); p.moveTo(-0.7 * I, 2.45 * I)
    p.curveTo(1.5 * I, 2.6 * I, 3.8 * I, 2.3 * I, 6.9 * I, 2.5 * I); p.lineTo(6.9 * I, -1.3 * I); p.lineTo(-0.7 * I, -1.3 * I); p.close()
    c.drawPath(p, stroke=0, fill=1)
    for x, h in [(0.32, 0.62), (0.7, 0.44), (5.35, 0.56), (5.75, 0.72)]:
        cover_pine(c, x * I, 2.3 * I, h * I)
    cottage(c, 1.15 * I, 2.34 * I, 0.42 * I, 0.24 * I); cottage(c, 4.65 * I, 2.36 * I, 0.38 * I, 0.22 * I)
    # the washing line of quilts, centred on the part of the board clear of the hinge
    mid = HINGE * I + (W - HINGE * I) / 2
    washing_line(c, mid - 2.25 * I, mid + 2.25 * I, 3.35 * I)
    c.restoreState()
    # type, centred on the part of the board clear of the hinge
    cx = (HINGE + (TW - HINGE) / 2) * I
    def centred(txt, font, size, y, col):
        c.setFont(font, size); c.setFillColor(col); c.drawCentredString(cx, y, txt)
        wdt = pdfmetrics.stringWidth(txt, font, size)
        assert cx - wdt / 2 >= (HINGE + 0.1) * I and cx + wdt / 2 <= (TW - SAFE) * I, (txt, wdt / I)
    centred("A Winter Patchwork Puzzle Book", "PlayfairSC", 11.5, 8.25 * I, colors.white)
    c.setStrokeColor(GOLD); c.setLineWidth(0.8); c.line(cx - 0.8 * I, 8.1 * I, cx + 0.8 * I, 8.1 * I)
    centred("The Quilts of", "PlayfairSC-B", 42, 7.22 * I, colors.white)
    centred("Frostwood", "PlayfairSC-B", 48, 6.49 * I, colors.white)
    centred(f"{NP} Shikaku Logic Puzzles", "Crimson-I", 17, 5.82 * I, PALE)
    centred("from the village sewing circle to the mountain huts", "Crimson-I", 14, 5.52 * I, PALE)
    centred("Easy to Expert · Big, Clear Grids · Solutions Included", "PlayfairSC", 10.5, 5.04 * I, GOLD)
    centred("A Frostwood Puzzle Book", "PlayfairSC", 11, 0.98 * I, NAVY)
    centred("Blake La Pierre", "Crimson-I", 13.5, 0.7 * I, colors.HexColor("#3a4d66"))
    assert 0.7 * I >= SAFE * I and 8.25 * I + 11 <= (TH - SAFE) * I
    c.restoreState()


cnt = {b: len(D[b]) for b in ("Easy", "Medium", "Hard", "Expert")}
BLURB = [
 "<b>When the snow settles in, Frostwood sews. The sewing circle meets in the village hall, the lodge keepers piece a new quilt for every guest room, and up in the mountain huts the heirloom quilts are pieced again by lamplight.</b>",
 f"{NP} quilt patterns are waiting, each with only a few numbers chalked on its squares. Each one is a Shikaku puzzle: cut the whole quilt into rectangular patches so that every patch holds exactly one number, and that number is the patch’s size.",
 "Every puzzle has exactly one solution, checked by computer, and every one can be solved by logic alone.",
]
FEATS = [f"{NP} Shikaku puzzles in four parts, from 7×7 to 12×12",
         f"{cnt['Easy']} Easy, {cnt['Medium']} Medium, {cnt['Hard']} Hard and {cnt['Expert']} Expert",
         "Large, clear grids with room to pencil in",
         "How-to-play guide with a fully worked example",
         "Complete solutions at the back, every patch outlined",
         "Book sixteen of the cozy Frostwood Puzzle Books, in hardcover"]


def back(c):
    r = random.Random(5)
    for _ in range(22):
        snowflake(c, (X_BACK + r.uniform(0.2, 5.9)) * I, (BLEED + r.uniform(2.9, 9.0)) * I, r.uniform(3, 8), colors.Color(1, 1, 1, alpha=r.uniform(0.1, 0.22)))
    x0 = (X_BACK + 0.72) * I; w = (TW - 0.72 - HINGE - 0.25) * I
    c.setFillColor(colors.white); c.setFont("PlayfairSC-B", 18)
    mid = (X_BACK + 0.72 + (TW - 0.72 - HINGE - 0.25) / 2) * I
    c.drawCentredString(mid, (BLEED + 8.3) * I, "Piece the Quilts")
    c.setStrokeColor(GOLD); c.setLineWidth(0.8); c.line(mid - 0.8 * I, (BLEED + 8.1) * I, mid + 0.8 * I, (BLEED + 8.1) * I)
    st = ParagraphStyle("bl", fontName="Crimson", fontSize=12.8, leading=17.4, textColor=colors.white, alignment=TA_JUSTIFY, spaceAfter=7)
    fl = [Paragraph(t, st) for t in BLURB]
    li = ParagraphStyle("li", parent=st, alignment=TA_LEFT, fontSize=12, leading=15.6, leftIndent=14, firstLineIndent=-12, spaceAfter=3, textColor=PALE)
    fl += [Paragraph("<font name='DejaVu' color='#ffd27a' size='8'>❄</font>&nbsp;&nbsp;" + t, li) for t in FEATS]
    f = Frame(x0, (BLEED + 2.75) * I, w, 5.25 * I, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
    f.addFromList(fl, c); assert not fl, "back cover text overflow"
    # lower left: a sample puzzle card (clear of the barcode area)
    p = D["Easy"][1]; cs = 0.215 * I; gw, gh = grid_size(p, cs)
    cx, cy = (X_BACK + 0.72) * I, (BLEED + 0.76) * I; cw, ch = 1.62 * I, 1.62 * I
    c.setFillColor(colors.white); c.roundRect(cx, cy, cw, ch, 4, stroke=0, fill=1)
    draw_quilt(c, cx + (cw - gw) / 2, cy + (ch + gh) / 2, cs, p)
    tx = (X_BACK + 2.45) * I
    LINES = ["Cut the quilt into", "rectangles. Each", "holds one number:", "its size in", "squares."]
    c.setFillColor(PALE); c.setFont("PlayfairSC", 9.5); c.drawString(tx, (BLEED + 2.22) * I, f"Puzzle No. {p['num']}")
    c.setFont("Crimson-I", 9.5)
    bx = X_BACK + TW - HINGE - 0.25 - 2.0
    for i, t in enumerate(LINES):
        assert tx + pdfmetrics.stringWidth(t, "Crimson-I", 9.5) < (bx - 0.08) * I, t   # stay clear of the barcode box
        c.drawString(tx, (BLEED + 2.0 - i * 0.18) * I, t)
    c.setFont("PlayfairSC", 8.5); c.setFillColor(GOLD); c.drawString(tx, (BLEED + 0.93) * I, "Logic Puzzles")
    c.setFont("Crimson-I", 9); c.setFillColor(PALE); c.drawString(tx, (BLEED + 0.78) * I, "Ages 12 and up")
    assert tx + pdfmetrics.stringWidth("Logic Puzzles", "PlayfairSC", 8.5) < (bx - 0.08) * I and tx + pdfmetrics.stringWidth("Ages 12 and up", "Crimson-I", 9) < (bx - 0.08) * I
    assert cy + ch < (BLEED + 2.75) * I - 4


def main(out=os.path.join(HERE, "..", "frostwood-16-the-quilts-of-frostwood-cover.pdf"), guides=False):
    c = canvas.Canvas(out, pagesize=(CW * I, CH * I), initialFontName="Crimson")
    c.setTitle("The Quilts of Frostwood — KDP hardcover cover"); c.setAuthor("Blake La Pierre")
    c.setFillColor(NAVY); c.rect(0, 0, CW * I, CH * I, stroke=0, fill=1)
    back(c)
    c.setFillColor(colors.HexColor("#17304f")); c.rect(X_SPINE * I, 0, SPINE * I, CH * I, stroke=0, fill=1)
    # spine text only when KDP allows it (more than 79 pages); keep 0.0625in clear on each side of the text
    assert PAGES > 79
    fs = 12.5; cap = 0.71 * fs
    assert cap <= (SPINE - 2 * 0.0625) * 72 + 0.01, (cap, SPINE)
    c.saveState(); c.translate((X_SPINE + SPINE / 2) * I, (BLEED + TH / 2) * I); c.rotate(-90)
    c.setFillColor(colors.white); c.setFont("PlayfairSC-B", fs); c.drawCentredString(-0.95 * I, -cap / 2, "The Quilts of Frostwood")
    c.setFillColor(GOLD); c.setFont("Crimson-I", 10); c.drawCentredString(1.4 * I, -3.4, f"{NP} Shikaku Puzzles")
    c.setFillColor(PALE); c.setFont("Crimson-I", 11); c.drawCentredString(3.0 * I, -3.8, "Blake La Pierre")
    ext = max(0.95 * I + pdfmetrics.stringWidth("The Quilts of Frostwood", "PlayfairSC-B", fs) / 2, 3.0 * I + pdfmetrics.stringWidth("Blake La Pierre", "Crimson-I", 11) / 2)
    assert ext <= (TH / 2 - SAFE) * I, ext / I
    c.restoreState()
    front(c, X_FRONT)
    bx, by = X_BACK + TW - HINGE - 0.25 - 2.0, BLEED + 0.76
    if guides:
        c.setLineWidth(0.8)
        c.setStrokeColor(colors.red); c.rect(BLEED * I, BLEED * I, (CW - 2 * BLEED) * I, TH * I)  # board/book edge (wrap outside)
        c.setStrokeColor(colors.magenta); c.line(X_SPINE * I, 0, X_SPINE * I, CH * I); c.line(X_FRONT * I, 0, X_FRONT * I, CH * I)
        c.setStrokeColor(colors.orange)
        for x in (X_SPINE - HINGE, X_FRONT + HINGE): c.line(x * I, 0, x * I, CH * I)  # hinge
        c.setStrokeColor(colors.lime); c.setDash(3, 3)
        c.rect((X_BACK + SAFE) * I, (BLEED + SAFE) * I, (TW - SAFE - HINGE) * I, (TH - 2 * SAFE) * I)
        c.rect((X_FRONT + HINGE) * I, (BLEED + SAFE) * I, (TW - SAFE - HINGE) * I, (TH - 2 * SAFE) * I)
        c.setStrokeColor(colors.yellow); c.setDash()
        c.rect(bx * I, by * I, 2.0 * I, 1.2 * I)
    c.showPage(); c.save()
    return dict(pages=PAGES, spine_in=round(SPINE, 6), width_in=round(CW, 6), height_in=round(CH, 6), bleed_in=BLEED,
                barcode_box_in=[round(bx, 4), round(by, 4), 2.0, 1.2], spine_text_pt=fs)


if __name__ == "__main__":
    m = main(); main(os.path.join(HERE, "..", "tmp", "frostwood-16-the-quilts-of-frostwood-cover-guides.pdf"), guides=True)
    m.update(wrap_in=BLEED, hinge_in=HINGE, board_in=[TW, TH], kind="hardcover case laminate")
    print(m); json.dump(m, open(os.path.join(HERE, "..", "cover-info.json"), "w"), indent=1)
