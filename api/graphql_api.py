from flask import Blueprint, jsonify, request
from graphene import ObjectType, String, Schema
import requests

graphql_api = Blueprint('graphql_api', __name__)

class Query(ObjectType):
    # this defines a Field `hello` in our Schema with a single Argument `name`
    hello = String(name=String(default_value="stranger"))
    goodbye = String()

    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (name) for the Field and returns data for the query Response
    def resolve_hello(root, info, name):
        return f'Hello {name}!'

    def resolve_goodbye(root, info):
        return 'See ya!'

schema = Schema(query=Query)

@graphql_api.errorhandler(404)
def page_not_found(e):
    return jsonify(Error='The resource (endpoint) could not be found'), 404

@graphql_api.route('/')
def home():
    return jsonify(Message='Welcome to Neilson\'s flask graphql weather API'), 200