"""Hook narration for the video opening, rendered locally with the audiobook's Kokoro voice (af_heart,
speed 0.92, same pronunciation list) and mastered like the audiobook (80 Hz high-pass, -20 dBFS RMS, limiter).

  /tmp/tts/venv/bin/python hook_audio.py "<line>" ../work/hook.wav
Writes a 44.1 kHz mono WAV with LEAD s of silence first, plus <out>.json with the word times (faster-whisper)."""
import json, os, subprocess, sys
import numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "audio", "tools"))
import narrate   # noqa: E402  (VOICE, SPEED, LANG, to_phonemes)
LEAD = 0.2

def main(text, out):
    from kokoro_onnx import Kokoro
    k = Kokoro(os.path.join(narrate.KOKORO_DIR, "kokoro-v1.0.onnx"), os.path.join(narrate.KOKORO_DIR, "voices-v1.0.bin"))
    a, sr = k.create(narrate.to_phonemes(text), voice=narrate.VOICE, speed=narrate.SPEED, lang=narrate.LANG, is_phonemes=True)
    raw = out + ".raw.wav"; sf.write(raw, a, sr, subtype="FLOAT")
    hp = out + ".hp.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-af", "highpass=f=80:poles=2,aresample=44100:resampler=soxr", "-c:a", "pcm_f32le", hp], check=True)
    x, _ = sf.read(hp, dtype="float32")
    rms = 20 * np.log10(np.sqrt(np.mean(x.astype(np.float64) ** 2)) + 1e-12)
    x = x * 10 ** ((-20.0 - rms) / 20)
    sf.write(hp, x, 44100, subtype="FLOAT")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", hp, "-af", "alimiter=limit=0.56:attack=3:release=60:level=disabled:asc=1", "-c:a", "pcm_f32le", raw], check=True)
    z, _ = sf.read(raw, dtype="float32")
    # trim Kokoro's own leading/trailing silence, then add LEAD
    nz = np.where(np.abs(z) > 0.003)[0]; z = z[max(0, nz[0] - 200): nz[-1] + 2000]
    z = np.concatenate([np.zeros(int(LEAD * 44100), np.float32), z])
    sf.write(out, z, 44100, subtype="FLOAT")
    for f in (raw, hp): os.remove(f)
    from faster_whisper import WhisperModel
    m = WhisperModel("small.en", device="cpu", compute_type="int8")
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", out, "-ar", "16000", "-ac", "1", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    segs, _ = m.transcribe(np.frombuffer(pcm, np.float32), word_timestamps=True, initial_prompt=text)
    words = [dict(w=w.word.strip(), s=round(w.start, 3), e=round(w.end, 3)) for sg in segs for w in sg.words]
    json.dump(dict(text=text, duration=round(len(z) / 44100, 3), words=words), open(out + ".json", "w"), indent=1)
    print(len(z) / 44100, words)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
