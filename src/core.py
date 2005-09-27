"""just a global placeholder.  We use this to keep shared variables:
        game => the instance of the game being played"""
import core
import pygame
from pygame.locals import *
from pygame.sprite import Sprite, RenderPlain
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
test_element = 1

game = None
screen = None

def init(opts):
  pygame.init()
  dimensions = (opts['width'], opts['height'])
  flags = 0
  if opts['fullscreen']: flags = flags | FULLSCREEN
  core.screen = core.display.set_mode(dimensions, flags)

def run(opts):
  pass
