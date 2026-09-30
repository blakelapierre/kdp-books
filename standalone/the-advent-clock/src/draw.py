from reportlab.lib.colors import Color
"""Drawing code for every puzzle type (puzzle and solution views). Grayscale only."""
import math
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

G = "/usr/share/fonts/truetype/sand-box/google/"
for n, p in [("Crimson", "Crimson Text/CrimsonText-Regular.ttf"), ("Crimson-I", "Crimson Text/CrimsonText-Italic.ttf"),
             ("Crimson-B", "Crimson Text/CrimsonText-Bold.ttf"), ("Crimson-SB", "Crimson Text/CrimsonText-SemiBold.ttf"),
             ("Crimson-BI", "Crimson Text/CrimsonText-BoldItalic.ttf"),
             ("PlayfairSC", "Playfair Display SC/PlayfairDisplaySC-Regular.ttf"), ("PlayfairSC-B", "Playfair Display SC/PlayfairDisplaySC-Bold.ttf"),
             ("Plex", "IBM Plex Sans Condensed/IBMPlexSansCondensed-Regular.ttf"), ("Plex-M", "IBM Plex Sans Condensed/IBMPlexSansCondensed-SemiBold.ttf")]:
    pdfmetrics.registerFont(TTFont(n, G + p))
pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))

DARK = colors.Color(0.17, 0.17, 0.17); MID = colors.Color(0.45, 0.45, 0.45); FROST = colors.Color(0.62, 0.62, 0.62)
ICE = colors.Color(0.9, 0.9, 0.9); PALE = colors.Color(0.955, 0.955, 0.955); INK = colors.Color(0.1, 0.1, 0.1); GRIDC = colors.Color(0.55, 0.55, 0.55)
LET = colors.Color(0.38, 0.38, 0.38)
P = lambda s: tuple(map(int, s.split(",")))

def snowflake(c, x, y, r, col, lw=0.09):
    c.saveState(); c.setStrokeColor(col); c.setLineWidth(r * lw); c.setLineCap(1)
    for i in range(6):
        a = math.pi / 3 * i; c.line(x, y, x + r * math.cos(a), y + r * math.sin(a))
        bx, by = x + r * 0.55 * math.cos(a), y + r * 0.55 * math.sin(a)
        for s in (-1, 1):
            b = a + s * math.pi / 4; c.line(bx, by, bx + r * 0.3 * math.cos(b), by + r * 0.3 * math.sin(b))
    c.restoreState()

# ---------------------------------------------------------------- icons
def star(c, x, y, r, fill=INK):
    p = c.beginPath()
    for i in range(10):
        a = math.pi / 2 + i * math.pi / 5; rr = r if i % 2 == 0 else r * 0.42
        (p.moveTo if i == 0 else p.lineTo)(x + rr * math.cos(a), y + rr * math.sin(a))
    p.close(); c.setFillColor(fill); c.drawPath(p, stroke=0, fill=1)

def pine(c, x, y, s):
    c.saveState(); c.setFillColor(DARK)
    for k, (w, yy) in enumerate([(0.62, -0.30), (0.48, -0.08), (0.34, 0.12)]):
        p = c.beginPath(); p.moveTo(x - w * s / 2, y + yy * s); p.lineTo(x + w * s / 2, y + yy * s); p.lineTo(x, y + (yy + 0.26) * s); p.close(); c.drawPath(p, stroke=0, fill=1)
    c.rect(x - 0.05 * s, y - 0.42 * s, 0.1 * s, 0.12 * s, stroke=0, fill=1); c.restoreState()

def snowman(c, x, y, s):
    c.saveState(); c.setStrokeColor(INK); c.setFillColor(colors.white); c.setLineWidth(max(0.7, s * 0.05))
    c.circle(x, y - 0.13 * s, 0.2 * s, stroke=1, fill=1); c.circle(x, y + 0.16 * s, 0.13 * s, stroke=1, fill=1)
    c.setFillColor(INK); c.rect(x - 0.1 * s, y + 0.27 * s, 0.2 * s, 0.03 * s, stroke=0, fill=1); c.rect(x - 0.065 * s, y + 0.29 * s, 0.13 * s, 0.1 * s, stroke=0, fill=1)
    c.restoreState()

def lantern(c, x, y, s):
    c.saveState(); c.setStrokeColor(INK); c.setLineWidth(max(0.6, s * 0.04)); c.setFillColor(ICE)
    c.roundRect(x - 0.15 * s, y - 0.2 * s, 0.3 * s, 0.36 * s, 0.05 * s, stroke=1, fill=1)
    c.line(x - 0.2 * s, y - 0.2 * s, x + 0.2 * s, y - 0.2 * s); c.line(x - 0.2 * s, y + 0.16 * s, x + 0.2 * s, y + 0.16 * s)
    c.arc(x - 0.08 * s, y + 0.12 * s, x + 0.08 * s, y + 0.3 * s, 0, 180)
    c.setFillColor(INK); c.circle(x, y - 0.02 * s, 0.05 * s, stroke=0, fill=1); c.restoreState()

def gift(c, x, y, s):
    c.saveState(); c.setStrokeColor(INK); c.setFillColor(ICE); c.setLineWidth(max(0.6, s * 0.04))
    c.rect(x - 0.22 * s, y - 0.24 * s, 0.44 * s, 0.34 * s, stroke=1, fill=1)
    c.setFillColor(INK); c.rect(x - 0.035 * s, y - 0.24 * s, 0.07 * s, 0.34 * s, stroke=0, fill=1)
    c.rect(x - 0.22 * s, y - 0.1 * s, 0.44 * s, 0.06 * s, stroke=0, fill=1)
    c.setFillColor(colors.white); c.ellipse(x - 0.18 * s, y + 0.08 * s, x, y + 0.24 * s, stroke=1, fill=0); c.ellipse(x, y + 0.08 * s, x + 0.18 * s, y + 0.24 * s, stroke=1, fill=0)
    c.restoreState()

def corner_letter(c, x, y, s, ch, col=LET):
    """small letter in the lower-right corner of a cell whose lower-left is (x, y)"""
    if not ch: return
    c.setFillColor(col); c.setFont("Plex-M", max(5.5, s * 0.26)); c.drawRightString(x + s - s * 0.1, y + s * 0.1, ch)

def num_badge(c, x, y, s, k):
    """numbered circle in the upper-left corner of a cell"""
    r = s * 0.17; cx, cy = x + r + s * 0.05, y + s - r - s * 0.05
    c.setFillColor(INK); c.circle(cx, cy, r, stroke=0, fill=1)
    c.setFillColor(colors.white); c.setFont("Plex-M", r * 1.35); c.drawCentredString(cx, cy - r * 0.45, str(k))

def grid_lines(c, x0, y0, n, m, s, lw=0.5, outer=1.3, col=GRIDC):
    c.setStrokeColor(col); c.setLineWidth(lw)
    for i in range(1, m): c.line(x0 + i * s, y0, x0 + i * s, y0 + n * s)
    for i in range(1, n): c.line(x0, y0 + i * s, x0 + m * s, y0 + i * s)
    c.setStrokeColor(DARK); c.setLineWidth(outer); c.rect(x0, y0, m * s, n * s)

