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

class LightSaber(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.damage = '6d12'
        self.name = 'Light Saber'
        self.value = 100

class Skin(Armor):
    def __init__(self):
        Armor.__init__(self)
        self.rating = 0
        self.name = 'Skin'
        self.value = 0

class ToughShirt(Armor):
    def __init__(self):
        Armor.__init__(self)
        self.rating = 1
        self.name = 'Tough Shirt'
        self.value = 10

class DiamondPlate(Armor):
    def __init__(self):
        Armor.__init__(self)
        self.rating = 100
        self.name = 'Diamond Plate'
        self.value = 50
