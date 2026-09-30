import sys; sys.path.insert(0,".")
import master, engine
from clues import CASES
G = master.build(); X = engine.Ctx(G)
for case in CASES:
    cl = case["clues"]; M=[i for i,c in enumerate(cl) if c["k"]=="M"]
    full=[p for p in G if all(engine.passes(cl[i],p,X) for i in M)]
    nm={i:sum(1 for p in G if [j for j in M if not engine.passes(cl[j],p,X)]==[i]) for i in M}
    rates={i: round(sum(engine.passes(cl[i],p,X) for p in G)/len(G),2) for i in M}
    print(case["num"], "full-M in master:", len(full), [p["name"] for p in full][:6], "nearmiss:", nm, "rates", rates)
