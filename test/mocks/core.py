import pygame
from pygame.sprite import Sprite, Group, RenderPlain
from pygame import image, Rect, color, Surface
from pygame import USEREVENT, error
from pygame.locals import RLEACCEL
screen = pygame.Surface((40,40))
import window_manager

class Display:
  def flip(self):
    pass

display = Display()
wm = window_manager.Minimal()
