"""Independent SAT model of a Chimneys (Skyscrapers) puzzle: one-hot heights, Latin rows and
columns, and for every clue an exact count of 'visible' squares (a square is visible when it is
taller than everything before it in that direction). CaDiCaL via python-sat."""
from satutil import CNF


def sat_solutions(p, limit=2):
    n = p["n"]; S = CNF()
    X = lambda r, c, v: S.v("x", r, c, v)
    for r in range(n):
        for c in range(n): S.eq([X(r, c, v) for v in range(1, n + 1)], 1)
    for i in range(n):
        for v in range(1, n + 1):
            S.eq([X(i, c, v) for c in range(n)], 1); S.eq([X(r, i, v) for r in range(n)], 1)
    def line(cells, k, tag):
        if k is None: return
        vis = []
        for i, (r, c) in enumerate(cells):
            a_list = []
            for v in range(1, n + 1):
                a = S.v("a", tag, i, v); a_list.append(a)
                taller = [X(r2, c2, w) for (r2, c2) in cells[:i] for w in range(v + 1, n + 1)]
                S.add([-a, X(r, c, v)])
                for t in taller: S.add([-a, -t])
                S.add([-X(r, c, v)] + taller + [a])
            s = S.v("vis", tag, i); vis.append(s)
            S.add([-s] + a_list)
            for a in a_list: S.add([-a, s])
        S.eq(vis, k)
    for r in range(n):
        row = [(r, c) for c in range(n)]
        line(row, p["clues"]["left"][r], ("L", r)); line(row[::-1], p["clues"]["right"][r], ("R", r))
    for c in range(n):
        col = [(r, c) for r in range(n)]
        line(col, p["clues"]["top"][c], ("T", c)); line(col[::-1], p["clues"]["bottom"][c], ("B", c))
    keys = [("x", r, c, v) for r in range(n) for c in range(n) for v in range(1, n + 1)]
    out = []
    for sol in S.solutions(keys, limit):
        g = [[0] * n for _ in range(n)]
        for _, r, c, v in sol: g[r][c] = v
        out.append(g)
    return out
