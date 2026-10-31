"""Independent verifier for The Fibbers of Frostwood -> ../verification.md
It does NOT import the generator. It re-reads every statement from its printed
English sentence (regex parser), then:
  1. brute-forces all 2^n worlds (bitmasks) and requires exactly one consistent world,
     equal to the printed answer;
  2. requires every statement to be needed (dropping any one leaves 2+ worlds);
  3. re-measures difficulty with its own world-set deduction ladder:
     depth 0 = one statement at a time; depth d = suppose one player's kind and
     run depth d-1 until a contradiction. The hypothesis count uses the canonical
     order (players in book order, "truth-teller" tried first, restart after each find);
  4. checks the band rules (players, depth, hypotheses), the hint, names and duplicates.
Run from src/: PYTHONHASHSEED=0 python3 verify.py
"""
import json, os, re, sys
from collections import Counter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
D = json.load(open(os.path.join(ROOT, "data.json")))
WORD = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7}
K = r"(truth-teller|fibber)"
WHO = r"(I am|[A-Z][a-z]+ is)"

def parse(text, speaker, names):
    idx = {nm: i for i, nm in enumerate(names)}
    me = idx[speaker]
    def who(tok):
        tok = tok.replace(" am", "").replace(" is", "")
        return me if tok == "I" else idx[tok]
    def T(k):
        return k.startswith("truth")
    m = re.fullmatch(r"([A-Z][a-z]+) is a " + K + r"\.", text)
    if m:
        x, v = who(m[1]), T(m[2]); return lambda w: w[x] == v
    m = re.fullmatch(r"([A-Z][a-z]+|I) and ([A-Z][a-z]+|I) are (the same kind|different kinds)\.", text)
    if m:
        x, y, same = who(m[1]), who(m[2]), m[3] == "the same kind"
        return lambda w: (w[x] == w[y]) == same
    m = re.fullmatch(r"([A-Z][a-z]+|I) and ([A-Z][a-z]+|I) are both (truth-tellers|fibbers)\.", text)
    if m:
        x, y, v = who(m[1]), who(m[2]), T(m[3]); return lambda w: w[x] == v and w[y] == v
    m = re.fullmatch(r"Either " + WHO + r" an? " + K + r", or " + WHO + r" an? " + K + r", or both\.", text)
    if m:
        x, a, y, b = who(m[1]), T(m[2]), who(m[3]), T(m[4]); return lambda w: w[x] == a or w[y] == b
    m = re.fullmatch(r"(Exactly|At least|At most) (\w+) of us (\w+) (?:is an?|are) (truth-tellers?|fibbers?)\.", text)
    if m:
        k, tot, v = WORD[m[2]], WORD[m[3]], T(m[4])
        assert tot == len(names), "group size mismatch"
        cmp = {"Exactly": lambda c: c == k, "At least": lambda c: c >= k, "At most": lambda c: c <= k}[m[1]]
        return lambda w: cmp(sum(1 for z in w if z == v))
    m = re.fullmatch(r"If " + WHO + r" an? " + K + r", then " + WHO + r" an? " + K + r"\.", text)
    if m:
        x, a, y, b = who(m[1]), T(m[2]), who(m[3]), T(m[4]); return lambda w: (w[x] != a) or (w[y] == b)
    raise ValueError("cannot parse: " + text)

def worlds(n):
    return [tuple(bool(mask >> (n - 1 - i) & 1) for i in range(n)) for mask in range(2 ** n)]

def ok_world(rules, w):
    return all(f(w) == w[s] for s, f in rules)

def box(domain, W):
    return [w for w in W if all(w[i] in domain[i] for i in range(len(domain)))]

def step0(rules, domain, W):
    """Single-statement deduction on per-player domains; None on contradiction."""
    domain = [set(d) for d in domain]
    while True:
        changed = False
        for s, f in rules:
            local = [w for w in box(domain, W) if f(w) == w[s]]
            if not local:
                return None
            for i in range(len(domain)):
                seen = {w[i] for w in local}
                if seen != domain[i]:
                    domain[i] = seen; changed = True
        if not changed:
            return domain

def ladder(rules, domain, W, d, count=None):
    domain = step0(rules, domain, W)
    if domain is None or d == 0:
        return domain
    n = len(domain)
    while any(len(x) > 1 for x in domain):
        found = False
        for i in range(n):
            if len(domain[i]) == 1:
                continue
            for val in (True, False):
                trial = [set(x) for x in domain]; trial[i] = {val}
                if ladder(rules, trial, W, d - 1) is None:
                    if count is not None: count.append((i, val))
                    domain[i] = {not val}
                    domain = step0(rules, domain, W)
                    if domain is None:
                        return None
                    found = True
                    break
            if found:
                break
        if not found:
            break
    return domain

def measure(rules, n, W):
    for d in range(4):
        hyp = []
        dom = ladder(rules, [{True, False} for _ in range(n)], W, d, hyp)
        if dom is not None and all(len(x) == 1 for x in dom):
            return d, len(hyp), hyp
    return None, None, None

