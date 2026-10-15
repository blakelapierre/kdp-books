"""Debug helper: print a puzzle (and optionally its loop) as ASCII art. Not used by the build."""
import sys, json
from slither import Geo
def show(p, loop=True):
    g = Geo(p["w"], p["h"]); L = set(p["loop"]) if loop else set(); out = []
    for r in range(g.h + 1):
        out.append("+" + "+".join("--" if g.H(r, c) in L else "  " for c in range(g.w)) + "+")
        if r < g.h:
            row = ""
            for c in range(g.w + 1):
                row += "|" if g.V(r, c) in L else " "
                if c < g.w:
                    n = p["clues"][r][c]; row += (str(n) if n is not None else ".") + " "
            out.append(row)
    return "\n".join(out)
if __name__ == "__main__":
    D = json.load(open("../data.json")); n = int(sys.argv[1])
    p = D["Example"][0] if n == 0 else [q for b in ("Easy", "Medium", "Hard", "Expert") for q in D[b] if q["num"] == n][0]
    print(show(p, loop=False)); print(show(p)); print(p["grade"], p["nclues"])
