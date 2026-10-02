"""Word searches, the maze, the fill-in, the logic grid, the snowball pyramid and the three ciphers."""
import random, itertools
from satutil import CNF

D8 = [(0, 1), (1, 0), (1, 1), (-1, 1), (0, -1), (-1, 0), (-1, -1), (1, -1)]

# ---------------------------------------------------------------- word search
def occurrences(grid, word):
    n, m = len(grid), len(grid[0]); out = []
    for r in range(n):
        for c in range(m):
            for dr, dc in D8:
                cells = [(r + dr * i, c + dc * i) for i in range(len(word))]
                if all(0 <= a < n and 0 <= b < m for a, b in cells) and "".join(grid[a][b] for a, b in cells) == word:
                    out.append(cells)
    return out

def gen_wordsearch(n, pool, message, dirs, seed, max_words=30):
    """Place words from `pool` until exactly len(message) cells stay uncovered; fill those with the message.
    Every listed word must then occur exactly once in the finished grid (checked in all 8 directions)."""
    rnd = random.Random(seed); target = len(message)
    for attempt in range(20000):
        g = [[None] * n for _ in range(n)]; placed = {}
        ws = pool[:]; rnd.shuffle(ws); ws.sort(key=lambda w: -len(w) + rnd.random() * 3)
        free = n * n
        for w in ws:
            if free == target or len(placed) >= max_words: break
            opts = []
            for r in range(n):
                for c in range(n):
                    for dr, dc in dirs:
                        cells = [(r + dr * i, c + dc * i) for i in range(len(w))]
                        if not all(0 <= a < n and 0 <= b < n for a, b in cells): continue
                        if all(g[a][b] in (None, ch) for (a, b), ch in zip(cells, w)):
                            new = sum(g[a][b] is None for a, b in cells)
                            if new and free - new >= target: opts.append((new, cells))
            if not opts: continue
            rnd.shuffle(opts)
            new, cells = opts[0]
            for (a, b), ch in zip(cells, w): g[a][b] = ch
            placed[w] = cells; free -= new
        if free != target: continue
        cellsfree = [(r, c) for r in range(n) for c in range(n) if g[r][c] is None]
        for (r, c), ch in zip(cellsfree, message): g[r][c] = ch
        words = list(placed)
        if all(len(occurrences(g, w)) == 1 for w in words) and not any(w in "".join(message) for w in words):
            return dict(n=n, grid=["".join(r) for r in g], words=sorted(words), placed=placed,
                        message=message, leftover=cellsfree)
    raise RuntimeError("wordsearch failed")

# ---------------------------------------------------------------- maze
def gen_maze(h, w, answer, n_decoys, seed):
    rnd = random.Random(seed)
    while True:
        # randomised DFS (perfect maze = a spanning tree, so the route between any two cells is unique)
        seen = {(0, 0)}; stack = [(0, 0)]; edges = set()
        while stack:
            r, c = stack[-1]
            nb = [(r + dr, c + dc) for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)) if 0 <= r + dr < h and 0 <= c + dc < w and (r + dr, c + dc) not in seen]
            if not nb: stack.pop(); continue
            x = rnd.choice(nb); edges.add(frozenset([(r, c), x])); seen.add(x); stack.append(x)
        # path start (0,0) -> end (h-1,w-1)
        adj = {}
        for e in edges:
            a, b = tuple(e); adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
        prev = {(0, 0): None}; q = [(0, 0)]
        for x in q:
            for y in adj[x]:
                if y not in prev: prev[y] = x; q.append(y)
        path = []; x = (h - 1, w - 1)
        while x: path.append(x); x = prev[x]
        path.reverse()
        if len(path) < h * w * 0.28: continue
        L = len(answer)
        idx = [round((i + 1) * (len(path) - 1) / (L + 1)) for i in range(L)]
        letters = {path[i]: ch for i, ch in zip(idx, answer)}
        off = [x for x in adj if x not in set(path)]
        rnd.shuffle(off)
        dec = {}
        for x in off:
            if len(dec) >= n_decoys: break
            if all(abs(x[0] - y[0]) + abs(x[1] - y[1]) > 2 for y in list(dec) + list(letters)):
                dec[x] = rnd.choice("ABCDEFGHIKLMNOPRSTUWY")
        return dict(h=h, w=w, edges=sorted([sorted(e) for e in edges]), path=path, letters={f"{r},{c}": ch for (r, c), ch in {**letters, **dec}.items()},
                    answer_cells=[path[i] for i in idx])

