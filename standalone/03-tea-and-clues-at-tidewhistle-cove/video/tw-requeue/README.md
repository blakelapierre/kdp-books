# Tidewhistle colour-only repost queue

Built 2026-10-17 from `yt_delete.txt` (69 YouTube IDs) and `tt_delete.tsv` (68 TikTok posts), the 0-view
Tidewhistle videos Blake approved for deletion (promos kept). Nothing in here has been uploaded.

- A slot is (case, Part 1 / Part 2 / wide) on YouTube, (case, Part 1 / Part 2) on TikTok. A slot is queued only if
  **every** known copy (B&W original and colour repost) is in the delete list. ID→slot mapping comes from
  `publish-log.md` plus `marketing/youtube-history.md` (Cases 1–9 IDs). Cases 1–9 wide IDs aren't recorded and none
  are in the delete list, so they're treated as surviving.
- One colour file per slot: `-color` files for Cases 1, 3 and 10–30 (25–30 `-color` = the swapped originals), original
  names for the other Cases 1–9, which were colour from the start. All files were checked and exist.
- Text reused from `shorts/case-NN-youtube.md`. Stale "Next up"/"Next case" lines removed and replaced with "More cases in the
  Tidewhistle Cove Mysteries playlist." Cases 10–24 keep the " (Colour)" title suffix, like the earlier reposts. Every entry includes "whodunit puzzle" / #whodunitpuzzle.
  YouTube descriptions end with the 📚 book block.
- YouTube settings for each post: Public, AI was used = Yes, not made for kids, playlist "Tidewhistle Cove Mysteries". For P1, set Related video
  to that case's live Part 2 at post time, whether it's a surviving copy or a reposted one (`related_video_note` column).
- Post in `seq` order, one every 7 hours per platform. After each post, set `status=posted` and fill in `posted_id`.
  `\n` in the TSV text means a newline.
- If `yt_deleted.txt` / `tt_deleted.txt` (the actual deletions) differ from the delete lists, rerun
  `parse.py && slots.py && build.py` with those files in place of the delete lists.

Counts: YouTube 30 entries (~8.75 days), TikTok 39 entries (~11.4 days).

2026-10-22: Blake approved fresh TikTok copies of the stalled (0–2 view) Case 8 P1/P2, Case 9 P1/P2 and Case 10 P1 posts.
Old posts are NOT deleted. New rows use the same files with fresh hooks, spread through the pending queue (pending rows renumbered):
seq 17 Case 8 P1, 22 Case 8 P2, 27 Case 9 P1, 32 Case 9 P2, 37 Case 10 P1. TikTok queue is now 44 entries.
