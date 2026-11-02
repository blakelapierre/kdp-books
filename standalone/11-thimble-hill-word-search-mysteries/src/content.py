"""Story text, suspects, hidden clues and word pools for The Thimble Hill Word Search Mysteries.
Every case is non-violent: something goes missing, and there is always a kind reason behind it."""

SLEUTH = "Hattie Bloom"

CASES = [
dict(
 title="The Blue Ribbon Jam",
 place="The Summer Fair",
 intro=("The Thimble Hill Summer Fair was in full swing. Bunting snapped in the breeze, the brass band puffed away on the bandstand, "
        "and the jam judges had just pinned a blue ribbon to the winning jar. Then they went off for a cup of tea. When they came back, "
        "the ribbon was gone. Hattie Bloom, who runs the wool shop on the high street, put down her toffee apple, called her terrier Pickle "
        "to heel, and went to have a look."),
 suspects=[
  ("Della Pruitt", "came second in the jam contest last year and the year before. She had been bottling strawberry jam all morning and her fingers were still pink."),
  ("Rupert Vane", "runs the fair. He wears a bow tie, carries a clipboard everywhere, and was due to read out the winners on the bandstand stage."),
  ("Lottie Green", "is ten years old and spent the whole day zooming between the stalls on roller skates, delivering lemonade."),
  ("Amos Hale", "keeps bees on the edge of the village. He never takes off his thick canvas gloves when his honey stall is open."),
 ],
 beats=[
  ("The judges' table stood under a striped awning. Hattie asked when the ribbon was last seen, and the judges all agreed on one thing.", "THE RIBBON VANISHED AT NOON"),
  ("On the white tablecloth, right where the ribbon had been, Hattie spotted a smudge. She bent down with her reading glasses.", "THE THIEF WORE NO GLOVES"),
  ("Behind the table the grass was soft and muddy from last night's rain. Pickle sniffed along the ground.", "NO WHEEL TRACKS IN THE MUD"),
  ("Hattie walked over to the bandstand, where the band was packing up their music stands, and asked who had been up there.", "RUPERT WAS ON STAGE AT NOON"),
  ("Back at the table, Hattie looked at the smudge again. It was a thumbprint, and it was not an ordinary color.", "THE PRINT IS PINK AND SWEET"),
  ("Pickle gave the tablecloth one long, happy sniff and wagged his tail. Hattie sniffed too.", "IT SMELLS OF STRAWBERRY"),
 ],
 culprit="Della Pruitt",
 solution=("The thief wore no gloves, so it was not Amos. There were no wheel tracks in the mud, so it was not Lottie on her skates. "
           "Rupert was on the stage at noon, in front of half the village. The thumbprint was pink and smelled of strawberry, just like "
           "Della's jam-stained fingers. Della owned up at once. She had noticed that the winning jar wore a label in her own handwriting. "
           "The labels had been swapped by mistake, and the winning jam was hers all along. She took the ribbon to prove it, then lost her nerve. "
           "The judges tasted again, agreed, and Della finally got her blue ribbon."),
 words="""STRAWBERRY BUNTING BANDSTAND JUDGES RIBBON AWNING TOFFEE LEMONADE CAROUSEL MARQUEE RAFFLE TOMBOLA PICNIC BLANKET PARASOL
 SUNSHINE HONEY BEEHIVE SCONES CREAM PRESERVE APRICOT RASPBERRY MARMALADE LABEL JARS TROPHY ROSETTE BRASS TRUMPET TUBA DRUMMER
 CLIPBOARD BOWTIE SKATES HAYBALE PONY TRACTOR WELLIES MEADOW DAISY BUTTERCUP CLOVER CUPCAKE ICECREAM WAFFLE PUNCH BALLOON KITE
 STALL BOOTH PRIZE WINNER SPOON GINGHAM APRON TEAPOT GARLAND FLAGS SUMMER""",
),
dict(
 title="The Missing First Edition",
 place="Thimble Hill Library",
 intro=("Once a year the library brings out its treasure: a signed first edition of The Hedgerow Year, a book of garden poems written "
        "by a woman who grew up on Thimble Hill. It sits in a glass case in the reading room for one afternoon only. This year, at the end "
        "of story hour, the case was open and the book was gone. In its place was a folded note. The head librarian ran straight to the wool shop "
        "to fetch Hattie Bloom."),
 suspects=[
  ("Professor Edmund Shaw", "is a visiting scholar who studies country poets. He writes all his notes in green ink with an old fountain pen."),
  ("Nell Archer", "is the librarian's assistant. She looks after the key to the glass case and stamps the books at the front desk."),
  ("Basil Thorn", "collects rare books. He fell off his bicycle last week and his right arm is in a sling."),
  ("Mira Patel", "teaches the village school. She brought her whole class in for story hour in the children's corner."),
 ],
 beats=[
  ("Hattie began with the clock. The librarian said the book was there at two and gone by three, which was exactly the time of one event.", "IT WAS TAKEN IN STORY HOUR"),
  ("Hattie peeked into the children's corner, where twenty small readers were sitting on cushions. They all told her the same thing.", "MISS PATEL READ ALL HOUR"),
  ("Next Hattie went to the front desk, where a long line of people had been waiting to borrow books.", "NELL WAS AT THE DESK"),
  ("Hattie looked closely at the glass case. Nothing was broken or scratched, and the folded note was still lying on the velvet.", "A NOTE WAS LEFT INSIDE"),
  ("She unfolded the note. It said: Sorry, I will bring it back by closing time. The writing was small and very neat.", "IT IS NEATLY HANDWRITTEN"),
  ("Hattie held the note up to the window and smiled at the color of the ink.", "THE INK IS GREEN"),
 ],
 culprit="Professor Edmund Shaw",
 solution=("The book went during story hour, and Miss Patel was reading to her class the whole time. Nell never left the front desk. "
           "The note was neatly handwritten, which Basil could not manage with his arm in a sling. The note was written in green ink, "
           "and only Professor Shaw writes in green. He had carried the book to the sunny window seat upstairs to compare the signature "
           "with an old letter in his bag. The letter was from the poet herself, to his great-grandmother, and the two were best friends. "
           "He brought the book back before closing, as promised, and gave the library the letter as a gift."),
 words="""LIBRARY READING POETRY HEDGEROW EDITION SIGNATURE BOOKMARK SHELVES CATALOG LIBRARIAN STAMP DESK CARD BORROW RETURN AUTHOR
 CHAPTER PAGES SPINE COVER JACKET VELVET GLASS CABINET FOUNTAIN PEN INKWELL NOTEBOOK PENCIL ATLAS DICTIONARY NOVEL FABLE STORY
 CUSHION LAMP WINDOW QUIET WHISPER LADDER INDEX VOLUME POEM VERSE RHYME SONNET LETTER ENVELOPE SCHOLAR READER GLOBE MAP PAPER
 RIBBON PARCHMENT QUILL BINDING TITLE PREFACE""",
),
dict(
 title="The Cherry Pie on the Sill",
 place="Larkspur Cottage",
 intro=("Bea Lark had baked her famous cherry pie for the Thimble Hill Bake-Off and set it on the kitchen windowsill to cool. "
        "The sill is outside the window and high above the garden path. At half past ten Bea went to fetch it, and the pie was gone, "
        "dish and all. The bake-off judging was at noon. Bea telephoned Hattie Bloom, who arrived with Pickle and a notebook."),
 suspects=[
  ("Tom Fenn", "is the village postman. He is very tall and was doing his morning round with his big canvas mailbag."),
  ("Rosa Lind", "lives next door and grows roses. She said she had been out all morning."),
  ("Ollie Bramble", "is eight years old and loves pie more than anything, but he is small for his age."),
  ("Gregor Bunn", "runs the bakery and is Bea's great rival in the bake-off. He always has flour on his apron."),
 ],
 beats=[
  ("Bea said the pie was on the sill at ten. Hattie wrote it down and looked up at the window.", "THE PIE WAS THERE AT TEN"),
  ("Hattie stood on tiptoe and could only just touch the sill herself. She made a note.", "THE SILL IS VERY HIGH UP"),
  ("Next door, Hattie found Rosa's husband trimming the hedge. He told her where Rosa had been.", "ROSA WAS AT THE DENTIST"),
  ("Hattie walked down to the bakery. The shop was full of customers, and the ovens were roaring.", "GREGOR NEVER LEFT HIS SHOP"),
  ("Back at the cottage, Pickle found a few dark red drops on the path, leading toward the front gate.", "JUICE DRIPPED ON A MAILBAG"),
  ("Hattie looked at the sill again and found three black feathers and a lot of little scratch marks.", "A BIG CROW WAS ON THE SILL"),
 ],
 culprit="Tom Fenn",
 solution=("The sill was very high, too high for little Ollie. Rosa was at the dentist and Gregor never left his busy shop. "
           "That left Tom, the tall postman, and the cherry juice on his mailbag. Tom had seen a big crow pecking at the crust. "
           "He shooed it away, then tucked the pie safely into Bea's parcel box by the front door, where it dripped on his bag. "
           "He meant to tell her, but he was running late for his round. The pie was fine, apart from one small crow peck, and "
           "Bea won second prize. She gave Tom a slice."),
 words="""CHERRY PASTRY CRUST LATTICE OVEN ROLLING PIN FLOUR BUTTER SUGAR DOUGH KITCHEN WINDOWSILL COTTAGE GARDEN PATH GATE ROSES
 HEDGE POSTMAN MAILBAG PARCEL LETTER STAMP BAKERY BREAD MUFFIN CRUMBLE CUSTARD WHISK SPOON BOWL APRON TEAPOT KETTLE CROW FEATHER
 NEST ORCHARD BLOSSOM PICNIC SLICE DISH PLATE TRAY JUDGES PRIZE NUTMEG CINNAMON VANILLA LEMON TART SCONE BISCUIT SPRINKLE MIXER""",
),
dict(
 title="The Gnome Who Walked Away",
 place="Mossbank Garden",
 intro=("Wendell Moss has the tidiest garden on Thimble Hill, and in the middle of it stands Sir Pumpernickel, a garden gnome with a red hat "
        "and a fishing rod. The Best Garden judge was due at three. At a quarter past two, Wendell went out to give Sir Pumpernickel a polish, "
        "and found only a round mark in the soil where he used to stand. Hattie Bloom was there in five minutes."),
 suspects=[
  ("Clara Bell", "lives across the lane and says gnomes are silly. She wears smart shoes with tall, thin heels."),
  ("Jasper Quill", "is the Best Garden judge. He drives a little green car and is never early for anything."),
  ("Hugo Penn", "is a teenager who delivers the newspapers on his bicycle."),
  ("Mabel Rook", "paints pictures of village gardens. There is usually a dab of blue paint somewhere on her."),
 ],
 beats=[
  ("Wendell said he last saw Sir Pumpernickel at lunch, and he was gone at a quarter past two.", "THE GNOME WAS GONE BY TWO"),
  ("Hattie asked about the judge. Wendell checked his watch and pointed at the little green car pulling up.", "JASPER CAME AT THREE"),
  ("Hattie looked at the garden gate and found a fresh smear on the latch.", "BLUE PAINT ON THE GATE"),
  ("The flower bed around the empty spot was soft, freshly raked soil. Hattie knelt down to look.", "NO HEEL MARKS IN THE SOIL"),
  ("Next Hattie asked Hugo's mother where he had been all week.", "HUGO WAS AWAY AT SUMMER CAMP"),
  ("Through the window of a cottage up the lane, Hattie saw an easel. On it was a half-finished picture with a red hat.", "THE GNOME IS IN A PAINTING"),
 ],
 culprit="Mabel Rook",
 solution=("Jasper only arrived at three, after the gnome had gone. Clara's tall heels would have left marks in the soft soil, and there were none. "
           "Hugo was away at summer camp. The blue paint on the gate pointed to Mabel, and the picture on her easel proved it. Mabel had borrowed "
           "Sir Pumpernickel to paint his portrait as a surprise for Wendell's birthday. She carried him back at once, the judge gave Wendell's "
           "garden first prize, and the portrait now hangs over Wendell's fireplace."),
 words="""GNOME GARDEN FLOWERBED TULIP DAFFODIL LUPIN FOXGLOVE HOLLYHOCK SUNFLOWER PEONY LAVENDER ROSEMARY TROWEL SPADE RAKE HOSE
 WATERING CAN WHEELBARROW GREENHOUSE POTTING SHED SEEDLING COMPOST BIRDBATH FOUNTAIN PEBBLE PATHWAY TRELLIS IVY HEDGE LAWN MOWER
 SNAIL LADYBIRD WORM BUTTERFLY ROBIN EASEL PAINTBRUSH CANVAS PALETTE PORTRAIT JUDGE PRIZE FISHING ROD HAT BEARD MUSHROOM TOADSTOOL
 GATE LATCH FENCE ARCH BENCH SUNDIAL""",
),
dict(
 title="The Quilt Square",
 place="The Quilting Bee",
 intro=("Every Thursday the Thimble Hill quilters meet in the village hall. For a year they have been making a quilt for the hall's hundredth "
        "birthday, and its center square shows a stitched map of the whole village. On Thursday afternoon, after the tea break, "
        "the center square was gone from the work table. Hattie Bloom was a quilter herself, so she was already in the room."),
 suspects=[
  ("Agnes Pike", "is the oldest quilter, ninety-one this spring. She always sits in the same armchair by the window."),
  ("Felix Dunn", "is the hall caretaker. He whistles while he works and carries a ring of jangling keys."),
  ("Hazel Wren", "is the youngest quilter. She had to catch the three o'clock bus to visit her grandmother."),
  ("Iris Cole", "leads the quilting bee and loves fancy stitching with shiny gold thread."),
 ],
 beats=[
  ("Hattie thought back. The square was on the table at four when the tea was poured, and gone when the cups were cleared.", "IT WENT AFTER THE TEA"),
  ("Hattie checked the bus timetable pinned by the door, and remembered waving goodbye.", "HAZEL LEFT AT THREE"),
  ("On the floorboards under the work table, something glinted in the afternoon sun.", "A GOLD THREAD WAS ON THE FLOOR"),
  ("Hattie asked the other quilters about Agnes, and every one of them said the same.", "AGNES NEVER LEFT HER CHAIR"),
  ("Hattie heard loud whistling from above, then the clank of a bucket. She went outside to look up.", "FELIX WAS UP ON THE ROOF"),
  ("In Iris's sewing basket, Hattie saw a sketch of the village map with one new shape drawn in the middle.", "IRIS WANTED TO ADD A STAR"),
 ],
 culprit="Iris Cole",
 solution=("The square went after tea, and Hazel had left at three. Agnes never left her chair, and Felix was up on the roof fixing a gutter. "
           "The gold thread under the table belonged to Iris, and so did the sketch. Iris had slipped the square into her basket to stitch "
           "a little gold star on the map, marking the spot where the first quilting bee met a hundred years ago. She wanted it to be a surprise. "
           "Now everyone knows, and the star is the first thing people look for."),
 words="""QUILT PATCHWORK THIMBLE NEEDLE THREAD BOBBIN SPOOL SCISSORS FABRIC COTTON CALICO GINGHAM VELVET FLANNEL SATIN LINEN STITCH
 SEAM HEM BINDING BATTING HOOP PINCUSHION BUTTON RIBBON LACE TAPE MEASURE PATTERN SQUARE TRIANGLE HEXAGON DIAMOND BORDER APPLIQUE
 EMBROIDERY SEWING BASKET ARMCHAIR TEACUP SAUCER BISCUITS VILLAGE HALL CARETAKER BUCKET LADDER GUTTER ROOF STAR GOLDEN MAP
 BIRTHDAY HUNDRED""",
),
dict(
 title="The Clock That Stopped",
 place="The Town Hall Tower",
 intro=("The town hall clock has kept time for Thimble Hill for a hundred years. Each Sunday it is wound with a big brass key that hangs on a hook "
        "inside the tower. On the morning of the village fete, the clock stopped, and the key was missing from its hook. "
        "Without the clock, nobody knew when the fete would open. The mayor sent for Hattie Bloom."),
 suspects=[
  ("Mayor Otto Briggs", "is round and jolly and wears a tall hat. He is terribly afraid of heights."),
  ("Winnie Shaw", "is the clock keeper, the only person who winds the clock each week."),
  ("Dot Fairley", "leads the church choir and holds practice very early in the morning."),
  ("Sam Ruddle", "is twelve and mad about clocks. He mends old watches at his kitchen table and always has a little oil on his fingers."),
 ],
 beats=[
  ("Hattie looked up at the clock face. Both hands pointed to a quarter past five, just as the sun came up.", "THE CLOCK STOPPED AT DAWN"),
  ("Hattie asked about the clock keeper. The mayor dabbed his forehead and explained.", "WINNIE WAS AWAY ALL WEEK"),
  ("Hattie climbed the narrow stone stairs inside the tower. Halfway up, her hand slid on something slippery.", "OIL ON THE STAIR RAIL"),
  ("At the top of the tower, Hattie looked down at the square far below and thought about the mayor.", "OTTO WILL NOT CLIMB UP"),
  ("From the church across the square, Hattie heard singing, and she remembered the choir practice.", "DOT WAS SINGING AT DAWN"),
  ("On a shelf in the tower, Hattie found an empty tin of brass polish and a soft cloth, both still warm from use.", "THE KEY WAS BEING POLISHED"),
 ],
 culprit="Sam Ruddle",
 solution=("Winnie was away all week. Otto will not climb the tower because he is afraid of heights. Dot was leading choir practice at dawn, "
           "when the clock stopped. The oil on the stair rail and the brass polish pointed to Sam. Sam had borrowed the key to polish it "
           "and oil the clock's gears for its hundredth birthday, as a surprise. He did not know the clock would stop if nobody wound it. "
           "He ran up with the key, wound the clock, and the mayor made him Assistant Clock Keeper on the spot."),
 words="""CLOCK TOWER PENDULUM GEARS COGWHEEL SPRING CHIME BELL HOUR MINUTE SECOND DIAL NUMERALS HANDS WINDING BRASS KEY HOOK STAIRS
 LADDER WEATHERVANE PIGEON MAYOR FETE SQUARE CHURCH CHOIR HYMN SINGING DAWN SUNRISE MORNING POLISH CLOTH OIL CAN WATCH SCREWDRIVER
 TWEEZERS SPANNER TICKING TOCK ALARM SUNDIAL CALENDAR CENTURY BIRTHDAY BUNTING BANNER CAKE STALL PARADE TOWNHALL STEEPLE""",
),
dict(
 title="The Swapped Seeds",
 place="The Seed Swap",
 intro=("Every spring Thimble Hill holds a seed swap in the old barn. The star of the show is a little paper packet of Giant Moon pumpkin seeds, "
        "kept in a tin on the back shelf. Last year a Giant Moon pumpkin from these seeds won the county prize. This year, when Hattie Bloom "
        "opened the tin for the raffle, the packet was full of striped sunflower seeds instead."),
 suspects=[
  ("Gil Barrow", "grows the biggest pumpkins in the county. His boots are always caked in mud from the fields."),
  ("Poppy Vance", "runs the flower shop and adores sunflowers."),
  ("Walt Kemp", "runs the seed swap. He was in charge of the soup pot at lunchtime."),
  ("June Ashby", "keeps a flock of chickens and carries a bag of sunflower seeds for them wherever she goes."),
 ],
 beats=[
  ("Hattie asked when the packet was last checked. Walt said he had looked inside it just before everyone sat down to eat.", "THE SWAP HAPPENED AT LUNCH"),
  ("Hattie asked who was ladling the soup, and the whole queue pointed at the same man.", "WALT WAS SERVING SOUP"),
  ("Hattie poured a few seeds into her palm. They were long and gray, with black stripes.", "THE NEW SEEDS ARE STRIPED"),
  ("Poppy's shop assistant told Hattie that Poppy had not been at the barn at all.", "POPPY STAYED HOME WITH A COLD"),
  ("Hattie looked at the floor of the back room, which had been swept that morning. It was still spotless.", "NO MUD ON THE FLOOR"),
  ("At the bottom of the tin, under the packet, Hattie found something soft and speckled.", "A FEATHER WAS IN THE TIN"),
 ],
 culprit="June Ashby",
 solution=("The seeds were swapped at lunch, and Walt was serving soup. Poppy stayed home with a cold. Gil's muddy boots would have left mud "
           "on the clean floor. The striped sunflower seeds and the speckled feather led to June. It was an accident. While tidying the shelf, "
           "June had filled the wrong packet from her chicken-feed bag and tipped the Giant Moon seeds into the bag. Her hens had not eaten them yet, "
           "and every single pumpkin seed was found. The raffle went ahead, and June's hens got extra corn."),
 words="""SEEDS PUMPKIN SUNFLOWER PACKET TIN BARN HAYLOFT RAFFLE SWAP SPRING PLANTING SOWING SPROUT SEEDLING MARROW SQUASH CARROT
 TURNIP RADISH LETTUCE CABBAGE BEANSTALK PEAPOD TOMATO CUCUMBER ONION GARLIC PARSNIP BEETROOT KALE CHARD CHICKENS HENS ROOSTER
 FEATHER EGGS COOP CORN SOUP LADLE BREAD QUEUE FARMER BOOTS TRACTOR FIELD MEADOW SCARECROW HARVEST BASKET WHEELBARROW TROWEL
 ALLOTMENT GREENHOUSE""",
),
dict(
 title="The Doves on the Cake",
 place="The Copper Kettle Tea Room",
 intro=("Nora and Ben were to be married on Saturday, and their wedding cake was waiting in the Copper Kettle Tea Room under a heavy glass dome. "
        "On top sat two tiny white china doves. On Saturday morning the cake was perfect, but the doves were gone. "
        "Nora was in tears. Hattie Bloom, who was knitting the bride a shawl, put down her needles and took charge."),
 suspects=[
  ("Maisie Fenwick", "owns the tea room and keeps the only front-door key."),
  ("Leo Hart", "is Ben's best man. He was traveling down from the city on Friday night."),
  ("Aunt Prudence", "is Nora's great-aunt. She is very sentimental and always smells of lavender water."),
  ("Kit Morrow", "baked the cake. Her wrist is in a bandage after she slipped on a wet floor."),
 ],
 beats=[
  ("Maisie said the doves were on the cake when she locked up at nine. So they must have gone overnight.", "THE DOVES FLEW OFF AT NIGHT"),
  ("Hattie asked about the best man. Ben showed her the ticket in Leo's coat pocket.", "LEO WAS ON THE LATE TRAIN"),
  ("When Hattie stepped close to the cake, she noticed a sweet, flowery smell in the air.", "THE ROOM SMELLED OF LAVENDER"),
  ("Hattie asked Maisie where she had spent the night. Maisie went pink.", "MAISIE SLEPT AT HER SISTERS"),
  ("Hattie tried to lift the glass dome herself. It took both hands and all her strength.", "THE DOME IS VERY HEAVY"),
  ("In the tea room's guest book, Hattie found an old photograph of a wedding cake from fifty years ago. On top were two little doves.", "THE DOVES WERE ON HER OWN CAKE"),
 ],
 culprit="Aunt Prudence",
 solution=("The doves flew off at night. Leo was on the late train, and Maisie slept at her sister's. Kit could not have lifted the heavy dome "
           "with her bandaged wrist. The lavender smell and the old photograph pointed to Aunt Prudence, who had a spare key from the days "
           "when she ran the tea room herself. The doves had been on her own wedding cake fifty years before. She had taken them home to tie "
           "a tiny blue ribbon around each one, so Nora would have something old and something blue. Nora cried all over again, happily this time."),
 words="""WEDDING CAKE DOVES BRIDE GROOM VEIL BOUQUET RING TIARA CHAPEL CONFETTI ORGANIST USHER BESTMAN TOAST CHAMPAGNE TEAROOM TEAPOT
 SAUCER SCONES CLOTTED CREAM DOILY LACE RIBBON ICING MARZIPAN SPONGE TIERS DOME GLASS TOPPER CHINA PORCELAIN LAVENDER PERFUME
 PHOTOGRAPH ALBUM SHAWL KNITTING NEEDLES GUESTBOOK INVITATION TRAIN TICKET SISTER AUNT GARDEN ROSES PEONIES HONEYMOON DANCE
 WALTZ VIOLIN""",
),
dict(
 title="The Harvest Song",
 place="The Village Hall",
 intro=("For the harvest concert, the choir director wrote a brand new song called Golden Fields. There was only one copy, written by hand, "
        "and it lived on the music stand by the piano. At ten past six on the evening before the concert, the stand was empty. "
        "Without the music, there would be no new song. Hattie Bloom sang alto in the choir, so she started asking questions at once."),
 suspects=[
  ("Wilma Hart", "is the choir's star soprano. She wanted a solo in the new song and did not get one."),
  ("Percy Lowe", "plays the tuba in the village band, which practices in the shed behind the hall."),
  ("Greta Holm", "plays the piano for the choir. She wears thick glasses and always has a pocket full of peppermints."),
  ("Ned Bly", "is the hall cleaner. He sweeps the hall and the front steps every evening."),
 ],
 beats=[
  ("Everyone agreed the music was on the stand when the hall clock struck six, and gone ten minutes later.", "THE MUSIC VANISHED AT SIX"),
  ("From the shed behind the hall came a long, low, wobbly note that went on and on.", "PERCY WAS TUNING HIS TUBA"),
  ("Under the music stand, Hattie found a crinkly little piece of paper. It was a wrapper.", "A PEPPERMINT WRAPPER"),
  ("Hattie asked the people waiting outside if they had seen Ned. They nodded and pointed at his broom.", "NED WAS SWEEPING THE STEPS"),
  ("Hattie telephoned Wilma's house. Her husband said she was not home, and told Hattie why.", "WILMA WAS AT HER SINGING LESSON"),
  ("On the piano lid, Hattie spotted a sheet of fresh music paper with very large, very dark notes.", "GRETA WAS COPYING THE MUSIC"),
 ],
 culprit="Greta Holm",
 solution=("The music vanished at six. Percy was tuning his tuba in the shed, Ned was sweeping the steps in front of everyone, and Wilma was at "
           "her singing lesson. The peppermint wrapper and the big dark notes led to Greta. The director's handwriting was tiny, and Greta "
           "could not read it from the piano stool. She took the song home to copy it out in large notes she could see. She brought both "
           "copies back that night, and Golden Fields was the hit of the concert."),
 words="""HARVEST CONCERT CHOIR SOPRANO ALTO TENOR BASS PIANO TUBA TRUMPET FLUTE CLARINET VIOLIN CELLO DRUM CYMBAL MELODY HARMONY
 CHORUS VERSE RHYTHM TEMPO TREBLE CLEF CRESCENDO ENCORE APPLAUSE CONDUCTOR BATON MUSIC STAND SHEET NOTES SOLO DUET ANTHEM SONG
 GOLDEN FIELDS WHEAT BARLEY SHEAF PUMPKIN APPLES BASKET LANTERN PEPPERMINT WRAPPER BROOM STEPS STAGE CURTAIN SPOTLIGHT TICKET
 REHEARSAL""",
),
dict(
 title="The Lantern Parade Star",
 place="The Craft Barn",
 intro=("On the first dark evening of autumn, the whole of Thimble Hill walks through the lanes carrying paper lanterns. At the front goes a "
        "big paper star lantern on a long pole. This year it was made in the craft barn, and it was left there to dry. At sunset, an hour before "
        "the parade, the star was gone. Hattie Bloom pulled on her coat, clipped on Pickle's lead, and went to find it."),
 suspects=[
  ("Arlo Finch", "is the lamplighter. Every evening he walks the lanes with his long pole, lighting the old gas lamps."),
  ("Bess Tully", "teaches the craft class and made the star herself, covered in glitter."),
  ("Cyril Marsh", "grumbles that the parade is too noisy. He sits on the parish council."),
  ("Pickle", "is Hattie's own scruffy terrier, who loves anything that rustles."),
 ],
 beats=[
  ("Bess said the star was hanging in the barn at four, but by dusk the hook was empty.", "THE STAR WAS GONE BY DUSK"),
  ("Hattie looked out at the lane. One by one, the old lamps were flickering on.", "ARLO WAS LIGHTING THE LAMPS"),
  ("The council clerk told Hattie that the meeting had gone on far too long, as usual.", "CYRIL WAS IN A MEETING"),
  ("Hattie peeked into the classroom next door, where a dozen children were gluing tissue paper.", "BESS WAS TEACHING A CLASS"),
  ("On the barn floor, in the dust, Hattie saw a trail of small, round prints.", "MUDDY PAW PRINTS"),
  ("Hattie followed a long piece of chewed string out of the barn, along the lane and through her own front door.", "THE STRING LED HOME"),
 ],
 culprit="Pickle",
 solution=("The star was gone by dusk. Arlo was lighting the lamps, Cyril was stuck in his meeting and Bess was teaching her class. "
           "The muddy paw prints and the chewed string led all the way to Hattie's own house, where Pickle was asleep in his basket, curled "
           "around the paper star. Its rustling had been too much for him to resist. The star was a little crumpled but not torn, and Bess "
           "patched it with glitter in ten minutes. Pickle walked at the front of the parade, right under the star, looking very pleased with himself."),
 words="""LANTERN PARADE STAR PAPER TISSUE GLITTER GLUE SCISSORS STRING CANDLE GLOW AUTUMN LEAVES ACORN CONKER CHESTNUT BONFIRE
 SCARF MITTENS WOOLLY HAT COAT BOOTS PUDDLE LAMPLIGHTER LAMPPOST DUSK SUNSET TWILIGHT MOONLIGHT OWL HEDGEHOG SQUIRREL TERRIER
 PAWPRINT BASKET BLANKET COUNCIL MEETING CRAFT BARN CLASSROOM CHILDREN CRAYON RIBBON LANE PROCESSION MARCHING DRUM WHISTLE
 COCOA TOFFEE APPLE CIDER""",
),
]
