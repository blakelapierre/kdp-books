"""Verifies every puzzle in ../data.json:
 1. well formed (clues on the right sides, 1..n) and the stored solution is a Latin square
    (every height once per row and column) that matches every clue
 2. independent SAT solver (sky_sat.py: CaDiCaL via python-sat) finds exactly one solution,
    equal to the stored one
 3. independent backtracking counter (sky_bt.py, no SAT, no shared code) agrees: exactly one, the same
 4. difficulty band: grid size; the logic tier needed is exactly the band's tier; the number of
    what-if steps is inside the band's range
 5. the two counters also agree on a copy of each puzzle with one clue removed (so they are not
    trivially both "1")
Writes ../verification.md and exits non-zero on any failure."""
import json, sys, time, random, copy
from multiprocessing import Pool
from sky import check, solve, need_tier, TIERS
from sky_sat import sat_solutions
from sky_bt import bt_solutions
from gen import BANDS

BANDS["Example"] = dict(n=4, need=1, whatif=(0, 0))
SIDES = ("top", "bottom", "left", "right")


def mutate(p, seed):
    rnd = random.Random(seed); q = copy.deepcopy(p)
    slots = [(s, i) for s in SIDES for i in range(q["n"]) if q["clues"][s][i] is not None]
    s, i = rnd.choice(slots); q["clues"][s][i] = None
    return q


def one(p):
    check(p)
    assert all(v is None or 1 <= v <= p["n"] for s in SIDES for v in p["clues"][s])
    sols = sat_solutions(p, 2)
    uniq = len(sols) == 1 and sols[0] == p["sol"]
    bt = bt_solutions(p, 2)
    bt_ok = len(bt) == 1 and bt[0] == p["sol"]
    B = BANDS[p["band"]]
    size_ok = p["n"] == B["n"]
    need = need_tier(p)
    ok, st, _ = solve(p, need, return_state=True)
    tier_ok = ok and need == B["need"] and B["whatif"][0] <= st["whatif"] <= B["whatif"][1]
    m = mutate(p, p["num"] + 17)
    ms = min(len(sat_solutions(m, 2)), 2); mb = min(len(bt_solutions(m, 2)), 2)
    nclues = sum(v is not None for s in SIDES for v in p["clues"][s])
    return dict(num=p["num"], band=p["band"], n=p["n"], nclues=nclues, nsol=len(sols), uniq=uniq, bt_ok=bt_ok,
                size_ok=size_ok, need=need, whatif=st["whatif"], tier_ok=tier_ok, agree=ms == mb, msat=ms)


if __name__ == "__main__":
    D = json.load(open("../data.json")); t = time.time()
    BN = ("Easy", "Medium", "Hard", "Expert")
    allp = [p for b in BN for p in D[b]]
    order = sorted(allp, key=lambda p: -p["n"])          # big grids first so the pool stays busy
    with Pool(8) as pool:
        R = pool.map(one, order + [D["Example"][0]], chunksize=1)
    rex = R.pop()
    R.sort(key=lambda r: r["num"])
    ex_ok = rex["uniq"] and rex["bt_ok"] and rex["tier_ok"]
    keys = [json.dumps(p["clues"]) for p in allp]
    nodup = len(set(keys)) == len(keys)
    order_ok = [p["num"] for p in allp] == list(range(1, len(allp) + 1))
    good = lambda r: r["uniq"] and r["bt_ok"] and r["size_ok"] and r["tier_ok"] and r["agree"]
    bad = [r for r in R if not good(r)]
    mc = {1: 0, 2: 0, 0: 0}
    for r in R: mc[r["msat"]] += 1
    n = len(R)
    L = ["# Verification report: Chimneys of Frostwood", "",
         f"Generated {time.strftime('%Y-%m-%d %H:%M %Z')} by `src/verify.py` in {time.time() - t:.1f} s.", "",
         f"- Puzzles checked: **{n}** (+ the worked example: {'unique, solvable with the edge rules and singles alone' if ex_ok else 'FAIL'})",
         f"- Well formed and the stored answer uses every height once per row and column and matches every clue: **{n}/{n}**",
         f"- Exactly one solution (SAT solver CaDiCaL via python-sat), equal to the stored answer: **{sum(r['uniq'] for r in R)}/{n}**",
         f"- Independent backtracking counter (`sky_bt.py`, no SAT, no shared code) finds exactly one solution, the same one: **{sum(r['bt_ok'] for r in R)}/{n}**",
         f"- Solvable by logic alone (the step-by-step solver finishes with no guessing) and inside their difficulty band: **{sum(1 for r in R if r['size_ok'] and r['tier_ok'])}/{n}**",
         f"- Counter cross-check on copies with one clue removed: SAT and backtracking agree in **{sum(r['agree'] for r in R)}/{n}** cases "
         f"(copies with exactly 1 solution: {mc[1]}, 2+: {mc[2]}, 0: {mc[0]})",
         f"- No duplicate puzzles: **{nodup}**; numbered 1..{n} in order: **{order_ok}**", "",
         "Logic tiers (the generator's own step-by-step solver): " + "; ".join(f"T{k} = {v}" for k, v in TIERS.items()) + ".", "",
         "| Band | Grid | Clues shown | Puzzles | Nos. | Band rule | What-if steps |",
         "|---|---|---|---|---|---|---|"]
    for b in BN:
        rs = [r for r in R if r["band"] == b]; B = BANDS[b]
        L.append(f"| {b} | {B['n']}×{B['n']} | {min(r['nclues'] for r in rs)}–{max(r['nclues'] for r in rs)} | {len(rs)} | {rs[0]['num']}–{rs[-1]['num']} | "
                 f"needs exactly T{B['need']} | {min(r['whatif'] for r in rs)}–{max(r['whatif'] for r in rs)} |")
    L += ["", "## Per-puzzle results", "",
          "| # | Band | Grid | Clues | SAT solutions | Unique | Backtracking agrees | Tier | What-ifs |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in R:
        L.append(f"| {r['num']} | {r['band']} | {r['n']}×{r['n']} | {r['nclues']} | {r['nsol']} | "
                 f"{'yes' if r['uniq'] else 'NO'} | {'yes' if r['bt_ok'] else 'NO'} | T{r['need']} | {r['whatif']} |")
    open("../verification.md", "w").write("\n".join(L) + "\n")
    print("\n".join(L[:20]))
    if bad or not (ex_ok and nodup and order_ok):
        print("FAILURES", len(bad), bad[:5]); sys.exit(1)
    print("ALL OK")
