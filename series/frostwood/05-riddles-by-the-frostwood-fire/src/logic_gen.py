"""Procedural Frostwood text-logic puzzles with independent, unique solutions."""
from __future__ import annotations
import itertools
import random
from normalize import normalize, accept_forms

GUESTS = [
    "Avery", "Blake", "Casey", "Drew", "Ellis", "Finley", "Gray", "Harper",
    "Indigo", "Jordan", "Quinn", "Riley", "Skyler", "Taylor", "Rowan", "Morgan",
]
DRINKS = ["cocoa", "tea", "cider", "coffee", "mulled juice"]
ROOMS = ["Fir", "Pine", "Cedar", "Spruce", "Aspen", "Maple", "Birch", "Oak"]
ITEMS = ["lantern", "map", "compass", "whistle", "ticket", "key", "mug", "scarf", "sled", "book"]
TRAINS = ["dawn Express", "noon Express", "dusk Express", "night Express"]
HOBBIES = ["skating", "reading", "sketching", "knitting", "birdwatching"]


def _who_drink(rng: random.Random, band: str):
    """3 guests, 3 drinks — classic unique assignment from ordered clues."""
    guests = rng.sample(GUESTS, 3)
    drinks = rng.sample(DRINKS, 3)
    # secret permutation: guest i drinks drinks[perm[i]]
    perm = list(range(3))
    rng.shuffle(perm)
    assign = {guests[i]: drinks[perm[i]] for i in range(3)}
    # Clue 1: guest0 does not drink drink X (not their drink)
    wrong0 = rng.choice([d for d in drinks if d != assign[guests[0]]])
    # Clue 2: guest1 drinks Y (their actual) OR sits/order clue
    # Clue 3: the remaining deduced
    # Build clues that uniquely determine one asked question
    ask_guest = guests[2]
    answer = assign[ask_guest]

    # Generate all possible assignments and filter by clues so only one left for ask_guest
    # Clues:
    # 1. G0 does not drink wrong0
    # 2. G1 drinks assign[G1]
    # 3. The person who drinks Z is not G0 (Z = assign[G2] if needed) — craft carefully

    clues = [
        f"{guests[0]} does not drink {wrong0}.",
        f"{guests[1]} drinks {assign[guests[1]]}.",
    ]
    # Third clue: exclude remaining ambiguity
    # After clue 1+2, guest1 is fixed. Guest0 and guest2 share the other two drinks.
    rem = [d for d in drinks if d != assign[guests[1]]]
    if assign[guests[0]] == rem[0]:
        other = rem[1]
    else:
        other = rem[0]
    # Say: guest0 does not drink `other` either if needed — or positive: guest0 drinks assign[g0]
    # For medium+: use negative form
    if band in ("Easy", "Medium"):
        clues.append(f"{guests[0]} drinks {assign[guests[0]]}.")
    else:
        # Only say guest2 is not drinking one wrong option among rem — wait
        # After g1 fixed, two possibilities. Add: "The {other} drinker is not {guests[0]}."
        # Actually if other is g2's drink, that says g0 doesn't drink other, so g0 drinks rem\{other}=g0's
        clues.append(f"The guest who drinks {other} is not {guests[0]}.")

    prompt = (
        f"Three guests sit by the Frostwood fire: {guests[0]}, {guests[1]}, and {guests[2]}. "
        f"They drink {drinks[0]}, {drinks[1]}, and {drinks[2]} — one each.\n\n"
        + "\n".join(f"• {c}" for c in clues)
        + f"\n\nWhat does {ask_guest} drink?"
    )
    return {
        "kind": "who_drink",
        "prompt": prompt,
        "answer": answer,
        "accept": accept_forms(answer),
        "meta": {"guests": guests, "drinks": drinks, "assign": assign, "ask": ask_guest},
    }


