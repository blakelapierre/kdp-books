"""Generate one logic-grid puzzle for a scene and band (used by master.py)."""
from __future__ import annotations
import random, itertools, copy
from logic import Grid, apply_clue, propagate, solve, holds, Contradiction, grid_solution
from text import Phraser, fmt_value

BAND_SPEC = {
    #          k  n  weights                                                       max clues, max pos, min complex
    "Easy":   (3, 4, dict(pos=.18, neg=.42, lt=.25, ltd=.15), 9, 3, 0),
    "Medium": (4, 4, dict(pos=.08, neg=.37, lt=.22, ltd=.13, either=.12, neither=.08), 12, 2, 1),
    "Hard":   (4, 5, dict(pos=.04, neg=.30, lt=.20, ltd=.13, either=.15, neither=.08, pair=.10), 14, 1, 2),
    "Expert": (5, 5, dict(pos=.02, neg=.24, lt=.20, ltd=.13, either=.16, neither=.08, pair=.17), 17, 1, 3),
}
COMPLEX = ("either", "neither", "pair")


def sort_key(t):
    t = t.lower()
    for a in ("a ", "the "):
        if t.startswith(a):
            return t[len(a):]
    return t


def build_frame(scene, band, rng, use):
    k, n = BAND_SPEC[band][:2]
    others = scene["cats"]
    while True:
        pick = sorted(rng.sample(range(4), k - 1))
        if any(others[i]["ordered"] for i in pick):
            break
    pool = list(scene["keypool"])
    rng.shuffle(pool)
    names, initials = [], set()
    for nm in pool:
        if nm[0] not in initials:
            names.append(nm); initials.add(nm[0])
        if len(names) == n:
            break
    cats = [dict(name=scene["key"], items=sorted(names), ordered=False)]
    for i in pick:
        c = copy.deepcopy(others[i])
        if c["ordered"]:
            st = rng.randrange(len(c["values"]) - n + 1)
            c["raw"] = c["values"][st:st + n]
            c["items"] = [fmt_value(c, v, label=True) for v in c["raw"]]
        else:
            used = set(names)
            c["items"] = sorted(rng.sample([x for x in c["pool"] if x not in used], n), key=sort_key)
        c.pop("pool", None)
        cats.append(c)
    return dict(scene=scene["id"], who=scene["who"], keytense=scene["keytense"], band=band, k=k, n=n,
                title=scene["titles"][use], intro=scene["intros"][use], cats=cats)


def rand_clue(P, sol, t, rng):
    k, n, cats = P["k"], P["n"], P["cats"]
    it = lambda c, e: [c, sol[c][e]]
    ords = [c for c in range(1, k) if cats[c]["ordered"]]
    for _ in range(50):
        if t == "pos":
            e = rng.randrange(n); c1, c2 = rng.sample(range(k), 2)
            return {"t": "pos", "a": it(c1, e), "b": it(c2, e)}
        if t == "neg":
            e1, e2 = rng.sample(range(n), 2); c1, c2 = rng.sample(range(k), 2)
            return {"t": "neg", "a": it(c1, e1), "b": it(c2, e2)}
        if t in ("lt", "ltd"):
            if not ords:
                return None
            o = rng.choice(ords)
            e1, e2 = rng.sample(range(n), 2)
            if sol[o][e1] > sol[o][e2]:
                e1, e2 = e2, e1
            rest = [c for c in range(k) if c != o]
            ca, cb = rng.choice(rest), rng.choice(rest)
            d = sol[o][e2] - sol[o][e1] if t == "ltd" else None
            return {"t": "lt", "a": it(ca, e1), "b": it(cb, e2), "o": o, "d": d}
        if t == "either":
            x, y = rng.sample(range(n), 2)
            ca = rng.randrange(k)
            rest = [c for c in range(1, k) if c != ca]
            if not rest:
                continue
            cb, cc = rng.choice(rest), rng.choice(rest)
            b, c = it(cb, x), it(cc, y)
            if rng.random() < .5:
                b, c = c, b
            return {"t": "either", "a": it(ca, x), "b": b, "c": c}
        if t == "neither":
            ec, ea, eb = rng.sample(range(n), 3)
            cc = rng.randrange(k)
            rest = [c for c in range(k) if c != cc]
            return {"t": "neither", "a": it(rng.choice(rest), ea), "b": it(rng.choice(rest), eb), "c": it(cc, ec)}
        if t == "pair":
            e1, e2 = rng.sample(range(n), 2)
            cc = rng.randrange(1, k)
            rest = [c for c in range(k) if c != cc]
            a, b = it(rng.choice(rest), e1), it(rng.choice(rest), e2)
            if rng.random() < .5:
                a, b = b, a
            return {"t": "pair", "a": a, "b": b, "c": it(cc, e1), "d": it(cc, e2)}
    return None


