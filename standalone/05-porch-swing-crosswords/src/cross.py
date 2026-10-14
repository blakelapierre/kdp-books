"""Freeform (criss-cross style) crossword layout generator used by master.py.

Places themed answers on a bounded grid so that every answer crosses at least one other, no two
answers touch side by side (so every across/down run of letters in the grid is a real answer),
and the finished grid can be filled in only one way from its own word bank (fill_count)."""
from __future__ import annotations
import random

DIRS = {"A": (0, 1), "D": (1, 0)}


class Layout:
    def __init__(s):
        s.cell = {}          # (r, c) -> letter
        s.dirs = {}          # (r, c) -> set of directions using the cell
        s.words = []         # (answer, r, c, dir)
        s.r0 = s.r1 = s.c0 = s.c1 = None

    def copy(s):
        n = Layout(); n.cell = dict(s.cell); n.dirs = {k: set(v) for k, v in s.dirs.items()}
        n.words = list(s.words); n.r0, n.r1, n.c0, n.c1 = s.r0, s.r1, s.c0, s.c1
        return n

    def check(s, w, r, c, d, W, H):
        """Return the number of crossings if w can go at (r, c, d), else -1."""
        dr, dc = DIRS[d]; pr, pc = DIRS["D" if d == "A" else "A"]
        if (r - dr, c - dc) in s.cell or (r + dr * len(w), c + dc * len(w)) in s.cell:
            return -1
        cross = 0
        for i, ch in enumerate(w):
            p = (r + dr * i, c + dc * i)
            if p in s.cell:
                if s.cell[p] != ch or d in s.dirs[p]:
                    return -1
                cross += 1
            else:
                if (p[0] + pr, p[1] + pc) in s.cell or (p[0] - pr, p[1] - pc) in s.cell:
                    return -1
        if s.words and cross == 0:
            return -1
        if s.words:
            r0 = min(s.r0, r); c0 = min(s.c0, c)
            r1 = max(s.r1, r + dr * (len(w) - 1)); c1 = max(s.c1, c + dc * (len(w) - 1))
            if r1 - r0 + 1 > H or c1 - c0 + 1 > W:
                return -1
        return cross

    def place(s, w, r, c, d):
        dr, dc = DIRS[d]
        for i, ch in enumerate(w):
            p = (r + dr * i, c + dc * i)
            s.cell[p] = ch; s.dirs.setdefault(p, set()).add(d)
        s.words.append((w, r, c, d))
        re_, ce = r + dr * (len(w) - 1), c + dc * (len(w) - 1)
        if s.r0 is None:
            s.r0, s.r1, s.c0, s.c1 = r, re_, c, ce
        else:
            s.r0 = min(s.r0, r); s.r1 = max(s.r1, re_); s.c0 = min(s.c0, c); s.c1 = max(s.c1, ce)

    def placements(s, w, W, H):
        out = []
        for (r, c), ch in s.cell.items():
            for i, wc in enumerate(w):
                if wc != ch:
                    continue
                for d in "AD":
                    if d in s.dirs[(r, c)]:
                        continue
                    dr, dc = DIRS[d]
                    rr, cc = r - dr * i, c - dc * i
                    x = s.check(w, rr, cc, d, W, H)
                    if x > 0:
                        out.append((x, rr, cc, d))
        return out

    def area(s):
        return (s.r1 - s.r0 + 1) * (s.c1 - s.c0 + 1)


