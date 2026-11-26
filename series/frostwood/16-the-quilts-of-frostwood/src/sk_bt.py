"""Independent backtracking counter for Quilts (Shikaku): no SAT, no shared code with the generator.
Fills the grid square by square (first empty square in reading order); that square must be the
top-left corner of a new rectangle, which must contain exactly one number equal to its area."""


def bt_solutions(p, limit=2):
    n = p["n"]; num = {}
    for i, (r, c, a) in enumerate(p["clues"]): num[(r, c)] = (i, a)
    g = [[None] * n for _ in range(n)]; out = []
    used = set()

    def first():
        for r in range(n):
            for c in range(n):
                if g[r][c] is None: return r, c
        return None

    def rec():
        if len(out) >= limit: return
        f = first()
        if f is None:
            if len(used) == len(num): out.append([row[:] for row in g])
            return
        r, c = f
        maxw = 0
        while c + maxw < n and g[r][c + maxw] is None: maxw += 1
        for h in range(1, n - r + 1):
            if g[r + h - 1][c] is not None: break
            for w in range(1, maxw + 1):
                if any(g[r + h - 1][cc] is not None for cc in range(c, c + w)): maxw = w - 1; break
                inside = [num[(rr, cc)] for rr in range(r, r + h) for cc in range(c, c + w) if (rr, cc) in num]
                if len(inside) > 1: break          # wider ones contain these too
                if len(inside) == 1 and inside[0][1] == h * w:
                    i = inside[0][0]
                    for rr in range(r, r + h):
                        for cc in range(c, c + w): g[rr][cc] = i
                    used.add(i); rec(); used.discard(i)
                    for rr in range(r, r + h):
                        for cc in range(c, c + w): g[rr][cc] = None
                    if len(out) >= limit: return
    rec()
    return out
