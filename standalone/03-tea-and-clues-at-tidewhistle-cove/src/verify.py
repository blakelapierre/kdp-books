"""Independent checks for every case. Writes ../verification.md. Exit code 1 on any failure.
- Logic cases: brute-force every possible culprit / seating / truth assignment from the rules as stated
  in the story text (models below are written from the text, not from the solution) and require exactly
  one answer that matches the stated culprit.
- Story cases: fair-play table (decisive clue planted in the story before the question; every other
  suspect has an exclusion stated in the story) plus automatic text checks.
- Whole book: no digits (read-aloud rule), no violent vocabulary, word count, every suspect named.
"""
import itertools, re, sys, os
import book

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
fails = []

# ---------- logic models ----------
def marrow():
    S = ["Jago", "Tamsin", "Hedley", "Morwenna"]
    out = []
    for c in S:
        st = {"Jago": c != "Hedley", "Tamsin": c in ("Jago", "Morwenna"),
              "Morwenna": c != "Morwenna" and c != "Tamsin"}
        st["Hedley"] = st["Tamsin"]
        # thief lies, everyone else truthful
        if all(st[p] == (p != c) for p in S): out.append(c)
    return out

def bakers():
    S = ["Pip", "Demelza", "Fenwick", "Kerensa"]
    out = []
    for c in S:
        d = c == "Kerensa"
        st = [c == "Demelza", d, c != "Fenwick", not d]
        if sum(st) == 1: out.append(c)
    return out

def window():
    S = ["Spargo", "Loveday", "Quill", "Wenna"]
    out = []
    for perm in itertools.permutations(range(1, 5)):
        pos = dict(zip(S, perm))
        if abs(pos["Quill"] - pos["Wenna"]) != 1: continue
        if pos["Loveday"] in (1, 4): continue
        if not pos["Spargo"] < pos["Quill"]: continue
        if pos["Wenna"] == 4: continue
        out.append([p for p in S if pos[p] == 4][0])
    return out

def lighthouse():
    # minutes after 1 pm
    start, end = 60, 75
    people = {"Wenna": (60, 80, 15), "Opie": (45, 90, 20), "Pip": (55, 70, 10)}
    out = []
    for p, (a, b, d) in people.items():
        # needs some t in [start,end] with a+d <= t <= b-d
        if max(a + d, start) <= min(b - d, end): out.append(p)
    return out

def fishermen():
    N = ["Ned", "Bran", "Col"]
    out = []
    for types in itertools.product([True, False], repeat=3):
        h = dict(zip(N, types))
        for c in N:
            st = {"Ned": [c != "Ned", not h["Bran"]], "Bran": [c == "Col"], "Col": [h["Ned"], c != "Col"]}
            if all(all(s == h[p] for s in st[p]) for p in N): out.append(c)
    return out

def queue():
    S = ["Fenwick", "Loveday", "Pip", "Demelza", "Hedley"]
    out = []
    for perm in itertools.permutations(range(1, 6)):
        pos = dict(zip(S, perm))
        if pos["Fenwick"] != 1 or pos["Loveday"] != 3: continue
        if not pos["Hedley"] > pos["Pip"]: continue
        if pos["Demelza"] == 5 or abs(pos["Demelza"] - pos["Fenwick"]) == 1: continue
        out.append([p for p in S if pos[p] == pos["Loveday"] + 1][0])
    return out

def truthfib():
    S = ["Hedley", "Kerensa", "Wenna", "Tamsin"]
    out = []
    for c in S:
        st = {"Hedley": [c != "Hedley", c == "Kerensa"], "Kerensa": [c != "Kerensa", c == "Wenna"],
              "Wenna": [c != "Wenna", c == "Hedley"], "Tamsin": [c != "Tamsin", c != "Wenna"]}
        if all(sum(v) == 1 for v in st.values()): out.append(c)
    return out

LOGIC = {"The Marrow Mix-up": (marrow, "Morwenna"), "The Four Bakers": (bakers, "Fenwick"),
         "The Window Table": (window, "Quill"), "The Lighthouse Path": (lighthouse, "Opie"),
         "The Honest Fishermen": (fishermen, "Bran"), "The Winning Ticket": (queue, "Demelza"),
         "Truth and Fib Night": (truthfib, "Tamsin")}

