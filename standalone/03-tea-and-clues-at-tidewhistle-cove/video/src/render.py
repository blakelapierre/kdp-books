"""Storybook video for Case 1, The Prize Sponge. Local render only: PIL frames piped to ffmpeg (libx264 + AAC).

  python3 art.py                       # ink illustrations -> ../work/art/*.png
  python3 render.py vertical           # -> ../standalone-03-tidewhistle-case-01-the-prize-sponge-vertical.mp4
  python3 render.py wide               # -> ...-wide.mp4
  python3 render.py vertical --frames 10,75,150   # just dump PNG stills for checking

Timing comes from ../timing.json (narrate.py segment times + faster-whisper word times, see align.py)."""
import json, math, os, subprocess, sys, textwrap
from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__)); VID = os.path.join(HERE, "..")
ART = os.path.join(VID, "work", "art"); WORK = os.path.join(VID, "work")
AUDIO = os.path.join(VID, "..", "audio", "standalone-03-tidewhistle-03-case-01-the-prize-sponge.mp3")
G = "/usr/share/fonts/truetype/sand-box/google/"
FPS = 30
PAPER = (247, 240, 225); ARTPAPER = (251, 247, 236); INK = (38, 33, 30); SOFT = (120, 104, 88); ACCENT = (150, 70, 52)
TIM = json.load(open(os.path.join(VID, "timing.json")))
AUDIO_END = 216.45; END = 221.5
CD0, CD1 = 147.5, 157.5          # visible countdown (after "Think about it.", until "The Solution.")

def F(name, size):
    p = {"play": "Playfair Display SC/PlayfairDisplaySC-Bold.ttf", "playr": "Playfair Display SC/PlayfairDisplaySC-Regular.ttf",
         "crim": "Crimson Text/CrimsonText-SemiBold.ttf", "crimi": "Crimson Text/CrimsonText-Italic.ttf",
         "crimb": "Crimson Text/CrimsonText-Bold.ttf", "plex": "IBM Plex Sans Condensed/IBMPlexSansCondensed-SemiBold.ttf"}[name]
    return ImageFont.truetype(G + p, size)

def ease(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)

# ----------------------------------------------------------------------------- scene list
# kind "art": (image, (cx, cy, zoom) start, end) with cx, cy in 0..1 of the panel; "pan": keyframes on the 4-panel strip
SCENES = [
    dict(k="title", t0=0.0, t1=4.6),
    dict(k="art", img="village", t0=4.6, t1=13.5, a=(0.55, 0.5, 1.12), b=(0.66, 0.48, 1.3)),
    dict(k="art", img="hall", t0=13.5, t1=30.3, a=(0.5, 0.52, 1.12), b=(0.6, 0.56, 1.45)),
    dict(k="art", img="handbag", t0=30.3, t1=41.0, a=(0.47, 0.5, 1.12), b=(0.46, 0.38, 1.4)),
    dict(k="art", img="tearoom", t0=41.0, t1=46.0, a=(0.5, 0.5, 1.12), b=(0.48, 0.55, 1.22)),
    dict(k="pan", t0=46.0, t1=64.8, keys=[(46.0, 1, 1.12), (51.6, 1, 1.16), (52.5, 2, 1.12), (54.0, 2, 1.15), (54.9, 3, 1.12), (64.8, 3, 1.22)]),
    dict(k="art", img="plate", t0=64.8, t1=77.4, a=(0.5, 0.5, 1.12), b=(0.46, 0.55, 1.4)),
    dict(k="pan", t0=77.4, t1=134.0, keys=[(77.4, 0, 1.12), (96.9, 0, 1.25), (97.8, 1, 1.12), (107.5, 1, 1.18), (108.4, 2, 1.12), (120.3, 2, 1.18), (121.2, 3, 1.12), (134.0, 3, 1.2)]),
    dict(k="art", img="handbag", t0=134.0, t1=140.6, a=(0.46, 0.4, 1.35), b=(0.5, 0.5, 1.12)),
    dict(k="ask", t0=140.6, t1=157.4),
    dict(k="soltitle", t0=157.4, t1=159.5),
    dict(k="art", img="clue", t0=159.5, t1=190.8, a=(0.5, 0.52, 1.12), b=(0.5, 0.32, 1.3)),
    dict(k="art", img="van", t0=190.8, t1=208.4, a=(0.5, 0.5, 1.12), b=(0.66, 0.68, 1.45)),
    dict(k="art", img="prize", t0=208.4, t1=214.6, a=(0.5, 0.5, 1.12), b=(0.5, 0.45, 1.28)),
    dict(k="end", t0=214.6, t1=END),
]
XF = 0.7  # crossfade length

