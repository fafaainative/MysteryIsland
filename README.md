# Mystery Island: The Lost Lighthouse

A beginner-friendly command-line Python adventure game built with the Python standard library.

## Mission

You wake up on Mystery Island after a storm. The lighthouse beacon is dark, and a rescue boat cannot locate the island. Explore the island, collect the rope and lantern, cross the damaged bridge, and restore the beacon.

## Requirements

- Python 3.10 or later
- Git (optional, for version control)

## Project structure

```text
mystery_island_cli/
├── main.py
├── game/
│   ├── __init__.py
│   ├── game.py
│   └── locations.py
├── tests/
│   ├── __init__.py
│   └── test_game.py
├── README.md
└── .gitignore
```

## Run the game

From the project root:

```bash
python main.py
```

On some systems, use `python3 main.py`.

## Run the tests

```bash
python3 -m unittest discover -s tests -v
```

## Rules

- You start at the Beach with 5 energy points.
- Each successful move costs 1 energy point.
- Invalid choices, viewing the map, checking inventory and collecting items cost no energy.
- Collect the rope in the Jungle before crossing the damaged bridge.
- Collect the lantern in the Cave before restoring the lighthouse beacon.
- You win by restoring the beacon at the Lighthouse while you still have energy.
- Reaching zero energy before restoring the beacon causes a loss.
- You can move backwards along available routes.

## Known limitations

- This is a local, single-player command-line game.
- Progress is not saved between playthroughs.
- The route and item locations are fixed.
- The game uses in-memory Python data structures; it does not use a database or JSON save file.

## Learning objectives

This project demonstrates Python modules and packages, dictionaries, lists, functions, loops, conditional logic, input validation, state management and unit testing.
