"""Front-only Kindle cover JPG, 1600 x 2560 (KDP ideal ratio). Snowy night, red-brick village post office with lit windows, Christmas tree with a star. Run: python3 cover.py"""
import os, random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "standalone-13-twenty-four-nights-at-the-christmas-post-cover.jpg")
G = "/usr/share/fonts/truetype/sand-box/google/"
W, H = 1600, 2560

def vfont(path, size, var=None):
    f = ImageFont.truetype(G + path, size)
    if var:
        try: f.set_variation_by_name(var)
        except Exception: pass
    return f

NAVY = (22, 34, 70); CREAM = (252, 244, 226); RED = (186, 40, 46); GOLD = (250, 200, 80)
BRICK = (160, 62, 50); SNOW = (244, 248, 255); GREEN = (30, 104, 70); WARM = (255, 214, 120)

def ctext(d, y, text, f, fill, shadow=None, off=5):
    w = d.textbbox((0, 0), text, font=f)[2]
    if shadow: d.text(((W - w) / 2 + off, y + off), text, font=f, fill=shadow)
    d.text(((W - w) / 2, y), text, font=f, fill=fill)

def star(d, cx, cy, r, fill):
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill)

def main():
    rng = random.Random(13)
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        t = min(1, y / (H * 0.7))
        c = tuple(int(a + (b - a) * t) for a, b in zip((14, 22, 52), (58, 78, 130)))
        d.line([(0, y), (W, y)], fill=c)
    # glow behind the post office
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    gd.ellipse([200, 1150, 1400, 2150], fill=(255, 200, 120, 70))
    im = Image.alpha_composite(im.convert("RGBA"), glow.filter(ImageFilter.GaussianBlur(120))).convert("RGB")
    d = ImageDraw.Draw(im)
    # snowy ground
    d.polygon([(0, 1930), (400, 1880), (900, 1910), (1300, 1870), (W, 1900), (W, H), (0, H)], fill=SNOW)
    d.polygon([(0, 2080), (600, 2040), (W, 2100), (W, H), (0, H)], fill=(228, 236, 250))
    # post office building
    bx0, bx1, by0, by1 = 330, 1130, 1380, 1960
    d.rectangle([bx0, by0, bx1, by1], fill=BRICK)
    for row in range(by0 + 20, by1, 44):
        off = 0 if (row // 44) % 2 else 40
        for col in range(bx0 + off, bx1, 80):
            d.rectangle([col, row, col + 74, row + 38], outline=(140, 52, 42), width=3)
    d.polygon([(bx0 - 60, by0 + 4), ((bx0 + bx1) / 2, 1130), (bx1 + 60, by0 + 4)], fill=(70, 50, 60))
    d.polygon([(bx0 - 70, by0 + 8), (bx0 - 20, by0 - 30), ((bx0 + bx1) / 2, 1110), (bx1 + 20, by0 - 30), (bx1 + 70, by0 + 8), ((bx0 + bx1) / 2, 1150)], fill=SNOW)
    # sign
    d.rounded_rectangle([450, 1410, 1010, 1500], 20, fill=CREAM, outline=GOLD, width=6)
    sf = vfont("Fredoka/Fredoka-VariableFont_wdth,wght.ttf", 62, "SemiBold")
    tw = d.textbbox((0, 0), "POST OFFICE", font=sf)[2]
    d.text((730 - tw / 2, 1418), "POST OFFICE", font=sf, fill=RED)
    # windows
    for wx in (400, 860):
        d.rectangle([wx, 1560, wx + 200, 1780], fill=WARM, outline=CREAM, width=12)
        d.line([(wx + 100, 1560), (wx + 100, 1780)], fill=CREAM, width=8)
        d.line([(wx, 1670), (wx + 200, 1670)], fill=CREAM, width=8)
        d.rectangle([wx - 10, 1780, wx + 210, 1800], fill=SNOW)
    # door with wreath
    d.rectangle([660, 1600, 800, 1960], fill=(40, 90, 70))
    d.ellipse([690, 1640, 770, 1720], outline=GREEN, width=18)
    d.polygon([(722, 1712), (738, 1712), (746, 1740), (714, 1740)], fill=RED)
    d.ellipse([772, 1780, 786, 1794], fill=GOLD)
    # red post box
    d.rounded_rectangle([1180, 1760, 1250, 1960], 30, fill=RED)
    d.rectangle([1170, 1770, 1260, 1790], fill=(150, 30, 36))
    d.rounded_rectangle([1170, 1740, 1260, 1770], 20, fill=SNOW)
    # Christmas tree with star and lights
    tx = 1400
    for i, (top, bot, half) in enumerate([(1400, 1640, 150), (1520, 1780, 190), (1650, 1940, 230)]):
        d.polygon([(tx, top), (tx - half, bot), (tx + half, bot)], fill=(24, 92, 60))
        d.polygon([(tx - half + 20, bot - 18), (tx, bot - 50), (tx + half - 20, bot - 18), (tx + half, bot), (tx - half, bot)], fill=SNOW)
    d.rectangle([tx - 25, 1940, tx + 25, 1985], fill=(100, 70, 50))
    for _ in range(40):
        y = rng.randint(1440, 1920); half = 150 + (y - 1400) * 0.32
        x = tx + rng.uniform(-half * 0.8, half * 0.8) * (y - 1400) / 540
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=rng.choice([GOLD, RED, (120, 200, 255), CREAM]))
    star(d, tx, 1380, 62, GOLD)
    # small tree on the left
    for top, bot, half in [(1640, 1820, 100), (1740, 1960, 130)]:
        d.polygon([(200, top), (200 - half, bot), (200 + half, bot)], fill=(28, 84, 58))
    # paper snowflakes and snow
    for _ in range(260):
        x, y, r = rng.randint(0, W), rng.randint(820, 2300), rng.choice([3, 4, 5, 6])
        d.ellipse([x - r, y - r, x + r, y + r], fill=WHITE)
    for cx, cy in [(180, 1000), (1420, 960), (300, 2230), (1300, 2250)]:
        for k in range(6):
            a = k * math.pi / 3
            d.line([(cx, cy), (cx + 60 * math.cos(a), cy + 60 * math.sin(a))], fill=CREAM, width=8)
            d.line([(cx + 34 * math.cos(a), cy + 34 * math.sin(a)), (cx + 50 * math.cos(a + 0.4), cy + 50 * math.sin(a + 0.4))], fill=CREAM, width=5)
    # title panel
    panel = Image.new("RGBA", (W, H), (0, 0, 0, 0)); pd = ImageDraw.Draw(panel)
    pd.rounded_rectangle([80, 100, W - 80, 860], 60, fill=(255, 250, 238, 240), outline=RED + (255,), width=12)
    im = Image.alpha_composite(im.convert("RGBA"), panel).convert("RGB"); d = ImageDraw.Draw(im)
    top = vfont("Fredoka/Fredoka-VariableFont_wdth,wght.ttf", 104, "SemiBold")
    big = vfont("Fredoka/Fredoka-VariableFont_wdth,wght.ttf", 150, "Bold")
    sub = vfont("Nunito/Nunito-VariableFont_wght.ttf", 58, "Bold")
    auth = vfont("Nunito/Nunito-VariableFont_wght.ttf", 92, "ExtraBold")
    ctext(d, 140, "Twenty-Four Nights", top, RED)
    ctext(d, 290, "at the", sub, NAVY)
    ctext(d, 370, "Christmas", big, NAVY, shadow=GOLD, off=6)
    ctext(d, 550, "Post", big, NAVY, shadow=GOLD, off=6)
    ctext(d, 745, "Cozy Mysteries to Solve Out Loud", sub, GREEN)
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(band)
    bd.rounded_rectangle([260, 2340, W - 260, 2490], 50, fill=RED + (240,))
    im = Image.alpha_composite(im.convert("RGBA"), band).convert("RGB"); d = ImageDraw.Draw(im)
    ctext(d, 2358, "Blake La Pierre", auth, CREAM)
    im.save(OUT, "JPEG", quality=92)
    print(OUT, im.size, os.path.getsize(OUT))

WHITE = (255, 255, 255)
if __name__ == "__main__":
    main()