# ---------------------------------------------------------------- fill-in (kriss-kross)
def gen_fillin(words, n, seed, want, need=None, tries=4000):
    rnd = random.Random(seed)
    for attempt in range(tries):
        g = {}; slots = []
        pool = words[:]; rnd.shuffle(pool)
        first = max(pool[:4], key=len); pool.remove(first)
        r0 = n // 2; c0 = (n - len(first)) // 2
        def put(w, r, c, d):
            cells = [(r + i * (d == "D"), c + i * (d == "A")) for i in range(len(w))]
            for x, ch in zip(cells, w): g[x] = ch
            slots.append(dict(word=w, r=r, c=c, d=d, cells=cells))
        put(first, r0, c0, "A")
        def can(w, r, c, d):
            cells = [(r + i * (d == "D"), c + i * (d == "A")) for i in range(len(w))]
            if not all(0 <= a < n and 0 <= b < n for a, b in cells): return False
            cross = 0
            for i, ((a, b), ch) in enumerate(zip(cells, w)):
                if (a, b) in g:
                    if g[(a, b)] != ch: return False
                    cross += 1
                else:
                    side = [(a + 1, b), (a - 1, b)] if d == "A" else [(a, b + 1), (a, b - 1)]
                    if any(s in g for s in side): return False
            before = (r - (d == "D"), c - (d == "A")); after = (cells[-1][0] + (d == "D"), cells[-1][1] + (d == "A"))
            if before in g or after in g: return False
            # no running along an existing parallel slot through a crossing cell
            for s in slots:
                if s["d"] == d and set(s["cells"]) & set(cells): return False
            return cross >= 1
        for w in pool * 3:
            if len(slots) >= want: break
            if any(sl["word"] == w for sl in slots): continue
            opts = []
            for (a, b), ch in list(g.items()):
                for i, wc in enumerate(w):
                    if wc != ch: continue
                    for d in "AD":
                        r, c = (a, b - i) if d == "A" else (a - i, b)
                        if can(w, r, c, d): opts.append((r, c, d))
            if opts:
                put(w, *rnd.choice(opts))
        if len(slots) < want: continue
        if need and any(sum(ch == L for w in (sl["word"] for sl in slots) for ch in w) < k for L, k in need.items()): continue
        words_ = [s["word"] for s in slots]; given = {}
        for _ in range(3):
            sols = fillin_count(slots, words_, given)
            if len(sols) != 2: break
            diff = [x for x in sols[0] if sols[0][x] != sols[1][x]]
            x = rnd.choice(diff); given[x] = g[x]
        if len(sols) == 1 and len(given) <= 1:
            return dict(n=n, slots=slots, words=sorted(words_), given={f"{a},{b}": ch for (a, b), ch in given.items()})
    raise RuntimeError("fillin failed")

def fillin_count(slots, words, given=None, limit=2):
    """Backtracking: assign each word to a slot of its length, crossings must agree. Returns solutions."""
    given = given or {}
    order = sorted(range(len(slots)), key=lambda i: -len(slots[i]["cells"]))
    sols = []
    def rec(k, grid, left):
        if len(sols) >= limit: return
        if k == len(order):
            sols.append(dict(grid)); return
        s = slots[order[k]]; tried = set()
        for j, w in enumerate(left):
            if len(w) != len(s["cells"]) or w in tried: continue
            tried.add(w)
            if all(grid.get(x, ch) == ch and given.get(x, ch) == ch for x, ch in zip(s["cells"], w)):
                g2 = dict(grid); g2.update(zip(s["cells"], w))
                rec(k + 1, g2, left[:j] + left[j + 1:])
    rec(0, {}, list(words))
    return sols

