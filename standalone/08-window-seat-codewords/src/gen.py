"""Codeword generator for Window Seat Codewords.
1. template(): a 13x13 crossword grid in the classic lattice style (180-degree symmetric), every answer 3-10 letters.
2. fill(): fills it with friendly common words (fill.txt), no word twice, using all 26 letters A-Z.
3. code it: each letter gets a secret number 1-26.
4. count_solutions(): an entry-by-entry backtracking solver over the FULL ENABLE dictionary (verify) finds every
   letter-to-number key that turns all answers into real words; starter letters are added until exactly one key works.
verify.py re-checks every finished puzzle with a separate SAT solver."""
from __future__ import annotations
import os, random, string, time
HERE = os.path.dirname(os.path.abspath(__file__))
N = 13
MINL, MAXL = 3, 10
ABC = string.ascii_lowercase

# ------------------------------------------------------------------ word lists
FILL = []
for line in open(os.path.join(HERE, "fill.txt")):
    w, z = line.split("\t"); FILL.append((w, float(z)))
VER = [w.strip() for w in open(os.path.join(HERE, "enable1.txt")) if w.strip().isalpha()]


class Index:
    """Bitset index: by length -> list of words, and (pos, letter) -> int bitset."""
    def __init__(s, words):
        s.words = {}; s.bits = {}
        for w in words:
            s.words.setdefault(len(w), []).append(w)
        for L, ws in s.words.items():
            b = {}
            for i, w in enumerate(ws):
                bit = 1 << i
                for p, ch in enumerate(w):
                    b[(p, ch)] = b.get((p, ch), 0) | bit
            s.bits[L] = b
            s.__dict__.setdefault("all", {})[L] = (1 << len(ws)) - 1

    def match(s, pattern):
        L = len(pattern)
        m = s.all.get(L, 0)
        b = s.bits.get(L, {})
        for p, ch in enumerate(pattern):
            if ch != ".":
                m &= b.get((p, ch), 0)
                if not m: return 0
        return m


ZIPF = dict(FILL)
FIX = Index([w for w, _ in FILL])


def set_fill(minz):
    """Restrict the filler to words at least this common (wordfreq Zipf)."""
    global FIX
    FIX = Index([w for w, z in FILL if z >= minz])


# ------------------------------------------------------------------ grid template
def runs_of(black):
    """All maximal horizontal and vertical runs of white cells with length >= 2 -> list of cell lists."""
    out = []
    for r in range(N):
        cur = []
        for c in range(N + 1):
            if c < N and (r, c) not in black: cur.append((r, c))
            else:
                if len(cur) >= 2: out.append(("A", cur))
                cur = []
    for c in range(N):
        cur = []
        for r in range(N + 1):
            if r < N and (r, c) not in black: cur.append((r, c))
            else:
                if len(cur) >= 2: out.append(("D", cur))
                cur = []
    return out


def template(rng):
    for _ in range(2000):
        black = {(r, c) for r in range(1, N, 2) for c in range(1, N, 2)}
        cand = [(r, c) for r in range(N) for c in range(N) if (r % 2 == 0 or c % 2 == 0)]
        lattice = set(black)
        target_extra = rng.randint(6, 10)
        tries = 0
        while tries < 400:
            tries += 1
            runs = runs_of(black)
            long_runs = [cells for d, cells in runs if len(cells) > MAXL]
            if long_runs:
                cells = rng.choice(long_runs)
                opts = list(cells[MINL:len(cells) - MINL])
                if not opts: break
                p = rng.choice(opts)
            elif len(black) - 36 < target_extra:
                p = rng.choice(cand)
            else:
                break
            q = (N - 1 - p[0], N - 1 - p[1])
            nb = black | {p, q}
            # no clumps: extra blocks never touch, and two in one row or column are at least three squares apart (no long black bars)
            extra = nb - lattice
            if any((a + da, b + db) in extra for (a, b) in (p, q) for da, db in NEAR if (a + da, b + db) not in (p, q)):
                continue
            ok = all(len(cells) >= MINL for d, cells in runs_of(nb))
            # every white cell must be in at least one run of length >= 3, and the grid stays connected
            if ok:
                cov = set()
                for d, cells in runs_of(nb): cov.update(cells)
                white = {(r, c) for r in range(N) for c in range(N)} - nb
                if cov != white: ok = False
            if ok and connected(nb):
                black = nb
        runs = runs_of(black)
        if all(MINL <= len(cells) <= MAXL for d, cells in runs) and len(black) - 36 >= 4:
            return black
    raise RuntimeError("no template")


