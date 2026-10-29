"""Nurikabe core: rule checker, SAT counter (CaDiCaL via python-sat, lazy connectivity cuts) and a
step-by-step logic solver with three tiers used to grade difficulty.

Book wording: shaded cells are the shovelled PATH (must be one connected path, never a 2x2 square of path),
unshaded cells are SNOW PATCHES (each holds exactly one number, and has exactly that many squares).

Puzzle dict: w, h, clues=[[r, c, n], ...], sol=["#..#", ...] ('#' = path / shaded, '.' = snow / unshaded).
Tiers: T1 = basic rules (finished patches, cells between two patches, out-of-reach cells, 2x2 rule,
only-one-way-out for patches and for the path); T2 = + listing every way a small patch can finish,
and cells the path cannot do without; T3 = + one-step trial ("what if?") using T2 to find the clash."""
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool

UNK, BLK, WHT = -1, 0, 1


class Contradiction(Exception):
    pass


class Grid:
    def __init__(s, p):
        s.w, s.h = w, h = p["w"], p["h"]; s.N = N = w * h
        s.nb = [[] for _ in range(N)]
        for r in range(h):
            for c in range(w):
                i = r * w + c
                if r > 0: s.nb[i].append(i - w)
                if r < h - 1: s.nb[i].append(i + w)
                if c > 0: s.nb[i].append(i - 1)
                if c < w - 1: s.nb[i].append(i + 1)
        s.clue = {r * w + c: n for r, c, n in p["clues"]}
        s.white_total = sum(s.clue.values()); s.black_total = N - s.white_total
        s.blocks = [(r * w + c, r * w + c + 1, (r + 1) * w + c, (r + 1) * w + c + 1) for r in range(h - 1) for c in range(w - 1)]
        s.blocks_of = [[] for _ in range(N)]
        for b in s.blocks:
            for i in b: s.blocks_of[i].append(b)


# ----------------------------------------------------------------------------- rule checker
def check_puzzle(p):
    w, h = p["w"], p["h"]; seen = set()
    for r, c, n in p["clues"]:
        assert 0 <= r < h and 0 <= c < w and n >= 1 and (r, c) not in seen
        seen.add((r, c))
    assert sum(n for _, _, n in p["clues"]) < w * h


def check_solution(p, sol=None):
    """Asserts that sol (default: the stored one) obeys every rule."""
    sol = sol or p["sol"]; w, h = p["w"], p["h"]
    assert len(sol) == h and all(len(row) == w for row in sol)
    blk = {(r, c) for r in range(h) for c in range(w) if sol[r][c] == "#"}
    for r, c, n in p["clues"]: assert (r, c) not in blk
    for r in range(h - 1):
        for c in range(w - 1):
            assert not {(r, c), (r + 1, c), (r, c + 1), (r + 1, c + 1)} <= blk, "2x2 of path"
    def comps(cells):
        cells = set(cells); out = []
        while cells:
            st = [cells.pop()]; cp = set(st)
            while st:
                r, c = st.pop()
                for x in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if x in cells: cells.discard(x); cp.add(x); st.append(x)
            out.append(cp)
        return out
    assert len(comps(blk)) == 1, "path not connected"
    clue = {(r, c): n for r, c, n in p["clues"]}
    wh = [(r, c) for r in range(h) for c in range(w) if (r, c) not in blk]
    for cp in comps(wh):
        cl = [x for x in cp if x in clue]
        assert len(cl) == 1, "patch without exactly one number"
        assert clue[cl[0]] == len(cp), "patch size"
    return True


