"""Master raw narration -> chapter MP3s, full-length MP3 with ID3 chapters, and a sample.

Chain per chapter: high-pass 80 Hz -> resample 44.1 kHz (soxr) -> gain to -20 dBFS RMS ->
true-peak-safe limiter -> faint room tone bed + head/tail room tone -> MP3 CBR mono.
"""
import json, os, re, subprocess, sys
import numpy as np, soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, ".."))
WORK = os.environ.get("AUDIO_WORK", "/tmp/tts/work")
COVER = os.path.join(OUT, "..", "standalone-03-tea-and-clues-at-tidewhistle-cove-cover.jpg")
SR = 44100
TARGET_RMS = -20.0
HEAD, TAIL = 0.75, 2.5
PREFIX = "standalone-03-tidewhistle"
BOOK = "standalone-03-tea-and-clues-at-tidewhistle-cove"
FULL_KBPS = os.environ.get("FULL_KBPS", "96k")
TAGS = dict(artist="Blake La Pierre", album_artist="Blake La Pierre", album="Tea and Clues at Tidewhistle Cove",
            genre="Audiobook", date="2026", copyright="© 2026 Blake La Pierre",
            comment="Narrated by a digital voice (Kokoro-82M, af_heart)")

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-2000:])
    return r

def rms_db(x):
    return 20 * np.log10(np.sqrt(np.mean(np.square(x, dtype=np.float64))) + 1e-12)

def ffilter(src, dst, af, ar=None):
    run(["ffmpeg", "-y", "-v", "error", "-i", src, "-af", af] + (["-ar", str(ar)] if ar else []) +
        ["-c:a", "pcm_f32le", dst])

def room_tone(n, rng):
    # very quiet, softly low-passed noise (~-72 dBFS RMS), so gaps are never pure digital silence
    w = rng.standard_normal(n + 64).astype(np.float32)
    w = np.convolve(w, np.ones(8) / 8, mode="same")[:n]
    return w * (10 ** (-72 / 20) / (np.sqrt(np.mean(w ** 2)) + 1e-12))

def master_chapter(raw, dst_wav, rng):
    tmp = dst_wav + ".hp.wav"
    ffilter(raw, tmp, "highpass=f=80:poles=2,aresample=44100:resampler=soxr:precision=28")
    x, _ = sf.read(tmp, dtype="float32")
    for _ in range(3):  # gain -> limit -> re-measure (limiting shaves a little RMS)
        y = x * 10 ** ((TARGET_RMS - rms_db(x)) / 20)
        sf.write(tmp, y, SR, subtype="FLOAT")
        ffilter(tmp, tmp + ".lim.wav", "alimiter=limit=0.56:attack=3:release=60:level=disabled:asc=1")
        z, _ = sf.read(tmp + ".lim.wav", dtype="float32")
        if abs(rms_db(z) - TARGET_RMS) < 0.15:
            break
        x = x * 10 ** ((TARGET_RMS - rms_db(z)) / 20)
    z = np.concatenate([np.zeros(int(HEAD * SR), np.float32), z, np.zeros(int(TAIL * SR), np.float32)])
    z = z + room_tone(len(z), rng)
    sf.write(dst_wav, z, SR, subtype="FLOAT")
    for f in (tmp, tmp + ".lim.wav"):
        os.remove(f)
    return len(z) / SR

def encode(src, dst, kbps, title, track=None, chapters_meta=None, cover=True):
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", src]
    if chapters_meta:
        cmd += ["-i", chapters_meta]
    if cover and os.path.exists(COVER):
        cmd += ["-i", COVER]
    cmd += ["-map", "0:a"]
    if chapters_meta:
        cmd += ["-map_chapters", "1"]
    if cover and os.path.exists(COVER):
        cmd += ["-map", f"{2 if chapters_meta else 1}:v", "-c:v", "mjpeg", "-disposition:v", "attached_pic",
                "-metadata:s:v", "title=Cover", "-metadata:s:v", "comment=Cover (front)"]
    cmd += ["-c:a", "libmp3lame", "-b:a", kbps, "-ar", str(SR), "-ac", "1", "-id3v2_version", "3",
            "-metadata", f"title={title}"]
    for k, v in TAGS.items():
        cmd += ["-metadata", f"{k}={v}"]
    if track:
        cmd += ["-metadata", f"track={track}"]
    run(cmd + [dst])

