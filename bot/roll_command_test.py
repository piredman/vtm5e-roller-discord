import pytest

from roll_command import RollCommand
from command_result import CommandResultState


def getEmojiMock(emote_name: str):
    return emote_name


def test_init_dice_pool_message():
    command = RollCommand(getEmojiMock)
    assert command is not None


@pytest.mark.parametrize(
    "dice,hunger",
    [
        pytest.param(1, 1),
        pytest.param(10, 3),
        pytest.param(30, 3),
    ]
)
def test_valid_roll(dice, hunger):
    command = RollCommand(getEmojiMock)
    result = command.roll(dice, hunger)
    assert result.state == CommandResultState.SUCCESS

    message = result.payload
    assert message['title'] is not None
    assert message['dice_text'] is not None
    assert message['dice_emojis'] is not None
    assert message['state'] is not None
    assert message['colour'] is not None


@pytest.mark.parametrize(
    "dice,hunger",
    [
        pytest.param(-1, 3),
        pytest.param(0, 3),
        pytest.param(31, 3),
    ]
)
def test_invalid_roll(dice, hunger):
    command = RollCommand(getEmojiMock)
    result = command.roll(dice, hunger)
    assert result.state == CommandResultState.ERROR

    message = result.payload
    assert type(message) is str


def test_optional_hunger_roll():
    command = RollCommand(getEmojiMock)
    result = command.roll(5, None)
    assert result.state == CommandResultState.SUCCESS

    message = result.payload
    assert message['title'] is not None
    assert message['dice_text'] is not None
    assert message['dice_emojis'] is not None
    assert message['state'] is not None
    assert message['colour'] is not None