# ----------------------------------------------------------------------------- SAT counter
def sat_solutions(p, limit=2):
    """Up to `limit` distinct solutions as lists of row strings. Independent of the logic solver."""
    G = Grid(p); w, N = G.w, G.N; pool = IDPool(); cls = []
    B = [pool.id(("B", i)) for i in range(N)]
    clues = sorted(G.clue.items())
    X = {}
    for k, (ci, n) in enumerate(clues):
        cr, cc = divmod(ci, w)
        for i in range(N):
            r, c = divmod(i, w)
            if abs(r - cr) + abs(c - cc) < n: X[k, i] = pool.id(("X", k, i))
    for i in range(N):
        mine = [X[k, i] for k in range(len(clues)) if (k, i) in X]
        cls.append([B[i]] + mine)                      # white -> in some island
        for x in mine: cls.append([-B[i], -x])         # black -> in none
        cls += CardEnc.atmost(mine, 1, vpool=pool, encoding=EncType.pairwise).clauses if len(mine) > 1 else []
    for k, (ci, n) in enumerate(clues):
        cls.append([X[k, ci]])
        lits = [v for (kk, i), v in X.items() if kk == k]
        cls += CardEnc.equals(lits, bound=n, vpool=pool, encoding=EncType.seqcounter).clauses
    for i in range(N):
        for j in G.nb[i]:
            for k in range(len(clues)):
                if (k, i) in X:   # i in island k and j white -> j in island k
                    cls.append([-X[k, i], B[j]] + ([X[k, j]] if (k, j) in X else []))
    for b in G.blocks: cls.append([-B[i] for i in b])
    out = []
    with Cadical153(bootstrap_with=cls) as S:
        while len(out) < limit:
            if not S.solve(): break
            m = set(l for l in S.get_model() if l > 0)
            blk = [B[i] in m for i in range(N)]
            cut = False
            # path connectivity
            bc = comps_of(G, [i for i in range(N) if blk[i]])
            if len(bc) > 1:
                for cp in bc:
                    bd = {j for i in cp for j in G.nb[i] if j not in cp}
                    S.add_clause([-B[i] for i in cp] + [B[j] for j in bd]); cut = True
            # island connectivity
            for k, (ci, n) in enumerate(clues):
                cells = [i for i in range(N) if (k, i) in X and X[k, i] in m]
                for cp in comps_of(G, cells):
                    if ci in cp: continue
                    bd = {j for i in cp for j in G.nb[i] if j not in cp}
                    S.add_clause([-X[k, i] for i in cp] + [X[k, j] for j in bd if (k, j) in X]); cut = True
            if cut: continue
            sol = ["".join("#" if blk[r * w + c] else "." for c in range(w)) for r in range(G.h)]
            out.append(sol)
            S.add_clause([-B[i] if blk[i] else B[i] for i in range(N)])
    return out


def comps_of(G, cells):
    cells = set(cells); out = []
    while cells:
        st = [cells.pop()]; cp = set(st)
        while st:
            i = st.pop()
            for j in G.nb[i]:
                if j in cells: cells.discard(j); cp.add(j); st.append(j)
        out.append(cp)
    return out


