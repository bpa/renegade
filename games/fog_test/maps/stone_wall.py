from map import MapBase

class stone_wall(MapBase):
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
