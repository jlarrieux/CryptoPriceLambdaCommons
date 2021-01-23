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

import unittest

from my_rolling_list import MyRollingList


class MyRollingListTest(unittest.TestCase):

    def test_empty_returns_size_zero(self):
        self.assertEqual(0, MyRollingList().size())

    def test_bounded_size(self):
        my = MyRollingList(max=2)
        my.add(3)
        my.add(2)
        my.add(1)
        self.assertEqual([1, 2], my.get_all())

    def test_after_add_size_is_one(self):
        my = MyRollingList()
        my.add(15)
        self.assertEqual(1, my.size())
        self.assertEqual(15, my.get_most_recents(1)[0])

    def test_asking_more_return_negative_one(self):
        my = MyRollingList()
        my.add(15)
        with self.assertLogs(level='INFO') as cm:
            self.assertEqual(-1, my.get_most_recents(2))
            self.assertIn("ERROR:root:Attempting to get 2 of values with current size of 1", cm.output)

    def test_get_all(self):
        my = MyRollingList()
        my.add(15)
        self.assertEqual([15], my.get_all())

    def test_clear(self):
        my = MyRollingList()
        my.add(15)
        self.assertEqual(1, my.size())
        my.clear()
        self.assertEqual(0, my.size())

    def test_get_most_recents(self):
        my = MyRollingList()
        my.add(1)
        my.add(2)
        my.add(3)
        self.assertEqual([3, 2, 1], my.get_most_recents(3))
        self.assertEqual([3, 2], my.get_most_recents(2))
        self.assertEqual([3], my.get_most_recents(1))


if __name__ == '__main__':
    unittest.main()
