from map import MapBase
from characters import Character

class StoneWall(MapBase):
    def __init__(self):
        MapBase.__init__(self,20,20)
        self.set_location( (0,0), 'stone', False )
        self.set_location( (1,1), 'stone', False )
        self.set_location( (2,2), 'stone', False )
        self.set_location( (3,2), 'stone', False )
        self.set_location( (4,2), 'stone', False )
        self.set_location( (5,2), 'stone', False )
        self.set_location( (6,1), 'stone', False )
        self.set_location( (7,0), 'stone', False )

        # Put a wise dude here, to talk to.
        sprite = Character( ('dude1', 'dude2') )
        self.place_sprite( sprite, (8,1) )
        self.get(8,1).set_walkable( False )
        self.add_entry_listener(8,2, self.walk_in_front_of_dude)

    def walk_in_front_of_dude(self):
        print "You walked in front of the dude!"