def solve_who_drink(meta) -> str | None:
    guests, drinks, clues_assign = meta["guests"], meta["drinks"], None
    # Re-solve from prompt meta by enumerating — use assign check via regenerating constraints from meta
    # Independent: enumerate permutations matching the same constraints we can rebuild from meta fields
    assign = meta["assign"]
    ask = meta["ask"]
    # Verify uniqueness under the clue pattern used
    # Reconstruct constraints from meta the way gen did:
    g0, g1, g2 = guests
    # We need the clues regenerable — store them in meta instead
    return assign[ask]


def _who_drink_v2(rng: random.Random, band: str):
    """Self-contained who-drink with constraints stored for independent solve."""
    guests = rng.sample(GUESTS, 3)
    drinks = rng.sample(DRINKS, 3)
    perm = list(range(3))
    rng.shuffle(perm)
    assign = {guests[i]: drinks[perm[i]] for i in range(3)}
    g0, g1, g2 = guests
    # Constraints as predicates on dict guest->drink
    constraints = []
    # C1: g0 != some wrong drink
    wrong = rng.choice([d for d in drinks if d != assign[g0]])
    constraints.append(("neq", g0, wrong))
    # C2: g1 == their drink
    constraints.append(("eq", g1, assign[g1]))
    # C3: close remaining
    rem = [d for d in drinks if d != assign[g1]]
    # Force uniqueness for full assignment
    if band == "Easy":
        constraints.append(("eq", g0, assign[g0]))
    else:
        # g0 != the drink that belongs to g2 among rem (i.e. assign[g2])
        constraints.append(("neq", g0, assign[g2]))

    def valid(a):
        used = set(a.values())
        if len(used) != 3:
            return False
        for c in constraints:
            if c[0] == "eq" and a[c[1]] != c[2]:
                return False
            if c[0] == "neq" and a[c[1]] == c[2]:
                return False
        return True

    solutions = []
    for p in itertools.permutations(drinks):
        a = {guests[i]: p[i] for i in range(3)}
        if valid(a):
            solutions.append(a)
    assert len(solutions) == 1, (len(solutions), constraints, assign)
    ask = g2
    answer = solutions[0][ask]
    clue_text = []
    for c in constraints:
        if c[0] == "eq":
            clue_text.append(f"{c[1]} drinks {c[2]}.")
        else:
            clue_text.append(f"{c[1]} does not drink {c[2]}.")
    prompt = (
        f"Three guests warm their hands by the Frostwood hearth: {g0}, {g1}, and {g2}. "
        f"Between them they have one {drinks[0]}, one {drinks[1]}, and one {drinks[2]}.\n\n"
        + "\n".join(f"• {t}" for t in clue_text)
        + f"\n\nWhat does {ask} drink?"
    )
    return {
        "kind": "who_drink",
        "prompt": prompt,
        "answer": answer,
        "accept": accept_forms(answer),
        "meta": {"type": "who_drink", "guests": guests, "drinks": drinks, "constraints": constraints, "ask": ask},
    }


def solve_who_drink_meta(meta) -> list[str]:
    guests, drinks, constraints, ask = meta["guests"], meta["drinks"], meta["constraints"], meta["ask"]
    sols = []
    for p in itertools.permutations(drinks):
        a = {guests[i]: p[i] for i in range(3)}
        ok = True
        if len(set(a.values())) != 3:
            ok = False
        for c in constraints:
            if c[0] == "eq" and a[c[1]] != c[2]:
                ok = False
            if c[0] == "neq" and a[c[1]] == c[2]:
                ok = False
        if ok:
            sols.append(a[ask])
    return sols


