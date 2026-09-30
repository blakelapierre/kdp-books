"""Train Tracks geometry + human-style logic solver (used by the generator for grading).

Grid n x n, cells (r, c), r=0 top. The track enters the grid through the LEFT edge of cell (er, 0)
and leaves through the BOTTOM edge of cell (n-1, ec). Every track cell holds a straight or a curve
(exactly two connections). Row/column numbers count track cells. The track is one simple path.
Edges: H(r,c) joins (r,c)-(r,c+1) for c=-1..n-1 (c=-1 / c=n-1 are border edges);
       V(r,c) joins (r,c)-(r+1,c) for r=-1..n-1.
"""
DIRS = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}

class Contradiction(Exception):
    pass

class Geo:
    _cache = {}
    def __new__(cls, n):
        if n in cls._cache: return cls._cache[n]
        g = super().__new__(cls); g._init(n); cls._cache[n] = g; return g
    def _init(s, n):
        s.n = n; s.NC = n * n; s.NH = n * (n + 1); s.NE = s.NH + n * (n + 1)
        s.ends = [None] * s.NE          # edge -> (cellA, cellB), -1 = outside
        for r in range(n):
            for c in range(-1, n):
                a = r * n + c if c >= 0 else -1; b = r * n + c + 1 if c + 1 < n else -1
                s.ends[s.H(r, c)] = (a, b)
        for r in range(-1, n):
            for c in range(n):
                a = r * n + c if r >= 0 else -1; b = (r + 1) * n + c if r + 1 < n else -1
                s.ends[s.V(r, c)] = (a, b)
        s.cell_edges = []
        for r in range(n):
            for c in range(n):
                s.cell_edges.append({"N": s.V(r - 1, c), "S": s.V(r, c), "W": s.H(r, c - 1), "E": s.H(r, c)})
        s.cell_elist = [tuple(d.values()) for d in s.cell_edges]
        s.rows = [[r * n + c for c in range(n)] for r in range(n)]
        s.cols = [[r * n + c for r in range(n)] for c in range(n)]
        s.border = [e for e in range(s.NE) if -1 in s.ends[e]]
        s.internal = [e for e in range(s.NE) if -1 not in s.ends[e]]
        # parity cuts: (edges crossing, required parity)
        s.vcut = [[s.H(r, c) for r in range(n)] for c in range(n - 1)]   # between col c and c+1
        s.hcut = [[s.V(r, c) for c in range(n)] for r in range(n - 1)]   # between row r and r+1
    def H(s, r, c): return r * (s.n + 1) + (c + 1)
    def V(s, r, c): return s.NH + (r + 1) * s.n + c

def piece_edges(g, cell, piece):
    return [g.cell_edges[cell][d] for d in piece]

def path_pieces(n, path, er, ec):
    """path: list of (r,c) from entry to exit. Returns {cell: piece-string}."""
    out = {}
    for i, (r, c) in enumerate(path):
        ds = []
        for (rr, cc) in ([path[i - 1]] if i > 0 else []) + ([path[i + 1]] if i + 1 < len(path) else []):
            for d, (dr, dc) in DIRS.items():
                if (r + dr, c + dc) == (rr, cc): ds.append(d)
        if i == 0: ds.append("W")
        if i == len(path) - 1: ds.append("S")
        out[r * n + c] = "".join(sorted(ds, key="NESW".index))
    return out

class State:
    __slots__ = ("g", "cell", "edge", "rows", "cols", "er", "ec", "total", "stats")
    def __init__(s, g, rows, cols, er, ec):
        s.g = g; s.rows = rows; s.cols = cols; s.er = er; s.ec = ec; s.total = sum(rows)
        s.cell = [0] * g.NC; s.edge = [0] * g.NE; s.stats = {}
        for e in g.border: s.edge[e] = -1
        s.edge[g.H(er, -1)] = 1; s.edge[g.V(g.n - 1, ec)] = 1
    def copy(s):
        t = State.__new__(State)
        t.g = s.g; t.rows = s.rows; t.cols = s.cols; t.er = s.er; t.ec = s.ec; t.total = s.total
        t.cell = s.cell[:]; t.edge = s.edge[:]; t.stats = dict(s.stats); return t
    def solved(s): return 0 not in s.cell and all(s.edge[e] != 0 for e in s.g.internal)
    def unknowns(s): return s.cell.count(0) + sum(1 for e in s.g.internal if s.edge[e] == 0)

def set_cell(st, c, v, tag):
    if st.cell[c] == v: return False
    if st.cell[c] == -v: raise Contradiction
    st.cell[c] = v; st.stats[tag] = st.stats.get(tag, 0) + 1; return True

def set_edge(st, e, v, tag):
    if st.edge[e] == v: return False
    if st.edge[e] == -v: raise Contradiction
    st.edge[e] = v; st.stats[tag] = st.stats.get(tag, 0) + 1; return True

