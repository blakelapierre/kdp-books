"""Case 12, The Stopped Clock: BLACK-AND-WHITE ink with the simple v1 peg-doll characters, SIMPLE ANIMATIONS (anim.py),
mid-screen question bar (Case 7+ layout), clue notebook and a "next case" end card.
Times are ORIGINAL narration times (timing-case-12.json, whole-file whisper alignment). render.py adds the hook shift
and the countdown splice. Art: art_case12.py -> work/art-12/ (bwkit). Part sprites use part_open (no frame2).
Opening: HOOK_STYLE="calendar" (render.py): tear-off desk calendar (MON, TUE, WED tear away to THU) beside the title,
borderless hero of the stopped wall clock above the caddy shelf, three equal suspect cards, ONE TIME IS WRONG stamp.
Unlike Case 10 (wet-paint sign) and Case 11 (tent card).
Fairness: Demelza, Hedley and Mr Prowse share pose, size and neutral faces until the solution; only the confession
shows Mr Prowse sheepish. KEEP_ASPECT: crops match the view."""
NUM, NAME = 12, "The Stopped Clock"
STYLE = "bw"
SLUG = "standalone-03-tidewhistle-case-12-the-stopped-clock"
AUDIO = "standalone-03-tidewhistle-14-case-12-the-stopped-clock.mp3"
TIMING = "timing-case-12.json"; CLUES = "clues/case-12.json"; ART = "work/art-12"; HOOK_WAV = "assets/hooks/hook-12.wav"
QUESTION = "How does Agnes know Mr Prowse is not telling the truth?"
HOOK_LINES = ["Who's lying", "about the time?"]; HOOK_EMOJI = "\u23F0"   # alarm clock (greyed in B&W)
HOOK_SAY = ("A silver tea caddy has gone, the tea-room clock has stopped, and the milkman is very sure of his times. "
            "Is he?")
HOOK_STYLE = "calendar"
HOOK_STAMP = "ONE TIME IS WRONG"
HOOK_LABEL = "3 visitors \u00b7 1 silver caddy \u00b7 1 stopped clock"
HOOK_FOCUS = ((0.45, 0.48, 1.0), (0.4, 0.42, 1.2))
LINEUP_PANELS = 3
SHOW_QBAR = True
KEEP_ASPECT = True
NEXT_CARD = True
TRIM = 0.45
CUT, EXTRA = 117.55, 7.0         # after "...the solution follows." (ends ~117.33); "The Solution." ~121.83
NARR_END = 117.33
AUDIO_END = 174.6                # last word ends ~173.8; MP3 is ~176.6 s
NO_CAP = {0, 1, 11, 14}          # titles, question card, "The Solution."

SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=5.0),
    # the old clock clicks and stops at ten to nine; clockmaker not until Friday
    dict(k="art", img="clock", t0=5.0, t1=24.7, a=(0.3, 0.42, 1.3), b=(0.52, 0.45, 1.02)),
    # "tell the time by your stomachs"
    dict(k="art", img="laugh", t0=24.7, t1=30.8, a=(0.5, 0.55, 1.05), b=(0.52, 0.55, 1.18)),
    # the caddy shelf: silver acorn dusted at 3:30, gone at 4:30
    dict(k="art", img="shelf", t0=30.8, t1=47.7, a=(0.6, 0.45, 1.1), b=(0.6, 0.42, 1.4)),
    dict(k="pan", t0=47.7, t1=82.8, keys=[
        (47.7, 0, 1.15), (63.6, 0, 1.26),
        (64.3, 1, 1.15), (77.6, 1, 1.26),
        (78.3, 2, 1.15), (82.8, 2, 1.26),
    ]),
    # Mr Prowse: "your clock said a quarter past three"
    dict(k="art", img="prowse", t0=82.8, t1=98.9, a=(0.45, 0.45, 1.05), b=(0.5, 0.4, 1.22)),
    # Agnes looks up: ten to nine, as all week
    dict(k="art", img="look", t0=98.9, t1=104.4, a=(0.34, 0.45, 1.15), b=(0.3, 0.4, 1.45)),
    dict(k="ask", t0=104.4, t1=121.6),
    dict(k="soltitle", t0=121.6, t1=123.8),
    dict(k="art", img="board", t0=123.8, t1=145.2, a=(0.5, 0.5, 1.05), b=(0.45, 0.48, 1.25)),
    dict(k="art", img="board", t0=145.2, t1=156.0, a=(0.45, 0.48, 1.25), b=(0.5, 0.5, 1.0)),
    # confession; the caddy moves to a higher shelf
    dict(k="art", img="confess", t0=156.0, t1=174.4, a=(0.45, 0.48, 1.05), b=(0.55, 0.42, 1.2)),
    dict(k="end", t0=174.4, t1=None),
]
SHORTS = dict(tag="", p1_end=111.7, recap=(104.6, 111.4), card_t=111.2,
              suspects="Demelza, Hedley, or Mr Prowse?")

