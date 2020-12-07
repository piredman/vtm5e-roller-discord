import pytest
from utils import clamp


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
