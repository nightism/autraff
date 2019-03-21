from flask import Flask, request, Response, jsonify
import json
from datetime import datetime

from service import app, db
from db_schema import Client, ClientSchema
from db_schema import Module, ModuleSchema
from db_schema import Persona, PersonaSchema
from db_schema import Job, JobSchema


client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)

module_schema = ModuleSchema()
modules_schema = ModuleSchema(many=True)

persona_schema = PersonaSchema()
personas_schema = PersonaSchema(many=True)

job_schema = JobSchema()
jobs_schema = JobSchema(many=True)


# endpoint to create new client
@app.route("/client", methods=["POST"])
def add_client():
    ip = request.json['ip']
    system = request.json['system']
    version = request.json['version']

    new_client = Client(ip, system, version)

    db.session.add(new_client)
    db.session.commit()

    resp = client_schema.jsonify(new_client)
    resp.headers.add('Access-Control-Allow-Origin', '*')

    return resp


# endpoint to show all clients
@app.route("/client", methods=["GET"])
def get_client():
    all_clients = Client.query.all()
    result = clients_schema.dump(all_clients)

    resp = jsonify(result.data)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


# endpoint to get client detail by ip
@app.route("/client/<ip>", methods=["GET"])
def client_detail(ip):
    client = Client.query.get(ip)

    resp = client_schema.jsonify(client)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


# endpoint to update client
@app.route("/client", methods=["PUT"])
def client_update():
    data = json.loads(request.data)
    ip = data['ip']
    client = Client.query.get(ip)
    new_ip = data['new_ip']
    system = data['system']
    version = data['version']

    client.ip = new_ip
    client.system = system
    client.version = version

    db.session.commit()

    resp = client_schema.jsonify(client)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


# endpoint to delete client
@app.route("/client", methods=["DELETE"])
def client_delete():
    data = json.loads(request.data)
    ip = data['ip']
    client = Client.query.get(ip)
    db.session.delete(client)
    db.session.commit()

    resp = client_schema.jsonify(client)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


# endpoint to add module
@app.route("/module", methods=["POST"])
def add_module():
    data = json.loads(request.data)

    name = data['name']
    description = data['description']

    new_module = Module(name, description)

    db.session.add(new_module)
    db.session.commit()

    resp = module_schema.jsonify(new_module)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


# endpoint to show all modules
@app.route("/module", methods=["GET"])
def get_module():
    all_modules = Module.query.all()
    result = modules_schema.dump(all_modules)

    resp = jsonify(result.data)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


# endpoint to add persona 
@app.route("/persona", methods=["POST"])
def add_persona():
    data = json.loads(request.data)

    name = data['name']
    engine = data['engine']
    interest = []  # TODO validate as a list
    account = dict()  # TODO validate as a dict

    new_persona = Persona(name, engine, interest, account)

    db.session.add(new_persona)
    db.session.commit()

    resp = persona_schema.jsonify(new_persona)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


# endpoint to add job
@app.route("/job", methods=["POST"])
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

    new_job = Job(name, module, client, interval, dt_obj, arguments=arguments)
    db.session.add(new_job)
    db.session.commit()

    resp = job_schema.jsonify(new_job)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


# endpoint to show all job
@app.route("/job", methods=["GET"])
def get_jobs():
    all_jobs = Job.query.all()
    result = jobs_schema.dump(all_jobs)

    resp = jsonify(result.data)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


# endpoint to show one job
@app.route("/job/<id>/detail", methods=["GET"])
def get_a_single_job(id):
    job = Job.query.get(id)

    resp = job_schema.jsonify(job)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


# endpoint to update one job
@app.route("/job/<id>", methods=["PUT"])
def update_a_job(id):
    job = Job.query.get(id)

    data = json.loads(request.data)
    job.name = data['name']
    # job.persona = request.json['persona']
    job.interval = int(data['interval'])
    job.start = datetime.strptime(data['start'], '%Y-%m-%d %H:%M:%S')
    job.arguments = data['arguments']
    print(job.arguments)

    db.session.commit()

    resp = job_schema.jsonify(job)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


# endpoint to add schedule_id to a job
@app.route("/job/schedule/<seq>", methods=["POST"])
def update_job_schedule_id(seq):
    print("test")
    # print(seq)
    # this_job = {
    #     "test": "test"
    # }
    data = json.loads(request.data)
    schedule_id = data['schedule_id']
    this_job = Job.query.get(seq)
    this_job.schedule_id = schedule_id
    db.session.commit()

    resp = job_schema.jsonify(this_job)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


# endpoint to get jobs of a client
@app.route("/job/<client>", methods=["GET"])
def get_jobs_of_a_client(client):
    print(client)
    jobs = Job.query.filter(Job.client == client)

    resp = jobs_schema.jsonify(jobs)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp

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



