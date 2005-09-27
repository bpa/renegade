import os, pickle
from conf import *
import core

# Global reference to the currently loaded save data
save_data = None

class SaveGameObject:
    def __init__(self):
        pass

class Game:
    def __init__(self, opts):
        self.opts = opts
        self.name = "Renegade game"
        self.save_data = SaveGameObject()
        self.new_game(opts)

    def load_map(self,map_name):
        """Loads a map by name.  This should always have a module.
             game.load_map('module.map') => None
             Sets game.save_data.map to specified map
             Assumes there are no submodules"""
        (map_module, map_class) = map_name.split('.')
        map_module = self.__module__ + ".maps." + map_module
        module = __import__(map_module, '', '', map_class)
        exec "self.save_data.map = module.%s()" % map_class

    def load(self, game):
        self.save_data = pickle.load(open(os.path.join(SAVE_GAMES_DIR,game)))

    def save(self, game):
        pickle.dump(self.save_data,open(os.path.join(SAVE_GAMES_DIR,game),'wb'))

    def run(self):
        global save_data
        save_data = self.save_data
        core.display.set_caption(self.name)
        core.mouse.set_visible(0)

        if not core.font:
            print 'Unable to initialize font subsystem'
            exit

        print "Running map..."
        self.running = True
        while self.running:
            ret = self.save_data.map.run()
            print "Map completed with return value: ", ret

    def teleport(self, effect, loc, dir=None, map_name=None):
        """Teleports the character to a new location using an optional
           effect.  If a map is specified, the current map will be changed,
           if not, the character will just be moved to the location on the
           current map"""
        if dir is None:
            dir = self.save_data.map.character.facing
        if effect is not None:
            pass
        if map_name is not None:
            dude = self.save_data.map.character
            self.save_data.map.running = False
            self.load_map(map_name)
        self.save_data.map.place_character(dude, loc, False, dir )
        self.save_data.map.update()
        self.save_data.map.draw()
        if effect is not None:
            pass
