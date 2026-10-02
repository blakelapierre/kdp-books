"""Generate all puzzles, grade them, order by difficulty within each band, write ../data.json."""
import json, time
from multiprocessing import Pool
import gen
from gen import make, BANDS
from stars import solve

gen.BANDS["Example"] = dict(n=5, k=1, tier=2, fail=1, count=1)

def grade(p):
    ok, st = solve(p, 4, return_state=True)
    s = st.stats
    return dict(tier=p["tier"], trials=s.get("trial", 0), unit=s.get("unit", 0),
                confine=sum(v for k, v in s.items() if k.startswith("confine")),
                multi=sum(v for k, v in s.items() if k.startswith("confine") and k != "confine1"))

if __name__ == "__main__":
    t0 = time.time(); out = {}
    with Pool(6) as pool:
        for band, base in (("Example", 11), ("Easy", 100), ("Medium", 2000), ("Hard", 30000), ("Expert", 400000)):
            k = 12 if band == "Example" else BANDS[band]["count"] + 16
            res = []; nxt = base
            while len(res) < k:   # keep drawing seeds until there are enough (some seeds fail the band)
                m = k - len(res) + 6
                res += [r for r in pool.map(make, [(band, nxt + i) for i in range(m)], chunksize=1) if r]; nxt += m
            seen = set(); uniq = []
            for r in res:
                key = json.dumps(r["regions"])
                if key in seen: continue
                seen.add(key); uniq.append(r)
            grades = pool.map(grade, uniq)
            for r, g in zip(uniq, grades): r["grade"] = g
            uniq.sort(key=lambda r: (r["grade"]["tier"], r["grade"]["trials"], r["grade"]["multi"], r["grade"]["confine"], r["grade"]["unit"]))
            want = 1 if band == "Example" else BANDS[band]["count"]
            assert len(uniq) >= want, (band, len(uniq))
            if band == "Example":
                uniq = [r for r in uniq if r["grade"]["unit"] + r["grade"]["confine"] >= 1][:1] or uniq[:1]
            else:
                idx = [round(i * (len(uniq) - 1) / (want - 1)) for i in range(want)]
                uniq = [uniq[i] for i in idx]
            out[band] = uniq
            print(band, len(uniq), "tiers", sorted({r["grade"]["tier"] for r in uniq}), round(time.time() - t0, 1), "s", flush=True)
    num = 1
    for band in ("Easy", "Medium", "Hard", "Expert"):
        for r in out[band]: r["num"] = num; num += 1
    json.dump(out, open("../data.json", "w"))
