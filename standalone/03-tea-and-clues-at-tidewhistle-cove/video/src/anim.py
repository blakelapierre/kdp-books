"""anim: a small, reusable 2D cut-out animation engine for the Tidewhistle videos (local PIL only, no AI services).

A picture is drawn by an art script as layers instead of one flat PNG (see art_case04.py / save_layers()):
  work/art-NN/<scene>.png            the PLATE: everything that never moves (RGB, same 4:3 picture as before)
  work/art-NN/<scene>.json           manifest: plate size, px per pt, and every PART with its variants + pixel box
  work/art-NN/<scene>__<part>__<variant>.png   RGBA sprites (variants of one part share one box, so they swap cleanly)
A case config (cases/caseNN.py) then choreographs each scene in ANIM = {key: dict(art=<scene>, layers=[...])}.
All coordinates are in the art's own points (x right, y UP, as in the drawing code) and all times are ORIGINAL
narration times (render.py shifts them for the hook and the countdown splice, exactly like the scene list).

Layer kinds (dict(kind=..., ...)):
  "sprite"  one part. Options (all optional):
      show=(t0, t1), fade=0.4          visible window with soft fades (None = always)
      keys=[(t, dict(dx=, dy=, a=, rot=, s=)), ...]   eased keyframes: offset (pt), alpha, rotation (deg), scale
      pivot="feet"|"centre"|"top"|(x, y)            pivot for rot / s / wobble (default feet = bottom centre)
      idle=True or dict(sway=0.008, period=6.0, breathe=0.005)   standing idle: tiny sway about the feet + breathing
      blink=True                       eyes-closed variant ("<base>+blink") for 0.15 s every 2.6-5 s (seeded by part name)
      talk=[(t0, t1), ...] or dict(seg=N, quotes=True)   mouth ("<base>+talk") moves word by word + a small bob
      nods=[t, ...]                    a gentle 0.6 s bob (used equally for every suspect when they are introduced)
      walk=dict(t0=, t1=, dx=, steps=4, bob=1.6)       walk in from dx pt to the rest position, with steps
      swaps=[(t, variant, dur), ...]   cross-fade the base variant (e.g. a reaction after the solution, a hand-over)
      wobble=dict(amp=deg, period=s)   rocking rotation about the pivot (compass needle, flags)
      bob=dict(amp=pt, period=s)       floating up and down (boats)
      reveal=dict(t0=, t1=, soft=pt)   left-to-right write-on wipe (chalk lettering)
  "fly"     birds: part variants are wing frames; n, area=(x0, y0, x1, y1), speed=(lo, hi) pt/s, flap=Hz, size=(lo, hi)
  "glint"   sparkles / wave strokes: part variants placed at seeded random spots in area, each fading in and out
            over life seconds while drifting by drift pt/s (water, sea foam)
  "rise"    steam: part variants rise from at=(x, y) by height pt over life s, swaying and fading
  "reveal_plate"  a second plate (e.g. the same view at high tide) shown below a moving wavy line inside area:
            plate=<scene>, area=(x0, y0, x1, y1), keys=[(t, level_y), ...], wave=(amp pt, wavelength pt, speed)
  "clock"   hand sprites rotate about a pivot: part=<part>, pivot=(x, y), keys=[(t, deg), ...]
            (the same as a sprite with rot keys; kept as a name for readability)
Everything is deterministic (seeded), so any frame can be re-rendered on its own (render.py --frames)."""
import json, math, os, random
import numpy as np
from PIL import Image, ImageChops

def ease(u): u = min(1.0, max(0.0, u)); return u * u * (3 - 2 * u)

def _interp(keys, t, field, default):
    """Eased interpolation of keys [(t, {field: v})] (missing field = previous value / default)."""
    pts = [(kt, kv[field]) for kt, kv in keys if field in kv]
    if not pts: return default
    if t <= pts[0][0]: return pts[0][1]
    for (ta, va), (tb, vb) in zip(pts, pts[1:]):
        if t < tb: return va + (vb - va) * ease((t - ta) / max(1e-6, tb - ta))
    return pts[-1][1]