def cell_xy(x0, y0, n, s, r, cc): return x0 + cc * s, y0 + (n - 1 - r) * s

def counts(c, x0, y0, n, s, rows, cols, fs=None):
    fs = fs or min(13, s * 0.45); c.setFillColor(INK); c.setFont("Plex-M", fs)
    for i in range(n):
        c.drawCentredString(x0 + i * s + s / 2, y0 + n * s + s * 0.22, str(cols[i]))
        c.drawCentredString(x0 + n * s + s * 0.45, y0 + (n - 1 - i) * s + s / 2 - fs * 0.35, str(rows[i]))

# ---------------------------------------------------------------- word search
def wordsearch(c, x, y, w, h, v, sol=False):
    g = v["grid"]; n = len(g); s = min(w / n, (h - (0 if sol else 1.3 * 72)) / n, 0.42 * 72)
    x0 = x + (w - n * s) / 2; y0 = y + h - n * s
    if sol:
        c.setStrokeColor(FROST); c.setLineCap(1)
        for word, cells in v["placed"].items():
            a, b = cells[0], cells[-1]
            ax, ay = cell_xy(x0, y0, n, s, *a); bx, by = cell_xy(x0, y0, n, s, *b)
            c.setLineWidth(s * 0.62); c.line(ax + s / 2, ay + s / 2, bx + s / 2, by + s / 2)
        c.setStrokeColor(INK); c.setLineWidth(0.9)
        for r, cc in v["leftover"]:
            cx, cy = cell_xy(x0, y0, n, s, r, cc); c.circle(cx + s / 2, cy + s / 2, s * 0.36)
    c.setStrokeColor(DARK); c.setLineWidth(1.2); c.rect(x0 - 4, y0 - 4, n * s + 8, n * s + 8)
    c.setFillColor(INK); c.setFont("Plex-M", s * 0.52)
    for r in range(n):
        for cc in range(n):
            cx, cy = cell_xy(x0, y0, n, s, r, cc); c.drawCentredString(cx + s / 2, cy + s * 0.3, g[r][cc])
    if sol: return
    words = v["words"]; cols = 3 if len(words) <= 12 else 4; per = math.ceil(len(words) / cols); cw = w / cols
    c.setFont("PlayfairSC", 10.5); c.setFillColor(DARK)
    for i, wd in enumerate(words):
        col, row = divmod(i, per)
        c.drawString(x + col * cw + 14, y0 - 30 - row * 15, wd.title()); c.setStrokeColor(MID); c.setLineWidth(0.6); c.rect(x + col * cw + 3, y0 - 30 - row * 15, 6.5, 6.5)

# ---------------------------------------------------------------- queens
def queens(c, x, y, w, h, v, sol=False):
    n = v["n"]; s = min(w / n, h / n, 0.62 * 72); x0 = x + (w - n * s) / 2; y0 = y + h - n * s; reg = v["regions"]
    shade = {}
    # alternate light shading per region to make the patchwork easy to see
    for g in range(n): shade[g] = PALE if g % 2 else colors.white
    for r in range(n):
        for cc in range(n):
            cx, cy = cell_xy(x0, y0, n, s, r, cc); c.setFillColor(shade[reg[r][cc]]); c.rect(cx, cy, s, s, stroke=0, fill=1)
    grid_lines(c, x0, y0, n, n, s, lw=0.4, col=FROST)
    c.setStrokeColor(INK); c.setLineWidth(2.0); c.setLineCap(2)
    for r in range(n):
        for cc in range(n):
            cx, cy = cell_xy(x0, y0, n, s, r, cc)
            if cc + 1 < n and reg[r][cc] != reg[r][cc + 1]: c.line(cx + s, cy, cx + s, cy + s)
            if r + 1 < n and reg[r][cc] != reg[r + 1][cc]: c.line(cx, cy, cx + s, cy)
    c.setLineWidth(2.2); c.rect(x0, y0, n * s, n * s)
    L = [row.split("|") for row in v["letters"]]
    for r in range(n):
        for cc in range(n):
            cx, cy = cell_xy(x0, y0, n, s, r, cc); corner_letter(c, cx, cy, s, L[r][cc])
    if sol:
        for r, cc in v["stars"]:
            cx, cy = cell_xy(x0, y0, n, s, r, cc); star(c, cx + s / 2, cy + s / 2 + s * 0.03, s * 0.32)

# ---------------------------------------------------------------- wordoku
def wordoku(c, x, y, w, h, v, sol=False):
    n, br, bc = v["n"], v["br"], v["bc"]; s = min(w / n, h / n, 0.62 * 72); x0 = x + (w - n * s) / 2; y0 = y + h - n * s
    giv = {P(k): ch for k, ch in v["givens"].items()}
    num = {tuple(x_): i + 1 for i, x_ in enumerate(v["shaded"])}
    for (r, cc), k in num.items():
        cx, cy = cell_xy(x0, y0, n, s, r, cc); c.setFillColor(ICE); c.rect(cx, cy, s, s, stroke=0, fill=1)
    grid_lines(c, x0, y0, n, n, s, lw=0.5)
    c.setStrokeColor(DARK); c.setLineWidth(1.6)
    for i in range(0, n + 1, bc): c.line(x0 + i * s, y0, x0 + i * s, y0 + n * s)
    for i in range(0, n + 1, br): c.line(x0, y0 + i * s, x0 + n * s, y0 + i * s)
    for r in range(n):
        for cc in range(n):
            cx, cy = cell_xy(x0, y0, n, s, r, cc)
            if (r, cc) in giv: c.setFillColor(INK); c.setFont("PlayfairSC-B", s * 0.52); c.drawCentredString(cx + s / 2, cy + s * 0.3, giv[(r, cc)])
            elif sol: c.setFillColor(MID); c.setFont("Crimson-I", s * 0.55); c.drawCentredString(cx + s / 2, cy + s * 0.3, v["full"][r][cc])
            if (r, cc) in num: num_badge(c, cx, cy, s, num[(r, cc)])

