"""Cases Fifteen to Twenty-Eight. Each case: title, kind (story|logic), story, ask, solution, keys."""

CASES_B = [
{
"title": 'The Library Card in the Wrong Pocket',
"kind": 'story',
"story": """
Ruth Ellery kept her old library card in her wallet for sentimental reasons, even though she bought her books at Willow Quill now. On Monday she paid for a stack of novels, put her wallet away, and later rang Iris in a panic.

"My library card is missing from my wallet," she said. "I had it when I paid."

Iris checked the counter and the card machine. Nothing. Theo checked the bagging shelf. Nothing.

Three people had stood at the counter while Ruth paid.

Pip Marlowe had been buying a postcard and had set her own canvas purse on the counter beside Ruth's wallet for a moment.

Benji Crowe had dropped off mail and leaned an elbow near the till.

Nora Peake had run in with change for the cafe float and scooped a handful of coins from the counter tray.

Iris asked Ruth to empty her shopping bag onto the counter. Between two novels was a thin library card. It was not Ruth's. It said Pip Marlowe, Village Library, in a teenage hand. And in Pip's canvas purse, which Pip had left on the window seat while she browsed magazines, Iris found Ruth's card tucked behind a lip-balm tube.
""",
"ask": "What happened to Ruth's library card?",
"solution": """
The two cards were swapped when Pip's purse and Ruth's wallet sat side by side on the counter. Pip picked up Ruth's card by mistake, and Ruth's novels somehow collected Pip's card between them when the stack was bagged.

Benji only leaned. Nora only took coins from the tray. The cards themselves prove the swap.

Iris traded the cards back. Pip bought a magazine. Ruth bought a tea next door and said she would keep her sentimental card in a zipper pocket from then on. Ruth renewed her sentimental card at the village library the next week, just to keep the date stamps tidy.
""",
"keys": ['It said Pip Marlowe', "found Ruth's card tucked behind a lip-balm tube", "beside Ruth's wallet"],
},
{
"title": 'The Torn Page Corner',
"kind": 'story',
"story": """
A customer returned a paperback with the corner of page one hundred torn off. Iris did not mind gently used books, but she wanted to know whether it had happened in the shop before the sale or afterward.

The buyer was Edna Voss, who swore the corner had been whole when she left the shop the day before. She had noticed the tear that morning at choir practice when she opened to her bookmark.

Theo remembered three people handling that very paperback the previous afternoon, when it was still a shelf copy.

Greta Holm had picked it up, read the back, and set it down to buy a baking book instead.

Marcus Lee had used it to prop open a large architecture folio for a minute while he compared a floor plan, then put both books back.

Clara Moss had sat with it in the window seat and torn a tiny scrap from her own notebook to mark a line she liked, then bought a different poetry book.

Iris looked at Edna's paperback. The torn edge was clean and slightly curved, the way a page tears when it catches on a ring. Marcus wore a wide silver ring on his right hand. Greta wore no rings. Clara's notebook scrap was still in the poetry book she had bought, unused as a bookmark after all. And on the architecture folio Marcus had handled, Iris found a tiny triangle of paperback paper caught in the endpaper.
""",
"ask": 'Who tore the corner, and when?',
"solution": """
Marcus Lee tore it while the book was still a shelf copy, when he used it to prop open the folio. His ring caught the page, and the tiny triangle of paper in the folio's endpaper matches the missing corner.

Greta only read the back. Clara tore a scrap from her notebook, not from the paperback. Edna received a book that was already torn.

Iris apologised to Edna, replaced the paperback with a fresh copy at no charge, and asked Marcus to use a proper book weight next time. Marcus bought the folio and a wooden weight from the counter display. Edna used her fresh copy at choir with a proper ribbon bookmark and never propped anything with a paperback again, she said, eyeing Marcus.
""",
"keys": ['wide silver ring', 'tiny triangle of paperback paper', 'used it to prop open a large architecture folio'],
},
{
"title": 'The Queue at Closing',
"kind": 'logic',
"story": """
Five minutes before closing, five people lined up at the counter to collect holds. Iris counted places from the front of the queue to the back. Place one was first to be served. Place five was last.

The five people were Nora Peake, Benji Crowe, Edna Voss, Greta Holm and Pip Marlowe. After the rush, Iris could not remember who had stood immediately behind Nora, and she needed to know because that person's hold had been handed to Nora by mistake.

They agreed on the following.

Nora was in place three.

Benji was in place one.

Greta was not in place five, and Greta was not standing beside Benji.

Pip's place number was higher than Edna's, meaning Pip was somewhere behind Edna.

Here are the facts again. Five places, one at the front through five at the back. Nora is in three. Benji is in one. Greta is not in five and not beside Benji. Pip is behind Edna. Who stood immediately behind Nora?
""",
"ask": 'Who stood immediately behind Nora in the queue?',
"solution": """
Greta Holm stood immediately behind Nora, in place four.

Benji is in one and Nora is in three, so place two is between them. Greta cannot be beside Benji and cannot be in five, so Greta cannot be in two and cannot be in five. The only place left for Greta is four. Places two and five then go to Edna and Pip with Pip behind Edna, so Edna is in two and Pip is in five.

Iris found Greta's hold in Nora's bag of cafe napkins, swapped it back, and locked the door two minutes late with everyone smiling. Pip, last in line, said she had enjoyed the view of everyone's hats, and bought a postcard of a queue for Nora's cafe noticeboard.
""",
"keys": ['Nora was in place three', 'Benji was in place one', 'Greta was not in place five', "Pip's place number was higher than Edna's"],
},
{
"title": 'The Mystery Dedication',
"kind": 'story',
"story": """
A second-hand hardback arrived in a donation box with a dedication on the flyleaf: For my favourite bookseller on Maple Lane, with thanks for every rainy afternoon. It was signed only with the initial H.

Iris felt sure it was meant for her shop, but she wanted to know who H was before she shelved it in the staff favourites section.

Three regulars had names beginning with H: Harper Blythe, and two others who were less likely, a quiet man named Hugh who came once a month, and a child named Holly who only read picture books.

Theo found a matching bookmark tucked deep in the middle, a thin strip of ticket stub from a travel lecture Harper had given at the village hall the previous winter. On the back of the stub, in the same hand as the dedication, was a note: Iris — this copy has the chapter you asked about.

Harper came in that afternoon for a new notebook. Iris showed her the flyleaf. Harper grinned.
""",
"ask": 'Who wrote the dedication, and who was it for?',
"solution": """
Harper Blythe wrote it for Iris.

The travel-lecture ticket stub bookmark, the note naming Iris, and the initial H all point to Harper. Hugh never gave lectures, and Holly could not have written that hand.

Harper said she had meant to bring the book by in person and had dropped it in the donation box by mistake when she cleared her shelf. Iris shelved it in staff favourites with a small card that said Gift from a traveller, and bought Harper the notebook as a thank-you. The staff favourites shelf gained a small willow-leaf sticker so other gifts would not be mistaken for donations.
""",
"keys": ['ticket stub from a travel lecture Harper', 'Iris — this copy has the chapter you asked about', 'signed only with the initial H'],
},
{
"title": 'The Umbrella Stand Switch',
"kind": 'story',
"story": """
The umbrella stand by the door of Willow Quill Books held three umbrellas on a wet afternoon: Iris's own navy one, Nora's yellow one on loan again, and a stranger's black one with a carved duck-head handle.

At five o'clock a woman in a green coat hurried in, grabbed the duck-head umbrella, and hurried out. Two minutes later an elderly man came in looking damp and confused.

"Someone has taken my duck-head umbrella," he said. "I left it while I browsed gardening."

Iris looked at the stand. Navy, yellow, and a plain black umbrella with a plastic handle remained. The plain black one had a luggage tag that said Property of Mabel Finch.

Mabel arrived moments later, dry under a different umbrella. "I took the wrong one when I left an hour ago," she said. "Mine is the plain black with the tag. I brought this duck-head back as soon as I noticed."

The elderly man took his duck-head with relief. The woman in the green coat was gone. Theo ran to the corner and saw her under a plain black umbrella, already turning back toward the shop with a sheepish look. She had grabbed Mabel's tagged umbrella after Mabel had taken the duck-head, and now everyone could sort it out.
""",
"ask": 'Whose umbrella ended up with whom, and how was it resolved?',
"solution": """
Mabel accidentally took the elderly man's duck-head umbrella, leaving her own tagged plain black one. The woman in the green coat then took Mabel's tagged umbrella, thinking it was hers or simply grabbing the remaining black one. Mabel returned the duck-head when she noticed. The green-coated woman returned Mabel's tagged umbrella. Iris's navy and Nora's yellow never moved.

Iris put a small sign on the stand: Please check the handle. The elderly man bought a gardening book. Mabel bought nothing but a dry pair of socks from her bag for the man, who refused them with a laugh. The duck-head umbrella became a shop legend, and Iris refused three offers to buy a fake one for the window.
""",
"keys": ['Property of Mabel Finch', 'brought this duck-head back', 'plain black umbrella with a plastic handle'],
},
{
"title": 'The Cookbook Stain',
"kind": 'story',
"story": """
A display copy of Harvest Kitchen developed a small jam stain on page twelve. Iris did not sell that copy. She wanted to know which browsing baker had been eating in the aisle.

Greta Holm admitted she had browsed that page but swore her hands were clean. She had washed them at the cafe before coming in.

Nora Peake said she had brought Greta a jam tart sample on a napkin, set it on the cookbook for a second while she hugged Greta, then taken it back to the cafe when Greta said she was working.

Pip Marlowe said she had wiped a shelf with a damp cloth near cooking and might have bumped the book.

Iris looked at page twelve. The stain was the shape of a tart bottom, round with a faint pastry ridge. On the napkin Nora still had in her apron pocket, there was a matching round jam print. Greta's sleeves were floury but not jammy. Pip's cloth was dusty water, not red.
""",
"ask": 'How did the jam stain get on page twelve?',
"solution": """
Nora set the jam tart sample on the open cookbook while she hugged Greta. The tart left a round stain. Nora did not do it to spoil the book. She simply used the nearest flat surface for a second.

Iris moved the stained copy to the staff kitchen shelf as a working cookbook and put a fresh display copy out. Nora brought a plate next time. Harvest Kitchen page twelve became the staff's jam tart page, and Nora's tarts improved with the recipe.
""",
"keys": ['shape of a tart bottom', 'matching round jam print', 'set it on the cookbook for a second'],
},
{
"title": "The Signed Copy That Wasn't",
"kind": 'story',
"story": """
A customer asked for a signed copy of Clara Moss's new poetry collection. Theo found a copy on the signed shelf with a flourish on the title page that looked like Clara's name. The customer bought it. An hour later Clara herself came in for tea and browsed the signed shelf.

"That signature is not mine," she said, pointing to the next copy with the same flourish. "Someone has been practising."

Iris compared the flourishes to Clara's real signature on a flyer for poetry night. The real signature was smaller and had a long cross on the double s. The flourish copies had no long cross.

Three people had been near the signed shelf that week with pens.

Jules Wren had been lettering price cards with a black pen.

Pip Marlowe had been drawing doodles in her sketchbook with a blue pen.

Owen Hart had been correcting student essays at the window seat with a red pen.

The flourish signatures were blue. On Pip's sketchbook open on the window seat, Iris found a whole page of practice flourishes that matched the fake signatures, beside a note that said Hope Clara does not mind — surprise for Mum.
""",
"ask": 'Who signed the copies that were not really signed by Clara?',
"solution": """
Pip Marlowe practised Clara's name in blue pen and signed two shop copies as a surprise gift idea for her mother, without asking.

Jules used black ink for price cards. Owen used red. The blue flourishes and the practice page in Pip's sketchbook match.

Clara was more amused than annoyed. She signed the two copies properly over the flourishes, dedicated one to Pip's mum, and asked Pip to ask next time. Pip bought a legitimate signed copy with her wages. Pip's mother framed her properly signed page, flourish and all, which Clara said was the finest kind of revision.
""",
"keys": ['flourish signatures were blue', 'page of practice flourishes', 'surprise for Mum'],
},
{
"title": 'The Empty Reserve Shelf',
"kind": 'story',
"story": """
Teachers sometimes reserved stacks of classroom novels on a low reserve shelf in the back room, marked with a school sticker and a clipboard for notes. On Tuesday morning the shelf was empty, though Owen Hart was due to collect twenty copies of The Quiet Orchard that afternoon for his literature class.

Theo said he had counted twenty copies onto the shelf on Monday evening, stacked them with the spines facing out, and initialled the clipboard.

Three people had keys to the back room where the reserve shelf stood: Iris, Theo, and Ruth Ellery, who helped with school orders once a week as a volunteer and knew the crate routine by heart.

Ruth arrived early on Tuesday, saw the empty shelf, and looked stricken. "I moved the Quiet Orchard stack to the school crate by the back door yesterday evening after Theo left," she said. "The crate goes to the school first thing with Benji. I thought Owen knew, because last term we did it the same way. I should have written on the clipboard."

Iris checked the school crate bay. It was empty. Benji Crowe had already collected it on his morning mail run, which also carried school parcels, and his log at the counter showed School crate — Quiet Orchard x twenty, initialled.

Owen arrived a little later, heard the story, and laughed with his hands on his hips. "The school rang me an hour ago. The books are on my desk. I came here out of habit, and because I wanted a coffee next door. Mystery solved before I even asked."
""",
"ask": 'Where are the twenty classroom copies?',
"solution": """
They are at the school. Ruth moved them from the reserve shelf into the school crate after Theo shelved them, and Benji collected the crate on his morning run. Nobody took them wrongly. The empty shelf was only a communication gap between a helpful volunteer and a habitual teacher.

Iris put a chalkboard by the reserve shelf: Write what you move. Ruth wrote her first note at once in large letters. Owen bought a coffee next door for Ruth and Theo, and added a second note that said Habit is not a plan.
""",
"keys": ['moved the Quiet Orchard stack to the school crate', 'Benji Crowe had already collected it', 'The books are on my desk'],
},
{
"title": 'Poetry Night Fib',
"kind": 'logic',
"story": """
On poetry night a guest poet's small notebook went missing from the signing table and turned up twenty minutes later under a chair, with no pages harmed. Iris still wanted to know who had taken it for those twenty minutes.

Four people had been near the table: Clara Moss, Jules Wren, Harper Blythe and Edna Voss. Each made two claims. Iris knew that each person was telling exactly one truth and exactly one fib.

Clara said, "I did not take it. Jules took it."

Jules said, "I did not take it. Harper took it."

Harper said, "I did not take it. Clara took it."

Edna said, "I did not take it. Harper did not take it."

Here are the facts again. Exactly one person took the notebook for a short time. Each of the four statements-pairs contains exactly one truth and exactly one fib. Who took the notebook?
""",
"ask": "Who took the guest poet's notebook for those twenty minutes?",
"solution": """
Edna Voss took it.

If Edna took it, then Clara's first claim is true and her second is false, Jules's first is true and her second is false, Harper's first is true and her second is false, and Edna's first claim is false while her second claim, that Harper did not take it, is true. Each person has exactly one truth and one fib. No other culprit produces that pattern.

Edna admitted she had only wanted to copy a stage direction the poet had scribbled, panicked when the lights went down, and tucked the notebook under the chair to return later. The poet laughed and initialled Edna's own notebook by way of peace. The guest poet dedicated the next poem to under-chair detectives, and Edna stood to take a bow.
""",
"keys": ['I did not take it. Jules took it', 'I did not take it. Harper took it', 'I did not take it. Clara took it', 'I did not take it. Harper did not take it'],
},
{
"title": 'The Sticky Fingerprint',
"kind": 'story',
"story": """
Iris used a rubber date stamp on due slips and special-order tickets. She was fond of the solid thunk it made. On Thursday the stamp pad was found open and drying beside the till, with a sticky purple fingerprint on the counter beside it, glittering faintly in the afternoon light.

Theo said he had stamped three holds before lunch, closed the pad firmly, and wiped the counter. He remembered the lid clicking shut.

Three people had leaned on the counter after lunch.

Greta Holm had paid with a card and taken her receipt, hands clean from the bakery wash station.

Sam Quinn had signed for a delivery of seed catalogues meant for the gardening window and left a soil smudge on the far edge of the counter, nowhere near purple.

Linnea Shaw had wrapped a gift bouquet for a customer at Iris's request, standing at the counter with ribbon and scissors, and had purple ribbon dye on her fingers from a wedding order at the florist shop that morning.

Iris looked at the fingerprint. It was purple and slightly glittery, the same glitter Linnea mixed into her ribbon dye for wedding orders. Linnea's left thumb still sparkled when she waved. And the stamp pad's lid had a matching glittery purple thumbprint on the underside, as if someone had pressed it shut with a dyed hand after opening it to look at the novelty of a bookshop stamp.
""",
"ask": 'Who opened the stamp pad after Theo closed it?',
"solution": """
Linnea Shaw opened it out of curiosity while wrapping the bouquet at the counter, then pressed the lid shut with her glittery purple thumb. She had only wanted to see the date backwards on the rubber.

Greta left no purple. Sam left soil, not purple glitter. The glitter dye and the lid print match Linnea.

Linnea apologised and bought a new stamp pad from Iris's supplier list, plus a bookmark for the wedding couple. Iris laughed and said the due slips would be fashionable for a day, and Theo stamped a scrap of paper as a test and declared the thunk restored.
""",
"keys": ['purple ribbon dye', 'glittery purple thumbprint', 'left thumb still sparkled'],
},
{
"title": 'The Late Night Lights',
"kind": 'story',
"story": """
On Sunday evening Iris locked Willow Quill Books at six, checked the front windows, and walked home along Maple Lane with a bag of returns. At eight, Nora rang her from the cafe flat upstairs next door. "The shop lights are on," Nora said. "I can see a warm glow through the back window. I thought you should know before I worry."

Iris returned with her keys. The front door was locked. Her key still worked, and the street lock showed no scratch. Inside, the main shop was dark, but the back-room lamp was on, casting a pool of light over the armchair and the reserve shelf. Quill the cat sat under it looking pleased with himself. The lamp switch was the old pull-cord type, low enough for a jumping cat, with a wooden knob polished by years of hands.

Theo had left at five after restocking. He swore the back-room lamp was off, because he always tugged the cord twice to be sure.

Marcus Lee had walked past at seven on his way home from a site visit and said he thought he saw movement inside, a quick shadow, but assumed it was Iris restocking late.

Ruth Ellery had a spare key for school-crate mornings and said she had not used it that weekend. Her key was still on the hook in her kitchen, she added, when Iris rang to check.

Iris looked at the pull cord. There were cat hairs on the wooden knob, and a faint claw scuff on the wall beside the lamp, at Quill's favourite jumping height from the armchair. A paperback on the armchair seat was slightly skewed, as if something had launched from it.
""",
"ask": 'Who turned the back-room lamp on?',
"solution": """
Quill the cat turned it on by pulling the cord after jumping from the armchair. The door was locked, Theo left with the lamp off, Ruth did not use her key, and Marcus only walked past. The cat hairs on the knob, the claw scuff, and the skewed paperback launch pad match Quill's habits.

Iris turned the lamp off, moved the armchair two feet farther from the cord, and gave Quill a treat for night watch. Nora got a free chapter from a mystery paperback for the tip-off, and Theo found a note on Monday that said The night clerk has fur.
""",
"keys": ['cat hairs on the wooden knob', 'claw scuff on the wall', 'low enough for a jumping cat'],
},
{
"title": 'The Gift Card Clue',
"kind": 'story',
"story": """
A gift card for Willow Quill Books was found on the floor near the biography shelf with no receipt tucked beside it. It still had twenty pounds on it when Theo checked the balance on the till. Iris wanted to return it to its owner before anyone else spent it, because gift cards found on floors have a way of growing legs.

The gift-card envelope nearby, half under the biography shelf lip, had a short message written in purple ink: Happy birthday Owen — from your class.

Owen Hart's birthday was the next day. Iris set the card aside for him and put a note on the till.

But Owen came in that afternoon with a smile and a tote and said his class had already given him a different gift card at school that morning, presented with cupcakes. He showed Iris one with a school sticker on the back and a different serial number.

Theo checked the sales log. Two gift cards had been sold the previous week. One was bought by Pearl Ashford with her usual debit card. One was bought by a cash customer who did not leave a name.

Pearl arrived for book club setup, saw the floor card on the till, and put a hand to her cheek. "That is the one I bought for Owen," she said. "I must have dropped it when I pulled out my knitting magazine from my bag by biography. The class collection was separate. We all chipped in at school for the sticker one. I wanted him to have something from me as well."
""",
"ask": 'Who should get the gift card found on the floor?',
"solution": """
Owen Hart should get it, as Pearl intended. Pearl bought it as her own birthday gift for him and dropped it by biography while wrestling a knitting magazine from her bag. The class gave him a different card at school with a sticker. Both gifts are real. The floor card is Pearl's, matching her sale in the log.

Iris tucked the card into Owen's birthday hold of a new history hardback and tied it with string. Pearl bought a replacement knitting magazine. Owen said it was the best sort of double birthday, and promised not to spend either card on red pens alone.
""",
"keys": ['Happy birthday Owen — from your class', 'bought by Pearl Ashford', 'class had already given him a different gift card'],
},
{
"title": 'The Whispered Title',
"kind": 'story',
"story": """
A shy customer asked Theo for a book in a near-whisper, standing half turned toward the door as if ready to leave if anyone listened too hard. Theo, who was facing the biography shelf and trying to be helpful without looming, heard The Midnight Garden and bustled off to fiction with a bright nod. The customer waited, looking worried, twisting the strap of a canvas tote.

Iris, who had been facing the customer from the till, gently asked for the title again in a soft voice of her own.

"The Midwife's Garden," the customer whispered. "Not midnight. Midwife. It is for my course reading list."

Theo returned with The Midnight Garden, a popular novel with a moon on the cover. Iris fetched The Midwife's Garden from the parenting and health shelf, a practical paperback with a green spine. The customer paid for the midwife book, tucked it deep in the tote, and smiled in relief.

Later Theo asked how Iris had known he had misheard before the customer repeated it. He had been sure about midnight.

Iris pointed to the customer's tote, which had a clinic logo and a badge that said Student Midwife pinned to the strap. She had also seen the customer's lips form the wide shape of wife rather than the tight shape of night, and she had noticed a course reading list peeking from the tote with Midwife underlined twice.
""",
"ask": "How did Iris know the whispered title was The Midwife's Garden before it was repeated?",
"solution": """
Iris saw the student-midwife badge and tote logo, watched the customer's mouth form wife rather than night, and spotted the underlined course list. Theo, who was turned partly away toward fiction, heard midnight because it was the more familiar shop title and a natural guess from a whisper.

Iris wrote Midwife on a counter card for whispered requests and taught Theo the lip shapes over tea. The customer left a thank-you note on a clinic pad, and Theo put The Midnight Garden back with a sticky that said Almost, but not quite.
""",
"keys": ['Student Midwife', 'lips form the wide shape of wife', "The Midwife's Garden"],
},
{
"title": 'The Last Bookmark',
"kind": 'story',
"story": """
On the last evening of the month, Iris found a thin paper bookmark left in the window seat copy of Coastal Paths. It was handmade, painted with a tiny willow tree and the words Thank you for the quiet shelves. There was no name.

Theo said three people had sat in the window seat that day with Coastal Paths.

Harper Blythe had sat there planning a walking chapter and left a ticket stub as a temporary bookmark, which Iris had already found and returned.

Pip Marlowe had sat there with paints from Jules's class and a jar of water, working on a tiny canvas.

Clara Moss had sat there reading and left a yellow sticky with a poem draft.

Iris looked at the painted willow. The green was the same shade Jules mixed for Pip's class that week, and the brushwork matched the tiny canvas drying on Jules's studio windowsill next door, which Pip had shown Iris that morning. On the back of the handmade bookmark, in very small letters, was To Iris and Theo — Pip.
""",
"ask": 'Who left the handmade willow bookmark?',
"solution": """
Pip Marlowe left it.

Harper used a ticket stub. Clara used a yellow sticky. The willow paint matches Pip's class colour and her tiny canvas, and the back of the bookmark names her.

Iris pinned the bookmark above the till. Theo gave Pip a free postcard. Quill the cat sniffed the willow and approved. The shop closed for the night with the kettle warm and the shelves quiet, just as the bookmark said. Iris still has the willow bookmark above the till. On quiet evenings Theo swears the painted leaves move when Quill jumps.
""",
"keys": ['same shade Jules mixed for Pip', 'To Iris and Theo — Pip', 'tiny canvas drying'],
},
]
