import dialog, game

def run_main_menu():
    options = ("Inventory", "Character")
    choice = options[dialog.question("Main Menu", options)]
    if choice == "Inventory":
        dialog.message("Place holder for the inventory page")
    elif choice == "Character":
        dialog.message("Place holder for the character page")
