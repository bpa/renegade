import pygame
import map
from pygame.locals import *

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
    current_map.set_location( (0,0), 'stone' )
    current_map.set_location( (1,1), 'stone' )
    current_map.set_location( (2,2), 'stone' )
    current_map.set_location( (3,2), 'stone' )
    current_map.set_location( (4,2), 'stone' )
    current_map.set_location( (5,2), 'stone' )
    current_map.set_location( (6,1), 'stone' )
    current_map.set_location( (7,0), 'stone' )

    # Start a main event loop for testing
    clock = pygame.time.Clock()
    while True:
        clock.tick(20)
    
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
        
            current_map.draw(screen)        
            pygame.display.flip()

test_main_loop()
