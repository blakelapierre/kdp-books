# Book-promo Shorts (TikTok @shortmysterycases + YouTube Shorts)

Separate from the Tidewhistle queue. **Nothing is posted yet** — `queue.tsv` rows are all `queued`.

- `build_promo_queue.py` → `queue.tsv` + `post/NAME.md` (YouTube title/description with Amazon link, AI = Yes, not made for kids; TikTok caption with "link in bio").
- Video source: `tidewhistle-video/src/promo.py` (`PROMOS`), rendered only on streambox: `sudo /usr/local/sbin/tw-render --case promo-NAME --skip-art`.
- Rendered files: streambox `/home/tidewhistle/tidewhistle-video/promo-NAME.mp4`, copied to the box at `/workspace/book-promos/` (MP4s are never committed).
- Part 1 → Part 2 pairs: post P2 after P1 and set YouTube Related video P1 → P2.
- Advent Clock first (Christmas timing).
