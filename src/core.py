"""just a global placeholder.  We use this to keep shared variables:
        game => the instance of the game being played"""
import core
import pygame
from pygame.locals import *
from pygame.sprite import Sprite, RenderPlain, Group
from pygame import color
from pygame import display
from pygame import draw
from pygame import error
from pygame import event
from pygame import font
from pygame import image
from pygame import mixer
from pygame import mouse
from pygame import Rect
from pygame import Surface
from pygame import time
import window_manager

wm = None
game = None
screen = None

def init(opts={}):
  pygame.init()
  fullscreen = opts.get('fullscreen',0)
  height = opts.get('height', 352)
  width  = opts.get('width',  352)
  dimensions = (width, height)
  flags = 0
  if fullscreen: flags = flags | FULLSCREEN
  core.screen = core.display.set_mode(dimensions, flags)
  wm = window_manager.Minimal()
