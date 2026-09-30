import sys; sys.path.insert(0,".")
import master, engine
from clues import CASES
G = master.build(); X = engine.Ctx(G)
for num in map(int, sys.argv[1:]):
    case=CASES[num-1]; cl=case["clues"]; M=[i for i,c in enumerate(cl) if c["k"]=="M"]
    print("case",num,"full:",[ (p["name"],p["room"]) for p in G if all(engine.passes(cl[i],p,X) for i in M)])
    for k in M:
        w=[p["name"] for p in G if all(engine.passes(cl[i],p,X) for i in M if i<k) and not engine.passes(cl[k],p,X)]
        print(" ",k,cl[k]["t"],len(w))