# ---------------------------------------------------------------- maze
def maze(c, x, y, w, h, v, sol=False):
    H, W = v["h"], v["w"]; s = min(w / W, h / H); x0 = x + (w - W * s) / 2; y0 = y + (h - H * s) / 2
    E = {frozenset(map(tuple, e)) for e in v["edges"]}
    X = lambda cc: x0 + cc * s; Y = lambda r: y0 + (H - r) * s
    if sol:
        c.setStrokeColor(FROST); c.setLineWidth(s * 0.36); c.setLineCap(1); c.setLineJoin(1)
        pa = c.beginPath(); pts = [(X(cc) + s / 2, Y(r) - s / 2) for r, cc in v["path"]]
        pa.moveTo(pts[0][0], pts[0][1] + s); [pa.lineTo(*p) for p in pts]; pa.lineTo(pts[-1][0], pts[-1][1] - s); c.drawPath(pa, stroke=1, fill=0)
    c.setStrokeColor(INK); c.setLineWidth(1.6); c.setLineCap(1)
    for r in range(H):
        for cc in range(W):
            if cc + 1 < W and frozenset([(r, cc), (r, cc + 1)]) not in E: c.line(X(cc + 1), Y(r), X(cc + 1), Y(r + 1))
            if r + 1 < H and frozenset([(r, cc), (r + 1, cc)]) not in E: c.line(X(cc), Y(r + 1), X(cc + 1), Y(r + 1))
    c.setLineWidth(2.2)
    c.line(X(1), Y(0), X(W), Y(0)); c.line(X(0), Y(H), X(W - 1), Y(H)); c.line(X(0), Y(0), X(0), Y(H)); c.line(X(W), Y(0), X(W), Y(H))
    c.setFont("PlayfairSC", 8); c.setFillColor(MID)
    c.drawCentredString(X(0) + s / 2, Y(0) + 6, "IN"); c.drawCentredString(X(W - 1) + s / 2, Y(H) - 12, "OUT")
    c.setFont("PlayfairSC-B", s * 0.5); c.setFillColor(INK)
    for k, ch in v["letters"].items():
        r, cc = P(k); c.drawCentredString(X(cc) + s / 2, Y(r) - s / 2 - s * 0.18, ch)

# ---------------------------------------------------------------- nonogram
def nonogram(c, x, y, w, h, v, sol=False):
    R, C = v["rows"], v["cols"]; n, m = len(R), len(C)
    mr = max(len(r) for r in R); mc = max(len(q) for q in C)
    s = min(w / (m + mr * 0.62 + 0.3), h / (n + mc * 0.7 + 0.3), 0.3 * 72)
    gw = m * s; x0 = x + (w - gw - mr * 0.62 * s) / 2 + mr * 0.62 * s; y0 = y + (h - n * s - mc * 0.7 * s) / 2
    if sol:
        c.setFillColor(DARK)
        for r, row in enumerate(v["picture"]):
            for cc, ch in enumerate(row):
                if ch == "#": cx, cy = cell_xy(x0, y0, n, s, r, cc); c.rect(cx, cy, s, s, stroke=0, fill=1)
    grid_lines(c, x0, y0, n, m, s, lw=0.4)
    c.setStrokeColor(DARK); c.setLineWidth(1.1)
    for i in range(5, m, 5): c.line(x0 + i * s, y0, x0 + i * s, y0 + n * s)
    for i in range(5, n, 5): c.line(x0, y0 + i * s, x0 + m * s, y0 + i * s)
    fs = s * 0.52; c.setFont("Plex-M", fs); c.setFillColor(INK)
    for r, cl in enumerate(R):
        yy = y0 + (n - 1 - r) * s + s / 2 - fs * 0.35
        for j, k in enumerate(reversed(cl)): c.drawCentredString(x0 - s * 0.36 - j * s * 0.62, yy, str(k))
    for cc, cl in enumerate(C):
        for j, k in enumerate(reversed(cl)): c.drawCentredString(x0 + cc * s + s / 2, y0 + n * s + s * 0.25 + j * s * 0.7, str(k))
    for i in range(0, n, 2):
        c.setFillColor(PALE); c.rect(x0 - mr * 0.62 * s, y0 + (n - 1 - i) * s, mr * 0.62 * s - 2, s, stroke=0, fill=1) if False else None

# ---------------------------------------------------------------- pyramid
def pyramid(c, x, y, w, h, v, sol=False):
    n = v["n"]; V = v["values"]; giv = {P(k): val for k, val in v["givens"].items()}
    bw = min(w / n, 0.95 * 72); bh = bw * 0.62; tot = n * bh
    y0 = y + (h - tot - bh * 1.6) / 2 + bh * 1.6
    for r in range(n):
        for i in range(n - r):
            bx = x + (w - (n - r) * bw) / 2 + i * bw; by = y0 + r * bh
            c.setStrokeColor(DARK); c.setLineWidth(1.2); c.setFillColor(ICE if (r, i) in giv else colors.white)
            c.roundRect(bx + 1.5, by + 1.5, bw - 3, bh - 3, bh * 0.35, stroke=1, fill=1)
            if (r, i) in giv or sol:
                c.setFillColor(INK if (r, i) in giv else MID); c.setFont("Plex-M" if (r, i) in giv else "Crimson-I", bh * 0.42)
                c.drawCentredString(bx + bw / 2, by + bh * 0.34, str(V[r][i]))
    # letter boxes under the base
    for i in range(n):
        bx = x + (w - n * bw) / 2 + i * bw + bw * 0.25
        c.setStrokeColor(DARK); c.setLineWidth(1); c.rect(bx, y0 - bh * 1.35, bw * 0.5, bw * 0.5)
        c.setFont("Plex", 7); c.setFillColor(MID); c.drawCentredString(bx + bw * 0.25, y0 - bh * 1.35 - 9, "letter")
        if sol: c.setFont("PlayfairSC-B", bw * 0.3); c.setFillColor(INK); c.drawCentredString(bx + bw * 0.25, y0 - bh * 1.35 + bw * 0.14, chr(64 + V[0][i]))
        c.setStrokeColor(FROST); c.setLineWidth(0.6); c.setDash(2, 2); c.line(bx + bw * 0.25, y0 - bh * 1.35 + bw * 0.5 + 2, bx + bw * 0.25, y0 - 2); c.setDash()

# ---------------------------------------------------------------- ciphers
def pigpen_sym(c, cx, cy, s, ch):
    i = ord(ch) - 65; c.setStrokeColor(INK); c.setLineWidth(max(1.0, s * 0.08)); c.setLineCap(1); c.setLineJoin(1); h = s * 0.36
    if i < 18:
        dot = i >= 9; r, q = divmod(i % 9, 3)
        if r > 0: c.line(cx - h, cy + h, cx + h, cy + h)
        if r < 2: c.line(cx - h, cy - h, cx + h, cy - h)
        if q > 0: c.line(cx - h, cy - h, cx - h, cy + h)
        if q < 2: c.line(cx + h, cy - h, cx + h, cy + h)
    else:
        j = i - 18; dot = j >= 4; k = j % 4      # S/W top, T/X left, U/Y right, V/Z bottom
        a = {0: [(-1, 1), (1, 1)], 1: [(-1, 1), (-1, -1)], 2: [(1, 1), (1, -1)], 3: [(-1, -1), (1, -1)]}[k]
        # a chevron whose point is the centre of the X and whose arms point into the letter's quarter
        ox, oy = {0: (0, -0.45), 1: (0.45, 0), 2: (-0.45, 0), 3: (0, 0.45)}[k]
        px, py = cx + ox * h, cy + oy * h
        p = c.beginPath(); p.moveTo(px + a[0][0] * h, py + a[0][1] * h * (0.9 if k in (0, 3) else 1)); p.lineTo(px, py); p.lineTo(px + a[1][0] * h, py + a[1][1] * h * (0.9 if k in (0, 3) else 1)); c.drawPath(p, stroke=1, fill=0)
    if dot:
        c.setFillColor(INK)
        if i < 18: c.circle(cx, cy, s * 0.07, stroke=0, fill=1)
        else:
            k = (i - 18) % 4; ox, oy = {0: (0, 0.35), 1: (-0.35, 0), 2: (0.35, 0), 3: (0, -0.35)}[k]
            c.circle(cx + ox * h, cy + oy * h, s * 0.07, stroke=0, fill=1)

