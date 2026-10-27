"""Independent backtracking counter (no SAT, no shared code with the generator's solver):
fills the grid one row at a time from the row arrangements that fit that row's clues, and
prunes with each column's clues (a column's partial top-down sequence must start some full
arrangement that fits that column's clues). Each row's arrangements are stored as a prefix
tree, so a row is built cell by cell and only heights its column still allows are tried."""
from itertools import permutations


def _vis(seq):
    best = 0; k = 0
    for h in seq:
        if h > best: best = h; k += 1
    return k


def bt_solutions(p, limit=2):
    n = p["n"]; cl = p["clues"]
    perms = list(permutations(range(1, n + 1)))
    fits = lambda s, a, b: (a is None or _vis(s) == a) and (b is None or _vis(s[::-1]) == b)
    tries = []
    for r in range(n):
        t = {}
        for s in perms:
            if fits(s, cl["left"][r], cl["right"][r]):
                node = t
                for h in s: node = node.setdefault(h, {})
        tries.append(t)
    nxt = []                      # per column: partial top-down sequence -> heights allowed next
    for c in range(n):
        d = {}
        for s in perms:
            if fits(s, cl["top"][c], cl["bottom"][c]):
                for k in range(n): d.setdefault(s[:k], set()).add(s[k])
        nxt.append(d)
    out = []; grid = []; cols = [() for _ in range(n)]
    def rows(node, c, cur):
        if c == n: yield tuple(cur); return
        allow = nxt[c].get(cols[c], ())
        for h, child in node.items():
            if h in allow:
                cur.append(h); yield from rows(child, c + 1, cur); cur.pop()
    def go(r):
        if len(out) >= limit: return
        if r == n: out.append([list(x) for x in grid]); return
        for s in list(rows(tries[r], 0, [])):
            grid.append(s); old = cols[:]
            for c in range(n): cols[c] = cols[c] + (s[c],)
            go(r + 1)
            cols[:] = old; grid.pop()
            if len(out) >= limit: return
    go(0)
    return out
