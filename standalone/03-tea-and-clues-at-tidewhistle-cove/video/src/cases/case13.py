"""Case 13, The Misspelled Note: BLACK-AND-WHITE ink with the simple v1 peg-doll characters, SIMPLE ANIMATIONS (anim.py),
mid-screen question bar (Case 7+ layout), clue notebook and a "next case" end card.
Times are ORIGINAL narration times (timing-case-13.json, whole-file whisper alignment). render.py adds the hook shift
and the countdown splice. Art: art_case13.py -> work/art-13/ (bwkit). Part sprites use part_open (no frame2).
Opening: HOOK_STYLE="redpen" (render.py): title handwritten on torn ruled notepaper, a red pen draws a wavy underline
and a margin "?", borderless hero of the empty office shelf with the folded note, three equal framed suspect cards,
ONE WORD GIVES IT AWAY stamp. Unlike Case 11 (tent card) and Case 12 (calendar).
Fairness: Tamsin, Jago and Hedley share pose, size and neutral faces until the solution; only the confession shows
Hedley sheepish. KEEP_ASPECT: crops match the view."""
NUM, NAME = 13, "The Misspelled Note"
STYLE = "bw"
SLUG = "standalone-03-tidewhistle-case-13-the-misspelled-note"
AUDIO = "standalone-03-tidewhistle-15-case-13-the-misspelled-note.mp3"
TIMING = "timing-case-13.json"; CLUES = "clues/case-13.json"; ART = "work/art-13"; HOOK_WAV = "assets/hooks/hook-13.wav"
QUESTION = "Who left the note and borrowed the ship in a bottle?"
HOOK_LINES = ["Who wrote", "the note?"]; HOOK_EMOJI = "\U0001F4DD"   # memo (greyed in B&W)
HOOK_SAY = ("Captain Quill's ship in a bottle has disappeared, and a friendly note was left in its place. One little "
            "word gives the writer away. Can you spot it?")
HOOK_STYLE = "redpen"
HOOK_STAMP = "ONE WORD GIVES IT AWAY"
HOOK_LABEL = "3 visitors \u00b7 1 empty shelf \u00b7 1 note"
HOOK_FOCUS = ((0.5, 0.5, 1.0), (0.52, 0.48, 1.25))
LINEUP_PANELS = 3
SHOW_QBAR = True
KEEP_ASPECT = True
NEXT_CARD = True
TRIM = 0.45
CUT, EXTRA = 107.75, 7.0         # after "...the solution follows." (ends ~107.52); "The Solution." ~112.02
NARR_END = 107.52
AUDIO_END = 170.6                # last word ends ~169.7; MP3 is ~172.5 s
NO_CAP = {0, 1, 10, 13}          # titles, question card, "The Solution."

SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=5.1),
    # Hedley's hand-painted sign: NO PARKING ON THE PEIR
    dict(k="art", img="sign", t0=5.1, t1=23.3, a=(0.5, 0.5, 1.0), b=(0.66, 0.6, 1.5)),
    # "I before E, Hedley." / "Looks right to me."
    dict(k="art", img="chat", t0=23.3, t1=31.6, a=(0.5, 0.55, 1.05), b=(0.5, 0.55, 1.15)),
    # the ship in a bottle on the office shelf ... empty, a folded note
    dict(k="art", img="office", t0=31.6, t1=49.4, a=(0.5, 0.45, 1.0), b=(0.53, 0.5, 1.5)),
    # the note: "Don't worry. Your ship will be back by the peir at sunset."
    dict(k="art", img="notec", t0=49.4, t1=57.6, a=(0.5, 0.5, 1.0), b=(0.48, 0.5, 1.15)),
    # the captain brings the note to the Kettle and Gull
    dict(k="art", img="kettle", t0=57.6, t1=63.1, a=(0.5, 0.55, 1.05), b=(0.5, 0.55, 1.15)),
    dict(k="pan", t0=63.1, t1=77.7, keys=[
        (63.1, 0, 1.15), (69.9, 0, 1.26),
        (70.3, 1, 1.15), (72.9, 1, 1.26),
        (73.3, 2, 1.15), (77.7, 2, 1.26),
    ]),
    # Tamsin's poster and Jago's chalkboard, both spelled correctly
    dict(k="art", img="spell", t0=77.7, t1=95.6, a=(0.3, 0.45, 1.3), b=(0.7, 0.45, 1.3)),
    dict(k="ask", t0=95.6, t1=111.8),
    dict(k="soltitle", t0=111.8, t1=114.0),
    dict(k="art", img="board", t0=114.0, t1=137.0, a=(0.5, 0.5, 1.0), b=(0.45, 0.5, 1.15)),
    # the bigger ship for the captain's birthday
    dict(k="art", img="confess", t0=137.0, t1=154.2, a=(0.45, 0.5, 1.05), b=(0.5, 0.48, 1.18)),
    # sunset: the ship is back; the birthday card ... "Down by the Peir"
    dict(k="art", img="sunset", t0=154.2, t1=170.4, a=(0.4, 0.5, 1.1), b=(0.66, 0.6, 1.3)),
    dict(k="end", t0=170.4, t1=None),
]
SHORTS = dict(tag="", p1_end=101.9, recap=(95.7, 101.6), card_t=101.4,
              suspects="Tamsin, Jago, or Hedley?")

def _gull(area=(18, 250, 494, 370), n=2, seed=3):
    return [dict(kind="fly", part="gull", area=area, n=n, speed=(12, 22), flap=2.2, size=(0.5, 0.85), seed=seed)]

def _pop(part, t, fade=0.3, s0=1.25, until=None):
    return dict(kind="sprite", part=part, show=(t, until), fade=fade, keys=[(t, dict(s=s0)), (t + 0.25, dict(s=1.0))], pivot="centre")

_SUS = ["s0", "s1", "s2"]
ANIM = {
    "hook": dict(art="hook", layers=[]),
    "cast": dict(art="cast", layers=[dict(kind="sprite", part=p, idle=True, blink=True) for p in _SUS]),
    "sign": dict(art="sign", layers=[_pop("ring", 16.2), _pop("tally", 21.5), *_gull(seed=2)]),
    "chat": dict(art="chat", layers=[
        dict(kind="sprite", part="agnes", idle=True, blink=True, talk=dict(seg=3, quotes=True)),
        dict(kind="sprite", part="hedley", idle=True, blink=True, talk=dict(seg=4, quotes=True)),
        *_gull(seed=3)]),
    "office": dict(art="office", layers=[
        dict(kind="sprite", part="ship", show=(None, 45.0), fade=0.45),
        dict(kind="sprite", part="note", show=(47.4, None), fade=0.4),
    ]),
    "notec": dict(art="notec", layers=[_pop("ring", 54.6)]),
    "kettle": dict(art="kettle", layers=[
        dict(kind="sprite", part="quill", idle=True, blink=True, nods=[58.4]),
        dict(kind="sprite", part="agnes", idle=True, blink=True, nods=[61.3]),
    ]),
    "lineup": dict(art="lineup", layers=[
        dict(kind="sprite", part=p, idle=True, blink=True, nods=[t]) for p, t in zip(_SUS, (67.8, 70.6, 73.6))]),
    "spell": dict(art="spell", layers=[_pop("poster", 79.5), _pop("ok1", 85.5), _pop("chalk", 87.7), _pop("ok2", 93.5)]),
    "board": dict(art="board", layers=[_pop("match", 122.1), _pop("tk1", 131.5), _pop("tk2", 132.7)]),
    "confess": dict(art="confess", layers=[
        dict(kind="sprite", part="hedley", idle=True, blink=True, swaps=[(0.0, "sheepish", 0.01)]),
        dict(kind="sprite", part="quill", idle=True, blink=True, nods=[152.4]),
        _pop("bigship", 145.2),
    ]),
    "sunset": dict(art="sunset", layers=[_pop("ship", 155.6), _pop("card", 166.9), *_gull(seed=6)]),
}