def pigpen_key(c, x, y, s):
    """draws the four key figures starting at (x, y) top-left; returns width"""
    c.setStrokeColor(INK); c.setLineWidth(1.1); c.setFont("PlayfairSC-B", s * 0.42); gap = s * 0.55; X = x
    for dot, base in ((False, 0), (True, 9)):
        c.line(X + s, y, X + s, y - 3 * s); c.line(X + 2 * s, y, X + 2 * s, y - 3 * s)
        c.line(X, y - s, X + 3 * s, y - s); c.line(X, y - 2 * s, X + 3 * s, y - 2 * s)
        for k in range(9):
            r, q = divmod(k, 3); cx, cy = X + q * s + s / 2, y - r * s - s / 2
            c.setFillColor(INK); c.drawCentredString(cx - (s * 0.18 if dot else 0), cy - s * 0.15, chr(65 + base + k))
            if dot: c.circle(cx + s * 0.22, cy, s * 0.06, stroke=0, fill=1)
        X += 3 * s + gap
    for dot, base in ((False, 18), (True, 22)):
        d = 1.5 * s; cx, cy = X + d, y - 1.5 * s
        c.line(cx - d * 0.8, cy + d * 0.8, cx + d * 0.8, cy - d * 0.8); c.line(cx - d * 0.8, cy - d * 0.8, cx + d * 0.8, cy + d * 0.8)
        for k, (ox, oy) in enumerate([(0, 0.5), (-0.5, 0), (0.5, 0), (0, -0.5)]):
            c.setFillColor(INK); c.drawCentredString(cx + ox * d - (s * 0.12 if dot else 0), cy + oy * d - s * 0.15, chr(65 + base + k))
            if dot: c.circle(cx + ox * d + s * 0.2, cy + oy * d, s * 0.06, stroke=0, fill=1)
        X += 2 * d * 0.85 + gap
    return X - x

def message_rows(text, per):
    words = text.split(); rows = [[]]; L = 0
    for wd in words:
        if L + len(wd) > per and rows[-1]: rows.append([]); L = 0
        rows[-1].append(wd); L += len(wd) + 1
    return rows

def pigpen(c, x, y, w, h, v, sol=False):
    ks = 0.3 * 72
    kw = pigpen_key(c, 0, 0, ks) if False else None
    # key centred
    c.saveState(); c.translate(0, 0)
    kx = x + (w - 2 * (3 * ks + ks * 0.55) - 2 * (3 * ks * 0.85 + ks * 0.55) + ks * 0.55) / 2
    pigpen_key(c, kx, y + h, ks); c.restoreState()
    c.setFont("PlayfairSC", 9); c.setFillColor(MID); c.drawCentredString(x + w / 2, y + h - 3 * ks - 16, "The key")
    s = 0.34 * 72; per = int(w / s) - 1
    rows = message_rows("".join(ch for ch in v["plain"] if ch.isalpha() or ch == " "), per)
    yy = y + h - 3 * ks - 52
    for row in rows:
        n = sum(len(wd) for wd in row) + len(row) - 1; xx = x + (w - n * s) / 2
        for wd in row:
            for ch in wd:
                pigpen_sym(c, xx + s / 2, yy, s * 0.8, ch)
                c.setStrokeColor(FROST); c.setLineWidth(0.7); c.line(xx + s * 0.12, yy - s * 0.95, xx + s * 0.88, yy - s * 0.95)
                if sol: c.setFont("PlayfairSC-B", s * 0.45); c.setFillColor(MID); c.drawCentredString(xx + s / 2, yy - s * 0.88, ch)
                xx += s
            xx += s
        yy -= s * 1.85

def caesar(c, x, y, w, h, v, sol=False):
    txt = v["plain"] if sol else v["cipher"]
    s = 0.3 * 72; per = int(w / s) - 1
    rows = message_rows(txt, per); yy = y + h - 14
    for row in rows:
        line = " ".join(row); n = len(line); xx = x + (w - n * s) / 2
        for ch in line:
            if ch != " ":
                c.setFont("Plex-M", s * 0.62); c.setFillColor(INK); c.drawCentredString(xx + s / 2, yy, ch)
                if ch.isalpha():
                    c.setStrokeColor(FROST); c.setLineWidth(0.7); c.line(xx + s * 0.12, yy - s * 0.95, xx + s * 0.88, yy - s * 0.95)
                    if sol: c.setFont("Crimson-I", s * 0.62); c.setFillColor(MID); c.drawCentredString(xx + s / 2, yy - s * 0.85, ch)
            xx += s
        yy -= s * 2.1
    # alphabet strip, in two rows of 13 so it stays inside the margins
    a = 0.3 * 72; ax = x + (w - 13 * a) / 2; ay = y + 30
    c.setFont("PlayfairSC", 8.5); c.setFillColor(MID); c.drawCentredString(x + w / 2, ay + a * 4.3 + 10, "Alphabet strip (write the shifted letters underneath if it helps)")
    for i in range(26):
        col = i % 13; by = ay + (a * 2.3 if i < 13 else 0); bx = ax + col * a
        c.setStrokeColor(GRIDC); c.setLineWidth(0.5); c.rect(bx, by + a, a, a); c.rect(bx, by, a, a)
        c.setFont("Plex-M", a * 0.5); c.setFillColor(INK); c.drawCentredString(bx + a / 2, by + a * 1.3, chr(65 + i))
        if sol: c.setFont("Crimson-I", a * 0.6); c.setFillColor(MID); c.drawCentredString(bx + a / 2, by + a * 0.28, chr(65 + (i - v["shift"]) % 26))

MORSE = {"A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---",
         "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
         "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--", "Z": "--.."}
def morse_glyphs(c, x, y, code, u):
    for sym in code:
        if sym == ".": c.circle(x + u * 0.5, y, u * 0.28, stroke=0, fill=1); x += u * 1.1
        else: c.roundRect(x, y - u * 0.22, u * 2.1, u * 0.44, u * 0.2, stroke=0, fill=1); x += u * 2.6
    return x

