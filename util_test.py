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

import crypto_price_lambda_commons_util


class UtilTest(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_format_money_return_correct_string_for_unit(self) -> None:
        self.assertEqual("$1.00", crypto_price_lambda_commons_util.format_money_to_string(1))

    def test_format_money_return_correct_string_for_tens(self) -> None:
        self.assertEqual("$10.00", crypto_price_lambda_commons_util.format_money_to_string(10))

    def test_format_money_return_correct_string_for_hundreds(self) -> None:
        self.assertEqual("$200.50", crypto_price_lambda_commons_util.format_money_to_string(200.5))

    def test_format_money_return_correct_string_for_thousands(self) -> None:
        self.assertEqual("$2,000.50", crypto_price_lambda_commons_util.format_money_to_string(2000.5))

    def test_format_money_return_correct_string_for_tens_of_thousand(self) -> None:
        self.assertEqual("$20,000.50", crypto_price_lambda_commons_util.format_money_to_string(20000.5))

    def test_format_money_return_correct_string_for_hundreds_of_thousand(self) -> None:
        self.assertEqual("$200,000.50", crypto_price_lambda_commons_util.format_money_to_string(200000.5))

    def test_format_money_return_correct_string_for_millions(self) -> None:
        self.assertEqual("$2.00M", crypto_price_lambda_commons_util.format_money_to_string(2000000.5))

    def test_format_money_return_correct_string_for_tens_of_million(self) -> None:
        self.assertEqual("$20.00M", crypto_price_lambda_commons_util.format_money_to_string(20000000.5))

    def test_format_money_return_correct_string_for_hundreds_of_million(self) -> None:
        self.assertEqual("$200.00M", crypto_price_lambda_commons_util.format_money_to_string(200000000.5))

    def test_format_money_return_correct_string_for_billions(self) -> None:
        self.assertEqual("$2.00B", crypto_price_lambda_commons_util.format_money_to_string(2000000000.5))

    def test_format_money_return_correct_string_for_tens_of_billion(self) -> None:
        self.assertEqual("$20.00B", crypto_price_lambda_commons_util.format_money_to_string(20000000000.5))

    def test_format_money_return_correct_string_for_hundreds_of_billion(self) -> None:
        self.assertEqual("$200.00B", crypto_price_lambda_commons_util.format_money_to_string(200000000000.5))

    def test_format_money_return_correct_string_for_trillions(self) -> None:
        self.assertEqual("$2.00T", crypto_price_lambda_commons_util.format_money_to_string(2000000000000.5))

    def test_format_money_return_correct_string_for_tens_of_trillion(self) -> None:
        self.assertEqual("$20.00T", crypto_price_lambda_commons_util.format_money_to_string(20000000000000.5))

    def test_format_money_return_correct_string_for_hundreds_of_trillion(self) -> None:
        self.assertEqual("$200.00T", crypto_price_lambda_commons_util.format_money_to_string(200000000000000.5))


if __name__ == '__main__':
    unittest.main()
