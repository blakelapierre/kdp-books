"""Case 3, The Dry Raincoat (see cases/case01.py for the field meanings). Times are ORIGINAL narration times
(timing-case-03.json, made with: align.py /tmp/tts/work/chapters.json <case03 16k wav> ../timing-case-03.json case-03).
STYLE = "bw": black-and-white ink art (art_case03.py) and a black-and-white frame/notebook; red solution marks stay."""
NUM, NAME = 3, "The Dry Raincoat"
STYLE = "bw"
SLUG = "standalone-03-tidewhistle-case-03-the-dry-raincoat"
AUDIO = "standalone-03-tidewhistle-05-case-03-the-dry-raincoat.mp3"
TIMING = "timing-case-03.json"; CLUES = "clues/case-03.json"; ART = "work/art-03"; HOOK_WAV = "work/hook-03.wav"
QUESTION = "Who took the signed book, and what gave them away?"
HOOK_LINES = ["Who took the", "signed book?"]; HOOK_EMOJI = "\U0001F4DA"
HOOK_SAY = "A signed book has vanished, and only one clue gives the thief away. Can you spot it?"
HOOK_FOCUS = ((0.49, 0.52, 1.3), (0.49, 0.56, 1.7))   # push in on the open, empty glass case
LINEUP_PANELS = 3
TRIM = 0.45
CUT, EXTRA = 136.6, 7.0          # narration ends 135.91 ("...the solution follows."); "The Solution." starts 140.57
NARR_END = 135.91
AUDIO_END = 210.0                # last word "time." ends 209.02
NO_CAP = {0, 1, 12, 15}          # case title, question and "The Solution." are shown as cards
SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=4.5),
    dict(k="art", img="street", t0=4.5, t1=14.1, a=(0.5, 0.5, 1.08), b=(0.46, 0.52, 1.35)),
    dict(k="art", img="case", t0=14.1, t1=30.1, a=(0.5, 0.5, 1.08), b=(0.5, 0.52, 1.35)),
    dict(k="art", img="storm", t0=30.1, t1=44.6, a=(0.5, 0.5, 1.08), b=(0.5, 0.42, 1.3)),
    dict(k="art", img="gone", t0=44.6, t1=51.6, a=(0.5, 0.5, 1.1), b=(0.49, 0.55, 1.45)),
    dict(k="art", img="chemist", t0=51.6, t1=56.4, a=(0.5, 0.5, 1.08), b=(0.5, 0.45, 1.2)),
    dict(k="pan", t0=56.4, t1=89.5, keys=[(56.4, 0, 1.12), (74.4, 0, 1.24), (75.2, 1, 1.14), (89.5, 1, 1.26)]),
    dict(k="art", img="bell", t0=89.5, t1=102.6, a=(0.5, 0.5, 1.08), b=(0.5, 0.72, 1.6)),
    dict(k="pan", t0=102.6, t1=118.1, keys=[(102.6, 2, 1.12), (118.1, 2, 1.28)]),
    dict(k="art", img="thinking", t0=118.1, t1=123.8, a=(0.5, 0.5, 1.08), b=(0.45, 0.5, 1.25)),
    dict(k="ask", t0=123.8, t1=140.4),
    dict(k="soltitle", t0=140.4, t1=142.6),
    dict(k="art", img="compare", t0=142.6, t1=168.2, a=(0.5, 0.5, 1.08), b=(0.62, 0.5, 1.3)),
    dict(k="art", img="bell", t0=168.2, t1=176.4, a=(0.5, 0.72, 1.5), b=(0.5, 0.5, 1.1)),
    dict(k="pan", t0=176.4, t1=184.8, keys=[(176.4, 0, 1.14), (180.9, 0, 1.2), (181.6, 1, 1.14), (184.8, 1, 1.2)]),
    dict(k="art", img="gone", t0=184.8, t1=189.7, a=(0.5, 0.5, 1.1), b=(0.49, 0.55, 1.35)),
    dict(k="art", img="returned", t0=189.7, t1=208.9, a=(0.5, 0.5, 1.08), b=(0.45, 0.48, 1.25)),
    dict(k="end", t0=208.9, t1=None),
]
# Shorts cuts, inside narration pauses: 130.4 between "Think about it." (ends 129.88) and "Take a moment" (130.85);
# 123.6 between "...So were her shoes." (122.91) and "Can you solve it?" (124.20).
SHORTS = dict(tag="", p1_end=130.4, recap=(123.6, 130.4), card_t=129.5, suspects="Hedley, Pip, or Wenna?")