# ----------------------------------------------------------------------------- captions
NO_CAP = {0, 1, 12, 15}   # case title, question and "The Solution." are shown as cards instead
def build_captions():
    words = TIM["words"]; segs = TIM["segments"]; caps = []
    for si in range(len(segs)):
        if si in NO_CAP: continue
        ws = [w for w in words if w["seg"] == si]; cur = []
        for i, w in enumerate(ws):
            cur.append(w); txt = " ".join(x["w"] for x in cur); nxt = ws[i + 1]["w"] if i + 1 < len(ws) else None
            end_sent = w["w"].rstrip('"\u201d').endswith((".", "?", "!"))
            if nxt is None or (end_sent and len(txt) >= 18) or (w["w"].endswith((",", ";", ":")) and len(txt) >= 44) \
               or len(txt) + 1 + len(nxt or "") > 74:
                caps.append(dict(text=txt, s=cur[0]["s"] - 0.08, e=cur[-1]["e"] + 0.25, seg=si)); cur = []
    for a, b in zip(caps, caps[1:]):
        a["e"] = b["s"] if b["s"] - a["e"] < 0.6 else min(a["e"] + 0.35, b["s"])
    return caps
CAPS = build_captions()

# ----------------------------------------------------------------------------- layouts
class Layout:
    def __init__(s, fmt):
        s.fmt = fmt
        if fmt == "vertical":
            s.W, s.H = 1080, 1920
            s.view = (40, 300, 1040, 1300)                 # art viewport
            s.cap = (50, 1345, 1030, 1790); s.cap_size = 72
        else:
            s.W, s.H = 1920, 1080
            s.view = (80, 90, 980, 990)
            s.cap = (1060, 330, 1860, 930); s.cap_size = 60
        s.vw, s.vh = s.view[2] - s.view[0], s.view[3] - s.view[1]
        s.cache = {}

    def bg(s):
        if "bg" in s.cache: return s.cache["bg"]
        im = Image.new("RGB", (s.W, s.H), PAPER)
        # gentle warm vignette
        v = Image.radial_gradient("L").resize((s.W, s.H)); dark = Image.new("RGB", (s.W, s.H), (226, 212, 188))
        im = Image.composite(dark, im, v.point(lambda p: int(max(0, p - 120) * 0.55)))
        s.cache["bg"] = im; return im

    def chrome(s):
        """Background + header + viewport border (everything static around the art)."""
        if "chrome" in s.cache: return s.cache["chrome"]
        im = s.bg().copy(); d = ImageDraw.Draw(im)
        x0, y0, x1, y1 = s.view
        d.rectangle([x0 - 14, y0 - 14, x1 + 13, y1 + 13], outline=INK, width=4)
        d.rectangle([x0 - 6, y0 - 6, x1 + 5, y1 + 5], outline=INK, width=1)
        if s.fmt == "vertical":
            ctext(d, s.W / 2, 92, "Tea and Clues at Tidewhistle Cove", F("play", 50), INK)
            ctext(d, s.W / 2, 172, "Case 1 \u00b7 The Prize Sponge", F("crimi", 50), ACCENT)
        else:
            cx = (s.cap[0] + s.cap[2]) / 2
            ctext(d, cx, 120, "Tea and Clues at Tidewhistle Cove", F("play", 46), INK)
            ctext(d, cx, 190, "Case 1 \u00b7 The Prize Sponge", F("crimi", 46), ACCENT)
            d.line([cx - 120, 270, cx + 120, 270], fill=SOFT, width=2)
        s.cache["chrome"] = im; return im

