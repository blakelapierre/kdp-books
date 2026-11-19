"""Generate the 120 line-up puzzles for Side by Side in Frostwood -> ../data.json
Run from src/: PYTHONHASHSEED=0 python3 gen.py
"""
import json, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lineup import Solver, count_solutions, sat_vec, holds, KINDS

SEED = 20261119
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
EASY_KINDS = ["at", "notat", "end", "notend", "even", "adj", "left1", "before"]
NO_AT = [k for k in KINDS if k != "at"]
# band: (count, people, clue kinds, max "at" clues, depth, supposition range, max clues)
BANDS = {
    "Easy":   (30, 4, EASY_KINDS, 1, 0, (0, 0), 6),
    "Medium": (30, 5, KINDS, 1, 0, (0, 0), 7),
    "Hard":   (30, 6, NO_AT, 0, 1, (1, 2), 9),
    "Expert": (30, 7, NO_AT, 0, 1, (3, 6), 10),
}
PLACE = {"Easy": "The Lodge", "Medium": "The Village", "Hard": "The Railway", "Expert": "The Mountain"}
NAMES = ["Ada", "Bram", "Clara", "Dov", "Elsie", "Finn", "Greta", "Hugo", "Ivy", "Jonah", "Kit", "Lena",
         "Milo", "Nell", "Otto", "Pippa", "Quinn", "Rosa", "Sam", "Tessa", "Uma", "Viggo", "Wren", "Yara", "Zeke"]
# (what they do, noun, plural)
SPOTS = {
"Easy": [
 ("have rooms along the upstairs hall", "room", "rooms"),
 ("hang their coats on the pegs in the boot room", "peg", "pegs"),
 ("sit on the long bench by the great hearth", "seat", "seats"),
 ("take chairs down one side of the long dining table", "chair", "chairs"),
 ("have bunks in a row in the attic", "bunk", "bunks"),
 ("hang their scarves on the hooks in the drying room", "hook", "hooks"),
 ("have cubbies in the mitten cupboard", "cubby", "cubbies"),
 ("keep their snowshoes in the snowshoe rack", "slot", "slots"),
 ("sit in the armchairs facing the big window", "armchair", "armchairs"),
 ("take seats at the long table in the puzzle parlour", "seat", "seats"),
 ("hang their lanterns on the porch hooks", "hook", "hooks"),
 ("have cushions on the window seat in the sitting room", "cushion", "cushions"),
 ("have shelves in the library book cupboard", "shelf", "shelves"),
 ("leave their mugs on the hooks above the cocoa cart", "hook", "hooks"),
 ("have easels in a row in the sunroom", "easel", "easels")],
"Medium": [
 ("run stalls along the winter market", "stall", "stalls"),
 ("live in the cottages on Willow Row", "cottage", "cottages"),
 ("rent huts beside the skating pond", "hut", "huts"),
 ("keep shops along the high street", "shop", "shops"),
 ("sit on the benches along the edge of the green", "bench", "benches"),
 ("have sheds on the Mill Lane allotments", "shed", "sheds"),
 ("sit in the front row of the village hall", "seat", "seats"),
 ("have pegs in the schoolhouse cloakroom", "peg", "pegs"),
 ("set up easels in the village hall art room", "easel", "easels"),
 ("have tables along the tea room window", "table", "tables"),
 ("keep beehives along the orchard wall", "hive", "hives"),
 ("put their cakes on the plates at the baking show", "plate", "plates"),
 ("hang lanterns on the posts of the old stone bridge", "post", "posts"),
 ("have boxes in the post office wall", "box", "boxes"),
 ("sit on the stools at the bakery counter", "stool", "stools")],
"Hard": [
 ("have seats in a row in the observation car", "seat", "seats"),
 ("have compartments in the sleeper car", "compartment", "compartments"),
 ("have lockers at the valley station", "locker", "lockers"),
 ("sit on the long bench in the waiting room", "seat", "seats"),
 ("have berths along the night carriage", "berth", "berths"),
 ("hang their bags on the hooks in the guard's van", "hook", "hooks"),
 ("have pigeonholes in the parcels office", "pigeonhole", "pigeonholes"),
 ("have tables in the dining car", "table", "tables"),
 ("sit on the stools at the tea urn counter", "stool", "stools"),
 ("hang lamps on the hooks in the lamp room", "hook", "hooks"),
 ("have workbenches in the carriage works", "workbench", "workbenches"),
 ("sit in the chairs on the summit station porch", "chair", "chairs"),
 ("have windows along the ticket office counter", "window", "windows"),
 ("stand at the numbered marks on the platform", "mark", "marks"),
 ("have shelves in the lost property office", "shelf", "shelves")],
"Expert": [
 ("have huts along the ridge path", "hut", "huts"),
 ("start from the sledge lanes at the top of Long Hill", "lane", "lanes"),
 ("have bunks in the summit hut", "bunk", "bunks"),
 ("keep their skis in the racks at the ski-patrol cabin", "rack", "racks"),
 ("take the cabins of the hot-spring bathhouse", "cabin", "cabins"),
 ("sit on the log bench at the glacier viewpoint", "seat", "seats"),
 ("set up telescopes on the stands of the star-watch platform", "stand", "stands"),
 ("hang their packs on the hooks in the shepherd's bothy", "hook", "hooks"),
 ("have stalls in the high pasture barn", "stall", "stalls"),
 ("sit along the window ledge of the fire lookout", "seat", "seats"),
 ("hang their snowshoes on the pegs at the trail-map cabin", "peg", "pegs"),
 ("have cubbies at the weather station", "cubby", "cubbies"),
 ("have benches in the old sawmill workshop", "bench", "benches"),
 ("take the window seats in the mountain chapel", "seat", "seats"),
 ("have nooks along the ice cave path", "nook", "nooks")],
}
NUMW = {1: "one", 2: "two", 3: "three"}
WORDS = {4: "Four", 5: "Five", 6: "Six", 7: "Seven"}

