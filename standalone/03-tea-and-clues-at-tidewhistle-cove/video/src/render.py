"""Storybook video for one Tidewhistle case (default Case 1; --case=2 for Case 2, config in cases/caseNN.py). Local render only: PIL frames piped to ffmpeg (libx264 + AAC).

  python3 art.py                       # ink illustrations -> ../work/art/*.png
  python3 render.py vertical           # -> ../standalone-03-tidewhistle-case-01-the-prize-sponge-vertical.mp4
  python3 render.py wide               # -> ...-wide.mp4
  python3 render.py vertical --frames 10,75,150   # just dump PNG stills for checking (../work/frames/)

Timing comes from ../timing.json (narrate.py segment times + faster-whisper word times, see align.py).
Clues for the notebook tracker come from ../clues/case-01.json (see tracker.py).
The narration MP3 is re-timed here: EXTRA seconds of silence are inserted at CUT (inside the pause after
"the solution follows.") so the 10-second countdown runs only after the narrator has finished."""
import json, math, os, re, subprocess, sys
from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageDraw, ImageFont
import tracker
from tracker import Notebook

import importlib
CASE = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--case=")), os.environ.get("CASE", "01"))
_num, _, _var = CASE.partition("-")      # --case=3-color -> cases/case03_color.py (a style variant of case 3)
C = importlib.import_module(f"cases.case{int(_num):02d}" + (f"_{_var}" if _var else ""))   # per-case config: cases/caseNN.py

HERE = os.path.dirname(os.path.abspath(__file__)); VID = os.path.join(HERE, "..")
ART = os.path.join(VID, C.ART); WORK = os.path.join(VID, "work")
AUDIO = os.path.join(VID, "..", "audio", C.AUDIO)
CLUES = os.path.join(VID, C.CLUES)
G = "/usr/share/fonts/truetype/sand-box/google/"
FPS = 30
PAPER = (247, 240, 225); ARTPAPER = (251, 247, 236); INK = (38, 33, 30); SOFT = (120, 104, 88); ACCENT = (150, 70, 52)
VIGNETTE = (226, 212, 188); RING = (205, 192, 170); SHADE = (150, 70, 52)
STYLE = getattr(C, "STYLE", "color")      # "bw": black-and-white ink look (cases/caseNN.py STYLE = "bw"); red marks stay red
if STYLE == "bw":
    PAPER = (244, 244, 241); ARTPAPER = (252, 252, 250); INK = (22, 22, 22); SOFT = (104, 104, 104); ACCENT = (168, 34, 34)
    VIGNETTE = (214, 214, 210); RING = (206, 206, 202); SHADE = (120, 120, 120)
    tracker.set_style("bw")
VARIANT = getattr(C, "VARIANT", "")      # e.g. "color": keeps work files apart from the base version of the case
PFX = ("" if C.NUM == 1 and not VARIANT else f"case{C.NUM:02d}-") + (f"{VARIANT}-" if VARIANT else "")
CASE_DOT = f"Case {C.NUM} \u00b7 {C.NAME}"; CASE_COLON = f"Case {C.NUM}: {C.NAME}"
FULL_TITLE = f"Tea and Clues at Tidewhistle Cove - {CASE_COLON}"

# ----------------------------------------------------------------------------- timing (+ inserted silence)
# Opening hook (hook_audio.py): a ~5 s spoken teaser, then the case narration.
# The case MP3 is trimmed by TRIM s of its leading silence and starts right after the hook.
HOOK_WAV = os.path.join(VID, C.HOOK_WAV)
HOOK = json.load(open(HOOK_WAV + ".json"))
HOOK_EMOJI = C.HOOK_EMOJI
HOOK_DUR, TRIM = HOOK["duration"], C.TRIM
P = HOOK_DUR - TRIM                        # every case-narration time moves later by P
CUT, EXTRA = C.CUT, C.EXTRA                # silence spliced in after the last pre-solution line
def sh(t): return t + P + (EXTRA if t >= CUT else 0.0)
TIM = json.load(open(os.path.join(VID, C.TIMING)))
TIM_ORIG_WORDS = [dict(w) for w in TIM["words"]]   # ORIGINAL narration times (for anim.py talk sync)
for w in TIM["words"]: w["s"], w["e"] = sh(w["s"]), sh(w["e"])
ANIM = getattr(C, "ANIM", None)   # optional per-scene animation specs (cases/case04.py)
AUDIO_END = sh(C.AUDIO_END); END = AUDIO_END + 5.0
CD0 = sh(C.NARR_END) + 0.62; CD1 = CD0 + 10.0  # visible 10-second countdown, after all pre-solution narration

