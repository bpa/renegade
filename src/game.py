import os, pickle
from conf import *
import pygame
import pygame.image
from pygame.locals import *

class SaveGameObject:
    def __init__(self):
        pass

class Game:
    def __init__(self, opts):
        self.opts = opts
        self.name = "Renegade game"
        self.save_data = SaveGameObject()
        pygame.init()
        dimensions = (opts['width'], opts['height'])
        flags = 0
        if opts['fullscreen']: flags = flags | FULLSCREEN
        self.screen = pygame.display.set_mode(dimensions, flags)

    def load(self, game):
        self.save_data = pickle.load(open(os.path.join(SAVE_GAMES_DIR,game)))

    def save(self, game):
        pickle.dump(self.save_data,open(os.path.join(SAVE_GAMES_DIR,game),'wb'))

    def run(self):
        pygame.display.set_caption(self.name)
        pygame.mouse.set_visible(0)

        if not pygame.font:
            print 'Unable to initialize font subsystem'
            exit

        print "Running map..."
        ret = self.save_data.map.run(self.screen)
        print "Map completed with return value: ", ret

