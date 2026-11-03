"""Verifies every puzzle in ../data.json:
 1. well formed (signs only between neighbours, numbers in range), and the stored solution obeys every
    rule (each row and column holds 1..n once, every given number, every sign)
 2. independent SAT solver (CaDiCaL via python-sat) finds exactly one solution, equal to the stored one
 3. independent backtracking counter (fut_bt.py, no SAT, no shared code) agrees: exactly one, the same
 4. difficulty band: grid size, logic tier needed is exactly the band's tier, and the number of
    one-step trials is inside the band's range
 5. the two counters also agree on a mutated copy of each puzzle (so they are not trivially both "1")
Writes ../verification.md and exits non-zero on any failure."""
import json, sys, time, random, copy, os
os.environ.setdefault("PYTHONHASHSEED", "0")
from multiprocessing import Pool
from futoshiki import sat_solutions, check_puzzle, check_solution, solve, need_tier
from fut_bt import bt_solutions
from gen import BANDS

BANDS["Example"] = dict(n=4, tier=1, fail=None, trials=(0, 0))


def mutate(p, seed):
    """Remove one clue (a number or a sign) and flip another sign, chosen at random."""
    rnd = random.Random(seed); q = copy.deepcopy(p)
    if q["givens"] and rnd.random() < 0.5: q["givens"].pop(rnd.randrange(len(q["givens"])))
    else: q["ineq"].pop(rnd.randrange(len(q["ineq"])))
    i = rnd.randrange(len(q["ineq"])); a, b, c, d = q["ineq"][i]; q["ineq"][i] = [c, d, a, b]
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
    band_ok = (p["n"] == B["n"] and
               (t == B["tier"] if B["fail"] is not None else t is not None and t <= B["tier"]) and
               B["trials"][0] <= trials <= B["trials"][1])
    return dict(num=p["num"], band=p["band"], size=f"{p['n']}×{p['n']}", g=len(p["givens"]), s=len(p["ineq"]),
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
    keys = [(p["n"], tuple(map(tuple, p["givens"])), tuple(map(tuple, p["ineq"]))) for p in ps[1:]]
    nodup = len(set(keys)) == len(keys)
    allok = all(r["unique"] and r["bt"] and r["band_ok"] and r["mut_agree"] for r in R) and ex["unique"] and ex["bt"] and ex["tier"] == 1 and nodup and nums == list(range(1, len(R) + 1))
    mut = [r["mut"] for r in R]
    L = ["# Verification report: The Icicles of Frostwood", "",
         f"Generated {time.strftime('%Y-%m-%d %H:%M %Z')} by `src/verify.py` in {round(time.time() - t0, 1)} s.", "",
         f"- Puzzles checked: **{len(R)}** (+ the worked example: unique, {'solvable with the basic rules alone' if ex['tier'] == 1 else 'tier ' + str(ex['tier'])})",
         f"- Well formed and the stored solution obeys every rule (each row and column holds every length once, every given number, every sign): **{len(R)}/{len(R)}**",
         f"- Exactly one solution (SAT solver CaDiCaL via python-sat), equal to the stored solution: **{sum(r['unique'] for r in R)}/{len(R)}**",
         f"- Independent backtracking counter (`fut_bt.py`, no SAT, no shared code) finds exactly one solution, the same one: **{sum(r['bt'] for r in R)}/{len(R)}**",
         f"- Meet their difficulty band (grid size, logic tier needed, number of what-if steps): **{sum(r['band_ok'] for r in R)}/{len(R)}**",
         f"- Counter cross-check on mutated copies (one clue removed, one sign flipped): SAT and backtracking agree in **{sum(r['mut_agree'] for r in R)}/{len(R)}** cases (mutations gave 0 solutions: {mut.count(0)}, exactly 1: {mut.count(1)}, 2+: {mut.count(2)})",
         f"- No duplicate puzzles: **{nodup}**; numbered 1..{len(R)} in order: **{nums == list(range(1, len(R) + 1))}**", "",
         "Logic tiers (the generator's own step-by-step solver, `futoshiki.py`): T1 = basic rules (a length used once per row and column, the only square left for a length, and pushing limits across each sign); "
         "T2 = + pairs and triples of squares that share the same two or three lengths, hidden pairs, and chains of signs; T3 = + one-step trial (what if?).", "",
         "| Band | Grid | Puzzles | Nos. | Band rule | Given numbers | Signs | What-if steps (range) |",
         "|---|---|---|---|---|---|---|---|"]
    for b in ("Easy", "Medium", "Hard", "Expert"):
        rs = [r for r in R if r["band"] == b]; B = BANDS[b]
        rule = {"Easy": "basic rules only (T1)", "Medium": "needs exactly T2", "Hard": "needs T3", "Expert": "needs T3, more what-ifs"}[b]
        L.append(f"| {b} | {B['n']}×{B['n']} | {len(rs)} | {rs[0]['num']}–{rs[-1]['num']} | {rule} | {min(r['g'] for r in rs)}–{max(r['g'] for r in rs)} | {min(r['s'] for r in rs)}–{max(r['s'] for r in rs)} | {min(r['trials'] for r in rs)}–{max(r['trials'] for r in rs)} |")
    L += ["", "## Per-puzzle results", "",
          "| # | Band | Grid | Numbers | Signs | SAT solutions | Unique | Backtracking agrees | Tier | What-if steps |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for r in R:
        L.append(f"| {r['num']} | {r['band']} | {r['size']} | {r['g']} | {r['s']} | {r['sat']} | {'yes' if r['unique'] else 'NO'} | {'yes' if r['bt'] else 'NO'} | T{r['tier']} | {r['trials']} |")
    L += ["", f"**Result: {'ALL CHECKS PASSED' if allok else 'FAILURES FOUND'}**", ""]
    open("../verification.md", "w").write("\n".join(L))
    print("ok" if allok else "FAIL", round(time.time() - t0, 1), "s")
    sys.exit(0 if allok else 1)
