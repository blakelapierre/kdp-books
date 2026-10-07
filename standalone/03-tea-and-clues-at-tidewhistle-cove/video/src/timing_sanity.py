"""Repair word times in a whole-file alignment where ASR lost a stretch: for any segment whose word times are
non-monotonic or cover < 60% of the segment span, spread that segment's words over it by character count.
python3 timing_sanity.py timing-case-NN.json [--write]"""
import json, sys
p = sys.argv[1]; d = json.load(open(p)); fixed = []
for si, s in enumerate(d["segments"]):
    ws = [w for w in d["words"] if w["seg"] == si]
    if len(ws) < 3: continue
    span = s["end"] - s["start"]; cov = (ws[-1]["e"] - ws[0]["s"]) / max(span, 1e-6)
    mono = all(ws[i]["s"] <= ws[i + 1]["s"] + 1e-6 for i in range(len(ws) - 1))
    if mono and cov >= 0.6: continue
    if cov >= 0.6:   # only a few out-of-order words: interpolate those between their good neighbours
        good = [True] * len(ws); last = -1
        for i, w in enumerate(ws):
            if w["s"] + 1e-6 < last or (i + 1 < len(ws) and w["s"] > ws[min(i + 1, len(ws) - 1)]["s"] + 1.0 and
                                         i + 2 < len(ws) and w["s"] > ws[i + 2]["s"]):
                good[i] = False
            else: last = w["s"]
        i = 0
        while i < len(ws):
            if good[i]: i += 1; continue
            j = i
            while j < len(ws) and not good[j]: j += 1
            a = ws[i - 1]["e"] if i > 0 else s["start"]; b = ws[j]["s"] if j < len(ws) else s["end"]
            for k in range(i, j):
                u0 = (k - i) / (j - i); u1 = (k - i + 0.85) / (j - i)
                ws[k]["s"] = round(a + (b - a) * u0, 3); ws[k]["e"] = round(a + (b - a) * u1, 3)
            i = j
        fixed.append((si, round(cov, 2), "interp")); continue
    tot = sum(len(w["w"]) + 1 for w in ws); t = s["start"]
    for w in ws:
        dur = span * (len(w["w"]) + 1) / tot; w["s"] = round(t, 3); w["e"] = round(t + dur * 0.85, 3); t += dur
    fixed.append((si, round(cov, 2), mono))
print(p, "respread segments:", fixed)
if "--write" in sys.argv: json.dump(d, open(p, "w"), indent=1)
