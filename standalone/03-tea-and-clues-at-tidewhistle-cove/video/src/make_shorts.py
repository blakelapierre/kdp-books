"""Cut YouTube Shorts (each <= 2:55) from the rendered vertical video, at narration pauses.

  python3 make_shorts.py            (after render.py vertical; --case=N or --case=3-color as for render.py)

Part 1: video 0 -> P1_END (pause after the question), then a 3 s card "Comment your guess! ... ANSWER IN PART 2".
Part 2: a 1 s silent "PART 2 · THE ANSWER" card, the question recap (RECAP), then the last CD_KEEP s of the
        countdown and the whole solution through the end card.
All times come from render.py (timing.json + the hook shift), so a cut never lands on a spoken word."""
import os, subprocess, sys, json
from PIL import Image, ImageDraw
import render as R

SHORTS = os.path.join(R.VID, "shorts"); os.makedirs(SHORTS, exist_ok=True)
CFG = R.SHORTS_CFG
SRC = os.path.join(R.VID, f"{R.VIDEO_SLUG}-vertical.mp4")
OUT1 = os.path.join(SHORTS, f"{R.SLUG}-{CFG['tag']}short-part1.mp4")
OUT2 = os.path.join(SHORTS, f"{R.SLUG}-{CFG['tag']}short-part2.mp4")
TMP = os.path.join(R.WORK, "shorts", *([R.PFX.rstrip("-")] if R.VARIANT else [])); os.makedirs(TMP, exist_ok=True)

def card(base_t, lines, path):
    L = R.Layout("vertical"); im = R.frame(L, base_t).convert("RGBA")
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    x0, y0, x1, y1 = 60, 560, 1020, 1360
    d.rectangle([0, 0, im.width, im.height], fill=R.PAPER + (120,))
    d.rounded_rectangle([x0 + 10, y0 + 14, x1 + 10, y1 + 14], radius=36, fill=R.SOFT + (70,))
    d.rounded_rectangle([x0, y0, x1, y1], radius=36, fill=R.ARTPAPER + (255,), outline=R.INK + (255,), width=5)
    d.rounded_rectangle([x0 + 14, y0 + 14, x1 - 14, y1 - 14], radius=26, outline=R.ACCENT + (255,), width=2)
    hs = sum(sz * 1.25 for _, _, sz, _ in lines); y = (y0 + y1) / 2 - hs / 2
    for text, font, size, col in lines:
        fs = size
        while fs > 30 and d.textlength(text, font=R.F(font, fs)) > (x1 - x0) - 90: fs -= 2   # shrink long lines to fit
        f = R.F(font, fs); R.ctext(d, im.width / 2, y + (size - fs) / 2, text, f, col + (255,)); y += size * 1.25
    Image.alpha_composite(im, ov).convert("RGB").save(path)

def run(cmd): subprocess.run(["ffmpeg", "-y", "-v", "error"] + cmd, check=True)

ENC = ["-c:v", "libx264", "-preset", "slow", "-crf", "21", "-tune", "animation", "-pix_fmt", "yuv420p", "-r", "30",
       "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "1", "-movflags", "+faststart"]

def still(png, dur, out):
    run(["-loop", "1", "-t", f"{dur}", "-i", png, "-f", "lavfi", "-t", f"{dur}", "-i", "anullsrc=r=48000:cl=mono",
         "-vf", "fps=30,format=yuv420p", "-shortest"] + ENC + [out])

def seg(t0, t1, out):
    run(["-ss", f"{t0:.3f}", "-to", f"{t1:.3f}", "-i", SRC] + ENC + [out])

def concat(parts, out, title):
    lst = os.path.join(TMP, "list.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    run(["-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", "-movflags", "+faststart", "-metadata", f"title={title}", "-metadata", "artist=Blake La Pierre", out])

def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)

def main():
    INK, SOFT, ACC = R.INK, R.SOFT, R.ACCENT
    c1 = os.path.join(TMP, "card1.png"); c2 = os.path.join(TMP, "card2.png")
    card(CFG["card_t"], [("Comment your guess!", "play", 70, INK), (CFG["suspects"], "crimi", 64, SOFT), ("", "crim", 30, INK),
                         ("ANSWER IN PART 2", "plex", 70, ACC)], c1)
    card(CFG["card_t"], [("PART 2 \u00b7 THE ANSWER", "plex", 66, ACC), ("", "crim", 24, INK), ("Did you work it out?", "play", 66, INK),
                         (CFG["title_line"], "crimi", 54, SOFT)], c2)
    a = [os.path.join(TMP, n) for n in ("p1a.mp4", "p1b.mp4", "p2a.mp4", "p2b.mp4", "p2c.mp4")]
    seg(0.0, CFG["p1_end"], a[0]); still(c1, 3.0, a[1])
    still(c2, 1.0, a[2]); seg(*CFG["recap"], a[3]); seg(CFG["cd_cut"], R.END, a[4])
    concat(a[:2], OUT1, CFG["yt_title"] + " (Part 1)"); concat(a[2:], OUT2, CFG["yt_title"] + " (Part 2)")
    for o in (OUT1, OUT2):
        d = dur(o); print(f"{o}: {d:.2f} s"); assert d <= 175.0, "Shorts must stay <= 2:55"

if __name__ == "__main__":
    main()
