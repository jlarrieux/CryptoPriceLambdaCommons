
from typing import List


def calculate_simple_moving_average(values: [List[float], int]) -> float:
    if values == -1:
        return -1
    return _get_average(values)


def _get_average(my_list: List[float]) -> float:
    return sum(my_list) / len(my_list)

