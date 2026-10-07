"""Case 18, The Moonlit Walk: BLACK-AND-WHITE ink with the simple v1 peg-doll characters, SIMPLE ANIMATIONS (anim.py),
mid-screen question bar (Case 7+ layout), clue notebook and a "next case" end card.
Times are ORIGINAL narration times (timing-case-18.json). render.py adds the hook shift and the countdown splice.
Art: art_case18.py -> work/art-18/ (bwkit). Part sprites use part_open (no frame2).
Opening: HOOK_STYLE="starfield" (render.py): the title letters revealed as stars twinkle on across a hatched night band,
a shooting star streaks through, borderless clifftop-tent hero, three equal suspect cards, CHECK THE SKY stamp.
Unlike Case 17 (bubble) and Case 16 (stopwatch).
Fairness: Demelza, Captain Quill and Miss Clemo share pose, size and neutral faces; the Gazette notice is on screen before
the question; the real night sky is drawn moonless throughout and Miss Clemo's moon appears only inside her own speech
bubble. Only the confession shows Miss Clemo sheepish. KEEP_ASPECT."""
NUM, NAME = 18, "The Moonlit Walk"
STYLE = "bw"
SLUG = "standalone-03-tidewhistle-case-18-the-moonlit-walk"
AUDIO = "standalone-03-tidewhistle-20-case-18-the-moonlit-walk.mp3"
TIMING = "timing-case-18.json"; CLUES = "clues/case-18.json"; ART = "work/art-18"; HOOK_WAV = "assets/hooks/hook-18.wav"
QUESTION = "Why does Agnes doubt Miss Clemo's story?"
HOOK_LINES = ["Whose story", "doesn't fit?"]; HOOK_EMOJI = "\u2B50"   # star (greyed in B&W)
HOOK_SAY = ("A priceless star chart vanishes from a clifftop tent, while everyone is gazing at the sky. Three people left "
            "early, and one walk home sounds just a little too lovely. Can you see why?")
HOOK_STYLE = "starfield"
HOOK_STAMP = "CHECK THE SKY"
HOOK_LABEL = "3 left early \u00b7 1 tent \u00b7 1 star chart"
HOOK_FOCUS = ((0.6, 0.45, 1.0), (0.7, 0.45, 1.25))
LINEUP_PANELS = 3
SHOW_QBAR = True
KEEP_ASPECT = True
NEXT_CARD = True
TRIM = 0.45
CUT, EXTRA = 109.8, 7.0          # after "...the solution follows." (ends ~109.58); "The Solution." ~114.08
NARR_END = 109.58
AUDIO_END = 172.0                # last word ends ~171.48
NO_CAP = {0, 1, 11, 14}          # titles, question card, "The Solution."

SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=5.0),
    # Agnes reads the Gazette over breakfast
    dict(k="art", img="breakfast", t0=5.0, t1=16.6, a=(0.5, 0.5, 1.0), b=(0.6, 0.45, 1.3)),
    # the back-page notice: NEW MOON THIS SATURDAY
    dict(k="art", img="notice", t0=16.6, t1=25.8, a=(0.5, 0.45, 1.25), b=(0.5, 0.5, 1.1)),
    # Saturday evening on the clifftop; the special guest; the star chart in the tent
    dict(k="art", img="cliff", t0=25.8, t1=45.4, a=(0.5, 0.5, 1.0), b=(0.72, 0.6, 1.35)),
    # eleven o'clock everyone outside; midnight the chart is gone
    dict(k="art", img="cliff", t0=45.4, t1=54.5, a=(0.45, 0.5, 1.05), b=(0.72, 0.6, 1.3)),
    dict(k="pan", t0=54.5, t1=79.0, keys=[
        (54.5, 0, 1.15), (66.9, 0, 1.26),
        (67.3, 1, 1.15), (72.7, 1, 1.26),
        (73.1, 2, 1.15), (79.0, 2, 1.26),
    ]),
    # Miss Clemo's story, her "full and bright" moon only inside her speech bubble
    dict(k="art", img="story", t0=79.0, t1=93.1, a=(0.45, 0.55, 1.1), b=(0.5, 0.6, 1.25)),
    # Agnes thinks of the notice
    dict(k="art", img="notice", t0=93.1, t1=98.0, a=(0.5, 0.5, 1.05), b=(0.5, 0.65, 1.4)),
    dict(k="ask", t0=98.0, t1=113.9),
    dict(k="soltitle", t0=113.9, t1=116.1),
    dict(k="art", img="board", t0=116.1, t1=150.9, a=(0.5, 0.5, 1.0), b=(0.55, 0.5, 1.12)),
    dict(k="art", img="confess", t0=150.9, t1=171.9, a=(0.45, 0.5, 1.05), b=(0.55, 0.45, 1.2)),
    dict(k="end", t0=171.9, t1=None),
]
SHORTS = dict(tag="", p1_end=103.6, recap=(98.0, 103.3), card_t=103.1,
              suspects="Demelza, Captain Quill, or Miss Clemo?")

def _pop(part, t, fade=0.3, s0=1.25, until=None):
    return dict(kind="sprite", part=part, show=(t, until), fade=fade, keys=[(t, dict(s=s0)), (t + 0.25, dict(s=1.0))], pivot="centre")

_SUS = ["s0", "s1", "s2"]
ANIM = {
    "hook": dict(art="hook", layers=[]),
    "cast": dict(art="cast", layers=[dict(kind="sprite", part=p, idle=True, blink=True) for p in _SUS]),
    "breakfast": dict(art="breakfast", layers=[
        dict(kind="sprite", part="agnes", idle=True, blink=True), dict(kind="sprite", part="cup"), _pop("gazette", 6.0)]),
    "notice": dict(art="notice", layers=[_pop("n0", 17.1), _pop("n1", 19.4), _pop("n2", 22.1), _pop("n3", 24.0)]),
    "cliff": dict(art="cliff", layers=[
        dict(kind="sprite", part="chart", show=(38.5, 52.9), fade=0.4),
        _pop("gone", 52.95),
        dict(kind="sprite", part="clemo", idle=True, blink=True, show=(32.6, 47.0), fade=0.4),
        _pop("guest", 31.5, until=45.2),
        dict(kind="sprite", part="clock", show=(45.7, None), fade=0.3, swaps=[(49.7, "mid", 0.4)]),
        dict(kind="sprite", part="club", show=(45.8, 49.6), fade=0.4),
    ]),
    "lineup": dict(art="lineup", layers=[
        *[dict(kind="sprite", part=p, idle=True, blink=True, nods=[t]) for p, t in zip(_SUS, (62.2, 67.4, 73.1))],
        _pop("t0", 63.6), _pop("h0", 71.1), _pop("t1", 67.8), _pop("h1", 71.1), _pop("t2", 75.4),
    ]),
    "story": dict(art="story", layers=[
        dict(kind="sprite", part="clemo", idle=True, blink=True, talk=dict(seg=9, quotes=True)),
        dict(kind="sprite", part="agnes", idle=True, blink=True, nods=[92.0]),
        dict(kind="sprite", part="ollie", idle=True, blink=True),
        _pop("bubble", 85.5),
    ]),
    "board": dict(art="board", layers=[_pop("new", 120.6), _pop("full", 126.9), _pop("x", 131.9), _pop("pair", 139.3)]),
    "confess": dict(art="confess", layers=[
        dict(kind="sprite", part="clemo", idle=True, blink=True, swaps=[(0.0, "sheepish", 0.01)]),
        _pop("chart", 166.7), _pop("talk", 170.3),
    ]),
}
