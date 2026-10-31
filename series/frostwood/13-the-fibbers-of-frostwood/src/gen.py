"""Generate the 120 truth-teller / fibber puzzles for The Fibbers of Frostwood -> ../data.json
Run from src/: PYTHONHASHSEED=0 python3 gen.py
"""
import json, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fibgen import all_solutions, min_depth, propagate, render, kind

SEED = 20261031
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

SIMPLE = ["is", "same", "diff", "both", "either"]
ALL = ["is", "same", "diff", "both", "either", "count", "if"]
TOUGH = ["either", "count", "if", "same", "diff", "both"]
# band: (count, players, statement types, step-depth, hypothesis range)
BANDS = {
    "Easy":   (30, 3, SIMPLE, 0, (0, 0)),
    "Medium": (35, 4, ALL, 1, (1, 1)),
    "Hard":   (35, 5, ALL, 1, (2, 3)),
    "Expert": (20, 6, TOUGH, 2, (1, 4)),
}
PLACE = {"Easy": "The Lodge", "Medium": "The Village", "Hard": "The Railway", "Expert": "The Mountain"}
NAMES = ["Ada", "Bram", "Clara", "Dov", "Elsie", "Finn", "Greta", "Hugo", "Ivy", "Jonah", "Kit", "Lena",
         "Milo", "Nell", "Otto", "Pippa", "Quinn", "Rosa", "Sam", "Tessa", "Uma", "Viggo", "Wren", "Yara", "Zeke"]

SPOTS = {
"Easy": ["by the great hearth", "in the boot room", "at the library writing desk", "on the window seat in the sitting room",
 "around the card table", "on the stair landing", "in the game room", "beside the cocoa cart", "in the reading nook",
 "in the map room", "on the front porch", "in the music room", "up in the attic", "at the front desk", "in the sunroom",
 "in the drying room", "in the tea alcove", "by the corner bookcase", "on the bell tower stairs", "in the kitchen",
 "by the mitten basket", "at the snowshoe rack", "in the upstairs hallway", "in the conservatory", "under the observatory hatch",
 "in the long dining room", "beside the woodbox", "in the linen room", "by the grandfather clock", "in the puzzle parlour"],
"Medium": ["at the bakery counter", "in the post office", "under the bandstand on the green", "in the bookshop window",
 "at the toy-mender's shelf", "in the skating-pond hut", "at the foot of the clock tower", "in the cheese shop",
 "in the wool shop", "in the schoolhouse cloakroom", "at the library returns desk", "by the market-cross well",
 "beside the blacksmith's forge", "in the candle shop", "in the mill wheel house", "in the tea room",
 "on the village hall stage", "in the apothecary", "in the sled-hire shed", "in the haberdashery",
 "by the chapel lane noticeboard", "on the old stone bridge", "among the greengrocer's crates", "at the cobbler's bench",
 "in the fire-watch hut", "in the lantern shop", "by the inn's cellar door", "in the barber's chair", "in the bee shed",
 "in the pottery", "in the hat shop", "up in the map maker's loft", "in the village museum", "in the plant nursery",
 "at the sweet shop"],
"Hard": ["in the valley station ticket office", "around the waiting room stove", "up in the signal box",
 "by the water tower", "in the parcels office", "in the dining car", "in the sleeper car", "in the guard's van",
 "in the engine shed", "beside the turntable", "under the luggage racks", "by the coal bunker", "in the lamp room",
 "at the halfway halt", "on the pine-cutting platform", "in the trestle watch hut", "in the tunnel mouth shelter",
 "in the snowplough shed", "in the brake van", "under the timetable board", "in the stationmaster's office",
 "in the observation car", "at the mail car sorting bench", "beside the tea urn trolley", "at the crossing keeper's cottage",
 "in the lost property office", "under the platform clock", "on the footbridge", "beneath the upper station canopy",
 "beside the token cabinet", "by the goods yard crane", "in the carriage works", "on the ice-cutting siding",
 "at the switchback halt", "on the summit station porch"],
"Expert": ["in the summit hut", "in the ridge shelter", "at the weather station", "in the ski-patrol cabin",
 "at the old sawmill", "below the frozen waterfall", "up the fire lookout tower", "in the snow-hare hide",
 "in the high pasture barn", "at the ice cave mouth", "by the cairn on Lantern Peak", "under the mountain chapel bell",
 "in the shepherd's bothy", "at the glacier viewpoint", "on the star-watch platform", "in the pine-cone gully",
 "at the pass toll hut", "in the hot-spring bathhouse", "in the trail-map cabin", "on the highest bench in Frostwood"],
}

