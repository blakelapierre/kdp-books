"""Generate all 120 puzzles (+ the worked example) for Logic on Lantern Lane -> ../data.json

Each of the 40 scenes is used three times, in three different bands (never twice in one band),
with a different title and opening each time. For every puzzle several candidates are generated
and the best one that fits its page is kept (Easy: the gentlest; harder bands: the one that needs
the most rounds of deduction). Deterministic: run with PYTHONHASHSEED=0 python3 master.py
"""
from __future__ import annotations
import json, os, random, sys, time
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scenarios import SCENES, EXAMPLE
from gen import build_frame, make, first_step_hint, BAND_SPEC, COMPLEX
from text import Phraser, WORDS
from layout import clue_lines, BAND_LAYOUT, free_space

BANDS = ["Easy", "Medium", "Hard", "Expert"]
PER_BAND = 30
CANDIDATES = {"Easy": 4, "Medium": 6, "Hard": 6, "Expert": 6}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data.json")


def plan():
    """(band, scene index, use index) for all 120 puzzles, in book order."""
    rng = random.Random(4040)
    per_band = {b: [] for b in BANDS}
    for i, sc in enumerate(SCENES):
        skip = BANDS[i % 4]
        use = 0
        for b in BANDS:
            if b == skip:
                continue
            per_band[b].append((b, i, use))
            use += 1
    out = []
    for b in BANDS:
        L = per_band[b]
        rng.shuffle(L)
        out += L
    return out


def render(P, sol, clues, rng):
    ph = Phraser(P)
    texts = []
    for c in clues:
        flip = rng.random() < 0.35
        texts.append(ph.clue(c, flip=flip))
    return texts


def one(job):
    num, band, si, use = job
    scene = SCENES[si] if si >= 0 else EXAMPLE
    rng = random.Random(1000 + num * 7919 + (use // 100) * 104729)
    use = use % 100
    best = None
    for cand in range(CANDIDATES[band]):
        P = build_frame(scene, band, rng, use)
        r = make(P, rng)
        if not r:
            continue
        sol, clues, rounds = r
        texts = render(P, sol, clues, rng)
        lines = clue_lines(texts, band)
        n_word = WORDS[P["n"]]
        room = free_space(P["intro"].format(n=n_word, N=n_word.capitalize()), texts, band, P["k"], P["n"])
        if room < (10 if band != "Expert" else 60):
            continue
        ncx = sum(c["t"] in COMPLEX for c in clues)
        if band == "Easy":
            score = (-rounds, len(clues), room)
        else:
            score = (rounds, ncx, room)
        if best is None or score > best[0]:
            best = (score, P, sol, clues, texts, rounds, lines)
    if best is None and use < 99:
        # very rare: nothing fitted the page, so try a fresh batch with another seed
        return one((num, band, si, use + 100))
    assert best, f"no puzzle for {job}"
    _, P, sol, clues, texts, rounds, lines = best
    n = P["n"]
    P["intro"] = P["intro"].format(n=WORDS[n], N=WORDS[n].capitalize())
    for c, t in zip(clues, texts):
        c["text"] = t
    P["clues"] = clues
    P["solution"] = sol
    P["rounds"] = rounds
    P["clue_lines"] = lines
    P["hint"] = first_step_hint(P, clues, sol)
    P["num"] = num
    for c in P["cats"]:
        c.pop("values", None)
    return P


def main():
    t0 = time.time()
    jobs = [(i + 1, b, si, use) for i, (b, si, use) in enumerate(plan())]
    jobs.append((0, "Easy", -1, 0))
    with Pool(min(8, os.cpu_count() or 2)) as pool:
        res = pool.map(one, jobs, chunksize=1)
    D = {b: [] for b in BANDS}
    for P in res:
        if P["num"] == 0:
            P["band"] = "Example"
            D["Example"] = [P]
        else:
            D[P["band"]].append(P)
    for b in BANDS:
        assert len(D[b]) == PER_BAND
        r = [p["rounds"] for p in D[b]]
        cl = [len(p["clues"]) for p in D[b]]
        print(f"{b}: rounds {min(r)}-{max(r)} avg {sum(r)/len(r):.1f}; clues {min(cl)}-{max(cl)} avg {sum(cl)/len(cl):.1f}")
    json.dump(D, open(OUT, "w"), indent=1)
    print(f"wrote {OUT} in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
