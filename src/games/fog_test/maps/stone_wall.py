from map import *
from characters import Character
import combat, dialog, NPC, games.fog_test.items
import core
from games.fog_test.items import *
import game

class ArmorMerchant(NPC.Merchant):
    def __init__(self, sprite_name):
        NPC.Merchant.__init__(self, sprite_name)
        self.set_intro("Welcome to Ye Olde Armor Shoppe!  How may I be of service?")
        self.set_item_list( (ToughShirt(), DiamondPlate()) )

    def purchased(self, armor):
        game.save_data.hero.equip_armor( armor )

class WeaponMerchant(NPC.Merchant):
    def __init__(self, sprite_name):
        NPC.Merchant.__init__(self, sprite_name)
        self.set_intro("Avast ye swarthies!  Tis time to be buyin a weapon now, is it?")
        self.set_item_list( (Dagger(), Dirk(), LightSaber()) )

    def purchased(self, weapon):
        game.save_data.hero.equip_weapon( weapon )

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

        # Place the armor merchant
        armor_dude = ArmorMerchant('dude_map')
        self.place_entity( armor_dude, (12,4) )
        armor_dude.face(WEST)
        armor_dude.always_animate = True
        armor_dude.animation_speed = 4

        # Place the weapon merchant
        weapon_dude = WeaponMerchant('dude_map')
        self.place_entity( weapon_dude, (12,6) )
        weapon_dude.face(WEST)
        weapon_dude.always_animate = True
        weapon_dude.animation_speed = 5

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
        
        if choice == 0:
            dialog.message("No! Stopping is not an option!")
        elif choice == 1:
            dialog.message("Good, I appreciate your patience.")
        elif choice == 2:
            dialog.message("Well, hurry and make up your mind!")
        elif choice == 3:
            dialog.message("Ummm.. you're supposed to know that.")
    
    def random_fight(self):
        monster = combat.gallery.generate_monster(1)
        combat.Combat(core.game.save_data.hero, monster, core.screen)
