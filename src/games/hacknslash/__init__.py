import sys

try:
    from RPG import *
    import map
    import characters
    import items
except ImportError, detail:
    print "Import error:", detail

class hacknslash(RPG):
    def new_game(self,opts):
        self.save_data.hero = characters.Hero()
        self.save_data.hero.equip_weapon( items.Hands() )
        self.save_data.hero.equip_armor( items.Skin() )
        self.load_map('town.AdventureTown')
        self.save_data.character = characters.Character()
        self.save_data.character.init('stolen-01',2,0,-1)
        self.save_data.map.place_character(self.save_data.character, (9,4) )
