"""Word-level timing for Case 1: slice the mastered MP3 by the narration script's own segment times
(narrate.py chapters.json, +0.75 s master head) and run faster-whisper on each slice; map script words to
ASR words with difflib; interpolate any unmatched words inside the segment."""
import json, sys, re, difflib
import numpy as np, soundfile as sf
from faster_whisper import WhisperModel
HEAD = 0.75
meta = json.load(open(sys.argv[1]))
ch = [c for c in meta if c["slug"].startswith("case-01")][0]
a, sr = sf.read(sys.argv[2], dtype="float32")
m = WhisperModel("small.en", device="cpu", compute_type="float32", cpu_threads=8)
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())
out = []
for seg in ch["segments"]:
    s0, s1 = seg["start"] + HEAD, seg["end"] + HEAD
    clip = a[int(max(0, s0 - 0.15) * sr): int((s1 + 0.2) * sr)]
    off = max(0, s0 - 0.15)
    res, _ = m.transcribe(clip, word_timestamps=True, beam_size=5, language="en", condition_on_previous_text=False)
    hyp = [(w.word.strip(), w.start + off, w.end + off) for r in res for w in r.words]
    ref = seg["text"].split()
    rn = [norm(w) for w in ref]; hn = [norm(h[0]) for h in hyp]
    times = [None] * len(ref)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, rn, hn, autojunk=False).get_opcodes():
        if tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1):
            for k in range(i2 - i1): times[i1 + k] = (hyp[j1 + k][1], hyp[j1 + k][2])
    # interpolate gaps by character count between anchors
    anchors = [(-1, s0, s0)] + [(i, t[0], t[1]) for i, t in enumerate(times) if t] + [(len(ref), s1, s1)]
    for (ia, _, ea), (ib, sb, _) in zip(anchors, anchors[1:]):
        gap = list(range(ia + 1, ib))
        if not gap: continue
        L = sum(len(ref[k]) + 1 for k in gap); t = ea
        for k in gap:
            d = (sb - ea) * (len(ref[k]) + 1) / L; times[k] = (t, t + d); t += d
    matched = sum(1 for x in times if x) 
    for w, (ts, te) in zip(ref, times): out.append(dict(w=w, s=round(ts, 3), e=round(te, 3), seg=ch["segments"].index(seg)))
    print(f"seg {ch['segments'].index(seg)}: {len(ref)} words, asr {len(hyp)}", flush=True)
json.dump(dict(segments=[dict(s["text"] and dict(text=s["text"], start=s["start"] + HEAD, end=s["end"] + HEAD, pause=s["pause"])) for s in ch["segments"]], words=out), open(sys.argv[3], "w"), indent=0)
