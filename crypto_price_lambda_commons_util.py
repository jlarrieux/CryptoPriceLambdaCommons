#  Copyright 2020 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import json
from enum import Enum, auto
from typing import Tuple
from my_rolling_list import MyRollingList
import indicator_util
from six.moves import urllib
import ssl

my_url = "https://crypto.jlarrieux.com/metric/data?asset={}"


class MovingAverageType(Enum):
    TEN = 10
    TWELVE = 12
    FIFTEEN = 15
    FIFTY = 50
    TWO_HUNDRED = 200


def format_number(value: float, dec=2) -> str:
    formatting_string = "{:,." + f'{dec}' + "f}"
    print(f"value: {value}")
    return formatting_string.format(float(value))


def get_whole_number_count(value: [float, int]) -> int:
    string_value = str(value)
    if "." in string_value:
        left, right = string_value.split(".")
        return len(left)
    else:
        return len(string_value)


def format_money_to_string(value: float) -> str:
    whole_number_count = get_whole_number_count(value)
    my_value = float(value)
    suffix = ""
    if whole_number_count > 6:
        rounded_value = round(my_value)
        str_value = str(rounded_value)
        index = whole_number_count - 6
        suffix = "M"
        if whole_number_count > 9:
            index = whole_number_count - 9
            suffix = "B"
        if whole_number_count > 12:
            index = whole_number_count - 12
            suffix = "T"
        my_value = float(str_value[:index] + "." + str_value[index:])
    return f"${format_number(my_value)}{suffix}"


def get_percent_delta(current_price: float, last_price: float) -> float:
    f_last_price = float(last_price)
    f_current_price = float(current_price)
    delta = (f_current_price - f_last_price) * 100 / f_last_price
    return delta


def get_current_metrics(asset: str) -> Tuple[float, float, float]:
    context = ssl._create_unverified_context()
    value = json.loads(urllib.request.urlopen(my_url.format(asset), context=context).read().decode())

    usd_price = value["usd_price"]
    usd_volume = value["volume_last_24_hours"]
    usd_marketcap = value["current_marketcap_usd"]
    return float(usd_price), float(usd_volume), float(usd_marketcap)


def get_average(number: int, my_rolling_average: MyRollingList) -> [int, float]:
    if number > my_rolling_average.size():
        return -1
    return indicator_util.calculate_simple_moving_average(my_rolling_average.get_most_recents(number))


def get_moving_average_string(ma_type: MovingAverageType) -> str:
    return f"{str(ma_type.value)} day"


if __name__ == '__main__':
    # print(get_current_metrics("eth"))
    print(MovingAverageType.TWELVE.value)
