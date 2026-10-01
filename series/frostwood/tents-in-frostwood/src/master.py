"""Generate all puzzles, grade them, order by difficulty within each band, write ../data.json."""
import json, time, os
os.environ.setdefault("PYTHONHASHSEED", "0")
from multiprocessing import Pool
import gen
from gen import make, BANDS
from tents import solve, need_tier

gen.BANDS["Example"] = dict(n=5, k=(3, 4), tier=1, fail=None, count=1)


def grade(p):
    ok, st = solve(p, 4, return_state=True)
    s = st.stats
    return dict(tier=need_tier(p) or 4,
                trials=s.get("trial", 0),
                unit=s.get("unit", 0),
                tree=s.get("tree", 0),
                confine=s.get("confine", 0))


if __name__ == "__main__":
    t0 = time.time(); out = {}
    with Pool(6) as pool:
        for band, base in (("Example", 7), ("Easy", 1000), ("Medium", 20000),
                           ("Hard", 300000), ("Expert", 4000000)):
            want_pool = 1 if band == "Example" else BANDS[band]["count"] + 24
            res = []; nxt = base
            rounds = 0
            while len(res) < want_pool and rounds < 80:
                m = max(want_pool - len(res) + 10, 12)
                chunk = pool.map(make, [(band, nxt + i) for i in range(m)], chunksize=1)
                res += [r for r in chunk if r]; nxt += m; rounds += 1
                print(f"  {band}: {len(res)}/{want_pool} (seeds through {nxt - 1})", flush=True)
            seen = set(); uniq = []
            for r in res:
                key = (r["n"], tuple(map(tuple, r["trees"])), tuple(r["rows"]), tuple(r["cols"]))
                if key in seen: continue
                seen.add(key); uniq.append(r)
            grades = pool.map(grade, uniq)
            for r, g in zip(uniq, grades): r["grade"] = g
            uniq.sort(key=lambda r: (r["grade"]["tier"], r["grade"]["trials"],
                                     r["grade"]["confine"], -r["grade"]["unit"]))
            want = 1 if band == "Example" else BANDS[band]["count"]
            assert len(uniq) >= want, (band, len(uniq))
            if band == "Example":
                uniq = uniq[:1]
            else:
                idx = [round(i * (len(uniq) - 1) / (want - 1)) for i in range(want)]
                uniq = [uniq[i] for i in idx]
            out[band] = uniq
            print(band, len(uniq), "tiers", sorted({r["grade"]["tier"] for r in uniq}),
                  round(time.time() - t0, 1), "s", flush=True)
    num = 1
    for band in ("Easy", "Medium", "Hard", "Expert"):
        for r in out[band]:
            r["num"] = num; num += 1
    json.dump(out, open("../data.json", "w"))
    print("wrote ../data.json", num - 1, "puzzles", round(time.time() - t0, 1), "s")
