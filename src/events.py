import pygame
from pygame.locals import *
from locals import *

class EventUtil:

    def __init__(self):
        self.left = False
        self.right = False
        self.up = False
        self.down = False

    def is_left(self):
        return self.left

    def is_right(self):
        return self.right

    def is_up(self):
        return self.up

    def is_down(self):
        return self.down

    def process_sdl_events(self):
        """A generator to process raw SDL events into logical events,
        using the preferred key/joystick mapping.  Yields
        logical events.
        """

        for event in pygame.event.get():
            if event.type == QUIT:
                yield pygame.event.Event(QUIT_EVENT)
                break
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    yield pygame.event.Event(QUIT_EVENT)
                    break
                elif event.key == K_LEFT:
                    self.left = True
                    self.right = False
                elif event.key == K_RIGHT:
                    self.right = True
                    self.left = False
                elif event.key == K_UP:
                    self.up = True
                    self.down = False
                elif event.key == K_DOWN:
                    self.down = True
                    self.up = False
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    self.left = False
                elif event.key == K_RIGHT:
                    self.right = False
                elif event.key == K_UP:
                    self.up = False
                elif event.key == K_DOWN:
                    self.down = False
