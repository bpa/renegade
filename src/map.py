import os
import pygame
import pygame.image
from pygame.locals import *
from conf import *

class MapLocation(object):
    "One square on the overview map"
    def __init__(self, map, loc, tile):
        self.loc = loc
        self.map = map
        self.tile = tile
        self.x_base = loc[0] * TILE_SIZE
        self.y_base = loc[1] * TILE_SIZE

    def set_tile(self, tile):
        self.tile = tile

    def loc(self):
        return self.loc
    
    def neighbor_north(self):
        return self.map.get( self.loc[0], self.loc[1] - 1 )

    def neighbor_east(self):
        return self.map.get( self.loc[0]+1, self.loc[1] )

    def neighbor_south(self):
        return self.map.get( self.loc[0], self.loc[1]+1 )

    def neighbor_west(self):
        return self.map.get( self.loc[0]-1, self.loc[1] )

    def draw(self, screen, x_offset, y_offset):
        x = x_offset + self.x_base
        y = y_offset + self.y_base
        screen.blit(self.tile, (x,y) )
        
class MapBase:
    def __init__(self, width, height):
        self.tile_manager = TileManager()
        default_tile = self.tile_manager.get_tile('floor')
        self.rows = []
        for x in range(width):
            row = []
            self.rows.append(row)
            for y in range(height):
                location = MapLocation(self, (x,y), default_tile)
                row.append(location)
        self.x_offset = 0
        self.y_offset = 0

    def get(self, x, y):
        try:
            return self.rows[x][y]
        except:
            return None
    
    def draw(self, screen):
        for row in self.rows:
            for location in row:
                location.draw(screen, self.x_offset, self.y_offset)

    def set_location(self, loc, tile_name):
        x, y = loc
        location = self.get(x, y)
        tile = self.tile_manager.get_tile(tile_name)
        location.set_tile(tile)

class TileManager(object):
    def __init__(self):
        self.tiles = {}

    def get_tile(self, name, colorkey=None):
        if not self.tiles.has_key(name):
            fullname = os.path.join(TILES_DIR, "%s.png" % name)
            try:
                image = pygame.image.load(fullname)
            except pygame.error, message:
                print 'Cannot load image:', name
                raise SystemExit, message
            image = image.convert()
            if colorkey is not None:
                if colorkey is -1:
                    colorkey = image.get_at((0,0))
                image.set_colorkey(colorkey, RLEACCEL)
            self.tiles[name] = image
        return self.tiles[name]
