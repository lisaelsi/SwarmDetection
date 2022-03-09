import csv
import json
import random

from weight_data_processer import delta_weight_calculator
from temp_data_processer import delta_temp_calculator
from get_weather import weather_json_response

my_path = "data/data.csv"

header = ['DATE', 'CURRENT_TEMP', '3_DAY_TEMP', '9_DAY_TEMP', '1_HOUR_WEIGHT', 'WEATHER', 'LABEL']


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


def get_weight_data(w_data):
    try:
        one_hour_diff = w_data[0]
    except Exception:
        one_hour_diff = 0

    return one_hour_diff


def get_temp_data(temperature_data):
    try:
        one_hour_diff = temperature_data[1]
    except Exception:
        one_hour_diff = 0
    try:
        current_temperature = temperature_data[0]
    except Exception:
        current_temperature = 0
    try:
        three_day_diff = temperature_data[2]
    except Exception:
        three_day_diff = 0
    try:
        nine_day_diff = temperature_data[3]
    except Exception:
        nine_day_diff = 0

    return current_temperature, three_day_diff, nine_day_diff


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


def swarm_detection(hive_temp, three_day_temp_diff, nine_day_temp_diff, weight_diff, month):
    # no_swarm: 3
    label = 3

    if is_summer(month) and (temp_constant(three_day_temp_diff) or temp_constant(nine_day_temp_diff)) \
            and within_temp_range(hive_temp):
        # swarm_warning: 1
        label = 1

    # TODO - vad göra om temperaturen endast varit konstant i tre dagar?
    #if is_clear_weather(weather_json_response) and temp_constant(temp_3) and weight_not_constant(
            #weight_diff) and is_summer(month) and within_temp_range(temp):
        #if random.uniform(0, 1) > 0.5:
        # swarm_now: 2
        #    label = 2

    # TODO - fix
    if is_clear_weather(weather_json_response) and temp_constant(nine_day_temp_diff) and weight_not_constant(
            weight_diff) and is_summer(month) and within_temp_range(hive_temp):
        # swarm_now: 2
        label = 2

    return label


def create_file(path, data):
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        writer.writerows(data)

        f.close()


def create_row(todays_date, weather_data, weight_data, temp_data):
    w = get_weather_data(weather_data)
    current_temp, temp_diff_3_day, temp_diff_9_day = get_temp_data(temp_data)
    weight_diff = get_weight_data(weight_data)

    month = extract_month(todays_date)

    label = swarm_detection(current_temp, temp_diff_3_day, temp_diff_9_day, weight_diff, month)

    return [todays_date, current_temp, temp_diff_3_day, temp_diff_9_day, weight_diff, w, label]


f = open('data/weight_data_test.json')
weight_data = json.load(f)
f.close()
weight = []
for (date, values) in weight_data.items():
    for time in values.keys():
        weight.append(delta_weight_calculator(date, values[time], test_data=True))

f = open('data/test.json')
temp_data = json.load(f)
f.close()
temp = []
dates = []
for (date, values) in temp_data.items():
    for time in values.keys():
        temp.append(delta_temp_calculator(date, values[time], test_data=True))
        dates.append(f"{date}:{time}")


all_data = []

for i in range(500, 5000):
    all_data.append(create_row(dates[i], weather_json_response, weight[i], temp[i]))

create_file(my_path, all_data)

