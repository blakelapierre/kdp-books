"""Place names for every puzzle header (one per puzzle, by band): where in Frostwood the icicles hang."""
NAMES = {
 "Easy": ("the Front Porch|the Kitchen Window|the Woodshed Roof|the Back Door|the Pantry Eave|the Boot Room|the Bay Window|the Garden Gate|the Bird Table|the Well Cover|"
          "the Tea Room Sill|the Rain Barrel|the Lantern Hook|the Wash House|the Side Porch|the Coal Hatch|the Dormer Window|the Attic Gable|the Hen House|the Potting Shed|"
          "the Cellar Steps|the Dairy Eave|the Log Store|the Glasshouse|the Pump House|the Bench Arbour|the Larder Window|the Front Gable|the Mud Room|the Mail Box|"
          "the Bell Pull|the Weather Vane|the Pergola|the Garden Arch|the Apple Loft|the Gutter Spout|the Brew House|the Bird Box|the Sundial Roof|the Chimney Stack"),
 "Medium": ("Baker’s Row|Bell Lane|Chapel Street|Cobble Square|Market Lane|Mill Lane|School Lane|Church Walk|Wool Lane|the Inn Yard|"
            "the Village Green|Pudding Lane|Clock Tower Square|Hazel Lane|Laundry Lane|Orchard Row|Smithy Lane|Ivy Court|Duck Pond Lane|Lantern Lane|"
            "Toll House Lane|Thimble Row|Candle Street|Rosehip Lane|Wheelwright’s Yard|Kettle Lane|Elder Close|Tea Room Corner|Bramble Lane|Holly Row|"
            "Post Office Lane|the Library Steps|Draper’s Lane|the Cheese Market|Well Close|Fiddler’s Row|Saddler’s Yard|Weaver’s Walk|Lamplighter’s Lane|Bridge Street"),
 "Hard": ("the Booking Hall|Platform One|Platform Two|the Goods Shed|the Signal Box|the Water Tower|the Coal Stage|the Turntable|the Footbridge|the Waiting Room|"
          "the Lamp Room|the Parcels Office|the Station Clock|the Engine Shed|the Weighbridge|the Porters’ Hut|the Tea Kiosk|the Level Crossing|the Station Canopy|the Ticket Window|"
          "the Siding|the Loading Dock|the Station Garden|the Milk Platform|the Guard’s Van|the Buffer Stop|the Snow Plough Shed|the Station Bench|the Cattle Dock|the Gate Lodge|"
          "the Telegraph Hut|the Ash Pit|the Carriage Shed|the Water Crane|the Station Yard|the Signal Gantry|the Goods Office|the Old Halt|the Tunnel Mouth|the Viaduct"),
 "Expert": ("the High Barn|the Shepherd’s Hut|the Cold Spring|the Fell Gate|the Sheepfold|the Ridge Cabin|the Hay Loft|the Upper Falls|the Peat Store|the Lookout|"
            "the Bothy|the Stone Barn|the Frozen Tarn|the Drovers’ Rest|the Ice Cave|the Heather Hut|the Summit Cairn|the Pine Shelter|the Hermit’s Rock|the Moss Ledge|"
            "the North Crag|the Snow Gully|the Larch Hut|the Ghyll Bridge|the Owl Barn|the Crow Rock|the Upper Meadow|the Fox Hollow|the Glen Hut|the Moon Ledge|"
            "the Mill Race|the Beacon Hill|the Wind Gap|the Far Fold|the Silver Falls|the Ram’s Rock|the Ice Bridge|the Long Ridge|the Hidden Spring|the Star Ledge"),
}
NAMES = {k: v.split("|") for k, v in NAMES.items()}
for k, v in NAMES.items(): assert len(v) == 40 and len(set(v)) == 40, k
