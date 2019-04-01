from flask import request, jsonify
from flask import Blueprint

from osbrain import NSProxy
from osbrain import run_agent
from osbrain import run_nameserver

import json

from utils.constants import *
from utils.request_utils import create_response

control_api = Blueprint('control_api', __name__)

ns = None
controller = None


@control_api.route("/open-connection", methods=["POST"])
def open_connection():
    try:
        global ns
        global controller

        ns = run_nameserver(NAMESERVER_ADDRESS)
        controller = run_agent(CONTROLLER_ALIAS)
        result = {
            "result": "success"
        }
        resp = create_response(result)
        return resp
    except Exception:
        result = {
            "result": "fail"
        }
        resp = create_response(result)
        return resp


@control_api.route("/check-connection", methods=["POST"])
def check_nameserver_connection():
    try:
        global ns
        if ns is None:
            ns = NSProxy(nsaddr=NAMESERVER_ADDRESS)

        pong = ns.ping()
        if pong != 'pong':
            raise Exception()

        # ns.proxy(CONTROLLER_ALIAS)

        result = {
            "result": "nameserver is running."
        }
        resp = create_response(result)
        return resp
    except Exception:
        result = {
            "result": "nameserver is malfunctioning."
        }
        resp = create_response(result)
        return resp


@control_api.route("/check-controller-connection", methods=["GET"])
def check_controller_connection():
    try:
        global ns
        global controller
        if ns is None:
            ns = NSProxy(nsaddr=NAMESERVER_ADDRESS)

        if controller is None:
            ns.proxy(CONTROLLER_ALIAS)

        pong = controller.ping()
        if pong != 'pong':
            raise Exception()

        result = {
            "result": "controller backend is running."
        }
        resp = create_response(result)
        return resp
    except Exception:
        result = {
            "result": "controller backend is malfunctioning."
        }
        resp = create_response(result)
        return resp


@control_api.route("/check-connection-naive", methods=["GET"])
def check_connection_naive():
    ns_address = ""
    controller_name = ""

    try:
        if ns is not None and ns.ping() == 'pong':
            ns_address = NAMESERVER_ADDRESS
        if controller is not None and controller.ping() == 'pong':
            controller_name = CONTROLLER_ALIAS
    except:
        pass

    result = {
        "nameserver": ns_address,
        "controller": controller_name,
    }
    resp = create_response(result)
    return resp

@control_api.route("/connect-to-client", methods=["POST"])
def connect_to_client():
    try:
        global ns
        global controller

        if ns is None:
            ns = NSProxy(nsaddr=NAMESERVER_ADDRESS)

        if controller is None:
            controller = ns.proxy(CONTROLLER_ALIAS)

        data = json.loads(request.data)
        client_name = data['client']

        req_addr = ns.proxy(CLIENT_PREFIX + client_name).addr(COMMUNICATION_CHANNEL)
        connection_name = client_name + CONNECTION_SUFFIX
        controller.connect(req_addr, connection_name)

        result = {
            "result": "success"
        }
        resp = create_response(result)
        return resp
    except Exception as e:
        result = {
            "result": "client is malfunctioning."
        }
        resp = create_response(result)
        return resp

    return connection_name


@control_api.route("/check-client-connection/<client>", methods=["GET"])
def check_client_connection(client):
    try:
        global ns
        global controller

        if ns is None:
            ns = NSProxy(nsaddr=NAMESERVER_ADDRESS)

        if controller is None:
            controller = ns.proxy(CONTROLLER_ALIAS)

        client_name = CLIENT_PREFIX + client
        connection_name = client + CONNECTION_SUFFIX

        req_addr = ns.proxy(client_name).addr(COMMUNICATION_CHANNEL)
        controller.connect(req_addr, connection_name)

        result = {
            "result": "success"
        }
        resp = create_response(result)
        return resp
    except Exception as e:
        result = {
            "result": "client is malfunctioning."
        }
        resp = create_response(result)
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
