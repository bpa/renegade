import pygame
import pygame.font
import pygame.display
import pygame.draw
import re
from pygame.locals import *

import events
import core
from locals import *

def message(text):
    d = Dialog(text)
    screen = pygame.display.get_surface()
    d.run(screen)
    core.game.save_data.map.clear_key_state()

def question(text, options):
    d = Dialog(text, options[:])
    screen = pygame.display.get_surface()
    ret = d.run(screen)
    core.game.save_data.map.clear_key_state()
    return ret

class Dialog(object):

    def __init__(self, text, options=None):
        self.font = pygame.font.Font(None, 20)
        self.text = text
        self.options = options
        if options is not None:
            self.selection = 0
        else:
            self.selection = None

    def draw(self, screen):
        screen.fill(self.fill_color, self.rect)
        current_y = 10
        for line in self.rendered:
            screen.blit(line, self.rect.move(10,current_y))
            current_y = current_y + self.font.get_linesize()
        current_y = current_y + self.font.get_linesize()
        first_option_y = current_y
        for option in self.rendered_opts:
            screen.blit(option, self.rect.move(20,current_y))
            current_y = current_y + self.font.get_linesize()
        if self.selection is not None:
            y_pos = first_option_y + self.selection * self.font.get_linesize()
            y_pos = y_pos + self.font.get_linesize() / 2 # Center it in line
            rect = self.rect.move(10, y_pos)
            center = (rect.left, rect.top)
            pygame.draw.circle(screen, self.text_color, center, 5)

    def render_one_line(self, line):
        return self.font.render(line, True, self.text_color).convert_alpha()

    def render_text(self):
        self.rendered = map(self.render_one_line, self.lines)
        if self.options is not None:
            self.rendered_opts = map(self.render_one_line, self.options)
            line_count = len(self.rendered) + len(self.rendered_opts) + 1
        else:
            self.rendered_opts = []
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

    def selection_up(self):
        if self.selection is not None and self.selection > 0:
            self.selection = self.selection - 1

    def selection_down(self):
        if self.selection is not None and self.selection < len(self.options)-1:
            self.selection = self.selection + 1

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
        #screen_copy = screen.copy()
        #copy doesn't appear to exist on FreeBSD or Windows
        screen_copy = pygame.Surface(screen.get_size())
        screen_copy.blit(screen,(0,0))
    
        clock = pygame.time.Clock()
        event_bag = events.EventUtil()
        while True:
            for event in event_bag.process_sdl_events():
                if event.type == QUIT_EVENT and self.selection is None:
                    self.dispose()
                    screen.blit(screen_copy, (0,0))
                    return None
                elif event.type == PUSH_ARROW_EVENT or \
                     event.type == REPEAT_ARROW_EVENT:
                    if event_bag.is_up():
                        self.selection_up()
                    elif event_bag.is_down():
                        self.selection_down()
                elif event.type == PUSH_ACTION_EVENT:
                    self.dispose()
                    screen.blit(screen_copy, (0,0))
                    if self.selection is not None:
                        #return self.options[self.selection]
                        return self.selection
                    else: return None
            
            self.draw(screen)
            pygame.display.flip()
            clock.tick(20)

    def dispose(self):
        self.rendered = None
