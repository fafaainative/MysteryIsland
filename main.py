"""Command-line entry point for Mystery Island: The Lost Lighthouse."""

from game.game import (
    create_player,
    display_status,
    play_game,
    show_instructions,
)


def main():
    print("=" * 58)
    print("          MYSTERY ISLAND: THE LOST LIGHTHOUSE")
    print("=" * 58)
    show_instructions()

    while True:
        name = input("\nWhat is your name, explorer? ").strip()
        if name:
            break
        print("Please enter a name so the island knows who you are.")

    player = create_player(name)
    play_game(player)

    while True:
        answer = input("\nWould you like to play again? (yes/no): ").strip().lower()
        if answer in ("yes", "y"):
            player = create_player(name)
            play_game(player)
        elif answer in ("no", "n"):
            print("\nThank you for exploring Mystery Island. Goodbye!")
            break
        else:
            print("Please enter yes or no.")


if __name__ == "__main__":
    main()
