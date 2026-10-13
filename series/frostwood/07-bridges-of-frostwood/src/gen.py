"""Hashi generator: grow a random connected bridge network on the grid, read off the island
numbers, and keep only puzzles with exactly one solution (SAT) that the logic solver finishes
at the band's tier but not below it."""
import random
from hashi import sat_solutions, solve, Struct, check_solution, check_puzzle

D4 = ((0, 1), (1, 0), (0, -1), (-1, 0))

BANDS = {
    # w, h, island-count range, solvable at tier, must fail at tier, target count
    # trials = how many one-step "what if?" eliminations the logic solver needs (min, max)
    "Easy":   dict(w=7,  h=7,  k=(10, 14), win=3, tier=1, fail=None, trials=(0, 0),  count=40),
    "Medium": dict(w=9,  h=9,  k=(16, 22), win=3, tier=2, fail=1,    trials=(0, 0),  count=40),
    "Hard":   dict(w=11, h=11, k=(22, 30), win=4, tier=3, fail=2,    trials=(1, 3),  count=50),
    "Expert": dict(w=13, h=15, k=(34, 44), win=4, tier=3, fail=2,    trials=(2, 99), count=50),
}


def grow(w, h, k, rnd, p_double=0.45, p_loop=0.35, short=0.8):
    """Random connected network of k islands, no two islands side by side."""
    isl = {}; bridges = {}; occ = set()
    start = (rnd.randrange(h), rnd.randrange(w)); isl[start] = 0
    def near_island(x, skip):
        return any((x[0] + dr, x[1] + dc) in isl and (x[0] + dr, x[1] + dc) != skip for dr, dc in D4)
    fails = 0
    while len(isl) < k and fails < 400:
        a = rnd.choice(list(isl)); dr, dc = rnd.choice(D4)
        path = []; x = (a[0] + dr, a[1] + dc)
        hit = None
        while 0 <= x[0] < h and 0 <= x[1] < w:
            if x in isl: hit = x; break
            if x in occ: break
            path.append(x); x = (x[0] + dr, x[1] + dc)
        key = None
        if hit is not None and len(path) >= 1 and rnd.random() < p_loop:
            key = tuple(sorted((a, hit)))
            if key in bridges: fails += 1; continue
            b = hit; cells = path
        else:
            opts = [i for i in range(1, len(path)) if not near_island(path[i], a if i == 0 else None)]
            if not opts: fails += 1; continue
            i = rnd.choices(opts, weights=[1.0 / (o ** short) for o in opts])[0]; b = path[i]; cells = path[:i]
            if b in occ: fails += 1; continue
            isl[b] = 0; key = tuple(sorted((a, b)))
        m = 2 if rnd.random() < p_double else 1
        bridges[key] = m; occ.update(cells); isl[a] += m; isl[b] += m
    if len(isl) < k: return None
    # islands must not sit on a bridge path, and the network must stay valid
    return isl, bridges


def empty_window(w, h, isl, k):
    """True if some k x k block of the grid holds no island (puzzle would look patchy)."""
    for r in range(h - k + 1):
        for c in range(w - k + 1):
            if not any((r + a, c + b) in isl for a in range(k) for b in range(k)): return True
    return False


def to_puzzle(w, h, isl, bridges):
    keys = sorted(isl); ix = {x: i for i, x in enumerate(keys)}
    p = dict(w=w, h=h, islands=[[r, c, isl[(r, c)]] for r, c in keys],
             bridges=sorted([ix[a], ix[b], m] if ix[a] < ix[b] else [ix[b], ix[a], m] for (a, b), m in bridges.items()))
    return p


def make(args):
    band, seed = args
    B = BANDS[band]; w, h = B["w"], B["h"]; rnd = random.Random(seed)
    for attempt in range(200):
        k = rnd.randint(*B["k"])
        g = grow(w, h, k, rnd, p_double=rnd.uniform(0.3, 0.6), p_loop=rnd.uniform(0.2, 0.5), short=rnd.uniform(0.3, 1.2))
        if not g: continue
        rows = {r for r, c in g[0]}; cols = {c for r, c in g[0]}
        if not {0, h - 1} <= rows or not {0, w - 1} <= cols: continue   # use the whole grid
        if empty_window(w, h, g[0], B["win"]): continue                  # no big empty patches
        p = to_puzzle(w, h, *g)
        if any(n > 8 for _, _, n in p["islands"]): continue
        try:
            check_puzzle(p); check_solution(p)
        except AssertionError:
            continue
        S = Struct(p)
        ok, st = solve(p, B["tier"], return_state=True, S=S)  # cheap filter first
        if not ok: continue
        if B["fail"] is not None and solve(p, B["fail"], S=S): continue
        tr = st.stats.get("trial", 0)
        if not B["trials"][0] <= tr <= B["trials"][1]: continue
        sols = sat_solutions(p, 2)
        if len(sols) != 1 or sols[0] != sorted(tuple(b) for b in p["bridges"]): continue
        p.update(band=band, seed=seed, k=len(p["islands"]),
                 grade=dict(tier=B["tier"], trials=tr, network=st.stats.get("isolate", 0) + st.stats.get("exit", 0),
                            steps=sum(st.stats.values())))
        return p
    return None


if __name__ == "__main__":
    import json, sys, time
    band = sys.argv[1] if len(sys.argv) > 1 else "Easy"
    t = time.time(); ok = 0
    for s in range(int(sys.argv[2]) if len(sys.argv) > 2 else 10):
        r = make((band, s)); ok += bool(r)
    print(band, ok, "ok", round(time.time() - t, 1), "s")
