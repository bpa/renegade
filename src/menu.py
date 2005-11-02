import dialog, game, core
import pickle

def run_main_menu():
    options = ("Inventory", "Character", "Save Game", "Load Game")
    choice = options[dialog.question("Main Menu", options)]
    if choice == "Inventory":
        dialog.message("Place holder for the inventory page")
    elif choice == "Character":
        dialog.message("Place holder for the character page")
    elif choice == "Save Game":
        core.game.save()
    elif choice == "Load Game":
        core.game.load()
