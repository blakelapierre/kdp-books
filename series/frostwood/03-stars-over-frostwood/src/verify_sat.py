"""INDEPENDENT verifier (does not import stars.py / gen.py).
Encodes a Star Battle puzzle as SAT (pysat, CaDiCaL): exactly k stars per row, column and region
(cardinality networks), no two stars in touching squares; counts solutions up to `limit` with
blocking clauses. Also checks a stored solution directly against the rules."""
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool

def _units(p):
    n = p["n"]; reg = p["regions"]
    rows = [[(r, c) for c in range(n)] for r in range(n)]
    cols = [[(r, c) for r in range(n)] for c in range(n)]
    ids = sorted({reg[r][c] for r in range(n) for c in range(n)})
    regs = [[(r, c) for r in range(n) for c in range(n) if reg[r][c] == i] for i in ids]
    return rows, cols, regs

def count_solutions(p, limit=2):
    n, k = p["n"], p["k"]; pool = IDPool()
    X = lambda r, c: pool.id((r, c))
    for r in range(n):
        for c in range(n): X(r, c)
    cls = []
    rows, cols, regs = _units(p)
    for u in rows + cols + regs:
        cls += CardEnc.equals([X(r, c) for r, c in u], bound=k, vpool=pool, encoding=EncType.seqcounter).clauses
    for r in range(n):
        for c in range(n):
            for rr, cc in ((r, c + 1), (r + 1, c - 1), (r + 1, c), (r + 1, c + 1)):
                if 0 <= rr < n and 0 <= cc < n: cls.append([-X(r, c), -X(rr, cc)])
    sols = []
    with Cadical153(bootstrap_with=cls) as s:
        while len(sols) < limit and s.solve():
            m = set(v for v in s.get_model() if v > 0)
            st = sorted((r, c) for r in range(n) for c in range(n) if X(r, c) in m)
            sols.append(st)
            s.add_clause([-X(r, c) for r, c in st])
    return sols

def connected(cells):
    S = set(cells); seen = {cells[0]}; st = [cells[0]]
    while st:
        r, c = st.pop()
        for q in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if q in S and q not in seen: seen.add(q); st.append(q)
    return len(seen) == len(S)

def check_puzzle(p):
    """well-formed: n x n, exactly n regions, each connected and big enough for k non-touching stars"""
    n = p["n"]; reg = p["regions"]
    assert len(reg) == n and all(len(row) == n for row in reg)
    rows, cols, regs = _units(p)
    assert len(regs) == n, "region count"
    for u in regs: assert connected(u), "region not connected"
    return True

def check_solution(p):
    n, k = p["n"], p["k"]; S = {tuple(x) for x in p["solution"]}
    rows, cols, regs = _units(p)
    for u in rows + cols + regs: assert sum(1 for x in u if x in S) == k, "unit count"
    for (r, c) in S:
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if (dr or dc) and (r + dr, c + dc) in S: raise AssertionError("touching stars")
    return True
