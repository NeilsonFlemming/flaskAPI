from flask import Blueprint, jsonify, request
from db.sqlite3 import api_log,api_query
import requests

restful_api = Blueprint('restful_api', __name__)

@restful_api.errorhandler(404)
def page_not_found(e):
    return jsonify(Error='The resource (endpoint) could not be found'), 404

@restful_api.route('/')
def home():
    return jsonify(Message='Welcome to Neilson\'s flask resultful weather API'), 200

@restful_api.route('/weather/current')
def current_weather():
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

    r = requests.get(
        'http://api.openweathermap.org/data/2.5/weather?zip={}&APPID=929be9dbced9ad5fe63ae8c31134eb3f'.format(zip_code))

    api_log(request.base_url,zip_code,r.text)
    return r.json(), 200

@restful_api.route('/weather/forecast')
def forcast_weather():
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

    r = requests.get(
        'http://api.openweathermap.org/data/2.5/forecast?zip={}&APPID=929be9dbced9ad5fe63ae8c31134eb3f'.format(zip_code))

    api_log(request.base_url, zip_code, r.text)
    return r.json(), 200

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

