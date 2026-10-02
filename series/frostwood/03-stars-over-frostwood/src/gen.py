"""Star Battle generator: random star layout -> regions grown around the stars -> regions reshaped
until the backtracking counter finds exactly one solution -> graded with the logic solver (stars.solve)
and kept only if it fits its band (solvable at the band tier, not solvable at the fail tier)."""
import json, random, sys, time
from multiprocessing import Pool
from stars import solve, count

BANDS = {  # grid n, stars per row/col/region k, solvable at tier, must fail at tier
    "Easy":   dict(n=6,  k=1, tier=2, fail=None, count=40),
    "Medium": dict(n=8,  k=1, tier=3, fail=1,    count=40),
    "Hard":   dict(n=10, k=2, tier=3, fail=2,    count=50),
    "Expert": dict(n=10, k=2, tier=4, fail=3,    count=50),
}

def random_solution(n, k, rnd):
    cols = [0] * n; out = []
    def rec(r, prev):
        if r == n: return True
        opts = [c for c in range(n) if cols[c] < k and all(abs(c - p) > 1 for p in prev)]
        # remaining rows must still be able to fill the columns
        combos = []
        if k == 1: combos = [(c,) for c in opts]
        else: combos = [(a, b) for i, a in enumerate(opts) for b in opts[i + 1:] if b - a > 1]
        rnd.shuffle(combos)
        for cb in combos:
            for c in cb: cols[c] += 1
            left = n - r - 1
            if all(k - cols[c] <= (left + 1) // 2 for c in range(n)):
                out.append(cb)
                if rec(r + 1, cb): return True
                out.pop()
            for c in cb: cols[c] -= 1
        return False
    if not rec(0, ()): return None
    return [(r, c) for r, cb in enumerate(out) for c in cb]

def grow(n, seeds, rnd, blocked=()):
    """random region growth from seed cells; returns label grid"""
    lab = [[-1] * n for _ in range(n)]
    front = []
    for i, (r, c) in enumerate(seeds): lab[r][c] = i
    for i, (r, c) in enumerate(seeds): front += [(i, r, c)]
    while front:
        j = rnd.randrange(len(front)); i, r, c = front[j]
        nbrs = [(r + dr, c + dc) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= r + dr < n and 0 <= c + dc < n and lab[r + dr][c + dc] < 0]
        if not nbrs: front[j] = front[-1]; front.pop(); continue
        rr, cc = rnd.choice(nbrs); lab[rr][cc] = i; front.append((i, rr, cc))
    return lab

def connected(n, lab, rid, without=None):
    cells = [(r, c) for r in range(n) for c in range(n) if lab[r][c] == rid and (r, c) != without]
    if not cells: return False
    seen = {cells[0]}; st = [cells[0]]; S = set(cells)
    while st:
        r, c = st.pop()
        for q in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if q in S and q not in seen: seen.add(q); st.append(q)
    return len(seen) == len(S)

def make_regions(n, k, sol, rnd):
    if k == 1: return grow(n, sol, rnd)
    for _ in range(200):
        sub = grow(n, sol, rnd)
        m = len(sol); adj = [set() for _ in range(m)]
        for r in range(n):
            for c in range(n):
                for rr, cc in ((r + 1, c), (r, c + 1)):
                    if rr < n and cc < n and sub[rr][cc] != sub[r][c]:
                        adj[sub[r][c]].add(sub[rr][cc]); adj[sub[rr][cc]].add(sub[r][c])
        # random perfect matching by backtracking
        mate = [-1] * m
        def rec():
            free = [i for i in range(m) if mate[i] < 0]
            if not free: return True
            i = min(free, key=lambda x: sum(1 for y in adj[x] if mate[y] < 0))
            opts = [y for y in adj[i] if mate[y] < 0]; rnd.shuffle(opts)
            for y in opts:
                mate[i], mate[y] = y, i
                if rec(): return True
                mate[i] = mate[y] = -1
            return False
        if not rec(): continue
        ids = {}; lab = [[0] * n for _ in range(n)]
        for i in range(m):
            key = min(i, mate[i]); ids.setdefault(key, len(ids))
        for r in range(n):
            for c in range(n): lab[r][c] = ids[min(sub[r][c], mate[sub[r][c]])]
        return lab
    return None

def make(args):
    band, seed = args
    B = BANDS[band]; n, k = B["n"], B["k"]; rnd = random.Random(seed)
    for attempt in range(60):
        sol = random_solution(n, k, rnd)
        if not sol: continue
        lab = make_regions(n, k, sol, rnd)
        if not lab: continue
        solset = {r * n + c for r, c in sol}
        p = dict(n=n, k=k, regions=lab)
        for step in range(300):
            alts = []
            cnt = count(p, 2, alts)
            if cnt == 1: break
            alt = [x for x in alts if set(x) != solset]
            if not alt: break
            # break the alternative: move one of its extra stars into a neighbouring region
            extra = [x for x in alt[0] if x not in solset]; rnd.shuffle(extra)
            moved = False
            for x in extra:
                r, c = divmod(x, n); a = lab[r][c]
                nb = list({lab[rr][cc] for rr, cc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)) if 0 <= rr < n and 0 <= cc < n and lab[rr][cc] != a})
                rnd.shuffle(nb)
                if nb and connected(n, lab, a, without=(r, c)):
                    lab[r][c] = nb[0]; moved = True; break
            if not moved: break
        if count(p, 2) != 1: continue
        # regions must be connected and hold k solution stars (always true by construction; checked in verify)
        if not solve(p, B["tier"]): continue
        if B["fail"] and solve(p, B["fail"]): continue
        need = next(t for t in (1, 2, 3, 4) if solve(p, t))
        return dict(n=n, k=k, regions=lab, solution=[list(divmod(x, n)) for x in sorted(solset)], band=band, seed=seed, attempt=attempt, tier=need)
    return None

if __name__ == "__main__":
    band = sys.argv[1]; m = int(sys.argv[2]); base = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    t = time.time()
    with Pool(6) as pool: res = pool.map(make, [(band, base + i) for i in range(m)])
    ok = [r for r in res if r]
    print(band, len(ok), "/", m, "in", round(time.time() - t, 1), "s", "tiers", sorted(r["tier"] for r in ok), "attempts", [r["attempt"] for r in ok])
