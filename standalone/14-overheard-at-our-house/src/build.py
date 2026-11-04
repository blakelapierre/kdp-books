"""Build the 6x9 hardcover interior for Overheard at Our House (B&W, white paper, no bleed, mirrored margins).
-> ../standalone-14-overheard-at-our-house-interior.pdf and ../build-info.json
Layout and helpers follow standalone/12-twenty-five-christmases/src/build.py."""
import json, os, sys, math
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
from content import (TITLE, SUBTITLE, TAGLINE, CHAPTERS, INTERLUDES, PROMPTS, QUICK_KICKERS, INTRO,
                     SPEAKER_FIELDS, BACK, SURE_STARTS)

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
SLUG = "standalone-14-overheard-at-our-house"
OUT = os.path.join(ROOT, f"{SLUG}-interior.pdf")
W, H = 6 * inch, 9 * inch
# KDP hardcover minimums (no bleed): inside >= 0.375in for 24-150 pages, outside/top/bottom >= 0.25in.
MI, MO, MT, MB = 0.75 * inch, 0.60 * inch, 0.85 * inch, 0.95 * inch
HEADER_Y = H - 0.62 * inch
FOLIO_Y = 0.6 * inch
INK = colors.HexColor("#1a1a1a")
GREY = colors.HexColor("#6b6b6b")
RULE = colors.HexColor("#a8a8a8")
VIGS = ["v-teddy", "v-blocks", "v-duck", "v-plane", "v-crayons", "v-balloons", "v-wagon", "v-kite", "v-bucket",
        "v-books", "v-cat", "v-bird", "v-car", "v-bed", "v-mug", "v-gift"]
PAGES = 108


