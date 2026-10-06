"""Verifies every puzzle in ../data.json and writes ../verification.md (exits non-zero on any failure):
 1. well formed: n x n picture; printed clues re-derived here (own run counter) from the picture
 2. independent SAT solver (satcheck.py, CaDiCaL via python-sat) finds exactly one solution, equal to the picture
 3. generator's line solver (nonogram.py) finishes the grid line by line, with no guessing, to the same picture
 4. difficulty band: grid size and the number of line-solver sweeps fall in the band's range
 5. each picture subject used once, puzzles numbered 1..N in order, pixel adjustments within the limit
 6. worked example: the statements printed in the how-to steps hold for its clues and the partial grid"""
import json, sys, time
from itertools import groupby
from multiprocessing import Pool
from satcheck import count
from nonogram import solve, grade, line_solve
from choose import BANDS
from gen import MAXFLIP

def runs(cells): return [len(list(g)) for k, g in groupby(cells) if k]

def one(p):
    n = p["n"]; pic = [[1 if ch == "#" else 0 for ch in row] for row in p["picture"]]
    wf = len(pic) == n and all(len(r) == n for r in pic) and all(ch in "#." for row in p["picture"] for ch in row)
    rows = [runs(r) for r in pic]; cols = [runs([pic[r][c] for r in range(n)]) for c in range(n)]
    clues_ok = rows == p["rows"] and cols == p["cols"]
    sols = count(p["rows"], p["cols"], 2)
    stored = sorted((r, c) for r in range(n) for c in range(n) if pic[r][c])
    uniq = len(sols) == 1 and sols[0] == stored
    g, st = solve(p["rows"], p["cols"])
    line_ok = st == "solved" and g == pic
    gr = grade(p["rows"], p["cols"])
    B = BANDS.get(p["band"])
    band_ok = True if B is None else (n == B["n"] and B["lo"] <= gr["sweeps"] <= B["hi"])
    flips_ok = len(p["flips"]) <= MAXFLIP.get(n, 0)
    fill = sum(map(sum, pic)) / (n * n)
    return dict(num=p["num"], band=p["band"], n=n, name=p["name"], nsol=len(sols), wf=wf, clues_ok=clues_ok, uniq=uniq,
                line_ok=line_ok, sweeps=gr["sweeps"], band_ok=band_ok, flips=len(p["flips"]), flips_ok=flips_ok, fill=round(fill, 2))

def example_checks(ex):
    pic = [[1 if ch == "#" else 0 for ch in row] for row in ex["picture"]]; n = ex["n"]
    R, C = ex["rows"], ex["cols"]
    g = [[-1] * n for _ in range(n)]
    for r in range(n): g[r] = line_solve(R[r], g[r])
    shaded_after_rows = sorted((r, c) for r in range(n) for c in range(n) if g[r][c] == 1)
    expect = sorted([(3, c) for c in range(8)] + [(7, c) for c in range(8)] + [(2, c) for c in range(2, 6)] + [(6, c) for c in range(2, 6)])
    checks = {
        "rows 4 and 8 say 8": R[3] == [8] and R[7] == [8],
        "rows 3 and 7 say 6": R[2] == [6] and R[6] == [6],
        "after one pass over the rows exactly rows 4, 8 and columns 3-6 of rows 3, 7 are shaded, nothing dotted":
            shaded_after_rows == expect and all(v != 0 for row in g for v in row),
        "columns 1 and 8 say 1 1": C[0] == [1, 1] and C[7] == [1, 1],
        "columns 2 and 7 say 6, filling rows 3 to 8": C[1] == [6] and C[6] == [6] and all(pic[r][1] and pic[r][6] for r in range(2, 8)) and not any(pic[r][1] or pic[r][6] for r in range(2)),
        "unique (SAT) and line-solvable": len(count(R, C, 2)) == 1 and solve(R, C)[1] == "solved",
    }
    return checks

