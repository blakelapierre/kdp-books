"""Text content for Twenty-Five Christmases (all original to this edition)."""
TITLE = "Twenty-Five Christmases"
SUBTITLE = "A Family Christmas Memory Book to Fill In Year by Year: 25 Years of Traditions, Photos, Gifts and Moments to Keep"
TAGLINE = "a family Christmas memory book"
YEARS = 25

CHAPTERS = [
    {"id": 1, "years": (1, 5), "name": "Around the Tree", "art": "opener-1",
     "line": "The first five Christmases: the ornaments we chose, the gifts we wrapped and the people gathered close."},
    {"id": 2, "years": (6, 10), "name": "Down the Snowy Lane", "art": "opener-2",
     "line": "Christmases six to ten: lights in the windows, cold walks home and the neighbours at the door."},
    {"id": 3, "years": (11, 15), "name": "Warm from the Kitchen", "art": "opener-3",
     "line": "Christmases eleven to fifteen: cookies on the plate, the good dishes out, and too many cooks."},
    {"id": 4, "years": (16, 20), "name": "By the Fire", "art": "opener-4",
     "line": "Christmases sixteen to twenty: stockings on the mantel, long talks and the cat in the warmest spot."},
    {"id": 5, "years": (21, 25), "name": "Under the Christmas Stars", "art": "opener-5",
     "line": "Christmases twenty-one to twenty-five: the snowy cottage, the quiet night and everything we have kept."},
]

INTERLUDES = {
    1: ("Some years it snowed and some years it rained. What we remembered was who was sitting at the table.", "v-candles"),
    2: ("Every ornament on the tree has a story. This book is where the stories go.", "v-baubles"),
    3: ("The recipe card is stained, the handwriting is fading, and it is still the best part of the day.", "v-house"),
    4: ("Write it down tonight. Next year you will be glad you did, and in twenty years you will be grateful.", "v-stocking"),
    5: ("Twenty-five Christmases is a lifetime of small moments, and every one of them counted.", "v-globe"),
}

# one different question for each year
QUESTIONS = [
    "What new tradition did we try this year, and will we keep it?",
    "Who was the first one awake on Christmas morning?",
    "What was the most surprising gift under the tree?",
    "Which Christmas song did we hear (or sing) the most?",
    "Who told the best story at the table this year?",
    "What did we do on the days between Christmas and New Year?",
    "Which decoration came out of the box first, and who hung it?",
    "What was the most talked-about dish on the table?",
    "Who travelled the farthest to be with us?",
    "What made this Christmas different from last year?",
    "Which homemade gift or card do we want to remember?",
    "What did the youngest person at the table say that made everyone laugh?",
    "What did we bake, and did it turn out the way we hoped?",
    "Which game did we play, and who won?",
    "Who did we miss this year, and what do we remember about them?",
    "What small kindness did someone do for us this Christmas?",
    "Which Christmas film or story did we watch or read together?",
    "What was the weather really like, and did we go outside?",
    "What did we give to someone outside the family this year?",
    "What would we do exactly the same way next year?",
    "What is something new in the family since last Christmas?",
    "Which old tradition made us feel the most at home?",
    "What was the quietest, best moment of the season?",
    "What is the funniest thing that went wrong?",
    "Looking back over the years, what are we most thankful for?",
]

WEATHER = ["Snow", "Frost", "Rain", "Sunshine", "Grey skies", "Wind"]

TRADITIONS = [
    "Choosing and decorating the tree", "Hanging the stockings", "Advent calendar or candle",
    "Christmas cards and letters", "Baking cookies together", "A gingerbread house",
    "Christmas lights drive or walk", "A Christmas film night", "Singing carols",
    "Matching pajamas", "Opening one gift on Christmas Eve", "Reading a Christmas story",
    "Leaving cookies by the fire", "A special Christmas breakfast", "Giving to those in need",
    "A Christmas Day walk", "Games after dinner", "Calling faraway family",
]

MENU_ROWS = ["To start", "The main dish", "On the side", "Something sweet", "To drink"]
TREE_ROWS = ["Where the tree came from", "On the very top", "A new ornament this year"]


if __name__ == "__main__":
    assert len(QUESTIONS) == 25 and len(set(QUESTIONS)) == 25, "need 25 different yearly questions"
    assert len(CHAPTERS) == 5 and len(TRADITIONS) == len(set(TRADITIONS))
    print("content ok: 25 unique questions,", len(TRADITIONS), "traditions, 5 chapters")
