import combat, dice
from characters import Monster

def register_monsters():
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

class Enemy(Monster):
  def damage_text(self, damage):
    return "%s for %d points of damage!" % (self.dmesg, damage)
  def get_gold(self):
    return dice.roll(self.gold)
  
class Snotling(Enemy):
    def __init__(self):
        Monster.__init__(self)
        self.name = "Snotling"
        self.max_hp = 6
        self.attack_damage = '1d4'
        self.thaco = 20
        self.ac = 10
        self.agility = 14
        self.exp_value = 2
        self.gold = '1d6'
        self.dmesg = 'The Snotling discharges its nose at you'

class LargeSlug(Enemy):
    def __init__(self):
        Monster.__init__(self)
        self.name = "Giant Slug"
        self.max_hp = 10
        self.attack_damage = '2d3'
        self.thaco = 18
        self.ac = 12
        self.agility = 10
        self.exp_value = 3
        self.gold = '2d4'
        self.dmesg = 'You slip on a puddle of slime'

class Jellyfish(Enemy):
    def __init__(self):
        Monster.__init__(self)
        self.name = "Jelly Fish"
        self.max_hp = 15
        self.attack_damage = '2d4'
        self.thaco = 15
        self.ac = 10
        self.agility = 8
        self.exp_value = 4
        self.gold = '1d6'
        self.dmesg = 'You are enveloped in stinging tentacles,'

class SilverJelly(Jellyfish):
    def __init__(self):
        Jellyfish.__init__(self)
        self.name = "Silver Jelly"
        self.max_hp = 25
        self.attack_damage = '2d6'
        self.exp_value = 6

class Kobold(Enemy):
    def __init__(self):
        Monster.__init__(self)
        self.name = "Kobold"
        self.max_hp = 10
        self.attack_damage = '4d4'
        self.thaco = 12
        self.ac = 12
        self.agility = 14
        self.exp_value = 10
        self.gold = '3d6'
        self.dmesg = 'It slashes with a vicious dagger,'

class TeenageNinja(Enemy):
    def __init__(self):
        Monster.__init__(self)
        self.name = "Teenage Ninja Kobold"
        self.max_hp = 10
        self.attack_damage = '4d6'
        self.thaco = 10
        self.ac = 15
        self.agility = 18
        self.exp_value = 15
        self.gold = '2d6'
        self.dmesg = 'It uses REAL ULTIMATE NINJA POWER against you'
    
class Snakeling(Enemy):
    def __init__(self):
        Monster.__init__(self)
        self.name = "Snakeling"
        self.max_hp = 20
        self.attack_damage = '4d4'
        self.thaco = 12
        self.ac = 20
        self.agility = 15
        self.exp_value = 15
        self.gold = '3d6'
        self.dmesg = 'It lashes out'

class Guardsman(Enemy):
    def __init__(self):
        Monster.__init__(self)
        self.name = "Guardsman"
        self.max_hp = 22
        self.attack_damage = '4d6'
        self.thaco = 10
        self.ac = 20
        self.agility = 18
        self.exp_value = 20
        self.gold = '5d6'
        self.dmesg = 'He slashes at you'

class DarkApprentice(Enemy):
    def __init__(self):
        Monster.__init__(self)
        self.name = "Dark Apprentice"
        self.max_hp = 25
        self.attack_damage = '4d6'
        self.thaco = 6
        self.ac = 25
        self.agility = 20
        self.exp_value = 28
        self.gold = '5d6'
        self.dmesg = 'He slashes at you'

class Henchman(Enemy):
    def __init__(self):
        Monster.__init__(self)
        self.name = "Henchman"
        self.max_hp = 32
        self.attack_damage = '8d4'
        self.thaco = 6
        self.ac = 25
        self.agility = 20
        self.exp_value = 35
        self.gold = '10d6'
        self.dmesg = 'He slashes at you'

class Minotaur(Enemy):
    def __init__(self):
        Monster.__init__(self)
        self.name = "The evil Minotaur"
        self.max_hp = 75
        self.attack_damage = '10d6'
        self.thaco = 0
        self.ac = 30
        self.agility = 30
        self.exp_value = 250
        self.gold = '20d20'
        self.dmesg = 'It throws you against the wall'

register_monsters()
