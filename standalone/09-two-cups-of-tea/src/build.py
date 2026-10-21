"""Build the 6x9 hardcover interior for Two Cups of Tea (B&W, white paper, no bleed, mirrored margins).
-> ../standalone-09-two-cups-of-tea-interior.pdf and ../build-info.json
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from PIL import Image
from content import (TITLE, SUBTITLE, TAGLINE, SEASONS, CHECKIN, INTERLUDES, STORY_SHARED,
                     FIRST_IMPRESSIONS, TODAY_ROWS, all_weeks)

G = "/usr/share/fonts/truetype/sand-box/google/"
for n, p in [("Crimson", "Crimson Text/CrimsonText-Regular.ttf"),
             ("Crimson-I", "Crimson Text/CrimsonText-Italic.ttf"),
             ("Crimson-B", "Crimson Text/CrimsonText-Bold.ttf"),
             ("PlayfairSC", "Playfair Display SC/PlayfairDisplaySC-Regular.ttf"),
             ("PlayfairSC-B", "Playfair Display SC/PlayfairDisplaySC-Bold.ttf"),
             ("Plex", "IBM Plex Sans Condensed/IBMPlexSansCondensed-Regular.ttf"),
             ("Plex-M", "IBM Plex Sans Condensed/IBMPlexSansCondensed-Medium.ttf")]:
    pdfmetrics.registerFont(TTFont(n, G + p))

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ILL = os.path.join(ROOT, "illustrations")
SLUG = "standalone-09-two-cups-of-tea"
OUT = os.path.join(ROOT, f"{SLUG}-interior.pdf")
W, H = 6 * inch, 9 * inch
# Mirrored margins. KDP hardcover minimums (no bleed): inside >= 0.375in for 24-150 pages,
# outside/top/bottom >= 0.25in. We use inside 0.75, outside 0.60, top 0.85, bottom 0.95.
MI, MO, MT, MB = 0.75 * inch, 0.60 * inch, 0.85 * inch, 0.95 * inch
HEADER_Y = H - 0.62 * inch
FOLIO_Y = 0.6 * inch
INK = colors.HexColor("#1a1a1a")
GREY = colors.HexColor("#6b6b6b")
RULE = colors.HexColor("#a8a8a8")
SEASON_VIG = {"spring": ["v-tulips", "v-can", "v-bird", "v-cupflowers"],
              "summer": ["v-basket", "v-kite", "v-lemonade", "v-boat"],
              "autumn": ["v-pumpkin", "v-leaves", "v-apples", "v-acorns"],
              "winter": ["v-mugs", "v-candle", "v-teapot", "v-mittens"]}
WORDS = {1: "One", 2: "Two", 3: "Three"}


class Book:
    def __init__(s):
        s.c = canvas.Canvas(OUT, pagesize=(W, H), initialFontName="Crimson", initialFontSize=11)
        s.c.setTitle(f"{TITLE}: {SUBTITLE}")
        s.c.setAuthor("Blake La Pierre")
        s.c.setSubject("Couple's question journal")
        s.page = 0
        s.marks = {}
        s.st = {
            "body": ParagraphStyle("body", fontName="Crimson", fontSize=11, leading=15.5, alignment=TA_JUSTIFY, textColor=INK),
            "q": ParagraphStyle("q", fontName="Crimson-B", fontSize=12.5, leading=15.5, alignment=TA_LEFT, textColor=INK),
            "cit": ParagraphStyle("cit", fontName="Crimson-I", fontSize=12, leading=16.5, alignment=TA_CENTER, textColor=INK),
            "it": ParagraphStyle("it", fontName="Crimson-I", fontSize=10.5, leading=14, alignment=TA_LEFT, textColor=INK),
            "quote": ParagraphStyle("quote", fontName="Crimson-I", fontSize=17, leading=23, alignment=TA_CENTER, textColor=INK),
        }

    # ---------- basics ----------
    def new(s, mark=None):
        if s.page:
            s.c.showPage()
        s.page += 1
        if mark:
            s.marks[mark] = s.page
        return s.page

    def box(s):
        odd = s.page % 2 == 1
        left = MI if odd else MO
        right = MO if odd else MI
        return left, W - right

    def folio(s):
        s.c.setFillColor(GREY); s.c.setFont("Plex", 8)
        s.c.drawCentredString(W / 2, FOLIO_Y, str(s.page))

    def header(s, text):
        s.c.setFillColor(GREY); s.c.setFont("PlayfairSC", 7.5)
        l, r = s.box()
        if s.page % 2 == 1:
            s.c.drawRightString(r, HEADER_Y, text.upper())
        else:
            s.c.drawString(l, HEADER_Y, text.upper())

    def running(s, right_text):
        s.header(TITLE if s.page % 2 == 0 else right_text)
        s.folio()

    def para(s, text, style, x, y, w):
        p = Paragraph(text, s.st[style] if isinstance(style, str) else style)
        _, fh = p.wrap(w, 1000)
        p.drawOn(s.c, x, y - fh)
        return y - fh

    def img(s, name, cx, top, max_w, max_h):
        path = os.path.join(ILL, f"{name}.png")
        iw, ih = Image.open(path).size
        dw = max_w; dh = dw * ih / iw
        if dh > max_h:
            dh = max_h; dw = dh * iw / ih
        s.c.drawImage(ImageReader(path), cx - dw / 2, top - dh, dw, dh, mask="auto")
        return dh

    def rules(s, x0, x1, y, n, gap=19):
        s.c.setStrokeColor(RULE); s.c.setLineWidth(0.6)
        for i in range(n):
            s.c.line(x0, y - i * gap, x1, y - i * gap)
        return y - (n - 1) * gap

    def ornament(s, cx, y, w=60):
        s.c.setStrokeColor(GREY); s.c.setLineWidth(0.6)
        s.c.line(cx - w, y, cx - 9, y); s.c.line(cx + 9, y, cx + w, y)
        s.heart(cx, y, 7)

    def heart(s, cx, cy, size, fill=True):
        import math
        p = s.c.beginPath()
        for i in range(41):
            t = 2 * math.pi * i / 40
            x = 16 * math.sin(t) ** 3; yy = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
            pt = (cx + x * size / 32, cy + yy * size / 32 - size * 0.05)
            p.moveTo(*pt) if i == 0 else p.lineTo(*pt)
        p.close()
        s.c.setFillColor(GREY if fill else colors.white); s.c.setStrokeColor(GREY); s.c.setLineWidth(0.5)
        s.c.drawPath(p, fill=1, stroke=1)

    def answer(s, who, x0, x1, top, n=4, gap=19):
        """An answer block for one partner: cup or mug icon, then n writing lines."""
        icon = "icon-teacup" if who == "teacup" else "icon-mug"
        s.img(icon, x0 + 9, top + 4, 19, 19)
        first = top - 10
        s.c.setStrokeColor(RULE); s.c.setLineWidth(0.6)
        s.c.line(x0 + 24, first, x1, first)
        for i in range(1, n):
            s.c.line(x0, first - i * gap, x1, first - i * gap)
        return first - (n - 1) * gap

    def question(s, label, text, x0, x1, top, n=4):
        s.c.setFillColor(GREY); s.c.setFont("PlayfairSC", 8)
        s.c.drawString(x0, top - 8, label.upper())
        y = s.para(text, "q", x0, top - 12, x1 - x0)
        y = s.answer("teacup", x0, x1, y - 16, n)
        y = s.answer("mug", x0, x1, y - 22, n)
        return y

    def checkbox(s, x, y, sz=8):
        s.c.setStrokeColor(INK); s.c.setLineWidth(0.7); s.c.setFillColor(colors.white)
        s.c.roundRect(x, y, sz, sz, 1.5, stroke=1, fill=1)

    def frame_box(s, x0, y0, x1, y1, r=6):
        s.c.setStrokeColor(GREY); s.c.setLineWidth(0.8); s.c.setFillColor(colors.white)
        s.c.roundRect(x0, y0, x1 - x0, y1 - y0, r, stroke=1, fill=0)

    def page_title(s, kicker, title, top=None):
        l, r = s.box(); cx = (l + r) / 2
        y = top or H - MT - 6
        if kicker:
            s.c.setFillColor(GREY); s.c.setFont("PlayfairSC", 9); s.c.drawCentredString(cx, y - 8, kicker.upper()); y -= 16
        s.c.setFillColor(INK); s.c.setFont("PlayfairSC-B", 20); s.c.drawCentredString(cx, y - 20, title)
        s.ornament(cx, y - 34)
        return y - 46

    # ---------- front matter ----------
    def half_title(s):
        s.new("half-title")
        s.c.setFillColor(INK); s.c.setFont("PlayfairSC-B", 24)
        s.c.drawCentredString(W / 2, H * 0.6, TITLE.upper())
        s.img("half-title", W / 2, H * 0.56, 2.6 * inch, 1.7 * inch)

    def frontis(s):
        s.new("frontispiece")
        s.img("frontispiece", W / 2 + 0.07 * inch, H - 0.8 * inch, 4.5 * inch, 6.6 * inch)
        s.c.setFont("Crimson-I", 10.5); s.c.setFillColor(GREY)
        s.c.drawCentredString(W / 2 + 0.07 * inch, 0.95 * inch, "A table for two, a pot of tea, and a whole year of conversations")

    def title_page(s):
        s.new("title")
        cx = W / 2 + 0.07 * inch
        s.c.setFillColor(GREY); s.c.setFont("PlayfairSC", 9.5)
        s.c.drawCentredString(cx, H - 1.25 * inch, "A COUPLE'S QUESTION JOURNAL")
        s.c.setFillColor(INK); s.c.setFont("PlayfairSC-B", 34)
        s.c.drawCentredString(cx, H - 2.0 * inch, "TWO CUPS")
        s.c.drawCentredString(cx, H - 2.55 * inch, "OF TEA")
        s.ornament(cx, H - 2.85 * inch, 80)
        s.c.setFont("Crimson-I", 13); s.c.drawCentredString(cx, H - 3.2 * inch, TAGLINE[0].upper() + TAGLINE[1:])
        s.img("title", cx, H - 3.6 * inch, 3.9 * inch, 1.9 * inch)
        s.c.setFont("PlayfairSC", 13); s.c.setFillColor(INK)
        s.c.drawCentredString(cx, 1.35 * inch, "BLAKE LA PIERRE")

    def copyright(s):
        s.new("copyright")
        l, r = s.box()
        y = 3.6 * inch
        s.c.setFont("Crimson-B", 11); s.c.setFillColor(INK); s.c.drawString(l, y, f"{TITLE}: {SUBTITLE}"); y -= 18
        s.c.setFont("Crimson", 10)
        for line in ["Copyright \u00a9 2026 Blake La Pierre", "All rights reserved.", "",
                     "No part of this book may be reproduced without permission,",
                     "except for brief quotations in reviews.", "",
                     "The questions, quotes and illustrations are original to this edition.",
                     "", "First edition, 2026."]:
            s.c.drawString(l, y, line); y -= 14

    def belongs(s):
        s.new("belongs")
        l, r = s.box(); cx = (l + r) / 2
        y = s.page_title("", "This Journal Belongs to Us", H - 1.4 * inch)
        y -= 30
        for who, label in (("teacup", "The Teacup"), ("mug", "The Mug")):
            s.img("icon-teacup" if who == "teacup" else "icon-mug", cx, y, 0.75 * inch, 0.75 * inch)
            y -= 0.75 * inch + 14
            s.c.setFont("PlayfairSC", 10); s.c.setFillColor(GREY); s.c.drawCentredString(cx, y, label.upper())
            y -= 28
            s.c.setStrokeColor(RULE); s.c.setLineWidth(0.6); s.c.line(cx - 1.5 * inch, y, cx + 1.5 * inch, y)
            y -= 40
        s.c.setFont("Crimson-I", 11.5); s.c.setFillColor(INK); s.c.drawCentredString(cx, y, "We started this journal on")
        y -= 30; s.c.line(cx - 1.5 * inch, y, cx + 1.5 * inch, y)
        s.heart(cx, y - 40, 12)

    def how_to(s):
        s.new("how-to")
        l, r = s.box()
        y = s.page_title("", "How to Use This Journal")
        y -= 8
        for t in [
            "This is a slow book. Each week brings one gentle theme and three questions, "
            "and every question has room for both of you to answer in your own words.",
            "Choose who is <b>the Teacup</b> and who is <b>the Mug</b>, and write your names on the page before. "
            "Then look for your little cup beside each answer space, so you always know where to write.",
            "Answer on your own first, without peeking, then swap and read. Or sit side by side "
            "with something warm and talk it through before you write. There is no wrong way.",
            "Each week ends with one small thing to do <i>together</i>: a walk, a recipe, a song. "
            "Tick the box when you have done it.",
            "The year is split into four seasons. Start in whichever season you are in, or simply at Week 1. "
            "At the end of every season there is a check-in, and at the end of the year, letters to each other.",
            "Skip a week if life gets busy. The questions will wait for you.",
        ]:
            y = s.para(t, "body", l, y, r - l) - 9
        s.img("v-cupflowers", (l + r) / 2, y - 6, 1.1 * inch, 1.1 * inch)
        s.folio()

    def contents(s):
        s.new("contents")
        l, r = s.box()
        y = s.page_title("", "Contents") - 10
        s.contents_y = y
        s.folio()

    def write_contents(s, c):
        pass  # contents are drawn in a second pass (see build)

    def our_story(s):
        s.new("our-story")
        l, r = s.box()
        y = s.page_title("Where it all began", "Our Story So Far")
        s.c.setFont("Crimson-I", 10.5); s.c.setFillColor(INK)
        s.c.drawCentredString((l + r) / 2, y, "Write these ones together.")
        y -= 20
        for p in STORY_SHARED:
            s.c.setFont("Crimson-B", 12.5); s.c.setFillColor(INK); s.c.drawString(l, y - 10, p)
            y = s.rules(l, r, y - 34, 5) - 30
        s.running("Our Story")
        s.new()
        l, r = s.box()
        y = s.page_title("", FIRST_IMPRESSIONS)
        y = s.answer("teacup", l, r, y - 10, 8)
        y = s.answer("mug", l, r, y - 34, 8)
        s.heart((l + r) / 2, y - 34, 12, fill=False)
        s.running("Our Story")

    def today(s):
        rows = TODAY_ROWS
        for half in (rows[:4], rows[4:]):
            s.new("today" if half is rows[:4] or "today" not in s.marks else None)
            l, r = s.box()
            y = s.page_title("A snapshot of right now", "Where We Are Today" if s.page % 2 == 0 else "Today, Continued")
            if s.page % 2 == 0:
                s.c.setFont("Crimson-I", 10.5); s.c.setFillColor(INK); s.c.drawString(l, y, "Date:"); s.c.setStrokeColor(RULE); s.c.line(l + 30, y - 2, l + 150, y - 2)
                y -= 26
            mid = (l + r) / 2
            for row in half:
                s.c.setFont("Crimson-B", 12.5); s.c.setFillColor(INK); s.c.drawString(l, y - 10, row)
                s.answer("teacup", l, mid - 10, y - 32, 3)
                y = s.answer("mug", mid + 10, r, y - 32, 3) - 34
            s.running("Where We Are Today")

    def bucket(s):
        s.new("bucket")
        l, r = s.box()
        y = s.page_title("Big dreams and small adventures", "Our Someday List") - 6
        for i in range(16):
            s.checkbox(l, y - 7)
            s.c.setStrokeColor(RULE); s.c.setLineWidth(0.6); s.c.line(l + 16, y - 7, r, y - 7)
            y -= 25
        s.running("Our Someday List")

    # ---------- seasons ----------
    def opener(s, sea):
        s.new(f"opener-{sea['id']}")
        l, r = s.box(); cx = (l + r) / 2
        s.c.setFillColor(GREY); s.c.setFont("PlayfairSC", 10); s.c.drawCentredString(cx, H - 1.15 * inch, sea["kicker"].upper())
        s.c.setFillColor(INK); s.c.setFont("PlayfairSC-B", 34); s.c.drawCentredString(cx, H - 1.7 * inch, sea["name"].upper())
        s.ornament(cx, H - 1.95 * inch, 70)
        dh = s.img(sea["art"], cx, H - 2.2 * inch, 4.3 * inch, 4.7 * inch)
        s.para(sea["blurb"], "cit", l + 0.25 * inch, H - 2.2 * inch - dh - 14, r - l - 0.5 * inch)

    def week(s, n, sea, theme, qs, together, vig):
        # left page
        s.new(f"week-{n}")
        l, r = s.box(); cx = (l + r) / 2
        top = H - MT
        s.c.setFillColor(GREY); s.c.setFont("PlayfairSC", 9); s.c.drawCentredString(cx, top - 8, f"WEEK {n}  \u00b7  {sea['name'].upper()}")
        s.c.setFillColor(INK); s.c.setFont("PlayfairSC-B", 19); s.c.drawCentredString(cx, top - 30, theme)
        s.ornament(cx, top - 42, 50)
        s.c.setFont("Crimson-I", 10.5); s.c.setFillColor(INK); s.c.drawCentredString(cx - 30, top - 62, "Week of")
        s.c.setStrokeColor(RULE); s.c.setLineWidth(0.6); s.c.line(cx - 8, top - 64, cx + 80, top - 64)
        y = top - 80
        y = s.question("Question One", qs[0], l, r, y, 4)
        y = s.question("Question Two", qs[1], l, r, y - 26, 4)
        s.running(sea["name"])
        # right page
        s.new()
        l, r = s.box(); cx = (l + r) / 2
        y = s.question("Question Three", qs[2], l, r, H - MT - 4, 5)
        y -= 28
        # together box
        p = Paragraph(together, s.st["it"]); _, ph = p.wrap(r - l - 50, 500)
        bh = ph + 40
        s.frame_box(l, y - bh, r, y)
        s.c.setFillColor(GREY); s.c.setFont("PlayfairSC", 8.5); s.c.drawString(l + 14, y - 16, "TOGETHER THIS WEEK")
        p.drawOn(s.c, l + 14, y - 24 - ph)
        s.checkbox(r - 24, y - 20, 10)
        y -= bh + 26
        s.c.setFont("Crimson-B", 12.5); s.c.setFillColor(INK); s.c.drawString(l, y - 10, "This week I appreciated\u2026")
        mid = (l + r) / 2
        s.answer("teacup", l, mid - 10, y - 32, 2)
        y = s.answer("mug", mid + 10, r, y - 32, 2) - 6
        avail = y - (MB + 4)
        if avail > 0.6 * inch:
            s.img(vig, cx, y - 12, 1.8 * inch, min(avail - 14, 1.3 * inch))
        s.running(sea["name"])

    def checkin(s, sea):
        s.new(f"checkin-{sea['id']}")
        l, r = s.box()
        y = s.page_title(f"End of {sea['name'].lower()}", "Season Check-In")
        mid = (l + r) / 2
        for i, p in enumerate(CHECKIN[sea["id"]]):
            s.c.setFont("Crimson-B", 12.5); s.c.setFillColor(INK); s.c.drawString(l, y - 10, p)
            if i == 3:
                s.answer("teacup", l, mid - 10, y - 32, 1)
                y = s.answer("mug", mid + 10, r, y - 32, 1) - 26
            else:
                y = s.answer("teacup", l, r, y - 32, 2)
                y = s.answer("mug", l, r, y - 22, 2) - 26
        s.running(sea["name"])
        s.new()
        l, r = s.box(); cx = (l + r) / 2
        y = s.page_title("", "A Memory to Keep")
        s.c.setFont("Crimson-I", 10.5); s.c.setFillColor(INK)
        s.c.drawCentredString(cx, y, "Tape in a photo or ticket stub, or draw a little picture.")
        y -= 14
        bh = 2.55 * inch
        s.frame_box(l + 0.2 * inch, y - bh, r - 0.2 * inch, y, 8)
        y -= bh + 22
        s.c.setFont("Crimson-B", 12.5); s.c.setFillColor(INK); s.c.drawString(l, y, "What was happening here")
        y = s.rules(l, r, y - 24, 4)
        s.img("checkin", cx, y - 14, 1.3 * inch, 0.78 * inch)
        s.running(sea["name"])

    def interlude(s, sea):
        art, quote, _ = INTERLUDES[sea["id"]]
        s.new(f"interlude-{sea['id']}")
        l, r = s.box(); cx = (l + r) / 2
        dh = s.img(art, cx, H - 1.15 * inch, 4.2 * inch, 4.6 * inch)
        y = H - 1.15 * inch - dh - 34
        s.ornament(cx, y + 10, 50)
        s.para(f"\u201c{quote}\u201d", "quote", l + 0.2 * inch, y - 8, r - l - 0.4 * inch)

    # ---------- end matter ----------
    def review(s):
        s.new("review")
        l, r = s.box()
        y = s.page_title("Looking back", "Our Year in Review")
        for p in ["My favourite memory of our year", "Something that surprised me about you", "What I'm proudest of us for"]:
            s.c.setFont("Crimson-B", 12.5); s.c.setFillColor(INK); s.c.drawString(l, y - 10, p)
            y = s.answer("teacup", l, r, y - 32, 2)
            y = s.answer("mug", l, r, y - 22, 2) - 26
        s.running("Year in Review")
        s.new()
        l, r = s.box(); cx = (l + r) / 2
        y = s.page_title("Looking ahead", "Wishes for Next Year")
        for p in ["One thing I hope we do next year", "A small habit I want to keep"]:
            s.c.setFont("Crimson-B", 12.5); s.c.setFillColor(INK); s.c.drawString(l, y - 10, p)
            y = s.answer("teacup", l, r, y - 32, 3)
            y = s.answer("mug", l, r, y - 22, 3) - 26
        s.img("review", cx, y - 4, r - l, 1.25 * inch)
        s.running("Year in Review")

    def letters(s):
        for who, label in (("teacup", "From the Teacup"), ("mug", "From the Mug")):
            s.new("letters" if who == "teacup" else None)
            l, r = s.box(); cx = (l + r) / 2
            y = s.page_title("A letter to you", label)
            s.img("letters", cx, y + 2, 1.2 * inch, 0.7 * inch)
            y -= 0.8 * inch
            s.c.setFont("Crimson-I", 12); s.c.setFillColor(INK); s.c.drawString(l, y - 10, "Dear")
            s.c.setStrokeColor(RULE); s.c.line(l + 28, y - 12, l + 160, y - 12)
            y = s.rules(l, r, y - 38, 15, 20)
            s.c.setFont("Crimson-I", 12); s.c.drawRightString(r - 110, y - 32, "With love,")
            s.c.line(r - 105, y - 34, r, y - 34)
            s.running("Letters")

    def notes(s):
        for i in range(2):
            s.new("notes" if i == 0 else None)
            l, r = s.box()
            y = s.page_title("", "Notes")
            s.rules(l, r, y - 6, 22, 20)
            s.running("Notes")

    def thanks(s):
        s.new("thanks")
        l, r = s.box(); cx = (l + r) / 2
        s.img("thanks", cx, H - 1.6 * inch, 3.0 * inch, 1.7 * inch)
        y = H - 3.6 * inch
        s.c.setFillColor(INK); s.c.setFont("PlayfairSC-B", 20); s.c.drawCentredString(cx, y, "Thank You")
        s.ornament(cx, y - 14)
        s.para("Thank you for sharing a year of questions with this little book. We hope it gave you "
               "plenty of slow mornings, long talks and new things to love about each other.", "cit", l + 0.2 * inch, y - 32, r - l - 0.4 * inch)
        s.para("If you enjoyed it, a short review on Amazon helps other couples find it, "
               "and it means a great deal to a small, independent author.", "cit", l + 0.2 * inch, y - 120, r - l - 0.4 * inch)
        s.c.setFont("PlayfairSC", 11); s.c.drawCentredString(cx, y - 210, "BLAKE LA PIERRE")

    def build(s):
        s.half_title(); s.frontis(); s.title_page(); s.copyright(); s.belongs(); s.how_to(); s.contents()
        s.our_story(); s.today(); s.bucket()
        weeks = list(all_weeks())
        for sea in SEASONS:
            s.opener(sea)
            vigs = SEASON_VIG[sea["id"]]
            for i, (n, se, theme, qs, tog) in enumerate([w for w in weeks if w[1] is sea]):
                s.week(n, se, theme, qs, tog, vigs[i % len(vigs)])
            s.checkin(sea)
            if sea["id"] in INTERLUDES:
                s.interlude(sea)
        s.review(); s.letters(); s.notes(); s.thanks()
        s.c.showPage(); s.c.save()
        return s.page, s.marks


def contents_entries(marks):
    e = [("Our Story So Far", marks["our-story"]), ("Where We Are Today", marks["today"]), ("Our Someday List", marks["bucket"])]
    for sea in SEASONS:
        e.append((f"{sea['kicker']}: {sea['name']}", marks[f"opener-{sea['id']}"]))
        e.append(("    Season Check-In", marks[f"checkin-{sea['id']}"]))
    e += [("Our Year in Review", marks["review"]), ("Letters to Each Other", marks["letters"]), ("Notes", marks["notes"])]
    return e


if __name__ == "__main__":
    # pass 1 to learn page numbers, pass 2 draws the contents
    b = Book(); pages, marks = b.build()
    entries = contents_entries(marks)

    orig = Book.contents
    def contents2(s):
        orig(s)
        l, r = s.box(); y = s.contents_y
        for name, pg in entries:
            sub = name.startswith("    ")
            s.c.setFont("Crimson-I" if sub else "Crimson", 11 if sub else 12.5); s.c.setFillColor(INK)
            x = l + (16 if sub else 0)
            s.c.drawString(x, y, name.strip())
            s.c.drawRightString(r, y, str(pg))
            tw = pdfmetrics.stringWidth(name.strip(), "Crimson-I" if sub else "Crimson", 11 if sub else 12.5)
            s.c.setStrokeColor(RULE); s.c.setDash(1, 3); s.c.line(x + tw + 6, y + 2, r - 20, y + 2); s.c.setDash()
            y -= 22 if not sub else 26
        s.img("icon-teacup", (l + r) / 2 - 18, y - 6, 30, 30); s.img("icon-mug", (l + r) / 2 + 18, y - 6, 30, 30)
    Book.contents = contents2
    b = Book(); pages2, marks2 = b.build()
    assert pages == pages2 and marks == marks2
    assert pages % 2 == 0, pages
    for k, v in marks.items():
        if k.startswith("week-") or k.startswith("checkin") or k in ("our-story", "review", "letters", "notes"):
            assert v % 2 == 0, (k, v)  # spreads start on a left-hand page
        if k.startswith("opener"):
            assert v % 2 == 1, (k, v)
    json.dump({"pages": pages, "marks": marks, "trim": "6x9", "bleed": False, "ink": "black", "paper": "white"},
              open(os.path.join(ROOT, "build-info.json"), "w"), indent=1)
    print("pages", pages, "->", OUT)
