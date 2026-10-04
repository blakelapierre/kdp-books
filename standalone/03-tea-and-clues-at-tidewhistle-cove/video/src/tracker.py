"""Clue tracker: an 'Agnes's Notebook' panel that fills in as the narrator speaks each clue.

Reusable for any case: clues live in ../clues/case-NN.json (sections, items, solution marks), times come
from the case's word timestamps. Usage:
    nb = Notebook(spec_path, words, w, h)        # words: [{w, s, e, seg}, ...] in video time
    img = nb.render(t, review=False)             # RGB image of the panel at time t
Fairness rules baked in: every item gets the identical pop-in + highlight and the same ink, so nothing hints
at the answer before the solution. Solution marks (circle / strike / check / note) only come from 'solution'."""
import json, math, re
from PIL import Image, ImageDraw, ImageFont

G = "/usr/share/fonts/truetype/sand-box/google/"
HAND = G + "Kalam/Kalam-Regular.ttf"; HANDB = G + "Kalam/Kalam-Bold.ttf"
PAGE = (253, 250, 240); RULE = (178, 202, 226); MARGIN = (222, 140, 130); INKC = (32, 36, 58)
HEAD = (150, 70, 52); RED = (196, 38, 38); HI = (255, 225, 110); DIM = (150, 146, 140); SHADOW = (196, 182, 160)

def ease(u): u = min(1.0, max(0.0, u)); return u * u * (3 - 2 * u)
def norm(w): return re.sub(r"[^a-z0-9]", "", w.lower().replace("\u2019", "'"))

def anchor_time(words, at):
    """Start time of the last word of `phrase` inside narration segment `seg` (or an explicit {t: sec})."""
    if "t" in at: return float(at["t"])
    ph = [norm(x) for x in at["phrase"].split()]
    ws = [w for w in words if w["seg"] == at["seg"]]; nw = [norm(w["w"]) for w in ws]
    for i in range(len(ws) - len(ph) + 1):
        if nw[i:i + len(ph)] == ph: return ws[i + len(ph) - 1]["s"]
    raise ValueError(f"phrase not found: {at}")

