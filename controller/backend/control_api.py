from flask import Flask, request, Response, jsonify

from osbrain import NSProxy
from osbrain import run_agent
from osbrain import run_nameserver

import json

from service import app, db


NAMESERVER_ADDRESS = '127.0.0.1:26000'
CONTROLLER_ALIAS = 'server'
COMMUNICATION_CHANNEL = 'request_addr'
CLIENT_PREFIX = 'client-'
CONNECTION_SUFFIX = '_tcp_channel'

COMMAND_SCHEDULE_TASK = 'schedule_task'
COMMAND_DELETE_TASK = 'delete_task'
COMMAND_GET_LOG = 'get_log'


@app.route("/open-connection", methods=["POST"])
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


@app.route("/check-connection", methods=["POST"])
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


@app.route("/connect_to_client", methods=["POST"])
def connect_to_client():
    try:
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


@app.route("/schedule-job", methods=["POST"])
def schedule_job():
    ns = NSProxy(nsaddr=NAMESERVER_ADDRESS)
    controller = ns.proxy(CONTROLLER_ALIAS)

    data = json.loads(request.data)

    connection_name = data['connection_name']
    message = {
        'command': COMMAND_SCHEDULE_TASK,
        'interval': int(data['interval']),
        'module': data['module'],
        'para': eval(data['para']),
    }

    controller.send(connection_name, message)
    reply = controller.recv(connection_name)

    result = {
        'schedule_id': str(reply)
    }

    resp = jsonify(result)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


@app.route("/stop-job", methods=["POST"])
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
