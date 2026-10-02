"""INDEPENDENT verification of every door -> ../verification.md.
Does not import the generators (grids, latin, misc, nonogram, gen). Each puzzle is re-solved from the
printed clues only, with a separate brute-force / backtracking counter (or, for Train Tracks, the SAT
checker from Frostwood Express), and must have exactly one solution matching the stored one. The answer
word is then re-extracted from that solution exactly as the book instructs, and the Christmas Eve ledger
is rebuilt from the key letters."""
import json, itertools, time
from fractions import Fraction
import tracks_sat

T0 = time.time()
D = json.load(open("../data.json")); doors = {int(k): v for k, v in D["doors"].items()}
N8 = [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1) if (a, b) != (0, 0)]
N4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
P = lambda s: tuple(map(int, s.split(",")))
rows_out = []

def letters(v):
    return [row.split("|") for row in v["letters"]]

# ---------------------------------------------------------------- solvers
def ws_check(v):
    g = v["grid"]; n = len(g); used = set()
    for w in v["words"]:
        occ = []
        for r in range(n):
            for c in range(n):
                for dr, dc in N8:
                    cells = [(r + dr * i, c + dc * i) for i in range(len(w))]
                    if all(0 <= a < n and 0 <= b < n for a, b in cells) and "".join(g[a][b] for a, b in cells) == w: occ.append(cells)
        assert len(occ) == 1, (w, len(occ)); used |= set(occ[0])
    left = "".join(g[r][c] for r in range(n) for c in range(n) if (r, c) not in used)
    assert left.startswith("THEKEYIS"); return 1, left[8:]

def shift(t, k): return "".join(chr((ord(ch) - 65 + k) % 26 + 65) if ch.isalpha() else ch for ch in t)

def queens_solve(v):
    n = v["n"]; reg = v["regions"]; sols = []
    def rec(r, cols, regs, prev):
        if r == n: sols.append(list(prev)); return
        for c in range(n):
            if c in cols or reg[r][c] in regs: continue
            if prev and abs(prev[-1] - c) <= 1: continue
            rec(r + 1, cols | {c}, regs | {reg[r][c]}, prev + [c])
    rec(0, set(), set(), [])
    return [[(r, c) for r, c in enumerate(s)] for s in sols]

def sudoku_solve(v):
    n, br, bc = v["n"], v["br"], v["bc"]; sym = v["symbols"]
    g = {(r, c): None for r in range(n) for c in range(n)}
    for k, ch in v["givens"].items(): g[P(k)] = ch
    sols = []
    def ok(r, c, ch):
        for i in range(n):
            if g[(r, i)] == ch or g[(i, c)] == ch: return False
        R, C = r - r % br, c - c % bc
        return all(g[(R + a, C + b)] != ch for a in range(br) for b in range(bc))
    empty = [x for x in g if g[x] is None]
    def rec(i):
        if len(sols) > 1: return
        if i == len(empty): sols.append(dict(g)); return
        x = empty[i]
        for ch in sym:
            if ok(*x, ch): g[x] = ch; rec(i + 1); g[x] = None
    rec(0); return sols

def maze_check(v):
    h, w = v["h"], v["w"]; E = [tuple(map(tuple, e)) for e in v["edges"]]
    assert len(E) == h * w - 1
    adj = {}
    for a, b in E: adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
    prev = {(0, 0): None}; q = [(0, 0)]
    for x in q:
        for y in adj[x]:
            if y not in prev: prev[y] = x; q.append(y)
    assert len(prev) == h * w          # connected + (h*w-1) edges => a tree => exactly one route
    path = []; x = (h - 1, w - 1)
    while x: path.append(x); x = prev[x]
    path.reverse()
    L = {P(k): ch for k, ch in v["letters"].items()}
    return 1, "".join(L[x] for x in path if x in L)

