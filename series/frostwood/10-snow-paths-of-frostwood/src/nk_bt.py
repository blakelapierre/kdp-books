"""Independent Nurikabe solution counter: depth-first search with simple forced moves.
Shares no code with nurikabe.py or the SAT model. Used only by verify.py."""
import sys
sys.setrecursionlimit(10000)
U, P, S = 0, 1, 2      # unknown, path (shaded), snow (unshaded)


def bt_solutions(p, limit=2):
    w, h = p["w"], p["h"]; n = w * h
    adj = []
    for i in range(n):
        r, c = divmod(i, w); a = []
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            rr, cc = r + dr, c + dc
            if 0 <= rr < h and 0 <= cc < w: a.append(rr * w + cc)
        adj.append(a)
    num = {r * w + c: k for r, c, k in p["clues"]}
    snow_total = sum(num.values()); path_total = n - snow_total
    squares = [(r * w + c, r * w + c + 1, r * w + w + c, r * w + w + c + 1) for r in range(h - 1) for c in range(w - 1)]
    found = []

    def groups(g, kind):
        lab = [-1] * n; out = []
        for i in range(n):
            if g[i] != kind or lab[i] >= 0: continue
            q = [i]; lab[i] = len(out); mem = []
            while q:
                x = q.pop(); mem.append(x)
                for y in adj[x]:
                    if g[y] == kind and lab[y] < 0: lab[y] = len(out); q.append(y)
            out.append(mem)
        return lab, out

    def settle(g):
        """Apply forced moves in place. Returns False on a dead end."""
        while True:
            moved = False
            if g.count(P) > path_total or g.count(S) > snow_total: return False
            for sq in squares:
                if g[sq[0]] == P and g[sq[1]] == P and g[sq[2]] == P and g[sq[3]] == P: return False
            lab, gs = groups(g, S)
            info = []
            for mem in gs:
                ks = [num[x] for x in mem if x in num]
                if len(ks) > 1: return False
                k = ks[0] if ks else 0
                if k and len(mem) > k: return False
                edge = {y for x in mem for y in adj[x] if g[y] == U}
                if not edge and (not k or len(mem) != k): return False
                info.append((k, mem, edge))
            plab, pgs = groups(g, P)
            if len(pgs) > 1:
                for mem in pgs:
                    if not any(g[y] == U for x in mem for y in adj[x]): return False
            for k, mem, edge in info:
                if k and len(mem) == k:
                    for y in edge: g[y] = P; moved = True
            if moved: continue
            for i in range(n):
                if g[i] != U: continue
                cl = {lab[y] for y in adj[i] if g[y] == S and info[lab[y]][0]}
                if len(cl) > 1: g[i] = P; moved = True
            if moved: continue
            # cells no numbered patch can reach
            ok = [False] * n
            for gi, (k, mem, edge) in enumerate(info):
                if not k: continue
                left = k - len(mem)
                for x in mem: ok[x] = True
                seen = set(mem); front = list(mem)
                for step in range(left):
                    nxt = []
                    for x in front:
                        for y in adj[x]:
                            if y in seen or g[y] == P: continue
                            if g[y] == S and info[lab[y]][0]: continue
                            if any(g[z] == S and lab[z] != gi and info[lab[z]][0] for z in adj[y]): continue
                            seen.add(y); nxt.append(y); ok[y] = True
                    front = nxt
            for k, mem, edge in info:
                if not k and not any(ok[x] for x in mem): return False
            for i in range(n):
                if g[i] == U and not ok[i]: g[i] = P; moved = True
            if moved: continue
            for sq in squares:
                vals = [g[x] for x in sq]
                if vals.count(P) == 3 and vals.count(U) == 1:
                    g[sq[vals.index(U)]] = S; moved = True
            if not moved: return True

    def full_ok(g):
        lab, gs = groups(g, P)
        if len(gs) != 1: return False
        for sq in squares:
            if all(g[x] == P for x in sq): return False
        lab, gs = groups(g, S)
        for mem in gs:
            ks = [num[x] for x in mem if x in num]
            if len(ks) != 1 or ks[0] != len(mem): return False
        return True

    def go(g):
        if len(found) >= limit: return
        if not settle(g): return
        if U not in g:
            if full_ok(g): found.append(["".join("#" if g[r * w + c] == P else "." for c in range(w)) for r in range(h)])
            return
        # branch next to an unfinished numbered patch if possible
        lab, gs = groups(g, S); pick = None; best = None
        for mem in gs:
            ks = [num[x] for x in mem if x in num]
            if ks and len(mem) < ks[0]:
                edge = sorted({y for x in mem for y in adj[x] if g[y] == U})
                if edge and (best is None or len(edge) < best): best = len(edge); pick = edge[0]
        if pick is None: pick = g.index(U)
        for val in (S, P):
            h2 = list(g); h2[pick] = val; go(h2)

    g = [U] * n
    for i in num: g[i] = S
    go(g)
    return found


if __name__ == "__main__":
    import json
    d = json.load(open("../data.json")); p = d["Easy"][0]
    print(bt_solutions(p), p["sol"])
