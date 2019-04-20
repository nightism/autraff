from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import STATE_STOPPED, STATE_PAUSED, STATE_RUNNING
from osbrain import NSProxy
from osbrain import run_agent

import os
from _datetime import datetime

from modules import *  # evaluated at run time, do not delete
from util.constants import BASE_DIR
from util.constants import LOG_FILE
from util.constants import DRIVER_LOG
from util.log.general_logger import logger

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
            logger('Background Scheduler started, status ' + str(scheduler.state), header="[Scheduler]")
    except Exception as err:
        print(str(err))

    command = message['command']
    # print(command)

    if command == 'schedule_task':
        mod_name = message['module']
        mod = eval(mod_name)
        logger("Scheduling module " + mod_name, header="[Scheduler]")

        interval = int(message['interval'])
        para = message['para']

        schedule_id = scheduler.add_job(lambda: mod.execute(para), 'interval', seconds=interval).id

        # print('Job scheduled: ' + str(id))
        logger("Scheduled module " + mod_name + " with id " + schedule_id, header="[Scheduler]")

        return schedule_id

    elif command == 'delete_task':
        mod_id = message['job_id']

        # TODO to check the return code rc
        rc = scheduler.remove_job(mod_id)

        logger("Stopping job " + mod_id, header="[Scheduler]")
        return "DEL"

    elif command == 'get_usage_logs':
        if not os.path.exists(LOG_FILE):
            return []

        log_file = open(LOG_FILE)
        log_str_list = []
        for line in log_file:
            log_str_list.append(line.strip())

        log_file.close()

        return log_str_list
    elif command == 'get_driver_logs':
        if not os.path.exists(DRIVER_LOG):
            return []

        log_file = open(DRIVER_LOG)
        log_str_list = []
        for line in log_file:
            log_str_list.append(line.strip())

        log_file.close()

        return log_str_list
    else:
        return "INVALID_COMMAND"


if __name__ == '__main__':
    if os.path.exists(LOG_FILE):
        file_time = datetime.fromtimestamp((os.path.getmtime(LOG_FILE))).strftime(".%Y%m%d.%H%M%S")
        os.rename(LOG_FILE, LOG_FILE + file_time)

    if os.path.exists(DRIVER_LOG):
        file_time = datetime.fromtimestamp((os.path.getmtime(DRIVER_LOG))).strftime(".%Y%m%d.%H%M%S")
        os.rename(DRIVER_LOG, BASE_DIR + '/logs/driver.log' + file_time)

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

    logger("Client successfully initiated.")
