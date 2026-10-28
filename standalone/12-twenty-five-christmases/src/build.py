"""Build the 6x9 hardcover interior for Twenty-Five Christmases (B&W, white paper, no bleed, mirrored margins).
-> ../standalone-12-twenty-five-christmases-interior.pdf and ../build-info.json
Layout and helpers follow standalone/09-two-cups-of-tea/src/build.py."""
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
from content import (TITLE, SUBTITLE, TAGLINE, YEARS, CHAPTERS, INTERLUDES, QUESTIONS, WEATHER,
                     TRADITIONS, MENU_ROWS, TREE_ROWS)

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
SLUG = "standalone-12-twenty-five-christmases"
OUT = os.path.join(ROOT, f"{SLUG}-interior.pdf")
W, H = 6 * inch, 9 * inch
# KDP hardcover minimums (no bleed): inside >= 0.375in for 24-150 pages, outside/top/bottom >= 0.25in.
MI, MO, MT, MB = 0.75 * inch, 0.60 * inch, 0.85 * inch, 0.95 * inch
HEADER_Y = H - 0.62 * inch
FOLIO_Y = 0.6 * inch
INK = colors.HexColor("#1a1a1a")
GREY = colors.HexColor("#6b6b6b")
RULE = colors.HexColor("#a8a8a8")
VIGS = ["v-wreath", "v-gifts", "v-holly", "v-bells", "v-gingerbread", "v-canes", "v-cones", "v-snowman",
        "v-cocoa", "v-tree", "v-baubles", "v-candles", "v-house", "v-globe", "v-stocking"]
NUM = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve",
       "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen", "Twenty",
       "Twenty-One", "Twenty-Two", "Twenty-Three", "Twenty-Four", "Twenty-Five"]


