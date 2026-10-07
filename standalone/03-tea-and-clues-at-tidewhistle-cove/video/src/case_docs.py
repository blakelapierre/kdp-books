"""Write docs/cases/case-NN-youtube.md in the Case 9/10 format (+ "Next case teaser" field) from a few fields.
Used by the per-case doc stubs in /workspace/tw_docs/docNN.py:  write(N, emoji, p1_title, p1_body, question, wide_title, wide_lead)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cases import teasers as T
import importlib
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
BOOK = '"Tea and Clues at Tidewhistle Cove", a book of gentle, cozy mini-mysteries'

def write(N, emoji, p1_title, p1_body, question, wide_title, wide_lead):
    C = importlib.import_module(f"cases.case{N:02d}"); slug = C.SLUG; name = C.NAME
    last = N >= T.LAST_CASE
    if not last:
        nt, tz = T.TITLES[N + 1], T.TEASERS[N + 1]
        teaser_block = f'**Next case teaser** (Case {N + 1} "{nt}"; on the end card of the wide video and Part 2, and can go in the descriptions)\n```\n{tz}\n```\n'
        nxt = f'\n\nNext up, Case {N + 1} "{nt}": {tz} New case every 6 hours.'
    else:
        teaser_block = ('**Next case teaser**: none. This is the last case in the book. The end card of the wide video and Part 2 '
                        'says so and points to the book instead.\n')
        nxt = f'\n\nThat was the last case in the book. All 30 cozy mini-mysteries, with every solution, are in {BOOK.split(",")[0]}.'
    md = f'''# Case {N} "{name}": YouTube text

No spoilers in Part 1 or the wide description: the answer is only in the Part 2 video (and the second half of the wide video) itself.

{teaser_block}
## Part 1 (`{slug}-short-part1.mp4`)

**Title** (≤100 characters)
```
{p1_title}
```

**Description**
```
{p1_body.strip()}

Pause before Part 2 and drop your guess in the comments: {question}

Case {N} of 30 from {BOOK} by Blake La Pierre. Coming soon to Kindle.

#cozymystery #mysterypuzzle #whodunit #brainteaser #riddle #canyousolveit #shorts
```

**Tags**
```
cozy mystery, mystery puzzle, whodunit, brainteaser, riddle, can you solve it, shorts, tidewhistle cove, tea and clues
```

## Part 2 (`{slug}-short-part2.mp4`)

**Title**
```
The answer: {emoji} Case {N} {name} #shorts
```

**Description**
```
The solution to Case {N}, {name}.

(Spoilers in the video.){nxt}

Case {N} of 30 from {BOOK} by Blake La Pierre. Coming soon to Kindle.

#cozymystery #mysterypuzzle #whodunit #shorts
```

## Wide / main channel (`{slug}-wide.mp4`)

**Title**
```
{wide_title}
```

**Description**
```
{wide_lead.strip()}

Pause when Agnes asks the question, then watch the solution.{nxt}

Case {N} of 30 from {BOOK} to solve by ear, by Blake La Pierre. Coming soon to Kindle.

#cozymystery #mysterypuzzle #whodunit #audiobook
```
'''
    assert len(p1_title) <= 100 and len(wide_title) <= 100
    out = os.path.join(ROOT, "docs", "cases", f"case-{N:02d}-youtube.md"); open(out, "w").write(md); print(out)
