import pytest
from dice_pool.dice_pool import DicePool, DicePoolState
from die.die import DieType, Die

from common.utils import clamp


def test_init_empty_dice_pool():
    dicePool = DicePool()
    dicePool.results.count
    assert len(dicePool.results) == 0


@pytest.mark.parametrize(
    "pool_size,hunger_size",
    [
        pytest.param(5, 0),
        pytest.param(5, 1),
        pytest.param(5, 5),
        pytest.param(5, 6),
    ]
)
def test_pool_contains_same_as_rolled(pool_size, hunger_size):
    dicePool = DicePool()
    dicePool.roll(pool_size, hunger_size)
    assert len(dicePool.results) == pool_size
    assert len(dicePool.getHungerDice()) == clamp(0, hunger_size, pool_size)


@pytest.mark.parametrize(
    "pool_size,hunger_size",
    [
        pytest.param(5, 0),
        pytest.param(5, 1),
        pytest.param(5, 5),
    ]
)
def test_pool_dice_between_one_and_ten(pool_size, hunger_size):
    dicePool = DicePool()
    dicePool.roll(pool_size, hunger_size)

    for die in dicePool.results:
        assert die.die_value >= 1 and die.die_value <= 10


def test_empty_hunger_defaults_to_zero():
    pool_size = 5
    dicePool = DicePool()
    dicePool.roll(pool_size, None)
    assert len(dicePool.results) == pool_size
    assert len(dicePool.getHungerDice()) == 0


@pytest.mark.parametrize(
    "hunger,regular",
    [
        pytest.param([1], [1]),
        pytest.param([1, 10], [1]),
        pytest.param([1, 5, 6, 9, 10], [1]),
        pytest.param([1, 2, 5, 6, 9, 10], [1]),
    ]
)
def test_hunger_dice_never_reroll(hunger, regular):
    dicePool = DicePool()
    dicePool.reroll(hunger, regular)
    assert len(hunger+regular) == len(dicePool.results)
    assert len(dicePool.getHungerDice()) == len(hunger)
    actual = list(map(lambda die: die.die_value, dicePool.getHungerDice()))
    assert hunger == actual


@pytest.mark.parametrize(
    "hunger,regular",
    [
        pytest.param([1], [2]),
        pytest.param([1], [1, 10]),
        pytest.param([1], [1, 5, 6, 9, 10]),
        pytest.param([1], [1, 2, 5, 6, 9, 10]),
    ]
)
def test_only_failed_regular_dice_reroll(hunger, regular):
    dicePool = DicePool()
    dicePool.reroll(hunger, regular)

    assert len(hunger+regular) == len(dicePool.results)
    assert len(dicePool.getRegularDice()) == len(regular)

    index = 0
    actual = list(map(lambda die: die.die_value, dicePool.getRegularDice()))
    while index < len(regular):
        input_die = regular[index]
        actual_die = actual[index]
        if input_die > 5:
            assert input_die == actual_die
        index += 1


@pytest.mark.parametrize(
    "hunger,regular,max,expected",
    [
        pytest.param([1], [1], 3, 1),
        pytest.param([1], [1, 2], 3, 2),
        pytest.param([1], [1, 2, 3], 3, 3),
        pytest.param([1], [1, 10, 3], 3, 2),
        pytest.param([1], [1, 10, 3, 5, 9], 3, 3),
    ]
)
def test_max_reroll_limit(hunger, regular, max, expected):
    dicePool = DicePool()
    reroll_count = dicePool.reroll(hunger, regular, max)

    assert len(hunger+regular) == len(dicePool.results)
    assert len(dicePool.getRegularDice()) == len(regular)
    assert reroll_count == expected


def test_get_failure_dice():
    dicePool = DicePool()
    for value in range(1, 10+1):
        dicePool.results.append(Die(DieType.REGULAR, value))

    actual = dicePool.getFailureDice()
    assert len(actual) == 5


def test_get_beastial_dice():
    dicePool = DicePool()
    for value in range(1, 10+1):
        dicePool.results.append(Die(DieType.HUNGER, value))

    actual = dicePool.getBeastialDice()
    assert len(actual) == 1


def test_get_success_dice():
    dicePool = DicePool()
    for value in range(1, 10+1):
        dicePool.results.append(Die(DieType.REGULAR, value))

    actual = dicePool.getSuccessDice()
    assert len(actual) == 5


def test_get_critical_dice():
    dicePool = DicePool()
    dicePool.results.append(Die(DieType.REGULAR, 5))
    dicePool.results.append(Die(DieType.REGULAR, 10))
    dicePool.results.append(Die(DieType.REGULAR, 10))

    actual = dicePool.getCriticalDice()
    assert len(actual) == 2


def test_regular_successes():
    dicePool = DicePool()
    for value in range(1, 10+1):
        dicePool.results.append(Die(DieType.REGULAR, value))

    successes = dicePool.Successes()
    assert successes == 5


@pytest.mark.parametrize(
    "results,expected_successes",
    [
        pytest.param([Die(die_value=10)], 1),
        pytest.param([Die(die_value=10), Die(die_value=10)], 4),
        pytest.param([Die(die_value=10), Die(die_value=10),
                      Die(die_value=10)], 5),
        pytest.param([Die(die_value=10), Die(die_value=10),
                      Die(die_value=10), Die(die_value=10)], 8)
    ]
)
def test_critical_successes(results, expected_successes):
    dicePool = DicePool()
    dicePool.results = results

    successes = dicePool.Successes()
    assert successes == expected_successes


@pytest.mark.parametrize(
    "results,state",
    [
        pytest.param([Die(DieType.HUNGER, 1)], DicePoolState.BEASTIAL),
        pytest.param([
            Die(DieType.REGULAR, 1),
            Die(DieType.HUNGER, 1)],
            DicePoolState.BEASTIAL),
        pytest.param([Die(DieType.REGULAR, 1)], DicePoolState.FAILURE),
        pytest.param([Die(DieType.REGULAR, 5)], DicePoolState.FAILURE),
        pytest.param([Die(DieType.REGULAR, 6)], DicePoolState.SUCCESS),
        pytest.param([Die(DieType.REGULAR, 10)], DicePoolState.SUCCESS),
        pytest.param([
            Die(DieType.REGULAR, 10),
            Die(DieType.REGULAR, 10)],
            DicePoolState.CRITICAL),
        pytest.param([
            Die(DieType.HUNGER, 10),
            Die(DieType.REGULAR, 10)],
            DicePoolState.MESSY),
    ]
)
def test_determine_state(results, state):
    dicePool = DicePool()
    dicePool.results = results

    assert dicePool.determineState() == state
