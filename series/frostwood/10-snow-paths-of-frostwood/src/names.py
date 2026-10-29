"""Place names for every puzzle header (one per puzzle, by band)."""
NAMES = {
 "Easy": ("the Kitchen Door|the Woodshed|the Herb Beds|the Sundial|the Rose Arch|the Bird Table|the Glasshouse|the Garden Gate|the Old Well|the Bee Skeps|"
          "the Rhubarb Patch|the Old Pump|the Tool Shed|the Wall Bench|the Pear Tree|the Cold Frames|the Potting Shed|the Lavender Walk|the Croquet Lawn|the Box Hedge|"
          "the Bird Bath|the Apple Store|the Log Pile|the Kitchen Garden|the Back Steps|the Lantern Hook|the Holly Bush|the Snowdrop Bed|the Tea Lawn|the Summerhouse|"
          "the Yew Walk|the Hen House|the Washing Line|the Boot Scraper|the Compost Bins|the Stone Trough|the Gooseberry Row|the Orchard Gate|the Side Porch|the Front Steps"),
 "Medium": ("Baker’s Row|Bell Lane|Chapel Street|Cobble Square|Market Lane|Mill Lane|School Lane|Church Walk|Wool Lane|the Inn Yard|"
            "the Village Green|Pudding Lane|Clock Tower Square|Hazel Lane|Laundry Lane|Orchard Row|Smithy Lane|Ivy Court|Duck Pond Lane|Lantern Lane|"
            "Toll House Lane|Thimble Row|Candle Street|Rosehip Lane|Wheelwright’s Yard|Kettle Lane|Elder Close|Tea Room Corner|Bramble Lane|Holly Row|"
            "Post Office Lane|the Library Steps|Draper’s Lane|the Cheese Market|Well Close|Fiddler’s Row|Saddler’s Yard|Weaver’s Walk|Lamplighter’s Lane|Bridge Street"),
 "Hard": ("the Booking Hall|Platform One|Platform Two|the Goods Shed|the Signal Box|the Water Tower|the Coal Stage|the Turntable|the Lamp Room|the Parcels Office|"
          "the Footbridge Steps|the Engine Shed|the Ticket Window|the Waiting Room|the Station Clock|the Milk Dock|the Weighbridge|the Level Crossing|the Long Siding|the Buffer Stops|"
          "the Porters’ Room|the Luggage Barrows|the Station Garden|the Mail Cart|the Crane Yard|the Timber Siding|the Down Platform|the Up Platform|the Coal Yard|the Sand House|"
          "the Points Lever|the Lamp Huts|the Carriage Shed|the Bucket Rack|the Station House|the Signal Gantry|the Tea Kiosk|the Bicycle Shed|the Yard Gate|the Last Lamp"),
 "Expert": ("the Shepherd’s Hut|the High Pasture|Cloudberry Meadow|the Cairn|the Summit Hut|the Saddle|Ptarmigan Ridge|the Long Meadow|Juniper Slope|the Old Sheepfold|"
            "the Upper Barn|Crag End|the Hayloft|Lark Meadow|the Tarn|the Ski Hut|the Weather Station|Edelweiss Bank|the Mountain Spring|the Larch Wood|"
            "Cowbell Meadow|the Lookout|Moonrise Col|the Stone Stile|the Milking Hut|the Far Meadow|Snowfield Corner|the Marmot Rocks|Gentian Slope|the Hay Barn|"
            "Raven Rock|the Wind Gap|the Bothy|Star Meadow|the Waymarker|the Pine Shoulder|the Last Gate|Frost Hollow|Shepherd’s Spring|the Top Meadow"),
}
NAMES = {b: v.split("|") for b, v in NAMES.items()}
assert all(len(v) == 40 and len(set(v)) == len(v) for v in NAMES.values()), {b: len(v) for b, v in NAMES.items()}
assert len({x for v in NAMES.values() for x in v}) == sum(len(v) for v in NAMES.values())
