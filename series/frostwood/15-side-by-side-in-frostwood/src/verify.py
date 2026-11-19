"""Independent verifier for Side by Side in Frostwood -> ../verification.md
It does NOT import the generator (gen.py / lineup.py). It re-reads every clue from its
printed English sentence (regex parser), then:
  1. tries all n! line-ups and requires exactly one to fit every clue, equal to the printed answer;
  2. requires every clue to be needed (dropping any one leaves 2+ line-ups);
  3. re-measures difficulty with its own line-up-set deduction ladder:
     depth 0 = one clue at a time (keep only the places each person can still take in some
     full line-up that fits that clue and what is already known); depth d = suppose one person
     takes one place and run depth d-1 until a clash. Suppositions are counted in the canonical
     order (people in cast order, places low to high, restart after each strike);
  4. checks band rules (people, clue kinds, plain "has place k" clues, depth, suppositions,
     clue count), the hint, that everyone is named in a clue, that the cast list is not the
     answer order, duplicates, and a no-Christmas / no-violence word scan.
Run from src/: PYTHONHASHSEED=0 python3 verify.py
"""
import json, os, re, sys
from itertools import permutations
from collections import Counter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
D = json.load(open(os.path.join(ROOT, "data.json")))
NUM = {"one": 1, "two": 2, "three": 3}
NM = r"([A-Z][a-z]+)"

def parse(t, names, noun, plural):
    ix = {x: i for i, x in enumerate(names)}
    N = len(names)
    m = re.fullmatch(NM + rf" has {noun} (\d+)\.", t)
    if m: a, k = ix[m[1]], int(m[2]) - 1; return "at", {a}, lambda L: L[a] == k
    m = re.fullmatch(NM + rf" does not have {noun} (\d+)\.", t)
    if m: a, k = ix[m[1]], int(m[2]) - 1; return "notat", {a}, lambda L: L[a] != k
    m = re.fullmatch(NM + r" is at one end of the row\.", t)
    if m: a = ix[m[1]]; return "end", {a}, lambda L: L[a] == 0 or L[a] == N - 1
    m = re.fullmatch(NM + r" is not at either end of the row\.", t)
    if m: a = ix[m[1]]; return "notend", {a}, lambda L: 0 < L[a] < N - 1
    m = re.fullmatch(NM + rf" has an (even|odd)-numbered {noun}\.", t)
    if m: a, ev = ix[m[1]], m[2] == "even"; return "even", {a}, lambda L: ((L[a] + 1) % 2 == 0) == ev
    m = re.fullmatch(NM + r" is right next to " + NM + r"\.", t)
    if m: a, b = ix[m[1]], ix[m[2]]; return "adj", {a, b}, lambda L: abs(L[a] - L[b]) == 1
    m = re.fullmatch(NM + r" is not next to " + NM + r"\.", t)
    if m: a, b = ix[m[1]], ix[m[2]]; return "notadj", {a, b}, lambda L: abs(L[a] - L[b]) != 1
    m = re.fullmatch(NM + r" is directly to the left of " + NM + r"\.", t)
    if m: a, b = ix[m[1]], ix[m[2]]; return "left1", {a, b}, lambda L: L[b] - L[a] == 1
    m = re.fullmatch(NM + r" is somewhere to the left of " + NM + r"\.", t)
    if m: a, b = ix[m[1]], ix[m[2]]; return "before", {a, b}, lambda L: L[a] < L[b]
    m = re.fullmatch(rf"There (?:is|are) exactly (one|two|three) (?:{noun}|{plural}) between " + NM + " and " + NM + r"\.", t)
    if m: g, a, b = NUM[m[1]], ix[m[2]], ix[m[3]]; return "gap", {a, b}, lambda L: abs(L[a] - L[b]) - 1 == g
    m = re.fullmatch(NM + r" is somewhere between " + NM + " and " + NM + r"\.", t)
    if m:
        x, a, b = ix[m[1]], ix[m[2]], ix[m[3]]
        return "between", {x, a, b}, lambda L: (L[a] < L[x] < L[b]) or (L[b] < L[x] < L[a])
    raise ValueError("cannot parse: " + t)

def lineups(n):
    return list(permutations(range(n)))  # L[i] = place of person i

