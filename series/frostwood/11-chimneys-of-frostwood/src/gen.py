"""Chimneys (Skyscrapers) generator: a seeded random Latin square, all 4n edge clues, then clues
are removed one at a time (in a seeded random order) while the step-by-step logic solver can still
finish the puzzle within the band's rules. A puzzle the logic solver finishes has exactly one
solution; verify.py re-checks that with an independent SAT solver and a separate backtracker."""
import random
from sky import clues_from, solve, need_tier, check

BANDS = {
    # n, tier allowed while removing clues, cap on what-ifs while removing, need: required tier,
    # whatif: accepted range of what-if steps in the final puzzle, floor: stop removing at this many
    # clues (keeps the easier bands friendlier)
    "Easy":   dict(n=5, tier=1, cap=0, need=1, whatif=(0, 0), count=20, floor=9),
    "Medium": dict(n=6, tier=2, cap=0, need=2, whatif=(0, 0), count=30, floor=10),
    "Hard":   dict(n=7, tier=2, cap=0, need=2, whatif=(0, 0), count=30),
    "Expert": dict(n=6, tier=3, cap=6, need=3, whatif=(1, 6), count=20),
}


def latin(n, rnd):
    g = [[0] * n for _ in range(n)]
    def fill(i):
        if i == n * n: return True
        r, c = divmod(i, n)
        vals = list(range(1, n + 1)); rnd.shuffle(vals)
        for v in vals:
            if any(g[r][k] == v for k in range(c)) or any(g[k][c] == v for k in range(r)): continue
            g[r][c] = v
            if fill(i + 1): return True
        g[r][c] = 0
        return False
    assert fill(0)
    return g


def make(args):
    band, seed = args
    B = BANDS[band]; n = B["n"]; rnd = random.Random(seed)
    for attempt in range(20):
        sol = latin(n, rnd)
        clues = clues_from(sol)
        p = dict(n=n, clues=clues, sol=sol)
        if not solve(p, B["tier"], cap=B["cap"]): continue
        slots = [(side, i) for side in ("top", "bottom", "left", "right") for i in range(n)]; rnd.shuffle(slots)
        left = 4 * n
        for side, i in slots:
            if left <= B.get("floor", 0): break
            keep = clues[side][i]; clues[side][i] = None
            ok, stt, _ = solve(p, B["tier"], return_state=True, cap=B["cap"])
            if ok and stt["whatif"] <= B["cap"]: left -= 1; continue
            clues[side][i] = keep
        need = need_tier(p)
        if need != B["need"]: continue
        ok, stt, _ = solve(p, need, return_state=True)
        assert ok
        if not (B["whatif"][0] <= stt["whatif"] <= B["whatif"][1]): continue
        p.update(band=band, seed=seed, nclues=sum(v is not None for s in clues.values() for v in s),
                 grade=dict(tier=need, whatif=stt["whatif"]))
        check(p)
        return p
    return None


if __name__ == "__main__":
    import sys, time
    band = sys.argv[1] if len(sys.argv) > 1 else "Easy"
    t = time.time(); ok = 0
    for s in range(int(sys.argv[2]) if len(sys.argv) > 2 else 10):
        t1 = time.time(); r = make((band, s)); ok += bool(r)
        print(s, bool(r), r and r["nclues"], r and r["grade"], round(time.time() - t1, 2), flush=True)
    print(band, ok, "ok", round(time.time() - t, 1), "s")
