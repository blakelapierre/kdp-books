"""Build one free printable US Letter sample PDF per book, using real pages from interior.pdf.
Run with pypdf + reportlab available:  python3 build_samples.py
"""
import io, os
from pypdf import PdfReader, PdfWriter, Transformation
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from common import BOOKS, FONTS, MKT, book_path, front_cover, NAVY, GOLD, SLATE

OUT = os.path.join(MKT, "social", "samples")
LW, LH = 612, 792          # US Letter in points
SCALE = 1.1                # 6 x 9 in page -> 6.6 x 9.9 in on Letter
for k in ("title", "title-reg", "body", "body-i", "body-b", "label"):
    pdfmetrics.registerFont(TTFont(k, FONTS[k]))
rgb = lambda c: tuple(v / 255 for v in c)

SAMPLES = {
    "the-thief-stayed-the-night": dict(
        pages=[9, 10, 11, 12, 13, 14], answers=[118],
        inside=["Case One: The Cocoa Tin", "The story, the guest register and all the clues",
                "A verdict page to record your answer", "The full step-by-step solution"]),
    "frostwood-express": dict(
        pages=[5, 8, 9, 34, 60], answers=[164, 168, 173],
        inside=["How to play Train Tracks", "Four Easy puzzles (No. 1 to 4)",
                "Two Medium puzzles (No. 51 and 52) and one Hard (No. 101)",
                "Answer pages (they also show a few puzzles not in this sample)"]),
    "stars-over-frostwood": dict(
        pages=[5, 8, 9, 30, 52], answers=[156, 159, 163],
        inside=["How to play Star Battle", "Four Easy puzzles (No. 1 to 4)",
                "Two Medium puzzles (No. 41 and 42) and one Hard two-star puzzle (No. 81)",
                "Answer pages (they also show a few puzzles not in this sample)"]),
    "the-advent-clock": dict(
        pages=[4, 6, 8, 9, 10, 11], answers=[65, 66],
        inside=["The story of the Great Advent Clock", "How the countdown works",
                "Door One (word search) and Door Two (secret code)", "The solutions for both doors"]),
}

def footer(c, title):
    c.setFont("body-i", 10); c.setFillColorRGB(*rgb(SLATE))
    c.drawCentredString(LW / 2, 18, f"More in {title} by Blake La Pierre on Amazon")

def intro_page(slug, info):
    b = BOOKS[slug]
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(LW, LH))
    c.setFillColorRGB(*rgb(NAVY)); c.rect(0, LH - 150, LW, 150, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1); c.setFont("title", 30)
    c.drawCentredString(LW / 2, LH - 75, b["title"])
    c.setFillColorRGB(*rgb(GOLD)); c.setFont("label", 13)
    c.drawCentredString(LW / 2, LH - 110, "A FREE PRINTABLE SAMPLE  \u00b7  WITH ANSWERS")
    cov = front_cover(slug, 150)
    w = 210; h = w * cov.height / cov.width
    c.drawImage(ImageReader(cov), 60, LH - 190 - h, w, h)
    x = 300; y = LH - 205
    c.setFillColorRGB(*rgb(NAVY)); c.setFont("title-reg", 17); c.drawString(x, y, "What's Inside"); y -= 24
    c.setFont("body", 13)
    for line in info["inside"]:
        words, cur = line.split(), ""
        first = True
        for wd in words:
            t = (cur + " " + wd).strip()
            if c.stringWidth(t, "body", 13) > 260:
                c.drawString(x + (0 if first else 12), y, ("\u2022 " if first else "") + cur); y -= 17; cur = wd; first = False
            else:
                cur = t
        c.drawString(x + (0 if first else 12), y, ("\u2022 " if first else "") + cur); y -= 22
    y -= 8
    c.setFont("title-reg", 17); c.drawString(x, y, "How to Print"); y -= 24
    c.setFont("body", 13)
    for line in ["US Letter paper, portrait.", "Choose \u201cActual size\u201d or \u201cFit\u201d.",
                 "Grab a pencil and an eraser.", "Answers are at the back. No peeking!"]:
        c.drawString(x, y, "\u2022 " + line); y -= 18
    y = min(y, LH - 200 - h) - 40
    c.setFont("title-reg", 16); c.drawCentredString(LW / 2, y, "Enjoyed these puzzles?"); y -= 22
    c.setFont("body", 13)
    c.drawCentredString(LW / 2, y, f"The full book, {b['title']}, is a paperback on Amazon."); y -= 18
    if b["asin"]:
        c.drawCentredString(LW / 2, y, f"amazon.com/dp/{b['asin']}"); y -= 18
    else:
        c.drawCentredString(LW / 2, y, f"Search Amazon for \u201c{b['title']} Blake La Pierre\u201d."); y -= 18
    c.setFont("body-i", 11); c.setFillColorRGB(*rgb(SLATE))
    c.drawCentredString(LW / 2, 60, "\u00a9 2026 Blake La Pierre. Free to print and share for personal, non-commercial use.")
    c.drawCentredString(LW / 2, 44, "Every puzzle is checked by computer to have exactly one solution.")
    footer(c, b["title"])
    c.showPage(); c.save(); buf.seek(0)
    return PdfReader(buf).pages[0]

def footer_page(title):
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(LW, LH)); footer(c, title); c.showPage(); c.save(); buf.seek(0)
    return PdfReader(buf).pages[0]

def build(slug, info):
    b = BOOKS[slug]
    src = PdfReader(book_path(slug, "interior.pdf"))
    w = PdfWriter()
    w.add_page(intro_page(slug, info))
    for pno in info["pages"] + info["answers"]:
        sp = src.pages[pno - 1]
        pw, ph = float(sp.mediabox.width), float(sp.mediabox.height)
        dx = (LW - pw * SCALE) / 2
        dy = 34 + (LH - 34 - ph * SCALE) / 2
        page = w.add_blank_page(LW, LH)
        page.merge_transformed_page(sp, Transformation().scale(SCALE).translate(dx, dy))
        page.merge_page(footer_page(b["title"]))
    w.add_metadata({"/Title": f"{b['title']}: Free Printable Sample", "/Author": "Blake La Pierre"})
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f"{slug}-sample.pdf")
    with open(path, "wb") as f:
        w.write(f)
    w.close()
    return path

if __name__ == "__main__":
    for slug, info in SAMPLES.items():
        p = build(slug, info)
        print(os.path.relpath(p, MKT), len(PdfReader(p).pages), "pages", os.path.getsize(p) // 1024, "KB")
