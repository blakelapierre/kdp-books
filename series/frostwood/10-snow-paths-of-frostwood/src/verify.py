"""Verifies every puzzle in ../data.json:
 1. well formed, and the stored solution obeys every rule (patch sizes, one number per patch,
    one connected path, no 2x2 block of path)
 2. independent SAT solver (CaDiCaL via python-sat, lazy connectivity cuts) finds exactly one solution, equal to the stored one
 3. independent backtracking counter (nk_bt.py, no SAT, no shared code) agrees: exactly one, the same
 4. difficulty band: grid size, logic tier needed is exactly the band's tier, and the number of
    one-step trials is inside the band's range
 5. the two counters also agree on a mutated copy of each puzzle (so they are not trivially both "1")
Writes ../verification.md and exits non-zero on any failure."""
import json, sys, time, random, copy, os
os.environ.setdefault("PYTHONHASHSEED", "0")
from multiprocessing import Pool
from nurikabe import sat_solutions, check_puzzle, check_solution, solve, need_tier
from nk_bt import bt_solutions
from gen import BANDS

BANDS["Example"] = dict(w=5, h=5, tier=2, fail=None, trials=(0, 0))


def mutate(p, seed):
    """Move one unit of snow from one number to another (keeps the total snow the same)."""
    rnd = random.Random(seed); q = copy.deepcopy(p); cl = q["clues"]
    for _ in range(100):
        i, j = rnd.sample(range(len(cl)), 2)
        if cl[j][2] > 1:
            cl[i][2] += 1; cl[j][2] -= 1; return q
    cl[0][2] += 1
    return q


def one(p):
    check_puzzle(p); check_solution(p)
    sols = sat_solutions(p, 2)
    bts = bt_solutions(p, 2)
    t = need_tier(p)
    ok3, st = solve(p, 3, return_state=True)
    trials = st.stats.get("trial", 0) if t == 3 else 0
    q = mutate(p, p["num"] + 7)
    ms, mb = sat_solutions(q, 2), bt_solutions(q, 2)
    B = BANDS[p["band"]]
    band_ok = (p["w"] == B["w"] and p["h"] == B["h"] and
               (t == B["tier"] if B["fail"] is not None else t is not None and t <= B["tier"]) and
               B["trials"][0] <= trials <= B["trials"][1])
    return dict(num=p["num"], band=p["band"], size=f"{p['w']}×{p['h']}", k=len(p["clues"]),
                path=sum(row.count("#") for row in p["sol"]), maxn=max(n for _, _, n in p["clues"]),
                sat=len(sols), unique=len(sols) == 1 and sols[0] == p["sol"],
                bt=len(bts) == 1 and bts[0] == p["sol"], tier=t, trials=trials, band_ok=band_ok,
                mut_agree=(len(ms) == len(mb) and (len(ms) != 1 or ms == mb)), mut=len(ms))


if __name__ == "__main__":
    t0 = time.time()
    D = json.load(open("../data.json"))
    ps = D["Example"] + [p for b in ("Easy", "Medium", "Hard", "Expert") for p in D[b]]
    with Pool(8) as pool: R = pool.map(one, ps, chunksize=1)
    ex, R = R[0], R[1:]
    nums = [r["num"] for r in R]
    keys = [(p["w"], p["h"], tuple(map(tuple, p["clues"]))) for p in ps[1:]]
    nodup = len(set(keys)) == len(keys)
    allok = all(r["unique"] and r["bt"] and r["band_ok"] and r["mut_agree"] for r in R) and ex["unique"] and ex["bt"] and nodup and nums == list(range(1, len(R) + 1))
    mut = [r["mut"] for r in R]
    L = ["# Verification report: Snow Paths of Frostwood", "",
         f"Generated {time.strftime('%Y-%m-%d %H:%M %Z')} by `src/verify.py` in {round(time.time() - t0, 1)} s.", "",
         f"- Puzzles checked: **{len(R)}** (+ the worked example: unique, {'solvable with the basic rules alone' if ex['tier'] == 1 else 'solvable without what-if steps'})",
         f"- Well formed and the stored solution obeys every rule (each number's patch has exactly that many squares, one number per patch, one connected path, no 2×2 block of path): **{len(R)}/{len(R)}**",
         f"- Exactly one solution (SAT solver CaDiCaL via python-sat, with connectivity cuts), equal to the stored solution: **{sum(r['unique'] for r in R)}/{len(R)}**",
         f"- Independent backtracking counter (`nk_bt.py`, no SAT, no shared code) finds exactly one solution, the same one: **{sum(r['bt'] for r in R)}/{len(R)}**",
         f"- Meet their difficulty band (grid size, logic tier needed, number of what-if steps): **{sum(r['band_ok'] for r in R)}/{len(R)}**",
         f"- Counter cross-check on mutated copies: SAT and backtracking agree in **{sum(r['mut_agree'] for r in R)}/{len(R)}** cases (mutations gave 0 solutions: {mut.count(0)}, exactly 1: {mut.count(1)}, 2+: {mut.count(2)})",
         f"- No duplicate puzzles: **{nodup}**; numbered 1..{len(R)} in order: **{nums == list(range(1, len(R) + 1))}**", "",
         "Logic tiers (the generator's own step-by-step solver, `nurikabe.py`): T1 = basic rules (finished patches, squares between two numbers, out-of-reach squares, the 2×2 rule, one way out for a patch or for the path); "
         "T2 = + listing every way a small patch can finish, and squares the path cannot do without; T3 = + one-step trial (what if?).", "",
         "| Band | Grid | Puzzles | Nos. | Band rule | Numbers per puzzle | Biggest number | What-if steps (range) |",
         "|---|---|---|---|---|---|---|---|"]
    for b in ("Easy", "Medium", "Hard", "Expert"):
        rs = [r for r in R if r["band"] == b]; B = BANDS[b]
        rule = {"Easy": "no what-if (T1 or T2)", "Medium": "needs exactly T2", "Hard": "needs T3", "Expert": "needs T3"}[b]
        L.append(f"| {b} | {B['w']}×{B['h']} | {len(rs)} | {rs[0]['num']}–{rs[-1]['num']} | {rule} | {min(r['k'] for r in rs)}–{max(r['k'] for r in rs)} | {max(r['maxn'] for r in rs)} | {min(r['trials'] for r in rs)}–{max(r['trials'] for r in rs)} |")
    L += ["", "## Per-puzzle results", "",
          "| # | Band | Grid | Numbers | Path squares | SAT solutions | Unique | Backtracking agrees | Tier | What-if steps |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for r in R:
        L.append(f"| {r['num']} | {r['band']} | {r['size']} | {r['k']} | {r['path']} | {r['sat']} | {'yes' if r['unique'] else 'NO'} | {'yes' if r['bt'] else 'NO'} | T{r['tier']} | {r['trials']} |")
    L += ["", f"**Result: {'ALL CHECKS PASSED' if allok else 'FAILURES FOUND'}**", ""]
    open("../verification.md", "w").write("\n".join(L))
    print("ok" if allok else "FAIL", round(time.time() - t0, 1), "s")
    sys.exit(0 if allok else 1)