def text(c, names, noun, plural):
    t = c[0]; A = names[c[1]]
    if t == "at": return f"{A} has {noun} {c[2] + 1}."
    if t == "notat": return f"{A} does not have {noun} {c[2] + 1}."
    if t == "end": return f"{A} is at one end of the row."
    if t == "notend": return f"{A} is not at either end of the row."
    if t == "even": return f"{A} has an {'even' if c[2] else 'odd'}-numbered {noun}."
    B = names[c[2]]
    if t == "adj": return f"{A} is right next to {B}."
    if t == "notadj": return f"{A} is not next to {B}."
    if t == "left1": return f"{A} is directly to the left of {B}."
    if t == "before": return f"{A} is somewhere to the left of {B}."
    if t == "gap":
        g = c[3]
        return f"There {'is' if g == 1 else 'are'} exactly {NUMW[g]} {noun if g == 1 else plural} between {A} and {B}."
    if t == "between": return f"{A} is somewhere between {names[c[2]]} and {names[c[3]]}."
    raise ValueError(c)

def rclue(rng, n, pos, kinds):
    while True:
        t = rng.choice(kinds)
        a, b, c = rng.sample(range(n), 3)
        if t == "at": cl = (t, a, pos[a])
        elif t == "notat": cl = (t, a, rng.choice([k for k in range(n) if k != pos[a]]))
        elif t in ("end", "notend"): cl = (t, a)
        elif t == "even": cl = (t, a, (pos[a] + 1) % 2 == 0)
        elif t in ("adj", "notadj", "left1", "before"): cl = (t, a, b)
        elif t == "gap": cl = (t, a, b, rng.randint(1, min(3, n - 2)))
        else: cl = (t, a, b, c)
        if holds(cl, pos, n): return cl

def key(c):  # symmetric clues are the same clue either way round
    if c[0] in ("adj", "notadj", "gap"): return (c[0], min(c[1], c[2]), max(c[1], c[2])) + tuple(c[3:])
    if c[0] == "between": return (c[0], c[1], min(c[2], c[3]), max(c[2], c[3]))
    return c

