"""Turns a picture subject into a nonogram: rasterise the glyph at the band's grid size under a
few fixed rendering settings, keep the settings whose clues the line solver finishes alone
(no guessing). If none does, flip the fewest pixels (greedy, seeded) until it does.
Deterministic: fixed settings and seeds, no hashing involved."""
import random
import numpy as np
from pics import glyph
from nonogram import picture_clues, solve, grade

SIZE = {"Easy": 15, "Medium": 20, "Hard": 25, "Expert": 25}
MAXFLIP = {10: 2, 15: 2, 20: 3, 25: 5}
# (weight, threshold, pad) settings tried in this order; the first is the house look
VARIANTS = {10: [(700, 0.40, 0.05), (700, 0.30, 0.05)],
            15: [(700, 0.30, 0.04), (700, 0.36, 0.04), (600, 0.30, 0.06), (700, 0.26, 0.06), (700, 0.33, 0.08)],
            20: [(700, 0.40, 0.04), (700, 0.34, 0.04), (600, 0.40, 0.05), (700, 0.46, 0.04), (700, 0.38, 0.07)],
            25: [(700, 0.42, 0.03), (700, 0.36, 0.03), (600, 0.42, 0.04), (700, 0.48, 0.03), (700, 0.40, 0.06)]}


def known(img):
    rows, cols = picture_clues(img.tolist())
    g, st = solve(rows, cols)
    return g, st


def repair(img, maxflip, seed):
    rnd = random.Random(seed); img = img.copy(); flips = []
    for _ in range(maxflip + 1):
        g, st = known(img)
        if st == "solved": return img, flips
        if len(flips) == maxflip: return None, flips
        unk = [(r, c) for r in range(img.shape[0]) for c in range(img.shape[1]) if g[r][c] == -1]
        cand = rnd.sample(unk, min(14, len(unk)))
        best = None
        for (r, c) in cand:
            img[r, c] ^= 1
            g2, st2 = known(img)
            k = sum(v != -1 for row in g2 for v in row) + (10 ** 6 if st2 == "solved" else 0)
            img[r, c] ^= 1
            if best is None or k > best[0]: best = (k, r, c)
        _, r, c = best; img[r, c] ^= 1; flips.append([r, c])
    return None, flips


def make(args):
    """args = (subject index, char, name, size). Returns a puzzle dict or None."""
    idx, ch, name, n = args
    best = None
    for vi, (w, thr, pad) in enumerate(VARIANTS[n]):
        img = glyph(ch, n, "outline", wght=w, thr=thr, pad=pad)
        if img.sum() < n * n * 0.12: continue           # too faint to read as a picture
        if img.sum() > n * n * 0.75: continue
        g, st = known(img)
        if st == "solved":
            best = (0, vi, img, []); break
    if best is None:
        for vi in (0, 1):
            w, thr, pad = VARIANTS[n][vi]
            img = glyph(ch, n, "outline", wght=w, thr=thr, pad=pad)
            fixed, flips = repair(img, MAXFLIP[n], seed=1000 * idx + n + vi)
            if fixed is not None and (best is None or len(flips) < best[0]):
                best = (len(flips), vi, fixed, flips)
    if best is None: return None
    nf, vi, img, flips = best
    pic = img.tolist()
    rows, cols = picture_clues(pic)
    gr = grade(rows, cols)
    assert gr["status"] == "solved"
    return dict(subject=idx, char=ch, name=name, n=n, variant=vi, flips=flips,
                rows=rows, cols=cols, picture=["".join("#" if v else "." for v in r) for r in pic],
                grade=gr)


if __name__ == "__main__":
    import sys, json
    from subjects import SUBJECTS
    i = int(sys.argv[1]); n = int(sys.argv[2])
    r = make((i, SUBJECTS[i][0], SUBJECTS[i][1], n))
    if r: print("\n".join(r["picture"])); print(r["grade"], r["flips"], r["variant"])
    else: print("FAIL")