def morse(c, x, y, w, h, v, sol=False):
    u = 4.2; c.setFillColor(INK)
    words = [wd for wd in "".join(ch for ch in v["plain"] if ch.isalpha() or ch == " ").split()]
    yy = y + h - 10; lh = 40
    # message: one word per line, letters separated by space, underline for each letter
    for wd in words:
        widths = [sum(u * 1.1 if s_ == "." else u * 2.6 for s_ in MORSE[ch]) for ch in wd]
        tot = sum(widths) + (len(wd) - 1) * u * 3.4 + u * 6
        xx = x + (w - tot) / 2
        for ch, wd_ in zip(wd, widths):
            c.setFillColor(INK); morse_glyphs(c, xx, yy, MORSE[ch], u)
            c.setStrokeColor(FROST); c.setLineWidth(0.7); c.line(xx, yy - 17, xx + max(wd_, 12), yy - 17)
            if sol: c.setFont("PlayfairSC-B", 10); c.setFillColor(MID); c.drawCentredString(xx + max(wd_, 12) / 2, yy - 15, ch)
            xx += wd_ + u * 3.4
        c.setFont("Plex-M", 12); c.setFillColor(MID); c.drawString(xx, yy - 4, "/")
        yy -= lh
    # table
    ty = y + 4 * 20 + 18; c.setFont("PlayfairSC", 9); c.setFillColor(MID); c.drawCentredString(x + w / 2, ty + 12, "Morse table")
    cw = w / 4
    for i, ch in enumerate(sorted(MORSE)):
        col, row = i % 4, i // 4
        tx = x + col * cw + 8; tyy = ty - row * 13
        c.setFont("PlayfairSC-B", 9); c.setFillColor(INK); c.drawString(tx, tyy - 3, ch); morse_glyphs(c, tx + 14, tyy, MORSE[ch], 3.2)

# ---------------------------------------------------------------- tents / akari / presents / fleet
def letter_grid(c, x0, y0, n, s, v, skip=()):
    L = [row.split("|") for row in v["letters"]]
    for r in range(n):
        for cc in range(n):
            if (r, cc) in skip: continue
            cx, cy = cell_xy(x0, y0, n, s, r, cc); corner_letter(c, cx, cy, s, L[r][cc])

def tents(c, x, y, w, h, v, sol=False):
    n = v["n"]; s = min(w / (n + 1), h / (n + 1), 0.55 * 72); x0 = x + (w - (n + 0.8) * s) / 2; y0 = y + (h - (n + 0.8) * s) / 2
    grid_lines(c, x0, y0, n, n, s); counts(c, x0, y0, n, s, v["rows"], v["cols"])
    trees = {tuple(t) for t in v["trees"]}
    for r, cc in trees: cx, cy = cell_xy(x0, y0, n, s, r, cc); pine(c, cx + s / 2, cy + s / 2, s * 0.95)
    letter_grid(c, x0, y0, n, s, v, skip=trees)
    if sol:
        for r, cc in v["tents"]: cx, cy = cell_xy(x0, y0, n, s, r, cc); snowman(c, cx + s * 0.45, cy + s * 0.5, s * 0.9)

def akari(c, x, y, w, h, v, sol=False):
    n = v["n"]; s = min(w / n, h / n, 0.62 * 72); x0 = x + (w - n * s) / 2; y0 = y + h - n * s
    black = {tuple(b) for b in v["black"]}; nums = {P(k): k2 for k, k2 in v["nums"].items()}
    if sol:
        lit = set()
        for b in v["bulbs"]:
            b = tuple(b); lit.add(b)
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                r, cc = b
                while True:
                    r += dr; cc += dc
                    if not (0 <= r < n and 0 <= cc < n) or (r, cc) in black: break
                    lit.add((r, cc))
        for r, cc in lit: cx, cy = cell_xy(x0, y0, n, s, r, cc); c.setFillColor(PALE); c.rect(cx, cy, s, s, stroke=0, fill=1)
    grid_lines(c, x0, y0, n, n, s)
    for r, cc in black:
        cx, cy = cell_xy(x0, y0, n, s, r, cc); c.setFillColor(DARK); c.rect(cx, cy, s, s, stroke=0, fill=1)
        if (r, cc) in nums: c.setFillColor(colors.white); c.setFont("Plex-M", s * 0.5); c.drawCentredString(cx + s / 2, cy + s * 0.32, str(nums[(r, cc)]))
    letter_grid(c, x0, y0, n, s, v, skip=black)
    if sol:
        for r, cc in v["bulbs"]: cx, cy = cell_xy(x0, y0, n, s, r, cc); lantern(c, cx + s * 0.45, cy + s * 0.52, s * 0.95)

def presents(c, x, y, w, h, v, sol=False):
    n = v["n"]; s = min(w / n, h / n, 0.62 * 72); x0 = x + (w - n * s) / 2; y0 = y + h - n * s
    clues = {P(k): k2 for k, k2 in v["clues"].items()}
    for (r, cc) in clues: cx, cy = cell_xy(x0, y0, n, s, r, cc); c.setFillColor(ICE); c.rect(cx, cy, s, s, stroke=0, fill=1)
    grid_lines(c, x0, y0, n, n, s)
    for (r, cc), k in clues.items():
        cx, cy = cell_xy(x0, y0, n, s, r, cc); c.setFillColor(INK); c.setFont("Plex-M", s * 0.5); c.drawCentredString(cx + s / 2, cy + s * 0.32, str(k))
    letter_grid(c, x0, y0, n, s, v, skip=set(clues))
    if sol:
        for r, cc in v["presents"]: cx, cy = cell_xy(x0, y0, n, s, r, cc); gift(c, cx + s * 0.45, cy + s * 0.52, s * 0.95)

def fleet(c, x, y, w, h, v, sol=False):
    n = v["n"]; s = min(w / (n + 1), h / (n + 1), 0.58 * 72); x0 = x + (w - (n + 0.8) * s) / 2; y0 = y + h - (n + 0.8) * s
    grid_lines(c, x0, y0, n, n, s); counts(c, x0, y0, n, s, v["rows"], v["cols"])
    shipc = {tuple(x_) for x_ in v["cells"]}
    def seg(r, cc, col=DARK):
        cx, cy = cell_xy(x0, y0, n, s, r, cc); m = s * 0.14
        l = (r, cc - 1) in shipc; rr = (r, cc + 1) in shipc; u = (r - 1, cc) in shipc; d = (r + 1, cc) in shipc
        x1 = cx + (0 if l else m); x2 = cx + s - (0 if rr else m); y1 = cy + (0 if d else m); y2 = cy + s - (0 if u else m)
        c.setFillColor(col); c.roundRect(x1, y1, x2 - x1, y2 - y1, s * 0.12 if not (l or rr or u or d) else s * 0.05, stroke=0, fill=1)
    def wave(r, cc):
        cx, cy = cell_xy(x0, y0, n, s, r, cc); c.setStrokeColor(MID); c.setLineWidth(1)
        for k in (0.4, 0.6):
            p = c.beginPath(); p.moveTo(cx + s * 0.2, cy + s * k)
            p.curveTo(cx + s * 0.35, cy + s * (k + 0.1), cx + s * 0.45, cy + s * (k - 0.1), cx + s * 0.6, cy + s * k)
            p.curveTo(cx + s * 0.7, cy + s * (k + 0.1), cx + s * 0.75, cy + s * (k - 0.05), cx + s * 0.8, cy + s * k); c.drawPath(p, stroke=1, fill=0)
    if sol:
        for r, cc in shipc: seg(r, cc, Color(0.8, 0.8, 0.8))
    else:
        for r, cc in v["given_ship"]:
            cx, cy = cell_xy(x0, y0, n, s, r, cc); c.setFillColor(FROST); c.circle(cx + s / 2, cy + s / 2, s * 0.3, stroke=0, fill=1)
    for r, cc in v["given_sea"]: wave(r, cc)
    letter_grid(c, x0, y0, n, s, v)
    # the fleet legend
    ly = y0 - s * 1.0; lx = x0; u = s * 0.45
    c.setFont("PlayfairSC", 9); c.setFillColor(MID); c.drawString(lx, ly, "The fleet:")
    lx += 52
    for L in v["fleet"]:
        for k in range(L):
            c.setFillColor(DARK); c.roundRect(lx + k * u, ly - 2, u - 1.5, u * 0.8, 1.5, stroke=0, fill=1)
        lx += L * u + 10

