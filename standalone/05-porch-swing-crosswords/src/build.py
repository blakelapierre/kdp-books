"""Builds the 6x9 interior PDF for Porch Swing Crosswords (black ink, no bleed, mirrored margins, embedded fonts)
-> ../standalone-05-porch-swing-crosswords-interior.pdf and ../build-info.json
Each puzzle is a two-page spread: clues on the left-hand (even) page, the grid on the right-hand (odd) page.
Run from src/: python3 build.py"""
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
    ("Crimson-B", "Crimson Text/CrimsonText-Bold.ttf"), ("Crimson-SB", "Crimson Text/CrimsonText-SemiBold.ttf"),
    ("Crimson-BI", "Crimson Text/CrimsonText-BoldItalic.ttf"),
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
PARTS = D["parts"]
ALL = [p for part in PARTS for p in part["puzzles"]]
assert len(ALL) == 80
TITLE = "Porch Swing Crosswords"
OUTNAME = "standalone-05-porch-swing-crosswords-interior.pdf"

W, H = 6 * inch, 9 * inch
INNER, OUTER, TOP, BOT = 0.75 * inch, 0.55 * inch, 0.70 * inch, 0.75 * inch
TW = W - INNER - OUTER
TH = H - TOP - BOT
DARK = colors.Color(0.12, 0.12, 0.12)
MID = colors.Color(0.40, 0.40, 0.40)
LINE = colors.Color(0.55, 0.55, 0.55)
INK = colors.Color(0.05, 0.05, 0.05)
ILL = os.path.join(ROOT, "illustrations")
VIGNETTES = ["v_pencil", "v_lemonade", "v_cat", "v_flowers", "v_leaves", "v_teacup", "v_swing", "v_pumpkin"]
PART_INFO = {
    "Spring": ("Part One", "Spring", "opener-spring", "Gentle warm-ups: about fifteen answers in each grid, with plain, friendly clues."),
    "Summer": ("Part Two", "Summer", "opener-summer", "Still easy, with a few more answers and slightly bigger grids."),
    "Autumn": ("Part Three", "Autumn", "opener-autumn", "Medium puzzles: bigger grids, more answers and more long words."),
    "Winter": ("Part Four", "Winter", "opener-winter", "The fullest grids in the book, for long, cozy evenings."),
}
LEVEL_DOTS = {"Easy": 1, "Medium": 2}

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


def small_holes(rows, maxsize=2):
    """Empty squares fully walled in by answer squares (holes of 1-2 squares) look like squares to write in,
    so they are inked solid black. Bigger enclosed gaps are clearly not answer squares and stay white."""
    nr, nc = len(rows), len(rows[0])
    seen, out = set(), set()
    for r in range(nr):
        for q in range(nc):
            if rows[r][q] != "." or (r, q) in seen:
                continue
            comp, st, edge = [], [(r, q)], False
            seen.add((r, q))
            while st:
                a, b = st.pop(); comp.append((a, b))
                for x, y in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
                    if not (0 <= x < nr and 0 <= y < nc):
                        edge = True
                    elif rows[x][y] == "." and (x, y) not in seen:
                        seen.add((x, y)); st.append((x, y))
            if not edge and len(comp) <= maxsize:
                out.update(comp)
    return out


