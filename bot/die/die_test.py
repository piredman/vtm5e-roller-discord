import pytest
from die.die import DieType, Die


def test_init_default():
    die = Die()

    assert die.die_type == DieType.REGULAR
    assert die.die_value == 0


@pytest.mark.parametrize(
    "die_type,die_value",
    [
        pytest.param(DieType.REGULAR, 1),
        pytest.param(DieType.HUNGER, 10),
    ]
)
def test_init_empty_dice_pool(die_type: DieType, die_value: int):
    die = Die(die_type, die_value)

    assert die.die_type == die_type
    assert die.die_value == die_value
