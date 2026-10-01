"""Verifies every puzzle in ../data.json:
 1. well formed; stored solution obeys every rule
 2. independent SAT solver finds exactly one solution, equal to the stored one
 3. independent backtracking counter agrees with SAT on the puzzle and on a mutated copy
 4. difficulty band: grid size; logic solver finishes at the band tier and fails at the fail tier
Writes ../verification.md and exits non-zero on any failure."""
import json, sys, time, random, copy
from multiprocessing import Pool
from tents import sat_count, bt_count, check_puzzle, check_solution, solve, need_tier
from gen import BANDS

TIERN = {1: "row/col fills & forced tree neighbours",
         2: "+ orphan-cell clearing",
         3: "+ small-set confinement",
         4: "+ one-step trial (what if?)"}


def mutate(p, seed):
    """Flip one tree to a neighbouring empty cell (or nudge a row clue) so the puzzle may break."""
    rnd = random.Random(seed); q = copy.deepcopy(p)
    trees = [tuple(t) for t in q["trees"]]; n = q["n"]; ts = set(trees)
    for _ in range(200):
        i = rnd.randrange(len(trees)); r, c = trees[i]
        opts = [(r + dr, c + dc) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1), (2, 0), (0, 2))
                if 0 <= r + dr < n and 0 <= c + dc < n and (r + dr, c + dc) not in ts]
        if not opts: continue
        trees[i] = rnd.choice(opts)
        q["trees"] = [list(t) for t in trees]
        try:
            check_puzzle(q)
        except AssertionError:
            trees[i] = (r, c); q["trees"] = [list(t) for t in trees]; continue
        return q
    # fallback: bump a row clue
    j = rnd.randrange(n); q["rows"][j] = (q["rows"][j] + 1) % (n + 1)
    return q


def one(p):
    check_puzzle(p); check_solution(p)
    sols = sat_count(p, 2)
    stored = sorted(tuple(x) for x in p["tents"])
    uniq = len(sols) == 1 and sols[0] == stored
    bt = bt_count(p, 2)
    bt_ok = min(len(bt), 2) == min(len(sols), 2) and (not bt or bt[0] == stored)
    B = BANDS.get(p["band"], dict(n=p["n"], k=(1, 99), tier=4, fail=None))
    size_ok = p["n"] == B["n"] and B["k"][0] <= p["k"] <= B["k"][1]
    tier_ok = solve(p, B["tier"])
    fail_ok = True if B["fail"] is None else not solve(p, B["fail"])
    need = need_tier(p)
    m = mutate(p, p.get("num", 0) + 17)
    msat = min(len(sat_count(m, 2)), 2)
    mbt = min(len(bt_count(m, 2)), 2)
    agree = msat == mbt
    return dict(num=p.get("num", 0), band=p["band"], n=p["n"], k=p["k"], nsol=len(sols),
                uniq=uniq, bt_ok=bt_ok, size_ok=size_ok, tier_ok=tier_ok, fail_ok=fail_ok,
                need=need, agree=agree, msat=msat)


if __name__ == "__main__":
    D = json.load(open("../data.json")); t = time.time()
    BN = ("Easy", "Medium", "Hard", "Expert")
    allp = [p for b in BN for p in D[b]]
    ex = dict(D["Example"][0], num=0, band="Example")
    with Pool(6) as pool:
        R = pool.map(one, allp + [ex], chunksize=1)
    rex = R.pop()
    ex_ok = rex["uniq"] and rex["tier_ok"] and rex["bt_ok"]
    keys = [(p["n"], tuple(map(tuple, p["trees"])), tuple(p["rows"]), tuple(p["cols"])) for p in allp]
    nodup = len(set(keys)) == len(keys)
    order_ok = [p["num"] for p in allp] == list(range(1, len(allp) + 1))
    bad = [r for r in R if not (r["uniq"] and r["bt_ok"] and r["size_ok"] and r["tier_ok"]
                                and r["fail_ok"] and r["agree"])]
    mc = {0: 0, 1: 0, 2: 0}
    for r in R:
        mc[r["msat"]] = mc.get(r["msat"], 0) + 1
    L = ["# Verification report", "",
         f"Generated {time.strftime('%Y-%m-%d %H:%M %Z')} by `src/verify.py` in {time.time() - t:.1f} s.", "",
         f"- Puzzles checked: **{len(R)}** (+ the worked example: {'unique, solvable' if ex_ok else 'FAIL'})",
         f"- Well formed and stored solution obeys every rule (one tent per tree, tents do not touch even diagonally, row/column counts): **{len(R)}/{len(R)}**",
         f"- Exactly one solution (independent SAT solver, CaDiCaL via python-sat), matching stored solution: **{sum(r['uniq'] for r in R)}/{len(R)}**",
         f"- Independent backtracking counter agrees with SAT on each puzzle: **{sum(r['bt_ok'] for r in R)}/{len(R)}**",
         f"- Meet difficulty band (grid size, tree count, solvable at band tier, not solvable at the band's fail tier): **{sum(1 for r in R if r['size_ok'] and r['tier_ok'] and r['fail_ok'])}/{len(R)}**",
         f"- Counter cross-check on mutated copies: SAT and backtracking counts agree in **{sum(r['agree'] for r in R)}/{len(R)}** cases "
         f"(mutations gave 0 solutions: {mc.get(0,0)}, 1: {mc.get(1,0)}, 2+: {mc.get(2,0)})",
         f"- No duplicate puzzles: **{nodup}**; numbered 1..{len(R)} in order: **{order_ok}**", "",
         "Logic tiers: " + "; ".join(f"T{k} = {v}" for k, v in TIERN.items()), "",
         "| Band | Grid | Trees | Puzzles | Nos. | Band rule | Tier needed (count) |",
         "|---|---|---|---|---|---|---|"]
    for b in BN:
        rs = [r for r in R if r["band"] == b]; B = BANDS[b]
        rule = f"solvable ≤T{B['tier']}" + (f", not ≤T{B['fail']}" if B["fail"] else "")
        tiers = {}
        for r in rs: tiers[r["need"]] = tiers.get(r["need"], 0) + 1
        L.append(f"| {b} | {B['n']}×{B['n']} | {B['k'][0]}–{B['k'][1]} | {len(rs)} | {rs[0]['num']}–{rs[-1]['num']} | {rule} | "
                 + ", ".join(f"T{k}: {v}" for k, v in sorted(tiers.items(), key=lambda x: (x[0] is None, x[0]))) + " |")
    L += ["", "## Per-puzzle results", "",
          "| # | Band | Grid | Trees | SAT solutions | Unique | Tier needed | Counters agree |",
          "|---|---|---|---|---|---|---|---|"]
    for r in R:
        L.append(f"| {r['num']} | {r['band']} | {r['n']}×{r['n']} | {r['k']} | {r['nsol']} | "
                 f"{'yes' if r['uniq'] else 'NO'} | T{r['need']} | {'yes' if r['agree'] else 'NO'} |")
    open("../verification.md", "w").write("\n".join(L) + "\n")
    print("\n".join(L[:22]))
    if bad or not (ex_ok and nodup and order_ok):
        print("FAILURES", len(bad), bad[:5]); sys.exit(1)
    print("ALL OK")
