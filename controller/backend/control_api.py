from flask import request, jsonify
from flask import Blueprint

from osbrain import NSProxy
from osbrain import run_agent
from osbrain import run_nameserver

import json

from utils.constants import *

control_api = Blueprint('control_api', __name__)


@control_api.route("/open-connection", methods=["POST"])
def open_connection():
    try:
        run_nameserver(NAMESERVER_ADDRESS)
        run_agent(CONTROLLER_ALIAS)
        result = {
            "result": "success"
        }
        resp = jsonify(result)
        resp.headers.add('Access-Control-Allow-Origin', '*')
        return resp
    except Exception:
        result = {
            "result": "fail"
        }
        resp = jsonify(result)
        resp.headers.add('Access-Control-Allow-Origin', '*')
        return resp


@control_api.route("/check-connection", methods=["POST"])
def check_connection():
    try:
        ns = NSProxy(nsaddr=NAMESERVER_ADDRESS)
        ns.proxy(CONTROLLER_ALIAS)
        result = {
            "result": "nameserver is running."
        }
        resp = jsonify(result)
        resp.headers.add('Access-Control-Allow-Origin', '*')
        return resp
    except Exception:
        result = {
            "result": "nameserver is malfunctioning."
        }
        resp = jsonify(result)
        resp.headers.add('Access-Control-Allow-Origin', '*')
        return resp


@control_api.route("/connect-to-client", methods=["POST"])
def connect_to_client():
    try:
        print("test")
        ns = NSProxy(nsaddr=NAMESERVER_ADDRESS)
        controller = ns.proxy(CONTROLLER_ALIAS)

        data = json.loads(request.data)
        client_name = data['client']

        req_addr = ns.proxy(CLIENT_PREFIX + client_name).addr(COMMUNICATION_CHANNEL)
        connection_name = client_name + CONNECTION_SUFFIX
        controller.connect(req_addr, connection_name)

        result = {
            "result": "success"
        }
        resp = jsonify(result)
        resp.headers.add('Access-Control-Allow-Origin', '*')
        return resp
    except Exception as e:
        result = {
            "result": "client is malfunctioning."
        }
        resp = jsonify(result)
        resp.headers.add('Access-Control-Allow-Origin', '*')
        return resp

    return connection_name


@control_api.route("/schedule-job", methods=["POST"])
def schedule_job():
    print("test2")
    ns = NSProxy(nsaddr=NAMESERVER_ADDRESS)
    controller = ns.proxy(CONTROLLER_ALIAS)
    print("test3")
    data = json.loads(request.data)
    print("test4")
    connection_name = data['connection_name']
    message = {
        'command': COMMAND_SCHEDULE_TASK,
        'interval': int(data['interval']),
        'module': data['module'],
        'para': eval(data['para']),
    }

    controller.send(connection_name, message)
    reply = controller.recv(connection_name)
    print("test5")

    result = {
        'schedule_id': str(reply)
    }

    resp = jsonify(result)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


@control_api.route("/stop-job", methods=["POST"])
def stop_job():
    ns = NSProxy(nsaddr=NAMESERVER_ADDRESS)
    controller = ns.proxy(CONTROLLER_ALIAS)

    data = json.loads(request.data)

    connection_name = data['connection_name']
    message = {
        'command': COMMAND_DELETE_TASK,
        'job_id': data['job_schedule_id'],
    }

    controller.send(connection_name, message)
    reply = controller.recv(connection_name)

    result = {
        'schedule_id': str(reply)
    }

    resp = jsonify(result)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp
