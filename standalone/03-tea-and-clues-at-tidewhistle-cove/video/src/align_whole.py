"""Whole-file word timing (Case 9+): run faster-whisper once on the full chapter MP3 (word timestamps), then map the
narration script words (narrate.py chapters.json segments, +HEAD s master offset) onto the ASR words with difflib.
Unmatched words are interpolated by character count between matched anchors, clamped inside their segment.
  /tmp/tts/venv/bin/python align_whole.py chapters.json chapter.mp3 out.json case-NN-slug"""
import json, sys, re, difflib, subprocess
import numpy as np
from faster_whisper import WhisperModel
HEAD = 0.75
meta = json.load(open(sys.argv[1])); slug = sys.argv[4]
ch = [c for c in meta if c["slug"].startswith(slug)][0]
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", sys.argv[2], "-ar", "16000", "-ac", "1", "-f", "f32le", "-"], capture_output=True, check=True).stdout
a = np.frombuffer(pcm, np.float32)
m = WhisperModel("small.en", device="cpu", compute_type="int8", cpu_threads=6)
script = " ".join(s["text"] for s in ch["segments"])
res, _ = m.transcribe(a, word_timestamps=True, beam_size=5, language="en", condition_on_previous_text=False, vad_filter=False)
hyp = [(w.word.strip(), w.start, w.end) for r in res for w in r.words]
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())
ref = []
for si, sg in enumerate(ch["segments"]):
    for w in sg["text"].split(): ref.append((w, si))
rn = [norm(w) for w, _ in ref]; hn = [norm(h[0]) for h in hyp]
times = [None] * len(ref)
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, rn, hn, autojunk=False).get_opcodes():
    if tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1):
        for k in range(i2 - i1): times[i1 + k] = (hyp[j1 + k][1], hyp[j1 + k][2])
segs = [(s["start"] + HEAD, s["end"] + HEAD) for s in ch["segments"]]
# drop matches outside their segment window (+-0.4 s) or out of order
last = -1
for i, t in enumerate(times):
    if t is None: continue
    s0, s1 = segs[ref[i][1]]
    if not (s0 - 0.4 <= t[0] <= s1 + 0.2) or t[0] < last - 0.02: times[i] = None
    else: last = t[0]
matched = sum(1 for t in times if t)
out = []
i = 0
while i < len(ref):
    if times[i] is not None: i += 1; continue
    j = i
    while j < len(ref) and times[j] is None: j += 1
    si = ref[i][1]
    ta = times[i - 1][1] if i > 0 and ref[i - 1][1] == si else segs[si][0]
    tb = times[j][0] if j < len(ref) and ref[j][1] == si else segs[si][1]
    # a run may cross segments: split per segment
    run = list(range(i, j)); groups = {}
    for k in run: groups.setdefault(ref[k][1], []).append(k)
    for sj, ks in groups.items():
        a0 = times[ks[0] - 1][1] if ks[0] > 0 and times[ks[0] - 1] and ref[ks[0] - 1][1] == sj else segs[sj][0]
        b0 = times[ks[-1] + 1][0] if ks[-1] + 1 < len(ref) and times[ks[-1] + 1] and ref[ks[-1] + 1][1] == sj else segs[sj][1]
        if b0 <= a0: b0 = a0 + 0.06 * len(ks)
        L = sum(len(ref[k][0]) + 1 for k in ks); t = a0
        for k in ks:
            d = (b0 - a0) * (len(ref[k][0]) + 1) / L; times[k] = (t, t + d); t += d
    i = j
for (w, si), (ts, te) in zip(ref, times): out.append(dict(w=w, s=round(ts, 3), e=round(te, 3), seg=si))
json.dump(dict(segments=[dict(text=s["text"], start=s["start"] + HEAD, end=s["end"] + HEAD, pause=s["pause"]) for s in ch["segments"]], words=out), open(sys.argv[3], "w"), indent=0)
print(f"{slug}: {len(ref)} words, asr {len(hyp)}, matched {matched}")
