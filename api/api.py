from flask import Flask
from flask import jsonify, request
import requests as Requests

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Neilson's python flask weather API </h1>
    <p>A prototype API for distant reading of science fiction novels.</p>'''

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/api/weather/current', methods=['GET'])
def current_weather():
    # Check if an zip was provided as part of the URL.
    # If zip is provided, assign it to a variable.
    # If no ID is provided, display an error via api.
    if 'zip' in request.args:
        # Try to assign ZIP to integer for lookup purposes
        try:
            id = int(request.args['id'])
        except:
            # Throw error if not valid Zip Code
            return jsonify(Error='ID provided is not a valid zip code')
    else:
        return jsonify(Error='No zip query field provided. Please provide an ID to lookup by - example.com/api/weather/current?zip=10018')

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for book in books:
        if book['id'] == id:
            results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)


if __name__ == '__main__':
    app.run()