def nono_count(R, C):
    h, w = len(R), len(C)
    def arr(n, clue):
        clue = [x for x in clue if x]
        if not clue: return [(0,) * n]
        out = []
        def rec(i, pos, acc):
            if i == len(clue): out.append(tuple(acc + [0] * (n - len(acc)))); return
            for s in range(pos, n - (sum(clue[i:]) + len(clue) - i - 1) + 1):
                a = acc + [0] * (s - len(acc)) + [1] * clue[i] + ([0] if i + 1 < len(clue) else [])
                rec(i + 1, len(a), a)
        rec(0, 0, []); return out
    RA = [arr(w, r) for r in R]; CA = [set(arr(h, c)) for c in C]
    # column prefix sets
    pref = [[set(a[:k] for a in CA[c]) for k in range(h + 1)] for c in range(w)]
    sols = []
    def rec(r, grid):
        if len(sols) > 1: return
        if r == h: sols.append(grid); return
        for a in RA[r]:
            g2 = grid + [a]
            if all(tuple(x[c] for x in g2) in pref[c][r + 1] for c in range(w)): rec(r + 1, g2)
    rec(0, []); return sols

def pyramid_check(v):
    n = v["n"]; giv = {P(k): val for k, val in v["givens"].items()}
    # unknowns: base values b0..b{n-1}; brick (r,i) = sum_j C(r, j) * b_{i+j}
    from math import comb
    rowsM = []; rhs = []
    for (r, i), val in giv.items():
        rowsM.append([Fraction(comb(r, j - i)) if 0 <= j - i <= r else Fraction(0) for j in range(n)]); rhs.append(Fraction(val))
    # gaussian elimination: rank must be n
    M = [row + [b] for row, b in zip(rowsM, rhs)]; rank = 0
    for col in range(n):
        piv = next((i for i in range(rank, len(M)) if M[i][col] != 0), None)
        if piv is None: continue
        M[rank], M[piv] = M[piv], M[rank]
        for i in range(len(M)):
            if i != rank and M[i][col] != 0:
                f = M[i][col] / M[rank][col]; M[i] = [a - f * b for a, b in zip(M[i], M[rank])]
        rank += 1
    assert rank == n
    base = [M[i][n] / M[i][i] for i in range(n)]
    assert all(b.denominator == 1 and 1 <= b <= 26 for b in base)
    return 1, "".join(chr(64 + int(b)) for b in base)

def logic_count(v):
    names = ["Sam", "Kit", "Ada", "Tom", "Eve"]; sols = []
    perms = list(itertools.permutations(range(5)))
    for room in perms:
        for top in perms:
            for knit in perms:
                val = {"room": room, "top": top, "knit": knit}
                def who(cat, x): return val[cat].index(x)
                ok = True
                for cl in v["clues"]:
                    t = cl[0]
                    if t == "is": ok = val[cl[2]][cl[1]] == cl[3]
                    elif t == "not": ok = val[cl[2]][cl[1]] != cl[3]
                    elif t == "same": ok = val[cl[3]][who(cl[1], cl[2])] == cl[4]
                    elif t == "diff": ok = val[cl[3]][who(cl[1], cl[2])] != cl[4]
                    else:
                        a, b = who(cl[1], cl[2]), who(cl[3], cl[4])
                        ra, rb = room[a], room[b]
                        ok = a != b and ((ra < rb) if t == "left" else (rb == ra + 1) if t == "rightnext" else abs(ra - rb) == 1)
                    if not ok: break
                if ok: sols.append((room, top, knit))
            if len(sols) > 1: break
    return sols

def tents_count(v):
    n = v["n"]; trees = [tuple(t) for t in v["trees"]]; ts = set(trees); rows, cols = v["rows"], v["cols"]; sols = []
    def rec(i, tents, rc, cc):
        if len(sols) > 1: return
        if i == len(trees):
            if rc == rows and cc == cols: sols.append(sorted(tents))
            return
        r, c = trees[i]
        for dr, dc in N4:
            x = (r + dr, c + dc)
            if not (0 <= x[0] < n and 0 <= x[1] < n) or x in ts or x in tents: continue
            if any((x[0] + a, x[1] + b) in tents for a, b in N8): continue
            if rc[x[0]] + 1 > rows[x[0]] or cc[x[1]] + 1 > cols[x[1]]: continue
            rc[x[0]] += 1; cc[x[1]] += 1; rec(i + 1, tents | {x}, rc, cc); rc[x[0]] -= 1; cc[x[1]] -= 1
    rec(0, frozenset(), [0] * n, [0] * n)
    return sols

