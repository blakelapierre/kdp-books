"""Builds the 6x9 interior PDF (grayscale, no bleed, mirrored margins, embedded fonts)."""
from __future__ import annotations
import json, sys, math, random, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether, Flowable,
)
from reportlab.lib.fonts import addMapping

G = "/usr/share/fonts/truetype/sand-box/google/"
for n, p in [
    ("Crimson", "Crimson Text/CrimsonText-Regular.ttf"),
    ("Crimson-I", "Crimson Text/CrimsonText-Italic.ttf"),
    ("Crimson-B", "Crimson Text/CrimsonText-Bold.ttf"),
    ("Crimson-SB", "Crimson Text/CrimsonText-SemiBold.ttf"),
    ("Crimson-BI", "Crimson Text/CrimsonText-BoldItalic.ttf"),
    ("PlayfairSC", "Playfair Display SC/PlayfairDisplaySC-Regular.ttf"),
    ("PlayfairSC-B", "Playfair Display SC/PlayfairDisplaySC-Bold.ttf"),
    ("Plex", "IBM Plex Sans Condensed/IBMPlexSansCondensed-Regular.ttf"),
    ("Plex-M", "IBM Plex Sans Condensed/IBMPlexSansCondensed-SemiBold.ttf"),
]:
    pdfmetrics.registerFont(TTFont(n, G + p))
pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
from reportlab import rl_config
rl_config.canvas_basefontname = "Crimson"
ParagraphStyle.defaults["fontName"] = "Crimson"
ParagraphStyle.defaults["bulletFontName"] = "Crimson"
addMapping("Crimson", 0, 0, "Crimson")
addMapping("Crimson", 0, 1, "Crimson-I")
addMapping("Crimson", 1, 0, "Crimson-B")
addMapping("Crimson", 1, 1, "Crimson-BI")

D = json.load(open(os.path.join(os.path.dirname(__file__), "..", "data.json")))
BANDS = ["Easy", "Medium", "Hard", "Expert"]
ALL = [p for b in BANDS for p in D[b]]
EX = D["Example"][0]
assert len(ALL) == 200

W, H = 6 * inch, 9 * inch
INNER, OUTER, TOP, BOT = 0.75 * inch, 0.55 * inch, 0.70 * inch, 0.75 * inch
DARK = colors.Color(0.17, 0.17, 0.17)
MID = colors.Color(0.45, 0.45, 0.45)
FROST = colors.Color(0.62, 0.62, 0.62)
ICE = colors.Color(0.925, 0.925, 0.925)
INK = colors.Color(0.1, 0.1, 0.1)
TITLE = "Fireside Cryptograms"
TW = W - INNER - OUTER
TH = H - TOP - BOT

PARTS = {
    "Easy": ("Part One", "Embers", "Three starter letters warm the grate. Common words and friendly patterns."),
    "Medium": ("Part Two", "Kindling", "Two starter letters. Look for repeated patterns and short words."),
    "Hard": ("Part Three", "Steady Flame", "One starter letter. Frequency and word shape do more of the work."),
    "Expert": ("Part Four", "Late Glow", "No starter letters. Pure cryptanalysis by the dying light."),
}
FL = "•&nbsp;&nbsp;"


class Doc(BaseDocTemplate):
    def handle_pageBegin(self):
        p = self.page + 1
        left = INNER if p % 2 == 1 else OUTER
        for t in self.pageTemplates:
            for f in t.frames:
                f._x1 = left
                f._geom()
        super().handle_pageBegin()

    def afterFlowable(self, fl):
        if getattr(fl, "section", None) is not None:
            self.section = fl.section
        if getattr(fl, "mark", None):
            self.marks[fl.mark] = self.page


class Kind(Flowable):
    def __init__(s, kind=None, section=None, mark=None):
        s.kind = kind
        s.section = section
        s.mark = mark
        s.width = s.height = 0

    def wrap(s, aw, ah):
        return 0, 0

    def draw(s):
        doc = s.canv._doctemplate
        if s.kind:
            doc.pkind[doc.page] = s.kind
        if s.section is not None:
            doc.section = s.section
        if s.mark:
            doc.marks[s.mark] = doc.page


