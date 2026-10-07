"""python3 montage.py out.png scale f1.png f2.png ...  -> side-by-side contact strip (for visual checks)."""
import sys
from PIL import Image, ImageDraw
out, sc = sys.argv[1], float(sys.argv[2]); ims = [Image.open(p).convert("RGB") for p in sys.argv[3:]]
ims = [im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS) for im in ims]
W = sum(i.width for i in ims) + 8 * (len(ims) - 1); H = max(i.height for i in ims)
s = Image.new("RGB", (W, H), (255, 0, 0)); x = 0
for i, p in zip(ims, sys.argv[3:]):
    s.paste(i, (x, 0)); ImageDraw.Draw(s).text((x + 4, H - 14), p.split("-")[-1], fill=(255, 0, 0)); x += i.width + 8
s.save(out); print(out, s.size)
