"""Tents (Tents and Trees) rules, SAT counter, and human-style logic solver.

Rules:
  - Place tents so each tree has exactly one orthogonally adjacent tent.
  - Tents do not touch even diagonally.
  - Row/column numbers show how many tents go in that row/column.
"""
from itertools import combinations
from satutil import CNF

N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
N8 = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))


def check_puzzle(p):
    n = p["n"]; trees = [tuple(t) for t in p["trees"]]; ts = set(trees)
    assert len(trees) == len(ts) == sum(p["rows"]) == sum(p["cols"])
    assert len(p["rows"]) == n == len(p["cols"])
    assert all(0 <= r < n and 0 <= c < n for r, c in trees)
    assert all(0 <= x <= n for x in p["rows"] + p["cols"])
    assert 1 <= len(trees) <= n * n // 2


def check_solution(p):
    n = p["n"]; trees = [tuple(t) for t in p["trees"]]; ts = set(trees)
    tents = [tuple(t) for t in p["tents"]]; tentset = set(tents)
    assert len(tents) == len(tentset) == len(trees)
    assert tentset.isdisjoint(ts)
    assert all(0 <= r < n and 0 <= c < n for r, c in tents)
    for r, c in tents:
        assert not any((r + dr, c + dc) in tentset for dr, dc in N8)
    matched = set()
    for tr, tc in trees:
        nbs = [(tr + dr, tc + dc) for dr, dc in N4 if (tr + dr, tc + dc) in tentset]
        assert len(nbs) == 1, (tr, tc, nbs)
        matched.add(nbs[0])
    assert matched == tentset
    rows = [sum(1 for (r, c) in tents if r == i) for i in range(n)]
    cols = [sum(1 for (r, c) in tents if c == i) for i in range(n)]
    assert rows == list(p["rows"]) and cols == list(p["cols"])


def sat_count(p, limit=2):
    n = p["n"]; trees = [tuple(t) for t in p["trees"]]; tset = set(trees)
    rows, cols = list(p["rows"]), list(p["cols"])
    inb = lambda r, c: 0 <= r < n and 0 <= c < n
    f = CNF(); T = lambda r, c: f.v("t", r, c); M = lambda i, r, c: f.v("m", i, r, c)
    into = {}
    for i, (r, c) in enumerate(trees):
        nbs = [(r + dr, c + dc) for dr, dc in N4 if inb(r + dr, c + dc) and (r + dr, c + dc) not in tset]
        f.eq([M(i, *x) for x in nbs], 1)
        for x in nbs:
            f.add([-M(i, *x), T(*x)])
            into.setdefault(x, []).append(M(i, *x))
    for r in range(n):
        for c in range(n):
            if (r, c) in tset:
                f.add([-T(r, c)]); continue
            ms = into.get((r, c), [])
            if not ms:
                f.add([-T(r, c)])
            else:
                f.add([-T(r, c)] + ms); f.atmost(ms, 1)
            for dr, dc in N8:
                rr, cc = r + dr, c + dc
                if inb(rr, cc) and (rr, cc) > (r, c):
                    f.add([-T(r, c), -T(rr, cc)])
    for i in range(n):
        f.eq([T(i, c) for c in range(n)], rows[i])
        f.eq([T(r, i) for r in range(n)], cols[i])
    sols = f.solutions([("t", r, c) for r in range(n) for c in range(n)], limit)
    return [sorted((r, c) for (_, r, c) in s) for s in sols]


def bt_count(p, limit=2):
    n = p["n"]; trees = [tuple(t) for t in p["trees"]]; ts = set(trees)
    rows, cols = list(p["rows"]), list(p["cols"]); sols = []

    def opts(t):
        r, c = t
        return sum(1 for dr, dc in N4 if 0 <= r + dr < n and 0 <= c + dc < n and (r + dr, c + dc) not in ts)

    trees = sorted(trees, key=opts)

    def rec(i, tents, rc, cc):
        if len(sols) >= limit: return
        if i == len(trees):
            if rc == rows and cc == cols: sols.append(sorted(tents))
            return
        r, c = trees[i]
        for dr, dc in N4:
            x = (r + dr, c + dc)
            if not (0 <= x[0] < n and 0 <= x[1] < n) or x in ts or x in tents: continue
            if any((x[0] + a, x[1] + b) in tents for a, b in N8): continue
            if rc[x[0]] + 1 > rows[x[0]] or cc[x[1]] + 1 > cols[x[1]]: continue
            left = len(trees) - i - 1
            if sum(rows) - (sum(rc) + 1) < left: continue
            rc[x[0]] += 1; cc[x[1]] += 1
            rec(i + 1, tents | {x}, rc, cc)
            rc[x[0]] -= 1; cc[x[1]] -= 1

    rec(0, frozenset(), [0] * n, [0] * n)
    return sols