def _seed(name): return sum((i + 1) * ord(c) for i, c in enumerate(name)) % 100003

class Part:
    def __init__(s, variants, box):
        s.v = variants; s.box = box    # box: (x0, y0) in scaled px of the plate
    def get(s, name): return s.v.get(name)

class Scene:
    """One animated picture: plate + parts + choreographed layers. frame(t, box, size) renders a view of it."""
    def __init__(s, art_dir, spec, tmap=lambda t: t, words=(), lut=None, scale=0.7, loader=None):
        s.dir, s.spec, s.scale, s.lut = art_dir, spec, scale, lut
        name = spec["art"]; s.man = json.load(open(os.path.join(art_dir, name + ".json")))
        s.ppt = s.man["ppt"] * scale; s.Hpt = s.man["H"] / s.man["ppt"]
        s.plate = s._load(name + ".png", "RGB")
        s.parts = {}
        for pn, pm in s.man["parts"].items():
            vs = {vn: s._load(f, "RGBA") for vn, f in pm["variants"].items()}
            s.parts[pn] = Part(vs, (pm["box"][0] * scale, pm["box"][1] * scale))
        s.tmap, s.words = tmap, list(words)
        s.layers = [s._make(L) for L in spec.get("layers", [])]
        s.extra_plates = {}

    # ------------------------------------------------------------------ loading
    def _load(s, fn, mode):
        im = Image.open(os.path.join(s.dir, fn))
        if mode == "RGB": im = im.convert("RGB")
        else: im = im.convert("RGBA")
        if s.scale != 1.0: im = im.resize((max(1, round(im.width * s.scale)), max(1, round(im.height * s.scale))), Image.LANCZOS)
        if s.lut is not None:
            if mode == "RGB": im = im.point(s.lut)
            else:
                r, g, b, a = im.split(); rgb = Image.merge("RGB", (r, g, b)).point(s.lut); im = Image.merge("RGBA", (*rgb.split(), a))
        return im

    def X(s, x): return x * s.ppt
    def Y(s, y): return (s.Hpt - y) * s.ppt

    def _times(s, L):
        """Map every ORIGINAL narration time in a layer spec to video time."""
        m = s.tmap; L = dict(L)
        if L.get("show"): L["show"] = tuple(None if v is None else m(v) for v in L["show"])
        if L.get("keys"): L["keys"] = [(m(t), v) for t, v in L["keys"]]
        if L.get("nods"): L["nods"] = [m(t) for t in L["nods"]]
        if L.get("swaps"): L["swaps"] = [(m(t), v, d) for t, v, d in L["swaps"]]
        if L.get("walk"): w = dict(L["walk"]); w["t0"], w["t1"] = m(w["t0"]), m(w["t1"]); L["walk"] = w
        if L.get("reveal"): r = dict(L["reveal"]); r["t0"], r["t1"] = m(r["t0"]), m(r["t1"]); L["reveal"] = r
        # talk windows stay in ORIGINAL narration time; Sprite applies tmap when building talkw
        return L

    def _make(s, L):
        L = s._times(L)
        kind = L.get("kind", "sprite")
        return dict(sprite=Sprite, clock=Sprite, fly=Fly, glint=Glint, rise=Rise, reveal_plate=RevealPlate)[kind](s, L)

    # ------------------------------------------------------------------ render
    def frame(s, t, box, size):
        """box = (x, y, w, h) in FULL-resolution plate pixels (float); returns an RGB image of `size`."""
        sc = s.scale; bx, by, bw, bh = box[0] * sc, box[1] * sc, box[2] * sc, box[3] * sc
        x0 = max(0, int(math.floor(bx)) - 1); y0 = max(0, int(math.floor(by)) - 1)
        x1 = min(s.plate.width, int(math.ceil(bx + bw)) + 2); y1 = min(s.plate.height, int(math.ceil(by + bh)) + 2)
        im = s.plate.crop((x0, y0, x1, y1))
        for L in s.layers: L.draw(im, t, x0, y0)
        return im.resize(size, Image.BILINEAR, box=(bx - x0, by - y0, bx - x0 + bw, by - y0 + bh))