def F(name, size):
    p = {"play": "Playfair Display SC/PlayfairDisplaySC-Bold.ttf", "playr": "Playfair Display SC/PlayfairDisplaySC-Regular.ttf",
         "crim": "Crimson Text/CrimsonText-SemiBold.ttf", "crimi": "Crimson Text/CrimsonText-Italic.ttf",
         "crimb": "Crimson Text/CrimsonText-Bold.ttf", "plex": "IBM Plex Sans Condensed/IBMPlexSansCondensed-SemiBold.ttf"}[name]
    return ImageFont.truetype(G + p, size)

def ease(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)

# ----------------------------------------------------------------------------- scene list (times in ORIGINAL narration time; sh() applied below)
# "art": (cx, cy, zoom) start -> end, cx/cy in 0..1 of the 4:3 picture. "pan": (t, panel, zoom) keys on the lineup strip.
SCENES = [dict(sc) for sc in C.SCENES]
for sc in SCENES:
    sc["t0"] = 0.0 if sc["t0"] is None else sh(sc["t0"]); sc["t1"] = END if sc["t1"] is None else sh(sc["t1"])
    if sc["k"] == "pan": sc["keys"] = [(sh(t), p, z) for t, p, z in sc["keys"]]
XF = 0.7  # crossfade length

SLUG = C.SLUG
VIDEO_SLUG = getattr(C, "VIDEO_SLUG", SLUG)   # full-video file name stem (variants add e.g. "-color")
SHORTS_CFG = dict(tag=C.SHORTS["tag"], p1_end=sh(C.SHORTS["p1_end"]), recap=tuple(sh(t) for t in C.SHORTS["recap"]), cd_cut=CD1 - 4.0,
                  card_t=sh(C.SHORTS["card_t"]), suspects=C.SHORTS["suspects"], title_line=CASE_DOT, yt_title=FULL_TITLE)

# ----------------------------------------------------------------------------- captions: phrase-boundary chunks
NO_CAP = C.NO_CAP
CONJ = {"and", "but", "because", "although", "with", "so", "which", "who", "when", "then", "or", "under", "by", "that", "he", "she"}
FUNC = {"a", "an", "in", "at", "to", "of", "past", "from", "for", "had", "was", "been", "on", "into", "without", "apart"}
NOEND = {"the", "a", "an", "of", "to", "in", "at", "on", "for", "with", "his", "her", "their", "my", "its", "own", "and", "but", "very", "had", "has", "have", "could", "would", "will"}
MAXC, MINC = 72, 16
def _txt(ws): return " ".join(w["w"] for w in ws)
def _split(ws):
    """Split a word run at the best phrase boundary until each piece fits MAXC characters."""
    if len(_txt(ws)) <= MAXC: return [ws]
    best, bs = None, 1e9
    for i in range(1, len(ws)):
        L, R = _txt(ws[:i]), _txt(ws[i:])
        if len(L) < MINC or len(R) < MINC: continue
        prev = ws[i - 1]["w"]; nxt = re.sub(r"[^a-z]", "", ws[i]["w"].lower()); pv = re.sub(r"[^a-z]", "", prev.lower())
        if re.search(r"[.?!][\"\u201d]?$", prev): q = 0
        elif re.search(r"[,;:\u2014][\"\u201d]?$", prev): q = 8
        elif nxt in CONJ: q = 30
        elif nxt in FUNC: q = 50
        else: q = 90
        if pv in NOEND and not re.search(r"[,;:.?!]", prev): q += 200
        score = q + abs(len(L) - len(R)) * 0.6 + (40 if max(len(L), len(R)) > MAXC else 0)
        if score < bs: best, bs = i, score
    if best is None: return [ws]
    return _split(ws[:best]) + _split(ws[best:])

