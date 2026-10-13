"""Case 23, The Odd Glove: BLACK-AND-WHITE ink with the simple v1 peg-doll characters, SIMPLE ANIMATIONS (anim.py),
mid-screen question bar (Case 7+ layout), clue notebook and a "next case" end card.
Times are ORIGINAL narration times (timing-case-23.json). render.py adds the hook shift and the countdown splice.
Art: art_case23.py -> work/art-23/ (bwkit). Part sprites use part_open (no frame2).
Opening: HOOK_STYLE="glovepair" (render.py): a navy LEFT glove with white anchors slides in beside the title while a dashed
empty RIGHT-glove outline pulses with "?" (the pair is never completed in the open), borderless lane hero, three equal
suspect cards, WHOSE GLOVE? stamp. Unlike Case 22 (toggle) and Case 21 (coinflip).
Fairness: Kerensa, Mr Fenwick and Mr Lanyon share pose, size and neutral faces and each gets the same-size hand tag when
narrated. The "a pair!" and ring marks appear only after "The Solution". Only the confession shows Lanyon sheepish. KEEP_ASPECT."""
NUM, NAME = 23, "The Odd Glove"
STYLE = "bw"
SLUG = "standalone-03-tidewhistle-case-23-the-odd-glove"
AUDIO = "standalone-03-tidewhistle-25-case-23-the-odd-glove.mp3"
TIMING = "timing-case-23.json"; CLUES = "clues/case-23.json"; ART = "work/art-23"; HOOK_WAV = "assets/hooks/hook-23.wav"
QUESTION = "Who took the orchid?"
HOOK_LINES = ["Whose glove", "is it?"]; HOOK_EMOJI = "\U0001F9E4"   # gloves (greyed in B&W)
HOOK_SAY = ("A rare orchid has vanished on a bitter, windy night, and one knitted glove was left behind. "
            "Whose hand does it fit?")
HOOK_STYLE = "glovepair"
HOOK_STAMP = "WHOSE GLOVE?"
HOOK_LABEL = "3 people \u00b7 1 odd glove"
HOOK_FOCUS = ((0.3, 0.5, 1.0), (0.32, 0.45, 1.3))
LINEUP_PANELS = 3
SHOW_QBAR = True
KEEP_ASPECT = True
NEXT_CARD = True
TRIM = 0.45
CUT, EXTRA = 106.45, 7.0         # after "...the solution follows." (ends ~106.3); "The Solution." ~111.36
NARR_END = 106.3
AUDIO_END = 166.4                # last word ends ~166.1
NO_CAP = {0, 1, 10, 13}          # titles, question card, "The Solution."

SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=4.9),
    # a bitter, windy evening in the lane
    dict(k="art", img="lane", t0=4.9, t1=13.0, a=(0.5, 0.5, 1.0), b=(0.5, 0.55, 1.12)),
    # Morwenna's rare white orchid on the back windowsill; window open, orchid gone
    dict(k="art", img="sill", t0=13.0, t1=31.9, a=(0.5, 0.5, 1.0), b=(0.5, 0.55, 1.15)),
    # under the window: a single navy RIGHT-hand glove with white anchors
    dict(k="art", img="cobble", t0=31.9, t1=43.2, a=(0.45, 0.4, 1.0), b=(0.6, 0.35, 1.18)),
    # Agnes passing; three people nearby
    dict(k="art", img="lane", t0=43.2, t1=52.5, a=(0.5, 0.5, 1.05), b=(0.45, 0.45, 1.15)),
    dict(k="pan", t0=52.5, t1=95.9, keys=[
        (52.5, 0, 1.12), (62.3, 0, 1.22),
        (62.4, 1, 1.12), (74.4, 1, 1.2),
        (74.5, 2, 1.12), (95.9, 2, 1.24),
    ]),
    dict(k="ask", t0=95.9, t1=111.2),
    dict(k="soltitle", t0=111.2, t1=113.0),
    dict(k="art", img="board", t0=113.0, t1=143.8, a=(0.5, 0.5, 1.0), b=(0.5, 0.5, 1.06)),
    dict(k="art", img="confess", t0=143.8, t1=166.2, a=(0.45, 0.5, 1.05), b=(0.55, 0.5, 1.2)),
    dict(k="end", t0=166.2, t1=None),
]
SHORTS = dict(tag="", p1_end=101.2, recap=(95.9, 100.9), card_t=100.7,
              suspects="Kerensa, Mr Fenwick, or Mr Lanyon?")

def _pop(part, t, fade=0.3, s0=1.25, until=None):
    return dict(kind="sprite", part=part, show=(t, until), fade=fade, keys=[(t, dict(s=s0)), (t + 0.25, dict(s=1.0))], pivot="centre")

_SUS = ["s0", "s1", "s2"]
ANIM = {
    "hook": dict(art="hook", layers=[]),
    "cast": dict(art="cast", layers=[dict(kind="sprite", part=p, idle=True, blink=True) for p in _SUS]),
    "lane": dict(art="lane", layers=[
        _pop("wind", 6.2, until=13.0),
        dict(kind="sprite", part="agnes", idle=True, blink=True, show=(43.3, None), fade=0.3),
        dict(kind="sprite", part="morwenna", idle=True, blink=True, show=(46.1, None), fade=0.3),
        _pop("three", 50.54)]),
    "sill": dict(art="sill", layers=[
        dict(kind="sprite", part="shut", show=(None, 27.9), fade=0.2),
        dict(kind="sprite", part="orchid", show=(None, 30.6), fade=0.4),
        dict(kind="sprite", part="morwenna", idle=True, blink=True),
        _pop("bloom", 19.96, until=27.0), _pop("open", 27.96), _pop("gone", 30.68)]),
    "cobble": dict(art="cobble", layers=[_pop("glove", 35.28), _pop("zoom", 38.86), _pop("anch", 41.06)]),
    "lineup": dict(art="lineup", layers=[
        *[dict(kind="sprite", part=p, idle=True, blink=True, talk=w) for p, w in zip(_SUS, ([], [(70.04, 73.4)], [(89.64, 95.0)]))],
        _pop("gk", 56.22), _pop("p0", 57.9),
        _pop("gf", 67.78), _pop("p1", 68.4),
        _pop("gl", 81.58), _pop("pocket", 86.06), _pop("p2", 86.9), _pop("lz", 89.64),
    ]),
    "board": dict(art="board", layers=[
        _pop("pair", 124.22), _pop("r0", 133.42), _pop("r1", 137.96), _pop("ring", 141.24)]),
    "confess": dict(art="confess", layers=[
        dict(kind="sprite", part="lanyon", idle=True, blink=True, swaps=[(0.0, "sheepish", 0.01)]),
        _pop("box", 152.42), _pop("miles", 158.46), _pop("cut", 162.04),
    ]),
}
