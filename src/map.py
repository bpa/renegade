import os
import core
from pygame import Rect, Surface
from pygame.sprite import Sprite, RenderPlain
from util import load_image
from conf import *
import util
import events
import menu
import dialog
from locals import *
from window_manager import Window
from weakref import proxy
import gc, traceback

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
    def draw(self, surface_blit):
        spritedict = self.spritedict
        for s in spritedict.keys():
            surface_blit(s.image, s.rect, s.image_tile)

    def entity_collisions(self,pos):
        """List of MapEntity in the group that occupy the pos(x,y)"""
        entities = []
        spritedict = self.spritedict
        for s in spritedict.keys():
            if s.pos == pos: entities.append(s)
        return entities

    def scroll(self, vector):
        spritedict = self.spritedict
        for s in spritedict.keys():
            s.rect.move_ip(vector)
    
    def run_command(self, method):
        spritedict = self.spritedict
        cmd = "s.%s" % method
        for s in spritedict.keys():
            eval(cmd)
        
class MapEntity(Sprite):
    """MapEntity is a sprite that knows how to interact with a map.
       It contains code that can be run periodically, the default
       is to do nothing.  There are also methods for each type of 
       map event.  To do anything useful, subclass this"""

    def __init__(self, image_map=None):
        self.name = self.__class__.__name__
        if image_map is not None:
            self.init(image_map)
           
    def __getstate__(self):
        dict = self.__dict__.copy()
        dict.pop('map')
        dict.pop('_Sprite__g')
        dict.pop('image')
        return dict

    def __setstate__(self, dict):
        self.__dict__ = dict
        Sprite.__init__(self)
        self.image = util.load_image(CHARACTERS_DIR, *self.image_args)

    def init(self,image_map,tile_x=0,tile_y=0,color_key=None):
        """MapEntity(Surface, tile_x, tile_y, direction)
       
           Surface should be obtained from util.load_image

           tile_x & tile_y specify what image map to use if you join
           multiple images into one map (Characters, Entities, etc)
           legal values are positive integers representing zero based index

           direction is what direction the entity should face,
           can also be set later with MapEntity.face(direction)
           legal values are map.NORTH, map.EAST, map.SOUTH, & map.WEST"""

        image = util.load_image(CHARACTERS_DIR, image_map, True, color_key)
        Sprite.__init__(self)
        self.image_args = (image_map, True, color_key)
        self.pos = (0,0)
        self.map = None
        self.image = image
        self.image_base_x = tile_x * 3 * TILE_SIZE
        self.image_base_y = tile_y * 4 * TILE_SIZE
        self.frame = 0
        self.image_tile = Rect( self.image_base_x, self.image_base_y,
                                TILE_SIZE, TILE_SIZE )
        self.rect = Rect(0,0,TILE_SIZE,TILE_SIZE)
        self.face(NORTH)
        self.next_frame()
        self.velocity = (0,0)
        self.speed = 4
        self.moving = False # For tile based motion
        self.always_animate = False
        self.animation_count = 1
        self.animation_speed = 4
        self.entered_tile = False
        self.can_trigger_actions = 0

    def speed(self, pixels_per_update):
        """speed(int) Set the movement speed, currently in pixels per update"""
        self.speed = pixels_per_update

    def face(self,direction):
        self.facing = direction
        self.image_tile.top = self.image_base_y + (self.facing * TILE_SIZE)

    def next_frame(self):
        self.frame = self.frame + 1
        if self.frame > 3: self.frame = 0
        if self.frame == 3:
          self.image_tile.left = self.image_base_x + (1 * TILE_SIZE)
        else:
          self.image_tile.left = self.image_base_x + (self.frame * TILE_SIZE)

    def move_to(self, pos):
        """Moves the entity to a location without running triggers
           or changing the direction its facing"""
        x, y = pos
        self.pos = pos
        self.rect.top  = TILE_SIZE * (y - self.map.viewport.top)
        self.rect.left = TILE_SIZE * (x - self.map.viewport.left)

    def move(self, direction, face_dir=True):
        """move(direction, face_direction=True)
           Start moving if not already"""
        if not self.moving:
            target = add(self.pos, MOVE_VECTORS[direction])
            if face_dir: self.face(direction)
            if self.map.move_ok(target, self):
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

################## The following are all action methods ########################
############ These are the ones you will override most commonly ################