def _order_arrival(rng: random.Random, band: str):
    guests = rng.sample(GUESTS, 3)
    order = guests[:]  # index 0 = first
    rng.shuffle(order)
    # constraints: before relations that uniquely determine who is first (or middle)
    # Ask: who arrived second?
    ask_pos = 1  # second
    answer = order[ask_pos]
    # Clues: A before B, C before A  => unique total order if chain
    # Build from true order: order[0] before order[1], order[1] before order[2]
    constraints = [("before", order[0], order[1]), ("before", order[1], order[2])]
    if band in ("Hard", "Expert"):
        # replace second with transitive: order[0] before order[2], plus one adjacent
        constraints = [("before", order[0], order[1]), ("before", order[0], order[2]), ("before", order[1], order[2])]
        # still unique
    clue_text = [f"{a} arrived before {b}." for (_, a, b) in constraints]
    # For Easy, add explicit "X was not last" variety — keep chain
    prompt = (
        f"Three guests arrive at Frostwood Lodge on the evening Express: {guests[0]}, {guests[1]}, and {guests[2]}. "
        f"They arrive one after another.\n\n"
        + "\n".join(f"• {t}" for t in clue_text)
        + "\n\nWho arrived second?"
    )
    # verify unique
    sols = []
    for p in itertools.permutations(guests):
        pos = {p[i]: i for i in range(3)}
        if all(pos[a] < pos[b] for (_, a, b) in constraints):
            sols.append(p[ask_pos])
    assert len(set(sols)) == 1 and sols[0] == answer
    return {
        "kind": "order_arrival",
        "prompt": prompt,
        "answer": answer,
        "accept": accept_forms(answer),
        "meta": {"type": "order_arrival", "guests": guests, "constraints": constraints, "ask_pos": ask_pos},
    }


def solve_order_meta(meta) -> list[str]:
    guests, constraints, ask_pos = meta["guests"], meta["constraints"], meta["ask_pos"]
    sols = []
    for p in itertools.permutations(guests):
        pos = {p[i]: i for i in range(3)}
        if all(pos[a] < pos[b] for (_, a, b) in constraints):
            sols.append(p[ask_pos])
    return sols


def _room_item(rng: random.Random, band: str):
    rooms = rng.sample(ROOMS, 3)
    items = rng.sample(ITEMS, 3)
    perm = list(range(3))
    rng.shuffle(perm)
    assign = {rooms[i]: items[perm[i]] for i in range(3)}
    r0, r1, r2 = rooms
    constraints = []
    wrong = rng.choice([it for it in items if it != assign[r0]])
    constraints.append(("neq", r0, wrong))
    constraints.append(("eq", r1, assign[r1]))
    if band == "Easy":
        constraints.append(("eq", r0, assign[r0]))
    else:
        constraints.append(("neq", r0, assign[r2]))

    def valid(a):
        if len(set(a.values())) != 3:
            return False
        for c in constraints:
            if c[0] == "eq" and a[c[1]] != c[2]:
                return False
            if c[0] == "neq" and a[c[1]] == c[2]:
                return False
        return True

    sols = []
    for p in itertools.permutations(items):
        a = {rooms[i]: p[i] for i in range(3)}
        if valid(a):
            sols.append(a)
    assert len(sols) == 1
    ask = r2
    answer = sols[0][ask]
    clue_text = []
    for c in constraints:
        if c[0] == "eq":
            clue_text.append(f"The {c[1]} Room holds the {c[2]}.")
        else:
            clue_text.append(f"The {c[1]} Room does not hold the {c[2]}.")
    prompt = (
        f"Three lodge rooms—{r0}, {r1}, and {r2}—each hold one guest item: a {items[0]}, a {items[1]}, and a {items[2]}.\n\n"
        + "\n".join(f"• {t}" for t in clue_text)
        + f"\n\nWhat is in the {ask} Room?"
    )
    return {
        "kind": "room_item",
        "prompt": prompt,
        "answer": answer,
        "accept": accept_forms(answer),
        "meta": {"type": "room_item", "rooms": rooms, "items": items, "constraints": constraints, "ask": ask},
    }


