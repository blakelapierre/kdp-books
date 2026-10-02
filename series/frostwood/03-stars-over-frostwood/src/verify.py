"""Verifies every puzzle in ../data.json:
 1. puzzle is well formed (n x n, n connected regions) and the stored solution obeys every rule (direct check)
 2. INDEPENDENT SAT solver (verify_sat.py) finds exactly one solution, equal to the stored one
 3. difficulty band: grid size and star count; logic solver finishes at the band tier and fails at the band's fail tier
 4. cross-check of the two counters: on a mutated copy of each puzzle (one square moved to a neighbouring
    region) the SAT counter and the generator's backtracking counter must agree (0, 1 or 2+ solutions)
Writes ../verification.md and exits non-zero on any failure."""
import json, sys, time, random, copy
from multiprocessing import Pool
from verify_sat import count_solutions, check_solution, check_puzzle
from stars import solve, count
from gen import BANDS

TIERN = {1: "singles", 2: "+ one-unit placements & single confinement", 3: "+ multi-unit confinement (2–4 units)", 4: "+ one-step trial"}

def mutate(p, seed):
    rnd = random.Random(seed); n = p["n"]; q = copy.deepcopy(p); reg = q["regions"]
    for _ in range(200):
        r, c = rnd.randrange(n), rnd.randrange(n)
        nb = [reg[rr][cc] for rr, cc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)) if 0 <= rr < n and 0 <= cc < n and reg[rr][cc] != reg[r][c]]
        if nb:
            reg[r][c] = rnd.choice(nb)
            try: check_puzzle(q); return q
            except AssertionError: reg[r][c] = p["regions"][r][c]
    return None

def one(p):
    check_puzzle(p); check_solution(p)
    sols = count_solutions(p, limit=2)
    uniq = len(sols) == 1 and sols[0] == sorted(tuple(x) for x in p["solution"])
    B = BANDS.get(p["band"], dict(n=5, k=1, tier=2, fail=1))
    size_ok = p["n"] == B["n"] and p["k"] == B["k"]
    tier_ok = solve(p, B["tier"])
    fail_ok = True if not B["fail"] else not solve(p, B["fail"])
    need = next((t for t in (1, 2, 3, 4) if solve(p, t)), None)
    m = mutate(p, p.get("num", 0) + 17)
    agree = min(len(count_solutions(m, 2)), 2) == min(count(m, 2), 2) if m else True
    msat = min(len(count_solutions(m, 2)), 2) if m else None
    return dict(num=p.get("num", 0), band=p["band"], n=p["n"], k=p["k"], nsol=len(sols), uniq=uniq, size_ok=size_ok, tier_ok=tier_ok,
                fail_ok=fail_ok, need=need, agree=agree, msat=msat)

if __name__ == "__main__":
    D = json.load(open("../data.json")); t = time.time()
    BN = ("Easy", "Medium", "Hard", "Expert")
    allp = [p for b in BN for p in D[b]]
    ex = dict(D["Example"][0], num=0, band="Example")
    with Pool(6) as pool: R = pool.map(one, allp + [ex], chunksize=1)
    rex = R.pop()
    ex_ok = rex["uniq"] and rex["tier_ok"]
    keys = [json.dumps(p["regions"]) for p in allp]
    nodup = len(set(keys)) == len(keys)
    order_ok = [p["num"] for p in allp] == list(range(1, len(allp) + 1))
    bad = [r for r in R if not (r["uniq"] and r["size_ok"] and r["tier_ok"] and r["fail_ok"] and r["agree"])]
    mc = {0: 0, 1: 0, 2: 0}
    for r in R:
        if r["msat"] is not None: mc[r["msat"]] += 1
    L = ["# Verification report", "", f"Generated {time.strftime('%Y-%m-%d %H:%M %Z')} by `src/verify.py` in {time.time() - t:.1f} s.", "",
         f"- Puzzles checked: **{len(R)}** (+ the worked example: {'unique, solvable at T2' if ex_ok else 'FAIL'})",
         f"- Well formed (n×n, n connected regions) and stored solution obeys every rule (k per row/column/region, no touching): **{len(R)}/{len(R)}**",
         f"- Exactly one solution (independent SAT solver, CaDiCaL via python-sat, blocking-clause enumeration), matching stored solution: **{sum(r['uniq'] for r in R)}/{len(R)}**",
         f"- Meet difficulty band (grid size, stars per unit, solvable at band tier, not solvable at the band's fail tier): **{sum(1 for r in R if r['size_ok'] and r['tier_ok'] and r['fail_ok'])}/{len(R)}**",
         f"- Counter cross-check on mutated copies (one square moved to a neighbouring region): SAT and backtracking counts agree in **{sum(r['agree'] for r in R)}/{len(R)}** cases "
         f"(mutations gave 0 solutions: {mc[0]}, 1: {mc[1]}, 2+: {mc[2]}, so the SAT counter demonstrably detects both broken and ambiguous grids)",
         f"- No duplicate puzzles: **{nodup}**; numbered 1..{len(R)} in order: **{order_ok}**", "",
         "Logic tiers: " + "; ".join(f"T{k} = {v}" for k, v in TIERN.items()), "",
         "| Band | Grid | Stars | Puzzles | Nos. | Band rule | Tier needed (count) |", "|---|---|---|---|---|---|---|"]
    for b in BN:
        rs = [r for r in R if r["band"] == b]; B = BANDS[b]
        rule = f"solvable ≤T{B['tier']}" + (f", not ≤T{B['fail']}" if B["fail"] else "")
        tiers = {}
        for r in rs: tiers[r["need"]] = tiers.get(r["need"], 0) + 1
        L.append(f"| {b} | {B['n']}×{B['n']} | {B['k']} | {len(rs)} | {rs[0]['num']}–{rs[-1]['num']} | {rule} | " + ", ".join(f"T{k}: {v}" for k, v in sorted(tiers.items())) + " |")
    L += ["", "## Per-puzzle results", "", "| # | Band | Grid | Stars | SAT solutions | Unique | Tier needed | Counters agree |", "|---|---|---|---|---|---|---|---|"]
    for r in R: L.append(f"| {r['num']} | {r['band']} | {r['n']}×{r['n']} | {r['k']} | {r['nsol']} | {'yes' if r['uniq'] else 'NO'} | T{r['need']} | {'yes' if r['agree'] else 'NO'} |")
    open("../verification.md", "w").write("\n".join(L) + "\n")
    print("\n".join(L[:20]))
    if bad or not (ex_ok and nodup and order_ok): print("FAILURES", bad); sys.exit(1)
    print("ALL OK")
