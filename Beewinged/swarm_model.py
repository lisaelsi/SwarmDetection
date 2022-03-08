import csv
import datetime
import json
import random

from weight_data_processer import delta_weight_calculator
from temp_data_processer import delta_temp_calculator
from get_weather import is_clear_weather, weather_json_response


"""

INPUT (json format)
today's date

dict with information about temperature diff:
    - constant temp for 3 days: index 0
    - constant temp for 9 days: index 1
→ bigger than some threshold (+/- 2 degrees)

weight diff for 1 hour:
→ bigger than some threshold (2 kg)

weather (clear/not_clear)

OUTPUT
csv file with
DATE, TEMPERATURE DIFF FOR 3 DAYS, TEMPERATURE DIFF FOR 9 DAYS, WEIGHT DIFF, WEATHER
date, t_diff_3_days, t_diff_9_days, weight_diff, weather

"""

my_path = "data/data.csv"

header = ['DATE', 'CURRENT_TEMP', '3_DAY_TEMP', '9_DAY_TEMP', '1_HOUR_WEIGHT', 'WEATHER', 'LABEL']

# format weight data: '{ "weight_diff": ["1-hour-diff", "3-day-diff", "9-day-diff"] }'
weight_data_json = '{ "weight_diff": ["20", "2.4", "2.8"] }'

# format temp data : '{ "date":"2022-07-20", "temp": ["1-hour-diff", "current-temp", "3-day-diff", "9-day-diff"] }'
temp_data_json = '{ "date": "2022-07-20", "temp": ["0.78", "34", "2.12", "3.21"] }'

# TODO - vad göra med denna?
weather_data_json = '{  }'


# TODO: Städa i koden

def create_file(path, data):
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        writer.writerows(data)

        f.close()


def add_to_csv(row, path):
    with open(path, 'a', newline='\n') as f:
        writer = csv.writer(f)

        writer.writerow(row)


def get_date(json_object):
    json_data = json.loads(json_object)
    return json_data['date']


def get_weight_data(w_data):
    #json_data = json.loads(json_object)
    #w_data = json_data['weight_diff']
    try:
        one_hour_diff = w_data[0]
    except Exception:
        one_hour_diff = 0

    return one_hour_diff


def get_temp_data(temperature_data):
    #emperature_data = json.loads(json_object)
    #temp_data = json_data['temp']

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


# TODO - vad ska temp-diffen vara??
def temp_constant(temp):
    temp = float(temp)
    if temp > 2:
        return False
    else:
        return True


def extract_month(date_string):
    date = date_string.split('-')
    month = int(date[1])
    return month


# TODO - vad ska weight_diff vara?
def weight_not_constant(weight_diff):
    weight_diff = float(weight_diff)
    if -3 < weight_diff < -1.5:
        return True
    else:
        return False


def is_summer(m):
    if 6 <= m <= 8:
        return True
    else:
        return False


def within_temp_range(temp):
    temp = int(temp)
    if 33 < temp < 38:
        return True
    else:
        return False


def generate_label(temp, temp_3, temp_9, weight_diff, month):
    # this function should generate labels for the data

    # no_swarm: 3
    label = 3

    if is_summer(month) and (temp_constant(temp_3) or temp_constant(temp_9)) and within_temp_range(temp):
        # swarm_warning: 1
        label = 1

    #if is_clear_weather(weather_json_response) and temp_constant(temp_3) and weight_not_constant(
            #weight_diff) and is_summer(month) and within_temp_range(temp):
        #if random.uniform(0, 1) > 0.5:  # TODO är detta ett bra sätt att göra det på?
        # swarm_now: 2
        #    label = 2

    # TODO - fixa denna långa fula rad?
    if is_clear_weather(weather_json_response) and temp_constant(temp_9) and weight_not_constant(
            weight_diff) and is_summer(
            month) and within_temp_range(temp):
        # swarm_now: 2
        label = 2

    return label


def create_row(todays_date, weather_data, weight_data, temp_data):
    w = get_weather_data(weather_data)
    current_temp, temp_diff_3_day, temp_diff_9_day = get_temp_data(temp_data)
    weight_diff = get_weight_data(weight_data)
    #date = get_date(temp_data) TODO: fixa detta? hur få datum
    #date = '2022-07-01'

    month = extract_month(todays_date)

    label = generate_label(current_temp, temp_diff_3_day, temp_diff_9_day, weight_diff, month)

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
    # data = create_row(dates[i], weather_json_response, weight[i], temp[i])

create_file(my_path, all_data)


#add_to_csv(data, my_path)