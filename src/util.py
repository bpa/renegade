import os
import pygame.image
import pygame.surface
from pygame.locals import *

cached_images = {}

def load_image(dir, name, alpha=False, colorkey=None):
    global cached_images
    fullname = os.path.join(dir, "%s.png" % name)
    if cached_images.has_key(fullname):
        return cached_images[fullname]
    else:
        try:
            image = pygame.image.load(fullname)
        except pygame.error, message:
            print 'Cannot load image:', name
            raise SystemExit, message
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        if alpha: image = image.convert_alpha()
        else: image = image.convert()
        cached_images[fullname] = image
    return image
