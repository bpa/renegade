import os
import pygame
import pygame.image
from pygame.locals import *

import util
from conf import *

def add(a, b):
    return (a[0]+b[0], a[1]+b[1])

class MapLocation(object):
    "One square on the overview map"
    def __init__(self, map, loc, tile, walkable=True):
        self.loc = loc
        self.map = map
        self.tile = tile
        self.x_base = loc[0] * TILE_SIZE
        self.y_base = loc[1] * TILE_SIZE
        self.character = None
        self.walkable = walkable

    def set_walkable(self, walkable):
        self.walkable = walkable

    def is_walkable(self):
        return self.walkable

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
        self.width = width
        self.height = height
        self.char_min_x = int(SCREEN_SIZE[0] * TILE_SIZE * 0.3)
        self.char_max_x = int(SCREEN_SIZE[0] * TILE_SIZE * 0.7)
        self.char_min_y = int(SCREEN_SIZE[1] * TILE_SIZE * 0.3)
        self.char_max_y = int(SCREEN_SIZE[1] * TILE_SIZE * 0.7)
        self.character = None
        self.update()

    def get(self, x, y):
        try:
            return self.rows[x][y]
        except:
            return None
    
    def draw(self, screen):
        for row in self.rows:
            for location in row:
                location.draw(screen, self.x_offset, self.y_offset)
        if self.character is not None:
            self.character.draw(screen, self.char_x, self.char_y)

    def set_location(self, loc, tile_name, walkable=True):
        x, y = loc
        location = self.get(x, y)
        tile = self.tile_manager.get_tile(tile_name)
        location.set_tile(tile)
        location.set_walkable(walkable)

    def place_character(self, character, character_pos):
        self.character = character
        self.character_pos = character_pos
        self.character_offset = (0,0)
        self.character_direction = None
        self.char_x = character_pos[0] * TILE_SIZE
        self.char_y = character_pos[1] * TILE_SIZE
        self.character.update()

    def update(self):
        """Invoked once per cycle of the event loop, to allow animation to update"""
        if self.character is not None:
            if self.character_direction is not None:
                velocity = (self.character_direction[0]*MOVE_SPEED, \
                            self.character_direction[1]*MOVE_SPEED)
                self.character_offset = add(self.character_offset, velocity)
                x = abs( self.character_offset[0] + self.character_offset[1] )
                if x >= TILE_SIZE:
                    self.character_pos = add(self.character_pos,
                                             self.character_direction)
                    # TODO: Emit some kind of move_complete event
                    self.character_direction = None
                    self.character_offset = (0,0)
                self.char_x = self.character_offset[0] 
                self.char_x = self.char_x + TILE_SIZE*self.character_pos[0]
                self.char_x = self.char_x + self.x_offset
                self.char_y = self.character_offset[1] 
                self.char_y = self.char_y + TILE_SIZE*self.character_pos[1]
                self.char_y = self.char_y + self.y_offset
                if self.char_x < self.char_min_x: 
                    self.x_offset = self.x_offset - self.char_x + self.char_min_x
                    self.char_x = self.char_min_x
                if self.char_x > self.char_max_x:
                    self.x_offset = self.x_offset - self.char_x + self.char_max_x
                    self.char_x = self.char_max_x
                if self.char_y < self.char_min_y:
                    self.y_offset = self.y_offset - self.char_y + self.char_min_y
                    self.char_y = self.char_min_y
                if self.char_y > self.char_max_y:
                    self.y_offset = self.y_offset - self.char_y + self.char_max_y
                    self.char_y = self.char_max_y
            self.character.update()

    def move_character_left(self):
        x,y = self.character_pos
        target = (x-1, y)
        if self.move_ok(target):
            self.character_direction = (-1, 0)

    def move_character_right(self):
        x,y = self.character_pos
        target = (x+1, y)
        if self.move_ok(target):
            self.character_direction = (1, 0)

    def move_character_up(self):
        x,y = self.character_pos
        target = (x, y-1)
        if self.move_ok(target):
            self.character_direction = (0, -1)

    def move_character_down(self):
        x,y = self.character_pos
        target = (x, y+1)
        if self.move_ok(target):
            self.character_direction = (0, 1)

    def move_ok(self, target_pos):
        x, y = target_pos
        target = self.get(x,y)
        return target is not None \
               and target.is_walkable() \
               and self.character_direction is None

class TileManager(object):
    def __init__(self):
        self.tiles = {}

    def get_tile(self, name, colorkey=None):
        if not self.tiles.has_key(name):
            image = util.load_image(TILES_DIR, name)
            self.tiles[name] = image
        return self.tiles[name]
