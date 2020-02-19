from flask import Flask
from flask import jsonify, request
import requests

#https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Neilson's python flask weather API </h1>
    <p>A prototype API for weather data.</p>'''

@app.errorhandler(404)
def page_not_found(e):
    return jsonify(Error='The resource could not be found'), 404

@app.route('/api/weather/current', methods=['GET'])
def current_weather():
    # Check if an zip was provided as part of the URL.
    # If zip is provided, assign it to a variable.
    # If no ID is provided, display an error via api.
    if 'zip' in request.args :
        # Try to assign ZIP to integer for lookup purposes
        try:
            if len(request.args['zip']) !=5:
                raise ValueError('Zip code length is less than or greater than 5')
            else:
                zip_code = int(request.args['zip'])
        except:
            # Throw error if not valid Zip Code
            return jsonify(Error='Zip provided is not a valid zip code')

    else:
        return jsonify(Error='No zip code query provided. Please provide an ID to lookup by - example.com/api/weather/current?zip=10018')

    r = requests.get(
        'http://api.openweathermap.org/data/2.5/weather?zip={}&APPID=929be9dbced9ad5fe63ae8c31134eb3f'.format(zip_code))

    return r.json(),200


if __name__ == '__main__':
    app.run()