def ctext(d, cx, y, t, f, fill):
    w = d.textlength(t, font=f); d.text((cx - w / 2, y), t, font=f, fill=fill)

def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for w in text.split():
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) <= maxw or not cur: cur = trial
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

_art = {}
def art(name):
    if name not in _art:
        g = Image.open(os.path.join(ART, name + ".png")).convert("L")
        lut = [int(INK[c] + (ARTPAPER[c] - INK[c]) * v / 255) for c in range(3) for v in range(256)]
        _art[name] = g.convert("RGB").point(lut)
    return _art[name]

def viewport(L, sc, t):
    if sc["k"] == "art":
        im = art(sc["img"]); u = ease((t - sc["t0"]) / (sc["t1"] - sc["t0"]))
        cx, cy, z = [a + (b - a) * u for a, b in zip(sc["a"], sc["b"])]
        S = im.width; side = S / z
        box = (cx * S - side / 2, cy * S - side / 2, cx * S + side / 2, cy * S + side / 2)
    else:  # pan along the lineup strip
        im = art("lineup"); keys = sc["keys"]; P = im.height
        k = max(i for i, kk in enumerate(keys) if kk[0] <= t or i == 0); k = min(k, len(keys) - 2)
        (ta, pa, za), (tb, pb, zb) = keys[k], keys[k + 1]; u = ease((t - ta) / (tb - ta))
        p = pa + (pb - pa) * u; z = za + (zb - za) * u; side = P / z
        cx = (p + 0.5) * P; cy = P * 0.52
        box = (cx - side / 2, cy - side / 2, cx + side / 2, cy + side / 2)
    side = box[2] - box[0]; m = 0.05 * im.height   # keep the art's own inner frame lines out of shot
    bx = min(max(0, box[0]), im.width - side) if sc["k"] == "pan" else min(max(m, box[0]), im.width - m - side)
    by = min(max(m, box[1]), im.height - m - side)
    return im.resize((L.vw, L.vh), Image.BILINEAR, box=(bx, by, bx + side, by + side))

def ask_panel(L, t):
    im = Image.new("RGB", (L.vw, L.vh), ARTPAPER); d = ImageDraw.Draw(im); W = L.vw
    ctext(d, W / 2, 70, "Can you solve it?", F("play", 92), INK)
    d.line([W / 2 - 180, 200, W / 2 + 180, 200], fill=ACCENT, width=3)
    f = F("crimi", 60); y = 240
    for ln in wrap(d, "Who took entry number seven, and how does Agnes know?", f, W - 140):
        ctext(d, W / 2, y, ln, f, INK); y += 74
    cx, cy, R = W / 2, 690, 190
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=(205, 192, 170), width=22)
    if t < CD0:
        ctext(d, cx, cy - 120, "?", F("play", 200), INK)
        ctext(d, cx, cy + R + 30, "Think about it\u2026", F("crimi", 52), SOFT)
    else:
        rem = max(0.0, CD1 - t); frac = rem / (CD1 - CD0)
        d.arc([cx - R, cy - R, cx + R, cy + R], start=-90, end=-90 + 360 * frac, fill=ACCENT, width=22)
        n = max(1, math.ceil(rem - 1e-6)) if rem > 0 else 0
        f2 = F("play", 210); txt = str(n) if n else "!"
        bb = d.textbbox((0, 0), txt, font=f2); d.text((cx - (bb[0] + bb[2]) / 2, cy - (bb[1] + bb[3]) / 2), txt, font=f2, fill=INK)
        ctext(d, cx, cy + R + 30, "Pause now if you need longer", F("crimi", 46), SOFT)
    return im

