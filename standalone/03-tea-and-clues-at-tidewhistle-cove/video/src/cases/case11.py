"""Case 11, The Window Table: BLACK-AND-WHITE ink with the simple v1 peg-doll characters, SIMPLE ANIMATIONS (anim.py),
mid-screen question bar (Case 7+ layout), clue notebook and a "next case" end card.
Times are ORIGINAL narration times (timing-case-11.json, whole-file whisper alignment; seg 6 word times re-spread by
timing_sanity.py where ASR lost the stretch). render.py adds the hook shift and the countdown splice.
Art: art_case11.py -> work/art-11/ (bwkit). Part sprites use part_open (no frame2).
Opening: HOOK_STYLE="placecard" (render.py): a folded RESERVED tent-card title that flips up, a borderless hero of the
four numbered tables and the empty windowsill, four numbered seat chips with a hopping "?" ring that never settles,
four equal framed suspect cards, ONE SEAT HIDES IT stamp. Unlike Case 9 (compass) and Case 10 (wet-paint sign).
Fairness: Mr Spargo, Loveday, Captain Quill and Wenna share pose, size and neutral faces until the solution; the
lineup has no table numbers; only the confession shows the captain sheepish. KEEP_ASPECT: crops match the view."""
NUM, NAME = 11, "The Window Table"
STYLE = "bw"
SLUG = "standalone-03-tidewhistle-case-11-the-window-table"
AUDIO = "standalone-03-tidewhistle-13-case-11-the-window-table.mp3"
TIMING = "timing-case-11.json"; CLUES = "clues/case-11.json"; ART = "work/art-11"; HOOK_WAV = "assets/hooks/hook-11.wav"
QUESTION = "Who sat at the window table and has the brooch?"
HOOK_LINES = ["Who sat by", "the window?"]; HOOK_EMOJI = "\U0001FA91"   # chair (greyed in B&W)
HOOK_SAY = ("A silver brooch has vanished from a tea-room windowsill. Four guests, four tables, and only a few "
            "muddled clues. Who sat by the window?")
HOOK_STYLE = "placecard"
HOOK_STAMP = "ONE SEAT HIDES IT"
HOOK_LABEL = "4 guests \u00b7 4 tables \u00b7 1 brooch"
HOOK_FOCUS = ((0.5, 0.6, 1.0), (0.62, 0.56, 1.18))   # drift toward the window end
LINEUP_PANELS = 4
SHOW_QBAR = True
KEEP_ASPECT = True
NEXT_CARD = True
TRIM = 0.45
CUT, EXTRA = 120.0, 7.0          # after "...the solution follows." (ends ~119.79); "The Solution." ~124.29
NARR_END = 119.79
AUDIO_END = 206.2                # last word ends ~205.4; MP3 is ~208.1 s
NO_CAP = {0, 1, 9, 12}           # titles, question card, "The Solution."

SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=4.9),
    # four tables in a row, door -> bay window; numbers pop on "first, second, third and fourth"
    dict(k="art", img="tables", t0=4.9, t1=21.4, a=(0.45, 0.6, 1.0), b=(0.5, 0.62, 1.1)),
    # Kerensa polishes the brooch, leaves it on the sill, hurries out; only the window table reaches the sill
    dict(k="art", img="sill", t0=21.4, t1=43.0, a=(0.6, 0.58, 1.08), b=(0.76, 0.55, 1.45)),
    # four guests, one per table (lineup, no numbers)
    dict(k="pan", t0=43.0, t1=52.4, keys=[
        (43.0, 0, 1.15), (45.0, 0, 1.24),
        (45.5, 1, 1.15), (47.3, 1, 1.24),
        (47.8, 2, 1.15), (49.6, 2, 1.24),
        (50.1, 3, 1.15), (52.4, 3, 1.24),
    ]),
    # ...the brooch was gone
    dict(k="art", img="sill", t0=52.4, t1=55.0, a=(0.86, 0.5, 2.0), b=(0.87, 0.5, 2.3)),
    # Agnes in the kitchen with the pasties; Pip serving
    dict(k="art", img="kitchen", t0=55.0, t1=67.1, a=(0.5, 0.45, 1.0), b=(0.55, 0.42, 1.18)),
    # Pip's four remembered clues
    dict(k="art", img="pip", t0=67.1, t1=83.7, a=(0.5, 0.5, 1.0), b=(0.5, 0.42, 1.1)),
    # Agnes's four squares + the recap of the clues
    dict(k="art", img="squares", t0=83.7, t1=107.5, a=(0.5, 0.58, 1.0), b=(0.5, 0.6, 1.08)),
    dict(k="ask", t0=107.5, t1=124.0),
    dict(k="soltitle", t0=124.0, t1=126.2),
    dict(k="art", img="board", t0=126.2, t1=135.2, a=(0.5, 0.62, 1.15), b=(0.5, 0.6, 1.1)),
    dict(k="art", img="board", t0=135.2, t1=168.3, a=(0.5, 0.36, 1.25), b=(0.5, 0.36, 1.2)),
    dict(k="art", img="board", t0=168.3, t1=189.2, a=(0.5, 0.52, 1.05), b=(0.5, 0.5, 1.0)),
    # the brooch in the captain's coat pocket
    dict(k="art", img="confess", t0=189.2, t1=206.0, a=(0.55, 0.58, 1.05), b=(0.62, 0.55, 1.2)),
    dict(k="end", t0=206.0, t1=None),
]
SHORTS = dict(tag="", p1_end=114.2, recap=(107.9, 113.9), card_t=113.7,
              suspects="Mr Spargo, Loveday, Captain Quill, or Wenna?")

