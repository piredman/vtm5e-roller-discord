from dice_pool.dice_pool import DicePool, DicePoolState
from die.die import DieType

import common.colours as Colours
import common.emojis as Emojis


class DicePoolMessage(object):

    def __init__(self, _dice_pool: DicePool):
        self.dice_pool = _dice_pool

    def getMessageColour(self):
        if (self.dice_pool.state == DicePoolState.BEASTIAL or self.dice_pool.state == DicePoolState.FAILURE):
            return Colours.RED
        if (self.dice_pool.state == DicePoolState.CRITICAL or self.dice_pool.state == DicePoolState.MESSY):
            return Colours.PURPLE
        return Colours.GREEN

    def getRegularDiceAsText(self):
        result = []
        for die in self.dice_pool.results:
            if die.die_type == DieType.REGULAR:
                die_text = f'~~{die.die_value}~~' if die.die_value < 6 else f'{die.die_value}'
                result.append(die_text)

        return ','.join(result)

    def getHungerDiceAsText(self):
        result = []
        for die in self.dice_pool.results:
            if die.die_type == DieType.HUNGER:
                die_text = f'~~{die.die_value}~~' if die.die_value < 6 else f'{die.die_value}'
                result.append(die_text)

        return ','.join(result)

    def getDiceAsEmotes(self, getEmoji):
        regularEmotes = []
        hungerEmotes = []
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
                hungerEmotes.append(str(die_emote))
            else:
                if die.die_value >= 1 and die.die_value <= 5:
                    die_emote = getEmoji(Emojis.REGULAR_FAILURE)
                elif die.die_value >= 6 and die.die_value <= 9:
                    die_emote = getEmoji(Emojis.REGULAR_SUCCESS)
                elif die.die_value == 10:
                    die_emote = getEmoji(Emojis.REGULAR_CRITICAL)
                regularEmotes.append(str(die_emote))

        emotes = regularEmotes + hungerEmotes
        return ''.join(emotes)

    def formatMessage(self, getEmoji):
        return {
            'title': f'{self.dice_pool.Successes()} successes',
            'dice_emojis': self.getDiceAsEmotes(getEmoji),
            'regular_dice_text': self.getRegularDiceAsText(),
            'hunger_dice_text': self.getHungerDiceAsText(),
            'state': self.dice_pool.state.name,
            'colour': self.getMessageColour()
        }