def curly(t):
    t = re.sub(r'(^|\s)"', '\\1\u201c', t); t = t.replace('"', '\u201d'); return t.replace("'", "\u2019")

def build_captions():
    words = TIM["words"]; caps = []
    for si in range(len(TIM["segments"])):
        if si in NO_CAP: continue
        ws = [w for w in words if w["seg"] == si]; sents, cur = [], []
        for w in ws:
            cur.append(w)
            if re.search(r"[.?!][\"\u201d]?$", w["w"]): sents.append(cur); cur = []
        if cur: sents.append(cur)
        merged = []
        for snt in sents:   # join very short sentences ("The cloth was there.") into one card
            if merged and len(_txt(merged[-1])) + len(_txt(snt)) + 1 <= 46 and len(_txt(snt)) < 30: merged[-1] = merged[-1] + snt
            else: merged.append(snt)
        for snt in merged:
            for piece in _split(snt):
                caps.append(dict(text=curly(_txt(piece)), s=piece[0]["s"] - 0.08, e=piece[-1]["e"] + 0.25, seg=si))
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
            s.view = (80, 148, 1000, 838)                  # 920 x 690 art (4:3)
            s.cap = (40, 852, 1040, 1022); s.cap_size = 56
            s.nb = (30, 1032, 1050, 1902)                  # notebook, lower part of the screen
        else:
            s.W, s.H = 1920, 1080
            s.view = (44, 112, 948, 790)                   # 904 x 678 art (4:3)
            s.cap = (20, 806, 972, 1066); s.cap_size = 54
            s.nb = (988, 26, 1898, 1056)                   # notebook, right-hand column
        s.vw, s.vh = s.view[2] - s.view[0], s.view[3] - s.view[1]
        s.cache = {}
        s.notebook = Notebook(CLUES, TIM["words"], s.nb[2] - s.nb[0], s.nb[3] - s.nb[1], max_fs=44, min_fs=28)

    def bg(s):
        if "bg" in s.cache: return s.cache["bg"]
        im = Image.new("RGB", (s.W, s.H), PAPER)
        v = Image.radial_gradient("L").resize((s.W, s.H)); dark = Image.new("RGB", (s.W, s.H), VIGNETTE)
        im = Image.composite(dark, im, v.point(lambda p: int(max(0, p - 120) * 0.55)))
        s.cache["bg"] = im; return im

    def chrome(s):
        if "chrome" in s.cache: return s.cache["chrome"]
        im = s.bg().copy(); d = ImageDraw.Draw(im)
        x0, y0, x1, y1 = s.view
        d.rectangle([x0 - 14, y0 - 14, x1 + 13, y1 + 13], outline=INK, width=4)
        d.rectangle([x0 - 6, y0 - 6, x1 + 5, y1 + 5], outline=INK, width=1)
        if s.fmt == "vertical":
            ctext(d, s.W / 2, 22, "Tea and Clues at Tidewhistle Cove", F("play", 48), INK)
            ctext(d, s.W / 2, 82, CASE_DOT, F("crimi", 42), ACCENT)
        else:
            cx = (x0 + x1) / 2
            ctext(d, cx, 6, "Tea and Clues at Tidewhistle Cove", F("play", 38), INK)
            ctext(d, cx, 52, CASE_DOT, F("crimi", 32), ACCENT)
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

