"""Skyscrapers ("Chimneys") puzzle model and the generator's step-by-step logic solver.

A puzzle: n (grid size), clues = {"top": [...], "bottom": [...], "left": [...], "right": [...]}
(None where no clue), sol = list of n rows of heights 1..n (a Latin square).
A clue says how many chimneys you can see from that end of the lane: a taller chimney hides
every shorter one behind it.

Logic tiers used for grading:
  T1 = edge rules (a clue k limits the first chimneys' heights) + naked and hidden singles
  T2 = T1 + whole-lane reasoning (keep only heights that appear in some arrangement of the lane
       that fits its clues and the pencil marks)
  T3 = T2 + what-ifs (try one height in one square, run T2, and rule it out if it breaks)"""
from itertools import permutations

TIERS = {1: "edge rules and singles", 2: "+ whole-lane reasoning", 3: "+ what-if tries"}


def visible(seq):
    m = 0; k = 0
    for v in seq:
        if v > m: m = v; k += 1
    return k


def lines(n, clues):
    """(cells, start clue, end clue) for every row and column."""
    L = []
    for r in range(n): L.append(([(r, c) for c in range(n)], clues["left"][r], clues["right"][r]))
    for c in range(n): L.append(([(r, c) for r in range(n)], clues["top"][c], clues["bottom"][c]))
    return L


def clues_from(sol):
    n = len(sol)
    rows = [list(r) for r in sol]; cols = [[sol[r][c] for r in range(n)] for c in range(n)]
    return {"top": [visible(c) for c in cols], "bottom": [visible(c[::-1]) for c in cols],
            "left": [visible(r) for r in rows], "right": [visible(r[::-1]) for r in rows]}


def check(p):
    """Stored solution is a Latin square that fits every clue."""
    n = p["n"]; sol = p["sol"]
    assert len(sol) == n and all(sorted(r) == list(range(1, n + 1)) for r in sol)
    assert all(sorted(sol[r][c] for r in range(n)) == list(range(1, n + 1)) for c in range(n))
    full = clues_from(sol)
    for side in ("top", "bottom", "left", "right"):
        assert len(p["clues"][side]) == n
        for a, b in zip(p["clues"][side], full[side]):
            assert a is None or a == b


class Contra(Exception): pass


def bits(m):
    return [v for v in range(1, 8) if m >> v & 1]


class State:
    def __init__(s, n, clues):
        s.n = n; s.clues = clues; s.L = lines(n, clues)
        full = 0
        for v in range(1, n + 1): full |= 1 << v
        s.cand = [[full] * n for _ in range(n)]

    def copy(s):
        t = State.__new__(State); t.n = s.n; t.clues = s.clues; t.L = s.L
        t.cand = [row[:] for row in s.cand]; return t

    def solved(s):
        return all(bin(m).count("1") == 1 for row in s.cand for m in row)

    def grid(s):
        return [[bits(m)[0] for m in row] for row in s.cand]

    def setc(s, r, c, m):
        new = s.cand[r][c] & m
        if new == 0: raise Contra()
        if new != s.cand[r][c]: s.cand[r][c] = new; return True
        return False

    def edge(s):
        n = s.n; ch = False
        for cells, a, b in s.L:
            for k, seq in ((a, cells), (b, cells[::-1])):
                if k is None: continue
                for d, (r, c) in enumerate(seq):
                    hi = n - k + 1 + d
                    if hi < n: ch |= s.setc(r, c, (1 << (hi + 1)) - 2)
        return ch

    def singles(s):
        n = s.n; ch = False
        for cells, _, _ in s.L:
            for (r, c) in cells:
                m = s.cand[r][c]
                if bin(m).count("1") == 1:
                    for (r2, c2) in cells:
                        if (r2, c2) != (r, c): ch |= s.setc(r2, c2, ~m)
            for v in range(1, n + 1):
                where = [(r, c) for (r, c) in cells if s.cand[r][c] >> v & 1]
                if not where: raise Contra()
                if len(where) == 1: ch |= s.setc(*where[0], 1 << v)
        return ch

    def lane(s):
        ch = False
        for cells, a, b in s.L:
            ms = [s.cand[r][c] for (r, c) in cells]; n = s.n
            union = [0] * n; found = False
            def dfs(i, used, seq):
                nonlocal found
                if i == n:
                    if (a is None or visible(seq) == a) and (b is None or visible(seq[::-1]) == b):
                        found = True
                        for j, v in enumerate(seq): union[j] |= 1 << v
                    return
                for v in range(1, n + 1):
                    if ms[i] >> v & 1 and not used >> v & 1:
                        seq.append(v); dfs(i + 1, used | 1 << v, seq); seq.pop()
            dfs(0, 0, [])
            if not found: raise Contra()
            for (r, c), u in zip(cells, union): ch |= s.setc(r, c, u)
        return ch

    def run(s, tier):
        s.edge()
        while True:
            if s.singles(): continue
            if tier >= 2 and s.lane(): continue
            return


def solve(p, tier, return_state=False, cap=999):
    """Run the logic solver up to `tier`. Returns ok (finished with no guessing), stats, state."""
    st = State(p["n"], p["clues"]); stats = {"whatif": 0, "lane": 0}
    try:
        st.run(min(tier, 2))
        while tier >= 3 and not st.solved():
            progress = False
            for r in range(st.n):
                for c in range(st.n):
                    if bin(st.cand[r][c]).count("1") == 1: continue
                    for v in bits(st.cand[r][c]):
                        t = st.copy()
                        try:
                            t.setc(r, c, 1 << v); t.run(2)
                        except Contra:
                            st.setc(r, c, ~(1 << v)); stats["whatif"] += 1; st.run(2); progress = True
                            break
                    if progress: break
                if progress: break
            if not progress or stats["whatif"] > cap: break
    except Contra:
        return (False, stats, None) if return_state else False
    ok = st.solved()
    if ok and return_state:
        g = st.grid()
        if g != p.get("sol", g): ok = False
    return (ok, stats, st) if return_state else ok


def need_tier(p):
    for t in (1, 2, 3):
        if solve(p, t): return t
    return 4
