from map import *
from characters import Character

class Overworld(MapBase):
    def __init__(self):
        MapBase.__init__(self,11,11)
        self.set_regen_rate(5)
        self.get_tiles_from_ascii(self.__ascii_art(),{
            'M': 'stone',
            ' ': 'water',
            'x': 'town',
            'i': 'trees',
            '_': 'dirt',
            'O': 'cave',
            'walkable': 'xi_O'})
        
    def __ascii_art(self):
        return(
            "MMMMMMMMMM ",
            "MMMMMMMMOM ",
            "MMMMMii___ ",
            "MMMMMii___ ",
            "MMMMMii_x_ ",
            "           ",
            "iiiiiiiiii ",
            "iiiiiiiiii ",
            "iiiiiiiiii ",
            "iiiiiiiiii ",
            "iiiiiiiiii ")