def page_end(c, doc):
    p = doc.page
    kind = getattr(doc, "pkind", {}).get(p, "normal")
    if kind in ("blank", "title", "nofolio"):
        return
    c.saveState()
    c.setFont("Crimson", 9)
    c.setFillColor(MID)
    c.drawCentredString(W / 2 + ((INNER - OUTER) / 2 if p % 2 else -(INNER - OUTER) / 2), 0.42 * inch, str(p))
    if kind != "opener":
        c.setFont("PlayfairSC", 7.5)
        c.setFillColor(MID)
        if p % 2 == 0:
            c.drawString(OUTER, H - 0.42 * inch, TITLE)
        else:
            c.drawRightString(W - OUTER, H - 0.42 * inch, getattr(doc, "section", ""))
    c.restoreState()


def heading(kicker, title):
    return [
        Paragraph(kicker, ParagraphStyle("k", fontName="PlayfairSC", fontSize=9.5, leading=12,
                                         alignment=TA_CENTER, textColor=MID, spaceAfter=4)),
        Paragraph(title, ParagraphStyle("h1", fontName="PlayfairSC-B", fontSize=20, leading=24,
                                        alignment=TA_CENTER, textColor=DARK, spaceAfter=2)),
        Spacer(1, 8),
    ]


def flame(c, x, y, s=1.0):
    c.saveState()
    c.setFillColor(ICE)
    c.ellipse(x - 10 * s, y - 2 * s, x + 10 * s, y + 6 * s, stroke=0, fill=1)
    c.setFillColor(MID)
    p = c.beginPath()
    p.moveTo(x, y + 22 * s)
    p.curveTo(x + 10 * s, y + 10 * s, x + 8 * s, y, x, y)
    p.curveTo(x - 8 * s, y, x - 10 * s, y + 10 * s, x, y + 22 * s)
    p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.setFillColor(DARK)
    p = c.beginPath()
    p.moveTo(x, y + 14 * s)
    p.curveTo(x + 5 * s, y + 7 * s, x + 4 * s, y + 2 * s, x, y + 2 * s)
    p.curveTo(x - 4 * s, y + 2 * s, x - 5 * s, y + 7 * s, x, y + 14 * s)
    p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.restoreState()


class FlameArt(Flowable):
    def __init__(s, w, h, seed=1):
        s.width = w
        s.height = h
        s.seed = seed

    def wrap(s, aw, ah):
        return s.width, s.height

    def draw(s):
        c = s.canv
        r = random.Random(s.seed)
        c.setStrokeColor(FROST)
        c.setLineWidth(0.8)
        c.line(0, 8, s.width, 8)
        for i in range(5):
            flame(c, 30 + i * (s.width - 60) / 4, 10, s=0.7 + 0.15 * (i % 2))
        c.setFillColor(MID)
        c.setFont("Crimson-I", 9)
        c.drawCentredString(s.width / 2, s.height - 14, "warm wisdom · quiet evenings · pencil ready")


def wrap_cipher_tokens(cipher, max_chars):
    """Word-wrap ciphertext into lines of at most max_chars (counting spaces)."""
    words = cipher.split()
    lines, cur, n = [], [], 0
    for w in words:
        add = len(w) + (1 if cur else 0)
        if cur and n + add > max_chars:
            lines.append(" ".join(cur))
            cur, n = [w], len(w)
        else:
            cur.append(w)
            n += add
    if cur:
        lines.append(" ".join(cur))
    return lines


