"""Builds the 6x9 interior PDF (grayscale, no bleed, mirrored margins, embedded fonts) -> ../interior.pdf"""
import json, sys, math, random
sys.path.insert(0, ".")
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak, KeepTogether, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.lib.fonts import addMapping
from reportlab import rl_config
import draw as Dw
from draw import DARK, MID, FROST, ICE, PALE, INK, snowflake, P
import stories as ST

rl_config.canvas_basefontname = "Crimson"
ParagraphStyle.defaults["fontName"] = "Crimson"; ParagraphStyle.defaults["bulletFontName"] = "Crimson"
addMapping("Crimson", 0, 0, "Crimson"); addMapping("Crimson", 0, 1, "Crimson-I"); addMapping("Crimson", 1, 0, "Crimson-B"); addMapping("Crimson", 1, 1, "Crimson-BI")

DATA = json.load(open("../data.json")); DOORS = {int(k): v for k, v in DATA["doors"].items()}
W, H = 6 * inch, 9 * inch
INNER, OUTER, TOP, BOT = 0.75 * inch, 0.55 * inch, 0.7 * inch, 0.75 * inch
TW = W - INNER - OUTER; TH = H - TOP - BOT
TITLE = "The Advent Clock"
WORDS = "One Two Three Four Five Six Seven Eight Nine Ten Eleven Twelve Thirteen Fourteen Fifteen Sixteen Seventeen Eighteen Nineteen Twenty Twenty-One Twenty-Two Twenty-Three Twenty-Four".split()
ORD = lambda k: {1: "1st", 2: "2nd", 3: "3rd"}.get(k, f"{k}th")

class Doc(BaseDocTemplate):
    def handle_pageBegin(self):
        p = self.page + 1; left = INNER if p % 2 == 1 else OUTER
        for t in self.pageTemplates:
            for f in t.frames: f._x1 = left; f._geom()
        super().handle_pageBegin()
    def afterFlowable(self, fl):
        if getattr(fl, "section", None) is not None: self.section = fl.section
        if getattr(fl, "mark", None): self.marks[fl.mark] = self.page

def page_end(c, doc):
    p = doc.page; kind = doc.pkind.get(p, "normal")
    if kind in ("blank", "title", "nofolio"): return
    c.saveState(); c.setFont("Crimson", 9); c.setFillColor(MID)
    c.drawCentredString(W / 2 + ((INNER - OUTER) / 2 if p % 2 else -(INNER - OUTER) / 2), 0.42 * inch, str(p))
    if kind != "opener":
        c.setFont("PlayfairSC", 7.5)
        if p % 2 == 0: c.drawString(OUTER, H - 0.42 * inch, TITLE)
        else: c.drawRightString(W - OUTER, H - 0.42 * inch, getattr(doc, "section", ""))
    c.restoreState()

class Kind(Flowable):
    def __init__(s, kind=None, section=None, mark=None): s.kind = kind; s.section = section; s.mark = mark; s.width = s.height = 0
    def wrap(s, aw, ah): return 0, 0
    def draw(s):
        doc = s.canv._doctemplate
        if s.kind: doc.pkind[doc.page] = s.kind

body = ParagraphStyle("b", fontName="Crimson", fontSize=11.2, leading=15, alignment=TA_JUSTIFY, firstLineIndent=14, textColor=INK)
body0 = ParagraphStyle("b0", parent=body, firstLineIndent=0)
story = ParagraphStyle("st", parent=body0, fontSize=11.4, leading=15.4)
rules = ParagraphStyle("ru", parent=body0, fontSize=10.8, leading=14.2, alignment=TA_LEFT)
h1 = ParagraphStyle("h1", fontName="PlayfairSC-B", fontSize=20, leading=24, alignment=TA_CENTER, textColor=DARK, spaceAfter=2)
kick = ParagraphStyle("k", fontName="PlayfairSC", fontSize=9.5, leading=12, alignment=TA_CENTER, textColor=MID, spaceAfter=4)
h2 = ParagraphStyle("h2", fontName="PlayfairSC-B", fontSize=12.5, leading=15, textColor=DARK, spaceBefore=4, spaceAfter=3)
small = ParagraphStyle("s", fontName="Crimson-I", fontSize=10, leading=13, alignment=TA_CENTER, textColor=colors.Color(.3, .3, .3))
bullet = ParagraphStyle("li", parent=body0, alignment=TA_LEFT, leftIndent=14, firstLineIndent=-12, spaceAfter=4)
hint = ParagraphStyle("hi", parent=body0, fontSize=10.4, leading=13.4, alignment=TA_LEFT, leftIndent=52, firstLineIndent=-52, spaceAfter=5)
clue = ParagraphStyle("cl", parent=body0, fontSize=10.5, leading=13.2, alignment=TA_LEFT, leftIndent=16, firstLineIndent=-16, spaceAfter=1.5)
FL = "<font name='DejaVu' color='#9e9e9e' size='9'>❄</font>&nbsp;&nbsp;"

