import decimal
import aws_util
import indicator_util
import boto3
import util
import csv
import pickle
from MyRollingList import MyRollingList
from my_rolling_list import MyRollingList as MY


decimal.getcontext().prec = 7
region = "us-east-1"
dynamodb = boto3.client('dynamodb', region_name=region)
parameter_key = '0'
table_name = 'eth-price-hourly-nosql-db'
s3_resource = boto3.resource('s3')
bucket = 'com.jlarrieux.lambda'
key = 'prices.pkl'


def main() -> None:
    my_rolling_list = aws_util.load_from_s3()
    print(my_rolling_list)
    # x = 10
    # print(f"last price: {aws_util.get_last_price()}")
    # recents = my_rolling_list.get_most_recents(x)
    # print(f"with size:{my_rolling_list.size()}\n{x} most recent: {recents}")
    # print(indicator_util.calculate_simple_moving_average(recents))
    print_averages(my_rolling_list, 3)
    print_averages(my_rolling_list, 7)
    print_averages(my_rolling_list, 10)
    print_averages(my_rolling_list, 15)
    print_averages(my_rolling_list, 30)
    print_averages(my_rolling_list, 50)
    print_averages(my_rolling_list, 100)
    print_averages(my_rolling_list, 200)
    print_averages(my_rolling_list, 500)
    print_averages(my_rolling_list, 1000)
    print_averages(my_rolling_list, 1500)
    # print(aws_util.get_last_moving_average(util.MovingAverageType.FIFTY))
    # current_size = my_rolling_list.size()
    # ten_day_ma = -1
    # fifty_day_ma = -1
    # two_hundred_day_ma = -1
    # if current_size >= 10:
    #     ten_day_ma = indicator_util.calculate_simple_moving_average(my_rolling_list.get_most_recents(10))
    # if current_size >= 50:
    #     fifty_day_ma = indicator_util.calculate_simple_moving_average(my_rolling_list.get_most_recents(50))
    # if current_size >= 200:
    #     two_hundred_day_ma = indicator_util.calculate_simple_moving_average(my_rolling_list.get_most_recents(200))
    #
    # print(f"10 day ma: {ten_day_ma}\t50 day ma: {fifty_day_ma}\t200 day ma: {two_hundred_day_ma}")

def print_averages(my_rolling_list:MyRollingList, value: int) ->None:
    print(f"The last {value} day averages were: {util.format_money_to_string(indicator_util.calculate_simple_moving_average(my_rolling_list.get_most_recents(value)))}")


def load_and_process() -> None:
    with open("C:\\Users\mrsea\Documents\Data\ETH-USD.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        i = 0
        # my = MY(max=100000)
        max = 0
        for row in csv_reader:
            if line_count == 0:
                print(",\t\t  ".join(row))
            else:
                val = float(row[4])
                if val > max:
                    max = val
            line_count +=1

    print(max)



if __name__ == '__main__':
    main()
