"""Logic-grid engine for Logic on Lantern Lane.

A puzzle has k categories of n items. Category 0 is the key (usually names). An "item" is a pair
(category, index). The solution sol[c][e] gives the item index of category c held by entity e
(entity e is the key item e, so sol[0] is the identity).

Clue types (all stored as plain dicts so they go straight into data.json):
  pos     a is b                                  {"t":"pos","a":[c,i],"b":[c,j]}
  neg     a is not b                              {"t":"neg", ...}
  lt      a's value in ordered category o is lower than b's  (optionally by exactly d steps)
                                                  {"t":"lt","a":..,"b":..,"o":c,"d":None|int}
  either  a is exactly one of b, c                {"t":"either","a":..,"b":..,"c":..}
  neither neither a nor b is c                    {"t":"neither","a":..,"b":..,"c":..}
  pair    of a and b, one is c and the other is d (c, d in the same category)
                                                  {"t":"pair","a":..,"b":..,"c":..,"d":..}

The solver below is a human-style grid solver: it only ever crosses out or ticks cells of the
standard logic grid, using the clues one at a time plus the two grid rules everybody uses
(one tick per row/column, and carrying ticks/crosses between grids). It never guesses.
A puzzle is accepted only if this solver fills the whole grid.
"""
from __future__ import annotations
import itertools
import numpy as np


def ent_of(sol, c, i):
    """Entity holding item i of category c."""
    return sol[c].index(i)


def holds(cl, sol, cats):
    """True if clue cl is true for solution sol (used by the generator and by verify)."""
    E = lambda it: ent_of(sol, it[0], it[1])
    t = cl["t"]
    if t == "pos":
        return E(cl["a"]) == E(cl["b"])
    if t == "neg":
        return E(cl["a"]) != E(cl["b"])
    if t == "lt":
        o = cl["o"]
        va = sol[o][E(cl["a"])]
        vb = sol[o][E(cl["b"])]
        return vb - va == cl["d"] if cl.get("d") else va < vb
    if t == "either":
        x = E(cl["a"])
        return (x == E(cl["b"])) != (x == E(cl["c"]))
    if t == "neither":
        return E(cl["a"]) != E(cl["c"]) and E(cl["b"]) != E(cl["c"])
    if t == "pair":
        a, b, c, d = E(cl["a"]), E(cl["b"]), E(cl["c"]), E(cl["d"])
        return a != b and {a, b} == {c, d}
    raise ValueError(t)


class Contradiction(Exception):
    pass


class Grid:
    """M[(i,j)] for i<j is an n x n boolean array: True = still possible."""

    def __init__(s, k, n):
        s.k, s.n = k, n
        s.M = {(i, j): np.ones((n, n), dtype=bool) for i in range(k) for j in range(i + 1, k)}

    def copy(s):
        g = Grid.__new__(Grid)
        g.k, g.n = s.k, s.n
        g.M = {key: v.copy() for key, v in s.M.items()}
        return g

    def mat(s, i, j):
        """View with rows = items of i, columns = items of j."""
        return s.M[(i, j)] if i < j else s.M[(j, i)].T

    def possible(s, x, y):
        if x[0] == y[0]:
            return x[1] == y[1]
        return bool(s.mat(x[0], y[0])[x[1], y[1]])

    def certain(s, x, y):
        if x[0] == y[0]:
            return x[1] == y[1]
        row = s.mat(x[0], y[0])[x[1]]
        return bool(row[y[1]]) and row.sum() == 1

    def cross(s, x, y):
        if x[0] == y[0]:
            if x[1] == y[1]:
                raise Contradiction
            return False
        m = s.mat(x[0], y[0])
        if m[x[1], y[1]]:
            m[x[1], y[1]] = False
            return True
        return False

    def tick(s, x, y):
        if x[0] == y[0]:
            if x[1] != y[1]:
                raise Contradiction
            return False
        m = s.mat(x[0], y[0])
        if not m[x[1], y[1]]:
            raise Contradiction
        ch = m[x[1]].sum() > 1 or m[:, y[1]].sum() > 1
        m[x[1], :] = False
        m[:, y[1]] = False
        m[x[1], y[1]] = True
        return ch

    def values(s, x, o):
        """Item indices of ordered category o still possible for item x."""
        if x[0] == o:
            return {x[1]}
        return set(np.nonzero(s.mat(x[0], o)[x[1]])[0].tolist())

    def solved(s):
        return all(m.sum() == s.n for m in s.M.values())

    def check(s):
        for m in s.M.values():
            if not m.any(axis=1).all() or not m.any(axis=0).all():
                raise Contradiction

    # ---------------------------------------------------------------- grid rules
    def singles(s):
        ch = False
        for m in s.M.values():
            for r in range(s.n):
                nz = np.nonzero(m[r])[0]
                if len(nz) == 0:
                    raise Contradiction
                if len(nz) == 1 and m[:, nz[0]].sum() > 1:
                    m[:, nz[0]] = False
                    m[r, nz[0]] = True
                    ch = True
            for cidx in range(s.n):
                nz = np.nonzero(m[:, cidx])[0]
                if len(nz) == 0:
                    raise Contradiction
                if len(nz) == 1 and m[nz[0]].sum() > 1:
                    m[nz[0], :] = False
                    m[nz[0], cidx] = True
                    ch = True
        return ch

    def transfer(s):
        """Carry information between grids: x-z is possible only if some y of a third category
        is possible with both x and z (ticks and crosses move across the grid this way)."""
        ch = False
        for i, j, l in itertools.permutations(range(s.k), 3):
            if not (i < l):
                continue
            a = s.mat(i, j).astype(np.uint8)
            b = s.mat(j, l).astype(np.uint8)
            reach = (a @ b) > 0
            m = s.M[(i, l)]
            new = m & reach
            if (new != m).any():
                s.M[(i, l)] = new
                ch = True
        return ch