class Flake(Flowable):
    def __init__(s, r=6): s.r = r; s.width = 0; s.height = 2 * r + 6
    def wrap(s, aw, ah): s.aw = aw; return aw, s.height
    def draw(s):
        c = s.canv; c.setStrokeColor(FROST); c.setLineWidth(0.5)
        c.line(s.aw / 2 - 60, s.r + 3, s.aw / 2 - s.r - 6, s.r + 3); c.line(s.aw / 2 + s.r + 6, s.r + 3, s.aw / 2 + 60, s.r + 3)
        snowflake(c, s.aw / 2, s.r + 3, s.r, DARK)
def heading(k, t): return [Paragraph(k, kick), Paragraph(t, h1), Flake(), Spacer(1, 8)]

class Box(Flowable):
    """calls fn(canvas, 0, 0, w, h) inside a w x h box"""
    def __init__(s, fn, w, h): s.fn = fn; s.width = w; s.height = h
    def wrap(s, aw, ah): return s.width, s.height
    def draw(s): s.fn(s.canv, 0, 0, s.width, s.height)

class Fill(Flowable):
    """takes all remaining height on the page and calls fn(c, 0, 0, w, h)"""
    def __init__(s, fn, minh=100): s.fn = fn; s.minh = minh
    def wrap(s, aw, ah): s.width = aw; s.height = max(ah - 1, s.minh); return aw, s.height
    def draw(s): s.fn(s.canv, 0, 0, s.width, s.height)

def answer_boxes(v, filled=False):
    n = len(v["answer"]); bs = min(0.36 * inch, (TW - 20) / n)
    def f(c, x, y, w, h):
        x0 = (w - n * bs) / 2
        for i in range(n):
            key = i + 1 == v["key"]
            c.setStrokeColor(INK); c.setLineWidth(2.2 if key else 0.8); c.setFillColor(PALE if key else colors.white)
            c.rect(x0 + i * bs + 2, 14, bs - 4, bs - 4, stroke=1, fill=1)
            if filled: c.setFillColor(INK); c.setFont("PlayfairSC-B", bs * 0.5); c.drawCentredString(x0 + i * bs + bs / 2, 14 + bs * 0.22, v["answer"][i])
            if key:
                c.setFont("PlayfairSC", 7.5); c.setFillColor(MID); c.drawCentredString(x0 + i * bs + bs / 2, 3, "key")
    return Box(f, TW, bs + 16)

# ------------------------------------------------------------------ puzzle page renderers
def puzzle_fn(v, sol=False):
    t = v["type"]; fn = getattr(Dw, t)
    return lambda c, x, y, w, h: fn(c, x, y, w, h, v, sol)

def door_header(v):
    d = v["door"]
    def f(c, x, y, w, h):
        c.setFillColor(DARK); c.setFont("PlayfairSC-B", 15); c.drawString(0, h - 14, f"Door {WORDS[d - 1]}")
        c.setFont("Crimson-I", 10.5); c.setFillColor(MID); c.drawRightString(w, h - 13, f"December {d}")
        c.setStrokeColor(FROST); c.setLineWidth(0.5); c.line(0, h - 22, w, h - 22)
    return Box(f, TW, 30)

