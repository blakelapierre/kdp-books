"""Slitherlink core: grid geometry, a step-by-step logic solver (used by the generator to grade
puzzles) and rule checks for a finished loop.

Grid of w x h cells. Vertices (r, c) for r in 0..h, c in 0..w, id r*(w+1)+c.
Horizontal edge H(r, c) joins vertex (r, c)-(r, c+1): id r*w + c  (r 0..h, c 0..w-1).
Vertical edge V(r, c) joins vertex (r, c)-(r+1, c): id (h+1)*w + r*(w+1) + c  (r 0..h-1, c 0..w).
Clues: list of h rows of w entries, None for a blank cell.
Edge states: 0 unknown, 1 fence (line), 2 no fence (cross)."""

UNK, LINE, CROSS = 0, 1, 2
TIERS = {1: "counting rules (cell numbers, two fence ends per post, no early closed loop)",
         2: "+ short what-if (a guess that breaks within 8 forced moves)",
         3: "+ long what-if (a guess followed as far as it goes)"}
SHORT = 8


class Geo:
    _cache = {}

    def __new__(cls, w, h):
        k = (w, h)
        if k not in cls._cache:
            o = super().__new__(cls); o._init(w, h); cls._cache[k] = o
        return cls._cache[k]

    def _init(s, w, h):
        s.w, s.h = w, h
        s.nv = (w + 1) * (h + 1)
        s.nh = (h + 1) * w
        s.ne = s.nh + h * (w + 1)
        s.ends = []
        for r in range(h + 1):
            for c in range(w): s.ends.append((r * (w + 1) + c, r * (w + 1) + c + 1))
        for r in range(h):
            for c in range(w + 1): s.ends.append((r * (w + 1) + c, (r + 1) * (w + 1) + c))
        s.vedges = [[] for _ in range(s.nv)]
        for e, (a, b) in enumerate(s.ends): s.vedges[a].append(e); s.vedges[b].append(e)
        s.cedges = []
        for r in range(h):
            for c in range(w):
                s.cedges.append([s.H(r, c), s.H(r + 1, c), s.V(r, c), s.V(r, c + 1)])
        s.ecells = [[] for _ in range(s.ne)]
        for i, es in enumerate(s.cedges):
            for e in es: s.ecells[e].append(i)

    def H(s, r, c): return r * s.w + c
    def V(s, r, c): return s.nh + r * (s.w + 1) + c


def region_edges(g, region):
    """Edges on the boundary of a set of cells (r, c)."""
    out = set()
    for (r, c) in region:
        for e, (dr, dc) in zip(g.cedges[r * g.w + c], ((-1, 0), (1, 0), (0, -1), (0, 1))):
            if (r + dr, c + dc) not in region: out.add(e)
    return out


def clues_from(g, lines):
    return [[sum(e in lines for e in g.cedges[r * g.w + c]) for c in range(g.w)] for r in range(g.h)]


def is_single_loop(g, lines):
    """True if the edge set is one simple closed loop."""
    if not lines: return False
    deg = [0] * g.nv; adj = {}
    for e in lines:
        a, b = g.ends[e]; deg[a] += 1; deg[b] += 1
        adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
    if any(d not in (0, 2) for d in deg): return False
    start = next(iter(adj)); seen = {start}; st = [start]
    while st:
        v = st.pop()
        for u in adj[v]:
            if u not in seen: seen.add(u); st.append(u)
    return len(seen) == len(adj)


def check(p):
    """Puzzle and stored solution obey every rule."""
    g = Geo(p["w"], p["h"]); lines = set(p["loop"])
    assert len(p["clues"]) == g.h and all(len(r) == g.w for r in p["clues"])
    assert is_single_loop(g, lines), "not one loop"
    for r in range(g.h):
        for c in range(g.w):
            n = p["clues"][r][c]
            if n is not None:
                assert 0 <= n <= 3 and sum(e in lines for e in g.cedges[r * g.w + c]) == n, (r, c)
    return True


class Contra(Exception):
    pass


