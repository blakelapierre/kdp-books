"""Build a valid EPUB 3 for Riddles by the Frostwood Fire (Kindle-ready).
Run from src/: python3 epub_build.py
"""
from __future__ import annotations
import json, os, re, shutil, zipfile, html
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
OUT = ROOT / "frostwood-05-riddles-by-the-frostwood-fire.epub"
BUILD = ROOT / "tmp" / "epub"
ILL = ROOT / "illustrations"
FONTS = ROOT / "fonts"
COVER = ROOT / "frostwood-05-riddles-by-the-frostwood-fire-cover.jpg"

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

def flakes(n):
    return "❄" * n

def xhtml(title, body, css="../styles/stylesheet.css"):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">
<head>
<meta charset="UTF-8"/>
<title>{escape(title)}</title>
<link rel="stylesheet" type="text/css" href="{css}"/>
</head>
<body>
{body}
</body>
</html>
'''

def esc(s):
    return escape(s).replace("\n", "<br/>")

def build():
    if BUILD.exists():
        shutil.rmtree(BUILD)
    oebps = BUILD / "OEBPS"
    for d in [BUILD / "META-INF", oebps / "text", oebps / "styles", oebps / "images", oebps / "fonts"]:
        d.mkdir(parents=True)

    # mimetype (uncompressed)
    (BUILD / "mimetype").write_text("application/epub+zip", encoding="utf-8")
    (BUILD / "META-INF" / "container.xml").write_text(
        '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
<rootfiles>
<rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
</rootfiles>
</container>
''', encoding="utf-8")

    (oebps / "styles" / "stylesheet.css").write_text(CSS, encoding="utf-8")
    shutil.copy(COVER, oebps / "images" / "cover.jpg")
    # illustrations
    img_map = {}
    for name in ["frontispiece", "title", "opener-easy", "opener-medium", "opener-hard", "opener-expert", "thanks",
                 "v_fire", "v_lantern", "v_kettle", "v_sled", "v_moon", "v_sign"]:
        src = ILL / f"{name}.png"
        if src.exists():
            dst = oebps / "images" / f"{name}.png"
            shutil.copy(src, dst)
            img_map[name] = f"../images/{name}.png"
    for f in FONTS.glob("*.ttf"):
        shutil.copy(f, oebps / "fonts" / f.name)

    puzzles = DATA["puzzles"]
    bands = ["Easy", "Medium", "Hard", "Expert"]
    by_band = {b: [p for p in puzzles if p["band"] == b] for b in bands}
    vignettes = ["v_fire", "v_lantern", "v_kettle", "v_sled", "v_moon", "v_sign"]

    spine = []
    manifest = []
    def add_item(id_, href, media, props=None):
        p = f' properties="{props}"' if props else ""
        manifest.append(f'    <item id="{id_}" href="{href}" media-type="{media}"{p}/>')

    add_item("css", "styles/stylesheet.css", "text/css")
    add_item("cover-img", "images/cover.jpg", "image/jpeg", "cover-image")
    for name in img_map:
        add_item(f"img-{name}", f"images/{name}.png", "image/png")
    for f in sorted((oebps / "fonts").glob("*.ttf")):
        add_item(f"font-{f.stem}", f"fonts/{f.name}", "font/ttf")

    # ---- pages ----
    pages = []  # (id, filename, title, nav_label)

    # cover page
    body = '<div class="center"><img class="ill" src="../images/cover.jpg" alt="Cover"/></div>'
    (oebps / "text" / "cover.xhtml").write_text(xhtml("Cover", body), encoding="utf-8")
    pages.append(("cover", "text/cover.xhtml", "Cover", "Cover"))

    # half title / frontis
    body = f'''
<p class="kicker">A Frostwood Puzzle Book</p>
<hr class="orn"/>
<h1>Riddles by the<br/>Frostwood Fire</h1>
<p class="center italic">Book 5</p>
<img class="frontis" src="{img_map.get('frontispiece','')}" alt="Frontispiece: lodge and campfire"/>
<p class="caption">The lodge hearth waits under a winter sky.</p>
'''
    (oebps / "text" / "frontispiece.xhtml").write_text(xhtml("Frontispiece", body), encoding="utf-8")
    pages.append(("frontispiece", "text/frontispiece.xhtml", "Frontispiece", "Frontispiece"))

    # title
    body = f'''
<img class="ill" src="{img_map.get('title','')}" alt="Title vignette"/>
<p class="kicker">A Frostwood Puzzle Book · No. 5</p>
<h1>Riddles by the<br/>Frostwood Fire</h1>
<p class="center italic">{escape(DATA["subtitle"])}</p>
<p class="center" style="margin-top:1.5em">Blake La Pierre</p>
'''
    (oebps / "text" / "title.xhtml").write_text(xhtml("Title Page", body), encoding="utf-8")
    pages.append(("titlepage", "text/title.xhtml", "Title Page", "Title Page"))

    # copyright
    body = f'''
<h2>Copyright</h2>
<p class="center">Riddles by the Frostwood Fire</p>
<p class="center italic">A Frostwood Puzzle Book</p>
<p class="center" style="margin-top:1.2em">Copyright © 2026 Blake La Pierre. All rights reserved.</p>
<p class="center small">No part of this book may be reproduced without permission, except for brief quotations in reviews.</p>
<p class="center small" style="margin-top:1em">Kindle edition.</p>
'''
    (oebps / "text" / "copyright.xhtml").write_text(xhtml("Copyright", body), encoding="utf-8")
    pages.append(("copyright", "text/copyright.xhtml", "Copyright", "Copyright"))

    # contents (nav also separate)
    toc_items = [
        ("howto.xhtml", "How to Play"),
        ("easy.xhtml", "Easy Riddles"),
        ("medium.xhtml", "Medium Riddles"),
        ("hard.xhtml", "Hard Riddles"),
        ("expert.xhtml", "Expert Riddles"),
        ("solutions.xhtml", "Solutions"),
        ("thanks.xhtml", "Thank You"),
        ("alsoby.xhtml", "Also by Blake La Pierre"),
    ]
    lis = "\n".join(f'<li><a href="{href}">{escape(label)}</a></li>' for href, label in toc_items)
    body = f'<h2>Contents</h2><ol class="toc">{lis}</ol>'
    (oebps / "text" / "contents.xhtml").write_text(xhtml("Contents", body), encoding="utf-8")
    pages.append(("contents", "text/contents.xhtml", "Contents", "Contents"))

    # how to play
    body = f'''
<h2>How to Play</h2>
<img class="ill" src="{img_map.get('opener-easy','')}" alt="Lodge vignette"/>
<p>Welcome to Frostwood Lodge. Outside, snow settles on the pines. Inside, the fire is going, and the chalkboard by the hearth is full of riddles and short logic puzzles.</p>
<p>This Kindle edition is built for your phone. There are <b>no write-in grids</b>. Read each puzzle, think it through, then tap <b>Show answer</b> to jump to the solution. From any solution, tap <b>Back to puzzle</b> to return.</p>
<h3>Difficulty</h3>
<p><span class="snow">{flakes(1)}</span> <b>Easy</b> — clear “what am I?” riddles and gentle logic.<br/>
<span class="snow">{flakes(2)}</span> <b>Medium</b> — twistier wordplay and short deductions.<br/>
<span class="snow">{flakes(3)}</span> <b>Hard</b> — classic brainteasers and tighter clues.<br/>
<span class="snow">{flakes(4)}</span> <b>Expert</b> — ciphers, anagrams, and multi-clue logic.</p>
<h3>Worked example</h3>
<div class="puzzle">
<p class="puzzle-head">Example · Easy</p>
<p class="prompt">I crackle and glow in the lodge fireplace. What am I?</p>
<p class="italic small">Think of the hearth itself on a snowy evening…</p>
<p><b>Answer:</b> fire</p>
</div>
<p>Every puzzle in this book has <b>exactly one intended answer</b>, checked in code. For logic puzzles, an independent solver confirms uniqueness. Spelling may vary slightly (for example, “hot cocoa” vs “cocoa”); the Solutions chapter lists the canonical form.</p>
<p class="center italic" style="margin-top:1.2em">Pour some cocoa. Begin whenever you like.</p>
'''
    (oebps / "text" / "howto.xhtml").write_text(xhtml("How to Play", body), encoding="utf-8")
    pages.append(("howto", "text/howto.xhtml", "How to Play", "How to Play"))

    opener_img = {"Easy": "opener-easy", "Medium": "opener-medium", "Hard": "opener-hard", "Expert": "opener-expert"}
    band_file = {"Easy": "easy", "Medium": "medium", "Hard": "hard", "Expert": "expert"}
    band_flakes = {"Easy": 1, "Medium": 2, "Hard": 3, "Expert": 4}
    band_blurb = {
        "Easy": "Warm up by the fire with clear winter riddles and gentle text logic.",
        "Medium": "The clues twist a little. Keep your cocoa close.",
        "Hard": "Classic brainteasers and tighter Frostwood deductions.",
        "Expert": "Ciphers, anagrams, and the longest chains of clues.",
    }

    for band in bands:
        fname = band_file[band] + ".xhtml"
        oid = band_file[band]
        parts = [f'<h2>{escape(band)}</h2>']
        parts.append(f'<p class="center snow">{flakes(band_flakes[band])}</p>')
        parts.append(f'<img class="ill" src="{img_map[opener_img[band]]}" alt="{band} opener"/>')
        parts.append(f'<p class="center italic">{escape(band_blurb[band])}</p>')
        parts.append('<hr class="orn"/>')
        for i, p in enumerate(by_band[band]):
            if i > 0 and i % 8 == 0:
                vg = vignettes[(i // 8) % len(vignettes)]
                parts.append(f'<img class="vignette" src="{img_map[vg]}" alt=""/>')
            n = p["num"]
            fl = flakes(band_flakes[band])
            parts.append('<div class="puzzle" id="p%d">' % n)
            parts.append(f'<p class="puzzle-head">No. {n} · {fl}</p>')
            parts.append(f'<p class="prompt">{esc(p["prompt"])}</p>')
            parts.append(f'<p class="answer-link"><a href="solutions.xhtml#s{n}">Show answer ❄</a></p>')
            parts.append('</div>')
        (oebps / "text" / fname).write_text(xhtml(band, "\n".join(parts)), encoding="utf-8")
        pages.append((oid, f"text/{fname}", band, f"{band} Riddles"))

    # solutions
    parts = ['<h2>Solutions</h2>', '<p class="center italic">Tap “Back to puzzle” to return.</p>', '<hr class="orn"/>']
    for p in puzzles:
        n = p["num"]
        parts.append(f'<div class="sol" id="s{n}">')
        parts.append(f'<p class="sol-head">No. {n} · {escape(p["band"])}</p>')
        parts.append(f'<p><b>{escape(str(p["answer"]))}</b></p>')
        parts.append(f'<p class="small"><a href="{band_file[p["band"]]}.xhtml#p{n}">← Back to puzzle</a></p>')
        parts.append('</div>')
    (oebps / "text" / "solutions.xhtml").write_text(xhtml("Solutions", "\n".join(parts)), encoding="utf-8")
    pages.append(("solutions", "text/solutions.xhtml", "Solutions", "Solutions"))

    # thanks
    body = f'''
<h2>Thank You</h2>
<img class="ill" src="{img_map.get('thanks','')}" alt="Thank you vignette"/>
<p class="center">Thank you for reading by the Frostwood fire.</p>
<p class="center italic">If you enjoyed this book, a short review on Amazon helps other puzzle lovers find the lodge.</p>
<p class="center" style="margin-top:1.2em">— Blake La Pierre</p>
'''
    (oebps / "text" / "thanks.xhtml").write_text(xhtml("Thank You", body), encoding="utf-8")
    pages.append(("thanks", "text/thanks.xhtml", "Thank You", "Thank You"))

    # also by
    body = '''
<h2>Also by Blake La Pierre</h2>
<p class="kicker">A Frostwood Puzzle Book</p>
<ol>
<li><i>The Thief Stayed the Night</i> — elimination mystery cases</li>
<li><i>Frostwood Express</i> — Train Tracks logic puzzles</li>
<li><i>Stars over Frostwood</i> — Star Battle logic puzzles</li>
<li><i>Tents in Frostwood</i> — Tents and Trees logic puzzles</li>
</ol>
<p class="center italic" style="margin-top:1.5em">More winters at the lodge are on the way.</p>
'''
    (oebps / "text" / "alsoby.xhtml").write_text(xhtml("Also by Blake La Pierre", body), encoding="utf-8")
    pages.append(("alsoby", "text/alsoby.xhtml", "Also by", "Also by Blake La Pierre"))

    # nav.xhtml (EPUB3)
    nav_lis = "\n".join(
        f'      <li><a href="{fn}">{escape(lab)}</a></li>'
        for (_id, fn, _t, lab) in pages if _id != "cover"
    )
    nav = f'''<?xml version="1.0" encoding="UTF-8"?>
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
<li><a epub:type="toc" href="#toc">Table of Contents</a></li>
<li><a epub:type="bodymatter" href="easy.xhtml">Start of Content</a></li>
</ol>
</nav>
</body>
</html>
'''
    (oebps / "text" / "nav.xhtml").write_text(nav, encoding="utf-8")
    add_item("nav", "text/nav.xhtml", "application/xhtml+xml", "nav")

    for pid, href, title, lab in pages:
        props = "svg" if False else None
        if pid == "cover":
            add_item(pid, href, "application/xhtml+xml")
        else:
            add_item(pid, href, "application/xhtml+xml")
        spine.append(pid)

    # content.opf
    man = "\n".join(manifest)
    sp = "\n".join(f'    <itemref idref="{s}"/>' for s in ["cover"] + [p[0] for p in pages if p[0] != "cover"])
    # ensure nav not in spine? It's ok either way; put after contents conceptually — not in spine for cleaner Kindle
    opf = f'''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid" xml:lang="en">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="uid">blake-lapierre-frostwood-05-riddles-by-the-frostwood-fire</dc:identifier>
    <dc:title>Riddles by the Frostwood Fire</dc:title>
    <dc:creator>Blake La Pierre</dc:creator>
    <dc:language>en</dc:language>
    <dc:publisher>Blake La Pierre</dc:publisher>
    <dc:rights>Copyright © 2026 Blake La Pierre</dc:rights>
    <dc:description>{escape(DATA["subtitle"])}. Cozy winter riddles and text logic puzzles set at Frostwood Lodge. Phone-friendly Kindle edition with tap-to-jump answers. Book 5 of A Frostwood Puzzle Book.</dc:description>
    <dc:subject>Puzzles</dc:subject>
    <dc:subject>Riddles</dc:subject>
    <dc:subject>Logic puzzles</dc:subject>
    <meta property="dcterms:modified">2026-10-03T16:00:00Z</meta>
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

    # zip
    if OUT.exists():
        OUT.unlink()
    with zipfile.ZipFile(OUT, "w") as z:
        z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        for path in BUILD.rglob("*"):
            if path.is_file() and path.name != "mimetype":
                arc = str(path.relative_to(BUILD)).replace(os.sep, "/")
                z.write(path, arc, compress_type=zipfile.ZIP_DEFLATED)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
    return OUT

if __name__ == "__main__":
    build()
