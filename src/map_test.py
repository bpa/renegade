import pygame
from pygame.locals import *

import map
import characters

def run_test():
    pygame.init()

    screen = pygame.display.set_mode((352, 352))
    pygame.display.set_caption('Renegade: Map Test')
    pygame.mouse.set_visible(0)

    if not pygame.font:
        print 'Unable to initialize font subsystem'
        exit

    # Initialize a test map
    current_map = map.MapBase(20, 20)
    current_map.set_location( (0,0), 'stone', False )
    current_map.set_location( (1,1), 'stone', False )
    current_map.set_location( (2,2), 'stone', False )
    current_map.set_location( (3,2), 'stone', False )
    current_map.set_location( (4,2), 'stone', False )
    current_map.set_location( (5,2), 'stone', False )
    current_map.set_location( (6,1), 'stone', False )
    current_map.set_location( (7,0), 'stone', False )
    
    # Create the character
    character = characters.Character( ('dude1', 'dude2', 'dude3', 'dude4') )
    current_map.place_character( character, (4,4) )
    current_map.run(screen)
    current_map.dispose()

run_test()
