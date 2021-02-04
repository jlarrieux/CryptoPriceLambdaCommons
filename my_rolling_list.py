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

import logging
from collections import deque
from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class MyRollingList:
    """
    This class is a FIFO list.
    """

    def __init__(self, max=100):
        self._max_length = max
        self._my_deque = deque(maxlen=max)

    def add(self, value: object) -> None:
        self._my_deque.appendleft(value)

    def __str__(self) -> str:
        return f"MyRollingList({list(self._my_deque.__iter__())}, max length={self._max_length}, current size={self.size()})"

    def get_all(self) -> List[object]:
        return list(self._my_deque.__iter__())

    def clear(self) -> None:
        self._my_deque.clear()

    def size(self) -> int:
        return len(list(self._my_deque.__iter__()))

    def __getitem__(self, item) -> List[object]:
        return list(self._my_deque)[item]

    def remove_last(self):
        if self.size() == 0:
            logger.error(f"Attempting to remove last item from empty!")
            return
        del self._my_deque[0]

    def get_most_recents(self, number) -> [List[object], object]:
        if number > self.size():
            logger.error(f"Attempting to get {number} of values with current size of {self.size()}")
            return -1
        return self[:number]
