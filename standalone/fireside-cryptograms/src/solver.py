"""INDEPENDENT cryptogram solver (does not use stored substitution keys)."""
from __future__ import annotations
import os
import re
from collections import defaultdict

ALPH = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
_HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_NODE_LIMIT = 30_000

_EXTRA = """
thou thee thy thine hath doth ye art wilt shalt aye nay ere oft
whence whither wherefore thrifty sharpeneth turneth goeth thinketh
verdure countenance haughty balm pangs gratify astonish belittle
aspirations sisterhood metaphysics underrate banquet unhistoric
amusements misfortunes effectual kindling mantel fireside hearthstone
peppermints thermos crossword armrest windshield duet simmer cinnamon
""".upper().split()


def load_dictionary(extra_words=None, path=None) -> set:
    if path is None:
        for name in ("words5k.txt", "words10k.txt", "words20k.txt"):
            p = os.path.join(_HERE, name)
            if os.path.exists(p):
                path = p
                break
    words = set()
    with open(path, encoding="utf-8") as f:
        for line in f:
            w = line.strip().upper()
            if w.isalpha() and 1 <= len(w) <= 28:
                words.add(w)
    for w in _EXTRA:
        if w.isalpha():
            words.add(w)
    if extra_words:
        for w in extra_words:
            w = str(w).upper()
            if w.isalpha():
                words.add(w)
    words.add("A")
    words.add("I")
    return words


def pattern_of(word: str) -> str:
    m, parts, n = {}, [], 0
    for ch in word:
        if ch not in m:
            m[ch] = n
            n += 1
        parts.append(str(m[ch]))
    return ".".join(parts)


def build_pattern_index(dictionary: set) -> dict:
    idx = defaultdict(list)
    for w in dictionary:
        idx[(len(w), pattern_of(w))].append(w)
    return idx


def tokenize_cipher(cipher: str) -> list:
    return re.findall(r"[A-Za-z]+", cipher.upper())


def letters_match(a: str, b: str) -> bool:
    la = "".join(ch.upper() for ch in a if ch.isalpha())
    lb = "".join(ch.upper() for ch in b if ch.isalpha())
    return la == lb


def _propagate(cwords, pos_cands, domains):
    changed = True
    while changed:
        changed = False
        singletons = {c: next(iter(d)) for c, d in domains.items() if len(d) == 1}
        for c, d in domains.items():
            before = len(d)
            for sc, sp in singletons.items():
                if sc != c:
                    d.discard(sp)
            if not d:
                return False
            if len(d) != before:
                changed = True
        for i, cw in enumerate(cwords):
            cands = []
            for pw in pos_cands[i]:
                if all(p in domains[c] for c, p in zip(cw, pw)):
                    cands.append(pw)
            if not cands:
                return False
            if len(cands) != len(pos_cands[i]):
                pos_cands[i] = cands
                changed = True
            for j, c in enumerate(cw):
                allowed = {pw[j] for pw in cands}
                before = len(domains[c])
                domains[c] &= allowed
                if not domains[c]:
                    return False
                if len(domains[c]) != before:
                    changed = True
    return True


def count_solutions(cipher: str, dictionary=None, givens=None, limit=2,
                    extra_words=None, node_limit=DEFAULT_NODE_LIMIT):
    """Return (n_found, list_of_plaintexts, status)."""
    if dictionary is None:
        dictionary = load_dictionary(extra_words)
    elif extra_words:
        dictionary = set(dictionary) | {w.upper() for w in extra_words if str(w).isalpha()}
    givens = {k.upper(): v.upper() for k, v in (givens or {}).items()}
    cwords = tokenize_cipher(cipher)
    if not cwords:
        return 0, [], "unsolved"

    idx = build_pattern_index(dictionary)
    cipher_letters = sorted({ch for w in cwords for ch in w})
    domains = {c: set(ALPH) for c in cipher_letters}
    for c, p in givens.items():
        if c in domains:
            if p not in domains[c]:
                return 0, [], "unsolved"
            domains[c] = {p}

    pos_cands = []
    for cw in cwords:
        cands = list(idx.get((len(cw), pattern_of(cw)), []))
        if givens:
            cands = [pw for pw in cands if all(givens.get(c, p) == p for c, p in zip(cw, pw))]
        if not cands:
            return 0, [], "unsolved"
        pos_cands.append(cands)

    def clone_state(doms, cands):
        return {c: set(d) for c, d in doms.items()}, [list(x) for x in cands]

    if not _propagate(cwords, pos_cands, domains):
        return 0, [], "unsolved"

    sols = []
    nodes = [0]
    hit_budget = [False]

    def decode(doms):
        mapping = {c: next(iter(d)) for c, d in doms.items()}
        return "".join(mapping[ch.upper()] if ch.isalpha() else ch for ch in cipher)

    def bt(doms, cands):
        nodes[0] += 1
        if nodes[0] > node_limit:
            hit_budget[0] = True
            return
        if len(sols) >= limit or hit_budget[0]:
            return
        if not _propagate(cwords, cands, doms):
            return
        if all(len(d) == 1 for d in doms.values()):
            mapping = {c: next(iter(d)) for c, d in doms.items()}
            if all("".join(mapping[ch] for ch in cw) in dictionary for cw in cwords):
                sols.append(decode(doms))
            return
        c = min((cc for cc, d in doms.items() if len(d) > 1), key=lambda cc: (len(doms[cc]), cc))
        for p in sorted(doms[c]):
            nd, nc = clone_state(doms, cands)
            nd[c] = {p}
            bt(nd, nc)
            if len(sols) >= limit or hit_budget[0]:
                return

    bt(domains, pos_cands)

    if len(sols) >= 2:
        return len(sols), sols, "ambiguous"
    if len(sols) == 1 and not hit_budget[0]:
        return 1, sols, "unique"
    if len(sols) == 1 and hit_budget[0]:
        return 1, sols, "budget"
    if hit_budget[0]:
        return 0, [], "budget"
    return 0, [], "unsolved"


def mapping_from_plain(cipher: str, plain: str) -> dict:
    """Recover cipher->plain mapping from a plaintext/cipher pair (letters only)."""
    m = {}
    for c, p in zip(cipher.upper(), plain.upper()):
        if c.isalpha():
            m[c] = p
    return m
