# Narrative text. Thief names are asserted against data.json at build time.
PROLOGUE = [
 "The last bus of the afternoon ground its way up the mountain road with its windscreen wipers going like mad, and it stopped, with a sigh of relief, outside the Frostwood Lodge: five floors of creaking timber, green shutters and chimney smoke, with a little turret on top where the Summit Suite sits like a hat.",
 "That was on Sunday. By Sunday night the snow had swallowed the road, the bus, the signpost and very nearly the postbox, and the radio in the lobby announced, with some glee, that the snowplough would reach Frostwood “by next Sunday, or thereabouts.”",
 "The manager, Mr. Alphonse Pemberton, a round man with a round moustache, took the news bravely. He had one hundred and fifty-two guests, a larder full of cocoa, and a week of festivities planned: a snowman contest, a Bake-Off, a skating race, a Talent Evening and, on the final Sunday, a party for the lodge’s 125th birthday, beneath the portrait of its founder, Josephine Frost, which hangs in the lobby.",
 "He also had Mr. Mortimer Grayle. Mr. Grayle builds glass-and-steel hotels with rooftop pools, and he had come up the mountain to buy Frostwood, knock it down, and put up something he calls <i>The SkyResort</i>. “You have until Sunday to sign, Pemberton,” he said, tapping a thick contract. “A charming old place, but trouble. Pure trouble. You’ll see.”",
 "It took less than a day for trouble to arrive.",
 "Which is where you come in. You are the guest in the little room behind the front desk, the one who finishes the newspaper crossword before the kettle boils. Mr. Pemberton’s niece, Pippa, who is fifteen and carries a detective’s notebook everywhere, noticed this within an hour of your arrival. By Monday morning she had appointed you the lodge’s Official Detective, and herself your assistant, and nobody has dared to argue.",
 "Over the next six snowbound days there will be twelve small mysteries at Frostwood. Nobody will be hurt; that is a promise. But things will go missing, pranks will be played, a cake will be ruined and one painting will turn out not to be what it seems. Each time, Mr. Pemberton will hand you the register, Pippa will hand you the clues, and it will be up to you to find the one guest who did it.",
]

CAST = [
 ("Mr. Alphonse Pemberton", "Manager of the Frostwood Lodge. Round, kind, and increasingly anxious."),
 ("Pippa Pemberton", "His niece, fifteen, your self-appointed assistant. Owns a magnifying glass and uses it."),
 ("Gus", "The night porter. Sits at the front desk knitting a scarf that gets longer with every case."),
 ("Dot", "The chambermaid. Up before everyone, notices everything, and warms the towels."),
 ("Mrs. Hilda Brisket", "The cook. Guardian of the cocoa, the larder and the Bake-Off."),
 ("Miss Lettice", "The librarian, who knows exactly where every book in the lodge should be."),
 ("Lady Winifred Ashgrove", "Has spent every winter in the Summit Suite for forty years. Tells stories about polar bears."),
 ("Mr. Mortimer Grayle", "A developer who wants to buy Frostwood and knock it down. Stays in the Tower Room."),
]
CAST_NOTE = "None of these people is ever a suspect. The staff sleep in the staff cottage across the courtyard, Lady Winifred rarely leaves the Summit Suite, and Mr. Grayle, much to Mr. Pemberton’s dismay, has been following him around all week and has an alibi for everything. The suspects are always guests listed in that case’s register."

