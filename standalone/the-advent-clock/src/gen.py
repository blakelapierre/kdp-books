"""Generate all 24 doors -> ../data.json. Deterministic (fixed seeds).
Every door has an ANSWER word and a KEY letter (answer[key-1]); the 24 key letters, placed into the
Christmas Eve ledger, spell THE STAR IS IN THE CLOCK TOWER. In door order (the Door Log) they are
deliberately scrambled: see choose_keys()."""
import json, random, sys
import grids, latin, misc, nonogram
import tracks_gen

MESSAGE = "THE STAR IS IN THE CLOCK TOWER"
SPEC = [  # door, type, answer  (the key position in each answer is chosen by choose_keys() below)
 (1, "wordsearch", "TINSEL"), (2, "caesar", "HOLLY"), (3, "queens", "WREATH"), (4, "wordoku", "SLEIGH"),
 (5, "maze", "TOBOGGAN"), (6, "nonogram", "CANDLE"), (7, "pyramid", "FROST"), (8, "pigpen", "ICICLE"),
 (9, "logic", "SKATE"), (10, "tents", "GINGERBREAD"), (11, "tracks", "NOEL"), (12, "akari", "TWINKLE"),
 (13, "fillin", "HEARTH"), (14, "presents", "PRESENTS"), (15, "futoshiki", "BAUBLE"), (16, "morse", "EGGNOG"),
 (17, "fleet", "SNOWFLAKES"), (18, "wordsearch", "LANTERN"), (19, "skyscrapers", "TOFFEE"), (20, "queens", "SNOWBALL"),
 (21, "nonogram", "BELL"), (22, "calcudoku", "MERRY"), (23, "wordoku", "FRUITCAKE"), (24, "tracks", "CHRISTMASEVE"),
]
ANSWERS = {a for _, _, a in SPEC}

# ------------------------------------------------------------------ key letters and the Christmas Eve ledger
# The reader copies the key letters into the Door Log in door order, so that order must NOT give the
# message away. We pick (key position per door, ledger permutation) as a random perfect matching in the
# bipartite graph  doors x message-slots  (edge when the slot's letter occurs in the door's answer), then
# reject anything whose door-order string or ledger looks meaningful. Deterministic: fixed seed, and
# among the first KEY_CANDIDATES acceptable matchings the lowest-scoring one wins.
KEY_SEED, KEY_CANDIDATES = 2412, 200
# common short English words (plus the message words) that must not appear in the door-order key string
BANNED_WORDS = set("""
THE STAR CLOCK TOWER TOW OWE OWER STARS TSAR RATS ARTS ART RAT TAR SAT SIT ITS TIS HIS HIT HAT HAS HER HEN THEN THEM
TEN TIN NIT NIL NET TOE TOT HOT HOE ONE NOT TON TOO COT CAT ACT CAN CAR ARC ARE ERA EAR EAT ATE TEA SEA SEE SET SHE
HEW NEW NOW OWN WON WHO HOW LOW OWL COW ROW ROT ORE ROE ONE EON NOR OAR OAT TAO SON NOS RIS IRE SIR STIR RITE TIRE
TIER CORE ROCK LOCK COCK LOCO COOK LOOK TOOK KILT KIT KIN INK SKI SKIT TICK LICK LIE LIT TIL OIL SOIL TOIL ALE ALL
ILL ELL TELL WELL WILL SILL HILL HELL LET LEST NEST REST TEST WEST WET WIT WIN WINE TWIN TWO TOWN WORE WORST CLOT
COST HOST MOST POST OAK KOA ASK TASK SOAK TOES TEAS SEAT EAST NEAT HEAT HEAR TEAR RARE CART CARE RACE ACE ICE NICE
RICE ORCA ROC HOE HOES SHOE SHOT SHOW WHAT THAT THIS THESE THOSE THERE WHERE HERE HERO TORE STORE SNORE SORE ROSE NOSE
TONE STONE STEN SENT SEEN TEEN KEEN KNEE KNOT KNOW SNOW STOW STEW SEW SAW WAS WAR RAW AWE EWE WEE TEE LEE EEL ELK
KEEL KALE LAKE TAKE SAKE RAKE ROKE COKE CLOAK CROCK CLICK TRICK TREK TREE TRIO RIOT TORI IRON NOIR LION LOIN COIN
ICON CION INTO ONTO UNTO NOTE TOTE TOTS LOTS SLOT LOST LIST SILT SLIT KISS MISS HISS LESS LOSS TOSS
EKE EKES LEEK SEEK REEK WEEK TIC TAC TOC AIL AIR SIC SIS TIT TAT OHO AHA ARK IRK INN ION RIN EEN ENE ERE ERR ORT RET TET HET OHS ETH ITH WEN WREN TREN
""".split())

