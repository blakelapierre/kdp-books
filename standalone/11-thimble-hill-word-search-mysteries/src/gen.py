"""Generates the 60 word search grids -> ../data.json (deterministic seeds). Run from src/: python3 gen.py
Each grid hides the case's word list; the unused squares, read left to right and top to bottom, spell the hidden clue."""
import json, os, random
import content
N = 12
ALL8 = [(0, 1), (1, 0), (1, 1), (-1, 1), (0, -1), (-1, 0), (-1, -1), (1, -1)]
DIRS = {1: [(0, 1), (1, 0), (1, 1)], 2: [(0, 1), (1, 0), (1, 1), (-1, 1)], 3: ALL8}
LEVEL_NAME = {1: "Gentle", 2: "Curious", 3: "Sharp-Eyed"}
BAD = [w.strip().upper() for w in open(os.path.join(os.path.dirname(__file__), "badwords.txt")) if w.strip().isalpha() and len(w.strip()) >= 4]


def level(ci):
    return 1 if ci < 3 else 2 if ci < 7 else 3


def count(grid, w):
    n = 0
    for r in range(N):
        for c in range(N):
            for dr, dc in ALL8:
                ok = True
                for i, ch in enumerate(w):
                    rr, cc = r + dr * i, c + dc * i
                    if not (0 <= rr < N and 0 <= cc < N) or grid[rr][cc] != ch: ok = False; break
                if ok: n += 1
    return n


def bad_hits(g, placed):
    """Offensive letter runs in any of the 8 directions, ignoring runs that sit wholly inside a hidden list word
    (BUTTER legitimately contains BUTT)."""
    inside = []
    for w, r, c, dr, dc in placed:
        cells = [(r + dr * i, c + dc * i) for i in range(len(w))]
        inside.append(set(cells))
    hits = []
    for r in range(N):
        for c in range(N):
            for dr, dc in ALL8:
                s = ""; rr, cc = r, c
                while 0 <= rr < N and 0 <= cc < N and len(s) < 12: s += g[rr][cc]; rr += dr; cc += dc
                for b in BAD:
                    if s.startswith(b):
                        cells = {(r + dr * i, c + dc * i) for i in range(len(b))}
                        if not any(cells <= ins for ins in inside): hits.append((b, r, c, dr, dc))
    return hits


def attempt(rng, pool, used, msg, dirs):
    U = len(msg)
    grid = [[None] * N for _ in range(N)]
    cand = [w for w in pool if used.get(w, 0) < 4 and 3 <= len(w) <= N and w != w[::-1]]
    rng.shuffle(cand)
    cand.sort(key=lambda w: used.get(w, 0) * 1.5 - len(w) + rng.random() * 4)
    placed = []
    unc = N * N
    for w in cand:
        if unc == U: break
        if any(w in p or p in w or w[::-1] in p or p in w[::-1] for p, *_ in placed): continue
        opts = []
        for r in range(N):
            for c in range(N):
                for dr, dc in dirs:
                    er, ec = r + dr * (len(w) - 1), c + dc * (len(w) - 1)
                    if not (0 <= er < N and 0 <= ec < N): continue
                    ov = 0; ok = True
                    for i, ch in enumerate(w):
                        g = grid[r + dr * i][c + dc * i]
                        if g is None: continue
                        if g != ch: ok = False; break
                        ov += 1
                    if not ok or ov == len(w): continue
                    new = len(w) - ov
                    if unc - new < U: continue
                    opts.append((ov + rng.random() * 1.5, r, c, dr, dc, new))
        if not opts: continue
        opts.sort(reverse=True)
        _, r, c, dr, dc, new = opts[rng.randrange(min(4, len(opts)))]
        for i, ch in enumerate(w): grid[r + dr * i][c + dc * i] = ch
        placed.append((w, r, c, dr, dc)); unc -= new
    if unc != U or not (12 <= len(placed) <= 24): return None
    k = 0
    for r in range(N):
        for c in range(N):
            if grid[r][c] is None: grid[r][c] = msg[k]; k += 1
    g = ["".join(row) for row in grid]
    for w, *_ in placed:
        if count(g, w) != 1: return None
    if bad_hits(g, placed): return None
    return g, placed


def build_case(ci):
    case = content.CASES[ci]
    cache = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tmp", "case-%02d.json" % (ci + 1))
    if os.path.exists(cache):
        old = json.load(open(cache))
        if [p["clue"] for p in old["puzzles"]] == [b[1] for b in case["beats"]] and old.get("words") == case["words"]:
            return old["data"]
    pool = case["words"].split()
    assert len(pool) == len(set(pool)), case["title"]
    used = {}
    lv = level(ci)
    puzzles = []
    for bi, (story, clue) in enumerate(case["beats"]):
        msg = clue.replace(" ", "")
        seed = 1000000 * (ci + 1) + 30000 * bi
        while True:
            seed += 1
            assert seed < 1000000 * (ci + 1) + 30000 * (bi + 1), "no grid found"
            res = attempt(random.Random(seed), pool, used, msg, DIRS[lv])
            if res: break
        g, placed = res
        for w, *_ in placed: used[w] = used.get(w, 0) + 1
        puzzles.append(dict(seed=seed, grid=g, clue=clue, words=sorted(w for w, *_ in placed),
                            placements=[dict(word=w, r=r, c=c, dr=dr, dc=dc) for w, r, c, dr, dc in placed]))
        print(case["title"], bi + 1, "seed", seed, "words", len(placed), flush=True)
    data = dict(title=case["title"], level=lv, level_name=LEVEL_NAME[lv], directions=[list(d) for d in DIRS[lv]], puzzles=puzzles)
    json.dump(dict(puzzles=puzzles, words=case["words"], data=data), open(cache, "w"))
    return data


def main():
    from multiprocessing import Pool
    with Pool(10) as p:
        cases = p.map(build_case, range(len(content.CASES)))
    pid = 0
    for c in cases:
        for pz in c["puzzles"]:
            pid += 1; pz["id"] = pid
    out = {"size": N, "cases": cases}
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data.json"), "w"), indent=1)
    print("wrote data.json", pid, "puzzles")


if __name__ == "__main__":
    main()
