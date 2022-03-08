import requests

api_key = "8835b43f30262cb50b03a4bc75bb8a6b"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
city_name = 'Gothenburg'
complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&units=metric"

response = requests.get(complete_url)
weather_json_response = response.json()

if weather_json_response["cod"] != "404":

    # store the value of "main" key in variable y
    y = weather_json_response["main"]

    current_temperature = y["temp"]
    current_pressure = y["pressure"]
    current_humidity = y["humidity"]

    # store the value of "weather" key in variable z
    z = weather_json_response["weather"]

    # store the value corresponding
    # to the "description" key at
    # the 0th index of z
    # https://openweathermap.org/weather-conditions
    weather_description = z[0]["description"]
    weather_id = z[0]["id"]

else:
    print(" City Not Found ")


def print_weather_data():
    print(" City name = " +
          city_name +
          " \n Temperature = " +
          str(current_temperature) +
          "°C" +
          "\n Atmospheric pressure (in hPa unit) = " +
          str(current_pressure) +
          "\n Humidity (in percentage) = " +
          str(current_humidity) +
          "\n Description = " +
          str(weather_description) +
          "\n Weather id = " +
          str(weather_id))


def is_clear_weather(json_response):
    weather = json_response["weather"]
    w_id = weather[0]["id"]
    if int(str(w_id)[:1]) == 8:
        return True
    else:
        return False


#print_weather_data()
#print(is_clear_weather(x))