S = {}
S[1] = dict(when="Monday Morning", title="The Cocoa Tin", item="Who Took the Cocoa Tin?",
 story=[
 "Every night at Frostwood ends with cocoa hour in the Great Hall, and every cup of cocoa begins with Mrs. Brisket’s tin. It is a battered old thing, painted with faded edelweiss, and it holds <i>Brisket’s Blend</i>: a secret mixture of cocoa and spices that Mrs. Brisket’s grandmother invented and that nobody else has ever seen written down.",
 "On Sunday night, with the snow piling up against the windows and the road gone for good, cocoa hour was especially popular. {Nw} guests squeezed into the Great Hall. Some sat in the big chairs by the Fireside, some on the cushions by the Window, and some around the old Piano, where a guest was playing the only three tunes the piano still remembered.",
 "At eleven o’clock, Mrs. Brisket went to the kitchen to fetch more milk. She left the tin on the serving table, between the marshmallows and the cinnamon, as she has done every night for twenty-two years.",
 "When she came back, the tin was gone.",
 "“Gone!” she said, so loudly that the piano stopped. “My grandmother’s tin! Nobody leaves this hall until it is found!”",
 "Unfortunately everybody had already left, because it was bedtime and Mrs. Brisket had been in the kitchen for quite a long time, looking for the good milk. By the time Mr. Pemberton arrived in his dressing gown, the Great Hall was empty except for forty dirty mugs and one very cross cook.",
 "At breakfast on Monday, Pippa presented you with a list of every guest who had been at cocoa hour, showing where each had been sitting and what they had put on top of their cocoa. (“I wrote it down at the time,” she said. “I write everything down at the time.”) Mr. Grayle, eating toast at the next table, sniffed. “A missing tin of cocoa,” he said. “First day of the snow. Trouble, Pemberton. I told you.”",
 "Mr. Pemberton turned pink. “You’ll find it, won’t you?” he whispered to you. “Mrs. Brisket won’t make another cup until you do.”",
 ],
 note="These are the {N} guests who were at Sunday’s cocoa hour, listed alphabetically by surname. Room numbers tell you the floor: Room 214 is on the 2nd floor. Guests who share a room have the same room number.",
 confess="The tin was found under {first}’s pillow, its lid still firmly shut. It turned out that {first} {last}, an {occ_l} from {home}, had simply been desperate to know what was in <i>Brisket’s Blend</i>, but the famous lid is stuck fast and only opens for Mrs. Brisket. “I tried for two hours,” {first} admitted. Mrs. Brisket was so pleased that her tin had defeated a professional that she forgave {first} on the spot, on condition of washing every cocoa mug for the rest of the week. She opened the lid with one flick of her thumb, and cocoa hour resumed that evening. Gus’s scarf reached his knees.")

S[2] = dict(when="Monday Afternoon", title="The Snowman’s Hat", item="Who Took the Snowman’s Hat?",
 story=[
 "The great Frostwood Snowman Contest was held in the courtyard on Monday afternoon, with the snow still falling in fat, lazy flakes. {Nw} guests took part in four teams, Red, Blue, Green and Gold, each wearing a wool armband and each quite certain it would win.",
 "Standing over the whole contest, as he does every year, was Sir Frostington: the lodge’s own snowman, seven feet tall, with coal buttons, a carrot nose and, on his head, the most precious hat in the building. It is a tall black top hat that once belonged to Mr. Pemberton’s great-grandfather, Colonel Pemberton, who (so the story goes) once walked all the way down the mountain in a blizzard to fetch soup for the guests, and came back wearing the hat and not much else.",
 "At half past three, while Mr. Pemberton was judging the Blue team’s snowman, Pippa looked up and gasped. Sir Frostington’s head was bare. The top hat had vanished. In its place was a licked-clean toffee-apple stick, and pinned to the snowman’s scarf was a note in wobbly capitals: <i>SIR FROSTINGTON HAS GONE TO FETCH THE SOUP, LIKE THE COLONEL.</i>",
 "“A prank!” said Mr. Pemberton faintly. “On Great-Grandpa’s hat!”",
 "Mr. Grayle, watching from the terrace with a flask of coffee, laughed until he had to sit down. “Pranks on the second day,” he said. “Wait until the reviews come in.”",
 "Pippa had already begun her list. Every contestant had signed in with their team, and the food stalls around the courtyard had written down which snack each contestant had bought. (Everybody got one free snack: hot Chestnuts, a Pretzel, a Toffee Apple, or a cup of Soup.) “Forty-eight names,” she said, handing it over. “And one of them is wearing a top hat under their bed.”",
 ],
 note="These are the {N} contestants in Monday’s Snowman Contest, listed alphabetically by surname, with their team and the free snack each one chose. Room numbers tell you the floor: Room 214 is on the 2nd floor. Guests who share a room have the same room number.",
 confess="The hat turned up that evening, perched on the head of the carved wooden moose in the lobby. {first} {last}, a {occ_l} from {home}, owned up at once. “The Colonel story is my family’s favourite,” {first} explained, “and I thought Sir Frostington deserved an adventure.” As for the toffee apple: “Dentists are allowed one a year,” said {first} with dignity. Mr. Pemberton decided that the moose looked rather distinguished in a top hat, and it is still wearing it. Mr. Grayle was heard to mutter that it was “unprofessional.” Gus’s scarf reached his ankles.")