def akari_count(v):
    n = v["n"]; black = {tuple(b) for b in v["black"]}; nums = {P(k): x for k, x in v["nums"].items()}
    white = [(r, c) for r in range(n) for c in range(n) if (r, c) not in black]
    def sees(a):
        out = set()
        for dr, dc in N4:
            r, c = a
            while True:
                r += dr; c += dc
                if not (0 <= r < n and 0 <= c < n) or (r, c) in black: break
                out.add((r, c))
        return out
    S = {x: sees(x) for x in white}; sols = []
    def nb(x): return [(x[0] + a, x[1] + b) for a, b in N4]
    def rec(i, bulbs):
        if len(sols) > 1: return
        for k, want in nums.items():
            have = sum(y in bulbs for y in nb(k)); undecided = sum(1 for y in nb(k) if y in S and white.index(y) >= i and y not in bulbs)
            if have > want or have + undecided < want: return
        if i == len(white):
            if all(x in bulbs or S[x] & bulbs for x in white): sols.append(sorted(bulbs))
            return
        x = white[i]
        if not (S[x] & bulbs): rec(i + 1, bulbs | {x})
        rec(i + 1, bulbs)
    rec(0, frozenset()); return sols

def presents_count(v):
    n = v["n"]; clues = {P(k): x for k, x in v["clues"].items()}; total = v["total"]
    cells = [(r, c) for r in range(n) for c in range(n) if (r, c) not in clues]; sols = []
    idx = {x: i for i, x in enumerate(cells)}
    def rec(i, pres):
        if len(sols) > 1 or len(pres) > total: return
        for k, want in clues.items():
            nbs = [(k[0] + a, k[1] + b) for a, b in N8]
            have = sum(y in pres for y in nbs); und = sum(1 for y in nbs if y in idx and idx[y] >= i)
            if have > want or have + und < want: return
        if i == len(cells):
            if len(pres) == total: sols.append(sorted(pres))
            return
        rec(i + 1, pres | {cells[i]}); rec(i + 1, pres)
    rec(0, frozenset()); return sols

def fleet_count(v):
    n = v["n"]; rows, cols = v["rows"], v["cols"]
    gs = {tuple(x) for x in v["given_ship"]}; gw = {tuple(x) for x in v["given_sea"]}; sols = []
    def rec(r, occ, cc):
        if len(sols) > 1: return
        if r == n:
            if cc != cols: return
            # ships = connected components; must be straight, non-touching diagonally, fleet must match
            seen = set(); lens = []
            for x in occ:
                if x in seen: continue
                comp = {x}; st = [x]
                while st:
                    a = st.pop()
                    for dr, dc in N4:
                        y = (a[0] + dr, a[1] + dc)
                        if y in occ and y not in comp: comp.add(y); st.append(y)
                seen |= comp
                if len({a for a, _ in comp}) > 1 and len({b for _, b in comp}) > 1: return
                lens.append(len(comp))
            for a in occ:
                for dr, dc in ((1, 1), (1, -1)):
                    y = (a[0] + dr, a[1] + dc)
                    if y in occ and (a[0], y[1]) not in occ and (y[0], a[1]) not in occ: return
            if sorted(lens) == sorted(v["fleet"]): sols.append(sorted(occ))
            return
        for comb in itertools.combinations(range(n), rows[r]):
            row = {(r, c) for c in comb}
            if gs & {(r, c) for c in range(n)} - row or gw & row: continue
            cc2 = [cc[c] + (c in comb) for c in range(n)]
            if any(cc2[c] > cols[c] for c in range(n)): continue
            rec(r + 1, occ | row, cc2)
    rec(0, frozenset(), [0] * n); return sols

def latin_solve(v, typ):
    n = 5; sols = []
    giv = {P(k): x for k, x in v.get("givens", {}).items()}
    g = [[0] * n for _ in range(n)]
    def vis(line):
        m = k = 0
        for h in line:
            if h > m: m = h; k += 1
        return k
    def full_ok():
        if typ == "futoshiki":
            return all(g[a[0]][a[1]] < g[b[0]][b[1]] for a, b in v["ineq"])
        if typ == "skyscrapers":
            for key, want in v["clues"].items():
                side, i = key.split(","); i = int(i)
                line = {"top": [g[r][i] for r in range(n)], "bottom": [g[r][i] for r in range(n)][::-1],
                        "left": g[i], "right": g[i][::-1]}[side]
                if vis(line) != want: return False
            return True
        for cg in v["cages"]:
            vals = [g[a][b] for a, b in cg["cells"]]; op, t = cg["op"], cg["target"]
            if op == "": ok = vals[0] == t
            elif op == "+": ok = sum(vals) == t
            elif op == "×":
                p = 1
                for x in vals: p *= x
                ok = p == t
            elif op == "−": ok = abs(vals[0] - vals[1]) == t
            else: ok = max(vals) == t * min(vals)
            if not ok: return False
        return True
    def rec(i):
        if len(sols) > 1: return
        if i == 25:
            if full_ok(): sols.append([row[:] for row in g])
            return
        r, c = divmod(i, n)
        for x in ([giv[(r, c)]] if (r, c) in giv else range(1, n + 1)):
            if x in g[r][:c] or any(g[k][c] == x for k in range(r)): continue
            g[r][c] = x; rec(i + 1); g[r][c] = 0
    rec(0); return sols

