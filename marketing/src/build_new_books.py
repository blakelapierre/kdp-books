"""Pinterest pins + A+ images for the Oct 2026 books (Bridges of Frostwood, Porch Swing Crosswords, Stories We Keep).
Run: cd marketing/src && python3 build_new_books.py
Pins -> marketing/social/pinterest/<slug>-pin-1.png ; A+ -> marketing/a-plus/<slug>/"""
import os, json, subprocess, tempfile
from PIL import Image, ImageDraw
from common import REPO, MKT, NAVY, GOLD, PALE, SNOW, SLATE, INK, font, fit, text_c, draw_wrapped, paper_card, paste_shadow, night_bg, save_png, render_page

NEW = {
 "bridges-of-frostwood": dict(dir="series/frostwood/07-bridges-of-frostwood", pdf="frostwood-07-bridges-of-frostwood", asin="B0HN6JKQQV",
   pin_kicker="180 HASHI BRIDGES LOGIC PUZZLES", pin_head=["Can You Connect", "Every Island?"], pin_foot="Easy to Expert · Solutions Included",
   head=("Build the Bridges", "180 cozy logic puzzles from the lodge pond to the lake of islands"),
   tiles=[(10, (0.4, 0.70, 5.6, 4.45), "easy-puzzle"), (106, (0.4, 0.60, 5.6, 8.30), "expert-puzzle"), (180, (0.4, 0.60, 5.6, 4.6), "solutions")]),
 "porch-swing-crosswords": dict(dir="standalone/05-porch-swing-crosswords", pdf="standalone-05-porch-swing-crosswords", asin="B0HN6QXPFG",
   pin_kicker="80 COZY CROSSWORDS FOR ADULTS", pin_head=["Relaxing Puzzles", "Through the Seasons"], pin_foot="Plain Clues · Word Banks · Solutions",
   head=("Slow Down and Solve", "Eighty relaxing, themed crosswords for porch-swing afternoons"),
   tiles=[(11, (0.4, 0.55, 5.6, 6.2), "grid"), (10, (0.4, 0.55, 5.6, 4.9), "clues"), (7, (0.4, 0.55, 5.6, 4.6), "tips")]),
 "stories-we-keep": dict(dir="standalone/06-stories-we-keep", pdf="standalone-06-stories-we-keep", asin="B0HN6TSN7T",
   pin_kicker="A GUIDED MEMORY KEEPSAKE", pin_head=["The Gift of", "Their Stories"], pin_foot="Writing Prompts for Parents & Grandparents",
   head=("Their Stories, Kept", "Gentle prompts that help a parent or grandparent write their life"),
   tiles=[(5, (0.4, 0.55, 5.6, 5.2), "how-it-works"), (9, (0.4, 0.55, 5.6, 4.2), "prompt-page"), (85, (0.4, 0.55, 5.6, 4.2), "letter-page")]),
}
P = lambda s, *a: os.path.join(REPO, NEW[s]["dir"], *a)

def cover(slug, dpi=300):
    ci = json.load(open(P(slug, "cover-info.json"))); bl = ci.get("wrap_in", ci.get("bleed_in", 0.125))
    with tempfile.TemporaryDirectory() as td:
        o = os.path.join(td, "c")
        subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-singlefile", P(slug, NEW[slug]["pdf"] + "-cover.pdf"), o], check=True)
        im = Image.open(o + ".png").convert("RGB")
    s = im.width / ci["width_in"]
    return im.crop((int((ci["width_in"] - bl - 6) * s), int(bl * s), int((ci["width_in"] - bl) * s), int((ci["height_in"] - bl) * s)))

def tile(slug, page, box, dpi=300):
    from PIL import ImageChops
    im = render_page(P(slug, NEW[slug]["pdf"] + "-interior.pdf"), page, dpi)
    im = im.crop(tuple(int(v * dpi) for v in box))
    bb = ImageChops.difference(im, Image.new("RGB", im.size, "white")).convert("L").point(lambda v: 255 if v > 18 else 0).getbbox()
    if bb: p = 18; im = im.crop((max(0, bb[0] - p), max(0, bb[1] - p), min(im.width, bb[2] + p), min(im.height, bb[3] + p)))
    return im

def ffit(d, t, face, size, maxw):
    while size > 12 and d.textlength(t, font=font(face, size)) > maxw: size -= 1
    return font(face, size)

def pin(slug, cv):
    b = NEW[slug]; W, H = 1000, 1500
    im = night_bg(W, H, seed=7 + len(slug), ground=False); d = ImageDraw.Draw(im)
    text_c(d, W / 2, 60, b["pin_kicker"], ffit(d, b["pin_kicker"], "label-b", 36, 880), GOLD); y = 115
    for ln in b["pin_head"]: text_c(d, W / 2, y, ln, ffit(d, ln, "title", 74, 900), SNOW); y += 88
    c = fit(cv, 640, 1290 - y - 50); paste_shadow(im, c, ((W - c.width) // 2, y + 25), radius=16, offset=(8, 12))
    d = ImageDraw.Draw(im); d.rectangle((0, 1300, W, H), fill=SNOW)
    text_c(d, W / 2, 1330, b["pin_foot"], ffit(d, b["pin_foot"], "title-reg", 44, 920), NAVY)
    text_c(d, W / 2, 1405, "by Blake La Pierre  ·  on Amazon", font("body-i", 38), SLATE)
    return im

def header(slug, cv):
    b = NEW[slug]; W, H = 970, 600
    im = night_bg(W, H, seed=3 + len(slug), ground=False); c = fit(cv, 330, 540)
    paste_shadow(im, c, (40, (H - c.height) // 2), radius=12, offset=(6, 8)); d = ImageDraw.Draw(im)
    t = tile(slug, *b["tiles"][0][:2]); card = paper_card(fit(t, 500, 330), pad=12)
    paste_shadow(im, card, (420 + (530 - card.width) // 2, 40), radius=10, offset=(5, 7)); d = ImageDraw.Draw(im)
    text_c(d, 420 + 265, 40 + card.height + 35, b["head"][0], ffit(d, b["head"][0], "title", 46, 500), GOLD)
    draw_wrapped(d, 420 + 265, 40 + card.height + 95, b["head"][1], font("body-i", 28), PALE, 500, 34, center=True)
    return im

def sample(slug, page, box, S=600):
    im = Image.new("RGB", (S, S), SNOW); t = tile(slug, page, box); card = paper_card(fit(t, S - 60, S - 60), pad=10)
    paste_shadow(im, card, ((S - card.width) // 2, (S - card.height) // 2), radius=8, offset=(4, 6), alpha=70)
    return im

def main():
    for slug, b in NEW.items():
        cv = cover(slug)
        print(save_png(pin(slug, cv), os.path.join(MKT, "social", "pinterest", f"{slug}-pin-1.png")))
        o = os.path.join(MKT, "a-plus", slug)
        print(save_png(header(slug, cv), os.path.join(o, "1-header-970x600.png")))
        for i, (pg, box, name) in enumerate(b["tiles"], 1):
            print(save_png(sample(slug, pg, box), os.path.join(o, f"2-sample-{i}-{name}-600x600.png")))

if __name__ == "__main__":
    main()