def paste(im, spr, x, y, a=1.0):
    """Paste RGBA spr onto RGB crop im at float (x, y) (rounded), with extra alpha a."""
    if spr is None or a <= 0.003: return
    if a < 0.997:
        spr = spr.copy(); spr.putalpha(spr.getchannel("A").point(lambda v, a=a: int(v * a)))
    ix, iy = int(round(x)), int(round(y))
    if ix >= im.width or iy >= im.height or ix + spr.width <= 0 or iy + spr.height <= 0: return
    im.paste(spr, (ix, iy), spr)

def affine(spr, x, y, M, P, T):
    """Forward map p' = P + M (p - P) + T for an RGBA sprite whose top-left is at (x, y) (all scaled px).
    Returns (image, x', y') for pasting. M is ((a, b), (c, d))."""
    (a, b), (c, d) = M
    corners = [(x, y), (x + spr.width, y), (x, y + spr.height), (x + spr.width, y + spr.height)]
    out = [(P[0] + a * (px - P[0]) + b * (py - P[1]) + T[0], P[1] + c * (px - P[0]) + d * (py - P[1]) + T[1]) for px, py in corners]
    X0 = math.floor(min(p[0] for p in out)); Y0 = math.floor(min(p[1] for p in out))
    X1 = math.ceil(max(p[0] for p in out)); Y1 = math.ceil(max(p[1] for p in out))
    det = a * d - b * c; ia, ib, ic, id_ = d / det, -b / det, -c / det, a / det
    # output pixel (u, v) -> absolute q = (X0 + u, Y0 + v); p = P + Minv (q - P - T); local = p - (x, y)
    ox, oy = X0 - P[0] - T[0], Y0 - P[1] - T[1]
    data = (ia, ib, ia * ox + ib * oy + P[0] - x, ic, id_, ic * ox + id_ * oy + P[1] - y)
    img = spr.transform((max(1, X1 - X0), max(1, Y1 - Y0)), Image.AFFINE, data, resample=Image.BICUBIC)
    return img, X0, Y0

