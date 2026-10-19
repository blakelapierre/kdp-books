"""Builds the 6x9 interior PDF for Window Seat Codewords (black ink, no bleed, mirrored margins, embedded fonts)
-> ../standalone-08-window-seat-codewords-interior.pdf and ../build-info.json
One codeword per page: numbered grid, key strip for 1-26 and an A-Z cross-off line. Run from src/: python3 build.py"""
from __future__ import annotations
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.fonts import addMapping

G = "/usr/share/fonts/truetype/sand-box/google/"
for n, p in [
    ("Crimson", "Crimson Text/CrimsonText-Regular.ttf"), ("Crimson-I", "Crimson Text/CrimsonText-Italic.ttf"),
    ("Crimson-B", "Crimson Text/CrimsonText-Bold.ttf"), ("Crimson-BI", "Crimson Text/CrimsonText-BoldItalic.ttf"),
    ("PlayfairSC", "Playfair Display SC/PlayfairDisplaySC-Regular.ttf"), ("PlayfairSC-B", "Playfair Display SC/PlayfairDisplaySC-Bold.ttf"),
    ("Plex", "IBM Plex Sans Condensed/IBMPlexSansCondensed-Regular.ttf"), ("Plex-M", "IBM Plex Sans Condensed/IBMPlexSansCondensed-SemiBold.ttf"),
]:
    pdfmetrics.registerFont(TTFont(n, G + p))
addMapping("Crimson", 0, 0, "Crimson"); addMapping("Crimson", 0, 1, "Crimson-I")
addMapping("Crimson", 1, 0, "Crimson-B"); addMapping("Crimson", 1, 1, "Crimson-BI")
ParagraphStyle.defaults["fontName"] = "Crimson"

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
D = json.load(open(os.path.join(ROOT, "data.json")))
LEVELS = D["levels"]
ALL = [p for lv in LEVELS for p in lv["puzzles"]]
assert len(ALL) == 120
TITLE = "Window Seat Codewords"
OUTNAME = "standalone-08-window-seat-codewords-interior.pdf"
W, H = 6 * inch, 9 * inch
INNER, OUTER, TOP, BOT = 0.75 * inch, 0.55 * inch, 0.70 * inch, 0.75 * inch
TW = W - INNER - OUTER
TH = H - TOP - BOT
DARK = colors.Color(0.12, 0.12, 0.12)
MID = colors.Color(0.40, 0.40, 0.40)
LINE = colors.Color(0.55, 0.55, 0.55)
INK = colors.Color(0.05, 0.05, 0.05)
ILL = os.path.join(ROOT, "illustrations")
VIGNETTES = ["v_mug", "v_cat", "v_key", "v_sheet", "v_tea", "v_plant", "v_candle"]
PART = {
    "Easy": ("Part One", "Morning Light", "opener-easy",
             "Easy codewords to warm up with. Six starter letters are filled in, and the answers are the most everyday words in the book."),
    "Medium": ("Part Two", "Rainy Afternoon", "opener-medium",
               "Medium codewords. Four starter letters, and a slightly wider range of words."),
    "Hard": ("Part Three", "Snowy Evening", "opener-hard",
             "Hard codewords. Only two starter letters, so the first few steps take real detective work."),
}
DOTS = {"Easy": 1, "Medium": 2, "Hard": 3}
body = ParagraphStyle("body", fontName="Crimson", fontSize=11, leading=14.4, textColor=INK, alignment=TA_JUSTIFY)
small = ParagraphStyle("small", parent=body, fontSize=10, leading=13, alignment=TA_CENTER, textColor=MID)


def left_x(p):
    return INNER if p % 2 == 1 else OUTER


def draw_ill(c, name, x, y, w, h):
    path = os.path.join(ILL, name + ".png")
    iw, ih = ImageReader(path).getSize()
    sc = min(w / iw, h / ih)
    c.drawImage(path, x + (w - iw * sc) / 2, y + (h - ih * sc) / 2, iw * sc, ih * sc)
    return ih * sc


