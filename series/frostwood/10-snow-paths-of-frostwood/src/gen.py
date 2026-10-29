"""Nurikabe generator: carve random snow patches out of an all-path grid until no 2x2 of path is left
(the path always stays connected and patches never touch side by side), put one number in each patch,
then keep only puzzles with exactly one solution (SAT) that the logic solver finishes at the band's
tier but not below it."""
import random
from nurikabe import solve, sat_solutions, check_solution, check_puzzle

BANDS = {
    # w, h, largest patch, share of snow (min, max), solvable at tier, must fail at tier, trial range, count
    "Easy":   dict(w=7,  h=7,  maxs=6,  white=(0.40, 0.52), tier=2, fail=None, trials=(0, 0),  count=40),
    "Medium": dict(w=9,  h=9,  maxs=7,  white=(0.40, 0.52), tier=2, fail=1,    trials=(0, 0),  count=40),
    "Hard":   dict(w=10, h=10, maxs=9,  white=(0.40, 0.52), tier=3, fail=2,    trials=(1, 6),  count=40),
    "Expert": dict(w=12, h=12, maxs=10, white=(0.40, 0.52), tier=3, fail=2,    trials=(4, 99), count=40),
}


def connected_without(w, h, black, x):
    """True if the path cells stay connected when cell x becomes snow."""
    cells = black - {x}
    if not cells: return False
    st = [next(iter(cells))]; seen = {st[0]}
    while st:
        r, c = st.pop()
        for y in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if y in cells and y not in seen: seen.add(y); st.append(y)
    return len(seen) == len(cells)


def carve(w, h, rnd, maxs, white_target):
    black = {(r, c) for r in range(h) for c in range(w)}
    owner = {}; islands = []
    def nbrs(x):
        r, c = x
        return [y for y in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)) if 0 <= y[0] < h and 0 <= y[1] < w]
    def pools():
        return [(r, c) for r in range(h - 1) for c in range(w - 1)
                if {(r, c), (r + 1, c), (r, c + 1), (r + 1, c + 1)} <= black]
    def try_white(x, allow_new):
        own = {owner[y] for y in nbrs(x) if y in owner}
        if len(own) > 1: return False
        if own:
            k = own.pop()
            if len(islands[k]) >= maxs: return False
        else:
            if not allow_new: return False
            k = None
        if not connected_without(w, h, black, x): return False
        black.discard(x)
        if k is None: k = len(islands); islands.append(set())
        islands[k].add(x); owner[x] = k
        return True
    fails = 0
    while fails < 600:
        P = pools()
        if not P: break
        r, c = rnd.choice(P)
        cells = [(r, c), (r + 1, c), (r, c + 1), (r + 1, c + 1)]; rnd.shuffle(cells)
        # prefer growing a neighbouring patch; start a new one sometimes
        grown = False
        for x in cells:
            if any(y in owner for y in nbrs(x)) and rnd.random() < 0.8 and try_white(x, False): grown = True; break
        if not grown:
            for x in cells:
                if try_white(x, True): grown = True; break
        if not grown: fails += 1
    if pools(): return None
    # top up: grow patches until the snow share is reached
    tgt = int(white_target * w * h); fails = 0
    while len(owner) < tgt and fails < 400:
        k = rnd.randrange(len(islands))
        opts = [y for x in islands[k] for y in nbrs(x) if y in black]
        if not opts: fails += 1; continue
        if not try_white(rnd.choice(opts), False): fails += 1
    return black, islands


def to_puzzle(w, h, black, islands, rnd):
    clues = []
    for isl in islands:
        r, c = rnd.choice(sorted(isl)); clues.append([r, c, len(isl)])
    clues.sort()
    sol = ["".join("#" if (r, c) in black else "." for c in range(w)) for r in range(h)]
    return dict(w=w, h=h, clues=clues, sol=sol)


def fix_clues(p, islands, rnd, rounds=40):
    """Move numbers inside their patches until the solution is unique (or give up)."""
    own = {}
    for k, isl in enumerate(islands):
        for x in isl: own[x] = k
    pos = {}
    for r, c, n in p["clues"]: pos[own[(r, c)]] = (r, c)
    def clues(): return sorted([pos[k][0], pos[k][1], len(islands[k])] for k in range(len(islands)))
    for _ in range(rounds):
        p["clues"] = clues()
        sols = sat_solutions(p, 2)
        if len(sols) == 1: return sols[0] == p["sol"]
        alt = sols[0] if sols[0] != p["sol"] else sols[1]
        diff = {(r, c) for r in range(p["h"]) for c in range(p["w"]) if alt[r][c] != p["sol"][r][c]}
        ks = sorted({own[x] for x in diff if x in own} | {own[y] for (r, c) in diff for y in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)) if y in own})
        moves = []
        for k in ks:
            for x in sorted(islands[k]):
                if x == pos[k]: continue
                old = pos[k]; pos[k] = x; q = dict(p, clues=clues())
                try: check_solution(q, alt); still = True
                except AssertionError: still = False
                pos[k] = old
                if not still: moves.append((k, x))
        if not moves: return False
        k, x = rnd.choice(moves); pos[k] = x
    return False


ATTEMPTS = 25


def make(args):
    band, seed = args
    B = BANDS[band]; w, h = B["w"], B["h"]; rnd = random.Random(seed)
    for attempt in range(ATTEMPTS):
        g = carve(w, h, rnd, B["maxs"], rnd.uniform(*B["white"]))
        if not g: continue
        black, islands = g
        if len(islands) < 3: continue
        p = to_puzzle(w, h, black, islands, rnd)
        if not fix_clues(p, islands, rnd): continue
        try:
            check_puzzle(p); check_solution(p)
        except AssertionError:
            continue
        ok, st = solve(p, B["tier"], return_state=True)
        if not ok or st.sol != p["sol"]: continue
        if B["fail"] is not None and solve(p, B["fail"]): continue
        tr = st.stats.get("trial", 0)
        if not B["trials"][0] <= tr <= B["trials"][1]: continue
        sols = sat_solutions(p, 2)
        if len(sols) != 1 or sols[0] != p["sol"]: continue
        st2 = st.stats
        p.update(band=band, seed=seed, k=len(p["clues"]),
                 grade=dict(tier=B["tier"], trials=tr,
                            t2=st2.get("patch-list", 0) + st2.get("path-needs", 0),
                            steps=sum(st2.values())))
        return p
    return None


if __name__ == "__main__":
    import sys, time
    band = sys.argv[1] if len(sys.argv) > 1 else "Easy"
    t = time.time(); ok = 0; n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    for s in range(n):
        r = make((band, s)); ok += bool(r)
        if r and ok == 1: print("\n".join(r["sol"]), r["clues"], r["grade"])
    print(band, ok, "/", n, "ok", round(time.time() - t, 1), "s")
