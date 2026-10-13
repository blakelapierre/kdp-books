"""Generate all puzzles, grade them, order by difficulty within each band, write ../data.json.
Deterministic: fixed seed ranges per band (run with PYTHONHASHSEED=0)."""
import json, time, os
os.environ.setdefault("PYTHONHASHSEED", "0")
from multiprocessing import Pool
import gen
from gen import make, BANDS

# the worked example: a small 5x5 Easy-style puzzle
gen.BANDS["Example"] = dict(w=5, h=5, k=(6, 7), win=3, tier=1, fail=None, trials=(0, 0), count=1)
EX_SEED = 63

if __name__ == "__main__":
    t0 = time.time(); out = {}
    ex = make(("Example", EX_SEED)); assert ex, "example seed failed"
    out["Example"] = [ex]
    with Pool(8) as pool:
        for band, base in (("Easy", 1000), ("Medium", 20000), ("Hard", 300000), ("Expert", 4000000)):
            want_pool = BANDS[band]["count"] + 30
            res = []; nxt = base; rounds = 0
            while len(res) < want_pool and rounds < 200:
                m = 64
                chunk = pool.map(make, [(band, nxt + i) for i in range(m)], chunksize=1)
                res += [r for r in chunk if r]; nxt += m; rounds += 1
            res = res[:want_pool]          # deterministic: first want_pool hits in seed order
            print(f"  {band}: {len(res)} candidates (seeds {base}..{nxt - 1})", flush=True)
            seen = set(); uniq = []
            for r in res:
                key = (r["w"], r["h"], tuple(map(tuple, r["islands"])))
                if key in seen: continue
                seen.add(key); uniq.append(r)
            uniq.sort(key=lambda r: (r["grade"]["trials"], r["grade"]["network"], r["k"], r["grade"]["steps"], r["seed"]))
            want = BANDS[band]["count"]
            assert len(uniq) >= want, (band, len(uniq))
            idx = [round(i * (len(uniq) - 1) / (want - 1)) for i in range(want)]
            out[band] = [uniq[i] for i in idx]
            print(band, len(out[band]), round(time.time() - t0, 1), "s", flush=True)
    num = 1
    for band in ("Easy", "Medium", "Hard", "Expert"):
        for r in out[band]:
            r["num"] = num; num += 1
    out["Example"][0]["num"] = 0
    json.dump(out, open("../data.json", "w"))
    print("wrote ../data.json", num - 1, "puzzles", round(time.time() - t0, 1), "s")