def rand_stmt(rng, s, n, types):
    t = rng.choice(types)
    others = [i for i in range(n) if i != s]
    v = rng.random() < 0.5
    if t == "is":
        return ("is", rng.choice(others), v)
    if t in ("same", "diff"):
        x, y = rng.sample(range(n), 2)
        return (t, x, y)
    if t in ("both", "either"):
        x, y = rng.sample(range(n), 2)
        return (t, x, y, v)
    if t == "count":
        op = rng.choice(["eq", "eq", "ge", "le"])
        return ("count", op, rng.randint(1, n - 1), v)
    if t == "if":
        x, y = rng.sample(range(n), 2)
        return ("if", x, rng.random() < 0.5, y, rng.random() < 0.5)

def every_needed(n, stmts):
    return all(len(all_solutions(n, stmts[:i] + stmts[i + 1:])) > 1 for i in range(n))

def canon(stmts):
    return tuple(stmts)

def hint_text(n, stmts, names, depth, log):
    if depth == 0:
        tr = []
        propagate(n, stmts, [None] * n, tr)
        s, v, val = tr[0]
        if v == s:
            return f"Start with {names[s]}. That statement alone shows that {names[s]} must be {kind(val)}."
        return f"Start with {names[s]}. Whichever kind {names[s]} is, that statement alone shows that {names[v]} is {kind(val)}."
    v, val = log[0]
    return f"Suppose {names[v]} is {kind(val)} and follow where it leads. Something breaks, so {names[v]} must be {kind(not val)}."

def main():
    rng = random.Random(SEED)
    nrng = random.Random(SEED + 1)
    puzzles = []; num = 0; seen = set()
    stats = {}
    for band, (count, n, types, depth, (hlo, hhi)) in BANDS.items():
        made = tries = 0
        while made < count:
            tries += 1
            stmts = [(s, rand_stmt(rng, s, n, types)) for s in range(n)]
            if len({st[0] for _, st in stmts}) < min(3, n):
                continue  # variety: at least three kinds of statement
            sols = all_solutions(n, stmts)
            if len(sols) != 1:
                continue
            d, log = min_depth(n, stmts)
            if d != depth or not (hlo <= len(log) <= hhi):
                continue
            if not every_needed(n, stmts):
                continue
            nfib = sum(1 for x in sols[0] if not x)
            if nfib == 0 and band != "Easy":
                continue  # keep at least one fibber outside Easy
            if canon(stmts) in seen:
                continue
            seen.add(canon(stmts))
            names = sorted(nrng.sample(NAMES, n))
            num += 1; made += 1
            puzzles.append({
                "num": num, "band": band, "players": n, "place": PLACE[band], "spot": SPOTS[band][made - 1],
                "names": names,
                "statements": [{"speaker": names[s], "text": render(s, st, names, n), "form": list(st)} for s, st in stmts],
                "answer": {names[i]: ("truth-teller" if sols[0][i] else "fibber") for i in range(n)},
                "step_depth": d, "hypotheses": len(log),
                "hint": hint_text(n, stmts, names, d, log),
            })
        stats[band] = tries
        print(band, "made", made, "tries", tries, file=sys.stderr)
    data = {
        "title": "The Fibbers of Frostwood",
        "subtitle": "120 Truth-Teller and Fibber Logic Puzzles for Kindle: Cozy Winter Knights and Knaves Brain Teasers, Easy to Expert, with Tap-to-Jump Hints and Answers",
        "seed": SEED,
        "bands": {b: {"count": v[0], "players": v[1], "statement_types": v[2], "step_depth": v[3], "hypotheses": list(v[4])} for b, v in BANDS.items()},
        "counts": {b: v[0] for b, v in BANDS.items()}, "total": len(puzzles), "generator_tries": stats, "puzzles": puzzles,
    }
    json.dump(data, open(os.path.join(ROOT, "data.json"), "w"), indent=1)
    print("wrote", len(puzzles), "puzzles")

if __name__ == "__main__":
    main()
