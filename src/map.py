import os
from util import load_image
import pygame
import pygame.image
import pygame.color
from pygame.sprite import Sprite, RenderPlain

import util
import events
from conf import *
from locals import *

SCROLL_EDGE=2
NORTH=0
EAST=1
SOUTH=2
WEST=3
MOVE_VECTORS = ((0,-1),(1,0),(0,1),(-1,0))

def add(a, b):
    return (a[0]+b[0], a[1]+b[1])

class RenderEntity(RenderPlain):
    """Simple RenderPlain subclass that allows you to use image maps"""
    def draw(self, surface):
        spritedict = self.spritedict
        surface_blit = surface.blit
        for s in spritedict.keys():
            surface_blit(s.image, s.rect, s.image_tile)

    def tile_collision(self,pos):
        """True if any MapEntity in the group occupies the pos(x,y)"""
        spritedict = self.spritedict
        for s in spritedict.keys():
            if s.pos == pos: return 1
        return 0

    def scroll(self, vector):
        spritedict = self.spritedict
        for s in spritedict.keys():
            s.rect.move_ip(vector)
    
class MapEntity(Sprite):
    """MapEntity is a sprite that knows how to interact with a map.
       It contains code that can be run periodically, the default
       is to do nothing.  There are also methods for each type of 
       map event.  To do anything useful, subclass this"""
           
    def __init__(self,image,tile_x=0,tile_y=0,direction=NORTH):
        """MapEntity(Surface, tile_x, tile_y, direction)
       
           Surface should be obtained from util.load_image

           tile_x & tile_y specify what image map to use if you join
           multiple images into one map (Characters, Entities, etc)
           legal values are positive integers representing zero based index

           direction is what direction the entity should face,
           can also be set later with MapEntity.face(direction)
           legal values are map.NORTH, map.EAST, map.SOUTH, & map.WEST"""

        Sprite.__init__(self)
        self.pos = (0,0)
        self.map = None
        self.image = image
        self.image_base_x = tile_x * 4 * TILE_SIZE
        self.image_base_y = tile_y * 4 * TILE_SIZE
        self.frame = 0
        self.image_tile = Rect( self.image_base_x, self.image_base_y,
                                TILE_SIZE, TILE_SIZE )
        self.rect = Rect(0,0,TILE_SIZE,TILE_SIZE)
        self.face(direction)
        self.next_frame()
        self.velocity = (0,0)
        self.speed = 5
        self.moving = False # For tile based motion
        self.always_animate = False
        self.animation_count = 1
        self.animation_speed = 5
        self.entered_tile = False

    def speed(self, pixels_per_update):
        """speed(int) Set the movement speed, currently in pixels per update"""
        self.speed = pixels_per_update

    def face(self,direction):
        self.direction = direction
        self.image_tile.top = self.image_base_y + (direction * TILE_SIZE)

    def next_frame(self):
        self.frame = self.frame + 1
        if self.frame > 3: self.frame = 0
        self.image_tile.left = self.image_base_x + (self.frame * TILE_SIZE)

    def move_to(self, pos):
        """Moves the entity to a location without running triggers
           or changing the direction its facing"""
        x, y = pos
        self.pos = pos
        self.rect.top = (TILE_SIZE * y)
        self.rect.left = (TILE_SIZE * x)
#TODO interface with map to see where you're supposed to be on the screen

    def move(self, direction, face_dir=True):
        """move(direction, face_direction=True)
           Start moving if not already"""
        if not self.moving:
            target = add(self.pos, MOVE_VECTORS[direction])
            if face_dir: self.face(direction)
            if self.map.move_ok(target):
                self.direction = MOVE_VECTORS[direction]
                self.pos = target
                self.moving = True
                self.pixels_left_to_move = TILE_SIZE
                self.velocity = (MOVE_VECTORS[direction][0] * self.speed, \
                        MOVE_VECTORS[direction][1] * self.speed)

    def update(self):
        if self.moving:
            self.pixels_left_to_move = self.pixels_left_to_move - self.speed
            self.animation_count = self.animation_count + 1
            if self.animation_count % self.animation_speed == 0:
                self.animation_count = 1
                self.next_frame()
            self.rect.move_ip(self.velocity)
            if self.pixels_left_to_move < self.speed:
                # Move the remaining pixels
                self.velocity = (self.direction[0] * self.pixels_left_to_move, \
                                 self.direction[1] * self.pixels_left_to_move)
                self.rect.move_ip(self.velocity)
                self.entered_tile = True
                self.moving = False
        else:
            if self.always_animate:
                self.animation_count = self.animation_count + 1
                if self.animation_count % self.animation_speed == 0:
                    self.animation_count = 1
                    self.next_frame()

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
        self.map.dirty()

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

