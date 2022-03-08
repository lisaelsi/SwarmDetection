"""
Calculates weight diff each hour.
Also
Calculates weight diff every three days and nine days to see if constant.
"""

import datetime
import numpy as np
import json

sensorType = ["weight"]  # format in L-E code.
sensorVal = 5  # format in L-E code.
weight_data = {}


def delta_weight_calculator(date, sensorVal, test_data=False):
    if test_data:
        current_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        three_days_back = (current_date - datetime.timedelta(days=3)).strftime("%Y-%m-%d")
        ten_days_back = (current_date - datetime.timedelta(days=10)).strftime("%Y-%m-%d")
        current_date = str(current_date)
    else:
        ten_days_back = (datetime.datetime.now() - datetime.timedelta(days=10)).strftime("%Y-%m-%d")
        three_days_back = (datetime.datetime.now() - datetime.timedelta(days=3)).strftime("%Y-%m-%d")
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    if ten_days_back in weight_data:  # erase data from ten days back
        weight_data.pop(ten_days_back)
    if current_date in weight_data:  # if there are already data for this day, add new data in same list
        weight_data[current_date].append(sensorVal)
    else:  # else, create new key for this day and add new data
        weight_data[current_date] = [sensorVal]

    diff = []
    yesterday_date = (datetime.datetime.strptime(date, "%Y-%m-%d").date() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    if len(weight_data[current_date]) < 6:
        try:
            index = -(6-len(weight_data[current_date]))
            weight_val_one_hour = weight_data[current_date][-1] - weight_data[yesterday_date][index]  # latest hour diff
        except KeyError:
            weight_val_one_hour = 0
    else:
        weight_val_one_hour = weight_data[current_date][-1] - weight_data[current_date][-6]  # latest hour diff
    diff.append(weight_val_one_hour)
    #print(weight_val_one_hour)
    if three_days_back in weight_data:  # wait to calculate weight daily diffs until the model has data for at least three days back
        arrays = []
        for key in weight_data.keys():
            arrays.append(np.array(weight_data[key]))
        means = []
        for array in arrays:
            means.append(np.mean(array))
        #print(means)
        temp_diff_each_day = np.diff(np.array(means))
        #print(temp_diff_each_day)
        if len(temp_diff_each_day) >= 2:
            diff.append(sum(temp_diff_each_day[1:2]))  # diff between three latest days
            if len(temp_diff_each_day) >= 8:
                diff.append(sum(temp_diff_each_day[3:8]))  # diff between nine latest days
        """
        first value in diff list is diff in one hour, second value is diff in three days,
        third value is diff in nine days. Might only have one value in the beginning.
        """
        #print({f"{current_date}-{time}": diff})
    return diff


if __name__ == '__main__':
    """
    1. To process generated data: for-loop  
    2. To process live sensor data: delta_weight_calculator(sensorVal)
    """
    f = open('data/weight_data_test.json')
    data = json.load(f)
    f.close()
    for (date, values) in data.items():
        for time in values.keys():
            delta_weight_calculator(date, values[time], test_data=True)

    #delta_weight_calculator(None, sensorVal)
