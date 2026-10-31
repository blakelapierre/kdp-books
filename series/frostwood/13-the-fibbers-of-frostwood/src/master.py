"""Rebuild The Fibbers of Frostwood end-to-end.
Run from src/:
  PYTHONHASHSEED=0 python3 master.py
"""
import os, subprocess, sys, json, shutil
os.chdir(os.path.dirname(os.path.abspath(__file__)))
env = os.environ.copy()
env["PYTHONHASHSEED"] = "0"

def run(script):
    print("==>", script)
    subprocess.check_call([sys.executable, script], env=env)

run("gen.py")
run("verify.py")
run("illustrations.py")
run("cover.py")
run("epub_build.py")

# optional EPUBCheck: set EPUBCHECK_JAR (and JAVA, if java is not on PATH)
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
java = os.environ.get("JAVA") or shutil.which("java")
jar = os.environ.get("EPUBCHECK_JAR")
epubcheck = "not run (no java / EPUBCHECK_JAR)"
if java and jar and os.path.exists(jar):
    r = subprocess.run([java, "-jar", jar, os.path.join(root, "frostwood-13-the-fibbers-of-frostwood.epub")], capture_output=True, text=True)
    last = [l for l in (r.stdout + r.stderr).splitlines() if l.startswith("Messages:")]
    epubcheck = ("PASS " if r.returncode == 0 else "FAIL ") + (last[0] if last else f"exit {r.returncode}")
    print("EPUBCheck:", epubcheck)
    if r.returncode != 0:
        print(r.stdout, r.stderr); sys.exit(1)

# build-info
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
data = json.load(open(os.path.join(root, "data.json")))
epub = os.path.join(root, "frostwood-13-the-fibbers-of-frostwood.epub")
cover = os.path.join(root, "frostwood-13-the-fibbers-of-frostwood-cover.jpg")
size = os.path.getsize(epub)
kb = (size + 1023) // 1024
mb = kb / 1024
fee = round(mb * 0.15, 2)
price = 3.99
royalty = round(0.70 * price - fee, 2)
info = {
    "title": data["title"],
    "slug": "13-the-fibbers-of-frostwood",
    "format": "Kindle ebook (EPUB 3)",
    "author": "Blake La Pierre",
    "series": "A Frostwood Puzzle Book",
    "series_number": 13,
    "seed": data["seed"],
    "pythonhashseed": 0,
    "total_puzzles": data["total"],
    "counts": data["counts"],
    "price_usd": price,
    "royalty_option": "70%",
    "delivery_fee_usd_per_mb": 0.15,
    "epub_bytes": size,
    "epub_mb_rounded_kb": round(mb, 4),
    "delivery_fee_usd": fee,
    "royalty_usd": royalty,
    "royalty_math": f"0.70 × {price} − {fee} = {royalty}",
    "cover_px": [1600, 2560],
    "cover_bytes": os.path.getsize(cover),
    "files": {
        "epub": "frostwood-13-the-fibbers-of-frostwood.epub",
        "cover": "frostwood-13-the-fibbers-of-frostwood-cover.jpg",
    },
    "epubcheck": epubcheck,
    "rebuild": "cd src && PYTHONHASHSEED=0 python3 master.py  (optional: EPUBCHECK_JAR=/path/epubcheck.jar JAVA=/path/java)",
}
json.dump(info, open(os.path.join(root, "build-info.json"), "w"), indent=2)
print(json.dumps(info, indent=2))
