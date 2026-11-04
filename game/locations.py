"""Location definitions and connections for Mystery Island."""

LOCATIONS = {
    "Beach": {
        "description": (
            "You wake on a quiet beach after a violent storm. "
            "The lighthouse is dark, and the rescue boat cannot find the island."
        ),
        "exits": ["Jungle"],
    },
    "Jungle": {
        "description": (
            "Tall trees surround a narrow trail. You notice a strong rope "
            "lying beside an old supply crate."
        ),
        "exits": ["Beach", "Cave"],
    },
    "Cave": {
        "description": (
            "The cave is damp and almost completely dark. An old lantern "
            "rests beside a dry patch of rock."
        ),
        "exits": ["Jungle", "Old Bridge"],
    },
    "Old Bridge": {
        "description": (
            "A damaged bridge crosses a deep ravine. Its far end leads "
            "towards the lighthouse."
        ),
        "exits": ["Cave", "Lighthouse"],
    },
    "Lighthouse": {
        "description": (
            "You reach the lighthouse. Its beacon mechanism is silent. "
            "A rescue boat will only come when the beacon is restored."
        ),
        "exits": ["Old Bridge"],
    },
}

ITEMS = {
    "rope": {
        "location": "Jungle",
        "description": "A sturdy rope that can help secure the damaged bridge.",
    },
    "lantern": {
        "location": "Cave",
        "description": "A working lantern that can illuminate the lighthouse mechanism.",
    },
}

MAP_TEXT = """
                 [LIGHTHOUSE]
                       |
                 [OLD BRIDGE]
                       |
                    [CAVE]
                       |
                   [JUNGLE]
                       |
                    [BEACH]
"""
