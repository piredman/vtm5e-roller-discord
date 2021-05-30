from dice_pool.dice_pool import DicePool
from dice_pool.dice_pool_message import DicePoolMessage
from command.command_result import CommandResult, CommandResultState


class WillCommand(object):

    MAX_REROLL = 3

    def __init__(self, fn_getEmoji):
        self._fn_getEmoji = fn_getEmoji

    def roll(self, hunger_dice, regular_dice):
        dice_pool = DicePool()
        dice_pool.reroll(hunger_dice, regular_dice,
                         max_reroll_size=self.MAX_REROLL)

        dice_pool_message = DicePoolMessage(dice_pool)
        message = dice_pool_message.formatMessage(self._fn_getEmoji)
        return CommandResult(CommandResultState.SUCCESS, message)
