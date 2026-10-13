"""Hashi (Hashiwokakero / Bridges): rules, SAT solution counter and human-style logic solver.

Puzzle format (dicts in data.json):
  w, h      grid width and height (columns, rows)
  islands   [[r, c, n], ...] sorted by (r, c); n = number of bridges touching the island (1..8)
  bridges   [[i, j, k], ...] the stored solution: islands i < j joined by k = 1 or 2 bridges

Rules: bridges run straight along rows or columns between two islands, 1 or 2 per pair,
never cross a bridge or an island, every island has as many bridges as its number,
and all the islands form one connected network."""
from satutil import CNF
from pysat.solvers import Cadical153


# ----------------------------------------------------------------------------- structure
def edges(p):
    """Candidate island pairs. Returns (E, X): E = [(i, j, orient, cells)], X = crossing edge-index pairs."""
    isl = [(r, c) for r, c, _ in p["islands"]]; pos = {x: i for i, x in enumerate(isl)}
    W, H = p["w"], p["h"]; E = []
    for i, (r, c) in enumerate(isl):
        cells = []; cc = c + 1
        while cc < W and (r, cc) not in pos: cells.append((r, cc)); cc += 1
        if cc < W: E.append((i, pos[(r, cc)], "h", cells))
        cells = []; rr = r + 1
        while rr < H and (rr, c) not in pos: cells.append((rr, c)); rr += 1
        if rr < H: E.append((i, pos[(rr, c)], "v", cells))
    X = []
    hcell = {}
    for k, e in enumerate(E):
        if e[2] == "h":
            for x in e[3]: hcell[x] = k
    for k, e in enumerate(E):
        if e[2] == "v":
            for x in e[3]:
                if x in hcell: X.append((hcell[x], k))
    return E, X


def check_puzzle(p):
    W, H = p["w"], p["h"]; isl = p["islands"]
    keys = [(r, c) for r, c, _ in isl]
    assert keys == sorted(keys) and len(set(keys)) == len(keys)
    assert all(0 <= r < H and 0 <= c < W and 1 <= n <= 8 for r, c, n in isl)
    assert sum(n for _, _, n in isl) % 2 == 0
    assert len(isl) >= 2


def check_solution(p, bridges=None):
    """Stored solution obeys every rule (independent of the solvers)."""
    isl = [(r, c) for r, c, _ in p["islands"]]; N = len(isl)
    br = p["bridges"] if bridges is None else bridges
    deg = [0] * N; occ = {}; adj = {i: set() for i in range(N)}; seen = set()
    island_cells = set(isl)
    for i, j, k in br:
        assert 0 <= i < j < N and k in (1, 2) and (i, j) not in seen; seen.add((i, j))
        (r1, c1), (r2, c2) = isl[i], isl[j]
        assert r1 == r2 or c1 == c2
        if r1 == r2: cells = [(r1, c) for c in range(min(c1, c2) + 1, max(c1, c2))]; o = "h"
        else: cells = [(r, c1) for r in range(min(r1, r2) + 1, max(r1, r2))]; o = "v"
        for x in cells:
            assert x not in island_cells, "bridge passes through an island"
            assert x not in occ, "bridges cross or overlap"
            occ[x] = o
        deg[i] += k; deg[j] += k; adj[i].add(j); adj[j].add(i)
    assert deg == [n for _, _, n in p["islands"]], "island numbers"
    st = [0]; vis = {0}
    while st:
        u = st.pop()
        for v in adj[u]:
            if v not in vis: vis.add(v); st.append(v)
    assert len(vis) == N, "not connected"
    return True


def sol_key(p, bridges):
    return tuple(sorted((i, j, k) for i, j, k in bridges))


# ----------------------------------------------------------------------------- SAT counter
def sat_solutions(p, limit=2):
    """Up to `limit` connected solutions, via CaDiCaL with lazily added connectivity cuts."""
    E, X = edges(p); N = len(p["islands"])
    f = CNF(); A = lambda e: f.v("a", e); B = lambda e: f.v("b", e)
    inc = [[] for _ in range(N)]
    for k, (i, j, _, _) in enumerate(E):
        A(k); B(k); inc[i].append(k); inc[j].append(k); f.add([-B(k), A(k)])
    for i, (_, _, n) in enumerate(p["islands"]):
        lits = [A(k) for k in inc[i]] + [B(k) for k in inc[i]]
        if len(lits) < n: return []
        f.eq(lits, n)
    for e, g in X: f.add([-A(e), -A(g)])
    sols = []; cuts = 0
    with Cadical153(bootstrap_with=f.cls) as S:
        while len(sols) < limit and S.solve():
            m = set(l for l in S.get_model() if l > 0)
            val = [(A(k) in m) + (B(k) in m) for k in range(len(E))]
            comp = list(range(N))
            def find(x):
                while comp[x] != x: comp[x] = comp[comp[x]]; x = comp[x]
                return x
            for k, (i, j, _, _) in enumerate(E):
                if val[k]: comp[find(i)] = find(j)
            roots = {find(i) for i in range(N)}
            if len(roots) > 1:
                bad = False
                for rt in roots:
                    cut = [A(k) for k, (i, j, _, _) in enumerate(E) if (find(i) == rt) != (find(j) == rt)]
                    if not cut: bad = True; break
                    S.add_clause(cut); cuts += 1
                if bad: break
                continue
            sols.append(sorted((E[k][0], E[k][1], val[k]) for k in range(len(E)) if val[k]))
            S.add_clause([-(A(k)) if A(k) in m else A(k) for k in range(len(E))] +
                         [-(B(k)) if B(k) in m else B(k) for k in range(len(E))])
    return sols