def _gull(area=(18, 250, 494, 370), n=2, seed=3):
    return [dict(kind="fly", part="gull", area=area, n=n, speed=(12, 22), flap=2.2, size=(0.5, 0.85), seed=seed)]

def _pop(part, t, fade=0.3, s0=1.25, until=None):
    return dict(kind="sprite", part=part, show=(t, until), fade=fade, keys=[(t, dict(s=s0)), (t + 0.25, dict(s=1.0))], pivot="centre")

_SUS = ["s0", "s1", "s2"]
ANIM = {
    "hook": dict(art="hook", layers=[]),
    "cast": dict(art="cast", layers=[dict(kind="sprite", part=p, idle=True, blink=True) for p in _SUS]),
    "clock": dict(art="clock", layers=[_pop("click", 12.3, until=16.0), _pop("friday", 19.1)]),
    "laugh": dict(art="laugh", layers=[
        dict(kind="sprite", part="agnes", idle=True, blink=True, talk=dict(seg=3, quotes=True)),
        dict(kind="sprite", part="g1", idle=True, blink=True, swaps=[(29.0, "smile", 3.0)]),
        dict(kind="sprite", part="g2", idle=True, blink=True, swaps=[(29.1, "smile", 3.0)]),
    ]),
    "shelf": dict(art="shelf", layers=[
        dict(kind="sprite", part="acorn", show=(None, 46.3), fade=0.45),
        _pop("t1", 41.2), _pop("t2", 44.4),
        dict(kind="sprite", part="gone", show=(46.4, None), fade=0.4),
    ]),
    "lineup": dict(art="lineup", layers=[
        *[dict(kind="sprite", part=p, idle=True, blink=True, nods=[t]) for p, t in zip(_SUS, (52.2, 65.4, 79.1))],
        dict(kind="sprite", part="quill", idle=True, blink=True, nods=[61.0]),
        *_gull(area=(30, 280, 480, 370), n=2, seed=4),
    ]),
    "prowse": dict(art="prowse", layers=[
        dict(kind="sprite", part="prowse", idle=True, blink=True, talk=dict(seg=9, quotes=True)),
        _pop("bubble", 92.9),
    ]),
    "look": dict(art="look", layers=[dict(kind="sprite", part="agnes", idle=True, blink=True, nods=[101.6])]),
    "board": dict(art="board", layers=[_pop("bub", 130.7), _pop("x", 136.0, fade=0.35), _pop("made", 140.2)]),
    "confess": dict(art="confess", layers=[
        dict(kind="sprite", part="prowse", idle=True, blink=True, swaps=[(0.0, "sheepish", 0.01)]),
        dict(kind="sprite", part="agnes", idle=True, blink=True, nods=[167.7]),
        _pop("high", 173.1),
    ]),
}
