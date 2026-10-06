"""Where each sketch was made (printed on the puzzle page; the subject itself is only revealed in the solutions)."""
PLACES = {
 "Easy": ("by the Hearth|on the Window Seat|in the Reading Nook|at the Tea Table|in the Boot Room|on the Landing|"
          "by the Tall Clock|in the Games Room|at the Front Desk|in the Pantry|in the Kitchen|by the Coat Pegs|"
          "in the Music Room|in the Library|on the Back Stairs|on the Sun Porch|by the Stove|in the Linen Room|"
          "at the Breakfast Bar|in the Map Room|under the Eaves|in the Attic|in the Snug|by the Bay Window|"
          "in the Drying Room|at the Writing Desk|in the Cellar|on the Veranda|in the Ski Room|by the Lantern Hook"),
 "Medium": ("on the Village Green|at the Bakery|by the Duck Pond|at the Post Office|on Market Street|by the Bandstand|"
            "at the Tea Shop|on the Old Bridge|at the Bookshop|by the Well|at the Station Halt|on Lantern Lane|"
            "by the Mill|at the Cheese Shop|by the Toll Gate|at the School House|on Holly Row|at the Wool Shop|"
            "by the Skating Pond|in the Inn Yard|on Orchard Lane|at the Sweet Shop|by the Horse Trough|at the Village Hall|"
            "on the High Street|by the Clock Tower|at the Greengrocer|on Fox Lane|at the Lending Library|by the Allotments|"
            "at the Toy Shop|on Mill Lane|by the Weir|at the Haberdasher|on Bell Lane|at the Cobbler|"
            "by the Water Pump|at the Corner Café|on the Garden Path|at the Village Gate"),
 "Hard": ("in Pine Hollow|by the Frozen Stream|at the Forester's Hut|on the Fox Trail|by the Old Oak|in Owl Wood|"
          "at the Beaver Dam|in Birch Glade|on the Larch Path|by the Mossy Stones|in Badger Dell|at the Footbridge|"
          "in Fern Hollow|by the Woodpile|on Deer Ridge|in the Spruce Grove|at the Bird Hide|by the Icicle Falls|"
          "in Hazel Copse|at the Trail Sign|in Rowan Glade|by the Hollow Log|on the Hare Path|in Juniper Wood|"
          "at the Warden's Cabin|in the Snowy Clearing|in Squirrel Wood|on the Ridge Path|by the Frozen Tarn|in Hemlock Hollow|"
          "at the Picnic Table|by the Old Stile|in Aspen Glade|on the Pine Needle Path|by the Otter Pool|under the Hollow Oak|"
          "at the Shelter Hut|by the Feeding Station|in Cedar Dell|at the Edge of the Wood"),
 "Expert": ("at the Ridge Hut|on the Summit Path|by the Weather Vane|at the Observatory|on the Glacier Edge|by the Mountain Tarn|"
            "at the Cable Car Station|on the Col|by the Waymarker Cairn|at the Ski Lift|on Eagle Crag|by the Snowfield|"
            "at the Refuge|on the Zigzag Path|at the Viewpoint|by the Ice Falls|on the High Meadow|at the Top Station|"
            "on the Ridge Walk|by the Frozen Lake|at the Summit Marker|on Cloud Ledge|by the Snow Fence|at the Mountain Inn|"
            "on Star Point|by the Hut Door|on the Lodge Roof|at the Telescope Dome|on the Last Bend|at the Top of the World"),
}
PLACES = {b: v.split("|") for b, v in PLACES.items()}
