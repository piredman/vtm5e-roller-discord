import re


def clamp(minimum: int, value: int, maximum: int):
    return max(minimum, min(value, maximum))


def string_to_numbers(roll_as_string: str) -> list:
    roll_list = roll_as_string.split(",")

    result = list()
    for roll in roll_list:
        roll_number = int(re.sub("[^0-9]", "", roll))
        result.append(roll_number)

    return result
