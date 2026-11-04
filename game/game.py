"""Core rules and command-line interactions for Mystery Island."""

from game.locations import ITEMS, LOCATIONS, MAP_TEXT

STARTING_ENERGY = 5
MAX_ENERGY = 5


def create_player(name):
    """Create a fresh player state for a new game."""
    return {
        "name": name,
        "location": "Beach",
        "energy": STARTING_ENERGY,
        "inventory": [],
        "collected_items": [],
        "game_over": False,
        "won": False,
        "decisions": [],
    }


def display_status(player):
    """Display the player's current status."""
    inventory = ", ".join(player["inventory"]) if player["inventory"] else "Empty"
    print("\n" + "-" * 58)
    print(f"Player: {player['name']}")
    print(f"Location: {player['location']}")
    print(f"Energy: {player['energy']}/{MAX_ENERGY}")
    print(f"Inventory: {inventory}")
    print("-" * 58)


def show_instructions():
    """Explain the objective and the main game rules."""
    print(
        "\nMISSION\n"
        "A storm has left you stranded on Mystery Island. Restore the "
        "lighthouse beacon so a rescue boat can find you.\n\n"
        "RULES\n"
        "1. Explore five connected locations: Beach, Jungle, Cave, Old Bridge and Lighthouse.\n"
        "2. You begin with 5 energy points.\n"
        "3. Every successful move costs 1 energy point.\n"
        "4. Invalid choices and blocked actions do not cost energy.\n"
        "5. Collect the rope in the Jungle and the lantern in the Cave.\n"
        "6. The rope is required to cross the damaged bridge.\n"
        "7. The lantern is required to restore the lighthouse beacon.\n"
        "8. You can check your inventory and view the map without spending energy.\n"
        "9. If your energy reaches 0 before the beacon is restored, you lose.\n"
    )


def available_exits(player):
    """Return exits that are currently accessible from the player's location."""
    location = player["location"]
    exits = LOCATIONS[location]["exits"]

    if location == "Cave" and "rope" not in player["inventory"]:
        return ["Jungle"]
    if location == "Old Bridge" and "rope" not in player["inventory"]:
        return ["Cave"]
    return list(exits)


def move_player(player, destination):
    """Move the player if the route is valid and energy is available.

    Returns (success, message). A failed move does not change player state.
    """
    if player["game_over"]:
        return False, "The game has ended. Start a new game to explore again."

    if destination not in LOCATIONS:
        return False, "That location does not exist."

    if destination not in available_exits(player):
        if destination == "Old Bridge" and "rope" not in player["inventory"]:
            return False, "The bridge is unsafe. Find the rope in the Jungle first."
        if destination == "Lighthouse" and "rope" not in player["inventory"]:
            return False, "You cannot cross the damaged bridge without the rope."
        return False, "You cannot travel there directly from this location."

    if player["energy"] <= 0:
        player["energy"] = 0
        player["game_over"] = True
        player["won"] = False
        return False, "You have no energy left. Your journey ends here."

    player["location"] = destination
    player["energy"] -= 1
    player["decisions"].append(f"Moved to {destination}")

    if player["energy"] == 0:
        player["game_over"] = True
        player["won"] = False
        return True, (
            f"You reached {destination}, but you have used your last energy point. "
            "You collapse before completing the mission."
        )

    return True, f"You moved to {destination}. One energy point was used."


def collect_item(player, item_name):
    """Collect an item available at the current location, once only."""
    item_name = item_name.strip().lower()

    if player["game_over"]:
        return False, "The game has ended. You cannot collect anything now."

    if item_name not in ITEMS:
        return False, "That item is not part of this adventure."

    if ITEMS[item_name]["location"] != player["location"]:
        return False, f"You cannot collect the {item_name} here."

    if item_name in player["collected_items"]:
        return False, f"You have already collected the {item_name}."

    player["inventory"].append(item_name)
    player["collected_items"].append(item_name)
    player["decisions"].append(f"Collected {item_name}")
    return True, f"You collected the {item_name}. It has been added to your inventory."