def step0(rules, dom, W):
    dom = [set(d) for d in dom]
    while True:
        changed = False
        box = [L for L in W if all(L[i] in dom[i] for i in range(len(dom)))]
        for _, _, f in rules:
            local = [L for L in box if f(L)]
            if not local: return None
            for i in range(len(dom)):
                seen = {L[i] for L in local}
                if seen != dom[i]:
                    dom[i] = seen; changed = True
                    box = [L for L in box if L[i] in seen]
        if not changed: return dom

def ladder(rules, dom, W, d, cnt):
    dom = step0(rules, dom, W)
    if dom is None or d == 0: return dom
    n = len(dom)
    while any(len(x) > 1 for x in dom):
        hit = None
        for i in range(n):
            if len(dom[i]) > 1:
                for k in sorted(dom[i]):
                    t = [set(x) for x in dom]; t[i] = {k}
                    if ladder(rules, t, W, d - 1, [0]) is None:
                        hit = (i, k); break
            if hit: break
        if not hit: break
        cnt[0] += 1
        dom[hit[0]].discard(hit[1])
        dom = step0(rules, dom, W)
        if dom is None: return None
    return dom

def measure(rules, n, W, maxd=2):
    for d in range(maxd + 1):
        cnt = [0]
        dom = ladder(rules, [set(range(n)) for _ in range(n)], W, d, cnt)
        if dom is not None and all(len(x) == 1 for x in dom):
            return d, cnt[0]
    return None, None

BAD = re.compile(r"\b(christmas|santa|xmas|advent|reindeer|elf|elves|kill|murder|blood|gun|knife|weapon|steal|stole|thief|crime)\b", re.I)

