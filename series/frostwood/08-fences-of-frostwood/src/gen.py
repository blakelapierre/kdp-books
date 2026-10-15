"""Slitherlink generator: grow a random hole-free region of cells, take its boundary as the
fence loop, write every clue, then remove clues one at a time (in a seeded random order) while
the step-by-step logic solver can still finish the puzzle within the band's rules. A puzzle the
logic solver finishes has exactly one solution; verify.py re-checks that with an independent SAT
solver."""
import random
from slither import Geo, region_edges, clues_from, is_single_loop, solve, check

D4 = ((0, 1), (1, 0), (0, -1), (-1, 0))

BANDS = {
    # w, h, max logic tier allowed while removing clues, max long what-ifs while removing,
    # need: required tier; short/long: accepted ranges of what-if counts in the final puzzle
    "Easy":   dict(w=6,  h=6,  tier=1, cap=0,  need=1, short=(0, 0),  long=(0, 0),  fill=(0.42, 0.58), count=20),
    "Medium": dict(w=7,  h=7,  tier=2, cap=0,  need=2, short=(1, 99), long=(0, 0),  fill=(0.42, 0.58), count=30),
    "Hard":   dict(w=8,  h=8,  tier=3, cap=3,  need=3, short=(0, 99), long=(1, 3),  fill=(0.42, 0.58), count=30),
    "Expert": dict(w=10, h=10, tier=3, cap=12, need=3, short=(0, 99), long=(3, 12), fill=(0.42, 0.58), count=20),
}


def grow_region(w, h, rnd, frac):
    g = Geo(w, h); target = int(round(frac * w * h))
    R = {(rnd.randrange(h), rnd.randrange(w))}
    tries = 0
    while len(R) < target and tries < 4000:
        tries += 1
        front = [(r + dr, c + dc) for (r, c) in R for dr, dc in D4
                 if 0 <= r + dr < h and 0 <= c + dc < w and (r + dr, c + dc) not in R]
        if not front: break
        # prefer cells touching the region on one side only: long, wiggly fences
        wts = []
        for (r, c) in front:
            k = sum((r + dr, c + dc) in R for dr, dc in D4)
            wts.append(1.0 if k == 1 else 0.25 if k == 2 else 0.08)
        x = rnd.choices(front, weights=wts)[0]
        R2 = R | {x}
        if is_single_loop(g, region_edges(g, R2)): R = R2
    return R if len(R) >= target else None


def make(args):
    band, seed = args
    B = BANDS[band]; w, h = B["w"], B["h"]; g = Geo(w, h); rnd = random.Random(seed)
    for attempt in range(30):
        R = grow_region(w, h, rnd, rnd.uniform(*B["fill"]))
        if not R: continue
        rows = {r for r, c in R}; cols = {c for r, c in R}
        if max(rows) - min(rows) < h - 2 or max(cols) - min(cols) < w - 2: continue   # fence spans the map
        loop = region_edges(g, R)
        full = clues_from(g, loop)
        clues = [row[:] for row in full]
        p = dict(w=w, h=h, clues=clues)
        cells = [(r, c) for r in range(h) for c in range(w)]; rnd.shuffle(cells)
        for (r, c) in cells:
            keep = clues[r][c]; clues[r][c] = None
            if solve(p, 1): continue
            if B["tier"] >= 2:
                ok, stt, _ = solve(p, B["tier"], return_state=True)
                if ok and stt["long"] <= B["cap"]: continue
            clues[r][c] = keep
        need = 1 if solve(p, 1) else 2 if solve(p, 2) else 3
        if need != B["need"]: continue
        ok, stt, st = solve(p, need, return_state=True)
        assert ok
        if not (B["short"][0] <= stt["short"] <= B["short"][1] and B["long"][0] <= stt["long"] <= B["long"][1]): continue
        sol = sorted(e for e in range(g.ne) if st.e[e] == 1)
        assert set(sol) == loop
        p.update(loop=sol, band=band, seed=seed, nclues=sum(n is not None for row in clues for n in row),
                 loop_len=len(sol), grade=dict(tier=need, short=stt["short"], long=stt["long"]))
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
