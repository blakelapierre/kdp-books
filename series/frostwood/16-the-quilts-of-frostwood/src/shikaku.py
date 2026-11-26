"""Quilts (Shikaku) puzzle model and the generator's step-by-step logic solver.

A puzzle is p = dict(n=grid size, clues=[[row, col, area], ...], sol=[[clue index per cell]], rects=[[r0, c0, h, w] per clue]).
Rules: split the square grid into rectangles (the quilt's patches) so that every patch holds exactly
one number and that number is the patch's area (its count of squares).

Logic tiers used for grading (the solver never guesses unless T3 is allowed):
 T1: a number with only one possible patch left takes it; a square that only one possible patch can
     still cover takes that patch.
 T2: + a square that only one number can still reach belongs to that number (its patches must cover it);
     squares inside every possible patch of a number belong to that number (no other patch may use them).
 T3: + what-if: pencil in one possible patch, follow T2 until something breaks, then cross that patch out.
"""
TIERS = {1: "single patch for a number, single patch for a square",
         2: "+ only-one-number squares and shared squares of all a number's patches",
         3: "+ what-if tries"}


def candidates(n, clues):
    """All rectangles for each clue: area = number, inside the grid, containing its clue and no other clue."""
    where = {(r, c): i for i, (r, c, a) in enumerate(clues)}
    out = []
    for i, (r, c, a) in enumerate(clues):
        lst = []
        for h in range(1, a + 1):
            if a % h: continue
            w = a // h
            if h > n or w > n: continue
            for r0 in range(max(0, r - h + 1), min(r, n - h) + 1):
                for c0 in range(max(0, c - w + 1), min(c, n - w) + 1):
                    cells = frozenset((rr, cc) for rr in range(r0, r0 + h) for cc in range(c0, c0 + w))
                    if any(where.get(x, i) != i for x in cells): continue
                    lst.append(((r0, c0, h, w), cells))
        out.append(lst)
    return out


class Contradiction(Exception): pass


def _propagate(n, cand, tier, stt):
    """In-place deduction with T1 (and T2 if tier >= 2). Raises Contradiction."""
    k = len(cand)
    while True:
        changed = False
        # cover map
        cover = {}
        for i in range(k):
            if not cand[i]: raise Contradiction()
            for j, (_, cells) in enumerate(cand[i]):
                for x in cells: cover.setdefault(x, []).append((i, j))
        if len(cover) < n * n: raise Contradiction()
        # fixed patches claim their squares
        owner = {}
        for i in range(k):
            if len(cand[i]) == 1:
                for x in cand[i][0][1]:
                    if x in owner: raise Contradiction()
                    owner[x] = i
        for i in range(k):
            if len(cand[i]) > 1:
                keep = [rc for rc in cand[i] if not any(owner.get(x, i) != i for x in rc[1])]
                if len(keep) < len(cand[i]): cand[i] = keep; changed = True
                if not keep: raise Contradiction()
        if changed: stt["steps"] += 1; continue
        # T1b: square covered by exactly one candidate patch overall
        for x, lst in cover.items():
            if len(lst) == 1:
                i, j = lst[0]
                if len(cand[i]) > 1: cand[i] = [cand[i][j]]; changed = True; stt["t1"] += 1; break
        if changed: continue
        if tier < 2: return
        # T2a: square reachable from only one number
        for x, lst in cover.items():
            who = {i for i, _ in lst}
            if len(who) == 1:
                i = next(iter(who))
                keep = [rc for rc in cand[i] if x in rc[1]]
                if len(keep) < len(cand[i]): cand[i] = keep; changed = True; stt["t2"] += 1; break
        if changed: continue
        # T2b: squares in every candidate of a number belong to it
        for i in range(k):
            if len(cand[i]) < 2: continue
            core = frozenset.intersection(*[rc[1] for rc in cand[i]])
            for j in range(k):
                if j == i or len(cand[j]) < 1: continue
                keep = [rc for rc in cand[j] if not (rc[1] & core)]
                if len(keep) < len(cand[j]):
                    cand[j] = keep; changed = True; stt["t2"] += 1
                    if not keep: raise Contradiction()
            if changed: break
        if not changed: return


def solve(p, tier, return_state=False, cap=10 ** 9):
    """Logic-only solve. Returns ok (and state, final rects) if return_state."""
    n = p["n"]; clues = p["clues"]
    cand = candidates(n, clues)
    stt = dict(steps=0, t1=0, t2=0, whatif=0)
    ok = True
    try:
        _propagate(n, cand, min(tier, 2), stt)
        if tier >= 3:
            while any(len(c) > 1 for c in cand) and stt["whatif"] <= cap:
                progress = False
                order = sorted((len(c), i) for i, c in enumerate(cand) if len(c) > 1)
                for _, i in order:
                    for j in range(len(cand[i])):
                        trial = [list(c) for c in cand]; trial[i] = [cand[i][j]]
                        try:
                            _propagate(n, trial, 2, dict(steps=0, t1=0, t2=0, whatif=0))
                        except Contradiction:
                            cand[i] = cand[i][:j] + cand[i][j + 1:]; stt["whatif"] += 1; progress = True
                            _propagate(n, cand, 2, stt)
                            break
                    if progress: break
                if not progress: break
    except Contradiction:
        ok = False
    ok = ok and all(len(c) == 1 for c in cand) and stt["whatif"] <= cap
    if ok:
        cells = set()
        for c in cand: cells |= c[0][1]
        ok = len(cells) == n * n
    rects = [list(c[0][0]) for c in cand] if ok else None
    return (ok, stt, rects) if return_state else ok


def need_tier(p):
    for t in (1, 2, 3):
        if solve(p, t): return t
    return 99


def check(p):
    """Well formed: every patch is a rectangle in the grid, holds exactly its own number, area matches, tiles the grid."""
    n = p["n"]; g = [[None] * n for _ in range(n)]
    assert len(p["rects"]) == len(p["clues"])
    for i, ((r, c, a), (r0, c0, h, w)) in enumerate(zip(p["clues"], p["rects"])):
        assert 0 <= r0 and 0 <= c0 and r0 + h <= n and c0 + w <= n and h * w == a
        assert r0 <= r < r0 + h and c0 <= c < c0 + w
        for rr in range(r0, r0 + h):
            for cc in range(c0, c0 + w):
                assert g[rr][cc] is None; g[rr][cc] = i
    assert all(v is not None for row in g for v in row)
    assert g == p["sol"]
    pos = [(r, c) for r, c, a in p["clues"]]
    assert len(set(pos)) == len(pos)
    for i, (r, c, a) in enumerate(p["clues"]): assert g[r][c] == i
    return True