# ----------------------------------------------------------------------------- logic solver
class Contradiction(Exception):
    pass


LO = {1: 0, 2: 1, 3: 0, 4: 2, 5: 0, 6: 1, 7: 0}   # min value in a {0,1,2} bitmask
HI = {1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 2}
TIERS = {1: "island counting + crossings", 2: "+ network (isolation) rules", 3: "+ one-step trial (what if?)"}


class Struct:
    def __init__(s, p):
        s.E, X = edges(p); s.N = len(p["islands"]); s.need = [n for _, _, n in p["islands"]]
        s.inc = [[] for _ in range(s.N)]; s.cross = [[] for _ in s.E]
        for k, (i, j, _, _) in enumerate(s.E): s.inc[i].append(k); s.inc[j].append(k)
        for e, g in X: s.cross[e].append(g); s.cross[g].append(e)


class State:
    def __init__(s, st, dom=None):
        s.S = st; s.dom = dom[:] if dom is not None else [7] * len(st.E); s.stats = {}

    def copy(s):
        t = State(s.S, s.dom); t.stats = dict(s.stats); return t

    def restrict(s, e, mask, tag):
        d = s.dom[e]; nd = d & mask
        if nd == d: return False
        if nd == 0: raise Contradiction
        s.dom[e] = nd; s.stats[tag] = s.stats.get(tag, 0) + 1; return True

    def solved(s): return all(d in (1, 2, 4) for d in s.dom)

    def solution(s):
        return sorted((s.S.E[k][0], s.S.E[k][1], LO[d]) for k, d in enumerate(s.dom) if LO[d] > 0)


def rng(lo, hi): return sum(1 << v for v in range(max(lo, 0), min(hi, 2) + 1))


def basic(st):
    """T1: per-island min/max bridge counting and crossing exclusion, to a fixpoint."""
    S = st.S; any_ch = False
    while True:
        ch = False
        for e in range(len(S.E)):
            if LO[st.dom[e]] >= 1:
                for g in S.cross[e]: ch |= st.restrict(g, 1, "cross")
        for i in range(S.N):
            ks = S.inc[i]; n = S.need[i]
            L = sum(LO[st.dom[k]] for k in ks); Hs = sum(HI[st.dom[k]] for k in ks)
            if L > n or Hs < n: raise Contradiction
            for k in ks:
                lo = n - (Hs - HI[st.dom[k]]); hi = n - (L - LO[st.dom[k]])
                ch |= st.restrict(k, rng(lo, hi), "count")
        if not ch: return any_ch
        any_ch = True


def network(st):
    """T2: connectivity. A finished group of islands may not be cut off from the rest;
    a group with a single way out must use it."""
    S = st.S; N = S.N; par = list(range(N))
    def find(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for k, (i, j, _, _) in enumerate(S.E):
        if LO[st.dom[k]] >= 1: par[find(i)] = find(j)
    rem = {}; size = {}
    for i in range(N):
        r = find(i); size[r] = size.get(r, 0) + 1
        rem[r] = rem.get(r, 0) + S.need[i] - sum(LO[st.dom[k]] for k in S.inc[i])
    if len(size) == 1: return False
    ch = False
    exits = {r: [] for r in size}
    for k, (i, j, _, _) in enumerate(S.E):
        a, b = find(i), find(j)
        if a != b and HI[st.dom[k]] >= 1: exits[a].append(k); exits[b].append(k)
    for r in size:
        if not exits[r] or rem[r] == 0: raise Contradiction
    for r in size:
        if len(exits[r]) == 1: ch |= st.restrict(exits[r][0], 6, "exit")
    if ch: return True
    for k, (i, j, _, _) in enumerate(S.E):
        d = st.dom[k]
        if d in (1, 2, 4): continue
        a, b = find(i), find(j); lo = LO[d]
        tot = rem[a] + (rem[b] if a != b else 0); sz = size[a] + (size[b] if a != b else 0)
        if sz >= N: continue
        for v in (1, 2):
            if d >> v & 1 and v > lo and tot - 2 * (v - lo) == 0:
                ch |= st.restrict(k, 7 & ~(1 << v), "isolate")
    return ch


def prop(st, tier):
    while True:
        basic(st)
        if tier < 2 or not network(st): return st.solved()


def trial(st):
    """T3: one-step what-if. Returns True if some value was ruled out."""
    for k in range(len(st.dom)):
        d = st.dom[k]
        if d in (1, 2, 4): continue
        for v in (0, 1, 2):
            if not d >> v & 1: continue
            t = st.copy(); t.dom[k] = 1 << v
            try:
                prop(t, 2)
            except Contradiction:
                st.restrict(k, 7 & ~(1 << v), "trial"); return True
    return False


def solve(p, tier=3, return_state=False, S=None):
    st = State(S or Struct(p)); ok = False
    try:
        while True:
            if prop(st, min(tier, 2)): ok = True; break
            if tier < 3 or not trial(st): break
    except Contradiction:
        ok = False
    if ok:
        try: check_solution(p, st.solution())
        except AssertionError: ok = False
    return (ok, st) if return_state else ok


def need_tier(p):
    S = Struct(p)
    for t in (1, 2, 3):
        if solve(p, t, S=S): return t
    return None
