import combat
from combat import Monster

def register_monsters():
    print "Registering monsters"
    combat.gallery.add_monster( range(1,2), Snotling ) 
    combat.gallery.add_monster( range(1,3), LargeSlug ) 
    combat.gallery.add_monster( range(2,4), Jellyfish ) 
    combat.gallery.add_monster( range(3,5), SilverJelly ) 
    combat.gallery.add_monster( range(4,7), Kobold ) 
    combat.gallery.add_monster( range(6,10), TeenageNinja ) 
    combat.gallery.add_monster( range(9,13), Snakeling ) 
    combat.gallery.add_monster( range(12,16), Guardsman ) 
    combat.gallery.add_monster( range(15,20), DarkApprentice ) 
    combat.gallery.add_monster( range(18,20), Henchman ) 
    combat.gallery.add_monster( range(99,99), Minotaur ) 
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

class Jellyfish(Monster):
    def __init__(self):
        self.name = "Jelly Fish"
        self.max_hp = 15
        self.attack_damage = '2d4'
        self.thaco = 15
        self.ac = 10
        self.agility = 8
        self.exp_value = 4
        self.gold = '1d6'
    def damage_text(self, damage):
        return 'You are enveloped in stinging tentacles, for %d points of damage' % damage

class SilverJelly(Jellyfish):
    def __init__(self):
        self.name = "Silver Jelly"
        self.max_hp = 25
        self.attack_damage = '2d6'
        self.thaco = 15
        self.ac = 10
        self.agility = 8
        self.exp_value = 6
        self.gold = '1d6'

class Kobold(Monster):
    def __init__(self):
        self.name = "Kobold"
        self.max_hp = 10
        self.attack_damage = '4d4'
        self.thaco = 12
        self.ac = 12
        self.agility = 14
        self.exp_value = 10
        self.gold = '3d6'
    def damage_text(self, damage):
        return 'It slashes with a vicious dagger, for %d points of damage!' % damage

class TeenageNinja(Monster):
    def __init__(self):
        self.name = "Teenage Ninja Kobold"
        self.max_hp = 10
        self.attack_damage = '4d6'
        self.thaco = 10
        self.ac = 15
        self.agility = 18
        self.exp_value = 15
        self.gold = '2d6'
    def damage_text(self, damage):
        return 'It uses REAL ULTIMATE NINJA POWER against you for %d points of damage!' % damage
    
class Snakeling(Monster):
    def __init__(self):
        self.name = "Snakeling"
        self.max_hp = 20
        self.attack_damage = '4d4'
        self.thaco = 12
        self.ac = 20
        self.agility = 15
        self.exp_value = 15
        self.gold = '3d6'
    def damage_text(self, damage):
        return 'It lashes out for %d points of damage!' % damage

class Guardsman(Monster):
    def __init__(self):
        self.name = "Guardsman"
        self.max_hp = 22
        self.attack_damage = '4d6'
        self.thaco = 10
        self.ac = 20
        self.agility = 18
        self.exp_value = 20
        self.gold = '5d6'
    def damage_text(self, damage):
        return 'He slashes at you for %d points of damage.' % damage

class DarkApprentice(Monster):
    def __init__(self):
        self.name = "Dark Apprentice"
        self.max_hp = 25
        self.attack_damage = '4d6'
        self.thaco = 6
        self.ac = 25
        self.agility = 20
        self.exp_value = 28
        self.gold = '5d6'
    def damage_text(self, damage):
        return 'He slashes at you for %d points of damage.' % damage

class Henchman(Monster):
    def __init__(self):
        self.name = "Henchman"
        self.max_hp = 32
        self.attack_damage = '8d4'
        self.thaco = 6
        self.ac = 25
        self.agility = 20
        self.exp_value = 35
        self.gold = '10d6'
    def damage_text(self, damage):
        return 'He slashes at you for %d points of damage.' % damage

class Minotaur(Monster):
    def __init__(self):
        self.name = "The evil Minotaur"
        self.max_hp = 75
        self.attack_damage = '10d6'
        self.thaco = 0
        self.ac = 30
        self.agility = 30
        self.exp_value = 250
        self.gold = '20d20'
    def damage_text(self, damage):
        return 'It throws you against the wall for %d points of damage' % damage

register_monsters()
