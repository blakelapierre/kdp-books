"""Page geometry shared by master.py (to make sure every puzzle fits its page) and build.py."""
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch

G = "/usr/share/fonts/truetype/sand-box/google/"
for n, p in [("Crimson", "Crimson Text/CrimsonText-Regular.ttf"), ("Crimson-I", "Crimson Text/CrimsonText-Italic.ttf"),
             ("Plex", "IBM Plex Sans Condensed/IBMPlexSansCondensed-Regular.ttf")]:
    try:
        pdfmetrics.registerFont(TTFont(n, G + p))
    except Exception:
        pass

W, H = 6 * inch, 9 * inch
INNER, OUTER, TOP, BOT = 0.75 * inch, 0.55 * inch, 0.70 * inch, 0.75 * inch
TW = W - INNER - OUTER
TH = H - TOP - BOT

# per band: clue font size, leading, grid cell size, label band (pt), max clue lines on the page
BAND_LAYOUT = {
    "Easy":   dict(fs=10.6, ld=13.6, cell=22, lab=80, max_lines=15),
    "Medium": dict(fs=10.2, ld=12.9, cell=18, lab=80, max_lines=13),
    "Hard":   dict(fs=9.8, ld=12.3, cell=14.6, lab=80, max_lines=14),
    "Expert": dict(fs=10.4, ld=13.4, cell=12.8, lab=80, max_lines=30),   # Expert puzzles take a two-page spread
}
CLUE_INDENT = 15


def wrap_lines(text, font, size, width):
    words = text.split()
    lines, cur = 0, ""
    for w in words:
        t = (cur + " " + w).strip()
        if cur and pdfmetrics.stringWidth(t, font, size) > width:
            lines += 1
            cur = w
        else:
            cur = t
    return lines + (1 if cur else 0)


def clue_lines(texts, band):
    L = BAND_LAYOUT[band]
    return sum(wrap_lines(t, "Crimson", L["fs"], TW - CLUE_INDENT - 2) for t in texts)


# ---- exact fit check (same paragraph styles as build.py) ----
def styles(band):
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    for n, p in [("Crimson-SB", "Crimson Text/CrimsonText-SemiBold.ttf")]:
        try:
            pdfmetrics.registerFont(TTFont(n, G + p))
        except Exception:
            pass
    L = BAND_LAYOUT[band]
    st = ParagraphStyle("cl", fontName="Crimson", fontSize=L["fs"], leading=L["ld"], leftIndent=CLUE_INDENT,
                        bulletIndent=0, bulletFontName="Crimson-SB", bulletFontSize=L["fs"],
                        textColor=colors.Color(0.08, 0.08, 0.08), spaceAfter=1.2)
    intro = ParagraphStyle("in", fontName="Crimson-I", fontSize=10.2, leading=12.8,
                           textColor=colors.Color(0.15, 0.15, 0.15), alignment=TA_LEFT)
    return st, intro


HEADER_H = 24
INTRO_GAP = 7


def text_height(intro_text, clue_texts, band):
    from reportlab.platypus import Paragraph
    st, intro = styles(band)
    h = HEADER_H + Paragraph(intro_text, intro).wrap(TW, 1000)[1] + INTRO_GAP
    for i, t in enumerate(clue_texts, 1):
        h += Paragraph(t, st, bulletText=f"{i}.").wrap(TW, 1000)[1] + st.spaceAfter
    return h


def grid_extent(k, n, band):
    L = BAND_LAYOUT[band]
    return L["lab"] + (k - 1) * n * L["cell"]


def free_space(intro_text, clue_texts, band, k, n):
    """Points left between the last clue and the grid (Expert: left-page space after the clues)."""
    avail = TH - 1
    if band == "Expert":
        return avail - text_height(intro_text, clue_texts, band)
    return avail - text_height(intro_text, clue_texts, band) - grid_extent(k, n, band)