# ---------------------------------------------------------------- latin puzzles
def key_table(c, x, y, w, keymap):
    c.setFont("PlayfairSC", 9); c.setFillColor(MID); c.drawCentredString(x + w / 2, y + 26, "Key")
    s = 26; x0 = x + (w - 5 * s) / 2
    for i in range(5):
        c.setStrokeColor(GRIDC); c.setLineWidth(0.6); c.rect(x0 + i * s, y, s, s); c.rect(x0 + i * s, y - s, s, s)
        c.setFont("Plex-M", 11); c.setFillColor(INK); c.drawCentredString(x0 + i * s + s / 2, y + 8, str(i + 1))
        c.setFont("PlayfairSC-B", 12); c.drawCentredString(x0 + i * s + s / 2, y - s + 8, keymap[str(i + 1)])

def latin_base(c, x0, y0, s, v, sol, badge=True):
    n = 5; giv = {P(k): val for k, val in v.get("givens", {}).items()}
    num = {tuple(x_): i + 1 for i, x_ in enumerate(v["numbered"])}
    for (r, cc) in num: cx, cy = cell_xy(x0, y0, n, s, r, cc); c.setFillColor(PALE); c.rect(cx, cy, s, s, stroke=0, fill=1)
    for r in range(n):
        for cc in range(n):
            cx, cy = cell_xy(x0, y0, n, s, r, cc)
            if (r, cc) in giv: c.setFillColor(INK); c.setFont("Plex-M", s * 0.5); c.drawCentredString(cx + s / 2, cy + s * 0.32, str(giv[(r, cc)]))
            elif sol: c.setFillColor(MID); c.setFont("Crimson-I", s * 0.55); c.drawCentredString(cx + s / 2, cy + s * 0.3, str(v["solution"][r][cc]))
            if (r, cc) in num and badge: num_badge(c, cx, cy, s, num[(r, cc)])

def futoshiki(c, x, y, w, h, v, sol=False):
    n = 5; s = min(w / 7, (h - 70) / 7, 0.6 * 72); g = s * 0.55; tot = n * s + (n - 1) * g
    x0 = x + (w - tot) / 2; ytop = y + h
    def pos(r, cc): return x0 + cc * (s + g), ytop - (r + 1) * s - r * g
    giv = {P(k): val for k, val in v.get("givens", {}).items()}; num = {tuple(x_): i + 1 for i, x_ in enumerate(v["numbered"])}
    for r in range(n):
        for cc in range(n):
            px, py = pos(r, cc)
            c.setFillColor(PALE if (r, cc) in num else colors.white); c.setStrokeColor(DARK); c.setLineWidth(1.2); c.rect(px, py, s, s, stroke=1, fill=1)
            if (r, cc) in giv: c.setFillColor(INK); c.setFont("Plex-M", s * 0.5); c.drawCentredString(px + s / 2, py + s * 0.32, str(giv[(r, cc)]))
            elif sol: c.setFillColor(MID); c.setFont("Crimson-I", s * 0.55); c.drawCentredString(px + s / 2, py + s * 0.3, str(v["solution"][r][cc]))
            if (r, cc) in num: num_badge(c, px, py, s, num[(r, cc)])
    c.setFillColor(INK); c.setFont("Plex-M", g * 0.95)
    for a, b in v["ineq"]:
        (ra, ca), (rb, cb) = a, b     # a < b
        if ra == rb:
            px, py = pos(ra, min(ca, cb)); sym = "<" if ca < cb else ">"
            c.drawCentredString(px + s + g / 2, py + s / 2 - g * 0.33, sym)
        else:
            px, py = pos(min(ra, rb), ca); sym = "∧" if ra < rb else "∨"
            c.setFont("DejaVu", g * 0.95); c.drawCentredString(px + s / 2, py - g / 2 - g * 0.33, sym); c.setFont("Plex-M", g * 0.95)
    if not sol: key_table(c, x, y + 30, w, v["keymap"])

def skyscrapers(c, x, y, w, h, v, sol=False):
    n = 5; s = min(w / 7.2, (h - 80) / 7.2, 0.6 * 72); x0 = x + (w - n * s) / 2; y0 = y + h - (n + 1) * s
    latin_base(c, x0, y0, s, v, sol); grid_lines(c, x0, y0, n, n, s, lw=0.7)
    c.setFont("Plex-M", s * 0.48); c.setFillColor(INK)
    for k, val in v["clues"].items():
        side, i = k.split(","); i = int(i)
        if side == "top": px, py = x0 + i * s + s / 2, y0 + n * s + s * 0.3
        elif side == "bottom": px, py = x0 + i * s + s / 2, y0 - s * 0.6
        elif side == "left": px, py = x0 - s * 0.5, y0 + (n - 1 - i) * s + s * 0.32
        else: px, py = x0 + n * s + s * 0.5, y0 + (n - 1 - i) * s + s * 0.32
        c.drawCentredString(px, py, str(val))
    if not sol: key_table(c, x, y + 30, w, v["keymap"])

def calcudoku(c, x, y, w, h, v, sol=False):
    n = 5; s = min(w / 6, (h - 80) / 6, 0.7 * 72); x0 = x + (w - n * s) / 2; y0 = y + h - n * s - 4
    cage = {}
    for i, cg in enumerate(v["cages"]):
        for a in cg["cells"]: cage[tuple(a)] = i
    latin_base(c, x0, y0, s, v, sol, badge=False)
    grid_lines(c, x0, y0, n, n, s, lw=0.4, col=FROST)
    c.setStrokeColor(INK); c.setLineWidth(2); c.setLineCap(2)
    for r in range(n):
        for cc in range(n):
            cx, cy = cell_xy(x0, y0, n, s, r, cc)
            if cc + 1 < n and cage[(r, cc)] != cage[(r, cc + 1)]: c.line(cx + s, cy, cx + s, cy + s)
            if r + 1 < n and cage[(r, cc)] != cage[(r + 1, cc)]: c.line(cx, cy, cx + s, cy)
    c.rect(x0, y0, n * s, n * s)
    for cg in v["cages"]:
        r, cc = min(tuple(a) for a in cg["cells"]); cx, cy = cell_xy(x0, y0, n, s, r, cc)
        c.setFillColor(INK); c.setFont("Plex-M", s * 0.22); c.drawString(cx + s * 0.08, cy + s * 0.74, f"{cg['target']}{cg['op']}")
    num = {tuple(x_): i + 1 for i, x_ in enumerate(v["numbered"])}
    for (r, cc), k in num.items():
        cx, cy = cell_xy(x0, y0, n, s, r, cc); rr = s * 0.13; bx, by = cx + s - rr - s * 0.06, cy + rr + s * 0.06
        c.setFillColor(INK); c.circle(bx, by, rr, stroke=0, fill=1); c.setFillColor(colors.white); c.setFont("Plex-M", rr * 1.35); c.drawCentredString(bx, by - rr * 0.45, str(k))
    if not sol: key_table(c, x, y + 30, w, v["keymap"])

