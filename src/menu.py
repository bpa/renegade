import dialog, game, core
import pickle

def run_main_menu():
    options = ("Inventory", "Save Game", "Load Game","New Game")
    choice = options[dialog.question("Main Menu", options)]
    if choice == "Inventory":
        core.game.show_inventory()
    elif choice == "Save Game":
        core.game.save()
    elif choice == "Load Game":
        core.game.load()
    elif choice == "New Game":
        core.game.start_new_game()
