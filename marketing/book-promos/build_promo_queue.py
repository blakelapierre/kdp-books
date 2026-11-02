"""Builds the book-promo Shorts queue + post text (YouTube Shorts + TikTok). Nothing here posts anything.
Videos render on streambox (tidewhistle-video src/promo.py via sudo /usr/local/sbin/tw-render --case promo-NAME);
files land in /home/tidewhistle/tidewhistle-video/promo-NAME.mp4 and are mirrored to /workspace/book-promos/ on the box.
Run: python3 build_promo_queue.py  -> queue.tsv + post/NAME.md"""
import os, csv
A = "https://www.amazon.com/dp/"
TAGS_YT = "#shorts #puzzle #cozy"
V = [  # seq, name, book, asin, part, pairs_with, title, hook line, tiktok hashtags
 (1, "advent-clock", "The Advent Clock", "B0HMW1MR5T", "P1", "advent-clock-p2", "Can you find the key to Door 1? 🎄 The Advent Clock",
  "24 little doors, 24 puzzles. Door 1 is a winter word search: find all 11 words, and the leftover letters spell the key. Comment your answer! Answer in Part 2.",
  "#adventcalendar #wordsearch #christmaspuzzle #puzzlebook #booktok"),
 (2, "advent-clock-p2", "The Advent Clock", "B0HMW1MR5T", "P2", "", "Door 1 answer: the key is… 🎄 The Advent Clock (Part 2)",
  "The answer to Door 1! Did you get it? 23 more doors are waiting, one for every day until Christmas.",
  "#adventcalendar #wordsearch #christmaspuzzle #puzzlebook #booktok"),
 (3, "frostwood-cocoa-tin", "The Thief Stayed the Night (Frostwood 1)", "B0HLMMS675", "P1", "frostwood-cocoa-tin-p2", "Who took the cocoa tin? ☕ A snowed-in logic mystery",
  "Forty guests, one missing cocoa tin, six clues. Can you find the thief? Comment your guess. Answer in Part 2.",
  "#logicpuzzle #cozymystery #whodunit #puzzlebook #booktok"),
 (4, "frostwood-cocoa-tin-p2", "The Thief Stayed the Night (Frostwood 1)", "B0HLMMS675", "P2", "", "The cocoa tin thief is… ☕ (Part 2)",
  "The answer! Here's how the last two clues point to one guest.", "#logicpuzzle #cozymystery #whodunit #puzzlebook #booktok"),
 (5, "frostwood-express", "Frostwood Express (Frostwood 2)", "B0HLMB966Q", "P1", "frostwood-express-p2", "Can you lay the train track? 🚂 10-second puzzle",
  "A Train Tracks logic puzzle: connect the arrows so every row and column has the right number of track squares. Pause and try it! Answer in Part 2.",
  "#logicpuzzle #traintracks #brainteaser #puzzlebook #booktok"),
 (6, "frostwood-express-p2", "Frostwood Express (Frostwood 2)", "B0HLMB966Q", "P2", "", "Train track answer 🚂 (Part 2)",
  "Here's the solution. Did you get it? 200 more in the book, easy to expert.", "#logicpuzzle #traintracks #brainteaser #puzzlebook #booktok"),
 (7, "bridges-of-frostwood", "Bridges of Frostwood", "B0HN6JKQQV", "single", "", "Can you connect all 10 islands? 🌉 Bridges puzzle",
  "Each number says how many bridges touch that island. Pause and try it in 15 seconds, then see the answer.", "#logicpuzzle #hashi #brainteaser #puzzlebook #booktok"),
 (8, "porch-swing-crosswords", "Porch Swing Crosswords", "B0HN6QXPFG", "single", "", "4 cozy crossword clues, one per season 🍂 How many can you get?",
  "Four seasonal clues, a few seconds each. Comment your score!", "#crossword #wordpuzzle #cozy #puzzlebook #booktok"),
 (9, "stories-we-keep", "The Stories We Keep", "B0HN6TSN7T", "single", "", "The gift of their stories 💛 A keepsake for grandparents",
  "Gentle prompts that help a parent or grandparent write their life story, one page at a time. A gift that comes back filled with their memories.",
  "#giftideas #grandparents #memorybook #keepsake #booktok"),
 (10, "tidewhistle", "Tea and Clues at Tidewhistle Cove", "B0HNFZGV6T", "single", "", "30 cozy mysteries 🫖 The book behind our mystery Shorts",
  "Tea and Clues at Tidewhistle Cove: 30 little seaside mysteries to solve before the kettle boils. No scary bits, just puzzles, tea and kind neighbours.",
  "#cozymystery #mysterybook #kindle #booktok #whodunit"),
]
os.makedirs("post", exist_ok=True)
with open("queue.tsv", "w", newline="") as f:
    w = csv.writer(f, delimiter="\t"); w.writerow(["seq", "name", "book", "asin", "amazon_url", "part", "related_part2", "file", "yt_status", "tt_status", "yt_url", "tt_url"])
    for seq, n, book, asin, part, p2, title, hook, tt in V:
        url = A + asin
        w.writerow([seq, n, book, asin, url, part, p2, f"promo-{n}.mp4", "queued", "queued", "", ""])
        desc = f"{hook}\n\n📖 {book}: {url}\n\nCozy puzzles and mysteries from Blake La Pierre. {TAGS_YT}"
        cap = f"{hook}\n\n📖 {book} · link to buy in bio\n{tt}"
        open(f"post/{n}.md", "w").write(
            f"# {n}\n\n- Book: {book} ({asin})\n- Amazon: {url}\n- File: promo-{n}.mp4 (1080x1920)\n- Part: {part}" + (f" (Related video → {p2})" if p2 else "") +
            "\n- YouTube: Altered/synthetic content (AI) = **Yes** · Made for kids = **No** · Shorts\n\n"
            f"## YouTube title\n{title}\n\n## YouTube description\n{desc}\n\n## TikTok caption (no links in captions; put the Amazon link in bio)\n{cap}\n\nBio link to use: {url}\n")
print("wrote", len(V))
