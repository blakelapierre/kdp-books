"""Verifies every puzzle in ../data.json:
 1. well formed (numbers 1-8, no two islands side by side, whole grid used) and the stored
    solution obeys every rule (counts, no crossings, one connected network)
 2. independent SAT solver (CaDiCaL via python-sat) finds exactly one solution, equal to the stored one
 3. independent backtracking counter (hashi_bt.py, no SAT, no shared code) agrees: exactly one, the same
 4. difficulty band: grid size, island count, logic tier needed is exactly the band's tier,
    and the number of one-step trials is inside the band's range
 5. the two counters also agree on a mutated copy of each puzzle (so they are not trivially both "1")
Writes ../verification.md and exits non-zero on any failure."""
import json, sys, time, random, copy
from multiprocessing import Pool
from hashi import sat_solutions, check_puzzle, check_solution, solve, need_tier, Struct, TIERS
from hashi_bt import bt_solutions
from gen import BANDS

BANDS["Example"] = dict(w=5, h=5, k=(6, 7), win=3, tier=1, fail=None, trials=(0, 0))


def style_ok(p):
    s = {(r, c) for r, c, _ in p["islands"]}
    no_touch = not any((r, c + 1) in s or (r + 1, c) in s for r, c in s)
    rows = {r for r, _ in s}; cols = {c for _, c in s}
    return no_touch and {0, p["h"] - 1} <= rows and {0, p["w"] - 1} <= cols


def mutate(p, seed):
    """Move one bridge-end: +1 on one island and -1 on a neighbour-in-line (keeps the sum even)."""
    rnd = random.Random(seed); q = copy.deepcopy(p); isl = q["islands"]
    for _ in range(100):
        i, j = rnd.sample(range(len(isl)), 2)
        if isl[i][2] < 8 and isl[j][2] > 1:
            isl[i][2] += 1; isl[j][2] -= 1; return q
    isl[0][2] = isl[0][2] % 8 + 1; isl[1][2] = isl[1][2] % 8 + 1
    return q


def one(p):
    check_puzzle(p); check_solution(p)
    stored = sorted(tuple(b) for b in p["bridges"])
    sols = sat_solutions(p, 2)
    uniq = len(sols) == 1 and sols[0] == stored
    bt = bt_solutions(p, 2)
    bt_ok = len(bt) == 1 and bt[0] == stored
    B = BANDS[p["band"]]
    size_ok = p["w"] == B["w"] and p["h"] == B["h"] and B["k"][0] <= p["k"] == len(p["islands"]) <= B["k"][1]
    need = need_tier(p)
    ok, st = solve(p, 3, return_state=True)
    tr = st.stats.get("trial", 0)
    tier_ok = need == B["tier"] and B["trials"][0] <= tr <= B["trials"][1]
    m = mutate(p, p["num"] + 17)
    ms = min(len(sat_solutions(m, 2)), 2); mb = min(len(bt_solutions(m, 2)), 2)
    return dict(num=p["num"], band=p["band"], w=p["w"], h=p["h"], k=p["k"], nsol=len(sols), uniq=uniq, bt_ok=bt_ok,
                size_ok=size_ok, style=style_ok(p), need=need, trials=tr, tier_ok=tier_ok, agree=ms == mb, msat=ms,
                maxn=max(n for _, _, n in p["islands"]), nb=len(p["bridges"]), dbl=sum(1 for b in p["bridges"] if b[2] == 2))


if __name__ == "__main__":
    D = json.load(open("../data.json")); t = time.time()
    BN = ("Easy", "Medium", "Hard", "Expert")
    allp = [p for b in BN for p in D[b]]
    with Pool(8) as pool:
        R = pool.map(one, allp + [D["Example"][0]], chunksize=1)
    rex = R.pop()
    ex_ok = rex["uniq"] and rex["bt_ok"] and rex["tier_ok"] and rex["style"]
    keys = [(p["w"], p["h"], tuple(map(tuple, p["islands"]))) for p in allp]
    nodup = len(set(keys)) == len(keys)
    order_ok = [p["num"] for p in allp] == list(range(1, len(allp) + 1))
    good = lambda r: r["uniq"] and r["bt_ok"] and r["size_ok"] and r["style"] and r["tier_ok"] and r["agree"]
    bad = [r for r in R if not good(r)]
    mc = {0: 0, 1: 0, 2: 0}
    for r in R: mc[r["msat"]] += 1
    n = len(R)
    L = ["# Verification report: Bridges of Frostwood", "",
         f"Generated {time.strftime('%Y-%m-%d %H:%M %Z')} by `src/verify.py` in {time.time() - t:.1f} s.", "",
         f"- Puzzles checked: **{n}** (+ the worked example: {'unique, solvable with island counting alone' if ex_ok else 'FAIL'})",
         f"- Well formed and the stored solution obeys every rule (each island's number met, 1 or 2 bridges per pair, no crossings, one connected network): **{n}/{n}**",
         f"- Exactly one solution (SAT solver CaDiCaL via python-sat, with connectivity cuts), equal to the stored solution: **{sum(r['uniq'] for r in R)}/{n}**",
         f"- Independent backtracking counter (`hashi_bt.py`, no SAT, no shared code) finds exactly one solution, the same one: **{sum(r['bt_ok'] for r in R)}/{n}**",
         f"- Layout (numbers 1–8, no two islands side by side, islands on all four edges of the grid): **{sum(r['style'] for r in R)}/{n}**",
         f"- Meet their difficulty band (grid size, island count, logic tier needed, number of what-if steps): **{sum(1 for r in R if r['size_ok'] and r['tier_ok'])}/{n}**",
         f"- Counter cross-check on mutated copies: SAT and backtracking agree in **{sum(r['agree'] for r in R)}/{n}** cases "
         f"(mutations gave 0 solutions: {mc[0]}, exactly 1: {mc[1]}, 2+: {mc[2]})",
         f"- No duplicate puzzles: **{nodup}**; numbered 1..{n} in order: **{order_ok}**", "",
         "Logic tiers (the generator's own step-by-step solver): " + "; ".join(f"T{k} = {v}" for k, v in TIERS.items()) + ".", "",
         "| Band | Grid | Islands | Puzzles | Nos. | Band rule | What-if steps (range) | Highest number |",
         "|---|---|---|---|---|---|---|---|"]
    for b in BN:
        rs = [r for r in R if r["band"] == b]; B = BANDS[b]
        rule = f"needs exactly T{B['tier']}"
        L.append(f"| {b} | {B['w']}×{B['h']} | {min(r['k'] for r in rs)}–{max(r['k'] for r in rs)} | {len(rs)} | {rs[0]['num']}–{rs[-1]['num']} | {rule} | "
                 f"{min(r['trials'] for r in rs)}–{max(r['trials'] for r in rs)} | {max(r['maxn'] for r in rs)} |")
    L += ["", "## Per-puzzle results", "",
          "| # | Band | Grid | Islands | Bridges (doubles) | SAT solutions | Unique | Backtracking agrees | Tier | What-if steps |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for r in R:
        L.append(f"| {r['num']} | {r['band']} | {r['w']}×{r['h']} | {r['k']} | {r['nb']} ({r['dbl']}) | {r['nsol']} | "
                 f"{'yes' if r['uniq'] else 'NO'} | {'yes' if r['bt_ok'] else 'NO'} | T{r['need']} | {r['trials']} |")
    open("../verification.md", "w").write("\n".join(L) + "\n")
    print("\n".join(L[:22]))
    if bad or not (ex_ok and nodup and order_ok):
        print("FAILURES", len(bad), bad[:5]); sys.exit(1)
    print("ALL OK")