class Sprite:
    BLINK_GAP = (2.6, 5.0); BLINK_DUR = 0.15
    def __init__(s, sc, L):
        s.sc, s.L = sc, L; s.part = sc.parts[L["part"]]; s.name = L.get("name", L["part"])
        first = next(iter(s.part.v.values())); s.w, s.h = first.width, first.height
        x, y = s.part.box; s.x, s.y = x, y
        pv = L.get("pivot", "feet")
        if pv == "feet": s.P = (x + s.w / 2, y + s.h)
        elif pv == "centre": s.P = (x + s.w / 2, y + s.h / 2)
        elif pv == "top": s.P = (x + s.w / 2, y)
        else: s.P = (sc.X(pv[0]), sc.Y(pv[1]))
        idle = L.get("idle"); s.idle = None
        if idle: s.idle = dict(sway=0.008, period=6.0, breathe=0.005, bperiod=3.8, **(idle if isinstance(idle, dict) else {}))
        r = random.Random(_seed(s.name) + L.get("seed", 0)); s.phase = r.uniform(0, 2 * math.pi); s.phase2 = r.uniform(0, 2 * math.pi)
        s.blinks = []
        if L.get("blink"):
            t = r.uniform(0.4, 2.5)
            while t < 900: s.blinks.append(t); t += r.uniform(*s.BLINK_GAP)
        s.talkw = []
        tk = L.get("talk"); m = sc.tmap
        if isinstance(tk, dict):
            s.talkw = [(m(a), m(b)) for a, b in _quoted_words(sc.words, tk["seg"], tk.get("quotes", True))]
        elif tk:
            # talk windows are ORIGINAL narration times (not remapped in _times); pick matching words, then map
            s.talkw = [(m(w["s"]), m(w["e"])) for w in sc.words if any(a <= w["s"] < b for a, b in tk)]
        s.talk_spans = _spans(s.talkw)
        s.swaps = sorted(L.get("swaps", []))

    # ---------------------------------------------------------------- state helpers
    def _blinking(s, t):
        for b in s.blinks:
            if b > t: return False
            if t < b + s.BLINK_DUR: return True
        return False

    def _mouth(s, t):
        for ws, we in s.talkw:
            if ws > t + 1: break
            d = we - ws
            if ws + 0.02 <= t < ws + max(0.09, 0.5 * d): return True
            if d > 0.42 and ws + 0.62 * d <= t < ws + 0.88 * d: return True
        return False

    def _talk_env(s, t):
        e = 0.0
        for a, b in s.talk_spans: e = max(e, ease((t - a + 0.15) / 0.3) * (1 - ease((t - b) / 0.35)))
        return e

    def _base(s, t):
        """(variant, previous variant, blend) after the swaps."""
        cur, prev, u = "base", None, 1.0
        for ts, v, d in s.swaps:
            if t >= ts: prev, cur, u = cur, v, ease((t - ts) / max(1e-3, d))
        return cur, prev, u

    def _variant(s, base, t):
        if s._blinking(t) and s.part.get(base + "+blink") is not None: return s.part.get(base + "+blink")
        if s.talkw and s._mouth(t) and s.part.get(base + "+talk") is not None: return s.part.get(base + "+talk")
        return s.part.get(base)

    def draw(s, im, t, ox, oy):
        L, sc = s.L, s.sc
        a = 1.0
        if L.get("show"):
            t0, t1 = L["show"]; f = L.get("fade", 0.4)
            if (t0 is not None and t < t0 - 0.001) or (t1 is not None and t > t1 + f): return
            if t0 is not None: a *= ease((t - t0) / f) if f > 0 else 1.0
            if t1 is not None: a *= 1 - ease((t - t1) / f) if f > 0 else (1.0 if t <= t1 else 0)
        keys = L.get("keys", [])
        dx = _interp(keys, t, "dx", 0.0) * sc.ppt; dy = -_interp(keys, t, "dy", 0.0) * sc.ppt
        a *= _interp(keys, t, "a", 1.0); rot = _interp(keys, t, "rot", 0.0); scl = _interp(keys, t, "s", 1.0)
        if a <= 0.003: return
        shear = 0.0; sy = 1.0
        if s.idle:
            shear += s.idle["sway"] * math.sin(2 * math.pi * t / s.idle["period"] + s.phase)
            sy += s.idle["breathe"] * math.sin(2 * math.pi * t / s.idle["bperiod"] + s.phase2)
        w = L.get("walk")
        if w:
            u = (t - w["t0"]) / max(1e-3, w["t1"] - w["t0"])
            if u < 1:
                uu = max(0.0, u); dx += w["dx"] * sc.ppt * (1 - ease(uu)) if w.get("ease", True) else w["dx"] * sc.ppt * (1 - uu)
                if 0 <= u < 1:
                    st = w.get("steps", 4) * uu; dy -= w.get("bob", 1.6) * sc.ppt * abs(math.sin(math.pi * st)) * (1 - ease((uu - 0.85) / 0.15))
                    shear += 0.012 * math.sin(math.pi * st)
        if s.talk_spans:
            e = s._talk_env(t)
            if e > 0: dy -= 0.9 * sc.ppt * e * (0.5 + 0.5 * math.sin(2 * math.pi * 1.7 * t))
        for tn in L.get("nods", []):
            if tn <= t < tn + 0.7: dy -= 2.0 * sc.ppt * math.sin(math.pi * (t - tn) / 0.7); sy += 0.006 * math.sin(math.pi * (t - tn) / 0.7)
        wb = L.get("wobble")
        if wb: rot += wb["amp"] * math.sin(2 * math.pi * t / wb["period"] + s.phase) + wb.get("amp2", 0) * math.sin(2 * math.pi * t / wb.get("period2", 1.7) + s.phase2)
        bb = L.get("bob")
        if bb: dy += bb["amp"] * sc.ppt * math.sin(2 * math.pi * t / bb["period"] + s.phase); rot += bb.get("rock", 0) * math.sin(2 * math.pi * t / bb["period"] + s.phase + 1.1)
        base, prev, u = s._base(t)
        img = s._variant(base, t)
        if prev is not None and u < 1:
            pimg = s._variant(prev, t); img = Image.blend(pimg, img, u)
        rv = L.get("reveal")
        if rv:
            p = (t - rv["t0"]) / max(1e-3, rv["t1"] - rv["t0"])
            if p <= 0: return
            if p < 1: img = _wipe(img, p, rv.get("soft", 6) * sc.ppt)
        x, y = s.x - ox, s.y - oy; P = (s.P[0] - ox, s.P[1] - oy)
        if abs(rot) < 1e-4 and abs(scl - 1) < 1e-5 and abs(shear) < 1e-6 and abs(sy - 1) < 1e-6:
            if abs(dx - round(dx)) < 0.05 and abs(dy - round(dy)) < 0.05: paste(im, img, x + dx, y + dy, a); return
        c, sn = math.cos(math.radians(-rot)), math.sin(math.radians(-rot))
        # scale/breathe about the pivot, shear (sway: x moves with height above the pivot), then rotate
        A = ((scl, -shear * scl * sy), (0.0, scl * sy))
        M = ((c * A[0][0] - sn * A[1][0], c * A[0][1] - sn * A[1][1]), (sn * A[0][0] + c * A[1][0], sn * A[0][1] + c * A[1][1]))
        # cull: skip if the sprite is far outside the crop
        if x + dx > im.width + s.w or y + dy > im.height + s.h or x + dx + 2 * s.w < 0 or y + dy + 2 * s.h < 0: return
        out, X0, Y0 = affine(img, x, y, M, P, (dx, dy))
        paste(im, out, X0, Y0, a)

