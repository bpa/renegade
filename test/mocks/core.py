import pygame, core
import window_manager

screen = None
game = None
wm = None

class __Display:
  def flip(self):
    pass

class __Surface:
  def __init__(self):
    self.width = 32
    self.height = 32

  def blit(*args):
    pass

  def fill(*args):
    pass

  def get_width(self, *args):
    return self.width

  def get_height(self, *args):
    return self.height

class __clock:
  def get_fps(self): return 20.0
  def get_time(self): return 45.0
  def get_rawtime(self): return 5
  def tick(self, time=0): pass

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
clock = __clock()
