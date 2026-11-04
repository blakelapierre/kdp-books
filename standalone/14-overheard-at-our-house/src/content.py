"""Words for Overheard at Our House. All prompts and lines are original to this book."""
TITLE = "Overheard at Our House"
SUBTITLE = "A Keepsake Journal of the Funny, Sweet and Surprising Things Our Kids Say"
TAGLINE = "A family keepsake journal"

CHAPTERS = [
    {"id": 1, "name": "Around the Kitchen Table", "art": "opener-1",
     "line": "Breakfast questions, dinner-table announcements and the things they said with their mouths full."},
    {"id": 2, "name": "On the Way There", "art": "opener-2",
     "line": "Car rides, walks to school and long waits in line, when small voices think out loud."},
    {"id": 3, "name": "Out in the Garden", "art": "opener-3",
     "line": "Mud, bugs, swings and sunshine, and everything they had to tell us about it."},
    {"id": 4, "name": "At Bedtime", "art": "opener-4",
     "line": "The big questions and quiet confessions that only come out after the light goes off."},
]

INTERLUDES = {
    1: ("They will not remember saying it. You will, if you write it down tonight.", "v-mug"),
    2: ("The best conversations happen when nobody is looking at anybody, only at the road ahead.", "v-car"),
    3: ("Every puddle is a discovery, and every discovery needs to be announced.", "v-bucket"),
    4: ("Some of the wisest things ever said were whispered by someone in pajamas.", "v-bed"),
}

# one prompt for each big-quote page: 9 per chapter, 36 in all, no repeats
PROMPTS = {
    1: ["Said at breakfast", "A dinner-table announcement", "Their opinion of a new food",
        "A question asked with a full mouth", "Their very own recipe", "Overheard while setting the table",
        "A birthday-cake moment", "What they said about grown-up coffee", "A kitchen-table deal they tried to make"],
    2: ["Said from the back seat", "Overheard at the shops", "On the walk to school",
        "A question about where we were going", "Their review of a long trip", "Said while waiting in line",
        "What they told a stranger", "A song they made up on the way", "Their idea of directions"],
    3: ["Said about a bug or a bird", "A puddle announcement", "Overheard on the swing",
        "Their plan for the garden", "What they said about the weather", "A treasure they found outside",
        "A conversation with the cat or dog", "At the park or the beach", "Their very own rule for a game"],
    4: ["Said in the bath", "A bedtime question", "Their excuse for staying up",
        "What they said about a dream", "A goodnight they made up", "Their idea of where the moon goes",
        "A quiet confession", "What they wished for", "The last thing they said tonight"],
}

# little sayings above the quick-entry pages (one per odd page, 36 in all)
QUICK_KICKERS = [
    "Little things, quickly written", "Before we forget", "Three more for the book", "Heard this week",
    "Overheard, word for word", "Said with total confidence", "Out of the mouths of babes", "Worth writing down",
    "Today's best lines",
]

INTRO = [
    "Children say the most wonderful things: wise, funny, sweet and completely unexpected. Then a week goes by, "
    "and the exact words are gone. This book is a place to catch them.",
    "Every even page holds <b>one big quote</b>, with room for who said it, how old they were, what was happening, "
    "and what you said back. Every odd page holds <b>three quick ones</b> for the days you only have a minute.",
    "The four chapters follow a family's day, from the kitchen table to bedtime, but you can write anywhere you like. "
    "Each big page has a small prompt at the top; treat it as a nudge, not a rule.",
    "Write the words exactly as they were said, mistakes and all. The mistakes are often the best part.",
    "At the back you will find a family dictionary for words only your house uses, pages for big questions, "
    "jokes and things they were absolutely sure of, room for whole conversations, and a letter to read when they are grown.",
    "There is space for more than one child, so brothers, sisters and cousins can share the book.",
]

SPEAKER_FIELDS = ["Name", "Nickname", "Born", "First word", "Favorite thing to say"]

BACK = {
    "dictionary": ("Our Family", "Dictionary", "Words and names only our family uses, and what they really mean."),
    "questions": ("Big Questions", "They Asked", "The questions that stopped us in our tracks, and how we tried to answer."),
    "sure": ("Things They Were", "Absolutely Sure Of", "Facts, according to them."),
    "jokes": ("Jokes", "They Told", "Write the joke, the punchline, and whether anyone understood it."),
    "talk": ("Conversations", "Worth Keeping", "Write down a whole back-and-forth, line by line."),
    "letter": ("", "A Letter for When You're Grown", "Write to them about the things they said, for when they are old enough to enjoy reading it."),
}

SURE_STARTS = ["Cats are really...", "When I grow up I will...", "Grown-ups always...", "The best food in the world is...",
               "The moon is made of...", "Dogs can...", "Babies come from...", "Our house is...", "Rain happens because...",
               "Money comes from...", "The oldest person in the world is...", "Teachers live...", "Bedtime is...",
               "The sky is blue because..."]

assert all(len(v) == 9 for v in PROMPTS.values())
_all = [p for v in PROMPTS.values() for p in v]
assert len(_all) == 36 and len(set(_all)) == 36, "prompts must be unique"