def _wipe(img, p, soft):
    """Left-to-right reveal of an RGBA sprite: fraction p, soft edge width soft px."""
    W = img.width; edge = p * (W + soft) - soft
    xs = np.arange(W, dtype=np.float32); ramp = np.clip((edge + soft - xs) / max(1.0, soft), 0, 1)
    m = Image.fromarray((ramp[None, :].repeat(img.height, 0) * 255).astype(np.uint8), "L")
    out = img.copy(); out.putalpha(ImageChops.multiply(img.getchannel("A"), m)); return out

def _quoted_words(words, seg, quotes=True):
    """(s, e) of the words of segment seg that are inside quotation marks (the character's own line)."""
    out, inq = [], False
    for w in words:
        if w["seg"] != seg: continue
        tx = w["w"]; opens = tx.startswith(("\"", "\u201c")); closes = tx.rstrip(".,!?;:").endswith(("\"", "\u201d")) or tx.endswith(("\"", "\u201d"))
        if not quotes or opens or inq: out.append((w["s"], w["e"]))
        if opens: inq = True
        if closes and inq: inq = False
    return out

def _spans(ws, gap=0.5):
    sp = []
    for a, b in ws:
        if sp and a - sp[-1][1] < gap: sp[-1][1] = b
        else: sp.append([a, b])
    return sp

