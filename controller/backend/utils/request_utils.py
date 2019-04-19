from flask import jsonify


def create_response(result):
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def add_cors_support(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
