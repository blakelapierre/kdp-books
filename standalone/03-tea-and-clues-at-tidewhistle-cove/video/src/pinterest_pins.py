"""Build 1000x1500 Pinterest image pins (ink style) for Cases 1-10.
Scene art is a frame grabbed from each Part 1 Short (no spoilers), converted to B&W ink.
Run from video/: python3 src/pinterest_pins.py"""
import subprocess, glob, os
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
G = "/usr/share/fonts/truetype/sand-box/google/"
PF = G + "Playfair Display SC/PlayfairDisplaySC-Bold.ttf"
CB = G + "Crimson Text/CrimsonText-Bold.ttf"
CI = G + "Crimson Text/CrimsonText-Italic.ttf"
KA = G + "Kalam/Kalam-Bold.ttf"
INK, PAPER, RED = (28, 25, 22), (246, 241, 230), (150, 40, 32)
W, H = 1000, 1500
# case: (slug, title, hook object, frame time, crop w,h,x,y, clues)
CASES = {
 1: ("the-prize-sponge", "The Prize Sponge", "Who took the prize sponge?", 6, (1000, 990, 40, 300),
     ["Every cake under a glass dome, with only a number card",
      "The who-baked-what list: folded in Agnes's handbag",
      "1 pm: entry #7 gone, only crumbs left on the plate"]),
 2: ("the-lemonade-on-the-lawn", "The Lemonade on the Lawn", "Who took the silver locket?", 12, (920, 690, 80, 146),
     ["The hottest afternoon of the summer",
      "Only ice left anywhere: the freezer in Loveday's kitchen",
      "Locket on the kitchen windowsill: seen at 2, gone by 2:30"]),
 3: ("the-dry-raincoat", "The Dry Raincoat", "Who took the signed book?", 12, (920, 690, 80, 146),
     ["3:00: a sudden, very heavy downpour until 3:20",
      "3:20: the glass case open, the book gone",
      "The shop door bell rang only once"]),
 4: ("the-sandbar-at-high-tide", "The Sandbar at High Tide", "Who took the brass compass?", 12, (920, 690, 80, 146),
     ["Tide board: high water at noon",
      "At high tide the sandbar is under more than a man's height of sea",
      "Compass on the windowsill: seen 11:30, gone by 12:30"]),
 5: ("the-marrow-mix-up", "The Marrow Mix-up", "Who took the prize marrow?", 40, (920, 690, 80, 146),
     ["The prize marrow vanished overnight from Hedley's shed",
      "Four people were at the allotments that evening",
      "Rule: the thief fibs, everyone else tells the truth"]),
 6: ("the-closed-post-office", "The Closed Post Office", "Who took the puffin blanket?", 12, (920, 560, 82, 150),
     ["It is Sunday morning in Tidewhistle Cove",
      "Post office: blind down, CLOSED sign on the door",
      "Blanket left on the porch bench Saturday evening"]),
 7: ("the-dog-that-stayed-quiet", "The Dog That Stayed Quiet", "Who took the garden gnome?", 20, (920, 560, 82, 150),
     ["The only way in is the little wooden gate",
      "Pickle the dog barks at everyone who comes in",
      "All night long, Pickle did not bark once"]),
 8: ("the-four-bakers", "The Four Bakers", "Who took the cinnamon buns?", 20, (920, 560, 82, 150),
     ["Twelve buns cooling by the bakery's back door",
      "Four people passed the door in ten minutes",
      "Only ONE of the four is telling the truth"]),
 9: ("the-sunset-over-the-sea", "The Sunset over the Sea", "Who took the watercolour?", 20, (920, 560, 82, 150),
     ["Tidewhistle Cove faces east: the sun rises out of the sea",
      "In the evening the sun sets behind the hills",
      "The painting: on its easel at 7, gone by 9"]),
 10: ("the-wet-paint-bench", "The Wet Paint Bench", "Who took the lifeboat box?", 20, (930, 560, 75, 140),
     ["2:30: the harbour benches painted bright green",
      "WET PAINT: tacky until at least 8 o'clock",
      "The collection box: there at 3, gone by 4"]),
}

