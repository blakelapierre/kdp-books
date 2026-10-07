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
_AUDIO_DIR = os.environ.get("TIDEWHISTLE_AUDIO_DIR") or os.path.join(VID, "..", "audio")
AUDIO = os.path.join(_AUDIO_DIR, C.AUDIO)
CLUES = os.path.join(VID, C.CLUES)
G = os.environ.get("TIDEWHISTLE_FONTS", "/usr/share/fonts/truetype/sand-box/google/").rstrip("/") + "/"
FPS = 30
# Resource caps for shared servers (unset = old behaviour: one worker per CPU, x264 auto threads)
WORKERS = int(os.environ["TIDEWHISTLE_WORKERS"]) if os.environ.get("TIDEWHISTLE_WORKERS") else None
X264_THREADS = ["-threads", os.environ["TIDEWHISTLE_X264_THREADS"]] if os.environ.get("TIDEWHISTLE_X264_THREADS") else []
PAPER = (247, 240, 225); ARTPAPER = (251, 247, 236); INK = (38, 33, 30); SOFT = (120, 104, 88); ACCENT = (150, 70, 52)
VIGNETTE = (226, 212, 188); RING = (205, 192, 170); SHADE = (150, 70, 52)
STYLE = getattr(C, "STYLE", "color")      # "bw": black-and-white ink look (cases/caseNN.py STYLE = "bw"); red marks stay red
if STYLE == "bw":
    PAPER = (244, 244, 241); ARTPAPER = (252, 252, 250); INK = (22, 22, 22); SOFT = (104, 104, 104); ACCENT = (168, 34, 34)
    VIGNETTE = (214, 214, 210); RING = (206, 206, 202); SHADE = (120, 120, 120)
    tracker.set_style("bw")
# Optional per-case accent (e.g. garden green for Case 7) — chrome / qbar / hook labels
if getattr(C, "ACCENT", None):
    ACCENT = tuple(C.ACCENT); SHADE = tuple(getattr(C, "SHADE", C.ACCENT))
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
AUDIO_END = sh(C.AUDIO_END)
# Case 10+: a "next case" teaser card after the book end card (Blake 2026-10-07). NEXT_CARD = True in the case config.
from cases import teasers as TZ
NEXT_ON = getattr(C, "NEXT_CARD", False)
END_HOLD = 4.0 if NEXT_ON else 5.0; NEXT_DUR = 5.0 if NEXT_ON else 0.0
END = AUDIO_END + END_HOLD + NEXT_DUR
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
if NEXT_ON:
    for sc in SCENES:
        if sc["k"] == "end": sc["t1"] = AUDIO_END + END_HOLD
    SCENES.append(dict(k="next", t0=AUDIO_END + END_HOLD, t1=END))
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
            # Titles live ABOVE the art frame with clear air (Blake 2026-10-06 screenshot fix).
            # Art shorter; taller question bar; gap before captions/notebook.
            s.view = (80, 140, 1000, 700)                  # 920 x 560 art — room for titles + qbar
            s.qbar = (40, 714, 1040, 910)                  # taller qbar so label border never strikes text
            s.cap = (40, 926, 1040, 1040); s.cap_size = 46 # captions under qbar with air
            s.nb = (30, 1050, 1050, 1902)                  # notebook, lower part of the screen
        else:
            s.W, s.H = 1920, 1080
            s.view = (44, 96, 948, 690)                    # art, titles clear of frame
            s.qbar = (44, 702, 948, 820)                   # taller question under art
            s.cap = (20, 836, 972, 1066); s.cap_size = 48
            s.nb = (988, 26, 1898, 1056)                   # notebook, right-hand column
        s.vw, s.vh = s.view[2] - s.view[0], s.view[3] - s.view[1]
        s.show_qbar = getattr(C, "SHOW_QBAR", False)
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
            # Series title, then case subtitle ABOVE the frame (frame top = view.y0 - 14 = 126).
            ctext(d, s.W / 2, 14, "Tea and Clues at Tidewhistle Cove", F("play", 40), INK)
            ctext(d, s.W / 2, 58, CASE_DOT, F("crimi", 34), ACCENT)  # ends ~92; frame at 126 → clear gap
        else:
            cx = (x0 + x1) / 2
            ctext(d, cx, 4, "Tea and Clues at Tidewhistle Cove", F("play", 34), INK)
            ctext(d, cx, 42, CASE_DOT, F("crimi", 28), ACCENT)
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

KEEP_ASPECT = getattr(C, "KEEP_ASPECT", False)   # Case 8+: crop at the view's own aspect (older cases: 4:3 crop, kept for re-renders)

def _view_box(sc, t, W, H, asp=None):
    """Compute the crop box (bx, by, bw, bh) in FULL-resolution plate pixels for an art/pan scene.
    asp: output aspect (KEEP_ASPECT) so nothing is stretched; default 4:3 as in cases 1-7."""
    asp = asp if (asp and KEEP_ASPECT) else 4 / 3
    if sc["k"] == "art":
        u = ease((t - sc["t0"]) / max(1e-6, sc["t1"] - sc["t0"]))
        cx, cy, z = [a + (b - a) * u for a, b in zip(sc["a"], sc["b"])]
        bh = H / z; bw = bh * asp
        if bw > W: bw = W; bh = bw / asp
        box = (cx * W - bw / 2, cy * H - bh / 2)
        m = 0.05 * H
        if KEEP_ASPECT:   # wide crops can be nearly full-width: shrink the margin instead of going negative
            mx = max(0.0, min(m, (W - bw) / 2)); my = max(0.0, min(m, (H - bh) / 2))
            return min(max(mx, box[0]), W - mx - bw), min(max(my, box[1]), H - my - bh), bw, bh
        bx = min(max(m, box[0]), W - m - bw); by = min(max(m, box[1]), H - m - bh)
        return bx, by, bw, bh
    keys = sc["keys"]; PWp = W / C.LINEUP_PANELS
    k = max(i for i, kk in enumerate(keys) if kk[0] <= t or i == 0); k = min(k, len(keys) - 2)
    (ta, pa, za), (tb, pb, zb) = keys[k], keys[k + 1]; u = ease((t - ta) / max(1e-6, tb - ta))
    p = pa + (pb - pa) * u; z = za + (zb - za) * u; bh = H / z; bw = bh * asp
    box = ((p + 0.45) * PWp - bw / 2, H * 0.95 - bh)
    m = 0.05 * H
    bx = min(max(0, box[0]), W - bw); by = min(max(m, box[1]), H - m - bh)
    return bx, by, bw, bh

def viewport(L, sc, t):
    key = sc["img"] if sc["k"] == "art" else "lineup"
    if ANIM and key in ANIM:
        scene = anim_scene(key); W, H = scene.man["W"], scene.man["H"]
        bx, by, bw, bh = _view_box(sc, t, W, H, L.vw / L.vh)
        return scene.frame(t, (bx, by, bw, bh), (L.vw, L.vh))
    im = art(key); bx, by, bw, bh = _view_box(sc, t, im.width, im.height, L.vw / L.vh)
    return im.resize((L.vw, L.vh), Image.BILINEAR, box=(bx, by, bx + bw, by + bh))


def question_bar(L, t):
    """Persistent mid-screen case question (between illustration and notebook). High-contrast banner.
    Layout (Blake 2026-10-06): label in its own top band; question BELOW that band; no border line
    ever crosses the question glyphs (inner accent is LEFT/RIGHT/BOTTOM only)."""
    if not getattr(L, "show_qbar", False) or not hasattr(L, "qbar"): return None
    x0, y0, x1, y1 = L.qbar; w, h = x1 - x0, y1 - y0
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    V = L.fmt == "vertical"
    # outer card
    d.rounded_rectangle([4, 4, w - 5, h - 5], radius=18, fill=ARTPAPER + (245,), outline=INK + (255,), width=4)
    # label band height (exclusive zone for "THE QUESTION")
    band = 56 if V else 48
    # accent rule under the label band only (NOT a full inner rounded rect that can clip text)
    d.line([18, band, w - 18, band], fill=ACCENT + (255,), width=2)
    d.line([18, band + 3, w - 18, band + 3], fill=INK + (90,), width=1)
    # side + bottom accent ticks (no top stroke through the question)
    d.line([12, band + 8, 12, h - 14], fill=ACCENT + (255,), width=2)
    d.line([w - 13, band + 8, w - 13, h - 14], fill=ACCENT + (255,), width=2)
    d.line([14, h - 14, w - 14, h - 14], fill=ACCENT + (255,), width=2)
    # label centred in the band
    lab = "THE QUESTION"; f0 = F("plex", 26 if V else 22)
    tw = d.textlength(lab, font=f0)
    bb = d.textbbox((0, 0), lab, font=f0); th = bb[3] - bb[1]
    d.text(((w - tw) / 2, (band - th) / 2 - 2), lab, font=f0, fill=ACCENT + (255,))
    # question text entirely below the band, with padding from side/bottom accents
    text_top = band + 14
    text_bot = h - 22
    avail = max(36, text_bot - text_top)
    f = F("crimb", 40 if V else 34)
    lines = wrap(d, C.QUESTION, f, w - 80)
    while (len(lines) * int(f.size * 1.25) > avail or len(lines) > 3) and f.size > 26:
        f = F("crimb", f.size - 2); lines = wrap(d, C.QUESTION, f, w - 80)
    lh = int(f.size * 1.25); total = len(lines) * lh
    y = text_top + max(0, (avail - total) / 2)
    for ln in lines:
        tw = d.textlength(ln, font=f)
        bb = d.textbbox((0, 0), ln, font=f)
        d.text(((w - tw) / 2, y - bb[1]), ln, font=f, fill=INK + (255,)); y += lh
    return im


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
# Bitmap (CBDT) Noto Color Emoji, as shipped by Debian. Fedora's COLRv1 build is not equivalent.
EMOJI_FONT = os.environ.get("TIDEWHISTLE_EMOJI_FONT", "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf")
def emoji_img(size):
    if size not in _emoji:
        f = ImageFont.truetype(EMOJI_FONT, 109)   # CBDT bitmap font: 109 px is its only strike
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

