from characters import Weapon
from characters import Armor

class Hands(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.damage = '1d1'
        self.name = 'Hands'
        self.value = 0

class Dagger(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.damage = '1d4'
        self.name = 'Dagger'
        self.value = 10

class Dirk(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.damage = '2d3'
        self.name = 'Dirk'
        self.value = 50

class Skin(Armor):
    def __init__(self):
        Armor.__init__(self)
        self.ac_modifier = 0
        self.name = 'Skin'
        self.value = 0

class ToughShirt(Armor):
    def __init__(self):
        Armor.__init__(self)
        self.ac_modifier = -1
        self.name = 'Tough Shirt'
        self.value = 10