class Fly:
    """Birds crossing an area, flapping (variants = wing frames, ping-pong)."""
    def __init__(s, sc, L):
        s.sc, s.L = sc, L; part = sc.parts[L["part"]]; frames = [part.v[k] for k in sorted(part.v)]
        r = random.Random(L.get("seed", 3)); n = L.get("n", 3)
        x0, y0, x1, y1 = L["area"]; s.area = (sc.X(x0), sc.Y(y1), sc.X(x1), sc.Y(y0))
        s.birds = []
        for i in range(n):
            size = r.uniform(*L.get("size", (0.7, 1.0)))
            fr = [f.resize((max(1, int(f.width * size)), max(1, int(f.height * size))), Image.LANCZOS) for f in frames]
            s.birds.append(dict(fr=fr, v=r.uniform(*L.get("speed", (14, 26))) * sc.ppt * (1 if L.get("dir", 1) > 0 else -1), x=r.uniform(0, 1),
                                y=r.uniform(0.15, 0.85), amp=r.uniform(2, 6) * sc.ppt, ph=r.uniform(0, 6.3), flap=L.get("flap", 2.2) * r.uniform(0.85, 1.15)))
    def draw(s, im, t, ox, oy):
        X0, Y0, X1, Y1 = s.area; W = X1 - X0 + 120
        for b in s.birds:
            x = X0 - 60 + ((b["x"] * W + b["v"] * t) % W); y = Y0 + b["y"] * (Y1 - Y0) + b["amp"] * math.sin(0.5 * t + b["ph"])
            n = len(b["fr"]); ph = (t * b["flap"] * 2 * (n - 1) + b["ph"] * 3) % (2 * (n - 1)) if n > 1 else 0
            k = int(ph) if ph < n else int(2 * (n - 1) - ph)
            f = b["fr"][max(0, min(n - 1, k))]
            if b["v"] < 0: f = f.transpose(Image.FLIP_LEFT_RIGHT)
            paste(im, f, x - f.width / 2 - ox, y - f.height / 2 - oy)

class Glint:
    """Short-lived marks (wave strokes, sparkles) that fade in and out at seeded random spots, drifting slowly."""
    def __init__(s, sc, L):
        s.sc, s.L = sc, L; part = sc.parts[L["part"]]; s.fr = [part.v[k] for k in sorted(part.v)]
        x0, y0, x1, y1 = L["area"]; s.area = (sc.X(x0), sc.Y(y1), sc.X(x1), sc.Y(y0))
        s.n, s.life, s.drift = L.get("n", 20), L.get("life", 3.0), L.get("drift", 4.0) * sc.ppt
        s.seed = L.get("seed", 1); s.amax = L.get("alpha", 1.0)
        s.rows = L.get("rows")   # optional: list of y (pt) so strokes sit on wave rows
        s.scales = L.get("scales")
        if s.scales:
            s.frs = {sz: [f.resize((max(1, int(f.width * sz)), max(1, int(f.height * sz))), Image.LANCZOS) for f in s.fr] for sz in s.scales}
    def draw(s, im, t, ox, oy):
        X0, Y0, X1, Y1 = s.area
        for i in range(s.n):
            off = (i * 0.618 * s.life) % s.life; c = math.floor((t + off) / s.life); u = ((t + off) / s.life) - c
            r = random.Random(s.seed * 7919 + i * 131 + c * 17)
            x = r.uniform(X0, X1); y = r.uniform(Y0, Y1)
            if s.rows: y = s.sc.Y(r.choice(s.rows)) + r.uniform(-2, 2) * s.sc.ppt
            k = r.randrange(len(s.fr))
            f = s.fr[k]
            if s.scales:
                # nearer (lower) rows get the larger strokes
                q = (y - Y0) / max(1, Y1 - Y0); sz = s.scales[min(len(s.scales) - 1, int(q * len(s.scales)))]; f = s.frs[sz][k]
            a = math.sin(math.pi * u) ** 1.5 * s.amax
            paste(im, f, x + s.drift * (u - 0.5) * s.life - f.width / 2 - ox, y - f.height / 2 - oy, a)

