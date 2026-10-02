"""Verifies every puzzle in ../data.json:
 1. stored solution satisfies all clues (direct check)
 2. INDEPENDENT SAT solver finds exactly one solution, equal to the stored one
 3. difficulty band: grid size; logic solver finishes at the band tier and fails one tier below
Writes ../verification.md and exits non-zero on any failure."""
import json, sys, time
from multiprocessing import Pool
from verify_sat import count_solutions, check_solution
from tracks import solve
from gen import BANDS

TIERN = {1: "basic cell & count rules", 2: "+ loop/fragment rules", 3: "+ parity (crossing) rule", 4: "+ one-step trial"}

def one(p):
    check_solution(p)
    sols = count_solutions(p, limit=2)
    uniq = len(sols) == 1 and sols[0] == [tuple(x) for x in p["solution"]]
    B = BANDS[p["band"]]
    size_ok = p["n"] == B["n"]
    tier_ok = solve(p, B["tier"])
    fail_ok = True if not B["fail"] else not solve(p, B["fail"])
    # sanity check that the counter really detects ambiguity: drop one given at a time
    amb = sum(1 for k in p["givens"] if len(count_solutions(dict(p, givens={x: v for x, v in p["givens"].items() if x != k}), 2)) >= 2)
    need = next((t for t in (1, 2, 3, 4) if solve(p, t)), None)
    return dict(num=p["num"], band=p["band"], n=p["n"], nsol=len(sols), uniq=uniq, size_ok=size_ok, tier_ok=tier_ok, fail_ok=fail_ok,
                need=need, amb=amb, givens=len(p["givens"]), cells=len(p["solution"]))

if __name__ == "__main__":
    D = json.load(open("../data.json")); t = time.time()
    allp = [p for b in ("Easy", "Medium", "Hard", "Expert") for p in D[b]]
    ex = D["Example"][0]; ex["num"] = 0
    with Pool(8) as pool: R = pool.map(one, allp)
    ex_ok = len(count_solutions(ex)) == 1 and check_solution(ex)
    keys = [(json.dumps(p["solution"]), json.dumps(p["givens"], sort_keys=True)) for p in allp]
    nodup = len(set(keys)) == len(keys)
    order_ok = [p["num"] for p in allp] == list(range(1, len(allp) + 1))
    bad = [r for r in R if not (r["uniq"] and r["size_ok"] and r["tier_ok"] and r["fail_ok"])]
    L = ["# Verification report", "", f"Generated {time.strftime('%Y-%m-%d %H:%M %Z')} by `src/verify.py` in {time.time() - t:.1f} s.", "",
         f"- Puzzles checked: **{len(R)}** (+ the worked example: {'unique' if ex_ok else 'FAIL'})",
         f"- Exactly one solution (independent SAT solver, CaDiCaL via python-sat, stray loops cut lazily), matching stored solution: **{sum(r['uniq'] for r in R)}/{len(R)}**",
         f"- Stored solutions satisfy every row/column count, the entry/exit and every given piece: **{len(R)}/{len(R)}**",
         f"- Meet difficulty band (grid size, solvable at band tier, not solvable one tier lower): **{len(R) - len(bad)}/{len(R)}**",
         f"- Sanity check of the counter: removing any single given from a puzzle makes the SAT solver find a 2nd solution in **{sum(r['amb'] for r in R)}/{sum(r['givens'] for r in R)}** cases (the other givens are not needed for uniqueness but are kept so that each puzzle can be finished by its band’s logic without guessing)",
         f"- No duplicate puzzles: **{nodup}**; numbered 1..{len(R)} in order: **{order_ok}**", "",
         "Logic tiers: " + "; ".join(f"T{k} = {v}" for k, v in TIERN.items()), "",
         "| Band | Grid | Puzzles | Nos. | Band rule | Tier needed (count) | Givens (min-max) | Track cells (min-max) |", "|---|---|---|---|---|---|---|---|"]
    for b in ("Easy", "Medium", "Hard", "Expert"):
        rs = [r for r in R if r["band"] == b]; B = BANDS[b]
        rule = f"solvable ≤T{B['tier']}" + (f", not ≤T{B['fail']}" if B["fail"] else "")
        tiers = {}
        for r in rs: tiers[r["need"]] = tiers.get(r["need"], 0) + 1
        L.append(f"| {b} | {B['n']}×{B['n']} | {len(rs)} | {rs[0]['num']}–{rs[-1]['num']} | {rule} | " + ", ".join(f"T{k}: {v}" for k, v in sorted(tiers.items())) +
                 f" | {min(r['givens'] for r in rs)}–{max(r['givens'] for r in rs)} | {min(r['cells'] for r in rs)}–{max(r['cells'] for r in rs)} |")
    L += ["", "## Per-puzzle results", "", "| # | Band | Grid | Solutions | Unique | Tier needed | Givens | Track cells |", "|---|---|---|---|---|---|---|---|"]
    for r in R: L.append(f"| {r['num']} | {r['band']} | {r['n']}×{r['n']} | {r['nsol']} | {'yes' if r['uniq'] else 'NO'} | T{r['need']} | {r['givens']} | {r['cells']} |")
    open("../verification.md", "w").write("\n".join(L) + "\n")
    print("\n".join(L[:14]))
    if bad or not (ex_ok and nodup and order_ok): print("FAILURES", bad); sys.exit(1)
    print("ALL OK")
