from game import *

class RPG(game):
    def __init__(self,opts):
        game.__init__(self,opts)

    def teleport(self, new_map, new_x, new_y, effect):
        self.save_data.map = new_map
        self.save_data.player.x = new_x
        self.save_data.player.y = new_y
        if effect != None:
            #Need to implement teleport effects
            pass
        self.update()
        self.save_data.map.draw(self.screen)
        if effect != None:
            #Need to implement teleport effects
            pass
