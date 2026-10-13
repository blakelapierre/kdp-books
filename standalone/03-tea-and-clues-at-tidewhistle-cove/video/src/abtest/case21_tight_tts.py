import sys, os, subprocess, numpy as np, soundfile as sf
sys.path.insert(0, os.getcwd()); import narrate
from kokoro_onnx import Kokoro
k = Kokoro("/tmp/tts/kokoro-v1.0.onnx", "/tmp/tts/voices-v1.0.bin")
for i, text in enumerate(sys.argv[1:]):
    a, sr = k.create(narrate.to_phonemes(text), voice=narrate.VOICE, speed=narrate.SPEED, lang=narrate.LANG, is_phonemes=True)
    nz = np.where(np.abs(a) > 0.003)[0]; a = a[max(0, nz[0]-200): nz[-1]+2000]
    raw = f"/workspace/tw21/l{i}.raw.wav"; sf.write(raw, a, sr, subtype="FLOAT")
    x, _ = sf.read(raw); rms = 20*np.log10(np.sqrt(np.mean(x**2))+1e-12); sf.write(raw, x*10**((-20-rms)/20), sr, subtype="FLOAT")
    subprocess.run(["ffmpeg","-y","-v","error","-i",raw,"-af","highpass=f=80:poles=2,aresample=48000,alimiter=limit=0.56:attack=3:release=60:level=disabled:asc=1","-ac","1",f"/workspace/tw21/l{i}.wav"],check=True)
    print(i, len(a)/sr)
