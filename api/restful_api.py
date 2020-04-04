from flask import Blueprint, jsonify, request
from db.sqlite3 import api_log,api_query
import requests
from datetime import datetime

restful_api = Blueprint('restful_api', __name__)

@restful_api.errorhandler(404)
def page_not_found(e):
    return jsonify(Error='The resource (endpoint) could not be found'), 404

@restful_api.route('/')
def home():
    return jsonify(Message='Welcome to Neilson\'s flask resultful weather API'), 200

@restful_api.route('/weather/current')
def currentWeather():
    # Check if an zip was provided as part of the URL.
    # If zip is provided, assign it to a variable.
    # If no ID is provided, display an error via api.
    if 'zip' in request.args:
        # Try to assign ZIP to integer for lookup purposes
        try:
            if len(request.args['zip']) != 5:
                raise ValueError('Zip code length is less than or greater than 5')
            else:
                zip_code = int(request.args['zip'])
        except:
            # Throw error if not valid Zip Code
            return jsonify(Error='Zip provided is not a valid zip code'), 404

    else:
        return jsonify(
            Error='No zip code query provided. Please provide an ID to lookup by - example.com/api/weather/current?zip=10018'), 404

    response = requests.get(
        'http://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&APPID=929be9dbced9ad5fe63ae8c31134eb3f'.format(zip_code))

    weatherData = response.json()

    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

    dailyWeather = {dt_string: {
        'temp': weatherData['main']['temp'],
        'temp_max': weatherData['main']['temp_max'],
        'temp_min': weatherData['main']['temp_min'],
        'weather_description': weatherData['weather'][0]['description'],
        'weather_id': weatherData['weather'][0]['id']}
    }

    api_response = {
        'city': weatherData['name'],
         'weather': [dailyWeather]
        }

    api_log(request.base_url, zip_code, response.text)

    return jsonify(api_response), 200

@restful_api.route('/weather/forecast')
def forcastWeather():
    # Check if an zip was provided as part of the URL.
    # If zip is provided, assign it to a variable.
    # If no ID is provided, display an error via api.
    if 'zip' in request.args:
        # Try to assign ZIP to integer for lookup purposes
        try:
            if len(request.args['zip']) != 5:
                raise ValueError('Zip code length is less than or greater than 5')
            else:
                zip_code = int(request.args['zip'])
        except:
            # Throw error if not valid Zip Code
            return jsonify(Error='Zip provided is not a valid zip code'), 404
    else:
        return jsonify(
            Error='No zip code query provided. Please provide an ID to lookup by - example.com/api/weather/forecast?zip=10018')

    if 'days' in request.args:
        days = int(request.args['days'])
    else:
        days = 5

    response = requests.get(
        'http://api.openweathermap.org/data/2.5/forecast?zip={}&cnt={}&units=imperial&APPID=929be9dbced9ad5fe63ae8c31134eb3f'.format(zip_code,days))

    weatherData = response.json()

    print(weatherData)

    day = 0
    dailyWeather = {}
    while day < days:
        print(day)
        #for each day in the number of days add data to dictonary
        data = {weatherData['list'][day]['dt_txt'] : {
            'temp': weatherData['list'][day]['main']['temp'],
            'temp_max': weatherData['list'][day]['main']['temp_max'],
            'temp_min': weatherData['list'][day]['main']['temp_min'],
            'weather_description': weatherData['list'][day]['weather'][0]['description'],
            'weather_id': weatherData['list'][day]['weather'][0]['id']}
             }
        #append to daily weather to dictionary
        dailyWeather.update(data)
        day += 1

    api_response = {
        'city': weatherData['city']['name'],
         'weather': [dailyWeather]
        }

    api_log(request.base_url, zip_code, response.text)
    # return weatherData, 200
    return jsonify(api_response), 200

@restful_api.route('/log')
def request_log():
    if 'id' in request.args:
        try:
            id = int(request.args['id'])
        except:
            return jsonify(Error='ID provided not a valid ID'), 404
        results = api_query('''select * from request_log where id = {}'''.format(id))
        if results:
            return jsonify(results), 200
        else:
            return jsonify(Error='ID not found'), 404
    else:
        results = api_query('''select * from request_log''')
        return jsonify(results), 200

