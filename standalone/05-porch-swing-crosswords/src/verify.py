"""Independent check of every crossword in ../data.json -> ../verification.md

Does not import the generator (cross.py). For each puzzle it:
 1. re-reads the solution grid and finds every across/down run of 2+ letters itself, numbers them the
    standard way and checks they match the printed clue list exactly (number, direction, position, answer);
 2. checks the grid is one connected piece and every answer crosses at least one other answer;
 3. uses a SAT solver (python-sat) to show the grid can be filled in exactly ONE way from its own word
    bank (the alphabetical answer list printed in the back of the book);
 4. checks each clue against its answer (the answer word or its stem must not appear in the clue),
    that no answer repeats anywhere in the book, and that every answer is a real English word
    (wordfreq, if installed);
 5. scans all printed text for violent words.
Run from src/: python3 verify.py"""
import json, os, re, sys, itertools
from collections import Counter
from pysat.solvers import Minisat22
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "..", "data.json")))
PUZ = [p for part in D["parts"] for p in part["puzzles"]]
VIOLENT = ["kill", "murder", "dead", "death", "die", "blood", "gun", "knife", "stab", "shoot", "weapon", "poison",
           "corpse", "victim", "crime", "attack", "fight", "war", "bomb", "cannon", "hunter", "hunt", "trap", "prey", "slaughter"]


def runs(rows):
    H, W = len(rows), len(rows[0]); out = []
    for r in range(H):
        for c in range(W):
            if rows[r][c] == ".":
                continue
            # across
            if (c == 0 or rows[r][c - 1] == ".") and c + 1 < W and rows[r][c + 1] != ".":
                e = c
                while e + 1 < W and rows[r][e + 1] != ".":
                    e += 1
                out.append(("A", r, c, [(r, k) for k in range(c, e + 1)]))
            if (r == 0 or rows[r - 1][c] == ".") and r + 1 < H and rows[r + 1][c] != ".":
                e = r
                while e + 1 < H and rows[e + 1][c] != ".":
                    e += 1
                out.append(("D", r, c, [(k, c) for k in range(r, e + 1)]))
    starts = sorted({(r, c) for _, r, c, _ in out})
    num = {p: i + 1 for i, p in enumerate(starts)}
    return [(num[(r, c)], d, r, c, "".join(rows[a][b] for a, b in cells), cells) for d, r, c, cells in out]


def sat_fill_count(rows, bank):
    """Number of fills (0, 1 or 2 = 'more than one') of the grid's slots from the bank, each word used once."""
    sl = runs(rows)
    pool = IDPool(); cnf = []
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cells = {p for *_, cs in sl for p in cs}
    for p in cells:   # exactly one letter per cell
        lits = [pool.id(("L", p, ch)) for ch in letters]
        cnf += CardEnc.equals(lits=lits, bound=1, vpool=pool, encoding=EncType.seqcounter).clauses
    bank_idx = list(enumerate(bank))
    use = {}
    for k, (_, d, r, c, ans, cs) in enumerate(sl):
        opts = [i for i, w in bank_idx if len(w) == len(cs)]
        lits = [pool.id(("S", k, i)) for i in opts]
        if not lits:
            return 0
        cnf += CardEnc.equals(lits=lits, bound=1, vpool=pool, encoding=EncType.seqcounter).clauses
        for i in opts:
            v = pool.id(("S", k, i)); use.setdefault(i, []).append(v)
            for p, ch in zip(cs, bank[i]):
                cnf.append([-v, pool.id(("L", p, ch))])
    for i, lits in use.items():   # each bank word used at most once
        if len(lits) > 1:
            cnf += CardEnc.atmost(lits=lits, bound=1, vpool=pool, encoding=EncType.seqcounter).clauses
    slot_vars = [pool.id(("S", k, i)) for k in range(len(sl)) for i, w in bank_idx if len(w) == len(sl[k][5])]
    n = 0
    with Minisat22(bootstrap_with=cnf) as s:
        while n < 2 and s.solve():
            n += 1
            m = set(x for x in s.get_model() if x > 0)
            s.add_clause([-v for v in slot_vars if v in m])
    return n


