"""
START_DATE, END_DATE format: "2022-04-01"
OBS! Only within same year currently - fix later.
"""

import json
import random
import datetime

START_DATE = "2022-07-01"
END_DATE = "2022-09-10"
NAME_DATA_FILE = "weight_data_test"
SWARM_DATE = "2022-07-15"
SWARM_TIME = "14:00"
data = {}
# Average temperatures during winter
WIN_WEIGHT = [10]
# Average temperatures during spring
SPR_WEIGHT = [20]
# Average temperatures during summer
SUM_WEIGHT = [30]
# Average temperatures during fall
FALL_WEIGHT = [20]


def main(name_data_file, start_date, end_date):
    generate_csv(name_data_file, start_date, end_date, WIN_WEIGHT, SPR_WEIGHT, SUM_WEIGHT, FALL_WEIGHT)
    insert_swarm(SWARM_DATE, SWARM_TIME)


def generate_csv(name_data_file, start_date, end_date, win_weight, spr_weight, sum_weight, fall_weight):
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y-%m-%d")
    start_year, start_month, start_day = start_date.split('-')
    end_year, end_month, end_day = end_date.split('-')
    current_year, current_month, current_day = start_year, start_month, start_day
    while int(current_month) <= int(end_month):
        if int(current_month) == int(end_month) and int(current_day) > int(end_day):
            break
        if int(current_month) <= 2 or int(current_month) == 12:
            """
            Winter. 
            """
            data[format_day(current_year, current_month, current_day)] = insert_daily_data(win_weight)

        if 5 >= int(current_month) >= 3:
            """
            Spring.
            """
            data[format_day(current_year, current_month, current_day)] = insert_daily_data(spr_weight)
        if 8 >= int(current_month) >= 6:
            """
            Summer.  
            """
            data[format_day(current_year, current_month, current_day)] = insert_daily_data(sum_weight)
        if 11 >= int(current_month) >= 9:
            """
            Fall.  
            """
            data[format_day(current_year, current_month, current_day)] = insert_daily_data(fall_weight)
        current_year, current_month, current_day = increase_day(current_year, current_month, current_day)

    with open(f"{name_data_file}.json", 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def increase_day(current_year, current_month, current_day):
    # currently this method makes all months have 30 days...
    date = f"{current_year}-{current_month}-{current_day}"
    date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    date = (date + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    return date.split("-")


def format_day(current_year, current_month, current_day):
    if int(current_month) < 10:
        current_month = f"0{int(current_month)}"
    if int(current_day) < 10:
        current_day = f"0{int(current_day)}"
    return f"{current_year}-{current_month}-{current_day}"


def insert_daily_data(avg_weight):
    data = {}
    current_hour = 0
    current_minute = 0
    weight = avg_weight[0]
    while current_hour < 24:
        if current_hour <= 8:
            data[format_time(current_hour, current_minute)] = weight + random.uniform(-0.2, 0.2)
        if 12 >= current_hour > 8:
            data[format_time(current_hour, current_minute)] = weight + random.uniform(-0.2, 0.2)
        if 18 >= current_hour > 12:
            data[format_time(current_hour, current_minute)] = weight + random.uniform(-0.2, 0.2)
        if 23 >= current_hour > 18:
            data[format_time(current_hour, current_minute)] = weight + random.uniform(-0.2, 0.2)
        current_hour, current_minute = increase_time(current_hour, current_minute)
    return data


def increase_time(current_hour, current_minute):
    increased_minute = current_minute + 10
    if increased_minute == 60:
        current_hour += 1
        return current_hour, 0
    return current_hour, increased_minute


def format_time(current_hour, current_minute):
    if current_hour < 10:
        current_hour = f"0{current_hour}"
    if current_minute < 10:
        current_minute = f"0{current_minute}"
    return f"{current_hour}:{current_minute}"


def insert_swarm(date: str, time: str):
    """
    insert swarm in given date. Will change the data approximately one week before
    to fulfill the conditions before swarming. OBS! must be within same generated data interval.
    there are roughly 4000 bees per pound. 1 pound = 0,45 kg.
    LE#1: 17 kg 29  May, 15 kg 30 May, 20 % drop. Might be for whole
    :param date: "2022-06-24"
    :return: None
    """
    #  weight should be fairly constant
    swarm_year, swarm_month, swarm_day = date.split('-')
    start_swarm_month, start_swarm_day = get_start_of_swarm_date(swarm_day, swarm_month)
    start_swarm_date = f"{swarm_year}-{start_swarm_month}-{start_swarm_day}"
    # Weight drop peak

    win_weight = [WIN_WEIGHT[0] - 2]
    spr_weight = [SPR_WEIGHT[0] - 2]
    sum_weight = [SUM_WEIGHT[0] - 2]
    fall_weight = [FALL_WEIGHT[0] - 2]
    generate_csv(NAME_DATA_FILE, start_swarm_date, date, win_weight, spr_weight, sum_weight, fall_weight)

    # Swarm occurs at desired time
    data[date][time] = data[date][time] - random.uniform(2, 3)

    with open(f"{NAME_DATA_FILE}.json", 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_start_of_swarm_date(swarm_day, swarm_month):

    start_swarm_month = int(swarm_month)
    start_swarm_day = int(swarm_day)
    return start_swarm_month, start_swarm_day


if __name__ == '__main__':
    main(NAME_DATA_FILE, START_DATE, END_DATE)