import core
import pygame
from pygame import time
from pygame.locals import *
from conf import *
from locals import *

class EventUtil:

    def __init__(self):
        self.clock = core.clock
        self.keys_pressed = pygame.key.get_pressed()

    def is_left(self):
        return self.keys_pressed[K_LEFT]

    def is_right(self):
        return self.keys_pressed[K_RIGHT]

    def is_up(self):
        return self.keys_pressed[K_UP]

    def is_down(self):
        return self.keys_pressed[K_DOWN]

    def process_sdl_events(self):
        """A generator to process raw SDL events into logical events,
        using the preferred key/joystick mapping.  Yields
        logical events.
        """

        for event in pygame.event.get():
            self.keys_pressed = pygame.key.get_pressed()
            if event.type == QUIT:
                yield pygame.event.Event(QUIT_EVENT)
                break
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    yield pygame.event.Event(QUIT_EVENT)
                    break
                elif event.key == K_LEFT  or \
                     event.key == K_RIGHT or \
                     event.key == K_UP    or \
                     event.key == K_DOWN:
                  yield pygame.event.Event(PUSH_ARROW_EVENT)
                elif event.key == K_LCTRL  or \
                     event.key == K_RETURN or \
                     event.key == K_SPACE  or \
                     event.key == K_KP_ENTER:
                   yield pygame.event.Event(PUSH_ACTION_EVENT)
                elif event.key == K_LSHIFT or \
                     event.key == K_RSHIFT or \
                     event.key == K_m:
                   yield pygame.event.Event(PUSH_ACTION2_EVENT)
