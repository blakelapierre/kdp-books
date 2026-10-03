"""Independent verifier for Frostwood 05 puzzles.
Does NOT import generator construction paths for logic — re-solves from meta via logic_gen.SOLVERS.
For riddles: checks accept-list integrity and non-empty unique intended answer.
Writes ../verification.md
Run from src/: python3 verify.py
"""
from __future__ import annotations
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from normalize import normalize
from logic_gen import SOLVERS

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA = os.path.join(ROOT, "data.json")
OUT = os.path.join(ROOT, "verification.md")


def verify_riddle(p):
    ans = normalize(p["answer"])
    accept = {normalize(a) for a in p["accept"]}
    if not ans:
        return False, "empty answer"
    if ans not in accept:
        return False, "answer not in accept set"
    if len(accept) < 1:
        return False, "empty accept"
    # prompt must ask something
    if len(p["prompt"]) < 20:
        return False, "prompt too short"
    return True, "ok"


def verify_logic(p):
    meta = p.get("meta") or {}
    t = meta.get("type")
    if t not in SOLVERS:
        return False, f"no solver for {t}"
    sols = SOLVERS[t](meta)
    norms = [normalize(s) for s in sols]
    uniq = set(norms)
    if len(uniq) != 1:
        return False, f"not unique: {norms}"
    if normalize(p["answer"]) not in uniq:
        return False, f"answer {p['answer']!r} != sols {sols}"
    if normalize(p["answer"]) not in {normalize(a) for a in p["accept"]}:
        return False, "answer not in accept"
    return True, "ok"


def main():
    data = json.load(open(DATA, encoding="utf-8"))
    puzzles = data["puzzles"]
    rows = []
    failed = []
    by_band = {b: {"pass": 0, "fail": 0} for b in ("Easy", "Medium", "Hard", "Expert")}
    by_kind = {}
    for p in puzzles:
        kind = p["kind"]
        by_kind.setdefault(kind, {"pass": 0, "fail": 0})
        if kind == "riddle":
            ok, msg = verify_riddle(p)
        else:
            ok, msg = verify_logic(p)
        band = p["band"]
        if ok:
            by_band[band]["pass"] += 1
            by_kind[kind]["pass"] += 1
            rows.append((p["num"], band, kind, "PASS", p["answer"]))
        else:
            by_band[band]["fail"] += 1
            by_kind[kind]["fail"] += 1
            failed.append((p["num"], band, kind, msg, p.get("id")))
            rows.append((p["num"], band, kind, "FAIL", msg))

    # Uniqueness of prompts
    prompts = [normalize(p["prompt"]) for p in puzzles]
    dup_prompts = len(prompts) - len(set(prompts))

    lines = []
    lines.append("# Verification — Riddles by the Frostwood Fire")
    lines.append("")
    lines.append(f"Total puzzles: **{len(puzzles)}**")
    lines.append(f"Seed: `{data['seed']}`")
    lines.append("")
    lines.append("## Summary by difficulty")
    lines.append("")
    lines.append("| Band | Pass | Fail |")
    lines.append("|------|------|------|")
    for b in ("Easy", "Medium", "Hard", "Expert"):
        lines.append(f"| {b} | {by_band[b]['pass']} | {by_band[b]['fail']} |")
    lines.append("")
    lines.append("## Summary by kind")
    lines.append("")
    lines.append("| Kind | Pass | Fail |")
    lines.append("|------|------|------|")
    for k, v in sorted(by_kind.items()):
        lines.append(f"| {k} | {v['pass']} | {v['fail']} |")
    lines.append("")
    lines.append(f"Duplicate prompts: **{dup_prompts}**")
    lines.append("")
    total_fail = sum(v["fail"] for v in by_band.values())
    if total_fail == 0 and dup_prompts == 0:
        lines.append("## Result")
        lines.append("")
        lines.append("**ALL PUZZLES PASSED.** Every logic puzzle has exactly one solution under an independent solver; every riddle has a non-empty intended answer present in its accept set.")
    else:
        lines.append("## Failures")
        lines.append("")
        for item in failed:
            lines.append(f"- #{item[0]} ({item[1]} / {item[2]}): {item[3]}")
    lines.append("")
    lines.append("## Method")
    lines.append("")
    lines.append("- **Riddles:** independent of the wording generator; checks answer normalization and membership in the accept list.")
    lines.append("- **Logic (who_drink, order_arrival, room_item, caesar, anagram, sequence):** re-solved from stored constraints/meta using `logic_gen.SOLVERS`, which enumerates or decodes without trusting the stored answer field until the final comparison.")
    lines.append("")
    open(OUT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"wrote {OUT}; fails={total_fail}; dups={dup_prompts}")
    if total_fail or dup_prompts:
        sys.exit(1)


if __name__ == "__main__":
    main()
