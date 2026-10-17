"""Build the EPUB 3 for The Lockboxes of Frostwood (Kindle-ready, phone-friendly).
Run from src/: python3 epub_build.py
"""
from __future__ import annotations
import json, os, shutil, zipfile
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
SLUG = "frostwood-09-the-lockboxes-of-frostwood"
OUT = ROOT / f"{SLUG}.epub"
BUILD = ROOT / "tmp" / "epub"
ILL = ROOT / "illustrations"
FONTS = ROOT / "fonts"
COVER = ROOT / f"{SLUG}-cover.jpg"

CSS = """
@namespace epub "http://www.idpf.org/2007/ops";
@font-face { font-family: "CrimsonText"; src: url("../fonts/CrimsonText-Regular.ttf"); font-weight: normal; font-style: normal; }
@font-face { font-family: "CrimsonText"; src: url("../fonts/CrimsonText-Italic.ttf"); font-weight: normal; font-style: italic; }
@font-face { font-family: "CrimsonText"; src: url("../fonts/CrimsonText-Bold.ttf"); font-weight: bold; font-style: normal; }
@font-face { font-family: "PlayfairSC"; src: url("../fonts/PlayfairDisplaySC-Regular.ttf"); font-weight: normal; font-style: normal; }
@font-face { font-family: "PlayfairSC"; src: url("../fonts/PlayfairDisplaySC-Bold.ttf"); font-weight: bold; font-style: normal; }
@font-face { font-family: "PlexCond"; src: url("../fonts/IBMPlexSansCondensed-Regular.ttf"); font-weight: normal; font-style: normal; }
@font-face { font-family: "PlexCond"; src: url("../fonts/IBMPlexSansCondensed-SemiBold.ttf"); font-weight: 600; font-style: normal; }
html, body { margin: 0; padding: 0; }
body { font-family: "CrimsonText", "Georgia", serif; font-size: 1.05em; line-height: 1.45; color: #1a1a1a; }
h1, h2, h3 { font-family: "PlayfairSC", "Georgia", serif; font-weight: bold; text-align: center; color: #1f3a5f; }
h1 { font-size: 1.8em; margin: 1.2em 0 0.4em; }
h2 { font-size: 1.35em; margin: 1.4em 0 0.5em; }
h3 { font-size: 1.15em; margin: 1em 0 0.4em; }
p { margin: 0.6em 0; }
.center { text-align: center; }
.italic { font-style: italic; }
.small { font-size: 0.92em; color: #333; }
.kicker { font-family: "PlayfairSC", serif; font-size: 0.85em; letter-spacing: 0.06em; color: #1f3a5f; text-align: center; }
.gold { color: #8a6a20; }
.snow { font-family: "PlexCond", sans-serif; color: #1f3a5f; }
.puzzle { margin: 1.4em 0 1.6em; padding: 0.6em 0 0.8em; border-bottom: 1px solid #d0d7e0; }
.puzzle-head { font-family: "PlexCond", sans-serif; font-weight: 600; font-size: 0.95em; color: #1f3a5f; margin-bottom: 0.35em; }
.prompt { white-space: pre-wrap; }
.answer-link { font-family: "PlexCond", sans-serif; font-size: 0.9em; margin-top: 0.55em; }
.answer-link a { color: #1f3a5f; text-decoration: underline; }
.sol { margin: 0.9em 0; padding: 0.5em 0; border-bottom: 1px dotted #c5ced8; }
.sol-head { font-family: "PlexCond", sans-serif; font-weight: 600; color: #1f3a5f; }
.sol a { color: #1f3a5f; }
img.ill { max-width: 100%; height: auto; display: block; margin: 0.8em auto; }
img.vignette { max-width: 45%; height: auto; display: block; margin: 0.6em auto; }
img.frontis { max-width: 92%; height: auto; display: block; margin: 0.5em auto; }
.caption { text-align: center; font-style: italic; font-size: 0.9em; color: #444; margin-top: 0.3em; }
.toc a { color: #1f3a5f; text-decoration: none; }
.toc li { margin: 0.35em 0; }
hr.orn { border: none; border-top: 1px solid #ffd27a; width: 40%; margin: 1em auto; }
"""
CSS += """
.clues { margin: 0.5em 0 0.4em 0; padding: 0; list-style: none; }
.clues li { margin: 0.45em 0; }
.guess { font-family: "PlexCond", sans-serif; font-weight: 600; font-size: 1.15em; letter-spacing: 0.18em; color: #1f3a5f; }
.where { font-style: italic; color: #333; margin: 0.2em 0 0.5em; }
.code { font-family: "PlexCond", sans-serif; font-weight: 600; font-size: 1.5em; letter-spacing: 0.25em; color: #1f3a5f; }
.check { font-size: 0.92em; color: #333; margin: 0.15em 0; }
"""

