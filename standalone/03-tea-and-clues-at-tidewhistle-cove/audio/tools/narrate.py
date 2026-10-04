"""Render the audiobook narration (raw, unmastered) with Kokoro-82M (kokoro-onnx), fully local.

Usage: python narrate.py  -> writes work/raw/NN-slug.wav (24 kHz float) + work/chapters.json
Needs: pip install kokoro-onnx soundfile ; model files kokoro-v1.0.onnx + voices-v1.0.bin in $KOKORO_DIR
"""
import hashlib, json, os, re, sys
import numpy as np, soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "src"))
from book import sections, TITLE, AUTHOR, NUM_WORDS  # noqa: E402

KOKORO_DIR = os.environ.get("KOKORO_DIR", "/tmp/tts")
WORK = os.environ.get("AUDIO_WORK", "/tmp/tts/work")
VOICE, LANG, SPEED = "af_heart", "en-us", 0.92
SR = 24000

# Pronunciation list from the book README, as hand-written IPA (espeak en-us style phonemes Kokoro understands).
NAMES = {
    "Penrose": "pˈɛnɹoʊz", "Carew": "kəɹˈuː", "Trevelyan": "tɹəvˈɛljən", "Penhallow": "pɛnhˈæloʊ",
    "Morwenna": "mɔːɹwˈɛnə", "Wenna": "wˈɛnə", "Polglaze": "pɑːlɡlˈeɪz", "Fenwick": "fˈɛnɪk",
    "Truscott": "tɹˈʌskɑːt", "Demelza": "dəmˈɛlzə", "Kerensa": "kəɹˈɛnzə", "Spargo": "spˈɑːɹɡoʊ",
    "Treloar": "tɹəlˈɔːɹ", "Polwhele": "pɑːlwˈiːl", "Opie": "ˈoʊpi", "Pascoe": "pˈæskoʊ",
    "Clemo": "klˈɛmoʊ", "Tobias": "toʊbˈaɪəs", "Vosper": "vˈɑːspɚ", "Nankervis": "nænkˈɜːɹvɪs",
    "Tonkin": "tˈɑːŋkɪn", "Lanyon": "lˈænjən", "Penberthy": "pɛnbˈɜːɹθi", "Keast": "kˈiːst",
    "Bolitho": "bəlˈaɪθoʊ", "Rundle": "ɹˈʌndəl", "Hocking": "hˈɑːkɪŋ", "Agnes": "ˈæɡnəs",
    "Tamsin": "tˈæmzɪn", "Loveday": "lˈʌvdeɪ", "Hedley": "hˈɛdli", "Jago": "dʒˈeɪɡoʊ",
    "Tidewhistle": "tˈaɪdwɪsəl", "Rosie": "ɹˈoʊzi", "Peir": "pˈɪɹ", "peir": "pˈɪɹ", "Pierre": "piˈɛɹ",
}
NAME_RE = re.compile(r"\b(" + "|".join(sorted(NAMES, key=len, reverse=True)) + r")('s)?\b")
VOICELESS_END = tuple("ptkfθ")

_phon = None
def phonemize_plain(text):
    global _phon
    if _phon is None:
        import espeakng_loader
        from phonemizer.backend.espeak.wrapper import EspeakWrapper
        from phonemizer.backend import EspeakBackend
        EspeakWrapper.set_library(espeakng_loader.get_library_path())
        EspeakWrapper.set_data_path(espeakng_loader.get_data_path())
        _phon = EspeakBackend(language=LANG, preserve_punctuation=True, with_stress=True)
    if not text.strip():
        return ""
    return _phon.phonemize([text])[0].strip()

def to_phonemes(text):
    out, pos = [], 0
    for m in NAME_RE.finditer(text):
        out.append(phonemize_plain(text[pos:m.start()]))
        ipa = NAMES[m.group(1)]
        if m.group(2):
            ipa += "ɪz" if ipa.endswith(("s", "z")) else ("s" if ipa.endswith(VOICELESS_END) else "z")
        out.append(ipa)
        pos = m.end()
    out.append(phonemize_plain(text[pos:]))
    ph = " ".join(p for p in out if p)
    ph = re.sub(r"\s+([,.!?;:])", r"\1", ph)
    return " ".join(ph.split())

