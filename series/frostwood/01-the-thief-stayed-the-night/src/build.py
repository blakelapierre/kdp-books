"""Builds the 6x9 interior PDF (grayscale, no bleed, mirrored margins, embedded fonts)."""
import json, sys, math, random
sys.path.insert(0, ".")
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak, Table,
    TableStyle, NextPageTemplate, KeepTogether, CondPageBreak)
from reportlab.platypus.flowables import HRFlowable, Flowable
from reportlab.lib.fonts import addMapping
from clues import CASES
import stories as ST

G = "/usr/share/fonts/truetype/sand-box/google/"
for n, p in [("Crimson", "Crimson Text/CrimsonText-Regular.ttf"), ("Crimson-I", "Crimson Text/CrimsonText-Italic.ttf"),
             ("Crimson-B", "Crimson Text/CrimsonText-Bold.ttf"), ("Crimson-SB", "Crimson Text/CrimsonText-SemiBold.ttf"),
             ("Crimson-BI", "Crimson Text/CrimsonText-BoldItalic.ttf"),
             ("PlayfairSC", "Playfair Display SC/PlayfairDisplaySC-Regular.ttf"), ("PlayfairSC-B", "Playfair Display SC/PlayfairDisplaySC-Bold.ttf"),
             ("Plex", "IBM Plex Sans Condensed/IBMPlexSansCondensed-Regular.ttf"), ("Plex-M", "IBM Plex Sans Condensed/IBMPlexSansCondensed-SemiBold.ttf")]:
    pdfmetrics.registerFont(TTFont(n, G + p))
pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
from reportlab import rl_config
rl_config.canvas_basefontname = "Crimson"   # avoid an unembedded Helvetica default font resource
ParagraphStyle.defaults["fontName"] = "Crimson"; ParagraphStyle.defaults["bulletFontName"] = "Crimson"
addMapping("Crimson", 0, 0, "Crimson"); addMapping("Crimson", 0, 1, "Crimson-I"); addMapping("Crimson", 1, 0, "Crimson-B"); addMapping("Crimson", 1, 1, "Crimson-BI")

D = json.load(open("../data.json"))
EXPECT = ["Dexter Hawthorne", "Verity Hollis", "Cyril Nightingale", "Frank Foxley", "Ida Dunmore", "Dorothy Aldridge", "Kenneth Parsley",
          "Walter Sallow", "Isadora Pilbeam", "Agatha Bramble", "Lark Yelland", "Gwendolyn Dimsdale"]
assert [c["thief"] for c in D] == EXPECT, "thieves changed: confessions must be re-checked"

