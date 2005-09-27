import core
from core import Sprite, Group

class Window(Sprite):
  """Base class for windows.  Must show() before useful.  The update function will be called with a time argument (milliseconds since last call).  Just assign a new function (or lambda) to update and have it draw the image."""
  def __init__(self, image, rect, wm):
    Sprite.__init__(self)
    self.image = image
    self.rect = rect
    self.wm = wm
  
  def show(self):
    self.wm.show(self)

  def hide(self):
    self.kill()

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
    black = core.color.Color('Black')
    core.screen.fill(black)
    core.display.flip()

  def show(self, sprite):
    self.add(sprite)

  def window(self,height=40,width=40,x=0,y=0):
    """Create a new window with size and position in pixels"""
    return Window(None,None,self)
