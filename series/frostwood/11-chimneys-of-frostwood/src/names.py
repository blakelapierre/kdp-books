"""Rooftop names for every puzzle header (one per puzzle, by band)."""
NAMES = {
 "Easy": ("Bakehouse Lane|Chapel Row|Smithy Lane|Well Street|Schoolhouse Row|Candle Lane|Inn Yard Row|Pump Street|Post Office Row|Bell Lane|"
          "Cobbler’s Row|Green End|Weaver’s Lane|Market Row|Toll House Lane|Hollyhock Row|Vicarage Lane|Clock Street|Tailor’s Row|Thimble Lane"),
 "Medium": ("the Lodge East Wing|the Lodge West Wing|the Boot Room Roofs|the Ski Hut Row|the Stable Roofs|Larch Terrace|the Skating Hut Row|Juniper Terrace|the Lantern Roofs|Hare Terrace|"
            "the Woodshed Row|Fern Terrace|the Hay Loft Roofs|Pine Terrace|the Toboggan Huts|Fox Terrace|the Orchard Cottages|Rowan Terrace|the Cocoa Kitchen Roofs|Birch Terrace|"
            "the Bird Table Row|Wren Terrace|the Stile Cottages|Robin Terrace|the Mitten Shop Roofs|Moss Terrace|the Snow Fort Row|Holly Terrace|the Far Wing|the Great Hall Roofs"),
 "Hard": ("the Ticket Office|the Signal Box Row|the Engine Shed|the Waiting Room Roofs|the Water Tower Yard|the Goods Shed|the Parcel Office|the Lamp Room Row|the Coal Stage|the Porter’s Lodge|"
          "the Booking Hall|the Platform Huts|the Turntable Yard|the Station Hotel|the Mail Shed|the Sleeper Stack Row|the Carriage Shed|the Lower Sidings|the Tea Room Roofs|the Stationmaster’s House|"
          "the Footbridge Row|the Points Hut|the Up Platform|the Down Platform|the Brake Van Yard|the Upper Sidings|the Clock Tower Row|the Halt Cottages|the Weighbridge|the Station Gate"),
 "Expert": ("the Shepherd’s Huts|the Summit Bothy|the High Dairy|the Cheese Loft|the Hayrick Row|the Herders’ Cottages|the Chapel Hut|the Goat Sheds|the Spring House|the Ridge Barns|"
            "the Lantern Hut|the Larch Huts|the Upper Farm|the Snowfield Cabins|the Crag Cottages|the Weather Hut|the Pass Inn|the Ice House|the Eyrie Barn|the Hamlet Crown"),
}
NAMES = {b: v.split("|") for b, v in NAMES.items()}
assert [len(v) for v in NAMES.values()] == [20, 30, 30, 20]
assert all(len(set(v)) == len(v) for v in NAMES.values())
assert len({x for v in NAMES.values() for x in v}) == sum(len(v) for v in NAMES.values())