class MapBase:
    def __init__(self, width, height):
        self.tile_manager = TileManager()
        default_tile = self.tile_manager.get_tile('floor')
        self.tiles = []
        for x in range(width):
            col = []
            self.tiles.append(col)
            for y in range(height):
                location = MapLocation(self, (x,y), default_tile)
                col.append(location)
        self.width = width
        self.height = height
        self.character = None
        self.entities = RenderEntity()
        self.non_passable_entities = RenderEntity()
        self.viewport = Rect(0,0,SCREEN_SIZE[0],SCREEN_SIZE[1])
        self.offset = Rect(0,0,0,0)
        self.map_tile_coverage = Rect(0,0,SCREEN_SIZE[0]+5,SCREEN_SIZE[1]+5)
        if self.map_tile_coverage.width > width:
            self.map_tile_coverage.width = width
        if self.map_tile_coverage.height > height:
            self.map_tile_coverage.height = height
        self.map_non_scroll_region = \
                    self.viewport.inflate(SCROLL_EDGE*-2,SCROLL_EDGE*-2)
        self.action_listeners = {}
        self.entry_listeners = {}
        self.scrolling = False
        self.frame = 0
        self.map_frames_dirty = [True,True,True,True]
        self.map_frames = []
        for f in range(4):
#TODO Add non hardcoded values for buffer
#TODO Make sure we don't make a larger surface than we need
#TODO   Ex: 5x5 map
            self.map_frames.append(pygame.Surface(((3+width) * TILE_SIZE, \
                    (3+height) * TILE_SIZE)))
        self.update()

    def dispose(self):
        self.tile_manager.clear()
        self.screen = None

    def get(self, x, y):
        if x<0 or y<0: return None
        try:
            return self.tiles[x][y]
        except:
            return None
    
    def calculate_tile_coverage(self, viewable_region):
        if self.character is None:
            return
#TODO Make sure there isn't more tile coverage than map on small maps
        self.map_tile_coverage.center = self.character.pos
        if self.map_tile_coverage.left < 0: self.map_tile_coverage.left = 0
        if self.map_tile_coverage.right > self.width:
            self.map_tile_coverage.right = self.width
        if self.map_tile_coverage.top < 0: self.map_tile_coverage.top = 0
        if self.map_tile_coverage.bottom > self.height:
            self.map_tile_coverage.bottom = self.height
        self.offset.left = \
                (viewable_region.left - self.map_tile_coverage.left) * TILE_SIZE
        self.offset.top = \
                (viewable_region.top - self.map_tile_coverage.top) * TILE_SIZE
        if not self.map_non_scroll_region.collidepoint(self.character.pos):
            self.map_non_scroll_region = \
                   self.viewport.inflate(SCROLL_EDGE*-2,SCROLL_EDGE*-2)

    def set_location(self, loc, tile_name, walkable=True):
        x, y = loc
        location = self.get(x, y)
        tile = self.tile_manager.get_tile(tile_name)
        location.set_tile(tile)
        location.set_walkable(walkable)

    def place_character(self, character, pos, passable=False, direction=NORTH):
        self.character = character
        character.map = self
        self.place_entity(character, pos, passable, direction)
        self.calculate_tile_coverage(self.viewport)

    def place_entity(self, entity, entity_pos, passable=False, direction=NORTH):
        entity.face(direction)
        entity.move_to(entity_pos)
        self.entities.add(entity)
        if not passable:
            self.non_passable_entities.add(entity)

    def add_entry_listener(self, x, y, listener):
        self.entry_listeners[ (x,y) ] = listener

    def get_screen(self):
        return self.screen

    def update(self):
        """Invoked once per cycle of the event loop, to allow animation to update"""
        self.entities.update()
        if self.scrolling:
            axis = self.scroll_axis
            diff = [0,0]
            diff[axis] = self.scroll_anchor - self.character.rect[axis]
            self.entities.scroll(diff)
            diff[axis] = diff[axis] * -1
            self.offset[axis] = self.offset[axis] + diff[axis]
            if not self.character.moving:
                self.scrolling = False
        if self.map_frames_dirty[self.frame]:
            self.build_current_frame()
            self.map_frames_dirty[self.frame] = False

    def draw(self, screen):
