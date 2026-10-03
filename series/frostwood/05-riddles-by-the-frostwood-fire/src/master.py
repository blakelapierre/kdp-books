"""Rebuild Riddles by the Frostwood Fire end-to-end.
Run from src/:
  PYTHONHASHSEED=0 python3 master.py
"""
import os, subprocess, sys, json
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

# build-info
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
data = json.load(open(os.path.join(root, "data.json")))
epub = os.path.join(root, "frostwood-05-riddles-by-the-frostwood-fire.epub")
cover = os.path.join(root, "frostwood-05-riddles-by-the-frostwood-fire-cover.jpg")
size = os.path.getsize(epub)
kb = (size + 1023) // 1024
mb = kb / 1024
fee = round(mb * 0.15, 2)
price = 3.99
royalty = round(0.70 * price - fee, 2)
info = {
    "title": data["title"],
    "slug": "05-riddles-by-the-frostwood-fire",
    "format": "Kindle ebook (EPUB 3)",
    "author": "Blake La Pierre",
    "series": "A Frostwood Puzzle Book",
    "series_number": 5,
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
        "epub": "frostwood-05-riddles-by-the-frostwood-fire.epub",
        "cover": "frostwood-05-riddles-by-the-frostwood-fire-cover.jpg",
    },
    "rebuild": "cd src && PYTHONHASHSEED=0 python3 master.py",
}
json.dump(info, open(os.path.join(root, "build-info.json"), "w"), indent=2)
print(json.dumps(info, indent=2))