# ----------------------------------------------------------------------------- "statements" open (Case 8+)
# A different shape from the case 6/7 open (banner title / framed art / cast strip): chalkboard title slab,
# borderless full-bleed hero art with feathered edges, then a 2x2 suspect grid whose speech bubbles pop in on
# "four statements" and an "ONLY 1 IS TRUE" stamp landing on "one". No suspect is singled out.
CHALK_SLATE = (44, 56, 58); CHALK_INK = (244, 240, 228); CHALK_DUST = (90, 104, 104)

def _word_t(word, nth=0):
    hits = [w for w in HOOK["words"] if re.sub(r"[^a-z0-9]", "", w["w"].lower()) == word]
    return hits[min(nth, len(hits) - 1)]["s"] if hits else None

def chalk_title(L):
    key = ("chalktitle",)
    if key in L.cache: return L.cache[key]
    V = L.fmt == "vertical"; f = F("play", 90 if V else 72); lines = C.HOOK_LINES
    W = (L.W - 80) if V else (L.vw + 0); lh = int(f.size * 1.2); H = lh * len(lines) + 70
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, W - 1, H - 1], radius=26, fill=CHALK_SLATE + (255,), outline=(120, 86, 60, 255), width=10)
    d.rounded_rectangle([18, 18, W - 19, H - 19], radius=16, outline=CHALK_INK + (110,), width=2)
    import random as _r
    rr = _r.Random(8)
    for _ in range(260):   # chalk dust
        x, y = rr.uniform(20, W - 20), rr.uniform(20, H - 20); d.line([x, y, x + rr.uniform(3, 18), y + rr.uniform(-1, 1)], fill=CHALK_DUST + (90,), width=1)
    es = int(f.size * 0.85)
    for i, ln in enumerate(lines):
        last = i == len(lines) - 1
        tw = d.textlength(ln, font=f) + (es + 22 if last else 0); x = (W - tw) / 2; y = 34 + i * lh
        d.text((x, y), ln, font=f, fill=CHALK_INK + (255,))
        if last: e = emoji_img(es); im.alpha_composite(e, (int(x + d.textlength(ln, font=f) + 22), int(y + f.size * 0.25)))
    L.cache[key] = im; return im

def _feather(w, h, edge):
    key = ("feather", w, h, edge)
    if key not in _art:
        m = Image.new("L", (w, h), 255); d = ImageDraw.Draw(m)
        for i in range(edge):
            v = int(255 * ease(i / edge)); d.line([0, i, w, i], fill=v); d.line([0, h - 1 - i, w, h - 1 - i], fill=v)
        _art[key] = m
    return _art[key]

def _bubble(size, a, flip=False):
    key = ("bubble", size, flip)
    if key not in _art:
        w, h = size; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([4, 4, w - 5, h - 34], radius=28, fill=(255, 253, 246, 255), outline=INK + (255,), width=5)
        X = (lambda x: w - x) if flip else (lambda x: x)   # tail on the left (default) or right; the "?" never mirrors
        tail = [(X(w * 0.18), h - 37), (X(w * 0.08), h - 4), (X(w * 0.38), h - 37)]
        d.polygon(tail, fill=(255, 253, 246, 255))
        d.line([(tail[0][0], h - 36), tail[1], tail[2]], fill=INK + (255,), width=5, joint="curve")
        f = F("play", int((h - 34) * 0.72)); bb = d.textbbox((0, 0), "?", font=f)
        d.text(((w - (bb[0] + bb[2])) / 2, (h - 34 - (bb[1] + bb[3])) / 2), "?", font=f, fill=ACCENT + (255,))
        _art[key] = im
    im = _art[key]
    if a >= 0.999: return im
    im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * a))); return im

def _stamp(L):
    key = ("stamp",)
    if key in L.cache: return L.cache[key]
    V = L.fmt == "vertical"; f = F("plex", 60 if V else 42); txt = getattr(C, "HOOK_STAMP", "ONLY 1 IS TRUE")
    d0 = ImageDraw.Draw(Image.new("RGBA", (10, 10))); tw = d0.textlength(txt, font=f)
    w, h = int(tw + 90), int(f.size * 1.75)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); col = (176, 40, 34)
    d.rounded_rectangle([4, 4, w - 5, h - 5], radius=16, fill=(255, 250, 240, 228), outline=col + (255,), width=9)
    d.rounded_rectangle([18, 18, w - 19, h - 19], radius=10, outline=col + (255,), width=3)
    bb = d.textbbox((0, 0), txt, font=f); d.text(((w - (bb[0] + bb[2])) / 2, (h - (bb[1] + bb[3])) / 2), txt, font=f, fill=col + (255,))
    im = im.rotate(7, resample=Image.BICUBIC, expand=True)
    L.cache[key] = im; return im

