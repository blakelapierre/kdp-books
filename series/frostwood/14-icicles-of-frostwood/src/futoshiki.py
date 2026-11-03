"""Futoshiki engine used by the generator: a step-by-step logic solver with three tiers, plus a SAT
uniqueness check (CaDiCaL via python-sat).
Puzzle: dict(n, givens=[[r, c, v]], ineq=[[r1, c1, r2, c2]] meaning cell (r1, c1) < cell (r2, c2), sol=[[...]]).
Values are 1..n. Tiers: T1 = singles (naked and hidden) and sign bounds; T2 = + naked pairs/triples and
hidden pairs in a row or column, and sign chains; T3 = + one-step trial (what if?) with T2 inside."""
from satutil import CNF

def units(n):
    return [[(r, c) for c in range(n)] for r in range(n)] + [[(r, c) for r in range(n)] for c in range(n)]

def bits(m):
    out = []; v = 1
    while m:
        if m & 1: out.append(v)
        m >>= 1; v += 1
    return out

def lo(m): return (m & -m).bit_length()
def hi(m): return m.bit_length()
def pc(m): return bin(m).count("1")


class Contra(Exception): pass


class State:
    def __init__(s, p):
        s.n = n = p["n"]; full = (1 << n) - 1
        s.cand = {(r, c): full for r in range(n) for c in range(n)}
        for r, c, v in p["givens"]: s.cand[(r, c)] = 1 << (v - 1)
        s.ineq = [((a, b), (c, d)) for a, b, c, d in p["ineq"]]
        s.U = units(n); s.stats = {}
        s.peers = {x: set() for x in s.cand}
        for u in s.U:
            for x in u: s.peers[x] |= set(u) - {x}
        # sign chains: every cell known to be smaller / larger than x, by following signs
        less = {x: set() for x in s.cand}; more = {x: set() for x in s.cand}
        for a, b in s.ineq: less[b].add(a); more[a].add(b)
        s.less = less; s.more = more
    def copy(s):
        t = State.__new__(State); t.__dict__.update(s.__dict__); t.cand = dict(s.cand); t.stats = {}; return t
    def bump(s, k): s.stats[k] = s.stats.get(k, 0) + 1
    def set_mask(s, x, m, rule):
        if m == s.cand[x]: return False
        if m == 0: raise Contra()
        s.cand[x] = m; s.bump(rule); return True
    def solved(s): return all(pc(m) == 1 for m in s.cand.values())
    def grid(s): return [[lo(s.cand[(r, c)]) for c in range(s.n)] for r in range(s.n)]


def chain_len(s, x, rel, memo):
    """Length of the longest sign chain going down (rel=less) from x, not counting x."""
    if x in memo: return memo[x]
    memo[x] = 0
    best = 0
    for y in rel[x]: best = max(best, 1 + chain_len(s, y, rel, memo))
    memo[x] = best; return best


def step_t1(s):
    ch = False; n = s.n
    for x, m in list(s.cand.items()):
        if pc(m) == 1:
            for y in s.peers[x]:
                if s.cand[y] & m: ch |= s.set_mask(y, s.cand[y] & ~m, "single")
    for u in s.U:
        for v in range(n):
            b = 1 << v; where = [x for x in u if s.cand[x] & b]
            if not where: raise Contra()
            if len(where) == 1 and s.cand[where[0]] != b: ch |= s.set_mask(where[0], b, "hidden")
    for a, b in s.ineq:   # a < b
        ma, mb = s.cand[a], s.cand[b]
        na = ma & ((1 << (hi(mb) - 1)) - 1)          # a < max(b)
        nb = mb & ~((1 << lo(ma)) - 1)               # b > min(a)
        ch |= s.set_mask(a, na, "sign"); ch |= s.set_mask(b, nb, "sign")
    return ch