def balanced(d, text, f, maxw, nlines):
    """Wrap into exactly nlines with the most even widths, preferring breaks after punctuation."""
    ws = text.split()
    if nlines == 1: return [text] if d.textlength(text, font=f) <= maxw else None
    best, bs = None, 1e18
    def rec(i, k, acc):
        nonlocal best, bs
        if k == 1:
            ln = " ".join(ws[i:]); wd = d.textlength(ln, font=f)
            if wd > maxw: return
            lines = acc + [ln]; widths = [d.textlength(x, font=f) for x in lines]
            sc = max(widths) - min(widths) - sum(60 for x in lines[:-1] if re.search(r"[,;:.?!\u2014][\"\u201d]?$", x))
            sc += sum(40 for x in lines[1:] if x.split()[0].lower() in ("a", "the", "of", "to")) * 0
            if sc < bs: best, bs = lines, sc
            return
        for j in range(i + 1, len(ws) - k + 2):
            ln = " ".join(ws[i:j])
            if d.textlength(ln, font=f) > maxw: break
            rec(j, k - 1, acc + [ln])
    rec(0, nlines, [])
    return best

_art = {}; _anim = {}; _lut = None
def lut():
    global _lut
    if _lut is None: _lut = [int(INK[c] + (ARTPAPER[c] - INK[c]) * v / 255) for c in range(3) for v in range(256)]
    return _lut

def art(name):
    if name not in _art:
        g = Image.open(os.path.join(ART, name + ".png")).convert("RGB")   # colour art (art.py); grey also works
        _art[name] = g.point(lut())
    return _art[name]

def anim_scene(key):
    """Lazy-load an anim.Scene for ANIM[key] (scale 0.7 keeps memory down; box coords stay full-res)."""
    if key not in _anim:
        import anim
        _anim[key] = anim.Scene(ART, ANIM[key], tmap=sh, words=TIM_ORIG_WORDS, scale=0.7, lut=lut())
    return _anim[key]

def _view_box(sc, t, W, H):
    """Compute the crop box (bx, by, bw, bh) in FULL-resolution plate pixels for an art/pan scene."""
    if sc["k"] == "art":
        u = ease((t - sc["t0"]) / max(1e-6, sc["t1"] - sc["t0"]))
        cx, cy, z = [a + (b - a) * u for a, b in zip(sc["a"], sc["b"])]
        bh = H / z; bw = bh * 4 / 3
        box = (cx * W - bw / 2, cy * H - bh / 2)
        m = 0.05 * H
        bx = min(max(m, box[0]), W - m - bw); by = min(max(m, box[1]), H - m - bh)
        return bx, by, bw, bh
    keys = sc["keys"]; PWp = W / C.LINEUP_PANELS
    k = max(i for i, kk in enumerate(keys) if kk[0] <= t or i == 0); k = min(k, len(keys) - 2)
    (ta, pa, za), (tb, pb, zb) = keys[k], keys[k + 1]; u = ease((t - ta) / max(1e-6, tb - ta))
    p = pa + (pb - pa) * u; z = za + (zb - za) * u; bh = H / z; bw = bh * 4 / 3
    box = ((p + 0.45) * PWp - bw / 2, H * 0.95 - bh)
    m = 0.05 * H
    bx = min(max(0, box[0]), W - bw); by = min(max(m, box[1]), H - m - bh)
    return bx, by, bw, bh

def viewport(L, sc, t):
    key = sc["img"] if sc["k"] == "art" else "lineup"
    if ANIM and key in ANIM:
        scene = anim_scene(key); W, H = scene.man["W"], scene.man["H"]
        bx, by, bw, bh = _view_box(sc, t, W, H)
        return scene.frame(t, (bx, by, bw, bh), (L.vw, L.vh))
    im = art(key); bx, by, bw, bh = _view_box(sc, t, im.width, im.height)
    return im.resize((L.vw, L.vh), Image.BILINEAR, box=(bx, by, bx + bw, by + bh))