S[3] = dict(when="Tuesday Morning", title="The Starlight Sapphire", item="Who Took the Sapphire?",
 story=[
 "The most distinguished guest at Frostwood is Lady Winifred Ashgrove, who occupies the Summit Suite at the very top of the lodge, a few steps above the 5th floor. Lady Winifred has come to Frostwood every winter for forty years, and every year she brings the <i>Starlight Sapphire</i>: a necklace of pale blue stones that, when held up to the chandelier, scatters little stars across the walls. She had shown it off at the welcome dinner on Saturday evening, and more than a few guests had gasped.",
 "On Monday night Lady Winifred placed the necklace, as always, in the velvet box on her dressing table, drank her warm milk, and went to sleep with the wind howling outside.",
 "At seven o’clock on Tuesday morning her shriek could be heard in the boiler room.",
 "The velvet box was open. The necklace was gone.",
 "Mr. Pemberton arrived in his dressing gown and slippers, followed closely by half the 5th floor. There was no sign of a break-in. The window was latched and frosted shut, and outside it lay a smooth, unbroken drift of snow. Whoever had taken the Starlight Sapphire had walked in through the door, and whoever it was had not left the lodge, because nobody <i>could</i> leave the lodge.",
 "“It must be one of the guests,” Mr. Pemberton whispered, clutching the register to his chest as though it might be stolen next.",
 "It was not quite as bad as it sounded. The Summit Suite can only be reached through the Old Wing staircases, and on Monday night the door between the Old Wing and the rest of the lodge had been bolted by Gus at ten o’clock sharp, as it is every night. That left the {Nw} guests whose rooms were on the Old Wing side of that door. One of them was sleeping with a sapphire necklace tucked under their pillow.",
 "By breakfast the lodge was buzzing. Gus remembered a few things. Dot remembered a few more. Lady Winifred herself had a story. Little by little, Pippa gathered the clues together and laid them out in front of the fire. Mr. Grayle said it was “the final straw, surely,” and asked Mr. Pemberton whether he had a pen.",
 "Mr. Pemberton turned to you. “Please,” he said. “Before the snowplough comes and the thief rides off down the mountain with it.”",
 ],
 note="These are the {N} guests who were on the Old Wing side of the bolted door on Monday night, listed alphabetically by surname. Room numbers tell you the floor: Room 214 is on the 2nd floor. Guests who share a room have the same room number.",
 confess="{first} {last}, a mild-mannered {occ_l} from {home}, had fallen head over heels for the Starlight Sapphire at Saturday’s dinner. “I only wanted to see it sparkle in the moonlight,” {first} confessed, handing the necklace back from inside a hollowed-out hyacinth bulb. Lady Winifred, rather touched, decided not to press charges, on the condition that {first} arrange the flowers for the lodge’s birthday party on Sunday. Mr. Grayle, who had been hoping for a scandal, looked disappointed. Gus’s scarf went twice round his chair.")

S[4] = dict(when="Tuesday Afternoon", title="The Salted Sponge", item="Who Salted the Sponge?",
 story=[
 "The Great Frostwood Bake-Off is the most serious event of the week. On Tuesday afternoon the Great Hall was filled with four long rows of baking stations, labelled A, B, C and D, and {Nw} contestants in borrowed aprons, each baking one entry: a Sponge, a Tart, Scones, Shortbread, or a Pie.",
 "The favourite, to everyone’s surprise, was Mr. Grayle. He had announced at lunch that he had won a baking prize at school “and several since,” and that his lemon sponge was “unbeatable.” He had also announced, rather loudly, that he planned to make “a little speech about the future of this building” when he collected his trophy.",
 "At twenty past two, something happened in the west pantry. Nobody saw it. But at three o’clock, when the judges took their first forkful of Mr. Grayle’s lemon sponge, their faces went through several interesting shapes. The sponge was salty. Extremely salty. Somebody had swapped the sugar jar in the west pantry for the salt jar, and Mr. Grayle, who had been bustling about with his measuring cups, had used a whole cupful.",
 "“Sabotage!” cried Mr. Grayle, red to the ears. “This place is a madhouse, Pemberton! A madhouse!”",
 "Mrs. Brisket tasted the sponge herself and agreed it was sabotage, and also that it was “a very light texture, considering.” The sugar jar was nowhere to be found.",
 "Pippa had written down every contestant’s station and entry, of course, and she had been hiding behind a sack of flour for most of the afternoon, “for observation purposes.” Between her notes and the gossip at the judges’ table, you soon had a stack of clues. There was only one question left: which of the {Nw} bakers had done it?",
 ],
 note="These are the {N} contestants in Tuesday’s Bake-Off, listed alphabetically by surname, with their Entry and their baking Station. Room numbers tell you the floor: Room 214 is on the 2nd floor. Guests who share a room have the same room number.",
 confess="The sugar jar was found on top of the wardrobe in Room {room}. {first} {last}, a {occ_l} from {home}, went rather pink. “I heard him practising his speech,” {first} said. “He was going to announce that Frostwood would be knocked down, right there, at the Bake-Off, in front of everybody. I thought if he didn’t win, he couldn’t make the speech.” Mr. Pemberton went pale; this was the first he had heard of any speech. Mr. Grayle said nothing at all, which was unusual, and later ate a second slice of the salty sponge when he thought nobody was looking. The Tart won. Gus’s scarf was now long enough to use as a draught excluder.")