def soltitle_panel(L, t):
    im = Image.new("RGB", (L.vw, L.vh), ARTPAPER); d = ImageDraw.Draw(im); W = L.vw
    ctext(d, W / 2, L.vh / 2 - 130, "The Solution", F("play", 110), INK)
    d.line([W / 2 - 200, L.vh / 2 + 30, W / 2 + 200, L.vh / 2 + 30], fill=ACCENT, width=3)
    ctext(d, W / 2, L.vh / 2 + 70, "Case 1 \u00b7 The Prize Sponge", F("crimi", 56), SOFT)
    return im

def vignette_img(size):
    key = ("vig", size)
    if key not in _art: _art[key] = art("vignette").resize((size, size), Image.LANCZOS)
    return _art[key]

def full_card(L, kind, t):
    key = ("card", kind)
    if key in L.cache: return L.cache[key]
    im = L.bg().copy(); d = ImageDraw.Draw(im); W, H = L.W, L.H
    if L.fmt == "vertical":
        vs, vy, ty = 760, 230, 1060
    else:
        vs, vy, ty = 640, 220, None
    vx = (W - vs) // 2 if L.fmt == "vertical" else 150
    im.paste(vignette_img(vs), (vx, vy)); d = ImageDraw.Draw(im)
    # cut the vignette's white square corners back to paper
    m = Image.new("L", (vs, vs), 0); ImageDraw.Draw(m).ellipse([vs * 0.04 - 4, vs * 0.04 - 4, vs * 0.96 + 4, vs * 0.96 + 4], fill=255)
    base = L.bg().crop((vx, vy, vx + vs, vy + vs)); im.paste(Image.composite(im.crop((vx, vy, vx + vs, vy + vs)), base, m), (vx, vy))
    d = ImageDraw.Draw(im)
    if L.fmt == "vertical":
        cx = W / 2; y = ty
    else:
        cx = 1300; y = 250
    if kind == "title":
        ctext(d, cx, y, "Tea and Clues", F("play", 96 if L.fmt == "vertical" else 84), INK); y += 115
        ctext(d, cx, y, "at Tidewhistle Cove", F("play", 76 if L.fmt == "vertical" else 66), INK); y += 130
        d.line([cx - 160, y, cx + 160, y], fill=ACCENT, width=3); y += 40
        ctext(d, cx, y, "Case 1: The Prize Sponge", F("crimi", 74 if L.fmt == "vertical" else 64), ACCENT); y += 140
        ctext(d, cx, y, "by Blake La Pierre", F("crim", 60 if L.fmt == "vertical" else 52), INK)
    else:
        ctext(d, cx, y, "Tea and Clues", F("play", 96 if L.fmt == "vertical" else 84), INK); y += 115
        ctext(d, cx, y, "at Tidewhistle Cove", F("play", 76 if L.fmt == "vertical" else 66), INK); y += 120
        ctext(d, cx, y, "30 cozy mini-mysteries to solve by ear", F("crimi", 54 if L.fmt == "vertical" else 46), SOFT); y += 100
        ctext(d, cx, y, "by Blake La Pierre", F("crim", 62 if L.fmt == "vertical" else 54), INK); y += 140
        f = F("plex", 56 if L.fmt == "vertical" else 50); tw = d.textlength("COMING SOON TO KINDLE", font=f)
        d.rounded_rectangle([cx - tw / 2 - 40, y - 22, cx + tw / 2 + 40, y + 86], radius=18, outline=ACCENT, width=4)
        ctext(d, cx, y, "COMING SOON TO KINDLE", f, ACCENT)
    L.cache[key] = im; return im

class _Sq: vw = vh = 1000
SQ = _Sq()   # cards are designed on a 1000 x 1000 panel, then fitted to the viewport
def fit(L, im): return im if im.size == (L.vw, L.vh) else im.resize((L.vw, L.vh), Image.LANCZOS)

def scene_frame(L, sc, t):
    if sc["k"] in ("title", "end"): return full_card(L, sc["k"], t)
    im = L.chrome().copy()
    v = {"art": viewport, "pan": viewport, "ask": lambda L, sc, t: fit(L, ask_panel(SQ, t)), "soltitle": lambda L, sc, t: fit(L, soltitle_panel(SQ, t))}[sc["k"]](L, sc, t)
    im.paste(v, L.view[:2]); return im

