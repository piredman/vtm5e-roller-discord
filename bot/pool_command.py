from dice_pool import DicePool
from dice_pool_message import DicePoolMessage
from command_result import CommandResult, CommandResultState


class PoolCommand(object):

    MIN_DICE_POOL_SIZE = 1
    MAX_DICE_POOL_SIZE = 30

    def __init__(self, fn_getEmoji):
        self._fn_getEmoji = fn_getEmoji

    def roll(self, number_of_dice: int, number_of_hunger: int):
        result = self.validate(number_of_dice, number_of_hunger)
        if (result.state == CommandResultState.ERROR):
            return result

        dice_pool = DicePool()
        dice_pool.roll(number_of_dice, number_of_hunger)
        dice_pool_message = DicePoolMessage(dice_pool)
        message = dice_pool_message.formatMessage(self._fn_getEmoji)
        return CommandResult(CommandResultState.SUCCESS, message)

    def validate(self, number_of_dice: int, number_of_hunger: int):
        if (number_of_dice < self.MIN_DICE_POOL_SIZE or number_of_dice > self.MAX_DICE_POOL_SIZE):
            return CommandResult(CommandResultState.ERROR, self.get_invalid_dice_message())

        return CommandResult(CommandResultState.SUCCESS, None)

    def get_invalid_dice_message(self):
        return f'Dice pools must be between {self.MIN_DICE_POOL_SIZE} and {self.MAX_DICE_POOL_SIZE}'
