from map import *
from characters import Character
import core

class Overworld(MapBase):
    def __init__(self):
        MapBase.__init__(self,20,15)
        self.set_regen_rate(5)
        self.get_tiles_from_ascii(self.__ascii_art(),{
            'M': ('stone',),
            ' ': ('water',),
            'x': ('town',),
            'i': ('trees',),
            '_': ('dirt',),
            'O': ('cave',),
            'walkable': 'xi_O'})
        self.add_entry_listener(10,5, self.enter_town)
        self.add_entry_listener(9,1, self.enter_cave)
        
    def __ascii_art(self):
        return(
            "MMMMMMMMMMMM   iiiii",
            "MMMMMMMMMOMM   iiiii",
            "MMMiiii_____   iiiii",
            "MMMiiii_____   iiiii",
            "MMMiiii_____   iiiii",
            "MMMiiii___x_   iiiii",
            "MMMiiii_____   iiiii",
            "               iiiii",
            "               iiiii",
            "iiiiiiiiiiii   iiiii",
            "iiiiiiiiiiii   iiiii",
            "iiiiiiiiiiii        ",
            "iiiiiiiiiiii        ",
            "iiiiiiiiiiii   iiiii",
            "iiiiiiiiiiii   iiiii")

    def enter_town(self):
        if self.character.facing == SOUTH:
            self.character.face(WEST)
        if self.character.facing == WEST:
            core.game.teleport((19,10), 'town.AdventureTown')
        else:
            core.game.teleport(( 0,10), 'town.AdventureTown')

    def enter_cave(self):
        core.game.teleport((5,9), 'cave.Cave')

