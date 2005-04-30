import combat
from combat import Monster
from random import Random

rnd = Random()

def monster_factory(level):
    """Want to generate a monster around the level you are on.
       Can get lower or higher level monsters some of the time"""
    prob = rnd.randint(1,100)
    if   prob > 85:
        level = level - 5 + rnd.randint(0,10)
    elif prob > 70:
        level = level - 3 + rnd.randint(0,6)
    elif prob > 60:
        level = level - 2 + rnd.randint(0,4)
    elif prob > 50:
        level = level - 1 + rnd.randint(0,2)
    if level > 20: level = 20
    if level < 1: level = 1
    m = Monster()
    m.name = "Snotling"
    m.max_hp = __roll_die(2*level,10)
    m.attack_damage = "%id%i" % (rnd.randint(1,level),rnd.randint(1,5))
    m.thaco = 22 - (level * 2)
    m.ac = level
    m.agility = 20 - rnd(2,level)
    m.exp_value = int(3 * level * level / 4)
    return m

def __roll_die(n, m):
    """__roll_die(n,m) => die roll of nDm"""
    roll = 0
    for r in range(n):
        roll = roll + rnd.randint(1,m)
    return roll
