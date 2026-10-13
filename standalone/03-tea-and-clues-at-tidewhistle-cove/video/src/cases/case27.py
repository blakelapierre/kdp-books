"""Case 27, The Silent Foghorn: BLACK-AND-WHITE ink with the simple v1 peg-doll characters, SIMPLE ANIMATIONS (anim.py),
mid-screen question bar (Case 7+ layout), clue notebook and a "next case" end card.
Times are ORIGINAL narration times (timing-case-27.json). render.py adds the hook shift and the countdown splice.
Art: art_case27.py -> work/art-27/ (bwkit). Part sprites use part_open (no frame2).
Opening: HOOK_STYLE="foghorn" (render.py): a foghorn sends out rings of sound with "BOOM", then the sound is struck out
and replaced by a quiet "…"; borderless starry harbour hero; three equal suspect cards; FOGGY? stamp.
Unlike Case 26 (queueslots) and Case 25 (spooncount).
Fairness: Captain Quill, Tamsin and Mr Keast share pose, size and neutral faces; equal tags. The FOG OR CLEAR? comparison
and the X appear only after "The Solution". Only the confession shows Keast red-faced. KEEP_ASPECT."""
NUM, NAME = 27, "The Silent Foghorn"
STYLE = "bw"
SLUG = "standalone-03-tidewhistle-case-27-the-silent-foghorn"
AUDIO = "standalone-03-tidewhistle-29-case-27-the-silent-foghorn.mp3"
TIMING = "timing-case-27.json"; CLUES = "clues/case-27.json"; ART = "work/art-27"; HOOK_WAV = "assets/hooks/hook-27.wav"
QUESTION = "How does Agnes know Mr Keast's story is false?"
HOOK_LINES = ["What's wrong", "with his night?"]; HOOK_EMOJI = "\U0001F32B"   # fog (greyed in B&W)
HOOK_SAY = ("A brass barometer vanished from a yacht in the night, and one visitor's alibi is full of fog. Can you see through it?")
HOOK_STYLE = "foghorn"
HOOK_STAMP = "FOGGY?"
HOOK_LABEL = "3 people \u00b7 1 night \u00b7 1 foghorn"
HOOK_FOCUS = ((0.5, 0.5, 1.0), (0.55, 0.45, 1.3))
LINEUP_PANELS = 3
SHOW_QBAR = True
KEEP_ASPECT = True
NEXT_CARD = True
TRIM = 0.45
CUT, EXTRA = 102.75, 7.0         # after "...the solution follows." (ends ~102.6); "The Solution." ~107.2
NARR_END = 102.6
AUDIO_END = 165.0
NO_CAP = {0, 1, 8, 11}           # titles, question card, "The Solution."

SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=4.8),
    dict(k="art", img="horn", t0=4.8, t1=27.0, a=(0.5, 0.5, 1.0), b=(0.6, 0.5, 1.12)),
    dict(k="art", img="bed", t0=27.0, t1=43.5, a=(0.5, 0.5, 1.0), b=(0.5, 0.5, 1.08)),
    dict(k="art", img="bay", t0=43.5, t1=56.5, a=(0.5, 0.5, 1.0), b=(0.5, 0.45, 1.12)),
    dict(k="pan", t0=56.5, t1=90.8, keys=[
        (56.5, 0, 1.12), (64.5, 0, 1.22),
        (64.6, 1, 1.12), (70.3, 1, 1.2),
        (70.4, 2, 1.12), (90.8, 2, 1.24),
    ]),
    dict(k="ask", t0=90.8, t1=107.1),
    dict(k="soltitle", t0=107.1, t1=109.5),
    dict(k="art", img="board", t0=109.5, t1=149.7, a=(0.5, 0.5, 1.0), b=(0.5, 0.5, 1.06)),
    dict(k="art", img="confess", t0=149.7, t1=164.8, a=(0.5, 0.5, 1.05), b=(0.55, 0.5, 1.15)),
    dict(k="end", t0=164.8, t1=None),
]
SHORTS = dict(tag="", p1_end=96.1, recap=(90.8, 95.8), card_t=95.6,
              suspects="Captain Quill, Tamsin, or Mr Keast?")

def _pop(part, t, fade=0.3, s0=1.25, until=None):
    return dict(kind="sprite", part=part, show=(t, until), fade=fade, keys=[(t, dict(s=s0)), (t + 0.25, dict(s=1.0))], pivot="centre")

_SUS = ["s0", "s1", "s2"]
ANIM = {
    "hook": dict(art="hook", layers=[]),
    "cast": dict(art="cast", layers=[dict(kind="sprite", part=p, idle=True, blink=True) for p in _SUS]),
    "horn": dict(art="horn", layers=[
        _pop("fog", 9.84, until=18.3), _pop("boom", 14.94, until=18.3), _pop("houses", 19.14), _pop("cat", 26.0),
        dict(kind="fly", part="gull", area=(18, 220, 300, 360), n=2, speed=(12, 22), flap=2.2, size=(0.5, 0.85), seed=9)]),
    "bed": dict(art="bed", layers=[
        dict(kind="sprite", part="agnes", idle=True, blink=True), _pop("open", 32.62), _pop("lemon", 34.8),
        _pop("hours", 36.52), _pop("clear", 40.22), _pop("silent", 41.74)]),
    "bay": dict(art="bay", layers=[
        dict(kind="sprite", part="yacht", show=(None, 48.0), fade=0.3), dict(kind="sprite", part="nob", show=(48.0, None), fade=0.3),
        _pop("gone", 48.44), _pop("dinghy", 53.4)]),
    "lineup": dict(art="lineup", layers=[
        *[dict(kind="sprite", part=p, idle=True, blink=True, talk=w) for p, w in zip(_SUS, ([], [], [(76.96, 89.4)]))],
        _pop("p0", 61.32), _pop("p1", 68.24), _pop("p2", 74.94), _pop("said", 83.06),
    ]),
    "board": dict(art="board", layers=[
        _pop("keast", 113.08), _pop("agnes", 128.36), _pop("x", 132.42), _pop("r0", 142.2), _pop("r1", 144.48), _pop("ring", 147.6)]),
    "confess": dict(art="confess", layers=[
        dict(kind="sprite", part="keast", idle=True, blink=True, swaps=[(0.0, "sheepish", 0.01)]),
        _pop("case", 152.12), _pop("collect", 155.46), _pop("check", 163.48),
    ]),
}