if __name__ == "__main__":
    D = json.load(open("../data.json")); t = time.time()
    BN = ("Easy", "Medium", "Hard", "Expert")
    allp = [p for b in BN for p in D[b]]
    with Pool(8) as pool:
        R = pool.map(one, allp, chunksize=1)
    exc = example_checks(D["Example"][0]); ex_ok = all(exc.values())
    subj = [p["subject"] for p in allp]; nodup = len(set(subj)) == len(subj)
    picdup = len({tuple(p["picture"]) for p in allp}) == len(allp)
    order_ok = [p["num"] for p in allp] == list(range(1, len(allp) + 1))
    bad = [r for r in R if not (r["wf"] and r["clues_ok"] and r["uniq"] and r["line_ok"] and r["band_ok"] and r["flips_ok"])]
    L = ["# Verification report", "",
         f"Generated {time.strftime('%Y-%m-%d %H:%M %Z')} by `src/verify.py` in {time.time() - t:.1f} s.", "",
         f"- Puzzles checked: **{len(R)}** (+ the worked example: {'all printed statements hold' if ex_ok else 'FAIL'})",
         f"- Well formed, and printed clues match the picture (clues re-counted independently): **{sum(r['wf'] and r['clues_ok'] for r in R)}/{len(R)}**",
         f"- Exactly one solution (independent SAT solver, CaDiCaL via python-sat), equal to the picture: **{sum(r['uniq'] for r in R)}/{len(R)}**",
         f"- Generator's line solver finishes the grid line by line, no guessing, to the same picture: **{sum(r['line_ok'] for r in R)}/{len(R)}**",
         f"- Meet difficulty band (grid size and line-solver sweeps in range): **{sum(r['band_ok'] for r in R)}/{len(R)}**",
         f"- Pixels adjusted to make a picture line-solvable within the limit (15×15: ≤{MAXFLIP[15]}, 20×20: ≤{MAXFLIP[20]}, 25×25: ≤{MAXFLIP[25]}): **{sum(r['flips_ok'] for r in R)}/{len(R)}**; "
         f"pictures left exactly as drawn: {sum(r['flips'] == 0 for r in R)}",
         f"- Each subject used once: **{nodup}**; no duplicate pictures: **{picdup}**; numbered 1..{len(R)} in order: **{order_ok}**", "",
         "A *sweep* is one pass of exact line deduction over every row and then every column; the count includes the final pass that finds nothing left to do.", "",
         "| Band | Grid | Puzzles | Nos. | Band rule (sweeps) | Sweeps seen |", "|---|---|---|---|---|---|"]
    for b in BN:
        rs = [r for r in R if r["band"] == b]; B = BANDS[b]
        rule = f"{B['lo']}–{B['hi']}" if B["hi"] < 99 else f"≥ {B['lo']}"
        L.append(f"| {b} | {B['n']}×{B['n']} | {len(rs)} | {rs[0]['num']}–{rs[-1]['num']} | {rule} | {min(r['sweeps'] for r in rs)}–{max(r['sweeps'] for r in rs)} |")
    L += ["", "## Worked example checks", ""] + [f"- {k}: **{'yes' if v else 'NO'}**" for k, v in exc.items()]
    L += ["", "## Per-puzzle results", "",
          "| # | Band | Grid | Picture | SAT solutions | Unique | Line-solved | Sweeps | Pixels adjusted | Shaded |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for r in R:
        L.append(f"| {r['num']} | {r['band']} | {r['n']}×{r['n']} | {r['name']} | {r['nsol']} | {'yes' if r['uniq'] else 'NO'} | "
                 f"{'yes' if r['line_ok'] else 'NO'} | {r['sweeps']} | {r['flips']} | {int(r['fill'] * 100)}% |")
    open("../verification.md", "w").write("\n".join(L) + "\n")
    print("\n".join(L[:20]))
    if bad or not (ex_ok and nodup and picdup and order_ok):
        print("FAILURES", len(bad), bad[:5]); sys.exit(1)
    print("ALL OK")
