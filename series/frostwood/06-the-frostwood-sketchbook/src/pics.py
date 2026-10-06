"""Rasterises a picture subject (a glyph of the monochrome Noto Emoji font, SIL OFL, in src/fonts/) to an n x n grid of 0/1."""
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import os
F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "NotoEmoji-wght.ttf")
_fc = {}
def hires(ch, wght=700, R=600):
    key = (ch, wght, R)
    if key in _fc: return _fc[key]
    f = ImageFont.truetype(F, R); f.set_variation_by_axes([wght])
    im = Image.new("L", (R*2, R*2), 0); d = ImageDraw.Draw(im)
    d.text((R//4, R//4), ch, font=f, fill=255)
    bb = im.getbbox(); im = im.crop(bb)
    a = np.asarray(im) > 127
    _fc[key] = a; return a
def glyph(ch, n, mode="outline", wght=700, thr=0.45, pad=0.04, close=0):
    a = hires(ch, wght)
    if mode == "sil":   # filled silhouettes (not used in this book; needs scipy)
        from scipy import ndimage
        b = ndimage.binary_closing(a, iterations=max(1, close)) if close else a
        a = ndimage.binary_fill_holes(b)
    h, w = a.shape; s = int(max(w, h) * (1 + 2 * pad))
    sq = np.zeros((s, s), bool); y0 = (s - h) // 2; x0 = (s - w) // 2; sq[y0:y0+h, x0:x0+w] = a
    im = Image.fromarray((sq * 255).astype(np.uint8)).resize((n, n), Image.BOX)
    return (np.asarray(im, dtype=float) / 255 > thr).astype(np.uint8)
