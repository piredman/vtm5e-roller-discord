import random
from enum import Enum


class DieType(Enum):
    REGULAR = 1
    HUNGER = 2


class Die(object):

    def __init__(self, die_type=DieType.REGULAR, die_value=0):
        self.die_type = die_type
        self.die_value = die_value
