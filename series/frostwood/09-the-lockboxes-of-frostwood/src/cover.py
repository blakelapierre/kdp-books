"""Kindle front cover JPG for The Lockboxes of Frostwood — KDP ideal 1600×2560 (W×H), navy/gold Frostwood night sky.
Run from src/: python3 cover.py
"""
from __future__ import annotations
import json, math, os, random
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FONTS = os.path.join(ROOT, "fonts")
OUT = os.path.join(ROOT, "frostwood-09-the-lockboxes-of-frostwood-cover.jpg")
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

    # gold lockbox in the snow with a padlock
    cx, cy = W * 0.5, H * 0.80
    bw, bh = 420, 230
    draw.rounded_rectangle([cx - bw / 2, cy - bh, cx + bw / 2, cy], radius=14, fill=(196, 150, 70), outline=DEEP, width=6)
    draw.polygon([(cx - bw / 2 - 14, cy - bh), (cx + bw / 2 + 14, cy - bh), (cx + bw / 2 - 6, cy - bh - 90), (cx - bw / 2 + 6, cy - bh - 90)], fill=GOLD, outline=DEEP)
    draw.line([(cx - bw / 2 - 14, cy - bh), (cx + bw / 2 + 14, cy - bh)], fill=DEEP, width=6)
    for (ux, uy) in [(cx - bw / 2, cy - bh), (cx + bw / 2, cy - bh), (cx - bw / 2, cy), (cx + bw / 2, cy)]:
        draw.rectangle([ux - 18, uy - 18, ux + 18, uy + 18], fill=DEEP)
    # dial window with three wheels
    dw = 64
    x0 = cx - dw * 1.5
    draw.rectangle([x0 - 10, cy - bh + 50, x0 + dw * 3 + 10, cy - bh + 150], fill=DEEP)
    dial = font("IBMPlexSansCondensed-SemiBold.ttf", 70)
    for i, ch in enumerate("???"):
        draw.rectangle([x0 + i * dw + 5, cy - bh + 60, x0 + (i + 1) * dw - 5, cy - bh + 140], fill=SNOW)
        bb = draw.textbbox((0, 0), ch, font=dial)
        draw.text((x0 + i * dw + (dw - (bb[2] - bb[0])) / 2 - bb[0], cy - bh + 62), ch, font=dial, fill=NAVY)
    # brass key leaning on the box
    kx, ky = cx + bw / 2 + 60, cy - 30
    draw.ellipse([kx - 34, ky - 120, kx + 34, ky - 52], outline=(176, 128, 52), width=12)
    draw.line([(kx, ky - 52), (kx, ky + 30)], fill=(176, 128, 52), width=14)
    draw.line([(kx, ky + 10), (kx + 30, ky + 10)], fill=(176, 128, 52), width=12)
    draw.line([(kx, ky + 28), (kx + 22, ky + 28)], fill=(176, 128, 52), width=12)
    # lantern on the left
    lx2, ly2 = cx - bw / 2 - 90, cy
    draw.rectangle([lx2 - 32, ly2 - 110, lx2 + 32, ly2], fill=DEEP)
    draw.rectangle([lx2 - 20, ly2 - 96, lx2 + 20, ly2 - 14], fill=GOLD)
    draw.polygon([(lx2 - 40, ly2 - 110), (lx2 + 40, ly2 - 110), (lx2, ly2 - 145)], fill=DEEP)
    draw.arc([lx2 - 18, ly2 - 175, lx2 + 18, ly2 - 135], 180, 360, fill=DEEP, width=6)

    playfair_b = font("PlayfairDisplaySC-Bold.ttf", 92)
    playfair = font("PlayfairDisplaySC-Regular.ttf", 32)
    playfair_sm = font("PlayfairDisplaySC-Regular.ttf", 26)
    crimson_i = font("CrimsonText-Italic.ttf", 36)
    crimson_i_sm = font("CrimsonText-Italic.ttf", 30)

    center_text(draw, 120, "CRACK-THE-CODE LOGIC", playfair_sm, WHITE)
    draw.line([(W / 2 - 140, 170), (W / 2 + 140, 170)], fill=GOLD, width=3)
    center_text(draw, 220, "The Lockboxes", playfair_b, WHITE)
    center_text(draw, 330, "of Frostwood", playfair_b, WHITE)
    center_text(draw, 470, "120 Crack-the-Code Logic Puzzles", crimson_i, PALE)
    center_text(draw, 520, "Cozy Winter Brain Teasers", crimson_i, PALE)
    center_text(draw, 590, "Easy to Expert · Tap for Hints and Answers", crimson_i_sm, PALE)
    center_text(draw, 650, "Phone-Friendly Kindle Edition", playfair_sm, GOLD)

    center_text(draw, H - 200, "A Frostwood Puzzle Book", playfair, NAVY)
    center_text(draw, H - 140, "Blake La Pierre", crimson_i, DIM)

    im.save(OUT, "JPEG", quality=92, optimize=True)
    info = {"width": W, "height": H, "path": os.path.basename(OUT), "bytes": os.path.getsize(OUT),
            "note": "KDP ideal ebook cover is 1600×2560 (W×H). User brief said 2560×1600; used portrait KDP ideal."}
    json.dump(info, open(os.path.join(ROOT, "cover-info.json"), "w"), indent=1)
    print(info)

if __name__ == "__main__":
    main()
