from RPG import *
import map, characters
from maps.stone_wall import StoneWall

class fog_test(RPG):
    def __init__(self,opts):
        RPG.__init__(self,opts)
        self.save_data.map = StoneWall()
        self.save_data.character = characters.Character('dude_map')
        self.save_data.map.place_character(self.save_data.character, (4,4) )
