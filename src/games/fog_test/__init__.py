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
    def __init__(self,opts):
        RPG.__init__(self,opts)
        monsters.register_packs()
        self.init_character()
        self.save_data.map = StoneWall()
        self.save_data.character = characters.Character('dude_map')
        self.save_data.map.place_character(self.save_data.character, (4,4) )
        self.save_data.map.place_hero(self.save_data.hero)

    def init_character(self):
        hero = characters.Hero( pygame.display.get_surface() )
        self.save_data.hero = hero
        hero.equip_weapon( items.Dagger() )
        hero.equip_armor( items.ToughShirt() )
