"""Build 6x9 interior PDF for Stories We Keep (B&W, no bleed, mirrored margins).
-> ../standalone-06-stories-we-keep-interior.pdf and ../build-info.json
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from content import TITLE, SUBTITLE, TAGLINE, SECTIONS, FAMILY_TREE_NOTE, TIMELINE_NOTE, EXTRA_NOTE

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
OUT = os.path.join(ROOT, "standalone-06-stories-we-keep-interior.pdf")
W, H = 6 * inch, 9 * inch
# mirrored margins: inside 0.75, outside 0.55, top 0.70, bottom 0.75
MI, MO, MT, MB = 0.75 * inch, 0.55 * inch, 0.70 * inch, 0.75 * inch

def margins(page_num):
    """Odd pages = right-hand = outside on the right."""
    odd = (page_num % 2 == 1)
    left = MI if odd else MO
    right = MO if odd else MI
    return left, right

def ill(name):
    return ImageReader(os.path.join(ILL, f"{name}.png"))

class Book:
    def __init__(s):
        s.c = canvas.Canvas(OUT, pagesize=(W, H))
        s.c.setTitle(f"{TITLE}: {SUBTITLE}")
        s.c.setAuthor("Blake La Pierre")
        s.c.setSubject("Guided memory keepsake journal")
        s.page = 0
        s.marks = {}
        s.body = ParagraphStyle("body", fontName="Crimson", fontSize=11, leading=15, alignment=TA_JUSTIFY)
        s.italic = ParagraphStyle("it", fontName="Crimson-I", fontSize=11, leading=15, alignment=TA_LEFT)
        s.center_it = ParagraphStyle("cit", fontName="Crimson-I", fontSize=12, leading=16, alignment=TA_CENTER)
        s.prompt_q = ParagraphStyle("pq", fontName="Crimson-B", fontSize=13, leading=17, alignment=TA_LEFT)
        s.prompt_h = ParagraphStyle("ph", fontName="Crimson-I", fontSize=10.5, leading=14, alignment=TA_LEFT)
        s.small = ParagraphStyle("sm", fontName="Crimson", fontSize=10, leading=13, alignment=TA_LEFT)

    def new(s, kind="content"):
        if s.page:
            s.c.showPage()
        s.page += 1
        return s.page

    def folio(s):
        s.c.setFillColor(colors.HexColor("#666666"))
        s.c.setFont("Plex", 8)
        s.c.drawCentredString(W / 2, 0.40 * inch, str(s.page))

    def header(s, text):
        s.c.setFillColor(colors.HexColor("#888888"))
        s.c.setFont("PlayfairSC", 7)
        left, right = margins(s.page)
        if s.page % 2 == 1:
            s.c.drawRightString(W - right, H - 0.42 * inch, text.upper())
        else:
            s.c.drawString(left, H - 0.42 * inch, text.upper())

    def content_box(s):
        left, right = margins(s.page)
        return left, MB, W - left - right, H - MT - MB

    def lines(s, x, y, w, n, gap=18):
        s.c.setStrokeColor(colors.HexColor("#bbbbbb"))
        s.c.setLineWidth(0.6)
        for i in range(n):
            yy = y - i * gap
            s.c.line(x, yy, x + w, yy)
        return y - n * gap

    def para(s, text, style, x, y, w, h=200):
        p = Paragraph(text, style)
        fw, fh = p.wrap(w, h)
        p.drawOn(s.c, x, y - fh)
        return y - fh

    def draw_img(s, name, x, y, max_w, max_h):
        path = os.path.join(ILL, f"{name}.png")
        from PIL import Image
        im = Image.open(path)
        iw, ih = im.size
        aspect = ih / iw
        dw = max_w
        dh = dw * aspect
        if dh > max_h:
            dh = max_h
            dw = dh / aspect
        s.c.drawImage(ImageReader(path), x + (max_w - dw) / 2, y - dh, dw, dh, mask="auto")
        return dh

    def blank_vignette(s):
        s.new("blank")
        s.draw_img("v-lamp", W / 2 - 0.7 * inch, H / 2 + 1.0 * inch, 1.4 * inch, 2.0 * inch)

    def half_title(s):
        s.new("title"); s.marks["half-title"] = s.page
        s.c.setFillColor(colors.black)
        s.c.setFont("PlayfairSC-B", 22)
        s.c.drawCentredString(W / 2, H * 0.62, TITLE.upper())
        s.draw_img("half-title", W / 2 - 1.6 * inch, H * 0.55, 3.2 * inch, 2.0 * inch)

    def frontis(s):
        s.new("nofolio"); s.marks["frontispiece"] = s.page
        dh = s.draw_img("frontispiece", 0.7 * inch, H - 0.85 * inch, 4.6 * inch, 6.4 * inch)
        s.c.setFont("Crimson-I", 10)
        s.c.setFillColor(colors.HexColor("#444444"))
        s.c.drawCentredString(W / 2, 0.85 * inch, "A house, a lamp, and stories waiting to be written")

    def title_page(s):
        s.new("title"); s.marks["title"] = s.page
        s.c.setFillColor(colors.HexColor("#666666"))
        s.c.setFont("PlayfairSC", 9)
        s.c.drawCentredString(W / 2, H - 1.1 * inch, "A GUIDED MEMORY KEEPSAKE")
        s.c.setFillColor(colors.black)
        s.c.setFont("PlayfairSC-B", 28)
        s.c.drawCentredString(W / 2, H - 1.85 * inch, "STORIES")
        s.c.drawCentredString(W / 2, H - 2.35 * inch, "WE KEEP")
        s.c.setFont("Crimson-I", 13)
        s.c.drawCentredString(W / 2, H - 2.85 * inch, SUBTITLE)
        s.c.setFont("Crimson", 11)
        s.c.setFillColor(colors.HexColor("#444444"))
        s.c.drawCentredString(W / 2, H - 3.25 * inch, TAGLINE)
        s.draw_img("title", W / 2 - 2.1 * inch, H - 3.5 * inch, 4.2 * inch, 2.4 * inch)
        s.c.setFillColor(colors.black)
        s.c.setFont("Crimson", 14)
        s.c.drawCentredString(W / 2, 1.35 * inch, "Blake La Pierre")

    def copyright(s):
        s.new("nofolio")
        left, right = margins(s.page)
        y = H - 1.5 * inch
        s.c.setFont("Crimson-B", 11); s.c.setFillColor(colors.black)
        s.c.drawString(left, y, TITLE)
        y -= 18
        s.c.setFont("Crimson", 10)
        for line in [
            "Copyright © 2026 Blake La Pierre",
            "All rights reserved.",
            "",
            "This is a guided keepsake journal. The prompts and",
            "illustrations are original to this edition.",
            "",
            "No ISBN on this page — KDP provides a free ISBN",
            "and prints the barcode on the back cover.",
            "",
            "Printed in the United States of America.",
            "First edition.",
        ]:
            s.c.drawString(left, y, line); y -= 14

    def how_to(s):
        s.new(); s.marks["howto"] = s.page
        s.folio(); s.header(TITLE)
        left, _, tw, _ = s.content_box()
        y = H - MT - 10
        s.c.setFont("PlayfairSC-B", 18); s.c.setFillColor(colors.black)
        s.c.drawCentredString(W / 2, y, "How This Book Works")
        y -= 28
        text = (
            "This book is a gift you give to someone whose stories you want to keep — "
            "a parent, a grandparent, an aunt, an uncle, a dear friend. Or it is a gift "
            "you give yourself, so the people who love you will have your voice on paper."
        )
        y = s.para(text, s.body, left, y, tw) - 12
        for t in [
            "<b>Write in ink or pencil.</b> There is no wrong answer and no perfect length.",
            "<b>Skip what you like.</b> Circle back later. Cross things out. Paste a photo in the margins if you want.",
            "<b>Use the lined pages at the back</b> when a story needs more room.",
            "<b>The letter pages near the end</b> are for notes to children, grandchildren, or the person who gave you this book.",
            "<b>Take your time.</b> A page a week is enough. This book is meant to last.",
        ]:
            y = s.para("• " + t, s.body, left, y, tw) - 8
        y -= 10
        y = s.para(
            "When it is finished, it becomes a family heirloom: handwriting, memories, and a little ink art of home.",
            s.italic, left, y, tw,
        )

    def belongs(s):
        s.new(); s.folio(); s.header(TITLE)
        left, _, tw, _ = s.content_box()
        y = H - MT - 20
        s.c.setFont("PlayfairSC-B", 16); s.c.setFillColor(colors.black)
        s.c.drawCentredString(W / 2, y, "This Book Belongs To")
        y -= 40
        for label in ["Name", "Given by", "Date", "For the family of"]:
            s.c.setFont("Crimson-I", 11)
            s.c.drawString(left, y, label)
            y -= 8
            y = s.lines(left, y, tw, 2, gap=20) - 18

    def contents(s):
        s.new(); s.marks["contents"] = s.page
        s.folio(); s.header(TITLE)
        left, _, tw, _ = s.content_box()
        y = H - MT - 10
        s.c.setFont("PlayfairSC-B", 18); s.c.setFillColor(colors.black)
        s.c.drawCentredString(W / 2, y, "Contents")
        y -= 36
        # page numbers filled after build via second pass not needed — write section names only with marks later
        items = [("How This Book Works", "howto")]
        for sec in SECTIONS:
            items.append((f"{sec['kicker']}: {sec['name']}", f"part-{sec['id']}"))
        items += [("Family Tree", "family-tree"), ("A Simple Timeline", "timeline"),
                  ("Extra Pages", "extra"), ("A Note of Thanks", "thanks")]
        s._contents_items = items
        s._contents_y = y
        s._contents_left = left
        s._contents_tw = tw
        # placeholder lines; rewrite at end
        for name, _ in items:
            s.c.setFont("Crimson", 12)
            s.c.drawString(left, y, name)
            y -= 22

    def rewrite_contents(s):
        """Called after all pages assigned — redraw contents page with page numbers."""
        # simplest approach: store marks and regenerate contents into a second PDF merge is heavy.
        # Instead, write page numbers now that marks exist by editing... we can't easily rewrite.
        # So: build contents AFTER sections by restructuring main().
        pass

    def section_opener(s, sec):
        # ensure right-hand (odd) page
        if s.page % 2 == 0:
            s.blank_vignette()
        s.new(); s.marks[f"part-{sec['id']}"] = s.page
        s.folio()
        left, _, tw, _ = s.content_box()
        y = H - MT - 8
        s.c.setFillColor(colors.HexColor("#666666"))
        s.c.setFont("PlayfairSC", 9)
        s.c.drawCentredString(W / 2, y, sec["kicker"].upper())
        y -= 26
        s.c.setFillColor(colors.black)
        s.c.setFont("PlayfairSC-B", 22)
        s.c.drawCentredString(W / 2, y, sec["name"].upper())
        y -= 18
        s.c.setStrokeColor(colors.HexColor("#aaaaaa")); s.c.setLineWidth(0.7)
        s.c.line(W / 2 - 40, y, W / 2 + 40, y)
        y -= 20
        y = s.para(sec["blurb"], s.center_it, left, y, tw) - 16
        s.draw_img(sec["art"], left, y, tw, 4.6 * inch)

    def prompt_page(s, sec, title, hint, vignette=None):
        s.new(); s.folio(); s.header(sec["name"])
        left, _, tw, _ = s.content_box()
        y = H - MT - 6
        s.c.setFont("PlayfairSC-B", 14); s.c.setFillColor(colors.black)
        s.c.drawString(left, y, title)
        y -= 18
        y = s.para(hint, s.prompt_h, left, y, tw) - 14
        # writing lines fill remaining space
        line_bottom = MB + 0.35 * inch
        if vignette:
            # leave room for small vignette at bottom
            avail = y - line_bottom - 1.5 * inch
            n = max(6, int(avail / 18))
            y = s.lines(left, y, tw, n, gap=18)
            s.draw_img(vignette, W / 2 - 0.7 * inch, line_bottom + 1.35 * inch, 1.4 * inch, 1.3 * inch)
        else:
            avail = y - line_bottom
            n = max(8, int(avail / 18))
            s.lines(left, y, tw, n, gap=18)

    def family_tree(s):
        if s.page % 2 == 0:
            s.blank_vignette()
        s.new(); s.marks["family-tree"] = s.page
        s.folio(); s.header(TITLE)
        left, _, tw, _ = s.content_box()
        y = H - MT - 8
        s.c.setFont("PlayfairSC-B", 18); s.c.setFillColor(colors.black)
        s.c.drawCentredString(W / 2, y, "Family Tree")
        y -= 24
        y = s.para(FAMILY_TREE_NOTE, s.italic, left, y, tw) - 16
        # empty boxes suggestion
        s.c.setStrokeColor(colors.HexColor("#888888")); s.c.setLineWidth(0.8)
        box_w, box_h = tw * 0.42, 0.7 * inch
        for row, labels in enumerate([
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
        ]):
            yy = y - row * (box_h + 28)
            for col in range(2):
                xx = left + col * (tw - box_w)
                s.c.rect(xx, yy - box_h, box_w, box_h, stroke=1, fill=0)
                s.c.setFont("Crimson-I", 8); s.c.setFillColor(colors.HexColor("#999999"))
                s.c.drawString(xx + 4, yy - 12, "name")
        # facing page
        s.new(); s.folio(); s.header(TITLE)
        left, _, tw, _ = s.content_box()
        y = H - MT - 8
        s.c.setFont("PlayfairSC-B", 14); s.c.setFillColor(colors.black)
        s.c.drawString(left, y, "More names and notes")
        y -= 24
        s.lines(left, y, tw, 22, gap=18)

    def timeline(s):
        s.new(); s.marks["timeline"] = s.page
        s.folio(); s.header(TITLE)
        left, _, tw, _ = s.content_box()
        y = H - MT - 8
        s.c.setFont("PlayfairSC-B", 18); s.c.setFillColor(colors.black)
        s.c.drawCentredString(W / 2, y, "A Simple Timeline")
        y -= 22
        y = s.para(TIMELINE_NOTE, s.italic, left, y, tw) - 18
        for _ in range(12):
            s.c.setFont("Crimson-I", 9); s.c.setFillColor(colors.HexColor("#888888"))
            s.c.drawString(left, y, "Year")
            s.c.setStrokeColor(colors.HexColor("#bbbbbb")); s.c.setLineWidth(0.6)
            s.c.line(left + 36, y - 2, left + 90, y - 2)
            s.c.line(left + 100, y - 2, left + tw, y - 2)
            y -= 28

    def extra_pages(s, n=8):
        if s.page % 2 == 0:
            s.blank_vignette()
        s.new(); s.marks["extra"] = s.page
        s.folio(); s.header(TITLE)
        left, _, tw, _ = s.content_box()
        y = H - MT - 8
        s.c.setFont("PlayfairSC-B", 16); s.c.setFillColor(colors.black)
        s.c.drawCentredString(W / 2, y, "Extra Pages")
        y -= 20
        y = s.para(EXTRA_NOTE, s.italic, left, y, tw) - 14
        s.lines(left, y, tw, 20, gap=18)
        for i in range(n - 1):
            s.new(); s.folio(); s.header(TITLE)
            left, _, tw, _ = s.content_box()
            y = H - MT - 6
            s.lines(left, y, tw, 24, gap=18)

    def thanks_page(s):
        if s.page % 2 == 0:
            s.blank_vignette()
        s.new(); s.marks["thanks"] = s.page
        # no folio on thanks for a clean close? keep folio for page count honesty
        s.folio()
        s.c.setFont("PlayfairSC-B", 18); s.c.setFillColor(colors.black)
        s.c.drawCentredString(W / 2, H - 1.6 * inch, "Thank You")
        s.draw_img("thanks", W / 2 - 1.5 * inch, H - 2.0 * inch, 3.0 * inch, 3.5 * inch)
        s.c.setFont("Crimson-I", 12)
        s.c.drawCentredString(W / 2, 2.0 * inch, "For writing the stories we will keep.")
        s.c.setFont("Crimson", 11)
        s.c.drawCentredString(W / 2, 1.55 * inch, "Blake La Pierre")

    def build(s):
        s.half_title()
        s.frontis()
        s.title_page()
        s.copyright()
        s.how_to()
        s.belongs()
        # contents placeholder — build after we know page numbers by doing sections first into a list? 
        # Simpler: put contents after howto with section names only (no page numbers), like some journals.
        s.contents_simple()
        vignettes = ["v-lamp", "v-envelope", "v-mug", "v-books"]
        vi = 0
        for sec in SECTIONS:
            s.section_opener(sec)
            for i, (title, hint) in enumerate(sec["prompts"]):
                vig = vignettes[vi % len(vignettes)] if i % 3 == 2 else None
                if vig:
                    vi += 1
                s.prompt_page(sec, title, hint, vignette=vig)
        s.family_tree()
        s.timeline()
        s.extra_pages(8)
        s.thanks_page()
        # ensure even page count? KDP doesn't require it. Leave as-is.
        s.c.save()
        info = {"pages": s.page, "marks": s.marks, "kind": "hardcover keepsake journal"}
        json.dump(info, open(os.path.join(ROOT, "build-info.json"), "w"), indent=1)
        print("wrote", OUT, "pages", s.page)
        return info

    def contents_simple(s):
        s.new(); s.marks["contents"] = s.page
        s.folio(); s.header(TITLE)
        left, _, tw, _ = s.content_box()
        y = H - MT - 10
        s.c.setFont("PlayfairSC-B", 18); s.c.setFillColor(colors.black)
        s.c.drawCentredString(W / 2, y, "Contents")
        y -= 36
        rows = ["How This Book Works", "This Book Belongs To"]
        for sec in SECTIONS:
            rows.append(f"{sec['kicker']}: {sec['name']}")
        rows += ["Family Tree", "A Simple Timeline", "Extra Pages", "A Note of Thanks"]
        for name in rows:
            s.c.setFont("Crimson", 12); s.c.setFillColor(colors.black)
            s.c.drawString(left, y, name)
            s.c.setStrokeColor(colors.HexColor("#cccccc")); s.c.setLineWidth(0.5)
            s.c.setDash(1, 2)
            s.c.line(left + s.c.stringWidth(name, "Crimson", 12) + 8, y + 2, left + tw, y + 2)
            s.c.setDash()
            y -= 20

if __name__ == "__main__":
    Book().build()
