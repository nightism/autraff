from flask import request, jsonify
from flask import Blueprint

from osbrain import NSProxy
from osbrain import run_agent
from osbrain import run_nameserver

import json

from utils.constants import *
from utils.request_utils import create_response

control_api = Blueprint('control_api', __name__)

ns = run_nameserver(NAMESERVER_ADDRESS)
controller = run_agent(CONTROLLER_ALIAS)

# http://localhost:5000/open-connection


@control_api.route("/open-connection", methods=["GET"])
def open_connection():
    try:
        global ns
        global controller

        # TODO Logic is a bit flawed, to be refined
        if ns is None:
            ns = run_nameserver(NAMESERVER_ADDRESS)

        if controller is None:
            controller = run_agent(CONTROLLER_ALIAS)
        result = {
            "result": "success",
            "nameserver": NAMESERVER_ADDRESS,
            "controller": CONTROLLER_ALIAS,
        }
        resp = create_response(result)
        return resp
    except Exception:
        result = {
            "result": "fail",
            "nameserver": "",
            "controller": "",
        }
        resp = create_response(result)
        return resp


@control_api.route("/nameserver/debug", methods=["POST"])
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


@control_api.route("/controller/debug", methods=["GET"])
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


@control_api.route("/controller/status", methods=["GET"])
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


@control_api.route("/connect/all", methods=["POST"])
def connect_to_all_client():
    try:
        from sqlite3 import connect
        from utils.constants import DB_PATH

        conn = connect(DB_PATH)
        c = conn.cursor()

        result = c.execute('SELECT ip FROM client')

        success = []

        for client in result.fetchall():
            try:
                client_name = client[0]
                req_addr = ns.proxy(CLIENT_PREFIX + client_name).addr(COMMUNICATION_CHANNEL)
                connection_name = client_name + CONNECTION_SUFFIX
                controller.connect(req_addr, connection_name)
                success.append(client_name)
            except Exception:
                pass

        c.close()

        return create_response({
            "success": success,
            "result": 'connected to clients: ' + str(success),
        })
    except Exception:
        result = {
            "result": "connection error."
        }
        resp = create_response(result)
        return resp


@control_api.route("/connect", methods=["POST"])
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
    except Exception as err:
        result = {
            "result": "client is malfunctioning."
        }
        resp = create_response(result)
        return resp


@control_api.route("/connect/<client>", methods=["GET"])
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


def create_job_obj(job_name):
    from sqlite3 import connect
    from utils.constants import DB_PATH

    conn = connect(DB_PATH)
    c = conn.cursor()

    if job_name is None or job_name == "":
        c.close()
        return {}

    c.execute('SELECT interval, module, arguments, success, failure FROM Job WHERE name = "' + job_name + '"')
    job = c.fetchall()[0]

    job_obj = {
        "interval": job[0],
        "module": job[1],
        "arguments": eval(job[2]),
        "success": create_job_obj(job[3]),
        'failure': create_job_obj(job[4]),
    }
    return job_obj


@control_api.route("/scheduling/schedule", methods=["POST"])
def schedule_job():
    global ns
    global controller

    if ns is None:
        ns = NSProxy(nsaddr=NAMESERVER_ADDRESS)
    if controller is None:
        controller = ns.proxy(CONTROLLER_ALIAS)

    from sqlite3 import connect
    from utils.constants import DB_PATH

    conn = connect(DB_PATH)
    c = conn.cursor()

    data = json.loads(request.data)
    connection_name = data['client'] + CONNECTION_SUFFIX
    job_name = data['name']
    job = create_job_obj(job_name)

    message = {
        # TODO some redundant information to be removed
        'command': COMMAND_SCHEDULE_TASK,
        'interval': int(data['interval']),
        'module': data['module'],
        'para': eval(data['para']),
        'job': job
    }

    controller.send(connection_name, message)
    reply = controller.recv(connection_name)

    result = {
        'schedule_id': str(reply)
    }

    resp = create_response(result)
    return resp


@control_api.route("/scheduling/stop", methods=["POST"])
def stop_job():
    global ns
    global controller

    if ns is None:
        ns = NSProxy(nsaddr=NAMESERVER_ADDRESS)
    if controller is None:
        controller = ns.proxy(CONTROLLER_ALIAS)
    data = json.loads(request.data)

    connection_name = data['client'] + CONNECTION_SUFFIX
    message = {
        'command': COMMAND_DELETE_TASK,
        'job_id': data['job_schedule_id'],
    }

    controller.send(connection_name, message)
    reply = controller.recv(connection_name)

    result = {
        'schedule_id': str(reply)
    }

    resp = create_response(result)
    return resp
