"""Builds the 6x9 interior PDF for The Thimble Hill Word Search Mysteries (black ink, no bleed, mirrored margins, embedded fonts)
-> ../standalone-11-thimble-hill-word-search-mysteries-interior.pdf and ../build-info.json.  Run from src/: python3 build.py
Two passes: the first records page numbers for the contents page, the second uses them."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.fonts import addMapping
import content

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

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
ILL = os.path.join(ROOT, "illustrations")
D = json.load(open(os.path.join(ROOT, "data.json")))
CASES = D["cases"]
N = D["size"]
assert len(CASES) == 10 and sum(len(c["puzzles"]) for c in CASES) == 60
TITLE = "The Thimble Hill Word Search Mysteries"
OUTNAME = "standalone-11-thimble-hill-word-search-mysteries-interior.pdf"
W, H = 6 * inch, 9 * inch
INNER, OUTER, TOP, BOT = 0.75 * inch, 0.55 * inch, 0.65 * inch, 0.70 * inch
TW = W - INNER - OUTER
TH = H - TOP - BOT
DARK = colors.Color(0.12, 0.12, 0.12)
MID = colors.Color(0.40, 0.40, 0.40)
LIGHT = colors.Color(0.62, 0.62, 0.62)
INK = colors.Color(0.05, 0.05, 0.05)
LEVEL_HELP = {
    "Gentle": "Words run left to right, top to bottom, or diagonally down to the right. Nothing is backwards.",
    "Curious": "Words run left to right, top to bottom, diagonally down to the right, or diagonally up to the right. Nothing is backwards.",
    "Sharp-Eyed": "Words can run in all eight directions, including backwards and diagonally both ways.",
}
DOTS = {"Gentle": 1, "Curious": 2, "Sharp-Eyed": 3}
WORDS = ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"]

body = ParagraphStyle("body", fontName="Crimson", fontSize=11, leading=14.3, textColor=INK, alignment=TA_JUSTIFY)
bodyl = ParagraphStyle("bodyl", parent=body, alignment=TA_LEFT)
story = ParagraphStyle("story", parent=body, fontName="Crimson-I", fontSize=10.5, leading=13.4)
small = ParagraphStyle("small", parent=body, fontSize=9.5, leading=12.2, alignment=TA_CENTER, textColor=MID)
susp = ParagraphStyle("susp", parent=body, fontSize=10.5, leading=13.4)


def left_x(p):
    return INNER if p % 2 == 1 else OUTER


def draw_ill(c, name, x, y, w, h):
    path = os.path.join(ILL, name + ".png")
    iw, ih = ImageReader(path).getSize()
    sc = min(w / iw, h / ih)
    c.drawImage(path, x + (w - iw * sc) / 2, y + (h - ih * sc) / 2, iw * sc, ih * sc)


def para(c, text, style, x, ytop, width):
    p = Paragraph(text, style)
    _, h = p.wrap(width, 10000)
    p.drawOn(c, x, ytop - h)
    return ytop - h


def ornament(c, cx, y, w=1.1 * inch):
    c.setStrokeColor(MID); c.setLineWidth(0.6)
    c.line(cx - w / 2, y, cx - 6, y); c.line(cx + 6, y, cx + w / 2, y)
    c.setFillColor(MID); c.circle(cx, y, 1.8, stroke=0, fill=1)


def dots(c, x, y, n, r=2.6):
    for i in range(3):
        c.setStrokeColor(DARK); c.setLineWidth(0.7)
        c.setFillColor(DARK if i < n else colors.white)
        c.circle(x + i * 8, y, r, stroke=1, fill=1)


def clue_boxes(c, clue, x, ytop, width, box=0.175 * inch, filled=False):
    """Letter boxes for the hidden clue, one group per word, wrapping onto new lines. Returns the y below them."""
    gap = box * 0.55
    lines, cur, cw = [], [], 0
    for wd in clue.split():
        need = len(wd) * box + (gap if cur else 0)
        if cur and cw + need > width:
            lines.append(cur); cur, cw = [], 0; need = len(wd) * box
        cur.append(wd); cw += need
    lines.append(cur)
    y = ytop
    for ln in lines:
        lw = sum(len(wd) for wd in ln) * box + gap * (len(ln) - 1)
        bx = x + (width - lw) / 2
        y -= box
        for wd in ln:
            for ch in wd:
                c.setStrokeColor(DARK); c.setLineWidth(0.6); c.setFillColor(colors.white)
                c.rect(bx, y, box, box, stroke=1, fill=0)
                if filled:
                    c.setFillColor(INK); c.setFont("Plex-M", box * 0.62); c.drawCentredString(bx + box / 2, y + box * 0.22, ch)
                bx += box
            bx += gap
        y -= box * 0.35
    return y


def word_cells(pl):
    return [(pl["r"] + pl["dr"] * i, pl["c"] + pl["dc"] * i) for i in range(len(pl["word"]))]


class Book:
    def __init__(s, out, marks):
        s.c = canvas.Canvas(out, pagesize=(W, H), initialFontName="Crimson")
        s.c.setTitle("The Thimble Hill Word Search Mysteries: 60 Cozy Puzzles, 10 Gentle Mysteries")
        s.c.setAuthor("Blake La Pierre")
        s.c.setSubject("Word search mystery puzzle book")
        s.p = 0; s.marks = {}; s.prev = marks

    def page(s, kind="normal", section=""):
        if s.p: s.c.showPage()
        s.p += 1
        c = s.c
        if kind in ("title", "nofolio"):
            return left_x(s.p)
        c.saveState()
        c.setFont("Crimson", 9); c.setFillColor(MID)
        c.drawCentredString(left_x(s.p) + TW / 2, 0.40 * inch, str(s.p))
        if kind != "opener":
            c.setFont("PlayfairSC", 7.5)
            if s.p % 2 == 0: c.drawString(OUTER, H - 0.40 * inch, TITLE)
            else: c.drawRightString(W - OUTER, H - 0.40 * inch, section)
        c.restoreState()
        return left_x(s.p)

    def ref(s, k): return s.prev.get(k, 0)

    # ------------------------------------------------------------------ grids
    def grid(s, P, x, ytop, cell, solved=False):
        c = s.c
        g = P["grid"]
        used = set()
        if solved:
            for pl in P["placements"]:
                used |= set(word_cells(pl))
            # capsules round every hidden word
            c.setStrokeColor(LIGHT); c.setLineWidth(cell * 0.62); c.setLineCap(1)
            for pl in P["placements"]:
                cl = word_cells(pl)
                (r0, c0), (r1, c1) = cl[0], cl[-1]
                c.line(x + (c0 + 0.5) * cell, ytop - (r0 + 0.5) * cell, x + (c1 + 0.5) * cell, ytop - (r1 + 0.5) * cell)
            c.setStrokeColor(colors.white); c.setLineWidth(cell * 0.46)
            for pl in P["placements"]:
                cl = word_cells(pl)
                (r0, c0), (r1, c1) = cl[0], cl[-1]
                c.line(x + (c0 + 0.5) * cell, ytop - (r0 + 0.5) * cell, x + (c1 + 0.5) * cell, ytop - (r1 + 0.5) * cell)
            c.setLineCap(0)
        for r in range(N):
            for q in range(N):
                ch = g[r][q]
                cx, cy = x + (q + 0.5) * cell, ytop - (r + 0.5) * cell
                if solved and (r, q) not in used:
                    c.setFillColor(DARK); c.circle(cx, cy, cell * 0.42, stroke=0, fill=1)
                    c.setFillColor(colors.white); c.setFont("Plex-M", cell * 0.6)
                else:
                    c.setFillColor(MID if solved else INK); c.setFont("Plex-M" if not solved else "Plex", cell * 0.6)
                c.drawCentredString(cx, cy - cell * 0.21, ch)
        c.setStrokeColor(DARK); c.setLineWidth(1.0)
        c.roundRect(x - cell * 0.15, ytop - N * cell - cell * 0.15, N * cell + cell * 0.3, N * cell + cell * 0.3, cell * 0.3, stroke=1, fill=0)

    def word_list(s, words, x, ytop, width, cols=3, size=10):
        c = s.c
        rows = (len(words) + cols - 1) // cols
        cw = width / cols
        lead = size * 1.42
        for i, wd in enumerate(words):
            col, row = divmod(i, rows)
            wx, wy = x + col * cw + 12, ytop - (row + 1) * lead
            c.setStrokeColor(MID); c.setLineWidth(0.5); c.setFillColor(colors.white)
            c.rect(wx - 11, wy - 0.5, 6.5, 6.5, stroke=1, fill=0)
            c.setFillColor(INK); c.setFont("Plex", size); c.drawString(wx, wy, wd)
        return ytop - rows * lead

    # ------------------------------------------------------------------ front matter
    def title_page(s):
        c = s.c; x = s.page("title")
        draw_ill(c, "title", x, H - 3.0 * inch, TW, 1.7 * inch)
        c.setFillColor(MID); c.setFont("PlayfairSC", 11)
        c.drawCentredString(x + TW / 2, H - 3.55 * inch, "The")
        c.setFillColor(DARK); c.setFont("PlayfairSC-B", 30)
        c.drawCentredString(x + TW / 2, H - 4.05 * inch, "Thimble Hill")
        c.setFont("PlayfairSC-B", 21)
        c.drawCentredString(x + TW / 2, H - 4.45 * inch, "Word Search Mysteries")
        ornament(c, x + TW / 2, H - 4.75 * inch)
        c.setFont("Crimson-I", 13); c.setFillColor(INK)
        c.drawCentredString(x + TW / 2, H - 5.1 * inch, "60 cozy word searches, 10 gentle mysteries,")
        c.drawCentredString(x + TW / 2, H - 5.32 * inch, "and a clue hidden in every grid")
        c.setFont("PlayfairSC", 13); c.setFillColor(DARK)
        c.drawCentredString(x + TW / 2, BOT + 0.6 * inch, "Blake La Pierre")

    def copyright_page(s):
        c = s.c; x = s.page("nofolio")
        lines = ["The Thimble Hill Word Search Mysteries", "Copyright © 2026 Blake La Pierre. All rights reserved.", "",
                 "No part of this book may be reproduced in any form without written permission",
                 "from the author, except for brief quotations in reviews.", "",
                 "This is a work of fiction. Thimble Hill and everyone in it are made up,",
                 "and any resemblance to real people or places is coincidence.", "",
                 "Every grid was checked by computer: each listed word appears exactly once,",
                 "and the leftover letters spell the hidden clue exactly.", "",
                 "No one is ever hurt in Thimble Hill. Things go missing, and there is always a kind reason."]
        c.setFont("Crimson", 9.5); c.setFillColor(MID)
        y = BOT + 2.6 * inch
        for ln in lines:
            c.drawCentredString(x + TW / 2, y, ln); y -= 13

    def contents(s):
        c = s.c; x = s.page("nofolio")
        y = H - TOP - 0.3 * inch
        c.setFillColor(DARK); c.setFont("PlayfairSC-B", 22); c.drawCentredString(x + TW / 2, y, "Contents")
        ornament(c, x + TW / 2, y - 14)
        y -= 0.7 * inch
        rows = [("Welcome to Thimble Hill", "welcome"), ("How to Solve a Word Search Mystery", "howto")]
        for i, cs in enumerate(CASES):
            rows.append((f"Case {i + 1}: {cs['title']}", f"case{i}"))
        rows += [("Solutions", "solutions"), ("Case Answers", "answers")]
        for i, (t, k) in enumerate(rows):
            lv = None
            if t.startswith("Case ") and ":" in t:
                lv = CASES[int(t.split()[1][:-1]) - 1]["level_name"]
            c.setFont("Crimson", 11.5); c.setFillColor(INK)
            c.drawString(x, y, t)
            tw = pdfmetrics.stringWidth(t, "Crimson", 11.5)
            num = str(s.ref(k))
            nw = pdfmetrics.stringWidth(num, "Crimson", 11.5)
            if lv:
                c.setFont("Crimson-I", 9.5); c.setFillColor(MID)
                lvw = pdfmetrics.stringWidth(lv, "Crimson-I", 9.5)
                c.drawString(x + TW - nw - lvw - 10, y, lv)
                end = x + TW - nw - lvw - 16
            else:
                end = x + TW - nw - 6
            c.setFillColor(LIGHT); c.setFont("Crimson", 11.5)
            dx = x + tw + 6
            while dx < end - 3:
                c.drawString(dx, y, "."); dx += 5
            c.setFillColor(INK); c.drawRightString(x + TW, y, num)
            y -= 0.27 * inch if i not in (1, 11) else 0.4 * inch

    def welcome(s):
        c = s.c; x = s.page("normal", "Welcome"); s.marks["welcome"] = s.p
        y = H - TOP - 0.2 * inch
        c.setFillColor(DARK); c.setFont("PlayfairSC-B", 20); c.drawCentredString(x + TW / 2, y, "Welcome to Thimble Hill")
        ornament(c, x + TW / 2, y - 14)
        draw_ill(c, "frontispiece", x, y - 0.3 * inch - 3.0 * inch, TW, 3.0 * inch)
        y -= 3.5 * inch
        for t in [
            "Thimble Hill is a small village with one high street, one post office, a library, a bandstand and a great many cakes. "
            "Nothing terrible ever happens here. But things do go missing: a prize ribbon, a pie, a garden gnome, a song.",
            "When they do, people walk to the wool shop on the high street and knock on the door of <b>Hattie Bloom</b>. "
            "Hattie has knitted for sixty years and notices everything. She is helped, and sometimes hindered, by <b>Pickle</b>, "
            "a scruffy little terrier with a nose for trouble.",
            "In this book you are Hattie's partner. Every case has six word searches, and every word search hides one clue. "
            "Find the clues, cross off the suspects, and tell Hattie who did it. There is always a kind reason in the end.",
        ]:
            y = para(c, t, body, x, y, TW) - 7

    def howto(s):
        c = s.c; x = s.page("normal", "How to Solve"); s.marks["howto"] = s.p
        y = H - TOP - 0.2 * inch
        c.setFillColor(DARK); c.setFont("PlayfairSC-B", 18); c.drawCentredString(x + TW / 2, y, "How to Solve a Word Search Mystery")
        ornament(c, x + TW / 2, y - 14)
        y -= 0.45 * inch
        steps = [
            "<b>1. Read the case.</b> Each case opens with what went missing and the four suspects. Every suspect has something about them worth remembering.",
            "<b>2. Find every word.</b> Each grid hides the words in its list. Tick the little box as you find each one and draw a loop round it in the grid. "
            "Letters can be shared where two words cross.",
            "<b>3. Read the leftover letters.</b> When every word is found, some letters are left over. Read them in order, left to right along each row, "
            "starting with the top row. They spell out a clue. Write it in the boxes under the grid. The boxes show how many letters are in each word.",
            "<b>4. Solve the case.</b> After six grids you will have six clues. Turn to the Case Notes page, cross off the suspects the clues rule out, "
            "and write down who did it, and why you think so.",
            "<b>5. Check your answer.</b> The solved grids start on page %d and Hattie explains every case from page %d." % (s.ref("solutions"), s.ref("answers")),
        ]
        for t in steps:
            y = para(c, t, body, x, y, TW) - 6
        y -= 4
        c.setFillColor(DARK); c.setFont("PlayfairSC-B", 12); c.drawString(x, y - 8, "Three levels"); y -= 22
        for lv in ("Gentle", "Curious", "Sharp-Eyed"):
            dots(c, x + 4, y - 4, DOTS[lv])
            c.setFont("PlayfairSC", 10); c.setFillColor(DARK); c.drawString(x + 32, y - 7, lv)
            y = para(c, LEVEL_HELP[lv], body, x + 105, y + 4, TW - 105) - 6
        y -= 2
        y = para(c, "<i>Cases 1 to 3 are Gentle, cases 4 to 7 are Curious, and cases 8 to 10 are Sharp-Eyed. "
                    "The grids are all 12 by 12 squares. A sharp pencil and a soft eraser are the only tools you need.</i>", body, x, y, TW)

    # ------------------------------------------------------------------ case pages
    def case_opener(s, i, cs, txt):
        c = s.c; x = s.page("opener"); s.marks[f"case{i}"] = s.p
        y = H - TOP - 0.15 * inch
        c.setFillColor(MID); c.setFont("PlayfairSC", 11); c.drawCentredString(x + TW / 2, y, f"Case {WORDS[i + 1]}")
        c.setFillColor(DARK); c.setFont("PlayfairSC-B", 23 if len(cs["title"]) < 24 else 20)
        c.drawCentredString(x + TW / 2, y - 30, cs["title"])
        c.setFont("Crimson-I", 11.5); c.setFillColor(MID); c.drawCentredString(x + TW / 2, y - 48, txt["place"])
        ornament(c, x + TW / 2, y - 60)
        draw_ill(c, f"c{i + 1}", x, y - 70 - 2.0 * inch, TW, 2.0 * inch)
        y = y - 70 - 2.25 * inch
        y = para(c, txt["intro"], body, x, y, TW) - 10
        c.setFont("PlayfairSC", 9.5); c.setFillColor(MID)
        lv = cs["level_name"]
        c.drawCentredString(x + TW / 2 - 14, BOT + 0.3 * inch, f"Level: {lv}")
        dots(c, x + TW / 2 + pdfmetrics.stringWidth(f"Level: {lv}", "PlayfairSC", 9.5) / 2 - 6, BOT + 0.3 * inch + 3.3, DOTS[lv])
        assert y > BOT + 0.5 * inch, ("opener overflow", i)

    def suspects_page(s, i, cs, txt):
        c = s.c; x = s.page("normal", f"Case {i + 1}: {cs['title']}")
        y = H - TOP - 0.15 * inch
        c.setFillColor(DARK); c.setFont("PlayfairSC-B", 17); c.drawCentredString(x + TW / 2, y, "The Suspects")
        ornament(c, x + TW / 2, y - 13)
        y -= 0.45 * inch
        for name, desc in txt["suspects"]:
            c.setStrokeColor(DARK); c.setLineWidth(0.7); c.setFillColor(colors.white)
            c.rect(x, y - 12, 10, 10, stroke=1, fill=0)
            y2 = para(c, f"<b>{name}</b> {desc}", susp, x + 20, y, TW - 20)
            y = y2 - 12
        c.setFont("Crimson-I", 9.5); c.setFillColor(MID)
        c.drawString(x + 20, y, "Tick a box when a clue rules that suspect out.")
        y -= 0.35 * inch
        c.setFillColor(DARK); c.setFont("PlayfairSC-B", 12); c.drawString(x, y, "Notes"); y -= 8
        c.setStrokeColor(LIGHT); c.setLineWidth(0.5)
        while y > BOT + 0.3 * inch:
            y -= 0.3 * inch
            c.line(x, y, x + TW, y)

    def puzzle_page(s, i, cs, k, P, beat):
        c = s.c; x = s.page("normal", f"Case {i + 1}: {cs['title']}")
        top = H - TOP - 0.05 * inch
        c.setFillColor(DARK); c.setFont("PlayfairSC-B", 14)
        c.drawString(x, top - 10, f"Puzzle {P['id']}")
        c.setFont("PlayfairSC", 9.5); c.setFillColor(MID)
        c.drawRightString(x + TW - 30, top - 9, f"Clue {k + 1} of 6")
        dots(c, x + TW - 19, top - 5.5, DOTS[cs["level_name"]])
        y = para(c, beat, story, x, top - 20, TW) - 8
        cell = 0.30 * inch
        gw = cell * N
        gx = x + (TW - gw) / 2
        s.grid(P, gx, y - cell * 0.2, cell)
        y = y - gw - cell * 0.45
        y = s.word_list(P["words"], x + 0.1 * inch, y - 2, TW - 0.1 * inch, cols=3, size=9.6) - 10
        c.setFont("PlayfairSC", 8.5); c.setFillColor(MID)
        c.drawCentredString(x + TW / 2, y, "The leftover letters spell")
        y = clue_boxes(c, P["clue"], x, y - 5, TW)
        assert y > BOT - 2, ("puzzle overflow", P["id"], y)

    def notes_page(s, i, cs, txt):
        c = s.c; x = s.page("normal", f"Case {i + 1}: {cs['title']}")
        y = H - TOP - 0.15 * inch
        c.setFillColor(DARK); c.setFont("PlayfairSC-B", 17); c.drawCentredString(x + TW / 2, y, "Case Notes")
        ornament(c, x + TW / 2, y - 13)
        y -= 0.4 * inch
        c.setFont("Crimson-I", 10.5); c.setFillColor(MID)
        c.drawCentredString(x + TW / 2, y, f"Copy your six clues from puzzles {cs['puzzles'][0]['id']} to {cs['puzzles'][-1]['id']}.")
        y -= 0.25 * inch
        for k in range(6):
            c.setFillColor(DARK); c.setFont("PlayfairSC-B", 11); c.drawString(x, y - 0.22 * inch, f"{k + 1}.")
            c.setStrokeColor(LIGHT); c.setLineWidth(0.5); c.line(x + 18, y - 0.22 * inch, x + TW, y - 0.22 * inch)
            y -= 0.38 * inch
        y -= 0.15 * inch
        c.setFillColor(DARK); c.setFont("PlayfairSC-B", 12); c.drawString(x, y, "Ruled out"); y -= 6
        for name, _ in txt["suspects"]:
            y -= 0.27 * inch
            c.setStrokeColor(DARK); c.setLineWidth(0.7); c.setFillColor(colors.white); c.rect(x, y - 1, 9, 9, stroke=1, fill=0)
            c.setFillColor(INK); c.setFont("Crimson", 11); c.drawString(x + 16, y, name)
            c.setStrokeColor(LIGHT); c.setLineWidth(0.5); c.line(x + 18 + pdfmetrics.stringWidth(name, "Crimson", 11) + 8, y - 1, x + TW, y - 1)
        y -= 0.45 * inch
        c.setFillColor(DARK); c.setFont("PlayfairSC-B", 12); c.drawString(x, y, "Who did it, and why?")
        c.setStrokeColor(LIGHT); c.setLineWidth(0.5)
        y -= 0.05 * inch
        while y > BOT + 0.85 * inch:
            y -= 0.3 * inch; c.line(x, y, x + TW, y)
        c.setFont("Crimson-I", 9.5); c.setFillColor(MID)
        c.drawCentredString(x + TW / 2, BOT + 0.25 * inch, f"Check your answer with Hattie on page {s.ref('ans' + str(i))}.")

    # ------------------------------------------------------------------ back matter
    def solutions(s):
        c = s.c; x = s.page("opener"); s.marks["solutions"] = s.p
        y = H - TOP - 1.2 * inch
        c.setFillColor(DARK); c.setFont("PlayfairSC-B", 26); c.drawCentredString(x + TW / 2, y, "Solutions")
        ornament(c, x + TW / 2, y - 16)
        draw_ill(c, "opener-solutions", x, y - 0.4 * inch - 2.0 * inch, TW, 2.0 * inch)
        para(c, "Every hidden word is looped in gray. The leftover letters are the white letters on black circles: "
                "read them left to right along each row, from the top row down, to spell the clue printed under each grid.",
             body, x + 0.2 * inch, y - 2.7 * inch, TW - 0.4 * inch)
        allp = [(cs, P) for cs in CASES for P in cs["puzzles"]]
        cell = 0.18 * inch
        gw = cell * N
        for pg in range(0, len(allp), 4):
            x = s.page("normal", "Solutions")
            for j, (cs, P) in enumerate(allp[pg:pg + 4]):
                col, row = j % 2, j // 2
                cx = x + col * (TW / 2) + (TW / 2 - gw) / 2
                ty = H - TOP - 0.1 * inch - row * 3.8 * inch
                c.setFillColor(DARK); c.setFont("PlayfairSC-B", 10)
                c.drawCentredString(cx + gw / 2, ty - 8, f"Puzzle {P['id']}")
                s.grid(P, cx, ty - 0.3 * inch, cell, solved=True)
                yy = ty - 0.3 * inch - gw - 0.18 * inch
                p = Paragraph(f"<i>{P['clue'].capitalize()}</i>", ParagraphStyle("cl", parent=small, textColor=INK, fontSize=9.5, leading=11.5))
                _, hh = p.wrap(TW / 2 - 0.15 * inch, 200)
                p.drawOn(c, x + col * (TW / 2) + 0.075 * inch, yy - hh)

    def answers(s):
        c = s.c
        first = True
        y = None
        for i, cs in enumerate(CASES):
            txt = content.CASES[i]
            p1 = Paragraph(txt["solution"], body)
            _, hh = p1.wrap(TW, 10000)
            need = hh + 0.75 * inch
            if first or y - need < BOT:
                x = s.page("normal", "Case Answers")
                y = H - TOP - 0.1 * inch
                if first:
                    s.marks["answers"] = s.p
                    c.setFillColor(DARK); c.setFont("PlayfairSC-B", 20); c.drawCentredString(x + TW / 2, y - 8, "Case Answers")
                    ornament(c, x + TW / 2, y - 22)
                    y -= 0.55 * inch
                first = False
            s.marks["ans" + str(i)] = s.p
            c.setFillColor(MID); c.setFont("PlayfairSC", 9); c.drawString(x, y - 8, f"Case {i + 1}")
            c.setFillColor(DARK); c.setFont("PlayfairSC-B", 13); c.drawString(x + 45, y - 8, cs["title"])
            y -= 18
            c.setFont("Crimson-B", 11); c.setFillColor(INK)
            c.drawString(x, y - 10, f"It was {txt['culprit']}.")
            y -= 16
            y = para(c, txt["solution"], body, x, y, TW) - 0.3 * inch

    def thanks(s):
        c = s.c; x = s.page("normal", "Thank You")
        y = H - TOP - 0.8 * inch
        c.setFillColor(DARK); c.setFont("PlayfairSC-B", 20); c.drawCentredString(x + TW / 2, y, "Thank You for Visiting")
        ornament(c, x + TW / 2, y - 15)
        draw_ill(c, "thanks", x, y - 0.4 * inch - 2.2 * inch, TW, 2.2 * inch)
        y -= 2.9 * inch
        for t in ["Hattie and Pickle hope you enjoyed your time in Thimble Hill, and that the kettle stayed warm while you searched.",
                  "If you liked this book, a short review on Amazon helps other puzzlers find it, and it means a great deal to a small, independent author.",
                  "<i>Blake La Pierre</i>"]:
            y = para(c, t, ParagraphStyle("c", parent=body, alignment=TA_CENTER), x + 0.2 * inch, y, TW - 0.4 * inch) - 8

    def build(s):
        s.title_page(); s.copyright_page(); s.contents(); s.page("nofolio")  # blank verso
        s.welcome(); s.howto()
        for i, cs in enumerate(CASES):
            txt = content.CASES[i]
            assert txt["title"] == cs["title"]
            s.case_opener(i, cs, txt)
            s.suspects_page(i, cs, txt)
            for k, P in enumerate(cs["puzzles"]):
                assert P["clue"] == txt["beats"][k][1]
                s.puzzle_page(i, cs, k, P, txt["beats"][k][0])
            s.notes_page(i, cs, txt)
        if s.p % 2 == 1:
            s.page("nofolio")
        s.solutions(); s.answers(); s.thanks()
        while s.p % 2:
            s.page("nofolio")
        s.c.showPage(); s.c.save()
        return s.p


if __name__ == "__main__":
    out = os.path.join(ROOT, OUTNAME)
    marks = {}
    for _ in range(3):
        b = Book(out, marks); pages = b.build()
        if b.marks == marks: break
        marks = b.marks
    paper = 2.30 if 24 <= pages <= 110 else round(1.00 + 0.012 * pages, 3)
    info = dict(pages=pages, puzzles=60, cases=10, trim="6x9", printing_cost=paper,
                royalty_at_9_99=round(0.6 * 9.99 - paper, 3), marks=b.marks)
    json.dump(info, open(os.path.join(ROOT, "build-info.json"), "w"), indent=1)
    print(info["pages"], "pages; printing", paper, "royalty", info["royalty_at_9_99"])
