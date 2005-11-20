import re
import events
import core
import pygame
from pygame import image, Rect, draw
from pygame.locals import RLEACCEL
import dialog
from locals import *
from window_manager import Window, StaticWindow
import gc

img = image.load("../data/edges-16x4.tga")
colorkey = img.get_at((0,0))
img.set_colorkey(colorkey, RLEACCEL)
dialog.circle_border_image = img

def message(text):
    d = Dialog(text)
    d.run()

def question(text, options):
    d = Dialog(text, options[:])
    ret = d.run()
    return ret

def draw_round_border(surface, width=4, color=None, bounds=None):
    """draw_round_border(Surface, line_width, Color, Rect) => None
       only Surface is required"""
    h = surface.get_height()
    w = surface.get_width()
    img = dialog.circle_border_image
    if color == None: color = pygame.color.Color("white")
    if bounds == None: bounds = surface.get_rect()

    r = Rect(0,0,8,8)
    border = bounds.inflate(-8,-8)
    border.topleft = bounds.topleft

    surface.blit(img, border.topleft, r)
    r.top = 8
    surface.blit(img, border.bottomleft, r)
    r.left = 8
    surface.blit(img, border.bottomright, r)
    r.top = 0
    surface.blit(img, border.topright, r)
    
    i = bounds.inflate(-17,-17)
    o = bounds.inflate(-3,-3)
    o.topleft = bounds.topleft
    draw.line(surface, color, (i.left,o.top),(i.right,o.top),       4 )
    draw.line(surface, color, (o.left,i.top),(o.left,i.bottom),     4 )
    draw.line(surface, color, (i.left,o.bottom),(i.right,o.bottom), 4 )
    draw.line(surface, color, (o.right,i.top),(o.right,i.bottom),   4 )

class Dialog:

    def __init__(self, text, options=None):
        self.options = options
        if options is not None:
            self.selection = 0
        else:
            self.selection = None

        self.fg = pygame.color.Color('white')
        self.bg = pygame.color.Color('blue')
        self.tr = pygame.color.Color('black')

        half = core.screen.get_width() * 4 / 5
        self.rect = Rect(0,0,half,0)
        self.text = text
        self.font = pygame.font.Font(None, 20)
        self.split_text()
        self.render_text()

        self.window = core.wm.window(half,self.rect.height,'center','center')
        self.window.update = self.update
        self.window.handle_event = self.handle_event
        self.screen = self.window.image
        self.screen.set_colorkey(self.tr, RLEACCEL)

        self.rect = Rect(self.window.rect)
        self.rect.center = self.screen.get_rect().center

        r = self.rect.inflate(-6,-6)
        self.bgwin = core.wm.window(r.width,r.height,'center','center',z=3)
        self.bgwin.image.fill(self.bg)
        self.bgwin.image.set_alpha(128)

        self.borderwin = core.wm.window(self.rect.width,self.rect.height, \
            'center','center', z=2)
        self.borderwin.image.fill(self.tr)
        dialog.draw_round_border(self.borderwin.image,color=self.fg)
        self.borderwin.image.set_colorkey(self.tr, RLEACCEL)

    def hide(self):
        self.window.hide()
        self.bgwin.hide()
        self.borderwin.hide()

    def nop(self): pass
    def update(self):
        self.window.update = self.nop
        self.screen.fill(self.tr)
        draw_round_border(self.screen,color=self.fg)
        current_y = 10
        for line in self.rendered:
            self.screen.blit(line, self.rect.move(10,current_y))
            current_y = current_y + self.font.get_linesize()
        current_y = current_y + self.font.get_linesize()
        first_option_y = current_y
        for option in self.rendered_opts:
            self.screen.blit(option, self.rect.move(20,current_y))
            current_y = current_y + self.font.get_linesize()
        if self.selection is not None:
            y_pos = first_option_y + self.selection * self.font.get_linesize()
            y_pos = y_pos + self.font.get_linesize() / 2 # Center it in line
            rect = self.rect.move(10, y_pos)
            center = (rect.left, rect.top)
            draw.circle(self.screen, self.fg, center, 5)

    def render_one_line(self, line):
        return self.font.render(line, True, self.fg).convert_alpha()

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
        if self.selection is not None:
            if self.selection == 0:
              self.selection = len(self.options)-1
            else:
              self.selection = self.selection - 1
        self.window.update = self.update

    def selection_down(self):
        if self.selection is not None:
            if self.selection < len(self.options)-1:
                self.selection = self.selection + 1
            else:
              self.selection = 0
        self.window.update = self.update

    def run(self):
        self.window.show()
        self.window.focus()
        core.wm.run()
        core.wm.running = True
        self.dispose()
        core.game.save_data.map.focus()
        if self.selection is not None:
            return self.selection
        else: return None

    def handle_event(self, event):
        if event.type == PUSH_ARROW_EVENT or \
             event.type == REPEAT_ARROW_EVENT:
            if core.event_bag.is_up():
                self.selection_up()
            elif core.event_bag.is_down():
                self.selection_down()
        elif event.type == PUSH_ACTION_EVENT:
            core.wm.running = False

    def dispose(self):
        self.rendered = None
        self.window.destroy()
        self.bgwin.destroy()
        self.borderwin.destroy()
        self.window.update = None

class FpsDialog(Window):
    def __init__(self, width=170, height=40, x=5, y=5):
        rect = Rect(x,y,width,height)
        Window.__init__(self, rect, 0)
        self.x = x
        self.y = y
        self.render = pygame.font.Font(None, 16).render
        self.fg = pygame.color.Color('yellow')
        self.bg = pygame.color.Color('black')
        self.tr = pygame.color.Color('red')

        self.bgwin = core.wm.window(width,height,x,y,z=1,name="FPS background")
        self.bgwin.image.fill(self.bg)
        self.bgwin.image.set_alpha(128)

    def draw(self, b):
        x = self.x + 5
        y = self.y
        c = core.clock
        f = self.render
        b(f("FPS: %.1f" % c.get_fps(),True,self.fg), (x,y))
        b(f("Render Time: %ims" % c.get_rawtime(),True,self.fg), (x,y+10))
        b(f("Time between frames: %ims" % c.get_time(),True,self.fg), (x,y+20))