def hook_frame_statements(L, t):
    V = L.fmt == "vertical"; im = L.bg().copy(); d = ImageDraw.Draw(im)
    # 1. hero art, full bleed (vertical) / borderless (wide), feathered top+bottom, slow push-in
    if V: aw, ah, ax, ay = L.W, 590, 0, 336
    else: aw, ah, ax, ay = 924, 520, 34, 300
    u = ease(t / HOOK_DUR) * 0.6 + 0.4 * (t / HOOK_DUR)
    (ca, cya, za), (cb, cyb, zb) = C.HOOK_FOCUS; cx, cy, z = ca + (cb - ca) * u, cya + (cyb - cya) * u, za + (zb - za) * u
    scene = anim_scene("hook"); W, H = scene.man["W"], scene.man["H"]
    bw = W / z; bh = bw * ah / aw
    if bh > H: bh = H; bw = bh * aw / ah
    bx = min(max(0, cx * W - bw / 2), W - bw); by = min(max(0, cy * H - bh / 2), H - bh)
    hero = scene.frame(t, (bx, by, bw, bh), (aw, ah))
    if V: im.paste(hero, (ax, ay), _feather(aw, ah, 46))
    else:
        m = _feather(aw, ah, 40).copy(); md = ImageDraw.Draw(m)
        for i in range(40):
            v = int(255 * ease(i / 40)); md.line([i, 0, i, ah], fill=v); md.line([aw - 1 - i, 0, aw - 1 - i, ah], fill=v)
        im.paste(hero, (ax, ay), m)
    # 2. chalkboard title slab (drops in a touch from frame 1 — still readable on frame 1)
    ct = chalk_title(L); dy = int(-14 * (1 - ease(t / 0.3)))
    tx, ty = (40, 26) if V else (34 + (924 - ct.width) // 2, 40)
    im.paste(ct, (tx, ty + dy), ct)
    # 3. spoken line
    f3 = F("crimi", 60 if V else 50); capy = 936 if V else 830; capw = (L.W - 80) if V else 924; capx = 40 if V else 34
    for c in HOOK_CAPS:
        if c["s"] <= t < c["e"]:
            a = min(1, (t - c["s"]) / 0.12) if c["s"] > 0 else 1
            lay = Image.new("RGBA", (capw, 170), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
            lines = wrap(dl, curly(c["text"]), f3, capw - 40); y = (160 - len(lines) * 70) // 2
            for ln in lines: ctext(dl, capw / 2, y, ln, f3, INK + (int(255 * a),)); y += 70
            im.paste(lay, (capx, capy), lay); break
    # 4. 2x2 suspect grid (equal cards, idle + blink only)
    gs = anim_scene("grid"); GWp, GHp = gs.man["W"], gs.man["H"]
    gw = 900 if V else 880; gh = int(gw * GHp / GWp)
    gx, gy = ((L.W - gw) // 2, 1110) if V else (1000, 170)
    gy += int(40 * (1 - ease(t / 0.5)))
    im.paste(gs.frame(t, (0, 0, GWp, GHp), (gw, gh)), (gx, gy))
    d.rectangle([gx - 6, gy - 6, gx + gw + 5, gy + gh + 5], outline=INK, width=3)
    # 5. "?" bubbles pop in, one per suspect, on "four statements"
    t_st = _word_t("statements") or 3.6; t_four = (_word_t("four", 1) or t_st - 0.1)
    bw_, bh_ = int(gw * 0.19), int(gw * 0.19 * 0.9)
    for i in range(4):
        tb = t_four + i * 0.16
        if t < tb: continue
        p = ease((t - tb) / 0.22); sc_ = 0.6 + 0.4 * p + 0.08 * math.sin(min(1, (t - tb) / 0.35) * math.pi)
        b = _bubble((bw_, bh_), p, flip=bool(i % 2))
        bob = int(4 * math.sin(2 * math.pi * (t - tb) / 1.6 + i))
        b = b.resize((max(1, int(bw_ * sc_)), max(1, int(bh_ * sc_))), Image.LANCZOS)
        col, row = i % 2, i // 2
        bx_ = gx + int(gw * (0.255 if col == 0 else 0.555)); by_ = gy + int(gh * (0.5 * row + 0.06)) + bob
        im.paste(b, (bx_ + (bw_ - b.width) // 2, by_ + (bh_ - b.height)), b)
    # 6. ONLY 1 IS TRUE stamp lands on "one"
    t_one = _word_t("one") or 4.76
    if t >= t_one - 0.05:
        st = _stamp(L); p = ease((t - t_one + 0.05) / 0.2); s_ = 1.0 + 0.6 * (1 - p)
        s2 = st.resize((int(st.width * s_), int(st.height * s_)), Image.LANCZOS)
        if p < 1: s2.putalpha(s2.getchannel("A").point(lambda v: int(v * p)))
        im.paste(s2, (gx + (gw - s2.width) // 2, gy + (gh - s2.height) // 2), s2)
    # 7. preview label
    n_sus = getattr(C, "LINEUP_PANELS", 4)
    lab = getattr(C, "HOOK_LABEL", f"{n_sus} suspects \u00b7 {n_sus} statements \u00b7 1 truth"); f2 = F("plex", 50 if V else 44)
    ctext(d, gx + gw / 2, gy + gh + 22, lab, f2, ACCENT)
    return im


# ----------------------------------------------------------------------------- "compass" open (Case 9+)
# Unlike case 6 closed-door, case 7 gnome-banner, and case 8 chalkboard-statements: a compass-rose title ring,
# borderless empty-easel hero, three equal suspect cards, a spinning compass that lands pointing EAST, and a
# "ONE STORY FAILS" stamp. Geography tease without naming the culprit.
COMPASS_INK = (46, 58, 72); COMPASS_GOLD = (220, 170, 80)

def compass_title(L):
    key = ("compasstitle",)
    if key in L.cache: return L.cache[key]
    V = L.fmt == "vertical"; f = F("play", 88 if V else 70); lines = C.HOOK_LINES
    W = (L.W - 100) if V else 900; lh = int(f.size * 1.18); H = lh * len(lines) + 56
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    # rounded navy plate with a thin gold compass tick border
    d.rounded_rectangle([0, 0, W - 1, H - 1], radius=30, fill=(36, 48, 68, 255), outline=COMPASS_GOLD + (255,), width=8)
    d.rounded_rectangle([14, 14, W - 15, H - 15], radius=20, outline=(244, 240, 228, 140), width=2)
    # tiny N/E/S/W ticks on the rim
    for lab, (tx, ty) in (("N", (W / 2, 8)), ("E", (W - 22, H / 2 - 10)), ("S", (W / 2, H - 28)), ("W", (10, H / 2 - 10))):
        d.text((tx - 6, ty), lab, font=F("plex", 22), fill=COMPASS_GOLD + (255,))
    es = int(f.size * 0.85)
    for i, ln in enumerate(lines):
        last = i == len(lines) - 1
        tw = d.textlength(ln, font=f) + (es + 20 if last else 0); x = (W - tw) / 2; y = 28 + i * lh
        d.text((x, y), ln, font=f, fill=(250, 246, 236, 255))
        if last:
            e = emoji_img(es); im.alpha_composite(e, (int(x + d.textlength(ln, font=f) + 20), int(y + f.size * 0.22)))
    L.cache[key] = im; return im

def _compass_dial(size, angle_deg, a=1.0):
    """Brass compass dial with needle at angle_deg (0=N, 90=E)."""
    key = ("compassdial", size, int(angle_deg) % 360)
    if key not in _art:
        s = size; im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        m = s // 2; r = s // 2 - 6
        d.ellipse([6, 6, s - 7, s - 7], fill=(250, 246, 232, 255), outline=(160, 120, 50, 255), width=6)
        d.ellipse([18, 18, s - 19, s - 19], outline=(46, 58, 72, 200), width=2)
        f = F("plex", max(18, s // 10))
        for lab, ang in (("N", 270), ("E", 0), ("S", 90), ("W", 180)):
            rad = math.radians(ang); Fx = m + int((r - 22) * math.cos(rad)); Fy = m + int((r - 22) * math.sin(rad))
            bb = d.textbbox((0, 0), lab, font=f)
            d.text((Fx - (bb[2] - bb[0]) / 2, Fy - (bb[3] - bb[1]) / 2), lab, font=f,
                   fill=((196, 84, 64, 255) if lab == "E" else (46, 58, 72, 255)))
        # needle (drawn pointing up / N, then we rotate the whole dial layer separately in the frame)
        d.polygon([(m - 7, m + 8), (m, m - r + 28), (m + 7, m + 8)], fill=(196, 84, 64, 255))
        d.polygon([(m - 5, m - 4), (m, m + r - 32), (m + 5, m - 4)], fill=(46, 58, 72, 220))
        d.ellipse([m - 8, m - 8, m + 8, m + 8], fill=(180, 140, 60, 255))
        _art[key] = im
    im = _art[key]
    # Rotate so 0° on dial (= drawn N-up) becomes the requested bearing (90° = East)
    # Pillow rotate is counter-clockwise; needle was drawn pointing up (screen-north).
    # Want needle to point to `angle_deg` clockwise from north → rotate by -angle_deg.
    rot = im.rotate(-angle_deg, resample=Image.BICUBIC, expand=False)
    if a >= 0.999: return rot
    rot = rot.copy(); rot.putalpha(rot.getchannel("A").point(lambda v: int(v * a))); return rot

def hook_frame_compass(L, t):
    V = L.fmt == "vertical"; im = L.bg().copy(); d = ImageDraw.Draw(im)
    # 1. hero: empty easel, full-bleed feathered
    if V: aw, ah, ax, ay = L.W, 560, 0, 310
    else: aw, ah, ax, ay = 924, 500, 34, 280
    u = ease(t / HOOK_DUR) * 0.6 + 0.4 * (t / HOOK_DUR)
    (ca, cya, za), (cb, cyb, zb) = C.HOOK_FOCUS; cx, cy, z = ca + (cb - ca) * u, cya + (cyb - cya) * u, za + (zb - za) * u
    scene = anim_scene("hook"); W, H = scene.man["W"], scene.man["H"]
    bw = W / z; bh = bw * ah / aw
    if bh > H: bh = H; bw = bh * aw / ah
    bx = min(max(0, cx * W - bw / 2), W - bw); by = min(max(0, cy * H - bh / 2), H - bh)
    hero = scene.frame(t, (bx, by, bw, bh), (aw, ah))
    if V: im.paste(hero, (ax, ay), _feather(aw, ah, 46))
    else:
        m = _feather(aw, ah, 40).copy(); md = ImageDraw.Draw(m)
        for i in range(40):
            v = int(255 * ease(i / 40)); md.line([i, 0, i, ah], fill=v); md.line([aw - 1 - i, 0, aw - 1 - i, ah], fill=v)
        im.paste(hero, (ax, ay), m)
    # 2. compass-rose title
    ct = compass_title(L); dy = int(-12 * (1 - ease(t / 0.3)))
    tx, ty = (50, 22) if V else (34 + (924 - ct.width) // 2, 36)
    im.paste(ct, (tx, ty + dy), ct)
    # 3. spoken line
    f3 = F("crimi", 58 if V else 48); capy = 900 if V else 800; capw = (L.W - 80) if V else 924; capx = 40 if V else 34
    for c in HOOK_CAPS:
        if c["s"] <= t < c["e"]:
            a = min(1, (t - c["s"]) / 0.12) if c["s"] > 0 else 1
            lay = Image.new("RGBA", (capw, 170), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
            lines = wrap(dl, curly(c["text"]), f3, capw - 40); y = (160 - len(lines) * 68) // 2
            for ln in lines: ctext(dl, capw / 2, y, ln, f3, INK + (int(255 * a),)); y += 68
            im.paste(lay, (capx, capy), lay); break
    # 4. three equal suspect cards
    gs = anim_scene("cast"); GWp, GHp = gs.man["W"], gs.man["H"]
    gw = 960 if V else 900; gh = int(gw * GHp / GWp)
    gx, gy = ((L.W - gw) // 2, 1160) if V else (1000, 180)
    gy += int(36 * (1 - ease(t / 0.5)))
    im.paste(gs.frame(t, (0, 0, GWp, GHp), (gw, gh)), (gx, gy))
    d.rectangle([gx - 5, gy - 5, gx + gw + 4, gy + gh + 4], outline=INK, width=3)
    # 5. spinning compass lands on EAST when "fit" / "story" is spoken
    t_spin = _word_t("story") or _word_t("fit") or 3.2
    dial_s = int(gw * 0.28) if V else int(gw * 0.26)
    if t >= t_spin - 1.2:
        # spin then settle on East (90°)
        age = t - (t_spin - 1.2)
        if age < 1.0:
            ang = (age * 720) % 360   # two full spins
            aa = min(1.0, age / 0.2)
        else:
            ang = 90.0; aa = 1.0
        dial = _compass_dial(dial_s, ang, aa)
        dx = gx + (gw - dial.width) // 2; dy = gy + (gh - dial.height) // 2 - (10 if V else 0)
        im.paste(dial, (dx, dy), dial)
    # 6. stamp on "lie" / "spot"
    t_stamp = _word_t("lie") or _word_t("spot") or (HOOK_DUR - 1.2)
    if t >= t_stamp - 0.05:
        st = _stamp(L); p = ease((t - t_stamp + 0.05) / 0.2); s_ = 1.0 + 0.55 * (1 - p)
        s2 = st.resize((int(st.width * s_), int(st.height * s_)), Image.LANCZOS)
        if p < 1: s2.putalpha(s2.getchannel("A").point(lambda v: int(v * p)))
        im.paste(s2, (gx + (gw - s2.width) // 2, gy + gh - s2.height - 8), s2)
    # 7. label
    lab = getattr(C, "HOOK_LABEL", "3 people · 1 painting · 1 wrong story"); f2 = F("plex", 48 if V else 42)
    ctext(d, gx + gw / 2, gy + gh + 20, lab, f2, ACCENT)
    return im

def hook_frame(L, t):
    if getattr(C, "HOOK_STYLE", "") == "statements": return hook_frame_statements(L, t)
    if getattr(C, "HOOK_STYLE", "") == "compass": return hook_frame_compass(L, t)
    if getattr(C, "HOOK_STYLE", "") in HOOK_STYLES: return HOOK_STYLES[C.HOOK_STYLE](L, t)
    V = L.fmt == "vertical"; im = L.bg().copy(); d = ImageDraw.Draw(im)
    # art: slowly pushing in from frame 1 (cases may enlarge / raise it via HOOK_ART_*)
    if V:
        aw, ah = getattr(C, "HOOK_ART_SIZE", (1000, 750))
        ax, ay = (L.W - aw) // 2, getattr(C, "HOOK_ART_Y", 400)
    else:
        aw, ah = L.vw, L.vh; ax, ay = L.view[:2]
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
    # Border: classic double frame, or soft vignette / bleed (HOOK_BORDER=False) for a less-templatey open
    if getattr(C, "HOOK_BORDER", True):
        d.rectangle([ax - 12, ay - 12, ax + aw + 11, ay + ah + 11], outline=INK, width=4)
        d.rectangle([ax - 5, ay - 5, ax + aw + 4, ay + ah + 4], outline=INK, width=1)
    else:
        # soft dark vignette ring so the art breaks the usual 4:3 double-border look
        vig = Image.new("RGBA", (aw + 40, ah + 40), (0, 0, 0, 0))
        gv = Image.radial_gradient("L").resize((aw + 40, ah + 40))
        mask = gv.point(lambda p: int(max(0, (200 - p) * 0.55)))
        dark = Image.new("RGBA", (aw + 40, ah + 40), INK + (0,))
        dark.putalpha(mask)
        im.paste(dark, (ax - 20, ay - 20), dark)
    # big hook text (visible on frame 1, settles with a small pop)
    ht = hook_title(L); sc = 0.93 + 0.07 * ease(t / 0.35)
    hs = ht.resize((int(ht.width * sc), int(ht.height * sc)), Image.LANCZOS)
    title_y = getattr(C, "HOOK_TITLE_Y", 70 if V else 96)
    if getattr(C, "HOOK_TITLE_STYLE", "classic") == "banner" and V:
        # garden / chalk banner behind the title (Case 7+)
        pad_x, pad_y = 36, 18
        bx0 = (L.W - hs.width) // 2 - pad_x; by0 = title_y - pad_y
        bx1 = bx0 + hs.width + 2 * pad_x; by1 = by0 + hs.height + 2 * pad_y
        d.rounded_rectangle([bx0, by0, bx1, by1], radius=22, fill=ARTPAPER, outline=ACCENT, width=5)
        d.rounded_rectangle([bx0 + 8, by0 + 8, bx1 - 8, by1 - 8], radius=16, outline=INK, width=1)
    tx = ((L.W - hs.width) // 2) if V else (958 + (940 - hs.width) // 2)
    ty = title_y + (ht.height - hs.height) // 2
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
    n_sus = getattr(C, "LINEUP_PANELS", 3); lab = f"{n_sus} suspects \u00b7 1 clue"; f2 = F("plex", 54 if V else 50)
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


# ----------------------------------------------------------------------------- "next case" end card (Case 10+)
BOOK_STATUS = os.environ.get("TIDEWHISTLE_BOOK_STATUS", "COMING SOON TO KINDLE")   # same wording as the end card

def _bell(d, cx, cy, s, col):
    """Tiny notification bell (subscribe hint), drawn with PIL."""
    d.chord([cx - s * 0.5, cy - s * 0.55, cx + s * 0.5, cy + s * 0.45], 180, 360, fill=col)
    d.polygon([(cx - s * 0.5, cy - s * 0.06), (cx + s * 0.5, cy - s * 0.06), (cx + s * 0.62, cy + s * 0.32), (cx - s * 0.62, cy + s * 0.32)], fill=col)
    d.ellipse([cx - s * 0.13, cy + s * 0.3, cx + s * 0.13, cy + s * 0.52], fill=col)
    d.ellipse([cx - s * 0.08, cy - s * 0.68, cx + s * 0.08, cy - s * 0.52], fill=col)

def next_card_static(L):
    key = ("nextcard",)
    if key in L.cache: return L.cache[key]
    V = L.fmt == "vertical"; W, H = L.W, L.H
    im = L.bg().copy(); d = ImageDraw.Draw(im)
    m = 46 if V else 40
    d.rectangle([m, m, W - m, H - m], outline=INK, width=4); d.rectangle([m + 10, m + 10, W - m - 10, H - m - 10], outline=INK, width=1)
    last = C.NUM >= TZ.LAST_CASE
    cx = W / 2; maxw = W - 2 * m - (110 if V else 260)
    if not last:
        n = C.NUM + 1; title = TZ.TITLES[n]; teaser = TZ.TEASERS[n]
        y = 500 if V else 120
        lab = "N E X T   C A S E"; ctext(d, cx, y, lab, F("plex", 52 if V else 42), ACCENT); y += 110 if V else 80
        ctext(d, cx, y, f"Case {n}", F("play", 150 if V else 120), INK); y += 190 if V else 150
        f = F("crimi", 84 if V else 70)
        for ln in wrap(d, title, f, maxw): ctext(d, cx, y, ln, f, INK); y += int(f.size * 1.15)
        y += 30; d.line([cx - 170, y, cx + 170, y], fill=ACCENT, width=3); y += 50
        f = F("crim", 60 if V else 50); lines = wrap(d, teaser, f, maxw - (0 if V else 120))
        for ln in lines: ctext(d, cx, y, ln, f, INK); y += int(f.size * 1.25)
        # subscribe box
        bw_ = (W - 2 * m - 120) if V else 1180; bh_ = 250 if V else 190
        by0 = min(y + (110 if V else 50), (H - m - 120 - bh_) if V else (H - m - 70 - bh_))
        bx0 = cx - bw_ / 2
        d.rounded_rectangle([bx0 + 8, by0 + 10, bx0 + bw_ + 8, by0 + bh_ + 10], radius=30, fill=VIGNETTE)
        d.rounded_rectangle([bx0, by0, bx0 + bw_, by0 + bh_], radius=30, fill=ARTPAPER, outline=INK, width=4)
        f1 = F("play", 66 if V else 58); f2 = F("crimi", 54 if V else 46)
        t1 = "New case every 6 hours"; bs = 64 if V else 56
        while d.textlength(t1, font=f1) + bs + 24 > bw_ - 70: f1 = F("play", f1.size - 2)
        tw = d.textlength(t1, font=f1)
        x1 = cx - (tw + bs + 24) / 2
        _bell(d, x1 + bs / 2, by0 + (70 if V else 56), bs, ACCENT)
        d.text((x1 + bs + 24, by0 + (34 if V else 24)), t1, font=f1, fill=INK)
        ctext(d, cx, by0 + (140 if V else 110), "subscribe so you don't miss it", f2, ACCENT)
    else:
        y = 300 if V else 120
        ctext(d, cx, y, "T H E   L A S T   C A S E", F("plex", 52 if V else 42), ACCENT); y += 110 if V else 80
        f = F("crimi", 70 if V else 58)
        for ln in wrap(d, "That was the last case in the book.", f, maxw): ctext(d, cx, y, ln, f, INK); y += int(f.size * 1.2)
        y += 40; d.line([cx - 170, y, cx + 170, y], fill=ACCENT, width=3); y += 60
        f = F("crim", 58 if V else 48)
        for ln in wrap(d, "All 30 cozy mini-mysteries, with every solution, are waiting in the book:", f, maxw):
            ctext(d, cx, y, ln, f, INK); y += int(f.size * 1.25)
        y += 40
        ctext(d, cx, y, "Tea and Clues", F("play", 96 if V else 80), INK); y += 115 if V else 95
        ctext(d, cx, y, "at Tidewhistle Cove", F("play", 76 if V else 64), INK); y += 120 if V else 100
        ctext(d, cx, y, "by Blake La Pierre", F("crim", 60 if V else 52), INK); y += 130 if V else 100
        f = F("plex", 56 if V else 50); tw = d.textlength(BOOK_STATUS, font=f)
        d.rounded_rectangle([cx - tw / 2 - 40, y - 22, cx + tw / 2 + 40, y + 86], radius=18, outline=ACCENT, width=4)
        ctext(d, cx, y, BOOK_STATUS, f, ACCENT); y += 170 if V else 130
        ctext(d, cx, y, "Thank you for solving along with Agnes.", F("crimi", 52 if V else 44), SOFT)
    L.cache[key] = im; return im

def next_card(L, u):
    """u = seconds since the card started: a soft settle (scale 0.97 -> 1) for the first 0.4 s, then static."""
    im = next_card_static(L)
    if u >= 0.4: return im
    sc = 0.97 + 0.03 * ease(u / 0.4); W, H = im.size
    sm = im.resize((int(W * sc), int(H * sc)), Image.BILINEAR); out = L.bg().copy()
    out.paste(sm, ((W - sm.width) // 2, (H - sm.height) // 2)); return out

# ----------------------------------------------------------------------------- shared hook helpers (Case 10+ B&W opens)
def _hook_hero(L, t, rect, feather=46, side_feather=None):
    """Paste the borderless hook hero (anim 'hook') into rect=(x, y, w, h), pushing along HOOK_FOCUS."""
    ax, ay, aw, ah = rect
    u = ease(t / HOOK_DUR) * 0.6 + 0.4 * (t / HOOK_DUR)
    (ca, cya, za), (cb, cyb, zb) = C.HOOK_FOCUS; cx, cy, z = ca + (cb - ca) * u, cya + (cyb - cya) * u, za + (zb - za) * u
    scene = anim_scene("hook"); W, H = scene.man["W"], scene.man["H"]
    bw = W / z; bh = bw * ah / aw
    if bh > H: bh = H; bw = bh * aw / ah
    bx = min(max(0, cx * W - bw / 2), W - bw); by = min(max(0, cy * H - bh / 2), H - bh)
    hero = scene.frame(t, (bx, by, bw, bh), (aw, ah))
    m = _feather(aw, ah, feather).copy()
    if side_feather:
        md = ImageDraw.Draw(m)
        for i in range(side_feather):
            v = int(255 * ease(i / side_feather)); md.line([i, 0, i, ah], fill=v); md.line([aw - 1 - i, 0, aw - 1 - i, ah], fill=v)
        # keep the corner minimum of both ramps
        m = ImageChops_darker(m, _feather(aw, ah, feather))
    return hero, m

def ImageChops_darker(a, b):
    from PIL import ImageChops
    return ImageChops.darker(a, b)

def _hook_caption(L, im, t, rect, size, lh):
    x, y, w, h = rect; f3 = F("crimi", size)
    for c in HOOK_CAPS:
        if c["s"] <= t < c["e"]:
            a = min(1, (t - c["s"]) / 0.12) if c["s"] > 0 else 1
            lay = Image.new("RGBA", (w, h), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
            lines = wrap(dl, curly(c["text"]), f3, w - 40); yy = (h - len(lines) * lh) // 2
            for ln in lines: ctext(dl, w / 2, yy, ln, f3, INK + (int(255 * a),)); yy += lh
            im.paste(lay, (x, y), lay); break

def _hook_cast(L, im, t, x, y, w, rise=36, border=True):
    gs = anim_scene("cast"); GWp, GHp = gs.man["W"], gs.man["H"]; h = int(w * GHp / GWp)
    y += int(rise * (1 - ease(t / 0.5)))
    im.paste(gs.frame(t, (0, 0, GWp, GHp), (w, h)), (x, y))
    if border: ImageDraw.Draw(im).rectangle([x - 5, y - 5, x + w + 4, y + h + 4], outline=INK, width=3)
    return x, y, w, h

def _hook_stamp(L, im, t, t_hit, cx, cy):
    if t < t_hit - 0.05: return
    st = _stamp(L); p = ease((t - t_hit + 0.05) / 0.2); s_ = 1.0 + 0.55 * (1 - p)
    s2 = st.resize((int(st.width * s_), int(st.height * s_)), Image.LANCZOS)
    if p < 1: s2.putalpha(s2.getchannel("A").point(lambda v: int(v * p)))
    im.paste(s2, (int(cx - s2.width / 2), int(cy - s2.height / 2)), s2)

def _hook_t(*words, default=None):
    for w in words:
        v = _word_t(w)
        if v is not None: return v
    return default if default is not None else HOOK_DUR - 1.2

# ----------------------------------------------------------------------------- "wetpaint" open (Case 10)
# A hand-painted hanging sign (title) that swings in on its chains and settles, with wet paint slowly dripping
# off the lettering; a borderless harbour hero (fresh-painted bench, the empty lifeboat-station step); three equal
# luggage-tag suspect cards; ONE ALIBI CRACKS stamp on "cracks". Unlike Case 8 (chalk slab) and Case 9 (compass).
def _sign_board(L):
    key = ("signboard",)
    if key in L.cache: return L.cache[key]
    V = L.fmt == "vertical"; f = F("play", 96 if V else 72); lines = C.HOOK_LINES
    W = (L.W - 120) if V else 880; lh = int(f.size * 1.16); bh = lh * len(lines) + 60; chain = 70 if V else 44; drip = 90
    im = Image.new("RGBA", (W + 40, chain + bh + drip), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    bx0, by0 = 20, chain
    for cxp in (bx0 + W * 0.18, bx0 + W * 0.82):          # chains
        for j in range(0, chain, 14): d.ellipse([cxp - 5, j, cxp + 5, j + 16], outline=INK + (255,), width=3)
    d.rounded_rectangle([bx0, by0, bx0 + W, by0 + bh], radius=14, fill=(255, 255, 253, 255), outline=INK + (255,), width=8)
    d.rounded_rectangle([bx0 + 14, by0 + 14, bx0 + W - 14, by0 + bh - 14], radius=8, outline=INK + (255,), width=2)
    es = int(f.size * 0.82)
    for i, ln in enumerate(lines):
        last = i == len(lines) - 1
        tw = d.textlength(ln, font=f) + (es + 20 if last else 0); x = bx0 + (W - tw) / 2; y = by0 + 26 + i * lh
        d.text((x, y), ln, font=f, fill=INK + (255,))
        if last: e = emoji_img(es); im.alpha_composite(e, (int(x + d.textlength(ln, font=f) + 20), int(y + f.size * 0.22)))
    L.cache[key] = (im, bx0, by0, W, bh); return L.cache[key]

def hook_frame_wetpaint(L, t):
    V = L.fmt == "vertical"; im = L.bg().copy(); d = ImageDraw.Draw(im)
    rect = (0, 350, L.W, 600) if V else (34, 300, 924, 500)
    hero, m = _hook_hero(L, t, rect, feather=46, side_feather=None if V else 40)
    im.paste(hero, rect[:2], m)
    # swinging sign with growing paint drips (drips drawn under the board's bottom edge)
    base, bx0, by0, W, bh = _sign_board(L)
    sg = base.copy(); sd = ImageDraw.Draw(sg)
    rr = __import__("random").Random(10)
    for k in range(9):
        x = bx0 + 40 + rr.uniform(0, W - 80); t0 = 0.3 + rr.uniform(0, 1.6); L_ = 28 + rr.uniform(0, 56)
        grow = ease((t - t0) / 2.4) * L_
        if grow > 1:
            wdt = 6 + rr.uniform(0, 5); y0 = by0 + bh - 3
            sd.rounded_rectangle([x - wdt / 2, y0, x + wdt / 2, y0 + grow], radius=int(wdt / 2), fill=INK + (255,))
            sd.ellipse([x - wdt * 0.8, y0 + grow - wdt * 0.6, x + wdt * 0.8, y0 + grow + wdt], fill=INK + (255,))
    ang = 7.0 * math.exp(-1.5 * t) * math.cos(2 * math.pi * t / 1.25)
    sg = sg.rotate(ang, resample=Image.BICUBIC, center=(sg.width / 2, 0))
    sx = (L.W - sg.width) // 2 if V else 34 + (924 - sg.width) // 2
    im.paste(sg, (sx, 0 if V else 6), sg)
    _hook_caption(L, im, t, (40, 960, L.W - 80, 170) if V else (34, 812, 924, 170), 58 if V else 48, 68)
    gx, gy, gw, gh = _hook_cast(L, im, t, (L.W - 960) // 2 if V else 1000, 1150 if V else 170, 960 if V else 880)
    _hook_stamp(L, im, t, _hook_t("cracks", "spot"), gx + gw / 2, gy + gh * 0.55)
    lab = getattr(C, "HOOK_LABEL", ""); ctext(d, gx + gw / 2, gy + gh + 20, lab, F("plex", 48 if V else 42), ACCENT)
    return im

HOOK_STYLES = {"wetpaint": hook_frame_wetpaint}

# ----------------------------------------------------------------------------- "placecard" open (Case 11)
# A folded RESERVED tent card (title) that flips up from the table; a borderless hero of the four numbered tables
# and the empty windowsill; four numbered seat chips with a "?" ring that hops seat to seat and never settles (no
# spoiler); four equal framed suspect cards; ONE SEAT HIDES IT stamp. Unlike Case 9 (compass) / Case 10 (sign).
def _tent_card(L):
    key = ("tentcard",)
    if key in L.cache: return L.cache[key]
    V = L.fmt == "vertical"; f = F("play", 84 if V else 70); lines = C.HOOK_LINES
    W = (L.W - 160) if V else 860; lh = int(f.size * 1.12); flap = 24 if V else 20; top = 58 if V else 50
    H = flap + top + lh * len(lines) + 34
    im = Image.new("RGBA", (W + 20, H + 14), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([12, 14, W + 12, H + 12], radius=10, fill=VIGNETTE + (255,))                  # shadow
    d.polygon([(0, flap), (W, flap), (W - 18, 0), (18, 0)], fill=(236, 234, 228, 255), outline=INK + (255,))   # folded top
    for x in range(22, W - 20, 9): d.line([x, 3, x - 6, flap - 3], fill=INK + (90,), width=1)
    d.rectangle([0, flap, W, H], fill=(255, 255, 253, 255), outline=INK + (255,), width=6)
    d.rectangle([12, flap + 12, W - 12, H - 12], outline=INK + (255,), width=2)
    ctext(d, W / 2, flap + 16, "R E S E R V E D", F("plex", 40 if V else 32), ACCENT)
    es = int(f.size * 0.8)
    for i, ln in enumerate(lines):
        last = i == len(lines) - 1; tw = d.textlength(ln, font=f) + (es + 18 if last else 0)
        x = (W - tw) / 2; y = flap + top + i * lh; d.text((x, y), ln, font=f, fill=INK + (255,))
        if last: im.alpha_composite(emoji_img(es), (int(x + d.textlength(ln, font=f) + 18), int(y + f.size * 0.2)))
    L.cache[key] = im; return im

def _ease_back(u):
    u = max(0.0, min(1.0, u)); c = 1.9
    return 1 + (c + 1) * (u - 1) ** 3 + c * (u - 1) ** 2

def hook_frame_placecard(L, t):
    V = L.fmt == "vertical"; im = L.bg().copy(); d = ImageDraw.Draw(im)
    rect = (0, 330, L.W, 620) if V else (34, 300, 924, 500)
    hero, m = _hook_hero(L, t, rect, feather=46, side_feather=None if V else 40)
    im.paste(hero, rect[:2], m)
    # tent card flipping up from its bottom fold
    tc = _tent_card(L); sy = 0.5 + 0.5 * _ease_back(t / 0.6); th = max(2, int(tc.height * sy))
    tcs = tc.resize((tc.width, th), Image.BICUBIC); base = 322 if V else 292
    im.paste(tcs, ((L.W - tc.width) // 2 if V else 34 + (924 - tc.width) // 2, base - th), tcs)
    # seat chips 1-4 with a hopping "?" ring (never stops on a seat)
    r = 44 if V else 38; gap = 170 if V else 140
    cx0 = L.W / 2 if V else 1440; cy = 1000 if V else 760
    xs = [cx0 + (i - 1.5) * gap for i in range(4)]
    t_hit = _hook_t("who", "window")
    for i, x in enumerate(xs):
        p = ease((t - 0.15 - 0.2 * i) / 0.25)
        if p <= 0: continue
        rr = r * (0.6 + 0.4 * p)
        d.ellipse([x - rr, cy - rr, x + rr, cy + rr], fill=ARTPAPER, outline=INK, width=4)
        ctext(d, x, cy - rr * 0.72, str(i + 1), F("play", int(rr * 1.2)), INK)
    if 1.0 < t < t_hit:
        ph = (t - 1.0) * 1.6; i0 = int(ph) % 4; i1 = (i0 + 1) % 4; u = ease(ph - int(ph))
        x = xs[i0] + (xs[i1] - xs[i0]) * u if i1 else xs[i0] + (xs[0] - xs[i0]) * u
        hop = 26 * math.sin(math.pi * u)
        d.ellipse([x - r - 12, cy - r - 12 - hop, x + r + 12, cy + r + 12 - hop], outline=ACCENT, width=6)
        ctext(d, x, cy - r - 86 - hop, "?", F("play", 64 if V else 52), ACCENT)
    _hook_caption(L, im, t, (40, 1052, L.W - 80, 140) if V else (34, 812, 924, 170), 56 if V else 48, 66)
    gx, gy, gw, gh = _hook_cast(L, im, t, (L.W - 960) // 2 if V else 1000, 1196 if V else 170, 960 if V else 880, border=False)
    _hook_stamp(L, im, t, t_hit, gx + gw / 2, gy + gh * 0.55)
    lab = getattr(C, "HOOK_LABEL", ""); ctext(d, gx + gw / 2, gy + gh + 20, lab, F("plex", 48 if V else 42), ACCENT)
    return im

HOOK_STYLES["placecard"] = hook_frame_placecard

# ----------------------------------------------------------------------------- "calendar" open (Case 12)
# A tear-off desk calendar beside the title: MON, TUE and WED pages tear away and fall, leaving THU (the day of the
# theft); a borderless hero of the stopped wall clock over the caddy shelf with its empty spot; three equal suspect
# cards; ONE TIME IS WRONG stamp on "he". Unlike Case 10 (swinging sign) and Case 11 (tent card + seat chips).
def _cal_page(L, S, day):
    key = ("calpage", S, day)
    if key in L.cache: return L.cache[key]
    im = Image.new("RGBA", (S, int(S * 0.8)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, S - 1, im.height - 1], fill=(255, 255, 253, 255), outline=INK + (255,), width=4)
    ctext(d, S / 2, int(S * 0.12), day, F("play", int(S * 0.36)), INK)
    d.line([S * 0.2, im.height - S * 0.14, S * 0.8, im.height - S * 0.14], fill=ACCENT, width=3)
    L.cache[key] = im; return im

def _calendar(L, t, S):
    """Desk calendar (binding band + pages) at time t; returns RGBA (S + margin)."""
    W = S + 120; H = int(S * 1.25) + 140
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x0, y0 = 20, 30; band = int(S * 0.22); ph = int(S * 0.8)
    d.rectangle([x0 + 10, y0 + band + 12, x0 + S + 10, y0 + band + ph + 12], fill=VIGNETTE + (255,))       # shadow
    for j in range(4, 0, -1):                                                                             # page stack edges
        d.rectangle([x0 + j * 2, y0 + band + j * 3, x0 + S + j * 2, y0 + band + ph + j * 3], fill=(250, 249, 244, 255), outline=INK + (255,), width=2)
    d.rectangle([x0, y0, x0 + S, y0 + band], fill=INK + (255,))
    ctext(d, x0 + S / 2, y0 + band * 0.26, "THE KETTLE AND GULL", F("plex", int(band * 0.34)), ARTPAPER)
    for cx in (x0 + S * 0.25, x0 + S * 0.75): d.ellipse([cx - 9, y0 - 22, cx + 9, y0 + 14], outline=INK + (255,), width=5)
    days = ["MON", "TUE", "WED", "THU"]; tears = [0.55, 1.15, 1.75]
    n = sum(1 for tt in tears if t >= tt + 0.7)          # pages fully gone
    im.alpha_composite(_cal_page(L, S, days[min(3, n + (1 if any(tt <= t < tt + 0.7 for tt in tears) else 0))]), (x0, y0 + band))
    for i, tt in enumerate(tears):
        if tt <= t < tt + 0.7:
            u = (t - tt) / 0.7; pg = _cal_page(L, S, days[i]).copy()
            if u > 0.5: pg.putalpha(pg.getchannel("A").point(lambda v: int(v * (1 - (u - 0.5) * 2))))
            rot = pg.rotate(-50 * ease(u), resample=Image.BICUBIC, expand=True)
            im.alpha_composite(rot, (int(x0 + 30 * u), int(y0 + band + 120 * u * u)))
    return im

def hook_frame_calendar(L, t):
    V = L.fmt == "vertical"; im = L.bg().copy(); d = ImageDraw.Draw(im)
    rect = (0, 360, L.W, 580) if V else (34, 300, 924, 500)
    hero, m = _hook_hero(L, t, rect, feather=46, side_feather=None if V else 40)
    im.paste(hero, rect[:2], m)
    S = 270 if V else 220
    cal = _calendar(L, t, S); im.paste(cal, (30 if V else 30, 20 if V else 10), cal)
    # title lines to the right of the calendar
    f = F("play", 84 if V else 66); tx0 = (S + 110) if V else (S + 100); tw_max = (L.W - tx0 - 40) if V else (958 - tx0)
    lines = C.HOOK_LINES
    while max(d.textlength(ln, font=f) + (int(f.size * 0.8) + 16 if i == len(lines) - 1 else 0) for i, ln in enumerate(lines)) > tw_max - 10:
        f = F("play", f.size - 2)
    lh = int(f.size * 1.18); es = int(f.size * 0.8); y = (150 - lh * len(lines) // 2 + 20) if V else 60
    sc = 0.94 + 0.06 * ease(t / 0.35)
    for i, ln in enumerate(lines):
        last = i == len(lines) - 1; wln = d.textlength(ln, font=f) + (es + 16 if last else 0)
        x = tx0 + (tw_max - wln) / 2; d.text((x, y), ln, font=f, fill=INK)
        if last:
            e = emoji_img(es); im.paste(e, (int(x + d.textlength(ln, font=f) + 16), int(y + f.size * 0.22)), e)
        y += lh
    d.line([tx0 + 40, y + 14, tx0 + tw_max - 40, y + 14], fill=ACCENT, width=4)
    _hook_caption(L, im, t, (40, 960, L.W - 80, 170) if V else (34, 812, 924, 170), 58 if V else 48, 68)
    gx, gy, gw, gh = _hook_cast(L, im, t, (L.W - 960) // 2 if V else 1000, 1150 if V else 170, 960 if V else 880)
    _hook_stamp(L, im, t, _hook_t("times", "sure"), gx + gw / 2, gy + gh * 0.55)
    lab = getattr(C, "HOOK_LABEL", ""); ctext(d, gx + gw / 2, gy + gh + 20, lab, F("plex", 48 if V else 42), ACCENT)
    return im

HOOK_STYLES["calendar"] = hook_frame_calendar

# ----------------------------------------------------------------------------- "redpen" open (Case 13)
# The title handwritten on a torn sheet of ruled notepaper; a red pen nib then draws a wavy correction underline
# under it and ticks a "?" in the margin; borderless hero of the harbour office's empty shelf with the folded note;
# three equal framed suspect cards; ONE WORD GIVES IT AWAY stamp on "word". Unlike Case 11/12 (tent card, calendar).
def _note_title(L):
    key = ("notetitle",)
    if key in L.cache: return L.cache[key]
    V = L.fmt == "vertical"; f = F("crimi", 112 if V else 84); lines = C.HOOK_LINES
    W = (L.W - 120) if V else 860; lh = int(f.size * 1.05); H = lh * len(lines) + (90 if V else 70)
    im = Image.new("RGBA", (W + 30, H + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rr = __import__("random").Random(13); edge = [(W, H)]
    x = W
    while x > 0: x -= rr.uniform(18, 34); edge.append((max(0, x), H + rr.uniform(-10, 10)))
    poly = [(0, 0), (W, 0)] + edge + [(0, H)]
    d.polygon([(px + 12, py + 14) for px, py in poly], fill=VIGNETTE + (255,))
    d.polygon(poly, fill=(255, 255, 252, 255), outline=INK + (255,))
    for yy in range(46, H - 10, 44 if V else 36): d.line([16, yy, W - 16, yy], fill=(150, 170, 190, 255), width=2)
    d.line([90, 6, 90, H - 12], fill=ACCENT + (255,), width=3)
    es = int(f.size * 0.7); y = 24; spans = []
    for i, ln in enumerate(lines):
        last = i == len(lines) - 1; tw = d.textlength(ln, font=f) + (es + 16 if last else 0); x0 = 90 + (W - 90 - tw) / 2
        d.text((x0, y), ln, font=f, fill=INK + (255,))
        if last: im.alpha_composite(emoji_img(es), (int(x0 + d.textlength(ln, font=f) + 16), int(y + f.size * 0.3)))
        spans.append((x0, x0 + d.textlength(ln, font=f), y + int(f.size * 1.08))); y += lh
    L.cache[key] = (im, spans); return L.cache[key]

def hook_frame_redpen(L, t):
    V = L.fmt == "vertical"; im = L.bg().copy(); d = ImageDraw.Draw(im)
    rect = (0, 360, L.W, 580) if V else (34, 300, 924, 500)
    hero, m = _hook_hero(L, t, rect, feather=46, side_feather=None if V else 40)
    im.paste(hero, rect[:2], m)
    base, spans = _note_title(L); pg = base.copy(); pd = ImageDraw.Draw(pg)
    x0, x1, yb = spans[-1]; u = ease((t - 0.35) / 1.1)
    if u > 0:
        n = 60; pts = [(x0 + (x1 - x0) * u * i / n, yb + 7 * math.sin(i / n * u * (x1 - x0) / 26)) for i in range(n + 1)]
        pd.line(pts, fill=ACCENT + (255,), width=7, joint="curve")
        if u < 1:   # pen nib at the tip
            px, py = pts[-1]
            pd.polygon([(px, py), (px + 16, py - 34), (px + 34, py - 26)], fill=INK + (255,))
            pd.polygon([(px + 16, py - 34), (px + 34, py - 26), (px + 96, py - 118), (px + 78, py - 126)], fill=ACCENT + (255,))
    if t > 1.6:
        q = ease((t - 1.6) / 0.25); fq = F("play", int((70 if V else 56) * (0.6 + 0.4 * q)))
        pd.text((26, 24), "?", font=fq, fill=ACCENT + (int(255 * q),))
    pg = pg.rotate(1.5, resample=Image.BICUBIC, expand=True)
    im.paste(pg, ((L.W - pg.width) // 2 if V else 34 + (924 - pg.width) // 2, 14 if V else 4), pg)
    _hook_caption(L, im, t, (40, 960, L.W - 80, 170) if V else (34, 812, 924, 170), 58 if V else 48, 68)
    gx, gy, gw, gh = _hook_cast(L, im, t, (L.W - 960) // 2 if V else 1000, 1150 if V else 170, 960 if V else 880, border=False)
    _hook_stamp(L, im, t, _hook_t("word", "away"), gx + gw / 2, gy + gh * 0.55)
    lab = getattr(C, "HOOK_LABEL", ""); ctext(d, gx + gw / 2, gy + gh + 20, lab, F("plex", 48 if V else 42), ACCENT)
    return im

HOOK_STYLES["redpen"] = hook_frame_redpen

# ----------------------------------------------------------------------------- "keyhole" open (Case 14)
# The title on a long key-fob tag with a key on its ring; the hero (the hall door and the plant pot) is first seen
# through a keyhole that opens out to the full picture; three equal luggage-tag suspect cards; ONE SLIP OF THE TONGUE
# stamp on "slip". Unlike Case 12 (calendar) and Case 13 (red pen notepaper).
def _key_fob(L):
    key = ("keyfob",)
    if key in L.cache: return L.cache[key]
    V = L.fmt == "vertical"; f = F("play", 88 if V else 68); lines = C.HOOK_LINES
    W = (L.W - 120) if V else 880; lh = int(f.size * 1.15); H = lh * len(lines) + 56; hole = int(H * 0.5)
    im = Image.new("RGBA", (W + 24, H + 24), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([12, 14, W + 12, H + 12], radius=H // 2, fill=VIGNETTE + (255,))
    d.rounded_rectangle([0, 0, W, H], radius=H // 2, fill=(255, 255, 252, 255), outline=INK + (255,), width=7)
    d.rounded_rectangle([14, 14, W - 14, H - 14], radius=H // 2 - 14, outline=INK + (255,), width=2)
    cx, cy = H // 2, H // 2
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=L.bg().getpixel((5, 5)) + (255,), outline=INK + (255,), width=5)
    # split key ring through the hole, crossing the fob's edge
    d.arc([cx - 70, cy - 46, cx + 2, cy + 46], 60, 330, fill=INK + (255,), width=6)
    d.arc([cx - 64, cy - 40, cx - 4, cy + 40], 70, 320, fill=INK + (255,), width=2)
    es = int(f.size * 0.8); x_text0 = H; y = 26
    for i, ln in enumerate(lines):
        last = i == len(lines) - 1; tw = d.textlength(ln, font=f) + (es + 16 if last else 0)
        x = x_text0 + (W - x_text0 - 30 - tw) / 2; d.text((x, y), ln, font=f, fill=INK + (255,))
        if last: im.alpha_composite(emoji_img(es), (int(x + d.textlength(ln, font=f) + 16), int(y + f.size * 0.22)))
        y += lh
    L.cache[key] = im; return im

def _keyhole_mask(w, h, scale):
    from PIL import ImageFilter
    m = Image.new("L", (w, h), 0); d = ImageDraw.Draw(m)
    r = h * 0.28 * scale; cx, cy = w / 2, h * 0.42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    d.polygon([(cx - r * 0.45, cy + r * 0.5), (cx + r * 0.45, cy + r * 0.5), (cx + r * 0.9, cy + r * 2.4), (cx - r * 0.9, cy + r * 2.4)], fill=255)
    return m.filter(ImageFilter.GaussianBlur(6))

def hook_frame_keyhole(L, t):
    V = L.fmt == "vertical"; im = L.bg().copy(); d = ImageDraw.Draw(im)
    rect = (0, 330, L.W, 600) if V else (34, 300, 924, 500)
    hero, m = _hook_hero(L, t, rect, feather=46, side_feather=None if V else 40)
    u = ease(t / 1.3)
    if u < 1:
        km = _keyhole_mask(rect[2], rect[3], 1.25 + 4.5 * u * u)
        m = ImageChops_darker(m, km)
    im.paste(hero, rect[:2], m)
    fob = _key_fob(L); sw = 4.0 * math.exp(-2.0 * t) * math.sin(2 * math.pi * t / 0.9)
    fr = fob.rotate(sw, resample=Image.BICUBIC, center=(fob.height // 2, fob.height // 2))
    im.paste(fr, ((L.W - fob.width) // 2 if V else 34 + (924 - fob.width) // 2, 24 if V else 20), fr)
    _hook_caption(L, im, t, (40, 950, L.W - 80, 170) if V else (34, 812, 924, 170), 58 if V else 48, 68)
    gx, gy, gw, gh = _hook_cast(L, im, t, (L.W - 960) // 2 if V else 1000, 1150 if V else 170, 960 if V else 880, border=False)
    _hook_stamp(L, im, t, _hook_t("slip", "tongue"), gx + gw / 2, gy + gh * 0.55)
    lab = getattr(C, "HOOK_LABEL", ""); ctext(d, gx + gw / 2, gy + gh + 20, lab, F("plex", 48 if V else 42), ACCENT)
    return im

HOOK_STYLES["keyhole"] = hook_frame_keyhole

# ----------------------------------------------------------------------------- "wiper" open (Case 15)
# The title on a frosted car windscreen (readable faintly from frame 1); a wiper blade sweeps across and clears the frost,
# then swings back to rest; borderless hero below; three equal suspect cards; THE CAT KNOWS stamp on "cat".
# Unlike Case 14 (keyhole) and Case 13 (red pen notepaper).
def _windscreen(L):
    from PIL import ImageChops
    key = ("windscreen",)
    if key in L.cache: return L.cache[key]
    import random as _r
    V = L.fmt == "vertical"; f = F("play", 86 if V else 66); lines = C.HOOK_LINES
    W = (L.W - 120) if V else 880; lh = int(f.size * 1.15); H = lh * len(lines) + 90; inset = int(W * 0.06)
    poly = [(inset, 6), (W - inset, 6), (W - 6, H - 6), (6, H - 6)]
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(base)
    d.polygon(poly, fill=(255, 255, 252, 255))
    es = int(f.size * 0.8); y = 40
    for i, ln in enumerate(lines):
        last = i == len(lines) - 1; tw = d.textlength(ln, font=f) + (es + 16 if last else 0)
        x = (W - tw) / 2; d.text((x, y), ln, font=f, fill=INK + (255,))
        if last: base.alpha_composite(emoji_img(es), (int(x + d.textlength(ln, font=f) + 16), int(y + f.size * 0.22)))
        y += lh
    scr = Image.new("L", (W, H), 0); ImageDraw.Draw(scr).polygon(poly, fill=255)
    frost = Image.new("RGBA", (W, H), (236, 236, 232, 0)); fd = ImageDraw.Draw(frost); rr = _r.Random(15)
    fd.polygon(poly, fill=(236, 236, 232, 190))
    for _ in range(int(W * H / 900)):
        cx, cy, r = rr.uniform(0, W), rr.uniform(0, H), rr.uniform(4, 14)
        for k in range(3):
            a = rr.uniform(0, math.pi) + k * math.pi / 3
            fd.line([(cx - r * math.cos(a), cy - r * math.sin(a)), (cx + r * math.cos(a), cy + r * math.sin(a))], fill=(255, 255, 255, 230), width=2)
    frost.putalpha(ImageChops.multiply(frost.getchannel("A"), scr))
    out = (base, frost, poly, W, H); L.cache[key] = out; return out

def _wiper_angle(t):
    """degrees, PIL convention (0 = 3 o'clock, clockwise): rest at 186 (lying left), up through 270, across to 354."""
    if t < 0.25: return 186.0, 186.0
    if t < 1.15: a = 186 + 168 * ease((t - 0.25) / 0.9); return a, a
    return 354 - 168 * ease((t - 1.25) / 0.6) if t > 1.25 else 354.0, 354.0

def hook_frame_wiper(L, t):
    from PIL import ImageChops
    V = L.fmt == "vertical"; im = L.bg().copy(); d = ImageDraw.Draw(im)
    rect = (0, 330, L.W, 600) if V else (34, 300, 924, 500)
    hero, m = _hook_hero(L, t, rect, feather=46, side_feather=None if V else 40)
    im.paste(hero, rect[:2], m)
    base, frost, poly, W, H = _windscreen(L)
    blade, swept = _wiper_angle(t)
    cx, cy, rx, ry = W / 2, H - 4, W * 0.56, H * 1.02
    clear = Image.new("L", (W, H), 0)
    if swept > 186.5: ImageDraw.Draw(clear).pieslice([cx - rx, cy - ry, cx + rx, cy + ry], 186, swept, fill=255)
    fa = ImageChops.subtract(frost.getchannel("A"), clear); fr = frost.copy(); fr.putalpha(fa)
    panel = base.copy(); panel.alpha_composite(fr); pd = ImageDraw.Draw(panel)
    pd.line(poly + [poly[0]], fill=INK + (255,), width=7, joint="curve")
    a = math.radians(blade); ex, ey = cx + rx * 0.97 * math.cos(a), cy + ry * 0.97 * math.sin(a)
    pd.line([(cx, cy), (ex, ey)], fill=INK + (255,), width=9)
    pd.line([(cx, cy), (cx + (ex - cx) * 0.55 + 6 * math.sin(a), cy + (ey - cy) * 0.55 - 6 * math.cos(a))], fill=INK + (255,), width=4)
    pd.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=INK + (255,))
    px = (L.W - W) // 2 if V else 34 + (924 - W) // 2
    im.paste(panel, (px, 24 if V else 20), panel)
    _hook_caption(L, im, t, (40, 950, L.W - 80, 170) if V else (34, 812, 924, 170), 58 if V else 48, 68)
    gx, gy, gw, gh = _hook_cast(L, im, t, (L.W - 960) // 2 if V else 1000, 1150 if V else 170, 960 if V else 880, border=False)
    _hook_stamp(L, im, t, _hook_t("cat", "ginger"), gx + gw / 2, gy + gh * 0.55)
    lab = getattr(C, "HOOK_LABEL", ""); ctext(d, gx + gw / 2, gy + gh + 20, lab, F("plex", 48 if V else 42), ACCENT)
    return im

HOOK_STYLES["wiper"] = hook_frame_wiper

def fit(L, im): return im if im.size == (L.vw, L.vh) else im.resize((L.vw, L.vh), Image.LANCZOS)

def scene_frame(L, sc, t):
    if sc["k"] == "hook": return hook_frame(L, t)
    if sc["k"] in ("title", "end"): return full_card(L, sc["k"], t)
    if sc["k"] == "next": return next_card(L, t - sc["t0"])
    im = L.chrome().copy()
    if sc["k"] in ("art", "pan"): v = viewport(L, sc, t)
    elif sc["k"] == "ask": v = fit(L, ask_panel(t))
    else: v = fit(L, soltitle_panel(t))
    im.paste(v, L.view[:2])
    nb = L.notebook.render(t, review=(sc["k"] == "ask"))
    im.paste(nb, L.nb[:2], nb)
    # Mid-screen question bar (between art and notebook) — always on for art/pan/ask when SHOW_QBAR
    if L.show_qbar and sc["k"] in ("art", "pan", "ask"):
        qb = question_bar(L, t)
        if qb is not None: im.paste(qb, L.qbar[:2], qb)
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
    in_card = any(sc["k"] in ("hook", "title", "end", "next") and sc["t0"] <= t < sc["t1"] for sc in SCENES)
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
           "-pix_fmt", "yuv420p", "-g", "60", *X264_THREADS, out]
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
    with ProcessPoolExecutor(WORKERS or parts) as ex: outs = list(ex.map(render_chunk, jobs))
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