class PuzzleFlowable(Flowable):
    """Large-print cryptogram: ciphertext with write-in blanks under each letter."""

    def __init__(s, puzzle, width, show_band=True, compact=False):
        s.p = puzzle
        s.width = width
        s.show_band = show_band
        s.compact = compact
        s.letter_size = 11 if compact else 13
        s.gap = 3.2 if compact else 4.0
        s.line_gap = 28 if compact else 34
        s._height = None

    def _layout(s):
        max_chars = int(s.width / (s.letter_size * 0.62 + s.gap * 0.15))
        # More accurate: measure with plex
        lines = []
        words = s.p["cipher"].split()
        cur = []
        while words:
            trial = (cur + [words[0]])
            # width of trial with letter spacing
            w = s._line_width(" ".join(trial))
            if cur and w > s.width - 4:
                lines.append(cur)
                cur = []
            else:
                cur.append(words.pop(0))
        if cur:
            lines.append(cur)
        return lines

    def _line_width(s, text):
        # each alpha gets letter_size*0.7 + gap; spaces get letter_size*0.45
        total = 0
        for ch in text:
            if ch == " ":
                total += s.letter_size * 0.45
            elif ch.isalpha():
                total += s.letter_size * 0.72 + s.gap
            else:
                total += s.letter_size * 0.45
        return total

    def wrap(s, aw, ah):
        lines = s._layout()
        header = 22
        author = 16
        starters = 14 if s.p.get("givens") else 0
        h = header + len(lines) * s.line_gap + author + starters + 8
        s._height = h
        s._lines = lines
        return s.width, h

    def draw(s):
        c = s.canv
        p = s.p
        y = s._height - 14
        # header
        c.setFillColor(DARK)
        c.setFont("PlayfairSC-B", 12)
        label = "Example" if p["band"] == "Example" else f"No. {p['num']}"
        c.drawString(0, y, label)
        if s.show_band and p["band"] != "Example":
            c.setFont("Crimson-I", 9)
            c.setFillColor(MID)
            c.drawRightString(s.width, y, p["band"])
        y -= 6
        c.setStrokeColor(FROST)
        c.setLineWidth(0.6)
        c.line(0, y, s.width, y)
        y -= s.line_gap - 4

        for word_line in s._lines:
            x = 0
            for wi, word in enumerate(word_line):
                if wi:
                    x += s.letter_size * 0.45
                for ch in word:
                    if ch.isalpha():
                        c.setFillColor(INK)
                        c.setFont("Plex-M", s.letter_size)
                        c.drawCentredString(x + s.letter_size * 0.36, y + 10, ch)
                        # write-in blank
                        c.setStrokeColor(DARK)
                        c.setLineWidth(0.7)
                        c.line(x, y, x + s.letter_size * 0.72, y)
                        x += s.letter_size * 0.72 + s.gap
                    else:
                        c.setFillColor(MID)
                        c.setFont("Crimson", s.letter_size)
                        c.drawString(x, y + 10, ch)
                        x += s.letter_size * 0.4
            y -= s.line_gap

        y += 8
        c.setFillColor(MID)
        c.setFont("Crimson-I", 10)
        c.drawRightString(s.width, y, f"— {p['author']}")
        y -= 14
        givens = p.get("givens") or {}
        if givens:
            # Sort by cipher letter
            parts = [f"{c} = {givens[c]}" for c in sorted(givens)]
            c.setFillColor(DARK)
            c.setFont("Plex", 9)
            c.drawString(0, y, "Starter letters:  " + "   ".join(parts))


def puzzle_height_estimate(p, width, compact=False):
    f = PuzzleFlowable(p, width, compact=compact)
    f.wrap(width, 1000)
    return f._height


class HintBlock(Flowable):
    def __init__(s, puzzles, width):
        s.ps = puzzles
        s.width = width
        s.height = 12 + len(puzzles) * 11

    def wrap(s, aw, ah):
        return s.width, s.height

    def draw(s):
        c = s.canv
        y = s.height - 10
        c.setFont("Crimson", 9)
        for p in s.ps:
            words = "".join(ch if ch.isalpha() or ch == " " else " " for ch in p["plaintext"]).split()
            hint = " ".join(w[0] + "_" * (len(w) - 1) for w in words if w)
            c.setFillColor(DARK)
            c.setFont("Plex-M", 8)
            c.drawString(0, y, f"{p['num']}.")
            c.setFont("Crimson", 8.5)
            c.setFillColor(MID)
            # truncate if needed
            text = hint
            while pdfmetrics.stringWidth(text, "Crimson", 8.5) > s.width - 28 and len(text) > 10:
                text = text[:-4] + "…"
            c.drawString(22, y, text)
            y -= 11


