"""Independent nonogram uniqueness check: encodes the clues as CNF (block-start variables,
exactly-one per block, block order, cell = OR of covering blocks) and enumerates solutions
with python-sat. Shares no code with nonogram.py's line solver."""
from satutil import CNF


def encode(rows, cols):
    R, C = len(rows), len(cols); f = CNF()
    def line(kind, idx, clue, n, cell):
        if not clue:
            for i in range(n): f.add([-cell(i)])
            return
        k = len(clue); lo = []; s = 0
        for L in clue: lo.append(s); s += L + 1
        hi = []; e = n
        for L in reversed(clue): hi.append(e - L); e -= L + 1
        hi = hi[::-1]
        B = [{p: f.v(kind, idx, j, p) for p in range(lo[j], hi[j] + 1)} for j in range(k)]
        for j in range(k):
            f.eq(list(B[j].values()), 1)
        for j in range(k - 1):
            for p, v in B[j].items():
                for q, w in B[j + 1].items():
                    if q < p + clue[j] + 1: f.add([-v, -w])
        cover = {i: [] for i in range(n)}
        for j in range(k):
            for p, v in B[j].items():
                for i in range(p, p + clue[j]): cover[i].append(v)
        for i in range(n):
            x = cell(i)
            for v in cover[i]: f.add([-v, x])
            f.add([-x] + cover[i])
    for r in range(R): line("r", r, rows[r], C, lambda i, r=r: f.v("x", r, i))
    for c in range(C): line("c", c, cols[c], R, lambda i, c=c: f.v("x", i, c))
    return f


def count(rows, cols, limit=2):
    f = encode(rows, cols)
    keys = [("x", r, c) for r in range(len(rows)) for c in range(len(cols))]
    sols = f.solutions(keys, limit=limit)
    return [sorted((k[1], k[2]) for k in s) for s in sols]
