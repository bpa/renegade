import dialog
import dice
import util
from conf import *
from map import MapEntity

class Hero(object):
    def __init__(self, screen):
        self.screen = screen
        self.inventory = []
        self.strength = 10
        self.agility = 10
        self.vitality = 10
        self.weapon = Weapon()
        self.armor = Armor()
        self.exp = 0
        self.level = 1
        self.exp_to_next_level = 10
        self.gold = 0
        self.recalculate()
        self.heal()

    def inventory(self):
        return self.inventory

    def equip_weapon(self, weapon):
        self.weapon = weapon
        self.recalculate()

    def equip_armor(self, armor):
        self.armor = armor
        self.recalculate()

    def recalculate(self):
        self.thaco = 30 - self.strength
        self.ac = 20 - self.armor.get_rating() - self.agility
        self.max_hp = 2 * self.vitality

    def heal(self):
        self.hp = self.max_hp

    def get_thaco(self):
        return self.thaco
    
    def get_ac(self):
        return self.ac

    def get_max_hp(self):
        return self.max_hp

    def get_hp(self):
        return self.hp

    def get_exp(self):
        return self.exp

    def get_level(self):
        return self.level

    def get_initiative(self):
        return dice.roll('1d20') + self.agility

    def damage(self, points):
        self.hp = self.hp - points
        return self.hp <= 0

    def regenerate(self):
        self.hp = self.hp + int(0.05 * self.max_hp)
        if self.hp > self.max_hp: self.hp = self.max_hp

    def gain_exp(self, exp):
        self.exp = self.exp + exp
       
    def check_level(self):
        while self.exp >= self.exp_to_next_level:
            self.gain_level()

    def gain_level(self):
        self.level = self.level + 1
        attribute = dice.roll('1d3')
        if attribute==1:
            self.strength = self.strength + 1
            new_val = self.strength
            message = 'strength'
        elif attribute==2:
            self.agility = self.agility + 1
            new_val = self.agility
            message = 'agility'
        elif attribute==3:
            self.vitality = self.vitality + 1
            new_val = self.vitality
            message = 'vitality'
        self.exp_to_next_level = self.exp_to_next_level * 2
        text = 'You have advanced to level %d.  Your %s has increased to %d.'
        dialog.message(text % (self.level, message, new_val))
        self.recalculate()

class Weapon(object):
    def __init__(self):
        self.damage = '1d1'

    def get_damage(self):
        return dice.roll(self.damage)
    
    def get_name(self):
        return self.name

class Armor(object):
    def __init__(self):
        self.rating = 0

    def get_rating(self):
        return self.rating

    def get_name(self):
        return self.name

class Character(MapEntity):
    pass
