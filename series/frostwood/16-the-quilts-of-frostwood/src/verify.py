"""Verifies every puzzle in ../data.json:
 1. well formed: every stored patch is a rectangle inside the grid with exactly one number, equal to
    its area, and the patches tile the grid (shikaku.check)
 2. independent SAT solver (sk_sat.py: CaDiCaL via python-sat) finds exactly one solution, equal to the stored one
 3. independent backtracking counter (sk_bt.py, no SAT, no shared code) agrees: exactly one, the same
 4. difficulty band: grid size; the logic tier needed is exactly the band's tier; the number of
    what-if steps is inside the band's range; at least the band's minimum number of deduction steps
 5. the two counters also agree on a copy of each puzzle with one number moved to a neighbouring free
    square (so they are not trivially both "1")
Writes ../verification.md and exits non-zero on any failure."""
import json, sys, time, random, copy
from multiprocessing import Pool
from shikaku import check, solve, need_tier, TIERS
from sk_sat import sat_solutions
from sk_bt import bt_solutions
from gen import BANDS

BANDS["Example"] = dict(n=5, need=1, whatif=(0, 0), minsteps=2)


def mutate(p, seed):
    rnd = random.Random(seed); q = copy.deepcopy(p); n = q["n"]
    taken = {(r, c) for r, c, a in q["clues"]}
    opts = [(i, r + dr, c + dc) for i, (r, c, a) in enumerate(q["clues"]) for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0))
            if 0 <= r + dr < n and 0 <= c + dc < n and (r + dr, c + dc) not in taken]
    i, r, c = rnd.choice(opts); q["clues"][i] = [r, c, q["clues"][i][2]]
    return q


def one(p):
    check(p)
    sols = sat_solutions(p, 2)
    uniq = len(sols) == 1 and sols[0] == p["sol"]
    bt = bt_solutions(p, 2)
    bt_ok = len(bt) == 1 and bt[0] == p["sol"]
    B = BANDS[p["band"]]
    size_ok = p["n"] == B["n"]
    need = need_tier(p)
    ok, st, _ = solve(p, need, return_state=True)
    steps = st["t1"] + st["t2"]
    tier_ok = ok and need == B["need"] and B["whatif"][0] <= st["whatif"] <= B["whatif"][1] and steps >= B.get("minsteps", 0)
    m = mutate(p, p["num"] + 17)
    ms = min(len(sat_solutions(m, 2)), 2); mb = min(len(bt_solutions(m, 2)), 2)
    return dict(num=p["num"], band=p["band"], n=p["n"], nclues=len(p["clues"]), nsol=len(sols), uniq=uniq, bt_ok=bt_ok,
                size_ok=size_ok, need=need, whatif=st["whatif"], steps=steps, tier_ok=tier_ok, agree=ms == mb, msat=ms,
                areas=(min(a for _, _, a in p["clues"]), max(a for _, _, a in p["clues"])))


if __name__ == "__main__":
    D = json.load(open("../data.json")); t = time.time()
    BN = ("Easy", "Medium", "Hard", "Expert")
    allp = [p for b in BN for p in D[b]]
    order = sorted(allp, key=lambda p: -p["n"])
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
    L = ["# Verification report: The Quilts of Frostwood", "",
         f"Generated {time.strftime('%Y-%m-%d %H:%M %Z')} by `src/verify.py` in {time.time() - t:.1f} s (puzzles made by `PYTHONHASHSEED=0 python3 master.py`, fixed seeds).", "",
         f"- Puzzles checked: **{n}** (+ the worked example: {'unique, solvable with the T1 rules alone' if ex_ok else 'FAIL'})",
         f"- Well formed (every stored patch is a rectangle holding exactly one number equal to its area, and the patches tile the grid): **{n}/{n}**",
         f"- Exactly one solution (SAT solver CaDiCaL via python-sat, `sk_sat.py`), equal to the stored answer: **{sum(r['uniq'] for r in R)}/{n}**",
         f"- Independent backtracking counter (`sk_bt.py`, no SAT, no shared code) finds exactly one solution, the same one: **{sum(r['bt_ok'] for r in R)}/{n}**",
         f"- Solvable by logic alone (the step-by-step solver in `shikaku.py` finishes with no guessing) and inside their difficulty band: **{sum(1 for r in R if r['size_ok'] and r['tier_ok'])}/{n}**",
         f"- Counter cross-check on copies with one number moved to a neighbouring square: SAT and backtracking agree in **{sum(r['agree'] for r in R)}/{n}** cases "
         f"(copies with exactly 1 solution: {mc[1]}, 2+: {mc[2]}, 0: {mc[0]})",
         f"- No duplicate puzzles: **{nodup}**; numbered 1..{n} in order: **{order_ok}**", "",
         "Logic tiers (the generator's own step-by-step solver): " + "; ".join(f"T{k} = {v}" for k, v in TIERS.items()) + ".", "",
         "| Band | Grid | Numbers (patches) | Patch sizes | Puzzles | Nos. | Band rule | Deduction steps | What-if steps |",
         "|---|---|---|---|---|---|---|---|---|"]
    for b in BN:
        rs = [r for r in R if r["band"] == b]; B = BANDS[b]
        L.append(f"| {b} | {B['n']}×{B['n']} | {min(r['nclues'] for r in rs)}–{max(r['nclues'] for r in rs)} | "
                 f"{min(r['areas'][0] for r in rs)}–{max(r['areas'][1] for r in rs)} | {len(rs)} | {rs[0]['num']}–{rs[-1]['num']} | "
                 f"needs exactly T{B['need']}, ≥ {B.get('minsteps', 0)} steps | {min(r['steps'] for r in rs)}–{max(r['steps'] for r in rs)} | {min(r['whatif'] for r in rs)}–{max(r['whatif'] for r in rs)} |")
    L += ["", "## Per-puzzle results", "",
          "| # | Band | Grid | Numbers | SAT solutions | Unique | Backtracking agrees | Tier | Steps | What-ifs |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for r in R:
        L.append(f"| {r['num']} | {r['band']} | {r['n']}×{r['n']} | {r['nclues']} | {r['nsol']} | "
                 f"{'yes' if r['uniq'] else 'NO'} | {'yes' if r['bt_ok'] else 'NO'} | T{r['need']} | {r['steps']} | {r['whatif']} |")
    open("../verification.md", "w").write("\n".join(L) + "\n")
    print("\n".join(L[:22]))
    if bad or not (ex_ok and nodup and order_ok):
        print("FAILURES", len(bad), bad[:5]); sys.exit(1)
    print("ALL OK")
