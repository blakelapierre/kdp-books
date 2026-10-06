"""Generates every candidate picture puzzle, chooses the book's 140 and writes ../data.json.
Run from src/: PYTHONHASHSEED=0 python3 master.py   (deterministic; no randomness outside fixed seeds)"""
import json, os, sys, time
os.environ.setdefault("PYTHONHASHSEED", "0")
from multiprocessing import Pool
from subjects import SUBJECTS
from gen import make

EXCLUDE = set("⛪🚁✈🚀🛸🔔👗🌵👒👕👜🐫🦘🦒🦀🐙🐘🌉🖼🌂🎳")
EASY = list("☕❄⛄🌲🏔🕯🏮🥾⛸🏠🛖🌙⭐🔑🍎🍄🦢♟✏⛺🪟🧦👢🍵🧁🎩☂💧🍒🍭🫙🎈🪜🚪💡🎵⌛✉⚓⛵☁☀🍐🥛🗻🧸")
COUNT = {"Easy": 30, "Medium": 40, "Hard": 40, "Expert": 30}

if __name__ == "__main__":
    t0 = time.time()
    idx = {ch: i for i, (ch, _) in enumerate(SUBJECTS)}
    easy = [c for c in EASY if c in idx]
    rest = [c for c, _ in SUBJECTS if c not in EXCLUDE and c not in set(easy)]
    jobs = [(idx[c], c, SUBJECTS[idx[c]][1], 15) for c in easy]
    jobs += [(idx[c], c, SUBJECTS[idx[c]][1], n) for c in rest for n in (20, 25)]
    with Pool(8) as pool:
        res = pool.map(make, jobs, chunksize=1)
    print("generated", sum(r is not None for r in res), "/", len(res), round(time.time() - t0), "s", flush=True)
    json.dump([r for r in res if r], open("../tmp/candidates.json", "w"))
