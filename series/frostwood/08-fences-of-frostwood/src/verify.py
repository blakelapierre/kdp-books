"""Verifies every puzzle in ../data.json:
 1. well formed (clues 0-3 on the right grid) and the stored loop is one closed fence that
    matches every clue
 2. independent SAT solver (slither_sat.py: CaDiCaL via python-sat, single-loop cuts) finds
    exactly one solution, equal to the stored loop
 3. independent backtracking counter (slither_bt.py, no SAT, no shared code) agrees: exactly one, the same
 4. difficulty band: grid size; the logic tier needed is exactly the band's tier; the number of
    short / long what-if steps is inside the band's range
 5. the two counters also agree on a copy of each puzzle with one clue removed (so they are not
    trivially both "1")
Writes ../verification.md and exits non-zero on any failure."""
import json, sys, time, random, copy
from multiprocessing import Pool
from slither import check, solve, need_tier, TIERS
from slither_sat import sat_solutions
from slither_bt import bt_solutions
from gen import BANDS

BANDS["Example"] = dict(w=5, h=5, need=1, short=(0, 0), long=(0, 0))


def mutate(p, seed):
    rnd = random.Random(seed); q = copy.deepcopy(p)
    cells = [(r, c) for r in range(q["h"]) for c in range(q["w"]) if q["clues"][r][c] is not None]
    r, c = rnd.choice(cells); q["clues"][r][c] = None
    return q


def one(p):
    check(p)
    stored = sorted(p["loop"])
    sols = sat_solutions(p, 2)
    uniq = len(sols) == 1 and sols[0] == stored
    bt = bt_solutions(p, 2)
    bt_ok = len(bt) == 1 and bt[0] == stored
    B = BANDS[p["band"]]
    size_ok = p["w"] == B["w"] and p["h"] == B["h"]
    need = need_tier(p)
    ok, st, _ = solve(p, need, return_state=True)
    tier_ok = ok and need == B["need"] and B["short"][0] <= st["short"] <= B["short"][1] and B["long"][0] <= st["long"] <= B["long"][1]
    m = mutate(p, p["num"] + 17)
    ms = min(len(sat_solutions(m, 2)), 2); mb = min(len(bt_solutions(m, 2)), 2)
    nclues = sum(n is not None for row in p["clues"] for n in row)
    return dict(num=p["num"], band=p["band"], w=p["w"], h=p["h"], nclues=nclues, nsol=len(sols), uniq=uniq, bt_ok=bt_ok,
                size_ok=size_ok, need=need, short=st["short"], long=st["long"], tier_ok=tier_ok, agree=ms == mb, msat=ms,
                loop=len(p["loop"]))


if __name__ == "__main__":
    D = json.load(open("../data.json")); t = time.time()
    BN = ("Easy", "Medium", "Hard", "Expert")
    allp = [p for b in BN for p in D[b]]
    with Pool(8) as pool:
        R = pool.map(one, allp + [D["Example"][0]], chunksize=1)
    rex = R.pop()
    ex_ok = rex["uniq"] and rex["bt_ok"] and rex["tier_ok"]
    keys = [json.dumps(p["clues"]) for p in allp]
    nodup = len(set(keys)) == len(keys)
    order_ok = [p["num"] for p in allp] == list(range(1, len(allp) + 1))
    good = lambda r: r["uniq"] and r["bt_ok"] and r["size_ok"] and r["tier_ok"] and r["agree"]
    bad = [r for r in R if not good(r)]
    mc = {1: 0, 2: 0, 0: 0}
    for r in R: mc[r["msat"]] += 1
    n = len(R)
    L = ["# Verification report: Fences of Frostwood", "",
         f"Generated {time.strftime('%Y-%m-%d %H:%M %Z')} by `src/verify.py` in {time.time() - t:.1f} s.", "",
         f"- Puzzles checked: **{n}** (+ the worked example: {'unique, solvable with the counting rules alone' if ex_ok else 'FAIL'})",
         f"- Well formed and the stored fence is one closed loop that matches every number: **{n}/{n}**",
         f"- Exactly one solution (SAT solver CaDiCaL via python-sat, with single-loop cuts), equal to the stored fence: **{sum(r['uniq'] for r in R)}/{n}**",
         f"- Independent backtracking counter (`slither_bt.py`, no SAT, no shared code) finds exactly one solution, the same one: **{sum(r['bt_ok'] for r in R)}/{n}**",
         f"- Solvable by logic alone (the step-by-step solver finishes with no guessing) and inside their difficulty band: **{sum(1 for r in R if r['size_ok'] and r['tier_ok'])}/{n}**",
         f"- Counter cross-check on copies with one number removed: SAT and backtracking agree in **{sum(r['agree'] for r in R)}/{n}** cases "
         f"(copies with exactly 1 solution: {mc[1]}, 2+: {mc[2]}, 0: {mc[0]})",
         f"- No duplicate puzzles: **{nodup}**; numbered 1..{n} in order: **{order_ok}**", "",
         "Logic tiers (the generator's own step-by-step solver): " + "; ".join(f"T{k} = {v}" for k, v in TIERS.items()) + ".", "",
         "| Band | Grid | Numbers shown | Puzzles | Nos. | Band rule | Short what-ifs | Long what-ifs |",
         "|---|---|---|---|---|---|---|---|"]
    for b in BN:
        rs = [r for r in R if r["band"] == b]; B = BANDS[b]
        L.append(f"| {b} | {B['w']}×{B['h']} | {min(r['nclues'] for r in rs)}–{max(r['nclues'] for r in rs)} | {len(rs)} | {rs[0]['num']}–{rs[-1]['num']} | "
                 f"needs exactly T{B['need']} | {min(r['short'] for r in rs)}–{max(r['short'] for r in rs)} | {min(r['long'] for r in rs)}–{max(r['long'] for r in rs)} |")
    L += ["", "## Per-puzzle results", "",
          "| # | Band | Grid | Numbers | Fence length | SAT solutions | Unique | Backtracking agrees | Tier | Short / long what-ifs |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for r in R:
        L.append(f"| {r['num']} | {r['band']} | {r['w']}×{r['h']} | {r['nclues']} | {r['loop']} | {r['nsol']} | "
                 f"{'yes' if r['uniq'] else 'NO'} | {'yes' if r['bt_ok'] else 'NO'} | T{r['need']} | {r['short']} / {r['long']} |")
    open("../verification.md", "w").write("\n".join(L) + "\n")
    print("\n".join(L[:20]))
    if bad or not (ex_ok and nodup and order_ok):
        print("FAILURES", len(bad), bad[:5]); sys.exit(1)
    print("ALL OK")
