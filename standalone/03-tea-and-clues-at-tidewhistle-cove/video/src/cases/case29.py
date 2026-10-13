"""Case 29, The Sugar Bowl: BLACK-AND-WHITE ink with the simple v1 peg-doll characters, SIMPLE ANIMATIONS (anim.py),
mid-screen question bar (Case 7+ layout), clue notebook and a "next case" end card.
Times are ORIGINAL narration times (timing-case-29.json; seg 15 word times re-spread evenly, ASR had collapsed them).
Art: art_case29.py -> work/art-29/ (bwkit). Part sprites use part_open (no frame2).
Opening: HOOK_STYLE="sugarlumps" (render.py): three lumps hop out of a 12-lump sugar bowl (counter 12 -> 9), then a cup of
dark, milkless tea slides in ("black?"); borderless study hero; three equal suspect cards; READ THE TEA TRAY stamp.
Unlike Case 28 (cardflip) and Case 27 (foghorn).
Fairness: Quill, Loveday and Bolitho share pose, size and neutral faces; equal "how they take it" tags (Agnes's words).
Board marks only after "The Solution". Only the confession shows Bolitho sheepish. KEEP_ASPECT."""
NUM, NAME = 29, "The Sugar Bowl"
STYLE = "bw"
SLUG = "standalone-03-tidewhistle-case-29-the-sugar-bowl"
AUDIO = "standalone-03-tidewhistle-31-case-29-the-sugar-bowl.mp3"
TIMING = "timing-case-29.json"; CLUES = "clues/case-29.json"; ART = "work/art-29"; HOOK_WAV = "assets/hooks/hook-29.wav"
QUESTION = "Who took the book of sea shanties?"
HOOK_LINES = ["Who drank", "this tea?"]; HOOK_EMOJI = "\U0001FAD6"   # teapot (greyed in B&W)
HOOK_SAY = ("A treasured book of sea shanties vanishes from the vicar's study, and the tea tray tells all. Can you read it?")
HOOK_STYLE = "sugarlumps"
HOOK_STAMP = "READ THE TEA TRAY"
HOOK_LABEL = "3 visitors \u00b7 12 lumps \u00b7 1 cup"
HOOK_FOCUS = ((0.3, 0.5, 1.0), (0.3, 0.45, 1.3))
LINEUP_PANELS = 3
SHOW_QBAR = True
KEEP_ASPECT = True
NEXT_CARD = True
TRIM = 0.45
CUT, EXTRA = 110.45, 7.0         # after "...the solution follows." (ends ~110.3); "The Solution." ~115.1
NARR_END = 110.3
AUDIO_END = 174.2
NO_CAP = {0, 1, 9, 12}           # titles, question card, "The Solution."

SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=4.6),
    dict(k="art", img="tea", t0=4.6, t1=14.6, a=(0.5, 0.5, 1.0), b=(0.5, 0.45, 1.1)),
    dict(k="art", img="study", t0=14.6, t1=75.0, a=(0.5, 0.5, 1.0), b=(0.42, 0.45, 1.1)),
    dict(k="pan", t0=75.0, t1=99.2, keys=[
        (75.0, 0, 1.12), (86.6, 0, 1.22),
        (86.7, 1, 1.12), (90.5, 1, 1.18),
        (90.6, 2, 1.12), (99.2, 2, 1.22),
    ]),
    dict(k="ask", t0=99.2, t1=114.9),
    dict(k="soltitle", t0=114.9, t1=117.1),
    dict(k="art", img="board", t0=117.1, t1=152.3, a=(0.5, 0.5, 1.0), b=(0.5, 0.5, 1.06)),
    dict(k="art", img="confess", t0=152.3, t1=173.9, a=(0.45, 0.5, 1.05), b=(0.55, 0.5, 1.15)),
    dict(k="end", t0=173.9, t1=None),
]
SHORTS = dict(tag="", p1_end=104.5, recap=(99.2, 104.2), card_t=104.0,
              suspects="Captain Quill, Loveday, or Mr Bolitho?")

def _pop(part, t, fade=0.3, s0=1.25, until=None):
    return dict(kind="sprite", part=part, show=(t, until), fade=fade, keys=[(t, dict(s=s0)), (t + 0.25, dict(s=1.0))], pivot="centre")

_SUS = ["s0", "s1", "s2"]
ANIM = {
    "hook": dict(art="hook", layers=[]),
    "cast": dict(art="cast", layers=[dict(kind="sprite", part=p, idle=True, blink=True) for p in _SUS]),
    "tea": dict(art="tea", layers=[dict(kind="sprite", part="agnes", idle=True, blink=True), _pop("know", 9.78)]),
    "study": dict(art="study", layers=[
        dict(kind="sprite", part="book", show=(None, 53.0), fade=0.3), _pop("tray2", 32.08, until=53.9), _pop("gone", 53.2),
        _pop("tray3", 54.0), _pop("dark", 57.04), _pop("nine", 62.96), _pop("vicar", 65.6)]),
    "lineup": dict(art="lineup", layers=[
        *[dict(kind="sprite", part=p, idle=True, blink=True) for p in _SUS],
        _pop("p0", 85.72), _pop("p1", 89.44), _pop("p2", 94.66)]),
    "board": dict(art="board", layers=[
        _pop("cup", 130.8), _pop("black", 134.4), _pop("r0", 140.3), _pop("r1", 142.6), _pop("r2", 144.8), _pop("r3", 147.8), _pop("ring", 150.0)]),
    "confess": dict(art="confess", layers=[
        dict(kind="sprite", part="bol", idle=True, blink=True, swaps=[(0.0, "sheepish", 0.01)]),
        _pop("sing", 159.07), _pop("ret", 166.86)]),
}
