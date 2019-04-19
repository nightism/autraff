import json
from flask import request
from flask import Blueprint

from database import db_schema

from utils.request_utils import add_cors_support
from utils.request_utils import create_response

db_api = Blueprint('db_client_api', __name__)

client_schema = db_schema.ClientSchema()
clients_schema = db_schema.ClientSchema(many=True)


# endpoint to show all clients
@db_api.route("/client", methods=["GET"])
def get_client():
    all_clients = db_schema.Client.query.all()
    result = clients_schema.dump(all_clients)

    resp = create_response(result.data)
    return resp


# endpoint to get client detail by ip
@db_api.route("/client/<ip>", methods=["GET"])
def client_detail(ip):
    client = db_schema.Client.query.get(ip)

    resp = create_response(client)
    return resp


# endpoint to create new client
@db_api.route("/client", methods=["POST"])
def add_client():
    data = json.loads(request.data)

    ip = data['ip']
    system = data['system']
    version = data['version']

    new_client = db_schema.Client(ip, system, version)

    db_schema.db.session.add(new_client)
    db_schema.db.session.commit()

    resp = add_cors_support(client_schema.jsonify(new_client))

    return resp


# endpoint to update client
@db_api.route("/client", methods=["PUT"])
def client_update():
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

    resp = add_cors_support(client_schema.jsonify(client))
    return resp


# endpoint to delete client
@db_api.route("/client", methods=["DELETE"])
def client_delete():
    data = json.loads(request.data)

    ip = data['ip']
    client = db_schema.Client.query.get(ip)
    db_schema.db.session.delete(client)
    db_schema.db.session.commit()

    resp = add_cors_support(client_schema.jsonify(client))
    return resp
