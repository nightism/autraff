from flask import request, jsonify
from flask import Blueprint

from datetime import datetime
import json

import db_schema

db_api = Blueprint('db_api', __name__)

client_schema = db_schema.ClientSchema()
clients_schema = db_schema.ClientSchema(many=True)

job_schema = db_schema.JobSchema()
jobs_schema = db_schema.JobSchema(many=True)


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


# endpoint to add job
@db_api.route("/job", methods=["POST"])
def add_job():
    data = json.loads(request.data)

    name = data['name']
    module = data['module']
    client = data['client']

    interval = int(data['interval'])
    date_time = data['start']
    dt_obj = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')

    # persona = data['persona']
    arguments = data['arguments']

    new_job = db_schema.Job(name, module, client, interval, dt_obj, arguments=arguments)
    db_schema.db.session.add(new_job)
    db_schema.db.session.commit()

    resp = job_schema.jsonify(new_job)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


# endpoint to show all job
@db_api.route("/job", methods=["GET"])
def get_jobs():
    all_jobs = db_schema.Job.query.all()
    result = jobs_schema.dump(all_jobs)

    resp = jsonify(result.data)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


# endpoint to show one job
@db_api.route("/job/<id>/detail", methods=["GET"])
def get_a_single_job(id):
    job = db_schema.Job.query.get(id)

    resp = job_schema.jsonify(job)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


# endpoint to update one job
@db_api.route("/job/<id>", methods=["PUT"])
def update_a_job(id):
    job = db_schema.Job.query.get(id)

    data = json.loads(request.data)
    job.name = data['name']
    # job.persona = request.json['persona']
    job.interval = int(data['interval'])
    job.start = datetime.strptime(data['start'], '%Y-%m-%d %H:%M:%S')
    job.arguments = data['arguments']
    print(job.arguments)

    db_schema.db.session.commit()

    resp = job_schema.jsonify(job)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


# endpoint to add schedule_id to a job
@db_api.route("/job/schedule/<seq>", methods=["POST"])
def update_job_schedule_id(seq):
    data = json.loads(request.data)
    schedule_id = data['schedule_id']
    this_job = db_schema.Job.query.get(seq)
    this_job.schedule_id = schedule_id
    db_schema.db.session.commit()

    resp = job_schema.jsonify(this_job)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


# endpoint to get jobs of a client
@db_api.route("/job/<client>", methods=["GET"])
def get_jobs_of_a_client(client):
    jobs = db_schema.Job.query.filter(db_schema.Job.client == client)

    resp = jobs_schema.jsonify(jobs)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


# TODO to be deleted in the future
# # endpoint to add module
# @db_api.route("/module", methods=["POST"])
# def add_module():
#     data = json.loads(request.data)
#
#     name = data['name']
#     description = data['description']
#
#     new_module = db_schema.Module(name, description)
#
#     db_schema.db.session.add(new_module)
#     db_schema.db.session.commit()
#
#     resp = module_schema.jsonify(new_module)
#     resp.headers.add('Access-Control-Allow-Origin', '*')
#     return resp
#
#
# # endpoint to show all modules
# @db_api.route("/module", methods=["GET"])
# def get_module():
#     all_modules = db_schema.Module.query.all()
#     result = modules_schema.dump(all_modules)
#
#     resp = jsonify(result.data)
#     resp.headers.add('Access-Control-Allow-Origin', '*')
#     return resp
#
#
# # endpoint to add persona
# @db_api.route("/persona", methods=["POST"])
# def add_persona():
#     data = json.loads(request.data)
#
#     name = data['name']
#     engine = data['engine']
#     interest = []
#     account = dict()
#
#     new_persona = db_schema.Persona(name, engine, interest, account)
#
#     db_schema.db.session.add(new_persona)
#     db_schema.db.session.commit()
#
#     resp = persona_schema.jsonify(new_persona)
#     resp.headers.add('Access-Control-Allow-Origin', '*')
#     return resp

# "client": "client",
    # "connection_name": "client_tcp_channel",
    # "module": "mod_visit_any_page",
    # "interval": 5,
    # "para": {
    #     "url": "https://www.google.com"
    # },
    # "ip": "10.0.26.4",
    # "new_ip": "10.0.26.4",
    # "system": "Linux",
    # "version": "Ubuntu 16.0.4",
    # "name": "mod_visit_any_page",
    # "description": "{'desc': 'visit any web page', 'para':{'url':'https://www.google.com'}}}"