S[5] = dict(when="Wednesday Morning", title="The Missing First Edition", item="Who Took the First Edition?",
 story=[
 "The Frostwood library occupies a long, low room on the 2nd floor of the West Wing, with a crackling fire, three sleeping cats and a very good view of the snow. Its greatest treasure is a first edition of <i>The Mystery at Pinecrest Pass</i>, the famous detective novel that was written, so they say, in this very room, in a single snowbound winter many years ago.",
 "On Tuesday, Miss Lettice the librarian moved the book from its old oak shelf into a new glass case, to keep it safe from sticky fingers. At lunchtime she locked the case, polished the glass and stood back admiring it.",
 "On Wednesday morning the case was empty.",
 "The cuckoo clock above the fireplace had been nudged and had stopped at a quarter past eleven, which was a great help. So was the library visitors’ book, which Miss Lettice insists every visitor signs. On Tuesday {Nw} guests had signed it, each one noting when they visited (Morning, Afternoon or Evening) and which kind of book they borrowed: Mystery, Poetry, Travel, Cookery or Science.",
 "“Somebody on this list,” Miss Lettice said, tapping the visitors’ book, “has taken the most valuable book in the lodge. And I want it back before breakfast tomorrow, or I shall close the library.” The whole lodge gasped. On a snowbound mountain, a closed library is a very serious threat.",
 "Mr. Grayle, passing, remarked that in <i>his</i> hotels there would be no libraries at all, “just screens, and far less trouble.” Miss Lettice looked at him in a way that made the cats leave the room.",
 "Pippa had spent the morning interviewing everyone in sight. “I’ve got nine clues,” she told you, “and a very strong feeling.”",
 ],
 note="These are the {N} guests who signed the library visitors’ book on Tuesday, listed alphabetically by surname, with the kind of book each Borrowed and when each Visited. The first digit of a room number is the floor. Guests who share a room have the same room number.",
 confess="The first edition was found on {first} {last}’s bedside table with a bookmark in the very last chapter. {first}, a {occ_l} from {home}, had owned a copy since childhood, but its final pages had been torn out long ago. “For thirty years I’ve wondered who did it,” {first} explained. “And there it was, behind glass, with the ending inside.” Miss Lettice, who understands these things, allowed {first} to finish the last chapter in the library, under supervision, with a cup of tea. (It was the vicar.) The library stayed open. Gus’s scarf had to be rolled up at night.")

S[6] = dict(when="Wednesday Afternoon", title="The Tangled Laces", item="Who Took the Laces?",
 story=[
 "By Wednesday the lake behind the lodge had frozen as smooth as glass, and Mr. Pemberton declared that the Frostwood Skating Race would take place at four o’clock. {Nw} guests signed up, and the race marshal (Gus, in a borrowed whistle) divided them into four heats: Heat 1, Heat 2, Heat 3 and Heat 4. Everybody was given a team scarf, too, which made the start line look like a box of crayons.",
 "The lodge keeps its rental skates in a little wooden shed at the edge of the lake. At three o’clock Pippa went to fetch them and found every single pair of skates sitting neatly on its shelf, and not one single lace. All eighty laces were gone.",
 "They turned up twenty minutes later, hanging from the roof of the lakeside gazebo: knotted together into one enormous, tangled ball the size of a pumpkin, like some sort of woollen hedgehog.",
 "It took Mrs. Brisket, Dot and three volunteers with knitting needles almost an hour to untangle them, and the race began very late, in the dusk, with lanterns on the ice. Mr. Grayle, who had been timing the delay on his expensive watch, told everyone that at The SkyResort the ice rink would be indoors, heated and “completely lace-free.” Nobody knew what that meant.",
 "Pippa had the race sign-up sheet, showing everyone’s heat and scarf, and she had spent the hour of untangling asking questions. “It wasn’t an accident,” she said. “Nobody ties eighty laces together by accident.”",
 ],
 note="These are the {N} guests who signed up for the Skating Race, listed alphabetically by surname, with their Heat and team Scarf. The first digit of a room number is the floor. Guests who share a room have the same room number.",
 confess="{first} {last}, a {occ_l} from {home}, came forward before you had even finished explaining. “I noticed the laces were fraying,” {first} said, “and I’d brought eighty brand-new waxed ones in my luggage, because I always do. I only meant to swap them. But I tied the old ones together to carry them, and the bundle got away from me, and then it was up in the gazebo and everybody was shouting, and I panicked.” The new laces were lovely. The race was won by a nine-year-old on the 2nd floor. Gus’s scarf now needed its own chair.")

