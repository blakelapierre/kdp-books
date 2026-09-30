"""Nonogram pictures + a pure line-logic solver (no guessing) and a backtracking solution counter."""
from functools import lru_cache

PICS = {
"CANDLE": """
.......#.......
......###......
......###......
.....#####.....
......###......
.......#.......
.....#####.....
.....#.#.#.....
.....##.##.....
.....#.#.#.....
.....##.##.....
.....#.#.#.....
..###########..
.#############.
...#########...
""",
"BELL": """
.......#.......
......###......
.....##.##.....
....##...##....
....#.....#....
...##.###.##...
...#..#.#..#...
...#..###..#...
..##.......##..
..#..#####..#..
.##.........##.
.#############.
......###......
.......#.......
...............
""",
}

def parse(s):
    rows = [l for l in s.strip("\n").split("\n")]
    return [[1 if ch == "#" else 0 for ch in r] for r in rows]

def clues_of(line):
    out = []; k = 0
    for v in line:
        if v: k += 1
        elif k: out.append(k); k = 0
    if k: out.append(k)
    return out or [0]

def picture_clues(g):
    R = [clues_of(r) for r in g]; C = [clues_of([g[r][c] for r in range(len(g))]) for c in range(len(g[0]))]
    return R, C

@lru_cache(None)
def arrangements(n, clue):
    clue = tuple(x for x in clue if x)
    if not clue: return [tuple([0] * n)]
    out = []
    def rec(i, pos, acc):
        if i == len(clue):
            out.append(tuple(acc + [0] * (n - len(acc)))); return
        rest = sum(clue[i + 1:]) + len(clue) - i - 1
        for s in range(pos, n - rest - clue[i] + 1):
            a = acc + [0] * (s - len(acc)) + [1] * clue[i]
            if i + 1 < len(clue): a = a + [0]
            rec(i + 1, len(a), a)
    rec(0, 0, [])
    return out

def line_solve(R, C, grid=None):
    h, w = len(R), len(C)
    g = grid or [[-1] * w for _ in range(h)]
    changed = True
    while changed:
        changed = False
        for axis in (0, 1):
            L = h if axis == 0 else w
            for i in range(L):
                cur = g[i] if axis == 0 else [g[r][i] for r in range(h)]
                cl = R[i] if axis == 0 else C[i]
                arr = [a for a in arrangements(len(cur), tuple(cl)) if all(x == -1 or x == y for x, y in zip(cur, a))]
                if not arr: return None
                for j in range(len(cur)):
                    if cur[j] != -1: continue
                    vs = {a[j] for a in arr}
                    if len(vs) == 1:
                        v = vs.pop()
                        if axis == 0: g[i][j] = v
                        else: g[j][i] = v
                        changed = True
    return g

def count_solutions(R, C, limit=2):
    h, w = len(R), len(C); sols = []
    def rec(g):
        g = line_solve(R, C, [row[:] for row in g])
        if g is None: return
        un = [(r, c) for r in range(h) for c in range(w) if g[r][c] == -1]
        if not un: sols.append(g); return
        r, c = un[0]
        for v in (1, 0):
            if len(sols) >= limit: return
            g2 = [row[:] for row in g]; g2[r][c] = v; rec(g2)
    rec([[-1] * w for _ in range(h)])
    return sols

if __name__ == "__main__":
    for k, s in PICS.items():
        g = parse(s); R, C = picture_clues(g)
        ls = line_solve(R, C)
        print(k, len(g), len(g[0]), "line-solvable:", ls is not None and all(-1 not in r for r in ls), "solutions:", len(count_solutions(R, C)))