def main():
    try:
        from wordfreq import zipf_frequency
    except ImportError:
        zipf_frequency = None
    out = []; problems = []
    all_answers = Counter()
    rows_tbl = []
    total_words = 0
    n = Counter()
    for p in PUZ:
        rows = p["rows"]; ents = p["entries"]
        assert len(set(len(r) for r in rows)) == 1
        mine = sorted((n, d, r, c, a) for n, d, r, c, a, _ in runs(rows))
        theirs = sorted((e["num"], e["dir"], e["r"], e["c"], e["answer"]) for e in ents)
        ok_struct = mine == theirs
        if not ok_struct:
            problems.append(f"#{p['num']}: clue list does not match the grid")
        # connectivity
        cells = {(r, c) for r, row in enumerate(rows) for c, ch in enumerate(row) if ch != "."}
        start = next(iter(cells)); seen = {start}; st = [start]
        while st:
            r, c = st.pop()
            for q in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if q in cells and q not in seen:
                    seen.add(q); st.append(q)
        connected = seen == cells
        rr = runs(rows)
        cover = Counter(pt for *_, cs in rr for pt in cs)
        crosses_ok = all(any(cover[pt] == 2 for pt in cs) for *_, cs in rr) and all(v in (1, 2) for v in cover.values())
        bank = sorted(e["answer"] for e in ents)
        fills = sat_fill_count(rows, bank)
        # clue checks
        clue_bad = []
        for e in ents:
            a = e["answer"].lower(); stem = a[:-1] if a.endswith("s") else a
            ws = re.findall(r"[a-z]+", e["clue"].lower())
            if not e["clue"].strip() or any(w in (a, stem, a + "s") or (len(stem) >= 4 and w.startswith(stem)) for w in ws):
                clue_bad.append(e["answer"])
            all_answers[e["answer"]] += 1
        ans = [e["answer"] for e in ents]
        prefix = [(x, y) for x, y in itertools.permutations(ans, 2) if y.startswith(x)]   # SKI/SKIS, SNOW/SNOWMAN
        rare = []
        if zipf_frequency:
            rare = [x for x in ans if zipf_frequency(x.lower(), "en") <= 0]
        text = " ".join([p["title"], p["scene"]] + [e["clue"] for e in ents]).lower()
        viol = sorted({w for w in VIOLENT if re.search(r"\b" + w + r"s?\b", text)})
        good = ok_struct and connected and crosses_ok and fills == 1 and not clue_bad and not prefix and not rare and not viol
        if not good:
            problems.append(f"#{p['num']} {p['title']}: struct={ok_struct} connected={connected} crossing={crosses_ok} fills={fills} clue={clue_bad} prefix={prefix} notword={rare} violent={viol}")
        total_words += len(ents)
        n["struct"] += ok_struct; n["conn"] += connected and crosses_ok; n["fill1"] += fills == 1
        n["clue"] += not clue_bad; n["prefix"] += bool(prefix); n["notword"] += bool(rare); n["viol"] += bool(viol)
        rows_tbl.append(f"| {p['num']} | {p['title']} | {p['level']} | {len(rows[0])}×{len(rows)} | {len(ents)} | {'yes' if ok_struct else 'NO'} | {'yes' if connected and crosses_ok else 'NO'} | {fills if fills < 2 else '2+'} | {'ok' if not clue_bad else 'CHECK'} |")
    dups = {a: n for a, n in all_answers.items() if n > 1}
    if dups:
        problems.append(f"answers used more than once: {dups}")
    out.append("# Verification report: *Porch Swing Crosswords*\n")
    out.append("Produced by `src/verify.py`, which does not use the generator code (`src/cross.py`). It reads only `data.json` (the printed grids and clue lists).\n")
    out.append("## Summary\n")
    out.append(f"- Puzzles checked: **{len(PUZ)}** ({sum(1 for p in PUZ if p['level']=='Easy')} Easy, {sum(1 for p in PUZ if p['level']=='Medium')} Medium), **{total_words}** clues in total")
    out.append(f"- Clue list matches the grid exactly (every across/down run of 2+ letters is a numbered answer, numbered the standard way, and nothing else): **{n['struct']} / {len(PUZ)}**")
    out.append(f"- Grid is one connected piece and every answer crosses at least one other: **{n['conn']} / {len(PUZ)}**")
    out.append(f"- **Exactly one way to fill the grid from its word bank** (independent SAT solver, Minisat via python-sat; the solver finds a fill, blocks it and must then find no other): **{n['fill1']} / {len(PUZ)}**")
    out.append(f"- No clue contains its own answer or the answer's stem: **{n['clue']} / {len(PUZ)}**")
    out.append(f"- Answers repeated anywhere in the book: **{len(dups)}**; puzzles where one answer is a prefix of another (e.g. SKI/SKIS): **{n['prefix']}**")
    out.append(f"- Every answer is an English dictionary word (wordfreq word list): **{('yes' if n['notword'] == 0 else 'NO') if zipf_frequency else 'not checked (wordfreq not installed)'}**")
    out.append(f"- Content scan of titles, scene lines and clues for violent words ({', '.join(VIOLENT)}): **{'none found' if n['viol'] == 0 else 'FOUND'}**")
    out.append(f"\n**Result: {'ALL CHECKS PASSED' if not problems else 'PROBLEMS FOUND'}**\n")
    if problems:
        out.append("## Problems\n"); out += [f"- {x}" for x in problems]; out.append("")
    out.append("## What \"exactly one solution\" means for a crossword\n")
    out.append("A crossword's answers come from its clues, so a computer can't prove a clue has only one possible answer. What it can prove is that the grid itself is sound: every word in the grid is one of the clued answers, all crossings agree, and, given the puzzle's word bank (printed in the back for solvers who get stuck), there is only one way to place the words. That last property means the word bank alone is enough to finish any puzzle with no guessing. The clues were also written to be plain and fair: definitions and simple fill-in-the-blanks, no cryptic wordplay, no trivia about celebrities.\n")
    out.append("## Per puzzle\n")
    out.append("| # | Title | Level | Grid | Clues | Clue list = grid | Connected | Word-bank fills | Clues |")
    out.append("|---|---|---|---|---|---|---|---|---|")
    out += rows_tbl
    open(os.path.join(HERE, "..", "verification.md"), "w").write("\n".join(out) + "\n")
    print("\n".join(out[:14]))
    print("PROBLEMS:", len(problems))
    for x in problems: print(" ", x)


if __name__ == "__main__":
    main()
