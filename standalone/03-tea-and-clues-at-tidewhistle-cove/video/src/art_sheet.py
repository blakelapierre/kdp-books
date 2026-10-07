"""Contact sheet of an art dir: every plate with all parts (first variant) composited.  python3 art_sheet.py ../work/art-10 out.png"""
import json, os, sys, glob
from PIL import Image, ImageDraw
d = sys.argv[1]; tiles = []
for jf in sorted(glob.glob(os.path.join(d, "*.json"))):
    m = json.load(open(jf)); im = Image.open(os.path.join(d, m["name"] + ".png")).convert("RGBA")
    for pn, pm in m["parts"].items():
        if pm.get("page") and pm["page"][0] < 100: continue
        v = sorted(pm["variants"].items())[0][1] if "base" not in pm["variants"] else pm["variants"]["base"]
        sp = Image.open(os.path.join(d, v)).convert("RGBA"); im.alpha_composite(sp, (pm["box"][0], pm["box"][1]))
    im = im.convert("RGB"); s = 520 / im.width if im.width < 3000 else 1560 / im.width
    im = im.resize((int(im.width * s), int(im.height * s))); ImageDraw.Draw(im).text((8, 8), m["name"], fill=(200, 0, 0))
    tiles.append(im)
W = 1580; x = y = 0; rowh = 0; pos = []
for t in tiles:
    if x + t.width > W: x = 0; y += rowh + 10; rowh = 0
    pos.append((x, y)); x += t.width + 10; rowh = max(rowh, t.height)
sheet = Image.new("RGB", (W, y + rowh), (255, 255, 255))
for t, p in zip(tiles, pos): sheet.paste(t, p)
sheet.save(sys.argv[2]); print(sys.argv[2], sheet.size)
