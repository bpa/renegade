import util

import pygame
import pygame.image
import pygame.event
import pygame.color
from pygame.time import Clock
from pygame.locals import *

def init():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    window = MainWindow(screen)
    window.run()
    

class Tile(object):
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x*32, y*32, 32, 32)
        self.image = image

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class MainWindow(object):
    def __init__(self, screen):
        self.screen = screen
        self.tiles = {}
        self.blank = pygame.Surface((32, 32))
        self.blank.fill( pygame.color.Color('blue') )
        for x in range(20):
            for y in range(20):
                tile = Tile(x, y, self.blank)
                self.tiles[(x,y)] = tile

    def draw(self, screen):
        for loc in self.tiles:
            tile = self.tiles[loc]
            tile.draw(screen)

    def run(self):
        clock = Clock()
        while True:
            clock.tick(50)
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if event.type == KEYDOWN:
                    return
            self.draw(self.screen)

init()
