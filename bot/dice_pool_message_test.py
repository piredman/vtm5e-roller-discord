import pytest

from dice_pool_message import DicePoolMessage
from dice_pool import DicePool, DicePoolState
from die import Die, DieType

import colours as Colours
import emojis as Emojis


def test_init_dice_pool_message():
    dice_pool = DicePool()
    message = DicePoolMessage(dice_pool)
    assert message.dice_pool is not None


@pytest.mark.parametrize(
    "state,colour",
    [
        pytest.param(DicePoolState.EMPTY, Colours.GREEN),
        pytest.param(DicePoolState.BEASTIAL, Colours.RED),
        pytest.param(DicePoolState.FAILURE, Colours.RED),
        pytest.param(DicePoolState.SUCCESS, Colours.GREEN),
        pytest.param(DicePoolState.CRITICAL, Colours.PURPLE),
        pytest.param(DicePoolState.MESSY, Colours.PURPLE),
    ]
)
def test_get_message_colour(state: DicePoolState, colour):
    dice_pool = DicePool()
    dice_pool.state = state

    message = DicePoolMessage(dice_pool)
    message_colour = message.getMessageColour()

    assert message_colour == colour


@pytest.mark.parametrize(
    "results,expected",
    [
        pytest.param([Die(die_value=10)], '10'),
        pytest.param([Die(die_value=10),
                      Die(die_value=3)], '10,~~3~~'),
        pytest.param([Die(die_value=10),
                      Die(die_value=1),
                      Die(die_value=3)], '10,~~1~~,~~3~~'),
    ]
)
def test_get_dice_as_text(results, expected):
    dice_pool = DicePool()
    dice_pool.results = results

    message = DicePoolMessage(dice_pool)
    result = message.getDiceAsText()
    assert result == expected


@pytest.mark.parametrize(
    "results,expected",
    [
        pytest.param([
            Die(die_value=1, die_type=DieType.HUNGER)],
            Emojis.HUNGER_BEASTIAL),
        pytest.param([
            Die(die_value=2, die_type=DieType.HUNGER)],
            Emojis.HUNGER_FAILURE),
        pytest.param([
            Die(die_value=6, die_type=DieType.HUNGER)],
            Emojis.HUNGER_SUCCESS),
        pytest.param([
            Die(die_value=10, die_type=DieType.HUNGER)],
            Emojis.HUNGER_CRITICAL),
        pytest.param([
            Die(die_value=1, die_type=DieType.REGULAR)],
            Emojis.REGULAR_FAILURE),
        pytest.param([
            Die(die_value=6, die_type=DieType.REGULAR)],
            Emojis.REGULAR_SUCCESS),
        pytest.param([
            Die(die_value=10, die_type=DieType.REGULAR)],
            Emojis.REGULAR_CRITICAL),
        pytest.param([
            Die(die_value=1, die_type=DieType.HUNGER),
            Die(die_value=6, die_type=DieType.REGULAR),
            Die(die_value=10, die_type=DieType.REGULAR)],
            f'{Emojis.HUNGER_BEASTIAL}{Emojis.REGULAR_SUCCESS}{Emojis.REGULAR_CRITICAL}')
    ]
)
def test_get_dice_as_emotes(results, expected):
    dice_pool = DicePool()
    dice_pool.results = results

    message = DicePoolMessage(dice_pool)
    result = message.getDiceAsEmotes(getEmojiMock)
    assert result == expected


def getEmojiMock(emote_name: str):
    return emote_name


@pytest.mark.parametrize(
    "results,expected",
    [
        pytest.param([
            Die(die_value=1, die_type=DieType.HUNGER),
            Die(die_value=6, die_type=DieType.REGULAR),
            Die(die_value=10, die_type=DieType.REGULAR)],
            {
                'title': f'2 successes',
                'dice_text': f'~~1~~,6,10',
                'dice_emojis': f'{Emojis.HUNGER_BEASTIAL}{Emojis.REGULAR_SUCCESS}{Emojis.REGULAR_CRITICAL}',
                'state': DicePoolState.SUCCESS.name,
                'colour': Colours.GREEN
        })
    ]
)
def test_format_message(results, expected):
    dice_pool = DicePool()
    dice_pool.results = results
    dice_pool.state = dice_pool.determineState()

    message = DicePoolMessage(dice_pool)
    result = message.formatMessage(getEmojiMock)
    assert result == expected
