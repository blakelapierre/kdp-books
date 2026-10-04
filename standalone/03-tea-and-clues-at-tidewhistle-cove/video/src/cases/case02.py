"""Case 2, The Lemonade on the Lawn (see cases/case01.py for the field meanings). Times are ORIGINAL narration times
(timing-case-02.json, made with: align.py /tmp/tts/work/chapters.json <case02 16k wav> ../timing-case-02.json case-02)."""
NUM, NAME = 2, "The Lemonade on the Lawn"
SLUG = "standalone-03-tidewhistle-case-02-the-lemonade-on-the-lawn"
AUDIO = "standalone-03-tidewhistle-04-case-02-the-lemonade-on-the-lawn.mp3"
TIMING = "timing-case-02.json"; CLUES = "clues/case-02.json"; ART = "work/art-02"; HOOK_WAV = "work/hook-02.wav"
QUESTION = "Who took the silver locket?"
HOOK_LINES = ["Who took the", "silver locket?"]; HOOK_EMOJI = "\U0001F34B"
HOOK_SAY = "A silver locket has vanished, and only one clue gives the thief away. Can you spot it?"
HOOK_FOCUS = ((0.47, 0.5, 1.45), (0.46, 0.46, 1.9))   # push in on the empty jewellery box on the windowsill
LINEUP_PANELS = 3
TRIM = 0.45
CUT, EXTRA = 127.4, 7.0          # narration ends 127.14 ("...the solution follows."); "The Solution." starts 131.49
NARR_END = 127.14
AUDIO_END = 196.0
NO_CAP = {0, 1, 11, 14}          # case title, question and "The Solution." are shown as cards
SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=4.9),
    dict(k="art", img="hillparty", t0=4.9, t1=16.0, a=(0.5, 0.5, 1.08), b=(0.55, 0.4, 1.3)),
    dict(k="art", img="lawn", t0=16.0, t1=32.3, a=(0.5, 0.5, 1.08), b=(0.3, 0.42, 1.45)),
    dict(k="art", img="kitchen", t0=32.3, t1=49.0, a=(0.62, 0.5, 1.08), b=(0.46, 0.4, 1.6)),
    dict(k="art", img="kitchen_gone", t0=49.0, t1=50.4, a=(0.46, 0.4, 1.6), b=(0.46, 0.4, 1.55)),
    dict(k="pan", t0=50.4, t1=67.4, keys=[(50.4, 0, 1.12), (67.4, 0, 1.24)]),
    dict(k="art", img="garden", t0=67.4, t1=72.0, a=(0.5, 0.5, 1.08), b=(0.5, 0.46, 1.2)),
    dict(k="pan", t0=72.0, t1=111.6, keys=[(72.0, 1, 1.12), (85.0, 1, 1.22), (85.8, 2, 1.14), (111.6, 2, 1.28)]),
    dict(k="art", img="garden", t0=111.6, t1=116.0, a=(0.5, 0.5, 1.1), b=(0.76, 0.7, 1.7)),
    dict(k="ask", t0=116.0, t1=131.4),
    dict(k="soltitle", t0=131.4, t1=133.6),
    dict(k="art", img="glasses", t0=133.6, t1=155.9, a=(0.5, 0.5, 1.08), b=(0.62, 0.45, 1.3)),
    dict(k="art", img="kitchen_gone", t0=155.9, t1=170.3, a=(0.5, 0.5, 1.08), b=(0.6, 0.45, 1.3)),
    dict(k="pan", t0=170.3, t1=178.4, keys=[(170.3, 1, 1.14), (173.6, 1, 1.2), (174.3, 0, 1.14), (178.4, 0, 1.2)]),
    dict(k="art", img="returned", t0=178.4, t1=194.0, a=(0.5, 0.5, 1.08), b=(0.45, 0.45, 1.25)),
    dict(k="end", t0=194.0, t1=None),
]
# Shorts cuts, inside narration pauses: 121.45 between "Think about it." (ends 121.01) and "Take a moment" (121.91);
# 115.6 between "...the blazing sun." (115.09) and "Can you solve it?" (116.19).
SHORTS = dict(tag="", p1_end=121.45, recap=(115.6, 121.45), card_t=120.5, suspects="Captain Quill, Demelza, or Mr Bramble?")
