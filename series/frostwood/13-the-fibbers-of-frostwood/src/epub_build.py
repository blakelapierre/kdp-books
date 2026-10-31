"""Build the EPUB 3 for The Fibbers of Frostwood (Kindle-ready, phone-friendly).
Run from src/: python3 epub_build.py
"""
from __future__ import annotations
import json, os, shutil, sys, zipfile
from pathlib import Path
from xml.sax.saxutils import escape
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fibgen import holds  # only to word the per-statement checks in the solutions

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
SLUG = "frostwood-13-the-fibbers-of-frostwood"
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
.says { margin: 0.5em 0 0.4em 0; padding: 0; list-style: none; }
.says li { margin: 0.5em 0; }
.who { font-family: "PlexCond", sans-serif; font-weight: 600; color: #1f3a5f; }
.ask { font-family: "PlexCond", sans-serif; font-size: 0.95em; color: #1f3a5f; margin-top: 0.4em; }
.kind { margin: 0.15em 0; }
.tt { font-family: "PlexCond", sans-serif; font-weight: 600; color: #1f3a5f; }
.fb { font-family: "PlexCond", sans-serif; font-weight: 600; color: #1a1a1a; }
.check { font-size: 0.92em; color: #333; margin: 0.15em 0; }
"""

WORDS = {3: "Three", 4: "Four", 5: "Five", 6: "Six"}
BAND_FLAKES = {"Easy": 1, "Medium": 2, "Hard": 3, "Expert": 4}
BAND_FILE = {"Easy": "easy", "Medium": "medium", "Hard": "hard", "Expert": "expert"}

def flakes(n):
    return "\u2744" * n

def kind_span(k):
    return f'<span class="tt">truth-teller \u2744</span>' if k == "truth-teller" else '<span class="fb">fibber</span>'

def cast(names):
    return ", ".join(names[:-1]) + " and " + names[-1]

def says_list(p):
    return "\n".join(f'<li><span class="who">{escape(st["speaker"])}:</span> \u201c{escape(st["text"])}\u201d</li>' for st in p["statements"])

def checks(p):
    a = tuple(p["answer"][nm] == "truth-teller" for nm in p["names"])
    out = []
    for st in p["statements"]:
        form = tuple(st["form"])
        true = holds(form, a)
        k = p["answer"][st["speaker"]]
        assert true == (k == "truth-teller"), (p["num"], st)
        verdict = "true, as a truth-teller\u2019s words must be" if true else "false, as a fibber\u2019s words must be"
        out.append(f'<p class="check">{escape(st["speaker"])} ({k}): \u201c{escape(st["text"])}\u201d is {verdict}.</p>')
    return "".join(out)

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
             "v_pair", "v_tin", "v_bench", "v_mug", "v_lantern", "v_sign"]
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

    page("cover", "cover.xhtml", "Cover", '<div class="center"><img class="ill" src="../images/cover.jpg" alt="Cover of The Fibbers of Frostwood"/></div>')
    page("frontispiece", "frontispiece.xhtml", "Frontispiece", f'''
<p class="kicker">A Frostwood Puzzle Book</p>
<hr class="orn"/>
<h1>The Fibbers<br/>of Frostwood</h1>
<p class="center italic">Book 13</p>
<img class="frontis" src="{img['frontispiece']}" alt="The lodge game tin with two pinecones, a lantern and a mug of cocoa in the snow below Frostwood Lodge"/>
<p class="caption">The pinecone tin comes out after supper.</p>
''')
    page("titlepage", "title.xhtml", "Title Page", f'''
<img class="ill" src="{img['title']}" alt="Frostwood Lodge at night with two pinecones in the snow"/>
<p class="kicker">A Frostwood Puzzle Book · No. 13</p>
<h1>The Fibbers<br/>of Frostwood</h1>
<p class="center italic">{escape(DATA["subtitle"])}</p>
<p class="center" style="margin-top:1.5em">Blake La Pierre</p>
''')
    page("copyright", "copyright.xhtml", "Copyright", '''
<h2>Copyright</h2>
<p class="center">The Fibbers of Frostwood</p>
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

    exl = "\n".join(f'<li><span class="who">{w}:</span> \u201c{t}\u201d</li>' for w, t in
                     [("Ada", "Bram is a fibber."), ("Bram", "Ada and I are the same kind."), ("Clara", "Bram is a truth-teller.")])
    page("howto", "howto.xhtml", "How to Play", f'''
<h2>How to Play</h2>
<img class="ill" src="{img['opener-easy']}" alt="The game tin outside Frostwood Lodge"/>
<p>On snowy evenings at Frostwood, someone always fetches the old tin marked GAME. Inside are pinecones: some dusted white with snow, some bare. Everyone draws one in secret. Draw a <b>snowy</b> pinecone and you are a <b>truth-teller</b> for the round. Draw a <b>bare</b> one and you are a <b>fibber</b>. Then each player says one thing, and the rest of the room has to work out who drew which.</p>
<h3>The rules</h3>
<p><span class="snow">\u2744</span> A <b>truth-teller</b> only says things that are true. A <b>fibber</b> only says things that are false.</p>
<p><span class="snow">\u2744</span> Every player is one or the other. There may be any number of each, even none.</p>
<p><span class="snow">\u2744</span> “Kind” means truth-teller or fibber. “Same kind” means both are truth-tellers or both are fibbers.</p>
<p><span class="snow">\u2744</span> “Exactly two of us four” counts <b>everyone</b> in that game, the speaker too.</p>
<p><span class="snow">\u2744</span> “Either … or …, or both” is true when at least one part is true.</p>
<p><span class="snow">\u2744</span> “If X, then Y” is false only when X happens and Y does not. When X does not happen, it is true.</p>
<p><span class="snow">\u2744</span> Exactly one way of sorting the players fits every statement, and every statement is needed.</p>
<p>No writing in the book is needed. Work it out in your head. Tap <b>Need a hint?</b> for a nudge, or <b>Show answer</b> to see who drew which pinecone, with a check of every statement. Tap <b>Back</b> to return to the game.</p>
<h3>Difficulty</h3>
<p><span class="snow">{flakes(1)}</span> <b>Easy, the Lodge</b>: three players. One statement settles someone straight away.<br/>
<span class="snow">{flakes(2)}</span> <b>Medium, the Village</b>: four players, and counting statements and “if … then …” join in. You will need one “suppose …”.<br/>
<span class="snow">{flakes(3)}</span> <b>Hard, the Railway</b>: five players and a few “suppose …” steps.<br/>
<span class="snow">{flakes(4)}</span> <b>Expert, the Mountain</b>: six players, no plain “X is a …” statements, and a “suppose …” inside a “suppose …”.</p>
<h3>Worked example</h3>
<div class="puzzle">
<p class="puzzle-head">Example \u00b7 {flakes(1)}</p>
<p class="cast">Ada, Bram and Clara are playing.</p>
<ul class="says">{exl}</ul>
<p class="ask">Who is a truth-teller, and who is a fibber?</p>
</div>
<p><b>1.</b> Start with Bram. If Bram is a truth-teller, his words are true, so Ada is the same kind as him: a truth-teller. If Bram is a fibber, his words are false, so Ada is a different kind from him: again a truth-teller. Either way, <b>Ada is a truth-teller</b>.</p>
<p><b>2.</b> Ada tells the truth, so “Bram is a fibber” is true. <b>Bram is a fibber.</b></p>
<p><b>3.</b> Clara says Bram is a truth-teller. That is false, so <b>Clara is a fibber</b>.</p>
<p>Ada drew a snowy pinecone; Bram and Clara drew bare ones.</p>
<p class="center italic" style="margin-top:1.2em">Pour some cocoa. The first game is by the great hearth.</p>
''')

    puzzles = DATA["puzzles"]
    blurbs = {
        "Easy": ("The Lodge", "Games of three around Frostwood Lodge, from the great hearth to the puzzle parlour."),
        "Medium": ("The Village", "The tin travels down the hill to the shops and the green. Four players a game."),
        "Hard": ("The Railway", "Along the Frostwood Express line, station by station. Five players a game."),
        "Expert": ("The Mountain", "High on the mountain, where the snow is deepest. Six players a game."),
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
<p class="puzzle-head">Game No. {n} \u00b7 {flakes(BAND_FLAKES[band])}</p>
<p class="cast">{WORDS[p["players"]]} players {escape(p["spot"])}: {escape(cast(p["names"]))}.</p>
<ul class="says">
{says_list(p)}
</ul>
<p class="ask">Who is a truth-teller, and who is a fibber?</p>
<p class="answer-link"><a href="hints.xhtml#h{n}">Need a hint?</a> \u00b7 <a href="solutions.xhtml#s{n}">Show answer \u2744</a></p>
</div>''')
        page(BAND_FILE[band], f"{BAND_FILE[band]}.xhtml", f"{band}: {place}", "\n".join(parts))

    parts = ["<h2>Hints</h2>", '<p class="center italic">A first step for each game. Tap \u201cBack\u201d to return.</p>', '<hr class="orn"/>']
    for p in puzzles:
        n = p["num"]
        parts.append(f'<div class="sol" id="h{n}"><p class="sol-head">Game No. {n}</p><p>{escape(p["hint"])}</p>'
                     f'<p class="small"><a href="{BAND_FILE[p["band"]]}.xhtml#p{n}">\u2190 Back to the game</a> \u00b7 <a href="solutions.xhtml#s{n}">Show answer</a></p></div>')
    page("hints", "hints.xhtml", "Hints", "\n".join(parts))

    parts = ["<h2>Solutions</h2>", '<p class="center italic">Who drew which pinecone, with a check of every statement. Tap \u201cBack\u201d to return.</p>', '<hr class="orn"/>']
    for p in puzzles:
        n = p["num"]
        kinds = "".join(f'<p class="kind">{escape(nm)}: {kind_span(p["answer"][nm])}</p>' for nm in p["names"])
        parts.append(f'<div class="sol" id="s{n}"><p class="sol-head">Game No. {n} \u00b7 {p["band"]}</p>'
                     f'{kinds}{checks(p)}'
                     f'<p class="small"><a href="{BAND_FILE[p["band"]]}.xhtml#p{n}">\u2190 Back to the game</a></p></div>')
    page("solutions", "solutions.xhtml", "Solutions", "\n".join(parts))

    page("thanks", "thanks.xhtml", "Thank You", f'''
<h2>Thank You</h2>
<img class="ill" src="{img['thanks']}" alt="Frostwood Lodge at night"/>
<p class="center">Thank you for playing every round of the pinecone game in Frostwood.</p>
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
    <dc:title>The Fibbers of Frostwood</dc:title>
    <dc:creator>Blake La Pierre</dc:creator>
    <dc:language>en</dc:language>
    <dc:publisher>Blake La Pierre</dc:publisher>
    <dc:rights>Copyright © 2026 Blake La Pierre</dc:rights>
    <dc:description>{escape(DATA["subtitle"])}. Book 13 of A Frostwood Puzzle Book.</dc:description>
    <dc:subject>Puzzles</dc:subject>
    <dc:subject>Logic puzzles</dc:subject>
    <dc:subject>Brain teasers</dc:subject>
    <meta property="dcterms:modified">2026-10-31T16:00:00Z</meta>
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