def apply_clue(g, cl):
    """Use one clue on the grid. Returns True if anything changed."""
    t = cl["t"]
    a = tuple(cl["a"]); b = tuple(cl["b"])
    ch = False
    if t == "pos":
        return g.tick(a, b)
    if t == "neg":
        return g.cross(a, b)
    if t == "lt":
        o, d = cl["o"], cl.get("d")
        if a[0] != b[0]:
            ch |= g.cross(a, b)
        A, B = g.values(a, o), g.values(b, o)
        okA = {v for v in A if any((w - v == d) if d else (w > v) for w in B)}
        okB = {w for w in B if any((w - v == d) if d else (w > v) for v in okA)}
        if not okA or not okB:
            raise Contradiction
        for x, S, ok in ((a, A, okA), (b, B, okB)):
            for v in S - ok:
                ch |= g.cross(x, (o, v))
        return ch
    if t == "either":
        c = tuple(cl["c"])
        if b[0] != c[0]:
            ch |= g.cross(b, c)
        pb, pc = g.possible(a, b), g.possible(a, c)
        if not pb and not pc:
            raise Contradiction
        if not pb:
            ch |= g.tick(a, c)
        elif not pc:
            ch |= g.tick(a, b)
        elif g.certain(a, b):
            ch |= g.cross(a, c)
        elif g.certain(a, c):
            ch |= g.cross(a, b)
        return ch
    if t == "neither":
        c = tuple(cl["c"])
        return g.cross(a, c) | g.cross(b, c)
    if t == "pair":
        c, d = tuple(cl["c"]), tuple(cl["d"])
        if a[0] != b[0]:
            ch |= g.cross(a, b)
        cc = c[0]
        for x in (a, b):
            for v in range(g.n):
                if v not in (c[1], d[1]):
                    ch |= g.cross(x, (cc, v))
        # if a is not c, then a is d and b is c (and the three symmetric cases)
        if not g.possible(a, c):
            ch |= g.tick(a, d) | g.tick(b, c)
        if not g.possible(a, d):
            ch |= g.tick(a, c) | g.tick(b, d)
        if not g.possible(b, c):
            ch |= g.tick(b, d) | g.tick(a, c)
        if not g.possible(b, d):
            ch |= g.tick(b, c) | g.tick(a, d)
        return ch
    raise ValueError(t)


def propagate(g, clues, max_rounds=200):
    """Run clues + grid rules to a fixed point. Returns number of rounds. Raises Contradiction."""
    rounds = 0
    while rounds < max_rounds:
        rounds += 1
        ch = False
        for cl in clues:
            ch |= apply_clue(g, cl)
        ch |= g.singles()
        ch |= g.transfer()
        g.check()
        if not ch:
            break
    return rounds


def solve(k, n, clues):
    """Human-style solve. Returns (grid, solved?, rounds)."""
    g = Grid(k, n)
    try:
        r = propagate(g, clues)
    except Contradiction:
        return g, False, -1
    return g, g.solved(), r


def grid_solution(g):
    """Read sol[c][e] from a solved grid."""
    k, n = g.k, g.n
    sol = [list(range(n))]
    for c in range(1, k):
        m = g.mat(0, c)
        sol.append([int(np.nonzero(m[e])[0][0]) for e in range(n)])
    return sol
