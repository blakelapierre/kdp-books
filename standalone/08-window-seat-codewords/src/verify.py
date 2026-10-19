"""Independent check of every codeword in ../data.json -> ../verification.md
Does NOT import the generator. For each puzzle it:
  * rebuilds the answers from the numbered grid and the printed key, and checks they are real words, that no
    answer repeats, that every white square is in an answer of 3+ letters, and that all 26 letters A-Z are used;
  * checks the starter letters agree with the key;
  * encodes the puzzle for a SAT solver (number n is letter L; each answer must be one dictionary word with the
    right repeat pattern) over the full ENABLE dictionary (172,823 words) and asks for every solution, blocking
    each one found. A puzzle passes only if exactly one letter key exists with its starters (and we also report
    how many exist with no starters at all).
Run from src/: python3 verify.py"""
import json, os, string
from pysat.solvers import Minisat22
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "..", "data.json")))
WORDS = [w.strip().upper() for w in open(os.path.join(HERE, "enable1.txt")) if w.strip().isalpha()]
WSET = set(WORDS)
ABC = string.ascii_uppercase


def pat(seq):
    m = {}
    return tuple(m.setdefault(x, len(m)) for x in seq)


BYPAT = {}
for w in WORDS:
    BYPAT.setdefault((len(w), pat(w)), []).append(w)


def entries_of(numbers):
    n = len(numbers)
    out = []
    for r in range(n):
        run = []
        for c in range(n + 1):
            if c < n and numbers[r][c]: run.append(numbers[r][c])
            else:
                if len(run) > 1: out.append(tuple(run))
                run = []
    for c in range(n):
        run = []
        for r in range(n + 1):
            if r < n and numbers[r][c]: run.append(numbers[r][c])
            else:
                if len(run) > 1: out.append(tuple(run))
                run = []
    return out


def covered(numbers):
    n = len(numbers)
    for r in range(n):
        for c in range(n):
            if not numbers[r][c]: continue
            h = sum(1 for x in range(max(0, c - 2), min(n, c + 3)) if numbers[r][x])
            def runlen(cells):
                return len(cells)
            # length of across and down runs through (r, c)
            a0 = c
            while a0 > 0 and numbers[r][a0 - 1]: a0 -= 1
            a1 = c
            while a1 < n - 1 and numbers[r][a1 + 1]: a1 += 1
            d0 = r
            while d0 > 0 and numbers[d0 - 1][c]: d0 -= 1
            d1 = r
            while d1 < n - 1 and numbers[d1 + 1][c]: d1 += 1
            if a1 - a0 + 1 < 3 and d1 - d0 + 1 < 3: return False
            if 1 < a1 - a0 + 1 < 3 or 1 < d1 - d0 + 1 < 3: return False
    return True


def sat_count(entries, givens, limit=3):
    pool = IDPool()
    x = lambda n, L: pool.id(("x", n, L))
    s = Minisat22()
    nums = sorted({n for e in entries for n in e})
    for n in nums:
        for cl in CardEnc.equals([x(n, L) for L in ABC], 1, vpool=pool, encoding=EncType.seqcounter).clauses: s.add_clause(cl)
    for L in ABC:
        for cl in CardEnc.atmost([x(n, L) for n in nums], 1, vpool=pool, encoding=EncType.seqcounter).clauses: s.add_clause(cl)
    for n, L in givens.items(): s.add_clause([x(int(n), L)])
    for i, e in enumerate(entries):
        cands = BYPAT.get((len(e), pat(e)), [])
        ys = []
        for j, w in enumerate(cands):
            y = pool.id(("y", i, j)); ys.append(y)
            for n, L in zip(e, w): s.add_clause([-y, x(n, L)])
        s.add_clause(ys)
    sols = []
    while len(sols) < limit and s.solve():
        m = set(v for v in s.get_model() if v > 0)
        key = {n: L for n in nums for L in ABC if x(n, L) in m}
        sols.append(key)
        s.add_clause([-x(n, key[n]) for n in nums])
    s.delete()
    return sols


def main():
    rows = []; bad = 0; total = 0; zero_unique = 0
    for lv in D["levels"]:
        for p in lv["puzzles"]:
            total += 1
            numbers = p["numbers"]; key = {int(k): v for k, v in p["key"].items()}
            errs = []
            ents = entries_of(numbers)
            words = ["".join(key[n] for n in e) for e in ents]
            if any(w not in WSET for w in words): errs.append("non-word answer")
            if len(set(words)) != len(words): errs.append("repeated answer")
            if sorted(words) != sorted(p["words"]): errs.append("answer list mismatch")
            if set(key.values()) != set(ABC) or len(key) != 26: errs.append("not all 26 letters")
            if not covered(numbers): errs.append("square not in a 3+ answer")
            for n, L in p["givens"].items():
                if key[int(n)] != L: errs.append("starter disagrees with key")
            sols = sat_count(ents, p["givens"], 3)
            if len(sols) != 1 or sols[0] != key: errs.append(f"{len(sols)} solutions with starters")
            z = sat_count(ents, {}, 2)
            if len(z) == 1: zero_unique += 1
            if errs: bad += 1
            rows.append(f"| {p['id']} | {p['level']} | {len(ents)} | {len(p['givens'])} | {len(sols)} | {'1' if len(z) == 1 else '2+'} | {'OK' if not errs else '; '.join(errs)} |")
            print(p["id"], "OK" if not errs else errs, flush=True)
    out = ["# Verification: Window Seat Codewords", "",
           f"Checked {total} puzzles with `src/verify.py`, a SAT solver (MiniSat 2.2 via PySAT) that does not use the generator's code. "
           "Every answer must be a word in the full ENABLE dictionary (172,823 words), so a puzzle only passes if no other letter key works even with obscure words.",
           "", f"**Result: {total - bad} of {total} puzzles pass; {bad} fail.** "
           f"{zero_unique} of {total} puzzles would have exactly one answer even with no starter letters at all.", "",
           "| # | Level | Answers | Starters | Keys with starters | Keys with no starters | Result |", "|---|---|---|---|---|---|---|"] + rows
    open(os.path.join(HERE, "..", "verification.md"), "w").write("\n".join(out) + "\n")
    print("bad", bad, "of", total)


if __name__ == "__main__":
    main()