# ---------------------------------------------------------------- fill-in
def fillin(c, x, y, w, h, v, sol=False):
    n = v["n"]; g = {}
    for sl in v["slots"]:
        for a, ch in zip(sl["cells"], sl["word"]): g[tuple(a)] = ch
    rs = [a for a, _ in g]; cs = [b for _, b in g]; r0, r1, c0, c1 = min(rs), max(rs), min(cs), max(cs)
    H, W = r1 - r0 + 1, c1 - c0 + 1
    s = min(w / W, (h - (0 if sol else 95)) / H, 0.4 * 72); x0 = x + (w - W * s) / 2; ytop = y + h
    num = {tuple(x_): i + 1 for i, x_ in enumerate(v["numbered"])}
    for (r, cc), ch in g.items():
        px, py = x0 + (cc - c0) * s, ytop - (r - r0 + 1) * s
        c.setFillColor(PALE if (r, cc) in num else colors.white); c.setStrokeColor(DARK); c.setLineWidth(1); c.rect(px, py, s, s, stroke=1, fill=1)
        if sol: c.setFillColor(MID); c.setFont("Crimson-I", s * 0.6); c.drawCentredString(px + s / 2, py + s * 0.28, ch)
        if (r, cc) in num: num_badge(c, px, py, s, num[(r, cc)])
    if sol: return
    by_len = {}
    for wd in v["words"]: by_len.setdefault(len(wd), []).append(wd)
    yy = ytop - H * s - 22; c.setFont("PlayfairSC", 9); cols = sorted(by_len); cw = w / len(cols)
    for i, L in enumerate(cols):
        c.setFillColor(MID); c.drawString(x + i * cw + 4, yy, f"{L} letters")
        for j, wd in enumerate(sorted(by_len[L])):
            c.setFillColor(INK); c.setFont("PlayfairSC-B", 9.5); c.drawString(x + i * cw + 4, yy - 14 - j * 13, wd.title()); c.setFont("PlayfairSC", 9)

# ---------------------------------------------------------------- logic grid
NAMES = ["Sam", "Kit", "Ada", "Tom", "Eve"]
TOPS = ["marshmallows", "cinnamon", "whipped cream", "peppermint", "nutmeg"]
KNITS = ["scarf", "mittens", "bobble hat", "socks", "jumper"]
def desc(cat, v):
    return {"top": f"the guest with {TOPS[v]} on their cocoa", "knit": f"the guest who knitted the {KNITS[v]}"}[cat]
def logic_clue(cl):
    t = cl[0]
    if t == "is": return f"{NAMES[cl[1]]} " + (f"has {TOPS[cl[3]]} on their cocoa." if cl[2] == "top" else f"knitted the {KNITS[cl[3]]}.")
    if t == "not":
        if cl[2] == "room": return f"{NAMES[cl[1]]} is not in Room {cl[3] + 1}."
        return f"{NAMES[cl[1]]} " + (f"does not have {TOPS[cl[3]]}." if cl[2] == "top" else f"did not knit the {KNITS[cl[3]]}.")
    a, b = desc(cl[1], cl[2]), desc(cl[3], cl[4])
    if t == "same": return (a[0].upper() + a[1:]) + (f" knitted the {KNITS[cl[4]]}." if cl[3] == "knit" else f" has {TOPS[cl[4]]}.")
    if t == "diff": return (a[0].upper() + a[1:]) + (f" did not knit the {KNITS[cl[4]]}." if cl[3] == "knit" else f" does not have {TOPS[cl[4]]}.")
    if t == "left": return (a[0].upper() + a[1:]) + f" is in a room somewhere to the left of {b}."
    if t == "rightnext": return (b[0].upper() + b[1:]) + f" is in the room directly to the right of {a}."
    if t == "next": return (a[0].upper() + a[1:]) + f" and {b} are in neighbouring rooms."

def logic(c, x, y, w, h, v, sol=False, clue_h=None):
    """chart only: rows = guests, columns = rooms | toppings | knits"""
    s = min((w - 70) / 15, 0.235 * 72); x0 = x + w - 15 * s - 2; hh = 58; y0 = y + h - hh - 5 * s
    heads = [f"Room {i + 1}" for i in range(5)] + ["marshm.", "cinnamon", "cream", "pepperm.", "nutmeg"] + ["scarf", "mittens", "hat", "socks", "jumper"]
    c.setFont("Plex", 7.2); c.setFillColor(INK)
    for i, t in enumerate(heads):
        c.saveState(); c.translate(x0 + i * s + s * 0.62, y0 + 5 * s + 4); c.rotate(70); c.drawString(0, 0, t); c.restoreState()
    for r, nm in enumerate(NAMES):
        c.setFont("PlayfairSC-B", 9.5); c.drawRightString(x0 - 5, y0 + (4 - r) * s + s * 0.3, nm)
    grid_lines(c, x0, y0, 5, 15, s, lw=0.4)
    c.setStrokeColor(DARK); c.setLineWidth(1.3)
    for k in (5, 10): c.line(x0 + k * s, y0, x0 + k * s, y0 + 5 * s)
    if sol:
        for g in range(5):
            for k, off in ((v["room"][g], 0), (v["top"][g], 5), (v["knit"][g], 10)):
                c.setFillColor(INK); c.circle(x0 + (off + k) * s + s / 2, y0 + (4 - g) * s + s / 2, s * 0.28, stroke=0, fill=1)
    return y0

# ---------------------------------------------------------------- Train Tracks (drawing code reused from Frostwood Express)
DV = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}

