"""Puzzle generator: random winding track -> row/col counts -> minimal set of given pieces that the
logic solver (tracks.solve) can finish at the band's tier, and cannot finish one tier lower."""
import json, random, sys, time
from multiprocessing import Pool
from tracks import solve, path_pieces

BANDS = {  # name: (n, tier_max, tier_must_fail, fill range, givens range, count)
    "Easy":   dict(n=6,  tier=2, fail=None, fill=(0.42, 0.62), giv=(2, 6),  count=50),
    "Medium": dict(n=8,  tier=3, fail=1,    fill=(0.42, 0.60), giv=(2, 8),  count=50),
    "Hard":   dict(n=10, tier=3, fail=2,    fill=(0.40, 0.58), giv=(2, 10), count=50),
    "Expert": dict(n=12, tier=4, fail=3,    fill=(0.40, 0.56), giv=(2, 12), count=50),
}

def random_path(n, rnd, lo, hi):
    er = rnd.randrange(n); ec = rnd.randrange(n)
    # start: go right along row er to column ec, then down (or up then... keep simple: L shape)
    path = [(er, c) for c in range(ec + 1)] + [(r, ec) for r in range(er + 1, n)]
    if len(path) < 2: return None
    target = rnd.randint(int(lo * n * n), int(hi * n * n))
    inb = lambda r, c: 0 <= r < n and 0 <= c < n
    for it in range(40000):
        used = set(path)
        L = len(path)
        grow = L < target or rnd.random() < 0.35
        i = rnd.randrange(L - 1)
        (r1, c1), (r2, c2) = path[i], path[i + 1]
        if grow:
            # detour: replace a-b by a-a'-b'-b (sidestep perpendicular)
            dr, dc = r2 - r1, c2 - c1
            sr, sc = (dc, dr) if rnd.random() < 0.5 else (-dc, -dr)
            a2, b2 = (r1 + sr, c1 + sc), (r2 + sr, c2 + sc)
            if inb(*a2) and inb(*b2) and a2 not in used and b2 not in used:
                path[i + 1:i + 1] = [a2, b2]
        else:
            # shortcut: a-x-y-b with a,b adjacent -> a-b ; or corner flip a-x-b -> a-y-b
            if i + 3 < L and abs(path[i][0] - path[i + 3][0]) + abs(path[i][1] - path[i + 3][1]) == 1 and L - 2 >= target * 0.8:
                del path[i + 1:i + 3]
            elif i + 2 < L:
                (ra, ca), (rb, cb) = path[i], path[i + 2]
                if ra != rb and ca != cb:
                    x = path[i + 1]; y = (ra, cb) if x == (rb, ca) else (rb, ca)
                    if y not in used: path[i + 1] = y
        if it > 3000 and abs(len(path) - target) <= 1 and rnd.random() < 0.002: break
    if not (lo * n * n <= len(path) <= hi * n * n): return None
    return er, ec, path

def make(args):
    band, seed = args
    B = BANDS[band]; n = B["n"]; rnd = random.Random(seed)
    for attempt in range(400):
        rp = random_path(n, rnd, *B["fill"])
        if not rp: continue
        er, ec, path = rp
        rows = [0] * n; cols = [0] * n
        for r, c in path: rows[r] += 1; cols[c] += 1
        if max(rows) == n and max(cols) == n and rnd.random() < 0.7: continue
        pieces = path_pieces(n, path, er, ec)
        p = dict(n=n, er=er, ec=ec, rows=rows, cols=cols, givens={})
        cells = list(pieces); rnd.shuffle(cells)
        giv = []
        while not solve(dict(p, givens={c: pieces[c] for c in giv}), B["tier"]):
            ok, st = solve(dict(p, givens={c: pieces[c] for c in giv}), B["tier"], return_state=True)
            # add a piece the solver has not pinned down yet
            cand = [c for c in cells if c not in giv]
            giv.append(cand[0]); cells.remove(cand[0]); cells.append(cand[0])
            if len(giv) > B["giv"][1] * 3: break
        # minimise
        order = giv[:]; rnd.shuffle(order)
        for c in order:
            trial = [x for x in giv if x != c]
            if solve(dict(p, givens={x: pieces[x] for x in trial}), B["tier"]): giv = trial
        gd = {c: pieces[c] for c in sorted(giv)}
        q = dict(p, givens=gd)
        if not solve(q, B["tier"]): continue
        if not (B["giv"][0] <= len(giv) <= B["giv"][1]): continue
        if B["fail"] and solve(q, B["fail"]): continue
        q["solution"] = [list(x) for x in path]; q["band"] = band; q["seed"] = seed
        q["givens"] = {str(c): v for c, v in gd.items()}
        return q
    return None

if __name__ == "__main__":
    band = sys.argv[1]; k = int(sys.argv[2]); base = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    t = time.time()
    with Pool(8) as pool:
        res = pool.map(make, [(band, base + i) for i in range(k)])
    res = [r for r in res if r]
    print(band, len(res), "ok in", round(time.time() - t, 1), "s")
    for r in res[:3]: print(len(r["givens"]), len(r["solution"]), r["rows"], r["cols"])
    json.dump(res, open(f"/tmp/gen_{band}_{base}.json", "w"))
