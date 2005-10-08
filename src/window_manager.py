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

pygame.font.init()
__f = font.Font(None, 16).render
__y = color.Color("yellow")

fps_win = None
fps_color = color.Color("black")

def init_fps_win():
    global fps_win, fps_color
    fps_win = Surface((165,35), HWSURFACE)
    fps_win.set_alpha(180)

def print_fps():
    global fps_win, fps_color
    if fps_win == None: init_fps_win()
    c = core.clock
    #b = core.screen.blit
    b = fps_win.blit
    fps_win.fill(fps_color)
    b(__f("FPS: %.1f" % c.get_fps(),True,__y), (5,0))
    b(__f("Render Time: %ims" % c.get_rawtime(),True,__y), (5,10))
    b(__f("Time between frames: %ims" % c.get_time(),True,__y), (5,20))
    core.screen.blit(fps_win, (5,0))

class Window(Sprite):
  """Base class for windows.  Just assign a new function (or lambda) to update and have it draw the image."""
  def __init__(self, image, rect, z, wm):
    Sprite.__init__(self)
    self.image = image
    self.rect = rect
    self.wm = wm
    self.z = z
  
  def show(self):
    self.wm.show(self)

  def hide(self):
    self.wm.hide(self)

  def destroy(self):
    self.kill()
    self.wm.sort_by_z()

  def update(self):
    pass

  def set_event_mask(self, mask):
    pass

  def handle_event(self, event):
    pass

class Minimal(AbstractGroup):
  def __init__(self):
    AbstractGroup.__init__(self)
    self.windows = RenderPlain()
    self.zorder = []
    black = color.Color('Black')
    core.screen.fill(black)
    core.display.flip()

  def add(self, sprite):
    AbstractGroup.add(self, sprite)
    self.sort_by_z()

  def sort_by_z(self):
    zorder = []
    for s in self.spritedict.keys():
      zorder.append(s)
    zorder.sort(self.reverse_z_sort_sprites)
    self.zorder = zorder

  def reverse_z_sort_sprites(self, a, b):
  	return cmp(b.z, a.z)

  def show(self, sprite):
    self.add(sprite)

  def hide(self, sprite):
    self.remove(sprite)
    self.sort_by_z()

  def draw(self):
    surface_blit = core.screen.blit
    for s in self.zorder:
        surface_blit(s.image, s.rect)
    print_fps()
    core.display.flip()
    core.clock.tick(20)

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
      image = Surface((rect.width,rect.height),flags)
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
      image = Surface((width,height),flags)
      rect = Rect(x,y,width,height)
    win = Window(image,rect,z,self)
    self.windows.add(win)
    self.add(win)
    return win
