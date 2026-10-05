"""layers: draw one picture as an animation-ready PLATE + PARTS (for anim.py). Reusable by any case's art script.

    job = dict(name="harbour", w=512, h=384, plate=draw_plate, parts={
              "quill": dict(fn=draw_quill, variants=["base", "base+blink", "base+talk"]),
              "gull":  dict(fn=draw_gull, variants=["f0", "f1", "f2"], page=(60, 30)),   # small page: an fx sprite
          }, seed=31)
    save_layers(out_dir, job, make_ink)          # make_ink(canvas, seed) -> the art script's Ink subclass

draw_plate(k, w, h) draws the still picture; each part fn(k, w, h, variant) draws one moving thing on its own
transparent page (same coordinates as the plate, so it lands exactly where it would have been drawn).
Variants of a part share one crop box and one ink seed, so swapping them (blink, talk, reactions) changes only
what differs. FACE states: face(variant) sets people.FACE from "+blink" / "+talk" in the variant name.
Output: <name>.png, <name>.json (manifest) and <name>__<part>__<variant>.png in out_dir."""
import json, os
from contextlib import contextmanager
import colorink
from colorink import render_color, render_rgba, grain_rgba
import people

DPI = 300

@contextmanager
def face(variant):
    """people.FACE for a variant name: '+blink' closes the eyes, '+talk' opens the mouth."""
    old = dict(people.FACE); people.FACE.clear()
    if "+blink" in variant: people.FACE["eyes"] = "closed"
    if "+talk" in variant: people.FACE["mouth"] = "open"
    try: yield
    finally: people.FACE.clear(); people.FACE.update(old)

def _plate(args):
    out_dir, name, w, h, fn, make_ink, seed = args
    def draw(c, W, H): fn(make_ink(c, seed), W, H)
    render_color(os.path.join(out_dir, name + ".png"), w / 72, h / 72, draw, seed=seed, dpi=DPI)
    return name

def _part(args):
    out_dir, name, w, h, pname, spec, make_ink, seed = args
    pw, ph = spec.get("page", (w, h)); ims = {}
    for v in spec["variants"]:
        def draw(c, W, H, v=v):
            with face(v): spec["fn"](make_ink(c, seed), W, H, v)
        ims[v] = render_rgba(None, pw / 72, ph / 72, draw, seed=seed, dpi=DPI, grain=False)
    boxes = [im.getchannel("A").getbbox() for im in ims.values()]
    boxes = [b for b in boxes if b]
    if not boxes: raise ValueError(f"{name}/{pname}: nothing drawn")
    pad = 3; W, H = next(iter(ims.values())).size
    box = (max(0, min(b[0] for b in boxes) - pad), max(0, min(b[1] for b in boxes) - pad), min(W, max(b[2] for b in boxes) + pad), min(H, max(b[3] for b in boxes) + pad))
    files = {}
    for v, im in ims.items():
        im = im.crop(box)
        if not colorink.is_bw(): im = grain_rgba(im, seed + 7)
        fn = f"{name}__{pname}__{v.replace('+', '_')}.png"; im.save(os.path.join(out_dir, fn), compress_level=1); files[v] = fn
    return pname, dict(box=list(box), variants=files, page=[pw, ph])

def save_layers(out_dir, jobs, make_ink, procs=8):
    """Render every job's plate and parts in parallel and write the manifests."""
    from concurrent.futures import ProcessPoolExecutor
    os.makedirs(out_dir, exist_ok=True)
    tasks_p, tasks_s = [], []
    for j in jobs:
        tasks_p.append((out_dir, j["name"], j["w"], j["h"], j["plate"], make_ink, j.get("seed", 31)))
        for pn, ps in j.get("parts", {}).items():
            tasks_s.append((out_dir, j["name"], j["w"], j["h"], pn, ps, make_ink, j.get("seed", 31) + 101 + sum(map(ord, pn))))
    res = {j["name"]: {} for j in jobs}
    with ProcessPoolExecutor(procs) as ex:
        futs_p = [ex.submit(_plate, a) for a in tasks_p]
        futs_s = [(a[1], ex.submit(_part, a)) for a in tasks_s]
        for f in futs_p: print("plate", f.result(), flush=True)
        for name, f in futs_s:
            pn, m = f.result(); res[name][pn] = m; print("part", name, pn, flush=True)
    for j in jobs:
        man = dict(name=j["name"], W=round(j["w"] * DPI / 72), H=round(j["h"] * DPI / 72), ppt=DPI / 72, parts=res[j["name"]])
        json.dump(man, open(os.path.join(out_dir, j["name"] + ".json"), "w"), indent=1)
