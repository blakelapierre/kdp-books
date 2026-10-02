"""Tents puzzle generator: place non-touching tents + adjacent trees, keep only uniquely
solvable puzzles that the logic solver finishes at the band tier and fails at the fail tier."""
import random
from tents import sat_count, solve, check_solution, N4, N8

BANDS = {
    # n, tree-count range, solvable at tier, must fail at fail tier, target count
    "Easy":   dict(n=6,  k=(5, 7),   tier=1, fail=None, count=40),
    "Medium": dict(n=8,  k=(9, 12),  tier=4, fail=1,    count=40),
    "Hard":   dict(n=10, k=(14, 18), tier=4, fail=1,    count=50),
    "Expert": dict(n=12, k=(20, 26), tier=4, fail=1,    count=50),
}


def place_layout(n, k, rnd):
    """Place k tents (no 8-touch) each with exactly one dedicated orthogonally adjacent tree."""
    inb = lambda r, c: 0 <= r < n and 0 <= c < n
    for _outer in range(100):
        tents = set(); trees = []; used = set()
        for _ in range(n * n * 50):
            if len(tents) == k: break
            r, c = rnd.randrange(n), rnd.randrange(n)
            if (r, c) in used: continue
            if any((r + dr, c + dc) in tents for dr, dc in N8): continue
            if any((r + dr, c + dc) in trees for dr, dc in N4): continue
            opts = []
            for dr, dc in N4:
                tr, tc = r + dr, c + dc
                if not inb(tr, tc) or (tr, tc) in used or (tr, tc) in tents: continue
                if any((tr + a, tc + b) in tents for a, b in N4): continue
                opts.append((tr, tc))
            if not opts: continue
            t = rnd.choice(opts)
            tents.add((r, c)); trees.append(t); used |= {(r, c), t}
        if len(tents) != k: continue
        return sorted(tents), sorted(trees)
    return None


def make(args):
    band, seed = args
    B = BANDS[band]; n = B["n"]; rnd = random.Random(seed)
    tries = 250 if band in ("Hard", "Expert") else 150
    for attempt in range(tries):
        k = rnd.randint(*B["k"])
        layout = place_layout(n, k, rnd)
        if not layout: continue
        tents, trees = layout
        rows = [sum(1 for (r, c) in tents if r == i) for i in range(n)]
        cols = [sum(1 for (r, c) in tents if c == i) for i in range(n)]
        zeros = rows.count(0) + cols.count(0)
        if band == "Easy" and zeros < 2: continue
        if band in ("Hard", "Expert") and zeros > n: continue
        p = dict(n=n, trees=trees, rows=rows, cols=cols, tents=tents)
        sols = sat_count(p, 2)
        if len(sols) != 1: continue
        if sols[0] != sorted(tents): continue
        p["band"] = band; p["seed"] = seed; p["k"] = k
        check_solution(p)
        if not solve(p, B["tier"]): continue
        if B["fail"] is not None and solve(p, B["fail"]): continue
        return dict(n=n, k=k, band=band, seed=seed,
                    trees=[list(t) for t in trees],
                    rows=rows, cols=cols,
                    tents=[list(t) for t in tents])
    return None


if __name__ == "__main__":
    import json, sys
    band = sys.argv[1] if len(sys.argv) > 1 else "Easy"
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    r = make((band, seed))
    print(json.dumps(r, indent=2) if r else "FAIL")
