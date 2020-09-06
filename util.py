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
from my_rolling_list import  MyRollingList
import indicator_util
from six.moves import urllib

url = "https://data.messari.io/api/v1/assets/eth/metrics?fields=id,symbol,market_data/price_usd," \
      "market_data/real_volume_last_24_hours,market_data/volume_last_24_hours,marketcap/current_marketcap_usd "
my_url = "https://crypto.jlarrieux.com/metric/data?asset={}"


class MovingAverageType(Enum):
    TEN = auto()
    TWELVE = auto()
    FIFTEEN = auto()
    FIFTY = auto()
    TWO_HUNDRED = auto()


def format_number(value: float, dec=2) -> str:
    formating_string = "{:,." + f'{dec}' + "f}"
    return formating_string.format(value)


def get_whole_number_count(value: [float, int]) -> int:
    string_value = str(value)
    if "." in string_value:
        left, right = string_value.split(".")
        return len(left)
    else:
        return len(string_value)


def format_money_to_string(value: float) -> str:
    whole_numer_count = get_whole_number_count(value)
    my_value = value
    suffix = ""
    if whole_numer_count > 6:
        rounded_value = round(my_value)
        str_value = str(rounded_value)
        index = whole_numer_count - 6
        suffix = "M"
        if whole_numer_count > 9:
            index = whole_numer_count - 9
            suffix = "B"
        if whole_numer_count > 12:
            index = whole_numer_count - 12
            suffix = "T"
        my_value = float(str_value[:index] + "." + str_value[index:])
    return f"${format_number(my_value)}{suffix}"


def get_percent_delta(current_price: float, last_price: float) -> float:
    f_last_price = float(last_price)
    f_current_price = float(current_price)
    delta = (f_current_price - f_last_price) * 100 / f_last_price
    return delta


def get_current_metrics(asset: str) -> Tuple[float, float, float]:
    value = json.loads(urllib.request.urlopen(my_url.format(asset)).read().decode())

    usd_price = value["usd_price"]
    usd_volume = value["volume_last_24_hours"]
    usd_marketcap = value["current_marketcap_usd"]
    return usd_price, usd_volume, usd_marketcap


def get_average(number: int, my_rolling_average: MyRollingList) -> [int, float]:
    if number > my_rolling_average.size():
        return -1
    return indicator_util.calculate_simple_moving_average(my_rolling_average.get_most_recents(number))


def get_moving_average_string(ma_type: MovingAverageType) -> str:
    return f"{str(get_moving_average_number(ma_type))} day"


def get_moving_average_number(ma_type: MovingAverageType) -> int:
    num = 0
    if ma_type == MovingAverageType.TEN:
        num = 10
    elif ma_type == MovingAverageType.TWELVE:
        num = 12
    elif ma_type == MovingAverageType.FIFTEEN:
        num = 15
    elif ma_type == MovingAverageType.FIFTY:
        num = 50
    elif ma_type == MovingAverageType.TWO_HUNDRED:
        num = 200
    return num


if __name__ == '__main__':
    print(get_current_metrics("eth"))
