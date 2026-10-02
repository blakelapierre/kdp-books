"""Star Battle logic solver (used by the generator and for grading).
Puzzle: dict(n, k, regions) where regions is a list of n lists of region ids 0..n-1.
Rules: k stars in every row, every column and every region; no two stars touch, not even diagonally.

solve(p, tier) applies human-style rules up to `tier` and returns True if that fully solves the puzzle:
  T1  singles: a star clears its 8 neighbours and, once a row/column/region is full, the rest of it;
      a unit with exactly as many open squares as stars still needed gets stars in all of them.
  T2  + one-unit reasoning: list the ways a single row/column/region can still hold its stars
      (non-touching); squares used by every way are stars, squares used by none are empty,
      squares touched by every way are empty; + single-unit confinement (a region squeezed into
      one row/column claims that row/column, and vice versa).
  T3  + multi-unit confinement: j regions squeezed into j rows (or columns), and the reverse, j = 2..4.
  T4  + one-step trial: suppose a square is a star, apply T3; if a rule breaks, the square is empty.
count(p, limit) is a plain backtracking solution counter (generator side only)."""
from itertools import combinations

class Contradiction(Exception): pass

class Geo:
    _cache = {}
    def __new__(cls, n, regions):
        key = (n, tuple(map(tuple, regions)))
        if key in cls._cache: return cls._cache[key]
        g = super().__new__(cls); cls._cache[key] = g
        if len(cls._cache) > 4000: cls._cache.clear(); cls._cache[key] = g
        g.n = n; N = n * n
        g.rows = [[r * n + c for c in range(n)] for r in range(n)]
        g.cols = [[r * n + c for r in range(n)] for c in range(n)]
        g.regs = [[] for _ in range(n)]
        for r in range(n):
            for c in range(n): g.regs[regions[r][c]].append(r * n + c)
        g.units = g.rows + g.cols + g.regs            # 0..n-1 rows, n..2n-1 cols, 2n..3n-1 regions
        g.of = [[] for _ in range(N)]
        for ui, u in enumerate(g.units):
            for x in u: g.of[x].append(ui)
        g.nb = []
        for x in range(N):
            r, c = divmod(x, n)
            g.nb.append([rr * n + cc for rr in range(r - 1, r + 2) for cc in range(c - 1, c + 2)
                         if (rr, cc) != (r, c) and 0 <= rr < n and 0 <= cc < n])
        g.nbs = [set(v) for v in g.nb]
        return g

class State:
    def __init__(s, g, k, v=None):
        s.g = g; s.k = k; s.v = list(v) if v else [0] * (g.n * g.n)   # 0 unknown, 1 star, -1 empty
        s.stats = {}
    def copy(s):
        t = State(s.g, s.k, s.v); return t
    def star(s, x, tag="single"):
        if s.v[x] == 1: return False
        if s.v[x] == -1: raise Contradiction
        s.v[x] = 1; s.stats[tag] = s.stats.get(tag, 0) + 1
        for y in s.g.nb[x]:
            if s.v[y] == 1: raise Contradiction
            s.v[y] = -1
        return True
    def empty(s, x, tag="single"):
        if s.v[x] == -1: return False
        if s.v[x] == 1: raise Contradiction
        s.v[x] = -1; s.stats[tag] = s.stats.get(tag, 0) + 1
        return True
    def need(s, u): return s.k - sum(1 for x in s.g.units[u] if s.v[x] == 1)
    def cand(s, u): return [x for x in s.g.units[u] if s.v[x] == 0]
    def done(s): return all(x != 0 for x in s.v)

def rule_singles(st):
    ch = False
    for u in range(len(st.g.units)):
        nd = st.need(u); cd = st.cand(u)
        if nd < 0 or len(cd) < nd: raise Contradiction
        if nd == 0:
            for x in cd: ch |= st.empty(x)
        elif len(cd) == nd:
            for x in cd: ch |= st.star(x)
    return ch

