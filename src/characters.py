import util
from conf import *

class Character(object):
    def __init__(self, image_names):
        """Construct a character using the specified files as animation"""
        self.images = map(lambda x: util.load_image(CHARACTERS_DIR, x, True), \
                          image_names)
        self.iter = iter( self.next_image_generator() )

    def update(self):
        self.image = self.iter.next()

    def draw(self, screen, x_pos, y_pos):
        screen.blit( self.image, (x_pos,y_pos) )

    def next_image_generator(self):
        while True:
            for image in self.images: 
                for i in range(10): yield image