class Contradiction(Exception):
    pass


class State:
    __slots__ = ("n", "trees", "tset", "rows", "cols", "cell", "matched", "stats", "tree_opts")

    def __init__(s, p):
        s.n = p["n"]; s.trees = [tuple(t) for t in p["trees"]]; s.tset = set(s.trees)
        s.rows = list(p["rows"]); s.cols = list(p["cols"])
        s.cell = [[0] * s.n for _ in range(s.n)]
        for r, c in s.tset: s.cell[r][c] = -1
        s.matched = [False] * len(s.trees)
        s.stats = {}
        s.tree_opts = []
        for (r, c) in s.trees:
            s.tree_opts.append([(r + dr, c + dc) for dr, dc in N4
                                if 0 <= r + dr < s.n and 0 <= c + dc < s.n and (r + dr, c + dc) not in s.tset])

    def copy(s):
        t = State.__new__(State)
        t.n = s.n; t.trees = s.trees; t.tset = s.tset; t.rows = s.rows; t.cols = s.cols
        t.cell = [row[:] for row in s.cell]; t.matched = s.matched[:]; t.stats = dict(s.stats)
        t.tree_opts = s.tree_opts; return t

    def solved(s):
        return all(s.matched) and all(s.cell[r][c] != 0 for r in range(s.n) for c in range(s.n))

    def mark(s, r, c, v, tag):
        cur = s.cell[r][c]
        if cur == v: return False
        if cur == -v: raise Contradiction
        if (r, c) in s.tset and v == 1: raise Contradiction
        s.cell[r][c] = v; s.stats[tag] = s.stats.get(tag, 0) + 1; return True


def _sync_matched(st):
    for i, opts in enumerate(st.tree_opts):
        if st.matched[i]: continue
        if any(st.cell[r][c] == 1 for r, c in opts):
            st.matched[i] = True


def _row_col_fills(st, tag="unit"):
    ch = False; n = st.n
    for i in range(n):
        open_r = [(i, c) for c in range(n) if st.cell[i][c] == 0]
        tents_r = sum(1 for c in range(n) if st.cell[i][c] == 1)
        need = st.rows[i] - tents_r
        if need < 0 or need > len(open_r): raise Contradiction
        if need == 0:
            for r, c in open_r: ch |= st.mark(r, c, -1, tag)
        elif need == len(open_r):
            for r, c in open_r: ch |= st.mark(r, c, 1, tag)
        open_c = [(r, i) for r in range(n) if st.cell[r][i] == 0]
        tents_c = sum(1 for r in range(n) if st.cell[r][i] == 1)
        needc = st.cols[i] - tents_c
        if needc < 0 or needc > len(open_c): raise Contradiction
        if needc == 0:
            for r, c in open_c: ch |= st.mark(r, c, -1, tag)
        elif needc == len(open_c):
            for r, c in open_c: ch |= st.mark(r, c, 1, tag)
    return ch


def _tent_side_effects(st, tag="touch"):
    ch = False; n = st.n
    for r in range(n):
        for c in range(n):
            if st.cell[r][c] != 1: continue
            for dr, dc in N8:
                rr, cc = r + dr, c + dc
                if 0 <= rr < n and 0 <= cc < n and st.cell[rr][cc] == 0:
                    ch |= st.mark(rr, cc, -1, tag)
            adj_trees = [i for i in range(len(st.trees))
                         if abs(st.trees[i][0] - r) + abs(st.trees[i][1] - c) == 1]
            if not adj_trees: raise Contradiction
            unmatched = [i for i in adj_trees if not st.matched[i]]
            if len(unmatched) == 1:
                st.matched[unmatched[0]] = True; ch = True
            elif len(unmatched) == 0:
                pass  # already matched
            # if 2+ unmatched trees adjacent, matching deferred
    _sync_matched(st)
    return ch


def _tree_forced(st, tag="tree"):
    ch = False
    for i, opts in enumerate(st.tree_opts):
        if st.matched[i]: continue
        if any(st.cell[r][c] == 1 for r, c in opts):
            st.matched[i] = True; continue
        open_opts = [(r, c) for r, c in opts if st.cell[r][c] == 0]
        if not open_opts: raise Contradiction
        if len(open_opts) == 1:
            r, c = open_opts[0]; ch |= st.mark(r, c, 1, tag)
    return ch


def _no_orphan_cells(st, tag="orphan"):
    ch = False; n = st.n
    useful = set()
    for i, opts in enumerate(st.tree_opts):
        if st.matched[i]: continue
        if any(st.cell[r][c] == 1 for r, c in opts): continue
        for r, c in opts:
            if st.cell[r][c] == 0: useful.add((r, c))
    for r in range(n):
        for c in range(n):
            if st.cell[r][c] == 0 and (r, c) not in useful:
                ch |= st.mark(r, c, -1, tag)
    return ch


