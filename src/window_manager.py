import core
import types
import pygame
from pygame.sprite import Sprite, RenderPlain
try:
    from pygame.sprite import AbstractGroup
except:
    from pygame.sprite import Group as AbstractGroup
from pygame.locals import HWSURFACE
from pygame import color, Surface, Rect, font

class Window(Sprite):
  """Base class for windows.  Just assign a new function (or lambda) to update and have it draw the image."""
  def __init__(self, rect, z):
    Sprite.__init__(self)
    self.rect = rect
    self.z = z
    core.wm.add(self)
  
  def show(self):
    core.wm.show(self)

  def hide(self):
    core.wm.hide(self)

  def destroy(self):
    self.kill()
    core.wm.current_screen.sort_by_z()

  def update(self):
    pass

  def draw(self, surface_blit):
    pass

  def set_event_mask(self, mask):
    pass

  def handle_event(self, event):
    pass

class StaticWindow(Window):
    def __init__(self, rect, z, flags):
        Window.__init__(self,rect,z)
        self.image = Surface((rect.width,rect.height),flags)

    def draw(self, surface_blit):
        surface_blit(self.image, self.rect)

class WindowGroup(AbstractGroup):
  def __init__(self):
    AbstractGroup.__init__(self)
    self.zorder = []

  def sort_by_z(self):
    zorder = []
    for s in self.spritedict.keys():
      zorder.append(s)
    zorder.sort(self.reverse_z_sort_sprites)
    self.zorder = zorder

  def reverse_z_sort_sprites(self, a, b):
  	return cmp(b.z, a.z)

  def draw(self):
    surface_blit = core.screen.blit
    for s in self.zorder: s.draw(surface_blit)
    core.display.flip()
    core.clock.tick(20)

  def add(self,sprite):
    AbstractGroup.add(self,sprite)
    self.sort_by_z()

  def remove(self,sprite):
    AbstractGroup.remove(self,sprite)
    self.sort_by_z()

class Minimal:
  def __init__(self):
    self.screens = {}
    self.set_screen('main')
    black = color.Color('Black')
    core.screen.fill(black)
    core.display.flip()
    core.wm = self

  def set_screen(self, screen):
    if self.screens.has_key(screen):
      self.current_screen = self.screens[screen]
    else:
      self.current_screen = WindowGroup()
      self.screens[screen] = self.current_screen
    cs = self.current_screen
    self.add  = cs.add
    self.show = cs.add
    self.hide = cs.remove
    self.draw = cs.draw
    self.update = cs.update

  def translate(self, full_size, win_size, position=None):
    if position == None and win_size.endswith('%'):
      return full_size * int(win_size[:-1]) / 100
    if position == 'center':
      return full_size / 2 - win_size / 2
    raise SyntaxError('Unknown positional parameter %s' % position)

  def window(self,width=None,height=None,x=0,y=0,z=0,flags=HWSURFACE):
    """Create a new window with size and position in pixels"""
    rect = Rect(0,0,0,0)
    if type(width) == type(rect):
      rect = width
    else:
      if width  == None: width  = core.screen.get_width()
      if height == None: height = core.screen.get_height()
      if type(width) == types.StringType:
        width = self.translate(core.screen.get_width(),width)
      if type(height) == types.StringType:
        height = self.translate(core.screen.get_height(),height)
      if width  < 1: width  = core.screen.get_width()  + width
      if height < 1: height = core.screen.get_height() + height
      if type(x) == types.StringType:
        x = self.translate(core.screen.get_width(),width,x)
      if type(y) == types.StringType:
        y = self.translate(core.screen.get_height(),height,y)
      if x < 0: x = core.screen.get_width()  + x
      if y < 0: y = core.screen.get_height() + y
      rect = Rect(x,y,width,height)
    win = StaticWindow(rect,z,flags)
    return win
