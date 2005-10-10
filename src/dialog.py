import re
import events
import core
import pygame
from pygame import image, Rect, draw
from pygame.locals import RLEACCEL
import dialog
from math import pi
from locals import *

img = image.load("../data/edges-16x4.tga")
colorkey = img.get_at((0,0))
img.set_colorkey(colorkey, RLEACCEL)
dialog.circle_border_image = img
dialog.running = False

def message(text):
    d = Dialog(text)
    d.run()

def question(text, options):
    d = Dialog(text, options[:])
    ret = d.run()
    return ret

def draw_round_border(surface, width=4, color=None):
    h = surface.get_height()
    w = surface.get_width()
    img = dialog.circle_border_image
    if color == None: color = pygame.color.Color("white")

    r = Rect(0,0,8,8)
    surface.blit(img, (0,0), r)
    r.top = 8
    surface.blit(img, (0,h-8), r)
    r.left = 8
    surface.blit(img, (w-8,h-8), r)
    r.top = 0
    surface.blit(img, (w-8,0), r)
    
    x1 = y1 = 2 * width
    x2 = w - x1 - 1
    y2 = h - y1 - 1
    bottom = h - width + 1
    right  = w - width + 1
    draw.line(surface, color, (x1,0),(x2,0),4 )
    draw.line(surface, color, (0,y1),(0,y2),4 )
    draw.line(surface, color, (x1,bottom),(x2,bottom),4 )
    draw.line(surface, color, (right,y1),(right,y2),4 )

class Dialog(object):

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

    def __del__(self):
        self.window.destroy()
        self.bgwin.destroy()
        self.borderwin.destroy()

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
        dialog.running = True
        clock = core.clock
        event_bag = core.game.event_bag
        while True:
            for event in event_bag.process_sdl_events():
                if event.type == QUIT_EVENT and self.selection is None:
                    self.dispose()
                    return None
                elif event.type == PUSH_ARROW_EVENT or \
                     event.type == REPEAT_ARROW_EVENT:
                    if event_bag.is_up():
                        self.selection_up()
                    elif event_bag.is_down():
                        self.selection_down()
                elif event.type == PUSH_ACTION_EVENT:
                    self.dispose()
                    if self.selection is not None:
                        #return self.options[self.selection]
                        return self.selection
                    else: return None
            
            core.game.save_data.map.update()
            core.wm.update()
            core.wm.draw()

    def dispose(self):
        dialog.running = False
        self.rendered = None
        self.window.destroy()
        self.bgwin.destroy()
        self.borderwin.destroy()
