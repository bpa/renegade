import pygame, core
from pygame.sprite import Sprite, Group, RenderPlain
from pygame import image, Rect, color, Surface
from pygame import USEREVENT, error, font
from pygame.locals import *
from pygame import draw, event, mixer, mouse, time
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

def init(opts={}):
  core.screen = __Surface()
  wm = window_manager.Minimal()

display = __Display()
