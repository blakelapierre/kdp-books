"""Independent check of every puzzle in ../data.json -> ../verification.md

This does NOT use the grid solver in logic.py. For each puzzle it:
  1. re-reads the clues as stated (structured form), encodes them for a SAT solver (python-sat) and
     counts ALL assignments that satisfy them (so it proves the answer is unique, not just findable);
  2. checks the one solution found equals the printed solution;
  3. re-renders every clue's English text from its structure and checks it matches the printed text,
     and checks each sentence is true of the printed solution;
  4. checks the content rules (no violent words) and that every clue is needed (removing any one
     clue leaves more than one solution, or the puzzle is still unique, reported as 'redundant').
"""
import json, os, sys, time, itertools, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from text import Phraser

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
D = json.load(open(os.path.join(ROOT, "data.json")))
BANDS = ["Easy", "Medium", "Hard", "Expert"]
BANNED = re.compile(r"\b(kill|killed|murder|dead|death|die|died|blood|gun|knife|stab|poison|corpse|body|weapon|gibbet|hang|hanged)\b", re.I)


def ok(cl, A):
    """A[c][e] = item of category c held by entity e (only assigned categories present)."""
    def ent(it):
        c, i = it
        return A[c].index(i)
    t = cl["t"]
    if t == "pos":
        return ent(cl["a"]) == ent(cl["b"])
    if t == "neg":
        return ent(cl["a"]) != ent(cl["b"])
    if t == "lt":
        o = cl["o"]
        x, y = A[o][ent(cl["a"])], A[o][ent(cl["b"])]
        return (y - x == cl["d"]) if cl.get("d") else x < y
    if t == "either":
        x = ent(cl["a"])
        return (x == ent(cl["b"])) != (x == ent(cl["c"]))
    if t == "neither":
        return ent(cl["a"]) != ent(cl["c"]) and ent(cl["b"]) != ent(cl["c"])
    if t == "pair":
        a, b, c, d = (ent(cl[q]) for q in "abcd")
        return a != b and {a, b} == {c, d}
    raise ValueError(t)


def count_solutions(k, n, clues, limit=2):
    """Count assignments satisfying the clues with a SAT solver (python-sat), up to `limit`.
    Variable v(c, e, i): entity e holds item i of category c (c >= 1; category 0 is the key)."""
    from pysat.solvers import Minisat22
    vid = {}

    def v(c, e, i):
        key = (c, e, i)
        if key not in vid:
            vid[key] = len(vid) + 2
        return vid[key]
    TRUE = 1
    cl = [[TRUE]]

    def E(it, e):
        c, i = it
        if c == 0:
            return TRUE if i == e else -TRUE
        return v(c, e, i)

    for c in range(1, k):
        for e in range(n):
            cl.append([v(c, e, i) for i in range(n)])
            for i, j in itertools.combinations(range(n), 2):
                cl.append([-v(c, e, i), -v(c, e, j)])
        for i in range(n):
            cl.append([v(c, e, i) for e in range(n)])
            for e, f in itertools.combinations(range(n), 2):
                cl.append([-v(c, e, i), -v(c, f, i)])
    for q in clues:
        t = q["t"]
        a = tuple(q["a"]); b = tuple(q["b"])
        if t == "pos":
            for e in range(n):
                cl += [[-E(a, e), E(b, e)], [E(a, e), -E(b, e)]]
        elif t == "neg":
            for e in range(n):
                cl.append([-E(a, e), -E(b, e)])
        elif t == "lt":
            o, d = q["o"], q.get("d")
            for e1 in range(n):
                for e2 in range(n):
                    for x in range(n):
                        for y in range(n):
                            good = (e1 != e2) and ((y - x == d) if d else x < y)
                            if not good:
                                cl.append([-E(a, e1), -E(b, e2), -E((o, x), e1), -E((o, y), e2)])
        elif t == "either":
            c_ = tuple(q["c"])
            for e in range(n):
                # a=e -> exactly one of b=e, c=e
                cl += [[-E(a, e), E(b, e), E(c_, e)], [-E(a, e), -E(b, e), -E(c_, e)]]
        elif t == "neither":
            c_ = tuple(q["c"])
            for e in range(n):
                cl += [[-E(a, e), -E(c_, e)], [-E(b, e), -E(c_, e)]]
        elif t == "pair":
            c_, d_ = tuple(q["c"]), tuple(q["d"])
            for e in range(n):
                cl += [[-E(a, e), E(c_, e), E(d_, e)], [-E(b, e), E(c_, e), E(d_, e)], [-E(a, e), -E(b, e)]]
        else:
            raise ValueError(t)
    # constant-false literals (-TRUE) are simply false; clauses containing TRUE are satisfied
    sols = []
    with Minisat22(bootstrap_with=cl) as S:
        while len(sols) < limit and S.solve():
            m = set(x for x in S.get_model() if x > 0)
            sol = [list(range(n))]
            for c in range(1, k):
                row = []
                for e in range(n):
                    row.append(next(i for i in range(n) if v(c, e, i) in m))
                sol.append(row)
            sols.append(sol)
            S.add_clause([-v(c, e, sol[c][e]) for c in range(1, k) for e in range(n)])
    return sols


