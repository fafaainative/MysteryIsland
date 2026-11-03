def new_game(name):
    return {
    "name": name,
    "location": "Beach",
    "energy": 5,
    "inventory": [],
    "game_over": False,
    "won": False
}


get_available_actions(location):
    if location == "Beach":
        return ["look", "quit"]
    
    return []