# ---------------------------------------------------------------- logic grid
NAMES = ["Sam", "Kit", "Ada", "Tom", "Eve"]
TOPS = ["marshmallows", "cinnamon", "whipped cream", "peppermint", "nutmeg"]
KNITS = ["scarf", "mittens", "bobble hat", "socks", "jumper"]

def lg_encode(clues):
    f = CNF(); X = lambda g, k, v: f.v(g, k, v)   # X(guest, category, value)
    cats = {"room": range(5), "top": range(5), "knit": range(5)}
    for cat, vals in cats.items():
        for g in range(5): f.eq([X(g, cat, v) for v in vals], 1)
        for v in vals: f.eq([X(g, cat, v) for g in range(5)], 1)
    for cl in clues:
        t = cl[0]
        if t == "is":            # guest g has cat=v
            _, g, cat, v = cl; f.add([X(g, cat, v)])
        elif t == "not":
            _, g, cat, v = cl; f.add([-X(g, cat, v)])
        elif t == "same":        # whoever has c1=v1 has c2=v2
            _, c1, v1, c2, v2 = cl
            for g in range(5): f.add([-X(g, c1, v1), X(g, c2, v2)])
        elif t == "diff":        # whoever has c1=v1 does not have c2=v2
            _, c1, v1, c2, v2 = cl
            for g in range(5): f.add([-X(g, c1, v1), -X(g, c2, v2)])
        elif t in ("left", "rightnext", "next"):   # A (c1=v1) vs B (c2=v2) by room
            _, c1, v1, c2, v2 = cl
            for a in range(5):
                for b in range(5):
                    for ra in range(5):
                        for rb in range(5):
                            ok = (ra < rb) if t == "left" else (rb == ra + 1) if t == "rightnext" else abs(ra - rb) == 1
                            if a == b and ra != rb: continue
                            if a == b and ra == rb: ok = False if t != "left" else False
                            if not ok:
                                f.add([-X(a, c1, v1), -X(a, "room", ra), -X(b, c2, v2), -X(b, "room", rb)])
    keys = [(g, cat, v) for g in range(5) for cat in cats for v in range(5)]
    return f, keys

def lg_solutions(clues, limit=2):
    f, keys = lg_encode(clues)
    return f.solutions(keys, limit)

def gen_logic(seed):
    rnd = random.Random(seed)
    # fixed room order spells the answer: rooms 0..4 hold Sam, Kit, Ada, Tom, Eve
    room = [0, 1, 2, 3, 4]
    top = list(range(5)); rnd.shuffle(top); knit = list(range(5)); rnd.shuffle(knit)
    val = {"room": room, "top": top, "knit": knit}
    def who(cat, v): return next(g for g in range(5) if val[cat][g] == v)
    cand = []
    for g in range(5):
        for cat in ("top", "knit"):
            cand.append(("is", g, cat, val[cat][g]))
            for v in range(5):
                if v != val[cat][g]: cand.append(("not", g, cat, v))
        for v in range(5):
            if v != room[g]: cand.append(("not", g, "room", v))
    for v1 in range(5):
        for v2 in range(5):
            g1 = who("top", v1)
            cand.append(("same" if val["knit"][g1] == v2 else "diff", "top", v1, "knit", v2))
    for a in range(5):
        for b in range(5):
            if a == b: continue
            for c1, c2 in (("top", "knit"), ("knit", "top"), ("top", "top"), ("knit", "knit")):
                ra, rb = room[a], room[b]
                if ra < rb: cand.append(("left", c1, val[c1][a], c2, val[c2][b]))
                if rb == ra + 1: cand.append(("rightnext", c1, val[c1][a], c2, val[c2][b]))
                if abs(ra - rb) == 1 and (c1, c2) in (("top", "knit"),): cand.append(("next", c1, val[c1][a], c2, val[c2][b]))
    # guest-name relational clues through room
    for a in range(5):
        for b in range(5):
            if a != b and room[b] == room[a] + 1: cand.append(("rightnext", "name", a, "name", b))
    cand = [c for c in cand if "name" not in c]   # names are tied to rooms only via the answer; keep clues about attributes + names
    rnd.shuffle(cand)
    # greedy: add clues until unique, then prune
    clues = []
    weights = {"is": 0.35, "not": 0.5, "same": 0.8, "diff": 0.7, "left": 1.0, "rightnext": 1.0, "next": 1.0}
    cand.sort(key=lambda c: -weights[c[0]] * rnd.random())
    for c in cand:
        clues.append(c)
        if len(lg_solutions(clues)) == 1: break
    for c in list(clues):
        t = [x for x in clues if x != c]
        if len(lg_solutions(t)) == 1: clues = t
    sol = lg_solutions(clues)
    assert len(sol) == 1
    return dict(clues=[list(c) for c in clues], room=room, top=top, knit=knit)

