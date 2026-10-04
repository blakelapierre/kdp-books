# Case 1 video: The Prize Sponge

A storybook-style video of Case 1 from *Tea and Clues at Tidewhistle Cove*, by Blake La Pierre. It uses the same Kokoro narration as the audiobook preview. Every frame is drawn locally by code, with no paid or AI video services.

| File | Format | Length | Size |
|---|---|---|---|
| `standalone-03-tidewhistle-case-01-the-prize-sponge-vertical.mp4` | 1080x1920, 30 fps, H.264 + AAC 128k (Shorts, Reels, TikTok) | 3:41 | ~36 MB |
| `standalone-03-tidewhistle-case-01-the-prize-sponge-wide.mp4` | 1920x1080, 30 fps, H.264 + AAC 128k (YouTube, Facebook) | 3:41 | ~34 MB |

## What's in it
- **Title card:** Tea and Clues at Tidewhistle Cove, Case 1: The Prize Sponge, by Blake La Pierre.
- **9 black-and-white ink illustrations** in the house `inkart` style, adapted for the seaside (no snow): the Summer Show harbour, the Kettle and Gull with Agnes, the hall table of covered cakes, Agnes's handbag with the entry list, the empty plate, a four-panel lineup (Constable Ollie, Morwenna, Hedley, Jago) that pans to whoever is speaking, and three scenes that appear only after "The Solution": the "lemon drizzle?" clue, the bakery van, and the prize cake. The pictures before the solution don't give the answer away. All the cakes stay covered, and the lineup treats everyone the same.
- Slow Ken Burns pans and zooms with 0.7 s crossfades.
- **Large captions** (Crimson Text, about 72 px on vertical), timed to the words. Timing comes from narrate.py's segment times plus faster-whisper word timestamps (`timing.json`).
- **"Can you solve it?" card** showing the question, with a visible 10-to-1 countdown ring after "Think about it…".
- **End card** with the title, by Blake La Pierre, **Coming soon to Kindle**. Change this to "Available on Kindle" only once the ebook is live.

## Rebuild
```
cd src
python3 art.py                   # illustrations -> ../work/art/
python3 render.py vertical       # ~1.5 min on 8 CPUs
python3 render.py wide
python3 render.py vertical --frames 20,152,218   # stills for checking -> ../work/frames/
# timing (only if the narration changes; needs the TTS venv with faster-whisper):
/tmp/tts/venv/bin/python align.py /tmp/tts/work/chapters.json <case01 16k wav> ../timing.json
```
Needs Python 3, Pillow, reportlab, poppler-utils (pdftoppm) and ffmpeg.

## Sharing note
The repo is private, so download the MP4 and upload it to the platform yourself. If a platform asks, say the narration is AI-generated (a synthetic voice), which matches the audiobook disclosure.
