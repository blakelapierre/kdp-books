"""5x5 Latin-square puzzles: Futoshiki, Skyscrapers ("Chimneys") and Calcudoku ("Cookie Tins").
Uniqueness is checked by filtering ALL 161,280 5x5 Latin squares (numpy), so the count is exact."""
import itertools, random
import numpy as np
from functools import lru_cache

N = 5

@lru_cache(None)
def all_squares():
    perms = list(itertools.permutations(range(1, N + 1)))
    out = []
    def rec(rows):
        if len(rows) == N: out.append(sum(rows, ())); return
        for p in perms:
            if all(p[i] != r[i] for r in rows for i in range(N)): rec(rows + [p])
    rec([])
    A = np.array(out, dtype=np.int8)
    assert A.shape == (161280, 25)
    return A

def cell(r, c): return r * N + c

# ---------------- Futoshiki: givens + inequalities between neighbours
def futo_mask(A, givens, ineq):
    m = np.ones(len(A), bool)
    for (r, c), v in givens.items(): m &= A[:, cell(r, c)] == v
    for (a, b) in ineq: m &= A[:, cell(*a)] < A[:, cell(*b)]      # a < b
    return m

def gen_futoshiki(seed):
    rnd = random.Random(seed); A = all_squares()
    sol = A[rnd.randrange(len(A))]
    pairs = [((r, c), (r, c + 1)) for r in range(N) for c in range(N - 1)] + [((r, c), (r + 1, c)) for r in range(N - 1) for c in range(N)]
    ineq = [(a, b) if sol[cell(*a)] < sol[cell(*b)] else (b, a) for a, b in pairs]
    givens = {}
    rnd.shuffle(ineq)
    keep = list(ineq)
    for q in list(ineq):
        if len(keep) <= 14: break
        t = [x for x in keep if x != q]
        if futo_mask(A, givens, t).sum() == 1: keep = t
    # add a couple of givens then drop more inequalities, for a friendlier mix
    for _ in range(2):
        r, c = rnd.randrange(N), rnd.randrange(N); givens[(r, c)] = int(sol[cell(r, c)])
    for q in list(keep):
        if len(keep) <= 11: break
        t = [x for x in keep if x != q]
        if futo_mask(A, givens, t).sum() == 1: keep = t
    for g in list(givens):
        t = {k: v for k, v in givens.items() if k != g}
        if futo_mask(A, t, keep).sum() == 1: givens = t
    assert futo_mask(A, givens, keep).sum() == 1
    return dict(givens={f"{r},{c}": v for (r, c), v in givens.items()}, ineq=[[list(a), list(b)] for a, b in keep],
                solution=sol.reshape(N, N).tolist())

# ---------------- Skyscrapers: edge clues = how many towers are visible
def visible(line):
    m = 0; k = 0
    for h in line:
        if h > m: m = h; k += 1
    return k

@lru_cache(None)
def vis_table():
    A = all_squares().reshape(-1, N, N)
    def vis(X):  # X: (..., N) -> visible count
        mx = np.maximum.accumulate(X, axis=-1)
        return 1 + (np.diff(mx, axis=-1) > 0).sum(-1)
    T = {}
    for i in range(N):
        T[("top", i)] = vis(A[:, :, i]); T[("bottom", i)] = vis(A[:, ::-1, i])
        T[("left", i)] = vis(A[:, i, :]); T[("right", i)] = vis(A[:, i, ::-1])
    return T

def sky_mask(clues, givens):
    A = all_squares(); T = vis_table(); m = np.ones(len(A), bool)
    for k, v in clues.items(): m &= T[k] == v
    for (r, c), v in givens.items(): m &= A[:, cell(r, c)] == v
    return m

def gen_skyscrapers(seed):
    rnd = random.Random(seed); A = all_squares(); T = vis_table()
    idx = rnd.randrange(len(A)); sol = A[idx]
    clues = {k: int(T[k][idx]) for k in T}
    keys = list(clues); rnd.shuffle(keys)
    for k in keys:
        if len(clues) <= 11: break
        t = {a: b for a, b in clues.items() if a != k}
        if sky_mask(t, {}).sum() == 1: clues = t
    assert sky_mask(clues, {}).sum() == 1
    return dict(clues={f"{a},{b}": v for (a, b), v in clues.items()}, solution=sol.reshape(N, N).tolist())

# ---------------- Calcudoku: cages with a target and an operation
def cage_ok_vec(A, cells, op, target):
    V = A[:, [cell(*x) for x in cells]].astype(np.int32)
    if op == "+": return V.sum(1) == target
    if op == "×": return V.prod(1) == target
    if op == "−": return np.abs(V[:, 0] - V[:, 1]) == target
    if op == "÷": return (np.maximum(V[:, 0], V[:, 1]) == target * np.minimum(V[:, 0], V[:, 1]))
    if op == "": return V[:, 0] == target

def gen_calcudoku(seed):
    rnd = random.Random(seed); A = all_squares()
    for attempt in range(2000):
        idx = rnd.randrange(len(A)); sol = A[idx].reshape(N, N)
        cells = [(r, c) for r in range(N) for c in range(N)]; free = set(cells); cages = []
        order = cells[:]; rnd.shuffle(order)
        for x in order:
            if x not in free: continue
            size = rnd.choice([1, 2, 2, 2, 3, 3, 3, 4]) if len(cages) else 2
            cg = [x]; free.discard(x)
            while len(cg) < size:
                nb = [(a + dr, b + dc) for a, b in cg for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)) if (a + dr, b + dc) in free]
                if not nb: break
                y = rnd.choice(nb); cg.append(y); free.discard(y)
            cages.append(cg)
        if sum(1 for c in cages if len(c) == 1) > 2: continue
        spec = []
        for cg in cages:
            vals = [int(sol[a][b]) for a, b in cg]
            if len(cg) == 1: spec.append((cg, "", vals[0])); continue
            if len(cg) == 2:
                hi, lo = max(vals), min(vals)
                if hi % lo == 0 and rnd.random() < 0.5: spec.append((cg, "÷", hi // lo)); continue
                if rnd.random() < 0.5: spec.append((cg, "−", hi - lo)); continue
            if rnd.random() < 0.3: spec.append((cg, "×", int(np.prod(vals))))
            else: spec.append((cg, "+", sum(vals)))
        m = np.ones(len(A), bool)
        for cg, op, t in spec: m &= cage_ok_vec(A, cg, op, t)
        if m.sum() == 1:
            assert (A[m][0] == A[idx]).all()
            return dict(cages=[dict(cells=[list(x) for x in cg], op=op, target=t) for cg, op, t in spec], solution=sol.tolist())
    raise RuntimeError("no calcudoku")