W, H = 6 * inch, 9 * inch
INNER, OUTER, TOP, BOT = 0.75 * inch, 0.55 * inch, 0.7 * inch, 0.75 * inch
# grayscale palette (black & white interior)
DARK = colors.Color(0.17, 0.17, 0.17); MID = colors.Color(0.45, 0.45, 0.45); FROST = colors.Color(0.62, 0.62, 0.62)
ICE = colors.Color(0.925, 0.925, 0.925); INK = colors.Color(0.1, 0.1, 0.1)
TITLE = "The Thief Stayed the Night"
NUMW = ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve"]
def words(n):
    ones = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
    tens = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
    if n < 20: return ones[n]
    if n < 100: return tens[n // 10] + ("-" + ones[n % 10] if n % 10 else "")
    return "one hundred" + (" and " + words(n - 100) if n > 100 else "")
TW = W - INNER - OUTER

class Doc(BaseDocTemplate):
    def handle_pageBegin(self):
        p = self.page + 1
        left = INNER if p % 2 == 1 else OUTER
        for t in self.pageTemplates:
            for f in t.frames:
                f._x1 = left; f._geom()
        super().handle_pageBegin()
    def afterFlowable(self, fl):
        if getattr(fl, "section", None) is not None: self.section = fl.section
        if getattr(fl, "mark", None): self.marks[fl.mark] = self.page

def snowflake(c, x, y, r, col, lw=0.09):
    c.saveState(); c.setStrokeColor(col); c.setLineWidth(r * lw); c.setLineCap(1)
    for i in range(6):
        a = math.pi / 3 * i; c.line(x, y, x + r * math.cos(a), y + r * math.sin(a))
        bx, by = x + r * 0.55 * math.cos(a), y + r * 0.55 * math.sin(a)
        for s in (-1, 1):
            b = a + s * math.pi / 4; c.line(bx, by, bx + r * 0.3 * math.cos(b), by + r * 0.3 * math.sin(b))
    c.restoreState()

def page_end(c, doc):
    p = doc.page; kind = getattr(doc, "pkind", {}).get(p, "normal")
    if kind in ("blank", "title", "nofolio"): return
    c.saveState()
    c.setFont("Crimson", 9); c.setFillColor(MID)
    c.drawCentredString(W / 2 + ((INNER - OUTER) / 2 if p % 2 else -(INNER - OUTER) / 2), 0.42 * inch, str(p))
    if kind != "opener":
        c.setFont("PlayfairSC", 7.5); c.setFillColor(MID)
        hdr = TITLE if p % 2 == 0 else getattr(doc, "section", "")
        if p % 2 == 0: c.drawString(OUTER, H - 0.42 * inch, hdr)
        else: c.drawRightString(W - OUTER, H - 0.42 * inch, hdr)
    c.restoreState()

class Kind(Flowable):
    """Zero-size marker: sets the page kind (for folio/header) and/or running section title."""
    def __init__(s, kind=None, section=None, mark=None): s.kind = kind; s.section = section; s.mark = mark; s.width = s.height = 0
    def wrap(s, aw, ah): return 0, 0
    def draw(s):
        doc = s.canv._doctemplate
        if s.kind: doc.pkind[doc.page] = s.kind

body = ParagraphStyle("b", fontName="Crimson", fontSize=11.2, leading=15, alignment=TA_JUSTIFY, firstLineIndent=14, textColor=INK)
body0 = ParagraphStyle("b0", parent=body, firstLineIndent=0)
drop0 = ParagraphStyle("d0", parent=body0)
h1 = ParagraphStyle("h1", fontName="PlayfairSC-B", fontSize=20, leading=24, alignment=TA_CENTER, textColor=DARK, spaceAfter=2)
kick = ParagraphStyle("k", fontName="PlayfairSC", fontSize=9.5, leading=12, alignment=TA_CENTER, textColor=MID, spaceAfter=4)
h2 = ParagraphStyle("h2", fontName="PlayfairSC-B", fontSize=12.5, leading=15, textColor=DARK, spaceBefore=4, spaceAfter=1)
small = ParagraphStyle("s", fontName="Crimson-I", fontSize=10, leading=13, alignment=TA_CENTER, textColor=colors.Color(.3, .3, .3))
clueb = ParagraphStyle("cb", parent=body0, fontSize=10.8, leading=14.2)
clueR = ParagraphStyle("cr", parent=clueb, fontName="Crimson-I", textColor=DARK, spaceBefore=2)
bullet = ParagraphStyle("li", parent=body0, alignment=TA_LEFT, leftIndent=14, firstLineIndent=-12, spaceAfter=3)

class Flake(Flowable):
    def __init__(s, r=6): s.r = r; s.width = 0; s.height = 2 * r + 6
    def wrap(s, aw, ah): s.aw = aw; return aw, s.height
    def draw(s):
        c = s.canv; c.setStrokeColor(FROST); c.setLineWidth(0.5)
        c.line(s.aw / 2 - 60, s.r + 3, s.aw / 2 - s.r - 6, s.r + 3); c.line(s.aw / 2 + s.r + 6, s.r + 3, s.aw / 2 + 60, s.r + 3)
        snowflake(c, s.aw / 2, s.r + 3, s.r, DARK)
def runin(t):
    w, rest = t.split(" ", 1)
    return f"<font name='PlayfairSC-B' color='#2b2b2b'>{w}</font> " + rest
def heading(k, t): return [Paragraph(k, kick), Paragraph(t, h1), Flake(), Spacer(1, 8)]
FL = "<font name='DejaVu' color='#9e9e9e' size='9'>❄</font>&nbsp;&nbsp;"

class TitleArt(Flowable):
    """Grayscale line-art version of the sample's title art (interior title page, no bleed)."""
    def __init__(s, w, h): s.width, s.height = w, h
    def draw(s):
        c = s.canv; w, h = s.width, s.height; r = random.Random(7)
        for _ in range(16):
            snowflake(c, r.uniform(0.05, 0.95) * w, r.uniform(0.45, 0.98) * h, r.uniform(3, 8), colors.Color(.72, .72, .72))
        c.setStrokeColor(MID); c.setLineWidth(1.1); c.setLineJoin(1)
        base = 0.0
        pts = [(0, 0.28), (0.2, 0.62), (0.33, 0.46), (0.52, 0.8), (0.72, 0.48), (0.85, 0.62), (1.0, 0.36)]
        p = c.beginPath(); p.moveTo(pts[0][0] * w, pts[0][1] * h * 0.55)
        for x, y in pts[1:]: p.lineTo(x * w, y * h * 0.55)
        c.drawPath(p, stroke=1, fill=0)
        # lodge
        bx, bw, bh = w / 2 - 0.8 * inch, 1.6 * inch, 1.05 * inch
        c.setFillColor(colors.white); c.setStrokeColor(DARK); c.setLineWidth(1.2)
        c.rect(bx, base, bw, bh, stroke=1, fill=1)
        p = c.beginPath(); p.moveTo(bx - 0.12 * inch, bh); p.lineTo(w / 2, bh + 0.48 * inch); p.lineTo(bx + bw + 0.12 * inch, bh); p.close()
        c.drawPath(p, stroke=1, fill=1)
        for row in range(4):
            for col in range(5):
                lit = r.random() < 0.65
                c.setFillColor(colors.Color(.2, .2, .2) if not lit else colors.white)
                c.rect(bx + (0.14 + col * 0.285) * inch, (0.12 + row * 0.23) * inch, 0.12 * inch, 0.13 * inch, stroke=1, fill=1)
        c.setLineWidth(0.8); c.line(-0.2 * inch, base, w + 0.2 * inch, base)

class LodgePlan(Flowable):
    """Diagram of one corridor: odd rooms lake side, even rooms mountain side, West 01-10, East 11-20."""
    def __init__(s, w): s.width = w; s.height = 1.75 * inch
    def wrap(s, aw, ah): return s.width, s.height
    def draw(s):
        c = s.canv; w = s.width; cw = w / 10.6; x0 = 0.3 * cw; y0 = 0.3 * inch; rh = 0.34 * inch; corr = 0.3 * inch
        top = y0 + 2 * rh + corr
        c.setFont("Plex", 6.2)
        for i in range(10):
            n_odd = 2 * i + 1; n_even = 2 * i + 2; x = x0 + i * cw
            for (yy, n) in ((y0 + rh + corr, n_odd), (y0, n_even)):
                c.setFillColor(ICE if n > 10 else colors.white); c.setStrokeColor(MID); c.setLineWidth(0.6)
                c.rect(x, yy, cw, rh, stroke=1, fill=1); c.setFillColor(INK)
                c.drawCentredString(x + cw / 2, yy + rh / 2 - 2, "3%02d" % n)
        c.setFillColor(MID); c.setFont("Crimson-I", 8.5)
        for cx in (x0 + 2.5 * cw, x0 + 7.5 * cw): c.drawCentredString(cx, y0 + rh + corr / 2 - 3, "corridor")
        c.drawCentredString(x0 + 5 * cw, top + 5, "Lake side (odd numbers)")
        c.drawCentredString(x0 + 5 * cw, y0 - 12, "Mountain side (even numbers)")
        c.setFont("PlayfairSC", 8.5); c.setFillColor(DARK)
        c.drawCentredString(x0 + 2.5 * cw, top + 19, "West Wing · 01–10")
        c.drawCentredString(x0 + 7.5 * cw, top + 19, "East Wing · 11–20")
        c.setStrokeColor(DARK); c.setLineWidth(1.4); c.line(x0 + 5 * cw, y0, x0 + 5 * cw, top)

def clue_block(i, cl):
    num = Paragraph(f"<font name='PlayfairSC-B' size='17' color='#2b2b2b'>{i}</font>", ParagraphStyle("nm", fontName="Crimson", alignment=TA_CENTER, leading=20))
    content = [Paragraph(cl["t"], ParagraphStyle("cn", parent=h2, spaceBefore=0)), Paragraph(cl["x"], clueb), Paragraph(cl["b"], clueR)]
    ct = Table([[num, content]], colWidths=[0.38 * inch, TW - 0.38 * inch])
    ct.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Crimson", 10), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 6), ("LINEBELOW", (0, 0), (-1, -1), 0.4, FROST)]))
    return ct

def register_table(case, reg):
    cols = [("☐", None), ("Guest", lambda g: f"{g['last']}, {g['first']}"), ("Room", lambda g: str(g["room"]))]
    cols += [("Floor", lambda g: str(g["floor"]))] if case["num"] <= 3 else []
    cols += [("Arrived", lambda g: g["arr"]), ("Home City", lambda g: g["home"]), ("Occupation", lambda g: g["occ"])]
    for key, label, vals in case.get("cols", []): cols.append((label, lambda g, key=key: g[key]))
    rows = [[c[0] for c in cols]]
    for g in reg: rows.append(["☐"] + [f(g) for _, f in cols[1:]])
    for fs in (7.6, 7.3, 7.0, 6.8):
        cw = [0.2 * inch] + [max(pdfmetrics.stringWidth(str(r[j]), "Plex-M" if k == 0 else "Plex", fs) for k, r in enumerate(rows)) + 5.5
                             for j in range(1, len(cols))]
        if sum(cw) <= TW: break
    assert sum(cw) <= TW + 0.5, (case["num"], sum(cw) / inch)
    extra = (TW - sum(cw)) / (len(cols) - 1); cw = [cw[0]] + [x + extra for x in cw[1:]]
    t = Table(rows, colWidths=cw, repeatRows=1, rowHeights=[14] + [11.4] * len(reg))
    ts = [("FONT", (0, 0), (-1, 0), "Plex-M", fs), ("FONT", (0, 1), (-1, -1), "Plex", fs), ("FONT", (0, 1), (0, -1), "DejaVu", 8),
          ("BACKGROUND", (0, 0), (-1, 0), DARK), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("TEXTCOLOR", (0, 1), (-1, -1), INK),
          ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (2, 0), (3 if case["num"] <= 3 else 2, -1), "CENTER"), ("ALIGN", (0, 0), (0, -1), "CENTER"),
          ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 2), ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
          ("LINEBELOW", (0, 0), (-1, -1), 0.3, FROST), ("LINEBELOW", (0, 0), (-1, 0), 0.8, DARK)]
    for i in range(1, len(rows)):
        if i % 2 == 0: ts.append(("BACKGROUND", (0, i), (-1, i), ICE))
    t.setStyle(TableStyle(ts))
    return t