def restore_beacon(player):
    """Attempt to restore the lighthouse beacon and determine the win outcome."""
    if player["game_over"]:
        return False, "The game has already ended."

    if player["location"] != "Lighthouse":
        return False, "You must be at the Lighthouse to restore the beacon."

    if "lantern" not in player["inventory"]:
        return False, "The mechanism is too dark to operate. You need the lantern."

    if player["energy"] <= 0:
        player["energy"] = 0
        player["game_over"] = True
        player["won"] = False
        return False, "You have no energy left to restore the beacon."

    player["decisions"].append("Restored lighthouse beacon")
    player["game_over"] = True
    player["won"] = True
    return True, (
        "The lantern illuminates the mechanism. You restore the lighthouse beacon!\n"
        "A rescue boat spots the light and heads towards the island.\n"
        "YOU WIN! You have been rescued from Mystery Island."
    )


def describe_location(player):
    """Print the description of the current location and available items."""
    location = player["location"]
    print(f"\nCURRENT LOCATION: {location.upper()}")
    print(LOCATIONS[location]["description"])

    available_items = [
        item for item, details in ITEMS.items()
        if details["location"] == location and item not in player["collected_items"]
    ]
    if available_items:
        print("You can see: " + ", ".join(available_items) + ".")


def show_inventory(player):
    """Display the items the player has collected."""
    if player["inventory"]:
        print("Inventory: " + ", ".join(player["inventory"]))
    else:
        print("Your inventory is empty.")


def show_map():
    """Display the island's location map."""
    print(MAP_TEXT)


def process_choice(player, choice):
    """Process a menu choice and return a message.

    This function is intentionally small enough to test without input().
    """
    choice = choice.strip().lower()

    if choice == "1":
        exits = available_exits(player)
        if not exits:
            return "There are no available routes from here."
        print("\nAvailable destinations:")
        for index, destination in enumerate(exits, start=1):
            print(f"{index}. {destination}")
        destination_choice = input("Where would you like to go? ").strip()
        if not destination_choice.isdigit():
            return "Please enter the number shown beside a destination."
        index = int(destination_choice) - 1
        if index < 0 or index >= len(exits):
            return "That destination number is not available."
        success, message = move_player(player, exits[index])
        return message

    if choice == "2":
        show_inventory(player)
        return ""

    if choice == "3":
        show_map()
        return ""

    if choice == "4":
        player["game_over"] = True
        player["won"] = False
        return "You chose to leave the island. Game over."

    if choice == "5":
        local_items = [
            item for item, details in ITEMS.items()
            if details["location"] == player["location"]
            and item not in player["collected_items"]
        ]
        if not local_items:
            return "There is nothing new to collect here."
        print("\nItems available to collect:")
        for index, item in enumerate(local_items, start=1):
            print(f"{index}. {item.title()} — {ITEMS[item]['description']}")
        item_choice = input("Which item would you like to collect? ").strip()
        if not item_choice.isdigit():
            return "Please enter the number shown beside an item."
        index = int(item_choice) - 1
        if index < 0 or index >= len(local_items):
            return "That item number is not available."
        success, message = collect_item(player, local_items[index])
        return message

    if choice == "6":
        success, message = restore_beacon(player)
        return message

    return "Invalid menu choice. Please choose a number from 1 to 6."


def play_game(player):
    """Run the main game loop for one playthrough."""
    while not player["game_over"]:
        display_status(player)
        describe_location(player)
        print(
            "\nMAIN MENU\n"
            "1. Explore / Move\n"
            "2. Check inventory\n"
            "3. View island map\n"
            "4. Quit game\n"
            "5. Collect an item\n"
            "6. Restore lighthouse beacon"
        )
        choice = input("Enter your choice: ")
        message = process_choice(player, choice)
        if message:
            print("\n" + message)

        if player["energy"] <= 0 and not player["game_over"]:
            player["energy"] = 0
            player["game_over"] = True
            player["won"] = False

    if player["won"]:
        print("\n" + "=" * 58)
        print("MISSION COMPLETE")
        print("=" * 58)
    else:
        print("\n" + "=" * 58)
        print("MISSION FAILED")
        print("=" * 58)
        print("The lighthouse beacon was not restored.")
