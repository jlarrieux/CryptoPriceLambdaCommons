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

import backend_commons_aws_util
from my_rolling_list import  MyRollingList

bucket = "com.jlarrieux.lambda"
s3_key = "ethereum_rsi_calculations.pkl"
key = "cryptofund2022/union/balance.pkl"

def trying():
   # print(backend_commons_aws_util.load_from_s3("ethereum_daily_closing_prices.pkl"))
   #  backend_commons_aws_util.save_to_s3(key, 3515.306)
    print(backend_commons_aws_util.load_from_s3(key))


if __name__ == '__main__':
    trying()
