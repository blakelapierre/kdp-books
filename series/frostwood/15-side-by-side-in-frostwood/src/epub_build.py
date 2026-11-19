"""Build the EPUB 3 for Side by Side in Frostwood (Kindle-ready, phone-friendly).
Run from src/: python3 epub_build.py
"""
from __future__ import annotations
import json, os, shutil, sys, zipfile
from pathlib import Path
from xml.sax.saxutils import escape
sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
SLUG = "frostwood-15-side-by-side-in-frostwood"
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
.cast { font-style: italic; color: #333; margin: 0.2em 0 0.5em; }
.clues { margin: 0.5em 0 0.4em 1.4em; padding: 0; }
.clues li { margin: 0.45em 0; }
.ask { font-family: "PlexCond", sans-serif; font-size: 0.95em; color: #1f3a5f; margin-top: 0.4em; }
.order { font-family: "PlexCond", sans-serif; font-weight: 600; color: #1f3a5f; margin: 0.3em 0; }
.check { font-size: 0.92em; color: #333; margin: 0.15em 0; }
"""

WORDS = {4: "Four", 5: "Five", 6: "Six", 7: "Seven"}
WHO = {"Easy": "guests", "Medium": "neighbours", "Hard": "travellers", "Expert": "friends"}
BAND_FLAKES = {"Easy": 1, "Medium": 2, "Hard": 3, "Expert": 4}
BAND_FILE = {"Easy": "easy", "Medium": "medium", "Hard": "hard", "Expert": "expert"}

def flakes(n):
    return "\u2744" * n

def cast(names):
    return ", ".join(names[:-1]) + " and " + names[-1]

def clue_list(p):
    return "\n".join(f"<li>{escape(c['text'])}</li>" for c in p["clues"])

def order_line(p):
    return " \u00b7 ".join(f"{i + 1} {escape(nm)}" for i, nm in enumerate(p["answer"]))

def checks(p):
    return "".join(f'<p class="check">\u2713 {escape(c["text"])}</p>' for c in p["clues"])

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
             "v_pegs", "v_mugs", "v_bench", "v_sleds", "v_lantern", "v_sign"]
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

    page("cover", "cover.xhtml", "Cover", '<div class="center"><img class="ill" src="../images/cover.jpg" alt="Cover of Side by Side in Frostwood"/></div>')
    page("frontispiece", "frontispiece.xhtml", "Frontispiece", f'''
<p class="kicker">A Frostwood Puzzle Book</p>
<hr class="orn"/>
<h1>Side by Side<br/>in Frostwood</h1>
<p class="center italic">Book 15</p>
<img class="frontis" src="{img['frontispiece']}" alt="Frostwood Lodge at night above the boot room wall, with five numbered pegs of scarves, mittens and hats, and mugs of cocoa on a bench"/>
<p class="caption">Five pegs, five scarves, and somebody always asks whose is whose.</p>
''')
    page("titlepage", "title.xhtml", "Title Page", f'''
<img class="ill" src="{img['title']}" alt="Frostwood Lodge at night with a row of pegs below"/>
<p class="kicker">A Frostwood Puzzle Book · No. 15</p>
<h1>Side by Side<br/>in Frostwood</h1>
<p class="center italic">{escape(DATA["subtitle"])}</p>
<p class="center" style="margin-top:1.5em">Blake La Pierre</p>
''')
    page("copyright", "copyright.xhtml", "Copyright", '''
<h2>Copyright</h2>
<p class="center">Side by Side in Frostwood</p>
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

    exl = "\n".join(f"<li>{t}</li>" for t in ["Clara is not at either end of the row.", "Bram is somewhere to the left of Ada.",
                                                "Dov is right next to Bram.", "Dov has an odd-numbered peg."])
    page("howto", "howto.xhtml", "How to Play", f'''
<h2>How to Play</h2>
<img class="ill" src="{img['opener-easy']}" alt="The numbered peg rail in the Frostwood Lodge boot room"/>
<p>Everything at Frostwood seems to come in rows: pegs in the boot room, stalls at the winter market, seats in the observation car, sledges at the top of Long Hill. And somebody always wants to know who is where. In every puzzle a few friends are lined up side by side in places numbered from 1 on the left. A handful of clues tell you about the line-up. Work out exactly who has which place.</p>
<h3>The rules</h3>
<p><span class="snow">\u2744</span> Places are numbered <b>1, 2, 3 …</b> from <b>left to right</b>. Each person has exactly one place, and no two people share a place.</p>
<p><span class="snow">\u2744</span> \u201cRight next to\u201d means in the very next place, on either side. \u201cNot next to\u201d means there is at least one place between them.</p>
<p><span class="snow">\u2744</span> \u201cDirectly to the left of\u201d means the very next place to the left. \u201cSomewhere to the left of\u201d means anywhere to the left, near or far.</p>
<p><span class="snow">\u2744</span> \u201cSomewhere between Ada and Bram\u201d means further right than one of them and further left than the other.</p>
<p><span class="snow">\u2744</span> \u201cExactly two places between\u201d counts only the places in between, not their own. \u201cAt one end\u201d means place 1 or the last place.</p>
<p><span class="snow">\u2744</span> Exactly one line-up fits every clue, and every clue is needed.</p>
<p>No writing in the book is needed. Work it out in your head (it helps to picture the row). Tap <b>Need a hint?</b> for a first step, or <b>Show answer</b> to see the line-up with every clue ticked off. Tap <b>Back</b> to return to the puzzle.</p>
<h3>Difficulty</h3>
<p><span class="snow">{flakes(1)}</span> <b>Easy, the Lodge</b>: four guests, simple clues. Take the clues one at a time.<br/>
<span class="snow">{flakes(2)}</span> <b>Medium, the Village</b>: five neighbours, and \u201cnot next to\u201d, \u201cbetween\u201d and gap clues join in.<br/>
<span class="snow">{flakes(3)}</span> <b>Hard, the Railway</b>: six travellers, no clue that names a place outright, and you will need one or two \u201csuppose \u2026\u201d tests.<br/>
<span class="snow">{flakes(4)}</span> <b>Expert, the Mountain</b>: seven friends and three to six \u201csuppose \u2026\u201d tests.</p>
<h3>Worked example</h3>
<div class="puzzle">
<p class="puzzle-head">Example \u00b7 {flakes(1)}</p>
<p class="cast">Four guests hang their coats on the pegs in the boot room, numbered 1 to 4 from left to right: Ada, Bram, Clara and Dov.</p>
<ol class="clues">{exl}</ol>
<p class="ask">Who has which peg?</p>
</div>
<p><b>1.</b> Bram is somewhere to the left of Ada, so Bram is not on peg 4 and Ada is not on peg 1.</p>
<p><b>2.</b> Dov has an odd peg: 1 or 3. Clara is not at an end: 2 or 3.</p>
<p><b>3.</b> Suppose Dov has peg 3. Then Clara must have peg 2, and Bram, right next to Dov, must have peg 4. But Bram cannot be on peg 4. So <b>Dov has peg 1</b>.</p>
<p><b>4.</b> Bram is right next to Dov, so <b>Bram has peg 2</b>. Clara is not at an end, so <b>Clara has peg 3</b>, and <b>Ada has peg 4</b>.</p>
<p>The line-up is 1 Dov \u00b7 2 Bram \u00b7 3 Clara \u00b7 4 Ada. Check: Bram is left of Ada, Dov is next to Bram, Clara is in the middle. \u2713</p>
<p class="center italic" style="margin-top:1.2em">Kick the snow off your boots. The first row of pegs is just inside the door.</p>
''')

    puzzles = DATA["puzzles"]
    blurbs = {
        "Easy": ("The Lodge", "Rows of rooms, pegs, bunks and armchairs all around Frostwood Lodge. Four guests a puzzle."),
        "Medium": ("The Village", "Down the hill to the market stalls, the cottages and the skating huts. Five neighbours a puzzle."),
        "Hard": ("The Railway", "Seats, berths and lockers along the Frostwood Express line. Six travellers a puzzle."),
        "Expert": ("The Mountain", "Huts, bunks and sledge lanes high on the mountain. Seven friends a puzzle."),
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
            parts.append(f'''<div class="puzzle" id="p{n}">
<p class="puzzle-head">Puzzle No. {n} \u00b7 {flakes(BAND_FLAKES[band])}</p>
<p class="cast">{WORDS[p["people"]]} {WHO[band]} {escape(p["setting"])}, numbered 1 to {p["people"]} from left to right: {escape(cast(p["names"]))}.</p>
<ol class="clues">
{clue_list(p)}
</ol>
<p class="ask">Who has which {escape(p["noun"])}?</p>
<p class="answer-link"><a href="hints.xhtml#h{n}">Need a hint?</a> \u00b7 <a href="solutions.xhtml#s{n}">Show answer \u2744</a></p>
</div>''')
        page(BAND_FILE[band], f"{BAND_FILE[band]}.xhtml", f"{band}: {place}", "\n".join(parts))

    parts = ["<h2>Hints</h2>", '<p class="center italic">A first step for each puzzle. Tap \u201cBack\u201d to return.</p>', '<hr class="orn"/>']
    for p in puzzles:
        n = p["num"]
        parts.append(f'<div class="sol" id="h{n}"><p class="sol-head">Puzzle No. {n}</p><p>{escape(p["hint"])}</p>'
                     f'<p class="small"><a href="{BAND_FILE[p["band"]]}.xhtml#p{n}">\u2190 Back to the puzzle</a> \u00b7 <a href="solutions.xhtml#s{n}">Show answer</a></p></div>')
    page("hints", "hints.xhtml", "Hints", "\n".join(parts))

    parts = ["<h2>Solutions</h2>", '<p class="center italic">The line-up from left to right, with every clue ticked off. Tap \u201cBack\u201d to return.</p>', '<hr class="orn"/>']
    for p in puzzles:
        n = p["num"]
        parts.append(f'<div class="sol" id="s{n}"><p class="sol-head">Puzzle No. {n} \u00b7 {p["band"]}</p>'
                     f'<p class="order">{order_line(p)}</p>{checks(p)}'
                     f'<p class="small"><a href="{BAND_FILE[p["band"]]}.xhtml#p{n}">\u2190 Back to the puzzle</a></p></div>')
    page("solutions", "solutions.xhtml", "Solutions", "\n".join(parts))

    page("thanks", "thanks.xhtml", "Thank You", f'''
<h2>Thank You</h2>
<img class="ill" src="{img['thanks']}" alt="Frostwood Lodge at night"/>
<p class="center">Thank you for sorting out every row in Frostwood.</p>
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
<li><i>The Lockboxes of Frostwood</i>: crack-the-code logic puzzles for Kindle</li>
<li><i>Snow Paths of Frostwood</i>: Nurikabe logic puzzles</li>
<li><i>Chimneys of Frostwood</i>: Skyscrapers logic puzzles</li>
<li value="13"><i>The Fibbers of Frostwood</i>: truth-teller and fibber logic puzzles for Kindle</li>
<li><i>The Icicles of Frostwood</i>: Futoshiki logic puzzles</li>
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
    <dc:title>Side by Side in Frostwood</dc:title>
    <dc:creator>Blake La Pierre</dc:creator>
    <dc:language>en</dc:language>
    <dc:publisher>Blake La Pierre</dc:publisher>
    <dc:rights>Copyright © 2026 Blake La Pierre</dc:rights>
    <dc:description>{escape(DATA["subtitle"])}. Book 15 of A Frostwood Puzzle Book.</dc:description>
    <dc:subject>Puzzles</dc:subject>
    <dc:subject>Logic puzzles</dc:subject>
    <dc:subject>Brain teasers</dc:subject>
    <meta property="dcterms:modified">2026-11-19T16:00:00Z</meta>
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
