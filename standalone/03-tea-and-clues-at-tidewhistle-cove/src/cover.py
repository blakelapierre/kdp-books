"""Front-only Kindle cover JPG, 1600 x 2560 (KDP ideal). Seaside tea room at dusk. Run from src/: python3 cover.py"""
import os, json, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "standalone-03-tea-and-clues-at-tidewhistle-cove-cover.jpg")
G = "/usr/share/fonts/truetype/sand-box/google/"
W, H = 1600, 2560

def vfont(path, size, var=None):
    f = ImageFont.truetype(G + path, size)
    if var:
        try: f.set_variation_by_name(var)
        except Exception: pass
    return f

TEAL = (22, 74, 86); DEEP = (12, 44, 56); SEA = (34, 104, 118); FOAM = (226, 240, 236)
CREAM = (250, 242, 222); GOLD = (240, 196, 110); CORAL = (226, 120, 92); ROCK = (52, 62, 70); WHITE = (255, 255, 255)

def ctext(d, y, text, f, fill, shadow=None):
    w = d.textbbox((0, 0), text, font=f)[2]
    if shadow: d.text(((W - w) / 2 + 4, y + 4), text, font=f, fill=shadow)
    d.text(((W - w) / 2, y), text, font=f, fill=fill)

def main():
    rng = random.Random(3)
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    # sky gradient dusk: teal to gold
    for y in range(int(H * 0.62)):
        t = y / (H * 0.62)
        c = tuple(int(DEEP[i] + (GOLD[i] * 0.85 - DEEP[i]) * t ** 1.6) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    for _ in range(60):
        x, y = rng.uniform(0, W), rng.uniform(0, H * 0.3)
        r = rng.uniform(1.5, 3.5); d.ellipse([x - r, y - r, x + r, y + r], fill=(235, 240, 230))
    # sea
    d.rectangle([0, H * 0.62, W, H], fill=SEA)
    for k in range(40):
        y = H * 0.63 + k * 22
        for _ in range(6):
            x = rng.uniform(0, W); L = rng.uniform(40, 160)
            d.line([(x, y), (x + L, y)], fill=(70, 140, 150), width=3)
    # cliff + lighthouse (left)
    d.polygon([(0, H * 0.50), (W * 0.18, H * 0.47), (W * 0.30, H * 0.55), (W * 0.36, H * 0.64), (0, H * 0.66)], fill=ROCK)
    lx = W * 0.14; ly = H * 0.47
    d.polygon([(lx - 38, ly), (lx + 38, ly), (lx + 26, ly - 260), (lx - 26, ly - 260)], fill=CREAM)
    for b in range(3):
        yb = ly - 50 - b * 80
        d.polygon([(lx - 36 + b * 4, yb), (lx + 36 - b * 4, yb), (lx + 34 - b * 4, yb - 30), (lx - 34 + b * 4, yb - 30)], fill=CORAL)
    d.rectangle([lx - 30, ly - 300, lx + 30, ly - 260], fill=GOLD)
    d.polygon([(lx - 36, ly - 300), (lx + 36, ly - 300), (lx, ly - 345)], fill=DEEP)
    beam = Image.new("RGBA", (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(beam)
    bd.polygon([(lx, ly - 280), (W * 1.1, ly - 600), (W * 1.1, ly - 330)], fill=(255, 230, 160, 55))
    beam = beam.filter(ImageFilter.GaussianBlur(18))
    im.paste(Image.alpha_composite(im.convert("RGBA"), beam).convert("RGB"))
    d = ImageDraw.Draw(im)
    # harbour cottages (right)
    base = H * 0.64
    xs = [W * 0.52, W * 0.63, W * 0.74, W * 0.86]
    cols = [(236, 222, 196), (206, 226, 222), (240, 208, 190), (230, 230, 214)]
    for x, c in zip(xs, cols):
        w, h = 170, rng.uniform(150, 200)
        d.rectangle([x - w / 2, base - h, x + w / 2, base], fill=c)
        d.polygon([(x - w / 2 - 12, base - h), (x + w / 2 + 12, base - h), (x, base - h - 90)], fill=(70, 60, 64))
        for wx in (-45, 45):
            d.rectangle([x + wx - 20, base - h + 40, x + wx + 20, base - h + 85], fill=GOLD)
    # tea room sign on the second cottage
    d.rectangle([xs[1] - 70, base - 60, xs[1] + 70, base - 20], fill=DEEP)
    # big teacup in foreground
    cx, cy = W * 0.5, H * 0.80
    d.ellipse([cx - 360, cy + 150, cx + 360, cy + 240], fill=(232, 236, 230))  # saucer
    d.ellipse([cx - 300, cy + 130, cx + 300, cy + 210], fill=(214, 222, 218))
    d.chord([cx - 250, cy - 180, cx + 250, cy + 200], 0, 180, fill=CREAM)
    d.rectangle([cx - 250, cy - 10, cx + 250, cy + 10], fill=CREAM)
    d.ellipse([cx - 250, cy - 50, cx + 250, cy + 40], fill=(150, 92, 60))  # tea
    d.ellipse([cx - 250, cy - 50, cx + 250, cy + 40], outline=CREAM, width=14)
    d.arc([cx + 200, cy - 10, cx + 360, cy + 140], 270, 90, fill=CREAM, width=34)
    d.line([(cx - 240, cy + 70), (cx + 240, cy + 70)], fill=CORAL, width=10)
    # steam as a question mark
    sf = vfont("Playfair Display/PlayfairDisplay-VariableFont_wght.ttf", 300, "Bold")
    steam = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(steam)
    q = "?"; qw = sd.textbbox((0, 0), q, font=sf)[2]
    sd.text((cx - qw / 2, cy - 420), q, font=sf, fill=(255, 255, 255, 170))
    steam = steam.filter(ImageFilter.GaussianBlur(2))
    im = Image.alpha_composite(im.convert("RGBA"), steam).convert("RGB")
    d = ImageDraw.Draw(im)
    # gull
    for gx, gy, s in [(W * 0.66, H * 0.33, 40), (W * 0.78, H * 0.36, 28)]:
        d.arc([gx - s, gy - s / 2, gx, gy + s / 2], 200, 340, fill=WHITE, width=6)
        d.arc([gx, gy - s / 2, gx + s, gy + s / 2], 200, 340, fill=WHITE, width=6)
    # title band
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(band)
    bd.rectangle([0, 90, W, 760], fill=(10, 36, 46, 150))
    im = Image.alpha_composite(im.convert("RGBA"), band).convert("RGB")
    d = ImageDraw.Draw(im)
    small = vfont("Lora/Lora-VariableFont_wght.ttf", 46, "Medium")
    big = vfont("Playfair Display/PlayfairDisplay-VariableFont_wght.ttf", 150, "Bold")
    mid = vfont("Playfair Display/PlayfairDisplay-Italic-VariableFont_wght.ttf", 92, "Italic")
    sub = vfont("Lora/Lora-Italic-VariableFont_wght.ttf", 54, "Italic")
    auth = vfont("Lora/Lora-VariableFont_wght.ttf", 78, "SemiBold")
    ctext(d, 130, "30 COZY MINI-MYSTERIES TO SOLVE BY EAR", small, GOLD)
    ctext(d, 215, "Tea and Clues", big, CREAM, shadow=(6, 24, 30))
    ctext(d, 400, "at", mid, CREAM, shadow=(6, 24, 30))
    ctext(d, 500, "Tidewhistle Cove", big, CREAM, shadow=(6, 24, 30))
    ctext(d, 680, "Gentle seaside whodunits. Nobody gets hurt.", sub, FOAM)
    ctext(d, H - 170, "Blake La Pierre", auth, CREAM, shadow=(6, 24, 30))
    im.save(OUT, "JPEG", quality=90, optimize=True)
    info = {"width": W, "height": H, "path": os.path.basename(OUT), "bytes": os.path.getsize(OUT)}
    json.dump(info, open(os.path.join(ROOT, "cover-info.json"), "w"), indent=1)
    print(info)

if __name__ == "__main__":
    main()
