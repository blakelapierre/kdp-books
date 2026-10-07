"""Print segment and word times for a case: python3 wt.py N            -> segment table
                                           python3 wt.py N "phrase" ... -> start/end of each phrase"""
import json, re, sys, os
N = int(sys.argv[1]); d = json.load(open(os.path.join(os.path.dirname(__file__), "..", f"timing-case-{N:02d}.json")))
W = d["words"]; norm = lambda s: re.sub(r"[^a-z0-9']", "", s.lower().replace("\u2019", "'"))
if len(sys.argv) == 2:
    for i, s in enumerate(d["segments"]): print(f"[{i}] {s['start']:.2f}-{s['end']:.2f} {s['text'][:90]}")
for ph in sys.argv[2:]:
    p = [norm(x) for x in ph.split()]; ws = [norm(w["w"] if "w" in w else w["word"]) for w in W]; hits = []
    for i in range(len(ws) - len(p) + 1):
        if ws[i:i + len(p)] == p: hits.append((W[i]["s"], W[i + len(p) - 1]["e"]))
    print(f"{ph!r}: " + ", ".join(f"{a:.2f}-{b:.2f}" for a, b in hits))
