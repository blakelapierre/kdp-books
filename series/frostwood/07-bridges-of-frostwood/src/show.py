"""Debug helper: print a puzzle (and its stored bridges) as ASCII art. Not used by the build."""
import sys, json
def show(p):
    g = [["." for _ in range(p["w"])] for _ in range(p["h"])]
    isl = p["islands"]
    for i, j, k in p.get("bridges", []):
        (r1, c1, _), (r2, c2, _) = isl[i], isl[j]
        if r1 == r2:
            for c in range(c1 + 1, c2): g[r1][c] = "-" if k == 1 else "="
        else:
            for r in range(r1 + 1, r2): g[r][c1] = "|" if k == 1 else "H"
    for r, c, n in isl: g[r][c] = str(n)
    return "\n".join(" ".join(row) for row in g)