S[7] = dict(when="Thursday Morning", title="The Midnight Feast", item="Who Ate the Feast?",
 story=[
 "On Wednesday evening Mrs. Brisket baked sixty sticky cinnamon buns for Thursday’s festival breakfast. She glazed them, set them out on her largest tray in the cold larder, locked the larder door with her own key, and went to bed feeling that all was right with the world.",
 "At six o’clock on Thursday morning, the larder door was locked and the tray was empty. Not a bun remained. There were crumbs, a smear of glaze on the door handle, and a trail of pastry flakes leading out across the kitchen and up the West Wing stairs.",
 "“Sixty buns,” said Mrs. Brisket, in a voice like a very distant avalanche. “<i>Sixty.</i>”",
 "Gus had been awake all night at the front desk, knitting, and he had seen somebody in pyjamas slip past the end of the corridor at one in the morning. Dot had noticed some slipper-marks. And Pippa, who takes these things personally, had spent the morning going door to door with a clipboard, asking {Nw} sleepy guests what pyjamas and slippers they had been wearing the night before. (Most of them told her. Some of them told her rather more than she needed to know.)",
 "Mr. Grayle came down to a breakfast of dry toast. “Burglary,” he said, “in the kitchens. Honestly, Pemberton, how much longer can you keep this up?” Mr. Pemberton pretended not to hear, and ate his toast in silence.",
 ],
 note="These are the {N} guests who could have reached the kitchen on Wednesday night, listed alphabetically by surname, with the Pyjamas and Slippers they wore. The first digit of a room number is the floor. Guests who share a room have the same room number.",
 confess="{first} {last}, a {occ_l} from {home}, confessed with glaze still on one sleeve. “The staff,” {first} said. “They’re snowed in across the courtyard in the staff cottage, and they were going to miss the festival breakfast completely. Dot said so. So I borrowed my roommate’s larder key and took the buns over through the snow at one in the morning.” Mrs. Brisket, who had not thought of that, sat down heavily, then stood up and baked sixty more, and then another sixty for good measure. The staff sent a thank-you card signed by everyone, including the cat. Gus’s scarf reached the front door.")

S[8] = dict(when="Thursday Afternoon", title="The Snow Globe", item="Who Took the Snow Globe?",
 story=[
 "On the lobby mantelpiece, for as long as anyone can remember, has stood the Frostwood snow globe: a heavy glass dome on a carved walnut base, and inside it a tiny model of the lodge itself, complete with green shutters and a little turret. Shake it and the snow falls on the tiny roof just as it falls on the real one. For most of the lodge’s history it lived in the dining room, and it was only moved to the lobby at lunchtime on Saturday, to make room for the Bake-Off trophy.",
 "On Thursday afternoon the lobby was quiet. Most guests were out enjoying the snow, or warming up in the sauna, or playing cards, or asleep in the library with a book on their face. At four o’clock, Gus came back to his desk from a tea break and looked at the mantelpiece, and the mantelpiece was bare.",
 "“It’s just a snow globe,” said Mr. Grayle, who happened to be reading a newspaper in the corner. But he said it rather more quietly than usual, and later Pippa saw him standing by the empty mantelpiece, looking thoughtful.",
 "Pippa had already made a list of all the {Nw} guests who had not been locked out of the lobby that afternoon (the side door had been bolted for painting), and next to each name she wrote down what they had been doing at three o’clock and what coat they had been wearing. “Lots of coats,” she said, “and one of them had a snow globe hidden under it.”",
 ],
 note="These are the {N} guests who could have passed through the lobby on Thursday afternoon, listed alphabetically by surname, with what each was doing At 3 p.m. and the Coat each wore. The first digit of a room number is the floor; the last two digits tell you where the room is on its corridor (see How to Solve a Case). Guests who share a room have the same room number.",
 confess="{first} {last}, a {occ_l} from {home}, handed the snow globe back with both hands and a sheepish smile. “I had never seen snow fall, not once, until this week,” {first} said. “And then it did, and it was the most beautiful thing I’d ever seen, and I wanted to take a little bit of it home. I only meant to keep it until Sunday. I’ve been shaking it every night before I go to sleep.” Lady Winifred, hearing this, sent down a snow globe of her own, a tiny one with a polar bear in it, as a present. The Frostwood globe went back on the mantelpiece. Gus’s scarf was now being knitted in the corridor.")

