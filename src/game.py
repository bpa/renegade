import os, pickle, sys, shelve
from conf import *
import core, events
from pygame import font, time
from locals import *
import hud, dialog, items
import map
import traceback

# Global reference to the currently loaded save data
#save_data = None

class SaveGameObject:
    def __init__(self):
        pass

class Game:
    def __init__(self):
        self.basedir = os.path.dirname(sys.modules[self.__module__].__file__)
        self.open_save_game()
        items.init(self.basedir)
        self.name = "Renegade game"
        self.save_data = SaveGameObject()
        self.save_data.map = None
        try:
          self.load()
        except:
          traceback.print_exc()
          self.new_game()
          self.save()
        self.hud = hud.HUD(self.save_data.hero)
        self.fps = dialog.FpsDialog()
        core.display.set_caption(self.name)
        self.impending_actions = []

    def open_save_game(self):
        try:
          os.mkdir(SAVE_GAMES_DIR)
        except:
          pass
        self.save_game = shelve.open(os.path.join(self.basedir,"save"),'c',2)
      
    def new_game(self):
        pass

    def load_map(self,map_name):
        """Loads a map by name.  This should always have a module.
             game.load_map('module.map') => None
             Sets game.save_data.map to specified map
             Assumes there are no submodules"""
        map = "map-%s" % map_name
        if self.save_game.has_key(map):
          self.save_data.map = self.save_game[map]
        else:
          (map_module, map_class) = map_name.split('.')
          map_module = self.__module__ + ".maps." + map_module
          module = __import__(map_module, '', '', map_class)
          exec "self.save_data.map = module.%s()" % map_class
          self.save_data.map.init()
        self.save_data.map.show()
        self.save_data.map.focus()

    def load(self):
        data = self.save_data
        save = self.save_game
        if data.map != None:
          data.map.dispose()
        map_name = save['current_map']
        data.hero = save['hero']
        data.map = save['map-%s' % map_name]
        data.character = save['character']
        if self.__dict__.has_key('hud'):
          self.hud.set_hero(data.hero)
        data.map.init()
        data.map.show()
        data.map.focus()
        data.map.place_character(data.character, data.character.pos)

    def save(self):
        data = self.save_data
        save = self.save_game
        map_name = data.map.__class__.__name__
        save['hero'] = data.hero
        save['character'] = data.character
        save['current_map'] = map_name
        save['map-%s' % map_name] = data.map

    def handle_event(self, event):
        self.save_data.map.handle_event(event)

    def run(self, handle_event=None):
        if handle_event == None:
          handle_event = self.handle_event
        event_bag    = core.event_bag
        wm_update    = core.wm.update
        wm_draw      = core.wm.draw
        flip_display = core.display.flip
        clock_tick   = clock = core.clock.tick
        impending = self.impending_actions
        running = True
        while running:
          if len(impending) > 0:
            action = impending.pop(0)
            action()
          for event in event_bag.process_sdl_events():
              if event.type == QUIT_EVENT:
                running = False
              else:
                if handle_event(event): running = False
          wm_update()
          wm_draw()
          flip_display()
          clock_tick(25)

    def teleport(self, loc, map_name=None, dir=None):
        self.impending_actions.append(lambda: self.__teleport(loc,map_name,dir))
        self.save_data.map.blur()

    def __teleport(self, loc, map_name, dir):
        """Teleports the character to a new location.  If a map is specified,
           the current map will be changed, if not, the character will just be
           moved to the location on the current map"""
        dude = self.save_data.map.character
        if dir is None:
            dir = dude.facing
        if map_name is not None:
          self.save_data.map.dispose()
          self.load_map(map_name)
        self.save_data.map.place_character(dude, loc, False, dir)
        self.save_data.map.focus()