def main():
    rows, fails, kinds_all = [], [], Counter()
    seen = set()
    for p in D["puzzles"]:
        n, names, noun, plural = p["people"], p["names"], p["noun"], p["plural"]
        band = D["bands"][p["band"]]
        W = lineups(n)
        errs = []
        try:
            rules = [parse(c["text"], names, noun, plural) for c in p["clues"]]
        except Exception as e:
            fails.append((p["num"], str(e))); rows.append((p, "-", "-", "-", "FAIL")); continue
        sols = [L for L in W if all(f(L) for _, _, f in rules)]
        ans = tuple(p["answer"].index(nm) for nm in names)
        if len(sols) != 1: errs.append(f"{len(sols)} solutions")
        elif sols[0] != ans: errs.append("solution differs from printed answer")
        for i in range(len(rules)):
            rest = rules[:i] + rules[i + 1:]
            if sum(1 for L in W if all(f(L) for _, _, f in rest)) < 2: errs.append(f"clue {i+1} not needed")
        d, h = measure(rules, n, W)
        kinds = Counter(r[0] for r in rules); kinds_all.update(kinds)
        if n != band["people"]: errs.append("people")
        if any(k not in band["kinds"] for k in kinds): errs.append("kind not allowed")
        if kinds["at"] > band["max_at"]: errs.append("too many plain place clues")
        if d != band["depth"] or not (band["suppositions"][0] <= h <= band["suppositions"][1]): errs.append(f"band depth/supp {d}/{h}")
        if len(rules) > band["max_clues"]: errs.append("too many clues")
        if set().union(*(r[1] for r in rules)) != set(range(n)): errs.append("someone never named")
        if list(p["answer"]) == list(names): errs.append("cast order equals answer")
        if names != sorted(names) or len(set(names)) != n: errs.append("cast list")
        sig = (n, tuple(sorted(c["text"] for c in p["clues"])))
        if sig in seen: errs.append("duplicate")
        seen.add(sig)
        blob = " ".join([p["setting"], p["hint"]] + [c["text"] for c in p["clues"]])
        if BAD.search(blob): errs.append("banned word")
        # hint check
        kind, who, k = p["hint_key"]
        wi, k0 = names.index(who), k - 1
        if f"{who}" not in p["hint"] or f"{noun} {k}" not in p["hint"]: errs.append("hint text")
        if kind == "pin":
            m = re.search(r"\u201c(.+?)\u201d", p["hint"])
            if not m or m[1] + "." not in [c["text"] for c in p["clues"]]: errs.append("hint clue not in puzzle")
            if ans[wi] != k0: errs.append("hint pins wrong place")
        else:
            t = [set(range(n)) for _ in range(n)]; t[wi] = {k0}
            if ans[wi] == k0 or step0(rules, t, W) is not None and ladder(rules, t, W, 0, [0]) is not None:
                errs.append("hint supposition does not clash at one-clue-at-a-time level")
        res = "PASS" if not errs else "FAIL: " + "; ".join(errs)
        if errs: fails.append((p["num"], res))
        rows.append((p, len(sols), d, h, res))
    # report
    B = ["Easy", "Medium", "Hard", "Expert"]
    out = ["# Verification \u2014 Side by Side in Frostwood", "",
           f"Total puzzles: **{len(D['puzzles'])}** \u00b7 seed `{D['seed']}` \u00b7 `PYTHONHASHSEED=0`", "", "## Result", ""]
    if fails:
        out.append(f"**{len(fails)} PUZZLES FAILED.**"); out += [f"- No. {a}: {b}" for a, b in fails]
    else:
        out += [f"**ALL {len(rows)} PUZZLES PASSED.**",
                "Each has exactly one line-up that fits every clue (equal to the printed answer), every clue is needed, each fits its band, every hint points the right way, everyone is named in at least one clue, the cast list (alphabetical) never equals the answer, and no puzzle repeats (duplicates: 0)."]
    out += ["", "## Bands", "", "| Band | Puzzles | People | Clue kinds | Plain \u201chas place k\u201d clues (max) | Step depth | Suppositions | Clues per puzzle | Pass | Fail |", "|---|---|---|---|---|---|---|---|---|---|"]
    for b in B:
        bb = D["bands"][b]; rs = [r for r in rows if r[0]["band"] == b]
        cl = [len(r[0]["clues"]) for r in rs]
        out.append(f"| {b} | {len(rs)} | {bb['people']} | {', '.join(bb['kinds'])} | {bb['max_at']} | {bb['depth']} | {bb['suppositions'][0]}\u2013{bb['suppositions'][1]} | {min(cl)}\u2013{max(cl)} (max {bb['max_clues']}) | {sum(r[4]=='PASS' for r in rs)} | {sum(r[4]!='PASS' for r in rs)} |")
    out += ["", "**Step depth** is measured by the verifier's own deduction ladder: 0 means the puzzle falls to reading one clue at a time (each clue, together with what is already known about who can sit where, narrows someone down). 1 means at least one \u201csuppose X has place k\u2026\u201d test is needed, where the clash shows up from single clues. **Suppositions** is how many such tests the ladder needs in its canonical order (people in cast order, places low to high).",
            "", "## Clue kinds used", "", "| Kind | Clues |", "|---|---|"]
    label = {"at": "has place k", "notat": "does not have place k", "end": "at one end", "notend": "not at either end", "even": "odd/even-numbered place",
             "adj": "right next to", "notadj": "not next to", "left1": "directly to the left of", "before": "somewhere to the left of",
             "gap": "exactly g places between", "between": "somewhere between"}
    out += [f"| {label[k]} | {kinds_all[k]} |" for k in label]
    out += ["", "## Method", "",
            "- `gen.py` (with `lineup.py`) picks a random line-up from a fixed seed, adds random true clues until its numpy enumerator finds exactly one line-up, removes every clue that is not needed, and keeps the puzzle only if its own step solver gives the band's depth and supposition count.",
            "- `verify.py` imports nothing from the generator. It parses the **printed English sentence** of every clue back into a rule with regular expressions, so a wording slip would show up as a parse failure or a wrong answer. It tries all n! line-ups in pure Python, re-checks that every clue is needed, and re-measures difficulty with its own line-up-set ladder.",
            "", "## Every puzzle", "", "| No. | Band | People | Clues | Solutions | Depth | Suppositions | Result |", "|---|---|---|---|---|---|---|---|"]
    for p, s, d, h, r in rows:
        out.append(f"| {p['num']} | {p['band']} | {p['people']} | {len(p['clues'])} | {s} | {d} | {h} | {r} |")
    open(os.path.join(ROOT, "verification.md"), "w").write("\n".join(out) + "\n")
    print("FAILS:", fails if fails else 0, "| kinds:", dict(kinds_all))
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()
