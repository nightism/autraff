from apscheduler.schedulers.background import BackgroundScheduler
from osbrain import NSProxy
from osbrain import run_agent
from selenium import webdriver

import time

from modules import *

NAMESERVER_ADDRESS = '127.0.0.1:26000'
CLIENT_RECEIVER_ADDRESS = '127.0.0.1:27000'
CLIENT_ALIAS = 'client'


scheduler = BackgroundScheduler()


def receive_command(agent, message):
    """
    handler for osBrain client to reply the server request.
    :para: agent object and message odject transmitted
    """
    if scheduler.state == 0:
        scheduler.start()

    command = message['command']

    if command == 'schedule_task':
        mod_name = message['module']
        mod = eval(mod_name)
        # print("Scheduling task " + mod_name)

        interval = int(message['interval'])
        para = message['para']
        job = lambda : mod.execute(para)

        id = scheduler.add_job(job, 'interval', seconds=interval).id
        # print('Job scheduled: ' + str(id))
        return id

    elif command == 'delete_task':
        mod_id = message['mod_id']
        rc = scheduler.remove_job(mod_id)
        return "DEL"


def lambda_job(para, driver=None):
    return lambda : execute(para, driver)


if __name__ == '__main__':

    ns = NSProxy(nsaddr=NAMESERVER_ADDRESS)
    client = run_agent(CLIENT_ALIAS, nsaddr=NAMESERVER_ADDRESS)  # TODO change the alias

    client.bind('REP', alias='request_addr', handler=receive_command, transport='tcp', addr=CLIENT_RECEIVER_ADDRESS)
