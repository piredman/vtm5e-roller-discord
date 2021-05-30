import pytest
from command.command_result import CommandResultState
from command.will.will_command import WillCommand
from dice_pool.dice_pool import DicePoolState


def getEmojiMock(emote_name: str):
    return emote_name


def test_init_will_command():
    command = WillCommand(getEmojiMock)
    assert command is not None


@pytest.mark.parametrize(
    "hunger,regular",
    [
        pytest.param([1], [1]),
        pytest.param([1, 10], [1, 10]),
        pytest.param([1, 5, 10], [1, 5, 10]),
    ]
)
def test_valid_roll(hunger, regular):
    command = WillCommand(getEmojiMock)
    result = command.roll(hunger, regular)
    assert result.state == CommandResultState.SUCCESS

    message = result.payload
    assert message['title'] is not None
    assert message['dice_emojis'] is not None
    assert message['regular_dice_text'] is not None
    assert message['hunger_dice_text'] is not None
    assert message['state'] != DicePoolState.EMPTY.name
    assert message['colour'] is not None
