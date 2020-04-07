from flask import Blueprint, jsonify, request
from db.sqlite3 import api_log, api_query
import requests
from datetime import datetime
import json

restful_api = Blueprint('restful_api', __name__)


def weatherEndpoint(zipCode):
    response = requests.get(
        'https://api.zip-codes.com/ZipCodesAPI.svc/1.0/QuickGetZipCodeDetails/{}?key=0MB3WYFJGRVXBGDYU3UL'.format(
            zipCode))

    locationData = response.json()
    longitude = locationData['Longitude']
    latitude = locationData['Latitude']

    response = requests.get(
        'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=imperial&APPID=929be9dbced9ad5fe63ae8c31134eb3f'.format(
            latitude, longitude))

    print(response.url)
    weatherData = response.json()

    return(locationData,weatherData)


@restful_api.errorhandler(404)
def page_not_found(e):
    return jsonify(Error='The resource (endpoint) could not be found'), 404


@restful_api.route('/')
def home():
    return jsonify(Message='Welcome to Neilson\'s flask resultful weather API'), 200


@restful_api.route('/weather/current')
def getCurrentWeather():
    # Check if an zip was provided as part of the URL.
    # If zip is provided, assign it to a variable.
    # If no ID is provided, display an error via api.
    if 'zip' in request.args:
        # Try to assign ZIP to integer for lookup purposes
        try:
            if len(request.args['zip']) != 5:
                raise ValueError('Zip code length is less than or greater than 5')
            else:
                zipCode = int(request.args['zip'])
        except:
            # Throw error if not valid Zip Code
            return jsonify(Error='Zip provided is not a valid zip code'), 404

    else:
        return jsonify(
            Error='No zip code query provided. Please provide an ID to lookup by - example.com/api/weather/current?zip=10018'), 404

    data = weatherEndpoint(zipCode)
    locationData = data[0]
    weatherData = data[1]

    currentWeather = {
           'date': weatherData['daily'][0]['dt'],
           'temp': weatherData['daily'][0]['temp']['day'],
           'temp_max': weatherData['daily'][0]['temp']['max'],
           'temp_min': weatherData['daily'][0]['temp']['min'],
           'weather_description': weatherData['daily'][0]['weather'][0]['main'],
           'weather_description_detail': weatherData['daily'][0]['weather'][0]['description'],
            'weather_id': weatherData['daily'][0]['weather'][0]['id']
    }

    endpoint_response = {
        'location': locationData,      
        'weather': currentWeather
    }

    api_log(request.base_url, zipCode, json.dumps(endpoint_response))

    return jsonify(endpoint_response), 200


@restful_api.route('/weather/forecast')
def getForcastWeather():
    # Check if an zip was provided as part of the URL.
    # If zip is provided, assign it to a variable.
    # If no ID is provided, display an error via api.
    if 'zip' in request.args:
        # Try to assign ZIP to integer for lookup purposes
        try:
            if len(request.args['zip']) != 5:
                raise ValueError('Zip code length is less than or greater than 5')
            else:
                zipCode = int(request.args['zip'])
        except:
            # Throw error if not valid Zip Code
            return jsonify(Error='Zip provided is not a valid zip code'), 404
    else:
        return jsonify(
            Error='No zip code query provided. Please provide an ID to lookup by - example.com/api/weather/forecast?zip=10018')

    data = weatherEndpoint(zipCode)
    locationData = data[0]
    weatherData = data[1]

    dailyWeather = []

    for day in weatherData['daily']:
        weather = {
            'date': day['dt'],
            'temp': day['temp']['day'],
            'temp_max': day['temp']['max'],
            'temp_min': day['temp']['min'],
            'weather_description': day['weather'][0]['main'],
            'weather_description_detail': day['weather'][0]['description'],
            'weather_id': day['weather'][0]['id']
        }
        dailyWeather.append(weather)

    endpoint_response = {
        'location': locationData,
        'weather': dailyWeather
    }

    api_log(request.base_url, zipCode, json.dumps(endpoint_response))

    return jsonify(endpoint_response), 200


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