class Book:
    def __init__(s, out, marks):
        s.c = canvas.Canvas(out, pagesize=(W, H), initialFontName="Crimson")
        s.c.setTitle("Porch Swing Crosswords: 80 Cozy Themed Crossword Puzzles for Adults")
        s.c.setAuthor("Blake La Pierre")
        s.c.setSubject("Crossword puzzle book")
        s.p = 0
        s.marks = {}
        s.prev = marks   # page numbers from the previous pass (for the contents and cross-references)

    def page(s, kind="normal", section=""):
        if s.p:
            s.c.showPage()
        s.p += 1
        s.kind, s.section = kind, section
        c = s.c
        if kind in ("title", "nofolio", "blank"):
            if kind == "blank":
                draw_ill(c, "v_swing", left_x(s.p) + (TW - 1.9 * inch) / 2, BOT + TH / 2 - 0.42 * inch, 1.9 * inch, 0.85 * inch)
            return left_x(s.p)
        c.saveState()
        c.setFont("Crimson", 9); c.setFillColor(MID)
        c.drawCentredString(left_x(s.p) + TW / 2, 0.42 * inch, str(s.p))
        if kind != "opener":
            c.setFont("PlayfairSC", 7.5)
            if s.p % 2 == 0:
                c.drawString(OUTER, H - 0.42 * inch, TITLE)
            else:
                c.drawRightString(W - OUTER, H - 0.42 * inch, section)
        c.restoreState()
        return left_x(s.p)

    def mark(s, k):
        s.marks[k] = s.p

    def ref(s, k):
        return s.prev.get(k, 0)

    # ---------------------------------------------------------------- front matter
    def front(s):
        c = s.c
        x = s.page("title")
        c.setFillColor(DARK); c.setFont("PlayfairSC-B", 28)
        c.drawCentredString(x + TW / 2, H - 2.9 * inch, "Porch Swing")
        c.drawCentredString(x + TW / 2, H - 2.9 * inch - 34, "Crosswords")
        draw_ill(c, "v_swing", x + (TW - 1.9 * inch) / 2, H - 4.6 * inch, 1.9 * inch, 0.85 * inch)
        x = s.page("title")
        draw_ill(c, "frontispiece", x, BOT + 0.35 * inch, TW, 7.0 * inch)
        c.setFont("Crimson-I", 10); c.setFillColor(MID)
        c.drawCentredString(x + TW / 2, BOT + 0.1 * inch, "A swing, a pencil and a lazy afternoon")
        x = s.page("title")
        y = H - TOP - 0.35 * inch
        c.setFont("PlayfairSC", 10); c.setFillColor(MID)
        c.drawCentredString(x + TW / 2, y, "Cozy Themed Crossword Puzzles for Adults")
        c.setFont("PlayfairSC-B", 36); c.setFillColor(DARK)
        c.drawCentredString(x + TW / 2, y - 52, "Porch Swing")
        c.drawCentredString(x + TW / 2, y - 94, "Crosswords")
        para(c, "80 puzzles through the seasons<br/>Easy to Medium · Plain Clues · Word Banks &amp; Solutions",
             ParagraphStyle("t2", parent=small, fontSize=12.5, leading=16), x, y - 118, TW)
        draw_ill(c, "title", x + (TW - 4.0 * inch) / 2, y - 4.15 * inch, 4.0 * inch, 2.0 * inch)
        c.setFont("Crimson", 13); c.setFillColor(DARK)
        c.drawCentredString(x + TW / 2, BOT + 0.6 * inch, "Blake La Pierre")
        x = s.page("nofolio")
        y = BOT + 3.2 * inch
        cs = ParagraphStyle("cp", parent=body, fontSize=9, leading=12, alignment=TA_LEFT)
        for t in ["<i>Porch Swing Crosswords: 80 Cozy Themed Crossword Puzzles for Adults</i>",
                  "Copyright © 2026 Blake La Pierre. All rights reserved.",
                  "No part of this book may be reproduced in any form without written permission from the author, except for brief quotations in reviews. Readers may photocopy puzzle pages for their own solving.",
                  "First edition, 2026",
                  "Set in Crimson Text, Playfair Display SC and IBM Plex Sans Condensed, used under the SIL Open Font License."]:
            y = para(c, t, cs, x, y, TW) - 6
        # contents
        x = s.page("normal", "Contents"); s.mark("contents")
        y = heading(c, x, H - TOP - 0.3 * inch, TITLE, "Contents")
        rows = [("How to Solve", s.ref("howto"))]
        for part in PARTS:
            num, name, _, _ = PART_INFO[part["name"]]
            ps = part["puzzles"]
            rows.append((f"{num} · {name}", f"{part['level']} · Puzzles {ps[0]['num']}–{ps[-1]['num']}", s.ref("part-" + part["name"])))
        rows += [("Word Banks", s.ref("banks")), ("Solutions", s.ref("solutions"))]
        y -= 10
        for r in rows:
            c.setFont("Crimson", 12.5); c.setFillColor(INK)
            c.drawString(x, y, r[0]); c.drawRightString(x + TW, y, str(r[-1]))
            if len(r) == 3:
                c.setFont("Crimson-I", 10); c.setFillColor(MID); c.drawString(x + 12, y - 13, r[1]); y -= 13
            c.setStrokeColor(LINE); c.setLineWidth(0.3); c.line(x, y - 6, x + TW, y - 6)
            y -= 26
        para(c, "A crossword for every week of the year, more or less: eighty friendly puzzles in four seasons, "
                "each one built around a cozy theme, from spring cleaning and the flower show to snow days and cocoa by the fire. "
                "No trivia about celebrities, no obscure words, no cryptic tricks. Just plain clues and a pencil.",
             ParagraphStyle("in", parent=small, fontSize=10.5, leading=14), x, y - 18, TW)
        # how to solve (left page) + tips (right page)
        x = s.page("normal", "How to Solve"); s.mark("howto")
        y = heading(c, x, H - TOP - 0.15 * inch, "Before You Begin", "How to Solve")
        hb = ParagraphStyle("hb", parent=body, fontSize=11, leading=14.4, spaceAfter=0)
        for t in [
            "Each puzzle takes up two facing pages. The <b>clues</b> are on the left, the <b>grid</b> is on the right, and every puzzle has a theme, "
            "so most of its answers belong together: things you'd find in a bakery, birds at the feeder, games on the lawn.",
            "Every answer starts in a <b>numbered square</b>. <b>Across</b> answers read left to right from their number, and <b>Down</b> answers read "
            "top to bottom. Write one letter in each square.",
            "Wherever two answers cross, they share a letter. That's the whole trick of a crossword: every answer you're sure of gives you letters for "
            "the answers that cross it.",
            "A clue with a blank, like <i>___ pin</i>, wants the missing word (ROLLING). A plural clue usually has a plural answer. "
            "No answer has spaces, hyphens or apostrophes.",
        ]:
            y = para(c, t, hb, x, y, TW) - 8
        # a tiny sample: SUN down crossing SWING across
        cell = 22; gx = x + 0.25 * inch; gy = y - 14
        sample = {(0, 3): ("S", 1), (1, 3): ("U", None), (2, 0): ("S", 2), (2, 1): ("W", None), (2, 2): ("I", None), (2, 3): ("N", None), (2, 4): ("G", None)}
        for (r, q), (ch, nn) in sample.items():
            cx, cy = gx + q * cell, gy - (r + 1) * cell
            c.setStrokeColor(INK); c.setLineWidth(0.9); c.setFillColor(colors.white); c.rect(cx, cy, cell, cell, stroke=1, fill=1)
            if nn:
                c.setFillColor(INK); c.setFont("Plex", 6.5); c.drawString(cx + 1.8, cy + cell - 7, str(nn))
            c.setFillColor(MID); c.setFont("Plex", 12); c.drawCentredString(cx + cell / 2, cy + 5, ch)
        tx = gx + 5 * cell + 18
        c.setFont("Crimson", 10.5); c.setFillColor(INK)
        c.drawString(tx, gy - 0.9 * cell, "1 Down: It shines on the porch  (SUN)")
        c.drawString(tx, gy - 1.9 * cell, "2 Across: It hangs from the porch roof  (SWING)")
        c.setFont("Crimson-I", 10); c.setFillColor(MID)
        c.drawString(tx, gy - 2.9 * cell, "The N is shared by both answers.")
        x = s.page("normal", "How to Solve")
        y = heading(c, x, H - TOP - 0.15 * inch, "Before You Begin", "Tips & Help")
        hl = ParagraphStyle("hl", parent=body, fontSize=10.8, leading=14, leftIndent=12, bulletIndent=0, spaceAfter=0, alignment=TA_LEFT)
        for t in [
            "<b>Start with the blanks.</b> Fill-in-the-blank clues are often the quickest wins.",
            "<b>Short answers next.</b> Three- and four-letter answers give you crossing letters for the long ones.",
            "<b>Think of the theme.</b> On the bakery page, a six-letter word for a long French loaf is probably a baker's word.",
            "<b>Use a pencil.</b> Write lightly, and rub out without worry.",
            "<b>Leave it and come back.</b> A clue that seems impossible often answers itself once two or three letters are in.",
            "<b>Word banks.</b> Really stuck? Every puzzle's answers are listed in alphabetical order in the Word Banks section at the back. "
            "With the word bank alone, each grid can be filled in exactly one way, so it turns any puzzle into a gentle fill-in.",
            "<b>Solutions</b> for all 80 puzzles follow the word banks.",
            "<b>Difficulty.</b> Spring and Summer are <b>Easy</b> (15 to 17 answers). Autumn and Winter are <b>Medium</b> (15 to 20 answers, "
            "bigger grids and more long words).",
        ]:
            y = para(c, t, hl, x, y, TW - 4) - 6
        draw_ill(c, "v_pencil", x + (TW - 1.9 * inch) / 2, BOT + 0.15 * inch, 1.9 * inch, 0.85 * inch)

    # ---------------------------------------------------------------- puzzle spreads
    def clue_block(s, P, x, y, fs, ld, draw=True):
        c = s.c
        st = ParagraphStyle("cl", fontName="Crimson", fontSize=fs, leading=ld, textColor=INK, alignment=TA_LEFT)
        for d, name in (("A", "Across"), ("D", "Down")):
            if draw:
                c.setFont("PlayfairSC-B", fs + 1.2); c.setFillColor(DARK); c.drawString(x, y - fs - 1, name)
            y -= ld + 6
            for e in [e for e in P["entries"] if e["dir"] == d]:
                p = Paragraph(e["clue"], st)
                _, h = p.wrap(TW - 26, 1000)
                if draw:
                    c.setFont("Crimson-B", fs); c.setFillColor(INK); c.drawRightString(x + 18, y - fs + 1, str(e["num"]))
                    p.drawOn(c, x + 26, y - h)
                y -= h + 2.2
            y -= 9
        return y

    def spread(s, P, part):
        c = s.c
        section = f"{PART_INFO[part['name']][1]} · {P['level']}"
        x = s.page("normal", section); s.mark(f"p{P['num']}")
        assert s.p % 2 == 0, "puzzle must start on a left-hand page"
        y = H - TOP
        c.setFont("PlayfairSC-B", 15); c.setFillColor(DARK)
        c.drawString(x, y - 14, f"{P['num']} · {P['title']}")
        # level dots
        c.setFont("Crimson-I", 9.5); c.setFillColor(MID)
        nd = LEVEL_DOTS[P["level"]]
        c.drawRightString(x + TW - 22, y - 13, P["level"])
        for i in range(2):
            cx = x + TW - 15 + i * 9
            c.setStrokeColor(DARK); c.setLineWidth(0.6)
            c.setFillColor(DARK if i < nd else colors.white); c.circle(cx - 3, y - 10, 2.8, stroke=1, fill=1)
        c.setStrokeColor(LINE); c.setLineWidth(0.5); c.line(x, y - 22, x + TW, y - 22)
        y = para(c, P["scene"], ParagraphStyle("sc", parent=body, fontName="Crimson-I", fontSize=10.5, leading=13.5, alignment=TA_LEFT, textColor=MID), x, y - 30, TW)
        y -= 10
        for fs, ld in ((11, 13.6), (10.6, 13.0), (10.2, 12.4), (9.8, 11.9)):
            end = s.clue_block(P, x, y, fs, ld, draw=False)
            if end > BOT:
                break
        assert end > BOT, f"clues overflow on puzzle {P['num']}"
        end = s.clue_block(P, x, y, fs, ld)
        if end - BOT > 1.05 * inch:
            vig = VIGNETTES[(P["num"] * 5) % len(VIGNETTES)]
            draw_ill(c, vig, x + (TW - 1.9 * inch) / 2, BOT + max(0, (end - BOT - 0.85 * inch) / 2 - 0.1 * inch), 1.9 * inch, 0.85 * inch)
        # right-hand page: the grid
        x = s.page("normal", section)
        rows = P["rows"]; nr, nc = len(rows), len(rows[0])
        top = H - TOP - 0.15 * inch
        c.setFont("PlayfairSC", 11); c.setFillColor(DARK)
        c.drawCentredString(x + TW / 2, top - 10, f"{P['num']} · {P['title']}")
        avail_h = TH - 0.15 * inch - 30 - 40
        cell = min(TW / nc, avail_h / nr, 0.42 * inch)
        gw, gh = cell * nc, cell * nr
        gx = x + (TW - gw) / 2
        gy = BOT + 40 + (avail_h - gh) / 2   # bottom of grid
        s.grid(rows, P["entries"], gx, gy, cell, letters=False)
        c.setFont("Crimson-I", 9); c.setFillColor(MID)
        c.drawCentredString(x + TW / 2, BOT + 8, f"Stuck? Word bank on page {s.ref('bank' + str(P['num']))} · Solution on page {s.ref('sol' + str(P['num']))}")

    def grid(s, rows, entries, gx, gy, cell, letters):
        c = s.c
        nr = len(rows)
        nums = {(e["r"], e["c"]): e["num"] for e in entries}
        c.setLineWidth(max(0.5, cell * 0.035)); c.setStrokeColor(INK)
        nc = len(rows[0])
        holes = small_holes(rows)
        for r, row in enumerate(rows):
            for q, ch in enumerate(row):
                if ch == ".":
                    if (r, q) in holes:
                        c.setFillColor(INK); c.rect(gx + q * cell, gy + (nr - 1 - r) * cell, cell, cell, stroke=1, fill=1)
                    continue
                x0, y0 = gx + q * cell, gy + (nr - 1 - r) * cell
                c.setFillColor(colors.white); c.rect(x0, y0, cell, cell, stroke=1, fill=1)
                if (r, q) in nums and not letters:
                    c.setFillColor(INK); c.setFont("Plex", max(5.2, cell * 0.27))
                    c.drawString(x0 + cell * 0.08, y0 + cell * 0.7, str(nums[(r, q)]))
                if letters:
                    c.setFillColor(INK); c.setFont("Plex-M", cell * 0.62)
                    c.drawCentredString(x0 + cell / 2, y0 + cell * 0.22, ch)

    # ---------------------------------------------------------------- parts
    def part(s, part):
        c = s.c
        num, name, art, blurb = PART_INFO[part["name"]]
        ps = part["puzzles"]
        x = s.page("opener"); s.mark("part-" + part["name"])
        assert s.p % 2 == 0
        y = heading(c, x, H - TOP - 1.2 * inch, num, name, size=30)
        c.setFont("Crimson-I", 12); c.setFillColor(MID)
        c.drawCentredString(x + TW / 2, y - 6, f"{part['level']} · Puzzles {ps[0]['num']} to {ps[-1]['num']}")
        para(c, blurb, ParagraphStyle("bl", parent=small, fontSize=11, leading=15), x, y - 26, TW)
        draw_ill(c, art, x, BOT + 1.0 * inch, TW, 2.6 * inch)
        x = s.page("normal", f"{name} · {part['level']}")
        y = heading(c, x, H - TOP - 0.2 * inch, f"{num} · {part['level']}", f"In {name}", size=18)
        y -= 4
        for P in ps:
            c.setFont("Crimson", 11.5); c.setFillColor(INK)
            c.drawString(x + 0.3 * inch, y, f"{P['num']}.  {P['title']}")
            c.drawRightString(x + TW - 0.3 * inch, y, str(s.ref(f"p{P['num']}")))
            y -= 17.5
        for P in ps:
            s.spread(P, part)

    # ---------------------------------------------------------------- back matter
    def banks(s):
        c = s.c
        x = s.page("normal", "Word Banks"); s.mark("banks")
        y = heading(c, x, H - TOP - 0.1 * inch, "For When You're Stuck", "Word Banks", size=18)
        y = para(c, "Each puzzle's answers in alphabetical order. With these, every grid fills in only one way.",
                 ParagraphStyle("wb", parent=small, fontSize=10, leading=13), x, y, TW) - 12
        st = ParagraphStyle("bk", fontName="Plex", fontSize=8.8, leading=11.6, textColor=INK, alignment=TA_LEFT)
        for P in ALL:
            words = sorted(e["answer"] for e in P["entries"])
            t = f"<font name='Plex-M'>{P['num']} · {P['title']}</font>&nbsp;&nbsp; " + " · ".join(words)
            p = Paragraph(t, st)
            _, h = p.wrap(TW, 1000)
            if y - h < BOT:
                x = s.page("normal", "Word Banks"); y = H - TOP
            p.drawOn(c, x, y - h); s.marks["bank" + str(P["num"])] = s.p
            y -= h + 7

    def solutions(s):
        c = s.c
        if s.p % 2 == 0:
            s.page("blank")
        x = s.page("normal", "Solutions"); s.mark("solutions")
        y0 = heading(c, x, H - TOP - 0.1 * inch, "Every Answer, Filled In", "Solutions", size=18) + 4
        per = 6
        first = True
        i = 0
        while i < len(ALL):
            if not first:
                x = s.page("normal", "Solutions"); y0 = H - TOP
            first = False
            colw = (TW - 16) / 2
            rowh = (y0 - BOT) / 3
            for k in range(per):
                if i >= len(ALL):
                    break
                P = ALL[i]; i += 1
                col, row = k % 2, k // 2
                bx = x + col * (colw + 16); btop = y0 - row * rowh
                rows = P["rows"]; nr, nc = len(rows), len(rows[0])
                cell = min(colw / nc, (rowh - 22) / nr)
                c.setFont("Plex-M", 8.2); c.setFillColor(INK)
                c.drawCentredString(bx + colw / 2, btop - 9, f"{P['num']} · {P['title']}")
                gx = bx + (colw - cell * nc) / 2
                s.grid(rows, P["entries"], gx, btop - 15 - cell * nr, cell, letters=True)
                s.marks["sol" + str(P["num"])] = s.p

    def thanks(s):
        c = s.c
        x = s.page("nofolio")
        y = heading(c, x, H - TOP - 1.3 * inch, "Thank You", "For Swinging By", size=20)
        y = para(c, "If these puzzles kept you company, a short, honest review helps other puzzlers find the book. "
                    "Thank you for your pencil, your patience and your quiet afternoons.", ParagraphStyle("ty", parent=body, alignment=TA_CENTER), x, y - 6, TW)
        c.setFont("PlayfairSC", 10); c.setFillColor(DARK)
        c.drawCentredString(x + TW / 2, y - 34, "Also by Blake La Pierre")
        para(c, "<i>The Thief Stayed the Night</i> · <i>Frostwood Express</i>", ParagraphStyle("ab", parent=small, fontSize=10, leading=13), x, y - 42, TW)
        draw_ill(c, "thanks", x + (TW - 3.4 * inch) / 2, y - 2.6 * inch, 3.4 * inch, 1.6 * inch)

    def save(s):
        s.c.showPage(); s.c.save()


def render(out, marks):
    b = Book(out, marks)
    b.front()
    for part in PARTS:
        b.part(part)
    b.banks()
    b.solutions()
    if b.p % 2 == 0:
        b.page("blank")
    b.thanks()
    if b.p % 2 == 1:
        b.page("blank")
    b.save()
    return b.marks, b.p


if __name__ == "__main__":
    out = os.path.join(ROOT, OUTNAME)
    marks = {}
    for _ in range(4):
        new, pages = render(out, marks)
        if new == marks:
            break
        marks = new
    assert new == marks
    info = {"pages": pages, "marks": {k: v for k, v in marks.items() if not k[:3] in ("ban", "sol", "p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9") or k in ("banks", "solutions")}}
    info["marks"] = {k: v for k, v in marks.items() if k in ("contents", "howto", "banks", "solutions") or k.startswith("part-")}
    info["puzzles"] = len(ALL)
    json.dump(info, open(os.path.join(ROOT, "build-info.json"), "w"), indent=1)
    print(json.dumps(info, indent=1))
    print(f"Wrote {out} ({pages} pages)")