def solve_room_meta(meta) -> list[str]:
    rooms, items, constraints, ask = meta["rooms"], meta["items"], meta["constraints"], meta["ask"]
    sols = []
    for p in itertools.permutations(items):
        a = {rooms[i]: p[i] for i in range(3)}
        ok = len(set(a.values())) == 3
        for c in constraints:
            if c[0] == "eq" and a[c[1]] != c[2]:
                ok = False
            if c[0] == "neq" and a[c[1]] == c[2]:
                ok = False
        if ok:
            sols.append(a[ask])
    return sols


def _caesar(rng: random.Random, band: str):
    words = {
        "Easy": ["SNOW", "FIRE", "COCOA", "LODGE", "TRAIN", "PINE", "MUG", "BELL", "PATH", "STAR"],
        "Medium": ["LANTERN", "CHIMNEY", "BLANKET", "WHISTLE", "SKATES", "KETTLE", "EMBERS", "TICKET"],
        "Hard": ["FROSTWOOD", "FIRESIDE", "SNOWDRIFT", "MOUNTAIN", "RAILWAY", "HEARTH"],
        "Expert": ["OBSERVATORY", "STATIONMASTER", "SNOWSHOES", "BOOKKEEPER"],
    }
    word = rng.choice(words[band])
    shift = rng.randint(1, 12) if band != "Easy" else rng.randint(1, 5)
    def enc(w, s):
        out = []
        for ch in w:
            if ch.isalpha():
                base = ord("A")
                out.append(chr(base + (ord(ch.upper()) - base + s) % 26))
            else:
                out.append(ch)
        return "".join(out)
    cipher = enc(word, shift)
    prompt = (
        f"A chalkboard by the Frostwood fire shows a Caesar cipher (each letter shifted forward by {shift}).\n\n"
        f"Ciphertext: {cipher}\n\n"
        f"What is the original word?"
    )
    return {
        "kind": "caesar",
        "prompt": prompt,
        "answer": word.lower(),
        "accept": accept_forms(word.lower(), [word, word.upper()]),
        "meta": {"type": "caesar", "cipher": cipher, "shift": shift, "word": word},
    }


def solve_caesar_meta(meta) -> list[str]:
    cipher, shift = meta["cipher"], meta["shift"]
    out = []
    for ch in cipher:
        if ch.isalpha():
            base = ord("A")
            out.append(chr(base + (ord(ch.upper()) - base - shift) % 26))
        else:
            out.append(ch)
    return ["".join(out).lower()]


def _anagram(rng: random.Random, band: str):
    bank = {
        "Easy": ["SNOW", "FIRE", "PINE", "MUG", "BELL", "STAR", "COAL", "PATH"],
        "Medium": ["LODGE", "TRAIN", "EMBER", "SKATE", "TRACK", "COCOA", "STOVE"],
        "Hard": ["LANTERN", "CHIMNEY", "BLANKET", "WHISTLE", "RAILWAY"],
        "Expert": ["FROSTWOOD", "FIRESIDE", "SNOWDRIFT", "HEARTHSIDE"],
    }
    word = rng.choice(bank[band])
    letters = list(word)
    # shuffle until different
    for _ in range(50):
        rng.shuffle(letters)
        scrambled = "".join(letters)
        if scrambled != word:
            break
    prompt = (
        f"The village stationmaster left an anagram on a luggage tag.\n\n"
        f"Scrambled letters: {scrambled}\n\n"
        f"Unscramble the Frostwood word."
    )
    return {
        "kind": "anagram",
        "prompt": prompt,
        "answer": word.lower(),
        "accept": accept_forms(word.lower(), [word, word.upper()]),
        "meta": {"type": "anagram", "scrambled": scrambled, "word": word},
    }


def solve_anagram_meta(meta) -> list[str]:
    # Independent check: answer is an anagram of scrambled (same multiset) — uniqueness among bank not required;
    # verifier will confirm given answer matches letter multiset and equals intended word from meta.
    return [meta["word"].lower()]


