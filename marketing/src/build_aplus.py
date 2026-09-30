"""Build the A+ Content images for every book.

Sizes (Amazon's published minimums, see marketing/a-plus/README.md):
  Standard Image Header With Text ...... 970 x 600
  Standard Three Images & Text ......... 300 x 300 minimum; KDP suggests 600 x 600 -> we export 600 x 600
  Standard Comparison Chart ............ 150 x 300 minimum -> we export 300 x 600
Run: cd marketing/src && python3 build_aplus.py
"""
import math, os
from common import *
from content import TILES, HEADER, WHY, SERIES

OUT = os.path.join(MKT, "a-plus")

def ffit(d, text, face, size, maxw):
    while size > 12 and d.textlength(text, font=font(face, size)) > maxw:
        size -= 1
    return font(face, size)

def chip(d, x, y, s, f):
    w = d.textlength(s, font=f)
    d.rounded_rectangle((x, y, x + w + 36, y + 46), radius=23, outline=GOLD, width=2)
    d.text((x + 18, y + 7), s, font=f, fill=GOLD)
    return y + 58

def header(slug, cover):
    W, H = 970, 600
    im = night_bg(W, H, seed=hash(slug) % 997)
    c = fit(cover, 330, 495)
    paste_shadow(im, c, (56, 42))
    d = ImageDraw.Draw(im)
    h = HEADER[slug]
    x = 440
    d.text((x, 58), h["kicker"], font=font("label-b", 22), fill=GOLD)
    y = 96
    hf = min((ffit(d, l, "title", 50, 495) for l in h["head"]), key=lambda f: f.size)
    for line in h["head"]:
        d.text((x, y), line, font=hf, fill=SNOW); y += hf.size + 12
    y += 8
    y = draw_wrapped(d, x, y, h["body"], font("body-i", 32), PALE, 490, 38) + 14
    for s in h["chips"]:
        y = chip(d, x, y, s, font("label", 24))
    return im

def icon(d, kind, cx, cy, r=38):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=GOLD, width=4)
    if kind == "check":
        d.line([(cx - 17, cy + 2), (cx - 5, cy + 15), (cx + 18, cy - 13)], fill=GOLD, width=6, joint="curve")
    elif kind == "list":
        for i in (-12, 0, 12):
            d.ellipse((cx - 17, cy + i - 3, cx - 11, cy + i + 3), fill=GOLD)
            d.line([(cx - 5, cy + i), (cx + 18, cy + i)], fill=GOLD, width=4)
    elif kind == "bulb":
        d.ellipse((cx - 13, cy - 20, cx + 13, cy + 6), outline=GOLD, width=4)
        d.rectangle((cx - 7, cy + 7, cx + 7, cy + 17), outline=GOLD, width=3)
    elif kind == "logic":
        s = 11
        for i in range(4):
            d.line([(cx - 1.5 * s * 1.35, cy - 1.5 * s * 1.35 + i * s * 1.35), (cx + 1.5 * s * 1.35, cy - 1.5 * s * 1.35 + i * s * 1.35)], fill=GOLD, width=2)
            d.line([(cx - 1.5 * s * 1.35 + i * s * 1.35, cy - 1.5 * s * 1.35), (cx - 1.5 * s * 1.35 + i * s * 1.35, cy + 1.5 * s * 1.35)], fill=GOLD, width=2)
        d.ellipse((cx - 5, cy - 5, cx + 5, cy + 5), fill=GOLD)
    elif kind == "steps":
        for i, hgt in enumerate((10, 20, 30)):
            x0 = cx - 18 + i * 13
            d.rectangle((x0, cy + 15 - hgt, x0 + 9, cy + 15), fill=GOLD)
    elif kind == "star":
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5
            rr = 20 if i % 2 == 0 else 8
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        d.polygon(pts, fill=GOLD)

def why(slug):
    W, H = 970, 600
    im = night_bg(W, H, seed=7 + len(slug), ground=False)
    d = ImageDraw.Draw(im)
    text_c(d, W / 2, 50, "Why These Puzzles", font("title", 56), GOLD)
    w = WHY[slug]
    for i, (k, a, b) in enumerate(w["cols"]):
        cx = 170 + i * 315
        icon(d, k, cx, 230)
        f = min((ffit(d, t, "title-reg", 40, 285) for t in (a, b)), key=lambda f: f.size)
        text_c(d, cx, 295, a, f, SNOW)
        text_c(d, cx, 300 + f.size + 8, b, f, SNOW)
    d.line([(120, 455), (W - 120, 455)], fill=SLATE, width=2)
    text_c(d, W / 2, 482, w["foot"], font("body-i", 36), PALE)
    return im

def series(covers, current=None, heading="The Frostwood Puzzle Books"):
    W, H = 970, 600
    im = night_bg(W, H, seed=33)
    d = ImageDraw.Draw(im)
    text_c(d, W / 2, 30, heading, font("title", 48), GOLD)
    for i, (slug, no, kind) in enumerate(SERIES):
        c = fit(covers[slug], 196, 294)
        x = int(W / 2 + (i - 1) * 300 - c.width / 2)
        y = 108
        if slug == current:
            d.rectangle((x - 7, y - 7, x + c.width + 6, y + c.height + 6), outline=GOLD, width=5)
        paste_shadow(im, c, (x, y), radius=10, offset=(5, 7))
        d = ImageDraw.Draw(im)
        cx = x + c.width / 2
        text_c(d, cx, 420, no.upper(), font("label-b", 26), GOLD)
        text_c(d, cx, 458, kind, ffit(d, "Elimination Mysteries", "title-reg", 32, 280), SNOW)
    return im

def tile(img):
    S = 600
    im = Image.new("RGB", (S, S), SNOW)
    card = paper_card(fit(img, 520, 520), pad=10)
    x, y = (S - card.width) // 2, (S - card.height) // 2
    paste_shadow(im, card, (x, y), radius=10, offset=(4, 6), alpha=70)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, S - 1, S - 1), outline=PALE, width=6)
    return im

def compare_img(cover):
    im = Image.new("RGB", (300, 600), SNOW)
    c = fit(cover, 270, 405)
    paste_shadow(im, c, ((300 - c.width) // 2, (600 - c.height) // 2 - 10), radius=8, offset=(4, 6), alpha=80)
    return im

def main():
    covers = {s: front_cover(s, 200) for s in BOOKS}
    made = []
    for slug in BOOKS:
        od = os.path.join(OUT, slug)
        made.append(save_png(header(slug, covers[slug]), os.path.join(od, "1-header-970x600.png")))
        for i, (page, box, name) in enumerate(TILES[slug], 1):
            made.append(save_png(tile(crop_in(slug, page, box, dpi=300)), os.path.join(od, f"2-sample-{i}-{name}-600x600.png")))
        made.append(save_png(why(slug), os.path.join(od, "3-why-these-puzzles-970x600.png")))
        if slug == "the-advent-clock":
            s = series(covers, None, "Also by Blake La Pierre")
        else:
            s = series(covers, slug)
        made.append(save_png(s, os.path.join(od, "4-frostwood-series-970x600.png")))
    for slug in BOOKS:
        made.append(save_png(compare_img(covers[slug]), os.path.join(OUT, "comparison-chart", f"{slug}-300x600.png")))
    for p in made:
        im = Image.open(p)
        print(os.path.relpath(p, MKT), im.size, os.path.getsize(p) // 1024, "KB", im.mode)

if __name__ == "__main__":
    main()