def difficulty(num): return min(5, 1 + (num - 1) * 5 // 12)

def build(recto_fix, out):
    S = []
    pkind_fixed = {}
    def recto(tag):
        S.append(PageBreak())
        if tag in recto_fix: S.extend([Kind("blank"), PageBreak()])
        S.append(Kind(mark=tag))
    # --- title page
    S += [Kind("title"), Spacer(1, 0.55 * inch), Paragraph("A Snowbound Hotel Mystery", ParagraphStyle("t0", parent=kick, fontSize=11, textColor=MID)),
          Spacer(1, 10), Paragraph("The Thief<br/>Stayed the Night", ParagraphStyle("tt", fontName="PlayfairSC-B", fontSize=34, leading=38, alignment=TA_CENTER, textColor=DARK)),
          Spacer(1, 14), Paragraph("Twelve cozy cases. One snowbound week.<br/>Can you find who did it?", ParagraphStyle("t2", parent=small, fontSize=13, leading=17)),
          Spacer(1, 0.45 * inch), TitleArt(TW, 2.9 * inch), Spacer(1, 0.35 * inch),
          Paragraph("An Elimination Puzzle Book", ParagraphStyle("t3", parent=kick, fontSize=10, textColor=DARK)),
          Paragraph("Blake La Pierre", ParagraphStyle("t4", parent=small, fontSize=11))]
    # --- copyright
    S += [PageBreak(), Kind("nofolio"), Spacer(1, 3.4 * inch)]
    cs = ParagraphStyle("cp", parent=body0, fontSize=9, leading=12, alignment=TA_LEFT)
    for t in ["<i>The Thief Stayed the Night: A Snowbound Hotel Mystery</i>",
              "Copyright © 2026 Blake La Pierre. All rights reserved.",
              "No part of this book may be reproduced in any form without written permission from the author, except for brief quotations in reviews. Readers are welcome to photocopy the guest registers for their own personal use while solving.",
              "This is a work of fiction. The Frostwood Lodge, its staff and its guests are imaginary, and any resemblance to real people or places is coincidental.",
              "First edition, 2026",
              "Set in Crimson Text, Playfair Display SC and IBM Plex Sans Condensed, used under the SIL Open Font License."]:
        S += [Paragraph(t, cs), Spacer(1, 6)]
    # --- contents
    recto("contents")
    S += [Kind(section="Contents"), Spacer(1, 0.3 * inch)] + heading("Frostwood Lodge", "Contents")
    S.append(("TOC",))
    # --- cast
    S += [PageBreak(), Kind(section="The Frostwood Household"), Spacer(1, 0.2 * inch)] + heading("Who’s Who", "The Frostwood Household")
    for n, d in ST.CAST: S.append(Paragraph(f"<b>{n}</b>: {d}", ParagraphStyle("cast", parent=body0, spaceAfter=5)))
    S += [Spacer(1, 6), Paragraph(ST.CAST_NOTE, ParagraphStyle("cn2", parent=small, alignment=TA_JUSTIFY))]
    # --- how to play
    recto("howto")
    S += [Kind(section="How to Solve a Case"), Spacer(1, 0.2 * inch)] + heading("Before You Begin", "How to Solve a Case")
    for t in ["Every case in this book works the same way. First, read the story. It sets the scene and tells you what went missing, when, and where.",
              "Next, study the <b>Register</b>. Every suspect in the case is listed there, along with their room, the day they arrived at the lodge, where they call home, what they do for a living, and one or two details that belong to that case alone (what they ate, what they wore, where they sat). One of them is the culprit.",
              "Finally, work through the <b>Clues</b> in order. Each clue rules some suspects out. Cross them off the register as you go: there is a little box beside every name for exactly that purpose. Pencils are recommended; detectives change their minds. Every clue ends with a line in <i>italics</i> that states the rule exactly.",
              "When you reach the end of the clues, exactly one name will remain. Write it on the Verdict page, then check your answer in the Solutions at the back of the book. The solutions also tell you how many suspects each clue clears, so you can find any slip."]:
        S += [Paragraph(t, body), Spacer(1, 4)]
    S += [Spacer(1, 6), Paragraph("<b>Reading a Room Number</b>", ParagraphStyle("x", parent=body0, alignment=TA_CENTER, textColor=DARK)), Spacer(1, 3)]
    for t in ["The lodge has five guest floors. The <b>first digit</b> is the floor: Room 314 is on the 3rd floor. The 1st floor is the ground floor.",
              "The <b>last two digits</b> (01 to 20) tell you where the room is along its corridor. Rooms 01 to 10 are in the <b>West Wing</b>; rooms 11 to 20 are in the <b>East Wing</b>.",
              "<b>Odd</b> numbers are on the <b>lake side</b> of the corridor; <b>even</b> numbers are on the <b>mountain side</b>.",
              "<b>Across the hall</b>: each odd room faces the next even number (305 faces 306). <b>Next door</b>: the room two numbers away on the same side and floor (305 is next door to 303 and 307). <b>Directly above</b>: same last two digits, one floor up (405 is directly above 305).",
              "Guests who share a room have the same room number. Clues about roommates, neighbours and the rooms above and below always mean guests <i>listed in that case’s register</i>, and that includes guests you have already crossed off. Crossing someone off means they are not the culprit; it does not mean they have left the lodge."]:
        S.append(Paragraph(FL + t, bullet))
    S += [Spacer(1, 8), LodgePlan(TW), Paragraph("The 3rd floor, seen from above. Every floor is laid out the same way.", small)]
    S += [Spacer(1, 10), Paragraph("<b>A Few House Rules</b>", ParagraphStyle("x", parent=body0, alignment=TA_CENTER, textColor=DARK)), Spacer(1, 3)]
    for t in ["Everything you need is written in the book. No trick questions, no outside knowledge, no hidden codes. When a clue mentions a group of cities or jobs, it lists every one of them.",
              "Clues mean exactly what they say. If a clue says a guest was elsewhere, they were.",
              "Nobody gets hurt at Frostwood. The worst crimes here are pranks, pinched pastries and one very salty cake.",
              "The cases get harder as the week goes on: from forty suspects and six clues on Monday to every guest in the lodge and fourteen clues on Saturday night. Each case stands alone, but the story runs through all twelve, so it is best to solve them in order."]:
        S.append(Paragraph(FL + t, bullet))
    # --- prologue
    recto("prologue")
    S += [Kind("opener"), Kind(section="Prologue"), Spacer(1, 0.3 * inch)] + heading("Sunday", "Prologue")
    S.append(Paragraph(runin(ST.PROLOGUE[0]), drop0))
    for t in ST.PROLOGUE[1:]: S.append(Paragraph(t, body))
    # --- cases
    for case, d in zip(CASES, D):
        n = case["num"]; st = ST.S[n]; reg = d["reg"]; N = len(reg)
        sec = f"Case {NUMW[n]} · {st['title']}"
        recto(f"case{n}")
        S += [Kind("opener"), Kind(section=sec), Spacer(1, 0.25 * inch)] + heading(f"Case {NUMW[n]} · {st['when']}", st["title"])
        S.append(Paragraph(f"{N} suspects · {len(case['clues'])} clues · Difficulty <font name='DejaVu' size='9'>{'❄' * difficulty(n)}</font><font name='DejaVu' size='9' color='#c8c8c8'>{'❄' * (5 - difficulty(n))}</font>",
                           ParagraphStyle("dif", parent=small, fontName="Crimson", fontSize=9.5)))
        S.append(Spacer(1, 8))
        txt = [p.replace("{Nw}", words(N)).replace("{N}", str(N)) for p in st["story"]]
        txt = [t[0].upper() + t[1:] if t.startswith(words(N)) else t for t in txt]
        avail = H - TOP - BOT - 0.25 * inch - 110
        for fs, ld in ((11.2, 15), (11.0, 14.6), (10.8, 14.3), (10.6, 14.0)):
            bs = ParagraphStyle("bs", parent=body, fontSize=fs, leading=ld); bs0 = ParagraphStyle("bs0", parent=bs, firstLineIndent=0)
            paras = [Paragraph(runin(txt[0]), bs0)] + [Paragraph(t, bs) for t in txt[1:]]
            hh = sum(p.wrap(TW, H)[1] for p in paras) + 30
            if hh <= avail or hh > avail * 1.25: break
        paras = [Paragraph(runin(txt[0]), bs0)] + [Paragraph(t, bs) for t in txt[1:]]
        S += paras[:-1]
        S += [KeepTogether([paras[-1], Spacer(1, 10), Paragraph("Turn the page to open the Register.", small)]), PageBreak()]
        S += [Paragraph("Register" if n != 12 else "The Complete Register", h1), Flake(), Spacer(1, 4)]
        note = st["note"].replace("{N}", str(N))
        if n == 12:
            occupied = {g["room"] for g in reg}
            empty = [r for r in range(101, 521) if r % 100 and r % 100 <= 20 and r not in occupied]
            note += " The only empty rooms in the lodge are " + ", ".join(map(str, empty[:-1])) + " and " + str(empty[-1]) + "."
        S += [Paragraph(note, ParagraphStyle("n", parent=small, fontSize=9.2, leading=11.5)), Spacer(1, 6), register_table(case, reg), PageBreak()]
        S += heading("The Evidence", "Clues")
        S += [Paragraph("Apply the clues in order, crossing suspects off the register as you go.", small), Spacer(1, 6)]
        for i, cl in enumerate(case["clues"], 1): S.append(clue_block(i, cl))
        S.append(PageBreak())
        S += [Spacer(1, 0.2 * inch)] + heading("Your Verdict", st["item"])
        S += [Paragraph("When only one name remains on the register, write it here, then turn to the solution at the back of the book.", small), Spacer(1, 14)]
        k = len(case["clues"])
        tr = [["Clue"] + [str(i) for i in range(1, k + 1)], ["Left"] + [""] * k]
        cwid = (TW - 0.5 * inch) / k
        tt = Table(tr, colWidths=[0.5 * inch] + [cwid] * k, rowHeights=[14, 22])
        tt.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Plex", 8), ("FONT", (0, 0), (0, -1), "Plex-M", 8), ("GRID", (0, 0), (-1, -1), 0.4, FROST),
                                ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("BACKGROUND", (0, 0), (-1, 0), ICE)]))
        S += [Paragraph("Suspects left after each clue (the solutions give these numbers too):", ParagraphStyle("lt", parent=small, fontSize=9)), Spacer(1, 4), tt, Spacer(1, 18)]
        for lab in ["The culprit is:", "Room:", "Why I’m sure:"]:
            S += [Paragraph(lab, ParagraphStyle("l", parent=body0, fontName="PlayfairSC", textColor=DARK)), Spacer(1, 16), HRFlowable(width="100%", thickness=0.5, color=FROST), Spacer(1, 12)]
        S.pop()
        for _ in range(3): S += [Spacer(1, 22), HRFlowable(width="100%", thickness=0.5, color=FROST)]
        S += [PageBreak(), Spacer(1, 0.1 * inch)] + heading(f"Case {NUMW[n]}", "Detective’s Notes")
        for _ in range(21): S += [Spacer(1, 18.5), HRFlowable(width="100%", thickness=0.4, color=FROST, dash=(1, 2))]
    # --- hints
    recto("hints")
    S += [Kind("opener"), Kind(section="Hints"), Spacer(1, 0.2 * inch)] + heading("Stuck?", "Hints")
    S += [Paragraph("A nudge for each case, without giving the answer away. Try the hints before you turn to the solutions.", small), Spacer(1, 8)]
    import re
    for case in CASES:
        n = case["num"]; titles = [c["t"] for c in case["clues"]]
        def T(m): return f"<b>Clue {titles.index(m.group(1)) + 1}</b> (<i>{m.group(1)}</i>)"
        items = [Paragraph(f"Case {NUMW[n]} · {ST.S[n]['title']}", ParagraphStyle("hh", parent=h2, fontSize=11.5))]
        for h in ST.HINTS[n]: items.append(Paragraph(FL + re.sub(r"\{T:([^}]+)\}", T, h), ParagraphStyle("hb", parent=bullet, fontSize=10.5, leading=13.6)))
        S.append(KeepTogether(items + [Spacer(1, 5)]))
    # --- solutions
    recto("solutions")
    S += [Kind("opener"), Kind(section="Solutions"), Spacer(1, 2.4 * inch)] + heading("No Peeking Until You’re Done", "Solutions")
    S.append(Paragraph("Each solution shows how many suspects every clue clears, then reveals the culprit and what really happened.", small))
    for case, d in zip(CASES, D):
        n = case["num"]; st = ST.S[n]; reg = d["reg"]
        th = next(g for g in reg if g["name"] == d["thief"])
        S += [PageBreak(), Kind(section=f"Solution · Case {NUMW[n]}")] + heading(f"Case {NUMW[n]} · {st['title']} · Solution", th["name"])
        S.append(Paragraph(f"Room {th['room']} · {th['occ']} from {th['home']}", ParagraphStyle("sub", parent=small, fontName="Crimson-SB", textColor=DARK, fontSize=11)))
        S.append(Spacer(1, 6))
        rows = [["Clue", "Cleared", "Left"]]
        for i, (cl, stp) in enumerate(zip(case["clues"], d["steps"]), 1):
            rows.append([Paragraph(f"<b>{i}. {cl['t']}.</b> {cl['s']}.", ParagraphStyle("e", fontName="Crimson", fontSize=9.6, leading=11.6)), str(len(stp["out"])), str(stp["left"])])
        stt = Table(rows, colWidths=[TW - 1.1 * inch, 0.6 * inch, 0.5 * inch], repeatRows=1)
        stt.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Crimson", 10), ("FONT", (0, 0), (-1, 0), "PlayfairSC-B", 9), ("TEXTCOLOR", (0, 0), (-1, 0), DARK), ("FONT", (1, 1), (-1, -1), "Crimson", 10),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LINEBELOW", (0, 0), (-1, 0), 0.8, DARK), ("LINEBELOW", (0, 1), (-1, -1), 0.3, FROST),
            ("LEFTPADDING", (0, 0), (-1, -1), 2), ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]))
        S += [Paragraph(f"Starting suspects: {len(reg)}", ParagraphStyle("ss", parent=small, fontSize=9)), Spacer(1, 2), stt, Spacer(1, 7)]
        last = d["steps"][-1]; lastcl = case["clues"][-1]
        others = [g for g in reg if g["name"] in last["out"]]
        names = [f"{g['name']} (Room {g['room']})" for g in others] + [f"{th['name']} (Room {th['room']})"]
        o = ", ".join(names[:-1]) + " and " + names[-1]
        S.append(Paragraph(f"Before the final clue, {words(last['before'])} suspects remained: {o}. "
                           f"The final clue, <i>{lastcl['t']}</i>, says: <i>{lastcl['b']}</i> Only {th['first']} fits, so {th['first']} {th['last']} is the culprit.",
                           ParagraphStyle("fin", parent=body0, fontSize=10.5, leading=13.8)))
        S.append(Spacer(1, 5))
        S.append(Paragraph(st["confess"].format(first=th["first"], last=th["last"], occ_l=th["occ"].lower(), home=th["home"], room=th["room"]),
                           ParagraphStyle("cf", parent=body, fontSize=10.8, leading=14.4)))
    # --- epilogue
    S += [PageBreak(), Kind("opener"), Kind(section="Epilogue"), Kind(mark="epilogue"), Spacer(1, 0.3 * inch)] + heading("Saturday Night · Sunday Morning", "Epilogue")
    S.append(Paragraph(runin(ST.EPILOGUE[0]), drop0))
    for t in ST.EPILOGUE[1:]: S.append(Paragraph(t, body))
    S += [Spacer(1, 18), Flake(), Spacer(1, 6), Paragraph("The End", ParagraphStyle("end", parent=kick, fontSize=12, textColor=DARK))]
    S += [PageBreak(), Kind("nofolio"), Spacer(1, 2.6 * inch)] + heading("Thank You", "A Note from Frostwood")
    S.append(Paragraph("Thank you for spending a snowbound week at the Frostwood Lodge. If you enjoyed solving these cases, a short review helps other puzzlers find the book, and Mr. Pemberton reads every single one (Gus reads them aloud to him).", ParagraphStyle("ty", parent=body0, alignment=TA_CENTER)))
    return S

