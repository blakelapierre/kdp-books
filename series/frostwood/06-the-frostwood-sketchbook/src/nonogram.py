"""Nonogram core: clues from a picture, an exact line solver (the generator's solver) and a
grid solver that records how many sweeps it needed. The independent SAT counter is in satcheck.py."""
import sys
sys.setrecursionlimit(10000)


def clues_of(line):
    out = []; run = 0
    for v in line:
        if v: run += 1
        elif run: out.append(run); run = 0
    if run: out.append(run)
    return out


def picture_clues(img):
    n_r = len(img); n_c = len(img[0])
    rows = [clues_of(r) for r in img]
    cols = [clues_of([img[r][c] for r in range(n_r)]) for c in range(n_c)]
    return rows, cols


def line_solve(clue, line):
    """Exact line deduction. line: list of -1 (unknown) / 0 (white) / 1 (black).
    Returns the most specific line consistent with every placement of the clue, or None if none fits."""
    n = len(line); k = len(clue)
    # prefix count of known whites, for 'can a block sit on [s, s+L)?'
    pw = [0] * (n + 1)
    for i, v in enumerate(line): pw[i + 1] = pw[i] + (v == 0)
    def fits(s, L): return s + L <= n and pw[s + L] - pw[s] == 0
    memo = {}
    def F(i, j):
        key = (i, j)
        if key in memo: return memo[key]
        if j == k:
            r = all(line[t] != 1 for t in range(i, n))
        elif i >= n:
            r = False
        else:
            r = False
            if line[i] != 1 and F(i + 1, j): r = True
            L = clue[j]
            if not r and fits(i, L):
                e = i + L
                if e == n: r = (j == k - 1)
                elif line[e] != 1: r = F(e + 1, j + 1)
        memo[key] = r; return r
    if not F(0, 0): return None
    cw = [False] * n; cb = [False] * n
    seen = set(); stack = [(0, 0)]
    while stack:
        i, j = stack.pop()
        if (i, j) in seen: continue
        seen.add((i, j))
        if j == k:
            for t in range(i, n): cw[t] = True
            continue
        if i >= n: continue
        if line[i] != 1 and F(i + 1, j):
            cw[i] = True; stack.append((i + 1, j))
        L = clue[j]
        if fits(i, L):
            e = i + L
            ok = (e == n and j == k - 1) or (e < n and line[e] != 1 and F(e + 1, j + 1))
            if ok:
                for t in range(i, e): cb[t] = True
                if e < n: cw[e] = True; stack.append((e + 1, j + 1))
    out = []
    for i in range(n):
        if cb[i] and cw[i]: out.append(-1)
        elif cb[i]: out.append(1)
        else: out.append(0)
    return out


class Stats:
    def __init__(s): s.sweeps = 0; s.line_moves = 0; s.first_sweep_known = 0


def solve(rows, cols, grid=None, stats=None):
    """Repeated full sweeps (all rows, then all columns) of exact line deduction.
    Returns (grid, status) with status 'solved', 'stuck' or 'contradiction'."""
    R, C = len(rows), len(cols)
    g = [row[:] for row in grid] if grid else [[-1] * C for _ in range(R)]
    st = stats or Stats()
    dirty_r = set(range(R)); dirty_c = set(range(C))
    while dirty_r or dirty_c:
        st.sweeps += 1
        nr, nc = set(), set()
        for r in sorted(dirty_r):
            new = line_solve(rows[r], g[r])
            if new is None: return g, "contradiction"
            ch = [c for c in range(C) if new[c] != g[r][c]]
            if ch:
                st.line_moves += 1; g[r] = new; nc.update(ch)
        dirty_c |= nc
        for c in sorted(dirty_c):
            col = [g[r][c] for r in range(R)]
            new = line_solve(cols[c], col)
            if new is None: return g, "contradiction"
            ch = [r for r in range(R) if new[r] != col[r]]
            if ch:
                st.line_moves += 1
                for r in ch: g[r][c] = new[r]
                nr.update(ch)
        if st.sweeps == 1: st.first_sweep_known = sum(v != -1 for row in g for v in row)
        dirty_r = nr; dirty_c = set()
    done = all(v != -1 for row in g for v in row)
    return g, ("solved" if done else "stuck")


def grade(rows, cols):
    st = Stats(); g, status = solve(rows, cols, stats=st)
    R, C = len(rows), len(cols)
    return dict(status=status, sweeps=st.sweeps, moves=st.line_moves,
                first=round(st.first_sweep_known / (R * C), 3))