def ask_panel(t):
    W, H = 1000, 750
    im = Image.new("RGB", (W, H), ARTPAPER); d = ImageDraw.Draw(im)
    ctext(d, W / 2, 34, "Can you solve it?", F("play", 88), INK)
    d.line([W / 2 - 180, 160, W / 2 + 180, 160], fill=ACCENT, width=3)
    f = F("crimi", 54); y = 182
    for ln in wrap(d, C.QUESTION, f, W - 160):
        ctext(d, W / 2, y, ln, f, INK); y += 64
    cx, cy, R = W / 2, 480, 150
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=RING, width=20)
    if t < CD0:
        ctext(d, cx, cy - 104, "?", F("play", 170), INK)
        ctext(d, cx, cy + R + 26, "Check Agnes's notebook\u2026", F("crimi", 46), SOFT)
    else:
        rem = max(0.0, CD1 - t); frac = rem / (CD1 - CD0)
        d.arc([cx - R, cy - R, cx + R, cy + R], start=-90, end=-90 + 360 * frac, fill=ACCENT, width=20)
        n = max(1, math.ceil(rem - 1e-6)) if rem > 0 else 0
        f2 = F("play", 180); txt = str(n) if n else "!"
        bb = d.textbbox((0, 0), txt, font=f2); d.text((cx - (bb[0] + bb[2]) / 2, cy - (bb[1] + bb[3]) / 2), txt, font=f2, fill=INK)
        ctext(d, cx, cy + R + 26, "Pause now if you need longer", F("crimi", 46), SOFT)
    return im

def soltitle_panel(t):
    W, H = 1000, 750
    im = Image.new("RGB", (W, H), ARTPAPER); d = ImageDraw.Draw(im)
    ctext(d, W / 2, H / 2 - 120, "The Solution", F("play", 110), INK)
    d.line([W / 2 - 200, H / 2 + 40, W / 2 + 200, H / 2 + 40], fill=ACCENT, width=3)
    ctext(d, W / 2, H / 2 + 76, CASE_DOT, F("crimi", 56), SOFT)
    return im

def vignette_img(size):
    key = ("vig", size)
    if key not in _art: _art[key] = art("vignette").resize((size, size), Image.LANCZOS)
    return _art[key]

def full_card(L, kind, t):
    key = ("card", kind)
    if key in L.cache: return L.cache[key]
    im = L.bg().copy(); W, H = L.W, L.H
    if L.fmt == "vertical": vs, vy, ty = 760, 230, 1060
    else: vs, vy, ty = 640, 220, None
    vx = (W - vs) // 2 if L.fmt == "vertical" else 150
    im.paste(vignette_img(vs), (vx, vy))
    m = Image.new("L", (vs, vs), 0); ImageDraw.Draw(m).ellipse([vs * 0.04 - 4, vs * 0.04 - 4, vs * 0.96 + 4, vs * 0.96 + 4], fill=255)
    base = L.bg().crop((vx, vy, vx + vs, vy + vs)); im.paste(Image.composite(im.crop((vx, vy, vx + vs, vy + vs)), base, m), (vx, vy))
    d = ImageDraw.Draw(im); V = L.fmt == "vertical"
    cx, y = (W / 2, ty) if V else (1300, 250)
    ctext(d, cx, y, "Tea and Clues", F("play", 96 if V else 84), INK); y += 115
    ctext(d, cx, y, "at Tidewhistle Cove", F("play", 76 if V else 66), INK)
    if kind == "title":
        y += 130; d.line([cx - 160, y, cx + 160, y], fill=ACCENT, width=3); y += 40
        ctext(d, cx, y, CASE_COLON, F("crimi", 74 if V else 64), ACCENT); y += 140
        ctext(d, cx, y, "by Blake La Pierre", F("crim", 60 if V else 52), INK)
    else:
        y += 120
        ctext(d, cx, y, "30 cozy mini-mysteries to solve by ear", F("crimi", 54 if V else 46), SOFT); y += 100
        ctext(d, cx, y, "by Blake La Pierre", F("crim", 62 if V else 54), INK); y += 140
        f = F("plex", 56 if V else 50); tw = d.textlength("COMING SOON TO KINDLE", font=f)
        d.rounded_rectangle([cx - tw / 2 - 40, y - 22, cx + tw / 2 + 40, y + 86], radius=18, outline=ACCENT, width=4)
        ctext(d, cx, y, "COMING SOON TO KINDLE", f, ACCENT)
    L.cache[key] = im; return im

