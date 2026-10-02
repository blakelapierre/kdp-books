"""Generators for the grid puzzles: Queens (stars), Wordoku, Snowmen & Pines (Tents), Lanterns (Akari),
Hidden Presents (Minesweeper-style) and the Sleigh Fleet (Battleships). Each returns a dict with the
puzzle, its unique solution, and a SAT-based uniqueness check (count == 1)."""
import random
from satutil import CNF

N8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
N4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# ---------------------------------------------------------------- Queens / stars
def queens_count(n, regions, limit=2):
    f = CNF(); X = lambda r, c: f.v("q", r, c)
    for i in range(n):
        f.eq([X(i, c) for c in range(n)], 1); f.eq([X(r, i) for r in range(n)], 1)
    for g in set(regions.values()):
        f.eq([X(r, c) for (r, c), k in regions.items() if k == g], 1)
    for r in range(n):
        for c in range(n):
            for dr, dc in N8:
                rr, cc = r + dr, c + dc
                if 0 <= rr < n and 0 <= cc < n and (rr, cc) > (r, c): f.add([-X(r, c), -X(rr, cc)])
    return f.solutions([("q", r, c) for r in range(n) for c in range(n)], limit)

def _connected(cells):
    cells = set(cells)
    if not cells: return True
    st = [next(iter(cells))]; seen = {st[0]}
    while st:
        r, c = st.pop()
        for dr, dc in N4:
            x = (r + dr, c + dc)
            if x in cells and x not in seen: seen.add(x); st.append(x)
    return len(seen) == len(cells)

def gen_queens(n, seed, tries=300):
    rnd = random.Random(seed)
    while True:
        perm = list(range(n)); rnd.shuffle(perm)
        if any(abs(perm[i] - perm[i + 1]) <= 1 for i in range(n - 1)): continue
        stars = [(r, perm[r]) for r in range(n)]
        reg = {s: i for i, s in enumerate(stars)}
        free = [(r, c) for r in range(n) for c in range(n) if (r, c) not in reg]
        while free:
            rnd.shuffle(free)
            for cell in list(free):
                nb = [reg[(cell[0] + dr, cell[1] + dc)] for dr, dc in N4 if (cell[0] + dr, cell[1] + dc) in reg]
                if nb:
                    sizes = {g: sum(1 for v in reg.values() if v == g) for g in set(nb)}
                    reg[cell] = min(sizes, key=lambda g: sizes[g] + rnd.random() * 3); free.remove(cell)
        # repair: move cells used by alternative solutions into a neighbouring region
        for it in range(tries):
            sols = queens_count(n, reg)
            if len(sols) == 1: break
            alt = [s for s in sols if sorted((r, c) for (_, r, c) in s) != sorted(stars)][0]
            bad = [(r, c) for (_, r, c) in alt if (r, c) not in stars]
            rnd.shuffle(bad); moved = False
            for x in bad:
                g0 = reg[x]
                opts = list({reg[(x[0] + dr, x[1] + dc)] for dr, dc in N4 if (x[0] + dr, x[1] + dc) in reg} - {g0})
                rnd.shuffle(opts)
                for g in opts:
                    rest = [y for y, k in reg.items() if k == g0 and y != x]
                    if _connected(rest):
                        reg[x] = g; moved = True; break
                if moved: break
            if not moved: break
        sols = queens_count(n, reg)
        if len(sols) == 1:
            sol = sorted((r, c) for (_, r, c) in sols[0])
            assert sol == sorted(stars)
            assert all(_connected([y for y, k in reg.items() if k == g]) for g in range(n))
            return dict(n=n, regions=[[reg[(r, c)] for c in range(n)] for r in range(n)], stars=sol)

# ---------------------------------------------------------------- Wordoku (sudoku with letters)
def sudoku_count(n, br, bc, givens, limit=2):
    f = CNF(); X = lambda r, c, d: f.v("s", r, c, d)
    for r in range(n):
        for c in range(n): f.eq([X(r, c, d) for d in range(n)], 1)
    for d in range(n):
        for i in range(n):
            f.eq([X(i, c, d) for c in range(n)], 1); f.eq([X(r, i, d) for r in range(n)], 1)
        for R in range(0, n, br):
            for C in range(0, n, bc):
                f.eq([X(R + a, C + b, d) for a in range(br) for b in range(bc)], 1)
    for (r, c), d in givens.items(): f.add([X(r, c, d)])
    return f.solutions([("s", r, c, d) for r in range(n) for c in range(n) for d in range(n)], limit)

