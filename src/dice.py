import re
from random import Random

rand = Random()

def roll(desc):
    match = re.search('(\d+)[dD](\d+)', desc)
    count = int(match.group(1))
    sides = int(match.group(2))
    result = 0
    for i in range(count):
        result = result + rand.randint(1, sides)
    return result
