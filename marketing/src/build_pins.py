"""Build two 1000 x 1500 Pinterest pins per book (2:3, Pinterest's recommended ratio).
Run: cd marketing/src && python3 build_pins.py
"""
import os
from common import *
from content import TILES, PINS

OUT = os.path.join(MKT, "social", "pinterest")
W, H = 1000, 1500

def ffit(d, text, face, size, maxw):
    while size > 12 and d.textlength(text, font=font(face, size)) > maxw:
        size -= 1
    return font(face, size)

def pin_cover(slug, cover):
    p = PINS[slug]
    im = night_bg(W, H, seed=11 + len(slug), ground=False)
    d = ImageDraw.Draw(im)
    text_c(d, W / 2, 70, p["p1_kicker"], ffit(d, p["p1_kicker"], "label-b", 34, 880), GOLD)
    y = 125
    for line in p["p1_head"]:
        text_c(d, W / 2, y, line, ffit(d, line, "title", 68, 880), SNOW); y += 80
    c = fit(cover, 600, 1270 - y - 60)
    paste_shadow(im, c, ((W - c.width) // 2, y + 30), radius=16, offset=(8, 12))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 1290, W, H), fill=SNOW)
    text_c(d, W / 2, 1325, "Free printable sample with answers", font("title-reg", 46), NAVY)
    text_c(d, W / 2, 1400, "by Blake La Pierre", font("body-i", 38), SLATE)
    return im

def pin_puzzle(slug, cover):
    p = PINS[slug]
    page, box, _ = TILES[slug][p["tile"]]
    if "box" in p:
        page, box = p["box"]
    im = Image.new("RGB", (W, H), SNOW)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 285), fill=NAVY)
    text_c(d, W / 2, 45, p["p2_head"], ffit(d, p["p2_head"], "title", 62, 900), GOLD)
    draw_wrapped(d, W / 2, 140, p["p2_sub"], font("body-i", 38), PALE, 860, 46, center=True)
    card = paper_card(fit(crop_in(slug, page, box, dpi=300), 860, 860), pad=16)
    paste_shadow(im, card, ((W - card.width) // 2, 285 + (955 - card.height) // 2), radius=12, offset=(5, 8), alpha=80)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 1250, W, H), fill=NAVY)
    c = fit(cover, 150, 225)
    im.paste(c, (60, 1263))
    d.text((250, 1290), "Print it free, answer included", font=font("title-reg", 44), fill=GOLD)
    t = BOOKS[slug]["title"]
    d.text((250, 1360), t, font=ffit(d, t, "body-i", 44, 700), fill=SNOW)
    d.text((250, 1420), "by Blake La Pierre", font=font("body-i", 34), fill=PALE)
    return im

def main():
    for slug in BOOKS:
        cover = front_cover(slug, 200)
        for n, fn in ((1, pin_cover), (2, pin_puzzle)):
            path = save_png(fn(slug, cover), os.path.join(OUT, f"{slug}-pin-{n}.png"))
            print(os.path.relpath(path, MKT), Image.open(path).size, os.path.getsize(path) // 1024, "KB")

if __name__ == "__main__":
    main()
