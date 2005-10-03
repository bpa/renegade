import sys

try:
    from RPG import *
    import map
    import characters
    import items
    from maps.stone_wall import StoneWall
    import monsters
except ImportError, detail:
    print "Import error:", detail

class fog_test(RPG):
    def __init__(self):
        monsters.register_packs()

    def new_game(self):
        self.init_character()
        self.save_data.map = StoneWall()
        #self.save_data.character = characters.Character('dude_map')
        self.save_data.character = characters.Character('stolen-01',2,0,-1)
        self.save_data.map.place_character(self.save_data.character, (4,4) )

    def init_character(self):
        hero = characters.Hero()
        self.save_data.hero = hero
        hero.equip_weapon( items.Dagger() )
        hero.equip_armor( items.ToughShirt() )
        hero.add_gold( 500 )
