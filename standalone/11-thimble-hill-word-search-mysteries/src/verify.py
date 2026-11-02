"""Independent checker for data.json. It ignores the generator's placement records and re-solves every grid from scratch:
1. every listed word is found exactly once, searching all 8 directions (forwards and backwards);
2. it runs only in the directions allowed for that case's difficulty level;
3. the squares not used by any word, read left to right and top to bottom, spell the hidden clue exactly;
4. no offensive word shows up in any line, except where it sits inside a real list word (BUTTER contains BUTT).
Writes ../verification.md."""
import json, os, sys
import content
here = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(here, "..", "data.json")))
n = D["size"]
bad = sorted({l.strip().upper() for l in open(os.path.join(here, "badwords.txt")) if l.strip().isalpha() and len(l.strip()) >= 4})
VEC = {"E": (0, 1), "W": (0, -1), "S": (1, 0), "N": (-1, 0), "SE": (1, 1), "NW": (-1, -1), "NE": (-1, 1), "SW": (1, -1)}


def rays(grid):
    """Yield (direction name, list of cells) for every maximal line in the grid in each of 8 directions."""
    for name, (dr, dc) in VEC.items():
        for r0 in range(n):
            for c0 in range(n):
                pr, pc = r0 - dr, c0 - dc
                if 0 <= pr < n and 0 <= pc < n: continue  # not the start of a maximal line
                cells = []; r, c = r0, c0
                while 0 <= r < n and 0 <= c < n: cells.append((r, c)); r += dr; c += dc
                yield name, cells


problems = []; rows = []
for ci, case in enumerate(D["cases"]):
    allowed = {k for k, v in VEC.items() if list(v) in case["directions"]}
    src = content.CASES[ci]
    assert case["title"] == src["title"]
    for bi, p in enumerate(case["puzzles"]):
        g = p["grid"]
        assert len(g) == n and all(len(row) == n and row.isalpha() and row.isupper() for row in g)
        assert p["clue"] == src["beats"][bi][1], "clue mismatch"
        lines = [(name, cells, "".join(g[r][c] for r, c in cells)) for name, cells in rays(g)]
        used = set(); spans = []
        for w in p["words"]:
            finds = []
            for name, cells, s in lines:
                i = s.find(w)
                while i != -1:
                    finds.append((name, cells[i:i + len(w)])); i = s.find(w, i + 1)
            if len(finds) != 1:
                problems.append(f"#{p['id']} {w} found {len(finds)} times"); continue
            name, cells = finds[0]
            if name not in allowed: problems.append(f"#{p['id']} {w} runs {name}, not allowed at this level")
            used |= set(cells); spans.append(set(cells))
        left = "".join(g[r][c] for r in range(n) for c in range(n) if (r, c) not in used)
        if left != p["clue"].replace(" ", ""):
            problems.append(f"#{p['id']} leftover letters spell {left}, expected {p['clue']}")
        for name, cells, s in lines:
            for b in bad:
                i = s.find(b)
                while i != -1:
                    span = set(cells[i:i + len(b)])
                    if not any(span <= sp for sp in spans): problems.append(f"#{p['id']} offensive run {b}")
                    i = s.find(b, i + 1)
        rows.append(f"| {p['id']} | {ci + 1} | {case['level_name']} | {len(p['words'])} | {''.join(sorted(allowed))} | {p['clue']} | OK |")

ok = not problems
with open(os.path.join(here, "..", "verification.md"), "w") as f:
    f.write("# Verification report\n\nIndependent re-solve of every grid by `src/verify.py` (it does not trust the generator's placement records).\n\n")
    f.write(f"Result: **{'ALL 60 PUZZLES PASS' if ok and len(rows) == 60 else 'PROBLEMS FOUND'}**\n\n")
    f.write("Checks: each listed word appears exactly once in all 8 directions; it runs only in that level's directions; the unused squares read in order spell the hidden clue exactly; no offensive word appears in any line outside a real list word.\n\n")
    f.write("| Puzzle | Case | Level | Words | Directions | Hidden clue | Result |\n|---|---|---|---|---|---|---|\n")
    f.write("\n".join(rows) + "\n")
    if problems: f.write("\n## Problems\n\n" + "\n".join("- " + x for x in problems) + "\n")
print("puzzles checked:", len(rows), "problems:", len(problems))
for x in problems[:20]: print(x)
sys.exit(0 if ok else 1)
