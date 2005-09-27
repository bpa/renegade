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

def init(opts={}):
  height = opts.get('height', 352)
  width  = opts.get('width',  352)
  dimensions = (width, height)
  core.screen = pygame.Surface(dimensions)
  wm = window_manager.Minimal()

class __Display:
  def flip(self):
    pass

display = __Display()