def font(p, s): return ImageFont.truetype(p, s)

def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines

def centered(d, y, text, f, fill=INK):
    w = d.textlength(text, font=f); d.text(((W - w) / 2, y), text, font=f, fill=fill)

def fit_lines(d, text, path, size, maxw, maxlines):
    while True:
        f = font(path, size); ls = wrap(d, text, f, maxw)
        if len(ls) <= maxlines: return f, ls
        size -= 2

def scene(n):
    slug, _, _, t, (cw, ch, cx, cy), _ = CASES[n]
    vid = [v for v in glob.glob(f"shorts/*case-{n:02d}-*short-part1.mp4") if "color" not in v][0]
    out = f"pinterest/scenes/case-{n:02d}-scene.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", vid, "-frames:v", "1",
                    "-vf", f"crop={cw}:{ch}:{cx}:{cy}", out], check=True)
    im = ImageOps.grayscale(Image.open(out))
    im = ImageOps.autocontrast(im, cutoff=1)
    im = ImageEnhance.Contrast(im).enhance(1.25)
    return Image.merge("RGB", [im.point(lambda v, a=a, b=b: int(a + (b - a) * v / 255)) for a, b in zip(INK, PAPER)])

def build(n):
    slug, name, hook, *_, clues = CASES[n]
    img = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(img)
    d.rectangle([18, 18, W - 19, H - 19], outline=INK, width=4)
    d.rectangle([30, 30, W - 31, H - 31], outline=INK, width=1)
    centered(d, 58, "Can you solve it?", font(CI, 50), RED)
    fh, ls = fit_lines(d, hook, PF, 82, W - 120, 2)
    y = 120
    for l in ls:
        centered(d, y, l, fh); y += int(fh.size * 1.12)
    y += 32
    # scene
    sc = scene(n); maxh = 1500 - y - 560 - 120
    sw = W - 140; sh = int(sc.height * sw / sc.width)
    if sh > maxh: sh = maxh; sw = int(sc.width * sh / sc.height)
    sc = sc.resize((sw, sh), Image.LANCZOS); sx = (W - sw) // 2
    img.paste(sc, (sx, y)); d.rectangle([sx - 6, y - 6, sx + sw + 5, y + sh + 5], outline=INK, width=4)
    y += sh + 34
    # notebook
    nb_top, nb_bot = y, H - 128
    d.rounded_rectangle([60, nb_top, W - 60, nb_bot], 14, fill=(252, 249, 240), outline=INK, width=3)
    for x in range(95, W - 80, 42): d.ellipse([x - 7, nb_top + 14, x + 7, nb_top + 28], fill=INK)
    d.line([120, nb_top + 40, 120, nb_bot - 8], fill=RED, width=2)
    d.text((140, nb_top + 40), f"Agnes's Notebook · Case {n}", font=font(KA, 40), fill=INK)
    cy = nb_top + 105; fk = font(KA, 37); avail = nb_bot - cy - 20
    blocks = [wrap(d, c, fk, W - 60 - 190) for c in clues]
    need = sum(len(b) for b in blocks) * 50 + (len(blocks) - 1) * 18
    if need > avail: raise SystemExit(f"case {n}: notebook overflow {need}>{avail}")
    for b in blocks:
        d.text((140, cy), "•", font=fk, fill=RED)
        for l in b: d.text((172, cy), l, font=fk, fill=INK); cy += 50
        cy += 18
    for ly in range(nb_top + 100, nb_bot - 10, 44): pass
    # footer
    centered(d, H - 112, f"Tidewhistle Cove Mysteries • Case {n} • Answer inside", font(CB, 36))
    centered(d, H - 70, "from the book  Tea and Clues at Tidewhistle Cove", font(CI, 28), RED)
    out = f"pinterest/images/pin-case-{n:02d}-{slug}.png"; img.save(out, optimize=True); print(out, "scene", sw, sh, "notebook free", avail - need)

if __name__ == "__main__":
    for n in CASES: build(n)