def render(recto_fix, out, toc):
    S = build(recto_fix, out)
    # TOC
    for i, x in enumerate(S):
        if isinstance(x, tuple):
            rows = [("Prologue", toc.get("prologue", 0))] + [(f"Case {NUMW[c['num']]} · {ST.S[c['num']]['title']}", toc.get(f"case{c['num']}", 0)) for c in CASES] + \
                   [("Hints", toc.get("hints", 0)), ("Solutions", toc.get("solutions", 0)), ("Epilogue (read after the solutions)", toc.get("epilogue", 0))]
            t = Table([[Paragraph(a, ParagraphStyle("tc", parent=body0, fontSize=11.5)), str(b)] for a, b in rows], colWidths=[TW - 0.5 * inch, 0.5 * inch])
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Crimson", 11), ("FONT", (1, 0), (1, -1), "Crimson", 11.5), ("ALIGN", (1, 0), (1, -1), "RIGHT"), ("LINEBELOW", (0, 0), (-1, -1), 0.3, FROST),
                                   ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
            S[i] = t
    fr = Frame(INNER, BOT, TW, H - TOP - BOT, id="f", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc = Doc(out, pagesize=(W, H), initialFontName="Crimson", title=TITLE + ": A Snowbound Hotel Mystery", author="Blake La Pierre", subject="Elimination puzzle book",
              pageTemplates=[PageTemplate("normal", [fr], onPageEnd=page_end)])
    doc.pkind = {}; doc.marks = {}; doc.section = ""
    doc.build(S)
    return doc.marks, doc.page

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "../interior.pdf"
    fix = set(); toc = {}
    for it in range(40):
        marks, pages = render(fix, out, toc)
        bad = sorted((p, k) for k, p in marks.items() if p % 2 == 0 and k != "epilogue")
        if not bad and marks == toc: break
        if bad: fix ^= {bad[0][1]}
        toc = marks
    print("pages", pages, "marks", marks)
    json.dump(dict(pages=pages, marks=marks), open("../build-info.json", "w"))
