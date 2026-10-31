"""Kindle front cover JPG for The Fibbers of Frostwood — KDP ideal 1600×2560 (W×H), navy/gold Frostwood night sky.
Run from src/: python3 cover.py
"""
from __future__ import annotations
import json, math, os, random
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FONTS = os.path.join(ROOT, "fonts")
OUT = os.path.join(ROOT, "frostwood-13-the-fibbers-of-frostwood-cover.jpg")
W, H = 1600, 2560  # KDP ideal ebook cover (width × height)

NAVY = (31, 58, 95)
DEEP = (21, 41, 63)
SLATE = (44, 77, 116)
GOLD = (255, 210, 122)
PALE = (219, 230, 241)
SNOW = (244, 247, 251)
WHITE = (255, 255, 255)
DIM = (58, 77, 102)

def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)

def snowflake(draw, x, y, r, fill):
    for i in range(6):
        a = math.pi / 3 * i + math.pi / 6
        draw.line([(x, y), (x + r * math.cos(a), y + r * math.sin(a))], fill=fill, width=max(1, int(r * 0.12)))

def cover_pine(draw, x, y, h, fill=DEEP):
    for k in range(3):
        yy = y - k * h * 0.28
        ww = h * (0.42 - k * 0.1)
        draw.polygon([(x - ww, yy), (x, yy - h * 0.5), (x + ww, yy)], fill=fill)

def center_text(draw, y, text, fnt, fill):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, y), text, font=fnt, fill=fill)