def measure(path):
    r = run(["ffmpeg", "-v", "info", "-nostats", "-i", path, "-af",
             "astats=metadata=0:measure_overall=RMS_level+Peak_level+Noise_floor:measure_perchannel=none,ebur128=peak=true",
             "-f", "null", "-"]).stderr
    g = lambda pat: float(re.findall(pat, r)[-1])
    return dict(rms_db=g(r"RMS level dB: (-?[\d.]+)"), peak_db=g(r"Peak level dB: (-?[\d.]+)"),
                true_peak_dbtp=g(r"Peak:\s+(-?[\d.]+) dBFS"), lufs=g(r"I:\s+(-?[\d.]+) LUFS"))

def esc(s):
    return re.sub(r"([=;#\\\n])", r"\\\1", s)

def main():
    meta = json.load(open(os.path.join(WORK, "chapters.json")))
    os.makedirs(os.path.join(WORK, "master"), exist_ok=True)
    rng = np.random.default_rng(2026)
    report, wavs, t = [], [], 0.0
    ff = [";FFMETADATA1", f"title={TAGS['album']}", f"artist={TAGS['artist']}"]
    for c in meta:
        wav = os.path.join(WORK, "master", c["name"] + ".wav")
        dur = master_chapter(os.path.join(WORK, "raw", c["name"] + ".wav"), wav, rng)
        mp3 = os.path.join(OUT, f"{PREFIX}-{c['name']}.mp3")
        encode(wav, mp3, "192k", c["title"], track=f"{c['n']+1}/{len(meta)}")
        m = measure(mp3)
        report.append(dict(file=os.path.basename(mp3), seconds=round(dur, 2), bytes=os.path.getsize(mp3), **m))
        print(report[-1], flush=True)
        ff += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={int(t*1000)}", f"END={int((t+dur)*1000)}", f"title={esc(c['title'])}"]
        wavs.append(wav); t += dur
    # full-length file
    lst = os.path.join(WORK, "concat.txt")
    open(lst, "w").write("".join(f"file '{w}'\n" for w in wavs))
    full_wav = os.path.join(WORK, "full.wav")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", full_wav])
    open(os.path.join(WORK, "chapters.ffmeta"), "w").write("\n".join(ff) + "\n")
    full = os.path.join(OUT, f"{BOOK}-full-audiobook.mp3")
    encode(full_wav, full, FULL_KBPS, TAGS["album"] + " (Full Audiobook)", chapters_meta=os.path.join(WORK, "chapters.ffmeta"))
    m = measure(full)
    summary = dict(full=dict(file=os.path.basename(full), seconds=round(t, 2), bytes=os.path.getsize(full), kbps=FULL_KBPS, **m))
    print(summary, flush=True)
    # sample: all of Case One (story, pause and solution), cut from the mastered chapter; no credits
    case1 = next(c for c in meta if c["slug"].startswith("case-01"))
    y, _ = sf.read(os.path.join(WORK, "master", case1["name"] + ".wav"), dtype="float32")
    sw = os.path.join(WORK, "sample.wav"); sf.write(sw, y, SR, subtype="FLOAT")
    sample = os.path.join(OUT, f"{BOOK}-audio-sample.mp3")
    encode(sw, sample, "192k", TAGS["album"] + " (Sample: Case One)")
    m = measure(sample)
    summary["sample"] = dict(file=os.path.basename(sample), seconds=round(len(y) / SR, 2), bytes=os.path.getsize(sample), **m)
    print(summary["sample"], flush=True)
    json.dump(dict(chapters=report, **summary), open(os.path.join(WORK, "levels.json"), "w"), indent=1)

if __name__ == "__main__":
    main()
