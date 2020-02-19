from flask import Blueprint, jsonify, request
import requests

graphql_api = Blueprint('graphql_api', __name__)

@graphql_api.errorhandler(404)
def page_not_found(e):
    return jsonify(Error='The resource (endpoint) could not be found'), 404

@graphql_api.route('/')
def home():
    return jsonify(Message='Welcome to Neilson\'s flask graphql weather API'), 200