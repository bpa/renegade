import os, pickle
from conf import *
import pygame
import pygame.image
from pygame.locals import *

class game_info_object:
    def __init__(self):
        pass

class game:
    def __init__(self, opts):
        self.opts = opts
        self.name = "Renegade game"
        self.game_info = game_info_object()
        pygame.init()
        self.screen = pygame.display.set_mode((opts['width'], opts['height']))

    def load(self, game):
        self.game_info = pickle.load(open(os.path.join(SAVE_GAMES_DIR,game)))

    def save(self, game):
        pickle.dump(self.game_info,open(os.path.join(SAVE_GAMES_DIR,game),'wb'))

    def run(self):
        pygame.display.set_caption(self.name)
        pygame.mouse.set_visible(0)

        if not pygame.font:
            print 'Unable to initialize font subsystem'
            exit

        clock = pygame.time.Clock()
        while True:
            clock.tick(20)
        
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
                    elif event.key == K_LEFT:
                        self.left_event()
                    elif event.key == K_RIGHT:
                        self.right_event()
                    elif event.key == K_UP:
                        self.up_event()
                    elif event.key == K_DOWN:
                        self.down_event()
            
            self.game_info.map.update()
            self.game_info.map.draw(self.screen)
            pygame.display.flip()

    def up_event(self):
        self.game_info.map.move_character_up()

    def down_event(self):
        self.game_info.map.move_character_down()

    def left_event(self):
        self.game_info.map.move_character_left()

    def right_event(self):
        self.game_info.map.move_character_right()
