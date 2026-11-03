"""Futoshiki generator: fill a random Latin square, give it every sign between neighbours (plus a few
numbers if needed), then take clues away one at a time, in a seeded random order, as long as the
puzzle stays solvable at the band's logic tier. Keep only puzzles that also fail one tier lower
(where the band says so), whose what-if count is in range, and that SAT finds exactly one solution for."""
import random
from futoshiki import solve, sat_solutions, check_solution, check_puzzle

BANDS = {
    # n, tier needed, must fail at tier, trial range, share of signs kept at most, count
    "Easy":   dict(n=5, tier=1, fail=None, trials=(0, 0),  count=40),
    "Medium": dict(n=6, tier=2, fail=1,    trials=(0, 0),  count=40),
    "Hard":   dict(n=7, tier=3, fail=2,    trials=(1, 3),  count=40),
    "Expert": dict(n=8, tier=3, fail=2,    trials=(4, 12), count=40),
}


def latin(n, rnd):
    g = [[0] * n for _ in range(n)]
    def rec(i):
        if i == n * n: return True
        r, c = divmod(i, n)
        vals = list(range(1, n + 1)); rnd.shuffle(vals)
        for v in vals:
            if v in g[r] or any(g[y][c] == v for y in range(r)): continue
            g[r][c] = v
            if rec(i + 1): return True
        g[r][c] = 0
        return False
    rec(0); return g


def all_signs(g):
    n = len(g); out = []
    for r in range(n):
        for c in range(n):
            for (y, x) in ((r, c + 1), (r + 1, c)):
                if y < n and x < n:
                    out.append([r, c, y, x] if g[r][c] < g[y][x] else [y, x, r, c])
    return out


def ok_at(p, B):
    if B["tier"] < 3: return solve(p, B["tier"])
    ok, st = solve(p, 3, return_state=True, max_trials=B["trials"][1])
    return ok and st.stats.get("trial", 0) <= B["trials"][1]


ATTEMPTS = 6


def make(args):
    band, seed = args
    B = BANDS[band]; n = B["n"]; rnd = random.Random(seed)
    for attempt in range(ATTEMPTS):
        g = latin(n, rnd)
        signs = all_signs(g)
        cells = [(r, c) for r in range(n) for c in range(n)]; rnd.shuffle(cells)
        givens = []
        p = dict(n=n, givens=givens, ineq=signs, sol=g)
        while not ok_at(p, B) and cells:
            r, c = cells.pop(); givens.append([r, c, g[r][c]])
        if not ok_at(p, B): continue
        # take clues away: numbers first (a few kept by chance), then signs
        order = [("g", tuple(x)) for x in givens]; rnd.shuffle(order)
        so = [("s", tuple(x)) for x in signs]; rnd.shuffle(so); order += so
        for kind, x in order:
            if kind == "g":
                q = dict(p, givens=[y for y in p["givens"] if tuple(y) != x])
            else:
                q = dict(p, ineq=[y for y in p["ineq"] if tuple(y) != x])
            if ok_at(q, B): p = q
        p["givens"] = sorted(p["givens"]); p["ineq"] = sorted(p["ineq"])
        try: check_puzzle(p); check_solution(p)
        except AssertionError: continue
        ok, st = solve(p, B["tier"], return_state=True)
        if not ok or st.sol != g: continue
        if B["fail"] is not None and solve(p, B["fail"]): continue
        tr = st.stats.get("trial", 0)
        if not B["trials"][0] <= tr <= B["trials"][1]: continue
        sols = sat_solutions(p, 2)
        if len(sols) != 1 or sols[0] != g: continue
        s2 = st.stats
        p.update(band=band, seed=seed, k=len(p["givens"]) + len(p["ineq"]),
                 grade=dict(tier=B["tier"], trials=tr, t2=s2.get("subset", 0) + s2.get("hidden-pair", 0) + s2.get("chain", 0),
                            steps=sum(s2.values())))
        return p
    return None


if __name__ == "__main__":
    import sys, time
    band = sys.argv[1] if len(sys.argv) > 1 else "Easy"
    t = time.time(); ok = 0; n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    for s in range(n):
        r = make((band, s)); ok += bool(r)
        if r and ok == 1: print(r["sol"], r["givens"], len(r["ineq"]), r["grade"])
    print(band, ok, "/", n, "ok", round(time.time() - t, 1), "s")
