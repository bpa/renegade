import sys

try:
    from RPG import *
    import map
    import characters
    import items
    import games.hacknslash.monsters
except ImportError, detail:
    print "Import error:", detail

class hacknslash(RPG):
    def new_game(self,opts):
        hero = characters.Hero()
        self.save_data.hero = hero
        hero.equip_weapon( items.Hands() )
        hero.equip_armor( items.Skin() )
        hero.add_gold(150)
        self.load_map('town.AdventureTown')
        self.save_data.character = characters.Character()
        self.save_data.character.init('stolen-01',2,0,-1)
        self.save_data.map.place_character(self.save_data.character, (9,4) )
