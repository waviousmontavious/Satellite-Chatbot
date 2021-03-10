import os
import json
import requests
from rasa_sdk import Tracker


def get_dict(json_file):
    with open(json_file) as f:
        return json.load(f)


def get_last_bot_event(tracker: Tracker):
    event = next(e for e in reversed(tracker.events) if e['event'] == 'bot')
    return event['metadata']['template_name']


def get_weather(city_name):
    # Enter your API key here
    api_key = "bd2f89be8d346be8d67f39c35098ac29"

    # base_url variable to store url
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    # complete_url variable to store
    # complete url address
    complete_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(city_name, api_key)

    # get method of requests module
    # return response object
    response = requests.get(complete_url)

    # json method of response object
    # convert json format data into
    # python format data
    x = response.json()

    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to
    # "404", means city is found otherwise,
    # city is not found
    if response.status_code == 200:
        # store the value of "main"
        # key in variable y
        y = x["main"]

        # store the value corresponding
        # to the "temp" key of y
        current_temperature = y["temp"]

        # store the value corresponding
        # to the "pressure" key of y
        current_pressure = y["pressure"]

        # store the value corresponding
        # to the "humidity" key of y
        current_humidiy = y["humidity"]

        # store the value of "weather"
        # key in variable z
        z = x["weather"]

        # store the value corresponding
        # to the "description" key at
        # the 0th index of z
        weather_description = z[0]["description"]

        # print following values
        info = f" Temperature (in kelvin unit) = {str(current_temperature)}" \
               f"\n Atmospheric pressure (in hPa unit) = {str(current_pressure)}" \
               f"\n Humidity (in percentage) = {str(current_humidiy)}" \
               f"\n Description = {weather_description}"
        return info

    else:
        return " City Not Found "