S[9] = dict(when="Friday Morning", title="The Ghost of the East Stairs", item="Who Was the Ghost?",
 story=[
 "At one o’clock on Friday morning, Mr. Grayle was coming back from a late-night conversation with the lodge’s telephone (the lines were down, but he talked to it anyway) when he met a ghost on the 2nd-floor landing.",
 "It was a tall, white, wobbly ghost, with two holes for eyes, and it said “Wooooooo” in a voice like a tea kettle. It announced that it was the Grey Lady of Frostwood, that it had haunted the lodge for a hundred years, and that it did not care for “men who knock down old buildings.” Then it fled up the East stairs with a clatter and was gone.",
 "Mr. Grayle, it must be said, was not frightened. He was delighted. He woke Mr. Pemberton to tell him about it. “A haunted hotel, Pemberton! Guests pay double for a ghost! When I own the place, I’ll put it on the brochure!” Mr. Pemberton, who had been fast asleep, said something that Pippa has promised not to write down.",
 "In the morning, a bedsheet with two eye-holes was found stuffed down the laundry chute, along with a keyring and, a little further along the stairs, an empty mug.",
 "Pippa gathered up every scrap of evidence, and then drew up a list of the {Nw} guests who could have been on the East stairs at one in the morning. Next to each name she wrote their usual Bedtime (from Dot’s turn-down list) and their Nightcap (from the kitchen’s order book). “There’s no such thing as ghosts,” she told you firmly. “But there is such a thing as a guest in a sheet.”",
 ],
 note="These are the {N} guests who could have been on the East stairs early on Friday morning, listed alphabetically by surname, with their usual Bedtime and Nightcap. The first digit of a room number is the floor; the last two digits tell you where the room is on its corridor (see How to Solve a Case). Guests who share a room have the same room number.",
 confess="{first} {last}, a {occ_l} from {home}, sewed the eye-holes in the sheet back up without being asked. “I thought if the lodge were haunted, he wouldn’t want to buy it,” {first} explained. “I didn’t know ghosts were good for business.” Mr. Grayle laughed loudly at that. But when {first} had gone, he asked Pippa, quite quietly, whether it was true that so many of the guests had been coming to Frostwood for years and years, and whether they really loved it that much. Pippa said yes. Mr. Grayle went away to think. Gus’s scarf had reached the 1st-floor landing.")

S[10] = dict(when="Friday Evening", title="The Silent Quartet", item="Who Silenced the Quartet?",
 story=[
 "Every year the Pinewood String Quartet travels up the mountain to play at Frostwood, and every year they close the Talent Evening with the <i>Frostwood Waltz</i>. This year they had been snowed in along with everybody else, which they did not mind at all, because Mrs. Brisket had been feeding them.",
 "The Talent Evening began at eight o’clock on Friday. {Nw} guests had signed up: some to perform (Singing, Magic, Juggling, Poetry or Piano) and some simply to sit in the Audience and clap. Everybody performing had been given a rehearsal slot in the ballroom that afternoon, at 4 p.m., 5 p.m., 6 p.m. or 7 p.m.",
 "At half past six the quartet’s leader went to the Music Room to fetch the instruments, and came back looking as if she had seen a second ghost. The violins, the viola and the cello were all present and correct. But all four bows had disappeared, and so had every page of sheet music.",
 "“We can’t play the <i>Waltz</i> without bows,” she said. “We can’t play anything without bows.”",
 "“The finale is ruined!” wailed Mr. Pemberton.",
 "Mr. Grayle, in a velvet jacket, looked around the ballroom at all the disappointed faces, and for once did not say anything clever at all.",
 "Pippa, however, was already at work. She had the list of every Act and every Rehearsal time, and in twenty minutes she had collected twelve clues. “There’s still time,” she said. “If we find the bows before nine, the quartet can still play.”",
 ],
 note="These are the {N} guests registered for Friday’s Talent Evening, listed alphabetically by surname, with their Act and their Rehearsal slot. The first digit of a room number is the floor; the last two digits tell you where the room is on its corridor (see How to Solve a Case). Guests who share a room have the same room number.",
 confess="The bows were in a violin case under the bed in Room {room}, and the sheet music at the bottom of the laundry chute, a little crumpled but perfectly playable. {first} {last}, a {occ_l} from {home}, was found backstage, shaking. “I was supposed to sing just before the quartet,” {first} whispered, “and I have never been so frightened in my life. I thought if there were no finale, they might cancel the whole evening.” The quartet’s leader listened, and then did something marvellous: she asked {first} to sing <i>with</i> them. At a quarter past nine, {first} {last} sang the <i>Frostwood Waltz</i> with the Pinewood String Quartet, and the ballroom rose to its feet. Mr. Grayle clapped loudest. Gus’s scarf was used as a stage curtain.")

