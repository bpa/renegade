from map import *
from characters import Character
import dialog, NPC
import core, combat

class ArmorMerchant(NPC.Merchant):
    def __init__(self, sprite_name=None):
        NPC.Merchant.__init__(self, sprite_name)
        self.set_intro("Welcome to Ye Olde Armor Shoppe!  How may I be of service?")
        self.set_item_list(*map(lambda i: "A%02i"%i,range(2,11)))

class WeaponMerchant(NPC.Merchant):
    def __init__(self, sprite_name=None):
        NPC.Merchant.__init__(self, sprite_name)
        self.set_intro("Warrior, I have arms to sell.  Have you gold to buy?")
        self.set_item_list(*map(lambda i: "W%02i"%i,range(2,12)))

class AdventureTown(MapBase):
    def __init__(self):
        MapBase.__init__(self,20,15)
        self.set_regen_rate(5)
        self.get_tiles_from_ascii(self.__ascii_art(),{
            '*': ('Castle_Set2',(5,0)),
            ' ': ('DungeonSet',(1,0)),
            '-': ('Castle_Set2',(4,4)),
            '^': ('water',),
            'walkable': ' -'})

        # Place armor and weapons merchants
        armor_dude = ArmorMerchant()
        armor_dude.init('m03', 1, 1, -1)
        self.place_entity( armor_dude, (3,2) )
        armor_dude.face(SOUTH)
        armor_dude.always_animate = True
        armor_dude.animation_speed = 40
        weapon_dude = WeaponMerchant()
        weapon_dude.init('m26', 0, 0, -1)
        self.place_entity( weapon_dude, (7,6) )
        weapon_dude.face(SOUTH)
        weapon_dude.always_animate = True
        weapon_dude.animation_speed = 37

        # Put a wise dude here, to talk to.
        sprite = MapEntity()
        sprite.init('m05', 2, 2, -1)
        self.place_entity( sprite, (9,1) )
        sprite.face(SOUTH)
        sprite.always_animate = True
        sprite.animation_speed = 18
        sprite.activate = self.walk_in_front_of_dude

        # Exit points
        self.add_entry_listener(0,10, self.leave_town)
        self.add_entry_listener(19,10, self.leave_town)

        # Random townsfolk
        tp = NPC.Townsperson()
        tp.init('m05', 0, 1, -1)
        self.place_entity(tp, (7,7) )
        tp.animation_speed = 5
        tp.set_dialog(( "Hi", "Yeah, what?", "You still here?",
            "Why are you talking to me?",
            "I don't know anything that would help you",
            "ok, you must be bored", "please leave me alone"))

    def walk_in_front_of_dude(self):
        choice = dialog.question(
            "I am the wise dude.  What is it you would like to know?",
            [ "What am I supposed to do here?",
              "How does fighting work?",
              "Any hints on getting started?",
              "This seems too simple, is that it?" ])
        
        if choice == 0:
            dialog.message("You're job is to destroy the evil Minotaur.  " +
                           "He lives in a cave north of town.  You'll find " +
                           "him on the 20th level.  Yeah, its a big cave.  " +
                           "Should be pretty easy to find him though, the " +
                           "levels are mostly just stops between stairs.  " +
                           "No one knows why he'd want to keep digging like " +
                           "that, seems like it would be a pain to go up " +
                           "and down the stairs all the time to mess with us.")
        elif choice == 1:
            dialog.message("Its pretty simple really, you can hack, slash, " +
                           "or stab.  Each method has a different chance of " +
                           "hitting and does a different amount of damage.  " +
                           "Hack is the basic attack.  It is the easiest to " +
                           "hit with, but does the least damage.  Slash is " +
                           "a little harder to hit with, but does more " +
                           "damage.  Stab is the hardest to use, but does " +
                           "the most damage.  Now get out there and fight")
        elif choice == 2:
            dialog.message("Starting out is always the hardest part.  You " +
                           "have nothing but a little money.  At least its " +
                           "not zilch.  There are two basic strategies for " +
                           "you.  Either save the money for the hospital, " +
                           "or go get yourself armor or a weapon and get " +
                           "fighting.  If you buy armor, you have a better " +
                           "chance of not getting hit.  The weapon will " +
                           "allow you to hit more often and do more damage.  " +
                           "I'd go with the weapon, personally, since the " +
                           "early fights will be shorter and you won't have " +
                           "as many opportunities to get hurt.")
            dialog.message("At the very beginning, you'll want to stick to " +
                           "the area right outside of town.  Then come back " +
                           "to town after each fight.  Heal and save, that " +
                           "sort of thing.  After you have a couple of " +
                           "levels under your belt, and some decent " +
                           "equiptment, you can head to the cave.  Fight on " +
                           "each level until you are comfortable with the " +
                           "risk.  That doesn't mean hang around levels " +
                           "with no challenge!  You won't get anywhere here " +
                           "unless you take risks.  The deeper you go into " +
                           "the cave, the more money and experience you get.")
        elif choice == 3:
            dialog.message("Ummm... That really is about it.  Oh yeah, if " +
                           "you do manage to get rid of the evil Minotaur, " +
                           "we'll make you mayor and all the girls will " +
                           "want you.  As mayor, you'll also have a nice " +
                           "retirement plan and good benefits.  The pay " +
                           "isn't the greatest, but you'll get to live in " +
                           "the town hall and have servants and food " +
                           "provided for you.  All in all, not a bad gig.")
    
    def leave_town(self):
        core.game.teleport((10,5), 'overworld.Overworld')

    def random_fight(self):
        monster = combat.gallery.generate_monster(1)
        hero = core.game.save_data.hero
        fight = combat.Combat(hero, monster)
        result = fight.run()
        if result == 'lose':
            self.end_game()

    def __ascii_art(self):
        return (
        "********************",
        "*                  *",
        "*                  *",
        "*    ----------    *",
        "*    ----------    *",
        "*    ----------    *",
        "*    ----------    *",
        "*    ----------    *",
        "*                  *",
        "*                  *",
        "                    ",
        "^^^^^^^^^^^^^^^^^^^^",
        "^^^^^^^^^^^^^^^^^^^^",
        "^^^^^^^^^^^^^^^^^^^^",
        "^^^^^^^^^^^^^^^^^^^^")