def main():
    bands = D["bands"]
    rows = []; fails = []; seen = Counter()
    for p in D["puzzles"]:
        names = p["names"]; n = len(names); W = worlds(n); errs = []
        rules = []
        for st in p["statements"]:
            if st["speaker"] in re.findall(r"[A-Z][a-z]+", st["text"].replace("Either", "").replace("If", "").replace("Exactly", "").replace("At", "")):
                errs.append(f"{st['speaker']} names themself")
            rules.append((names.index(st["speaker"]), parse(st["text"], st["speaker"], names)))
        sols = [w for w in W if ok_world(rules, w)]
        if len(sols) != 1:
            errs.append(f"{len(sols)} solutions")
        else:
            got = {names[i]: ("truth-teller" if sols[0][i] else "fibber") for i in range(n)}
            if got != p["answer"]:
                errs.append("answer mismatch")
        for j in range(n):
            if len([w for w in W if ok_world(rules[:j] + rules[j + 1:], w)]) == 1:
                errs.append(f"statement {j + 1} not needed")
        d, h, hyp = measure(rules, n, W)
        b = bands[p["band"]]
        if n != b["players"]: errs.append("player count")
        if d != b["step_depth"]: errs.append(f"depth {d}")
        if h is None or not (b["hypotheses"][0] <= h <= b["hypotheses"][1]): errs.append(f"hypotheses {h}")
        if len(set(names)) != n or len({x[0] for x in names}) != n: errs.append("names")
        # hint must point the right way
        m = re.search(r"so (\w+) must be an? (truth-teller|fibber)\.$", p["hint"]) or re.search(r"shows that (\w+) (?:must be|is) an? (truth-teller|fibber)\.$", p["hint"])
        if not m or p["answer"].get(m[1]) != m[2]: errs.append("hint")
        if d and hyp and names[hyp[0][0]] != m[1]: errs.append("hint not first hypothesis")
        key = (n, tuple(sorted(st["text"] for st in p["statements"])))
        seen[key] += 1
        nf = sum(1 for v in p["answer"].values() if v == "fibber")
        rows.append((p["num"], p["band"], n, len(sols), d, h, nf, "PASS" if not errs else "FAIL: " + "; ".join(errs)))
        if errs: fails.append((p["num"], errs))
    dups = sum(c - 1 for c in seen.values() if c > 1)
    if dups: fails.append(("dup", dups))
    by = Counter(); byf = Counter()
    for r in rows:
        by[r[1]] += 1
        if r[-1] != "PASS": byf[r[1]] += 1
    kinds = Counter()
    for p in D["puzzles"]:
        for st in p["statements"]:
            t = st["text"]
            k = ("count" if re.match(r"(Exactly|At least|At most)", t) else "if-then" if t.startswith("If ") else
                 "either/or" if t.startswith("Either") else "both" if " both " in t else
                 "same/different kind" if "kind" in t else "is a")
            kinds[k] += 1
    out = ["# Verification — The Fibbers of Frostwood", "",
           f"Total puzzles: **{len(rows)}** · seed `{D['seed']}` · `PYTHONHASHSEED=0`", "",
           "## Result", "",
           ("**ALL 120 PUZZLES PASSED.**" if not fails and len(rows) == 120 else f"**FAILURES: {fails}**"),
           "Each has exactly one consistent assignment of truth-tellers and fibbers (equal to the printed answer), every statement is needed, "
           "each fits its band, every hint points the right way, and no puzzle repeats (duplicates: %d)." % dups, "",
           "## Bands", "",
           "| Band | Puzzles | Players | Statement kinds | Step depth | Hypotheses | Pass | Fail |",
           "|---|---|---|---|---|---|---|---|"]
    for bname, b in bands.items():
        out.append(f"| {bname} | {by[bname]} | {b['players']} | {', '.join(b['statement_types'])} | {b['step_depth']} | "
                   f"{b['hypotheses'][0]}–{b['hypotheses'][1]} | {by[bname] - byf[bname]} | {byf[bname]} |")
    out += ["", "**Step depth** is measured by the verifier's own deduction ladder: 0 means the puzzle falls to reading one statement at a time "
            "(each statement, with what is already known, pins someone down). 1 means at least one \"suppose X is a truth-teller…\" test is needed, "
            "where the contradiction shows up from single statements. 2 means a supposition inside a supposition is needed. "
            "**Hypotheses** is how many such tests the ladder needs in its canonical order (players in book order, truth-teller tried first).", "",
            "## Statement kinds used", "", "| Kind | Statements |", "|---|---|"]
    out += [f"| {k} | {v} |" for k, v in sorted(kinds.items())]
    out += ["", "## Method", "",
            "- `gen.py` builds random statements from a fixed seed, keeps a puzzle only if its own enumerator finds one world, its own step solver gives the band's depth and hypothesis count, and every statement is needed.",
            "- `verify.py` imports nothing from the generator. It parses the **printed English sentence** of every statement back into a rule with regular expressions, "
            "so a wording mistake would show up as a parse failure or a wrong answer. It brute-forces all 2^n worlds with bitmasks, re-checks that each statement is needed, "
            "and re-measures difficulty with an independent world-set deduction ladder.", "",
            "## Every puzzle", "", "| No. | Band | Players | Solutions | Depth | Hypotheses | Fibbers | Result |", "|---|---|---|---|---|---|---|---|"]
    out += [f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} | {r[7]} |" for r in rows]
    open(os.path.join(ROOT, "verification.md"), "w").write("\n".join(out) + "\n")
    print("fails:", fails, "rows:", len(rows))
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()