_capimg = {}
def caption_img(L, i):
    key = (L.fmt, i)
    if key in _capimg: return _capimg[key]
    x0, y0, x1, y1 = L.cap; w, h = x1 - x0, y1 - y0
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    size = L.cap_size
    while True:
        f = F("crim", size); lines = wrap(d, CAPS[i]["text"], f, w - 20); lh = int(size * 1.22)
        if len(lines) * lh <= h or size < 40: break
        size -= 4
    y = (h - len(lines) * lh) / 2
    for ln in lines:
        tw = d.textlength(ln, font=f); d.text(((w - tw) / 2, y), ln, font=f, fill=INK + (255,)); y += lh
    _capimg[key] = im; return im

def frame(L, t):
    act = [sc for sc in SCENES if sc["t0"] - XF / 2 <= t < sc["t1"] + XF / 2]
    if len(act) == 1: im = scene_frame(L, act[0], t)
    else:
        a, b = act[0], act[1]; u = ease((t - (b["t0"] - XF / 2)) / XF)
        im = Image.blend(scene_frame(L, a, t), scene_frame(L, b, t), u)
    in_card = any(sc["k"] in ("title", "end") and sc["t0"] <= t < sc["t1"] for sc in SCENES)
    if not in_card:
        for i, c in enumerate(CAPS):
            if c["s"] <= t < c["e"]:
                a = min(1, (t - c["s"]) / 0.15, (c["e"] - t) / 0.15)
                x0, y0, x1, y1 = L.cap; reg = im.crop(L.cap).convert("RGBA")
                comp = Image.alpha_composite(reg, caption_img(L, i))
                if a < 1: comp = Image.blend(reg, comp, a)
                im.paste(comp.convert("RGB"), (x0, y0)); break
    return im

def render_chunk(args):
    fmt, f0, f1, out = args
    L = Layout(fmt)
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{L.W}x{L.H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "slow", "-crf", "21", "-maxrate", "2800k", "-bufsize", "5600k", "-tune", "animation",
           "-pix_fmt", "yuv420p", "-g", "60", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for n in range(f0, f1): p.stdin.write(frame(L, n / FPS).tobytes())
    p.stdin.close(); p.wait(); assert p.returncode == 0
    return out

def main():
    fmt = sys.argv[1] if len(sys.argv) > 1 else "vertical"
    if "--frames" in sys.argv:
        L = Layout(fmt); os.makedirs(os.path.join(WORK, "frames"), exist_ok=True)
        for ts in sys.argv[sys.argv.index("--frames") + 1].split(","):
            p = os.path.join(WORK, "frames", f"{fmt}-{float(ts):06.1f}.png"); frame(L, float(ts)).save(p); print(p)
        return
    N = int(END * FPS); parts = 8; step = math.ceil(N / parts)
    os.makedirs(os.path.join(WORK, "parts"), exist_ok=True)
    jobs = [(fmt, i * step, min(N, (i + 1) * step), os.path.join(WORK, "parts", f"{fmt}-{i:02d}.mp4")) for i in range(parts)]
    with ProcessPoolExecutor(parts) as ex: outs = list(ex.map(render_chunk, jobs))
    lst = os.path.join(WORK, "parts", f"{fmt}.txt"); open(lst, "w").write("".join(f"file '{o}'\n" for o in outs))
    final = os.path.join(VID, f"standalone-03-tidewhistle-case-01-the-prize-sponge-{fmt}.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", AUDIO,
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af", f"apad=whole_dur={END}", "-c:a", "aac", "-b:a", "128k", "-ar", "48000",
                    "-t", f"{END}", "-movflags", "+faststart",
                    "-metadata", "title=Tea and Clues at Tidewhistle Cove - Case 1: The Prize Sponge", "-metadata", "artist=Blake La Pierre", final], check=True)
    print(final)

if __name__ == "__main__":
    main()
