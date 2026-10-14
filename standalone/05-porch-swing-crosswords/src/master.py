"""Generates the 80 crosswords -> ../data.json.
Run from src/: PYTHONHASHSEED=0 python3 master.py   (deterministic: fixed seeds)"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cross import generate, number, fill_count
import themes_spring, themes_summer, themes_autumn, themes_winter
from themes_extra import EXTRA

HERE = os.path.dirname(os.path.abspath(__file__))
PARTS = [
    # name, level, themes, max width, max height, min words, max words
    ("Spring", "Easy", themes_spring.THEMES, 12, 13, 14, 16),
    ("Summer", "Easy", themes_summer.THEMES, 13, 14, 15, 17),
    ("Autumn", "Medium", themes_autumn.THEMES, 13, 15, 16, 19),
    ("Winter", "Medium", themes_winter.THEMES, 13, 15, 17, 20),
]


def parse(block):
    out = []
    for line in block.strip().splitlines():
        a, c = line.split(":", 1)
        a = a.strip(); c = c.strip()
        assert re.fullmatch(r"[A-Z]{3,13}", a), a
        out.append((a, c))
    return out


def main():
    used = set()
    data = {"parts": []}
    num = 0
    t0 = time.time()
    for pname, level, themes, W, H, lo, hi in PARTS:
        part = {"name": pname, "level": level, "puzzles": []}
        for i, (title, scene, block) in enumerate(themes):
            num += 1
            words = parse(block) + parse(EXTRA.get(title, ""))
            clues = {}
            for a, c in words:
                if a not in used and a not in clues:
                    clues[a] = c
            # near-duplicates in one puzzle: SKI/SKIS or SEED/SEEDS keep the first listed; for a compound
            # such as SNOW/SNOWMAN keep the longer word
            for a in list(clues):
                for b in list(clues):
                    if a in clues and b in clues and a != b and b.startswith(a):
                        del clues[b if len(b) - len(a) <= 2 and list(clues).index(a) < list(clues).index(b) else a]
            best = None
            for need in (lo, lo - 1, lo - 2):
                for seed in range(num * 100, num * 100 + 6):
                    b = generate(list(clues), W, H, need, hi, seed, tries=150)
                    if b and (best is None or b[0] > best[0]):
                        best = b
                if best:
                    break
            if best is None:
                raise SystemExit(f"puzzle {num} {title}: no layout with {lo}+ words from {len(clues)} candidates")
            _, rows, L = best
            ents = number(rows)
            assert fill_count(rows, [e[4] for e in ents]) == 1
            for e in ents:
                used.add(e[4])
            part["puzzles"].append({
                "num": num, "title": title, "scene": scene, "level": level,
                "rows": rows,
                "entries": [{"num": n, "dir": d, "r": r, "c": c, "answer": a, "clue": clues[a]} for n, d, r, c, a in ents],
            })
            print(f"{num:2d} {title:28s} {len(ents):2d} words  {len(rows[0])}x{len(rows)}  cand {len(clues)}  {time.time()-t0:.0f}s", flush=True)
        data["parts"].append(part)
    json.dump(data, open(os.path.join(HERE, "..", "data.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