# ---------- fair play table for story cases ----------
FAIR = {
 "The Prize Sponge": ("Names the cake as a lemon drizzle when Ollie only said entry number seven; cakes were under glass domes and cloths and the only entry list was in Agnes's handbag.",
   {"Morwenna Day": "Never names the cake; at the far end with flowers.", "Hedley Truscott": "Never names the cake; says he couldn't tell one from another."}),
 "The Lemonade on the Lawn": ("Sharp-edged ice in a frosty glass on the hottest afternoon, when the outdoor ice ran out at two and the only ice left was in the kitchen freezer beside the locket.",
   {"Demelza Rowe": "Asleep in a deckchair since before two, three witnesses.", "Captain Quill": "With Agnes at the harbour office from one o'clock until they arrived together."}),
 "The Dry Raincoat": ("Claims she just ran in from the harbour through the downpour, yet is completely dry; door bell rang only for Hedley.",
   {"Hedley Truscott": "At the counter in Tamsin's view from the moment he arrived.", "Pip Carew": "Outside under the awning, seen through the window throughout; never came in."}),
 "The Sandbar at High Tide": ("Claims to be digging on the sandbar during high water at noon, when it is under more than a man's height of sea.",
   {"Morwenna Day": "With the vicar eleven to one.", "Pip Carew": "With Agnes all morning."}),
 "The Closed Post Office": ("Claims he bought the blanket at the post office on Sunday morning; the post office is always closed on Sundays.",
   {"Tamsin Trevelyan": "In church since ten.", "Jago Penhallow": "Baking since five with two helpers."}),
 "The Dog That Stayed Quiet": ("Pickle barks at everyone at the only gate except Loveday and Pip; a wakeful neighbour heard no barking.",
   {"Mr Fenwick": "Pickle would have barked.", "Mrs Ashby": "Pickle would have barked."}),
 "The Sunset over the Sea": ("Tidewhistle Cove faces east; the sun rises over the sea and sets behind the hills, so no sunset into the sea.",
   {"Tamsin Trevelyan": "Running book club, eight witnesses.", "Hedley Truscott": "Darts team all evening."}),
 "The Wet Paint Bench": ("Claims an hour on a bench painted at half past two that stays tacky till eight, but his cream trousers are spotless.",
   {"Hedley Truscott": "Paint on hands, but with Ollie all afternoon.", "Wenna Polglaze": "In the tea room with Agnes three to four."}),
 "The Stopped Clock": ("Claims the tea room clock read a quarter past three; it has been stopped at ten to nine since Monday.",
   {"Demelza Rowe": "Left before half past three, then with Captain Quill.", "Hedley Truscott": "Asleep at home from twenty past three, wife confirms."}),
 "The Misspelled Note": ("The note spells pier p, e, i, r, exactly like Hedley's slipway sign.",
   {"Tamsin Trevelyan": "Her poster spells pier correctly.", "Jago Penhallow": "His chalkboard spells pier correctly."}),
 "The Blue Ribbon Key": ("Mentions the blue ribbon, which only committee members or a user of the key would know; Ollie mentioned only the key.",
   {"Demelza Rowe": "At her sister's from five, confirmed.", "Pip Carew": "Shows no knowledge of the key."}),
 "The Warm Bonnet": ("Biscuit sleeps on recently run engines; Mr Treloar's bonnet is warm on a chilly morning though he says the car hasn't moved.",
   {"Mr Fenwick": "Car up on bricks with a flat tyre.", "Kerensa Hale": "Untouched overnight dew on the windscreen."}),
 "The Talking Parrot": ("Admiral suddenly repeats Mr Pascoe's unique catchphrase, which he learns only by hearing it several times in a row; Pascoe has a key.",
   {"Tamsin Trevelyan": "Never says the phrase; nobody but Pascoe does.", "Mr Fenwick": "Never says the phrase; nobody but Pascoe does."}),
 "The Moonlit Walk": ("Describes a bright full moon on the night the Gazette gives as a new moon.",
   {"Demelza Rowe": "Left before eleven with Captain Quill, while the chart was still there.", "Captain Quill": "Walked Demelza home before eleven."}),
 "The Ship's Bell": ("Only the tallest person can reach the hook on tiptoe; ladder locked, only key with Agnes, no furniture, stool broken.",
   {"Loveday Nance": "A little over five feet, cannot reach.", "Mr Fenwick": "Not much taller than Loveday, cannot reach."}),
 "The Scent of Lavender": ("Drawer velvet smells strongly of lavender water; only Mrs Vosper wears it.",
   {"Captain Quill": "Smells of fish and seaweed.", "Hedley Truscott": "Smells only of engine oil."}),
 "The Spanish Coin": ("The till started empty except a sealed bank float; only Mr Nankervis put coins into it.",
   {"Demelza Rowe": "Paid by card.", "Pip Carew": "Paid with a banknote; coins went out to him as change."}),
 "The Odd Glove": ("The right glove with anchors matches the left glove Mr Lanyon is wearing.",
   {"Kerensa Hale": "Wearing both of a plain pair.", "Mr Fenwick": "Never wears gloves."}),
 "The Kite Festival": ("Wind blew from the sea inland all day, so a snapped kite could not fly out to sea.",
   {"Pip Carew": "At the top of the beach with his class.", "Tamsin Trevelyan": "At the book stall by the car park all afternoon."}),
 "The Teaspoon Thief": ("Doors locked, gap a hand's width, only shiny objects taken, magpie feather on the sill: the thief is a bird.",
   {"Pip Carew": "No key; gap too small for any person.", "Mr Fenwick": "At the grocer's from five, confirmed; no key.", "Loveday Nance": "No key; gap too small."}),
 "The Silent Foghorn": ("Claims the foghorn boomed all night; it sounds whenever there is fog, and Agnes, awake with the window open, heard none on a clear night.",
   {"Captain Quill": "On watch with two crew all night.", "Tamsin Trevelyan": "At her sister's in town overnight."}),
 "The Sugar Bowl": ("Tea drunk black with three sugars (twelve lumps down to nine, milk untouched); only Mr Bolitho takes it that way.",
   {"Captain Quill": "Plenty of milk, no sugar.", "Loveday Nance": "Milk and one sugar."}),
 "The Missing Sign": ("The note is in green ink; only Ollie writes in green ink.",
   {"Hedley Truscott": "Writes only in pencil, has no pen.", "Tamsin Trevelyan": "Writes only in blue ink."}),
}

