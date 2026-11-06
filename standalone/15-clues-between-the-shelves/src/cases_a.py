"""Cases One to Fourteen. Each case: title, kind (story|logic), story, ask, solution, keys (clue phrases that must appear in the story before the question)."""

CASES_A = [
{
"title": 'The Mis-Shelved Cookbook',
"kind": 'story',
"story": """
On a rainy Tuesday morning, Iris Quill opened Willow Quill Books and found a problem on the travel shelf. Wedged between two guides to Italy was a thick hardcover cookbook with flour still faint on the cloth binding. The spine said Harvest Kitchen. It did not belong in travel at all.

Theo Vale came in shaking rain from his coat. "I shelved every new arrival yesterday," he said. "I put cookbooks in cooking. I put travel in travel. I did not put a cookbook in Italy."

Three people had been in the shop late the afternoon before, after Theo had finished shelving and gone to the post office with returns.

First, Mabel Finch had browsed knitting patterns near the front, then asked Iris for a book about pasta sauces for her grandson. Iris had pointed her toward cooking and gone to help another customer at the till.

Second, Owen Hart, the history teacher, had spent twenty minutes in biography, then carried three hardbacks to the counter and paid for them without going near travel.

Third, Nora Peake from the cafe next door had ducked in to borrow Iris's umbrella because her own had a broken spoke. She had stood dripping by the travel shelf while Iris fetched the umbrella from the back room, and she had left with a wave and a promise to return it the next day.

Iris pulled Harvest Kitchen free. Inside the front cover, someone had tucked a cafe napkin with a coffee ring on it and a short list in pencil: basil, cream, garlic, tagliatelle. The handwriting was small and tidy, with a little curl on every capital letter. Iris knew that curl. Nora wrote the specials board at the cafe every morning with exactly those curls.
""",
"ask": 'Who put the cookbook on the travel shelf, and how does Iris know?',
"solution": """
Nora Peake put it there.

Theo had finished shelving before he left, so the cookbook was moved after he went. Owen never left biography until he paid. Mabel asked for a pasta book and was pointed to cooking, but Iris never saw her take a book to travel. Nora stood dripping beside the travel shelf while Iris was in the back, and the napkin tucked inside Harvest Kitchen carried Nora's curly cafe handwriting and a coffee ring from next door.

Nora admitted she had picked up the cookbook to copy a quick sauce for the lunch special, heard the post van arrive, and slid the book onto the nearest shelf so her hands were free for the umbrella. Iris laughed, shelved Harvest Kitchen in cooking, and kept the napkin for the cafe's jar of useful scraps. Theo wrote a small shelf tip for the staff notebook: If it smells of garlic, it is not travel.
""",
"keys": ['stood dripping by the travel shelf', 'little curl on every capital letter', 'Nora wrote the specials board'],
},
{
"title": 'The Borrowed Bookmark',
"kind": 'story',
"story": """
Pearl Ashford ran the Thursday evening book club, and she never turned a page without her favourite bookmark, a thin strip of green leather with a tiny brass acorn at the top. On Thursday at six, she swept into Willow Quill Books for the club meeting in the back room, opened her copy of The Quiet Orchard, and gasped.

"My bookmark is gone," she said. "It was in this book when I left the house."

Iris checked the holds shelf, the counter, and the window seat. No green leather. Quill the cat blinked from the mystery shelf and offered no help.

Three people had handled Pearl's book that day.

Theo had stamped the shop's due-date slip into it that morning when Pearl reserved the shop's extra copy for a friend. He said he had set the bookmark on the counter for a moment, then put it straight back between the same pages.

Clara Moss, the poet, had borrowed the book for an hour at lunch to check a passage she wanted to quote in a new poem. She returned it to Pearl's tote at the cafe with a thank-you note on a yellow sticky.

Benji Crowe, the mailman, had carried Pearl's tote from the cafe to the bookshop at half past five because Pearl's hands were full of scones for the club. He said he had not opened the book.

Iris asked Clara about the sticky note. Clara pointed to Pearl's tote. The yellow sticky was still on the cover. Under it, pressed into the cloth, was a faint green outline the shape of a thin bookmark, as if leather had sat under the sticky in a warm room. And in Clara's own bag, half tucked under a notebook, Iris spotted a flash of green leather and a tiny brass acorn.
""",
"ask": "Who has Pearl's bookmark, and how did it leave the book?",
"solution": """
Clara Moss has it.

Theo put the bookmark back after stamping. Benji never opened the book. Clara borrowed the book at lunch, and the green outline under her sticky note shows the bookmark was still in the book when she pressed the sticky onto the cover. She must have slipped the bookmark out afterward, and Iris found the green leather with the brass acorn half tucked in Clara's own bag.

Clara went pink. She had meant to copy the acorn shape for a poem about autumn and had forgotten to put the bookmark back. Pearl got her acorn, the club got their scones, and Clara bought a plain paper bookmark from the counter jar so she would not be tempted again. Iris added acorn bookmarks to the counter jar that week, and they sold out by Saturday.
""",
"keys": ['faint green outline the shape of a thin bookmark', 'flash of green leather and a tiny brass acorn', 'borrowed the book for an hour at lunch'],
},
{
"title": 'The Swapped Tote Bags',
"kind": 'story',
"story": """
Saturday mornings at Willow Quill Books were busy. Iris kept a basket by the door for customers' tote bags while they browsed. At noon, Ruth Ellery, the retired librarian, came to collect her bag and frowned.

"This is not my tote," she said. "Mine is canvas with a blue stripe. This one is canvas with a green stripe."

Theo checked the basket. Two totes remained, both canvas, one blue-striped and one green-striped, sitting side by side where someone had set them down together.

Ruth's blue-striped tote held a knitting magazine, a packet of peppermints, and a library card with her name. The green-striped tote held a seed catalogue, a pair of muddy gardening gloves, and a shopping list that began with rose feed and ended with a reminder to return a book about espaliered apples.

Sam Quinn, the gardener, arrived breathless a minute later. "Has anybody seen a green tote? I set it down by the door while I looked at the gardening shelf."

Iris looked at both bags again. The blue-striped tote's handles were clean. The green-striped tote's handles had a smear of potting soil. Sam's boots were muddy. Ruth's shoes were spotless. And tucked into the blue-striped tote, under the peppermints, was a receipt from the cafe next door timed half an hour earlier for two peppermint teas, which was Ruth's usual order with Nora.
""",
"ask": 'Whose tote is whose, and did anybody swap them on purpose?',
"solution": """
The blue-striped tote is Ruth's and the green-striped tote is Sam's. Nobody swapped them on purpose. They simply set them down side by side and each picked up the wrong one later.

Ruth's library card and cafe peppermint-tea receipt sit in the blue-striped tote, and her shoes are clean, matching the clean handles. Sam's seed catalogue, muddy gloves, rose-feed list and muddy boots match the green-striped tote with soil on the handles.

Iris handed each person the right bag. Sam laughed and bought the espalier book. Ruth bought nothing but a peppermint from her own packet, which she offered to Theo for his trouble. Iris tied a spare luggage tag roll to the basket with a sign that said Label me if I look like yours.
""",
"keys": ['library card with her name', 'seed catalogue', 'smear of potting soil', 'receipt from the cafe'],
},
{
"title": 'The Missing First Edition',
"kind": 'story',
"story": """
Iris kept a locked glass case near the counter for special books. Inside it sat a first edition of River Light, signed by the author on the title page. On Monday morning the case was locked, the key was on Iris's ring, and River Light was gone.

Theo had opened the shop. He swore he had not touched the case. The lock showed no scratch. The key had never left Iris's ring overnight, and Iris had locked up herself on Sunday evening with the book still inside.

Three people had been near the case on Sunday afternoon.

Greta Holm from the bakery had leaned on the case while she waited for a gift wrap, and she had left fingerprints of icing sugar on the glass. The sugar prints were still there on Monday, undisturbed.

Marcus Lee, the architect, had asked to see the first edition. Iris had unlocked the case, handed him the book, watched him read the signature, and locked it back herself. Marcus paid for a different book and left.

Harper Blythe, the travel writer, had browsed nearby and asked Theo whether signed copies ever went on silent auction for the village fair. Theo said Iris handled all of that.

Iris looked at the case again. The velvet pad where River Light had rested still held the book's rectangular dent. Beside that dent was a second, fainter dent, the same size, as if another book of the same footprint had sat there recently. On the holds shelf, wrapped in brown paper with Harper's name on it, Iris found a book of the same thickness. She unwrapped a corner. It was a later printing of River Light, unsigned. And in the glass case, pushed to the very back under the velvet fold, she found a yellow sticky that said Hold for Harper — silent auction pledge, in Theo's handwriting.
""",
"ask": 'Where is the signed first edition, and what happened?',
"solution": """
The signed first edition is in Harper Blythe's brown-paper hold on the holds shelf. Theo had wrapped it for the village fair silent auction and set Harper's unsigned later printing in the case as a temporary stand-in, meaning to tell Iris on Monday, then forgotten.

Greta only left icing sugar on the glass and never opened the case. Marcus was handed the book by Iris and watched while she locked it away. The second dent and Theo's sticky under the velvet show the planned swap for the auction pledge.

Iris unlocked the hold, confirmed the signature, laughed with relief, and wrote a proper auction card. Harper got credit for the pledge. The later printing went back to the shelves. Theo got a reminder note on the till: tell Iris before you rearrange the glass case. The silent auction raised a happy sum for the village fair, and Harper wrote a travel essay about bookshop pledges.
""",
"keys": ['second, fainter dent', 'Hold for Harper', 'later printing of River Light, unsigned'],
},
{
"title": 'The Wrong Order Slip',
"kind": 'story',
"story": """
Special orders at Willow Quill Books were written on pink slips and clipped to a board behind the counter. On Wednesday, Linnea Shaw from the flower shop came to collect a book she had ordered about Victorian nosegays. Theo handed her a wrapped parcel from the special-order shelf. Linnea opened it at the counter and stared.

"This is a book about Victorian railways," she said. "I ordered nosegays."

Iris checked the pink slips. There were two slips with similar handwriting, both dated the same day. One said L. Shaw — Victorian nosegays. The other said L. Shaw — Victorian railways. Both had been ticked as arrived.

Linnea swore she had only ordered nosegays. She had never cared about railways.

Three people had written slips that week: Theo, Iris, and Jules Wren, the art teacher, who sometimes took phone orders when Iris was with a customer.

Jules arrived for her lunch break browsing. Iris showed her both slips. Jules peered at them. "I took a phone order for an L. Shaw on Monday," she said. "The caller wanted Victorian railways. I wrote the slip and clipped it up."

Iris rang the number on the railways slip. A man answered. "This is Leo Shaw," he said. "Did my railway book come in? I ordered it for my father."

Linnea's eyes widened. "Leo is my cousin. We have the same initial. He must have given this shop number as a pickup."
""",
"ask": 'Why were there two slips for L. Shaw, and who should get which book?',
"solution": """
There were two different customers with the same initial and surname. Linnea Shaw ordered Victorian nosegays. Her cousin Leo Shaw ordered Victorian railways by phone, and Jules wrote that slip. Both parcels arrived, and Theo matched the surname without checking the first name.

Iris gave Linnea the nosegays book and set the railways book aside for Leo. Jules promised to write first names in full on every future slip. Theo redrew the special-order board with a bigger Name column. Leo collected his railways book with a grin and promised to send Linnea a postcard from the steam museum.
""",
"keys": ['L. Shaw — Victorian nosegays', 'L. Shaw — Victorian railways', 'This is Leo Shaw'],
},
{
"title": 'The Coffee Ring Clue',
"kind": 'story',
"story": """
Iris found a brand-new paperback of Coastal Paths on the window seat with a brown coffee ring on its cover and a receipt tucked inside as a bookmark. The receipt was from Nora's cafe, timed that morning, for one oat-milk latte. The book had not been paid for. It still had the shop's price sticker.

Theo said three people had sat on the window seat that morning with drinks from next door.

Greta Holm had come in with a paper cup, browsed baking memoirs, and left her cup on the counter, not on the window seat. The counter had a matching ring that morning, which Theo had wiped.

Owen Hart had sat on the window seat with a black coffee, read the first chapter of a biography, and bought it. His cup had a cardboard sleeve. Coastal Paths was not a biography.

Pip Marlowe, a teenager who helped Nora after school and sometimes on weekend mornings, had dashed in with an oat-milk latte for herself, set it on the window-seat ledge, and pulled Coastal Paths from the shelf to see whether it mentioned her aunt's village. She had been called back to the cafe before she finished the page.

Iris turned the receipt over. On the back, in pencil, someone had written Aunt May — page forty. The handwriting matched the cafe order pad Nora kept for Pip's shift notes.
""",
"ask": 'Who left the unpaid book on the window seat with the coffee ring?',
"solution": """
Pip Marlowe left it.

Greta's cup sat on the counter, not the window seat. Owen drank black coffee with a sleeve and bought a biography. Pip had an oat-milk latte, which matches the receipt, sat on the window seat with Coastal Paths, and wrote about her Aunt May on the back in the same hand as her cafe shift notes. She was called away before she could buy the book.

Iris walked the book next door. Pip paid at once, kept the receipt as a proper bookmark, and promised to finish her drinks at the cafe before browsing. Coastal Paths sold three more copies that week after Pip told her aunt, which Iris considered a fair trade for one coffee ring.
""",
"keys": ['oat-milk latte', 'Aunt May — page forty', 'cafe order pad Nora kept for Pip'],
},
{
"title": 'The Reading Circle Seats',
"kind": 'logic',
"story": """
On Friday evening Iris set four chairs in a straight row in the back room for a short reading circle. She counted the chairs from the door to the window. Chair one was nearest the door. Chair four was the window seat, where she had left a thin pamphlet of reading questions on the cushion.

Pearl Ashford, Owen Hart, Clara Moss and Mabel Finch each sat in one chair. When Iris came back with the tea tray, the pamphlet was gone from chair four, and nobody would say who had sat where.

They did agree on four facts.

Pearl did not sit in chair one or chair four.

Owen sat somewhere to the left of Clara, meaning Owen's chair number was smaller than Clara's.

Mabel sat beside Pearl. Beside means their chair numbers differ by exactly one.

Clara did not sit in chair four.

Iris also knew that whoever sat in chair four had tucked the pamphlet into a bag to keep it safe, and she wanted it back before the questions began.

Here are the facts again. Four chairs in a row, one through four from door to window. Pearl is not in one or four. Owen's number is smaller than Clara's. Mabel is beside Pearl. Clara is not in four. Who sat in the window chair, chair four?
""",
"ask": 'Who sat in chair four, and where did each person sit?',
"solution": """
Mabel Finch sat in chair four. The only arrangement that fits every clue is Owen in chair one, Clara in chair two, Pearl in chair three, and Mabel in chair four.

Pearl must be in two or three. Clara is not in four, and Owen must have a smaller number than Clara, so Owen cannot be in four either. That leaves Mabel for the window chair. If Mabel is in four, Pearl must be beside her in three. The remaining chairs, one and two, go to Owen and Clara with Owen's number smaller, so Owen is in one and Clara is in two.

Mabel blushed and pulled the pamphlet from her knitting bag. She had sat by the window for the light and tucked the questions away so Quill the cat would not sit on them.
""",
"keys": ['Pearl did not sit in chair one or chair four', 'Owen sat somewhere to the left of Clara', 'Mabel sat beside Pearl', 'Clara did not sit in chair four'],
},
{
"title": 'The Unsigned Note',
"kind": 'story',
"story": """
Iris found a folded note under the till drawer on Tuesday. It was written in blue ink on cream paper and said, Please hold the new garden memoir for me. I will pay on Friday. There was no name.

Theo said three people had asked about the garden memoir that week.

Sam Quinn had asked whether it was in yet, then said he would wait until payday and left without writing anything.

Dot Bramble from the antique shop had browsed gardening, then written something at the counter while Iris wrapped a gift for another customer. Dot always carried a fountain pen with blue ink.

Edna Voss, the choir director, had asked Theo to put her name on a hold if a second copy arrived. Theo had written Edna Voss on a pink slip himself, in pencil.

Iris held the cream note to the light. The cream paper matched the small stack of note cards Dot sold at the antique shop and had left as samples by the till the week before. And in the corner of the note, almost rubbed away, was a tiny embossed antique-shop mark that Dot stamped on every card she sold.
""",
"ask": 'Who wrote the unsigned hold note?',
"solution": """
Dot Bramble wrote it.

Sam wrote nothing. Theo wrote Edna's hold himself in pencil on a pink slip. The cream note is blue fountain-pen ink on Dot's own embossed sample cards, which matches Dot writing at the counter while Iris was busy.

Iris rang Dot, who laughed and said she had meant to sign it and been distracted by the gift wrap. The memoir went on hold under Dot's name, to be paid on Friday as promised. Dot paid on Friday as promised and bought a second garden memoir for the antique-shop window.
""",
"keys": ['fountain pen with blue ink', 'embossed antique-shop mark', 'cream paper matched the small stack'],
},
{
"title": 'The Cat Who Liked Mysteries',
"kind": 'story',
"story": """
Quill the bookshop cat had a favourite shelf: mystery, third from the bottom, where the afternoon sun made a warm stripe. On Thursday, Iris found three paperbacks on the floor beneath that shelf, and one hardcover mystery missing from its place: The Lantern Key, a shop favourite with a bright yellow spine.

Theo picked up the paperbacks. "Quill knocks paperbacks down," he said. "He cannot move a hardcover that heavy."

Three people had been in mystery that morning.

Ruth Ellery had been looking for a gentle puzzle mystery and had carried two paperbacks to the counter, paid, and left. Both were still in her bag when Iris checked later with a quick call.

Jules Wren had sketched the yellow spine of The Lantern Key for an art-class still life, standing with a pencil and a pad, then moved on to cookbooks.

Benji Crowe had rested his heavy mail satchel on the mystery shelf while he sorted a few shop letters for Iris, then swung the satchel back onto his shoulder and left through the front door.

Iris looked at the empty gap where The Lantern Key had been. On the shelf lip there was a smear of yellow dust from the spine's dye. On the side of Benji's satchel, which he had set down again by the counter while he drank a quick tea, there was a matching yellow smear. And inside the satchel's outer pocket, Iris saw a bright yellow corner.
""",
"ask": 'Where is The Lantern Key, and how did it leave the shelf?',
"solution": """
The Lantern Key slid into Benji Crowe's mail satchel when he rested the satchel on the mystery shelf. It was not a deliberate taking. The yellow spine dye on the shelf lip matches the smear on the satchel, and the yellow corner is visible in the outer pocket.

Ruth bought two different paperbacks. Jules only sketched. Quill can knock paperbacks down but not lift a heavy hardcover into a satchel.

Benji was horrified and delighted in equal measure. He returned the book at once, bought it properly as an apology, and promised to set his satchel on the floor from then on. Quill returned to the sun stripe and pretended he had solved it first. The Lantern Key became Benji's favourite lunchtime read on his mail rounds, carefully kept away from the satchel's outer pocket.
""",
"keys": ['smear of yellow dust', 'matching yellow smear', 'bright yellow corner'],
},
{
"title": 'The Mixed-Up Holds',
"kind": 'story',
"story": """
The holds shelf at Willow Quill Books used brown paper parcels labelled with first names in large marker. On Saturday, Pearl Ashford opened a parcel labelled Pearl and found a book about deep-sea fishing. Pearl hated boats.

Theo checked the hold list. Pearl had reserved The Orchard Clock. Owen Hart had reserved Deep Water Fishing. Both parcels had been wrapped the evening before by Theo, who admitted he had labelled them while talking to Nora through the open door and might have mixed the names.

Two parcels sat on the shelf labelled Pearl and Owen. Iris opened a corner of the Owen parcel. Inside was The Orchard Clock. So the books had been swapped in the wrapping, or the labels had been swapped after wrapping.

Nora said she had come in early that morning to return Iris's umbrella and had tidied the holds shelf because the parcels were leaning. She had set them upright. She swore she had not opened them.

Iris looked at the marker labels. Theo always wrote with the shop's black marker. The Pearl label was black. The Owen label was black too. But under the Owen label, a corner of an older label peeked out, and when Iris peeled it back she found Theo's original Owen written underneath, and under the Pearl label she found Theo's original Pearl. Both current top labels were in a slightly different hand, with a rounder O.

Nora's cafe chalk menu used that same rounder O every morning.
""",
"ask": 'Who swapped the hold labels, and which parcel should each person get?',
"solution": """
Nora Peake swapped the outer labels while tidying, without opening the parcels. She had meant to help and had mixed which name went on which parcel. Theo's original labels underneath still matched: the parcel with Deep Water Fishing was originally Owen's, and the parcel with The Orchard Clock was originally Pearl's. After Nora's swap, the names on the outside disagreed with the books inside.

Iris restored Theo's labels, gave Pearl The Orchard Clock and Owen the fishing book. Nora brought them both a free pastry by way of apology, and Theo started writing holds on tags tied through the string instead of on the paper. Pearl finished The Orchard Clock in two evenings and told Owen the fishing book smelled faintly of cafe chalk, which made them both laugh.
""",
"keys": ['under the Owen label', 'slightly different hand, with a rounder O', 'cafe chalk menu used that same rounder O'],
},
{
"title": 'The Dusty Ladder',
"kind": 'story',
"story": """
The tallest shelf at Willow Quill Books held oversized art books. Iris kept a wooden ladder on a rail for that wall. On Monday, she found the ladder left at the far end of the rail, dusty handprints on the sides, and an oversized book about cathedral windows lying flat on top of the lower shelf instead of upright in its place.

Theo said he had not climbed the ladder since the Friday before.

Three people had asked about tall shelves over the weekend.

Marcus Lee had wanted a book on cathedral architecture for a client. Iris had climbed the ladder herself on Saturday morning, handed him the cathedral-windows book, and watched him page through it at the counter. He had not bought it. Iris had put it back herself and left the ladder at the centre of the rail.

Jules Wren had come on Saturday afternoon to photograph spine colours for a collage. She said she never climbed. She stood on the floor with her camera.

Harper Blythe had come late Saturday and asked Theo, who was alone closing, whether she could look at the oversized travel atlases. Theo had been counting the till and told her the ladder was free if she was careful.

Iris looked at the dusty handprints. They were small, with a smudge of blue paint on the right print's index finger. Jules had been teaching an art class that morning and still had a fleck of blue paint on her right index finger. Harper's hands were clean. And the cathedral-windows book, when Iris opened it, had a receipt from Jules's usual art-supply shop tucked in as a page marker, dated Saturday afternoon.
""",
"ask": 'Who left the ladder and the oversized book out of place?',
"solution": """
Jules Wren did.

Marcus looked at the book with Iris and Iris reshelved it. Harper's hands were clean, and the blue paint and art-supply receipt point to Jules, who claimed she never climbed but left paint-dusted prints on the ladder and her receipt in the cathedral book.

Jules admitted she had climbed after her photograph session to look at the window plates for a collage idea, then left in a hurry when her bus was due. Iris smiled, shelved the book, rolled the ladder to its home mark, and sold Jules a paperback on stained glass that did not need a ladder at all. Jules's collage later hung in the shop for a month, cathedral windows and all, with a small card thanking the ladder.
""",
"keys": ['smudge of blue paint', 'fleck of blue paint on her right index finger', "receipt from Jules's usual art-supply shop"],
},
{
"title": 'The Special Order Mix-up',
"kind": 'story',
"story": """
A customer named Greta Holm had ordered a baking memoir called Flour and Time. When it arrived, Theo wrapped it and set it on the special-order shelf. An hour later Greta came in, paid, and left with a parcel. Ten minutes after that, Greta rang the shop in a panic.

"I opened the parcel at the bakery," she said. "It is a hiking guide called Flour of the Peaks. I cannot hike. I bake."

Iris checked the special-order shelf. A second parcel remained, labelled G. Holm. She opened a corner. Flour and Time.

Theo went pale. "There was a phone order this morning for G. Holm," he said. "A hiking guide. I thought it was Greta. I wrapped both when they arrived together."

Iris checked the phone-order slip. The number was not the bakery. It belonged to a man named Gordon Holm in the next village, who answered and said yes, he had ordered Flour of the Peaks for a walking holiday, and he had asked for pickup under G. Holm.

Greta arrived back, laughing now, and swapped parcels with Iris. Gordon collected his hiking guide that afternoon.
""",
"ask": 'How did Greta end up with the hiking guide?',
"solution": """
Theo wrapped two different orders for two different people who shared the initial G and the surname Holm: Greta Holm the baker and Gordon Holm the walker. He handed Greta the wrong parcel because both were labelled G. Holm.

Iris started writing full first names on special-order labels that afternoon. Greta bought Flour and Time properly. Gordon got his peaks. Theo kept the empty hiking-guide wrap as a reminder on the back-room wall. Gordon sent a walking postcard to the shop from the peaks, addressed to G. Holm care of Willow Quill, which Theo framed as a warning.
""",
"keys": ['phone order this morning for G. Holm', 'Gordon Holm', 'second parcel remained, labelled G. Holm'],
},
{
"title": 'The Moved Map',
"kind": 'logic',
"story": """
A rare fold-out map of Maple Lane as it was a hundred years ago lived in a flat drawer under the counter. On Wednesday the drawer was shut and the map was missing. It turned up an hour later on the local-history shelf, carefully refolded, with no harm done. Iris still wanted to know who had moved it without asking.

Four people had been behind the counter that morning for one reason or another: Theo Vale, Jules Wren, Marcus Lee and Dot Bramble. Each made a statement. Iris knew that the person who moved the map was fibbing, and the other three were telling the truth.

Theo said, "Jules did not move the map."

Jules said, "It was Theo or Marcus who moved it."

Marcus said, "I did not move it, and Dot did not move it either."

Dot said the same as Jules: "It was Theo or Marcus who moved it."

Here are the facts again. Exactly one of the four moved the map. That one is fibbing. The other three are telling the truth. Theo says Jules did not move it. Jules says it was Theo or Marcus. Marcus says it was not me and not Dot. Dot repeats Jules. Who moved the map?
""",
"ask": 'Who moved the map?',
"solution": """
Marcus Lee moved the map.

If Marcus is the one fibbing, then Theo's statement is true, so Jules did not move it. Jules's statement is true, so it was Theo or Marcus, and since Jules is truthful and Marcus is the fibber, it was Marcus. Marcus's own statement is false, which fits because he did move it. Dot's repeat of Jules is true. No other culprit fits all four statements at once.

Marcus admitted he had wanted to compare the old lane to a client's plot and had meant to ask. Iris thanked him for refolding it properly and started a sign-out card for the flat drawer. The sign-out card for the flat drawer filled with neat architect handwriting for the rest of the month.
""",
"keys": ['Jules did not move the map', 'Theo or Marcus', 'I did not move it, and Dot did not', 'the person who moved the map was fibbing'],
},
{
"title": 'The Lost Reading Glasses',
"kind": 'story',
"story": """
Iris kept a spare pair of reading glasses in a soft blue case beside the till for customers who forgot their own. She had bought them years ago at a market stall, and half the village had borrowed them at least once. On Friday the case was open and empty.

Theo said he had seen the glasses on the counter at noon, folded neatly beside a stack of bookmarks. By three they were gone, and a customer looking for large-print gardening had to hold a book at arm's length.

Three people had used the spare glasses that afternoon.

Mabel Finch had borrowed them to read a knitting pattern's tiny type, then set them on the poetry shelf while she compared yarn colours in her bag. She said she forgot them there and meant to come back.

Owen Hart had borrowed them to check a footnote in a history hardback, then walked to the till wearing them, paid for the hardback, and asked Theo where the case was. Theo pointed. Owen said he put them back in the case and heard the little click of the lid.

Clara Moss had sat in the window seat writing, then asked if she could borrow the spare glasses for a moment to check a line break. Theo had looked at the case and found it empty, so Clara had managed without, squinting cheerfully.

Iris checked the poetry shelf. No glasses. She checked the case. Empty. She looked at Owen's shirt pocket, where a blue earpiece was peeking out above a fountain pen. Owen patted his pocket, pulled out the spare reading glasses, and groaned so loudly that Quill the cat flicked an ear from the mystery shelf.
""",
"ask": 'Who has the spare reading glasses?',
"solution": """
Owen Hart has them in his shirt pocket.

Mabel left them on the poetry shelf, but they were not there by three, and Owen later borrowed them and walked to the till still wearing them. He thought he returned them to the case and even remembered a lid click, yet Theo found the case empty when Clara asked, and Iris found the glasses in Owen's pocket. The click he remembered was probably his fountain pen cap.

Owen returned them with an apology and a promise to pat his pockets before leaving. Iris stuck a bright tag on the blue case that said Please put me back, and Mabel bought the knitting book without needing the spare pair a second time. Clara said her squinting poem was better for the struggle.
""",
"keys": ['blue earpiece was peeking out', 'walked to the till wearing them', 'found it empty'],
},
]
