import sys

try:
    from RPG import *
    import map
    import characters
    import items
    from maps.town import AdventureTown
    from maps.overworld import Overworld
    from maps.cave import Cave
    import monsters
except ImportError, detail:
    print "Import error:", detail

class hacknslash(RPG):
    def __init__(self,opts):
        RPG.__init__(self,opts)
        self.init_character()
        self.save_data.map = AdventureTown()
        self.save_data.character = characters.Character('stolen-01',2,0,-1)
        self.save_data.map.place_character(self.save_data.character, (9,4) )
        self.save_data.map.place_hero(self.save_data.hero)

    def init_character(self):
        hero = characters.Hero( pygame.display.get_surface() )
        self.save_data.hero = hero
        hero.equip_weapon( items.weapon('Bare Hands') )
        hero.equip_armor( items.armor('Nothing') )