# ----------------------------------------------------------------------------- logic solver
class State:
    def __init__(s, G, v=None):
        s.G = G
        if v is None:
            v = [UNK] * G.N
            for i in G.clue: v[i] = WHT
        s.v = v
        s.stats = {}; s.trace = None

    def copy(s):
        t = State(s.G, list(s.v)); return t

    def set(s, i, val, rule):
        if s.v[i] == val: return False
        if s.v[i] != UNK: raise Contradiction(rule)
        s.v[i] = val; s.stats[rule] = s.stats.get(rule, 0) + 1
        if s.trace is not None: s.trace.append((rule, divmod(i, s.G.w), "path" if val == BLK else "snow"))
        return True

    def analyse(s):
        """White and black components with their facts. Raises Contradiction on a broken rule."""
        G = s.G; v = s.v; N = G.N
        comp = [-1] * N; W = []
        for i in range(N):
            if v[i] == WHT and comp[i] < 0:
                cid = len(W); st = [i]; comp[i] = cid; cells = [i]
                while st:
                    a = st.pop()
                    for b in G.nb[a]:
                        if v[b] == WHT and comp[b] < 0: comp[b] = cid; st.append(b); cells.append(b)
                cl = [x for x in cells if x in G.clue]
                if len(cl) > 1: raise Contradiction("two numbers in one patch")
                n = G.clue[cl[0]] if cl else None
                if n is not None and len(cells) > n: raise Contradiction("patch too big")
                unk = {b for a in cells for b in G.nb[a] if v[b] == UNK}
                if not unk:
                    if n is None or len(cells) != n: raise Contradiction("closed patch")
                W.append(dict(cells=cells, n=n, unk=unk))
        bcomp = [-1] * N; Bc = []
        for i in range(N):
            if v[i] == BLK and bcomp[i] < 0:
                cid = len(Bc); st = [i]; bcomp[i] = cid; cells = [i]
                while st:
                    a = st.pop()
                    for b in G.nb[a]:
                        if v[b] == BLK and bcomp[b] < 0: bcomp[b] = cid; st.append(b); cells.append(b)
                unk = {b for a in cells for b in G.nb[a] if v[b] == UNK}
                Bc.append(dict(cells=cells, unk=unk))
        nb_ = sum(1 for x in v if x == BLK); nw = sum(1 for x in v if x == WHT)
        if nb_ > G.black_total or nw > G.white_total: raise Contradiction("counts")
        if len(Bc) > 1 and any(not c["unk"] for c in Bc): raise Contradiction("path cut off")
        for b in G.blocks:
            if all(v[i] == BLK for i in b): raise Contradiction("2x2 path")
        s.comp, s.W, s.bcomp, s.Bc, s.nblack, s.nwhite = comp, W, bcomp, Bc, nb_, nw

    # --- T1 rules -------------------------------------------------------------
    def reach(s, skip=()):
        """Cells some numbered patch could still reach (shortest path within its remaining size,
        never next to another numbered patch). Returns the reachable set; unreachable unknowns are path."""
        G = s.G; v = s.v; comp = s.comp; W = s.W
        clued = [k for k, c in enumerate(W) if c["n"] is not None]
        reach = set(); s.by = {}
        for k in clued:
            if k in skip: continue
            c = W[k]; rem = c["n"] - len(c["cells"])
            reach.update(c["cells"]); s.by[k] = set(c["cells"])
            if rem == 0: continue
            dist = {x: 0 for x in c["cells"]}; frontier = list(c["cells"]); d = 0
            while frontier and d < rem:
                d += 1; nxt = []
                for a in frontier:
                    for b in G.nb[a]:
                        if b in dist or v[b] == BLK: continue
                        if v[b] == WHT and W[comp[b]]["n"] is not None: continue
                        if any(v[x] == WHT and comp[x] != k and W[comp[x]]["n"] is not None for x in G.nb[b]): continue
                        dist[b] = d; nxt.append(b)
                frontier = nxt
            reach.update(dist); s.by[k] = set(dist)
        return reach

    def t1(s):
        G = s.G; v = s.v; ch = False
        s.analyse(); W = s.W; comp = s.comp
        # all white placed / all black placed
        if s.nwhite == G.white_total:
            for i in range(G.N):
                if v[i] == UNK: ch |= s.set(i, BLK, "count")
            if ch: return True
        if s.nblack == G.black_total:
            for i in range(G.N):
                if v[i] == UNK: ch |= s.set(i, WHT, "count")
            if ch: return True
        # finished patches are walled in
        for c in W:
            if c["n"] is not None and len(c["cells"]) == c["n"]:
                for b in c["unk"]: ch |= s.set(b, BLK, "finished")
        if ch: return True
        # a cell touching two numbered patches (or a numbered patch that would overflow) is path
        for i in range(G.N):
            if v[i] != UNK: continue
            ks = {comp[b] for b in G.nb[i] if v[b] == WHT}
            cl = [k for k in ks if W[k]["n"] is not None]
            if len(cl) > 1: ch |= s.set(i, BLK, "between"); continue
            if cl:
                tot = 1 + sum(len(W[k]["cells"]) for k in ks)
                if tot > W[cl[0]]["n"]: ch |= s.set(i, BLK, "between")
        if ch: return True
        # out of reach of every numbered patch
        R = s.reach()
        for i in range(G.N):
            if v[i] == UNK and i not in R: ch |= s.set(i, BLK, "reach")
        for c in W:
            if c["n"] is None and not any(x in R for x in c["cells"]): raise Contradiction("orphan snow")
        if ch: return True
        # 2x2 rule
        for b in G.blocks:
            un = [i for i in b if v[i] == UNK]
            if len(un) == 1 and all(v[i] == BLK for i in b if i != un[0]): ch |= s.set(un[0], WHT, "2x2")
        if ch: return True
        # a 2x2 of path/unknown must get some snow: if only one of its cells can still be reached, that one is snow
        for b in G.blocks:
            if any(v[i] == WHT for i in b): continue
            rr = [i for i in b if v[i] == UNK and i in R]
            if not rr: raise Contradiction("unavoidable 2x2")
            if len(rr) == 1: ch |= s.set(rr[0], WHT, "pool")
        if ch: return True
        # only one way out
        for c in W:
            if (c["n"] is None or len(c["cells"]) < c["n"]) and len(c["unk"]) == 1:
                ch |= s.set(next(iter(c["unk"])), WHT, "exit")
        for c in s.Bc:
            if len(c["cells"]) < G.black_total and len(c["unk"]) == 1:
                ch |= s.set(next(iter(c["unk"])), BLK, "path-exit")
        return ch

    # --- T2 rules -------------------------------------------------------------
    def needs(s):
        """For each numbered patch k: groups of cells of which its finished shape must include at least one
        (2x2 blocks only k can save, and unnumbered snow only k can reach)."""
        G = s.G; v = s.v; W = s.W; R = s.reach(); need = {}
        for b in G.blocks:
            if any(v[i] == WHT for i in b): continue
            who = {k for i in b if v[i] == UNK for k, cells in s.by.items() if i in cells}
            if len(who) == 1:
                k = who.pop(); need.setdefault(k, []).append(frozenset(i for i in b if v[i] == UNK and i in s.by[k]))
        for c in W:
            if c["n"] is not None: continue
            who = {k for k, cells in s.by.items() if c["cells"][0] in cells}
            if len(who) == 1:
                k = who.pop(); need.setdefault(k, []).append(frozenset(c["cells"]))
        return need

    def completions(s, k, cap=1500, need=()):
        """Every way numbered patch k can be finished (as frozensets), or None if more than cap."""
        G = s.G; v = s.v; comp = s.comp; W = s.W; c = W[k]; n = c["n"]
        def ok_cell(b):
            if v[b] == BLK: return False
            if v[b] == WHT and comp[b] != k and W[comp[b]]["n"] is not None: return False
            return not any(v[x] == WHT and comp[x] != k and W[comp[x]]["n"] is not None for x in G.nb[b])
        res = set(); seen = set(); count = [0]
        def grow(cells):
            key = frozenset(cells)
            if key in seen: return True
            seen.add(key)
            if len(seen) > cap * 8: return False
            if len(cells) == n:
                bd = {b for a in cells for b in G.nb[a] if b not in cells}
                if any(v[b] == WHT for b in bd): return True
                if any(not (g & cells) for g in need): return True
                for blk in {bl for b in bd for bl in G.blocks_of[b]}:
                    if all(x in bd or v[x] == BLK for x in blk): return True
                res.add(key)
                return len(res) <= cap
            cand = {b for a in cells for b in G.nb[a] if b not in cells and v[b] != BLK}
            for b in cand:
                if not ok_cell(b): continue
                add = {b}
                if v[b] == WHT: add = set(W[comp[b]]["cells"])
                for x in G.nb[b]:   # joining b also swallows any unnumbered snow next to it
                    if v[x] == WHT and comp[x] != k and x not in cells: add |= set(W[comp[x]]["cells"])
                nc = cells | add
                if len(nc) > n: continue
                if not grow(nc): return False
            return True
        if not grow(frozenset(c["cells"])): return None
        return res

    def articulation(s):
        """Unknown cells the path cannot do without (making them snow would split the path)."""
        G = s.G; v = s.v; ch = False
        blacks = [i for i in range(G.N) if v[i] == BLK]
        if len(blacks) < 2: return False
        for u in range(G.N):
            if v[u] != UNK: continue
            st = [blacks[0]] if blacks[0] != u else [blacks[1]]; seen = set(st)
            while st:
                a = st.pop()
                for b in G.nb[a]:
                    if b != u and b not in seen and v[b] != WHT: seen.add(b); st.append(b)
            if any(b not in seen for b in blacks): ch |= s.set(u, BLK, "path-needs")
        return ch

    def t2(s):
        s.analyse(); G = s.G; v = s.v; ch = False
        if s.articulation(): return True
        s.analyse(); W = s.W
        need = s.needs()
        union = set(); done = set()
        for k, c in enumerate(W):
            if c["n"] is None or len(c["cells"]) == c["n"]: continue
            if c["n"] - len(c["cells"]) > 9: continue
            comps_ = s.completions(k, need=need.get(k, ()))
            if comps_ is None: continue
            if not comps_: raise Contradiction("patch cannot finish")
            done.add(k)
            inter = frozenset.intersection(*comps_)
            for i in inter: ch |= s.set(i, WHT, "patch-list")
            bds = [frozenset(b for a in cs for b in G.nb[a] if b not in cs) for cs in comps_]
            for i in frozenset.intersection(*bds):
                if v[i] == UNK: ch |= s.set(i, BLK, "patch-list")
            for cs in comps_: union |= cs
            if ch: return True
        if done:
            R = s.reach(skip=done) | union
            for i in range(G.N):
                if v[i] == UNK and i not in R: ch |= s.set(i, BLK, "patch-list")
        return ch

    def propagate(s, tier):
        while True:
            if s.t1(): continue
            if tier >= 2 and s.t2(): continue
            break
        s.analyse()

    def solved(s):
        return all(x != UNK for x in s.v)


def solve(p, tier, return_state=False, max_trials=99):
    """Run the logic solver up to `tier`. Returns True if it finishes (or (ok, state))."""
    G = Grid(p); st = State(G)
    try:
        st.propagate(min(tier, 2))
        if tier >= 3:
            while not st.solved():
                hit = False
                for i in range(G.N):
                    if st.v[i] != UNK: continue
                    for val in (BLK, WHT):
                        t = st.copy(); t.v[i] = val
                        try: t.propagate(2); clash = False
                        except Contradiction: clash = True
                        if clash:
                            st.set(i, WHT if val == BLK else BLK, "trial"); hit = True; break
                    if hit: break
                if not hit or st.stats.get("trial", 0) > max_trials: break
                st.propagate(2)
    except Contradiction:
        return (False, st) if return_state else False
    ok = st.solved()
    if ok:
        sol = ["".join("#" if st.v[r * G.w + c] == BLK else "." for c in range(G.w)) for r in range(G.h)]
        try: check_solution(p, sol)
        except AssertionError: ok = False
        st.sol = sol
    return (ok, st) if return_state else ok


def need_tier(p):
    for t in (1, 2, 3):
        if solve(p, t): return t
    return None