def logic_page(v):
    fl = [door_header(v), Spacer(1, 2)]
    cl = [Paragraph(f"<b>{i + 1}.</b>&nbsp;&nbsp;{Dw.logic_clue(q)}", clue) for i, q in enumerate(v["clues"])]
    fl += cl + [Spacer(1, 8), Fill(lambda c, x, y, w, h: Dw.logic(c, x, y, w, h, v))]
    return fl

def rules_text(v):
    d = v["door"]; txt = ST.DOORS[d][2]
    fmt = dict(dirs=v.get("dirs", ""), syms=", ".join(v.get("symbols", [])), total=v.get("total", ""), snow="wavy lines", ship="grey dot")
    return txt.format(**fmt)

# ------------------------------------------------------------------ hints
def rc(x): return f"row {x[0] + 1}, column {x[1] + 1}"
def foothold(v):
    t = v["type"]; a = v["answer"]
    if t == "wordsearch":
        w = max(v["words"], key=len); cells = v["placed"][w]; (r0, c0), (r1, c1) = cells[0], cells[1]
        dname = {(0, 1): "across to the right", (1, 0): "down", (1, 1): "diagonally down to the right", (0, -1): "backwards to the left", (-1, 0): "upwards",
                 (-1, -1): "diagonally up to the left", (-1, 1): "diagonally up to the right", (1, -1): "diagonally down to the left"}[(r1 - r0, c1 - c0)]
        return f"{w.title()} starts at {rc(cells[0])} and runs {dname}. The message begins THE KEY IS."
    if t == "caesar": return f"The shift is {v['shift']}: every D stands for A, E for B, and so on. The first word, {v['cipher'].split()[0]}, is {v['plain'].split()[0]}."
    if t == "queens":
        reg = v["regions"]; n = v["n"]; sizes = {}
        for r in range(n):
            for c in range(n): sizes[reg[r][c]] = sizes.get(reg[r][c], 0) + 1
        g = min(sizes, key=sizes.get); st = next(x for x in v["stars"] if reg[x[0]][x[1]] == g)
        return f"The smallest region has {sizes[g]} squares; its star is at {rc(st)}."
    if t == "wordoku": return f"The top row reads {' '.join(v['full'][0])}."
    if t == "maze":
        p = v["path"]; x = p[len(p) // 2]
        return f"The route passes through {rc(x)}, roughly halfway along. The first letter you meet is {a[0]}."
    if t == "nonogram": return {"CANDLE": "The picture is something you light when the power goes out. Row 13 is almost full.", "BELL": "The picture hangs in a tower and rings. Row 12 is almost full."}[a]
    if t == "pyramid":
        V = v["values"]; return f"The second brick from the left in the second row up is {V[1][1]}, and the far-left brick of the bottom row is {V[0][0]}."
    if t == "pigpen": return f"The first two words are {' '.join(v['plain'].split()[:2])}."
    if t == "logic":
        g = v["room"].index(2); return f"{Dw.NAMES[g]} is in Room 3."
    if t == "tents":
        tr = v["trees"][0]; tn = next(x for x in v["tents"] if abs(x[0] - tr[0]) + abs(x[1] - tr[1]) == 1)
        return f"The pine at {rc(tr)} has its snowman at {rc(tn)}."
    if t == "tracks":
        s = v["solution"]; return f"The track runs through {rc(s[1])}, {rc(s[2])} and {rc(s[3])} just after A."
    if t == "akari": return f"There are lanterns at {rc(v['bulbs'][0])} and at {rc(v['bulbs'][-1])}."
    if t == "presents": return f"There are presents at {rc(v['presents'][0])} and at {rc(v['presents'][-1])}."
    if t in ("futoshiki", "skyscrapers", "calcudoku"): return f"The top row reads {' '.join(map(str, v['solution'][0]))}."
    if t == "morse": return f"The first word is {v['plain'].split()[0].strip('.')}."
    if t == "fleet":
        big = next(s for s in v["ships"] if len(s) == 3); return f"The three-square sleigh covers {rc(big[0])} to {rc(big[-1])}."
    if t == "fillin":
        sl = max(v["slots"], key=lambda s: len(s["word"])); return f"{sl['word'].title()} goes in the slot that starts at {rc(sl['cells'][0])}, reading {'across' if sl['d'] == 'A' else 'down'}."
def last_step(v):
    a = v["answer"]; k = max(2, len(a) // 2)
    return f"The answer has {len(a)} letters and begins {a[:k]}. The key letter is its {ORD(v['key'])} letter."

def walkthrough(v):
    t = v["type"]; a = v["answer"]; L = " – ".join(a)
    how = {"wordsearch": lambda: f"With every word crossed out, the unused letters read THE KEY IS {a}.",
           "caesar": lambda: f"Shifting back by {v.get('shift')} turns {v['cipher'].split()[0]} into {v['plain'].split()[0]}, and the whole message reads as above.",
           "queens": lambda: f"The stars, read row by row, sit on the letters {L}.",
           "wordoku": lambda: f"The numbered cells, in order, hold {L}.",
           "maze": lambda: f"The only route from IN to OUT passes the letters {L}, in that order; the other letters are all on dead ends.",
           "nonogram": lambda: f"The picture is a {a.lower()}.",
           "pyramid": lambda: "The bottom row is " + ", ".join(str(x) for x in v.get("values", [[0]])[0]) + f", which turns into {L} with A = 1, B = 2 and so on.",
           "pigpen": lambda: "Reading the symbols with the key gives the message above.",
           "morse": lambda: "Splitting the rings at the spaces and looking each group up in the table gives the message above.",
           "logic": lambda: f"Walking down the corridor from Room 1, the guests are " + ", ".join(Dw.NAMES[g] for g in sorted(range(5), key=lambda g: v['room'][g])) + f": {L}.",
           "tents": lambda: f"Read row by row, the snowmen stand on {L}.",
           "tracks": lambda: f"From A to B the track passes the letters {L}; the other letters are off the line.",
           "akari": lambda: f"Read row by row, the lanterns sit on {L}.",
           "presents": lambda: f"Read row by row, the presents are on {L}.",
           "fleet": lambda: f"Read row by row, the sleighs and sleds cover {L}.",
           "futoshiki": lambda: f"With the key, the numbered cells spell {L}.", "skyscrapers": lambda: f"With the key, the numbered cells spell {L}.",
           "calcudoku": lambda: f"With the key, the numbered cells spell {L}.", "fillin": lambda: f"The numbered circles, in order, hold {L}."}[t]()
    fh = foothold(v)
    if t in ("caesar", "pigpen", "morse", "nonogram", "wordsearch"): return how + f" The key letter is the {ORD(v['key'])} letter, <b>{v['letter']}</b>."
    return "Checkpoint: " + fh + " " + how + f" The key letter is the {ORD(v['key'])} letter, <b>{v['letter']}</b>."

# ------------------------------------------------------------------ solution blocks
def sol_block(v, h):
    d = v["door"]
    def f(c, x, y, w, hh):
        c.setFillColor(DARK); c.setFont("PlayfairSC-B", 11.5); c.drawString(0, hh - 12, f"Door {WORDS[d - 1]}")
        c.setFont("Crimson", 10.5); c.setFillColor(INK)
        c.drawRightString(w, hh - 12, f"Answer: {v['answer']}   ·   key letter {v['letter']}")
        c.setStrokeColor(FROST); c.setLineWidth(0.5); c.line(0, hh - 18, w, hh - 18)
        bh = hh - 30
        t = v["type"]
        if t in ("caesar", "pigpen", "morse"):
            st_ = ParagraphStyle("x", parent=body0, fontSize=11, leading=15, alignment=TA_CENTER)
            txt = {"caesar": f"Shift each letter back by {v.get('shift')}: D→A, E→B, F→C …<br/><br/><b>{v['plain']}</b>",
                   "pigpen": f"Using the key, the symbols read:<br/><br/><b>{v['plain']}</b>",
                   "morse": f"The bells ring out:<br/><br/><b>{v['plain']}</b>"}[t]
            p = Paragraph(txt, st_); pw, ph = p.wrap(w - 40, bh); p.drawOn(c, 20, hh - 30 - ph - 20)
            return
        if t == "logic":
            y0 = Dw.logic(c, 0, 20, w, bh - 20, v, sol=True)
            order = sorted(range(5), key=lambda g: v["room"][g])
            line = " · ".join(f"Room {v['room'][g] + 1}: {Dw.NAMES[g]}, {Dw.TOPS[v['top'][g]]}, {Dw.KNITS[v['knit'][g]]}" for g in order)
            p = Paragraph(line, ParagraphStyle("x", parent=body0, fontSize=9.2, leading=11.5, alignment=TA_CENTER)); pw, ph = p.wrap(w, 60); p.drawOn(c, 0, y0 - ph - 8)
            return
        getattr(Dw, t)(c, 20, 6, w - 40, bh - 6, v, True)
    return Box(f, TW, h)

# ------------------------------------------------------------------ the book
def build(fix):
    S = []
    def page(tag=None, parity=None):
        """new page; parity 'recto'/'verso' inserts a blank page when the fix-list says so"""
        S.append(PageBreak())
        if tag in fix: S.extend([Kind("blank"), PageBreak()])
        if tag: S.append(Kind(mark=tag))
    # title
    S += [Kind("title"), Spacer(1, 0.55 * inch), Paragraph("A Christmas Puzzle Countdown", ParagraphStyle("t0", parent=kick, fontSize=11, textColor=MID)),
          Spacer(1, 10), Paragraph("The Advent<br/>Clock", ParagraphStyle("tt", fontName="PlayfairSC-B", fontSize=40, leading=44, alignment=TA_CENTER, textColor=DARK)),
          Spacer(1, 14), Paragraph("24 doors, 24 puzzles and one hidden star", ParagraphStyle("t2", parent=small, fontSize=13, leading=17)),
          Spacer(1, 0.35 * inch), Box(clock_art, TW, 3.0 * inch), Spacer(1, 0.4 * inch),
          Paragraph("Blake La Pierre", ParagraphStyle("t4", parent=small, fontSize=12))]
    S += [PageBreak(), Kind("nofolio"), Spacer(1, 3.8 * inch)]
    cs = ParagraphStyle("cp", parent=body0, fontSize=9, leading=12, alignment=TA_LEFT)
    for t in ["<i>The Advent Clock: A Christmas Puzzle Countdown</i>", "Copyright © 2026 Blake La Pierre. All rights reserved.",
              "No part of this book may be reproduced in any form without written permission from the author, except for brief quotations in reviews. Readers are welcome to photocopy puzzle pages for their own personal use while solving.",
              "This is a work of fiction. Snowberry Lodge, its guests and its clock are imaginary, and any resemblance to real places or people is coincidental.",
              "First edition, 2026", "Set in Crimson Text, Playfair Display SC and IBM Plex Sans Condensed, used under the SIL Open Font License."]:
        S += [Paragraph(t, cs), Spacer(1, 6)]
    page("contents")
    S += [Kind(section="Contents"), Spacer(1, 0.3 * inch)] + heading("The Advent Clock", "Contents") + [("TOC",)]
    page("prologue")
    S += [Kind(section="The Great Advent Clock"), Spacer(1, 0.1 * inch)] + heading("Snowberry Lodge, December", "The Great Advent Clock")
    S += [Paragraph(t, body if i else body0) for i, t in enumerate(ST.PROLOGUE)]
    page("letter")
    S += [Kind(section="A Letter"), Spacer(1, 0.25 * inch)] + heading("Found in the envelope", "A Letter")
    lt = ParagraphStyle("lt", parent=body0, fontName="Crimson-I", fontSize=12, leading=17, spaceAfter=9)
    S += [Paragraph(t, lt) for t in ST.LETTER]
    page("howto")
    S += [Kind(section="How This Book Works"), Spacer(1, 0.1 * inch)] + heading("Before you begin", "How This Book Works")
    S += [("HOWTO",)]
    page("log")
    S += [Kind(section="The Door Log")] + heading("Keep your key letters here", "The Door Log") + [Box(door_log, TW, TH - 70)]
    for d in range(1, 25):
        v = DOORS[d]; title, text, _ = ST.DOORS[d]
        page(f"door{d}")
        S += [Kind(section=f"Door {WORDS[d - 1]}")] + [Paragraph(f"December {d} · Door {WORDS[d - 1]}", kick), Paragraph(title, h1), Flake(), Spacer(1, 6),
              Paragraph(text, story), Spacer(1, 8), Paragraph("How to solve", h2), Paragraph(rules_text(v), rules), Spacer(1, 10),
              Paragraph("Your answer", ParagraphStyle("ya", parent=h2, alignment=TA_CENTER)), answer_boxes(v),
              Paragraph(f"The heavy box is today’s key letter. Copy it into the Door Log (page {{log}}).", ParagraphStyle("kl", parent=small, fontSize=9.5)),
              Paragraph(f"Hints: pages {{hint1}}, {{hint2}} and {{hint3}} · Solution: page {{sol{d}}}", ParagraphStyle("hl", parent=small, fontSize=9))]
        page()
        S += logic_page(v) if v["type"] == "logic" else [door_header(v), Spacer(1, 6), Fill(puzzle_fn(v))]
    page("eve")
    S += [Kind(section="Christmas Eve")] + heading("Christmas Eve, a quarter to midnight", "The Last Message") + [
        Paragraph("All twenty-four doors are open. Behind the last one is a little card in Ottilie’s handwriting: <i>Put each door’s key letter in the box with that door’s number, and you will know where to go.</i>", body0),
        Spacer(1, 10), Box(ledger, TW, 3.3 * inch), Spacer(1, 8),
        Paragraph("When you have read the message, turn the page.", small)]
    page("midnight")
    S += [Kind(section="Midnight")] + heading("Christmas Eve", "Midnight") + [Paragraph(t, body if i else body0) for i, t in enumerate(ST.EPILOGUE)]
    S += [Spacer(1, 0.3 * inch), Box(lambda c, x, y, w, h: Dw.star(c, w / 2, h / 2, 26, DARK), TW, 70)]
    # hints
    for tier, (name, sub, fn) in enumerate([("Hints I: Nudges", "A gentle push in the right direction", lambda v: ST.NUDGE[v["type"]]),
                                            ("Hints II: Footholds", "One solid fact to start from", foothold),
                                            ("Hints III: Last Steps", "Almost the answer", last_step)], 1):
        page(f"hint{tier}")
        S += [Kind(section=name)] + heading(sub, name)
        for d in range(1, 25):
            S.append(Paragraph(f"<font name='PlayfairSC-B'>Door {d}</font>&nbsp;&nbsp;&nbsp;{fn(DOORS[d])}", hint))
    page("solutions")
    S += [Kind(section="Solutions")] + heading("Look away now if you are still solving", "Solutions")
    for d in range(1, 25):
        if d > 1: page()
        S += [Kind(mark=f"sol{d}"), sol_block(DOORS[d], (TH - 90) * 0.78 if d == 1 else TH * 0.8), Spacer(1, 6),
              Paragraph("<b>How it goes.</b> " + walkthrough(DOORS[d]), ParagraphStyle("wt", parent=body0, fontSize=10.5, leading=14))]
    page("about")
    S += [Kind(section="Thank You"), Spacer(1, 0.5 * inch)] + heading("Thank you", "Thank You for Solving")
    S += [Paragraph("I hope the Great Advent Clock kept you good company through December. If you enjoyed it, a short review on Amazon helps other puzzlers find the book, and it means a great deal to a small, independent author.", body0), Spacer(1, 8),
          Paragraph("If you think you have found a mistake, please check the solution pages first: every puzzle in this book was re-solved by a separate program and has exactly one answer.", body0), Spacer(1, 16),
          Paragraph("Also by Blake La Pierre", h2),
          Paragraph(FL + "<i>The Thief Stayed the Night</i>: a snowbound hotel mystery puzzle book", bullet),
          Paragraph(FL + "<i>Frostwood Express</i>: 200 Train Tracks logic puzzles", bullet)]
    return S

def clock_art(c, x, y, w, h):
    """line-art grandfather clock with 24 little doors"""
    cx = w / 2; cw = 1.35 * inch; top = h - 4
    c.setStrokeColor(DARK); c.setLineWidth(1.2); c.setFillColor(colors.white)
    # hood + face
    c.roundRect(cx - cw / 2, top - 1.0 * inch, cw, 1.0 * inch, 8, stroke=1, fill=1)
    c.circle(cx, top - 0.5 * inch, 0.38 * inch, stroke=1, fill=0); c.circle(cx, top - 0.5 * inch, 0.33 * inch, stroke=1, fill=0)
    for i in range(12):
        a = math.pi / 2 - i * math.pi / 6; r1, r2 = 0.26 * inch, 0.31 * inch
        c.setLineWidth(1.4 if i % 3 == 0 else 0.6); c.line(cx + r1 * math.cos(a), top - 0.5 * inch + r1 * math.sin(a), cx + r2 * math.cos(a), top - 0.5 * inch + r2 * math.sin(a))
    c.setLineWidth(1.4); c.line(cx, top - 0.5 * inch, cx, top - 0.5 * inch + 0.22 * inch); c.line(cx, top - 0.5 * inch, cx + 0.16 * inch * math.cos(math.radians(-60)), top - 0.5 * inch + 0.16 * inch * math.sin(math.radians(-60)))
    star_y = top + 2; Dw.star(c, cx, top + 1, 9, DARK) if False else None
    # body with 24 doors (6 x 4)
    bt = top - 1.0 * inch; bh = 1.7 * inch; bw = cw * 0.86
    c.setLineWidth(1.2); c.rect(cx - bw / 2, bt - bh, bw, bh, stroke=1, fill=0)
    dw, dh = bw / 4, bh / 6
    c.setFont("Plex", 6.5); c.setFillColor(MID)
    for k in range(24):
        r, q = divmod(k, 4); x0 = cx - bw / 2 + q * dw; y0 = bt - (r + 1) * dh
        c.setStrokeColor(MID); c.setLineWidth(0.6); c.rect(x0 + 3, y0 + 3, dw - 6, dh - 6)
        c.drawCentredString(x0 + dw / 2, y0 + dh / 2 - 2.5, str(k + 1))
    # base
    c.setStrokeColor(DARK); c.setLineWidth(1.2); c.rect(cx - cw / 2, bt - bh - 0.2 * inch, cw, 0.2 * inch)
    r = random.Random(3)
    for _ in range(16): snowflake(c, r.uniform(0.05, 0.95) * w, r.uniform(0.25, 0.95) * h, r.uniform(3, 7), colors.Color(.72, .72, .72))
    for sx in (-1, 1):
        c.setStrokeColor(MID); c.setLineWidth(0.8); Dw.pine(c, cx + sx * 1.55 * inch, 0.55 * inch, 0.9 * inch)

def door_log(c, x, y, w, h):
    rh = min(22, (h - 20) / 25); x0 = 0; y0 = h - rh
    c.setFont("PlayfairSC-B", 9); c.setFillColor(DARK)
    c.drawString(x0 + 4, y0 + 6, "Door"); c.drawString(x0 + 60, y0 + 6, "Answer"); c.drawRightString(w - 4, y0 + 6, "Key letter")
    for d in range(1, 25):
        yy = y0 - d * rh
        if d % 2 == 0: c.setFillColor(PALE); c.rect(x0, yy, w, rh, stroke=0, fill=1)
        c.setFillColor(INK); c.setFont("Plex-M", 10); c.drawString(x0 + 8, yy + rh * 0.3, str(d))
        c.setFont("Crimson-I", 8.5); c.setFillColor(MID); c.drawString(x0 + 26, yy + rh * 0.3, f"Dec {d}")
        c.setStrokeColor(FROST); c.setLineWidth(0.6); c.line(x0 + 60, yy + 5, w - 60, yy + 5)
        c.setStrokeColor(INK); c.setLineWidth(1.6); c.setFillColor(colors.white); c.rect(w - 36, yy + 2, rh - 4, rh - 4, stroke=1, fill=1)

def ledger(c, x, y, w, h, sol=False):
    words = DATA["message"].split(); lines = [["THE", "STAR"], ["IS", "IN", "THE"], ["CLOCK", "TOWER"]]
    bs = 0.42 * inch; k = 0; yy = h - bs - 6
    for line in lines:
        n = sum(len(wd) for wd in line) + (len(line) - 1) * 0.6
        xx = (w - n * bs) / 2
        for wd in line:
            for ch in wd:
                c.setStrokeColor(INK); c.setLineWidth(1.4); c.setFillColor(colors.white); c.rect(xx + 2, yy, bs - 4, bs - 4, stroke=1, fill=1)
                c.setFont("Plex-M", 8); c.setFillColor(MID); c.drawCentredString(xx + bs / 2, yy - 11, str(DATA["ledger"][k]))
                if sol: c.setFont("PlayfairSC-B", 16); c.setFillColor(INK); c.drawCentredString(xx + bs / 2, yy + 8, ch)
                xx += bs; k += 1
            xx += bs * 0.6
        yy -= bs + 30
    c.setFont("Crimson-I", 9.5); c.setFillColor(MID); c.drawCentredString(w / 2, yy + bs - 4, "The small number under each box is a door number.")

def fill_placeholders(S, marks):
    out = []
    for f in S:
        if isinstance(f, tuple) and f[0] == "TOC":
            items = [("The Great Advent Clock", "prologue"), ("A Letter", "letter"), ("How This Book Works", "howto"), ("The Door Log", "log")]
            items += [(f"Door {d} · {ST.DOORS[d][0]}", f"door{d}") for d in range(1, 25)]
            items += [("Christmas Eve: The Last Message", "eve"), ("Hints I: Nudges", "hint1"), ("Hints II: Footholds", "hint2"), ("Hints III: Last Steps", "hint3"), ("Solutions", "solutions")]
            data = [[Paragraph(t, ParagraphStyle("tc", parent=body0, fontSize=10.3, leading=12.4)), Paragraph(str(marks.get(k, 0)), ParagraphStyle("tn", parent=body0, fontSize=10.3, leading=12.4, alignment=2))] for t, k in items]
            tb = Table(data, colWidths=[TW - 40, 40]); tb.setStyle(TableStyle([("FONTNAME", (0, 0), (-1, -1), "Crimson"), ("BOTTOMPADDING", (0, 0), (-1, -1), 0.6), ("TOPPADDING", (0, 0), (-1, -1), 0.6)]))
            out.append(tb)
        elif isinstance(f, tuple) and f[0] == "HOWTO":
            for a, b in ST.HOWTO: out.append(Paragraph(FL + f"<b>{a}</b> " + b.format(log=marks.get("log", 0)), bullet))
        elif isinstance(f, Paragraph) and "{" in f.text:
            t = f.text
            for k, v in marks.items(): t = t.replace("{" + k + "}", str(v))
            out.append(Paragraph(t, f.style))
        else: out.append(f)
    return out

from reportlab import rl_config
rl_config.canvas_basefontname = "Crimson"   # avoid an unembedded Helvetica default font resource

def run():
    fix = set(); marks = {}
    for it in range(10):
        doc = Doc("../interior.pdf", pagesize=(W, H), initialFontName="Crimson", leftMargin=INNER, rightMargin=OUTER, topMargin=TOP, bottomMargin=BOT,
                  title="The Advent Clock: A Christmas Puzzle Countdown", author="Blake La Pierre")
        doc.marks = {}; doc.pkind = {}; doc.section = ""
        fr = Frame(INNER, BOT, TW, TH, id="f", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        doc.addPageTemplates([PageTemplate(id="p", frames=[fr], onPageEnd=page_end)])
        doc.build(fill_placeholders(build(fix), marks))
        used = marks; marks = dict(doc.marks); newfix = set(fix)
        for d in range(1, 25):
            if marks[f"door{d}"] % 2 == 1: newfix.add(f"door{d}"); break   # doors open on a left-hand page
        else:
            for tg in ("contents", "hint1", "solutions"):
                if marks[tg] % 2 == 0: newfix.add(tg); break
            else:
                if marks["eve"] % 2 == 1: newfix.add("eve")
        if newfix == fix and used == marks: break
        fix = newfix
    pages = doc.page
    assert used == marks, 'marks did not settle'
    for d in range(1, 25): assert marks[f"door{d}"] % 2 == 0, d
    json.dump(dict(pages=pages, marks=marks), open("../build-info.json", "w"), indent=1)
    print("pages", pages, {k: marks[k] for k in ("contents", "prologue", "log", "door1", "door24", "eve", "hint1", "solutions", "about")})

if __name__ == "__main__":
    run()
