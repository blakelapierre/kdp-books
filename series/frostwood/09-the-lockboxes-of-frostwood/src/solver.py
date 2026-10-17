"""Independent depth-first solver for Frostwood lockbox (crack-the-code) puzzles.
Written separately from gen.py: it never enumerates the full code space, and scores
each guess with set arithmetic rather than gen.py's per-position loop.
solve(length, clues) -> (list_of_solutions, nodes_visited)
Each clue is (guess_string, right_place, wrong_place). All digits in a code are different."""

def score(code, guess):
    right = sum(1 for c, g in zip(code, guess) if c == g)
    common = len(set(code) & set(guess))
    return right, common - right

def solve(length, clues, limit=10):
    sols, nodes = [], 0
    clues = [(g, a, b) for g, a, b in clues]
    def ok(partial):
        r = length - len(partial)
        for g, a, b in clues:
            ac = sum(1 for i, d in enumerate(partial) if g[i] == d)
            bc = sum(1 for i, d in enumerate(partial) if d in g and g[i] != d)
            if ac > a or bc > b:
                return False
            if ac + r < a or bc + r < b or ac + bc + r < a + b:
                return False
        return True
    def dfs(partial):
        nonlocal nodes
        nodes += 1
        if len(partial) == length:
            if all(score(partial, g) == (a, b) for g, a, b in clues):
                sols.append(partial)
            return
        for d in "0123456789":
            if d in partial:
                continue
            p = partial + d
            if ok(p):
                dfs(p)
                if len(sols) >= limit:
                    return
    dfs("")
    return sols, nodes
