import os
import pygame.image
from pygame.locals import *

def load_image(dir, name, alpha=False, colorkey=None):
    fullname = os.path.join(dir, "%s.png" % name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    if alpha: image = image.convert_alpha()
    else: image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image