def make(rng, n, kinds, max_at):
    pos = list(range(n)); rng.shuffle(pos)
    clues, keys = [], set()
    while True:
        c = rclue(rng, n, pos, kinds)
        if key(c) in keys: continue
        if c[0] == "at" and sum(1 for x in clues if x[0] == "at") >= max_at: continue
        clues.append(c); keys.add(key(c))
        if count_solutions(n, [sat_vec(x, n) for x in clues])[0] == 1: break
    rng.shuffle(clues)
    i = 0
    while i < len(clues):  # drop any clue that is not needed
        t = clues[:i] + clues[i + 1:]
        if count_solutions(n, [sat_vec(x, n) for x in t])[0] == 1: clues = t
        else: i += 1
    return pos, clues

def main():
    rng = random.Random(SEED)
    puzzles, seen, num = [], set(), 0
    spot_i = {b: 0 for b in BANDS}
    for band, (count, n, kinds, max_at, depth, (h0, h1), maxc) in BANDS.items():
        got = 0
        while got < count:
            pos, clues = make(rng, n, kinds, max_at)
            if len(clues) > maxc: continue
            mentioned = set()
            for c in clues:
                mentioned.add(c[1])
                if c[0] in ("adj", "notadj", "left1", "before", "gap", "between"): mentioned.add(c[2])
                if c[0] == "between": mentioned.add(c[3])
            if len(mentioned) < n: continue  # everyone appears in a clue
            s = Solver(n, clues)
            d, log = s.measure(2)
            if d != depth or not (h0 <= len(log) <= h1): continue
            sig = tuple(sorted(key(c) for c in clues))
            if (n, sig) in seen: continue
            seen.add((n, sig))
            names = sorted(rng.sample(NAMES, n))
            if pos == list(range(n)): continue  # cast order must not give the answer away
            what, noun, plural = SPOTS[band][spot_i[band] % len(SPOTS[band])]; spot_i[band] += 1
            num += 1; got += 1
            if depth == 0:
                ci, p, k = s.first_step()
                hint = f"Work toward {names[p]}. With the clue \u201c{text(clues[ci], names, noun, plural)[:-1]}\u201d and what you already know, {names[p]} can only have {noun} {k + 1}."
                hk = ("pin", names[p], k + 1)
            else:
                p, k = log[0]
                hint = f"Try supposing {names[p]} has {noun} {k + 1}. Follow the clues one at a time and you reach a clash, so {names[p]} does not have {noun} {k + 1}."
                hk = ("suppose", names[p], k + 1)
            order = [None] * n
            for i, q in enumerate(pos): order[q] = names[i]
            puzzles.append({
                "num": num, "band": band, "place": PLACE[band], "people": n,
                "setting": what, "noun": noun, "plural": plural, "names": names,
                "clues": [{"text": text(c, names, noun, plural), "form": list(c)} for c in clues],
                "answer": order, "depth": d, "suppositions": len(log),
                "hint": hint, "hint_key": list(hk),
            })
        print(band, got, flush=True)
    counts = {b: sum(1 for p in puzzles if p["band"] == b) for b in BANDS}
    data = {"title": "Side by Side in Frostwood",
            "subtitle": "120 Cozy Line-Up Logic Puzzles for Kindle: Who Sits Where? Winter Seating and Ordering Brain Teasers, Easy to Expert, with Tap-to-Jump Hints and Answers",
            "seed": SEED, "total": len(puzzles), "counts": counts,
            "bands": {b: {"people": v[1], "kinds": v[2], "max_at": v[3], "depth": v[4], "suppositions": list(v[5]), "max_clues": v[6]} for b, v in BANDS.items()},
            "puzzles": puzzles}
    json.dump(data, open(os.path.join(ROOT, "data.json"), "w"), indent=1, ensure_ascii=False)
    print("wrote data.json", counts)

if __name__ == "__main__":
    main()