def _gull(area=(18, 250, 494, 370), n=2, seed=3):
    return [dict(kind="fly", part="gull", area=area, n=n, speed=(12, 22), flap=2.2, size=(0.5, 0.85), seed=seed)]

def _pop(part, t, fade=0.3, s0=1.25, until=None):
    return dict(kind="sprite", part=part, show=(t, until), fade=fade, keys=[(t, dict(s=s0)), (t + 0.25, dict(s=1.0))], pivot="centre")

_SUS = ["s0", "s1", "s2", "s3"]
_BOARD = [("c3", 126.8), ("ring", 127.6),
          ("a2", 135.9), ("a0", 143.3), ("a1", 145.7), ("a3", 148.3), ("xa", 153.8),
          ("b2", 155.0), ("b1", 155.3), ("b0", 157.0), ("b3", 160.2), ("xb", 164.4),
          ("c1", 168.7), ("c2", 178.9), ("c0", 186.1)]
ANIM = {
    "hook": dict(art="hook", layers=[*_gull(area=(170, 290, 400, 370), n=2, seed=1)]),
    "cast": dict(art="cast", layers=[dict(kind="sprite", part=p, idle=True, blink=True) for p in _SUS]),
    "tables": dict(art="tables", layers=[_pop(f"n{i}", t) for i, t in enumerate((13.6, 14.4, 15.1, 15.9))]),
    "sill": dict(art="sill", layers=[
        dict(kind="sprite", part="kerensa", idle=True, blink=True, show=(None, 31.9), fade=0.5),
        dict(kind="sprite", part="brooch", show=(29.1, 52.8), fade=0.4),
        _pop("reach", 35.4, until=43.0),
        dict(kind="sprite", part="gone", show=(52.9, None), fade=0.4),
    ]),
    "lineup": dict(art="lineup", layers=[
        dict(kind="sprite", part=p, idle=True, blink=True, nods=[t]) for p, t in zip(_SUS, (43.6, 45.8, 48.1, 50.4))]),
    "kitchen": dict(art="kitchen", layers=[
        dict(kind="sprite", part="agnes", idle=True, blink=True, nods=[57.8]),
        dict(kind="sprite", part="pip", idle=True, blink=True, nods=[59.8]),
        dict(kind="glint", part="steam", area=(80, 140, 200, 170), n=3, life=2.0, drift=6.0, seed=2),
    ]),
    "pip": dict(art="pip", layers=[
        dict(kind="sprite", part="pip", idle=True, blink=True, talk=dict(seg=6, quotes=True)),
        dict(kind="sprite", part="agnes", idle=True, blink=True, nods=[76.0]),
        *[_pop(f"c{i}", t) for i, t in enumerate((69.2, 72.2, 74.3, 77.9))],
    ]),
    "squares": dict(art="squares", layers=[
        *[_pop(f"r{i}", t) for i, t in enumerate((92.2, 94.8, 97.0, 99.3))],
        _pop("names", 102.4),
    ]),
    "board": dict(art="board", layers=[_pop(p, t, fade=0.3) for p, t in _BOARD]),
    "confess": dict(art="confess", layers=[
        dict(kind="sprite", part="quill", idle=True, blink=True, swaps=[(0.0, "sheepish", 0.01)]),
        dict(kind="sprite", part="kerensa", idle=True, blink=True, nods=[203.0]),
        _pop("pocket", 189.2),
        dict(kind="sprite", part="wind", show=(192.3, 196.5), fade=0.4),
        _pop("teapot", 204.5),
    ]),
}