# ----------------------------------------------------------------------------- opening hook
def hook_caps():
    ws = [dict(w["w"]) if False else dict(w) for w in HOOK["words"]]
    ws[0]["s"] = max(ws[0]["s"], 0.0)
    groups, cur = [], []
    for w in ws:
        cur.append(w)
        if re.search(r"[,.?!]$", w["w"]): groups.append(cur); cur = []
    if cur: groups.append(cur)
    caps = [dict(text=_txt(g), s=0.0 if i == 0 else g[0]["s"] - 0.05, e=g[-1]["e"] + 0.3) for i, g in enumerate(groups)]
    for a, b in zip(caps, caps[1:]): a["e"] = b["s"]
    caps[-1]["e"] = HOOK_DUR + 1
    return caps
HOOK_CAPS = hook_caps()

_emoji = {}
def emoji_img(size):
    if size not in _emoji:
        f = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 109)
        im = Image.new("RGBA", (136, 128), (0, 0, 0, 0)); ImageDraw.Draw(im).text((0, 0), HOOK_EMOJI, font=f, embedded_color=True)
        im = im.crop(im.getbbox())
        if STYLE == "bw":   # grey emoji: keep the black-and-white look
            a = im.getchannel("A"); im = im.convert("L").convert("RGBA"); im.putalpha(a)
        _emoji[size] = im.resize((int(im.width * size / im.height), size), Image.LANCZOS)
    return _emoji[size]

def hook_title(L):
    """Big hook text as an RGBA layer (cached); lines centred, emoji after the last line."""
    key = ("hooktitle",)
    if key in L.cache: return L.cache[key]
    V = L.fmt == "vertical"; f = F("play", 116 if V else 92); lines = C.HOOK_LINES
    W = L.W if V else 940; lh = int(f.size * 1.18); H = lh * len(lines) + 20
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); es = int(f.size * 0.9)
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=f) + (es + 24 if i == len(lines) - 1 else 0); x = (W - tw) / 2; y = i * lh
        d.text((x + 4, y + 5), ln, font=f, fill=SHADE + (90,)); d.text((x, y), ln, font=f, fill=INK + (255,))
        if i == len(lines) - 1:
            e = emoji_img(es); im.alpha_composite(e, (int(x + d.textlength(ln, font=f) + 24), int(y + f.size * 0.22)))
    L.cache[key] = im; return im

