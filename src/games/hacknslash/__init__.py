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
        self.save_data.hero.equip_weapon( items.weapon('Bare Hands') )
        self.save_data.hero.equip_armor( items.armor('Nothing') )
        self.load_map('town.AdventureTown')
        self.save_data.character = characters.Character('stolen-01',2,0,-1)
        self.save_data.map.place_character(self.save_data.character, (9,4) )