#TODO Decide if these methods should have a prefix like action_
    def activate(self):
        """Called when the character hits the action key while facing entity"""
        pass

    def touch(self):
        """Called when the character makes contact with the entity
           This can be one of the following conditions:
              The character attempts to move into the entity
              The entity attempts to move into the character
           This will not be triggered if the sprites overlap temporarily.
           If it should, add an enhancement request and I'll fix it"""
        pass

    def enter_map(self):
        pass

    def leave_map(self):
        pass
              
class MapLocation(object):
    "One square on the overview map"
    def __init__(self, map, loc, tile, walkable=True):
        self.loc = loc
        self.map = proxy(map)
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

class MapBase(Window):
    def __init__(self, width, height, default_tile_name='floor'):
        Window.__init__(self,None,10)
        self.tile_manager = TileManager()
        default_tile = self.tile_manager.get_tile(default_tile_name)
        self.tiles = []
        for x in range(width):
            col = []
            self.tiles.append(col)
            for y in range(height):
                location = MapLocation(self, (x,y), default_tile)
                col.append(location)
        self.width = width
        self.height = height
        tiles_x = core.screen.get_width() / 32
        tiles_y = core.screen.get_height() / 32
        self.dimentions = Rect(0,0,width,height)
        self.character = None
        self.entities = RenderEntity()
        self.non_passable_entities = RenderEntity()
        self.viewport = Rect(0,0,tiles_x,tiles_y)
        self.offset = Rect(0,0,0,0)
        self.map_tile_coverage = Rect(0,0,tiles_x+5,tiles_y+5)
        if self.map_tile_coverage.width > width:
            self.map_tile_coverage.width = width
        if self.map_tile_coverage.height > height:
            self.map_tile_coverage.height = height
        self.map_non_scroll_region = \
                    self.viewport.inflate(SCROLL_EDGE*-2,SCROLL_EDGE*-2)
        self.action_listeners = {}
        self.entry_listeners = {}
        self.movement_listeners = []
        self.scrolling = False
        self.frame = 0
        self.map_frames_dirty = [True,True,True,True]
        self.map_frames = []
        self.heal_points = 0
        self.regen_rate = 2000000000
        self.sound = core.mixer.Sound('%s/sounds/beep.wav' % DATA_DIR)
        for f in range(4):