class Rise:
    """Steam / smoke wisps rising from a point, swaying, growing and fading."""
    def __init__(s, sc, L):
        s.sc, s.L = sc, L; part = sc.parts[L["part"]]; base = [part.v[k] for k in sorted(part.v)]
        s.sizes = [0.6, 0.75, 0.9, 1.05, 1.2]
        s.fr = {z: [b.resize((max(1, int(b.width * z)), max(1, int(b.height * z))), Image.LANCZOS) for b in base] for z in s.sizes}
        s.at = (sc.X(L["at"][0]), sc.Y(L["at"][1])); s.n = L.get("n", 4); s.life = L.get("life", 3.2); s.hgt = L.get("height", 30) * sc.ppt
        s.show = L.get("show")
    def draw(s, im, t, ox, oy):
        g = 1.0
        if s.show:
            t0, t1 = s.show
            if t0 is not None: g *= ease((t - t0) / 0.8)
            if t1 is not None: g *= 1 - ease((t - t1) / 0.8)
            if g <= 0: return
        for i in range(s.n):
            off = i * s.life / s.n; c = math.floor((t + off) / s.life); u = (t + off) / s.life - c
            r = random.Random(i * 31 + c * 7)
            z = s.sizes[min(len(s.sizes) - 1, int(u * len(s.sizes)))]; f = s.fr[z][r.randrange(len(s.fr[z]))]
            x = s.at[0] + math.sin(u * 4.0 + r.uniform(0, 6)) * 3.0 * s.sc.ppt + r.uniform(-2, 2) * s.sc.ppt; y = s.at[1] - u * s.hgt
            a = g * min(1.0, u / 0.2) * (1 - ease((u - 0.45) / 0.55)) * s.L.get("alpha", 0.85)
            paste(im, f, x - f.width / 2 - ox, y - f.height - oy, a)

class RevealPlate:
    """Show a second plate (same picture, another state) below a moving wavy line inside an area: a rising tide."""
    def __init__(s, sc, L):
        s.sc, s.L = sc, L
        if L["plate"] not in sc.extra_plates if hasattr(sc, "extra_plates") else True:
            pass
        s.plate = sc._load(L["plate"] + ".png", "RGB")
        x0, y0, x1, y1 = L["area"]; s.box = (int(sc.X(x0)), int(sc.Y(y1)), int(math.ceil(sc.X(x1))), int(math.ceil(sc.Y(y0))))
        s.keys = list(L["keys"])   # already time-mapped by Scene._times
        s.wave = L.get("wave", (1.2, 40.0, 0.6))
    def level(s, t):
        k = s.keys
        if t <= k[0][0]: return k[0][1]
        for (ta, la), (tb, lb) in zip(k, k[1:]):
            if t < tb: return la + (lb - la) * ease((t - ta) / max(1e-3, tb - ta))
        return k[-1][1]
    def draw(s, im, t, ox, oy):
        bx0, by0, bx1, by1 = s.box
        cx0, cy0 = max(bx0, ox), max(by0, oy); cx1, cy1 = min(bx1, ox + im.width), min(by1, oy + im.height)
        if cx0 >= cx1 or cy0 >= cy1: return
        lv = s.level(t); sc = s.sc; amp, wl, sp = s.wave
        xs = (np.arange(cx0, cx1, dtype=np.float32) / sc.ppt)
        ylev = lv + amp * np.sin(2 * np.pi * (xs / wl) - sp * 2 * np.pi * t) + 0.5 * amp * np.sin(2 * np.pi * (xs / (wl * 0.53)) + 1.3 * t)
        ypx = (sc.Hpt - ylev) * sc.ppt                         # waterline in px (down)
        Y = np.arange(cy0, cy1, dtype=np.float32)[:, None]
        m = np.clip((Y - ypx[None, :]) * 0.8 + 0.5, 0, 1)      # 1 below the waterline -> second plate
        if m.max() <= 0: return
        mask = Image.fromarray((m * 255).astype(np.uint8), "L")
        src = s.plate.crop((cx0, cy0, cx1, cy1))
        im.paste(src, (cx0 - ox, cy0 - oy), mask)
