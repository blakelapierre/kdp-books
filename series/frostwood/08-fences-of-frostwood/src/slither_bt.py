"""Second independent Slitherlink solution counter: depth-first search over fence edges with its
own simple constraint propagation (no SAT, no code shared with the generator or its logic solver).
Rules propagated: a clue cell with its number of fences closes its other sides, and one that needs
all its open sides fences them; a post has 0 or 2 fence ends. A closed loop that leaves other fence
pieces is rejected. Branching extends a loose fence end; leaves are checked as one closed loop."""


def bt_solutions(p, limit=2):
    w, h, clues = p["w"], p["h"], p["clues"]
    nh = (h + 1) * w; ne = nh + h * (w + 1); nv = (h + 1) * (w + 1)
    ends = [(r * (w + 1) + c, r * (w + 1) + c + 1) for r in range(h + 1) for c in range(w)] + \
           [(r * (w + 1) + c, (r + 1) * (w + 1) + c) for r in range(h) for c in range(w + 1)]
    at = [[] for _ in range(nv)]
    for e, (a, b) in enumerate(ends): at[a].append(e); at[b].append(e)
    cell = []
    for r in range(h):
        for c in range(w):
            if clues[r][c] is not None:
                cell.append((clues[r][c], [r * w + c, (r + 1) * w + c, nh + r * (w + 1) + c, nh + r * (w + 1) + c + 1]))
    of_edge = [[] for _ in range(ne)]
    for i, (_, es) in enumerate(cell):
        for e in es: of_edge[e].append(i)
    out = []

    def prop(s, todo):
        """s: list of edge values (None/1/0). todo: edges just set. Returns False on a contradiction."""
        while todo:
            e = todo.pop()
            groups = [at[v] for v in ends[e]] + [cell[i][1] for i in of_edge[e]]
            kinds = ["v", "v"] + [cell[i][0] for i in of_edge[e]]
            for es, k in zip(groups, kinds):
                on = sum(1 for f in es if s[f] == 1); und = [f for f in es if s[f] is None]
                if k == "v":
                    if on > 2 or (on == 1 and not und): return False
                    if on == 2 or (on == 0 and len(und) == 1): val = 0
                    elif on == 1 and len(und) == 1: val = 1
                    else: continue
                else:
                    if on > k or on + len(und) < k: return False
                    if on == k: val = 0
                    elif on + len(und) == k: val = 1
                    else: continue
                for f in und: s[f] = val; todo.append(f)
        return True

    def pieces(s):
        """Fence pieces as (edge count, closed?)."""
        adj = {}
        for e in range(ne):
            if s[e] == 1:
                a, b = ends[e]; adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
        seen = set(); res = []
        for v0 in adj:
            if v0 in seen: continue
            comp = [v0]; seen.add(v0); i = 0
            while i < len(comp):
                for u in adj[comp[i]]:
                    if u not in seen: seen.add(u); comp.append(u)
                i += 1
            closed = all(len(adj[v]) == 2 for v in comp)
            res.append((sum(len(adj[v]) for v in comp) // 2, closed))
        return res

    def search(s):
        if len(out) >= limit: return
        pc = pieces(s)
        if any(cl for _, cl in pc):
            if len(pc) > 1: return
            t = [1 if x == 1 else 0 for x in s]
            if all(sum(t[f] for f in es) == n for n, es in cell):
                sol = sorted(e for e in range(ne) if t[e] == 1)
                if sol not in out: out.append(sol)
            return
        if None not in s: return
        # branch on a loose fence end if there is one, else on an edge of a clue cell
        pick = None
        for v in range(nv):
            if sum(1 for f in at[v] if s[f] == 1) == 1:
                und = [f for f in at[v] if s[f] is None]
                if und and (pick is None or len(und) < len(pick)): pick = und
        if pick is None:
            cands = [f for n, es in sorted(cell, key=lambda x: -x[0]) for f in es if s[f] is None]
            f = cands[0] if cands else s.index(None)
            for val in (1, 0):
                t = s[:]; t[f] = val
                if prop(t, [f]): search(t)
            return
        for i, f in enumerate(pick):   # exactly one of the loose end's open edges is the fence
            t = s[:]; t[f] = 1; todo = [f]
            for g in pick:
                if g != f and t[g] is None: t[g] = 0; todo.append(g)
            if prop(t, todo): search(t)

    s = [None] * ne
    todo = []
    for n, es in cell:
        if n == 0:
            for f in es:
                if s[f] is None: s[f] = 0; todo.append(f)
    # seed propagation from every clue and post
    ok = prop(s, todo)
    if ok:
        # run each group once (a 3 in a corner, etc. are found by the general rules)
        changed = True
        while changed and ok:
            before = s[:]
            for e in range(ne):
                if not prop(s, [e]): ok = False; break
            changed = s != before
    if ok: search(s)
    return out