class SolutionBlock(Flowable):
    def __init__(s, puzzles, width):
        s.ps = puzzles
        s.width = width
        s.height = 14 + len(puzzles) * 28

    def wrap(s, aw, ah):
        # compute real height
        h = 8
        for p in s.ps:
            # roughly 2 lines of text
            h += 26 + 10 * (len(p["plaintext"]) // 70)
        s.height = h
        return s.width, s.height

    def draw(s):
        c = s.canv
        y = s.height - 2
        for p in s.ps:
            y -= 11
            c.setFillColor(DARK)
            c.setFont("PlayfairSC-B", 9)
            c.drawString(0, y, f"No. {p['num']}")
            c.setFont("Crimson-I", 8)
            c.setFillColor(MID)
            c.drawRightString(s.width, y, p["author"])
            y -= 12
            c.setFillColor(INK)
            c.setFont("Crimson", 9)
            # wrap plaintext
            words = p["plaintext"].split()
            line = []
            for w in words:
                trial = (" ".join(line + [w]))
                if line and pdfmetrics.stringWidth(trial, "Crimson", 9) > s.width:
                    c.drawString(0, y, " ".join(line))
                    y -= 11
                    line = [w]
                else:
                    line.append(w)
            if line:
                c.drawString(0, y, " ".join(line))
                y -= 8
            y -= 4


body = ParagraphStyle("b", fontName="Crimson", fontSize=11.2, leading=15, alignment=TA_JUSTIFY,
                      firstLineIndent=14, textColor=INK)
body0 = ParagraphStyle("b0", parent=body, firstLineIndent=0)
bullet = ParagraphStyle("bu", parent=body0, leftIndent=12, firstLineIndent=0, spaceAfter=3)
small = ParagraphStyle("s", fontName="Crimson-I", fontSize=10, leading=13, alignment=TA_CENTER,
                       textColor=colors.Color(0.3, 0.3, 0.3))


def build(recto_fix):
    S = []

    def recto(tag):
        S.append(PageBreak())
        if tag in recto_fix:
            S.extend([Kind("blank"), PageBreak()])
        S.append(Kind(mark=tag))

    # Title
    S += [
        Kind("title"),
        Spacer(1, 0.55 * inch),
        Paragraph("Large-Print Quote Puzzles for Quiet Evenings",
                  ParagraphStyle("t0", fontName="PlayfairSC", fontSize=10, leading=13,
                                 alignment=TA_CENTER, textColor=MID)),
        Spacer(1, 12),
        Paragraph("Fireside<br/>Cryptograms",
                  ParagraphStyle("tt", fontName="PlayfairSC-B", fontSize=36, leading=40,
                                 alignment=TA_CENTER, textColor=DARK)),
        Spacer(1, 12),
        Paragraph("200 monoalphabetic quote puzzles<br/>Easy to Expert · Hints &amp; Solutions",
                  ParagraphStyle("t2", parent=small, fontSize=12.5, leading=16)),
        Spacer(1, 0.35 * inch),
        FlameArt(TW, 1.4 * inch, seed=3),
        Spacer(1, 0.35 * inch),
        Paragraph("Blake La Pierre",
                  ParagraphStyle("t4", parent=small, fontSize=12)),
    ]

    # Copyright
    S += [PageBreak(), Kind("nofolio"), Spacer(1, 3.4 * inch)]
    cs = ParagraphStyle("cp", parent=body0, fontSize=9, leading=12, alignment=TA_LEFT)
    for t in [
        "<i>Fireside Cryptograms: 200 Large-Print Quote Puzzles for Adults</i>",
        "Copyright © 2026 Blake La Pierre. All rights reserved.",
        "No part of this book may be reproduced in any form without written permission from the author, except for brief quotations in reviews. Readers may photocopy puzzle pages for personal solving.",
        "Quotations from public-domain authors are used under public-domain status. Original aphorisms are by Blake La Pierre. No modern copyrighted quotations appear in this book.",
        "First edition, 2026",
        "Set in Crimson Text, Playfair Display SC and IBM Plex Sans Condensed, used under the SIL Open Font License.",
    ]:
        S += [Paragraph(t, cs), Spacer(1, 6)]

    # Contents
    recto("contents")
    S += [Kind(section="Contents"), Spacer(1, 0.25 * inch)] + heading("Fireside Cryptograms", "Contents")
    S.append(("TOC",))
    S += [
        Spacer(1, 0.3 * inch),
        Paragraph(
            "Pull a chair close to the fire. Each puzzle is a famous (or fireside) saying written in a secret alphabet: "
            "every letter has been swapped for another, the same way all the way through. Word lengths and punctuation stay the same. "
            "Your job is to bring the words back. Every puzzle has exactly one solution, checked by computer.",
            ParagraphStyle("in", parent=small, fontSize=10.5, leading=14),
        ),
    ]

    # How to play
    recto("howto")
    S += [Kind(section="How to Play"), Spacer(1, 0.08 * inch)] + heading("Before You Begin", "How to Play")
    S.append(Paragraph(
        "A <b>cryptogram</b> (or cryptoquote) is a message written in a <b>monoalphabetic substitution cipher</b>. "
        "One plain letter always becomes the same cipher letter, and no two plain letters share a cipher letter.",
        ParagraphStyle("hb0", parent=body0, fontSize=10.8, leading=14),
    ))
    S.append(Spacer(1, 4))
    for t in [
        "Punctuation and word lengths are unchanged. An apostrophe or period can be a useful foothold.",
        "A one-letter word in English is almost always <b>A</b> or <b>I</b>.",
        "Look for common short words: <b>THE</b>, <b>AND</b>, <b>TO</b>, <b>OF</b>, <b>IN</b>, <b>IS</b>, <b>YOU</b>.",
        "Repeated letter patterns help: a three-letter word with the pattern X Y X is often <b>EYE</b> or similar; "
        "double letters (as in XX) often stand for <b>LL</b>, <b>EE</b>, <b>SS</b> or <b>OO</b>.",
        "English letter frequency is a quiet guide: <b>E</b>, <b>T</b>, <b>A</b>, <b>O</b>, <b>I</b>, <b>N</b> are common.",
        "Some puzzles print <b>starter letters</b> (for example <b>Q = T</b>). Fill those in first and pencil them above the alphabet strip in your mind.",
        "Write lightly. When a letter is certain, pencil it every place that cipher letter appears.",
        "The author’s name beside each puzzle is printed in ordinary English and is <b>not</b> encrypted.",
    ]:
        S.append(Paragraph(FL + t, ParagraphStyle("hb", parent=bullet, fontSize=10.5, leading=13.6)))

    S += [PageBreak(), Kind(section="How to Play"), Spacer(1, 0.05 * inch)] + heading("Let’s Warm Up", "A Worked Example")
    S.append(Paragraph(
        "Here is a complete Easy puzzle with three starter letters. Try it before peeking at the solution on the next page.",
        ParagraphStyle("exi", parent=body0, fontSize=10.5, leading=13.5, spaceAfter=6),
    ))
    S.append(PuzzleFlowable(EX, TW, show_band=False))
    S.append(Spacer(1, 10))
    S.append(Paragraph("<b>One path to the answer</b>", ParagraphStyle("x", parent=body0, alignment=TA_CENTER, textColor=DARK)))
    S.append(Spacer(1, 4))
    # Build a short narrative from EX givens
    gparts = ", ".join(f"<b>{c} = {v}</b>" for c, v in sorted((EX.get("givens") or {}).items()))
    for i, t in enumerate([
        f"Pencil in the starter letters first: {gparts or 'none on this example'}."
        if gparts else "This example has starter letters printed under the cipher.",
        "Hunt for one-letter words and the pattern of <b>THE</b> (the most common three-letter word).",
        "Each time you place a letter, write it above every matching cipher letter on the page.",
        "When the sentence reads as natural English and every cipher letter has a partner, you are done.",
        f"The plaintext of this example is: <i>{EX['plaintext']}</i> — {EX['author']}.",
    ], 1):
        S.append(Paragraph(f"<font name='PlayfairSC-B' color='#2b2b2b'>{i}.</font>&nbsp;&nbsp;{t}",
                           ParagraphStyle("exs", parent=bullet, fontSize=10.4, leading=13.4, spaceAfter=2.5)))
    S.append(Spacer(1, 6))
    S.append(Paragraph("Hints (first letters of each word) and full solutions are at the back of the book.",
                       ParagraphStyle("sm2", parent=small, fontSize=9.5)))

    # Puzzle parts
    for band in BANDS:
        part, line, blurb = PARTS[band]
        ps = D[band]
        recto(band)
        S += [Kind("opener"), Kind(section=f"{part} · {line}"), Spacer(1, 1.4 * inch)] + heading(f"{part} · {band}", line)
        S += [
            Paragraph(f"Puzzles {ps[0]['num']} to {ps[-1]['num']}", ParagraphStyle("pn", parent=small, fontSize=11)),
            Spacer(1, 12),
            Paragraph(blurb, ParagraphStyle("bl", parent=small, fontSize=11, leading=15)),
            Spacer(1, 0.4 * inch),
            FlameArt(TW, 1.2 * inch, seed=10 + BANDS.index(band)),
        ]
        S.append(PageBreak())

        # Pack 1–2 puzzles per page by height
        i = 0
        while i < len(ps):
            S.append(Kind(section=f"{part} · {line}"))
            h1 = puzzle_height_estimate(ps[i], TW, compact=False)
            if i + 1 < len(ps):
                h2 = puzzle_height_estimate(ps[i + 1], TW, compact=False)
                if h1 + h2 + 18 < TH - 8:
                    S.append(PuzzleFlowable(ps[i], TW))
                    S.append(Spacer(1, 14))
                    S.append(PuzzleFlowable(ps[i + 1], TW))
                    i += 2
                else:
                    S.append(PuzzleFlowable(ps[i], TW))
                    i += 1
            else:
                S.append(PuzzleFlowable(ps[i], TW))
                i += 1
            if i < len(ps):
                S.append(PageBreak())

    # Hints
    recto("hints")
    S += [Kind("opener"), Kind(section="Hints"), Spacer(1, 1.8 * inch)] + heading("A Soft Nudge", "Hints")
    S.append(Paragraph(
        "Each hint shows the first letter of every word, with blanks for the rest. "
        "Use them only when the fire is almost out.",
        small,
    ))
    for band in BANDS:
        ps = D[band]
        for i in range(0, len(ps), 18):
            chunk = ps[i:i + 18]
            S += [PageBreak(), Kind(section=f"Hints · {band}")]
            S.append(Paragraph(f"{band} · Nos. {chunk[0]['num']}–{chunk[-1]['num']}",
                               ParagraphStyle("hh", fontName="PlayfairSC-B", fontSize=11,
                                              textColor=DARK, spaceAfter=6)))
            S.append(HintBlock(chunk, TW))

    # Solutions
    recto("solutions")
    S += [Kind("opener"), Kind(section="Solutions"), Spacer(1, 1.8 * inch)] + heading("Into the Clear", "Solutions")
    S.append(Paragraph("Plaintext and author for every puzzle.", small))
    for band in BANDS:
        ps = D[band]
        for i in range(0, len(ps), 8):
            chunk = ps[i:i + 8]
            S += [PageBreak(), Kind(section=f"Solutions · {band}")]
            S.append(Paragraph(f"{band} · Nos. {chunk[0]['num']}–{chunk[-1]['num']}",
                               ParagraphStyle("hh", fontName="PlayfairSC-B", fontSize=11,
                                              textColor=DARK, spaceAfter=6)))
            S.append(SolutionBlock(chunk, TW))

    # About
    recto("about")
    S += [Kind("nofolio"), Spacer(1, 1.5 * inch)] + heading("Thank You", "For Sitting by the Fire")
    S.append(Paragraph(
        "If these puzzles kept you company, a short honest review helps other readers find the book. "
        "Thank you for your pencil, your patience and your quiet hour.",
        ParagraphStyle("ty", parent=body0, alignment=TA_CENTER),
    ))
    S += [
        Spacer(1, 0.45 * inch),
        Paragraph("Also by Blake La Pierre", ParagraphStyle("ab", parent=body0, alignment=TA_CENTER,
                                                            fontName="PlayfairSC", fontSize=10, textColor=DARK)),
        Spacer(1, 6),
        Paragraph("<i>The Thief Stayed the Night</i> · <i>Frostwood Express</i> · <i>Stars over Frostwood</i> · <i>The Advent Clock</i>",
                  ParagraphStyle("ab2", parent=small, fontSize=9.5, leading=13)),
    ]
    S.append(("PAD",))
    return S


def render(recto_fix, out, toc):
    S = build(recto_fix)
    if toc.get("_odd"):
        S += [PageBreak(), Kind("blank")]
    for i, x in enumerate(S):
        if x == ("PAD",):
            S[i] = Spacer(0, 0)
            continue
        if isinstance(x, tuple) and x[0] == "TOC":
            rows = [
                ("How to Play", toc.get("howto", 0)),
                ("A Worked Example", (toc.get("howto", 0) or 0) + 1),
            ]
            for b in BANDS:
                part, line, _ = PARTS[b]
                ps = D[b]
                rows.append((
                    f"{part} · {line}<br/><font size='9.5' color='#737373'>{b} · Puzzles {ps[0]['num']}–{ps[-1]['num']}</font>",
                    toc.get(b, 0),
                ))
            rows += [("Hints", toc.get("hints", 0)), ("Solutions", toc.get("solutions", 0))]
            t = Table(
                [[Paragraph(a, ParagraphStyle("tc", parent=body0, fontSize=11.5, leading=14)), str(b)]
                 for a, b in rows],
                colWidths=[TW - 0.5 * inch, 0.5 * inch],
            )
            t.setStyle(TableStyle([
                ("FONT", (0, 0), (-1, -1), "Crimson", 11),
                ("FONT", (1, 0), (1, -1), "Crimson", 11.5),
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LINEBELOW", (0, 0), (-1, -1), 0.3, FROST),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]))
            S[i] = t
    fr = Frame(INNER, BOT, TW, TH, id="f", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc = Doc(
        out, pagesize=(W, H), initialFontName="Crimson",
        title="Fireside Cryptograms: 200 Large-Print Quote Puzzles",
        author="Blake La Pierre",
        subject="Cryptogram puzzle book",
        pageTemplates=[PageTemplate("normal", [fr], onPageEnd=page_end)],
    )
    doc.pkind = {}
    doc.marks = {}
    doc.section = ""
    doc.build(S)
    return doc.marks, doc.page


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "interior.pdf")
    fix = set()
    toc = {}
    care = {"howto", "hints", "solutions", "contents", "about"}
    pages = marks = None
    for it in range(12):
        marks, pages = render(fix, out, toc)
        bad = sorted((p, k) for k, p in marks.items() if not str(k).startswith("_") and p % 2 == 0)
        marks["_odd"] = toc.get("_odd", False) ^ (pages % 2 == 1)
        important_bad = [k for _, k in bad if k in care]
        if not important_bad and marks.get("_odd") == toc.get("_odd", False):
            toc = marks
            break
        fix |= set(important_bad)
        toc = marks
    info = {"pages": pages, "marks": {k: v for k, v in toc.items() if not str(k).startswith("_")}}
    info_path = os.path.join(os.path.dirname(__file__), "..", "build-info.json")
    json.dump(info, open(info_path, "w"), indent=1)
    print(json.dumps(info, indent=1))
    print(f"Wrote {out} ({pages} pages)")
