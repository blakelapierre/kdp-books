"""Small SAT helpers (python-sat, CaDiCaL) used by the generators."""
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool

class CNF:
    def __init__(s): s.pool = IDPool(); s.cls = []
    def v(s, *key): return s.pool.id(key)
    def add(s, cl): s.cls.append(list(cl))
    def eq(s, lits, k): s.cls += CardEnc.equals(lits, bound=k, vpool=s.pool, encoding=EncType.seqcounter).clauses
    def atmost(s, lits, k):
        if len(lits) > k: s.cls += CardEnc.atmost(lits, bound=k, vpool=s.pool, encoding=EncType.seqcounter).clauses
    def atleast(s, lits, k): s.cls += CardEnc.atleast(lits, bound=k, vpool=s.pool, encoding=EncType.seqcounter).clauses
    def solutions(s, keys, limit=2, extra=()):
        """Enumerate up to `limit` distinct assignments of the variables in `keys` (list of var keys)."""
        ids = [s.v(*k) for k in keys]; out = []
        with Cadical153(bootstrap_with=s.cls + [list(c) for c in extra]) as S:
            while len(out) < limit and S.solve():
                m = set(l for l in S.get_model() if l > 0)
                sol = frozenset(k for k, i in zip(keys, ids) if i in m); out.append(sol)
                S.add_clause([-i if i in m else i for i in ids])
        return out
