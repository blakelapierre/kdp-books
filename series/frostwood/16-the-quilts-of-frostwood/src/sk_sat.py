"""Independent SAT model for Quilts (Shikaku), CaDiCaL via python-sat. Shares no code with the
generator's logic solver: here every square chooses one of the numbers, and each number's squares
must form exactly one full rectangle of the right area (encoded as: choose one placement among all
rectangles of that area containing the number; a square belongs to the number iff the chosen placement covers it)."""
from satutil import CNF


def sat_solutions(p, limit=2):
    n = p["n"]; cl = p["clues"]; F = CNF()
    keys = []
    for i, (r, c, a) in enumerate(cl):
        pl = []
        for h in range(1, a + 1):
            if a % h: continue
            w = a // h
            for r0 in range(0, n - h + 1):
                for c0 in range(0, n - w + 1):
                    if r0 <= r < r0 + h and c0 <= c < c0 + w: pl.append((r0, c0, h, w))
        lits = [F.v("p", i, q) for q in pl]
        if not lits: return []
        F.eq(lits, 1)
        for q in pl:
            r0, c0, h, w = q
            for rr in range(r0, r0 + h):
                for cc in range(c0, c0 + w): F.add([-F.v("p", i, q), F.v("x", rr, cc, i)])
        for rr in range(n):
            for cc in range(n):
                cov = [F.v("p", i, q) for q in pl if q[0] <= rr < q[0] + q[2] and q[1] <= cc < q[1] + q[3]]
                F.add([-F.v("x", rr, cc, i)] + cov)
    for rr in range(n):
        for cc in range(n):
            F.eq([F.v("x", rr, cc, i) for i in range(len(cl))], 1)
    keys = [("x", rr, cc, i) for rr in range(n) for cc in range(n) for i in range(len(cl))]
    out = []
    for sol in F.solutions(keys, limit):
        g = [[None] * n for _ in range(n)]
        for _, rr, cc, i in sol: g[rr][cc] = i
        out.append(g)
    return out