S[11] = dict(when="Saturday Morning", title="The Master Key", item="Who Took the Master Key?",
 story=[
 "Mr. Pemberton’s master key opens every door at Frostwood: every bedroom, every cupboard, the wine cellar, the boiler room and the little locked door to the old attic, which nobody has opened in years. It hangs on a brass hook in his office, just off the dining room, and it has never, ever gone missing.",
 "On Saturday morning, between half past seven and half past eight, it went missing.",
 "Mr. Pemberton discovered it at twenty to nine, when he went to fetch the key to the linen cupboard and found the hook empty and sticky. “Everything!” he said, sitting down suddenly. “It opens <i>everything</i>!”",
 "Mr. Grayle, who had followed him into the office to talk about contracts, looked at the empty hook. Then he looked at Mr. Pemberton, who was very pale. “Let me get you a cup of tea, Alphonse,” he said, which was the first time anyone had heard him use Mr. Pemberton’s first name.",
 "Breakfast at Frostwood is served at eight tables in the dining room, and each guest is given a paper ticket with their table number printed on it. Mrs. Brisket keeps a record of what everyone ate, because she likes to know. Between the tickets, Mrs. Brisket’s record and a very determined morning of questions, Pippa put together a list of the {Nw} guests who could have gone near the office. “Thirteen clues,” she said, a little breathlessly. “This is the hardest one yet.”",
 ],
 note="These are the {N} guests who could have been near Mr. Pemberton’s office on Saturday morning, listed alphabetically by surname, with their Breakfast and their dining-room Table. The first digit of a room number is the floor; the last two digits tell you where the room is on its corridor (see How to Solve a Case). Guests who share a room have the same room number.",
 confess="{first} {last}, a {occ_l} from {home}, returned the key with a dusty cobweb still hanging from it. “Grandma first came to Frostwood sixty years ago,” {first} explained, “and danced at the midwinter ball in a blue silk gown that was packed away in the attic and never found again. It’s her birthday tomorrow. I only wanted to find the dress and mend it for her, and I couldn’t ask for the key without spoiling the surprise.” The dress was found, in a trunk, in the attic, and with it an old guest book going back to 1901. Mr. Pemberton was too relieved to be cross. Mr. Grayle spent the rest of the morning in the attic, reading the old guest book. Gus’s scarf had become a local landmark.")

S[12] = dict(when="Saturday Evening", title="The Forged Founder", item="Who Swapped the Portrait?",
 story=[
 "In the lobby of the Frostwood Lodge hangs the portrait of Josephine Frost, who built the lodge in 1901 with her own savings and, according to legend, a good deal of her own carpentry. She is painted in a dark green coat, standing in the snow, with the lodge behind her and a look on her face that says she will not be argued with. Tomorrow is the lodge’s 125th birthday, and the party is to be held beneath her.",
 "At afternoon tea on Saturday, Lady Winifred came down from the Summit Suite especially to look at the portrait, as she does once every year. She looked at it for a long moment. Then she put down her teacup.",
 "“That,” said Lady Winifred, “is not Josephine.”",
 "She was right. On close inspection, the painting was a copy: a very good one, but the varnish was only a day old, the frame had been screwed on with shiny new screws, and there were tiny initials in the corner that had never been there before. Somebody had taken the real portrait and hung a copy in its place, and Gus’s night log showed that the swap must have happened on Friday night, between eleven o’clock and midnight.",
 "Mr. Pemberton sat down on the stairs and put his head in his hands. “Josephine,” he said. “On her birthday.”",
 "And then an extraordinary thing happened. Mr. Grayle sat down on the stairs beside him. “We’ll find her, Alphonse,” he said. “Your detective hasn’t failed yet.”",
 "This time there was no smaller list. On Friday night, any guest in the lodge could have crossed the lobby. So Pippa, with the help of Gus, Dot and a great deal of cocoa, drew up a register of every single guest at Frostwood, all {Nw} of them, with what each was doing at 11 p.m. and what each had on their feet. “Fourteen clues,” she said. “It’s the last case of the week. Let’s make it a good one.”",
 ],
 note="This register lists all {N} guests staying at Frostwood, alphabetically by surname, with what each was doing At 11 p.m. on Friday and the Shoes each wore. Every occupied room in the lodge appears here. The first digit of a room number is the floor; the last two digits tell you where the room is on its corridor (see How to Solve a Case). Guests who share a room have the same room number.",
 confess="The real portrait of Josephine Frost was found in Room {room}, propped carefully against the wall, wrapped in a quilt. {first} {last}, a {occ_l} from {home}, was sitting in front of it, holding a yellowed envelope. “Josephine Frost was my great-great-grandmother,” {first} said quietly. “In her diary she wrote that she had hidden a letter ‘behind my own face, for whoever needs it most.’ I needed to look behind the portrait without anyone fussing, so I made a copy from my photographs and swapped them for one night. I was going to put her back before the party. I promise I was.”")

