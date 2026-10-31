"""Truth-teller / fibber puzzle model, English rendering and the generator-side
step solver for The Fibbers of Frostwood.

Every player is either a Truth-teller (T, everything they say is true) or a
Fibber (F, everything they say is false). Each speaker makes one statement.
Statements (speaker s, players indexed 0..n-1, True = truth-teller):
  ("is", x, v)            x is v
  ("same", x, y)          x and y are the same kind
  ("diff", x, y)          x and y are different kinds
  ("both", x, y, v)       x and y are both v
  ("either", x, y, v)     at least one of x, y is v
  ("count", op, k, v)     op in {eq, ge, le}: number of v among all n players
  ("if", x, a, y, b)      if x is a then y is b
"""
from itertools import product

NUMW = ["zero", "one", "two", "three", "four", "five", "six", "seven"]

def kind(v, plural=False):
    if v:
        return "truth-tellers" if plural else "a truth-teller"
    return "fibbers" if plural else "a fibber"

def holds(st, a):
    t = st[0]
    if t == "is":
        return a[st[1]] == st[2]
    if t == "same":
        return a[st[1]] == a[st[2]]
    if t == "diff":
        return a[st[1]] != a[st[2]]
    if t == "both":
        return a[st[1]] == st[3] and a[st[2]] == st[3]
    if t == "either":
        return a[st[1]] == st[3] or a[st[2]] == st[3]
    if t == "count":
        c = sum(1 for x in a if x == st[3])
        return {"eq": c == st[2], "ge": c >= st[2], "le": c <= st[2]}[st[1]]
    if t == "if":
        return (a[st[1]] != st[2]) or (a[st[3]] == st[4])
    raise ValueError(st)

def refs(st, n):
    t = st[0]
    if t == "is":
        return {st[1]}
    if t in ("same", "diff", "both", "either"):
        return {st[1], st[2]}
    if t == "count":
        return set(range(n))
    if t == "if":
        return {st[1], st[3]}
    raise ValueError(st)

def consistent(stmts, a):
    return all(holds(st, a) == a[s] for s, st in stmts)

def all_solutions(n, stmts):
    return [a for a in product((True, False), repeat=n) if consistent(stmts, a)]

# ---------- English ----------
def _nm(i, s, names, subj=True):
    if i == s:
        return "I" if subj else "me"
    return names[i]

def _is(i, s, names, v):
    if i == s:
        return f"I am {kind(v)}"
    return f"{names[i]} is {kind(v)}"

def render(s, st, names, n):
    t = st[0]
    if t == "is":
        return _is(st[1], s, names, st[2]) + "."
    if t in ("same", "diff"):
        x, y = st[1], st[2]
        if y == s:
            x, y = y, x
        if x == s:
            who = f"{names[y]} and I"
            return f"{who} are {'the same kind' if t == 'same' else 'different kinds'}."
        return f"{names[x]} and {names[y]} are {'the same kind' if t == 'same' else 'different kinds'}."
    if t == "both":
        x, y, v = st[1], st[2], st[3]
        if y == s:
            x, y = y, x
        if x == s:
            return f"{names[y]} and I are both {kind(v, True)}."
        return f"{names[x]} and {names[y]} are both {kind(v, True)}."
    if t == "either":
        x, y, v = st[1], st[2], st[3]
        if y == s:
            x, y = y, x
        return f"Either {_is(x, s, names, v)}, or {_is(y, s, names, v)}, or both."
    if t == "count":
        op, k, v = st[1], st[2], st[3]
        pre = {"eq": "Exactly", "ge": "At least", "le": "At most"}[op]
        if k == 1:
            return f"{pre} one of us {NUMW[n]} is {kind(v)}."
        return f"{pre} {NUMW[k]} of us {NUMW[n]} are {kind(v, True)}."
    if t == "if":
        x, a, y, b = st[1:]
        first = _is(x, s, names, a)
        second = _is(y, s, names, b)
        return f"If {first}, then {second}."
    raise ValueError(st)

# ---------- step solver (generator side) ----------
def _completions(st, s, n, part):
    """Assignments to unknown vars in {s} ∪ refs(st) that satisfy speaker rule."""
    vs = sorted(({s} | refs(st, n)))
    unk = [v for v in vs if part[v] is None]
    out = []
    for vals in product((True, False), repeat=len(unk)):
        a = list(part)
        for v, x in zip(unk, vals):
            a[v] = x
        # count statements may reference all players; fill others arbitrarily only if needed
        if st[0] == "count":
            # all refs are in vs, so a is full
            pass
        if holds(st, a) == a[s]:
            out.append(dict(zip(unk, vals)))
    return unk, out

def propagate(n, stmts, part, trace=None):
    """Single-statement deduction to a fixpoint. Returns (part, ok, used).
    If trace is a list, (speaker, var, value) is appended for every fixed var."""
    part = list(part)
    changed = True
    steps = 0
    while changed:
        changed = False
        for s, st in stmts:
            unk, comps = _completions(st, s, n, part)
            if not comps:
                return part, False, steps
            for v in unk:
                vals = {c[v] for c in comps}
                if len(vals) == 1:
                    part[v] = vals.pop()
                    if trace is not None:
                        trace.append((s, v, part[v]))
                    changed = True
                    steps += 1
    return part, True, steps

def solve_depth(n, stmts, depth, part=None):
    """Solve with nested hypotheses up to `depth`. Returns (part, ok, log)."""
    if part is None:
        part = [None] * n
    part, ok, _ = propagate(n, stmts, part)
    log = []
    if not ok:
        return part, False, log
    if depth == 0:
        return part, True, log
    progress = True
    while progress and None in part:
        progress = False
        for v in range(n):
            if part[v] is not None:
                continue
            for val in (True, False):
                trial = list(part)
                trial[v] = val
                _, tok, _ = solve_depth(n, stmts, depth - 1, trial)
                if not tok:
                    log.append((v, val))
                    part[v] = not val
                    part, ok, _ = propagate(n, stmts, part)
                    if not ok:
                        return part, False, log
                    progress = True
                    break
            if progress:
                break
    return part, True, log

def min_depth(n, stmts, maxd=3):
    for d in range(maxd + 1):
        part, ok, log = solve_depth(n, stmts, d)
        if ok and None not in part:
            return d, log
    return None, None

def hypo_count(n, stmts, d):
    part, ok, log = solve_depth(n, stmts, d)
    return len(log)