def attempt(words, W, H, hi, rng):
    order = sorted(words, key=lambda w: -len(w) + rng.uniform(-2.5, 2.5))
    L = Layout()
    first = order.pop(0)
    if len(first) > W:
        return None
    L.place(first, 0, 0, "A")
    while order and len(L.words) < hi:
        best = None
        for w in order:
            for x, r, c, d in L.placements(w, W, H):
                dr, dc = DIRS[d]
                r0 = min(L.r0, r); c0 = min(L.c0, c)
                r1 = max(L.r1, r + dr * (len(w) - 1)); c1 = max(L.c1, c + dc * (len(w) - 1))
                grow = (r1 - r0 + 1) * (c1 - c0 + 1) - L.area()
                sc = x * 6 - grow * 0.35 + len(w) * 0.4 + rng.uniform(0, 3)
                if best is None or sc > best[0]:
                    best = (sc, w, r, c, d)
        if best is None:
            break
        _, w, r, c, d = best
        L.place(w, r, c, d); order.remove(w)
    return L


def slots(rows):
    """Every maximal across/down run of 2+ letters in a grid (list of strings, '.' = no cell)."""
    H, W = len(rows), len(rows[0]); out = []
    for r in range(H):
        for c in range(W):
            if rows[r][c] == ".":
                continue
            for d, (dr, dc) in DIRS.items():
                pr, pc = r - dr, c - dc
                if 0 <= pr < H and 0 <= pc < W and rows[pr][pc] != ".":
                    continue
                L = 0
                while r + dr * L < H and c + dc * L < W and rows[r + dr * L][c + dc * L] != ".":
                    L += 1
                if L >= 2:
                    out.append((r, c, d, L))
    return out


def fill_count(rows, bank, limit=2):
    """How many ways (up to limit) the grid shape can be filled using each bank word once."""
    sl = slots(rows)
    cells = [[(r + DIRS[d][0] * i, c + DIRS[d][1] * i) for i in range(L)] for r, c, d, L in sl]
    from collections import Counter
    avail = Counter(bank)
    grid = {}
    count = [0]

    def ok(word, cs):
        return all(grid.get(p, ch) == ch for p, ch in zip(cs, word))

    todo = list(range(len(sl)))

    def rec():
        if count[0] >= limit:
            return
        if not todo:
            count[0] += 1; return
        # most constrained slot first
        best = None
        for k in todo:
            cands = [w for w in avail if avail[w] > 0 and len(w) == len(cells[k]) and ok(w, cells[k])]
            if best is None or len(cands) < len(best[1]):
                best = (k, cands)
                if not cands:
                    return
        k, cands = best
        todo.remove(k)
        for w in cands:
            added = [p for p in cells[k] if p not in grid]
            for p, ch in zip(cells[k], w):
                grid[p] = ch
            avail[w] -= 1
            rec()
            avail[w] += 1
            for p in added:
                del grid[p]
        todo.append(k)

    rec()
    return count[0]


def to_rows(L):
    H = L.r1 - L.r0 + 1; W = L.c1 - L.c0 + 1
    g = [["."] * W for _ in range(H)]
    for (r, c), ch in L.cell.items():
        g[r - L.r0][c - L.c0] = ch
    return ["".join(x) for x in g]


def number(rows):
    """Standard crossword numbering -> list of (num, dir, r, c, answer)."""
    sl = sorted(slots(rows), key=lambda t: (t[0], t[1]))
    nums = {}; out = []
    for r, c, d, L in sl:
        if (r, c) not in nums:
            nums[(r, c)] = len(nums) + 1
        dr, dc = DIRS[d]
        out.append((nums[(r, c)], d, r, c, "".join(rows[r + dr * i][c + dc * i] for i in range(L))))
    return sorted(out, key=lambda t: (t[1], t[0]))


def generate(words, W, H, lo, hi, seed, tries=400):
    rng = random.Random(seed)
    best = None
    for t in range(tries):
        L = attempt(list(words), W, H, hi, rng)
        if L is None or len(L.words) < lo:
            continue
        rows = to_rows(L)
        cross = sum(1 for v in L.dirs.values() if len(v) == 2)
        dens = len(L.cell) / L.area()
        sc = len(L.words) * 10 + cross * 3 + dens * 25
        if best is None or sc > best[0]:
            if fill_count(rows, [w for w, *_ in L.words]) != 1:
                continue
            best = (sc, rows, L)
    return best
