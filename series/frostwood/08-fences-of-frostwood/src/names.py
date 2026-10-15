"""Lot names for every puzzle header (one per puzzle, by band)."""
NAMES = {
 "Easy": ("the Baker’s Yard|Chapel Close|the Smithy Plot|Well Lane|the Schoolhouse Garden|Candle Row|the Inn Paddock|Pump Corner|the Post Office Yard|Bell Lane|"
          "the Cobbler’s Plot|Green End|the Weaver’s Garden|Market Corner|the Toll House|Hollyhock Row|the Vicarage Lawn|Clock Lane|the Tailor’s Patch|Thimble Corner"),
 "Medium": ("the Long Meadow|Lodge Paddock|the Sledge Run Field|Snowdrop Lea|the Pony Paddock|Larch Field|the Skating Meadow|Juniper Lea|the Lantern Field|Hare Meadow|"
            "the Woodpile Plot|Fern Lea|the Hay Barn Field|Pine Paddock|the Toboggan Slope|Fox Meadow|the Lodge Orchard Gate|Rowan Lea|the Cocoa Lawn|Birch Field|"
            "the Bird Table Meadow|Wren Paddock|the Stile Field|Robin Lea|the Bonfire Field|Moss Meadow|the Snow Fort Field|Holly Paddock|the Far Meadow|the Lodge Field"),
 "Hard": ("the Timber Yard|the Saw Pit|the Log Stack|the Wheelwright’s Plot|the Mill Pond Bank|the Grain Store|the Sack Loft Yard|the Millstone Plot|the Cart Shed|the Plank Rack|"
          "the Sluice Yard|the Bark Heap|the Kiln Plot|the Cooper’s Yard|the Weir Bank|the Drying Shed|the Flour Store|the Lower Yard|the Ox Pen|the Cartwright’s Plot|"
          "the Hopper Yard|the Shingle Stack|the Mill Lane Plot|the Barrow Shed|the Tannery Bank|the Upper Yard|the Hoist Yard|the Stable Plot|the Miller’s Garden|the Mill Gate"),
 "Expert": ("the Apple Rows|the Pear Walk|the Quince Lot|the Plum Terrace|the Cider Press Plot|the Russet Rows|the Beehive Lot|the Crab-Apple Corner|the Damson Walk|the Pippin Terrace|"
            "the Medlar Lot|the Bramley Rows|the Cherry Walk|the Ladder Shed Lot|the Top Terrace|the Graft Lot|the Codlin Rows|the Frost Pocket|the Old Pear Lot|the Orchard Crown"),
}
NAMES = {b: v.split("|") for b, v in NAMES.items()}
assert [len(v) for v in NAMES.values()] == [20, 30, 30, 20]
assert all(len(set(v)) == len(v) for v in NAMES.values())
assert len({x for v in NAMES.values() for x in v}) == sum(len(v) for v in NAMES.values())
