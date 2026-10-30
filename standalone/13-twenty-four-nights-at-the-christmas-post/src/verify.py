"""Checks the book text and writes ../verification.md."""
import os, re, book
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
VIOLENT = re.compile(r"\b(murder\w*|kill|killed|killing|killer|death|deaths|dead|bloody|blood|weapon\w*|gun|guns|stab\w*|violent|violence|corpse|assassin\w*|steal\w*|stole|stolen|thief|thieves|crime\w*)\b", re.I)
problems, lines = [], []
secs = book.sections()
if len(book.CASES) != 24: problems.append(f"expected 24 cases, got {len(book.CASES)}")
titles = [c["title"] for c in book.CASES]
if len(set(titles)) != len(titles): problems.append("duplicate case titles")
for i, c in enumerate(book.CASES):
    story = " ".join(c["story"].split())
    for k in c["keys"]:
        if " ".join(k.split()) not in story: problems.append(f"case {i+1}: clue not in story before question: {k!r}")
    for part in ("story", "ask", "solution"):
        if len(c[part].split()) < (3 if part == "ask" else 40): problems.append(f"case {i+1}: {part} too short")
for sid, h, blocks in secs:
    if sid.startswith("case"):
        kinds = [k for k, _ in blocks]; texts = [t for _, t in blocks]
        a = texts.index(next(t for t in texts if t.startswith(book.ASK)))
        if kinds[a + 1] != "think" or texts[a + 1] != book.THINK: problems.append(f"{sid}: no Think about it after question")
body = book.all_text(include_copyright=False)
heads = {h for _, h, _ in secs}
body_no_heads = "\n".join(l for l in body.split("\n") if l not in heads)
digits = re.findall(r"\d+", body_no_heads)
if digits: problems.append(f"digits in body text: {sorted(set(digits))[:20]}")
v = sorted({m.group(0).lower() for m in VIOLENT.finditer(book.all_text())})
if v: problems.append(f"flagged words: {v}")
for bad in ["\t", "*", "|", "[", "]", "^"]:
    if bad in body: problems.append(f"odd character {bad!r} in text")
words = len(book.all_text().split())
if not 9000 <= words <= 23000: problems.append(f"word count {words} outside 9,000 to 23,000")
# snowflake message and per-night letter lines
msg = "".join(c["letter"] for c in book.CASES)
if msg != "THANKYOUFOREVERYKINDNESS": problems.append(f"snowflake letters spell {msg}")
for i, c in enumerate(book.CASES):
    if f"snowflake letter is {c['letter']}" not in " ".join(c["solution"].split()): problems.append(f"night {i+1}: letter line missing")
# Night Seventeen Secret Santa: brute-force that the clues give exactly one answer
from itertools import permutations
P = ["Nell", "Walt", "Rafe", "Wren"]
sols = []
for perm in permutations(P):
    d = dict(zip(P, perm))
    if any(d[x] == x for x in P): continue
    if d["Nell"] != "Rafe": continue
    if not d["Rafe"].startswith("W") or d["Rafe"] == "Wren": continue
    if d["Walt"] == "Nell": continue
    sols.append(d)
if len(sols) != 1 or sols[0] != {"Nell": "Rafe", "Rafe": "Walt", "Walt": "Wren", "Wren": "Nell"}: problems.append(f"Secret Santa not unique: {sols}")
# Night Nineteen: twelfth house from the church end of houses one to twenty-one
if list(range(21, 0, -1))[11] != 10: problems.append("wreath count wrong")
lines.append("# Verification: Twenty-Four Nights at the Christmas Post\n")
lines.append(f"- Snowflake letters across the twenty-four nights spell: {msg} (Thank you for every kindness)")
lines.append("- Night Seventeen (Secret Santa) checked by trying every possible draw: exactly one fits the clues")
lines.append("- Night Nineteen (wreath) checked: the twelfth house counting down from number twenty-one is number ten")
lines.append(f"- Nights (mysteries): {len(book.CASES)} (each with its clue phrases present in the story before the question, then Can you solve it, Think about it, solution)")
lines.append(f"- Word count (whole book): {words:,}")
lines.append(f"- Words per night: {min(len((c['story']+c['ask']+c['solution']).split()) for c in book.CASES)} to {max(len((c['story']+c['ask']+c['solution']).split()) for c in book.CASES)}")
lines.append("- Digits in body text: none" if not digits else f"- Digits in body text: {digits[:10]}")
lines.append("- Violent or crime vocabulary (murder, kill, dead, blood, weapon, steal, thief, crime and similar): none" if not v else f"- Flagged words: {v}")
lines.append("- No tables, images, grids or footnotes in chapters (text paragraphs only)")
lines.append(f"\n**Result: {'PASS' if not problems else 'FAIL'}**\n")
for p in problems: lines.append(f"- PROBLEM: {p}")
open(os.path.join(ROOT, "verification.md"), "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
