"""INDEPENDENT verifier (does not import tracks.py / gen.py).
Encodes a Train Tracks puzzle as SAT (pysat, CaDiCaL), eliminates stray loops lazily with cycle cuts,
and counts track solutions up to 2. Also checks the stored solution against the clues directly."""
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool

def count_solutions(p, limit=2):
    n = p["n"]; er, ec = p["er"], p["ec"]
    pool = IDPool()
    X = lambda r, c: pool.id(("x", r, c))
    # internal edges: ('h', r, c) joins (r,c)-(r,c+1); ('v', r, c) joins (r,c)-(r+1,c)
    E = lambda k, r, c: pool.id((k, r, c))
    edges = [("h", r, c) for r in range(n) for c in range(n - 1)] + [("v", r, c) for r in range(n - 1) for c in range(n)]
    for k in edges: E(*k)
    def inc(r, c):
        """incident internal edge vars + number of forced border connections"""
        es = []
        if c > 0: es.append(E("h", r, c - 1))
        if c < n - 1: es.append(E("h", r, c))
        if r > 0: es.append(E("v", r - 1, c))
        if r < n - 1: es.append(E("v", r, c))
        b = (1 if (r == er and c == 0) else 0) + (1 if (r == n - 1 and c == ec) else 0)
        return es, b
    cls = []
    for r in range(n):
        for c in range(n):
            es, b = inc(r, c); x = X(r, c)
            for e in es: cls.append([-e, x])                       # edge -> both cells are track
            need = 2 - b
            if b: cls.append([x])
            # x -> exactly `need` of es ; not x -> none (already by edge->x)
            if need == 0:
                for e in es: cls.append([-e])
            else:
                atl = CardEnc.atleast(es, bound=need, vpool=pool, encoding=EncType.seqcounter)
                atm = CardEnc.atmost(es, bound=need, vpool=pool, encoding=EncType.seqcounter)
                for cl in atl.clauses: cls.append(cl + [-x])
                cls += atm.clauses
    for r in range(n):
        cls += CardEnc.equals([X(r, c) for c in range(n)], bound=p["rows"][r], vpool=pool, encoding=EncType.seqcounter).clauses
    for c in range(n):
        cls += CardEnc.equals([X(r, c) for r in range(n)], bound=p["cols"][c], vpool=pool, encoding=EncType.seqcounter).clauses
    D = {"N": (-1, 0), "S": (1, 0), "W": (0, -1), "E": (0, 1)}
    def edge_var(r, c, d):
        dr, dc = D[d]; r2, c2 = r + dr, c + dc
        if not (0 <= r2 < n and 0 <= c2 < n): return None
        if dr == 0: return E("h", r, min(c, c2))
        return E("v", min(r, r2), c)
    for key, pc in p["givens"].items():
        cell = int(key); r, c = divmod(cell, n); cls.append([X(r, c)])
        for d in "NESW":
            v = edge_var(r, c, d)
            border_on = (d == "W" and c == 0 and r == er) or (d == "S" and r == n - 1 and c == ec)
            if v is None:
                assert (d in pc) == border_on, ("given piece points off-grid", key, pc)
            else: cls.append([v] if d in pc else [-v])
    sols = []
    with Cadical153(bootstrap_with=cls) as S:
        while len(sols) < limit and S.solve():
            m = set(l for l in S.get_model() if l > 0)
            on = [k for k in edges if E(*k) in m]
            adj = {}
            for k, r, c in on:
                a, b = (r, c), ((r, c + 1) if k == "h" else (r + 1, c))
                adj.setdefault(a, []).append((b, (k, r, c))); adj.setdefault(b, []).append((a, (k, r, c)))
            # walk from entry
            seen = set(); cur, prev = (er, 0), None; path = [cur]; seen.add(cur)
            while True:
                nx = [b for b, _ in adj.get(cur, []) if b != prev]
                if not nx: break
                prev, cur = cur, nx[0]; path.append(cur); seen.add(cur)
            cells = [(r, c) for r in range(n) for c in range(n) if X(r, c) in m]
            if set(cells) == seen and path[-1] == (n - 1, ec):
                sols.append(path)
                S.add_clause([-E(*k) for k in on] + [E(*k) for k in edges if E(*k) not in m])  # block this solution
            else:
                # cut every stray cycle
                rest = set(cells) - seen
                while rest:
                    s0 = rest.pop(); comp = {s0}; stack = [s0]
                    while stack:
                        a = stack.pop()
                        for b, _ in adj.get(a, []):
                            if b not in comp: comp.add(b); stack.append(b); rest.discard(b)
                    cyc = sorted({ek for a in comp for _, ek in adj[a]})
                    S.add_clause([-E(*k) for k in cyc])
    return sols

def check_solution(p):
    """Direct check of the stored solution against every clue."""
    n = p["n"]; path = [tuple(x) for x in p["solution"]]
    assert len(set(path)) == len(path), "self-crossing"
    assert path[0] == (p["er"], 0) and path[-1] == (n - 1, p["ec"]), "endpoints"
    for a, b in zip(path, path[1:]): assert abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1, "gap"
    assert [sum(1 for r, c in path if r == i) for i in range(n)] == p["rows"], "row counts"
    assert [sum(1 for r, c in path if c == i) for i in range(n)] == p["cols"], "col counts"
    D = {(-1, 0): "N", (1, 0): "S", (0, -1): "W", (0, 1): "E"}
    for i, (r, c) in enumerate(path):
        ds = set()
        if i: ds.add(D[(path[i - 1][0] - r, path[i - 1][1] - c)])
        else: ds.add("W")
        if i + 1 < len(path): ds.add(D[(path[i + 1][0] - r, path[i + 1][1] - c)])
        else: ds.add("S")
        key = str(r * n + c)
        if key in p["givens"]: assert set(p["givens"][key]) == ds, "given piece mismatch"
    return True
