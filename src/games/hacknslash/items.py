from characters import Weapon
from characters import Armor

weapon_stats = {
    "Bare Hands":      (0, '1d1'),  # 1  - 1
    "Dagger":          (1, '1d5'),  # 1  - 5
    "Stiletto":        (2, '2d5'),  # 2  - 10
    "Mace":            (3, '3d5'),  # 3  - 15
    "Rapier":          (4, '5d4'),  # 5  - 20
    "Longsword":       (5, '10d3'), # 10 - 30
    "Razor Axe":       (6, '15d3'), # 15 - 45
    "Chainsaw":        (7, '25d3'), # 25 - 75
    "Poison Dart Gun": (8, '50d3'), # 50 - 150
    "Phasor":          (9, '100d2') # 100 - 200
}
armor_stats = {
    "Nothing":         0,
    "Cloth":           1,
    "Tough Cloak":     2,
    "Leather Armor":   3,
    "Buckler":         4,
    "Studded Leather": 5,
    "Chainmail":       6,
    "Plate":           7,
    "Diamond Armor":   8,
    "Angelic Aura":    9
}

def armor(name):
    global armor_stats
    a = Armor()
    stat = armor_stats[name]
    a.value = stat
    a.ac_modifier = stat
    a.name = name
    return a

def weapon(name):
    global weapon_stats
    w = Weapon()
    stats = weapon_stats[name]
    w.value = stats[0]
    w.damage = stats[1]
    w.name = name
    return w
