from map import MapBase
from characters import Character
import dialog

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
        dialog.message("You stand before the wise dude!  Here is a lot " +
                       "of text that you will need to split across at " +
                       "least two lines, perhaps several more!  And as " +
                       "a special feature, if this first line is longer " +
                       "than the next dialog, then it will even be trimmed " +
                       "properly!")       
        choice = dialog.question(
           "Since this is a very very wise man, he has much " +
           "to say to you.  This may even spill over into " +
           "another dialog!", 
           [ "No, make it stop!", 
             "Yes, Continue!",
             "I can't decide",
             "Who knows?" ])       
        
        if choice == "No, make it stop!":
            dialog.message("No! Stopping is not an option!")
        elif choice == "Yes, Continue!":
            dialog.message("Good, I appreciate your patience.")
        elif choice == "I can't decide":
            dialog.message("Well, hurry and make up your mind!")
        elif choice == "Who knows?":
            dialog.message("Ummm.. you're supposed to know that.")
    

