"""Shared helpers for the marketing image and PDF builders.

Run the build scripts from inside marketing/src/. All paths are relative to this folder.
Requires poppler-utils (pdftoppm) and Pillow; build_samples.py also needs pypdf + reportlab.
"""
import os, subprocess, tempfile, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MKT = os.path.join(REPO, "marketing")

BOOKS = {
    "the-thief-stayed-the-night": dict(
        dir="series/frostwood/01-the-thief-stayed-the-night", short="thief",
        title="The Thief Stayed the Night",
        subtitle="A Snowbound Hotel Mystery Puzzle Book",
        asin="B0HLMMS675", series_no=1, kind="12 cozy elimination cases"),
    "frostwood-express": dict(
        dir="series/frostwood/02-frostwood-express", short="express",
        title="Frostwood Express",
        subtitle="200 Train Tracks Logic Puzzles",
        asin="B0HLMB966Q", series_no=2, kind="200 Train Tracks puzzles"),
    "stars-over-frostwood": dict(
        dir="series/frostwood/03-stars-over-frostwood", short="stars",
        title="Stars over Frostwood",
        subtitle="180 Star Battle Logic Puzzles",
        asin=None, series_no=3, kind="180 Star Battle puzzles"),
    "the-advent-clock": dict(
        dir="standalone/01-the-advent-clock", short="advent",
        title="The Advent Clock",
        subtitle="A Christmas Puzzle Countdown",
        asin=None, series_no=None, kind="24 daily puzzles"),
}

# House palette (from the Frostwood cover.py files)
NAVY = (31, 58, 95); GOLD = (255, 210, 122); PALE = (219, 230, 241); SNOW = (244, 247, 251)
DEEP = (21, 41, 63); SLATE = (44, 77, 116); DIM = (39, 64, 94); INK = (34, 40, 49)

FD = "/usr/share/fonts/truetype/sand-box/google"
FONTS = {
    "title": f"{FD}/Playfair Display SC/PlayfairDisplaySC-Bold.ttf",
    "title-reg": f"{FD}/Playfair Display SC/PlayfairDisplaySC-Regular.ttf",
    "body": f"{FD}/Crimson Text/CrimsonText-Regular.ttf",
    "body-i": f"{FD}/Crimson Text/CrimsonText-Italic.ttf",
    "body-b": f"{FD}/Crimson Text/CrimsonText-SemiBold.ttf",
    "label": f"{FD}/IBM Plex Sans Condensed/IBMPlexSansCondensed-Medium.ttf",
    "label-b": f"{FD}/IBM Plex Sans Condensed/IBMPlexSansCondensed-SemiBold.ttf",
    "sym": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
}

def font(name, size):
    return ImageFont.truetype(FONTS[name], size)

def book_path(slug, *parts):
    return os.path.join(REPO, BOOKS[slug]["dir"], *parts)

def render_page(pdf, page, dpi=300):
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "p")
        subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-f", str(page), "-l", str(page),
                        "-singlefile", pdf, out], check=True)
        return Image.open(out + ".png").convert("RGB")

def crop_in(slug, page, box, dpi=300, trim=True, pad=0.06):
    """Crop a region (x0, y0, x1, y1 in inches from the top-left of the 6x9 page)."""
    im = render_page(book_path(slug, "interior.pdf"), page, dpi)
    x0, y0, x1, y1 = [int(v * dpi) for v in box]
    im = im.crop((x0, y0, x1, y1))
    if trim:
        bg = Image.new("RGB", im.size, (255, 255, 255))
        diff = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > 18 else 0)
        bb = diff.getbbox()
        if bb:
            p = int(pad * dpi)
            im = im.crop((max(0, bb[0] - p), max(0, bb[1] - p), min(im.width, bb[2] + p), min(im.height, bb[3] + p)))
    return im

def front_cover(slug, dpi=300):
    d = book_path(slug)
    ci = json.load(open(os.path.join(d, "cover-info.json")))
    x0 = (0.125 + 6 + ci["spine_in"]) * dpi
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "c")
        subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-singlefile", "-x", str(int(round(x0))),
                        "-y", str(int(0.125 * dpi)), "-W", str(6 * dpi), "-H", str(9 * dpi),
                        os.path.join(d, "cover.pdf"), out], check=True)
        return Image.open(out + ".png").convert("RGB")

# ---------- drawing helpers ----------
def night_bg(w, h, seed=1, flakes=True, ground=True):
    """Navy night-sky background with soft snowflakes and a snowy ground line."""
    import random
    rnd = random.Random(seed)
    im = Image.new("RGB", (w, h), NAVY)
    top, bot = DEEP, NAVY
    px = im.load()
    grad = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / max(1, h - 1)
        grad.putpixel((0, y), tuple(int(top[i] * (1 - t) + bot[i] * t) for i in range(3)))
    im = grad.resize((w, h))
    if flakes:
        layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        n = int(w * h / 9000)
        for _ in range(n):
            s = rnd.choice([10, 12, 14, 18, 22])
            f = ImageFont.truetype(FONTS["sym"], s)
            a = rnd.randint(35, 90)
            d.text((rnd.randint(0, w), rnd.randint(0, h)), "\u2744", font=f, fill=(219, 230, 241, a))
        im = Image.alpha_composite(im.convert("RGBA"), layer).convert("RGB")
    if ground:
        d = ImageDraw.Draw(im)
        gh = int(h * 0.09)
        d.ellipse((-w * 0.2, h - gh, w * 0.6, h + gh * 1.6), fill=SNOW)
        d.ellipse((w * 0.35, h - gh * 0.8, w * 1.25, h + gh * 1.8), fill=SNOW)
    return im

def shadowed(im, radius=14, offset=(8, 10), alpha=110):
    """Return an RGBA image of `im` with a soft drop shadow (canvas grows)."""
    pad = radius * 3
    W, H = im.width + pad * 2 + abs(offset[0]), im.height + pad * 2 + abs(offset[1])
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh = Image.new("RGBA", (im.width, im.height), (0, 0, 0, alpha))
    base.paste(sh, (pad + offset[0], pad + offset[1]))
    base = base.filter(ImageFilter.GaussianBlur(radius))
    base.paste(im.convert("RGBA"), (pad, pad))
    return base, pad

def paste_shadow(canvas, im, xy, **kw):
    s, pad = shadowed(im, **kw)
    canvas.paste(s, (xy[0] - pad, xy[1] - pad), s)

def fit(im, max_w, max_h):
    r = min(max_w / im.width, max_h / im.height)
    return im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))), Image.LANCZOS)

def text_c(d, cx, y, s, f, fill):
    w = d.textlength(s, font=f)
    d.text((cx - w / 2, y), s, font=f, fill=fill)

def wrap(d, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def draw_wrapped(d, x, y, s, f, fill, max_w, lh, center=False):
    for line in wrap(d, s, f, max_w):
        if center:
            text_c(d, x, y, line, f, fill)
        else:
            d.text((x, y), line, font=f, fill=fill)
        y += lh
    return y

def paper_card(im, pad=24, fill=(255, 255, 255)):
    c = Image.new("RGB", (im.width + pad * 2, im.height + pad * 2), fill)
    c.paste(im, (pad, pad))
    return c

def save_png(im, path, max_bytes=2_000_000):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path, "PNG", optimize=True)
    if os.path.getsize(path) > max_bytes:  # fall back to high-quality JPG under Amazon's 2 MB cap
        jp = os.path.splitext(path)[0] + ".jpg"
        im.convert("RGB").save(jp, "JPEG", quality=90, optimize=True)
        os.remove(path)
        path = jp
    return path