# ---------------------------------------------------------------- snowball pyramid
def pyramid_values(base):
    rows = [list(base)]
    while len(rows[-1]) > 1: rows.append([a + b for a, b in zip(rows[-1], rows[-1][1:])])
    return rows          # rows[0] = bottom

def pyr_propagate(n, known):
    k = dict(known); ch = True
    while ch:
        ch = False
        for r in range(1, n):
            for i in range(n - r):
                t, a, b = (r, i), (r - 1, i), (r - 1, i + 1)
                have = [x in k for x in (t, a, b)]
                if sum(have) == 2:
                    if t not in k: k[t] = k[a] + k[b]
                    elif a not in k: k[a] = k[t] - k[b]
                    else: k[b] = k[t] - k[a]
                    ch = True
    return k

def gen_pyramid(base, seed):
    rnd = random.Random(seed); n = len(base); V = pyramid_values(base)
    allc = [(r, i) for r in range(n) for i in range(n - r)]
    for attempt in range(5000):
        giv = {x: V[x[0]][x[1]] for x in rnd.sample([x for x in allc if x[0] > 0], 4) + rnd.sample([(0, i) for i in range(n)], 1)}
        k = pyr_propagate(n, giv)
        if len(k) == len(allc):
            for x in list(giv):
                t = {a: b for a, b in giv.items() if a != x}
                if len(pyr_propagate(n, t)) == len(allc): giv = t
            if sum(1 for x in giv if x[0] == 0) <= 1:
                return dict(n=n, givens={f"{r},{i}": v for (r, i), v in giv.items()}, values=V)
    raise RuntimeError

# ---------------------------------------------------------------- ciphers
def caesar(text, k): return "".join(chr((ord(ch) - 65 + k) % 26 + 65) if ch.isalpha() else ch for ch in text)

MORSE = {"A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---",
         "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
         "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--", "Z": "--.."}

# Pigpen: letters A-I in a # grid, J-R in a dotted # grid, S-V in an X, W-Z in a dotted X.
def pigpen_shape(ch):
    i = ord(ch) - 65
    if i < 18:
        dot = i >= 9; k = i % 9; r, c = divmod(k, 3)
        # which sides of the cell are drawn: grid cell (r,c) of the #
        sides = set()
        if r > 0: sides.add("N")
        if r < 2: sides.add("S")
        if c > 0: sides.add("W")
        if c < 2: sides.add("E")
        return ("grid", frozenset(sides), dot)
    j = i - 18; dot = j >= 4; k = j % 4
    return ("x", "NESW"[[0, 1, 3, 2][k]] if False else ["N", "W", "E", "S"][k], dot)