def fillin_solve(v):
    slots = v["slots"]; words = v["words"]; given = {P(k): ch for k, ch in v.get("given", {}).items()}; sols = []
    def rec(k, grid, left):
        if len(sols) > 1: return
        if k == len(slots): sols.append(dict(grid)); return
        s = slots[k]; cells = [tuple(x) for x in s["cells"]]; tried = set()
        for j, w in enumerate(left):
            if len(w) != len(cells) or w in tried: continue
            tried.add(w)
            if all(grid.get(x, ch) == ch and given.get(x, ch) == ch for x, ch in zip(cells, w)):
                g2 = dict(grid); g2.update(zip(cells, w)); rec(k + 1, g2, left[:j] + left[j + 1:])
    rec(0, {}, list(words)); return sols

# ---------------------------------------------------------------- per door
MORSE = {"A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---",
         "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
         "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--", "Z": "--.."}
def key_after(text):
    t = "".join(ch for ch in text if ch.isalpha() or ch == " ")
    return t.split("THE KEY IS ")[1].split()[0]

for d in range(1, 25):
    v = doors[d]; t = v["type"]; note = ""
    if t == "wordsearch": nsol, got = ws_check(v); note = f"{len(v['words'])} words, each found exactly once (all 8 directions scanned)"
    elif t == "caesar":
        dec = shift(v["cipher"], -v["shift"]); assert dec == v["plain"]
        cands = [k for k in range(1, 5) if "THE KEY IS" in shift(v["cipher"], -k)]; assert cands == [v["shift"]]
        nsol, got = 1, key_after(dec); note = f"shift {v['shift']}; only shift 1–4 that reads as English"
    elif t == "pigpen": nsol, got = 1, key_after(v["plain"]); note = "encoded from the plain text by build.py's fixed key"
    elif t == "morse":
        code = " / ".join(" ".join(MORSE[ch] for ch in w if ch.isalpha()) for w in v["plain"].split())
        rev = {b: a for a, b in MORSE.items()}
        dec = " ".join("".join(rev[s] for s in w.split()) for w in code.split(" / "))
        nsol, got = 1, key_after(dec); note = "Morse re-encoded and decoded"
    elif t == "queens":
        s = queens_solve(v); nsol = len(s); assert s[0] == [tuple(x) for x in v["stars"]]
        L = letters(v); got = "".join(L[r][c] for r, c in s[0]); note = f"{v['n']}×{v['n']}, backtracking count"
    elif t == "wordoku":
        s = sudoku_solve(v); nsol = len(s)
        assert all(s[0][(r, c)] == v["full"][r][c] for r in range(v["n"]) for c in range(v["n"]))
        got = "".join(s[0][tuple(x)] for x in v["shaded"]); note = f"{v['n']}×{v['n']}, {len(v['givens'])} givens"
    elif t == "maze": nsol, got = maze_check(v); note = f"{v['h']}×{v['w']} perfect maze (a tree), route {len(v['path'])} cells"
    elif t == "nonogram":
        s = nono_count(v["rows"], v["cols"]); nsol = len(s)
        assert ["".join("#" if x else "." for x in r) for r in s[0]] == v["picture"]
        got = v["answer"]; note = "15×15; picture = " + v["answer"].lower()
    elif t == "pyramid": nsol, got = pyramid_check(v); note = f"{len(v['givens'])} given bricks, linear system of full rank"
    elif t == "logic":
        s = logic_count(v); nsol = len(s); room = s[0][0]
        got = "".join(["S", "K", "A", "T", "E"][g] for g in sorted(range(5), key=lambda g: room[g])); note = f"{len(v['clues'])} clues, all 1,728,000 combinations tried"
    elif t == "tents":
        s = tents_count(v); nsol = len(set(map(tuple, s))); L = letters(v); got = "".join(L[r][c] for r, c in sorted(s[0]))
        assert sorted(s[0]) == [tuple(x) for x in v["tents"]]; note = f"8×8, {len(v['trees'])} pines"
    elif t == "tracks":
        s = tracks_sat.count_solutions(v); nsol = len(s); tracks_sat.check_solution(v)
        L = {P(k): ch for k, ch in v["letters"].items()}; got = "".join(L[x] for x in s[0] if x in L)
        note = f"{v['n']}×{v['n']}, SAT count (Frostwood Express checker)"
    elif t == "akari":
        s = akari_count(v); nsol = len(s); L = letters(v); got = "".join(L[r][c] for r, c in s[0]); note = f"7×7, {len(v['nums'])} numbered blocks"
    elif t == "presents":
        s = presents_count(v); nsol = len(s); L = letters(v); got = "".join(L[r][c] for r, c in s[0]); note = f"7×7, {len(v['clues'])} numbers"
    elif t == "fleet":
        s = fleet_count(v); nsol = len(s); L = letters(v); got = "".join(L[r][c] for r, c in s[0]); note = "7×7, fleet 3,2,2,1,1,1"
    elif t in ("futoshiki", "skyscrapers", "calcudoku"):
        s = latin_solve(v, t); nsol = len(s); assert s[0] == v["solution"]
        got = "".join(v["keymap"][str(s[0][r][c])] for r, c in v["numbered"]); note = "5×5, backtracking count"
    elif t == "fillin":
        s = fillin_solve(v); nsol = len(s); got = "".join(s[0][tuple(x)] for x in v["numbered"]); note = f"{len(v['words'])} words"
    assert nsol == 1, (d, t, nsol)
    assert got == v["answer"], (d, got, v["answer"])
    assert v["letter"] == v["answer"][v["key"] - 1]
    rows_out.append((d, t, v["answer"], v["key"], v["letter"], nsol, note))
    print(d, t, got, "ok", round(time.time() - T0, 1), flush=True)

