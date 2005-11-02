import core
import types
import pygame
import events
from locals import QUIT_EVENT
from pygame.sprite import Sprite, RenderPlain
try:
    from pygame.sprite import AbstractGroup
except:
    from pygame.sprite import Group as AbstractGroup
from pygame.locals import HWSURFACE
from pygame import color, Surface, Rect, font

class Window(Sprite):
  """Base class for windows.  Just assign a new function (or lambda) to update and have it draw the image."""
  def __init__(self, rect, z=0, name=None):
    Sprite.__init__(self)
    self.rect = rect
    self.z = z
    core.wm.add(self)
    if name == None:
      self.name = self.__class__.__name__
    else:
      self.name = "%s: %s" % (self.__class__.__name__, name)
  
  def __repr__(self):
    return "<%s(in %d groups)>" % (self.name, len(self._Sprite__g))

  def show(self):
    core.wm.show(self)

  def hide(self):
    core.wm.hide(self)

  def destroy(self):
    self.blur()
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

  def focus(self): core.wm.focus(self)
  def focus_events(self):
    self.is_left  = core.event_bag.is_left
    self.is_right = core.event_bag.is_right
    self.is_up    = core.event_bag.is_up
    self.is_down  = core.event_bag.is_down

  def blur(self): core.wm.blur(self)
  def blur_events(self):
    self.is_left  = lambda: False
    self.is_right = lambda: False
    self.is_up    = lambda: False
    self.is_down  = lambda: False

  def is_left(self):  return False
  def is_right(self): return False
  def is_up(self):    return False
  def is_down(self):  return False

class StaticWindow(Window):
    def __init__(self, rect, z=0, flags=HWSURFACE, name=None):
        Window.__init__(self,rect,z,name)
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

  def add(self,sprite):
    AbstractGroup.add(self,sprite)
    self.sort_by_z()

  def remove(self,sprite):
    AbstractGroup.remove(self,sprite)
    self.sort_by_z()

class Minimal:
  def __init__(self):
    self.active_window = None
    self.current_screen = None
    self.screens = {}
    self.set_screen('main')
    black = color.Color('Black')
    core.screen.fill(black)
    core.display.flip()
    core.wm = self
    core.event_bag = events.EventUtil()

  def focus(self, win):
    if self.active_window != None:
      self.active_window.blur_events()
    win.focus_events()
    self.active_window = win
    
  def blur(self, win):
    if self.active_window == None:
        self.active_window = None
    else:
       if self.active_window == win:
        self.active_window.blur_events()
        self.active_window = None
    
  def set_screen(self, screen):
    if self.current_screen != None:
      self.current_screen.zorder = []
    if self.screens.has_key(screen):
      self.current_screen = self.screens[screen]
    else:
      self.current_screen = WindowGroup()
      self.screens[screen] = self.current_screen
    cs = self.current_screen
    cs.sort_by_z()
    self.add  = cs.add
    self.show = cs.add
    self.hide = cs.remove
    self.draw = cs.draw
    self.update = cs.update
    self.blur(None)

  def translate(self, full_size, win_size, position=None):
    if position == None and win_size.endswith('%'):
      return full_size * int(win_size[:-1]) / 100
    if position == 'center':
      return full_size / 2 - win_size / 2
    raise SyntaxError('Unknown positional parameter %s' % position)

  def make_rect_from_relative(self, x, y, width, height):
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
    return Rect(x,y,width,height)

  def window(self,width=None,height=None,x=0,y=0,z=0,flags=HWSURFACE,name=None):
    """Create a new window with size and position in pixels"""
    rect = Rect(0,0,0,0)
    if type(width) == type(rect):
      rect = width
    else:
      rect = self.make_rect_from_relative(x, y, width, height)
    win = StaticWindow(rect,z,flags,name)
    return win
