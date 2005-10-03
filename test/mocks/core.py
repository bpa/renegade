import pygame, core
import window_manager

screen = None
game = None
wm = None

class __Display:
  def flip(self):
    pass

class __Surface:
  def blit(*args):
    pass

  def fill(*args):
    pass

  def get_width(*args):
    return 32

  def get_height(*args):
    return 32

class Mute:
    def Sound(self,file):
        return Mute()
    def play(self):
        pass

def init(opts={}):
  pygame.display.init()
  core.mixer = Mute()
  core.screen = __Surface()
  wm = window_manager.Minimal()

display = __Display()
