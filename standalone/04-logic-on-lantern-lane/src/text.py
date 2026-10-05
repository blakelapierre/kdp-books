"""Turns structured clues into plain English sentences, and formats values for clues and grids."""
import re

WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]
ORD = ["", "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth"]
ORD_S = ["", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th"]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
NUMWORDS = {"two": 2, "three": 3, "four": 4, "five": 5}


def clock(m):
    h, mm = divmod(int(m), 60)
    h = h % 12 or 12
    return f"{h}:{mm:02d}"


def money(v):
    return f"${v:.2f}" if abs(v - round(v)) > 1e-9 else f"${int(round(v))}"


def fmt_value(cat, v, label=False):
    """Text for one value of an ordered category (v is the raw number)."""
    k = cat["kind"]
    if k == "time":
        return clock(v)
    if k == "money":
        return money(v)
    if k == "ordinal":
        return ORD_S[v] if label else ORD[v]
    if k == "day":
        return DAYS[v][:3] if label else DAYS[v]
    if k == "row":
        return str(v)
    t = cat["lf"] if label else (cat["vf1"] if (v == 1 and cat.get("vf1")) else cat["vf"])
    return t.format(v=f"{v:,}")


def fmt_diff(cat, steps):
    """Difference of `steps` positions in an ordered category, as words."""
    vals = cat.get("raw") or cat["values"]
    d = round(vals[1] - vals[0], 2) * steps
    k = cat["kind"]
    if k == "time":
        d = int(round(d))
        return {30: "half an hour", 60: "an hour", 90: "an hour and a half", 120: "two hours"}.get(d, f"{d} minutes")
    if k == "money":
        if d < 1:
            return f"{int(round(d * 100))} cents"
        return money(d)
    d = int(round(d))
    sing, plur = cat["du"] if cat.get("du") else ("", "")
    num = WORDS[d] if d < len(WORDS) else f"{d:,}"
    if not sing:
        return num
    if sing == "lb":
        return f"{d} lb"
    return f"{num} {sing if d == 1 else plur}"


def diff_num(cat, steps):
    vals = cat.get("raw") or cat["values"]
    d = int(round((vals[1] - vals[0]) * steps))
    return WORDS[d] if d < len(WORDS) else f"{d:,}"


class Phraser:
    def __init__(s, puzzle):
        s.p = puzzle
        s.who = puzzle["who"]

    def vtext(s, c, i):
        cat = s.p["cats"][c]
        if cat["ordered"]:
            return fmt_value(cat, cat["raw"][i])
        return cat["items"][i]

    def np(s, it):
        c, i = it
        if c == 0:
            return s.vtext(0, i)
        return s.p["cats"][c]["np"].format(who=s.who, v=s.vtext(c, i))

    def _pred_parts(s, it):
        c, i = it
        if c == 0:
            t = s.p["keytense"]
            v = s.vtext(0, i)
            return f"{t} {v}", f"{t} not {v}"
        tmpl = s.p["cats"][c]["pred"].format(who=s.who, v=s.vtext(c, i))
        present = tmpl.startswith("~")
        tmpl = tmpl.lstrip("~")
        m = re.match(r"(\S+)/(\S+)(.*)$", tmpl)
        if m:
            past, base, rest = m.groups()
            return past + rest, ("does not " if present else "did not ") + base + rest
        w = tmpl.split(" ", 1)
        first, rest = w[0], (w[1] if len(w) > 1 else "")
        if first in ("was", "is", "were"):
            return tmpl, f"{first} not {rest}"
        if first == "has":
            nxt = rest.split(" ", 1)[0]
            if nxt in ("the", "a") or re.match(r"^[\d,]+$", nxt):
                return tmpl, f"does not have {rest}"
            return tmpl, f"has not {rest}"
        raise ValueError(f"cannot negate: {tmpl}")

    def pred(s, it):
        return s._pred_parts(it)[0]

    def neg(s, it):
        return s._pred_parts(it)[1]

    def clue(s, cl, flip=False):
        t = cl["t"]
        a, b = tuple(cl["a"]), tuple(cl["b"])
        if t in ("pos", "neg"):
            if b[0] == 0 or (flip and a[0] != 0):
                a, b = b, a
            body = (s.pred if t == "pos" else s.neg)(b)
            return cap(f"{s.np(a)} {body}.")
        if t == "lt":
            cat = s.p["cats"][cl["o"]]
            d = cl.get("d")
            if flip:
                a, b = b, a
                tm = cat["dgt"] if d else cat["gt"]
            else:
                tm = cat["dlt"] if d else cat["lt"]
            if d:
                tm = tm.replace("{d}", fmt_diff(cat, d)).replace("{dn}", diff_num(cat, d))
                if cat.get("du") and diff_num(cat, d) == "one":
                    sing, plur = cat["du"]
                    tm = re.sub(r"\bone (fewer |more )?" + re.escape(plur) + r"\b", lambda m: "one " + (m.group(1) or "") + sing, tm)
            return cap(f"{s.np(a)} {tm} {s.np(b)}.")
        if t == "either":
            c = tuple(cl["c"])
            if flip:
                b, c = c, b
            return cap(f"{s.np(a)} either {s.pred(b)} or {s.pred(c)}.")
        if t == "neither":
            c = tuple(cl["c"])
            if flip:
                a, b = b, a
            return cap(f"Neither {s.np(a)} nor {s.np(b)} {s.pred(c)}.")
        if t == "pair":
            c, d = tuple(cl["c"]), tuple(cl["d"])
            if flip:
                c, d = d, c
            return cap(f"Of {s.np(a)} and {s.np(b)}, one {s.pred(c)} and the other {s.pred(d)}.")
        raise ValueError(t)

    def fact(s, x, y, true=True):
        cl = {"t": "pos" if true else "neg", "a": list(x), "b": list(y)}
        return s.clue(cl)


def cap(t):
    return t[0].upper() + t[1:]
