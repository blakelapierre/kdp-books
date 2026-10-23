"""Front-only Kindle cover JPG, 1600 x 2560 (KDP ideal ratio). Camper van on a sunny winding road. Run: python3 cover.py"""
import os, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "standalone-10-the-backseat-detectives-cover.jpg")
G = "/usr/share/fonts/truetype/sand-box/google/"
W, H = 1600, 2560

def vfont(path, size, var=None):
    f = ImageFont.truetype(G + path, size)
    if var:
        try: f.set_variation_by_name(var)
        except Exception: pass
    return f

NAVY = (28, 46, 84); CREAM = (252, 244, 226); TEAL = (40, 150, 160); CORAL = (238, 108, 77)
SUN = (255, 214, 102); ROAD = (92, 88, 96); WHITE = (255, 255, 255)

def ctext(d, y, text, f, fill, shadow=None, off=5):
    w = d.textbbox((0, 0), text, font=f)[2]
    if shadow: d.text(((W - w) / 2 + off, y + off), text, font=f, fill=shadow)
    d.text(((W - w) / 2, y), text, font=f, fill=fill)

def main():
    rng = random.Random(10)
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    # sky gradient
    for y in range(H):
        t = min(1, y / (H * 0.62))
        c = (int(120 + 130 * t), int(196 + 40 * t), int(236 - 20 * t))
        d.line([(0, y), (W, y)], fill=c)
    # sun
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    gd.ellipse([1130, 820, 1450, 1140], fill=(255, 236, 160, 120))
    glow = glow.filter(ImageFilter.GaussianBlur(40))
    im = Image.alpha_composite(im.convert("RGBA"), glow).convert("RGB"); d = ImageDraw.Draw(im)
    d.ellipse([1190, 880, 1390, 1080], fill=SUN)
    # clouds
    for cx, cy, s in [(260, 1000, 1.0), (900, 1080, 0.8), (520, 1200, 0.6)]:
        for dx, dy, r in [(0, 0, 60), (60, -25, 70), (130, 0, 58), (65, 18, 60)]:
            d.ellipse([cx + dx * s - r * s, cy + dy * s - r * s, cx + dx * s + r * s, cy + dy * s + r * s], fill=WHITE)
    # far hills
    def hill(base, amp, col, seed, step=40):
        r = random.Random(seed); pts = [(0, H)]
        y = base
        for x in range(0, W + step, step):
            y = base + amp * (0.5 * __import__("math").sin(x / 260 + seed) + 0.3 * __import__("math").sin(x / 97 + seed * 2))
            pts.append((x, y))
        pts.append((W, H)); d.polygon(pts, fill=col)
    hill(1360, 60, (126, 178, 150), 1)
    hill(1470, 50, (98, 160, 112), 3)
    hill(1580, 40, (120, 184, 96), 5)
    # pine trees on hills
    for _ in range(22):
        x = rng.uniform(0, W); y = rng.uniform(1440, 1560); h = rng.uniform(70, 130)
        d.polygon([(x, y - h), (x - h * 0.32, y), (x + h * 0.32, y)], fill=(56, 112, 78))
    # meadow
    d.rectangle([0, 1640, W, H], fill=(132, 192, 92))
    # winding road (perspective)
    road = [(700, 1600), (780, 1600), (900, 1760), (1200, 2000), (1600, 2250), (1600, 2560), (300, 2560), (560, 2200), (720, 1900), (690, 1700)]
    d.polygon(road, fill=ROAD)
    # center dashes
    for (x0, y0, x1, y1) in [(745, 1640, 760, 1700), (790, 1760, 820, 1840), (870, 1930, 920, 2030), (960, 2120, 1030, 2240), (1080, 2330, 1160, 2470)]:
        d.line([(x0, y0), (x1, y1)], fill=(250, 220, 120), width=int(6 + (y0 - 1640) / 80))
    # flowers
    for _ in range(160):
        x = rng.uniform(0, W); y = rng.uniform(1680, 2540)
        if 300 < x < 1600 and y > 1600 and (x > 560 - (y - 2200) * 0.6) and x < 1600: 
            pass
        r = rng.uniform(4, 9)
        d.ellipse([x - r, y - r, x + r, y + r], fill=rng.choice([(255, 255, 255), (255, 222, 90), (240, 140, 160)]))
    d.polygon(road[:6] + road[6:], fill=ROAD)  # redraw road over flowers
    for (x0, y0, x1, y1) in [(745, 1640, 760, 1700), (790, 1760, 820, 1840), (870, 1930, 920, 2030), (960, 2120, 1030, 2240), (1080, 2330, 1160, 2470)]:
        d.line([(x0, y0), (x1, y1)], fill=(250, 220, 120), width=int(6 + (y0 - 1640) / 80))
    # camper van (side view) on road
    vx, vy = 420, 1960  # bottom-left of body
    vw, vh = 760, 360
    d.rounded_rectangle([vx + 8, vy - vh + 12, vx + vw + 8, vy + 12], 70, fill=(60, 60, 60))  # shadow
    d.rounded_rectangle([vx, vy - vh, vx + vw, vy], 70, fill=CREAM, outline=NAVY, width=8)
    d.rectangle([vx + 4, vy - 150, vx + vw - 4, vy - 90], fill=TEAL)  # stripe
    d.rounded_rectangle([vx, vy - 90, vx + vw, vy], 40, fill=TEAL, outline=NAVY, width=8)
    # windshield (right side = front)
    d.polygon([(vx + vw - 170, vy - vh + 40), (vx + vw - 40, vy - vh + 40), (vx + vw - 8, vy - 170), (vx + vw - 170, vy - 170)], fill=(170, 220, 240), outline=NAVY)
    # back windows with two kids peering, one with magnifying glass
    for i, wx in enumerate([vx + 70, vx + 300]):
        d.rounded_rectangle([wx, vy - vh + 50, wx + 190, vy - 180], 26, fill=(190, 228, 244), outline=NAVY, width=6)
        hx, hy = wx + 95, vy - 245
        skin = (236, 190, 150) if i == 0 else (205, 150, 110)
        d.ellipse([hx - 48, hy - 50, hx + 48, hy + 46], fill=skin)
        hair = (120, 70, 40) if i == 0 else (40, 30, 30)
        d.pieslice([hx - 54, hy - 60, hx + 54, hy + 30], 180, 360, fill=hair)
        d.ellipse([hx - 22, hy - 4, hx - 10, hy + 8], fill=NAVY); d.ellipse([hx + 10, hy - 4, hx + 22, hy + 8], fill=NAVY)
        d.arc([hx - 18, hy + 8, hx + 18, hy + 30], 20, 160, fill=NAVY, width=4)
    # magnifying glass held up by June (first window)
    mx, my = vx + 210, vy - 300
    d.line([(mx + 40, my + 40), (mx + 95, my + 95)], fill=(120, 72, 40), width=18)
    d.ellipse([mx - 55, my - 55, mx + 55, my + 55], outline=(214, 160, 60), width=14)
    lens = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lens)
    ld.ellipse([mx - 48, my - 48, mx + 48, my + 48], fill=(255, 255, 255, 90))
    im = Image.alpha_composite(im.convert("RGBA"), lens).convert("RGB"); d = ImageDraw.Draw(im)
    # driver (Grandpa) in front
    gx, gy = vx + vw - 100, vy - 240
    d.ellipse([gx - 40, gy - 40, gx + 40, gy + 40], fill=(236, 196, 160))
    d.pieslice([gx - 46, gy - 52, gx + 46, gy + 10], 180, 360, fill=(200, 200, 200))
    d.ellipse([gx - 30, gy + 8, gx + 30, gy + 30], fill=(210, 210, 210))
    # dog in door window? roof rack with suitcases
    d.rounded_rectangle([vx + 120, vy - vh - 70, vx + 330, vy - vh - 4], 14, fill=CORAL, outline=NAVY, width=6)
    d.rounded_rectangle([vx + 350, vy - vh - 54, vx + 520, vy - vh - 4], 14, fill=SUN, outline=NAVY, width=6)
    # wheels
    for wx in (vx + 160, vx + vw - 170):
        d.ellipse([wx - 72, vy - 60, wx + 72, vy + 84], fill=(40, 40, 46))
        d.ellipse([wx - 32, vy - 20, wx + 32, vy + 44], fill=(200, 200, 205))
    # headlight
    d.ellipse([vx + vw - 34, vy - 70, vx + vw - 6, vy - 42], fill=SUN)
    # title panel
    panel = Image.new("RGBA", (W, H), (0, 0, 0, 0)); pd = ImageDraw.Draw(panel)
    pd.rounded_rectangle([90, 110, W - 90, 800], 60, fill=(255, 250, 236, 235), outline=NAVY + (255,), width=10)
    im = Image.alpha_composite(im.convert("RGBA"), panel).convert("RGB"); d = ImageDraw.Draw(im)
    top = vfont("Fredoka/Fredoka-VariableFont_wdth,wght.ttf", 84, "SemiBold")
    big = vfont("Fredoka/Fredoka-VariableFont_wdth,wght.ttf", 196, "Bold")
    sub = vfont("Nunito/Nunito-VariableFont_wght.ttf", 62, "Bold")
    auth = vfont("Nunito/Nunito-VariableFont_wght.ttf", 92, "ExtraBold")
    ctext(d, 160, "THE", top, CORAL)
    ctext(d, 250, "Backseat", big, NAVY, shadow=(240, 200, 120), off=6)
    ctext(d, 470, "Detectives", big, NAVY, shadow=(240, 200, 120), off=6)
    ctext(d, 712, "24 Road Trip Mysteries to Solve Out Loud", sub, TEAL)
    # author band
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(band)
    bd.rounded_rectangle([260, 2340, W - 260, 2490], 50, fill=NAVY + (235,))
    im = Image.alpha_composite(im.convert("RGBA"), band).convert("RGB"); d = ImageDraw.Draw(im)
    ctext(d, 2358, "Blake La Pierre", auth, CREAM)
    im.save(OUT, "JPEG", quality=92)
    print(OUT, im.size, os.path.getsize(OUT))

if __name__ == "__main__":
    main()
