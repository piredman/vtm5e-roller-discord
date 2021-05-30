import random
from enum import Enum
from die.die import DieType, Die


class DicePoolState(Enum):
    EMPTY = 0
    BEASTIAL = 1
    FAILURE = 2
    SUCCESS = 3
    CRITICAL = 4
    MESSY = 5


class DicePool(object):

    def __init__(self):
        self.state = DicePoolState.EMPTY
        self.results = []

    def roll(self, pool_size: int, hunger_size: int):
        if (hunger_size == None):
            hunger_size = 0

        pool_results = []
        for index in range(pool_size):
            dieType = DieType.HUNGER if index + 1 <= hunger_size else DieType.REGULAR
            value = random.choice(range(1, 10 + 1))
            die = Die(dieType, value)
            pool_results.append(die)

        self.results = pool_results
        self.state = self.determineState()

    def reroll(self, hunger_dice, regular_dice, max_reroll_size=3) -> int:
        self.results.clear()

        for die in hunger_dice:
            self.results.append(Die(die_type=DieType.HUNGER, die_value=die))

        reroll_count = 0
        for die in regular_dice:
            if reroll_count >= max_reroll_size:
                self.results.append(
                    Die(die_type=DieType.REGULAR, die_value=die))
                continue

            if die > 5:
                self.results.append(
                    Die(die_type=DieType.REGULAR, die_value=die))
                continue

            value = random.choice(range(1, 10 + 1))
            die = Die(DieType.REGULAR, value)
            self.results.append(die)
            reroll_count += 1

        self.state = self.determineState()
        return reroll_count

    def getHungerDice(self):
        return list(filter(lambda die: (die.die_type == DieType.HUNGER), self.results))

    def getRegularDice(self):
        return list(filter(lambda die: (die.die_type == DieType.REGULAR), self.results))

    def getFailureDice(self):
        return list(filter(lambda die: (die.die_value <= 5), self.results))

    def getBeastialDice(self):
        return list(filter(lambda die: (die.die_type == DieType.HUNGER and die.die_value == 1), self.getFailureDice()))

    def getSuccessDice(self):
        return list(filter(lambda die: (die.die_value >= 6), self.results))

    def getCriticalDice(self):
        return list(filter(lambda die: (die.die_value == 10), self.getSuccessDice()))

    def getMessyCriticalDice(self):
        return list(filter(lambda die: (die.die_type == DieType.HUNGER), self.getCriticalDice()))

    def calc_criticals(self):
        return int(len(self.getCriticalDice()) / 2)

    def Successes(self):
        success_dice = self.getSuccessDice()
        multiplier = self.calc_criticals() * 2
        return len(success_dice) + multiplier

    def determineState(self):
        num_beastials = len(self.getBeastialDice())
        num_successes = len(self.getSuccessDice())
        num_criticals = self.calc_criticals()
        num_messy = len(self.getMessyCriticalDice())

        if (num_successes == 0 and num_beastials > 0):
            return DicePoolState.BEASTIAL

        if (num_successes == 0):
            return DicePoolState.FAILURE

        if (num_criticals > 0 and num_messy > 0):
            return DicePoolState.MESSY

        if (num_criticals > 0):
            return DicePoolState.CRITICAL

        return DicePoolState.SUCCESS
