"""colorink: soft watercolour-style colour fills under the house inkart ink lines (reusable for any case).

How it works
  * ColorInk is a mixin for inkart.Ink. Drawing code stays exactly the same ink code, but inside
        with k.tint(PAL.apron):            ...   # white fills become the apron colour
        with k.tint(PAL.navy, dark=PAL.navy): ...   # solid black fills become navy too
    every white (Wt) fill turns into the tint colour, solid black (K) fills optionally turn into `dark`,
    and hatching is drawn in a deeper shade of the tint instead of black, so it reads as soft shading.
    Outlines always stay ink.
  * k.wash(points, colour) lays a flat colour area with no outline (skies, sea, walls, floors).
  * render_color() rasterises the page in RGB at 300 dpi and adds a gentle paper grain / pigment
    mottle, so flat fills look like a light watercolour wash rather than vector flats.
Everything is code-drawn; no image generation service is involved."""
import math, os, subprocess, tempfile, random
from contextlib import contextmanager
from reportlab.pdfgen import canvas as rlcanvas
from reportlab.lib import colors

K = colors.black; Wt = colors.white

def C(r, g, b): return colors.Color(r / 255, g / 255, b / 255)
def shade(c, f=0.72):
    """Darker version of a colour (for hatching / shadows)."""
    return colors.Color(c.red * f, c.green * f, c.blue * f)
def mix(a, b, t): return colors.Color(a.red + (b.red - a.red) * t, a.green + (b.green - a.green) * t, a.blue + (b.blue - a.blue) * t)

class PAL:
    """Cozy seaside palette: soft, slightly warm, never fully saturated."""
    # setting
    sky = C(214, 233, 240); sky2 = C(236, 242, 236); cloud = C(252, 250, 244); sun = C(250, 222, 140)
    sea = C(146, 192, 210); sea2 = C(118, 170, 196); foam = C(236, 244, 244)
    sand = C(240, 223, 184); grass = C(190, 212, 156); headland = C(168, 194, 138); rock = C(190, 182, 166)
    glass = C(214, 232, 238); glass_lit = C(252, 236, 180)
    hall_wall = C(247, 234, 206); dado = C(222, 196, 154); floor = C(224, 192, 146); floor2 = C(210, 176, 130)
    curtain = C(228, 178, 166); stage = C(176, 92, 88); wood = C(196, 150, 104); wood_dk = C(150, 108, 72)
    cloth = Wt; cloth_tbl = C(250, 244, 226); dome = C(226, 238, 242); card = C(253, 250, 240)
    roof = C(206, 136, 108); slate = C(150, 162, 178); chimney = C(196, 128, 104)
    walls = [C(244, 208, 202), C(247, 228, 168), C(200, 220, 234), C(206, 230, 208), C(250, 246, 236), C(236, 214, 230)]
    doors = [C(84, 128, 160), C(182, 86, 76), C(92, 140, 112), C(214, 168, 72), C(96, 112, 150), C(160, 100, 140)]
    teal = C(92, 146, 148); teal_lt = C(160, 200, 196); slateboard = C(64, 74, 76); copper = C(196, 120, 80)
    stripe = C(232, 128, 118); awning_lt = C(252, 244, 232)
    bunting = [C(228, 122, 112), C(246, 206, 112), C(130, 178, 212), C(152, 198, 142), C(238, 168, 190)]
    # people
    skin = C(245, 210, 186); skin2 = C(236, 196, 168); cheek = C(240, 164, 156); blush = C(234, 120, 118)
    hair_grey = C(196, 196, 204); hair_dark = C(112, 82, 64); hair_ginger = C(196, 128, 82)
    agnes_dress = C(178, 186, 226); apron = C(253, 250, 242); teapot = C(226, 150, 150)
    navy = C(54, 70, 112); navy_lt = C(92, 110, 158); silver = C(232, 232, 236); brass = C(236, 206, 120)
    sage = C(178, 206, 162); straw = C(234, 206, 132); pea_pink = C(238, 150, 188); pea_purple = C(176, 140, 214); pea_white = C(250, 236, 244)
    leaf = C(132, 176, 112)
    tweed = C(200, 174, 118); cap = C(150, 116, 84); shirt = C(232, 236, 240)
    baker = C(253, 252, 248); apron_blue = C(170, 196, 222); bread = C(214, 158, 94); crust = C(184, 124, 70); wicker = C(222, 184, 120)
    # things
    bag = C(176, 92, 84); bag_dk = C(130, 64, 60); paper = C(252, 250, 242)
    sponge = C(242, 206, 132); lemon = C(250, 232, 140); jam = C(210, 90, 90); cream = C(253, 248, 236)
    rosette = C(120, 160, 214); rosette2 = C(232, 196, 96); van = C(172, 206, 214); lighthouse_red = C(212, 104, 92)
    note_yellow = C(255, 228, 120)

def _is(c, ref):
    return c is ref or (c is not None and hasattr(c, "rgb") and c.rgb() == ref.rgb())