class State:
    __slots__ = ("g", "clue", "e", "vl", "vx", "cl", "cx", "part", "plen", "nl", "q", "nset", "budget")

    def __init__(s, g, clue):
        s.g = g; s.clue = clue
        s.e = [UNK] * g.ne
        s.vl = [0] * g.nv; s.vx = [0] * g.nv
        s.cl = [0] * (g.w * g.h); s.cx = [0] * (g.w * g.h)
        s.part = list(range(g.nv))   # for a path end: the vertex at its other end
        s.plen = [0] * g.nv          # for a path end: number of edges in its path
        s.nl = 0; s.q = []; s.nset = 0; s.budget = None

    def copy(s):
        t = State.__new__(State)
        t.g = s.g; t.clue = s.clue; t.e = s.e[:]; t.vl = s.vl[:]; t.vx = s.vx[:]; t.cl = s.cl[:]; t.cx = s.cx[:]
        t.part = s.part[:]; t.plen = s.plen[:]; t.nl = s.nl; t.q = []; t.nset = 0; t.budget = None
        return t

    def closes_ok(s, e):
        """Edge e would close a loop: is that loop the whole solution?"""
        g = s.g; a, b = g.ends[e]
        if s.nl != s.plen[a]: return False
        for i, n in enumerate(s.clue):
            if n is None: continue
            k = s.cl[i] + (1 if e in g.cedges[i] else 0)
            if k != n: return False
        return True

    def set(s, e, v):
        cur = s.e[e]
        if cur == v: return
        if cur != UNK: raise Contra()
        g = s.g
        if v == LINE:
            a, b = g.ends[e]
            if s.vl[a] >= 2 or s.vl[b] >= 2: raise Contra()
            closing = s.vl[a] == 1 and s.vl[b] == 1 and s.part[a] == b
            if closing and not s.closes_ok(e): raise Contra()
        s.e[e] = v; s.nset += 1
        if s.budget is not None and s.nset > s.budget: raise OverflowError()
        if v == LINE:
            s.nl += 1
            ea = s.part[a] if s.vl[a] == 1 else a
            eb = s.part[b] if s.vl[b] == 1 else b
            la = s.plen[a] if s.vl[a] == 1 else 0
            lb = s.plen[b] if s.vl[b] == 1 else 0
            s.vl[a] += 1; s.vl[b] += 1
            for x in g.ecells[e]: s.cl[x] += 1
            if closing:
                for f in range(g.ne):
                    if s.e[f] == UNK: s.q.append((f, CROSS))
            else:
                s.part[ea] = eb; s.part[eb] = ea; s.plen[ea] = s.plen[eb] = la + lb + 1
                # an edge joining the two new ends would close this loop early
                for f in g.vedges[ea]:
                    if s.e[f] == UNK:
                        x, y = g.ends[f]
                        if (x == eb or y == eb) and not s.closes_ok(f): s.q.append((f, CROSS))
        else:
            a, b = g.ends[e]
            s.vx[a] += 1; s.vx[b] += 1
            for x in g.ecells[e]: s.cx[x] += 1
        for x in g.ends[e]: s.vertex(x)
        for x in g.ecells[e]: s.cell(x)

    def vertex(s, x):
        es = s.g.vedges[x]; L = s.vl[x]; U = len(es) - L - s.vx[x]
        if L > 2 or (L == 1 and U == 0): raise Contra()
        if U == 0: return
        if L == 2: s.q += [(f, CROSS) for f in es if s.e[f] == UNK]
        elif L == 1 and U == 1: s.q += [(f, LINE) for f in es if s.e[f] == UNK]
        elif L == 0 and U == 1: s.q += [(f, CROSS) for f in es if s.e[f] == UNK]

    def cell(s, i):
        n = s.clue[i]
        if n is None: return
        L = s.cl[i]; U = 4 - L - s.cx[i]
        if L > n or L + U < n: raise Contra()
        if U == 0: return
        if L == n: s.q += [(f, CROSS) for f in s.g.cedges[i] if s.e[f] == UNK]
        elif L + U == n: s.q += [(f, LINE) for f in s.g.cedges[i] if s.e[f] == UNK]

    def run(s):
        while s.q:
            e, v = s.q.pop(); s.set(e, v)

    def start(s):
        for i in range(len(s.clue)): s.cell(i)
        for x in range(s.g.nv): s.vertex(x)
        s.run()

    def done(s): return UNK not in s.e


def flat(clues): return [n for row in clues for n in row]


def solve(p, tier, return_state=False):
    """Logic solve with rules up to `tier`. Returns ok (and the state, with .stats) if return_state."""
    g = Geo(p["w"], p["h"]); st = State(g, flat(p["clues"])); stats = {"short": 0, "long": 0}
    ok = False
    try:
        st.start()
        while not st.done():
            if tier < 2: break
            found = False
            for limit in ((SHORT, None) if tier >= 3 else (SHORT,)):
                for e in range(g.ne):
                    if st.e[e] != UNK: continue
                    for v in (LINE, CROSS):
                        t = st.copy(); t.budget = limit
                        try:
                            t.set(e, v); t.run()
                        except Contra:
                            st.set(e, CROSS if v == LINE else LINE); st.run()
                            stats["short" if limit else "long"] += 1; found = True; break
                        except OverflowError:
                            pass
                    if found: break
                if found: break
            if not found: break
        ok = st.done()
    except Contra:
        ok = False
    st_stats = stats
    if return_state:
        return ok, st_stats, st
    return ok


def need_tier(p):
    for t in (1, 2, 3):
        if solve(p, t): return t
    return 9
