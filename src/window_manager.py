import core
from core import Sprite, Group

class Window(Sprite):
  """Base class for windows.  Must show() before useful.  The update function will be called with a time argument (milliseconds since last call).  Just assign a new function (or lambda) to update and have it draw the image."""
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

  def update(self):
    pass

  def set_event_mask(self, mask):
    pass

  def handle_event(self, event):
    pass

class Minimal(Group):
  def __init__(self):
    Group.__init__(self)
    self.windows = core.RenderPlain()
    self.zorder = []
    black = core.color.Color('Black')
    core.screen.fill(black)
    core.display.flip()

  def add(self, sprite):
    Group.add(self, sprite)
    self.sort_by_z()

  def sort_by_z(self):
    zorder = []
    for s in self.spritedict.keys():
      zorder.append(s)
    zorder.sort(key=lambda sprite: sprite.z)
    self.zorder = zorder

  def show(self, sprite):
    self.add(sprite)

  def hide(self, sprite):
    self.remove(sprite)
    self.sort_by_z()

  def draw(self):
    surface_blit = core.screen.blit
    for s in self.zorder:
        surface_blit(s.image, s.rect)

  def window(self,width=None,height=None,x=0,y=0,z=0):
    """Create a new window with size and position in pixels"""
    if width  == None: width  = core.screen.get_width()
    if height == None: height = core.screen.get_height()
    if width  < 1: width  = core.screen.get_width()  + width
    if height < 1: height = core.screen.get_height() + height
    if x < 0: x = core.screen.get_width()  + x
    if y < 0: y = core.screen.get_height() + y
    image = core.Surface((width,height))
    rect = core.Rect(x,y,width,height)
    win = Window(image,rect,z,self)
    self.windows.add(win)
    self.add(win)
    return win