def connected(black):
    white = [(r, c) for r in range(N) for c in range(N) if (r, c) not in black]
    seen = {white[0]}; st = [white[0]]
    while st:
        r, c = st.pop()
        for p in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= p[0] < N and 0 <= p[1] < N and p not in black and p not in seen:
                seen.add(p); st.append(p)
    return len(seen) == len(white)


# ------------------------------------------------------------------ fill
NEAR = [(da, db) for da in (-1, 0, 1) for db in (-1, 0, 1) if da or db] + [(0, 2), (0, -2), (2, 0), (-2, 0)]
RARE = set("jqxzkvwyb")
BOOKUSED = set()   # answers already used elsewhere in the book (the filler avoids them)


def fill(black, rng, deadline):
    slots = [cells for d, cells in runs_of(black)]
    letters = {}
    used = set()
    nodes = [0]

    def pattern(cells):
        return "".join(letters.get(p, ".") for p in cells)

    def present():
        return set(letters.values())

    def rec():
        nodes[0] += 1
        if time.time() > deadline or nodes[0] > 20000: return False
        best = None
        for i, cells in enumerate(slots):
            pt = pattern(cells)
            if "." not in pt: continue
            m = FIX.match(pt)
            k = m.bit_count()
            if k == 0: return False
            if best is None or k < best[0]:
                best = (k, i, m, pt)
                if k == 1: break
        if best is None:
            return True
        k, i, m, pt = best
        ws = FIX.words[len(pt)]
        idx = []
        mm = m
        while mm:
            low = mm & -mm; idx.append(low.bit_length() - 1); mm ^= low
        if len(idx) > 60: idx = rng.sample(idx, 60)
        have = present()
        missing = set(ABC) - have
        def score(j):
            w = ws[j]
            return rng.random() - (1.2 if w in BOOKUSED else 0) + 0.25 * ZIPF[w] + 2.5 * len(set(w) & missing & RARE) + 0.6 * len(set(w) & missing)
        idx.sort(key=score, reverse=True)
        cells = slots[i]
        for j in idx[:12]:
            w = ws[j]
            if w in used: continue
            # every other fully-determined crossing must be a word: handled by match() on next level
            placed = [p for p, ch in zip(cells, w) if p not in letters]
            for p, ch in zip(cells, w): letters[p] = ch
            used.add(w)
            # quick check that crossings remain fillable
            okc = True
            for p in placed:
                for cs in slots:
                    if p in cs and cs is not cells:
                        pt2 = pattern(cs)
                        if not FIX.match(pt2): okc = False; break
                        if "." not in pt2 and pt2 in used and pt2 != w and pt2 not in [pattern(o) for o in slots if o is not cs]: pass
                if not okc: break
            if okc and rec(): return True
            used.discard(w)
            for p in placed: del letters[p]
        return False

    if not rec(): return None
    words = ["".join(letters[p] for p in cells) for cells in slots]
    if len(set(words)) != len(words): return None
    return letters, slots, words


def make_grid(rng, need_pangram=True, budget=6.0):
    t0 = time.time()
    while time.time() - t0 < budget:
        black = template(rng)
        res = fill(black, rng, time.time() + 1.5)
        if not res: continue
        letters, slots, words = res
        if need_pangram and set(letters.values()) != set(ABC): continue
        return black, letters, slots, words
    return None


# ------------------------------------------------------------------ uniqueness solver (full dictionary)
def signature(seq):
    first = {}
    return tuple(first.setdefault(x, len(first)) for x in seq)


class SigIndex:
    def __init__(s, words):
        s.groups = {}
        for w in words:
            s.groups.setdefault((len(w), signature(w)), []).append(w)
        s.bits = {}
        for key, ws in s.groups.items():
            b = {}
            for i, w in enumerate(ws):
                bit = 1 << i
                for p, ch in enumerate(w):
                    b[(p, ch)] = b.get((p, ch), 0) | bit
            s.bits[key] = b


