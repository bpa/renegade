from game import *

class RPG(game):
    def __init__(self,opts):
        game.__init__(self,opts)

    def teleport(self, new_map, new_x, new_y, effect):
        self.game_info.map = new_map
        self.game_info.player.x = new_x
        self.game_info.player.y = new_y
        if effect != None:
            #Need to implement teleport effects
            pass
        self.update()
        self.game_info.map.draw(self.screen)
        if effect != None:
            #Need to implement teleport effects
            pass
