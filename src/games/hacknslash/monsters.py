import combat
from combat import Monster

def register_monsters():
    print "Registering monsters"
    combat.gallery.add_monster( range(1,2), Snotling ) 
    combat.gallery.add_monster( range(1,3), LargeSlug ) 
    registered = True

class Snotling(Monster):
    def __init__(self):
        self.name = "Snotling"
        self.max_hp = 6
        self.attack_damage = '1d4'
        self.thaco = 20
        self.ac = 10
        self.agility = 14
        self.exp_value = 2
        self.gold = '1d6'
    def damage_text(self, damage):
        return 'The %s discharges its nose at you for %d points of damage!' % \
            (self.get_name(), damage)

class LargeSlug(Monster):
    def __init__(self):
        self.name = "Giant Slug"
        self.max_hp = 10
        self.attack_damage = '2d3'
        self.thaco = 18
        self.ac = 12
        self.agility = 10
        self.exp_value = 3
        self.gold = '2d4'
    def damage_text(self, damage):
        return 'You slip on a puddle of slime for %d points of damage!' % damage

register_monsters()
