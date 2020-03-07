from flask import Flask, jsonify
from api.restful_api import restful_api
from api.graphql_api import graphql_api
from db.sqlite3 import db_setup

#https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask
#https://peaceful-thicket-43573.herokuapp.com/

app = Flask(__name__)
app.config["DEBUG"] = True
app.register_blueprint(restful_api, url_prefix='/api')
app.register_blueprint(graphql_api, url_prefix='/graphql')
db_setup()

@app.errorhandler(404)
def page_not_found(e):
    return jsonify(Error='The resource could not be found'), 404

@app.route('/', methods=['GET'])
def home():
    return jsonify(Message='Welcome to Neilson\'s flask app'), 200

if __name__=='__main__':
    app.run()