def key_problems(keystr, ledger, message):
    """reasons the door-order key string / ledger give too much away (empty list = acceptable)"""
    msg = message.replace(" ", ""); bad = []
    grams = {msg[i:i + 3] for i in range(len(msg) - 2)}
    for i in range(len(keystr) - 2):
        if keystr[i:i + 3] in grams: bad.append(f"run {keystr[i:i + 3]} from the message")
    for n in range(3, 7):
        for i in range(len(keystr) - n + 1):
            if keystr[i:i + n] in BANNED_WORDS: bad.append(f"word {keystr[i:i + n]}")
    if sum(a == b for a, b in zip(keystr, msg)) > 2: bad.append("too many letters in message position")
    for i in range(len(ledger) - 1):
        if abs(ledger[i + 1] - ledger[i]) == 1: bad.append(f"ledger run {ledger[i]},{ledger[i + 1]}")
    if sum(ledger[i] == i + 1 for i in range(len(ledger))) > 1: bad.append("ledger fixed points")
    return bad

def key_score(keystr, ledger, message):
    """lower is better: message bigrams kept in order, adjacent ledger steps of 2, doubled letters"""
    msg = message.replace(" ", ""); bi = {msg[i:i + 2] for i in range(len(msg) - 1)}
    return (sum(keystr[i:i + 2] in bi for i in range(len(keystr) - 1)) * 3
            + sum(abs(ledger[i + 1] - ledger[i]) <= 2 for i in range(len(ledger) - 1))
            + sum(keystr[i] == keystr[i + 1] for i in range(len(keystr) - 1)))

def random_matching(answers, msg, rnd):
    """random perfect matching door -> message slot, slot letter must occur in the door's answer"""
    doors = list(answers); rnd.shuffle(doors); slot_of = {}; door_of = {}
    def augment(d, seen):
        opts = [p for p in range(len(msg)) if msg[p] in answers[d]]; rnd.shuffle(opts)
        for p in opts:
            if p in seen: continue
            seen.add(p)
            if p not in door_of or augment(door_of[p], seen):
                door_of[p] = d; slot_of[d] = p; return True
        return False
    for d in doors:
        if not augment(d, set()): return None
    return slot_of

def choose_keys(message=MESSAGE, seed=KEY_SEED, candidates=KEY_CANDIDATES):
    """-> (keys {door: 1-based key position}, ledger [door for each message slot])"""
    answers = {d: a for d, _, a in SPEC}; msg = message.replace(" ", ""); rnd = random.Random(seed)
    best = None; found = 0
    for _ in range(200000):
        slot_of = random_matching(answers, msg, rnd)
        if slot_of is None: continue
        keys = {}
        for d, p in slot_of.items():
            keys[d] = rnd.choice([i + 1 for i, ch in enumerate(answers[d]) if ch == msg[p]])
        ledger = [None] * len(msg)
        for d, p in slot_of.items(): ledger[p] = d
        keystr = "".join(answers[d][keys[d] - 1] for d in sorted(answers))
        if key_problems(keystr, ledger, message): continue
        sc = key_score(keystr, ledger, message); found += 1
        if best is None or sc < best[0]: best = (sc, keys, ledger)
        if found >= candidates: break
    assert best, "no acceptable key assignment"
    _, keys, ledger = best
    assert "".join(answers[d][keys[d] - 1] for d in ledger) == msg and sorted(ledger) == sorted(answers)
    return keys, ledger

FILL = "ABCDEFGHIKLMNOPRSTUVWY"

def letters_grid(n, cells, word, rnd, avoid=()):
    """Letter in every cell; `cells` (in reading order) carry `word`, the rest random."""
    g = [[rnd.choice(FILL) for _ in range(n)] for _ in range(n)]
    for (r, c), ch in zip(cells, word): g[r][c] = ch
    for (r, c) in avoid: g[r][c] = ""
    return ["|".join(row) for row in g]