class Book:
    def __init__(s):
        s.c = canvas.Canvas(OUT, pagesize=(W, H), initialFontName="Crimson", initialFontSize=11)
        s.c.setTitle(f"{TITLE}: {SUBTITLE}")
        s.c.setAuthor("Blake La Pierre")
        s.c.setSubject("Family Christmas memory book")
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
        s.c.setFillColor(INK); s.c.setFont("PlayfairSC-B", 20); s.c.drawCentredString(cx, y - 20, title)
        s.ornament(cx, y - 34)
        return y - 46

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
        s.c.drawCentredString(cx, 1.9 * inch, "The tree, the fire, the stockings in a row,")
        s.c.drawCentredString(cx, 1.9 * inch - 15, "and twenty-five Christmases still to come")

    def title_page(s):
        s.new("title")
        cx = W / 2 + 0.07 * inch
        s.c.setFillColor(GREY); s.c.setFont("PlayfairSC", 9.5)
        s.c.drawCentredString(cx, H - 1.25 * inch, TAGLINE.upper())
        s.c.setFillColor(INK); s.c.setFont("PlayfairSC-B", 34)
        s.c.drawCentredString(cx, H - 2.0 * inch, "TWENTY-FIVE")
        s.c.drawCentredString(cx, H - 2.55 * inch, "CHRISTMASES")
        s.ornament(cx, H - 2.85 * inch, 80)
        s.c.setFont("Crimson-I", 13)
        s.c.drawCentredString(cx, H - 3.2 * inch, "Traditions, photos, gifts and moments to keep, year by year")
        s.img("title", cx, H - 3.55 * inch, 3.9 * inch, 1.4 * inch)
        s.c.setFont("PlayfairSC", 13); s.c.setFillColor(INK)
        s.c.drawCentredString(cx, 1.35 * inch, "BLAKE LA PIERRE")

    def copyright(s):
        s.new("copyright")
        l, r = s.box()
        y = 3.6 * inch
        s.c.setFont("Crimson-B", 11); s.c.setFillColor(INK); s.c.drawString(l, y, TITLE); y -= 14
        s.c.setFont("Crimson-I", 10); s.c.drawString(l, y, "A Family Christmas Memory Book to Fill In Year by Year"); y -= 18
        s.c.setFont("Crimson", 10)
        for line in ["Copyright \u00a9 2026 Blake La Pierre", "All rights reserved.", "",
                     "No part of this book may be reproduced without permission,",
                     "except for brief quotations in reviews.", "",
                     "The prompts, quotes and illustrations are original to this edition.",
                     "", "First edition, 2026."]:
            s.c.drawString(l, y, line); y -= 14

    def belongs(s):
        s.new("belongs")
        l, r = s.box(); cx = (l + r) / 2
        y = s.page_title("", "Our Family Christmas Book", H - 1.3 * inch)
        y -= 14
        s.img("belongs", cx, y, 2.1 * inch, 2.1 * inch)
        y -= 2.1 * inch + 26
        s.c.setFont("PlayfairSC", 10); s.c.setFillColor(GREY); s.c.drawCentredString(cx, y, "THIS BOOK BELONGS TO THE")
        y -= 34; s.c.setStrokeColor(RULE); s.c.setLineWidth(0.6); s.c.line(cx - 1.6 * inch, y, cx + 1.6 * inch, y)
        y -= 14; s.c.setFont("PlayfairSC", 10); s.c.setFillColor(GREY); s.c.drawCentredString(cx, y, "FAMILY")
        y -= 40
        s.c.setFont("Crimson-I", 12); s.c.setFillColor(INK); s.c.drawCentredString(cx, y, "Our first Christmas in this book was")
        y -= 30; s.c.line(cx - 1.6 * inch, y, cx + 1.6 * inch, y)
        s.star(cx, y - 30, 8)

    def how_to(s):
        s.new("how-to")
        l, r = s.box()
        y = s.page_title("", "How to Use This Book")
        y -= 8
        for t in [
            "This book holds <b>twenty-five Christmases</b>, one after another. Each Christmas has four pages "
            "of its own: a page for a photo or this year's Christmas card, a page for who was here and how the tree looked, "
            "a page for Christmas morning and the meal, and a page for gifts, the best moment and a wish for next year.",
            "Fill in the year at the top of each Christmas. Start this year, whatever year it is, and simply keep going.",
            "Write a little on Christmas night, or on a slow day before New Year, while the memories are still fresh. "
            "Pass the pen around: let grandparents, parents and children each add a line in their own handwriting.",
            "Every Christmas has one question of its own, so no two years look quite the same.",
            "At the front are pages for your family traditions and for the family as it is today. At the back you will find "
            "all twenty-five Christmases at a glance, pages for treasured recipes, and letters to the family of the future.",
            "Use a ballpoint or fine-liner pen, and a glue stick or photo corners for pictures.",
        ]:
            y = s.para(t, "body", l, y, r - l) - 9
        s.img("v-cocoa", (l + r) / 2, y - 4, 1.2 * inch, 0.9 * inch)
        s.folio()

    def contents(s):
        s.new("contents")
        l, r = s.box()
        s.contents_y = s.page_title("", "Contents") - 10
        s.folio()

    def traditions(s):
        s.new("traditions")
        l, r = s.box()
        y = s.page_title("Our Family", "Christmas Traditions")
        s.para("Tick the traditions that belong to your family, and add the year you began them.", "cit", l, y, r - l)
        y -= 44
        for t in TRADITIONS:
            s.checkbox(l, y - 1, 9)
            s.c.setFont("Crimson", 11.5); s.c.setFillColor(INK); s.c.drawString(l + 16, y, t)
            s.c.setFont("Crimson-I", 9.5); s.c.setFillColor(GREY); s.c.drawRightString(r - 44, y, "since")
            s.c.setStrokeColor(RULE); s.c.setLineWidth(0.6); s.c.line(r - 40, y - 1, r, y - 1)
            y -= 20.5
        s.running("Traditions")
        s.new()
        l, r = s.box()
        y = s.page_title("Our Family", "Traditions All Our Own")
        y = s.section(l, r, y - 4, "Traditions only our family has")
        y = s.rules(l, r, y - 14, 7, 20) - 18
        y = s.section(l, r, y, "How they began")
        y = s.rules(l, r, y - 14, 6, 20) - 18
        y = s.section(l, r, y, "One we would like to start")
        s.rules(l, r, y - 14, 3, 20)
        s.running("Traditions")

    def family(s):
        s.new("family")
        l, r = s.box()
        y = s.page_title("When We Began This Book", "Our Family")
        cols = [l, l + (r - l) * 0.58, l + (r - l) * 0.78, r]
        s.label(cols[0], y - 4, "Name"); s.label(cols[1] + 4, y - 4, "Age"); s.label(cols[2] + 4, y - 4, "Role")
        y -= 12
        s.c.setStrokeColor(RULE); s.c.setLineWidth(0.6)
        for i in range(12):
            yy = y - 22 * (i + 1); s.c.line(l, yy, r, yy)
        for x in cols[1:3]: s.c.line(x, y - 4, x, y - 22 * 12)
        y -= 22 * 12 + 28
        y = s.section(l, r, y, "Where we live")
        s.rules(l, r, y - 14, 3, 20)
        s.running("Our Family")
        s.new()
        l, r = s.box()
        y = s.page_title("When We Began This Book", "A Family Photo")
        fh = 3.3 * inch
        s.photo_frame(l, y - fh - 4, r, y - 4, "a family photo")
        y -= fh + 26
        y = s.section(l, r, y, "What we love most about Christmas")
        s.rules(l, r, y - 14, 5, 20)
        s.running("Our Family")

    def photo_frame(s, x0, y0, x1, y1, what="a photo or this year's Christmas card"):
        c = s.c
        c.setStrokeColor(GREY); c.setLineWidth(0.9); c.rect(x0, y0, x1 - x0, y1 - y0, stroke=1, fill=0)
        c.setLineWidth(0.4); c.rect(x0 + 4, y0 + 4, x1 - x0 - 8, y1 - y0 - 8, stroke=1, fill=0)
        # photo corners
        k = 16
        c.setFillColor(colors.HexColor("#d9d9d9")); c.setStrokeColor(GREY); c.setLineWidth(0.5)
        for (cx, cy, sx, sy) in [(x0 + 10, y0 + 10, 1, 1), (x1 - 10, y0 + 10, -1, 1), (x0 + 10, y1 - 10, 1, -1), (x1 - 10, y1 - 10, -1, -1)]:
            p = c.beginPath(); p.moveTo(cx, cy); p.lineTo(cx + sx * k, cy); p.lineTo(cx, cy + sy * k); p.close(); c.drawPath(p, stroke=1, fill=1)
        c.setFillColor(GREY); c.setFont("Crimson-I", 10.5)
        c.drawCentredString((x0 + x1) / 2, (y0 + y1) / 2 - 4, f"Paste {what} here")
        s.star((x0 + x1) / 2, (y0 + y1) / 2 + 14, 5, fill=False)

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
        a, b = ch["years"]
        s.c.setFillColor(GREY); s.c.setFont("PlayfairSC", 10)
        s.c.drawCentredString(cx, H - 1.15 * inch, f"CHRISTMASES {a} TO {b}")
        sz = 26
        while pdfmetrics.stringWidth(ch["name"], "PlayfairSC-B", sz) > r - l - 0.2 * inch: sz -= 1
        s.c.setFillColor(INK); s.c.setFont("PlayfairSC-B", sz); s.c.drawCentredString(cx, H - 1.65 * inch, ch["name"])
        s.ornament(cx, H - 1.9 * inch, 70)
        s.img(ch["art"], cx, H - 2.15 * inch, 4.4 * inch, 4.4 * inch)
        s.para(ch["line"], "cit", l + 0.25 * inch, 1.75 * inch, r - l - 0.5 * inch)

    def year(s, n):
        hdr = f"Christmas {n}"
        vig = VIGS[(n - 1) % len(VIGS)]
        # --- A: photo page (left)
        s.new(f"year-{n}")
        l, r = s.box(); cx = (l + r) / 2
        y = H - MT - 4
        s.c.setFillColor(GREY); s.c.setFont("PlayfairSC", 9); s.c.drawCentredString(cx, y - 8, f"CHRISTMAS NUMBER {NUM[n].upper()}")
        s.c.setFillColor(INK); s.c.setFont("PlayfairSC-B", 24)
        txt = "Christmas"; tw = pdfmetrics.stringWidth(txt, "PlayfairSC-B", 24)
        lw = 1.15 * inch; x = cx - (tw + 8 + lw) / 2
        s.c.drawString(x, y - 38, txt)
        s.c.setStrokeColor(INK); s.c.setLineWidth(0.8); s.c.line(x + tw + 8, y - 38, x + tw + 8 + lw, y - 38)
        s.ornament(cx, y - 52, 70)
        y -= 64
        fh = 3.35 * inch
        s.photo_frame(l, y - fh, r, y)
        y -= fh + 24
        s.field(l, r, y, "In the picture"); y -= 21
        s.rules(l, r, y, 1); y -= 26
        s.field(l, r, y, "Where we celebrated"); y -= 30
        s.label(l, y, "The weather on Christmas Day"); y -= 18
        x = l
        for wtxt in WEATHER:
            s.checkbox(x, y - 1, 8); s.c.setFont("Crimson", 10.5); s.c.setFillColor(INK); s.c.drawString(x + 12, y, wtxt)
            x += 12 + pdfmetrics.stringWidth(wtxt, "Crimson", 10.5) + 12
        s.running(hdr)
        # --- B: who was here, the tree, Christmas Eve (right)
        s.new()
        l, r = s.box()
        y = H - MT - 4
        y = s.section(l, r, y, "Who Was Here")
        mid = (l + r) / 2
        s.c.setStrokeColor(RULE); s.c.setLineWidth(0.6)
        for i in range(6):
            yy = y - 16 - i * 20; s.c.line(l, yy, mid - 8, yy); s.c.line(mid + 8, yy, r, yy)
        y -= 16 + 5 * 20 + 26
        y = s.section(l, r, y, "Our Tree This Year")
        y -= 14
        for t in TREE_ROWS:
            s.field(l, r, y, t); y -= 22
        y -= 10
        y = s.section(l, r, y, "Christmas Eve")
        s.c.setFont("Crimson-I", 10); s.c.setFillColor(GREY); s.c.drawString(l, y - 10, "Where we were, what we did, how we waited")
        y = s.rules(l, r, y - 30, 6, 20) - 24
        y = s.section(l, r, y, "Cards, Calls and Visitors")
        s.rules(l, r, y - 16, 3, 20)
        s.running(hdr)
        # --- C: Christmas morning, the table, this year's question (left)
        s.new()
        l, r = s.box()
        y = H - MT - 4
        y = s.section(l, r, y, "Christmas Morning")
        y = s.rules(l, r, y - 16, 5, 20) - 26
        y = s.section(l, r, y, "On the Table")
        y -= 14
        for t in MENU_ROWS:
            s.field(l, r, y, t); y -= 22
        y -= 10
        y = s.section(l, r, y, "This Year's Question")
        y = s.para(QUESTIONS[n - 1], "q", l, y - 4, r - l - 1.0 * inch)
        y = s.rules(l, r - 1.05 * inch, y - 16, 4, 20)
        s.img(vig, r - 0.48 * inch, y + 72, 0.95 * inch, 0.95 * inch)
        y = s.section(l, r, y - 26, "Songs, Films and Stories")
        s.rules(l, r, y - 16, 2, 20)
        s.running(hdr)
        # --- D: gifts, best moment, laughs, wish (right)
        s.new()
        l, r = s.box()
        y = H - MT - 4
        y = s.section(l, r, y, "Gifts to Remember")
        cols = [l, l + (r - l) * 0.27, l + (r - l) * 0.5, r]
        y -= 12
        s.label(cols[0], y, "From"); s.label(cols[1] + 4, y, "To"); s.label(cols[2] + 4, y, "The gift")
        s.c.setStrokeColor(RULE); s.c.setLineWidth(0.6)
        for i in range(7):
            yy = y - 20 * (i + 1); s.c.line(l, yy, r, yy)
        for x in cols[1:3]: s.c.line(x, y - 4, x, y - 140)
        y -= 140 + 26
        y = s.section(l, r, y, "The Best Moment")
        y = s.rules(l, r, y - 16, 4, 20) - 24
        y = s.section(l, r, y, "Something That Made Us Laugh")
        y = s.rules(l, r, y - 16, 3, 20) - 24
        y = s.section(l, r, y, "A Wish for Next Christmas")
        y = s.rules(l, r, y - 16, 2, 20)
        s.running(hdr)

    # ---------- back matter ----------
    def glance(s):
        for half, rng in ((0, range(1, 14)), (1, range(14, 26))):
            s.new("glance" if half == 0 else None)
            l, r = s.box()
            y = s.page_title("Twenty-Five Christmases", "At a Glance")
            cols = [l, l + 30, l + 74, l + (r - l) * 0.55, r]
            s.label(cols[0], y - 2, "No."); s.label(cols[1] + 3, y - 2, "Year"); s.label(cols[2] + 3, y - 2, "Where we were"); s.label(cols[3] + 3, y - 2, "One word for it")
            y -= 8
            gap = 31
            s.c.setStrokeColor(RULE); s.c.setLineWidth(0.6)
            for i, n in enumerate(rng):
                yy = y - gap * (i + 1)
                s.c.line(l, yy, r, yy)
                s.c.setFont("PlayfairSC-B", 11); s.c.setFillColor(INK); s.c.drawCentredString(l + 13, yy + 9, str(n))
            nrows = len(rng)
            for x in cols[1:4]: s.c.line(x, y, x, y - gap * nrows)
            if half == 1:
                s.img("glance", (l + r) / 2, y - gap * nrows - 12, 3.6 * inch, 0.8 * inch)
            s.running("At a Glance")

    def recipes(s):
        for i in range(4):
            s.new("recipes" if i == 0 else None)
            l, r = s.box()
            y = s.page_title("From Our Kitchen", "A Christmas Recipe")
            s.field(l, r, y - 6, "Recipe"); y -= 28
            s.field(l, r, y, "From the kitchen of"); y -= 28
            s.field(l, (l + r) / 2 - 8, y, "Serves"); s.field((l + r) / 2 + 8, r, y, "Time"); y -= 30
            y = s.section(l, r, y, "Ingredients")
            mid = (l + r) / 2
            s.c.setStrokeColor(RULE); s.c.setLineWidth(0.6)
            for k in range(6):
                yy = y - 16 - 20 * k; s.c.line(l, yy, mid - 8, yy); s.c.line(mid + 8, yy, r, yy)
            y -= 16 + 100 + 26
            y = s.section(l, r, y, "Method")
            y = s.rules(l, r, y - 16, 8, 20)
            if i == 3:
                pass
            s.running("Recipes")

    def letters(s):
        for i in range(2):
            s.new("letters" if i == 0 else None)
            l, r = s.box(); cx = (l + r) / 2
            if i == 0:
                y = s.page_title("", "A Letter to Our Future Family")
                s.para("Write to whoever opens this book twenty-five Christmases from now.", "cit", l, y, r - l)
                y -= 40
                s.field(l, r, y, "Written on"); y -= 26
                s.rules(l, r, y, 17, 20)
            else:
                y = H - MT - 10
                y = s.rules(l, r, y, 19, 20)
                s.img("letters", cx, y - 14, 1.6 * inch, 1.0 * inch)
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
        s.img("thanks", cx, H - 1.6 * inch, 3.0 * inch, 1.5 * inch)
        y = H - 3.6 * inch
        s.c.setFillColor(INK); s.c.setFont("PlayfairSC-B", 20); s.c.drawCentredString(cx, y, "Thank You")
        s.ornament(cx, y - 14)
        s.para("Thank you for keeping your family's Christmases in this little book. We hope it fills up with "
               "photos, handwriting and stories that your family will love to read again every December.", "cit", l + 0.2 * inch, y - 32, r - l - 0.4 * inch)
        s.para("If you enjoyed it, a short review on Amazon helps other families find it, "
               "and it means a great deal to a small, independent author.", "cit", l + 0.2 * inch, y - 120, r - l - 0.4 * inch)
        s.c.setFont("PlayfairSC", 11); s.c.setFillColor(INK); s.c.drawCentredString(cx, y - 210, "BLAKE LA PIERRE")

    def build(s):
        s.half_title(); s.frontis(); s.title_page(); s.copyright(); s.belongs(); s.how_to(); s.contents()
        s.traditions(); s.family()
        for ch in CHAPTERS:
            s.interlude(ch); s.opener(ch)
            a, b = ch["years"]
            for n in range(a, b + 1):
                s.year(n)
        s.glance(); s.recipes(); s.letters(); s.notes(); s.thanks()
        s.c.showPage(); s.c.save()
        return s.page, s.marks


