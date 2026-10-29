"""Checks every interior page for ink outside the text area (running heads and page numbers excepted)
and for anything closer than 0.5in to the trim. Prints a summary line; exits non-zero on a failure."""
import subprocess, tempfile, glob, os, sys
from PIL import Image
PDF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frostwood-10-snow-paths-of-frostwood-interior.pdf")
DPI = 72
INNER, OUTER, TOP, BOT = 0.75, 0.55, 0.7, 0.75
d = tempfile.mkdtemp()
subprocess.run(["pdftoppm", "-r", str(DPI), "-gray", "-png", PDF, os.path.join(d, "p")], check=True)
bad = []; near = []
files = sorted(glob.glob(os.path.join(d, "p-*.png")))
for f in files:
    n = int(f.rsplit("-", 1)[1].split(".")[0]); im = Image.open(f).convert("L"); w, h = im.size; px = im.load()
    left = (INNER if n % 2 else OUTER) * DPI; right = w - (OUTER if n % 2 else INNER) * DPI
    top = TOP * DPI; bot = h - BOT * DPI
    for y in range(h):
        in_head = abs(y - 0.42 * DPI) < 0.12 * DPI; in_foot = abs(y - (h - 0.42 * DPI)) < 0.12 * DPI
        for x in range(w):
            if px[x, y] < 200:
                if x < 0.5 * DPI or x > w - 0.5 * DPI or y < 0.3 * DPI or y > h - 0.3 * DPI: near.append((n, x, y)); continue
                outside = x < left - 2 or x > right + 2 or y < top - 2 or y > bot + 2
                if outside and not (in_head or in_foot): bad.append((n, x, y))
pages_bad = sorted({b[0] for b in bad}); pages_near = sorted({b[0] for b in near})
print(f"{len(files)} pages; ink outside text area on pages: {pages_bad or 'none'}; ink within 0.5in/0.3in of trim: {pages_near or 'none'}")
sys.exit(1 if bad or near else 0)