def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

# --- script -------------------------------------------------------------------
# item = ("say", text, pause_after_seconds)
P_PARA, P_HEAD, P_THINK = 0.85, 1.4, 4.5

def script():
    chapters = []
    chapters.append(("opening-credits", "Opening Credits", [
        ("say", f"{TITLE}.", 0.9),
        ("say", "Thirty cozy mini-mysteries to solve by ear.", 0.9),
        ("say", f"Written by {AUTHOR}.", 0.8),
        ("say", "Narrated by a digital voice.", 0.5)]))
    for sid, head, blocks in sections():
        items = []
        if sid.startswith("case"):
            i = int(sid[4:]) - 1
            title = head.split(": ", 1)[1]
            items.append(("say", f"Case {NUM_WORDS[i]}.", 0.6))
            items.append(("say", f"{title}.", P_HEAD))
            slug = f"case-{i+1:02d}-{slugify(title)}"
        else:
            items.append(("say", f"{head}.", P_HEAD))
            slug = slugify(head)
        for kind, text in blocks:
            if kind == "ask":
                items[-1] = items[-1][:2] + (1.1,)
                items.append(("say", text, 1.2))
            elif kind == "think":
                items.append(("say", "Think about it.", 0.9))
            elif kind == "h2":
                items[-1] = items[-1][:2] + (P_THINK,)   # the thinking silence before the solution
                items.append(("say", f"{text}.", 1.1))
            else:
                items.append(("say", text, P_PARA))
        items[-1] = items[-1][:2] + (0.0,)
        chapters.append((slug, head, items))
    chapters.append(("closing-credits", "Closing Credits", [
        ("say", f"This has been {TITLE},", 0.3),
        ("say", f"written by {AUTHOR}.", 0.9),
        ("say", f"Copyright twenty twenty-six, {AUTHOR}.", 0.9),
        ("say", "The end.", 0.0)]))
    return chapters

def main(only=None):
    from kokoro_onnx import Kokoro
    k = Kokoro(os.path.join(KOKORO_DIR, "kokoro-v1.0.onnx"), os.path.join(KOKORO_DIR, "voices-v1.0.bin"))
    os.makedirs(os.path.join(WORK, "raw"), exist_ok=True)
    os.makedirs(os.path.join(WORK, "cache"), exist_ok=True)
    meta = []
    for n, (slug, head, items) in enumerate(script()):
        name = f"{n:02d}-{slug}"
        parts, segs, t = [], [], 0.0
        for _, text, pause in items:
            ph = to_phonemes(text)
            key = hashlib.sha1(f"{VOICE}|{SPEED}|{ph}".encode()).hexdigest()[:16]
            cp = os.path.join(WORK, "cache", key + ".wav")
            if os.path.exists(cp):
                a, _ = sf.read(cp, dtype="float32")
            else:
                a, sr = k.create(ph, voice=VOICE, speed=SPEED, lang=LANG, is_phonemes=True)
                assert sr == SR
                sf.write(cp, a, SR, subtype="FLOAT")
            segs.append(dict(text=text, start=round(t, 3), end=round(t + len(a) / SR, 3), pause=pause))
            parts += [a, np.zeros(int(pause * SR), np.float32)]
            t += len(a) / SR + pause
        if only is None or name in only:
            sf.write(os.path.join(WORK, "raw", name + ".wav"), np.concatenate(parts), SR, subtype="FLOAT")
        meta.append(dict(n=n, name=name, slug=slug, title=head, seconds=round(t, 2), segments=segs))
        print(f"{name}: {t/60:.1f} min", flush=True)
    json.dump(meta, open(os.path.join(WORK, "chapters.json"), "w"), indent=1)

if __name__ == "__main__":
    main(set(sys.argv[1:]) or None)
