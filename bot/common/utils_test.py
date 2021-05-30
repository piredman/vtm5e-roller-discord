import pytest
from common.utils import clamp, string_to_numbers


@pytest.mark.parametrize(
    "min,value,max",
    [
        pytest.param(0, 0, 10),
        pytest.param(0, 5, 10),
        pytest.param(0, 10, 10),
        pytest.param(0, 15, 10),
    ]
)
def test_init_empty_dice_pool(min, value, max):
    actual = clamp(min, value, max)
    assert actual >= min and actual <= max


@pytest.mark.parametrize(
    "input, expected",
    [
        pytest.param("1,2,3,4,5", [1, 2, 3, 4, 5]),
        pytest.param("~1~,~~2~~,a3,@4,-5", [1, 2, 3, 4, 5])
    ]
)
def test_roll_string_to_numbers(input, expected):
    actual = string_to_numbers(input)
    assert actual == expected
