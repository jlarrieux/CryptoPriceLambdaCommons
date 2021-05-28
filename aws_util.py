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

from decimal import Decimal

import boto3
import datetime
import indicator_util
import pickle
from crypto_price_lambda_commons_util import MovingAverageType
from my_rolling_list import MyRollingList
import crypto_price_lambda_commons_util

region = "us-east-1"
dynamodb = boto3.client('dynamodb', region_name=region)
ssm = boto3.client('ssm', region_name=region)
table_name = 'eth-price-hourly-nosql-db'
parameter_key = '0'
s3_resource = boto3.resource('s3')


def get_last_price() -> [None, float]:
    json_string = _get_from_dynamo()
    return None if json_string is None else float(json_string['Item']['last_price']['N'])


def get_last_moving_average(ma_type: MovingAverageType):
    json_string = _get_from_dynamo()
    ma_string = f"{str(ma_type.value)}_day_ma"
    if json_string is None:
        return None
    try:
        json_string['Item'][ma_string]
    except KeyError:
        return None
    return json_string['Item'][ma_string]['N']


def _get_from_dynamo() -> [None, str]:
    return dynamodb.get_item(
        TableName=table_name, Key={'id': {'N': parameter_key}})


def save_price(val: float, is_time_to_save: bool, key: str, bucket: str, initial_size: int = 500) -> MyRollingList:
    update_dynamo_table(val, "last_price")
    round_val = float(Decimal(val).quantize(Decimal("0.01")))
    rolling_average = _load_from_s3(bucket, key)
    if is_time_to_save:
        if rolling_average is None:
            rolling_average = MyRollingList(initial_size)
        rolling_average.add(round_val)
        save_to_s3(bucket, key, rolling_average)
        ma_10 = indicator_util.calculate_simple_moving_average(rolling_average.get_most_recents(10))
        ma_12 = indicator_util.calculate_simple_moving_average(rolling_average.get_most_recents(12))
        ma_50 = indicator_util.calculate_simple_moving_average(rolling_average.get_most_recents(50))
        ma_200 = indicator_util.calculate_simple_moving_average(rolling_average.get_most_recents(200))
        update_dynamo_table(ma_10, "10_day_ma")
        update_dynamo_table(ma_12, "12_day_ma")
        update_dynamo_table(ma_50, "50_day_ma")
        update_dynamo_table(ma_200, "200_day_ma")
    return rolling_average


def update_dynamo_table(val: float, item: str) -> None:
    dynamodb.update_item(TableName=table_name, Key={'id': {
        'N': parameter_key}}, ExpressionAttributeNames={"#name": item}, UpdateExpression=f"set #name = :v",
                         ExpressionAttributeValues={':v': {'N': str(val)}})


def get_parameter(parameter_name):
    return ssm.get_parameter(Name=parameter_name, WithDecryption=True)['Parameter']['Value']


def _load_from_s3(bucket: str, s3_key: str) -> [MyRollingList, None]:
    return load_from_s3(bucket, s3_key)


def save_to_s3(bucket: str, key: str, obj: object) -> None:
    pickle_byte_obj = pickle.dumps(obj)
    s3_resource.Object(bucket, key).put(Body=pickle_byte_obj)


def load_from_s3(bucket: str, key: str):
    try:
        return pickle.loads(s3_resource.Object(bucket, key).get()['Body'].read())
    except Exception as error:
        if isinstance(error, s3_resource.meta.client.exceptions.NoSuchKey):
            return None


def get_rolling_average(path: str) -> [MyRollingList, None]:
    return load_from_s3(path)
