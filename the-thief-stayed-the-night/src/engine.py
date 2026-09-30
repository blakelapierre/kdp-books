"""Register context + generator + independent verifier."""
import random
from collections import defaultdict

class Ctx:
    def __init__(self, reg):
        self.reg = reg
        self.by_room = defaultdict(list)
        for p in reg: self.by_room[p["room"]].append(p)
    def at(self, room): return self.by_room.get(room, [])
    def mates(self, p): return [q for q in self.by_room[p["room"]] if q is not p]
    def party(self, p): return len(self.by_room[p["room"]])
    def above(self, p): return self.at(p["room"] + 100) if p["floor"] < 5 else []
    def below(self, p): return self.at(p["room"] - 100) if p["floor"] > 1 else []
    def across_room(self, p): n = p["num"]; return p["room"] + (1 if n % 2 else -1)
    def across(self, p): return self.at(self.across_room(p))
    def nextdoor_rooms(self, p): return [p["room"] + d for d in (-2, 2) if 1 <= p["num"] + d <= 20]
    def nextdoor(self, p): return [q for r in self.nextdoor_rooms(p) for q in self.at(r)]

def passes(clue, p, X):
    return bool(clue["f"](p, X))

def solve(reg, clues):
    X = Ctx(reg); alive = list(reg); steps = []
    for c in clues:
        out = [p for p in alive if not passes(c, p, X)]
        alive = [p for p in alive if passes(c, p, X)]
        steps.append(dict(title=c["t"], before=len(alive) + len(out), out=[p["name"] for p in out], left=len(alive)))
    return alive, steps

def verify(reg, clues, thief_name):
    """Independent brute-force checks. Returns dict of results; raises AssertionError on failure."""
    X = Ctx(reg)
    sat = [p for p in reg if all(passes(c, p, X) for c in clues)]
    assert len(sat) == 1 and sat[0]["name"] == thief_name, ("not unique", [p["name"] for p in sat])
    alive, steps = solve(reg, clues)
    for s in steps: assert len(s["out"]) >= 1, ("clue eliminates nobody", s["title"])
    assert steps[-1]["before"] >= 2, "final clue does not matter"
    # stronger: every clue is individually necessary (dropping any one leaves >1 suspect)
    nec = []
    for i in range(len(clues)):
        rest = clues[:i] + clues[i+1:]
        n = sum(1 for p in reg if all(passes(c, p, X) for c in rest))
        nec.append(n)
    names = [p["name"] for p in reg]
    assert len(set(names)) == len(names)
    return dict(steps=steps, necessity=nec)

def generate(case, master, used_thieves, max_seeds=20000):
    """Build a register for the case. Requirements (checked by verify()):
    exactly one guest satisfies every clue; applying clues in order, each clue eliminates >=1 guest;
    at least two suspects remain before the final clue."""
    clues = case["clues"]; cols = case.get("cols", [])
    n = len(clues)
    M = [i for i, c in enumerate(clues) if c["k"] == "M"]
    C = [i for i, c in enumerate(clues) if c["k"] == "C"]
    rooms = sorted({g["room"] for g in master})
    size = {rm: sum(1 for g in master if g["room"] == rm) for rm in rooms}
    Xm = Ctx(master)
    pre = [g for g in master if g["name"] not in used_thieves and all(passes(clues[i], g, Xm) for i in M)]
    if case.get("force_thief"): pre = [g for g in pre if g["name"] == case["force_thief"]]
    if not pre: raise RuntimeError("no possible thief in master for case %d" % case["num"])
    for seed in range(1, max_seeds):
        r = random.Random(case["num"] * 100000 + seed)
        t0 = r.choice(pre)
        if case["N"] >= len(master):
            reg = [dict(g) for g in master]
        else:
            rr = [x for x in rooms if x != t0["room"]]; r.shuffle(rr)
            pick = {t0["room"]}; k = size[t0["room"]]
            # force in one ordered witness (from the master list) for each master clue
            for kk in M:
                w = [g for g in master if all(passes(clues[i], g, Xm) for i in M if i < kk) and not passes(clues[kk], g, Xm)]
                if w:
                    g = r.choice(w)
                    if g["room"] not in pick: pick.add(g["room"]); k += size[g["room"]]
            if not C:   # master-only case: keep out every other guest who would satisfy all clues
                bad = {g["room"] for g in master if g["name"] != t0["name"] and all(passes(clues[i], g, Xm) for i in M)}
                rr = [x for x in rr if x not in bad]; pick -= bad
                k = sum(size[x] for x in pick)
            rr = [x for x in rr if x not in pick]
            for room in rr:
                if k + size[room] > case["N"]: continue
                pick.add(room); k += size[room]
                if k == case["N"]: break
            if k != case["N"]: continue
            reg = [dict(g) for g in master if g["room"] in pick]
        X = Ctx(reg)
        thief = next(p for p in reg if p["name"] == t0["name"])
        mpass = {p["name"]: [passes(clues[i], p, X) if clues[i]["k"] == "M" else None for i in range(n)] for p in reg}
        if not all(mpass[thief["name"]][i] for i in M): continue
        def roll(p):
            for key, _, vals in cols: p[key] = r.choice(vals)
        def first_fail(p):
            for i in range(n):
                if not passes(clues[i], p, X): return i
            return None
        others = [p for p in reg if p is not thief]
        if C:
            for p in reg: roll(p)
            ok = False
            for _ in range(500):
                roll(thief)
                if first_fail(thief) is None: ok = True; break
            if not ok: continue
            for p in others:
                tries = 0
                while first_fail(p) is None and tries < 300: roll(p); tries += 1
                if first_fail(p) is None: break
            else:
                pass
            if any(first_fail(p) is None for p in others): continue
            # ensure every clue has at least one guest whose FIRST failing clue is that clue
            for rnd in range(6):
                ff = [first_fail(p) for p in others]
                missing = [i for i in range(n) if i not in ff]
                if not missing: break
                for k in missing:
                    counts = {i: ff.count(i) for i in range(n)}
                    # candidates: pass every master clue before k (and fail k if k is master)
                    cand = [j for j, p in enumerate(others) if all(mpass[p["name"]][i] for i in M if i < k)
                            and (clues[k]["k"] == "C" or not mpass[p["name"]][k]) and counts.get(ff[j], 0) > 1]
                    r.shuffle(cand)
                    for j in cand[:40]:
                        p = others[j]; saved = {c[0]: p[c[0]] for c in cols}; hit = False
                        for _ in range(200):
                            roll(p)
                            if first_fail(p) == k: hit = True; break
                        if hit: ff[j] = k; counts[k] = 1; break
                        p.update(saved)
        else:
            if any(first_fail(p) is None for p in others): continue
        try:
            v = verify(reg, clues, thief["name"])
        except AssertionError:
            continue
        return dict(seed=seed, reg=reg, thief=thief["name"], **v)
    raise RuntimeError("no valid data for case %d" % case["num"])