WORDS = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five"}
ORD = ["first", "second", "third", "fourth", "fifth"]
BAND_FLAKES = {"Easy": 1, "Medium": 2, "Hard": 3, "Expert": 4}
BAND_FILE = {"Easy": "easy", "Medium": "medium", "Hard": "hard", "Expert": "expert"}

def flakes(n):
    return "\u2744" * n

def verdict(a, b):
    if a == 0 and b == 0:
        return "Nothing is right."
    parts = []
    if a:
        parts.append(f"{WORDS[a] if not parts else WORDS[a].lower()} {'digit is' if a == 1 else 'digits are'} right and in the right place")
    if b:
        w = WORDS[b] if not parts else WORDS[b].lower()
        parts.append(f"{w} {'digit is' if b == 1 else 'digits are'} right but in the wrong place")
    return "; ".join(parts) + "."

def spaced(g):
    return " ".join(g)

def check_line(code, g, a, b):
    right = [d for i, d in enumerate(g) if code[i] == d]
    wrong = [d for i, d in enumerate(g) if d in code and code[i] != d]
    if not right and not wrong:
        return f"{spaced(g)}: none of {', '.join(g)} is in the code."
    bits = []
    if right: bits.append(f"{' and '.join(right)} in place")
    if wrong: bits.append(f"{' and '.join(wrong)} in the code but moved")
    return f"{spaced(g)}: " + "; ".join(bits) + "."

def xhtml(title, body):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">
<head>
<meta charset="UTF-8"/>
<title>{escape(title)}</title>
<link rel="stylesheet" type="text/css" href="../styles/stylesheet.css"/>
</head>
<body>
{body}
</body>
</html>
'''

def build():
    if BUILD.exists():
        shutil.rmtree(BUILD)
    oebps = BUILD / "OEBPS"
    for d in [BUILD / "META-INF", oebps / "text", oebps / "styles", oebps / "images", oebps / "fonts"]:
        d.mkdir(parents=True)
    (BUILD / "META-INF" / "container.xml").write_text('''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
<rootfiles>
<rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
</rootfiles>
</container>
''', encoding="utf-8")
    (oebps / "styles" / "stylesheet.css").write_text(CSS, encoding="utf-8")
    shutil.copy(COVER, oebps / "images" / "cover.jpg")
    names = ["frontispiece", "title", "opener-easy", "opener-medium", "opener-hard", "opener-expert", "thanks",
             "v_key", "v_lockbox", "v_padlock", "v_tin", "v_lantern", "v_sign"]
    img = {}
    for n in names:
        shutil.copy(ILL / f"{n}.png", oebps / "images" / f"{n}.png")
        img[n] = f"../images/{n}.png"
    for f in FONTS.glob("*.ttf"):
        shutil.copy(f, oebps / "fonts" / f.name)
    vignettes = names[7:]

    manifest = []
    def add_item(id_, href, media, props=None):
        p = f' properties="{props}"' if props else ""
        manifest.append(f'    <item id="{id_}" href="{href}" media-type="{media}"{p}/>')
    add_item("css", "styles/stylesheet.css", "text/css")
    add_item("cover-img", "images/cover.jpg", "image/jpeg", "cover-image")
    for n in names:
        add_item(f"img-{n}", f"images/{n}.png", "image/png")
    for f in sorted((oebps / "fonts").glob("*.ttf")):
        add_item(f"font-{f.stem}", f"fonts/{f.name}", "font/ttf")

    pages = []
    def page(pid, fname, title, body, label=None):
        (oebps / "text" / fname).write_text(xhtml(title, body), encoding="utf-8")
        pages.append((pid, f"text/{fname}", label or title))

    page("cover", "cover.xhtml", "Cover", '<div class="center"><img class="ill" src="../images/cover.jpg" alt="Cover of The Lockboxes of Frostwood"/></div>')
    page("frontispiece", "frontispiece.xhtml", "Frontispiece", f'''
