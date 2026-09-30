import json, sys, time
sys.path.insert(0, ".")
import master, engine
from clues import CASES
G = master.build()
used = set(); out = []
for case in CASES:
    t = time.time()
    try:
        res = engine.generate(case, G, used, max_seeds=int(sys.argv[1]) if len(sys.argv) > 1 else 3000)
    except RuntimeError as e:
        print("FAIL", case["num"], e); out.append(None); continue
    used.add(res["thief"])
    print(f"case {case['num']:2d} seed {res['seed']:5d} N={len(res['reg'])} clues={len(case['clues'])} thief={res['thief']} "
          f"{[ (s['before'], len(s['out'])) for s in res['steps']]} nec={res['necessity']} {time.time()-t:.1f}s")
    out.append(dict(num=case["num"], seed=res["seed"], thief=res["thief"], reg=res["reg"], steps=res["steps"], necessity=res["necessity"]))
json.dump(out, open("../data.json", "w"), indent=0)
