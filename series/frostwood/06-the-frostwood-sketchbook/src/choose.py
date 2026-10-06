"""Chooses the book's puzzles from ../tmp/candidates.json (made by master.py); run as python3 choose.py and writes ../data.json.
Band rules (checked again by verify.py):
  Easy    15x15, line-solvable in at most 9 sweeps
  Medium  20x20, line-solvable in 3 to 12 sweeps
  Hard    25x25, line-solvable in 6 to 13 sweeps
  Expert  25x25, line-solvable in 14 or more sweeps
Each subject appears once. Fewer flipped pixels (truer pictures) are preferred."""
import json
BANDS = {"Easy": dict(n=15, lo=1, hi=9, count=30), "Medium": dict(n=20, lo=3, hi=12, count=40),
         "Hard": dict(n=25, lo=6, hi=13, count=40), "Expert": dict(n=25, lo=14, hi=99, count=30)}
ORDER = ("Easy", "Medium", "Hard", "Expert")
# hand-drawn 8x8 worked example: a cottage with its door, on the snow
EXAMPLE_PIC = ["...##...", "..####..", ".######.", "########", ".##..##.", ".##..##.", ".######.", "########"]

if __name__ == "__main__":
    C = json.load(open("../tmp/candidates.json"))
    used = set(); out = {}
    for band in ("Expert", "Hard", "Easy", "Medium"):
        B = BANDS[band]
        rs = [r for r in C if r["n"] == B["n"] and r["subject"] not in used
              and B["lo"] <= r["grade"]["sweeps"] <= B["hi"]]
        key = (lambda r: (len(r["flips"]), -r["grade"]["sweeps"], r["subject"])) if band == "Expert" else \
              (lambda r: (len(r["flips"]), r["subject"]))
        rs.sort(key=key); pick = rs[:B["count"]]
        assert len(pick) == B["count"], (band, len(pick))
        used |= {r["subject"] for r in pick}
        pick.sort(key=lambda r: (r["grade"]["sweeps"], r["grade"]["moves"], r["subject"]))
        for r in pick: r["band"] = band
        out[band] = pick
    from nonogram import picture_clues, grade
    pic = EXAMPLE_PIC; img = [[1 if ch == "#" else 0 for ch in r] for r in pic]
    rows, cols = picture_clues(img)
    out["Example"] = [dict(subject=-1, char="", name="A Little Cottage", n=8, variant=0, flips=[], rows=rows, cols=cols,
                           picture=pic, grade=grade(rows, cols), band="Example", num=0)]
    num = 1
    for b in ORDER:
        for r in out[b]: r["num"] = num; num += 1
    json.dump(out, open("../data.json", "w"))
    print({b: len(out[b]) for b in out}, "total", num - 1)
