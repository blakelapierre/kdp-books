# Case 7 visual checklist

Confirmed on-screen (not narration-only):

1. Sir Reginald — hook hero close-up (red hat, beard, rod); garden gnome part; returned bright hat; vignette
2. Empty pedestal + crushed grass — hook + garden after "gone" (gnome part hidden)
3. High thick hedge + wooden gate — garden, porch, returned, lineup
4. Pickle in porch facing the gate — porch part (awake/sleep swaps); night sleeping; kitchen basket thump
5. Still night / no bark — night plate: moon, lit Hocking window, sleeping Pickle
6. Mrs Ashby (holidaymaker) — street show-in, cast, lineup beach panel
7. Mr Fenwick (grocer) — street, cast, lineup shop panel (+ tiny rival gnome prop)
8. Pip Carew — street, cast, lineup, shed confession, returned smile
9. Repaint surprise — shed paint pots + bright-hat gnome; returned on pedestal

Part sprites use `part_open` (clip only). No `frame2` on animated parts.

Layout (shared `render.py`, Case 7+):
- Case subtitle above art frame with clear padding (no text-through-border)
- Taller question bar; "THE QUESTION" label above text with gap; question never sits under border lines
- Air between qbar and captions / notebook

Open (Case 7-specific): `HOOK_BORDER=False`, banner title, garden-green accent, hero gnome fills frame.
