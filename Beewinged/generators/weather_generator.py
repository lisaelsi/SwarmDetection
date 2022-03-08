import json
import random

START_DATE = "2022-07-01"
END_DATE = "2022-09-10"
NAME_DATA_FILE = "weather_data"
SWARM_DATE = "2022-07-15"
SWARM_TIME = "14:00"
data = {}
# Clear weather
CLEAR = ['clear']
# Not clear weather
NOT_CLEAR = ['not_clear']


def main(name_data_file, start_date, end_date):
    generate_csv(name_data_file, start_date, end_date)


def generate_csv(name_data_file, start_date, end_date):
    start_year, start_month, start_day = start_date.split('-')
    end_year, end_month, end_day = end_date.split('-')
    current_year, current_month, current_day = start_year, start_month, start_day
    while int(current_month) <= int(end_month):
        if int(current_month) == int(end_month) and int(current_day) > int(end_day):
            break
        data[format_day(current_year, current_month, current_day)] = insert_daily_data()
        current_month, current_day = increase_day(current_month, current_day)

    with open(f"{name_data_file}.json", 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def increase_day(current_month, current_day):
    # currently this method makes all months have 30 days...
    increased_day = int(current_day) + 1
    if increased_day > 30:
        return int(current_month) + 1, 1
    return int(current_month), int(current_day) + 1


def insert_daily_data():
    current_hour = 0
    current_minute = 0

    rand_factor = random.uniform(0, 1)

    if rand_factor > 0.4:
        json_data = "clear"
    else:
        json_data = "not_clear"
    increase_time(current_hour, current_minute)
    return json_data


def format_day(current_year, current_month, current_day):
    if int(current_month) < 10:
        current_month = f"0{int(current_month)}"
    if int(current_day) < 10:
        current_day = f"0{int(current_day)}"
    return f"{current_year}-{current_month}-{current_day}"


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


if __name__ == '__main__':
    main(NAME_DATA_FILE, START_DATE, END_DATE)