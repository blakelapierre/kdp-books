"""Generate Frostwood book 5 puzzle set: riddles + text logic for Kindle.
Fixed seed. Writes ../data.json
Run from src/: PYTHONHASHSEED=0 python3 gen.py
"""
from __future__ import annotations
import json, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from normalize import normalize, accept_forms
from riddle_bank import all_riddles
from logic_gen import make_logic

SEED = 20261003
# Target counts
COUNTS = {"Easy": 40, "Medium": 40, "Hard": 40, "Expert": 20}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data.json")


def riddle_puzzle(band, prompt, answer, extras, idx):
    return {
        "id": f"{band[0]}{idx:03d}",
        "num": idx,  # filled later globally
        "band": band,
        "kind": "riddle",
        "prompt": prompt.strip(),
        "answer": answer.strip(),
        "accept": accept_forms(answer, extras or []),
        "meta": {"type": "riddle"},
    }


def logic_puzzle(band, p, idx):
    return {
        "id": f"{band[0]}{idx:03d}",
        "num": idx,
        "band": band,
        "kind": p["kind"],
        "prompt": p["prompt"].strip(),
        "answer": str(p["answer"]).strip(),
        "accept": p["accept"],
        "meta": p["meta"],
    }


def build(seed=SEED):
    rng = random.Random(seed)
    banks = all_riddles()
    puzzles = []
    seen_prompts = set()
    seen_answers_per_band = {b: set() for b in COUNTS}

    def add(p):
        key = normalize(p["prompt"])[:160]
        if key in seen_prompts:
            return False
        # Allow repeated answers across different prompts (many riddles share themes)
        # but avoid identical prompt+answer pairs
        pa = (key, normalize(p["answer"]))
        if pa in seen_prompts:
            return False
        seen_prompts.add(key)
        puzzles.append(p)
        return True

    # 1) Place curated riddles first
    for band, items in banks.items():
        need = COUNTS[band]
        # Use all riddles that fit, up to need
        for prompt, answer, extras in items:
            if sum(1 for p in puzzles if p["band"] == band) >= need:
                break
            # Skip very weak expert open-ended
            if band == "Expert" and "non-random" in prompt:
                continue
            rp = riddle_puzzle(band, prompt, answer, extras, 0)
            add(rp)

    # 2) Fill with logic
    for band, need in COUNTS.items():
        attempts = 0
        while sum(1 for p in puzzles if p["band"] == band) < need and attempts < need * 80:
            attempts += 1
            try:
                lp = make_logic(rng, band)
            except RuntimeError:
                continue
            p = logic_puzzle(band, lp, 0)
            add(p)

    # Sort by band order then stable
    order = {"Easy": 0, "Medium": 1, "Hard": 2, "Expert": 3}
    puzzles.sort(key=lambda p: (order[p["band"]], p["kind"], normalize(p["prompt"])))

    # Renumber globally 1..N within whole book, also per-band numbers
    band_count = {b: 0 for b in COUNTS}
    for i, p in enumerate(puzzles, 1):
        p["num"] = i
        band_count[p["band"]] += 1
        p["band_num"] = band_count[p["band"]]
        p["id"] = f"{p['band'][0]}{p['band_num']:03d}"

    # Sanity counts
    counts = {b: sum(1 for p in puzzles if p["band"] == b) for b in COUNTS}
    for b, n in COUNTS.items():
        if counts[b] != n:
            raise SystemExit(f"count mismatch {b}: got {counts[b]} want {n}")

    # Dedup check
    prompts = [normalize(p["prompt"]) for p in puzzles]
    if len(prompts) != len(set(prompts)):
        raise SystemExit("duplicate prompts")

    data = {
        "title": "Riddles by the Frostwood Fire",
        "subtitle": "140 Cozy Winter Riddles and Text Logic Puzzles for Kindle",
        "series": "A Frostwood Puzzle Book",
        "series_number": 5,
        "author": "Blake La Pierre",
        "seed": seed,
        "counts": counts,
        "total": len(puzzles),
        "puzzles": puzzles,
    }
    return data


def main():
    data = build()
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
    print(f"wrote {OUT}: {data['total']} puzzles {data['counts']}")


if __name__ == "__main__":
    main()
