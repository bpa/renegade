from RPG import *
import map, characters

class fog_adventure(RPG):
    def __init__(self,opts):
        RPG.__init__(self,opts)
        self.game_info.map = map.MapBase(20, 20)
        self.game_info.map.set_location( (0,0), 'stone', False )
        self.game_info.map.set_location( (1,1), 'stone', False )
        self.game_info.map.set_location( (2,2), 'stone', False )
        self.game_info.map.set_location( (3,2), 'stone', False )
        self.game_info.map.set_location( (4,2), 'stone', False )
        self.game_info.map.set_location( (5,2), 'stone', False )
        self.game_info.map.set_location( (6,1), 'stone', False )
        self.game_info.map.set_location( (7,0), 'stone', False )
        self.character = characters.Character( ('dude1', 'dude2', 'dude3', 'dude4') )
        self.game_info.map.place_character( self.character, (4,4) )
