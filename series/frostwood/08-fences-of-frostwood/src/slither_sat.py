"""Independent Slitherlink solution counter: CNF + CaDiCaL (python-sat), with lazily added
single-loop cuts. Shares no code with the generator or the logic solver (own geometry)."""
from itertools import combinations
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool


def edges_of(w, h):
    """Own edge numbering, same convention as the data file: H(r,c) = r*w+c, V(r,c) = (h+1)*w + r*(w+1)+c."""
    ends = {}
    for r in range(h + 1):
        for c in range(w): ends[r * w + c] = ((r, c), (r, c + 1))
    for r in range(h):
        for c in range(w + 1): ends[(h + 1) * w + r * (w + 1) + c] = ((r, c), (r + 1, c))
    return ends


def sat_solutions(p, limit=2):
    w, h, clues = p["w"], p["h"], p["clues"]
    ends = edges_of(w, h); E = sorted(ends)
    pool = IDPool(); x = {e: pool.id(("e", e)) for e in E}; cls = []
    at = {}
    for e, (a, b) in ends.items(): at.setdefault(a, []).append(e); at.setdefault(b, []).append(e)
    for v, es in at.items():            # degree 0 or 2 at every post
        for e in es: cls.append([-x[e]] + [x[f] for f in es if f != e])
        for a, b, c in combinations(es, 3): cls.append([-x[a], -x[b], -x[c]])
    for r in range(h):
        for c in range(w):
            n = clues[r][c]
            if n is None: continue
            side = [x[r * w + c], x[(r + 1) * w + c], x[(h + 1) * w + r * (w + 1) + c], x[(h + 1) * w + r * (w + 1) + c + 1]]
            cls += CardEnc.equals(side, bound=n, vpool=pool, encoding=EncType.seqcounter).clauses
    cls.append([x[e] for e in E])       # at least one fence
    out = []
    with Cadical153(bootstrap_with=cls) as S:
        while len(out) < limit and S.solve():
            m = set(l for l in S.get_model() if l > 0)
            on = [e for e in E if x[e] in m]
            comps = loops(on, ends)
            if len(comps) == 1:
                out.append(sorted(on)); S.add_clause([-x[e] for e in on]); continue
            for comp in comps:          # a closed loop may only exist if it is the only fence
                for f in E:
                    if f not in comp: S.add_clause([-x[e] for e in comp] + [-x[f]])
    return out


def loops(on, ends):
    adj = {}
    for e in on:
        a, b = ends[e]; adj.setdefault(a, []).append(e); adj.setdefault(b, []).append(e)
    seen = set(); comps = []
    for e0 in on:
        if e0 in seen: continue
        comp = set(); st = [e0]
        while st:
            e = st.pop()
            if e in comp: continue
            comp.add(e)
            for v in ends[e]: st += [f for f in adj[v] if f not in comp]
        seen |= comp; comps.append(comp)
    return comps
