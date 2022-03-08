"""
Data comes in format:
Widget setdata
{
  "series": [
    {
      "name": "temperature_0",
      "values": [
        31.81,
        32.06,
        31.75,
    }
}

find out which sensor is in the middle
sensorType = t_name_list
sensorVal = t_val_list

Box2 center inside = apiary_le_temperature_4
"""

"""
Program. Takes temp data and calculates the temp mean each day. Takes the diff for three days and for nine days back 
for the current day. Will update everytime a new temp value comes in. 
"""
import datetime
import numpy as np
import json

sensorType = ["temperature_4"]  # format in L-E code.
sensorVal = [0, 1, 2]  # format in L-E code.
MIDDLE_SENSOR_NAME = "temperature_4"
temp_data = {}


def delta_temp_calculator(date, sensorVal, test_data=False, sensorType=None):
    if test_data:
        current_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        temp_val = sensorVal
        three_days_back = (current_date - datetime.timedelta(days=3)).strftime("%Y-%m-%d")
        ten_days_back = (current_date - datetime.timedelta(days=10)).strftime("%Y-%m-%d")
        current_date = str(current_date)
    else:
        ten_days_back = (datetime.datetime.now() - datetime.timedelta(days=10)).strftime("%Y-%m-%d")
        three_days_back = (datetime.datetime.now() - datetime.timedelta(days=3)).strftime("%Y-%m-%d")
        temp_index = sensorType.index(MIDDLE_SENSOR_NAME)
        temp_val = sensorVal[temp_index]
        current_date = datetime.datetime.now()
        current_date = current_date.strftime("%Y-%m-%d")

    if ten_days_back in temp_data:  # erase data from ten days back
        temp_data.pop(ten_days_back)
    if current_date in temp_data:  # if there are already data for this day, add new data in same list
        temp_data[current_date].append(temp_val)
    else:  # else, create new key for this day and add new data
        temp_data[current_date] = [temp_val]

    diff = [temp_val]
    yesterday_date = (datetime.datetime.strptime(date, "%Y-%m-%d").date() - datetime.timedelta(days=1)).strftime(
            "%Y-%m-%d")
    if len(temp_data[current_date]) < 6:
        try:
            index = -(6 - len(temp_data[current_date]))
            temp_val_one_hour = temp_data[current_date][-1] - temp_data[yesterday_date][
                index]  # latest hour diff
        except KeyError:
            temp_val_one_hour = 0
    else:
        temp_val_one_hour = temp_data[current_date][-1] - temp_data[current_date][-6]  # latest hour diff
    diff.append(temp_val_one_hour)

    if three_days_back in temp_data:  # wait to calculate temp diffs until the model has data for at least three days back
        arrays = []
        for key in temp_data.keys():
            arrays.append(np.array(temp_data[key]))
        means = []
        for array in arrays:
            means.append(np.mean(array))
        #print(means)
        temp_diff_each_day = np.diff(np.array(means))
        #print(temp_diff_each_day)
        if len(temp_diff_each_day) >= 2:
            diff.append(sum(temp_diff_each_day[1:2]))
            if len(temp_diff_each_day) >= 8:
                (diff.append(sum(temp_diff_each_day[3:8])))
    #print(diff)
    #print({current_date: diff})
    """
    first value in diff list is current temp
    second value is temp diff in one hour 
    third value is temp diff in three days
    fourth value is temp diff in nine days 
    """
    return diff


if __name__ == '__main__':
    """
    1. To process generated data: for-loop  
    2. To process live sensor data: delta_temp_calculator(sensorType, sensorVal)
    """
    f = open('data/test.json')
    data = json.load(f)
    f.close()
    temp = []
    for (date, values) in data.items():
        for time in values.keys():
            temp.append(delta_temp_calculator(date, values[time], test_data=True))
            #print(f"{date}: {values[time]}")

    #delta_temp_calculator(sensorType, sensorVal)
