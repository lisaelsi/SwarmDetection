import requests

api_key = "8835b43f30262cb50b03a4bc75bb8a6b"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
city_name = 'Gothenburg'
complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&units=metric"

response = requests.get(complete_url)
weather_json_response = response.json()
