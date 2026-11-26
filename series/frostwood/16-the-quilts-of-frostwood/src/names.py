"""Quilt names for every puzzle header (one per puzzle, by band)."""
NAMES = {
 "Easy": ("Bakehouse Square|Chapel Star|Smithy Blocks|Well Lane Nine-Patch|Schoolroom Squares|Candle Lane Strip|Inn Yard Log Cabin|Pump Street Patch|Post Office Squares|Bell Lane Bricks|"
          "Cobbler’s Patch|Green End Blocks|Weaver’s Lattice|Market Day Squares|Toll House Strips|Hollyhock Patch|Vicarage Blocks|Clock Street Squares|Tailor’s Offcuts|Thimble Lane Patch"),
 "Medium": ("the Blue Room Quilt|the Garden Room Quilt|the Tower Room Quilt|the Pine Room Quilt|the Lantern Room Quilt|the Larch Room Quilt|the Attic Bunk Quilt|the Juniper Room Quilt|the Fox Room Quilt|the Hare Room Quilt|"
            "the Woodshed Rug|the Fern Room Quilt|the Hay Loft Throw|the Rowan Room Quilt|the Window Seat Throw|the Birch Room Quilt|the Owl Room Quilt|the Wren Room Quilt|the Cocoa Corner Throw|the Holly Room Quilt|"
            "the Robin Room Quilt|the Library Throw|the Moss Room Quilt|the Boot Room Rug|the Snowdrop Room Quilt|the Far Wing Quilt|the Hearth Rug|the Sitting Room Throw|the Great Hall Banner|the Lodge Keeper’s Quilt"),
 "Hard": ("Sleeper Berth One|Sleeper Berth Two|Sleeper Berth Three|the Guard’s Van Blanket|the Dining Car Cloth|the Observation Car Throw|the Waiting Room Bench Pad|the Stationmaster’s Quilt|the Signal Box Rug|the Porter’s Blanket|"
          "Sleeper Berth Four|Sleeper Berth Five|the Booking Hall Banner|the Tea Room Cloth|the Parcel Office Rug|Sleeper Berth Six|the Lamp Room Throw|the Mail Van Blanket|Sleeper Berth Seven|the Footbridge Banner|"
          "Sleeper Berth Eight|the Water Tower Hut Rug|the Station Hotel Quilt|Sleeper Berth Nine|the Engine Shed Blanket|the Halt Cottage Quilt|Sleeper Berth Ten|the Night Mail Throw|Sleeper Berth Eleven|the Last Train Quilt"),
 "Expert": ("the Shepherd’s Hut Quilt|the Summit Bothy Quilt|the High Dairy Quilt|the Cheese Loft Throw|the Herders’ Quilt|the Chapel Hut Quilt|the Spring House Throw|the Ridge Barn Blanket|the Lantern Hut Quilt|the Larch Hut Quilt|"
            "the Upper Farm Quilt|the Snowfield Cabin Quilt|the Crag Cottage Quilt|the Weather Hut Throw|the Pass Inn Quilt|the Ice House Blanket|the Eyrie Barn Quilt|the Hamlet Crown Quilt|the Starwatch Quilt|the Heirloom Quilt"),
}
NAMES = {b: v.split("|") for b, v in NAMES.items()}
assert [len(v) for v in NAMES.values()] == [20, 30, 30, 20]
assert all(len(set(v)) == len(v) for v in NAMES.values())
assert len({x for v in NAMES.values() for x in v}) == sum(len(v) for v in NAMES.values())