def singles_solve(n, br, bc, givens):
    """Naked + hidden singles only. Returns the filled grid or None if it gets stuck."""
    g = dict(givens)
    units = [[(r, c) for c in range(n)] for r in range(n)] + [[(r, c) for r in range(n)] for c in range(n)]
    units += [[(R + a, C + b) for a in range(br) for b in range(bc)] for R in range(0, n, br) for C in range(0, n, bc)]
    peers = {(r, c): set(x for u in units if (r, c) in u for x in u) - {(r, c)} for r in range(n) for c in range(n)}
    while len(g) < n * n:
        cand = {x: set(range(n)) - {g[p] for p in peers[x] if p in g} for x in peers if x not in g}
        prog = False
        for x, cs in cand.items():
            if not cs: return None
            if len(cs) == 1: g[x] = next(iter(cs)); prog = True; break
        if prog: continue
        for u in units:
            for d in range(n):
                spots = [x for x in u if x not in g and d in cand[x]]
                if len(spots) == 1 and not any(g.get(x) == d for x in u): g[spots[0]] = d; prog = True; break
            if prog: break
        if not prog: return None
    return g

def gen_wordoku(n, br, bc, seed, target):
    rnd = random.Random(seed)
    # random full grid by shuffling a pattern grid
    base = [[(bc * (r % br) + r // br + c) % n for c in range(n)] for r in range(n)]
    for _ in range(40):
        # swap rows within band, cols within stack, bands, stacks, relabel
        b = rnd.randrange(n // br); i, j = rnd.sample(range(br), 2); base[b * br + i], base[b * br + j] = base[b * br + j], base[b * br + i]
        s = rnd.randrange(n // bc); i, j = rnd.sample(range(bc), 2)
        for row in base: row[s * bc + i], row[s * bc + j] = row[s * bc + j], row[s * bc + i]
    lab = list(range(n)); rnd.shuffle(lab)
    full = {(r, c): lab[base[r][c]] for r in range(n) for c in range(n)}
    assert len(sudoku_count(n, br, bc, full)) == 1
    giv = dict(full); cells = list(full); rnd.shuffle(cells)
    for x in cells:
        if len(giv) <= target: break
        t = dict(giv); del t[x]
        if singles_solve(n, br, bc, t) and len(sudoku_count(n, br, bc, t)) == 1: giv = t
    return dict(n=n, br=br, bc=bc, givens=giv, full=full)

# ---------------------------------------------------------------- Tents (snowmen next to pines)
def tents_count(n, trees, rows, cols, givens_empty=(), limit=2):
    f = CNF(); T = lambda r, c: f.v("t", r, c); M = lambda t, r, c: f.v("m", t, r, c)
    tset = set(trees)
    inb = lambda r, c: 0 <= r < n and 0 <= c < n
    into = {}
    for i, (r, c) in enumerate(trees):
        nbs = [(r + dr, c + dc) for dr, dc in N4 if inb(r + dr, c + dc) and (r + dr, c + dc) not in tset]
        f.eq([M(i, *x) for x in nbs], 1)
        for x in nbs: f.add([-M(i, *x), T(*x)]); into.setdefault(x, []).append(M(i, *x))
    for r in range(n):
        for c in range(n):
            if (r, c) in tset: f.add([-T(r, c)]); continue
            ms = into.get((r, c), [])
            if not ms: f.add([-T(r, c)])
            else:
                f.add([-T(r, c)] + ms); f.atmost(ms, 1)
            for dr, dc in N8:
                rr, cc = r + dr, c + dc
                if inb(rr, cc) and (rr, cc) > (r, c): f.add([-T(r, c), -T(rr, cc)])
    for i in range(n):
        f.eq([T(i, c) for c in range(n)], rows[i]); f.eq([T(r, i) for r in range(n)], cols[i])
    for x in givens_empty: f.add([-T(*x)])
    return f.solutions([("t", r, c) for r in range(n) for c in range(n)], limit)

def gen_tents(n, k, seed):
    rnd = random.Random(seed)
    inb = lambda r, c: 0 <= r < n and 0 <= c < n
    while True:
        tents = set(); trees = []; used = set()
        for _ in range(3000):
            if len(tents) == k: break
            r, c = rnd.randrange(n), rnd.randrange(n)
            if (r, c) in used or any((r + dr, c + dc) in tents for dr, dc in N8): continue
            opts = [(r + dr, c + dc) for dr, dc in N4 if inb(r + dr, c + dc) and (r + dr, c + dc) not in used and (r + dr, c + dc) not in tents]
            opts = [o for o in opts if not any((o[0] + dr, o[1] + dc) in tents for dr, dc in []) ]
            if not opts: continue
            t = rnd.choice(opts)
            tents.add((r, c)); trees.append(t); used |= {(r, c), t}
        if len(tents) != k: continue
        rows = [sum(1 for (r, c) in tents if r == i) for i in range(n)]
        cols = [sum(1 for (r, c) in tents if c == i) for i in range(n)]
        sols = tents_count(n, trees, rows, cols)
        if len(sols) == 1:
            got = sorted((r, c) for (_, r, c) in sols[0]); assert got == sorted(tents)
            return dict(n=n, trees=sorted(trees), rows=rows, cols=cols, tents=got)

# ---------------------------------------------------------------- Akari (lanterns)
def segs(n, black):
    """maximal horizontal & vertical white segments"""
    out = []
    for r in range(n):
        cur = []
        for c in range(n + 1):
            if c < n and (r, c) not in black: cur.append((r, c))
            else:
                if cur: out.append(cur)
                cur = []
    for c in range(n):
        cur = []
        for r in range(n + 1):
            if r < n and (r, c) not in black: cur.append((r, c))
            else:
                if cur: out.append(cur)
                cur = []
    return out

def akari_count(n, black, nums, limit=2):
    f = CNF(); B = lambda r, c: f.v("b", r, c)
    S = segs(n, black)
    for s in S: f.atmost([B(*x) for x in s], 1)
    for r in range(n):
        for c in range(n):
            if (r, c) in black: f.add([-B(r, c)]); continue
            vis = set(x for s in S if (r, c) in s for x in s)
            f.add([B(*x) for x in vis])
    for (r, c), k in nums.items():
        nb = [(r + dr, c + dc) for dr, dc in N4 if 0 <= r + dr < n and 0 <= c + dc < n and (r + dr, c + dc) not in black]
        f.eq([B(*x) for x in nb], k) if nb else None
        if not nb: assert k == 0
    return f.solutions([("b", r, c) for r in range(n) for c in range(n)], limit)

def gen_akari(n, want, seed, dens=0.2):
    rnd = random.Random(seed)
    while True:
        black = set()
        for r in range(n):
            for c in range(n):
                if rnd.random() < dens and (r, c) not in black: black.add((r, c)); black.add((n - 1 - r, n - 1 - c))
        S = segs(n, black)
        white = [(r, c) for r in range(n) for c in range(n) if (r, c) not in black]
        bulbs = set(); lit = set(); order = white[:]; rnd.shuffle(order)
        for x in order:
            if x in lit: continue
            bulbs.add(x); lit |= set(y for s in S if x in s for y in s)
        if len(bulbs) != want: continue
        nb = lambda r, c: [(r + dr, c + dc) for dr, dc in N4 if (r + dr, c + dc) in bulbs]
        nums = {b: len(nb(*b)) for b in black}
        if len(akari_count(n, black, nums)) != 1: continue
        keys = list(nums); rnd.shuffle(keys)
        for k in keys:
            t = dict(nums); del t[k]
            if len(akari_count(n, black, t)) == 1: nums = t
        sol = akari_count(n, black, nums)
        assert len(sol) == 1 and sorted((r, c) for (_, r, c) in sol[0]) == sorted(bulbs)
        return dict(n=n, black=sorted(black), nums={f"{r},{c}": k for (r, c), k in nums.items()}, bulbs=sorted(bulbs))

# ---------------------------------------------------------------- Hidden presents (minesweeper-style)
def presents_count(n, clues, total, limit=2):
    f = CNF(); P = lambda r, c: f.v("p", r, c)
    for (r, c), k in clues.items():
        f.add([-P(r, c)])
        f.eq([P(r + dr, c + dc) for dr, dc in N8 if 0 <= r + dr < n and 0 <= c + dc < n], k)
    f.eq([P(r, c) for r in range(n) for c in range(n)], total)
    return f.solutions([("p", r, c) for r in range(n) for c in range(n)], limit)

def gen_presents(n, k, seed):
    rnd = random.Random(seed)
    while True:
        cells = [(r, c) for r in range(n) for c in range(n)]
        pres = set(rnd.sample(cells, k))
        if any(sum((r + dr, c + dc) in pres for dr, dc in N8) >= 4 for (r, c) in pres): continue
        clues = {x: sum((x[0] + dr, x[1] + dc) in pres for dr, dc in N8) for x in cells if x not in pres}
        keys = list(clues); rnd.shuffle(keys)
        for x in keys:
            t = dict(clues); del t[x]
            if len(presents_count(n, t, k)) == 1: clues = t
        sol = presents_count(n, clues, k)
        assert len(sol) == 1 and sorted((r, c) for (_, r, c) in sol[0]) == sorted(pres)
        if len(clues) < n * n * 0.33: continue      # keep it gentle: enough numbers to work from
        return dict(n=n, total=k, clues={f"{r},{c}": v for (r, c), v in clues.items()}, presents=sorted(pres))

# ---------------------------------------------------------------- Sleigh fleet (battleships)
def fleet_count(n, fleet, rows, cols, given_ship=(), given_sea=(), limit=2):
    f = CNF(); S = lambda r, c: f.v("x", r, c)
    places = []
    for L in sorted(set(fleet)):
        for r in range(n):
            for c in range(n):
                for dr, dc in ((0, 1), (1, 0)) if L > 1 else ((0, 1),):
                    cells = [(r + dr * i, c + dc * i) for i in range(L)]
                    if all(0 <= a < n and 0 <= b < n for a, b in cells): places.append((L, tuple(cells)))
    P = [f.v("pl", i) for i in range(len(places))]
    cover = {}
    for i, (L, cells) in enumerate(places):
        for x in cells: cover.setdefault(x, []).append(P[i])
    for r in range(n):
        for c in range(n):
            cv = cover.get((r, c), [])
            f.add([-S(r, c)] + cv); f.atmost(cv, 1)
            for p in cv: f.add([-p, S(r, c)])
    for L in set(fleet): f.eq([P[i] for i, (l, _) in enumerate(places) if l == L], fleet.count(L))
    # no touching (even diagonally) between different ships: a ship's cells + halo are otherwise empty
    for i, (L, cells) in enumerate(places):
        cs = set(cells)
        halo = set((a + dr, b + dc) for a, b in cells for dr, dc in N8) - cs
        for h in halo:
            if 0 <= h[0] < n and 0 <= h[1] < n: f.add([-P[i], -S(*h)])
    for i in range(n):
        f.eq([S(i, c) for c in range(n)], rows[i]); f.eq([S(r, i) for r in range(n)], cols[i])
    for x in given_ship: f.add([S(*x)])
    for x in given_sea: f.add([-S(*x)])
    return f.solutions([("x", r, c) for r in range(n) for c in range(n)], limit)

def gen_fleet(n, fleet, seed):
    rnd = random.Random(seed)
    while True:
        occ = set(); ships = []
        ok = True
        for L in sorted(fleet, reverse=True):
            for _ in range(500):
                h = rnd.random() < 0.5
                r, c = rnd.randrange(n), rnd.randrange(n)
                cells = [(r, c + i) if h else (r + i, c) for i in range(L)]
                if not all(0 <= a < n and 0 <= b < n for a, b in cells): continue
                if any((a + dr, b + dc) in occ for a, b in cells for dr, dc in N8 + [(0, 0)]): continue
                occ |= set(cells); ships.append(cells); break
            else: ok = False; break
        if not ok: continue
        rows = [sum(1 for (r, c) in occ if r == i) for i in range(n)]
        cols = [sum(1 for (r, c) in occ if c == i) for i in range(n)]
        gs, gw = [], []
        cells = [(r, c) for r in range(n) for c in range(n)]; rnd.shuffle(cells)
        while len(fleet_count(n, fleet, rows, cols, gs, gw)) > 1:
            x = cells.pop()
            (gs if x in occ else gw).append(x)
        # minimise givens
        for x in list(gs + gw):
            a = [y for y in gs if y != x]; b = [y for y in gw if y != x]
            if len(fleet_count(n, fleet, rows, cols, a, b)) == 1: gs, gw = a, b
        sol = fleet_count(n, fleet, rows, cols, gs, gw)
        assert len(sol) == 1 and sorted((r, c) for (_, r, c) in sol[0]) == sorted(occ)
        return dict(n=n, fleet=fleet, rows=rows, cols=cols, given_ship=sorted(gs), given_sea=sorted(gw),
                    ships=[sorted(s) for s in ships], cells=sorted(occ))
