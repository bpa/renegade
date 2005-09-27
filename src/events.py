import core
from core import *
from conf import *
from locals import *

class EventUtil:

    def __init__(self):
        self.clear()
        self.clock = core.time.Clock()

    def clear(self):
        self.left = -1 
        self.right = -1
        self.up = -1
        self.down = -1
        self.action = -1
        self.action2 = -1

    def is_left(self):
        return self.left>=0

    def is_right(self):
        return self.right>=0

    def is_up(self):
        return self.up>=0

    def is_down(self):
        return self.down>=0

    def is_action(self):
        """Basically pop action events so we don't get stuck in a loop"""
        if self.action >= 0:
            self.action = -1
            return 1
        return 0

    def is_action2(self):
        return self.action2>=0

    def process_sdl_events(self):
        """A generator to process raw SDL events into logical events,
        using the preferred key/joystick mapping.  Yields
        logical events.
        """

        for event in core.event.get():
            if event.type == QUIT:
                yield core.event.Event(QUIT_EVENT)
                break
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    yield core.event.Event(QUIT_EVENT)
                    break
                elif event.key == K_LEFT:
                    self.left = 0
                    self.right = -1
                    yield core.event.Event(PUSH_ARROW_EVENT)
                elif event.key == K_RIGHT:
                    self.right = 0
                    self.left = -1
                    yield core.event.Event(PUSH_ARROW_EVENT)
                elif event.key == K_UP:
                    self.up = 0
                    self.down = -1
                    yield core.event.Event(PUSH_ARROW_EVENT)
                elif event.key == K_DOWN:
                    self.down = 0
                    self.up = -1
                    yield core.event.Event(PUSH_ARROW_EVENT)
                elif event.key == K_LCTRL or \
                     event.key == K_RETURN or \
                     event.key == K_SPACE or \
                     event.key == K_KP_ENTER:
                    self.action = 0
                    yield core.event.Event(PUSH_ACTION_EVENT)
                elif event.key == K_LSHIFT or \
                     event.key == K_RSHIFT or \
                     event.key == K_m:
                    self.action2 = 0
                    yield core.event.Event(PUSH_ACTION2_EVENT)

            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    self.left = -1
                elif event.key == K_RIGHT:
                    self.right = -1
                elif event.key == K_UP:
                    self.up = -1
                elif event.key == K_DOWN:
                    self.down = -1
                elif event.key == K_LCTRL or \
                     event.key == K_RETURN or \
                     event.key == K_SPACE or \
                     event.key == K_KP_ENTER:
                    self.action = -1
                elif event.key == K_LSHIFT or \
                     event.key == K_RSHIFT or \
                     event.key == K_c:
                    self.action2 = -1

        elapsed = self.clock.tick()
        if self.is_left():
            self.left = self.left + elapsed
            if self.left > REPEAT_DELAY:
                self.left = 0
                yield core.event.Event(REPEAT_ARROW_EVENT)
        elif self.is_right():
            self.right = self.right + elapsed
            if self.right > REPEAT_DELAY:
                self.right = 0
                yield core.event.Event(REPEAT_ARROW_EVENT)
        if self.is_up():
            self.up = self.up + elapsed
            if self.up > REPEAT_DELAY:
                self.up = 0
                yield core.event.Event(REPEAT_ARROW_EVENT)
        elif self.is_down():
            self.down = self.down + elapsed
            if self.down > REPEAT_DELAY:
                self.down = 0
                yield core.event.Event(REPEAT_ARROW_EVENT)
        if self.is_action():
            self.action = self.action + elapsed
            if self.action > REPEAT_DELAY:
                self.action = 0
                yield core.event.Event(REPEAT_ACTION_EVENT)
        if self.is_action2():
            self.action2 = self.action2 + elapsed
            if self.action2 > REPEAT_DELAY:
                self.action2 = 0
                yield core.event.Event(REPEAT_ACTION2_EVENT)
            
