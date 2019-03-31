import json
from flask import request, jsonify
from flask import Blueprint

from database import db_schema

db_api = Blueprint('db_client_api', __name__)

client_schema = db_schema.ClientSchema()
clients_schema = db_schema.ClientSchema(many=True)


# endpoint to show all clients
@db_api.route("/client", methods=["GET"])
def get_client():
    all_clients = db_schema.Client.query.all()
    result = clients_schema.dump(all_clients)

    resp = jsonify(result.data)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


# endpoint to get client detail by ip
@db_api.route("/client/<ip>", methods=["GET"])
def client_detail(ip):
    client = db_schema.Client.query.get(ip)

    resp = client_schema.jsonify(client)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


# endpoint to create new client
@db_api.route("/client", methods=["POST"])
def add_client():
    # TODO to be deprecated
    ip = request.json['ip']
    system = request.json['system']
    version = request.json['version']

    new_client = db_schema.Client(ip, system, version)

    db_schema.db.session.add(new_client)
    db_schema.db.session.commit()

    resp = client_schema.jsonify(new_client)
    # TODO for all: find a more elegant way to deal with cors header
    #  for example -
    resp.headers.add('Access-Control-Allow-Origin', '*')

    return resp


# endpoint to update client
@db_api.route("/client", methods=["PUT"])
def client_update():
    # TODO to be deprecated
    data = json.loads(request.data)
    ip = data['ip']
    client = db_schema.Client.query.get(ip)
    new_ip = data['new_ip']
    system = data['system']
    version = data['version']

    client.ip = new_ip
    client.system = system
    client.version = version

    db_schema.db.session.commit()

    resp = client_schema.jsonify(client)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


# endpoint to delete client
@db_api.route("/client", methods=["DELETE"])
def client_delete():
    # TODO to be deprecated
    data = json.loads(request.data)
    ip = data['ip']
    client = db_schema.Client.query.get(ip)
    db_schema.db.session.delete(client)
    db_schema.db.session.commit()

    resp = client_schema.jsonify(client)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp
