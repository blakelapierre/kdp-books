"""Independent Futoshiki solution counter: depth-first search with bitmasks, the fewest-options-first
rule, static chain-length bounds from the signs, and a look-ahead that each unfilled neighbour across
a sign still has a value that fits. Shares no code with futoshiki.py or the SAT check."""
import sys
sys.setrecursionlimit(10000)


def bt_solutions(p, limit=2):
    n = p["n"]; full = (1 << n) - 1
    grid = [[0] * n for _ in range(n)]
    rowu = [0] * n; colu = [0] * n
    for r, c, v in p["givens"]:
        if grid[r][c] and grid[r][c] != v: return []
        if not grid[r][c]:
            if rowu[r] >> (v - 1) & 1 or colu[c] >> (v - 1) & 1: return []
            grid[r][c] = v; rowu[r] |= 1 << (v - 1); colu[c] |= 1 << (v - 1)
    smaller = {}; larger = {}   # larger[(a,b)]: cells that must be bigger than (a,b)
    for a, b, c, d in p["ineq"]:
        larger.setdefault((a, b), []).append((c, d)); smaller.setdefault((c, d), []).append((a, b))
    # longest chain of strictly smaller cells below / larger cells above each cell (a cycle means no solution)
    memo_dn, memo_up = {}, {}
    def depth(cell, nbrs, memo, stack):
        if cell in memo: return memo[cell]
        if cell in stack: raise ValueError
        stack.add(cell)
        d = max((1 + depth(x, nbrs, memo, stack) for x in nbrs.get(cell, [])), default=0)
        stack.discard(cell); memo[cell] = d; return d
    try:
        lo = {(r, c): 1 + depth((r, c), smaller, memo_dn, set()) for r in range(n) for c in range(n)}
        hi = {(r, c): n - depth((r, c), larger, memo_up, set()) for r in range(n) for c in range(n)}
    except ValueError:
        return []
    def cand(r, c):
        free = full & ~(rowu[r] | colu[c])
        return [v for v in range(lo[(r, c)], hi[(r, c)] + 1) if free >> (v - 1) & 1]
    def ok(r, c, v):
        if not lo[(r, c)] <= v <= hi[(r, c)]: return False
        for (y, x) in larger.get((r, c), []):
            w = grid[y][x]
            if w:
                if not v < w: return False
            elif not any(u > v for u in cand(y, x) if not ((y == r or x == c) and u == v)): return False
        for (y, x) in smaller.get((r, c), []):
            w = grid[y][x]
            if w:
                if not w < v: return False
            elif not any(u < v for u in cand(y, x)): return False
        return True
    for r in range(n):
        for c in range(n):
            if grid[r][c] and not ok(r, c, grid[r][c]): return []
    out = []
    def rec():
        if len(out) >= limit: return
        best = None
        for r in range(n):
            for c in range(n):
                if grid[r][c]: continue
                opts = [v for v in cand(r, c) if ok(r, c, v)]
                if not opts: return
                if best is None or len(opts) < len(best[2]):
                    best = (r, c, opts)
                    if len(opts) == 1: break
            if best and len(best[2]) == 1: break
        if best is None:
            out.append([row[:] for row in grid]); return
        r, c, opts = best
        for v in opts:
            grid[r][c] = v; rowu[r] |= 1 << (v - 1); colu[c] |= 1 << (v - 1)
            rec()
            grid[r][c] = 0; rowu[r] &= ~(1 << (v - 1)); colu[c] &= ~(1 << (v - 1))
            if len(out) >= limit: return
    rec()
    return out