def door(d, typ, ans, key):
    rnd = random.Random(1000 + d)
    out = dict(door=d, type=typ, answer=ans, key=key, letter=ans[key - 1])
    if typ == "wordsearch":
        if d == 1:
            pool = "STAR BELL SNOW GIFT BOW SLED COCOA PINE CAKE CANDY TREE SOCKS SCARF ANGEL MITTEN SANTA ROBIN NORTH".split()
            out.update(misc.gen_wordsearch(8, pool, "THEKEYIS" + ans, [(0, 1), (1, 0), (1, 1)], d, max_words=11))
            out["dirs"] = "across, down or diagonally down-right"
        else:
            pool = ("CHIMNEY STOCKING GARLAND RIBBON PARCEL SNOWMAN NUTMEG COOKIE PUDDING GINGER MITTENS SCARF SLED CANDY "
                    "FIRESIDE ORNAMENT KETTLE BLANKET CRACKER SLIPPERS CINNAMON CHESTNUT PINECONE SNOWDRIFT WINTER JUMPER").split()
            out.update(misc.gen_wordsearch(10, pool, "THEKEYIS" + ans, misc.D8, d, max_words=18))
            out["dirs"] = "in any of the eight directions, including backwards"
    elif typ == "caesar":
        plain = "HANG THE GREEN LEAVES AND RED BERRIES ABOVE EVERY DOOR. THE KEY IS " + ans + "."
        out.update(shift=3, plain=plain, cipher=misc.caesar(plain, 3))
    elif typ == "queens":
        n = len(ans)
        q = grids.gen_queens(n, 30 + d); out.update(q)
        out["letters"] = letters_grid(n, q["stars"], ans, rnd)
    elif typ == "wordoku":
        n = len(ans); br, bc = (2, 3) if n == 6 else (3, 3)
        w = grids.gen_wordoku(n, br, bc, 40 + d, 14 if n == 6 else 32)
        full = w["full"]; sym = sorted(set(ans))      # digit k <-> letter sym[k]
        # shaded cells: one per answer letter, not givens, in reading order
        free = [x for x in sorted(full) if x not in w["givens"]]
        pick = []                                    # numbered cells 1..len(ans), one per answer letter
        for ch in ans:
            cand = [x for x in free if sym[full[x]] == ch and x not in pick and all(max(abs(x[0] - y[0]), abs(x[1] - y[1])) > 1 for y in pick)]
            pick.append(rnd.choice(cand))
        out.update(n=n, br=br, bc=bc, symbols=sym, givens={f"{r},{c}": sym[v] for (r, c), v in w["givens"].items()},
                   full=["".join(sym[full[(r, c)]] for c in range(n)) for r in range(n)], shaded=pick)
    elif typ == "maze":
        out.update(misc.gen_maze(15, 11, ans, 12, 50 + d))
    elif typ == "nonogram":
        pic = "CANDLE" if ans == "CANDLE" else "BELL"
        g = nonogram.parse(nonogram.PICS[pic]); R, C = nonogram.picture_clues(g)
        out.update(rows=R, cols=C, picture=["".join("#" if v else "." for v in r) for r in g])
    elif typ == "pyramid":
        base = [ord(ch) - 64 for ch in ans]
        out.update(misc.gen_pyramid(base, 60 + d))
    elif typ == "pigpen":
        out["plain"] = "FROZEN DRIPS HANG FROM THE EAVES. THE KEY IS " + ans + "."
    elif typ == "logic":
        lg = misc.gen_logic(70 + d); out.update(lg)
        assert "".join(misc.NAMES[g][0] for g in sorted(range(5), key=lambda g: lg["room"][g])).upper() == ans
    elif typ == "tents":
        for s in range(200):
            t = grids.gen_tents(8, len(ans), 80 + d * 100 + s)
            if sum(1 for v in t["rows"] + t["cols"] if v == 0) <= 2: break
        out.update(t); out["letters"] = letters_grid(8, t["tents"], ans, rnd, avoid=t["trees"])
    elif typ == "tracks":
        band = "Easy" if len(ans) <= 6 else "Medium"
        for s in range(500):
            p = tracks_gen.make((band, 900 + d * 50 + s))
            if not p: continue
            path = [tuple(x) for x in p["solution"]]; n = p["n"]
            giv = {divmod(int(k), n) for k in p["givens"]}
            free = [x for x in path if x not in giv and x != path[0] and x != path[-1]]
            if len(free) < len(ans) * 1.4: continue
            idx = [round(i * (len(free) - 1) / (len(ans) - 1)) for i in range(len(ans))]
            cells = [free[i] for i in idx]
            if len(set(cells)) != len(ans): continue
            off = [(r, c) for r in range(n) for c in range(n) if (r, c) not in set(path)]
            rnd.shuffle(off); dec = off[:max(3, len(ans) // 2)]
            letters = {f"{r},{c}": ch for (r, c), ch in zip(cells, ans)}
            letters.update({f"{r},{c}": rnd.choice(FILL) for r, c in dec})
            out.update(p); out["letters"] = letters; out["answer_cells"] = cells
            break
        else: raise RuntimeError("tracks")
    elif typ == "akari":
        a = grids.gen_akari(7, len(ans), 120 + d); out.update(a)
        black = {tuple(x) for x in a["black"]}
        out["letters"] = letters_grid(7, a["bulbs"], ans, rnd, avoid=black)
    elif typ == "fillin":
        W = ("CHIMNEY STOCKING GARLAND RIBBON PARCEL SNOWMAN NUTMEG COOKIE PUDDING GINGER MITTENS SCARF SLED CANDY "
             "HAMPER CHESTNUT HOLIDAY KETTLE BLANKET CRACKER SLIPPERS").split()
        for s in range(400):
            try: f = misc.gen_fillin(W, 11, 130 + d * 1000 + s, 12, need={"H": 3, "E": 2, "A": 2, "R": 2, "T": 2}, tries=20000)
            except RuntimeError: continue
            g = {}
            for sl in f["slots"]:
                for x, ch in zip(sl["cells"], sl["word"]): g[tuple(x)] = ch
            giv = {tuple(map(int, k.split(","))) for k in f["given"]}
            cells = sorted(x for x in g if x not in giv)
            pick = []
            used = set()
            for ch in ans:
                cand = [x for x in cells if g[x] == ch and x not in used and all(abs(x[0] - y[0]) + abs(x[1] - y[1]) > 2 for y in used)]
                if not cand: break
                x = rnd.choice(cand); pick.append(x); used.add(x)
            if len(pick) == len(ans):
                out.update(f); out["numbered"] = pick; break
        else: raise RuntimeError("fillin")
    elif typ == "presents":
        p = grids.gen_presents(7, len(ans), 140 + d); out.update(p)
        clue_cells = {tuple(map(int, k.split(","))) for k in p["clues"]}
        out["letters"] = letters_grid(7, p["presents"], ans, rnd, avoid=clue_cells)
    elif typ in ("futoshiki", "skyscrapers", "calcudoku"):
        f = dict(futoshiki=latin.gen_futoshiki, skyscrapers=latin.gen_skyscrapers, calcudoku=latin.gen_calcudoku)[typ](150 + d)
        sol = f["solution"]
        letters = list(dict.fromkeys(ans))
        extra = [ch for ch in "SANDGW" if ch not in letters]
        while len(letters) < 5: letters.append(extra.pop(0))
        rnd.shuffle(letters)
        keymap = {k + 1: letters[k] for k in range(5)}             # digit -> letter
        giv = {tuple(map(int, k.split(","))) for k in f.get("givens", {})}
        cells = [(r, c) for r in range(5) for c in range(5) if (r, c) not in giv]
        rnd.shuffle(cells); pick = []
        for ch in ans:
            x = next(x for x in cells if keymap[sol[x[0]][x[1]]] == ch and x not in pick); pick.append(x)
        out.update(f); out["keymap"] = {str(k): v for k, v in keymap.items()}; out["numbered"] = pick
    elif typ == "morse":
        out["plain"] = "NUTMEG ON TOP. THE KEY IS " + ans + "."
    elif typ == "fleet":
        fl = grids.gen_fleet(7, [3, 2, 2, 1, 1, 1], 170 + d); out.update(fl)
        out["letters"] = letters_grid(7, fl["cells"], ans, rnd)
    return out

if __name__ == "__main__":
    only = set(map(int, sys.argv[1:]))
    try: data = json.load(open("../data.json"))
    except FileNotFoundError: data = {}
    doors = {int(k): v for k, v in data.get("doors", {}).items()}
    keys, slots = choose_keys()
    for d, typ, ans in SPEC:
        if only and d not in only and d in doors: continue
        doors[d] = door(d, typ, ans, keys[d]); print(d, typ, ans, "ok", flush=True)
        json.dump(dict(doors={str(k): doors[k] for k in sorted(doors)}), open("../data.json", "w"), default=list)
    # key position/letter never affect a puzzle, so refresh them on doors that were not regenerated
    for d, typ, ans in SPEC: doors[d].update(key=keys[d], letter=ans[keys[d] - 1])
    # Christmas Eve ledger: slot i of the message is filled by the key letter of door slots[i]
    assert "".join(doors[x]["letter"] for x in slots) == MESSAGE.replace(" ", "")
    json.dump(dict(message=MESSAGE, ledger=slots, doors={str(k): doors[k] for k in sorted(doors)}), open("../data.json", "w"), default=list)
    print("keys (door order)", "".join(doors[d]["letter"] for d in sorted(doors)))
    print("ledger", slots)