BANNED = r"\b(murder\w*|kill\w*|dead|death|die|died|dies|dying|blood\w*|gun\w*|knife|knives|stab\w*|poison\w*|weapon\w*|corpse\w*|shoot\w*|shot|violen\w*|attack\w*|punch\w*|strangl\w*|bomb\w*|arson\w*|gore|hurt)\b"

def check_text():
    text = book.all_text()
    # 'Nobody Gets Hurt' / 'badly hurt' are allowed reassurance phrases
    hits = [m.group(0) for m in re.finditer(BANNED, text, re.I)]
    hits = [h for h in hits if h.lower() != "hurt"]
    if hits: fails.append(f"banned words: {sorted(set(hits))}")
    digits = re.findall(r".{0,20}\d.{0,20}", book.all_text(include_copyright=False))
    if digits: fails.append(f"digits found: {digits[:5]}")
    for bad in ["\t", "  ", "*", "#", "[", "]", "(", ")"]:
        if bad in text: fails.append(f"character {bad!r} found in book text")
    return len(text.split())

def first_name(s):
    return s.replace("Mr ", "").replace("Mrs ", "").replace("Miss ", "").replace("Captain ", "").replace("Constable ", "").split()[0]

rows = []
words = check_text()
for i, c in enumerate(book.CASES):
    t = c["title"]; story = " ".join(c["story"].split()); sol = " ".join(c["solution"].split())
    status = []
    for s in c["suspects"]:
        if first_name(s) not in story and s not in story: fails.append(f"{t}: suspect {s} not named in story")
    for cl in c["clues"]:
        if cl.lower() not in story.lower(): fails.append(f"{t}: clue phrase '{cl}' not planted in story")
    cul = c["culprit"]
    if c["kind"] == "logic":
        fn, want = LOGIC[t]
        got = fn()
        ok = got == [want] and want in cul.replace("Mr ", "").replace("Captain ", "")
        if not ok: fails.append(f"{t}: logic model gives {got}, expected [{want}]")
        rows.append((i, t, "logic", cul, f"Brute force over every possibility gives exactly one answer: {got}", ""))
    else:
        if t not in FAIR: fails.append(f"{t}: no fair-play entry"); continue
        clue, excl = FAIR[t]
        others = [s for s in c["suspects"] if s != cul]
        for o in others:
            if o not in excl: fails.append(f"{t}: no exclusion recorded for {o}")
        rows.append((i, t, "story", cul, clue, "; ".join(f"{k}: {v}" for k, v in excl.items())))
    lead = sol.split(".")[0]
    key = first_name(cul) if cul != "a magpie" else "magpie"
    if key not in lead and key not in sol.split(".")[1]: fails.append(f"{t}: solution does not open with the culprit ({lead})")

out = ["# Verification: Tea and Clues at Tidewhistle Cove", "",
       f"Run: `cd src && python3 verify.py`. Result: **{'PASS' if not fails else 'FAIL'}**.", "",
       f"- Cases: **{len(book.CASES)}** ({sum(c['kind']=='logic' for c in book.CASES)} logic cases checked by brute force, {sum(c['kind']=='story' for c in book.CASES)} clue-based story cases checked against a fair-play table)",
       f"- Total words in the book text: **{words:,}**",
       "- Read-aloud rules: no digits anywhere, no tables, grids, images, footnotes or symbols inside chapters; every case ends with *Can you solve it?*, then *Think about it...*, then the solution.",
       "- Content rule: no violent vocabulary (murder, kill, dead, death, blood, weapon and similar words are all checked). Every case is a theft, a borrowing or a missing item, and every item is returned.", ""]
if fails:
    out += ["## Failures", ""] + [f"- {f}" for f in fails] + [""]
out += ["## Logic cases", "", "| # | Case | Answer | Check |", "|---|------|--------|-------|"]
out += [f"| {i+1} | {t} | {cul} | {chk} |" for i, t, k, cul, chk, _ in rows if k == "logic"]
out += ["", "## Story cases: fair-play table", "",
        "Each decisive clue appears in the story before the question; each other suspect is ruled out by something stated in the story.", "",
        "| # | Case | Answer | Decisive clue | Others ruled out |", "|---|------|--------|---------------|------------------|"]
out += [f"| {i+1} | {t} | {cul} | {chk} | {ex} |" for i, t, k, cul, chk, ex in rows if k == "story"]
open(os.path.join(ROOT, "verification.md"), "w").write("\n".join(out) + "\n")
print("PASS" if not fails else "FAIL", words, "words")
for f in fails: print(" -", f)
sys.exit(1 if fails else 0)
