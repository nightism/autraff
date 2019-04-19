import json
from datetime import datetime
from flask import request, jsonify
from flask import Blueprint

from database import db_schema

from utils.request_utils import create_response
from utils.request_utils import add_cors_support

db_api = Blueprint('db_job_api', __name__)

job_schema = db_schema.JobSchema()
jobs_schema = db_schema.JobSchema(many=True)


# endpoint to add job
@db_api.route("/job", methods=["POST"])
def add_job():
    # TODO this api is out of date, but it's ok for now since it is not used by front end

    data = json.loads(request.data)

    name = data['name']
    module = data['module']
    client = data['client']

    interval = int(data['interval'])
    date_time = data['start']
    dt_obj = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')

    arguments = data['arguments']

    new_job = db_schema.Job(name, module, client, interval, dt_obj, arguments=arguments)
    db_schema.db.session.add(new_job)
    db_schema.db.session.commit()

    resp = add_cors_support(job_schema.jsonify(new_job))
    return resp


# endpoint to show all job
@db_api.route("/job", methods=["GET"])
def get_jobs():
    all_jobs = db_schema.Job.query.all()
    result = jobs_schema.dump(all_jobs)

    resp = create_response(result.data)
    return resp


# endpoint to show the details of one job
@db_api.route("/job/<name>/detail", methods=["GET"])
def get_a_single_job(name):
    job = db_schema.Job.query.get(name)

    resp = add_cors_support(job_schema.jsonify(job))
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
    resp = add_cors_support(resp)
    return resp


# endpoint to get jobs of a client
@db_api.route("/job/<client>", methods=["GET"])
def get_jobs_of_a_client(client):
    jobs = db_schema.Job.query.filter(db_schema.Job.client == client)

    resp = jobs_schema.jsonify(jobs)
    resp = add_cors_support(resp)
    return resp


# endpoint to update one job
@db_api.route("/job/<seq>", methods=["PUT"])
def update_a_job(seq):
    # TODO this api is out of date, but it's ok for now since it is not used by front end

    job = db_schema.Job.query.get(seq)

    data = json.loads(request.data)
    job.name = data['name']
    # job.persona = request.json['persona']
    job.interval = int(data['interval'])
    job.start = datetime.strptime(data['start'], '%Y-%m-%d %H:%M:%S')
    job.arguments = data['arguments']
    print(job.arguments)

    db_schema.db.session.commit()

    resp = job_schema.jsonify(job)
    resp = add_cors_support(resp)
    return resp
