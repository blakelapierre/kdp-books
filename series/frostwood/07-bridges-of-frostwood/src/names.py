"""Place names for every puzzle header (one per puzzle, by band)."""
NAMES = {
 "Easy": ("the Boathouse|Lily Steps|the Duck House|Reed Corner|the Skating Bench|Willow Point|the Lantern Jetty|Cocoa Landing|the Little Island|Heron Rock|"
          "the Stepping Stones|Snowdrop Bank|the Frozen Fountain|the Sluice Gate|Pebble Shore|the Ice House|Kingfisher Bend|the Lodge Steps|the Mooring Post|Mallard Cove|"
          "the Bird Hide|Fern Bank|the Old Pump|the Tea Lawn Edge|Birch Spit|the Swan Shelter|Moorhen Reach|the Garden Gate|Holly Island|the Bell Post|"
          "Juniper Bank|the Wishing Well|Larch Landing|the Pond Steps|Coot Corner|Rowan Isle|the Path’s End|Candle Cove|the Summerhouse|the Far Bank"),
 "Medium": ("the Mill Race|Baker’s Brook|the Chapel Stream|Cobble Ford|Market Brook|the Old Weir|Bell Brook|Wool Lane Brook|the Water Meadow|the Inn Yard Stream|"
            "the Green Brook|Church Lane Ford|the Mill Leat|Pudding Lane Brook|the Clock Tower Stream|Hazel Brook|the Laundry Steps|Orchard Brook|the Smithy Ford|Ivy Brook|"
            "the Duck Pond Brook|School Lane Stream|the Watercress Beds|Lantern Lane Brook|the Toll Bridge Stream|Thimble Brook|the Bakery Ford|Candle Brook|the Village Green Stream|Rosehip Brook|"
            "the Wheelwright’s Ford|Kettle Brook|the Sheep Wash|Elder Brook|the Tea Room Stream|Bramble Ford|the Little Weir|Holly Brook|the Station Stream|the Lower Mill"),
 "Hard": ("the Reed Beds|Bittern Pool|the Long Boardwalk|Sedge Flats|Rush Pool|the Willow Carr|Otter Pool|the Plank Path|Snipe Flats|Cotton-Grass Moss|"
          "the Peat Banks|Heron Pool|the Alder Carr|Bulrush Bend|Teal Pool|the Marsh Gate|Mist Pool|the Lantern Boardwalk|Frost Flats|Wigeon Pool|"
          "the Sedge Maze|Moss Bank|Reedmace Pool|the Old Causeway|Water-Rail Flats|the Withy Beds|Sweet-Gale Moss|Coot Pool|the Middle Fen|Sallow Carr|"
          "the Dyke Bridge|Pintail Pool|the Ice Flats|Marigold Bank|the Boardwalk Bend|Gadwall Pool|the Far Fen|Cranberry Moss|the Sluice Bridge|Shoveler Pool|"
          "Rime Flats|the Hide Steps|Bog-Bean Pool|the Willow Bridge|Grebe Pool|the Lower Fen|Starling Reeds|the Upper Fen|Lapwing Flats|Marsh End"),
 "Expert": ("the Pine Isles|Heron Skerries|the Lantern Islands|Twin Holms|the Snow Holms|Kettle Island|the Bell Skerries|Birch Holm|the Swan Islands|the Star Skerries|"
            "Larch Holm|the Moon Islands|Holly Skerries|Rowan Holm|the Wren Islands|Juniper Skerries|the Candle Holms|Lodge Island|the Frost Skerries|Osprey Holm|"
            "the Seven Sisters|the Loon Islands|the North Skerries|Cloudberry Holm|the Teacup Islands|the Ice Skerries|the Long Holm|Sledge Island|the Merganser Isles|Goldeneye Skerries|"
            "the Hearth Islands|Pinecone Holm|the Starlight Skerries|Tern Island|the Boathouse Holms|the Bunting Isles|the Middle Skerries|Mitten Island|the Chain of Isles|Owl Holm|"
            "the East Skerries|the Fir Islands|the Ptarmigan Holms|Lantern Rock|the West Isles|Crowberry Holm|the Outer Skerries|Aurora Island|the Last Isles|the Lodge Point Holms"),
}
NAMES = {b: v.split("|") for b, v in NAMES.items()}
assert all(len(set(v)) == len(v) for v in NAMES.values())
assert len({x for v in NAMES.values() for x in v}) == sum(len(v) for v in NAMES.values())
