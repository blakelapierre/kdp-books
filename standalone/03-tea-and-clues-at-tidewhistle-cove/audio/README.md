# Tea and Clues at Tidewhistle Cove: audiobook preview

A full read-aloud preview, narrated by a local digital voice (Kokoro-82M, voice `af_heart`; the model is Apache-2.0 licensed). It's for listening and sharing. It is **not** the file for Audible: Audible only takes AI narration through KDP Virtual Voice, which Amazon produces itself once the ebook is live.

- [Full audiobook, one file, about 1 hr 35 min, 69 MB](standalone-03-tea-and-clues-at-tidewhistle-cove-full-audiobook.mp3?raw=true), 96 kbps mono, easiest to share
- [Sample, about 3-5 min](standalone-03-tea-and-clues-at-tidewhistle-cove-audio-sample.mp3?raw=true)
- One MP3 per chapter is in this folder too (192 kbps CBR, 44.1 kHz mono, about -20.5 dB RMS, peaks about -5 dB)

Each case ends with "Think about it..." followed by a pause before the answer, so you can guess first.

Rebuild: `tools/narrate.py` (needs kokoro-onnx plus the model files in `$KOKORO_DIR`), then `tools/master.py`.
