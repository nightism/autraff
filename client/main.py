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

scheduler = BackgroundScheduler()


def receive_command(agent, message):
    """
    handler for osBrain client to reply the server request.
    :para: agent object and message odject transmitted
    """
    print('test1')

    try:
        print("exco??")
        if scheduler.state == STATE_STOPPED or scheduler.state == STATE_PAUSED:
            # scheduler =
            print("wat??")
            scheduler.start()
            print("wat???")
    except Exception as e:
        print(e)
        print(str(e))

    print('test2')

    command = message['command']
    print(command)

    if command == 'schedule_task':
        print("test3")
        mod_name = message['module']
        mod = eval(mod_name)
        # print("Scheduling task " + mod_name)

        interval = int(message['interval'])
        para = message['para']
        job = lambda: mod.execute(para)

        id = scheduler.add_job(job, 'interval', seconds=interval).id
        # print('Job scheduled: ' + str(id))
        return id

    elif command == 'delete_task':
        mod_id = message['job_id']
        rc = scheduler.remove_job(mod_id)
        return "DEL"

    return "NAN"


if __name__ == '__main__':
    # keyword = input()
    # mod_human_web_browsing.execute({
    #     'keyword': keyword,
    #     'time': 10
    # })

    try:
        ns = NSProxy(nsaddr=NAMESERVER_ADDRESS)
        client = run_agent(CLIENT_ALIAS, nsaddr=NAMESERVER_ADDRESS)

        client.bind('REP', alias="request_addr", handler=receive_command, transport='tcp',
                    addr=CLIENT_RECEIVER_ADDRESS)
    except Exception as e:
        print("Error occurred.")
        print(str(e))
        raise e

    print("client successfully initiated.")


