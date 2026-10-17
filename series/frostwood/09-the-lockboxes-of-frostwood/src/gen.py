"""Generate the 120 lockbox puzzles for The Lockboxes of Frostwood -> ../data.json
Run from src/: PYTHONHASHSEED=0 python3 gen.py
"""
import json, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lockgen import make, feedback
from solver import solve

SEED = 20261017
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# band: (count, digits, min clues, max clues, 'nothing is right' rule, solver-node window)
BANDS = {
    "Easy":   (30, 3, 4, 5, "require", (1, 18)),
    "Medium": (35, 3, 5, 6, "forbid", (19, 40)),
    "Hard":   (35, 4, 5, 7, "any", (41, 90)),
    "Expert": (20, 5, 7, 9, "forbid", (91, 10**9)),
}
PLACE = {"Easy": "The Lodge", "Medium": "The Village", "Hard": "The Railway", "Expert": "The Mountain"}

SPOTS = {
"Easy": ["the boot-room bench", "the pantry's top shelf", "the library writing desk", "the hearth mantel",
 "the cloakroom hooks", "the guest-book stand", "the window seat in the sitting room", "the linen cupboard",
 "the stair landing", "the game-room cabinet", "the kitchen dresser", "the cocoa cart", "the reading nook",
 "the map room", "the porch woodbox", "the music-room bench", "the attic trunk", "the front desk",
 "the sunroom", "the drying room", "the tea alcove", "the corner bookcase", "the bell tower stairs",
 "the scullery", "the mitten basket", "the snowshoe rack", "the upstairs hallway", "the card-table drawer",
 "the conservatory", "the observatory hatch"],
"Medium": ["the bakery counter", "the post office", "the village green bandstand", "the bookshop window",
 "the toy-mender's shelf", "the skating-pond hut", "the clock tower", "the cheese shop", "the wool shop",
 "the schoolhouse cloakroom", "the library returns box", "the market-cross well", "the blacksmith's bench",
 "the candle shop", "the mill wheel house", "the tea room", "the village hall stage", "the apothecary",
 "the sled-hire shed", "the haberdashery", "the chapel lane noticeboard", "the bridge tollbox",
 "the greengrocer's crates", "the cobbler's workbench", "the fire-watch hut", "the lantern shop",
 "the inn's cellar door", "the barber's chair", "the bee shed", "the pottery kiln room", "the hat shop",
 "the map maker's loft", "the village museum", "the plant nursery", "the sweet shop jars"],
"Hard": ["the valley station ticket office", "the waiting room stove", "the signal box", "the water tower ladder",
 "the parcels office", "the dining car pantry", "the sleeper car berth", "the guard's van", "the engine shed",
 "the turntable hut", "the luggage rack", "the coal bunker", "the lamp room", "the halfway halt",
 "the pine-cutting platform", "the trestle watch hut", "the tunnel mouth shelter", "the snowplough shed",
 "the brake van", "the timetable board", "the stationmaster's office", "the observation car",
 "the mail car sorting bench", "the tea urn trolley", "the crossing keeper's cottage", "the lost property cupboard",
 "the platform clock", "the footbridge", "the upper station canopy", "the token cabinet", "the goods yard crane",
 "the carriage works", "the ice-cutting siding", "the switchback halt", "the summit station porch"],
"Expert": ["the summit hut", "the ridge shelter", "the weather station", "the ski-patrol cabin", "the old sawmill",
 "the frozen waterfall ledge", "the fire lookout tower", "the snow-hare hide", "the high pasture barn",
 "the ice cave mouth", "the cairn on Lantern Peak", "the mountain chapel bell", "the shepherd's bothy",
 "the glacier viewpoint", "the star-watch platform", "the pine-cone gully", "the pass toll hut",
 "the hot-spring bathhouse", "the trail-map cabin", "the highest bench in Frostwood"],
}
TREATS = ["a tin of cinnamon cocoa", "a pair of red wool mittens", "a jar of honey drops", "a bundle of beeswax candles",
 "a pocket compass", "a packet of seed cards", "a little brass bell", "a hand-knitted scarf", "a box of oat biscuits",
 "a carved wooden owl", "a pouch of marbles", "a set of postcards of the lodge", "a skate-lace repair kit",
 "a pine-scented soap", "a tiny pewter train", "a jar of plum jam", "a deck of cards", "a sketchbook and pencil",
 "a bag of roasted chestnuts", "a snow globe of the lodge", "a pair of thick socks", "a tea-light lantern",
 "a bookmark of pressed ferns", "a puzzle ring", "a slab of toffee", "a star chart", "a tin whistle",
 "a felt pinecone", "a pocket notebook", "a mug with a fox on it", "a jar of maple butter", "a wooden yo-yo",
 "a spool of ribbon", "a magnifying glass", "a packet of spiced tea", "a wind-up mouse", "a pair of ear warmers",
 "a jar of shortbread", "a pocket kaleidoscope", "a tiny brass key on a ribbon"]

def main():
    rng = random.Random(SEED)
    puzzles = []; n = 0; used_codes = set()
    trng = random.Random(SEED + 1)
    treats = []
    while len(treats) < 120:
        t = TREATS[:]; trng.shuffle(t); treats += t
    for band, (count, L, cmin, cmax, noth, (lo, hi)) in BANDS.items():
        made = 0; rejected = 0
        while made < count:
            secret, clues = make(rng, L, cmin, cmax, noth)
            sols, nodes = solve(L, clues)
            if sols != [secret] or not (lo <= nodes <= hi) or secret in used_codes:
                rejected += 1; continue
            n += 1; made += 1; used_codes.add(secret)
            hint_pos = n % L
            puzzles.append({
                "num": n, "band": band, "digits": L, "place": PLACE[band],
                "spot": SPOTS[band][made - 1], "treat": treats[n - 1],
                "code": secret, "clues": [[g, a, b] for g, a, b in clues],
                "solver_nodes": nodes, "hint_pos": hint_pos, "hint_digit": secret[hint_pos],
            })
        print(band, "made", made, "rejected", rejected, file=sys.stderr)
    data = {
        "title": "The Lockboxes of Frostwood",
        "subtitle": "120 Crack-the-Code Logic Puzzles for Kindle: Cozy Winter Brain Teasers, Easy to Expert, with Tap-to-Jump Hints and Answers",
        "seed": SEED, "bands": {b: {"count": v[0], "digits": v[1], "clues": [v[2], v[3]], "nothing_rule": v[4], "solver_nodes": list(v[5])} for b, v in BANDS.items()},
        "counts": {b: v[0] for b, v in BANDS.items()}, "total": len(puzzles), "puzzles": puzzles,
    }
    json.dump(data, open(os.path.join(ROOT, "data.json"), "w"), indent=1)
    print("wrote", len(puzzles), "puzzles")

if __name__ == "__main__":
    main()