#TODO Add non hardcoded values for buffer
#TODO Make sure we don't make a larger surface than we need
#TODO   Ex: 5x5 map
            self.map_frames.append(Surface(((1+width) * TILE_SIZE, \
                    (1+height) * TILE_SIZE)))

    def __getstate__(self):
        dict = {}
        dict['width']  = self.width
        dict['height'] = self.height
        return dict
  
    def __setstate__(self, dict):
        if self.__class__.__name__ == 'MapBase':
          self.__init__(dict['width'],dict['height'])
        else:
          self.__init__()
        self.blur_events()

    def dispose(self):
        self.destroy()
        del self.tiles
        self.tile_manager.clear()
        del self.action_listeners
        del self.entry_listeners
        del self.movement_listeners
        self.entities.empty()
        self.non_passable_entities.empty()
        self.character.map = None
    
    def set_regen_rate(self, rate):
        self.regen_rate = rate

    def get(self, x, y):
        if x<0 or y<0: return None
        try:
            return self.tiles[x][y]
        except:
            return None
    
    def calculate_tile_coverage(self, viewable):
        if self.character is None:
            return
        coverage = self.map_tile_coverage
        coverage.center = self.character.pos
        view_scroll = viewable.inflate(8,8)
        coverage.clamp_ip(view_scroll)
        coverage.clamp_ip(self.dimentions)
        self.offset.left = (viewable.left - coverage.left) * TILE_SIZE
        self.offset.top  = (viewable.top  - coverage.top ) * TILE_SIZE
        if not self.map_non_scroll_region.collidepoint(self.character.pos):
            self.map_non_scroll_region = \
                   self.viewport.inflate(SCROLL_EDGE*-2,SCROLL_EDGE*-2)

    def set_location(self, loc, tile_name, walkable=True, tile_pos=None):
        x, y = loc
        location = self.get(x, y)
        tile = self.tile_manager.get_tile(tile_name, None, tile_pos)
        location.set_tile(tile)
        location.set_walkable(walkable)

    def place_character(self, character, pos, passable=False, direction=NORTH):
        self.character = character
        character.map = self
        character.can_trigger_actions = 1
        if not self.viewport.collidepoint(pos):
          self.viewport.center = pos
          self.viewport.clamp_ip(self.dimentions)
        self.place_entity(character, pos, passable, direction)
        self.calculate_tile_coverage(self.viewport)

    def place_entity(self, entity, entity_pos, passable=False, direction=NORTH):
        entity.face(direction)
        entity.map = self
        entity.move_to(entity_pos)
        self.entities.add(entity)
        if not passable:
            self.non_passable_entities.add(entity)

    def add_entry_listener(self, x, y, listener):
        self.entry_listeners[ (x,y) ] = listener

    def add_movement_listener(self, listener):
        self.movement_listeners.append(listener)

    def update(self):
        """Invoked once per cycle of the event loop, to allow animation to update"""
        if self.character.entered_tile:
            self.character.entered_tile = False
            self.check_heal()
            if self.entry_listeners.has_key( self.character.pos ):
                self.entry_listeners[self.character.pos]()
            for listener in self.movement_listeners:
                listener()
        if self.scrolling:
            axis = self.scroll_axis
            diff = [0,0]
            diff[axis] = self.scroll_anchor - self.character.rect[axis]
            self.entities.scroll(diff)
            diff[axis] = diff[axis] * -1
            self.offset[axis] = self.offset[axis] + diff[axis]
            if not self.character.moving:
                self.scrolling = False
        if self.is_left(): self.move_character(WEST)
        if self.is_right(): self.move_character(EAST)
        if self.is_up(): self.move_character(NORTH)
        if self.is_down(): self.move_character(SOUTH)
        if self.map_frames_dirty[self.frame]:
            self.build_current_frame()
            self.map_frames_dirty[self.frame] = False
        self.entities.update()

    def draw(self, blit):
      blit(self.map_frames[self.frame], (0,0), self.offset)
      self.entities.draw(blit)

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

    def init(self):
        self.offset.width = core.screen.get_rect().width
        self.offset.height = core.screen.get_rect().height
        self.entities.run_command('enter_map')

    def handle_event(self,event):
        if event.type == PUSH_ACTION_EVENT: self.character_activate()
        if event.type == PUSH_ACTION2_EVENT: menu.run_main_menu()

    def check_heal(self):
        self.heal_points = self.heal_points + 1
        if self.heal_points >= self.regen_rate:
            core.game.save_data.hero.regenerate()
            self.heal_points = 0

    def character_activate(self):
        if not self.character.moving:
            target = add(self.character.pos,MOVE_VECTORS[self.character.facing])
            entities = self.non_passable_entities.entity_collisions(target)
            for e in entities:
                e.activate()
        
    def move_character(self, dir):
        self.character.move(dir)
        if not self.scrolling:
            if self.character.moving:
                nsr = self.map_non_scroll_region
                x,y = self.character.pos

                if dir % 2 == 0: # North or south
                    if y <  nsr.bottom and \
                       y >= nsr.top:
                          return
                    if y <  SCROLL_EDGE or \
                       y >= self.height - SCROLL_EDGE:
                          return
                    self.scroll_axis = 1
                else:            # East or west
                    if x <  nsr.right and \
                       x >= nsr.left:
                          return
                    if x <  SCROLL_EDGE or \
                       x >= self.width - SCROLL_EDGE:
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

    def move_ok(self, target_pos, character):
        x, y = target_pos
        target = self.get(x,y)
        if target is not None and target.is_walkable():
            entities = self.non_passable_entities.entity_collisions(target_pos)
            if len(entities) > 0:
                if character.can_trigger_actions:
                    for e in entities:
                        e.touch()
                else:
                    for e in entities:
                        if e.can_trigger_actions: character.touch()
                return 0
            else:
                self.sound.play()
                return 1
        else:
            return 0

    def get_tiles_from_ascii(self,ascii,tile_map):
        for y in range(self.height):
            line = ascii[y]
            for x in range(self.width):
                c = line[x]
                args = tile_map[c]
                pos = None
                if len(args) > 1:
                    pos = args[1]
                self.set_location( (x,y), args[0],
                    tile_map['walkable'].find(c)!=-1, pos )

class TileManager(object):
    def __init__(self):
        self.tiles = {}

    def get_tile(self, name, colorkey=None, tile_pos=None):
        key = (name, tile_pos)
        if not self.tiles.has_key( key ):
            image = util.load_image(TILES_DIR, name)
            image = util.load_image(TILES_DIR, name).convert()
            if tile_pos is not None:
                tmp = Surface( (TILE_SIZE, TILE_SIZE) )
                rect = Rect(tile_pos[0]*TILE_SIZE, tile_pos[1]*TILE_SIZE,TILE_SIZE,TILE_SIZE)
                tmp.blit(image, (0,0), rect)
                image = tmp.convert()
            self.tiles[key] = image
        return self.tiles[key]

    def clear(self):
        self.tiles.clear()
