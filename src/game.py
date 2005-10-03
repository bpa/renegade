import os, pickle
from conf import *
import core, events
from pygame import mouse, font, time
from locals import *
import hud

# Global reference to the currently loaded save data
#save_data = None

class SaveGameObject:
    def __init__(self):
        pass

class Game:
    def __init__(self):
        self.name = "Renegade game"
        self.save_data = SaveGameObject()
        self.screen = core.wm.window(z=10)
        self.new_game()
        self.hud = hud.HUD(self.save_data.hero)

    def new_game(self):
        pass

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
        mouse.set_visible(0)

        if not font:
            print 'Unable to initialize font subsystem'
            exit

        print "Running map..."
        self.save_data.map.init()
        clock = time.Clock()
        event_bag = events.EventUtil()
        self.event_bag = event_bag
        iteration = 1
        self.running = True
        while self.running:
            for event in event_bag.process_sdl_events():
                if event.type == QUIT_EVENT:
                  core.game.running = False
                  self.save_data.map.dispose()
                  return
                else:
                  self.save_data.map.handle_event(event)
            self.save_data.map.update()
            core.wm.update()
            core.wm.draw()
            clock.tick(20)

    def clear_key_state(self):
        self.event_bag.clear()

    def teleport(self, loc, map_name=None, dir=None):
        """Teleports the character to a new location.  If a map is specified,
           the current map will be changed, if not, the character will just be
           moved to the location on the current map"""
        if dir is None:
            dir = self.save_data.map.character.facing
        if map_name is not None:
            dude = self.save_data.map.character
            self.save_data.map.dispose()
            self.load_map(map_name)
            self.save_data.map.init()
        self.save_data.map.place_character(dude, loc, False, dir )
        self.save_data.map.update()
