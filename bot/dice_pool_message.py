from dice_pool import DicePool, DicePoolState
from die import DieType
import colours as Colours
import emojis as Emojis


class DicePoolMessage(object):

    def __init__(self, _dice_pool: DicePool):
        self.dice_pool = _dice_pool

    def getMessageColour(self):
        if (self.dice_pool.state == DicePoolState.BEASTIAL or self.dice_pool.state == DicePoolState.FAILURE):
            return Colours.RED
        if (self.dice_pool.state == DicePoolState.CRITICAL or self.dice_pool.state == DicePoolState.MESSY):
            return Colours.PURPLE
        return Colours.GREEN

    def getDiceAsText(self):
        result = []
        for die in self.dice_pool.results:
            die_text = f'~~{die.die_value}~~' if die.die_value < 6 else f'{die.die_value}'
            result.append(die_text)

        return ','.join(result)

    def getDiceAsEmotes(self, getEmoji):
        result = []
        for die in self.dice_pool.results:
            die_emote = ''
            if die.die_type == DieType.HUNGER:
                if die.die_value == 1:
                    die_emote = getEmoji(Emojis.HUNGER_BEASTIAL)
                elif die.die_value >= 2 and die.die_value <= 5:
                    die_emote = getEmoji(Emojis.HUNGER_FAILURE)
                elif die.die_value >= 6 and die.die_value <= 9:
                    die_emote = getEmoji(Emojis.HUNGER_SUCCESS)
                elif die.die_value == 10:
                    die_emote = getEmoji(Emojis.HUNGER_CRITICAL)
            else:
                if die.die_value >= 1 and die.die_value <= 5:
                    die_emote = getEmoji(Emojis.REGULAR_FAILURE)
                elif die.die_value >= 6 and die.die_value <= 9:
                    die_emote = getEmoji(Emojis.REGULAR_SUCCESS)
                elif die.die_value == 10:
                    die_emote = getEmoji(Emojis.REGULAR_CRITICAL)
            result.append(str(die_emote))

        return ''.join(result)

    def formatMessage(self, getEmoji):
        return {
            'title': f'{self.dice_pool.Successes()} successes',
            'dice_text': self.getDiceAsText(),
            'dice_emojis': self.getDiceAsEmotes(getEmoji),
            'state': self.dice_pool.state.name,
            'colour': self.getMessageColour()
        }