<p class="kicker">A Frostwood Puzzle Book</p>
<hr class="orn"/>
<h1>The Lockboxes<br/>of Frostwood</h1>
<p class="center italic">Book 9</p>
<img class="frontis" src="{img['frontispiece']}" alt="A lockbox, a lantern and a key in the snow below Frostwood Lodge"/>
<p class="caption">The first lockbox waits in the snow below the lodge.</p>
''')
    page("titlepage", "title.xhtml", "Title Page", f'''
<img class="ill" src="{img['title']}" alt="Frostwood Lodge at night with a lockbox in the snow"/>
<p class="kicker">A Frostwood Puzzle Book · No. 9</p>
<h1>The Lockboxes<br/>of Frostwood</h1>
<p class="center italic">{escape(DATA["subtitle"])}</p>
<p class="center" style="margin-top:1.5em">Blake La Pierre</p>
''')
    page("copyright", "copyright.xhtml", "Copyright", '''
<h2>Copyright</h2>
<p class="center">The Lockboxes of Frostwood</p>
<p class="center italic">A Frostwood Puzzle Book</p>
<p class="center" style="margin-top:1.2em">Copyright © 2026 Blake La Pierre. All rights reserved.</p>
<p class="center small">No part of this book may be reproduced without permission, except for brief quotations in reviews.</p>
<p class="center small" style="margin-top:1em">Kindle edition.</p>
''')
    toc = [("howto.xhtml", "How to Play"), ("easy.xhtml", "Easy: The Lodge"), ("medium.xhtml", "Medium: The Village"),
           ("hard.xhtml", "Hard: The Railway"), ("expert.xhtml", "Expert: The Mountain"), ("hints.xhtml", "Hints"),
           ("solutions.xhtml", "Solutions"), ("thanks.xhtml", "Thank You"), ("alsoby.xhtml", "Also by Blake La Pierre")]
    lis = "\n".join(f'<li><a href="{h}">{escape(l)}</a></li>' for h, l in toc)
    page("contents", "contents.xhtml", "Contents", f'<h2>Contents</h2><ol class="toc">{lis}</ol>')

    ex = [("152", 0, 0), ("634", 0, 2), ("496", 1, 0), ("841", 0, 2)]
    exl = "\n".join(f'<li><span class="guess">{spaced(g)}</span><br/>{escape(verdict(a, b))}</li>' for g, a, b in ex)
    page("howto", "howto.xhtml", "How to Play", f'''