def hook_frame(L, t):
    V = L.fmt == "vertical"; im = L.bg().copy(); d = ImageDraw.Draw(im)
    # art: the empty plate, slowly pushing in from frame 1
    aw, ah = (1000, 750) if V else (L.vw, L.vh); ax, ay = ((L.W - aw) // 2, 400) if V else L.view[:2]
    u = ease(t / HOOK_DUR) * 0.6 + 0.4 * (t / HOOK_DUR)
    (ca, cya, za), (cb, cyb, zb) = C.HOOK_FOCUS; cx, cy, z = ca + (cb - ca) * u, cya + (cyb - cya) * u, za + (zb - za) * u
    if ANIM and "hook" in ANIM:
        scene = anim_scene("hook"); W, H = scene.man["W"], scene.man["H"]
        bh = H / z; bw = bh * 4 / 3
        bx = min(max(0, cx * W - bw / 2), W - bw); by = min(max(0, cy * H - bh / 2), H - bh)
        im.paste(scene.frame(t, (bx, by, bw, bh), (aw, ah)), (ax, ay))
    else:
        src = art("hook"); bh = src.height / z; bw = bh * 4 / 3
        bx = min(max(0, cx * src.width - bw / 2), src.width - bw); by = min(max(0, cy * src.height - bh / 2), src.height - bh)
        im.paste(src.resize((aw, ah), Image.BILINEAR, box=(bx, by, bx + bw, by + bh)), (ax, ay))
    d.rectangle([ax - 12, ay - 12, ax + aw + 11, ay + ah + 11], outline=INK, width=4); d.rectangle([ax - 5, ay - 5, ax + aw + 4, ay + ah + 4], outline=INK, width=1)
    # big hook text (visible on frame 1, settles with a small pop)
    ht = hook_title(L); sc = 0.93 + 0.07 * ease(t / 0.35)
    hs = ht.resize((int(ht.width * sc), int(ht.height * sc)), Image.LANCZOS)
    tx, ty = ((L.W - hs.width) // 2, 70 + (ht.height - hs.height) // 2) if V else (958 + (940 - hs.width) // 2, 96 + (ht.height - hs.height) // 2)
    im.paste(hs, (tx, ty), hs)
    # three suspects, same size and treatment
    cw = 920 if V else 880
    if ANIM and "cast" in ANIM:
        scene = anim_scene("cast"); ch = int(cw * scene.man["H"] / scene.man["W"])
        cs = scene.frame(t, (0, 0, scene.man["W"], scene.man["H"]), (cw, ch))
    else:
        cs = art("cast"); ch = int(cw * cs.height / cs.width); cs = cs.resize((cw, ch), Image.LANCZOS)
    cxp, cyp = ((L.W - cw) // 2, 1390) if V else (978, 430)
    cyp += int(36 * (1 - ease(t / 0.6)))          # slides up into place from frame 1
    im.paste(cs, (cxp, cyp))
    lab = "3 suspects \u00b7 1 clue"; f2 = F("plex", 54 if V else 50)
    ctext(d, cxp + cw / 2, cyp + ch + 16, lab, f2, ACCENT)
    # spoken line as a caption
    f3 = F("crimi", 64 if V else 54); capy = 1196 if V else 822
    capw = (L.W - 80) if V else (L.vw + 20); capx = 40 if V else L.view[0] - 10
    for c in HOOK_CAPS:
        if c["s"] <= t < c["e"]:
            a = min(1, (t - c["s"]) / 0.12) if c["s"] > 0 else 1
            lay = Image.new("RGBA", (capw, 220), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
            lines = wrap(dl, curly(c["text"]), f3, capw - 40); y = (200 - len(lines) * 76) // 2
            for ln in lines: ctext(dl, capw / 2, y, ln, f3, INK + (int(255 * a),)); y += 76
            im.paste(lay, (capx, capy), lay); break
    return im

def fit(L, im): return im if im.size == (L.vw, L.vh) else im.resize((L.vw, L.vh), Image.LANCZOS)

def scene_frame(L, sc, t):
    if sc["k"] == "hook": return hook_frame(L, t)
    if sc["k"] in ("title", "end"): return full_card(L, sc["k"], t)
    im = L.chrome().copy()
    if sc["k"] in ("art", "pan"): v = viewport(L, sc, t)
    elif sc["k"] == "ask": v = fit(L, ask_panel(t))
    else: v = fit(L, soltitle_panel(t))
    im.paste(v, L.view[:2])
    nb = L.notebook.render(t, review=(sc["k"] == "ask"))
    im.paste(nb, L.nb[:2], nb)
    note = L.notebook.note_image(t, int(L.vw * 0.64), 36 if L.fmt == "vertical" else 34) if sc["k"] in ("art", "pan") else None
    if note is not None: im.paste(note, (L.view[0] + 20, L.view[3] - note.height - 18), note)
    return im

_capimg = {}
def caption_img(L, i):
    key = (L.fmt, i)
    if key in _capimg: return _capimg[key]
    x0, y0, x1, y1 = L.cap; w, h = x1 - x0, y1 - y0
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    text = CAPS[i]["text"]; lines = None
    for size in range(L.cap_size, 38, -2):
        f = F("crim", size); lh = int(size * 1.2); maxl = max(1, h // lh)
        for n in range(1, maxl + 1):
            lines = balanced(d, text, f, w - 30, n)
            if lines: break
        if lines: break
    y = (h - len(lines) * lh) / 2 - 4
    for ln in lines:
        tw = d.textlength(ln, font=f); d.text(((w - tw) / 2, y), ln, font=f, fill=INK + (255,)); y += lh
    _capimg[key] = im; return im

def frame(L, t):
    act = [sc for sc in SCENES if sc["t0"] - XF / 2 <= t < sc["t1"] + XF / 2]
    if len(act) == 1: im = scene_frame(L, act[0], t)
    else:
        a, b = act[0], act[1]; u = ease((t - (b["t0"] - XF / 2)) / XF)
        im = Image.blend(scene_frame(L, a, t), scene_frame(L, b, t), u)
    in_card = any(sc["k"] in ("hook", "title", "end") and sc["t0"] <= t < sc["t1"] for sc in SCENES)
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
           "-c:v", "libx264", "-preset", "slow", "-crf", "21", "-maxrate", "3200k", "-bufsize", "6400k", "-tune", "animation",
           "-pix_fmt", "yuv420p", "-g", "60", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for n in range(f0, f1): p.stdin.write(frame(L, n / FPS).tobytes())
    p.stdin.close(); p.wait(); assert p.returncode == 0
    return out

def retimed_audio():
    """Narration with EXTRA s of silence spliced in at CUT (lossless WAV in ../work)."""
    out = os.path.join(WORK, f"case{C.NUM:02d}-{VARIANT + '-' if VARIANT else ''}narration-retimed.wav")
    fc = (f"[0:a]atrim={TRIM}:{CUT},asetpts=PTS-STARTPTS[a];[0:a]atrim={CUT},asetpts=PTS-STARTPTS[b];"
          f"aevalsrc=0:d={EXTRA}:s=44100:c=mono[z];[a]aresample=44100,aformat=channel_layouts=mono[a2];"
          f"[b]aresample=44100,aformat=channel_layouts=mono[b2];[1:a]aresample=44100,aformat=channel_layouts=mono[h];"
          f"[h][a2][z][b2]concat=n=4:v=0:a=1[o]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", AUDIO, "-i", HOOK_WAV, "-filter_complex", fc, "-map", "[o]", out], check=True)
    return out

def main():
    fmt = sys.argv[1] if len(sys.argv) > 1 else "vertical"
    if "--frames" in sys.argv:
        L = Layout(fmt); os.makedirs(os.path.join(WORK, "frames"), exist_ok=True)
        for ts in sys.argv[sys.argv.index("--frames") + 1].split(","):
            p = os.path.join(WORK, "frames", f"{PFX}{fmt}-{float(ts):06.1f}.png"); frame(L, float(ts)).save(p); print(p)
        return
    if "--captions" in sys.argv:
        for c in CAPS: print(f"{c['s']:7.2f} {c['e']:7.2f}  {c['text']}")
        return
    N = int(END * FPS); parts = max(4, os.cpu_count() or 4); step = math.ceil(N / parts)
    os.makedirs(os.path.join(WORK, "parts"), exist_ok=True)
    jobs = [(fmt, i * step, min(N, (i + 1) * step), os.path.join(WORK, "parts", f"{PFX}{fmt}-{i:02d}.mp4")) for i in range(parts)]
    with ProcessPoolExecutor(parts) as ex: outs = list(ex.map(render_chunk, jobs))
    lst = os.path.join(WORK, "parts", f"{PFX}{fmt}.txt"); open(lst, "w").write("".join(f"file '{o}'\n" for o in outs))
    final = os.path.join(VID, f"{VIDEO_SLUG}-{fmt}.mp4")
    wav = retimed_audio()
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", wav,
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af", f"apad=whole_dur={END}", "-c:a", "aac", "-b:a", "128k", "-ar", "48000",
                    "-t", f"{END}", "-movflags", "+faststart",
                    "-metadata", f"title={FULL_TITLE}", "-metadata", "artist=Blake La Pierre", final], check=True)
    print(final)

if __name__ == "__main__":
    main()
