"""Generate 200 verified-unique fireside cryptograms -> ../data.json"""
from __future__ import annotations
import json, os, random, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from quotes import normalized_quotes
from cipher import word_tokens
from solver import load_dictionary, count_solutions, letters_match
from gen import make_puzzle, discriminating_givens

BANDS = ["Easy", "Medium", "Hard", "Expert"]
PER_BAND = 50


def main():
    t0 = time.time()
    quotes = normalized_quotes()
    # Use full corpus words from the start so final book dict can't introduce alternates
    corpus_words = set()
    for text, _, _ in quotes:
        corpus_words.update(word_tokens(text))
    base = load_dictionary(extra_words=corpus_words)
    print(f"quotes={len(quotes)} dict={len(base)} corpus_words={len(corpus_words)}", flush=True)

    rng = random.Random(20261001)
    order = list(enumerate(quotes))
    rng.shuffle(order)

    buckets = {0: [], 1: [], 2: [], 3: []}
    for i, (text, author, source) in order:
        p = make_puzzle(text, author, source, "Expert", seed=30_000 + i,
                        base_dictionary=base, node_limit=25_000)
        if not p:
            continue
        b = min(p["n_givens"], 3)
        buckets[b].append(p)
        if sum(len(v) for v in buckets.values()) % 50 == 0:
            print(f"  progress {[len(buckets[k]) for k in (0,1,2,3)]}", flush=True)
        if all(len(buckets[k]) >= PER_BAND + 5 for k in (0, 1, 2, 3)):
            break

    print(f"buckets: 0={len(buckets[0])} 1={len(buckets[1])} 2={len(buckets[2])} 3+={len(buckets[3])}", flush=True)
    for k in (0, 1, 2, 3):
        assert len(buckets[k]) >= PER_BAND, (k, len(buckets[k]))

    def take(key, band, target):
        items = sorted(buckets[key], key=lambda p: (-p["n_letters"], p["plaintext"]))
        out = []
        for p in items[:PER_BAND]:
            q = dict(p)
            q["band"] = band
            q["target_givens"] = target
            out.append(q)
        return out

    selected = {
        "Expert": take(0, "Expert", 0),
        "Hard": take(1, "Hard", 1),
        "Medium": take(2, "Medium", 2),
        "Easy": take(3, "Easy", 3),
    }

    example = dict(selected["Easy"][0])
    example["band"] = "Example"
    example["num"] = 0

    # Final verify (same dict)
    final = {"Example": [], "Easy": [], "Medium": [], "Hard": [], "Expert": []}
    for band in ["Example"] + BANDS:
        src = [example] if band == "Example" else selected[band]
        for p in src:
            nsol, sols, status = count_solutions(
                p["cipher"], dictionary=base, givens=p["givens"], limit=2,
                extra_words=corpus_words, node_limit=50_000,
            )
            if not (status == "unique" and nsol == 1 and letters_match(sols[0], p["plaintext"])):
                # Last-chance escalate
                key_inv = {v: k for k, v in p["key"].items()}
                givens, st = discriminating_givens(
                    p["cipher"], p["plaintext"], key_inv, base, word_tokens(p["plaintext"]),
                    target_min_givens=p["n_givens"], max_givens=10, node_limit=40_000,
                )
                assert st == "unique" and givens is not None, (band, p["plaintext"][:50], status, st)
                p = dict(p)
                p["givens"] = givens
                p["n_givens"] = len(givens)
            final[band].append(p)

    n = 0
    for band in BANDS:
        for p in final[band]:
            n += 1
            p["num"] = n
    final["Example"][0]["num"] = 0

    path = os.path.join(os.path.dirname(__file__), "..", "data.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(final, f, indent=1)
        f.write("\n")
    print(f"Wrote {n} + example in {time.time()-t0:.1f}s -> {path}", flush=True)
    for b in BANDS:
        gs = [p["n_givens"] for p in final[b]]
        print(f"  {b}: n={len(final[b])} givens avg={sum(gs)/len(gs):.2f} "
              f"min={min(gs)} max={max(gs)}", flush=True)


if __name__ == "__main__":
    main()
