"""Checks the book text and writes ../verification.md."""
import os, re, itertools, book
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
VIOLENT = re.compile(
    r"\b(murder\w*|kill|killed|killing|killer|death|deaths|dead|bloody|blood|weapon\w*|gun|guns|"
    r"stab\w*|violent|violence|corpse|assassin\w*|steal\w*|stole|stolen|thief|thieves|crime\w*)\b",
    re.I,
)
problems, lines = [], []
secs = book.sections()
if len(book.CASES) != 28:
    problems.append(f"expected 28 cases, got {len(book.CASES)}")
titles = [c["title"] for c in book.CASES]
if len(set(titles)) != len(titles):
    problems.append("duplicate case titles")
for i, c in enumerate(book.CASES):
    story = " ".join(c["story"].split())
    for k in c["keys"]:
        if " ".join(k.split()) not in story:
            problems.append(f"case {i+1}: clue not in story before question: {k!r}")
    for part in ("story", "ask", "solution"):
        if len(c[part].split()) < (3 if part == "ask" else 40):
            problems.append(f"case {i+1}: {part} too short")
for sid, h, blocks in secs:
    if sid.startswith("case"):
        kinds = [k for k, _ in blocks]
        texts = [t for _, t in blocks]
        a = texts.index(next(t for t in texts if t.startswith(book.ASK)))
        if kinds[a + 1] != "think" or texts[a + 1] != book.THINK:
            problems.append(f"{sid}: no Think about it after question")
body = book.all_text(include_copyright=False)
heads = {h for _, h, _ in secs}
body_no_heads = "\n".join(l for l in body.split("\n") if l not in heads)
digits = re.findall(r"\d+", body_no_heads)
if digits:
    problems.append(f"digits in body text: {sorted(set(digits))[:20]}")
v = sorted({m.group(0).lower() for m in VIOLENT.finditer(book.all_text())})
if v:
    problems.append(f"flagged words: {v}")
for bad in ["\t", "*", "|", "[", "]", "^"]:
    if bad in body:
        problems.append(f"odd character {bad!r} in text")
words = len(book.all_text().split())
if not 9000 <= words <= 23000:
    problems.append(f"word count {words} outside 9,000 to 23,000")

# Logic: Reading Circle Seats
people = ["Pearl", "Owen", "Clara", "Mabel"]
seat_sols = []
for perm in itertools.permutations(range(1, 5)):
    pos = dict(zip(people, perm))
    if pos["Pearl"] in (1, 4):
        continue
    if not pos["Owen"] < pos["Clara"]:
        continue
    if abs(pos["Mabel"] - pos["Pearl"]) != 1:
        continue
    if pos["Clara"] == 4:
        continue
    seat_sols.append(pos)
if len(seat_sols) != 1 or seat_sols[0] != {"Pearl": 3, "Owen": 1, "Clara": 2, "Mabel": 4}:
    problems.append(f"Reading Circle Seats not unique: {seat_sols}")

# Logic: The Moved Map (only culprit fibs)
S = ["Theo", "Jules", "Marcus", "Dot"]
map_sols = []
for c in S:
    st = {
        "Theo": c != "Jules",
        "Jules": c in ("Theo", "Marcus"),
        "Marcus": c != "Marcus" and c != "Dot",
    }
    st["Dot"] = st["Jules"]
    if all(st[p] == (p != c) for p in S):
        map_sols.append(c)
if map_sols != ["Marcus"]:
    problems.append(f"Moved Map not unique: {map_sols}")

# Logic: Queue at Closing
Q = ["Nora", "Benji", "Edna", "Greta", "Pip"]
queue_sols = []
for perm in itertools.permutations(range(1, 6)):
    pos = dict(zip(Q, perm))
    if pos["Nora"] != 3 or pos["Benji"] != 1:
        continue
    if pos["Greta"] == 5 or abs(pos["Greta"] - pos["Benji"]) == 1:
        continue
    if not pos["Pip"] > pos["Edna"]:
        continue
    behind = [p for p in Q if pos[p] == pos["Nora"] + 1][0]
    queue_sols.append(behind)
if queue_sols != ["Greta"]:
    problems.append(f"Queue at Closing not unique: {queue_sols}")

# Logic: Poetry Night Fib (exactly one truth per person)
P = ["Clara", "Jules", "Harper", "Edna"]
fib_sols = []
for c in P:
    st = {
        "Clara": [c != "Clara", c == "Jules"],
        "Jules": [c != "Jules", c == "Harper"],
        "Harper": [c != "Harper", c == "Clara"],
        "Edna": [c != "Edna", c != "Harper"],
    }
    if all(sum(v) == 1 for v in st.values()):
        fib_sols.append(c)
if fib_sols != ["Edna"]:
    problems.append(f"Poetry Night Fib not unique: {fib_sols}")

logic_n = sum(1 for c in book.CASES if c.get("kind") == "logic")
story_n = len(book.CASES) - logic_n

lines.append("# Verification: Clues Between the Shelves\n")
lines.append(f"- Cases: {len(book.CASES)} ({story_n} observation/clue stories + {logic_n} text-logic)")
lines.append("- Reading Circle Seats checked by trying every seating: exactly one fits (Mabel in chair four)")
lines.append("- The Moved Map checked: exactly one culprit-fibber assignment fits (Marcus)")
lines.append("- The Queue at Closing checked by trying every line order: exactly one person immediately behind Nora (Greta)")
lines.append("- Poetry Night Fib checked: exactly one person fits the one-truth-one-fib pattern (Edna)")
lines.append(f"- Each case has clue phrases in the story before the question, then Can you solve it, Think about it, solution")
lines.append(f"- Word count (whole book): {words:,}")
per = [len((c["story"] + c["ask"] + c["solution"]).split()) for c in book.CASES]
lines.append(f"- Words per case: {min(per)} to {max(per)}")
lines.append("- Digits in body text: none" if not digits else f"- Digits in body text: {digits[:10]}")
lines.append(
    "- Violent or crime vocabulary (murder, kill, dead, blood, weapon, steal, thief, crime and similar): none"
    if not v
    else f"- Flagged words: {v}"
)
lines.append("- No tables, images, grids or footnotes in chapters (text paragraphs only)")
lines.append(f"\n**Result: {'PASS' if not problems else 'FAIL'}**\n")
for p in problems:
    lines.append(f"- PROBLEM: {p}")
open(os.path.join(ROOT, "verification.md"), "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
raise SystemExit(1 if problems else 0)
