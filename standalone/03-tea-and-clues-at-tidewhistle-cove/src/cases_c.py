CASES_C = [
dict(title="The Spanish Coin", kind="story", culprit="Mr Nankervis",
suspects=["Mr Nankervis", "Demelza Rowe", "Pip Carew"],
clues=["float", "card", "change", "handful of coins"],
story="""
The little museum above the post office has a glass case of old coins that were washed up on Tidewhistle Cove beach over the years. The best of them were silver Spanish coins, worn smooth by the sea, with a crown stamped on one side.

On Wednesday night, someone lifted the lid of the case and took a small velvet bag holding six of them.

On Thursday morning, Jenna Tonkin opened up her ice cream van on the sea front at ten o'clock, as usual. Every evening Jenna empties her till completely and takes the money home. Every morning she fills it with a fresh float, a sealed bag of new coins from the bank, so that she can give change.

At eleven o'clock, she came hurrying into the Kettle and Gull, holding out something on her palm. It was a worn silver coin with a crown on one side.

"It was in my till," she said to Agnes Bell. "Right on top of the coins. I've only had three customers all morning, because of that sea mist. I remember every one."

Agnes poured her a cup of tea and asked her to go through them slowly.

"First was Demelza Rowe, for a lemon sorbet. She paid by tapping her card on my little machine. Second was Pip, for a double scoop of mint. He gave me a banknote, and I gave him his change out of the till. Third was Mr Nankervis, who's been staying at the inn. He had a vanilla cone, and he paid by counting out a handful of coins from his pocket."

"And you put his coins straight into the till?" asked Agnes.

"Straight in," said Jenna. "Without looking. I was busy with the cone."
""",
question="Who took the Spanish coins?",
solution="""
Mr Nankervis took the coins.

Jenna's till was empty overnight and started the day with a sealed bag of brand new coins from the bank, so the Spanish coin wasn't in it at opening time. It must have come in during the morning, from a customer.

Demelza paid by tapping her card, so she put no money into the till at all. Pip paid with a banknote, and the only coins involved went the other way, out of the till as his change. Mr Nankervis was the only customer who put coins into the till, counting out a handful from his pocket without Jenna looking. One of them was a Spanish coin from the museum.

Mr Nankervis turned out his pockets at the inn and found the velvet bag with the other five coins. He was a coin collector who had got carried away, and he said he had mixed one into his loose change by mistake and spent it on ice cream. He returned all six, and the museum, rather pleased by the story, now has a little card in the case about the most expensive vanilla cone in Tidewhistle Cove.
"""),

dict(title="The Honest Fishermen", kind="logic", culprit="Bran",
suspects=["Ned", "Bran", "Col"],
clues=["honest", "fibber"],
story="""
In Tidewhistle Cove they say there are two kinds of fishermen. There are honest ones, who tell the truth every time they open their mouths. And there are fibbers, who never tell the truth at all, not even about the weather. Every fisherman is one or the other, and nobody changes from one to the other.

Captain Quill's brand new fishing net had vanished from the harbour wall, and he was sure that one of three fishermen had taken it: Ned, Bran or Col. Exactly one of them took it.

Agnes Bell brought out a plate of saffron buns and asked each of them what they knew. She did not know which of them were honest and which were fibbers. There might be several fibbers, or just one, or none at all.

Ned said, "I didn't take the net. And Bran is a fibber."

Bran said, "Col took the net."

Col said, "Ned is an honest man. And I didn't take the net."

Agnes ate a whole saffron bun very slowly while she thought.

Here are the statements again. Ned: I didn't take it, and Bran is a fibber. Bran: Col took it. Col: Ned is honest, and I didn't take it. Each fisherman is either honest, so everything he says is true, or a fibber, so everything he says is false.
""",
question="Who took Captain Quill's net?",
solution="""
Bran took the net.

Start with Col. If Col were a fibber, both of his statements would be false. Then Ned would be a fibber, and Col would have taken the net. But if Ned were a fibber, his statement I didn't take the net would be false, which means Ned took it. Both Ned and Col can't have taken the net, so Col is not a fibber. Col is honest.

Since Col is honest, Ned is an honest man and Col didn't take the net. Since Ned is honest, Ned didn't take the net, and Bran is a fibber.

Bran is a fibber, so his statement Col took the net is false, which fits with what we already know. That leaves only one person who could have taken the net: Bran himself.

Bran had borrowed the net because his own was full of holes, and he had meant to bring it back before the captain noticed. Since he is a fibber, he naturally said it was nothing to do with him. Agnes made him mend his own net on the harbour wall that afternoon, where everyone could see him do it.
"""),

dict(title="The Odd Glove", kind="story", culprit="Mr Lanyon",
suspects=["Mr Lanyon", "Kerensa Hale", "Mr Fenwick"],
clues=["right hand", "anchors", "left hand"],
story="""
It was a bitter, windy evening, the kind when everyone in Tidewhistle Cove walks with their hands deep in their pockets.

Morwenna Day had been growing a rare white orchid on the back windowsill of her flower shop for three years, and it had just bloomed for the very first time. At closing time she went to the front to lock up, and when she returned to the back, the window was open and the orchid, pot and all, was gone.

Under the open window, on the cobbles outside, lay a single knitted glove. It was navy blue, for a right hand, with a pattern of little white anchors around the wrist.

Agnes Bell was passing on her way home, and Morwenna called her in. Together they looked up and down the lane. Three people were nearby.

Kerensa Hale was waiting at the bus stop, wearing a pair of navy gloves. They were plain, with no pattern at all, and she had one on each hand.

Mr Fenwick was locking up the grocer's next door. He wasn't wearing any gloves at all, and his fingers were red with the cold. "Never wear them," he said. "Can't count change in gloves."

The third was Mr Lanyon, a visitor, walking briskly down the lane. On his left hand he wore a navy knitted glove with a pattern of little white anchors around the wrist. His right hand was pushed deep into his coat pocket.

"Lost the other glove weeks ago," said Mr Lanyon, when Agnes asked. "Haven't seen it since."
""",
question="Who took the orchid?",
solution="""
Mr Lanyon took the orchid.

The glove under the window was for a right hand, navy blue, with a pattern of little white anchors. Mr Lanyon was wearing its partner, a navy left hand glove with exactly the same anchor pattern, and keeping his bare right hand in his pocket.

Kerensa was wearing both of her gloves, and they were plain, with no pattern. Mr Fenwick doesn't wear gloves at all. Neither of them could have dropped a patterned right hand glove.

Mr Lanyon had not lost the glove weeks ago. He had dropped it a few minutes earlier, while lifting the orchid through the window. The orchid turned up in a box on the back seat of his car, safe and sound. He was a passionate orchid grower and had driven three hundred miles to see it bloom. Morwenna let him take a cutting, properly, and he went home with the right glove back on his right hand.
"""),

dict(title="The Kite Festival", kind="story", culprit="Mr Penberthy",
suspects=["Mr Penberthy", "Pip Carew", "Tamsin Trevelyan"],
clues=["from the sea", "inland", "over the dunes"],
story="""
Every year, Tidewhistle Cove holds a kite festival on the long beach. This year the weather was perfect. All day a steady breeze blew in from the sea toward the land. The flags on the harbour wall stood straight out, pointing inland toward the hills. Every kite on the beach leaned the same way, out over the dunes, and when little Rosie Hale let go of her balloon it sailed away over the village toward the hills.

The prize for the best kite was a wooden puffin, beautifully carved and painted, and it stood on a table in the judges' tent, down by the water's edge.

At four o'clock, while the judges were out on the sand admiring a kite shaped like a lobster, the wooden puffin disappeared.

Agnes Bell was one of the judges, and she asked around.

Pip Carew had been flying his kite at the top of the beach, beside the dunes, with half his school class, and they all said he hadn't moved from that spot.

Tamsin Trevelyan had been selling books at a stall by the car park all afternoon, with a queue that never seemed to get any shorter.

Then there was Mr Penberthy, who had been seen hurrying away from the water's edge, near the judges' tent, at about four o'clock.

"Oh, I can explain that," said Mr Penberthy. "My kite string snapped. The kite flew off out over the sea, so I ran down to the water's edge after it. Lost it, I'm afraid. It's probably halfway to France by now."

Agnes looked at the flags on the harbour wall. They were still pointing toward the hills.
""",
question="What is wrong with Mr Penberthy's explanation?",
solution="""
Mr Penberthy took the wooden puffin.

All day the wind blew from the sea toward the land. The flags pointed inland, every kite leaned out over the dunes, and Rosie's balloon floated away over the village toward the hills. If Mr Penberthy's kite string really had snapped, his kite would have blown inland, over the dunes, not out to sea. He had no reason to run down to the water's edge, except to visit the judges' tent.

Pip had been at the top of the beach with his whole class, and Tamsin had been busy at her book stall by the car park. Mr Penberthy was the one person seen near the tent, with a story that the wind proved untrue.

The wooden puffin was in his kite bag, along with his kite, which had never broken at all. He said he had come second at the festival five years running and simply wanted the puffin on his mantelpiece just once. He was asked to return it, and then, as a kindly joke, he was given a special prize for the most imaginative kite story of the day.
"""),

dict(title="The Teaspoon Thief", kind="story", culprit="a magpie",
suspects=["Pip Carew", "Mr Fenwick", "Loveday Nance"],
clues=["patch of bright white", "Only the shiny things went", "hand's width"],
story="""
For three mornings in a row, a silver teaspoon went missing from the Kettle and Gull.

Every night, Agnes Bell lays out the tables for breakfast and leaves a tray of clean spoons on the sideboard under the back window. Then she locks both doors, and keeps the only keys in her apron pocket. The back window stays open at the top, just a hand's width, to let the kitchen air out. Nobody could squeeze through a gap that size, not even a small child.

On Monday morning, one silver teaspoon was gone from the tray. On Tuesday, another. On Wednesday, a third, and also a scrap of shiny silver foil from a chocolate wrapper that Pip had left on the sideboard.

Strangely, other things on the same sideboard were never touched. There was a jar of coins for the lifeboat. There were wooden spoons, and a dull old pewter spoon. There was a sugar bowl, and a whole plate of shortbread under a cloth. Only the shiny things went.

Agnes's three regular early helpers were all a little offended to be asked. Pip pointed out that he couldn't stand teaspoons and only ever used a big spoon. Mr Fenwick said he'd been at the grocer's from five each morning, which his delivery driver confirmed. Loveday said she had been at home in bed, and so had Pickle the terrier, and neither of them had keys.

On Wednesday, Agnes found something on the back windowsill, just under the gap at the top of the window. It was a long, glossy feather, black, with a patch of bright white near the end.
""",
question="Who has been taking the teaspoons?",
solution="""
None of the suspects took the spoons. The thief was a magpie.

The doors were locked every night and Agnes had the only keys. The only way in was the gap at the top of the back window, just a hand's width, far too small for any person. But it was plenty of room for a bird.

The thief took only shiny things: silver spoons and a scrap of silver foil. It ignored the coins in the jar, the dull pewter spoon, the wooden spoons and even the shortbread. Magpies are famous for snatching small, bright, shiny objects. And on the windowsill, right under the gap, was a glossy black feather with a patch of white, which is exactly what a magpie feather looks like.

Pip climbed the old apple tree behind the tea room, very carefully, and found a messy nest of twigs. In it were three silver teaspoons, a scrap of foil, two bottle tops, and a shiny button that Loveday had lost in the spring. Agnes now closes the back window at night and leaves a bottle top on the garden wall for the magpie, by way of a thank you for the excitement.
"""),

dict(title="The Winning Ticket", kind="logic", culprit="Demelza Rowe",
suspects=["Mr Fenwick", "Loveday Nance", "Pip Carew", "Demelza Rowe", "Hedley Truscott"],
clues=["directly behind her", "very front", "exactly in the middle"],
story="""
At the summer fair, the raffle prize was a hamper so large it took two people to lift it. Loveday Nance bought a single raffle ticket, tucked it into the top of her basket, and joined the queue at the tea stall.

Five people stood in that queue, one behind the other. A moment later a gust of wind lifted the ticket out of Loveday's basket, and it fluttered to the ground behind her. It was picked up by the person standing directly behind her.

At three o'clock, the vicar drew the winning number. It was Loveday's number. But the ticket was handed in, and the hamper claimed, by somebody else.

Loveday couldn't remember exactly who had been behind her, because she had been talking about Pickle the whole time. The five people in the queue were Mr Fenwick, Loveday herself, Pip Carew, Demelza Rowe and Hedley Truscott. Agnes Bell, who had been serving the tea, remembered a few things.

"Mr Fenwick was at the very front," said Agnes. "Hedley was somewhere behind Pip. Loveday was exactly in the middle of the queue. And Demelza wasn't last, and she wasn't standing right next to Mr Fenwick."

Here are Agnes's clues again. There were five people in a single queue. Mr Fenwick was at the front. Hedley was somewhere behind Pip. Loveday was exactly in the middle. Demelza was not last, and not right next to Mr Fenwick.
""",
question="Who was standing directly behind Loveday and picked up the ticket?",
solution="""
Demelza Rowe picked up the ticket.

Number the places from the front. Mr Fenwick was first. With five people, the middle place is the third, so Loveday was third.

That leaves the second, fourth and fifth places for Pip, Demelza and Hedley. Demelza wasn't last, so she wasn't fifth. She wasn't right next to Mr Fenwick, so she wasn't second. So Demelza was fourth, directly behind Loveday.

That leaves Pip and Hedley for the second and fifth places, and since Hedley was behind Pip, Pip was second and Hedley was fifth.

Demelza went very pink. She said she had seen a ticket on the ground, picked it up, and honestly thought it might be one she'd bought earlier and forgotten. When the number was called, she got carried away by the sight of the hamper. She handed it straight over to Loveday, who opened it there and then and shared the shortbread with the whole queue.
"""),

dict(title="The Silent Foghorn", kind="story", culprit="Mr Keast",
suspects=["Mr Keast", "Captain Quill", "Tamsin Trevelyan"],
clues=["foghorn", "never sounded", "clear"],
story="""
At the end of the harbour wall in Tidewhistle Cove stands the foghorn. Whenever fog rolls in over the bay, it sounds all by itself, a deep, mournful boom every half a minute, until the fog clears. You can hear it from every house in the village. People say it could wake a sleeping walrus, though Agnes Bell says it only ever wakes the cat.

On Tuesday night, Agnes had a cold and couldn't sleep. She sat up in bed with her window open, reading a book and drinking honey and lemon, from ten o'clock until three in the morning. The night was clear and starry, and the foghorn never sounded once.

On Wednesday morning, the yacht moored in the middle of the bay was missing its brass barometer. Somebody had rowed out to it during the night in a dinghy, and left the dinghy tied up on the wrong side of the jetty.

Captain Quill had been on night watch at the harbour office, with two lifeboat crew members, from ten o'clock until dawn. Tamsin Trevelyan had been at her sister's in town and caught the first bus back in the morning.

Then there was Mr Keast, a visitor, who had been admiring the yacht's brass fittings all week.

"I was at home all night," said Mr Keast. "Couldn't have gone out on the water if I'd wanted to. The fog was so thick you couldn't see your hand in front of your face. That foghorn kept me awake half the night, booming away."
""",
question="How does Agnes know Mr Keast's story is false?",
solution="""
Mr Keast took the barometer.

He said thick fog rolled in, and that the foghorn kept him awake booming half the night. But the foghorn sounds by itself whenever there is fog in the bay, and you can hear it from every house in the village. Agnes was awake with her window open from ten until three, and the night was clear and starry, and the foghorn never sounded once. There was no fog, and no booming. Mr Keast invented a foggy night to explain why he couldn't have rowed out to the yacht.

Captain Quill was on watch with two crew members all night, and Tamsin was in town. Mr Keast was the only one whose story didn't fit the night.

The barometer was in his suitcase, wrapped in a towel. He confessed that he collected old weather instruments, and returned it with a very red face. Agnes says that next time he makes up a story about the weather, he should check the weather first.
"""),

dict(title="Truth and Fib Night", kind="logic", culprit="Tamsin Trevelyan",
suspects=["Hedley Truscott", "Kerensa Hale", "Wenna Polglaze", "Tamsin Trevelyan"],
clues=["one truth and one fib"],
story="""
Every year on the first of April, the village hall holds Truth and Fib Night. The rule is very simple, and everyone sticks to it all evening, because it's the whole point of the game. Whenever anyone says two things in a row, exactly one of them must be true, and exactly one must be a fib.

This year, the prize for the best fib of the night was a magnificent chocolate cake, baked by Jago Penhallow and decorated with a sugar fish. Halfway through the evening, the cake vanished from the prize table.

Four people had been near the prize table at the time: Hedley Truscott, Kerensa Hale, Wenna Polglaze and Tamsin Trevelyan. Exactly one of them took the cake.

Agnes Bell, who was running the game, asked each of them to tell her two things, by the rules of the night.

Hedley said, "I didn't take the cake. Kerensa took it."

Kerensa said, "I didn't take the cake. Wenna took it."

Wenna said, "I didn't take the cake. Hedley took it."

Tamsin said, "I didn't take the cake. And it wasn't Wenna."

Agnes smiled. She loves Truth and Fib Night.

Here are the statements again. Hedley: I didn't take it, Kerensa took it. Kerensa: I didn't take it, Wenna took it. Wenna: I didn't take it, Hedley took it. Tamsin: I didn't take it, it wasn't Wenna. Each person told exactly one truth and one fib.
""",
question="Who took the chocolate cake?",
solution="""
Tamsin Trevelyan took the cake.

Each person said I didn't take the cake, and then one more thing. Anyone who is innocent is telling the truth with their first statement, so their second statement must be the fib. The one who took the cake is fibbing with the first statement, so their second statement must be true.

Suppose Hedley took it. Then Wenna's second statement, Hedley took it, would be true, while her first, I didn't take it, would also be true. Two truths breaks the rule. So it wasn't Hedley.

In the same way, if Kerensa took it, Hedley would be telling two truths. And if Wenna took it, Kerensa would be telling two truths. So it wasn't Kerensa or Wenna either.

That leaves Tamsin. Her first statement, I didn't take the cake, is the fib. Her second, it wasn't Wenna, is true. Everyone else's second statement is a fib. It all fits.

Tamsin laughed and fetched the cake from under the stage. She had hidden it there, she said, so that she could claim she had told the best fib of the night. Agnes agreed that it had been a very good one, and the cake was shared out among everybody in the hall.
"""),

dict(title="The Sugar Bowl", kind="story", culprit="Mr Bolitho",
suspects=["Mr Bolitho", "Captain Quill", "Loveday Nance"],
clues=["three sugars", "no milk", "twelve lumps"],
story="""
Agnes Bell has served tea in Tidewhistle Cove for ten years, and she knows how every single person in the village takes it. She never needs to ask.

On Saturday afternoon, the vicarage opened its gardens to visitors. In the vicar's study, on a little stand by the window, lay the church's oldest treasure, a tiny hand written book of sea shanties more than two hundred years old.

The vicar's housekeeper had taken a tray of tea into the empty study at two o'clock, to have it ready for the vicar. On the tray was a pot of tea, a jug of milk, a cup, and a sugar bowl. She always fills the sugar bowl with exactly twelve lumps, she said, no more and no fewer, because the vicar is trying to cut down.

At three o'clock, the shanty book was gone. The pot had been used. The cup was half full of dark tea with no milk in it at all, and the milk jug was still full. In the sugar bowl, only nine lumps were left.

The vicar takes his tea with milk and no sugar, and he had been out in the garden all afternoon. The housekeeper never drinks tea at all, only cocoa.

Three visitors had been seen going in and out of the vicarage that afternoon.

"Captain Quill?" said Agnes, when the vicar listed them. "He takes it strong, with plenty of milk, and no sugar. Loveday Nance takes hers with milk and one sugar. And Mr Bolitho, the gentleman staying at the inn, takes his black, with three sugars. He's had tea at my place every day this week."
""",
question="Who took the book of sea shanties?",
solution="""
Mr Bolitho took the book.

Whoever sat in the study and helped themselves to tea left a cup of dark tea with no milk, and the milk jug was untouched. The sugar bowl started with exactly twelve lumps and was down to nine, so three lumps had gone. Someone drank tea black, with three sugars.

Captain Quill takes his with plenty of milk and no sugar, and Loveday with milk and one sugar. The vicar takes milk and no sugar, and the housekeeper doesn't drink tea at all. Only Mr Bolitho takes his tea black, with three sugars.

When Agnes put this to him over the counter of the Kettle and Gull, Mr Bolitho sighed into his cup. He was a singer of sea shanties, he said, and had only meant to copy out a song or two, but he could not resist taking the book. He returned it to the vicar that evening, and on Sunday he sang three shanties from it in church, beautifully, to make up for it.
"""),

dict(title="The Missing Sign", kind="story", culprit="Constable Ollie Penrose",
suspects=["Hedley Truscott", "Tamsin Trevelyan", "Constable Ollie Penrose"],
clues=["green ink", "paper bag", "back soon"],
story="""
On the morning of the Kettle and Gull's tenth birthday, Agnes Bell came downstairs, opened the front door, and stopped.

Her sign was gone.

It was a painted wooden sign showing a kettle and a seagull, and it had hung above the door on its iron bracket for ten years. Now the bracket was empty. On the doorstep sat a small brown paper bag. Inside were the four brass bolts that had held the sign up, and on the outside of the bag, someone had written two words: Back soon.

The words were written in bright green ink.

Agnes sat down on her doorstep and thought about who might have done such a thing.

Hedley Truscott owned the tallest ladder in Tidewhistle Cove. But Hedley always wrote in pencil, which he kept behind his ear, and he had lost his last pen years ago.

Tamsin Trevelyan wrote more than anyone in the village, with labels and posters and signs. But Tamsin wrote only in blue ink, with a fountain pen. She said green ink gave her a headache.

And there was Constable Ollie Penrose. Ollie writes everything in his notebook in green ink, with a fat green pen that once belonged to his grandfather, who was also the village constable. He says it's a family tradition. Everybody in the village has seen it.

Agnes looked at the green writing again. Then she looked up the street, and saw that the lights were on in the village hall, very early indeed for a Saturday morning.
""",
question="Who took the sign, and why?",
solution="""
Constable Ollie Penrose took the sign.

The note on the bag of bolts was written in green ink. Hedley only ever writes in pencil and has no pen, and Tamsin writes only in blue. Ollie writes everything in green ink, with his grandfather's fat green pen, and the whole village knows it.

When Agnes walked up the street to the village hall, she found Ollie inside, with Hedley and his tall ladder, Tamsin with a pot of paint, Demelza with her brushes, Jago with a cake, and what seemed to be half of Tidewhistle Cove. Ollie had borrowed the sign at dawn, because Demelza wanted to repaint it as a surprise for the tea room's tenth birthday. They had put the bolts in a bag and left the note so that Agnes wouldn't worry.

The sign went back up that afternoon, with the kettle shining and the seagull's feathers bright as new. Painted underneath, in small letters, it now says: Ten years of tea and clues. Agnes says it is the best mystery she has ever solved. She has been asked to judge the baking again next year.
"""),
]