def step_t2(s):
    ch = False; n = s.n
    from itertools import combinations
    for u in s.U:
        open_ = [x for x in u if pc(s.cand[x]) > 1]
        for k in (2, 3):
            if len(open_) <= k: continue
            for grp in combinations(open_, k):
                m = 0
                for x in grp: m |= s.cand[x]
                if pc(m) == k:
                    for y in open_:
                        if y not in grp and s.cand[y] & m: ch |= s.set_mask(y, s.cand[y] & ~m, "subset")
            # hidden pairs
        if len(open_) > 2:
            vals = [v for v in range(n) if sum(1 for x in open_ if s.cand[x] >> v & 1) == 2]
            for v1, v2 in combinations(vals, 2):
                w1 = {x for x in open_ if s.cand[x] >> v1 & 1}; w2 = {x for x in open_ if s.cand[x] >> v2 & 1}
                if w1 == w2:
                    m = (1 << v1) | (1 << v2)
                    for x in w1: ch |= s.set_mask(x, s.cand[x] & m, "hidden-pair")
    # sign chains: a cell with a chain of k smaller cells below it is at least k+1; with k larger above it, at most n-k
    md, mu = {}, {}
    for x in s.cand:
        dn = chain_len(s, x, s.less, md); up = chain_len(s, x, s.more, mu)
        m = s.cand[x] & ~((1 << dn) - 1) & ((1 << (n - up)) - 1)
        ch |= s.set_mask(x, m, "chain")
    return ch


def propagate(s, tier):
    while True:
        if step_t1(s): continue
        if tier >= 2 and step_t2(s): continue
        return


def solve(p, tier, return_state=False, max_trials=999):
    s = State(p)
    try:
        propagate(s, min(tier, 2))
        if tier >= 3:
            while not s.solved():
                found = False
                for x in sorted(s.cand, key=lambda x: (pc(s.cand[x]), x)):
                    m = s.cand[x]
                    if pc(m) == 1: continue
                    for v in bits(m):
                        t = s.copy(); t.cand[x] = 1 << (v - 1)
                        try: propagate(t, 2); bad = False
                        except Contra: bad = True
                        if bad:
                            s.set_mask(x, m & ~(1 << (v - 1)), "trial"); found = True; break
                    if found: break
                if not found: break
                if s.stats.get("trial", 0) > max_trials: break
                propagate(s, 2)
    except Contra:
        return (False, s) if return_state else False
    ok = s.solved()
    if ok: s.sol = s.grid()
    return (ok, s) if return_state else ok


def need_tier(p):
    for t in (1, 2, 3):
        if solve(p, t): return t
    return None


def check_puzzle(p):
    n = p["n"]
    assert 4 <= n <= 9
    for r, c, v in p["givens"]: assert 0 <= r < n and 0 <= c < n and 1 <= v <= n
    for a, b, c, d in p["ineq"]: assert abs(a - c) + abs(b - d) == 1, "signs sit between neighbours"
    pairs = [frozenset([(a, b), (c, d)]) for a, b, c, d in p["ineq"]]
    assert len(set(pairs)) == len(pairs)


def check_solution(p, sol=None):
    sol = sol or p["sol"]; n = p["n"]
    for r in range(n): assert sorted(sol[r]) == list(range(1, n + 1))
    for c in range(n): assert sorted(sol[r][c] for r in range(n)) == list(range(1, n + 1))
    for r, c, v in p["givens"]: assert sol[r][c] == v
    for a, b, c, d in p["ineq"]: assert sol[a][b] < sol[c][d]


def sat_solutions(p, limit=2):
    n = p["n"]; F = CNF()
    X = lambda r, c, v: F.v("x", r, c, v)
    for r in range(n):
        for c in range(n): F.eq([X(r, c, v) for v in range(1, n + 1)], 1)
    for v in range(1, n + 1):
        for r in range(n): F.eq([X(r, c, v) for c in range(n)], 1)
        for c in range(n): F.eq([X(r, c, v) for r in range(n)], 1)
    for r, c, v in p["givens"]: F.add([X(r, c, v)])
    for a, b, c, d in p["ineq"]:
        for va in range(1, n + 1):
            for vb in range(1, va + 1): F.add([-X(a, b, va), -X(c, d, vb)])
    keys = [("x", r, c, v) for r in range(n) for c in range(n) for v in range(1, n + 1)]
    out = []
    for sol in F.solutions(keys, limit):
        g = [[0] * n for _ in range(n)]
        for _, r, c, v in sol: g[r][c] = v
        out.append(g)
    return out