EPILOGUE = [
 "The letter was read aloud that evening in the lobby, beneath the real portrait, which was back on its hook where it belonged.",
 "<i>“To whoever needs this,”</i> Josephine Frost had written, in 1901. <i>“I built this lodge so that travellers caught by the snow would always have somewhere warm to wait. It is not the building that matters. It is the waiting together: the cocoa, the stories, and the kindness of strangers who become friends. Whoever owns Frostwood, keep the fires lit.”</i>",
 "There was a long silence. Then Mr. Grayle stood up, took his thick contract out of his velvet jacket, and, very slowly, tore it in half.",
 "“I came here to buy a building,” he said. “I seem to have spent a week in a family instead. My grandmother honeymooned here, you know; I found her name in the old guest book in the attic. I’d forgotten.” He cleared his throat. “If Mr. Pemberton will allow it, I should like to pay for a new roof. And I should like to book the Tower Room for next winter. And the winter after that.”",
 "Mr. Pemberton could not speak, so he shook Mr. Grayle’s hand for about a minute and a half.",
 "The snowplough arrived on Sunday morning, just in time for the birthday party. The cocoa tin was on the serving table, the top hat was on the moose, the snow globe was on the mantelpiece, the Starlight Sapphire sparkled on Lady Winifred, and Josephine Frost watched over all of it with the look of someone who had known all along how it would turn out. Queenie Yelland danced in her blue silk gown. The Pinewood String Quartet played the <i>Frostwood Waltz</i> three times.",
 "Gus finished his scarf. It was one hundred and twenty-five feet long, one foot for every year, and they wrapped it all the way round the lodge like a ribbon on a present.",
 "Nobody was in any hurry to leave.",
]

# Hints: {T:Title} is replaced by "Clue n (Title)" at build time.
HINTS = {
 1: ["{T:The Landing} is about floors: look only at the first digit of each room number.",
     "{T:Plain Cocoa} and {T:The Sticky Shelf} both use the Topping column. Apply them in order anyway; the solutions count each one separately."],
 2: ["{T:The East Door} is about the last two digits of the room number: 11 to 20 is the East Wing.",
     "{T:Snowmen Back Home} lists exactly six cities. Anyone from any other city is cleared."],
 3: ["{T:Nobody to Vouch} is about sharing a room: look for any other guest on the register with the same room number, even one you have already crossed off.",
     "{T:The Clicking Door}: even room numbers end in 0, 2, 4, 6 or 8."],
 4: ["{T:The Apron} is about the first name, not the surname.",
     "{T:A Whispered Word}: a suspect shares a room if any other guest on the register has the same room number."],
 5: ["{T:Two Teacups} needs exactly two guests in the room: not one, and not three.",
     "{T:The Signature}: count the letters in the surname. Seven or more letters survive."],
 6: ["{T:The Lake View}: odd room numbers end in 1, 3, 5, 7 or 9.",
     "{T:Where’s the Shed?} keeps only Sunday arrivals."],
 7: ["{T:Plaid or Bunny} is an either/or clue. A suspect with Plaid pyjamas <i>and</i> Bunny slippers is cleared, and so is a suspect with neither.",
     "{T:The Borrowed Key}: look at everyone else sharing the suspect’s room, including roommates you have already crossed off. At least one of them must be a Chef or a Baker."],
 8: ["{T:Across the Hall}: find the facing room (an odd room faces the next even number, so 417 faces 418) and see whether anybody on the register is staying there, crossed off or not.",
     "{T:The Creaking Ceiling}: the room directly above has the same last two digits and a first digit one higher. A 5th-floor room has nothing above it."],
 9: ["{T:The Grey Lady} is an ‘at least one’ clue: a Sunday arrival survives only if their Bedtime is Midnight.",
     "{T:The Midnight Snack}: check every roommate of each suspect. If any of them is a Student, the suspect is cleared.",
     "{T:Thumping}: the room directly below has the same last two digits and a first digit one lower."],
 10: ["{T:Quiet Above} clears a suspect if <i>anyone</i> on the register (crossed off or not) is staying in the room directly above.",
      "{T:Two Possibilities}: keep a suspect if their Rehearsal is 4 p.m., or if they live in Montreal, Quebec City or Toronto, or both."],
 11: ["{T:The Breakfast Ticket}: compare the Table number with the first digit of the Room number. The Table must be bigger.",
      "{T:The Neighbour’s Knock} and {T:Nobody Across the Hall}: next door is two numbers away on the same floor (Room 101 has only 103 beside it; Room 120 has only 118). Across the hall, odd faces the next even (113 faces 114).",
      "{T:The Name Tag}: count the letters in the first name and in the surname."],
 12: ["The note above the register lists every empty room in the lodge, which helps with {T:Paint Fumes}.",
      "{T:If the Movie, then Sneakers} is an if/then clue: Movie-goers must be wearing Sneakers, and everyone else must be wearing Boots.",
      "{T:The Signature}: compare the first letter of the first name with the first letter of the surname. <i>Zelda Abbott</i> would survive (Z comes after A); <i>Abe Zimmer</i> would not."],
}