def para(c, text, style, x, ytop, width):
    p = Paragraph(text, style)
    _, h = p.wrap(width, 10000)
    p.drawOn(c, x, ytop - h)
    return ytop - h


def heading(c, x, y, kicker, title, size=20):
    c.setFillColor(MID); c.setFont("PlayfairSC", 9.5)
    c.drawCentredString(x + TW / 2, y, kicker)
    c.setFillColor(DARK); c.setFont("PlayfairSC-B", size)
    c.drawCentredString(x + TW / 2, y - size - 4, title)
    return y - size - 18


def dots(c, x, y, n, r=2.6):
    for i in range(3):
        c.setStrokeColor(DARK); c.setLineWidth(0.7)
        c.setFillColor(DARK if i < n else colors.white)
        c.circle(x + i * 8, y, r, stroke=1, fill=1)


class Book:
    def __init__(s, out, marks):
        s.c = canvas.Canvas(out, pagesize=(W, H), initialFontName="Crimson")
        s.c.setTitle("Window Seat Codewords: 120 Cozy Codeword Puzzles for Adults")
        s.c.setAuthor("Blake La Pierre")
        s.c.setSubject("Codeword puzzle book")
        s.p = 0; s.marks = {}; s.prev = marks

    def page(s, kind="normal", section=""):
        if s.p: s.c.showPage()
        s.p += 1
        c = s.c
        if kind in ("title", "nofolio", "blank"):
            if kind == "blank":
                draw_ill(c, "v_cat", left_x(s.p) + (TW - 1.9 * inch) / 2, BOT + TH / 2 - 0.4 * inch, 1.9 * inch, 0.8 * inch)
            return left_x(s.p)
        c.saveState()
        c.setFont("Crimson", 9); c.setFillColor(MID)
        c.drawCentredString(left_x(s.p) + TW / 2, 0.42 * inch, str(s.p))
        if kind != "opener":
            c.setFont("PlayfairSC", 7.5)
            if s.p % 2 == 0: c.drawString(OUTER, H - 0.42 * inch, TITLE)
            else: c.drawRightString(W - OUTER, H - 0.42 * inch, section)
        c.restoreState()
        return left_x(s.p)

    def mark(s, k): s.marks[k] = s.p
    def ref(s, k): return s.prev.get(k, 0)

    # ---------------------------------------------------------------- grid drawing
    def grid(s, P, x, y, cell, solved=False, numbers=True):
        """Draw puzzle P with its top-left at (x, y)."""
        c = s.c
        nums = P["numbers"]; key = P["key"]; giv = P["givens"]
        n = len(nums)
        for r in range(n):
            for q in range(n):
                cx, cy = x + q * cell, y - (r + 1) * cell
                v = nums[r][q]
                if not v:
                    c.setFillColor(DARK); c.rect(cx, cy, cell, cell, stroke=0, fill=1); continue
                c.setStrokeColor(DARK); c.setLineWidth(0.5); c.setFillColor(colors.white)
                c.rect(cx, cy, cell, cell, stroke=1, fill=0)
                if numbers:
                    c.setFillColor(INK); c.setFont("Plex", cell * 0.25)
                    c.drawString(cx + cell * 0.06, cy + cell * 0.72, str(v))
                L = key[str(v)] if solved else giv.get(str(v))
                if L:
                    c.setFillColor(INK)
                    if numbers:
                        c.setFont("Plex-M", cell * 0.52); c.drawCentredString(cx + cell * 0.56, cy + cell * 0.14, L)
                    else:
                        c.setFont("Plex-M", cell * 0.66); c.drawCentredString(cx + cell / 2, cy + cell * 0.24, L)
        c.setStrokeColor(DARK); c.setLineWidth(1.2 if numbers else 0.8)
        c.rect(x, y - n * cell, n * cell, n * cell, stroke=1, fill=0)

    def puzzle_page(s, P, k):
        c = s.c
        x = s.page("normal", f"{P['level']} Codewords")
        s.marks["p" + str(P["id"])] = s.p
        top = H - TOP
        c.setFillColor(DARK); c.setFont("PlayfairSC-B", 15)
        c.drawString(x, top - 14, f"Codeword {P['id']}")
        c.setFont("PlayfairSC", 9.5); c.setFillColor(MID)
        c.drawRightString(x + TW - 30, top - 12, P["level"])
        dots(c, x + TW - 19, top - 9, DOTS[P["level"]])
        c.setFont("Crimson-I", 9); c.setFillColor(MID)
        c.drawString(x, top - 28, f"Starter letters: {', '.join(P['givens'][n] + ' = ' + n for n in sorted(P['givens'], key=int))}")
        n = len(P["numbers"])
        cell = 0.335 * inch
        gw = cell * n
        gx = x + (TW - gw) / 2
        gy = top - 0.5 * inch
        s.grid(P, gx, gy, cell)
        # key strip
        ky = gy - gw - 0.22 * inch
        c.setFont("PlayfairSC", 8); c.setFillColor(MID)
        c.drawString(gx, ky + 3, "Key")
        kc = gw / 13
        kh = 0.34 * inch
        for i in range(26):
            row, col = divmod(i, 13)
            bx = gx + col * kc; by = ky - (row + 1) * kh - row * 3
            c.setStrokeColor(DARK); c.setLineWidth(0.6); c.setFillColor(colors.white)
            c.rect(bx, by, kc, kh, stroke=1, fill=0)
            c.setFillColor(INK); c.setFont("Plex", 6.3)
            c.drawString(bx + 1.6, by + kh - 7, str(i + 1))
            L = P["givens"].get(str(i + 1))
            if L:
                c.setFont("Plex-M", 12); c.drawCentredString(bx + kc * 0.56, by + 3.5, L)
        # alphabet cross-off line
        ay = ky - 2 * kh - 3 - 0.3 * inch
        c.setFont("PlayfairSC", 8); c.setFillColor(MID)
        c.drawString(gx, ay + 13, "Cross off each letter as you place it")
        used = set(P["givens"].values())
        step = gw / 26
        for i in range(26):
            L = chr(65 + i)
            lx = gx + step * (i + 0.5)
            c.setFillColor(INK); c.setFont("Plex-M", 10)
            c.drawCentredString(lx, ay, L)
            if L in used:
                c.setStrokeColor(INK); c.setLineWidth(0.9); c.line(lx - 4, ay + 3.5, lx + 4, ay + 3.5)
        # vignette
        v = VIGNETTES[k % len(VIGNETTES)]
        vh = min(0.62 * inch, ay - 0.25 * inch - BOT)
        if vh > 0.35 * inch:
            draw_ill(c, v, x + (TW - 1.5 * inch) / 2, BOT + 0.02 * inch, 1.5 * inch, vh)

    # ---------------------------------------------------------------- front matter
    def front(s):
        c = s.c
        x = s.page("title")
        y = H - TOP - 0.35 * inch
        c.setFont("PlayfairSC", 10); c.setFillColor(MID)
        c.drawCentredString(x + TW / 2, y, "Cozy Codeword Puzzles for Adults")
        c.setFont("PlayfairSC-B", 36); c.setFillColor(DARK)
        c.drawCentredString(x + TW / 2, y - 52, "Window Seat")
        c.drawCentredString(x + TW / 2, y - 94, "Codewords")
        para(c, "120 puzzles in American English<br/>Easy · Medium · Hard · Full Solutions",
             ParagraphStyle("t2", parent=small, fontSize=12.5, leading=16), x, y - 118, TW)
        draw_ill(c, "title", x + (TW - 4.0 * inch) / 2, y - 4.0 * inch, 4.0 * inch, 1.8 * inch)
        c.setFont("Crimson", 13); c.setFillColor(DARK)
        c.drawCentredString(x + TW / 2, BOT + 0.6 * inch, "Blake La Pierre")
        x = s.page("nofolio")
        y = BOT + 3.0 * inch
        cs = ParagraphStyle("cp", parent=body, fontSize=9, leading=12, alignment=TA_LEFT)
        for t in ["<i>Window Seat Codewords: 120 Cozy Codeword Puzzles for Adults</i>",
                  "Copyright © 2026 Blake La Pierre. All rights reserved.",
                  "No part of this book may be reproduced in any form without written permission from the author, except for brief quotations in reviews. Readers may photocopy puzzle pages for their own solving.",
                  "Every puzzle was checked by computer to have exactly one solution, using a 172,823-word dictionary.",
                  "First edition, 2026",
                  "Set in Crimson Text, Playfair Display SC and IBM Plex Sans Condensed, used under the SIL Open Font License."]:
            y = para(c, t, cs, x, y, TW) - 6
        x = s.page("normal", "Contents"); s.mark("contents")
        y = heading(c, x, H - TOP - 0.3 * inch, TITLE, "Contents")
        rows = [("How to Solve", s.ref("howto")), ("Solving Tips", s.ref("tips"))]
        for lv in LEVELS:
            num, name, _, _ = PART[lv["name"]]
            ps = lv["puzzles"]
            rows.append((f"{num} · {name}", f"{lv['name']} · Codewords {ps[0]['id']}–{ps[-1]['id']}", s.ref("part-" + lv["name"])))
        rows += [("Solutions", s.ref("solutions"))]
        y -= 10
        for r in rows:
            c.setFont("Crimson", 12.5); c.setFillColor(INK)
            c.drawString(x, y, r[0]); c.drawRightString(x + TW, y, str(r[-1]))
            if len(r) == 3:
                c.setFont("Crimson-I", 10); c.setFillColor(MID); c.drawString(x + 12, y - 13, r[1]); y -= 13
            c.setStrokeColor(LINE); c.setLineWidth(0.3); c.line(x, y - 6, x + TW, y - 6)
            y -= 26
        x = s.page("nofolio")
        draw_ill(c, "frontispiece", x, BOT + 0.45 * inch, TW, 6.6 * inch)
        c.setFont("Crimson-I", 10); c.setFillColor(MID)
        c.drawCentredString(x + TW / 2, BOT + 0.15 * inch, "A cushion, a pencil and the rain on the glass")
        s.howto()
        s.tips()

    def howto(s):
        c = s.c
        x = s.page("normal", "How to Solve"); s.mark("howto")
        y = heading(c, x, H - TOP - 0.2 * inch, "Before You Begin", "How to Solve")
        st = ParagraphStyle("h", parent=body, spaceAfter=0)
        for t in [
            "A codeword is a crossword with no clues. Every white square holds a number from <b>1 to 26</b>, and each number stands for one letter of the alphabet. "
            "The same number is always the same letter, wherever it appears. Different numbers are always different letters, and <b>every letter from A to Z is used</b> somewhere in each grid.",
            "A few <b>starter letters</b> are filled in for you, shown in the grid and in the key below it. Put each new letter you discover into every square with that number, "
            "write it in the key and cross it off the alphabet line. Every across and down answer is an everyday English word, and the puzzle has only one solution.",
        ]:
            y = para(c, t, st, x, y, TW) - 9
        # worked example: KETTLE
        c.setFont("PlayfairSC", 9.5); c.setFillColor(MID)
        c.drawCentredString(x + TW / 2, y - 6, "A small example")
        cell = 0.36 * inch
        word = "KETTLE"; nums = [15, 3, 7, 7, 21, 3]
        gx = x + (TW - cell * 6) / 2; gy = y - 16
        for stage, shown in enumerate(({"E"}, {"E", "T"})):
            yy = gy - stage * (cell + 26)
            for i, (L, nn) in enumerate(zip(word, nums)):
                cx, cy = gx + i * cell, yy - cell
                c.setStrokeColor(DARK); c.setLineWidth(0.7); c.rect(cx, cy, cell, cell, stroke=1, fill=0)
                c.setFillColor(INK); c.setFont("Plex", 7); c.drawString(cx + 2, cy + cell - 8, str(nn))
                if L in shown:
                    c.setFont("Plex-M", 13); c.drawCentredString(cx + cell * 0.56, cy + 4, L)
            c.setFont("Crimson-I", 9.5); c.setFillColor(MID)
            c.drawCentredString(x + TW / 2, yy - cell - 11,
                                "3 is a starter letter, E. Both 3s in this answer are E." if stage == 0 else
                                "7 7 is a double letter between two Es. TT fits well, so try 7 = T.")
        y = gy - 2 * (cell + 26) - 8
        for t in [
            "Try a guess like that in pencil, then check it against the answers that cross it. When a word such as KETTLE appears, write K in every 15 and L in every 21, and carry on.",
            "Stuck? The full solution to every puzzle is at the back of the book, starting on page " + str(s.ref("solutions")) + ".",
        ]:
            y = para(c, t, st, x, y, TW) - 9

    def tips(s):
        c = s.c
        x = s.page("normal", "Solving Tips"); s.mark("tips")
        y = heading(c, x, H - TOP - 0.2 * inch, "From the Window Seat", "Solving Tips")
        li = ParagraphStyle("li", parent=body, leftIndent=14, firstLineIndent=-12)
        for t in [
            "<b>Start where the starters are.</b> Look for short answers that already have one or two letters showing.",
            "<b>Look for patterns.</b> A double number (like 7 7) is often LL, EE, SS, OO, TT or RR. An answer with the same number in the first and last square might be a word like EAGLE or TOAST.",
            "<b>Use common endings.</b> Answers often end in -ED, -ER, -ES, -ING, -LY or -TION. If three numbers keep showing up together at the ends of answers, try -ING.",
            "<b>Q is nearly always followed by U.</b> And the rarest letters, J, Q, X and Z, are each used at least once in every grid, often only once.",
            "<b>Count the numbers.</b> The number that appears most often is usually E, and the next few are often A, S, T, R, I or O.",
            "<b>Keep the alphabet tidy.</b> Crossing letters off as you go tells you which letters are left, which is a big help near the end.",
            "<b>Use a pencil.</b> A light guess you can rub out is better than an empty grid.",
        ]:
            y = para(c, "•&nbsp;&nbsp;" + t, li, x, y, TW) - 6
        y -= 6
        y = para(c, "All the answers are ordinary words in American spelling. There are no names of people or places, no abbreviations and nothing gloomy: just the kind of words you'd use over a cup of tea.",
                 ParagraphStyle("n", parent=body, fontName="Crimson-I"), x, y, TW)
        draw_ill(c, "v_tea", x + (TW - 1.9 * inch) / 2, BOT + 0.1 * inch, 1.9 * inch, 0.8 * inch)

    def opener(s, lv):
        c = s.c
        if s.p % 2 == 1: s.page("blank")
        x = s.page("opener"); s.mark("part-" + lv["name"])
        num, name, art, blurb = PART[lv["name"]]
        y = H - TOP - 0.9 * inch
        c.setFillColor(MID); c.setFont("PlayfairSC", 11); c.drawCentredString(x + TW / 2, y, num)
        c.setFillColor(DARK); c.setFont("PlayfairSC-B", 28); c.drawCentredString(x + TW / 2, y - 38, name)
        ps = lv["puzzles"]
        c.setFont("Crimson-I", 13); c.setFillColor(MID)
        c.drawCentredString(x + TW / 2, y - 60, f"{lv['name']} · Codewords {ps[0]['id']}–{ps[-1]['id']}")
        dots(c, x + TW / 2 - 8, y - 78, DOTS[lv["name"]], r=3.2)
        draw_ill(c, art, x, y - 100 - 2.6 * inch, TW, 2.6 * inch)
        para(c, blurb, ParagraphStyle("ob", parent=body, alignment=TA_CENTER, fontName="Crimson-I", fontSize=12, leading=16), x + 0.3 * inch, y - 118 - 2.6 * inch, TW - 0.6 * inch)

    def solutions(s):
        c = s.c
        if s.p % 2 == 1: s.page("blank")
        x = s.page("opener"); s.mark("solutions")
        y = H - TOP - 1.2 * inch
        c.setFillColor(MID); c.setFont("PlayfairSC", 11); c.drawCentredString(x + TW / 2, y, "Every Grid, Filled In")
        c.setFillColor(DARK); c.setFont("PlayfairSC-B", 28); c.drawCentredString(x + TW / 2, y - 38, "Solutions")
        draw_ill(c, "opener-solutions", x + (TW - 4.0 * inch) / 2, y - 70 - 1.8 * inch, 4.0 * inch, 1.8 * inch)
        para(c, "Each solution shows the finished grid. Under it is the full key, number by number, so you can check a single letter without seeing the rest of the puzzle.",
             ParagraphStyle("sb", parent=body, alignment=TA_CENTER, fontName="Crimson-I", fontSize=12, leading=16), x + 0.3 * inch, y - 90 - 1.8 * inch, TW - 0.6 * inch)
        per = 6; i = 0
        while i < len(ALL):
            x = s.page("normal", "Solutions"); y0 = H - TOP
            colw = (TW - 18) / 2; rowh = (y0 - BOT) / 3
            for k in range(per):
                if i >= len(ALL): break
                P = ALL[i]; i += 1
                col, row = k % 2, k // 2
                bx = x + col * (colw + 18); btop = y0 - row * rowh
                n = len(P["numbers"])
                cell = min(colw / n, (rowh - 36) / n)
                c.setFont("Plex-M", 8.2); c.setFillColor(INK)
                c.drawCentredString(bx + colw / 2, btop - 9, f"Codeword {P['id']} · {P['level']}")
                gx = bx + (colw - cell * n) / 2
                s.grid(P, gx, btop - 14, cell, solved=True, numbers=False)
                ky = btop - 14 - cell * n - 9
                c.setFont("Plex", 5.6); c.setFillColor(INK)
                kk = [f"{m}{P['key'][str(m)]}" for m in range(1, 27)]
                c.drawCentredString(bx + colw / 2, ky, " ".join(kk[:13]))
                c.drawCentredString(bx + colw / 2, ky - 7.5, " ".join(kk[13:]))
                s.marks["sol" + str(P["id"])] = s.p

    def thanks(s):
        c = s.c
        x = s.page("nofolio")
        y = heading(c, x, H - TOP - 1.2 * inch, "Thank You", "For Sitting a While", size=20)
        y = para(c, "If these codewords kept you company, a short, honest review helps other puzzlers find the book. "
                    "Thank you for your pencil, your patience and your quiet afternoons.", ParagraphStyle("ty", parent=body, alignment=TA_CENTER), x, y - 6, TW)
        c.setFont("PlayfairSC", 10); c.setFillColor(DARK)
        c.drawCentredString(x + TW / 2, y - 34, "Also by Blake La Pierre")
        para(c, "<i>Porch Swing Crosswords</i> · <i>Fireside Cryptograms</i> · <i>Logic on Lantern Lane</i>", ParagraphStyle("ab", parent=small, fontSize=10, leading=13), x, y - 42, TW)
        draw_ill(c, "thanks", x + (TW - 3.4 * inch) / 2, y - 2.9 * inch, 3.4 * inch, 2.2 * inch)

    def save(s):
        s.c.showPage(); s.c.save()


def render(out, marks):
    b = Book(out, marks)
    b.front()
    k = 0
    for lv in LEVELS:
        b.opener(lv)
        for P in lv["puzzles"]:
            b.puzzle_page(P, k); k += 1
    b.solutions()
    if b.p % 2 == 0: b.page("blank")
    b.thanks()
    if b.p % 2 == 1: b.page("blank")
    b.save()
    return b.marks, b.p


if __name__ == "__main__":
    out = os.path.join(ROOT, OUTNAME)
    marks = {}
    for _ in range(4):
        new, pages = render(out, marks)
        if new == marks: break
        marks = new
    assert new == marks
    info = {"pages": pages, "marks": {k: v for k, v in marks.items() if k in ("contents", "howto", "tips", "solutions") or k.startswith("part-")}, "puzzles": len(ALL)}
    json.dump(info, open(os.path.join(ROOT, "build-info.json"), "w"), indent=1)
    print(json.dumps(info, indent=1)); print(f"Wrote {out} ({pages} pages)")
