from RPG import *
import map, characters
from maps.stone_wall import stone_wall

class fog_test(RPG):
    def __init__(self,opts):
        RPG.__init__(self,opts)
        self.save_data.map = stone_wall()
        self.save_data.character = characters.Character(
            ('dude1', 'dude2', 'dude3', 'dude4') )
        self.save_data.map.place_character( self.save_data.character, (4,4) )