<h2>How to Play</h2>
<img class="ill" src="{img['opener-easy']}" alt="Lockbox outside Frostwood Lodge"/>
<p>Every winter, the keepers of Frostwood Lodge hide small brass lockboxes around the lodge, the village, the railway and the mountain. Each one holds a little treat. Guests have already tried some codes on each box, and the lock's tiny window told them how close they came. Their notes are all you get.</p>
<h3>The rules</h3>
<p><span class="snow">\u2744</span> A code is three, four or five digits from 0 to 9, and <b>no digit appears twice</b> in a code. The tried codes never repeat a digit either.</p>
<p><span class="snow">\u2744</span> Each note is exact and describes the <b>whole</b> tried code. “One digit is right and in the right place” means exactly one of its digits is in the code at that same spot, and none of its other digits are in the code at all.</p>
<p><span class="snow">\u2744</span> “Right but in the wrong place” means the digit is in the code, at a different spot. “Nothing is right” means none of those digits are in the code.</p>
<p><span class="snow">\u2744</span> Put the notes together and exactly one code fits them all. Every note is needed.</p>
<p>No writing in the book is needed. Work it out in your head, or keep a scrap of paper handy for the longer locks. Tap <b>Need a hint?</b> to see one digit of the code, or <b>Show answer</b> to see the code with a check of every note. Tap <b>Back</b> to return to the box.</p>
<h3>Difficulty</h3>
<p><span class="snow">{flakes(1)}</span> <b>Easy, the Lodge</b>: three digits, four or five notes, one of them “nothing is right”.<br/>
<span class="snow">{flakes(2)}</span> <b>Medium, the Village</b>: three digits, five or six notes, and no free “nothing is right”.<br/>
<span class="snow">{flakes(3)}</span> <b>Hard, the Railway</b>: four digits, five to seven notes.<br/>
<span class="snow">{flakes(4)}</span> <b>Expert, the Mountain</b>: five digits, seven to nine notes.</p>
<h3>Worked example</h3>
<div class="puzzle">
<p class="puzzle-head">Example · {flakes(1)}</p>
<ul class="clues">{exl}</ul>
</div>
<p><b>1.</b> 1 5 2: nothing is right, so 1, 5 and 2 are not in the code.</p>
<p><b>2.</b> 8 4 1: 1 is out, so 8 and 4 are both in the code, each in a different spot from where it sits here. So 8 is not first and 4 is not second.</p>
<p><b>3.</b> 6 3 4: two of these are in the code. 4 is one of them, so exactly one of 6 and 3 is in.</p>
<p><b>4.</b> 4 9 6: exactly one digit is right and in place, and nothing else here is in the code. 4 is in the code, so it must be the one in place: 4 is first. That also rules out 9 and 6.</p>
<p><b>5.</b> Back to 6 3 4: 6 is out, so 3 is in, and not in the middle. 3 is third, which leaves the middle for 8.</p>
<p>The code is <span class="code">483</span>.</p>
<p class="center italic" style="margin-top:1.2em">Pour some cocoa. The first box is in the boot room.</p>
''')

    puzzles = DATA["puzzles"]
    blurbs = {
        "Easy": ("The Lodge", "Boxes tucked around Frostwood Lodge, from the boot room to the observatory hatch. Three digits each."),
        "Medium": ("The Village", "Down the hill to the shops, the green and the frozen mill pond. Three digits, and no free ‘nothing is right’."),
        "Hard": ("The Railway", "Along the Frostwood Express line, station by station. Four-digit locks."),
        "Expert": ("The Mountain", "High on the mountain, where the snow is deepest. Five-digit locks."),
    }
    for band in ["Easy", "Medium", "Hard", "Expert"]:
        place, blurb = blurbs[band]
        parts = [f"<h2>{band}: {place}</h2>", f'<p class="center snow">{flakes(BAND_FLAKES[band])}</p>',
                 f'<img class="ill" src="{img["opener-" + BAND_FILE[band]]}" alt="{place} scene"/>',
                 f'<p class="center italic">{escape(blurb)}</p>', '<hr class="orn"/>']
        bp = [p for p in puzzles if p["band"] == band]
        for i, p in enumerate(bp):
            if i > 0 and i % 6 == 0:
                vg = vignettes[(p["num"] // 6) % len(vignettes)]
                parts.append(f'<img class="vignette" src="{img[vg]}" alt=""/>')
            n = p["num"]
            cl = "\n".join(f'<li><span class="guess">{spaced(g)}</span><br/>{escape(verdict(a, b))}</li>' for g, a, b in p["clues"])
            parts.append(f'''<div class="puzzle" id="p{n}">
<p class="puzzle-head">Box No. {n} · {flakes(BAND_FLAKES[band])}</p>
<p class="where">Found at {escape(p["spot"])}. {WORDS[p["digits"]]} wheels, no digit twice.</p>
<ul class="clues">
{cl}
</ul>
<p class="answer-link"><a href="hints.xhtml#h{n}">Need a hint?</a> · <a href="solutions.xhtml#s{n}">Show answer \u2744</a></p>
</div>''')
        page(BAND_FILE[band], f"{BAND_FILE[band]}.xhtml", f"{band}: {place}", "\n".join(parts))

    parts = ["<h2>Hints</h2>", '<p class="center italic">One digit of each code. Tap “Back” to return to the box.</p>', '<hr class="orn"/>']
    for p in puzzles:
        n = p["num"]
        parts.append(f'<div class="sol" id="h{n}"><p class="sol-head">Box No. {n}</p><p>The {ORD[p["hint_pos"]]} digit is <b>{p["hint_digit"]}</b>.</p>'
                     f'<p class="small"><a href="{BAND_FILE[p["band"]]}.xhtml#p{n}">\u2190 Back to the box</a> · <a href="solutions.xhtml#s{n}">Show answer</a></p></div>')
    page("hints", "hints.xhtml", "Hints", "\n".join(parts))

    parts = ["<h2>Solutions</h2>", '<p class="center italic">Each answer checks every note. Tap “Back” to return.</p>', '<hr class="orn"/>']
    for p in puzzles:
        n = p["num"]
        checks = "".join(f'<p class="check">{escape(check_line(p["code"], g, a, b))}</p>' for g, a, b in p["clues"])
        parts.append(f'<div class="sol" id="s{n}"><p class="sol-head">Box No. {n} · {p["band"]}</p>'
                     f'<p><span class="code">{p["code"]}</span></p><p class="italic">Inside: {escape(p["treat"])}.</p>{checks}'
                     f'<p class="small"><a href="{BAND_FILE[p["band"]]}.xhtml#p{n}">\u2190 Back to the box</a></p></div>')
    page("solutions", "solutions.xhtml", "Solutions", "\n".join(parts))

    page("thanks", "thanks.xhtml", "Thank You", f'''
