# Pinterest: Tea and Clues at Tidewhistle Cove

Goal: sell the book. Every pin links to the book's Amazon page.

**Amazon link:** `AMAZON_URL_TBD`. The book isn't on KDP yet (repo README says "Draft, ebook-ready. Not yet published"), so there's no ASIN. Once it's live, replace `AMAZON_URL_TBD` in `src/pinterest_docs.py`, then rerun it. (You could link to Blake's live Frostwood books in the meantime, but they're a different series.)

## Files
- `images/pin-case-NN-*.png`: 1000x1500 (2:3) image pins in black-and-white ink, Cases 1-10. Each has a hook question, a scene, 3 clues in Agnes's notebook (no answer), and a footer. Made by `../src/pinterest_pins.py`.
- `scenes/`: raw scene crops taken from each Part 1 Short.
- Video pins: the existing B&W Part 1 Shorts in `../shorts/*-short-part1.mp4`. They're used as-is with no re-encode, because all meet Pinterest's specs: 1080x1920 9:16, MP4, H.264 yuv420p + AAC, 1:43-2:35 long (limit is 4 s-15 min), 11-35 MB (limit is 4 GB). Use the matching image pin as the cover.
- `pins.csv`: bulk-upload sheet with 20 pins. Pinterest's bulk upload needs a public **Media URL**, so host the files (for example on Drive or Dropbox with public links) and swap them in for the relative paths. Publish dates are relative slots (T+0h, T+3h, ...). Change them to real dates when uploading.
- `pins.md`: the same pins in readable form, with title, description, alt text, board and link.

## Boards
1. **Cozy Mystery Puzzles**: Gentle whodunits from a seaside village. Read the clues, spot the fib, solve the case. Short cozy mystery puzzles for tea-break sleuths.
2. **Logic Puzzles for Kids**: Story-based logic puzzles and brain teasers for kids and families, with no grids or maths. Just listen, think and solve together.
3. **Whodunit Riddles**: Quick mystery riddles. Who took it, and how do you know? Answers are in the book.
4. **Tea and Clues at Tidewhistle Cove**: The book's home board, with all 30 cozy mini-mysteries starring Agnes Bell of the Kettle and Gull tea room. Every case pin goes here too (save each pin to its topic board first, then to this one).

## Profile
- **Name:** Tidewhistle Cove Mysteries | Cozy Mystery Puzzles
- **Bio (≤500):** Cozy mini-mysteries you can solve in two minutes. ☕🔎 Join Agnes Bell in a little seaside village where prize cakes vanish and alibis crack. New case every 6 hours, for kids, families and puzzle lovers. From the book *Tea and Clues at Tidewhistle Cove* by Blake La Pierre.
- **Website:** the Amazon book link, once it exists.
