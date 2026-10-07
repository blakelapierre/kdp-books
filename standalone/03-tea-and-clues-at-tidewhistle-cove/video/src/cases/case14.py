"""Case 14, The Blue Ribbon Key: BLACK-AND-WHITE ink with the simple v1 peg-doll characters, SIMPLE ANIMATIONS (anim.py),
mid-screen question bar (Case 7+ layout), clue notebook and a "next case" end card.
Times are ORIGINAL narration times (timing-case-14.json, whole-file whisper alignment). render.py adds the hook shift
and the countdown splice. Art: art_case14.py -> work/art-14/ (bwkit). Part sprites use part_open (no frame2).
Opening: HOOK_STYLE="keyhole" (render.py): title on a swinging key-fob tag, the hall door + plant pot seen through a
keyhole that opens out, three equal luggage-tag suspect cards, ONE SLIP OF THE TONGUE stamp.
Unlike Case 12 (calendar) and Case 13 (red pen).
Fairness: Demelza, Pip and Mr Spargo share pose, size and neutral faces until the solution; only the confession shows
Mr Spargo sheepish. Nothing marks his "blue ribbon" line before the solution. KEEP_ASPECT: crops match the view."""
NUM, NAME = 14, "The Blue Ribbon Key"
STYLE = "bw"
SLUG = "standalone-03-tidewhistle-case-14-the-blue-ribbon-key"
AUDIO = "standalone-03-tidewhistle-16-case-14-the-blue-ribbon-key.mp3"
TIMING = "timing-case-14.json"; CLUES = "clues/case-14.json"; ART = "work/art-14"; HOOK_WAV = "assets/hooks/hook-14.wav"
QUESTION = "What gave Mr Spargo away?"
HOOK_LINES = ["Who knew", "the secret?"]; HOOK_EMOJI = "\U0001F511"   # key (greyed in B&W)
HOOK_SAY = ("The raffle hamper has vanished from a locked village hall, and nobody broke in. Three helpers, one hidden "
            "key, and one slip of the tongue. Can you catch it?")
HOOK_STYLE = "keyhole"
HOOK_STAMP = "ONE SLIP OF THE TONGUE"
HOOK_LABEL = "3 helpers \u00b7 1 locked hall \u00b7 1 hidden key"
HOOK_FOCUS = ((0.5, 0.5, 1.0), (0.62, 0.62, 1.3))
LINEUP_PANELS = 3
SHOW_QBAR = True
KEEP_ASPECT = True
NEXT_CARD = True
TRIM = 0.45
CUT, EXTRA = 110.25, 7.0         # after "...the solution follows." (ends ~110.03); "The Solution." ~114.53
NARR_END = 110.03
AUDIO_END = 170.2                # last word ends ~169.5; MP3 is ~172.2 s
NO_CAP = {0, 1, 11, 14}          # titles, question card, "The Solution."

SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=5.1),
    # the spare key on its ribbon under the plant pot; committee only
    dict(k="art", img="front", t0=5.1, t1=23.0, a=(0.5, 0.5, 1.0), b=(0.72, 0.62, 1.45)),
    # the raffle hamper vanishes from the locked hall
    dict(k="art", img="inside", t0=23.0, t1=43.2, a=(0.55, 0.6, 1.2), b=(0.4, 0.55, 1.05)),
    # Ollie lifts the pot, looks, sets it down
    dict(k="art", img="front", t0=43.2, t1=55.9, a=(0.6, 0.58, 1.15), b=(0.66, 0.62, 1.35)),
    dict(k="pan", t0=55.9, t1=81.0, keys=[
        (55.9, 0, 1.15), (70.6, 0, 1.26),
        (71.0, 1, 1.15), (76.9, 1, 1.26),
        (77.3, 2, 1.15), (81.0, 2, 1.26),
    ]),
    # Mr Spargo: "A spare key? Under a plant pot? ... a key on a blue ribbon like that"
    dict(k="art", img="spargo", t0=81.0, t1=98.9, a=(0.42, 0.55, 1.1), b=(0.5, 0.55, 1.05)),
    dict(k="ask", t0=98.9, t1=114.3),
    dict(k="soltitle", t0=114.3, t1=116.5),
    dict(k="art", img="board", t0=116.5, t1=147.8, a=(0.5, 0.5, 1.0), b=(0.55, 0.5, 1.15)),
    # the hamper back, one jar of jam lighter; a book of raffle tickets
    dict(k="art", img="confess", t0=147.8, t1=170.0, a=(0.5, 0.55, 1.05), b=(0.55, 0.52, 1.18)),
    dict(k="end", t0=170.0, t1=None),
]
SHORTS = dict(tag="", p1_end=104.4, recap=(98.9, 104.1), card_t=103.9,
              suspects="Demelza, Pip, or Mr Spargo?")

def _pop(part, t, fade=0.3, s0=1.25, until=None):
    return dict(kind="sprite", part=part, show=(t, until), fade=fade, keys=[(t, dict(s=s0)), (t + 0.25, dict(s=1.0))], pivot="centre")

_SUS = ["s0", "s1", "s2"]
_LIFT = [(7.4, dict(dy=0)), (7.9, dict(dy=72)), (16.6, dict(dy=72)), (17.1, dict(dy=0)),
         (45.9, dict(dy=0)), (46.4, dict(dy=72)), (48.7, dict(dy=72)), (49.2, dict(dy=0))]
ANIM = {
    "hook": dict(art="hook", layers=[]),
    "cast": dict(art="cast", layers=[dict(kind="sprite", part=p, idle=True, blink=True) for p in _SUS]),
    "front": dict(art="front", layers=[
        dict(kind="sprite", part="ollie", idle=True, blink=True, show=(43.0, None), fade=0.4),
        dict(kind="sprite", part="key"),
        dict(kind="sprite", part="pot", keys=_LIFT),
        _pop("committee", 18.2, until=43.0),
    ]),
    "inside": dict(art="inside", layers=[
        dict(kind="sprite", part="hamper", show=(None, 33.6), fade=0.45),
        dict(kind="sprite", part="gone", show=(33.7, None), fade=0.4),
        _pop("lock", 40.4),
    ]),
    "lineup": dict(art="lineup", layers=[
        dict(kind="sprite", part=p, idle=True, blink=True, nods=[t]) for p, t in zip(_SUS, (63.2, 71.3, 78.2))]),
    "spargo": dict(art="spargo", layers=[
        dict(kind="sprite", part="spargo", idle=True, blink=True, talk=dict(seg=9, quotes=True)),
        dict(kind="sprite", part="ollie", idle=True, blink=True, nods=[96.6]),
        dict(kind="sprite", part="agnes", idle=True, blink=True, nods=[96.8]),
    ]),
    "board": dict(art="board", layers=[_pop("ring", 126.0), _pop("nobody", 131.0), _pop("only", 135.2)]),
    "confess": dict(art="confess", layers=[
        dict(kind="sprite", part="spargo", idle=True, blink=True, swaps=[(0.0, "sheepish", 0.01)]),
        dict(kind="sprite", part="ollie", idle=True, blink=True, nods=[165.4]),
        _pop("hamper", 157.6), _pop("jam", 160.0), _pop("tickets", 162.5),
    ]),
}