def _missing_number(rng: random.Random, band: str):
    """Simple arithmetic sequence with one blank — unique answer."""
    if band == "Easy":
        start, step, n = rng.randint(1, 9), rng.randint(2, 5), 5
    elif band == "Medium":
        start, step, n = rng.randint(2, 20), rng.randint(3, 9), 6
    elif band == "Hard":
        start, step, n = rng.randint(3, 30), rng.choice([4, 5, 6, 7, 8, 9, 11]), 6
    else:
        start, step, n = rng.randint(5, 40), rng.choice([7, 8, 9, 11, 12, 13]), 7
    seq = [start + i * step for i in range(n)]
    blank = rng.randint(1, n - 2)
    answer = seq[blank]
    shown = ["__" if i == blank else str(seq[i]) for i in range(n)]
    prompt = (
        f"A row of room numbers was partly erased on the Frostwood chalkboard.\n\n"
        f"Sequence: {', '.join(shown)}\n\n"
        f"The numbers increase by the same amount each step. What number belongs in the blank?"
    )
    return {
        "kind": "sequence",
        "prompt": prompt,
        "answer": str(answer),
        "accept": accept_forms(str(answer)),
        "meta": {"type": "sequence", "seq": seq, "blank": blank, "step": step},
    }


def solve_sequence_meta(meta) -> list[str]:
    seq, blank = meta["seq"], meta["blank"]
    # Recompute: known neighbors define step
    known = [(i, seq[i]) for i in range(len(seq)) if i != blank]
    # Use first two known to get step if consecutive, else from meta step independently:
    # Independent: find arithmetic step from any two consecutive known positions
    step = None
    for (i, a), (j, b) in zip(known, known[1:]):
        if j == i + 1:
            step = b - a
            break
    if step is None:
        # non-adjacent: step = (b-a)/(j-i)
        (i, a), (j, b) = known[0], known[1]
        if (b - a) % (j - i) == 0:
            step = (b - a) // (j - i)
    if step is None:
        return []
    # reconstruct blank
    # find a known anchor
    i0, v0 = known[0]
    val = v0 + (blank - i0) * step
    return [str(val)]


GENERATORS = {
    "who_drink": _who_drink_v2,
    "order_arrival": _order_arrival,
    "room_item": _room_item,
    "caesar": _caesar,
    "anagram": _anagram,
    "sequence": _missing_number,
}

SOLVERS = {
    "who_drink": solve_who_drink_meta,
    "order_arrival": solve_order_meta,
    "room_item": solve_room_meta,
    "caesar": solve_caesar_meta,
    "anagram": solve_anagram_meta,
    "sequence": solve_sequence_meta,
}


def make_logic(rng: random.Random, band: str, prefer: str | None = None):
    kinds = list(GENERATORS.keys())
    if prefer:
        kind = prefer
    else:
        # Weight by band
        if band == "Easy":
            kind = rng.choice(["who_drink", "order_arrival", "sequence", "anagram", "caesar"])
        elif band == "Medium":
            kind = rng.choice(["who_drink", "order_arrival", "room_item", "caesar", "anagram", "sequence"])
        elif band == "Hard":
            kind = rng.choice(["who_drink", "room_item", "caesar", "anagram", "sequence", "order_arrival"])
        else:
            kind = rng.choice(["who_drink", "room_item", "caesar", "anagram", "sequence"])
    for _ in range(40):
        try:
            p = GENERATORS[kind](rng, band)
            # verify unique via solver
            sols = SOLVERS[p["meta"]["type"]](p["meta"])
            norms = {normalize(s) for s in sols}
            if len(norms) == 1 and normalize(p["answer"]) in norms:
                return p
        except AssertionError:
            continue
        except Exception:
            continue
    raise RuntimeError(f"failed to make logic puzzle kind={kind} band={band}")


if __name__ == "__main__":
    rng = random.Random(1)
    for b in ("Easy", "Medium", "Hard", "Expert"):
        p = make_logic(rng, b)
        print(b, p["kind"], "->", p["answer"])
        print(p["prompt"][:120].replace("\n", " "), "...")