def informative(g, cl):
    h = g.copy()
    try:
        return apply_clue(h, cl) or False
    except Contradiction:
        return False


def make(P, rng, tries=60):
    band = P["band"]
    k, n, W, maxc, maxpos, mincx = BAND_SPEC[band]
    types, weights = zip(*W.items())
    for _ in range(tries):
        sol = [list(range(n))] + [rng.sample(range(n), n) for _ in range(k - 1)]
        clues = []
        g = Grid(k, n)
        ok = False
        while len(clues) < 30:
            t = rng.choices(types, weights)[0]
            cl = rand_clue(P, sol, t, rng)
            if cl is None or not holds(cl, sol, P["cats"]):
                continue
            if not informative(g, cl):
                continue
            clues.append(cl)
            try:
                propagate(g, clues)
            except Contradiction:
                raise RuntimeError("true clues contradicted: solver bug")
            if g.solved():
                ok = True
                break
        if not ok:
            continue
        # minimise: drop clues that are not needed
        order = list(range(len(clues)))
        rng.shuffle(order)
        keep = list(clues)
        for i in order:
            trial = [c for c in keep if c is not clues[i]]
            _, done, _ = solve(k, n, trial)
            if done:
                keep = trial
        npos = sum(c["t"] == "pos" for c in keep)
        ncx = sum(c["t"] in COMPLEX for c in keep)
        if len(keep) > maxc or npos > maxpos or ncx < mincx:
            continue
        g2, done, rounds = solve(k, n, keep)
        assert done and grid_solution(g2) == sol
        # order the clues: shuffle, but keep a gentle start for Easy (a positive clue early)
        rng.shuffle(keep)
        return sol, keep, rounds
    return None


def first_step_hint(P, clues, sol):
    """Find the smallest group of clues (1-3) that on its own fixes a match nobody was told directly."""
    k, n = P["k"], P["n"]
    ph = Phraser(P)
    stated = set()
    for c in clues:
        if c["t"] == "pos":
            stated.add((tuple(c["a"]), tuple(c["b"]))); stated.add((tuple(c["b"]), tuple(c["a"])))
    idx = list(range(len(clues)))
    for size in (1, 2, 3, 4):
        best = None
        for combo in itertools.combinations(idx, size):
            if all(clues[i]["t"] == "pos" for i in combo):
                continue
            g = Grid(k, n)
            try:
                propagate(g, [clues[i] for i in combo])
            except Contradiction:
                continue
            found = None
            for c1 in range(k):
                for c2 in range(c1 + 1, k):
                    m = g.mat(c1, c2)
                    for r in range(n):
                        if m[r].sum() == 1:
                            x = (c1, r); y = (c2, int(m[r].argmax()))
                            if (x, y) in stated:
                                continue
                            score = (0 if c1 == 0 else 1)
                            if found is None or score < found[0]:
                                found = (score, x, y)
            if found and (best is None or found[0] < best[0]):
                best = (found[0], combo, found[1], found[2])
                if found[0] == 0:
                    break
        if best:
            _, combo, x, y = best
            nums = [str(i + 1) for i in combo]
            if len(nums) == 1:
                lead = f"Clue {nums[0]} on its own shows"
            else:
                lead = "Clues " + ", ".join(nums[:-1]) + " and " + nums[-1] + " together show"
            fact = ph.fact(x, y)
            return f"{lead} that {("t" + fact[1:]) if fact.startswith("The ") else fact}"
    return "Start with the clue that names a single match, and cross out its whole row and column."
