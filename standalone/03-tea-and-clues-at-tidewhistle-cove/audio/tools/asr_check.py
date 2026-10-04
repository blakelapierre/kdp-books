"""Listen-check proxy: transcribe every narrated paragraph with faster-whisper and diff against the script."""
import difflib, hashlib, json, os, re, sys
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import narrate as N
from faster_whisper import WhisperModel

MODEL = os.environ.get("ASR_MODEL", "small.en")
m = WhisperModel(MODEL, device="cpu", compute_type="float32", cpu_threads=6)
NUM = {w.lower(): w for w in N.NUM_WORDS}

def norm(s):
    s = s.lower().replace("mr ", "mister ").replace("mrs ", "missus ").replace("mr. ", "mister ").replace("mrs. ", "missus ")
    s = re.sub(r"[^a-z0-9' ]+", " ", s.replace("-", " "))
    return s.split()

def resample16(a):
    n = int(len(a) * 16000 / 24000)
    return np.interp(np.linspace(0, len(a) - 1, n), np.arange(len(a)), a).astype(np.float32)

only = set(sys.argv[1:])
rows = []
for n, (slug, head, items) in enumerate(N.script()):
    name = f"{n:02d}-{slug}"
    if only and name not in only:
        continue
    for _, text, _ in items:
        ph = N.to_phonemes(text)
        key = hashlib.sha1(f"{N.VOICE}|{N.SPEED}|{ph}".encode()).hexdigest()[:16]
        a, _ = sf.read(os.path.join(N.WORK, "cache", key + ".wav"), dtype="float32")
        a = np.concatenate([np.zeros(8000, np.float32), resample16(a), np.zeros(8000, np.float32)])
        segs, _ = m.transcribe(a, beam_size=5, condition_on_previous_text=False, language="en")
        hyp = " ".join(s.text for s in segs)
        r, h = norm(text), norm(hyp)
        sm = difflib.SequenceMatcher(None, r, h, autojunk=False)
        errs = [(op, " ".join(r[i1:i2]), " ".join(h[j1:j2])) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"]
        wer = sum(max(i2 - i1, j2 - j1) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal") / max(1, len(r))
        rows.append(dict(chapter=name, wer=round(wer, 3), dur=round(len(a) / 16000, 1), words=len(r), text=text, hyp=hyp.strip(), errs=errs))
        print(f"{name} wer={wer:.2f} {errs[:6]}", flush=True)
json.dump(rows, open(os.path.join(N.WORK, "asr.json"), "w"), indent=1)
tot = sum(r["wer"] * r["words"] for r in rows) / sum(r["words"] for r in rows)
print(f"OVERALL word-mismatch rate {tot:.3f} over {sum(r['words'] for r in rows)} words")