def contents_entries(marks):
    e = [("Our Christmas Traditions", marks["traditions"]), ("Our Family", marks["family"])]
    for ch in CHAPTERS:
        a, b = ch["years"]
        e.append((ch["name"], marks[f"opener-{ch['id']}"]))
        e.append((f"    Christmases {a} to {b}", marks[f"year-{a}"]))
    e += [("Twenty-Five Christmases at a Glance", marks["glance"]), ("Family Christmas Recipes", marks["recipes"]),
          ("A Letter to Our Future Family", marks["letters"]), ("Notes", marks["notes"])]
    return e


if __name__ == "__main__":
    b = Book(); pages, marks = b.build()
    entries = contents_entries(marks)
    orig = Book.contents
    def contents2(s):
        orig(s)
        l, r = s.box(); y = s.contents_y
        for name, pg in entries:
            sub = name.startswith("    ")
            f, sz = ("Crimson-I", 11) if sub else ("Crimson", 12.5)
            s.c.setFont(f, sz); s.c.setFillColor(INK)
            x = l + (16 if sub else 0)
            s.c.drawString(x, y, name.strip()); s.c.drawRightString(r, y, str(pg))
            tw = pdfmetrics.stringWidth(name.strip(), f, sz)
            s.c.setStrokeColor(RULE); s.c.setDash(1, 3); s.c.line(x + tw + 6, y + 2, r - 20, y + 2); s.c.setDash()
            y -= 20 if not sub else 26
        s.img("v-holly", (l + r) / 2, y - 4, 1.0 * inch, 0.7 * inch)
    Book.contents = contents2
    b = Book(); pages2, marks2 = b.build()
    assert pages == pages2 and marks == marks2
    assert pages % 2 == 0, pages
    for k, v in marks.items():
        if k.startswith(("year-", "interlude", "traditions", "family", "glance", "recipes", "letters", "notes")):
            assert v % 2 == 0, (k, v)
        if k.startswith("opener"):
            assert v % 2 == 1, (k, v)
    json.dump({"pages": pages, "marks": marks, "trim": "6x9", "bleed": False, "ink": "black", "paper": "white"},
              open(os.path.join(ROOT, "build-info.json"), "w"), indent=1)
    print("pages", pages, "->", OUT)