class ColorInk:
    """Mixin: put before inkart.Ink in the bases, e.g. class Sea(ColorInk, Ink)."""
    def _tints(s):
        if not hasattr(s, "_tstack"): s._tstack = []
        return s._tstack

    @contextmanager
    def tint(s, light, dark=None, hatch=None, hatch_lw=None):
        s._tints().append(dict(light=light, dark=dark, hatch=hatch, hatch_lw=hatch_lw))
        try: yield
        finally: s._tints().pop()

    def _top(s): t = s._tints(); return t[-1] if t else None

    def _map(s, fill):
        t = s._top()
        if t is None or fill is None: return fill
        if t["light"] is not None and _is(fill, Wt): return t["light"]
        if t["dark"] is not None and _is(fill, K): return t["dark"]
        return fill

    def shape(s, pts, lw=0.8, fill=Wt, stroke=True, amp=0.3):
        return super().shape(pts, lw=lw, fill=s._map(fill), stroke=stroke, amp=amp)

    def circle(s, x, y, r, lw=0.8, fill=Wt, stroke=True):
        return super().circle(x, y, r, lw=lw, fill=s._map(fill), stroke=stroke)

    def blob(s, pts, fill=K):
        return super().blob(pts, fill=s._map(fill))

    def hatch(s, region, angle=-55, gap=2.4, lw=0.45, jitter=0.25, cross=False, color=None):
        t = s._top()
        if color is None and t is not None:
            color = t["hatch"] or (shade(t["light"], 0.74) if t["light"] is not None else None)
            if t["hatch_lw"]: lw = t["hatch_lw"]
        c = s.c; c.saveState()
        c.clipPath(s.path(region, closed=True), stroke=0, fill=0)
        xs = [p[0] for p in region]; ys = [p[1] for p in region]
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        R = math.hypot(max(xs) - min(xs), max(ys) - min(ys)) / 2 + 2
        c.setStrokeColor(color or K); c.setLineWidth(lw)
        for ang in ([angle, angle + 90] if cross else [angle]):
            a = math.radians(ang); dx, dy = math.cos(a), math.sin(a); nx, ny = -dy, dx
            k = -R
            while k <= R:
                o = k + s.r.uniform(-jitter, jitter)
                c.line(cx + nx * o - dx * R, cy + ny * o - dy * R, cx + nx * o + dx * R, cy + ny * o + dy * R); k += gap
        c.restoreState()

    def wash(s, pts, color):
        """Flat colour area, no outline."""
        s.c.setFillColor(color); s.c.drawPath(s.path(pts, closed=True), stroke=0, fill=1)

    def wash_rect(s, x0, y0, x1, y1, color): s.wash([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], color)

    def vgrad(s, x0, y0, x1, y1, top, bottom, steps=24):
        """Soft vertical gradient band (sky, sea)."""
        for i in range(steps):
            u0, u1 = i / steps, (i + 1) / steps
            s.wash_rect(x0, y0 + (y1 - y0) * u0, x1, y0 + (y1 - y0) * u1 + 0.3, mix(bottom, top, (u0 + u1) / 2))

def render_color(path, w_in, h_in, fn, seed=1, dpi=300, grain=True):
    """Draw fn(canvas, w_pt, h_pt) and save an RGB PNG with a light watercolour paper texture."""
    from PIL import Image, ImageFilter
    import numpy as np
    tmpd = tempfile.mkdtemp(); pdf = os.path.join(tmpd, "a.pdf")
    c = rlcanvas.Canvas(pdf, pagesize=(w_in * 72, h_in * 72))
    fn(c, w_in * 72, h_in * 72)
    c.showPage(); c.save()
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-singlefile", pdf, os.path.join(tmpd, "a")], check=True)
    im = Image.open(os.path.join(tmpd, "a.png")).convert("RGB")
    if grain:
        W, H = im.size; rng = np.random.default_rng(seed)
        def field(cell, amp):
            small = rng.normal(0, 1, (max(2, H // cell), max(2, W // cell))).astype(np.float32)
            f = np.asarray(Image.fromarray(small, mode="F").resize((W, H), Image.BICUBIC))
            return f * amp
        mottle = field(90, 0.013) + field(28, 0.009) + field(6, 0.006)     # pigment blooms + paper tooth
        a = np.asarray(im).astype(np.float32) / 255.0
        lum = a.mean(axis=2, keepdims=True)
        # stronger on colour washes, almost none on ink so lines stay crisp
        k = np.clip((lum - 0.25) / 0.5, 0, 1)
        white = np.clip((a.min(axis=2, keepdims=True) - 0.84) / 0.1, 0, 1)   # bare paper: only a faint tooth
        k = k * (1.0 - 0.8 * white)
        a = a * (1.0 + mottle[..., None] * k)
        im = Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8))
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    im.save(path, dpi=(dpi, dpi), optimize=True)
    return path
