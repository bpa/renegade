import util
from conf import *
from map import MapEntity

class Character(MapEntity):
    def __init__(self, image_map, tile_x=0, tile_y=0):
        """Construct a character using the specified image_map as animation"""
        image = util.load_image(CHARACTERS_DIR, image_map, True)
        MapEntity.__init__(self,image,tile_x,tile_y)
