"""Generate a single cryptogram puzzle from a plaintext quote."""
from __future__ import annotations
import random
from collections import Counter
from cipher import make_key, word_tokens
from solver import count_solutions, letters_match, mapping_from_plain


def letter_freq_order(cipher: str) -> list:
    cnt = Counter(ch for ch in cipher.upper() if ch.isalpha())
    return [ch for ch, _ in sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))]


def pick_givens(cipher: str, key_inv: dict, n: int) -> dict:
    order = letter_freq_order(cipher)
    givens = {}
    for ch in order:
        if len(givens) >= n:
            break
        givens[ch] = key_inv[ch]
    return givens


def discriminating_givens(cipher, intended, key_inv, base_dictionary, qwords,
                          target_min_givens=0, max_givens=8, node_limit=20_000):
    """Add starter letters until the independent solver proves uniqueness.

    Prefers letters that distinguish the intended plaintext from an alternate
    solution when the puzzle is still ambiguous.
    """
    givens = pick_givens(cipher, key_inv, target_min_givens) if target_min_givens else {}
    intended_map = {c: key_inv[c] for c in set(ch for ch in cipher.upper() if ch.isalpha())}

    for _ in range(max_givens + 1):
        nsol, sols, status = count_solutions(
            cipher, dictionary=base_dictionary, givens=givens, limit=3,
            extra_words=qwords, node_limit=node_limit,
        )
        if status == "unique" and nsol == 1 and letters_match(sols[0], intended):
            return givens, "unique"
        if status == "unsolved":
            return None, "unsolved"
        if status in ("ambiguous", "budget") and sols:
            # Prefer a given that separates intended from an alternate
            alts = [s for s in sols if not letters_match(s, intended)]
            if not alts and status == "unique":
                return givens, "unique"
            placed = False
            if alts:
                alt_map = mapping_from_plain(cipher, alts[0])
                # Letters where intended differs from alternate, most frequent first
                order = letter_freq_order(cipher)
                for c in order:
                    if c in givens:
                        continue
                    if intended_map.get(c) != alt_map.get(c):
                        givens[c] = intended_map[c]
                        placed = True
                        break
            if not placed:
                # Fall back: add next most frequent unset letter
                for c in letter_freq_order(cipher):
                    if c not in givens:
                        givens[c] = intended_map[c]
                        placed = True
                        break
            if not placed:
                return None, "stuck"
            continue
        if status == "budget" and not sols:
            # Add a frequent letter and retry
            for c in letter_freq_order(cipher):
                if c not in givens:
                    givens[c] = intended_map[c]
                    break
            else:
                return None, "budget"
            continue
        # unique but wrong plaintext — broken
        if status == "unique":
            return None, "wrong"
    return None, "max_givens"


def make_puzzle(text, author, source, band, seed, base_dictionary, node_limit=20_000):
    """Build one puzzle for a difficulty band. Band sets minimum starter letters."""
    target = {"Easy": 3, "Medium": 2, "Hard": 1, "Expert": 0, "Example": 3}[band]
    qwords = word_tokens(text)
    key = make_key(random.Random(seed))
    key_inv = {v: k for k, v in key.items()}
    cipher = "".join((key[ch.upper()] if ch.isalpha() else ch) for ch in text)
    givens, status = discriminating_givens(
        cipher, text, key_inv, base_dictionary, qwords,
        target_min_givens=target, max_givens=8, node_limit=node_limit,
    )
    if status != "unique" or givens is None:
        return None
    return {
        "plaintext": text,
        "cipher": cipher,
        "author": author,
        "source": source,
        "band": band,
        "seed": seed,
        "key": key,
        "givens": givens,
        "n_givens": len(givens),
        "target_givens": target,
        "n_letters": sum(1 for ch in text if ch.isalpha()),
        "n_distinct": len({ch.upper() for ch in text if ch.isalpha()}),
    }


# Back-compat alias
def minimal_unique_puzzle(text, author, source, seed, base_dictionary, node_limit=20_000,
                          max_givens=5, max_attempts=3):
    for attempt in range(max_attempts):
        for band, target in [("Expert", 0), ("Hard", 1), ("Medium", 2), ("Easy", 3)]:
            p = make_puzzle(text, author, source, band, seed + attempt * 9973, base_dictionary, node_limit)
            if p:
                return p
    return None


def assign_band(n_givens: int) -> str:
    if n_givens >= 3:
        return "Easy"
    if n_givens == 2:
        return "Medium"
    if n_givens == 1:
        return "Hard"
    return "Expert"
