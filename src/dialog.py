import pygame
import pygame.font
from pygame.locals import *

import events
from locals import *

class Dialog(object):
    def __init__(self, text):
        self.font = pygame.font.Font(None, 20)
        self.text = text

    def draw(self, screen):
        screen.fill(self.fill_color, self.rect)
        screen.blit(self.rendered, self.rect.move(10,10))

    def render_text(self):
        t = self.font.render(self.text, True, self.text_color)
        self.rendered = t.convert_alpha()

    def run(self, screen):

        # Calculate the size of the dialog
        self.rect = pygame.Rect(0,0,0,0)
        self.rect.width = int(screen.get_width() * 0.7)
        self.rect.height = int(screen.get_height() * 0.7)
        self.rect.center = screen.get_rect().center

        # Precalculate some stuff
        self.fill_color = pygame.color.Color('blue')
        self.text_color = pygame.color.Color('white')
        self.render_text()
    
        clock = pygame.time.Clock()
        event_bag = events.EventUtil()
        while True:
            clock.tick(20)
        
            for event in event_bag.process_sdl_events():
                if event.type == QUIT_EVENT:
                    return
            
            self.draw(screen)
            pygame.display.flip()
        

    def dispose(self):
        self.rendered = None
