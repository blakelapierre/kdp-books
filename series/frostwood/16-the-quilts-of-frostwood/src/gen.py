"""Quilts (Shikaku) generator: a seeded random tiling of the grid into rectangles (patches), one
number placed at a seeded random square of each patch, then the step-by-step logic solver must
finish the puzzle within the band's tier. A puzzle the logic solver finishes has exactly one solution;
verify.py re-checks that with an independent SAT solver and a separate backtracker."""
import random
from shikaku import solve, need_tier, check

BANDS = {
    # n: grid size; amin/amax: patch areas; ones: max 1-square patches; need: required logic tier;
    # whatif: accepted range of what-if steps; tries: clue placements per tiling
    "Easy":   dict(n=7, amin=2, amax=8, ones=1, need=1, whatif=(0, 0), count=20, tries=30, minsteps=2),
    "Medium": dict(n=9, amin=2, amax=10, ones=1, need=2, whatif=(0, 0), count=30, tries=30, minsteps=6),
    "Hard":   dict(n=10, amin=2, amax=14, ones=1, need=2, whatif=(0, 0), count=30, tries=30, minsteps=10),
    "Expert": dict(n=12, amin=2, amax=16, ones=2, need=3, whatif=(1, 12), count=20, tries=30),
}


def tiling(n, B, rnd):
    g = [[None] * n for _ in range(n)]; rects = []; ones = 0
    for r in range(n):
        for c in range(n):
            if g[r][c] is not None: continue
            opts = []
            maxw = 0
            while c + maxw < n and g[r][c + maxw] is None: maxw += 1
            for h in range(1, n - r + 1):
                for w in range(1, maxw + 1):
                    if any(g[r + h - 1][cc] is not None for cc in range(c, c + w)): break
                    a = h * w
                    if B["amin"] <= a <= B["amax"] and not (h == 1 and w > 6) and not (w == 1 and h > 6):
                        opts.append((h, w))
            if not opts:
                if ones >= B["ones"]: return None
                opts = [(1, 1)]; ones += 1
            h, w = rnd.choice(opts)
            for rr in range(r, r + h):
                for cc in range(c, c + w): g[rr][cc] = len(rects)
            rects.append([r, c, h, w])
    return rects, g


def make(args):
    band, seed = args
    B = BANDS[band]; n = B["n"]; rnd = random.Random(seed)
    for attempt in range(40):
        t = tiling(n, B, rnd)
        if not t: continue
        rects, g = t
        for k in range(B["tries"]):
            clues = []
            for (r0, c0, h, w) in rects:
                clues.append([r0 + rnd.randrange(h), c0 + rnd.randrange(w), h * w])
            p = dict(n=n, clues=clues, sol=g, rects=rects)
            if not solve(p, B["need"], cap=B["whatif"][1]): continue
            need = need_tier(p)
            if need != B["need"]: break
            ok, stt, got = solve(p, need, return_state=True)
            assert ok and got == rects, (got, rects)
            if not (B["whatif"][0] <= stt["whatif"] <= B["whatif"][1]): continue
            if stt["t1"] + stt["t2"] < B.get("minsteps", 0): continue
            p.update(band=band, seed=seed, nclues=len(clues), grade=dict(tier=need, whatif=stt["whatif"], steps=stt["t1"] + stt["t2"]))
            check(p)
            return p
    return None


if __name__ == "__main__":
    import sys, time
    band = sys.argv[1] if len(sys.argv) > 1 else "Easy"
    t = time.time(); ok = 0
    for s in range(int(sys.argv[2]) if len(sys.argv) > 2 else 10):
        t1 = time.time(); r = make((band, s)); ok += bool(r)
        print(s, bool(r), r and r["nclues"], r and r["grade"], round(time.time() - t1, 2), flush=True)
    print(band, ok, "ok", round(time.time() - t, 1), "s")
