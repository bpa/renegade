import pygame
import pygame.font
import pygame.display
import re
from pygame.locals import *

import events
from locals import *

def message(text):
    d = Dialog(text)
    screen = pygame.display.get_surface()
    d.run(screen)

class Dialog(object):
    def __init__(self, text):
        self.font = pygame.font.Font(None, 20)
        self.text = text

    def draw(self, screen):
        screen.fill(self.fill_color, self.rect)
        current_y = 10
        for line in self.rendered:
            screen.blit(line, self.rect.move(10,current_y))
            current_y = current_y + self.font.get_linesize()

    def render_one_line(self, line):
        return self.font.render(line, True, self.text_color).convert_alpha()

    def render_text(self):
        self.rendered = map(self.render_one_line, self.lines)
        line_count = len(self.rendered)
        self.rect.height = self.font.get_linesize() * line_count + 20

    def split_text(self):
        self.lines = []
        current = ''
        for chunk in re.split(' ', self.text):
            width, height = self.font.size(current + chunk + ' ')
            if width < self.rect.width - 10:
                current = current + chunk + ' '
            else:
                self.lines.append(current)
                current = chunk + ' '
        if len(current) > 1:
            self.lines.append(current)

    def run(self, screen):

        # Calculate the size of the dialog
        self.rect = pygame.Rect(0,0,0,0)
        self.rect.width = int(screen.get_width() * 0.7)

        # Precalculate some stuff
        self.fill_color = pygame.color.Color('blue')
        self.text_color = pygame.color.Color('white')
        self.split_text()
        self.render_text()
        self.rect.center = screen.get_rect().center

        # Save off a copy of the screen that I'm about to overwrite
        screen_copy = screen.copy()
    
        clock = pygame.time.Clock()
        event_bag = events.EventUtil()
        while True:
            for event in event_bag.process_sdl_events():
                if event.type == QUIT_EVENT:
                    self.dispose()
                    screen.blit(screen_copy, (0,0))
                    return
            
            self.draw(screen)
            pygame.display.flip()
            clock.tick(5)

    def dispose(self):
        self.rendered = None
