"""No-spoiler 'next case' teaser lines (Blake 2026-10-07). The end card of Case N teases Case N+1 with TEASERS[N+1];
the same line goes in case-NN-youtube.md as the 'Next case teaser' field. Case 30 (the last case) gets the
book end card instead (render.py: next_card, LAST_CASE)."""
TITLES = {
    9: "The Sunset over the Sea", 10: "The Wet Paint Bench", 11: "The Window Table", 12: "The Stopped Clock",
    13: "The Misspelled Note", 14: "The Blue Ribbon Key", 15: "The Warm Bonnet", 16: "The Lighthouse Path",
    17: "The Talking Parrot", 18: "The Moonlit Walk", 19: "The Ship's Bell", 20: "The Scent of Lavender",
    21: "The Spanish Coin", 22: "The Honest Fishermen", 23: "The Odd Glove", 24: "The Kite Festival",
    25: "The Teaspoon Thief", 26: "The Winning Ticket", 27: "The Silent Foghorn", 28: "Truth and Fib Night",
    29: "The Sugar Bowl", 30: "The Missing Sign",
}
TEASERS = {
    9: "A painting vanishes from the sea front, and one man's evening on the clifftop doesn't add up. Can you see why?",
    10: "A lifeboat collection box vanishes on a freshly painted afternoon. Three alibis, and one of them cracks.",
    11: "A silver brooch on a tea-room windowsill, four guests, four tables, and only a few muddled clues. Who sat by the window?",
    12: "The tea-room clock has stopped, a silver tea caddy has gone, and the milkman is sure of his times. Is he?",
    13: "A ship in a bottle disappears and a friendly note is left in its place. One little word gives the writer away.",
    14: "The village hall was locked, the window was whole, and the raffle hamper still vanished. Who knew the secret?",
    15: "A trophy is taken at dawn, a small blue car is spotted, and a ginger cat knows more than he lets on.",
    16: "A brass telescope vanishes in fifteen minutes flat. Three people, six sightings, steep paths. Who could make it?",
    17: "A silver thimble goes missing from a locked shop, and the only witness is a very clever parrot.",
    18: "A star chart disappears from a clifftop tent, and one stargazer's walk home sounds just a little too lovely.",
    19: "A brass ship's bell vanishes from a hook nobody can reach. So who did?",
    20: "A silver fountain pen is taken from a velvet drawer, and Agnes follows her nose. Can you?",
    21: "Six old Spanish coins are stolen, and one turns up somewhere very unexpected. Who spent it?",
    22: "A fishing net goes missing. Some fishermen always tell the truth, some never do. Can you untangle it?",
    23: "A rare orchid disappears on a bitter, windy night, and a single knitted glove is left behind.",
    24: "A carved wooden puffin vanishes at the kite festival, and one man's story goes against the wind.",
    25: "Silver teaspoons keep vanishing from a locked tea room, and nothing else is ever touched. Who's the thief?",
    26: "A winning raffle ticket blows away in a queue of five, and somebody else claims the prize. Who picked it up?",
    27: "A brass barometer disappears from a yacht in the night, and one visitor's story is full of fog.",
    28: "Truth and Fib Night: a chocolate cake vanishes and four suspects each tell one truth and one fib.",
    29: "A treasured book of sea shanties is taken from the vicar's study, and the tea tray tells all.",
    30: "On the Kettle and Gull's tenth birthday, Agnes's sign vanishes, and the note is written in green ink.",
}
LAST_CASE = 30
