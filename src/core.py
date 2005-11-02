"""just a global placeholder.  We use this to keep shared variables:
        game => the instance of the game being played"""
import core
import pygame
from pygame import display
import window_manager

wm = None
game = None
screen = None
mixer = None
event_bag = None
clock = pygame.time.Clock()

class Mute:
    def Sound(self,file):
        return Mute()
    def play(self):
        pass

def init(opts={}):
    pygame.init()
    if pygame.mixer.get_init():
        core.mixer = pygame.mixer
    else:
        core.mixer = Mute()
    if not pygame.font:
        print 'Unable to initialize font subsystem'
        exit
        
    pygame.mouse.set_visible(0)
    fullscreen = opts.get('fullscreen',0)
    width  = opts.get('width',  640)
    height = opts.get('height', 480)
    dimensions = (width, height)
    flags = pygame.HWSURFACE
    if fullscreen: flags = flags | pygame.FULLSCREEN
    core.screen = core.display.set_mode(dimensions, flags)
    core.wm = window_manager.Minimal()