class Book:
    def __init__(s):
        s.c = canvas.Canvas(OUT, pagesize=(W, H), initialFontName="Crimson", initialFontSize=11)
        s.c.setTitle(f"{TITLE}: {SUBTITLE}")
        s.c.setAuthor("Blake La Pierre")
        s.c.setSubject("Kids quote keepsake journal")
        s.page = 0
        s.marks = {}
        s.st = {
            "body": ParagraphStyle("body", fontName="Crimson", fontSize=11, leading=15.5, alignment=TA_JUSTIFY, textColor=INK),
            "q": ParagraphStyle("q", fontName="Crimson-B", fontSize=12, leading=15, alignment=TA_LEFT, textColor=INK),
            "cit": ParagraphStyle("cit", fontName="Crimson-I", fontSize=12, leading=16.5, alignment=TA_CENTER, textColor=INK),
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
        return (MI if odd else MO), W - (MO if odd else MI)

    def folio(s):
        s.c.setFillColor(GREY); s.c.setFont("Plex", 8)
        s.c.drawCentredString(W / 2, FOLIO_Y, str(s.page))

    def header(s, text):
        s.c.setFillColor(GREY); s.c.setFont("PlayfairSC", 7.5)
        l, r = s.box()
        (s.c.drawRightString(r, HEADER_Y, text.upper()) if s.page % 2 == 1 else s.c.drawString(l, HEADER_Y, text.upper()))

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

    def star(s, cx, cy, r, fill=True):
        p = s.c.beginPath()
        for i in range(10):
            a = math.pi / 2 + math.pi / 5 * i; rr = r if i % 2 == 0 else r * 0.42
            pt = (cx + rr * math.cos(a), cy + rr * math.sin(a))
            p.moveTo(*pt) if i == 0 else p.lineTo(*pt)
        p.close()
        s.c.setFillColor(GREY if fill else colors.white); s.c.setStrokeColor(GREY); s.c.setLineWidth(0.5)
        s.c.drawPath(p, fill=1, stroke=1)

    def ornament(s, cx, y, w=60):
        s.c.setStrokeColor(GREY); s.c.setLineWidth(0.6)
        s.c.line(cx - w, y, cx - 10, y); s.c.line(cx + 10, y, cx + w, y)
        s.star(cx, y, 5.5)

    def checkbox(s, x, y, sz=8):
        s.c.setStrokeColor(INK); s.c.setLineWidth(0.7); s.c.setFillColor(colors.white)
        s.c.roundRect(x, y, sz, sz, 1.5, stroke=1, fill=1)

    def label(s, x, y, text, size=8):
        s.c.setFillColor(GREY); s.c.setFont("PlayfairSC", size); s.c.drawString(x, y, text.upper())

    def section(s, x0, x1, top, title):
        """Small-caps section label with a short rule after it; returns y below."""
        s.c.setFillColor(INK); s.c.setFont("PlayfairSC-B", 11); s.c.drawString(x0, top - 11, title)
        tw = pdfmetrics.stringWidth(title, "PlayfairSC-B", 11)
        s.c.setStrokeColor(GREY); s.c.setLineWidth(0.5); s.c.line(x0 + tw + 8, top - 7, x1, top - 7)
        s.star(x1 - 3, top - 7, 3, fill=False)
        return top - 18

    def field(s, x0, x1, y, text):
        """Inline label followed by a writing line."""
        s.c.setFillColor(INK); s.c.setFont("Crimson-I", 11); s.c.drawString(x0, y + 3, text)
        tw = pdfmetrics.stringWidth(text, "Crimson-I", 11)
        s.c.setStrokeColor(RULE); s.c.setLineWidth(0.6); s.c.line(x0 + tw + 6, y, x1, y)

    def page_title(s, kicker, title, top=None):
        l, r = s.box(); cx = (l + r) / 2
        y = top or H - MT - 6
        if kicker:
            s.c.setFillColor(GREY); s.c.setFont("PlayfairSC", 9); s.c.drawCentredString(cx, y - 8, kicker.upper()); y -= 16
        sz = 20
        while pdfmetrics.stringWidth(title, "PlayfairSC-B", sz) > r - l: sz -= 0.5
        s.c.setFillColor(INK); s.c.setFont("PlayfairSC-B", sz); s.c.drawCentredString(cx, y - 20, title)
        s.ornament(cx, y - 34)
        return y - 46

    def bubble(s, x0, y0, x1, y1, tail="l", lw=0.9, rad=14):
        """Speech-bubble frame; tail hangs below the bottom edge."""
        c = s.c
        c.setStrokeColor(INK); c.setLineWidth(lw); c.setFillColor(colors.white)
        c.roundRect(x0, y0, x1 - x0, y1 - y0, rad, stroke=1, fill=1)
        tx = x0 + 0.16 * (x1 - x0) if tail == "l" else x1 - 0.16 * (x1 - x0)
        d = -1 if tail == "l" else 1
        p = c.beginPath(); p.moveTo(tx - 9, y0); p.lineTo(tx + d * 14, y0 - 16); p.lineTo(tx + 9, y0)
        c.drawPath(p, stroke=1, fill=1)
        c.setStrokeColor(colors.white); c.setLineWidth(lw + 1.2); c.line(tx - 9 + lw, y0, tx + 9 - lw, y0)

    def quote_marks(s, x, y, size=30):
        s.c.setFillColor(RULE); s.c.setFont("PlayfairSC-B", size); s.c.drawString(x, y, "\u201c")

    # ---------- front matter ----------
    def half_title(s):
        s.new("half-title")
        s.c.setFillColor(INK); s.c.setFont("PlayfairSC-B", 21)
        s.c.drawCentredString(W / 2 + 0.07 * inch, H * 0.6, TITLE.upper())
        s.img("half-title", W / 2 + 0.07 * inch, H * 0.57, 2.0 * inch, 1.3 * inch)

    def frontis(s):
        s.new("frontispiece")
        cx = W / 2 - 0.07 * inch
        s.img("frontispiece", cx, H - 1.6 * inch, 4.5 * inch, 4.4 * inch)
        s.c.setFont("Crimson-I", 11); s.c.setFillColor(GREY)
        s.c.drawCentredString(cx, 1.9 * inch, "A small house, a full garden,")
        s.c.drawCentredString(cx, 1.9 * inch - 15, "and something wonderful said every single day")

    def title_page(s):
        s.new("title")
        cx = W / 2 + 0.07 * inch
        s.c.setFillColor(GREY); s.c.setFont("PlayfairSC", 9.5)
        s.c.drawCentredString(cx, H - 1.25 * inch, TAGLINE.upper())
        s.c.setFillColor(INK); s.c.setFont("PlayfairSC-B", 34)
        s.c.drawCentredString(cx, H - 2.0 * inch, "OVERHEARD")
        s.c.setFont("PlayfairSC-B", 24)
        s.c.drawCentredString(cx, H - 2.45 * inch, "AT OUR HOUSE")
        s.ornament(cx, H - 2.75 * inch, 80)
        s.c.setFont("Crimson-I", 13)
        s.c.drawCentredString(cx, H - 3.1 * inch, "The funny, sweet and surprising things")
        s.c.drawCentredString(cx, H - 3.1 * inch - 16, "our kids say, written down before we forget")
        s.img("title", cx, H - 3.75 * inch, 4.0 * inch, 1.45 * inch)
        s.c.setFont("PlayfairSC", 13); s.c.setFillColor(INK)
        s.c.drawCentredString(cx, 1.35 * inch, "BLAKE LA PIERRE")

    def copyright(s):
        s.new("copyright")
        l, r = s.box()
        y = 3.6 * inch
        s.c.setFont("Crimson-B", 11); s.c.setFillColor(INK); s.c.drawString(l, y, TITLE); y -= 14
        s.c.setFont("Crimson-I", 10); s.c.drawString(l, y, "A Keepsake Journal of the Funny, Sweet and"); y -= 13
        s.c.drawString(l, y, "Surprising Things Our Kids Say"); y -= 18
        s.c.setFont("Crimson", 10)
        for line in ["Copyright \u00a9 2026 Blake La Pierre", "All rights reserved.", "",
                     "No part of this book may be reproduced without permission,",
                     "except for brief quotations in reviews.", "",
                     "The prompts and illustrations are original to this edition.",
                     "", "First edition, 2026."]:
            s.c.drawString(l, y, line); y -= 14

    def belongs(s):
        s.new("belongs")
        l, r = s.box(); cx = (l + r) / 2
        y = s.page_title("", "Overheard at Our House", H - 1.3 * inch)
        y -= 14
        s.img("belongs", cx, y, 2.3 * inch, 2.3 * inch)
        y -= 2.3 * inch + 26
        s.c.setFont("PlayfairSC", 10); s.c.setFillColor(GREY); s.c.drawCentredString(cx, y, "THE THINGS OUR KIDS SAY, KEPT BY THE")
        y -= 34; s.c.setStrokeColor(RULE); s.c.setLineWidth(0.6); s.c.line(cx - 1.6 * inch, y, cx + 1.6 * inch, y)
        y -= 14; s.c.setFont("PlayfairSC", 10); s.c.setFillColor(GREY); s.c.drawCentredString(cx, y, "FAMILY")
        y -= 40
        s.c.setFont("Crimson-I", 12); s.c.setFillColor(INK); s.c.drawCentredString(cx, y, "We started writing on")
        y -= 30; s.c.line(cx - 1.6 * inch, y, cx + 1.6 * inch, y)
        s.star(cx, y - 30, 8)

    def how_to(s):
        s.new("how-to")
        l, r = s.box()
        y = s.page_title("", "How to Use This Book")
        y -= 8
        for t in INTRO:
            y = s.para(t, "body", l, y, r - l) - 9
        s.img("v-crayons", (l + r) / 2, y - 2, 1.2 * inch, 0.85 * inch)
        s.folio()

    def contents(s):
        s.new("contents")
        l, r = s.box()
        s.contents_y = s.page_title("", "Contents") - 10
        s.folio()

    def speakers(s):
        s.new("speakers")
        l, r = s.box()
        y = s.page_title("Meet the", "Little Speakers")
        gap = 10; cw = (r - l - gap) / 2; ch = 142
        for i in range(6):
            col, row = i % 2, i // 2
            x0 = l + col * (cw + gap); top = y - 4 - row * (ch + gap)
            s.c.setStrokeColor(GREY); s.c.setLineWidth(0.7); s.c.roundRect(x0, top - ch, cw, ch, 8, stroke=1, fill=0)
            yy = top - 24
            for f in SPEAKER_FIELDS:
                s.c.setFont("Crimson-I", 10); s.c.setFillColor(INK); s.c.drawString(x0 + 8, yy + 3, f)
                tw = pdfmetrics.stringWidth(f, "Crimson-I", 10)
                s.c.setStrokeColor(RULE); s.c.setLineWidth(0.6)
                if tw + 14 > cw - 30:
                    yy -= 15; s.c.line(x0 + 8, yy, x0 + cw - 8, yy)
                else:
                    s.c.line(x0 + 14 + tw, yy, x0 + cw - 8, yy)
                yy -= 24
        s.running("The Little Speakers")

    def first_words(s):
        s.new("first-words")
        l, r = s.box()
        y = s.page_title("Where It All Began", "Their First Words")
        cols = [l, l + (r - l) * 0.27, l + (r - l) * 0.58, l + (r - l) * 0.72, r]
        for i, t in enumerate(["Name", "First word", "Age", "Who heard it"]):
            s.label(cols[i] + (0 if i == 0 else 4), y - 4, t)
        y -= 10
        s.c.setStrokeColor(RULE); s.c.setLineWidth(0.6)
        n = 8
        for i in range(n): s.c.line(l, y - 24 * (i + 1), r, y - 24 * (i + 1))
        for x in cols[1:4]: s.c.line(x, y - 2, x, y - 24 * n)
        y -= 24 * n + 26
        y = s.section(l, r, y, "Words they said their own way")
        y = s.rules(l, r, y - 14, 5, 20) - 10
        s.img("speakers", (l + r) / 2, y, r - l, 0.75 * inch)
        s.running("First Words")

    # ---------- chapters ----------
    def interlude(s, ch):
        s.new(f"interlude-{ch['id']}")
        l, r = s.box(); cx = (l + r) / 2
        q, art = INTERLUDES[ch["id"]]
        s.img(art, cx, H * 0.68, 1.9 * inch, 1.7 * inch)
        s.ornament(cx, H * 0.68 + 22, 50)
        s.para(q, "quote", l + 0.2 * inch, H * 0.68 - 1.9 * inch, r - l - 0.4 * inch)
        s.folio()

    def opener(s, ch):
        s.new(f"opener-{ch['id']}")
        l, r = s.box(); cx = (l + r) / 2
        s.c.setFillColor(GREY); s.c.setFont("PlayfairSC", 10)
        s.c.drawCentredString(cx, H - 1.15 * inch, f"CHAPTER {['', 'ONE', 'TWO', 'THREE', 'FOUR'][ch['id']]}")
        sz = 26
        while pdfmetrics.stringWidth(ch["name"], "PlayfairSC-B", sz) > r - l - 0.2 * inch: sz -= 1
        s.c.setFillColor(INK); s.c.setFont("PlayfairSC-B", sz); s.c.drawCentredString(cx, H - 1.65 * inch, ch["name"])
        s.ornament(cx, H - 1.9 * inch, 70)
        s.img(ch["art"], cx, H - 2.15 * inch, 4.4 * inch, 4.2 * inch)
        s.para(ch["line"], "cit", l + 0.25 * inch, 1.75 * inch, r - l - 0.5 * inch)

    def big_page(s, ch, prompt, vig):
        """One big quote with its story (even page)."""
        s.new(); s.big_count += 1
        l, r = s.box(); cx = (l + r) / 2
        y = H - MT - 4
        s.c.setFillColor(GREY); s.c.setFont("PlayfairSC", 8.5); s.c.drawCentredString(cx, y - 8, "OVERHEARD")
        s.c.setFillColor(INK); s.c.setFont("Crimson-I", 16); s.c.drawCentredString(cx, y - 27, prompt)
        s.ornament(cx, y - 40, 60)
        y -= 54
        bh = 2.2 * inch
        s.bubble(l + 2, y - bh, r - 2, y, tail="l")
        s.quote_marks(l + 12, y - 30)
        s.rules(l + 34, r - 16, y - 34, 5, 25)
        y -= bh + 34
        mid = l + (r - l) * 0.64
        s.field(l, mid - 10, y, "Who said it"); s.field(mid + 4, r, y, "Age"); y -= 26
        s.field(l, mid - 10, y, "Where we were"); s.field(mid + 4, r, y, "Date"); y -= 30
        y = s.section(l, r, y, "What was happening")
        y = s.rules(l, r, y - 14, 3, 20) - 24
        y = s.section(l, r, y, "What we said back")
        yb = s.rules(l, r - 1.05 * inch, y - 14, 3, 20)
        s.img(vig, r - 0.48 * inch, y - 2, 0.95 * inch, 0.82 * inch)
        s.running(ch["name"])

    def quick_page(s, ch, kicker):
        """Three quick quotes (odd page)."""
        s.new(); s.quick_count += 3
        l, r = s.box(); cx = (l + r) / 2
        y = H - MT - 4
        s.c.setFillColor(GREY); s.c.setFont("PlayfairSC", 8.5); s.c.drawCentredString(cx, y - 8, kicker.upper())
        y -= 20
        slot = (y - MB) / 3
        for i in range(3):
            top = y - i * slot
            tail = "l" if i % 2 == 0 else "r"
            bh = 72
            s.bubble(l + 2, top - bh, r - 2, top - 4, tail=tail, rad=11)
            s.quote_marks(l + 10, top - 30, 24)
            s.rules(l + 30, r - 14, top - 30, 3, 20)
            yy = top - bh - 30
            x1 = l + (r - l) * 0.5; x2 = l + (r - l) * 0.72
            s.field(l, x1 - 8, yy, "Who"); s.field(x1, x2 - 8, yy, "Age"); s.field(x2, r, yy, "Date")
            yy -= 24
            s.field(l, r, yy, "The story behind it")
        s.running(ch["name"])

    # ---------- back matter ----------
    def back_title(s, key):
        kicker, title, note = BACK[key]
        l, r = s.box()
        y = s.page_title(kicker, title)
        s.para(note, "cit", l, y, r - l)
        return y - 38

    def dictionary(s):
        for p in range(2):
            s.new("dictionary" if p == 0 else None)
            l, r = s.box()
            y = s.back_title("dictionary") if p == 0 else H - MT - 4
            cols = [l, l + (r - l) * 0.3, l + (r - l) * 0.76, r]
            s.label(cols[0], y - 4, "Their word"); s.label(cols[1] + 4, y - 4, "What it meant"); s.label(cols[2] + 4, y - 4, "Who, age")
            y -= 10
            n = 12 if p == 0 else 15
            gap = 30
            s.c.setStrokeColor(RULE); s.c.setLineWidth(0.6)
            for i in range(n): s.c.line(l, y - gap * (i + 1), r, y - gap * (i + 1))
            for x in cols[1:3]: s.c.line(x, y - 2, x, y - gap * n)
            if p == 1:
                s.img("dictionary", (l + r) / 2, y - gap * n - 8, 1.8 * inch, 0.62 * inch)
            s.running("Family Dictionary")

    def questions(s):
        for p in range(2):
            s.new("questions" if p == 0 else None)
            l, r = s.box()
            y = s.back_title("questions") if p == 0 else H - MT - 4
            n = 3 if p == 0 else 5
            for i in range(n):
                s.c.setFont("PlayfairSC-B", 13); s.c.setFillColor(INK); s.c.drawString(l, y - 12, "?")
                s.field(l + 14, r, y - 12, "They asked"); s.rules(l + 14, r, y - 34, 1)
                s.field(l + 14, r, y - 58, "We said"); s.rules(l + 14, r, y - 80, 1)
                y -= 104
            if p == 0:
                s.img("questions", (l + r) / 2, y + 6, 2.2 * inch, 0.6 * inch)
            s.running("Big Questions")

    def sure(s):
        for p in range(2):
            s.new("sure" if p == 0 else None)
            l, r = s.box()
            y = s.back_title("sure") if p == 0 else H - MT - 4
            items = SURE_STARTS[:6] if p == 0 else SURE_STARTS[6:]
            for t in items:
                if t:
                    s.c.setFont("Crimson-I", 11); s.c.setFillColor(INK); s.c.drawString(l, y - 12, t)
                    tw = pdfmetrics.stringWidth(t, "Crimson-I", 11)
                    s.c.setStrokeColor(RULE); s.c.setLineWidth(0.6); s.c.line(l + tw + 6, y - 15, r, y - 15)
                else:
                    s.rules(l, r, y - 15, 1)
                s.rules(l, r, y - 35, 1)
                s.c.setFont("Crimson-I", 9); s.c.setFillColor(GREY); s.c.drawRightString(r, y - 49, "who, and how old")
                s.c.setStrokeColor(RULE); s.c.line(r - 2.0 * inch, y - 51, r - 0.95 * inch, y - 51)
                y -= 64
            if p == 0:
                s.img("sure", (l + r) / 2, y + 8, 1.4 * inch, 0.65 * inch)
            s.running("Absolutely Sure")

    def jokes(s):
        for p in range(2):
            s.new("jokes" if p == 0 else None)
            l, r = s.box()
            y = s.back_title("jokes") if p == 0 else H - MT - 4
            n = 3 if p == 0 else 4
            for i in range(n):
                s.field(l, r, y - 12, "The joke"); s.rules(l, r, y - 32, 1)
                s.field(l, r, y - 54, "The punchline")
                yy = y - 78
                s.field(l, l + (r - l) * 0.55, yy, "Told by")
                x = l + (r - l) * 0.6
                for t in ["Hilarious", "Huh?"]:
                    s.checkbox(x, yy + 1, 8); s.c.setFont("Crimson", 10); s.c.setFillColor(INK); s.c.drawString(x + 11, yy + 2, t)
                    x += 18 + pdfmetrics.stringWidth(t, "Crimson", 10) + 6
                y -= 108
            if p == 0:
                s.img("jokes", (l + r) / 2, y + 4, 2.0 * inch, 0.75 * inch)
            s.running("Jokes They Told")

    def talk(s):
        for p in range(4):
            s.new("talk" if p == 0 else None)
            l, r = s.box()
            y = s.back_title("talk") if p == 0 else H - MT - 4
            for half in range(1 if p == 0 else 2):
                mid = l + (r - l) * 0.6
                s.field(l, mid - 8, y - 6, "Who was talking"); s.field(mid + 4, r, y - 6, "When")
                y -= 30
                n = 8 if p == 0 else 9
                for i in range(n):
                    s.c.setStrokeColor(RULE); s.c.setLineWidth(0.6)
                    s.c.line(l, y, l + 0.75 * inch, y)
                    s.c.setFont("Crimson-B", 11); s.c.setFillColor(GREY); s.c.drawString(l + 0.78 * inch, y + 2, ":")
                    s.c.line(l + 0.9 * inch, y, r, y)
                    y -= 22
                y -= 8
                if half == 0 and p > 0:
                    s.ornament((l + r) / 2, y + 2, 50); y -= 18
            if p == 0:
                s.img("talk", (l + r) / 2, y, 2.0 * inch, 0.95 * inch)
            s.running("Conversations")

    def letter(s):
        for i in range(2):
            s.new("letter" if i == 0 else None)
            l, r = s.box(); cx = (l + r) / 2
            if i == 0:
                y = s.back_title("letter")
                s.field(l, r, y, "Dear"); y -= 26
                s.rules(l, r, y, 17, 20)
            else:
                y = H - MT - 10
                y = s.rules(l, r, y, 18, 20) - 22
                s.field(l, r, y, "With love,")
                s.img("letters", cx, y - 18, 1.6 * inch, 0.95 * inch)
            s.running("A Letter")

    def notes(s):
        for i in range(4):
            s.new("notes" if i == 0 else None)
            l, r = s.box()
            y = s.page_title("", "Notes") if i == 0 else H - MT - 4
            n = 22 if i == 0 else 26
            s.rules(l, r, y - 6, n, 20)
            s.running("Notes")

    def thanks(s):
        s.new("thanks")
        l, r = s.box(); cx = (l + r) / 2
        s.img("thanks", cx, H - 1.6 * inch, 3.2 * inch, 1.6 * inch)
        y = H - 3.6 * inch
        s.c.setFillColor(INK); s.c.setFont("PlayfairSC-B", 20); s.c.drawCentredString(cx, y, "Thank You")
        s.ornament(cx, y - 14)
        s.para("Thank you for keeping your children's words in this little book. We hope it fills up with "
               "the kind of lines your family will be quoting at birthdays and weddings for years to come.", "cit", l + 0.2 * inch, y - 32, r - l - 0.4 * inch)
        s.para("If you enjoyed it, a short review on Amazon helps other families find it, "
               "and it means a great deal to a small, independent author.", "cit", l + 0.2 * inch, y - 120, r - l - 0.4 * inch)
        s.c.setFont("PlayfairSC", 11); s.c.setFillColor(INK); s.c.drawCentredString(cx, y - 210, "BLAKE LA PIERRE")

    def build(s):
        s.big_count = 0; s.quick_count = 0
        s.half_title(); s.frontis(); s.title_page(); s.copyright(); s.belongs(); s.how_to(); s.contents()
        s.speakers(); s.first_words()
        k = 0
        for ch in CHAPTERS:
            s.interlude(ch); s.opener(ch)
            s.marks[f"entries-{ch['id']}"] = s.page + 1
            for i, prompt in enumerate(PROMPTS[ch["id"]]):
                s.big_page(ch, prompt, VIGS[k % len(VIGS)])
                s.quick_page(ch, QUICK_KICKERS[(k + ch["id"]) % len(QUICK_KICKERS)])
                k += 1
        s.dictionary(); s.questions(); s.sure(); s.jokes(); s.talk(); s.letter(); s.notes(); s.thanks()
        s.c.showPage(); s.c.save()
        return s.page, s.marks


def contents_entries(marks):
    e = [("Meet the Little Speakers", marks["speakers"]), ("Their First Words", marks["first-words"])]
    for ch in CHAPTERS:
        e.append((f"{ch['id']}. {ch['name']}", marks[f"opener-{ch['id']}"]))
    e += [("Our Family Dictionary", marks["dictionary"]), ("Big Questions They Asked", marks["questions"]),
          ("Things They Were Absolutely Sure Of", marks["sure"]), ("Jokes They Told", marks["jokes"]),
          ("Conversations Worth Keeping", marks["talk"]), ("A Letter for When You're Grown", marks["letter"]),
          ("Notes", marks["notes"])]
    return e


if __name__ == "__main__":
    b = Book(); pages, marks = b.build()
    entries = contents_entries(marks)
    orig = Book.contents
    def contents2(s):
        orig(s)
        l, r = s.box(); y = s.contents_y
        for name, pg in entries:
            f, sz = "Crimson", 12.5
            s.c.setFont(f, sz); s.c.setFillColor(INK)
            s.c.drawString(l, y, name); s.c.drawRightString(r, y, str(pg))
            tw = pdfmetrics.stringWidth(name, f, sz)
            s.c.setStrokeColor(RULE); s.c.setDash(1, 3); s.c.line(l + tw + 6, y + 2, r - 20, y + 2); s.c.setDash()
            y -= 27
        s.img("v-teddy", (l + r) / 2, y - 4, 1.1 * inch, 0.9 * inch)
    Book.contents = contents2
    b = Book(); pages2, marks2 = b.build()
    assert pages == pages2 and marks == marks2
    assert pages == PAGES, pages
    assert b.big_count == 36 and b.quick_count == 108, (b.big_count, b.quick_count)
    for k, v in marks.items():
        if k.startswith(("interlude", "speakers", "dictionary", "questions", "sure", "jokes", "talk", "letter", "notes", "entries")):
            assert v % 2 == 0, (k, v)
        if k.startswith("opener"):
            assert v % 2 == 1, (k, v)
    assert [marks[f"interlude-{i}"] for i in range(1, 5)] == [10, 30, 50, 70], marks
    json.dump({"pages": pages, "marks": marks, "quote_spaces": b.big_count + b.quick_count, "trim": "6x9", "bleed": False,
               "ink": "black", "paper": "white"}, open(os.path.join(ROOT, "build-info.json"), "w"), indent=1)
    print("pages", pages, "quotes", b.big_count + b.quick_count, "->", OUT)
