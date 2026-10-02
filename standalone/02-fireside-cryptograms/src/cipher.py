"""Monoalphabetic substitution helpers (shared by generator only — solver must not import keys)."""
import random
import string

ALPH = string.ascii_uppercase

def make_key(rng: random.Random) -> dict:
    """Return a random bijective A-Z -> A-Z mapping (no letter maps to itself optional: allow fixed points)."""
    plain = list(ALPH)
    cipher = list(ALPH)
    rng.shuffle(cipher)
    # Prefer derangements for slightly harder puzzles, but allow a few retries then accept
    for _ in range(40):
        rng.shuffle(cipher)
        if all(a != b for a, b in zip(plain, cipher)):
            break
    return dict(zip(plain, cipher))

def invert_key(key: dict) -> dict:
    return {v: k for k, v in key.items()}

def encrypt(text: str, key: dict) -> str:
    out = []
    for ch in text:
        up = ch.upper()
        if up in key:
            enc = key[up]
            out.append(enc if ch.isupper() or not ch.isalpha() else enc.lower())
        else:
            out.append(ch)
    return "".join(out)

def decrypt(text: str, key: dict) -> str:
    return encrypt(text, invert_key(key))

def letters_only(text: str) -> str:
    return "".join(ch.upper() for ch in text if ch.isalpha())

def word_tokens(text: str) -> list:
    """Split into alphabetic words (uppercase), preserving order; punctuation stripped per token."""
    words = []
    cur = []
    for ch in text:
        if ch.isalpha():
            cur.append(ch.upper())
        else:
            if cur:
                words.append("".join(cur))
                cur = []
    if cur:
        words.append("".join(cur))
    return words

def pattern_of(word: str) -> str:
    m = {}
    parts = []
    n = 0
    for ch in word.upper():
        if ch not in m:
            m[ch] = n
            n += 1
        parts.append(str(m[ch]))
    return ".".join(parts)