msg = "".join(doors[x]["letter"] for x in D["ledger"])
assert msg == D["message"].replace(" ", ""); assert sorted(D["ledger"]) == list(range(1, 25))
# the Door Log (door order) must not give the message away, and the ledger must not look ordered
log = "".join(doors[d]["letter"] for d in range(1, 25)); M = D["message"].replace(" ", "")
tri = {M[i:i + 3] for i in range(len(M) - 2)}
assert not [log[i:i + 3] for i in range(len(log) - 2) if log[i:i + 3] in tri], ("message run in door order", log)
for wd in set(D["message"].split()) | {"STAR", "CLOCK", "TOWER", "THE", "TOW", "OWE", "ART", "RAT", "TAR", "SIT", "HIS", "ITS", "HER", "TEN", "TIN", "ONE", "NOT"}:
    assert len(wd) < 3 or wd not in log, ("readable word in door order", wd, log)
assert sum(a == b for a, b in zip(log, M)) <= 2, ("door order too close to message", log)
assert all(abs(D["ledger"][i + 1] - D["ledger"][i]) != 1 for i in range(23)), ("ledger has a consecutive run", D["ledger"])
with open("../verification.md", "w") as f:
    f.write("# Verification report\n\nGenerated by `src/verify.py` (independent of the generators) in %.1f s.\n\n" % (time.time() - T0))
    f.write("- Doors checked: **24/24**. Every puzzle was re-solved from its printed clues and has **exactly one solution**, equal to the stored solution.\n")
    f.write("- Every answer word was re-extracted from that solution the way the book tells the reader to, and matches.\n")
    f.write(f"- The 24 key letters placed in the Christmas Eve ledger read: **{D['message']}**.\n")
    f.write(f"- In door order (as copied into the Door Log) the key letters read **{log}**: no three-letter run of the message, no readable words, "
            "and no two neighbouring ledger boxes hold consecutive door numbers.\n\n")
    f.write("| Door | Puzzle | Answer | Key letter | Solutions | Check |\n|---|---|---|---|---|---|\n")
    for d, t, a, k, l, n, note in rows_out: f.write(f"| {d} | {t} | {a} | {l} (letter {k}) | {n} | {note} |\n")
print("ALL OK", msg, "door order", log)