def main():
    rng = random.Random(19)
    im = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(im)

    for _ in range(70):
        x, y = rng.uniform(30, W - 30), rng.uniform(40, H * 0.48)
        r = rng.uniform(3, 11)
        a = int(rng.uniform(50, 140))
        snowflake(draw, x, y, r, (255, 255, 255, a) if False else (255, 255, 255))
        # soft: draw small white dots with varying presence
    # redraw flakes more softly as small crosses
    im = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(im)
    for _ in range(55):
        x, y = rng.uniform(40, W - 40), rng.uniform(50, H * 0.5)
        r = rng.uniform(4, 12)
        col = tuple(int(255 * rng.uniform(0.35, 0.85)) for _ in range(3))
        # blend toward navy
        col = tuple(int(NAVY[i] + (255 - NAVY[i]) * (col[0] / 255) * 0.55) for i in range(3))
        snowflake(draw, x, y, r, col)

    peaks = [(0, H * 0.62), (W * 0.2, H * 0.48), (W * 0.38, H * 0.55), (W * 0.55, H * 0.38),
             (W * 0.72, H * 0.52), (W * 0.9, H * 0.44), (W, H * 0.58), (W, H), (0, H)]
    draw.polygon(peaks, fill=SLATE)
    for (px, py, s) in [(W * 0.2, H * 0.48, 55), (W * 0.55, H * 0.38, 80), (W * 0.9, H * 0.44, 50)]:
        draw.polygon([(px, py), (px - s, py + s * 0.75), (px + s, py + s * 0.75)], fill=WHITE)

    lx, ly, lw, lh = W * 0.42, H * 0.45, W * 0.16, H * 0.055
    draw.rectangle([lx, ly, lx + lw, ly + lh], fill=DEEP)
    draw.polygon([(lx - 6, ly), (lx + lw / 2, ly - H * 0.028), (lx + lw + 6, ly)], fill=DEEP)
    for i in range(4):
        for j in range(2):
            draw.rectangle([lx + 14 + i * 26, ly + 10 + j * 22, lx + 14 + i * 26 + 12, ly + 10 + j * 22 + 12], fill=GOLD)

    fg = [(0, H * 0.72), (W * 0.35, H * 0.69), (W * 0.65, H * 0.73), (W, H * 0.7), (W, H), (0, H)]
    draw.polygon(fg, fill=SNOW)
    for x, hh in [(W * 0.1, 160), (W * 0.18, 120), (W * 0.26, 175), (W * 0.78, 140), (W * 0.86, 185), (W * 0.94, 130)]:
        cover_pine(draw, x, H * 0.72, hh)

    # the lodge's game tin with two big pinecones in the snow: snowy (truth-teller) and bare (fibber)
    cx, cy = W * 0.5, H * 0.80
    BROWN, DARK = (120, 78, 40), (70, 44, 22)
    def cone(x, y, h, snowy):
        w = h * 0.64
        body = []
        for i in range(60):
            t = i / 60 * 2 * math.pi
            yy = h * 0.45 - math.cos(t) * h * 0.43
            r = math.sin(t) * w / 2 * (0.55 + 0.45 * ((yy / h) ** 0.6))
            body.append((x + r, y - yy))
        draw.polygon(body, fill=BROWN if snowy else DARK, outline=DEEP)
        for row in range(8):
            yy = h * (0.1 + 0.1 * row)
            c = (h * 0.45 - yy) / (h * 0.43)
            half = w / 2 * (0.55 + 0.45 * ((yy / h) ** 0.6)) * math.sqrt(max(0, 1 - c * c))
            n = max(2, int(half * 2 / (w * 0.2)))
            sw = half * 2 / n
            off = sw / 2 if row % 2 else 0
            for j in range(n + (1 if row % 2 else 0)):
                sx = x - half + sw / 2 + j * sw - off
                if abs(sx - x) > half - sw * 0.25:
                    continue
                draw.arc([sx - sw / 2, y - yy - sw * 0.45, sx + sw / 2, y - yy + sw * 0.45], 0, 180, fill=DEEP if snowy else (150, 105, 60), width=5)
                if snowy and row >= 2:
                    draw.ellipse([sx - sw * 0.32, y - yy - sw * 0.2, sx + sw * 0.32, y - yy + sw * 0.08], fill=SNOW)
        draw.line([(x, y - h * 0.86), (x + h * 0.04, y - h * 1.0)], fill=DEEP, width=int(h * 0.05))
        if snowy:
            draw.ellipse([x - w * 0.3, y - h * 0.92, x + w * 0.3, y - h * 0.78], fill=SNOW, outline=DEEP, width=4)
    def bubble(x, y, txt, d=1):
        draw.rounded_rectangle([x - 70, y - 60, x + 70, y + 60], radius=36, fill=SNOW, outline=DEEP, width=5)
        draw.polygon([(x - 20 * d, y + 56), (x + 12 * d, y + 56), (x + 30 * d, y + 100)], fill=SNOW, outline=None)
        draw.line([(x - 20 * d, y + 58), (x + 30 * d, y + 100), (x + 12 * d, y + 58)], fill=DEEP, width=5)
        f = font("PlayfairDisplaySC-Bold.ttf", 90)
        bb = draw.textbbox((0, 0), txt, font=f)
        draw.text((x - (bb[2] - bb[0]) / 2 - bb[0], y - (bb[3] - bb[1]) / 2 - bb[1]), txt, font=f, fill=NAVY)
    # tin
    tw, th = 300, 270
    tx = cx
    draw.rectangle([tx - tw / 2, cy - th, tx + tw / 2, cy], fill=(196, 150, 70), outline=DEEP, width=6)
    draw.ellipse([tx - tw / 2 - 8, cy - th - 34, tx + tw / 2 + 8, cy - th + 34], fill=GOLD, outline=DEEP, width=6)
    draw.rectangle([tx - 110, cy - th + 90, tx + 110, cy - th + 180], fill=SNOW, outline=DEEP, width=4)
    lab = font("PlayfairDisplaySC-Bold.ttf", 58)
    bb = draw.textbbox((0, 0), "GAME", font=lab)
    draw.text((tx - (bb[2] - bb[0]) / 2 - bb[0], cy - th + 103), "GAME", font=lab, fill=NAVY)
    cone(cx - 330, cy + 10, 300, True)
    cone(cx + 330, cy + 10, 300, False)
    bubble(cx - 400, cy - 420, "?")
    bubble(cx + 400, cy - 420, "!", -1)
    # lantern on the left
    lx2, ly2 = W * 0.08 + 40, H * 0.86
    draw.rectangle([lx2 - 32, ly2 - 110, lx2 + 32, ly2], fill=DEEP)
    draw.rectangle([lx2 - 20, ly2 - 96, lx2 + 20, ly2 - 14], fill=GOLD)
    draw.polygon([(lx2 - 40, ly2 - 110), (lx2 + 40, ly2 - 110), (lx2, ly2 - 145)], fill=DEEP)
    draw.arc([lx2 - 18, ly2 - 175, lx2 + 18, ly2 - 135], 180, 360, fill=DEEP, width=6)

    playfair_b = font("PlayfairDisplaySC-Bold.ttf", 92)
    playfair = font("PlayfairDisplaySC-Regular.ttf", 32)
    playfair_sm = font("PlayfairDisplaySC-Regular.ttf", 26)
    crimson_i = font("CrimsonText-Italic.ttf", 36)
    crimson_i_sm = font("CrimsonText-Italic.ttf", 30)

    center_text(draw, 120, "WHO IS TELLING THE TRUTH?", playfair_sm, WHITE)
    draw.line([(W / 2 - 140, 170), (W / 2 + 140, 170)], fill=GOLD, width=3)
    center_text(draw, 220, "The Fibbers", playfair_b, WHITE)
    center_text(draw, 330, "of Frostwood", playfair_b, WHITE)
    center_text(draw, 470, "120 Truth-Teller and Fibber Logic Puzzles", crimson_i, PALE)
    center_text(draw, 520, "Cozy Winter Knights and Knaves Brain Teasers", crimson_i, PALE)
    center_text(draw, 590, "Easy to Expert · Tap for Hints and Answers", crimson_i_sm, PALE)
    center_text(draw, 650, "Phone-Friendly Kindle Edition", playfair_sm, GOLD)

    center_text(draw, H - 200, "A Frostwood Puzzle Book", playfair, NAVY)
    center_text(draw, H - 140, "Blake La Pierre", crimson_i, DIM)

    im.save(OUT, "JPEG", quality=92, optimize=True)
    info = {"width": W, "height": H, "path": os.path.basename(OUT), "bytes": os.path.getsize(OUT),
            "note": "KDP ideal ebook cover is 1600×2560 (W×H)."}
    json.dump(info, open(os.path.join(ROOT, "cover-info.json"), "w"), indent=1)
    print(info)

if __name__ == "__main__":
    main()
