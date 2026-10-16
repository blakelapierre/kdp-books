"""Front-only Kindle cover JPG, 1600 x 2560 (KDP ideal). Candlelit cottage at evening. Run: python3 cover.py"""
import os, json, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "standalone-07-three-clues-by-candlelight-cover.jpg")
G = "/usr/share/fonts/truetype/sand-box/google/"
W, H = 1600, 2560

def vfont(path, size, var=None):
    f = ImageFont.truetype(G + path, size)
    if var:
        try: f.set_variation_by_name(var)
        except Exception: pass
    return f

NIGHT = (18, 22, 40); DEEP = (28, 34, 58); WARM = (72, 42, 28)
CREAM = (250, 236, 210); GOLD = (240, 196, 110); AMBER = (255, 180, 80)
GLOW = (255, 220, 140); STONE = (62, 58, 52); ROOF = (48, 40, 38)
WHITE = (255, 252, 245); FOAM = (230, 220, 200)

def ctext(d, y, text, f, fill, shadow=None):
    w = d.textbbox((0, 0), text, font=f)[2]
    if shadow: d.text(((W - w) / 2 + 3, y + 3), text, font=f, fill=shadow)
    d.text(((W - w) / 2, y), text, font=f, fill=fill)

def main():
    rng = random.Random(7)
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    # night sky gradient
    for y in range(int(H * 0.55)):
        t = y / (H * 0.55)
        c = tuple(int(NIGHT[i] + (DEEP[i] - NIGHT[i]) * t) for i in range(3))
        # warm toward horizon
        c = tuple(int(c[i] + (WARM[i] - c[i]) * (t ** 2) * 0.55) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    # stars
    for _ in range(90):
        x, y = rng.uniform(0, W), rng.uniform(0, H * 0.38)
        r = rng.uniform(1.0, 2.8)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(235, 230, 210))
    # ground
    d.rectangle([0, H * 0.55, W, H], fill=(32, 36, 30))
    for k in range(30):
        y = H * 0.56 + k * 18
        d.line([(0, y), (W, y)], fill=(40 + k, 44, 36), width=2)
    # cottage body
    cx, base = W * 0.5, H * 0.72
    bw, bh = 780, 420
    left, top = cx - bw / 2, base - bh
    d.rectangle([left, top, left + bw, base], fill=(118, 92, 70))
    # timber framing hints
    for x in (left + 40, left + bw / 2, left + bw - 40):
        d.line([(x, top), (x, base)], fill=(70, 52, 40), width=8)
    d.line([(left, top + bh * 0.45), (left + bw, top + bh * 0.45)], fill=(70, 52, 40), width=6)
    # roof
    d.polygon([(left - 50, top), (left + bw + 50, top), (cx, top - 280)], fill=ROOF)
    d.polygon([(left - 30, top), (left + bw + 30, top), (cx, top - 250)], fill=(58, 48, 44))
    # chimney
    d.rectangle([cx + 180, top - 220, cx + 250, top - 40], fill=STONE)
    # smoke
    smoke = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(smoke)
    for i, (sx, sy, sr) in enumerate([(cx + 215, top - 260, 28), (cx + 230, top - 310, 36), (cx + 210, top - 360, 30)]):
        sd.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(200, 200, 210, 50 - i * 10))
    smoke = smoke.filter(ImageFilter.GaussianBlur(12))
    im = Image.alpha_composite(im.convert("RGBA"), smoke).convert("RGB")
    d = ImageDraw.Draw(im)
    # glowing windows
    windows = [(cx - 220, top + 120), (cx + 80, top + 120), (cx - 70, top + 260)]
    sizes = [(110, 130), (110, 130), (90, 100)]
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    for (wx, wy), (ww, wh) in zip(windows, sizes):
        gd.rectangle([wx, wy, wx + ww, wy + wh], fill=(255, 200, 100, 220))
        # mullions
        gd.line([(wx + ww / 2, wy), (wx + ww / 2, wy + wh)], fill=(80, 50, 30, 200), width=4)
        gd.line([(wx, wy + wh / 2), (wx + ww, wy + wh / 2)], fill=(80, 50, 30, 200), width=4)
        # outer glow
        gd.ellipse([wx - 40, wy - 30, wx + ww + 40, wy + wh + 40], fill=(255, 180, 80, 40))
    glow = glow.filter(ImageFilter.GaussianBlur(2))
    im = Image.alpha_composite(im.convert("RGBA"), glow).convert("RGB")
    d = ImageDraw.Draw(im)
    # door
    dx = cx - 40
    d.rectangle([dx, base - 200, dx + 90, base], fill=(60, 40, 28))
    d.ellipse([dx + 60, base - 110, dx + 72, base - 98], fill=GOLD)
    # foreground candle and table hint
    tx, ty = W * 0.5, H * 0.86
    d.ellipse([tx - 420, ty + 40, tx + 420, ty + 160], fill=(48, 36, 28))  # table top oval
    # candlestick
    d.rectangle([tx - 18, ty - 40, tx + 18, ty + 50], fill=(180, 150, 90))
    d.ellipse([tx - 50, ty + 40, tx + 50, ty + 70], fill=(160, 130, 70))
    # candle
    d.rectangle([tx - 14, ty - 160, tx + 14, ty - 40], fill=CREAM)
    # flame
    flame = Image.new("RGBA", (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(flame)
    fd.ellipse([tx - 22, ty - 220, tx + 22, ty - 150], fill=(255, 230, 120, 230))
    fd.polygon([(tx, ty - 250), (tx - 18, ty - 180), (tx + 18, ty - 180)], fill=(255, 160, 60, 240))
    fd.ellipse([tx - 80, ty - 240, tx + 80, ty - 100], fill=(255, 200, 80, 45))
    flame = flame.filter(ImageFilter.GaussianBlur(3))
    im = Image.alpha_composite(im.convert("RGBA"), flame).convert("RGB")
    d = ImageDraw.Draw(im)
    # title band
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(band)
    bd.rectangle([0, 80, W, 720], fill=(12, 16, 28, 165))
    im = Image.alpha_composite(im.convert("RGBA"), band).convert("RGB")
    d = ImageDraw.Draw(im)
    small = vfont("Lora/Lora-VariableFont_wght.ttf", 42, "Medium")
    big = vfont("Playfair Display/PlayfairDisplay-VariableFont_wght.ttf", 118, "Bold")
    mid = vfont("Playfair Display/PlayfairDisplay-Italic-VariableFont_wght.ttf", 78, "Italic")
    sub = vfont("Lora/Lora-Italic-VariableFont_wght.ttf", 44, "Italic")
    auth = vfont("Lora/Lora-VariableFont_wght.ttf", 72, "SemiBold")
    ctext(d, 120, "150 COZY WHAT-AM-I RIDDLES IN THREE CLUES", small, GOLD)
    ctext(d, 200, "Three Clues", big, CREAM, shadow=(8, 12, 24))
    ctext(d, 340, "by", mid, CREAM, shadow=(8, 12, 24))
    ctext(d, 430, "Candlelight", big, CREAM, shadow=(8, 12, 24))
    ctext(d, 590, "Kitchen, garden, fireside and more. Pause, then guess.", sub, FOAM)
    ctext(d, H - 160, "Blake La Pierre", auth, CREAM, shadow=(8, 12, 24))
    im.save(OUT, "JPEG", quality=90, optimize=True)
    info = {"width": W, "height": H, "path": os.path.basename(OUT), "bytes": os.path.getsize(OUT)}
    json.dump(info, open(os.path.join(ROOT, "cover-info.json"), "w"), indent=1)
    print(info)

if __name__ == "__main__":
    main()
