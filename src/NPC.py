from map import *
import dialog, random

class Townsperson(MapEntity):
    "A normal MapEntity that talks when activated and moves around on its own"
    
    def __init__(self,image,tile_x=0,tile_y=0,direction=NORTH):
        MapEntity.__init__(self,image,tile_x,tile_y,direction)
        self.__next_move = 30

    def set_dialog(self, messages):
        """set_dialog(Tuple or Array)
           The strings in the array will be spoken in a loop"""
        self.dialog_text = messages
        self.current_dialog = 0

    def activate(self):
        dialog.message(self.dialog_text[self.current_dialog])
        self.current_dialog = self.current_dialog + 1
        if self.current_dialog >= len(self.dialog_text):
            self.current_dialog = 0

    def move_to(self, pos):
        MapEntity.move_to(self, pos)
        self.base_pos = pos

#TODO Make the Townsperson stay home.  I.E. make the random direction
#TODO     statistically keep the townsperson stay within a certain range
#TODO     from where they were last moved to
    def update(self):
        if not self.moving:
            if self.__next_move < 1:
                self.__next_move = random.randint(10,75)
                direction = random.randint(0,3)
                self.move(direction)
            self.__next_move = self.__next_move - 1
        MapEntity.update(self)
