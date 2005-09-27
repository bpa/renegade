import sys

try:
    import map
    import characters
    import items
    import games.hacknslash.monsters
    from game import Game
except ImportError, detail:
    print "Import error:", detail

class hacknslash(Game):
    def new_game(self,opts):
        hero = characters.Hero()
        self.save_data.hero = hero
        hero.equip_weapon( items.Hands() )
        hero.equip_armor( items.Skin() )
        hero.add_gold(150)
        self.load_map('town.AdventureTown')
        self.save_data.character = map.MapEntity()
        self.save_data.character.init('stolen-01',2,0,-1)
        self.save_data.map.place_character(self.save_data.character, (9,4) )