def main():
    t0 = time.time()
    rows, fails, redundant = [], [], 0
    allp = D["Example"] + [p for b in BANDS for p in D[b]]
    for P in allp:
        k, n = P["k"], P["n"]
        sols = count_solutions(k, n, P["clues"])
        uniq = len(sols) == 1
        match = uniq and sols[0] == P["solution"]
        ph = Phraser(P)
        text_ok = True
        true_ok = all(ok(cl, {c: P["solution"][c] for c in range(k)}) for cl in P["clues"])
        for cl in P["clues"]:
            if cl["text"] not in (ph.clue(cl, flip=False), ph.clue(cl, flip=True)):
                text_ok = False
        words = " ".join([P["title"], P["intro"]] + [c["text"] for c in P["clues"]] + [P["hint"]])
        clean = not BANNED.search(words)
        red = 0
        for i in range(len(P["clues"])):
            rest = P["clues"][:i] + P["clues"][i + 1:]
            if len(count_solutions(k, n, rest)) == 1:
                red += 1
        redundant += red
        good = uniq and match and text_ok and true_ok and clean
        if not good:
            fails.append(P["num"])
        rows.append((P, len(sols), match, text_ok, true_ok, clean, red, good))
    dt = time.time() - t0
    L = ["# Verification report", "",
         "Generated by `src/verify.py`. It does not use the grid solver that built the puzzles (`src/logic.py`).", "",
         "Method:",
         "- Each puzzle's clues (as stated) are encoded independently for a SAT solver (python-sat / MiniSat), which counts every assignment of the categories that satisfies them. A puzzle passes only if **exactly one** assignment satisfies all of its clues and it equals the printed solution.",
         "- Each clue's printed English sentence is re-rendered from its structure and must match word for word; each clue must be true of the printed solution.",
         "- Content check: titles, openings, clues and hints are scanned for violent words (none allowed).",
         "- Redundancy: for each clue, the search is re-run without it. A clue is *redundant* if the puzzle stays unique without it (a brute-force reader who tried every case could skip it). The human-style solver can still need such a clue (it never guesses), so redundant clues are reported, not failed.", "",
         f"Runtime: **{dt:.1f}s**.", "",
         f"- Puzzles checked: **{len(rows)}** (120 puzzles + 1 worked example).",
         f"- Exactly one solution, matching the printed answer: **{sum(r[1] == 1 and r[2] for r in rows)}/{len(rows)}**",
         f"- Clue text matches structure and is true: **{sum(r[3] and r[4] for r in rows)}/{len(rows)}**",
         f"- Content check clean: **{sum(r[5] for r in rows)}/{len(rows)}**",
         f"- Redundant clues (puzzle still unique without them): {redundant} in total",
         f"- ALL PASSED: **{'YES' if not fails else 'NO ' + str(fails)}**", "",
         "| # | Band | Title | Size | Clues | Solutions | Matches | Text | Redundant | Result |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for P, ns, match, tok, trok, clean, red, good in rows:
        L.append(f"| {P['num'] or 'Ex'} | {P['band']} | {P['title']} | {P['k']}×{P['n']} | {len(P['clues'])} | {ns} | "
                 f"{'yes' if match else 'NO'} | {'ok' if tok and trok else 'BAD'} | {red} | {'OK' if good else 'FAIL'} |")
    open(os.path.join(ROOT, "verification.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L[:20]))
    if fails:
        sys.exit(1)


if __name__ == "__main__":
    main()
