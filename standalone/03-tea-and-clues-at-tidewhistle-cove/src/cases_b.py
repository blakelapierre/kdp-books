CASES_B = [
dict(title="The Window Table", kind="logic", culprit="Captain Quill",
suspects=["Mr Spargo", "Loveday Nance", "Captain Quill", "Wenna Polglaze"],
clues=["four little tables in a row", "window table"],
story="""
The Kettle and Gull has four little tables in a row, running from the door at one end to the big bay window at the other. Agnes Bell calls them the first, second, third and fourth tables, counting from the door, so the fourth table is the window table.

On Wednesday, Kerensa Hale came in early for a pot of tea. She took off her silver seagull brooch to polish it, set it on the windowsill beside the window table, and then hurried out without it when she saw her bus. The windowsill can only be reached from the window table itself. To reach it from anywhere else, you would have to climb over the window table.

Four guests had lunch that day, one at each table, and none of them got up from their seats until they left. When Kerensa came rushing back at two o'clock, the brooch was gone.

Agnes had spent the whole lunchtime in the kitchen with a tray of pasties, and young Pip Carew had done the serving. Pip couldn't remember exactly who sat where, but he did remember a few things.

"Captain Quill sat at a table right next to Wenna's," he said. "Loveday wasn't at either end of the row. Mr Spargo sat closer to the door than Captain Quill did. And I'm sure that Wenna wasn't at the window table, because she complained that she couldn't see the boats."

Agnes wiped the flour off her hands and drew four little squares in her mind.

Here are Pip's clues again. Captain Quill sat right next to Wenna. Loveday was not at either end. Mr Spargo sat closer to the door than Captain Quill. Wenna was not at the window table. The four guests were Mr Spargo, Loveday, Captain Quill and Wenna, one at each table.
""",
question="Who sat at the window table and has the brooch?",
solution="""
Captain Quill sat at the window table, so he has the brooch.

Loveday was not at either end, so she was at the second or third table.

Suppose Loveday was at the third table. Wenna was not at the window table, so she was at the first or second. If Wenna was at the first table, Captain Quill had to be beside her at the second, and Mr Spargo would be left with the window table, which is further from the door than the captain. That breaks a clue. If Wenna was at the second table, the captain had to be at the first, beside her, and again Mr Spargo would be at the window, further from the door. That breaks the same clue. So Loveday was not at the third table.

So Loveday was at the second table. Wenna can't be at the window, and if she were at the first table, the captain would have to be at the second, which is Loveday's. So Wenna was at the third table, the captain was beside her at the window table, and Mr Spargo was at the first table, closest to the door.

Captain Quill turned out his coat pocket and there was the seagull brooch. A gust of wind had come in through the open window, and he had pocketed the brooch to stop it from blowing into the harbour, and then he had forgotten all about it. He was very embarrassed, and paid for Kerensa's next pot of tea.
"""),

dict(title="The Stopped Clock", kind="story", culprit="Mr Prowse",
suspects=["Mr Prowse", "Demelza Rowe", "Hedley Truscott"],
clues=["ten to nine", "stopped", "clock"],
story="""
The big clock on the wall of the Kettle and Gull is older than Agnes Bell's grandmother. On Monday morning it gave a tired little click and stopped quite still at ten to nine. Agnes sent for the clockmaker from town, but he could not come until Friday. So all week, the clock's hands pointed to ten to nine.

"You'll have to tell the time by your stomachs," Agnes told her customers, and they all laughed.

On the shelf behind the counter, Agnes kept her collection of antique tea caddies. The finest of them was a little silver one shaped like an acorn. On Thursday at half past three she dusted it, and it was there. At half past four she noticed it was gone.

Three people had been in the tea room on Thursday afternoon.

Demelza Rowe had come in at a quarter past three to drop off some paintings, and left straight away. At half past three she was at the sea front with Captain Quill, and they stayed together all afternoon.

Hedley Truscott had fixed a squeaky door hinge at three o'clock and gone home. His wife said he had been asleep in his armchair from twenty past three until supper time, snoring loud enough to rattle the windows.

Mr Prowse, who delivers the milk, had brought the afternoon crate.

"I wasn't here anywhere near half past three," said Mr Prowse. "I dropped the crate at the back door, popped my head in, and looked up at your clock. It said a quarter past three, so I knew I was running early. I was gone a couple of minutes later."

Agnes looked up at her clock. It said ten to nine, as it had all week.
""",
question="How does Agnes know Mr Prowse is not telling the truth?",
solution="""
Mr Prowse took the silver acorn caddy.

He said he had looked at the tea room clock and seen that it was a quarter past three. But the clock had been stopped at ten to nine since Monday. It could not have said a quarter past three on Thursday. Mr Prowse had made up the time to make it sound as if he had left before the caddy disappeared.

Demelza had left before half past three and was with Captain Quill, and Hedley was asleep at home. Only Mr Prowse had been at the tea room after half past three.

He confessed with a hang of the head. He collected acorns of every kind, he said, and the little silver one had been calling to him for months. He gave it back, and Agnes, who believes in second chances, still lets him deliver the milk. She has, however, moved the caddy to a higher shelf.
"""),

dict(title="The Misspelled Note", kind="story", culprit="Hedley Truscott",
suspects=["Hedley Truscott", "Tamsin Trevelyan", "Jago Penhallow"],
clues=["p, e, i, r", "spelled pier", "sign"],
story="""
Down by the slipway there is a hand painted sign that says No Parking on the Pier. At least, that is what it means to say. Hedley Truscott painted it himself last spring, and he spelled pier p, e, i, r. Agnes Bell has pointed this out to him at least four times.

"I before E, Hedley," she reminds him. "P, i, e, r."

"Looks right to me," says Hedley, every time.

Captain Quill's most treasured possession is a ship in a bottle, a tiny three masted sailing ship with sails no bigger than a fingernail. It sits on a shelf in his harbour office. On Friday afternoon, the shelf was empty, and in the ship's place was a folded note.

The note said: Don't worry. Your ship will be back by the peir at sunset. And the word pier was spelled p, e, i, r.

Captain Quill brought the note straight to the Kettle and Gull. Agnes read it twice.

Three people had been in and out of the harbour office that afternoon. Tamsin Trevelyan had dropped off a book about knots. Jago Penhallow had delivered a pasty. And Hedley had been fixing a loose board in the office floor.

Tamsin had just finished writing a poster for her shop window. It said Story Time on the Pier, Saturday, and the word pier was spelled perfectly. Jago's chalkboard outside the bakery said Pasties, Two Doors from the Pier, and Jago had spelled it perfectly too.
""",
question="Who left the note and borrowed the ship in a bottle?",
solution="""
Hedley Truscott borrowed the ship in a bottle.

The note spelled pier as p, e, i, r. That is exactly the mistake on Hedley's sign by the slipway, the one Agnes has corrected again and again, and which Hedley still thinks looks right. Tamsin's poster and Jago's chalkboard both spelled pier correctly that very same day.

When Agnes showed Hedley the note, he grinned sheepishly. Captain Quill's birthday was on Sunday, and Hedley had been building him a second, bigger ship in a bottle as a present. He needed the original to copy the rigging. He had left the note so the captain wouldn't worry.

At sunset, the ship was back on the pier, just as promised. On Sunday, the captain received a second one, slightly lopsided and absolutely beautiful. The card that came with it, Agnes noticed, said Happy Birthday from Hedley, Down by the Peir.
"""),

dict(title="The Blue Ribbon Key", kind="story", culprit="Mr Spargo",
suspects=["Mr Spargo", "Demelza Rowe", "Pip Carew"],
clues=["blue ribbon", "plant pot", "except that the spare key was still there"],
story="""
The village hall in Tidewhistle Cove has a spare key. It is hidden under the big terracotta plant pot beside the front door, and it hangs on a short blue ribbon so it is easy to find in the dark. Only the hall committee knows about it, and Agnes Bell is on the hall committee.

On Saturday night, the raffle prize for the summer fair went missing from the locked hall. It was a large wicker hamper full of jams, chutneys and a whole Cornish cheese. There was no sign of a broken window or a forced door. Whoever took it had let themselves in with a key, and locked the door again on the way out.

On Sunday morning, Constable Ollie Penrose lifted the plant pot, looked underneath, and set it down again. He didn't say anything about what he'd seen, except that the spare key was still there.

He and Agnes then spoke to three people who had been helping set up the fair on Saturday afternoon.

Demelza Rowe said that she had left at five o'clock and gone straight to her sister's for supper. Her sister confirmed it.

Pip Carew said that he had gone home at six and had no idea there was a spare key at all.

The third was Mr Spargo, who had been building the tombola stall.

"A spare key? Under a plant pot?" said Mr Spargo, shaking his head. "I had no idea. And I'm sure I'd remember a key on a blue ribbon like that. Honestly, Constable, I never knew it existed."

Ollie and Agnes looked at each other.
""",
question="What gave Mr Spargo away?",
solution="""
Mr Spargo took the hamper.

He said he had never known there was a spare key under the plant pot. But in the same breath he described it as a key on a blue ribbon. Ollie had only said that the spare key was still there. Nobody had mentioned the ribbon. The only people who know about the ribbon are the hall committee, and whoever has actually lifted that pot and used the key.

Pip, on the other hand, didn't seem to know anything about the key at all, and Demelza had been at her sister's.

Mr Spargo had watched a committee member fetch the key on Saturday afternoon. He came back after dark, let himself in, and took the hamper home. He returned it, a little lighter by one jar of strawberry jam, and bought a whole book of raffle tickets by way of apology. The hall committee now hides the key somewhere else, and Agnes isn't saying where.
"""),

dict(title="The Warm Bonnet", kind="story", culprit="Mr Treloar",
suspects=["Mr Treloar", "Mr Fenwick", "Kerensa Hale"],
clues=["Biscuit", "warm", "bonnet"],
story="""
Biscuit is the ginger cat who lives at the Kettle and Gull. He is fat, lazy and very wise. He has one great passion in life, apart from sardines. On a chilly morning, he seeks out any car whose engine has been running recently, climbs onto the bonnet, and curls up on the warm metal like a loaf of bread.

It was a chilly, grey morning in late September, with a sharp wind off the sea.

At seven o'clock that morning, somebody slipped into the sailing club in Polwhele, the next village along the coast, a ten minute drive away, and took the silver sailing trophy from the club's cabinet. A fisherman saw a small blue car driving away from Polwhele at a quarter past seven, heading in the direction of Tidewhistle Cove.

Three people in Tidewhistle Cove owned small blue cars.

Mr Fenwick's car had a flat tyre and had been up on bricks outside the grocer's for a week. Kerensa Hale's car was parked outside her cottage with a thick layer of overnight dew on its windscreen, untouched.

At half past seven, Agnes Bell walked to the end of the street to fetch the milk, and found the third car outside Mr Treloar's house. Biscuit was curled up on its bonnet, purring, with his eyes shut tight.

Mr Treloar came to the door in his dressing gown.

"My car? It hasn't moved since last night," he said. "I've been at home all morning with my newspaper. Haven't been out at all."

Agnes rested her hand on the bonnet, beside the cat. It was warm.
""",
question="Why does Agnes not believe Mr Treloar?",
solution="""
Mr Treloar took the trophy.

On a chilly morning, Biscuit always looks for a car whose engine has just been running, because the bonnet is warm. At half past seven he was curled up on Mr Treloar's car, and when Agnes touched the bonnet it was warm. A car that had stood still all night in that sharp sea wind would have been as cold as the morning. Mr Treloar's car had been driven very recently, which fits the blue car leaving Polwhele at a quarter past seven.

Mr Fenwick's car was up on bricks with a flat tyre, and Kerensa's car was still covered in untouched overnight dew. Neither of them had moved.

Mr Treloar admitted that he had come second in the sailing race four years in a row, and just wanted to know how it felt to hold the trophy. He drove it back to Polwhele that afternoon. Biscuit, who did not care about any of this, went back to sleep on the bonnet until it cooled.
"""),

dict(title="The Lighthouse Path", kind="logic", culprit="Mr Opie",
suspects=["Wenna Polglaze", "Mr Opie", "Pip Carew"],
clues=["fifteen minutes", "twenty minutes", "ten minutes"],
story="""
The old lighthouse on the point is a little museum now, and Hedley Truscott is its keeper. In the lamp room at the top stands a polished brass telescope that once belonged to the very first lighthouse keeper.

On Tuesday at two o'clock exactly, Hedley climbed out onto the gallery to clean the windows. At a quarter past two he came back in. In those fifteen minutes, the telescope disappeared.

Three people had been seen around the village that afternoon, and each of them had been seen twice.

Wenna Polglaze was seen in the Kettle and Gull at two o'clock, and again at twenty past two.

Mr Opie, a visitor with binoculars always around his neck, was seen at the harbour at a quarter to two, and again at half past two.

Pip Carew was seen in the bookshop at five to two, and again at ten past two.

The paths up to the point are steep and rocky. Everybody in Tidewhistle Cove agrees on these times, and agrees that nobody could possibly do the journeys any faster. From the Kettle and Gull to the lighthouse is fifteen minutes. From the harbour to the lighthouse is twenty minutes. From the bookshop to the lighthouse is ten minutes. Each journey takes exactly as long going back down as it does going up.

Agnes Bell took out a pencil and an old receipt, then put the pencil down and decided to do it in her head instead.

Here is the puzzle again. The telescope vanished between two o'clock and a quarter past two. Wenna was at the tea room at two and at twenty past, fifteen minutes from the lighthouse. Mr Opie was at the harbour at a quarter to two and at half past, twenty minutes from the lighthouse. Pip was at the bookshop at five to two and at ten past, ten minutes from the lighthouse.
""",
question="Who is the only person who could have reached the lighthouse in time to take the telescope?",
solution="""
Mr Opie took the telescope.

Take Wenna first. She was at the tea room at two o'clock, so the earliest she could reach the lighthouse was a quarter past two, just as Hedley came back in. And to be back at the tea room by twenty past two, she would have had to leave the lighthouse by five past two. She can't arrive at a quarter past and leave at five past, so it wasn't Wenna.

Now Pip. He was at the bookshop at five to two, so the earliest he could reach the lighthouse was five past two. But to be back in the bookshop by ten past two, he would have had to leave the lighthouse by two o'clock. He can't arrive at five past and leave at two, so it wasn't Pip.

Now Mr Opie. He left the harbour at a quarter to two at the earliest, so he could have reached the lighthouse by five past two. To be back at the harbour by half past two, he only needed to leave the lighthouse by ten past two. That gives him five minutes in the lamp room while Hedley was out on the gallery. He is the only one who could have done it.

Mr Opie was a keen collector of anything to do with lighthouses, and he admitted that the telescope had been too much for him. He returned it, and Hedley now lets him look through it, under supervision, every Tuesday at two.
"""),

dict(title="The Talking Parrot", kind="story", culprit="Mr Pascoe",
suspects=["Mr Pascoe", "Tamsin Trevelyan", "Mr Fenwick"],
clues=["mind how you go, my lovely", "parrot", "picks up"],
story="""
Mr Pascoe the window cleaner has been cleaning the windows of Tidewhistle Cove for twenty years, and he has said the same thing to every customer on every single visit. Agnes Bell heard it again that very morning, as he climbed down his ladder outside the Kettle and Gull.

"Mind how you go, my lovely," he said, tipping his cap. "Mind how you go."

Nobody else in Tidewhistle Cove ever says it. People tease Mr Pascoe about it, and he just laughs and says it again.

Wenna Polglaze runs the little antique shop on the corner, and she shares it with an elderly grey parrot called Admiral. Admiral is a very clever bird. He picks up any phrase he hears said a few times in a row, and then repeats it for days. At the moment, he knows how to say Good morning, Pieces of eight, and Wenna's own favourite saying, Put the kettle on.

On Thursday afternoon Wenna popped out for half an hour, leaving the shop locked and Admiral on his perch. Three people had keys to the shop, because each of them sometimes looked after it for her: Tamsin Trevelyan, Mr Fenwick, and Mr Pascoe, who cleaned the inside windows once a month.

When Wenna came back, her antique silver thimble was gone from the counter. And Admiral was bobbing up and down on his perch, saying something he had never said before.

"Mind how you go, my lovely!" he squawked. "Mind how you go! Mind how you go, my lovely!"

Wenna stopped in the doorway with her mouth open.

When Agnes asked around, Tamsin said she had been in her own shop all afternoon, and Mr Fenwick said he had been at the grocer's. All three keyholders said they had not been in Wenna's shop that day.
""",
question="Who took the silver thimble?",
solution="""
Mr Pascoe took the thimble.

Admiral only picks up a phrase when he hears it said several times in a row. When Wenna left, he didn't know the phrase mind how you go, my lovely. When she came back half an hour later, he couldn't stop saying it. So somebody had been in the shop with him that half hour, saying it over and over.

Mind how you go, my lovely is the phrase Mr Pascoe has said to every customer for twenty years, and the one Agnes heard him say twice that very morning. Mr Pascoe also had a key, so the locked door was no obstacle.

Mr Pascoe confessed. He had dropped in to clean the windows a day early, chatted away to Admiral while he worked, and then the thimble had caught his eye. His late mother had owned one just like it. He gave it back, and Wenna, quite touched, let him buy it at a very kind price. Admiral still says mind how you go, my lovely, to every customer who walks out the door.
"""),

dict(title="The Moonlit Walk", kind="story", culprit="Miss Clemo",
suspects=["Miss Clemo", "Demelza Rowe", "Captain Quill"],
clues=["new moon", "darkest night", "New moon this Saturday"],
story="""
The Tidewhistle Cove Gazette comes out every Friday, and Agnes Bell reads it cover to cover over her breakfast. This week, the back page had a little notice from the stargazing club.

New moon this Saturday, it said. The darkest night of the month. Perfect for spotting meteors. Bring a blanket and a flask.

On Saturday evening, the stargazing club met on the clifftop with their telescopes. They had a special guest, Miss Clemo, an astronomer from the city who was staying at the inn. The club had borrowed a beautiful antique star chart from the museum to show her, and it was spread out on a little table in the club's tent.

At eleven o'clock, everyone went outside to look at the sky. At midnight, when they came back into the tent, the star chart was gone.

On Sunday morning, Agnes and Constable Ollie Penrose spoke to the people who had left the clifftop early.

Demelza Rowe had left at half past ten, before the chart went missing. Captain Quill had walked her home, and they both arrived at Demelza's cottage before eleven.

Miss Clemo had left the clifftop at about a quarter past eleven, saying she was tired.

"I walked back to the inn along the cliff path," said Miss Clemo. "It was such a lovely night. The moon was full and bright, so bright I could see every pebble on the path without a torch. I never went back into the tent."

Agnes thought of the little notice on the back page of the Gazette.
""",
question="Why does Agnes doubt Miss Clemo's story?",
solution="""
Miss Clemo took the star chart.

The Gazette said Saturday was a new moon, the darkest night of the month. On a new moon there is no moonlight at all. Miss Clemo said she walked home under a full, bright moon that lit every pebble on the path. That could not have been true on Saturday night. She made up her walk home.

Demelza and Captain Quill had left together before eleven, while the chart was still on the table. Miss Clemo was the one who left alone after everyone had gone out to look at the sky, and the one whose story did not fit the night.

Miss Clemo blushed and admitted that she had slipped back into the tent and rolled up the chart, because she had never seen one quite so old and wanted to study it properly. Being an astronomer, she said, she really ought to have known what phase the moon was in. The chart was returned to the museum, and Miss Clemo gave the stargazing club a free talk about the moon.
"""),

dict(title="The Ship's Bell", kind="story", culprit="Tobias Ferris",
suspects=["Tobias Ferris", "Loveday Nance", "Mr Fenwick"],
clues=["hook so high", "tiptoe", "stepladder"],
story="""
Above the door of the sailing club hangs a brass ship's bell, rung for the start of every race. It hangs on a hook so high above the door that, as everyone in Tidewhistle Cove likes to say, even the tallest person in the village has to stretch up on tiptoe to reach it.

The tallest person in the village is Tobias Ferris, who is on the lifeboat crew. He is six and a half feet tall and has to duck through most doorways.

The club's stepladder lives in a cupboard that is kept locked, and Agnes Bell, who is the club treasurer, keeps the only key on her own key ring. On Sunday the cupboard was still locked, and the ladder was still inside. There was no other furniture in the porch to stand on, only a tiny wooden stool that had been broken for months.

On Sunday morning, the bell was gone from its hook.

Three people had been at the club on Saturday evening for the quiz night.

Loveday Nance is a little over five feet tall. She said she had been at the quiz table all evening, and that she couldn't reach that hook if she stood on a chair.

Mr Fenwick is not much taller than Loveday. He said he had left early with a headache.

Tobias said he had been at the quiz too, and had gone home at ten.

"I didn't touch the bell," said Tobias. "I hardly ever even notice it."

Agnes jingled her key ring and looked up at the empty hook.
""",
question="Who took the ship's bell?",
solution="""
Tobias Ferris took the bell.

The hook is so high that even the tallest person in the village has to stretch on tiptoe to reach it, and the tallest person in the village is Tobias. Loveday and Mr Fenwick are both much shorter, and there was nothing they could have stood on. The stepladder was locked in the cupboard, Agnes had the only key, and the stool was broken. Only Tobias could have lifted the bell from its hook.

Tobias went red. The bell had a crack, he explained, and it had been clanking instead of ringing for weeks. He had taken it to his workshop to mend it as a surprise for the club, and he hadn't wanted to spoil the surprise by admitting it. The next Saturday the bell was back on its hook, and it rang out as clear as a church bell. The sailing club gave Tobias a round of applause, and he had to duck to get out of the room.
"""),

dict(title="The Scent of Lavender", kind="story", culprit="Mrs Vosper",
suspects=["Mrs Vosper", "Captain Quill", "Hedley Truscott"],
clues=["lavender", "fish", "engine oil"],
story="""
Agnes Bell has the best nose in Tidewhistle Cove. She can tell a breakfast tea from an afternoon blend from across the room, and she can tell when scones are one minute from burning.

On Monday, Tamsin Trevelyan asked her to come to the bookshop at once. Tamsin's grandfather's silver fountain pen had been taken from the little velvet lined drawer under the counter. Tamsin had shown it to three customers that morning, one after another, and each had held the drawer open and looked inside. When the last one had left, the pen was gone.

The three customers had been Captain Quill, Hedley Truscott and Mrs Vosper, a visitor from up the coast.

Agnes bent over the open drawer and breathed in. The velvet smelled, quite strongly, of lavender water.

Then she went to find the three customers.

Captain Quill was on the quay helping to unload the morning's catch, and he smelled, as he nearly always did, of fish and seaweed.

Hedley Truscott was in the boatyard with his head inside an outboard motor, and he smelled of engine oil and nothing else whatsoever.

Mrs Vosper was taking tea in the Kettle and Gull. As Agnes stepped through the door, a wave of lavender drifted across the room. Mrs Vosper wore a little sprig of lavender pinned to her collar, and she dabbed lavender water on her wrists as she spoke.

"A pen?" said Mrs Vosper. "Oh, I barely glanced into that drawer. I certainly never touched anything inside it."
""",
question="Who took the silver fountain pen?",
solution="""
Mrs Vosper took the pen.

The velvet inside the drawer smelled strongly of lavender water. Of the three people who had looked into that drawer, only Mrs Vosper wears lavender. Captain Quill smelled of fish and seaweed, and Hedley of engine oil. If she had barely glanced in, her scent would not have soaked into the velvet. Someone wearing lavender water had reached right inside.

Mrs Vosper sighed and took the pen out of her handbag. She said she wrote all her letters with a fountain pen, and had never seen one so fine. Tamsin, who knew a fellow letter writer when she met one, sold her a good, plain fountain pen from the shop, and threw in a bottle of blue ink. The drawer smelled of lavender for a month.
"""),
]