<h2>Thank You</h2>
<img class="ill" src="{img['thanks']}" alt="Frostwood Lodge at night"/>
<p class="center">Thank you for opening every lockbox in Frostwood.</p>
<p class="center italic">If you enjoyed this book, a short review on Amazon helps other puzzle lovers find the lodge.</p>
<p class="center" style="margin-top:1.2em">Blake La Pierre</p>
''')
    page("alsoby", "alsoby.xhtml", "Also by Blake La Pierre", '''
<h2>Also by Blake La Pierre</h2>
<p class="kicker">A Frostwood Puzzle Book</p>
<ol>
<li><i>The Thief Stayed the Night</i>: elimination mystery cases</li>
<li><i>Frostwood Express</i>: Train Tracks logic puzzles</li>
<li><i>Stars over Frostwood</i>: Star Battle logic puzzles</li>
<li><i>Tents in Frostwood</i>: Tents and Trees logic puzzles</li>
<li><i>Riddles by the Frostwood Fire</i>: riddles and text logic for Kindle</li>
<li><i>The Frostwood Sketchbook</i>: nonogram picture puzzles</li>
<li><i>Bridges of Frostwood</i>: Hashi bridges logic puzzles</li>
<li><i>Fences of Frostwood</i>: Slitherlink logic puzzles</li>
</ol>
<p class="center italic" style="margin-top:1.5em">More winters at the lodge are on the way.</p>
''')

    nav_lis = "\n".join(f'      <li><a href="{fn.split("/")[1]}">{escape(lab)}</a></li>' for (pid, fn, lab) in pages if pid != "cover")
    (oebps / "text" / "nav.xhtml").write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head><meta charset="UTF-8"/><title>Navigation</title>
<link rel="stylesheet" type="text/css" href="../styles/stylesheet.css"/>
</head>
<body>
<nav epub:type="toc" id="toc">
<h1>Table of Contents</h1>
<ol>
{nav_lis}
</ol>
</nav>
<nav epub:type="landmarks" id="landmarks" hidden="hidden">
<ol>
<li><a epub:type="cover" href="cover.xhtml">Cover</a></li>
<li><a epub:type="toc" href="contents.xhtml">Table of Contents</a></li>
<li><a epub:type="bodymatter" href="howto.xhtml">Start of Content</a></li>
</ol>
</nav>
</body>
</html>
''', encoding="utf-8")
    add_item("nav", "text/nav.xhtml", "application/xhtml+xml", "nav")
    for pid, href, _ in pages:
        add_item(pid, href, "application/xhtml+xml")
    man = "\n".join(manifest)
    sp = "\n".join(f'    <itemref idref="{p[0]}"/>' for p in pages)
    opf = f'''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid" xml:lang="en">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="uid">blake-lapierre-{SLUG}</dc:identifier>
    <dc:title>The Lockboxes of Frostwood</dc:title>
    <dc:creator>Blake La Pierre</dc:creator>
    <dc:language>en</dc:language>
    <dc:publisher>Blake La Pierre</dc:publisher>
    <dc:rights>Copyright © 2026 Blake La Pierre</dc:rights>
    <dc:description>{escape(DATA["subtitle"])}. Book 9 of A Frostwood Puzzle Book.</dc:description>
    <dc:subject>Puzzles</dc:subject>
    <dc:subject>Logic puzzles</dc:subject>
    <dc:subject>Brain teasers</dc:subject>
    <meta property="dcterms:modified">2026-10-17T16:00:00Z</meta>
    <meta name="cover" content="cover-img"/>
  </metadata>
  <manifest>
{man}
  </manifest>
  <spine>
{sp}
  </spine>
</package>
'''
    (oebps / "content.opf").write_text(opf, encoding="utf-8")
    if OUT.exists():
        OUT.unlink()
    with zipfile.ZipFile(OUT, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        for path in sorted(BUILD.rglob("*")):
            if path.is_file():
                arc = str(path.relative_to(BUILD)).replace(os.sep, "/")
                z.write(path, arc, compress_type=zipfile.ZIP_DEFLATED)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")

if __name__ == "__main__":
    build()
