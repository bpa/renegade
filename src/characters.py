import dialog
import dice
import util
from observing import Observable
from conf import *
from items import Weapon, Armor

class Character(object):
    def __init__(self):
      self.level = 1
      self.hp = 10
      self.max_hp = 10
      self.strength = 10
      self.agility = 10
      self.vitality = 10
      self.weapon = Weapon('None','1d1',0)
      self.armor = Armor('None',0,0)
      self.gold = 0
      self.recalculate()

    def equip_weapon(self, weapon):
        if self.weapon != None:
            self.inventory.append(self.weapon)
        self.weapon = weapon
        self.recalculate()

    def equip_armor(self, armor):
        if self.armor != None:
            self.inventory.append(self.armor)
        self.armor = armor
        self.recalculate()

    def recalculate(self):
        self.thaco = 30 - self.strength
        self.ac = 20 - self.armor.get_rating() - self.agility
        self.max_hp = 2 * self.vitality

    def damage(self, points):
        self.hp = self.hp - points
        return self.hp <= 0

    def do_damage(self):
        return dice.roll(self.attack_damage)

    def get_gold(self):
        return self.gold

    def get_level(self):
        return self.level

    def get_thaco(self):
        return self.thaco
    
    def get_max_hp(self):
        return self.max_hp

    def get_hp(self):
        return self.hp

    def get_ac(self):
        return self.ac

    def get_exp(self):
        return self.exp

    def get_initiative(self):
        return dice.roll('1d20') + self.agility

class Monster(Character):
    def __init__(self):
        Character.__init__(self)
        self.gold = dice.roll("%iD10"%self.level)
        self.exp_value = dice.roll("%iD10"%self.level)

    def prepare(self):
        self.current_hp = self.max_hp

    def get_name(self):
        return self.name

    def get_exp_value(self):
        return self.exp_value

    def damage_text(self, damage):
        return 'The %s hits you for %d points of damage!' % \
            (self.get_name(), damage)

class Hero(Observable, Character):
    def __init__(self):
        Character.__init__(self)
        self.inventory = []
        self.exp = 0
        self.exp_to_next_level = 10
        self.recalculate()
        self.heal()

    def __getstate__(self):
        dict = self.__dict__.copy()
        if dict.has_key('_Observable__observers'):
          dict.pop('_Observable__observers')
        return dict

    def get_inventory(self):
        return self.inventory

    def heal(self):
        self.hp = self.max_hp

    def add_gold(self, amount):
        self.gold = self.gold + amount

    def regenerate(self):
        #Being observable, we don't want to change variables
        #just to change them back
        if self.hp == self.max_hp: return
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
            self.strength = self.strength + 3
            new_val = self.strength
            message = 'strength'
        elif attribute==2:
            self.agility = self.agility + 3
            new_val = self.agility
            message = 'agility'
        elif attribute==3:
            self.vitality = self.vitality + 3
            new_val = self.vitality
            message = 'vitality'
        self.exp_to_next_level = self.exp_to_next_level * 1.5
        text = 'You have advanced to level %d.  Your %s has increased to %d.'
        dialog.message(text % (self.level, message, new_val))
        self.recalculate()
