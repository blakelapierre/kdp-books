"""Front-only Kindle cover JPG, 1600 x 2560 (KDP ideal ratio). Cozy independent bookshop at dusk with warm windows and shelves. Run: python3 cover.py"""
import os, random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "standalone-15-clues-between-the-shelves-cover.jpg")
G = "/usr/share/fonts/truetype/sand-box/google/"
W, H = 1600, 2560

def vfont(path, size, var=None):
    f = ImageFont.truetype(G + path, size)
    if var:
        try: f.set_variation_by_name(var)
        except Exception: pass
    return f

NAVY = (28, 42, 68); CREAM = (252, 244, 226); GOLD = (214, 168, 72)
BRICK = (120, 72, 58); WARM = (255, 214, 130); GREEN = (36, 92, 70)
WOOD = (92, 58, 36); WHITE = (255, 255, 255); DEEP = (18, 28, 48)

def ctext(d, y, text, f, fill, shadow=None, off=5):
    w = d.textbbox((0, 0), text, font=f)[2]
    if shadow: d.text(((W - w) / 2 + off, y + off), text, font=f, fill=shadow)
    d.text(((W - w) / 2, y), text, font=f, fill=fill)

def main():
    rng = random.Random(15)
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    # dusk sky
    for y in range(H):
        t = min(1, y / (H * 0.55))
        c = tuple(int(a + (b - a) * t) for a, b in zip((24, 36, 72), (70, 88, 120)))
        d.line([(0, y), (W, y)], fill=c)
    # warm glow behind shop
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    gd.ellipse([180, 1200, 1420, 2200], fill=(255, 190, 110, 80))
    im = Image.alpha_composite(im.convert("RGBA"), glow.filter(ImageFilter.GaussianBlur(110))).convert("RGB")
    d = ImageDraw.Draw(im)
    # pavement
    d.polygon([(0, 1980), (500, 1940), (1100, 1960), (W, 1930), (W, H), (0, H)], fill=(64, 68, 78))
    d.polygon([(0, 2100), (W, 2080), (W, H), (0, H)], fill=(50, 54, 64))
    # bookshop building
    bx0, bx1, by0, by1 = 260, 1340, 1280, 2000
    d.rectangle([bx0, by0, bx1, by1], fill=BRICK)
    for row in range(by0 + 16, by1, 40):
        off = 0 if (row // 40) % 2 else 36
        for col in range(bx0 + off, bx1, 72):
            d.rectangle([col, row, col + 66, row + 34], outline=(100, 58, 46), width=2)
    # roof
    d.polygon([(bx0 - 50, by0 + 6), ((bx0 + bx1) / 2, 1040), (bx1 + 50, by0 + 6)], fill=(48, 40, 52))
    d.polygon([(bx0 - 60, by0 + 10), (bx0 - 10, by0 - 40), ((bx0 + bx1) / 2, 1020), (bx1 + 10, by0 - 40), (bx1 + 60, by0 + 10), ((bx0 + bx1) / 2, 1060)], fill=(230, 232, 240))
    # shop sign
    d.rounded_rectangle([380, 1320, 1220, 1440], 24, fill=CREAM, outline=GOLD, width=8)
    sf = vfont("Fredoka/Fredoka-VariableFont_wdth,wght.ttf", 58, "SemiBold")
    tw = d.textbbox((0, 0), "WILLOW QUILL BOOKS", font=sf)[2]
    d.text((800 - tw / 2, 1345), "WILLOW QUILL BOOKS", font=sf, fill=NAVY)
    # big display windows with shelves
    for wx in (320, 900):
        d.rectangle([wx, 1500, wx + 340, 1880], fill=WARM, outline=CREAM, width=14)
        # shelves of book spines
        for sy in (1540, 1640, 1740):
            d.rectangle([wx + 24, sy, wx + 316, sy + 70], fill=WOOD)
            x = wx + 30
            while x < wx + 300:
                bw = rng.randint(14, 28)
                col = rng.choice([(160, 50, 50), (40, 80, 120), (40, 100, 70), (120, 80, 40), (80, 50, 100), (180, 120, 40)])
                d.rectangle([x, sy + 6, x + bw, sy + 64], fill=col)
                x += bw + 3
        d.rectangle([wx - 8, 1880, wx + 348, 1900], fill=(236, 240, 248))
    # door
    d.rectangle([700, 1560, 900, 2000], fill=(48, 78, 64))
    d.rectangle([720, 1585, 880, 1720], fill=WARM, outline=CREAM, width=8)
    d.ellipse([860, 1780, 880, 1800], fill=GOLD)
    # hanging lantern
    d.rectangle([760, 1460, 840, 1490], fill=GOLD)
    d.polygon([(760, 1490), (800, 1545), (840, 1490)], fill=WARM)
    # window-box flowers
    for wx in (320, 900):
        d.rectangle([wx, 1885, wx + 340, 1935], fill=(40, 90, 60))
        for _ in range(18):
            fx = rng.randint(wx + 10, wx + 320); fy = rng.randint(1888, 1925)
            d.ellipse([fx - 8, fy - 8, fx + 8, fy + 8], fill=rng.choice([(220, 80, 100), (250, 200, 60), (240, 240, 250)]))
    # cat silhouette in right window
    d.ellipse([1120, 1780, 1180, 1835], fill=DEEP)
    d.polygon([(1130, 1790), (1125, 1765), (1140, 1785)], fill=DEEP)
    d.polygon([(1170, 1790), (1175, 1765), (1160, 1785)], fill=DEEP)
    # street lamp
    d.rectangle([100, 1600, 120, 2000], fill=(60, 60, 70))
    d.ellipse([60, 1520, 160, 1620], fill=(255, 220, 140, ))
    glow2 = Image.new("RGBA", (W, H), (0, 0, 0, 0)); g2 = ImageDraw.Draw(glow2)
    g2.ellipse([20, 1480, 200, 1660], fill=(255, 220, 140, 90))
    im = Image.alpha_composite(im.convert("RGBA"), glow2.filter(ImageFilter.GaussianBlur(40))).convert("RGB")
    d = ImageDraw.Draw(im)
    # title panel
    panel = Image.new("RGBA", (W, H), (0, 0, 0, 0)); pd = ImageDraw.Draw(panel)
    pd.rounded_rectangle([70, 80, W - 70, 900], 56, fill=(255, 250, 238, 242), outline=GOLD + (255,), width=10)
    im = Image.alpha_composite(im.convert("RGBA"), panel).convert("RGB"); d = ImageDraw.Draw(im)
    top = vfont("Fredoka/Fredoka-VariableFont_wdth,wght.ttf", 96, "SemiBold")
    big = vfont("Fredoka/Fredoka-VariableFont_wdth,wght.ttf", 118, "Bold")
    sub = vfont("Nunito/Nunito-VariableFont_wght.ttf", 52, "Bold")
    auth = vfont("Nunito/Nunito-VariableFont_wght.ttf", 90, "ExtraBold")
    ctext(d, 130, "Clues Between", top, NAVY)
    ctext(d, 260, "the Shelves", big, GREEN, shadow=GOLD, off=5)
    ctext(d, 430, "Twenty-Eight Cozy Bookshop", sub, NAVY)
    ctext(d, 510, "Mysteries to Solve by Ear", sub, NAVY)
    ctext(d, 640, "Can you solve them before the answer?", sub, (120, 72, 58))
    # tiny books decoration under subtitle
    for i, col in enumerate([(160, 50, 50), (40, 80, 120), (40, 100, 70), (120, 80, 40), (80, 50, 100), (180, 120, 40), (50, 50, 50)]):
        x = 560 + i * 70
        d.rectangle([x, 740, x + 48, 820], fill=col)
        d.rectangle([x + 6, 748, x + 42, 756], fill=CREAM)
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(band)
    bd.rounded_rectangle([260, 2340, W - 260, 2490], 50, fill=GREEN + (240,))
    im = Image.alpha_composite(im.convert("RGBA"), band).convert("RGB"); d = ImageDraw.Draw(im)
    ctext(d, 2358, "Blake La Pierre", auth, CREAM)
    im.save(OUT, "JPEG", quality=92)
    print(OUT, im.size, os.path.getsize(OUT))

if __name__ == "__main__":
    main()