def placements(st, cells, nd, limit=4000):
    """all ways to put nd mutually non-touching stars on cells"""
    out = []; nbs = st.g.nbs
    def rec(i, chosen):
        if len(out) > limit: return
        if len(chosen) == nd: out.append(tuple(chosen)); return
        for j in range(i, len(cells)):
            x = cells[j]
            if all(y not in nbs[x] for y in chosen):
                chosen.append(x); rec(j + 1, chosen); chosen.pop()
    rec(0, []); return out

def rule_unit(st):
    ch = False; g = st.g
    for u in range(len(g.units)):
        nd = st.need(u); cd = st.cand(u)
        if nd <= 0: continue
        pl = placements(st, cd, nd)
        if not pl: raise Contradiction
        if len(pl) > 4000: continue
        inall = set(pl[0]).intersection(*pl[1:])
        inany = set().union(*pl)
        for x in cd:
            if x in inall: ch |= st.star(x, "unit")
            elif x not in inany: ch |= st.empty(x, "unit")
        # squares (outside the unit) touched by every placement
        touch = None
        for P in pl:
            t = set()
            for x in P: t |= g.nbs[x]
            touch = t if touch is None else touch & t
            if not touch: break
        for y in (touch or ()):
            if st.v[y] == 0 and y not in inany: ch |= st.empty(y, "unit")
        if ch: return True
    return ch

def rule_confine(st, jmax):
    g = st.g; n = g.n; ch = False
    groups = [(range(2 * n, 3 * n), range(0, n)), (range(2 * n, 3 * n), range(n, 2 * n)),
              (range(0, n), range(2 * n, 3 * n)), (range(n, 2 * n), range(2 * n, 3 * n)),
              (range(0, n), range(n, 2 * n)), (range(n, 2 * n), range(0, n))]
    for A, B in groups:
        live = [u for u in A if st.need(u) > 0]
        cands = {u: set(st.cand(u)) for u in live}
        for j in range(1, jmax + 1):
            if j > len(live) // 2 + 1: break
            for S in combinations(live, j):
                U = set().union(*(cands[u] for u in S))
                T = {b for x in U for b in g.of[x] if b in B}
                if len(T) > j: continue
                nS = sum(st.need(u) for u in S); nT = sum(st.need(b) for b in T)
                if nT < nS: raise Contradiction
                if nT == nS:
                    for b in T:
                        for x in st.cand(b):
                            if x not in U: ch |= st.empty(x, f"confine{j}")
                    if ch: return True
    return ch

def propagate(st, tier):
    while True:
        if rule_singles(st): continue
        if tier >= 2 and rule_unit(st): continue
        if tier >= 2 and rule_confine(st, 1): continue
        if tier >= 3 and rule_confine(st, 4): continue
        if tier >= 4 and trial(st): continue
        break
    # final validity
    for u in range(len(st.g.units)):
        if st.need(u) < 0: raise Contradiction
    return st

def trial(st):
    for x in range(len(st.v)):
        if st.v[x] != 0: continue
        t = st.copy()
        try:
            t.star(x); propagate(t, 3)
        except Contradiction:
            st.empty(x, "trial"); return True
    return False

def solve(p, tier, return_state=False):
    g = Geo(p["n"], p["regions"]); st = State(g, p["k"])
    try:
        propagate(st, tier); ok = st.done()
    except Contradiction:
        ok = False
    return (ok, st) if return_state else ok

def count(p, limit=2, sols=None):
    """Backtracking counter with T1 propagation; returns number of solutions (capped at limit)."""
    g = Geo(p["n"], p["regions"]); found = []
    def rec(st):
        if len(found) >= limit: return
        try: propagate(st, 1)
        except Contradiction: return
        if st.done(): found.append([i for i, v in enumerate(st.v) if v == 1]); return
        best = None
        for u in range(len(g.units)):
            nd = st.need(u)
            if nd > 0:
                cd = st.cand(u)
                if best is None or len(cd) < len(best): best = cd
        x = best[0]
        t = st.copy(); t.star(x) if True else None
        rec(t)
        t = st.copy()
        try: t.empty(x)
        except Contradiction: return
        rec(t)
    rec(State(g, p["k"]))
    if sols is not None: sols.extend(found)
    return len(found)
