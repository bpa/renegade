from map import *
from characters import Character
import combat, dialog, NPC, core

class StoneWall(MapBase):
    def __init__(self):
        MapBase.__init__(self,20,20)
        self.set_regen_rate(1)
        self.set_location( (0,0), 'stone', False )
        self.set_location( (1,1), 'stone', False )
        self.set_location( (2,2), 'stone', False )
        self.set_location( (3,2), 'stone', False )
        self.set_location( (4,2), 'stone', False )
        self.set_location( (5,2), 'stone', False )
        self.set_location( (6,1), 'stone', False )
        self.set_location( (7,0), 'stone', False )

        # Put a wise dude here, to talk to.
        sprite = Character('dude_map')
        self.place_entity( sprite, (8,1) )
        sprite.face(SOUTH)
        sprite.always_animate = True
        sprite.animation_speed = 10
        self.add_entry_listener(8,2, self.walk_in_front_of_dude)
        self.add_entry_listener(8,3, self.random_fight)

        tp = NPC.Townsperson('dude_map')
        self.place_entity(tp, (7,7) )
        tp.animation_speed = 5
        tp.set_dialog(( "Hi", "Yeah, what?", "You still here?", \
            "Why are you talking to me?", "I don't know anything that would help you", "ok, you must be bored", "please leave me alone"))

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
    
    def random_fight(self):
        monster = combat.gallery.generate_monster(1)
        combat.Combat(core.game.save_data.hero, monster, core.screen)
