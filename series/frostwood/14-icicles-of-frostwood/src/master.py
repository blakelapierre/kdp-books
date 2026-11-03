"""Generate all puzzles, grade them, order by difficulty within each band, write ../data.json.
Deterministic: fixed seed ranges per band (run with PYTHONHASHSEED=0)."""
import json, time, os, sys
os.environ.setdefault("PYTHONHASHSEED", "0")
from multiprocessing import Pool
import gen
from gen import make, BANDS

EXTRA = 16   # candidates beyond the band count, spread evenly by difficulty
gen.BANDS["Example"] = dict(n=4, tier=1, fail=None, trials=(0, 0), count=1)

if __name__ == "__main__":
    t0 = time.time()
    out = json.load(open("../data.json")) if os.path.exists("../data.json") and "--resume" in sys.argv else {}
    # worked example: the first 4x4 seed whose puzzle has 2 numbers and at most 9 signs
    s = 7
    while True:
        e = make(("Example", s))
        if e and len(e["givens"]) <= 2 and len(e["ineq"]) <= 9: break
        s += 1
    out["Example"] = [e]
    with Pool(8) as pool:
        for band, base in (("Easy", 1000), ("Medium", 20000), ("Hard", 300000), ("Expert", 4000000)):
            if band in out: continue
            want_pool = BANDS[band]["count"] + EXTRA
            res = []; nxt = base; rounds = 0
            while len(res) < want_pool and rounds < 400:
                m = 32
                chunk = pool.map(make, [(band, nxt + i) for i in range(m)], chunksize=1)
                res += [r for r in chunk if r]; nxt += m; rounds += 1
                print(f"  {band}: {len(res)} after seeds {base}..{nxt - 1} ({round(time.time() - t0)} s)", flush=True)
            res = res[:want_pool]
            seen = set(); uniq = []
            for r in res:
                key = (r["n"], tuple(map(tuple, r["givens"])), tuple(map(tuple, r["ineq"])))
                if key in seen: continue
                seen.add(key); uniq.append(r)
            uniq.sort(key=lambda r: (r["grade"]["trials"], r["grade"]["t2"], -r["k"], r["grade"]["steps"], r["seed"]))
            want = BANDS[band]["count"]
            assert len(uniq) >= want, (band, len(uniq))
            idx = [round(i * (len(uniq) - 1) / (want - 1)) for i in range(want)]
            out[band] = [uniq[i] for i in idx]
            print(band, len(out[band]), round(time.time() - t0, 1), "s", flush=True)
            json.dump(out, open("../data.json", "w"))
    num = 1
    for band in ("Easy", "Medium", "Hard", "Expert"):
        for r in out[band]:
            r["num"] = num; num += 1
    out["Example"][0]["num"] = 0
    json.dump(out, open("../data.json", "w"))
    print("wrote ../data.json", num - 1, "puzzles", round(time.time() - t0, 1), "s")