def rule_cells(st):
    ch = False; E = st.edge; g = st.g
    for c in range(g.NC):
        es = g.cell_elist[c]; y = u = 0
        for e in es:
            v = E[e]
            if v == 1: y += 1
            elif v == 0: u += 1
        cv = st.cell[c]
        if y > 2: raise Contradiction
        if cv == -1:
            if y: raise Contradiction
            for e in es:
                if E[e] == 0: ch |= set_edge(st, e, -1, "cell")
            continue
        if y >= 1 and cv == 0: ch |= set_cell(st, c, 1, "cell"); cv = 1
        if y == 2:
            for e in es:
                if E[e] == 0: ch |= set_edge(st, e, -1, "cell")
        elif y + u < 2:
            if y == 1 or cv == 1: raise Contradiction
            ch |= set_cell(st, c, -1, "cell")
            for e in es:
                if E[e] == 0: ch |= set_edge(st, e, -1, "cell")
        elif cv == 1 and y + u == 2:
            for e in es:
                if E[e] == 0: ch |= set_edge(st, e, 1, "cell")
    return ch

def rule_counts(st):
    ch = False; g = st.g
    for lines, ks in ((g.rows, st.rows), (g.cols, st.cols)):
        for line, k in zip(lines, ks):
            t = u = 0
            for c in line:
                v = st.cell[c]
                if v == 1: t += 1
                elif v == 0: u += 1
            if t > k or t + u < k: raise Contradiction
            if u and t == k:
                for c in line:
                    if st.cell[c] == 0: ch |= set_cell(st, c, -1, "count")
            elif u and t + u == k:
                for c in line:
                    if st.cell[c] == 0: ch |= set_cell(st, c, 1, "count")
    return ch

def fragments(st):
    g = st.g; S, T = g.NC, g.NC + 1
    par = list(range(g.NC + 2)); size = [1] * g.NC + [0, 0]
    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for e in range(g.NE):
        if st.edge[e] != 1: continue
        a, b = g.ends[e]
        if a == -1: a = S if e == g.H(st.er, -1) else T
        if b == -1: b = S if e == g.H(st.er, -1) else T
        ra, rb = find(a), find(b)
        if ra == rb: raise Contradiction      # a closed loop
        par[ra] = rb; size[rb] += size[ra]
    return find, size, S, T

def rule_loops(st):
    ch = False; g = st.g
    find, size, S, T = fragments(st)
    rS, rT = find(S), find(T)
    if rS == rT and size[rS] != st.total: raise Contradiction
    for e in g.internal:
        if st.edge[e] != 0: continue
        a, b = g.ends[e]; ra, rb = find(a), find(b)
        if ra == rb: ch |= set_edge(st, e, -1, "loop")
        elif {ra, rb} == {rS, rT} and size[ra] + size[rb] != st.total: ch |= set_edge(st, e, -1, "loop")
    return ch

def rule_parity(st):
    ch = False; g = st.g; n = g.n
    for cuts, odd_of in ((g.vcut, lambda i: st.ec > i), (g.hcut, lambda i: st.er <= i)):
        for i, es in enumerate(cuts):
            y = 0; unk = []
            for e in es:
                v = st.edge[e]
                if v == 1: y += 1
                elif v == 0: unk.append(e)
            need = 1 if odd_of(i) else 0
            if not unk:
                if y % 2 != need: raise Contradiction
            elif len(unk) == 1:
                ch |= set_edge(st, unk[0], 1 if (y + 1) % 2 == need else -1, "parity")
    return ch

def final_check(st):
    """Fully decided state must be exactly one path from entry to exit."""
    g = st.g; find, size, S, T = fragments(st)
    if find(S) != find(T) or size[find(S)] != st.total: raise Contradiction

def propagate(st, tier):
    while True:
        ch = rule_cells(st)
        ch |= rule_counts(st)
        if ch: continue
        if tier >= 2 and rule_loops(st): continue
        if tier >= 3 and rule_parity(st): continue
        break
    if st.solved(): final_check(st)

def solve(p, tier, return_state=False):
    """tier 1: cell+count rules; 2: +loop/fragment rules; 3: +parity cuts; 4: +one-step trial.
    Returns True if logic alone determines the full solution."""
    g = Geo(p["n"]); st = State(g, p["rows"], p["cols"], p["er"], p["ec"])
    try:
        for c, pc in p["givens"].items():
            c = int(c); set_cell(st, c, 1, "given")
            for d in "NESW":
                set_edge(st, g.cell_edges[c][d], 1 if d in pc else -1, "given")
        propagate(st, min(tier, 3))
        if tier >= 4:
            while not st.solved():
                if not trial_round(st): break
    except Contradiction:
        return (False, None) if return_state else False
    ok = st.solved()
    return (ok, st) if return_state else ok

def trial_round(st):
    """Try each undecided cell/edge both ways (depth 1, full tier-3 propagation); keep forced results."""
    g = st.g; progress = False
    cands = [("c", c) for c in range(g.NC) if st.cell[c] == 0] + [("e", e) for e in g.internal if st.edge[e] == 0]
    for kind, x in cands:
        if (st.cell[x] if kind == "c" else st.edge[x]) != 0: continue
        for v in (1, -1):
            t = st.copy()
            try:
                (set_cell if kind == "c" else set_edge)(t, x, v, "trial"); propagate(t, 3)
            except Contradiction:
                (set_cell if kind == "c" else set_edge)(st, x, -v, "trial"); propagate(st, 3)
                progress = True; break
        if st.solved(): return True
    return progress
