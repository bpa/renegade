import random

import dialog
import dice

rand = random.Random()

class Combat(object):
    def __init__(self, hero, monster):
        self.hero = hero
        self.monster = monster

    def run(self):
        monster = self.monster
        hero = self.hero
        dialog.message('You have been attacked by a %s!' % monster.get_name())
        hero_initiative = hero.get_initiative()
        monster_initiative = monster.get_initiative()
        while True:
            if hero_initiative > monster_initiative:
                monster_initiative = monster_initiative + monster.get_initiative()
                action = dialog.question('What is your bidding?', \
                                ( 'Hack', 'Slash', 'Stab' ))
                if action == 0:
                    thaco = hero.get_thaco() - 2
                    mult = 1.0
                elif action == 1:
                    thaco = hero.get_thaco()
                    mult = 1.5
                elif action == 2:
                    thaco = hero.get_thaco() + 2
                    mult = 2.0
                if thaco - monster.ac <= dice.roll('1d20'):
                    damage = int(hero.weapon.get_damage() * mult * hero.strength / 10.0)
                    if monster.damage(damage):
                        gold = monster.get_gold()
                        hero.gain_exp(monster.get_exp_value())
                        hero.add_gold(gold)
                        mess = 'You hit the %s for %d points of damage, ' + \
                               'killing it!  You find %d gold.  For valor ' + \
                               'in combat, you receive %d experience points.'
                        mess = mess % (monster.get_name(), damage, gold, monster.get_exp_value())
                        dialog.message(mess)
                        hero.check_level()
                        return 'win'
                    else:
                        dialog.message('You hit the %s for %d points of damage.' % \
                               (monster.get_name(), damage))

                else:
                    dialog.message('You missed!')
            else:
                hero_initiative = hero_initiative + hero.get_initiative()
                if monster.thaco - hero.get_ac() <= dice.roll('1d20'):
                    damage = monster.do_damage()
                    message = monster.damage_text(damage)
                    if hero.damage(damage):
                        dialog.message(message + '  You have died!')
                        return 'lose'
                    else: dialog.message(message)
                else:
                    dialog.message('The %s misses you!' % monster.get_name())

class MonsterGallery(object):
    def __init__(self):
        self.monster_types = {}
        self.monster_names = {}

    def add_monster(self, levels, type):
        instance = type()
        self.monster_names[instance.get_name()] = type
        mt = self.monster_types
        for level in levels:
            if mt.has_key(level):
                mt[level].append(type)
            else:
                mt[level] = [type,]

    def generate_monster(self, monster_level):
        available = self.monster_types[monster_level]
        type = available[ rand.randint(0, len(available)-1) ]
        monster = type()
        monster.prepare()
        return monster

    def get_monster(self, name):
        type = self.monster_names[name]
        monster = type()
        monster.prepare()
        return monster

class Monster(object):
    def __init__(self):
        pass

    def prepare(self):
        self.current_hp = self.max_hp

    def damage(self, damage):
        self.current_hp = self.current_hp - damage
        return self.current_hp <= 0

    def do_damage(self):
        return dice.roll(self.attack_damage)

    def get_name(self):
        return self.name

    def get_exp_value(self):
        return self.exp_value

    def get_gold(self):
        return dice.roll(self.gold)

    def get_initiative(self):
        return dice.roll('1d20') + self.agility

    def damage_text(self, damage):
        return 'The %s hits you for %d points of damage!' % \
            (self.get_name(), damage)

gallery = MonsterGallery()