def draw_rails(c, cx, cy, s, piece, rail=DARK, tie=colors.Color(.6, .6, .6)):
    """A railway piece (two rails + sleepers) centred at (cx, cy) in a cell of size s."""
    d1, d2 = piece[0], piece[1]
    g = 0.17 * s; tl = 0.31 * s
    c.saveState(); c.setLineCap(0)
    if set(piece) in ({"N", "S"}, {"E", "W"}):
        vx, vy = DV[d1] if d1 in "NS" else (1, 0)
        if set(piece) == {"N", "S"}: vx, vy = 0, 1
        px, py = -vy, vx
        c.setStrokeColor(tie); c.setLineWidth(0.085 * s)
        for k in (-1, 0, 1):
            t = k * s / 3; c.line(cx + vx * t - px * tl, cy + vy * t - py * tl, cx + vx * t + px * tl, cy + vy * t + py * tl)
        c.setStrokeColor(rail); c.setLineWidth(0.05 * s)
        for o in (-g, g):
            c.line(cx - vx * s / 2 + px * o, cy - vy * s / 2 + py * o, cx + vx * s / 2 + px * o, cy + vy * s / 2 + py * o)
    else:
        a1, a2 = DV[d1], DV[d2]
        kx, ky = cx + (a1[0] + a2[0]) * s / 2, cy + (a1[1] + a2[1]) * s / 2       # corner of the cell
        t1 = math.degrees(math.atan2(-a1[1], -a1[0])); t2 = math.degrees(math.atan2(-a2[1], -a2[0]))
        ext = ((t2 - t1 + 180) % 360) - 180
        c.setStrokeColor(tie); c.setLineWidth(0.085 * s)
        for k in range(3):
            th = math.radians(t1 + ext * (k + 0.5) / 3)
            c.line(kx + (s / 2 - tl) * math.cos(th), ky + (s / 2 - tl) * math.sin(th), kx + (s / 2 + tl) * math.cos(th), ky + (s / 2 + tl) * math.sin(th))
        c.setStrokeColor(rail); c.setLineWidth(0.05 * s)
        for rr in (s / 2 - g, s / 2 + g):
            c.arc(kx - rr, ky - rr, kx + rr, ky + rr, t1, ext)
    c.restoreState()

def pieces_of(p):
    n = p["n"]; path = [tuple(x) for x in p["solution"]]; out = {}
    D4 = {(-1, 0): "N", (1, 0): "S", (0, -1): "W", (0, 1): "E"}
    for i, (r, c) in enumerate(path):
        ds = ["W"] if i == 0 else [D4[(path[i - 1][0] - r, path[i - 1][1] - c)]]
        ds.append("S" if i == len(path) - 1 else D4[(path[i + 1][0] - r, path[i + 1][1] - c)])
        out[(r, c)] = "".join(ds)
    return out

def draw_grid(c, x0, y0, s, p, mode="puzzle", edges=None, xs=(), labels=True, fs=None):
    """(x0, y0) = lower-left corner of the grid. mode: puzzle | solution | partial (edges = list of cell pairs)."""
    n = p["n"]; top = y0 + n * s
    fs = fs or min(13, max(5.5, s * 0.46))
    givens = {divmod(int(k), n): v for k, v in p["givens"].items()}
    X = lambda cc: x0 + cc * s + s / 2; Y = lambda r: top - r * s - s / 2
    c.saveState()
    if mode == "solution":
        c.setFillColor(ICE)
        for (r, cc) in givens: c.rect(x0 + cc * s, top - (r + 1) * s, s, s, stroke=0, fill=1)
    c.setStrokeColor(GRIDC); c.setLineWidth(0.5 if s > 12 else 0.3)
    for i in range(1, n):
        c.line(x0 + i * s, y0, x0 + i * s, top); c.line(x0, y0 + i * s, x0 + n * s, y0 + i * s)
    # entry / exit stubs
    er, ec = p["er"], p["ec"]
    stub = 0.55 * s
    if mode == "solution":
        c.setStrokeColor(INK); c.setLineWidth(max(1.2, s * 0.16)); c.setLineCap(1); c.setLineJoin(1)
        pts = [(x0 - stub, Y(er))] + [(X(cc), Y(r)) for r, cc in p["solution"]] + [(X(ec), y0 - stub)]
        pa = c.beginPath(); pa.moveTo(*pts[0])
        for q in pts[1:]: pa.lineTo(*q)
        c.drawPath(pa, stroke=1, fill=0)
    else:
        c.saveState(); cp = c.beginPath(); cp.rect(x0 - stub, Y(er) - s, stub, 2 * s); cp.rect(X(ec) - s, y0 - stub, 2 * s, stub)
        c.clipPath(cp, stroke=0, fill=0)
        draw_rails(c, x0 - s / 2, Y(er), s, "EW"); draw_rails(c, X(ec), y0 - s / 2, s, "NS")
        c.restoreState()
        for (r, cc), pc in givens.items(): draw_rails(c, X(cc), Y(r), s, pc)
        if edges:
            c.setStrokeColor(INK); c.setLineWidth(max(1.2, s * 0.12)); c.setLineCap(1)
            for (a, b) in edges:
                ax, ay = (x0 - s / 2, Y(a[0])) if a[1] < 0 else ((X(a[1]), y0 - s / 2) if a[0] >= n else (X(a[1]), Y(a[0])))
                bx, by = (X(b[1]), y0 - s / 2) if b[0] >= n else (X(b[1]), Y(b[0]))
                c.line(ax, ay, bx, by)
        c.setStrokeColor(MID); c.setLineWidth(max(0.8, s * 0.05))
        for (r, cc) in xs:
            d = s * 0.16; c.line(X(cc) - d, Y(r) - d, X(cc) + d, Y(r) + d); c.line(X(cc) - d, Y(r) + d, X(cc) + d, Y(r) - d)
    c.setStrokeColor(DARK); c.setLineWidth(1.3 if s > 12 else 0.8); c.rect(x0, y0, n * s, n * s)
    # counts: columns on top, rows on the right
    c.setFillColor(INK); c.setFont("Plex-M", fs)
    for i in range(n):
        c.drawCentredString(X(i), top + s * 0.22 + (0 if s > 12 else 1), str(p["cols"][i]))
        c.drawCentredString(x0 + n * s + s * 0.45 + (0 if s > 12 else 1), Y(i) - fs * 0.35, str(p["rows"][i]))
    if labels:
        c.setFont("PlayfairSC-B", fs * 0.95); c.setFillColor(DARK)
        c.drawRightString(x0 - stub - 3, Y(er) - fs * 0.35, "A")
        c.drawCentredString(X(ec), y0 - stub - fs * 0.95, "B")
    c.restoreState()


def tracks(c, x, y, w, h, v, sol=False):
    n = v["n"]; s = min(w / (n + 1.6), h / (n + 2.2), 0.55 * 72); x0 = x + (w - n * s) / 2 + s * 0.2; y0 = y + (h - n * s) / 2 + s * 0.2
    draw_grid(c, x0, y0, s, v, mode="solution" if sol else "puzzle", labels=True)
    top = y0 + n * s
    for k, ch in v["letters"].items():
        r, cc = P(k)
        c.setFillColor(colors.white); c.circle(x0 + cc * s + s / 2, top - r * s - s / 2, s * 0.24, stroke=0, fill=1)
        c.setFillColor(INK); c.setFont("PlayfairSC-B", s * 0.36); c.drawCentredString(x0 + cc * s + s / 2, top - r * s - s / 2 - s * 0.12, ch)
