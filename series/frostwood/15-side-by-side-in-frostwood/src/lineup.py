"""Core of the line-up puzzle generator for Side by Side in Frostwood (generator side only;
verify.py does not import this). People sit in places 1..n from left to right.
A clue is a tuple; positions are 0-based internally, 1-based in print.
"""
from itertools import permutations
import numpy as np

KINDS = ["at", "notat", "end", "notend", "even", "adj", "notadj", "left1", "before", "gap", "between"]
_PERMS = {}

def perms(n):
    if n not in _PERMS:
        _PERMS[n] = np.array(list(permutations(range(n))), dtype=np.int8)  # row: pos of person i
    return _PERMS[n]

def holds(c, pos, n):
    t = c[0]
    if t == "at": return pos[c[1]] == c[2]
    if t == "notat": return pos[c[1]] != c[2]
    if t == "end": return pos[c[1]] in (0, n - 1)
    if t == "notend": return pos[c[1]] not in (0, n - 1)
    if t == "even": return ((pos[c[1]] + 1) % 2 == 0) == c[2]
    if t == "adj": return abs(pos[c[1]] - pos[c[2]]) == 1
    if t == "notadj": return abs(pos[c[1]] - pos[c[2]]) != 1
    if t == "left1": return pos[c[1]] + 1 == pos[c[2]]
    if t == "before": return pos[c[1]] < pos[c[2]]
    if t == "gap": return abs(pos[c[1]] - pos[c[2]]) == c[3] + 1
    if t == "between": return min(pos[c[2]], pos[c[3]]) < pos[c[1]] < max(pos[c[2]], pos[c[3]])
    raise ValueError(c)

def sat_vec(c, n):
    P = perms(n).astype(int)
    t = c[0]
    if t == "at": return P[:, c[1]] == c[2]
    if t == "notat": return P[:, c[1]] != c[2]
    if t == "end": return (P[:, c[1]] == 0) | (P[:, c[1]] == n - 1)
    if t == "notend": return (P[:, c[1]] != 0) & (P[:, c[1]] != n - 1)
    if t == "even": return ((P[:, c[1]] + 1) % 2 == 0) == c[2]
    if t == "adj": return np.abs(P[:, c[1]] - P[:, c[2]]) == 1
    if t == "notadj": return np.abs(P[:, c[1]] - P[:, c[2]]) != 1
    if t == "left1": return P[:, c[1]] + 1 == P[:, c[2]]
    if t == "before": return P[:, c[1]] < P[:, c[2]]
    if t == "gap": return np.abs(P[:, c[1]] - P[:, c[2]]) == c[3] + 1
    if t == "between":
        a, b, x = P[:, c[2]], P[:, c[3]], P[:, c[1]]
        return (np.minimum(a, b) < x) & (x < np.maximum(a, b))
    raise ValueError(c)

def count_solutions(n, vecs):
    m = np.ones(len(perms(n)), bool)
    for v in vecs: m &= v
    return int(m.sum()), m

class Solver:
    """Step ladder. Depth 0: for each clue in turn, keep only the places each person can
    still take in some full line-up that fits the clue and every known 'can only be in' set.
    Depth d: suppose person p takes place k; if depth d-1 reaches a clash, strike k from p.
    Canonical order: people in cast order, places low to high, restart after each strike."""
    def __init__(s, n, clues):
        s.n = n; s.P = perms(n); s.clues = clues
        s.vecs = [sat_vec(c, n) for c in clues]
        s.trace = []

    def boxmask(s, D):
        m = np.ones(len(s.P), bool)
        for p in range(s.n):
            allowed = np.zeros(s.n, bool); allowed[list(D[p])] = True
            m &= allowed[s.P[:, p]]
        return m

    def step0(s, D, trace=None):
        D = [set(d) for d in D]
        while True:
            changed = False
            for ci, v in enumerate(s.vecs):
                local = s.boxmask(D) & v
                if not local.any(): return None
                sub = s.P[local]
                for p in range(s.n):
                    seen = set(np.unique(sub[:, p]).tolist())
                    if seen != D[p]:
                        if trace is not None and len(seen) == 1 and len(D[p]) > 1:
                            trace.append((ci, p, next(iter(seen))))
                        D[p] = seen; changed = True
            if not changed: return D

    def ladder(s, D, d, log=None):
        D = s.step0(D)
        if D is None or d == 0: return D
        while any(len(x) > 1 for x in D):
            found = False
            for p in range(s.n):
                if len(D[p]) < 2: continue
                for k in sorted(D[p]):
                    trial = [set(x) for x in D]; trial[p] = {k}
                    if s.ladder(trial, d - 1) is None:
                        if log is not None: log.append((p, k))
                        D[p].discard(k)
                        D = s.step0(D)
                        if D is None: return None
                        found = True; break
                if found: break
            if not found: break
        return D

    def measure(s, maxd=2):
        full = [set(range(s.n)) for _ in range(s.n)]
        for d in range(maxd + 1):
            log = []
            D = s.ladder(full, d, log)
            if D is not None and all(len(x) == 1 for x in D):
                return d, log
        return None, None

    def first_step(s):
        full = [set(range(s.n)) for _ in range(s.n)]
        tr = []
        s.step0(full, tr)
        for ci, p, k in tr:  # first pin that does not just repeat a "has place k" clue
            if not (s.clues[ci][0] == "at" and s.clues[ci][1] == p):
                return ci, p, k
        return tr[0] if tr else None