VIX = SigIndex(VER)


def count_solutions(entries, givens, limit=2, deadline=None):
    """entries: list of number tuples. givens: {num: letter}. Returns list of up to `limit` full keys {num: letter}."""
    groups = []
    for e in entries:
        key = (len(e), signature(e))
        groups.append((key, len(VIX.groups.get(key, []))))
    sols = []
    assign = dict(givens)
    usedl = set(givens.values())

    def cands(i):
        e = entries[i]; key = groups[i][0]
        b = VIX.bits.get(key)
        if b is None: return 0
        m = (1 << groups[i][1]) - 1
        seen = set()
        for p, n in enumerate(e):
            if n in seen: continue
            seen.add(n)
            if n in assign:
                m &= b.get((p, assign[n]), 0)
            else:
                for l in usedl:
                    m &= ~b.get((p, l), 0)
            if not m: return 0
        return m

    def rec():
        if deadline and time.time() > deadline: raise TimeoutError
        best = None
        for i, e in enumerate(entries):
            if all(n in assign for n in e): continue
            m = cands(i)
            k = m.bit_count()
            if k == 0: return
            if best is None or k < best[0]:
                best = (k, i, m)
                if k == 1: break
        if best is None:
            # all entries determined; check full words exist (they do, by construction of candidates)
            for i, e in enumerate(entries):
                w = "".join(assign[n] for n in e)
                if w not in VSET: return
            sols.append(dict(assign)); return
        k, i, m = best
        ws = VIX.groups[groups[i][0]]
        e = entries[i]
        while m:
            low = m & -m; j = low.bit_length() - 1; m ^= low
            w = ws[j]
            new = []
            okw = True
            for n, ch in zip(e, w):
                if n in assign:
                    if assign[n] != ch: okw = False; break
                elif n not in [x for x, _ in new]:
                    if ch in usedl: okw = False; break
                    new.append((n, ch))
            if not okw: continue
            if len(set(ch for _, ch in new)) != len(new): continue
            for n, ch in new: assign[n] = ch; usedl.add(ch)
            rec()
            for n, ch in new: del assign[n]; usedl.discard(ch)
            if len(sols) >= limit: return

    rec()
    return sols


VSET = set(VER)


def encode(letters, slots, rng):
    perm = list(ABC); rng.shuffle(perm)
    num = {ch: i + 1 for i, ch in enumerate(perm)}
    entries = [tuple(num[letters[p]] for p in cells) for cells in slots]
    return num, entries


def choose_givens(num, entries, rng, target, deadline):
    key = {n: ch for ch, n in num.items()}
    nums = list(key)
    rng.shuffle(nums)
    # avoid giving away the rarest letters first; start with a random target-size set
    common = [n for n in nums if key[n] not in "jqxz"]
    giv = {n: key[n] for n in common[:max(1, target)]}
    for _ in range(26):
        sols = count_solutions(entries, giv, 2, deadline)
        if len(sols) == 1: break
        if not sols: raise RuntimeError("no solution?!")
        alt = [s for s in sols if s != key]
        diff = [n for n in nums if alt[0].get(n) != key[n] and n not in giv]
        n = rng.choice(diff); giv[n] = key[n]
    else:
        return None
    # try to trim back down to the target (harder puzzles) while staying unique
    for n in list(giv):
        if len(giv) <= target: break
        trial = {k: v for k, v in giv.items() if k != n}
        if len(count_solutions(entries, trial, 2, deadline)) == 1:
            giv = trial
    return giv


if __name__ == "__main__":
    import sys
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    t = time.time()
    g = make_grid(rng, budget=60)
    print("grid", time.time() - t)
    black, letters, slots, words = g
    for r in range(N):
        print(" ".join(letters.get((r, c), "#") for c in range(N)))
    print(len(words), "words", sorted(words, key=len)[-5:])
    num, entries = encode(letters, slots, rng)
    t = time.time()
    giv = choose_givens(num, entries, rng, 2, time.time() + 120)
    print("givens", giv and {n: c for n, c in giv.items()}, time.time() - t)
