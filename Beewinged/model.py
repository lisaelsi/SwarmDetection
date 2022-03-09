import csv
import json
import random

from weight_data_processer import delta_weight_calculator
from temp_data_processer import delta_temp_calculator
from get_weather import weather_json_response

my_path = "data/data.csv"


def is_clear_weather(json_response):
    if weather_json_response["cod"] != "404":
        weather = json_response["weather"]
        w_id = weather[0]["id"]
        if int(str(w_id)[:1]) == 8:
            return True
        else:
            return False
    else:
        return False


def get_date(json_object):
    json_data = json.loads(json_object)
    return json_data['date']


def get_weather_data(json_weather):
    is_clear = is_clear_weather(json_weather)

    if is_clear:
        return 1
    else:
        return 0


def temp_constant(temp_diff):
    temp_diff = float(temp_diff)
    if temp_diff > 2:
        return False
    else:
        return True


def extract_month(date_string):
    split_date = date_string.split('-')
    month = int(split_date[1])
    return month


def weight_not_constant(weight_diff):
    weight_diff = float(weight_diff)
    if -3 < weight_diff < -1.5:
        return True
    else:
        return False


def is_summer(m):
    if 5 <= m <= 8:
        return True
    else:
        return False


def within_temp_range(temp_diff):
    temp_diff = int(temp_diff)
    if 33 < temp_diff < 38:
        return True
    else:
        return False


def swarm_detection(hive_temp, three_day_temp_diff, nine_day_temp_diff, weight_diff):
    warning = 'no warning'

   # if is_summer(month) and
    if (temp_constant(three_day_temp_diff) or temp_constant(nine_day_temp_diff)) and within_temp_range(hive_temp):
        warning = 'yngel warning'

    # TODO - vad göra om temperaturen endast varit konstant i tre dagar?
    # if is_clear_weather(weather_json_response) and temp_constant(temp_3) and weight_not_constant(
    # weight_diff) and is_summer(month) and within_temp_range(temp):
    # if random.uniform(0, 1) > 0.5:
    #    warning = 'swarm now'

    # TODO - fix
    # if is_summer(month)
    if is_clear_weather(weather_json_response) and temp_constant(nine_day_temp_diff) and weight_not_constant(
            weight_diff) and within_temp_range(hive_temp):
        warning = 'swarm now'

    return warning


def main(weight_data, temp_data):
    current_temp, one_hour_diff_temp, three_day_diff_temp, nine_day_diff_temp = delta_temp_calculator(temp_data)
    one_hour_diff_weight, three_day_diff_weight, nine_day_diff_weight = delta_weight_calculator(weight_data)

    warning = swarm_detection(current_temp, three_day_diff_temp, nine_day_diff_temp, one_hour_diff_weight)

    return warning
