"""Verify every lockbox puzzle -> ../verification.md
Checks use solver.py (independent depth-first search) plus a separate exhaustive count
written here with solver.score, never gen.py's lockgen.feedback."""
import itertools, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solver import solve, score
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
D = json.load(open(os.path.join(ROOT, "data.json")))

def exhaustive(L, clues):
    return [c for c in ("".join(p) for p in itertools.permutations("0123456789", L))
            if all(score(c, g) == (a, b) for g, a, b in clues)]

rows = []; fails = []
spots = set(); nums = []; codes = set()
for p in D["puzzles"]:
    b = D["bands"][p["band"]]; L = p["digits"]; clues = [tuple(c) for c in p["clues"]]
    errs = []
    if L != b["digits"]: errs.append("digit count")
    if len(set(p["code"])) != L: errs.append("code repeats a digit")
    for g, a, bb in clues:
        if len(g) != L or len(set(g)) != L: errs.append(f"bad guess {g}")
        if g == p["code"]: errs.append("guess equals code")
        if score(p["code"], g) != (a, bb): errs.append(f"verdict wrong for {g}")
    sols, nodes = solve(L, clues)
    if sols != [p["code"]]: errs.append(f"DFS solutions {sols}")
    ex = exhaustive(L, clues)
    if ex != [p["code"]]: errs.append(f"exhaustive solutions {ex[:5]}")
    lo, hi = b["clues"]
    if not lo <= len(clues) <= hi: errs.append("clue count out of band")
    nothing = sum(1 for _, a, bb in clues if a + bb == 0)
    if b["nothing_rule"] == "require" and nothing != 1: errs.append("needs exactly one nothing clue")
    if b["nothing_rule"] == "forbid" and nothing: errs.append("nothing clue not allowed")
    if b["nothing_rule"] == "any" and nothing > 1: errs.append("too many nothing clues")
    nlo, nhi = b["solver_nodes"]
    if not nlo <= nodes <= nhi: errs.append(f"solver effort {nodes} outside band")
    if nodes != p["solver_nodes"]: errs.append("recorded effort differs")
    necessary = all(len(solve(L, [c for c in clues if c != k], limit=2)[0]) > 1 for k in clues)
    if not necessary: errs.append("a clue is redundant")
    if p["code"][p["hint_pos"]] != p["hint_digit"]: errs.append("hint wrong")
    if p["spot"] in spots: errs.append("repeated spot")
    if p["code"] in codes: errs.append("repeated code")
    codes.add(p["code"])
    spots.add(p["spot"]); nums.append(p["num"])
    rows.append((p["num"], p["band"], L, len(clues), nothing, nodes, len(sols), len(ex), "yes" if necessary else "NO", "PASS" if not errs else "FAIL"))
    if errs: fails.append((p["num"], errs))
if nums != list(range(1, len(nums) + 1)): fails.append((0, ["numbering"]))

out = ["# Verification: The Lockboxes of Frostwood", "",
       f"Seed `{D['seed']}`, `PYTHONHASHSEED=0`. Rebuild with `cd src && PYTHONHASHSEED=0 python3 master.py`; the generator output is byte-identical between runs.", "",
       "## What is checked", "",
       "- **Generator** (`lockgen.py`): builds each puzzle against the full code space (every code of distinct digits) and keeps only clue sets with exactly one surviving code, then drops every clue it can.",
       "- **Independent solver** (`solver.py`): a depth-first search with partial-code pruning that never enumerates the code space and scores guesses with set arithmetic. It must find exactly one code, equal to the answer.",
       "- **Second exhaustive check** (`verify.py`): re-tests every code of distinct digits with the solver's scoring rule. Exactly one may pass.",
       "- **No repeats**: every answer code and every location is used once in the book.",
       "- **Every clue is needed**: removing any single clue leaves more than one code.",
       "- **Difficulty band**: digit count, clue count, the 'nothing is right' rule, and the solver's search effort (nodes visited) must all sit inside the band.", "",
       "| Band | Puzzles | Digits | Clues | 'Nothing is right' clue | Solver nodes |", "|---|---|---|---|---|---|"]
for name, b in D["bands"].items():
    nr = {"require": "exactly one", "forbid": "none", "any": "at most one"}[b["nothing_rule"]]
    hi = b["solver_nodes"][1]
    out.append(f"| {name} | {b['count']} | {b['digits']} | {b['clues'][0]}–{b['clues'][1]} | {nr} | {b['solver_nodes'][0]}–{'∞' if hi > 10**8 else hi} |")
out += ["", f"## Result: **{len(rows) - len(fails)} / {len(rows)} PASS**" + ("" if not fails else f" — FAILURES: {fails}"), "",
        "| No. | Band | Digits | Clues | Nothing clues | Solver nodes | DFS solutions | Exhaustive solutions | Every clue needed | Result |",
        "|---|---|---|---|---|---|---|---|---|---|"]
out += ["| " + " | ".join(str(x) for x in r) + " |" for r in rows]
open(os.path.join(ROOT, "verification.md"), "w").write("\n".join(out) + "\n")
print(f"{len(rows) - len(fails)}/{len(rows)} pass"); 
if fails: print(fails); sys.exit(1)