#TODO Move the map
        screen.blit(self.map_frames[self.frame], (0,0), self.offset)
        self.entities.draw(screen)
        
    def build_current_frame(self):
#TODO Decide if map_tile_coverage is the right name for this
        blit = self.map_frames[self.frame].blit
        rect = (self.frame * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)
        x = 0
        y = 0
        for col in range(self.map_tile_coverage.left, \
                         self.map_tile_coverage.right):
            column = self.tiles[col]
            for row in range(self.map_tile_coverage.top, \
                             self.map_tile_coverage.bottom):
                blit(column[row].tile, (x,y), rect)
                y = y + TILE_SIZE
            x = x + TILE_SIZE
            y = 0

    def run(self, screen):
        self.screen = screen
        self.offset.width = screen.get_rect().width
        self.offset.height = screen.get_rect().height

        # The main event loop for rendering the map
        clock = pygame.time.Clock()
        event_bag = events.EventUtil()
        iteration = 1
        while True:
            clock.tick(20)
        
            for event in event_bag.process_sdl_events():
                if event.type == QUIT_EVENT:
                    self.dispose()
                    return
            
            if event_bag.is_left(): self.move_character(WEST)
            if event_bag.is_right(): self.move_character(EAST)
            if event_bag.is_up(): self.move_character(NORTH)
            if event_bag.is_down(): self.move_character(SOUTH)
            self.update()
            self.draw(screen)
            pygame.display.flip()
            #I wish there was a better place for this code, but I can't think of any
            if self.character is not None and self.character.entered_tile:
                self.character.entered_tile = False
                # See if there is a listener on entry to this square
                if self.entry_listeners.has_key( self.character.pos ):
                    self.entry_listeners[self.character.pos]()

    def move_character(self, dir):
        self.character.move(dir)
        if not self.scrolling:
            if self.character.moving:
                x,y = self.character.pos
                if dir % 2 == 0:
                    y = self.character.pos[1]
                    if y >= self.map_non_scroll_region.top and \
                       y < self.map_non_scroll_region.bottom:
                        return
                    if y < SCROLL_EDGE or y >= self.height - SCROLL_EDGE:
                        return
                    self.scroll_axis = 1
                else:
                    x = self.character.pos[0]
                    if x >= self.map_non_scroll_region.left and \
                       x < self.map_non_scroll_region.right:
                        return
                    if x < SCROLL_EDGE or x >= self.width - SCROLL_EDGE:
                        return
                    self.scroll_axis = 0
                self.scrolling = True
                vector = MOVE_VECTORS[dir]
                self.map_non_scroll_region.move_ip(vector)
                old_viewport = self.viewport
                self.viewport = old_viewport.move(vector)
                self.scroll_anchor = self.character.rect[self.scroll_axis]
                if not self.map_tile_coverage.contains(self.viewport):
                    self.calculate_tile_coverage(old_viewport)
                    self.dirty()

    def dirty(self):
        for f in range(4):
            self.map_frames_dirty[f] = True

    def move_ok(self, target_pos):
        x, y = target_pos
        target = self.get(x,y)
        return target is not None \
               and target.is_walkable() \
               and not self.non_passable_entities.tile_collision(target_pos)

class TileManager(object):
    def __init__(self):
        self.tiles = {}

    def get_tile(self, name, colorkey=None):
        if not self.tiles.has_key(name):
            image = util.load_image(TILES_DIR, name)
            self.tiles[name] = image
        return self.tiles[name]

    def clear(self):
        self.tiles.clear()
