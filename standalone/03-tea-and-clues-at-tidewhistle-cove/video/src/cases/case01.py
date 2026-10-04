"""Case 1, The Prize Sponge: everything render.py / make_shorts.py need that is specific to this case.
Times are ORIGINAL narration times (timing.json); render.py adds the hook shift and the countdown splice."""
NUM, NAME = 1, "The Prize Sponge"
SLUG = "standalone-03-tidewhistle-case-01-the-prize-sponge"
AUDIO = "standalone-03-tidewhistle-03-case-01-the-prize-sponge.mp3"   # in ../../audio/
TIMING = "timing.json"; CLUES = "clues/case-01.json"; ART = "work/art"; HOOK_WAV = "work/hook.wav"
QUESTION = "Who took entry number seven, and how does Agnes know?"
HOOK_LINES = ["Who stole the", "prize cake?"]; HOOK_EMOJI = "\U0001F370"
HOOK_SAY = "A prize cake has vanished, and only one clue gives the thief away. Can you spot it?"
HOOK_FOCUS = ((0.47, 0.56, 1.3), (0.44, 0.6, 1.65))   # (cx, cy, zoom) start -> end on art "hook"
LINEUP_PANELS = 4
TRIM = 0.45                     # leading silence trimmed off the case MP3 (it has 0.75 s)
CUT, EXTRA = 153.4, 7.0         # narration ends 153.08 ("...the solution follows."); "The Solution." was 157.4
NARR_END = 153.08               # last pre-solution word; the countdown starts 0.62 s later
AUDIO_END = 216.45
NO_CAP = {0, 1, 12, 15}         # case title, question and "The Solution." are shown as cards instead
SCENES = [
    dict(k="hook", t0=None, t1=TRIM),
    dict(k="title", t0=TRIM, t1=4.6),
    dict(k="art", img="village", t0=4.6, t1=13.5, a=(0.5, 0.5, 1.08), b=(0.62, 0.52, 1.3)),
    dict(k="art", img="hall", t0=13.5, t1=30.3, a=(0.5, 0.5, 1.08), b=(0.62, 0.52, 1.3)),
    dict(k="art", img="handbag", t0=30.3, t1=41.0, a=(0.47, 0.5, 1.1), b=(0.44, 0.42, 1.4)),
    dict(k="art", img="tearoom", t0=41.0, t1=46.0, a=(0.5, 0.5, 1.08), b=(0.53, 0.42, 1.3)),
    dict(k="pan", t0=46.0, t1=64.8, keys=[(46.0, 1, 1.12), (51.6, 1, 1.2), (52.4, 2, 1.14), (54.0, 2, 1.2), (54.8, 3, 1.14), (64.8, 3, 1.26)]),
    dict(k="art", img="plate", t0=64.8, t1=77.4, a=(0.5, 0.5, 1.1), b=(0.46, 0.55, 1.4)),
    dict(k="pan", t0=77.4, t1=134.0, keys=[(77.4, 0, 1.12), (96.8, 0, 1.24), (97.6, 1, 1.14), (107.4, 1, 1.22), (108.2, 2, 1.14), (120.2, 2, 1.22), (121.0, 3, 1.14), (134.0, 3, 1.26)]),
    dict(k="art", img="handbag", t0=134.0, t1=140.6, a=(0.45, 0.42, 1.35), b=(0.5, 0.5, 1.1)),
    dict(k="ask", t0=140.6, t1=157.4),
    dict(k="soltitle", t0=157.4, t1=159.5),
    dict(k="art", img="clue", t0=159.5, t1=190.8, a=(0.5, 0.52, 1.08), b=(0.5, 0.4, 1.25)),
    dict(k="art", img="van", t0=190.8, t1=208.4, a=(0.5, 0.5, 1.08), b=(0.66, 0.46, 1.3)),
    dict(k="art", img="prize", t0=208.4, t1=214.6, a=(0.5, 0.5, 1.08), b=(0.55, 0.48, 1.25)),
    dict(k="end", t0=214.6, t1=None),
]
# Shorts cuts (make_shorts.py), all inside narration pauses of timing.json:
#   147.4 in the pause after "Think about it." (146.95-147.85); 140.4 in the pause before "Can you solve it?" (139.64-140.74).
SHORTS = dict(tag="color-", p1_end=147.4, recap=(140.4, 147.4), card_t=146.0, suspects="Morwenna, Hedley, or Jago?")
