"""Generate all puzzles, grade them, order by difficulty within each band, write ../data.json."""
import json, time
from multiprocessing import Pool
import gen
from gen import make, BANDS
from tracks import solve

gen.BANDS["Example"] = dict(n=5, tier=2, fail=None, fill=(0.5, 0.64), giv=(2, 3), count=1)

def grade(p):
    need = next(t for t in (1, 2, 3, 4) if solve(p, t))
    ok, st = solve(p, 4, return_state=True)
    return dict(tier=need, trials=st.stats.get("trial", 0), parity=st.stats.get("parity", 0), loops=st.stats.get("loop", 0))

if __name__ == "__main__":
    t0 = time.time(); out = {}
    with Pool(8) as pool:
        for band, base in (("Example", 7), ("Easy", 100), ("Medium", 2000), ("Hard", 30000), ("Expert", 400000)):
            k = 1 if band == "Example" else BANDS[band]["count"] + 20
            res = [r for r in pool.map(make, [(band, base + i) for i in range(k)]) if r]
            seen = set(); uniq = []
            for r in res:
                key = (tuple(map(tuple, r["solution"])), tuple(sorted(r["givens"].items())))
                if key in seen: continue
                seen.add(key); uniq.append(r)
            grades = pool.map(grade, uniq)
            for r, g in zip(uniq, grades): r["grade"] = g
            uniq.sort(key=lambda r: (r["grade"]["tier"], -len(r["givens"]), r["grade"]["trials"], len(r["solution"])))
            if band != "Example":
                # keep an even spread of the sorted list
                want = BANDS[band]["count"]
                idx = [round(i * (len(uniq) - 1) / (want - 1)) for i in range(want)]
                uniq = [uniq[i] for i in idx]
            out[band] = uniq
            print(band, len(uniq), "tiers", sorted({r["grade"]["tier"] for r in uniq}), round(time.time() - t0, 1), "s", flush=True)
    num = 1
    for band in ("Easy", "Medium", "Hard", "Expert"):
        for r in out[band]: r["num"] = num; num += 1
    json.dump(out, open("../data.json", "w"))