def _pair_exclude(st, tag="pair"):
    """If two open option cells for the same tree touch (8-adj), they can't both be tents —
    already global. More useful: when a tree has options A,B and A touches every option of
    another unmatched tree, A cannot be the tent for the first... skip; keep Hall-lite:
    for a set of trees, if neighborhood size < set size -> contradiction;
    if equal and no two neighborhood cells 8-touch, all are tents.
    """
    ch = False
    unmatched = [i for i in range(len(st.trees)) if not st.matched[i]
                 and not any(st.cell[r][c] == 1 for r, c in st.tree_opts[i])]
    for sz in range(1, min(4, len(unmatched) + 1)):
        for group in combinations(unmatched, sz):
            cells = []
            seen = set()
            for i in group:
                for r, c in st.tree_opts[i]:
                    if st.cell[r][c] == 0 and (r, c) not in seen:
                        seen.add((r, c)); cells.append((r, c))
            if len(cells) < sz: raise Contradiction
            if len(cells) != sz: continue
            # check tents wouldn't 8-touch each other
            ok = True
            for a in range(sz):
                for b in range(a + 1, sz):
                    r1, c1 = cells[a]; r2, c2 = cells[b]
                    if max(abs(r1 - r2), abs(c1 - c2)) <= 1 and (r1, c1) != (r2, c2):
                        # adjacent including diagonal — can't both be tents; but Hall says they must —
                        # only force if they don't touch
                        ok = False; break
                if not ok: break
            if not ok: continue
            for r, c in cells:
                if st.cell[r][c] == 0: ch |= st.mark(r, c, 1, tag)
    return ch


def _basic(st):
    ch = False
    ch |= _row_col_fills(st, "unit")
    ch |= _tent_side_effects(st, "touch")
    ch |= _tree_forced(st, "tree")
    ch |= _no_orphan_cells(st, "orphan")
    return ch


def _close_up(st):
    """If all trees matched, mark remaining unknowns empty and check counts."""
    if not all(st.matched): return False
    ch = False
    for r in range(st.n):
        for c in range(st.n):
            if st.cell[r][c] == 0: ch |= st.mark(r, c, -1, "finish")
    tents = [(r, c) for r in range(st.n) for c in range(st.n) if st.cell[r][c] == 1]
    rows = [sum(1 for (rr, cc) in tents if rr == i) for i in range(st.n)]
    cols = [sum(1 for (rr, cc) in tents if cc == i) for i in range(st.n)]
    if rows != st.rows or cols != st.cols: raise Contradiction
    return ch


def propagate_basic(st, use_pair=False):
    while True:
        ch = _basic(st)
        if use_pair: ch |= _pair_exclude(st, "confine")
        ch |= _close_up(st) if all(st.matched) else False
        if not ch: break
    return st.solved()


def _lookahead(st, tag="trial"):
    """Single-cell forcing: if assuming cell=v leads to contradiction under basic+pair, force opposite."""
    n = st.n
    cands = []
    for i, opts in enumerate(st.tree_opts):
        if st.matched[i]: continue
        for x in opts:
            if st.cell[x[0]][x[1]] == 0: cands.append(x)
    if not cands:
        cands = [(r, c) for r in range(n) for c in range(n) if st.cell[r][c] == 0]
    # unique preserve order
    seen = set(); ordered = []
    for x in cands:
        if x not in seen: seen.add(x); ordered.append(x)
    forced = False
    for r, c in ordered:
        for guess in (1, -1):
            t = st.copy()
            try:
                t.mark(r, c, guess, tag)
                propagate_basic(t, use_pair=True)
            except Contradiction:
                st.mark(r, c, -guess, tag)
                st.stats["trial"] = st.stats.get("trial", 0) + 1
                forced = True
                break
        if forced: break
    return forced


def propagate(st, tier):
    use_pair = tier >= 3
    while True:
        try:
            if propagate_basic(st, use_pair=use_pair):
                return True
        except Contradiction:
            raise
        if tier < 4: return False
        if not _lookahead(st, "trial"):
            return st.solved()
        # loop: apply more basic after a forced cell


def solve(p, tier=4, return_state=False):
    st = State(p)
    try:
        ok = propagate(st, tier)
        if not ok and tier >= 4:
            # last resort: keep lookahead looping was already done; try a few more rounds
            for _ in range(st.n * st.n):
                if st.solved(): ok = True; break
                if not _lookahead(st, "trial"): break
                try:
                    if propagate_basic(st, use_pair=True): ok = True; break
                except Contradiction:
                    ok = False; break
            ok = st.solved()
    except Contradiction:
        ok = False
    if return_state: return ok, st
    return ok


def need_tier(p):
    for t in (1, 2, 3, 4):
        if solve(p, t): return t
    return None
