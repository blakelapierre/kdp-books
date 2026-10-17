"""Puzzle generator core (brute-force over the whole code space)."""
import itertools, random

def feedback(code, guess):
    a = 0; b = 0
    for i in range(len(code)):
        if code[i] == guess[i]:
            a += 1
        elif guess[i] in code:
            b += 1
    return a, b

_SPACE = {}
def space(L):
    if L not in _SPACE:
        _SPACE[L] = ["".join(p) for p in itertools.permutations("0123456789", L)]
    return _SPACE[L]

def consistent(cands, clues):
    out = cands
    for g, a, b in clues:
        out = [c for c in out if feedback(c, g) == (a, b)]
    return out

def make(rng, L, cmin, cmax, nothing, tries=4000):
    """nothing: 'require' (exactly one 'nothing is right' clue), 'forbid', or 'any' (at most one)."""
    S = space(L)
    for _ in range(tries):
        secret = "".join(rng.sample("0123456789", L))
        clues = []; cands = S; used_nothing = False
        if nothing == "require":
            pool = [d for d in "0123456789" if d not in secret]
            g = "".join(rng.sample(pool, L)); clues.append((g, 0, 0)); used_nothing = True
            cands = consistent(cands, [clues[-1]])
        guard = 0
        while len(cands) > 1 and guard < 200:
            guard += 1
            g = "".join(rng.sample("0123456789", L))
            if g == secret or any(g == c[0] for c in clues):
                continue
            a, b = feedback(secret, g)
            if a == L:
                continue
            if a + b == 0 and (nothing == "forbid" or used_nothing):
                continue
            if a + b == 0 and nothing == "any" and rng.random() < 0.7:
                continue
            # keep clues weak-ish: at most L-1 digits right in total, and must cut some candidates
            if a + b >= L:
                continue
            new = [c for c in cands if feedback(c, g) == (a, b)]
            if len(new) == len(cands):
                continue
            # avoid clues that are too strong early (spread information over more clues)
            if len(cands) > 40 and len(new) < len(cands) * 0.12 and rng.random() < 0.8:
                continue
            clues.append((g, a, b)); cands = new
            if a + b == 0: used_nothing = True
        if len(cands) != 1:
            continue
        # minimise: drop any clue that is not needed
        order = list(range(len(clues))); rng.shuffle(order)
        keep = list(clues)
        for idx in order:
            c = clues[idx]
            if nothing == "require" and c[1] + c[2] == 0:
                continue
            trial = [k for k in keep if k != c]
            if len(consistent(S, trial)) == 1:
                keep = trial
        if not (cmin <= len(keep) <= cmax):
            continue
        if nothing == "require" and not any(a + b == 0 for _, a, b in keep):
            continue
        # every clue necessary
        if any(len(consistent(S, [k for k in keep if k != c])) == 1 for c in keep):
            continue
        rng.shuffle(keep)
        return secret, keep
    raise RuntimeError("could not generate")
