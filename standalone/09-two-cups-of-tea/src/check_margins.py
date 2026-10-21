"""Render the interior at 100 dpi and check every page keeps ink inside safe zones.
- nothing within 0.5in of the top, bottom and outside edges, or within 0.6in of the gutter
- below the content area only the folio may appear (band 0.52-0.72in from the bottom)
"""
import subprocess, glob, os, sys
from PIL import Image
import numpy as np
pdf = sys.argv[1]; d = "tmp/mc"; os.makedirs(d, exist_ok=True)
for f in glob.glob(d + "/*.png"): os.remove(f)
subprocess.run(["pdftoppm", "-r", "100", "-gray", "-png", pdf, d + "/p"], check=True)
bad = 0
for f in sorted(glob.glob(d + "/*.png")):
    n = int(f.split("-")[-1].split(".")[0])
    a = np.array(Image.open(f).convert("L")) < 200; H, W = a.shape; dpi = 100
    ys, xs = np.nonzero(a)
    if len(xs) == 0: continue
    odd = n % 2 == 1
    gut_x = 0 if odd else W
    left_lim = 0.6 * dpi if odd else 0.5 * dpi
    right_lim = W - (0.5 * dpi if odd else 0.6 * dpi)
    issues = []
    if xs.min() < left_lim: issues.append(f"left ink at {xs.min()/dpi:.2f}in")
    if xs.max() > right_lim: issues.append(f"right ink at {(W-xs.max())/dpi:.2f}in from edge")
    if ys.min() < 0.5 * dpi: issues.append(f"top ink at {ys.min()/dpi:.2f}in")
    if ys.max() > H - 0.5 * dpi: issues.append(f"bottom ink at {(H-ys.max())/dpi:.2f}in")
    # content must stay above 0.80in from bottom, except folio band
    band = a[int(H - 0.80 * dpi):, :]
    by, bx = np.nonzero(band)
    by = H - 0.80 * dpi + by
    outside_folio = [(y, x) for y, x in zip(by, bx) if not (H - 0.73 * dpi <= y <= H - 0.5 * dpi and abs(x - W / 2) < 0.25 * dpi)]
    if outside_folio: issues.append(f"{len(outside_folio)} px in bottom band, lowest {(H-max(y for y,_ in outside_folio))/dpi:.2f}in")
    if issues:
        bad += 1; print(n, "; ".join(issues))
print("pages with issues:", bad)