class Notebook:
    def __init__(s, spec_path, words, W, H, max_fs=40, min_fs=26):
        s.spec = json.load(open(spec_path)); s.W, s.H = W, H
        for it in s.spec["items"]: it["t"] = anchor_time(words, it["at"])
        s.marks = []
        for m in s.spec.get("solution", []):
            m = dict(m); m["t"] = anchor_time(words, m["at"]) + m.get("delay", 0.0); s.marks.append(m)
        s.items = {it["id"]: it for it in s.spec["items"]}
        for fs in range(max_fs, min_fs - 1, -1):
            if s._layout(fs): break
        s._paper(); s._sprites(); s.cache = {}

    # ------------------------------------------------------------------ layout
    def _tokens(s, it):
        toks = []
        if it.get("name"): toks += [(w, "b") for w in (it["name"] + " \u2014").split()]
        toks += [(w, "r") for w in it["text"].split()]
        return toks

    def _wrap(s, toks, maxw):
        rows, cur, x = [], [], 0.0
        for w, f in toks:
            font = s.fb if f == "b" else s.fr; ww = font.getlength(w); sp = s.fr.getlength(" ")
            if cur and x + sp + ww > maxw: rows.append(cur); cur, x = [], 0.0
            if cur: x += sp
            cur.append((x, w, f)); x += ww
        if cur: rows.append(cur)
        # no widows: pull words down until the last row is at least a third of the width
        def rowlen(r): return r[-1][0] + (s.fb if r[-1][2] == "b" else s.fr).getlength(r[-1][1])
        def relay(ws):
            out, x = [], 0.0
            for w, f in ws:
                if out: x += s.fr.getlength(" ")
                out.append((x, w, f)); x += (s.fb if f == "b" else s.fr).getlength(w)
            return out
        while len(rows) > 1 and rowlen(rows[-1]) < maxw / 3 and len(rows[-2]) > 2:
            moved = rows[-2][-1]; prev = relay([(w, f) for _, w, f in rows[-2][:-1]])
            last = relay([(moved[1], moved[2])] + [(w, f) for _, w, f in rows[-1]])
            if rowlen(last) > maxw: break
            rows[-2], rows[-1] = prev, last
        return rows

    def _layout(s, fs):
        s.fs = fs; s.fr = ImageFont.truetype(HAND, fs); s.fb = ImageFont.truetype(HANDB, fs)
        s.fh = ImageFont.truetype(HANDB, int(fs * 0.86)); s.ft = ImageFont.truetype(HANDB, int(fs * 1.12))
        s.lh = int(fs * 1.25); s.top = int(s.H * 0.02) + 34 + int(fs * 1.5)   # spiral + title band
        s.mx = int(fs * 2.3); s.pad_r = int(fs * 0.6)
        y = s.top + int(s.lh * 0.15); s.rows = {}; s.heads = []
        for sec in s.spec["sections"]:
            s.heads.append((sec["heading"].upper(), y)); y += s.lh
            for it in s.spec["items"]:
                if it["section"] != sec["id"]: continue
                ind = int(fs * 1.1) if it.get("parent") else 0
                rws = s._wrap(s._tokens(it), s.W - s.mx - s.pad_r - ind - (fs if not it.get("name") and not it.get("parent") else 0))
                bullet = not it.get("name") and not it.get("parent")
                x0 = s.mx + ind + (fs if bullet else 0)
                it["_rows"] = [(x0, y + k * s.lh, r) for k, r in enumerate(rws)]; it["_bullet"] = bullet; it["_x0"] = x0
                y += len(rws) * s.lh
            y += int(s.lh * 0.25)
        return y + int(s.lh * 0.1) <= s.H

    # ------------------------------------------------------------------ static paper
    def _paper(s):
        W, H = s.W, s.H; im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([8, 10, W - 1, H - 1], radius=14, fill=SHADOW + (255,))
        d.rounded_rectangle([0, 0, W - 9, H - 11], radius=14, fill=PAGE + (255,), outline=(120, 104, 88, 255), width=2)
        y = s.top + int(s.lh * 0.15) + s.lh - int(s.fs * 0.28)
        while y < H - 20:
            d.line([(10, y), (W - 20, y)], fill=RULE + (255,), width=2); y += s.lh
        d.line([(s.mx - int(s.fs * 0.5), s.top - 6), (s.mx - int(s.fs * 0.5), H - 14)], fill=MARGIN + (255,), width=3)
        n = max(6, int(W / 70))
        for i in range(n):   # spiral binding
            x = int((i + 0.5) * (W - 9) / n)
            d.ellipse([x - 9, 14, x + 9, 32], fill=(90, 80, 72, 255))
            d.arc([x - 13, -6, x + 13, 26], 200, 340, fill=(70, 66, 64, 255), width=5)
        t = s.spec["title"]; tw = s.ft.getlength(t)
        d.text((s.mx - int(s.fs * 0.2), 34 + int(s.fs * 0.05)), t, font=s.ft, fill=INKC + (255,))
        d.line([(s.mx - int(s.fs * 0.2), 34 + int(s.fs * 1.38)), (s.mx + tw, 34 + int(s.fs * 1.38))], fill=INKC + (255,), width=2)
        for h, y in s.heads:
            d.text((s.mx, y + int(s.fs * 0.18)), h, font=s.fh, fill=HEAD + (255,))
        s.paper = im
        s.title_right = s.mx + tw + int(s.fs * 0.6)

    def _draw_rows(s, d, rows, color, ox=0, oy=0, bullet=False):
        for k, (x0, y, r) in enumerate(rows):
            if bullet and k == 0: d.text((x0 - s.fs + ox, y + oy), "\u2022", font=s.fb, fill=color)
            for x, w, f in r: d.text((x0 + x + ox, y + oy), w, font=s.fb if f == "b" else s.fr, fill=color)

    def _bbox(s, rows, span=None):
        xs0 = min(x0 for x0, _, _ in rows); y0 = rows[0][1]; y1 = rows[-1][1] + s.lh
        if span == "name":
            r = rows[0][2]; nm = [t for t in r if t[2] == "b" and t[1] != "\u2014"]
            x1 = rows[0][0] + nm[-1][0] + s.fb.getlength(nm[-1][1]); return (rows[0][0], y0, x1, y0 + s.lh)
        x1 = max(x0 + r[-1][0] + (s.fb if r[-1][2] == "b" else s.fr).getlength(r[-1][1]) for x0, _, r in rows)
        return (xs0, y0, x1, y1)

    def _sprites(s):
        """Each item as its own RGBA sprite (normal + dimmed) for the pop-in animation."""
        s.spr = {}
        for it in s.spec["items"]:
            bb = s._bbox(it["_rows"]); x0 = int(bb[0] - s.fs * (1.2 if it["_bullet"] else 0.2)); y0 = int(bb[1]); x1 = int(bb[2] + 6); y1 = int(bb[3])
            it["_bb"] = bb; it["_sbox"] = (x0, y0)
            for key, col in (("n", INKC), ("d", DIM)):
                im = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
                s._draw_rows(d, it["_rows"], col + (255,), -x0, -y0, it["_bullet"]); s.spr[(it["id"], key)] = im
    # ------------------------------------------------------------------ per-frame
    def _struck(s, iid, t):
        for m in s.marks:
            ids = m["item"] if isinstance(m.get("item"), list) else [m.get("item")]
            if m["do"] == "strike" and iid in ids and t >= m["t"]: return min(1.0, (t - m["t"]) / 0.55)
        return 0.0

    def render(s, t, review=False):
        im = s.paper.copy(); d = ImageDraw.Draw(im, "RGBA")
        if review:   # countdown: the whole notebook, labelled as the full set of clues
            lab = s.spec.get("review_label", "Every clue so far"); f = ImageFont.truetype(HAND, int(s.fs * 0.8))
            lw = f.getlength(lab); x = s.W - 30 - lw
            if x > s.title_right:
                d.rounded_rectangle([x - 14, 38, x + lw + 14, 38 + int(s.fs * 1.15)], radius=10, fill=(255, 236, 160, 255), outline=HEAD + (255,), width=2)
                d.text((x, 38 + int(s.fs * 0.05)), lab, font=f, fill=HEAD + (255,))
        for it in s.spec["items"]:
            dt = t - it["t"]
            if dt < 0: continue
            # highlighter swipe behind the new line: identical for every item
            if dt < 3.2:
                a = ease(dt / 0.35) * (1 - ease((dt - 2.2) / 1.0)); grow = ease(dt / 0.4)
                for x0, y, r in it["_rows"]:
                    xe = x0 + r[-1][0] + (s.fb if r[-1][2] == "b" else s.fr).getlength(r[-1][1])
                    xs = x0 - (s.fs if it["_bullet"] else 0) - 6
                    d.rounded_rectangle([xs, y + s.fs * 0.12, xs + (xe + 8 - xs) * grow, y + s.lh - s.fs * 0.12], radius=6, fill=HI + (int(200 * a),))
            sk = s._struck(it["id"], t); spr = s.spr[(it["id"], "d" if sk >= 1 else "n")]
            x0, y0 = it["_sbox"]
            if dt < 0.45:   # pop in: fade + settle from 112 % scale
                u = ease(dt / 0.45); sc = 1.12 - 0.12 * u
                sp = spr.resize((max(1, int(spr.width * sc)), max(1, int(spr.height * sc))), Image.BILINEAR)
                al = sp.getchannel("A").point(lambda v: int(v * u)); sp.putalpha(al)
                im.alpha_composite(sp, (int(x0 - (sp.width - spr.width) * 0.1), int(y0 - (sp.height - spr.height) / 2)))
            else:
                im.alpha_composite(spr, (x0, y0))
            if sk > 0:
                for x0r, y, r in it["_rows"]:
                    xe = x0r + r[-1][0] + (s.fb if r[-1][2] == "b" else s.fr).getlength(r[-1][1]); xs = x0r - 4
                    k = it["_rows"].index((x0r, y, r)); u = max(0.0, min(1.0, sk * len(it["_rows"]) - k))
                    if u > 0:
                        ym = y + s.lh * 0.56
                        d.line([(xs, ym + 2), (xs + (xe - xs + 8) * u, ym - 2)], fill=RED + (255,), width=max(3, s.fs // 10))
        for m in s.marks:
            dt = t - m["t"]
            if dt < 0: continue
            if m["do"] == "check":
                it = s.items[m["item"]]; x0, y, _ = it["_rows"][0]; cx = s.mx - s.fs * 1.55; cy = y + s.lh * 0.5
                pts = [(cx - s.fs * 0.36, cy - s.fs * 0.02), (cx - s.fs * 0.08, cy + s.fs * 0.3), (cx + s.fs * 0.5, cy - s.fs * 0.46)]
                u = ease(dt / 0.35) * 2
                d.line([pts[0], (pts[0][0] + (pts[1][0] - pts[0][0]) * min(1, u), pts[0][1] + (pts[1][1] - pts[0][1]) * min(1, u))], fill=RED + (255,), width=max(4, s.fs // 7))
                if u > 1: d.line([pts[1], (pts[1][0] + (pts[2][0] - pts[1][0]) * (u - 1), pts[1][1] + (pts[2][1] - pts[1][1]) * (u - 1))], fill=RED + (255,), width=max(4, s.fs // 7))
            elif m["do"] == "circle":
                it = s.items[m["item"]]; bb = s._bbox(it["_rows"], m.get("span"))
                cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2; rx = (bb[2] - bb[0]) / 2 + s.fs * 0.5; ry = (bb[3] - bb[1]) / 2 + s.fs * 0.05
                rx = min(rx, cx - 4, s.W - 16 - cx)
                u = ease(dt / 0.8); n = int(64 * 1.12 * u) + 1; pts = []
                for i in range(n):
                    a = math.radians(200 - 360 * 1.12 * i / 64); g = 1 + 0.035 * i / 64
                    pts.append((cx + rx * g * math.cos(a), cy - ry * g * math.sin(a) + 2 * math.sin(i / 9)))
                if len(pts) > 1: d.line(pts, fill=RED + (255,), width=max(4, s.fs // 8), joint="curve")
        return im

    def note_image(s, t, width, fs):
        """The solution's red 'how Agnes knows' note as a torn notebook slip (RGBA), or None before its time.
        Placed by the caller (over the bottom of the picture) so the clue list itself never has to shrink."""
        ms = [m for m in s.marks if m["do"] == "note" and t >= m["t"]]
        if not ms: return None
        m = ms[-1]; u = ease((t - m["t"]) / 0.5); key = ("note", width, fs)
        if "hold" in m: u = min(u, 1 - ease((t - m["t"] - m["hold"]) / 0.6))
        if u <= 0: return None
        if key not in s.cache:
            f = ImageFont.truetype(HANDB, fs); d0 = ImageDraw.Draw(Image.new("RGB", (8, 8)))
            words, rows, cur = m["text"].split(), [], ""
            for w in words:
                tr = (cur + " " + w).strip()
                if f.getlength(tr) <= width - 2.2 * fs or not cur: cur = tr
                else: rows.append(cur); cur = w
            rows.append(cur); lh = int(fs * 1.25); h = lh * len(rows) + int(fs * 0.9)
            im = Image.new("RGBA", (width, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
            d.rectangle([6, 6, width - 1, h - 1], fill=SHADOW + (255,))
            d.rectangle([0, 0, width - 7, h - 7], fill=(255, 246, 196, 255), outline=(150, 120, 80, 255), width=2)
            for k, r in enumerate(rows): d.text((fs, int(fs * 0.3) + k * lh), r, font=f, fill=RED + (255,))
            s.cache[key] = im
        im = s.cache[key].copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * u)))
        return im
