import combat
from combat import Monster

def register_monsters():
    combat.gallery.add_monster( range(1,2), Snotling ) 
    combat.gallery.add_monster( range(1,3), LargeSlug ) 

class Snotling(Monster):
    def __init__(self):
        self.name = "Snotling"
        self.max_hp = 6
        self.attack_damage = '1d4'
        self.thaco = 20
        self.ac = 10
        self.agility = 14
        self.exp_value = 2

class LargeSlug(Monster):
    def __init__(self):
        self.name = "Giant Slug"
        self.max_hp = 10
        self.attack_damage = '2d3'
        self.thaco = 18
        self.ac = 12
        self.agility = 10
        self.exp_value = 3

