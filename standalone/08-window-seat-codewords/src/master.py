"""Generates all 120 codewords -> ../data.json (deterministic seeds). Run from src/: python3 master.py"""
import json, os, random, time
import gen
HERE = os.path.dirname(os.path.abspath(__file__))
LEVELS = [("Easy", 40, 3.8, 6), ("Medium", 40, 3.5, 4), ("Hard", 40, 3.3, 2)]
EXTRA_OK = "etaoinsrhldcump"   # letters handed out as extra Easy starters (never J, Q, X or Z)


def main():
    out = {"levels": []}
    allwords = set()
    pid = 0
    for name, count, minz, target in LEVELS:
        gen.set_fill(minz)
        puzzles = []
        seed = {"Easy": 1000, "Medium": 2000, "Hard": 3000}[name]
        while len(puzzles) < count:
            seed += 1
            rng = random.Random(seed)
            g = gen.make_grid(rng, budget=20)
            if not g: continue
            black, letters, slots, words = g
            # keep the book varied: a grid may share at most 4 answers of 5+ letters with earlier grids
            if len({w for w in words if len(w) >= 5} & allwords) > 4: continue
            num, entries = gen.encode(letters, slots, rng)
            key = {n: ch for ch, n in num.items()}
            try:
                giv = gen.choose_givens(num, entries, rng, target, time.time() + 15)
            except TimeoutError:
                continue
            if giv is None: continue
            if len(giv) < target:
                extra = [n for n in key if n not in giv and key[n] in EXTRA_OK]
                rng.shuffle(extra)
                for n in extra[: target - len(giv)]: giv[n] = key[n]
            pid += 1
            allwords |= set(words); gen.BOOKUSED |= set(words)
            grid = []
            for r in range(gen.N):
                grid.append("".join(letters.get((r, c), "#") for c in range(gen.N)))
            numgrid = [[(num[letters[(r, c)]] if (r, c) in letters else 0) for c in range(gen.N)] for r in range(gen.N)]
            puzzles.append(dict(id=pid, level=name, seed=seed, grid=grid, numbers=numgrid,
                                key={str(n): ch.upper() for n, ch in sorted(key.items())},
                                givens={str(n): ch.upper() for n, ch in sorted(giv.items())},
                                words=[w.upper() for w in words]))
            print(name, len(puzzles), "seed", seed, "givens", len(giv), flush=True)
        out["levels"].append(dict(name=name, puzzles=puzzles, min_zipf=minz, starters=target))
    json.dump(out, open(os.path.join(HERE, "..", "data.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
