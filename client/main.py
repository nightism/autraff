from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import STATE_STOPPED, STATE_PAUSED, STATE_RUNNING
from osbrain import NSProxy
from osbrain import run_agent

import time

from modules import *

NAMESERVER_ADDRESS = '127.0.0.1:26000'
CLIENT_RECEIVER_ADDRESS = '127.0.0.1:27000'
CLIENT_NAME = '127.0.0.1'
CLIENT_ALIAS = 'client-' + CLIENT_NAME

scheduler = None


def receive_command(agent, message):
    """
    handler for osBrain client to reply the server request.
    :para: agent object and message odject transmitted
    """

    global scheduler

    try:
        # TODO the following codes do not work, needs to figure out why
        # print('[Scheduler] status: ' + str(scheduler.state))
        # if scheduler.state == STATE_STOPPED or scheduler.state == STATE_PAUSED:
        #     print('[Scheduler] Background Scheduler restarted.')
        #     scheduler.start()
        if scheduler is None:
            scheduler = BackgroundScheduler()
            scheduler.start()
            print('[Scheduler] Background Scheduler started, status ' + str(scheduler.state))
    except Exception as err:
        print(str(err))

    command = message['command']
    # print(command)

    if command == 'schedule_task':
        mod_name = message['module']
        mod = eval(mod_name)
        print("[Scheduler] Scheduling task " + mod_name)

        interval = int(message['interval'])
        para = message['para']

        schedule_id = scheduler.add_job(lambda: mod.execute(para), 'interval', seconds=interval).id
        # print('Job scheduled: ' + str(id))
        return schedule_id

    elif command == 'delete_task':
        mod_id = message['job_id']
        rc = scheduler.remove_job(mod_id)
        return "DEL"
    elif command == 'retrieve_logs':
        log_file = open('./geckodriver.log').read()
        return log_file

    return "NAN"


if __name__ == '__main__':
    try:
        # global scheduler
        # scheduler = BackgroundScheduler()
        # scheduler.start()
        # print('[Scheduler] Background Scheduler started, status ' + str(scheduler.state))

        ns = NSProxy(nsaddr=NAMESERVER_ADDRESS)
        client = run_agent(CLIENT_ALIAS, nsaddr=NAMESERVER_ADDRESS)

        client.bind('REP', alias="request_addr", handler=receive_command, transport='tcp',
                    addr=CLIENT_RECEIVER_ADDRESS)
    except Exception as e:
        print("Error occurred.")
        print(str(e))
        raise e

    print("[General] client successfully initiated.")
