import pygame
from pygame.locals import *

import map
import characters

def test_main_loop():
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

    # Start a main event loop for testing
    clock = pygame.time.Clock()
    while True:
        clock.tick(20)
    
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                elif event.key == K_LEFT:
                    current_map.move_character_left()
                elif event.key == K_RIGHT:
                    current_map.move_character_right()
                elif event.key == K_UP:
                    current_map.move_character_up()
                elif event.key == K_DOWN:
                    current_map.move_character_down()
        
        current_map.update()
        current_map.draw(screen)        
        pygame.display.flip()

test_main_loop()
