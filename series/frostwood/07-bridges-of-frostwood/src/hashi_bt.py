"""Independent Hashi solution counter (plain backtracking, no SAT, no shared code with hashi.py).

It rebuilds the island neighbours from the grid itself (consecutive islands along each row
and column), then fills islands one at a time in reading order, trying every split of the
island's remaining number over its still-open bridges, while marking the cells each bridge
covers so no two bridges can cross. A finished, closed-off group of islands is pruned
early, and every complete fill is checked for one connected network."""
from itertools import product


def bt_solutions(p, limit=2):
    W, H = p["w"], p["h"]
    num = {(r, c): n for r, c, n in p["islands"]}
    order = sorted(num)                         # reading order
    idx = {x: i for i, x in enumerate(order)}
    need = [num[x] for x in order]; N = len(order)
    pairs = []                                  # (a, b, covered cells)
    for r in range(H):
        row = [c for c in range(W) if (r, c) in num]
        for c1, c2 in zip(row, row[1:]):
            pairs.append((idx[(r, c1)], idx[(r, c2)], [(r, c) for c in range(c1 + 1, c2)]))
    for c in range(W):
        col = [r for r in range(H) if (r, c) in num]
        for r1, r2 in zip(col, col[1:]):
            pairs.append((idx[(r1, c)], idx[(r2, c)], [(r, c) for r in range(r1 + 1, r2)]))
    at = [[] for _ in range(N)]
    for q, (a, b, _) in enumerate(pairs): at[a].append(q); at[b].append(q)
    val = [None] * len(pairs); used = [0] * N; occ = {}; out = []

    def can_place(q):
        return all(x not in occ for x in pairs[q][2])

    def closed_group_ok():
        # any group of islands that is complete (no open pairs left, all numbers met)
        # and not the whole map makes the fill impossible
        seen = [False] * N
        for s in range(N):
            if seen[s]: continue
            comp = [s]; seen[s] = True; k = 0; open_ = False
            while k < len(comp):
                u = comp[k]; k += 1
                if used[u] != need[u]: open_ = True
                for q in at[u]:
                    if val[q] is None: open_ = True
                    elif val[q] > 0:
                        a, b, _ = pairs[q]; v = b if a == u else a
                        if not seen[v]: seen[v] = True; comp.append(v)
            if not open_ and len(comp) < N: return False
        return True

    def rec(i):
        if len(out) >= limit: return
        if i == N:
            if closed_group_ok():
                out.append(sorted((min(order[pairs[q][0]], order[pairs[q][1]]), max(order[pairs[q][0]], order[pairs[q][1]]), val[q])
                                  for q in range(len(pairs)) if val[q]))
            return
        free = [q for q in at[i] if val[q] is None]
        left = need[i] - used[i]
        for combo in product((0, 1, 2), repeat=len(free)):
            if sum(combo) != left: continue
            ok = True; placed = []
            for q, v in zip(free, combo):
                a, b, cells = pairs[q]; o = b if a == i else a
                if v and (used[o] + v > need[o] or not can_place(q)): ok = False; break
                val[q] = v; placed.append(q)
                if v:
                    used[i] += v; used[o] += v
                    for x in cells: occ[x] = q
            if ok:
                # every later island must still be able to reach its number
                for j in range(i + 1, N):
                    cap = sum(2 for q in at[j] if val[q] is None and can_place(q))
                    if used[j] > need[j] or used[j] + cap < need[j]: ok = False; break
            if ok and closed_group_ok(): rec(i + 1)
            for q in placed:
                v = val[q]; a, b, cells = pairs[q]; o = b if a == i else a
                if v:
                    used[i] -= v; used[o] -= v
                    for x in cells: del occ[x]
                val[q] = None
            if len(out) >= limit: return

    rec(0)
    # report as island-index triples in the puzzle's own island order
    pidx = {(r, c): k for k, (r, c, _) in enumerate(p["islands"])}
    res = []
    for s in out:
        res.append(sorted((min(pidx[a], pidx[b]), max(pidx[a], pidx[b]), v) for a, b, v in s))
    return res
